#!/usr/bin/env python3
"""C2 — RESOLVABILITY, not matching.

C2.1: the vocabulary is unbounded. "Y3 §6.3", "the Y3 document", "the waived
ruling", "per the earlier decision" all denote the same thing and no regex spans
them. Widening the pattern is a losing game.

C2.2: ask the CLOSED question instead. Every INSERTION POINT field names its
targets as PREREG.md line numbers. So:

    for each of the 16 fields, is EVERY PREREG line it names covered by a record
    whose operative text resolves inside SCHEMA_SET_FINAL.md?

A field naming a target with no record is the finding, HOWEVER IT IS PHRASED.
SC-12 named line 1035 and line 856; records covered 1035 only. That is what this
check sees - and it sees it without reading the words "Y3", "operative", or
"text", because it never looks at how the target was described.

C2.3: this is the generator's own discovery made deliberate. SC-12 surfaced
because the generator needed text that was not there.

C2.4: a field whose targets cannot be mechanically resolved is LISTED FOR
READING, never passed. Sixteen is a readable number.

WHY THERE IS NO NOT_TARGET REGEX HERE (H-L21, and C2.1 taken literally)
----------------------------------------------------------------------
Version 1 of this file tried to classify boundary references ("before the `---`
at line 268") away from real targets with a NOT_TARGET pattern. Two things went
wrong and BOTH are the reason the pattern is gone:

  1. Widening never converged. Every field phrased its non-targets differently
     ("before the ... at line", "stands byte-exact", "NOT superseded", "is the
     floor"). That is precisely C2.1's warning, arriving on schedule.
  2. The widened pattern was CORRUPTED IN WRITING. A `\\b` passed through a
     non-raw Python triple-quoted string became a literal backspace byte (0x08),
     so `?<BS>at\\s+line` could never match. Identical in kind to the §88 sweep's
     backspace defect. There it caused a FALSE CLEAN; here a false POSITIVE.

So classification is not done by pattern. Every named line that no record covers
must carry an explicit entry in READ_RECORD below: the field's own words, quoted,
and the determination. An uncovered line with no entry FAILS. That is §30.1's
exclusion list stated with the result, and §30.2's "where an exclusion cannot be
justified, it is not an exclusion, it is a miss".
"""
import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]

# A target is a PREREG.md line number named anywhere in the field.
TARGET = re.compile(r"lines?\s+\*{0,2}(\d{2,4})\*{0,2}")

# ---------------------------------------------------------------------------
# READ_RECORD - the §30.1 exclusion list. Keyed (clause, prereg_line).
# Each entry: (the field's own words, quoted) and (why it is not a target).
# Every one of these was READ, not matched. Nothing is here that was not read.
# ---------------------------------------------------------------------------
READ_RECORD = {
    ("SC-1", 268): (
        "before the `---` at line 268",
        "BOUNDARY. Names the upper bound of the insertion, not a second target. "
        "The target is line 266, covered by record SC-1."),
    ("SC-2", 453): (
        "before the `**Pass gate - discrimination, not tier.**` heading at line 453",
        "BOUNDARY. Names what the insertion must precede. The target is line 451, "
        "covered by record SC-2."),
    ("SC-4", 459): (
        "Criterion 1's own text at line 459 **stands byte-exact**",
        "EXPLICIT NON-SUPERSESSION. The field states line 459 is NOT modified. A "
        "record covering it would contradict the field."),
    ("SC-13a", 1031): (
        "Lines 1031, 1033 and 1035 stand byte-exact and are **NOT superseded**",
        "EXPLICIT NON-SUPERSESSION, stated by the field itself."),
    ("SC-13a", 1033): (
        "Lines 1031, 1033 and 1035 stand byte-exact and are **NOT superseded**",
        "EXPLICIT NON-SUPERSESSION, stated by the field itself."),
    ("SC-5", 466): (
        "before line 466's parenthetical",
        "BOUNDARY. The target is the block SC-4 inserts after line 464, covered "
        "by records SC-4 and SC-5."),
    ("SC-7", 470): (
        "before line 470's \"What this gate does and does not guarantee\"",
        "BOUNDARY. The target is line 468, covered by record SC-7."),
    ("SC-9", 101): (
        "before line 101's \"Membership in A or B must be citable\"",
        "BOUNDARY. The target is line 99, covered by record SC-9."),
    ("SC-13c", 818): (
        "inserted after `PREREG.md` line 816 (§7.2.1), between line 816 and line 818",
        "BOUNDARY. Names the lower bound. The target is line 816, covered by "
        "record SC-13c-2."),
    ("SC-13c", 1036): (
        "still between line 1035's paragraph and line 1036. The enumeration is untouched",
        "BOUNDARY. Same lower bound as SC-13b's limb 1. The target is line 1035, "
        "covered by record SC-13c-1."),
    ("SC-8", 97): (
        "Two supersession markers accompany it: one beneath §11's list (item 3's "
        "file set), one after `PREREG.md` line 97 (§0.2.1's \"both\")",
        "SUPERSESSION MARKER, not applied text. All 17 SUPERSESSION MARKER blocks "
        "in PART 1 are covered by no record and contribute 0 of 96 lines to the "
        "diff - the treatment is uniform, not an omission here. The substantive "
        "supersession IS carried in APPLIED text: §11 item 8 states in the diff "
        "that \"§0.2.1 line 97's 'both' ... is superseded as the set by this item\"."),
    ("SC-13b", 1036): (
        "between line 1035's paragraph and line 1036 (criterion 3)",
        "BOUNDARY. Names the lower bound of a pure insertion. The target is line "
        "1035, covered by record SC-13b."),
}


