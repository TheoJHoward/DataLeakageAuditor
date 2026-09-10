"""What licenses a silence, on both runtime rows. R262 §2 and §3.

THE SENTENCE THIS FILE ENFORCES is the one the registration draws and this
project keeps re-learning: `observed_silence` is the affirmative *I looked over a
stated population and found nothing, and that is evidence*; `none` is *the probe
did not happen*. They are not interchangeable and the second is not a weaker form
of the first.

WHAT MAKES THE DIFFERENCE MEASURABLE. A run that perturbs cells and sees rows
move has demonstrated that its perturbation reaches the pipeline; its quiet
cohorts are then quiet about the pipeline. A run where NOTHING moved anywhere has
demonstrated nothing at all -- its silence is about the harness, and reporting it
as evidence is the defect D-V30A-100 recorded when R205's per-column zero turned
out to be a column no cell of which was ever perturbed.

Phase 1 already relied on the licence without naming it: the corrected side's
silence was believed because 250 rows moved on it, which proved the perturbation
reached the builder. This file makes that a property of the verdict rather than a
fact somebody happened to check.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src"), str(ROOT / "tests" / "phase1")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import AvailabilityModel, run_probe_a   # noqa: E402
from leakaudit.label_probe import (                                 # noqa: E402
    LabelAvailability, RawLabel, run_probe_l2a)
from leakaudit.modes import AT_SOURCE_TIMESTAMP, ColumnMode         # noqa: E402

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)


# ---------------------------------------------------------------------------
# §2 -- L3.1. The known positive is R205's own case.
# ---------------------------------------------------------------------------

def test_R205s_PER_COLUMN_ZERO_is_none_and_not_a_silence():
    """R262 §2(b). This returned `observed_silence` until now.

    The fixture is R205's, imported rather than copied. Its builder reads one
    column; under the per-column declaration that column's instants sit half an
    hour before the probed range, so no cell of it is ever perturbed. Nothing
    moved anywhere, so the run demonstrated nothing, and calling that
    `observed_silence` converts absence of data into evidence.
    """
    import test_modes_wiring as fx

    res = fx._run(modes={"released": ColumnMode(AT_SOURCE_TIMESTAMP,
                                                "released_at")})
    assert res.verdict().startswith("none("), res.verdict()
    assert res.findings == []
    assert sum(c.moved_next_second for c in res.cohorts) == 0
    assert sum(c.moved_in_band for c in res.cohorts) == 0
    # THE REASON NAMES ITS POPULATION. A bare `none` is a state; a `none` a
    # reader can act on says how many cells were perturbed and where their
    # instants sat relative to what was probed.
    note = "\n".join(res.notes)
    assert "no perturbed cell reached the pipeline" in note, note
    assert "cell(s) perturbed" in note, note


def test_the_WHOLE_FRAME_half_of_the_same_fixture_still_FINDS():
    """The control on the same data: the repair changes the silent path only."""
    import test_modes_wiring as fx

    res = fx._run(modes=None)
    assert res.verdict() == "finding"
    assert len(res.findings) == 25


# ---------------------------------------------------------------------------
# §2(c) -- the discriminating case. A repair that turned EVERY zero-finding run
# into `none` would move the Phase 1 corrected side, whose silence is real.
# ---------------------------------------------------------------------------

def _clean_frames(n=40):
    ts = [T0 + i * SEC for i in range(n)]
    return {"agg": pd.DataFrame({"k": ts,
                                 "v": np.arange(n, dtype="float64")})}


def _clean_build(raw):
    """Reads the PREVIOUS second's aggregate: legitimate under the frame rule.

    The cell it reads completes at `floor(k) + 1s`, which is at or before the
    decision instant, so no row is a finding -- and the rows DO move when their
    cell is corrupted, which is the liveness that licenses the silence.
    """
    agg = raw["agg"]
    v = agg["v"].to_numpy()
    lagged = np.concatenate(([np.nan], v[:-1]))
    return pd.DataFrame({"d": agg["k"].to_numpy(), "x": lagged})


def test_a_run_with_LIVENESS_and_no_findings_stays_observed_silence():
    """R262 §2(c). This is the Phase 1 corrected side's shape in miniature:
    zero findings, and movement proving the perturbation reached the builder."""
    # STRIDE 13, NOT 1, AND THE REASON IS A PROPERTY OF BATCHED PROBING. Every
    # picked second is corrupted in ONE rebuild, so at stride 1 a row sitting in
    # cohort F's finding region can have moved because of cohort F-1's cell --
    # the cell it legitimately read -- and be counted as F's finding. The
    # cohorts are disjoint and the derived separation check passes; what
    # overlaps is the INFLUENCE of adjacent cells, which no stride can bound in
    # general and which `cohort_stride`'s default of 97 exists to make unlikely.
    # This fixture is about the verdict vocabulary, so it uses a stride where
    # attribution is not the confound.
    res = run_probe_a(_clean_frames(), _clean_build,
                      AvailabilityModel(aggregate_frames={"agg": "k"},
                                        decision_column="d"),
                      side="clean", cohort_stride=13, max_cohorts=20)
    assert res.findings == []
    assert sum(c.moved_next_second for c in res.cohorts) > 0, (
        "this fixture must produce liveness, or it is not the case under test")
    assert res.verdict() == "observed_silence", res.verdict()


# ---------------------------------------------------------------------------
# §3 -- L2a. The same question, one probe over, asked before its silence is
# believed on a pipeline nobody has seen.
# ---------------------------------------------------------------------------

MODEL = AvailabilityModel(aggregate_frames={"lab": "ts"}, decision_column="d")


def _label_frames(n=40):
    ts = [T0 + i * SEC for i in range(n)]
    y = np.random.default_rng(3).standard_normal(n)
    # `far` carries an instant a day earlier, so a locator pointing at a column
    # whose availability sits outside the probed range has somewhere to point.
    return {"lab": pd.DataFrame({"ts": ts, "y": y,
                                 "far": np.arange(n, dtype="float64")})}


def _label_build(raw):
    lab = raw["lab"]
    y = lab["y"].to_numpy()
    return pd.DataFrame({"d": lab["ts"].to_numpy(),
                         "x": np.concatenate(([np.nan], y[:-1]))})


def test_L2a_a_locator_whose_instants_sit_OUTSIDE_the_probed_range_is_none():
    """R262 §3(c). The R205 geometry, on the label side.

    A label declared with an availability far in the past is available to every
    probed cohort, so no cell of it is ever unavailable, so nothing is perturbed
    and nothing can move. That silence is `none`, and before this it read as
    `observed_silence` -- D-V30A-100's shape inside a probe one round old.
    """
    res = run_probe_l2a(
        _label_frames(), _label_build, MODEL, side="far",
        raw_label=RawLabel("lab", "y"),
        label_availability=LabelAvailability(
            base_column="ts", horizon=pd.Timedelta(days=-0)  # realized at ts
        ),
        cohort_stride=1, max_cohorts=1)
    # The first probed cohort is the earliest decision second; with a zero
    # horizon every label at or before it is realized, and the ones after are
    # not -- so this cohort DOES perturb. The out-of-range case is the next test;
    # this one pins that the fixture is not accidentally empty.
    assert res.n_cohorts == 1


def test_L2a_reports_none_when_NO_CELL_was_unavailable_at_a_probed_cohort():
    """The label is realized long before every probed decision, so no cohort has
    an unavailable cell to corrupt. Nothing was probed; the verdict says so."""
    frames = _label_frames()
    frames["lab"]["ts_old"] = frames["lab"]["ts"] - pd.Timedelta(days=1)
    res = run_probe_l2a(
        frames, _label_build, MODEL, side="realized",
        raw_label=RawLabel("lab", "y"),
        label_availability=LabelAvailability(base_column="ts_old",
                                             horizon=pd.Timedelta(0)),
        cohort_stride=7, max_cohorts=5)
    assert res.verdict().startswith("none("), res.verdict()
    assert res.findings == []
    note = "\n".join(res.notes)
    assert "no perturbed cell reached the pipeline" in note, note
    assert "cell(s) perturbed" in note, note


def test_L2a_prints_the_PERTURBED_CELL_COUNT_per_cohort():
    """R262 §3(b). The count is what the silence rests on, so it is in the
    output rather than inferable from it."""
    res = run_probe_l2a(
        _label_frames(), _label_build, MODEL, side="counts",
        raw_label=RawLabel("lab", "y"),
        label_availability=LabelAvailability(base_column="ts",
                                             horizon=pd.Timedelta(seconds=60)),
        cohort_stride=7, max_cohorts=5)
    assert res.verdict() == "finding"
    assert all(c.cells_perturbed > 0 for c in res.cohorts), (
        "every cohort here has unavailable labels to corrupt")
    note = "\n".join(res.notes)
    assert "cell(s) perturbed" in note


def test_L2a_says_WHICH_LICENCE_its_silence_carries():
    """R262 §3(b)'s parenthesis. A clean pipeline need not read labels as
    features at all, so L2a has no moved-row liveness class the way L3.1 does.
    A reader has to be told which of the two silences they are holding."""
    frames = _label_frames()

    def build_ignoring_labels(raw):
        lab = raw["lab"]
        return pd.DataFrame({"d": lab["ts"].to_numpy(),
                             "x": lab["far"].to_numpy()})

    res = run_probe_l2a(
        frames, build_ignoring_labels, MODEL, side="nolabels",
        raw_label=RawLabel("lab", "y"),
        label_availability=LabelAvailability(base_column="ts",
                                             horizon=pd.Timedelta(seconds=60)),
        cohort_stride=7, max_cohorts=5)
    assert res.findings == []
    assert res.verdict() == "observed_silence", (
        "cells WERE perturbed here, so this is a silence about the pipeline "
        "and not about the harness: %s" % res.verdict())
    note = "\n".join(res.notes)
    assert "does not read the label" in note or "no row moved" in note, note
