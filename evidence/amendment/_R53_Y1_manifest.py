#!/usr/bin/env python3
"""DELTA R53/Y1 - assign the two moved blocks in the manifest, and retire their §B rows.

They are no longer "drawing text from elsewhere" - SCHEMA_SET_FINAL.md IS their source
now - so they leave §B and enter §A, where M6 check (II) binds them by `src in op`
(source contained in hunk), the direction that catches a deletion.

§B's row for each is replaced by a MOVED note rather than deleted, so the history of
where the text used to live is not silently erased.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

cur = json.loads((D / "_K1_population.json").read_text(encoding="utf-8"))
new = [b for b in cur if b["idx"] in (34, 35)]
assert len(new) == 2, "expected 2 new blocks, got %d" % len(new)
b34, b35 = new
assert "C2op" in str(b34["heading"]), b34["heading"]
assert "C2ret" in str(b35["heading"]), b35["heading"]

man_p = D / "BLOCK_MANIFEST.md"
t = man_p.read_text(encoding="utf-8")

# ---- §A: append two rows -----------------------------------------------------
LAST = "| 33 | 1605\u20131652 | \u00a7AB \u2014 the amendments-block recording text | **H2** (8, insert) |"
assert t.count(LAST) == 1, "\u00a7A tail row match %d" % t.count(LAST)
ADD = (LAST
       + "\n| 34 | %d\u2013%d | \u00a710.1-C2op \u2014 the C2 operative item (moved here R53/Y1) | **H32** (1022, replace) |"
         % (b34["lines"][0], b34["lines"][1])
       + "\n| 35 | %d\u2013%d | \u00a710.1-C2ret \u2014 the C2 retention block (moved here R53/Y1) | **H31** (1022, insert) |"
         % (b35["lines"][0], b35["lines"][1]))
t = t.replace(LAST, ADD, 1)
print("\u00a7A: rows 34 (L%d-%d -> H32) and 35 (L%d-%d -> H31) added"
      % (b34["lines"][0], b34["lines"][1], b35["lines"][0], b35["lines"][1]))

# ---- §B: retire both rows ----------------------------------------------------
n = 0
out = []
for line in t.split("\n"):
    m = re.search(r"\*\*(H3[12])\*\*", line)
    if m and line.startswith("|") and "_X5_hunks_v2.json" in line:
        hid = m.group(1)
        blk = "\u00a710.1-C2op" if hid == "H32" else "\u00a710.1-C2ret"
        line = ("| **%s** | 1022 | **MOVED R53/Y1 \u2014 no longer section B.** Its text now lives in "
                "`SCHEMA_SET_FINAL.md` under `%s` and is claimed by \u00a7A row %s; M6 check (II) binds it. "
                "It was section-B only because it was drafted inside a delta. |"
                % (hid, blk, "34" if hid == "H32" else "35"))
        n += 1
    out.append(line)
assert n == 2, "\u00a7B rows retired: %d" % n
man_p.write_text("\n".join(out), encoding="utf-8")
print("\u00a7B: 2 rows retired with a MOVED note (history kept, not erased)")
