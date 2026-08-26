"""C3 diagnosis for the timestamped pc2 variant set.

For each pre/post pair:
- Load timestamp (int64 ns), true_label, fwd_move_ticks, mid_price_t.
- Align rows by sorted-multiset merge on timestamp: vectorized common prefix,
  vectorized common suffix, two-pointer merge over the (tiny) middle.
- only_pre / only_post: rows whose timestamp has no partner on the other side.
- For matched row pairs: bitwise comparison (uint64 view) of each column.
- Boundary classification (rule from the gate spec): a row is SESSION BOUNDARY
  if its row index is within h rows (h = horizon seconds; lattice is ~1 s) of a
  segment edge, where segment edges are: file start, file end, any position
  with a timestamp gap > 60 s, or a calendar (UTC-date-of-timestamp) change
  between consecutive rows. Otherwise INTERIOR.
Outputs pc2_diff_summary.csv and per-row detail pc2_diff_rows.csv.
"""
import os
import numpy as np
import pyarrow.parquet as pq

TS_DIR = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\phase7\l2_predictions"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
COLS = ["true_label", "fwd_move_ticks", "mid_price_t"]
DAY_NS = 86_400_000_000_000
GAP_NS = 60_000_000_000


def load(path):
    t = pq.read_table(path, columns=["timestamp"] + COLS)
    out = {"timestamp": t.column("timestamp").combine_chunks().to_numpy(zero_copy_only=False).astype("int64")}
    for c in COLS:
        out[c] = t.column(c).combine_chunks().to_numpy(zero_copy_only=False)
    return out


def align(a: np.ndarray, b: np.ndarray):
    """Sorted-multiset alignment. Returns (ia, ib, only_a, only_b)."""
    na, nb = len(a), len(b)
    m = min(na, nb)
    neq = np.nonzero(a[:m] != b[:m])[0]
    pref = int(neq[0]) if len(neq) else m
    ra, rb = a[pref:], b[pref:]
    mm = min(len(ra), len(rb))
    if mm:
        neq2 = np.nonzero(ra[len(ra) - mm:] != rb[len(rb) - mm:])[0]
        suf = mm - (int(neq2[-1]) + 1) if len(neq2) else mm
    else:
        suf = 0
    # middle segments
    a_mid = a[pref:na - suf]
    b_mid = b[pref:nb - suf]
    ia = [np.arange(pref, dtype=np.int64)]
    ib = [np.arange(pref, dtype=np.int64)]
    only_a, only_b = [], []
    i = j = 0
    mia, mib = [], []
    while i < len(a_mid) and j < len(b_mid):
        if a_mid[i] == b_mid[j]:
            mia.append(pref + i); mib.append(pref + j)
            i += 1; j += 1
        elif a_mid[i] < b_mid[j]:
            only_a.append(pref + i); i += 1
        else:
            only_b.append(pref + j); j += 1
    while i < len(a_mid):
        only_a.append(pref + i); i += 1
    while j < len(b_mid):
        only_b.append(pref + j); j += 1
    ia.append(np.array(mia, dtype=np.int64))
    ib.append(np.array(mib, dtype=np.int64))
    ia.append(np.arange(na - suf, na, dtype=np.int64))
    ib.append(np.arange(nb - suf, nb, dtype=np.int64))
    return (np.concatenate(ia), np.concatenate(ib),
            np.array(only_a, dtype=np.int64), np.array(only_b, dtype=np.int64))


