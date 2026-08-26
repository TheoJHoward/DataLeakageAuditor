"""ITEM C4 — INDEPENDENT re-measurement of corrected-side availability, ZC 2025-01.

Written from the availability definitions alone; all computation in POLARS.
Reads ONLY the raw archive parquets and (definitions) the f2 builder source.

Definitions implemented (derived from f2/phase5_ml_fixture.py, quoted line numbers):
  - Lattice: zc_snapshots_2025-01.parquet, sorted by timestamp (L187), session filter
      L188: snap["hour_utc"] = snap["timestamp"].dt.hour
      L189: snap = snap[(snap["hour_utc"] >= ds) & (snap["hour_utc"] < de)].copy()
    with ds=14, de=19 for zc (L58: "zc": {... "day_start_utc": 14, "day_end_utc": 19 ...}).
  - Wall-clock join key: L225: snap["ts_floor"] = snap["timestamp"].dt.floor("1s")
    trades L233: trades["ts_floor"] = trades["ts_event"].dt.floor("1s")
    mbo    L162: df["ts_floor"] = df["ts_event"].dt.floor("1s")   (small path; file is 8.27M rows < 50M, L126)
  - CORRECTED side: feature content of row i = joined aggregates of row i-1's second
    [floor(T_{i-1}), floor(T_{i-1})+1s)  (universal shift(1) per fixture.py L51:
    snap[feature_cols] = snap[feature_cols].shift(1)). Row 0 has no content -> measured rows are i>=1.
  - Decision time of row i = T_i (its own stamp). Strict violation: event ts_event > T_i inside
    the absorbed window; equal: ts_event == T_i (violation only under ties=unavailable).
  - Secondary boundary B_i = T_{i-1}: same window, strict > T_{i-1}, equal == T_{i-1}.

Event classes (10), builder semantics verbatim:
  trades (L234-239):
    is_buy = trades["aggressor_side"].isin(["B","Buy","buy"])   (aggressor_side EXISTS in parquet)
      -> actual parquet values are {BUY_AGGRESSOR, SELL_AGGRESSOR, UNKNOWN}: the test matches
         NOTHING; trades_buy is EMPTY, trades_sell (~is_buy) is ALL trades. Measured as-is.
    trades["is_large"] = (trades["size"] >= 10)
  mbo small path (L163-167):
    is_bid = side.isin(["B","b","Buy","bid"])
    bid_add = (action=="A") & is_bid ; ask_add = (action=="A") & ~is_bid
    bid_cancel = (action=="C") & is_bid ; ask_cancel = (action=="C") & ~is_bid
    total_events = count of ALL rows (L171: total_events=("action","count"))

Row-level counting: a row i is counted for (class, boundary, strict) if its absorbed window
contains >=1 event of the class with ts_event strictly after the boundary; similarly for equal.

Window-length independence: snapshot stamps are sorted, so every OLDER absorbed second
[floor(T_j), floor(T_j)+1s), j < i-1, ends no later than floor(T_{i-1})+1s; any event in it
with ts_event > T_i (>= T_{i-1} >= floor(T_{i-1})) necessarily lies in
[floor(T_{i-1}), floor(T_{i-1})+1s) — i.e. inside the NEWEST absorbed second — hence a
w-second rolling window violates iff its newest second violates. Verified empirically below.
"""
import sys
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"
OUT = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\c4"
DS, DE = 14, 19                      # zc session hours (builder INST_META L58)
ONE_S = 1_000_000_000                # ns

print("polars", pl.__version__)

# ── 1. Lattice ────────────────────────────────────────────────────────────────
snap = (
    pl.read_parquet(BASE + r"\zc_snapshots_2025-01.parquet", columns=["timestamp"])
    .sort("timestamp")                                   # builder L187 sort_values("timestamp")
    .with_columns(pl.col("timestamp").dt.hour().alias("hour_utc"))   # L188 (naive ns stamps)
    .filter((pl.col("hour_utc") >= DS) & (pl.col("hour_utc") < DE))  # L189
    .select("timestamp")
)
N = snap.height
print(f"lattice rows after session filter: {N}  (expected build record: 338159)")

