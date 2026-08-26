"""F1: compare recomputed AUCs (run1.csv) against recorded meta test_auc values."""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
ARCHIVE = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
META = {
    "pre": ARCHIVE / "results" / "phase7" / "l2_model_meta.csv",
    "post": ARCHIVE / "results" / "phase7_fixed" / "l2_model_meta.csv",
}

rec = pd.read_csv(HERE / "run1.csv", dtype={"recomputed_auc": float})
rec["horizon_s"] = rec["horizon"].str.rstrip("s").astype(int)

metas = []
for side, p in META.items():
    m = pd.read_csv(p)
    m["side"] = side
    metas.append(m[["side", "instrument", "architecture", "horizon_s", "test_auc", "n_test"]])
meta = pd.concat(metas, ignore_index=True)

out = rec.merge(
    meta,
    left_on=["side", "instrument", "model", "horizon_s"],
    right_on=["side", "instrument", "architecture", "horizon_s"],
    how="outer",
    indicator=True,
)
out["delta"] = out["recomputed_auc"] - out["test_auc"]
out["abs_delta"] = out["delta"].abs()
out["flag_gt_5e-5"] = out["abs_delta"] > 5e-5
out["rows_match_n_test"] = out["n_rows"] == out["n_test"]

cols = ["side", "instrument", "model", "horizon", "n_rows", "n_used", "n_zero_tick",
        "n_label_pos", "n_label_eq_signpos", "recomputed_auc", "test_auc", "n_test",
        "delta", "abs_delta", "flag_gt_5e-5", "rows_match_n_test", "_merge"]
out = out.sort_values(["side", "instrument", "model", "horizon_s"],
                      ascending=[False, True, True, True]).reset_index(drop=True)
final = out[cols].copy()
final.to_csv(HERE / "f1_results.csv", index=False, lineterminator="\n",
             float_format="%.10f")

pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)
print(final.to_string())
print("\n--- unmatched (parquet without meta row or vice versa) ---")
print(out[out["_merge"] != "both"][["side", "instrument", "model", "horizon", "architecture", "test_auc", "n_rows", "n_test"]].to_string())
print("\n--- flagged |delta| > 5e-5 ---")
flagged = out[(out["_merge"] == "both") & out["flag_gt_5e-5"]]
print(flagged[cols].to_string() if len(flagged) else "NONE")
print("\n--- max abs_delta among matched:", out.loc[out["_merge"] == "both", "abs_delta"].max())
print("--- any n_rows != n_test among matched:",
      (~out.loc[out["_merge"] == "both", "rows_match_n_test"]).sum())
print("--- any NaN pred/label anywhere:", int(rec["n_nan_pred"].sum() + rec["n_nan_label"].sum()))
print("--- any NaN fwd_move_ticks anywhere:", int(rec["n_nan_fwd"].sum()))
zt = rec[rec["n_zero_tick"] > 0]
print("--- files with zero-tick rows present:", len(zt), "of", len(rec))
print("--- files where true_label == (fwd>0) for ALL rows:",
      int((rec["n_label_eq_signpos"] == rec["n_rows"]).sum()), "of", len(rec))
