"""Probe B -- the column probe (Layer 1), and its CombinationTrace emission.

WHAT IT ESTABLISHES. For each source column: corrupt the whole column, re-run
`build` once, compare the output exact. Movement means the output reads that
column. It needs no availability model, no decision time and no split, which is
why it is the zero-configuration layer.

WHAT THE SCHEMA AXES CARRY HERE, said explicitly so no reader mistakes one for
something it is not:

    cohort  = THE PERTURBED DOMAIN. For L3.1 that is the cells of a decision
              cohort whose availability instant falls after d(i). For the column
              probe it is one whole source column, written `col:<frame>.<name>`.
              It is NOT a decision cohort -- Layer 1 has none, because it has no
              availability model.
    feature = the OUTPUT column that moved.

TERMINATION. PREREG.md §6.6 line 1053: on the evaluation corpora, the
conformance suite and the acceptance fixture gate run, every configured strategy
executes at every selected eligible cohort regardless of any finding. This probe
therefore runs the full product in those contexts and never stops early. Line
1051 gives the reason, and it is worth restating because it inverts the intuition
that stopping early is free: if promoted strategies execute only where preserving
ones found nothing, that combination is evaluated disproportionately on the hard
and the negative cases, and its published rate is biased by another combination's
result. Strategy ORDER still holds -- promotion-safe first -- because order costs
nothing and preserves PROVEN where PROVEN is available.

THE TWO COMBINATIONS ARE KEPT SQUARE. PREREG.md §3.2: promotion is per strategy
per frame, so `nan` promotes on an integer column and preserves on a float one. A
combination whose schedule is the ragged remainder of that split cannot report
`completed` honestly, so the split is made on the cohort axis instead:

    preserving: strategies (shuffle, sentinel) x every probed column
    promoted:   strategy  (nan,)              x the columns where nan promotes

Every slot in each product is scheduled, so `completed` means what §6.6 says it
means. `nan` on a float column preserves and is deliberately not configured
there; that is a configuration choice, stated, not a silent omission.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import pandas as pd

from protocol.runtime_reference import (
    CombinationTrace,
    ExecutionRecord,
    FailureReason,
    FindingRecord,
    PromotionStatus,
    RunContext,
)

from . import corruption as cx
from .determinism import DeterminismResult, check_frame, frames_equal

DETECTOR_ID = "columndep"


def cohort_id_for(frame_name: str, column: str) -> str:
    return "col:%s.%s" % (frame_name, column)


@dataclass
class ProbeResult:
    """Both combinations, plus Layer 1's own product: the dependency map."""
    preserving: CombinationTrace
    promoted: CombinationTrace
    dependency_map: dict[str, tuple[str, ...]] = field(default_factory=dict)
    determinism: dict[str, DeterminismResult] = field(default_factory=dict)
    baseline_columns: tuple[str, ...] = ()

    @property
    def traces(self) -> tuple[CombinationTrace, CombinationTrace]:
        return (self.preserving, self.promoted)


def _call(build: Callable, frames: dict[str, pd.DataFrame], bare: bool):
    """`build` takes ONE positional argument. Anything else, the user wraps."""
    return build(next(iter(frames.values())) if bare else frames)


def _substitute(frames: dict[str, pd.DataFrame], frame_name: str,
                column: str, new: pd.Series) -> dict[str, pd.DataFrame]:
    """A shallow copy with one column replaced. The caller's frames are never
    mutated -- a probe that edits its input has destroyed its own baseline."""
    out = dict(frames)
    f = frames[frame_name].copy(deep=False)
    f[column] = new
    out[frame_name] = f
    return out


