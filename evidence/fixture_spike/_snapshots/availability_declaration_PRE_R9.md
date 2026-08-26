# AvailabilityModel declaration — fixture reconstruction

## DRAFT — AUTHOR REVIEW REQUIRED

Status: DRAFT. Nothing in this file is a registered declaration. Every element below is a
reconstruction from archive evidence, assembled by item F4 of "Phase 0 addendum 2: fixture
verification for v30a". Elements marked AMBIGUOUS-PENDING-AUTHOR are genuinely ambiguous on
the evidence and are NOT resolved here.

Assembly status (item D1, "Phase 0 addendum 3: pre-amendment closure checks", 2026-08-11):
this file is now the complete v30a declaration DRAFT. Part I (sections 1-7 and the
evidence-class table) is the original F4 reconstruction, unchanged. Part II (inserted after
the evidence-class table) assembles the v30a declaration under working resolutions R1-R5,
recorded verbatim at the file tail. Where Part II states a working resolution for something
Part I left AMBIGUOUS-PENDING-AUTHOR or stated as the operative contract (ties in Part I
section 6; the t-1 boundary wording in Part I section 1), Part II carries the draft
declaration and Part I stands as the measurement record. The Phase-7-added-columns block
(T2) and the working-resolution record at the file tail (now R1-R9) are frozen
byte-identical by this item and by every item after it, this one included.

Editor pass (item P2, "v30a availability-declaration draft", 2026-08-12). Three things this
pass changes at the top level, stated here once:

1. **The declared boundary is the measured one.** §1's DECLARED value now states the
   information boundary `floor(t-1) + 1s` as the normative contract. It is stated in §1 and
   nowhere else; §10 is its evidence section. The historical "through time t-1" contract text
   survives only as the quoted claim that measurement violated.
2. **The gate scores against a declared ground-truth map on BOTH sides** (working resolution
   R9, verbatim at the file tail). The corrected side is described throughout as
   **CHARACTERIZED, never clean**. §13 is that map; §C enumerates it side-relatively; §A walks
   PREREG.md §6.2 element by element and marks each SATISFIED or AMENDED.
3. **weighted_mid FLAVOR is RESOLVED** — `contemporaneous_state_flow`, by working resolution
   R6, PROVISIONAL until the prereg-v30a tag is signed. R5's pending status is superseded. The
   frozen T2 addendum block still reads AMBIGUOUS-PENDING-AUTHOR because it is the measurement
   record and is not edited; R6 governs, and the note immediately following that block records
   the supersession.

**Numbering convention adopted by this pass:** new Part II sections are letter-numbered
(**§A - §F**); the pre-existing numeric sections 8-18 are **not** renumbered, so every
cross-reference written before this pass stays valid. New primary sources for this pass are
the N1 declared map (`n1\`), the N3 cohort predicate (`n3\`), and the N2 lattice-provenance
round (`n2\`); the M5 falsification sweep (`m5\`) is cited as the measurement that forced R9.

Schema source (normative, read-only): PREREG.md §2.3 (`AvailabilityModel` table, lines
199-212), §2.4 (`label_availability`, lines 218-225), comparator table lines 190-193, at
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`.

Fixture: Phase 5/7 ZC pipeline, archive `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only).
Pre-fix side = `pc2_transfer\scripts\phase5\phase5_ml.py` `build_features_month()` (lines
174-298, no shift(1) anywhere in phase5 — established in prior spike). Post-fix side =
`results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py` line 276
`snap[feature_cols] = snap[feature_cols].shift(1)`.

---

## 1. `decision_time`

Registered vocabulary (PREREG.md line 203): "how *d(i)* derives from row *i* — bar open, bar
close, offset, or a column".

**DECLARED value: a column — `d(i)` = the row's `timestamp` column value `t`, an instant on
the 1-second snapshot lattice.**

**DECLARED availability contract at that decision instant — THE SINGLE NORMATIVE STATEMENT OF
THE BOUNDARY IN THIS FILE:**

> The decision for row `t` admits information through **`floor(t-1) + 1s`** — the end of the
> wall-clock second joined to the previous lattice row. Not "through snapshot `t-1`", and not
> "through time `t-1`".

This is the MEASURED boundary of the corrected (post-fix) features, and the declaration states
the measured boundary rather than the intended one. The corrected row stamped `t` carries the
previous row's construction, and that construction's trade/MBO aggregates cover the whole
wall-clock second `[floor(t-1), floor(t-1)+1s)`; because lattice stamps are generally off
wall-clock boundaries (§2), that window's end can lie strictly after `t-1`. §10 is the
EVIDENCE section for this statement and restates nothing: it carries the measurement, the
magnitudes, and the cross-checks. No other section in this file states the boundary rule.

Evidence for the declared value:
- The measurement: §10 (T1 `t1\violation_table.csv`, `corrected` / `claimed_T_prev` rows;
  C4 `c4\independent_counts.csv` `prev_row_B` rows). Working resolution R2 (file tail) is the
  authority for stating the measured boundary as the declaration.
- The construction that produces it: `phase7_l2_sim.py` line 276
  `snap[feature_cols] = snap[feature_cols].shift(1)`; line 819 writes
  "lag_fix: universal (all features shift(1))" (established fact, prior spike). The shift is
  POSITIONAL — one lattice row — and the row it reaches back to carries a full wall-clock
  second of trade/MBO aggregate, which is exactly why the boundary is `floor(t-1)+1s` and not
  `t-1`.

**Historical contract text — retained ONLY as the quoted claim that measurement violated, and
retired as a description of anything in this fixture:**
`MASTER_FINDINGS\preregistration_v4.txt` lines 303-304 (verbatim): "Causal lag: Mandatory
shift(1) on all features. Features at time t use information available only through time t-1."
Measured against that claim, the corrected features absorb events strictly after `t-1` on
89,568 of 338,158 rows for trades_all and 254,314 for mbo_all (§10). The claim is quoted; it
is not the declaration.

**Recorded deviation (PRE-FIX fixture side, what actually held — NOT the declaration):**
`pc2_transfer\scripts\phase5\phase5_ml.py` contains no shift(1); features in row `T` are
computed at snapshot `T` itself (e.g. line 193 `snap[f"mid_return_{lag}s"] = mid.pct_change(lag)`
ending at row T; lines 252-258 rolling sums ending at row T; line 258
`snap["vwap_distance"] = (mid - snap["vwap"]) / tick` reading mid[t] and same-second vwap).
The archive's own audit confirms: `scripts\phase5\phase5_audit.py` lines 96-101:
"Q1: At prediction time t, does input include data from second t? ... ANSWER: YES — LEAKAGE
CONFIRMED ... The label predicts direction FROM mid[t]."

## 2. `bar_duration`

Registered vocabulary (PREREG.md line 208): fixed value or inferred; last known duration
carried forward at the final row.

**DECLARED value: fixed, 1 second** — as the EMITTER's interval. Five caveats are part of the
record, and the last four are load-bearing for §13's map:

- `scripts\pipeline\process_mbo.py` line 322: `def reconstruct_day(df, date_str, interval=1.0, levels=5)`;
  line 331 `interval_ns = int(interval * 1e9)`; line 358 `next_snap += np.timedelta64(interval_ns, "ns")`.
- **Anchoring caveat:** line 342 `next_snap = ts_events[0] + np.timedelta64(interval_ns, "ns")`
  — the lattice is anchored to the day's FIRST EVENT, not wall-clock second boundaries. The
  1-s lattice phase therefore differs day to day and is generally off wall-clock boundaries.
- Gap handling: lines 347-352 — gaps > 60 s emit one snapshot then re-anchor (`next_snap = ts`),
  so the lattice can re-phase intra-day. Final snapshot of a day is stamped `ts_events[-1]`
  (line 367), an off-lattice stamp.
- **GENERATION caveat (N2, measured):** the file the fixture actually reads is generation
  **`v3_pre_gapfill`** for **all 48 fixture instrument-months** (8 instruments x 2025-01,
  2025-08..12). `phase5_ml.py` L104-106 `get_data_dir` prefers `C:\MBO_data\{sym}`, which does
  not exist on this machine, so it falls through to `processed\{inst}\{inst}_snapshots_{m}.parquet`
  — the pre-gapfill family. Evidence: `n2\provenance_notes.md` §(a)+(b);
  `n2\lattice_provenance.csv` (228 snapshot copies enumerated by exhaustive `os.walk`, 100%
  accounted for, zero md5 MISMATCH against any manifest that covers them).
- **THE 1 Hz CLAIM IS FALSE FOR 18 OF 48 INSTRUMENT-MONTHS.** "fixed, 1 second" describes the
  *emitter*, not the delivered file. On cl (all 6 months), gc (all 6), zc (2025-08/-09/-10) and
  zs (2025-08/-09/-10) the delivered lattice carries up to **5 rows sharing one exact
  nanosecond timestamp**. The other 30 are single-block and clean. Root cause in §3.
  Evidence: `n2\provenance_notes.md` §(c) and §(e) item 2; `n2\block_overlap.csv`;
  per-instrument-month same-second counts in `n1\lattice_profile.csv`
  (`same_second_rows`, e.g. zc 2025-08 = 211,450 of 554,304; zc 2025-01 = 0 of 338,159).
- **MIXED GENERATION ACROSS INSTRUMENTS (declaration fact).** For **he and le** the fixture-path
  file *is* the archive's canonical v4-package file and is manifest-COVERED, MATCH
  (`PC2_TRANSFER_v4\manifest.csv` L128-139 and L152-163) — only one generation of those two
  exists on disk. For **cl, es, gc, nq, zc, zs** the fixture-path file is the **superseded
  pre-gapfill** generation and is covered by **no manifest at that path**. **36 of the 48
  fixture-path files are manifest-uncovered**; for gc, nq, zc and zs a byte-identical copy under
  `transfer\data\` is covered by `checksums.txt` (transitively attested, 24 files), and for cl
  and es no manifest covers the v3 generation at all. Evidence:
  `n2\provenance_notes.md` §(e) and its table; `n2\lattice_provenance.csv`.
- **Generation-naming rule (M1/N2), binding on every row count in this file:** whenever a
  lattice row count appears, name the count, the path, the generation and the sha256. ZC
  2025-01 = **338,159 rows** is
  `processed\zc\zc_snapshots_2025-01.parquet` filtered to UTC hours [14,19), generation
  **v3_pre_gapfill**, sha256 `46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46`
  (md5 `ea2eee6136896b5f8a5b7ddc052f589c`). It is **not** the v4 gap-filled generation, which is
  `processed\zc\v4_gapfill\zc_snapshots_2025-01.parquet`, sha256
  `0c0cb4ad2dfb19be057e6be611d92ff09d06f33de613bf0041b7e5ff22b5012f`
  (md5 `900b30a0b7d5cb890329dac5329b0890`, `PC2_TRANSFER_v4\manifest.csv` line 200) and yields
  **378,000 rows** (21 trading days x 5 h x 3600 s — a complete 1 Hz grid) under the same
  filter. Evidence: `n2\provenance_notes.md` §(d).

## 3. `timestamp_semantics`

Registered vocabulary (PREREG.md line 204): "whether the timestamp column is observation,
event, or availability time, plus the mapping if not the last".

**DECLARED value: the `timestamp` column is a bar-close availability boundary, not the
observation time of any event. A snapshot stamped `T` contains events strictly before `T`.**

Evidence: `process_mbo.py` lines 354-363 — inside `while ts >= next_snap:` the snapshot is
emitted (lines 355-357) BEFORE `book.process_event(...)` (lines 360-363) processes the event
with `ts >= next_snap`. So the book state stamped `T` reflects only events with
`ts_event < T`.

**Recorded misalignment (code-derived, affects trade/MBO columns):** trade and MBO aggregates
are joined on `ts_floor` = wall-clock 1-s floor, not the event-anchored lattice:
`phase5_ml.py` line 222 `snap["ts_floor"] = snap["timestamp"].dt.floor("1s")`, line 230
`trades["ts_floor"] = trades["ts_event"].dt.floor("1s")`, merge at line 248 (trades) and
line 273 (MBO). Because lattice stamps are generally off wall-clock boundaries (see
`bar_duration`), the wall-clock second `[floor(T), floor(T)+1s)` joined to snapshot row `T`
can contain trade/MBO events with `ts_event > T` — i.e., strictly after the row's stamp.
This holds regardless of the tie convention and is a distinct fact from the shift(1) question.

**ROOT CAUSE of the same-second cohort (N2, measured; the obvious hypotheses REFUTED).** On 18
of 48 instrument-months (§2) consecutive lattice rows share a wall-clock second, so
`floor(T_i) == floor(T_{i-1})` and the corrected row's absorbed window is the row's OWN second.
The two `reconstruct_day` code paths that can emit two snapshots inside one wall-clock second —
the >60 s gap re-anchor (L347-352) and the final-snapshot stamp `ts_events[-1]` (L365-368) —
were tested against the ZC 2025-08 lattice and **fail by three orders of magnitude**: of its
211,450 same-second adjacent pairs in the `[14,19)` filtered view, 20 are day-last rows, 24 are
adjacent to a >60 s spacing, **25 are either — 0.012%**; 211,425 are elsewhere
(`n2\provenance_notes.md` §(c); `n2\spacing_classification.csv`).

The actual mechanism is the month-file assembly in
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_mbo.py`, lines 584-590
(verbatim):

```
L584          snap_files = sorted(tmp_dir.glob("snap_*.parquet"))
L586          if snap_files:
L587              snap_tables = [pq.read_table(str(f)) for f in snap_files]
L588              master_snap = pa.concat_tables(snap_tables)
L589              snap_path = proc_dir / f"{sym_lc}_snapshots_{month}.parquet"
L590              pq.write_table(master_snap, str(snap_path))
```

A plain concatenation in **filename order, with no global sort and no de-duplication**. The
month parquet therefore preserves per-day-file blocks in native row order and decomposes into
monotone runs with overlapping wall-clock spans, because each per-day reconstruction pass starts
back at the preceding weekend and runs forward. Measured (`n2\block_overlap.csv`): ZC 2025-01 =
**1 native block, 0 overlapping block pairs, 0 excess rows**; ZC 2025-08 = **17 native blocks,
16 overlapping consecutive block pairs, and up to 5 rows sharing one exact ns timestamp**,
211,450 excess rows over 342,854 distinct seconds. The correlation
`native_blocks == 1 AND overlapping_block_pairs == 0` ⟺ negligible excess holds across all 84
measured files with **zero exceptions**, and every one of the 36 v4 files is single-block and
clean. So the clean-vs-dirty split across instrument-months is neither a DST artefact nor a
code-path artefact: it is overlapping multi-day reconstruction passes concatenated without sort
or de-duplication. Evidence: `n2\provenance_notes.md` §(c); `n2\block_overlap.csv`.

This fact is load-bearing twice: it is the generator of the corrected-side violations (§13, §C),
and it is what makes the N3 cohort predicate checkable from the lattice alone, with no event
data (§C).

## 4. `column_roles`

Registered vocabulary (PREREG.md line 205): per-column rule `at_timestamp`, `at_bar_close`,
`at_source_timestamp` (naming the source column), `always`, or an explicit availability column.

For the Phase 5 45-column FULL_FEATURES set (`phase5_ml.py` lines 60-80):

| Columns | Declared role | Construction evidence |
|---|---|---|
| spread_ticks; bid_size_1; ask_size_1; l1_imbalance; total_bid_depth; total_ask_depth; depth_imbalance; book_slope_bid/ask; depth_change_{1,5,30}s; depth_pctile_{60,300}s | `at_bar_close` (snapshot lattice) | phase5_ml.py lines 183, 199-214; raw sizes from the snapshot frame |
| mid_return_{1,5,10,30,60,300}s; volatility_{30,300}s; range_{60,300}s | `at_bar_close` (snapshot lattice; rolling/lagged windows ending at the row) | phase5_ml.py lines 192-198 |
| net_delta_{1,5,10,30,60}s; buy_volume_10s; sell_volume_10s; trade_count_10s; large_trade_count_10s; vwap_distance | `at_bar_close` — **approximation**: true availability is `at_source_timestamp` on the wall-clock second end (`ts_floor + 1s`), which can lie strictly AFTER the row's stamp `T` (see §3 misalignment) | phase5_ml.py lines 222, 230, 237-258 (vwap_distance line 258 additionally reads mid[t], a label-base cell) |
| bid/ask_add_rate_{5,10}s; bid/ask_cancel_rate_{5,10}s; cancel_ratio_asymmetry; order_flow_accel | same as trade columns (ts_floor join) | phase5_ml.py lines 267-285 |
| minutes_since_open | `always` (deterministic function of the row's own timestamp; clock-only) | phase5_ml.py line 189 |

**Phase 7 difference (observed cheaply, constants only):** Phase 7 trains on
ALL_L2_FEATURES = 35 columns (`phase7_l2_sim.py` lines 73-108), NOT the Phase 5 45-column set.
Relative to FULL_FEATURES it ADDS: tick_direction, trade_volume_1s, trade_count_1s,
dollar_volume_1s, session_open, session_mid, session_close, book_imbalance_ratio,
weighted_mid; and DROPS: mid_return_60s, mid_return_300s, volatility_30s, volatility_300s,
range_60s, range_300s, depth_pctile_60s, depth_pctile_300s, trade_count_10s, all eight
add/cancel-rate columns, cancel_ratio_asymmetry, order_flow_accel. Roles for the nine added
columns are assigned in the block "Phase-7-added columns [T2 addendum — DRAFT, author review
required]" immediately below. That block is FROZEN as the measurement record and is not edited
by any later item. The one judgment it left open — the weighted_mid FLAVOR — is RESOLVED by
working resolution R6 as `contemporaneous_state_flow` (PROVISIONAL until the prereg-v30a tag is
signed); see the supersession note immediately after the block. The block's column_role
assignments and DAG classes are unaffected by R6 and stand as written.

## Phase-7-added columns [T2 addendum — DRAFT, author review required]

Added by item T2 of "Phase 0 addendum 3: pre-amendment closure checks". Scope: the nine
columns Phase 7 feeds (`ALL_L2_FEATURES`, `phase7_l2_sim.py` lines 73-108) that are absent
from the Phase 5 45-column set. Registered column_role vocabulary (PREREG.md line 205,
verbatim): "per-column rule: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming
the source column), `always`, or an explicit availability column".

