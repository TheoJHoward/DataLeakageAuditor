"""C1(b): re-derive the 338,159 row count from the archive ZC 2025-01 snapshots
parquet by applying the builder's session filter exactly as written in
fixture_spike/f2/phase5_ml_fixture.py build_features_month().

Filter provenance (phase5_ml_fixture.py):
  line  58: "zc": {..., "day_start_utc": 14, "day_end_utc": 19, ...}
  line 179: ds, de = meta["day_start_utc"], meta["day_end_utc"]
  line 184: snap["timestamp"] = pd.to_datetime(snap["timestamp"])
  line 187: snap = snap.sort_values("timestamp").reset_index(drop=True)
  line 188: snap["hour_utc"] = snap["timestamp"].dt.hour
  line 189: snap = snap[(snap["hour_utc"] >= ds) & (snap["hour_utc"] < de)].copy()

Read-only against the archive.
"""
import os
from datetime import datetime, timezone

import pandas as pd
import pyarrow.parquet as pq

ARCHIVE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025"
SNAP = os.path.join(ARCHIVE, "processed", "zc", "zc_snapshots_2025-01.parquet")
FIXTURE = (r"C:\Users\ttbea\AppData\Local\Temp\claude"
           r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
           r"\f2\phase5_ml_fixture.py")

CITED = [58, 179, 184, 187, 188, 189]
DS, DE = 14, 19
EXPECTED = 338159


def main():
    print("C1 (b) 338,159 row-count re-derivation")
    print("run_utc: %s" % datetime.now(timezone.utc).isoformat())
    print("pandas %s / pyarrow %s" % (pd.__version__, pq.__name__ and __import__("pyarrow").__version__))
    print()
    print("input parquet: %s" % SNAP)
    print("  size_bytes: %d" % os.path.getsize(SNAP))
    print()
    print("filter source: %s" % FIXTURE)
    with open(FIXTURE, "r", encoding="utf-8", errors="replace") as fh:
        src = fh.read().splitlines()
    for ln in CITED:
        print("  line %3d: %s" % (ln, src[ln - 1].rstrip()))
    print()
    print("constants read from source: ds=day_start_utc=%d, de=day_end_utc=%d" % (DS, DE))
    print("predicate: (hour_utc >= %d) & (hour_utc < %d)" % (DS, DE))
    print()

    snap = pq.read_table(SNAP).to_pandas()
    n_total = len(snap)
    print("rows in parquet (unfiltered): %s" % f"{n_total:,}")
    print("timestamp dtype as stored: %s" % snap["timestamp"].dtype)

    snap["timestamp"] = pd.to_datetime(snap["timestamp"])
    snap = snap.sort_values("timestamp").reset_index(drop=True)
    snap["hour_utc"] = snap["timestamp"].dt.hour
    kept = snap[(snap["hour_utc"] >= DS) & (snap["hour_utc"] < DE)].copy()
    n_kept = len(kept)

    print("timestamp min: %s" % snap["timestamp"].min())
    print("timestamp max: %s" % snap["timestamp"].max())
    print()
    print("rows kept after filter: %s" % f"{n_kept:,}")
    print("rows dropped:           %s" % f"{n_total - n_kept:,}")
    print()
    print("per-hour breakdown of kept rows:")
    vc = kept["hour_utc"].value_counts().sort_index()
    for h, c in vc.items():
        print("  hour %02d UTC: %s" % (h, f"{c:,}"))
    print("  sum of breakdown: %s" % f"{int(vc.sum()):,}")
    print()
    print("derivation: %s total rows -> hour_utc in [%d,%d) -> %s rows"
          % (f"{n_total:,}", DS, DE, f"{n_kept:,}"))
    print("expected: %s  |  derived: %s  |  verdict: %s"
          % (f"{EXPECTED:,}", f"{n_kept:,}", "MATCH" if n_kept == EXPECTED else "MISMATCH"))


if __name__ == "__main__":
    main()
