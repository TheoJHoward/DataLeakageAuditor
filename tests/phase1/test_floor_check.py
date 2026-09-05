"""The floor check refuses to guess its interpreter. R229 §1.

WHAT THIS GUARDS. `tools/floor_check.py` re-measures the declared floor: it runs
the suite and the portability digest under a named interpreter and prints the
figures with their invocation. Its one dangerous failure mode is measuring the
WRONG environment and reporting confidently about it — D-V30A-48's defect, which
this project has already paid for once, where a check reported green over a
population it was not looking at.

So the argument is required and there is no discovery heuristic, and that is
asserted here rather than left to the docstring.

WHAT IS NOT TESTED HERE, said rather than implied: the full run. Exercising it end
to end costs a floor suite (~45 s) plus a probe, and doing that on every suite run
would put the thing it measures inside the thing it measures. The paths tested are
the ones that decide WHICH environment gets measured.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "floor_check.py"

for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import floor_check                                              # noqa: E402


def test_no_argument_is_REFUSED_not_defaulted():
    r = subprocess.run([sys.executable, str(TOOL)], capture_output=True,
                       text=True, cwd=str(ROOT))
    assert r.returncode == 2, (
        "running it with no interpreter did not refuse. A floor check that "
        "picks its own environment reports about whichever one it finds.")
    assert "name the interpreter" in (r.stdout + r.stderr)


def test_a_nonexistent_interpreter_is_REFUSED():
    r = subprocess.run([sys.executable, str(TOOL), str(ROOT / "no_such_python")],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2
    assert "no such interpreter" in (r.stdout + r.stderr)


def test_an_interpreter_without_the_dependencies_is_REFUSED_as_not_a_floor():
    """The case that matters most: a bare 3.11 on this machine has no numpy, so
    pointing the check at it must say 'that is not a floor environment' rather
    than crash inside pytest and leave a partial number on screen."""
    import shutil
    bare = shutil.which("python") or sys.executable
    probe = subprocess.run([bare, "-c", "import numpy"], capture_output=True)
    if probe.returncode == 0:
        import pytest
        pytest.skip("the interpreter on PATH has numpy; no bare one to point at")
    r = subprocess.run([sys.executable, str(TOOL), bare],
                       capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 2
    assert "not a floor environment" in (r.stdout + r.stderr)


def test_the_module_takes_its_interpreter_as_a_parameter_with_no_default():
    """A signature check, so the refusal cannot be softened into a default
    later without this failing."""
    import inspect
    sig = inspect.signature(floor_check.main)
    assert list(sig.parameters) == ["argv"], sig
    assert sig.parameters["argv"].default is inspect.Parameter.empty


def test_it_names_no_discovery_heuristic():
    src = TOOL.read_text(encoding="utf-8")
    code = "\n".join(ln for ln in src.split("\n")
                     if not ln.strip().startswith("#"))
    body = code.split('"""')[-1]
    for banned in ("glob(", "rglob(", "getmtime", "st_mtime"):
        assert banned not in body, (
            "%r appears in the body: this file must not search for an "
            "environment, only accept one" % banned)
