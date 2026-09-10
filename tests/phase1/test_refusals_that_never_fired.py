"""The six refusals TB-25 measured as never having fired, one test each.

R265 §4. A refusal is an absence claim until a positive reddens it: until a case
produces the condition, "this is guarded" is a sentence beside the code and not a
property of it. TB-25's siblings line enumerated six across the two probes, found
by searching the suite for each refusal's own message text.

TWO OF THEM TURN OUT TO BE UNREACHABLE, and that is the deliverable rather than a
gap. R265 §4 asks for the classification and forbids deleting either kind this
round, so each is classified here with the reason, and nothing is removed.
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
    AvailabilityModel, ProbeError, eligible_cohorts, run_probe_a)
from leakaudit.label_probe import (                                # noqa: E402
    LabelAvailability, RawLabel, _assert_only_unavailable_labels_moved,
    run_probe_l2a)

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def _frames(n=30):
    return {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(n)],
                                 "v": np.arange(n, dtype="float64")})}


def _build(raw):
    """Decision instants come from a FIXED range, not from the frame's key.

    That separation is what lets a test move the key out of the probed seconds
    without moving the probed seconds with it -- which is the only way to reach
    a run whose declared frame matches nothing.
    """
    agg = raw["agg"]
    n = len(agg)
    return pd.DataFrame({"d": [T0 + i * SEC for i in range(n)],
                         "x": agg["v"].to_numpy()})


# --------------------------------------------------------------------------
# 1. REACHABLE. `eligible_cohorts`, every selected second uncarried.
# --------------------------------------------------------------------------

def test_1_NO_selected_second_is_carried_by_any_declared_frame():
    """The note that separates a run whose cohorts are all ineligible from one
    that probed. Fired by selecting seconds a year away from the data."""
    raw = _frames()
    d = pd.to_datetime(_build(raw)["d"])
    picked = [T0 + pd.Timedelta(days=365) + i * SEC for i in range(3)]
    res = eligible_cohorts(raw, MODEL, picked, d)
    assert res.eligible == ()
    joined = "\n".join(res.notes)
    assert "NO selected second is carried by any declared aggregate frame" in joined
    assert "`none` rather than `observed_silence`" in joined


# --------------------------------------------------------------------------
# 2. REACHABLE. A declared frame that was not supplied.
# --------------------------------------------------------------------------

def test_2_a_DECLARED_frame_that_was_not_supplied_refuses_and_names_it():
    """R210's walk found this with one frame misspelled -- `scan` for `scans`.
    The message names the declared set and the supplied set, so the fix is
    visible without reading the model file."""
    # The frame IS supplied, under the name the builder reads; the MODEL names
    # a different one. That is the misspelling R210 hit, and it is the only
    # shape that reaches this branch: with any declared frame present and
    # matching, `touched` is non-zero and the run proceeds with a note instead.
    model = AvailabilityModel(aggregate_frames={"scans": "t"},
                              decision_column="d")
    with pytest.raises(ProbeError) as e:
        run_probe_a(_frames(), _build, model, side="absent",
                    cohort_stride=2, max_cohorts=5)
    msg = str(e.value)
    assert "were not supplied" in msg
    assert "'scans'" in msg, "the refusal must name the DECLARED set: %s" % msg
    assert "Supplied:" in msg and "'agg'" in msg, (
        "and the SUPPLIED set, or the fix is invisible: %s" % msg)


# --------------------------------------------------------------------------
# 3. REACHABLE. A builder whose output shape moves under corruption.
# --------------------------------------------------------------------------

def test_3_a_corrupted_build_that_CHANGES_SHAPE_refuses():
    """Rows cannot be compared positionally if the build returns a different
    number of them, and a probe that compared them anyway would attribute
    movement to whichever rows happened to line up."""
    def dropping_build(raw):
        agg = raw["agg"]
        out = pd.DataFrame({"d": agg["k"].to_numpy(),
                            "x": agg["v"].to_numpy()})
        # The perturbation is large and positive, so this drops exactly the
        # corrupted rows and nothing else on a clean run.
        return out[out["x"] < 1.0e5].reset_index(drop=True)

    with pytest.raises(ProbeError) as e:
        run_probe_a(_frames(), dropping_build, MODEL, side="shape",
                    cohort_stride=2, max_cohorts=5)
    assert "changed shape" in str(e.value)
    assert "compared positionally" in str(e.value)


# --------------------------------------------------------------------------
# 4 and 5. REACHABLE AS A FUNCTION, UNREACHABLE THROUGH THE PROBE.
#
# These are `DESIGN.md` §2.7's every-call assertion. They fire only if the
# probe perturbed something it should not have -- which is to say, only if the
# probe is broken. No user input reaches them, and that is the point of them:
# they guard the probe's own correctness, not the caller's declaration. So the
# positive calls the check directly, with a corrupted frame built by hand, and
# the classification below says why the probe cannot produce one.
# --------------------------------------------------------------------------

def test_4_an_AVAILABLE_label_cell_perturbed_is_caught_by_the_assertion():
    raw = {"lab": pd.DataFrame({"ts": [T0, T0 + SEC], "y": [1.0, 2.0]})}
    corrupt = {"lab": raw["lab"].copy()}
    corrupt["lab"].loc[0, "y"] = 99.0          # cell 0 is NOT in the mask
    mask = np.array([False, True])
    with pytest.raises(ProbeError) as e:
        _assert_only_unavailable_labels_moved(raw, corrupt,
                                              RawLabel("lab", "y"), mask)
    assert "an AVAILABLE label cell was perturbed" in str(e.value)


def test_5_a_NON_LABEL_column_that_changed_is_caught_by_the_assertion():
    raw = {"lab": pd.DataFrame({"ts": [T0, T0 + SEC], "y": [1.0, 2.0],
                                "other": [3.0, 4.0]})}
    corrupt = {"lab": raw["lab"].copy()}
    corrupt["lab"].loc[1, "other"] = 99.0
    mask = np.array([False, True])
    with pytest.raises(ProbeError) as e:
        _assert_only_unavailable_labels_moved(raw, corrupt,
                                              RawLabel("lab", "y"), mask)
    assert "column 'other' of the label frame changed" in str(e.value)


def test_the_ASSERTION_passes_on_a_correct_perturbation():
    """The negative half. Without it the two above would pass against a check
    that raised on everything."""
    raw = {"lab": pd.DataFrame({"ts": [T0, T0 + SEC], "y": [1.0, 2.0],
                                "other": [3.0, 4.0]})}
    corrupt = {"lab": raw["lab"].copy()}
    corrupt["lab"].loc[1, "y"] = 99.0
    _assert_only_unavailable_labels_moved(raw, corrupt, RawLabel("lab", "y"),
                                          np.array([False, True]))


# --------------------------------------------------------------------------
# 6. UNREACHABLE BY CONSTRUCTION, and this test pins the reason.
# --------------------------------------------------------------------------

def test_6_the_no_aggregate_cells_matched_branch_is_UNREACHABLE_and_why():
    """`run_probe_a`'s `touched == 0` branch has a second message -- "no
    aggregate cells matched the corrupted seconds" -- for the case where every
    declared frame WAS supplied and none of them matched. **It cannot be
    reached**, and the reason is a guard one loop above it:

        for each declared frame present in `raw`:
            if not mask.any(): raise "frame %r matched NO corrupted second"

    A present frame with no match raises there, naming the frame. A frame
    absent from `raw` is skipped by `continue`, so it contributes nothing to
    `touched` -- but then `absent` is non-empty and the FIRST message fires
    instead. `touched == 0` with every declared frame present therefore
    requires a present frame whose mask is empty, which the guard above has
    already refused.

    CLASSIFIED: unreachable by construction, not by defect. It is a correct
    message for a state the code prevents earlier, and R265 §4 forbids deleting
    it this round. What this test pins is the PREEMPTION -- if the per-frame
    guard is ever removed or narrowed, this fails and the branch becomes live.
    """
    raw = _frames()
    with pytest.raises(ProbeError) as e:
        run_probe_a({"agg": raw["agg"].assign(k=raw["agg"]["k"]
                                              + pd.Timedelta(days=365))},
                    _build, MODEL, side="nomatch", cohort_stride=2,
                    max_cohorts=5)
    msg = str(e.value)
    assert "matched NO corrupted second" in msg, (
        "the per-frame guard must be what fires; if this is now the "
        "`no aggregate cells matched` message, the preemption is gone and that "
        "branch is live: %s" % msg)
    assert "no aggregate cells matched" not in msg
