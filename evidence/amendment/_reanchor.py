#!/usr/bin/env python3
"""Generic manifest re-anchor after a block of SCHEMA_SET_FINAL.md grows.

Usage: python _reanchor.py <marker-file>
where <marker-file> holds the EXACT quoted text that was inserted (with its "> "
prefixes), so the pre-edit source can be reconstructed and the re-anchor PROVEN
rather than computed. Arithmetic that looks right is not evidence.

For every manifest row: the text at its NEW range in the NEW file must be
byte-identical to the text at its OLD range in the OLD file. Nothing is written
unless all rows pass.
"""
import re
import sys
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

inserted = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
ssf = D / "SCHEMA_SET_FINAL.md"
new_src = ssf.read_text(encoding="utf-8")
assert new_src.count(inserted) == 1, "inserted text appears %d times" % new_src.count(inserted)

old_src = new_src.replace(inserted, "", 1)
OLD, NEW = old_src.split("\n"), new_src.split("\n")
GROWTH = len(NEW) - len(OLD)
BOUNDARY = new_src[:new_src.index(inserted)].count("\n")   # last OLD line before the insert
print("growth: %+d lines; rows starting after OLD line %d shift" % (GROWTH, BOUNDARY))


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
    if a <= BOUNDARY < b:
        nb = b + GROWTH
    if (na, nb) != (a, b):
        shifted += 1
        line = (m.group(1) + str(na) + (m.group(3) + str(nb) if m.group(4) else "")
                + m.group(5) + line[m.end():])
    ot, nt = block_text(OLD, a, b), block_text(NEW, na, nb)
    if a <= BOUNDARY < b:
        _dp = chr(10).join(re.sub(r"^>\s?", "", x) for x in inserted.split(chr(10)))
        ot = (ot + chr(10) + _dp).strip()   # blank lines PRESERVED - stripping them cost 2 chars
    if ot == nt:
        proved += 1
    else:
        failed.append((a, b, na, nb, len(ot), len(nt)))
    out_lines.append(line)

print("rows shifted: %d   rows PROVEN identical after re-anchor: %d   FAILED: %d"
      % (shifted, proved, len(failed)))
for f in failed:
    print("   *** OLD L%d-%d -> NEW L%d-%d  (%d chars vs %d)" % f)
assert not failed, "re-anchor not proven; nothing written"
man_p.write_text("\n".join(out_lines), encoding="utf-8")
print("BLOCK_MANIFEST.md re-anchored and PROVEN.")
