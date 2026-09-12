"""C: the budget, the three coverage states, and the exit classes. R267 §3, R268 §3.

R268 restored the denominator to every cohort the declared model makes
probe-able, independent of stride and budget, so a default run at stride 97 is
INCOMPLETE and says so. Each pair below holds everything but one quantity fixed
and says what is held -- R257's rule for a controlled comparison.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                     # noqa: E402
from leakaudit.coverage import (                              # noqa: E402
    BUDGET_TARGET_SECONDS, DEFAULT_L2A_COHORTS, FIXTURE_BUILD_SECONDS,
    AuditIncomplete, Coverage, assert_audit_complete, budget_arithmetic)
from leakaudit.label_probe import run_probe_l2a              # noqa: E402


def _cov(probed, unprobed, ineligible=0, l2a_p=0, l2a_e=0, context=0):
    """Rows mirror cohorts at ten per second, so both rows of states move
    together and a test varying one quantity varies nothing else."""
    return Coverage(cohorts_probed=probed, cohorts_unprobed=unprobed,
                    cohorts_ineligible=ineligible,
                    rows_probed=probed * 10, rows_unprobed=unprobed * 10,
                    rows_ineligible=ineligible * 10, context_rows=context,
                    l2a_probed=l2a_p, l2a_eligible=l2a_e)


# --------------------------------------------------------------------------
# §3(b)/(e) -- the default is derived, printed, and has ONE definition
# --------------------------------------------------------------------------

def test_the_default_is_DERIVED_from_the_measured_build_time():
    """`(N + 1) * build <= target`, and N is the LARGEST such value."""
    assert (DEFAULT_L2A_COHORTS + 1) * FIXTURE_BUILD_SECONDS <= BUDGET_TARGET_SECONDS
    assert (DEFAULT_L2A_COHORTS + 2) * FIXTURE_BUILD_SECONDS > BUDGET_TARGET_SECONDS


def test_the_SHIPPED_default_it_replaced_was_over_the_target():
    """25 cohorts is ~15 minutes against a ten-minute target."""
    assert (25 + 1) * FIXTURE_BUILD_SECONDS > BUDGET_TARGET_SECONDS


def test_25_IS_GONE_from_both_entry_points():
    """R268 §3(e). At R267 the CLI defaulted to 16 while `run_probe_l2a`'s own
    signature still said 25 -- two defaults for one quantity, differing by the
    door a user came in through. The library default is the derived constant."""
    assert (inspect.signature(run_probe_l2a).parameters["max_cohorts"].default
            == DEFAULT_L2A_COHORTS)
    for rel in ("src/leakaudit/label_probe.py", "src/leakaudit/cli.py"):
        src = (ROOT / rel).read_text(encoding="utf-8")
        assert "max_cohorts: int = 25" not in src
        assert "min(max_cohorts, 25)" not in src


def test_the_budget_note_PRINTS_the_default_and_the_sum():
    note = budget_arithmetic(DEFAULT_L2A_COHORTS)
    assert "default %d" % DEFAULT_L2A_COHORTS in note
    assert "ONCE PER COHORT" in note
    assert "%.1f" % FIXTURE_BUILD_SECONDS in note
    assert str(BUDGET_TARGET_SECONDS) in note


def test_a_NON_default_budget_still_prints_the_default_beside_it():
    note = budget_arithmetic(3)
    assert "L2a cohort budget: 3" in note
    assert "default %d" % DEFAULT_L2A_COHORTS in note


# --------------------------------------------------------------------------
# §3(a)(b) -- the denominator, and the three states
# --------------------------------------------------------------------------

def test_STRIDE_EXCLUDED_seconds_ARE_counted_unprobed():
    """R268 §3(a), reversing R267. The default run's shape: 13 probed, 1,187
    eligible and not probed. That run is INCOMPLETE, and the class saying so is
    the point."""
    default_run = _cov(13, 1187)
    assert not default_run.complete
    assert default_run.cohorts_eligible == 1200


def test_the_table_has_THREE_columns_for_cohorts_AND_rows():
    t = _cov(13, 1187, ineligible=5).table()
    for header in ("probed", "eligible, unprobed", "ineligible under the model"):
        assert header in t
    assert "L3.1 cohorts" in t and "L3.1 rows" in t
    assert "COMPLETE: NO" in t


def test_a_run_complete_over_its_PROBED_cohorts_does_not_read_as_covering_ALL_rows():
    """R268 §3(b): "a run that is complete over 13 cohorts must not read as
    covering 1,200 rows". The unprobed rows are a column, not an omission."""
    t = _cov(13, 1187).table()
    assert "11870" in t, "the unprobed rows are shown"
    assert "130 (1.1%)" in t, "the probed rows are a share of all subjects"


