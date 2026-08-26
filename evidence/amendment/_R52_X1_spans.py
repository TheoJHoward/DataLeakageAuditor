#!/usr/bin/env python3
"""DELTA R52/X1 - declare a source SPAN for every section-B hunk, in the MANIFEST.

The manifest is the authority (M1), so spans are declared there and read from there -
not hardcoded in the checker. Each span is a (start, end) marker pair delimiting the
operative block inside the named source; the checker extracts it FRESH from the source
each run and requires it to survive verbatim inside the hunk.

Why this matters, for the record: DELETION is the class that produced hunk 2.33, and
coverage tiling is deletion-blind by construction - removing text never lowers the
provenance of what remains. Only the converse direction sees it.

Markers are DERIVED from the source, verified UNIQUE in it, and verified to bracket a
block that is present in the hunk today. Two hunks are SELF-SOURCED: their source of
record IS `_X5_hunks_v2.json`, so there is no external document to check against and
the span test cannot apply. That is declared, not silently skipped.
"""
import json
import pathlib
import re
import importlib.util

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
spec = importlib.util.spec_from_file_location("prov", str(D / "_provenance.py"))
prov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prov)
prov.MAX_PROBE = 4000

man_p = D / "BLOCK_MANIFEST.md"
man = man_p.read_text(encoding="utf-8")
secA = man[:man.index("## \u00a7B")]
hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}
MARK = 55


def longest_common(op, src):
    best = (0, 0)
    i = 0
    while i < len(op):
        n = prov.longest_match_at(op, i, [src])
        if n > best[0]:
            best = (n, i)
        i += max(1, n)
    return best


out, declared, selfsourced = [], 0, 0
for line in man.split("\n"):
    if not (line.startswith("|") and "**H" in line):
        out.append(line)
        continue
    hid_m = re.search(r"\*\*(H\d+)\*\*", line)
    if not hid_m or "span:" in line:
        out.append(line)
        continue
    hid = hid_m.group(1)
    if re.search(r"\*\*" + hid + r"\*\*", secA):
        out.append(line)                       # section-A claimed; M6 (II) binds it
        continue
    files = re.findall(r"`([A-Za-z0-9_.\-]+\.(?:md|json))`", line)
    op = prov.norm((HN.get(hid) or {}).get("operative_text"))
    if not op or not files:
        out.append(line)
        continue
    if files[0] == "_X5_hunks_v2.json":
        line = line.rstrip().rstrip("|").rstrip() + " span:SELF-SOURCED |"
        selfsourced += 1
        out.append(line)
        continue
    src = prov.norm((D / files[0]).read_text(encoding="utf-8"))
    n, a = longest_common(op, src)
    blk = op[a:a + n]
    start, end = blk[:MARK], blk[-MARK:]
    assert src.count(start) == 1, "%s: start marker not unique (%d)" % (hid, src.count(start))
    assert src.count(end) == 1, "%s: end marker not unique (%d)" % (hid, src.count(end))
    i, j = src.find(start), src.find(end)
    assert i >= 0 and j > i, "%s: markers do not bracket" % hid
    extracted = src[i:j + len(end)]
    assert extracted in op, "%s: extracted span is not in the hunk (%d chars)" % (hid, len(extracted))
    line = (line.rstrip().rstrip("|").rstrip()
            + " span:\u00ab%s\u00bb\u2026\u00ab%s\u00bb |" % (start, end))
    declared += 1
    out.append(line)

man_p.write_text("\n".join(out), encoding="utf-8")
print("spans declared in the manifest : %d" % declared)
print("declared SELF-SOURCED           : %d" % selfsourced)
print("every declared span was verified UNIQUE in its source and PRESENT in its hunk")
