r"""N1 summary tables: corrected-side and contaminated-side maxima per instrument-month,
plus the coverage / unscored ledger. Reads only n1/declared_map.csv and n1/lattice_profile.csv.
"""
import sys
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")
pl.Config.set_tbl_rows(200); pl.Config.set_tbl_cols(30); pl.Config.set_tbl_width_chars(250)

OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n1")
DECLARED10 = ["trades_all", "trades_buy", "trades_sell", "trades_large",
              "mbo_all", "mbo_bid_add", "mbo_ask_add",
              "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]

d = pl.read_csv(OUT / "declared_map.csv")
scored = d.filter(pl.col("scored_flag") != "UNSCORED_FOR_LACK_OF_DATA")

for side in ["corrected", "contaminated"]:
    s = scored.filter((pl.col("side") == side) & pl.col("class").is_in(DECLARED10))
    mx = (s.group_by("instrument", "month")
            .agg(pl.col("strict_count").max().alias("max_strict"),
                 pl.col("equal_count").max().alias("max_equal"),
                 pl.col("rows").max().alias("rows"),
                 pl.col("class").filter(pl.col("strict_count") ==
                                        pl.col("strict_count").max()).first().alias("argmax_strict"),
                 pl.col("class").filter(pl.col("equal_count") ==
                                        pl.col("equal_count").max()).first().alias("argmax_equal"),
                 (pl.col("strict_count") > 0).sum().alias("classes_strict_gt0"),
                 (pl.col("equal_count") > 0).sum().alias("classes_equal_gt0"),
                 pl.len().alias("classes_scored"))
            .sort("instrument", "month"))
    mx = mx.with_columns((pl.col("max_strict") / pl.col("rows")).round(6).alias("max_strict_frac"))
    print("=" * 120)
    print(f"{side.upper()} SIDE — boundary=decision_T — max over the 10 declared classes")
    print(mx)
    mx.write_csv(OUT / f"summary_{side}.csv")

print("=" * 120)
print("UNSCORED LEDGER (cells with no input parquet)")
u = d.filter(pl.col("scored_flag") == "UNSCORED_FOR_LACK_OF_DATA")
print(f"  total unscored (side x inst x month x class) rows in declared_map.csv: {u.height}")
led = (u.group_by("instrument", "month", "missing_path")
         .agg(pl.col("class").unique().sort().str.join(",").alias("classes"),
              pl.len().alias("n_cells"))
         .sort("instrument", "month"))
print(led)
led.write_csv(OUT / "unscored_ledger.csv")

print("=" * 120)
print("LATTICE PROFILE")
print(pl.read_csv(OUT / "lattice_profile.csv"))
