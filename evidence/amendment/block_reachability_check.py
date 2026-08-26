#!/usr/bin/env python3
"""BLOCK REACHABILITY — does every operative block in PART 1 reach the diff?

WHY THIS EXISTS, AND WHAT IT FOUND
----------------------------------
C2 asks a question keyed on INSERTION POINT fields: does every PREREG line a
field NAMES have a record? That question cannot see operative text that never
had an INSERTION POINT field in the first place.

§10.1-C2op is exactly that. It is a `###` section in PART 1 headed "THE C2
OPERATIVE ITEM (replaces `PREREG.md` line 1022)". It names its target in its own
heading, not in an INSERTION POINT field. No record carries prereg_line 1022, so
the generated diff has no hunk covering line 1022 — and C2 returned 16 of 16
clean while that was true.

The existing ledger could not see it either:
  §53.2 asks "does every line IN THE DIFF trace back to a declared range?"  It
        does — the missing text is not in the diff to be traced.
  §53.3 asks "is every CLAUSE represented?"  All 15 are. §10.1-C2op is not a
        clause; it is a replacement item.
  §82   compares two paths to the SAME RECORD's text. A block with no record has
        no path to compare.
Every one of those checks reasons FORWARD FROM THE RECORD SET. This one reasons
forward from THE SOURCE, which is the only direction that can see a block the
record set never claimed. That is H-L21 restated: an instrument's PASS is a
statement about its domain, and the record set was the whole domain until now.

THE QUESTION
------------
For every block of quoted operative text in PART 1: are its lines present in the
generated diff — all of them, none of them, or SOME of them?
  ALL  -> applied.
  NONE -> must be justified by kind (marker/metadata) or by the block's own words
          ("drafted, not applied"). Anything else is a MISS (§30.2).
  SOME -> a partially applied block. Always a defect: nothing legitimately lands
          half in.
"""
import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]

HDR = re.compile(
    r"^\*\*(INSERTION TEXT|INSERTION POINT|THE CLAUSE|SUPERSESSION MARKER|DATA THE"
    r"|ROWS COVERED|OPERATIVE v30a TEXT|INSERT AFTER|WHY|Why|Corroboration"
    r"|SC-12\(w\))|^### |^#### |^## |^# ")

# §30.1 exclusion list: block kinds that legitimately contribute NOTHING to the
# diff, each with the reason. Anything not here and not applied is a MISS.
JUSTIFIED_UNAPPLIED = {
    "SUPERSESSION MARKER":
        "metadata. Recorded in each record's `supersession` field, never inserted "
        "into PREREG.md. Uniform: every such block contributes 0 lines.",
    "SC-12(w)":
        "descriptive wrapper. The applied limb text is the separate "
        "`OPERATIVE v30a TEXT at line 929` block, which IS applied.",
}
# Blocks whose own text declares them unapplied. Verified by reading, not matched.
SELF_DECLARED_UNAPPLIED = {
    "§AB": "heading reads \"(revised; drafted, not applied)\".",
    "§AC": "\"Appended to the §AB amendments-block recording text and claimed by "
           "the same hunk\" — §AB is not applied, so neither is §AC.",
}


def norm(s):
    s = s.strip()
    if s.startswith(">"):
        s = s[1:].strip()
    return s


def blocks_of(ssf_lines, part1_end):
    out, cur = [], None
    for i, l in enumerate(ssf_lines, 1):
        if i >= part1_end:
            break
        if HDR.match(l):
            if cur:
                out.append(cur)
            cur = [l, i, i]
        elif cur:
            cur[2] = i
    if cur:
        out.append(cur)
    return out


def kind_of(hdr):
    m = re.match(r"^\*\*([^,.]+)", hdr)
    if m:
        return re.sub(r"\s*—.*", "", m.group(1)).strip()
    m = re.match(r"^#+\s+(\S+)", hdr)
    return m.group(1) if m else hdr[:30]


def base_prereg():
    """The registered base, read from the TAG — never from the worktree."""
    import subprocess
    out = subprocess.run(["git", "show", "prereg-v30:PREREG.md"], cwd=str(REPO),
                         capture_output=True, check=True).stdout.decode("utf-8")
    return {norm(l) for l in out.split("\n")}


