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
    `nan` in an already-float column promotes nothing.
    """
    if strategy_id in (SHUFFLE, SENTINEL):
        return PromotionStatus.PRESERVING
    if strategy_id == NAN:
        if pd.api.types.is_float_dtype(series.dtype):
            return PromotionStatus.PRESERVING
        return PromotionStatus.PROMOTED
    raise ValueError("unknown strategy %r" % strategy_id)


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
        return pd.Timestamp("2262-04-11")  # near the ns-resolution ceiling
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
        if _is_integer(series.dtype) or pd.api.types.is_bool_dtype(series.dtype):
            out = out.astype("float64")   # the promotion, made explicit
        out.loc[mask] = np.nan
        return out

    raise ValueError("unknown strategy %r" % strategy_id)


class Unsupportable(Exception):
    """This strategy has no in-dtype realisation on this column.

    Raised rather than silently substituted: a strategy that quietly becomes a
    different strategy reports a finding for a probe that never ran.
    """


# The order in which strategies are attempted. Promotion-safe first.
STRATEGY_ORDER: tuple[str, ...] = (SHUFFLE, SENTINEL, NAN)
