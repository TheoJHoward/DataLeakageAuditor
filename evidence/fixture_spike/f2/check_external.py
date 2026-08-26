"""F2 check (d)(ii) EXTERNAL: match the corrected fixture's ZC 2025-08 frame against
the stored post-fix prediction parquets that carry timestamps:
results/pc2_all_phases/phase7/l2_predictions/zc_{arch}_5_predictions_fixed.parquet
(schema: timestamp, pred_score, true_label, mid_price_t, fwd_move_ticks).

Checks, per architecture:
  1. every stored 2025-08 timestamp exists on the builder's snapshot lattice
  2. stored mid_price_t == builder mid_price at the same second (exempt from lag)
  3. stored fwd_move_ticks == builder fwd_move_ticks_5s at the same second
  4. stored true_label == (builder fwd_move_ticks_5s > 0)
Read-only on the archive.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

_F2 = Path(__file__).resolve().parent
ARCHIVE = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
PRED = ARCHIVE / "results" / "pc2_all_phases" / "phase7" / "l2_predictions"

corr = pd.read_pickle(_F2 / "out" / "corrected_zc_2025-08_run1.pkl")
b = corr[["timestamp", "mid_price", "fwd_move_ticks_5s"]].copy()
report = {"builder_rows_2025_08": int(len(b)),
          "builder_ts_unique": bool(b["timestamp"].is_unique)}

for arch in ["LightGBM", "XGBoost"]:
    p = PRED / f"zc_{arch}_5_predictions_fixed.parquet"
    st = pq.read_table(str(p)).to_pandas()
    st["timestamp"] = pd.to_datetime(st["timestamp"])
    aug = st[(st["timestamp"] >= "2025-08-01") & (st["timestamp"] < "2025-09-01")].copy()
    r = {"stored_rows_total": int(len(st)), "stored_rows_2025_08": int(len(aug)),
         "stored_ts_unique_in_aug": bool(aug["timestamp"].is_unique)}

    m = aug.merge(b, on="timestamp", how="left", indicator=True)
    unmatched = m[m["_merge"] != "both"]
    r["stored_aug_ts_not_on_builder_lattice"] = int(len(unmatched))

    both = m[m["_merge"] == "both"]
    r["n_matched"] = int(len(both))
    if len(both):
        d_mid = (both["mid_price_t"] - both["mid_price"]).abs()
        d_fwd = (both["fwd_move_ticks"] - both["fwd_move_ticks_5s"]).abs()
        r["mid_price max_abs_diff"] = float(d_mid.max())
        r["mid_price n_exact_equal"] = int((d_mid == 0).sum())
        r["fwd_move max_abs_diff"] = float(d_fwd.max()) if d_fwd.notna().any() else None
        r["fwd_move n_exact_equal"] = int((d_fwd == 0).sum())
        r["fwd_move n_nan_builder"] = int(both["fwd_move_ticks_5s"].isna().sum())
        r["fwd_move n_nan_stored"] = int(both["fwd_move_ticks"].isna().sum())
        lbl = (both["fwd_move_ticks_5s"] > 0).astype(int)
        r["true_label n_mismatch"] = int((both["true_label"].astype(int) != lbl).sum())
        r["stored fwd==0 rows (should be 0, zero-excluded)"] = int((both["fwd_move_ticks"] == 0).sum())
    report[arch] = r

print(json.dumps(report, indent=2, default=str))