def load(ssf_path, rec_path, drop=()):
    lines = ssf_path.read_text(encoding="utf-8").split("\n")
    records = json.loads(rec_path.read_text(encoding="utf-8"))["records"]
    records = [r for r in records if r["id"] not in drop]
    covered = {}
    for r in records:
        covered.setdefault(r["prereg_line"], []).append(r["id"])
    return lines, covered


def field_body(L, start, part1_end):
    """Read an INSERTION POINT field. A field ending in a colon continues into a
    numbered sub-list ("**Two:**") - stopping at the first blank line would
    truncate exactly the fields with MULTIPLE targets, the ones that matter."""
    end = next((i for i in range(start, part1_end)
                if not L[i - 1].strip() and i > start), start + 1)
    # ".rstrip('*')" because the colon sits INSIDE the emphasis markers in
    # "**Two:**" - the exact form used by the two fields with the most targets.
    if L[end - 2].rstrip().rstrip("*").rstrip().endswith(":"):
        while end < part1_end and (not L[end - 1].strip()
                                   or re.match(r"^\s*(?:\d+\.|[-*])\s", L[end - 1])
                                   or L[end - 1].startswith("   ")):
            end += 1
    return " ".join(L[start - 1:end])


def run(ssf_path, rec_path, drop=(), quiet=False):
    L, covered = load(ssf_path, rec_path, drop)
    part1_end = next(i for i, l in enumerate(L, 1) if l.startswith("# PART 2 "))
    fields = [i for i, l in enumerate(L, 1)
              if l.startswith("**INSERTION POINT.**") and i < part1_end]

    if not quiet:
        print("C2 - TARGET RESOLVABILITY")
        print("  source   : %s" % ssf_path.name)
        print("  records  : %s%s" % (rec_path.name,
                                     "  (DROPPED: %s)" % ", ".join(drop) if drop else ""))
        print("  population (§30.1): all %d INSERTION POINT fields in PART 1."
              % len(fields))
        print("  exclusions (§30.1): only the %d recorded reads listed below. "
              "No others.\n" % len(READ_RECORD))

    unresolved, read_used, ok = [], [], 0
    for start in fields:
        body = field_body(L, start, part1_end)
        clause = None
        for i in range(start, 0, -1):
            m = re.match(r"^### (SC-[0-9a-z]+) - |^### (SC-[0-9a-z]+) — ", L[i - 1])
            if m:
                clause = m.group(1) or m.group(2)
                break
        named = sorted({int(m.group(1)) for m in TARGET.finditer(body)})
        if not named:
            unresolved.append((clause, start, "NO LINE TARGET EXTRACTED", body))
            if not quiet:
                print("  %-8s ssf l.%-5d ** NO LINE TARGET EXTRACTED - READ (C2.4) **"
                      % (clause, start))
            continue
        miss, excused = [], []
        for n in named:
            if n in covered:
                continue
            if (clause, n) in READ_RECORD:
                excused.append(n)
                read_used.append((clause, n))
            else:
                miss.append(n)
        if miss:
            unresolved.append((clause, start, miss, body))
            if not quiet:
                print("  %-8s ssf l.%-5d ** UNRESOLVED TARGET(S): %s **"
                      % (clause, start, miss))
                print("       names %s; records cover %s"
                      % (named, [n for n in named if n in covered]))
        else:
            ok += 1
            if not quiet:
                note = "  [+%d recorded read%s]" % (len(excused),
                                                    "" if len(excused) == 1 else "s") if excused else ""
                print("  %-8s ssf l.%-5d ok   targets %s -> %s%s"
                      % (clause, start, [n for n in named if n in covered],
                         sorted({r for n in named if n in covered for r in covered[n]}),
                         note))
    return fields, unresolved, read_used, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssf", default=str(REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"))
    ap.add_argument("--records", default=str(REPO / "evidence/amendment/SCHEMA_RECORDS.json"))
    ap.add_argument("--drop", default="", help="record ids to drop (known-positive test)")
    ap.add_argument("--self-test", action="store_true",
                    help="B5.3/C3: fire on a known positive before reporting clean")
    a = ap.parse_args()
    ssf, rec = pathlib.Path(a.ssf), pathlib.Path(a.records)
    drop = tuple(x for x in a.drop.split(",") if x)

    if a.self_test:
        # B5.3 / C3.1 - the known positive is the R79 state: SC-12's field named
        # PREREG line 856 and NO record covered it. Reproduced by dropping SC-12p.
        print("B5.3 / C3.1 - KNOWN-POSITIVE TEST (run BEFORE any clean result)")
        print("  positive : the R79 defect - SC-12 names PREREG line 856, no record covers it")
        print("  method   : current source, record SC-12p dropped\n")
        _, unres, _, _ = run(ssf, rec, drop=("SC-12p",), quiet=True)
        hits = [(c, m) for c, s, m, b in unres if c == "SC-12"]
        if not hits:
            print("  ** DID NOT FIRE ON THE KNOWN POSITIVE - THIS IS NOT AN INSTRUMENT **")
            return 2
        print("  FIRED: SC-12 -> UNRESOLVED TARGET(S) %s" % hits[0][1])
        print("  The check sees the R79 defect. Clean results below are reportable.\n")
        print("=" * 78 + "\n")

    fields, unresolved, read_used, ok = run(ssf, rec, drop=drop)

    print("\n  fields with every target covered : %d of %d" % (ok, len(fields)))
    print("  fields with an UNRESOLVED target : %d" % len(unresolved))
    print("  recorded reads relied on         : %d of %d"
          % (len(read_used), len(READ_RECORD)))

    unused = set(READ_RECORD) - set(read_used)
    if unused:
        # D7's lesson: an exemption that fires on nothing is a silent revert.
        print("  ** RECORDED READ FIRED ON NOTHING: %s **" % sorted(unused))

    print("\n  §30.1 EXCLUSION LIST - every uncovered line, its own words, and why:")
    for (clause, n), (quoted, why) in sorted(READ_RECORD.items()):
        mark = "used" if (clause, n) in read_used else "**UNUSED**"
        print("    %-8s line %-5d [%s]\n        field says : \"%s\"\n        read       : %s"
              % (clause, n, mark, quoted, why))

    for clause, start, miss, body in unresolved:
        print("\n  UNRESOLVED - %s, ssf l.%d, %s:\n    %s" % (clause, start, miss, body[:400]))

    return 1 if (unresolved or unused) else 0


if __name__ == "__main__":
    sys.exit(main())
