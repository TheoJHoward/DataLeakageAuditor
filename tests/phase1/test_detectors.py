"""B9 -- the value and null detectors, against controls with KNOWN answers.

EVERY DETECTOR HERE HAS A POSITIVE AND A NEGATIVE CONTROL. A detector exercised
only on real data cannot be told apart from a detector that does nothing: both
produce a plausible-looking trace. So the synthetic frame below is built so that
each detector MUST fire on a named column and MUST stay silent on another, and
both are asserted.

THE FIRST DRAFT OF THIS FILE HAD A CONTROL THAT COULD NOT FIRE. `s` held
"a0"/"a1"/"a2" -- all length 2 -- so `s.map(len)` was constant and no
permutation of `s` could move it. The detector reported silence, correctly, and
the control proved nothing. That is the `aggressor_side` class (a predicate or
projection that is constant over the column's actual values, so the column is
invisible to a value shuffle) reproduced by accident in the test written to
demonstrate the instrument. The lengths now vary, and this paragraph is why.
"""
from __future__ import annotations

import subprocess
import sys
import textwrap

import numpy as np
import pandas as pd
import pytest

from leakaudit import corruption as cx
from leakaudit.detectors import (
    NULL_DETECTOR_ID,
    VALUE_DETECTOR_ID,
    null_domain_statement,
    probe_nulls,
    probe_values,
    value_domain_statement,
)
from leakaudit.probe import domain_statement as columndep_domain
from protocol.runtime_reference import (
    EvidenceOutcome,
    FailureReason,
    RunContext,
    ScheduleStateKind,
    resolve_state_pair,
)

N = 40


def _frame() -> pd.DataFrame:
    return pd.DataFrame({
        "i": np.arange(N, dtype="int32"),
        "f": pd.Series([float(k) if k % 5 else np.nan for k in range(N)],
                       dtype="float64"),
        "b": pd.Series([k % 2 == 0 for k in range(N)]),
        "s": pd.Series(["a" * (1 + k % 4) for k in range(N)]),   # lengths VARY
        "t": pd.Series(pd.date_range("2025-01-01", periods=N, freq="s")),
        "unused": np.ones(N, dtype="float64"),
    })


def _build(f: pd.DataFrame) -> pd.DataFrame:
    """Reads i's VALUES, f's NULL MASK only, s's values, and nothing else."""
    return pd.DataFrame({
        "value_of_i": f["i"] * 2,
        "null_of_f": f["f"].isna().astype("int8"),
        "count_of_s": f["s"].map(len),
        "const": np.zeros(len(f)),
    }, index=f.index)


def _run(fn):
    return fn({"raw": _frame()}, _build, case_id="ctl",
              run_context=RunContext.FIXTURE, bare=True)


# ---------------------------------------------------------------- valueread --

def test_value_detector_fires_on_a_value_read_and_is_silent_on_an_unread_column():
    r = _run(probe_values)
    assert "col:raw.i" in r.dependency_map, "positive control did not fire"
    assert "value_of_i" in r.dependency_map["col:raw.i"]
    assert "col:raw.s" in r.dependency_map, "the string control did not fire"
    assert "count_of_s" in r.dependency_map["col:raw.s"]
    assert "col:raw.unused" not in r.dependency_map, "negative control fired"


def test_value_detectors_promoted_side_is_a_dtype_defined_subset():
    """§6.6 l.1080 permits it; this asserts WHICH columns and why."""
    r = _run(probe_values)
    prom = set(r.promoted.selected_eligible_cohorts)
    # int32 -> float64 and bool -> int64 are the two widenings that exist.
    assert prom == {"col:raw.i", "col:raw.b"}
    # float, str and datetime have no wider dtype and are therefore not
    # eligible -- NOT silently attempted and failed.
    for absent in ("col:raw.f", "col:raw.s", "col:raw.t", "col:raw.unused"):
        assert absent not in prom
    state, _ = resolve_state_pair(r.promoted)
    assert state.kind is ScheduleStateKind.COMPLETED, (
        "the promoted side ran its whole schedule over its own cohort set; "
        "an ineligible column is not an incomplete one")


