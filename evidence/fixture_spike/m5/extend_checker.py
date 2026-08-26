"""ITEM M5 — EXTEND the corrected-side zero across instruments.

Adapted from c4/independent_checker.py (read-only reference, ZC-only) to run PER INSTRUMENT
over the 8 instrument lattices, using each instrument's own session hours.

DEFINITIONS (unchanged from C4; source line numbers are in
C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\scripts\\phase5\\phase5_ml.py unless noted):

  Lattice          L180-186: read {inst}_snapshots_{month}.parquet, sort_values("timestamp"),
                   hour_utc = timestamp.dt.hour, keep ds <= hour_utc < de, with
                   (ds, de) = INST_META[inst]["day_start_utc"/"day_end_utc"]  (L49-57).
  Join key         L222 snap["ts_floor"] = timestamp.dt.floor("1s")
                   L230 trades["ts_floor"] = ts_event.dt.floor("1s")
                   L159 mbo    ["ts_floor"] = ts_event.dt.floor("1s")   (SMALL path)
                   L129 mbo    ts_floor = (ts // 1e9) * 1e9             (LARGE path)
  CORRECTED side   feature content of row i = joined aggregates of row i-1's second
                   [floor(T_{i-1}), floor(T_{i-1})+1s)  (universal shift(1),
                   f2/fixture.py L51: snap[feature_cols] = snap[feature_cols].shift(1)).
                   Row 0 has no content -> measured rows are i >= 1  (N-1 rows).
  CONTAMINATED side  feature content of row i = its OWN second [floor(T_i), floor(T_i)+1s).
                   All N rows measured.
  decision_T       boundary = T_i (the row's own stamp). strict: event ts_event > T_i inside the
                   absorbed window; equal: ts_event == T_i inside the absorbed window.
  prev_row_B       boundary = B_i = T_{i-1}, same absorbed window (corrected side only).

MBO CLASS DEFINITIONS FOLLOW THE BUILDER PATH THAT WOULD ACTUALLY RUN (L123):
  n_rows > 50_000_000 -> LARGE path (L124-150): side cast to 'U1' (FIRST CHARACTER),
      is_bid = (sid == 'B'); total_events = bid_adds+ask_adds+bid_cancels+ask_cancels (L147),
      i.e. only action in {A, C} contributes -> mbo_all := (action=="A") | (action=="C").
  else               -> SMALL path (L152-171): is_bid = side.isin(["B","b","Buy","bid"]) (L160);
      total_events = ("action","count") (L168) = ALL rows -> mbo_all := every MBO row.
  For LARGE-path instruments an extra class `mbo_all_rows` (= every MBO row, the SMALL-path
  definition) is also reported so the two paths stay comparable.

Trades classes (identical for all instruments, L231-236):
  is_buy = aggressor_side.isin(["B","Buy","buy"]) — parquet values are
  {BUY_AGGRESSOR, SELL_AGGRESSOR, UNKNOWN}, so this matches NOTHING: trades_buy is EMPTY and
  trades_sell (~is_buy) is ALL trades. Measured as built, not as intended.
  trades_large = (size >= 10)  (L236).

All arithmetic in integer nanoseconds. All computation in polars.
Reads ONLY C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed (read-only archive).
"""
import sys, time, argparse, json
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

PROC = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\m5")

# phase5_ml.py L49-57, verbatim day_start_utc / day_end_utc
INST_SESSION = {
    "es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
    "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19),
}
ONE_S = 1_000_000_000
BIG_PATH_THRESHOLD = 50_000_000          # phase5_ml.py L123


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
    # contaminated frame: every row, window = its own second
    cont = snap.with_columns(floor_s(pl.col("T")).alias("wstart"))
    # corrected frame: rows i>=1, window = second of T_{i-1}
    corr = (snap.with_columns(pl.col("T").shift(1).alias("Tprev"))
                .slice(1)
                .with_columns(floor_s(pl.col("Tprev")).alias("wstart"),
                              ((pl.col("T") - pl.col("Tprev")) != ONE_S).alias("is_gap")))
    return snap, cont, corr, N, (ds, de)


