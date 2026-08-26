# ITEM X4 — NQ MBO CROSS-GENERATION JOIN: SOUNDNESS CHARACTERISATION

**Working resolution R12: this is NOT gate-scored.** It exists so the information exists. Nothing
below is acceptance evidence and nothing below is authorised to enter the acceptance denominator.

Scripts: `x4_nq_mbo_diagnostic.py` (the sweep), `summarize.py` (this characterisation),
`probe.py` (schema/tz/timing probe). Full captured output: `summarize_output.txt`, `run_full.log`,
`run_logs.json`. Runtime 170.7 s for six months x two event generations (~90 GB of parquet read,
three columns each).

---

## 0. WHAT IS BEING JOINED, AND WHY THIS ITEM EXISTS

N1 could not score NQ's six MBO classes because the fixture path
`processed\nq\nq_mbo_{month}.parquet` does not exist (N1 `unscored_ledger.csv`, 6 rows x 12 cells
= 72 unscored cells). X4 substitutes an event source.

**Lattice (unchanged, both joins):** `processed\nq\nq_snapshots_{month}.parquet`, generation
**v3_pre_gapfill** (n2 `provenance_notes.md` family A), filtered to UTC hours **[14, 22)** from
`scripts\phase5\phase5_ml.py` L48-49, verbatim:

```
INST_META = {
    "es": {"tick_size": 0.25, "matching": "FIFO", "day_start_utc": 14, "day_end_utc": 22, "ct_ratio": 3.26},
    "nq": {"tick_size": 0.25, "matching": "FIFO", "day_start_utc": 14, "day_end_utc": 22, "ct_ratio": 7.84},
```

**Event source V4 (mandated by X4):**
`processed\nq\v4_gapfill\nq_mbo_{month}\nq_mbo_YYYYMMDD.parquet`, per-day files enumerated and
concatenated. Generation **v4_gapfill**. This is the cross-generation join.

