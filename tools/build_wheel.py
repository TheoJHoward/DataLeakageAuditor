#!/usr/bin/env python3
"""Build the wheel the way the verification does: through an sdist. R276 §1(5).

    py -3.12 tools/build_wheel.py [--out DIR] [--python EXE]

WHY THIS TOOL EXISTS, AND IT IS A DEFECT THIS PROJECT SHIPPED. R275 §1 tried to
show the wheel check failing -- package-data line removed, rebuild, look for the
template -- and it would not fail. `pip wheel .` builds IN TREE, setuptools
copies what it builds into `build/lib`, and it never clears that directory. So
every in-tree wheel inherited `build/lib/leakaudit/templates/TEMPLATE.json` from
an earlier build, whatever the configuration said, and a check built that way
proves nothing about the configuration it claims to check (D-V30A-122).

WHAT IT DOES, in order, printing each step:

  1. REMOVES `build/`. Its own housekeeping, recorded in the output with the
     count, because a silent deletion is how the next person loses a file they
     were using.
  2. Builds the SDIST, then the wheel FROM the sdist -- `python -m build`, whose
     default does exactly that. The sdist carries what the configuration
     declares and nothing a previous build left behind.
  3. Prints the wheel's file list, so what shipped is on the screen rather than
     in somebody's assumption.

Exit 0 on a built wheel, 1 on a build failure. Written with the Write tool per
D2.1.
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def clean_build_tree(root: pathlib.Path) -> int:
    """Remove `build/`, returning how many files went. Housekeeping, announced."""
    tree = root / "build"
    if not tree.exists():
        print("  build/ absent, nothing to remove")
        return 0
    n = sum(1 for p in tree.rglob("*") if p.is_file())
    shutil.rmtree(tree)
    print("  removed build/ -- %d file(s). An in-tree build tree is inherited "
          "by the next wheel whatever the configuration says (D-V30A-122), so "
          "it goes before anything is built." % n)
    return n


def build(root: pathlib.Path, out: pathlib.Path, python: str) -> pathlib.Path:
    """`python -m build`: sdist first, then the wheel FROM the sdist."""
    cmd = [python, "-m", "build", "--outdir", str(out)]
    print("  %s" % " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True)
    if r.returncode != 0:
        sys.stdout.write(r.stdout[-4000:])
        sys.stderr.write(r.stderr[-4000:])
        raise SystemExit("BUILD FAILED (exit %d). `python -m build` is the route "
                         "this tool takes; install it with `%s -m pip install "
                         "build`." % (r.returncode, python))
    wheels = sorted(out.glob("*.whl"), key=lambda p: p.stat().st_mtime)
    if not wheels:
        raise SystemExit("the build reported success and produced no wheel in %s"
                         % out)
    return wheels[-1]


def file_list(wheel: pathlib.Path) -> list:
    with zipfile.ZipFile(wheel) as z:
        return sorted(z.namelist())


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(ROOT / "dist"),
                    help="where the sdist and wheel are written (default dist/)")
    ap.add_argument("--python", default=sys.executable,
                    help="the interpreter that runs `python -m build`")
    args = ap.parse_args(argv)
    out = pathlib.Path(args.out)

    print("BUILD THE WHEEL THROUGH AN SDIST -- %s" % ROOT)
    print("1. housekeeping")
    clean_build_tree(ROOT)
    print("2. build")
    wheel = build(ROOT, out, args.python)
    print("3. what shipped: %s" % wheel)
    names = file_list(wheel)
    for name in names:
        print("     %s" % name)
    templates = [n for n in names if "/templates/" in n]
    print("  %d file(s) in the wheel; %d under templates/%s"
          % (len(names), len(templates),
             "" if templates else " -- NO templates ENTRY"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
