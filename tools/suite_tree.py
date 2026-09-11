#!/usr/bin/env python3
"""The suite records which tree it ran on; certification refuses a stale one.

    $ py -3.12 tools/suite_tree.py

Exit 0 when the recorded run describes HEAD and a clean tree, 1 otherwise.

**D-V30A-102's REMAINING HALF, AS A MECHANISM RATHER THAN AN ORDER TO REMEMBER.**
The step set puts `pytest tests` fifth, after `clean_tree.py`, and nothing made
that ordering hold: a suite run, then a commit, then certification would report
a suite result measured on a tree that is no longer the shipped one. That is the
R247 shape -- evidence measured at state A, artifact shipped at state B -- and it
had been closed everywhere except here, where it rested on somebody running the
steps in order.

So the suite writes down what it ran on, the way `wholeframe_guard.py` writes its
own timings, and a step reads it back. The knowledge moves out of the operator's
head and into a file that the next step compares against `git rev-parse HEAD`.

WHAT IS CHECKED, and each because a run can be stale in that particular way:

  THE COMMIT. The recorded hash has to be HEAD now. Commit anything after the
  suite and this refuses -- which is the known positive.

  THE CLEANLINESS AT RUN TIME. A suite that ran over uncommitted edits measured
  a tree nobody will ever ship, even if HEAD has not moved since.

  THE SCOPE. `pytest tests/phase1/test_slicing.py` records a real run of a real
  tree, and it is not the suite. Certification's claim is over the whole suite,
  so a subset run is refused by name rather than accepted because the hash
  happened to match.

WHY THE RECORD FILE ITSELF DOES NOT BREAK `clean_tree.py`. Writing it dirties the
tree, so the file is named in that tool's ignore list -- by exact path, not by
prefix, so nothing else hides behind it. Tracked rather than ignored by git,
because the point is that a reader can see which tree the shipped suite result
came from; untracking it would put the evidence back in somebody's memory.

Written with the Write tool per D2.1.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
RECORD = REPO / "tools" / "suite_tree_record.json"

#: Paths whose dirt is not the round's. `.claude/` is never committed; the
#: record is written by the run being recorded.
_NOT_DIRT = (".claude/", "tools/suite_tree_record.json")

_WHAT = ("Which tree the last `pytest tests` run measured. Written by "
         "tests/conftest.py at session finish, never by hand (R267 section "
         "1.1). `tools/suite_tree.py` refuses certification when this does not "
         "describe HEAD and a clean tree.")


def _git(*args) -> str:
    out = subprocess.run(["git", "-C", str(REPO), *args],
                         capture_output=True, text=True)
    return out.stdout.strip()


def head() -> str:
    return _git("rev-parse", "--short", "HEAD") or "?"


def dirty_paths() -> list:
    """Working-tree paths that count as dirt, in porcelain order."""
    out = []
    for line in _git("status", "--porcelain").splitlines():
        path = line[3:].strip().strip('"')
        if any(path.startswith(p) for p in _NOT_DIRT):
            continue
        out.append(path)
    return sorted(out)


def is_full_suite(args) -> bool:
    """Did this invocation cover the whole `tests` tree?

    Anything narrower is a real run of a real tree and is not the suite, so it
    is recorded honestly and refused by the check rather than quietly counted.
    """
    if not args:
        return False
    allowed = {REPO.resolve(), (REPO / "tests").resolve()}
    for a in args:
        try:
            if pathlib.Path(a).resolve() not in allowed:
                return False
        except OSError:
            return False
    return True


def record(args, exitstatus, counts=None) -> dict:
    """Write the record. Never raises into the suite -- a broken write is a
    missing record, which the check refuses; it is not a test failure."""
    import datetime
    dirt = dirty_paths()
    doc = {
        "what": _WHAT,
        "last": {
            "when": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "commit": head(),
            "clean": not dirt,
            "dirty_paths": dirt,
            "args": list(args),
            "full_suite": is_full_suite(args),
            "exitstatus": int(exitstatus),
            "counts": counts or {},
        },
    }
    RECORD.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8",
                      newline="\n")
    return doc


def check(doc=None, current=None) -> list:
    """Reasons the recorded run does not describe the shipped tree. Empty = OK."""
    if doc is None:
        try:
            doc = json.loads(RECORD.read_text(encoding="utf-8"))
        except Exception as e:                               # noqa: BLE001
            return ["no usable suite record at %s (%s). Run the suite."
                    % (RECORD.relative_to(REPO).as_posix(), e)]
    last = doc.get("last") or {}
    if not last:
        return ["the suite record carries no run. Run the suite."]
    now = head() if current is None else current
    out = []
    if last.get("commit") != now:
        out.append("the suite ran on %s and HEAD is %s -- the suite result "
                   "describes a tree that is not the one being certified. "
                   "Re-run `py -3.12 -m pytest tests`."
                   % (last.get("commit"), now))
    if not last.get("clean", False):
        out.append("the suite ran over a DIRTY tree (%s), so it measured a "
                   "state nobody ships: %s"
                   % (len(last.get("dirty_paths") or []),
                      ", ".join((last.get("dirty_paths") or [])[:6]) or "?"))
    if not last.get("full_suite", False):
        out.append("the recorded run was not the whole suite; its arguments "
                   "were %r. Certification's claim is over `pytest tests`."
                   % (last.get("args"),))
    return out


def main(argv=None) -> int:
    print("SUITE TREE RECORD -- %s" % RECORD.relative_to(REPO).as_posix())
    try:
        doc = json.loads(RECORD.read_text(encoding="utf-8"))
        last = doc.get("last") or {}
        print("  recorded : %s on %s, clean=%s, args=%r"
              % (last.get("when"), last.get("commit"), last.get("clean"),
                 last.get("args")))
        print("  counts   : %s" % (last.get("counts") or {}))
    except Exception:                                        # noqa: BLE001
        doc = None
        print("  recorded : <absent or unreadable>")
    print("  HEAD now : %s" % head())
    problems = check(doc)
    if problems:
        print()
        for p in problems:
            print("REFUSED: %s" % p)
        return 1
    print("\nOK. The suite ran on HEAD over a clean tree, whole-suite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
