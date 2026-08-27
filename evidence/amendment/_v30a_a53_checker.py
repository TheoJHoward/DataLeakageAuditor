#!/usr/bin/env python3
"""A5.3 — the checker edits that do not depend on final line positions.

TWO EDITS, and the D8 citation registry is deliberately NOT among them: its three
line numbers must be re-derived AFTER the last declaration edit, or they drift
again before C2. That is the whole reason the ordering is stated rather than
assumed.

  1. An ephemeral entry for the licence draft in the pinned work root. It is a
     draft of a file that is in the tree on the Phase 1 branch, and Track A runs
     on the branch where that file does not exist -- so it has no content twin
     here and D10 cannot reconcile it.

  2. An ENUMERATION exemption for the declaration's limb table. §187's first
     resort -- change the content -- is available but wrong here: the table
     splits the set by which limb of item 8 admits each path, and that split IS
     the section's argument. Rewriting it into the flat set in order would
     delete the reason the enumeration is there. This is the case where the last
     resort is the right resort, and the reason recorded is that the enumeration
     is deliberately a limb breakdown rather than the set.

CRLF preserved: this file is stored uniformly CRLF.

Written with the Write tool per D2.1.
"""
import ast
import pathlib
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SRC = REPO / "tools/check_registration.py"
body = SRC.read_text(encoding="utf-8")


def sub(old, new, why):
    global body
    if body.count(old) != 1:
        sys.exit("HALT: %s -- %d occurrences, expected 1" % (why, body.count(old)))
    body = body.replace(old, new, 1)


# ---- 1. the licence draft ---------------------------------------------------
sub('    ("__pycache__", "compiled bytecode, regenerated on import"),',
    '    ("__pycache__", "compiled bytecode, regenerated on import"),\n'
    '    ("/licence/",\n'
    '     "a draft of the distribution licence. The committed LICENSE lives on the "\n'
    '     "Phase 1 branch, because the tag attests the registration and not the "\n'
    '     "distribution -- so on this branch the draft has no content twin and this "\n'
    '     "check cannot reconcile it by hash. Reproducible: it is the MIT text."),',
    "ephemeral entry for the licence draft")

# ---- 2. the limb table ------------------------------------------------------
ENUM_ENTRY = (
    "_HASH_SET_ENUM_EXEMPT = {\n"
    "    ('AVAILABILITY_DECLARATION.md',\n"
    "     '| 1 \\u2014 item 1, named individually |'): (\n"
    "        ('PREREG.md', 'DESIGN.md', 'HISTORY.md', 'DEVIATIONS.md',\n"
    "         'PARKING_LOT.md', 'VALIDATED_CONFIG.toml',\n"
    "         'tools/check_registration.py', 'protocol/runtime_reference.py'),\n"
    "        'D6 - \\u00a7D.2 enumerates the set BY LIMB, showing which limb of \\u00a711 item 8 '\n"
    "        'admits each path. That breakdown is the section argument: the set is '\n"
    "        'not a list someone chose, it is what three stated rules produce. '\n"
    "        'Flattening it into the set in order would satisfy this check and '\n"
    "        'delete the reason the enumeration is there, so the content fix is '\n"
    "        'unavailable and the exemption is the right instrument. The row is '\n"
    "        'limb 1 alone; the remaining rows carry the other limbs.'),\n")
sub("_HASH_SET_ENUM_EXEMPT = {\n", ENUM_ENTRY, "limb-table enumeration exemption")

head = subprocess.run(["git", "show", "HEAD:tools/check_registration.py"],
                      cwd=str(REPO), capture_output=True).stdout
crlf, lf = head.count(b"\r\n"), head.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: checker is MIXED at HEAD")
out = body.encode("utf-8")
if crlf:
    out = out.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
SRC.write_bytes(out)
ast.parse(SRC.read_text(encoding="utf-8"))
print("checker: ephemeral entry + limb-table exemption; %d CRLF / %d LF; parses"
      % (out.count(b"\r\n"), out.count(b"\n")))