def test_the_states_must_COVER_the_population():
    cov = _cov(10, 5, ineligible=3)
    cov.verify(18, 180)
    with pytest.raises(ValueError):
        cov.verify(19, 180)
    with pytest.raises(ValueError):
        cov.verify(18, 181)


def test_padding_rows_are_CONTEXT_counted_apart():
    cov = _cov(10, 0, context=40)
    cov.verify(10, 140)
    assert "context the builder reads" in cov.table()


def test_NO_LEVEL_is_defined_anywhere():
    """A level is a threshold, and thresholds get adjusted toward. §3(c)."""
    src = (ROOT / "src" / "leakaudit" / "coverage.py").read_text(encoding="utf-8")
    for word in ("MIN_COVERAGE", "COVERAGE_LEVEL", "REQUIRED_COVERAGE",
                 "threshold ="):
        assert word not in src, "a coverage level appeared: %s" % word


def test_L2a_NOT_RUN_does_not_make_the_audit_incomplete():
    """`unsupported` is a verdict about that row, not a coverage shortfall."""
    assert _cov(72, 0).complete


def test_L2a_eligible_is_NOT_divided_by_its_stride():
    src = (ROOT / "src" / "leakaudit" / "label_probe.py").read_text(encoding="utf-8")
    assert "res.n_eligible = len(seconds)" in src
    assert "res.n_eligible = len(seconds[::cohort_stride])" not in src


# --------------------------------------------------------------------------
# §3(d) -- the exit classes, and the pair around the L2a boundary
# --------------------------------------------------------------------------

def test_the_exit_codes_are_DISTINCT():
    codes = {cli.EXIT_OK_SILENT, cli.EXIT_FINDINGS, cli.EXIT_USAGE,
             cli.EXIT_NOTHING_PROBED, cli.EXIT_INCOMPLETE_SILENT}
    assert len(codes) == 5
    assert cli.EXIT_INCOMPLETE_SILENT != cli.EXIT_OK_SILENT


def test_BELOW_the_boundary_the_audit_is_INCOMPLETE():
    """§3's positive: L2a budget 5 of 72. HELD: L3.1 complete (72, 0)."""
    assert not _cov(72, 0, l2a_p=5, l2a_e=72).complete


def test_AT_the_boundary_the_audit_is_COMPLETE():
    """Budget >= 72. HELD: L3.1 complete, L2a eligible 72."""
    assert _cov(72, 0, l2a_p=72, l2a_e=72).complete
    assert _cov(72, 0, l2a_p=99, l2a_e=72).complete


def test_the_L2a_boundary_is_pinned_ONE_COHORT_APART():
    """HELD: L3.1 at (72, 0), L2a eligible at 72. VARIED: the L2a budget only."""
    assert not _cov(72, 0, l2a_p=71, l2a_e=72).complete
    assert _cov(72, 0, l2a_p=72, l2a_e=72).complete


def test_the_L31_boundary_is_pinned_ONE_COHORT_APART():
    """HELD: eligible at 72, L2a not run. VARIED: one cohort probed or not."""
    assert not _cov(71, 1).complete
    assert _cov(72, 0).complete


# --------------------------------------------------------------------------
# §3(e) of R267 -- the same rule at the library door
# --------------------------------------------------------------------------

def test_the_library_assertion_RAISES_on_an_incomplete_audit():
    with pytest.raises(AuditIncomplete) as e:
        assert_audit_complete(_cov(72, 0, l2a_p=5, l2a_e=72))
    assert "5 of 72" in str(e.value), "it names the row that fell short"


def test_the_library_assertion_RAISES_on_a_DEFAULT_stride_run():
    with pytest.raises(AuditIncomplete):
        assert_audit_complete(_cov(13, 1187))


def test_the_library_assertion_PASSES_with_a_DECLARED_acceptance():
    assert_audit_complete(_cov(13, 1187), accept_partial_coverage=True)


def test_the_library_assertion_PASSES_on_a_complete_audit():
    assert_audit_complete(_cov(72, 0, l2a_p=72, l2a_e=72))


def test_acceptance_is_NOT_the_default_at_either_door():
    sig = inspect.signature(assert_audit_complete)
    assert sig.parameters["accept_partial_coverage"].default is False
    src = (ROOT / "src" / "leakaudit" / "cli.py").read_text(encoding="utf-8")
    assert '"--accept-partial-coverage", action="store_true"' in src
