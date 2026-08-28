"""B-9 -- Probe A under the frozen output contract. R153 §4.

§6.2's acceptance scores `CombinationTrace`s; a probe that emits none cannot be
evaluated by the registered machinery. This module converts a `ProbeAResult` into
traces the machinery already knows how to resolve.

**THE REDUCERS ARE NOT ADJUSTED.** R153 §6 makes adjusting one a halt. If
`resolve_state_pair` rejects a trace, the trace is wrong -- the machinery
predates the tool, and that is exactly its value.

THE MAPPINGS, each derived from the registered legality table rather than chosen:

  ELIGIBILITY.  A picked second with NO aggregate row is **not an eligible
  cohort**: there is nothing to corrupt, so nothing can be scheduled there.
  Those cohorts are excluded from `selected_eligible_cohorts` and counted
  separately. Putting them in and emitting no record would resolve to
  INCOMPLETE(crash) -- a missing schedule slot with no recorded failure -- which
  would report a dead process where the truth is an empty probe surface.

  PROMOTION.  The corruption is dtype-preserving by construction (integers get
  an in-range integer offset, booleans negate, floats stay floats), so every
  execution belongs to the PRESERVING combination. The PROMOTED combination has
  **no resolved strategy**, which resolves to NOT_APPLICABLE and pairs legally
  with NONE. It is emitted rather than omitted: a combination that ran nothing is
  a fact the trace should carry.

  OUTCOME.  A cohort whose in-second rows moved carries a `FindingRecord` --
  the build read a cell the model marks unavailable at that decision instant.
  A cohort that was probed and did not move is a valid record with no finding,
  which resolves to OBSERVED_SILENCE. **The distinction the artifact already
  draws in prose is exactly the one the contract draws in types.**

  RUN CONTEXT.  `FIXTURE`. `terminal_decision_occurred` is False -- the
  validator makes a terminal short-circuit outside a user run illegal for the
  whole run.
"""
from __future__ import annotations

from typing import Iterable

from protocol.runtime_reference import (
    CombinationTrace, EvidenceOutcome, ExecutionRecord, FindingRecord,
    PromotionStatus, RunContext, ScheduleStateKind, resolve_state_pair)

from .availability import ProbeAResult

STRATEGY_ID = "availability_corrupt"
DETECTOR_ID = "probe_a_availability"


def _cohort_id(second) -> str:
    """A cohort id with no reserved separator. `|` is the member/gate separator
    and the validator rejects it; ISO timestamps do not contain one, but the
    check is asserted rather than assumed."""
    cid = str(second).replace(" ", "T")
    if "|" in cid:
        raise ValueError("cohort id %r carries the reserved separator" % cid)
    return cid


def traces_for(result: ProbeAResult,
               eligible_seconds: Iterable,
               case_id: str) -> list[CombinationTrace]:
    """Two traces: the PRESERVING combination that ran, and the PROMOTED one
    that had no strategy resolve to it."""
    eligible = {str(s) for s in eligible_seconds}

    records, cohorts = [], []
    for c in result.cohorts:
        if str(c.second) not in eligible:
            continue                      # no aggregate row: nothing to schedule
        cid = _cohort_id(c.second)
        cohorts.append(cid)
        finding = None
        if c.moved_in_second > 0:
            feats = c.features_in_second or ()
            if not feats:
                # A finding must name a feature. If the probe recorded movement
                # but no column, the trace cannot be honestly emitted.
                raise ValueError(
                    "cohort %s moved %d row(s) but named no feature; a "
                    "FindingRecord may not be filled with a placeholder"
                    % (cid, c.moved_in_second))
            finding = FindingRecord(
                feature=feats[0],
                probe_cohort=cid,          # must equal the executing cohort
                affected_output_cohort=cid,
                is_secondary=False)
        records.append(ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id,
            strategy_id=STRATEGY_ID, promotion_status=PromotionStatus.PRESERVING,
            cohort_id=cid, attempted=True, valid=True, finding=finding))

    preserving = CombinationTrace(
        detector_id=DETECTOR_ID, case_id=case_id,
        promotion_status=PromotionStatus.PRESERVING,
        run_context=RunContext.FIXTURE,
        resolved_strategies=(STRATEGY_ID,),
        selected_eligible_cohorts=tuple(cohorts),
        required_inputs_available=True,
        terminal_decision_occurred=False,
        records=tuple(records))

    # NO STRATEGY PROMOTES. Emitted, not omitted -- a combination that ran
    # nothing is a fact, and NOT_APPLICABLE x NONE is a legal pair.
    promoted = CombinationTrace(
        detector_id=DETECTOR_ID, case_id=case_id,
        promotion_status=PromotionStatus.PROMOTED,
        run_context=RunContext.FIXTURE,
        resolved_strategies=(),
        selected_eligible_cohorts=(),
        required_inputs_available=True,
        terminal_decision_occurred=False,
        records=())
    return [preserving, promoted]


def resolve_all(traces: Iterable[CombinationTrace]) -> list[dict]:
    """Run every trace through the UNMODIFIED registered resolvers."""
    out = []
    for t in traces:
        state, outcome = resolve_state_pair(t)     # raises if illegal
        out.append({
            "detector_id": t.detector_id, "case_id": t.case_id,
            "promotion_status": t.promotion_status.value,
            "run_context": t.run_context.value,
            "schedule_state": state.kind.value,
            "schedule_reason": state.reason.value if state.reason else None,
            "evidence_outcome": outcome.value,
            "n_cohorts": len(t.selected_eligible_cohorts),
            "n_records": len(t.records),
            "n_findings": sum(1 for r in t.records if r.finding is not None),
            "legal_pair": True,
        })
    return out
