#!/usr/bin/env python3
"""A4(c) — add the phase7_l2_sim.py line to evidence/MANIFEST.sha256.

The hash is COMPUTED from the file on disk, never transcribed. The line is placed
beside its sibling in the same f3 directory rather than appended, because the
manifest is grouped by directory and an appended line would sit away from the
group a reader scans.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
MAN = REPO / "evidence/MANIFEST.sha256"
REL = "fixture_spike/f3/phase7_l2_sim.py"
TARGET = REPO / "evidence" / REL
SIBLING = "fixture_spike/f3/fixture_manifest_DRAFT.json"

digest = hashlib.sha256(TARGET.read_bytes()).hexdigest()
text = MAN.read_text(encoding="utf-8")
lines = text.split("\n")

if any(line.endswith("  " + REL) for line in lines):
    sys.exit("HALT: %s already has a manifest line" % REL)

anchor = [i for i, line in enumerate(lines) if line.endswith("  " + SIBLING)]
if len(anchor) != 1:
    sys.exit("HALT: expected exactly one sibling line for %s, found %d"
             % (SIBLING, len(anchor)))

# Same-directory ordering: the .json sorts before the .py, so the new line
# follows its sibling.
lines.insert(anchor[0] + 1, "%s  %s" % (digest, REL))
MAN.write_text("\n".join(lines), encoding="utf-8", newline="\n")

entries = [l for l in lines if l and not l.startswith("#") and "  " in l]
print("manifest: added %s" % REL)
print("  sha256 %s (computed from disk)" % digest)
print("  entries: %d" % len(entries))
