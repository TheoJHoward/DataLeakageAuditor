"""L2a, the label probe: its pair, its pin, and its refusals.

THE PAIR IS THE REGISTRATION'S OWN SEPARATOR. `PREREG.md` §2.4: the corpus is
unadjudicable without a declared horizon, because §6.5 "contains a lagged label
that *is* realized (clean) and one that is *not yet* realized (leaking), and only
a declared horizon separates them." So the pair is one frame set, one builder,
one cohort selection, and ONE DECLARED SCALAR varying.

    horizon 60s   the lagged label the feature reads is not yet realized at the
                  decision instant  ->  finding
    horizon 0s    the same lagged label IS realized                ->  silence

HELD CONSTANT, named because R257 requires the specification to name it and not
only what is compared: the frame bytes, the builder, the row population, the
label column, the decision column, the probed cohorts, the perturbation seed, the
comparator branch, and the number of cohorts. The horizon is the only difference.

THE LEAKING HALF IS ASSERTED BEFORE THE CLEAN HALF IS BELIEVED, and the clean
half re-runs it rather than trusting a neighbouring test, because a silence whose
positive was never confirmed in the same breath establishes nothing.

IT DISCRIMINATES AGAINST BOTH NEIGHBOURS, which is what makes it more than a
wiring test:

    L3.1 on the same declared frames returns `observed_silence` -- it RUNS, over
    the frame carrying the leak, and affirmatively finds nothing. Pinned below,
    so that if it ever starts catching this the suite says so.

    `check_pairwise_label_correlation` is silent because the label is drawn
    i.i.d., so the lagged copy carries no pairwise resemblance. Asserted, with
    both statistics printed beside the threshold so the margin is visible -- a
    printed number is not a pin, and a pin without the number is not a margin.
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

from leakaudit.availability import AvailabilityModel, run_probe_a   # noqa: E402
from leakaudit.checks import check_pairwise_label_correlation       # noqa: E402
from leakaudit.label_probe import (                                 # noqa: E402
    DETECTOR_ID, LabelAvailability, LabelDeclarationError, RawLabel,
    resolve_label_declaration, run_probe_l2a)

T0 = pd.Timestamp("2026-01-01 00:00:00")
SEC = pd.Timedelta(seconds=1)
N = 90
HORIZON = pd.Timedelta(seconds=60)
MODEL = AvailabilityModel(aggregate_frames={"lab": "ts"}, decision_column="d")
RAW_LABEL = RawLabel(frame="lab", column="y")


def _frames():
    """ONE frame set. Built once per call from one seed, so the two halves of
    the pair are the same bytes and not two draws that happen to look alike --
    R257's row exists because a pair once varied its data as well as its
    subject."""
    ts = [T0 + i * SEC for i in range(N)]
    y = np.random.default_rng(11).standard_normal(N)
    return {"lab": pd.DataFrame({"ts": ts, "y": y})}


def _build(raw):
    """Output row i decides at `ts_i` and reads the PREVIOUS row's label.

    A lagged label, which is the case the registration says only a declared
    horizon can adjudicate: with a 60s horizon that value is not realized until
    59 seconds after the decision, and with a zero horizon it was realized a
    second before it.
    """
    lab = raw["lab"]
    y = lab["y"].to_numpy()
    lagged = np.concatenate(([np.nan], y[:-1]))
    return pd.DataFrame({"d": lab["ts"].to_numpy(), "x": lagged})


def _l2a(horizon):
    return run_probe_l2a(
        _frames(), _build, MODEL, side="pair",
        raw_label=RAW_LABEL,
        label_availability=LabelAvailability(base_column="ts", horizon=horizon),
        cohort_stride=7, max_cohorts=10, seed=5)


# --------------------------------------------------------------------------
# The pair
# --------------------------------------------------------------------------

def test_A_THE_LEAKING_HALF_a_60s_horizon_finds_the_unrealized_lagged_label():
    """Asserted first. Nothing below is believable until this fires."""
    res = _l2a(HORIZON)
    assert res.verdict() == "finding", res.verdict()
    assert res.findings, "no cohort carried a finding"
    assert res.detector == DETECTOR_ID
    # The band is empty by construction here: this row's mask IS the comparator,
    # so every perturbed cell is unavailable to every row the cohort speaks for.
    assert sum(c.moved_in_band for c in res.cohorts) == 0


def test_B_THE_CLEAN_HALF_a_zero_horizon_is_silent_and_the_leak_half_still_fires():
    """The negative, and it re-runs the positive rather than trusting it.

    One declared scalar differs between the two calls below. Everything else --
    frames, builder, cohorts, seed, comparator -- is the same.
    """
    leaking = _l2a(HORIZON)
    assert leaking.verdict() == "finding", (
        "the positive half must fire in this test too; a silence whose positive "
        "was confirmed only elsewhere is a silence nobody checked")
    clean = _l2a(pd.Timedelta(0))
    assert clean.verdict() == "observed_silence", clean.verdict()
    assert clean.findings == []
    # AND THE PROBE WAS LIVE ON THE CLEAN HALF. Without this the silence could
    # be a perturbation that never reached the builder, which is the difference
    # between `observed_silence` and `none`.
    assert clean.read_beyond > 0, (
        "no row moved anywhere on the clean half, so this silence is about the "
        "harness rather than about the pipeline")
    assert clean.n_cohorts == leaking.n_cohorts


def test_the_ROW_AT_THE_COHORTS_OWN_INSTANT_is_inside_the_cohort():
    """R262 §3(d). The tie row, lost to a unit and recovered.

    §2.6 makes a change at any row with `d(i) <= d` a valid finding, so the row
    deciding EXACTLY at the cohort's instant is inside it. L2a's window was
    first written as `d < f_sec + 1ns`, and on frames carrying microsecond
    resolution `np.datetime64(f_sec + 1ns)` truncates back to `f_sec` -- so the
    strict comparison dropped that row on every cohort. Asserted as row counts,
    because the defect was invisible in the verdict: the run still found the
    leak, on one row fewer per cohort than it should have.
    """
    res = _l2a(HORIZON)
    seconds = sorted(c.second for c in res.cohorts)
    for c in sorted(res.cohorts, key=lambda c: c.second):
        # Rows deciding at or before this cohort's instant, on a fixture with
        # one decision row per second starting at T0.
        want = int((c.second - T0) / SEC) + 1
        assert c.rows_in_second == want, (
            "cohort %s speaks for %d row(s) and counted %d; the row at its own "
            "instant is the one a strict comparison drops"
            % (c.second, want, c.rows_in_second))
    assert seconds[0] == T0


def test_the_FIRST_COHORT_is_silent_and_the_reason_is_the_builders_lag():
    """R262 §3(d): name the silent one. A stated reason beats a silent
    narrowing.

    Nine cohorts of ten carry a finding. The tenth is the FIRST, and it is not a
    detection failure: it speaks for exactly one row -- the one deciding at the
    start of the frame -- and that row's feature is the one-row-lagged label of a
    predecessor that does not exist, so it is NaN and cannot move whatever is
    done to the labels. The cohort probed 90 cells and the row it speaks for
    reads none of them.
    """
    res = _l2a(HORIZON)
    first = min(res.cohorts, key=lambda c: c.second)
    assert first.second == T0
    assert len(res.findings) == len(res.cohorts) - 1, (
        "exactly one cohort is expected to be silent here")
    assert not first.finding()
    assert first.rows_in_second == 1, "it speaks for one row"
    assert first.cells_perturbed > 0, (
        "and it is not a probe that did not happen -- cells WERE perturbed, so "
        "this cohort's quiet is about the row rather than about the harness")
    built = _build(_frames())
    assert pd.isna(built["x"].iloc[0]), (
        "the reason, stated as data: the first row's feature is NaN because a "
        "one-row lag has no predecessor at the head of the frame")


def test_the_pair_varies_ONLY_the_horizon_and_the_frames_are_one_object():
    """R257: the specification names what is held constant, and a test that
    asserts it is the only thing that keeps it true."""
    a, b = _frames(), _frames()
    assert a["lab"].equals(b["lab"]), (
        "the two halves must be the same bytes; a re-seeded draw would let the "
        "pair fire on the data instead of on the horizon")


# --------------------------------------------------------------------------
# The two neighbours it has to discriminate against
# --------------------------------------------------------------------------

def test_L31_RUNS_over_the_same_leak_and_returns_observed_silence():
    """THE PIN. R260 §8, R261 §4.

    `observed_silence`, not `none`: L3.1 probes the declared frame, perturbs the
    label column under the frame rule, and affirmatively finds nothing -- so the
    pair discriminates a probe from a probe rather than a probe from a
    non-probe. If a future change makes L3.1 catch this, this test fails, and
    that is information rather than a regression.
    """
    res = run_probe_a(_frames(), _build, MODEL, side="pin",
                      cohort_stride=7, max_cohorts=10)
    assert res.verdict() == "observed_silence", res.verdict()
    assert res.findings == []
    assert res.detector == "L3.1"
    # It really did probe: the frame is declared and cells were perturbed.
    assert res.unmodelled_frames == ()
    assert any("corrupted" in n for n in res.notes)


def test_the_correlation_check_is_SILENT_and_its_margin_is_printed():
    """Asserted, not printed -- and printed as well, so the margin is visible.

    A printed number is not a pin: with the seed fixed the fixture is
    deterministic, so the assertion is that the check reports nothing, and both
    statistics are put beside the threshold so a reader can see how far from
    firing it was rather than taking `no finding` on trust.
    """
    # THE QUESTION THE CHECK IS ASKED HAS TO BE THE ONE IT COULD ANSWER. It
    # screens each FEATURE against the declared LABEL, so the frame handed to it
    # carries both: the feature the builder produces and the label it lags.
    # Screening the feature against itself, or against a timestamp, would be a
    # test of nothing.
    lab = _frames()["lab"]["y"].to_numpy()
    lagged = np.concatenate(([np.nan], lab[:-1]))
    screen = pd.DataFrame({"x": lagged, "y": lab})
    res = check_pairwise_label_correlation(screen, label="y")
    assert not res.findings, (
        "the model-free screen fired on the pair, so the pair no longer "
        "discriminates against it: %r" % (res.findings,))
    assert res.population, "the check must have looked, or its silence is `none`"
    # The margin, measured on the same values.
    ok = ~np.isnan(lagged)
    pear = abs(np.corrcoef(lagged[ok], lab[ok])[0, 1])
    ranks = lambda v: pd.Series(v).rank().to_numpy()          # noqa: E731
    spear = abs(np.corrcoef(ranks(lagged[ok]), ranks(lab[ok]))[0, 1])
    print("correlation margin against a 0.999 screen: Pearson %.5f, "
          "Spearman %.5f" % (pear, spear))
    assert pear < 0.5 and spear < 0.5, (
        "the label is drawn i.i.d. so a one-row lag should carry almost no "
        "pairwise resemblance; measured %.5f / %.5f" % (pear, spear))


# --------------------------------------------------------------------------
# The refusals, each shown to fire. R246: a refusal is an absence claim until a
# positive reddens it.
# --------------------------------------------------------------------------

def test_NOTHING_declared_is_unsupported_on_a_none_and_never_a_pass():
    res = run_probe_l2a(_frames(), _build, MODEL, side="none")
    assert res.verdict().startswith("unsupported("), res.verdict()
    assert res.findings == []
    assert res.cohorts == [], "nothing was probed, so there are no cohorts"
    assert "raw_label" in res.unsupported and "label_availability" in res.unsupported
    assert any("NOT PROBED" in n for n in res.notes)


def test_HALF_declared_REFUSES_and_names_the_missing_element():
    with pytest.raises(LabelDeclarationError) as e:
        run_probe_l2a(_frames(), _build, MODEL, side="half",
                      raw_label=RAW_LABEL)
    msg = str(e.value)
    assert "declared in part" in msg
    assert "`label_availability`" in msg and "missing" in msg
    # The other half, so the refusal is not one-sided.
    with pytest.raises(LabelDeclarationError) as e2:
        run_probe_l2a(_frames(), _build, MODEL, side="half2",
                      label_availability=LabelAvailability("ts", HORIZON))
    assert "`raw_label`" in str(e2.value)


@pytest.mark.parametrize("bad,expect", [
    (LabelAvailability("", HORIZON), "base_column"),
    (LabelAvailability("ts", 60), "duration"),
    (LabelAvailability("ts", -SEC), "negative"),
    (LabelAvailability("ts", HORIZON, -SEC), "negative"),
])
def test_a_MALFORMED_declaration_REFUSES(bad, expect):
    with pytest.raises(LabelDeclarationError) as e:
        run_probe_l2a(_frames(), _build, MODEL, side="bad",
                      raw_label=RAW_LABEL, label_availability=bad)
    assert expect in str(e.value)


def test_a_raw_label_naming_an_absent_frame_or_column_REFUSES():
    with pytest.raises(LabelDeclarationError) as e:
        run_probe_l2a(_frames(), _build, MODEL, side="absent",
                      raw_label=RawLabel("nope", "y"),
                      label_availability=LabelAvailability("ts", HORIZON))
    assert "was not supplied" in str(e.value)
    with pytest.raises(LabelDeclarationError) as e2:
        run_probe_l2a(_frames(), _build, MODEL, side="absent2",
                      raw_label=RawLabel("lab", "nope"),
                      label_availability=LabelAvailability("ts", HORIZON))
    assert "has no column" in str(e2.value)


def test_the_NON_TEMPORAL_mode_REFUSES_with_its_registration_finding():
    """R261 §4 / R260 §7: refuse now, do not build. The reason is the finding,
    and the refusal carries it rather than saying `unavailable`."""
    with pytest.raises(LabelDeclarationError) as e:
        run_probe_l2a(_frames(), _build, MODEL, side="nt",
                      raw_label=RAW_LABEL,
                      label_availability=LabelAvailability("ts", HORIZON),
                      has_timestamp=False)
    msg = str(e.value)
    assert "NON-TEMPORAL" in msg and "NOT BUILT" in msg
    assert "cohort" in msg and "NEXT_REGISTRATION_REQUIREMENTS" in msg


def test_the_refusal_is_ONE_function_reachable_without_running_a_probe():
    """The shared consumption point, callable by every entry point rather than
    reimplemented at each. R238 §1: completeness that rests on a neighbouring
    line's position is not a property a refusal can have."""
    state, reason = resolve_label_declaration(None, None, where="a test")
    assert state == "unsupported" and "missing" in reason
    state2, reason2 = resolve_label_declaration(
        RAW_LABEL, LabelAvailability("ts", HORIZON), where="a test")
    assert state2 == "ok" and reason2 is None


def test_only_UNAVAILABLE_label_cells_are_perturbed_and_nothing_else_moves():
    """DESIGN.md §2.7's every-call assertion, exercised rather than trusted: if
    the probe perturbed an available label cell or any other column, the run
    raises rather than reporting a finding that could not be attributed."""
    res = _l2a(HORIZON)
    assert res.verdict() == "finding"
    # The assertion runs inside the probe on every cohort; reaching a finding
    # at all means it held on every one of them.
    assert res.n_cohorts > 1
