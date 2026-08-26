"""V3 dtype witness: parquet SCHEMA-ONLY reads for the six g2-produced instruments.

Reads metadata only (pyarrow.parquet.ParquetFile / read_schema) -- no data pages
are loaded and the archive is never written to.

Path logic mirrors a4_runner.py:134-140 exactly:
  es              -> ROOT/processed/es/v4_morning_chunk
  nq,cl,gc,zc,zs  -> ROOT/processed/<inst>/v4_gapfill
Trades filename per a4_runner.py:214: {inst}_trades_tagged_{YYYY-MM}.parquet
MONTHS per a4_runner.py:89: 2025-01 .. 2025-12
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pyarrow
import pyarrow.parquet as pq

ROOT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
INSTS = ["es", "nq", "cl", "gc", "zc", "zs"]


def data_dir_for(inst: str) -> Path:
    inst = inst.lower()
    if inst == "es":
        return ROOT / "processed" / "es" / "v4_morning_chunk"
    if inst in ("nq", "cl", "gc", "zc", "zs"):
        return ROOT / "processed" / inst / "v4_gapfill"
    return ROOT / "processed" / inst


def first_existing_trades(inst: str):
    d = data_dir_for(inst)
    for mm in MONTHS:
        p = d / f"{inst}_trades_tagged_{mm}.parquet"
        if p.exists():
            return p
    return None


def col_witness(pf: pq.ParquetFile, arrow_schema, name: str) -> dict:
    out = {"column": name}
    idx = None
    for i in range(len(arrow_schema.names)):
        if arrow_schema.names[i] == name:
            idx = i
            break
    if idx is None:
        out["present"] = False
        return out
    out["present"] = True
    out["arrow_type"] = str(arrow_schema.field(idx).type)
    # parquet-level physical/logical type via ParquetSchema
    pschema = pf.schema  # ParquetSchema
    pidx = None
    for j in range(len(pschema.names)):
        if pschema.names[j] == name:
            pidx = j
            break
    if pidx is not None:
        col = pschema.column(pidx)
        out["physical_type"] = col.physical_type
        out["logical_type"] = str(col.logical_type)
        out["converted_type"] = str(col.converted_type)
    return out


def main():
    results = []
    for inst in INSTS:
        rec = {"instrument": inst, "dir": str(data_dir_for(inst))}
        p = first_existing_trades(inst)
        if p is None:
            # record which filenames were probed
            rec["file"] = None
            rec["verdict"] = "FILE-ABSENT"
            rec["dir_exists"] = data_dir_for(inst).exists()
            results.append(rec)
            continue
        st = p.stat()
        rec["file"] = str(p)
        rec["file_size_bytes"] = st.st_size
        rec["mtime_utc"] = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat()
        pf = pq.ParquetFile(str(p))
        arrow_schema = pf.schema_arrow
        rec["num_rows"] = pf.metadata.num_rows
        rec["num_columns"] = pf.metadata.num_columns
        rec["created_by"] = pf.metadata.created_by
        rec["all_columns"] = list(arrow_schema.names)
        rec["size"] = col_witness(pf, arrow_schema, "size")
        rec["is_buy_aggressor"] = col_witness(pf, arrow_schema, "is_buy_aggressor")
        sz = rec["size"]
        if not sz.get("present"):
            rec["verdict"] = "WITNESSED-other(size-column-missing)"
        elif sz.get("arrow_type") == "uint32":
            rec["verdict"] = "WITNESSED-uint32"
        else:
            rec["verdict"] = f"WITNESSED-other({sz.get('arrow_type')})"
        results.append(rec)

    print("pyarrow", pyarrow.__version__)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
