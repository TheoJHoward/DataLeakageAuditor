"""Emit the declared floor's figures. R229 §1.

    python tools/floor_check.py <path-to-floor-interpreter>

    python tools/floor_check.py C:\\Users\\...\\v311corner\\Scripts\\python.exe

WHY THIS EXISTS. `INSTALL.md`'s floor row was a hand-typed number: a measurement
of one commit, written as a standing fact about the package, with nothing
connecting it to the tree it came from. It went stale in the worst way available
— sixty-three minutes after it was written, a tool was wired onto a 3.12-only
recorder, and the row kept asserting a suite result that no longer held. Nothing
re-ran it because nothing could: the environment was gone.

**A change on the probe's path re-runs the whole-frame guard. A change that breaks
the declared floor interpreter ran into nothing at all.** This is the missing
counterpart, and the corner venv now exists, so it is one command.

THE FIGURES ARE EMITTED, NOT REMEMBERED. Same rule as the interpreter banner in
`check_registration.py`: the frame travels with the figure or it does not travel.
Everything below is printed by the run that produced it — the interpreter, the
four package versions, the suite counts, the digest and its recipe — in the form
`INSTALL.md`'s row wants, so the row is pasted rather than typed.

THE INTERPRETER IS A REQUIRED ARGUMENT. No discovery, no default, no
"most-recently-modified venv" heuristic. This project has already recorded what
guessing an environment costs (D-V30A-48), and a floor check that silently
measured the wrong interpreter would be worse than none: it would report green
about a population it never touched.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]

VERSIONS = (
    "import sys, numpy, pandas, pyarrow;"
    "print(sys.version.split()[0], numpy.__version__,"
    " pandas.__version__, pyarrow.__version__)"
)


def _run(argv: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, cwd=str(REPO),
                          **kw)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__.strip().split("\n\n")[1])
        print("\nRefused rather than guessed: name the interpreter. A floor "
              "check that picked its own would report about whichever "
              "environment it happened to find.", file=sys.stderr)
        return 2

    py = pathlib.Path(argv[0])
    if not py.is_file():
        print("no such interpreter: %s" % py, file=sys.stderr)
        return 2

    probe = _run([str(py), "-c", VERSIONS])
    if probe.returncode != 0:
        print("that interpreter cannot import the dependencies, so it is not a "
              "floor environment:\n%s" % probe.stderr.strip(), file=sys.stderr)
        return 2
    pyv, npv, pdv, pav = probe.stdout.split()

    print("FLOOR CHECK")
    print("  interpreter  CPython %s" % pyv)
    print("  numpy        %s" % npv)
    print("  pandas       %s" % pdv)
    print("  pyarrow      %s" % pav)
    print("  executable   %s" % py)
    print()

    t = time.time()
    suite = _run([str(py), "-m", "pytest", "tests", "-q"])
    secs = time.time() - t
    tail = [ln for ln in suite.stdout.splitlines() if " passed" in ln
            or " failed" in ln or " error" in ln]
    print("  $ %s -m pytest tests -q" % py.name)
    print("    %s" % (tail[-1] if tail else "(no summary line)"))
    print("    wall clock %.0f s" % secs)
    failed = [ln for ln in suite.stdout.splitlines() if ln.startswith("FAILED")]
    for ln in failed:
        print("    %s" % ln)
    print()

    dig = _run([str(py), str(REPO / "tools" / "portability_digest.py")])
    line = [ln for ln in dig.stdout.splitlines() if ln.startswith("DIGEST")]
    print("  $ %s tools/portability_digest.py" % py.name)
    print("    %s" % (line[0] if line else "(no digest line)"))
    print("    recipe: sha256 over the canonical body, lines joined with a "
          "single LF,")
    print("            one trailing LF, encoded UTF-8, banner excluded.")
    print()

    print("  INSTALL.md row, ready to paste:")
    # ASCII only: this line is copied into a file, and a console that cannot
    # encode the character silently substitutes one, which is how a digest
    # prefix becomes a question mark in a published table.
    print("  | **%s** | **%s** | **%s** | **%s** | %s | `%s...` |"
          % (pyv, npv, pdv, pav,
             (tail[-1].split(" in ")[0] if tail else "?"),
             (line[0].split()[-1][:12]) if line else "?"))
    return 0 if suite.returncode == 0 else 1


if __name__ == "__main__":                                   # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
