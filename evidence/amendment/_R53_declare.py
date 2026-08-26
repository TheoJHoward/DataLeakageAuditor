#!/usr/bin/env python3
"""DELTA R53/Y1 - declare the two added blocks so N2 can absorb them."""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
cur = json.loads((D / "_K1_population.json").read_text(encoding="utf-8"))
b34 = [b for b in cur if b["idx"] == 34][0]
b35 = [b for b in cur if b["idx"] == 35][0]

ADD = """

---

## R53/Y1 \u2014 the last two hunks get a source of record

| block | lines | sha12 | change |
|---|---|---|---|
| 34 \u2014 \u00a710.1-C2op | %d\u2013%d | `%s` | **ADDED** \u2014 the C2 operative item |
| 35 \u2014 \u00a710.1-C2ret | %d\u2013%d | `%s` | **ADDED** \u2014 the C2 retention block |

**What moved, and why it was wrong where it was.** Both texts lived in `_X5_hunks_v2.json` and
nowhere else. That was never a decision \u2014 they were drafted inside deltas (the operative item at
R39/F2, the retention block at K2 \u00a79.2) and redrafted at R47/P1 to the narrowest C2. The
consequence, surfaced at R52: **the amendment's newest and most-revised normative text was the only
applied text no provenance check could reach.** Every other hunk had a source document to be checked
against; these two were checkable by review alone.

**Where they went.** `SCHEMA_SET_FINAL.md` PART 1, under their own headings, as **fenced** blocks.
One source of record for all applied text. **No second document was created for delta-drafted
hunks** \u2014 that would be the duplicated-authority shape, and the fix for a provenance gap must not
introduce a worse defect than the one it closes.

**What this changes about how they are checked.** They leave manifest \u00a7B and enter \u00a7A. \u00a7A is bound
by **M6 check (II)**, which asserts `src in op` \u2014 the SOURCE block contained in the HUNK. **That is
the converse direction, so it catches a deletion**, which is the whole reason for the move. \u00a7B's
rows are retired with a MOVED note rather than deleted, so where the text used to live is still on
the record.

**Structural obstacles: none, and each was checked before writing rather than after (R53/Y2).**
The enumerator already treats fences as population blocks \u2014 3 of the 33 frozen blocks were fences.
The blocks were appended at PART 1's tail, after the last existing block, so **no existing block's
line range moved**: N2 reports `added 2, removed 0, modified 0, re-anchored 0, identical 33`, and no
re-anchor was required. The assembler is unaffected: it builds from the hunk JSON, and the JSON is
now bound to the source rather than being the source.

**Verification owed (N5).** Neither text changed a character in this move \u2014 both were copied from
the hunks verbatim and M6 (II) proves containment. What changed is what can check them. The texts
themselves still carry the R49/R6 verification's open findings.
""" % (b34["lines"][0], b34["lines"][1], b34["sha12"],
       b35["lines"][0], b35["lines"][1], b35["sha12"])

p = D / "_POPULATION_CHANGES.md"
t = p.read_text(encoding="utf-8")
assert "R53/Y1" not in t
p.write_text(t.rstrip() + ADD, encoding="utf-8")
print("declared: blocks 34 (%s) and 35 (%s)" % (b34["sha12"], b35["sha12"]))
