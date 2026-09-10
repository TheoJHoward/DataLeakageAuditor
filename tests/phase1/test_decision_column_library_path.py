"""The LIBRARY entry point's own overlapping-clock positive. R237 §4.

**WHY THIS FILE HAD TO EXIST RATHER THAN BEING COVERED BY THE FILE-PATH ONE.**
R237 §4 sets the condition: one test covers both entry points only if they *join*
above the shared refusal. They do not. Measured from the call sites:

    file path     load_model  ->  require_decision_column(..., "the model file")
                                  refuses AT LOAD; `run_probe_a` is never reached
    library path  AvailabilityModel(...)  ->  run_probe_a
                                  ->  require_decision_column(..., "the probe")

Two independent call sites, and the file path terminates before the probe's. So
`test_decision_column_required.py`, which drives everything through `cli.main`,
is a **wiring test** for the library path — it would pass with the probe's call
site deleted. This file reaches the probe's call site directly.

**AND IT WAS NOT COVERED BY ACCIDENT EITHER.** An AST scan over `tests/` for
`AvailabilityModel(...)` constructions omitting `decision_column` returned
**zero** before this file: every existing construction declares the clock, so
nothing anywhere exercised the defaulted library path. R236's hole-1 measurement
was a one-off script, not a standing check.

**THE CLOCKS OVERLAP BY TWO SECONDS, and that is the whole design.** With the
wrong clock an hour away the probe's own `decision column ... is not in the built
output` guard, or the `frame matched NO corrupted second` guard, refuses for an
unrelated reason — so an hour-off positive passes *before* the fix and proves
nothing. Two seconds is both the realistic error (a load stamp beside an event
stamp) and the case where no existing machinery saves you.
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

from leakaudit.availability import (                                # noqa: E402
    NOT_SET, AvailabilityModel, ProbeError, require_decision_column, run_probe_a)
from leakaudit.identity_control import run_identity_control        # noqa: E402

SECS = pd.date_range("2026-04-01 08:00:00", periods=200, freq="1s")

#: DECLARED, BECAUSE THE FIGURES BELOW ARE ABOUT THE CLOCK AND NOT THE SCHEDULE.
#: R263 §2(b). These calls used to omit `cohort_stride` and take the parameter's
#: default of 97, which over 200 seconds picks three cohorts -- so the recorded
#: "3 findings" was a fact about a default nobody in this file had chosen. The
#: default is now a sentinel and an omitted stride is DERIVED from the model's
#: floor, which here is 2 and picks a hundred cohorts. Declaring 97 keeps every
#: figure in this file comparable with the rounds that recorded them, and makes
#: the schedule a stated input rather than an inherited one.
STRIDE = 97


@pytest.fixture
def frames():
    """`timestamp` is two seconds early. Same range, same resolution, same
    timezone — nothing about it looks wrong."""
    rng = np.random.default_rng(5)
    return {
        "agg": pd.DataFrame({"k": SECS, "v": rng.standard_normal(len(SECS))}),
        "dec": pd.DataFrame({
            "timestamp": SECS + pd.Timedelta(milliseconds=300)
            - pd.Timedelta(seconds=2),
            "decided_at": SECS + pd.Timedelta(milliseconds=300),
            "q": rng.standard_normal(len(SECS)),
        }),
    }


def build(f):
    o = f["dec"].copy()
    a = f["agg"].copy()
    a["sec"] = pd.to_datetime(a["k"]).dt.floor("1s")
    o["sec"] = pd.to_datetime(o["decided_at"]).dt.floor("1s")
    o["x"] = o["sec"].map(a.set_index("sec")["v"]).fillna(0.0)
    return o[["timestamp", "decided_at", "q", "x"]]


def _model(**kw):
    # `window` is a Timedelta on the model; the FILE key is `window_seconds` and
    # the loader converts. The two names are one more place the library and file
    # entry points differ, which is the theme of this file.
    return AvailabilityModel(aggregate_frames={"agg": "k"},
                             window=pd.Timedelta(seconds=1), **kw)


# ---------------------------------------------------------------------------
# the pair -- the refusal, and proof it is refusing something real
# ---------------------------------------------------------------------------
def test_the_TRUE_clock_finds_leaks_through_the_LIBRARY_path(frames):
    """The other half. Without this the refusal below could be refusing a frame
    set that has nothing to find, which is a refusal proving nothing.

    `verdict` IS A METHOD, and this test asserted `res.verdict == "finding"` on
    the first run -- comparing a bound method to a string, which is False for
    every input and cannot distinguish anything. It failed loudly here because
    the true clock has to FIND; the same mistake in the silence direction would
    have passed and asserted nothing.
    """
    res = run_probe_a(frames, build, _model(decision_column="decided_at"),
                      "test", cohort_stride=STRIDE)
    assert res.verdict() == "finding", res.notes
    assert sum(c.moved_in_second for c in res.cohorts) == 3


def test_an_UNDECLARED_clock_is_REFUSED_at_the_LIBRARY_entry_point(frames):
    """R236 §3's hole 1, as a standing check rather than a one-off script.

    Before the sentinel this returned `observed_silence` with 0 findings on the
    frames above — the tool's most confident state, on a real leak."""
    with pytest.raises(ProbeError) as e:
        run_probe_a(frames, build, _model(), "test", cohort_stride=STRIDE)
    msg = str(e.value)
    assert "no decision column is declared" in msg
    assert "observed_silence" in msg, (
        "the refusal does not say what the default actually did, so a library "
        "caller meets a rule rather than a reason: %s" % msg)
    assert "the availability probe" in msg, (
        "the refusal does not say WHERE it fired; the same words serve the file "
        "boundary and a caller has to be able to tell them apart")


