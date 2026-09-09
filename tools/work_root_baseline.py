"""Write the work-root residue baseline. R226 §3.

    python tools/work_root_baseline.py             # show the increment
    python tools/work_root_baseline.py --write     # accept it into the baseline

WHY THIS IS A SEPARATE TOOL AND NOT SOMETHING THE CHECK DOES. A baseline that
updated itself on every run would make the increment empty always, and the check
would report green over a population it had just absorbed -- which is the exact
defect D-V30A-48 recorded, a check confidently reporting nothing about a set it
was not looking at. Accepting an increment is a decision, so it is a command
somebody types.

WHAT AN ENTRY MEANS, stated because the wrong reading is the dangerous one. A
path in the baseline has been REPORTED AND READ. It does NOT mean the file is
ephemeral, does not mean it belongs where it is, and does not remove it from the
level the check prints every run. The ephemeral list is the place where a claim
about a file is made, and it takes a reason; this file takes none, because it
asserts nothing.

THE LEVEL STAYS IN THE OUTPUT. R226 §3's rule is that a growing level is not a
finding and its increment is; it is not that the level disappears. Both are
printed on every run.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import check_registration as cr                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
HEADER = (
    "# Work-root residue baseline. R226 §3.\n"
    "#\n"
    "# One path per line, relative to LEAKAUDIT_WORK_ROOT. An entry means the\n"
    "# file was REPORTED BY `round_reconciliation` AND READ -- it is not a claim\n"
    "# that the file is ephemeral, and it does not remove the file from the\n"
    "# level the check prints. Claims about files, with reasons, live in\n"
    "# `_EPHEMERAL` in tools/check_registration.py; this file makes none.\n"
    "#\n"
    "# Written by `python tools/work_root_baseline.py --write`, deliberately,\n"
    "# at the end of a round. Never by the check itself.\n")


def _residue() -> list[str]:
    """The current unreconciled set, from the check's own findings."""
    work_root = cr._work_root()
    if work_root is None:
        raise SystemExit(
            "LEAKAUDIT_WORK_ROOT is unset, so there is no working directory to "
            "baseline. Set it to this round's scratch directory. Writing a "
            "baseline from an empty population would record that nothing is "
            "outstanding, which is the defect D-V30A-48 describes.")
    if not work_root.exists():
        raise SystemExit("LEAKAUDIT_WORK_ROOT names %s, which does not exist."
                         % work_root)

    import hashlib
    import re
    repo_hashes = set()
    for p in ROOT.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            try:
                repo_hashes.add(hashlib.sha256(p.read_bytes()).hexdigest())
            except OSError:
                pass
    out = []
    for p in work_root.rglob("*"):
        if not p.is_file():
            continue
        posix = "/" + p.relative_to(work_root).as_posix()
        if any(tok in posix or posix.endswith(tok) for tok, _ in cr._EPHEMERAL):
            continue
        try:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError:
            continue
        if digest in repo_hashes:
            continue
        if p.stat().st_size > 5_000_000:
            continue
        out.append(posix.lstrip("/"))
    return sorted(out)


#: The per-root section marker. A COMMENT, deliberately: `check_registration`
#: reads this file by taking every non-`#` line as a path, and that reader is
#: the frozen instrument. Carrying the root in a comment lets the writer keep
#: roots apart without the reader changing, which is what R261 §5(c) bounds this
#: to. The cost is stated where it is paid, in `split_by_root` below.
ROOT_MARK = "# root: "

#: Entries written before R261, when the format carried no root at all. They
#: cannot be attributed now -- the information was never recorded -- so they are
#: labelled for what they are rather than guessed at.
LEGACY = "unrecorded (written before R261 §5; the format carried no root)"


def split_by_root(text: str) -> dict:
    """{root label -> [paths]}, preserving order, from a baseline file.

    WHAT THIS BUYS AND WHAT IT DOES NOT. It buys the merge: accepting an
    increment under root B rewrites B's block and leaves A's alone, so a work
    root that is mounted again finds its own entries where it left them. It does
    NOT make the READER root-aware: `check_registration` still takes the union
    of every path in the file, so a path under root B is satisfied by an
    identical relative path recorded under root A. That is a real weakening of
    the increment check and it is the price of leaving the frozen reader alone;
    closing it needs that reader to change, which is a ruled-difference spend and
    is not this round's.
    """
    blocks: dict = {}
    label = LEGACY
    for line in text.splitlines():
        if line.startswith(ROOT_MARK):
            label = line[len(ROOT_MARK):].strip() or LEGACY
            blocks.setdefault(label, [])
            continue
        if line.startswith("#") or not line.strip():
            continue
        blocks.setdefault(label, []).append(line.strip())
    return blocks


def render(blocks: dict) -> str:
    """The file, root by root. Empty blocks are kept: a root with nothing
    outstanding is a different statement from a root nobody has looked at."""
    out = [HEADER.rstrip("\n"), "",
           "# ROOT SECTIONS -- R261 §5. Each block is the residue accepted under",
           "# one work root. Accepting an increment rewrites only that root's",
           "# block; a root that is not the current one is never touched.", ""]
    for label, paths in blocks.items():
        out.append(ROOT_MARK + label)
        out.extend(sorted(set(paths)))
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def main(argv) -> int:
    path = ROOT / cr._WORK_ROOT_BASELINE
    current = set(_residue())
    this_root = str(cr._work_root())
    if path.exists():
        text = path.read_text(encoding="utf-8")
        blocks = split_by_root(text)
        baseline = {p for paths in blocks.values() for p in paths}
    else:
        blocks = {}
        baseline = set()
        print("no baseline at %s" % cr._WORK_ROOT_BASELINE)
    print("root      : %s" % this_root)
    print("roots held: %d (%s)"
          % (len(blocks), ", ".join(blocks) if blocks else "none"))

    appeared = sorted(current - baseline)
    gone = sorted(baseline - current)
    print("level     : %d" % len(current))
    print("baseline  : %d" % len(baseline))
    print("appeared  : %d" % len(appeared))
    for p in appeared[:40]:
        print("    + %s" % p)
    if len(appeared) > 40:
        print("    ... and %d more" % (len(appeared) - 40))
    print("gone      : %d" % len(gone))

    if "--write" not in argv:
        print("\nnot written. Re-run with --write to accept these into the "
              "baseline, which records that they were reported and read.")
        return 0

    # MERGE, NEVER REPLACE. R261 §5(a). The previous writer rendered the whole
    # file from the CURRENT root's residue, so changing work roots silently
    # dropped every entry the old root had accumulated -- 738 of them, at R260,
    # in an artifact the manifest attests. Only this root's block moves.
    blocks[this_root] = sorted(current)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(blocks), encoding="utf-8", newline="\n")
    kept = sum(len(v) for k, v in blocks.items() if k != this_root)
    print("\nwrote %s: %d path(s) under this root, %d under %d other root(s), "
          "untouched" % (cr._WORK_ROOT_BASELINE, len(current), kept,
                         max(0, len(blocks) - 1)))
    return 0


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
