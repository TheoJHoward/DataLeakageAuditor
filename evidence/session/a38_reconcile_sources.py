"""A38 -- do the held-banking lines survive in the committed record? READ-ONLY.

R144 §3/A38 reconciles every source of `evidence/session/ROUND_STATE.md`. The
question that decides the shape of the work is narrow: does `stash@{0}` carry any
line that the committed file does not?

THE STASH IS READ VIA `git show`, NEVER APPLIED. R144 §6 makes applying, popping
or dropping it a halt; the branch ref is the only write. This script runs
`git show` and nothing else.

WHY LINE-SET CONTAINMENT AND NOT A DIFF. `git diff` between the stash and main
would report thousands of changes, because the committed file has moved on
through fifteen commits -- the header was rewritten every round by design. That
noise would bury the only thing at issue: whether any HELD line is MISSING.
Presence of each added line is the question, so presence is what is tested.

BLANK AND RULE LINES ARE EXCLUDED FROM THE VERDICT. A file full of blank lines
and `---` would otherwise score as fully contained. They are counted separately
so the number that matters is the number of lines that carry text.

    usage: a38_reconcile_sources.py
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
REL = "evidence/session/ROUND_STATE.md"
COMMITTED = REPO / REL


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=REPO, capture_output=True)
    if r.returncode:
        sys.exit("HALT: git %s failed: %s" % (" ".join(args), r.stderr.decode()[:200]))
    return r.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n")


stash_text = git("show", "stash@{0}:" + REL)
base_text = git("show", "d39643e:" + REL)
live_text = COMMITTED.read_text(encoding="utf-8").replace("\r\n", "\n")

print("stash@{0}   %s  %d lines" % (hashlib.sha256(stash_text.encode()).hexdigest()[:16],
                                    stash_text.count("\n")))
print("d39643e     %s  %d lines" % (hashlib.sha256(base_text.encode()).hexdigest()[:16],
                                    base_text.count("\n")))
print("committed   %s  %d lines" % (hashlib.sha256(COMMITTED.read_bytes()).hexdigest()[:16],
                                    live_text.count("\n")))
print()

base = base_text.split("\n")
stash = stash_text.split("\n")
live = set(l.strip() for l in live_text.split("\n"))

# The lines the stash ADDS over its own base -- the held banking proper.
base_set = set(base)
added = [l for l in stash if l not in base_set]
substantive = [l for l in added if l.strip() and l.strip() != "---"]
print("stash adds %d line(s) over d39643e; %d carry text"
      % (len(added), len(substantive)))
print()

missing = [l for l in substantive if l.strip() not in live]
print("=== VERDICT ===")
print("  held lines carrying text      : %d" % len(substantive))
print("  present in the committed file : %d" % (len(substantive) - len(missing)))
print("  ** MISSING **                 : %d" % len(missing))
print()

if missing:
    print("=== lines in the held banking that the committed record does NOT carry ===")
    for l in missing[:60]:
        print("  %s" % l[:112])
    if len(missing) > 60:
        print("  ... and %d more" % (len(missing) - 60))
    print()
    print("A38: the stash is NOT redundant. Its content must be consolidated into "
          "the committed record before the backup ref can be retired.")
    sys.exit(2)

print("A38: every held line carrying text is already in the committed record. The "
      "stash is REDUNDANT -- but it is NOT dropped here: R144 §6 reserves that to "
      "A15, and the backup ref stays until then.")
