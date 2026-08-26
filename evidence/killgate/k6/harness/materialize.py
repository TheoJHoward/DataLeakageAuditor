"""Materialize C1..C8 x {contaminated, clean} to CSV + manifest, and hash them.

Run ONCE, before any tool is executed. The hashes fix the case set for item 7
("No case excluded after results are seen").
"""
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "cases"))

import case_defs as cd  # noqa: E402


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def main():
    manifest = {}
    for case in cd.CASES:
        for side in cd.SIDES:
            d = cd.get(case, side)
            tag = f"{case}_{side}"
            sub = os.path.join(OUT, tag)
            os.makedirs(sub, exist_ok=True)
            full = d["full"]
            full.to_csv(os.path.join(sub, "full.csv"), index=False)
            d["raw"].to_csv(os.path.join(sub, "raw.csv"), index=False)
            tr, te = np.asarray(d["train_idx"]), np.asarray(d["test_idx"])
            full.iloc[tr].to_csv(os.path.join(sub, "train.csv"), index=False)
            full.iloc[te].to_csv(os.path.join(sub, "test.csv"), index=False)
            np.savetxt(os.path.join(sub, "train_idx.txt"), tr, fmt="%d")
            np.savetxt(os.path.join(sub, "test_idx.txt"), te, fmt="%d")
            meta = dict(d["meta"])
            meta.update(case=case, side=side, type=cd.CASE_TYPE[case],
                        detector_row=cd.CASE_ROW[case],
                        n_rows=int(len(full)), n_train=int(len(tr)), n_test=int(len(te)),
                        n_index_overlap=int(len(np.intersect1d(tr, te))))
            with open(os.path.join(sub, "meta.json"), "w") as f:
                json.dump(meta, f, indent=2)
            manifest[tag] = {fn: sha256(os.path.join(sub, fn))
                             for fn in sorted(os.listdir(sub))}
            manifest[tag]["_meta"] = meta
    with open(os.path.join(OUT, "MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps({k: v["full.csv"] for k, v in manifest.items()}, indent=2))
    print("\nrows/train/test/overlap per case-side:")
    for k, v in manifest.items():
        m = v["_meta"]
        print(f"  {k:24s} n={m['n_rows']:4d} tr={m['n_train']:4d} te={m['n_test']:4d} "
              f"idx_overlap={m['n_index_overlap']:3d}")


if __name__ == "__main__":
    main()
