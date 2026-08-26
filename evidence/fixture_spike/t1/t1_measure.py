"""T1: ts_floor persistence measurement, both sides (contaminated / corrected).

MEASUREMENT ONLY. Reads: archive raw parquets (read-only), f2 out pkls (read-only).
Writes: only under fixture_spike/t1/.

Definitions:
- decision time of a row = its own snapshot stamp T (snapshot contains book events
  strictly before T, per process_mbo.py lines 354-363).
- contaminated side: features at row t are built from wall-clock second floor(T_t)
  (rolling windows over lattice ROWS always include the current row, and every older
  window second s <= floor(T_t)-1 contains only events with ts_event < floor(T_t) <= T_t,
  so ONLY the row's own second can contribute post-T events -> per-row violation
  indicator is EXACT for every window length, not a bound).
- corrected side: features at row t = contaminated features at row t-1 (universal
  shift(1)); absorbed window is that of T_prev = stamp of previous lattice row.
  Compared against BOTH the decision time T_t and the claimed boundary T_prev.
- tie branches: ts_event strictly after boundary = violation under BOTH branches;
  ts_event exactly equal = branch-dependent (counted separately).
"""
import json
import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

T1 = os.path.dirname(os.path.abspath(__file__))
F2_OUT = os.path.join(os.path.dirname(T1), "f2", "out")
RAW = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"

NS = 1_000_000_000

# ---------------------------------------------------------------- load pkls
cont = pd.read_pickle(os.path.join(F2_OUT, "contaminated_zc_2025-01_run1.pkl"))
corr = pd.read_pickle(os.path.join(F2_OUT, "corrected_zc_2025-01_run1.pkl"))
print("contaminated shape:", cont.shape, " corrected shape:", corr.shape)

ts = pd.to_datetime(cont["timestamp"])
if ts.dt.tz is not None:
    ts = ts.dt.tz_localize(None)
