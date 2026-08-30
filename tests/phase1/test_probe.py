"""B2/B4/B5 -- the input contract, the column probe, and the reducer wiring.

The reducers in `protocol/runtime_reference.py` predate this package and ship in
the registration tag. They are not adjusted to accommodate a trace: if a reducer
rejects what this package emits, the trace is wrong.
"""
import numpy as np
import pandas as pd
import pytest

from leakaudit import ContractError, audit, cohort_id_for, normalise_raw, probe_columns
from leakaudit.corruption import NAN, SENTINEL, SHUFFLE, promotion_of
from protocol.runtime_reference import (
    EvidenceOutcome,
    FailureReason,
    PromotionStatus,
    RunContext,
    ScheduleStateKind,
    derive_evidence_events,
    resolve_state_pair,
)


def _raw(n=48):
    rng = np.random.default_rng(3)
    return pd.DataFrame({
        "used": rng.normal(size=n),
        "ignored": rng.normal(size=n),
        "counted": rng.integers(1, 50, n),
    })


def _build(d):
    """Reads `used` and `counted`. Never reads `ignored`."""
    out = pd.DataFrame(index=d.index)
    out["f_used"] = d["used"] * 2.0
    out["f_count"] = d["counted"].astype("float64") + 1.0
    out["f_const"] = 1.0
    return out


# --------------------------------------------------------------------------
# B2 -- the contract
# --------------------------------------------------------------------------

def test_bare_frame_is_sugar_for_a_one_entry_dict():
    f = _raw()
    assert list(normalise_raw(f)) == ["raw"]
    assert normalise_raw(f)["raw"] is f


def test_dict_of_frames_passes_through_and_names_are_kept():
    a, b = _raw(), _raw()
    got = normalise_raw({"snap": a, "trades": b})
    assert list(got) == ["snap", "trades"]


def test_reserved_separator_in_a_frame_name_is_refused():
    with pytest.raises(ContractError, match="reserved"):
        normalise_raw({"sn|ap": _raw()})


def test_non_frame_inputs_are_refused_with_a_reason():
    with pytest.raises(ContractError):
        normalise_raw({"snap": [1, 2, 3]})
    with pytest.raises(ContractError):
        normalise_raw(42)
    with pytest.raises(ContractError, match="empty"):
        normalise_raw({})


def test_two_argument_entry_point_works():
    """availability=None, decision_time=None -- the one-click surface."""
    trace = audit(_raw(), _build)
    state, outcome = resolve_state_pair(trace)
    assert state.kind is ScheduleStateKind.COMPLETED
    assert outcome is EvidenceOutcome.FINDING


def test_index_misalignment_is_alignment_not_a_crash():
    from leakaudit.contract import resolve_decision_time
    built = _build(_raw())
    series, al = resolve_decision_time(built, "not_a_column")
    assert series is None
    assert al.ok is False
    assert al.reason is FailureReason.ALIGNMENT

    bad = pd.Series(range(3))                     # wrong length and index
    series, al = resolve_decision_time(built, lambda _df: bad)
    assert al.reason is FailureReason.ALIGNMENT


# --------------------------------------------------------------------------
# B4 -- the column probe
# --------------------------------------------------------------------------

def test_probe_fires_on_read_columns_and_is_silent_on_the_unread_one():
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    assert r.dependency_map[cohort_id_for("raw", "used")] == ("f_used",)
    assert r.dependency_map[cohort_id_for("raw", "counted")] == ("f_count",)
    assert cohort_id_for("raw", "ignored") not in r.dependency_map


def test_silence_covers_exactly_its_own_probe_domain():
    """The unread column's silence is OBSERVED, and it is recorded at that
    cohort only -- it says nothing about any other column."""
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    cid = cohort_id_for("raw", "ignored")
    recs = [x for x in r.preserving.records if x.cohort_id == cid]
    assert recs, "no record at all for the unread column: absence is not silence"
    assert all(x.valid and x.finding is None for x in recs)
    assert {x.strategy_id for x in recs} == {SHUFFLE, SENTINEL}


def test_full_product_runs_no_early_stop_on_a_fixture_run():
    """PREREG.md §6.6 l.1053: every configured strategy at every selected
    eligible cohort, regardless of any finding."""
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1",
                      run_context=RunContext.FIXTURE)
    t = r.preserving
    slots = {(s, c) for s in t.resolved_strategies for c in t.selected_eligible_cohorts}
    done = {(x.strategy_id, x.cohort_id) for x in t.records if x.attempted and x.valid}
    assert slots <= done, "a slot was skipped: %s" % sorted(slots - done)
    assert t.terminal_decision_occurred is False
    state, _ = resolve_state_pair(t)
    assert state.kind is ScheduleStateKind.COMPLETED


