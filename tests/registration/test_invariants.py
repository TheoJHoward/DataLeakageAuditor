"""Mechanical invariants asserted across every fixture (PREREG §6.6.1)."""

import inspect

import pytest

import protocol.runtime_reference as rr
from protocol.runtime_reference import (
    LEGAL_PAIRS,
    CombinationTrace,
    EvidenceOutcome,
    FailureReason,
    ProtocolViolation,
    PromotionStatus,
    RunContext,
    ScheduleStateKind,
    apply_runtime_gates,
    compute_runtime_metrics,
    resolve_reach_basis,
    resolve_state_pair,
)
from protocol.runtime_reference import (
    GateResult,
    derive_evidence_events,
    derive_reported_findings,
)
from traces import FIXTURES, PRES, find, rec, tr


def _all_metrics():
    for fx in FIXTURES:
        yield fx, compute_runtime_metrics(fx.traces, fx.case_labels)


def test_legal_pairs_is_ten_of_fifteen():
    assert len(LEGAL_PAIRS) == 10
    assert len(ScheduleStateKind) * len(EvidenceOutcome) == 15
    for kind in (ScheduleStateKind.NOT_APPLICABLE, ScheduleStateKind.UNSUPPORTED):
        assert (kind, EvidenceOutcome.NONE) in LEGAL_PAIRS
        assert (kind, EvidenceOutcome.FINDING) not in LEGAL_PAIRS
        assert (kind, EvidenceOutcome.OBSERVED_SILENCE) not in LEGAL_PAIRS
    assert (ScheduleStateKind.COMPLETED, EvidenceOutcome.NONE) not in LEGAL_PAIRS


def test_every_trace_resolves_exactly_one_legal_pair():
    for fx in FIXTURES:
        for trace in fx.traces:
            state, outcome = resolve_state_pair(trace)  # raises on illegal
            assert (state.kind, outcome) in LEGAL_PAIRS
            # Determinism: the same trace resolves identically on re-run.
            assert resolve_state_pair(trace) == (state, outcome)


def test_numerators_are_subsets_by_membership():
    for fx, metrics in _all_metrics():
        for mv in metrics.values():
            if isinstance(mv, rr.SuppressedMetric):
                continue
            assert mv.numerator_members <= mv.denominator_members, mv.metric_id
            assert mv.numerator == len(mv.numerator_members)
            assert mv.denominator == len(mv.denominator_members)


def test_rates_bounded_or_none_at_zero_denominator():
    for fx, metrics in _all_metrics():
        for mv in metrics.values():
            if isinstance(mv, rr.SuppressedMetric):
                continue
            if mv.denominator == 0:
                assert mv.value is None, mv.metric_id
            else:
                assert 0.0 <= mv.value <= 1.0, mv.metric_id


def test_suppressed_metrics_carry_no_numeric_value():
    """PREREG §7.2.1 (v30): a suppressed metric is visibly suppressed and
    never renders as 0 — structurally, the record has no numerator,
    denominator, or value at all, and counts are never suppressed."""
    fields = set(rr.SuppressedMetric.__dataclass_fields__)
    assert fields == {"metric_id", "unit", "reason"}
    for fx, metrics in _all_metrics():
        for mid, mv in metrics.items():
            if isinstance(mv, rr.SuppressedMetric):
                assert not mid.endswith("_count"), (
                    f"{mid}: counts are the honest signal and are never suppressed")
                assert mv.reason
    # An all-not_applicable combination in a one-case body is suppressed…
    t15 = next(f for f in FIXTURES if f.fixture_id == "T15")
    m15 = compute_runtime_metrics(t15.traces, t15.case_labels)
    assert isinstance(m15["L3.1|preserving|proof_yield"], rr.SuppressedMetric)
    assert isinstance(m15["L3.1|preserving|not_applicable_count"], rr.MetricValue)
    # …while a mixed body publishes normally (all-or-nothing over the body).
    t18 = next(f for f in FIXTURES if f.fixture_id == "T18")
    m18 = compute_runtime_metrics(t18.traces, t18.case_labels)
    assert isinstance(m18["L3.1|promoted|evidence_yield"], rr.MetricValue)
    gates18 = apply_runtime_gates(m18)
    assert isinstance(gates18["L3.1|promoted"], rr.GateResult)


