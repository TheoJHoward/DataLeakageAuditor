"""Checks that need no availability model. R203 P4.

WHY THESE FIRST. They cost a stranger nothing: no decision times, no
declaration of when a value became knowable. Someone who will never write an
availability model still gets something on the day they install the package.

EVERY CHECK SAYS WHETHER IT LOOKED. "No duplicate rows across the split" and
"no split was declared, so duplicates across one were not checked" are different
sentences, and the second is the one that matters. The registered vocabulary
already distinguishes them and this module uses it:

    finding            something was found
    observed_silence   the check ran over a stated population and found nothing
    none               the check did not run -- there is nothing to have found

A clean result that cannot say which of the last two it is, is the failure this
package refuses everywhere else.

WHICH OF THESE ARE ROWS OF THE REGISTERED TABLE, STATED ACCURATELY. PREREG.md
§4 enumerates eleven detector rows and closes. Of what is built here:

    split_validity            L1.1  -- "Missing or overlapping declared
                                       evaluation split... Indices disjoint and
                                       non-empty"
    duplicate_rows_across_split
                              L1.4a -- "Exact duplicate rows across split"
    label_under_another_name  L2b's NEIGHBOURHOOD -- a single-feature screen
                                       against the label. L2b is a REVIEW row
                                       with `domain_judgment` basis and its
                                       adjudication is deferred to a module that
                                       does not exist, so this is not that row;
                                       it is a check of the same shape.
    constant_columns          NOT A ROW OF THE TABLE. An ordinary data-quality
                                       check, useful and unregistered.

A fifth was specified and is NOT BUILT -- "the target survives a shuffle". Its
known positive did not fire, so it was removed rather than have its test
weakened. The reasoning is recorded below, where it was written.

That accounting is here rather than in a commit message because the distinction
gets blurred by repetition. **A built detector row is not a satisfied criterion,
and a check that is not a row is not coverage of anything.**
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

FINDING = "finding"
OBSERVED_SILENCE = "observed_silence"
NONE = "none"


@dataclass(frozen=True)
class CheckFinding:
    subject: str
    detail: str

    def __str__(self) -> str:
        return "%s: %s" % (self.subject, self.detail)


@dataclass
class CheckResult:
    """One check's answer, including whether it looked at all."""
    check: str
    registered_row: str
    looked: bool
    population: str = ""
    did_not_look_because: str = ""
    findings: tuple = ()
    notes: list = field(default_factory=list)

    @property
    def outcome(self) -> str:
        if not self.looked:
            return NONE
        return FINDING if self.findings else OBSERVED_SILENCE

    def explain(self) -> str:
        """THE TWO SENTENCES. Found-nothing and did-not-look are never the same."""
        if not self.looked:
            return ("%s: NOT CHECKED -- %s. This is not a clean result; it is "
                    "the absence of one." % (self.check, self.did_not_look_because))
        if self.findings:
            return "%s: %d finding(s) over %s.\n%s" % (
                self.check, len(self.findings), self.population,
                "\n".join("  - %s" % f for f in self.findings))
        return "%s: nothing found over %s. The check ran." % (
            self.check, self.population)

    def __str__(self) -> str:
        return self.explain()


def _numeric(frame: pd.DataFrame) -> list[str]:
    return [c for c in frame.columns
            if pd.api.types.is_numeric_dtype(frame[c])
            and not pd.api.types.is_bool_dtype(frame[c])]


# ---------------------------------------------------------------------------
# L1.1 -- the split itself
# ---------------------------------------------------------------------------

def check_split_validity(train_idx=None, test_idx=None) -> CheckResult:
    """PREREG.md §4's L1.1: indices disjoint and non-empty.

    The narrowness is the registration's own and is worth carrying: two disjoint
    non-empty index sets do NOT establish that a test set was held out, was not
    reused for model selection, and is not a renamed validation set.
    """
    r = CheckResult(check="split_validity", registered_row="L1.1", looked=False)
    if train_idx is None or test_idx is None:
        r.did_not_look_because = (
            "no split was declared, so nothing was checked about one. Declare "
            "`split` in the model file to check it")
        return r
    train, test = list(train_idx), list(test_idx)
    r.looked = True
    r.population = "%d training and %d test row position(s)" % (len(train), len(test))
    found = []
    if not train:
        found.append(CheckFinding("train", "the training index is empty"))
    if not test:
        found.append(CheckFinding("test", "the test index is empty"))
    overlap = sorted(set(train) & set(test))
    if overlap:
        found.append(CheckFinding(
            "train n test",
            "%d row position(s) are in BOTH sets, e.g. %s. A row scored in test "
            "and fitted on in training is scored against itself"
            % (len(overlap), overlap[:5])))
    r.findings = tuple(found)
    r.notes.append(
        "Disjoint and non-empty is all this establishes. It does not establish "
        "that the test set was held out, was not reused for model selection, or "
        "is not a renamed validation set.")
    return r


