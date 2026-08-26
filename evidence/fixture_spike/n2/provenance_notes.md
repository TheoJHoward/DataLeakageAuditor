# ITEM N2 — LATTICE-GENERATION PROVENANCE

Scope: 8 instruments x {2025-01, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12} = 48 fixture
instrument-months. Every `{inst}_snapshots_{month}.parquet` copy on disk under the read-only
archive was enumerated by exhaustive `os.walk`: **228 files**, 100% accounted for, none skipped.

Artifacts in this directory:

| file | content |
|---|---|
| `lattice_provenance.csv` | 228 rows, one per file: path, size, mtime, sha256, md5, manifest coverage, total + filtered row counts, block structure |
| `block_overlap.csv` | 84 rows: native concat-block structure per file (both generations) |
| `spacing_classification.csv` | same-second-pair classification (day-edge / >60 s gap / elsewhere) |
| `spacing_by_hour.csv` | same-second pairs by UTC hour |
| `inventory.py`, `enrich.py`, `blocks.py`, `spacing.py` | the scripts that produced the above |
| `inventory_run.log` | captured stdout of the 228-file inventory run |

Runtime: inventory 19.2 s for 228 files (~5.2 GB hashed sha256 + md5).

---

## (a) + (b) EXACTLY TWO GENERATIONS EXIST — and the fixture reads the older one

Across all 228 files there are exactly **2 distinct sha256 values per instrument-month** for
cl / es / gc / nq / zc / zs, and exactly **1** for he / le. Six location families hold copies:

| family | path shape | generation | manifest |
|---|---|---|---|
| A | `processed/{inst}/{inst}_snapshots_{m}.parquet` | **v3_pre_gapfill** | NOT_COVERED (36) / MATCH (12: he+le) |
| B | `processed/{inst}/v4_gapfill/` , `processed/es/v4_morning_chunk/` | v4 | `PC2_TRANSFER_v4/manifest.csv` MATCH (36) |
| D | `PC2_TRANSFER_v4/processed/...` | v4 (+ he/le v3) | `PC2_TRANSFER_v4/manifest.csv` MATCH (48) |
| E | `pc2_transfer/processed/{inst}/` | v3_pre_gapfill | NOT_COVERED (48) |
| F | `pc2_transfer/transfer/data/{gc,nq,zc,zs}/` | v3_pre_gapfill | `pc2_transfer/transfer/checksums.txt` MATCH (24) |
| G | `transfer/data/{gc,nq,zc,zs}/` | v3_pre_gapfill | `transfer/checksums.txt` MATCH (24) |

**Every manifest-covered file MATCHES its recorded md5. Zero MISMATCH across all 228 files.**
The two `checksums.txt` files (`transfer/` and `pc2_transfer/transfer/`) are byte-identical
(md5 `4b692b0a9d02d9b78a99575765802979`); the task named only the latter, so F and G are two
mirrors of the same manifest and the same generation.

Manifest path resolution note: `PC2_TRANSFER_v4/manifest.csv` `relative_path` values such as
`processed/zc/v4_gapfill/zc_snapshots_2025-01.parquet` resolve **both** under the package root
`PC2_TRANSFER_v4/` (family D) **and** verbatim under the archive root (family B). Both
resolutions are recorded in `lattice_provenance.csv` (`manifest_by_path`, `manifest_line`), and
both files are byte-identical, so the ambiguity is harmless. `checksums.txt` paths (`data/...`)
are relative to the directory holding the file.

### The fixture path is generation v3_pre_gapfill — for all 48 instrument-months

`scripts/phase5/phase5_ml.py`:

```
L104  def get_data_dir(sym):
L105      local = LOCAL_DATA / sym
L106      return local if local.exists() else PROC / sym
...
L38   PROJECT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")
L39   PROC = PROJECT / "processed"
L40   LOCAL_DATA = Path(r"C:\MBO_data")
...
L177      data_dir = get_data_dir(sym)
L178      p = data_dir / f"{sym}_snapshots_{month}.parquet"
```

