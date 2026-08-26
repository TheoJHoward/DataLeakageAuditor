"""ITEM M5 verification — localise the corrected-side violating rows.

For each instrument with a nonzero corrected/decision_T count, check the claim that EVERY
violating row is a row whose own second equals the previous row's second, i.e.
floor(T_i) == floor(T_{i-1}), so the shift(1) window [floor(T_{i-1}), floor(T_{i-1})+1s)
IS the row's own second and the shift absorbs nothing. Also dump concrete example rows
with verbatim nanosecond timestamps.

Read-only against the archive. Class used: mbo_all (builder-path definition) and trades_all.
"""
import sys, json
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from extend_checker import (PROC, INST_SESSION, ONE_S, BIG_PATH_THRESHOLD,
                            build_lattice, floor_s)

OUT = Path(__file__).parent
MONTH = "2025-01"
out = {}

for inst in ["es", "cl", "gc", "he", "le", "nq", "zc", "zs"]:
    snap, cont, corr, N, (ds, de) = build_lattice(inst, MONTH)
    lat_stamps = snap["T"]
    rec = {"inst": inst, "corrected_rows": corr.height,
           "rows_same_second_as_prev": int(corr.filter(floor_s(pl.col("T")) == pl.col("wstart")).height)}

    srcs = {}
    tp = PROC / inst / f"{inst}_trades_tagged_{MONTH}.parquet"
    srcs["trades_all"] = (pl.scan_parquet(tp).select(
        pl.col("ts_event").dt.replace_time_zone(None).dt.timestamp("ns").alias("ns")), pl.lit(True))
    mp = PROC / inst / f"{inst}_mbo_{MONTH}.parquet"
    if mp.exists():
        large = pq.ParquetFile(str(mp)).metadata.num_rows > BIG_PATH_THRESHOLD
        cond = ((pl.col("action") == "A") | (pl.col("action") == "C")) if large else pl.lit(True)
        srcs["mbo_all"] = (pl.scan_parquet(mp).select(
            pl.col("ts_event").dt.replace_time_zone(None).dt.timestamp("ns").alias("ns"),
            pl.col("action")), cond)

    for cname, (scan, cond) in srcs.items():
        agg = (scan.filter(cond).with_columns(floor_s(pl.col("ns")).alias("sec"))
                   .group_by("sec").agg(pl.col("ns").max().alias("mx"),
                                        pl.col("ns").filter(pl.col("ns").is_in(lat_stamps))
                                          .unique().alias("eq"))
                   .collect(engine="streaming"))
        eq = agg["eq"].explode().drop_nulls().unique()
        f = (corr.join(agg.select("sec", "mx"), left_on="wstart", right_on="sec", how="left")
                 .with_columns(pl.col("T").is_in(eq).alias("ev_at_T"))
                 .with_columns((floor_s(pl.col("T")) == pl.col("wstart")).alias("same_sec"))
                 .with_columns((pl.col("mx").is_not_null() & (pl.col("mx") > pl.col("T"))).alias("v_strict"),
                               (pl.col("ev_at_T") & (floor_s(pl.col("T")) == pl.col("wstart"))).alias("v_equal")))
        viol = f.filter(pl.col("v_strict") | pl.col("v_equal"))
        k = f"{cname}"
        rec[k] = {
            "violating_rows": viol.height,
            "strict": int(f["v_strict"].sum()), "equal": int(f["v_equal"].sum()),
            "all_violating_rows_have_same_second_as_prev": bool(viol["same_sec"].all()) if viol.height else None,
            "violating_rows_NOT_same_second": int(viol.filter(~pl.col("same_sec")).height),
            "strict_violations_as_frac_of_same_second_rows":
                (round(int(f["v_strict"].sum()) / rec["rows_same_second_as_prev"], 4)
                 if rec["rows_same_second_as_prev"] else None),
        }
        ex = viol.head(3).select("T", "Tprev", "wstart", "mx", "v_strict", "v_equal")
        rec[k]["examples"] = [
            {"T_i_ns": r["T"], "T_prev_ns": r["Tprev"],
             "T_i_utc": str(pl.Series([r["T"]]).cast(pl.Datetime("ns"))[0]),
             "T_prev_utc": str(pl.Series([r["Tprev"]]).cast(pl.Datetime("ns"))[0]),
             "gap_ns": r["T"] - r["Tprev"],
             "window_start_utc": str(pl.Series([r["wstart"]]).cast(pl.Datetime("ns"))[0]),
             "max_event_in_window_utc": (str(pl.Series([r["mx"]]).cast(pl.Datetime("ns"))[0])
                                         if r["mx"] is not None else None),
             "max_event_minus_T_i_ns": (r["mx"] - r["T"]) if r["mx"] is not None else None,
             "strict": r["v_strict"], "equal": r["v_equal"]}
            for r in ex.to_dicts()]
    out[inst] = rec
    print(json.dumps(rec, indent=2, default=str), flush=True)

(OUT / "verify_violating_rows.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
print("\nwrote", OUT / "verify_violating_rows.json")
