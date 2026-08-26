"""F2 check (d)(i) SELF-CONSISTENCY: corrected[t] == contaminated[t-1] for every
lagged column; exempt columns identical at same t; corrected row 0 NaN in lagged cols.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_F2 = Path(__file__).resolve().parent
sys.path.insert(0, str(_F2))
from fixture import apply_universal_lag  # only to reproduce the exempt-scope sets

cont = pd.read_pickle(_F2 / "out" / "contaminated_zc_2025-01_run1.pkl")
corr = pd.read_pickle(_F2 / "out" / "corrected_zc_2025-01_run1.pkl")

assert list(cont.columns) == list(corr.columns), "column sets differ"
assert len(cont) == len(corr), "row counts differ"

# Recompute the exempt/lagged split exactly as the wrapper does
EXEMPT_COLS = {"timestamp", "mid_price", "month", "ts_floor", "hour_utc"}
label_cols = {c for c in cont.columns if c.startswith("fwd_move_ticks_")}
raw_book_cols = {f"bid_price_{i}" for i in range(1, 6)} | \
                {f"ask_price_{i}" for i in range(1, 6)} | \
                {f"bid_size_{i}" for i in range(2, 6)} | \
                {f"ask_size_{i}" for i in range(2, 6)} | \
                {"spread", "book_imbalance"}
exempt = EXEMPT_COLS | label_cols | raw_book_cols
lagged_cols = [c for c in cont.columns if c not in exempt]
exempt_cols_present = [c for c in cont.columns if c in exempt]

results = {"n_rows": len(cont), "n_lagged_cols": len(lagged_cols),
           "n_exempt_cols_present": len(exempt_cols_present),
           "lagged_cols": lagged_cols, "exempt_cols_present": exempt_cols_present}

# 1) Lagged columns: corr.iloc[1:] must equal cont.iloc[:-1] (NaN placement identical)
max_abs = 0.0
worst_col = None
nan_mismatch_total = 0
value_mismatch_total = 0
row0_not_nan = []
for c in lagged_cols:
    a = corr[c].to_numpy()[1:]
    b = cont[c].to_numpy()[:-1]
    if a.dtype.kind in "fciu" and b.dtype.kind in "fciu":
        a = a.astype(float); b = b.astype(float)
        nan_a, nan_b = np.isnan(a), np.isnan(b)
        nan_mismatch = int((nan_a != nan_b).sum())
        both = ~nan_a & ~nan_b
        diff = np.abs(a[both] - b[both])
        m = float(diff.max()) if both.any() else 0.0
        vm = int((diff > 0).sum())
    else:
        # non-numeric lagged column (e.g. datetime ts_floor is exempt; shouldn't hit)
        eq = pd.Series(a).eq(pd.Series(b)) | (pd.Series(a).isna() & pd.Series(b).isna())
        nan_mismatch = 0
        vm = int((~eq).sum())
        m = float(vm > 0)
    nan_mismatch_total += nan_mismatch
    value_mismatch_total += vm
    if m > max_abs:
        max_abs = m; worst_col = c
    v0 = corr[c].iloc[0]
    if not (pd.isna(v0)):
        row0_not_nan.append((c, repr(v0)))

results["lagged_max_abs_diff"] = max_abs
results["lagged_worst_col"] = worst_col
results["lagged_nan_placement_mismatches"] = nan_mismatch_total
results["lagged_value_mismatches"] = value_mismatch_total
results["corrected_row0_non_nan_lagged"] = row0_not_nan

# 2) Exempt columns: identical at same index
exempt_mismatch = {}
for c in exempt_cols_present:
    s1, s2 = cont[c], corr[c]
    eq = s1.eq(s2) | (s1.isna() & s2.isna())
    n_bad = int((~eq).sum())
    if n_bad:
        exempt_mismatch[c] = n_bad
results["exempt_col_mismatches"] = exempt_mismatch

print(json.dumps(results, indent=2, default=str))
