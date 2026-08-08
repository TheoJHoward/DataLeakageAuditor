"""Exhaustive small-trace suite (PREREG §6.6.1): both state fields plus every
metric that reads them, per fixture, against hand-derived expectations."""

import pytest

from protocol.runtime_reference import (
    EvidenceOutcome,
    GateResult,
    MetricValue,
    PromotionStatus,
    SuppressedGate,
    SuppressedMetric,
    apply_runtime_gates,
    compute_runtime_metrics,
    derive_evidence_events,
    derive_reported_findings,
    evaluate_runtime_assertions,
    gate_id_for,
    resolve_state_pair,
)
from traces import ASSERTION_SCENARIOS, FIXTURES, PRES, PROM, SUPPRESSED


def _prefix(trace):
    return gate_id_for(trace.detector_id, trace.promotion_status)


@pytest.mark.parametrize("fx", FIXTURES, ids=lambda fx: fx.fixture_id)
def test_state_pair(fx):
    seen = {}
    for trace in fx.traces:
        state, outcome = resolve_state_pair(trace)  # legality checked inside
        seen[f"{_prefix(trace)}@{trace.case_id}"] = (state, outcome)
    # Every trace must be covered by exactly one expectation, keyed either
    # per combination (single-case fixtures) or per combination@case.
    for key, (state, outcome) in seen.items():
        prefix = key.split("@")[0]
        expected = fx.expected_pairs.get(key) or fx.expected_pairs.get(prefix)
        assert expected is not None, f"no expected pair for {key}"
        assert state.kind is expected.kind, key
        assert state.reason is expected.reason, key
        assert outcome is expected.outcome, key
    for key in fx.expected_pairs:
        assert key in seen or any(k.startswith(key + "@") for k in seen), (
            f"expected pair {key} matches no trace")


@pytest.mark.parametrize("fx", FIXTURES, ids=lambda fx: fx.fixture_id)
def test_metrics(fx):
    metrics = compute_runtime_metrics(fx.traces, fx.case_labels)
    assert set(metrics) == set(fx.expected_metrics), (
        "metric id set must match the expectation exactly — a runtime metric "
        "not computed by the reducer does not exist (PREREG §6.6.1)")
    for mid, exp in fx.expected_metrics.items():
        mv = metrics[mid]
        if exp is SUPPRESSED:
            assert isinstance(mv, SuppressedMetric), mid
            assert mv.reason, mid
            assert not hasattr(mv, "value"), mid
            continue
        assert isinstance(mv, MetricValue), mid
        num, den = exp
        assert (mv.numerator, mv.denominator) == (num, den), mid
        if den == 0:
            assert mv.value is None, mid
        else:
            assert mv.value == num / den, mid


@pytest.mark.parametrize(
    "fx", [f for f in FIXTURES if f.expected_gates or f.expected_suppressed_gates],
    ids=lambda fx: fx.fixture_id)
def test_gates(fx):
    metrics = compute_runtime_metrics(fx.traces, fx.case_labels)
    gates = apply_runtime_gates(metrics)
    for prefix, expected in fx.expected_gates.items():
        g = gates[prefix]
        assert isinstance(g, GateResult), (fx.fixture_id, prefix)
        for field_name, value in expected.items():
            assert getattr(g, field_name) == value, (fx.fixture_id, prefix, field_name)
    for prefix in fx.expected_suppressed_gates:
        g = gates[prefix]
        assert isinstance(g, SuppressedGate), (fx.fixture_id, prefix)
        assert g.reason, (fx.fixture_id, prefix)


def test_t05_events_and_reported_finding():
    fx = next(f for f in FIXTURES if f.fixture_id == "T05")
    events = derive_evidence_events(fx.traces)
    assert len(events) == 2, "one EvidenceEvent per combination (PREREG §7.2)"
    assert {e.promotion_status for e in events} == {
        PromotionStatus.PRESERVING, PromotionStatus.PROMOTED}
    gates = {
        p: GateResult(p, False, False, False, 0, 0, 0) for p in (PRES, PROM)}
    findings = derive_reported_findings(events, gates)
    assert len(findings) == 1, "one ReportedFinding for the pair (PREREG §7.2)"
    rf = findings[0]
    assert rf.tier == "PROVEN"
    assert len(rf.evidence) == 2, "the promoted event is retained as corroboration"


def test_t04_dedup_within_combination():
    """A pair found by several probes/strategies in one combination is one
    event, one true positive (PREREG §7.2)."""
    fx = next(f for f in FIXTURES if f.fixture_id == "T04")
    events = derive_evidence_events(fx.traces)
    assert len(events) == 1
    assert events[0].strategies == frozenset({"shuffle"})


@pytest.mark.parametrize("sc", ASSERTION_SCENARIOS, ids=lambda sc: sc.fixture_id)
def test_assertions(sc):
    events = derive_evidence_events(sc.traces)
    gates = {
        prefix: GateResult(prefix, experimental, experimental, False, 1,
                           1 if experimental else 0, 1)
        for prefix, experimental in sc.experimental.items()}
    result = evaluate_runtime_assertions(events, gates)
    assert result.no_proven_leakage_passed is sc.expect_pass, sc.fixture_id
    assert len(result.proven_triggering_events) == sc.expected_trigger_count
    # The merged display object retains per-event gate status and carries no
    # single inferred experimental boolean (PREREG §8.3).
    findings = derive_reported_findings(events, gates)
    assert len(findings) == 1
    rf = findings[0]
    assert not hasattr(rf, "experimental")
    statuses = {c.event.promotion_status: c.experimental for c in rf.evidence}
    assert statuses == {
        PromotionStatus.PRESERVING: sc.experimental[PRES],
        PromotionStatus.PROMOTED: sc.experimental[PROM]}


def test_t13_no_event_case_in_denominator():
    fx = next(f for f in FIXTURES if f.fixture_id == "T13")
    assert derive_evidence_events(fx.traces) == []
    metrics = compute_runtime_metrics(fx.traces, fx.case_labels)
    mv = metrics[f"{PRES}|clean_case_finding_rate"]
    assert (mv.numerator, mv.denominator) == (0, 1)
    assert mv.denominator_members == frozenset({"t13"})
    assert metrics[f"{PRES}|clean_case_finding_rate"].value == 0.0


def test_t09_short_circuited_finding_pair_is_legal():
    fx = next(f for f in FIXTURES if f.fixture_id == "T09")
    for trace in fx.traces:
        state, outcome = resolve_state_pair(trace)
        assert outcome is EvidenceOutcome.FINDING
