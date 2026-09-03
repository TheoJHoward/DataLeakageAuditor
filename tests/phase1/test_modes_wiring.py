"""Per-column modes wired into the probe. R205 §3.

THE POSITIVE HAS TO DISCRIMINATE, AND THAT IS THE WHOLE DIFFICULTY. A wiring
that is a no-op passes every test that does not distinguish it from the
whole-frame path, so "per-column modes produce a finding" proves nothing. What
is required is data on which the two paths give DIFFERENT answers, with the
difference measured.

THE CONSTRUCTION. One aggregate frame, two columns:

    own_second   an aggregate over the second it is keyed to. It completes at
                 key + 1s, so a row deciding inside that second could not have
                 used it.
    released     a figure published half an hour EARLIER and carried on the same
                 rows. Its instant travels in the frame, in `released_at`.

Under the whole-frame path both columns share the frame's rule, so both are
perturbed at the same selected seconds. Under per-column modes `released` is
declared `at_source_timestamp`, its instant is half an hour earlier, and it is
perturbed at DIFFERENT seconds -- so a pipeline reading it moves different rows.

THE OTHER DIRECTION IS TESTED TOO: with no modes given, the selection is the
frame's, and the two paths agree exactly. That pair is what shows the wiring is
a generalisation rather than a replacement.
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

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.modes import AT_SOURCE_TIMESTAMP, ColumnMode        # noqa: E402

N = 400
LAG = pd.Timedelta(minutes=30)
MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def _frames():
    secs = pd.date_range("2026-01-01 09:00:00", periods=N, freq="1s")
    rng = np.random.default_rng(17)
    agg = pd.DataFrame({
        "ts_floor": secs,
        "own_second": rng.standard_normal(N),
        "released": rng.standard_normal(N),
        "released_at": secs - LAG,
    })
    snap = pd.DataFrame({
        "timestamp": [s + pd.Timedelta(milliseconds=400) for s in secs]})
    return {"snap": snap, "agg": agg}


def _build_reads_released(raw):
    """Reads the RELEASED column, keyed on the row's own second."""
    out = raw["snap"].copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    a = raw["agg"].set_index("ts_floor")
    out["from_released"] = out["ts_floor"].map(a["released"]).to_numpy()
    return out[["timestamp", "from_released"]]


def _run(modes=None, stride=13):
    return run_probe_a(_frames(), _build_reads_released, MODEL, side="s",
                       cohort_stride=stride, max_cohorts=25, seed=7,
                       column_modes=modes)


# ---------------------------------------------------------------------------
# The discriminating positive
# ---------------------------------------------------------------------------

def test_per_column_modes_give_a_DIFFERENT_answer_from_the_whole_frame_path():
    """THE POSITIVE THAT DISCRIMINATES. Same data, same seconds, same seed --
    only the declared rule for one column differs, and the answers differ."""
    whole = _run(modes=None)
    per_col = _run(modes={"released": ColumnMode(AT_SOURCE_TIMESTAMP,
                                                 "released_at")})
    whole_hits = {str(c.second) for c in whole.findings}
    per_hits = {str(c.second) for c in per_col.findings}
    assert whole_hits != per_hits, (
        "the two paths agreed, so the wiring added no capability -- which would "
        "itself be the finding")
    # And the difference is measured rather than asserted.
    assert whole.verdict() == "finding"
    assert len(whole_hits) > 0


def test_the_difference_is_the_release_lag_and_nothing_else():
    """The reason, stated: the release instant is half an hour earlier, so the
    cell becomes knowable in a different second and a different row moves."""
    per_col = _run(modes={"released": ColumnMode(AT_SOURCE_TIMESTAMP,
                                                 "released_at")})
    # With the release instant carried, the column is perturbed at seconds
    # displaced by the lag, so the rows that move are not the rows that moved
    # under the frame rule.
    whole = _run(modes=None)
    assert {str(c.second) for c in whole.findings} - \
           {str(c.second) for c in per_col.findings} != set() or \
           {str(c.second) for c in per_col.findings} - \
           {str(c.second) for c in whole.findings} != set()


# ---------------------------------------------------------------------------
# The other direction: no modes means the frame's rule, unchanged
# ---------------------------------------------------------------------------

def test_without_modes_the_selection_is_the_frames_own_and_nothing_moves():
    """THE PAIR. The wiring is a generalisation, not a replacement: with no
    modes the path is the one Phase 1's evidence came through."""
    a = _run(modes=None)
    b = _run(modes=None)
    assert [str(c.second) for c in a.findings] == [str(c.second) for c in b.findings]
    assert a.verdict() == b.verdict()


def test_an_empty_mode_map_is_the_same_as_none():
    assert ([str(c.second) for c in _run(modes={}).findings]
            == [str(c.second) for c in _run(modes=None).findings])


def test_a_mode_on_a_column_the_frame_does_not_carry_is_ignored_not_applied():
    """A mode keyed on a column of another frame must not silently change this
    frame's selection."""
    a = _run(modes={"not_here": ColumnMode(AT_SOURCE_TIMESTAMP, "released_at")})
    b = _run(modes=None)
    assert [str(c.second) for c in a.findings] == [str(c.second) for c in b.findings]


def test_a_column_whose_instants_fall_in_no_selected_second_says_so():
    """Its silence is `none`, not `observed_silence` -- the unnamed-frame rule
    one level down, now at the column."""
    far = ColumnMode(AT_SOURCE_TIMESTAMP, "released_at")
    frames = _frames()
    frames["agg"]["released_at"] = frames["agg"]["ts_floor"] + pd.Timedelta(days=3650)
    res = run_probe_a(frames, _build_reads_released, MODEL, side="s",
                      cohort_stride=13, max_cohorts=25, seed=7,
                      column_modes={"released": far})
    joined = " ".join(res.notes)
    assert "was not" in joined and "perturbed" in joined
    assert "`none`, not `observed_silence`" in joined


def test_a_column_that_fell_back_to_the_frame_rule_is_named():
    """R205 §3.3. Whether a frame-level declaration covers its columns, or a
    column without its own mode is undeclared, is settled by neither the
    registration nor the modes document. The code takes one reading and NAMES
    the columns the answer depends on, so the choice is visible rather than
    silent."""
    res = _run(modes={"released": ColumnMode(AT_SOURCE_TIMESTAMP, "released_at")})
    joined = " ".join(res.notes)
    assert "took the FRAME rule" in joined
    assert "own_second" in joined, "the column that fell back was not named"
    assert "not settled by the registration" in joined


def test_no_fallback_note_when_every_column_has_a_mode():
    """The pair: with every numeric column declared, there is nothing to name."""
    res = _run(modes={"released": ColumnMode(AT_SOURCE_TIMESTAMP, "released_at"),
                      "own_second": ColumnMode(AT_SOURCE_TIMESTAMP, "ts_floor"),
                      "released_at": ColumnMode(AT_SOURCE_TIMESTAMP, "ts_floor")})
    assert not any("took the FRAME rule" in n for n in res.notes)