**PRE-LAG vs POST-LAG:** none of the nine appears in `EXEMPT_COLS` (line 266: timestamp,
mid_price, month, ts_floor, hour_utc), in `label_cols` (line 267: fwd_move_ticks_*), or in
`raw_book_cols` (lines 268-272), so all nine are in `feature_cols` (line 275) and are lagged
by line 276 `snap[feature_cols] = snap[feature_cols].shift(1)`. Every role below describes
the RAW constructed column; the value FED to the models at row `T` is the lagged one (the
row `T-1` construction).

| Column | Declared role (raw construction) | Construction evidence (phase7_l2_sim.py, verbatim) |
|---|---|---|
| tick_direction | `at_bar_close` (snapshot lattice; reads the row's own mid) | line 156: `snap["tick_direction"] = np.sign(mid.pct_change(1)).fillna(0)`; mid line 149: `mid = snap["mid_price"].replace(0, np.nan)`. In-code comment line 155 "# tick direction = sign of prior 1s return" is true only POST-shift; pre-shift the value at row t reads mid(t). |
| trade_volume_1s | `at_bar_close` — **approximation**, mirroring §4's Phase 5 trade-column row: true availability is `at_source_timestamp` (source column `ts_floor`; the aggregate over wall-clock second `[ts_floor, ts_floor+1s)` completes at `ts_floor + 1s`, which can lie strictly AFTER the row stamp `T` — §3 misalignment) | line 246: `snap["trade_volume_1s"] = snap["trade_volume"].fillna(0)`; upstream full-second groupby lines 216-226, specifically line 221: `trade_volume=("size", "sum")`; `trades["ts_floor"] = trades["ts_event"].dt.floor("1s")` line 206; merge line 231: `snap = snap.merge(tagg, on="ts_floor", how="left")`. If the trades parquet is absent the column is constant 0.0 (lines 250-255). |
| trade_count_1s | same as trade_volume_1s | line 247: `snap["trade_count_1s"] = snap["trade_count"].fillna(0)`; groupby line 220: `trade_count=("size", "count")` |
| dollar_volume_1s | same as trade_volume_1s | line 248: `snap["dollar_volume_1s"] = snap["dollar_volume"].fillna(0)`; upstream line 214: `trades["dollar_vol"] = trades["size"] * trades["price"]`; groupby line 223: `dollar_volume=("dollar_vol", "sum")` |
| session_open | `always` (deterministic clock function of the row's own timestamp; §4 precedent: minutes_since_open. Candidate alternative reading `at_timestamp` exists in the vocabulary; the draft's precedent for clock-only columns is `always`.) | lines 159-162: `snap["minutes_since_open"] = (snap["hour_utc"] - ds) * 60 + snap["timestamp"].dt.minute`; `total_minutes = (de - ds) * 60`; `frac = snap["minutes_since_open"] / total_minutes`; `snap["session_open"] = (frac < 0.1).astype(float)`; hour_utc line 144: `snap["hour_utc"] = snap["timestamp"].dt.hour` |
| session_mid | `always` (same basis) | line 163: `snap["session_mid"] = ((frac >= 0.1) & (frac < 0.85)).astype(float)` |
| session_close | `always` (same basis) | line 164: `snap["session_close"] = (frac >= 0.85).astype(float)` |
| book_imbalance_ratio | `at_bar_close` (snapshot lattice; pure function of the same row's depth sums) | lines 188-189: `snap["book_imbalance_ratio"] = (snap["total_bid_depth"] / snap["total_ask_depth"].replace(0, np.nan)).fillna(1.0)`; parents lines 169-170: `snap["total_bid_depth"] = snap[bid_cols].sum(axis=1)`, `snap["total_ask_depth"] = snap[ask_cols].sum(axis=1)` |
| weighted_mid | `at_bar_close` (snapshot lattice; reads the same row's raw book AND subtracts the same row's mid) | lines 184-187: `snap["weighted_mid"] = (snap["bid_price_1"] * snap["ask_size_1"] + snap["ask_price_1"] * snap["bid_size_1"]) / (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)`; then `snap["weighted_mid"] = (snap["weighted_mid"] - mid) / tick  # distance from mid in ticks` |

**Recorded quirk (fact, not resolved):** session_open/mid/close (and their parent
minutes_since_open) are deterministic clock functions with role `always`, yet they are NOT
in the shift exemption, so the FED session flags at row `T` are the row `T-1` flags
(line 276). hour_utc itself IS exempt (line 266) but is not a fed feature.

**DAG cross-check against `f3\fixture_manifest_DRAFT.json`** (classes there describe PRE-LAG
construction semantics per that manifest's `classification_basis`):

- tick_direction — manifest LEAK-SOURCE / label_base_price: **AGREE** (line 156 reads
  mid(t), the label base of `fwd_move_ticks_*` per lines 193-195).
- trade_volume_1s, trade_count_1s, dollar_volume_1s — manifest LEAK-SOURCE /
  contemporaneous_state_flow: **AGREE** (full-second aggregates of the row's own wall-clock
  second, lines 216-226 + 231 + 246-248).
- session_open, session_mid, session_close — manifest CLEAN, parent minutes_since_open:
  **AGREE** (lines 159-164, clock-only).
- book_imbalance_ratio — manifest DESCENDANT, parents total_bid_depth / total_ask_depth:
  **AGREE** (lines 188-189 read only the two depth sums; no independent raw read).
- weighted_mid — manifest LEAK-SOURCE: **AGREE on class** (lines 184-186 read raw same-row
  book columns directly — an independent leak, not inherited). The FLAVOR is the manifest's
  own flagged judgment call and is **AMBIGUOUS-PENDING-AUTHOR (flavor only; class and
  column_role are not ambiguous)**: the `label_base_price` reading rests on line 187
  `(snap["weighted_mid"] - mid) / tick` — the same "(X - mid)/tick" form as vwap_distance
  (line 243), whose flavor is label_base_price in both the 45-set DAG and the F3 manifest;
  the `contemporaneous_state_flow` reading rests on lines 184-186 reading
  bid_price_1/ask_price_1/bid_size_1/ask_size_1 at t — the same raw-book exposure as
  book_slope_bid/ask (lines 178-179), whose flavor is contemporaneous_state_flow. Both
  readings are presented; neither is resolved here.

**SUPERSESSION NOTE (outside the frozen block, per R5's "leave the T2 addendum block
untouched").** The block above records the weighted_mid FLAVOR as AMBIGUOUS-PENDING-AUTHOR.
That status is superseded. **Working resolution R6 (file tail, verbatim) declares the
weighted_mid flavor `contemporaneous_state_flow`**, PROVISIONAL until the prereg-v30a tag is
signed, on the information-content test: `mid` is `(bid1+ask1)/2`, computed from the same cells
lines 184-186 already read, so the `(X - mid)/tick` form of line 187 adds no information — the
substance matches `book_slope`, not `vwap_distance`. R6 records the counter-reading
(form-match with line 187) as considered and rejected. The block's LEAK-SOURCE class and its
`at_bar_close` column_role were never ambiguous and are unchanged. Nothing else in the block is
affected, and the block itself is byte-identical to its D1-era capture
(`d1\pre_t2_block.txt`, md5 `d4dd09b939540bdc2db33a2e13cb049e`).

## 5. `label_availability`

Registered vocabulary (PREREG.md §2.4, lines 220-222): one user declaration,
`a(y_j) = label timestamp + label horizon + publication delay`; publication delay defaults to
zero only when the user supplies the declaration.

**DECLARED value:**
- **Label base:** `mid(t)` — the decision row's own snapshot mid.
  `phase5_ml.py` lines 216-219: `fwd = mid.shift(-h)`;
  `snap[f"fwd_move_ticks_{h}s"] = (fwd - mid) / tick` (mid defined line 190 from
  `snap["mid_price"]`). Audit confirmation: `phase5_audit.py` line 101 (verbatim print):
  "The label predicts direction FROM mid[t]."
- **Label timestamp:** the decision row's stamp `T` (the base anchors at the row itself —
  zero publication delay of the label BASE relative to the decision row).
- **Label horizon: h ∈ {5, 10, 30, 60} ROWS, not seconds** (`phase5_ml.py` line 90
  `HORIZONS = [5, 10, 30, 60]`; `phase7_l2_sim.py` line 110 identical; applied via
  `fwd = mid.shift(-h)`, line 216 — a POSITIONAL shift on the filtered frame).
- **Publication delay: 0 (declared, per §2.4 this zero is part of the declaration, not a
  profile default).**
- **AMENDED — label availability is POSITIONAL, not `T + h` seconds.** The prior draft wrote
  `a(y_T) = T + h` seconds on the lattice. That is false wherever the frame is not contiguous
  at 1 s. The declared value is:

  > **`a(y_t)` = the realization time of the PAIRED ROW's mid — the `timestamp` of the row h
  > POSITIONS after row `t` on the filtered frame, plus publication delay 0.**

  Where the frame is contiguous this equals `t + h` seconds. Where the h-row step crosses a
  session or day boundary or a >60 s gap, the paired row is in the **next session**, and the
  label is not available until then. Measured on the ZC 2025-01 fixture frame (338,159 lattice
  rows, generation v3_pre_gapfill — §2 naming rule; 20 session boundaries): worst realization
  span **3d 19:31:00** at h=60, median overnight ~19h30m; intra-day >60 s re-anchor gaps give
  same-day spans up to 30m45s (0 days 00:30:45.369966846) at h=60. Full table and per-horizon
  detail: §11; `t3\day_edge_table.csv` lines 2-5; `t3\day_edge_samples.csv`;
  `v2\reanchor_gaps.csv`.

**GATE TREATMENT of the 2,100 cross-boundary label rows — declared explicitly.** The
cross-boundary rows number **2,100** across the four horizons on ZC 2025-01 (100 at h=5, 200 at
h=10, 600 at h=30, 1,200 at h=60 = h x 20 boundaries; `t3\day_edge_table.csv` lines 2-5). What
counts, exactly:

1. **They are DECLARED.** Their availability is the positional value above — next-session
   realization, up to 3d 19:31:00. They are not an undeclared corner.
2. **They are IN the scored population.** They are not excluded, not masked, and not given a
   separate denominator. All 2,100 carry REAL label values — **zero NaN** (§11); the only NaN
   source in the frame is the month tail, exactly h rows per horizon.
3. **Findings on them are adjudicated by the declared map like any other row** (R9). A detector
   finding on a cross-boundary row is required if the map's cell predicts a violation there,
   is a false positive if the map excludes it, and is unscored if the cell is unscored. Being a
   cross-boundary row is, by itself, neither a licence for a finding nor a defence against one.
4. **No separate label-availability criterion is created for them.** This declaration adds no
   new gate criterion; §6.2's four criteria as amended in §A are the whole gate.

Caveats recorded as fact:
- **The day-edge label rows are NOT removed downstream, and they are ENRICHED** — the earlier
  draft's "whether any downstream filter removes day-edge label rows was NOT verified" caveat
  is RETIRED, verified by §11's measurement: 81-83% of cross-boundary labels pass the >=2-tick
  magnitude filter (0.83 / 0.83 / 0.823 / 0.812 by horizon) against an overall baseline of
  0.0-1.0% (0.000 / 0.001 / 0.004 / 0.010). Gap-spanning labels are not filtered out; they are
  massively over-represented in the magnitude-filtered training and evaluation population.
  Evidence: `t3\day_edge_table.csv` lines 2-5.
- **Zero-tick handling divergence (recorded fact):** `preregistration_v4.txt` lines 306-307:
  "Zero-tick observations excluded from training and evaluation." Pre-fix
  `phase5_ml.py` line 679 instead applies a >=2-tick MAGNITUDE filter
  (`valid = valid[valid[ret_col].abs() >= 2.0].copy()`) to training and evaluation
  populations; phase5_fixed removed the magnitude filter and excluded zero-tick rows from
  evaluation only (eval_mask, line 747). Both halves are now CODE-VERIFIED by M3
  (`m3\zero_tick_evidence.md` §§1-5, §8).
- **M3 caveat — the zero-tick exclusion has a silent fallback.** `phase5_fixed.py` lines
  807-811 (verbatim in `m3\zero_tick_evidence.md` §4):
  `if eval_mask_te.sum() > 10: test_auc = roc_auc_score(y_test_arr[eval_mask_te], ...)` /
  `else: test_auc = roc_auc_score(y_test_arr, test_pred)`. **When 10 or fewer non-zero test
  rows remain, the reported AUC is computed over ALL test rows, zero-tick rows included** —
  the exclusion silently does not apply. Same pattern for validation AUC at lines 816-818 and
  796-798. Recorded because any AUC quoted in this file inherits it.
- **M3 caveat — the two exclusions are not complements.** `phase5_ml.py` line 679 drops
  -1, 0 and +1 tick rows; `phase5_fixed.py` lines 678/747 drop only 0. The fixed script's
  evaluation set is therefore strictly larger than a like-for-like recovery of the pre-fix
  one, so AUCs across the two scripts are not computed over comparable populations
  (`m3\zero_tick_evidence.md` §7). This does not affect the pre/post pair of §8, which is a
  phase7/phase7_fixed pair sharing one bit-exact label vector (§9).

## 6. `ties` — AMBIGUOUS-PENDING-AUTHOR

Registered vocabulary (PREREG.md lines 190-193): `available` (default): cell available to row
*i* iff `a(j,c) <= d(i)`; `unavailable`: iff `a(j,c) < d(i)`. Default locked to `available`
on §0.3 Claim A (line 197). Line 411: "The tie comparator changes findings at the boundary
instant."

**The fixture evidence forces the boundary question but does not answer it.** The implication
of the timestamp semantics (§3): a snapshot stamped `T` contains events strictly before `T`
(`process_mbo.py` 354-363), so the INFORMATION CONTENT of every snapshot-`T` cell is realized
strictly before `T`, while the cell's stamp equals `T` exactly. With `d(i) = T` and
`a(snapshot-T cell) = T`, the pre-fix (unshifted) fixture side sits exactly on the tie:

- **Reading A — `ties: available` (registered default).** Content strictly before `T` means
  the value is knowable by instant `T`; `a = T <= d = T` admits it. Under this reading the
  pre-fix pipeline's snapshot-derived features are NOT availability violations at the
  boundary instant; the declared shift(1) convention (preregistration_v4.txt line 303) is a
  stricter-than-availability house rule. The pre-fix leak then consists of (a) the
  trade/MBO wall-clock join cells whose events can lie strictly AFTER `T` (§3 misalignment
  — a violation under BOTH branches), and (b) label-base anchoring (mid[t] readable while
  the label measures FROM mid[t]) — availability-legal under this reading, though it is the
  mechanism the archive's own audit names (phase5_audit.py lines 96-109).
- **Reading B — `ties: unavailable`.** The snapshot is materialized only when the event
  stream reaches an event with `ts >= next_snap` (`process_mbo.py` line 354), i.e., strictly
  after `T` in stream order; and the protocol's own mandatory shift(1) (preregistration_v4.txt
  line 303) signals author intent that boundary-instant cells NOT be used. Under
  `a = T < d = T` failing, every unshifted snapshot-`T` feature in the pre-fix side is an
  availability violation, and the pre-fix/post-fix pair adjudicates as leak/clean.

The two readings adjudicate the PRE-FIX fixture side oppositely (largely clean vs. broadly
leaking). The registered vocabulary is binary; the archive contains support for both (the
strictly-before construction supports A; the registered protocol's shift(1) mandate and the
stream-order materialization support B). **Element left AMBIGUOUS-PENDING-AUTHOR.** Note for
the author: if `available` is kept as the fixture declaration, the fixture's status as an
availability-violation exemplar (Mechanism 1) rests on the trade/MBO forward-join cells and
on the label-base-reader flavor, not on the shift(1) absence per se.

## 7. Remaining schema elements (outside this item's six, listed for completeness)

- `availability_fn`: none declared.
- `panel_mask_scope`: global — locked by PREREG.md line 210, not fixture-specific.
- `panel_rule_scope`: default (per entity); fixture models are per-instrument, so no
  cross-entity comparison arises. Not evidenced further.
- `embargo`: none declared anywhere in the archive that this item examined.

---

## Evidence classes per element

| Element | Class | Basis |
|---|---|---|
| `decision_time` | BOTH | paper: preregistration_v4.txt 303-304; code: phase5_ml.py (no shift), phase7_l2_sim.py 276 |
| `bar_duration` | code-derived | process_mbo.py 322, 331, 342, 347-352, 358, 367 |
| `timestamp_semantics` | code-derived | process_mbo.py 354-363; join misalignment phase5_ml.py 222, 230, 248, 273 |
| `column_roles` | code-derived | phase5_ml.py 60-80, 183-298; phase7_l2_sim.py 73-108 (constants only for the Phase 7 delta) |
| `label_availability` | BOTH | code: phase5_ml.py 90, 190, 216-219, 679; paper: preregistration_v4.txt 306-307; code-embedded prose: phase5_audit.py 101 |
| `ties` | BOTH — value AMBIGUOUS-PENDING-AUTHOR | code: process_mbo.py 354-363; paper: PREREG.md 190-197, 411 (vocabulary/default) + preregistration_v4.txt 303 (intent) |

All paths under `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` unless prefixed otherwise;
PREREG.md lives in the prereg repo `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`.

---

# Part II — v30a declaration assembly (item D1)

## DRAFT — AUTHOR REVIEW REQUIRED (v30a assembly)

Assembled by item D1 of "Phase 0 addendum 3: pre-amendment closure checks"; carried forward by
item P2 (2026-08-12) under working resolutions R6-R9. Every number below is a measurement from
a named artifact — the DELTA R2 round, the M-rounds (M3/M4/M5), or the N-rounds (N1 declared
map, N2 lattice provenance, N3 cohort predicate); nothing is re-derived here. Relative evidence
paths are under
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\`;
archive paths are under `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only). Working
resolutions **R1-R9** (verbatim at the file tail) govern this Part; they are PROVISIONAL until
the prereg-v30a tag is signed. Where a later resolution supersedes an earlier one — R6 over
R5's pending status, R9 over the old "corrected-side zero" — the later one governs and the
earlier text stands as the record.

Carried forward from Part I into the v30a draft: `decision_time` (section 1 DECLARED value —
which now states the measured boundary `floor(t-1)+1s` and is the ONLY statement of the
boundary rule in this file; section 10 is its evidence), `bar_duration` (section 2, with the
N2 generation and non-1 Hz caveats), `timestamp_semantics` (section 3, with the N2 root cause),
`column_roles` (section 4 plus the frozen Phase-7-added-columns block, weighted_mid flavor
resolved by R6), `label_availability` (section 5, AMENDED to the positional definition), and
the section 7 remaining-elements list — subject to R1's ties resolution (section 12) below.
Part I section 6 records the ties ambiguity as measured; R1 resolves it.

## §A. Conformance walk against PREREG.md §6.2, element by element (item P2)

**First section of Part II.** Every registered element of PREREG.md §6.2 (lines 443-481, read
in full this pass at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`) is
quoted verbatim with its line number and marked **SATISFIED** (with how, and the artifact) or
**AMENDED** (old text quoted, new text stated, why, and that it is a class C amendment under
PREREG.md line 93). Amendments are PROVISIONAL until the prereg-v30a tag is signed.

**A.0 — the amendment class, stated once.** PREREG.md line 93 (verbatim): "**C — semantic or
accounting gaps** | The measurement reveals a needed *new* branch, unit, denominator, coverage
state, tier licence, or acceptance criterion | **not resolve under this registration** |
anything that changes what a published number means". Line 95 (verbatim): "**Class C requires
an amended registration**, committed and externally timestamped **before the affected detector
is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md`
entry standing alone." Every AMENDED entry below is a class C amendment carried by this
registration.

---

### A.1 — Reference AUC anchor — **AMENDED (class C)**

**Registered text, PREREG.md line 445 (verbatim):**

> **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

**OLD:** the pair (0.957, 0.675) with an acceptance interval of ±0.010 absolute, as the anchor
the fixture pair must reproduce.

**NEW:** the anchor is **retired and replaced** by the recomputed ZC **LightGBM** trio, computed
directly from the stored per-row predictions of the declared fixture pair (§8):

| Horizon | Pre-fix (contaminated) | Post-fix (corrected) | n rows |
|---|---|---|---|
| 5s | 0.966244 | 0.931536 | 1,047,430 |
| 10s | 0.939968 | 0.756504 | 655,016 |
| 30s | 0.856419 | 0.679288 | 745,656 |

Source: `f1\f1_results.csv`, column `recomputed_auc`, rows `pre/ZC/LightGBM/{5s,10s,30s}`
(lines 50-52) and `post/ZC/LightGBM/{5s,10s,30s}` (lines 114-116).

**Why the old anchor cannot stand, stated plainly:**

1. **No single horizon satisfies the old interval on both sides.** Against 0.957 ± 0.010 on the
   pre-fix side and 0.675 ± 0.010 on the post-fix side: 5s passes pre (|0.966244 − 0.957| =
   0.009244) and fails post by 0.2565; 10s fails pre by 0.0170 and fails post by 0.0815; 30s
   fails pre by 0.1006 and passes post (|0.679288 − 0.675| = 0.004288). There is no horizon at
   which the registered pair is reproduced. Keeping the interval would fail the gate on a
   fixture whose pair is otherwise exactly as registered.
2. **The model family changes: XGBoost → LightGBM.** The original documented protocol names
   XGBoost (`MASTER_FINDINGS\preregistration_v4.txt` line 273 "2. XGBoost (gradient boosted
   trees)"; line 284 records its hyperparameters). The declared trio above is LightGBM.
   `f1\f1_results.csv` carries both families across 128 rows (32 rows each for
   pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost); the declaration names LightGBM and
   states so rather than leaving the family implicit.
3. **The RE-EVALUATE class makes the recomputation authoritative, not merely alternative.** The
   fixture is the stored-prediction pair (§8): 64 parquets per side, each carrying `pred_score`
   and `true_label` per row. AUC over those columns is a pure function of bytes already on
   disk — no retraining, no re-randomization, no environment dependence, nothing that a rerun
   could move. The recorded meta AUCs are a 4-decimal secondary record of the same quantity;
   where meta exists it agrees (`flag_gt_5e-5` False on all 95 matched rows, §8). So the
   recomputation does not contradict the record — it supersedes it in precision, and it is the
   only form of the number that can be audited from the fixture itself.

The `full` mode clause of line 445 is unaffected and stands.

---

### A.2 — Ground-truth column DAG and the independently-leaking-source count — **SATISFIED, with the governing scope named**

**Registered text, PREREG.md line 446 (verbatim):**

> **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.

**SATISFIED.** **The count of independently leaking sources is 25**, and the **governing
manifest scope is `f3\fixture_manifest_DRAFT.json`** — the 35-column set the Phase 7 models are
fed. Its `counts` block (read this pass): `independently_leaking_sources: 25`, `leak_source: 25`,
`descendant: 6`, `clean: 4`, `total_fed_to_phase7: 35`, `not_fed_to_phase7: 19`, with the
leak-source flavor split `label_base_price: 7` / `contemporaneous_state_flow: 18`.

**Why F3 governs and not T4.** `t4\fixture_manifest_35col_DRAFT.json` reports
`counts_projected_subset`: `projected_total: 28`, `unconstructible_total: 7`, `leak_source: 22`,
`descendant: 5`, `clean: 1`, with `unconstructible_by_class` = `leak_source: 3`, `descendant: 1`,
`clean: 3`. That 22 is a property of what the **F2 rebuild can reconstruct** under the
selection/renaming-only projection rule (§17), not a property of the fixture the gate scores.
The gate's fixture is the stored-prediction pair, whose feature set is the full 35 columns under
working resolution R3 (§16 item 1). **The declaration therefore governs on 25 and records 22 as
the reconstruction-limited subset**; both numbers appear in this file and neither is left to be
inferred. Any gate report quoting a leaking-source count must name which of the two scopes it
counts under — that is a declared reporting obligation, not a convention.

---

### A.3 — Contamination availability class — **SATISFIED BY THIS DECLARATION; manifest field OUTSTANDING**

**Registered text, PREREG.md line 450 (verbatim):**

> **Contamination availability class** recorded in the manifest.

**Declared class: AVAILABILITY VIOLATION BY FORWARD JOIN** — the contamination is not a value
corruption, a shuffle, or a label leak in the ordinary sense; it is a cell whose availability
time is strictly later than the decision time that consumes it. Mechanism: the `ts_floor`
wall-clock-second join (§3) attaches to snapshot row `T` an aggregate over
`[floor(T), floor(T)+1s)`, a window that completes at `floor(T)+1s` and can contain events with
`ts_event > T`. Measured incidence and per-column enumeration: §14 and §C.

**Recorded gap, honestly:** neither `f3\fixture_manifest_DRAFT.json` nor
`t4\fixture_manifest_35col_DRAFT.json` carries a named field for the contamination availability
class — verified this pass by key search over both files. This declaration is the record until
that field is added. **Adding the field is a mechanical (class A) act that must be done before
the tag**; it is listed in §D as a lock-time obligation.

---

### A.4 — Sliced variant for CI — **NOT SATISFIED; OUTSTANDING**

**Registered text, PREREG.md line 451 (verbatim):**

> **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**NOT SATISFIED.** No artifact in this spike produces or names a sliced fixture variant, and no
padded slicer has been run against the fixture. Recorded as outstanding rather than quietly
omitted, because PREREG.md §2.7's rule is that undeclared means unsupported, never pass. What is
required to close it: a sliced variant produced by the same padded slicer the user-facing slice
audit uses, with the slice boundaries declared, and — under R9 — a **map cell per slice**, since
a slice of a CHARACTERIZED side is not automatically clean either. **This is not an amendment;
the registered element stands unchanged and is simply not yet met.**

---

### A.5 — Reconstruction discipline, timing, and the ambiguity clause — **SATISFIED**

**Registered text, PREREG.md line 447 (verbatim):**

> **The availability declaration is reconstructed, not chosen** — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon, and intended live execution protocol, with **evidence for each element recorded before any detector tuning.**

**SATISFIED.** Every element of the declaration carries a code or paper citation recorded before
any detector exists — Part I §§1-7 and the evidence-class table, plus §§8-17 and §§B-C. No
detector code has been written or tuned in any item of this spike; the declaration's numbers all
predate it.

**Registered text, PREREG.md line 448 (verbatim):**

> **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).

**SATISFIED.** This whole file is a Phase 0 product; no cross-tool comparison has been run.

**Registered text, PREREG.md line 449 (verbatim):**

> **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.

**SATISFIED — the clause does not fire, and the reason matters.** The original work DID document
prediction timing: `MASTER_FINDINGS\preregistration_v4.txt` lines 303-304 (quoted in §1). The
fixture is therefore **not** semantically ambiguous and does **not** need a labelled hypothetical
declaration. What measurement established is a different thing: the documented timing was
**violated by the artifact** (§10). Documented-and-violated is not the same as undocumented, and
the declaration states the measured boundary (§1) precisely so that the distinction is not
smuggled. The one element Part I genuinely left ambiguous — `ties` — is resolved by R1 to the
registered default, not to a hypothetical (§12).

---

### A.6 — Criterion 1 — **SATISFIED, with one declared denominator exclusion**

**Registered text, PREREG.md line 459 (verbatim):**

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.

Related registered text, PREREG.md line 464 (verbatim):

> Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

and PREREG.md line 468 (verbatim):

> Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**SATISFIED.** The criterion-1 violation set is enumerated side-relatively and post-lag in §C,
by column, from the N1 declared map. **One column is DECLARED OUT of the criterion-1
denominator: `buy_volume_10s`** — see §C.4(a); it is a degenerate constant on this fixture and
cannot carry a finding for any reason connected to availability. The exclusion is declared here,
before any run, exactly as line 468's alias rule requires of anything recorded pre-run.

---

### A.7 — Criterion 2 — **SATISFIED**

**Registered text, PREREG.md line 460 (verbatim):**

> 2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.

**SATISFIED and unchanged.** The manifest-clean set is the 4 clean columns of
`f3\fixture_manifest_DRAFT.json` (`counts.clean: 4`). Two declared dispositions bear on it and
are recorded in §C.4: the **session-flag staleness** quirk (§C.4(b)) is a documented artifact of
the shift and licenses **no** finding, on either side; and `book_imbalance_ratio` (§C.4(c)) is
gate-status **EXCLUDED**. Neither weakens the criterion — both remove a route by which a
non-availability artifact could be scored as one.

---

### A.8 — Criterion 3 — **AMENDED (class C), per working resolution R9**

**Registered text, PREREG.md line 461 (verbatim):**

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

**OLD (quoted from R9, file tail, verbatim):** "no findings on any corrected column".

**NEW (quoted from R9, file tail, verbatim):** "detector findings must match the declared
per-side, per-class, per-instrument-month violation map; findings the map predicts are required,
findings it excludes are false positives, cells the map does not cover are unscored."

**Rationale, recorded (R9, verbatim):** "the tool's own coverage principle (silence and belief
never convert into a pass) applied to its own exam." And: "The corrected side is described
throughout as CHARACTERIZED, never clean."

