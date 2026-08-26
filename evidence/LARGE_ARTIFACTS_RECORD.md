# LARGE ARTIFACTS — hashes, durable location, producing command, reproducibility

**Ruled at R76/§62.1: these 20 files do NOT enter the repository.** Partly forced — GitHub rejects
blobs over 100 MB and five are 224–370 MB — and Git LFS would change what the tag hashes, which is
not going into the ceremony a fortnight out.

**Moved out of the temp scratchpad at R76/§62.2**, copied, **re-hashed at the destination**, compared,
and only then deleted from temp. 20/20 verified.

**Durable location:** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025_v30a_large_artifacts\`, a sibling of
the read-only archive on the same OneDrive Desktop the project already uses. Machine-readable move
record with every hash: `_MOVE_RECORD.json` at that location.

---

## §62.3 — CAN THE BYTES BE REGENERATED? **(a) YES · (b) NO · (c) YES**

### (a) Is the producing code in the repository? **YES — as of R76, and NOT BEFORE.**

| group | producer, now in `evidence/` |
|---|---|
| f2 rebuild pickles | `fixture_spike/f2/fixture.py`, `run_fixture.py`, `phase5_ml_fixture.py` |
| t4 CSVs | `fixture_spike/t4/t4_project.py` |
| p5probe parquets | `p5probe/p5_probe.py` |

**This was a live gap until this round.** R74/§56 brought in 230 *records* but filtered `.py` as
"script/build" — so `p5_probe.py`, and **the entire §9.2 kill-gate harness** (`killgate/k6/harness/`,
8 scripts, and `cases/_scripts/`, 16 scripts) existed only in the temp directory. **161 scripts were
brought in at R76.** The triage that missed them had a domain narrower than its claim, and it
excluded in the direction that hides the problem — which is H-L21, committed inside the round that
filed H-L21.

### (b) Are the inputs in the repository? **NO. They are external, and this is the answer that matters.**

All three groups read the **read-only archive** at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025`
(**684 GB**), verified from the producers' own source this pass:

- **f2** reads the archive's phase5 pipeline (`archive phase5_ml.py, write paths redirected`).
- **t4** reads `MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py`.
- **p5probe** reads `MBO_2025\processed\zc`.

**The inputs are outside the repository, outside the evidence tree, and outside the tag.**

### (c) Is the pipeline deterministic? **YES, demonstrated twice over.**

Two independent runs produce **byte-identical** output, and the evidence is recorded in two places
that were derived separately:

| file | repo-recorded `.sha256` | re-hashed at destination R76 |
|---|---|---|
| `contaminated_zc_2025-01_run1.pkl` | `73143359a90022f3…` | `36921b5d9ca7…` |
| `contaminated_zc_2025-01_run2.pkl` | `73143359a90022f3…` | `36921b5d9ca7…` |
| `corrected_zc_2025-01_run1.pkl` | `d5ca7b7ec45efcc0…` | `12c0ddef23cd…` |
| `corrected_zc_2025-01_run2.pkl` | `d5ca7b7ec45efcc0…` | `12c0ddef23cd…` |

*(The two hash columns differ because the repo `.sha256` files record the pickle's payload hash as
written by the producer, and the R76 column is a whole-file hash taken at the destination. **Within
each column run1 == run2**, which is the determinism claim.)* The same holds for the four t4 CSVs
(`32edf4389d9c` ×2 contaminated, `db4193aa1ad8` ×2 corrected) and for the p5probe parquets shared
across baseline / pertA / pertB.

---

## THE CONSEQUENCE, STATED RATHER THAN RESOLVED (§62.5)

**§62.3's test is (a) AND (b) AND (c). It does not pass, because (b) fails.**

**Hashes plus code are therefore NOT a complete record.** They are a complete record *conditional on
the 684 GB archive surviving*. The archive is:

- **not in the repository**, and not covered by the signed tag;
- **on the same single machine** as everything else in this project;
- the declared read-only source of truth for every fixture claim the registration makes.

So the bytes are not strictly irreplaceable — they are **reproducible for exactly as long as the
archive exists, and unreproducible the moment it does not.** Moving them out of a temp directory
removed the acute risk. It did not remove that dependency, and no arrangement inside this repository
can.

**This is the trade-off in its real form, for the author to rule on** — not whether 1.5 GB should be
committed, but whether a pre-registration whose fixture claims rest on a 684 GB single-copy external
archive should say so in `DEVIATIONS.md` §12, and whether that archive should be backed up before
the tag rather than after.

**Nothing here is a recommendation to delay the tag.** The registration's claims about the fixture
are already recorded, hashed, and independently checked; what is at stake is a future reader's
ability to *rebuild* the fixture, not the integrity of what is being registered.

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
