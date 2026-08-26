"""ITEM N2 (c) — the measured mechanism behind same-second rows.

process_mbo.py L584-590 builds the month snapshot parquet as
    snap_files = sorted(tmp_dir.glob("snap_*.parquet"))
    master_snap = pa.concat_tables([pq.read_table(f) for f in snap_files])
i.e. a plain CONCATENATION in FILENAME order, with NO global sort and NO de-duplication.
Each snap_<date>.parquet is one reconstruct_day() output.

So the month file's NATIVE row order decomposes into monotone runs ("blocks"), one per
per-day snapshot file (or fewer, when consecutive files happen to be disjoint+increasing).
If the per-day chunks cover DISJOINT wall-clock spans the month file is globally sorted and
every second appears once. If the per-day chunks OVERLAP, the same wall-clock second is
reconstructed more than once and the sorted lattice carries multiple rows per second.

This script measures, per fixture instrument-month (generation v3 pre-gapfill, the path the
builder and the M5/N1 sweep read):
  native_blocks          number of monotone runs in native row order
  overlapping_block_pairs number of consecutive block pairs whose spans overlap
  max_rows_per_second     max multiplicity of any single ns timestamp (FULL view)
  dup_timestamps          number of distinct ns timestamps carried by >1 row (FULL view)
  filt_max_rows_per_sec   max rows sharing one wall-clock second in the FILTERED lattice
  filt_rows / filt_secs   filtered lattice rows and distinct seconds
"""
import sys
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude"
           r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n2")
ONE_S = 1_000_000_000
INST_SESSION = {"es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
                "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19)}
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]


def run(path, inst, month, gen):
    s = pl.read_parquet(path, columns=["timestamp"])            # NATIVE order
    n = s.height
    t = (s.select(pl.col("timestamp").dt.timestamp("ns").alias("T"))
          .with_columns(pl.arange(0, n).alias("i")))
    t = t.with_columns((pl.col("T") < pl.col("T").shift(1)).fill_null(False).cum_sum().alias("blk"))
    g = (t.group_by("blk").agg(pl.len().alias("n"), pl.col("T").min().alias("t0"),
                               pl.col("T").max().alias("t1"), pl.col("i").min().alias("i0"))
          .sort("i0"))
    nb = g.height
    t0 = g["t0"].to_list()
    t1 = g["t1"].to_list()
    overlaps = sum(1 for k in range(1, nb) if t0[k] <= t1[k - 1])
    vc = t.group_by("T").len()
    max_mult = int(vc["len"].max())
    dup_ts = int((vc["len"] > 1).sum())

    ds, de = INST_SESSION[inst]
    lat = (s.sort("timestamp")
            .with_columns(pl.col("timestamp").dt.hour().alias("h"))
            .filter((pl.col("h") >= ds) & (pl.col("h") < de))
            .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
    fr = lat.height
    persec = lat.group_by(((pl.col("T") // ONE_S)).alias("s")).len()
    fsec = persec.height
    fmax = int(persec["len"].max()) if fsec else 0
    return dict(instrument=inst, month=month, generation=gen, path=str(path),
                total_rows=n, native_blocks=nb, overlapping_block_pairs=overlaps,
                max_rows_per_timestamp=max_mult, duplicate_timestamps=dup_ts,
                filtered_rows=fr, filtered_distinct_seconds=fsec,
                filtered_max_rows_per_second=fmax,
                filtered_excess_rows=fr - fsec)


def main():
    rows = []
    for inst in ["cl", "es", "gc", "he", "le", "nq", "zc", "zs"]:
        for month in MONTHS:
            p = ARCH / "processed" / inst / f"{inst}_snapshots_{month}.parquet"
            r = run(p, inst, month, "v3_pre_gapfill_FIXTURE_PATH")
            rows.append(r)
            print(f"{inst} {month} v3   blocks={r['native_blocks']:>3} "
                  f"ovl_pairs={r['overlapping_block_pairs']:>3} "
                  f"maxmult={r['max_rows_per_timestamp']} dupTS={r['duplicate_timestamps']:>7} "
                  f"filt={r['filtered_rows']:>7} secs={r['filtered_distinct_seconds']:>7} "
                  f"excess={r['filtered_excess_rows']:>7}", flush=True)
    # v4 counterpart where it exists
    for inst in ["cl", "gc", "nq", "zc", "zs", "es"]:
        sub = "v4_morning_chunk" if inst == "es" else "v4_gapfill"
        for month in MONTHS:
            p = ARCH / "processed" / inst / sub / f"{inst}_snapshots_{month}.parquet"
            if not p.exists():
                continue
            r = run(p, inst, month, f"v4_{sub}")
            rows.append(r)
            print(f"{inst} {month} v4   blocks={r['native_blocks']:>3} "
                  f"ovl_pairs={r['overlapping_block_pairs']:>3} "
                  f"maxmult={r['max_rows_per_timestamp']} dupTS={r['duplicate_timestamps']:>7} "
                  f"filt={r['filtered_rows']:>7} secs={r['filtered_distinct_seconds']:>7} "
                  f"excess={r['filtered_excess_rows']:>7}", flush=True)
    pl.DataFrame(rows).write_csv(OUT / "block_overlap.csv")
    print("wrote block_overlap.csv")


if __name__ == "__main__":
    main()