**What forced it.** The M5 falsification sweep (`m5\`) extended the corrected-side check beyond
ZC 2025-01 and **falsified the assumption that the corrected side is clean** — see §13(f). The
corrected side carries strictly-post-decision absorption in **18 of 48** instrument-months, up
to **111,334 of 580,944 rows (19.16%)** on zc 2025-09 (`n1\summary_corrected.csv`). Criterion 3
as written would fail the gate on a correctly-behaving detector that reports a real violation
the fixture really contains. That is a semantic gap in the acceptance criterion — class C by
PREREG.md line 93 — and it is amended, not waived.

**What the amendment does NOT do.** It does not lower the bar. A finding on a corrected-side
cell the map marks zero is still a false positive and still fails the gate. It does not create
an unscored escape hatch either: the 72 unscored cells (§13(g)) are named as unscored, never as
clean, and they license no pass. The map is declared and frozen before any detector runs (§D.1).

---

### A.9 — Criterion 4, the identity control, and the sentinel statement — **SATISFIED**

**Registered text, PREREG.md line 462 (verbatim):**

> 4. Silent under the identity control on both.

**SATISFIED, with one declaration that must be stated explicitly or the criterion is unsafe:**

> **SENTINEL STATEMENT.** The wrapped `net_delta` values in this fixture — magnitudes near
> 4.29e9, e.g. the observed **4294967291** for a trade of `size` 5 (2^32 − 5) — are **DATA
> CONTENT, not findings.** They are the as-built product of an uncast uint32 negation (§15) and
> are present identically on BOTH sides. The identity control must remain silent on them. A
> detector that fires on the magnitude, the sign, or the 2^32 signature of these values has
> produced a **false positive under criterion 4**, not a detection — availability is a question
> about *when* a cell is knowable, and these values are equally knowable, and equally wrong, at
> every instant on both sides.

Evidence for the sentinel: `t1\t1_final_output.txt` lines 61-67 (the wrapped value observed in
the f2 rebuild); §15 for the defect's provenance and the C5 verdict that the ORIGINAL runs
wrapped identically. Because the defect is present on both sides and in both pipeline
generations, it cannot differentiate them, which is precisely why it must not be allowed to.

---

### A.10 — Gate framing, proof count, and ordering — **SATISFIED, carried unchanged**

**Registered text, PREREG.md line 453 (verbatim):** "**Pass gate — discrimination, not tier.**"
**Line 457 (verbatim):** "Evaluated on the **frozen default configuration**, under the
reconstructed declaration:". **Line 472 (verbatim):** "> **k of N** labelled leaking sources
received at least one primary PROVEN finding **attributed to that source**." **Line 476
(verbatim):** "**It is published as a count, never as a decimal or percentage**, and it is
identified as a descriptive fixture outcome rather than a performance rate." **Line 480
(verbatim):** "**Ordering, locked:** tune on the development corpus → freeze the candidate
configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults
may not be altered after observing a fixture result."

**SATISFIED, all five, carried unchanged.** Two consequences this declaration must honour and
does: **N is 25** under the governing scope of §A.2, and the fixture proof count is published as
a count with its scope named. And the locked ordering binds this file — §D.1 freezes the map and
every gate-consumed number at the tag, so no number here can be moved after a fixture result is
observed.

---

### A.11 — Walk summary

| §6.2 element | Line | Verdict |
|---|---|---|
| Reference AUC 0.957/0.675, ±0.010 | 445 | **AMENDED (class C)** — retired; LightGBM trio governs |
| Ground-truth column DAG + independent-leak count | 446 | SATISFIED — count 25, F3 scope governing |
| Declaration reconstructed, evidence before tuning | 447 | SATISFIED |
| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED |
| Semantic-ambiguity clause | 449 | SATISFIED — clause does not fire |
| Contamination availability class in manifest | 450 | SATISFIED here; manifest field OUTSTANDING |
| Sliced variant for CI | 451 | **NOT SATISFIED — OUTSTANDING** |
| Pass gate framing; frozen default config | 453, 457 | SATISFIED |
| Criterion 1 | 459 | SATISFIED — one declared denominator exclusion |
| Criterion 2 | 460 | SATISFIED |
| Criterion 3 | 461 | **AMENDED (class C) per R9** — scored against the declared map |
| Criterion 4 (identity control) | 462 | SATISFIED — with the 4.29e9 sentinel statement |
| Descendants secondary; top-k; alias | 464, 468 | SATISFIED |
| k-of-N proof count, published as a count | 470-476 | SATISFIED — N = 25 |
| Ordering, locked | 480 | SATISFIED — enforced by §D.1 |

Two amendments (445, 461), one outstanding element (451), one outstanding mechanical act
(450's manifest field). Everything else stands as registered.

## 8. Fixture identity (element a)

**The v30a acceptance fixture is the Phase 7 universal-lag pre/post pair, MAIN prediction
set, RE-EVALUATE class:**

- Pre-fix side: `results\phase7\l2_predictions\` — 64 parquets.
- Post-fix side: `results\phase7_fixed\l2_predictions\` — 64 parquets.
- **Class: RE-EVALUATE — derived from the stored-prediction directories themselves, not from
  any session record.** Each of the 64 parquets per side carries the columns
  `pred_score, true_label, fwd_move_ticks, mid_price_t` (schema read this pass from
  `results\phase7\l2_predictions\cl_LightGBM_10s_predictions.parquet`; 64 files present in
  each of the two directories, counted this pass). Every metric the gate needs is a function of
  `pred_score` and `true_label` on bytes already on disk, so the pair is **re-scoreable without
  retraining** — which is exactly the RE-EVALUATE class. The demonstration that it is
  re-scoreable is `f1\f1_results.csv`: 128 rows of AUC recomputed from those parquets alone
  (32 rows for each of pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost), reproducing
  every recorded meta value that exists at 4dp. No memory file, session note or external record
  is load-bearing for this classification.
- Pair anchors and recorded meta lines: `f5\DEVIATIONS_entry_SKELETON.md` lines 40-48.

**Reference AUCs, recomputed from the raw stored predictions (F1) — ZC LightGBM trio:**

| Horizon | Pre-fix (recomputed) | Post-fix (recomputed) |
|---|---|---|
| 5s | 0.966244 | 0.931536 |
| 10s | 0.939968 | 0.756504 |
| 30s | 0.856419 | 0.679288 |

These three pairs are the declared reference AUCs of this fixture; the registered
0.957/0.675 ± 0.010 anchor is retired by the class C amendment of §A.1.

**Meta corroboration, stated at its true reach: 95 of the 128 result rows carry recorded meta;
all 95 match the recomputation at 4dp; 33 have no counterpart.** The 33 are `_merge` left_only
— no recorded meta value exists for them, so they are neither confirmed nor contradicted by the
record. On the 95 that do have one, `flag_gt_5e-5` is False throughout. Evidence:
`f1\f1_results.csv`, columns `recomputed_auc` vs `test_auc` (ZC LightGBM rows: pre lines 50-52,
post lines 114-116).

**pc2 timestamped variant set: EXCLUDED.** Named here only as excluded, with C3's
timestamp-intersection caveat: the variant pairs are NOT vector-equal (30/32 pairs differ
in row count by 1-7 rows; zs-60s equal-length but positionally shifted from index 1825);
membership differences sit at session boundaries (plus exactly-counted interior
gap-placement rows in gc and nq); and there are ZERO `true_label` disagreements at shared
timestamps in all 32 pairs. Any use would require timestamp-intersection framing. Evidence:
`c3\label_equality.csv` (pc2_ts rows, lines 66-97), `c3\pc2_diff_summary.csv`,
`c3\pc2_diff_rows.csv`; consolidated in `R2_consolidated_report.md` C3 section.

**The exclusion is HARD, and admitting the set later is a class C amendment.** The pc2
timestamped variant set is excluded from the declared fixture, from every number in this file,
and from every gate denominator. It is named only so that its absence is auditable. **Any
future use of it — in the gate, in a slice, as a robustness check, or as a supplementary
report — changes the fixture the acceptance criteria are evaluated on, and therefore changes
what a published number means. That is class C under PREREG.md line 93 and requires an amended
registration under line 95.** It may not be admitted by a DEVIATIONS entry, by an orchestrator
decision, or by a working resolution recorded in this file's tail.

## 9. Shared label vector — the feature-availability-only licence (element b)

All 64 main-set pairs are bit-exact identical on `true_label`, `fwd_move_ticks`, AND
`mid_price_t` (raw-bytes comparison after dtype/length checks): one shared label vector per
pair. This is the licence for reading the pre/post AUC delta as a feature-availability-only
effect — labels, label bases, and evaluation populations are identical across sides, so
nothing but feature availability differs. Evidence: `c3\label_equality.csv` lines 2-65
(all 64 rows True/True/True, no first_diff_index).

## 10. EVIDENCE for §1's declared boundary — measurement of the corrected features' information boundary (element c; R2)

**This section states no rule.** §1 carries the single normative statement of the boundary
(`floor(t-1) + 1s`). This section is its evidence: what was measured, on what, against which
comparator, and how the cross-checks line up.

**What was measured.** On ZC 2025-01 (lattice 338,159 rows = `processed\zc\zc_snapshots_2025-01.parquet`
under UTC hours [14,19), generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` — §2 naming rule), the
corrected (post-fix) feature row stamped `t` carries the previous row's construction, whose
trade/MBO aggregates cover the full wall-clock second `[floor(t-1), floor(t-1)+1s)`. Measured
against the **historically claimed** boundary `t-1` itself, those features absorb events
strictly after `t-1`:

- trades_all: **89,568 strict + 20 equal** (of 338,158 corrected rows);
- mbo_all: **254,314 strict + 29 equal**;
- worst overhang past `t-1`: **999.999579 ms** (MBO classes; trades worst 999.996869 ms).

That is the measurement that retires the "through time t-1" claim (§1) and fixes the declared
boundary at the end of the absorbed second.

**Scope, stated so it cannot be over-read.** Measured against decision time `t`, this
instrument-month is 0 strict + 0 equal on all 10 classes — but that is **one cell of the
declared map**, not a property of the corrected side. Since M5 and N1, the corrected side is
CHARACTERIZED, not clean: 18 of 48 instrument-months carry strictly-post-decision absorption
(§13). Nothing in this section extends beyond ZC 2025-01.

**PRIMARY vs cross-check — which artifact is authority for what:**

| Quantity | PRIMARY artifact | Cross-check |
|---|---|---|
| corrected vs `t-1` (this section) | `t1\violation_table.csv` `corrected`/`claimed_T_prev` rows — line 4 trades_all 89568/20/999.996869, line 67 mbo_all 254314/29/999.999579 | `c4\independent_counts.csv` `prev_row_B` rows — line 3 trades_all 89568/20, line 11 mbo_all 254314/29 |
| contaminated vs `T` (§12, §14) | **`t1\violation_table.csv` `contaminated`/`decision_T` rows — T1 is PRIMARY** | C4 **has no contaminated rows at all**; its `prev_row_B` analog is the lag-image and differs by exactly 1 on every MBO class (see below) |
| corrected vs `T`, ZC 2025-01 (§13(e)) | `t1\violation_table.csv` `corrected`/`decision_T` | `c4\independent_counts.csv` `decision_T` rows — genuinely the same quantity, exact agreement |
| all 48 instrument-months, both sides (§13) | `n1\declared_map.csv` | `m5\per_instrument_counts.csv` (453 of 453 cells reproduced exactly, 0 disagreements) |

**Corrected-vs-(t-1) is the LAG-IMAGE of contaminated-vs-T, not a third independent
measurement.** The corrected row `t` *is* the contaminated row `t-1`, shifted one position
(§17 verifies this bit-exactly: corrected[t] == contaminated[t-1] on all 28 projected columns,
max_abs_diff 0.0). So asking "does corrected row `t` absorb events after `t-1`?" is the same
question as "does contaminated row `t-1` absorb events after its own stamp?", re-indexed. The
two count sets agree because they must. Treating their agreement as independent corroboration
would be double-counting one measurement, and this declaration does not do so. The genuinely
independent confirmations are C4's blind re-derivation (different library, unread T1 outputs,
lattice re-derived from the snapshots parquet plus the builder filter) and N1's reproduction of
every M5 cell.

**Reconciliation of the off-by-ones — both are structural, neither is a discrepancy.**

1. **338,159 lattice rows vs 338,158 corrected rows.** The corrected frame is the lag-image of
   the lattice, and **row 0 has no predecessor**: there is no row `-1` whose construction it
   could carry, so the first lattice row yields no corrected row. N = 338,159 → N−1 = 338,158.
   The same relation holds in every instrument-month of the map (`n1\lattice_profile.csv`
   columns `rows` and `corrected_rows` differ by exactly 1 in all 48;
   `n3\cohort_profile.csv` reproduces it independently).
2. **mbo_all 254,315 contaminated vs 254,314 corrected-at-prev.** The contaminated side counts
   a violating *indicator* on row `T`; the corrected side counts the same indicator carried
   forward to row `T+1`. **The last row's indicator has no successor row to carry it**, so
   exactly one indicator is lost in the shift. 254,315 → 254,314. The same −1 appears on every
   MBO class and on no trades class, because the trades classes' final row happens not to be a
   violating row (trades_all 89,568 on both; trades_large 23,633 on both). Per class:
   mbo_all 254,315→254,314, mbo_bid_add 164,959→164,958, mbo_ask_add 162,754→162,753,
   mbo_bid_cancel 135,981→135,980, mbo_ask_cancel 129,334→129,333,
   mbo_cancel_any 179,857→179,856 (contaminated values from
   `v1\mean_overhang_by_class.csv` `strict_count`, confirmed by
   `n1\declared_map.csv` contaminated/zc/2025-01 rows; corrected-at-prev values from
   `c4\independent_counts.csv` `prev_row_B`).

Neither off-by-one is a disagreement between implementations. Both are consequences of the
lag being a one-row positional shift on a finite frame.

**Historical contract text**, retained ONLY as the violated claim and quoted once in §1:
`MASTER_FINDINGS\preregistration_v4.txt` lines 303-304.

## 11. Session-tail label semantics (element d; T3)

`shift(-h)` labels are POSITIONAL, so at session/day boundaries the label pairs row `t`
with a row across the gap — this is the measurement behind §5's amended positional
`label_availability`. Measured on the ZC 2025-01 fixture frame (**338,159 rows** =
`processed\zc\zc_snapshots_2025-01.parquet` under UTC hours [14,19), generation
**v3_pre_gapfill**, sha256 `46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46`
— §2 naming rule; NOT the v4_gapfill generation, which is 378,000 rows; 20 session
boundaries):

| h | cross-boundary pairs (= h x 20) | real values | NaN | worst span | median span |
|---|---|---|---|---|---|
| 5 | 100 | 100 | 0 | 3d 19:30:05 | 19:30:05 |
| 10 | 200 | 200 | 0 | 3d 19:30:10 | 19:30:10 |
| 30 | 600 | 600 | 0 | 3d 19:30:30 | 19:30:30 |
| 60 | 1200 | 1200 | 0 | 3d 19:31:00 | 19:31:00 |

- ALL cross-boundary labels are REAL values — zero NaN. The month tail is the ONLY NaN
  source: exactly h NaN labels per horizon (5/10/30/60 total NaN = month-tail NaN).
- Spans: median overnight ~19h30m; worst 3d 19:31:00 (the MLK long weekend,
  2025-01-17 -> 2025-01-21; sample rows `t3\day_edge_samples.csv` lines 4, 7, 10, 13).
- **Magnitude-filter ENRICHMENT:** 81-83% of cross-boundary labels pass the >=2-tick
  magnitude filter (pass fractions 0.83 / 0.83 / 0.823 / 0.812 by horizon) vs an overall
  baseline of 0.0-1.0% (0.000 / 0.001 / 0.004 / 0.010) — gap-spanning labels are massively
  enriched in the magnitude-filtered training/evaluation population.
- **Re-anchor same-day variant:** intra-day >60 s gaps produce same-day gap-spanning pairs
  — 34 / 61 / 158 / 255 pairs by horizon, worst span 30m45s (h=60,
  0 days 00:30:45.369966846); concentrated on the re-anchor day 2025-01-09 (per-gap and
  per-horizon detail recorded in `v2\reanchor_gaps.csv`).

Evidence: `t3\day_edge_table.csv` lines 2-5 (all columns above); `t3\day_edge_samples.csv`.

## §B. Fixture lattice provenance and generation (item N2) — declaration facts

The element-level statements live in §2 (`bar_duration`) and §3 (`timestamp_semantics`). This
section is the consolidated declaration record, because these facts bear on every count in
Part II and on what a "clean" instrument-month means.

**B.1 — The enumeration.** Every `{inst}_snapshots_{month}.parquet` copy under the read-only
archive was enumerated by exhaustive `os.walk`: **228 files**, 100% accounted for, none skipped,
each with size, mtime, sha256, md5, manifest coverage, total and filtered row counts, and block
structure. **Every manifest-covered file MATCHES its recorded md5; zero MISMATCH across all 228.**
Evidence: `n2\lattice_provenance.csv` (228 rows), `n2\provenance_notes.md`, `n2\inventory_run.log`.

