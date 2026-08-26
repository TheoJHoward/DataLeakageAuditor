"""M4: per-stamp-type breakdown of strict availability violations, contaminated side
vs decision time T (window = row's own wall-clock second [floor(T), floor(T)+1s)).

MEASUREMENT ONLY. Reads (read-only):
  - fixture_spike/f2/out/contaminated_zc_2025-01_run1.pkl   (row timestamps)
  - fixture_spike/t1/per_second_trades.parquet, per_second_mbo.parquet
  - archive raw parquets C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed\\zc
    (zc_trades_tagged_2025-01.parquet, zc_mbo_2025-01.parquet) -- for the 8 sub-classes
Writes: only under fixture_spike/m4/.

Stamp types:
  integral-second : T == floor(T)   (row stamp lies exactly on a second boundary)
  mid-second      : T >  floor(T)

Strict violation (identical to t1_measure.py row_indicators, contaminated/decision_T):
  at least one event of the class with  T < ts_event < floor(T)+1s.
Events with ts_event == T exactly are the 'equal' tie branch, counted separately.

Method A (independent, per-second tables only): strict <=> second floor(T) present in
  the per-second table AND max_ts_ns > T. Valid because within the row's own second
  every event has ts >= floor(T), so max_ts > T <=> an event strictly after T exists
  ... EXCEPT the tie case max_ts == T which is 'equal' not strict -- the > comparison
  handles that correctly. Available for trades_all and mbo_all only.
Method B (t1 replication from raw archive): searchsorted on sorted event stamps,
  strict count = events in (T, floor(T)+1s) > 0. All 10 t1 classes.
Cross-checks: A == B row-for-row on trades_all/mbo_all; per-class strict totals must
  equal t1 violation_table.csv (89568, 254315, ...).
"""
import json
import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

M4 = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(M4)
F2_OUT = os.path.join(SPIKE, "f2", "out")
T1 = os.path.join(SPIKE, "t1")
RAW = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"
NS = 1_000_000_000

# t1 violation_table.csv strict totals, contaminated / decision_T (expected)
EXPECTED = {
    "trades_all": 89568, "trades_buy": 0, "trades_sell": 89568,
    "trades_large": 23633, "mbo_all": 254315, "mbo_bid_add": 164959,
    "mbo_ask_add": 162754, "mbo_bid_cancel": 135981, "mbo_ask_cancel": 129334,
    "mbo_cancel_any": 179857,
}
EXPECTED_EQUAL = {
    "trades_all": 20, "trades_buy": 0, "trades_sell": 20, "trades_large": 20,
    "mbo_all": 29, "mbo_bid_add": 1, "mbo_ask_add": 4, "mbo_bid_cancel": 23,
    "mbo_ask_cancel": 22, "mbo_cancel_any": 24,
}

# ------------------------------------------------------------------ timestamps
cont = pd.read_pickle(os.path.join(F2_OUT, "contaminated_zc_2025-01_run1.pkl"))
ts = pd.to_datetime(cont["timestamp"])
if ts.dt.tz is not None:
    ts = ts.dt.tz_localize(None)
