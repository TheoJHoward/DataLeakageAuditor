"""A34b -- repair a collision A34 itself created. Inside the same correction class.

A34 was careful not to quote §AB's headline in the four block citations, because
D8 resolves an anchor only when it occurs EXACTLY ONCE and five copies would have
destroyed the uniqueness that makes the citation work. It then quoted SC-12(w)'s
limb heading verbatim in the provenance note and did precisely that to the limb:

    "(w) ENTRY CONDITION FOR" went from 1 occurrence to 2.

The same trap, avoided in one place and walked into two paragraphs later. The
guard A34 carried checked only §AB's anchor; it did not check the limb's, so
nothing failed. **A guard that pins one invariant does not pin its neighbour.**

THE FIX uses the form A34 should have used throughout: name the block by SECTION
plus a DESCRIPTOR THAT DOES NOT COLLIDE. `entry-condition limb` occurs zero times
in the file; the limb sits in §10.2 (heading l.1797). The heading itself is left
as the file's only copy.

    usage: a34b_fix_collision.py
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
NEW = "as SC-12(w)'s entry-condition limb in §10.2"
LIMB_ANCHOR = "(w) ENTRY CONDITION FOR"

raw = PREREG.read_bytes()
if raw.count(b"\r\n"):
    sys.exit("HALT: PREREG.md carries CRLF")
before = hashlib.sha256(raw).hexdigest()
print("PREREG.md before: %s  (%d lines)" % (before[:16], raw.count(b"\n")))
t = raw.decode("utf-8")

if NEW in t:
    print("ALREADY APPLIED. Nothing written.")
    sys.exit(0)

n0 = t.count(LIMB_ANCHOR)
print("'%s' occurrences before: %d" % (LIMB_ANCHOR, n0))
if n0 != 2:
    sys.exit("HALT: expected the collision (2 occurrences), found %d. This "
             "script repairs a specific defect and must not run against a file "
             "in another state." % n0)

# Located between anchors, never respelled: the span carries an em-dash-free but
# backticked identifier and a line break, and a patch that spells the text it
# edits can misspell it.
A, B = "is in this file below, headed", "COVERAGE STATE**."
ia, ib = t.find(A), t.find(B)
if ia < 0 or ib < 0 or ib <= ia:
    sys.exit("HALT: the note's anchors did not locate cleanly")
old = t[ia:ib + len(B)]
t = t[:ia] + "is in this file below, " + NEW + "." + t[ib + len(B):]
print("replaced %d chars: %r" % (len(old), old[:70]))

n1 = t.count(LIMB_ANCHOR)
print("'%s' occurrences after : %d" % (LIMB_ANCHOR, n1))
if n1 != 1:
    sys.exit("HALT: the limb's heading is still not unique (%d)" % n1)

# BOTH anchors are asserted now, not just the one this script touched -- the
# defect being repaired is precisely that only one was checked.
ab = t.count("RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT")
print("§AB's anchor occurrences: %d" % ab)
if ab != 1:
    sys.exit("HALT: §AB's anchor is no longer unique (%d)" % ab)

o = t.split("\n")
for k, l in enumerate(o):
    if l.strip() == "---" and k and o[k - 1].strip() and not o[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, o[k - 1][:60]))
print("structure: no rule flush against text")

PREREG.write_bytes(t.encode("utf-8"))
b = PREREG.read_bytes()
print()
print("PREREG.md after : %s  (%d lines, %d CRLF / %d LF)"
      % (hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
         b.count(b"\r\n"), b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
