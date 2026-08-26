r"""ITEM X4 — NQ NON-GATED CROSS-GENERATION MBO DIAGNOSTIC (working resolution R12).

NOT gate evidence. Produces the map that N1 could not produce for NQ, because the fixture
path `processed\nq\nq_mbo_{month}.parquet` does not exist (N1 unscored_ledger.csv rows 2-7).

Adapted from (read-only reference)
  ...\scratchpad\fixture_spike\n1\n1_declared_map.py
Same definitions, same polars/integer-nanosecond arithmetic, same count_side() logic.
WHAT CHANGES vs N1
  * instrument fixed to nq; the six MBO classes only (+ the 11th diagnostic class
    `mbo_all_rows`, exactly as N1/M5 report it on LARGE-path instrument-months).
  * event source is not a month file at the fixture path. Two sources are measured:
      V4  = processed\nq\v4_gapfill\nq_mbo_{month}\nq_mbo_YYYYMMDD.parquet   (mandated by X4)
      V3  = pc2_transfer\processed\nq\nq_mbo_{month}.parquet                 (found by search;
            generation v3_pre_gapfill, family E of n2\provenance_notes.md)
    The lattice is the v3 fixture path in BOTH cases, so V4 is a cross-generation join and
    V3 is a same-generation join.
  * a per-day soundness characterisation ((a) day coverage, (b) event counts + V3-vs-V4 delta,
    (c) per-day timestamp-range alignment) is emitted before any count is interpreted.

DEFINITIONS (line numbers in C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\phase5\phase5_ml.py)

  Lattice        L176-186: read nq_snapshots_{month}.parquet, sort by timestamp,
                 hour_utc = timestamp.dt.hour, keep 14 <= hour_utc < 22.
                 phase5_ml.py L48-49, verbatim:
                     INST_META = {
                       "nq": {"tick_size": 0.25, "matching": "FIFO",
                              "day_start_utc": 14, "day_end_utc": 22, "ct_ratio": 7.84},
  Join key       L129 mbo ts_floor = (ts // 1_000_000_000) * 1_000_000_000   (LARGE path)
  CONTAMINATED   row i absorbs its OWN second [floor(T_i), floor(T_i)+1s). All N rows measured.
  CORRECTED      row i absorbs the PREVIOUS row's second [floor(T_{i-1}), floor(T_{i-1})+1s).
                 Row 0 has no content -> i>=1, N-1 rows.
  decision_T     boundary = T_i.  strict: absorbed event has ts_event > T_i.
                                  equal : absorbed event has ts_event == T_i.
  prev_row_B     boundary = B_i = T_{i-1} (corrected side only, supplementary CSV).

CLASS DEFINITIONS — LARGE builder path, phase5_ml.py L123-150, verbatim:

    if n_rows > 50_000_000:
        for batch in pf.iter_batches(batch_size=10_000_000, columns=["ts_event","action","side"]):
            ts  = batch.column("ts_event").cast('int64').to_numpy()
            act = batch.column("action").to_numpy(zero_copy_only=False).astype('U1')
            sid = batch.column("side").to_numpy(zero_copy_only=False).astype('U1')
            ts_floor = (ts // 1_000_000_000) * 1_000_000_000
            is_bid = (sid == 'B'); is_add = (act == 'A'); is_cancel = (act == 'C')
        ...
        result["total_events"] = result["bid_adds"] + result["ask_adds"] \
                               + result["bid_cancels"] + result["ask_cancels"]

  -> is_bid = side[:1] == 'B'; mbo_all = action in {A, C} (the four summed components);
     mbo_all_rows = every MBO row (the SMALL-path definition, 11th diagnostic class).
  Both NQ sources are LARGE path (row counts asserted at runtime).

Reads ONLY C:\Users\ttbea\OneDrive\Desktop\MBO_2025 (read-only archive).
Writes ONLY under ...\scratchpad\fixture_spike\x4.
"""
import sys, time, json, re, traceback
from datetime import datetime, timezone
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
LATTICE_DIR = ARCH / "processed" / "nq"                       # v3_pre_gapfill fixture path
V4_DIR = ARCH / "processed" / "nq" / "v4_gapfill"             # v4 per-day MBO
V3_MBO_DIR = ARCH / "pc2_transfer" / "processed" / "nq"       # v3_pre_gapfill month MBO
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\x4")
OUT.mkdir(parents=True, exist_ok=True)

