"""V7 minimal lattice probe (READ-ONLY on the archive).

Question: in the lattice that v4/v5 actually load (a4_runner.load_snapshots),
can two CONSECUTIVE rows share a wall-clock second?  That is the exact
precondition for the same-second residual channel, because
  - add_trade_features joins on second = floor(ts,'1s') by EQUALITY, and
  - apply_causal_lag shifts by one ROW.

Reads ONLY the 'timestamp' column. Writes nothing outside this scratchpad.
Replicates a4_runner.load_snapshots ordering exactly:
    concat months 2025-01..2025-12 -> sort_values("timestamp") -> reset_index
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
OUT = Path(__file__).resolve().parent


def data_dir_for(inst: str) -> Path:
    """Byte-copy of a4_runner.data_dir_for."""
    inst = inst.lower()
    if inst == "es":
        return ROOT / "processed" / "es" / "v4_morning_chunk"
    if inst in ("nq", "cl", "gc", "zc", "zs"):
        return ROOT / "processed" / inst / "v4_gapfill"
    return ROOT / "processed" / inst


def probe(inst: str, base: Path, tag: str, months=MONTHS) -> list[dict]:
    rows = []
    parts = []
    for mm in months:
        p = base / f"{inst}_snapshots_{mm}.parquet"
        if not p.exists():
            rows.append({"lattice": tag, "inst": inst, "month": mm,
                         "n_rows": 0, "file": "MISSING", "path": str(p)})
            continue
        ts = pq.read_table(str(p), columns=["timestamp"]).to_pandas()["timestamp"]
        ts = pd.to_datetime(ts, utc=True)
        parts.append(ts)
        # per-month, in file order (no re-sort), adjacency
        v = ts.to_numpy()
        sec = v.astype("datetime64[s]")
        same = int((sec[1:] == sec[:-1]).sum()) if len(v) > 1 else 0
        dup = int((v[1:] == v[:-1]).sum()) if len(v) > 1 else 0
        rows.append({"lattice": tag, "inst": inst, "month": mm,
                     "n_rows": int(len(v)),
                     "adj_same_second_pairs": same,
                     "adj_exact_dup_ts": dup,
                     "file": "PRESENT", "path": str(p)})
    if parts:
        allts = pd.concat(parts, ignore_index=True).sort_values().reset_index(drop=True)
        v = allts.to_numpy()
        sec = v.astype("datetime64[s]")
        same = int((sec[1:] == sec[:-1]).sum())
        dup = int((v[1:] == v[:-1]).sum())
        d = (v[1:] - v[:-1]).astype("timedelta64[ns]").astype(np.int64)
        rows.append({"lattice": tag, "inst": inst, "month": "ALL12_SORTED",
                     "n_rows": int(len(v)),
                     "adj_same_second_pairs": same,
                     "adj_exact_dup_ts": dup,
                     "min_gap_ns": int(d.min()) if len(d) else None,
                     "median_gap_ns": int(np.median(d)) if len(d) else None,
                     "n_gap_lt_1s": int((d < 1_000_000_000).sum()) if len(d) else 0,
                     "file": "AGG", "path": str(base)})
    return rows


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.time()
    out = []
    # (1) exactly what v4/v5 load
    for inst in ["es", "nq", "cl", "gc", "zc", "zs", "he", "le"]:
        t = time.time()
        r = probe(inst, data_dir_for(inst), "v4_load_snapshots")
        out.extend(r)
        agg = [x for x in r if x["month"] == "ALL12_SORTED"]
        print(f"{inst}: {agg[0] if agg else 'NO FILES'}  [{time.time()-t:.1f}s]",
              flush=True)
    # (2) cross-check: the Phase-5 lattice used by M5 (same files only for he/le)
    for inst in ["zc", "zs", "gc", "cl", "es", "he", "le"]:
        r = probe(inst, ROOT / "processed" / inst, "phase5_processed_root",
                  months=["2025-01", "2025-08"])
        out.extend(r)
        print(f"phase5 {inst}: "
              f"{[(x['month'], x.get('n_rows'), x.get('adj_same_second_pairs')) for x in r]}",
              flush=True)
    df = pd.DataFrame(out)
    df.to_csv(OUT / "lattice_same_second_probe.csv", index=False)
    print(f"\nwrote {OUT / 'lattice_same_second_probe.csv'}  "
          f"total {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