def test_the_IDENTITY_CONTROL_refuses_too_it_is_the_SECOND_consumer(frames):
    """Two consumers read the clock and a fix at one is not a fix at the other —
    which is the lesson this whole defect keeps re-teaching."""
    with pytest.raises(ProbeError) as e:
        run_identity_control(frames, build, _model(), "test")
    assert "no decision column is declared" in str(e.value)
    assert "the identity control" in str(e.value)


# ---------------------------------------------------------------------------
# the discriminating property: the overlap defeats the downstream guards
# ---------------------------------------------------------------------------
def test_the_WRONG_clock_DECLARED_still_runs_and_that_is_the_point(frames):
    """THE POINT IS NOT THAT `timestamp` IS FORBIDDEN. A user may declare it and
    be wrong; this tool cannot check a declaration. What the sentinel removes is
    the silent pick, not the freedom to be mistaken.

    **AND THIS IS WHAT MAKES THE POSITIVE DISCRIMINATING.** The run completes —
    no guard fires — so before the sentinel the undeclared case reached exactly
    here and produced an answer. An hour-apart clock would have been stopped by
    an unrelated guard, and the test would have passed against the defect.
    """
    res = run_probe_a(frames, build, _model(decision_column="timestamp"), "test",
                      cohort_stride=STRIDE)
    # R262 §2 CHANGED WHAT THE WRONG CLOCK CLAIMS, AND NOT WHAT IT MISSES. This
    # asserted `observed_silence`, which is what made R236's defect so bad: the
    # wrong clock produced the tool's most confident state on a frame set whose
    # true clock finds three. The wrong clock puts every corrupted cell's
    # movement outside every bucket, so NOTHING moves anywhere, and there was
    # never a licence for that claim. The miss is identical; the report is not.
    assert res.verdict().startswith("none("), res.notes
    assert res.liveness == 0
    assert res.n_cohorts > 0, (
        "no cohort was built, so some guard refused for an unrelated reason and "
        "this construction is not discriminating after all")
    assert sum(c.moved_in_second for c in res.cohorts) == 0, (
        "the wrong clock moved rows, so the two clocks are not distinguishable "
        "on these frames and the pair proves nothing")


