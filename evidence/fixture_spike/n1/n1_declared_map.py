r"""ITEM N1 (GATES PHASE TWO) — FULL-WINDOW DECLARED-MAP SWEEP.

Adapted from (read-only reference)
  ...\scratchpad\fixture_spike\m5\extend_checker.py
which itself was adapted from c4\independent_checker.py.

WHAT CHANGES vs M5
  * months: 2025-01 (train) + 2025-08,09,10,11,12 (test)  -> 6 months x 8 instruments = 48 cells
  * one process, month-major loop in the mandated order 2025-01, 2025-08, 09, 10, 11, 12
  * every (instrument, month, class, side) cell is EMITTED, including UNSCORED cells with the
    exact missing input path. Nothing is silently skipped.
  * lattice_profile records rows / same_second_rows / same_second_frac / gaps_gt_60s / runtime_s
  * only boundary = decision_T goes into declared_map.csv (per the item spec); the prev_row_B
    numbers are also computed and dumped to full_map_all_boundaries.csv for completeness.

DEFINITIONS (unchanged; line numbers are in
C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\scripts\\phase5\\phase5_ml.py unless noted):

  Lattice        L180-186: read {inst}_snapshots_{month}.parquet, sort by timestamp,
                 hour_utc = timestamp.dt.hour, keep day_start_utc <= hour_utc < day_end_utc
                 from INST_META (L49-57, quoted verbatim in INST_SESSION below).
  Join key       L222 snap ts_floor = timestamp.dt.floor("1s")
                 L230 trades ts_floor = ts_event.dt.floor("1s")
                 L159 mbo    ts_floor = ts_event.dt.floor("1s")  (SMALL path)
                 L129 mbo    ts_floor = (ts // 1e9) * 1e9        (LARGE path)
  CONTAMINATED   row i absorbs its OWN second [floor(T_i), floor(T_i)+1s). All N rows measured.
  CORRECTED      row i absorbs the PREVIOUS row's second [floor(T_{i-1}), floor(T_{i-1})+1s)
                 (universal shift(1); f2/fixture.py L51). Row 0 has no content -> i>=1, N-1 rows.
  decision_T     boundary = T_i (the row's own decision time).
                 strict : an absorbed event has ts_event >  T_i   (violation under either branch)
                 equal  : an absorbed event has ts_event == T_i   (violation only under
                          ties=unavailable). "Absorbed" means the stamp lies in the window, so on
                          the corrected side equal can only fire when floor(T_i)==floor(T_{i-1}).
  prev_row_B     boundary = B_i = T_{i-1}, same absorbed window (corrected side only, supplementary).

EVENT CLASSES (the 10 declared classes)
  trades_all, trades_buy, trades_sell, trades_large,
  mbo_all, mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any
  trades_buy: is_buy = aggressor_side.isin(["B","Buy","buy"]) (L231). Parquet values are
    {BUY_AGGRESSOR, SELL_AGGRESSOR, UNKNOWN} -> matches NOTHING -> trades_buy empty and
    trades_sell (~is_buy) = all trades. Measured as built, not as intended.
  trades_large = size >= 10 (L236).
  mbo_all follows the builder path that would actually run (L123): n_rows > 50e6 -> LARGE
    (L124-150, total_events = bid_adds+ask_adds+bid_cancels+ask_cancels -> action in {A,C});
    else SMALL (L152-171, total_events = count of ALL rows).
  For LARGE-path instrument-months an ELEVENTH diagnostic class `mbo_all_rows` (= every MBO row,
  the SMALL-path definition) is also reported, exactly as M5 did, so the M5 comparison is
  apples-to-apples. It is flagged scored_flag=SCORED_DIAGNOSTIC_11TH_CLASS.

All arithmetic in integer nanoseconds, all computation in polars.
Reads ONLY C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed (read-only archive).
Writes ONLY under ...\\scratchpad\\fixture_spike\\n1.
"""
import sys, time, json, traceback
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

PROC = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n1")
OUT.mkdir(parents=True, exist_ok=True)

# phase5_ml.py L49-57, verbatim day_start_utc / day_end_utc
INST_SESSION = {
    "es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
    "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19),
}
INSTS = ["es", "nq", "cl", "gc", "zc", "zs", "he", "le"]
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]  # mandated order

