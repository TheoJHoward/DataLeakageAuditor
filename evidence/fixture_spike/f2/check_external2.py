"""F2 check (d)(ii) EXTERNAL, refined: restrict to timestamps that are UNIQUE on
both sides (builder lattice and stored parquet), so a timestamp join is exact row
identity. Also quantify the duplicate-timestamp structure honestly.
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

vc_b = b["timestamp"].value_counts()
report = {
    "builder_rows_2025_08": int(len(b)),
    "builder_distinct_ts": int(len(vc_b)),
    "builder_ts_with_dup": int((vc_b > 1).sum()),
    "builder_max_dup": int(vc_b.max()),
}
b_uni = b[b["timestamp"].map(vc_b) == 1]
report["builder_rows_ts_unique"] = int(len(b_uni))

# raw snapshot duplication for context
snap = pq.read_table(str(ARCHIVE / "processed" / "zc" / "zc_snapshots_2025-08.parquet"),
                     columns=["timestamp"]).to_pandas()
vc_s = pd.to_datetime(snap["timestamp"]).value_counts()
report["raw_snapshot_rows"] = int(len(snap))
report["raw_snapshot_ts_with_dup"] = int((vc_s > 1).sum())
report["raw_snapshot_max_dup"] = int(vc_s.max())

for arch in ["LightGBM", "XGBoost"]:
    st = pq.read_table(str(PRED / f"zc_{arch}_5_predictions_fixed.parquet")).to_pandas()
    st["timestamp"] = pd.to_datetime(st["timestamp"])
    aug = st[(st["timestamp"] >= "2025-08-01") & (st["timestamp"] < "2025-09-01")].copy()
    vc_a = aug["timestamp"].value_counts()
    a_uni = aug[aug["timestamp"].map(vc_a) == 1]

    m = a_uni.merge(b_uni, on="timestamp", how="inner")
    r = {"stored_rows_2025_08": int(len(aug)),
         "stored_ts_with_dup": int((vc_a > 1).sum()),
         "stored_rows_ts_unique": int(len(a_uni)),
         "n_matched_unique_both_sides": int(len(m))}
    if len(m):
        d_mid = (m["mid_price_t"] - m["mid_price"]).abs()
        d_fwd = (m["fwd_move_ticks"] - m["fwd_move_ticks_5s"]).abs()
        r["mid_price_max_abs_diff"] = float(d_mid.max())
        r["mid_price_n_mismatch"] = int((d_mid != 0).sum())
        r["fwd_move_max_abs_diff"] = float(d_fwd.max())
        r["fwd_move_n_mismatch"] = int((d_fwd != 0).sum())
        lbl = (m["fwd_move_ticks_5s"] > 0).astype(int)
        r["true_label_n_mismatch"] = int((m["true_label"].astype(int) != lbl).sum())
        # where fwd mismatches, show a few examples
        bad = m[d_fwd != 0]
        if len(bad):
            r["fwd_mismatch_examples"] = bad[["timestamp", "fwd_move_ticks",
                                              "fwd_move_ticks_5s", "mid_price_t",
                                              "mid_price"]].head(5).to_dict("records")
    report[arch] = r

print(json.dumps(report, indent=2, default=str))