`C:\MBO_data` **does not exist on this machine** (verified: `ls: cannot access 'C:/MBO_data':
No such file or directory`), so `get_data_dir` falls through to `PROC / sym` and the lattice is
`processed/{inst}/{inst}_snapshots_{month}.parquet` — family A, generation **v3_pre_gapfill** —
for every instrument-month. This is the file the builder and the M5/N1 sweep read.

> Declaration caveat: the fixture path is machine-conditional. Line 106 would silently switch
> the entire lattice to `C:\MBO_data\{sym}\` on any machine where that directory exists. The
> generation identification here is valid for this machine, where the directory is absent.

**36 of the 48 fixture-path files are covered by no manifest in the archive.** The 12 that are
covered are exactly he and le — see (e).

### Consistency with the M5 prior result

M5 reported ZC 2025-08 as `90868/2857 of 554,303 corrected rows`. This inventory measures the
ZC 2025-08 fixture-path lattice at **554,304 rows**; corrected rows = N-1 = **554,303**. Exact
match. M1's 338,159 for ZC 2025-01 also reproduces exactly. **No contradiction found.**

---

## (c) SPACING QUESTION — ANSWERED (not undecidable). The hypothesised code paths are REFUTED.

### The hypothesis was tested and fails by three orders of magnitude

`scripts/pipeline/process_mbo.py` `reconstruct_day` (L322-370) has exactly two paths that can
emit two snapshots inside one wall-clock second:

- **gap re-anchor**, L347-352: `if gap > max_gap_ns:` emit at the stale `next_snap`, then
  `next_snap = ts` — re-anchoring the 1 s grid to a new sub-second phase;
- **final-snapshot stamp**, L365-368: after the loop, one extra snapshot stamped
  `ts_events[-1]` rather than on the grid.

Measured on the actual ZC 2025-08 fixture lattice (`spacing_classification.csv`), classifying
all 211,450 same-second adjacent pairs in the `[14,19)` filtered view:

| classification | pairs |
|---|---|
| row is the last row of its UTC date (final-snapshot stamp, L365-368) | **20** |
| adjacent to a > 60 s spacing (gap re-anchor, L347-352) | **24** |
| either of the above | **25** |
| **elsewhere** | **211,425** |

**25 of 211,450 = 0.012%.** Neither code path explains the phenomenon. (Same picture in the
unfiltered view: 749 of 297,406.) On the months that *are* clean the same two paths account
for 100% of the handful of pairs — e.g. ZC 2025-01 full view: 20 pairs, 20 of them day-last.

### The actual mechanism, measured

`process_mbo.py` L583-590 assembles the month file:

```
L584          snap_files = sorted(tmp_dir.glob("snap_*.parquet"))
L587          snap_tables = [pq.read_table(str(f)) for f in snap_files]
L588          master_snap = pa.concat_tables(snap_tables)
L590          pq.write_table(master_snap, str(snap_path))
```

A plain concatenation in **filename order**, with **no global sort and no de-duplication**. The
month parquet therefore preserves per-day-file blocks in its native row order, and decomposes
into monotone runs. Measuring those runs (`block_overlap.csv`):

| file | native blocks | overlapping consecutive block pairs | max rows sharing one exact ns | filtered rows | distinct seconds | excess |
|---|---|---|---|---|---|---|
| ZC 2025-01 v3 (fixture) | **1** | 0 | 2 | 338,159 | 338,159 | **0** |
| ZC 2025-08 v3 (fixture) | **17** | 16 | 5 | 554,304 | 342,854 | **211,450** |

ZC 2025-08's 17 blocks have heavily overlapping wall-clock spans — each per-day reconstruction
starts back at the preceding weekend and runs forward:

```
blk  0 n= 144264  2025-07-27 12:00:06 -> 2025-08-04 18:19:59
blk  1 n=  73473  2025-08-03 14:15:20 -> 2025-08-05 18:19:59
blk  2 n=  76833  2025-08-03 14:15:20 -> 2025-08-06 18:19:59
blk  3 n=  86609  2025-08-03 14:15:20 -> 2025-08-07 18:19:59
blk  4 n= 153931  2025-08-03 14:15:20 -> 2025-08-11 18:19:59
blk  5 n=  73836  2025-08-10 12:00:07 -> 2025-08-12 18:19:59
   ... 11 more, same Sunday-anchored pattern ...
