#!/usr/bin/env python3
"""DELTA R38 / E1 — refine H-L13 so it cannot be applied mechanically against a
closure constraint. Match-count asserted."""

import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
H = REPO / "HISTORY.md"

OLD = ("**Three instances is a structural defect, not bad luck: enumerated ranges in "
       "cross-references are fragile by construction, because the obligation to re-bump lives "
       "outside the edit that grows the target.** The `DESIGN.md` reference now names the series "
       "(`the H-L review-lesson series`, open range) rather than its current tail, so appending a "
       "lesson cannot desynchronize a registered document. The same shape — an index that must be "
       "re-bumped in a separate edit — is looked for in any future cross-reference whose target "
       "grows.")

NEW = ("**Three instances is a structural defect, not bad luck: enumerated ranges in "
       "cross-references are fragile by construction, because the obligation to re-bump lives "
       "outside the edit that grows the target.** The `DESIGN.md` reference now names the series "
       "(`the H-L review-lesson series`, open range) rather than its current tail, so appending a "
       "lesson cannot desynchronize a registered document. The same shape — an index that must be "
       "re-bumped in a separate edit — is looked for in any future cross-reference whose target "
       "grows. **What this lesson is NOT about, added 21 Aug 2026 after a sweep for the shape "
       "nearly deleted a constraint.** The fragile object is a numeral that *points at* an "
       "enumeration which may grow: it goes stale silently, because nothing in the edit that adds "
       "the eleventh item forces the sentence that said ten to be found. A numeral that *forbids* "
       "growth is the opposite object and is not covered here — \"exactly three classes, mutually "
       "exclusive and exhaustive; there is no fourth class and no residue class\", or \"the "
       "exception rests on two grounds and on no other\". There the count is not a reference to "
       "the set, it **is** the rule: it is what closes the set, and a reader who strikes the "
       "numeral in the name of this lesson has not de-fragilised a cross-reference, they have "
       "deleted the constraint and admitted a fourth class. **The test is what happens when the "
       "target grows.** If growth silently falsifies the numeral, the numeral is a stale reference "
       "and this lesson applies. If growth is what the numeral forbids, the numeral is a closure "
       "constraint and removing it is a weakening, which §0.2.1 line 97 does not permit an "
       "amendment to make.")


def main():
    s = H.read_text(encoding="utf-8")
    c = s.count(OLD)
    assert c == 1, f"H-L13 tail match count = {c}, expected 1"
    H.write_text(s.replace(OLD, NEW, 1), encoding="utf-8", newline="")
    t = H.read_text(encoding="utf-8")
    print("H-L13 refined (match count 1)")
    print(f"  HISTORY.md now {t.count(chr(10))} lines")
    for probe in ("closure constraint", "no fourth class", "The test is what happens when the target grows"):
        print(f"  contains {probe!r}: {probe in t}")


if __name__ == "__main__":
    main()
