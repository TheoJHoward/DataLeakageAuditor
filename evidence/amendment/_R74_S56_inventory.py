#!/usr/bin/env python3
"""§56.4 — is each scratchpad file's CONTENT already in the repository, in full?

By content hash, not by name. A file whose bytes appear nowhere in the repo is
content that exists only in a destructible temp directory.

Scripts, caches and build intermediates are separated from RECORDS: a .py that
applied an edit is reproducible from its result; a .md recording a ruling is not.
"""
import hashlib, pathlib, collections

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

def digests(root, skip_git=True):
    out = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        parts = p.relative_to(root).parts
        if skip_git and parts and parts[0] == ".git":
            continue
        if "__pycache__" in parts:
            continue
        try:
            out.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), []).append(p)
        except OSError:
            pass
    return out

repo = digests(REPO)
scr = digests(SCR)

RECORD_EXT = {".md", ".json", ".txt", ".csv", ".toml", ".asc", ".ots"}
missing = collections.defaultdict(list)
present = 0
for h, paths in scr.items():
    p = paths[0]
    rel = p.relative_to(SCR).as_posix()
    if h in repo:
        present += 1
        continue
    kind = "RECORD" if p.suffix.lower() in RECORD_EXT else "script/build"
    missing[kind].append((p.stat().st_size, rel))

print("scratchpad distinct contents : %d" % len(scr))
print("  already in the repo byte-for-byte : %d" % present)
print("  NOT in the repo                   : %d" % sum(len(v) for v in missing.values()))
for kind in ("RECORD", "script/build"):
    print("      %-14s %d" % (kind, len(missing.get(kind, []))))

print("\n=== RECORDS NOT IN THE REPOSITORY (top 40 by size) ===")
for size, rel in sorted(missing.get("RECORD", []), reverse=True)[:40]:
    print("  %9d  %s" % (size, rel))

print("\n=== record-bearing DIRECTORIES with content not in the repo ===")
bydir = collections.Counter(rel.rsplit("/", 1)[0] if "/" in rel else "(root)"
                            for _, rel in missing.get("RECORD", []))
for d, n in sorted(bydir.items()):
    print("  %-40s %d" % (d, n))