**Event source V3 (found by exhaustive search — see (b)):**
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`, month files. Generation **v3_pre_gapfill**.
This is a *same*-generation join and is reported alongside as the control.

Column names verified against the builder's MBO aggregation
(`f2\phase5_ml_fixture.py` = `phase5_ml.py` L118-150, verbatim):

```
    if n_rows > 50_000_000:
        for batch in pf.iter_batches(batch_size=10_000_000, columns=["ts_event", "action", "side"]):
            ts  = batch.column("ts_event").cast('int64').to_numpy()
            act = batch.column("action").to_numpy(zero_copy_only=False).astype('U1')
            sid = batch.column("side").to_numpy(zero_copy_only=False).astype('U1')
            ts_floor = (ts // 1_000_000_000) * 1_000_000_000
            is_bid = (sid == 'B'); is_add = (act == 'A'); is_cancel = (act == 'C')
        ...
        result["total_events"] = result["bid_adds"] + result["ask_adds"] \
                               + result["bid_cancels"] + result["ask_cancels"]
```

Event time column = `ts_event` (Arrow `timestamp[ns, tz=UTC]` in both generations, schemas
byte-for-byte identical field lists); action/side = `action` / `side`, `large_string`. Observed
`action` values on NQ: `A, C, M, F, T`; `side`: `A, B`. Both sources exceed the
50,000,000-row threshold in every month, so **both take the LARGE builder path**, and
`mbo_all = action in {A, C}` for both. The 11th diagnostic class `mbo_all_rows` (= every MBO row,
the SMALL-path definition) is carried exactly as N1/M5 carry it on LARGE-path cells.

---

## (a) DAY COVERAGE — the v4 MBO per-day files DO NOT cover the same trading days as the v3 lattice

`soundness_a_day_coverage.csv`, `per_day_coverage.csv`.

| month | lattice dates | v4 day files | in both | lattice-only | v4-only | lattice rows | lattice rows on uncovered dates | % |
|---|---|---|---|---|---|---|---|---|
| 2025-01 | 24 | 21 | 21 | **3** | 0 | 598,228 | 20,421 | 3.414% |
| 2025-08 | 30 | 21 | 21 | **9** | 0 | 540,531 | 6,127 | 1.134% |
| 2025-09 | 27 | 21 | 21 | **6** | 0 | 549,431 | 15,467 | 2.815% |
| 2025-10 | 30 | 23 | 23 | **7** | 0 | 590,786 | 4,276 | 0.724% |
| 2025-11 | 20 | 18 | 18 | **2** | 0 | 550,464 | 32,061 | 5.824% |
| 2025-12 | 23 | 22 | 22 | **1** | 0 | 620,108 | 1 | 0.000% |
| **total** | 154 | 126 | 126 | **28** | **0** | 3,449,548 | **78,353** | **2.272%** |

**The v4 day set is a strict subset of the lattice day set — 126 of 154. There is no date the
v4 source covers and the lattice does not.** The 28 lattice-only dates, with the lattice rows and
the v3 in-window event count each carries:

| month | date | dow | lattice rows | v3 events in window | character |
|---|---|---|---|---|---|
| 2025-01 | 2024-12-30 | Mon | 423 | 153 | prior-month spillover |
| 2025-01 | 2024-12-31 | Tue | 2,197 | 371 | prior-month spillover |
| 2025-01 | **2025-01-20** | Mon | **17,801** | **2,279,312** | **MLK — full session, absent from v4** |
| 2025-08 | 2025-07-27..31 | Sun-Thu | 2 / 8 / 4 / 193 / 3,769 | 1 / 4 / 2 / 44 / 499 | prior-month spillover |
| 2025-08 | 08-03, -10, -17, -24 | Sun | 870 / 549 / 391 / 341 | 2,591 / 256 / 126 / 140 | Sunday-evening reopen |
| 2025-09 | 2025-08-31 | Sun | 171 | 140 | Sunday-evening reopen |
| 2025-09 | **2025-09-01** | Mon | **13,586** | **274,740** | **Labor Day — absent from v4** |
| 2025-09 | 09-07, -14, -21, -28 | Sun | 378 / 230 / 598 / 504 | 227 / 126 / 436 / 305 | Sunday-evening reopen |
| 2025-10 | 09-28, -29, -30 | Sun-Tue | 9 / 245 / 1,578 | 20 / 70 / 381 | prior-month spillover |
| 2025-10 | 10-05, -12, -19, -26 | Sun | 660 / 529 / 539 / 716 | 336 / 329 / 426 / 335 | Sunday-evening reopen |
| 2025-11 | **2025-11-27** | Thu | **16,760** | **465,145** | **Thanksgiving — absent from v4** |
| 2025-11 | **2025-11-28** | Fri | **15,301** | **3,455,358** | **day after Thanksgiving — absent from v4** |
| 2025-12 | 2025-12-14 | Sun | 1 | 1,172 | Sunday-evening reopen |

Four of the 28 are **material**: 2025-01-20, 2025-09-01, 2025-11-27, 2025-11-28 are real sessions
carrying 13,586–17,801 lattice rows each and hundreds of thousands to millions of v3 MBO events —
63,448 of the 78,353 uncovered lattice rows (81%). The other 24 are thin spillover / Sunday-evening
fringes (1–3,769 rows).

**This is an intrinsic, self-consistent property of the v4 generation, not a transfer defect.**
The v4 generation's *own* lattice has exactly the same day set as its MBO day files:

| month | v3 snapshot dates | v4 snapshot dates | v4 MBO day files |
|---|---|---|---|
| 2025-01 | 24 (incl. 2024-12-30/31, 01-20) | **21** (no 2024-12-30/31, no 01-20) | **21** |
| 2025-09 | 27 | **21** | **21** |
| 2025-11 | 20 (incl. 11-27, 11-28) | **18** (no 11-27, 11-28) | **18** |

v4 2025-11 = 518,400 rows = 18 x 8 h x 3600 s exactly; v4 2025-01 = 604,800 = 21 x 8 x 3600
exactly. The v4 generation dropped the spillover, Sunday-evening and US-holiday sessions and
gap-filled the remainder to a complete 1 Hz grid. **X4's join imports the v4 day set into a v3
denominator**: 2.272% of the v3 lattice rows have no v4 event data of any kind behind them.

---

## (b) EVENT COUNTS IN THE JOINED WINDOW, AND THE v3 SOURCE THAT DOES EXIST

### A v3-generation NQ MBO source EXISTS

Exhaustive `os.walk` of the whole archive root (26,596 files) for `nq*mbo*.parquet` returns
**exactly 262 files in exactly two families**:

| family | path | files | generation | evidence |
|---|---|---|---|---|
| **V4** | `processed\nq\v4_gapfill\nq_mbo_{month}\nq_mbo_YYYYMMDD.parquet` | 250 (12 months) | v4_gapfill | sibling of the v4 snapshots; mtime 2026-04-16 |
| **V3** | `pc2_transfer\processed\nq\nq_mbo_{month}.parquet` | 12 | **v3_pre_gapfill** | see below |

Nothing under `USB_ALL_PHASES`, `PC2_TRANSFER_v4`, `v4`, `v5`, `transfer` or `MASTER_FINDINGS`.
`PC2_TRANSFER_v4\processed\nq\` holds only `v4_gapfill\` (snapshots + trades, no MBO).
No MBO file of either generation is covered by `PC2_TRANSFER_v4\manifest.csv` or by either
`checksums.txt` — the MBO layer is unattested in every manifest in the archive.

The V3 family's generation is established two ways:
1. **Directory family.** `pc2_transfer\processed\{inst}\` is family **E** of n2
   `provenance_notes.md`, identified there as **v3_pre_gapfill**. Verified here for NQ directly:
   `pc2_transfer\processed\nq\nq_snapshots_2025-08.parquet` and
   `processed\nq\nq_snapshots_2025-08.parquet` have the same sha256
   `1A200A3A71A597C84E869D0CE647195B86250C0D28E3D0C813A3AAF40F1304D7` — the pc2_transfer copy of
   the NQ tree *is* the fixture-path generation, and it carries the MBO month files that
   `processed\nq\` lacks. `pc2_transfer` is a real directory, not a junction (`LinkType` empty).
2. **Build timestamps.** The V3 MBO month files are stamped 2026-03-31 / 2026-04-01, interleaved
   with the v3 snapshots (2026-04-01/02) and trades (2026-03-31/04-01). Every v4 artefact is
   stamped 2026-04-16.

**So the answer to "is there a v3-generation NQ MBO source anywhere in the archive" is YES**, and
it is at the same row scale (e.g. 2025-08: v3 254,599,115 rows vs v4 253,568,875).

### Event counts and the v3-vs-v4 delta

`soundness_b_event_counts.csv`. "Joined window" = UTC hours [14,22) on the 126 dates present in
**both** the lattice and the v4 day set.

| month | joined days | v4 events | v3 events | v4 − v3 | % | v3 events on v4-uncovered dates | v4 file rows (month) | v3 file rows (month) |
|---|---|---|---|---|---|---|---|---|
| 2025-01 | 21 | 296,599,309 | 296,046,315 | +552,994 | +0.187% | 2,279,836 | 369,506,687 | 374,834,326 |
| 2025-08 | 21 | 176,197,675 | 175,873,836 | +323,839 | +0.184% | 3,663 | 253,568,875 | 254,599,115 |
| 2025-09 | 21 | 180,287,632 | 180,021,133 | +266,499 | +0.148% | 275,974 | 256,260,278 | 258,593,765 |
| 2025-10 | 23 | 272,111,252 | 271,641,366 | +469,886 | +0.173% | 1,897 | 392,808,280 | 394,256,908 |
| 2025-11 | 18 | 379,399,535 | 378,778,023 | +621,512 | +0.164% | 3,920,503 | 469,430,529 | 475,240,551 |
| 2025-12 | 22 | 301,515,128 | 301,144,274 | +370,854 | +0.123% | 1,172 | 362,632,882 | 363,311,850 |

**Inside the shared days the two generations are nearly the same event stream.** Per-day
v4 − v3 over all 126 joined days: min +518, median +17,591, max +75,931; as a percentage
min +0.066%, median +0.154%, max +0.307%, **never negative**. The v4 generation adds ~0.15% more
events in-window on every single covered day — consistent with gap-fill adding, not replacing.

The whole-month file row counts run the other way (v3 files are 0.2–1.4% larger) because the v3
month files also carry the uncovered dates and the out-of-window hours.

---

## (c) PER-DAY TIMESTAMP-RANGE ALIGNMENT ON THE COVERED DAYS — essentially exact

Over all 126 joined days, comparing the lattice's first/last row inside [14,22) with the v4 MBO
stream's first/last event inside [14,22):

- **Session start: 126 of 126 days agree to the minute — both at 14:00.** No exceptions.
- **Session end: 105 of 126 agree to the minute.** The 21 that differ:
  - 14 days: lattice ends `20:59:59.9x`, v4 ends `21:00:00.068` — Fridays / early closes; a
    **0.07-second** overshoot of the lattice's last row by the last in-window MBO event.
  - 6 days (2025-09-24, -25, 2025-10-16, -20, -22, -28): lattice ends 21:55–21:58, v4 ends
    21:59:59.9 — the lattice's last snapshot precedes the true 22:00 close by 1–4 minutes; v4 runs
    to the close. The v3 MBO source ends at the same 21:55–21:58 point as the lattice on exactly
    these days, so this is a v3-lattice truncation, not a v4 excess.
  - 1 day (2025-09-30): lattice and v3 end 20:59:59.99, v4 ends 21:59:59.96 — an hour of v4 events
    beyond the v3 lattice's last row.
- No day has the v4 stream *ending before* the lattice, and no day has a mid-session hole: every
  joined day carries 2.2 M – 33 M v4 in-window events against 23 k – 25 k lattice rows.

---

## VERDICT: SOUND ENOUGH TO REPORT, WITH ONE NAMED CAVEAT — and the caveat is measurable

The generational difference is **not** a different event set on the days both sources have. It is
**a smaller day set**. Two independent checks:

**Check 1 — restrict both joins to the 126 v4-covered days** (`restricted_to_v4_covered_days_*.csv`).
Same lattice rows, same window, both event generations:

| | max abs strict delta (v4 − v3) | max abs equal delta |
|---|---|---|
| full lattice denominator | **27,194** | **217** |
| restricted to v4-covered days | **745** | **1** |

The cross-generation deficit collapses by 36x once the day hole is removed; the residual 745 (on
`mbo_all_rows`, 2025-08, contaminated, 525,159 rows) is **0.14%** — the same order as the +0.15%
event-count delta in (b), i.e. it is gap-fill, not a structural mismatch. The 2025-11 delta, the
worst at −27,194, is entirely the two Thanksgiving sessions.

**Check 2 — the corrected side is 0 under both generations, restricted or not.** Every corrected
strict count is 0 in all six months, all seven classes, for the v4 join, the v3 join, and both
restricted joins. The day hole cannot be hiding a corrected-side violation, because the
same-generation source that *does* cover those days also reports 0.

**The caveat that must travel with every V4 number:**

> The V4 join's denominator is the full v3 lattice, but 2.272% of those rows (78,353 of
> 3,449,548; 5.824% in 2025-11 alone) fall on 28 dates for which the v4 source holds no events at
> all — including four real sessions (MLK 2025-01-20, Labor Day 2025-09-01, Thanksgiving
> 2025-11-27 and 2025-11-28). Those rows are scored as non-violating by construction, so every V4
> **contaminated** strict count is a **lower bound**, understated by up to 5% of the denominator.
> The V4 **corrected** counts are unaffected in value (0 either way).

For that reason the same-generation V3 map (`nq_mbo_v3_same_generation_map.csv`) is the sounder of
the two and is reported alongside. It is not the source X4 named, and it is equally non-gated.

---

## RESULTS — decision_T boundary, all six MBO classes + the 11th diagnostic class

### V4 join (the X4 deliverable — `nq_mbo_diagnostic.csv`)

**corrected side: strict = 0 in every cell.**

| class | 2025-01 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 |
|---|---|---|---|---|---|---|
| mbo_all | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_bid_add | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_ask_add | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_bid_cancel | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_ask_cancel | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_cancel_any | 0 | 0 | 0 | 0 | 0 | 0 |
| mbo_all_rows | 0 | 0 | 0 | 0 | 0 | 0 |
| *corrected rows* | 598,227 | 540,530 | 549,430 | 590,785 | 550,463 | 620,107 |

corrected equal (fires only where floor(T_i) == floor(T_{i-1})):

| class | 2025-01 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 |
|---|---|---|---|---|---|---|
| mbo_all | 5 | 5 | 5 | 5 | 3 | 5 |
| mbo_bid_add | 0 | 0 | 0 | 1 | 0 | 2 |
| mbo_ask_add | 1 | 0 | 1 | 1 | 2 | 0 |
| mbo_bid_cancel | 1 | 4 | 3 | 2 | 0 | 2 |
| mbo_ask_cancel | 3 | 1 | 1 | 1 | 1 | 2 |
| mbo_cancel_any | 4 | 5 | 4 | 3 | 1 | 3 |
| mbo_all_rows | 5 | 5 | 5 | 5 | 3 | 6 |

The lattice's own same-second row count is 6 / 7 / 5 / 5 / 3 / 6 — the equal counts are bounded by
it and nearly saturate it.

**contaminated side: strict** (and, in brackets, as a % of the full-lattice denominator)

| class | 2025-01 | 2025-08 | 2025-09 | 2025-10 | 2025-11 | 2025-12 |
|---|---|---|---|---|---|---|
| mbo_all | 573,849 (95.92) | 524,025 (96.95) | 523,307 (95.25) | 576,402 (97.57) | 516,516 (93.83) | 614,563 (99.11) |
| mbo_bid_add | 566,294 (94.66) | 513,246 (94.95) | 512,737 (93.32) | 567,634 (96.08) | 511,979 (93.01) | 605,001 (97.56) |
| mbo_ask_add | 566,209 (94.65) | 513,303 (94.96) | 512,597 (93.30) | 567,767 (96.10) | 512,042 (93.02) | 605,213 (97.60) |
| mbo_bid_cancel | 565,958 (94.61) | 514,325 (95.15) | 513,551 (93.47) | 568,799 (96.28) | 512,735 (93.15) | 606,399 (97.79) |
| mbo_ask_cancel | 566,085 (94.63) | 514,089 (95.11) | 513,283 (93.42) | 568,652 (96.25) | 512,849 (93.17) | 606,587 (97.82) |
| mbo_cancel_any | 570,947 (95.44) | 520,516 (96.30) | 519,646 (94.58) | 573,725 (97.11) | 515,516 (93.65) | 612,434 (98.76) |
| mbo_all_rows | 574,626 (96.05) | 525,159 (97.16) | 524,469 (95.46) | 577,120 (97.69) | 516,909 (93.90) | 615,494 (99.26) |
| *contaminated rows* | 598,228 | 540,531 | 549,431 | 590,786 | 550,464 | 620,108 |

On the restricted (v4-covered-days) denominator the same strict counts give 96.0–99.7%, i.e. the
sub-94% cells above are the day-hole artefact, not a lower contamination rate.

contaminated equal: mbo_all = 5 / 94 / 90 / 102 / 3 / 5.

### V3 join, same lattice, same generation (`nq_mbo_v3_same_generation_map.csv`)

**corrected side: strict = 0 in every cell** (identical to V4). corrected equal:
mbo_all = 6 / 7 / 5 / 5 / 3 / 5, mbo_all_rows = 6 / 7 / 5 / 5 / 3 / 6.

contaminated strict, mbo_all: 588,354 (98.35%) / 523,573 (96.86) / 532,341 (96.89) /
576,194 (97.53) / 543,253 (98.69) / 614,564 (99.11). Per-class rates 94.6–99.3%.

---

## WHAT THIS DIAGNOSTIC DOES AND DOES NOT LICENSE

**Does:**
- It states that for NQ, under both available MBO generations, on all six fixture months, all six
  declared MBO classes plus the diagnostic 11th, at boundary decision_T, the **corrected side
  produces zero strict availability violations**, and the equal counts are 0–7, bounded by the
  lattice's 3–7 same-second rows per month.
- It states that the **contaminated side produces 93.0–99.3% strict violation rates** on the same
  cells — i.e. NQ behaves like the instruments N1 could score.
- It records that a **v3-generation NQ MBO source exists** at
  `pc2_transfer\processed\nq\nq_mbo_{month}.parquet`, byte-verified as the same tree family as the
  fixture-path v3 snapshots, which N1 did not have and which makes a same-generation NQ join
  possible at all.
- It quantifies the v3/v4 generational difference: same event stream to +0.15%, different day set
  by 28 dates / 2.272% of lattice rows.

**Does NOT:**
- **It is not gate evidence.** R12 places X4 outside the gate. No cell here is scored, and the
  kill-gate is neither triggered nor exonerated by anything above.
- **It does not convert N1's 72 unscored NQ MBO cells into scored cells.** Those cells are unscored
  because the *fixture path* has no MBO file; X4 read a different path, on one join a different
  generation. Moving these numbers into the acceptance denominator would change what the
  denominator is measured on and is therefore a **class C amendment** — it is not authorised by
  this item and has not been performed. The N1 `unscored_ledger.csv` is unchanged.
- **It does not license the V3 map as a drop-in either.** `pc2_transfer\processed\nq\` is not the
  path `phase5_ml.py` reads (`get_data_dir` -> `PROC / sym` -> `processed\nq\`), it is covered by
  no manifest, and using it would be the same class C amendment.
- **It does not re-open A1 or the Mechanism-1 finding.** No artifact outside this directory was
  read for writing, adjusted, or re-derived. Nothing here was tuned toward a decision (R13).
