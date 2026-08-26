"""V1: per-class mean/median/worst overhang (contaminated side vs decision time T).

Reads (read-only): t1 per-second parquets, f2 lattice pkl, archive raw parquets.
Writes: only under fixture_spike/v1/.

Definition (per item V1): for each event class, over lattice rows whose own
wall-clock second [floor(T), floor(T)+1s) contains an event with ts_event > T
(strictly), report mean/median/worst of (max ts_event in that second - T) in ms.

Strictness note: strict violation <=> max ts_event in the row's second > T,
because the max is itself an event in the second; overhang uses that same max.
"""
import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
T1 = os.path.join(BASE, "t1")
V1 = os.path.join(BASE, "v1")
PKL = os.path.join(BASE, "f2", "out", "contaminated_zc_2025-01_run1.pkl")
RAW = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"
NS = 1_000_000_000

# Known strict counts from t1_final_output.txt lines 23-52 (contaminated, decision_T)
EXPECTED_STRICT = {
    "trades_all": 89568,
    "trades_large": 23633,
    "mbo_all": 254315,
    "mbo_bid_add": 164959,
    "mbo_ask_add": 162754,
    "mbo_bid_cancel": 135981,
    "mbo_ask_cancel": 129334,
    "mbo_cancel_any": 179857,
}

# ---------------------------------------------------------------- lattice
cont = pd.read_pickle(PKL)
assert len(cont) == 338159, f"lattice rows {len(cont)} != 338159"
ts = pd.to_datetime(cont["timestamp"])
if ts.dt.tz is not None:
    ts = ts.dt.tz_localize(None)
