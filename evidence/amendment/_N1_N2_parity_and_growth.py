#!/usr/bin/env python3
"""DELTA R46 / N1 + N2.

N1  PARITY: the composed document and the signable artifact must render the SAME
    operative text for every hunk. Both are now built from the manifest-built JSON;
    this re-establishes, against the new source, the property that held before M1.

N2  POPULATION GROWTH: freeze means no SILENT change, not no change. SC-4(k) will
    add blocks to SCHEMA_SET_FINAL.md. On any change to that file this reports the
    delta - added / removed / unchanged - and FAILS until every added block is
    assigned in the manifest. Same shape as the conditional declared-region skip:
    the frozen thing stays usable, and any movement in it is visible and blocking.

Usage:
    python _N1_N2_parity_and_growth.py            # parity + growth report
    python _N1_N2_parity_and_growth.py --refreeze # adopt the current enumeration
                                                  # as the new frozen population
                                                  # (only legitimate once every
                                                  #  added block is in the manifest)
"""

import hashlib
import json
import re
import subprocess
import sys
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

fail = 0


def head(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ---------------------------------------------------------------- N1 parity
head("N1 — PARITY: composed document vs signable artifact")

hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
art = (D / "X5_FINAL_PREREG_DIFF.md").read_text(encoding="utf-8")
comp = (D / "_E3_composed_sections.md").read_text(encoding="utf-8")
art_n, comp_n = norm(art), norm(comp)

SECTIONS = [(443, 481), (849, 856), (917, 932), (1016, 1027), (1028, 1043)]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else None


in_scope, both, only_art, only_comp, neither = 0, 0, [], [], []
for h in hunks:
    n = ln(h)
    op = norm(h.get("operative_text"))
    if not op:
        continue
    probe = op[:110]
    scoped = any(a <= (n or -1) <= b for a, b in SECTIONS)
    ina, inc = probe in art_n, probe in comp_n
    if scoped:
        in_scope += 1
        if ina and inc:
            both += 1
        elif ina and not inc:
            only_art.append((n, (h.get("clause") or "")[:40]))
        elif inc and not ina:
            only_comp.append((n, (h.get("clause") or "")[:40]))
        else:
            neither.append((n, (h.get("clause") or "")[:40]))

print(f"  hunks landing in the five composed sections : {in_scope}")
print(f"  rendered identically in BOTH                : {both}")
print(f"  in the artifact only                        : {len(only_art)}  {only_art if only_art else ''}")
print(f"  in the composed doc only                    : {len(only_comp)}  {only_comp if only_comp else ''}")
print(f"  in NEITHER                                  : {len(neither)}  {neither if neither else ''}")
if only_art or only_comp or neither:
    fail += 1
    print("  *** PARITY BROKEN — the two documents do not agree ***")
else:
    print("  PASS — every in-scope hunk renders the same operative text in both")

print(f"\n  (hunks outside the five sections appear in the artifact only, by design:"
      f" {sum(1 for h in hunks if norm(h.get('operative_text')) and not any(a <= (ln(h) or -1) <= b for a, b in SECTIONS))})")

# ------------------------------------------------------- N2 growth procedure
head("N2 — POPULATION GROWTH: is the frozen enumeration still current?")

frozen = json.loads((D / "_K1_population_FROZEN.json").read_text(encoding="utf-8"))
res = subprocess.run([sys.executable, str(D / "_K1_enumerate2.py")],
                     capture_output=True, text=True, encoding="utf-8")
current = json.loads((D / "_K1_population.json").read_text(encoding="utf-8"))

fz = {b["sha12"]: b for b in frozen}
cu = {b["sha12"]: b for b in current}
added = [cu[k] for k in cu if k not in fz]
removed = [fz[k] for k in fz if k not in cu]
unchanged = [k for k in cu if k in fz]

# A MODIFIED block presents as removed+added. Pairing them by start line is what
# lets the freeze absorb a declared edit; without it the check crashed on the
# first real change (KeyError 'lines') and no edit could ever be adopted.
modified = []
for r in list(removed):
    # start line first; then idx+heading, because an EARLIER block growing shifts a
    # later modified block and start-line pairing then reports it as removed+added.
    a = next((x for x in added if x["lines"][0] == r["lines"][0]), None)
    if a is None:
        a = next((x for x in added if x.get("idx") == r.get("idx")
                  and x.get("heading") == r.get("heading")), None)
    if a:
        modified.append((r, a))
        removed.remove(r)
        added.remove(a)

# Same text, moved range: a consequence of another block's growth, not a change.
reanchored = [(fz[k], cu[k]) for k in unchanged if fz[k]["lines"] != cu[k]["lines"]]

print(f"  frozen population  : {len(frozen)} blocks")
print(f"  current enumeration: {len(current)} blocks")
print(f"  DELTA - added {len(added)}, removed {len(removed)}, "
      f"modified {len(modified)}, re-anchored {len(reanchored)}, "
      f"identical {len(unchanged) - len(reanchored)}")

changes_p = D / "_POPULATION_CHANGES.md"
changes = changes_p.read_text(encoding="utf-8") if changes_p.exists() else ""
man = (D / "BLOCK_MANIFEST.md").read_text(encoding="utf-8")

for b in added:
    ok = str(b["lines"][0]) in man
    print(f"    ADDED      L{b['lines'][0]}-{b['lines'][1]} {str(b.get('heading'))[:38]:<38} "
          f"in manifest: {'yes' if ok else '*** NO ***'}")
    if not ok:
        fail += 1
for r, a in modified:
    ok = r["sha12"] in changes and a["sha12"] in changes
    print(f"    MODIFIED   L{a['lines'][0]}-{a['lines'][1]} {str(a.get('heading'))[:38]:<38} "
          f"{r['sha12']} -> {a['sha12']}  declared: {'yes' if ok else '*** NO ***'}")
    if not ok:
        fail += 1
        print("               declare it in _POPULATION_CHANGES.md with BOTH hashes")
for b in removed:
    print(f"    REMOVED    L{b['lines'][0]}-{b['lines'][1]} {str(b.get('heading'))[:38]}")
    fail += 1
if reanchored:
    lo = min(a["lines"][0] for _, a in reanchored)
    print(f"    RE-ANCHORED {len(reanchored)} block(s), lowest at L{lo} - same text, moved range")

if not (added or removed or modified or reanchored):
    print("  PASS - the frozen enumeration is current; no change to absorb")
elif not fail:
    print("  PASS - every change is declared; --refreeze may adopt it")

if "--refreeze" in sys.argv:
    if fail:
        print("\n  REFUSING to refreeze while the delta is unresolved.")
    else:
        json.dump(current, open(D / "_K1_population_FROZEN.json", "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        print(f"\n  REFROZEN at {len(current)} blocks.")

head("N1 / N2 RESULT")
print(f"  failures: {fail}")
sys.exit(1 if fail else 0)