```

so the same wall-clock second is reconstructed up to **5 times** (max multiplicity 5; 64,073
distinct ns timestamps carried by more than one row). ZC 2025-01 is a single monotone block —
the per-day chunks were disjoint and increasing, so the concat came out globally sorted with
exactly one row per second. (True of ZC 2025-01 specifically — `filtered_max_rows_per_second` = 1,
excess 0. It does not generalise: ZC 2025-01 is one of only 7 of the 30 single-block v3 files at
zero excess. See the corrected 30-file list below.)

The per-date view makes the trading-calendar signature explicit. **Fridays are clean, Mon–Thu
are multiply covered:**

```
date         dow     rows span_start  span_end  phases  rows_in_[14,19)
2025-08-01   Fri    59991  00:00:00  18:19:59      40           15601
2025-08-04   Mon    89997  00:00:00  23:59:59     322           34288
2025-08-05   Tue    84821  00:00:00  23:59:59     318           29589
2025-08-08   Fri    59988  00:00:00  18:19:59      43           15601
2025-08-15   Fri    61389  00:00:00  18:19:59      28           15601
2025-08-22   Fri    59959  00:00:00  18:19:59      44           15601
2025-08-29   Fri    61476  00:00:00  18:19:59      26           15601
```

15,601 = 14:00:00 → 18:20:00 inclusive at 1 Hz — the exact single-coverage count for the ZC
CDT day session inside `[14,19)`. All five Fridays hit 15,601 exactly; the sixteen full Mon–Thu
sessions carry 21,428–44,220, i.e. **1.37x–2.83x** single coverage. Fridays are the days with no
following overnight session, so no subsequent chunk reaches back over them.
Distinct sub-second phases per date: 26–44 on Fridays vs 216–393 Mon–Thu (one phase per
re-anchored reconstruction pass).

### The correlation is perfect across all 84 measured files, zero exceptions

`native_blocks == 1 AND overlapping_block_pairs == 0` ⟺ `filtered_excess_rows <= 17`
(and those residual few are exactly the day-edge/gap-re-anchor rows). `native_blocks > 1`
⟺ excess in the tens of thousands. Which fixture-path files are affected:

- **multi-block / overlapping:** cl (all 6 months), gc (all 6), zc (2025-08, -09, -10),
  zs (2025-08, -09, -10) — 18 of 48.
- **single block, non-overlapping:** es, he, le, nq (all 6 months each), zc (2025-01, -11, -12),
  zs (2025-01, -11, -12) — 30 of 48. **PRECISION FIX (applied 2026-08-12, item Y4): these 30 are
  single-block, which is NOT the same as "clean". Only 7 of the 30 carry ZERO filtered excess
  rows** (he 2025-11, le 2025-11, zc 2025-01, zc 2025-11, zs 2025-01, zs 2025-11, zs 2025-12);
  **the other 23 carry 1-17 filtered excess rows**, with at most **2 rows sharing any one second**
  (`filtered_max_rows_per_second` = 2 on all 23; the maximum excess is 17, at he 2025-10). That is
  the same `<= 17` bound already stated immediately above, and it matches the phrasing the
  declaration's §2/§3 now use. This is a precision fix to a factual statement — the word "clean"
  conflated "single block" with "exactly one row per second" — and it changes no measurement:
  every number here is read from `block_overlap.csv` as originally written, and neither the 18/30
  split nor the v3-vs-v4 contrast is affected.
- **every v4 file (36 of 36) is single-block** (`native_blocks == 1`,
  `overlapping_block_pairs == 0`). **PRECISION FIX (applied 2026-08-12, item X3): the exact
  1 Hz grid totals (378,000 / 680,400 / 604,800 / 324,000 / ...) are DISTINCT-SECOND counts
  (`filtered_distinct_seconds`), not row counts (`filtered_rows`).** The two coincide in only
  12 of the 36 files; the other **24 carry 1-5 filtered excess rows**, with at most **2 rows
  sharing any one second** (`filtered_max_rows_per_second` = 2 on all 24). Example: zc
  2025-01 v4 = 378,000 rows / 378,000 distinct seconds (excess 0), zc 2025-08 v4 = 366,005
  rows / **366,000** distinct seconds (excess 5). This is a precision fix to a factual
  statement — the wording above conflated rows with seconds — and it changes no measurement:
  every number here is read from `block_overlap.csv` as originally written, and the v3-vs-v4
  contrast (v3 excess up to 211,450 rows, 5 rows on one exact nanosecond) is unaffected.

So the ZC 2025-01-vs-2025-08 contrast is not a DST artefact and not a code-path artefact: it is
**overlapping multi-day reconstruction passes concatenated without sort or de-duplication**,
present in 2025-08/09/10 for ZC and ZS and absent in 2025-01/11/12.

Incidental observation, recorded raw, not interpreted here: the ZC 2025-08 fixture rows sampled
at 2025-08-04 14:00:00–14:00:07 carry `bid_price_1 = 412.0` above `ask_price_1 = 409.5`
(crossed book). `MASTER_FINDINGS/v4/G2_G3_summary.txt` records the v4 gap-fill reprocessing as
taking the ZC afternoon negative-spread fraction from 65.81% to 2.13%.

---

## (d) THE 338,159-vs-378,000 AMBIGUITY — RESOLVED

Both numbers are ZC 2025-01 under the `[14,19)` UTC hour filter. They are two different
generations of the snapshot file:

| | rows under `[14,19)` | total rows | size | generation |
|---|---|---|---|---|
| `processed/zc/zc_snapshots_2025-01.parquet` | **338,159** | 1,262,191 | 15,919,599 | v3_pre_gapfill |
| `processed/zc/v4_gapfill/zc_snapshots_2025-01.parquet` | **378,000** | 1,346,274 | 18,328,075 | v4_gapfill |

- **338,159** — sha256 `46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46`,
  md5 `ea2eee6136896b5f8a5b7ddc052f589c`. Not covered by any manifest at this path; the
  byte-identical copy at `pc2_transfer/transfer/data/zc/zc_snapshots_2025-01.parquet` is
  covered by `pc2_transfer/transfer/checksums.txt` line 49, MATCH.
- **378,000** — sha256 `0c0cb4ad2dfb19be057e6be611d92ff09d06f33de613bf0041b7e5ff22b5012f`,
  md5 `900b30a0b7d5cb890329dac5329b0890`, covered by `PC2_TRANSFER_v4/manifest.csv` line 200,
  MATCH. 378,000 = 21 trading days x 5 h x 3600 s — a complete, gap-filled 1 Hz grid.

**338,159 is the number the fixture, the builder, and the M5/N1 sweep actually see.** 378,000
belongs to the generation the archive's own hand-off package calls canonical and which the
fixture path does not read.

### Citation phrasing for the declaration

Whenever the ZC 2025-01 lattice row count appears:

> ZC 2025-01 lattice = 338,159 rows, being
> `processed/zc/zc_snapshots_2025-01.parquet` filtered to UTC hours [14, 19) —
> generation **v3 pre-gapfill**, sha256 `46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46`
> (md5 `ea2eee6136896b5f8a5b7ddc052f589c`).
> This is **not** the v4 gap-filled generation, which for the same instrument-month is
> `processed/zc/v4_gapfill/zc_snapshots_2025-01.parquet`, sha256
> `0c0cb4ad2dfb19be057e6be611d92ff09d06f33de613bf0041b7e5ff22b5012f`
> (md5 `900b30a0b7d5cb890329dac5329b0890`, `PC2_TRANSFER_v4/manifest.csv` line 200) and yields
> 378,000 rows under the same filter.

The generic form, for any instrument-month: name the count, the path, the generation
(`v3_pre_gapfill` / `v4_gapfill` / `v4_morning_chunk`), and the sha256 — all four are in
`lattice_provenance.csv`, keyed by `instrument`, `month`, `is_fixture_path`.

---

## (e) MIXED-GENERATION CHECK — YES, the fixture window mixes generations, by instrument

The fixture path holds **v3_pre_gapfill for all 8 instruments in all 6 months** — it is
generation-stable *across months*. The mixing is *across instruments*, in what that generation
means relative to the archive's canonical set:

| instruments | months | fixture-path generation | is a v4 generation available? | manifest coverage of the fixture file |
|---|---|---|---|---|
| **he, le** | all 6 | v3_pre_gapfill | **No** — only one generation exists on disk | **COVERED, MATCH** (`PC2_TRANSFER_v4/manifest.csv` L128–139, L152–163) |
| cl, es, gc, nq, zc, zs | all 6 | v3_pre_gapfill | **Yes**, and it is the canonical one | **NOT COVERED by any manifest** |

For he and le the fixture file *is* the canonical v4-package file — `PC2_SETUP_README.txt`
(archive, verbatim):

```
  he/                           24 files (v3 canonical; no reprocessing)
  le/                           24 files (v3 canonical; no reprocessing)
