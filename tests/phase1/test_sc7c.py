"""SC-7(c)'s invariant, and the known-positives that make its clean result mean
something.

A check that has never fired on a positive is not a check -- it is a function
that returns. So every route `sc7c` claims to close gets its own violating copy
of the package, and the check is required to fire on each. The negative control
runs last: an unmodified copy must PASS, or the four positives above it would
only prove the check always fires.

The scratch copies are built in pytest's tmp_path. Nothing in the real package or
in any session scratchpad is written to.
"""
from __future__ import annotations

import pathlib
import shutil

import pytest

from sc7c import KeyLeak, assert_key_free

PKG = pathlib.Path(__file__).resolve().parents[2] / "src" / "leakaudit"

# One per route sc7c enumerates. The comment is the route; the string is the
# line spliced into an otherwise untouched copy of the package.
VIOLATIONS = {
    "import-the-name":
        "from protocol.runtime_reference import CaseLabels\n",
    "bind-the-harness-module":
        "import protocol.runtime_reference\n",
    "construct-it":
        "def _leak():\n    return CaseLabels('d', 'c', frozenset())\n",
    "reach-it-by-attribute":
        "def _leak(mod):\n    return mod.CaseLabels\n",
}


def test_the_real_package_is_key_free():
    """The shipped package cannot reach the scoring key."""
    n = assert_key_free(PKG)
    assert n >= 9, "expected the package's nine modules, scanned %d" % n


@pytest.mark.parametrize("route", sorted(VIOLATIONS))
def test_known_positive_each_route_fires(tmp_path, route):
    """Splice one violation into a copy and require the check to fire.

    Parametrised per route rather than looped, so a route that stops being
    detected names itself in the failure instead of hiding behind the first.
    """
    dst = tmp_path / route / "leakaudit"
    shutil.copytree(PKG, dst)
    target = dst / "probe.py"
    target.write_text(target.read_text(encoding="utf-8") + "\n\n"
                      + VIOLATIONS[route], encoding="utf-8")

    with pytest.raises(KeyLeak) as exc:
        assert_key_free(dst)
    assert "probe.py" in str(exc.value), \
        "the check fired but did not name the module carrying the violation"


def test_negative_control_an_untouched_copy_passes(tmp_path):
    """Without this the four positives prove only that the check always fires."""
    dst = tmp_path / "clean" / "leakaudit"
    shutil.copytree(PKG, dst)
    assert assert_key_free(dst) >= 9


def test_an_empty_population_is_not_a_pass(tmp_path):
    """A scan with nothing to scan must not report success."""
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(KeyLeak):
        assert_key_free(empty)


def test_the_docstring_citation_resolves():
    """`leakaudit`'s docstring cites where the invariant lives. It cited a file
    that did not exist, which is how an unenforced invariant survived; this
    fails if the citation goes stale again."""
    doc = (PKG / "__init__.py").read_text(encoding="utf-8")
    cited = "tests/phase1/sc7c.py"
    assert cited in doc, \
        "the package docstring no longer cites %s; correct it or move the check" % cited
    assert (pathlib.Path(__file__).resolve().parent / "sc7c.py").exists()
