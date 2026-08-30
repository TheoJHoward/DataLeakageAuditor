"""The input contract.

    audit(raw, build, availability=None, decision_time=None,
          train_idx=None, test_idx=None, meta=None) -> CombinationTrace

WHY `raw` IS A DICT OF FRAMES. A single-frame contract cannot express a
cross-frame join, and the acceptance fixture's pipeline performs two of them:

    snap["ts_floor"] = snap["timestamp"].dt.floor("1s")
    trades["ts_floor"] = trades["ts_event"].dt.floor("1s")
    snap = snap.merge(tagg,  on="ts_floor", how="left")   # trades aggregate
    snap = snap.merge(magg, on="ts_floor", how="left")    # MBO aggregate

The `ts_floor` join is the fixture's own headline availability channel: a trade
aggregate over the wall-clock second [ts_floor, ts_floor+1s) completes at
ts_floor+1s, which can lie strictly after the row stamp T that consumes it. An
instrument that cannot represent the second frame cannot probe the join, and an
instrument narrower than its claim fails in the direction that hides findings.

RECORDED, BECAUSE IT IS THE REASON THE CONTRACT IS NOT NARROWER: the k6
comparison harness -- the surface this contract otherwise follows, discovered
across eleven tools -- passes a SINGLE frame in all eight of its cases (`raw` is
either the built frame itself with `build=lambda d: d`, or one source frame).
Validating this interface against k6 alone would have produced a single-frame
contract that the acceptance fixture cannot use. An interface validated only
against the harness that motivated it inherits that harness's blind spot.

A bare frame is sugar for `{"raw": frame}`, so the k6 surface still works
unchanged with two positional arguments.

WHAT THE GATE MAY PASS IS NARROWER THAN THIS SIGNATURE. PREREG.md SC-7(a): at
gate time a detector receives exactly two things, for one side at a time -- the
pipeline for that side, and the availability declaration's declared elements.
This signature is the library surface; `leakaudit.trace.gate_inputs_only`
enforces the narrower gate surface at the call site that matters.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import pandas as pd

from protocol.runtime_reference import CombinationTrace, FailureReason, RunContext

RawFrames = Mapping[str, pd.DataFrame]


class ContractError(Exception):
    """The call does not satisfy the input contract."""


@dataclass(frozen=True)
class Alignment:
    """The relationship between build's output and the decision-time series.

    An index mismatch is a RESULT, never an exception: PREREG.md §6.6 gives it
    `FailureReason.ALIGNMENT`, and a crash would lose the trace that has to
    carry it.
    """
    ok: bool
    reason: FailureReason | None = None
    detail: str = ""


def normalise_raw(raw) -> dict[str, pd.DataFrame]:
    """A bare frame is sugar for {"raw": frame}; a mapping passes through.

    Frame NAMES matter: they are the cohort prefix a column probe reports, so
    two frames carrying a column of the same name stay distinguishable.
    """
    if isinstance(raw, pd.DataFrame):
        return {"raw": raw}
    if isinstance(raw, Mapping):
        out = {}
        for k, v in raw.items():
            if not isinstance(k, str):
                raise ContractError("raw frame keys must be strings, got %r" % type(k).__name__)
            if "|" in k:
                raise ContractError(
                    "raw frame name %r contains '|', the reserved member/gate separator" % k)
            if not isinstance(v, pd.DataFrame):
                raise ContractError(
                    "raw[%r] must be a DataFrame, got %s" % (k, type(v).__name__))
            out[k] = v
        if not out:
            raise ContractError("raw is empty: there is nothing to probe")
        return out
    raise ContractError(
        "raw must be a DataFrame or a mapping of name -> DataFrame, got %s"
        % type(raw).__name__)


def check_build(build: Callable) -> None:
    if not callable(build):
        raise ContractError("build must be callable, got %s" % type(build).__name__)


def resolve_decision_time(built: pd.DataFrame, decision_time) -> tuple[pd.Series | None, Alignment]:
    """Resolve `decision_time` to one value per OUTPUT row.

    Accepts a column name present in the built frame, or a callable of the built
    frame returning a per-row series. Index misalignment returns
    `FailureReason.ALIGNMENT`; it does not raise.
    """
    if decision_time is None:
        return None, Alignment(True)

    if isinstance(decision_time, str):
        if decision_time not in built.columns:
            return None, Alignment(
                False, FailureReason.ALIGNMENT,
                "decision_time column %r is not in build's output (%d columns)"
                % (decision_time, len(built.columns)))
        series = built[decision_time]
    elif callable(decision_time):
        try:
            series = decision_time(built)
        except Exception as e:                              # noqa: BLE001
            return None, Alignment(False, FailureReason.CRASH,
                                   "decision_time callable raised: %s: %s"
                                   % (type(e).__name__, e))
        if not isinstance(series, pd.Series):
            try:
                series = pd.Series(series, index=built.index)
            except Exception:                               # noqa: BLE001
                return None, Alignment(
                    False, FailureReason.ALIGNMENT,
                    "decision_time returned %s, which does not align to build's "
                    "output index" % type(series).__name__)
    else:
        return None, Alignment(
            False, FailureReason.ALIGNMENT,
            "decision_time must be a column name or a callable, got %s"
            % type(decision_time).__name__)

    if len(series) != len(built):
        return None, Alignment(
            False, FailureReason.ALIGNMENT,
            "decision_time has %d values for %d output rows" % (len(series), len(built)))
    if not series.index.equals(built.index):
        return None, Alignment(
            False, FailureReason.ALIGNMENT,
            "decision_time's index does not match build's output index")
    return series, Alignment(True)


def audit(
    raw,
    build: Callable[[Any], pd.DataFrame],
    availability=None,
    decision_time=None,
    train_idx=None,
    test_idx=None,
    meta=None,
    *,
    case_id: str = "user",
    run_context: RunContext = RunContext.USER,
) -> CombinationTrace:
    """Audit one pipeline and return its preserving-combination trace.

    TWO ARGUMENTS IS THE ENTRY POINT. `audit(raw, build)` runs Layer 1 -- the
    column dependency probe -- and needs no availability model, no decision
    time, and no split. That is deliberate: the zero-configuration layer is the
    adoption surface, and a tool whose first useful result requires a declared
    availability model has no first useful result.

    `availability=None` means no AVAILABILITY verdict is produced, because
    without declared elements there is nothing to violate. It does not mean no
    result: the dependency map is Layer 1's product.

    Returns the PRESERVING trace. `leakaudit.probe.probe_columns` returns both
    combinations plus the dependency map, and is what a harness calls.
    """
    from .probe import probe_columns

    frames = normalise_raw(raw)
    check_build(build)
    # `bare` is carried, not re-derived: a caller who passed one frame gets that
    # frame back in `build`, exactly as k6's `build=lambda d: d` expects. Losing
    # this hands the pipeline a dict it never asked for, and the failure then
    # surfaces as a determinism or crash reason about the pipeline rather than
    # as what it is -- a contract error on our side.
    bare = isinstance(raw, pd.DataFrame)
    result = probe_columns(
        frames, build, bare=bare,
        case_id=case_id, run_context=run_context,
        decision_time=decision_time, availability=availability,
        train_idx=train_idx, test_idx=test_idx, meta=meta,
    )
    return result.preserving
