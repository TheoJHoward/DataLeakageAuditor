#!/usr/bin/env python3
"""The working tree a run measured, as one hash. R272 §2(g).

    $ py -3.12 tools/tree_fingerprint.py

D-V30A-117 WAS A COMMIT OF A TREE NO SUITE HAD MEASURED. The suite record said
which HEAD it ran on, and HEAD alone cannot say that: a suite run, then an edit,
then a commit leaves HEAD where the suite saw it and ships a file the suite never
read. So a run records a fingerprint of the WORKING tree -- HEAD plus the content
hash of every modified, staged, deleted and untracked non-ignored file -- and the
commit route computes the same fingerprint and refuses when no record matches.

WHAT IS LEFT OUT, AND WHY EACH. `.claude/` is never committed. The two RUN
RECORDS, the suite's and the guard's, are written by the runs they record, so
including them would make every run invalidate its own record. CONTENT hashes,
not porcelain status codes: `git add` after the suite changes a line's status and
not the tree the suite read.

THE GUARD'S FINGERPRINT IS NARROWER, ON PURPOSE. The guard vouches for the probe
path, not for the records a round appends after it, so `path_set_fingerprint`
covers the path-set files' content only. A whole-tree fingerprint there would make
every disclosure written after the guard demand a second guard run, which a round
is not allowed.

Written with the Write tool per D2.1. Reads only.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]

#: Never committed, so never part of the tree a commit ships.
NOT_TREE_PREFIXES = (".claude/",)

#: Written by the runs they record. Exact paths, not prefixes.
RUN_RECORDS = ("tools/suite_tree_record.json", "tools/wholeframe_guard_times.json")


class FingerprintError(RuntimeError):
    """git could not be asked, so no fingerprint is a result."""


def _git(root, *args) -> bytes:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if r.returncode != 0:
        raise FingerprintError(
            "`git %s` exited %d in %s, so the tree is unknown and no fingerprint "
            "is reported: %s" % (" ".join(args), r.returncode, root,
                                 r.stderr[:200].decode("utf-8", "replace")))
    return r.stdout


def head(root=None) -> str:
    """The full HEAD hash, or `unborn` in a repository with no commit yet."""
    r = subprocess.run(["git", "-C", str(root or REPO), "rev-parse", "--verify",
                        "-q", "HEAD"], capture_output=True)
    return r.stdout.decode().strip() if r.returncode == 0 else "unborn"


def changed_paths(root=None) -> list:
    """Every modified, staged, deleted or untracked non-ignored path, sorted.

    `-z` porcelain, so no path is quoted or trimmed -- the first-line stripping
    defect `suite_tree.dirty_paths` once had cannot occur -- and
    `--untracked-files=all`, so an untracked directory is its files, not one line.
    """
    root = root or REPO
    parts = _git(root, "status", "--porcelain=v1", "-z",
                 "--untracked-files=all").split(b"\0")
    out = set()
    i = 0
    while i < len(parts):
        entry = parts[i]
        i += 1
        if not entry:
            continue
        code = entry[:2].decode("ascii", "replace")
        path = entry[3:].decode("utf-8")
        if code[0] in "RC":
            i += 1   # a rename or copy carries its source as the next field
        if path.startswith(NOT_TREE_PREFIXES) or path in RUN_RECORDS:
            continue
        out.add(path)
    return sorted(out)


def _content(root, rel) -> str:
    p = pathlib.Path(root) / rel
    if not p.exists():
        return "absent"
    if p.is_dir():
        return "directory"
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fingerprint(root=None) -> dict:
    """HEAD plus the content of every changed path, as a digest."""
    root = root or REPO
    h = head(root)
    files = {rel: _content(root, rel) for rel in changed_paths(root)}
    lines = ["head %s" % h] + ["%s %s" % (files[k], k) for k in sorted(files)]
    return {"head": h, "files": files,
            "digest": hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()}


def path_set_fingerprint(paths, root=None) -> str:
    """The content of the named paths, as a digest. What the guard vouches for."""
    root = root or REPO
    lines = ["%s %s" % (_content(root, rel), rel) for rel in sorted(paths)]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def main(argv=None) -> int:
    fp = fingerprint()
    print("TREE FINGERPRINT %s" % fp["digest"])
    print("  head  : %s" % fp["head"])
    print("  files : %d changed, non-ignored, outside the run records"
          % len(fp["files"]))
    for k in sorted(fp["files"]):
        print("    %s  %s" % (fp["files"][k][:12], k))
    return 0


if __name__ == "__main__":
    sys.exit(main())