DS, DE = 14, 22                       # phase5_ml.py L49 INST_META["nq"]
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
ONE_S = 1_000_000_000
DAY_NS = 86_400 * ONE_S
BIG_PATH_THRESHOLD = 50_000_000       # phase5_ml.py L123
ENGINE = "streaming"

MBO_CLASSES = ["mbo_all", "mbo_bid_add", "mbo_ask_add",
               "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]
DIAG_CLASS = "mbo_all_rows"
ALL_CLASSES = MBO_CLASSES + [DIAG_CLASS]


def floor_s(e):
    return (e // ONE_S) * ONE_S


def ns_to_date(ns):
    return datetime.fromtimestamp(int(ns) // ONE_S, tz=timezone.utc).strftime("%Y-%m-%d")


def ns_to_str(ns):
    if ns is None:
        return None
    s, r = divmod(int(ns), ONE_S)
    return datetime.fromtimestamp(s, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + f".{r:09d}"


def build_lattice(month):
    p = LATTICE_DIR / f"nq_snapshots_{month}.parquet"
    snap = (pl.read_parquet(p, columns=["timestamp"])
              .sort("timestamp")                                              # L184
              .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))  # L185
              .filter((pl.col("hour_utc") >= DS) & (pl.col("hour_utc") < DE)) # L186
              .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
    N = snap.height
    cont = snap.with_columns(floor_s(pl.col("T")).alias("wstart"))
    corr = (snap.with_columns(pl.col("T").shift(1).alias("Tprev"))
                .slice(1)
                .with_columns(floor_s(pl.col("Tprev")).alias("wstart"),
                              (pl.col("T") - pl.col("Tprev")).alias("dt")))
    prof = {
        "lattice_path": str(p),
        "rows": N,
        "corrected_rows": corr.height,
        "same_second_rows": int(corr.filter(floor_s(pl.col("T")) == pl.col("wstart")).height),
        "gaps_gt_60s": int(corr.filter(pl.col("dt") > 60 * ONE_S).height),
        "T_min": snap["T"].min(), "T_max": snap["T"].max(),
    }
    return snap, cont, corr, N, prof


CLASS_CONDS = None


def class_conds():
    """LARGE builder path (phase5_ml.py L128-147)."""
    is_bid = pl.col("side").str.slice(0, 1) == "B"
    isA, isC = pl.col("action") == "A", pl.col("action") == "C"
    return {
        "mbo_all": isA | isC,                       # bid_adds+ask_adds+bid_cancels+ask_cancels
        "mbo_bid_add": isA & is_bid, "mbo_ask_add": isA & ~is_bid,
        "mbo_bid_cancel": isC & is_bid, "mbo_ask_cancel": isC & ~is_bid,
        "mbo_cancel_any": isC,
        DIAG_CLASS: pl.lit(True),
    }


def per_second_table(paths, lat_stamps):
    """ONE streaming pass per file. Returns a per-second frame:
         sec | min_all | max_all | max_<c> | n_<c> ...   and eqsets {class -> lattice stamps hit}
    Days are disjoint across the v4 per-day files, but the frames are re-aggregated by `sec`
    anyway so overlapping inputs would still be handled correctly."""
    classes = class_conds()
    exprs = [pl.col("ns").min().alias("min_all"), pl.col("ns").max().alias("max_all")]
    for c, cond in classes.items():
        exprs.append(pl.col("ns").filter(cond).max().alias(f"max_{c}"))
        exprs.append(pl.col("ns").filter(cond).len().alias(f"n_{c}"))
        exprs.append(pl.col("ns").filter(cond & pl.col("is_lat")).unique().alias(f"eq_{c}"))
    parts = []
    for p in paths:
        q = (pl.scan_parquet(p)
               .select(pl.col("ts_event").dt.replace_time_zone(None)
                         .dt.timestamp("ns").alias("ns"),
                       pl.col("action"), pl.col("side"))
               .with_columns(pl.col("ns").is_in(lat_stamps.implode()).alias("is_lat"))
               .with_columns(floor_s(pl.col("ns")).alias("sec"))
               .group_by("sec").agg(exprs))
        parts.append(q.collect(engine=ENGINE))
    agg = pl.concat(parts, how="vertical") if len(parts) > 1 else parts[0]
    if len(parts) > 1:
        re_exprs = [pl.col("min_all").min(), pl.col("max_all").max()]
        for c in classes:
            re_exprs += [pl.col(f"max_{c}").max(), pl.col(f"n_{c}").sum(),
                         pl.col(f"eq_{c}").flatten().unique()]
        agg = agg.group_by("sec").agg(re_exprs)
    eqsets = {c: agg[f"eq_{c}"].explode().drop_nulls().unique() for c in classes}
    agg = agg.select(["sec", "min_all", "max_all"]
                     + [f"max_{c}" for c in classes] + [f"n_{c}" for c in classes])
    return agg, eqsets


def count_side(frame, agg, eqsets, side, n_rows, has_prev):
    """N1 count_side(), verbatim logic. Returns (class, side, boundary, strict, equal, rows)."""
    out = []
    for c in ALL_CLASSES:
        eq = eqsets[c]
        f = (frame.join(agg.select(["sec", f"max_{c}"]),
                        left_on="wstart", right_on="sec", how="left")
                  .rename({f"max_{c}": "mx"}))
        f = f.with_columns(pl.col("T").is_in(eq.implode()).alias("ev_at_T"))
        strict_T = int(f.select((pl.col("mx").is_not_null()
                                 & (pl.col("mx") > pl.col("T"))).sum()).item())
        equal_T = int(f.select((pl.col("ev_at_T")
                                & (floor_s(pl.col("T")) == pl.col("wstart"))).sum()).item())
        out.append((c, side, "decision_T", strict_T, equal_T, n_rows))
        if has_prev:
            f = f.with_columns(pl.col("Tprev").is_in(eq.implode()).alias("ev_at_Tprev"))
            strict_B = int(f.select((pl.col("mx").is_not_null()
                                     & (pl.col("mx") > pl.col("Tprev"))).sum()).item())
            equal_B = int(f.select(pl.col("ev_at_Tprev").sum()).item())
            out.append((c, side, "prev_row_B", strict_B, equal_B, n_rows))
    return out


def per_day(agg):
    """Per UTC date, restricted to the lattice hour window [14,22): event counts per class,
    plus the true min/max ts_event inside the window."""
    w = (agg.with_columns(((pl.col("sec") // (3600 * ONE_S)) % 24).alias("hour_utc"),
                          (pl.col("sec") // DAY_NS).alias("day_idx"))
            .filter((pl.col("hour_utc") >= DS) & (pl.col("hour_utc") < DE)))
    g = w.group_by("day_idx").agg(
        [pl.col("min_all").min().alias("ev_min"), pl.col("max_all").max().alias("ev_max"),
         pl.col("sec").n_unique().alias("distinct_secs")]
        + [pl.col(f"n_{c}").sum().alias(f"n_{c}") for c in ALL_CLASSES])
    return g.sort("day_idx")


def lattice_per_day(snap):
    return (snap.with_columns((pl.col("T") // DAY_NS).alias("day_idx"))
                .group_by("day_idx")
                .agg(pl.len().alias("lat_rows"), pl.col("T").min().alias("lat_min"),
                     pl.col("T").max().alias("lat_max"))
                .sort("day_idx"))


def v4_paths(month):
    d = V4_DIR / f"nq_mbo_{month}"
    ym = month.replace("-", "")
    out = []
    for p in sorted(d.glob("nq_mbo_*.parquet")):
        m = re.fullmatch(r"nq_mbo_(\d{8})\.parquet", p.name)
        if m and m.group(1).startswith(ym):
            out.append(p)
    strays = [p.name for p in sorted(d.glob("nq_mbo_*.parquet"))
              if p not in out]
    return out, strays


def main():
    t_all = time.time()
    logs = {"months": {}}
    rows_all = []          # v4 join   (mandated deliverable)
    rows_v3 = []           # v3 join   (same-generation supplementary)
    rows_r4, rows_r3 = [], []   # both joins restricted to days the v4 source covers
    day_rows = []          # soundness (a)(b)(c)

    for month in MONTHS:
        t0 = time.time()
        log = {}
        snap, cont, corr, N, prof = build_lattice(month)
        lat = snap["T"]
        log["lattice"] = dict(prof, T_min_str=ns_to_str(prof["T_min"]),
                              T_max_str=ns_to_str(prof["T_max"]))
        lday = lattice_per_day(snap)
        log["lattice_secs"] = round(time.time() - t0, 2)

        p4, strays = v4_paths(month)
        # lattice frames restricted to the UTC dates the v4 per-day source actually covers.
        # corrected: BOTH the decision row's date and the absorbed window's date must be covered.
        cov_idx = sorted({int(datetime.strptime(p.name[7:15], "%Y%m%d")
                              .replace(tzinfo=timezone.utc).timestamp()) // 86400 for p in p4})
        cov = pl.Series("d", cov_idx, dtype=pl.Int64)
        cont_r = cont.filter((pl.col("T") // DAY_NS).is_in(cov.implode()))
        corr_r = corr.filter((pl.col("T") // DAY_NS).is_in(cov.implode())
                             & (pl.col("Tprev") // DAY_NS).is_in(cov.implode()))
        log["restricted_rows"] = {"contaminated": cont_r.height, "corrected": corr_r.height}
        log["v4_files"] = len(p4)
        log["v4_stray_files_not_in_month"] = strays
        n4 = sum(pq.ParquetFile(str(p)).metadata.num_rows for p in p4)
        log["v4_total_rows"] = n4
        log["v4_builder_path"] = "LARGE" if n4 > BIG_PATH_THRESHOLD else "SMALL"

        p3 = V3_MBO_DIR / f"nq_mbo_{month}.parquet"
        log["v3_path"] = str(p3)
        log["v3_exists"] = p3.exists()
        if p3.exists():
            n3 = pq.ParquetFile(str(p3)).metadata.num_rows
            log["v3_total_rows"] = n3
            log["v3_builder_path"] = "LARGE" if n3 > BIG_PATH_THRESHOLD else "SMALL"

        # ---------------- V4 pass ----------------
        t1 = time.time()
        agg4, eq4 = per_second_table(p4, lat)
        log["v4_pass_secs"] = round(time.time() - t1, 1)
        d4 = per_day(agg4)
        raw = count_side(corr, agg4, eq4, "corrected", corr.height, True)
        raw += count_side(cont, agg4, eq4, "contaminated", N, False)
        for (c, side, b, s, e, nr) in raw:
            rows_all.append(dict(side=side, month=month, **{"class": c}, boundary=b,
                                 strict_count=s, equal_count=e, rows=nr))
        raw = count_side(corr_r, agg4, eq4, "corrected", corr_r.height, True)
        raw += count_side(cont_r, agg4, eq4, "contaminated", cont_r.height, False)
        for (c, side, b, s, e, nr) in raw:
            rows_r4.append(dict(side=side, month=month, **{"class": c}, boundary=b,
                                strict_count=s, equal_count=e, rows=nr))
        del agg4

        # ---------------- V3 pass ----------------
        d3 = None
        if p3.exists():
            t1 = time.time()
            agg3, eq3 = per_second_table([p3], lat)
            log["v3_pass_secs"] = round(time.time() - t1, 1)
            d3 = per_day(agg3)
            raw = count_side(corr, agg3, eq3, "corrected", corr.height, True)
            raw += count_side(cont, agg3, eq3, "contaminated", N, False)
            for (c, side, b, s, e, nr) in raw:
                rows_v3.append(dict(side=side, month=month, **{"class": c}, boundary=b,
                                    strict_count=s, equal_count=e, rows=nr))
            raw = count_side(corr_r, agg3, eq3, "corrected", corr_r.height, True)
            raw += count_side(cont_r, agg3, eq3, "contaminated", cont_r.height, False)
            for (c, side, b, s, e, nr) in raw:
                rows_r3.append(dict(side=side, month=month, **{"class": c}, boundary=b,
                                    strict_count=s, equal_count=e, rows=nr))
            del agg3

        # ---------------- per-day soundness join ----------------
        idx = set(lday["day_idx"].to_list()) | set(d4["day_idx"].to_list())
        if d3 is not None:
            idx |= set(d3["day_idx"].to_list())
        L = {r["day_idx"]: r for r in lday.to_dicts()}
        F4 = {r["day_idx"]: r for r in d4.to_dicts()}
        F3 = {r["day_idx"]: r for r in (d3.to_dicts() if d3 is not None else [])}
        v4_file_days = {p.name[7:15] for p in p4}
        for di in sorted(idx):
            date = ns_to_date(di * DAY_NS)
            l, a, b = L.get(di), F4.get(di), F3.get(di)
            day_rows.append(dict(
                month=month, date=date,
                in_lattice=l is not None, lattice_rows=(l or {}).get("lat_rows"),
                lattice_min=ns_to_str((l or {}).get("lat_min")),
                lattice_max=ns_to_str((l or {}).get("lat_max")),
                v4_day_file_present=date.replace("-", "") in v4_file_days,
                v4_events_in_window=(a or {}).get(f"n_{DIAG_CLASS}"),
                v4_mbo_all_in_window=(a or {}).get("n_mbo_all"),
                v4_min=ns_to_str((a or {}).get("ev_min")),
                v4_max=ns_to_str((a or {}).get("ev_max")),
                v3_events_in_window=(b or {}).get(f"n_{DIAG_CLASS}"),
                v3_mbo_all_in_window=(b or {}).get("n_mbo_all"),
                v3_min=ns_to_str((b or {}).get("ev_min")),
                v3_max=ns_to_str((b or {}).get("ev_max")),
            ))
        log["month_secs"] = round(time.time() - t0, 1)
        logs["months"][month] = log
        print(json.dumps({month: log}, default=str), flush=True)

    cols = ["side", "month", "class", "boundary", "strict_count", "equal_count", "rows"]
    df4 = pl.DataFrame(rows_all).select(cols)
    df4.filter(pl.col("boundary") == "decision_T").write_csv(OUT / "nq_mbo_diagnostic.csv")
    df4.write_csv(OUT / "nq_mbo_diagnostic_all_boundaries.csv")
    if rows_v3:
        df3 = pl.DataFrame(rows_v3).select(cols)
        df3.filter(pl.col("boundary") == "decision_T").write_csv(
            OUT / "nq_mbo_v3_same_generation_map.csv")
        df3.write_csv(OUT / "nq_mbo_v3_same_generation_all_boundaries.csv")
    pl.DataFrame(rows_r4).select(cols).filter(pl.col("boundary") == "decision_T").write_csv(
        OUT / "restricted_to_v4_covered_days_v4source.csv")
    if rows_r3:
        pl.DataFrame(rows_r3).select(cols).filter(pl.col("boundary") == "decision_T").write_csv(
            OUT / "restricted_to_v4_covered_days_v3source.csv")
    pl.DataFrame(day_rows).write_csv(OUT / "per_day_coverage.csv")
    (OUT / "run_logs.json").write_text(json.dumps(logs, indent=2, default=str), encoding="utf-8")
    print(f"### WALL TOTAL {time.time()-t_all:.1f}s", flush=True)


if __name__ == "__main__":
    main()
