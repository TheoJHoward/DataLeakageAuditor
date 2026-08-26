"""C3 gate: bit-exact label-vector equality across Phase 7 pre/post pairs.

Comparison method:
- Load columns via pyarrow.parquet.read_table (no pandas conversion for the
  compared arrays; combine_chunks -> numpy via .to_numpy()).
- For every compared column: first confirm same dtype and same length.
- Integer column (true_label): np.array_equal AND raw-bytes equality
  (a.tobytes() == b.tobytes()) -- both reported; bytes is the recorded method.
- Float columns (fwd_move_ticks, mid_price_t): raw-bytes equality
  a.tobytes() == b.tobytes() after dtype/length confirmation. This is
  bit-exact: distinguishes 0.0 from -0.0 and matches NaN payloads bitwise.
- first_diff_index: smallest row index where the 8-byte words differ,
  computed per column via np.frombuffer on the raw bytes viewed as uint64
  (bitwise, not value-wise).
"""
import os
import sys
import numpy as np
import pyarrow.parquet as pq

MAIN_PRE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase7\l2_predictions"
MAIN_POST = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase7_fixed\l2_predictions"
TS_DIR = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\phase7\l2_predictions"
OUT_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "label_equality.csv")

INSTRUMENTS_MAIN = ["cl", "es", "gc", "he", "le", "nq", "zc", "zs"]
INSTRUMENTS_TS = ["gc", "nq", "zc", "zs"]
MODELS = ["LightGBM", "XGBoost"]
HORIZONS = ["5", "10", "30", "60"]
COLS = ["true_label", "fwd_move_ticks", "mid_price_t"]


def load_cols(path):
    t = pq.read_table(path, columns=COLS)
    out = {}
    for c in COLS:
        arr = t.column(c).combine_chunks()
        np_arr = arr.to_numpy(zero_copy_only=False)
        out[c] = np_arr
    return out


def bitwise_first_diff(a: np.ndarray, b: np.ndarray):
    """Return (equal_bytes, first_diff_index or ''). Bitwise via uint64 view."""
    ab = a.tobytes()
    bb = b.tobytes()
    if ab == bb:
        return True, ""
    ua = np.frombuffer(ab, dtype=np.uint64)
    ub = np.frombuffer(bb, dtype=np.uint64)
    idx = int(np.nonzero(ua != ub)[0][0])
    return False, idx


def compare_pair(set_name, instrument, model, horizon, pre_path, post_path, rows, problems):
    if not (os.path.exists(pre_path) and os.path.exists(post_path)):
        problems.append(f"MISSING FILE: {pre_path if not os.path.exists(pre_path) else post_path}")
        rows.append([set_name, instrument, model, horizon, "", "MISSING", "MISSING", "MISSING", ""])
        return
    pre = load_cols(pre_path)
    post = load_cols(post_path)

    n_pre = len(pre["true_label"])
    n_post = len(post["true_label"])
    if n_pre != n_post:
        problems.append(
            f"ROWCOUNT MISMATCH {set_name} {instrument} {model} {horizon}s: pre={n_pre} post={n_post}"
        )
        rows.append([set_name, instrument, model, horizon, f"{n_pre}/{n_post}",
                     "N_MISMATCH", "N_MISMATCH", "N_MISMATCH", ""])
        return

    results = {}
    diffs = {}
    for c in COLS:
        a, b = pre[c], post[c]
        if a.dtype != b.dtype:
            problems.append(
                f"DTYPE MISMATCH {set_name} {instrument} {model} {horizon}s col={c}: {a.dtype} vs {b.dtype}"
            )
            results[c] = "DTYPE_MISMATCH"
            diffs[c] = ""
            continue
        if a.dtype.itemsize != 8:
            problems.append(
                f"UNEXPECTED ITEMSIZE {set_name} {instrument} {model} {horizon}s col={c}: dtype={a.dtype}"
            )
        eq, fd = bitwise_first_diff(a, b)
        # cross-check for the integer gate column with value equality
        if c == "true_label":
            veq = bool(np.array_equal(a, b))
            if veq != eq:
                problems.append(
                    f"BYTE/VALUE DISAGREEMENT {set_name} {instrument} {model} {horizon}s true_label: bytes={eq} values={veq}"
                )
        results[c] = eq
        diffs[c] = fd

    first_diff = ""
    for c in COLS:
        if diffs[c] != "":
            first_diff = diffs[c] if first_diff == "" else min(first_diff, diffs[c])
    rows.append([set_name, instrument, model, horizon, n_pre,
                 results["true_label"], results["fwd_move_ticks"], results["mid_price_t"], first_diff])
    # record dtypes once per pair for reporting
    return {c: str(pre[c].dtype) for c in COLS}


def main():
    rows = []
    problems = []
    dtype_seen = {}

    for inst in INSTRUMENTS_MAIN:
        for model in MODELS:
            for h in HORIZONS:
                fn = f"{inst}_{model}_{h}s_predictions.parquet"
                d = compare_pair("main", inst, model, h,
                                 os.path.join(MAIN_PRE, fn),
                                 os.path.join(MAIN_POST, fn),
                                 rows, problems)
                if d:
                    dtype_seen[("main", inst, model, h)] = d

    for inst in INSTRUMENTS_TS:
        for model in MODELS:
            for h in HORIZONS:
                pre_fn = f"{inst}_{model}_{h}_predictions.parquet"
                post_fn = f"{inst}_{model}_{h}_predictions_fixed.parquet"
                d = compare_pair("pc2_ts", inst, model, h,
                                 os.path.join(TS_DIR, pre_fn),
                                 os.path.join(TS_DIR, post_fn),
                                 rows, problems)
                if d:
                    dtype_seen[("pc2_ts", inst, model, h)] = d

    header = ["set", "instrument", "model", "horizon", "n_rows",
              "label_equal", "fwd_bitexact", "mid_bitexact", "first_diff_index"]
    with open(OUT_CSV, "w", newline="") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")

    print("CSV written:", OUT_CSV)
    print()
    print("\t".join(header))
    for r in rows:
        print("\t".join(str(x) for x in r))
    print()
    uniq_dtypes = set()
    for d in dtype_seen.values():
        uniq_dtypes.add(tuple(sorted(d.items())))
    print("distinct dtype signatures across pairs:", uniq_dtypes)
    print()
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" -", p)
    else:
        print("PROBLEMS: none")

    n_label_bad = sum(1 for r in rows if r[5] is not True)
    n_fwd_bad = sum(1 for r in rows if r[6] is not True)
    n_mid_bad = sum(1 for r in rows if r[7] is not True)
    print(f"SUMMARY: pairs={len(rows)} label_mismatch_pairs={n_label_bad} "
          f"fwd_mismatch_pairs={n_fwd_bad} mid_mismatch_pairs={n_mid_bad}")


if __name__ == "__main__":
    sys.exit(main())
