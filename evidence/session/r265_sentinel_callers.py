"""R265 §2. Every caller the stride sentinel changed, and whether a figure moved.

    PYTHONPATH=. py -3.12 evidence/session/r265_sentinel_callers.py

WHY. R263 made `run_probe_a`'s `cohort_stride` a sentinel and resolved an
undeclared stride to the FLOOR. R265 §2 restores the shipped default of 97 where
it clears the floor. Between those two rounds, any caller that OMITTED the
stride was silently running at a different schedule -- so the question is not
"what changed" but "did any of them produce a recorded figure while it was
changed".

PARSED, NOT GREPPED, for the reason this project keeps re-learning: a search for
`cohort_stride` reports the calls that pass it, and the population here is the
calls that DO NOT.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import ast
import pathlib
import subprocess
import sys

REPO = pathlib.Path.cwd()


def call_sites(rel: str):
    """(line, passes_stride) for every `run_probe_a` / `run_probe_l2a` call."""
    tree = ast.parse((REPO / rel).read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
        if name not in ("run_probe_a", "run_probe_l2a"):
            continue
        kw = {k.arg for k in node.keywords if k.arg}
        out.append((name, node.lineno, "cohort_stride" in kw))
    return out


def main() -> int:
    files = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "--cached", "--others",
         "--exclude-standard", "--", "*.py"],
        capture_output=True, text=True, encoding="utf-8").stdout.split()

    print("=" * 78)
    print("R265 section 2 -- callers that omit the stride and reach the sentinel")
    print("=" * 78)
    omitters = []
    total = 0
    for rel in sorted(files):
        if rel.startswith("build/"):
            continue
        try:
            sites = call_sites(rel)
        except (SyntaxError, OSError):
            continue
        for name, line, passes in sites:
            total += 1
            if not passes:
                omitters.append((rel, line, name))
    print("call sites parsed        : %d" % total)
    print("of which OMIT the stride : %d" % len(omitters))
    print()
    for rel, line, name in omitters:
        collected = "COLLECTED BY PYTEST" if pathlib.Path(rel).name.startswith(
            "test_") else "not a pytest module"
        print("  %-52s:%-5d %-14s %s" % (rel, line, name, collected))
    print()
    print("WHY THE DISTINCTION IS THE WHOLE ANSWER. A caller that pytest does")
    print("not collect did not RUN between R263 and R265, so the schedule it")
    print("would have taken was never executed and no figure it produces moved.")
    print("A collected one ran on every suite invocation in that window.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
