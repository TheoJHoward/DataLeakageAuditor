"""The slice rule: its refusals, and the edge leak it exists to stop masking.

`DESIGN.md` §5.3, built at R255.

THE KNOWN POSITIVE IS THE POINT OF THIS FILE AND IT IS AN EDGE POSITIVE. R255
§4. A leak the probe finds anywhere would only show the probe is wired; the
defect §5.3 names is specific -- slicing shifts window warmup, so a leak SITTING
AT THE HEAD OF THE SLICE is masked by the truncation itself. So the pair below
holds the probed cohorts FIXED and varies only how far back the data reaches:

    without padding  the head buckets have an incomplete rolling window, the
                     feature is NaN there, corrupting the second moves nothing,
                     and the probe reports silence over a real leak.
    with padding     the same seconds, the same builder, a full window -- and
                     the leak is found.

Both halves are measured. The masked half is asserted FIRST, because it is the
defect being closed and a pair whose negative half was never confirmed does not
establish that padding is what made the difference.

The leaking builder is the modal error `DESIGN.md` §9 names: a window that
silently includes the current bar. The bar at `floor(d)` is available at
`floor(d) + window`, which is after `d`, so a decision reading it is reading the
future.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from leakaudit.availability import (                               # noqa: E402
    NOT_DECLARED, AvailabilityModel, ProbeError, run_probe_a)
from leakaudit.slicing import (                                    # noqa: E402
    SliceError, context_note, model_padding_floor, plan_slice, split_seconds)

# The builder's lookback. Deliberately much larger than the model's `window`,
# because that gap IS the establish: the model founds one second and the
# builder needs sixty, and nothing on the model moves when this number changes.
LOOKBACK = 60
T0 = pd.Timestamp("2026-01-01 00:00:00")
SLICE_AT = T0 + pd.Timedelta(seconds=LOOKBACK)


def _frames(start: pd.Timestamp, stop: pd.Timestamp):
    """One aggregate row and one decision row per second over [start, stop).

    VALUES ARE KEYED TO ABSOLUTE TIME, NOT TO POSITION IN THE RANGE, and the
    difference is a defect this fixture carried at R255. Position-indexed
    values made `_frames(SLICE_AT, X)` a DIFFERENT SERIES from the tail of
    `_frames(T0, X)` rather than its suffix -- measured: 1.0, 2.0, 3.0 against
    10.0, 11.0, 12.0 at the same instants. The pair therefore varied the data
    extent AND the data, so "padding is the only difference" was not true of
    the frames even though it was true of the mechanism. R256 §2 requires the
    pair on ONE frame. Keying to absolute time makes every construction agree
    on its overlap, and `_truncate` below CUTS rather than rebuilds.
    """
    secs = pd.date_range(start, stop, freq="1s", inclusive="left")
    step = ((secs - T0) // pd.Timedelta(seconds=1)).astype("int64")
    agg = pd.DataFrame({"k": secs, "v": (step % 17 + 1).astype(float)})
    # Decision instants sit mid-second, so the bar at `floor(d)` completes at
    # `floor(d) + 1s`, which is strictly AFTER the decision. Under the
    # registered `a <= d` comparator that is unambiguously unavailable.
    dec = pd.DataFrame({"d": secs + pd.Timedelta(milliseconds=500),
                        "row": step})
    return {"agg": agg, "dec": dec}


def _full():
    """THE one frame both halves of the positive are measured on. R256 §2."""
    return _frames(T0, SLICE_AT + pd.Timedelta(seconds=30))


#: Flipped ONLY by `test_the_ONE_FRAME_check_REDDENS_when_the_frame_is_rebuilt`,
#: which restores it in a `finally`. It reproduces the R255 fixture -- rebuild
#: the truncated frame instead of cutting it -- so the check added at R256 can
#: be shown red mechanically rather than asserted to have been shown red once.
_REBUILD_INSTEAD = False


def _truncate(frames, at):
    """The SAME frame with everything before `at` cut away.

    This is what a user does today: they hand the auditor a slice of their
    data. Nothing is rebuilt, so the surviving rows are byte-for-byte the rows
    the padded run reads -- the only difference between the two halves of the
    pair is how far back the frame reaches.
    """
    agg, dec = frames["agg"], frames["dec"]
    out = {"agg": agg[agg["k"] >= at].reset_index(drop=True),
           "dec": dec[dec["d"] >= at].reset_index(drop=True)}
    if _REBUILD_INSTEAD:  # MUTANT M8: the R255 shape -- rebuild, do not cut
        o = out["agg"]
        out["agg"] = o.assign(v=[float(i % 17) + 1.0 for i in range(len(o))])
    return out


def _leaky_build(frames):
    """The modal error: a rolling window that includes the current bar.

    `min_periods=LOOKBACK` is not a flourish -- it is the masking mechanism.
    Where the history is short the feature is NaN, and a NaN does not move when
    the data behind it is corrupted, so the probe sees nothing. That is what a
    slice without padding manufactures at its own head.
    """
    agg = frames["agg"].sort_values("k").reset_index(drop=True)
    feat = agg["v"].rolling(LOOKBACK, min_periods=LOOKBACK).mean()
    lookup = pd.Series(feat.to_numpy(), index=agg["k"])
    out = frames["dec"].sort_values("d").reset_index(drop=True).copy()
    out["feat"] = out["d"].dt.floor("s").map(lookup)
    return out


MODEL = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d")


def _probe(frames, **kw):
    return run_probe_a(frames, _leaky_build, MODEL, side="test",
                       cohort_stride=1, max_cohorts=400, **kw)


# --------------------------------------------------------------------------
# R255 §4 -- the known positive, at the edge, both halves measured.
# --------------------------------------------------------------------------

def test_WITHOUT_padding_the_edge_leak_is_MASKED():
    """The defect being closed, and it is TODAY'S ACTUAL USER PATH. R256 §2.

    The truncated slice is audited as an ORDINARY FRAME -- no `slice_from`, no
    padding, nothing this feature added. That is exactly what a user does now
    when they hand the auditor a window of their data, and the silent mislead
    they get back is what D closes. The slice feature REFUSING is the fix; this
    plain-frame path masking is the defect, and it is still reachable, because
    a caller who truncates before calling is indistinguishable from one whose
    data starts late.
    """
    res = _probe(_truncate(_full(), SLICE_AT))
    probed = {c.second for c in res.cohorts}
    assert probed, "the run must actually probe, or the silence proves nothing"
    assert res.verdict() == "observed_silence", (
        "a plain-frame audit ran over the head of a truncated slice and found "
        "nothing -- this is the masking DESIGN.md section 5.3 describes, and if "
        "this assertion fails the pair below no longer isolates padding as the "
        "cause. Got %r with %d finding(s)."
        % (res.verdict(), len(res.findings)))


def test_WITH_padding_the_SAME_cohorts_find_the_leak():
    """The same frame uncut, the same builder, padding declared. Found."""
    res = _probe(_full(), slice_from=SLICE_AT,
                 padding=pd.Timedelta(seconds=LOOKBACK))
    assert res.findings, (
        "the leak at the head of the slice is present in the data and the "
        "padding makes the builder's window complete there, so the probe must "
        "find it. Got %r." % res.verdict())
    assert res.verdict() == "finding"


def test_the_pair_IS_ONE_FRAME_cut_two_ways():
    """R256 §2: same frame, same leak, edge-positioned.

    THE R255 VERSION OF THIS TEST DID NOT ESTABLISH WHAT IT CLAIMED. It built
    the two halves with separate `_frames` calls whose values were indexed by
    POSITION, so the truncated half was a different series -- 1.0, 2.0, 3.0
    where the padded half held 10.0, 11.0, 12.0 at the same instants. Two
    things varied and the test only checked one of them. This checks both: the
    surviving rows are identical, and the probed seconds are identical, so the
    only difference left between the halves is how far back the frame reaches.
    """
    full = _full()
    cut = _truncate(full, SLICE_AT)

    tail = full["agg"][full["agg"]["k"] >= SLICE_AT].reset_index(drop=True)
    assert cut["agg"]["v"].tolist() == tail["v"].tolist(), (
        "the cut frame must be a SUFFIX of the full one, not a rebuild")
    assert cut["agg"]["k"].tolist() == tail["k"].tolist()

    bare = _probe(cut)
    padded = _probe(full, slice_from=SLICE_AT,
                    padding=pd.Timedelta(seconds=LOOKBACK))
    assert {c.second for c in bare.cohorts} == {c.second for c in padded.cohorts}
    # And the halves genuinely disagree, or the pair shows nothing.
    assert bare.verdict() == "observed_silence"
    assert padded.verdict() == "finding"


def test_the_ONE_FRAME_check_REDDENS_when_the_frame_is_rebuilt():
    """The mutation is run by the suite, not asserted in a report. TB-11/F6.

    R255 shipped the rebuild-instead-of-cut shape by accident and its
    same-cohorts test stayed green, because that test compared probed seconds
    and never compared the DATA. Flipping `_REBUILD_INSTEAD` reproduces exactly
    that fixture, and the check added at R256 has to go red on it -- otherwise
    the check is a restatement of the bug it was written against.
    """
    import test_slicing as me
    me._REBUILD_INSTEAD = True
    try:
        with pytest.raises(AssertionError, match="SUFFIX"):
            test_the_pair_IS_ONE_FRAME_cut_two_ways()
    finally:
        me._REBUILD_INSTEAD = False
    # and the restore worked, or every test after this one is running mutated
    assert not me._REBUILD_INSTEAD
    test_the_pair_IS_ONE_FRAME_cut_two_ways()


def test_an_INTERIOR_leak_is_the_wiring_test_not_the_defect():
    """Found with no slice at all, deep in the data. R255 §4's control.

    This is what a probe finds when nothing is truncated. It shows the detector
    works; it says nothing about the edge, which is why it is not the positive.
    """
    res = _probe(_frames(T0, T0 + pd.Timedelta(seconds=300)))
    assert res.findings, "the interior leak must be found with no slice"


# --------------------------------------------------------------------------
# R255 §2 -- the refusal is a refusal.
# --------------------------------------------------------------------------

def test_slice_without_declared_padding_REFUSES():
    frames = _frames(T0, SLICE_AT + pd.Timedelta(seconds=30))
    with pytest.raises(SliceError) as e:
        _probe(frames, slice_from=SLICE_AT)
    assert "no padding was declared" in str(e.value)


def test_the_refusal_returns_NO_verdict_at_all():
    """R255 §2: refuses, does not warn-and-audit.

    A warn-and-continue would return a `ProbeAResult` whose `verdict()` reads
    `observed_silence` over the very cohorts the truncation masked -- the
    defect, published as a clean bill. Nothing is returned instead.
    """
    frames = _frames(T0, SLICE_AT + pd.Timedelta(seconds=30))
    out = "no result"
    try:
        out = _probe(frames, slice_from=SLICE_AT)
    except SliceError:
        pass
    assert out == "no result"


def test_the_MODEL_ALONE_never_suffices_so_padding_is_ALWAYS_required():
    """R256 §1's second case is unreachable here, and that is pinned.

    The rule offers three cases: both supply a window, only the model does, only
    the user does. The middle one does not exist in this design -- the model
    determines a FLOOR and never the requirement -- so there is no slice on
    which the tool's own number suffices and the caller may stay silent. Left
    as an unwritten branch it would be assumed into existence by the next
    reader; asserted here, a change that makes the model authoritative fails
    this test and has to say so out loud.
    """
    for window in ("1s", "10min", "24h"):
        model = AvailabilityModel(aggregate_frames={"agg": "k"},
                                  decision_column="d",
                                  window=pd.Timedelta(window))
        with pytest.raises(SliceError) as e:
            plan_slice(raw=_full(), model=model, slice_from=SLICE_AT)
        assert "no padding was declared" in str(e.value), (
            "however large the model's own window, it never stands in for the "
            "declaration (window=%s)" % window)


def test_padding_below_the_model_founded_floor_REFUSES():
    model = AvailabilityModel(aggregate_frames={"agg": "k"}, decision_column="d",
                              window=pd.Timedelta("10min"))
    with pytest.raises(SliceError) as e:
        plan_slice(raw=_frames(T0, SLICE_AT), model=model, slice_from=SLICE_AT,
                   padding=pd.Timedelta("1min"))
    msg = str(e.value)
    # R256 §1: the conflict is refused, BOTH numbers are named, and the smaller
    # is not adopted merely because a user typed it.
    assert "IS NOT USED BECAUSE IT WAS DECLARED" in msg
    assert "0 days 00:01:00" in msg, "the declared number is quoted back"
    assert "0 days 00:10:00" in msg, "the model's number is quoted too"
    assert "AvailabilityModel.window" in msg, "the report names the driver"


def test_declared_padding_ABSENT_FROM_THE_DATA_refuses():
    """Declaring the padding is not supplying it. DESIGN.md section 5.3."""
    short = _frames(SLICE_AT - pd.Timedelta(seconds=5), SLICE_AT + pd.Timedelta(seconds=10))
    with pytest.raises(SliceError) as e:
        plan_slice(raw=short, model=MODEL, slice_from=SLICE_AT,
                   padding=pd.Timedelta(seconds=LOOKBACK))
    assert "do not reach back that far" in str(e.value)
    assert "agg starts" in str(e.value), "the report names the short frame"


def test_padding_declared_without_a_slice_refuses():
    with pytest.raises(ProbeError) as e:
        _probe(_frames(T0, T0 + pd.Timedelta(seconds=90)),
               padding=pd.Timedelta(seconds=LOOKBACK))
    assert "without `slice_from=`" in str(e.value)


def test_negative_and_unparseable_padding_refuse():
    frames = _frames(T0, SLICE_AT + pd.Timedelta(seconds=10))
    with pytest.raises(SliceError):
        plan_slice(raw=frames, model=MODEL, slice_from=SLICE_AT,
                   padding=pd.Timedelta(seconds=-1))
    with pytest.raises(SliceError):
        plan_slice(raw=frames, model=MODEL, slice_from=SLICE_AT,
                   padding="not a duration")
    with pytest.raises(SliceError):
        plan_slice(raw=frames, model=MODEL, slice_from=SLICE_AT, padding=None)


# --------------------------------------------------------------------------
# R255 §3 -- padding rows are context, never reported as audited-clean.
# --------------------------------------------------------------------------

def test_padding_seconds_are_NOT_in_cohorts():
    """`cohorts` is the probed-subject list and `verdict()` reads it."""
    res = _probe(_frames(T0, SLICE_AT + pd.Timedelta(seconds=30)),
                 slice_from=SLICE_AT, padding=pd.Timedelta(seconds=LOOKBACK))
    assert res.context_seconds, "the padding seconds must be carried, not dropped"
    assert all(c.second >= SLICE_AT for c in res.cohorts)
    assert all(s < SLICE_AT for s in res.context_seconds)
    assert not (set(res.context_seconds) & {c.second for c in res.cohorts})


def test_padding_seconds_outcome_is_not_applicable_never_silence():
    res = _probe(_frames(T0, SLICE_AT + pd.Timedelta(seconds=30)),
                 slice_from=SLICE_AT, padding=pd.Timedelta(seconds=LOOKBACK))
    assert res.context_outcome() == "not_applicable"
    assert res.context_outcome() != "observed_silence"


def test_the_printed_note_refuses_to_call_the_padding_clean():
    res = _probe(_frames(T0, SLICE_AT + pd.Timedelta(seconds=30)),
                 slice_from=SLICE_AT, padding=pd.Timedelta(seconds=LOOKBACK))
    note = "\n".join(res.notes)
    assert "NOT PROBED" in note
    assert "not_applicable" in note
    assert "PREREG.md section 8.2" in note, "the vocabulary names its document"
    assert "not clean" in note
    # R256 §1, third case: the padding is the USER's number and the run says so,
    # because a reader who cannot tell a declared number from a computed one
    # will read the declared one as corroborated.
    assert "DECLARED AND UNVERIFIABLE" in note
    assert "YOUR number, not this tool's" in note
    assert "clearing a floor is not corroboration" in note


def test_the_padding_is_present_claim_CARRIES_ITS_POPULATION():
    """A frame the check could not read is named, not silently dropped.

    "No modelled frame reaches back less far than declared" is an absence
    claim, and an absence claim carries its population. A frame the model
    declares and the caller did not supply is a frame this check said nothing
    about; swallowing it would make the claim quietly narrower than it reads.
    """
    model = AvailabilityModel(
        aggregate_frames={"agg": "k", "missing": "k", "nokey": "nope"},
        decision_column="d")
    raw = _frames(T0, SLICE_AT + pd.Timedelta(seconds=10))
    raw["nokey"] = pd.DataFrame({"other": [1, 2, 3]})
    plan = plan_slice(raw=raw, model=model, slice_from=SLICE_AT,
                      padding=pd.Timedelta(seconds=LOOKBACK))
    assert set(plan.unchecked_frames) == {"missing", "nokey"}
    assert "not supplied" in plan.unchecked_frames["missing"]
    assert "key column" in plan.unchecked_frames["nokey"]
    assert set(plan.frame_starts) == {"agg"}, "only the readable frame is a check"
    # And the run says so where a reader will see it.
    note = context_note(plan, 60)
    assert "DID NOT COVER 2 modelled frame(s)" in note
    assert "missing" in note and "nokey" in note


def test_the_population_line_is_ABSENT_when_every_frame_was_checked():
    """A standing caveat that always prints is a caveat nobody reads."""
    plan = plan_slice(raw=_frames(T0, SLICE_AT + pd.Timedelta(seconds=10)),
                      model=MODEL, slice_from=SLICE_AT,
                      padding=pd.Timedelta(seconds=LOOKBACK))
    assert plan.unchecked_frames == {}
    assert "DID NOT COVER" not in context_note(plan, 60)


def test_split_seconds_partitions_and_the_two_are_disjoint():
    plan = plan_slice(raw=_frames(T0, SLICE_AT + pd.Timedelta(seconds=10)),
                      model=MODEL, slice_from=SLICE_AT,
                      padding=pd.Timedelta(seconds=LOOKBACK))
    secs = list(pd.date_range(T0, SLICE_AT + pd.Timedelta(seconds=10), freq="1s"))
    probed, context = split_seconds(secs, plan)
    assert set(probed) | set(context) == set(secs), "jointly covering"
    assert not (set(probed) & set(context)), "disjoint"


# --------------------------------------------------------------------------
# R255 §1 -- the floor is founded, and is not sufficiency.
# --------------------------------------------------------------------------

def test_the_floor_is_the_max_over_the_FOUNDED_terms_and_names_its_driver():
    m = AvailabilityModel(aggregate_frames={"a": "k"}, decision_column="d",
                          window=pd.Timedelta("10min"))
    assert model_padding_floor(m)[0] == pd.Timedelta("10min")
    assert "window" in model_padding_floor(m)[1]
    # A larger DECLARED bar_duration takes over, and is named.
    floor, driver = model_padding_floor(m, pd.Timedelta("1h"))
    assert floor == pd.Timedelta("1h")
    assert "bar_duration" in driver
    # A smaller one does not.
    assert model_padding_floor(m, pd.Timedelta("1min"))[0] == pd.Timedelta("10min")


def test_an_INFERRED_bar_duration_contributes_NOTHING_to_the_floor():
    """R255 §1: only declared terms are founded.

    `bar_duration=None` is the inferred route, which produces a PER-ROW series
    with no single value -- `modes.py` declines to name one when the gaps
    disagree. A floor built from it would be a scalar standing for a set that
    has no centre.
    """
    m = AvailabilityModel(aggregate_frames={"a": "k"}, decision_column="d")
    assert model_padding_floor(m, None) == model_padding_floor(m)


def test_THE_RESIDUAL_HOLE_a_padding_that_clears_the_floor_can_still_mask():
    """The limit of the refusal, pinned as behaviour rather than left as prose.

    Measured at R255: two seconds of padding CLEARS the model-founded floor of
    one second and the data check, and the run is still completely masked --
    thirty cohorts, zero findings, over seconds M1 measured as carrying thirty
    real ones. Nothing here is a bug: the builder's lookback is sixty seconds
    and no field on the availability model moves when it changes, so the tool
    has nothing to compare against. This is §1's establish stated as a run.

    It is a test so that a later reader who assumes the refusal covers this
    finds it contradicted by the suite. If a future change DOES close it, this
    test fails and that is correct -- it should be rewritten then, deliberately.
    """
    fr = _truncate(_full(), SLICE_AT - pd.Timedelta(seconds=2))
    res = _probe(fr, slice_from=SLICE_AT, padding=pd.Timedelta(seconds=2))
    assert res.cohorts, "the probe must reach the seconds it then says nothing about"
    assert res.verdict() == "observed_silence", (
        "if this now finds the leak, the tool has gained a check it did not "
        "have at R255 and this test needs rewriting, not deleting")
    assert res.findings == []
    # And the run says so where a reader will see it: the number was theirs.
    note = "\n".join(res.notes)
    assert "DECLARED AND UNVERIFIABLE" in note
    assert "clearing a floor is not corroboration" in note


def test_clearing_the_floor_is_recorded_as_NOT_sufficiency():
    plan = plan_slice(raw=_frames(T0, SLICE_AT + pd.Timedelta(seconds=10)),
                      model=MODEL, slice_from=SLICE_AT,
                      padding=pd.Timedelta(seconds=LOOKBACK))
    assert "does NOT establish" in plan.floor_is_not_sufficiency
    # And the founded floor really is far below what this builder needs, which
    # is the establish stated as a number rather than as prose.
    assert plan.floor == pd.Timedelta(seconds=1)
    assert plan.padding == pd.Timedelta(seconds=LOOKBACK)
    assert plan.floor < plan.padding


# --------------------------------------------------------------------------
# R255 §5 -- the entry points, and that each one is covered.
# --------------------------------------------------------------------------

def test_the_LIBRARY_entry_carries_the_refusal():
    """`leakaudit.run_probe_a`, exported by `__init__.py`."""
    import leakaudit
    assert leakaudit.run_probe_a is run_probe_a
    with pytest.raises(SliceError):
        leakaudit.run_probe_a(_frames(T0, SLICE_AT + pd.Timedelta(seconds=10)),
                              _leaky_build, MODEL, side="t", slice_from=SLICE_AT)


def test_the_CLI_availability_path_JOINS_the_library_entry():
    """The CLI does not carry a second copy of the rule -- it calls this one.

    Substring ABSENCE is the sound direction (R241 §3): if `cli.py` contains no
    slice threshold of its own, it cannot have one that drifts from
    `slicing.py`'s. The check is that the CLI never constructs a padding
    comparison, only forwards the arguments.
    """
    src = (ROOT / "src" / "leakaudit" / "cli.py").read_text(encoding="utf-8")
    assert "slice_from=slice_from" in src, "the CLI forwards the slice"
    assert "padding=NOT_DECLARED if padding is None else padding" in src
    assert "model_padding_floor" not in src, (
        "the CLI must not compute a floor of its own")
    assert "plan_slice" not in src, "the CLI must not plan a slice of its own"


def test_the_CLI_second_cohort_selection_is_SLICED_TOO():
    """cli.py picks cohorts a second time for eligibility. R255 §5."""
    src = (ROOT / "src" / "leakaudit" / "cli.py").read_text(encoding="utf-8")
    assert "if result.slice_plan is not None:" in src, (
        "the eligibility table's cohort list must be filtered by the plan, or "
        "padding seconds are listed as probe subjects")


def test_the_MODEL_FREE_path_refuses_the_flags_rather_than_ignoring_them():
    """`leakaudit run` with no --model reaches no availability probe."""
    out = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path[:0]=[%r,%r]; "
         "from leakaudit.cli import main; sys.exit(main())"
         % (str(ROOT), str(ROOT / "src")),
         "run", "--pipeline", "x:y", "--frame", "a=b.csv",
         "--slice-from", "2026-01-01"],
        capture_output=True, text=True)
    assert out.returncode != 0
    assert "--slice-from needs --model" in out.stderr


def test_every_entry_reaching_the_probe_is_ENUMERATED_here():
    """The enumeration is a claim about the tree, so it is checked against it.

    An entry point added later that calls `run_probe_a` without appearing in
    this list makes the §5 claim stale, and a stale enumeration is the shape
    this session kept finding: an absence claim with no population.
    """
    import re
    found = set()
    for path in (ROOT / "src" / "leakaudit").rglob("*.py"):
        if path.name == "availability.py":
            continue
        text = path.read_text(encoding="utf-8")
        # Calls, not mentions: `run_probe_a(` with something before the paren
        # that is not `def`. Prose naming it in a docstring is not an entry.
        for line in text.splitlines():
            if re.search(r"run_probe_a\s*\(", line) and "`" not in line:
                found.add(path.relative_to(ROOT).as_posix())
    # EQUALITY, NOT SUBSET, AND THE DIFFERENCE IS THE WHOLE VALUE. Written as
    # `found <= known` this passed on the EMPTY SET -- a regex that stopped
    # matching, a moved package, a renamed function would all have produced a
    # green totality claim over nothing. Measured before it was tightened:
    # `found` is exactly one file. `__init__.py` re-EXPORTS `run_probe_a` and
    # never calls it, so it is not a call site; that the export resolves to
    # this function is pinned by `test_the_LIBRARY_entry_carries_the_refusal`.
    assert found == {"src/leakaudit/cli.py"}, (
        "the set of files CALLING run_probe_a changed: %s" % sorted(found))
