"""Block reach: the window, measured, and it governs every stride. R271 §2.

The single-second reach corrupts one second and asks how far the output moves.
A feature that takes a median, a threshold or a rank answers "as far as one
second's worth of corruption can push it", which can be nothing at all. A
batched pass puts several corruptions inside the window, and the window is what
interferes. So the block reach corrupts every modelled cell at or before a
sampled second, rebuilds once, and reads how far forward the output moved.

THE PAIR. HELD: frames, model, seed. VARIED: one corrupted second against a
corrupted history. On a rolling MEDIAN of constant values one perturbed cell
never moves the median and the history does, for about half the window.

ALSO HERE, because it was found establishing this: the single-second reach
never aligned its keys to the decision clock, so a timezone-aware key frame was
never corrupted at all.
"""
from __future__ import annotations

import io
import sys
import types
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                      # noqa: E402
from leakaudit.availability import (                           # noqa: E402
    DEFAULT_STRIDE, AvailabilityModel, ProbeError, run_probe_a)
from leakaudit.reach import (                                  # noqa: E402
    BLOCK_SAMPLES, ReachError, _corrupt_one, measure_block_reach,
    measure_reach)

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def _frames(n):
    return {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(n)],
                                 "v": np.ones(n, dtype="float64")})}


def _median(W):
    """Reads the PREVIOUS W cells' median: available, and a median of constants."""
    def build(raw):
        agg = raw["agg"]
        x = agg["v"].shift(1).rolling(W, min_periods=1).median()
        return pd.DataFrame({"d": pd.to_datetime(agg["k"]).to_numpy(),
                             "x": x.to_numpy()})
    return build


def _cumsum(raw):
    """Every later row reads every earlier cell: the history never ends."""
    agg = raw["agg"]
    return pd.DataFrame({"d": pd.to_datetime(agg["k"]).to_numpy(),
                         "x": agg["v"].shift(1).cumsum().to_numpy()})


# --------------------------------------------------------------------------
# the pair
# --------------------------------------------------------------------------

def test_THE_PAIR_one_second_moves_NOTHING_and_the_block_moves_HALF_THE_WINDOW():
    frames = _frames(60)
    build = _median(10)
    base = build(frames)
    single = measure_reach(frames, build, MODEL, base, "d", k=3)
    assert single.measured is None, (
        "one perturbed cell among ten constants cannot move a median: %s"
        % single.note())
    block = measure_block_reach(frames, build, MODEL, base, "d")
    assert block.k == BLOCK_SAMPLES == 1
    # Row F+m reads cells F+m-10 .. F+m-1, of which 11-m are corrupted; the
    # median of ten moves while at least five are, so up to m = 6.
    assert block.measured == 6 * SEC, block.spread()
    assert "BLOCK REACH" in block.note() and "1 sampled block position" in block.note()


def test_the_block_note_carries_its_RESIDUAL_and_says_k():
    frames = _frames(60)
    build = _median(10)
    block = measure_block_reach(frames, build, MODEL, build(frames), "d", k=3)
    note = block.note()
    assert "below resolution" in note, note
    assert "none of 3 sampled block position" in note, note


# --------------------------------------------------------------------------
# the floor, on every run
# --------------------------------------------------------------------------

def test_the_DEFAULT_stride_stays_where_it_CLEARS_the_block_floor():
    """The floor rises -- 7 s over the model's 2 s -- and the run says so; the
    shipped default of 97 still clears it, so it is still the stride."""
    res = run_probe_a(_frames(600), _median(10), MODEL, side="t", max_cohorts=0)
    assert res.block_reach is not None and res.block_reach.measured == 6 * SEC
    assert res.resolved_stride == DEFAULT_STRIDE
    floor = [n for n in res.notes if "STRIDE FLOOR FROM THE BLOCK REACH" in n]
    assert floor and "7s" in floor[0], res.notes
    assert not any("does NOT clear" in n for n in res.notes), res.notes


def test_a_default_run_BELOW_the_block_floor_uses_the_floor_and_SAYS_SO():
    """A stranger's long window at stride 97 is the same defect."""
    res = run_probe_a(_frames(1200), _median(400), MODEL, side="t", max_cohorts=0)
    m = res.block_reach.measured
    assert m is not None and m > DEFAULT_STRIDE * SEC, res.block_reach.spread()
    assert res.resolved_stride * SEC >= m + SEC
    assert any("STRIDE FLOOR FROM THE BLOCK REACH" in n for n in res.notes), res.notes
    assert any("does NOT clear" in n for n in res.notes), res.notes


