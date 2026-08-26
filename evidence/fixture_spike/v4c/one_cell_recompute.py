"""ITEM V4 -- one-cell recompute of the a4_runner net_delta cell (zc, v4_gapfill).

Reproduces, on real v4 input data, exactly what a4_runner.py does at:
  - line 218: pq.read_table(p, columns=["ts_event","price","size","is_buy_aggressor"]).to_pandas()
  - line 306: tr["second"] = tr["ts_event"].dt.floor("1s")
  - line 307: tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
  - lines 311-312: per_sec = tr.groupby("second").agg(net_delta=("signed_size","sum"))
  - line 655: X = df[feats].to_numpy(dtype=np.float32)   (simulated as np.float32(sum))

and, side by side, the AS-INTENDED computation (size cast to int64 BEFORE negation).

READ-ONLY on the archive. All output stays in this directory.
Claim under test: as-executed net_delta == 2**32 * sell_count + true_net_delta (exact in
uint64), and after the float32 cast the true-delta term is lost below precision, so the
stored feature encodes scaled sell-trade counts, not signed volume.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

SRC = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\v4_gapfill\zc_trades_tagged_2025-01.parquet")
OUT_DIR = Path(__file__).resolve().parent

lines = []
def emit(s=""):
    print(s)
    lines.append(s)

emit("# One-cell recompute: a4_runner net_delta on zc v4_gapfill (2025-01)")
emit()
emit(f"- pandas {pd.__version__}, numpy {np.__version__}, "
     f"pyarrow {__import__('pyarrow').__version__}, python {sys.version.split()[0]}")
emit(f"- source file (read-only): `{SRC}`")
emit(f"- instrument: **zc** (preferred per a4_runner.py:134-140 -> ROOT/processed/zc/v4_gapfill); "
     f"file exists, so no fallback to he/le needed")
emit()

# ---- (e) execution-witness: dtype at read time, exactly as a4_runner.py:218 loads it ----
tbl = pq.read_table(str(SRC), columns=["ts_event", "price", "size", "is_buy_aggressor"])
arrow_types = {f.name: str(f.type) for f in tbl.schema}
tr_full = tbl.to_pandas()
tr_full["ts_event"] = pd.to_datetime(tr_full["ts_event"], utc=True)  # a4_runner.py:219

emit("## (e) Loaded dtypes (execution witness)")
emit()
emit("| column | arrow type (parquet schema as read) | pandas dtype after .to_pandas() |")
emit("|---|---|---|")
for c in ["ts_event", "price", "size", "is_buy_aggressor"]:
    emit(f"| {c} | {arrow_types[c]} | {tr_full[c].dtype} |")
emit()
emit(f"- rows in month file: {len(tr_full):,}; "
     f"ts range {tr_full['ts_event'].min()} .. {tr_full['ts_event'].max()}")
emit()

# ---- (b) one session hour slice ----
# Pick the first day in the file, session hour 14:30-15:30 UTC (ZC floor session);
# if that hour has < 1000 trades, fall back to the busiest hour of that day.
day0 = tr_full["ts_event"].dt.floor("D").iloc[0]
h_start = day0 + pd.Timedelta(hours=14, minutes=30)
h_end = h_start + pd.Timedelta(hours=1)
tr = tr_full[(tr_full["ts_event"] >= h_start) & (tr_full["ts_event"] < h_end)].copy()
if len(tr) < 1000:
    hours = tr_full["ts_event"].dt.floor("h")
    busiest = hours.value_counts().idxmax()
    h_start, h_end = busiest, busiest + pd.Timedelta(hours=1)
    tr = tr_full[(tr_full["ts_event"] >= h_start) & (tr_full["ts_event"] < h_end)].copy()
emit(f"## (b) Session-hour slice: {h_start} .. {h_end}  ({len(tr):,} trades)")
emit()

# ---- the cell, exactly as executed (a4_runner.py:306-312) ----
tr["second"] = tr["ts_event"].dt.floor("1s")                                        # :306
with np.errstate(all="ignore"):
    tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool),
                                 tr["size"], -tr["size"])                            # :307 verbatim
emit(f"- signed_size dtype as executed: **{tr['signed_size'].dtype}** "
     f"(np.where(bool, uint32, -uint32) stays unsigned; negation wraps mod 2**32)")
per_sec_exec = tr.groupby("second").agg(net_delta=("signed_size", "sum")).reset_index()  # :311-312
emit(f"- groupby-sum net_delta dtype as executed: **{per_sec_exec['net_delta'].dtype}**")
emit()

# ---- as intended: int64 BEFORE negation, same aggregation ----
tr["signed_size_ok"] = np.where(tr["is_buy_aggressor"].astype(bool),
                                tr["size"].astype(np.int64),
                                -tr["size"].astype(np.int64))
per_sec_ok = tr.groupby("second").agg(net_delta=("signed_size_ok", "sum")).reset_index()
emit(f"- as-intended signed_size dtype: {tr['signed_size_ok'].dtype}; "
     f"as-intended net_delta dtype: {per_sec_ok['net_delta'].dtype}")
emit()

# per-second buy/sell counts for window selection and the claim check
cnt = tr.groupby("second").agg(
    buys=("is_buy_aggressor", lambda s: int(s.astype(bool).sum())),
    sells=("is_buy_aggressor", lambda s: int((~s.astype(bool)).sum())),
    n=("size", "size"),
).reset_index()

m = cnt.merge(per_sec_exec, on="second").merge(per_sec_ok, on="second", suffixes=("_exec", "_ok"))

# ---- pick the two windows ----
# window A: >=1 buy AND >=1 sell (prefer the one with the largest |true delta| so the
#           lost-precision term is as big as the hour offers)
# window B: >=2 sells
cand_a = m[(m.buys >= 1) & (m.sells >= 1)]
cand_b = m[m.sells >= 2]
if cand_a.empty or cand_b.empty:
    emit("**FAILED to find required windows in this hour -- rerun with another slice**")
    sys.exit(1)
win_a = cand_a.loc[cand_a["net_delta_ok"].abs().idxmax()]
win_b = cand_b.loc[cand_b["sells"].idxmax()]

emit("## (c)/(d) The two windows, side by side")
emit()
rows = []
for label, w in (("A: >=1 buy and >=1 sell", win_a), ("B: >=2 sells", win_b)):
    raw_exec = w["net_delta_exec"]              # uint64 raw sum, as executed
    f32_exec = np.float32(raw_exec)             # the line-655 cast, applied to this value
    intended = w["net_delta_ok"]                # int64 true net delta
    sells = int(w["sells"])
    strong = np.float32(np.uint64(2**32) * np.uint64(sells))
    identity_holds = (int(raw_exec) == 2**32 * sells + int(intended))
    rows.append((label, w["second"], int(w["buys"]), sells, int(w["n"]),
                 int(raw_exec), f32_exec, int(intended), strong,
                 identity_holds, f32_exec == strong,
                 float(f32_exec) - float(strong)))

emit("| window | second (UTC) | buys | sells | trades | as-executed raw (uint64) | as-executed float32 | as-intended (int64) | float32(2^32*sells) | raw == 2^32*sells + intended | f32_exec == f32(2^32*sells) | f32 diff |")
emit("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    emit(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]!r} | {r[7]} | {r[8]!r} | {r[9]} | {r[10]} | {r[11]} |")
emit()

# ---- hour-wide strong-form census, so the two windows are not cherry-picked ----
m["raw_identity"] = m.apply(
    lambda r: int(r["net_delta_exec"]) == 2**32 * int(r["sells"]) + int(r["net_delta_ok"]), axis=1)
m["f32_exec"] = m["net_delta_exec"].astype(np.float32)
m["f32_strong"] = (np.uint64(2**32) * m["sells"].astype(np.uint64)).astype(np.float32)
m["strong_form"] = m["f32_exec"] == m["f32_strong"]
n_windows = len(m)
n_id = int(m["raw_identity"].sum())
n_strong = int(m["strong_form"].sum())
n_with_sells = int((m["sells"] > 0).sum())
viol = m[~m["strong_form"]]
emit("## Hour-wide census (all 1-second windows in the slice)")
emit()
emit(f"- windows: {n_windows}; windows containing >=1 sell: {n_with_sells}")
emit(f"- raw identity `as_executed == 2^32*sells + true_delta` holds in **{n_id}/{n_windows}**")
emit(f"- strong form `float32(as_executed) == float32(2^32*sells)` holds in **{n_strong}/{n_windows}**")
if len(viol):
    emit(f"- strong-form violations: {len(viol)} -- largest |true delta| among them: "
         f"{int(viol['net_delta_ok'].abs().max())}; examples:")
    for _, r in viol.nlargest(3, "sells").iterrows():
        emit(f"    - {r['second']}: sells={int(r['sells'])}, true delta={int(r['net_delta_ok'])}, "
             f"f32_exec={r['f32_exec']!r}, f32_strong={r['f32_strong']!r}, "
             f"diff={float(r['f32_exec']) - float(r['f32_strong'])}")
emit()

# ---- measured float32 spacing at 2^32 * k ----
emit("## float32 spacing at 2^32 * k (measured, np.spacing)")
emit()
emit("| k (sell count) | value 2^32*k | np.spacing(float32(value)) | half-ulp (rounding radius) |")
emit("|---|---|---|---|")
for k in [1, 2, 3, 5, 10, 50, 100]:
    v = np.float32(np.uint64(2**32) * np.uint64(k))
    sp = np.spacing(v)
    emit(f"| {k} | {2**32 * k} | {sp} | {sp / 2} |")
emit()
emit("Any true-delta term with |delta| < half-ulp is rounded away entirely by the line-655 "
     "float32 cast; |delta| >= half-ulp survives only as a multiple of the ulp.")
emit()

# ---- true-delta magnitude in this hour, to compare against the spacing ----
emit(f"- true net_delta over the hour: min={int(m['net_delta_ok'].min())}, "
     f"max={int(m['net_delta_ok'].max())}, "
     f"max |delta|={int(m['net_delta_ok'].abs().max())}, "
     f"99th pct |delta|={float(m['net_delta_ok'].abs().quantile(0.99)):.1f}")
emit()

(OUT_DIR / "one_cell_recompute.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\n[written] {OUT_DIR / 'one_cell_recompute.md'}")
