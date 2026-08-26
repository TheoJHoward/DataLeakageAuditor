r"""M2 pedigree support — derive the T1-vs-C4 comparison table from the two CSVs.

Inputs (read-only):
  t1\violation_table.csv      (T1 orchestrated measurement, per feature COLUMN)
  c4\independent_counts.csv   (C4 blind re-measurement, per EVENT CLASS)

T1 is per-column; every column of a class must carry identical counts within a
(side, boundary) — asserted here, never assumed. Boundary name mapping:
  T1 'claimed_T_prev' (corrected side)  ==  C4 'prev_row_B'   (B_i = T_{i-1})
  T1 'decision_T'                        ==  C4 'decision_T'   (T_i)

Outputs: c4\t1_vs_c4_comparison.csv and stdout log (captured to
c4\build_t1_c4_comparison_output.txt by the caller).
"""
import csv
import sys
from collections import defaultdict

BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
T1 = BASE + r"\t1\violation_table.csv"
C4 = BASE + r"\c4\independent_counts.csv"
OUT = BASE + r"\c4\t1_vs_c4_comparison.csv"

sys.stdout.reconfigure(encoding="utf-8")

# ---- load T1 (per column) and collapse to per (event_class, side, boundary) ----
t1_cells = defaultdict(list)   # (event_class, side, boundary) -> [(column, strict, equal, total)]
with open(T1, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        t1_cells[(r["event_class"], r["side"], r["boundary"])].append(
            (r["column"], int(r["strictly_after_count"]), int(r["equal_count"]), int(r["total_rows"]))
        )

t1 = {}
for key, rows in sorted(t1_cells.items()):
    vals = {(s, e, t) for (_c, s, e, t) in rows}
    assert len(vals) == 1, f"T1 columns disagree within {key}: {rows}"
    s, e, t = next(iter(vals))
    t1[key] = dict(strict=s, equal=e, total=t, n_cols=len(rows),
                   cols=",".join(c for (c, *_x) in rows))
    print(f"T1 {key}: {len(rows)} column(s) all identical -> strict={s} equal={e} total={t}")

n_cols_total = sum(v["n_cols"] for k, v in t1.items() if k[1] == "corrected" and k[2] == "decision_T")
print(f"T1 corrected/decision_T column coverage: {n_cols_total} columns (expect 33)")

# ---- load C4 (per class) ----
c4 = {}
class_order = []
with open(C4, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        c4[(r["event_class"], r["boundary"])] = {k: int(r[k]) for k in
            ("strict_count", "equal_count", "total_rows",
             "gap_row_subset_strict", "gap_row_subset_equal", "n_events_in_class")}
        if r["event_class"] not in class_order:
            class_order.append(r["event_class"])

# ---- compare ----
rows_out = []
all_ok = True
for cls in class_order:
    for c4_bnd, t1_bnd in (("decision_T", "decision_T"), ("prev_row_B", "claimed_T_prev")):
        c = c4[(cls, c4_bnd)]
        t = t1[(cls, "corrected", t1_bnd)]
        cont = t1[(cls, "contaminated", "decision_T")]
        agree = (c["strict_count"] == t["strict"] and c["equal_count"] == t["equal"]
                 and c["total_rows"] == t["total"])
        all_ok &= agree
        delta_cont = cont["strict"] - c["strict_count"] if c4_bnd == "prev_row_B" else ""
        eq_cont = (cont["equal"] == c["equal_count"]) if c4_bnd == "prev_row_B" else ""
        rows_out.append(dict(
            event_class=cls, boundary_c4=c4_bnd, boundary_t1=t1_bnd,
            t1_columns_in_class=t["n_cols"],
            t1_corrected_strict=t["strict"], t1_corrected_equal=t["equal"], t1_corrected_total=t["total"],
            c4_strict=c["strict_count"], c4_equal=c["equal_count"], c4_total=c["total_rows"],
            exact_agreement=agree,
            c4_gap_strict=c["gap_row_subset_strict"], c4_gap_equal=c["gap_row_subset_equal"],
            t1_contaminated_strict=cont["strict"], t1_contaminated_equal=cont["equal"],
            contaminated_minus_c4_strict=delta_cont, contaminated_equal_matches=eq_cont,
        ))
        tag = "AGREE" if agree else "** DISAGREE **"
        extra = f"  cont_strict-{c4_bnd}_strict = {delta_cont}" if c4_bnd == "prev_row_B" else ""
        print(f"{cls:15s} {c4_bnd:10s} T1 {t['strict']:>6}/{t['equal']:<2} vs C4 "
              f"{c['strict_count']:>6}/{c['equal_count']:<2}  {tag}{extra}")

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
    w.writeheader()
    w.writerows(rows_out)

deltas_mbo = {r["event_class"]: r["contaminated_minus_c4_strict"] for r in rows_out
              if r["boundary_c4"] == "prev_row_B" and r["event_class"].startswith("mbo")}
deltas_trd = {r["event_class"]: r["contaminated_minus_c4_strict"] for r in rows_out
              if r["boundary_c4"] == "prev_row_B" and r["event_class"].startswith("trades")}
print(f"\nALL 20 (class,boundary) cells exact T1-vs-C4 agreement: {all_ok}")
print(f"contaminated-minus relation at prev_row_B: mbo classes {deltas_mbo}  trades classes {deltas_trd}")
print(f"wrote {OUT}")
