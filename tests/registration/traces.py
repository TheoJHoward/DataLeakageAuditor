"""Canonical trace fixtures for the registration suite (PREREG §6.6.1).

Every expected value here is hand-derived from PREREG.md prose, independently
of the reducer. The tests compare reducer output against these pins;
EXPECTED_OUTPUTS.md is then generated from the reducer under the pins. A
disagreement between the two blocks the tag and is routed, not patched over.

Interpretation notes encoded in these fixtures — both confirmed by v28:
  I1. Pair-level yield denominators are scope-eligible, so labelled pairs
      from not_applicable and unsupported cases remain in proof/evidence
      yield and the unprobed rate as misses; case-level denominators are
      execution-eligible (schedule_state in {completed, incomplete}).
      Confirmed: PREREG v28 §7.4 now defines both denominators for every
      row, runtime included.
  I2. short_circuited is excluded from every metric denominator, pair-level
      included (PREREG §6.6). It cannot arise in an evaluation run, so no
      published number depends on the exclusion. Confirmed unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from protocol.runtime_reference import (
    CaseLabels,
    CombinationTrace,
    EvidenceOutcome,
    ExecutionRecord,
    FailureReason,
    FindingRecord,
    PromotionStatus,
    RunContext,
    ScheduleStateKind,
)

D = "L3.1"
PRES = "L3.1|preserving"
PROM = "L3.1|promoted"

_P = PromotionStatus.PRESERVING
_M = PromotionStatus.PROMOTED


def find(feature: str = "f1", probe: str = "c1", affected: str = "c1",
         secondary: bool = False) -> FindingRecord:
    return FindingRecord(feature=feature, probe_cohort=probe,
                         affected_output_cohort=affected, is_secondary=secondary)


def rec(strategy: str, cohort: str, *, case: str, status: PromotionStatus = _P,
        valid: bool = True, finding: FindingRecord | None = None,
        reason: FailureReason | None = None) -> ExecutionRecord:
    return ExecutionRecord(
        detector_id=D, case_id=case, strategy_id=strategy,
        promotion_status=status, cohort_id=cohort, attempted=True,
        valid=valid, finding=finding, failure_reason=reason)


def tr(case: str, records: tuple[ExecutionRecord, ...], *,
       status: PromotionStatus = _P,
       context: RunContext = RunContext.EVALUATION,
       strategies: tuple[str, ...] = ("shuffle",),
       cohorts: tuple[str, ...] = ("c1", "c2"),
       inputs: bool = True, terminal: bool = False) -> CombinationTrace:
    return CombinationTrace(
        detector_id=D, case_id=case, promotion_status=status,
        run_context=context, resolved_strategies=strategies,
        selected_eligible_cohorts=cohorts,
        required_inputs_available=inputs,
        terminal_decision_occurred=terminal, records=records)


def labels(case: str, *pairs: tuple[str, str]) -> CaseLabels:
    return CaseLabels(detector_id=D, case_id=case, leaking_pairs=frozenset(pairs))


@dataclass(frozen=True)
class ExpectedPair:
    kind: ScheduleStateKind
    outcome: EvidenceOutcome
    reason: FailureReason | None = None


def combo_expectations(prefix: str, *, detection_yield, conditional, sensitivity,
                       discovery, unprobed, precision, completion, incompletion,
                       clean_finding, clean_incompletion, na, unsup, sc):
    """Full expected (numerator, denominator) map for one combination —
    every metric the state pair feeds, asserted on every trace."""
    yield_name = ("proof_yield" if prefix.endswith("preserving") else "evidence_yield")
    return {
        f"{prefix}|{yield_name}": detection_yield,
        f"{prefix}|conditional_feature_cohort_recall": conditional,
        f"{prefix}|cohort_sensitivity": sensitivity,
        f"{prefix}|feature_discovery_recall": discovery,
        f"{prefix}|unprobed_feature_cohort_rate": unprobed,
        f"{prefix}|feature_cohort_precision": precision,
        f"{prefix}|combination_completion_rate": completion,
        f"{prefix}|combination_incompletion_rate": incompletion,
        f"{prefix}|clean_case_finding_rate": clean_finding,
        f"{prefix}|clean_case_incompletion_rate": clean_incompletion,
        f"{prefix}|not_applicable_count": na,
        f"{prefix}|unsupported_count": unsup,
        f"{prefix}|short_circuited_count": sc,
    }


# Sentinel expectation: the metric must be a SuppressedMetric with a reason
# (PREREG §7.2.1, v30) — never a numeric value, never 0.
SUPPRESSED = "SUPPRESSED"

_SUPPRESSIBLE_NAMES = (
    "conditional_feature_cohort_recall", "cohort_sensitivity",
    "feature_discovery_recall", "unprobed_feature_cohort_rate",
    "feature_cohort_precision", "combination_completion_rate",
    "combination_incompletion_rate", "clean_case_finding_rate",
    "clean_case_incompletion_rate")


def suppressed_combo_expectations(prefix: str, *, na, unsup, sc):
    """PREREG §7.2.1 (v30): a combination not_applicable on every
    scope-eligible case in the body publishes its counts and suppresses its
    yields, rates, and gate. Counts are the honest signal and stay numeric."""
    yield_name = ("proof_yield" if prefix.endswith("preserving") else "evidence_yield")
    out: dict = {f"{prefix}|{yield_name}": SUPPRESSED}
    for name in _SUPPRESSIBLE_NAMES:
        out[f"{prefix}|{name}"] = SUPPRESSED
    out[f"{prefix}|not_applicable_count"] = na
    out[f"{prefix}|unsupported_count"] = unsup
    out[f"{prefix}|short_circuited_count"] = sc
    return out


@dataclass(frozen=True)
class TraceFixture:
    fixture_id: str
    title: str
    prose_basis: str
    traces: tuple[CombinationTrace, ...]
    case_labels: tuple[CaseLabels, ...]
    # Keyed by combination prefix for single-case fixtures, or by
    # "prefix@case_id" where one combination spans several cases.
    expected_pairs: dict[str, ExpectedPair]
    expected_metrics: dict[str, object]  # (num, den) tuple or SUPPRESSED
    notes: str = ""
    # For gate-bearing fixtures: expected gate outcome per combination prefix.
    expected_gates: dict[str, dict] = field(default_factory=dict)
    # Combinations whose gate must be a SuppressedGate (PREREG §7.2.1, v30).
    expected_suppressed_gates: tuple[str, ...] = ()


_RAW_FIXTURES: tuple[TraceFixture, ...] = (

    TraceFixture(
        fixture_id="T01", title="zero valid executions",
        prose_basis="PREREG §6.6 (incomplete, reason precedence), §7.2 (miss stays in)",
        traces=(tr("t01", (
            rec("shuffle", "c1", case="t01", valid=False, reason=FailureReason.DETERMINISM),
            rec("shuffle", "c2", case="t01", valid=False, reason=FailureReason.DETERMINISM),
        )),),
        case_labels=(labels("t01", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.INCOMPLETE, EvidenceOutcome.NONE, FailureReason.DETERMINISM)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 1), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 1), unprobed=(1, 1), precision=(0, 0),
            completion=(0, 1), incompletion=(1, 1),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        notes="Guard failed everywhere: the labelled pair is a miss and stays "
              "in the proof-yield denominator; nothing was probed."),

    TraceFixture(
        fixture_id="T02", title="valid silence, then a later failure",
        prose_basis="PREREG §6.6 (totalized evidence_outcome — the v23 counterexample)",
        traces=(tr("t02", (
            rec("shuffle", "c1", case="t02"),
            rec("shuffle", "c2", case="t02", valid=False, reason=FailureReason.COMPATIBILITY),
        )),),
        case_labels=(labels("t02", ("f1", "c2")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.INCOMPLETE, EvidenceOutcome.OBSERVED_SILENCE,
            FailureReason.COMPATIBILITY)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 1), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 1), unprobed=(1, 1), precision=(0, 0),
            completion=(0, 1), incompletion=(1, 1),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        notes="observed_silence covers the executions actually performed, "
              "never the schedule. The leaky cohort c2 was never probed, so "
              "cohort sensitivity has an empty denominator."),

    TraceFixture(
        fixture_id="T03", title="valid finding, then a later failure",
        prose_basis="PREREG §6.6 (incomplete x finding), §7.2.1 (findings from "
                    "incomplete schedules count), §7.7",
        traces=(tr("t03", (
            rec("shuffle", "c1", case="t03", finding=find()),
            rec("shuffle", "c2", case="t03", valid=False, reason=FailureReason.COMPATIBILITY),
        )),),
        case_labels=(labels("t03", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.INCOMPLETE, EvidenceOutcome.FINDING,
            FailureReason.COMPATIBILITY)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(1, 1), conditional=(0, 0), sensitivity=(1, 1),
            discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
            completion=(0, 1), incompletion=(1, 1),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        notes="Proof yield 1/1 while conditional recall is undefined (no "
              "completed case): the two metrics answer different questions."),

    TraceFixture(
        fixture_id="T04", title="two strategies, one fails and one succeeds",
        prose_basis="PREREG §6.6 (reason precedence: compatibility over crash), §6.11",
        traces=(tr("t04", (
            rec("shuffle", "c1", case="t04", finding=find()),
            rec("shuffle", "c2", case="t04"),
            rec("noise", "c1", case="t04", valid=False, reason=FailureReason.COMPATIBILITY),
            rec("noise", "c2", case="t04", valid=False, reason=FailureReason.CRASH),
        ), strategies=("shuffle", "noise")),),
        case_labels=(labels("t04", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.INCOMPLETE, EvidenceOutcome.FINDING,
            FailureReason.COMPATIBILITY)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(1, 1), conditional=(0, 0), sensitivity=(1, 1),
            discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
            completion=(0, 1), incompletion=(1, 1),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        notes="Both cohorts count as probed for the combination — shuffle "
              "validly executed them (PREREG §6.11 aggregation). noise's "
              "failures leave the schedule incomplete under reason precedence."),

    TraceFixture(
        fixture_id="T05", title="a promoted finding before any preserving execution",
        prose_basis="PREREG §6.5 (regardless of which ran first), §7.2 (two events, "
                    "one PROVEN finding with corroboration)",
        traces=(
            tr("t05", (
                rec("complex", "c1", case="t05", status=_M, finding=find()),
                rec("complex", "c2", case="t05", status=_M),
            ), status=_M, strategies=("complex",)),
            tr("t05", (
                rec("shuffle", "c1", case="t05", finding=find()),
                rec("shuffle", "c2", case="t05"),
            )),
        ),
        case_labels=(labels("t05", ("f1", "c1")),),
        expected_pairs={
            PRES: ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
            PROM: ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
        },
        expected_metrics={
            **combo_expectations(
                PRES, detection_yield=(1, 1), conditional=(1, 1), sensitivity=(1, 1),
                discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
                completion=(1, 1), incompletion=(0, 1),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(0, 1)),
            **combo_expectations(
                PROM, detection_yield=(1, 1), conditional=(1, 1), sensitivity=(1, 1),
                discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
                completion=(1, 1), incompletion=(0, 1),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        },
        notes="Two EvidenceEvents (one per combination), one ReportedFinding "
              "at PROVEN with the promoted event as corroboration."),

    TraceFixture(
        fixture_id="T06", title="a completed clean case with a finding",
        prose_basis="PREREG §7.7 (clean-case finding rate), §10.2 criterion 3",
        traces=(tr("t06", (
            rec("shuffle", "c1", case="t06", finding=find()),
            rec("shuffle", "c2", case="t06"),
        )),),
        case_labels=(labels("t06"),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 0), unprobed=(0, 0), precision=(0, 1),
            completion=(1, 1), incompletion=(0, 1),
            clean_finding=(1, 1), clean_incompletion=(0, 1),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        expected_gates={PRES: dict(experimental=True, finding_gate_fired=True,
                                   completion_gate_fired=False)},
        notes="N=1 clean case, k=1 false finding: k >= floor(0.20*1)+1 = 1, "
              "so the finding gate fires. Yield denominators are empty on a "
              "clean-only corpus and read None, never 0.0 or 1.0."),

    TraceFixture(
        fixture_id="T07", title="an incomplete clean case with a finding",
        prose_basis="PREREG §7.7 (no false finding escapes the gate because its "
                    "schedule later failed), §10.2 criterion 3 (completion floor)",
        traces=(tr("t07", (
            rec("shuffle", "c1", case="t07", finding=find()),
            rec("shuffle", "c2", case="t07", valid=False, reason=FailureReason.COMPATIBILITY),
        )),),
        case_labels=(labels("t07"),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.INCOMPLETE, EvidenceOutcome.FINDING,
            FailureReason.COMPATIBILITY)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 0), unprobed=(0, 0), precision=(0, 1),
            completion=(0, 1), incompletion=(1, 1),
            clean_finding=(1, 1), clean_incompletion=(1, 1),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        expected_gates={PRES: dict(experimental=True, finding_gate_fired=True,
                                   completion_gate_fired=True)},
        notes="The incomplete case sits in both clean-case denominators; the "
              "false finding still counts and the completion floor also fires."),

    TraceFixture(
        fixture_id="T08", title="a combination's own terminal finding, remaining work unrun",
        prose_basis="PREREG §6.6 (short_circuited covers a combination's own "
                    "terminal finding — the v24 gap), user runs only",
        traces=(tr("t08", (
            rec("shuffle", "c1", case="t08", finding=find()),
        ), context=RunContext.USER, terminal=True),),
        case_labels=(labels("t08", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.FINDING)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 0), unprobed=(0, 0), precision=(0, 0),
            completion=(0, 0), incompletion=(0, 0),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(0, 1), sc=(1, 1)),
        notes="short_circuited x finding is legal; the case is excluded from "
              "every metric denominator and published only as a count."),

    TraceFixture(
        fixture_id="T09", title="REVIEW evidence, then another combination's terminal finding",
        prose_basis="PREREG §6.6 (short_circuited x finding — being cut short says "
                    "nothing about whether evidence was already observed)",
        traces=(
            tr("t09", (
                rec("complex", "c1", case="t09", status=_M, finding=find()),
            ), status=_M, strategies=("complex",), context=RunContext.USER, terminal=True),
            tr("t09", (
                rec("shuffle", "c1", case="t09", finding=find()),
            ), context=RunContext.USER, terminal=True),
        ),
        case_labels=(labels("t09", ("f1", "c1")),),
        expected_pairs={
            PROM: ExpectedPair(ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.FINDING),
            PRES: ExpectedPair(ScheduleStateKind.SHORT_CIRCUITED, EvidenceOutcome.FINDING),
        },
        expected_metrics={
            **combo_expectations(
                PRES, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
                discovery=(0, 0), unprobed=(0, 0), precision=(0, 0),
                completion=(0, 0), incompletion=(0, 0),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(1, 1)),
            **combo_expectations(
                PROM, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
                discovery=(0, 0), unprobed=(0, 0), precision=(0, 0),
                completion=(0, 0), incompletion=(0, 0),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(1, 1)),
        },
        notes="The promoted combination recorded REVIEW evidence at c1 before "
              "the preserving combination's terminal finding preempted it."),

    TraceFixture(
        fixture_id="T10", title="valid silence, then another combination's terminal finding",
        prose_basis="PREREG §6.6 (short_circuited x observed_silence; completed "
                    "under a terminal decision when nothing remained)",
        traces=(
            tr("t10", (
                rec("complex", "c1", case="t10", status=_M),
            ), status=_M, strategies=("complex",), context=RunContext.USER, terminal=True),
            tr("t10", (
                rec("shuffle", "c1", case="t10", finding=find()),
            ), context=RunContext.USER, terminal=True, cohorts=("c1",)),
        ),
        case_labels=(labels("t10", ("f1", "c1")),),
        expected_pairs={
            PROM: ExpectedPair(ScheduleStateKind.SHORT_CIRCUITED,
                               EvidenceOutcome.OBSERVED_SILENCE),
            PRES: ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
        },
        expected_metrics={
            **combo_expectations(
                PRES, detection_yield=(1, 1), conditional=(1, 1), sensitivity=(1, 1),
                discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
                completion=(1, 1), incompletion=(0, 1),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(0, 1)),
            **combo_expectations(
                PROM, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
                discovery=(0, 0), unprobed=(0, 0), precision=(0, 0),
                completion=(0, 0), incompletion=(0, 0),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 1), unsup=(0, 1), sc=(1, 1)),
        },
        notes="The preserving schedule had one selected cohort and finished it, "
              "so a terminal decision with nothing unrun resolves completed, "
              "not short_circuited. The promoted row is preempted mid-schedule."),

    TraceFixture(
        fixture_id="T13", title="a completed clean case with no event at all",
        prose_basis="PREREG §6.6.1 (every case-level metric includes no-event cases)",
        traces=(tr("t13", (
            rec("shuffle", "c1", case="t13"),
            rec("shuffle", "c2", case="t13"),
        )),),
        case_labels=(labels("t13"),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.COMPLETED, EvidenceOutcome.OBSERVED_SILENCE)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 0), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 0), unprobed=(0, 0), precision=(0, 0),
            completion=(1, 1), incompletion=(0, 1),
            clean_finding=(0, 1), clean_incompletion=(0, 1),
            na=(0, 1), unsup=(0, 1), sc=(0, 1)),
        expected_gates={PRES: dict(experimental=False, finding_gate_fired=False,
                                   completion_gate_fired=False)},
        notes="A clean case that produced nothing still sits in its own "
              "denominator: clean-case finding rate is 0/1, not 0/0."),

    TraceFixture(
        fixture_id="T14", title="unsupported: strategies resolve, inputs missing",
        prose_basis="PREREG §2.7 (undeclared means unsupported, never pass), §6.6, "
                    "§7.2 (the pair stays in — interpretation note I1)",
        traces=(tr("t14", (), inputs=False),),
        case_labels=(labels("t14", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.UNSUPPORTED, EvidenceOutcome.NONE)},
        expected_metrics=combo_expectations(
            PRES, detection_yield=(0, 1), conditional=(0, 0), sensitivity=(0, 0),
            discovery=(0, 1), unprobed=(1, 1), precision=(0, 0),
            completion=(0, 0), incompletion=(0, 0),
            clean_finding=(0, 0), clean_incompletion=(0, 0),
            na=(0, 1), unsup=(1, 1), sc=(0, 1)),
        notes="The case leaves every case-level denominator and is published "
              "as a count, while its labelled pair stays in the pair-level "
              "yield denominator as a miss — dropping it would convert "
              "missing coverage into a better rate."),

    TraceFixture(
        fixture_id="T15", title="not_applicable: no strategy resolves to this status",
        prose_basis="PREREG §6.6 (resolution order step 1), §7.2 (a case whose only "
                    "firing strategies promoted contributes misses — note I1)",
        traces=(tr("t15", (), strategies=()),),
        case_labels=(labels("t15", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE)},
        expected_metrics=suppressed_combo_expectations(
            PRES, na=(1, 1), unsup=(0, 1), sc=(0, 1)),
        expected_suppressed_gates=(PRES,),
        notes="Preserving row on a case where nothing resolves preserving. "
              "In this one-case body the combination is not_applicable "
              "everywhere, so its yields, rates, and gate are suppressed "
              "with the counts as the honest signal (PREREG §7.2.1, v30); "
              "in a mixed body the labelled pair stays a yield miss (T18)."),

    TraceFixture(
        fixture_id="T16", title="not_applicable: strategies resolve, no eligible cohort selected",
        prose_basis="PREREG §6.6 resolution order step 1, second clause (v28) — "
                    "vacuous completed x none is illegal, so nothing-to-do "
                    "resolves not_applicable",
        traces=(tr("t16", (), cohorts=()),),
        case_labels=(labels("t16", ("f1", "c1")),),
        expected_pairs={PRES: ExpectedPair(
            ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE)},
        expected_metrics=suppressed_combo_expectations(
            PRES, na=(1, 1), unsup=(0, 1), sc=(0, 1)),
        expected_suppressed_gates=(PRES,),
        notes="Resolved strategies, available inputs, zero selected eligible "
              "cohorts: not_applicable x none. As in T15, the one-case body "
              "is all-not_applicable for this combination, so suppression "
              "applies (PREREG §7.2.1, v30)."),

    TraceFixture(
        fixture_id="T17", title="multi-case body, promoted not_applicable everywhere: suppressed",
        prose_basis="PREREG §7.2.1 (v30) — an all-not_applicable combination "
                    "publishes its counts and suppresses its yields, rates, "
                    "and gate, naming the reason",
        traces=(
            tr("t17a", (rec("shuffle", "c1", case="t17a", finding=find()),
                        rec("shuffle", "c2", case="t17a"))),
            tr("t17b", (rec("shuffle", "c1", case="t17b"),
                        rec("shuffle", "c2", case="t17b"))),
            tr("t17a", (), status=_M, strategies=()),
            tr("t17b", (), status=_M, strategies=()),
        ),
        case_labels=(labels("t17a", ("f1", "c1")), labels("t17b")),
        expected_pairs={
            f"{PRES}@t17a": ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
            f"{PRES}@t17b": ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.OBSERVED_SILENCE),
            f"{PROM}@t17a": ExpectedPair(ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE),
            f"{PROM}@t17b": ExpectedPair(ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE),
        },
        expected_metrics={
            **combo_expectations(
                PRES, detection_yield=(1, 1), conditional=(1, 1), sensitivity=(1, 1),
                discovery=(1, 1), unprobed=(0, 1), precision=(1, 1),
                completion=(2, 2), incompletion=(0, 2),
                clean_finding=(0, 1), clean_incompletion=(0, 1),
                na=(0, 2), unsup=(0, 2), sc=(0, 2)),
            **suppressed_combo_expectations(PROM, na=(2, 2), unsup=(0, 2), sc=(0, 2)),
        },
        expected_gates={PRES: dict(experimental=False, finding_gate_fired=False,
                                   completion_gate_fired=False)},
        expected_suppressed_gates=(PROM,),
        notes="The promoted combination never applied anywhere in this "
              "two-case body: its evidence yield would print 0/1 and read as "
              "a mode that ran and found nothing, so it is suppressed with "
              "the not_applicable count 2/2 as the honest signal."),

    TraceFixture(
        fixture_id="T18", title="multi-case body, promoted not_applicable on some cases only: no suppression",
        prose_basis="PREREG §7.2.1 (v30) — suppression is all-or-nothing over the "
                    "body; a mixed body publishes normally, with not_applicable "
                    "cases contributing misses per §7.2/§7.4",
        traces=(
            tr("t18a", (rec("shuffle", "c1", case="t18a", finding=find()),
                        rec("shuffle", "c2", case="t18a"))),
            tr("t18b", (rec("shuffle", "c1", case="t18b"),
                        rec("shuffle", "c2", case="t18b"))),
            tr("t18a", (), status=_M, strategies=()),
            tr("t18b", (rec("complex", "c1", case="t18b", status=_M),
                        rec("complex", "c2", case="t18b", status=_M)),
               status=_M, strategies=("complex",)),
        ),
        case_labels=(labels("t18a", ("f1", "c1")), labels("t18b", ("f1", "c1"))),
        expected_pairs={
            f"{PRES}@t18a": ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.FINDING),
            f"{PRES}@t18b": ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.OBSERVED_SILENCE),
            f"{PROM}@t18a": ExpectedPair(ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE),
            f"{PROM}@t18b": ExpectedPair(ScheduleStateKind.COMPLETED, EvidenceOutcome.OBSERVED_SILENCE),
        },
        expected_metrics={
            **combo_expectations(
                PRES, detection_yield=(1, 2), conditional=(1, 2), sensitivity=(1, 2),
                discovery=(1, 2), unprobed=(0, 2), precision=(1, 1),
                completion=(2, 2), incompletion=(0, 2),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(0, 2), unsup=(0, 2), sc=(0, 2)),
            **combo_expectations(
                PROM, detection_yield=(0, 2), conditional=(0, 1), sensitivity=(0, 1),
                discovery=(0, 2), unprobed=(1, 2), precision=(0, 0),
                completion=(1, 1), incompletion=(0, 1),
                clean_finding=(0, 0), clean_incompletion=(0, 0),
                na=(1, 2), unsup=(0, 2), sc=(0, 2)),
        },
        expected_gates={
            PRES: dict(experimental=False),
            PROM: dict(experimental=False),
        },
        notes="The promoted combination applied on t18b, so nothing is "
              "suppressed: t18a's labelled pair is an evidence-yield miss "
              "from a not_applicable case (scope-eligible per §7.4) and an "
              "unprobed pair, while t18b's was probed and missed by silence."),
)


def _with_promoted_na(fx: TraceFixture) -> TraceFixture:
    """PREREG §6.6 (v29): every labelled case carries an explicit trace for
    EVERY combination, and promotion_status is a closed two-valued axis
    (§3.1) — so a fixture whose case narrative involves no promoting strategy
    still traces the promoted combination as not_applicable explicitly.

    The appended expectation row is hand-derived from prose, stated once: a
    not_applicable combination sits outside every case-level denominator and
    is published as a count (§7.7, §7.2.1), while its labelled pairs remain
    scope-eligible misses in the yield and unprobed denominators (§7.4)."""
    if any(t.promotion_status is _M for t in fx.traces):
        return fx
    first = fx.traces[0]
    promoted_trace = tr(
        first.case_id, (), status=_M, strategies=(),
        context=first.run_context, terminal=first.terminal_decision_occurred)
    return replace(
        fx,
        traces=fx.traces + (promoted_trace,),
        expected_pairs={
            **fx.expected_pairs,
            PROM: ExpectedPair(ScheduleStateKind.NOT_APPLICABLE, EvidenceOutcome.NONE)},
        expected_metrics={
            **fx.expected_metrics,
            # The one-case body is all-not_applicable for the promoted
            # combination, so its yields, rates, and gate are suppressed
            # (PREREG §7.2.1, v30) and only the counts publish.
            **suppressed_combo_expectations(PROM, na=(1, 1), unsup=(0, 1), sc=(0, 1))},
        expected_suppressed_gates=fx.expected_suppressed_gates + (PROM,),
        notes=fx.notes + " The promoted combination is traced not_applicable "
              "explicitly — a missing trace raises (PREREG §6.6) — and, being "
              "not_applicable on this whole one-case body, its yields, rates, "
              "and gate are suppressed (PREREG §7.2.1, v30).")


FIXTURES: tuple[TraceFixture, ...] = tuple(_with_promoted_na(fx) for fx in _RAW_FIXTURES)


# ---------------------------------------------------------------------------
# Assertion scenarios: traces 11 and 12 (PREREG §8.3)
# ---------------------------------------------------------------------------

def _mixed_pair_traces(case: str) -> tuple[CombinationTrace, ...]:
    """One pair, found by both combinations, schedules completed."""
    return (
        tr(case, (
            rec("shuffle", "c1", case=case, finding=find()),
            rec("shuffle", "c2", case=case),
        )),
        tr(case, (
            rec("complex", "c1", case=case, status=_M, finding=find()),
            rec("complex", "c2", case=case, status=_M),
        ), status=_M, strategies=("complex",)),
    )


@dataclass(frozen=True)
class AssertionScenario:
    fixture_id: str
    title: str
    prose_basis: str
    traces: tuple[CombinationTrace, ...]
    experimental: dict[str, bool]     # combination prefix -> gate status
    expect_pass: bool
    expected_trigger_count: int
    notes: str


ASSERTION_SCENARIOS: tuple[AssertionScenario, ...] = (
    AssertionScenario(
        fixture_id="T11",
        title="experimental preserving event + non-experimental promoted event: passes",
        prose_basis="PREREG §8.3 — the assertion reads unaggregated events and the "
                    "gate table, never a merged finding's inferred boolean",
        traces=_mixed_pair_traces("t11"),
        experimental={PRES: True, PROM: False},
        expect_pass=True,
        expected_trigger_count=0,
        notes="The only PROVEN-licensing event belongs to an experimental "
              "combination; the non-experimental event is promoted and does "
              "not license PROVEN. A single inferred boolean on the merged "
              "finding would get this wrong in either direction."),
    AssertionScenario(
        fixture_id="T12",
        title="non-experimental preserving event + experimental promoted event: fails",
        prose_basis="PREREG §8.3",
        traces=_mixed_pair_traces("t12"),
        experimental={PRES: False, PROM: True},
        expect_pass=False,
        expected_trigger_count=1,
        notes="The preserving event licenses PROVEN and its combination is "
              "non-experimental: assert_no_proven_leakage() must fail."),
)
