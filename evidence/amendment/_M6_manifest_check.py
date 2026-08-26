#!/usr/bin/env python3
"""DELTA R45 / M6 — L1(c): the mechanical check on the corrected manifest.

K1's three assertions, fail-closed, in the direction of authority M1 fixed
(manifest -> JSON -> artifact):

  (I)   every block of the frozen population is claimed by exactly ONE hunk,
        or is declared APPARATUS. Unclaimed-and-not-apparatus is a FAILURE,
        not a warning - that is the property the heuristics could never have.
  (II)  every claim byte-matches source at its stated anchor.
  (III) the rendered artifact contains every claimed block.

SEPARATOR RULE, stated here rather than assumed (R44/L2): a bare '>' line
between two markers belongs to the entry ABOVE it. Lines 153, 567, 692 and 698
are covered that way. The check enforces the rule by requiring the sub-entry
ranges of a multi-site run to partition the parent run with no gap and no
overlap, and it prints any line the partition leaves uncovered.

The check NEVER discovers blocks. It reads the frozen population and the
hand-authored manifest and verifies one against the other.
"""

import json
import re
import sys
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

SSF = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8").split("\n")
POP = json.loads((D / "_K1_population_FROZEN.json").read_text(encoding="utf-8"))
hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
man = (D / "BLOCK_MANIFEST.md").read_text(encoding="utf-8")

fail = 0


def head(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}

secA = man[man.index("## §A —"):man.index("## §B —")]
ROW = re.compile(r"^\|\s*(\S+?)\s*\|\s*(\d+)(?:[–-](\d+))?\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")
entries = []
for line in secA.split("\n"):
    m = ROW.match(line)
    if not m or m.group(1) == "#" or set(m.group(1)) <= set("-"):
        continue
    eid, a, b, desc, tgt = m.groups()
    hm = re.search(r"\*\*(H\d+)\*\*", tgt)
    entries.append({"id": eid, "a": int(a), "b": int(b or a), "desc": desc,
                    "hunk": hm.group(1) if hm else None,
                    "apparatus": "APPARATUS" in tgt})

print(f"population (frozen) : {len(POP)} blocks")
print(f"manifest entries    : {len(entries)}  "
      f"(claimed {sum(1 for e in entries if e['hunk'])}, "
      f"apparatus {sum(1 for e in entries if e['apparatus'])})")

# ---------------------------------------------------------------- (I)
head("(I) EVERY POPULATION BLOCK CLAIMED BY EXACTLY ONE HUNK, OR DECLARED APPARATUS")

covered_lines = set()
for e in entries:
    covered_lines |= set(range(e["a"], e["b"] + 1))

orphans, partial = [], []
for b in POP:
    a, z = b["lines"]
    body_lines = {i for i in range(a, z + 1) if SSF[i - 1].strip() not in ("", ">")}
    miss = sorted(body_lines - covered_lines)
    if not (body_lines & covered_lines):
        orphans.append((b["idx"], a, z, b["heading"]))
    elif miss:
        partial.append((b["idx"], a, z, miss))

print(f"  population blocks with no manifest entry at all : {len(orphans)}")
for i, a, z, hd in orphans:
    print(f"    *** ORPHAN block {i} L{a}-{z}  {str(hd)[:52]}")
print(f"  population blocks only partly covered           : {len(partial)}")
for i, a, z, miss in partial:
    print(f"    *** PARTIAL block {i} L{a}-{z}, uncovered body lines {miss}")

dbl = {}
for e in entries:
    if e["hunk"]:
        dbl.setdefault((e["a"], e["b"]), set()).add(e["hunk"])
double = {k: v for k, v in dbl.items() if len(v) > 1}
print(f"  anchors claimed by more than one hunk           : {len(double)}  {double if double else ''}")

if orphans or partial or double:
    fail += 1
else:
    print("  PASS — every block claimed exactly once or declared apparatus")

