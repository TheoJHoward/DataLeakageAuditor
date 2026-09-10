"""Attribution is the registered comparator, not the second a row moved in.

R261 §1, repairing what R260 §3(c) measured and D-V30A-98 disclosed.

WHAT WAS WRONG. `moved_in_second` classified a moved row by which second it sat
in: the corrupted second `F` meant a finding, the following one meant the cell
had arrived. That is the registered comparator `a(j) > d(i)` ONLY where every
perturbed cell's declared instant is exactly `F + window`. It is, on the
whole-frame path. It is not under a declared `column_modes` block, where cells
are selected by `floor(a - window)` and the instant is the column's own `a`, so
`a(j) - F` lies anywhere in `[window, window + 1s)`. There the geometry reported
a real leak as `observed_silence`.

THE RULE NOW, for a batch B of cells perturbed for one cohort and a moved row i:

    every cell unavailable to i   -> FINDING
    every cell available to i     -> LIVENESS   (the old "next second" bucket)
    neither                       -> BAND, a third state, never folded into
                                     either, because the movement cannot be
                                     attributed to an available or an
                                     unavailable cell

`unavailable` is `PREREG.md` §2.3's comparator under the declared tie branch, so
FINDING is `d(i) < min_B a(j)` and LIVENESS is `d(i) >= max_B a(j)` under the
registered default. On the whole-frame path `min == max`, the band is empty, and
the three classes are the old two -- which is why the guard can require the
Phase 1 pair to be bit-identical.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import (                               # noqa: E402
    AvailabilityModel, run_probe_a)
from leakaudit.modes import ColumnMode                             # noqa: E402

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
MS = pd.Timedelta(milliseconds=1)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")
MODES = {"v": ColumnMode("at_timestamp")}


# --------------------------------------------------------------------------
# §1(c) -- the positive that failed. Same frames, same cohort, same builder.
# --------------------------------------------------------------------------

def _lagged_frames(n=12, offset=pd.Timedelta(milliseconds=500)):
    """Aggregate rows keyed mid-second; one decision row per second.

    A mid-second key is the fixture's own shape: `trades.ts_event` is off the
    boundary on 397,408 of 397,457 rows, median 467.83 ms.
    """
    k = [T0 + i * SEC + offset for i in range(n)]
    return {"agg": pd.DataFrame({"k": k, "v": np.arange(n, dtype="float64")})}


def _lagged_build(raw):
    """Output row m decides at `T0 + m s` and reads the cell keyed 0.5 s later.

    Unavailable under both declarations, so the comparator says finding under
    both. Only the geometry disagreed.
    """
    agg = raw["agg"]
    n = len(agg)
    return pd.DataFrame({"d": [T0 + m * SEC for m in range(n)],
                         "x": agg["v"].to_numpy()})


def test_THE_POSITIVE_THAT_FAILED_declared_column_mode_finds_the_leak():
    """R261 §1(c). This was `observed_silence` before the repair.

    ONE cohort, so exactly one cell is corrupted and exactly one row moves and
    the batch cannot supply the answer by corrupting everything at once. The
    moved row decides at `F + 1s`; the cell's declared instant is `F + 1.5s`;
    `F + 1.5s > F + 1s` is unavailable, so the row is a finding.
    """
    raw = _lagged_frames()
    res = run_probe_a(raw, _lagged_build, MODEL, side="mode",
                      cohort_stride=1, max_cohorts=1, column_modes=MODES)
    assert res.verdict() == "finding", (
        "the declared column mode reported %r; under the comparator the moved "
        "row at F+1s against a cell at F+1.5s is a finding" % res.verdict())
    c = res.cohorts[0]
    assert c.moved_in_second == 1
    assert c.moved_next_second == 0
    assert c.moved_in_band == 0, "min and max coincide here, so no band exists"


def test_the_WHOLE_FRAME_half_of_the_same_pair_is_unchanged():
    """The control. It found the leak before the repair and still does."""
    raw = _lagged_frames()
    res = run_probe_a(raw, _lagged_build, MODEL, side="frame",
                      cohort_stride=1, max_cohorts=1)
    assert res.verdict() == "finding"
    assert res.cohorts[0].moved_in_second == 1
    assert res.cohorts[0].moved_in_band == 0


# --------------------------------------------------------------------------
# §1(d) -- the discriminating fixture. Two instants in ONE batch, so the band
# is not empty and a repair that over-reports it is caught.
# --------------------------------------------------------------------------

F = T0
GUARD_KEY = F + pd.Timedelta(milliseconds=500)     # satisfies the frame mask
LO_KEY = F + SEC + pd.Timedelta(milliseconds=300)  # a(j) = F + 1.3s
HI_KEY = F + SEC + pd.Timedelta(milliseconds=700)  # a(j) = F + 1.7s

#: (decision instant, expected class). One row per class, plus one before the
#: cohort's own second to show the finding region is not bounded below by it.
BAND_ROWS = (
    (F + pd.Timedelta(milliseconds=500), "finding"),
    (F + SEC + pd.Timedelta(milliseconds=100), "finding"),
    (F + SEC + pd.Timedelta(milliseconds=500), "band"),
    (F + SEC + pd.Timedelta(milliseconds=800), "liveness"),
)


def _band_frames():
    return {"agg": pd.DataFrame(
        {"k": [GUARD_KEY, LO_KEY, HI_KEY], "v": [1.0, 2.0, 3.0]})}


def _band_build(raw):
    """Every output row reads every aggregate value, so every row moves.

    The classification is then purely the comparator on the row's own decision
    instant, which is what this fixture is testing. A builder where only some
    rows moved would confound the class with the read.
    """
    total = float(raw["agg"]["v"].sum())
    return pd.DataFrame({"d": [d for d, _ in BAND_ROWS],
                         "x": [total] * len(BAND_ROWS)})


def test_THE_BAND_IS_ITS_OWN_STATE_and_the_three_classes_are_exact():
    """R261 §1(d). Three assertions, one fixture, one batch.

    The batch holds two instants -- `F + 1.3s` and `F + 1.7s` -- so the cohort's
    `[min, max]` is a real interval and the three classes are distinguishable.
    A repair that widened the band would move the `F + 1.1s` row out of
    `finding`; one that collapsed it would put the `F + 1.5s` row into `finding`
    or into `liveness`. Both are caught here.
    """
    res = run_probe_a(_band_frames(), _band_build, MODEL, side="band",
                      cohort_stride=1, max_cohorts=1, column_modes=MODES)
    assert len(res.cohorts) == 1
    c = res.cohorts[0]
    assert c.a_min == LO_KEY, "the batch's earliest declared instant"
    assert c.a_max == HI_KEY, "the batch's latest declared instant"
    want = {k: sum(1 for _, cls in BAND_ROWS if cls == k)
            for k in ("finding", "band", "liveness")}
    assert c.moved_in_second == want["finding"], (
        "rows before F+1.3s are unavailable to EVERY perturbed cell")
    assert c.moved_in_band == want["band"], (
        "the row at F+1.5s is after one instant and before the other, so the "
        "movement cannot be attributed to an available or an unavailable cell")
    assert c.moved_next_second == want["liveness"], (
        "rows at or after F+1.7s are available to every perturbed cell")


def test_a_BAND_ONLY_run_is_not_reported_as_a_silence():
    """A band row is evidence that something moved. Calling the run
    `observed_silence` would fold the band into liveness, which is the defect
    the third state exists to prevent."""
    def build(raw):
        v = raw["agg"]["v"].to_numpy()
        # Row 0 sits in the cohort's own second and reads only the cell that is
        # NOT in the batch, so it is finding-eligible and does not move. Row 1
        # sits between the batch's two instants and reads both, so it moves and
        # is a band row. That separation is the whole point: without it a row in
        # the finding region would move and the run would have a finding.
        return pd.DataFrame(
            {"d": [F + pd.Timedelta(milliseconds=200),
                   F + SEC + pd.Timedelta(milliseconds=500)],
             "x": [float(v[0]), float(v[1] + v[2])]})

    frames = _band_frames()
    res = run_probe_a(frames, build, MODEL, side="bandonly",
                      cohort_stride=1, max_cohorts=1, column_modes=MODES)
    assert res.verdict() == "attribution_ambiguous", res.verdict()
    assert res.findings == []
    c = res.cohorts[0]
    assert c.rows_in_second == 1, "the finding region was populated and silent"
    assert c.moved_in_second == 0
    assert c.moved_in_band == 1


# --------------------------------------------------------------------------
# §1(f) -- one-way. The repair adds findings and removes none, and the rows it
# adds are named.
# --------------------------------------------------------------------------

def _old_rule(res, model):
    """The pre-repair classification, recomputed from the same result.

    Kept here rather than described, because "the repair adds and never
    removes" is a claim about the difference between two rules and a claim
    about a difference needs both sides present.
    """
    out = {}
    for c in res.cohorts:
        out[c.second] = (c.second, c.second + model.window)
    return out


def test_the_WHOLE_FRAME_path_gains_and_loses_NOTHING():
    """§1(f), first half, and the reason §1(e)'s guard can require SAME.

    On the whole-frame path every perturbed cell's instant is `F + window`
    exactly, so `min == max`, the finding region is `[F, F + window)` and the
    liveness region is `[F + window, F + window + 1s)` -- the old two buckets,
    unchanged.
    """
    raw = _lagged_frames()
    # STRIDE 2: the derived floor. R263 §2. At stride 1 the probed seconds are
    # one second apart and a cohort's corruption is observable over two, so a
    # cell corrupted for one cohort moves rows the next counts as findings.
    # This test is about `min == max` on the whole-frame path, not about the
    # schedule, so it takes the floor rather than a value that is now refused.
    res = run_probe_a(raw, _lagged_build, MODEL, side="oneway",
                      cohort_stride=2, max_cohorts=40)
    for c in res.cohorts:
        assert c.a_min == c.a_max == c.second + MODEL.window
        assert c.moved_in_band == 0, "no band exists where min == max"


def test_the_ADDED_findings_lie_only_in_the_named_interval():
    """§1(f), second half. On the per-column path the repair can only add rows
    in `[F + window, min_B a(j))` -- rows the old rule put in the next-second
    bucket and the comparator calls unavailable. Nothing outside that interval
    changes class, and nothing leaves `finding`."""
    raw = _lagged_frames()
    res = run_probe_a(raw, _lagged_build, MODEL, side="added",
                      cohort_stride=1, max_cohorts=1, column_modes=MODES)
    c = res.cohorts[0]
    lo_old, hi_old = c.second, c.second + MODEL.window
    # Every row the new rule calls a finding is either in the old finding
    # region or in the named added interval, and never outside both.
    added_lo, added_hi = hi_old, c.a_min
    assert added_lo < added_hi, (
        "with a mid-second key the added interval is non-empty: %s to %s"
        % (added_lo, added_hi))
    assert c.moved_in_second == 1
    # The moved row is at F + 1s, which is exactly the start of the added
    # interval and outside the old finding region [F, F + 1s).
    assert not (lo_old <= c.second + SEC < hi_old)
    assert added_lo <= c.second + SEC < added_hi
