"""Reference reducers for the leakaudit runtime protocol.

Normative source: PREREG.md v30. This module is built FROM that file and is
checked AGAINST it (PREREG §6.6.1). It is pure protocol tooling: no I/O, no
randomness, no pandas, no detector implementation. Where this module and the
prose disagree, the disagreement blocks the tag and is routed per the build
protocol -- the reducer detects, it does not adjudicate.

Requirement IDs implemented here (labels for existing PREREG clauses; the
convention is fixed and introduces no new semantics):

    R6.6-SCHEDULE-RESOLUTION         resolve_schedule_state
    R6.6-EVIDENCE-OUTCOME            resolve_evidence_outcome
    R6.6-LEGAL-PAIRS                 LEGAL_PAIRS / check_pair_legal
    R7.2-PROOF-YIELD                 compute_runtime_metrics
    R7.2-EVIDENCE-YIELD              compute_runtime_metrics
    R7.2-CONDITIONAL-RECALL          compute_runtime_metrics
    R7.2-COHORT-SENSITIVITY          compute_runtime_metrics
    R7.2-DISCOVERY-RECALL            compute_runtime_metrics
    R7.2-UNPROBED-RATE               compute_runtime_metrics
    R7.2.1-FEATURE-COHORT-PRECISION  compute_runtime_metrics
    R7.2.1-COMPLETION-RATE           compute_runtime_metrics
    R7.2.1-INCOMPLETION-RATE         compute_runtime_metrics
    R7.7-CLEAN-FINDING-RATE          compute_runtime_metrics
    R10.2-RUNTIME-GATES              apply_runtime_gates
    R8.3-PROVEN-ASSERTION            evaluate_runtime_assertions

Deliberately outside this reference reducer (build-brief scope; PREREG §11
lists the seven functions above as the minimum): §7.5's per-strategy
diagnostics and §6.11's compatibility-escalation arithmetic. Per §6.6.1 a
runtime number is publishable only once the reducer computes it, so neither
may be published until this module grows them.

The §7.2 keys apply within a case; corpus-level records additionally carry
case identity (PREREG §7.2, v29), because two cases may reuse a
(feature, cohort) name and must not merge. The extension adds no semantics
within a single case.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Mapping


class ProtocolViolation(Exception):
    """A trace, pair, or input outside the domain PREREG.md defines."""


# ---------------------------------------------------------------------------
# Vocabulary (PREREG §3.1, §6.6, §8.2)
# ---------------------------------------------------------------------------

class PromotionStatus(str, Enum):
    PRESERVING = "preserving"
    PROMOTED = "promoted"


class RunContext(str, Enum):
    EVALUATION = "evaluation"
    CONFORMANCE = "conformance"
    FIXTURE = "fixture"
    USER = "user"


class FailureReason(str, Enum):
    DETERMINISM = "determinism"
    ALIGNMENT = "alignment"
    COMPATIBILITY = "compatibility"
    CONTROL_ARTIFACT = "control_artifact"
    CRASH = "crash"


# PREREG §6.6: reason precedence when strategies fail differently.
REASON_PRECEDENCE: tuple[FailureReason, ...] = (
    FailureReason.DETERMINISM,
    FailureReason.ALIGNMENT,
    FailureReason.COMPATIBILITY,
    FailureReason.CONTROL_ARTIFACT,
    FailureReason.CRASH,
)


class ScheduleStateKind(str, Enum):
    NOT_APPLICABLE = "not_applicable"
    UNSUPPORTED = "unsupported"
    SHORT_CIRCUITED = "short_circuited"
    COMPLETED = "completed"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class ScheduleState:
    kind: ScheduleStateKind
    reason: FailureReason | None = None

    def __post_init__(self) -> None:
        if self.kind is ScheduleStateKind.INCOMPLETE and self.reason is None:
            raise ProtocolViolation("incomplete requires a reason (PREREG §6.6)")
        if self.kind is not ScheduleStateKind.INCOMPLETE and self.reason is not None:
            raise ProtocolViolation("only incomplete carries a reason (PREREG §6.6)")


class EvidenceOutcome(str, Enum):
    FINDING = "finding"
    OBSERVED_SILENCE = "observed_silence"
    NONE = "none"


# PREREG §6.6: ten of fifteen pairs are legal.  [R6.6-LEGAL-PAIRS]
LEGAL_PAIRS: frozenset[tuple[ScheduleStateKind, EvidenceOutcome]] = frozenset({
    (ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE),
    (ScheduleStateKind.UNSUPPORTED, EvidenceOutcome.NONE),
    (ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.FINDING),
    (ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.OBSERVED_SILENCE),
    (ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.NONE),
    (ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
    (ScheduleStateKind.COMPLETED, EvidenceOutcome.OBSERVED_SILENCE),
    (ScheduleStateKind.INCOMPLETE, EvidenceOutcome.FINDING),
    (ScheduleStateKind.INCOMPLETE, EvidenceOutcome.OBSERVED_SILENCE),
    (ScheduleStateKind.INCOMPLETE, EvidenceOutcome.NONE),
})


# ---------------------------------------------------------------------------
# Trace schema (build brief §1; facts may not be dropped)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FindingRecord:
    feature: str
    probe_cohort: str
    affected_output_cohort: str
    is_secondary: bool = False


@dataclass(frozen=True)
class ExecutionRecord:
    detector_id: str
    case_id: str
    strategy_id: str
    promotion_status: PromotionStatus
    cohort_id: str
    attempted: bool
    valid: bool
    finding: FindingRecord | None = None
    failure_reason: FailureReason | None = None


@dataclass(frozen=True)
class CombinationTrace:
    detector_id: str
    case_id: str
    promotion_status: PromotionStatus
    run_context: RunContext
    resolved_strategies: tuple[str, ...]
    selected_eligible_cohorts: tuple[str, ...]
    required_inputs_available: bool
    terminal_decision_occurred: bool
    records: tuple[ExecutionRecord, ...]


def _no_separator(*values: str) -> None:
    for v in values:
        if "|" in v:
            raise ProtocolViolation(
                f"identifier {v!r} contains '|', the reserved member/gate "
                "separator; distinct units would collide in membership sets")


def _validate_trace(trace: CombinationTrace) -> None:
    _no_separator(trace.detector_id, trace.case_id, *trace.resolved_strategies,
                  *trace.selected_eligible_cohorts)
    if trace.terminal_decision_occurred and trace.run_context is not RunContext.USER:
        # §6.6: no terminal short-circuit in evaluation, conformance, or the
        # fixture gate run — the condition is illegal for the whole run, not
        # merely for the states that would read it.
        raise ProtocolViolation(
            "terminal short-circuit outside a user run violates PREREG §6.6")
    for r in trace.records:
        if (r.detector_id, r.case_id) != (trace.detector_id, trace.case_id):
            raise ProtocolViolation("record does not belong to this trace")
        if r.promotion_status is not trace.promotion_status:
            raise ProtocolViolation(
                "record promotion status differs from its combination; promotion "
                "is per strategy per frame and keys the combination (PREREG §3.2, §6.6)")
        if r.valid and not r.attempted:
            raise ProtocolViolation("valid execution must have been attempted")
        if r.valid and r.failure_reason is not None:
            raise ProtocolViolation("valid execution cannot carry a failure reason")
        if r.strategy_id not in trace.resolved_strategies:
            # §6.6's schedule and reason precedence range over the strategies
            # resolved to this combination; a record from any other strategy
            # is outside the trace's own schema, valid or not.
            raise ProtocolViolation(
                "execution record from a strategy not resolved to this combination")
        if r.cohort_id not in trace.selected_eligible_cohorts:
            # The schedule is the product of both axes (§6.6: every configured
            # strategy at every selected eligible cohort); an execution at an
            # unselected cohort is outside the trace's own schema and could
            # otherwise move probed sets, yields, and incomplete's reason.
            raise ProtocolViolation(
                "execution record at a cohort not selected for this combination")
        _no_separator(r.strategy_id, r.cohort_id)
        if r.finding is not None:
            _no_separator(r.finding.feature, r.finding.probe_cohort,
                          r.finding.affected_output_cohort)
            if r.finding.probe_cohort != r.cohort_id:
                # The probe that produced a finding is the execution it rode
                # on; §8.4 prints the probe cohort, so it may not name a
                # probe that never ran.
                raise ProtocolViolation(
                    "finding's probe_cohort differs from its executing "
                    "record's cohort")
    if not trace.resolved_strategies and trace.records:
        raise ProtocolViolation(
            "not_applicable combination cannot carry execution records (PREREG §6.6)")
    if not trace.selected_eligible_cohorts and trace.records:
        raise ProtocolViolation(
            "a combination with no selected eligible cohorts scheduled nothing "
            "and cannot carry execution records (PREREG §6.6)")
    if not trace.required_inputs_available and trace.records:
        raise ProtocolViolation(
            "unsupported combination cannot carry execution records (PREREG §6.6)")


def _valid_records(trace: CombinationTrace) -> tuple[ExecutionRecord, ...]:
    return tuple(r for r in trace.records if r.attempted and r.valid)


def _schedule_slots(trace: CombinationTrace) -> frozenset[tuple[str, str]]:
    return frozenset(
        (s, c) for s in trace.resolved_strategies for c in trace.selected_eligible_cohorts)


def _schedule_complete(trace: CombinationTrace) -> bool:
    done = {(r.strategy_id, r.cohort_id) for r in _valid_records(trace)}
    return _schedule_slots(trace) <= done


# ---------------------------------------------------------------------------
# The two resolvers (PREREG §6.6)
# ---------------------------------------------------------------------------

def resolve_schedule_state(trace: CombinationTrace) -> ScheduleState:
    """PREREG §6.6 resolution order.  [R6.6-SCHEDULE-RESOLUTION]"""
    _validate_trace(trace)
    if not trace.resolved_strategies or not trace.selected_eligible_cohorts:
        # §6.6 step 1 (v28): no strategy resolves to this status, OR no
        # eligible cohort was selected for it. The second clause covers a
        # combination with resolved strategies, available inputs, and nothing
        # to do -- vacuous completed would have to pair with none, which the
        # legality table forbids.
        return ScheduleState(ScheduleStateKind.NOT_APPLICABLE)
    if not trace.required_inputs_available:
        return ScheduleState(ScheduleStateKind.UNSUPPORTED)
    complete = _schedule_complete(trace)
    # _validate_trace guarantees terminal_decision_occurred implies a user run.
    if trace.terminal_decision_occurred and not complete:
        return ScheduleState(ScheduleStateKind.SHORT_CIRCUITED)
    if complete:
        return ScheduleState(ScheduleStateKind.COMPLETED)
    return ScheduleState(ScheduleStateKind.INCOMPLETE, reason=_incomplete_reason(trace))


def _incomplete_reason(trace: CombinationTrace) -> FailureReason:
    recorded = {
        r.failure_reason for r in trace.records
        if r.attempted and not r.valid and r.failure_reason is not None}
    for reason in REASON_PRECEDENCE:
        if reason in recorded:
            return reason
    # Schedule slots missing with no recorded failure: the process died before
    # emitting anything. Absence of records never carries a second meaning.
    return FailureReason.CRASH


def resolve_evidence_outcome(trace: CombinationTrace) -> EvidenceOutcome:
    """PREREG §6.6, total over every trace.  [R6.6-EVIDENCE-OUTCOME]"""
    _validate_trace(trace)
    valid = _valid_records(trace)
    if any(r.finding is not None for r in valid):
        return EvidenceOutcome.FINDING
    if valid:
        return EvidenceOutcome.OBSERVED_SILENCE
    return EvidenceOutcome.NONE


def check_pair_legal(state: ScheduleState, outcome: EvidenceOutcome) -> None:
    """PREREG §6.6 legality table.  [R6.6-LEGAL-PAIRS]"""
    if (state.kind, outcome) not in LEGAL_PAIRS:
        raise ProtocolViolation(
            f"illegal pair under PREREG §6.6: {state.kind.value} x {outcome.value}")


def resolve_state_pair(trace: CombinationTrace) -> tuple[ScheduleState, EvidenceOutcome]:
    state = resolve_schedule_state(trace)
    outcome = resolve_evidence_outcome(trace)
    check_pair_legal(state, outcome)
    return state, outcome


# ---------------------------------------------------------------------------
# Evidence events and reported findings (PREREG §7.2, §3.1, §8.3)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EvidenceEvent:
    detector_id: str
    case_id: str
    promotion_status: PromotionStatus
    feature: str
    affected_output_cohort: str
    probe_cohorts: frozenset[str]
    strategies: frozenset[str]
    is_secondary: bool

    @property
    def licenses_proven(self) -> bool:
        # PREREG §3.1: preserving -> PROVEN; promoted -> REVIEW dtype_promoted.
        return self.promotion_status is PromotionStatus.PRESERVING

    @property
    def pair(self) -> tuple[str, str]:
        return (self.feature, self.affected_output_cohort)


def derive_evidence_events(traces: Iterable[CombinationTrace]) -> list[EvidenceEvent]:
    """One event per combination per (feature, affected cohort); probes,
    strategies, and repeated runs within a combination corroborate rather than
    multiply (PREREG §7.2)."""
    acc: dict[tuple, dict] = {}
    for trace in traces:
        _validate_trace(trace)
        for r in _valid_records(trace):
            if r.finding is None:
                continue
            key = (trace.detector_id, trace.case_id, trace.promotion_status,
                   r.finding.feature, r.finding.affected_output_cohort)
            slot = acc.setdefault(
                key, {"probes": set(), "strategies": set(), "secondary": set()})
            slot["probes"].add(r.finding.probe_cohort)
            slot["strategies"].add(r.strategy_id)
            slot["secondary"].add(r.finding.is_secondary)
    # §7.6: secondariness is a property of the unit's position in the leakage
    # DAG, not of promotion status — contradictory input across combinations
    # is rejected, not surfaced as two events that disagree.
    by_pair: dict[tuple, set[bool]] = {}
    for (detector, case, _status, feature, cohort), slot in acc.items():
        by_pair.setdefault((detector, case, feature, cohort), set()).update(
            slot["secondary"])
    for pair_key, vals in by_pair.items():
        if len(vals) > 1:
            raise ProtocolViolation(
                f"pair {pair_key} recorded primary in one combination and "
                "secondary in another (PREREG §7.6)")
    events = []
    for key in sorted(acc, key=lambda k: (k[0], k[1], k[2].value, k[3], k[4])):
        detector, case, status, feature, cohort = key
        slot = acc[key]
        if len(slot["secondary"]) != 1:
            raise ProtocolViolation(
                "one pair recorded as both primary and secondary within a "
                "combination (PREREG §7.6)")
        events.append(EvidenceEvent(
            detector_id=detector, case_id=case, promotion_status=status,
            feature=feature, affected_output_cohort=cohort,
            probe_cohorts=frozenset(slot["probes"]),
            strategies=frozenset(slot["strategies"]),
            is_secondary=next(iter(slot["secondary"]))))
    return events


def gate_id_for(detector_id: str, status: PromotionStatus) -> str:
    return f"{detector_id}|{status.value}"


@dataclass(frozen=True)
class ConstituentEvidence:
    event: EvidenceEvent
    experimental: bool  # gate status of the event's combination (PREREG §8.3)


@dataclass(frozen=True)
class ReportedFinding:
    """Display unit, keyed (detector, feature, affected cohort) per case.
    Carries the highest tier its events justify and retains the gate status
    of EACH constituent event -- no single inferred experimental boolean
    (PREREG §7.2, §8.3)."""
    detector_id: str
    case_id: str
    feature: str
    affected_output_cohort: str
    tier: str  # "PROVEN" | "REVIEW"
    evidence: tuple[ConstituentEvidence, ...]


def derive_reported_findings(
    events: Iterable[EvidenceEvent],
    gate_results: Mapping[str, "GateResult | SuppressedGate"],
) -> list[ReportedFinding]:
    groups: dict[tuple, list[EvidenceEvent]] = {}
    for e in events:
        groups.setdefault(
            (e.detector_id, e.case_id, e.feature, e.affected_output_cohort), []).append(e)
    findings = []
    for key in sorted(groups):
        detector, case, feature, cohort = key
        constituents = []
        for e in sorted(groups[key], key=lambda e: e.promotion_status.value):
            gid = gate_id_for(e.detector_id, e.promotion_status)
            if gid not in gate_results:
                raise ProtocolViolation(f"no gate status for combination {gid} (PREREG §8.3)")
            gate = gate_results[gid]
            if isinstance(gate, SuppressedGate):
                # An event implies a valid execution, which implies a
                # non-not_applicable state on that case — an all-na
                # combination cannot have produced it.
                raise ProtocolViolation(
                    f"event from suppressed combination {gid} is contradictory "
                    "input (PREREG §7.2.1)")
            constituents.append(ConstituentEvidence(
                event=e, experimental=gate.experimental))
        tier = "PROVEN" if any(c.event.licenses_proven for c in constituents) else "REVIEW"
        findings.append(ReportedFinding(
            detector_id=detector, case_id=case, feature=feature,
            affected_output_cohort=cohort, tier=tier, evidence=tuple(constituents)))
    return findings


# ---------------------------------------------------------------------------
# Labels and metric values (PREREG §7.2, §7.2.1, §7.7)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CaseLabels:
    detector_id: str
    case_id: str
    leaking_pairs: frozenset[tuple[str, str]]  # (feature, affected output cohort)

    def __post_init__(self) -> None:
        _no_separator(self.detector_id, self.case_id,
                      *(v for pair in self.leaking_pairs for v in pair))

    @property
    def is_clean(self) -> bool:
        return not self.leaking_pairs


# PREREG §7.0 rule 2 (v28): the fixed unit grammar, `feature` included.
UNIT_GRAMMAR: frozenset[str] = frozenset({
    "case", "cohort", "feature", "feature_cohort", "cluster", "code_site",
    "candidate"})


@dataclass(frozen=True)
class MetricValue:
    metric_id: str
    unit: str  # member of UNIT_GRAMMAR (PREREG §7.0 rule 2)
    numerator: int
    denominator: int
    value: float | None
    numerator_members: frozenset[str]
    denominator_members: frozenset[str]
    interval_method: str

    def __post_init__(self) -> None:
        if self.unit not in UNIT_GRAMMAR:
            raise ProtocolViolation(
                f"{self.metric_id}: unit {self.unit!r} is outside the fixed "
                "grammar of PREREG §7.0 rule 2")
        if len(self.numerator_members) != self.numerator:
            raise ProtocolViolation(f"{self.metric_id}: numerator does not match its member set")
        if len(self.denominator_members) != self.denominator:
            raise ProtocolViolation(f"{self.metric_id}: denominator does not match its member set")
        if not self.numerator_members <= self.denominator_members:
            raise ProtocolViolation(
                f"{self.metric_id}: numerator members are not a subset of "
                "denominator members (PREREG §6.6.1)")
        if self.denominator == 0 and self.value is not None:
            raise ProtocolViolation(f"{self.metric_id}: value must be None at a zero denominator")
        if self.denominator > 0 and self.value != self.numerator / self.denominator:
            raise ProtocolViolation(f"{self.metric_id}: value does not equal numerator/denominator")


@dataclass(frozen=True)
class SuppressedMetric:
    """PREREG §7.2.1 (v30): a combination that is not_applicable on every
    scope-eligible case in a body publishes its counts and suppresses its
    yields, rates, and gates, naming the reason. A suppressed metric never
    carries a numeric value — this record deliberately has no numerator,
    denominator, or value, so it cannot render as 0."""
    metric_id: str
    unit: str
    reason: str

    def __post_init__(self) -> None:
        if self.unit not in UNIT_GRAMMAR:
            raise ProtocolViolation(
                f"{self.metric_id}: unit {self.unit!r} is outside the fixed "
                "grammar of PREREG §7.0 rule 2")
        if not self.reason:
            raise ProtocolViolation(
                f"{self.metric_id}: a suppression without a reason is not "
                "visibly suppressed (PREREG §7.2.1)")


@dataclass(frozen=True)
class SuppressedGate:
    """The gate of an all-not_applicable combination is suppressed with its
    metrics (PREREG §7.2.1, v30)."""
    gate_id: str
    reason: str


_BINOMIAL = "binomial_95 (PREREG §7.10)"
_BOOTSTRAP = "case_clustered_bootstrap_95 (PREREG §7.10)"
_COUNT = "descriptive_count_no_interval (PREREG §7.2.1)"


def _metric(metric_id: str, unit: str, num: frozenset[str], den: frozenset[str],
            interval: str) -> MetricValue:
    return MetricValue(
        metric_id=metric_id, unit=unit,
        numerator=len(num), denominator=len(den),
        value=(len(num) / len(den)) if den else None,
        numerator_members=num, denominator_members=den,
        interval_method=interval)


# ---------------------------------------------------------------------------
# Runtime metrics (PREREG §7.1, §7.2, §7.2.1, §7.7)
# ---------------------------------------------------------------------------

def compute_runtime_metrics(
    traces: Iterable[CombinationTrace],
    labels: Iterable[CaseLabels],
) -> dict[str, "MetricValue | SuppressedMetric"]:
    """Every published runtime metric (PREREG §6.6.1: a number absent here
    does not exist). No metric reads the detector-case state of §7.7 -- the
    trace schema carries none, so the assertion holds by construction and is
    checked mechanically by the suite."""
    traces = list(traces)
    label_index: dict[tuple[str, str], CaseLabels] = {}
    for lab in labels:
        key = (lab.detector_id, lab.case_id)
        if key in label_index:
            raise ProtocolViolation(f"duplicate labels for {key}")
        label_index[key] = lab

    combos: dict[tuple[str, PromotionStatus], dict[str, CombinationTrace]] = {}
    for t in traces:
        if (t.detector_id, t.case_id) not in label_index:
            raise ProtocolViolation(
                f"trace for unlabelled case {(t.detector_id, t.case_id)}: every "
                "evaluation case carries labels")
        per_case = combos.setdefault((t.detector_id, t.promotion_status), {})
        if t.case_id in per_case:
            raise ProtocolViolation(
                f"two traces for one combination on case {t.case_id}")
        per_case[t.case_id] = t

    # PREREG §6.6 (v29): every labelled case carries an explicit trace for
    # EVERY combination — a missing trace is a protocol violation and must
    # raise, never default. promotion_status is a closed two-valued axis
    # (§3.1), so a labelled detector always has both combination rows; a
    # combination absent wholesale would silently publish no row at all,
    # and enforcement must not depend on whether some other case happened
    # to trace it. Encode not_applicable/unsupported explicitly.
    labelled_detectors = {d for (d, _c) in label_index}
    for detector in sorted(labelled_detectors):
        for status in PromotionStatus:
            if (detector, status) not in combos:
                raise ProtocolViolation(
                    f"no trace for combination {gate_id_for(detector, status)} "
                    "on a labelled detector: absence is not a state — a "
                    "missing trace must raise, never default (PREREG §6.6)")
    for (detector, _status), per_case in sorted(
            combos.items(), key=lambda kv: (kv[0][0], kv[0][1].value)):
        for (lab_detector, case) in sorted(label_index):
            if lab_detector == detector and case not in per_case:
                raise ProtocolViolation(
                    f"labelled case {case} has no trace for combination "
                    f"{gate_id_for(detector, _status)}: absence is not a "
                    "state (PREREG §6.6); encode not_applicable or "
                    "unsupported explicitly")

    out: dict[str, MetricValue | SuppressedMetric] = {}
    for (detector, status), per_case in sorted(
            combos.items(), key=lambda kv: (kv[0][0], kv[0][1].value)):
        out.update(_combo_metrics(detector, status, per_case, label_index))
    return out


def _combo_metrics(
    detector: str,
    status: PromotionStatus,
    per_case: dict[str, CombinationTrace],
    label_index: dict[tuple[str, str], CaseLabels],
) -> dict[str, "MetricValue | SuppressedMetric"]:
    prefix = f"{detector}|{status.value}"
    states: dict[str, ScheduleState] = {}
    outcomes: dict[str, EvidenceOutcome] = {}
    for case, trace in per_case.items():
        st, oc = resolve_state_pair(trace)
        states[case], outcomes[case] = st, oc

    # PREREG §6.6: short_circuited is excluded from every metric denominator.
    # (It cannot arise in an evaluation run, so no published number moves.)
    sc_cases = {c for c, s in states.items() if s.kind is ScheduleStateKind.SHORT_CIRCUITED}
    scored_cases = {c for c in per_case if c not in sc_cases}

    # PREREG §7.7: execution-eligible membership, defined directly on the state.
    in_den = {c for c, s in states.items()
              if s.kind in (ScheduleStateKind.COMPLETED, ScheduleStateKind.INCOMPLETE)}
    completed = {c for c, s in states.items() if s.kind is ScheduleStateKind.COMPLETED}
    incomplete = {c for c, s in states.items() if s.kind is ScheduleStateKind.INCOMPLETE}

    def pid(case: str, feature: str, cohort: str) -> str:
        return f"{case}|{feature}|{cohort}"

    # Pair-level scope-eligible denominator (PREREG §7.2: "the pair stays in"
    # for every non-proving outcome; §7.4 distinguishes it from the
    # execution-eligible case denominators above).
    scope_pairs = {
        pid(c, f, coh)
        for c in scored_cases
        for (f, coh) in label_index[(detector, c)].leaking_pairs}

    events = [e for e in derive_evidence_events(per_case.values())
              if e.case_id in scored_cases]
    def correct(e: EvidenceEvent) -> bool:
        return e.pair in label_index[(detector, e.case_id)].leaking_pairs
    primary = [e for e in events if not e.is_secondary]
    correct_pair_ids = {
        pid(e.case_id, e.feature, e.affected_output_cohort)
        for e in primary if correct(e)}
    false_event_ids = {
        pid(e.case_id, e.feature, e.affected_output_cohort)
        for e in primary if not correct(e)}

    probed: dict[str, frozenset[str]] = {
        c: frozenset(r.cohort_id for r in _valid_records(t))
        for c, t in per_case.items()}

    m: dict[str, MetricValue] = {}

    # [R7.2-PROOF-YIELD] / [R7.2-EVIDENCE-YIELD] -- same denominator, own
    # numerator, the names never interchanged (PREREG §7.1, §7.2).
    yield_name = "proof_yield" if status is PromotionStatus.PRESERVING else "evidence_yield"
    m[f"{prefix}|{yield_name}"] = _metric(
        f"{prefix}|{yield_name}", "feature_cohort",
        correct_pair_ids & scope_pairs, frozenset(scope_pairs), _BOOTSTRAP)

    # [R7.2-CONDITIONAL-RECALL] -- numerator AND denominator restricted to
    # cases whose schedule_state is completed.
    completed_pairs = {
        pid(c, f, coh) for c in completed
        for (f, coh) in label_index[(detector, c)].leaking_pairs}
    m[f"{prefix}|conditional_feature_cohort_recall"] = _metric(
        f"{prefix}|conditional_feature_cohort_recall", "feature_cohort",
        correct_pair_ids & completed_pairs, frozenset(completed_pairs), _BOOTSTRAP)

    # [R7.2-COHORT-SENSITIVITY] -- probed cohorts containing >=1 labelled
    # leaking feature; probed is combination-level (PREREG §6.11).
    def cid(case: str, cohort: str) -> str:
        return f"{case}|{cohort}"
    leaky_cohorts = {
        (c, coh) for c in scored_cases
        for (_f, coh) in label_index[(detector, c)].leaking_pairs}
    probed_leaky = {cid(c, coh) for (c, coh) in leaky_cohorts if coh in probed[c]}
    hit_cohorts = {
        cid(e.case_id, e.affected_output_cohort)
        for e in primary if correct(e)}
    m[f"{prefix}|cohort_sensitivity"] = _metric(
        f"{prefix}|cohort_sensitivity", "cohort",
        hit_cohorts & probed_leaky, frozenset(probed_leaky), _BOOTSTRAP)

    # [R7.2-DISCOVERY-RECALL] -- labelled leaking features found in >=1
    # cohort; secondary, never quoted alone. Unit "feature", added to the
    # grammar by v28 (PREREG §7.0 rule 2).
    def fid(case: str, feature: str) -> str:
        return f"{case}|{feature}"
    labelled_features = {
        fid(c, f) for c in scored_cases
        for (f, _coh) in label_index[(detector, c)].leaking_pairs}
    found_features = {fid(e.case_id, e.feature) for e in primary if correct(e)}
    m[f"{prefix}|feature_discovery_recall"] = _metric(
        f"{prefix}|feature_discovery_recall", "feature",
        found_features & labelled_features, frozenset(labelled_features), _BOOTSTRAP)

    # [R7.2-UNPROBED-RATE] -- labelled pairs whose affected cohort was not
    # itself probed; a coverage statistic, independent of incidental detection.
    unprobed = {
        pid(c, f, coh) for c in scored_cases
        for (f, coh) in label_index[(detector, c)].leaking_pairs
        if coh not in probed[c]}
    m[f"{prefix}|unprobed_feature_cohort_rate"] = _metric(
        f"{prefix}|unprobed_feature_cohort_rate", "feature_cohort",
        unprobed, frozenset(scope_pairs), _BOOTSTRAP)

    # [R7.2.1-FEATURE-COHORT-PRECISION] -- primary events only; findings from
    # incomplete schedules included; None at an empty denominator.
    m[f"{prefix}|feature_cohort_precision"] = _metric(
        f"{prefix}|feature_cohort_precision", "feature_cohort",
        correct_pair_ids, frozenset(correct_pair_ids | false_event_ids), _BOOTSTRAP)

    # [R7.2.1-COMPLETION-RATE] / [R7.2.1-INCOMPLETION-RATE]
    m[f"{prefix}|combination_completion_rate"] = _metric(
        f"{prefix}|combination_completion_rate", "case",
        frozenset(completed), frozenset(in_den), _BINOMIAL)
    m[f"{prefix}|combination_incompletion_rate"] = _metric(
        f"{prefix}|combination_incompletion_rate", "case",
        frozenset(incomplete), frozenset(in_den), _BINOMIAL)

    # [R7.7-CLEAN-FINDING-RATE] and the incompletion companion -- same
    # denominator set, neither numerator depends on the other axis; a clean
    # case that produced no event still sits in its own denominator.
    clean_in_den = {c for c in in_den if label_index[(detector, c)].is_clean}
    clean_finding = {c for c in clean_in_den if outcomes[c] is EvidenceOutcome.FINDING}
    clean_incomplete = {c for c in clean_in_den
                        if states[c].kind is ScheduleStateKind.INCOMPLETE}
    m[f"{prefix}|clean_case_finding_rate"] = _metric(
        f"{prefix}|clean_case_finding_rate", "case",
        frozenset(clean_finding), frozenset(clean_in_den), _BINOMIAL)
    m[f"{prefix}|clean_case_incompletion_rate"] = _metric(
        f"{prefix}|clean_case_incompletion_rate", "case",
        frozenset(clean_incomplete), frozenset(clean_in_den), _BINOMIAL)

    # PREREG §7.2.1 (v29): each excluded state is published as a count over
    # all cases for the combination — numerator and denominator in the
    # §6.6.1 MetricValue shape — and enters no rate.
    all_cases = frozenset(per_case)
    for kind, name in ((ScheduleStateKind.NOT_APPLICABLE, "not_applicable_count"),
                       (ScheduleStateKind.UNSUPPORTED, "unsupported_count"),
                       (ScheduleStateKind.SHORT_CIRCUITED, "short_circuited_count")):
        members = frozenset(c for c, s in states.items() if s.kind is kind)
        m[f"{prefix}|{name}"] = _metric(f"{prefix}|{name}", "case", members, all_cases, _COUNT)

    # PREREG §7.2.1 (v30): a combination not_applicable on every
    # scope-eligible case in this body suppresses its yields, rates, and
    # gates — a yield over a combination that never applied is not a
    # measurement of the tool, and 0/N in print is indistinguishable from a
    # mode that ran everywhere and found nothing. Counts are the honest
    # signal and are never suppressed. Suppression is all-or-nothing over
    # the body, not per case.
    if all(s.kind is ScheduleStateKind.NOT_APPLICABLE for s in states.values()):
        reason = ("not_applicable on every scope-eligible case in this body: "
                  "a yield over a combination that never applied is not a "
                  "measurement of the tool (PREREG §7.2.1)")
        for name in (yield_name, "conditional_feature_cohort_recall",
                     "cohort_sensitivity", "feature_discovery_recall",
                     "unprobed_feature_cohort_rate", "feature_cohort_precision",
                     "combination_completion_rate", "combination_incompletion_rate",
                     "clean_case_finding_rate", "clean_case_incompletion_rate"):
            mid = f"{prefix}|{name}"
            m[mid] = SuppressedMetric(metric_id=mid, unit=m[mid].unit, reason=reason)
    return m


# ---------------------------------------------------------------------------
# Gates (PREREG §10.2 criterion 3)  [R10.2-RUNTIME-GATES]
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GateConfig:
    clean_fraction: float = 0.20   # locked, PREREG §10.2 criterion 3
    clean_excess: int = 1          # k >= floor(fraction * N) + excess
    completion_floor: float = 0.60


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    experimental: bool
    finding_gate_fired: bool
    completion_gate_fired: bool
    clean_n: int
    clean_findings: int
    clean_completed: int


def apply_runtime_gates(
    metrics: Mapping[str, "MetricValue | SuppressedMetric"],
    config: GateConfig = GateConfig(),
) -> dict[str, "GateResult | SuppressedGate"]:
    """Deterministic, per combination, applied independently (PREREG §10.2).
    A combination whose clean-case rates are suppressed has its gate
    suppressed with them, carrying the same reason (PREREG §7.2.1, v30)."""
    out: dict[str, GateResult | SuppressedGate] = {}
    prefixes = sorted({
        mid.rsplit("|", 1)[0] for mid in metrics
        if mid.endswith("|clean_case_finding_rate")})
    for prefix in prefixes:
        finding = metrics[f"{prefix}|clean_case_finding_rate"]
        incompletion = metrics[f"{prefix}|clean_case_incompletion_rate"]
        if isinstance(finding, SuppressedMetric) or isinstance(incompletion, SuppressedMetric):
            reason = (finding.reason if isinstance(finding, SuppressedMetric)
                      else incompletion.reason)
            out[prefix] = SuppressedGate(gate_id=prefix, reason=reason)
            continue
        if finding.denominator_members != incompletion.denominator_members:
            raise ProtocolViolation(
                f"{prefix}: the two clean-case rates must share one denominator "
                "set (PREREG §7.7)")
        n = finding.denominator
        k = finding.numerator
        completed = n - incompletion.numerator  # N = completed U incomplete
        finding_fired = n > 0 and k >= math.floor(round(config.clean_fraction * n, 9)) + config.clean_excess
        completion_fired = n > 0 and completed * 10**9 < int(round(config.completion_floor * 10**9)) * n
        out[prefix] = GateResult(
            gate_id=prefix,
            experimental=finding_fired or completion_fired,
            finding_gate_fired=finding_fired,
            completion_gate_fired=completion_fired,
            clean_n=n, clean_findings=k, clean_completed=completed)
    return out


# ---------------------------------------------------------------------------
# Assertions (PREREG §8.3)  [R8.3-PROVEN-ASSERTION]
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AssertionResults:
    no_proven_leakage_passed: bool
    proven_triggering_events: tuple[EvidenceEvent, ...]


def evaluate_runtime_assertions(
    events: Iterable[EvidenceEvent],
    gate_results: Mapping[str, "GateResult | SuppressedGate"],
) -> AssertionResults:
    """assert_no_proven_leakage fails iff an EvidenceEvent (1) licenses PROVEN
    and (2) belongs to a non-experimental combination. Consumes unaggregated
    events and the gate table -- never a merged ReportedFinding's inferred
    boolean (PREREG §8.3)."""
    triggering = []
    for e in events:
        gid = gate_id_for(e.detector_id, e.promotion_status)
        if gid not in gate_results:
            raise ProtocolViolation(f"no gate status for combination {gid} (PREREG §8.3)")
        gate = gate_results[gid]
        if isinstance(gate, SuppressedGate):
            raise ProtocolViolation(
                f"event from suppressed combination {gid} is contradictory "
                "input (PREREG §7.2.1)")
        if e.licenses_proven and not gate.experimental:
            triggering.append(e)
    return AssertionResults(
        no_proven_leakage_passed=not triggering,
        proven_triggering_events=tuple(triggering))


# ---------------------------------------------------------------------------
# Reach basis (PREREG §8.5)
# ---------------------------------------------------------------------------

def resolve_reach_basis(candidate_count: int, cap: int, all_candidates_scanned: bool) -> str:
    """Above the cap the capped subset is not scanned at all: the lower-bound
    procedure runs and reach_basis = lower_bound. full_scan is permitted only
    at or below the cap with every boundary scanned (PREREG §8.5)."""
    if candidate_count > cap:
        if all_candidates_scanned:
            raise ProtocolViolation(
                "a scan above the candidate-grid cap cannot be reported as "
                "full_scan (PREREG §8.5)")
        return "lower_bound"
    return "full_scan" if all_candidates_scanned else "lower_bound"