t_ns = ts.astype("int64").to_numpy()
fl = (t_ns // NS) * NS
print("lattice rows:", len(t_ns))

# ------------------------------------------- per-second max lookup machinery
def overhang_from_per_second(sec_start, max_ts):
    """sec_start/max_ts: sorted per-second table arrays. Returns (strict_mask,
    overhang_ns for strict rows) over the lattice."""
    idx = np.searchsorted(sec_start, fl, "left")
    idx_c = np.clip(idx, 0, len(sec_start) - 1)
    present = (idx < len(sec_start)) & (sec_start[idx_c] == fl)
    mx = np.where(present, max_ts[idx_c], np.int64(-1))
    strict = present & (mx > t_ns)
    return strict, (mx[strict] - t_ns[strict])

def per_second_from_events(a):
    """a: sorted int64 ns event stamps -> (sec_start sorted unique, max_ts per sec)."""
    s = (a // NS) * NS
    # a sorted => within each second the last element is the max
    sec, last_idx = np.unique(s, return_index=True)
    # last index of each group = next group's first index - 1
    ends = np.append(last_idx[1:], len(a)) - 1
    return sec, a[ends]

# ---------------------------------------------------------------- class arrays
# trades_all / mbo_all primary source: t1 per-second parquets (schema verified:
# sec_start_ns, count, max_ts_ns; class-level only -> subclasses from raw below)
ps_tr = pq.read_table(os.path.join(T1, "per_second_trades.parquet")).to_pandas()
ps_mbo = pq.read_table(os.path.join(T1, "per_second_mbo.parquet")).to_pandas()
assert list(ps_tr.columns) == ["sec_start_ns", "count", "max_ts_ns"], list(ps_tr.columns)
assert list(ps_mbo.columns) == ["sec_start_ns", "count", "max_ts_ns"], list(ps_mbo.columns)
assert ps_tr["sec_start_ns"].is_monotonic_increasing
assert ps_mbo["sec_start_ns"].is_monotonic_increasing
print("per_second_trades rows:", len(ps_tr), " total events:", int(ps_tr["count"].sum()))
print("per_second_mbo rows:   ", len(ps_mbo), " total events:", int(ps_mbo["count"].sum()))

# raw trades (for trades_large + cross-check of trades_all)
tr = pq.read_table(os.path.join(RAW, "zc_trades_tagged_2025-01.parquet"),
                   columns=["ts_event", "size"]).to_pandas()
tr["ts_event"] = pd.to_datetime(tr["ts_event"])
if tr["ts_event"].dt.tz is not None:
    tr["ts_event"] = tr["ts_event"].dt.tz_localize(None)
tr_ns = tr["ts_event"].astype("int64").to_numpy()
tr_size = tr["size"].to_numpy()

# raw mbo (for subclasses + cross-check of mbo_all); builder class defs
# phase5_ml_fixture.py lines 163-167: is_bid = side.isin(["B","b","Buy","bid"]);
# bid_add = action=="A" & is_bid; ask_add = action=="A" & ~is_bid;
# bid_cancel = action=="C" & is_bid; ask_cancel = action=="C" & ~is_bid
mbo = pq.read_table(os.path.join(RAW, "zc_mbo_2025-01.parquet"),
                    columns=["ts_event", "action", "side"]).to_pandas()
mbo["ts_event"] = pd.to_datetime(mbo["ts_event"])
if mbo["ts_event"].dt.tz is not None:
    mbo["ts_event"] = mbo["ts_event"].dt.tz_localize(None)
m_is_bid = mbo["side"].isin(["B", "b", "Buy", "bid"]).to_numpy()
m_act = mbo["action"].to_numpy()
mbo_ns = mbo["ts_event"].astype("int64").to_numpy()

class_arrays = {
    "trades_all":     np.sort(tr_ns),
    "trades_large":   np.sort(tr_ns[tr_size >= 10]),
    "mbo_all":        np.sort(mbo_ns),
    "mbo_bid_add":    np.sort(mbo_ns[(m_act == "A") & m_is_bid]),
    "mbo_ask_add":    np.sort(mbo_ns[(m_act == "A") & ~m_is_bid]),
    "mbo_bid_cancel": np.sort(mbo_ns[(m_act == "C") & m_is_bid]),
    "mbo_ask_cancel": np.sort(mbo_ns[(m_act == "C") & ~m_is_bid]),
    "mbo_cancel_any": np.sort(mbo_ns[m_act == "C"]),
}
print({k: len(v) for k, v in class_arrays.items()})

# ---------------------------------------------------------------- compute
rows = []
mismatches = []
for cname, a in class_arrays.items():
    sec, mx = per_second_from_events(a)
    strict, over_ns = overhang_from_per_second(sec, mx)

    # cross-check class-level results against the t1 per-second parquets
    if cname == "trades_all":
        s2, o2 = overhang_from_per_second(ps_tr["sec_start_ns"].to_numpy(),
                                          ps_tr["max_ts_ns"].to_numpy())
        assert int(s2.sum()) == int(strict.sum()) and np.array_equal(o2, over_ns), \
            "trades_all: parquet-based vs raw-based disagree"
        print("trades_all: t1 parquet vs raw recompute AGREE")
    if cname == "mbo_all":
        s2, o2 = overhang_from_per_second(ps_mbo["sec_start_ns"].to_numpy(),
                                          ps_mbo["max_ts_ns"].to_numpy())
        assert int(s2.sum()) == int(strict.sum()) and np.array_equal(o2, over_ns), \
            "mbo_all: parquet-based vs raw-based disagree"
        print("mbo_all: t1 parquet vs raw recompute AGREE")

    n = int(strict.sum())
    exp = EXPECTED_STRICT[cname]
    if n != exp:
        mismatches.append((cname, n, exp))
    over_ms = over_ns / 1e6
    rows.append(dict(
        **{"class": cname},
        strict_count=n,
        mean_overhang_ms=round(float(over_ms.mean()), 6),
        median_overhang_ms=round(float(np.median(over_ms)), 6),
        worst_overhang_ms=round(float(over_ms.max()), 6),
    ))

out = pd.DataFrame(rows)
print("\n" + out.to_string(index=False))
if mismatches:
    print("\nSTRICT-COUNT MISMATCHES vs t1 record:", mismatches)
else:
    print("\nAll strict counts reproduce the t1 record exactly.")
out.to_csv(os.path.join(V1, "mean_overhang_by_class.csv"), index=False)
print("written:", os.path.join(V1, "mean_overhang_by_class.csv"))
