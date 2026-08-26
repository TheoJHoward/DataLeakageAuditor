#!/usr/bin/env python3
"""DELTA R42 / J1 — repair the over-assignment my own J1 fix introduced.

Two bugs in _J1_fix.py:
  1. tag_of() used a prefix regex, so "SC-12(w) consequential - the section 7.7
     pointer, redrafted" matched "SC-12" and the pointer hunk was OVERWRITTEN with
     SC-12's clause text. That destroyed the R35/B3 pointer redraft.
  2. THE CLAUSE was assigned to a clause's primary hunk, but "primary" was computed
     per block rather than once, so clauses with several hunks got their clause text
     attached to more than one site - five duplications.

A clause's THE CLAUSE lands at exactly ONE site: its primary insertion point.
Markers and second INSERTION TEXT blocks land at their own sites, which they name.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

data = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
hunks = data["hunks"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


def parts_of(op):
    """[(heading, body)] from a rebuilt operative_text."""
    if not op.lstrip().startswith("["):
        return [(None, op)]
    out = []
    for chunk in re.split(r"\n\n(?=\[)", op):
        m = re.match(r"\[(.*?)\]\n(.*)", chunk, re.S)
        out.append((m.group(1), m.group(2).strip()) if m else (None, chunk))
    return out


# Where each clause's THE CLAUSE belongs: its primary insertion site.
PRIMARY = {"SC-1": 266, "SC-2": 451, "SC-3": 461, "SC-4": 464, "SC-5": 464,
           "SC-6": 856, "SC-7": 468, "SC-8": 480, "SC-9": 99, "SC-10": 441,
           "SC-11": 892, "SC-12": 1035, "SC-13a": 1030, "SC-13b": 1035,
           "SC-13c": 1036}

PTR77 = ("**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it "
         "appears, including this table, and **SC-12(w) registers the condition under which a "
         "detector-case may be reported in this state.** Neither is restated here.")

fixed_ptr = 0
dropped = 0
for h in hunks:
    cl = h.get("clause") or ""
    # ---- bug 1: restore the section 7.7 pointer -----------------------------
    if "pointer, redrafted" in cl:
        h["operative_text"] = PTR77
        h.pop("operative_blocks", None)
        fixed_ptr += 1
        continue
    op = h.get("operative_text") or ""
    if not op.lstrip().startswith("["):
        continue
    # ---- bug 2: keep THE CLAUSE only at the clause's primary site -----------
    m = re.match(r"(SC-[0-9]+[a-z]?)\b", cl)
    tag = m.group(1) if m else None
    keep = []
    for heading, body in parts_of(op):
        if heading and "THE CLAUSE" in heading.upper():
            if tag and PRIMARY.get(tag) != ln(h):
                dropped += 1
                continue
        keep.append((heading, body))
    if keep:
        h["operative_text"] = "\n\n".join(
            (f"[{hd}]\n{bd}" if hd else bd) for hd, bd in keep)
        h["operative_blocks"] = [hd for hd, _ in keep if hd]
    else:
        h["operative_text"] = ""
        h.pop("operative_blocks", None)

print(f"pointer hunks restored : {fixed_ptr}")
print(f"stray THE CLAUSE copies removed: {dropped}")

json.dump(data, open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

# ---- verify: no duplication, nothing empty ---------------------------------
import collections
seen = collections.defaultdict(list)
empty = []
for h in hunks:
    op = h.get("operative_text") or ""
    if not op.strip():
        empty.append((ln(h), (h.get("clause") or "")[:40]))
    for heading, body in parts_of(op):
        if len(body) > 200:
            seen[re.sub(r"\s+", " ", body)[:150]].append((ln(h), (h.get("clause") or "")[:34]))
dupes = {k: v for k, v in seen.items() if len(v) > 1}
print(f"\nduplicated blocks across hunks: {len(dupes)}")
for k, v in dupes.items():
    print("   ", v, "|", k[:80])
print(f"hunks with empty operative text: {len(empty)}  {empty}")