TRADE_CLASSES = ["trades_all", "trades_buy", "trades_sell", "trades_large"]
MBO_CLASSES = ["mbo_all", "mbo_bid_add", "mbo_ask_add",
               "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]

ONE_S = 1_000_000_000
SIXTY_S = 60 * ONE_S
BIG_PATH_THRESHOLD = 50_000_000          # phase5_ml.py L123
ENGINE = "streaming"


def floor_s(e):
    return (e // ONE_S) * ONE_S


def build_lattice(inst, month):
    ds, de = INST_SESSION[inst]
    p = PROC / inst / f"{inst}_snapshots_{month}.parquet"
    snap = (pl.read_parquet(p, columns=["timestamp"])
              .sort("timestamp")                                              # L184
              .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))  # L185
              .filter((pl.col("hour_utc") >= ds) & (pl.col("hour_utc") < de)) # L186
              .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
    N = snap.height
    cont = snap.with_columns(floor_s(pl.col("T")).alias("wstart"))
    corr = (snap.with_columns(pl.col("T").shift(1).alias("Tprev"))
                .slice(1)
                .with_columns(floor_s(pl.col("Tprev")).alias("wstart"),
                              (pl.col("T") - pl.col("Tprev")).alias("dt")))
    corr = corr.with_columns((pl.col("dt") != ONE_S).alias("is_gap"))
    prof = {
        "rows": N,
        "corrected_rows": corr.height,
        "same_second_rows": int(corr.filter(floor_s(pl.col("T")) == pl.col("wstart")).height),
        "gaps_gt_60s": int(corr.filter(pl.col("dt") > SIXTY_S).height),
        "gap_rows_ne_1s": int(corr["is_gap"].sum()),
        "subsecond_spacing_rows": int(corr.filter(pl.col("dt") < ONE_S).height),
    }
    prof["same_second_frac"] = (prof["same_second_rows"] / prof["corrected_rows"]
                               ) if prof["corrected_rows"] else None
    return snap, cont, corr, N, (ds, de), prof


def per_second_and_eq(scan, classes, lat_stamps, engine=ENGINE):
    """ONE pass over the event file.
    Returns (agg, eqsets, nev):
      agg    : sec -> max_<c> (max ts_event of class c inside that second)
      eqsets : {class -> distinct lattice stamps carrying >=1 event of that class at that exact ns}
      nev    : {class -> number of events in the class}
    """
    exprs = []
    for c, cond in classes.items():
        exprs.append(pl.col("ns").filter(cond).max().alias(f"max_{c}"))
        exprs.append(pl.col("ns").filter(cond).len().alias(f"n_{c}"))
        exprs.append(pl.col("ns").filter(cond & pl.col("is_lat")).unique().alias(f"eq_{c}"))
    q = (scan.with_columns(pl.col("ns").is_in(lat_stamps).alias("is_lat"))
             .with_columns(floor_s(pl.col("ns")).alias("sec"))
             .group_by("sec").agg(exprs))
    agg = q.collect(engine=engine)
    eqsets, nev = {}, {}
    for c in classes:
        eqsets[c] = agg[f"eq_{c}"].explode().drop_nulls().unique()
        nev[c] = int(agg[f"n_{c}"].sum())
    agg = agg.select(["sec"] + [f"max_{c}" for c in classes])
    return agg, eqsets, nev


def count_side(frame, agg, eqsets, classes, side, n_rows, has_prev):
    """Returns list of (class, side, boundary, strict, equal, rows)."""
    out = []
    for c in classes:
        eq = eqsets[c]
        f = (frame.join(agg.select(["sec", f"max_{c}"]),
                        left_on="wstart", right_on="sec", how="left")
                  .rename({f"max_{c}": "mx"}))
        f = f.with_columns(pl.col("T").is_in(eq).alias("ev_at_T"))
        strict_T = int(f.select((pl.col("mx").is_not_null()
                                 & (pl.col("mx") > pl.col("T"))).sum()).item())
        equal_T = int(f.select((pl.col("ev_at_T")
                                & (floor_s(pl.col("T")) == pl.col("wstart"))).sum()).item())
        out.append((c, side, "decision_T", strict_T, equal_T, n_rows))
        if has_prev:
            f = f.with_columns(pl.col("Tprev").is_in(eq).alias("ev_at_Tprev"))
            strict_B = int(f.select((pl.col("mx").is_not_null()
                                     & (pl.col("mx") > pl.col("Tprev"))).sum()).item())
            equal_B = int(f.select(pl.col("ev_at_Tprev").sum()).item())
            out.append((c, side, "prev_row_B", strict_B, equal_B, n_rows))
    return out


def unscored_rows(classes, missing_path, n_corr, n_cont):
    r = []
    for c in classes:
        r.append(dict(side="corrected", **{"class": c}, boundary="decision_T",
                      strict_count=None, equal_count=None, rows=n_corr,
                      scored_flag="UNSCORED_FOR_LACK_OF_DATA", missing_path=missing_path))
        r.append(dict(side="contaminated", **{"class": c}, boundary="decision_T",
                      strict_count=None, equal_count=None, rows=n_cont,
                      scored_flag="UNSCORED_FOR_LACK_OF_DATA", missing_path=missing_path))
    return r


def run_cell(inst, month):
    t_start = time.time()
    d = PROC / inst
    rows_out, log = [], {"inst": inst, "month": month}

    snap_p = d / f"{inst}_snapshots_{month}.parquet"
    if not snap_p.exists():
        log["status"] = "UNSCORED_FOR_LACK_OF_DATA (no snapshots)"
        log["missing"] = str(snap_p)
        for c in TRADE_CLASSES + MBO_CLASSES:
            rows_out += unscored_rows([c], str(snap_p), None, None)
        prof = {"rows": None, "corrected_rows": None, "same_second_rows": None,
                "same_second_frac": None, "gaps_gt_60s": None, "gap_rows_ne_1s": None,
                "subsecond_spacing_rows": None}
        return rows_out, prof, log

    snap, cont, corr, N, (ds, de), prof = build_lattice(inst, month)
    lat_stamps = snap["T"]
    log.update(day_start_utc=ds, day_end_utc=de, **prof)
    log["lattice_secs"] = round(time.time() - t_start, 2)

    raw = []

    # ---------------- trades ----------------
    tp = d / f"{inst}_trades_tagged_{month}.parquet"
    if not tp.exists():
        log["trades"] = f"ABSENT {tp}"
        rows_out += unscored_rows(TRADE_CLASSES, str(tp), corr.height, N)
    else:
        t0 = time.time()
        tscan = (pl.scan_parquet(tp)
                   .select(pl.col("ts_event").dt.replace_time_zone(None)
                             .dt.timestamp("ns").alias("ns"),
                           pl.col("aggressor_side"), pl.col("size")))
        is_buy = pl.col("aggressor_side").is_in(["B", "Buy", "buy"])              # L231
        tclasses = {"trades_all": pl.lit(True), "trades_buy": is_buy,
                    "trades_sell": ~is_buy, "trades_large": pl.col("size") >= 10}  # L236
        tagg, teq, tnev = per_second_and_eq(tscan, tclasses, lat_stamps)
        raw += count_side(corr, tagg, teq, tclasses, "corrected", corr.height, True)
        raw += count_side(cont, tagg, teq, tclasses, "contaminated", N, False)
        log["trades_secs"] = round(time.time() - t0, 2)
        log["trades_events"] = tnev
        del tagg, teq

    # ---------------- mbo ----------------
    mp = d / f"{inst}_mbo_{month}.parquet"
    if not mp.exists():
        log["mbo"] = f"ABSENT {mp}"
        rows_out += unscored_rows(MBO_CLASSES, str(mp), corr.height, N)
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
            is_bid = pl.col("side").str.slice(0, 1) == "B"                    # L128+L130 ('U1')
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
            mclasses["mbo_all_rows"] = pl.lit(True)   # 11th diagnostic class, LARGE path only
        magg, meq, mnev = per_second_and_eq(mscan, mclasses, lat_stamps)
        raw += count_side(corr, magg, meq, mclasses, "corrected", corr.height, True)
        raw += count_side(cont, magg, meq, mclasses, "contaminated", N, False)
        log["mbo_secs"] = round(time.time() - t0, 2)
        log["mbo_events"] = mnev
        del magg, meq

    for (c, side, boundary, strict, equal, nrows) in raw:
        rows_out.append(dict(side=side, **{"class": c}, boundary=boundary,
                             strict_count=strict, equal_count=equal, rows=nrows,
                             scored_flag=("SCORED_DIAGNOSTIC_11TH_CLASS"
                                          if c == "mbo_all_rows" else "SCORED"),
                             missing_path=None))

    prof["runtime_s"] = round(time.time() - t_start, 2)
    log["total_secs"] = prof["runtime_s"]
    return rows_out, prof, log


def main():
    all_rows, all_prof, all_logs = [], [], []
    t_all = time.time()
    projected = None
    for month in MONTHS:
        for inst in INSTS:
            t0 = time.time()
            try:
                rows_out, prof, log = run_cell(inst, month)
            except Exception:
                log = {"inst": inst, "month": month, "status": "ERROR",
                       "traceback": traceback.format_exc()}
                print(json.dumps(log), flush=True)
                all_logs.append(log)
                continue
            for r in rows_out:
                all_rows.append(dict(instrument=inst, month=month, **r))
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

    df = pl.DataFrame(all_rows, schema={
        "instrument": pl.Utf8, "month": pl.Utf8, "side": pl.Utf8, "class": pl.Utf8,
        "boundary": pl.Utf8, "strict_count": pl.Int64, "equal_count": pl.Int64,
        "rows": pl.Int64, "scored_flag": pl.Utf8, "missing_path": pl.Utf8})
    df = df.select(["side", "instrument", "month", "class", "boundary",
                    "strict_count", "equal_count", "rows", "scored_flag", "missing_path"])
    df.write_csv(OUT / "full_map_all_boundaries.csv")
    df.filter(pl.col("boundary") == "decision_T").write_csv(OUT / "declared_map.csv")

    pf = pl.DataFrame(all_prof).select(
        ["instrument", "month", "rows", "same_second_rows", "same_second_frac",
         "gaps_gt_60s", "runtime_s", "corrected_rows", "gap_rows_ne_1s",
         "subsecond_spacing_rows"])
    pf.write_csv(OUT / "lattice_profile.csv")
    (OUT / "run_logs.json").write_text(json.dumps(all_logs, indent=2, default=str),
                                       encoding="utf-8")
    print("wrote", OUT / "declared_map.csv", df.height, "rows total;",
          df.filter(pl.col("boundary") == "decision_T").height, "decision_T rows")


if __name__ == "__main__":
    main()
