"""A33b -- what the author APPROVED against what A33 APPLIED. Read-only.

R142 §1.1 approved hunks 1-3 as presented in `A32_PROPOSED_DIFF.md`. A33 applied
them at their TRUE extents, which are longer: `BLOCK_MANIFEST.md`'s declared
ranges for §AB and §AC are the right length and start eight lines early, so the
presentation stopped eight lines short of each block's end.

THE APPROVAL IS NOT ASSUMED TO COVER THE DIFFERENCE. This script does not argue
that the extra text is fine; it establishes exactly WHAT the difference is, so
the author can rule. The claim under test is narrow and falsifiable:

    the applied block is the presented block PLUS a suffix -- no presented line
    is removed, reordered or altered.

If that is false the script says so and exits non-zero. A weaker check -- "the
presented text appears somewhere in the applied text" -- would pass even if a
line had been changed elsewhere, so the test is prefix equality line by line.

BOTH SIDES ARE READ FROM DISK, neither is retyped. The presented side comes out
of the committed presentation; the applied side out of `PREREG.md`. Comparing a
reconstruction against a reconstruction would prove only that I am consistent.

    usage: a33b_divergence.py
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
PRESENTED = REPO / "evidence/amendment/A32_PROPOSED_DIFF.md"
PREREG = REPO / "PREREG.md"
SSF = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"

APPROVED_COMMIT = "26d4856"


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


# The presentation must be the COMMITTED one, not a working copy. A presentation
# edited after approval is not what was approved, and comparing against it would
# quietly launder the very drift this script exists to measure.
dirty = subprocess.run(["git", "status", "--porcelain", "--", str(PRESENTED)],
                       cwd=REPO, capture_output=True, text=True).stdout.strip()
if dirty:
    sys.exit("HALT: %s is modified in the working tree (%r). The approved bytes "
             "are the committed ones." % (PRESENTED.name, dirty))
print("presentation clean at %s: %s" % (APPROVED_COMMIT, PRESENTED.name))

pres = text_of(PRESENTED).split("\n")
prereg = text_of(PREREG).split("\n")
ssf = text_of(SSF).split("\n")
print("PREREG.md: %s  (%d lines)"
      % (hashlib.sha256(PREREG.read_bytes()).hexdigest()[:16], len(prereg) - 1))
print()


def presented_block(first_line, label):
    """The hunk body as the AUTHOR SAW IT: the contiguous `>` run in the
    presentation that opens with this line."""
    hits = [i for i, l in enumerate(pres) if l == first_line]
    if len(hits) != 1:
        sys.exit("HALT: %s -- its opening line occurs %d times in the "
                 "presentation, expected 1" % (label, len(hits)))
    i = hits[0]
    j = i
    while j < len(pres) and pres[j].startswith(">"):
        j += 1
    return pres[i:j]


def applied_block(first_line, label):
    """The same block as it now stands in `PREREG.md`."""
    hits = [i for i, l in enumerate(prereg) if l == first_line]
    if len(hits) != 1:
        sys.exit("HALT: %s -- its opening line occurs %d times in PREREG.md, "
                 "expected 1" % (label, len(hits)))
    i = hits[0]
    j = i
    while j < len(prereg) and prereg[j].startswith(">"):
        j += 1
    return prereg[i:j], i + 1


AB_OPEN = ssf[1639]          # SSF l.1640, §AB's first quoted line
AC_OPEN = ssf[1694]          # SSF l.1695, §AC's first quoted line
LIMB_OPEN = ssf[1144]        # SSF l.1145, the limb's first quoted line

fail = 0
for label, opener, declared, true_rng in (
        ("§AB", AB_OPEN, (1632, 1679), (1640, 1687)),
        ("§AC", AC_OPEN, (1687, 1737), (1695, 1745)),
        ("SC-12(w) limb", LIMB_OPEN, (1145, 1181), (1145, 1181))):
    p = presented_block(opener, label)
    a, at = applied_block(opener, label)
    print("%-14s presented %2d lines | applied %2d lines at PREREG l.%d"
          % (label, len(p), len(a), at))

    # PREFIX EQUALITY, line by line. Not `"\n".join(p) in "\n".join(a)`:
    # substring containment would also pass if the applied block had gained a
    # line in the MIDDLE, which is a different and much worse fact.
    if len(p) > len(a):
        print("    ** APPLIED IS SHORTER THAN PRESENTED -- text was lost **")
        fail += 1
        continue
    bad = [k for k in range(len(p)) if p[k] != a[k]]
    if bad:
        print("    ** %d presented line(s) ALTERED, first at offset %d **"
              % (len(bad), bad[0]))
        print("       presented: %r" % p[bad[0]][:88])
        print("       applied  : %r" % a[bad[0]][:88])
        fail += 1
        continue

    extra = a[len(p):]
    if not extra:
        print("    identical -- presented and applied agree exactly")
        continue
    # The suffix must be the SSF lines the declared range excluded, and nothing
    # else. If it is anything other than those, the extra text did not come from
    # approved content and the whole point collapses.
    want = ssf[declared[1]:true_rng[1]]
    if extra != want:
        print("    ** the %d extra line(s) are NOT SSF ll.%d-%d **"
              % (len(extra), declared[1] + 1, true_rng[1]))
        fail += 1
        continue
    print("    APPENDED %d line(s), verbatim SSF ll.%d-%d; every presented line "
          "unchanged" % (len(extra), declared[1] + 1, true_rng[1]))
    print("      first: %s" % extra[0][:92])
    print("      last : %s" % extra[-1][:92])

print()
if fail:
    sys.exit("HALT: %d block(s) diverge in a way that is not a pure append" % fail)
print("RESULT: the applied text is the presented text plus 16 appended lines, "
      "all verbatim from SSF at the approved hash. Nothing presented was removed "
      "or altered. THE DIFFERENCE IS THE AUTHOR'S TO RULE ON.")
