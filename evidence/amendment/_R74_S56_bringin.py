#!/usr/bin/env python3
"""§56.4 — bring the not-in-repo RECORDS into the repository.

NEVER overwrites an existing repo file whose bytes differ: that would destroy
repo content with a scratch copy, which is the failure mode this whole item is
about, pointed the other way. Any such collision is reported and skipped.
"""
import hashlib, pathlib, shutil

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
EV = REPO / "evidence"

EXCLUDE = {"applied", "_verify", "_verify2", "_K2_verify", "s47check",
           "_x5_truncated_original", "backup_R33", "_retired", "clone_test",
           "repo_copy", "__pycache__", "ceremony", "author_review"}
SKIP_EXT = {".py", ".sh", ".pyc", ".bak"}
BIG = 5_000_000

repo_hashes = {hashlib.sha256(p.read_bytes()).hexdigest()
               for p in REPO.rglob("*") if p.is_file() and ".git" not in p.parts}

copied, skipped_big, collisions, already = 0, 0, [], 0
for p in sorted(SCR.rglob("*")):
    if not p.is_file():
        continue
    rel = p.relative_to(SCR)
    if set(rel.parts) & EXCLUDE or p.suffix.lower() in SKIP_EXT:
        continue
    if hashlib.sha256(p.read_bytes()).hexdigest() in repo_hashes:
        already += 1
        continue
    if p.stat().st_size > BIG:
        skipped_big += 1
        continue
    # root-level session files land under evidence/session/
    dst = EV / ("session" / rel if len(rel.parts) == 1 else rel)
    if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() != \
            hashlib.sha256(p.read_bytes()).hexdigest():
        collisions.append(rel.as_posix())
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dst)
    copied += 1

print("  copied into evidence/      : %d" % copied)
print("  already present (bytes)    : %d" % already)
print("  skipped, >5 MB (group C)   : %d" % skipped_big)
print("  COLLISIONS (repo differs, NOT overwritten): %d" % len(collisions))
for c in collisions:
    print("      %s" % c)
