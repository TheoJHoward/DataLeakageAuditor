"""Corruption across the dtypes the acceptance fixture actually contains.

WHY THESE EXIST. The synthetic tests used int, float and bool. The fixture's
frames also carry tz-naive datetimes, TZ-AWARE datetimes, and object columns, and
every one of those broke something:

  * `promotion_of` asked "is this float?" and called everything else promoted.
    Right for integers by accident, wrong for datetimes -- which drove the sweep
    to build a promoted frame by casting to float64, raising
    `Cannot cast DatetimeArray to dtype float64` and killing four processes
    fifteen minutes in.
  * `_sentinel_value` returned a tz-NAIVE Timestamp for a tz-AWARE column, which
    cannot be assigned into it.

**Promotion is a dtype change and only a dtype change.** `nan` promotes exactly
where the column cannot hold a null in its own dtype: integer and boolean. A
float holds NaN, a datetime holds NaT, an object holds None -- none of those
changes dtype, so none of them promotes.

The synthetic suite could not have caught this. It had a domain narrower than
the data, in the direction that hides the failure until it costs real time.
"""
import numpy as np
import pandas as pd
import pytest

from leakaudit.corruption import (
    NAN,
    SENTINEL,
    SHUFFLE,
    Unsupportable,
    corrupt,
    promote,
    promotion_of,
)
from protocol.runtime_reference import PromotionStatus

PRES, PROM = PromotionStatus.PRESERVING, PromotionStatus.PROMOTED

COLUMNS = {
    "int64": pd.Series([1, 2, 3, 4], dtype="int64"),
    "float64": pd.Series([1.0, 2.0, 3.0, 4.0]),
    "bool": pd.Series([True, False, True, False]),
    "datetime_naive": pd.Series(pd.date_range("2025-01-01", periods=4, freq="s")),
    "datetime_utc": pd.Series(pd.date_range("2025-01-01", periods=4, freq="s",
                                            tz="UTC")),
    "object": pd.Series(["a", "b", "c", "d"]),
}


@pytest.mark.parametrize("name", sorted(COLUMNS))
def test_every_strategy_produces_an_assignable_column(name):
    """Whatever the dtype, a strategy either produces a column or refuses in a
    way the caller can record. It must never raise an unhandled TypeError --
    that is what killed the sweep."""
    s = COLUMNS[name]
    for strat in (SHUFFLE, SENTINEL, NAN):
        try:
            out = corrupt(s, strat)
        except Unsupportable:
            continue                      # a refusal the caller records
        assert len(out) == len(s)
        # the result must be assignable back into a frame of that column
        df = pd.DataFrame({name: s.copy()})
        df[name] = out


@pytest.mark.parametrize("name,expected", [
    ("int64", PROM),
    ("bool", PROM),
    ("float64", PRES),
    ("datetime_naive", PRES),
    ("datetime_utc", PRES),
    ("object", PRES),
])
def test_nan_promotes_exactly_where_a_null_changes_the_dtype(name, expected):
    assert promotion_of(NAN, COLUMNS[name]) is expected


@pytest.mark.parametrize("name", sorted(COLUMNS))
def test_promotion_status_agrees_with_what_corrupt_actually_does(name):
    """The status is a claim about the resulting dtype. Check the claim against
    the result rather than trusting the table -- a status that disagrees with
    the frame it describes is the defect §3.2 keys everything on."""
    s = COLUMNS[name]
    try:
        out = corrupt(s, NAN)
    except Unsupportable:
        pytest.skip("nan has no realisation on %s" % name)
    changed = out.dtype != s.dtype
    assert changed is (promotion_of(NAN, s) is PROM), (
        "%s: dtype %s -> %s but status says %s"
        % (name, s.dtype, out.dtype, promotion_of(NAN, s).value))


@pytest.mark.parametrize("name", sorted(COLUMNS))
def test_promote_is_a_noop_where_nothing_promotes(name):
    s = COLUMNS[name]
    p = promote(s)
    if promotion_of(NAN, s) is PRES:
        assert p.dtype == s.dtype
        pd.testing.assert_series_equal(p, s, check_names=False)
    else:
        assert p.dtype == np.dtype("float64")


def test_sentinel_on_a_tz_aware_column_keeps_the_timezone():
    """A tz-naive Timestamp cannot be assigned into a tz-aware column. An
    out-of-range value that cannot be assigned is not an out-of-range value."""
    s = COLUMNS["datetime_utc"]
    out = corrupt(s, SENTINEL)
    assert out.dtype == s.dtype
    assert str(getattr(out.dtype, "tz", None)) == "UTC"
    assert (out != s).any()


def test_nan_on_a_datetime_column_yields_NaT_and_keeps_the_dtype():
    for name in ("datetime_naive", "datetime_utc"):
        s = COLUMNS[name]
        out = corrupt(s, NAN)
        assert out.dtype == s.dtype, name
        assert out.isna().all(), name


def test_shuffle_preserves_dtype_on_every_column():
    for name, s in COLUMNS.items():
        out = corrupt(s, SHUFFLE)
        assert out.dtype == s.dtype, name
        assert sorted(out.astype(str)) == sorted(s.astype(str)), name