def test_at_the_dtype_ceiling_only_the_out_of_dtype_sentinel_perturbs_at_all():
    """The promoted side's reason for existing, demonstrated rather than argued.

    A column pinned at its dtype's maximum is the case where the preserving
    strategies RUN OUT. A permutation of identical values is the identity. The
    in-dtype sentinel is by construction capped by the dtype, and at the ceiling
    the cap IS the column's value -- so it is the identity too. Both are
    recorded `control_artifact`: the probe did not happen, which is not the same
    as a probe that happened and found nothing.

    The out-of-dtype sentinel is the only strategy that can perturb this column,
    and it costs promotion to do it. That trade is the whole content of the
    promoted combination.

    A first draft of this test framed it as a CLAMP in the builder and asserted
    the promoted side would get past it. That was wrong on its face -- a clamp
    means the output is insensitive to anything above the bound, so nothing
    should move, and the test failed for the right reason.
    """
    lim = np.iinfo("int32").max
    src = pd.DataFrame({"i": np.full(N, lim, dtype="int32")})

    def build(f):
        return pd.DataFrame({"passthrough": f["i"].astype("float64")},
                            index=f.index)

    r = probe_values({"raw": src}, build, case_id="ceiling",
                     run_context=RunContext.FIXTURE, bare=True)

    pres = r.preserving.records
    assert pres and all(not x.valid for x in pres), (
        "at the ceiling neither preserving strategy can perturb")
    assert {x.failure_reason for x in pres} == {FailureReason.CONTROL_ARTIFACT}
    pres_state, pres_outcome = resolve_state_pair(r.preserving)
    assert pres_outcome is EvidenceOutcome.NONE, (
        "no valid execution occurred, so the outcome is `none` -- reporting "
        "`observed_silence` here would claim a probe that never ran")

    prom = [x for x in r.promoted.records if x.finding]
    assert prom, "the out-of-dtype sentinel should be able to perturb the ceiling"
    assert {x.finding.feature for x in prom} == {"passthrough"}


# ----------------------------------------------------------------- nullread --

def test_null_detector_sees_the_float_null_mask_columndep_cannot():
    """The gap columndep publishes, closed -- and the closure demonstrated.

    `null_of_f` reads `f` ONLY through `isna()`. `f` is float, so `nan`
    preserves there and columndep -- which configures `nan` in the promoted
    combination only -- never applies it. This detector does.
    """
    r = _run(probe_nulls)
    assert "col:raw.f" in r.dependency_map, "the gap is not closed"
    assert "null_of_f" in r.dependency_map["col:raw.f"]
    assert "col:raw.f" in r.preserving.selected_eligible_cohorts


def test_null_detectors_two_combinations_partition_the_columns():
    r = _run(probe_nulls)
    pres = set(r.preserving.selected_eligible_cohorts)
    prom = set(r.promoted.selected_eligible_cohorts)
    every = {"col:raw.%s" % c for c in _frame().columns}
    assert not (pres & prom), "a column is in BOTH combinations"
    assert pres | prom == every, "a column is in NEITHER combination"
    # And the split is by dtype, per §3.2: nan promotes exactly where the column
    # cannot hold a null in its own dtype.
    assert prom == {"col:raw.i", "col:raw.b"}


def test_null_detector_is_silent_on_a_column_nothing_reads():
    r = _run(probe_nulls)
    assert "col:raw.unused" not in r.dependency_map


# ------------------------------------------------- the empty combination ----

