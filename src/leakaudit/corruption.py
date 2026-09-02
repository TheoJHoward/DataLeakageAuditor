"""Corruption strategies, in the order PREREG.md's promotion semantics require.

THE ORDER IS NOT COSMETIC. `PromotionStatus.PROMOTED` disqualifies PROVEN
(PREREG.md §3.1: preserving -> PROVEN; promoted -> REVIEW dtype_promoted), so a
strategy that promotes the frame's dtype costs the strongest tier available.
Trying the promotion-safe strategies first preserves PROVEN wherever it can be
preserved:

    1. shuffle       type-preserving permutation within the probed domain
    2. sentinel      out-of-range value, still in-dtype
    3. nan           promotes int -> float, and therefore promotes the combination
    4. sentinel_ood  a value the column's own dtype cannot hold, so it promotes
                     unconditionally -- and where no wider dtype exists it has
                     NO realisation and says so, rather than degrading into (2)

TERMINATION IS A SEPARATE QUESTION FROM ORDER, and the two must not be conflated.
PREREG.md §6.6 line 1053:

    On the evaluation corpora, the conformance suite, and the acceptance fixture
    gate run, every configured strategy executes at every selected eligible
    cohort, regardless of any finding. No terminal short-circuit applies at any
    level.

So ordering holds everywhere. The registration licenses stopping early only in a
user-facing run, where it yields `short_circuited` and leaves every metric
denominator; the rule is PREREG.md §6.6 and §7.7 and is not restated here.

**NO SHORT-CIRCUIT IS IMPLEMENTED IN THIS PACKAGE.** Every trace it emits carries
`terminal_decision_occurred=False`, in all four emitters. *(This sentence
previously cited a helper that decides the policy. No such helper was ever
written, and the citation was found by the citation check rather than by review
-- which is the case that check was built for.)*

Comparison is exact throughout (PREREG.md §6.9: bitwise equality, not a
tolerance).
"""
from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd

from protocol.runtime_reference import PromotionStatus

# Strategy ids. No "|" anywhere: it is the reserved member/gate separator and
# `protocol.runtime_reference._no_separator` raises on it.
SHUFFLE = "shuffle"
SENTINEL = "sentinel"
SENTINEL_OOD = "sentinel_ood"
NAN = "nan"


def seed_for(*parts) -> int:
    """A perturbation seed stable across processes, runs and machines.

    FOUND AT R134, IN THE INSTRUMENT, WHILE READING IT FOR B9. Every caller
    previously computed `abs(hash((frame, column, strategy))) % 2**31`. CPython
    salts `hash()` for `str` with `PYTHONHASHSEED`, which is random per process
    unless pinned -- so the same cohort drew a DIFFERENT permutation on every
    run, and the four sweep workers each drew from a different salt.

    Nothing it produced was invalid: any permutation is a legitimate shuffle,
    and the identity case is caught explicitly as `control_artifact`. What it
    lacked is REPRODUCIBILITY. An evidence record that cannot be re-run to the
    same trace is a measurement nobody can check, and a shuffle that happens to
    move nothing on one draw and something on the next turns `observed_silence`
    into a coin toss.

    SHA-256 is used rather than `hash()` because the requirement is a stable
    function of the key, not a fast one -- this is called once per (cohort,
    strategy), not in a loop. The unit separator joins the parts so that
    ("ab", "c") and ("a", "bc") cannot collide.
    """
    key = "\x1f".join(str(p) for p in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(key).digest()[:4], "big")


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
    if strategy_id == SENTINEL_OOD:
        # Definitionally a promotion: the value it inserts is one the column's
        # own dtype cannot hold, so inserting it changes the dtype or the
        # strategy has no realisation at all. It is never preserving, and where
        # no wider dtype exists `corrupt` raises `Unsupportable` rather than
        # quietly becoming the in-dtype sentinel.
        return PromotionStatus.PROMOTED
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


