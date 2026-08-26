r"""ITEM N3 (GATES PHASE TWO) — MECHANISM PREDICATE VERIFICATION.

ADAPTED FROM (read-only reference)
  ...\scratchpad\fixture_spike\n1\n1_declared_map.py   (the N1 sweep checker)
which was itself adapted from m5\extend_checker.py.  Lattice construction, session
filter, join key, class definitions, builder-path selection and the strict-violation
test are COPIED VERBATIM from n1_declared_map.py so that strict_viol here must equal
N1's declared_map.csv strict_count (side=corrected, boundary=decision_T) cell for cell.

WHAT IS ADDED vs N1
  * per corrected row i (i>=1) the lattice-only predicate
        same_second_i  :=  floor(T_i, 1s) == floor(T_{i-1}, 1s)
    equivalently  floor(T_i) == wstart_i  (wstart_i is the absorbed window start).
  * per (instrument, month, class):
        strict_viol       = corrected rows with an absorbed event ts_event >  T_i
        same_second_viol  = those of them with same_second_i TRUE
        exception_viol    = those of them with same_second_i FALSE   <-- must be 0
        cohort_size       = corrected rows with same_second_i TRUE (class-independent)
        nonviol_in_cohort = cohort_size - same_second_viol           (converse context)
  * every exception row (if any) is dumped raw: lattice row index, T_i, T_{i-1},
    and the offending ts_event (the max ts_event inside the absorbed second).
  * monotonicity audit of the lattice: count of rows with T_i < T_{i-1} and with
    floor(T_i) < wstart_i.  Reported raw, never reconciled.

WHAT IS DROPPED vs N1
  * the `equal` branch (eqsets).  N3's claim concerns strict violations only, and the
    eq computation does not touch the `max per second` aggregate that strict uses.
  * the contaminated side and the prev_row_B boundary (not part of the claim).

Reads ONLY C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed  (read-only archive).
Writes ONLY under ...\scratchpad\fixture_spike\n3.
"""
import sys, time, json, traceback
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

PROC = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n3")
OUT.mkdir(parents=True, exist_ok=True)

# phase5_ml.py L49-57, verbatim day_start_utc / day_end_utc
INST_SESSION = {
    "es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
    "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19),
}
INSTS = ["es", "nq", "cl", "gc", "zc", "zs", "he", "le"]
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]

