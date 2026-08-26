#!/usr/bin/env python3
"""§70 — record §69.4(a) sync state and (b) input footprint."""
import pathlib

p = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/LARGE_ARTIFACTS_RECORD.md")
s = p.read_text(encoding="utf-8")

NEW = r'''
---

## §69.4 — TWO MEASURED FACTS THAT CHANGE THE SIZE OF THE PROBLEM (R77/§70)

### (a) Is the archive synced to OneDrive? **NO. And neither is anything else.**

Read from the sync client's own state, not from the path:

| evidence | finding |
|---|---|
| `OneDrive.exe` process | **NOT RUNNING** |
| `SyncEngineDatabase.db` last write | **5 September 2023** — nearly three years ago |
| account `.dat` last write | 5 September 2023 |
| `MBO_2025` in the sync database | **absent** (UTF-16 and ASCII scans) |
| `PREREG` in the sync database | **absent** |
| file attributes, archive and repo alike | `PLAIN` — no `PINNED`, `UNPINNED` or placeholder bits |
| Desktop shell folder | `C:\Users\ttbea\OneDrive\Desktop` — Known Folder Move *was* configured |

**The folder is named OneDrive; it is not synced.** Known Folder Move redirected the Desktop at some
point, then the sync client stopped and has not run since September 2023.

**The consequence is wider than this record's subject.** It is not that 684 GB of archive is
unbacked — **it is that nothing in this project is backed up, including the repository, the
evidence tree, and the 1.54 GB just moved to `MBO_2025_v30a_large_artifacts\`.** Every copy of every
artifact this registration depends on is on one machine, on one disk.

### (b) What is the ACTUAL input footprint? **346 MB, not 684 GB.**

Measured from what the three producers actually read, traced through their own source:

| input | size |
|---|---|
| `processed/zc/zc_mbo_2025-01.parquet` | 173.5 MB |
| `processed/zc/zc_mbo_2025-08.parquet` | 119.3 MB |
| `processed/zc/zc_snapshots_2025-01.parquet` | 15.2 MB |
| `processed/zc/zc_snapshots_2025-08.parquet` | 16.7 MB |
| `processed/zc/zc_trades_tagged_2025-01.parquet` | 11.0 MB |
| `processed/zc/zc_trades_tagged_2025-08.parquet` | 7.7 MB |
| `results/pc2_all_phases/_scripts` (t4's reference, 118 files) | 2.6 MB |
| **TOTAL** | **124 files, 346 MB — 0.049% of the archive** |

`phase5_ml_fixture.py` sets `PROJECT = MBO_2025`, `PROC = PROJECT/"processed"`, and
`LOCAL_DATA = C:\MBO_data` which does not exist, so `get_data_dir` falls back to `PROC`. The fixture
is **ZC 2025-01 and 2025-08 only**; nothing else in `processed/` (249 GB), `pc2_transfer/` (210 GB)
or `raw_data/` (204 GB) is read by any of the three producers.

**§70.2 was: do not recommend a backup strategy until (b) is measured.** It is now measured. The
factual position, with no recommendation attached: **the reproducibility-critical inputs are
346 MB** — small enough to sit beside the evidence tree, on external media, or anywhere else. The
constraint that made this look like a 684 GB problem does not exist. **What to do about that, and
about the fact that nothing in the project is backed up at all, is the author's call.**
'''

p.write_text(s + NEW, encoding="utf-8")
print("LARGE_ARTIFACTS_RECORD.md: \u00a769.4(a) and (b) recorded")
