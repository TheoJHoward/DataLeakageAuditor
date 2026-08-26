"""ITEM N2 (c) — SPACING QUESTION.

Measure, on the actual lattices, where the same-second adjacent pairs sit.
A "same-second pair" is (row i-1, row i) with floor(T_{i-1},1s) == floor(T_i,1s).

Two views per file:
  FULL      = every row of the month parquet (sorted by timestamp), no hour filter.
              This is the view in which process_mbo.py reconstruct_day's per-day
              structure (day edges, >60 s gap re-anchors) is visible.
  FILTERED  = the fixture lattice: hour_utc in [day_start_utc, day_end_utc).

Classification of each same-second pair (row i-1 -> row i), on the FULL view:
  day_edge_last      : row i is the LAST row of its UTC calendar date
                       (= process_mbo.py L365-368 final-snapshot stamp ts_events[-1])
  gap_adjacent       : the pair sits immediately next to a > 60 s spacing
                       (T_i - T_{i-1} > 60s is impossible for a same-second pair,
                        so this tests T_{i+1}-T_i > 60s or T_{i-1}-T_{i-2} > 60s)
  elsewhere          : neither
Writes CSVs + a text log under the n2 directory.
"""
import io, json, sys, time
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude"
           r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n2")
ONE_S = 1_000_000_000
SIXTY_S = 60 * ONE_S
INST_SESSION = {"es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
                "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19)}


def load(path, inst, filtered):
    ds, de = INST_SESSION[inst]
    s = pl.read_parquet(path, columns=["timestamp"]).sort("timestamp")
    if filtered:
        s = (s.with_columns(pl.col("timestamp").dt.hour().alias("h"))
              .filter((pl.col("h") >= ds) & (pl.col("h") < de)))
    return s.select(
        pl.col("timestamp").dt.timestamp("ns").alias("T"),
        pl.col("timestamp").dt.date().alias("d"),
        pl.col("timestamp").dt.hour().alias("hour"),
    )


def analyse(path, inst, month, view, filtered, rows_out, pairs_out):
    lat = load(path, inst, filtered)
    N = lat.height
    lat = lat.with_columns(pl.arange(0, N).alias("i"))
    # last / first row of each UTC calendar date
    edges = lat.group_by("d").agg(pl.col("i").max().alias("i_last"), pl.col("i").min().alias("i_first"))
    last_ix = set(edges["i_last"].to_list())
    first_ix = set(edges["i_first"].to_list())
    d = lat.with_columns(
        pl.col("T").shift(1).alias("Tprev"),
        pl.col("T").shift(-1).alias("Tnext"),
        pl.col("T").shift(2).alias("Tprev2"),
    ).slice(1)
    d = d.with_columns(
        (pl.col("T") - pl.col("Tprev")).alias("dt"),
        ((pl.col("T") // ONE_S) == (pl.col("Tprev") // ONE_S)).alias("same_sec"),
    )
    ss = d.filter(pl.col("same_sec"))
    n_ss = ss.height
    ss = ss.with_columns(
        pl.col("i").is_in(list(last_ix)).alias("row_is_day_last"),
        (pl.col("i") - 1).is_in(list(first_ix)).alias("prev_is_day_first"),
        ((pl.col("Tnext") - pl.col("T")) > SIXTY_S).fill_null(False).alias("gap_after"),
        ((pl.col("Tprev") - pl.col("Tprev2")) > SIXTY_S).fill_null(False).alias("gap_before"),
    )
    n_day_last = int(ss.select(pl.col("row_is_day_last").sum()).item()) if n_ss else 0
    n_gap_adj = int(ss.select((pl.col("gap_after") | pl.col("gap_before")).sum()).item()) if n_ss else 0
    n_either = int(ss.select((pl.col("row_is_day_last") | pl.col("gap_after")
                              | pl.col("gap_before")).sum()).item()) if n_ss else 0
    n_else = n_ss - n_either
    n_days = lat["d"].n_unique()

    # spacing histogram buckets
    hist = {}
    if d.height:
        hist = {
            "dt_eq_0ns": int(d.select((pl.col("dt") == 0).sum()).item()),
            "dt_lt_1ms": int(d.select(((pl.col("dt") > 0) & (pl.col("dt") < 1_000_000)).sum()).item()),
            "dt_1ms_to_100ms": int(d.select(((pl.col("dt") >= 1_000_000) & (pl.col("dt") < 100_000_000)).sum()).item()),
            "dt_100ms_to_1s": int(d.select(((pl.col("dt") >= 100_000_000) & (pl.col("dt") < ONE_S)).sum()).item()),
            "dt_eq_1s": int(d.select((pl.col("dt") == ONE_S).sum()).item()),
            "dt_1s_to_60s": int(d.select(((pl.col("dt") > ONE_S) & (pl.col("dt") <= SIXTY_S)).sum()).item()),
            "dt_gt_60s": int(d.select((pl.col("dt") > SIXTY_S).sum()).item()),
        }
    rows_out.append(dict(instrument=inst, month=month, view=view, path=str(path),
                         rows=N, days=n_days, same_second_pairs=n_ss,
                         ss_day_last_row=n_day_last, ss_gap_adjacent=n_gap_adj,
                         ss_day_last_or_gap=n_either, ss_elsewhere=n_else, **hist))
    # per-hour distribution of same-second pairs (full view only)
    if n_ss:
        ph = ss.group_by("hour").len().sort("hour")
        for r in ph.iter_rows():
            pairs_out.append(dict(instrument=inst, month=month, view=view, hour_utc=r[0], same_second_pairs=r[1]))
    return rows_out[-1]


def main():
    rows_out, pairs_out = [], []
    targets = [("zc", "2025-01"), ("zc", "2025-08"), ("zc", "2025-11"),
               ("zs", "2025-01"), ("zs", "2025-08"),
               ("gc", "2025-01"), ("gc", "2025-08"),
               ("cl", "2025-01"), ("es", "2025-01"), ("es", "2025-08"),
               ("he", "2025-08"), ("le", "2025-08")]
    for inst, month in targets:
        p = ARCH / "processed" / inst / f"{inst}_snapshots_{month}.parquet"
        for view, filt in (("FULL_v3_pregapfill", False), ("FILTERED_v3_pregapfill", True)):
            r = analyse(p, inst, month, view, filt, rows_out, pairs_out)
            print(json.dumps(r, default=str), flush=True)
    # the v4 gapfill counterpart, for contrast, for zc
    for inst, month in [("zc", "2025-01"), ("zc", "2025-08"), ("zs", "2025-08"), ("gc", "2025-01")]:
        p = ARCH / "processed" / inst / "v4_gapfill" / f"{inst}_snapshots_{month}.parquet"
        for view, filt in (("FULL_v4_gapfill", False), ("FILTERED_v4_gapfill", True)):
            r = analyse(p, inst, month, view, filt, rows_out, pairs_out)
            print(json.dumps(r, default=str), flush=True)

    pl.DataFrame(rows_out).write_csv(OUT / "spacing_classification.csv")
    if pairs_out:
        pl.DataFrame(pairs_out).write_csv(OUT / "spacing_by_hour.csv")
    print("wrote spacing_classification.csv / spacing_by_hour.csv")


if __name__ == "__main__":
    main()