t_ns = ts.astype("int64").to_numpy()
n_rows = len(t_ns)
fl = (t_ns // NS) * NS
sec_end = fl + NS
integral = t_ns == fl            # stamp type: integral-second
mid = ~integral                  # stamp type: mid-second
print(json.dumps({"rows": n_rows,
                  "rows_integral(T==floor)": int(integral.sum()),
                  "rows_mid_second(T>floor)": int(mid.sum())}))
assert int(integral.sum()) == 321384 and int(mid.sum()) == 16775, \
    "row-population split does not match t1 output"

# ------------------------------------- Method A: per-second tables (t1 parquets)
def strict_mask_from_per_second(path):
    ps = pd.read_parquet(path)
    # map row's own second -> max event ts in that second (NaN if second eventless)
    mx = pd.Series(ps["max_ts_ns"].to_numpy(), index=ps["sec_start_ns"].to_numpy())
    row_max = mx.reindex(fl).to_numpy()
    return (~np.isnan(row_max)) & (row_max > t_ns)

A = {
    "trades_all": strict_mask_from_per_second(os.path.join(T1, "per_second_trades.parquet")),
    "mbo_all":    strict_mask_from_per_second(os.path.join(T1, "per_second_mbo.parquet")),
}
print("Method A strict totals:", {k: int(v.sum()) for k, v in A.items()})

# ------------------------- Method B: t1 class replication from raw archive
tr = pq.read_table(os.path.join(RAW, "zc_trades_tagged_2025-01.parquet"),
                   columns=["ts_event", "aggressor_side", "size"]).to_pandas()
tr["ts_event"] = pd.to_datetime(tr["ts_event"])
if tr["ts_event"].dt.tz is not None:
    tr["ts_event"] = tr["ts_event"].dt.tz_localize(None)
is_buy = tr["aggressor_side"].isin(["B", "Buy", "buy"])
tr_ns = tr["ts_event"].astype("int64").to_numpy()

mbo = pq.read_table(os.path.join(RAW, "zc_mbo_2025-01.parquet"),
                    columns=["ts_event", "action", "side"]).to_pandas()
mbo["ts_event"] = pd.to_datetime(mbo["ts_event"])
if mbo["ts_event"].dt.tz is not None:
    mbo["ts_event"] = mbo["ts_event"].dt.tz_localize(None)
m_is_bid = mbo["side"].isin(["B", "b", "Buy", "bid"])
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
print("class event counts:", {k: len(v) for k, v in classes.items()})

def strict_equal_masks(a):
    """t1 row_indicators specialized to contaminated/decision_T:
    boundary=T, window=[fl, sec_end)."""
    hi_b = np.searchsorted(a, t_ns, "right")
    lo_b = np.searchsorted(a, t_ns, "left")
    hi_w = np.searchsorted(a, sec_end, "left")
    lo_w = np.searchsorted(a, fl, "left")
    equal = (hi_b > lo_b)  # boundary T always inside [fl, sec_end): fl <= T < fl+1s
    start = np.maximum(hi_b, lo_w)
    strict = hi_w > start
    return strict, equal

rows_out = []
mism_total = 0
for cname, a in classes.items():
    s, e = strict_equal_masks(a)
    n_s, n_e = int(s.sum()), int(e.sum())
    ok_s = n_s == EXPECTED[cname]
    ok_e = n_e == EXPECTED_EQUAL[cname]
    if not (ok_s and ok_e):
        print(f"MISMATCH vs t1 [{cname}]: strict {n_s} (exp {EXPECTED[cname]}), "
              f"equal {n_e} (exp {EXPECTED_EQUAL[cname]})")
        mism_total += 1
    # Method A cross-check where available
    a_note = ""
    if cname in A:
        diff = int((s != A[cname]).sum())
        a_note = f"methodA_row_diffs={diff}"
        print(f"cross-check {cname}: method A vs B per-row differences = {diff}")
        assert diff == 0, f"method A/B disagree on {cname}"
    si, sm = int((s & integral).sum()), int((s & mid).sum())
    ei, em = int((e & integral).sum()), int((e & mid).sum())
    rows_out.append(dict(
        event_class=cname,
        side="contaminated", boundary="decision_T",
        rows_total=n_rows,
        rows_integral=int(integral.sum()), rows_mid_second=int(mid.sum()),
        strict_viol_integral=si, strict_viol_mid_second=sm, strict_viol_total=n_s,
        strict_total_matches_t1=ok_s,
        equal_tie_integral=ei, equal_tie_mid_second=em, equal_tie_total=n_e,
        equal_total_matches_t1=ok_e,
        viol_rate_integral=round(si / int(integral.sum()), 6),
        viol_rate_mid_second=round(sm / int(mid.sum()), 6),
        share_of_viol_on_integral=round(si / n_s, 6) if n_s else np.nan,
        share_of_rows_integral=round(int(integral.sum()) / n_rows, 6),
        method="B: searchsorted on raw archive (t1 replication)"
               + ("; A cross-checked (" + a_note + ")" if a_note else ""),
    ))

out = pd.DataFrame(rows_out)
out.to_csv(os.path.join(M4, "stamp_type_breakdown.csv"), index=False)
print("\nstamp_type_breakdown.csv written:", out.shape)
print(out[["event_class", "strict_viol_integral", "strict_viol_mid_second",
           "strict_viol_total", "viol_rate_integral", "viol_rate_mid_second",
           "share_of_viol_on_integral"]].to_string(index=False))
print("\nclasses mismatching t1 totals:", mism_total)
print("DONE")
