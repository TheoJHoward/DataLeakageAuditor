"""The tie branch is wired, and its positive DISCRIMINATES. R216 §2.

WHAT WAS WRONG. `AvailabilityModel.available()` -- the comparator `PREREG.md`
§2.3 locks, argued for at length in §0.3 Claim A -- had no caller anywhere in the
repository. `ties_available` was parsed, type-checked, refused if non-boolean,
and documented in `leakaudit schema`; the probe never read it. A user writing
`ties_available: false` got the opposite rule and no error, which is P0's shape
exactly: doing the right thing and being silently ignored.

NO PUBLISHED FIGURE MOVES, AND THAT WAS CHECKED RATHER THAN ASSUMED. The implicit
behaviour was `a <= d` -- the registered default -- so every recorded result was
computed under the declared rule. The default's behaviour is unchanged here, and
`test_the_DEFAULT_branch_is_byte_for_byte_what_it_was` is the assertion of that.

THE POSITIVE HAS TO DISCRIMINATE, and R215 §0's refinement is what says so --
applied immediately to the defect that produced it. The two branches differ on
exactly one input: a decision row stamped EXACTLY at an aggregate's completion
instant. A positive built from a 200 ms stamp -- the shape the B-6 controls use --
passes under both branches and proves nothing, which is precisely how the
inertness survived.
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

from leakaudit.availability import AvailabilityModel, run_probe_a  # noqa: E402

N = 400
WINDOW = pd.Timedelta(seconds=1)


def _frames(offset_ms):
    """`offset_ms` is where each decision row sits inside its own second.

    0 puts every row EXACTLY on a second boundary. A row at second S reads the
    aggregate of second S-1, whose instant is exactly S -- the tie.
    """
    secs = pd.date_range("2026-02-02 09:00:00", periods=N, freq="1s")
    rng = np.random.default_rng(19)
    agg = pd.DataFrame({"ts_floor": secs, "v": rng.standard_normal(N)})
    snap = pd.DataFrame({
        "timestamp": [s + pd.Timedelta(milliseconds=offset_ms) for s in secs]})
    return {"snap": snap, "agg": agg}


def _build_reads_previous_second(raw):
    """Reads the PREVIOUS second's aggregate: instant exactly the row's stamp
    when the row sits on a boundary. Legal under `<=`, illegal under `<`."""
    out = raw["snap"].copy()
    out["sec"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    a = raw["agg"].set_index("ts_floor")["v"]
    out["feature"] = (out["sec"] - WINDOW).map(a).to_numpy()
    return out[["timestamp", "feature"]]


def _run(ties, offset_ms, build=_build_reads_previous_second):
    model = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                              decision_column="timestamp",
                              ties_available=ties)
    return run_probe_a(_frames(offset_ms), build, model, side="t",
                       cohort_stride=13, max_cohorts=20, seed=4)


def _findings(res):
    return sum(1 for c in res.cohorts if c.finding())


# ---------------------------------------------------------------------------
# THE DISCRIMINATING POSITIVE -- stamps exactly on the boundary.
# ---------------------------------------------------------------------------

def test_on_the_tie_the_two_branches_DISAGREE():
    avail, unavail = _run(True, 0), _run(False, 0)
    assert _findings(avail) == 0, (
        "under the registered default a cell whose instant equals the decision "
        "instant has arrived, so reading it is legal: %d findings"
        % _findings(avail))
    assert _findings(unavail) > 0, (
        "under `ties_available=False` the same read is illegal and must fire. "
        "It did not, which is the inertness this test exists to prevent "
        "returning: %d findings" % _findings(unavail))


def test_the_NON_BOUNDARY_case_cannot_tell_them_apart():
    """The negative control for the positive above, and the reason it is needed.

    At 200 ms inside the second the two branches agree, so a positive built on
    that shape would pass whether or not the key was wired -- which is how the
    key stayed inert through every previous suite.
    """
    a, u = _run(True, 200), _run(False, 200)
    assert _findings(a) == _findings(u), (
        "the branches differ off the boundary, so this control is not "
        "controlling what it claims")


def test_the_DEFAULT_branch_is_byte_for_byte_what_it_was():
    """No published figure moves. The default path must be untouched."""
    for offset in (0, 200, 450):
        res = _run(True, offset)
        assert _findings(res) == 0, (
            "the default branch now fires at offset %d ms where it did not; "
            "every recorded Phase 1 figure was computed under this branch"
            % offset)


def test_only_the_TIE_ROWS_move_between_branches():
    """Not 'more findings' -- the specific rows the comparator disagrees about."""
    unavail = _run(False, 0)
    for c in unavail.cohorts:
        assert c.moved_next_second == 0, (
            "a row was still counted as next-second under the strict branch; "
            "the tie rows should have moved into the in-second bucket")


# ---------------------------------------------------------------------------
# THE COMPARATOR TRAVELS WITH THE RESULT.
# ---------------------------------------------------------------------------

def test_the_non_default_branch_says_so_LOUDLY():
    notes = "\n".join(_run(False, 0).notes)
    assert "COMPARATOR IS NOT THE DEFAULT" in notes, notes
    assert "a(j,c) < d(i)" in notes
    assert "Every finding below was computed under that branch" in notes


def test_the_default_branch_still_names_its_comparator():
    notes = "\n".join(_run(True, 0).notes)
    assert "ties AVAILABLE" in notes and "a(j,c) <= d(i)" in notes, notes
    assert "NOT THE DEFAULT" not in notes


@pytest.mark.parametrize("ties", [True, False])
def test_the_comparator_note_is_rendered_to_the_user(ties):
    from leakaudit.availability_trace import traces_for
    from leakaudit.findings import AuditResult

    res = _run(ties, 0)
    out = AuditResult(traces_for(res, [c.second for c in res.cohorts],
                                 case_id="t"), source=res)
    assert "comparator" in out.explain().lower(), (
        "the comparator is in the notes and not in the rendered output, which "
        "is where a user meets it:\n%s" % out.explain())
