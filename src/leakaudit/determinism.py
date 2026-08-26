"""The determinism guard (PREREG.md §6.9, §6.10).

PER EXECUTION FRAME, NOT ONCE. §6.10, registered:

    The guard runs on every execution frame, not once. A pipeline can be
    deterministic on its original integer frame and nondeterministic on a
    promoted float or complex branch. With a single original-frame guard, that
    pipeline passes, and a promoted run then reports a difference caused by
    nondeterminism as though it were caused by intervention.

    Each distinct execution frame carries its own determinism guard: the
    original frame for preserving runs, and each promoted alignment family for
    the strategies that use it.

    A frame that fails its guard produces no runtime finding. It is recorded as
    could_not_run(determinism) for the strategies assigned to it. There is no
    routing decision, no fallback, and no configuration parameter selecting
    between outcomes.

So a failing frame does NOT downgrade to RULE or REVIEW. It yields no runtime
finding at all -- RULE findings arise only from deterministic declared rules
(§6.12), which is a different mechanism, not a weaker version of this one.

NO TOLERANCE. §6.9: "decided by bitwise equality, not a tolerance." A tolerance
is a tunable knob, and a tunable knob on the comparison is a knob on PROVEN.
Values AND dtypes are compared; a pipeline that returns the same numbers in a
different dtype has not returned the same frame.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DeterminismResult:
    frame_id: str
    deterministic: bool
    differing_columns: tuple[str, ...] = ()
    detail: str = ""
    raised: bool = False
    """True when `build` could not run at all on its OWN unperturbed input.

    THIS IS NOT A DETERMINISM FAILURE AND MUST NOT BE REPORTED AS ONE. A
    pipeline that raises on the input it was given has not been shown to be
    nondeterministic -- it has been shown not to run, which `FailureReason.CRASH`
    names and `DETERMINISM` does not. Collapsing the two would report
    `could_not_run(determinism)` for a caller who simply passed the wrong object,
    and a wrong reason is worse than an absent one: it sends the next reader to
    look for nondeterminism that was never there.
    """

    def __bool__(self) -> bool:
        return self.deterministic


def frames_equal(a: pd.DataFrame, b: pd.DataFrame) -> tuple[bool, tuple[str, ...], str]:
    """Exact comparison: shape, index, columns, dtypes, then values.

    Returns (equal, differing_columns, detail). NaN is treated as equal to NaN
    in the same position -- that is positional identity, not a tolerance: two
    runs that both produced a null in the same cell agree about that cell.
    """
    if list(a.columns) != list(b.columns):
        only_a = [c for c in a.columns if c not in set(b.columns)]
        only_b = [c for c in b.columns if c not in set(a.columns)]
        return False, tuple(only_a + only_b), (
            "column sets differ: %d vs %d (only in run1: %s; only in run2: %s)"
            % (len(a.columns), len(b.columns), only_a[:8], only_b[:8]))
    if a.shape != b.shape:
        return False, (), "shape differs: %s vs %s" % (a.shape, b.shape)
    if not a.index.equals(b.index):
        return False, (), "index differs"

    differing = []
    dtype_only = []
    for c in a.columns:
        if a[c].dtype != b[c].dtype:
            differing.append(c)
            dtype_only.append("%s(%s->%s)" % (c, a[c].dtype, b[c].dtype))
            continue
        s1, s2 = a[c], b[c]
        same = (s1.isna() & s2.isna()) | (s1 == s2)
        if not bool(same.all()):
            differing.append(c)
    if differing:
        d = "%d column(s) differ between two unperturbed runs" % len(differing)
        if dtype_only:
            d += "; dtype changes: " + ", ".join(dtype_only[:8])
        return False, tuple(differing), d
    return True, (), ""


def check_frame(build, frame, frame_id: str) -> DeterminismResult:
    """Run `build` twice on identical input and compare exact.

    `build` is called with the SAME object both times, exactly as the audit
    calls it, so anything the pipeline does to its input is part of what is
    being tested. If the pipeline mutates its input, the second run sees the
    mutation -- and that is a real nondeterminism from the caller's point of
    view, which is the point of view that matters.
    """
    try:
        r1 = build(frame)
        r2 = build(frame)
    except Exception as e:                                  # noqa: BLE001
        return DeterminismResult(frame_id, False, (),
                                 "build raised on its own unperturbed input: %s: %s"
                                 % (type(e).__name__, e), raised=True)
    if r1 is None or r2 is None:
        return DeterminismResult(frame_id, False, (), "build returned None",
                                 raised=True)
    ok, cols, detail = frames_equal(r1, r2)
    return DeterminismResult(frame_id, ok, cols, detail)


def baseline_of(build, frame):
    """The unperturbed output. Called only after `check_frame` passed."""
    return build(frame)
