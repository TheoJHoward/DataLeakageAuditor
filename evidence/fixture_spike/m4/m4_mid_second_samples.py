"""M4 addendum: enumerate the (rare) strictly-violating rows that sit on MID-SECOND
stamps, for trades_all (all of them) and mbo_all (all 49), as verbatim evidence.
Reads read-only; writes only fixture_spike/m4/mid_second_violation_rows.txt."""
import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

M4 = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(M4)
RAW = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"
NS = 1_000_000_000

cont = pd.read_pickle(os.path.join(SPIKE, "f2", "out", "contaminated_zc_2025-01_run1.pkl"))
ts = pd.to_datetime(cont["timestamp"])
if ts.dt.tz is not None:
    ts = ts.dt.tz_localize(None)
t_ns = ts.astype("int64").to_numpy()
fl = (t_ns // NS) * NS
sec_end = fl + NS
mid = t_ns > fl

def masks(a):
    hi_b = np.searchsorted(a, t_ns, "right")
    hi_w = np.searchsorted(a, sec_end, "left")
    lo_w = np.searchsorted(a, fl, "left")
    return hi_w > np.maximum(hi_b, lo_w)

tr_ns = np.sort(pd.to_datetime(
    pq.read_table(os.path.join(RAW, "zc_trades_tagged_2025-01.parquet"),
                  columns=["ts_event"]).to_pandas()["ts_event"]
    ).dt.tz_localize(None).astype("int64").to_numpy())
mbo_ns = np.sort(pd.to_datetime(
    pq.read_table(os.path.join(RAW, "zc_mbo_2025-01.parquet"),
                  columns=["ts_event"]).to_pandas()["ts_event"]
    ).dt.tz_localize(None).astype("int64").to_numpy())

lines = []
for cname, a in [("trades_all", tr_ns), ("mbo_all", mbo_ns)]:
    s = masks(a)
    idx = np.flatnonzero(s & mid)
    lines.append(f"{cname}: strict-violating rows on MID-SECOND stamps: n={len(idx)}")
    for i in idx:
        hi_b = np.searchsorted(a, t_ns[i], "right")
        hi_w = np.searchsorted(a, sec_end[i], "left")
        n_after = int(hi_w - hi_b)
        worst = a[hi_w - 1] - t_ns[i]
        lines.append(
            f"  row {i}: T={pd.Timestamp(t_ns[i])} floor={pd.Timestamp(fl[i])} "
            f"frac_offset_ms={(t_ns[i]-fl[i])/1e6:.3f} events_after_T_in_second={n_after} "
            f"max_overhang_ms={worst/1e6:.3f}")
    lines.append("")

out = "\n".join(lines)
with open(os.path.join(M4, "mid_second_violation_rows.txt"), "w") as f:
    f.write(out)
print(out)
