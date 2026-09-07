"""The vacuity detector's own known positives. R251 §0.

**THE PROBE THAT HUNTS VACUITY WAS VACUOUS.** Its first version patched the
population helpers on the TEST module while the tests call them on the tool they
imported, so it emptied nothing and reported 37 candidates — the instrument built
to find checks that do not exercise their subject did not exercise its own.

**It was caught by a number looking wrong, not by a mechanism.** 37 was chased
because it seemed high; had the bug produced a plausible count, nothing would
have prompted the look. That is diligence, and diligence is what this project
keeps establishing does not survive the busy round.

So the probe gets what it demands of everything else:

    A CONSTRUCTED VACUOUS ASSERTION has to come back `candidate`.
    A CONSTRUCTED HEALTHY ASSERTION has to come back `reddens`.

Five real assertions reddening shows the probe *can* fire. Only the constructed
pair shows it fires **on the shape it exists to catch, and not on everything** —
a detector that flagged all of them, or none, would look identical in the summary
counts.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import empty_population_probe as epp                               # noqa: E402


def _synth(tmp_path, source, name="synth_mod.py"):
    (tmp_path / name).write_text(textwrap.dedent(source), encoding="utf-8")
    return name


# ---------------------------------------------------------------------------
# the known positive: a vacuity the probe has to catch
# ---------------------------------------------------------------------------
def test_a_CONSTRUCTED_VACUOUS_assertion_comes_back_CANDIDATE(tmp_path):
    """The assertion concludes something about every member of a population it
    reads, so emptying the population makes it vacuously true. This is the
    `round_reconciliation` shape and the shape the probe exists to find."""
    rel = _synth(tmp_path, '''
        def tracked_files():
            return ["a.py", "b.ipynb"]

        def test_no_tracked_file_is_a_notebook():
            tail = [f for f in tracked_files() if f.endswith(".ipynb")]
            assert not [f for f in tail if f.startswith("z")]
    ''')
    verdict, detail = epp.probe(rel, "test_no_tracked_file_is_a_notebook",
                                tmp_path)
    assert verdict == "candidate", (
        "a deliberately vacuous assertion came back %r, so the probe does not "
        "detect the shape it exists to detect: %s" % (verdict, detail))


def test_a_CONSTRUCTED_HEALTHY_assertion_comes_back_REDDENS(tmp_path):
    """The negative control. A probe that returned `candidate` for everything
    would pass the known positive above and be worthless."""
    rel = _synth(tmp_path, '''
        def tracked_files():
            return ["a.py", "b.py"]

        def test_the_population_is_not_empty():
            files = tracked_files()
            assert len(files) > 1, "the population is empty"
    ''', "synth_healthy.py")
    verdict, detail = epp.probe(rel, "test_the_population_is_not_empty",
                                tmp_path)
    assert verdict == "reddens", (
        "an assertion that checks its population is non-empty came back %r "
        "rather than reddening when emptied: %s" % (verdict, detail))


def test_a_test_the_probe_CANNOT_EMPTY_comes_back_UNPROBED(tmp_path):
    """The third state, and the one the first version collapsed. A test whose
    population this mechanism cannot reach is UNVERIFIED, not clean — reporting
    it as a candidate is what produced the 37."""
    rel = _synth(tmp_path, '''
        HARDCODED = ("x", "y")

        def test_over_a_literal():
            assert all(isinstance(h, str) for h in HARDCODED)
    ''', "synth_literal.py")
    verdict, detail = epp.probe(rel, "test_over_a_literal", tmp_path)
    assert verdict == "unprobed", (
        "a test with no emptiable population came back %r; the probe is "
        "claiming to have tested something it never touched: %s"
        % (verdict, detail))
    assert "no population helper" in detail


def test_a_test_TAKING_A_FIXTURE_comes_back_UNPROBED(tmp_path):
    """The 40 largest group of unprobed. Named as unverified rather than
    silently folded into a swept count."""
    rel = _synth(tmp_path, '''
        def tracked_files():
            return ["a"]

        def test_with_a_fixture(some_fixture):
            assert some_fixture
    ''', "synth_fixture.py")
    verdict, detail = epp.probe(rel, "test_with_a_fixture", tmp_path)
    assert verdict == "unprobed" and "fixture" in detail


# ---------------------------------------------------------------------------
# the mechanism the first version got wrong
# ---------------------------------------------------------------------------
def test_patch_targets_REACHES_THE_IMPORTED_TOOL_not_just_the_test_module():
    """THE BUG, PINNED. A test calls `mv.entries()`, not `entries()`. Stopping
    at the test module empties nothing, which is how 37 candidates were
    reported over populations that were never emptied."""
    import coverage_assertion_sweep as cas

    import tests.phase1.test_coverage_assertion_sweep as t  # noqa: F401
    mod = epp.load("tests/phase1/test_coverage_assertion_sweep.py")
    targets = epp.patch_targets(mod)
    assert len(targets) > 1, (
        "patch_targets returned only the test module, so no imported tool would "
        "be emptied and every population would survive the probe")
    assert any(getattr(m, "__name__", "").endswith("coverage_assertion_sweep")
               for m in targets), [getattr(m, "__name__", "?") for m in targets]


def test_the_probe_REPORTS_and_does_not_gate():
    """Candidates, never findings — so it cannot become pressure to mark
    assertions clean."""
    assert epp.main([]) == 0
