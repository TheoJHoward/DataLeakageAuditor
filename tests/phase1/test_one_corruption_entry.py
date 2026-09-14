"""One corruption entry point, and nothing selects cells by time outside it. R272 §1.

THE DEFECT. For three rounds the reach control kept its own copy of the cell
selection, compared a UTC-aware trades key with naive decision seconds, and
corrupted no trades cell -- pandas answers that comparison with all-False and
raises nothing -- while printing a reach over one frame of two. The probe had
the right rule; the copy did not.

THE MECHANISM. `availability.select_cells` is the one time selection and
`availability.corrupt_cells` the one corruption. Both align through
`to_decision_clock`, refuse an aware/naive comparison, and count cells per
declared frame.

THE TOTALITY. Every call that aligns a clock, selects by `isin`, or perturbs --
in every tracked and untracked module under `src/leakaudit` -- is enumerated
here, and each has to sit inside the entry point or in `ALLOWED` with the reason
it selects no input cell. A new site fails this file until somebody places it.
"""
from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import (                           # noqa: E402
    AvailabilityModel, ProbeError, same_clock, select_cells)
from leakaudit.reach import frames_never_corrupted, measure_reach  # noqa: E402

SRC = ROOT / "src" / "leakaudit"

#: Calls that align a clock, select rows by membership, or perturb cells.
WATCHED = {"perturb_cells", "_perturb", "to_decision_clock", "align_key", "isin"}

#: (module, innermost function) -> why a watched call may sit there.
ALLOWED = {
    ("availability", "select_cells"): "THE entry point's time selection",
    ("availability", "corrupt_cells"): "THE entry point's corruption",
    ("reach", "head_cutoff"):
        "aligns each frame's key to take its FIRST stamp for the head of the "
        "frame; it selects and writes no cell",
    ("cli", "_run_availability"):
        "counts DECISION rows per coverage state with `isin` over the built "
        "output; no input cell is selected or written",
}