def segment_edges(ts: np.ndarray):
    """Positions p (1..n-1) where a new segment starts, plus 0 and n."""
    gap = np.diff(ts) > GAP_NS
    daychange = (ts[1:] // DAY_NS) != (ts[:-1] // DAY_NS)
    starts = np.nonzero(gap | daychange)[0] + 1
    return np.concatenate(([0], starts, [len(ts)]))


def boundary_mask(row_idx: np.ndarray, edges: np.ndarray, h: int):
    """True where row is within h rows of its segment's start or end."""
    if len(row_idx) == 0:
        return np.zeros(0, dtype=bool)
    seg = np.searchsorted(edges, row_idx, side="right") - 1
    seg_start = edges[seg]
    seg_end = edges[seg + 1]  # exclusive
    d = np.minimum(row_idx - seg_start, seg_end - 1 - row_idx)
    return d < h


def bits(x: np.ndarray):
    return x.view(np.uint64)


def main():
    summary_rows = []
    detail_rows = []
    per_model_fingerprint = {}
    for inst in ["gc", "nq", "zc", "zs"]:
        for model in ["LightGBM", "XGBoost"]:
            for h in [5, 10, 30, 60]:
                pre = load(os.path.join(TS_DIR, f"{inst}_{model}_{h}_predictions.parquet"))
                post = load(os.path.join(TS_DIR, f"{inst}_{model}_{h}_predictions_fixed.parquet"))
                ia, ib, only_pre, only_post = align(pre["timestamp"], post["timestamp"])
                assert np.array_equal(pre["timestamp"][ia], post["timestamp"][ib])
                n_match = len(ia)
                res = {}
                mismatch_idx = None
                for c in COLS:
                    d = np.nonzero(bits(pre[c][ia]) != bits(post[c][ib]))[0]
                    res[c] = len(d)
                    if c == "true_label":
                        mismatch_idx = ia[d]  # pre-file row indices of label diffs
                        mismatch_ts = pre["timestamp"][ia[d]]
                        pre_lab = pre[c][ia[d]]
                        post_lab = post[c][ib[d]]
                edges_pre = segment_edges(pre["timestamp"])
                edges_post = segment_edges(post["timestamp"])
                bm_lab = boundary_mask(mismatch_idx, edges_pre, h)
                bm_op = boundary_mask(only_pre, edges_pre, h)
                bm_opo = boundary_mask(only_post, edges_post, h)
                summary_rows.append([
                    inst, model, h, len(pre["timestamp"]), len(post["timestamp"]),
                    n_match, len(only_pre), int(bm_op.sum()), len(only_pre) - int(bm_op.sum()),
                    len(only_post), int(bm_opo.sum()), len(only_post) - int(bm_opo.sum()),
                    res["true_label"], int(bm_lab.sum()), res["true_label"] - int(bm_lab.sum()),
                    res["fwd_move_ticks"], res["mid_price_t"],
                ])
                fp = (len(only_pre), len(only_post), res["true_label"],
                      res["fwd_move_ticks"], res["mid_price_t"],
                      tuple(only_pre.tolist()), tuple(only_post.tolist()),
                      tuple(mismatch_idx.tolist()))
                per_model_fingerprint.setdefault((inst, h), {})[model] = fp
                for k in range(len(mismatch_idx)):
                    detail_rows.append([
                        inst, model, h, "label_diff", int(mismatch_idx[k]),
                        str(np.datetime64(int(mismatch_ts[k]), "ns")),
                        int(pre_lab[k]), int(post_lab[k]),
                        "boundary" if bm_lab[k] else "interior"])
                for k in range(len(only_pre)):
                    detail_rows.append([
                        inst, model, h, "only_pre", int(only_pre[k]),
                        str(np.datetime64(int(pre["timestamp"][only_pre[k]]), "ns")),
                        int(pre["true_label"][only_pre[k]]), "",
                        "boundary" if bm_op[k] else "interior"])
                for k in range(len(only_post)):
                    detail_rows.append([
                        inst, model, h, "only_post", int(only_post[k]),
                        str(np.datetime64(int(post["timestamp"][only_post[k]]), "ns")),
                        "", int(post["true_label"][only_post[k]]),
                        "boundary" if bm_opo[k] else "interior"])

    hdr = ["instrument", "model", "horizon", "n_pre", "n_post", "n_matched",
           "only_pre", "only_pre_boundary", "only_pre_interior",
           "only_post", "only_post_boundary", "only_post_interior",
           "label_diff_matched", "label_diff_boundary", "label_diff_interior",
           "fwd_diff_matched", "mid_diff_matched"]
    with open(os.path.join(OUT_DIR, "pc2_diff_summary.csv"), "w", newline="") as f:
        f.write(",".join(hdr) + "\n")
        for r in summary_rows:
            f.write(",".join(str(x) for x in r) + "\n")
    with open(os.path.join(OUT_DIR, "pc2_diff_rows.csv"), "w", newline="") as f:
        f.write("instrument,model,horizon,kind,row_index,timestamp,pre_label,post_label,class\n")
        for r in detail_rows:
            f.write(",".join(str(x) for x in r) + "\n")

    print("\t".join(hdr))
    for r in summary_rows:
        print("\t".join(str(x) for x in r))
    print()
    print("model-consistency (LightGBM vs XGBoost identical diff fingerprints):")
    for k, v in sorted(per_model_fingerprint.items()):
        same = v.get("LightGBM") == v.get("XGBoost")
        print(f"  {k}: {'IDENTICAL' if same else 'DIFFER'}")
    print()
    print("detail rows written:", len(detail_rows))


if __name__ == "__main__":
    main()
