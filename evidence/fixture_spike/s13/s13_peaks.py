import csv, os
B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
dm = list(csv.DictReader(open(os.path.join(B, "n1", "declared_map.csv"), newline="", encoding="utf-8")))
TRADE = {"trades_all", "trades_buy", "trades_sell", "trades_large"}

def cell(inst, mon, side="contaminated"):
    return [d for d in dm if d["side"] == side and d["instrument"] == inst and d["month"] == mon
            and d["boundary"] == "decision_T" and d["scored_flag"] == "SCORED"]

for inst, mon in [("es", "2025-12"), ("gc", "2025-10"), ("nq", "2025-01"), ("es", "2025-11"), ("es", "2025-01"), ("zc", "2025-01")]:
    sub = cell(inst, mon)
    n = int(sub[0]["rows"])
    mx = max(int(d["strict_count"]) for d in sub)
    mxt = max((int(d["strict_count"]) for d in sub if d["class"] in TRADE), default=0)
    who = sorted(d["class"] for d in sub if int(d["strict_count"]) == mx)
    whot = sorted(d["class"] for d in sub if d["class"] in TRADE and int(d["strict_count"]) == mxt)
    print("%s %s rows=%d | full-class max %d (%.2f%%) classes=%s | trade max %d (%.2f%%) classes=%s | nclasses=%d"
          % (inst, mon, n, mx, 100.0*mx/n, ",".join(who), mxt, 100.0*mxt/n, ",".join(whot), len(sub)))

# which trade classes are live across all 48 contaminated cells
print("\nper-trade-class strict-positive counts over the 48 contaminated cells:")
from collections import Counter
c = Counter(); ce = Counter(); tot = Counter()
for d in dm:
    if d["side"] == "contaminated" and d["boundary"] == "decision_T" and d["scored_flag"] == "SCORED" and d["class"] in TRADE:
        tot[d["class"]] += 1
        if int(d["strict_count"]) > 0: c[d["class"]] += 1
        if int(d["equal_count"]) > 0: ce[d["class"]] += 1
for k in sorted(tot):
    print("  %-13s scored cells %2d  strict>0 %2d  equal>0 %2d" % (k, tot[k], c[k], ce[k]))
