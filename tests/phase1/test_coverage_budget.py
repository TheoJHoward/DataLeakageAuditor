"""C: the budget, the two numbers, and the four exit classes. R267 §3.

The positives §3 names, plus the pair around the boundary with the cohorts held
constant — R257's rule: a pair varies exactly the thing under test and the
specification says what is held fixed. Here the frame, the builder, the stride
and the eligible set are all identical across the halves; only the budget moves.
"""
from __future__ import annotations

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


def _cov(probed, eligible, l2a_p=0, l2a_e=0):
    return Coverage(cohorts_probed=probed, cohorts_eligible=eligible,
                    rows_in_probed=probed * 10, rows_total=eligible * 10,
                    l2a_probed=l2a_p, l2a_eligible=l2a_e)


# --------------------------------------------------------------------------
# §3(b) -- the default is a COST choice and is printed as one
# --------------------------------------------------------------------------

def test_the_default_is_DERIVED_from_the_measured_build_time():
    """Not picked. `(N + 1) * build <= target` is the whole of it."""
    assert (DEFAULT_L2A_COHORTS + 1) * FIXTURE_BUILD_SECONDS <= BUDGET_TARGET_SECONDS
    # and it is the LARGEST such N -- one more would breach the target, so the
    # number is determined rather than merely consistent.
    assert (DEFAULT_L2A_COHORTS + 2) * FIXTURE_BUILD_SECONDS > BUDGET_TARGET_SECONDS


def test_the_SHIPPED_default_it_replaced_was_over_the_target():
    """R267 measured this: 25 cohorts is ~15 minutes, not ten.

    Recorded as a test because the old number was not wrong by opinion -- it
    was wrong by an arithmetic nobody had written down.
    """
    assert (25 + 1) * FIXTURE_BUILD_SECONDS > BUDGET_TARGET_SECONDS


def test_the_budget_note_PRINTS_the_default_and_the_sum():
    note = budget_arithmetic(DEFAULT_L2A_COHORTS)
    assert "default %d" % DEFAULT_L2A_COHORTS in note
    assert "ONCE PER COHORT" in note
    assert "%.1f" % FIXTURE_BUILD_SECONDS in note, "the build time is shown"
    assert str(BUDGET_TARGET_SECONDS) in note, "the target is shown"


def test_a_NON_default_budget_still_prints_the_default_beside_it():
    """Or a reader cannot tell a chosen number from the shipped one."""
    note = budget_arithmetic(3)
    assert "L2a cohort budget: 3" in note
    assert "default %d" % DEFAULT_L2A_COHORTS in note


# --------------------------------------------------------------------------
# §3(c) -- coverage is reported, never thresholded
# --------------------------------------------------------------------------

def test_the_table_carries_BOTH_numbers_and_names_the_budgeted_row():
    t = _cov(5, 72, l2a_p=5, l2a_e=72).table()
    assert "5 of 72" in t
    assert "rows in those cohorts" in t
    assert "budgeted row" in t, "a reader must know which row the budget binds"
    assert "not thresholded" in t


def test_NO_LEVEL_is_defined_anywhere():
    """A level is a threshold, and thresholds get adjusted toward. §3(c)."""
    src = (ROOT / "src" / "leakaudit" / "coverage.py").read_text(encoding="utf-8")
    for word in ("MIN_COVERAGE", "COVERAGE_LEVEL", "REQUIRED_COVERAGE",
                 "threshold ="):
        assert word not in src, "a coverage level appeared: %s" % word


def test_L2a_NOT_RUN_does_not_make_the_audit_incomplete():
    """`unsupported` is a verdict about that row, not a coverage shortfall."""
    assert _cov(72, 72, l2a_p=0, l2a_e=0).complete


def test_the_stride_is_NOT_counted_as_a_shortfall():
    """The denominator is the separation-eligible set. R267.

    Counting stride-excluded seconds as unprobed would report a gap no budget
    could close, and an incomplete class that fires on every run is one that
    distinguishes nothing.
    """
    assert _cov(72, 72).complete


# --------------------------------------------------------------------------
# §3(d) -- four classes, and the pair around the boundary
# --------------------------------------------------------------------------

def test_the_four_exit_codes_are_DISTINCT():
    codes = {cli.EXIT_OK_SILENT, cli.EXIT_FINDINGS, cli.EXIT_USAGE,
             cli.EXIT_NOTHING_PROBED, cli.EXIT_INCOMPLETE_SILENT}
    assert len(codes) == 5, "complete-silent, finding, refused, nothing-probed "\
                            "and incomplete-silent are five distinct answers"
    assert cli.EXIT_INCOMPLETE_SILENT != cli.EXIT_OK_SILENT


def test_BELOW_the_boundary_the_audit_is_INCOMPLETE():
    """§3's positive: budget 5 of 72."""
    assert not _cov(72, 72, l2a_p=5, l2a_e=72).complete


def test_AT_the_boundary_the_audit_is_COMPLETE():
    """§3's positive: budget >= 72. The pair holds the eligible set at 72."""
    assert _cov(72, 72, l2a_p=72, l2a_e=72).complete
    assert _cov(72, 72, l2a_p=99, l2a_e=72).complete


def test_the_boundary_is_pinned_ONE_COHORT_APART():
    """The pair, with everything but the budget held fixed. R257's rule."""
    assert not _cov(72, 72, l2a_p=71, l2a_e=72).complete
    assert _cov(72, 72, l2a_p=72, l2a_e=72).complete


# --------------------------------------------------------------------------
# §3(e) -- the same rule at the library door
# --------------------------------------------------------------------------

def test_the_library_assertion_RAISES_on_an_incomplete_audit():
    with pytest.raises(AuditIncomplete) as e:
        assert_audit_complete(_cov(72, 72, l2a_p=5, l2a_e=72))
    assert "5 of 72" in str(e.value), "it names the numbers, not just the state"


def test_the_library_assertion_PASSES_with_a_DECLARED_acceptance():
    assert_audit_complete(_cov(72, 72, l2a_p=5, l2a_e=72),
                          accept_partial_coverage=True)


def test_the_library_assertion_PASSES_on_a_complete_audit():
    assert_audit_complete(_cov(72, 72, l2a_p=72, l2a_e=72))


def test_acceptance_is_NOT_the_default_at_either_door():
    """A rule enforced at one of two entry points is a rule with a bypass."""
    import inspect
    sig = inspect.signature(assert_audit_complete)
    assert sig.parameters["accept_partial_coverage"].default is False
    src = (ROOT / "src" / "leakaudit" / "cli.py").read_text(encoding="utf-8")
    assert '"--accept-partial-coverage", action="store_true"' in src, (
        "the CLI flag must default to off, or the declaration is not a "
        "declaration")
