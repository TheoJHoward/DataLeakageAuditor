"""ITEM N2 — finalise lattice_provenance.csv.

Adds, on top of inventory.py's measurements:
  generation            v3_pre_gapfill | v4_gapfill | v4_morning_chunk
  is_fixture_path       TRUE for processed/{inst}/{inst}_snapshots_{month}.parquet
                        (the path phase5_ml.py / the builder / the M5+N1 sweep read)
  manifest_by_path      manifest line whose relative_path resolves to THIS file, under either
                        admissible root (archive root, or the manifest's own package root)
  manifest_by_md5       manifest line carrying this file's md5, wherever it points
  manifest_status       MATCH / MISMATCH / NOT_COVERED
  block_* columns       merged from block_overlap.csv (native concat-block structure)

Both archive manifests are md5. checksums.txt paths are relative to the directory holding it;
manifest.csv paths ("processed/zc/v4_gapfill/...") resolve BOTH under PC2_TRANSFER_v4/ and,
verbatim, under the archive root -- both resolutions are recorded.
"""
import csv, sys
from pathlib import Path
import polars as pl

sys.stdout.reconfigure(encoding="utf-8")
ARCH = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
OUT = Path(r"C:\Users\ttbea\AppData\Local\Temp\claude"
           r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
           r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n2")

# ---- manifests -------------------------------------------------------------
by_path, by_md5 = {}, {}


def add(key, name, line, md5, size):
    by_path.setdefault(key.lower(), []).append((name, line, md5.lower(), size))
    by_md5.setdefault(md5.lower(), []).append((name, line, key))


for cpath, root in [(ARCH / "pc2_transfer" / "transfer" / "checksums.txt", "pc2_transfer/transfer"),
                    (ARCH / "transfer" / "checksums.txt", "transfer")]:
    if not cpath.exists():
        continue
    name = cpath.relative_to(ARCH).as_posix()
    for i, line in enumerate(cpath.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            add(f"{root}/{parts[1].strip().lstrip('*')}", name, i, parts[0], None)

mpath = ARCH / "PC2_TRANSFER_v4" / "manifest.csv"
mname = mpath.relative_to(ARCH).as_posix()
with open(mpath, newline="", encoding="utf-8", errors="replace") as fh:
    for i, row in enumerate(csv.DictReader(fh), 2):
        rel = row["relative_path"].replace("\\", "/")
        md5, size = row["md5_hash"].strip(), int(row["size_bytes"])
        add(f"PC2_TRANSFER_v4/{rel}", mname, i, md5, size)     # package-root resolution
        add(rel, mname, i, md5, size)                          # archive-root resolution


def generation(rel: str) -> str:
    if "/v4_gapfill/" in rel:
        return "v4_gapfill"
    if "/v4_morning_chunk/" in rel:
        return "v4_morning_chunk"
    return "v3_pre_gapfill"


def main():
    d = pl.read_csv(OUT / "lattice_provenance.csv")
    b = (pl.read_csv(OUT / "block_overlap.csv")
           .select("path", "native_blocks", "overlapping_block_pairs",
                   "max_rows_per_timestamp", "duplicate_timestamps",
                   "filtered_distinct_seconds", "filtered_max_rows_per_second",
                   "filtered_excess_rows")
           .rename({"path": "abs_path"}))

    gens, isfix, mp, ml, mm, ms, mby5 = [], [], [], [], [], [], []
    for r in d.iter_rows(named=True):
        rel, md5 = r["rel_path"], r["md5"].lower()
        gens.append(generation(rel))
        isfix.append(rel.startswith("processed/") and "/v4_" not in rel)
        hits = by_path.get(rel.lower(), [])
        if hits:
            name, line, hmd5, hsize = hits[0]
            mp.append(name); ml.append(line); mm.append(hmd5)
            ms.append("MATCH" if hmd5 == md5 else "MISMATCH")
        else:
            mp.append("NOT_COVERED"); ml.append(None); mm.append(""); ms.append("NOT_COVERED")
        h5 = by_md5.get(md5, [])
        mby5.append("; ".join(f"{n}:L{l}->{k}" for n, l, k in h5) if h5 else "")

    d = (d.drop("manifest", "manifest_line", "manifest_md5", "manifest_status")
          .with_columns(
              pl.Series("generation", gens), pl.Series("is_fixture_path", isfix),
              pl.Series("manifest_by_path", mp),
              pl.Series("manifest_line", ml, dtype=pl.Int64),
              pl.Series("manifest_md5", mm), pl.Series("manifest_status", ms),
              pl.Series("manifest_by_md5", mby5))
          .drop("distinct_seconds", "same_second_rows")
          .join(b, on="abs_path", how="left")
          .sort(["instrument", "month", "generation", "rel_path"]))
    d.write_csv(OUT / "lattice_provenance.csv")
    print("rows", d.height)
    for r in (d.group_by("location_family", "generation", "manifest_by_path", "manifest_status")
                .len().sort("location_family").iter_rows()):
        print(r)


if __name__ == "__main__":
    main()