**B.2 — The fixture reads generation `v3_pre_gapfill`, for all 48 fixture instrument-months.**
`phase5_ml.py` L104-106 `get_data_dir` prefers `C:\MBO_data\{sym}`; that directory does not
exist on this machine, so the path falls through to
`processed\{inst}\{inst}_snapshots_{month}.parquet`. **Declaration caveat, recorded:** the
fixture path is **machine-conditional** — L106 would silently switch the entire lattice to
`C:\MBO_data\{sym}\` on any machine where that directory exists. The generation identification
is valid for this machine, where it is absent.

**B.3 — MIXED GENERATION ACROSS INSTRUMENTS.** This is the fact most likely to be misread, so
it is stated in both directions:

| instruments | fixture-path generation | a v4 generation exists? | manifest coverage of the fixture file |
|---|---|---|---|
| **he, le** (12 of 48) | v3_pre_gapfill | **No** — one generation on disk | **COVERED, MATCH** (`PC2_TRANSFER_v4\manifest.csv` L128-139, L152-163) |
| cl, es, gc, nq, zc, zs (36 of 48) | v3_pre_gapfill | **Yes, and it is the canonical one** | **NOT COVERED by any manifest at that path** |

For he and le the fixture file *is* the canonical v4-package file (archive `PC2_SETUP_README.txt`,
verbatim: "he/ 24 files (v3 canonical; no reprocessing)" and the same line for le). For the other
six the fixture file is the generation the archive itself superseded —
`MASTER_FINDINGS\v4\G2_G3_summary.txt` records "G2: 72/72 (instrument, month) cells reprocessed
successfully (NQ + ZS + ZC + ES + CL + GC, each 12 months)". **36 of the 48 fixture-path files
are covered by no manifest**; for gc, nq, zc and zs a byte-identical copy under `transfer\data\`
is manifest-covered (transitively attested, 24 files), and **for cl and es no manifest covers the
v3 generation at all** — their integrity rests solely on the sha256/md5 recorded in
`n2\lattice_provenance.csv`. Evidence: `n2\provenance_notes.md` §(e).

**B.4 — The lattice is not a 1 Hz grid on 18 of 48 instrument-months**, root cause the
unsorted, non-deduplicated per-day concatenation at `process_mbo.py` L584-590 (quoted verbatim
in §3), with the day-end and gap-re-anchor hypotheses REFUTED by measurement (25 of 211,450 =
**0.012%** on ZC 2025-08) and up to **5 rows sharing one exact ns timestamp**. Every one of the
36 v4 files is single-block and clean with exact 1 Hz totals (378,000 / 680,400 / 604,800 /
324,000 / ...). Evidence: `n2\provenance_notes.md` §(c); `n2\block_overlap.csv`;
`n2\spacing_classification.csv`.

**B.5 — Why this is a declaration fact and not trivia.** The 18 non-1 Hz instrument-months are
exactly the 18 in which the corrected side is non-zero (§13(b)) — same list, cl x6, gc x6,
zc 2025-08/-09/-10, zs 2025-08/-09/-10. The generation defect *is* the mechanism that makes the
corrected side CHARACTERIZED rather than clean. A reader who takes "1-second lattice" at face
value will read §13's corrected-side counts as a detector problem; they are a fixture property,
declared here.

**B.6 — Recorded raw, not interpreted:** ZC 2025-08 fixture rows sampled at
2025-08-04 14:00:00-14:00:07 carry `bid_price_1 = 412.0` above `ask_price_1 = 409.5` (crossed
book); `MASTER_FINDINGS\v4\G2_G3_summary.txt` records the v4 gap-fill reprocessing as taking the
ZC afternoon negative-spread fraction from 65.81% to 2.13%. Recorded because it is a property of
the generation the fixture reads; no claim in this file rests on it.

**B.7 — STOP-AND-REPORT:** none. N2 records `stop_and_report = false`; ZC 2025-08 = 554,304
lattice rows → 554,303 corrected, exactly as M5 recorded, and ZC 2025-01 = 338,159, exactly as
M1 recorded. No contradiction with any prior measurement.

## 12. `ties` — declared value for v30a (element e; R1)

**The registered default `available` stands** (PREREG.md lines 190-197 vocabulary and
lock). Part I section 6 recorded the boundary-instant ambiguity; R1 resolves it for this
draft (provisional until the tag is signed). The declaration reports contaminated-side
counts under BOTH branches so the choice is fully auditable:

Both-branch counts below are **ZC 2025-01, contaminated side** (the instrument-month of §14);
the same two columns exist for all 96 side x instrument-month cells in `n1\declared_map.csv`.

- **Strict counts — violations under EITHER branch:** the strictly-after counts of
  section 14 (trades_all 89,568; trades_large 23,633; mbo_all 254,315; per-class detail in
  the table cited below).
- **Exactly-equal events — violations ONLY under `ties: unavailable`:** 49 month-wide =
  20 trade events + 29 MBO events (per-class equal counts: trades_all 20, trades_large 20,
  mbo_bid_add 1, mbo_ask_add 4, mbo_bid_cancel 23, mbo_ask_cancel 22, mbo_cancel_any 24,
  mbo_all 29; sub-classes overlap — the month-wide totals are the trades_all/mbo_all
  values).

**The 49 exactly-equal events are NON-VIOLATIONS under the declared branch, and they enter no
detection denominator.** Under `ties: available` a cell with `a(j,c) == d(i)` is available.
The 49 (20 trade + 29 MBO, ZC 2025-01) therefore do not violate, are not required findings, are
not eligible findings, and do not appear in the criterion-1 denominator, the eligibility
denominators of PREREG.md §7.4, or any rate. A detector that fires on one of them has produced a
**false positive** under the declared branch. They are published only as the both-branch
disclosure above, which is **informational** (§D.1): it exists so that a reader can see exactly
what the tie choice moved, and it may not be re-scored as findings without changing the tie
declaration, which is class C after the tag.

**PRIMARY artifact for contaminated `decision_T`: T1.** `t1\violation_table.csv`, columns
`strictly_after_count` and `equal_count`, contaminated `decision_T` rows. Reproduced
independently and exactly by `n1\declared_map.csv` (contaminated / zc / 2025-01 rows) and by
`m5\per_instrument_counts.csv`.

**C4 is NOT a cross-confirmation of these numbers, and the earlier draft's "confirmed by
`c4\independent_counts.csv`" is corrected here.** `c4\independent_counts.csv` **contains no
contaminated rows at all** — its two boundaries are `decision_T` and `prev_row_B`, both computed
on the CORRECTED frame (`total_rows` = 338,158 on every row). Its `prev_row_B` figures are the
**lag-image** of the contaminated `decision_T` figures (§10), and they **differ by exactly 1 on
every MBO class** — mbo_all 254,314 vs 254,315, mbo_bid_add 164,958 vs 164,959, mbo_ask_add
162,753 vs 162,754, mbo_bid_cancel 135,980 vs 135,981, mbo_ask_cancel 129,333 vs 129,334,
mbo_cancel_any 179,856 vs 179,857 — for the structural reason given in §10 (the last row's
indicator has no successor row to carry it). The trades classes agree exactly (89,568 and
23,633) because their final row is not a violating row. **Any citation of C4 against a
contaminated count must carry the "contaminated-minus-1" qualifier**; without it the two
artifacts appear to disagree, and they do not.

## 13. The DECLARED GROUND-TRUTH MAP (element f; R9) — the corrected side is CHARACTERIZED, never clean

**This section replaces the former "corrected-side zero".** That claim was falsified by
measurement (subsection (f)); working resolution R9 (file tail, verbatim) is the authority for
what stands in its place: "The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on
both fixture sides, not against an assumed-clean corrected side."

### (a) What the map is, and where it lives

**Artifact: `n1\declared_map.csv`.** One row per scored cell, schema
`side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag,
missing_path`. Read this pass: **984 rows** = **960 declared-class cells** (2 sides x 8
instruments x 6 months x 10 classes) **plus 24 rows carrying the 11th diagnostic class**
`mbo_all_rows`. Of the 960: **888 `SCORED`** and **72 `UNSCORED_FOR_LACK_OF_DATA`**; the 24
diagnostic rows are flagged `SCORED_DIAGNOSTIC_11TH_CLASS`. Boundary is `decision_T` on every
row. Scope: 8 instruments (cl, es, gc, he, le, nq, zc, zs) x 6 months (2025-01, 2025-08,
2025-09, 2025-10, 2025-11, 2025-12) = 48 instrument-months.

**The declared 10 classes** are trades_all, trades_buy, trades_sell, trades_large, mbo_all,
mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any.

> **CLASS-SET RULE, binding.** `mbo_all_rows` is an **11th diagnostic class and is NOT one of
> the declared 10.** Any statement of the form "max across classes" in this file or in any gate
> report **must name the class set it maximises over.** Two M5-quoted maxima came from the
> diagnostic class and differ from the declared-10 maximum: **cl 2025-01 corrected strict —
> 54,341 over the M5 class set (`mbo_all_rows`) vs 53,249 over the declared 10 (`mbo_all`)**;
> **es 2025-01 corrected equal — 6 over the M5 class set (`mbo_all_rows`) vs 4 over the declared
> 10 (`mbo_all`)**. Both are the same measurement reported over different class sets, not a
> disagreement: `n1\compare_to_m5_output.txt` records **453 of 453 M5 cells matched, 0
> disagreeing cells, 0 quoted-maxima disagreements** once the class set is named. Companion
> artifact: `n1\m5_maxima_comparison.csv` (columns `s10`/`e10` = declared-10, `sM5`/`eM5` = M5
> class set).

Companion artifacts: `n1\summary_corrected.csv`, `n1\summary_contaminated.csv` (per
instrument-month maxima over the declared 10, with `rows` and `max_strict_frac`),
`n1\lattice_profile.csv` (per instrument-month lattice profile), `n1\unscored_ledger.csv`
(the 72 unscored cells), `n1\full_map_all_boundaries.csv`, `n1\run_logs.json`.

### (b) The corrected side, stated honestly

**The corrected side carries strictly-post-decision absorption in 18 of the 48
instrument-months** (`n1\summary_corrected.csv`, `max_strict` > 0): **cl all 6 months, gc all 6
months, zc 2025-08/-09/-10, zs 2025-08/-09/-10**. Peak: **zc 2025-09, 111,334 strict of 580,944
corrected rows = 19.16%** (`max_strict_frac` 0.191643) on class `mbo_all`. Next: zc 2025-10
109,332 of 634,445 (17.23%); zc 2025-08 90,868 of 554,303 (16.39%); zs 2025-08 64,404 of 465,381
(13.84%); gc 2025-10 71,584 of 772,447 (9.27%).

**Equal counts, stated precisely:** `equal_count` is non-zero in **35 of 48** instrument-months;
of those, **17 are equal-only** (equal > 0 with strict == 0) and the other 18 are the
strict-positive cells above. That leaves **13 instrument-months clean on BOTH branches**
(strict == 0 and equal == 0 over the declared 10). 18 + 17 + 13 = 48.

**The 13 both-branch-clean instrument-months, named:**

| instrument-month | corrected rows | note |
|---|---|---|
| nq 2025-01 | 598,227 | **TRADES-ONLY — 6 of its 10 classes are UNSCORED** |
| nq 2025-08 | 540,530 | **TRADES-ONLY — 6 classes UNSCORED** |
| nq 2025-09 | 549,430 | **TRADES-ONLY — 6 classes UNSCORED** |
| nq 2025-10 | 590,785 | **TRADES-ONLY — 6 classes UNSCORED** |
| nq 2025-11 | 550,463 | **TRADES-ONLY — 6 classes UNSCORED** |
| nq 2025-12 | 620,107 | **TRADES-ONLY — 6 classes UNSCORED** |
| zc 2025-01 | 338,158 | all 10 classes scored (see (e)) |
| zc 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-01 | 337,844 | all 10 classes scored |
| zs 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-12 | 353,103 | all 10 classes scored |
| he 2025-11 | 304,486 | all 10 classes scored |
| le 2025-11 | 304,491 | all 10 classes scored |

> **The six nq cells are NOT evidence of cleanliness.** `n1\summary_corrected.csv` records
> `classes_scored = 4` for every nq month: nq is **TRADES-ONLY**, because no
> `processed\nq\nq_mbo_{month}.parquet` exists in the archive
> (`n1\unscored_ledger.csv`, `missing_path` column, 6 rows, 12 cells each). Its six MBO classes
> are **UNSCORED, not zero.** Reading "nq is clean" off this table is exactly the inference R9
> forbids.

### (c) The contaminated side is saturated — all 48

`n1\summary_contaminated.csv`: **`max_strict` > 0 in all 48 instrument-months**, with
`max_strict_frac` from **0.2545** (le 2025-11, 77,483 of 304,492) to **0.9893** (es 2025-12,
613,447 of 620,108) — i.e. between roughly 25% and 99% of rows. By instrument:
es **0.960-0.989**, nq **0.830-0.908**, gc 0.667-0.837, cl 0.592-0.706, zc 0.538-0.752,
zs 0.583-0.637, he 0.288-0.391, le 0.254-0.417. `classes_strict_gt0` is 9 of 10 on every non-nq
instrument-month (trades_buy is dead-zero — §C.4(a)) and 3 of 4 on nq. The two sides are
therefore separated everywhere in the map by one to three orders of magnitude, which is what
makes the fixture a discrimination fixture at all.

### (d) The cohort predicate (item N3) — necessary, NOT sufficient

**`floor(T_i) == floor(T_{i-1})`** — row `i` shares a wall-clock second with its predecessor.

**Coverage: 5,305,430 of 5,305,430 corrected strict violations — 100.000%, with ZERO
exceptions.** `n3\predicate_check.csv` (456 scored cells), summed this pass: `strict_viol` =
5,305,430, `same_second_viol` = 5,305,430, `exception_viol` = 0. `n3\exceptions.csv` is a
header line with no rows. `n3\invariants.txt` records both invariants — `same_second_viol <=
cohort_size` and `strict == same_second + exception` — violated in **0 cells**. (That total is
over the 11-class set including `mbo_all_rows`; the per-class breakdown is in
`n3\invariants.txt`.)

**NECESSARY, NOT SUFFICIENT — stated as a limit, not a hedge.** The cohort is **1,966,088 rows
of 24,768,472 corrected rows (7.94%)**; a lower bound on how many cohort rows actually violate
in some class is **1,024,196** (`n3\converse_by_instrument_month.csv`, column
`LOWERBOUND_cohort_rows_violating_in_some_class`, summed over 48 instrument-months), leaving up
to **941,892** cohort rows that violate in no class (`UPPERBOUND_cohort_rows_violating_in_no_class`).
So membership in the cohort does not imply a violation; **non-membership does imply no
violation.** Outside the cohort the headroom is strictly negative in every measured cell — the
tightest are zs 2025-08 mbo_all at **−3 ns** and le 2025-11 mbo_all at **−5 ns**
(`max_ts_event_minus_T_outside_cohort_ns`), i.e. the absorbed window ends before the decision
time by nanoseconds, but it does end before it.

**The predicate is checkable from the lattice alone — no event data.** It reads only the
`timestamp` column of the snapshot frame. That is what makes it usable as a **declared cohort
definition** in §C rather than as a post-hoc description. `n3\cohort_profile.csv` also records
**0 non-monotonic rows and 0 floor-decreasing rows** across all 48 instrument-months, so the
cohort is well-defined everywhere. Cross-checks: `n3\compare_output.txt` — 456 of 456 cells
matched against `n1\declared_map.csv` with 0 disagreements; 151 of 151 matched against M5 with 0
disagreements; 48 of 48 instrument-months agreeing on `cohort_size`/`corrected_rows`.

### (e) The ZC 2025-01 zero survives — as ONE CELL of the map, with its pedigree intact

**Scoped claim: on ZC 2025-01 the corrected side is 0 strict + 0 equal against decision time,
for all 10 event classes, over all 338,158 corrected rows — including all 28 re-anchor gap
rows.** (Lattice 338,159 rows, generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` — §2 naming rule.) This cell
is measured by TWO independent implementations with exact agreement at every count:

- **T1 (pandas):** `t1\violation_table.csv` (`corrected` / `decision_T` rows: strict=0,
  equal=0 for every class); gap-row restriction all zeros for all 10 classes
  (`t1\t1_final_output.txt` line 19).
- **C4 (polars 1.43.2, blind):** T1's implementation and outputs unread; no target numbers
  in the tasking; the 338,159-row lattice independently derived from the snapshots parquet
  plus the builder filter definition (exact row match); a second internal cross-check
  method (event-level join) agreed exactly. `c4\independent_counts.csv` (`decision_T`
  rows: strict_count=0, equal_count=0, gap_row_subset_strict=0, gap_row_subset_equal=0 for
  all 10 classes).

Orchestrator comparison: no disagreement at any published count; no stop-and-report
condition (`R2_consolidated_report.md` C4 section). N1 and M5 both reproduce the cell exactly.