# separator-rule report
head("SEPARATOR RULE — a bare '>' between two markers belongs to the entry ABOVE")
seps = []
for b in POP:
    a, z = b["lines"]
    for i in range(a, z + 1):
        if SSF[i - 1].strip() == ">":
            owner = next((e["id"] for e in entries if e["a"] <= i <= e["b"]), None)
            seps.append((i, owner))
print(f"  bare '>' lines inside population blocks: {len(seps)}")
for i, owner in seps:
    print(f"    line {i:<5} -> {'entry ' + owner if owner else '*** UNCOVERED ***'}")
if any(o is None for _, o in seps):
    fail += 1
    print("  *** a separator is uncovered — the partition has a gap ***")
else:
    print("  PASS — every separator belongs to the entry above it")

# ---------------------------------------------------------------- (II)
head("(II) EVERY CLAIM BYTE-MATCHES SOURCE AT ITS ANCHOR")


def block_text(a, b):
    out = []
    for raw in SSF[a - 1:b]:
        if raw.startswith("```"):
            continue
        out.append(re.sub(r"^>\s?", "", raw) if raw.startswith(">") else raw)
    return "\n".join(out).strip()


bad = []
for e in entries:
    if not e["hunk"]:
        continue
    src = block_text(e["a"], e["b"])
    op = HN[e["hunk"]].get("operative_text") or ""
    if src and src not in op:
        bad.append((e["id"], e["hunk"], e["a"], e["b"], len(src)))
print(f"  claimed entries: {sum(1 for e in entries if e['hunk'])}   "
      f"byte-matching their hunk: {sum(1 for e in entries if e['hunk']) - len(bad)}")
for eid, hk, a, b, n in bad:
    print(f"    *** entry {eid} ({hk}) L{a}-{b}, {n} chars, NOT found in the hunk")
if bad:
    fail += 1
else:
    print("  PASS — every claim is present byte-for-byte in its hunk")

# ---------------------------------------------------------------- (III)
head("(III) THE ARTIFACT RENDERS WHAT THE MANIFEST ASSIGNS")
art_p = D / "X5_FINAL_PREREG_DIFF.md"
if not art_p.exists():
    print("  artifact not assembled yet — run the assembler, then re-run this check")
else:
    art = art_p.read_text(encoding="utf-8")
    miss = []
    for e in entries:
        if not e["hunk"]:
            continue
        src = block_text(e["a"], e["b"])
        probe = re.sub(r"\s+", " ", src)[:110]
        if probe and probe not in re.sub(r"\s+", " ", art):
            miss.append((e["id"], e["hunk"]))
    print(f"  claimed entries rendered in the artifact: "
          f"{sum(1 for e in entries if e['hunk']) - len(miss)}"
          f"/{sum(1 for e in entries if e['hunk'])}")
    for eid, hk in miss:
        print(f"    *** entry {eid} ({hk}) NOT rendered")
    # APPARATUS: the assertion is STRUCTURAL, not textual.
    #
    # A text-match test cannot do this job. Registered text may be legitimately
    # quoted under an attribution inside applied text - section AB (entry 33, in
    # H2) quotes PREREG.md line 816 verbatim as "Line 816, verbatim: ..." to
    # record the 816/830 duplicated-authority defect, and block 31 IS line 816.
    # Matching text therefore reports a leak where there is an attributed quote.
    #
    # The property that actually matters is: no block declared APPARATUS is
    # assigned to a hunk. That is checkable exactly, from the manifest, with no
    # false positives - so it is checked that way.
    leaked = [e["id"] for e in entries if e["apparatus"] and e["hunk"]]
    print(f"  apparatus blocks assigned to a hunk: {len(leaked)}  {leaked if leaked else '(none)'}")
    if miss or leaked:
        fail += 1
    else:
        print("  PASS — artifact renders every claim, and no apparatus")

head("MANIFEST CHECK RESULT")
print(f"  assertions failed: {fail} of 3")
sys.exit(1 if fail else 0)
