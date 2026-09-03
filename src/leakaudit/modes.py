"""The availability modes: `a(j, c)` per column. R204 P5.

THE ARITHMETIC WAS WRITTEN BEFORE THIS FILE. `AVAILABILITY_MODES.md` states what
each mode computes and was committed before any parser existed, so the mapping
is what this implements rather than what this happened to do. Where the two
disagree, the document is right and this is a defect.

The vocabulary is the registration's `column_roles` vocabulary, quoted in that
document from `DESIGN.md` §2.1 with its supporting rules cited.

    at_timestamp          ts[j]
    at_bar_close          ts[j] + bar_duration(j)
    at_source_timestamp   the named source column's value at row j
    always                negative infinity
    explicit              the named column's value at row j
    availability_fn       whatever the user's callable returns

TWO OF THEM COMPUTE THE SAME THING. `at_source_timestamp` and `explicit` both
read an instant out of a named column at row j; the difference is what the
declaration says, not what is computed. No data distinguishes them, and this
module does not pretend otherwise -- they share an implementation and the
docstring says so.

WHAT THIS COMPUTES IS THE LEFT-HAND SIDE ONLY. Whether a cell is available to a
row is settled by the comparator registered at `PREREG.md` §2.3 and is not
restated here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd

AT_TIMESTAMP = "at_timestamp"
AT_BAR_CLOSE = "at_bar_close"
AT_SOURCE_TIMESTAMP = "at_source_timestamp"
ALWAYS = "always"
EXPLICIT = "explicit"
AVAILABILITY_FN = "availability_fn"

#: The modes a config FILE may declare. `availability_fn` is absent on purpose:
#: a file cannot carry a function, and a mode declarable only by writing Python
#: does not belong in a document a user may hash into their own registration.
FILE_MODES = (AT_TIMESTAMP, AT_BAR_CLOSE, AT_SOURCE_TIMESTAMP, ALWAYS, EXPLICIT)
ALL_MODES = FILE_MODES + (AVAILABILITY_FN,)

#: Modes that name a column alongside themselves.
MODES_TAKING_A_COLUMN = (AT_SOURCE_TIMESTAMP, EXPLICIT)

#: Negative infinity as a timestamp. `pd.Timestamp.min` is the representable
#: floor; using it rather than a sentinel keeps `a(j,c)` a timestamp everywhere,
#: so a comparator never has to special-case one mode.
NEVER_UNAVAILABLE = pd.Timestamp.min


class ModeError(Exception):
    """A column's mode cannot be applied as declared."""


@dataclass(frozen=True)
class ColumnMode:
    """One column's declared rule, and the column it names if it names one."""
    mode: str
    column: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in ALL_MODES:
            raise ModeError(
                "unknown mode %r. The modes are %s -- and %r is reachable only "
                "from the library, not from a file, because a file cannot carry "
                "a function." % (self.mode, list(FILE_MODES), AVAILABILITY_FN))
        if self.mode in MODES_TAKING_A_COLUMN and not self.column:
            raise ModeError(
                "mode %r names no column. It reads the availability instant OUT "
                "of a column, so without one there is nothing to read and the "
                "mode would silently fall back to the row's own stamp -- which "
                "is a different mode with a different answer." % self.mode)
        if self.mode not in MODES_TAKING_A_COLUMN and self.column:
            raise ModeError(
                "mode %r was given the column %r and does not read one. Refused "
                "rather than ignored: a column named and unused is a declaration "
                "the tool did not apply." % (self.mode, self.column))


# Which `bar_duration` route each `at_bar_close` computation took, in order.
# Read by the probe so the run can say so; a list rather than a flag because a
# frame may carry several such columns and "some were inferred" is not the same
# statement as "all were".
ROUTE_TAKEN: list[str] = []


def bar_duration(ts: pd.Series, declared: pd.Timedelta | None = None) -> pd.Series:
    """The bar length at each row.

    `DESIGN.md` §2.1 and `PREREG.md` §2.3: the declared bar length, or under
    `inferred` the gap to the next timestamp -- and AT THE FINAL ROW THE LAST
    KNOWN DURATION IS CARRIED FORWARD, since there is no successor to measure
    against. That last clause is the one an implementation drops, and dropping
    it puts a NaT in the final row's availability and quietly excludes it.
    """
    ts = pd.to_datetime(ts)
    if declared is not None:
        return pd.Series([declared] * len(ts), index=ts.index)
    if len(ts) == 0:
        return pd.Series([], index=ts.index, dtype="timedelta64[ns]")
    gaps = ts.shift(-1) - ts
    if len(ts) > 1:
        gaps.iloc[-1] = gaps.iloc[-2]
    else:
        raise ModeError(
            "bar_duration was inferred from a single row, which has no "
            "successor and no predecessor to carry forward from. Declare the "
            "bar length rather than have one guessed from nothing.")
    return gaps