lat = (
    snap.rename({"timestamp": "T"})
    .with_columns(pl.col("T").shift(1).alias("Tprev"))
    .slice(1)                                            # rows i >= 1 (row 0 has no content)
    .with_columns(
        pl.col("Tprev").dt.truncate("1s").alias("wstart"),           # floor(T_{i-1})
        ((pl.col("T") - pl.col("Tprev")).dt.total_nanoseconds() != ONE_S).alias("is_gap"),
    )
)
n_rows = lat.height
n_gap = int(lat["is_gap"].sum())
print(f"measured rows (i>=1): {n_rows}; re-anchor gap rows (spacing != 1s): {n_gap}")

# spacing distribution for the record
spc = (
    lat.with_columns((pl.col("T") - pl.col("Tprev")).dt.total_nanoseconds().alias("spacing_ns"))
    .group_by("spacing_ns").len().sort("len", descending=True).head(12)
)
print("top spacing values (ns):")
for r in spc.to_dicts():
    print("  ", r)

# ── 2. Events ─────────────────────────────────────────────────────────────────
trades = (
    pl.read_parquet(BASE + r"\zc_trades_tagged_2025-01.parquet",
                    columns=["ts_event", "aggressor_side", "size"])
    .with_columns(pl.col("ts_event").dt.replace_time_zone(None))     # builder L231 tz_localize(None), tz=UTC
)
mbo = (
    pl.read_parquet(BASE + r"\zc_mbo_2025-01.parquet",
                    columns=["ts_event", "action", "side"])
    .with_columns(pl.col("ts_event").dt.replace_time_zone(None))     # builder L161
)

is_buy = pl.col("aggressor_side").is_in(["B", "Buy", "buy"])         # builder L234 — matches nothing here
is_bid = pl.col("side").is_in(["B", "b", "Buy", "bid"])              # builder L163 (small path)

CLASSES = {
    "trades_all":     (trades, pl.lit(True)),
    "trades_buy":     (trades, is_buy),
    "trades_sell":    (trades, ~is_buy),
    "trades_large":   (trades, pl.col("size") >= 10),                # builder L239
    "mbo_all":        (mbo, pl.lit(True)),
    "mbo_bid_add":    (mbo, (pl.col("action") == "A") & is_bid),
    "mbo_ask_add":    (mbo, (pl.col("action") == "A") & ~is_bid),
    "mbo_bid_cancel": (mbo, (pl.col("action") == "C") & is_bid),
    "mbo_ask_cancel": (mbo, (pl.col("action") == "C") & ~is_bid),
    "mbo_cancel_any": (mbo, pl.col("action") == "C"),
}

# ── 3. Per-class row-level violation flags ───────────────────────────────────
rows_out = []
flags_for_sample = {}   # keep mbo_all flags frame for the 500-row verification

