r"""N3 contradiction check.

(a) N3 predicate_check.strict_viol  vs  N1 declared_map.csv strict_count
    (side=corrected, boundary=decision_T), joined on (instrument, month, class).
(b) N3 cohort_size  vs  N1 lattice_profile.csv same_second_rows, per (instrument, month).
(c) N3 strict_viol  vs  M5 per_instrument_counts.csv (side=corrected, boundary=decision_T)
    for the two months M5 covered, 2025-01 and 2025-08.
Everything is reported raw. No reconciliation.
"""
import sys
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")
BASE = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
            r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike")
N3, N1, M5 = BASE / "n3", BASE / "n1", BASE / "m5"

n3 = pl.read_csv(N3 / "predicate_check.csv")
print(f"N3 predicate_check.csv rows = {n3.height}")

# ---- (a) vs N1 declared_map ------------------------------------------------
dm = (pl.read_csv(N1 / "declared_map.csv")
        .filter((pl.col("side") == "corrected") & (pl.col("boundary") == "decision_T")
                & pl.col("scored_flag").str.starts_with("SCORED")))
print(f"N1 declared_map corrected/decision_T SCORED rows = {dm.height}")
j = n3.join(dm.select(["instrument", "month", "class", "strict_count"]),
            on=["instrument", "month", "class"], how="full", coalesce=True)
missing_n3 = j.filter(pl.col("strict_viol").is_null())
missing_n1 = j.filter(pl.col("strict_count").is_null())
both = j.filter(pl.col("strict_viol").is_not_null() & pl.col("strict_count").is_not_null())
dis = both.filter(pl.col("strict_viol") != pl.col("strict_count"))
print(f"(a) matched cells = {both.height}; N1 cells with no N3 counterpart = {missing_n3.height}; "
      f"N3 cells with no N1 counterpart = {missing_n1.height}; DISAGREEING = {dis.height}")
if missing_n3.height: print(missing_n3)
if missing_n1.height: print(missing_n1)
if dis.height: print(dis)

# ---- (b) cohort_size vs N1 lattice_profile.same_second_rows ----------------
lp = pl.read_csv(N1 / "lattice_profile.csv").select(
    ["instrument", "month", "rows", "same_second_rows", "corrected_rows"])
c = (n3.select(["instrument", "month", "cohort_size", "corrected_rows"]).unique()
       .join(lp, on=["instrument", "month"], how="full", coalesce=True,
             suffix="_n1"))
bad = c.filter((pl.col("cohort_size") != pl.col("same_second_rows"))
               | (pl.col("corrected_rows") != pl.col("corrected_rows_n1")))
print(f"(b) instrument-months compared = {c.height}; cohort_size/corrected_rows mismatches = {bad.height}")
if bad.height: print(bad)

# ---- (c) vs M5 -------------------------------------------------------------
m5 = pl.read_csv(M5 / "per_instrument_counts.csv")
print("M5 columns:", m5.columns)
m5c = m5.filter((pl.col("side") == "corrected") & (pl.col("boundary") == "decision_T"))
print(f"M5 corrected/decision_T rows = {m5c.height}")
n3_2 = n3.filter(pl.col("month").is_in(["2025-01", "2025-08"]))
j2 = n3_2.join(m5c.select(["instrument", "month", "class",
                           pl.col("strict").alias("strict_m5")]),
               on=["instrument", "month", "class"], how="full", coalesce=True,
               suffix="_m5")
b2 = j2.filter(pl.col("strict_viol").is_not_null() & pl.col("strict_m5").is_not_null())
d2 = b2.filter(pl.col("strict_viol") != pl.col("strict_m5"))
only_m5 = j2.filter(pl.col("strict_viol").is_null())
only_n3 = j2.filter(pl.col("strict_m5").is_null())
print(f"(c) matched cells = {b2.height}; M5-only = {only_m5.height}; N3-only = {only_n3.height}; "
      f"DISAGREEING = {d2.height}")
if only_m5.height: print(only_m5)
if only_n3.height: print(only_n3.select(["instrument","month","class","strict_viol"]))
if d2.height: print(d2)

# ---- headline totals -------------------------------------------------------
print("\n=== HEADLINE ===")
print(f"scored cells                 : {n3.height}")
print(f"total strict_viol            : {int(n3['strict_viol'].sum())}")
print(f"total same_second_viol       : {int(n3['same_second_viol'].sum())}")
print(f"total exception_viol         : {int(n3['exception_viol'].sum())}")
print(f"cells with exception_viol>0  : {n3.filter(pl.col('exception_viol') > 0).height}")
print(f"cells with strict_viol>0     : {n3.filter(pl.col('strict_viol') > 0).height}")
cp = pl.read_csv(N3 / "cohort_profile.csv")
print(f"total cohort rows (per i-m)  : {int(cp['cohort_size'].sum())}")
print(f"total corrected rows         : {int(cp['corrected_rows'].sum())}")
print(f"nonmonotonic rows total      : {int(cp['nonmonotonic_rows'].sum())}")
print(f"floor_decreasing rows total  : {int(cp['floor_decreasing_rows'].sum())}")

# Converse context (NOT part of the claim): the predicate is necessary, not sufficient.
# Per class the exact non-violating cohort count is predicate_check.nonviol_in_cohort.
# Aggregated over classes we can only bound it: the per-class violating sets are not
# disjoint and their union is not computed here, so
#   cohort_size - max_over_classes(same_second_viol)
# is an UPPER BOUND on the number of cohort rows that violate in NO class, and
#   max_over_classes(same_second_viol)
# is a LOWER BOUND on the number that violate in at least one class.
conv = (n3.group_by(["instrument", "month"])
          .agg(pl.col("same_second_viol").max().alias("max_ss_viol_any_class"),
               pl.col("cohort_size").first())
          .with_columns(
              pl.col("max_ss_viol_any_class")
                .alias("LOWERBOUND_cohort_rows_violating_in_some_class"),
              (pl.col("cohort_size") - pl.col("max_ss_viol_any_class"))
                .alias("UPPERBOUND_cohort_rows_violating_in_no_class"))
          .sort(["month", "instrument"]))
conv.write_csv(N3 / "converse_by_instrument_month.csv")
print("\nconverse (cohort vs best-covered class), per instrument-month:")
with pl.Config(tbl_rows=60):
    print(conv)
