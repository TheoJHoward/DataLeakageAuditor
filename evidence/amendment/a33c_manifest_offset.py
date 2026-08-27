"""A33c -- HOW FAR DOES BLOCK_MANIFEST'S OFFSET REACH? Read-only.

A33 found §AB's and §AC's declared ranges eight lines early and recorded it as a
two-block defect. That was too narrow. Entry 23 declares SC-12(w)'s limb at
1137-1173, and its true extent is 1145-1181 -- ALSO eight early. A32's
presentation used 1145-1181 for the limb, so the limb LOOKED correct when checked
against A32 and was never checked against the manifest.

So the question is not "which two rows are wrong" but "WHERE DOES THE SHIFT
START". If eight lines were inserted into SSF after the manifest was written,
every row below the insertion is off by eight and every row above it is right.
That boundary is a fact about the file and is derivable, so it is derived rather
than estimated from three samples.

THE TEST IS STRUCTURAL, NOT TEXTUAL. For each declared range the script asks
whether SSF's line `first` begins a structure -- a blockquote line, a heading, a
table row, a fence -- and whether line `first + 8` does. A row is classified:

    AT      only the declared start is a boundary          -> range is correct
    OFF+8   only `first + 8` is a boundary                 -> range is eight early
    BOTH    both are boundaries                            -> undecidable here
    NEITHER neither is                                     -> reported, not guessed

A row that cannot be decided is REPORTED AS UNDECIDABLE. Forcing every row into
one of the two answers would manufacture a clean boundary out of ambiguity, which
is the failure this whole exercise exists to catch.

    usage: a33c_manifest_offset.py
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
MAN = REPO / "evidence/amendment/BLOCK_MANIFEST.md"
APPROVED_SSF = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"
SHIFT = 8

ssf_sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if ssf_sha != APPROVED_SSF:
    sys.exit("HALT: SSF is %s, not the approved %s" % (ssf_sha[:16], APPROVED_SSF[:16]))
print("SSF at the approved hash %s, %d lines"
      % (ssf_sha[:16], SSF.read_text(encoding="utf-8").count("\n")))

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def line(n):
    """SSF line n, 1-indexed. Out of range is empty, never an exception -- a row
    pointing past the file is a finding, not a crash."""
    return ssf[n - 1] if 1 <= n <= len(ssf) else ""


def is_boundary(n):
    """Does SSF line n BEGIN a structure? A block starts at a heading, a
    blockquote, a table row or a fence -- and the line before it must not be the
    same kind of thing, or we are mid-structure rather than at its start."""
    cur, prev = line(n).lstrip(), line(n - 1).lstrip()
    if not cur:
        return False
    kinds = (("#", "#"), (">", ">"), ("|", "|"), ("```", "```"))
    for mark, _ in kinds:
        if cur.startswith(mark):
            return not prev.startswith(mark)
    if cur.startswith("**") and not prev:
        return True                      # a bolded block opener after a blank
    return False


# Rows: | <id> | <first>-<last> | <description> | <hunk> |   (en-dash or hyphen)
ROW = re.compile(r"^\|\s*([0-9]+[a-z]?)\s*\|\s*(\d+)\s*[–—-]\s*(\d+)\s*\|\s*(.*?)\s*\|")
rows = []
for raw in MAN.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"):
    m = ROW.match(raw)
    if m:
        rows.append((m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)))

print("parsed %d §A rows carrying a line range" % len(rows))
if not rows:
    sys.exit("HALT: no rows parsed -- the table's shape changed and this script "
             "would otherwise report a clean sweep over nothing")
print()

tally = {"AT": [], "OFF+8": [], "BOTH": [], "NEITHER": []}
for rid, first, last, desc in rows:
    at, off = is_boundary(first), is_boundary(first + SHIFT)
    verdict = ("AT" if at and not off else "OFF+8" if off and not at
               else "BOTH" if at and off else "NEITHER")
    tally[verdict].append((rid, first, last, desc))

for v in ("AT", "OFF+8", "BOTH", "NEITHER"):
    print("%-8s %2d row(s)" % (v, len(tally[v])))
print()

decided = tally["AT"] + tally["OFF+8"]
if decided:
    hi_at = max([r[1] for r in tally["AT"]], default=None)
    lo_off = min([r[1] for r in tally["OFF+8"]], default=None)
    print("highest DECLARED start still correct   : %s" % hi_at)
    print("lowest  DECLARED start eight lines out : %s" % lo_off)
    if hi_at is not None and lo_off is not None:
        if hi_at < lo_off:
            print("=> the shift begins between SSF l.%d and l.%d: rows above are "
                  "right, rows below are eight early" % (hi_at, lo_off))
        else:
            print("=> NO CLEAN BOUNDARY: correct and shifted rows INTERLEAVE "
                  "(%d >= %d). The manifest is not uniformly stale; rows must be "
                  "taken one at a time." % (hi_at, lo_off))
print()

print("=== every row, in table order ===")
for v_name, group in (("AT", tally["AT"]), ("OFF+8", tally["OFF+8"]),
                      ("BOTH", tally["BOTH"]), ("NEITHER", tally["NEITHER"])):
    for rid, first, last, desc in group:
        print("  %-7s row %-4s %4d-%-4d  %s" % (v_name, rid, first, last, desc[:56]))

print()
print("NOTE: 'BOTH' and 'NEITHER' are NOT counted as evidence either way. A row "
      "whose start is ambiguous cannot testify to the boundary, and pretending "
      "otherwise would produce a tidy answer the file does not support.")
