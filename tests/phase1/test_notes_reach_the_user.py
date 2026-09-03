"""What the probe says about a run reaches whoever ran it. R208 §3.

FOUND BY WALKING THE PATH, NOT BY A TEST, which is why this file exists. The
probe appends notes for things the reader has to know: that a non-boundary key
was floored and by how much, that a column with no declared mode took the
frame's rule, that an aggregate frame was declared and absent so nothing in it
was corrupted. `AuditResult.explain()` rendered the unprobed frames, the domain
and the check tally, and rendered NONE of those notes. Every one of them was
invisible to every user of the command.

That is the fourth instance of the class this project keeps finding: a detection
that exists and does not arrive. The first three arrived as library exceptions
nobody reads as detections (TB-13). This one arrived in a field nothing printed
-- and it made a commit message's claim that a conflict is surfaced "in the run's
own output" false for everyone not calling the library directly.

The positive here is that the flooring report -- the one R207 made a halt of
shipping silently -- is present in rendered output for a key that needs it and
absent for one that does not.
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
from leakaudit.availability_trace import traces_for                # noqa: E402
from leakaudit.findings import AuditResult                         # noqa: E402

N = 240
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"},
                          decision_column="timestamp")


def _result(offset_ms, extra_frame=False):
    secs = pd.date_range("2026-06-01 11:00:00", periods=N, freq="1s")
    rng = np.random.default_rng(3)
    raw = {
        "snap": pd.DataFrame({
            "timestamp": [s + pd.Timedelta(milliseconds=200) for s in secs]}),
        "agg": pd.DataFrame({"k": secs + pd.Timedelta(milliseconds=offset_ms),
                             "v": rng.standard_normal(N)}),
    }
    if extra_frame:
        raw["other"] = pd.DataFrame({"t": secs, "z": rng.standard_normal(N)})

    def build(frames):
        out = frames["snap"].copy()
        out["sec"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
        a = frames["agg"].copy()
        a["sec"] = pd.to_datetime(a["k"]).dt.floor("s")
        out["v"] = out["sec"].map(a.set_index("sec")["v"]).to_numpy()
        return out[["timestamp", "v"]]

    res = run_probe_a(raw, build, MODEL, side="user",
                      cohort_stride=9, max_cohorts=15, seed=2)
    return AuditResult(traces_for(res, [c.second for c in res.cohorts],
                                  case_id="user"), source=res)


def test_the_flooring_report_is_in_the_RENDERED_output():
    text = _result(offset_ms=400).explain()
    assert "flooring to" in text, (
        "the flooring report did not reach the rendered output. R207 makes "
        "flooring a non-boundary key without reporting it a halt, and a report "
        "that only a library caller can reach is not a report:\n%s" % text)
    assert "floor(k) + 1s" in text
    assert "ABOUT THIS RUN" in text


def test_a_key_that_needs_NO_flooring_produces_no_such_line():
    text = _result(offset_ms=0).explain()
    assert "flooring to" not in text, (
        "a frame whose key is already a wall-clock second was reported as "
        "floored, so the line is a banner rather than a report:\n%s" % text)


def test_the_unprobed_frame_fact_is_stated_ONCE():
    """It is rendered from the structured field AND stated as a note."""
    text = _result(offset_ms=400, extra_frame=True).explain()
    assert text.count("NOT PROBED") == 1, (
        "the same fact is printed twice in one screen, which teaches the "
        "reader that this section repeats itself:\n%s" % text)
    assert "other" in text


def test_notes_are_read_from_the_source_and_not_cached():
    """`AuditResult` is a view. The notes property must not copy state."""
    r = _result(offset_ms=400)
    before = len(r.notes)
    r.source.notes.append("added after the view was built")
    assert len(r.notes) == before + 1, (
        "the view cached the notes, so a result and its source can disagree -- "
        "the defect this class was rewritten to prevent")
    assert "added after the view was built" in r.explain()
