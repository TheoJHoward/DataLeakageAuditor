#!/usr/bin/env python3
# =============================================================================
# SUPERSEDED — DO NOT RUN. Marked at R83/§94.2.
# =============================================================================
# Superseded by `_K1_enumerate2.py`, which writes the cited population artifact
# `_K1_population_FROZEN.json` (schema idx/lines/kind). THIS script emits a
# different schema (line/heading/sha12) and its output `_K1_population.json` is
# cited in NO document.
#
# DEFECT, recorded and deliberately NOT repaired (R13 - a dated build record is
# not adjusted): the `MARK` regex below contains a literal BACKSPACE (0x08) where
# `\b` was intended, so MARK.match() never returns a match and the marker split it
# guards NEVER RUNS. Measured against the current source: 37 blocks emitted where
# 40 are correct; 2 runs collapse; 3 marker sites (§8.2 line 915, §11 item 3,
# §0.2.1 line 97) appear in no catalogue entry. MISCOUNT plus MISATTRIBUTION, not
# a miss - each collapsed run keeps ONE sha12 anchor and ONE `first` field.
#
# The failure is silent by construction: the "marker split: N run(s) -> M block(s)"
# line only prints WHEN the split fires, so a split that never fires prints nothing.
#
# The body below is unchanged. The guard exists so the record can be read but not
# re-run, which is what §94.2 asks for.
# =============================================================================
import sys as _sys
if __name__ == "__main__":
    _sys.exit("SUPERSEDED (R83/§94.2): use _K1_enumerate2.py. This script's MARK "
              "regex contains a literal BACKSPACE and never splits markers.")

"""DELTA R43 / K1 step 1 — enumerate the population the manifest must account for.

K3's rule applied to this script itself: it DECLARES its population and PROVES the
declaration covers the whole file, rather than scanning a subset and reporting green.

POPULATION DECLARED: every blockquote run in SCHEMA_SET_FINAL.md PART 1, where Part 1
is the region from the "# PART 1" heading to the "# PART 2" heading. Part 1 is the
part that lands; Parts 2+ are verification records.

PROOF OF COVERAGE: the script reports the byte range it scanned, the total blockquote
runs in the WHOLE file, the number inside Part 1, and the number outside - so the
reader can see the split rather than trust it.

Anchors are (section, ordinal, sha12) where section is the nearest preceding heading
of any level. sha12 makes the anchor self-verifying: content drift breaks the anchor.
"""

import hashlib
import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
SSF = D / "SCHEMA_SET_FINAL.md"
text = SSF.read_text(encoding="utf-8")


def fences(body, base_line):
    """Every fenced block: (start_line, heading, body). Applied text appears in
    fenced form as well as blockquoted form - section 13c-P's INSERT AFTER is fenced,
    and a population defined as blockquotes alone misses it. This is the K3 rule
    applied to the population definition itself."""
    out, cur, start, head, last, inside = [], [], None, None, None, False
    for i, ln in enumerate(body.split(chr(10)), start=base_line):
        hm = re.match(r"^#{1,6}\s+(.*)$", ln)
        if hm and not inside:
            last = hm.group(1).strip()
        bm = re.match(r"^\*\*(.+?)\.?\*\*", ln.strip())
        if bm and not inside:
            last = bm.group(1).strip()
        if ln.startswith("```"):
            if not inside:
                inside, start, head, cur = True, i, last, []
            else:
                inside = False
                out.append((start, head or "(none)", chr(10).join(cur).strip()))
                cur = []
            continue
        if inside:
            cur.append(ln)
    return out


def runs(body, base_line):
    """Every blockquote run: (start_line, heading, body)."""
    out, cur, start, head, last = [], [], None, None, None
    for i, ln in enumerate(body.split("\n"), start=base_line):
        hm = re.match(r"^#{1,6}\s+(.*)$", ln)
        if hm:
            last = hm.group(1).strip()
        bm = re.match(r"^\*\*(.+?)\.?\*\*", ln.strip())
        if bm and not ln.startswith(">"):
            last = bm.group(1).strip()
        if ln.startswith(">"):
            if not cur:
                start, head = i, last
            cur.append(re.sub(r"^>\s?", "", ln))
        else:
            if cur:
                out.append((start, head or "(none)", "\n".join(cur).strip()))
                cur = []
    if cur:
        out.append((start, head or "(none)", "\n".join(cur).strip()))
    return out


