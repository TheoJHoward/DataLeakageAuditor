# ============================================================================
# THROWAWAY SCRIPT — NOT PART OF THE PACKAGE, NOT PART OF THE REGISTRATION.
# To be DELETED, not committed. v10-spike precedent (PREREG.md line 83:
# claims "settled in a morning of measurement"). Kept out of the evidence tree.
#
# P5 probe: L2a's own probe RUN AS A MEASUREMENT of a fixture property,
# not as a detector (no detector code, no tuning, no development-corpus
# contact). Question: does ANY fixture feature's value change when a label
# cell unavailable at its own decision cohort is corrupted?
#
# Method: corrupt the LABEL-FORMING future values (mid_price at all
# timestamps >= T_cut) in a scratchpad COPY of the zc 2025-01 snapshot
# parquet, rebuild the fixture feature frame with the unmodified Artifact A
# builder (fixture_spike\f2\fixture.py + phase5_ml_fixture.py), and compare
# FEATURE columns (not label columns) at all rows whose decision time
# precedes T_cut. Both sides: contaminated and corrected.
# The builder is proven deterministic (F2), re-witnessed below, so any
# feature difference at a pre-cut row is a real unavailable-label dependency.
#
# Archive is read-only source only. All writes land under p5probe\.
# ============================================================================
import sys, json, shutil, time, traceback
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

SESS = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad")
P5PROBE = SESS / "p5probe"
F2 = SESS / "fixture_spike" / "f2"
ARCHIVE = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc")

sys.path.insert(0, str(F2))
import fixture as fx                 # noqa: E402
import phase5_ml_fixture as p5       # noqa: E402

SYM, MONTH = "zc", "2025-01"
PERT_FACTOR = 1.01
# Cut A: intra-session (zc in-hours 14:00-19:00 UTC) — plain strictly-future cohort.
CUT_A = pd.Timestamp("2025-01-16 16:30:00")
# Cut B: session boundary between the Jan 15 and Jan 16 sessions — the
# cross-boundary label cohort (T3 / declaration §11 cohort class).
CUT_B = pd.Timestamp("2025-01-16 00:00:00")

FEATURES = list(p5.FULL_FEATURES)                       # 44 registered fixture features
LABELS = [f"fwd_move_ticks_{h}s" for h in p5.HORIZONS]  # label columns, EXCLUDED from the feature claim

log_lines = []
def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    log_lines.append(line)


def gen_agg_master():
    """Generate the mbo aggregate cache ONCE from the archive raw mbo parquet,
    through the builder's own load_mbo_aggregated (small-file branch), so both
    baseline and perturbed builds consume the identical cached aggregate via
    the identical code path."""
    out = P5PROBE / "zc_mbo_agg_2025-01.parquet"
    if out.exists():
        log(f"agg master already present: {out.name}")
        return
    log("generating mbo agg master from archive (read-only) ...")
    r = p5.load_mbo_aggregated(SYM, MONTH)   # LOCAL_DATA absent -> falls to archive PROC
    assert r is not None and len(r) > 0, "mbo aggregation returned nothing"
    pq.write_table(pa.Table.from_pandas(r, preserve_index=False), str(out))
    log(f"agg master written: {len(r):,} rows")


def stage_variant(name, cut):
    """Stage a data root: trades byte-copied, agg cache copied, snapshot
    round-tripped through the SAME read/modify/write cycle for every variant
    (identity modification for the baseline) so variants differ ONLY in the
    multiplied mid_price cells."""
    root = P5PROBE / f"data_{name}"
    (root / "zc").mkdir(parents=True, exist_ok=True)
    (root / "zc_mbo_agg").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ARCHIVE / "zc_trades_tagged_2025-01.parquet", root / "zc" / "zc_trades_tagged_2025-01.parquet")
    shutil.copy2(P5PROBE / "zc_mbo_agg_2025-01.parquet", root / "zc_mbo_agg" / "zc_mbo_agg_2025-01.parquet")

    t = pq.read_table(str(ARCHIVE / "zc_snapshots_2025-01.parquet"))
    schema = t.schema
    df = t.to_pandas()
    ts = pd.to_datetime(df["timestamp"])
    if getattr(ts.dt, "tz", None) is not None:
        ts = ts.dt.tz_localize(None)
    if cut is None:
        mask = np.zeros(len(df), dtype=bool)
    else:
        mask = (ts >= cut).values
    n_pert = int(mask.sum())
    df.loc[mask, "mid_price"] = df.loc[mask, "mid_price"] * PERT_FACTOR
    t2 = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
    pq.write_table(t2, str(root / "zc" / "zc_snapshots_2025-01.parquet"))
    log(f"staged {name}: {n_pert:,} perturbed mid_price cells (of {len(df):,} parquet rows)")
    return root, n_pert


def build(root):
    """Build both fixture sides from a staged root, via the unmodified
    Artifact A callables. apply_universal_lag mutates in place -> copy."""
    p5.LOCAL_DATA = root   # get_data_dir: LOCAL_DATA/zc exists -> all reads from staged root
    t0 = time.time()
    cont = fx.fixture_contaminated(SYM, MONTH)
    assert cont is not None, "builder returned None"
    corr, _ = fx.apply_universal_lag(cont.copy())
    log(f"built from {root.name}: {len(cont):,} frame rows in {time.time()-t0:.1f}s")
    return cont, corr


