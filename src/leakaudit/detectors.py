"""B9 -- the second and third detectors: what the output reads a column FOR.

`columndep` (Layer 1, `probe.py`) answers one question: does the output read
this column at all? These two split that answer into the two things a pipeline
can read a column for, so that a dependency can be told apart from a value
dependency and from a null-mask dependency.

    valueread   does the output read this column's VALUES?
                preserving  shuffle, in-dtype sentinel   -- every column
                promoted    out-of-dtype sentinel        -- where a wider dtype
                                                            exists at all
    nullread    does the output read this column's NULL PATTERN?
                preserving  nan  -- columns that already hold a null in their
                                    own dtype (float, datetime, object)
                promoted    nan  -- columns that do not (integer, boolean)

WHY THE COHORT SETS ARE DTYPE-DEFINED, AND WHY THAT IS LEGAL. `PREREG.md` §6.6
line 1080: "a combination is execution-eligible for a case when at least one
configured strategy resolves to that promotion status on that case and has all
required inputs. **This is per case rather than per configuration because
`noise`, `nan`, and `constant` preserve on some frames and promote on others
(§3.2).**" The clause names `nan` in terms, and `nullread` is that sentence
built into a detector: one strategy, two combinations, and which combination a
column belongs to is decided by the column's own dtype.

Line 1084 closes the remaining question -- what a combination with nothing to
do is traced as: "`not_applicable` -- no configured strategy resolves to this
promotion status on this case, **or no eligible cohort was selected for it**.
The second clause covers a combination with resolved strategies, available
inputs, and nothing to do." So an empty combination is legal and has an
explicit state; it is never a missing trace, which line 1078 makes a protocol
violation.

`nullread`'s two combinations PARTITION the columns -- every column is in
exactly one, none in both, none in neither -- and that is asserted at run time
rather than argued here, because a partition claim that nothing checks is the
kind of claim that quietly stops being true.

WHAT `valueread`'s PRESERVING SIDE SHARES WITH `columndep`, said plainly. It is
the same two strategies over the same columns, so on the acceptance fixture it
will reproduce columndep's preserving findings. That is not redundancy: a
detector's two combinations are read against each other, and the promoted side
here is a different strategy from columndep's. A promoted result with no
preserving control in the same detector could not be interpreted.

TERMINATION, unchanged. §6.6 line 1053: on the evaluation corpora, the
conformance suite and the acceptance fixture gate run, every configured
strategy executes at every selected eligible cohort regardless of any finding.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

import pandas as pd

from protocol.runtime_reference import (
    CombinationTrace,
    ExecutionRecord,
    FailureReason,
    PromotionStatus,
    RunContext,
)

from . import corruption as cx
from .determinism import DeterminismResult, check_frame
from .probe import ProbeResult, _call, _run_one, _substitute, cohort_id_for

VALUE_DETECTOR_ID = "valueread"
NULL_DETECTOR_ID = "nullread"


@dataclass(frozen=True)
class Combination:
    """One side of a detector: its strategies, who is eligible, how it promotes.

    `eligible` is a predicate on the column, not a list of names, so the cohort
    set is DERIVED from the data at run time. A hardcoded list would be an
    assertion about dtypes that could silently stop matching the fixture.

    `promoter` is None on a preserving combination and is the function that
    produces the promoted-but-UNPERTURBED column on a promoted one. The
    promoted baseline must be built through it: comparing a promoted perturbed
    run against the ORIGINAL baseline would report the dtype change itself as
    movement, on every feature downstream, every time.
    """
    strategies: tuple[str, ...]
    eligible: Callable[[pd.Series], bool]
    promoter: Callable[[pd.Series], pd.Series] | None = None


def _ood_eligible(series: pd.Series) -> bool:
    try:
        cx.promote_ood(series)
        return True
    except cx.Unsupportable:
        return False


def _nan_preserves(series: pd.Series) -> bool:
    return cx.promotion_of(cx.NAN, series) is PromotionStatus.PRESERVING


def _nan_promotes(series: pd.Series) -> bool:
    return cx.promotion_of(cx.NAN, series) is PromotionStatus.PROMOTED


VALUE_PRESERVING = Combination((cx.SHUFFLE, cx.SENTINEL), lambda s: True)
VALUE_PROMOTED = Combination((cx.SENTINEL_OOD,), _ood_eligible, cx.promote_ood)
NULL_PRESERVING = Combination((cx.NAN,), _nan_preserves)
NULL_PROMOTED = Combination((cx.NAN,), _nan_promotes, cx.promote)


def value_domain_statement() -> str:
    """What `valueread` can and cannot see, DERIVED from its configuration."""
    return (
        "Probed: every source column, under %s in the preserving combination. "
        "The promoted combination runs %s, and its eligible cohorts are a "
        "DTYPE-DEFINED SUBSET -- the columns for which a wider dtype exists at "
        "all (integer -> float64, boolean -> int64). NOT probed by the promoted "
        "side: float columns, because no floating dtype is wider than float64; "
        "object columns, because every value is already representable and there "
        "is nothing to promote to; and datetime columns, because the only wider "
        "thing is the unit, and widening a timestamp's unit changes what the "
        "builder merges on rather than what the column contains. On those three "
        "classes the out-of-dtype sentinel has NO realisation, the record is "
        "`could_not_run(compatibility)` with that reason attached, and the "
        "combination's silence there is not evidence about them. What the "
        "promoted side buys where it does run: a feature that CLIPS or CLAMPS "
        "at the dtype's own bound is invisible to the in-dtype sentinel, which "
        "cannot get past that bound."
        % (", ".join("`%s`" % s for s in VALUE_PRESERVING.strategies),
           ", ".join("`%s`" % s for s in VALUE_PROMOTED.strategies)))


def null_domain_statement() -> str:
    """What `nullread` can and cannot see, DERIVED from its configuration."""
    return (
        "Probed: every source column, under %s. The two combinations PARTITION "
        "the columns by dtype -- preserving where the column already holds a "
        "null in its own dtype (float, datetime, object), promoted where it "
        "does not and the null forces a dtype change (integer, boolean) -- so "
        "every column is in exactly one, and no column is outside the "
        "detector. This is the gap `columndep`'s domain statement published and "
        "could not close: there, `nan` was configured only in the promoted "
        "combination, so a float column never received a null and a feature "
        "reading it only through its null mask was reported silent. Here it "
        "does. NOT probed: nothing on the column axis. What this detector still "
        "cannot see is a feature that reads a null pattern the column does not "
        "have -- introducing a null tests whether nulls are read, never whether "
        "an EXISTING null pattern is read, and a column with no nulls to begin "
        "with cannot answer the second question."
        % ", ".join("`%s`" % s for s in NULL_PRESERVING.strategies))


def probe_values(frames, build, **kw) -> ProbeResult:
    """`valueread` -- does the output read this column's values?"""
    return _run_detector(VALUE_DETECTOR_ID, VALUE_PRESERVING, VALUE_PROMOTED,
                         value_domain_statement(), frames, build, **kw)