def test_an_empty_promoted_combination_is_not_applicable_not_a_missing_trace():
    """§6.6 l.1084's second clause, exercised.

    A float-only frame gives `valueread`'s promoted side resolved strategies,
    available inputs and NOTHING TO DO. The trace still exists -- l.1078 makes a
    missing trace a protocol violation -- and resolves `not_applicable x none`,
    which is a legal pair. A vacuous `completed` would have to pair with `none`,
    which the legality table forbids, and that is the reason the clause is there.
    """
    src = pd.DataFrame({"a": np.arange(N, dtype="float64"),
                        "b": np.arange(N, dtype="float64")})

    def build(f):
        return pd.DataFrame({"out": f["a"] * 2.0}, index=f.index)

    r = probe_values({"raw": src}, build, case_id="empty",
                     run_context=RunContext.FIXTURE, bare=True)
    assert r.promoted.selected_eligible_cohorts == ()
    assert r.promoted.records == ()
    state, outcome = resolve_state_pair(r.promoted)      # raises on an illegal pair
    assert state.kind is ScheduleStateKind.NOT_APPLICABLE
    assert outcome is EvidenceOutcome.NONE
    # the preserving side still did its work
    assert "col:raw.a" in r.dependency_map


# ---------------------------------------------------- the seed, R134 finding --

def test_perturbation_seed_is_stable_across_processes():
    """R134: the seed was `abs(hash((frame, column, strategy)))`.

    CPython salts `hash()` for `str` with PYTHONHASHSEED, random per process
    unless pinned, and nothing in this repository pins it. So the same cohort
    drew a different permutation on every run and the four sweep workers each
    drew from a different salt. Nothing it produced was invalid -- any
    permutation is a legitimate shuffle -- but the run was not reproducible,
    and a shuffle that moves nothing on one draw and something on the next
    turns `observed_silence` into a coin toss.

    THREE SEPARATE PROCESSES, because that is the only place the defect lived.
    Calling `seed_for` twice inside one process would have passed against the
    old implementation too, which is the shape of guard that proves nothing.
    """
    prog = textwrap.dedent(
        """
        import pathlib, sys
        root = pathlib.Path(%r)
        sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "src"))
        from leakaudit.corruption import seed_for
        print(seed_for("trades", "size", "shuffle"))
        """ % str(__import__("pathlib").Path(__file__).resolve().parents[2]))
    seen = set()
    for _ in range(3):
        out = subprocess.run([sys.executable, "-c", prog], capture_output=True,
                             text=True, timeout=120)
        assert out.returncode == 0, out.stderr
        seen.add(out.stdout.strip())
    assert len(seen) == 1, "the seed differs between processes: %s" % sorted(seen)


def test_seed_parts_cannot_collide_by_concatenation():
    assert cx.seed_for("ab", "c") != cx.seed_for("a", "bc")


# ------------------------------------------------------- domain statements --

@pytest.mark.parametrize("stmt,strategies", [
    (value_domain_statement, (cx.SHUFFLE, cx.SENTINEL, cx.SENTINEL_OOD)),
    (null_domain_statement, (cx.NAN,)),
])
def test_domain_statements_name_every_configured_strategy(stmt, strategies):
    """§39: a silence is honest only with its domain attached, and the domain
    has to be DERIVED from the configuration or it drifts from what runs."""
    text = stmt()
    for s in strategies:
        assert s in text, "%s is configured but unnamed in the domain" % s


def test_columndep_domain_statement_is_updated_not_deleted():
    """DELTA R134: the gap statement is UPDATED when the gap closes.

    A reader of an EARLIER columndep result needs to know the gap was open when
    that result was produced. Deleting the sentence would make the closure
    invisible to exactly the reader it matters to -- so both halves must be
    present: the gap, and the detector that now covers it.
    """
    text = columndep_domain()
    assert "not applied to float columns" in text, "the gap statement was deleted"
    assert NULL_DETECTOR_ID in text, "the closure is not recorded"


def test_detector_ids_are_distinct_and_separator_free():
    ids = (VALUE_DETECTOR_ID, NULL_DETECTOR_ID)
    assert len(set(ids)) == 2
    for i in ids:
        assert "|" not in i          # reserved member/gate separator
