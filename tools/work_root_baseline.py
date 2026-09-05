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


def main(argv) -> int:
    path = ROOT / cr._WORK_ROOT_BASELINE
    current = set(_residue())
    if path.exists():
        baseline = {ln.strip() for ln in
                    path.read_text(encoding="utf-8").splitlines()
                    if ln.strip() and not ln.startswith("#")}
    else:
        baseline = set()
        print("no baseline at %s" % cr._WORK_ROOT_BASELINE)

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

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + "\n".join(sorted(current)) + "\n",
                    encoding="utf-8", newline="\n")
    print("\nwrote %s: %d path(s)" % (cr._WORK_ROOT_BASELINE, len(current)))
    return 0


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