def probe_nulls(frames, build, **kw) -> ProbeResult:
    """`nullread` -- does the output read this column's null pattern?"""
    return _run_detector(NULL_DETECTOR_ID, NULL_PRESERVING, NULL_PROMOTED,
                         null_domain_statement(), frames, build, **kw)


def _run_detector(
    detector_id: str,
    preserving: Combination,
    promoted: Combination,
    domain: str,
    frames: dict[str, pd.DataFrame],
    build: Callable[[Any], pd.DataFrame],
    *,
    case_id: str = "user",
    run_context: RunContext = RunContext.USER,
    bare: bool = False,
    columns: tuple[str, ...] | None = None,
    cohorts: tuple[str, ...] | None = None,
) -> ProbeResult:
    """Run one detector's two combinations and emit both traces.

    `cohorts` selects by COHORT ID (`col:<frame>.<column>`) rather than by
    column name, and is what a sharded run partitions on. `columns` selects by
    bare name, which is ambiguous the moment two frames share one -- so a
    sharded caller must use `cohorts`, and a caller that passes both gets the
    intersection.
    """
    targets: list[tuple[str, str]] = []
    for fname, f in frames.items():
        for c in f.columns:
            if columns is not None and c not in columns:
                continue
            if "|" in str(c) or "|" in fname:
                continue        # reserved separator; cannot be a cohort id
            if cohorts is not None and cohort_id_for(fname, str(c)) not in cohorts:
                continue
            targets.append((fname, str(c)))

    # ---- the original-frame determinism guard (§6.10: per frame, not once) --
    det: dict[str, DeterminismResult] = {}
    g0 = check_frame(lambda fr: _call(build, fr, bare), frames, "original")
    det["original"] = g0
    if not g0.deterministic:
        # A build that RAISED on its own unperturbed input was never shown to be
        # nondeterministic; it was shown not to run. §6.6's reason precedence
        # has a name for that and it is CRASH.
        return _failed_frame_result(
            detector_id, preserving, promoted, domain, targets, frames,
            case_id, run_context, det,
            FailureReason.CRASH if g0.raised else FailureReason.DETERMINISM)

    baseline = _call(build, frames, bare)
    baseline_cols = tuple(str(c) for c in baseline.columns)

    pres_records: list[ExecutionRecord] = []
    prom_records: list[ExecutionRecord] = []
    pres_cohorts: list[str] = []
    prom_cohorts: list[str] = []
    depmap: dict[str, tuple[str, ...]] = {}

    for fname, col in targets:
        cid = cohort_id_for(fname, col)
        series = frames[fname][col]
        moved_any: set[str] = set()

        # ---- preserving side -------------------------------------------------
        if preserving.eligible(series):
            pres_cohorts.append(cid)
            for strat in preserving.strategies:
                recs, moved = _run_one(build, frames, bare, baseline, fname, col,
                                       strat, cid, case_id,
                                       PromotionStatus.PRESERVING,
                                       detector_id=detector_id)
                pres_records.extend(recs)
                moved_any |= moved

        # ---- promoted side, against its OWN baseline -------------------------
        if promoted.eligible(series):
            prom_cohorts.append(cid)
            fid = "promoted:%s" % cid
            promoted_frames = _substitute(frames, fname, col,
                                          promoted.promoter(series))
            g = check_frame(lambda fr: _call(build, fr, bare), promoted_frames, fid)
            det[fid] = g
            if not g.deterministic:
                # §6.10: a frame that fails its guard produces NO runtime
                # finding. Every strategy assigned to it is could_not_run.
                for strat in promoted.strategies:
                    prom_records.append(ExecutionRecord(
                        detector_id=detector_id, case_id=case_id,
                        strategy_id=strat,
                        promotion_status=PromotionStatus.PROMOTED, cohort_id=cid,
                        attempted=True, valid=False,
                        failure_reason=(FailureReason.CRASH if g.raised
                                        else FailureReason.DETERMINISM)))
            else:
                prom_base = _call(build, promoted_frames, bare)
                for strat in promoted.strategies:
                    recs, moved = _run_one(build, frames, bare, prom_base, fname,
                                           col, strat, cid, case_id,
                                           PromotionStatus.PROMOTED,
                                           detector_id=detector_id)
                    prom_records.extend(recs)
                    moved_any |= moved

        if moved_any:
            depmap[cid] = tuple(sorted(moved_any))

    return ProbeResult(
        _trace(detector_id, case_id, PromotionStatus.PRESERVING, run_context,
               preserving.strategies, pres_cohorts, pres_records),
        _trace(detector_id, case_id, PromotionStatus.PROMOTED, run_context,
               promoted.strategies, prom_cohorts, prom_records),
        depmap, det, baseline_cols, domain=domain)