def _population() -> list:
    """Tracked AND untracked modules under src/leakaudit: the floor, both ways."""
    out = set()
    for args in (["ls-files"], ["ls-files", "--others", "--exclude-standard"]):
        r = subprocess.run(["git", "-C", str(ROOT), *args, "src/leakaudit"],
                           capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stderr
        out |= {l.strip() for l in r.stdout.splitlines()
                if l.strip().endswith(".py")}
    return sorted(out)


def _watched_calls(source: str, module: str) -> set:
    """(module, innermost enclosing function) for every watched call."""
    tree = ast.parse(source)
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    found = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
        if name not in WATCHED:
            continue
        up = parents.get(node)
        while up is not None and not isinstance(up, (ast.FunctionDef,
                                                     ast.AsyncFunctionDef)):
            up = parents.get(up)
        found.add((module, up.name if up is not None else "<module>"))
    return found


def _live_sites() -> set:
    sites = set()
    for rel in _population():
        p = ROOT / rel
        if p.is_file():
            sites |= _watched_calls(p.read_text(encoding="utf-8"), p.stem)
    return sites


# --------------------------------------------------------------------------
# the totality, both directions, and the scanner's own positive
# --------------------------------------------------------------------------

def test_the_population_is_READ_from_git_and_is_not_empty():
    pop = _population()
    assert "src/leakaudit/availability.py" in pop and "src/leakaudit/reach.py" in pop


def test_EVERY_time_selection_and_corruption_site_goes_through_the_entry_point():
    stray = sorted(_live_sites() - set(ALLOWED))
    assert not stray, (
        "these functions align a clock, select by membership or perturb cells "
        "outside the one entry point, and none is listed with a reason: %s. "
        "Route them through availability.select_cells / corrupt_cells, or add "
        "each to ALLOWED with why it selects no input cell." % stray)


def test_no_ALLOWED_entry_names_a_site_that_is_gone():
    gone = sorted(set(ALLOWED) - _live_sites())
    assert not gone, "listed and no longer present: %s" % gone


def test_the_SCANNER_finds_a_rogue_selection():
    rogue = ("def rogue(frame, second):\n"
             "    return frame['k'].dt.floor('s').isin({second})\n"
             "def fine():\n"
             "    return 1\n")
    assert _watched_calls(rogue, "somewhere") == {("somewhere", "rogue")}


def test_the_retired_copies_are_gone():
    sites = _live_sites()
    for retired in (("reach", "_corrupt_one"), ("reach", "_corrupt_block"),
                    ("label_probe", "run_probe_l2a"), ("label_probe", "_perturb"),
                    ("identity_control", "run_identity_control"),
                    ("availability", "run_probe_a"),
                    ("availability", "eligible_cohorts")):
        assert retired not in sites, "%s still selects or perturbs itself" % (retired,)


# --------------------------------------------------------------------------
# the refusal, R272 §1(b)
# --------------------------------------------------------------------------

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def test_the_OLD_comparison_is_ALL_FALSE_and_raises_nothing():
    """The fact the refusal exists for, pinned on this interpreter."""
    aware = pd.Series(pd.to_datetime([T0]).tz_localize("UTC"))
    assert not bool((aware.dt.floor("s") == T0).any())


def test_an_AWARE_selection_against_the_NAIVE_decision_clock_RAISES():
    frames = {"agg": pd.DataFrame({"k": [T0 + i * SEC for i in range(10)],
                                   "v": np.arange(10.0)})}
    decision = pd.Series([T0 + i * SEC for i in range(10)])
    with pytest.raises(ProbeError) as e:
        select_cells(frames, MODEL, decision,
                     seconds={pd.Timestamp(T0 + 5 * SEC).tz_localize("UTC")})
    msg = str(e.value)
    assert "REFUSED" in msg and "all-False" in msg, msg


@pytest.mark.parametrize("stamps,reference", [
    (pd.Series(pd.to_datetime([T0]).tz_localize("UTC")), T0),
    (pd.Series([T0]), pd.Timestamp(T0).tz_localize("UTC")),
])
def test_same_clock_RAISES_both_ways(stamps, reference):
    with pytest.raises(ProbeError):
        same_clock(stamps, reference, what="a test comparison")


def test_an_AWARE_KEY_is_ALIGNED_not_refused():
    """The negative: a UTC-aware key reaches naive decisions through the one
    alignment and IS selected -- the stance every Phase 1 figure rests on."""
    frames = {"agg": pd.DataFrame({
        "k": pd.to_datetime([T0 + i * SEC for i in range(10)]).tz_localize("UTC"),
        "v": np.arange(10.0)})}
    decision = pd.Series([T0 + i * SEC for i in range(10)])
    sel = select_cells(frames, MODEL, decision, seconds={T0 + 5 * SEC})
    assert sel.rows_by_frame == {"agg": 1}


# --------------------------------------------------------------------------
# the per-frame report, R272 §1(c)(e)
# --------------------------------------------------------------------------

TWO = AvailabilityModel(aggregate_frames={"magg": "ts", "trades": "ts_event"},
                        decision_column="d")


def _two_frames(n=60):
    magg = pd.DataFrame({"ts": [T0 + i * SEC for i in range(n)],
                         "events": np.ones(n)})
    # trades only in the first three seconds, none at any sampled position
    trades = pd.DataFrame({
        "ts_event": pd.to_datetime([T0 + i * SEC for i in range(3)]).tz_localize("UTC"),
        "size": [1.0, 2.0, 3.0]})
    return {"magg": magg, "trades": trades}


def _two_build(raw):
    m = raw["magg"]
    return pd.DataFrame({"d": pd.to_datetime(m["ts"]).to_numpy(),
                         "x": m["events"].shift(1).rolling(5, min_periods=1).sum().to_numpy()})


def test_KNOWN_POSITIVE_a_frame_with_ZERO_cells_at_EVERY_position_gets_NO_REACH():
    frames = _two_frames()
    base = _two_build(frames)
    rr = measure_reach(frames, _two_build, TWO, base, "d", k=3)
    note = rr.note()
    assert "trades: 0 cells at 3 of 3 positions" in note, note
    assert "NO REACH IS CLAIMED FOR trades" in note, note
    assert "magg: cells at 3 of 3 positions" in note, note
    assert frames_never_corrupted(rr) == ("trades",)
    for s in rr.samples:
        assert s.cells_by_frame.get("trades", 0) == 0
        assert s.cells_by_frame.get("magg", 0) > 0
