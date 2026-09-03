"""P4's checks: a positive and a NEGATIVE CONTROL for each. R203 §4.

THE NEGATIVE IS THE ONE THAT MATTERS. A check that fires on everything is as
broken as one that fires on nothing, and it looks stricter, so it is the failure
almost nobody tests for. Every check below has a case built to make it fire and
a case built to make it stay silent, differing in exactly the respect the check
is about.

AND EVERY CHECK HAS A THIRD CASE: the one where it did not look. "No duplicate
rows across the split" and "no split was declared, so duplicates across one were
not checked" are different sentences, and both are asserted here, because the
second is the one a user acts on wrongly.
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

from leakaudit.checks import (                                     # noqa: E402
    FINDING, NONE, OBSERVED_SILENCE, check_constant_columns,
    check_duplicate_rows_across_split, check_label_under_another_name,
    check_split_validity, render, run_all)


# ---------------------------------------------------------------------------
# L1.1 — the split itself
# ---------------------------------------------------------------------------

def test_split_validity_fires_on_an_overlapping_split():
    r = check_split_validity(train_idx=[0, 1, 2, 3], test_idx=[3, 4, 5])
    assert r.outcome == FINDING
    assert "in BOTH sets" in str(r.findings[0])
    assert "scored against itself" in str(r.findings[0])


def test_split_validity_fires_on_an_empty_side():
    r = check_split_validity(train_idx=[0, 1], test_idx=[])
    assert r.outcome == FINDING
    assert any("empty" in str(f) for f in r.findings)


def test_split_validity_is_silent_on_a_clean_split():
    """THE NEGATIVE CONTROL."""
    r = check_split_validity(train_idx=[0, 1, 2], test_idx=[3, 4])
    assert r.outcome == OBSERVED_SILENCE
    assert r.findings == ()
    assert "3 training and 2 test" in r.population


def test_split_validity_says_when_it_did_not_look():
    r = check_split_validity()
    assert r.outcome == NONE
    assert "no split was declared" in r.explain()
    assert "not a clean result" in r.explain()


def test_split_validity_carries_the_registrations_own_narrowness():
    r = check_split_validity(train_idx=[0], test_idx=[1])
    assert any("renamed validation set" in n for n in r.notes)


# ---------------------------------------------------------------------------
# L1.4a — duplicate rows across the split
# ---------------------------------------------------------------------------

def _frame_with_duplicate():
    return pd.DataFrame({"a": [1, 2, 3, 1, 9], "b": ["x", "y", "z", "x", "w"]})


def _frame_without_duplicate():
    return pd.DataFrame({"a": [1, 2, 3, 7, 9], "b": ["x", "y", "z", "v", "w"]})


def test_duplicate_rows_fires_when_a_test_row_equals_a_training_row():
    r = check_duplicate_rows_across_split(_frame_with_duplicate(),
                                          train_idx=[0, 1, 2], test_idx=[3, 4])
    assert r.outcome == FINDING
    assert "1 test row(s) are exactly equal" in str(r.findings[0])


def test_duplicate_rows_is_silent_when_no_row_repeats():
    """THE NEGATIVE CONTROL: the same shape of frame and split, one value
    changed. A check that fired here would be firing on the split, not on a
    duplicate."""
    r = check_duplicate_rows_across_split(_frame_without_duplicate(),
                                          train_idx=[0, 1, 2], test_idx=[3, 4])
    assert r.outcome == OBSERVED_SILENCE
    assert "2 test row(s) against 3 training row(s)" in r.population


def test_duplicate_rows_says_when_it_did_not_look():
    r = check_duplicate_rows_across_split(_frame_with_duplicate())
    assert r.outcome == NONE
    assert "no split was declared" in r.explain()
    assert "duplicates ACROSS one were not checked" in r.explain()


def test_duplicate_rows_does_not_claim_to_have_checked_within_the_frame():
    """The frame HAS a duplicate pair; without a split the check must not be
    read as having found nothing about it."""
    r = check_duplicate_rows_across_split(_frame_with_duplicate())
    assert r.outcome == NONE
    assert "a different question" in r.explain()


# ---------------------------------------------------------------------------
# Constant columns — not a registered row
# ---------------------------------------------------------------------------

def test_constant_columns_fires_on_a_single_valued_column():
    df = pd.DataFrame({"varies": [1, 2, 3], "constant": [7, 7, 7]})
    r = check_constant_columns(df)
    assert r.outcome == FINDING
    assert [f.subject for f in r.findings] == ["constant"]
    assert "carries no information" in str(r.findings[0])


def test_constant_columns_is_silent_when_every_column_varies():
    """THE NEGATIVE CONTROL."""
    r = check_constant_columns(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    assert r.outcome == OBSERVED_SILENCE


def test_an_all_null_column_counts_as_constant():
    r = check_constant_columns(pd.DataFrame({"a": [1, 2], "n": [None, None]}))
    assert [f.subject for f in r.findings] == ["n"]


def test_constant_columns_says_when_it_did_not_look():
    r = check_constant_columns(pd.DataFrame({"a": []}))
    assert r.outcome == NONE
    assert "no rows" in r.explain()


def test_constant_columns_declares_it_is_not_a_registered_row():
    assert check_constant_columns(
        pd.DataFrame({"a": [1, 2]})).registered_row == "not a registered row"


# ---------------------------------------------------------------------------
# The label under another name — L2b's neighbourhood
# ---------------------------------------------------------------------------

def test_label_under_another_name_fires_on_an_identical_column():
    df = pd.DataFrame({"y": [1, 0, 1, 0], "copy": [1, 0, 1, 0],
                       "other": [5, 2, 9, 1]})
    r = check_label_under_another_name(df, label="y")
    assert r.outcome == FINDING
    assert [f.subject for f in r.findings] == ["copy"]
    assert "identical to the label" in str(r.findings[0])


def test_label_under_another_name_fires_on_a_rescaled_copy():
    rng = np.random.default_rng(3)
    y = rng.standard_normal(50)
    df = pd.DataFrame({"y": y, "scaled": y * 3.0 + 1.0,
                       "noise": rng.standard_normal(50)})
    r = check_label_under_another_name(df, label="y")
    assert [f.subject for f in r.findings] == ["scaled"]


def test_label_under_another_name_is_silent_on_ordinary_features():
    """THE NEGATIVE CONTROL. These columns are correlated with the label the
    ordinary amount; a screen that fired here would fire on every dataset."""
    rng = np.random.default_rng(4)
    y = rng.standard_normal(200)
    df = pd.DataFrame({"y": y, "weak": y * 0.4 + rng.standard_normal(200),
                       "none": rng.standard_normal(200)})
    r = check_label_under_another_name(df, label="y")
    assert r.outcome == OBSERVED_SILENCE


def test_label_under_another_name_says_when_no_label_was_declared():
    df = pd.DataFrame({"a": [1, 2], "b": [1, 2]})
    r = check_label_under_another_name(df)
    assert r.outcome == NONE
    assert "no label column was declared" in r.explain()


def test_label_under_another_name_says_when_the_label_is_absent():
    r = check_label_under_another_name(pd.DataFrame({"a": [1, 2]}), label="y")
    assert r.outcome == NONE
    assert "is not in the built frame" in r.explain()


def test_it_reports_a_candidate_rather_than_a_verdict():
    df = pd.DataFrame({"y": [1, 0, 1, 0], "copy": [1, 0, 1, 0]})
    r = check_label_under_another_name(df, label="y")
    assert any("does not adjudicate" in n for n in r.notes)


# ---------------------------------------------------------------------------
# All of them together
# ---------------------------------------------------------------------------

def test_run_all_reports_which_checks_did_not_look():
    df = pd.DataFrame({"a": [1, 2, 3], "k": [1, 1, 1]})
    results = run_all(df)
    text = render(results)
    assert "1 of 4 check(s) ran" in text
    assert "did not look, and that is reported above rather than counted as clean" in text


def test_run_all_runs_everything_when_everything_is_declared():
    rng = np.random.default_rng(8)
    y = rng.standard_normal(40)
    df = pd.DataFrame({"y": y, "a": rng.standard_normal(40)})
    results = run_all(df, label="y", train_idx=list(range(30)),
                      test_idx=list(range(30, 40)))
    assert all(r.looked for r in results)
    assert "4 of 4 check(s) ran" in render(results)


def test_every_check_names_whether_it_is_a_registered_row():
    df = pd.DataFrame({"a": [1, 2, 3]})
    for r in run_all(df):
        assert r.registered_row, "%s names no row status" % r.check