def availability(frame: pd.DataFrame, column: str, spec: ColumnMode, *,
                 timestamp_column: str,
                 declared_bar_duration: pd.Timedelta | None = None,
                 fn: Callable | None = None) -> pd.Series:
    """`a(j, c)` for every row of one column, per `AVAILABILITY_MODES.md`."""
    if column not in frame.columns:
        raise ModeError("column %r is not in the frame" % column)

    if spec.mode == ALWAYS:
        # a(j,c) = negative infinity. The cell was knowable before any decision
        # this frame contains.
        return pd.Series([NEVER_UNAVAILABLE] * len(frame), index=frame.index)

    if spec.mode == AVAILABILITY_FN:
        if fn is None:
            raise ModeError(
                "column %r declares %r and no callable was supplied. The mode is "
                "the escape hatch and the escape needs somewhere to go."
                % (column, AVAILABILITY_FN))
        out = fn(frame, column)
        # THE LENGTH IS CHECKED BEFORE THE SERIES IS BUILT. Handing a short
        # result to the Series constructor raises a pandas ValueError about
        # index lengths -- a detection surfacing as somebody else's exception,
        # which is the failure mode the identity control was hardened against
        # twice. The message below is this package's, and it says why.
        if len(out) != len(frame):
            raise ModeError(
                "the callable for column %r returned %d value(s) for %d row(s). "
                "Refused rather than broadcast: a short result would be "
                "recycled across rows and every row after the first cycle would "
                "carry an instant computed for a different one."
                % (column, len(out), len(frame)))
        if not isinstance(out, pd.Series):
            out = pd.Series(list(out), index=frame.index)
        out = pd.to_datetime(out, errors="coerce")
        if out.isna().any():
            raise ModeError(
                "the callable for column %r returned %d value(s) that are not "
                "timestamps. An unparseable availability instant compares false "
                "against every decision time, which reads as available and hides "
                "findings." % (column, int(out.isna().sum())))
        return out

    if spec.mode in MODES_TAKING_A_COLUMN:
        # at_source_timestamp and explicit: the SAME arithmetic. The difference
        # is what the declaration says, and no data distinguishes them.
        src = spec.column
        if src not in frame.columns:
            raise ModeError(
                "column %r declares mode %r naming %r, which is not in the "
                "frame. The instant it would read is not there."
                % (column, spec.mode, src))
        out = pd.to_datetime(frame[src], errors="coerce")
        if out.isna().all() and len(frame):
            raise ModeError(
                "column %r declares mode %r naming %r, and no value in %r parses "
                "as a timestamp. A column of unparseable instants would compare "
                "false against every decision time, which reads as available."
                % (column, spec.mode, src, src))
        return out

    if timestamp_column not in frame.columns:
        raise ModeError(
            "column %r declares mode %r, which reads the frame's timestamp "
            "column %r, and that column is not in the frame."
            % (column, spec.mode, timestamp_column))
    ts = pd.to_datetime(frame[timestamp_column])

    if spec.mode == AT_TIMESTAMP:
        return ts
    if spec.mode == AT_BAR_CLOSE:
        # THE ROUTE TAKEN IS RECORDED, because the registration names TWO and no
        # default between them. R223 §2.
        #
        # `PREREG.md` line 255 is `bar_duration`'s only appearance in the whole
        # registration: "fixed value, OR inferred from successive timestamps".
        # Two routes joined by "or", with no default named -- and the same
        # registration DOES name defaults when it means to, marking `available`
        # "(default)" in §2.3's tie table and saying so again in prose.
        #
        # So the tool is selecting where the registration does not. Until that is
        # ruled, the selection is at least VISIBLE: which route ran is recorded
        # on the call rather than left for a reader to deduce from whether a
        # duration was passed. A result whose method is invisible is the tie
        # comparator problem again, and that half needed no structural read.
        ROUTE_TAKEN.append(
            "declared" if declared_bar_duration is not None else "inferred")
        return ts + bar_duration(ts, declared_bar_duration)

    raise ModeError("unreachable: mode %r has no branch" % spec.mode)


def availability_matrix(frame: pd.DataFrame, modes: dict, *,
                        timestamp_column: str,
                        declared_bar_duration: pd.Timedelta | None = None,
                        fn: Callable | None = None) -> dict[str, pd.Series]:
    """`a(j, c)` for every declared column.

    A column with no declared mode is NOT given one. It is absent from the
    result, and the caller reports it as undeclared rather than assuming a
    default -- an assumed mode is an availability model the user did not write.
    """
    return {c: availability(frame, c, spec,
                            timestamp_column=timestamp_column,
                            declared_bar_duration=declared_bar_duration, fn=fn)
            for c, spec in modes.items()}


def undeclared_columns(frame: pd.DataFrame, modes: dict, *,
                       timestamp_column: str | None = None) -> tuple[str, ...]:
    """Columns the frame carries and the model does not describe.

    Reported, never defaulted. The timestamp column is excluded because it is
    the frame's clock rather than one of its values.
    """
    return tuple(sorted(c for c in frame.columns
                        if c not in modes and c != timestamp_column))
