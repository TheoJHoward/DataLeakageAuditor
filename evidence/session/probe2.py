import sys
sys.path.insert(0, r"C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

from protocol.runtime_reference import (
    CaseLabels, CombinationTrace, ExecutionRecord, FindingRecord,
    PromotionStatus, RunContext, ProtocolViolation,
    compute_runtime_metrics, resolve_state_pair,
)

P = PromotionStatus.PRESERVING
from protocol.runtime_reference import FailureReason as FR

def rec(case, strat, cohort, valid=True, finding=None, reason=None):
    return ExecutionRecord(detector_id="L3.1", case_id=case, strategy_id=strat,
                           promotion_status=P, cohort_id=cohort,
                           attempted=True, valid=valid, finding=finding,
                           failure_reason=reason)

def tr(case, records, cohorts=("c1",)):
    return CombinationTrace(detector_id="L3.1", case_id=case, promotion_status=P,
                            run_context=RunContext.EVALUATION,
                            resolved_strategies=("shuffle",),
                            selected_eligible_cohorts=cohorts,
                            required_inputs_available=True,
                            terminal_decision_occurred=False, records=records)

print("=== PROBE A: invalid record at a cohort OUTSIDE the selected schedule changes incomplete's reason ===")
# schedule: only c1. Real failure at c1 = crash. Out-of-schedule record at c9 = determinism.
t_clean = tr("a1", (rec("a1","shuffle","c1",valid=False,reason=FR.CRASH),))
s, o = resolve_state_pair(t_clean)
print("without out-of-schedule record:", s.kind.value, s.reason.value if s.reason else None, "x", o.value)

t_dirty = tr("a1", (rec("a1","shuffle","c1",valid=False,reason=FR.CRASH),
                    rec("a1","shuffle","c9",valid=False,reason=FR.DETERMINISM)))
try:
    s, o = resolve_state_pair(t_dirty)
    print("WITH out-of-schedule record:  ", s.kind.value, s.reason.value if s.reason else None, "x", o.value)
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE B: valid finding at an out-of-schedule cohort feeds proof_yield / probed set ===")
f9 = FindingRecord(feature="f1", probe_cohort="c9", affected_output_cohort="c9")
t = tr("b1", (rec("b1","shuffle","c1"),
              rec("b1","shuffle","c9",finding=f9)))
labels = [CaseLabels("L3.1","b1",frozenset({("f1","c9")}))]
try:
    m = compute_runtime_metrics([t], labels)
    for name in ("proof_yield","cohort_sensitivity","unprobed_feature_cohort_rate",
                 "combination_completion_rate"):
        mv = m[f"L3.1|preserving|{name}"]
        print(f"{name}: {mv.numerator}/{mv.denominator}")
    s, o = resolve_state_pair(t)
    print("state:", s.kind.value, "x", o.value)
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE C: same, but WITHOUT the rogue record (spec-conformant trace) ===")
t2 = tr("b1", (rec("b1","shuffle","c1"),))
m = compute_runtime_metrics([t2], labels)
for name in ("proof_yield","cohort_sensitivity","unprobed_feature_cohort_rate",
             "combination_completion_rate"):
    mv = m[f"L3.1|preserving|{name}"]
    print(f"{name}: {mv.numerator}/{mv.denominator}")
