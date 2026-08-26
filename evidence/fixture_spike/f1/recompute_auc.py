"""F1 reference recompute: AUC from stored Phase 7 prediction parquets.

Reads (READ-ONLY) every *_predictions.parquet under
  C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\results\\phase7\\l2_predictions        (side=pre)
  C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\results\\phase7_fixed\\l2_predictions  (side=post)

For each parquet:
  - load [pred_score, true_label, fwd_move_ticks]
  - count NaN pred/label rows; drop them ONLY if present (n_nan_* columns report this)
  - compute sklearn.metrics.roc_auc_score(true_label, pred_score)
  - record row counts and zero-tick diagnostics:
      n_rows            total rows in parquet
      n_nan_pred        NaN in pred_score
      n_nan_label       NaN in true_label
      n_used            rows used for AUC after NaN drop
      n_zero_tick       rows with fwd_move_ticks == 0
      n_nan_fwd         rows with fwd_move_ticks NaN
      n_label_pos       rows with true_label == 1
      n_label_eq_signpos  rows where true_label == int(fwd_move_ticks > 0)

Output: deterministic CSV (sorted file order, fixed float formats) to argv[1].
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

ARCHIVE = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
SIDES = [
    ("pre", ARCHIVE / "results" / "phase7" / "l2_predictions"),
    ("post", ARCHIVE / "results" / "phase7_fixed" / "l2_predictions"),
]


def main(out_csv: str) -> None:
    rows = []
    for side, d in SIDES:
        files = sorted(d.glob("*_predictions.parquet"), key=lambda p: p.name)
        for f in files:
            instrument, model, horizon, _ = f.name.split("_")
            df = pd.read_parquet(f, columns=["pred_score", "true_label", "fwd_move_ticks"])
            n_rows = len(df)
            n_nan_pred = int(df["pred_score"].isna().sum())
            n_nan_label = int(df["true_label"].isna().sum())
            use = df
            if n_nan_pred or n_nan_label:
                use = df.dropna(subset=["pred_score", "true_label"])
            n_used = len(use)
            auc = roc_auc_score(use["true_label"].to_numpy(), use["pred_score"].to_numpy())
            fwd = df["fwd_move_ticks"]
            n_nan_fwd = int(fwd.isna().sum())
            n_zero_tick = int((fwd == 0).sum())
            n_label_pos = int((df["true_label"] == 1).sum())
            sign_pos = (fwd > 0).astype("int64")
            n_label_eq_signpos = int((df["true_label"].to_numpy() == sign_pos.to_numpy()).sum())
            rows.append(
                {
                    "side": side,
                    "instrument": instrument.upper(),
                    "model": model,
                    "horizon": horizon,
                    "file": f.name,
                    "n_rows": n_rows,
                    "n_nan_pred": n_nan_pred,
                    "n_nan_label": n_nan_label,
                    "n_used": n_used,
                    "recomputed_auc": f"{auc:.10f}",
                    "n_zero_tick": n_zero_tick,
                    "n_nan_fwd": n_nan_fwd,
                    "n_label_pos": n_label_pos,
                    "n_label_eq_signpos": n_label_eq_signpos,
                }
            )
            print(f"{side} {f.name}: rows={n_rows} auc={auc:.10f}", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(out_csv, index=False, lineterminator="\n")
    print(f"wrote {out_csv} ({len(out)} rows)")


if __name__ == "__main__":
    main(sys.argv[1])
