import pathlib, re
p = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment/"
                 "_N1_N2_parity_and_growth.py")
t = p.read_text(encoding="utf-8")

OLD_CALL = 'res = subprocess.run([sys.executable, str(D / "_K1_enumerate.py")],'
NEW_CALL = 'res = subprocess.run([sys.executable, str(D / "_K1_enumerate2.py")],'
assert t.count(OLD_CALL) == 1, t.count(OLD_CALL)
t = t.replace(OLD_CALL, NEW_CALL, 1)

start = t.index('fz = {b["sha12"]: b for b in frozen}')
end = t.index('if "--refreeze" in sys.argv:')
BLOCK = '''fz = {b["sha12"]: b for b in frozen}
cu = {b["sha12"]: b for b in current}
added = [cu[k] for k in cu if k not in fz]
removed = [fz[k] for k in fz if k not in cu]
unchanged = [k for k in cu if k in fz]

# A MODIFIED block presents as removed+added. Pairing them by start line is what
# lets the freeze absorb a declared edit; without it the check crashed on the
# first real change (KeyError 'lines') and no edit could ever be adopted.
modified = []
for r in list(removed):
    a = next((x for x in added if x["lines"][0] == r["lines"][0]), None)
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

'''
t = t[:start] + BLOCK + t[end:]
p.write_text(t, encoding="utf-8")
print("N2 patched: modified-block pairing, re-anchor class, enumerate2")