def test_gates_deterministic():
    for fx, metrics in _all_metrics():
        assert apply_runtime_gates(metrics) == apply_runtime_gates(metrics)


def test_no_runtime_metric_touches_detector_case_state():
    """The trace schema carries no detector-case coverage state (PREREG §7.7
    keeps that layer for assert_audit_complete alone), and the reducer never
    names its vocabulary."""
    # SCOPE: ONE MODULE. The population is `protocol.runtime_reference` and
    # nothing else, so a pass here says the REDUCER does not name the coverage
    # vocabulary -- not that the package does not. `could_not_run` appears in
    # `DESIGN.md` and in the amendment records by design, and a sibling module
    # acquiring it would leave this test silent. An absence claim carries its
    # population; this is that population, written down. R223 §4.
    source = inspect.getsource(rr)
    for token in ("could_not_run", "waived", "detector_case_state"):
        assert token not in source, token
    field_names = {f for f in CombinationTrace.__dataclass_fields__}
    assert "coverage_state" not in field_names
    assert "detector_case_state" not in field_names


def test_reach_basis_rule():
    assert resolve_reach_basis(6, 5, all_candidates_scanned=False) == "lower_bound"
    assert resolve_reach_basis(5, 5, all_candidates_scanned=True) == "full_scan"
    assert resolve_reach_basis(4, 5, all_candidates_scanned=False) == "lower_bound"
    with pytest.raises(ProtocolViolation):
        resolve_reach_basis(6, 5, all_candidates_scanned=True)


def test_case_level_metrics_include_no_event_cases():
    for fx, metrics in _all_metrics():
        for trace in fx.traces:
            state, _ = resolve_state_pair(trace)
            if state.kind not in (ScheduleStateKind.COMPLETED,
                                  ScheduleStateKind.INCOMPLETE):
                continue
            prefix = f"{trace.detector_id}|{trace.promotion_status.value}"
            for name in ("combination_completion_rate",
                         "combination_incompletion_rate"):
                assert trace.case_id in metrics[f"{prefix}|{name}"].denominator_members


# ---------------------------------------------------------------------------
# Traces outside the reducer's domain are rejected, not guessed at.
# ---------------------------------------------------------------------------

def test_terminal_decision_outside_user_run_is_rejected():
    trace = tr("x1", (rec("shuffle", "c1", case="x1"),),
               context=RunContext.EVALUATION, terminal=True)
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(trace)


def test_zero_selected_cohorts_resolves_not_applicable():
    """PREREG v28 §6.6 step 1, second clause: resolved strategies with no
    selected eligible cohort resolve not_applicable x none (vacuous completed
    would have to pair with none, which the table forbids)."""
    state, outcome = resolve_state_pair(tr("x2", (), cohorts=()))
    assert state.kind is ScheduleStateKind.NOT_APPLICABLE
    assert outcome is EvidenceOutcome.NONE


def test_zero_cohorts_wins_over_missing_inputs():
    """Step 1 precedes step 2: zero eligible cohorts resolves not_applicable
    even when required inputs are also missing."""
    state, _ = resolve_state_pair(tr("x2b", (), cohorts=(), inputs=False))
    assert state.kind is ScheduleStateKind.NOT_APPLICABLE


def test_zero_cohorts_with_records_is_rejected():
    bad = tr("x2c", (rec("shuffle", "c1", case="x2c"),), cohorts=())
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_every_metric_unit_is_in_the_fixed_grammar():
    """PREREG §7.0 rule 2 (v28): case, cohort, feature, feature-cohort,
    cluster, code-site, candidate."""
    assert rr.UNIT_GRAMMAR == frozenset({
        "case", "cohort", "feature", "feature_cohort", "cluster",
        "code_site", "candidate"})
    for _fx, metrics in _all_metrics():
        for mv in metrics.values():
            assert mv.unit in rr.UNIT_GRAMMAR, mv.metric_id
    with pytest.raises(ProtocolViolation):
        rr.MetricValue("x", "not_a_unit", 0, 0, None, frozenset(), frozenset(),
                       "binomial_95")