def test_THE_PAIR_IS_THE_MEASUREMENT_hole_one_at_the_library_level(frames):
    """R236 §3's hole 1, stated as the two-sided figure it actually is.

    Same frames, same builder, same model but for the clock. The wrong clock is
    the one the library used to pick SILENTLY, so before the sentinel the second
    row below was what a library caller got with no `decision_column` at all:
    a quiet answer on data whose true clock finds three.

    **THE QUIET ANSWER USED TO BE `observed_silence` AND IS NOW `none`.** R262
    §2. The wrong clock puts every corrupted cell's movement outside every
    bucket, so no row moves anywhere and nothing ever licensed the affirmative
    claim. Two things were wrong here and only one of them was the clock: the
    tool also had no way to say "my perturbation reached nothing." The figure
    the pair measures -- three findings against zero -- is unchanged.
    """
    def moved(clock):
        r = run_probe_a(frames, build, _model(decision_column=clock), "test",
                        cohort_stride=STRIDE)
        return r.verdict(), sum(c.moved_in_second for c in r.cohorts)

    assert moved("decided_at") == ("finding", 3)
    wrong_verdict, wrong_findings = moved("timestamp")
    assert wrong_verdict.startswith("none(")
    assert wrong_findings == 0


def test_a_clock_that_is_not_a_column_is_refused_by_the_PROBE_not_by_pandas(frames):
    """The near neighbour, kept apart from the one above. A declared name that
    is not in the built output is a different fact from a name nobody declared,
    and the loader cannot check it: it never sees the built output."""
    with pytest.raises(ProbeError) as e:
        run_probe_a(frames, build, _model(decision_column="nope"), "test")
    assert "is not in the built output" in str(e.value)


# ---------------------------------------------------------------------------
# the structural fact the file-path test cannot assert
# ---------------------------------------------------------------------------
def test_the_TWO_ENTRY_POINTS_DO_NOT_JOIN_above_the_refusal():
    """R237 §4's condition, asserted rather than argued.

    If these ever did join, one test would cover both and this file could
    retire. Asserted so that a refactor which merges them has to say so.

    **AND IT EARNED ITS KEEP IMMEDIATELY.** It was written at R237 asserting
    THREE call sites and failed at R238 when `cli.py` gained one -- `cli.py`
    being a consumer that read the clock directly and had been counted as two
    consumers rather than three for two rounds. A structural count is worth
    asserting precisely because the thing it counts moves without anyone
    noticing.
    """
    import ast

    src = (ROOT / "src" / "leakaudit").glob("*.py")
    sites = []
    for p in src:
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id == "require_decision_column":
                sites.append(p.name)
    assert sorted(sites) == ["availability.py", "cli.py", "identity_control.py",
                             "label_probe.py", "model_file.py"], (
        "the call sites of the shared refusal changed: %s. Five are expected -- "
        "FOUR consumers and one early message at the file boundary -- and the "
        "count is what makes 'they do not join' true." % sorted(sites))
    # R261 §4. `label_probe.py` is the fourth consumer, added with L2a. It reads
    # the same clock for the same reason -- every availability instant it
    # computes is compared against the output row's decision instant -- so it
    # takes the shared refusal rather than a fourth copy of the words. The count
    # moved and this assertion is what made that a decision instead of a drift.


def test_the_SENTINEL_is_not_a_column_name_anyone_would_write():
    assert " " in NOT_SET and NOT_SET != "timestamp"
    assert require_decision_column("decided_at", "x") == "decided_at", (
        "the refusal does not pass a declared clock through unchanged")


# ---------------------------------------------------------------------------
# R238 §1 -- the shared refusal refuses what the file boundary refused
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad", [None, "", 0, 3.5, ["decided_at"]])
def test_a_NON_COLUMN_clock_is_refused_BY_THE_REFUSAL_not_by_the_next_line(bad):
    """THE DISCRIMINATING FORM: the refusal is called with NOTHING adjacent.

    R238 §1 asked whether the downstream `ProbeError` catches these by DESIGN or
    by ORDERING, and named the test that separates them — move the consumption
    so the membership check is not next to it. Measured before the fix: with the
    neighbour removed, `None`, `''` and `0` reached pandas as `KeyError: None`,
    a detection arriving as somebody else's exception. **Ordering, not design.**

    Consolidating to one refusal had therefore made it refuse LESS than the file
    boundary it replaced — TB-22's shape, a guarantee at one layer read as a
    guarantee at another.
    """
    with pytest.raises(ProbeError) as e:
        require_decision_column(bad, "a consumer with no neighbour")
    assert "a column name was expected" in str(e.value)
    assert "a consumer with no neighbour" in str(e.value)