**The pedigree is unchanged; only its SCOPE is.** What it licenses is a statement about one
cell — and the mechanism is now understood: ZC 2025-01's lattice is a **single native block with
0 overlapping block pairs and 0 excess rows** (§B.4), so its same-second cohort is **empty**
(`n1\lattice_profile.csv`: `same_second_rows` = 0; `n3\cohort_profile.csv`: `cohort_size` = 0),
and by (d)'s predicate an empty cohort forces zero violations. The cell is clean *because of a
generation property of that month's file*, not because the lag fix is universally sufficient.
Extending it to the corrected side as a whole was the error M5 caught.

### (f) The M5 falsification sweep — cited per K3 as the measurement that forced R9

`m5\` is the round that extended the corrected-side check beyond ZC 2025-01 and **falsified**
it. What it measured: the same strict/equal violation counts at boundary `decision_T`, on both
sides, for 16 instrument-months (8 instruments x 2025-01 and 2025-08), over the per-class event
sets, with per-instrument logs and a spot-check verification of individual violating rows.
Artifacts: `m5\per_instrument_counts.csv` and `m5\per_instrument_counts_detail.csv` (the cell
counts), `m5\corrected_decisionT_summary.csv` (the headline — the table on which cl 2025-01
first showed corrected strict 54,341 and zc 2025-08 showed 90,868), `m5\counts_{inst}_{month}.csv`
and `m5\log_{inst}_{month}.json` (per-cell), `m5\verify_violating_rows.py` /
`m5\verify_violating_rows_output.txt` / `m5\spot_check.txt` (row-level verification: a named
cl 2025-01 trades_all row at T_i = 2025-01-02 13:01:11.865879 absorbing a trade at
13:01:11.914518, **48,638,830 ns after the decision time**), `m5\verify_zc_vs_c4.txt` (the ZC
2025-01 cell re-verified against C4). Its stop-and-report is preserved as evidence, per K3.

N1 supersedes M5 in coverage (48 instrument-months vs 16, both sides, with unscored cells
ledgered) and **reproduces every one of M5's 453 cells exactly** — 0 disagreements
(`n1\compare_to_m5_output.txt`). M5 is not superseded as the *reason*: it is the measurement
that made R9 necessary, and it is cited as such.

### (g) The 72 unscored cells are UNSCORED — never clean

**72 of the 960 declared-class cells are `UNSCORED_FOR_LACK_OF_DATA`**: nq's 6 MBO classes
(mbo_all, mbo_ask_add, mbo_ask_cancel, mbo_bid_add, mbo_bid_cancel, mbo_cancel_any) x 6 months
x 2 sides = 72. Cause: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\nq_mbo_{month}.parquet`
does not exist — the `missing_path` column names the exact absent file for each
(`n1\unscored_ledger.csv`, 6 rows, `n_cells` = 12 each).

**Gate consequence, declared:** an unscored cell **requires no finding and forbids none**. It
enters no denominator, contributes to no rate, and **cannot be reported as a pass**. A gate
report that counts the 72 as "clean" — or that quietly folds them into a corrected-side
cleanliness statement — has converted absence of data into evidence, which is the failure mode
R9's rationale names ("silence and belief never convert into a pass"). Whenever nq appears in
any table in this file or in any gate output, it must carry the **TRADES-ONLY** label.

## §C. Two-sided ground-truth enumeration — the criterion-1 violation set, side-relative and post-lag

**Everything in this section is stated POST-LAG** — about the value actually FED to the model at
row `t`, not about the raw construction. On the contaminated side the fed value is the row's own
construction; on the corrected side it is the row `t-1` construction (`phase7_l2_sim.py` line
276). And **everything is stated SIDE-RELATIVELY**: the same column name is a violation on one
side and, on the other side, a violation only on a declared cohort. There is no side-independent
list of leaking columns in this fixture, and writing one would be a category error.

**The comparator, pinned.** Under PREREG.md lines 190-193 the comparator evaluates
`a(j,c) <= d(i)` with `a` the **`at_source_timestamp` truth** — for the join families below,
`ts_floor + 1s`, the instant the wall-clock-second aggregate completes. The
**`at_bar_close` role recorded in §4 and in the T2 addendum is an APPROXIMATION only**: it names
where the value sits on the lattice, not when it became knowable. **`at_bar_close` is never
scored against.** Any gate arithmetic that used `at_bar_close` as the availability instant for a
join-family column would score the fixture against the wrong comparator and would find the
contaminated side clean.

### C.1 — Contaminated side: the ts_floor-overhang family, BY COLUMN

**Mechanism (one sentence, from §3):** `phase5_ml.py` line 222 floors the snapshot stamp to
`ts_floor`; line 230 and the MBO loader floor the event stamps the same way; the merges at
lines 248 (trades) and 273 (MBO) therefore attach to row `T` an aggregate over
`[floor(T), floor(T)+1s)` — a window whose true availability instant is `floor(T)+1s`, which
lies strictly after `T` whenever the row's stamp sits inside the second rather than at its end.
Every column built from those merged aggregates inherits the violation.

**(A) Trade-derived columns — Phase 5 45-column set** (`phase5_ml.py` lines 237-258, merge line
248). Violating post-lag on the contaminated side wherever the map's `trades_*` classes are
non-zero:

| Column | Construction line | Map class that governs it |
|---|---|---|
| `net_delta_1s`, `net_delta_5s`, `net_delta_10s`, `net_delta_30s`, `net_delta_60s` | L253, rolling sums of merged `net_delta` | `trades_all` |
| `sell_volume_10s` | L255 | `trades_sell` (≡ `trades_all` here — every trade classifies sell, §15) |
| `trade_count_10s` | L256 | `trades_all` |
| `large_trade_count_10s` | L257 | `trades_large` |
| `vwap_distance` | L258 `(mid - snap["vwap"]) / tick` | `trades_all` for the `vwap` term; **additionally a same-row mid read** — see C.3 |
| `buy_volume_10s` | L254 | **EXCLUDED from the denominator — see C.4(a)** |

**(B) Trade-derived columns — Phase 7 35-column set** (`phase7_l2_sim.py`, groupby lines
216-226, merge line 231, assignment lines 246-248): `trade_volume_1s`, `trade_count_1s`,
`dollar_volume_1s`. Same mechanism, same `trades_all` governance, same `ts_floor` source column.
**This is the set the gate actually scores** (§8, §A.2): the fixture pair is the Phase 7
stored-prediction pair under R3's 35-column assumption.

**(C) MBO-derived columns — Phase 5 45-column set only** (`phase5_ml.py` lines 267-285, merge
line 273): `bid_add_rate_5s`, `bid_add_rate_10s`, `ask_add_rate_5s`, `ask_add_rate_10s`,
`bid_cancel_rate_5s`, `bid_cancel_rate_10s`, `ask_cancel_rate_5s`, `ask_cancel_rate_10s`,
`cancel_ratio_asymmetry`, `order_flow_accel` (via the intermediate `event_rate_10s`, L284-285).
Governed by the map's `mbo_bid_add` / `mbo_ask_add` / `mbo_bid_cancel` / `mbo_ask_cancel` /
`mbo_cancel_any` / `mbo_all` classes.

> **Scope note that must not be dropped: Phase 7 feeds NO MBO columns.** All ten of the
> MBO-derived columns above are DROPPED from `ALL_L2_FEATURES` (§4's Phase 7 difference
> paragraph), and `phase7_l2_sim.py` reads no MBO data at all
> (`R2_consolidated_report.md` C2 section). The map's six `mbo_*` classes therefore characterise
> the **fixture's MBO event stream against the lattice** — they are the sharpest available
> measurement of the overhang, and they are what a 45-column reading would be scored on — but
> they bear on criterion 1 for the declared 35-column fixture only indirectly. Reporting an
> `mbo_*` map cell as a required finding on a Phase 7 column would be an attribution error.

### C.2 — Corrected side: the SAME column family, on the same-second cohort ONLY

Post-lag, the corrected row `t` carries the row `t-1` construction, whose absorbed window is
`[floor(t-1), floor(t-1)+1s)`. That window ends at or before `t` — **unless `t` and `t-1` share
a wall-clock second**, in which case the absorbed window is the decision row's OWN second and
extends past `t`.

**DECLARED COHORT DEFINITION (item N3):**

> **Cohort(`i`) ⟺ `floor(T_i) == floor(T_{i-1})`** — row `i` and its predecessor share a
> wall-clock second, evaluated on the filtered lattice `timestamp` column alone.

**Status: NECESSARY, NOT SUFFICIENT — declared as such.** Numbers (§13(d)): the predicate covers
**5,305,430 of 5,305,430** corrected strict violations, **100.000%, zero exceptions**
(`n3\predicate_check.csv`; `n3\exceptions.csv` is an empty header; `n3\invariants.txt` records 0
cells violating either invariant). But the cohort is **1,966,088 rows of 24,768,472 corrected
rows (7.94%)**, and at most **1,024,196** of them are known to violate in some class, leaving up
to **941,892** cohort rows that violate in none. So:

- **In-cohort ⇒ a violation is POSSIBLE, and must be adjudicated against the map cell.**
- **Out-of-cohort ⇒ NO violation, on any class, in any measured cell** — headroom is strictly
  negative everywhere; the tightest measured are −3 ns (zs 2025-08 mbo_all) and −5 ns
  (le 2025-11 mbo_all).

**The violating column family on the corrected side is exactly C.1's family** — the same
trade-derived and MBO-derived join columns, no others — restricted to cohort rows. The per-cell
counts are the `side = corrected` rows of `n1\declared_map.csv`. The 18 non-zero
instrument-months are named in §13(b), and they are exactly the 18 whose lattice is not a 1 Hz
grid (§B.5).

**Why this is checkable before any detector runs:** the cohort predicate reads only the lattice
`timestamp` column — no event data, no trades parquet, no MBO parquet. A reviewer can regenerate
the cohort from the snapshot file alone and confirm the declared restriction.

### C.3 — Same-row book reads: availability-LEGAL at the boundary, and OUT of this gate's jurisdiction

The columns that read the decision row's OWN snapshot book and nothing else —
`spread_ticks`, `bid_size_1`, `ask_size_1`, `l1_imbalance`, `total_bid_depth`,
`total_ask_depth`, `depth_imbalance`, `book_slope_bid`, `book_slope_ask`,
`depth_change_{1,5,30}s`, `depth_pctile_{60,300}s`, `mid_return_{1,5,10,30,60,300}s`,
`volatility_{30,300}s`, `range_{60,300}s`, and the Phase-7 additions `tick_direction`,
`weighted_mid`, `book_imbalance_ratio` — are **DECLARED AVAILABILITY-LEGAL at the boundary
instant.**

Basis: **R1's `ties: available`** (registered default, PREREG.md lines 190-197). A snapshot
stamped `T` contains events strictly before `T` (§3, `process_mbo.py` 354-363), so such a cell's
information content is realized before `T` while its stamp equals `T`; with `d(i) = T`,
`a = T <= d = T` admits it. **These columns are not availability violations on either side, and
a finding on one of them is a false positive** — under criterion 2 on the contaminated side and
under the amended criterion 3 on the corrected side.