def test_record_promotion_status_must_match_combination():
    bad = tr("x3", (rec("complex", "c1", case="x3",
                        status=PromotionStatus.PROMOTED),))
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_not_applicable_with_records_is_rejected():
    bad = tr("x4", (rec("shuffle", "c1", case="x4"),), strategies=())
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_unsupported_with_records_is_rejected():
    bad = tr("x5", (rec("shuffle", "c1", case="x5"),), inputs=False)
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_valid_record_with_failure_reason_is_rejected():
    bad = tr("x6", (rec("shuffle", "c1", case="x6", valid=True,
                        reason=FailureReason.CRASH),))
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_trace_for_unlabelled_case_is_rejected():
    trace = tr("x7", (rec("shuffle", "c1", case="x7"),
                      rec("shuffle", "c2", case="x7")))
    with pytest.raises(ProtocolViolation):
        compute_runtime_metrics([trace], [])


def test_labelled_case_without_trace_is_rejected():
    """Absence is not a state: a labelled case with no trace for a
    combination would silently leave every denominator (PREREG §6.6, §7.4) —
    encode not_applicable or unsupported explicitly."""
    from traces import labels
    traced = tr("y1", (rec("shuffle", "c1", case="y1", finding=None),
                       rec("shuffle", "c2", case="y1")))
    with pytest.raises(ProtocolViolation, match="absence is not a state"):
        compute_runtime_metrics([traced], [labels("y1"), labels("y2", ("f1", "c1"))])


def test_labels_for_untraced_detector_are_rejected():
    from protocol.runtime_reference import CaseLabels
    traced = tr("y3", (rec("shuffle", "c1", case="y3"),
                       rec("shuffle", "c2", case="y3")))
    other = CaseLabels(detector_id="L2a", case_id="y3",
                       leaking_pairs=frozenset({("f1", "c1")}))
    from traces import labels
    with pytest.raises(ProtocolViolation, match="absence is not a state"):
        compute_runtime_metrics([traced], [labels("y3"), other])


def test_terminal_decision_outside_user_rejected_even_when_not_applicable():
    """The §6.6 no-short-circuit rule holds for the whole run, not per
    resolution step: a not_applicable-resolving trace claiming a terminal
    decision in an evaluation context is still malformed."""
    bad = tr("x8", (), strategies=(), context=RunContext.EVALUATION, terminal=True)
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_invalid_record_from_unresolved_strategy_is_rejected():
    """§6.6's reason precedence ranges over the combination's own strategies;
    an out-of-domain record must not be able to change incomplete's reason."""
    bad = tr("x9", (
        rec("shuffle", "c1", case="x9", valid=False,
            reason=FailureReason.COMPATIBILITY),
        rec("ghost", "c2", case="x9", valid=False,
            reason=FailureReason.DETERMINISM),
    ))
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(bad)


def test_missing_promoted_combination_is_rejected():
    """PREREG §6.6 (v29): promotion_status is a closed two-valued axis, so a
    labelled detector always has both combination rows — one absent wholesale
    must raise, and enforcement may not depend on whether some other case
    happened to trace it."""
    from traces import labels
    pres_only = tr("z1", (rec("shuffle", "c1", case="z1"),
                          rec("shuffle", "c2", case="z1")))
    with pytest.raises(ProtocolViolation, match="absence is not a state"):
        compute_runtime_metrics([pres_only], [labels("z1", ("f1", "c1"))])


def test_record_at_unselected_cohort_is_rejected():
    """The §6.6 schedule is strategies x selected cohorts; an execution at an
    unselected cohort could otherwise flip incomplete's reason or add to the
    probed set and the yields."""
    bad = tr("z2", (rec("shuffle", "c1", case="z2"),
                    rec("shuffle", "c9", case="z2", valid=False,
                        reason=FailureReason.DETERMINISM)))
    with pytest.raises(ProtocolViolation, match="not selected"):
        resolve_state_pair(bad)
    bad2 = tr("z3", (rec("shuffle", "c9", case="z3",
                         finding=find(probe="c9", affected="c1")),))
    with pytest.raises(ProtocolViolation, match="not selected"):
        resolve_state_pair(bad2)


