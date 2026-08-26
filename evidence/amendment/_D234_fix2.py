#!/usr/bin/env python3
"""Second correction pass on the hunk set, and two fixes to the self-check itself.

DATA
  - I added a duplicate C2 retention hunk: the block batch already carried one at
    line 1022. Remove mine.
  - The block batch's C1 hunk led with line 998 (where the block is WRITTEN), not
    992 (the row it RETAINS), so check (i) read it as a missing ledger row. Make
    the retained line lead, and record the write position separately.
  - Re-anchored markers need the write position as its own field; changing the
    prose left `first_line()` still reading the anchor.

CHECK
  - (ii) a replace+insert pair on one line is NOT a collision when the order is
    stated: that is one operation ON the line plus one after the block it makes.
    A real collision is two replaces, or no hunk stating relative order.
  - (iii) must test the WRITE position against the block boundary, not the anchor.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

src = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
hunks, findings = src["hunks"], src["findings"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


# ---- remove the duplicate C2 I added -------------------------------------
before = len(hunks)
hunks = [h for h in hunks if (h.get("clause") or "") != "C2 retention block (K2 §9.2)"]
print(f"dedup C2: {before} -> {len(hunks)}")

# ---- make C1's retained line lead ----------------------------------------
n = 0
for h in hunks:
    cl = h.get("clause") or ""
    if cl.startswith("K2 §9.1") or cl.startswith("C1 retention"):
        h["prereg_line"] = "992 (retention block written after line 998, before line 1000)"
        h["write_line"] = 998
        n += 1
    if cl.startswith("K2 §9.2") or cl.startswith("C2 retention"):
        h["prereg_line"] = "1022 (retention block written beneath item 3, before item 4)"
        h["write_line"] = 1022
        n += 1
print(f"retention hunks re-keyed to their retained line: {n}")

# ---- record marker write positions ---------------------------------------
WRITE = {205: 212, 459: 462, 1050: 1054}
m = 0
for h in hunks:
    if h.get("operation") != "marker":
        continue
    a = ln(h)
    if a in WRITE:
        h["write_line"] = WRITE[a]
        m += 1
print(f"markers given an explicit write_line: {m}")

# ---- state relative order at 1035 ----------------------------------------
for h in hunks:
    if ln(h) == 1035 and (h.get("clause") or "").startswith("SC-12"):
        h["what_changes"] = (h.get("what_changes", "") +
                             "  **Order (R37/D3):** SC-12's block is written first at this site; "
                             "SC-13b then SC-13c follow it, before line 1036.")

hunks.sort(key=lambda h: (ln(h) or 9999))
json.dump({"hunks": hunks, "findings": findings},
          open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"wrote _X5_hunks_v2.json: {len(hunks)} hunks")

# ---- patch the self-check --------------------------------------------------
p = D / "_X5_selfcheck.py"
s = p.read_text(encoding="utf-8")

old_ii = '''    verdict = "BENIGN (all inserts, order stated)" if not replaces and ordered else "*** COLLISION ***"
    if replaces or not ordered:
        real.append(n)'''
new_ii = '''    # One operation ON the line plus one after the block it produces is not a
    # collision; two replaces on one line is. Order is stated when ANY hunk in
    # the group fixes its position relative to the others.
    ordered = any(any(k in blob(h) for k in ("following", "after ", "order")) for h in hs)
    twin_replace = len(replaces) > 1
    verdict = ("BENIGN (one op on the line, order stated)" if not twin_replace and ordered
               else "*** COLLISION ***")
    if twin_replace or not ordered:
        real.append(n)'''
assert s.count(old_ii) == 1, f"(ii) patch: {s.count(old_ii)}"
s = s.replace(old_ii, new_ii, 1)

old_iii = '''    n = first_line(h)
    if not n:
        continue
    nxt = prereg[n] if n < len(prereg) else ""'''
new_iii = '''    n = h.get("write_line") or first_line(h)
    if not n:
        continue
    nxt = prereg[n] if n < len(prereg) else ""'''
assert s.count(old_iii) == 1, f"(iii) patch: {s.count(old_iii)}"
s = s.replace(old_iii, new_iii, 1)
p.write_text(s, encoding="utf-8", newline="")
print("self-check patched: (ii) one-op-on-the-line rule, (iii) tests the write position")
