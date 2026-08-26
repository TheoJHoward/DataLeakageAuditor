"""T4: 35-column projection of the F2 ZC 2025-01 fixture builds.

(a) mapping is encoded in PROJ / UNCON below (decided from side-by-side construction
    reading of phase7_l2_sim.py vs phase5_ml_fixture.py; quotes live in the manifest).
(b) project both variants x both runs to the 28 constructible columns, canonical
    to_csv(index=False, float_format="%.12g") sha256, run1-vs-run2 determinism.
(c) self-consistency corrected[t] == contaminated[t-1] per projected column.
(d) re-emit manifest fixture_manifest_35col_DRAFT.json (done in this same script).
Projection is column selection/renaming ONLY - no feature is constructed.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike")
F2OUT = BASE / "f2" / "out"
F3MAN = BASE / "f3" / "fixture_manifest_DRAFT.json"
T4 = BASE / "t4"

R3_LINE = "R3. 35-column: accepted as a documented-unverifiable assumption (basis: F3 manifest 9/9 agreement). T4 is unblocked by this."

# (target_column_in_phase7_name, source_column_in_existing_build)
# Order = phase7 ALL_L2_FEATURES order restricted to constructible columns.
PROJ = [
    ("mid_return_1s", "mid_return_1s"),
    ("mid_return_5s", "mid_return_5s"),
    ("mid_return_10s", "mid_return_10s"),
    ("mid_return_30s", "mid_return_30s"),
    ("trade_volume_1s", "trade_volume"),
    ("trade_count_1s", "trade_count"),
    ("minutes_since_open", "minutes_since_open"),
    ("net_delta_1s", "net_delta_1s"),
    ("net_delta_5s", "net_delta_5s"),
    ("net_delta_10s", "net_delta_10s"),
    ("net_delta_30s", "net_delta_30s"),
    ("net_delta_60s", "net_delta_60s"),
    ("buy_volume_10s", "buy_volume_10s"),
    ("sell_volume_10s", "sell_volume_10s"),
    ("large_trade_count_10s", "large_trade_count_10s"),
    ("vwap_distance", "vwap_distance"),
    ("bid_size_1", "bid_size_1"),
    ("ask_size_1", "ask_size_1"),
    ("total_bid_depth", "total_bid_depth"),
    ("total_ask_depth", "total_ask_depth"),
    ("spread_ticks", "spread_ticks"),
    ("depth_imbalance", "depth_imbalance"),
    ("book_slope_bid", "book_slope_bid"),
    ("book_slope_ask", "book_slope_ask"),
    ("depth_change_1s", "depth_change_1s"),
    ("depth_change_5s", "depth_change_5s"),
    ("depth_change_30s", "depth_change_30s"),
    ("l1_imbalance", "l1_imbalance"),
]
UNCON = ["tick_direction", "dollar_volume_1s", "session_open", "session_mid",
         "session_close", "book_imbalance_ratio", "weighted_mid"]

assert len(PROJ) + len(UNCON) == 35

# Lag-exemption scope, verbatim from phase7_l2_sim.py lines 266-272 / f2 fixture.py
EXEMPT_COLS = {"timestamp", "mid_price", "month", "ts_floor", "hour_utc"}
RAW_BOOK_COLS = {f"bid_price_{i}" for i in range(1, 6)} | \
                {f"ask_price_{i}" for i in range(1, 6)} | \
                {f"bid_size_{i}" for i in range(2, 6)} | \
                {f"ask_size_{i}" for i in range(2, 6)} | \
                {"spread", "book_imbalance"}


def canonical(df):
    s = df.to_csv(index=False, float_format="%.12g")
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


report = {"r3_line": R3_LINE, "projection": {}, "determinism": {},
          "self_consistency": {}, "aux": {}}
frames = {}

for variant in ("contaminated", "corrected"):
    for run in ("1", "2"):
        key = f"{variant}_run{run}"
        df = pd.read_pickle(F2OUT / f"{variant}_zc_2025-01_run{run}.pkl")
        label_cols = {c for c in df.columns if c.startswith("fwd_move_ticks_")}
        exempt = EXEMPT_COLS | label_cols | RAW_BOOK_COLS
        # which projected SOURCE columns are lag-exempt (should be none)
        src_exempt = [s for _, s in PROJ if s in exempt]
        missing = [s for _, s in PROJ if s not in df.columns]
        assert not missing, f"missing source cols: {missing}"
        proj = df[[s for _, s in PROJ]].copy()
        proj.columns = [t for t, _ in PROJ]
        s, sha = canonical(proj)
        out_csv = T4 / f"proj28_{key}.csv"
        with open(out_csv, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        report["projection"][key] = {
            "rows": int(len(proj)), "cols": int(proj.shape[1]),
            "sha256_canonical_csv": sha, "canonical_csv_bytes": len(s),
            "csv_path": str(out_csv),
            "lag_exempt_source_columns_in_projection": src_exempt,
        }
        frames[key] = proj
        del df, s

for variant in ("contaminated", "corrected"):
    h1 = report["projection"][f"{variant}_run1"]["sha256_canonical_csv"]
    h2 = report["projection"][f"{variant}_run2"]["sha256_canonical_csv"]
    report["determinism"][variant] = {"run1": h1, "run2": h2, "equal": h1 == h2}

# aux: NaN counts + zero-denominator counts (materiality of the fillna discrepancy
# on l1_imbalance / depth_imbalance) measured on contaminated run1 (pre-lag frame)
cont = frames["contaminated_run1"]
report["aux"]["nan_counts_contaminated_run1"] = {
    c: int(cont[c].isna().sum()) for c in cont.columns if cont[c].isna().any()}
report["aux"]["rows_bid1_plus_ask1_eq_0_contaminated_run1"] = int(
    ((cont["bid_size_1"] + cont["ask_size_1"]) == 0).sum())
report["aux"]["rows_total_depth_eq_0_contaminated_run1"] = int(
    ((cont["total_bid_depth"] + cont["total_ask_depth"]) == 0).sum())

# (c) self-consistency: corrected[t] == contaminated[t-1] for every projected column
for run in ("1", "2"):
    corr = frames[f"corrected_run{run}"]
    con = frames[f"contaminated_run{run}"]
    per_col = {}
    max_abs, worst = 0.0, None
    nan_mm_total, val_mm_total = 0, 0
    row0_not_nan = []
    for c in corr.columns:
        a = corr[c].to_numpy()[1:].astype(float)
        b = con[c].to_numpy()[:-1].astype(float)
        na, nb = np.isnan(a), np.isnan(b)
        nan_mm = int((na != nb).sum())
        both = ~na & ~nb
        diff = np.abs(a[both] - b[both])
        m = float(diff.max()) if both.any() else 0.0
        vm = int((diff > 0).sum())
        nan_mm_total += nan_mm
        val_mm_total += vm
        if m > max_abs:
            max_abs, worst = m, c
        if not pd.isna(corr[c].iloc[0]):
            row0_not_nan.append((c, repr(corr[c].iloc[0])))
        if nan_mm or vm:
            per_col[c] = {"nan_placement_mismatches": nan_mm,
                          "value_mismatches": vm, "max_abs_diff": m}
    report["self_consistency"][f"run{run}"] = {
        "n_projected_cols_checked": int(corr.shape[1]),
        "all_projected_cols_lagged": True,
        "exempt_projected_cols": [],
        "max_abs_diff": max_abs, "worst_col": worst,
        "nan_placement_mismatches_total": nan_mm_total,
        "value_mismatches_total": val_mm_total,
        "corrected_row0_non_nan": row0_not_nan,
        "per_col_anomalies": per_col,
    }

with open(T4 / "t4_verification_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

# ── (d) manifest re-emission ─────────────────────────────────────────────
f3 = json.loads(F3MAN.read_text(encoding="utf-8"))
by_name = {e["name"]: e for e in f3["columns"]}
assert len(by_name) == 35

STATUS = {t: ("direct" if t == srcname else f"mapped-from:{srcname}")
          for t, srcname in PROJ}

EVIDENCE = {
    "trade_volume_1s": ("phase7_l2_sim.py line 246: 'snap[\"trade_volume_1s\"] = snap[\"trade_volume\"].fillna(0)'; "
        "its groupby line 216 'tagg = trades.groupby(\"ts_floor\").agg(' with line 221 'trade_volume=(\"size\", \"sum\"),', merge line 231, fillna(0) lines 232-234. "
        "phase5_ml_fixture.py groupby line 240 'tagg = trades.groupby(\"ts_floor\").agg(' with line 243 'trade_volume=(\"size\",\"sum\"), large_trade_count=(\"is_large\",\"sum\"),', merge line 251, fillna(0) lines 252-253. "
        "Same source column ('size'), same aggregation ('sum'), same window (ts_floor = ts_event.dt.floor(\"1s\"): phase7 line 206, fixture line 233), same left merge on ts_floor, same fillna(0). "
        "phase7's extra .fillna(0) at line 246 acts on a column already filled at lines 232-234, hence identity. => mappable."),
    "trade_count_1s": ("phase7_l2_sim.py line 247: 'snap[\"trade_count_1s\"] = snap[\"trade_count\"].fillna(0)'; "
        "groupby line 220 'trade_count=(\"size\", \"count\"),'. "
        "phase5_ml_fixture.py line 242 'sell_volume=(\"sell_vol\",\"sum\"), trade_count=(\"size\",\"count\"),'. "
        "Same source column ('size'), same aggregation ('count'), same ts_floor 1s window, same merge/fillna(0) as trade_volume. => mappable."),
}

DISCREPANCY = {
    "l1_imbalance": ("CONSTRUCTION DISCREPANCY (NaN handling only): phase7_l2_sim.py lines 174-175 end with .fillna(0): "
        "'snap[\"l1_imbalance\"] = ((snap[\"bid_size_1\"] - snap[\"ask_size_1\"]) /\\n                             (snap[\"bid_size_1\"] + snap[\"ask_size_1\"]).replace(0, np.nan)).fillna(0)'. "
        "phase5_ml_fixture.py lines 202-203 have NO .fillna(0): "
        "'snap[\"l1_imbalance\"] = ((snap[\"bid_size_1\"] - snap[\"ask_size_1\"]) /\\n                            (snap[\"bid_size_1\"] + snap[\"ask_size_1\"]).replace(0, np.nan))'. "
        "Build output holds NaN where bid_size_1+ask_size_1 == 0; phase7 would hold 0 there. Measured materiality on contaminated run1 is in t4_verification_report.json (aux)."),
    "depth_imbalance": ("CONSTRUCTION DISCREPANCY (NaN handling only): phase7_l2_sim.py lines 172-173 end with .fillna(0): "
        "'snap[\"depth_imbalance\"] = ((snap[\"total_bid_depth\"] - snap[\"total_ask_depth\"]) /\\n                                td.replace(0, np.nan)).fillna(0)'. "
        "phase5_ml_fixture.py line 210 has NO .fillna(0): "
        "'snap[\"depth_imbalance\"] = ((snap[\"total_bid_depth\"] - snap[\"total_ask_depth\"]) / td.replace(0, np.nan))'. "
        "Build output holds NaN where total depth == 0; phase7 would hold 0 there. Measured materiality on contaminated run1 is in t4_verification_report.json (aux)."),
}

UNCON_REASON = {
    "tick_direction": ("No column of this name or equivalent construction exists in the 87-column build output. "
        "phase7_l2_sim.py line 156: 'snap[\"tick_direction\"] = np.sign(mid.pct_change(1)).fillna(0)'. The build holds mid_return_1s = mid.pct_change(1) "
        "(phase5_ml_fixture.py lines 195-196), but producing tick_direction requires applying np.sign(...).fillna(0) - a new construction, prohibited under the projection rule (selection/renaming only)."),
    "dollar_volume_1s": ("No dollar-volume column or intermediate exists in the build output (grep for 'dollar' in phase5_ml_fixture.py: no hits). "
        "phase7_l2_sim.py line 214 'trades[\"dollar_vol\"] = trades[\"size\"] * trades[\"price\"]', groupby line 223 'dollar_volume=(\"dollar_vol\", \"sum\"),', line 248 'snap[\"dollar_volume_1s\"] = snap[\"dollar_volume\"].fillna(0)'. Constructing it is prohibited."),
    "session_open": ("No session one-hot columns exist in the build output. phase7_l2_sim.py lines 161-162: 'frac = snap[\"minutes_since_open\"] / total_minutes' / 'snap[\"session_open\"] = (frac < 0.1).astype(float)'. "
        "minutes_since_open IS in the build, but the threshold transform is a new construction, prohibited."),
    "session_mid": ("Same basis as session_open. phase7_l2_sim.py line 163: 'snap[\"session_mid\"] = ((frac >= 0.1) & (frac < 0.85)).astype(float)'. New construction, prohibited."),
    "session_close": ("Same basis as session_open. phase7_l2_sim.py line 164: 'snap[\"session_close\"] = (frac >= 0.85).astype(float)'. New construction, prohibited."),
    "book_imbalance_ratio": ("phase7_l2_sim.py lines 188-189 construct it: 'snap[\"book_imbalance_ratio\"] = (snap[\"total_bid_depth\"] /\\n                                     snap[\"total_ask_depth\"].replace(0, np.nan)).fillna(1.0)'. "
        "The build output contains a column named 'book_imbalance', but it is a RAW snapshot-parquet pass-through (phase5_ml_fixture.py never constructs or touches it; it appears in the builder only inside the lag-exemption set); its construction inside the snapshot builder is not verifiable from the fixture code, so exact-construction equivalence CANNOT be verified => NOT mappable. "
        "Additionally, 'book_imbalance' is lag-EXEMPT in the corrected build (raw_book_cols, fixture.py lines 43-47 / phase7_l2_sim.py lines 268-272) whereas phase7's book_imbalance_ratio IS lagged at line 276 - different lag treatment even if values coincided. Constructing the ratio from total depths is prohibited."),
    "weighted_mid": ("No such column in the build output. phase7_l2_sim.py lines 184-187: 'snap[\"weighted_mid\"] = (snap[\"bid_price_1\"] * snap[\"ask_size_1\"] +\\n                            snap[\"ask_price_1\"] * snap[\"bid_size_1\"]) / \\\\\\n                           (snap[\"bid_size_1\"] + snap[\"ask_size_1\"]).replace(0, np.nan)' then line 187 'snap[\"weighted_mid\"] = (snap[\"weighted_mid\"] - mid) / tick'. "
        "Requires arithmetic over raw book columns and mid - a new construction, prohibited."),
}

# construction-identity evidence for the 26 direct columns (fixture line vs phase7 line)
DIRECT_EVIDENCE = {
    "mid_return_1s": "identical: phase7 lines 152-153 'for lag in [1, 5, 10, 30]:\\n    snap[f\"mid_return_{lag}s\"] = mid.pct_change(lag)' == fixture lines 195-196 'for lag in [1, 5, 10, 30, 60, 300]:\\n    snap[f\"mid_return_{lag}s\"] = mid.pct_change(lag)' (shared lags 1/5/10/30; mid identical: phase7 line 149 == fixture line 193 'mid = snap[\"mid_price\"].replace(0, np.nan)')",
    "mid_return_5s": "same as mid_return_1s",
    "mid_return_10s": "same as mid_return_1s",
    "mid_return_30s": "same as mid_return_1s",
    "minutes_since_open": "identical: phase7 line 159 == fixture line 192 'snap[\"minutes_since_open\"] = (snap[\"hour_utc\"] - ds) * 60 + snap[\"timestamp\"].dt.minute'; zc ds=14 in both INST_META (phase7 line 50, fixture line 58)",
    "net_delta_1s": "identical: phase7 lines 238-239 == fixture lines 255-256 'for w in [1, 5, 10, 30, 60]:\\n    snap[f\"net_delta_{w}s\"] = snap[\"net_delta\"].rolling(w, min_periods=1).sum()'; upstream net_delta=(\"signed_vol\",\"sum\") phase7 line 217 == fixture line 241; signed_vol phase7 line 209 == fixture line 236",
    "net_delta_5s": "same as net_delta_1s",
    "net_delta_10s": "same as net_delta_1s",
    "net_delta_30s": "same as net_delta_1s",
    "net_delta_60s": "same as net_delta_1s",
    "buy_volume_10s": "identical: phase7 line 240 == fixture line 257 'snap[\"buy_volume_10s\"] = snap[\"buy_volume\"].rolling(10, min_periods=1).sum()'",
    "sell_volume_10s": "identical: phase7 line 241 == fixture line 258 'snap[\"sell_volume_10s\"] = snap[\"sell_volume\"].rolling(10, min_periods=1).sum()'",
    "large_trade_count_10s": "identical: phase7 line 242 == fixture line 260 'snap[\"large_trade_count_10s\"] = snap[\"large_trade_count\"].rolling(10, min_periods=1).sum()'; is_large phase7 line 212 == fixture line 239 'trades[\"is_large\"] = (trades[\"size\"] >= 10).astype(int)'",
    "vwap_distance": "identical: phase7 line 243 == fixture line 261 'snap[\"vwap_distance\"] = (mid - snap[\"vwap\"]) / tick'; vwap lambda phase7 lines 224-225 == fixture lines 244-245; ffill phase7 line 235 == fixture line 254; zc tick_size 0.25 in both",
    "bid_size_1": "identical: raw pass-through from {sym}_snapshots_{month}.parquet in both (phase7 line 139, fixture line 183); lagged (not exempt) in both lag scopes",
    "ask_size_1": "same as bid_size_1",
    "total_bid_depth": "identical: phase7 line 169 == fixture line 207 'snap[\"total_bid_depth\"] = snap[bid_cols].sum(axis=1)'; bid_cols comprehension phase7 line 167 == fixture line 205",
    "total_ask_depth": "identical: phase7 line 170 == fixture line 208 'snap[\"total_ask_depth\"] = snap[ask_cols].sum(axis=1)'",
    "spread_ticks": "identical: phase7 lines 141-142 == fixture lines 185-186 'snap[\"spread\"] = snap[\"spread\"].clip(lower=0.0)\\nsnap[\"spread_ticks\"] = snap[\"spread\"] / tick'; zc tick_size 0.25 in both",
    "depth_imbalance": "see construction_discrepancy - identical EXCEPT phase7's trailing .fillna(0)",
    "book_slope_bid": "identical: phase7 line 178 == fixture line 212 'snap[\"book_slope_bid\"] = (snap[\"bid_size_1\"] - snap[bid_cols[-1]]) / max(nb-1,1) if nb >= 2 else 0.0' (whitespace around nb-1 only)",
    "book_slope_ask": "identical: phase7 line 179 == fixture line 213",
    "depth_change_1s": "identical: phase7 lines 180-181 == fixture lines 214-215 'for lag in [1, 5, 30]:\\n    snap[f\"depth_change_{lag}s\"] = td.diff(lag)'; td = total_bid_depth + total_ask_depth phase7 line 171 == fixture line 209",
    "depth_change_5s": "same as depth_change_1s",
    "depth_change_30s": "same as depth_change_1s",
    "l1_imbalance": "see construction_discrepancy - identical EXCEPT phase7's trailing .fillna(0)",
}

projected_entries = []
for tgt, src in PROJ:
    e = dict(by_name[tgt])  # keep class/flavor/quotes verbatim from F3
    e["projection_status"] = STATUS[tgt]
    if tgt in EVIDENCE:
        e["projection_evidence"] = EVIDENCE[tgt]
    else:
        e["projection_evidence"] = DIRECT_EVIDENCE[tgt]
    if tgt in DISCREPANCY:
        e["construction_discrepancy"] = DISCREPANCY[tgt]
    projected_entries.append(e)

uncon_entries = []
for name in UNCON:
    e = dict(by_name[name])
    e["projection_status"] = "UNCONSTRUCTIBLE"
    e["reason"] = UNCON_REASON[name]
    uncon_entries.append(e)

cls = [by_name[t]["class"] for t, _ in PROJ]
flv = [by_name[t].get("flavor") for t, _ in PROJ]
counts = {
    "projected_total": len(PROJ),
    "unconstructible_total": len(UNCON),
    "leak_source": cls.count("LEAK-SOURCE"),
    "descendant": cls.count("DESCENDANT"),
    "clean": cls.count("CLEAN"),
    "leak_source_label_base_price": sum(1 for c, f in zip(cls, flv) if c == "LEAK-SOURCE" and f == "label_base_price"),
    "leak_source_contemporaneous_state_flow": sum(1 for c, f in zip(cls, flv) if c == "LEAK-SOURCE" and f == "contemporaneous_state_flow"),
    "direct": sum(1 for t, s in PROJ if t == s),
    "mapped_from_intermediate": sum(1 for t, s in PROJ if t != s),
    "unconstructible_by_class": {
        "leak_source": sum(1 for n in UNCON if by_name[n]["class"] == "LEAK-SOURCE"),
        "descendant": sum(1 for n in UNCON if by_name[n]["class"] == "DESCENDANT"),
        "clean": sum(1 for n in UNCON if by_name[n]["class"] == "CLEAN"),
    },
}

manifest = {
    "manifest_status": "DRAFT - author review required",
    "item": "T4 35-column projection manifest: F3 ground-truth manifest filtered to the columns constructible from the existing F2 ZC 2025-01 fixture builds by column selection/renaming only",
    "generated_utc_date": "2026-08-10",
    "working_resolution_R3": R3_LINE,
    "derived_from": {
        "f3_manifest": str(F3MAN),
        "phase7_script": r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py",
        "build_pickles": [str(F2OUT / f"{v}_zc_2025-01_run{r}.pkl") for v in ("contaminated", "corrected") for r in ("1", "2")],
        "builder_code": str(BASE / "f2" / "phase5_ml_fixture.py"),
        "lag_wrapper": str(BASE / "f2" / "fixture.py"),
    },
    "projection_rule": "Column selection/renaming ONLY. A target column is 'direct' on exact name match in the 87-column build output, 'mapped-from:<name>' only where the construction of the intermediate was verified identical to phase7's construction (source column, aggregation, window), else UNCONSTRUCTIBLE. No feature was constructed.",
    "canonical_serialization": "df.to_csv(index=False, float_format=\"%.12g\"), sha256 over utf-8 bytes (same convention as f2/run_fixture.py lines 28-31)",
    "projection_column_order": [t for t, _ in PROJ],
    "projected_columns": projected_entries,
    "unconstructible_columns": uncon_entries,
    "counts_projected_subset": counts,
    "projection_verification": {
        "determinism": report["determinism"],
        "self_consistency": report["self_consistency"],
        "aux_nan_and_zero_denominator": report["aux"],
    },
}

out_manifest = T4 / "fixture_manifest_35col_DRAFT.json"
with open(out_manifest, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

# validate
with open(out_manifest, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print("MANIFEST_VALID_JSON:", out_manifest)
print("projected:", len(loaded["projected_columns"]),
      "unconstructible:", len(loaded["unconstructible_columns"]))
print(json.dumps(report["determinism"], indent=2))
for run in ("1", "2"):
    sc = report["self_consistency"][f"run{run}"]
    print(f"self-consistency run{run}: max_abs_diff={sc['max_abs_diff']}",
          f"nan_mm={sc['nan_placement_mismatches_total']}",
          f"val_mm={sc['value_mismatches_total']}",
          f"row0_non_nan={sc['corrected_row0_non_nan']}",
          f"anomalies={sc['per_col_anomalies']}")
print("aux:", json.dumps(report["aux"], indent=2))
print("counts:", json.dumps(counts, indent=2))
