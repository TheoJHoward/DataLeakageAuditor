"""Corruption strategies, in the order PREREG.md's promotion semantics require.

THE ORDER IS NOT COSMETIC. `PromotionStatus.PROMOTED` disqualifies PROVEN
(PREREG.md §3.1: preserving -> PROVEN; promoted -> REVIEW dtype_promoted), so a
strategy that promotes the frame's dtype costs the strongest tier available.
Trying the promotion-safe strategies first preserves PROVEN wherever it can be
preserved:

    1. shuffle   type-preserving permutation within the probed domain
    2. sentinel  out-of-range value, still in-dtype
    3. nan       promotes int -> float, and therefore promotes the combination

TERMINATION IS A SEPARATE QUESTION FROM ORDER, and the two must not be conflated.
PREREG.md §6.6 line 1053:

    On the evaluation corpora, the conformance suite, and the acceptance fixture
    gate run, every configured strategy executes at every selected eligible
    cohort, regardless of any finding. No terminal short-circuit applies at any
    level.

So ordering holds everywhere; stopping early is licensed only in a user-facing
run (`RunContext.USER`), where it yields `short_circuited` and leaves every
metric denominator. See `leakaudit.trace.may_short_circuit`.

Comparison is exact throughout (PREREG.md §6.9: bitwise equality, not a
tolerance).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from protocol.runtime_reference import PromotionStatus

# Strategy ids. No "|" anywhere: it is the reserved member/gate separator and
# `protocol.runtime_reference._no_separator` raises on it.
SHUFFLE = "shuffle"
SENTINEL = "sentinel"
NAN = "nan"


def _is_integer(dtype) -> bool:
    return pd.api.types.is_integer_dtype(dtype) and not pd.api.types.is_bool_dtype(dtype)


def promotion_of(strategy_id: str, series: pd.Series) -> PromotionStatus:
    """Promotion status of `strategy_id` ON THIS SERIES.

    PREREG.md §3.2: `noise`, `nan` and `constant` preserve on some frames and
    promote on others, so promotion is per strategy per frame and is resolved
    against the actual column rather than declared once for the strategy.

    PROMOTION IS A DTYPE CHANGE, AND ONLY A DTYPE CHANGE. `nan` promotes exactly
    where the column cannot hold a null in its own dtype -- integer and boolean.
    A float column already holds NaN; a datetime column holds NaT; an object
    column holds None. None of those changes dtype, so none of them promotes.

    An earlier version asked "is this float?" and called everything else
    promoted. That was right for integers by accident and wrong for datetimes,
    where it drove the caller to build a "promoted frame" by casting to float64
    -- which raises. The question is not whether the column is float; it is
    whether inserting a null would change its dtype.
    """
    if strategy_id in (SHUFFLE, SENTINEL):
        return PromotionStatus.PRESERVING
    if strategy_id == NAN:
        if _is_integer(series.dtype) or pd.api.types.is_bool_dtype(series.dtype):
            return PromotionStatus.PROMOTED
        return PromotionStatus.PRESERVING
    raise ValueError("unknown strategy %r" % strategy_id)


def promote(series: pd.Series) -> pd.Series:
    """The series in the dtype `nan` would promote it to.

    Exposed so a caller building a promoted execution frame does not hardcode a
    cast. §6.10 requires each promoted alignment family to carry its own
    determinism guard, so the caller needs the promoted frame -- and the only
    correct way to produce it is to ask the strategy what promotion means here.
    """
    if promotion_of(NAN, series) is PromotionStatus.PRESERVING:
        return series.copy()
    return series.astype("float64")


def _sentinel_value(series: pd.Series):
    """An out-of-range value that stays inside the column's own dtype.

    Chosen from the observed extremes rather than from a dtype limit, so the
    value is out of range for THIS column while remaining representable in it.
    Overflow is avoided by falling back to the dtype's own bound.
    """
    dt = series.dtype
    if _is_integer(dt):
        info = np.iinfo(dt)
        hi = series.max()
        if pd.isna(hi):
            return info.max
        span = abs(int(hi)) + 1
        return info.max if int(hi) > info.max - span else int(hi) + span
    if pd.api.types.is_float_dtype(dt):
        hi = series.max(skipna=True)
        if pd.isna(hi):
            return np.float64(-1.0e300)
        return np.float64(abs(float(hi)) * 1.0e6 + 1.0e6)
    if pd.api.types.is_bool_dtype(dt):
        # A bool column has no out-of-range value in its own dtype. Inverting is
        # the strongest in-dtype perturbation available; reported as such rather
        # than silently promoted to object.
        return None
    if pd.api.types.is_datetime64_any_dtype(dt):
        # Near the ns-resolution ceiling. THE TIMEZONE MUST MATCH: a tz-naive
        # Timestamp assigned into a tz-aware column raises, and the fixture's
        # trades frame carries a UTC-aware stamp. An out-of-range value that
        # cannot be assigned is not an out-of-range value.
        ts = pd.Timestamp("2262-04-11")
        tz = getattr(dt, "tz", None)
        return ts.tz_localize(tz) if tz is not None else ts
    return None


def corrupt(series: pd.Series, strategy_id: str, mask=None, seed: int = 0) -> pd.Series:
    """Return a copy of `series` corrupted under `strategy_id`.

    `mask` selects the cells to corrupt; None means the whole column, which is
    the column probe's domain. The original is never mutated -- an in-place
    corruption would silently poison the baseline it is compared against.
    """
    out = series.copy()
    if mask is None:
        mask = pd.Series(True, index=series.index)
    n = int(mask.sum())
    if n == 0:
        return out

    if strategy_id == SHUFFLE:
        # A permutation of the column's OWN values: the dtype, the multiset of
        # values, and the null pattern's cardinality all survive. If the output
        # moves under this, it moves on row-to-row correspondence alone.
        rng = np.random.default_rng(seed)
        vals = out.loc[mask].to_numpy(copy=True)
        if n > 1:
            for _ in range(8):
                perm = rng.permutation(n)
                if not np.array_equal(perm, np.arange(n)):
                    break
            vals = vals[perm]
        out.loc[mask] = vals
        return out

    if strategy_id == SENTINEL:
        v = _sentinel_value(series)
        if v is None:
            if pd.api.types.is_bool_dtype(series.dtype):
                out.loc[mask] = ~out.loc[mask].astype(bool)
                return out
            raise Unsupportable("no in-dtype out-of-range value exists for dtype %s" % series.dtype)
        out.loc[mask] = v
        return out

    if strategy_id == NAN:
        out = promote(out)                # a no-op where nothing promotes
        out.loc[mask] = (pd.NaT if pd.api.types.is_datetime64_any_dtype(out.dtype)
                         else np.nan)
        return out

    raise ValueError("unknown strategy %r" % strategy_id)


class Unsupportable(Exception):
    """This strategy has no in-dtype realisation on this column.

    Raised rather than silently substituted: a strategy that quietly becomes a
    different strategy reports a finding for a probe that never ran.
    """


# The order in which strategies are attempted. Promotion-safe first.
STRATEGY_ORDER: tuple[str, ...] = (SHUFFLE, SENTINEL, NAN)
