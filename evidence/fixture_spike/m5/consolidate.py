"""ITEM M5 — consolidate per-instrument runs into the artifact CSVs + runtime log."""
import sys, json, glob, subprocess
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).parent
ORDER = {i: n for n, i in enumerate(["es", "nq", "cl", "gc", "zc", "zs", "he", "le"])}
CLS = {c: n for n, c in enumerate(
    ["trades_all", "trades_buy", "trades_sell", "trades_large",
     "mbo_all", "mbo_all_rows", "mbo_bid_add", "mbo_ask_add",
     "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"])}
SIDE = {"corrected": 0, "contaminated": 1}
BND = {"decision_T": 0, "prev_row_B": 1}

df = pl.concat([pl.read_csv(f) for f in sorted(glob.glob(str(OUT / "counts_*.csv")))])
df = (df.with_columns(pl.col("instrument").replace_strict(ORDER, return_dtype=pl.Int32).alias("_i"),
                      pl.col("class").replace_strict(CLS, return_dtype=pl.Int32).alias("_c"),
                      pl.col("side").replace_strict(SIDE, return_dtype=pl.Int32).alias("_s"),
                      pl.col("boundary").replace_strict(BND, return_dtype=pl.Int32).alias("_b"))
        .sort(["_i", "month", "_s", "_b", "_c"]))

# artifact: exactly the 8 requested columns
df.select("instrument", "month", "class", "side", "boundary", "strict", "equal", "rows") \
  .write_csv(OUT / "per_instrument_counts.csv")
# companion: adds the re-anchor gap-row subset (corrected/decision_T only)
df.select("instrument", "month", "class", "side", "boundary", "strict", "equal", "rows",
          "gap_strict", "gap_equal").write_csv(OUT / "per_instrument_counts_detail.csv")

# runtime + lattice-structure log
logs = []
for f in sorted(glob.glob(str(OUT / "log_*.json"))):
    logs.append(json.loads(Path(f).read_text(encoding="utf-8")))
lg = pl.DataFrame(logs, infer_schema_length=None)
keep = ["inst", "month", "day_start_utc", "day_end_utc", "lattice_rows", "corrected_rows",
        "contaminated_rows", "gap_rows", "subsecond_spacing_rows", "same_second_as_prev_rows",
        "mbo_rows", "mbo_builder_path", "trades_secs", "mbo_secs", "total_secs",
        "corrected_decisionT_nonzero_cells"]
keep = [k for k in keep if k in lg.columns]
lg = (lg.select(keep)
        .with_columns(pl.col("inst").replace_strict(ORDER, return_dtype=pl.Int32).alias("_i"))
        .sort(["_i", "month"]).drop("_i"))
lg.write_csv(OUT / "runtime_and_lattice_log.csv")

d = df.filter((pl.col("side") == "corrected") & (pl.col("boundary") == "decision_T"))
summ = (d.group_by("instrument", "month")
         .agg(pl.col("strict").max().alias("max_strict"), pl.col("equal").max().alias("max_equal"),
              ((pl.col("strict") > 0) | (pl.col("equal") > 0)).sum().alias("nonzero_cells"),
              pl.len().alias("cells"), pl.col("rows").max().alias("rows"))
         .join(lg.select(pl.col("inst").alias("instrument"), "month", "same_second_as_prev_rows"),
               on=["instrument", "month"])
         .with_columns(pl.col("instrument").replace_strict(ORDER, return_dtype=pl.Int32).alias("_i"))
         .sort(["month", "_i"]).drop("_i"))
summ.write_csv(OUT / "corrected_decisionT_summary.csv")

pl.Config.set_tbl_rows(60); pl.Config.set_tbl_width_chars(220)
print("=== CORRECTED / decision_T summary (the headline) ===")
print(summ)
print("\nartifact rows:", df.height, "->", OUT / "per_instrument_counts.csv")
print("total wall-clock compute (sum of total_secs):", round(float(lg["total_secs"].sum()), 2), "s")
