#!/usr/bin/env python3
"""A5 — grow the FILES authority from six paths to the twenty item 8 requires.

FILES is the single authority for the set: every gate in the ceremony iterates
it and no gate reads a numeral. So this line is the only place the set changes,
and everything that restates it is checked against this line rather than edited
alongside it.

The ceremony's own §3.2 records that this is the sanctioned shape of the change
and that it is reversible: "Adding a file later is a Class B change - a parameter
of a locked procedure."

The order is deliberate and is NOT alphabetical: the five the prereg-v30 tag
carried come first, in the v30 order, so the v30 five-line block stays a verbatim
prefix and no v30-era verification instruction is invalidated. The declaration
follows, then the rest of item 1's named paths, then tests/registration/ expanded,
then the files SC-8(f) reaches.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
CER = REPO / "evidence/ceremony/CEREMONY_COMMANDS.md"

FILES = [
    # the prereg-v30 five, in the v30 order -- kept first as a verbatim prefix
    "PREREG.md", "DESIGN.md", "HISTORY.md",
    "tools/check_registration.py", "protocol/runtime_reference.py",
    # limb 2: the document the amendment registers under §0.2.1
    "AVAILABILITY_DECLARATION.md",
    # limb 1: the rest of what §11 item 1 names
    "DEVIATIONS.md", "PARKING_LOT.md", "VALIDATED_CONFIG.toml",
    # limb 1: tests/registration/ is a DIRECTORY; a directory name pins no
    # content, and item 8 speaks of a registered FILE
    "tests/registration/EXPECTED_OUTPUTS.md",
    "tests/registration/conftest.py",
    "tests/registration/generate_expected_outputs.py",
    "tests/registration/test_checker.py",
    "tests/registration/test_expected_outputs.py",
    "tests/registration/test_invariants.py",
    "tests/registration/test_traces.py",
    "tests/registration/traces.py",
    # limb 3: files the freeze ranges over that are not elements inside the
    # declaration -- the gate input SC-4(k2) reads, and the scoring key
    "evidence/fixture_spike/f3/fixture_manifest_DRAFT.json",
    "evidence/fixture_spike/n1/declared_map.csv",
    # the code §D.1 pins as the manifest's meaning
    "evidence/fixture_spike/f3/phase7_l2_sim.py",
]

missing = [f for f in FILES if not (REPO / f).exists()]
if missing:
    sys.exit("HALT: not in the tree: %s" % ", ".join(missing))
if len(set(FILES)) != len(FILES):
    sys.exit("HALT: duplicate path in FILES")

OLD_HEAD = "## 3.2 The FIXED SIX. The list is closed."
NEW_HEAD = "## 3.2 The FIXED SET. The list is closed."

OLD_BLOCK = (
    "# The six files whose hashes the prereg-v30a tag message carries.\n"
    "# FIXED. Not derived from `git status`, not filtered, not extended, not shortened.\n"
    'FILES="PREREG.md DESIGN.md HISTORY.md tools/check_registration.py '
    'protocol/runtime_reference.py AVAILABILITY_DECLARATION.md"')

NEW_BLOCK = (
    "# The files whose hashes the prereg-v30a tag message carries, as PREREG.md\n"
    "# \u00a711 item 8 defines the set: item 1's named paths (tests/registration/\n"
    "# expanded to its files), the document \u00a70.2.1 registers, and the files\n"
    "# SC-8(f) reaches. FIXED. Not derived from `git status`, not filtered, not\n"
    "# extended, not shortened.\n"
    "#\n"
    "# ORDER IS NOT ALPHABETICAL AND MUST NOT BE MADE SO: the prereg-v30 five come\n"
    "# first in the v30 order, so the v30 block stays a verbatim prefix of this one\n"
    "# and no v30-era verification instruction is invalidated.\n"
    "#\n"
    "# The COUNT is read from this line. No clause anywhere states it as a literal.\n"
    'FILES="' + " ".join(FILES) + '"')

raw = CER.read_bytes()
if raw.count(b"\r\n") != raw.count(b"\n"):
    sys.exit("HALT: CEREMONY_COMMANDS.md is not uniformly CRLF")
text = raw.decode("utf-8").replace("\r\n", "\n")

for old, new, what in ((OLD_HEAD, NEW_HEAD, "\u00a73.2 heading"),
                       (OLD_BLOCK, NEW_BLOCK, "FILES block")):
    if text.count(old) != 1:
        sys.exit("HALT: %s occurs %d times, expected 1" % (what, text.count(old)))
    text = text.replace(old, new, 1)

CER.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
print("FILES grown to %d paths" % len(FILES))
for f in FILES:
    print("   %s" % f)
