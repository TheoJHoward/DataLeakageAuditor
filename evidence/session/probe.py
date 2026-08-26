import sys
sys.path.insert(0, r"C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
sys.path.insert(0, r"C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/tests/registration")

from protocol.runtime_reference import (
    CaseLabels, CombinationTrace, ExecutionRecord, FindingRecord,
    PromotionStatus, RunContext, ProtocolViolation,
    compute_runtime_metrics, derive_evidence_events, apply_runtime_gates,
)

P = PromotionStatus.PRESERVING
M = PromotionStatus.PROMOTED

def rec(det, case, strat, cohort, status=P, valid=True, finding=None, reason=None):
    return ExecutionRecord(detector_id=det, case_id=case, strategy_id=strat,
                           promotion_status=status, cohort_id=cohort,
                           attempted=True, valid=valid, finding=finding,
                           failure_reason=reason)

def tr(det, case, records, status=P, strategies=("shuffle",), cohorts=("c1","c2"),
       inputs=True, terminal=False, ctx=RunContext.EVALUATION):
    return CombinationTrace(detector_id=det, case_id=case, promotion_status=status,
                            run_context=ctx, resolved_strategies=strategies,
                            selected_eligible_cohorts=cohorts,
                            required_inputs_available=inputs,
                            terminal_decision_occurred=terminal, records=records)

def lab(det, case, *pairs):
    return CaseLabels(detector_id=det, case_id=case, leaking_pairs=frozenset(pairs))

print("=== PROBE 1: whole promoted combination absent (preserving fully traced) ===")
traces = [
    tr("L3.1", "c1", (rec("L3.1","c1","shuffle","c1"), rec("L3.1","c1","shuffle","c2"))),
    tr("L3.1", "c2", (rec("L3.1","c2","shuffle","c1"), rec("L3.1","c2","shuffle","c2"))),
]
labels = [lab("L3.1","c1",("f1","c1")), lab("L3.1","c2")]
try:
    m = compute_runtime_metrics(traces, labels)
    print("NO RAISE — metric prefixes computed:", sorted({k.rsplit('|',1)[0] for k in m}))
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 2: promoted combination exists for c1 only (partial) ===")
traces2 = traces + [
    tr("L3.1", "c1", (rec("L3.1","c1","complex","c1",status=M),
                      rec("L3.1","c1","complex","c2",status=M)),
       status=M, strategies=("complex",)),
]
try:
    m = compute_runtime_metrics(traces2, labels)
    print("NO RAISE")
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 3: duplicate CaseLabels ===")
try:
    compute_runtime_metrics(traces2, labels + [lab("L3.1","c1",("f9","c9"))])
    print("NO RAISE")
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 4: two traces, one combination, one case ===")
try:
    compute_runtime_metrics(traces + [tr("L3.1","c1",())], labels)
    print("NO RAISE")
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 5: labels for a second detector, no traces at all for it ===")
try:
    compute_runtime_metrics(traces, labels + [lab("L2a","c1",("f1","c1"))])
    print("NO RAISE")
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 6: event merge across cases? (same feature/cohort, two cases) ===")
f = FindingRecord(feature="f1", probe_cohort="c1", affected_output_cohort="c1")
tA = tr("L3.1","a1",(rec("L3.1","a1","shuffle","c1",finding=f),
                     rec("L3.1","a1","shuffle","c2")))
tB = tr("L3.1","b1",(rec("L3.1","b1","shuffle","c1",finding=f),
                     rec("L3.1","b1","shuffle","c2")))
ev = derive_evidence_events([tA, tB])
print("events:", len(ev), [(e.case_id, e.feature, e.affected_output_cohort) for e in ev])

print()
print("=== PROBE 7: within-case merge across strategies and probes ===")
f2 = FindingRecord(feature="f1", probe_cohort="c2", affected_output_cohort="c1")
tC = tr("L3.1","m1",(rec("L3.1","m1","shuffle","c1",finding=f),
                     rec("L3.1","m1","shuffle","c2",finding=f2),
                     rec("L3.1","m1","noise","c1",finding=f),
                     rec("L3.1","m1","noise","c2")),
        strategies=("shuffle","noise"))
ev = derive_evidence_events([tC])
print("events:", len(ev), "probes:", sorted(ev[0].probe_cohorts), "strategies:", sorted(ev[0].strategies))

print()
print("=== PROBE 8: finding whose probe_cohort mismatches its record cohort_id ===")
fbad = FindingRecord(feature="f1", probe_cohort="c9", affected_output_cohort="c1")
tD = tr("L3.1","q1",(rec("L3.1","q1","shuffle","c1",finding=fbad),
                     rec("L3.1","q1","shuffle","c2")))
try:
    ev = derive_evidence_events([tD])
    print("NO RAISE — event probe_cohorts:", sorted(ev[0].probe_cohorts))
    m = compute_runtime_metrics([tD],[lab("L3.1","q1",("f1","c1"))])
    ps = m["L3.1|preserving|cohort_sensitivity"]
    print("cohort_sensitivity:", ps.numerator, "/", ps.denominator)
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 9: same pair primary in preserving, secondary in promoted ===")
fsec = FindingRecord(feature="f1", probe_cohort="c1", affected_output_cohort="c1", is_secondary=True)
tE1 = tr("L3.1","s1",(rec("L3.1","s1","shuffle","c1",finding=f),
                      rec("L3.1","s1","shuffle","c2")))
tE2 = tr("L3.1","s1",(rec("L3.1","s1","complex","c1",status=M,finding=fsec),
                      rec("L3.1","s1","complex","c2",status=M)),
         status=M, strategies=("complex",))
try:
    ev = derive_evidence_events([tE1,tE2])
    print("NO RAISE — events:", [(e.promotion_status.value, e.is_secondary) for e in ev])
except ProtocolViolation as e:
    print("RAISED:", e)

print()
print("=== PROBE 10: count denominators include sc cases; counts feed no gate ===")
tU1 = tr("L3.1","u1",(rec("L3.1","u1","shuffle","c1",finding=f),),
         ctx=RunContext.USER, terminal=True)
tU2 = tr("L3.1","u2",(rec("L3.1","u2","shuffle","c1"), rec("L3.1","u2","shuffle","c2")))
m = compute_runtime_metrics([tU1,tU2],[lab("L3.1","u1",("f1","c1")), lab("L3.1","u2")])
for name in ("not_applicable_count","unsupported_count","short_circuited_count",
             "combination_completion_rate","combination_incompletion_rate",
             "clean_case_finding_rate"):
    mv = m[f"L3.1|preserving|{name}"]
    print(f"{name}: {mv.numerator}/{mv.denominator} den_members={sorted(mv.denominator_members)}")
g = apply_runtime_gates(m)
print("gate:", g)