def test_the_UNSET_sentinel_and_a_NON_COLUMN_are_DIFFERENT_refusals():
    """Two questions, two messages. Merging them would tell a user who wrote
    `"decision_column": 0` that they declared nothing, which is not what they
    did."""
    with pytest.raises(ProbeError) as unset:
        require_decision_column(NOT_SET, "x")
    with pytest.raises(ProbeError) as junk:
        require_decision_column(0, "x")
    assert "no decision column is declared" in str(unset.value)
    assert "no decision column is declared" not in str(junk.value)
    assert "a column name was expected" in str(junk.value)


def test_the_LOADER_gets_the_SAME_WORDS_because_it_delegates():
    """Not a copy. The loader's own type check was the only place this
    predicate lived, which is how the shared refusal came to be weaker."""
    import json
    import tempfile

    from leakaudit.model_file import ModelFileError, load_model

    d = Path(tempfile.mkdtemp())
    p = d / "m.json"
    p.write_text(json.dumps({"version": 3, "aggregate_frames": {"a": "k"},
                             "decision_column": 0}), encoding="utf-8")
    with pytest.raises(ModelFileError) as e:
        load_model(str(p))
    assert "a column name was expected" in str(e.value)
    assert "REFUSED HERE RATHER THAN DOWNSTREAM" in str(e.value), (
        "the loader is not carrying the shared refusal's words, so it has its "
        "own copy again")


def test_a_DECLARED_clock_still_passes_through_unchanged():
    """The negative control. A refusal that refused everything would pass every
    test above and be useless."""
    assert require_decision_column("decided_at", "x") == "decided_at"


def test_the_isinstance_guard_means_a_weird_EQ_cannot_answer_for_NOT_SET():
    """`dcol == NOT_SET` alone asks an arbitrary object's `__eq__` a question
    about a string; an array-like answers with an array, which is not a truth
    value. Only a `str` can equal a `str`."""
    class AlwaysEqual:
        def __eq__(self, other):
            return True

    with pytest.raises(ProbeError) as e:
        require_decision_column(AlwaysEqual(), "x")
    assert "a column name was expected" in str(e.value), (
        "an object claiming equality with everything was read as the unset "
        "sentinel, so the sentinel test is answering to someone else's __eq__")

# ---------------------------------------------------------------------------
# the scope split, all four cells. R238 §1.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("body,outcome,why", [
    ({"version": 3, "label_column": "q"},
     "loads",
     "a checks-only file consumes no clock, so it is not asked for one"),
    ({"version": 3, "label_column": "q", "decision_column": "d"},
     "loads",
     "declaring one it will not use is the user's business"),
    ({"version": 3, "label_column": "q", "decision_column": 0},
     "a column name was expected",
     "MALFORMED IS MALFORMED REGARDLESS OF SCOPE -- the type check is ungated "
     "for exactly this cell, and it is the one the gating would have missed"),
    ({"version": 3, "aggregate_frames": {"a": "k"}},
     "no decision column is declared",
     "an availability model consumes the clock, so the unset test applies"),
])
def test_the_SCOPE_SPLIT_is_a_two_by_two_and_all_four_cells_hold(
        tmp_path, body, outcome, why):
    """**THE TWO CHECKS HAVE DIFFERENT SCOPES AND THAT IS DELIBERATE.**

    "Nobody declared a clock" matters only where a clock is consumed, so it is
    gated on the file declaring an availability model. "The clock was declared
    as the integer 0" is malformed anywhere, so it is not gated. Collapsing the
    two into one gate loses a cell whichever way it collapses: gate both and a
    malformed checks-only file loads; gate neither and `leakaudit check` starts
    demanding a clock it never reads.
    """
    import json

    from leakaudit.model_file import ModelFileError, load_model

    p = tmp_path / "m.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    if outcome == "loads":
        cfg = load_model(str(p))
        assert cfg is not None, why
    else:
        with pytest.raises(ModelFileError) as e:
            load_model(str(p))
        assert outcome in str(e.value), why
