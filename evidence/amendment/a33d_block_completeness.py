"""A33d -- IS ANY APPLIED BLOCK TRUNCATED? Read-only, whole-block, every row.

A33 found §AB and §AC applied eight lines short because `BLOCK_MANIFEST.md`'s
declared ranges end before the blockquote does. A33c then showed the defect is not
confined to those two: SEVEN decidable rows are eight lines early, including row
28 -- SC-13a, a fifty-nine-line clause that WAS applied to `PREREG.md`.

So the question this script asks is the one that actually matters before a
signature: FOR EVERY BLOCK THE MANIFEST DECLARES, IS THE WHOLE OF IT IN
`PREREG.md`, OR ONLY A PREFIX?

WHY THE GATE DOES NOT ALREADY ANSWER THIS. `block_reachability` asks whether a
block is REACHABLE -- whether a distinctive line of it can be found. A block
truncated at its tail still has its distinctive opening line, so it passes.
Reachability and completeness are different questions, and only the first was
being asked. This is the same shape as the defect it is looking for: an
instrument that confirms presence cannot testify to extent.

METHOD. For each row, the block's TRUE extent is derived from the structure's own
delimiters -- the contiguous blockquote, heading-led run, or table -- starting
from whichever of `first` or `first + 8` actually begins a structure (A33c showed
both occur). The full extent is then sought in `PREREG.md` as a CONTIGUOUS run.

    COMPLETE    every line present, contiguous
    TRUNCATED   a proper prefix is present and the tail is not  <- the defect
    ABSENT      the opening line is not in PREREG.md at all
    APPARATUS   the block is drafting apparatus and is not meant to be applied

ABSENT IS NOT REPORTED AS A FAILURE. Most rows are markers, citations and
insertion apparatus that were never meant to reach `PREREG.md` -- SSF §0.2 admits
only THE CLAUSE, SUPERSESSION MARKER and INSERTION TEXT. Only TRUNCATED is a
defect, because a truncated block is registered text that LOOKS applied.

    usage: a33d_block_completeness.py
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
PREREG = REPO / "PREREG.md"
APPROVED_SSF = "32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc"

ssf_sha = hashlib.sha256(SSF.read_bytes()).hexdigest()
if ssf_sha != APPROVED_SSF:
    sys.exit("HALT: SSF is %s, not the approved %s" % (ssf_sha[:16], APPROVED_SSF[:16]))

ssf = SSF.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
prereg = PREREG.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
print("SSF %s (%d lines) | PREREG.md %s (%d lines)"
      % (ssf_sha[:16], len(ssf) - 1,
         hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16], len(prereg) - 1))
print()

MARKS = ("#", ">", "|", "```")


def opener(n):
    """The structural mark line n opens with, or None if it opens nothing."""
    cur = ssf[n - 1].lstrip() if 1 <= n <= len(ssf) else ""
    prev = ssf[n - 2].lstrip() if 2 <= n <= len(ssf) else ""
    for m in MARKS:
        if cur.startswith(m):
            return None if prev.startswith(m) else m
    return None


def extent(first):
    """The contiguous run of the structure beginning at `first`."""
    m = opener(first)
    if m is None:
        return None
    i = first
    while i <= len(ssf) and ssf[i - 1].lstrip().startswith(m):
        i += 1
    return ssf[first - 1:i - 1]


ROW = re.compile(r"^\|\s*([0-9]+[a-z]?)\s*\|\s*(\d+)\s*[–—-]\s*(\d+)\s*\|\s*(.*?)\s*\|")
rows = []
for raw in MAN.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"):
    m = ROW.match(raw)
    if m:
        rows.append((m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)))
if not rows:
    sys.exit("HALT: no §A rows parsed; a clean sweep over nothing is not a result")
print("population: %d §A rows carrying a line range" % len(rows))
print()

results = {"COMPLETE": [], "TRUNCATED": [], "ABSENT": [], "NO-STRUCTURE": []}
for rid, first, last, desc in rows:
    body = extent(first) or extent(first + 8)
    used = first if extent(first) else first + 8
    if not body:
        results["NO-STRUCTURE"].append((rid, first, desc, 0, 0))
        continue
    head = body[0]
    hits = [i for i, l in enumerate(prereg) if l == head]
    if not hits:
        results["ABSENT"].append((rid, used, desc, len(body), 0))
        continue
    best = 0
    for h in hits:
        k = 0
        while k < len(body) and h + k < len(prereg) and prereg[h + k] == body[k]:
            k += 1
        best = max(best, k)
    if best == len(body):
        results["COMPLETE"].append((rid, used, desc, len(body), best))
    else:
        results["TRUNCATED"].append((rid, used, desc, len(body), best))

for k in ("TRUNCATED", "COMPLETE", "ABSENT", "NO-STRUCTURE"):
    print("%-13s %2d row(s)" % (k, len(results[k])))
print()

if results["TRUNCATED"]:
    print("=== ** TRUNCATED -- registered text that LOOKS applied ** ===")
    for rid, first, desc, n, got in results["TRUNCATED"]:
        print("  row %-4s SSF l.%-5d %2d of %2d lines present (%d MISSING)  %s"
              % (rid, first, got, n, n - got, desc[:52]))
        body = extent(first) or extent(first + 8)
        print("      first missing line: %s" % (body[got][:96] if got < len(body) else "?"))
    print()

print("=== COMPLETE ===")
for rid, first, desc, n, _ in results["COMPLETE"]:
    print("  row %-4s SSF l.%-5d %2d lines, all present  %s" % (rid, first, n, desc[:52]))
print()
print("=== ABSENT (expected for apparatus: markers, citations, INSERT blocks) ===")
for rid, first, desc, n, _ in results["ABSENT"]:
    print("  row %-4s SSF l.%-5d %2d lines  %s" % (rid, first, n, desc[:56]))
if results["NO-STRUCTURE"]:
    print()
    print("=== NO STRUCTURE AT EITHER OFFSET (reported, not guessed) ===")
    for rid, first, desc, _, _ in results["NO-STRUCTURE"]:
        print("  row %-4s SSF l.%-5d  %s" % (rid, first, desc[:60]))

print()
if results["TRUNCATED"]:
    sys.exit("HALT: %d applied block(s) are truncated in PREREG.md"
             % len(results["TRUNCATED"]))
print("RESULT: no applied block is truncated. Every block whose opening line is "
      "in PREREG.md is present in full.")
