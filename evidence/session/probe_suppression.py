import sys
sys.path.insert(0, r"C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
sys.path.insert(0, r"C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/tests/registration")

from protocol.runtime_reference import (
    CaseLabels, PromotionStatus, RunContext, SuppressedGate, SuppressedMetric,
    apply_runtime_gates, compute_runtime_metrics)
from traces import tr, rec, labels, find, _M

def show(tag, metrics):
    print(f"--- {tag} ---")
    for mid in sorted(metrics):
        mv = metrics[mid]
        if isinstance(mv, SuppressedMetric):
            print(f"  {mid}: SUPPRESSED")
        else:
            print(f"  {mid}: {mv.numerator}/{mv.denominator} = {mv.value}")
    gates = apply_runtime_gates(metrics)
    for gid in sorted(gates):
        g = gates[gid]
        if isinstance(g, SuppressedGate):
            print(f"  GATE {gid}: SUPPRESSED")
        else:
            print(f"  GATE {gid}: experimental={g.experimental} n={g.clean_n} k={g.clean_findings} completed={g.clean_completed}")

# Scenario 1: all-unsupported body, 2 labelled cases (preserving), promoted na everywhere
traces1 = (
    tr("a", (), inputs=False),
    tr("b", (), inputs=False),
    tr("a", (), status=_M, strategies=()),
    tr("b", (), status=_M, strategies=()),
)
labs1 = (labels("a", ("f1", "c1")), labels("b", ("f1", "c1")))
show("S1 all-unsupported preserving body", compute_runtime_metrics(traces1, labs1))

# Scenario 2: mixed na + unsupported (preserving)
traces2 = (
    tr("a", (), strategies=()),          # not_applicable
    tr("b", (), inputs=False),           # unsupported
    tr("a", (), status=_M, strategies=()),
    tr("b", (), status=_M, strategies=()),
)
show("S2 mixed na+unsupported preserving body", compute_runtime_metrics(traces2, labs1))

# Scenario 3: mixed na + short_circuited (user run)
traces3 = (
    tr("a", (), strategies=(), context=RunContext.USER),   # na
    tr("b", (rec("shuffle", "c1", case="b", finding=find()),),
       context=RunContext.USER, terminal=True),            # short_circuited
    tr("a", (), status=_M, strategies=(), context=RunContext.USER),
    tr("b", (), status=_M, strategies=(), context=RunContext.USER),
)
show("S3 mixed na+short_circuited preserving body", compute_runtime_metrics(traces3, labs1))

# Scenario 4: all-na body sanity — exact suppressible set
traces4 = (
    tr("a", (), strategies=()),
    tr("b", (), cohorts=()),
    tr("a", (), status=_M, strategies=()),
    tr("b", (), status=_M, strategies=()),
)
m4 = compute_runtime_metrics(traces4, labs1)
supp = sorted(k for k, v in m4.items() if isinstance(v, SuppressedMetric) and k.startswith("L3.1|preserving"))
num = sorted(k for k, v in m4.items() if not isinstance(v, SuppressedMetric) and k.startswith("L3.1|preserving"))
print("--- S4 all-na: suppressed set (preserving) ---")
for k in supp: print("  S:", k)
for k in num: print("  N:", k, f"{m4[k].numerator}/{m4[k].denominator}")
print("repr of a suppressed metric:", repr(m4["L3.1|preserving|proof_yield"])[:200])

# Scenario 5: combination runs ONLY on the clean case; na on every leaking-labelled case
traces5 = (
    tr("a", (), strategies=()),                             # na on leaking case
    tr("clean", (rec("shuffle", "c1", case="clean"),
                 rec("shuffle", "c2", case="clean"))),      # completed on clean case
    tr("a", (), status=_M, strategies=()),
    tr("clean", (), status=_M, strategies=()),
)
labs5 = (labels("a", ("f1", "c1")), labels("clean"))
show("S5 na on every leaking case, ran only on clean case", compute_runtime_metrics(traces5, labs5))