def _ood_target_dtype(series: pd.Series):
    """The narrowest dtype that can hold a value the column's own dtype cannot.

    THE ELIGIBILITY OF THE OUT-OF-DTYPE SENTINEL IS DERIVED HERE, and it is a
    dtype-defined subset of the columns. `PREREG.md` §6.6 line 1080 permits
    exactly this -- "a combination is execution-eligible for a case when at
    least one configured strategy resolves to that promotion status on that
    case" -- and names `nan` as the reason eligibility is per case rather than
    per configuration. Line 1084 then gives a combination with no eligible
    cohort a legal state, `not_applicable`.

    Returns None where no such dtype exists. The three Nones are not an
    oversight and each is a different reason:

      float    -- there is no wider floating dtype. A magnitude outside float64
                  is not representable as a float at all, so "out of dtype but
                  still a number" does not exist here.
      object   -- every value is representable, so no insertion can change the
                  dtype. There is nothing to promote TO.
      datetime -- a wider UNIT exists, but widening the unit of a timestamp
                  changes what the builder merges on. That is a different
                  perturbation from inserting an out-of-domain value, and a
                  strategy that quietly becomes a different strategy reports a
                  finding for a probe that never ran.

    Each reason is returned with the refusal rather than collapsed into one
    message, because "no realisation" without its ground is the silence §39
    forbids.
    """
    dt = series.dtype
    if _is_integer(dt):
        return "float64"
    if pd.api.types.is_bool_dtype(dt):
        return "int64"
    return None


def _ood_refusal(series: pd.Series) -> str:
    """Why the out-of-dtype sentinel has no realisation on this column."""
    dt = series.dtype
    if pd.api.types.is_float_dtype(dt):
        return ("no floating dtype is wider than %s, so a value outside it is "
                "not a number at all" % dt)
    if pd.api.types.is_datetime64_any_dtype(dt):
        return ("%s has a wider unit, but widening a timestamp's unit changes "
                "what the builder merges on -- a different perturbation from "
                "the one this strategy names" % dt)
    return ("every value is representable in %s, so no insertion changes the "
            "dtype and there is nothing to promote to" % dt)


def promote_ood(series: pd.Series) -> pd.Series:
    """The series in the dtype an out-of-dtype sentinel would promote it to.

    The mirror of `promote()` for `nan`, and exposed for the same reason: a
    caller building a promoted execution frame must ask the strategy what
    promotion means here rather than hardcoding a cast. §6.10 requires each
    promoted alignment family to carry its own determinism guard, which needs
    the promoted-but-unperturbed frame.
    """
    target = _ood_target_dtype(series)
    if target is None:
        raise Unsupportable("out-of-dtype sentinel: " + _ood_refusal(series))
    return series.astype(target)


def _sentinel_ood_value(series: pd.Series):
    """A value outside the column's OWN dtype, representable in the wider one.

    Out of the DTYPE, not merely out of the observed range -- that is what
    separates this from `_sentinel_value`, which deliberately stays inside the
    dtype and is therefore capped by it. A feature that clips or clamps at the
    dtype's own bound is invisible to the in-dtype sentinel, because the
    in-dtype sentinel cannot get past that bound. This one can.
    """
    dt = series.dtype
    if _is_integer(dt):
        return np.float64(np.iinfo(dt).max) * 2.0
    if pd.api.types.is_bool_dtype(dt):
        return 2                    # not a boolean, and arithmetic-safe
    return None


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

    if strategy_id == SENTINEL_OOD:
        v = _sentinel_ood_value(series)
        out = promote_ood(series)         # raises Unsupportable where none exists
        if v is None:
            raise Unsupportable(
                "no out-of-dtype sentinel value exists for dtype %s" % series.dtype)
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


# The order in which strategies are attempted. Promotion-safe first, then the
# two promoting ones. `sentinel_ood` joins at R134/B9; it is unconditionally
# promoting, so it can only ever sit after both preserving strategies, and its
# position relative to `nan` is free because neither can preserve PROVEN for
# the other.
STRATEGY_ORDER: tuple[str, ...] = (SHUFFLE, SENTINEL, NAN, SENTINEL_OOD)