for cname, (src, cond) in CLASSES.items():
    ev = src.filter(cond).select("ts_event")
    n_ev = ev.height
    if n_ev == 0:
        for boundary in ("decision_T", "prev_row_B"):
            rows_out.append(dict(event_class=cname, boundary=boundary,
                                 strict_count=0, equal_count=0, total_rows=n_rows,
                                 gap_row_subset_strict=0, gap_row_subset_equal=0,
                                 n_events_in_class=0))
        print(f"{cname:15s} events=0 (empty class) -> all counts 0")
        continue

    # per-second max event timestamp
    agg = (ev.with_columns(pl.col("ts_event").dt.truncate("1s").alias("sec"))
             .group_by("sec").agg(pl.col("ts_event").max().alias("max_ts")))
    # distinct exact event timestamps (for equality tests)
    ets = ev.unique().with_columns(pl.lit(True).alias("has_ev"))

    f = (
        lat.join(agg, left_on="wstart", right_on="sec", how="left")
           .join(ets, left_on="T", right_on="ts_event", how="left")
           .rename({"has_ev": "ev_at_T"})
           .join(ets, left_on="Tprev", right_on="ts_event", how="left")
           .rename({"has_ev": "ev_at_Tprev"})
           .with_columns(
               # (a) vs decision time T_i
               (pl.col("max_ts").is_not_null() & (pl.col("max_ts") > pl.col("T"))).alias("strict_T"),
               (pl.col("ev_at_T").fill_null(False)
                & (pl.col("T").dt.truncate("1s") == pl.col("wstart"))).alias("equal_T"),
               # (b) vs boundary B_i = T_{i-1} (an event == T_{i-1} always lies in the window)
               (pl.col("max_ts").is_not_null() & (pl.col("max_ts") > pl.col("Tprev"))).alias("strict_B"),
               pl.col("ev_at_Tprev").fill_null(False).alias("equal_B"),
           )
    )
    if cname == "mbo_all":
        flags_for_sample["mbo_all"] = f.select("T", "Tprev", "wstart", "strict_T", "equal_T")

    s = f.select(
        pl.col("strict_T").sum(), pl.col("equal_T").sum(),
        pl.col("strict_B").sum(), pl.col("equal_B").sum(),
        pl.col("strict_T").filter(pl.col("is_gap")).sum().alias("gap_strict_T"),
        pl.col("equal_T").filter(pl.col("is_gap")).sum().alias("gap_equal_T"),
        pl.col("strict_B").filter(pl.col("is_gap")).sum().alias("gap_strict_B"),
        pl.col("equal_B").filter(pl.col("is_gap")).sum().alias("gap_equal_B"),
    ).row(0)
    (sT, eT, sB, eB, gsT, geT, gsB, geB) = [int(x) for x in s]
    rows_out.append(dict(event_class=cname, boundary="decision_T",
                         strict_count=sT, equal_count=eT, total_rows=n_rows,
                         gap_row_subset_strict=gsT, gap_row_subset_equal=geT,
                         n_events_in_class=n_ev))
    rows_out.append(dict(event_class=cname, boundary="prev_row_B",
                         strict_count=sB, equal_count=eB, total_rows=n_rows,
                         gap_row_subset_strict=gsB, gap_row_subset_equal=geB,
                         n_events_in_class=n_ev))
    print(f"{cname:15s} events={n_ev:>9,}  decision_T: strict={sT} equal={eT} (gap {gsT}/{geT})"
          f"  |  prev_row_B: strict={sB} equal={eB} (gap {gsB}/{geB})")

res = pl.DataFrame(rows_out)
res.write_csv(OUT + r"\independent_counts.csv")
print("\nwrote", OUT + r"\independent_counts.csv")

# ── 4. Window-length independence: 500-row empirical check, class=mbo_all, w=5 ─
# Union window of corrected rolling-w at row i = union of seconds of rows i-w..i-1.
# Claim: strict/equal violation vs T_i in the union  <=>  violation in newest second (row i-1).
# All arithmetic in integer nanoseconds to keep exact ns precision.
mb_ns = mbo.select(pl.col("ts_event").dt.timestamp("ns").alias("ns"))
mb_agg = (mb_ns.with_columns(((pl.col("ns") // ONE_S) * ONE_S).alias("sec"))
               .group_by("sec").agg(pl.col("ns").max().alias("max_ts")))
mb_ets_set = set(mb_ns["ns"].unique().to_list())
sec_map = dict(zip(mb_agg["sec"].to_list(), mb_agg["max_ts"].to_list()))

T_all = snap["timestamp"].dt.timestamp("ns").to_list()
W = 5
import random
random.seed(20260810)
sample_idx = sorted(random.sample(range(W, N), 500))

mismatch = 0
checked = 0
for i in sample_idx:
    Ti = T_all[i]
    secs = {(T_all[j] // ONE_S) * ONE_S for j in range(i - W, i)}
    union_strict = any(sec_map.get(s, -1) > Ti for s in secs)
    union_equal = (Ti in mb_ets_set) and ((Ti // ONE_S) * ONE_S in secs)
    newest_sec = (T_all[i - 1] // ONE_S) * ONE_S
    newest_strict = sec_map.get(newest_sec, -1) > Ti
    newest_equal = (Ti in mb_ets_set) and (newest_sec == (Ti // ONE_S) * ONE_S)
    checked += 1
    if union_strict != newest_strict or union_equal != newest_equal:
        mismatch += 1
        print(f"  MISMATCH at lattice idx {i}: union=({union_strict},{union_equal}) "
              f"newest=({newest_strict},{newest_equal})")
print(f"\nwindow-length independence check (class=mbo_all, w=5, {checked} sampled rows): "
      f"{mismatch} mismatches")
print("done")
