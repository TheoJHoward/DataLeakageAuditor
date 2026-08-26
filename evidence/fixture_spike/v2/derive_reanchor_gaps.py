"""V2: re-derive re-anchor variant date attribution from the run1 lattice timestamps.

Reads the contaminated ZC 2025-01 run1 pickle (read-only), derives:
  (a) all consecutive row-spacing gaps > 60 s, classified day-boundary vs intra-day
  (b) per-horizon stretched same-day pair counts (pairs i, i+h positional, same UTC
      date both sides, wall-clock span > h seconds) and worst such span
Writes v2/reanchor_gaps.csv (two sections in one file) and prints both tables.
"""
import pandas as pd
import numpy as np
import io, os, sys

BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
PKL = os.path.join(BASE, "f2", "out", "contaminated_zc_2025-01_run1.pkl")
OUT = os.path.join(BASE, "v2", "reanchor_gaps.csv")

df = pd.read_pickle(PKL)
print("rows:", len(df), "index dtype:", df.index.dtype, "timestamp col dtype:", df["timestamp"].dtype)

ts = pd.DatetimeIndex(df["timestamp"])
print("tz:", ts.tz)
print("first:", ts[0], "last:", ts[-1])
print("monotonic increasing:", ts.is_monotonic_increasing)

# Work in UTC for date classification
if ts.tz is None:
    ts_utc = ts  # assume already UTC; report as naive-assumed-UTC
    tz_note = "naive (assumed UTC)"
else:
    ts_utc = ts.tz_convert("UTC")
    tz_note = str(ts.tz)

# ---------- (a) consecutive gaps > 60 s ----------
diffs = ts_utc[1:] - ts_utc[:-1]
gap_mask = diffs > pd.Timedelta(seconds=60)
gap_positions = np.nonzero(np.asarray(gap_mask))[0]  # gap between row i and row i+1

gap_rows = []
for i in gap_positions:
    t0 = ts_utc[i]
    t1 = ts_utc[i + 1]
    gap = t1 - t0
    d0 = t0.date()
    d1 = t1.date()
    kind = "intra-day" if d0 == d1 else "day-boundary"
    gap_rows.append({
        "row_before_pos": i,
        "row_after_pos": i + 1,
        "ts_before_utc": t0.isoformat(),
        "ts_after_utc": t1.isoformat(),
        "gap_seconds": gap.total_seconds(),
        "gap_str": str(gap),
        "date_before": str(d0),
        "date_after": str(d1),
        "class": kind,
    })

gaps_df = pd.DataFrame(gap_rows)
n_total = len(gaps_df)
n_intra = int((gaps_df["class"] == "intra-day").sum()) if n_total else 0
n_bound = n_total - n_intra
print(f"\ntotal >60s gaps: {n_total} ({n_bound} day-boundary, {n_intra} intra-day)")

intra = gaps_df[gaps_df["class"] == "intra-day"]
print("\nINTRA-DAY GAPS:")
print(intra.to_string(index=False))
print("\nintra-day gap dates:", sorted(intra["date_before"].unique()))

# ---------- (b) per-horizon stretched same-day pairs ----------
arr = ts_utc.values  # datetime64[ns] UTC
dates = ts_utc.normalize().values  # midnight-normalized for date equality
horizon_rows = []
for h in (5, 10, 30, 60):
    a = arr[:-h]
    b = arr[h:]
    same_day = dates[:-h] == dates[h:]
    span = b - a
    stretched = same_day & (span > np.timedelta64(h, "s"))
    count = int(stretched.sum())
    if count:
        spans = span[stretched]
        worst = spans.max()
        worst_idx_local = int(np.nonzero(stretched)[0][np.argmax(spans)])
        worst_i = worst_idx_local
        worst_t0 = pd.Timestamp(arr[worst_i]).isoformat()
        worst_t1 = pd.Timestamp(arr[worst_i + h]).isoformat()
        worst_td = pd.Timedelta(worst)
        worst_str = str(worst_td)
        worst_secs = worst_td.total_seconds()
        # date attribution of stretched pairs
        pair_dates = pd.Series(dates[:-h][stretched]).dt.date.astype(str)
        date_counts = pair_dates.value_counts().sort_index()
        dates_summary = "; ".join(f"{d}:{c}" for d, c in date_counts.items())
    else:
        worst_str, worst_secs, worst_t0, worst_t1, dates_summary = "", "", "", "", ""
    horizon_rows.append({
        "horizon_s": h,
        "stretched_same_day_pairs": count,
        "worst_span": worst_str,
        "worst_span_seconds": worst_secs,
        "worst_pair_t0_utc": worst_t0,
        "worst_pair_t1_utc": worst_t1,
        "pair_dates": dates_summary,
    })

hz_df = pd.DataFrame(horizon_rows)
print("\nPER-HORIZON STRETCHED SAME-DAY PAIRS:")
print(hz_df.to_string(index=False))

# ---------- write CSV (two sections, one file) ----------
buf = io.StringIO()
buf.write("# V2 re-anchor gap derivation from lattice timestamps\n")
buf.write(f"# source: {PKL}\n")
buf.write(f"# rows: {len(df)}; timestamp tz: {tz_note}; monotonic: {ts.is_monotonic_increasing}\n")
buf.write(f"# section 1: all consecutive row-spacing gaps > 60 s "
          f"({n_total} total: {n_bound} day-boundary, {n_intra} intra-day)\n")
gaps_df.to_csv(buf, index=False)
buf.write("\n# section 2: per-horizon stretched same-day pairs "
          "(rows i,i+h positional; same UTC date; span > h seconds)\n")
hz_df.to_csv(buf, index=False)
with open(OUT, "w", newline="") as f:
    f.write(buf.getvalue())
print("\nwrote:", OUT)
