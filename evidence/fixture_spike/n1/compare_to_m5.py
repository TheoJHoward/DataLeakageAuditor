r"""N1 CONTRADICTION CHECK vs M5.

Two independent comparisons, both mandatory:

  (A) CELL-BY-CELL against the actual M5 artifact
      ...\scratchpad\fixture_spike\m5\per_instrument_counts.csv
      joined on (instrument, month, class, side, boundary) for months 2025-01 and 2025-08.
      Any difference in strict / equal / rows is a disagreement.

  (B) MAXIMA against the M5 numbers quoted verbatim in the N1 brief
      (corrected side, boundary=decision_T, max strict / max equal across classes).
      Reported twice: over the 10 DECLARED classes, and over the M5 CLASS SET
      (the 10 declared classes plus the LARGE-path-only 11th diagnostic class mbo_all_rows,
      which is what M5's own maxima were taken over).

NOTHING IS RECONCILED. Differences are printed raw.
"""
import sys
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

BASE = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
            r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike")
M5 = BASE / "m5" / "per_instrument_counts.csv"
N1 = BASE / "n1" / "full_map_all_boundaries.csv"
OUT = BASE / "n1"

DECLARED10 = ["trades_all", "trades_buy", "trades_sell", "trades_large",
              "mbo_all", "mbo_bid_add", "mbo_ask_add",
              "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]

# quoted verbatim from the N1 brief: inst -> {month: (strict, equal)}
QUOTED = {
    ("zc", "2025-01"): (0, 0),     ("zc", "2025-08"): (90868, 2857),
    ("zs", "2025-01"): (0, 0),     ("zs", "2025-08"): (64404, 2161),
    ("gc", "2025-01"): (37065, 1853), ("gc", "2025-08"): (42886, 1907),
    ("cl", "2025-01"): (54341, 2197), ("cl", "2025-08"): (27852, 1427),
    ("es", "2025-01"): (0, 6),     ("es", "2025-08"): (0, 6),
    ("he", "2025-01"): (0, 1),     ("he", "2025-08"): (0, 15),
    ("le", "2025-01"): (0, 1),     ("le", "2025-08"): (0, 13),
    ("nq", "2025-01"): (0, 0),     ("nq", "2025-08"): (0, 0),
}
QUOTED_ROWS = {("zc", "2025-08"): 554303}   # the one row-total quoted in the brief

m5 = (pl.read_csv(M5)
        .rename({"strict": "m5_strict", "equal": "m5_equal", "rows": "m5_rows"}))
n1 = (pl.read_csv(N1)
        .filter(pl.col("scored_flag") != "UNSCORED_FOR_LACK_OF_DATA")
        .rename({"strict_count": "n1_strict", "equal_count": "n1_equal", "rows": "n1_rows"}))

# ---------------------------------------------------------------- (A) cell-by-cell
j = m5.join(n1, on=["instrument", "month", "class", "side", "boundary"], how="full",
            coalesce=True)
missing_in_n1 = j.filter(pl.col("n1_strict").is_null())
missing_in_m5 = j.filter(pl.col("m5_strict").is_null()
                         & pl.col("month").is_in(["2025-01", "2025-08"]))
both = j.filter(pl.col("n1_strict").is_not_null() & pl.col("m5_strict").is_not_null())
diff = both.filter((pl.col("m5_strict") != pl.col("n1_strict"))
                   | (pl.col("m5_equal") != pl.col("n1_equal"))
                   | (pl.col("m5_rows") != pl.col("n1_rows")))

print("=" * 78)
print("(A) CELL-BY-CELL vs m5/per_instrument_counts.csv  (2025-01 & 2025-08)")
print(f"  M5 cells                       : {m5.height}")
print(f"  N1 cells matched to an M5 cell : {both.height}")
print(f"  M5 cells with NO N1 counterpart: {missing_in_n1.height}")
print(f"  DISAGREEING CELLS              : {diff.height}")
if missing_in_n1.height:
    print(missing_in_n1.select("instrument", "month", "class", "side", "boundary",
                               "m5_strict", "m5_equal"))
if diff.height:
    print(diff.select("instrument", "month", "class", "side", "boundary",
                      "m5_strict", "n1_strict", "m5_equal", "n1_equal",
                      "m5_rows", "n1_rows"))
    diff.write_csv(OUT / "m5_disagreements.csv")
else:
    print("  -> EXACT REPRODUCTION of every M5 cell.")

# ---------------------------------------------------------------- (B) maxima
cd = (n1.filter((pl.col("side") == "corrected") & (pl.col("boundary") == "decision_T")
                & pl.col("month").is_in(["2025-01", "2025-08"])))
mx10 = (cd.filter(pl.col("class").is_in(DECLARED10))
          .group_by("instrument", "month")
          .agg(pl.col("n1_strict").max().alias("s10"), pl.col("n1_equal").max().alias("e10"),
               pl.col("n1_rows").max().alias("rows")))
mxm5 = (cd.group_by("instrument", "month")
          .agg(pl.col("n1_strict").max().alias("sM5"), pl.col("n1_equal").max().alias("eM5")))
mx = mx10.join(mxm5, on=["instrument", "month"]).sort("instrument", "month")

print()
print("=" * 78)
print("(B) MAXIMA vs the M5 numbers QUOTED IN THE BRIEF (corrected, decision_T)")
print(f"{'inst':4} {'month':8} {'quoted':>14} {'N1 max over M5 class set':>26} "
      f"{'N1 max over declared 10':>25} {'rows':>9}  verdict")
bad = []
for r in mx.iter_rows(named=True):
    key = (r["instrument"], r["month"])
    q = QUOTED[key]
    ok_m5set = (q == (r["sM5"], r["eM5"]))
    ok_10 = (q == (r["s10"], r["e10"]))
    if ok_m5set:
        v = "MATCH (M5 class set)" + ("" if ok_10 else "; differs over declared-10 only "
                                                       "b/c M5 max used mbo_all_rows")
    else:
        v = "*** DISAGREE ***"
        bad.append((key, q, (r["sM5"], r["eM5"]), (r["s10"], r["e10"])))
    print(f"{r['instrument']:4} {r['month']:8} {str(q):>14} "
          f"{str((r['sM5'], r['eM5'])):>26} {str((r['s10'], r['e10'])):>25} "
          f"{r['rows']:>9}  {v}")
for k, v in QUOTED_ROWS.items():
    got = mx.filter((pl.col("instrument") == k[0]) & (pl.col("month") == k[1]))["rows"].item()
    print(f"  quoted row total {k}: brief={v} n1={got} "
          f"{'MATCH' if got == v else '*** DISAGREE ***'}")
    if got != v:
        bad.append((k, ("rows", v), ("rows", got), None))

print()
print(f"TOTAL QUOTED-MAXIMA DISAGREEMENTS: {len(bad)}")
print(f"TOTAL CELL-BY-CELL DISAGREEMENTS : {diff.height}")
mx.write_csv(OUT / "m5_maxima_comparison.csv")
