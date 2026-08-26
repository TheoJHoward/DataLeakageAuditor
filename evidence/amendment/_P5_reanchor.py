#!/usr/bin/env python3
"""DELTA R47 / P5 follow-through - re-anchor the manifest after SC-3(a) grew.

The SC-3(a) edit added 6 lines at 312. Every block below shifted. The manifest is
the AUTHORITY (M1), so it is re-anchored - and the re-anchoring is PROVEN, not
assumed: for every entry, the text at its NEW range in the NEW file must be
byte-identical to the text at its OLD range in the OLD file. Arithmetic that
looks right is not evidence.
"""
import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

NEWTXT = ("published as an artifact with a **declared schema**: one row per cell of the declared scored\n"
          "population, with every field named, including the field that records whether the cell is\n"
          "scored. **The artifact may in addition carry rows of a class the declaration declares\n"
          "DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no\n"
          "criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the\n"
          "map's cells, not over the artifact's row count**. A count taken from the artifact without\n"
          "excluding them counts a different population, and **every figure published from the artifact\n"
          "names which population it counts**.")
OLDTXT = ("published as an artifact with a **declared schema**: one row per scored cell, with every field\n"
          "named, including the field that records whether the cell is scored.")

ssf = D / "SCHEMA_SET_FINAL.md"
new_src = ssf.read_text(encoding="utf-8")
new_q = "\n".join("> " + l for l in NEWTXT.split("\n"))
old_q = "\n".join("> " + l for l in OLDTXT.split("\n"))
assert new_src.count(new_q) == 1
old_src = new_src.replace(new_q, old_q, 1)          # reconstruct the pre-edit file
OLD, NEW = old_src.split("\n"), new_src.split("\n")
GROWTH = len(NEW) - len(OLD)
BOUNDARY = 312 + len(old_q.split("\n")) - 1          # last line of the OLD passage
print("growth: %+d lines; entries starting after OLD line %d shift" % (GROWTH, BOUNDARY))
assert GROWTH == 6, GROWTH


def block_text(lines, a, b):
    out = []
    for raw in lines[a - 1:b]:
        if raw.startswith("```"):
            continue
        out.append(re.sub(r"^>\s?", "", raw) if raw.startswith(">") else raw)
    return "\n".join(out).strip()


man_p = D / "BLOCK_MANIFEST.md"
man = man_p.read_text(encoding="utf-8")
ROW = re.compile(r"^(\|\s*\S+?\s*\|\s*)(\d+)(\s*[\u2013-]\s*)?(\d+)?(\s*\|)")

out_lines, shifted, proved, failed = [], 0, 0, []
for line in man.split("\n"):
    m = ROW.match(line)
    if not m or not re.match(r"^\|\s*[0-9]", line):
        out_lines.append(line)
        continue
    a = int(m.group(2))
    b = int(m.group(4)) if m.group(4) else a
    na = a + GROWTH if a > BOUNDARY else a
    nb = b + GROWTH if b > BOUNDARY else b
    # entry 6 itself CONTAINS the edit: its end moves, its start does not
    if a <= BOUNDARY < b:
        nb = b + GROWTH
    if (na, nb) != (a, b):
        shifted += 1
        pre, sep, post = m.group(1), m.group(3), m.group(5)
        line = (pre + str(na) + (sep + str(nb) if m.group(4) else "") + post
                + line[m.end():])
    # PROOF: same text at the new range in the new file as the old range in the old file
    ot, nt = block_text(OLD, a, b), block_text(NEW, na, nb)
    if a <= BOUNDARY < b:
        ot = ot.replace(OLDTXT, NEWTXT, 1)           # this block legitimately changed
    if ot == nt:
        proved += 1
    else:
        failed.append((a, b, na, nb, len(ot), len(nt)))
    out_lines.append(line)

print("rows shifted: %d   rows proven identical after re-anchor: %d   FAILED: %d"
      % (shifted, proved, len(failed)))
for f in failed:
    print("   *** OLD L%d-%d -> NEW L%d-%d  (%d chars vs %d)" % f)
assert not failed, "re-anchor is not proven; nothing written"
man_p.write_text("\n".join(out_lines), encoding="utf-8")
print("\nBLOCK_MANIFEST.md re-anchored and PROVEN.")
