"""Known positives for Probe A's trace emission. R190 §2.

WHAT THIS FILE EXISTS TO STOP. `traces_for` emitted `feats[0]` -- the
alphabetically first column that moved in a cohort -- and dropped every other
one. The probe had them all; the loss was at the trace boundary, and it is
silent, because a trace with one finding where ten belong is well-formed and
resolves legally.

It is wrong in both directions that matter:

  * criterion 1 wants every ground-truth leaking source column to receive a
    finding attributed to IT. Nine of ten attributions vanish, and the criterion
    reads as nine misses that never happened.
  * criterion 2 forbids ANY finding of any tier on a manifest-clean column. A
    clean column that moved and sorts after the survivor vanishes -- a false
    negative in the direction that hides a violation.

The second is the one that makes this a defect rather than an inconvenience: a
detector whose trace can silently drop its own false positives is grading
itself. `test_a_clean_column_sorting_last_is_not_dropped` is that case, written
so that it FAILS under the old emitter.

NO FIXTURE IS TOUCHED. Every case builds a synthetic `ProbeAResult` by hand, so
the emission is tested independently of anything that takes minutes to run.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import CohortResult, ProbeAResult   # noqa: E402
from leakaudit.availability_trace import traces_for             # noqa: E402
from protocol.runtime_reference import (                        # noqa: E402
    EvidenceOutcome, PromotionStatus, ScheduleStateKind, derive_evidence_events,
    resolve_state_pair)

CASE = "synthetic_case"
T0 = pd.Timestamp("2025-01-02 14:30:00")
T1 = pd.Timestamp("2025-01-02 14:31:00")


def _result(*cohorts) -> ProbeAResult:
    return ProbeAResult(side="synthetic", n_cohorts=len(cohorts),
                        cohorts=list(cohorts))


def _cohort(second, moved, feats, rows=1) -> CohortResult:
    return CohortResult(second=second, rows_in_second=rows,
                        moved_in_second=moved, moved_next_second=0,
                        features_in_second=tuple(feats))


def _preserving(traces):
    return [t for t in traces
            if t.promotion_status is PromotionStatus.PRESERVING][0]


def _findings(trace):
    return [r.finding for r in trace.records if r.finding is not None]


# ---------------------------------------------------------------------------
# The defect, stated as a test
# ---------------------------------------------------------------------------

def test_every_moved_feature_gets_its_own_record(tmp_path):
    res = _result(_cohort(T0, moved=1, feats=("a_first", "m_middle", "z_last")))
    trace = _preserving(traces_for(res, [T0], CASE))
    assert sorted(f.feature for f in _findings(trace)) == [
        "a_first", "m_middle", "z_last"]


def test_a_clean_column_sorting_last_is_not_dropped():
    """THE CRITERION-2 CASE. Under the old emitter this trace carried one
    finding on `net_delta_1s` and the clean column's movement was invisible --
    a false positive the tool would have hidden from its own examiner."""
    res = _result(_cohort(T0, moved=3,
                          feats=("net_delta_1s", "session_open")))
    trace = _preserving(traces_for(res, [T0], CASE))
    features = {f.feature for f in _findings(trace)}
    assert "session_open" in features, (
        "a clean column moved and the trace did not say so")
    assert features == {"net_delta_1s", "session_open"}


def test_ten_required_columns_in_one_cohort_yield_ten_attributions():
    """THE CRITERION-1 CASE. One second, ten columns, ten attributions."""
    feats = tuple("net_delta_%ds" % n for n in (1, 5, 10, 30, 60)) + (
        "sell_volume_10s", "large_trade_count_10s", "vwap_distance",
        "trade_volume_1s", "trade_count_1s")
    trace = _preserving(traces_for(_result(_cohort(T0, 1, feats)), [T0], CASE))
    assert len(_findings(trace)) == 10
    assert {f.feature for f in _findings(trace)} == set(feats)


# ---------------------------------------------------------------------------
# What the repair may not have broken
# ---------------------------------------------------------------------------

def test_a_cohort_that_did_not_move_is_one_silent_record():
    trace = _preserving(traces_for(_result(_cohort(T0, 0, ())), [T0], CASE))
    assert len(trace.records) == 1 and trace.records[0].finding is None
    state, outcome = resolve_state_pair(trace)
    assert state.kind is ScheduleStateKind.COMPLETED
    assert outcome is EvidenceOutcome.OBSERVED_SILENCE


def test_repeated_cohorts_across_records_still_resolve_completed():
    """The schedule resolver takes the SET of (strategy, cohort) pairs, so
    several records per cohort leave `completed` meaning what it meant. Asserted
    rather than assumed, because the repair multiplies records per cohort."""
    res = _result(_cohort(T0, 1, ("a", "b", "c")), _cohort(T1, 0, ()))
    trace = _preserving(traces_for(res, [T0, T1], CASE))
    assert len(trace.records) == 4
    state, outcome = resolve_state_pair(trace)
    assert state.kind is ScheduleStateKind.COMPLETED
    assert outcome is EvidenceOutcome.FINDING


def test_the_cohort_list_counts_cohorts_not_records():
    res = _result(_cohort(T0, 1, ("a", "b", "c")))
    trace = _preserving(traces_for(res, [T0], CASE))
    assert len(trace.selected_eligible_cohorts) == 1
    assert len(set(trace.selected_eligible_cohorts)) == 1


def test_each_finding_carries_its_own_cohort_on_both_fields():
    res = _result(_cohort(T0, 1, ("a", "b")))
    trace = _preserving(traces_for(res, [T0], CASE))
    for r in trace.records:
        assert r.finding.probe_cohort == r.cohort_id
        assert r.finding.affected_output_cohort == r.cohort_id


def test_distinct_features_in_one_cohort_are_distinct_events():
    """The registered unit keys an event on feature and affected cohort, so
    three features in one second are three events, not one corroborated one."""
    res = _result(_cohort(T0, 1, ("a", "b", "c")))
    events = derive_evidence_events(traces_for(res, [T0], CASE))
    assert len(events) == 3
    assert {e.pair for e in events} == {
        (f, str(T0).replace(" ", "T")) for f in ("a", "b", "c")}


def test_an_ineligible_second_is_not_scheduled():
    res = _result(_cohort(T0, 1, ("a",)), _cohort(T1, 1, ("b",)))
    trace = _preserving(traces_for(res, [T0], CASE))
    assert len(trace.selected_eligible_cohorts) == 1
    assert {f.feature for f in _findings(trace)} == {"a"}


def test_movement_with_no_named_feature_raises_rather_than_inventing_one():
    res = _result(_cohort(T0, moved=7, feats=()))
    with pytest.raises(ValueError, match="named no feature"):
        traces_for(res, [T0], CASE)


def test_the_promoted_combination_is_emitted_empty_not_omitted():
    traces = traces_for(_result(_cohort(T0, 1, ("a",))), [T0], CASE)
    promoted = [t for t in traces
                if t.promotion_status is PromotionStatus.PROMOTED][0]
    state, outcome = resolve_state_pair(promoted)
    assert state.kind is ScheduleStateKind.NOT_APPLICABLE
    assert outcome is EvidenceOutcome.NONE