def run(ssf_path, diff_path, drop_ids=(), rec_path=None, quiet=False):
    base = base_prereg()
    ssf = ssf_path.read_text(encoding="utf-8").split("\n")
    diff_text = diff_path.read_text(encoding="utf-8")
    added = {norm(l[1:]) for l in diff_text.split("\n")
             if l.startswith("+") and not l.startswith("+++")}
    if drop_ids:
        # known-positive mode: pretend a record's inserted lines never landed
        recs = json.loads(rec_path.read_text(encoding="utf-8"))["records"]
        for r in recs:
            if r["id"] in drop_ids:
                for j in range(r["clause_first_line"], r["clause_last_line"] + 1):
                    added.discard(norm(ssf[j - 1]))
    part1_end = next(i for i, l in enumerate(ssf, 1) if l.startswith("# PART 2 "))

    findings, tally = [], {}
    for hdr, s, e in blocks_of(ssf, part1_end):
        # Operative text appears in TWO carriers: blockquotes and fenced code.
        # §10.1-C2op — the item that replaces PREREG line 1022 — uses a fence.
        # A quote-only reader cannot see it, and would pass its omission.
        body, fenced = [], False
        for j in range(s, e + 1):
            raw = ssf[j - 1]
            if raw.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced or raw.lstrip().startswith(">"):
                body.append(norm(raw))
        # A body line that is VERBATIM EXISTING PREREG.md text is context, not
        # applied text: anchors quoted for matching (§13c-P), and instance records
        # quoting registered sites. Excluding them by what they ARE, mechanically,
        # rather than by naming the blocks - which would be the widening C2.1 warns
        # against. §10.1-C2op survives this filter because its text is NEW.
        body = [b for b in body if len(b) > 25 and b not in base]
        if not body:
            continue
        hit = sum(1 for b in body if b in added)
        k = kind_of(hdr)
        t = tally.setdefault(k, [0, 0, 0, 0])          # blocks, lines, applied, unapplied
        t[0] += 1; t[1] += len(body); t[2] += hit
        if hit == len(body):
            continue
        t[3] += 1
        if 0 < hit < len(body):
            findings.append(("PARTIAL", k, hdr, s, hit, len(body)))
        elif k in JUSTIFIED_UNAPPLIED or any(k.startswith(x) for x in SELF_DECLARED_UNAPPLIED):
            continue
        else:
            findings.append(("UNAPPLIED", k, hdr, s, hit, len(body)))

    if not quiet:
        print("BLOCK REACHABILITY — PART 1 operative blocks vs the generated diff")
        print("  source : %s" % ssf_path.name)
        print("  diff   : %s%s\n" % (diff_path.name,
                                     "   (DROPPED: %s)" % ",".join(drop_ids) if drop_ids else ""))
        print("  %-34s %6s %7s %8s %s" % ("block kind", "blocks", "lines", "applied", "unapplied"))
        for k, (nb, nl, na, nu) in sorted(tally.items()):
            print("  %-34s %6d %7d %8d %s" % (k, nb, nl, na, nu))
        print("\n  §30.1 EXCLUSIONS — kinds that legitimately contribute nothing:")
        for k, why in sorted(JUSTIFIED_UNAPPLIED.items()):
            print("    %-22s %s" % (k, why))
        for k, why in sorted(SELF_DECLARED_UNAPPLIED.items()):
            print("    %-22s %s" % (k, why))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssf", default=str(REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"))
    ap.add_argument("--diff", default=str(REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"))
    ap.add_argument("--records", default=str(REPO / "evidence/amendment/SCHEMA_RECORDS.json"))
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    ssf, diff, rec = pathlib.Path(a.ssf), pathlib.Path(a.diff), pathlib.Path(a.records)

    if a.self_test:
        # B5.3 / C3: fire on a KNOWN POSITIVE before any clean result is reported.
        print("B5.3 / C3 — KNOWN-POSITIVE TEST")
        print("  positive : SC-12's §7.7 pointer block present in the source but")
        print("             absent from the diff — the R79 defect, in block terms.\n")
        f = run(ssf, diff, drop_ids=("SC-12p",), rec_path=rec, quiet=True)
        if not any(x[0] == "UNAPPLIED" for x in f):
            print("  ** DID NOT FIRE ON THE KNOWN POSITIVE — NOT AN INSTRUMENT **")
            return 2
        print("  FIRED: %s\n" % "; ".join("%s %s ssf l.%d" % (x[0], x[1], x[3])
                                          for x in f if x[0] == "UNAPPLIED"))
        print("=" * 78 + "\n")

    findings = run(ssf, diff)
    print("\n  FINDINGS: %d" % len(findings))
    for state, k, hdr, s, hit, tot in findings:
        print("\n  ** %s ** ssf l.%d — %d of %d lines in the diff\n     %s"
              % (state, s, hit, tot, hdr.strip()[:110]))
    if not findings:
        print("  No unjustified unapplied block. No partially applied block.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
