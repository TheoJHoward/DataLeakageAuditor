#!/usr/bin/env python3
"""DELTA R42 / J1 — block-by-block sweep of every hunk's operative text against source.

The R39/F3 extractor took each clause's "THE CLAUSE." blockquote and nothing else.
Any clause whose applied text also includes a SUPERSESSION MARKER, a bounds block, or
a second INSERTION TEXT block therefore landed incomplete. Hunk 2.33 (SC-13a) is the
instance that surfaced; J1's premise is that one omission indicts the extractor, so
this sweeps all of them.

Read-only. Reports; writes nothing.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]

# Headings whose blockquote is APPLIED TEXT (lands in PREREG.md), per
# SCHEMA_SET_FINAL.md's own convention: only THE CLAUSE, SUPERSESSION MARKER text at
# the superseded site, and INSERTION TEXT blocks are applied.
APPLIED = ("THE CLAUSE", "SUPERSESSION MARKER", "INSERTION TEXT",
           "What this limb does NOT permit")
# Headings whose blockquote is apparatus and must NOT land.
APPARATUS = ("DATA THE DECLARATION MUST SUPPLY", "Instance record", "ROWS COVERED",
             "REGISTERS", "INSERTION POINT", "Why it is drafted", "Corroboration")


def clause_sections(text):
    """{tag: body} for every ### SC-n heading."""
    out = {}
    ms = list(re.finditer(r"^### (SC-[0-9]+[a-z]?) — .*$", text, re.M))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out[m.group(1)] = text[m.start():end]
    return out


def blocks_in(body):
    """[(heading, blockquote_text)] for each blockquote run, tagged by nearest
    preceding bold heading."""
    lines = body.split("\n")
    res, cur, head = [], [], None
    last_bold = None
    for ln in lines:
        bm = re.match(r"^\*\*(.+?)\.?\*\*", ln.strip())
        if bm and not ln.startswith(">"):
            last_bold = bm.group(1)
        if ln.startswith(">"):
            if not cur:
                head = last_bold
            cur.append(re.sub(r"^>\s?", "", ln))
        else:
            if cur:
                res.append((head or "(untitled)", "\n".join(cur).strip()))
                cur, head = [], None
    if cur:
        res.append((head or "(untitled)", "\n".join(cur).strip()))
    return res


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


secs = clause_sections(ssf)
print(f"clause sections found: {len(secs)}  ({', '.join(sorted(secs))})")
print()

# map hunks to a clause tag
def tag_of(h):
    cl = h.get("clause") or ""
    m = re.match(r"(SC-[0-9]+[a-z]?)", cl)
    return m.group(1) if m else None

by_tag = {}
for h in hunks:
    t = tag_of(h)
    if t:
        by_tag.setdefault(t, []).append(h)

print("=" * 78)
print("BLOCK-BY-BLOCK SWEEP — applied blocks present in source vs carried in a hunk")
print("=" * 78)
missing_total = 0
report = []
for tag in sorted(secs, key=lambda x: (len(x), x)):
    body = secs[tag]
    blocks = blocks_in(body)
    applied = [(hd, b) for hd, b in blocks
               if hd and any(k.lower() in hd.lower() for k in APPLIED)]
    if not applied:
        continue
    hs = by_tag.get(tag, [])
    carried = norm(" ".join((h.get("operative_text") or "") for h in hs))
    print(f"\n{tag}:  applied blocks in source = {len(applied)}   hunks = {len(hs)}")
    for hd, b in applied:
        first = norm(b)[:70]
        present = norm(b)[:120] in carried
        flag = "carried" if present else "*** DROPPED ***"
        print(f"   [{flag:>15}] {hd[:38]:<38} | {first[:58]}")
        if not present:
            missing_total += 1
            report.append((tag, hd, b))

print()
print("=" * 78)
print(f"RESULT: {missing_total} applied block(s) dropped by the extractor")
print("=" * 78)
for tag, hd, b in report:
    print(f"\n--- {tag} :: {hd}")
    print("\n".join("    " + l for l in b.split("\n")[:6]))
    if len(b.split("\n")) > 6:
        print("    ...")
