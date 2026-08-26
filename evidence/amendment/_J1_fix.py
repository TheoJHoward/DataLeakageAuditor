#!/usr/bin/env python3
"""DELTA R42 / J1 — rebuild operative_text from ALL applied blocks, site-mapped.

The R39/F3 extractor took one blockquote per clause ("THE CLAUSE.") and dropped
every SUPERSESSION MARKER and every second INSERTION TEXT block - twelve in all.
The markers are what carry the retained v30 text, so the amendments block's item 1,
"No registered sentence is deleted from this file", was landing false for ten
clauses.

The fix maps each applied block to the hunk at ITS OWN SITE rather than to its
clause, because a clause with two insertion points produces two hunks and its blocks
belong to different ones. Each block names its site in its own text.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ssf = (D / "SCHEMA_SET_FINAL.md").read_text(encoding="utf-8")
data = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
hunks = data["hunks"]

APPLIED = ("THE CLAUSE", "SUPERSESSION MARKER", "INSERTION TEXT",
           "What this limb does NOT permit")


def sections(text):
    out, ms = {}, list(re.finditer(r"^### (SC-[0-9]+[a-z]?) — .*$", text, re.M))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out[m.group(1)] = text[m.start():end]
    return out


def blocks_in(body):
    lines, res, cur, head, last = body.split("\n"), [], [], None, None
    for ln in lines:
        bm = re.match(r"^\*\*(.+?)\.?\*\*", ln.strip())
        if bm and not ln.startswith(">"):
            last = bm.group(1)
        if ln.startswith(">"):
            if not cur:
                head = last
            cur.append(re.sub(r"^>\s?", "", ln))
        else:
            if cur:
                res.append((head or "(untitled)", "\n".join(cur).strip()))
                cur, head = [], None
    if cur:
        res.append((head or "(untitled)", "\n".join(cur).strip()))
    return [(h, b) for h, b in res if h and any(k.lower() in h.lower() for k in APPLIED)]


def site_of(heading, body):
    """The PREREG line this block attaches to, from its own text."""
    for src in (heading, body[:400]):
        m = re.search(r"line\s+(\d{2,4})", src)
        if m:
            return int(m.group(1))
    return None


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


def tag_of(h):
    m = re.match(r"(SC-[0-9]+[a-z]?)", h.get("clause") or "")
    return m.group(1) if m else None


secs = sections(ssf)
assign = {}          # id(hunk) -> [blocks in source order]
unassigned = []

for tag, body in secs.items():
    hs = [h for h in hunks if tag_of(h) == tag]
    if not hs:
        continue
    for heading, block in blocks_in(body):
        site = site_of(heading, block)
        target = None
        if site is not None:
            cands = [h for h in hs if ln(h) == site]
            if cands:
                # a marker block goes to the marker hunk where one exists
                mk = [h for h in cands if h.get("operation") == "marker"]
                if "SUPERSESSION MARKER" in heading.upper() and mk:
                    target = mk[0]
                else:
                    target = cands[0]
        if target is None:
            # THE CLAUSE and unsited blocks go to the clause's primary hunk
            prim = [h for h in hs if h.get("operation") in ("insert", "replace", "replace-row")]
            target = prim[0] if prim else hs[0]
        assign.setdefault(id(target), []).append((heading, block))

added = 0
for h in hunks:
    blocks = assign.get(id(h))
    if not blocks:
        continue
    cur = (h.get("operative_text") or "").strip()
    parts, seen = [], set()
    for heading, block in blocks:
        key = re.sub(r"\s+", " ", block)[:120]
        if key in seen:
            continue
        seen.add(key)
        parts.append((heading, block))
    rebuilt = []
    for heading, block in parts:
        rebuilt.append(f"[{heading}]\n{block}")
    new = "\n\n".join(rebuilt)
    if re.sub(r"\s+", " ", new) != re.sub(r"\s+", " ", cur):
        h["operative_text"] = new
        h["operative_blocks"] = [p[0] for p in parts]
        added += 1

print(f"hunks whose operative_text was rebuilt from all applied blocks: {added}")
print()
for h in hunks:
    if h.get("operative_blocks"):
        print(f"  line {ln(h):<5} {h.get('clause','')[:34]:<34} blocks: {h['operative_blocks']}")

json.dump(data, open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\nwrote _X5_hunks_v2.json ({len(hunks)} hunks)")