def _trace(detector_id, case_id, status, run_context, strategies, cohorts, records):
    """One CombinationTrace.

    `resolved_strategies` is emptied when no cohort was selected, so the trace
    resolves to `not_applicable` under §6.6's rule 1 rather than to a vacuous
    `completed` -- which would have to pair with `none`, and the legality table
    forbids that pair.
    """
    return CombinationTrace(
        detector_id=detector_id, case_id=case_id,
        promotion_status=status, run_context=run_context,
        resolved_strategies=tuple(strategies) if cohorts else (),
        selected_eligible_cohorts=tuple(cohorts),
        required_inputs_available=True,
        terminal_decision_occurred=False,
        records=tuple(records))


def _failed_frame_result(detector_id, preserving, promoted, domain, targets,
                         frames, case_id, run_context, det, reason) -> ProbeResult:
    """Every strategy assigned to a failed frame is could_not_run(reason).

    Both sides are filled, each over ITS OWN eligible cohorts, because a
    combination with no trace has no state (§6.6 l.1078) and an empty promoted
    side here would claim the frame failed for the preserving strategies only.
    """
    pres_c, prom_c = [], []
    for fname, col in targets:
        cid = cohort_id_for(fname, col)
        s = frames[fname][col]
        if preserving.eligible(s):
            pres_c.append(cid)
        if promoted.eligible(s):
            prom_c.append(cid)

    def recs(cohorts, comb, status):
        return [ExecutionRecord(
            detector_id=detector_id, case_id=case_id, strategy_id=st,
            promotion_status=status, cohort_id=cid, attempted=True,
            valid=False, failure_reason=reason)
            for cid in cohorts for st in comb.strategies]

    return ProbeResult(
        _trace(detector_id, case_id, PromotionStatus.PRESERVING, run_context,
               preserving.strategies, pres_c,
               recs(pres_c, preserving, PromotionStatus.PRESERVING)),
        _trace(detector_id, case_id, PromotionStatus.PROMOTED, run_context,
               promoted.strategies, prom_c,
               recs(prom_c, promoted, PromotionStatus.PROMOTED)),
        {}, det, (), domain=domain)
