"""Probe A itself, on synthetic frames. R192 §1.

WHY SYNTHETIC. A probe whose only positive is the fixture's own contamination is
a probe testing itself. These frames are built here, so the leaky and clean
builders differ in exactly one respect -- WHEN they read the aggregate -- and a
firing is attributable to that and to nothing else. The construction is the one
`b6_probe_a_controls.py` established; it is exercised by pytest here so it runs
in the default suite rather than only when someone remembers the script.

  POSITIVE  a builder that reads its OWN second's aggregate. The aggregate over
            [F, F+1s) completes at F+1s and the decision instant lies inside F,
            so the cell is unavailable and the probe fires IN-SECOND.
  NEGATIVE  a builder that reads the PREVIOUS second's aggregate. Its instant is
            F and the decision instant is at or after F, so it is available and
            the probe is silent in-second -- while STILL moving the following
            second's rows, which is what proves the corruption landed at all.
            A negative that moves nothing anywhere is a probe testing itself.
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

from leakaudit.availability import (                      # noqa: E402
    AvailabilityModel, ProbeError, run_probe_a)

N_SECONDS, ROWS_PER_SECOND, SEED = 400, 3, 20260828
MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def _frames():
    rng = np.random.default_rng(SEED)
    secs = pd.date_range(pd.Timestamp("2026-01-01 00:00:00"),
                         periods=N_SECONDS, freq="1s")
    agg = pd.DataFrame({"ts_floor": secs,
                        "agg_value": rng.standard_normal(N_SECONDS)})
    stamps = [s + pd.Timedelta(milliseconds=200 + 250 * k)
              for s in secs for k in range(ROWS_PER_SECOND)]
    snap = pd.DataFrame({"timestamp": stamps,
                         "own": rng.standard_normal(len(stamps))})
    return {"snap": snap, "agg": agg}


def _merge(raw, shift_seconds):
    out = raw["snap"].copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    key = out["ts_floor"] - pd.Timedelta(seconds=shift_seconds)
    m = raw["agg"].set_index("ts_floor")["agg_value"]
    out["feature"] = key.map(m).to_numpy()
    return out[["timestamp", "own", "feature"]]


def build_leaky(raw):
    return _merge(raw, 0)


def build_clean(raw):
    return _merge(raw, 1)


def _run(build, stride=7):
    return run_probe_a(_frames(), build, MODEL, side="synthetic",
                       cohort_stride=stride, max_cohorts=40, seed=SEED)


def test_the_known_positive_fires_in_second():
    res = _run(build_leaky)
    assert res.determinism_ok
    assert res.verdict() == "finding"
    assert res.findings, "the leaky builder reads an unavailable cell and the probe said nothing"


def test_the_known_negative_is_silent_in_second():
    res = _run(build_clean)
    assert res.verdict() == "observed_silence"
    assert all(c.moved_in_second == 0 for c in res.cohorts)


def test_the_negative_still_moves_the_following_second():
    """The requirement that makes the negative worth anything: silence in-second
    proves nothing unless the corruption reached the build at all."""
    res = _run(build_clean)
    assert sum(c.moved_next_second for c in res.cohorts) > 0, (
        "the corruption never reached the output; this negative tests nothing")


def test_the_finding_names_the_column_that_moved():
    res = _run(build_leaky)
    for c in res.findings:
        assert "feature" in c.features_in_second
        assert "own" not in c.features_in_second


# ---------------------------------------------------------------------------
# base_columns -- R192 §1
# ---------------------------------------------------------------------------

def test_base_columns_are_the_compared_frame_s_own_columns():
    """A caller was rebuilding the frame to learn its columns, which costs a
    build and takes the column set from a different build than the findings came
    from. The probe carries them out now."""
    res = _run(build_leaky)
    assert res.base_columns == ("timestamp", "own", "feature")


def test_base_columns_are_set_even_when_the_probe_is_silent():
    assert _run(build_clean).base_columns == ("timestamp", "own", "feature")


def test_base_columns_are_set_before_the_determinism_guard_can_fail():
    """A non-deterministic builder returns early. The column set is still a fact
    about the baseline, and a caller reading it should not get an empty tuple
    that looks like a build with no columns."""
    state = {"n": 0}

    def wobbly(raw):
        state["n"] += 1
        out = _merge(raw, 0)
        out["own"] = out["own"] + state["n"]
        return out

    res = run_probe_a(_frames(), wobbly, MODEL, side="synthetic",
                      cohort_stride=7, max_cohorts=40, seed=SEED)
    assert res.determinism_ok is False
    assert res.base_columns == ("timestamp", "own", "feature")


def test_a_frame_that_matches_no_corrupted_second_raises():
    """A frame that is never corrupted reports a silence about the harness, not
    about the pipeline, so the probe refuses rather than returning silence."""
    raw = _frames()
    raw["agg"] = raw["agg"].assign(
        ts_floor=raw["agg"]["ts_floor"] + pd.Timedelta(days=3650))
    try:
        run_probe_a(raw, build_leaky, MODEL, side="synthetic",
                    cohort_stride=7, max_cohorts=40, seed=SEED)
    except ProbeError as exc:
        assert "matched NO corrupted second" in str(exc)
    else:
        raise AssertionError("a never-corrupted frame returned silence")
