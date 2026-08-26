"""V7 follow-up probe: WHERE do the same-second-adjacent rows fall?

For each instrument, months 2025-01 and 2025-08 (the M5 sample months), on the
lattice a4_runner actually loads: find adjacent row pairs with
floor(T_{i-1},'1s') == floor(T_i,'1s'), take the LATER row of each pair (the row
that receives the same-second residual after apply_causal_lag's shift(1)), and
classify it with the archive's own bucket_assigner.assign_buckets.

That tells us exactly which v4 (inst, bucket) cells retain the affected rows,
since a4_runner.process_cell filters to the bucket BEFORE the lag.

Reads the archive read-only (timestamp column only). Writes only in this dir.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
sys.path.insert(0, str(ROOT / "scripts" / "v4"))
from bucket_assigner import assign_buckets  # noqa: E402

OUT = Path(__file__).resolve().parent
MONTHS = ["2025-01", "2025-08"]


def data_dir_for(inst: str) -> Path:
    inst = inst.lower()
    if inst == "es":
        return ROOT / "processed" / "es" / "v4_morning_chunk"
    if inst in ("nq", "cl", "gc", "zc", "zs"):
        return ROOT / "processed" / inst / "v4_gapfill"
    return ROOT / "processed" / inst


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    rows = []
    for inst in ["es", "nq", "cl", "gc", "zc", "zs", "he", "le"]:
        for mm in MONTHS:
            p = data_dir_for(inst) / f"{inst}_snapshots_{mm}.parquet"
            if not p.exists():
                print(f"{inst} {mm}: MISSING {p}", flush=True)
                continue
            ts = pd.to_datetime(
                pq.read_table(str(p), columns=["timestamp"]).to_pandas()["timestamp"],
                utc=True).sort_values().reset_index(drop=True)
            v = ts.to_numpy()
            s = v.astype("datetime64[s]")
            idx = np.where(s[1:] == s[:-1])[0]
            later = pd.Series(pd.to_datetime(v[idx + 1], utc=True), name="ts_event")
            n_rows_month = len(v)
            if len(later) == 0:
                print(f"{inst} {mm}: n_rows={n_rows_month:,} pairs=0", flush=True)
                continue
            tagged = assign_buckets(pd.DataFrame({"ts_event": later}), inst.upper(),
                                    ts_col="ts_event")
            bcounts = tagged["bucket"].value_counts().to_dict()
            n_fs = int(tagged["in_full_session"].sum())
            ny = later.dt.tz_convert("America/New_York")
            print(f"{inst} {mm}: n_rows={n_rows_month:,} pairs={len(later)} "
                  f"in_full_session={n_fs} buckets={bcounts} "
                  f"NY_time_range=[{ny.min().time()} .. {ny.max().time()}]", flush=True)
            for b, c in bcounts.items():
                rows.append({"inst": inst, "month": mm, "n_rows_month": n_rows_month,
                             "n_same_second_pairs": len(later), "bucket": b, "n": c,
                             "n_in_full_session": n_fs,
                             "first_affected_ts_utc": str(later.min()),
                             "last_affected_ts_utc": str(later.max())})
    pd.DataFrame(rows).to_csv(OUT / "affected_row_buckets.csv", index=False)
    print(f"\nwrote {OUT / 'affected_row_buckets.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
