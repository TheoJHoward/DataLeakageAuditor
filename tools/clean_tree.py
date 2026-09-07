#!/usr/bin/env python3
"""Certification runs against the state that ships, not a state you have left.

    $ py -3.12 tools/clean_tree.py

Exit 0 when the working tree is clean, 1 otherwise. Run FIRST in the
certification sequence, because every instrument after it is measuring a tree,
and which tree it measured is the whole question.

**THE RULE THIS ENFORCES.** *A verification is a claim about a specific tree
state. Any edit after it, in the same round, voids it.* "I verified X" means
nothing unless X is the state that shipped.

**IT IS HALF THIS SESSION'S DEFECTS IN ONE SENTENCE**, and each was found
separately before the shape was named:

    the manifest hash          attested, then the file was edited after
    a recorded suite count     measured before three files joined the commit
    the whole-frame guard      owed after a probe-path file moved beneath it
    the interpreter pin        recorded after the figures it was meant to frame
    R245's count repair        verified, then broken by the paragraph
                               documenting it, and never re-verified

Every one is *evidence measured at state A, artifact shipped at state B, A ≠ B.*

**WHY A SIBLING AND NOT A CHECK IN THE GATE.** R243: `check_registration.py` is
verdict-frozen against the tagged instrument, differences are ruled against a
ceiling of four, and an addition does not need a slot when it can stand beside.
Measured before writing this: the gate has no dirty-tree check of any kind.

**WHAT IT DOES NOT CLAIM.** A clean tree says the instruments measured the
committed state. It says nothing about whether they measured it *correctly*, and
nothing about work that never reached the tree at all. It removes one specific
way of being wrong.

**`.claude/` IS EXCLUDED**, and that is a durable rule rather than a
convenience: it is never committed and never read, so its presence is not
uncommitted work — it is not work.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]

#: Paths whose presence is not uncommitted work.
IGNORED_PREFIXES = (".claude/",)


class TreeUnreadable(Exception):
    """git could not be asked, so nothing here is a result."""


def entries(repo: pathlib.Path = None) -> list:
    """Porcelain lines that represent uncommitted work."""
    root = repo or REPO
    r = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise TreeUnreadable(
            "`git status --porcelain` exited %d, so the tree's state is "
            "unknown and this reports nothing rather than reporting clean: %s"
            % (r.returncode, r.stderr[:200]))
    out = []
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        if any(path.startswith(p) for p in IGNORED_PREFIXES):
            continue
        out.append(line.rstrip())
    return out


def main(argv=None) -> int:
    try:
        dirty = entries()
    except TreeUnreadable as e:
        print("UNREADABLE: %s" % e)
        return 1

    print("WORKING TREE STATE -- %s" % REPO)
    if not dirty:
        print("  clean. Evidence produced now describes the committed state.")
        return 0
    print("  %d uncommitted entr%s:" % (len(dirty),
                                        "y" if len(dirty) == 1 else "ies"))
    for line in dirty[:20]:
        print("    %s" % line)
    if len(dirty) > 20:
        print("    ... and %d more" % (len(dirty) - 20))
    print()
    print("DIRTY. Certification against this tree would attest a state that is "
          "not the one shipping: the suite, the gate, the guard and the "
          "manifest would all describe a mixture of committed and uncommitted "
          "work, and the commit would carry evidence measured elsewhere.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