TRADE_CLASSES = ["trades_all", "trades_buy", "trades_sell", "trades_large"]
MBO_CLASSES = ["mbo_all", "mbo_bid_add", "mbo_ask_add",
               "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]

ONE_S = 1_000_000_000
BIG_PATH_THRESHOLD = 50_000_000          # phase5_ml.py L123
ENGINE = "streaming"
MAX_EXC_DUMP_PER_CELL = 200              # exceptions are expected to be zero


def floor_s(e):
    return (e // ONE_S) * ONE_S


def build_lattice(inst, month):
    """Identical to N1 build_lattice, plus lattice_idx and the same_second flag."""
    ds, de = INST_SESSION[inst]
    p = PROC / inst / f"{inst}_snapshots_{month}.parquet"
    snap = (pl.read_parquet(p, columns=["timestamp"])
              .sort("timestamp")                                              # L184
              .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))  # L185
              .filter((pl.col("hour_utc") >= ds) & (pl.col("hour_utc") < de)) # L186
              .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
    N = snap.height
    snap = snap.with_row_index("lattice_idx")
    corr = (snap.with_columns(pl.col("T").shift(1).alias("Tprev"))
                .slice(1)
                .with_columns(floor_s(pl.col("Tprev")).alias("wstart")))
    corr = corr.with_columns(
        (floor_s(pl.col("T")) == pl.col("wstart")).alias("same_second"),
        (pl.col("T") < pl.col("Tprev")).alias("nonmonotonic"),
        (floor_s(pl.col("T")) < pl.col("wstart")).alias("floor_decreasing"),
    )
    prof = {
        "rows": N,
        "corrected_rows": corr.height,
        "cohort_size": int(corr["same_second"].sum()),
        "nonmonotonic_rows": int(corr["nonmonotonic"].sum()),
        "floor_decreasing_rows": int(corr["floor_decreasing"].sum()),
    }
    return snap, corr, N, (ds, de), prof


def per_second_max(scan, classes, engine=ENGINE):
    """ONE pass over the event file -> sec -> max_<c> (max ts_event of class c in that
    second) and n_<c> (event count).  Same aggregate N1 used for the strict test."""
    exprs = []
    for c, cond in classes.items():
        exprs.append(pl.col("ns").filter(cond).max().alias(f"max_{c}"))
        exprs.append(pl.col("ns").filter(cond).len().alias(f"n_{c}"))
    q = (scan.with_columns(floor_s(pl.col("ns")).alias("sec"))
             .group_by("sec").agg(exprs))
    agg = q.collect(engine=engine)
    nev = {c: int(agg[f"n_{c}"].sum()) for c in classes}
    agg = agg.select(["sec"] + [f"max_{c}" for c in classes])
    return agg, nev


def check_classes(corr, agg, classes, inst, month, cohort_size):
    """Returns (rows_out, exception_records)."""
    rows_out, excs = [], []
    for c in classes:
        f = (corr.join(agg.select(["sec", f"max_{c}"]),
                       left_on="wstart", right_on="sec", how="left")
                 .rename({f"max_{c}": "mx"}))
        # N1's strict test, verbatim
        viol = pl.col("mx").is_not_null() & (pl.col("mx") > pl.col("T"))
        strict_viol = int(f.select(viol.sum()).item())
        same_second_viol = int(f.select((viol & pl.col("same_second")).sum()).item())
        exception_viol = int(f.select((viol & ~pl.col("same_second")).sum()).item())
        # HEADROOM on the non-cohort side: over corrected rows OUTSIDE the cohort that
        # actually absorbed >=1 event of this class, the largest value of (ts_event - T_i).
        # The claim requires this to be < 0 everywhere (i.e. no event ever overshoots T_i).
        nonss = f.filter(~pl.col("same_second") & pl.col("mx").is_not_null())
        nonss_rows_with_events = nonss.height
        max_margin_ns = (int(nonss.select((pl.col("mx") - pl.col("T")).max()).item())
                         if nonss_rows_with_events else None)
        rows_out.append(dict(
            instrument=inst, month=month, **{"class": c},
            strict_viol=strict_viol, same_second_viol=same_second_viol,
            exception_viol=exception_viol, cohort_size=cohort_size,
            nonviol_in_cohort=cohort_size - same_second_viol,
            corrected_rows=corr.height,
            noncohort_rows_with_absorbed_events=nonss_rows_with_events,
            max_ts_event_minus_T_outside_cohort_ns=max_margin_ns))
        if exception_viol:
            ex = (f.filter(viol & ~pl.col("same_second"))
                   .select(["lattice_idx", "T", "Tprev", "wstart", "mx"])
                   .head(MAX_EXC_DUMP_PER_CELL))
            for r in ex.iter_rows(named=True):
                excs.append(dict(instrument=inst, month=month, **{"class": c},
                                 lattice_row_idx=r["lattice_idx"],
                                 T_i_ns=r["T"], T_prev_ns=r["Tprev"],
                                 absorbed_window_start_ns=r["wstart"],
                                 offending_ts_event_ns=r["mx"]))
    return rows_out, excs


def run_cell(inst, month):
    t_start = time.time()
    d = PROC / inst
    rows_out, excs, log = [], [], {"inst": inst, "month": month}

    snap_p = d / f"{inst}_snapshots_{month}.parquet"
    if not snap_p.exists():
        log["status"] = "UNSCORED_NO_SNAPSHOTS"
        log["missing"] = str(snap_p)
        return rows_out, excs, {"rows": None}, log

    snap, corr, N, (ds, de), prof = build_lattice(inst, month)
    log.update(day_start_utc=ds, day_end_utc=de, **prof)
    log["lattice_secs"] = round(time.time() - t_start, 2)
    cohort = prof["cohort_size"]

    # ---------------- trades ----------------
    tp = d / f"{inst}_trades_tagged_{month}.parquet"
    if not tp.exists():
        log["trades"] = f"ABSENT {tp}"
    else:
        t0 = time.time()
        tscan = (pl.scan_parquet(tp)
                   .select(pl.col("ts_event").dt.replace_time_zone(None)
                             .dt.timestamp("ns").alias("ns"),
                           pl.col("aggressor_side"), pl.col("size")))
        is_buy = pl.col("aggressor_side").is_in(["B", "Buy", "buy"])              # L231
        tclasses = {"trades_all": pl.lit(True), "trades_buy": is_buy,
                    "trades_sell": ~is_buy, "trades_large": pl.col("size") >= 10}  # L236
        tagg, tnev = per_second_max(tscan, tclasses)
        r, e = check_classes(corr, tagg, tclasses, inst, month, cohort)
        rows_out += r; excs += e
        log["trades_secs"] = round(time.time() - t0, 2)
        log["trades_events"] = tnev
        del tagg

    # ---------------- mbo ----------------
    mp = d / f"{inst}_mbo_{month}.parquet"
    if not mp.exists():
        log["mbo"] = f"ABSENT {mp}"
    else:
        t0 = time.time()
        n_mbo = pq.ParquetFile(str(mp)).metadata.num_rows
        large = n_mbo > BIG_PATH_THRESHOLD
        log["mbo_rows"] = n_mbo
        log["mbo_builder_path"] = "LARGE" if large else "SMALL"
        mscan = (pl.scan_parquet(mp)
                   .select(pl.col("ts_event").dt.replace_time_zone(None)
                             .dt.timestamp("ns").alias("ns"),
                           pl.col("action"), pl.col("side")))
        if large:
            is_bid = pl.col("side").str.slice(0, 1) == "B"                    # L128+L130
            all_def = (pl.col("action") == "A") | (pl.col("action") == "C")   # L147
        else:
            is_bid = pl.col("side").is_in(["B", "b", "Buy", "bid"])           # L160
            all_def = pl.lit(True)                                            # L168
        isA, isC = pl.col("action") == "A", pl.col("action") == "C"
        mclasses = {"mbo_all": all_def,
                    "mbo_bid_add": isA & is_bid, "mbo_ask_add": isA & ~is_bid,
                    "mbo_bid_cancel": isC & is_bid, "mbo_ask_cancel": isC & ~is_bid,
                    "mbo_cancel_any": isC}
        if large:
            mclasses["mbo_all_rows"] = pl.lit(True)   # 11th diagnostic class, LARGE only
        magg, mnev = per_second_max(mscan, mclasses)
        r, e = check_classes(corr, magg, mclasses, inst, month, cohort)
        rows_out += r; excs += e
        log["mbo_secs"] = round(time.time() - t0, 2)
        log["mbo_events"] = mnev
        del magg

    prof["runtime_s"] = round(time.time() - t_start, 2)
    log["total_secs"] = prof["runtime_s"]
    return rows_out, excs, prof, log


def main():
    all_rows, all_exc, all_prof, all_logs = [], [], [], []
    t_all = time.time()
    projected = None
    for month in MONTHS:
        for inst in INSTS:
            t0 = time.time()
            try:
                rows_out, excs, prof, log = run_cell(inst, month)
            except Exception:
                log = {"inst": inst, "month": month, "status": "ERROR",
                       "traceback": traceback.format_exc()}
                print(json.dumps(log), flush=True)
                all_logs.append(log)
                continue
            all_rows += rows_out
            all_exc += excs
            if prof.get("rows") is not None:
                all_prof.append(dict(instrument=inst, month=month, **prof))
            all_logs.append(log)
            print(json.dumps(log, default=str), flush=True)
            if projected is None:
                one = time.time() - t0
                projected = one * len(INSTS) * len(MONTHS)
                print(f"### FIRST CELL {inst} {month} took {one:.2f}s -> "
                      f"crude projection for 48 cells = {projected:.0f}s "
                      f"({projected/60:.1f} min)", flush=True)
    print(f"### WALL TOTAL {time.time()-t_all:.1f}s", flush=True)

    df = pl.DataFrame(all_rows).select(
        ["instrument", "month", "class", "strict_viol", "same_second_viol",
         "exception_viol", "cohort_size", "nonviol_in_cohort", "corrected_rows",
         "noncohort_rows_with_absorbed_events",
         "max_ts_event_minus_T_outside_cohort_ns"])
    df.write_csv(OUT / "predicate_check.csv")

    if all_exc:
        pl.DataFrame(all_exc).write_csv(OUT / "exceptions.csv")
        print(f"### EXCEPTIONS FOUND: {len(all_exc)} rows dumped")
    else:
        (OUT / "exceptions.csv").write_text(
            "instrument,month,class,lattice_row_idx,T_i_ns,T_prev_ns,"
            "absorbed_window_start_ns,offending_ts_event_ns\n", encoding="utf-8")
        print("### NO EXCEPTIONS (empty exceptions.csv written, header only)")

    pl.DataFrame(all_prof).write_csv(OUT / "cohort_profile.csv")
    (OUT / "run_logs.json").write_text(json.dumps(all_logs, indent=2, default=str),
                                       encoding="utf-8")

    tot_s = int(df["strict_viol"].sum())
    tot_ss = int(df["same_second_viol"].sum())
    tot_ex = int(df["exception_viol"].sum())
    print(f"### TOTALS over {df.height} scored cells: strict_viol={tot_s} "
          f"same_second_viol={tot_ss} exception_viol={tot_ex}")
    nm = sum(p["nonmonotonic_rows"] for p in all_prof)
    fd = sum(p["floor_decreasing_rows"] for p in all_prof)
    print(f"### LATTICE AUDIT: nonmonotonic_rows total={nm} floor_decreasing_rows total={fd}")
    mg = df["max_ts_event_minus_T_outside_cohort_ns"].drop_nulls()
    print(f"### HEADROOM outside cohort: cells with absorbed events={mg.len()} "
          f"worst (largest) ts_event-T_i = {int(mg.max())} ns "
          f"(must be < 0 for the claim to hold); "
          f"cells with worst >= 0 = {int((mg >= 0).sum())}")


if __name__ == "__main__":
    main()
