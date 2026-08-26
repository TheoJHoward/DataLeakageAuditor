"""C1(b) addendum: the archive holds a SECOND, later ZC 2025-01 snapshots file
under processed/zc/v4_gapfill/. Apply the identical [14,19) UTC-hour filter to it
so the 338,159 figure is pinned to a specific generation of the file.

Read-only against the archive.
"""
import os
from datetime import datetime, timezone

import pandas as pd
import pyarrow.parquet as pq

A = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\zc_snapshots_2025-01.parquet"
B = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\v4_gapfill\zc_snapshots_2025-01.parquet"
DS, DE = 14, 19


def stat(path):
    snap = pq.read_table(path).to_pandas()
    n_total = len(snap)
    snap["timestamp"] = pd.to_datetime(snap["timestamp"])
    snap = snap.sort_values("timestamp").reset_index(drop=True)
    snap["hour_utc"] = snap["timestamp"].dt.hour
    kept = snap[(snap["hour_utc"] >= DS) & (snap["hour_utc"] < DE)]
    return n_total, len(kept), snap["timestamp"].min(), snap["timestamp"].max()


def main():
    print()
    print("=" * 78)
    print("ADDENDUM - competing generation of the same month on disk")
    print("run_utc: %s" % datetime.now(timezone.utc).isoformat())
    print("=" * 78)
    print("Same predicate (hour_utc in [%d,%d)) applied to both files." % (DS, DE))
    print()
    for label, path in (("PRE-GAPFILL (the C1 file)", A), ("v4_gapfill (later build)", B)):
        n_total, n_kept, tmin, tmax = stat(path)
        print("%s" % label)
        print("  path: %s" % path)
        print("  size_bytes: %d" % os.path.getsize(path))
        print("  mtime_utc: %s" % datetime.fromtimestamp(
            os.path.getmtime(path), timezone.utc).isoformat())
        print("  rows total: %s" % f"{n_total:,}")
        print("  rows in [14,19): %s" % f"{n_kept:,}")
        print("  ts min/max: %s / %s" % (tmin, tmax))
        print()


if __name__ == "__main__":
    main()