def probe_columns(
    frames: dict[str, pd.DataFrame],
    build: Callable[[Any], pd.DataFrame],
    *,
    case_id: str = "user",
    run_context: RunContext = RunContext.USER,
    bare: bool = False,
    decision_time=None,
    availability=None,
    train_idx=None,
    test_idx=None,
    meta=None,
    columns: tuple[str, ...] | None = None,
) -> ProbeResult:
    """Run the column probe over every source column and emit both traces."""
    targets: list[tuple[str, str]] = []
    for fname, f in frames.items():
        for c in f.columns:
            if columns is not None and c not in columns:
                continue
            if "|" in str(c) or "|" in fname:
                continue        # reserved separator; cannot be a cohort id
            targets.append((fname, str(c)))

    # ---- the original-frame determinism guard (§6.10: per frame, not once) --
    det: dict[str, DeterminismResult] = {}
    g0 = check_frame(lambda fr: _call(build, fr, bare), frames, "original")
    det["original"] = g0

    if not g0.deterministic:
        # §6.10: a frame that fails its guard produces NO runtime finding. Every
        # strategy assigned to it is could_not_run(determinism). Not a downgrade
        # to RULE -- RULE findings arise only from declared rules (§6.12).
        #
        # But a build that RAISED on its own unperturbed input was never shown to
        # be nondeterministic; it was shown not to run. §6.6's reason precedence
        # has a name for that and it is CRASH.
        return _failed_frame_result(
            targets, case_id, run_context, det,
            FailureReason.CRASH if g0.raised else FailureReason.DETERMINISM)

    baseline = _call(build, frames, bare)
    baseline_cols = tuple(str(c) for c in baseline.columns)

    pres_records: list[ExecutionRecord] = []
    prom_records: list[ExecutionRecord] = []
    prom_cohorts: list[str] = []
    pres_cohorts: list[str] = []
    depmap: dict[str, tuple[str, ...]] = {}

    for fname, col in targets:
        cid = cohort_id_for(fname, col)
        pres_cohorts.append(cid)
        series = frames[fname][col]
        moved_any: set[str] = set()

        promotes_here = cx.promotion_of(cx.NAN, series) is PromotionStatus.PROMOTED
        if promotes_here:
            prom_cohorts.append(cid)

        # ---- preserving strategies: the full product, no early stop ---------
        for strat in (cx.SHUFFLE, cx.SENTINEL):
            recs, moved = _run_one(build, frames, bare, baseline, fname, col,
                                   strat, cid, case_id, PromotionStatus.PRESERVING)
            pres_records.extend(recs)
            moved_any |= moved

        # ---- the promoting strategy, on its own promoted frame --------------
        if promotes_here:
            fid = "promoted:%s" % cid
            promoted_frames = _substitute(
                frames, fname, col, cx.corrupt(series, cx.NAN, mask=pd.Series(
                    False, index=series.index)).astype("float64"))
            g = check_frame(lambda fr: _call(build, fr, bare), promoted_frames, fid)
            det[fid] = g
            if not g.deterministic:
                prom_records.append(ExecutionRecord(
                    detector_id=DETECTOR_ID, case_id=case_id, strategy_id=cx.NAN,
                    promotion_status=PromotionStatus.PROMOTED, cohort_id=cid,
                    attempted=True, valid=False,
                    failure_reason=FailureReason.DETERMINISM))
            else:
                prom_base = _call(build, promoted_frames, bare)
                recs, moved = _run_one(build, frames, bare, prom_base, fname, col,
                                       cx.NAN, cid, case_id, PromotionStatus.PROMOTED)
                prom_records.extend(recs)
                moved_any |= moved

        if moved_any:
            depmap[cid] = tuple(sorted(moved_any))

    preserving = CombinationTrace(
        detector_id=DETECTOR_ID, case_id=case_id,
        promotion_status=PromotionStatus.PRESERVING, run_context=run_context,
        resolved_strategies=(cx.SHUFFLE, cx.SENTINEL) if pres_cohorts else (),
        selected_eligible_cohorts=tuple(pres_cohorts),
        required_inputs_available=True,
        terminal_decision_occurred=False,
        records=tuple(pres_records))

    promoted = CombinationTrace(
        detector_id=DETECTOR_ID, case_id=case_id,
        promotion_status=PromotionStatus.PROMOTED, run_context=run_context,
        resolved_strategies=(cx.NAN,) if prom_cohorts else (),
        selected_eligible_cohorts=tuple(prom_cohorts),
        required_inputs_available=True,
        terminal_decision_occurred=False,
        records=tuple(prom_records))

    return ProbeResult(preserving, promoted, depmap, det, baseline_cols)


