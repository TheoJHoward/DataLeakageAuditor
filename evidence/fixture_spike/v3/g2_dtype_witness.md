# V3 — Direct dtype witness for the six g2-produced instruments

**Date of witness:** 2026-08-11
**Method:** parquet SCHEMA-ONLY metadata read (`pyarrow.parquet.ParquetFile` — `.schema_arrow` for the arrow type, `.schema.column(i)` for the parquet physical/logical types). No data pages loaded; no archive mutation. Script: `schema_witness.py` (same directory as this file).
**Environment at witness time:** pyarrow 23.0.1 (matches the pinned original environment: pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1).

**Path resolution (verbatim source of truth):** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py`, `data_dir_for` at lines 134-140:

```python
def data_dir_for(inst: str) -> Path:
    inst = inst.lower()
    if inst == "es":
        return ROOT / "processed" / "es" / "v4_morning_chunk"
    if inst in ("nq", "cl", "gc", "zc", "zs"):
        return ROOT / "processed" / inst / "v4_gapfill"
    return ROOT / "processed" / inst
```

Trades filename pattern per a4_runner.py line 214: `{inst}_trades_tagged_{mm}.parquet` with `MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]` (line 89). `ROOT` resolves to `MBO_2025/` (line 44). One file per instrument was witnessed — the first existing month in a4_runner's own iteration order, which was 2025-01 for all six.

## Six-row witness table

| Inst | File (one witnessed parquet) | Size (bytes) | mtime (UTC) | Rows | `size` arrow type | `size` parquet physical / logical | `is_buy_aggressor` | Verdict |
|------|------------------------------|--------------|-------------|------|-------------------|-----------------------------------|--------------------|---------|
| es | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\es\v4_morning_chunk\es_trades_tagged_2025-01.parquet` | 271,334,356 | 2026-04-17T06:05:25.365287+00:00 | 10,985,167 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |
| nq | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\v4_gapfill\nq_trades_tagged_2025-01.parquet` | 215,692,895 | 2026-04-16T23:38:46.343092+00:00 | 8,503,243 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |
| cl | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\cl\v4_gapfill\cl_trades_tagged_2025-01.parquet` | 54,086,905 | 2026-04-17T09:12:05.410228+00:00 | 2,077,707 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |
| gc | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\gc\v4_gapfill\gc_trades_tagged_2025-01.parquet` | 38,640,914 | 2026-04-17T09:45:40.267306+00:00 | 1,449,440 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |
| zc | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\v4_gapfill\zc_trades_tagged_2025-01.parquet` | 11,518,576 | 2026-04-17T03:58:32.315508+00:00 | 398,188 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |
| zs | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zs\v4_gapfill\zs_trades_tagged_2025-01.parquet` | 15,405,144 | 2026-04-17T03:48:15.890150+00:00 | 561,265 | `uint32` | INT32 / `Int(bitWidth=32, isSigned=false)` (converted UINT_32) | arrow `bool` (BOOLEAN) | **WITNESSED-uint32** |

## Supporting detail (identical across all six files)

- `created_by` in parquet footer: `parquet-cpp-arrow version 23.0.1` — written by the same pyarrow version as the pinned environment.
- Column set (17 columns, same order in all six): `ts_recv, ts_event, rtype, publisher_id, instrument_id, action, side, price, size, channel_id, order_id, flags, ts_in_delta, sequence, symbol, aggressor_side, is_buy_aggressor`.
- `size`: parquet physical INT32 with logical `Int(bitWidth=32, isSigned=false)` / converted UINT_32 → decodes as arrow `uint32`, i.e. pandas `uint32` on `to_pandas()`.
- `is_buy_aggressor`: parquet BOOLEAN → arrow `bool` in every file, consistent with a4_runner.py:218 loading it and line 307 (`tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])`) operating on a genuine boolean column.

## Verdict

All six g2-produced instruments: **WITNESSED-uint32**. The v4 wrap claim for es/nq/cl/gc/zc/zs is now a direct metadata witness, not provenance inference: `size` is stored unsigned-32-bit in the exact parquets a4_runner.py loads, so the uncast negation at a4_runner.py:307 (`-tr["size"]` on a uint32 column under numpy 2.4.2) operates on unsigned input for these instruments.

## Scope limits

- One month witnessed per instrument (2025-01, the first month in a4_runner's own load order). Other months in each directory were not read; no claim is made about them here.
- This item witnesses storage dtype only. What `np.where(..., tr["size"], -tr["size"])` produces at runtime under pandas 3.0.1 / numpy 2.4.2 is a separate (already-established) question; this file only pins the input dtype.