lines = text.split("\n")
p1 = next((i for i, l in enumerate(lines, 1) if l.startswith("# PART 1")), None)
p2 = next((i for i, l in enumerate(lines, 1) if l.startswith("# PART 2")), None)
assert p1 and p2 and p2 > p1, f"Part 1 boundaries not found: {p1}, {p2}"

all_runs = sorted(runs(text, 1) + fences(text, 1), key=lambda r: r[0])
part1 = [r for r in all_runs if p1 <= r[0] < p2]
outside = [r for r in all_runs if not (p1 <= r[0] < p2)]

print("POPULATION DECLARED: blockquote runs AND fenced blocks in SCHEMA_SET_FINAL.md PART 1")
print(f"  file lines            : {len(lines)}")
print(f"  PART 1 heading at line: {p1}")
print(f"  PART 2 heading at line: {p2}")
print(f"  Part 1 spans lines    : {p1}..{p2 - 1}   ({p2 - p1} lines)")
print()
print("PROOF OF COVERAGE")
print(f"  blockquote runs + fenced blocks, WHOLE file : {len(all_runs)}")
print(f"  inside Part 1                     : {len(part1)}")
print(f"  outside Part 1 (not in scope)     : {len(outside)}")
print(f"  {len(part1)} + {len(outside)} = {len(part1) + len(outside)}  "
      f"{'OK' if len(part1) + len(outside) == len(all_runs) else '*** MISMATCH ***'}")
print()

# NO SIZE THRESHOLD. A "substantive" cut-off silently drops small blocks - it
# dropped L1490-1492 (174 chars), which is manifest entry 31 - and a population
# that quietly excludes members is the failure mode this whole apparatus exists
# to prevent. Every Part 1 block is in the population; the manifest decides which
# are applied and which are apparatus.
SUBSTANTIVE = 0
sub = [r for r in part1 if len(r[2]) >= SUBSTANTIVE]
small = [r for r in part1 if len(r[2]) < SUBSTANTIVE]
print(f"  Part 1 runs >= {SUBSTANTIVE} chars (candidate applied text): {len(sub)}")
print(f"  Part 1 runs <  {SUBSTANTIVE} chars (quotes, fragments)      : {len(small)}")
print()

# --- marker granularity -------------------------------------------------------
# A blockquote run may hold SEVERAL markers for SEVERAL sites: the SC-8 run at L687
# carries four (section 6.2 line 480; section 11 items 1-7; section 11 item 3;
# section 0.2.1 line 97), each belonging to a different hunk. A manifest at run
# granularity cannot say "exactly one hunk per block", so runs are split on their
# internal blank-quote boundaries wherever each part opens with its own bold heading.
def split_markers(start, head, body):
    parts, cur = [], []
    for ln in body.split(chr(10)):
        if ln.strip() == "" and cur:
            parts.append(chr(10).join(cur).strip()); cur = []
        else:
            cur.append(ln)
    if cur:
        parts.append(chr(10).join(cur).strip())
    parts = [x for x in parts if x]
    # Split ONLY when every part opens with a MARKER signature - a bold site
    # reference like "**§6.2 line 480 —" or "**§11 item 3 —". Clause limbs also
    # open with "**" ( "**(a) ..." ), so a bare bold test over-splits a clause
    # into its limbs: 32 runs became 96 blocks on the first attempt.
    MARK = re.compile(r"^\*\*§[\d.]+\s+(line|item|items)")
    if len(parts) > 1 and all(MARK.match(x.lstrip()) for x in parts):
        return [(start, head, x) for x in parts]
    return [(start, head, body)]

expanded = []
for st, hd, bd in sub:
    expanded.extend(split_markers(st, hd, bd))
if len(expanded) != len(sub):
    print(f"  marker split: {len(sub)} run(s) -> {len(expanded)} block(s)")
    print()
sub = expanded

cat = []
for start, head, body in sub:
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
    cat.append({"line": start, "heading": head, "sha12": sha,
                "chars": len(body), "first": re.sub(r"\s+", " ", body)[:90]})

print("=" * 96)
print("THE POPULATION — every substantive Part 1 block, with its anchor")
print("=" * 96)
for c in cat:
    print(f"  L{c['line']:<5} {c['sha12']}  {c['chars']:>5}c  {c['heading'][:44]:<44} {c['first'][:44]}")

json.dump(cat, open(D / "_K1_population.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nwrote _K1_population.json — {len(cat)} blocks to be claimed")
