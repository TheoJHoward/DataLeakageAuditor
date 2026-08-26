"""B7 — the fixture adapter, and the known-positive for its equality check.

TWO TIERS, and the split is deliberate. The fixture's builder takes ~25 s per
call and its inputs are hundreds of megabytes on one machine, so a suite that
ran it would not run anywhere else and would not be run here either. The tests
that need it are opt-in via `LEAKAUDIT_FIXTURE=1`; everything checkable without
it runs always.

**A skipped known-positive is not a known-positive.** The opt-in tests were run
and their results are recorded in the round report; the skip marker keeps them
runnable, it does not stand in for having run them.
"""
import os

import pandas as pd
import pytest

from leakaudit import fixture_adapter as fa

FIXTURE = os.environ.get("LEAKAUDIT_FIXTURE") == "1"
needs_fixture = pytest.mark.skipif(
    not FIXTURE, reason="set LEAKAUDIT_FIXTURE=1 to run against the acceptance fixture")


# --------------------------------------------------------------------------
# Always-on: the partition between what is probed and what is merely captured
# --------------------------------------------------------------------------

def _inputs(**frames):
    return fa.FixtureInputs(sym="zc", month="2025-01", frames=frames)


def test_raw_excludes_the_captured_but_unread_frame():
    """The raw MBO parquet is captured and must NOT reach the probe.

    Serving `magg` from memory means the builder never reads the raw frame, so
    perturbing its columns could not move the output. A probe would record
    `observed_silence` on every one of them -- silence caused by the adapter,
    presented as a fact about the pipeline.
    """
    inp = _inputs(snap=pd.DataFrame({"a": [1]}),
                  trades=pd.DataFrame({"b": [2]}),
                  magg=pd.DataFrame({"c": [3]}),
                  **{"other:zc_mbo_2025-01.parquet": pd.DataFrame({"d": [4]})})
    assert set(inp.raw) == {"snap", "trades", "magg"}
    assert inp.not_probed == ("other:zc_mbo_2025-01.parquet",)


def test_the_exclusion_is_visible_not_silent():
    """It is retained in `frames`, so the exclusion can be audited."""
    inp = _inputs(snap=pd.DataFrame({"a": [1]}),
                  **{"other:x.parquet": pd.DataFrame({"d": [4]})})
    assert "other:x.parquet" in inp.frames
    assert "other:x.parquet" not in inp.raw


def test_a_none_frame_is_not_offered_to_the_probe():
    """`load_mbo_aggregated` returns None when its input is absent. None is not
    a frame, and handing one to the probe would crash it rather than record a
    missing input."""
    inp = _inputs(snap=pd.DataFrame({"a": [1]}), magg=None)
    assert set(inp.raw) == {"snap"}


def test_side_must_be_one_of_the_two():
    """SC-7(d) makes one-side-at-a-time a hard sequencing rule, so a builder is
    bound to a single side and a typo must not silently pick one."""
    with pytest.raises(ValueError, match="corrected"):
        fa.builder_for(_inputs(snap=pd.DataFrame({"a": [1]})), side="both")


# --------------------------------------------------------------------------
# Opt-in: the equality instrument and its known-positive
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def captured():
    return fa.read_inputs("zc", "2025-01")


@needs_fixture
def test_adapter_output_equals_the_fixture_exactly(captured):
    ok, cols, detail = fa.assert_matches_fixture(captured, "corrected")
    assert ok, "adapter diverged from the fixture: %s %s" % (list(cols)[:8], detail)


@needs_fixture
def test_known_positive_perturbing_the_served_snapshots_FIRES(captured):
    """If the equality check cannot detect a corrupted adapter, it is not
    evidence that an uncorrupted one is faithful."""
    from leakaudit.determinism import frames_equal
    build = fa.builder_for(captured, "corrected")
    ref = fa.unadapted("zc", "2025-01", "corrected")
    bad = {k: v.copy(deep=True) for k, v in captured.raw.items()}
    bad["snap"]["bid_size_1"] = bad["snap"]["bid_size_1"] + 1
    ok, cols, _ = frames_equal(ref, build(bad))
    assert not ok, "a corrupted adapter compared EQUAL; the check detects nothing"
    assert cols


@needs_fixture
def test_known_positive_perturbing_trades_reaches_the_output(captured):
    """The trades frame reaches the output only through the `ts_floor` join.

    This is the fixture's own headline availability channel, and it is the
    reason `raw` is a dict rather than a single frame. If perturbing trades did
    NOT move the output, the adapter would be serving a frame the builder never
    joins -- and the cross-frame probe would be measuring nothing.
    """
    from leakaudit.determinism import frames_equal
    build = fa.builder_for(captured, "corrected")
    ref = fa.unadapted("zc", "2025-01", "corrected")
    bad = {k: v.copy(deep=True) for k, v in captured.raw.items()}
    bad["trades"]["size"] = bad["trades"]["size"] * 2
    ok, cols, _ = frames_equal(ref, build(bad))
    assert not ok, "perturbing trades moved nothing; the ts_floor join is not live"


@needs_fixture
def test_serving_does_not_let_one_run_alter_the_next(captured):
    """The builder assigns columns onto what it reads. If the adapter handed it
    the caller's frame, run N would mutate run N+1's input and the pipeline
    would look nondeterministic when it is not."""
    build = fa.builder_for(captured, "corrected")
    before = {k: v.copy(deep=True) for k, v in captured.raw.items()}
    build(captured.raw)
    for k, v in before.items():
        pd.testing.assert_frame_equal(captured.raw[k], v)
