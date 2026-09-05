"""A silence is read in the frame its NAME supplies. R226 §2(d).

THE DEFECT THIS HOLDS CLOSED. `check_pairwise_label_correlation` tests near-exact
LINEAR duplication of single columns. Its name says something much broader, and a
user who sees it report nothing concludes their features contain no relabelled
copy of the target. That conclusion is false and the check's own output used to
support it.

    Measured (evidence/session/LABEL_SCREEN_CASES.md): `y**3` is a PERFECT
    monotone copy of a label -- invertible, rank order preserved, no information
    lost -- and it screens at |r| = 0.762. It passes at every threshold. The
    failure is the statistic, not the cutoff, which is why moving the threshold
    was the wrong question.

WHY THIS IS A TEST AND NOT A COMMENT. The qualification lives in the sentence a
user reads, and a sentence is deleted by anyone tidying output. The check that it
is still there is cheap and the thing it protects is the difference between a
narrow true statement and a broad false one.

THE THREE-STATE DISCIPLINE IS UNCHANGED. `none`, `observed_silence` and `finding`
still mean what they meant; this adds the SCOPE of an `observed_silence` where the
check's name overstates it. A silence in the wrong frame is a fourth failure the
vocabulary did not distinguish.
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

from leakaudit.checks import (                                   # noqa: E402
    CheckResult, check_pairwise_label_correlation, render, run_all)


def _frame(n=400):
    rng = np.random.default_rng(5)
    y = rng.standard_normal(n)
    return pd.DataFrame({"y": y, "a": rng.standard_normal(n),
                         "b": rng.standard_normal(n)})


def test_the_label_checks_SILENCE_names_what_it_is_a_silence_about():
    r = check_pairwise_label_correlation(_frame(), label="y")
    assert r.outcome == "observed_silence"
    text = r.explain()
    assert "THIS SILENCE IS ABOUT" in text, (
        "the check reported nothing found and did not say what the nothing is "
        "about:\n%s" % text)
    assert "PAIRWISE" in text and "NON-MONOTONE" in text, text
    assert "0.011" in text and "0.022" in text, (
        "the qualification does not carry the measured numbers that make it "
        "checkable, so a reader has to take it on trust:\n%s" % text)


def test_the_SILENCE_names_BOTH_screens_and_BOTH_thresholds():
    """R231 section 6: a frame naming one of two screens is the same defect one
    size smaller. The silence is produced by two cutoffs, so it names two."""
    text = check_pairwise_label_correlation(_frame(), label="y").explain()
    assert "Pearson" in text and "Spearman" in text, text
    assert text.count("0.999") >= 2, (
        "both screens run and the population line states fewer than two "
        "thresholds:\n%s" % text)


def test_a_MONOTONE_copy_is_now_CAUGHT_which_is_the_point_of_the_extension():
    """The discriminating positive that was already in hand when the decision
    was made: `y**3` is a perfect copy of the label, Pearson passes it at every
    threshold, Spearman catches it at 1.000."""
    f = _frame()
    f["cube"] = f["y"] ** 3
    r = check_pairwise_label_correlation(f, label="y")
    assert r.outcome == "finding", (
        "a perfect monotone copy of the label was not reported")
    detail = " ".join(str(x) for x in r.findings)
    assert "cube" in detail and "Spearman" in detail
    assert "Pearson" not in detail, (
        "Pearson is reported as firing on y**3, which it does not -- the "
        "finding must name the screen that actually fired: %s" % detail)


def test_a_NON_MONOTONE_copy_is_still_missed_and_the_silence_SAYS_SO():
    """The bound, asserted rather than described. `y**2` is a perfect copy and
    neither statistic sees it, so the silence must not read as coverage."""
    f = _frame()
    f["sq"] = f["y"] ** 2
    r = check_pairwise_label_correlation(f, label="y")
    assert r.outcome == "observed_silence", (
        "y**2 is now caught, so the stated bound is out of date")
    assert "NON-MONOTONE" in r.explain()


def test_the_scope_reaches_the_RENDERED_output_a_user_reads():
    """explain() is not the surface. `render` is what the CLI prints."""
    results = run_all(_frame(), label="y", train_idx=[0, 1], test_idx=[2, 3])
    text = render(results)
    assert "THIS SILENCE IS ABOUT" in text, (
        "the qualification exists on the result object and does not reach the "
        "printed output, which is the only surface a user has:\n%s" % text)


def test_a_FINDING_does_not_carry_the_scope_line():
    """The scope qualifies a SILENCE. A finding is a positive statement and
    needs no frame of this kind -- and appending it there would read as a hedge
    on a result that is not hedged."""
    f = _frame()
    f["copy"] = f["y"]
    r = check_pairwise_label_correlation(f, label="y")
    assert r.outcome == "finding"
    assert "THIS SILENCE IS ABOUT" not in r.explain()


def test_a_NOT_CHECKED_result_does_not_carry_it_either():
    r = check_pairwise_label_correlation(_frame())
    assert r.outcome == "none"
    assert "THIS SILENCE IS ABOUT" not in r.explain()
    assert "NOT CHECKED" in r.explain()


def test_a_check_whose_name_matches_its_test_carries_NO_scope_line():
    """The discriminating negative. If every check acquired one of these the
    field would be decoration rather than a statement about a specific
    overstatement -- so the checks whose names are accurate must not have it."""
    results = run_all(_frame(), label="y", train_idx=[0, 1], test_idx=[2, 3])
    named = {r.check: r for r in results}
    for name in ("split_validity", "duplicate_rows_across_split",
                 "constant_columns"):
        assert name in named, sorted(named)
        assert not named[name].silence_is_about, (
            "%r carries a silence-scope line and its name does not overstate "
            "its test. The field marks a specific known gap; spreading it "
            "makes it noise." % name)


def test_the_field_defaults_to_absent():
    r = CheckResult(check="x", registered_row="none", looked=True,
                    population="0 things")
    assert r.silence_is_about == ""
    assert "THIS SILENCE IS ABOUT" not in r.explain()
