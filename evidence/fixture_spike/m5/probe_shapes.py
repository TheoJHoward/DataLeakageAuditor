"""ITEM M5 probe — cheap metadata pass before the expensive counting run.

Purpose:
  (a) parquet row counts (metadata only, no data read) for every {inst}_mbo / _trades_tagged /
      _snapshots 2025-01 file, so we know which builder MBO path applies
      (phase5_ml.py L123: `if n_rows > 50_000_000:` -> LARGE path, else SMALL path);
  (b) lattice size + inter-row spacing + per-second uniqueness of lattice stamps,
      after the builder's session filter (phase5_ml.py L185-186) with each instrument's
      own day_start_utc/day_end_utc from INST_META (L49-57);
  (c) trades schema: presence of aggressor_side and its distinct values (builder L231).
Read-only against C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed.
"""
import sys, time, json
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

PROC = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\m5")

# phase5_ml.py L49-57 INST_META (verbatim day_start_utc / day_end_utc)
SESSION = {
    "es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
    "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19),
}
ONE_S = 1_000_000_000
MONTH = "2025-01"
rows = []

for inst in ["es", "nq", "cl", "gc", "zc", "zs", "he", "le"]:
    d = PROC / inst
    ds, de = SESSION[inst]
    rec = {"inst": inst, "day_start_utc": ds, "day_end_utc": de}
    for kind in ["snapshots", "trades_tagged", "mbo"]:
        p = d / f"{inst}_{kind}_{MONTH}.parquet"
        if not p.exists():
            rec[f"{kind}_rows"] = None
            rec[f"{kind}_present"] = False
            continue
        rec[f"{kind}_present"] = True
        rec[f"{kind}_rows"] = pq.ParquetFile(str(p)).metadata.num_rows
    if rec.get("mbo_rows"):
        rec["mbo_builder_path"] = "LARGE(>50M)" if rec["mbo_rows"] > 50_000_000 else "SMALL(<=50M)"
    else:
        rec["mbo_builder_path"] = "ABSENT"

    # lattice
    t0 = time.time()
    snap = (pl.read_parquet(d / f"{inst}_snapshots_{MONTH}.parquet", columns=["timestamp"])
              .sort("timestamp")
              .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))
              .filter((pl.col("hour_utc") >= ds) & (pl.col("hour_utc") < de))
              .select("timestamp"))
    rec["lattice_rows"] = snap.height
    rec["lattice_secs_read"] = round(time.time() - t0, 2)
    rec["lattice_tz"] = str(snap.schema["timestamp"])
    ns = snap.select(pl.col("timestamp").dt.timestamp("ns").alias("ns"))
    rec["distinct_stamps"] = ns["ns"].n_unique()
    rec["distinct_seconds"] = ns.select((pl.col("ns") // ONE_S)).to_series().n_unique()
    rec["stamps_unique_per_second"] = (rec["distinct_stamps"] == rec["distinct_seconds"]
                                       == rec["lattice_rows"])
    sp = (ns.with_columns((pl.col("ns") - pl.col("ns").shift(1)).alias("d"))
            .drop_nulls().group_by("d").len().sort("len", descending=True).head(5))
    rec["top_spacings_ns"] = [(int(a), int(b)) for a, b in zip(sp["d"], sp["len"])]
    rec["n_nonzero_subsecond_spacings"] = int(
        ns.with_columns((pl.col("ns") - pl.col("ns").shift(1)).alias("d"))
          .drop_nulls().filter(pl.col("d") < ONE_S).height)

    # trades schema
    tp = d / f"{inst}_trades_tagged_{MONTH}.parquet"
    sch = pq.ParquetFile(str(tp)).schema_arrow
    rec["trades_has_aggressor_side"] = "aggressor_side" in sch.names
    col = "aggressor_side" if rec["trades_has_aggressor_side"] else "side"
    rec["trades_side_col"] = col
    vals = (pl.read_parquet(tp, columns=[col]).unique().to_series().to_list())
    rec["trades_side_values"] = sorted([str(v) for v in vals])[:10]
    tsch = pl.read_parquet_schema(tp)
    rec["trades_ts_dtype"] = str(tsch["ts_event"])
    if rec["mbo_builder_path"] != "ABSENT":
        msch = pl.read_parquet_schema(d / f"{inst}_mbo_{MONTH}.parquet")
        rec["mbo_ts_dtype"] = str(msch["ts_event"])
        rec["mbo_side_dtype"] = str(msch.get("side"))
        rec["mbo_action_dtype"] = str(msch.get("action"))
    rows.append(rec)
    print(json.dumps(rec, default=str), flush=True)

(OUT / "probe_shapes.json").write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
print("\nwrote", OUT / "probe_shapes.json")