def per_second_and_eq(scan, classes, lat_stamps, engine):
    """ONE pass over the event file.

    Returns (agg, eqsets, nev):
      agg    : DataFrame sec -> max_<c> (max ts_event of class c inside that second) and n_<c>
      eqsets : {class -> set of lattice stamps carrying >=1 event of that class at that exact ns}
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
        s = agg[f"eq_{c}"].explode().drop_nulls().unique()
        eqsets[c] = s
        nev[c] = int(agg[f"n_{c}"].sum())
    agg = agg.select(["sec"] + [f"max_{c}" for c in classes])
    return agg, eqsets, nev


def count_side(frame, agg, eqsets, classes, side, n_rows, has_prev):
    out = []
    for c in classes:
        eq = eqsets[c]
        f = (frame.join(agg.select(["sec", f"max_{c}"]), left_on="wstart", right_on="sec", how="left")
                  .rename({f"max_{c}": "mx"}))
        f = f.with_columns(pl.col("T").is_in(eq).alias("ev_at_T"))
        if has_prev:
            f = f.with_columns(pl.col("Tprev").is_in(eq).alias("ev_at_Tprev"))
        # boundary = decision time T_i
        strict_T = int(f.select((pl.col("mx").is_not_null() & (pl.col("mx") > pl.col("T"))).sum()).item())
        # an event exactly at T_i counts only if T_i lies inside the absorbed window
        equal_T = int(f.select((pl.col("ev_at_T") & (floor_s(pl.col("T")) == pl.col("wstart"))).sum()).item())
        out.append((c, side, "decision_T", strict_T, equal_T, n_rows))
        if has_prev:
            strict_B = int(f.select((pl.col("mx").is_not_null() & (pl.col("mx") > pl.col("Tprev"))).sum()).item())
            equal_B = int(f.select(pl.col("ev_at_Tprev").sum()).item())
            out.append((c, side, "prev_row_B", strict_B, equal_B, n_rows))
            # gap-row subset (spacing != 1s) at decision_T, recorded in the detail file
            g = f.filter(pl.col("is_gap"))
            gs = int(g.select((pl.col("mx").is_not_null() & (pl.col("mx") > pl.col("T"))).sum()).item())
            ge = int(g.select((pl.col("ev_at_T") & (floor_s(pl.col("T")) == pl.col("wstart"))).sum()).item())
            out[-2] = out[-2] + (gs, ge)
            out[-1] = out[-1] + (None, None)
        else:
            out[-1] = out[-1] + (None, None)
    return out


def run(inst, month, engine="streaming"):
    t_start = time.time()
    d = PROC / inst
    snap, cont, corr, N, (ds, de) = build_lattice(inst, month)
    lat_stamps = snap["T"]
    log = {"inst": inst, "month": month, "day_start_utc": ds, "day_end_utc": de,
           "lattice_rows": N, "corrected_rows": corr.height, "contaminated_rows": N,
           "gap_rows": int(corr["is_gap"].sum()),
           "subsecond_spacing_rows": int(corr.filter((pl.col("T") - pl.col("Tprev")) < ONE_S).height),
           "same_second_as_prev_rows": int(corr.filter(floor_s(pl.col("T")) == pl.col("wstart")).height),
           "lattice_secs": round(time.time() - t_start, 2)}
    print(json.dumps(log), flush=True)

    rows = []

    # ---------- trades ----------
    t0 = time.time()
    tp = d / f"{inst}_trades_tagged_{month}.parquet"
    tscan = (pl.scan_parquet(tp)
               .select(pl.col("ts_event").dt.replace_time_zone(None).dt.timestamp("ns").alias("ns"),
                       pl.col("aggressor_side"), pl.col("size")))
    is_buy = pl.col("aggressor_side").is_in(["B", "Buy", "buy"])          # L231
    tclasses = {"trades_all": pl.lit(True), "trades_buy": is_buy,
                "trades_sell": ~is_buy, "trades_large": pl.col("size") >= 10}   # L236
    tagg, teq, tnev = per_second_and_eq(tscan, tclasses, lat_stamps, engine)
    rows += count_side(corr, tagg, teq, tclasses, "corrected", corr.height, True)
    rows += count_side(cont, tagg, teq, tclasses, "contaminated", N, False)
    t_trades = round(time.time() - t0, 2)
    log["trades_secs"] = t_trades
    log["trades_events"] = tnev

    # ---------- mbo ----------
    mp = d / f"{inst}_mbo_{month}.parquet"
    if not mp.exists():
        log["mbo"] = "ABSENT — no MBO parquet for this instrument; trade classes only"
        log["mbo_secs"] = 0.0
        mnev = {}
    else:
        t0 = time.time()
        n_mbo = pq.ParquetFile(str(mp)).metadata.num_rows
        large = n_mbo > BIG_PATH_THRESHOLD
        log["mbo_rows"] = n_mbo
        log["mbo_builder_path"] = "LARGE" if large else "SMALL"
        mscan = (pl.scan_parquet(mp)
                   .select(pl.col("ts_event").dt.replace_time_zone(None).dt.timestamp("ns").alias("ns"),
                           pl.col("action"), pl.col("side")))
        if large:
            is_bid = pl.col("side").str.slice(0, 1) == "B"                # L128+L130 ('U1' cast)
            all_def = (pl.col("action") == "A") | (pl.col("action") == "C")   # L147 total_events
        else:
            is_bid = pl.col("side").is_in(["B", "b", "Buy", "bid"])       # L160
            all_def = pl.lit(True)                                        # L168 count of all rows
        isA, isC = pl.col("action") == "A", pl.col("action") == "C"
        mclasses = {"mbo_all": all_def,
                    "mbo_bid_add": isA & is_bid, "mbo_ask_add": isA & ~is_bid,
                    "mbo_bid_cancel": isC & is_bid, "mbo_ask_cancel": isC & ~is_bid,
                    "mbo_cancel_any": isC}
        if large:
            mclasses["mbo_all_rows"] = pl.lit(True)
        magg, meq, mnev = per_second_and_eq(mscan, mclasses, lat_stamps, engine)
        rows += count_side(corr, magg, meq, mclasses, "corrected", corr.height, True)
        rows += count_side(cont, magg, meq, mclasses, "contaminated", N, False)
        log["mbo_secs"] = round(time.time() - t0, 2)
    log["mbo_events"] = mnev
    log["total_secs"] = round(time.time() - t_start, 2)

    df = pl.DataFrame(
        [dict(instrument=inst, month=month, **dict(zip(
            ["class", "side", "boundary", "strict", "equal", "rows", "gap_strict", "gap_equal"], r)))
         for r in rows],
        schema={"instrument": pl.Utf8, "month": pl.Utf8, "class": pl.Utf8, "side": pl.Utf8,
                "boundary": pl.Utf8, "strict": pl.Int64, "equal": pl.Int64, "rows": pl.Int64,
                "gap_strict": pl.Int64, "gap_equal": pl.Int64})

    bad = df.filter((pl.col("side") == "corrected") & (pl.col("boundary") == "decision_T")
                    & ((pl.col("strict") > 0) | (pl.col("equal") > 0)))
    log["corrected_decisionT_nonzero_cells"] = bad.height
    print(json.dumps(log, default=str), flush=True)
    if bad.height:
        print(f"  *** NONZERO CORRECTED decision_T for {inst} {month} ***")
        print(bad.select("class", "strict", "equal", "rows"))
    return df, log


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inst", required=True)
    ap.add_argument("--month", default="2025-01")
    ap.add_argument("--engine", default="streaming")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    df, log = run(a.inst, a.month, a.engine)
    tag = a.tag or f"{a.inst}_{a.month}"
    df.write_csv(OUT / f"counts_{tag}.csv")
    (OUT / f"log_{tag}.json").write_text(json.dumps(log, indent=2, default=str), encoding="utf-8")
    print(df)
    print("wrote", OUT / f"counts_{tag}.csv")
