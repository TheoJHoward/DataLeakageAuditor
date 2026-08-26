#!/usr/bin/env python3
"""Z4 — scrub PRACTICES.md of references that resolve only to unpublished files,
then report. Writes the scrubbed text to a NEW scratch file; landing it at the repo
root is a separate, explicit step.

Every rule asserts its match count. Nothing is written if any assert fails.

Usage:
    python _Z4_scrub_practices.py            # dry run, show every change
    python _Z4_scrub_practices.py --write    # write the scrubbed draft
"""

import re
import sys
import hashlib

SCRATCH = ("C:/Users/ttbea/AppData/Local/Temp/claude/"
           "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
           "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
SRC = SCRATCH + "/amendment/PRACTICES.md"
OUT = SCRATCH + "/amendment/PRACTICES.scrubbed.md"

SRC_SHA = "0163335313b85c5171ad08620bba0d3fc6840e7cb4502a6a1fcf93448e4e4db6"

# ---------------------------------------------------------------- literal rules
# (name, old, new, expected_count)
LITERAL = [
    ("title: drop the task label",
     "# PRACTICES.md \u2014 non-normative working practices carried out of the v30a availability declaration (item K3)",
     "# PRACTICES.md \u2014 non-normative working practices carried out of the v30a availability declaration",
     1),

    ("preamble: working-resolution number -> registered section",
     "**`PREREG.md` does not cite this file.** Under working resolution R21, `PREREG.md` is the single\n"
     "normative source for measurement semantics and it references nothing here. The availability\n"
     "declaration may point to an entry below where a practice was removed from it by the K4 scrub, and\n"
     "such a pointer is a breadcrumb for a reader, not a citation of authority.",
     "**`PREREG.md` does not cite this file.** `PREREG.md` is the single normative source for\n"
     "measurement semantics (\u00a70.2.1) and it references nothing here. The availability declaration may\n"
     "point to an entry below where a practice was removed from it by the v30a scrub, and such a\n"
     "pointer is a breadcrumb for a reader, not a citation of authority.",
     1),

    ("contents: classification described, not labelled",
     "that J1 classified NON-GATE and that K1, applying R25, left outside `PREREG.md`: reporting,\n"
     "provenance, labelling, and evidence-accounting practices that neither determine a gate verdict nor\n"
     "protect the integrity of a declared instance.",
     "classified as neither gate-determining nor integrity-protecting, and therefore left outside\n"
     "`PREREG.md` by the schema pass: reporting, provenance, labelling, and evidence-accounting\n"
     "practices that neither determine a gate verdict nor protect the integrity of a declared instance.",
     1),

    ("scope and provenance: remove scratch path, scratch hash, and unpublished-file citations",
     "**Scope and provenance.** Source rows are identified by the J1 row id\n"
     "(`J1_GATE_CRITICAL_CLASSIFICATION.md` \u00a73) and K1's disposition table (`K1_SCHEMA_CLAUSES.md` \u00a73,\n"
     "\"REMAINING PRACTICES (19 rows)\"). Declaration line numbers are those of the scratch copy before the\n"
     "K4 scrub (`applied\\AVAILABILITY_DECLARATION.md`, 3,695 lines, sha256 `1290186e\u20261c30`); the scrub\n"
     "replaces each source passage with a pointer to the entry here (K4_SCRUB_DIFF.md records every such\n"
     "edit). The entries are numbered by their J1 row id (P-02 is J1 row 2, and so on) so the mapping is\n"
     "checkable without a concordance.",
     "**Scope and provenance.** Each entry carries a `P-NN` identifier, unique within this file and\n"
     "stable across revisions. Each entry names the declaration **section** its source passage came\n"
     "from, and the v30a scrub replaces that passage with a pointer to the entry here. Sections are\n"
     "named rather than line numbers given, because line numbers move whenever the declaration is\n"
     "edited and a stale line number is worse than none.",
     1),

    ("P-02 source: elide the unpublished labels inside the quotation",
     "the bullet \"Generation-naming rule (M1/N2), binding",
     "the bullet \"Generation-naming rule \u2026 binding",
     1),

    ("P-61 why-here: attribute the finding to the pass, not to an unpublished file",
     "**Why here.** Ledger bookkeeping; no criterion reads it. J1 records that the count \"four\" is\n"
     "falsified by the object count the schema set introduces, which is exactly why the ledger of record is",
     "**Why here.** Ledger bookkeeping; no criterion reads it. The count \"four\" is falsified by the\n"
     "object count the schema set introduces, which is exactly why the ledger of record is",
     1),

    ("P-87 source: elide the delta-issued working-resolution number inside the quotation",
     "**Source.** Declaration \u00a713(i), \"The obligation, stated first. Delta-issued working resolution\n"
     "R17(ii) requires both maps to be published side by side with the delta explicit\"",
     "**Source.** Declaration \u00a713(i), \"The obligation, stated first. \u2026 both maps to be published side\n"
     "by side with the delta explicit\"",
     1),

    ("section 3: name the scrub by its registration, not by its task label",
     "marked; the K4 scrub, for each, cites the registered limb in the declaration and adds the pointer",
     "marked; the v30a scrub, for each, cites the registered limb in the declaration and adds the pointer",
     1),
]

# ------------------------------------------------------------------ regex rules
# (name, pattern, replacement, flags, expected_count or None for "report only")
REGEX = [
    ("drop (scratch line[s] N[-M]) parentheticals",
     r"[ \n]*\(scratch lines?\s+\d+(?:\s*[\u2013\u2014-]\s*\d+)?\)", "", re.S, None),

    # ORDER MATTERS. The bare-parenthetical rule must run FIRST: otherwise the
    # "(J1 row N, " prefix rule bites the head off "(J1 rows 82, 85, 123)" and
    # leaves "85, 123)" orphaned in the text.
    ("drop bare (J1 row N) / (J1 rows N, M, K) parentheticals",
     r"[ \n]*\(J1 rows?\s+\d+(?:\s*,\s*\d+)*\s*\)", "", re.S, None),

    ("drop 'J1 row N -> ' prefix inside a pointer parenthesis",
     r"\(J1 rows?\s+[\d,\s]+\u2192\s*", "(", re.S, None),

    ("drop 'J1 row N, ' prefix inside a pointer parenthesis (followed by prose)",
     r"\(J1 rows?\s+\d+,\s*(?=[A-Za-z])", "(", re.S, None),
]

# --------------------------------------------------------------- block rewrites
SEC2_NEW = """## 2. The nineteen entries, and why there are nineteen

The entries are P-02, P-10, P-13, P-20, P-47, P-51, P-61, P-65, P-68, P-70, P-77, P-83, P-87,
P-111, P-113, P-115, P-117, P-131 and P-133 \u2014 nineteen in total. Four of them are flagged in \u00a73 as
candidates for removal, because a registered clause limb now carries their substance; flagging is
not removal, and all nineteen stand until the author decides otherwise.

The identifiers are not consecutive, and no meaning attaches to the gaps. They preserve the ordering
of the scrub pass that produced them; the missing numbers are the rows that pass sent elsewhere \u2014 to
`PREREG.md` as registered schema, or back to the declaration as instance data. No row was added,
dropped, or moved between destinations by this file.

"""

SEC4_NEW = """## 4. What this file does not contain

- **No instance data.** Rows carrying this fixture's own measurements, enumerations and identities
  stay in the declaration, where the v30a scrub labels them as the data the registered schema
  requires.
- **No gate-critical rule.** Rows that determine a gate verdict are registered in `PREREG.md` as
  SC-1 \u2026 SC-13c, and after the scrub the declaration cites them rather than restating them. One row
  in that set could not be carried by the schema, and is flagged as such in the scrub's own record.
- **No integrity rule.** Rows protecting the integrity of a declared instance are registered as
  SC-9 and SC-8(f).
- **Nothing from the declaration's two frozen regions** \u2014 the T2 addendum block and the decision-log
  tail of working resolutions \u2014 which the scrub does not touch, and which have been verified
  byte-identical across it.
"""


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def main():
    write = "--write" in sys.argv
    with open(SRC, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()

    print("=" * 76)
    print("Z4 \u2014 PRACTICES.md SCRUB  --  %s" % ("WRITE" if write else "DRY RUN"))
    print("=" * 76)
    print("\nsource sha256 : %s  %d lines" % (sha(text), text.count("\n")))
    if sha(text) != SRC_SHA:
        print("ABORT: source is not the expected draft.")
        return 2

    failures = []

    print("\n-- literal rules --")
    for name, old, new, expect in LITERAL:
        c = text.count(old)
        status = "OK" if c == expect else "*** FAIL ***"
        print("  [%-4s] %-2d/%-2d  %s" % (status if status == "OK" else "FAIL", c, expect, name))
        if c != expect:
            failures.append(name)
        else:
            text = text.replace(old, new, expect)

    print("\n-- regex rules --")
    for name, pat, repl, flags, expect in REGEX:
        hits = list(re.finditer(pat, text, flags))
        print("  [%2d ] %s" % (len(hits), name))
        for m in hits[:40]:
            frag = m.group(0).replace("\n", "\\n")
            print("         removed: %r" % frag[:90])
        if expect is not None and len(hits) != expect:
            failures.append(name)
        text = re.sub(pat, repl, text, flags=flags)

    print("\n-- block rewrites --")
    m2 = re.search(r"## 2\. Verification against J1 by row id.*?(?=## 3\. )", text, re.S)
    print("  [%s] section 2 re-keyed" % ("OK" if m2 else "FAIL"))
    if not m2:
        failures.append("section 2")
    else:
        text = text[:m2.start()] + SEC2_NEW + text[m2.end():]

    m4 = re.search(r"## 4\. What this file does not contain.*\Z", text, re.S)
    print("  [%s] section 4 rewritten" % ("OK" if m4 else "FAIL"))
    if not m4:
        failures.append("section 4")
    else:
        text = text[:m4.start()] + SEC4_NEW

    # ------------------------------------------------------------ residual scan
    print("\n-- residual unresolvable-reference scan --")
    residual = {
        "J1": r"\bJ1\b",
        "K1": r"\bK1\b",
        "K3": r"\bK3\b",
        "K4": r"\bK4\b",
        "K4_SCRUB_DIFF": r"K4_SCRUB_DIFF",
        "scratch path": r"applied\\\\|scratchpad",
        "scratch hash 1290186e": r"1290186e",
        "M1/N2": r"\bM1/N2\b",
        "R14+ working resolutions": r"\bR(1[4-9]|[2-9]\d)\b",
        "scratch line refs": r"scratch lines?",
    }
    clean = True
    for label, pat in residual.items():
        hits = [(text[:m.start()].count("\n") + 1, m.group(0))
                for m in re.finditer(pat, text)]
        if hits:
            clean = False
            print("  REMAINS  %-26s %d: lines %s" % (label, len(hits), [h[0] for h in hits][:10]))
        else:
            print("  clear    %s" % label)

    print("\nresult sha256 : %s  %d lines" % (sha(text), text.count("\n")))
    print("VERDICT: %s" % ("ALL RULES PASSED" if not failures else "FAILURES: %s" % failures))
    print("RESIDUAL: %s" % ("CLEAN" if clean else "see above"))

    if write:
        if failures:
            print("\nREFUSING TO WRITE.")
            return 3
        with open(OUT, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        print("\nWROTE %s" % OUT)
        print("  sha256: %s" % sha(text))
    else:
        print("\nDRY RUN \u2014 nothing written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