def diff_counts(a, b, cols, lo, hi):
    """NaN-aware per-column diff over positions [lo, hi)."""
    out = {}
    for c in cols:
        x, y = a[c].iloc[lo:hi], b[c].iloc[lo:hi]
        neq = (x != y) & ~(x.isna() & y.isna())
        n = int(neq.sum())
        e = {"n_diff": n}
        if n:
            idx = neq[neq].index
            e["first_pos"] = int(idx[0])
            e["last_pos"] = int(idx[-1])
            try:
                e["max_abs_diff"] = float((x[neq] - y[neq]).abs().max())
            except Exception:
                e["max_abs_diff"] = "non-numeric"
        out[c] = e
    return out


def total_diffs(d):
    return sum(v["n_diff"] for v in d.values())


def compare_variant(name, cut, base_cont, base_corr, cont, corr):
    assert len(base_cont) == len(cont), "row count changed under perturbation"
    assert (base_cont["timestamp"].values == cont["timestamp"].values).all(), "timestamps changed"
    ts = base_cont["timestamp"]
    pos_cut = int((ts >= cut).values.argmax())
    assert bool(ts.iloc[pos_cut] >= cut) and bool(ts.iloc[pos_cut - 1] < cut)
    n = len(ts)
    other_cols = [c for c in base_cont.columns
                  if c not in FEATURES and c not in LABELS and c != "timestamp"]
    r = {"cut": str(cut), "pos_cut": pos_cut, "n_rows": n, "n_precut": pos_cut}
    # PRIMARY QUESTION — features at rows whose decision time precedes T_cut:
    r["cont_features_precut"] = diff_counts(base_cont, cont, FEATURES, 0, pos_cut)
    r["corr_features_precut"] = diff_counts(base_corr, corr, FEATURES, 0, pos_cut)
    # POSITIVE CONTROL 1 — label cells at pre-cut decision rows MUST have moved
    # (expected: exactly h per horizon, at positions pos_cut-h .. pos_cut-1):
    r["cont_labels_precut"] = diff_counts(base_cont, cont, LABELS, 0, pos_cut)
    r["corr_labels_precut"] = diff_counts(base_corr, corr, LABELS, 0, pos_cut)
    # POSITIVE CONTROL 2 — post-cut features MUST have moved (perturbation
    # reached the feature pipeline at all):
    r["cont_features_postcut_sample"] = diff_counts(
        base_cont, cont, ["mid_return_1s", "volatility_30s", "range_60s", "vwap_distance"], pos_cut, n)
    # SECONDARY — every non-feature non-label column pre-cut (expect zero):
    r["cont_other_precut"] = diff_counts(base_cont, cont, other_cols, 0, pos_cut)
    # INFORMATIVE — corrected side AT the cut row (its features come from
    # pos_cut-1, so they should be clean even at the boundary row):
    r["corr_features_at_poscut"] = diff_counts(base_corr, corr, FEATURES, pos_cut, pos_cut + 1)
    log(f"variant {name}: pos_cut={pos_cut:,}/{n:,} | "
        f"PRE-CUT feature diffs cont={total_diffs(r['cont_features_precut'])} "
        f"corr={total_diffs(r['corr_features_precut'])} | "
        f"pre-cut label diffs cont={total_diffs(r['cont_labels_precut'])} | "
        f"post-cut sample diffs={total_diffs(r['cont_features_postcut_sample'])} | "
        f"other pre-cut diffs={total_diffs(r['cont_other_precut'])}")
    return r


def main():
    results = {
        "env": {"pandas": pd.__version__, "numpy": np.__version__, "pyarrow": pa.__version__,
                "python": sys.version.split()[0]},
        "slice": f"{SYM} {MONTH}", "pert_factor": PERT_FACTOR,
        "n_features_tested": len(FEATURES), "features": FEATURES, "labels": LABELS,
    }
    t_all = time.time()
    gen_agg_master()

    base_root, n0 = stage_variant("baseline", None)
    rootA, nA = stage_variant("pertA_intrasession", CUT_A)
    rootB, nB = stage_variant("pertB_sessionboundary", CUT_B)
    assert n0 == 0 and nA > 0 and nB > nA
    results["n_perturbed_cells"] = {"baseline": n0, "A_intrasession": nA, "B_sessionboundary": nB}

    # Baseline + determinism re-witness (same root, built twice)
    cont_base, corr_base = build(base_root)
    cont_base2, _ = build(base_root)
    det = diff_counts(cont_base, cont_base2, list(cont_base.columns), 0, len(cont_base))
    n_det = total_diffs(det)
    results["determinism_rewitness_total_diffs"] = n_det
    log(f"determinism re-witness: {n_det} differing cells across ALL columns (expect 0)")
    assert n_det == 0, "builder non-deterministic in this environment; probe invalid"
    del cont_base2

    contA, corrA = build(rootA)
    results["variant_A_intrasession"] = compare_variant("A", CUT_A, cont_base, corr_base, contA, corrA)
    del contA, corrA

    contB, corrB = build(rootB)
    results["variant_B_sessionboundary"] = compare_variant("B", CUT_B, cont_base, corr_base, contB, corrB)
    del contB, corrB

    results["elapsed_s"] = round(time.time() - t_all, 1)
    with open(P5PROBE / "p5_probe_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    with open(P5PROBE / "p5_probe_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    log("DONE — results at p5probe\\p5_probe_results.json")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        with open(P5PROBE / "p5_probe_log.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n\nFAILED:\n" + traceback.format_exc())
        sys.exit(1)