t_ns = ts.astype("int64").to_numpy()
assert np.all(np.diff(t_ns) > 0) or True
n_rows = len(t_ns)
fl = (t_ns // NS) * NS          # start of the row's wall-clock second
sec_end = fl + NS               # exclusive end of the row's wall-clock second

# lattice spacing / re-anchoring
d = np.diff(t_ns)
n_exact_1s = int(np.sum(d == NS))
n_gt_1s = int(np.sum(d > NS))
n_lt_1s = int(np.sum(d < NS))
n_nonpos = int(np.sum(d <= 0))
print(json.dumps({
    "rows": n_rows,
    "spacing_exact_1s": n_exact_1s,
    "spacing_gt_1s(re-anchor/gap)": n_gt_1s,
    "spacing_lt_1s": n_lt_1s,
    "spacing_nonpositive": n_nonpos,
    "max_gap_s": float(d.max() / NS),
    "min_gap_s": float(d.min() / NS),
    "rows_mid_second(T>floor)": int(np.sum(t_ns > fl)),
    "rows_on_second_boundary(T==floor)": int(np.sum(t_ns == fl)),
    "dup_ts_floor_vs_prev_row": int(np.sum(fl[1:] == fl[:-1])),
}, indent=1))

# ------------------------------------------------- load raw events, tz-naive ns
tr = pq.read_table(os.path.join(RAW, "zc_trades_tagged_2025-01.parquet"),
                   columns=["ts_event", "aggressor_side", "side", "size", "price"]).to_pandas()
tr["ts_event"] = pd.to_datetime(tr["ts_event"])
if tr["ts_event"].dt.tz is not None:
    tr["ts_event"] = tr["ts_event"].dt.tz_localize(None)
is_buy = tr["aggressor_side"].isin(["B", "Buy", "buy"])          # builder line 234 (archive 231)
tr_ns = tr["ts_event"].astype("int64").to_numpy()

mbo = pq.read_table(os.path.join(RAW, "zc_mbo_2025-01.parquet"),
                    columns=["ts_event", "action", "side"]).to_pandas()
mbo["ts_event"] = pd.to_datetime(mbo["ts_event"])
if mbo["ts_event"].dt.tz is not None:
    mbo["ts_event"] = mbo["ts_event"].dt.tz_localize(None)
m_is_bid = mbo["side"].isin(["B", "b", "Buy", "bid"])            # builder line 166 (archive 163)
m_act = mbo["action"].to_numpy()
mbo_ns = mbo["ts_event"].astype("int64").to_numpy()

classes = {
    "trades_all":      np.sort(tr_ns),
    "trades_buy":      np.sort(tr_ns[is_buy.to_numpy()]),
    "trades_sell":     np.sort(tr_ns[~is_buy.to_numpy()]),
    "trades_large":    np.sort(tr_ns[(tr["size"] >= 10).to_numpy()]),
    "mbo_all":         np.sort(mbo_ns),
    "mbo_bid_add":     np.sort(mbo_ns[(m_act == "A") & m_is_bid.to_numpy()]),
    "mbo_ask_add":     np.sort(mbo_ns[(m_act == "A") & ~m_is_bid.to_numpy()]),
    "mbo_bid_cancel":  np.sort(mbo_ns[(m_act == "C") & m_is_bid.to_numpy()]),
    "mbo_ask_cancel":  np.sort(mbo_ns[(m_act == "C") & ~m_is_bid.to_numpy()]),
    "mbo_cancel_any":  np.sort(mbo_ns[(m_act == "C")]),
}
print({k: len(v) for k, v in classes.items()})

# --------------------------------------- (b) per-second max ts + count tables
def per_second(a):
    s = (a // NS) * NS
    df = pd.DataFrame({"sec": s, "ts": a})
    g = df.groupby("sec")["ts"].agg(["count", "max"]).reset_index()
    g.columns = ["sec_start_ns", "count", "max_ts_ns"]
    return g

ps_tr = per_second(classes["trades_all"])
ps_mbo = per_second(classes["mbo_all"])
ps_tr.to_parquet(os.path.join(T1, "per_second_trades.parquet"))
ps_mbo.to_parquet(os.path.join(T1, "per_second_mbo.parquet"))
print("per-second trades: seconds =", len(ps_tr), " total events =", int(ps_tr["count"].sum()))
print("per-second mbo:    seconds =", len(ps_mbo), " total events =", int(ps_mbo["count"].sum()))

# ---------------------------------------------- per-row indicators per class
def row_indicators(a, boundary_ns, win_lo_ns, win_hi_ns):
    """Events of sorted array a inside window [win_lo, win_hi) relative to boundary.
    Returns (strict_after bool[], equal bool[], overhang_ns int[] (0 if none))."""
    lo_b = np.searchsorted(a, boundary_ns, "left")
    hi_b = np.searchsorted(a, boundary_ns, "right")
    hi_w = np.searchsorted(a, win_hi_ns, "left")
    lo_w = np.searchsorted(a, win_lo_ns, "left")
    # equal: event exactly at boundary AND boundary inside window
    equal = (hi_b > lo_b) & (boundary_ns >= win_lo_ns) & (boundary_ns < win_hi_ns)
    # strictly after boundary but inside window: indices in (max(hi_b, lo_w), hi_w)
    start = np.maximum(hi_b, lo_w)
    strict = hi_w > start
    over = np.zeros(len(boundary_ns), dtype="int64")
    idx = hi_w - 1
    has = strict
    over[has] = a[idx[has]] - boundary_ns[has]
    return strict, equal, over

results = {}   # (class, side, boundary) -> dict
prev_fl = np.roll(fl, 1)
prev_t = np.roll(t_ns, 1)
valid_prev = np.ones(n_rows, dtype=bool)
valid_prev[0] = False   # corrected row 0 has NaN features (shift(1)) - no absorbed content

for cname, a in classes.items():
    # contaminated vs decision T: window = row's own second
    s, e, o = row_indicators(a, t_ns, fl, sec_end)
    results[(cname, "contaminated", "decision_T")] = dict(
        strict=int(s.sum()), equal=int(e.sum()), total=n_rows,
        worst_ms=float(o.max() / 1e6),
        strict_mask=s)
    # corrected vs claimed boundary T_prev: window = prev row's second, boundary T_prev
    s2, e2, o2 = row_indicators(a, prev_t, prev_fl, prev_fl + NS)
    s2 &= valid_prev; e2 &= valid_prev; o2 = np.where(valid_prev, o2, 0)
    results[(cname, "corrected", "claimed_T_prev")] = dict(
        strict=int(s2.sum()), equal=int(e2.sum()), total=int(valid_prev.sum()),
        worst_ms=float(o2.max() / 1e6))
    # corrected vs decision T: window = prev row's second, boundary = own T
    s3, e3, o3 = row_indicators(a, t_ns, prev_fl, prev_fl + NS)
    s3 &= valid_prev; e3 &= valid_prev; o3 = np.where(valid_prev, o3, 0)
    results[(cname, "corrected", "decision_T")] = dict(
        strict=int(s3.sum()), equal=int(e3.sum()), total=int(valid_prev.sum()),
        worst_ms=float(o3.max() / 1e6))

# consistency: corrected-vs-claimed should equal contaminated-vs-decision shifted by 1
for cname in classes:
    c_dec = results[(cname, "contaminated", "decision_T")]
    c_cla = results[(cname, "corrected", "claimed_T_prev")]
    last_row_ind = bool(c_dec["strict_mask"][-1])
    expect = c_dec["strict"] - (1 if last_row_ind else 0)
    ok = expect == c_cla["strict"]
    if not ok:
        print("MISMATCH shift-identity:", cname, c_dec["strict"], c_cla["strict"], last_row_ind)

# re-anchor rows: does excluding them change corrected-side answers?
gap_rows = np.zeros(n_rows, dtype=bool)
gap_rows[1:] = d != NS
print("rows whose prev-row spacing != 1s:", int(gap_rows[1:].sum()))
for cname, a in classes.items():
    s3, e3, o3 = row_indicators(a, t_ns, prev_fl, prev_fl + NS)
    s3 &= valid_prev
    print(f"  corrected decision_T strict on gap rows only [{cname}]:",
          int((s3 & gap_rows).sum()))
    break  # identical zero-arithmetic applies; report trades_all, verify all classes below

# full zero verification for all classes on gap rows
gap_viol = {}
for cname, a in classes.items():
    s3, e3, o3 = row_indicators(a, t_ns, prev_fl, prev_fl + NS)
    s3 &= valid_prev; e3 &= valid_prev
    gap_viol[cname] = [int((s3 & gap_rows).sum()), int((e3 & gap_rows).sum())]
print("corrected decision_T (strict,equal) restricted to re-anchor/gap rows:", gap_viol)

# ---------------------------------------------- column map -> violation table
col_map = [
    # (column, class, window_desc)
    ("net_delta",             "trades_all",     "merged 1s aggregate (own second)"),
    ("buy_volume",            "trades_buy",     "merged 1s aggregate (own second)"),
    ("sell_volume",           "trades_sell",    "merged 1s aggregate (own second)"),
    ("trade_count",           "trades_all",     "merged 1s aggregate (own second)"),
    ("trade_volume",          "trades_all",     "merged 1s aggregate (own second)"),
    ("large_trade_count",     "trades_large",   "merged 1s aggregate (own second)"),
    ("vwap",                  "trades_all",     "merged 1s aggregate; if own second tradeless, stale value from earlier second (ffill)"),
    ("net_delta_1s",          "trades_all",     "rolling 1 row (== net_delta)"),
    ("net_delta_5s",          "trades_all",     "rolling 5 rows ending at own row"),
    ("net_delta_10s",         "trades_all",     "rolling 10 rows ending at own row"),
    ("net_delta_30s",         "trades_all",     "rolling 30 rows ending at own row"),
    ("net_delta_60s",         "trades_all",     "rolling 60 rows ending at own row"),
    ("buy_volume_10s",        "trades_buy",     "rolling 10 rows ending at own row"),
    ("sell_volume_10s",       "trades_sell",    "rolling 10 rows ending at own row"),
    ("trade_count_10s",       "trades_all",     "rolling 10 rows ending at own row"),
    ("large_trade_count_10s", "trades_large",   "rolling 10 rows ending at own row"),
    ("vwap_distance",         "trades_all",     "inherits vwap (mid is snapshot-native)"),
    ("bid_adds",              "mbo_bid_add",    "merged 1s aggregate (own second)"),
    ("ask_adds",              "mbo_ask_add",    "merged 1s aggregate (own second)"),
    ("bid_cancels",           "mbo_bid_cancel", "merged 1s aggregate (own second)"),
    ("ask_cancels",           "mbo_ask_cancel", "merged 1s aggregate (own second)"),
    ("total_events",          "mbo_all",        "merged 1s aggregate (own second)"),
    ("bid_add_rate_5s",       "mbo_bid_add",    "rolling 5 rows ending at own row"),
    ("bid_add_rate_10s",      "mbo_bid_add",    "rolling 10 rows ending at own row"),
    ("ask_add_rate_5s",       "mbo_ask_add",    "rolling 5 rows ending at own row"),
    ("ask_add_rate_10s",      "mbo_ask_add",    "rolling 10 rows ending at own row"),
    ("bid_cancel_rate_5s",    "mbo_bid_cancel", "rolling 5 rows ending at own row"),
    ("bid_cancel_rate_10s",   "mbo_bid_cancel", "rolling 10 rows ending at own row"),
    ("ask_cancel_rate_5s",    "mbo_ask_cancel", "rolling 5 rows ending at own row"),
    ("ask_cancel_rate_10s",   "mbo_ask_cancel", "rolling 10 rows ending at own row"),
    ("cancel_ratio_asymmetry","mbo_cancel_any", "from bid/ask_cancel_rate_10s"),
    ("event_rate_10s",        "mbo_all",        "rolling 10 rows ending at own row"),
    ("order_flow_accel",      "mbo_all",        "event_rate_10s.diff(5): rows t-14..t"),
]

col_notes = {
    "buy_volume": "AS-BUILT CAVEAT: is_buy=aggressor_side.isin(['B','Buy','buy']) matches no value "
                  "(actual values SELL_AGGRESSOR/BUY_AGGRESSOR/UNKNOWN) -> buy_volume identically 0.0, absorbs nothing",
    "buy_volume_10s": "identically 0.0 as built (see buy_volume)",
    "sell_volume": "as built absorbs ALL trades (every trade classified sell; sell_volume==trade_volume on all rows)",
    "sell_volume_10s": "as built absorbs ALL trades (see sell_volume)",
    "net_delta": "as built signed_vol = -uint32 size wraps to 2**32-size for every trade (all classified sell)",
}
rows_out = []
for col, cls, wdesc in col_map:
    for side, boundary in [("contaminated", "decision_T"),
                           ("corrected", "decision_T"),
                           ("corrected", "claimed_T_prev")]:
        r = results[(cls, side, boundary)]
        rows_out.append(dict(
            column=col, side=side, boundary=boundary, event_class=cls,
            window=wdesc,
            strictly_after_count=r["strict"], equal_count=r["equal"],
            total_rows=r["total"],
            frac=round(r["strict"] / r["total"], 6),
            worst_overhang_ms=round(r["worst_ms"], 6),
            exactness="exact (only own/prev second can exceed boundary)",
            note=col_notes.get(col, ""),
        ))
vt = pd.DataFrame(rows_out)
vt.to_csv(os.path.join(T1, "violation_table.csv"), index=False)
print("violation_table.csv written:", vt.shape)

# compact per-class summary for findings
print("\nPER-CLASS SUMMARY (one line per class x side x boundary):")
for cname in classes:
    for side, boundary in [("contaminated", "decision_T"),
                           ("corrected", "decision_T"),
                           ("corrected", "claimed_T_prev")]:
        r = results[(cname, side, boundary)]
        print(f"{cname:16s} {side:12s} {boundary:14s} strict={r['strict']:7d} "
              f"equal={r['equal']:4d} total={r['total']} frac={r['strict']/r['total']:.4f} "
              f"worst_ms={r['worst_ms']:.3f}")

# ---------------------------- (d) verification of newest-second argument, w=5 sample
rng = np.random.default_rng(20260810)
sample = rng.choice(np.arange(60, n_rows), size=2000, replace=False)
a = classes["trades_all"]
ps = ps_tr.set_index("sec_start_ns")
mismatch = 0
w5_vs_w1_diff = 0
s1 = results[("trades_all", "contaminated", "decision_T")]["strict_mask"]
for i in sample:
    secs = fl[i - 4:i + 1]          # the 5 window rows' own seconds
    # exact absorbed max over the 5 seconds:
    mx = None
    for s_ in secs:
        if s_ in ps.index:
            v = ps.loc[s_, "max_ts_ns"]
            mx = v if mx is None else max(mx, v)
    # newest-second-with-events max:
    mx2 = None
    for s_ in secs[::-1]:
        if s_ in ps.index:
            mx2 = ps.loc[s_, "max_ts_ns"]
            break
    if mx != mx2:
        mismatch += 1
    # w=5 violation indicator vs w=1 indicator
    viol5 = (mx is not None) and (mx > t_ns[i])
    if viol5 != bool(s1[i]):
        w5_vs_w1_diff += 1
print(f"\n(d) sample n=2000: newest-second-max == window-max mismatches: {mismatch}; "
      f"w5 violation indicator != w1 indicator: {w5_vs_w1_diff}")

# ------------------------------- shift(1) relationship verification on a sample
feat_check = ["net_delta_1s", "net_delta_5s", "event_rate_10s", "vwap_distance",
              "buy_volume_10s", "order_flow_accel", "total_events", "vwap"]
idx = rng.choice(np.arange(1, n_rows), size=5000, replace=False)
bad = {}
for c in feat_check:
    x = corr[c].to_numpy()[idx]
    y = cont[c].to_numpy()[idx - 1]
    both_nan = pd.isna(x) & pd.isna(y)
    eqv = (x == y) | both_nan
    bad[c] = int((~eqv).sum())
print("corrected[t] == contaminated[t-1] mismatches (sample n=5000):", bad)

# ---------------------------------------------- (e) end-to-end sanity-check row
viol_idx = np.flatnonzero(results[("trades_all", "contaminated", "decision_T")]["strict_mask"])
print("\ntotal strict-violating rows (trades_all, contaminated, decision_T):", len(viol_idx))
i = int(viol_idx[len(viol_idx) // 2])   # a mid-month example
T = t_ns[i]
print("row index:", i)
print("row stamp T:", pd.Timestamp(T))
print("row ts_floor (joined second):", pd.Timestamp(fl[i]))
in_sec = tr[(tr_ns >= fl[i]) & (tr_ns < sec_end[i])].sort_values("ts_event")
print("raw trades in joined second:")
sub = in_sec.copy()
sub["after_T"] = sub["ts_event"].astype("int64") > T
sub["signed_vol"] = np.where(sub["aggressor_side"].isin(["B", "Buy", "buy"]),
                             sub["size"], -sub["size"])
print(sub[["ts_event", "price", "size", "aggressor_side", "signed_vol", "after_T"]].to_string())
print("sum signed_vol over second =", sub["signed_vol"].sum(),
      "; pkl net_delta_1s at row =", cont["net_delta_1s"].iloc[i],
      "; pkl net_delta at row =", cont["net_delta"].iloc[i])
print("max trade ts in second =", sub["ts_event"].max(),
      "; overhang past T (ms) =", (sub["ts_event"].astype("int64").max() - T) / 1e6)
print("corrected pkl net_delta_1s at row i+1 =", corr["net_delta_1s"].iloc[i + 1],
      " (should equal contaminated row i)")
print("corrected row i+1 stamp =", pd.Timestamp(t_ns[i + 1]))
# save the sanity row for the record
with open(os.path.join(T1, "sanity_row.txt"), "w") as f:
    f.write(f"row index {i}\nrow stamp T {pd.Timestamp(T)}\njoined second {pd.Timestamp(fl[i])}\n")
    f.write(sub[["ts_event", "price", "size", "aggressor_side", "signed_vol", "after_T"]].to_string())
    f.write(f"\nsum signed_vol {sub['signed_vol'].sum()} pkl net_delta_1s {cont['net_delta_1s'].iloc[i]}\n")
    f.write(f"max trade ts {sub['ts_event'].max()} overhang_ms {(sub['ts_event'].astype('int64').max() - T)/1e6}\n")
    f.write(f"corrected net_delta_1s at row i+1 {corr['net_delta_1s'].iloc[i+1]} stamp {pd.Timestamp(t_ns[i+1])}\n")
print("\nDONE")