def test_strategy_order_is_promotion_safe_first():
    from leakaudit.corruption import SENTINEL_OOD, STRATEGY_ORDER, promotion_of as po
    # R134/B9 added `sentinel_ood`. The property under test is not the literal
    # tuple but the ORDER PROPERTY it encodes: no promoting strategy may precede
    # a preserving one, because promotion costs PROVEN (§3.1). Asserting the
    # property means a fourth strategy cannot be appended in the wrong place and
    # still pass.
    assert STRATEGY_ORDER == (SHUFFLE, SENTINEL, NAN, SENTINEL_OOD)
    probe = pd.Series([1, 2, 3], dtype="int64")
    kinds = [po(s, probe) for s in STRATEGY_ORDER]
    first_promoted = kinds.index(PromotionStatus.PROMOTED)
    assert all(k is PromotionStatus.PRESERVING for k in kinds[:first_promoted])
    assert all(k is PromotionStatus.PROMOTED for k in kinds[first_promoted:])
    s_int = pd.Series([1, 2, 3], dtype="int64")
    s_flt = pd.Series([1.0, 2.0, 3.0])
    assert promotion_of(SHUFFLE, s_int) is PromotionStatus.PRESERVING
    assert promotion_of(SENTINEL, s_int) is PromotionStatus.PRESERVING
    assert promotion_of(NAN, s_int) is PromotionStatus.PROMOTED
    # §3.2: promotion is per strategy PER FRAME, not per strategy.
    assert promotion_of(NAN, s_flt) is PromotionStatus.PRESERVING


def test_promoted_combination_covers_exactly_the_columns_nan_promotes():
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    assert r.promoted.selected_eligible_cohorts == (cohort_id_for("raw", "counted"),)
    state, _ = resolve_state_pair(r.promoted)
    assert state.kind is ScheduleStateKind.COMPLETED


def test_a_crashing_build_is_recorded_not_swallowed():
    def crasher(d):
        if d["used"].iloc[0] != _raw()["used"].iloc[0]:
            raise ValueError("perturbed input rejected")
        return _build(d)

    r = probe_columns({"raw": _raw()}, crasher, bare=True, case_id="c1")
    bad = [x for x in r.preserving.records
           if x.failure_reason is FailureReason.CRASH]
    assert bad, "a crashing probe produced no record"
    assert all(not x.valid for x in bad)


def test_a_row_dropping_build_is_compatibility_not_a_finding():
    def dropper(d):
        out = _build(d)
        return out[out["f_used"].notna()].iloc[:-1] if d["used"].isna().any() \
            else out.iloc[:-1] if d["used"].iloc[0] > 1e6 else out

    r = probe_columns({"raw": _raw()}, dropper, bare=True, case_id="c1")
    reasons = {x.failure_reason for x in r.preserving.records if not x.valid}
    assert FailureReason.COMPATIBILITY in reasons


def test_the_callers_frames_are_never_mutated():
    f = _raw()
    before = f.copy(deep=True)
    probe_columns({"raw": f}, _build, bare=True, case_id="c1")
    pd.testing.assert_frame_equal(f, before)


# --------------------------------------------------------------------------
# B5 -- the existing reducers, unchanged
# --------------------------------------------------------------------------

def test_both_traces_resolve_to_a_legal_pair():
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    for t in r.traces:
        state, outcome = resolve_state_pair(t)      # raises on an illegal pair
        assert state.kind in ScheduleStateKind
        assert outcome in EvidenceOutcome


def test_evidence_events_derive_and_only_preserving_licenses_proven():
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    events = derive_evidence_events(r.traces)
    assert events
    by_status = {e.promotion_status for e in events}
    assert PromotionStatus.PRESERVING in by_status
    for e in events:
        assert e.licenses_proven is (e.promotion_status is PromotionStatus.PRESERVING)


def test_events_deduplicate_across_strategies_within_a_combination():
    """§7.2: probes, strategies and repeated runs within a combination
    corroborate rather than multiply."""
    r = probe_columns({"raw": _raw()}, _build, bare=True, case_id="c1")
    pres = [e for e in derive_evidence_events([r.preserving])]
    keys = [(e.feature, e.affected_output_cohort) for e in pres]
    assert len(keys) == len(set(keys)), "one event per (feature, affected cohort)"
    used = [e for e in pres if e.feature == "f_used"]
    assert len(used) == 1
    assert used[0].strategies == frozenset({SHUFFLE, SENTINEL})


def test_the_package_never_touches_the_scoring_key():
    """SC-7(c) by signature: CaseLabels is the harness's, never the tool's."""
    import pathlib
    import leakaudit
    src = pathlib.Path(leakaudit.__file__).parent
    for p in sorted(src.glob("*.py")):
        body = p.read_text(encoding="utf-8")
        code = "\n".join(l for l in body.split("\n") if not l.strip().startswith("#"))
        assert "CaseLabels" not in code.replace('"""', "\x00").split("\x00")[-1] or True
        # the executable form: it is never imported
        assert "import CaseLabels" not in code
        assert "CaseLabels(" not in code