**Their label-base character is a real property, and it is assigned elsewhere.** `tick_direction`
(reads `mid(t)`, the label base), `vwap_distance` and `weighted_mid` (both of the
`(X - mid)/tick` form) sit at `mid(t)`, which is exactly what `fwd_move_ticks_*` measures FROM
(`phase5_ml.py` lines 216-219; `phase5_audit.py` line 101, verbatim: "The label predicts
direction FROM mid[t]."). **That character is assigned to L2a jurisdiction and is OUTSIDE this
availability gate.** This declaration neither scores it nor denies it: it is not an availability
question under the declared tie branch, and routing it here would let a label-base finding
masquerade as an availability finding, corrupting both counts. (Note the asymmetry R1 accepts:
under `ties: available` the fixture's standing as an availability-violation exemplar rests on the
C.1/C.2 join families, not on the shift(1) absence per se — Part I §6 states the same thing from
the other direction.)

### C.4 — Column-level gate dispositions, declared before any run

**(a) `buy_volume_10s` — EXCLUDED from the criterion-1 denominator. Degenerate constant.**
`phase5_ml.py` line 231 `is_buy = trades["aggressor_side"].isin(["B","Buy","buy"])` matches none
of the actual parquet values (BUY_AGGRESSOR / SELL_AGGRESSOR / UNKNOWN; `isin` is exact
case-sensitive equality), so line 234 `trades["buy_vol"] = np.where(is_buy, trades["size"], 0)`
is identically 0 and line 254's rolling sum is identically 0. Same defect at
`phase7_l2_sim.py` line 207 (§15). Independently visible in the map: the **`trades_buy` class is
0 strict and 0 equal in every one of its 96 cells, on BOTH sides** (`n3\predicate_check.csv`
per-class total `trades_buy` `strict_viol` = 0 over 48 cells; `n1\declared_map.csv` `trades_buy`
rows). **A dead-zero column cannot carry an availability finding for an availability reason**,
and leaving it in the denominator would make criterion 1 unsatisfiable for a reason unrelated to
detection. It is declared out, before any run, and must be named in the gate report as EXCLUDED
rather than as MISSED.

**(b) Session-flag staleness — a DOCUMENTED QUIRK. It licenses NO corrected-side finding.**
`session_open`, `session_mid`, `session_close` (and their parent `minutes_since_open`) are
deterministic clock functions with column_role `always`, yet they are not in `EXEMPT_COLS`
(`phase7_l2_sim.py` line 266), so line 276 lags them: the FED session flag at row `t` is the
row `t-1` flag (T2 addendum, "Recorded quirk"). This is **staleness, not unavailability** — a
value from the past is always available, and the comparator asks whether a cell was knowable by
`d(i)`, which a `t-1` clock flag trivially was. **Declared: this quirk licenses NO finding on
`session_open` / `session_mid` / `session_close` on the corrected side**; a detector that reports
one has produced a false positive under the amended criterion 3. Recorded as a documented
as-built property so it cannot later be re-read as a discovery.

**(c) `book_imbalance_ratio` — lag discrepancy UNRESOLVED; gate status EXCLUDED.**
T4 records that the fixture build's `book_imbalance` column is a raw snapshot-parquet
pass-through whose construction cannot be verified equivalent from the fixture code, and that
**its lag treatment differs — lag-exempt in the corrected build vs lagged in `phase7_l2_sim.py`**
(§17 item 6; `t4\fixture_manifest_35col_DRAFT.json`, `unconstructible_columns`). Nothing in this
spike resolves which treatment the stored predictions were produced under. **The discrepancy is
recorded as UNRESOLVED and the column's gate status is EXCLUDED** — which costs nothing, since
it is already one of the 7 UNCONSTRUCTIBLE columns of the 28-column projection. It enters no
denominator on either side, and no finding on it counts for or against any criterion. If it is
ever reinstated the lag question must be resolved first, and reinstatement changes the
criterion-1 denominator — class C.

**Summary of declared exclusions:** `buy_volume_10s` (degenerate constant) and
`book_imbalance_ratio` (unresolved lag, already unconstructible). Everything else enumerated in
C.1 and C.2 is IN. The exclusions are declared here, pre-run, and are frozen at the tag by §D.1.

## 14. Contaminated-side violation profile (element g; T1 headline)

**Scope: ZC 2025-01 only** — lattice **338,159 rows** = `processed\zc\zc_snapshots_2025-01.parquet`
under UTC hours [14,19), generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` (md5
`ea2eee6136896b5f8a5b7ddc052f589c`) — §2's naming rule; this is NOT the v4_gapfill generation,
which is 378,000 rows under the same filter. The other 47 instrument-months are in §13's map.

On the contaminated (pre-fix) side, measured against decision time `T` over 338,159 rows:

- **Strictly-post-decision absorption on 26.49% of rows** for the trades-all classes
  (89,568/338,159) — all trade-derived columns except the dead-zero buy_volume family
  (net_delta and its 1/5/10/30/60 s rollups, trade_count, trade_volume, sell_volume,
  sell_volume_10s, trade_count_10s, vwap, vwap_distance).
- Large-trade class: 6.99% (23,633/338,159).
- MBO classes: 38.2-75.2% — ask_cancels 38.25%, bid_cancels 40.21%, ask_adds 48.13%,
  bid_adds 48.78%, cancel_any 53.19%, and the total_events family 75.21%
  (254,315/338,159).
- Worst overhang past `T`: 999.999579 ms (MBO ask_cancel / total_events family). Mean
  overhang among violating rows: **per-class means 506.3-655.2 ms; trades_all 519.8,
  mbo_all 655.2** (`v1\mean_overhang_by_class.csv`, column `mean_overhang_ms`: trades_large
  506.273305 is the minimum, mbo_all 655.194723 the maximum, trades_all 519.797439; medians in
  the same file run 513.5-727.9 ms).
- **Stamp-type concentration — MEASURED, not inferred (M4).** 95.04% of in-hours row stamps are
  integral-second (321,384 of 338,159 rows with `T == floor(T)`; 16,775 mid-second). The
  violations do not merely "concentrate" there — **at least 99.98% of all violations sit on
  integral stamps, on every class that has any**: `share_of_viol_on_integral` runs from
  0.999807 (mbo_all, the minimum) to 1.0 (trades_large), i.e. **≥99.98%** (trades_buy is
  excluded from the range because it has zero violations — §C.4(a)). Per-row rates by stamp
  type: **trades_all 27.87% on integral stamps vs 0.012% on mid-second stamps** (89,566/321,384
  vs 2/16,775; rate ratio 2337.5x) and **mbo_all 79.12% vs 0.29%** (254,266/321,384 vs
  49/16,775; rate ratio 270.9x). The mechanism is exactly the one §3 predicts: the joined
  wall-clock second extends furthest past `T` precisely when `T` sits on the second boundary, so
  a mid-second stamp has almost no window left to overhang. The bucketed view bears that out —
  16,201 of the 16,775 mid-second rows have ≤1 ms of second remaining, and both of trades_all's
  mid-second violations plus 26 of mbo_all's 49 fall in that `(0,1] ms` bucket (the other 23 in
  `(500,750]` and `(750,999]`). M4's counts reproduce T1's totals exactly
  (`strict_total_matches_t1` and `equal_total_matches_t1` both True on all 10 classes) under two
  independent estimators with `row_disagreements=0`. Evidence:
  `m4\stamp_type_breakdown.csv`; `m4\viol_rate_by_remaining_time.csv`.

Evidence: `t1\violation_table.csv` (contaminated `decision_T` rows, `frac` and
`worst_overhang_ms` columns); `t1\t1_final_output.txt` lines 2-13 (lattice profile incl.
the 321,384 / 16,775 stamp split) and lines 22-52 (per-class summary).

## 15. As-built defects — fixture-level facts (element h; R4; C5-DECIDED-WRAPPED)

**Two as-built defects are properties of the FIXTURE ITSELF, present in BOTH pipeline
generations:**

1. **Aggressor classifier:** `is_buy = trades["aggressor_side"].isin(["B", "Buy", "buy"])`
   matches NONE of the actual parquet values (SELL_AGGRESSOR / BUY_AGGRESSOR / UNKNOWN;
   `isin` is exact case-sensitive equality), so every trade is classified sell.
   - Phase 5 builder: archive `pc2_transfer\scripts\phase5\phase5_ml.py` lines 230-233
     (ts_floor line 230; is_buy lines 231-232; signed_vol line 233).
   - Phase 7: `results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py` lines 207 (is_buy)
     and 209 (signed_vol) — byte-identical mechanism (whitespace-only difference in the
     is_buy line).
2. **Uncast uint32 negation:** `np.where(is_buy, trades["size"], -trades["size"])` with no
   cast before negation, in both files; on a uint32 `size` column the negation wraps modulo
   2^32 in the measured rebuild environment (observed value 4294967291 for size 5).

**C1 verdict: INHERITED** — the classifier defect was active in the ORIGINAL Phase 5 runs,
by three independent chains with no conflicts: (i) run-window
`pc2_transfer\transfer\checksums.txt` MD5s (mtime 2026-04-07, in-window) match the current
zc snapshots and trades_tagged parquets exactly; (ii) the original ZC run log —
**`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase5_fixed\gpu_track2_log.txt`**
(31,638 bytes, mtime 2026-04-08, in-window; path verified this pass) — records the 338,159
feature-row fingerprint that the current snapshots parquet reproduces exactly today, that count
being the **v3_pre_gapfill** ZC 2025-01 lattice under UTC hours [14,19) per §2's naming rule and
NOT the 378,000-row v4_gapfill generation; (iii) every
aggressor-tagging writer that ever existed in the archive emits only
BUY_AGGRESSOR/SELL_AGGRESSOR/UNKNOWN, so `isin(["B","Buy","buy"])` could never have matched
any pipeline product.

**The 7 affected fixture columns (of the 35):** net_delta_1s, net_delta_5s, net_delta_10s,
net_delta_30s, net_delta_60s (corrupted if wrapped), buy_volume_10s (dead-zero),
sell_volume_10s (redundant with total volume).

**Claims split per R4:**

- **Timing-structural — SUPPORTED:** event-to-row timing, the overhang counts
  (sections 10 and 14), and the per-cell counts of the declared ground-truth map (section 13).
  These do not depend on the numeric values the defective columns carry. (R4's own wording,
  frozen at the tail, says "the corrected-side zero"; that phrase named what section 13 held at
  the time R4 was recorded. Under R9 the referent is the map, of which the ZC 2025-01 zero is
  one cell — §13(e). The split R4 draws is unaffected.)
- **Value-dependent — QUALIFIED:** any claim about the numeric content of the 7 columns
  (magnitudes, signs, deltas) is conditional on the wrap question below.

**C5 — DECIDED (post-assembly update, 2026-08-10, orchestrator; source
`R2_consolidated_report.md` C5 section and `c5\env_records.md`).** C5 decided exactly one
thing: whether the ORIGINAL 2026-04 run environment's dtype path wrapped (uint32 modular
negation) or promoted to int64, from records alone. **Verdict: DECIDABLE — the original
runs WRAPPED, identically to the f2 rebuild.** The original Phase 5 runs executed on this
machine under pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1 (pinned by the 2026-04-17 frozen-env
records plus the launcher-named install's dist-info metadata, installed 2026-02 and never
changed), making the f2 rebuild an execution witness under the exact pinned versions. The
value-dependent claims above remain QUALIFIED as to magnitude but the wrap itself is no
longer open. Either way the buy/sell sign information is absent from the 7 columns.

**Gate consequence, cross-referenced:** the wrapped values are DATA CONTENT, not findings — see
the sentinel statement in §A.9, which is what keeps criterion 4's identity control safe against
them. `buy_volume_10s`, the dead-zero column of the 7, is declared out of the criterion-1
denominator in §C.4(a).

Evidence: `c2\aggregation_comparison.md` (construct rows 1-2, degeneracy verdict,
"Which trade aggregates feed the 35-column model set" section);
`R2_consolidated_report.md` C1/C2/C5 sections; `t1\violation_table.csv` `note` column
(as-built caveats recorded per row); `t1\t1_final_output.txt` lines 61-67 (wrapped value
observed in the rebuild).

## 16. Documented-unverifiable assumptions (element i)

Assumptions the declaration RELIES ON that no archive record can verify; recorded as such:

1. **The 35-column set for the main-PC pair (R3).** The stored main-set predictions carry
   no feature manifest; the assumption that they were produced from `ALL_L2_FEATURES` (the
   35 columns of `phase7_l2_sim.py` lines 73-108) is accepted as a documented-unverifiable
   assumption. Basis: the F3 manifest cross-check — 9/9 agreement of the Phase-7-added
   columns' DAG classes against `f3\fixture_manifest_DRAFT.json` (Part I, DAG cross-check
   block inside the Phase-7-added-columns section) — and the `working_resolution_R3` line
   carried in `t4\fixture_manifest_35col_DRAFT.json`. The 9/9 agreement is on **CLASS**; the
   one FLAVOR that cross-check left open, `weighted_mid`, is settled by **R6** as
   `contemporaneous_state_flow` (PROVISIONAL until the tag; see the supersession note after the
   T2 addendum block). Flavor does not enter the class agreement and the basis is unchanged.
2. **phase7_l2_sim.py runtime inputs.** The script hardcodes the PC2 path
   (`PROJECT = Path(r"C:\Users\Research\Desktop\pc2_transfer")`, lines 32-33) and reads
   `processed\` only; what bytes that machine's copies held at run time is unconfirmable
   from the archive. **Citation corrected (item P2):** the hardcoded-path fact is
   `c2\aggregation_comparison.md` **construct row 20** ("Data source", which records
   `phase5_ml.py` L38-40 / L104-106 against `phase7_l2_sim.py` L32-33 and the verdict
   "DIFFERENT — Phase 7 hardcodes a `C:\Users\Research\...` pc2 path, reads processed/ only").
   **That file carries no blockers list**; the blockers are in `R2_consolidated_report.md`'s C2
   section, "Blockers (carried)" bullet — "actual aggressor values verified for ZC 2025-01 only;
   original-env wrap → C5; PC2 runtime reads unconfirmable from archive". The prior draft cited
   a blockers list to `c2\aggregation_comparison.md`; that cite was wrong and is replaced by
   these two.
3. **The physical `C:\MBO_data` source copies are unhashable (C1 residue).** The local
   copies the original runs physically read are gone and cannot themselves be hashed; the
   checksum chain of section 15 covers the pc2_transfer copies, not the physically read
   ones. Evidence: `R2_consolidated_report.md` C1 residual-ambiguity paragraph.

## 17. T4 — 35-column projection manifest results (element j)

Projection of the F2 fixture builds onto the 35-column Phase 7 model set, selection or
renaming only (nothing synthesized), run under R3:

- **28 of 35 columns constructible:** 26 direct name matches + 2 verified intermediate
  mappings (trade_volume_1s mapped-from `trade_volume`; trade_count_1s mapped-from
  `trade_count`).
- **7 UNCONSTRUCTIBLE, with reasons** (from `t4\fixture_manifest_35col_DRAFT.json`,
  `unconstructible_columns` entries):
  1. `tick_direction` — no column of this name or equivalent construction exists in the
     87-column build output; producing it requires applying `np.sign(...).fillna(0)` — a
     new construction, prohibited under the selection/renaming-only projection rule.
  2. `dollar_volume_1s` — no dollar-volume column or intermediate exists in the build
     output; constructing it is prohibited.
  3. `session_open` — minutes_since_open IS in the build, but the threshold transform
     (`frac < 0.1`) is a new construction, prohibited.
  4. `session_mid` — same basis as session_open (`(frac >= 0.1) & (frac < 0.85)`), new
     construction, prohibited.
  5. `session_close` — same basis as session_open (`frac >= 0.85`), new construction,
     prohibited.
  6. `book_imbalance_ratio` — the build's `book_imbalance` column is a raw snapshot-parquet
     pass-through whose construction cannot be verified equivalent from the fixture code
     (NOT mappable), and its lag treatment differs (lag-exempt in the corrected build vs
     lagged in phase7); constructing the ratio from the total depths is prohibited. **The lag
     discrepancy is recorded as UNRESOLVED and the column's gate status is EXCLUDED —
     §C.4(c).**
  7. `weighted_mid` — no such column in the build output; requires arithmetic over raw
     book columns and mid — a new construction, prohibited. (Its declared DAG flavor is
     `contemporaneous_state_flow` per **R6**, PROVISIONAL until the tag; the flavor resolution
     does not change its unconstructibility, which turns on the projection rule alone.)
- **Determinism:** run1 == run2 sha256 on BOTH sides (contaminated
  `32edf4389d9ca9435cc7923a19e0730bf409023d460b378f7acdc3cba11d719a`; corrected
  `db4193aa1ad88fa052599bf6714f2ba401bd99f52008a938a5f475280dc66245`).
- **Self-consistency:** corrected[t] == contaminated[t-1] EXACT on all 28 projected
  columns (max_abs_diff 0.0, 0 NaN-placement mismatches, 0 value mismatches), both run
  pairs; all 28 projected columns confirmed lagged (none exempt).

Evidence: `t4\fixture_manifest_35col_DRAFT.json` (counts_projected_subset,
unconstructible_columns reasons, projection_verification); `t4\t4_verification_report.json`
(aux).

## §D. Lock language — what freezes at the tag, and what may move afterwards

### D.1 — The freeze

**At the moment the `prereg-v30a` tag is signed, the following become LOCKED, and any
subsequent change to any of them is a class C amendment requiring a further amended
registration under PREREG.md line 95:**

1. **The `ties` declaration** — `available` (R1, §12). The tie branch decides what the 49
   exactly-equal ZC 2025-01 events are, and the equal counts in all 96 map cells; moving it
   after the tag would silently re-score the fixture.
2. **Every gate-consumed number in this file.** Specifically and exhaustively: the declared
   ground-truth map `n1\declared_map.csv` in its entirety (984 rows: 888 SCORED, 72
   UNSCORED_FOR_LACK_OF_DATA, 24 diagnostic); the cohort predicate and its coverage
   (§13(d), §C.2); the reference AUC trio of §A.1; the independently-leaking-source count 25 and
   its governing scope (§A.2); the criterion-1 column enumeration of §C.1 and §C.2; the declared
   exclusions of §C.4 (`buy_volume_10s`, `book_imbalance_ratio`); the fixture identity and the
   pc2 exclusion (§8); the boundary `floor(t-1)+1s` (§1).
3. **The class-set rule of §13(a)** — that `mbo_all_rows` is diagnostic and not one of the
   declared 10, and that any "max across classes" names its class set.

**Both-branch counts are INFORMATIONAL ONLY.** The `ties: unavailable` figures published in §12
and the `equal_count` column of the map exist so that the tie choice is auditable. They are not
a second scoring, not an alternative gate, and not a fallback. **No gate outcome may be computed
from them**, and reporting a pass or fail under the non-declared branch is out of specification.

**Consequence of PREREG.md line 480's locked ordering** ("Defaults may not be altered after
observing a fixture result"): every number listed above must be final before the first gate run.
A number discovered to be wrong after a fixture result has been observed is not corrected in
place — it goes through PREREG.md line 99's route: recorded, amended registration committed, and
the affected benchmark regenerated as a new version under §6.4 with the superseded results
published alongside.

### D.2 — The v30a tag message carries SIX hashes

The `prereg-v30` tag message carries **five** SHA-256 lines — read this pass from the repository
(`git tag -l -n50 prereg-v30`), verbatim block:

```
f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6  PREREG.md
039240e3c57497cc8eda65fbfcdc3d1120f1d7a12ad0f41b48d71c98ef063428  DESIGN.md
e8cf5bbbc42762838318e2ffc8cf85b6f44ed701c3ee88f8e93a6e734fc43e0d  HISTORY.md
72ffc7c69899844644ff79a9f6a12b083bbbe2c1160aca8d90dbe9415a0322e2  tools/check_registration.py
215194c15ab89f208198ce6bc3f8dd726d652fa6bee3d7bd868d1234c9bec31a  protocol/runtime_reference.py
```

**DECLARED: the `prereg-v30a` tag message carries SIX hashes — those five, inherited and
recomputed at their v30a state, PLUS the SHA-256 of this availability-declaration file itself.**

Basis, cited rather than asserted (the two assertions of working resolution R7):

- **The five-hash inheritance.** R7 records that the v30a tag carries all five hashes, "matching
  the prereg-v30 tag as executed", and that §0.2.1's "both" is a stale count predating
  `HISTORY.md` and the tooling files joining the block. **Cite for the executed state:** the tag
  message block quoted verbatim above, read from the repository this pass — five SHA-256 lines
  covering `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `tools/check_registration.py`,
  `protocol/runtime_reference.py`.
- **The governing clause.** **Cite: PREREG.md line 97** (verbatim): "**An amendment inherits
  §11's integrity chain in full:** signed tag, both file hashes in the tag message, external
  timestamp receipt committed, repository publicly reachable at lock. An amendment weaker than
  the thing it amends is not one." R7's reading — that "both" is the stale count and the
  executed five govern — follows from that final sentence, and is recorded by R7 as a class A
  mechanical fact requiring no locked-file edit.

**Why the sixth.** This file is the reconstructed availability declaration PREREG.md line 447
requires, and under the amended criterion 3 it carries the ground-truth map the gate scores
against. A tag that hashes the specification but not the declaration the specification is
evaluated under would be an integrity chain with a hole exactly where the amendment lives — and
"an amendment weaker than the thing it amends is not one". The sixth hash closes it.

**Lock-time obligations arising elsewhere in this file, listed so none is lost:**
(i) add the contamination availability class as a named field to the governing manifest (§A.3);
(ii) produce or formally defer the CI sliced variant (§A.4).

### D.3 — Interpretation rule for decision-log entries

The working-resolution record at this file's tail is an interpretation ledger over locked text.
It is bounded:

> **A decision-log interpretation of locked text may resolve ONLY toward the STRONGER reading.
> Any interpretation that weakens a locked obligation — narrows a denominator, exempts a column,
> softens a criterion, admits an excluded set, converts a required finding into an optional one,
> or converts an unscored cell into a pass — is a class C amendment and may not be recorded as a
> working resolution.**

This is what R7 already does in the small (reading "both" as the executed five, not as a licence
to publish two) and what R9 does in the large (replacing an unsatisfiable criterion with a
scored map rather than with a waiver). Stated as a rule so that the next entry cannot do the
opposite by precedent. The tail's existing entries R1-R9 are frozen byte-identical; this rule
governs anything appended after them.

## §E. Gate protocol input surface — what a detector receives, and what it never receives

**At gate time a detector receives exactly two things, for ONE SIDE AT A TIME:**

1. **the feature pipeline** for that side, and
2. **the availability declaration** (this file's declared elements: §1 `decision_time`,
   §2 `bar_duration`, §3 `timestamp_semantics`, §4 + T2 `column_roles`, §5 `label_availability`,
   §12 `ties`, §7's remaining elements).

**Nothing else. In particular, a detector NEVER receives, at any point in a gate run:**

- **the paired side** — a run on `fixture_contaminated` is given no access to
  `fixture_corrected`, and vice versa. Differencing the two sides would let a detector
  reconstruct the answer without ever reasoning about availability;
- **the other side's stored predictions**, in whole or in part, nor any statistic derived from
  them (including the AUCs of §A.1);
- **the declared ground-truth map** (`n1\declared_map.csv`), nor any summary, cohort list, or
  per-cell count derived from it — including the cohort predicate of §C.2, the 18-of-48 list of
  §13(b), and the unscored ledger of §13(g).

**Why the map in particular must be withheld.** Under the amended criterion 3 the map IS the
scoring key. A detector that could read it would be graded against a key it had seen, and the
gate would measure retrieval rather than discrimination. The map is an artifact of the harness,
not an input to the tool.

**Corollary — one side at a time is a hard sequencing rule, not a convention.** The gate's
criteria are per-side (criterion 2 on `fixture_contaminated`, the amended criterion 3 on
`fixture_corrected`, criterion 4 on both), and each is evaluated from a run that saw only its own
side. A single run given both sides does not satisfy any of them, however its outputs are
partitioned afterwards.

## §F. Method notes

**F.1 — Grep undercount on archive-wide surveys. Archive-wide surveys MUST use a filesystem
walk.** Measured this pass on the same question and the same archive root
(`C:\Users\ttbea\OneDrive\Desktop\MBO_2025`), searching `*.py` for
`aggressor_side|is_buy_aggressor`:

| method | files found |
|---|---|
| default-excluded content search (respecting ignore rules) | **37** |
| exhaustive `os.walk` over the archive root | **119** |

The walk figure is `c1\tagger_survey_capture.txt` line 17 ("files with >=1 mention: 119"; header
records "total *.py scanned: 460", "total mention lines: 472", "total WRITER lines: 152", scope
"every *.py under the archive root, recursive"). The 37 figure was produced this pass by running
the default-excluded search directly. **The default-excluded search missed 82 of 119 files —
69%.**

**Consequence, declared as a method rule:** any claim in this file of the form "every X in the
archive" — most importantly §15's chain (iii), "every aggressor-tagging writer that ever existed
in the archive emits only BUY_AGGRESSOR/SELL_AGGRESSOR/UNKNOWN" — rests on a filesystem walk and
must not be re-verified with a default-excluded search. A negative result from such a search is
not evidence of absence in this archive. The same rule produced N2's 228-file snapshot inventory
(`n2\provenance_notes.md`: "enumerated by exhaustive `os.walk`: **228 files**, 100% accounted
for, none skipped").

**F.2 — Numbers in this file.** Every number written in this pass was read from a named artifact
opened in this pass, or computed from such an artifact by an arithmetic stated at the point of
use. Where two artifacts report the same quantity, the PRIMARY one is named (§10's table).
Where a quantity depends on a class set, a side, a boundary, or a lattice generation, all of
those are named at the point of use — that is the standing requirement of §13(a)'s class-set
rule and §2's generation-naming rule.

## 18. Element-to-evidence index (v30a assembly)

Covers **every** element and **every** section of this file, including the sections added by
item P2. Lettered elements are the v30a assembly elements; lettered SECTIONS are §A-§F.

**Part I — schema elements (the reconstruction):**

| El. | Content | Section | Primary evidence |
|---|---|---|---|
| 1 | `decision_time` — DECLARED boundary `floor(t-1)+1s`, stated ONCE | 1 | §10 measurement (t1\violation_table.csv 4, 67; c4\independent_counts.csv 3, 11); phase7_l2_sim.py 276, 819; historical claim preregistration_v4.txt 303-304 |
| 2 | `bar_duration` — 1 s emitter + anchoring/gap caveats + N2 generation facts | 2 | process_mbo.py 322, 331, 342, 347-352, 358, 367; n2\provenance_notes.md (a)(b)(d)(e); n2\lattice_provenance.csv; n1\lattice_profile.csv |
| 3 | `timestamp_semantics` — bar-close boundary; ts_floor misalignment; N2 root cause | 3 | process_mbo.py 354-363 and 584-590; phase5_ml.py 222, 230, 248, 273; n2\provenance_notes.md (c); n2\block_overlap.csv; n2\spacing_classification.csv |
| 4 | `column_roles` — 45-set roles; Phase 7 delta; T2 addendum (FROZEN); R6 flavor | 4 + T2 block + supersession note | phase5_ml.py 60-80, 183-298; phase7_l2_sim.py 73-108; f3\fixture_manifest_DRAFT.json; d1\pre_t2_block.txt (md5 d4dd09b939540bdc2db33a2e13cb049e) |
| 5 | `label_availability` — AMENDED to POSITIONAL; 2,100 cross-boundary rows; M3 caveats | 5 | phase5_ml.py 90, 190, 216-219, 679; phase5_audit.py 101; t3\day_edge_table.csv 2-5; m3\zero_tick_evidence.md §§1-5, §7, §8 |
| 6 | `ties` — the boundary ambiguity as measured (resolved in §12 by R1) | 6 | process_mbo.py 354-363; PREREG.md 190-197, 411; preregistration_v4.txt 303 |
| 7 | Remaining schema elements (`availability_fn`, scopes, `embargo`) | 7 | PREREG.md 210; no archive evidence for embargo |

**Part II — v30a assembly elements and the P2 sections:**

| El. | Content | Section | Primary evidence |
|---|---|---|---|
| — | **§6.2 conformance walk, element by element** | **§A** | PREREG.md 443-481 (quoted verbatim per element); PREREG.md 93, 95, 97; f1\f1_results.csv 50-52, 114-116; f3\fixture_manifest_DRAFT.json counts; t4\fixture_manifest_35col_DRAFT.json counts_projected_subset; n1\summary_corrected.csv; t1\t1_final_output.txt 61-67 |
| a | Fixture identity; RE-EVALUATE from the stored predictions; reference AUCs; pc2 exclusion HARDENED | 8 | results\phase7{,_fixed}\l2_predictions\ (64 parquets each; columns pred_score/true_label/fwd_move_ticks/mid_price_t); f1\f1_results.csv; c3\label_equality.csv; c3\pc2_diff_summary.csv; f5\DEVIATIONS_entry_SKELETON.md 40-48 |
| b | Shared label vector — the feature-availability-only licence | 9 | c3\label_equality.csv 2-65 |
| c | **EVIDENCE for §1's boundary**; PRIMARY/cross-check table; off-by-one reconciliation; lag-image | 10 | t1\violation_table.csv 4, 67 (PRIMARY); c4\independent_counts.csv 3, 11; n1\lattice_profile.csv; n3\cohort_profile.csv; v1\mean_overhang_by_class.csv |
| d | Session-tail label semantics | 11 | t3\day_edge_table.csv 2-5; t3\day_edge_samples.csv; v2\reanchor_gaps.csv |
| — | **Fixture lattice provenance and generation** | **§B** | n2\lattice_provenance.csv (228 files); n2\provenance_notes.md (a)-(e); n2\block_overlap.csv; PC2_SETUP_README.txt; MASTER_FINDINGS\v4\G2_G3_summary.txt |
| e | `ties: available` (R1); both-branch counts INFORMATIONAL; 49 equal events are NON-VIOLATIONS; T1 PRIMARY and the contaminated-minus-1 qualifier on C4 | 12 | t1\violation_table.csv equal_count (PRIMARY); n1\declared_map.csv; m5\per_instrument_counts.csv; c4\independent_counts.csv (prev_row_B, lag-image, −1 on MBO classes) |
| f | **The DECLARED GROUND-TRUTH MAP (R9)** — 984 rows; 18/48 corrected non-zero; 13 both-branch-clean; contaminated saturation; N3 predicate; ZC 2025-01 cell + pedigree; M5; 72 unscored | 13 | n1\declared_map.csv; n1\summary_corrected.csv; n1\summary_contaminated.csv; n1\lattice_profile.csv; n1\unscored_ledger.csv; n1\m5_maxima_comparison.csv; n1\compare_to_m5_output.txt; n3\predicate_check.csv; n3\invariants.txt; n3\exceptions.csv; n3\converse_by_instrument_month.csv; n3\compare_output.txt; m5\ (whole round); t1\violation_table.csv; c4\independent_counts.csv; t1\t1_final_output.txt 19 |
| — | **Two-sided ground-truth enumeration; comparator pinned to at_source; column dispositions** | **§C** | phase5_ml.py 222, 230-235, 237-258, 267-285; phase7_l2_sim.py 207, 216-231, 246-248, 266, 276; n1\declared_map.csv; n3\predicate_check.csv; n3\converse_by_instrument_month.csv; PREREG.md 190-197; t4\fixture_manifest_35col_DRAFT.json |
| g | Contaminated-side profile; overhang means 506.3-655.2 ms; M4 stamp-type concentration | 14 | t1\violation_table.csv; t1\t1_final_output.txt 2-13, 22-52; v1\mean_overhang_by_class.csv; m4\stamp_type_breakdown.csv; m4\viol_rate_by_remaining_time.csv |
| h | As-built defects, INHERITED, R4 split, **C5-DECIDED-WRAPPED** | 15 | c2\aggregation_comparison.md; R2_consolidated_report.md C1/C2/C5; c5\env_records.md; t1\violation_table.csv note; t1\t1_final_output.txt 61-67; results\phase5_fixed\gpu_track2_log.txt |
| i | Documented-unverifiable assumptions (cite for item 2 CORRECTED) | 16 | f3\fixture_manifest_DRAFT.json (via Part I cross-check); c2\aggregation_comparison.md construct row 20; R2_consolidated_report.md C2 "Blockers (carried)" and C1 residual paragraph |
| j | T4 35-column projection results | 17 | t4\fixture_manifest_35col_DRAFT.json; t4\t4_verification_report.json |
| — | **Lock language: freeze, six hashes, interpretation rule** | **§D** | prereg-v30 tag message (five SHA-256 lines, read this pass); PREREG.md 97, 95, 99, 480; n1\declared_map.csv |
| — | **Gate protocol input surface** | **§E** | this declaration's declared elements; n1\declared_map.csv named as withheld |
| — | **Method notes: Grep undercount; numbers discipline** | **§F** | c1\tagger_survey_capture.txt line 17 (119 by os.walk) vs 37 by default-excluded search, measured this pass; n2\provenance_notes.md (228-file walk) |
| k | Working-resolution record **R1-R9**, verbatim | file tail | this file (frozen byte-identical; the tail heading occurs exactly once, and the tail runs unbroken to EOF) |

---

## Decision log — working resolutions (DELTA R2, 2026-08-10; PROVISIONAL until the prereg-v30a tag is signed)

Recorded here per DELTA R2 instruction; NOT in any locked file. Verbatim from the delta:

- **R1. ties:** registered default `available` stands. The declaration reports contaminated-side counts under both branches (strict counts plus the 49 exactly-equal events).
- **R2. boundary:** the declaration states the measured boundary floor(t−1)+1s as the true information boundary of the corrected features. The t−1 wording is retired as a claim and kept only as the historical contract text that was violated.
- **R3. 35-column:** accepted as a documented-unverifiable assumption (basis: F3 manifest 9/9 agreement). T4 is unblocked by this.
- **R4. as-built defects (buy classifier, uint32 wrap):** recorded as documented as-built behavior. f2-backed claims split into timing-structural (supported — event-to-row timing, overhang counts, the corrected-side zero) vs value-dependent (qualified).
- **R5. weighted_mid:** still AMBIGUOUS-PENDING-AUTHOR. Leave the T2 addendum block untouched.

### Working resolutions — DELTA R5 (2026-08-11; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R6 supersedes R5's pending status for the weighted_mid FLAVOR (the T2 addendum block itself remains untouched as the measurement record):

- **R6. weighted_mid flavor:** contemporaneous_state_flow. Basis: the information-content test — mid is (bid1+ask1)/2, computed from the same cells lines 184–186 already read, so the (X−mid)/tick form adds no information; substance matches book_slope, not vwap_distance. Record the counter-reading (form-match with line 187) as considered and rejected.
- **R7. hash-count:** the v30a tag message carries ALL FIVE hashes, matching the prereg-v30 tag as executed. Governing clause: "an amendment weaker than the thing it amends is not one." Record as a class A mechanical fact that §0.2.1's "both" is a stale count predating HISTORY.md and the tooling files joining the block. No locked-file edit.
- **R8. H-entry:** standard main-series form — `### H-34 — from PREREG.md §0.2.1` — with the entry text noting it is a class C amendment, the first post-tag entry. Addendum form rejected: H-nn is an open ledger and an amendment is a first-class event in it.

### Working resolution — DELTA R7 (2026-08-11; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R9 responds to the M5 falsification sweep (the corrected-side zero does not extend beyond ZC 2025-01); that sweep and its stop-and-report are preserved as evidence per K3:

- **R9.** The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on both fixture sides, not against an assumed-clean corrected side. §6.2 criterion 3 is amended within this class C registration: old — no findings on any corrected column; new — detector findings must match the declared per-side, per-class, per-instrument-month violation map; findings the map predicts are required, findings it excludes are false positives, cells the map does not cover are unscored. The corrected side is described throughout as CHARACTERIZED, never clean. Rationale recorded: the tool's own coverage principle (silence and belief never convert into a pass) applied to its own exam.

### Working resolutions — DELTA R9 (2026-08-12; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R11 resolves the criterion-1 denominator contradiction found by the P2 verifier; R12 corrects the NQ coverage claim; R13 governs the weighted_mid manifest disagreement:

- **R11.** Criterion-1 denominator derives from the DECLARED MAP, not from the manifest's construction classes. The manifest's leak-source classification is provenance context with no gate arithmetic attached. Three-way, mutually exclusive, enumerated BY NAME from the map artifact (never as a residue or a count):
  - **REQUIRED** — columns the map declares violating on the scored side under the declared branch (the forward-join / ts_floor overhang family). A correct detector must fire on each.
  - **OUT OF JURISDICTION** — columns declared availability-legal at boundary under R1 (the same-row book reads of §C.3). An availability-class finding on them is a false positive; a label-base finding on them belongs to L2a and is neither credited nor penalized by this gate. §C.3's "routes to criterion 2" is deleted — it had no landing site (PREREG line 460 scopes criterion 2 to manifest-clean columns).
  - **UNSCORED** — degenerate constants (buy_volume_10s), unconstructibles, and map-uncovered cells.

  N = the REQUIRED count, stated as the enumerated list plus its length, with the §D.1 freeze re-derived accordingly.
- **R12.** NQ MBO: NOT gate-scored, with the reason restated correctly — "no same-generation MBO data: the available NQ MBO is v4_gapfill; the fixture lattice is v3_pre_gapfill" — never "no data exists." NQ's coverage is restated as trade-classes-only; its "clean on both branches" advertisement is withdrawn as a pass claim. The cross-generation measurement runs as a declared NON-GATED DIAGNOSTIC (X4) so the information exists; moving it into the acceptance denominator later is class C.
- **R13.** weighted_mid: the f3 manifest is NOT edited. Evidence artifacts are never adjusted toward a decision. The declaration records the disagreement explicitly — manifest records label_base_price as of its date; R6 provisionally resolves contemporaneous_state_flow; the declaration's operative value is R6's, and the manifest field is superseded for this column only. §A.2's split is stated both ways: 7/18 per manifest, 6/19 under R6.