def test_a_DECLARED_stride_below_the_block_floor_is_REFUSED():
    with pytest.raises(ReachError) as e:
        run_probe_a(_frames(1200), _median(400), MODEL, side="t",
                    cohort_stride=DEFAULT_STRIDE, max_cohorts=10)
    msg = str(e.value)
    assert "BLOCK REACH" in msg and "97" in msg, msg
    assert issubclass(ReachError, ProbeError)


def test_block_samples_ZERO_is_a_declaration_and_the_run_says_so():
    res = run_probe_a(_frames(60), _median(10), MODEL, side="t", max_cohorts=0,
                      block_samples=0)
    assert res.block_reach is None
    assert any("BLOCK REACH NOT MEASURED" in n for n in res.notes)


# --------------------------------------------------------------------------
# the fallback bound
# --------------------------------------------------------------------------

def test_a_block_that_BREAKS_the_build_falls_back_and_STATES_the_bound():
    frames = _frames(60)
    inner = _median(10)

    def fragile(raw):
        if int((raw["agg"]["v"] > 1.0e5).sum()) > 12:
            raise ValueError("too many huge values")
        return inner(raw)

    base = fragile(frames)
    block = measure_block_reach(frames, fragile, MODEL, base, "d",
                                fallback_seconds=10)
    s = block.samples[0]
    assert s.bound == 10 * SEC
    assert "ValueError" in s.note
    assert "cannot show" in block.note() and "10" in block.note(), block.note()
    assert block.measured is not None


# --------------------------------------------------------------------------
# the clock
# --------------------------------------------------------------------------

def _aware_frames(n):
    return {"agg": pd.DataFrame({
        "k": pd.to_datetime([T0 + i * SEC for i in range(n)]).tz_localize("UTC"),
        "v": np.arange(n, dtype="float64")})}


def _aware_build(raw):
    agg = raw["agg"]
    k = pd.to_datetime(agg["k"]).dt.tz_convert("UTC").dt.tz_localize(None)
    return pd.DataFrame({"d": k.to_numpy(),
                         "x": agg["v"].shift(1).rolling(5, min_periods=1).sum().to_numpy()})


def test_the_single_second_reach_CORRUPTS_an_aware_key_frame():
    frames = _aware_frames(60)
    base = _aware_build(frames)
    d = pd.to_datetime(base["d"])
    second = T0 + 30 * SEC
    # The comparison the reach control used to make, pinned as the fact that
    # made it silent: an aware key against a naive second selects nothing.
    unaligned = pd.to_datetime(frames["agg"]["k"]).dt.floor("s") == second
    assert int(unaligned.sum()) == 0
    _out, cells = _corrupt_one(frames, MODEL, second, 1, d)
    assert cells == 1, cells
    rr = measure_reach(frames, _aware_build, MODEL, base, "d", k=3)
    assert rr.measured == 5 * SEC, rr.note()


# --------------------------------------------------------------------------
# --complete
# --------------------------------------------------------------------------

def _config():
    return types.SimpleNamespace(column_modes=None, bar_duration=None)


def test_COMPLETE_takes_its_stride_from_the_BLOCK_reach():
    buf = io.StringIO()
    with redirect_stdout(buf):
        res, note = cli._probe_complete(_frames(300), _median(10), MODEL,
                                        _config(), None, None, None)
    out = buf.getvalue()
    assert "BLOCK REACH SPREAD over 10 sample(s)" in out, out
    assert "7 pass(es) at stride 7" in out, out
    assert "block reach" in note.lower(), note
    # At stride 7 no ten-row window holds more than two corrupted cells, so no
    # median moves anywhere: the honest verdict is `none`, and what matters
    # here is that the passes invented no finding.
    assert not res.findings, [c.second for c in res.findings]


def test_COMPLETE_REFUSES_when_the_block_reach_runs_to_the_frame_end():
    buf = io.StringIO()
    with redirect_stdout(buf), pytest.raises(ProbeError) as e:
        cli._probe_complete(_frames(120), _cumsum, MODEL, _config(),
                            None, None, None)
    msg = str(e.value)
    assert "COMPLETE RUN REFUSED" in msg, msg
    assert "unbatched" in msg.lower(), msg
    assert "120 rebuilds" in msg, msg
