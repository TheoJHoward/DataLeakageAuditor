"""F2 runner: build one (variant, sym, month) in a fresh process, canonically
serialize, hash, and persist for later comparison.

Usage: python run_fixture.py {contaminated|corrected} SYM MONTH RUN_ID
Writes under f2/out/: {variant}_{sym}_{month}_run{id}.pkl, .sha256, .meta.json
"""
import hashlib
import json
import sys
import time
import warnings
from pathlib import Path

_F2 = Path(__file__).resolve().parent
if str(_F2) not in sys.path:
    sys.path.insert(0, str(_F2))

# phase5_ml.py sets warnings.filterwarnings("ignore") at import time.
# Import first, then RESET filters in this runner so pandas-3.x behavioral
# warnings actually surface during the build (item e).
import fixture  # noqa: E402  (imports phase5_ml_fixture -> torch, lgb, xgb, pandas)
warnings.resetwarnings()

import numpy as np   # noqa: E402
import pandas as pd  # noqa: E402


def canonical_csv_sha256(df):
    """Canonical serialization: to_csv with fixed float_format, sha256 of bytes."""
    s = df.to_csv(index=False, float_format="%.12g")
    return hashlib.sha256(s.encode("utf-8")).hexdigest(), len(s)


def main():
    variant, sym, month, run_id = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    fn = {"contaminated": fixture.fixture_contaminated,
          "corrected": fixture.fixture_corrected}[variant]

    caught = []
    t0 = time.time()
    with warnings.catch_warnings(record=True) as wrec:
        warnings.simplefilter("always")
        df = fn(sym, month)
        for w in wrec:
            caught.append(f"{w.category.__name__}: {str(w.message)} [{w.filename}:{w.lineno}]")
    elapsed = time.time() - t0

    if df is None:
        print("BUILDER RETURNED None"); sys.exit(2)

    sha, nbytes = canonical_csv_sha256(df)

    out = _F2 / "out"
    out.mkdir(exist_ok=True)
    stem = f"{variant}_{sym}_{month}_run{run_id}"
    df.to_pickle(out / f"{stem}.pkl")
    (out / f"{stem}.sha256").write_text(sha + "\n")
    meta = {
        "variant": variant, "sym": sym, "month": month, "run_id": run_id,
        "rows": int(len(df)), "cols": int(df.shape[1]),
        "columns": list(df.columns),
        "canonical_csv_sha256": sha, "canonical_csv_bytes": nbytes,
        "build_seconds": round(elapsed, 2),
        "pandas": pd.__version__, "numpy": np.__version__,
        "warnings_during_build": sorted(set(caught)),
        "n_warnings_raw": len(caught),
    }
    (out / f"{stem}.meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps({k: meta[k] for k in
                      ["variant", "sym", "month", "run_id", "rows", "cols",
                       "canonical_csv_sha256", "build_seconds", "n_warnings_raw"]}, indent=2))
    for wmsg in meta["warnings_during_build"]:
        print("WARN:", wmsg)


if __name__ == "__main__":
    main()
