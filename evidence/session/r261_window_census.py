"""R261 §3.1. Every Phase 1 run's window and column_modes, parsed not recalled.

    PYTHONPATH=. py -3.12 <this file>

WHY IT PARSES RATHER THAN GREPS. The question is an ABSENCE claim -- no Phase 1
run used a window other than 1.0, and none declared column_modes -- and an
absence claim needs its population enumerated. A grep for `window` reports the
lines that say `window`; it cannot report a call that omitted it, which is the
case that matters. So every `AvailabilityModel(...)` construction and every
`run_probe_a(...)` call in the population is parsed from the AST and reported
WITH ITS DEFAULTS MADE EXPLICIT.

THE POPULATION IS STATED AND IS NOT `tests/phase1/*.py` ENTIRE. It is the
harnesses that produced Phase 1 run records, plus the guard that re-runs the
whole-frame path, plus the two probe-A/B side scripts. Unit-test modules are
excluded by name and the exclusion is printed, because a scan exclusion where a
declared token is available is its own defect.

Written with the Write tool per D2.1. Read-only against the repository.
"""
from __future__ import annotations

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve()
REPO = pathlib.Path.cwd()

#: The population. Named, not globbed, so a reader can disagree with the set.
POPULATION = [
    "tests/phase1/harness_criteria_12.py",
    "tests/phase1/harness_criteria_12_population.py",
    "tests/phase1/harness_identity_control.py",
    "tests/phase1/harness_acceptance.py",
    "tests/phase1/harness_probe_b.py",
    "tests/phase1/harness_probe_b_shard.py",
    "tests/phase1/harness_b9_shard.py",
    "tests/phase1/b6_probe_a_controls.py",
    "tests/phase1/b7_probe_a_side.py",
    "tests/phase1/b9_wrapped_controls.py",
    "tests/phase1/b9_wrapped_side.py",
    "tools/wholeframe_guard.py",
]

EXCLUDED_REASON = (
    "tests/phase1/test_*.py are unit modules: they construct models to exercise "
    "the probe, they produced no Phase 1 run record, and no published figure "
    "rests on them. Named here rather than silently outside the glob."
)


def _lit(node):
    """A readable rendering of an argument node, or its source shape."""
    try:
        return repr(ast.literal_eval(node))
    except Exception:
        return ast.unparse(node)


def calls(path: pathlib.Path, name: str):
    """Every call to `name` in `path`, as (lineno, {kw: rendered})."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        label = getattr(fn, "id", None) or getattr(fn, "attr", None)
        if label != name:
            continue
        kw = {k.arg: _lit(k.value) for k in node.keywords if k.arg}
        out.append((node.lineno, kw))
    return out


def main() -> int:
    print("=" * 78)
    print("R261 section 3.1 -- Phase 1's window and column_modes, from the tree")
    print("=" * 78)
    print("population: %d named file(s)" % len(POPULATION))
    print("excluded  : %s" % EXCLUDED_REASON)
    print()

    missing = [p for p in POPULATION if not (REPO / p).exists()]
    if missing:
        print("REFUSED: %d population file(s) are not on disk: %s"
              % (len(missing), ", ".join(missing)))
        return 1

    n_models = n_probes = 0
    non_unit_window = []
    with_modes = []

    for rel in POPULATION:
        p = REPO / rel
        models = calls(p, "AvailabilityModel")
        probes = calls(p, "run_probe_a")
        if not models and not probes:
            print("%-46s no model construction, no probe call" % rel)
            continue
        print(rel)
        for line, kw in models:
            n_models += 1
            w = kw.get("window", "<default: SECOND = 1s>")
            if "window" in kw:
                non_unit_window.append((rel, line, w))
            print("    line %-5d AvailabilityModel  window=%s" % (line, w))
        for line, kw in probes:
            n_probes += 1
            cm = kw.get("column_modes", "<omitted: None>")
            if "column_modes" in kw:
                with_modes.append((rel, line, cm))
            print("    line %-5d run_probe_a        column_modes=%s" % (line, cm))
        print()

    print("-" * 78)
    print("model constructions parsed : %d" % n_models)
    print("run_probe_a calls parsed   : %d" % n_probes)
    print("constructions passing an EXPLICIT window : %d" % len(non_unit_window))
    for rel, line, w in non_unit_window:
        print("    %s:%d  window=%s" % (rel, line, w))
    print("probe calls passing column_modes         : %d" % len(with_modes))
    for rel, line, cm in with_modes:
        print("    %s:%d  column_modes=%s" % (rel, line, cm))
    print("-" * 78)
    print("A construction with no `window=` takes `AvailabilityModel.window`'s")
    print("default, which is `SECOND` -- one second -- so it is on the path where")
    print("the identity holds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
