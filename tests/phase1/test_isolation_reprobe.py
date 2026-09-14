"""The isolation re-probe: one cohort's cells, one rebuild, the shared rule. R270 §1(a).

A batched finding and an interference finding differ in exactly one way: the
real one survives being probed ALONE. With no other cohort in the batch no cell
corrupted for a neighbour can move a row, so interference is impossible by
construction and whatever still classifies as a finding is the cohort's own.

THE PAIR. HELD: the frames, the model, the seed, and the builder within each
half. VARIED: batched against isolated, and nothing else.

  * NEGATIVE -- a builder that reads the cell THREE seconds back. That cell is
    available to the reading row, so there is nothing to find. At stride 3
    with the reach control declared off, a neighbour's corrupted cell lands in
    the next cohort's finding region and the batch reports findings that are
    false by construction. Isolated, none of them is a finding.
  * POSITIVE -- a builder that reads its OWN second's cell, unavailable at the
    decision instant. Batched it finds; isolated, every finding persists.

The reach control is declared off (`reach_samples=0`) on the batched negative
because a measured reach of 3 s would refuse stride 3 -- which is the refusal
working. Switching it off stands in for a reach that is a lower bound and
missed the path, which is the reading the instrument exists to test.
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

from leakaudit.availability import (                               # noqa: E402
    AvailabilityModel, ProbeError, isolate_cohorts, run_probe_a)

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
N = 60
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def _frames():
    return {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(N)],
                                 "v": np.arange(N, dtype="float64") + 1.0})}


def _lag3(raw):
    """Reads the cell three seconds back: available, so nothing to find."""
    agg = raw["agg"]
    v = agg["v"].to_numpy()
    return pd.DataFrame({"d": agg["k"].to_numpy(),
                         "x": np.concatenate(([np.nan] * 3, v[:-3]))})


def _own(raw):
    """Reads its own second's cell, available only at the second's end: a leak."""
    agg = raw["agg"]
    return pd.DataFrame({"d": agg["k"].to_numpy(), "x": agg["v"].to_numpy()})


def _batched(build):
    # BOTH controls declared off. Since R271 the block reach measures this
    # builder's three-second lookback and refuses stride 3 -- the repair working
    # on the very construction this pair was built from, pinned below -- so the
    # batched half stands in for a run whose reach and block reach both missed
    # the path.
    return run_probe_a(_frames(), build, MODEL, side="batch", cohort_stride=3,
                       max_cohorts=10 ** 6, reach_samples=0, block_samples=0)


def test_with_the_BLOCK_REACH_on_the_same_batch_is_REFUSED():
    """R271 §2(c). The interference this pair manufactures is exactly what the
    block reach exists to refuse: 3 s of lookback, stride 3, floor 4 s."""
    with pytest.raises(ProbeError) as e:
        run_probe_a(_frames(), _lag3, MODEL, side="batch", cohort_stride=3,
                    max_cohorts=10 ** 6, reach_samples=0)
    assert "BLOCK REACH" in str(e.value), str(e.value)


def _shared_reach(build):
    return run_probe_a(_frames(), build, MODEL, side="reach",
                       max_cohorts=0).reach


# --------------------------------------------------------------------------
# the pair
# --------------------------------------------------------------------------

def test_NEGATIVE_batched_interference_findings_VANISH_when_isolated():
    batch = _batched(_lag3)
    false = [c.second for c in batch.findings]
    assert batch.verdict() == "finding" and len(false) >= 5, (
        "the batched half must show the interference, or the pair shows "
        "nothing: %s" % batch.verdict())

    iso = isolate_cohorts(_frames(), _lag3, MODEL, false,
                          reach=_shared_reach(_lag3))
    assert [r.second for r in iso] == sorted(false)
    assert not any(r.persisted for r in iso), (
        "a finding on a builder that reads only available cells survived "
        "isolation: %s" % [(r.second, r.verdict) for r in iso if r.persisted])
    assert all(r.batched_features == () for r in iso), (
        "no batched features were handed in, so none may be reported")


def test_POSITIVE_real_findings_PERSIST_when_isolated():
    batch = run_probe_a(_frames(), _own, MODEL, side="batch", cohort_stride=3,
                        max_cohorts=10 ** 6, reach_samples=0)
    real = [c.second for c in batch.findings]
    assert batch.verdict() == "finding" and len(real) >= 5

    iso = isolate_cohorts(_frames(), _own, MODEL, real,
                          reach=_shared_reach(_own))
    assert len(iso) == len(real)
    assert all(r.persisted for r in iso), (
        "a real leak vanished under isolation, so the instrument is wrong: %s"
        % [(r.second, r.verdict) for r in iso if not r.persisted])
    assert all(r.verdict == "finding" for r in iso)
    assert all(r.features == ("x",) for r in iso)


# --------------------------------------------------------------------------
# the instrument's own properties
# --------------------------------------------------------------------------

def test_ONE_rebuild_per_cohort_after_ONE_determinism_pair():
    calls = []

    def counting(raw):
        calls.append(1)
        return _own(raw)

    reach = _shared_reach(_own)
    secs = [T0 + 10 * SEC, T0 + 20 * SEC, T0 + 30 * SEC, T0 + 40 * SEC]
    isolate_cohorts(_frames(), counting, MODEL, secs, reach=reach)
    assert len(calls) == 2 + len(secs), (
        "two clean builds for determinism, then one rebuild per cohort; got %d"
        % len(calls))


def test_each_isolation_corrupts_ONLY_its_own_cohort():
    reach = _shared_reach(_own)
    secs = [T0 + 10 * SEC, T0 + 25 * SEC]
    for r in isolate_cohorts(_frames(), _own, MODEL, secs, reach=reach):
        assert r.result.n_cohorts == 1
        assert [c.second for c in r.result.cohorts] == [r.second]
        assert r.result.min_separation is None, "one cohort has no neighbour"


def test_a_second_that_is_NOT_a_decision_second_is_REFUSED():
    with pytest.raises(ProbeError) as e:
        isolate_cohorts(_frames(), _own, MODEL, [T0 - 5 * SEC],
                        reach=_shared_reach(_own))
    assert "not decision seconds" in str(e.value)


def test_a_nondeterministic_builder_isolates_NOTHING():
    state = {"n": 0}

    def drifting(raw):
        state["n"] += 1
        out = _own(raw)
        out["x"] = out["x"] + state["n"]
        return out

    with pytest.raises(ProbeError) as e:
        isolate_cohorts(_frames(), drifting, MODEL, [T0 + 10 * SEC],
                        reach=None)
    assert "not deterministic" in str(e.value)


def test_a_frame_with_NO_cell_in_the_isolated_second_is_NOTED_not_refused():
    """A batch of many seconds matches every frame somewhere; one second need
    not. The per-frame refusal exists to catch a timezone or resolution
    mismatch, which the batch that produced the finding has already ruled out,
    so under isolation a frame silent in that one second is stated instead."""
    frames = _frames()
    frames["other"] = pd.DataFrame({"k2": [T0 + 50 * SEC], "w": [1.0]})
    model = AvailabilityModel(aggregate_frames={"agg": "k", "other": "k2"},
                              decision_column="d")
    r = isolate_cohorts(frames, _own, model, [T0 + 10 * SEC], reach=None)[0]
    assert r.persisted
    assert any("has no cell in the isolated second" in n for n in r.result.notes)


def test_reach_measured_AT_named_seconds_sees_the_builder_there():
    """R270 §1(c). If isolated findings vanish, the reading is interference and
    the reach at those cohorts has to exceed what the spread samples saw. So
    the reach is measurable at named seconds, and k is their count."""
    from leakaudit.reach import measure_reach
    frames = _frames()
    base = _lag3(frames)
    at = [T0 + 10 * SEC, T0 + 30 * SEC]
    rr = measure_reach(frames, _lag3, MODEL, base, "d", at_seconds=at)
    assert rr.k == 2
    assert [s.second for s in rr.samples] == at
    assert rr.measured == 3 * SEC
    assert "REACH SPREAD over 2 sample(s)" in rr.spread()


def test_the_batched_features_are_CARRIED_beside_the_isolated_ones():
    batch = run_probe_a(_frames(), _own, MODEL, side="batch", cohort_stride=3,
                        max_cohorts=10 ** 6, reach_samples=0)
    f = batch.findings[0]
    r = isolate_cohorts(_frames(), _own, MODEL, [f.second], reach=None,
                        batched={f.second: f})[0]
    assert r.batched_features == f.features_in_second
    assert r.batched_moved == f.moved_in_second
