"""A non-boundary aggregate key is floored AND SAID SO. R207 Q1.

THE HALT THIS TESTS IS "flooring a non-boundary key without reporting it", so
the positive is not "the note exists". A note that fires on every frame reports
nothing: it would be a banner, not a finding, and a reader would learn to skip
it. What has to be shown is that the note DISCRIMINATES -- silent where the key
is already a wall-clock second, present where it is not, on frames that are
otherwise identical.

The second half matters as much. Flooring is the DECLARED rule for an aggregate
frame (`AVAILABILITY_DECLARATION.md` §3, §C.1: the join family's availability
instant is `floor(T) + 1s`), so applying it is not inference and refusing the
configuration would reject a correct one. What was wrong was that it happened
invisibly -- which is how the model's own docstring came to state `key + window`
and stay wrong for two rounds while the code computed something else
(D-V30A-43). So the arithmetic is unchanged and the silence is what is fixed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402

N = 300
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"},
                          decision_column="timestamp")


def _frames(offsets_ms):
    """One aggregate frame whose key carries `offsets_ms` inside each second.

    `offsets_ms` of zero gives a key that IS a wall-clock second. Anything else
    gives a raw-event-stamp key of the kind `trades.ts_event` is.
    """
    secs = pd.date_range("2026-03-02 13:00:00", periods=N, freq="1s")
    off = pd.to_timedelta(offsets_ms, unit="ms")
    rng = np.random.default_rng(41)
    agg = pd.DataFrame({"k": secs + off, "v": rng.standard_normal(N)})
    snap = pd.DataFrame({
        "timestamp": [s + pd.Timedelta(milliseconds=250) for s in secs]})
    return {"snap": snap, "agg": agg}


def _build(raw):
    out = raw["snap"].copy()
    out["sec"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    a = raw["agg"].copy()
    a["sec"] = pd.to_datetime(a["k"]).dt.floor("s")
    out["v"] = out["sec"].map(a.set_index("sec")["v"]).to_numpy()
    return out[["timestamp", "v"]]


def _run(offsets_ms):
    raw = _frames(offsets_ms)
    return run_probe_a(raw, _build, MODEL, side="test",
                       cohort_stride=7, max_cohorts=30, seed=5)


def _floor_notes(res):
    return [n for n in res.notes if "flooring to" in n]


# ---------------------------------------------------------------------------
# The discrimination: same frame, same builder, keys differing only in offset.
# ---------------------------------------------------------------------------

def test_a_key_ALREADY_on_second_boundaries_says_NOTHING():
    res = _run(np.zeros(N))
    assert _floor_notes(res) == [], (
        "the note fired on a key that needs no flooring, so it is a banner "
        "rather than a report and a reader would learn to skip it: %r"
        % (res.notes,))


def test_a_key_OFF_the_boundary_is_floored_AND_REPORTED():
    res = _run(np.full(N, 400))
    notes = _floor_notes(res)
    assert len(notes) == 1, (
        "flooring happened and was not reported -- the exact halt this "
        "guards: %r" % (res.notes,))
    n = notes[0]
    assert "'k'" in n and "'agg'" in n, "the note must name the key and frame: %r" % n
    assert "floor(k) + 1s" in n, (
        "the note must state the arithmetic applied, readably -- `1s`, not "
        "pandas' `0 days 00:00:01`, because the reader of this line is deciding "
        "whether their configuration is right: %r" % n)
    assert "0.0000%" in n, "0 of 300 keys are on a boundary here: %r" % n


def test_the_two_cases_are_DIFFERENT_which_is_what_makes_it_a_report():
    assert _floor_notes(_run(np.zeros(N))) != _floor_notes(_run(np.full(N, 400)))


# ---------------------------------------------------------------------------
# The fraction is measured, not a flag. A key that is MOSTLY floored is a
# different situation from one that is never floored, and the difference is the
# only thing that tells a reader whether to care.
# ---------------------------------------------------------------------------

def test_the_reported_fraction_is_the_measured_one_not_a_flag():
    off = np.zeros(N)
    off[:N // 4] = 0          # a quarter on the boundary
    off[N // 4:] = 750
    res = _run(off)
    notes = _floor_notes(res)
    assert len(notes) == 1, res.notes
    pct = float(re.search(r"\(([0-9.]+)% ", notes[0]).group(1))
    assert abs(pct - 25.0) < 1e-6, (
        "reported %.4f%% where 75 of 300 keys are on a boundary" % pct)


def test_one_key_off_the_boundary_is_enough_to_report():
    """A frame that is 99.67%% clean still floors, so it still says so."""
    off = np.zeros(N)
    off[0] = 1
    notes = _floor_notes(_run(off))
    assert len(notes) == 1, "a single unfloored key was floored in silence"
    assert "99.6667%" in notes[0], notes[0]


# ---------------------------------------------------------------------------
# The arithmetic did NOT change. This is the guard against "fixing" the probe to
# match the docstring, which R207 rules out: the running rule is the declared
# rule.
# ---------------------------------------------------------------------------

def test_reporting_the_floor_did_not_move_the_probe():
    off = np.full(N, 400)
    a, b = _run(off), _run(np.zeros(N))
    assert [c.second for c in a.cohorts] == [c.second for c in b.cohorts], (
        "the selected seconds differ between a floored and an unfloored key, "
        "which would mean the report changed the arithmetic it describes")
    assert a.verdict() == b.verdict()