```

For the other six the fixture file is the superseded pre-gapfill generation.
`MASTER_FINDINGS/v4/G2_G3_summary.txt` records the reprocessing that produced the replacement:

```
- G2: 72/72 (instrument, month) cells reprocessed successfully
      (NQ + ZS + ZC + ES + CL + GC, each 12 months)
```

and `PC2_SETUP_README.txt` describes the package as containing "the canonical v4 processed
parquets". So: **for 6 of 8 fixture instruments the lattice is the generation the archive itself
superseded; for 2 of 8 (he, le) it is the canonical generation.** That is a declaration fact.

Two further declaration facts from the same table:

1. **36 of the 48 fixture-path files are covered by no manifest in the archive** — their
   integrity is attested only by the sha256/md5 recorded in `lattice_provenance.csv`. (For
   gc, nq, zc, zs a byte-identical copy is manifest-covered under `transfer/data/`, so those 24
   are transitively attested; for cl and es no manifest covers the v3 generation at all.)
2. **The v3 fixture lattice is not a 1 Hz lattice for 18 of 48 instrument-months** (cl x6,
   gc x6, zc x3, zs x3): it carries up to 5 rows per wall-clock second from overlapping
   reconstruction passes. **PRECISION FIX (applied 2026-08-12, item Y4): the other 30 v3 files and
   all 36 v4 files are single-block, but single-block does not mean exact 1 Hz.** Of the 30 v3
   single-block files only **7** carry zero filtered excess rows and **23 carry 1-17**; of the 36
   v4 files only **12** carry zero and **24 carry 1-5** (both per (c) above). In both of those sets
   the residual excess is bounded at **2 rows per second**, against up to **5** in the 18
   multi-block v3 files — which is the contrast this bullet rests on, and it is unchanged. Same
   conflation as (c), same correction: no measurement, count, or conclusion changes.

---

## STOP-AND-REPORT

`stop_and_report = false`. No contradiction was found between anything measured here and the
ESTABLISHED facts or the M5 prior result: ZC 2025-08 lattice = 554,304 rows → 554,303 corrected
rows, exactly as M5 recorded; ZC 2025-01 = 338,159, exactly as M1 recorded. Everything above is
a *resolution* of the stated ambiguity, not a conflict with a prior measurement.
