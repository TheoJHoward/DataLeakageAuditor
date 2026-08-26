#!/usr/bin/env python3
"""Re-anchor BLOCK_MANIFEST.md from the population.  DELTA R55/A1.

TWO KINDS OF CHANGE, AND ONLY ONE OF THEM IS ARITHMETIC.

  DISPLACED       - the block's position moved, its CONTENT is unchanged (sha12 equal).
                    Every row inside it keeps its offset from the block start, so
                    shifting by the start delta is VALID.

  GREW INTERNALLY - the block's own content changed (sha12 differs). **Every sub-entry
                    boundary inside it is now invalid**, because the text they delimit
                    moved relative to the block start by an unknown amount. Shifting
                    them is arithmetic on an assumption that no longer holds. This tool
                    REFUSES to shift them and reports instead; they must be RE-DERIVED
                    from source markers.

WHY THIS SHAPE OF FIX. Three separate failures in this tool came from one assumption -
that all change is displacement:
  1. a marker extracted without its trailing newline made GROWTH +34 where blocks moved
     +35, leaving 29 rows one line short (M6 saw it as 25 PARTIAL blocks);
  2. MODIFIED pairing matched only on start line, so an earlier block's growth made a
     later modified block read as removed+added;
  3. sub-entries 7a/7b were shifted through a block that grew from 3 lines to 25, and
     entry 7b then pointed at the wrong text (M6 (II) saw it; the arithmetic did not).
Patching each instance leaves the assumption in place. The fix belongs at the coupling.

A block with exactly ONE row spanning it whole has no sub-entry boundaries to invalidate,
so its end is extended to the block's new end - that IS re-derivation, not a shift.
"""
import json
import pathlib
import re
import subprocess
import sys

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

frozen = json.loads((D / "_K1_population_FROZEN.json").read_text(encoding="utf-8"))
subprocess.run([sys.executable, str(D / "_K1_enumerate2.py")], capture_output=True)
current = json.loads((D / "_K1_population.json").read_text(encoding="utf-8"))

# MATCH BY CONTENT, NOT BY POSITION. Index alignment breaks the moment a block is INSERTED
# mid-file: every block after it shifts index, and frozen[i] stops meaning current[i].
# That is the same coupling defect R55/A1 fixed for displacement-vs-growth, in a third
# form - the tool assuming a structure the document does not guarantee. Content identity
# is what actually survives an insertion.
_cur_by_sha = {}
for _c in current:
    _cur_by_sha.setdefault(_c["sha12"], []).append(_c)

NEW = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8").split("\n")

MATCH = {}          # frozen idx -> current block, matched by content
UNMATCHED = []      # frozen blocks whose content is gone: changed, or removed
for f in frozen:
    c = _cur_by_sha.get(f["sha12"])
    if c:
        MATCH[f["idx"]] = c.pop(0)
    else:
        UNMATCHED.append(f)
ADDED = [c for cs in _cur_by_sha.values() for c in cs]
print("blocks frozen %d -> current %d   matched by content: %d   unmatched frozen: %d   added: %d"
      % (len(frozen), len(current), len(MATCH), len(UNMATCHED), len(ADDED)))
if ADDED:
    print("  ADDED (assign in the manifest, then refreeze): %s"
          % [(c["lines"], str(c.get("heading"))[:40]) for c in ADDED])


def block_text(a, b):
    out = []
    for raw in NEW[a - 1:b]:
        if raw.startswith("```"):
            continue
        out.append(re.sub(r"^>\s?", "", raw) if raw.startswith(">") else raw)
    return "\n".join(out).strip()


man_p = D / "BLOCK_MANIFEST.md"
man = man_p.read_text(encoding="utf-8")
ROW = re.compile(r"^(\|\s*(\S+?)\s*\|\s*)(\d+)(\s*[\u2013-]\s*)?(\d+)?(\s*\|)")

# how many manifest rows sit inside each frozen block?
rows_per_block = {}
for line in man.split("\n"):
    m = ROW.match(line)
    if not m or not re.match(r"^\|\s*[0-9]", line):
        continue
    a = int(m.group(3))
    owner = next((f["idx"] for f in frozen if f["lines"][0] <= a <= f["lines"][1]), None)
    if owner:
        rows_per_block.setdefault(owner, []).append(m.group(2))

out, shifted, extended, refused, orphan = [], 0, 0, [], []
for line in man.split("\n"):
    m = ROW.match(line)
    if not m or not re.match(r"^\|\s*[0-9]", line):
        out.append(line)
        continue
    rid = m.group(2)
    a = int(m.group(3))
    b = int(m.group(5)) if m.group(5) else a
    owner = next((i for i, f in enumerate(frozen) if f["lines"][0] <= a <= f["lines"][1]), None)
    if owner is None:
        orphan.append((rid, a, b))
        out.append(line)
        continue
    fo = frozen[owner]
    cu = MATCH.get(fo["idx"])
    idx = fo["idx"]

    if cu is None:                       # content gone: the block changed or was removed
        siblings = rows_per_block.get(idx, [])
        # a changed block must be re-identified by POSITION among the current blocks,
        # since its content no longer matches anything. Only safe when it is the sole
        # row in the block; otherwise the A1 refusal applies.
        cand = current[owner] if owner < len(current) else None
        whole = (a == fo["lines"][0] and b == fo["lines"][1]
                 and len(siblings) == 1 and cand is not None)
        if whole:
            na, nb = cand["lines"][0], cand["lines"][1]  # re-derived, not shifted
            extended += 1
        else:
            refused.append((rid, a, b, idx, len(siblings)))
            out.append(line)
            continue
    else:
        d = cu["lines"][0] - fo["lines"][0]
        na = a + d
        nb = cu["lines"][1] if b == fo["lines"][1] else b + d
        if (na, nb) != (a, b):
            shifted += 1

    if (na, nb) != (a, b):
        line = (m.group(1) + str(na) + (m.group(4) + str(nb) if m.group(5) else "")
                + m.group(6) + line[m.end():])
    out.append(line)

print("rows shifted (displaced blocks): %d   rows extended (grown, single-row): %d"
      % (shifted, extended))
if orphan:
    print("  *** rows in no frozen block: %s" % orphan)
if refused:
    print()
    print("  *** REFUSED TO SHIFT %d SUB-ENTRY ROW(S) THROUGH A BLOCK THAT GREW INTERNALLY ***"
          % len(refused))
    for rid, a, b, idx, n in refused:
        print("      row %-4s L%d-%d sits in block %d, which has %d manifest rows and whose"
              % (rid, a, b, idx, n))
        print("           content changed. Its boundary is NOT recoverable by arithmetic.")
        print("           RE-DERIVE it from the source marker that opens its text.")
    print("      Nothing was written. Re-derive these, then re-run.")
    sys.exit(1)

if "--apply" in sys.argv:
    man_p.write_text("\n".join(out), encoding="utf-8")
    print("BLOCK_MANIFEST.md re-anchored.")
else:
    print("(dry run \u2014 pass --apply to write)")
