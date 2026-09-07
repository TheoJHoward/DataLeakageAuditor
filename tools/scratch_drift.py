#!/usr/bin/env python3
"""Round work stays under the scratch subdirectory. R252 §3(c).

    $ LEAKAUDIT_WORK_ROOT=<the scratch subdir> py -3.12 tools/scratch_drift.py

Exit 0 when no round-work file sits outside the work root, 1 otherwise.

**THIS IS WHAT MAKES OPTION B SAFE.** B keeps the work root a dedicated scratch
subdirectory, so `tasks/` -- the harness's background-command logs -- falls
outside it and no frozen `_EPHEMERAL` change is needed: the ruled-difference
count stays 2 of 4 and no slot is spent. **The price is a discipline
dependency**: if round scratch is written anywhere else, it silently leaves the
reconciliation's population.

That is not hypothetical. It is exactly what happened: 49 files -- every
disclosure body from `d77.md` and every commit message from `msg2.txt` -- were
written one level above the declared root and were invisible to
`round_reconciliation` for many rounds. **B without this guard is that failure
waiting to recur**, so the discipline dependency is turned into a check rather
than a resolution.

**WHAT IT CONSIDERS OUTSIDE.** The work root's PARENT is scanned. Anything under
the work root is fine. Anything under a directory this file names as harness
infrastructure is fine -- that is what it is, not round work. Everything else is
drift, and it is reported with its path.

**HARNESS INFRASTRUCTURE IS NAMED, NOT GUESSED.** The list is short and explicit
so that adding to it is a decision somebody makes and a reader can see, rather
than a pattern that quietly grows to cover whatever appeared.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import os
import pathlib
import sys

WORK_ROOT_ENV = "LEAKAUDIT_WORK_ROOT"

#: Directories beside the work root that the harness owns. Not round work.
HARNESS_DIRS = ("tasks",)


class DriftUnreadable(Exception):
    """The work root could not be resolved, so nothing here is a result."""


def resolve_root(env=None) -> pathlib.Path:
    raw = (env if env is not None else os.environ.get(WORK_ROOT_ENV))
    if not raw:
        raise DriftUnreadable(
            "%s is unset, so there is no scratch subdirectory to check drift "
            "against. This reports nothing rather than reporting no drift."
            % WORK_ROOT_ENV)
    p = pathlib.Path(raw)
    if not p.is_dir():
        raise DriftUnreadable("%s names %s, which is not a directory"
                              % (WORK_ROOT_ENV, p))
    return p


def drifted(root: pathlib.Path) -> list:
    """Files beside the work root that are neither under it nor harness-owned."""
    parent = root.parent
    out = []
    for p in sorted(parent.rglob("*")):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(parent)
        except ValueError:
            continue
        first = rel.parts[0] if rel.parts else ""
        if first == root.name or first in HARNESS_DIRS:
            continue
        out.append(rel.as_posix())
    return out


def main(argv=None) -> int:
    try:
        root = resolve_root()
    except DriftUnreadable as e:
        print("UNREADABLE: %s" % e)
        return 1

    stray = drifted(root)
    print("SCRATCH DRIFT -- round work outside the work root")
    print("  work root  : %s" % root)
    print("  scanned    : %s" % root.parent)
    print("  harness-owned, not round work: %s" % ", ".join(HARNESS_DIRS))
    print()
    if not stray:
        print("NO DRIFT. Every round-work file is under the work root, so the "
              "reconciliation's population is the round's work.")
        return 0
    print("  %d file(s) outside the work root:" % len(stray))
    for rel in stray[:20]:
        print("    %s" % rel)
    if len(stray) > 20:
        print("    ... and %d more" % (len(stray) - 20))
    print()
    print("DRIFT. These are round work sitting outside the reconciliation's "
          "population, so `round_reconciliation` cannot see them -- which is "
          "how 49 files went unreconciled for many rounds. Move them under the "
          "work root, or name their directory as harness infrastructure here "
          "with a reason.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
