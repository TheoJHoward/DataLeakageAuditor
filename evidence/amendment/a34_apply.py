"""A34 -- the correction class. R146 §1.2 rules the citations anchor-keyed.

FIVE SITES, all inside A30's approved class: each makes a false claim true and
changes no substantive rule.

  4x  the block citations -- they name "the amendments block", a container that
      was never created and never will be.
  1x  A30's provenance note -- TRUE when written, falsified by hunk 3 landing.

THE CITATION FORM, AND WHY NOT THE OBVIOUS ONE. The natural anchor is §AB's own
headline, "RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT". Quoting it in four
citations would put the phrase in the file FIVE times -- and D8 resolves an
anchor only when it occurs EXACTLY ONCE. The obvious fix would have destroyed
the very uniqueness that makes the citation resolvable.

So the block is named by SECTION plus a DESCRIPTOR THAT DOES NOT COLLIDE:

    "the v30a recorded-defect block in §7.2.1"

`recorded-defect` (lowercase, hyphenated) occurs zero times in the file, so it
adds no collision; §7.2.1 spans ll.1322-1454 and contains EXACTLY ONE such
block, verified before this script was written. `§AB` is not used: it is SSF's
label for the block, appears zero times in `PREREG.md`, and a label citation
would point at nothing.

SPLICED BY INDEX BETWEEN ANCHORS, NOT BY RETYPING. The provenance note contains
em-dashes and backticked identifiers; respelling it in this script is the D2.1
hazard one level up -- a patch that spells the text it edits can misspell it. The
old span is located by two short ASCII anchors and replaced wholesale.

    usage: a34_apply.py
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
PREREG = REPO / "PREREG.md"
BLOCK = "the v30a recorded-defect block in §7.2.1"
ANCHOR = "RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT"

raw = PREREG.read_bytes()
if raw.count(b"\r\n"):
    sys.exit("HALT: PREREG.md carries CRLF; this applier assumes LF")
before = hashlib.sha256(raw).hexdigest()
print("PREREG.md before: %s  (%d lines)" % (before[:16], raw.count(b"\n")))
t = raw.decode("utf-8")

if BLOCK in t:
    print("ALREADY APPLIED. Nothing written.")
    sys.exit(0)

# --- the four block citations ---------------------------------------------
CITES = [
    ("the amendments block records",
     BLOCK + " records", "l.1998 -- SC-13a(a2)'s gate"),
    ("recorded in the v30a amendments block (SC-13c(c2))",
     "recorded in " + BLOCK + " (SC-13c(c2))", "l.2002 -- the first ground"),
    # SPANS A LINE BREAK. A line-scoped replacement finds nothing here, which is
    # the same shape as the sweep's false all-clear: prose wraps, and a line is
    # not a unit of meaning. The newline and its `> ` are part of the match.
    ("recorded in the v30a\n> amendments block in terms",
     "recorded in\n> " + BLOCK + " in terms", "ll.2063-2064 -- spans a line break"),
    ("recorded in the amendments block as a duplicated-authority",
     "recorded in that block (§7.2.1) as a duplicated-authority",
     "l.2066 -- names it two lines after the full form"),
]
for old, new, why in CITES:
    n = t.count(old)
    if n != 1:
        sys.exit("HALT: %r occurs %d times, expected 1" % (old[:44], n))
    t = t.replace(old, new, 1)
    print("  cite  %-46s %s" % (why, "OK"))

# --- A30's provenance note, spliced between anchors ------------------------
A, B = "**It was not.**", "so it was never offered for approval."
ia, ib = t.find(A), t.find(B)
if ia < 0 or ib < 0 or ib <= ia:
    sys.exit("HALT: the provenance note's anchors did not locate cleanly")
NOTE = (
    "**It was not — and it no longer needs to be.** SC-12(w)'s limb was applied at "
    "R142/A33\nunder its own approval and is in this file below, headed **(w) ENTRY CONDITION "
    "FOR §7.7's\n`waived` COVERAGE STATE**. The `SC-12` record's clause span in "
    "`SCHEMA_SET_FINAL.md` stops short\nof it, which is why it was not offered alongside that "
    "record; it was approved separately.")
old_note = t[ia:ib + len(B)]
t = t[:ia] + NOTE + t[ib + len(B):]
print("  note  l.1533 -- %d chars replaced by %d" % (len(old_note), len(NOTE)))

o = t.split("\n")

# --- the anchor must STILL be unique ---------------------------------------
hits = [i for i, l in enumerate(o, 1) if ANCHOR in l]
if len(hits) != 1:
    sys.exit("HALT: %r now occurs %d times -- the citations destroyed the "
             "anchor's uniqueness, which is the whole point of anchor-keying"
             % (ANCHOR, len(hits)))
print("anchor %r still unique, at l.%d" % (ANCHOR[:28] + "...", hits[0]))

# --- nothing may still name the container ----------------------------------
left = t.count("amendments block")
fenced = 0
inf = False
for l in o:
    if l.lstrip().startswith("```"):
        inf = not inf
        continue
    if inf and "amendments block" in l:
        fenced += 1
print("'amendments block' remaining: %d (of which inside a fence: %d)" % (left, fenced))
if left != fenced:
    sys.exit("HALT: %d operative mention(s) of the container remain" % (left - fenced))

# --- structure, BEFORE the write -------------------------------------------
for k, l in enumerate(o):
    if l.strip() == "---" and k and o[k - 1].strip() and not o[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, o[k - 1][:60]))
for k, l in enumerate(o):
    if 1990 < k < 2075 and l and not l.startswith(">") and l.strip() and not l.startswith("#"):
        pass                       # the region is blockquote; stray text would show below
print("structure: no rule flush against text")

PREREG.write_bytes(t.encode("utf-8"))
b = PREREG.read_bytes()
print()
print("PREREG.md after : %s  (%d lines, %d CRLF / %d LF)"
      % (hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
         b.count(b"\r\n"), b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
