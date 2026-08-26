#!/usr/bin/env python3
"""COMPLETION-CLAIM VERIFICATION.  DELTA R56/B2.

**A record of a fix is not a fix, and a FALSE record of a fix is worse than no record:
it converts an open defect into a closed one in the reader's mind.**

Check (ix) asks whether a HAND-REGISTERED withdrawn claim is asserted live. This asks
the more general question, and derives its own register: wherever commentary says a
correction happened - "previously read X", "X is struck", "corrected to Y" - **that
sentence is itself a claim**, and it is checked against the operative field.

WHY IT GENERALISES (ix). (ix) only knows what someone remembered to register. This knows
whatever the drafter WROTE DOWN as done, which is exactly the set at risk: a drafter who
records a correction believes it was made. The instance: H10's justification said the
model-family claim "is struck from both" while it stood in operative_text for two rounds.

THE RULE. Where commentary quotes text and says it was removed/struck/corrected/no longer
present, that quoted text must not appear in the same hunk's operative_text except as a
QUOTATION (inside quote marks near a struck-marker). Quoting makes it a mention; bare
presence makes it a use.

LIMIT, stated rather than implied: this reads quoted claims only. A completion claim that
paraphrases rather than quotes ("the family-change ground was removed") is not machine
-checkable here and is not caught. Reported as UNQUOTED-CLAIM so the count is visible.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

COMMENTARY = ("what_changes", "justification")
WINDOW = 320

# commentary patterns that assert a correction is COMPLETE, each capturing the quoted text
# The gap between the quotation and the completion marker must allow SENTENCES, not
# merely clauses. The first draft required them within 120 chars with no intervening
# period, and MISSED the instance it was written for. The real commentary reads:
#     ... also said "the anchor's model family changed", relying on A.1 item 2. That
#     claim was FALSE against its own cited source ... and is struck from both.
# - two sentences apart. Mutation testing found that; reading the regex did not. H-L16.
_DONE = (r"(?:is|was|has been)\s+(?:struck|removed|corrected|withdrawn)"
         r"|stood here until|no longer (?:appears|stands)")
CLAIM_PATTERNS = [
    re.compile(r"previously read[:,]?\s*" + '[\\"\\u201c]' + r"(.{12,400}?)" + '[\\"\\u201d]', re.S),
    re.compile('[\\"\\u201c]' + r"(.{12,400}?)" + '[\\"\\u201d]' + r".{0,400}?(?:" + _DONE + r")", re.S),
    re.compile(r"(?:" + _DONE + r").{0,400}?" + '[\\"\\u201c]' + r"(.{12,400}?)" + '[\\"\\u201d]', re.S),
]
# commentary that asserts completion WITHOUT quoting what was removed
UNQUOTED = re.compile(
    r"\bis struck from both\b|\bhas been (?:removed|struck|corrected)\b|"
    r"\bwas (?:removed|struck) from\b|\bno longer appears\b", re.I)
DEAD_MARK = re.compile(
    r"struck|WITHDRAWN|withdrawn|SUPERSEDED|superseded|NOT operative|not operative|"
    r"stood here until|previously read|is false|was false", re.I)


def _quoted_in(op, frag):
    """Is every occurrence of frag inside op a QUOTATION marked as dead?"""
    for m in re.finditer(re.escape(frag), op):
        a, b = max(0, m.start() - WINDOW), min(len(op), m.end() + WINDOW)
        ctx = op[a:b]
        rel_s, rel_e = m.start() - a, m.end() - a
        lo = max(ctx.rfind('"', 0, rel_s), ctx.rfind("\u201c", 0, rel_s))
        hi = max(ctx.find('"', rel_e), ctx.find("\u201d", rel_e))
        if not (lo >= 0 and hi >= 0 and DEAD_MARK.search(ctx)):
            return False
    return True


def run(verbose=True):
    hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]

    def ln(h):
        m = re.search(r"\d+", h.get("prereg_line", "") or "")
        return int(m.group(0)) if m else 9999

    HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}
    checked, false_records, unquoted = 0, [], []
    for hid, h in HN.items():
        op = h.get("operative_text") or ""
        for fld in COMMENTARY:
            txt = h.get(fld) or ""
            for pat in CLAIM_PATTERNS:
                for m in pat.finditer(txt):
                    frag = re.sub(r"\s+", " ", m.group(1)).strip()
                    if len(frag) < 12:
                        continue
                    checked += 1
                    if frag in re.sub(r"\s+", " ", op) and not _quoted_in(
                            re.sub(r"\s+", " ", op), frag):
                        false_records.append((hid, fld, frag[:90]))
            for m in UNQUOTED.finditer(txt):
                a, b = max(0, m.start() - 200), min(len(txt), m.end() + 200)
                if not re.search(r"[\"\u201c]", txt[a:b]):
                    unquoted.append((hid, fld, txt[a:b][:90]))

    if verbose:
        print("  completion claims found in commentary and verified : %d" % checked)
        print("  FALSE RECORDS (commentary says removed, operative still asserts it): %d"
              % len(false_records))
        for hid, fld, frag in false_records:
            print("    *** %s.%s claims removal of %r \u2014 still LIVE in operative_text"
                  % (hid, fld, frag))
        print("  completion claims that QUOTE NOTHING (not machine-checkable): %d"
              % len(unquoted))
        for hid, fld, ctx in unquoted[:4]:
            print("        %s.%s: %r" % (hid, fld, ctx))
        if not false_records:
            print("  PASS \u2014 every quoted completion claim is true of the operative field")
    return false_records


if __name__ == "__main__":
    import sys
    sys.exit(1 if run() else 0)
