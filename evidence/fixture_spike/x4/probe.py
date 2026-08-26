"""X4 probe: schema/tz sanity + timing on ONE v4 day file and ONE v3 month row-group slice."""
import sys, time
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")
ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
ONE_S = 1_000_000_000
DS, DE = 14, 22

# ---- lattice sanity (v3 fixture path) ----
p = ARCH / "processed" / "nq" / "nq_snapshots_2025-08.parquet"
t0 = time.time()
head = pl.read_parquet(p, n_rows=3)
print("snapshot schema timestamp dtype:", head.schema["timestamp"])
snap = (pl.read_parquet(p, columns=["timestamp"])
          .sort("timestamp")
          .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))
          .filter((pl.col("hour_utc") >= DS) & (pl.col("hour_utc") < DE))
          .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
print("lattice rows 2025-08:", snap.height, "secs", round(time.time() - t0, 2))
print("lattice T min/max:", snap["T"].min(), snap["T"].max())

# ---- v4 day file: distinct action/side values + timing of the full one-pass agg ----
d4 = ARCH / "processed" / "nq" / "v4_gapfill" / "nq_mbo_2025-08" / "nq_mbo_20250801.parquet"
t0 = time.time()
vals = (pl.scan_parquet(d4).select("action", "side")
          .group_by("action", "side").len().collect(engine="streaming"))
print("\nv4 day action/side value counts:")
print(vals.sort("len", descending=True))
print("value scan secs", round(time.time() - t0, 2))

lat = snap["T"]
is_bid = pl.col("side").str.slice(0, 1) == "B"
isA, isC = pl.col("action") == "A", pl.col("action") == "C"
classes = {
    "mbo_all": isA | isC,
    "mbo_bid_add": isA & is_bid, "mbo_ask_add": isA & ~is_bid,
    "mbo_bid_cancel": isC & is_bid, "mbo_ask_cancel": isC & ~is_bid,
    "mbo_cancel_any": isC, "mbo_all_rows": pl.lit(True),
}
exprs = [pl.col("ns").min().alias("min_all"), pl.col("ns").max().alias("max_all")]
for c, cond in classes.items():
    exprs.append(pl.col("ns").filter(cond).max().alias(f"max_{c}"))
    exprs.append(pl.col("ns").filter(cond).len().alias(f"n_{c}"))
    exprs.append(pl.col("ns").filter(cond & pl.col("is_lat")).unique().alias(f"eq_{c}"))
t0 = time.time()
q = (pl.scan_parquet(d4)
       .select(pl.col("ts_event").dt.replace_time_zone(None).dt.timestamp("ns").alias("ns"),
               pl.col("action"), pl.col("side"))
       .with_columns(pl.col("ns").is_in(lat).alias("is_lat"))
       .with_columns(((pl.col("ns") // ONE_S) * ONE_S).alias("sec"))
       .group_by("sec").agg(exprs))
agg = q.collect(engine="streaming")
print("\none-pass agg on one v4 day file: secs", round(time.time() - t0, 2),
      "distinct seconds", agg.height,
      "rows", pq.ParquetFile(str(d4)).metadata.num_rows)
print("n_mbo_all_rows sum:", agg["n_mbo_all_rows"].sum(),
      "n_mbo_all sum:", agg["n_mbo_all"].sum())
