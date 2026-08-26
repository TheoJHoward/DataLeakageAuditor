#!/usr/bin/env python3
"""Bring named instruments into evidence/amendment/ and resync the manifest.

Two jobs that must happen together and in this order: a new instrument needs a
manifest line, and every attested file whose bytes moved needs its line
recomputed. Doing either alone leaves the manifest disagreeing with the tree.

Hashes are always computed from disk. No value is ever carried in from a report.

Usage: sync.py [instrument.py ...]   (bare name, resolved in this scratchpad)

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import shutil
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
HERE = pathlib.Path(__file__).resolve().parent
MAN = REPO / "evidence/MANIFEST.sha256"
DEST = REPO / "evidence/amendment"

brought = []
for name in sys.argv[1:]:
    src = HERE / name
    if not src.exists():
        sys.exit("HALT: %s not found in %s" % (name, HERE))
    dst = DEST / ("_v30a_" + name if not name.startswith("_v30a_") else name)
    if dst.exists():
        print("already present: %s" % dst.name)
        continue
    shutil.copyfile(src, dst)
    brought.append("amendment/" + dst.name)

lines = MAN.read_bytes().decode("utf-8").split("\n")

resynced = []
for i, line in enumerate(lines):
    if not line or line.startswith("#") or "  " not in line:
        continue
    digest, rel = line.split("  ", 1)
    target = (REPO / rel[3:]) if rel.startswith("../") else (REPO / "evidence" / rel)
    if not target.exists():
        continue
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != digest:
        lines[i] = "%s  %s" % (actual, rel)
        resynced.append(rel)

if brought:
    last = max(i for i, l in enumerate(lines) if "  amendment/" in l)
    for k, rel in enumerate(brought):
        d = hashlib.sha256((REPO / "evidence" / rel).read_bytes()).hexdigest()
        lines.insert(last + 1 + k, "%s  %s" % (d, rel))

MAN.write_bytes("\n".join(lines).encode("utf-8"))

print("brought in : %s" % (", ".join(brought) or "(none)"))
print("resynced   : %d -> %s" % (len(resynced), ", ".join(resynced) or "(none)"))
print("entries    : %d"
      % len([l for l in lines if l and not l.startswith("#") and "  " in l]))