def test_duplicate_labels_are_rejected():
    from traces import labels
    both = [tr("z4", (rec("shuffle", "c1", case="z4"),
                      rec("shuffle", "c2", case="z4"))),
            tr("z4", (), status=PromotionStatus.PROMOTED, strategies=())]
    with pytest.raises(ProtocolViolation, match="duplicate labels"):
        compute_runtime_metrics(both, [labels("z4"), labels("z4")])


def test_duplicate_trace_for_one_combination_is_rejected():
    from traces import labels
    t1 = tr("z5", (rec("shuffle", "c1", case="z5"),
                   rec("shuffle", "c2", case="z5")))
    with pytest.raises(ProtocolViolation, match="two traces"):
        compute_runtime_metrics([t1, t1], [labels("z5")])


def test_case_identity_is_not_merged_across_cases():
    """PREREG §7.2 (v29): the key applies within a case; corpus-level records
    carry case identity, so two cases reusing a (feature, cohort) name must
    not merge in events or reported findings."""
    t_a = tr("ca", (rec("shuffle", "c1", case="ca", finding=find()),))
    t_b = tr("cb", (rec("shuffle", "c1", case="cb", finding=find()),))
    events = derive_evidence_events([t_a, t_b])
    assert len(events) == 2
    gates = {PRES: GateResult(PRES, False, False, False, 0, 0, 0)}
    assert len(derive_reported_findings(events, gates)) == 2


def test_probe_cohorts_corroborate_within_one_event():
    """PREREG §7.2: probe cohorts are corroborating evidence, not additional
    events — one pair found from two probes is one event carrying both."""
    t = tr("cc", (
        rec("shuffle", "c1", case="cc", finding=find(probe="c1", affected="c1")),
        rec("shuffle", "c2", case="cc", finding=find(probe="c2", affected="c1"))))
    events = derive_evidence_events([t])
    assert len(events) == 1
    assert events[0].probe_cohorts == frozenset({"c1", "c2"})


def test_finding_probe_cohort_must_match_execution_cohort():
    """§8.4 prints the probe cohort; it may not name a probe that never ran."""
    bad = tr("z6", (rec("shuffle", "c1", case="z6",
                        finding=find(probe="c2", affected="c1")),))
    with pytest.raises(ProtocolViolation, match="probe_cohort"):
        resolve_state_pair(bad)


def test_suppressed_gate_rejects_events():
    """PREREG §7.2.1 (v30): an event implies a valid execution, so an
    all-not_applicable (suppressed) combination cannot have produced one —
    a hand-built gate table pairing a SuppressedGate with an event for the
    same combination is contradictory input and must raise, in both
    consumers of the gate table."""
    from protocol.runtime_reference import evaluate_runtime_assertions
    events = derive_evidence_events(
        [tr("g1", (rec("shuffle", "c1", case="g1", finding=find()),))])
    gates = {PRES: rr.SuppressedGate(gate_id=PRES, reason="r")}
    with pytest.raises(ProtocolViolation, match="suppressed combination"):
        evaluate_runtime_assertions(events, gates)
    with pytest.raises(ProtocolViolation, match="suppressed combination"):
        derive_reported_findings(events, gates)


def test_cross_combination_secondary_disagreement_is_rejected():
    """§7.6: secondariness is a property of the unit's position in the
    leakage DAG, not of promotion status."""
    pres = tr("z7", (rec("shuffle", "c1", case="z7", finding=find()),))
    prom = tr("z7", (rec("complex", "c1", case="z7",
                         status=PromotionStatus.PROMOTED,
                         finding=find(secondary=True)),),
              status=PromotionStatus.PROMOTED, strategies=("complex",))
    with pytest.raises(ProtocolViolation, match="secondary"):
        derive_evidence_events([pres, prom])


def test_separator_character_is_rejected_in_identifiers():
    """'|' is the reserved member/gate separator; allowing it would merge
    distinct pairs in membership sets."""
    from protocol.runtime_reference import CaseLabels, FindingRecord
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(tr("x|10", (rec("shuffle", "c1", case="x|10"),)))
    with pytest.raises(ProtocolViolation):
        resolve_state_pair(tr("x11", (
            rec("shuffle", "c1", case="x11",
                finding=FindingRecord("f|1", "c1", "c1")),)))
    with pytest.raises(ProtocolViolation):
        CaseLabels("L3.1", "x12", frozenset({("f1", "c|1")}))
