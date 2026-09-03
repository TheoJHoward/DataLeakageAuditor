"""Each mode's known positive, and its neighbouring-mode negative. R204 §4.

THE SHAPE OF EVERY PAIR. Data where one mode is right and a neighbouring mode is
wrong, and the tool has to tell them apart. A mode that produced the same
instant as its neighbour on every input would be a key name with no arithmetic
behind it, and the pair is what shows it is not.

ONE PAIR CANNOT BE BUILT, and that is reported rather than faked.
`at_source_timestamp` and `explicit` read the same instant out of the same
column; the difference is what the declaration says, not what is computed. No
data distinguishes them, so the test below asserts that they AGREE, and the
distinction is documentary.

The arithmetic under test is `AVAILABILITY_MODES.md`, which was committed
before the module this exercises.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.modes import (                                      # noqa: E402
    ALWAYS, AT_BAR_CLOSE, AT_SOURCE_TIMESTAMP, AT_TIMESTAMP, AVAILABILITY_FN,
    EXPLICIT, FILE_MODES, NEVER_UNAVAILABLE, ColumnMode, ModeError,
    availability, availability_matrix, bar_duration, undeclared_columns)

TS = "ts"


def _frame(n=6, freq="1min"):
    ts = pd.date_range("2026-01-01 09:00:00", periods=n, freq=freq)
    return pd.DataFrame({
        TS: ts,
        "value": np.arange(float(n)),
        "released": ts - pd.Timedelta(minutes=30),   # a source's release instant
        "static": ["ES"] * n,
    })


def _a(frame, column, spec, **kw):
    return availability(frame, column, spec, timestamp_column=TS, **kw)


# ---------------------------------------------------------------------------
# at_timestamp — positive, and at_bar_close as its neighbour
# ---------------------------------------------------------------------------

def test_at_timestamp_is_the_rows_own_stamp():
    f = _frame()
    got = _a(f, "value", ColumnMode(AT_TIMESTAMP))
    assert got.equals(pd.to_datetime(f[TS]))


def test_at_bar_close_gives_a_different_answer_on_the_same_data():
    """THE NEIGHBOUR. A value observed at the stamp and a value summarising the
    bar that opens there are not knowable at the same instant, and the two modes
    must not agree."""
    f = _frame()
    at_ts = _a(f, "value", ColumnMode(AT_TIMESTAMP))
    at_close = _a(f, "value", ColumnMode(AT_BAR_CLOSE))
    assert not at_ts.equals(at_close)
    assert (at_close - at_ts == pd.Timedelta(minutes=1)).all()


# ---------------------------------------------------------------------------
# at_bar_close — the duration rules, including the one implementations drop
# ---------------------------------------------------------------------------

def test_at_bar_close_uses_a_declared_duration_when_given_one():
    f = _frame()
    got = _a(f, "value", ColumnMode(AT_BAR_CLOSE),
             declared_bar_duration=pd.Timedelta(minutes=5))
    assert (got - pd.to_datetime(f[TS]) == pd.Timedelta(minutes=5)).all()


def test_the_final_rows_duration_is_carried_forward_not_left_missing():
    """THE CLAUSE AN IMPLEMENTATION DROPS. There is no successor to measure the
    last bar against, so the last known duration carries forward. Dropping it
    puts a NaT in the final row and quietly excludes that row from every
    comparison."""
    f = _frame(n=5)
    got = _a(f, "value", ColumnMode(AT_BAR_CLOSE))
    assert got.notna().all(), "the final row's availability is missing"
    assert got.iloc[-1] - pd.to_datetime(f[TS]).iloc[-1] == pd.Timedelta(minutes=1)


def test_an_irregular_gap_is_inferred_per_row():
    ts = pd.to_datetime(["2026-01-01 09:00", "2026-01-01 09:01",
                         "2026-01-01 09:05", "2026-01-01 09:06"])
    f = pd.DataFrame({TS: ts, "value": [1.0, 2.0, 3.0, 4.0]})
    got = _a(f, "value", ColumnMode(AT_BAR_CLOSE)) - ts
    assert list(got) == [pd.Timedelta(minutes=1), pd.Timedelta(minutes=4),
                         pd.Timedelta(minutes=1), pd.Timedelta(minutes=1)]


def test_a_single_row_refuses_rather_than_guessing_a_duration():
    f = _frame(n=1)
    with pytest.raises(ModeError, match="guessed from nothing"):
        _a(f, "value", ColumnMode(AT_BAR_CLOSE))


# ---------------------------------------------------------------------------
# at_source_timestamp — positive, with at_timestamp as its neighbour
# ---------------------------------------------------------------------------

def test_at_source_timestamp_reads_the_named_column_not_the_row_stamp():
    """THE POSITIVE, and the whole point of the mode: a figure released on its
    own schedule and carried onto a fast frame is knowable when it was
    RELEASED."""
    f = _frame()
    got = _a(f, "value", ColumnMode(AT_SOURCE_TIMESTAMP, "released"))
    assert got.equals(pd.to_datetime(f["released"]))
    assert not got.equals(pd.to_datetime(f[TS]))


def test_the_neighbour_at_timestamp_is_wrong_by_the_release_lag():
    """THE NEIGHBOURING-MODE NEGATIVE. Declaring at_timestamp on a
    forward-filled exogenous column claims it was knowable half an hour before
    it was released."""
    f = _frame()
    src = _a(f, "value", ColumnMode(AT_SOURCE_TIMESTAMP, "released"))
    at_ts = _a(f, "value", ColumnMode(AT_TIMESTAMP))
    assert ((at_ts - src) == pd.Timedelta(minutes=30)).all()


def test_a_mode_that_reads_a_column_refuses_without_one():
    with pytest.raises(ModeError, match="names no column"):
        ColumnMode(AT_SOURCE_TIMESTAMP)


def test_a_named_column_that_is_absent_is_refused():
    with pytest.raises(ModeError, match="not in the frame"):
        _a(_frame(), "value", ColumnMode(AT_SOURCE_TIMESTAMP, "nope"))


def test_a_named_column_of_unparseable_instants_is_refused():
    """It would compare false against every decision time, which reads as
    available and hides findings."""
    f = _frame()
    f["released"] = "not a time"
    with pytest.raises(ModeError, match="reads as available"):
        _a(f, "value", ColumnMode(AT_SOURCE_TIMESTAMP, "released"))


# ---------------------------------------------------------------------------
# always — positive, with at_timestamp as its neighbour
# ---------------------------------------------------------------------------

def test_always_is_before_every_decision_this_frame_carries():
    f = _frame()
    got = _a(f, "static", ColumnMode(ALWAYS))
    assert (got == NEVER_UNAVAILABLE).all()
    assert (got < pd.to_datetime(f[TS])).all()


def test_the_neighbour_at_timestamp_makes_static_metadata_time_varying():
    """THE NEIGHBOURING-MODE NEGATIVE. A tick size declared at_timestamp becomes
    unknowable before its row, which is false about the world."""
    f = _frame()
    assert not _a(f, "static", ColumnMode(ALWAYS)).equals(
        _a(f, "static", ColumnMode(AT_TIMESTAMP)))


def test_always_refuses_a_column_it_would_not_read():
    with pytest.raises(ModeError, match="does not read one"):
        ColumnMode(ALWAYS, "released")


# ---------------------------------------------------------------------------
# explicit — and the pair that CANNOT be distinguished
# ---------------------------------------------------------------------------

def test_explicit_reads_the_named_column():
    f = _frame()
    got = _a(f, "value", ColumnMode(EXPLICIT, "released"))
    assert got.equals(pd.to_datetime(f["released"]))


def test_explicit_and_at_source_timestamp_AGREE_and_that_is_the_finding():
    """NO DATA DISTINGUISHES THESE TWO. They read the same instant out of the
    same column; the difference is what the declaration says. A test claiming to
    tell them apart would be testing nothing, so this asserts the agreement
    instead -- and the distinction is documentary, which
    `AVAILABILITY_MODES.md` states."""
    f = _frame()
    assert _a(f, "value", ColumnMode(EXPLICIT, "released")).equals(
        _a(f, "value", ColumnMode(AT_SOURCE_TIMESTAMP, "released")))


# ---------------------------------------------------------------------------
# availability_fn — the escape hatch, and its refusals
# ---------------------------------------------------------------------------

def test_availability_fn_returns_whatever_the_callable_computes():
    f = _frame()
    got = _a(f, "value", ColumnMode(AVAILABILITY_FN),
             fn=lambda fr, c: pd.to_datetime(fr[TS]) - pd.Timedelta(hours=1))
    assert (pd.to_datetime(f[TS]) - got == pd.Timedelta(hours=1)).all()


def test_the_escape_hatch_refuses_without_a_callable():
    with pytest.raises(ModeError, match="somewhere to go"):
        _a(_frame(), "value", ColumnMode(AVAILABILITY_FN))


def test_a_short_result_is_refused_rather_than_broadcast():
    """Recycling a short result gives every row after the first cycle an instant
    computed for a different row."""
    with pytest.raises(ModeError, match="Refused rather than broadcast"):
        _a(_frame(), "value", ColumnMode(AVAILABILITY_FN),
           fn=lambda fr, c: pd.to_datetime(["2026-01-01"]))


def test_a_non_timestamp_result_is_refused():
    with pytest.raises(ModeError, match="not\n?\\s*timestamps|are not"):
        _a(_frame(), "value", ColumnMode(AVAILABILITY_FN),
           fn=lambda fr, c: ["x"] * len(fr))


def test_the_escape_hatch_is_not_a_file_mode():
    """A file cannot carry a function, and a mode declarable only in Python does
    not belong in a document a user may hash into their own registration."""
    assert AVAILABILITY_FN not in FILE_MODES
    assert set(FILE_MODES) == {AT_TIMESTAMP, AT_BAR_CLOSE, AT_SOURCE_TIMESTAMP,
                               ALWAYS, EXPLICIT}


# ---------------------------------------------------------------------------
# Undeclared columns are reported, never defaulted
# ---------------------------------------------------------------------------

def test_an_undeclared_column_gets_no_mode_and_is_named():
    f = _frame()
    modes = {"value": ColumnMode(AT_TIMESTAMP)}
    assert "value" not in undeclared_columns(f, modes, timestamp_column=TS)
    assert set(undeclared_columns(f, modes, timestamp_column=TS)) == {
        "released", "static"}


def test_the_matrix_covers_exactly_what_was_declared():
    f = _frame()
    m = availability_matrix(f, {"value": ColumnMode(AT_TIMESTAMP),
                                "static": ColumnMode(ALWAYS)},
                            timestamp_column=TS)
    assert set(m) == {"value", "static"}


def test_an_unknown_mode_is_refused_naming_the_ones_that_exist():
    with pytest.raises(ModeError) as e:
        ColumnMode("at_bar_open")
    assert "at_bar_close" in str(e.value)
