# P6 T3 REPRODUCIBILITY — COMPLETE day-edge producer.
#
# The archived producer (evidence\fixture_spike\t3\measure_day_edge.py) builds ELEVEN
# keys per horizon; the archived table (t3\day_edge_table.csv) carries FOURTEEN columns.
# This script reproduces ALL FOURTEEN: the archived script's eleven (logic replicated
# verbatim below, marked ARCHIVED LOGIC) plus the three magnitude-filter columns the
# archived script never builds:
#   cross_boundary_passing_mag_filter_abs_ge_2ticks
#   cross_boundary_mag_filter_pass_frac
#   overall_mag_filter_pass_frac
# Magnitude filter definition: |fwd_move_ticks_{h}s| >= 2.0, per pre-fix phase5_ml.py
# line 679 (`valid = valid[valid[ret_col].abs() >= 2.0].copy()`), as cited in
# AVAILABILITY_DECLARATION.md lines 466-469 and ERRATA_REGISTER.md Entry 5.
#
# MEASUREMENT ONLY — no detector code, no fixes. Writes ONLY under p6repro\.
#
# Input path convention: the archived script reads HERE.parent/f2/out/<pkl> (t3 is a
# sibling of f2 under evidence\fixture_spike). This script sits at scratchpad\p6repro\,
# a sibling of scratchpad\fixture_spike\, so the analogue is
# HERE.parent/fixture_spike/f2/out/<pkl> — the SAME f2 build output tree; the archive's
# f2\out\ carries only the .sha256/.meta.json attestations, not the pickle bytes.
# The input is therefore attested below by recomputing the f2 canonical-CSV sha256
# (run_fixture.py lines 28-31: to_csv(index=False, float_format="%.12g"), sha256 of
# utf-8 bytes) and requiring it to equal the archived sidecar value.
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
F2_OUT = HERE.parent / "fixture_spike" / "f2" / "out"
PKL = F2_OUT / "contaminated_zc_2025-01_run1.pkl"

# Archived attestation: evidence\fixture_spike\f2\out\contaminated_zc_2025-01_run1.sha256
EXPECTED_CANONICAL_SHA256 = (
    "73143359a90022f30af60cde7e637fd0b1585716f09d09437696fae411a10465"
)
EXPECTED_CANONICAL_BYTES = 163349778  # meta.json canonical_csv_bytes

MAG_TICKS = 2.0  # the >=2-tick magnitude filter (phase5_ml.py:679)

snap = pd.read_pickle(PKL)
print(f"loaded {PKL}")
print(f"rows={len(snap)} cols={snap.shape[1]}")

# ---- input attestation: canonical CSV sha256 must match the archived sidecar ----
canon = snap.to_csv(index=False, float_format="%.12g")
canon_sha = hashlib.sha256(canon.encode("utf-8")).hexdigest()
canon_bytes = len(canon)
print(f"canonical_csv_sha256 recomputed: {canon_sha} ({canon_bytes} bytes)")
if canon_sha != EXPECTED_CANONICAL_SHA256 or canon_bytes != EXPECTED_CANONICAL_BYTES:
    print("INPUT ATTESTATION FAILED: pickle does not match archived canonical sha256")
    sys.exit(2)
print("input attestation OK: matches archived contaminated_zc_2025-01_run1.sha256")

# ---- ARCHIVED LOGIC (measure_day_edge.py lines 16-27), replicated verbatim ----
ts = pd.to_datetime(snap["timestamp"]).reset_index(drop=True)
snap = snap.reset_index(drop=True)

dates = ts.dt.normalize()
day_change = (dates != dates.shift(1))
n_sessions = dates.nunique()
n_day_boundaries = int(day_change.sum()) - 1  # first row is not a boundary
print(f"unique calendar dates (sessions): {n_sessions}")
print(f"consecutive-row day-change boundaries: {n_day_boundaries}")

N = len(snap)
horizons = [5, 10, 30, 60]
rows_out = []
overall_diag = []  # denominator diagnostics for overall_mag_filter_pass_frac

for h in horizons:
    lab = snap[f"fwd_move_ticks_{h}s"]
    nan_total = int(lab.isna().sum())
    tail_nan = int(lab.iloc[-h:].isna().sum())  # month-boundary check: expect == h
    # positional counterpart: row i pairs with row i+h            (ARCHIVED LOGIC)
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
    # same-day pairs spanning an intra-day >60s re-anchor gap     (ARCHIVED LOGIC)
    sameday = ~cross
    is_ = i[sameday]; js_ = j[sameday]
    spans_sd = (ts.values[js_] - ts.values[is_])
    n_sameday_gt60 = int(np.sum(spans_sd > np.timedelta64(60, 's')))
    worst_sd = pd.Timedelta(spans_sd.max()) if len(spans_sd) else pd.NaT

    # ---- NEW: the three magnitude-filter columns (the gap) ----
    # (1) count of cross-boundary label rows passing |label| >= 2 ticks.
    #     NaN labels compare False, so they never count as passing.
    n_cross_pass = int(np.sum(np.abs(lab_cross) >= MAG_TICKS))
    # (2) cross-boundary pass fraction, over ALL cross-boundary pairs, rounded to
    #     3 decimals — the archived CSV stores 3-decimal values (0.83/0.83/0.823/0.812),
    #     so 3-dp rounding is the serialization convention being reproduced.
    cross_frac = round(n_cross_pass / n_cross, 3) if n_cross else float("nan")
    # (3) overall baseline pass fraction. Three denominator candidates exist a priori
    #     (all N lattice rows; the N-nan_total real-labelled rows; the N-h positional
    #     pairs). All are computed and printed; the emitted column uses ALL N ROWS.
    #     The diagnostics below demonstrate all three round identically at 3 dp.
    n_overall_pass = int(np.sum(np.abs(lab.values) >= MAG_TICKS))  # NaN-safe: False
    f_all_rows = n_overall_pass / N
    f_real_lab = n_overall_pass / (N - nan_total)
    f_pairs = int(np.sum(np.abs(lab.values[i]) >= MAG_TICKS)) / (N - h)
    overall_frac = round(f_all_rows, 3)
    overall_diag.append({
        "horizon_s": h,
        "overall_pass_count": n_overall_pass,
        "frac_all_rows_raw": f_all_rows,
        "frac_real_labels_raw": f_real_lab,
        "frac_pairs_raw": f_pairs,
        "round3_all_rows": round(f_all_rows, 3),
        "round3_real_labels": round(f_real_lab, 3),
        "round3_pairs": round(f_pairs, 3),
    })

    rows_out.append({
        # ---- the archived producer's eleven keys, identical logic ----
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
        # ---- the three columns the archived producer does NOT build ----
        "cross_boundary_passing_mag_filter_abs_ge_2ticks": n_cross_pass,
        "cross_boundary_mag_filter_pass_frac": cross_frac,
        "overall_mag_filter_pass_frac": overall_frac,
    })

