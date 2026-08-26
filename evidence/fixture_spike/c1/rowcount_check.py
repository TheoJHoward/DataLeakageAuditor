"""C1 provenance: row counts via pyarrow only (read-only on archive).
- num_rows metadata for the three ZC 2025-01 parquets
- snapshot rows with UTC hour in [14,19) to compare vs Phase 5 run log's 338,159
"""
import pyarrow.parquet as pq
import pyarrow.compute as pc

BASE = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"

for name in ["zc_snapshots_2025-01.parquet", "zc_trades_tagged_2025-01.parquet", "zc_mbo_2025-01.parquet"]:
    pf = pq.ParquetFile(BASE + "\\" + name)
    print(name, "num_rows =", pf.metadata.num_rows)

t = pq.read_table(BASE + r"\zc_snapshots_2025-01.parquet", columns=["timestamp"])
ts = t.column("timestamp")
print("timestamp type:", ts.type)
h = pc.hour(ts)
mask = pc.and_(pc.greater_equal(h, 14), pc.less(h, 15 + 4))
print("snapshot rows with UTC hour in [14,19):", pc.sum(pc.cast(mask, "int64")).as_py())

# distinct seconds in trades (context said 137,492) and aggressor_side value counts
tt = pq.read_table(BASE + r"\zc_trades_tagged_2025-01.parquet", columns=["aggressor_side"])
vc = pc.value_counts(tt.column("aggressor_side"))
print("aggressor_side value counts:", vc.to_pylist())
