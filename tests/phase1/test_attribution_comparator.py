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

import pytest                                                      # noqa: E402

from leakaudit.availability import (                               # noqa: E402
    AvailabilityModel, ProbeError, run_probe_a, stride_floor)
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


# --------------------------------------------------------------------------
# R264 §2(d) -- the derived stride's discriminating positive. Three states, one
# fixture, and the ground truth is that there is NOTHING TO FIND.
# --------------------------------------------------------------------------

def _clean_frames(n=40):
    return {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(n)],
                                 "v": np.arange(n, dtype="float64")})}


def _clean_build(raw):
    """Reads the PREVIOUS second's cell, whose declared instant is at or before
    the reading row's decision instant. AVAILABLE, so not a leak. Any finding
    on this fixture is false by construction."""
    agg = raw["agg"]
    v = agg["v"].to_numpy()
    return pd.DataFrame({"d": agg["k"].to_numpy(),
                         "x": np.concatenate(([np.nan], v[:-1]))})


def test_STRIDE_BELOW_THE_FLOOR_is_refused_and_the_floor_is_named():
    """State one of three. Measured at R263 BEFORE the floor existed: this same
    fixture at stride 1 reported **39 false findings across 40 cohorts** and a
    verdict of `finding`, on a builder that leaks nothing. That number cannot
    be reproduced now because the run refuses, which is the repair; it is
    recorded here so the positive stays readable after it stops reproducing."""
    with pytest.raises(ProbeError) as e:
        run_probe_a(_clean_frames(), _clean_build, MODEL, side="s1",
                    cohort_stride=1, max_cohorts=40)
    msg = str(e.value)
    assert "BELOW THE DERIVED FLOOR" in msg
    assert "1s apart" in msg and "2s" in msg, (
        "the refusal must name BOTH numbers -- what was probed and what is "
        "required -- or a caller cannot act on it: %s" % msg)


def test_STRIDE_AT_THE_FLOOR_runs_and_finds_NOTHING_which_is_correct():
    """State two. The same fixture, one stride up, with no interference: the
    pipeline has no leak and the probe says so."""
    res = run_probe_a(_clean_frames(), _clean_build, MODEL, side="s2",
                      cohort_stride=2, max_cohorts=40)
    assert sum(c.moved_in_second for c in res.cohorts) == 0, (
        "a finding here would be false: every cell this builder reads is "
        "available to the row that reads it")
    assert res.verdict() == "observed_silence"
    assert res.liveness > 0, "and the silence is licensed -- rows did move"


def test_an_UNDECLARED_stride_takes_the_default_and_says_which():
    """State three, corrected at R265 §2.

    R264 wrote this asserting that an undeclared stride resolves to the FLOOR.
    That confused a bound with a value: 97 is a sampling default and clears the
    floor at every registered window, so resolving to the floor made a
    stranger's run about fifty times more expensive for no correctness. What
    the run must do is say WHICH of the two it used.
    """
    res = run_probe_a(_clean_frames(), _clean_build, MODEL, side="derived",
                      max_cohorts=40)
    note = "\n".join(res.notes)
    assert "NOT DECLARED" in note, note
    assert "default 97" in note, note
    assert sum(c.moved_in_second for c in res.cohorts) == 0


def test_an_UNDECLARED_stride_takes_the_SHIPPED_DEFAULT_where_it_clears():
    """R265 §2. The floor is a BOUND, not a value.

    R263 resolved an undeclared stride to the floor, which made a stranger's
    default run about fifty times more expensive and bought no correctness: 97
    already cleared the floor at every registered window. The default is
    restored and the floor is applied to it, which is what a bound is for.
    """
    res = run_probe_a(_clean_frames(n=300), _clean_build, MODEL,
                      side="default", max_cohorts=40)
    note = "\n".join(res.notes)
    assert "default 97" in note, note
    assert "correctness bound and not a schedule" in note, note
    # 300 seconds at stride 97 is four cohorts; at the floor it would be 150.
    assert res.n_cohorts == 4, (
        "an undeclared stride must sample at the default, not at the floor: "
        "got %d cohorts" % res.n_cohorts)


def test_where_the_DEFAULT_is_BELOW_the_floor_the_floor_is_used_and_says_so():
    """The other half. A declared window large relative to the decision seconds
    puts the floor above 97, and then the bound wins over the default."""
    model = AvailabilityModel(aggregate_frames={"agg": "k"},
                              decision_column="d",
                              window=pd.Timedelta(seconds=200))
    res = run_probe_a(_clean_frames(n=900), _clean_build, model,
                      side="bigwindow", max_cohorts=10)
    note = "\n".join(res.notes)
    assert "does NOT clear the derived floor" in note, note
    assert "default 97 was below it" in note or "(default 97" in note, note


# --------------------------------------------------------------------------
# R265 §3(b) -- the floor's own positive, on the case that would break a floor
# one second too small.
# --------------------------------------------------------------------------

def test_THE_FLOOR_HOLDS_on_the_PER_COLUMN_WORST_CASE_at_exactly_the_floor():
    """R265 §3(b). The plausible wrong floor is one that omits the second the
    per-column selection throws away.

    Selection there is `floor(a - window)`, so a cell's declared instant lands
    anywhere in `[F + window, F + window + 1s)`. The worst case is the top of
    that interval, and this fixture sits at `F + window + 0.99s`. The pipeline
    is CLEAN -- every row reads a cell already available to it -- so a finding
    here is false, and the floor is probed at EXACTLY its own value.

    IF THIS FAILS THE FORMULA IS WRONG, and the floor is not to be widened by
    hand to make it pass; that would be fitting the bound to the fixture.
    """
    n = 60
    off = pd.Timedelta(milliseconds=990)
    frames = {"agg": pd.DataFrame({"k": [T0 + i * SEC + off for i in range(n)],
                                   "v": np.arange(n, dtype="float64")})}

    def build(raw):
        agg = raw["agg"]
        v = agg["v"].to_numpy()
        # Row m decides at T0 + m s and reads cell m-1, whose declared instant
        # under the column mode is T0 + (m-1) s + 0.99 s -- BEFORE the decision,
        # so available, so legitimate.
        return pd.DataFrame({"d": [T0 + m * SEC for m in range(n)],
                             "x": np.concatenate(([np.nan], v[:-1]))})

    modes = {"v": ColumnMode("at_timestamp")}
    floor = stride_floor(MODEL, modes)
    assert floor == pd.Timedelta(seconds=3), (
        "the per-column floor is `window + 2s`; if this moved, the test below "
        "is no longer probing the floor: %s" % floor)
    res = run_probe_a(frames, build, MODEL, side="worst",
                      cohort_stride=3, max_cohorts=40, column_modes=modes)
    a_span = {(c.a_max - c.second) for c in res.cohorts if c.a_max is not None}
    assert a_span, "no cohort carried a batch; the fixture probed nothing"
    assert max(a_span) >= pd.Timedelta(seconds=1, milliseconds=980), (
        "the fixture is not at the per-column worst case: widest instant sits "
        "%s past its cohort" % max(a_span))
    assert sum(c.moved_in_second for c in res.cohorts) == 0, (
        "a finding on a clean pipeline at exactly the floor means the floor's "
        "formula is too small. Do not widen it here -- that is the finding.")


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