# ---------------------------------------------------------------------------
# L1.4a -- exact duplicate rows across the split
# ---------------------------------------------------------------------------

def check_duplicate_rows_across_split(frame: pd.DataFrame, train_idx=None,
                                      test_idx=None,
                                      columns: Sequence[str] | None = None
                                      ) -> CheckResult:
    """PREREG.md §4's L1.4a: exact duplicate rows across the split.

    A test row byte-identical to a training row is memorisable rather than
    predictable, and the score it earns is not evidence about unseen data.
    """
    r = CheckResult(check="duplicate_rows_across_split", registered_row="L1.4a",
                    looked=False)
    if train_idx is None or test_idx is None:
        r.did_not_look_because = (
            "no split was declared, so duplicates ACROSS one were not checked. "
            "Duplicates within the frame as a whole are a different question and "
            "were not asked either")
        return r
    cols = list(columns) if columns is not None else list(frame.columns)
    if not cols:
        r.did_not_look_because = "the frame has no columns to compare"
        return r
    train = frame.iloc[list(train_idx)][cols]
    test = frame.iloc[list(test_idx)][cols]
    r.looked = True
    r.population = ("%d test row(s) against %d training row(s), over %d column(s)"
                    % (len(test), len(train), len(cols)))
    if not len(train) or not len(test):
        r.notes.append("one side of the split is empty, so no pair could match")
        return r
    key_train = set(map(tuple, train.astype("string").fillna("<NA>").to_numpy()))
    dup_mask = [tuple(row) in key_train
                for row in test.astype("string").fillna("<NA>").to_numpy()]
    n = int(np.sum(dup_mask))
    if n:
        where = [int(i) for i, hit in zip(list(test_idx), dup_mask) if hit][:5]
        r.findings = (CheckFinding(
            "rows",
            "%d test row(s) are exactly equal to a training row over the "
            "compared columns, e.g. positions %s" % (n, where)),)
    return r


# ---------------------------------------------------------------------------
# Not a registered row -- constant columns
# ---------------------------------------------------------------------------

def check_constant_columns(frame: pd.DataFrame) -> CheckResult:
    """A column with one distinct value carries no information.

    NOT one of PREREG.md §4's eleven rows. It is an ordinary data-quality check,
    and it earns its place because a constant column is silent under every probe
    in this package -- so without it, a degenerate column and a clean one look
    identical in the output.
    """
    r = CheckResult(check="constant_columns", registered_row="not a registered row",
                    looked=True,
                    population="%d column(s)" % len(frame.columns))
    if not len(frame):
        r.looked = False
        r.did_not_look_because = "the frame has no rows, so no column has a value"
        return r
    found = []
    for c in frame.columns:
        s = frame[c]
        n_distinct = s.nunique(dropna=False)
        if n_distinct <= 1:
            value = s.iloc[0] if len(s) else None
            found.append(CheckFinding(
                str(c), "one distinct value (%r) over %d row(s); it carries no "
                        "information and is silent under every probe here"
                        % (value, len(s))))
    r.findings = tuple(found)
    return r


# ---------------------------------------------------------------------------
# L2b's neighbourhood -- the label under another name
# ---------------------------------------------------------------------------

