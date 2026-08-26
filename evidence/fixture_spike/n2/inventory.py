"""ITEM N2 (a)+(b) — lattice-generation provenance inventory.

For every fixture instrument-month (8 instruments x {2025-01, 2025-08..2025-12}), enumerate every
{inst}_snapshots_{month}.parquet copy on disk under the READ-ONLY archive
C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025 and record:
  path, size, mtime, sha256, md5, total_rows (parquet footer num_rows),
  filtered_rows (the lattice: hour_utc in [day_start_utc, day_end_utc) per phase5_ml.py INST_META),
  ts_min/ts_max, n_distinct_seconds, same_second_rows (rows whose floor(T,1s) == floor(T_prev,1s)).

Manifest coverage is resolved against the two archive manifests (both md5):
  pc2_transfer/transfer/checksums.txt   (paths relative to pc2_transfer/transfer/)
  PC2_TRANSFER_v4/manifest.csv          (paths relative to the archive root == PC2_TRANSFER_v4/)

Reads only; writes only under the n2 scratchpad directory.
"""
import csv, hashlib, io, json, os, re, sys, time
from pathlib import Path
import polars as pl
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding="utf-8")

ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude"
           r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n2")

# phase5_ml.py L49-57 day_start_utc / day_end_utc
INST_SESSION = {
    "es": (14, 22), "nq": (14, 22), "gc": (13, 22), "cl": (13, 22),
    "zs": (14, 19), "zc": (14, 19), "le": (14, 19), "he": (14, 19),
}
INSTS = ["cl", "es", "gc", "he", "le", "nq", "zc", "zs"]
MONTHS = ["2025-01", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12"]
ONE_S = 1_000_000_000

FNAME_RE = re.compile(r"^(cl|es|gc|he|le|nq|zc|zs)_snapshots_(2025-(?:01|08|09|10|11|12))\.parquet$")


def load_manifests():
    """Return {normalized_relpath_lower: (manifest_name, line_no, md5, size_or_None)}."""
    cov = {}
    # 1) pc2_transfer/transfer/checksums.txt  ->  "md5  data/gc/gc_snapshots_2025-01.parquet"
    p1 = ARCH / "pc2_transfer" / "transfer" / "checksums.txt"
    for i, line in enumerate(p1.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        md5, rel = parts[0].strip(), parts[1].strip().lstrip("*")
        key = ("pc2_transfer/transfer/" + rel.replace("\\", "/")).lower()
        cov[key] = ("pc2_transfer/transfer/checksums.txt", i, md5.lower(), None)
    # 2) PC2_TRANSFER_v4/manifest.csv -> relative_path,size_bytes,md5_hash
    p2 = ARCH / "PC2_TRANSFER_v4" / "manifest.csv"
    with open(p2, newline="", encoding="utf-8", errors="replace") as fh:
        rd = csv.DictReader(fh)
        for i, row in enumerate(rd, 2):   # line 1 = header
            rel = row["relative_path"].replace("\\", "/")
            key = ("PC2_TRANSFER_v4/" + rel).lower()
            cov[key] = ("PC2_TRANSFER_v4/manifest.csv", i, row["md5_hash"].strip().lower(),
                        int(row["size_bytes"]))
    return cov


MANIFEST = load_manifests()


def manifest_lookup(abs_path: Path):
    rel = abs_path.relative_to(ARCH).as_posix()
    hits = []
    # direct location match
    if rel.lower() in MANIFEST:
        hits.append((rel, MANIFEST[rel.lower()]))
    return hits


def digest_and_read(path: Path):
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    md5 = hashlib.md5(data).hexdigest()
    return data, sha, md5


def measure(inst, data):
    ds, de = INST_SESSION[inst]
    buf = io.BytesIO(data)
    pf = pq.ParquetFile(buf)
    total = pf.metadata.num_rows
    cols = [f.name for f in pf.schema_arrow]
    buf.seek(0)
    snap = pl.read_parquet(buf, columns=["timestamp"]).sort("timestamp")
    lat = (snap.with_columns(pl.col("timestamp").dt.hour().alias("h"))
               .filter((pl.col("h") >= ds) & (pl.col("h") < de))
               .select(pl.col("timestamp").dt.timestamp("ns").alias("T")))
    n = lat.height
    if n == 0:
        return total, cols, n, None, None, 0, 0, 0, 0
    T = lat["T"]
    tmin, tmax = int(T.min()), int(T.max())
    sec = lat.select(((pl.col("T") // ONE_S) * ONE_S).alias("s"))
    n_sec = sec["s"].n_unique()
    d = lat.with_columns(pl.col("T").shift(1).alias("Tp")).slice(1)
    same_sec = int(d.select((((pl.col("T") // ONE_S)) == ((pl.col("Tp") // ONE_S))).sum()).item())
    sub_sec = int(d.select(((pl.col("T") - pl.col("Tp")) < ONE_S).sum()).item())
    gap_rows = int(d.select(((pl.col("T") - pl.col("Tp")) != ONE_S).sum()).item())
    return total, cols, n, tmin, tmax, n_sec, same_sec, sub_sec, gap_rows


def location_family(rel: str) -> str:
    r = rel.lower()
    if r.startswith("processed/") and "/v4_gapfill/" in r:
        return "B_processed_v4_gapfill"
    if r.startswith("processed/") and "/v4_morning_chunk/" in r:
        return "B_processed_v4_morning_chunk"
    if r.startswith("processed/"):
        return "A_processed_FIXTURE_PATH"
    if r.startswith("pc2_transfer_v4/") or r.startswith("pc2_transfer_v4"):
        return "D_PC2_TRANSFER_v4"
    if r.startswith("pc2_transfer/transfer/data/"):
        return "F_pc2_transfer_transfer_data"
    if r.startswith("pc2_transfer/processed/"):
        return "E_pc2_transfer_processed"
    if r.startswith("transfer/data/"):
        return "G_transfer_data"
    return "OTHER"


def main():
    t0 = time.time()
    files = []
    for dirpath, dirnames, filenames in os.walk(ARCH):
        for fn in filenames:
            m = FNAME_RE.match(fn)
            if m:
                files.append((Path(dirpath) / fn, m.group(1), m.group(2)))
    files.sort(key=lambda t: (t[1], t[2], str(t[0])))
    print(f"found {len(files)} snapshot files for the fixture window", flush=True)

    rows = []
    for k, (p, inst, month) in enumerate(files, 1):
        st = p.stat()
        data, sha, md5 = digest_and_read(p)
        total, cols, n, tmin, tmax, n_sec, same_sec, sub_sec, gap_rows = measure(inst, data)
        rel = p.relative_to(ARCH).as_posix()
        fam = location_family(rel.replace("PC2_TRANSFER_v4", "PC2_TRANSFER_v4"))
        if rel.startswith("PC2_TRANSFER_v4/"):
            fam = "D_PC2_TRANSFER_v4"
        hits = manifest_lookup(p)
        if hits:
            _, (mname, mline, mmd5, msize) = hits[0]
            covered, mstat = mname, ("MATCH" if mmd5 == md5 else "MISMATCH")
            mline_s, mmd5_s = mline, mmd5
        else:
            covered, mstat, mline_s, mmd5_s = "NOT_COVERED", "", "", ""
        ds, de = INST_SESSION[inst]
        rows.append(dict(
            instrument=inst, month=month, location_family=fam, rel_path=rel,
            abs_path=str(p), size_bytes=st.st_size,
            mtime_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(st.st_mtime)),
            sha256=sha, md5=md5,
            manifest=covered, manifest_line=mline_s, manifest_md5=mmd5_s, manifest_status=mstat,
            day_start_utc=ds, day_end_utc=de,
            total_rows=total, filtered_rows=n,
            ts_min_ns=tmin, ts_max_ns=tmax, distinct_seconds=n_sec,
            same_second_rows=same_sec, subsecond_spacing_rows=sub_sec, nonexact_1s_gap_rows=gap_rows,
            n_columns=len(cols),
        ))
        print(f"[{k}/{len(files)}] {rel}  size={st.st_size}  rows={total}  filt={n}  "
              f"same_sec={same_sec}  {covered}:{mstat}", flush=True)

    df = pl.DataFrame(rows)
    df.write_csv(OUT / "lattice_provenance.csv")
    print("wrote", OUT / "lattice_provenance.csv", f"({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
