"""A silence is read in the frame its NAME supplies. R226 §2(d).

THE DEFECT THIS HOLDS CLOSED. `check_label_under_another_name` tests near-exact
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
    CheckResult, check_label_under_another_name, render, run_all)


def _frame(n=400):
    rng = np.random.default_rng(5)
    y = rng.standard_normal(n)
    return pd.DataFrame({"y": y, "a": rng.standard_normal(n),
                         "b": rng.standard_normal(n)})


def test_the_label_checks_SILENCE_names_what_it_is_a_silence_about():
    r = check_label_under_another_name(_frame(), label="y")
    assert r.outcome == "observed_silence"
    text = r.explain()
    assert "THIS SILENCE IS ABOUT" in text, (
        "the check reported nothing found and did not say what the nothing is "
        "about. Its name claims more than it tests:\n%s" % text)
    assert "LINEAR" in text and "column" in text
    assert "0.762" in text, (
        "the qualification does not carry the measured number that makes it "
        "checkable, so a reader has to take it on trust")


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
    r = check_label_under_another_name(f, label="y")
    assert r.outcome == "finding"
    assert "THIS SILENCE IS ABOUT" not in r.explain()


def test_a_NOT_CHECKED_result_does_not_carry_it_either():
    r = check_label_under_another_name(_frame())
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