def _run_one(build, frames, bare, baseline, fname, col, strat, cid, case_id, status):
    """One (strategy, cohort) execution. Returns (records, moved output columns).

    Emits one record per moved output feature, or a single finding-free record
    when nothing moved -- that record is what makes the slot's silence OBSERVED
    rather than merely absent, and absence of records never carries a second
    meaning (§6.6).
    """
    series = frames[fname][col]
    try:
        bad = cx.corrupt(series, strat, seed=abs(hash((fname, col, strat))) % (2 ** 31))
    except cx.Unsupportable as e:
        return [ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True, valid=False,
            failure_reason=FailureReason.COMPATIBILITY)], set()

    if bad.equals(series):
        # A permutation that is the identity perturbs nothing. Reporting silence
        # here would be reporting that a probe which did not happen found
        # nothing -- the control-artifact case (§6.11 control 2).
        return [ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True, valid=False,
            failure_reason=FailureReason.CONTROL_ARTIFACT)], set()

    try:
        out = _call(build, _substitute(frames, fname, col, bad), bare)
    except Exception:                                       # noqa: BLE001
        return [ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True, valid=False,
            failure_reason=FailureReason.CRASH)], set()

    if out is None or out.shape[0] != baseline.shape[0] or not out.index.equals(baseline.index):
        # §6.11 control 3: shape and index are validated on EVERY perturbed
        # execution. A pipeline that drops rows makes every later comparison
        # meaningless, including the ones that look clean.
        return [ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True, valid=False,
            failure_reason=FailureReason.COMPATIBILITY)], set()

    equal, differing, _ = frames_equal(baseline, out)
    if equal:
        return [ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True,
            valid=True, finding=None)], set()

    recs = []
    for feat in differing:
        recs.append(ExecutionRecord(
            detector_id=DETECTOR_ID, case_id=case_id, strategy_id=strat,
            promotion_status=status, cohort_id=cid, attempted=True, valid=True,
            finding=FindingRecord(feature=str(feat), probe_cohort=cid,
                                  affected_output_cohort=cid)))
    return recs, {str(c) for c in differing}


def _failed_frame_result(targets, case_id, run_context, det, reason) -> ProbeResult:
    """Every strategy assigned to a failed frame is could_not_run(reason)."""
    cohorts = tuple(cohort_id_for(f, c) for f, c in targets)
    pres = tuple(ExecutionRecord(
        detector_id=DETECTOR_ID, case_id=case_id, strategy_id=s,
        promotion_status=PromotionStatus.PRESERVING, cohort_id=cid,
        attempted=True, valid=False, failure_reason=reason)
        for cid in cohorts for s in (cx.SHUFFLE, cx.SENTINEL))
    return ProbeResult(
        CombinationTrace(
            detector_id=DETECTOR_ID, case_id=case_id,
            promotion_status=PromotionStatus.PRESERVING, run_context=run_context,
            resolved_strategies=(cx.SHUFFLE, cx.SENTINEL) if cohorts else (),
            selected_eligible_cohorts=cohorts, required_inputs_available=True,
            terminal_decision_occurred=False, records=pres),
        CombinationTrace(
            detector_id=DETECTOR_ID, case_id=case_id,
            promotion_status=PromotionStatus.PROMOTED, run_context=run_context,
            resolved_strategies=(), selected_eligible_cohorts=(),
            required_inputs_available=True, terminal_decision_occurred=False,
            records=()),
        {}, det, ())