tbl = pd.DataFrame(rows_out)
OUT_CSV = HERE / "day_edge_table_full.csv"
tbl.to_csv(OUT_CSV, index=False)
print(f"\nwrote {OUT_CSV}")
print("\n=== per-horizon table (all fourteen columns) ===")
print(tbl.to_string(index=False))

print("\n=== overall-denominator diagnostics (raw and 3-dp) ===")
diag = pd.DataFrame(overall_diag)
print(diag.to_string(index=False))
diag.to_csv(HERE / "overall_denominator_diagnostics.csv", index=False)

# ---- COLUMN-BY-COLUMN comparison against the archived day_edge_table.csv ----
ARCHIVED = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01"
                r"\evidence\fixture_spike\t3\day_edge_table.csv")
ref = pd.read_csv(ARCHIVED)
new = pd.read_csv(OUT_CSV)  # re-read so both sides pass through identical CSV parsing

print(f"\n=== comparison vs {ARCHIVED} ===")
ok = True
if list(ref.columns) != list(new.columns):
    print("COLUMN SET/ORDER MISMATCH")
    print(" archived:", list(ref.columns))
    print(" produced:", list(new.columns))
    ok = False
else:
    print(f"column set and order: IDENTICAL ({len(ref.columns)} columns)")

FRAC_COLS = {"cross_boundary_mag_filter_pass_frac", "overall_mag_filter_pass_frac"}
rows = []
for col in ref.columns:
    a = ref[col]
    b = new[col]
    if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):
        dev = (b - a).abs().max()
        if col in FRAC_COLS:
            # archived CSV stores 3 decimals; tolerance 5e-4 = half-ulp at 3 dp.
            # Exact equality still expected because the same 3-dp rounding is applied.
            match = bool(dev <= 5e-4)
            kind = "fraction (3-dp)"
        else:
            match = bool(dev == 0)
            kind = "count"
        rows.append((col, kind, f"{dev:.17g}", "MATCH" if match else "MISMATCH"))
        ok &= match
    else:
        eq = bool((a.astype(str) == b.astype(str)).all())
        rows.append((col, "string", "0" if eq else "differs", "MATCH" if eq else "MISMATCH"))
        ok &= eq

w = max(len(r[0]) for r in rows)
print(f"{'column'.ljust(w)}  {'type':<14} {'max_abs_deviation':<20} verdict")
for col, kind, dev, verdict in rows:
    print(f"{col.ljust(w)}  {kind:<14} {dev:<20} {verdict}")

# raw-token comparison: the strongest form — the serialized cells themselves
ref_lines = ARCHIVED.read_text().strip().splitlines()
new_lines = OUT_CSV.read_text().strip().splitlines()
token_identical = ref_lines == new_lines
print(f"\nraw CSV lines identical (byte-for-byte tokens): {token_identical}")
if not token_identical:
    for k, (ra, rb) in enumerate(zip(ref_lines, new_lines)):
        if ra != rb:
            print(f" line {k+1} archived: {ra}")
            print(f" line {k+1} produced: {rb}")

# ---- (d) the declaration's enrichment figures, re-verified from THIS output ----
print("\n=== declaration enrichment figures (AVAILABILITY_DECLARATION.md:461-462) ===")
print("cross-boundary pass fracs (declared 0.83 / 0.83 / 0.823 / 0.812):",
      " / ".join(f"{v:g}" for v in tbl["cross_boundary_mag_filter_pass_frac"]))
print("overall baseline fracs   (declared 0.000 / 0.001 / 0.004 / 0.010):",
      " / ".join(f"{v:.3f}" for v in tbl["overall_mag_filter_pass_frac"]))
decl_cross = [0.83, 0.83, 0.823, 0.812]
decl_overall = [0.000, 0.001, 0.004, 0.010]
d_ok = (list(tbl["cross_boundary_mag_filter_pass_frac"]) == decl_cross and
        list(tbl["overall_mag_filter_pass_frac"]) == decl_overall)
print(f"declaration figures reproduce: {d_ok}")

print(f"\nVERDICT: {'REPRODUCED' if (ok and token_identical and d_ok) else 'STOP-AND-REPORT: MISMATCH'}")
sys.exit(0 if (ok and token_identical and d_ok) else 1)