def check_label_under_another_name(frame: pd.DataFrame, label: str | None = None,
                                   threshold: float = 0.999) -> CheckResult:
    """A feature that reproduces the label is the label wearing a hat.

    L2b's NEIGHBOURHOOD, not L2b: that row is REVIEW with a `domain_judgment`
    basis whose adjudication is deferred to a module that does not exist. This
    is a single-feature screen of the same shape, and it reports candidates
    rather than deciding anything.
    """
    r = CheckResult(check="label_under_another_name",
                    registered_row="L2b's neighbourhood", looked=False)
    if label is None:
        r.did_not_look_because = (
            "no label column was declared, so no feature was compared against "
            "one. Declare `label_column` in the model file to check it")
        return r
    if label not in frame.columns:
        r.did_not_look_because = (
            "the declared label column %r is not in the built frame, so nothing "
            "was compared against it" % label)
        return r
    y = frame[label]
    others = [c for c in frame.columns if c != label]
    r.looked = True
    r.population = "%d column(s) against the label %r" % (len(others), label)
    found = []
    for c in others:
        s = frame[c]
        if s.equals(y):
            found.append(CheckFinding(
                str(c), "identical to the label %r, value for value" % label))
            continue
        if pd.api.types.is_numeric_dtype(s) and pd.api.types.is_numeric_dtype(y):
            a = pd.to_numeric(s, errors="coerce")
            b = pd.to_numeric(y, errors="coerce")
            if a.nunique(dropna=True) <= 1 or b.nunique(dropna=True) <= 1:
                continue
            corr = a.corr(b)
            if corr is not None and not pd.isna(corr) and abs(corr) >= threshold:
                found.append(CheckFinding(
                    str(c), "correlates with the label %r at %.4f, at or above "
                            "the %.3f screen" % (label, corr, threshold)))
    r.findings = tuple(found)
    r.notes.append(
        "A candidate, not a verdict: a legitimate feature can be near-perfectly "
        "correlated with its label. This screen reports; it does not adjudicate.")
    return r


# ---------------------------------------------------------------------------
# NOT BUILT: "the target survives a shuffle"
# ---------------------------------------------------------------------------
#
# It was written, its known positive did not fire, and it was removed rather
# than have its test weakened. The record of why is here because the reasoning
# is reusable and the next person to propose it deserves it.
#
# THE IDEA. Permute the label's values and re-measure each feature's
# association with it. A relationship that survives is not through the label.
#
# WHY IT CANNOT WORK WITHOUT A MODEL FIT. Permutation destroys the pairing
# between a feature's rows and the label's rows REGARDLESS of why the pairing
# existed. Measured, on a feature that is pure row order against a sorted
# label -- the most positional relationship constructible -- the shuffled
# absolute correlation came out 0.076, 0.050, 0.031, 0.046, 0.018. It collapses
# exactly as a genuine relationship does, so the two are indistinguishable and
# the check is silent on everything.
#
# WORSE THAN VACUOUS. The one case where a shuffled correlation does persist is
# a heavily imbalanced label, where permutation often nearly reproduces the
# original vector. Flagging that would report class imbalance as positional
# leakage -- a false positive dressed as a subtle finding.
#
# WHAT IT WOULD NEED. The real form of this check permutes the label and REFITS,
# asking whether performance survives; that detects a pipeline that saw the
# target, such as an encoding fit across the split. This package fits no models,
# so the check belongs to something that does.


# ---------------------------------------------------------------------------
# Running them together
# ---------------------------------------------------------------------------

def run_all(frame: pd.DataFrame, *, label: str | None = None,
            train_idx=None, test_idx=None) -> list[CheckResult]:
    """Every check, each reporting whether it looked."""
    return [
        check_split_validity(train_idx, test_idx),
        check_duplicate_rows_across_split(frame, train_idx, test_idx),
        check_constant_columns(frame),
        check_label_under_another_name(frame, label),
    ]


def render(results: Iterable[CheckResult]) -> str:
    results = list(results)
    lines = []
    for r in results:
        lines.append("[%s] %s" % (r.outcome, r.check))
        lines.append("  " + r.explain().replace("\n", "\n  "))
        for n in r.notes:
            lines.append("  note: %s" % n)
        lines.append("")
    ran = sum(1 for r in results if r.looked)
    missed = len(results) - ran
    # THE ALL-RAN CASE GETS ITS OWN SENTENCE. The tally read "The other 0 did
    # not look" whenever a complete model was given -- recorded during the
    # definition-of-done walk and deliberately not counted among its six, since
    # it costs a reader nothing. Fixed here rather than left, and reported as
    # outside that list rather than folded into it.
    if missed:
        lines.append("%d of %d check(s) ran. The other %d did not look, and "
                     "that is reported above rather than counted as clean."
                     % (ran, len(results), missed))
    else:
        lines.append("%d of %d check(s) ran. Every check had what it needed, so "
                     "no result above is a silence standing in for one."
                     % (ran, len(results)))
    return "\n".join(lines)
