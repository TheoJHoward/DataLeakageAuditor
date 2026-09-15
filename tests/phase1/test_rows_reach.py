"""Reach in ROWS against a stride in POSITIONS, across an overnight gap. R272 §2(c).

`cohort_stride` counts positions in the sorted decision seconds. A rolling window
counts rows. Where the decision seconds have a gap -- a session ending and the
next starting hours later -- a 60-row window spans hours of clock and still 60
rows, so a separation measured in SECONDS says two cohorts are hours apart while
one sits inside the other's window.

THE PAIR, over one frame and one builder. HELD: two 100-second sessions ten hours
apart, a builder summing the previous 60 rows. VARIED: how the cohorts are spaced.
Two cohorts hours apart in clock time but 5 rows apart across the gap interfere;
a stride of 61 positions, the block reach in rows plus one, does not.
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

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.reach import (ReachError, measure_block_reach,  # noqa: E402
                             measured_rows)

T0 = pd.Timestamp("2026-01-01 09:00:00")
SEC = pd.Timedelta(seconds=1)
GAP = pd.Timedelta(hours=10)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")

A = [T0 + i * SEC for i in range(100)]
B = [T0 + GAP + i * SEC for i in range(100)]


def _frames():
    return {"agg": pd.DataFrame({"k": A + B, "v": np.ones(200)})}


def _roll60(raw):
    """Each row reads the previous 60 ROWS -- available cells, nothing to find."""
    agg = raw["agg"]
    return pd.DataFrame({"d": pd.to_datetime(agg["k"]).to_numpy(),
                         "x": agg["v"].shift(1).rolling(60, min_periods=1).sum().to_numpy()})


def test_the_reach_across_the_gap_is_60_ROWS_and_HOURS_of_seconds():
    frames = _frames()
    rr = measure_block_reach(frames, _roll60, MODEL, _roll60(frames), "d",
                             at_seconds=[A[95]])
    assert measured_rows(rr) == 60, rr.spread()
    assert rr.measured > pd.Timedelta(hours=9), rr.spread()


def test_a_SEPARATION_IN_SECONDS_across_the_gap_INTERFERES():
    """Cohorts hours apart in clock time, five rows apart across the gap: B's
    first row reads A's last cells, available to it, and moves -- a false
    finding a separation in seconds would call safe."""
    res = run_probe_a(_frames(), _roll60, MODEL, side="seconds",
                      cohort_seconds=[A[95], B[0]], reach_samples=0,
                      block_samples=0)
    assert res.min_separation > pd.Timedelta(hours=9)
    assert B[0] in {c.second for c in res.findings}, (
        [str(c.second) for c in res.findings])


def test_a_STRIDE_IN_ROWS_does_not_interfere_across_the_same_gap():
    res = run_probe_a(_frames(), _roll60, MODEL, side="rows", cohort_stride=61,
                      max_cohorts=10 ** 6)
    assert measured_rows(res.block_reach) == 60
    assert res.resolved_stride == 61
    assert not res.findings, [str(c.second) for c in res.findings]


def test_a_DECLARED_stride_below_the_rows_floor_is_REFUSED():
    with pytest.raises(ReachError) as e:
        run_probe_a(_frames(), _roll60, MODEL, side="rows", cohort_stride=40,
                    max_cohorts=10 ** 6)
    assert "40 positions" in str(e.value) and "60 row(s)" in str(e.value)


def test_the_EXACT_model_floor_accepts_a_stride_the_CONVERTED_one_refuses_and_stays_SAFE():
    """R273 §1(c), measured rather than asserted.

    The line R273 asked for -- that no input exists which the exact check accepts
    and a conversion at the smallest spacing refuses -- is FALSE, and this is the
    input. Decision seconds 1 s and 10 s apart, alternately, and a 5 s model
    floor: `_stride_for` takes stride 2, because every probed gap is 11 s;
    converting the floor at the smallest spacing, 1 s, demands stride 5.

    What IS true, and what this pins: the exact check accepts a stride only when
    every gap it actually probes clears the floor, because it computes those gaps
    rather than bounding them. It is less conservative than the conversion and
    no less safe."""
    import math

    from leakaudit.availability import _stride_for
    spacing = [1, 10] * 20
    secs = [T0]
    for s in spacing:
        secs.append(secs[-1] + s * SEC)
    floor = 5 * SEC
    k = _stride_for(secs, floor)
    converted = math.ceil(floor.total_seconds() / min(spacing))
    gaps = [secs[i + k] - secs[i] for i in range(0, len(secs) - k, k)]
    assert (k, converted) == (2, 5)
    assert min(gaps) >= floor, min(gaps)
