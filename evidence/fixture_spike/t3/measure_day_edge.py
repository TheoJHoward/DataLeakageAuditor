# T3 DAY-EDGE LABELS measurement — MEASUREMENT ONLY, no detector code, no fixes.
# Reads the existing f2 fixture build output (contaminated_zc_2025-01_run1.pkl) and
# measures whether the label shift(-h) crosses trading-session (calendar-day) boundaries.
import pandas as pd
import numpy as np
from pathlib import Path

HERE = Path(__file__).resolve().parent
F2_OUT = HERE.parent / "f2" / "out"
PKL = F2_OUT / "contaminated_zc_2025-01_run1.pkl"

snap = pd.read_pickle(PKL)
print(f"loaded {PKL}")
print(f"rows={len(snap)} cols={snap.shape[1]}")

ts = pd.to_datetime(snap["timestamp"]).reset_index(drop=True)
snap = snap.reset_index(drop=True)

# ---- session boundary detection (reported, not inferred away) ----
# Method A (primary): the builder's own session logic is a per-calendar-day hour
# filter (ZC: hour_utc in [14,19)), so one session == one calendar UTC date.
dates = ts.dt.normalize()
day_change = (dates != dates.shift(1))
n_sessions = dates.nunique()
n_day_boundaries = int(day_change.sum()) - 1  # first row is not a boundary
print(f"unique calendar dates (sessions): {n_sessions}")
print(f"consecutive-row day-change boundaries: {n_day_boundaries}")
print("session dates:", sorted(d.strftime('%Y-%m-%d') for d in dates.unique()))

# Method B (cross-check): consecutive-row wall-clock gap > 60 s (re-anchor threshold)
gap = ts.diff()
gap_gt60 = gap > pd.Timedelta(seconds=60)
n_gap60 = int(gap_gt60.sum())
# partition: gap>60s AND day change vs gap>60s within same day (intra-day re-anchor)
gap60_daychange = int((gap_gt60 & day_change).sum())
gap60_sameday = int((gap_gt60 & ~day_change).sum())
print(f"consecutive-row gaps > 60 s: {n_gap60} "
      f"(coinciding with day change: {gap60_daychange}; intra-day: {gap60_sameday})")
# gap sizes at day boundaries
day_gap_sizes = gap[day_change & (gap.notna())]
if len(day_gap_sizes):
    print(f"day-boundary gap sizes: min={day_gap_sizes.min()}, max={day_gap_sizes.max()}")
# intra-day >60s gaps listing
intra = gap[gap_gt60 & ~day_change]
if len(intra):
    print("intra-day >60s gaps (row ts -> gap):")
    for i in intra.index[:20]:
        print(f"  after {ts.iloc[i-1]} -> {ts.iloc[i]}  gap={gap.iloc[i]}")

N = len(snap)
horizons = [5, 10, 30, 60]
rows_out = []
samples_out = []

for h in horizons:
    lab = snap[f"fwd_move_ticks_{h}s"]
    nan_total = int(lab.isna().sum())
    tail_nan = int(lab.iloc[-h:].isna().sum())  # month-boundary check: expect == h
    # positional counterpart: row i pairs with row i+h
    i = np.arange(0, N - h)
    j = i + h
    cross = (dates.values[j] != dates.values[i])
    n_cross = int(cross.sum())
    ic = i[cross]
    jc = j[cross]
    lab_cross = lab.values[ic]
    n_cross_real = int(np.sum(~np.isnan(lab_cross)))
    n_cross_nan = int(np.sum(np.isnan(lab_cross)))
    spans = ts.values[jc] - ts.values[ic]
    if len(spans):
        worst = pd.Timedelta(spans.max())
        med = pd.Timedelta(np.median(spans.astype('timedelta64[ns]').astype('int64')), unit='ns')
    else:
        worst = med = pd.NaT
    # same-day pairs spanning an intra-day >60s re-anchor gap (pretend-h-seconds within day)
    sameday = ~cross
    is_ = i[sameday]; js_ = j[sameday]
    spans_sd = (ts.values[js_] - ts.values[is_])
    n_sameday_gt60 = int(np.sum(spans_sd > np.timedelta64(60, 's')))
    worst_sd = pd.Timedelta(spans_sd.max()) if len(spans_sd) else pd.NaT

    rows_out.append({
        "horizon_s": h,
        "total_rows": N,
        "nan_labels_total": nan_total,
        "month_tail_last_h_rows_nan": tail_nan,
        "cross_boundary_label_pairs": n_cross,
        "cross_boundary_label_real_value": n_cross_real,
        "cross_boundary_label_nan": n_cross_nan,
        "worst_wallclock_span_cross": str(worst),
        "median_wallclock_span_cross": str(med),
        "sameday_pairs_span_gt60s": n_sameday_gt60,
        "worst_wallclock_span_sameday": str(worst_sd),
    })

    # 3 samples per horizon: first, one mid, and the worst-span cross-boundary pair
    if n_cross:
        order = np.argsort(spans)  # ascending
        pick = [order[0], order[len(order)//2], order[-1]]
        seen = set()
        for k in pick:
            if k in seen: continue
            seen.add(k)
            a, b = ic[k], jc[k]
            samples_out.append({
                "horizon_s": h,
                "row_pos": int(a),
                "row_stamp": str(ts.iloc[a]),
                "counterpart_pos": int(b),
                "counterpart_stamp": str(ts.iloc[b]),
                "wallclock_span": str(ts.iloc[b] - ts.iloc[a]),
                "label_value_fwd_move_ticks": (float(lab.iloc[a]) if not np.isnan(lab.iloc[a]) else np.nan),
                "mid_at_row": float(snap["mid_price"].iloc[a]),
                "mid_at_counterpart": float(snap["mid_price"].iloc[b]),
            })

tbl = pd.DataFrame(rows_out)
tbl.to_csv(HERE / "day_edge_table.csv", index=False)
print("\n=== per-horizon table ===")
print(tbl.to_string(index=False))

smp = pd.DataFrame(samples_out)
smp.to_csv(HERE / "day_edge_samples.csv", index=False)
print("\n=== cross-boundary samples (min / median / max span per horizon) ===")
print(smp.to_string(index=False))

# verify label arithmetic on the worst-span 60s sample: (mid[j]-mid[i])/0.25
print("\n=== label arithmetic check on samples ===")
for r in samples_out:
    recomputed = (r["mid_at_counterpart"] - r["mid_at_row"]) / 0.25
    print(f"h={r['horizon_s']} row={r['row_stamp']} label={r['label_value_fwd_move_ticks']} "
          f"recomputed=(mid_j-mid_i)/tick={recomputed:.1f}")
