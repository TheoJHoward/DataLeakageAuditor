"""Known positives for the identity control. R194 §2.

THE OBVIOUS POSITIVE IS THE EASY ONE. A write that changes values is caught by
any comparison at all, so passing it demonstrates almost nothing about the path
this control exists to test. The cases that matter are VALUE-PRESERVING and
change something else, and they come first here for that reason:

  1. a write that preserves every value and PROMOTES THE DTYPE -- the case that
     matters most, because promotion status keys the combination and decides the
     tier, so a silent promotion moves the tier every real finding is reported
     at;
  2. a write that preserves values and dtype and REPLACES THE INDEX;
  3. only then the value change, which any comparison catches;
  4. and the negative control -- a genuine identity write, which is silent, and
     which means nothing until 1 and 2 have fired.

The frames are synthetic and built here, outside the instrument's own domain, so
a firing is attributable to the injected fault and to nothing else.

TWO LIMBS, TESTED APART. Limb (a) is the registered criterion: did the OUTPUT
move. Limb (b) is input invariance, which is beyond the registered text. Case 2
is the reason they are kept apart: a builder that resets the index absorbs the
fault, limb (a) stays silent, and limb (b) is the only thing that sees it. A
suite that folded them together could not show that.

SC-5(f)'s sentinel route has its own cases at the end.
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

from leakaudit.availability import AvailabilityModel                # noqa: E402
from leakaudit.identity_control import (                            # noqa: E402
    SENTINEL_WRAP, identity_write_back, run_identity_control,
    sentinel_columns, sentinel_false_positives)

N_SECONDS, ROWS_PER_SECOND, SEED = 300, 3, 20260828
MODEL = AvailabilityModel(aggregate_frames={"agg": "ts_floor"},
                          decision_column="timestamp")


def _frames():
    rng = np.random.default_rng(SEED)
    secs = pd.date_range(pd.Timestamp("2026-01-01 00:00:00"),
                         periods=N_SECONDS, freq="1s")
    agg = pd.DataFrame({
        "ts_floor": secs,
        "agg_value": rng.standard_normal(N_SECONDS),
        "agg_count": rng.integers(1, 100, N_SECONDS).astype("int64")})
    stamps = [s + pd.Timedelta(milliseconds=200 + 250 * k)
              for s in secs for k in range(ROWS_PER_SECOND)]
    snap = pd.DataFrame({"timestamp": stamps,
                         "own": rng.standard_normal(len(stamps))})
    return {"snap": snap, "agg": agg}


def _build(raw):
    """Reads its own second's aggregate. Order-insensitive, index-insensitive --
    which is what makes case 2 land the way it does."""
    out = raw["snap"].copy()
    out["ts_floor"] = pd.to_datetime(out["timestamp"]).dt.floor("s")
    a = raw["agg"].set_index("ts_floor")
    out["feature"] = out["ts_floor"].map(a["agg_value"]).to_numpy()
    out["counted"] = out["ts_floor"].map(a["agg_count"]).to_numpy()
    return out[["timestamp", "own", "feature", "counted"]]


def _run(write_back=identity_write_back, stride=7):
    return run_identity_control(_frames(), _build, MODEL, side="synthetic",
                                cohort_stride=stride, max_cohorts=30,
                                write_back=write_back)


# ---------------------------------------------------------------------------
# The value-preserving positives, first
# ---------------------------------------------------------------------------

def _promoting_write(frame, column, mask):
    """Writes every value back unchanged and promotes the column to float64."""
    vals = frame.loc[mask, column].to_numpy()
    frame[column] = frame[column].astype("float64")
    frame.loc[mask, column] = vals.astype("float64")


def test_a_value_preserving_dtype_promotion_fires():
    """THE CASE THAT MATTERS MOST. Promotion status keys the combination and
    decides the tier, so a write-back that silently promotes changes the tier
    every real finding is reported at."""
    res = _run(_promoting_write)
    promoted = [c for c in res.input_checks
                if c.dtype_before != c.dtype_after]
    assert promoted, "a dtype promotion in the write-back was not detected"
    assert all(c.values_equal for c in promoted), (
        "this positive is only interesting if the VALUES were preserved")
    assert not res.input_invariant
    assert any("int64 -> float64" in c.why() for c in promoted)


def test_the_promotion_positive_also_moves_the_output_here():
    """On this builder the promoted column reaches the output, so the registered
    limb fires too. Asserted rather than assumed -- if it did not, the case would
    be resting on limb (b) alone and the docstring above would be wrong."""
    res = _run(_promoting_write)
    assert res.verdict() == "control_artifact"
    assert "counted" in res.moved_columns


def _index_replacing_write(frame, column, mask):
    """Every value and dtype preserved; the index replaced."""
    identity_write_back(frame, column, mask)
    frame.index = pd.RangeIndex(1000, 1000 + len(frame))


def test_a_value_preserving_index_replacement_fires_on_limb_b():
    res = _run(_index_replacing_write)
    changed = [c for c in res.input_checks if not c.index_equal]
    assert changed, "an index replacement in the write-back was not detected"
    assert all(c.values_equal and c.dtype_before == c.dtype_after
               for c in changed), "this positive must preserve values and dtype"
    assert not res.input_invariant


def test_and_the_builder_absorbs_it_so_limb_a_stays_silent():
    """THE REASON THE TWO LIMBS ARE KEPT APART. This builder maps by key and
    never reads the index, so the registered limb sees nothing. Limb (b) is the
    only instrument that sees this fault -- and limb (b) is beyond the registered
    text, which is why it is reported separately and never quoted as the
    criterion."""
    res = _run(_index_replacing_write)
    assert res.verdict() == "silent"
    assert res.moved_columns == ()
    assert not res.input_invariant


# ---------------------------------------------------------------------------
# The easy positive, and the negative control
# ---------------------------------------------------------------------------

def _value_changing_write(frame, column, mask):
    frame.loc[mask, column] = frame.loc[mask, column].to_numpy() + 1


def test_a_value_change_fires_on_both_limbs():
    res = _run(_value_changing_write)
    assert res.verdict() == "control_artifact"
    assert res.moved_columns
    assert not res.input_invariant


def test_the_genuine_identity_write_is_silent_on_both_limbs():
    """The negative control, and it means nothing until the three above fire."""
    res = _run()
    assert res.verdict() == "silent"
    assert res.moved_columns == ()
    assert res.input_invariant
    assert res.input_checks, "a control that checked no column proves nothing"


def test_the_identity_write_actually_touched_cells():
    """A control that selected nothing would be silent for the wrong reason."""
    res = _run()
    assert all(c.n_cells_written > 0 for c in res.input_checks)
    assert any("wrote" in n for n in res.notes)


def test_a_mask_that_matches_nothing_raises_rather_than_reporting_silence():
    raw = _frames()
    raw["agg"] = raw["agg"].assign(
        ts_floor=raw["agg"]["ts_floor"] + pd.Timedelta(days=3650))
    try:
        run_identity_control(raw, _build, MODEL, side="synthetic",
                             cohort_stride=7, max_cohorts=30)
    except Exception as exc:                                   # noqa: BLE001
        assert "matched NO selected second" in str(exc)
    else:
        raise AssertionError("a never-matched mask reported silence")


def test_a_shape_change_is_a_compatibility_failure_and_is_not_scoreable():
    """R195 §3, settled from the registration rather than chosen.

    Section 6.11's third control owns shape and index and says every comparison
    after a shape change is meaningless, INCLUDING ONE THAT LOOKS CLEAN, so the
    result is discarded. Section 6.11's head rules out the other reading: control
    failures are recorded per the coverage scheme and NEVER AS FINDINGS. And
    section 6.6 puts `compatibility` ahead of `control_artifact` in precedence.

    It is not a pass. Section 8.2 forbids displaying a not-run state as one, so
    `scoreable` is False and criterion 4 has no answer on this side.
    """
    def appending_write(frame, column, mask):
        """Writes the values back, then appends one row keyed a second past the
        end -- a key no decision row carries, so nothing about the mapping
        changes. Guarded so it appends once rather than once per column."""
        identity_write_back(frame, column, mask)
        if len(frame) == N_SECONDS:
            row = frame.iloc[-1].copy()
            row["ts_floor"] = row["ts_floor"] + pd.Timedelta(seconds=1)
            frame.loc[len(frame)] = row

    def dropping_build(raw):
        """Drops a row when the aggregate frame has grown. The baseline keeps
        its shape; the control run does not."""
        out = _build(raw)
        return out.iloc[:-1] if len(raw["agg"]) > N_SECONDS else out

    res = run_identity_control(_frames(), dropping_build, MODEL, side="synthetic",
                               cohort_stride=7, max_cohorts=30,
                               write_back=appending_write)
    assert res.verdict() == "could_not_run(compatibility)"
    assert res.scoreable is False
    assert res.output_identical is None, (
        "a void comparison must not be recorded as a clean one")
    assert res.moved_columns == ()
    assert any("meaningless" in n for n in res.notes)


def test_the_silent_result_is_scoreable_and_the_artifact_result_is_too():
    """Both criterion-4 answers are answers. Only the not-run states are not."""
    assert _run().scoreable is True
    assert _run(_value_changing_write).scoreable is True


def test_a_nondeterministic_builder_is_could_not_run_not_silent():
    state = {"n": 0}

    def wobbly(raw):
        state["n"] += 1
        out = _build(raw)
        out["own"] = out["own"] + state["n"]
        return out

    res = run_identity_control(_frames(), wobbly, MODEL, side="synthetic",
                               cohort_stride=7, max_cohorts=30)
    assert res.verdict() == "could_not_run(determinism)"
    assert res.determinism_ok is False


# ---------------------------------------------------------------------------
# SC-5(f) -- the declared sentinel route
# ---------------------------------------------------------------------------

def _sentinel_frame(with_sentinel: bool):
    v = [1.0, 2.0, 3.0]
    if with_sentinel:
        v = [float(SENTINEL_WRAP - 5), 2.0, 3.0]      # 2**32 - k for size k = 5
    return pd.DataFrame({"net_delta": v, "clean": [1.0, 2.0, 3.0]})


def test_the_declared_signature_is_detected():
    cols = sentinel_columns(_sentinel_frame(True))
    assert "net_delta" in cols and cols["net_delta"] == 1
    assert "clean" not in cols


def test_ordinary_values_do_not_match_the_signature():
    assert sentinel_columns(_sentinel_frame(False)) == {}


def test_a_firing_on_a_both_sided_sentinel_is_a_false_positive_under_the_control():
    a = sentinel_columns(_sentinel_frame(True))
    b = sentinel_columns(_sentinel_frame(True))
    assert sentinel_false_positives(["net_delta", "clean"], a, b) == ["net_delta"]


def test_a_one_sided_artefact_is_not_a_sentinel_and_is_not_excused():
    """Identical presence on EVERY side is what makes an artefact a sentinel: it
    cannot differentiate the sides. One that appears on one side only can, so it
    is not excused here."""
    a = sentinel_columns(_sentinel_frame(True))
    b = sentinel_columns(_sentinel_frame(False))
    assert sentinel_false_positives(["net_delta"], a, b) == []
