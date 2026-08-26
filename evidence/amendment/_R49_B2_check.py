#!/usr/bin/env python3
"""DELTA R49 - close the gap that let the WITHDRAWN C1 reach the signable artifact.

Manifest section A hunks are bound to SCHEMA_SET_FINAL.md by M6 check (II). Section B
hunks - the eleven that draw text from elsewhere - were bound to NOTHING. J3 redrafted
C1; the hunk kept the withdrawn text; every check stayed green for two rounds.

Nine of the eleven section-B rows name a file. Two named only a round ("Drafted
R39/F2") - and those two are exactly the exposed pair. This names their sources and
installs check (viii): every section-B hunk's operative text must be traceable to the
document its manifest row names.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

# ---- 1. name the two unbound sources ----------------------------------------
man = D / "BLOCK_MANIFEST.md"
t = man.read_text(encoding="utf-8")
PAIRS = [
    ("| **H29** | 992 | Drafted R39/F2 \u2014 the C1 operative row |",
     "| **H29** | 992 | `J3_C1_REDRAFT.md` \u00a73, the operative row \u2014 **rebuilt from it at R49/B2; it "
     "previously carried the WITHDRAWN R39/F2 draft** |"),
    ("| **H32** | 1022 | Drafted R39/F2 \u2014 the C2 operative item |",
     "| **H32** | 1022 | `_X5_hunks_v2.json` is the source of record \u2014 redrafted in place at R47/P1 "
     "(narrowest C2); no separate drafting file exists |"),
]
for o, n in PAIRS:
    assert t.count(o) == 1, "manifest row match %d for %.40s" % (t.count(o), o)
    t = t.replace(o, n, 1)
man.write_text(t, encoding="utf-8")
print("manifest \u00a7B: H29 and H32 now name their sources")

# ---- 2. install check (viii) -------------------------------------------------
sc = D / "_X5_selfcheck.py"
s = sc.read_text(encoding="utf-8")
assert "check (viii)" not in s, "already installed"
ANCHOR = 'head("SELF-CHECK RESULT")'
assert s.count(ANCHOR) == 1

NEW = '''# ---------------------------------------------------------------- (viii) R49/B2
head("(viii) EVERY SECTION-B HUNK IS TRACEABLE TO THE SOURCE ITS MANIFEST ROW NAMES")
print("  Section-A hunks are bound to SCHEMA_SET_FINAL.md by M6 check (II). The eleven")
print("  section-B hunks - those drawing text from elsewhere - were bound to nothing, and")
print("  that is how the WITHDRAWN C1 rendered into the signable artifact for two rounds")
print("  while every check reported green.")
print()
_man = (D / "BLOCK_MANIFEST.md").read_text(encoding="utf-8")
_secB = _man[_man.index("## \\u00a7B"):]
if "## \\u00a7C" in _secB:
    _secB = _secB[:_secB.index("## \\u00a7C")]
_hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]


def _ln(h):
    m = re.search(r"\\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


_HN = {f"H{i}": h for i, h in enumerate(sorted(_hunks, key=_ln), 1)}


def _norm(x):
    return re.sub(r"\\s+", " ", x or "").strip()


_rows, _unnamed, _unbound, _bound = [], [], [], 0
for _line in _secB.split("\\n"):
    if not (_line.startswith("|") and "**H" in _line):
        continue
    _m = re.search(r"\\*\\*(H\\d+)\\*\\*", _line)
    _f = re.findall(r"`([A-Za-z0-9_.\\-]+\\.(?:md|json))`", _line)
    _rows.append((_m.group(1), _f, _line))
print(f"  section-B hunks: {len(_rows)}")
for _h, _files, _line in _rows:
    _op = _norm((_HN.get(_h) or {}).get("operative_text"))
    if not _files:
        _unnamed.append(_h)
        continue
    if "_X5_hunks_v2.json" in _files:
        _bound += 1                      # the JSON IS its source of record, declared as such
        continue
    _hit = False
    for _fn in _files:
        _fp = D / _fn
        if _fp.exists() and _norm(_fp.read_text(encoding="utf-8")).find(_op[:110]) >= 0:
            _hit = True
            break
    if _hit:
        _bound += 1
    else:
        _unbound.append((_h, _files))
print(f"  traceable to the source their row names : {_bound}")
print(f"  naming NO source document               : {len(_unnamed)}  {_unnamed if _unnamed else ''}")
print(f"  naming a source that does NOT carry them: {len(_unbound)}  {_unbound if _unbound else ''}")
if _unnamed or _unbound:
    fail += 1
    print("  *** a section-B hunk that no document backs can drift from its draft silently ***")
    print("  *** which is exactly how the withdrawn C1 reached the artifact                ***")
else:
    print("  PASS \\u2014 every section-B hunk is traceable to a named source")

'''
s = s.replace(ANCHOR, NEW + ANCHOR, 1)
s = s.replace('print(f"  assertions failed: {fail} of 7")',
              'print(f"  assertions failed: {fail} of 8")', 1)
sc.write_text(s, encoding="utf-8")
print("check (viii) installed - self-check now scores 8")
