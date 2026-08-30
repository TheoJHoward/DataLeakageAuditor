"""The probe's DOMAIN statement, and the gap it publishes (§39).

PREREG.md §39: silence is honest only with its domain attached. These tests do
two things a prose statement cannot: they prove the published domain matches what
the code actually runs, and they DEMONSTRATE the gap rather than asserting it --
a documented limitation nobody has reproduced is a claim, not a finding.
"""
import numpy as np
import pandas as pd

from leakaudit import cohort_id_for, probe_columns
from leakaudit.corruption import NAN, SENTINEL, SHUFFLE
from leakaudit.probe import (
    PRESERVING_STRATEGIES,
    PROMOTED_STRATEGIES,
    domain_statement,
)


def _frame(n=40):
    rng = np.random.default_rng(5)
    return pd.DataFrame({
        "f": rng.normal(size=n),                 # float
        "i": rng.integers(1, 40, n),             # int
    })


# --------------------------------------------------------------------------
# The statement must describe the configuration, not a remembered version of it
# --------------------------------------------------------------------------

def test_domain_statement_is_derived_from_the_configuration():
    s = domain_statement()
    for strat in PRESERVING_STRATEGIES + PROMOTED_STRATEGIES:
        assert "`%s`" % strat in s, "strategy %r runs but is not in the domain" % strat
    assert "NOT probed" in s


def test_every_result_carries_its_domain():
    r = probe_columns({"raw": _frame()}, lambda d: pd.DataFrame(
        {"y": d["f"] * 2.0}, index=d.index), bare=True, case_id="c")
    assert r.domain == domain_statement()
    assert r.domain, "a result carried no domain: silence would be unqualified"


def test_the_configuration_the_statement_describes_is_the_one_that_runs():
    r = probe_columns({"raw": _frame()}, lambda d: pd.DataFrame(
        {"y": d["f"] * 2.0 + d["i"]}, index=d.index), bare=True, case_id="c")
    assert set(r.preserving.resolved_strategies) == set(PRESERVING_STRATEGIES)
    assert set(r.promoted.resolved_strategies) == set(PROMOTED_STRATEGIES)
    # nan is configured only where it promotes -- the float column is absent
    assert r.promoted.selected_eligible_cohorts == (cohort_id_for("raw", "i"),)


# --------------------------------------------------------------------------
# THE GAP, DEMONSTRATED. This is the known-positive B6 asks for, and it FAILS
# to fire -- which is the point. It is kept as an executable record of the
# limitation, so the gap cannot be quietly forgotten or quietly closed.
# --------------------------------------------------------------------------

def test_null_mask_reader_on_a_float_column_is_MISSED_and_this_is_the_gap():
    """A feature whose only read of a float column is its null mask.

    No configured strategy introduces a null into a float column: `shuffle` and
    `sentinel` preserve the null pattern, and `nan` is configured only in the
    promoted combination, where a float column never lands. So the probe reports
    silence about a column the feature genuinely reads.

    THE ASSERTION IS THAT IT IS MISSED. If this test ever fails, the gap has
    closed and the domain statement is now overstating the limitation -- delete
    the gap from `domain_statement()` in the same change.
    """
    def reads_only_the_null_mask(d):
        return pd.DataFrame({"n_missing": [float(d["f"].isna().sum())] * len(d)},
                            index=d.index)

    r = probe_columns({"raw": _frame()}, reads_only_the_null_mask,
                      bare=True, case_id="c")
    cid = cohort_id_for("raw", "f")

    assert cid not in r.dependency_map, (
        "the float null-mask read was DETECTED -- the gap has closed; update "
        "domain_statement() in the same change")
    recs = [x for x in r.preserving.records if x.cohort_id == cid]
    assert recs and all(x.valid and x.finding is None for x in recs)
    assert "null mask" in r.domain, (
        "the probe missed it AND did not publish the gap -- unqualified silence")


def test_the_same_read_on_an_INT_column_is_caught():
    """The companion positive: the gap is dtype-specific, not a blanket failure
    to see null-mask reads. On an int column `nan` promotes, so it is
    configured, so the read is found."""
    def reads_only_the_null_mask(d):
        return pd.DataFrame({"n_missing": [float(d["i"].isna().sum())] * len(d)},
                            index=d.index)

    r = probe_columns({"raw": _frame()}, reads_only_the_null_mask,
                      bare=True, case_id="c")
    assert cohort_id_for("raw", "i") in r.dependency_map, (
        "nan is configured on int columns; this read should have been found")
