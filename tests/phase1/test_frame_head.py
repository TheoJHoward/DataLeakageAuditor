"""The head of the frame: rows whose lookback reads before the frame. R269 §2.

THE CASE THE REACH WAS FOR. A plain frame that was cut from something longer
carries no declaration of it, so no slice rule can refuse it. When the builder
emits values from a partial window, the head rows still move when in-frame cells
are perturbed -- that is liveness, the licence for a silence -- while the cells
their production lookback actually leaks on lie before the frame and were never
perturbed. The verdict is `observed_silence` over a real leak.

THE DATA. Cells before a cut point C were revised late: `released_at = key + 21 s`,
so a row reading one within its 10-bucket lookback reads a cell that had not
arrived. Cells from C on are on time, available at the end of their own bucket.
The builder is the mean of the previous 10 buckets with `min_periods=1`.

**THE RED, shown on the pre-R269 code before any of this was built**, by
`r269_head_red.py`: the UNCUT frame -> `finding` (4 findings, liveness 8); the
frame CUT at C -> `observed_silence` (0 findings, liveness 5); the cut frame's
head cohort alone -> `observed_silence` (liveness 1). Reach 10.5 s in both.

THE PAIR HOLDS the builder, the stride, and every row from C on byte-for-byte,
and VARIES only whether the rows before C are present.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit import cli                                         # noqa: E402
from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402
from leakaudit.modes import AT_SOURCE_TIMESTAMP, ColumnMode        # noqa: E402

T0 = pd.Timestamp("2026-01-01 00:00:00")
N, CUT_S, LOOKBACK, ON_TIME_S, LATE_S = 120, 60, 10, 1, 21
C = T0 + pd.Timedelta(seconds=CUT_S)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")
MODES = {"v": ColumnMode(AT_SOURCE_TIMESTAMP, "released_at")}
HEAD_VERDICT = "none(lookback exceeds the frame's head"


def _frames(start):
    secs = pd.date_range(start, T0 + pd.Timedelta(seconds=N), freq="1s",
                         inclusive="left")
    step = ((secs - T0) // pd.Timedelta(seconds=1)).astype("int64")
    released = np.where(secs < C, secs + pd.Timedelta(seconds=LATE_S),
                        secs + pd.Timedelta(seconds=ON_TIME_S))
    agg = pd.DataFrame({"k": secs, "v": (step % 17 + 1).astype(float),
                        "released_at": pd.to_datetime(released)})
    dec = pd.DataFrame({"d": secs + pd.Timedelta(milliseconds=500), "row": step})
    return {"agg": agg, "dec": dec}


def _partial_window(fr):
    agg = fr["agg"].sort_values("k").reset_index(drop=True)
    past = agg["v"].shift(1).rolling(LOOKBACK, min_periods=1).mean()
    lookup = pd.Series(past.to_numpy(), index=pd.to_datetime(agg["k"]))
    out = fr["dec"].sort_values("d").reset_index(drop=True).copy()
    out["feat"] = pd.to_datetime(out["d"]).dt.floor("s").map(lookup)
    return out


def _probe(fr, **kw):
    return run_probe_a(fr, _partial_window, MODEL, side="t",
                       column_modes=MODES, cohort_stride=12, **kw)


# --------------------------------------------------------------------------
# the pair
# --------------------------------------------------------------------------

def test_the_LEAK_IS_REAL_in_the_uncut_frame():
    """Without this the pair shows only that a clean frame stays clean."""
    assert _probe(_frames(T0), max_cohorts=10 ** 9).verdict() == "finding"


def test_the_HEAD_COHORT_alone_is_NONE_with_its_reason_never_SILENCE():
    """THE DISCRIMINATING HALF. Before R269 this read `observed_silence`,
    liveness 1: a silence licensed by in-frame movement over a row whose
    production lookback leaks on cells the frame does not contain."""
    r = _probe(_frames(C), max_cohorts=1)
    assert r.verdict().startswith(HEAD_VERDICT), r.verdict()
    assert r.head_seconds == (pd.Timestamp(C),)
    assert r.liveness > 0, "the head row still moves -- that is the trap"


def test_THE_PAIR_varies_only_the_cut():
    """HELD: builder, stride, every row from C on. VARIED: rows before C."""
    uncut, cut_fr = _frames(T0), _frames(C)
    tail = uncut["agg"][uncut["agg"]["k"] >= C].reset_index(drop=True)
    assert cut_fr["agg"].reset_index(drop=True).equals(tail), (
        "the cut frame is a suffix of the uncut one, not a rebuild")

    before = _probe(uncut, max_cohorts=10 ** 9)
    after = _probe(cut_fr, max_cohorts=10 ** 9)
    assert before.verdict() == "finding"
    assert pd.Timestamp(C) in after.head_seconds
    # The verdict over the remaining rows is whatever it is -- here, silence
    # over the on-time cells after the head, with the head held out of it.
    assert after.verdict() == "observed_silence", after.verdict()
    assert any(n.startswith("HEAD OF FRAME:") for n in after.notes)


def test_the_head_reason_says_the_reach_is_a_LOWER_BOUND():
    """R269 §2(d): and names the residual that remains."""
    r = _probe(_frames(C), max_cohorts=1)
    assert "LOWER BOUND from 3 sample(s)" in r.head_reason
    assert "a lookback that showed in none of 3 samples" in r.head_reason
    assert "cells before the frame cannot be probed" in r.head_reason


# --------------------------------------------------------------------------
# what the head rule does NOT do
# --------------------------------------------------------------------------

def _current_bucket(fr):
    """Reads its own second, which completes after the decision: a leak on an
    IN-frame cell, whatever row it sits in."""
    agg = fr["agg"].sort_values("k").reset_index(drop=True)
    lookup = pd.Series(agg["v"].to_numpy(), index=pd.to_datetime(agg["k"]))
    out = fr["dec"].sort_values("d").reset_index(drop=True).copy()
    out["feat"] = pd.to_datetime(out["d"]).dt.floor("s").map(lookup)
    return out


def test_a_FINDING_in_the_head_is_STILL_a_finding():
    """The rule withholds a SILENCE. A moved row with an unavailable in-frame
    cell is evidence wherever it sits, and hiding it would be the mirror
    defect."""
    r = run_probe_a(_frames(C), _current_bucket, MODEL, side="t",
                    cohort_stride=12, max_cohorts=1)
    assert r.head_seconds, "the probed cohort sits in the head"
    assert r.verdict() == "finding"


def test_an_UNMEASURED_reach_leaves_the_head_NOT_ASSESSED_and_says_so():
    r = _probe(_frames(C), max_cohorts=1, reach_samples=0)
    assert r.head_cutoff is None and r.head_seconds == ()
    assert r.head_reason.startswith("HEAD OF FRAME NOT ASSESSED")
    assert any(n.startswith("HEAD OF FRAME NOT ASSESSED") for n in r.notes)


# --------------------------------------------------------------------------
# the table: head seconds are INELIGIBLE, with their own reason
# --------------------------------------------------------------------------

PIPELINE = (
    "import pandas as pd\n"
    "\n"
    "def previous_second(frames):\n"
    "    agg = frames['agg'].copy()\n"
    "    agg['k'] = pd.to_datetime(agg['k'])\n"
    "    out = frames['dec'].copy()\n"
    "    out['d'] = pd.to_datetime(out['d'])\n"
    "    lk = pd.Series(agg['v'].to_numpy(), index=agg['k'] + pd.Timedelta(seconds=1))\n"
    "    out['feat'] = out['d'].dt.floor('s').map(lk)\n"
    "    return out\n")


@pytest.fixture
def work(tmp_path):
    name = "r269_head_pipe"
    (tmp_path / (name + ".py")).write_text(PIPELINE, encoding="utf-8")
    secs = pd.date_range(T0, periods=300, freq="1s")
    pd.DataFrame({"k": secs, "v": [float(i % 17) + 1.0 for i in range(300)]}
                 ).to_csv(tmp_path / "agg.csv", index=False)
    pd.DataFrame({"d": secs + pd.Timedelta(milliseconds=500), "row": range(300)}
                 ).to_csv(tmp_path / "dec.csv", index=False)
    (tmp_path / "m.json").write_text(json.dumps({
        "version": 3, "aggregate_frames": {"agg": "k"},
        "decision_column": "d"}), encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        yield tmp_path, name
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(name, None)


def test_the_TABLE_counts_the_head_as_INELIGIBLE_with_its_own_reason(work, capsys):
    tmp, name = work
    rc = cli.main(["run", "--pipeline", "%s:previous_second" % name,
                   "--frame", "agg=%s" % (tmp / "agg.csv"),
                   "--frame", "dec=%s" % (tmp / "dec.csv"),
                   "--model", str(tmp / "m.json")])
    out = capsys.readouterr().out
    assert rc == cli.EXIT_INCOMPLETE_SILENT
    assert "HEAD OF THE FRAME" in out
    assert "lookback exceeds the frame's head" in out
    assert "ineligible because no declared frame carries a row" in out, (
        "the head is broken out FROM the model-ineligible count, not merged")
