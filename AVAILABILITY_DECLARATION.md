# AvailabilityModel declaration — fixture reconstruction

## LINE REFERENCES IN THIS FILE AND IN THE TAG MESSAGE — WHICH REGISTRATION VERSION THEY MEAN (R95/§146.2)

**Unqualified `PREREG.md` line numbers in records predating 25 August 2026 are v30 line numbers.**
A line reference written before the v30a amendment was applied refers to the registration version
current at that record's date, and is **correct as history**. The v30a amendment inserted 981 lines
after `PREREG.md` line 99, so **every v30 line number above 99 differs from its v30a position** —
`git show prereg-v30:PREREG.md` recovers the registered v30 text byte-exact and is where such a
reference resolves.

**THIS FRAME REACHES THE `prereg-v30a` TAG MESSAGE, and says so here because the tag message
cannot say it itself.** The tag message's own summary line cites `PREREG.md` §6.2 by line —
reference AUC at l.445, the contamination availability class recording locus at l.450, the sliced CI
variant at l.451, criterion 3 at l.461. **Those are v30 line numbers.** In the amended file they land
on a table rule, a blank line, and prose about something else, so a reader who resolves them against
the file the tag ships is reading the wrong lines and gets no warning.

The tag message's format is fixed by the ceremony and is not edited to carry a caveat, so the frame
is stated here instead — in a file the same tag hashes, which is what makes this statement as
firmly attested as the message it qualifies. **`git show prereg-v30:PREREG.md` is where those four
references resolve.**

**They are deliberately NOT renumbered.** Renumbering a dated record falsifies what was cited when,
which is the one thing the record exists to preserve. Where this file quotes registered text, it
quotes it verbatim beside the line number, so a reader can verify the quotation against the tag
without needing the number to resolve in the current file.

## STATUS — REGISTERED, AND OPERATIVE AT THE `prereg-v30a` TAG

**This file is the availability declaration `PREREG.md` §6.2 requires, and it is registered.**
Its SHA-256 is enumerated in the `prereg-v30a` tag message, §D.1's list freezes at that tag, and
`PREREG.md` SC-7(a) names its **declared elements** as one of the two things a detector receives
at gate time. SC-8(f) names it the file that **carries the scoring key**.

**What its earlier status said, and why it is corrected rather than retained.** Until the v30a
amendment was assembled this file read *"Status: DRAFT. Nothing in this file is a registered
declaration."* That was true when written: the file was then a reconstruction awaiting review,
and no tag enumerated it. **It stopped being true when the amendment made this file a hashed,
frozen object that registered clauses read from, and it was not updated.** A status marker is a
claim about the file's standing, so a stale one is a false statement inside the signed object —
not a stale description of something else. Correcting it is the only disposition available:
a disclosure elsewhere cannot repair a claim the tag itself attests.

**Every element below is still a reconstruction from archive evidence**, assembled by item F4 of
"Phase 0 addendum 2: fixture verification for v30a". Registered and reconstructed are not
opposites: what is registered is that these are the declared elements, with the provenance each
one states.

**Section-level markers are NOT claims about this file's standing, and are deliberately left as
they are.** Part I's `AMBIGUOUS-PENDING-AUTHOR` entries record elements the measurement genuinely
did not resolve; where a working resolution later resolved one — `ties`, Part I section 6, carried
in Part II §12 and frozen at §D.1 item 1 — **the resolution governs and Part I stands as the
measurement record.** The Phase-7-added-columns block (T2) and the working-resolution record at
the file tail are **frozen byte-identical** (l.89-93). Rewriting a dated record to look current
falsifies what was known when, which is the one thing those records exist to preserve.

**`PROVISIONAL until the prereg-v30a tag is signed` is a different marker and is untouched.** It
is a forward-looking condition, true as written, and discharged by the signing itself rather than
by an edit.

Assembly status (item D1, "Phase 0 addendum 3: pre-amendment closure checks", 2026-08-11):
this file is now the complete v30a declaration DRAFT. **Part I is NOT unchanged, and the
earlier claim that it was is withdrawn here.** Part I (sections 1-7 and the evidence-class
table) began as the F4 reconstruction and has since been amended in place, in five sections,
by the P2 pass (2026-08-12) and by this X-round correction pass (2026-08-12):
**§1** — the declared boundary now states the measured `floor(t-1) + 1s`;
**§2** — the N2 generation caveats, the non-1 Hz finding, and the M1/N2 generation-naming
rule, **plus (2026-08-12, post-PRE_R9) the single-block PRECISION FIX** that replaced "the other
30 are single-block and clean" with the measured split **30 = 7 zero-excess + 23 carrying 1-17
filtered excess rows**, and the two-count labelling of the 1 Hz failure (**18 of 48 multi-block /
41 of 48 excess-carrying**); **§3** — the N2 root-cause block (the unsorted per-day
concatenation), **plus (2026-08-12, post-PRE_R9) the v4 PRECISION FIX** that replaced "every one
of the 36 v4 files is single-block and clean" with **36 single-block = 12 zero-excess + 24
carrying 1-5**; both fixes rest on `n2\block_overlap.csv` and are recorded here because the
standing "which Part I sections were amended" statement must be complete. **Neither is a change
made by the R11-batch pass**, whose "amends NO Part I section" statement below therefore stands;
**§4** — the sentence recording R6's weighted_mid flavor resolution;
**§5** — the positional `label_availability` declaration and the gate-treatment block for the
2,100 cross-boundary rows. **Every other section of Part I stands as the F4 measurement
record and is unamended.** Part II (inserted after the evidence-class table) assembles the
v30a declaration under working resolutions R1-R9 and R11-R13 (there is no R10), recorded
verbatim at the file tail.

**This R11-batch pass (2026-08-12), under the DELTA-ISSUED working resolutions R14-R17 and on
the evidence of item Y1, changes five things and amends NO Part I section:** it rewrites the
header's **Fixture paragraph** below (the pre-fix side of the stored pair is not a 45-column
MBO-reading build); it adds **Part II §0**, the two-artifact disambiguation, and tags every
measurement section with the artifact it rests on; it adds **§13(i)**, publishing both maps side
by side per R17(ii) with the R17(iii) check; it adds **§13(j)**, the standing of the six `mbo_*`
classes after Y1; and it rewrites **§C.3's scope passage** into four independently-derived
categories, retiring the 27-column list as a class claim. R14-R17 are **not** appended to the
tail — that record is frozen — and are cited by number as delta-issued authority (Part II
preamble).

**The SYMMETRY pass that follows it (2026-08-13, delta-issued items S1-S4, operating under R17
and on the same Y1 evidence) changes four things and again amends NO Part I section:** it
restates **§14** with both profiles side by side — the full-class profile AS MEASURED and the
fed-column-restricted one — because Y1's premise is side-independent and §14's published
headline was an `mbo_*` figure, and adds **§14.1**, the 48-cell contaminated table that places
that cell in its distribution; it adds **§A.6.5**, cross-tabulating the Y1 SOURCE partition
against the R11 GATE partition column by column; it adds **§C.5**, the `vwap_distance`
dual-ground statement, cross-referenced from §A.6.1; and it adds **§F.3**, the all-zero control.
**The headline consequence, stated at the top because it is a number falling:** restricted to the
columns the fixture actually feeds, §14's contaminated headline for ZC 2025-01 is **26.49%, not
the 75.21% previously published** — a smaller honest number replacing a larger one. S1-S4 are
**not** appended to the tail either, for the same reason.

**Where the boundary rule lives — stated here so the locator is not read backwards.**
**Part I §1 is the single normative statement of the information boundary
`floor(t-1) + 1s` in this file.** §10 is its EVIDENCE section and states no rule; Part II
carries no competing statement of the boundary and no working resolution restates it. R2 is
the authority for §1 stating the *measured* boundary rather than the historical "through time
t-1" contract text, which survives in §1 only as the quoted claim that measurement violated.
Where Part I genuinely left an element AMBIGUOUS-PENDING-AUTHOR — `ties`, Part I section 6 —
a working resolution carries the draft declaration in Part II (§12) and Part I stands as the
measurement record. The Phase-7-added-columns block (T2) and the working-resolution record at
the file tail (now R1-R9 plus R11-R13) are frozen byte-identical by this item and by every
item after it, this one included.

Editor pass (item P2, "v30a availability-declaration draft", 2026-08-12). Three things this
pass changes at the top level, stated here once:

1. **The declared boundary is the measured one.** §1's DECLARED value now states the
   information boundary `floor(t-1) + 1s` as the normative contract. It is stated in §1 and
   nowhere else; §10 is its evidence section. The historical "through time t-1" contract text
   survives only as the quoted claim that measurement violated.
2. **The gate scores against a declared ground-truth map on BOTH sides** — `PREREG.md` §6.2
   criterion 3 as amended [SC-3], cited and not restated; working resolution R9 (verbatim at
   the file tail) is the record of its adoption for this fixture. The corrected side is
   described throughout as **CHARACTERIZED, never clean** (SC-3(g)). §13 is that map; §C
   enumerates it side-relatively; §A walks PREREG.md §6.2 element by element and marks each
   SATISFIED or AMENDED.
3. **weighted_mid FLAVOR is RESOLVED** — `contemporaneous_state_flow`, by working resolution
   R6, PROVISIONAL until the prereg-v30a tag is signed. R5's pending status is superseded. The
   frozen T2 addendum block still reads AMBIGUOUS-PENDING-AUTHOR because it is the measurement
   record and is not edited; R6 governs, and the note immediately following that block records
   the supersession.

**Numbering convention adopted by this pass:** new Part II sections are letter-numbered
(**§A - §F**, plus **§0**, the two-artifact section placed before §A by the later R11-batch
pass); the pre-existing numeric sections 8-18 are **not** renumbered, so every
cross-reference written before this pass stays valid. New primary sources for this pass are
the N1 declared map (`n1\`), the N3 cohort predicate (`n3\`), and the N2 lattice-provenance
round (`n2\`); the M5 falsification sweep (`m5\`) is cited as the measurement that forced R9.

Schema source (normative, read-only): PREREG.md §2.3 (`AvailabilityModel` table, lines
199-212), §2.4 (`label_availability`, lines 218-225), comparator table lines 190-193, and
§2.9 [SC-1] (what a reconstructed declaration fixes, and what it may not leave open — the
schema every Part I element below supplies data under), at
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`.

Fixture: Phase 5/7 ZC pipeline, archive `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only).

**The fixture the gate scores is the STORED PREDICTION PAIR** — `results\phase7\l2_predictions\`
(pre-fix) against `results\phase7_fixed\l2_predictions\` (post-fix), 64 parquets each (§8).
**Both of its sides are phase7-family `l2_` outputs over ONE 35-column, MBO-free column universe**
(working resolution R3), so neither side is a 45-column MBO-reading build.

**The earlier wording of this paragraph is CORRECTED here.** It read "Pre-fix side =
`phase5_ml.py` `build_features_month()`" against "Post-fix side = `phase7_l2_sim.py`". That
names the **Phase 5 → Phase 7 LINEAGE**, not the two sides of the stored pair, and reading it as
the pair's two sides asserts a 45-column MBO-reading pre-fix side that the archive does not
support — the pre-fix stored side is itself an `l2_` output whose own methodology note says "no
MBO data" (item Y1 §4.4; §0 below states the evidence and its limit). The lineage is unchanged
and still governs the construction citations throughout Part I:

- `pc2_transfer\scripts\phase5\phase5_ml.py` `build_features_month()` (lines 174-298; no shift(1)
  anywhere in phase5 — established in prior spike) is the 45-column, MBO-reading builder of the
  lineage. Its lattice and its `ts_floor` event joins are what every timing measurement in this
  file is taken against.
- `results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py` line 276
  `snap[feature_cols] = snap[feature_cols].shift(1)` is the universal lag, and its 35-column,
  MBO-free scope (`ALL_L2_FEATURES`, lines 73-108) is the column universe the gate's fixture
  inherits under R3.

**Which artifact carries which claim is set out in Part II §0, and every measurement section is
tagged there and in place.** This paragraph is the file's header, not a Part I section; Part I
§§1-7 are unamended by this pass.

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

This is the MEASURED boundary of the corrected (post-fix) features. It is declared as the
measured value, with the documented (intended) value recorded beside it below and the artifact
each was read from named — the form `PREREG.md` §2.9 SC-1(a) (measured, not intended) requires;
the rule is cited, not restated. The corrected row stamped `t` carries the
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
- **THE 1 Hz CLAIM FAILS ON THE DELIVERED FILE, AND IT FAILS ON TWO DIFFERENT COUNTS THAT MUST
  NEVER BE INTERCHANGED: 18 OF 48 INSTRUMENT-MONTHS ARE MULTI-BLOCK** (`native_blocks` > 1 with
  `overlapping_block_pairs` > 0 — overlapping native blocks), **AND 41 OF 48 CARRY FILTERED
  EXCESS ROWS** (`filtered_excess_rows` > 0 — not an exact 1 Hz grid); only **7 of 48** carry
  zero excess. "fixed, 1 second" describes the
  *emitter*, not the delivered file. On cl (all 6 months), gc (all 6), zc (2025-08/-09/-10) and
  zs (2025-08/-09/-10) the delivered lattice carries up to **5 rows sharing one exact
  nanosecond timestamp**. **The other 30 are all single-block (`native_blocks == 1`,
  `overlapping_block_pairs == 0`), but only 7 of them carry ZERO filtered excess rows** — he
  2025-11, le 2025-11, zc 2025-01, zc 2025-11, zs 2025-01, zs 2025-11, zs 2025-12. **The
  remaining 23 carry 1-17 filtered excess rows, with at most 2 rows sharing one second**
  (`n2\block_overlap.csv`, columns `filtered_excess_rows` and
  `filtered_max_rows_per_second`; max 17 at he 2025-10). "Single-block" and "zero excess" are
  therefore not the same predicate, and §3 states the correlation in its precise form —
  single-block ⟺ *negligible* excess, not zero excess. **THE TWO CRITERIA, RECONCILED IN ONE
  SENTENCE so they cannot be conflated:** MULTI-BLOCK is a property of the file's ASSEMBLY
  (overlapping native blocks concatenated without sort) and EXCESS is a property of the DELIVERED
  GRID (rows beyond one per distinct second), so the **18 multi-block are a strict subset of the
  41 excess-carrying** — 18 + 23 single-block-with-excess = 41 — and the **7** zero-excess months
  (he 2025-11, le 2025-11, zc 2025-01, zc 2025-11, zs 2025-01, zs 2025-11, zs 2025-12) are the
  only fixture-path months that are exact 1 Hz grids. Root cause in §3.
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
- **Generation naming (M1/N2), as practised on every row count in this file** (the naming form
  is recorded in `PRACTICES.md` P-02; the provenance obligation it applies is `PREREG.md`
  §8.6's): the count, the path, the generation and the sha256 are named together. ZC
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
measured files with **zero exceptions**, and every one of the 36 v4 files is single-block —
12 of them with zero filtered excess rows and the other 24 with 1-5 (§B.4). So the
clean-vs-dirty split across instrument-months is neither a DST artefact nor a
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
  at 1 s. **The horizon term's UNIT is declared here as positional (rows on the filtered
  frame) — the unit statement `PREREG.md` §2.9 SC-1(d) requires of the declaration for every
  term it supplies to §2.4's registered formula. That the substitution of this unit for the
  duration reading is class C is SC-1(d)'s and the amended registration's, not this file's
  (cited, not restated).** The declared value is:

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
2. **They are IN the scored population** — a declared subclass of it, under `PREREG.md` §6.2
   SC-3(c) (the map covers the whole declared scored population; cited, not restated). All
   2,100 carry REAL label values — **zero NaN** (§11); the only NaN source in the frame is the
   month tail, exactly h rows per horizon.
3. **Findings on them are adjudicated by the declared map (§13) like any other row** — the
   disposition `PREREG.md` §6.2 SC-3(b)–(c) registers for every unit of the scored population,
   structurally awkward subclasses included (cited, not restated; working resolution R9 is the
   record of its adoption for this fixture).
4. **No separate label-availability criterion exists for them.** A declaration creates no gate
   object (`PREREG.md` §0.2.1 SC-9(a), cited); §A walks the four §6.2 criteria as amended,
   which SC-9(a) names as the whole gate.

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
- `panel_mask_scope`: global — locked by `PREREG.md` **§2.3's `panel_mask_scope` row**, not fixture-specific.
  *(Converted from a line number at R95/§146.4: this points a CURRENT reader at CURRENT text, so it must survive the next insertion. §17.2's remedy is an anchor, not a renumber.)*
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

## PART II — THE v30a ASSEMBLY (registered; see STATUS above)

Assembled by item D1 of "Phase 0 addendum 3: pre-amendment closure checks"; carried forward by
item P2 (2026-08-12) under working resolutions R6-R9, and corrected by the X-round pass
(2026-08-12) under working resolutions R11-R13. Every number below is a measurement from
a named artifact — the DELTA R2 round, the M-rounds (M3/M4/M5), or the N-rounds (N1 declared
map, N2 lattice provenance, N3 cohort predicate); nothing is re-derived here. Relative evidence
paths are under
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\`;
archive paths are under `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only). Working
resolutions **R1-R9 and R11-R13** (verbatim at the file tail; there is no R10) govern this
Part; they are PROVISIONAL until the prereg-v30a tag is signed.

> **Working resolutions R14-R17 are DELTA-ISSUED and are NOT in the tail record.** This pass
> operates under them and cites them **by number** as delta-issued authority — principally
> **R16** (`book_imbalance_ratio` carries ONE class only, §C.3 category 2) and **R17** (the
> restricted-map justification, the both-maps publication obligation, and the non-zero check,
> §13(i)). They are not appended to the decision log: the tail is an append-only record frozen
> byte-identical by this item and by every item after it, and appending to it is not this
> pass's authority. Their authority as working resolutions is `PREREG.md` §0.2.1 SC-9(d)'s
> (working-resolution authority is uniform, and supersession is ordered), cited here and not
> restated. Their status is the same as R1-R13's — PROVISIONAL until the tag is signed — and the
> interpretation rule SC-9(e) registers (see §D.3) reaches them exactly as it reaches the
> recorded ones.
>
> **The same applies to delta-issued items S1-S4**, under which the symmetry pass records
> **§14 / §14.1** (S1 — the fed-column restriction applied to the CONTAMINATED side, both
> profiles side by side with the delta explicit, and §13(j)'s forbidden-use rules restated for
> that side), **§A.6.5** (S2 — the Y1-SOURCE x R11-GATE cross-tabulation and its arithmetic
> reconciliation), **§C.5** (S3 — `vwap_distance` as the sole dual-ground column) and **§F.3**
> (S4 — the all-zero control). **S1-S4 operate under R17** and add no authority of their own
> beyond applying it symmetrically: R17(i)'s column-universe criterion is not re-argued in any of
> them, and R17(ii)'s both-maps obligation is what §14 discharges for the contaminated side.
> They are likewise **NOT appended to the tail**, are cited by number where they are exercised,
> and carry the same PROVISIONAL status.

The supersession order among these resolutions — R6 over R5's pending status, R9 over the old
"corrected-side zero", R11 over the manifest-derived criterion-1 denominator, R12 over the "no
NQ MBO data exists" claim, and §13(h)'s PREMISE CORRECTION over R12's own stated reason (on
measured evidence) — is this file's record under `PREREG.md` §0.2.1 SC-9(d) (working-resolution
authority and supersession; cited, not restated).

Carried forward from Part I into the v30a draft: `decision_time` (section 1 DECLARED value —
which now states the measured boundary `floor(t-1)+1s` and is the ONLY statement of the
boundary rule in this file; section 10 is its evidence), `bar_duration` (section 2, with the
N2 generation and non-1 Hz caveats), `timestamp_semantics` (section 3, with the N2 root cause),
`column_roles` (section 4 plus the frozen Phase-7-added-columns block, weighted_mid flavor
resolved by R6), `label_availability` (section 5, AMENDED to the positional definition), and
the section 7 remaining-elements list — subject to R1's ties resolution (section 12) below.
Part I section 6 records the ties ambiguity as measured; R1 resolves it.

## §0. THE TWO ARTIFACTS — what is MEASURED ON A, and what is SCORED ON B

**Placed first in Part II because every later section depends on it. It renumbers nothing:**
§A-§F and the numeric sections 8-18 keep their identifiers, and no cross-reference written
before this pass changes.

> *Instance data.* This section and §8 together are the fixture-composition enumeration
> `PREREG.md` §6.2 SC-2(a) requires — the artifacts that constitute the fixture, by side, with
> provenance — plus the lattice bridge between the measuring artifact and the scored one.

**The problem this section fixes.** This file contains TWO pre/post pairs, and the earlier text
slid between them — most visibly in the header's Fixture paragraph, corrected above. They are
different objects, built by different code, carrying different columns, and used for different
purposes. Neither substitutes for the other. From here on they are named.

### §0.1 — Artifact A: the f2 REBUILD pair (what timing is MEASURED ON)

**What it is.** The pre-fix and post-fix FEATURE BUILDS produced in this spike from the
`phase5_ml.py` lineage — the **45-column, MBO-READING** universe (`FULL_FEATURES`,
`phase5_ml.py` lines 60-80) — at
`...\scratchpad\fixture_spike\f2\` (`f2\phase5_ml_fixture.py`, a byte-verified copy of the
archive builder; `f2\run_fixture.py`; build outputs under `f2\out\`, named
`contaminated_zc_{month}_run{1,2}` and `corrected_zc_{month}_run{1,2}`, each with a `.pkl`, a
`.meta.json` and a `.sha256` — the two runs per side being T4's determinism check, §17).

**What it is FOR, and its only use: ground-truth measurement of event-to-row timing.** It is the
only object in this spike on which the question "which events does the row stamped `t` absorb?"
can be asked at all, because it is the only one that contains features and their event joins.
**T1** and **T4** read the f2 build outputs directly (T1's wrapped-`net_delta` observation,
`t1\t1_final_output.txt` lines 61-67, is an f2 observation; T4 projects the f2 builds onto the
35-column set). **C4, M4, M5, N1, N3** and **X4** measure on the same lineage lattice and event
parquets that the f2 build reads — the fixture-path `{inst}_snapshots_{month}.parquet`,
`{inst}_trades_tagged_{month}.parquet` and `{inst}_mbo_{month}.parquet` files (the last where it
exists; `processed\nq\` holds none, which is the whole of §13(g)), generation `v3_pre_gapfill`
(§B.2).

**What it is NOT.** It is **not** the gate's fixture. It carries no stored predictions, no AUC
the gate consumes, and no label vector the gate scores. Nothing in §6.2's four criteria is
evaluated on it.

### §0.2 — Artifact B: the FIXTURE pair (what the gate SCORES)

**What it is.** The stored per-row predictions —
`results\phase7\l2_predictions\` (pre-fix) against `results\phase7_fixed\l2_predictions\`
(post-fix), **64 parquets each**, same 64 filenames, 8 instruments x 2 architectures x 4
horizons. Column universe: the **35-column, MBO-FREE** `ALL_L2_FEATURES` set under working
resolution R3. Full identity, class and provenance: §8.

**THIS is what the gate scores.** Criteria 1-4, the reference AUC trio, the shared-label-vector
licence, and the k-of-N proof count are all statements about Artifact B.

**The structural fact that forces the split.** Artifact B stores **no feature columns**. Its
parquets carry `pred_score`, `true_label`, `fwd_move_ticks`, `mid_price_t` (schema read in §8;
Y1 §1.3 item 4 additionally lists `timestamp` from the writer at `phase7_l2_sim.py` L402-408) —
and nothing else on either enumeration. **No event-to-row timing question can be answered from
Artifact B at all.** That is not a convenience; it is why the ground truth must be measured on
Artifact A and then applied to Artifact B.

**The bridge, and what it rests on.** Artifact B's rows are rows of the same fixture-path
snapshot lattice that Artifact A is built on (§B.2, generation `v3_pre_gapfill`), so a
per-side, per-class, per-instrument-month map cell measured against that lattice indexes the
same rows the stored predictions are scored over. **That bridge rests on R3 plus §B.2's
generation identification — not on a generator script**, because both of Artifact B's
generators are absent from the archive (§0.4).

### §0.3 — Which claims rest on which

| Claim | Section | Rests on |
|---|---|---|
| Information boundary `floor(t-1) + 1s` | §1 (rule), §10 (evidence) | **A** |
| Session-tail / positional label semantics; the 2,100 cross-boundary rows | §5, §11 | **A** |
| Lattice provenance, generation, the 18-of-48 MULTI-BLOCK and 41-of-48 EXCESS findings (§B.4) | §2, §3, §B | **A** |
| The DECLARED GROUND-TRUTH MAP, all 984 rows, both sides | §13 | **A** |
| The cohort predicate `floor(T_i) == floor(T_{i-1})` and its coverage | §13(d), §C.2 | **A** |
| Contaminated-side violation profile; stamp-type concentration | §14 | **A** |
| Per-cell counts attached to columns in the two-sided enumeration | §C.1, §C.2 | **A** |
| T4 35-column projection and its self-consistency check | §17 | **A**, projected onto B's column set |
| As-built defects (aggressor classifier, uint32 wrap) | §15 | **A** as execution witness; the defect is a property of BOTH lineages |
| Fixture identity and the RE-EVALUATE class | §8 | **B** |
| Shared label vector — the feature-availability-only licence | §9 | **B** |
| Reference AUC trio (the retired anchor's replacement) | §A.1 | **B** |
| The 35-column universe whose partition is frozen | §A.6, §D.1 item 2 | **B**'s column universe under R3, classed by construction evidence from the lineage |

**Reading convention followed throughout this file** (the artifact-naming practice is recorded
in `PRACTICES.md` P-10; the provenance obligation it sharpens is `PREREG.md` §8.6's). A
measurement made on Artifact A is quoted as ground truth for Artifact B **only** through the
lattice bridge above, and names the artifact it was measured on — with one admissible third
case, stated rather than left implicit: a measurement **of the archive itself**, belonging to
neither artifact (§16's unverifiable-assumption record and §F's method measurements are the only
instances in this file, and both say so in place). Every measurement section below carries an
explicit `MEASURED ON ARTIFACT A`, `SCORED ON ARTIFACT B`, or archive-level line for exactly
this reason.

### §0.4 — The asymmetry, resolved (item Y1)

**The apparent asymmetry.** The header formerly described the fixture's pre-fix side as
`phase5_ml.py build_features_month` (45 columns, MBO-reading) and its post-fix side as
`phase7_l2_sim.py` — i.e. two sides with *different column universes*, one of which reads MBO.

**It is not an asymmetry of the fixture. It is the LINEAGE described as if it were the pair.**
Per Y1 §4.4: both sides of the stored pair are phase7-family `l2_` outputs; the pre-fix stored
side is itself an `l2_` (35-column) output, not a 45-column build. The header is rewritten
accordingly, and the lineage reading is retained there explicitly labelled as the lineage.

**The evidence that BOTH fixture sides share ONE column universe — stated with its limit.**

Positive evidence, all of it from the archive:

1. **Byte-identical methodology notes on the two sides.** `results\phase7\methodology_note.txt`
   and `results\phase7_fixed\methodology_note.txt` share SHA256
   `ea11e0ffd382167d8209259a6847234c9dd99c7345ea29e801dbc8d0ee113535`, and both open: "Phase 7
   trading simulation uses models retrained on L1+L2 features only (order book and trade flow,
   no MBO data)." (Y1 §4.2(i).)
2. **No `feature_set` column in the `l2_` family, on EITHER side.**
   `results\phase7\l2_sim_results.csv` and `results\phase7_fixed\l2_sim_results.csv` carry no
   such column — unlike the 45-set families `full_sim_results.csv`, `main_pc_results.csv` and
   `pilot_main.csv`, which all carry `feature_set` with values `Full` / `BFree`. A single
   feature set on both `l2_` sides is what a missing discriminator column implies. (Y1 §4.2(ii).)
3. **The PC2 sibling pair — the one phase7 pre/post pair whose provenance IS recorded — is
   35-column, no-MBO on BOTH sides.** `pc2_complete.txt` (pre-fix): `feature_set: L2 (35
   features, 21 L1 + 14 L2)`; `pc2_phase7_complete.txt` (post-fix): `feature_set: L1+L2 (35
   features, universal lag)`. The only difference recorded between the two is the lag.
   (Y1 §4.2(iii).)

**THE LIMIT, stated plainly and not softened: this is inference from prose and structure, NOT
from code.** **Both** stored sides were written by main-PC generators that are **ABSENT from the
archive.** The one archived phase7 script writes `f"{sym}_{arch}_{hz}_predictions_fixed.parquet"`
(`phase7_l2_sim.py` L715) — a different filename pattern from the one both stored directories
use — so **it produced neither directory**; and `find` for `*phase7*.py` over the whole archive
returns only that one file. There is therefore **no generator code for either side of Artifact
B**, and none of the three evidence items above is a feature list emitted by a generator. This
is exactly the content of working resolution R3: **documented-unverifiable** (Y1 §4.1, §4.3,
§4.4; §16 item 1). Two further gaps are recorded rather than smoothed over: no archived record
accounts for the post-fix side's CL/ES/HE/LE prediction files at all, and the pre-fix side has
64 prediction files against 63 meta rows (Y1 §4.3).

**WHY THIS MATTERS — the licence of §9 depends on it.** §9 reads the pre/post AUC delta as a
**feature-availability-only** effect. That licence is bounded by `PREREG.md` §6.2 SC-2(c) (the
pre/post licence is bounded) — cited, not restated — and the column universe is what the bound
turns on here. If
Artifact B's two sides did not share one column universe — if, say, the pre-fix side really were
a 45-column MBO-reading build — then the delta would confound a *change of columns* with a
*change of when columns are knowable*, and **the feature-availability-only licence would fail
outright**, taking §A.1's reference trio and the discrimination framing of the whole gate with
it. §9's own measurement does not rescue this: the bit-exact identity of `true_label`,
`fwd_move_ticks` and `mid_price_t` across all 64 pairs establishes a shared label vector and a
shared evaluation population, and says nothing whatever about the feature set.

**The strongest positive evidence that the two sides DO share one universe is T4's
self-consistency result:** on the projected 35-column set, **`corrected[t] == contaminated[t-1]`
EXACT on all 28 projected columns** — max_abs_diff 0.0, 0 NaN-placement mismatches, 0 value
mismatches, on both run pairs, with all 28 confirmed lagged and none exempt (§17). A pre/post
relation that is a **pure one-row positional shift on a single column set** is precisely what a
shared column universe looks like, and precisely what a changed column set could not produce.
**Its artifact tag is A, not B** — T4 measures the f2 rebuild pair — so it is evidence by
lineage, not a direct measurement on the stored pair. It is named as the strongest available
evidence, and its artifact is named with it.

## §A. Conformance walk against PREREG.md §6.2, element by element (item P2)

**First CONFORMANCE section of Part II** (§0 precedes it and renumbers nothing). Every
registered element of PREREG.md §6.2 (lines 443-481, read
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
entry standing alone." The class of every AMENDED entry below is the amended registration's to
state — `PREREG.md` §0.2.1 lines 93 and 95 and its v30a amendments block govern it; this walk
asserts nothing about class on its own authority (`PRACTICES.md` P-13).

---

### A.1 — Reference AUC anchor — **AMENDED (class C)**

> **SCORED ON ARTIFACT B** (§0.2) — the trio is recomputed from Artifact B's stored `pred_score`
> / `true_label` columns. No Artifact A number enters it.

**Registered text, PREREG.md line 445 (verbatim):**

> **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

**OLD:** the pair (0.957, 0.675) with an acceptance interval of ±0.010 absolute, as the anchor
the fixture pair must reproduce.

**NEW:** the registered pair is **retired** by the amended registration — `PREREG.md` §6.2
"Reference AUC anchor — v30a, operative", with SC-2(d) (a reference anchor is constituted by
recomputation, not by transcription); cited, not restated. What this declaration supplies under
it is the **enumerated anchor-entry set**: the recomputed ZC **LightGBM** trio, computed directly
from the stored per-row predictions of the declared fixture pair (§8):

| Horizon | Pre-fix (contaminated) | Post-fix (corrected) | n rows |
|---|---|---|---|
| 5s | 0.966244 | 0.931536 | 1,047,430 |
| 10s | 0.939968 | 0.756504 | 655,016 |
| 30s | 0.856419 | 0.679288 | 745,656 |

Source: `f1\f1_results.csv`, column `recomputed_auc`, rows `pre/ZC/LightGBM/{5s,10s,30s}`
(lines 50-52) and `post/ZC/LightGBM/{5s,10s,30s}` (lines 114-116). *(This table is the
declaration's SC-2(d) anchor-entry set — one entry per declared horizon and side, each naming
its provenance; the tolerance is the registered ±0.010 per entry.)*

**Why the old anchor cannot stand, stated plainly** *(evidence for the amendment — instance; the
rule it instantiates is SC-2(d))*:

1. **No single horizon satisfies the old interval on both sides.** Against 0.957 ± 0.010 on the
   pre-fix side and 0.675 ± 0.010 on the post-fix side: 5s passes pre (|0.966244 − 0.957| =
   0.009244) and fails post by 0.2565; 10s fails pre by 0.0170 and fails post by 0.0815; 30s
   fails pre by 0.1006 and passes post (|0.679288 − 0.675| = 0.004288). There is no horizon at
   which the registered pair is reproduced. Keeping the interval would fail the gate on a
   fixture whose pair is otherwise exactly as registered.
2. **The registered anchor names no model family; this declaration names one.** *(Corrected 21
   August 2026, R48/Q4. This item previously read "**The model family changes: XGBoost →
   LightGBM**", asserting that the original documented protocol named XGBoost. **That claim is
   false against its own cited source.** `MASTER_FINDINGS\preregistration_v4.txt` names **six
   fixed architectures**, with line 272 "1. LightGBM (gradient boosted trees)" immediately
   **above** line 273 "2. XGBoost (gradient boosted trees)", and records hyperparameters for
   both. **LightGBM was in the registered protocol from the start. No family changed.** The
   error was a justification citing a source that does not say what was claimed.)* Registered
   `PREREG.md` line 445 states the pair 0.957/0.675 and **names no architecture, horizon or
   instrument**, so the configuration it was computed under is **not recoverable from the
   registered text**. The declared trio above is ZC / LightGBM and says so rather than leaving
   the configuration implicit. `f1\f1_results.csv` carries both families across 128 rows (32
   rows each for pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost). **This item is a
   disclosure about under-specification in the registered text, not a discrepancy in the
   fixture**; the ground for the amendment is item 1, which does not depend on it.
3. **The RE-EVALUATE class makes the recomputation authoritative, not merely alternative.** The
   fixture is the stored-prediction pair (§8): 64 parquets per side, each carrying `pred_score`
   and `true_label` per row. AUC over those columns is a pure function of bytes already on
   disk — no retraining, no re-randomization, no environment dependence, nothing that a rerun
   could move. The recorded meta AUCs are a 4-decimal secondary record of the same quantity;
   where meta exists it agrees (`flag_gt_5e-5` False on all 95 matched rows, §8). So the
   recomputation does not contradict the record — it supersedes it in precision, and it is the
   only form of the number that can be audited from the fixture itself.

4. **REGISTERED EX ANTE — the post-fix trio has no originating counterpart, and none can
   exist.** *(Registered 21 August 2026, R48/Q7: **before any Phase 1 measurement**, and stated as
   a ground, never as a tolerance discovered after a miss (§7.0).)* The **pre-fix** entries have an
   originating counterpart in **Phase 6** —
   `results\pc2_all_phases\phase6\second_pc\phase6_main_summary.csv`, keyed
   (`instrument`, `architecture`, `horizon_s`, `tier`), rows ZC / LightGBM / L2: **0.9662 /
   0.9400 / 0.8564** at 5s / 10s / 30s. The declared trio reproduces them to **|Δ| ≤ 4.4e-5**.
   The **post-fix** entries have **no originating counterpart anywhere in the archive, and none
   can exist**: the universal-lag correction that *defines* the post-fix side was first applied in
   **Phase 7 itself**, so no prior experiment ever measured that side. The absence is a property
   of the experimental record, not of this declaration's diligence. **Where a gate limb compares a
   declared entry against a figure an originating experiment recorded, the three post-fix entries
   take that limb's no-counterpart branch on this registered ground, and on no other.**

**Phase 7 re-derived; it did not transcribe.** *(Determined 21 August 2026, R48/Q5.)* All 32 Phase 6
L2 cells appear in `results\phase7\l2_model_meta.csv` byte-identical, **including `shuffle_mean`**.
That is not evidence of copying: `phase7_l2_sim.py` trains its own models, reads no Phase 6 output
(its eight `phase6` references are all to a rerun mode that **writes**), Phase 6 stored **no
prediction files at all** so Phase 7's 64 parquets cannot be copies, and the shuffle mean is
computed over **fixed seeds [42, 123, 456]** via `RandomState(seed).permutation` — deterministic by
construction, so identity across a seeded re-run is expected. Recomputing AUC from Phase 7's own
`zc_LightGBM_5s_predictions.parquet` gives **0.966244**, matching the declared entry to 2.5e-7.
**Not established:** no Phase 6 script survives on disk, so whether the two runs shared seeds and
parameters — and hence whether the agreement is deterministic identity or independent convergence
— cannot be settled from the artifacts.

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

> **THIS COUNT CARRIES NO GATE ARITHMETIC** — `PREREG.md` §6.2 SC-4(a) (the denominator is
> derived from the declared map, by the rule registered there), cited and not restated; working
> resolution R11 is the record of its adoption for this fixture. PREREG.md line 446 is a
> **manifest-content**
> requirement: the manifest must record the DAG and the count. It is satisfied by the manifest
> recording 25 *(instance: manifest content, line 446)*. The manifest's leak-source
> classification is **provenance context**: it says how a column was built, not whether the
> map declares a violation on it on the scored side under the declared tie branch. Reading 25
> as N was the contradiction R11 resolves; **N is 11** (§A.6). Both numbers are in this file
> and neither is left to be inferred.

**The flavor split, stated BOTH ways (working resolution R13).** The manifest and the
declaration disagree on exactly one column's FLAVOR, and the disagreement is recorded rather
than removed:

| Flavor | Per `f3\fixture_manifest_DRAFT.json`, as of its date | Under R6 (the declaration's operative value) |
|---|---|---|
| `label_base_price` | **7** (incl. `weighted_mid`) | **6** |
| `contemporaneous_state_flow` | **18** | **19** (incl. `weighted_mid`) |
| leak_source total | 25 | 25 |

- **The manifest is NOT edited** — `PREREG.md` §0.2.1 SC-9(b) (evidence artifacts are never
  adjusted toward a decision), cited and not restated; working resolution R13 is the record of
  its application to this artifact. `f3\fixture_manifest_DRAFT.json` is an evidence artifact of
  a dated measurement round.
  Editing its `flavor` field to agree with R6 would make the artifact appear to have measured
  what a later resolution decided, and would destroy the only record of what the F3 round
  actually judged.
- **R6 is the declaration's operative value** for `weighted_mid` — `contemporaneous_state_flow`,
  PROVISIONAL until the prereg-v30a tag is signed, on the information-content test recorded in
  the supersession note after the T2 addendum block.
- **The supersession is scoped to one column and one field.** The manifest's `flavor` for
  `weighted_mid` is superseded **for `weighted_mid` only**; every other flavor, every CLASS
  assignment (including `weighted_mid`'s own LEAK-SOURCE class, which was never ambiguous),
  the parent lists, and all four `counts` totals stand exactly as the manifest records them.
- **Nothing in the gate turns on the split** — the flavor split is a classification of the
  scored set other than the registered derivation, and `PREREG.md` §6.2 SC-4(a) governs what
  such a classification may carry (cited, not restated); the split is reported because a reader
  comparing the two artifacts would otherwise find an unexplained 7-vs-6 and be entitled to
  distrust both.

**Why F3 governs and not T4.** `t4\fixture_manifest_35col_DRAFT.json` reports
`counts_projected_subset`: `projected_total: 28`, `unconstructible_total: 7`, `leak_source: 22`,
`descendant: 5`, `clean: 1`, with `unconstructible_by_class` = `leak_source: 3`, `descendant: 1`,
`clean: 3`. That 22 is a property of what the **F2 rebuild can reconstruct** under the
selection/renaming-only projection rule (§17), not a property of the fixture the gate scores.
The gate's fixture is the stored-prediction pair, whose feature set is the full 35 columns under
working resolution R3 (§16 item 1). **The declaration therefore governs on 25 and records 22 as
the reconstruction-limited subset**; both numbers appear in this file and neither is left to be
inferred. Every quotation of a leaking-source count in this file names which of the two scopes
it counts under (`PRACTICES.md` P-20; `PREREG.md` §6.2 SC-4(a), last sentence, carries the
report-side requirement and is cited).

---

### A.3 — Contamination availability class — **SATISFIED BY SUBSTITUTE (class C amendment of the RECORDING LOCUS)**

**Registered text, PREREG.md line 450 (verbatim):**

> **Contamination availability class** recorded in the manifest.

**Declared class: AVAILABILITY VIOLATION BY FORWARD JOIN** — the contamination is not a value
corruption, a shuffle, or a label leak in the ordinary sense; it is a cell whose availability
time is strictly later than the decision time that consumes it. Mechanism: the `ts_floor`
wall-clock-second join (§3) attaches to snapshot row `T` an aggregate over
`[floor(T), floor(T)+1s)`, a window that completes at `floor(T)+1s` and can contain events with
`ts_event > T`. Measured incidence and per-column enumeration: §14 and §C.

**The measured gap:** neither `f3\fixture_manifest_DRAFT.json` nor
`t4\fixture_manifest_35col_DRAFT.json` carries a named field for the contamination availability
class — verified this pass by key search over both files.

**RESOLUTION — the recording locus is AMENDED, and the element is MET, not outstanding.** The
earlier draft left this element half-met ("this declaration is the record until the field is
added") and booked the field as a class A act due before the tag. That disposition is
withdrawn. It is replaced as follows:

**OLD (registered, PREREG.md line 450, verbatim):** "**Contamination availability class**
recorded in the manifest."

**NEW:** the contamination availability class is **recorded in this availability declaration** —
the recording locus `PREREG.md` §6.2 "Contamination availability class — v30a, operative"
registers, with SC-9(b) (cited, not restated); the declared class above is that clause's
instance. This file is hashed in the `prereg-v30a` tag message (§D.2) and frozen at the tag by
§D.1. The manifest is not the locus and is not edited.

**Why this substitute, and why it is not weaker (class C under PREREG.md line 93):**

1. **The manifest cannot take the field without becoming something it is not.**
   `f3\fixture_manifest_DRAFT.json` is an evidence artifact of a dated measurement round.
   Writing a *declaration* into it would make a measurement record carry a decision — precisely
   what `PREREG.md` §0.2.1 SC-9(b) forbids (cited; working resolution R13 applied it in the
   neighbouring case). The registered wording assumed one artifact where this fixture
   has two: a measurement manifest and a declaration.
2. **The substitute binds harder than the original.** The manifest is hashed in no tag message.
   This declaration is hashed in the v30a tag message (§D.2 enumerates the set) and its contents are
   frozen by §D.1, so moving the class after the tag is itself a class C amendment. Recording
   the class here therefore subjects it to a stronger integrity chain than line 450 asked for —
   "an amendment weaker than the thing it amends is not one" (PREREG.md line 97) is satisfied
   in the direction the clause intends.
3. **Nothing is lost in reach.** The class is stated above with its mechanism, its measured
   incidence (§14), its per-column enumeration (§C) and its per-cell map (§13). A reader
   looking for it in the manifest is routed here by this section, which is itself hashed.

**What this amendment does NOT do.** It does not remove the obligation to record the class —
the class is recorded, verbatim, above. Its scope limit — one element's locus moves and nothing
else — is stated in the amended clause itself (`PREREG.md` §6.2, "This clause moves the locus of
one element and nothing else") and in SC-9(b); this file restates neither: line 446's
ground-truth DAG and independent-leak count remain manifest content and are satisfied there
(§A.2). And it does not retroactively make the
earlier "field OUTSTANDING" reading correct; that reading is superseded, and the lock-time
obligation it generated is discharged in §D.2.

---

### A.4 — Sliced variant for CI — **AMENDED (class C): moved off the Phase 0 acceptance fixture and re-registered as a Phase 1 CI obligation**

**Registered text, PREREG.md line 451 (verbatim):**

> **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**The measured state.** No artifact in this spike produces or names a sliced fixture variant,
and no padded slicer has been run against the fixture.

**The element is UNSATISFIABLE AS REGISTERED at the moment this amendment must be committed,
and the reason is structural, not an omission.** Line 451 requires the variant to come from
**the same padded slicer as user-facing slice auditing** — a component of the tool under
development. PREREG.md line 95 requires a class C amendment to be committed and externally
timestamped **"before the affected detector is implemented or evaluated"**. At that instant no
slicer exists, so no artifact satisfying line 451 can exist either. Leaving the element
"outstanding" would ship the registration with a permanently unmet registered element and would
invite it to be quietly re-read as satisfied later — the failure mode §2.7's undeclared-means-
unsupported rule exists to stop. **The instrument for an element that cannot be met as written
is an amendment. It is amended here, explicitly, and not waived.**

**OLD:** a sliced fixture variant, produced by the same padded slicer as user-facing slice
auditing, is part of the §6.2 acceptance fixture.

**NEW — registered as `PREREG.md` §6.2 "Sliced variant — v30a, operative", with SC-2(a), SC-2(e)
(moving an element between phases) and SC-3(f) (a derived subset inherits its cells); the clause
is cited, not restated.** What this declaration supplies under it, in three parts:

1. **Locus.** The fixture the v30a gate is evaluated on is exactly §8's stored-prediction pair
   (SC-2(a)'s enumeration); no sliced variant is part of it.
2. **The re-registered obligation's due event**, as the clause names it: the first CI run that
   exercises the padded slicer, before any user-facing slice auditing is published — produced by
   that same padded slicer, with its slice boundaries declared.
3. **The cells a slice will be scored against:** the `n1\declared_map.csv` cells its rows
   select (§13), under `PREREG.md` §6.2 criterion 3 as amended (SC-3) and SC-3(f). The scoring
   rule is the registered one; it is not restated here.

**Why this is class C and not class A.** It changes which artifacts the acceptance criteria are
evaluated on, and therefore what a published fixture number means — PREREG.md line 93's
definition exactly. It is carried by this registration under line 95.

**What this amendment does NOT do.** It does not delete slice auditing and does not exempt the
slicer from CI. How the re-registered obligation may and may not be discharged — and that
dropping it is a further class C amendment — is `PREREG.md` §0.2.1 SC-9(c) (a locked obligation
is discharged only by being met or by being amended), cited and not restated; the obligation is
frozen under §D.1.

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

**SATISFIED AS TO ORDERING. THE COMPARISON THAT RAN DOES NOT SATISFY §9.2.**

*(Corrected 21 August 2026, R48/Q2. This paragraph previously read: "**SATISFIED.** This whole file
is a Phase 0 product; no cross-tool comparison has been run." The second clause was false when
written. The correction is recorded here rather than by silent replacement.)*

**Line 448's ordering holds.** This whole file is a Phase 0 product, and the reconstruction it
records preceded the cross-tool comparison.

**A cross-tool comparison WAS executed on 14 August 2026** — eleven tools over eight hand-written
cases and their eight clean paired controls, 88 tool × case cells — with the case set authored,
materialised and hashed **before the first tool ran** (29.261 s, corroborated independently of the
clock by a hash chain: 112 declared case hashes recomputed, 0 mismatches, 0 unresolved).

**It does not satisfy §9.2, and §9.2 remains un-run in its registered form.** §9.2 requires the
comparison set "committed with this protocol"; the set is in no commit, appears nowhere in git
history, and the tagged tree of `prereg-v30` is fixed at 20 paths — so that clause is **breached and
uncurable for this tag**. **The acceptance-fixture half of §9.2 was not run.** **§10.1 criterion 3
therefore remains unevaluated for every rostered tool**, and the kill-gate verdict rests on
criterion 1. The run is **unverified by any party that did not perform it**; no result of it is
cited load-bearing anywhere in this declaration.

Recorded in full at `DEVIATIONS.md` **D-003**.

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

### A.6 — Criterion 1 — **SATISFIED; denominator RE-DERIVED FROM THE DECLARED MAP under working resolution R11. N = 11.**

**Registered text, PREREG.md line 459 (verbatim):**

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.

Related registered text, PREREG.md line 464 (verbatim):

> Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

and PREREG.md line 468 (verbatim):

> Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**SATISFIED.** The criterion-1 violation set is enumerated side-relatively and post-lag in §C,
by column. **The criterion-1 denominator is the object `PREREG.md` §6.2 SC-4(a)–(b) registers —
the REQUIRED class, derived from the declared map (`n1\declared_map.csv`) by the registered
predicates, and not from the manifest's construction classes** (cited, not restated); working
resolution R11, verbatim at the file tail, is the record of its adoption for this fixture. The
earlier draft's implicit denominator was the manifest's 25 independently-leaking sources; that
was the contradiction the P2 verifier found, because line 446's count is a statement about how
columns were BUILT and the registered predicate reads what the map DECLARES VIOLATING on the
scored side under the declared tie branch. **The manifest's leak-source classification is
provenance context and carries no gate arithmetic** (§A.2; SC-4(a)).

**The three classes are published as `PREREG.md` §6.2 SC-4(b) and SC-4(f) require** (exactly
three classes, exhaustive over the declared scored set; publication discipline — cited, not
restated): exhaustive over the 35 fed columns, each **ENUMERATED BY NAME** in §A.6.1–§A.6.3,
none defined as a residue or stated as a bare count, with the partition check printed in
§A.6.4.

#### A.6.0 — DERIVATION, BY CITATION. **The enumeration below is what the registered rule yields.**

Each column's class is derived by the registered rule — the class predicates `PREREG.md` SC-4(b)
registers, under SC-4(c)'s precedence — applied to the column's declared construction and gate
status. This section states no rule of its own (`PREREG.md` SC-4(a), SC-9(a)): per class it cites
the `PREREG.md` row that carries the predicate, and per column the table below states the class
assigned and the declared ground on which the column satisfies that predicate. Re-derivation when a
column changes construction re-applies the cited rows to the column's new facts (SC-4(h)). Where a
column's ground satisfies more than one row, SC-4(c)'s registered precedence decides — UNSCORED
wins — and the table says so for that column. The citations:

- **REQUIRED** — predicate: `PREREG.md` SC-4(b), row REQUIRED, cited and not restated. Declared
  ground, per column in the table below: its construction carries the wall-clock `ts_floor` join,
  which is the violation §C declares on it on the scored side under R1.
- **OUT OF JURISDICTION** — predicate: `PREREG.md` SC-4(b), row OUT OF JURISDICTION, cited and not
  restated. Declared ground, per column: its construction reads only same-row — read as
  within-lattice, reading note below — book/clock values, each read availability-legal at the
  boundary instant under R1's `ties: available` (§A.6.2).
- **UNSCORED** — predicate: `PREREG.md` SC-4(b), row UNSCORED, cited and not restated, on a ground
  `PREREG.md` SC-4(e) registers. Declared ground, per column: degenerate-constant, or
  unconstructible under T4 (gate status EXCLUDED on the gate-scored fixture; §A.6.3).

Three reading notes fix the reading at each edge on the 35-column set, as `PREREG.md` §6.2
SC-4(d) requires the declaration to do ex ante. Each states the declared fact the cited row is
applied to, and which registered reading it is applied under; none states a rule of its own:

- **Precedence.** Registered at `PREREG.md` SC-4(c) (precedence, registered — UNSCORED wins) and
  cited, not restated. On this fixture it decides exactly one column: `book_imbalance_ratio`
  satisfies the OUT OF JURISDICTION predicate (a pure function of the same row's two depth sums)
  **and** the UNSCORED predicate on the unresolved-lag ground (T4-EXCLUDED, §C.4(c)); SC-4(c)
  resolves it to UNSCORED, per §A.6.3 and frozen §D.1 item 2. `buy_volume_10s` reads a merged
  `ts_floor` aggregate but is identically constant on the fixture; it satisfies the UNSCORED
  predicate on the degenerate-unit ground `PREREG.md` SC-4(e) registers (§A.6.3, first bullet),
  and is recorded under the same precedence so the table has one answer per column.
- **"Same-row book/clock" is read as "within-lattice book/clock", not literally single-row** —
  the registered reading `PREREG.md` SC-4(d)(i) (the locality reading), cited. Declared fact: a
  same-lattice lagged read (`depth[t] - depth[t-5s]`, `mid[t] / mid[t-1s]`) reads two rows of
  the same book/clock column and carries no `ts_floor` join to a trade aggregate; each
  constituent read is availability-legal at its own timestamp under R1's `ties: available`
  (§A.6.2's explicit basis; PREREG.md 190-197). These are OUT OF JURISDICTION.
- **"Unconstructible under T4" is read as "gate status EXCLUDED under T4 applied to the
  gate-scored fixture", not as "F2-rebuild-unconstructible"** — the registered reading
  `PREREG.md` SC-4(d)(ii) (the unconstructibility reading), cited. Declared fact: the F2
  rebuild's seven selection/renaming-only unconstructibles (§17) are not gate-unscored; the
  reading SC-4(d)(ii) forbids would silently drop `dollar_volume_1s` (REQUIRED) and
  `tick_direction` (OUT OF JURISDICTION) out of the arithmetic, contradicting R11. §A.6.3's
  closing paragraph states the application.

**Column-by-column application (all 35 fed columns) — the per-unit derivation `PREREG.md`
SC-4(a) requires the declaration to show.** The class the cited rows yield for each column is
shown alongside the sub-section where the frozen enumeration lists it. A disagreement between
the derived class and the frozen class would be a stop-and-report under `PREREG.md` SC-4(i)
(cited); there is none this pass.

> **Reading the "construction" column, per §0.3's artifact rule.** These 35 are Artifact-B fed
> columns, and Y1 traces all 35 to `phase7_l2_sim.py`. Where a row cites a bare line number or a
> `phase5_ml.py` line, it names the **lineage** construction (Part I's citation base, §0.1) —
> the same construction exists in the Phase 7 builder, and the `ts_floor` join the rule turns on
> is present in BOTH generations, so no row's class depends on which file is read. The trade
> rollups are `phase5_ml.py` L253/L255/L257/L258 ≡ `phase7_l2_sim.py` L238-239/L241/L242/L243,
> with the trades merge at `phase5_ml.py` L248 ≡ `phase7_l2_sim.py` L231. Rows that cite
> `phase7_l2_sim.py` explicitly are Phase-7-only columns with no lineage counterpart.

| # | Column | Class (SC-4(b) row cited) | Declared ground | Frozen at |
|---|---|---|---|---|
| 1  | `net_delta_1s`          | REQUIRED | `ts_floor` merge on `net_delta` (`phase5_ml.py` L253) | A.6.1 #1 |
| 2  | `net_delta_5s`          | REQUIRED | same L253 rolling(5)                                       | A.6.1 #2 |
| 3  | `net_delta_10s`         | REQUIRED | same L253 rolling(10)                                      | A.6.1 #3 |
| 4  | `net_delta_30s`         | REQUIRED | same L253 rolling(30)                                      | A.6.1 #4 |
| 5  | `net_delta_60s`         | REQUIRED | same L253 rolling(60)                                      | A.6.1 #5 |
| 6  | `sell_volume_10s`       | REQUIRED | L255, `sell_size` merged on `ts_floor`                     | A.6.1 #6 |
| 7  | `large_trade_count_10s` | REQUIRED | L257, large-count aggregate merged on `ts_floor`           | A.6.1 #7 |
| 8  | `vwap_distance`         | REQUIRED | L258, the `vwap` term is the merged per-second aggregate   | A.6.1 #8 |
| 9  | `trade_volume_1s`       | REQUIRED | `phase7_l2_sim.py` groupby L216-226, merge L231, assign L246 | A.6.1 #9 |
| 10 | `trade_count_1s`        | REQUIRED | groupby L220, assign L247                                  | A.6.1 #10 |
| 11 | `dollar_volume_1s`      | REQUIRED | L214 + groupby L223, assign L248                           | A.6.1 #11 |
| 12 | `minutes_since_open`    | OUT OF JURISDICTION | deterministic clock function of the row's own timestamp | A.6.2 (a) |
| 13 | `session_open`          | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 14 | `session_mid`           | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 15 | `session_close`         | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 16 | `spread_ticks`          | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 17 | `bid_size_1`            | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 18 | `ask_size_1`            | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 19 | `l1_imbalance`          | OUT OF JURISDICTION | same-row derivation of bid/ask sizes                    | A.6.2 (b) |
| 20 | `total_bid_depth`       | OUT OF JURISDICTION | same-row sum across levels                              | A.6.2 (b) |
| 21 | `total_ask_depth`       | OUT OF JURISDICTION | same-row sum                                            | A.6.2 (b) |
| 22 | `depth_imbalance`       | OUT OF JURISDICTION | same-row ratio                                          | A.6.2 (b) |
| 23 | `book_slope_bid`        | OUT OF JURISDICTION | same-row slope across price levels                      | A.6.2 (b) |
| 24 | `book_slope_ask`        | OUT OF JURISDICTION | same-row slope across price levels                      | A.6.2 (b) |
| 25 | `depth_change_1s`       | OUT OF JURISDICTION | within-lattice lagged reads of `depth`; no trade join   | A.6.2 (b) |
| 26 | `depth_change_5s`       | OUT OF JURISDICTION | within-lattice lagged reads                             | A.6.2 (b) |
| 27 | `depth_change_30s`      | OUT OF JURISDICTION | within-lattice lagged reads                             | A.6.2 (b) |
| 28 | `mid_return_1s`         | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 29 | `mid_return_5s`         | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 30 | `mid_return_10s`        | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 31 | `mid_return_30s`        | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 32 | `tick_direction`        | OUT OF JURISDICTION | sign of within-lattice `mid` change                     | A.6.2 (b) |
| 33 | `weighted_mid`          | OUT OF JURISDICTION | same-row bid/ask weighting                              | A.6.2 (b) |
| 34 | `buy_volume_10s`        | UNSCORED (SC-4(e), degenerate unit) | `phase5_ml.py` L231 (= `phase7_l2_sim.py` L207) aggressor classifier matches none of the parquet's aggressor values → column identically 0 | A.6.3 |
| 35 | `book_imbalance_ratio`  | UNSCORED (SC-4(e), unresolved lag)  | construction not verified equivalent from fixture code; gate status EXCLUDED (§C.4(c), §17 item 6) | A.6.3 |

**What the cited rows yield.** REQUIRED (rows 1-11): 11. OUT OF JURISDICTION (rows 12-33): 22 —
4 clock-function (rows 12-15) + 18 book/lattice (rows 16-33). UNSCORED (rows 34-35): 2.
Total 35. This matches the sub-sections' enumerations column by column and matches the
partition check in §A.6.4. **Re-derivation on a construction change, and the standing of this
enumeration as the current output of the registered rule and never a substitute for it, are
`PREREG.md` SC-4(h)'s (re-derivation is mandatory, and moving a unit is an amendment) — cited,
not restated. On this fixture the live case is `book_imbalance_ratio` becoming constructible per
§C.4(c); its class is then re-derived under SC-4(h) and the change is a class C amendment.**

#### A.6.1 — REQUIRED (the criterion-1 denominator). **N = 11.**

Columns the declared map declares violating on the scored side under the declared branch — the
**forward-join / `ts_floor` overhang family**. Derivation, stated so it is reproducible: these
are the columns of the 35-column fed set whose construction reads an aggregate merged on
`ts_floor`, the wall-clock-second key (§3, §C.1), so their true availability instant is
`ts_floor + 1s`; the map classes that govern them are the `trades_*` classes, which are
strict-positive on the contaminated side in **all 48** instrument-months (§13(c)) and on the
corrected side in the 18 of §13(b).

| # | Column | Construction | Governing map class |
|---|---|---|---|
| 1 | `net_delta_1s` | `phase5_ml.py` L253, rolling sum of merged `net_delta` | `trades_all` |
| 2 | `net_delta_5s` | L253 | `trades_all` |
| 3 | `net_delta_10s` | L253 | `trades_all` |
| 4 | `net_delta_30s` | L253 | `trades_all` |
| 5 | `net_delta_60s` | L253 | `trades_all` |
| 6 | `sell_volume_10s` | L255 | `trades_sell` (≡ `trades_all` here, §15) |
| 7 | `large_trade_count_10s` | L257 | `trades_large` |
| 8 | `vwap_distance` | L258, `(mid - snap["vwap"]) / tick` — the `vwap` term is the merged aggregate | `trades_all` |
| 9 | `trade_volume_1s` | `phase7_l2_sim.py` groupby L216-226, merge L231, assign L246 | `trades_all` |
| 10 | `trade_count_1s` | groupby L220, assign L247 | `trades_all` |
| 11 | `dollar_volume_1s` | L214 + groupby L223, assign L248 | `trades_all` |

**N = 11**, being the length of that list — the only quantity that is N under `PREREG.md` §6.2
SC-4(b) (cited). *(The table above is the REQUIRED list SC-4(f)1 requires, enumerated by name;
its "Governing map class" column is the ground on which each unit satisfies the cited row.)*
What a finding on each of the eleven must be — at least one **primary** runtime finding, on the
side, in the cells and on the ground the map declares — is `PREREG.md` §6.2 criterion 1 with
SC-5(b) (attribution is to the ground, not to the name), cited and not restated. PREREG.md
line 468 binds: top-k presence does not satisfy it, and an alias satisfies it only if recorded
before the run.

Two notes that keep the list honest:

- **`vwap_distance` is REQUIRED for its `vwap` term, not for its `mid` term.** Its
  `(X - mid)/tick` form also makes it a label-base reader; that character is assigned to L2a
  in §C.3 — the detector-jurisdiction assignment `PREREG.md` §6.2 SC-5(e) requires the
  declaration to make, with SC-5(e)'s consequence for this gate (cited, not restated). Its
  availability violation is the merged wall-clock-second aggregate, which is a §C.1 join-family
  violation like the other ten. **It is the fixture's SOLE dual-ground column — the only
  MIXED-source column of the 35 — and the full statement of what that means for this entry is
  §C.5**, which must be read with this row: the violating ground is the **forward-join** ground
  (`ts_floor` trade window, `phase7_l2_sim.py` L224-225 / L231 / L235), the same-row `mid[t]`
  read (L149) is the legal ground, and **which of the two a finding must be on to satisfy this
  entry is `PREREG.md` §6.2 SC-5(b) (attribution is to the ground, not to the name) — cited,
  not restated.** Under `PREREG.md` SC-4(g) (one gate class per unit) the column carries **one
  gate class only — REQUIRED** (§C.5's comparison table; R16 is the working resolution that
  applied the same discipline to `book_imbalance_ratio`).
- **No MBO-derived column is in the list, and that is a scope fact, not an omission** *(instance:
  a fact about the named scored set `ALL_L2_FEATURES`, SC-4(j))*. Phase 7
  feeds no MBO columns at all (§4's Phase 7 difference, §C.1's scope note), so the map's six
  `mbo_*` classes characterise the fixture's MBO stream against the lattice without attaching
  to any fed column. `trade_count_10s` is likewise absent because Phase 7 drops it.

#### A.6.2 — OUT OF JURISDICTION (22 columns)

Declared availability-legal at the boundary instant under R1's `ties: available` — the declared
ground on which each satisfies `PREREG.md` §6.2 SC-4(b), row OUT OF JURISDICTION (cited). **The
gate consequence of an availability-class finding on any of them — a declared false positive —
is `PREREG.md` §6.2 SC-5(c)'s (the false-positive consequence attaches to the out-of-jurisdiction
class and to no other), cited and not restated.** *(The two lists below are the OUT OF
JURISDICTION enumeration SC-4(f)1 requires, by name.)* Two sub-groups, because their
false-positive routes differ:

**(a) Manifest-CLEAN columns — 4. Route: criterion 2 (contaminated side) and the amended
criterion 3 (corrected side).** `minutes_since_open`, `session_open`, `session_mid`,
`session_close`. Role `always`, deterministic clock functions of the row's own timestamp
(§4, T2 addendum). The session-flag staleness quirk licenses no finding on either side
(§C.4(b)).

**(b) Same-row book and lattice reads that the manifest classes LEAK-SOURCE or DESCENDANT —
18. Route: declared false positive; criterion 2 has NO landing site for them.** `spread_ticks`,
`bid_size_1`, `ask_size_1`, `l1_imbalance`, `total_bid_depth`, `total_ask_depth`,
`depth_imbalance`, `book_slope_bid`, `book_slope_ask`, `depth_change_1s`, `depth_change_5s`,
`depth_change_30s`, `mid_return_1s`, `mid_return_5s`, `mid_return_10s`, `mid_return_30s`,
`tick_direction`, `weighted_mid`.

> PREREG.md line 460 (verbatim): "2. No **manifest-clean** source column receives **any runtime
> finding of any tier, primary or secondary**, on `fixture_contaminated`." Its scope is
> manifest-CLEAN columns. The 18 above are manifest LEAK-SOURCE or DESCENDANT, so **criterion 2
> has no landing site for them** — routing them there was the error R11 deletes in §C.3. What
> happens to a finding on one of them instead — a declared false positive, recorded as such, and
> not a criterion-2 failure — is `PREREG.md` §6.2 SC-5(c), cited and not restated.

**Their label-base character is real and is assigned to L2a.** `tick_direction`, `weighted_mid`
(and `vwap_distance`, which is REQUIRED for a different reason) sit at `mid(t)`, the base
`fwd_move_ticks_*` measures from. **This is the detector-jurisdiction assignment `PREREG.md`
§6.2 SC-5(e) (jurisdiction between detectors is declared, and a boundary cuts both ways)
requires the declaration to make before any detector runs; its consequence for this gate is
SC-5(e)'s, cited and not restated** (§C.3 states the assignment in full).

#### A.6.3 — UNSCORED (2 columns, plus a cell-level member)

Gate class UNSCORED — `PREREG.md` §6.2 SC-4(b), row UNSCORED, and §7.7 SC-6(a) (the `unscored`
state: its semantics and gate consequences), cited and not restated. What this declaration
supplies is SC-6(b)'s unscored ledger: at unit level, the two columns below, each with its
ground; at cell level, the 72 cells of §13(g).

- **`buy_volume_10s` — degenerate constant.** `phase5_ml.py` L231's `isin(["B","Buy","buy"])`
  matches none of the parquet's `BUY_AGGRESSOR`/`SELL_AGGRESSOR`/`UNKNOWN` values, so the column
  is identically 0 and the `trades_buy` map class is 0 strict / 0 equal in all 96 of its cells
  on both sides (§C.4(a)). It is a degenerate unit that cannot carry a finding of the scored
  class — the first exclusion ground `PREREG.md` §6.2 SC-4(e) registers (cited, not restated).
  Its reporting as **EXCLUDED** rather than MISSED is `PREREG.md` §7.8 SC-11(g)'s (cited;
  `PRACTICES.md` P-47 records the vocabulary practice).
- **`book_imbalance_ratio` — gate status EXCLUDED, lag treatment UNRESOLVED** (§C.4(c), §17
  item 6) — the second exclusion ground `PREREG.md` SC-4(e) registers. **It carries ONE gate
  class and one only — UNSCORED** (`PREREG.md` §6.2 SC-4(g), one gate class per unit — cited;
  working resolution R16 is the record of its application). That it WOULD be OUT OF
  JURISDICTION if it were constructible is recorded as a fact in §C.3 category 2 and is **not
  applied**. Reinstatement is governed by `PREREG.md` SC-4(e) and SC-4(h) (class C), cited.
- **Cell-level: the 72 `UNSCORED_FOR_LACK_OF_DATA` map cells** (nq's six MBO classes x 6 months
  x 2 sides, §13(g), §13(h)). These are **cells, not columns** — the two levels `PREREG.md` §7.7
  SC-6(c) (two levels, and they do not collapse) keeps apart, cited: because Phase 7 feeds no
  MBO column, none of the 35 fed columns is put into UNSCORED by them. Recorded here so the
  ledger is complete at both levels.

**R11's third UNSCORED limb, read under `PREREG.md` §6.2 SC-4(d)(ii) (the unconstructibility
reading; cited).** R11 names "unconstructibles" as UNSCORED; on this fixture the columns whose
gate status is declared EXCLUDED is `book_imbalance_ratio` alone. The 7 UNCONSTRUCTIBLE columns
of §17 are unconstructible **in the F2 rebuild's selection/renaming-only projection**, not in the
fixture the gate scores — the gate scores the stored-prediction pair over the full 35 columns
under R3 (§A.2, §16 item 1). Reading §17's seven as gate-unscored is the reading SC-4(d)(ii)
forbids: it would silently drop `dollar_volume_1s` and `tick_direction` out of the arithmetic,
the opposite of what R11 does. **`dollar_volume_1s` is REQUIRED
(A.6.1 #11); `tick_direction`, `weighted_mid`, `session_open`, `session_mid`, `session_close`
are OUT OF JURISDICTION (A.6.2); only `book_imbalance_ratio` is UNSCORED.**

#### A.6.4 — PARTITION CHECK (printed here as `PREREG.md` §6.2 SC-4(f)3 requires)

| Class | Count |
|---|---|
| REQUIRED (A.6.1) | **11** |
| OUT OF JURISDICTION (A.6.2) — 4 manifest-clean + 18 same-row reads | **22** |
| UNSCORED (A.6.3) | **2** |
| **Total** | **35** |

11 + 22 + 2 = **35** = `f3\fixture_manifest_DRAFT.json` `counts.total_fed_to_phase7`. **No
column appears in two classes and no fed column is missing from all three** — checked column by
column against the manifest's 35-entry `columns` array this pass. The check is printed here, in
the declaration, as `PREREG.md` §6.2 SC-4(f)3 requires (cited; `PRACTICES.md` P-51 records the
shown-not-asserted practice). *(Instance: the counts in this table are the lengths of the
enumerated lists in §A.6.1–§A.6.3; what freezes is the lists, `PREREG.md` SC-8(b).)*

#### A.6.5 — CROSS-TABULATION of the TWO partitions: Y1 SOURCE class x R11 GATE class (item S2)

> *Instance data.* A consistency check over the SC-4 partition of §A.6.1–§A.6.4; it derives
> nothing, changes no class, and is not a gate object.

**What this is, and why it is not redundant with §A.6.4.** The 35 fed columns are cut twice by
two independent instruments. **Cut 1 — the Y1 SOURCE partition** (`y1\column_universe.csv`, 35
rows, each carrying its construction quote and upstream line numbers) asks *which raw file the
column's construction reads*: snapshot parquet **13**, trades parquet **11**,
derived-from-another-column **9**, clock-only **1**, MIXED snapshot+trades **1**; MBO **0**.
**Cut 2 — the R11 GATE partition** (§A.6.1 / §A.6.2 / §A.6.3, which are authoritative here and
are the lists transcribed below) asks *what the gate does with a finding on the column*:
REQUIRED **11**, OUT OF JURISDICTION **22**, UNSCORED **2**. The two cuts were built from
different artifacts for different purposes and neither was derived from the other. §A.6.4 checks
that Cut 2 is a partition; **this subsection checks that Cut 1 and Cut 2 COMPOSE** — that the
gate class of every column is the one its construction implies.

**WHY they should compose, stated as the mechanism before the table so the table can refute it.**
A column's gate class follows from **whether its construction carries the wall-clock `ts_floor`
join**. That join — `phase5_ml.py` L222/L230, merges L248/L273; `phase7_l2_sim.py` L206/L231
(§3, §C.1) — attaches to row `T` an aggregate over `[floor(T), floor(T)+1s)`, whose true
availability instant is `floor(T)+1s`, strictly after `T`. **Carrying that join is a property of
the SOURCE**: the trades parquet reaches the lattice only through it, while the snapshot parquet
*is* the lattice and needs no join, and the clock is a function of the row's own stamp. So
**trade-touching ⇒ forward-join ⇒ REQUIRED**, and **not-trade-touching ⇒ same-row read ⇒
availability-legal at the boundary under R1 ⇒ OUT OF JURISDICTION** — in each case *unless* a
separately-registered carve-out removes the column from scoring altogether. There are exactly two
such carve-outs, both pre-existing and neither invented here: `buy_volume_10s` (degenerate
constant, §C.4(a)) and `book_imbalance_ratio` (lag treatment unresolved, R16, §C.4(c)).

**THE 35 ROWS.** SOURCE class from `y1\column_universe.csv` (`source_class`); GATE class
transcribed by name from §A.6.1 (11), §A.6.2(a)+(b) (4 + 18) and §A.6.3 (2). The two name sets
were compared as sets before anything else: **identical, 35 = 35, no name in one and not the
other.**

| # | Column | Y1 SOURCE class | R11 GATE class | composes? |
|---|---|---|---|---|
| 1 | `mid_return_1s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 2 | `mid_return_5s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 3 | `mid_return_10s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 4 | `mid_return_30s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 5 | `tick_direction` | snapshot parquet | OUT OF JURISDICTION | yes |
| 6 | `trade_volume_1s` | trades parquet | REQUIRED | yes |
| 7 | `trade_count_1s` | trades parquet | REQUIRED | yes |
| 8 | `dollar_volume_1s` | trades parquet | REQUIRED | yes |
| 9 | `minutes_since_open` | clock-only | OUT OF JURISDICTION | yes |
| 10 | `session_open` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 11 | `session_mid` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 12 | `session_close` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 13 | `net_delta_1s` | trades parquet | REQUIRED | yes |
| 14 | `net_delta_5s` | trades parquet | REQUIRED | yes |
| 15 | `net_delta_10s` | trades parquet | REQUIRED | yes |
| 16 | `net_delta_30s` | trades parquet | REQUIRED | yes |
| 17 | `net_delta_60s` | trades parquet | REQUIRED | yes |
| 18 | `buy_volume_10s` | trades parquet | **UNSCORED** — carve-out, §C.4(a) | yes, **via the declared carve-out** |
| 19 | `sell_volume_10s` | trades parquet | REQUIRED | yes |
| 20 | `large_trade_count_10s` | trades parquet | REQUIRED | yes |
| 21 | `vwap_distance` | **MIXED: snapshot + trades** | REQUIRED | yes — **on the trades ground only; see §C.5** |
| 22 | `bid_size_1` | snapshot parquet | OUT OF JURISDICTION | yes |
| 23 | `ask_size_1` | snapshot parquet | OUT OF JURISDICTION | yes |
| 24 | `total_bid_depth` | snapshot parquet | OUT OF JURISDICTION | yes |
| 25 | `total_ask_depth` | snapshot parquet | OUT OF JURISDICTION | yes |
| 26 | `book_imbalance_ratio` | derived (parents `total_bid_depth`/`total_ask_depth`) | **UNSCORED** — carve-out, R16 / §C.4(c) | yes, **via the declared carve-out** |
| 27 | `weighted_mid` | snapshot parquet | OUT OF JURISDICTION | yes |
| 28 | `spread_ticks` | snapshot parquet | OUT OF JURISDICTION | yes |
| 29 | `depth_imbalance` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 30 | `book_slope_bid` | snapshot parquet | OUT OF JURISDICTION | yes |
| 31 | `book_slope_ask` | snapshot parquet | OUT OF JURISDICTION | yes |
| 32 | `depth_change_1s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 33 | `depth_change_5s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 34 | `depth_change_30s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 35 | `l1_imbalance` | derived (parents `bid_size_1`/`ask_size_1`) | OUT OF JURISDICTION | yes |

**RESULT: all 35 compose. NO column is flagged, and there is no flagged row in the table above.**
This was checked **column by column and not by count** — every row was evaluated against the
mechanism paragraph individually, and the two count identities below were computed only
afterwards, from the per-column result. **A non-composing column would have been a FINDING and
would appear above as a flagged row** with its two classifications and the contradiction named:
a trade-touching column classed OUT OF JURISDICTION would mean the gate declares a forward-join
column availability-legal, and a snapshot-or-clock-rooted column classed REQUIRED would mean the
criterion-1 denominator contains a column with no forward join to violate on. Neither occurs.

**THE RECONCILIATION, STATED AS ARITHMETIC.** Both identities were confirmed, not assumed:

> **(1) TRADE-TOUCHING 12 = REQUIRED 11 + `buy_volume_10s` (UNSCORED). CONFIRMED.**
> Trade-touching = trades parquet **11** + MIXED **1** = **12**, enumerated:
> `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s`, `net_delta_{1,5,10,30,60}s`,
> `buy_volume_10s`, `sell_volume_10s`, `large_trade_count_10s`, `vwap_distance`. Of those,
> **11 are REQUIRED — exactly §A.6.1's list, name for name — 1 is UNSCORED (`buy_volume_10s`),
> and 0 are OUT OF JURISDICTION.** 11 + 1 = 12.
>
> **(2) SNAPSHOT-ROOTED + CLOCK 23 = OUT OF JURISDICTION 22 + `book_imbalance_ratio`
> (UNSCORED). CONFIRMED.** = snapshot parquet **13** + derived **9** + clock-only **1** = **23**.
> Of those, **22 are OUT OF JURISDICTION — exactly §A.6.2's list, name for name — 1 is UNSCORED
> (`book_imbalance_ratio`), and 0 are REQUIRED.** 22 + 1 = 23.
>
> **(3) 12 + 23 = 35**, and the two source buckets are disjoint and exhaustive over the fed set,
> so the two partitions are a clean 2 x 3 cross-tabulation with **four occupied cells**:
> trade-touching x REQUIRED **11**, trade-touching x UNSCORED **1**, snapshot/clock x OUT OF
> JURISDICTION **22**, snapshot/clock x UNSCORED **1**. **The two empty cells are the
> load-bearing ones:** trade-touching x OUT OF JURISDICTION is **empty**, and snapshot/clock x
> REQUIRED is **empty**. Those two zeros are the composition claim.

**A finer reconciliation, which the two partitions also pass.** Inside the 23, the SOURCE cut
separates **clock-rooted 4** (`minutes_since_open` plus the three session flags derived from it —
`raw_source_traced` = "snapshot parquet: timestamp (clock only)" on all four) from **book-rooted
19**. **The clock-rooted 4 are exactly §A.6.2(a)'s four manifest-CLEAN columns**, and the
book-rooted 19 are exactly §A.6.2(b)'s 18 plus `book_imbalance_ratio`. §A.6.2(b)'s 18 in turn
split **13 snapshot-parquet + 5 derived** under the SOURCE cut, and the 5 derived are
`l1_imbalance`, `depth_imbalance`, `depth_change_{1,5,30}s` — **the same five, by name**, that
§C.3 Category 1(b) records as the **5 DESCENDANT** against **13 LEAK-SOURCE**. Two taxonomies
built from different artifacts (Y1's construction trace vs the f3 manifest's construction class)
land on the identical 13 / 5 split. That is a third, independent corroboration and it is recorded
as such rather than as a coincidence.

**What this subsection does NOT do.** It does not re-derive N, change any class, or create a
fourth class. **§A.6.4's partition governs**; this is a consistency check on it, and its only
operative consequence is the pair of empty cells in (3), which is what licenses §13(i)'s
statement that every REQUIRED column is already governed by a `trades_*` class and therefore that
the restricted map drops no adjudicating cell. Derivation script and output:
`s13\s13_crosstab.py`, `s13\s13_crosstab_output.txt`.

---

### A.7 — Criterion 2 — **SATISFIED**

**Registered text, PREREG.md line 460 (verbatim):**

> 2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.

**SATISFIED and unchanged.** The manifest-clean set is the 4 clean columns of
`f3\fixture_manifest_DRAFT.json` (`counts.clean: 4`) *(instance: the units criterion 2 scopes;
under `PREREG.md` SC-5(c) these are the units that route to it)*. Two declared dispositions bear
on it and
are recorded in §C.4: the **session-flag staleness** quirk (§C.4(b)) is a documented artifact of
the shift and licenses **no** finding, on either side; and `book_imbalance_ratio` (§C.4(c)) is
gate-status **EXCLUDED**. Neither weakens the criterion — both remove a route by which a
non-availability artifact could be scored as one.

---

### A.8 — Criterion 3 — **AMENDED (class C), per working resolution R9**

**Registered text, PREREG.md line 461 (verbatim):**

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

**OLD (registered line 461, quoted above):** no runtime finding of any tier on `fixture_corrected`.

**NEW: `PREREG.md` §6.2 criterion 3 as amended — "Runtime findings on every fixture side are
scored against the fixture's DECLARED GROUND-TRUTH MAP — v30a, operative" [SC-3].** The
criterion, its three dispositions (SC-3(b)) and its scope limits are registered there and are
cited, not restated; working resolution R9 (file tail, verbatim) is the record of its adoption
for this fixture, and R9's rationale — "the tool's own coverage principle (silence and belief
never convert into a pass) applied to its own exam" — is recorded as such. **What this
declaration supplies under SC-3:** the map artifact and its declared schema (§13(a),
`n1\declared_map.csv`); the cell key, named — (side, instrument, month, class); the declared
violation classes (the ten of §13(a)); the declared scored population and its subclasses (§5's
2,100 cross-boundary rows among them); the per-cell expected findings (§13(b)–(c), §C); the
unscored ledger (§13(g)); and the reporting re-aggregation with its delta (§13(i)).

**What forced it** *(instance: the measurement that forced the amendment; SC-3's supersession
marker names its genus)*. The M5 falsification sweep (`m5\`) extended the corrected-side check beyond
ZC 2025-01 and **falsified the assumption that the corrected side is clean** — see §13(f). The
corrected side carries strictly-post-decision absorption in **18 of 48** instrument-months, up
to **111,334 of 580,944 rows (19.16%)** on zc 2025-09 (`n1\summary_corrected.csv`). Criterion 3
as written would fail the gate on a correctly-behaving detector that reports a real violation
the fixture really contains. That is a semantic gap in the acceptance criterion — class C by
PREREG.md line 93 — and it is amended, not waived.

**What the amendment does NOT do** is registered at `PREREG.md` §6.2 SC-3(h) (the amendment
does not lower the bar) and is cited, not restated. On this fixture: the 72 unscored cells
(§13(g)) are ledgered by name and ground; the map is declared here and frozen at the tag by §D.1
item 3 under SC-8, before any detector runs.

---

### A.9 — Criterion 4, the identity control, and the sentinel statement — **SATISFIED**

**Registered text, PREREG.md line 462 (verbatim):**

> 4. Silent under the identity control on both.

**SATISFIED, with the sentinel enumeration `PREREG.md` §6.2 SC-5(f) (declared sentinels under
the identity control) requires the declaration to make ex ante — cited, not restated:**

> **SENTINEL, declared ex ante.** The wrapped `net_delta` values in this fixture — magnitudes near
> 4.29e9, e.g. the observed **4294967291** for a trade of `size` 5 (2^32 − 5) — are the as-built
> product of an uncast uint32 negation (§15) and are present identically on BOTH sides.
> **Signature:** magnitude ≈ 2^32 − k for a trade of `size` k; the sign; the 2^32 wrap. Their
> gate disposition — an as-built artefact present identically on every side — is SC-5(f)'s,
> cited and not restated: availability is a question about *when* a cell is knowable, and these
> values are equally knowable, and equally wrong, at every instant on both sides.

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
identified as a descriptive fixture outcome rather than a performance rate." **PREREG.md line
480 (verbatim):** "**Ordering, locked:** tune on the development corpus → freeze the candidate
configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults
may not be altered after observing a fixture result."

**SATISFIED, all five, carried unchanged.** Three consequences this declaration must honour and
does.

1. **N is 11** — the length of the REQUIRED list of §A.6.1, which `PREREG.md` §6.2 SC-4(b)
   makes the only quantity that is N (cited). Line 472's "**k of N** labelled leaking sources"
   is published against it. **N = 25 is withdrawn as the gate's N** — 25 is line 446's manifest
   DAG count and carries no gate arithmetic (§A.2; SC-4(a); working resolution R11).
2. **The proof count is published as a count, with its scope named**, per line 476 — and under
   §A.6 "scope" means the class: k of N = 11 REQUIRED columns; false positives on the 22 OUT OF
   JURISDICTION columns reported separately, that class and no other bearing the consequence
   (`PREREG.md` §6.2 SC-5(c), cited); findings on the UNSCORED class reported separately as
   unscored observations and not as false positives, the three classes never folded into one
   another (`PREREG.md` §7.7 SC-6(d), cited; §C.3 Category 2, §C.4(c), §A.6.3 and frozen §D.1
   item 2 are where this fixture's UNSCORED members are named). Each of those is a citation,
   not a restatement.
3. **The locked ordering of line 480 binds this file** — `PREREG.md` §6.2 SC-8(a) (everything
   the gate consumes freezes at the tag) is its enforcement, cited; §D.1 is the exhaustive
   enumeration of frozen objects SC-8(a) requires this declaration to supply, so no number here
   can be moved after a fixture result is observed.

---

### A.11 — Walk summary

**The Line column holds v30 line numbers, as of the `prereg-v30` tag (R95/§148.1).** The v30a
positions differ — the amendment inserted 981 lines after line 99 — and the numbers here are **not**
renumbered, because the walk records which *registered* elements were amended and renumbering would
falsify that record. Resolve them with `git show prereg-v30:PREREG.md`.

**Why line 478 has no row, and keeps none (§148.2).** It is the one non-blank §6.2 line this walk
does not cover. **A row is not added now**: a walk row asserts a verdict reached by walking, and no
walk of that line happened. The line is handled instead by **specific disclosure at D-STALE**, by
line and by quotation. Adding a row would assert a walk that did not occur, which is the defect this
table exists to prevent.


| §6.2 element | Line | Verdict |
|---|---|---|
| Reference AUC 0.957/0.675, ±0.010 | 445 | **AMENDED (class C)** — retired; LightGBM trio governs |
| Ground-truth column DAG + independent-leak count | 446 | SATISFIED — count 25, F3 scope governing; **no gate arithmetic attached** (R11); flavor split stated both ways (R13) |
| Declaration reconstructed, evidence before tuning | 447 | SATISFIED |
| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED **as to ordering** — but see §A.5: a cross-tool comparison ran 14 Aug 2026 and does **not** satisfy §9.2 (commitment clause breached and uncurable; acceptance-fixture half not run; criterion 3 unevaluated). D-003. |
| Semantic-ambiguity clause | 449 | SATISFIED — clause does not fire |
| Contamination availability class in manifest | 450 | **SATISFIED BY SUBSTITUTE (class C)** — locus amended to this declaration, hashed in the tag |
| Sliced variant for CI | 451 | **AMENDED (class C)** — off the Phase 0 fixture; re-registered as a Phase 1 CI obligation with its scoring rule declared ex ante |
| Pass gate framing; frozen default config | 453, 457 | SATISFIED |
| Criterion 1 | 459 | SATISFIED — **denominator re-derived from the declared map (R11); N = 11**; three-class partition summing to 35 |
| Criterion 2 | 460 | SATISFIED — scope is manifest-CLEAN columns only; the §C.3 mis-routing is deleted |
| Criterion 3 | 461 | **AMENDED (class C) per R9** — scored against the declared map |
| Criterion 4 (identity control) | 462 | SATISFIED — with the 4.29e9 sentinel statement |
| Descendants secondary; top-k; alias | 464, 468 | SATISFIED |
| k-of-N proof count, published as a count | 470-476 | SATISFIED — **N = 11** |
| Ordering, locked | 480 | SATISFIED — enforced by §D.1 |

**Four §6.2 sites are amended in this walk (445, 450, 451, 461). The ledger of record for what
the amendment comprises is the amended registration's own v30a amendments block (`PREREG.md`);
this table is a walk summary, not that ledger (`PRACTICES.md` P-61).** NO registered §6.2
element is left NOT MET, and none is left "outstanding". Every element is now either SATISFIED
as registered, AMENDED with the old text quoted and the new text cited to its registered site,
or SATISFIED BY SUBSTITUTE with the substitute named and shown to bind at least as hard.
Everything not amended stands exactly as registered. The class of each amendment is `PREREG.md`
§0.2.1 line 93's and it is carried under line 95; all are PROVISIONAL until the `prereg-v30a`
tag is signed.

---

### A.12 — "Waived" — defined at `PREREG.md` §10.2 [SC-12]; this subsection records the gap that forced it (finding RS-3) and corroborates

**Outside §6.2 and kept in the walk because the walk is where the gap was found.** This
subsection defines nothing. The defining clause is registered at `PREREG.md` §10.2 [SC-12] and
is cited here, not restated; what follows is the record of the gap, and what this declaration
supplies and corroborates under SC-12.

**Registered text, PREREG.md line 1035 (verbatim):**

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

Context, PREREG.md line 1033 (verbatim), which is what that floor floors:

> On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**The gap (RS-3), as found.** "Waived" appeared in the floor with no defining clause anywhere in
the registration. It appeared once more, at PREREG.md line 855, as a **detector-case coverage
state** in §7.7's vocabulary table — also undefined. An undefined term inside a floor that
exists to stop criteria being dropped silently is the exact shape of a term that gets read
permissively later. That gap is closed by the amended registration, not by this file.

**Where the definition lives, and what it carries — cited, not restated.** `PREREG.md` §10.2
[SC-12] registers the defining clause of "waived" (its head and limbs (i)–(v)), the rule that
it may not be invoked, and the seven limits on what the definition does not permit; §7.7's
pointer beneath the coverage-state table makes that definition govern the word wherever it
appears. This subsection adds nothing to SC-12 and claims no authority over it.

**What this declaration supplies under SC-12, and what it corroborates:**

1. **Which detectors the floor governs is not this declaration's to choose** — `PREREG.md` SC-12
   and SC-13c(c3) pin the governed set to §7.1's two runtime metric rows and line 1039's "both
   of L2a/L3.1's combinations". This file's statement that the two runtime detectors are L2a
   and L3.1 (PREREG.md lines 318, 320) is corroboration of that registered set, not its source.
2. **On this fixture a cell with no data is `unscored`, not "waived"** — the case SC-12 item (4)
   governs. The 72 such cells are ledgered by name and missing path (§13(g), `n1\unscored_ledger.csv`;
   §A.6.3), which is the entry condition `PREREG.md` §7.7 SC-6(b) requires; their gate
   disposition is SC-6(a)'s, cited.
3. **The replacement criterion's unit, threshold, and denominator are not supplied by this
   file.** Where §6.2 line 449's ambiguity branch has fired and been recorded, `PREREG.md`
   §10.2 [SC-13a], [SC-13b] and [SC-13c] register them; whether the branch fires for this
   fixture is the reading of line 449 recorded at §A.5, on which see K4_SCRUB_DIFF.md (row
   28). Nothing in this subsection bears on that question.

**Status** (bookkeeping; `PRACTICES.md` P-65): SC-12 is class C amendment content carried by the
amended registration, PROVISIONAL until the `prereg-v30a` tag is signed and frozen under
`PREREG.md` SC-8 thereafter; any reading of it is governed by SC-9(e).

## 8. Fixture identity (element a)

> **SCORED ON ARTIFACT B** (§0.2). This section IS Artifact B's identity statement — the
> artifact enumeration `PREREG.md` §6.2 SC-2(a) requires (the fixture, by side, with
> provenance), with the reference-anchor entries SC-2(d) requires and the declared exclusion
> SC-2(b) governs.

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

**The exclusion is HARD — `PREREG.md` §6.2 SC-2(b) (changing the composition is class C — never
a deviation, never a working resolution), cited and not restated.** The pc2 timestamped variant
set is a declared exclusion under SC-2(a)–(b): outside the declared fixture and outside every
number in this file, and named only so that its absence is auditable. Any future use of it — in
the gate, in a slice, as a robustness check, or as a supplementary report — is the composition
change SC-2(b) governs.

## 9. Shared label vector — the feature-availability-only licence (element b)

> **SCORED ON ARTIFACT B** (§0.2) — a raw-bytes comparison of Artifact B's own stored columns.
> **§0.4 records what this licence additionally depends on and cannot itself establish:** that
> Artifact B's two sides share ONE column universe. A shared label vector is not a shared
> feature set.

All 64 main-set pairs are bit-exact identical on `true_label`, `fwd_move_ticks`, AND
`mid_price_t` (raw-bytes comparison after dtype/length checks): one shared label vector per
pair. This is the measured basis on which the pre/post AUC delta is read as a
feature-availability-only effect — labels, label bases, and evaluation populations are
identical across sides (the interpretation practice is recorded in `PRACTICES.md` P-68; the
fixture-admission bound it rests on is `PREREG.md` §6.2 SC-2(c)'s, §0.4). Evidence:
`c3\label_equality.csv` lines 2-65 (all 64 rows True/True/True, no first_diff_index).

## 10. EVIDENCE for §1's declared boundary — measurement of the corrected features' information boundary (element c; R2)

> **MEASURED ON ARTIFACT A** (§0.1) — the f2 lineage's lattice and event joins. Artifact B
> stores no feature columns, so this measurement cannot be taken on it (§0.2).

**This section states no rule.** §1 carries the single normative statement of the boundary
(`floor(t-1) + 1s`). This section is its evidence: what was measured, on what, against which
comparator, and how the cross-checks line up — the measurement and artifact record `PREREG.md`
§2.9 SC-1(a) requires beside a declared measured value (instance).

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
two count sets agree because they must, and this declaration does not count their agreement as
independent corroboration (`PRACTICES.md` P-70). The genuinely
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

> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice.

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

> **MEASURED ON ARTIFACT A** (§0.1) — the lineage's own snapshot files. This section is also
> what licenses the §0.2 lattice bridge from A to B, so its generation identification is
> load-bearing in both directions.

The element-level statements live in §2 (`bar_duration`) and §3 (`timestamp_semantics`). This
section is the consolidated declaration record, because these facts bear on every count in
Part II and on what a "clean" instrument-month means.

**B.1 — The enumeration.** Every `{inst}_snapshots_{month}.parquet` copy under the read-only
archive was enumerated by exhaustive `os.walk`: **228 files**, 100% accounted for, none skipped,
each with size, mtime, sha256, md5, generation, manifest coverage, total and filtered row counts,
first/last timestamp, column count, and the two spacing counts (`subsecond_spacing_rows`,
`nonexact_1s_gap_rows`) — all 228 rows carry every one of those. **BLOCK STRUCTURE WAS MEASURED
ON 84 OF THE 228, NOT ON ALL OF THEM (corrected here).** The seven block-structure columns
(`native_blocks`, `overlapping_block_pairs`, `max_rows_per_timestamp`, `duplicate_timestamps`,
`filtered_distinct_seconds`, `filtered_max_rows_per_second`, `filtered_excess_rows`) are
populated on exactly **84 rows — the 48 fixture-path v3 files plus the 36 v4 files** (30
`v4_gapfill` + 6 `v4_morning_chunk`) — and are EMPTY on the other **144**, which are the copies
under the four non-measured location families (`D_PC2_TRANSFER_v4` 48, `E_pc2_transfer_processed`
48, `F_pc2_transfer_transfer_data` 24, `G_transfer_data` 24) and carry identity, generation,
manifest coverage, row counts and spacing counts only. The 84 are exactly the file set §3 calls
"all 84 measured files" and §B.4's "36 v4 rows". **Every manifest-covered file MATCHES its
recorded md5; zero MISMATCH across all 228.**
Evidence: `n2\lattice_provenance.csv` (228 rows, 84 of them with block structure),
`n2\provenance_notes.md`, `n2\inventory_run.log`; `n2\block_overlap.csv` (the 84).

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
| cl, es, gc, **nq (TRADES-CLASSES-ONLY)**, zc, zs (36 of 48) | v3_pre_gapfill | **Yes, and it is the canonical one** | **NOT COVERED by any manifest at that path** |

**Label carried on nq in the row above, per §13(g)'s binding obligation:** nq is
**TRADES-CLASSES-ONLY** — 4 of 10 classes scored; its six MBO classes are UNSCORED, not zero,
because **there is no MBO file at the fixture path `processed\nq\`** (not "no data exists", and
not "no same-generation data": same-generation v3 NQ MBO exists at
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`, a path the builder never reads — §13(g),
§13(h)). The label is required on **every** appearance of nq in a table, including this one,
which is about lattice provenance and not about map coverage.

For he and le the fixture file *is* the canonical v4-package file (archive `PC2_SETUP_README.txt`,
verbatim: "he/ 24 files (v3 canonical; no reprocessing)" and the same line for le). For the other
six the fixture file is the generation the archive itself superseded —
`MASTER_FINDINGS\v4\G2_G3_summary.txt` records "G2: 72/72 (instrument, month) cells reprocessed
successfully (NQ + ZS + ZC + ES + CL + GC, each 12 months)". **36 of the 48 fixture-path files
are covered by no manifest**; for gc, nq, zc and zs a byte-identical copy under `transfer\data\`
is manifest-covered (transitively attested, 24 files), and **for cl and es no manifest covers the
v3 generation at all** — their integrity rests solely on the sha256/md5 recorded in
`n2\lattice_provenance.csv`. Evidence: `n2\provenance_notes.md` §(e).

**B.4 — The delivered lattice departs from a 1 Hz grid on TWO DIFFERENT COUNTS, and the label
belongs to whichever count is being quoted: 18 of 48 fixture-path instrument-months are
MULTI-BLOCK (`native_blocks` > 1 with `overlapping_block_pairs` > 0), while 41 of 48 carry
FILTERED EXCESS ROWS (`filtered_excess_rows` > 0) and are therefore not exact 1 Hz grids; only 7
of 48 carry zero excess.** The 18 are a strict subset of the 41 — the other 23 are single-block
months carrying 1-17 excess rows at no more than 2 rows per second (§2) — because MULTI-BLOCK
describes the file's assembly and EXCESS describes the delivered grid. Both counts are read from
`n2\block_overlap.csv`'s 48 fixture-path rows. Root cause of the 18 is the
unsorted, non-deduplicated per-day concatenation at `process_mbo.py` L584-590 (quoted verbatim
in §3), with the day-end and gap-re-anchor hypotheses REFUTED by measurement (25 of 211,450 =
**0.012%** on ZC 2025-08) and up to **5 rows sharing one exact ns timestamp**.

**The v4 comparison, stated precisely (corrected this pass).** All 36 v4 files are
single-block (`native_blocks == 1`, `overlapping_block_pairs == 0`). **The exact 1 Hz totals
— 378,000 / 680,400 / 604,800 / 324,000 and the rest — are DISTINCT-SECOND counts
(`filtered_distinct_seconds`), not row counts (`filtered_rows`).** The two coincide in only
**12 of the 36** files; the other **24 carry 1-5 filtered excess rows** over their
distinct-second count, with **at most 2 rows sharing any one second**
(`filtered_max_rows_per_second` = 2 on all 24). Worked example from the same artifact: zc
2025-01 v4 = 378,000 rows over 378,000 distinct seconds (excess 0), while zc 2025-08 v4 =
366,005 rows over **366,000** distinct seconds (excess 5). The v4 generation is therefore an
exact 1 Hz grid *in its second coverage*, not in its row count, and the earlier wording
("exact 1 Hz totals", "clean") conflated the two. The contrast with the v3 fixture generation
is unaffected in kind and enormous in degree: v3's excess runs to 211,450 rows on ZC 2025-08
with up to 5 rows on one exact nanosecond, against a v4 maximum of 5 rows and 2 per second.
Evidence: `n2\block_overlap.csv` (columns `native_blocks`, `overlapping_block_pairs`,
`filtered_rows`, `filtered_distinct_seconds`, `filtered_max_rows_per_second`,
`filtered_excess_rows`; 36 v4 rows); `n2\provenance_notes.md` §(c);
`n2\spacing_classification.csv`.

**B.5 — Why this is a declaration fact and not trivia.** The **18 MULTI-BLOCK** instrument-months
— **not** the wider 41 that carry filtered excess rows — are exactly the 18 in which the
corrected side is non-zero (§13(b)): same list, cl x6, gc x6,
zc 2025-08/-09/-10, zs 2025-08/-09/-10. **The alignment is with the MULTI-BLOCK criterion and
with that criterion only:** the 23 single-block instrument-months that carry 1-17 excess rows are
corrected-side ZERO, so quoting the 41 here would break the correspondence that makes this
section load-bearing. The generation defect *is* the mechanism that makes the
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

> **MEASURED ON ARTIFACT A** (§0.1) — both-branch counts come from `t1\violation_table.csv` and
> `n1\declared_map.csv`. The tie DECLARATION itself is a declaration, not a measurement, and
> governs the scoring of Artifact B.

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

**The 49 exactly-equal events are NON-VIOLATIONS under the declared branch.** Under
`PREREG.md` §2.3's comparator, `ties: available` row (cited), a cell with `a(j,c) == d(i)` is
available; the 49 (20 trade + 29 MBO, ZC 2025-01) therefore do not violate and are not required
findings, and a detector that fires on one of them has produced a **false positive** under the
declared branch. They are published only as the both-branch disclosure above, which is an
**informational disclosure** in the sense of `PREREG.md` §2.9 SC-1(f) (one comparator branch is
scored; cited, not restated): it exists so that a reader can see exactly what the tie choice
moved. Re-scoring it as findings would change the tie declaration, which is class C after the
tag (§D.1 item 1). *(Instance: this section supplies the declared `ties` branch SC-1(f)
requires, with the figures under the non-declared branch labelled as informational.)*

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

> **MEASURED ON ARTIFACT A** (§0.1) — every cell of the map is an event-to-row timing
> measurement on the lineage's lattice and event parquets. **APPLIED TO ARTIFACT B** through
> the §0.2 lattice bridge: the map is the key the gate scores Artifact B's findings against.
> Both halves of that sentence must appear wherever a map number is quoted.

**This section replaces the former "corrected-side zero".** That claim was falsified by
measurement (subsection (f)); working resolution R9 (file tail, verbatim) is the authority for
what stands in its place: "The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on
both fixture sides, not against an assumed-clean corrected side."

### (a) What the map is, and where it lives

**Artifact: `n1\declared_map.csv`** — the map artifact with its declared schema that `PREREG.md`
§6.2 SC-3(a) (what the map is) requires; cited, not restated. **Cell key, declared and named:**
(`side`, `instrument`, `month`, `class`) — the unit this declaration partitions the fixture
into. One row per scored cell, schema
`side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag,
missing_path`, the last two being the field that records whether the cell is scored and its
ground. Read this pass: **984 rows** = **960 declared-class cells** (2 sides x 8
instruments x 6 months x 10 classes) **plus 24 rows carrying the 11th diagnostic class**
`mbo_all_rows`. Of the 960: **888 `SCORED`** and **72 `UNSCORED_FOR_LACK_OF_DATA`**; the 24
diagnostic rows are flagged `SCORED_DIAGNOSTIC_11TH_CLASS`. Boundary is `decision_T` on every
row. Scope: 8 instruments (cl, es, gc, he, le, nq, zc, zs) x 6 months (2025-01, 2025-08,
2025-09, 2025-10, 2025-11, 2025-12) = 48 instrument-months.

**The declared 10 classes** are trades_all, trades_buy, trades_sell, trades_large, mbo_all,
mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any.

> **CLASS SET — declared as `PREREG.md` §6.1 SC-10(c) (diagnostic classes are not declared
> classes) requires; cited, not restated.** `mbo_all_rows` is an **11th diagnostic class and is
> NOT one of the declared 10**; every statement of the form "max across classes" in this file
> names the class set it maximises over, as SC-10(c) requires. Two M5-quoted maxima came from the
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
corrected rows = 19.16%** (`max_strict_frac` 0.191643) on class `mbo_all`, and zc 2025-09 is the
peak under BOTH metrics.

**THE RANKING BELOW IS BY RATE**, i.e. by `max_strict_frac` = `max_strict` / `rows`, descending.
**The metric is named because the rate order and the absolute-count order are different orders**
(`PRACTICES.md` P-77; for the peaks themselves the requirement is `PREREG.md` §6.1
SC-10(d)(4)'s). *(Instance: per-cell map data, SC-3(a).)* `argmax_strict` is
`mbo_all` on all 18 and `classes_scored` is 10 on all 18. Derived from
`n1\summary_corrected.csv` (rows with `max_strict` > 0), reproduced cell-for-cell with zero
disagreement by `y1\trade_class_only_map.csv` (`max_strict_declared10`, `rows`, side =
`corrected`). All 18 are listed — the set is small enough that a top-N would only re-create the
truncation defect this table replaces.

| rate rank | instrument-month | strict | corrected rows | rate (`max_strict_frac`) | absolute rank |
|---|---|---|---|---|---|
| 1 | zc 2025-09 | 111,334 | 580,944 | **19.16%** (0.191643) | 1 |
| 2 | zc 2025-10 | 109,332 | 634,445 | 17.23% (0.172327) | 2 |
| 3 | zc 2025-08 | 90,868 | 554,303 | 16.39% (0.163932) | 3 |
| 4 | zs 2025-08 | 64,404 | 465,381 | 13.84% (0.13839) | 5 |
| 5 | zs 2025-10 | 60,559 | 508,910 | 11.90% (0.118997) | 6 |
| 6 | zs 2025-09 | 45,255 | 429,465 | 10.54% (0.105375) | 11 |
| 7 | gc 2025-10 | 71,584 | 772,447 | 9.27% (0.092672) | 4 |
| 8 | gc 2025-09 | 59,691 | 734,280 | 8.13% (0.081292) | 7 |
| 9 | cl 2025-11 | 48,607 | 703,999 | 6.90% (0.069044) | 10 |
| 10 | cl 2025-01 | 53,249 | 801,410 | 6.64% (0.066444) | 8 |
| 11 | gc 2025-12 | 49,649 | 772,202 | 6.43% (0.064295) | 9 |
| 12 | gc 2025-08 | 42,886 | 692,041 | 6.20% (0.06197) | 12 |
| 13 | cl 2025-10 | 42,377 | 745,569 | 5.68% (0.056838) | 13 |
| 14 | cl 2025-12 | 38,945 | 768,531 | 5.07% (0.050675) | 14 |
| 15 | cl 2025-09 | 34,010 | 687,658 | 4.95% (0.049458) | 16 |
| 16 | gc 2025-01 | 37,065 | 761,736 | 4.87% (0.048659) | 15 |
| 17 | gc 2025-11 | 30,577 | 674,038 | 4.54% (0.045364) | 17 |
| 18 | cl 2025-08 | 27,852 | 664,076 | 4.19% (0.041941) | 18 |

**The two orders diverge, which is the whole reason the metric must be named:** zs 2025-09 is 6th
by rate and 11th by absolute; gc 2025-10 is 7th by rate and 4th by absolute; cl 2025-01 is 10th by
rate and 8th by absolute. **Under the ABSOLUTE metric the top five are** zc 2025-09 (111,334),
zc 2025-10 (109,332), zc 2025-08 (90,868), gc 2025-10 (71,584), zs 2025-08 (64,404).

> **WITHDRAWN: the earlier prose list** "Next: zc 2025-10 …; zc 2025-08 …; zs 2025-08 …; gc
> 2025-10 …". **Every number in it was correct; the ORDERING was not a ranking under either
> metric** — it ran zs 2025-08 (64,404) ahead of gc 2025-10 (71,584), which is not absolute
> order, and it terminated at gc 2025-10 (9.27%) while omitting **zs 2025-10 (60,559 of 508,910 =
> 11.90%)** and **zs 2025-09 (45,255 of 429,465 = 10.54%)**, both of which outrank gc 2025-10 by
> rate. The table above replaces it; no truncated restatement of it may be quoted.

**Equal counts, stated precisely:** `equal_count` is non-zero in **35 of 48** instrument-months;
of those, **17 are equal-only** (equal > 0 with strict == 0) and the other 18 are the
strict-positive cells above. That leaves **13 instrument-months with zero strict and zero equal
over the classes that are SCORED for them**. 18 + 17 + 13 = 48.

> **"Clean on both branches" is WITHDRAWN as a pass claim for the six nq months (working
> resolution R12)** — `PREREG.md` §7.8 SC-11(f) (a zero over a partial population is not a zero
> over the population) governs and is cited, not restated. The arithmetic above is a
> measurement and stands; the *label* does not. For nq, zero-over-scored-classes and
> zero-over-the-declared-10 differ by six unscored classes per month. The 13 rows below are
> therefore listed as **measured-zero over their scored classes**, with the scored-class count
> named on every row — the population each zero is zero over, which SC-11(f) requires named.
> Seven of the thirteen are zero over all ten declared classes; six — every nq month — are zero
> over four. **What a row of such a table may be quoted as is SC-11(f)'s, cited; the six nq
> rows in particular are not evidence of cleanliness.**

**The 13 measured-zero instrument-months, named, with their scored-class count:**

| instrument-month | corrected rows | note |
|---|---|---|
| nq 2025-01 | 598,227 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 MBO classes UNSCORED, not zero. NOT a pass.** |
| nq 2025-08 | 540,530 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-09 | 549,430 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-10 | 590,785 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-11 | 550,463 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-12 | 620,107 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| zc 2025-01 | 338,158 | all 10 classes scored (see (e)) |
| zc 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-01 | 337,844 | all 10 classes scored |
| zs 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-12 | 353,103 | all 10 classes scored |
| he 2025-11 | 304,486 | all 10 classes scored |
| le 2025-11 | 304,491 | all 10 classes scored |

> **The six nq cells are NOT evidence of cleanliness.** `n1\summary_corrected.csv` records
> `classes_scored = 4` for every nq month: **nq's coverage in this map is TRADES-CLASSES-ONLY**
> — `trades_all`, `trades_buy`, `trades_sell`, `trades_large`. Its six MBO classes are
> **UNSCORED, not zero.** Reading "nq is clean" off this table is exactly the inference R9
> forbids.
>
> **The reason, restated correctly — it is NOT that no data exists, and it is NOT that no
> same-generation data exists** (R12, whose stated reason §13(h) supersedes on measured
> evidence). The earlier draft said the NQ MBO data does not exist; R12 replaced that with "no
> same-generation data". Both are false and are corrected here. **NQ MBO exists in the archive in
> TWO generations — one of them the fixture's own v3 — and what does not exist is an MBO file AT
> THE FIXTURE PATH.** `phase5_ml.py`'s `get_data_dir` resolves to `PROC/sym` = `processed\nq\`
> (because `C:\MBO_data` does not exist), and that directory holds **no MBO file of any
> generation** — which is exactly the file `n1\unscored_ledger.csv` records as missing
> (`missing_path` = `...\processed\nq\nq_mbo_{month}.parquet`, 6 rows, 12 cells each). The two
> families that do exist are **v4_gapfill** per-day parquets under
> `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\v4_gapfill\nq_mbo_YYYY-MM\` and
> **same-generation `v3_pre_gapfill`** month files under
> `pc2_transfer\processed\nq\nq_mbo_{month}.parquet` — a path the builder never reads (§13(h),
> verified this pass). **NQ's six MBO classes are therefore UNSCORED because the fixture path
> carries no MBO file**, and adopting either family into the acceptance denominator is class C.
>
> Both joins are worth having and both run as a **declared non-gated diagnostic** — §13(h). The
> v4 join is additionally **cross-generation**: §B.4's generation defect is precisely a
> lattice-timestamp defect, so the two generations do not share a row-to-second correspondence
> and a v4-event / v3-lattice count reports the mismatch as well as the fixture. The v3 join is
> the same-generation control. Neither is in the acceptance denominator, and moving either there
> later is class C.

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
`timestamp` column of the snapshot frame. That is what satisfies `PREREG.md` §6.2 SC-8(c) (ex
ante means checkable before any detector runs — cited, not restated) for the **declared cohort
definition** in §C; this predicate and its coverage are the declared cohort SC-8(c) requires
regenerable from the declared inputs alone. `n3\cohort_profile.csv` also records
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
x 2 sides = 72.

**Cause, stated correctly: NO MBO FILE AT THE FIXTURE PATH — not "no data exists", and not "no
same-generation data" either** (R12, whose stated reason §13(h) supersedes on measured evidence).
`phase5_ml.py`'s `get_data_dir` resolves to `PROC/sym` = `processed\nq\` (because `C:\MBO_data`
does not exist), and `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\nq_mbo_{month}.parquet`
does not exist — that directory holds **no MBO file of any generation**. The `missing_path`
column names that exact absent file for each cell (`n1\unscored_ledger.csv`, 6 rows, `n_cells` =
12 each). **NQ MBO data does exist in the archive, in TWO families, neither of which the builder
reads**: `v4_gapfill` per-day parquets under `processed\nq\v4_gapfill\nq_mbo_YYYY-MM\`, and
**same-generation `v3_pre_gapfill`** month files under
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet` (§13(h) items 1-2, verified this pass).
Adopting either family into the acceptance denominator is a class C amendment; the v4 family
would in addition require a cross-generation join whose counts report the generation mismatch as
well as the fixture (§13(b), §13(h)). **Any statement of this cause that says "no NQ MBO data
exists", or that says same-generation NQ MBO data is absent, is wrong and is withdrawn.**

**Gate consequence:** `PREREG.md` §7.7 SC-6(a) and SC-6(e) (the `unscored` state at cell level;
the pass prohibition is absolute), with §6.2 SC-3(b) — cited, not restated. What this
declaration supplies is SC-6(b)'s cell-level unscored ledger: the 72 cells above, by name, with
their ground (no MBO file at the fixture path) and missing path (`n1\unscored_ledger.csv`),
frozen at the tag (§D.1 item 3). R9's rationale ("silence and belief never convert into a pass")
is the working resolution that recorded the principle for this fixture. **Labelling practice for
nq in this file** (`PRACTICES.md` P-83): every appearance of nq in a table carries the
**TRADES-CLASSES-ONLY** label together with the correct reason — **no MBO file at the fixture
path `processed\nq\`**, where `get_data_dir` resolves because `C:\MBO_data` is absent — never
"no data exists" and never "no same-generation MBO data". Same-generation MBO **does** exist, at
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`, a path the builder never reads; adopting
either that family or the v4 family into the acceptance arithmetic is the class C move
`PREREG.md` §6.1 SC-10(b) governs.

### (h) NON-GATED DIAGNOSTIC — the NQ cross-generation MBO measurement (item X4)

**This subsection is declared NOT PART OF THE GATE — the marking `PREREG.md` §6.1 SC-10(a) (a
declaration may carry data the gate does not consume, if it says so in terms) requires, under
SC-10(b)'s condition on the exemption; cited, not restated.** It is separated from (a)-(g) for
exactly that reason, excluded from the §D.1 freeze (item 6), and labelled at every point of use
*(instance: non-gated data, marked)*.

**What it is.** §13(g) records that nq's six MBO classes are unscored because **the fixture path
`processed\nq\` holds no MBO file of any generation** — not because the archive lacks NQ MBO, and
not because it lacks same-generation NQ MBO; the PREMISE CORRECTION below supersedes R12's stated
reason on measured evidence. The information is nevertheless worth having, so the measurement is
run against the archive's out-of-path MBO families and reported here as a **declared non-gated
diagnostic** under working resolution R12: v4 NQ MBO events
(`processed\nq\v4_gapfill\nq_mbo_YYYY-MM\nq_mbo_YYYYMMDD.parquet`), with the same-generation v3
month files (`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`) as a control, measured against
the v3 fixture lattice, on the same strict/equal/`decision_T` definitions as the map.

**What it can and cannot support.**

- It **cannot** satisfy criterion 1, cannot convert any of the 72 unscored cells into scored
  cells, and cannot be quoted as a pass or a fail for nq.
- Its counts are **cross-generation**: the v3 lattice carries the §B.4 timestamp defect and the
  v4 lattice does not, so a v4-event / v3-lattice join reports a quantity that mixes the
  overhang with the generation mismatch. It is a diagnostic of *whether an MBO overhang is
  present at all* on nq, not a measurement of the fixture's own MBO overhang.
- **Moving it into the acceptance arithmetic later is class C** — `PREREG.md` §6.1 SC-10(b)
  (the exemption is conditional), cited; not a working resolution and not a `DEVIATIONS.md`
  entry.

**Results (folded in by the orchestrator, 2026-08-12, from item X4; artifacts under `x4\`).**

**PREMISE CORRECTION — R12's stated reason is superseded by X4's own search, and this is the
third and (as measured) final statement of it. Recorded here as fact; the tail record of R12 is
append-only and is not edited.** R12 gives the reason for not gate-scoring nq MBO as "no
same-generation MBO data: the available NQ MBO is v4_gapfill". X4's exhaustive walk of the
archive root (26,596 files, 262 `nq*mbo*.parquet` hits) found **two** families, not one:

1. **v4** — `processed\nq\v4_gapfill\nq_mbo_{month}\nq_mbo_YYYYMMDD.parquet`, 250 per-day files,
   mtime 2026-04-16. (This is the family that falsified the earlier "no data exists" wording.)
2. **v3, same generation as the fixture lattice** — `pc2_transfer\processed\nq\nq_mbo_{month}.parquet`,
   12 month files, mtime 2026-03-31/04-01. Generation verified two ways: the sibling
   `pc2_transfer\processed\nq\nq_snapshots_2025-08.parquet` and the fixture-path
   `processed\nq\nq_snapshots_2025-08.parquet` share sha256
   `1A200A3A71A597C84E869D0CE647195B86250C0D28E3D0C813A3AAF40F1304D7`, and its build stamps
   interleave with the v3 snapshots/trades and precede every v4 artifact.

So the correct reason nq MBO is not gate-scored is **not** that same-generation data is absent.
It is that **the fixture path has no MBO file**: `phase5_ml.py`'s `get_data_dir` resolves to
`PROC/sym` = `processed\nq\` (because `C:\MBO_data` does not exist), and that directory contains
no MBO file of any generation. The v3 month files sit at a path the builder never reads.
Adopting either family into the acceptance denominator is a **class C amendment** — not
performed, not authorized here; `n1\unscored_ledger.csv` is untouched.

**Provenance fact recorded in passing:** no MBO file of either generation is covered by any
manifest in the archive — neither `PC2_TRANSFER_v4\manifest.csv` nor either `checksums.txt`. The
MBO layer is unattested archive-wide.

**Join soundness (measured before any count was reported).** The generational difference is not
a different event set on shared days but a smaller DAY set:

- Day coverage: the v4 day set is a strict subset of the lattice's — 126 of 154 dates, with
  `v4_only = 0` in every month. 78,353 of 3,449,548 lattice rows (2.272%; 5.824% in 2025-11) sit
  on v4-uncovered dates and therefore score as non-violating by construction, so **every v4
  contaminated strict count is a lower bound**. 24 of the 28 uncovered dates are thin spillover
  or Sunday-reopen fringes; **four are real sessions** — MLK 2025-01-20, Labor Day 2025-09-01,
  Thanksgiving 2025-11-27 and 11-28 — which alone are 63,448 (81%) of the uncovered rows. The
  hole is intrinsic to the v4 generation (its own snapshot lattice carries the same day set),
  not a transfer defect.
- Event counts on the 126 shared days: v4 exceeds v3 by **+0.12% to +0.19%** every month, per-day
  never negative (min +0.066%, median +0.154%, max +0.307%) — consistent with gap-fill adding
  rather than replacing.
- Timestamp alignment on covered days: session start agrees to the minute on 126 of 126; session
  end on 105 of 126, with the 21 exceptions characterized (14 are a 0.07-second overshoot at
  early closes; 6 are v3-lattice truncation confirmed by the v3 MBO source ending at the same
  point; 1 is a genuine v4 overrun).
- Soundness test: restricting **both** joins to the 126 v4-covered days collapses the
  cross-generation deficit — max |strict delta| from 27,194 to **745** (0.14%, the same order as
  the event-count delta) and max |equal delta| from 217 to **1**. The worst unrestricted delta is
  entirely the two Thanksgiving sessions.

**Corrected side, boundary decision_T: `strict_count = 0` in EVERY cell** — all six declared MBO
classes plus the diagnostic `mbo_all_rows`, all six months, under **all four joins** (v4, v3
same-generation, and both day-restricted). Corrected rows 598,227 / 540,530 / 549,430 / 590,785 /
550,463 / 620,107. `equal_count` is **0–7** per class (v4 `mbo_all` 5/5/5/5/3/5; v3 6/7/5/5/3/5;
the maxima are 6 in the v4 map at 2025-12 `mbo_all_rows` and 7 in the v3 map at 2025-08, on both
`mbo_all` and `mbo_all_rows`), **bounded by the lattice's 3–7 same-second rows per month**
(6/7/5/5/3/6) — the range and bound `x4\join_soundness.md` states. **The day hole cannot be masking
a corrected-side violation**, because the same-generation source that does cover those dates also
reports 0.

**Contaminated side, v4 join, `mbo_all` strict (rate on the full v3 lattice denominator):**
573,849 (95.92%) / 524,025 (96.95%) / 523,307 (95.25%) / 576,402 (97.57%) / 516,516 (93.83%) /
614,563 (99.11%) for 2025-01/08/09/10/11/12. All-class v4 rate range 93.01%–99.26%; on the
day-restricted denominator 96.00%–99.71%, so the sub-94% cells are the day-hole artifact, not a
lower contamination rate. **v3 same-generation control** (no day hole, the sounder of the two but
equally non-gated): `mbo_all` strict 588,354 (98.35%) / 523,573 / 532,341 / 576,194 / 543,253 /
614,564 (99.11%), all-class range 94.58%–99.26%.

Artifacts: `x4\nq_mbo_diagnostic.csv` (the mandated deliverable), `x4\join_soundness.md`,
`x4\nq_mbo_v3_same_generation_map.csv`, `x4\restricted_to_v4_covered_days_{v4,v3}source.csv`,
`x4\per_day_coverage.csv`, `x4\soundness_{a,b}_*.csv`, `x4\v4_vs_v3_count_delta.csv`, run logs.

### (i) BOTH MAPS, published side by side — the full-class map AS MEASURED and the fixture-universe-restricted map (R17(ii))

**The obligation, stated first.** Both maps are published side by side with the delta explicit
and neither replaces the other — `PREREG.md` §6.2 SC-3(e) (one scoring key, and only one),
cited and not restated; delta-issued working resolution **R17(ii)** is the record of its
adoption for this fixture (`PRACTICES.md` P-87 records the publication practice). *(Instance:
the restricted map below is the reporting re-aggregation, with its delta, that SC-3(e)
governs.)* The
full-class map is the measurement and is what `n1\declared_map.csv` contains; the restricted map
is a re-aggregation of that same artifact over a narrower class set, adding no new measurement
and changing no cell. Source for the restricted figures: `y1\trade_class_only_map.csv` (96 rows
= 48 instrument-months x 2 sides, both class scopes on every row), re-derived from
`n1\declared_map.csv` by `y1\y1_trade_class_map.py`.

**THE RESTRICTED MAP'S JUSTIFICATION — BY THE COLUMN-UNIVERSE CRITERION ALONE (R17(i)).**

> **No fixture column consumes the MBO event source.** `phase7_l2_sim.py` opens exactly **two**
> data files in the whole script — `{sym}_snapshots_{month}.parquet` (path L135, read L139) and
> `{sym}_trades_tagged_{month}.parquet` (path L199, read L201) — and opens no MBO parquet and no
> MBO aggregate anywhere. `ALL_L2_FEATURES` (L108) contains **none** of the ten MBO-derived
> Phase 5 columns. The script asserts its own scope four times: L4 "L2 features only (no L3/MBO
> cancel/add/rate features).", L57 "# L1 + L2 FEATURE DEFINITIONS (35 total, NO L3/MBO
> features)", L128 "Build L1+L2 features for one month. NO L3/MBO features.", and L549
> `assert len(features) == 35`. Column by column, all 35 trace to: snapshot parquet **13**,
> trades parquet **11**, snapshot-derived **9**, clock-only **1** (`minutes_since_open`), MIXED
> snapshot+trades **1** (`vwap_distance`). **MBO-fed: 0 of 35.** Evidence:
> `y1\column_universe.csv` (35 rows, each with its construction quote and upstream line
> numbers); Y1 §1.1, §2, §3.1, §3.2.
>
> **The criterion follows from that alone:** a map class whose event source no fixture column
> consumes cannot bear on any fed column, so the scored surface that corresponds to the
> fixture's column universe is the four **trade** classes — `trades_all`, `trades_buy`,
> `trades_sell`, `trades_large`.

**This justification makes no reference to what the restriction does to any count** — the form
`PREREG.md` §6.2 SC-8(d) (a scope choice is justified independently of its effect on any
number) requires; cited, not restated. R17(i) is the working resolution that applied it here.
The counts are stated below, as a separate factual matter, and are not part of the reason.

**MAP 1 vs MAP 2 — CORRECTED SIDE.**

| Statistic (over SCORED cells) | Full-class map AS MEASURED (declared 10) | Fixture-universe-restricted map (4 trade classes) |
|---|---|---|
| strict-positive instrument-months | **18 / 48** | **18 / 48 — the SAME 18 cells** |
| `equal_count` non-zero | **35 / 48** | **11 / 48** |
| equal-only (equal > 0, strict == 0) | **17 / 48** | **2 / 48** — `es 2025-10`, `es 2025-11` |
| zero strict AND zero equal | **13 / 48** | **28 / 48** |
| partition check | 18 + 17 + 13 = **48** | 18 + 2 + 28 = **48** |
| peak strict by fraction | **zc 2025-09, 111,334 / 580,944 = 19.16%** (class `mbo_all`) | **zc 2025-10, 34,492 / 634,445 = 5.44%** |
| peak strict by absolute count | zc 2025-09, 111,334 | gc 2025-10, 37,913 / 772,447 = 4.91% |

**MAP 1 vs MAP 2 — CONTAMINATED SIDE.**

| Statistic (over SCORED cells) | Full-class map AS MEASURED (declared 10) | Restricted map (4 trade classes) |
|---|---|---|
| strict-positive instrument-months | **48 / 48** | **48 / 48** |
| `equal_count` non-zero | **42 / 48** | **23 / 48** |
| equal-only | 0 / 48 | 0 / 48 |
| zero strict AND zero equal | 0 / 48 | 0 / 48 |

**The 18 strict-positive corrected cells, both maps, cell by cell.** The cell set is identical;
only the magnitudes differ. (`corrected rows` from `y1\trade_class_only_map.csv`, column `rows`;
it agrees with `n1\summary_corrected.csv` on every row.)

| instrument-month | corrected rows | restricted strict | restricted equal | full-class strict | full-class equal |
|---|---|---|---|---|---|
| cl 2025-01 | 801,410 | 21,770 | 0 | 53,249 | 2,194 |
| cl 2025-08 | 664,076 | 9,048 | 0 | 27,852 | 1,427 |
| cl 2025-09 | 687,658 | 10,803 | 1 | 34,010 | 1,388 |
| cl 2025-10 | 745,569 | 15,002 | 3 | 42,377 | 1,893 |
| cl 2025-11 | 703,999 | 15,345 | 0 | 48,607 | 1,680 |
| cl 2025-12 | 768,531 | 10,837 | 2 | 38,945 | 1,985 |
| gc 2025-01 | 761,736 | 13,907 | 3 | 37,065 | 1,853 |
| gc 2025-08 | 692,041 | 16,051 | 0 | 42,886 | 1,907 |
| gc 2025-09 | 734,280 | 25,862 | 0 | 59,691 | 2,053 |
| gc 2025-10 | 772,447 | 37,913 | 0 | 71,584 | 2,588 |
| gc 2025-11 | 674,038 | 12,764 | 1 | 30,577 | 1,686 |
| gc 2025-12 | 772,202 | 20,195 | 0 | 49,649 | 1,793 |
| zc 2025-08 | 554,303 | 23,755 | 3 | 90,868 | 2,857 |
| zc 2025-09 | 580,944 | 30,617 | 1 | **111,334** | 2,640 |
| zc 2025-10 | 634,445 | **34,492** | 2 | 109,332 | 2,873 |
| zs 2025-08 | 465,381 | 17,717 | 2 | 64,404 | 2,161 |
| zs 2025-09 | 429,465 | 10,382 | 0 | 45,255 | 2,281 |
| zs 2025-10 | 508,910 | 16,397 | 0 | 60,559 | 2,353 |

The 18 are **cl all 6 months, gc all 6 months, zc 2025-08/-09/-10, zs 2025-08/-09/-10** — the
same list §13(b) publishes, unchanged.

**Which trade class carries the restricted map's non-zeros** (`y1\y1_trade_class_map_output.txt`
final block): corrected — `trades_all` 18 strict / 11 equal, `trades_sell` 18 / 11,
`trades_large` 18 / 1, **`trades_buy` 0 / 0**; contaminated — `trades_all` 48 / 23,
`trades_sell` 48 / 23, `trades_large` 48 / 8, **`trades_buy` 0 / 0**. `trades_buy` is identically
zero in all 96 of its cells on both sides, the dead-zero consequence of the aggressor-literal
mismatch (§C.4(a), §15). **The restricted surface is therefore carried by three live classes,
not four**, and a gate report may not describe it as a four-class surface without that note.

**THE DELTA, stated as a separate factual paragraph.** Restricting the scored surface to the
fixture's column universe leaves the **strict cell set UNCHANGED**: **18 of 48** corrected
instrument-months, **the same 18 cells**, and **48 of 48** contaminated. **The equal arithmetic
collapses**: corrected equal-non-zero **35 / 48 → 11 / 48** (equal-only 17 → 2), contaminated
equal-non-zero **42 / 48 → 23 / 48**. **The corrected peak falls** from **zc 2025-09, 111,334
strict (19.16% of 580,944 rows)** to **zc 2025-10, 34,492 strict (5.44% of 634,445 rows)** — a
different cell as well as a smaller number, and roughly a threefold fall in rate. Nothing else
moves: no cell changes sign, no unscored cell becomes scored, and the 72 unscored cells of
§13(g) are unaffected in either map.

**What the restricted map IS, so the two are never confused.** It is a **REPORTING object** in
the sense of `PREREG.md` §6.2 SC-3(e) (one scoring key, and only one — cited, not restated),
published under R17(ii) and to make §13(j)'s quotation rules checkable. The gate scores against
`n1\declared_map.csv` as frozen by §D.1 item 3, and no cell that adjudicates a fed-column
finding is dropped by the restriction — because **every one of the eleven REQUIRED columns is
already governed by a `trades_*` class** (§A.6.1's third table column: `trades_all` on nine,
`trades_sell` on `sell_volume_10s`, `trades_large` on `large_trade_count_10s`). The restricted
map adds no measurement, changes no cell value, and is regenerable from the frozen artifact by
`y1\y1_trade_class_map.py`; §D.1's freeze is therefore unaffected in either direction.

**R17(iii) — THE CHECK, RECORDED AS A FINDING.** The trade-class re-derivation **returns
NON-ZERO in the same 18 cells**. **That is the expected result, and it is recorded as a
substantive finding rather than as a formality**: the same-second mechanism is a property of the
**wall-clock JOIN KEY** — `ts_floor`, and the cohort predicate `floor(T_i) == floor(T_{i-1})`
(§13(d), §C.2) — **not of the event source**. Trades and MBO events are attached to a lattice
row by the identical `ts_floor` merge (§3; `phase5_ml.py` L222/L230 and L248, `phase7_l2_sim.py`
L206/L231), so a row whose absorbed window overhangs its own stamp overhangs it for **every**
event stream that has an event in that window. The MBO stream is denser and therefore populates
the overhang window more often and more sharply, which is why the magnitudes fall — but the
cells where an overhang exists at all are a property of the lattice, and they do not move.
**An all-zero return would have been a FINDING, not a pass** — `PREREG.md` §7.8 SC-11(e) (an
unexpected all-zero is a finding, not a pass), cited: on this fixture it would have meant that the
corrected-side violations recorded in §13(b) were carried entirely by an event source no fixture
column consumes, and that no fixture column violates anywhere on the corrected side — which
would have put criterion 1's REQUIRED list, and the discrimination framing of the corrected
side, in question. The check was run for that possibility, and the possibility is excluded.

### (j) THE SIX `mbo_*` CLASSES AFTER Y1 — what they still evidence, and what they may never again be quoted as

**Standing, restated.** Y1 establishes that **0 of the 35 fixture columns is MBO-fed** (§13(i)'s
justification box). The six MBO classes — `mbo_all`, `mbo_bid_add`, `mbo_ask_add`,
`mbo_bid_cancel`, `mbo_ask_cancel`, `mbo_cancel_any` — therefore attach to **no fed column**.
They are not withdrawn, not deleted from the map, and not reclassified: they remain SCORED cells
of `n1\declared_map.csv` and every count in them stands as measured. What changes is what they
may be quoted **for**.

**They STILL legitimately evidence — and may be quoted for:**

1. **Lattice-irregularity characterization of the fixture's SOURCE stream.** The MBO event
   stream measured against the snapshot lattice is a real, measured property of the data the
   fixture is built from and of the wall-clock-second join geometry. §B.4's two counts — **18 of
   48 instrument-months MULTI-BLOCK, 41 of 48 carrying filtered excess rows** — and §3's root
   cause are statements about the *stream and the
   lattice*, and they stand.
2. **Boundary-instant characterization of that source stream** — how far past a claimed decision
   instant the wall-clock-second bucket reaches, measured on the densest available event stream.
   MBO is the densest, which is exactly why it yields the sharpest boundary measurement: worst
   overhang past `t-1` **999.999579 ms** on MBO classes against **999.996869 ms** on trades
   (§10, §14).
3. **Corroboration of the join-family MECHANISM.** The `ts_floor` geometry that produces the MBO
   overhang is the same geometry that produces the trades overhang. The MBO measurement is a
   higher-resolution view of ONE mechanism, not a second mechanism — which is also why §13(i)'s
   restricted map returns the same 18 cells.

**What they may never be quoted as is registered at `PREREG.md` §6.1 SC-10(d) (four forbidden
uses of non-gate data) and is cited, not restated. Applied to this fixture, the four read:**

1. **(SC-10(d)(1) — evidence about a fed column.)** An `mbo_*` class being strict-positive in a
   cell says nothing about whether any of the 35 columns violates in that cell, and its being
   zero says nothing about any column being clean. They attach to no column at all.
2. **(SC-10(d)(2) — criterion-1 arithmetic.)** §A.6.1 contains no `mbo_*` column; Y1 confirms
   there is no route by which one could enter, and N = 11 is re-derived unchanged against the
   columns the fixture actually contains (§A.6.4).
3. **(SC-10(d)(3) — an unqualified headline over the scored population.)** Where the sentence
   is about the fixture's FED columns, the class set is the four trade classes: **18/48 strict
   corrected (unchanged), but 11/48 equal-non-zero and 2/48 equal-only — not 35 and 17**
   (§13(i)).
4. **(SC-10(d)(4) — an unqualified peak.)** The published corrected peak — zc 2025-09, 111,334,
   19.16% — is an `mbo_all` figure. Restricted to the fed columns (trade classes), the peak
   differs by metric, and both are named: the **RATE peak is zc 2025-10 — 34,492 of 634,445
   corrected rows, 5.44%**; the **ABSOLUTE peak is gc 2025-10 — 37,913 of 772,447 corrected
   rows, 4.91%**. Neither is "the" peak. §13(a)'s class-set statement (SC-10(c)) names the class
   set on every "max across classes"; SC-10(d)(4) adds the metric, and after Y1 that is
   load-bearing, not housekeeping.
   (Derivation: `y1\trade_class_only_map.csv`, corrected rows, `max_strict_trade_only` over
   `rows`; top five by rate are zc 2025-10 5.44%, zc 2025-09 5.27%, gc 2025-10 4.91%,
   zc 2025-08 4.29%, zs 2025-08 3.81%.)

**CAUTION, recorded verbatim from Y1 §3.2 — the `BOUNCE_FREE_FEATURES` trap.** The reasoning
above depends on which 35-column set is meant, and the archive contains two sets of length 35
whose MBO content is opposite:

> **Consequence, stated explicitly:** the 35-set is **not** Phase 5's `BOUNCE_FREE_FEATURES`
> (L91 `BOUNCE_FREE_FEATURES = [f for f in FULL_FEATURES if f not in PRICE_LAG_FEATURES]`, which
> is also 35 long but **keeps all 10 MBO columns** and drops the 10 price-lag ones instead).
> Any reasoning that treats "the 35-set" as the bounce-free set would reach the opposite MBO
> conclusion. The sets are disjoint in exactly the way that matters here.

**The named constant `PREREG.md` §6.2 SC-4(j) (the scored set is named, not counted) requires
the declaration to declare — cited, not restated:** "the 35-column set" in this file means
`ALL_L2_FEATURES` (`phase7_l2_sim.py` lines 73-108), never `BOUNCE_FREE_FEATURES`; any
re-derivation names that constant under SC-4(j). The `feature_set` values `Full` / `BFree`
that the 45-set result families carry (§0.4 item 2) are exactly where a reader would otherwise
pick up the wrong 35.

## §C. Two-sided ground-truth enumeration — the criterion-1 violation set, side-relative and post-lag

> **DUAL TAG, and it must not be collapsed.** The COLUMN UNIVERSE enumerated here is **ARTIFACT
> B's** — the 35 columns the gate scores, under R3 (§0.2). The PER-CELL COUNTS attached to those
> columns are **MEASURED ON ARTIFACT A** (§0.1), via `n1\declared_map.csv`. This section is
> exactly the join of the two artifacts, which is why the join is stated at the top of it.

**Everything in this section is stated POST-LAG** — about the value actually FED to the model at
row `t`, not about the raw construction: the representation `PREREG.md` §2.9 SC-1(b) requires
named, and the one SC-3(d) requires the map stated in. On the contaminated side the fed value is
the row's own construction; on the corrected side it is the row `t-1` construction
(`phase7_l2_sim.py` line 276). And **everything is stated SIDE-RELATIVELY**, as `PREREG.md`
§6.2 SC-3(d) (the map is stated in the terms the declaration declares) requires — cited, not
restated: the same column name is a violation on one side and, on the other side, a violation
only on a declared cohort; this fixture has no side-independent list of leaking columns.
*(Instance: the tables of C.1 and C.2 are the side-relative enumeration SC-3(d) requires, with
the declared cohort SC-8(c) requires checkable pre-run.)*

**The comparator, pinned.** Under PREREG.md lines 190-193 the comparator evaluates
`a(j,c) <= d(i)`; the declared availability instant for the join families below is the
**`at_source_timestamp` truth** — `ts_floor + 1s`, the instant the wall-clock-second aggregate
completes. The **`at_bar_close` role recorded in §4 and in the T2 addendum is declared an
APPROXIMATION of that instant** — it names where the value sits on the lattice, not when it
became knowable — which is the statement `PREREG.md` §2.9 SC-1(c) (a role is a position, not an
availability instant) requires the declaration to make, and under which the approximating role
is not the scored instant; cited, not restated. On this fixture, scoring `at_bar_close` as the
availability instant for a join-family column would find the contaminated side clean — which is
why the declaration is made here, in terms.

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
instrument-months are named in §13(b), and they are exactly the **18 MULTI-BLOCK**
instrument-months of §B.4 — **not** the wider 41 that merely carry filtered excess rows (§B.5).

**Why this is checkable before any detector runs:** the cohort predicate reads only the lattice
`timestamp` column — no event data, no trades parquet, no MBO parquet. A reviewer can regenerate
the cohort from the snapshot file alone and confirm the declared restriction.

### C.3 — Same-row book reads: availability-LEGAL at the boundary — an AVAILABILITY PROPERTY, not a gate class

> **Heading corrected this pass (Y2).** It formerly read "...and OUT of this gate's
> jurisdiction", which invited the enumeration below to be read as §A.6.2's OUT OF JURISDICTION
> *class*. It is not that class: it enumerates an availability property across fed and not-fed
> columns alike. The four gate categories are stated separately further down, and the §-number
> `C.3` is unchanged, so every cross-reference written before this pass stays valid.

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
`a = T <= d = T` admits it. **These 27 constructions are not availability violations on either
side.** That is the AVAILABILITY DECLARATION and it covers all 27. **An availability declaration
about a unit and the unit's gate class are different objects — `PREREG.md` §6.2 SC-4(g) (one
gate class per unit), cited — so the gate class is stated PER CATEGORY below and no column
carries two.** The false-positive consequence attaches to the **22 OUT OF JURISDICTION columns
of §A.6.2 ONLY** — `PREREG.md` §6.2 SC-5(c), cited — Category 1 below, being the 4
manifest-CLEAN columns plus the 18 of this list that Category 1(b) enumerates. Two carve-outs,
each following an already-issued resolution rather than making a new one:

- **Category 2 — `book_imbalance_ratio` is UNSCORED (working resolution R16), and a finding on it
  is not a false positive** (`PREREG.md` §7.7 SC-6(d), findings on `unscored` units — cited).
  §A.6.3: "It carries ONE gate class and one only — UNSCORED"; frozen §D.1 item 2 places it in
  UNSCORED alongside `buy_volume_10s`. **Scoring a finding on it as a false positive would
  contradict that frozen class assignment.** That it WOULD be OUT OF JURISDICTION if it were
  constructible is recorded at §A.6.3 and at Category 2 below, and is **not applied**.
- **Category 3 — the 8 not-fed columns hold NO gate class whatever** (`PREREG.md` §6.2 SC-4(g),
  last sentence — an unfed unit holds no gate class; cited): the gate **does not adjudicate
  them**, because they are outside the fixture's column universe (Category 3 below).
- **Category 4 — the REQUIRED 11 are not in this list at all**, and a finding on one of them is
  REQUIRED, not a false positive (§A.6.1). Stated here so that all four categories' gate
  consequences appear together, per-category, with no column carrying two. *(Instance: the
  category lists below are the declared facts on which each unit satisfies its cited SC-4(b)
  row.)*

**Scoping check, performed against §A.6.2, §A.6.3, §C.4(c) and frozen §D.1 item 2 before this
passage was written:** the 22 is §A.6.2's count and list; the `book_imbalance_ratio` carve-out
reproduces §A.6.3's UNSCORED entry, §C.4(c)'s "no finding on it counts for or against any
criterion", and §D.1 item 2's frozen UNSCORED membership; the Category 3 carve-out reproduces
Category 3 below. Arithmetic: 18 (of this list) + 4 (manifest-CLEAN, **not** in this list) = 22;
18 + 1 + 8 = 27.

> **THE 27-COLUMN LIST ABOVE IS RETIRED AS A CLASS CLAIM (Y2).** It survives ONLY as what it
> actually is — **an availability-legality observation**: these 27 constructions read the
> decision row's own snapshot book and nothing else, and are therefore availability-legal at the
> boundary instant under R1. **It is NOT a gate class, it names no denominator, and it may never
> be cited as one.** It mixes fed and not-fed columns and it cuts across three different gate
> dispositions, which is exactly why the earlier "27 = 18 + 1 + 8" reconciliation read like a
> partition and was not one. **§D.1 item 2's frozen enumeration governs class membership.**

**SCOPE — FOUR CATEGORIES, DERIVED INDEPENDENTLY AND NEVER FOLDED TOGETHER (Y2).** Each is
derived from its own source, enumerated by name, and counted. Every count below was verified
this pass against `f3\fixture_manifest_DRAFT.json` — its 35-entry `columns` array,
`counts.total_fed_to_phase7` = 35, `counts.not_fed_to_phase7` = 19 and its 19-entry
`not_fed_to_phase7_models` array — column by column, before this passage was written.

**CATEGORY 1 — OUT OF JURISDICTION: 22 columns of the 35-column partition. VERIFIED COUNT: 22.**
Source: §A.6.2, cross-checked against the manifest's `class` field on each name. Declared
availability-legal at the boundary instant under R1's `ties: available` — the ground on which
each satisfies `PREREG.md` SC-4(b), row OUT OF JURISDICTION; the false-positive consequence is
SC-5(c)'s (cited). Two sub-groups, kept apart because their
false-positive routes differ, **not** because they are different classes:

- **(a) Manifest-CLEAN — 4:** `minutes_since_open`, `session_open`, `session_mid`,
  `session_close`. Manifest `class` = `CLEAN` on all four (verified). Route: criterion 2 on the
  contaminated side, amended criterion 3 on the corrected side.
- **(b) Same-row book and lattice reads the manifest classes LEAK-SOURCE or DESCENDANT — 18:**
  `spread_ticks`, `bid_size_1`, `ask_size_1`, `l1_imbalance`, `total_bid_depth`,
  `total_ask_depth`, `depth_imbalance`, `book_slope_bid`, `book_slope_ask`, `depth_change_1s`,
  `depth_change_5s`, `depth_change_30s`, `mid_return_1s`, `mid_return_5s`, `mid_return_10s`,
  `mid_return_30s`, `tick_direction`, `weighted_mid`. Verified: **13 `LEAK-SOURCE`, 5
  `DESCENDANT`** (`l1_imbalance`, `depth_imbalance`, `depth_change_{1,5,30}s`), **0 `CLEAN`** —
  13 + 5 = 18, and the zero is exactly why criterion 2 has no landing site for them.
  **4 + 18 = 22.**

**CATEGORY 2 — `book_imbalance_ratio`: UNSCORED, ONE CLASS ONLY (working resolution R16).
COUNT: 1.** Derived independently of Category 1 and it is **not** a member of it.

- **The reason is unconstructibility, not availability.** The column is one of §17's 7
  UNCONSTRUCTIBLE columns: the F2 build's `book_imbalance` is a raw snapshot-parquet
  pass-through whose construction cannot be verified equivalent from the fixture code, and its
  **lag treatment differs** — lag-exempt in the corrected build against lagged in
  `phase7_l2_sim.py` (§17 item 6, §C.4(c); `t4\fixture_manifest_35col_DRAFT.json`,
  `unconstructible_columns`). Nothing in this spike resolves which treatment the stored
  predictions were produced under. Its lag treatment is therefore declared **UNRESOLVED** — the
  second exclusion ground `PREREG.md` §6.2 SC-4(e) (grounds for exclusion are declared, and
  declared pre-run) registers; cited, not restated. Its gate status is **EXCLUDED** on that
  ground, and its gate class is UNSCORED (§A.6.3).
- **Recorded fact, NOT applied: it WOULD be OUT OF JURISDICTION if it were constructible.** Its
  construction is a pure function of the same row's two depth sums (manifest `class` =
  `DESCENDANT`, parents `total_bid_depth` / `total_ask_depth`; `phase7_l2_sim.py` lines 188-189),
  so on the availability question alone it sits exactly where Category 1(b) sits. **That fact is
  recorded and is not acted on.** Assigning it both classes would put one column in two frozen
  classes at once, which `PREREG.md` §6.2 SC-4(g) (one gate class per unit; §0.2.1 line 79)
  forbids — cited. R16 resolves it to ONE class: UNSCORED. §D.1 item 2 freezes it there,
  alongside `buy_volume_10s`.
- Reinstatement is **class C** (`PREREG.md` SC-4(e), SC-4(h) — cited); the lag question must be
  resolved first.

**CATEGORY 3 — the 8 Phase-5-only columns: OUTSIDE THE FIXTURE'S COLUMN UNIVERSE. VERIFIED
COUNT: 8.** `depth_pctile_60s`, `depth_pctile_300s`, `mid_return_60s`, `mid_return_300s`,
`volatility_30s`, `volatility_300s`, `range_60s`, `range_300s`. All eight verified present in
the manifest's 19-entry `not_fed_to_phase7_models` array and absent from its 35-entry `columns`
array. **This is a FOURTH category and is never folded into OUT OF JURISDICTION.** OUT OF
JURISDICTION is a *gate class held by a fed column*; these eight are **not fed at all** and
therefore hold **no gate class whatever** — `PREREG.md` §6.2 SC-4(g), last sentence (an unfed
unit holds no gate class, and calling it out of jurisdiction would imply adjudication), cited
and not restated. The fixture does not contain them, so the gate does not adjudicate them. (The
other 11 not-fed columns are the 10 MBO-derived Phase 5 columns plus
`trade_count_10s` — likewise outside the fixture's column universe; see §13(i), §13(j).)

**CATEGORY 4 — REQUIRED: the 11. VERIFIED COUNT: 11.** `net_delta_1s`, `net_delta_5s`,
`net_delta_10s`, `net_delta_30s`, `net_delta_60s`, `sell_volume_10s`, `large_trade_count_10s`,
`vwap_distance`, `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s` (§A.6.1). All eleven
verified present in the manifest's 35-entry `columns` array. Derived from the declared map by
the registered predicates (`PREREG.md` SC-4(a)–(b); working resolution R11), not from the
manifest's construction classes. Re-derived against the fixture's actual column
sources by Y1: all eleven are trades-parquet-fed (`vwap_distance` additionally snapshot-fed for
its `mid` term) and **none is MBO-fed**, so **N is unchanged at 11**.

**THE ARITHMETIC, printed so it is auditable.** Categories 1, 2 and 4 are disjoint subsets of the
35 fed columns; the 35th column is `buy_volume_10s`, UNSCORED as a degenerate constant (§C.4(a)),
which is the second member of the UNSCORED class and belongs to none of the four categories:

> **22 (Cat 1) + 1 (Cat 2) + 11 (Cat 4) + 1 (`buy_volume_10s`) = 35 fed columns.**
> Restated as §A.6.4's partition: REQUIRED **11** + OUT OF JURISDICTION **22** + UNSCORED **2**
> = **35** = `f3\fixture_manifest_DRAFT.json` `counts.total_fed_to_phase7`.
> **Category 3's 8 are OUTSIDE this arithmetic entirely** — they are 8 of the 19 not-fed
> columns, and adding them to any of the four totals is the error this passage exists to stop.

**Category 4 is the criterion-1 denominator** — the REQUIRED list, whose length is N under
`PREREG.md` §6.2 SC-4(b) (cited); Categories 1, 2 and 3 are not in it. The availability
declaration stated above is unaffected by any of this bookkeeping, and so is the 11 + 22 + 2 =
35 partition arithmetic of §A.6.4.

> **DELETED THIS PASS (working resolution R11): the clause that routed these columns to
> criterion 2.** **Referent, stated so the four-category passage above cannot be read into it:
> "these columns" and "above" in this note mean THE 27-COLUMN AVAILABILITY-LEGALITY LIST and the
> R1-basis sentence that follows it — not Categories 1-4.** The earlier draft ended that
> R1-basis sentence with "under criterion 2 on the contaminated side and under the amended
> criterion 3 on the corrected side." The criterion-2
> limb had **no landing site**. PREREG.md line 460 (verbatim): "2. No **manifest-clean** source
> column receives **any runtime finding of any tier, primary or secondary**, on
> `fixture_contaminated`." Its scope is **manifest-CLEAN** columns; **every one of the 27 is
> manifest LEAK-SOURCE or DESCENDANT** in `f3\fixture_manifest_DRAFT.json` (verified this pass:
> the 19 fed among them split 13 LEAK-SOURCE / 6 DESCENDANT counting `book_imbalance_ratio`, and
> the 8 not-fed split 4 LEAK-SOURCE / 4 DESCENDANT; **0 CLEAN**), so criterion
> 2 could never receive a finding on one of them and the routing was inoperative text that
> looked like a rule.
>
> **What happens instead — the routing `PREREG.md` §6.2 SC-5 (adjudication routing) registers,
> cited limb by limb and not restated; this file supplies the units each limb applies to:**
> 1. **An availability-class finding on any of the 22 OUT OF JURISDICTION columns (§A.6.2) is a
>    declared FALSE POSITIVE** — `PREREG.md` SC-5(c) — recorded as such, by name, in the gate
>    report; not a criterion-2 failure, and not silently dropped either. **The scope is the 22,
>    NOT the 27-column list this note is about**, and the two carve-outs stated at the
>    availability declaration above bind here identically: `book_imbalance_ratio` is UNSCORED
>    (R16, §A.6.3, §C.4(c), frozen §D.1 item 2; SC-6(d)); the 8 not-fed columns hold no gate
>    class whatever and the gate does not adjudicate them (SC-4(g)).
> 2. **On the corrected side a false positive on one of those same 22 is also a criterion-3
>    failure** — `PREREG.md` SC-5(d) (the double charge where the criteria are independent) with
>    SC-3(b): the amended criterion 3 (§A.8) scores every corrected-side finding against the
>    declared map and the map declares no violation on those columns. That limb of the old
>    sentence was correct and survives. It carries the same scope: neither carve-out in item 1
>    routes to criterion 3 either.
> 3. **A finding about their LABEL-BASE character belongs to L2a** — the jurisdiction assignment
>    `PREREG.md` SC-5(e) requires, with SC-5(e)'s consequence for this gate — see the paragraph
>    immediately below.
> 4. **The four manifest-CLEAN columns are a different case and DO route to criterion 2** —
>    `PREREG.md` SC-5(c), the units the declaration declares clean: `minutes_since_open`,
>    `session_open`, `session_mid`, `session_close` (§A.6.2(a)). Criterion 2 is exactly in scope
>    for them, which is why the two sub-groups are kept apart.

**Their label-base character is a real property, and it is assigned elsewhere.** `tick_direction`
(reads `mid(t)`, the label base), `vwap_distance` and `weighted_mid` (both of the
`(X - mid)/tick` form) sit at `mid(t)`, which is exactly what `fwd_move_ticks_*` measures FROM
(`phase5_ml.py` lines 216-219; `phase5_audit.py` line 101, verbatim: "The label predicts
direction FROM mid[t]."). **That character is assigned to L2a jurisdiction — the ex-ante
detector-jurisdiction assignment `PREREG.md` §6.2 SC-5(e) (jurisdiction between detectors is
declared, and a boundary cuts both ways) requires the declaration to make; its consequence for
this gate is SC-5(e)'s, cited and not restated (§A.6.2 states the same assignment and is the
second site of it).** It is not an availability question under the declared tie branch. (Note
the asymmetry R1 accepts:
under `ties: available` the fixture's standing as an availability-violation exemplar rests on the
C.1/C.2 join families, not on the shift(1) absence per se — Part I §6 states the same thing from
the other direction.)

### C.4 — Column-level gate dispositions, declared before any run

**(a) `buy_volume_10s` — EXCLUDED, on the degenerate-unit ground `PREREG.md` §6.2 SC-4(e)
registers (cited). Degenerate constant.**
`phase5_ml.py` line 231 `is_buy = trades["aggressor_side"].isin(["B","Buy","buy"])` matches none
of the actual parquet values (BUY_AGGRESSOR / SELL_AGGRESSOR / UNKNOWN; `isin` is exact
case-sensitive equality), so line 234 `trades["buy_vol"] = np.where(is_buy, trades["size"], 0)`
is identically 0 and line 254's rolling sum is identically 0. Same defect at
`phase7_l2_sim.py` line 207 (§15). Independently visible in the map: the **`trades_buy` class is
0 strict and 0 equal in every one of its 96 cells, on BOTH sides** (`n3\predicate_check.csv`
per-class total `trades_buy` `strict_viol` = 0 over 48 cells; `n1\declared_map.csv` `trades_buy`
rows). It is a degenerate unit that cannot carry a finding of the scored class — the first
exclusion ground SC-4(e) registers, with SC-4(e)'s own reason; cited, not restated. It is
declared out here, before any run (SC-4(e); SC-8(c)); its reporting as EXCLUDED rather than as
MISSED is `PREREG.md` §7.8 SC-11(g)'s (cited; `PRACTICES.md` P-47).

**(b) Session-flag staleness — a DOCUMENTED QUIRK. It licenses NO corrected-side finding.**
`session_open`, `session_mid`, `session_close` (and their parent `minutes_since_open`) are
deterministic clock functions with column_role `always`, yet they are not in `EXEMPT_COLS`
(`phase7_l2_sim.py` line 266), so line 276 lags them: the FED session flag at row `t` is the
row `t-1` flag (T2 addendum, "Recorded quirk"). This is **staleness, not unavailability** —
`PREREG.md` §2.9 SC-1(e) (staleness is not unavailability), cited and not restated: a `t-1`
clock flag was knowable by `d(i)`. **Declared fact: the lagged session flags on the corrected
side are a documented as-built property of this fixture**, recorded here so it cannot later be
re-read as a discovery; what a finding resting on that staleness is, on either side, is
SC-1(e)'s.

**(c) `book_imbalance_ratio` — lag discrepancy UNRESOLVED; gate status EXCLUDED.**
T4 records that the fixture build's `book_imbalance` column is a raw snapshot-parquet
pass-through whose construction cannot be verified equivalent from the fixture code, and that
**its lag treatment differs — lag-exempt in the corrected build vs lagged in `phase7_l2_sim.py`**
(§17 item 6; `t4\fixture_manifest_35col_DRAFT.json`, `unconstructible_columns`). Nothing in this
spike resolves which treatment the stored predictions were produced under. **The discrepancy is
recorded as UNRESOLVED and the column's gate status is EXCLUDED** — the second exclusion ground
`PREREG.md` §6.2 SC-4(e) registers (cited) — which costs nothing, since it is already one of the
7 UNCONSTRUCTIBLE columns of the 28-column projection. Its gate class is UNSCORED (§A.6.3;
SC-4(b), §7.7 SC-6(a)). If it is ever reinstated the lag question must be resolved first, and
reinstatement is class C (SC-4(e), SC-4(h)).

**Summary of declared exclusions:** `buy_volume_10s` (degenerate constant) and
`book_imbalance_ratio` (unresolved lag, already unconstructible). Everything else enumerated in
C.1 and C.2 is IN. The exclusions are declared here, pre-run, each on a ground `PREREG.md` §6.2
SC-4(e) registers, and are frozen at the tag by §D.1 (SC-8(a)–(c)) — this is the
declared-exclusions data SC-4(e) and SC-8(b) require: the named unit and its ground.

### C.5 — `vwap_distance`: the SOLE dual-ground column — REQUIRED on ONE ground, OUT OF JURISDICTION on the other (item S3)

**Why this column gets its own subsection** *(instance: the unit with two grounds that
`PREREG.md` §6.2 SC-5(b) requires the declaration to name, with which ground governs)*. Of the
35 fed columns, `vwap_distance` is the
**only MIXED one** — the only column whose construction reads **both** raw files
(`y1\column_universe.csv` row 21, `source_class` = "MIXED: snapshot parquet + trades parquet";
§A.6.5 row 21). Every other column is single-sourced, so for every other column "which ground is
this finding on?" has one answer. Here it has two, and leaving that implicit would let a detector
fire on the wrong one and have it counted.

**THE CONSTRUCTION, with both grounds traced.** `phase7_l2_sim.py` **L243**:

> `snap["vwap_distance"] = (mid - snap["vwap"]) / tick`

- **`mid`** is the decision row's OWN snapshot mid, read at **L149** from the snapshot frame
  loaded at L139 (path L135). **Same-row read. No join.**
- **`snap["vwap"]`** is the wall-clock-second trade aggregate: groupby at **L224-225** over the
  trades frame (path L199, read L201), merged onto the lattice on `ts_floor` at **L231**, then
  forward-filled at **L235** so a tradeless second carries an earlier second's value.
  **Forward join on the wall-clock second.**

**(a) IT CARRIES TWO GROUNDS AT ONCE, and they have opposite availability verdicts.**

1. **The same-row `mid[t]` ground — availability-LEGAL at the boundary.** A snapshot stamped `T`
   contains events strictly before `T` (§3, `process_mbo.py` 354-363), so with `d(i) = T` the
   comparator admits it: `a = T <= d = T` under **R1's registered `ties: available`**. This is
   the identical basis on which §C.3 declares the 27 same-row book constructions
   availability-legal, and `vwap_distance`'s `mid` term sits squarely inside it.
2. **The `ts_floor` trade-window ground — a violation.** The merged aggregate covers
   `[floor(T), floor(T)+1s)`, whose true availability instant is `floor(T)+1s`, which lies
   strictly after `T` whenever the row's stamp sits inside its second. **This window absorbs
   post-decision events**, and it is the §C.1 join-family mechanism without modification.

**(b) THE GROUND THAT MAKES IT REQUIRED IS THE FORWARD-JOIN ONE.** `vwap_distance` is in
§A.6.1's denominator (#8) **because of the `ts_floor` trade window and for no other reason**.
Its governing map class is `trades_all` — the class of the `vwap` term — and it is that class,
in the cells where the map declares it non-zero, that the finding must be adjudicated against.
The `mid` term contributes **nothing** to its REQUIRED status; strip the `vwap` term and the
column would not be REQUIRED at all.

**(c) THE VIOLATING GROUND IS THE FORWARD-JOIN GROUND, and which ground a finding must be on is
registered.** Criterion 1 asks for **at least one primary runtime finding attributed to
`vwap_distance`** (PREREG.md line 459; §A.6.1); which ground satisfies that is `PREREG.md` §6.2
SC-5(b) (attribution is to the ground, not to the name) — cited, not restated. On this column
the violating ground is the absorbed wall-clock-second trade window — the `ts_floor` overhang —
and the same-row `mid` read is the legal ground. A detector that flags `vwap_distance` for
reading the decision row's own mid has named the right column on the wrong ground; SC-5(b)
says what that is worth.

**(d) AN AVAILABILITY-CLASS FINDING ON ITS SAME-ROW BOOK READ IS OUT OF JURISDICTION AND IS NOT
THE REQUIRED FINDING.** The `mid[t]` read is declared availability-legal under R1 (ground 1
above). An availability-class finding raised against **that** ground is the same kind of finding
that §A.6.2 declares a **FALSE POSITIVE** on the 22; how it is recorded, and that it is not
credited to the column's REQUIRED status, is `PREREG.md` SC-5(b) (cited). Separately and outside
this gate: the `(X - mid)/tick` form also makes the column a **label-base reader**, since
`fwd_move_ticks_*` measures from `mid[t]` (`phase5_ml.py` 216-219; `phase5_audit.py` 101).
**That character is assigned to L2a** (§A.6.1's note, §C.3), the assignment `PREREG.md` SC-5(e)
requires, with SC-5(e)'s consequence (cited). Three characters, three dispositions, no
double-counting — the instance SC-5(b) and SC-5(e) are applied to: forward join → REQUIRED;
same-row mid, availability class → out of jurisdiction, false positive if raised as an
availability violation; same-row mid, label base → L2a, outside this gate entirely.

**THE FRAME: THIS IS R16's TREATMENT OF `book_imbalance_ratio`, APPLIED TO A COLUMN THAT CARRIES
TWO GROUNDS RATHER THAN TWO CANDIDATE CLASSES.** R16 faced a column for which **two frozen gate
CLASSES** were each defensible — OUT OF JURISDICTION on the availability question, UNSCORED on
the unresolved-lag question — and resolved it to **ONE class only**, recording the other as a
fact that is *not applied*, because a column carrying two frozen classes is what `PREREG.md`
§6.2 SC-4(g) (one gate class per unit; §0.2.1 line 79) forbids (§A.6.3, §C.3 category 2). The
same discipline governs here, and the
distinction between the two cases is the point:

| | `book_imbalance_ratio` (R16) | `vwap_distance` (this subsection) |
|---|---|---|
| what is doubled | **two candidate gate CLASSES** | **two construction GROUNDS** |
| how resolved | a resolution PICKS one class; the other is recorded and **not applied** | the grounds are not in competition — **only one of them is a violation ground**, so the class follows without a carve-out |
| resulting gate class | **UNSCORED**, one class only | **REQUIRED**, one class only |
| what is recorded but not applied | that it WOULD be OUT OF JURISDICTION if constructible | that its `mid` term IS availability-legal, and that an availability finding on that term is out of jurisdiction |

**AND THAT IS WHY IT SITS IN EXACTLY ONE GATE CLASS DESPITE THE DUAL GROUND.** What a column's
gate class *is* — and that the gate needs exactly one answer per column — is `PREREG.md` §6.2
SC-4(g)'s (cited, not restated). `vwap_distance` has two grounds but only one of them can produce an
availability violation, so the two grounds do **not** generate two classes — they generate one
class plus one recorded-and-not-applied fact, which is the shape R16 established. **It appears
once in §A.6.4's partition, in REQUIRED, and in no other class**; §A.6.5's cross-tabulation
places it in the trade-touching x REQUIRED cell for the same reason. Anyone tempted to give it a
second class on the strength of the `mid` term is making exactly the move R16 forbade.

## 14. Contaminated-side violation profile (element g; T1 headline)

> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice and its event parquets.

> **BOTH VERSIONS, PUBLISHED SIDE BY SIDE — THE FED-COLUMN RESTRICTION APPLIED SYMMETRICALLY
> (delta-issued item S1).** *(Instance: per-cell map data on the contaminated side, with its
> reporting re-aggregation and delta — SC-3(a), SC-3(e); peaks carry class set and metric,
> SC-10(d)(4).)* §13(i) applies the fixture-universe restriction to the CORRECTED side
> and publishes both maps. **Y1's premise is side-independent** — no fixture column consumes the
> MBO event source, on either side — so the same restriction governs THIS section, whose
> published headline (75.21%, the `total_events` family) has until now been an `mbo_*` figure.
> Both versions appear below: **PROFILE 1, the full-class profile AS MEASURED**, which is
> unchanged, stands as measured, and remains the measurement; and **PROFILE 2, the
> fed-column-restricted profile** over the four `trades_*` classes, which is what any statement
> about the fixture's 35 columns may quote. **Neither replaces the other**, and PROFILE 2 adds no
> measurement and changes no count — it is a re-read of the same artifact rows over a narrower
> class set.
>
> **The justification for the restriction is §13(i)'s R17(i) box and is NOT re-argued here.**
> That box establishes the criterion on the column universe alone — `phase7_l2_sim.py` opens two
> data files and no MBO file; `ALL_L2_FEATURES` contains none of the ten MBO-derived Phase 5
> columns; all 35 columns trace to snapshot 13 / trades 11 / snapshot-derived 9 / clock 1 / MIXED
> 1, **MBO-fed 0 of 35** (`y1\column_universe.csv`). **Per R17(i), the criterion makes no
> reference to what the restriction does to any count, and none may be added to it.** The counts
> below are a separate factual matter and are not part of the reason.

**Scope: ZC 2025-01 only** — lattice **338,159 rows** = `processed\zc\zc_snapshots_2025-01.parquet`
under UTC hours [14,19), generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` (md5
`ea2eee6136896b5f8a5b7ddc052f589c`) — §2's naming rule; this is NOT the v4_gapfill generation,
which is 378,000 rows under the same filter. The other 47 instrument-months are in §13's map.

**PROFILE 1 — THE FULL-CLASS PROFILE, AS MEASURED (all 10 declared classes). UNCHANGED BY S1;
this is the measurement, and every count in it stands.** On the contaminated (pre-fix) side,
measured against decision time `T` over 338,159 rows:

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

**PROFILE 2 — THE FED-COLUMN-RESTRICTED PROFILE (the four `trades_*` classes). This is the only
version a statement about the fixture's 35 columns may quote.** Same cell, same artifacts, same
338,159 rows; **no new measurement and no changed count** — a re-read of the identical rows over
the class set that corresponds to the fixture's column universe.

| Quantity | PROFILE 1 — full-class AS MEASURED (10 classes) | PROFILE 2 — fed-column-restricted (4 `trades_*` classes) | delta |
|---|---|---|---|
| headline strict rate (max over the class set) | **75.21% — 254,315 / 338,159**, class `mbo_all` | **26.49% — 89,568 / 338,159**, classes `trades_all` ≡ `trades_sell` | **−48.72 pp**; 164,747 fewer rows; the restricted figure is **35.2%** of the published one |
| per-class strict-rate span, live classes | **6.99% – 75.21%**, 9 live classes | **6.99% – 26.49%**, 3 live classes | ceiling falls; **floor unmoved** — `trades_large` is the minimum in both |
| classes carrying any strict violation | 9 of 10 (`trades_buy` dead-zero, §C.4(a)) | 3 of 4 (the same dead zero) | — |
| worst overhang past `T` | **999.999579 ms**, classes `mbo_ask_cancel` / `mbo_all` / `mbo_cancel_any` | **999.996869 ms**, classes `trades_all` / `trades_sell` (`trades_large` 999.954529 ms) | **−2.71 µs** — the mechanism's ceiling is the same 1 s bucket under both |
| mean overhang among violating rows | **506.3 – 655.2 ms** (min `trades_large`, max `mbo_all`) | **506.3 – 519.8 ms** (min `trades_large`, max `trades_all`) | upper end falls **135.4 ms**; lower end unmoved |
| median overhang | **513.5 – 727.9 ms** | **513.5 – 536.4 ms** | upper end falls **191.5 ms** |
| share of violations on integral stamps | **≥ 99.98%** (minimum 0.999807, `mbo_all`) | **≥ 99.9978%** (minimum 0.999978, `trades_all`/`trades_sell`; `trades_large` exactly 1.0) | the concentration is **sharper** under the restriction, not weaker |
| integral vs mid-second per-row rate | `mbo_all` **79.12% vs 0.29%**, ratio 270.9x | `trades_all` **27.87% vs 0.012%**, ratio **2337.5x** | the rate RATIO is **8.6x larger** on the fed classes |
| strict / equal at the cell | 254,315 strict + 29 equal (`mbo_all`) | **89,568 strict + 20 equal** (`trades_all` ≡ `trades_sell`) | equal falls 29 → 20 |

**Provenance of every PROFILE 2 figure, row by row.** `t1\violation_table.csv`,
contaminated/`decision_T`: `trades_all` lines 2 / 11 / 14 / 23 / 26 / 29 / 32 / 35 / 44 / 50 (89568, 20,
`frac` 0.264869, `worst_overhang_ms` 999.996869), `trades_sell` lines 8 / 41 (identical),
`trades_large` lines 17 / 47 (23633, 20, 0.069887, 999.954529), `trades_buy` lines 5 / 38
(0, 0, 0.0 — dead-zero), `mbo_all` lines 65 / 95 / 98 (254315, 29, 0.752057, 999.999579),
`mbo_ask_cancel` lines 62 / 86 / 89 (129334, 22, 999.999579).
`v1\mean_overhang_by_class.csv` for the mean/median/worst triples (`trades_all`
519.797439 / 536.435824 / 999.996869; `trades_large` 506.273305 / 513.500435 / 999.954529;
`mbo_all` 655.194723 / 727.947559 / 999.999579). `m4\stamp_type_breakdown.csv` for the stamp
split (`trades_all` `viol_rate_integral` 0.278688, `viol_rate_mid_second` 0.000119,
`rate_ratio_integral_over_mid` 2337.499, `share_of_viol_on_integral` 0.999978; `trades_large`
`share_of_viol_on_integral` 1.0; `mbo_all` 0.791159 / 0.002921 / 270.851 / 0.999807).

**CROSS-CHECK, performed this pass and reported with its result.** The restricted figures were
derived from `y1\trade_class_only_map.csv` (contaminated/zc/2025-01: `max_strict_trade_only`
**89,568**, `max_equal_trade_only` **20**, `max_strict_declared10` **254,315**, `rows`
**338,159**) and independently re-derived from `n1\declared_map.csv` by taking the maximum
`strict_count` over that cell's SCORED `decision_T` rows within each class set: **max over the
four `trades_*` = 89,568; max over the six `mbo_*` = 254,315; max over all ten = 254,315** —
**exact agreement on all three**. The same re-derivation was run over **all 96 rows** of
`y1\trade_class_only_map.csv` against the **984-row** declared map, on `max_strict_trade_only`,
`max_equal_trade_only` and `max_strict_declared10` together: **0 mismatches**. The declared map's
per-class rows for this cell also reproduce PROFILE 1 exactly — `mbo_ask_cancel` 129,334 =
38.25%, `mbo_bid_cancel` 135,981 = 40.21%, `mbo_ask_add` 162,754 = 48.13%, `mbo_bid_add`
164,959 = 48.78%, `mbo_cancel_any` 179,857 = 53.19%, `mbo_all` 254,315 = 75.21%, `trades_all`
and `trades_sell` 89,568 = 26.49%, `trades_large` 23,633 = 6.99%, `trades_buy` 0 — so the two
profiles are two readings of one artifact and not two measurements.

**THE DELTA, STATED PLAINLY — AS THE POINT, NOT AS A CONCESSION.** **The fed-column-restricted
headline for this cell is MATERIALLY SMALLER than the headline this section published: 26.49%
where the published headline said 75.21%** — **89,568 rows where it said 254,315**, a fall of
**48.72 percentage points** and of **164,747 rows**, leaving **35.2%** of the published
magnitude, a factor of **2.84**. **A smaller honest number has replaced a larger one, and
recording that replacement IS the deliverable.** The 75.21% was never wrong as a *measurement* —
it is `mbo_all` at ZC 2025-01, it stands exactly as measured, and §13(j)'s "what they still
evidence" list continues to apply to it — but it was carried as **this section's headline** for a
fixture **none of whose 35 columns consumes the MBO event source**, so *as a statement about the
fixture* it overstated the contaminated side by 2.84x. Two further facts are stated here rather
than left to be discovered: **ZC 2025-01 is the cell where the restriction bites HARDEST of all
48** — its 48.72 pp delta is the largest in the map (§14.1) — so the section that headlines this
cell is exactly the section that most needed the correction; and the cell's **rank moves**, from
15th of 48 by full-class rate to 20th of 48 by restricted rate, i.e. it is nearer the middle of
the contaminated distribution than the full-class figure made it look. **Nothing about the
fixture's discrimination claim depends on the larger number:** the contaminated side is
strict-positive in **48 of 48** instrument-months under BOTH class sets (§13(i)), and the two
sides remain separated by one to three orders of magnitude in the restricted map exactly as in
the full one.

**FORBIDDEN USE — `PREREG.md` §6.1 SC-10(d) (four forbidden uses of non-gate data), cited for
THIS side and not restated (SC-10(e): one copy; the declaration restates the rules for no
side).** §13(j) applies them to the corrected side; Y1's premise is side-independent, so they
bind here identically. The six `mbo_*` classes remain SCORED cells of `n1\declared_map.csv`;
every count in PROFILE 1 stands as measured; **what changes is only what they may be quoted
FOR.** The contaminated-side instance of each registered use — the figures, not the rule:

1. **(SC-10(d)(1).)** PROFILE 1's MBO bullet attaches to no column at all: `mbo_all` at 75.21%
   says nothing about whether any of the 35 columns violates in this cell, and had it been zero
   it would have said nothing about any column being clean.
2. **(SC-10(d)(2).)** **N = 11 and is unchanged** (§A.6.1, §A.6.4, §A.6.5); Y1 confirms there is
   no route by which an `mbo_*` figure could enter criterion-1 arithmetic.
3. **(SC-10(d)(3).)** Where the sentence is about the fixture's FED columns the class set is the
   four `trades_*` classes. On the contaminated side the **strict** cell count does not move —
   **48 / 48 under both class sets** — but the **equal** arithmetic does: **equal-non-zero 42 /
   48 → 23 / 48** (§13(i)). Quoting 42 as a fed-column fact is the error SC-10(d)(3) stops.
4. **(SC-10(d)(4).)** The contaminated-side peaks, each with its class set AND its metric
   (`y1\trade_class_only_map.csv`, contaminated rows, `max_strict_trade_only` /
   `max_strict_declared10` over `rows`):
   - **full-class RATE peak — es 2025-12, 613,447 / 620,108 = 98.93%, class `mbo_all`;**
   - **full-class ABSOLUTE peak — gc 2025-10, 646,575 of 772,448 rows = 83.70%, class
     `mbo_all`;**
   - **restricted RATE *and* ABSOLUTE peak — nq 2025-01, 543,341 / 598,228 = 90.83%, classes
     `trades_all` ≡ `trades_sell`.** **nq is TRADES-CLASSES-ONLY** — 4 of 10 classes scored, its
     six MBO classes UNSCORED and **not zero**, because there is no MBO file at the fixture path
     `processed\nq\` (§13(g), §13(h)). **The label is required on every appearance of nq in a
     table, including this one.** Its restricted and full-class figures are identical *because
     it has no MBO classes to drop* — not because the restriction spared it, and not because it
     is cleaner or dirtier than any other cell;
   - **restricted peaks EXCLUDING nq**, stated because the unqualified restricted peak is an
     nq cell for the coverage reason just given: **RATE — es 2025-11, 484,420 / 549,424 =
     88.17%**; **ABSOLUTE — es 2025-01, 514,323 of 605,290 rows = 84.97%**; both classes
     `trades_all` ≡ `trades_sell`.

   **None of those six figures is "the" peak; each is quoted with its class set and its metric
   (SC-10(d)(4)).**

   **Summary-level peaks for this side — the EX-NQ figures** (`PRACTICES.md` P-111 records the
   summary-level quotation practice; the per-cell requirement is `PREREG.md` SC-10(d)(4)'s).
   nq's restricted peak (90.83%, nq 2025-01) is a **COVERAGE ARTIFACT**: nq's restricted and
   full-class figures coincide only because nq has **no MBO classes to drop**, not because the
   restriction spared it. **A summary-level statement of the restricted contaminated peak in
   this file and in §14.1 therefore quotes the EX-NQ peak: RATE es 2025-11, 484,420 / 549,424 =
   88.17%; ABSOLUTE es 2025-01, 514,323 of 605,290 rows = 84.97%; both classes `trades_all` ≡
   `trades_sell`.** The nq figure appears only as a per-cell entry carrying its
   TRADES-CLASSES-ONLY label and its coverage-artifact reason, not as the restricted
   contaminated headline. Quoting 90.83% as the peak is the same error §13(j) item 4 stops on
   the corrected side. *(This paragraph resolves the tension a verifier found between the
   preceding sentence and the summary in §14.1: "none is the peak" governs PER-CELL quotation,
   where every figure carries its class set and metric; this paragraph governs SUMMARY-LEVEL
   quotation in this file, where a single peak is named and the coverage artifact is not it.)*
5. **`trades_buy` is 0 strict and 0 equal in all 48 contaminated cells** (§C.4(a), §15), so the
   restricted contaminated surface is carried by **three live classes, not four** — the same note
   §13(i) attaches to the corrected side; a headline over it names that partition (`PREREG.md`
   SC-10(c), cited).

### 14.1 — The same restriction across all 48 contaminated cells (a declared scope step-out)

> **SCOPE NOTE, so §14's ZC 2025-01 banner is not silently contradicted.** §14 above is ZC
> 2025-01 only and stays so. This subsection **deliberately steps outside that cell**, for one
> purpose: to place ZC 2025-01 in the 48-cell distribution, so that a single-cell headline is
> never read as representative of the contaminated side. It is the contaminated-side analogue of
> §13(i)'s 18-cell corrected table. **It introduces no new measurement** — every figure is
> `y1\trade_class_only_map.csv`, contaminated rows, itself re-derived from `n1\declared_map.csv`
> and re-verified against it this pass with **0 mismatches over all 96 rows**.

`restricted` = max strict over the four `trades_*` classes (`max_strict_trade_only`);
`full-class` = max strict over the declared classes SCORED in that cell
(`max_strict_declared10`); rate = strict / `rows`. **nq is TRADES-CLASSES-ONLY in all six of its
months** — 4 of 10 classes scored, its six MBO classes UNSCORED and not zero (§13(g), §13(h)) —
which is why its two columns are equal and its delta is 0.00 pp. **That is a coverage fact about
nq's map cells, not a finding about nq**, and it is the reason nq must never be read as the
cell where "the restriction changed nothing".

| instrument-month | rows | restricted strict | restricted % | full-class strict | full-class % | delta pp |
|---|---|---|---|---|---|---|
| cl 2025-01 | 801,411 | 232,865 | 29.06 | 534,779 | 66.73 | 37.67 |
| cl 2025-08 | 664,077 | 142,974 | 21.53 | 406,797 | 61.26 | 39.73 |
| cl 2025-09 | 687,659 | 132,950 | 19.33 | 414,893 | 60.33 | 41.00 |
| cl 2025-10 | 745,570 | 190,595 | 25.56 | 493,760 | 66.23 | 40.66 |
| cl 2025-11 | 704,000 | 158,683 | 22.54 | 497,360 | 70.65 | 48.11 |
| cl 2025-12 | 768,532 | 126,520 | 16.46 | 454,867 | 59.19 | 42.72 |
| es 2025-01 | 605,290 | 514,323 | 84.97 | 585,940 | 96.80 | 11.83 |
| es 2025-08 | 546,610 | 424,624 | 77.68 | 524,929 | 96.03 | 18.35 |
| es 2025-09 | 553,280 | 420,017 | 75.91 | 532,496 | 96.24 | 20.33 |
| es 2025-10 | 599,190 | 490,161 | 81.80 | 576,377 | 96.19 | 14.39 |
| es 2025-11 | 549,424 | 484,420 | 88.17 | 542,495 | 98.74 | 10.57 |
| es 2025-12 | 620,108 | 499,061 | 80.48 | 613,447 | 98.93 | 18.45 |
| gc 2025-01 | 761,737 | 210,374 | 27.62 | 523,228 | 68.69 | 41.07 |
| gc 2025-08 | 692,042 | 204,014 | 29.48 | 461,530 | 66.69 | 37.21 |
| gc 2025-09 | 734,281 | 252,461 | 34.38 | 515,322 | 70.18 | 35.80 |
| gc 2025-10 | 772,448 | 371,565 | 48.10 | 646,575 | 83.70 | 35.60 |
| gc 2025-11 | 674,039 | 213,333 | 31.65 | 470,500 | 69.80 | 38.15 |
| gc 2025-12 | 772,203 | 264,176 | 34.21 | 604,763 | 78.32 | 44.11 |
| he 2025-01 | 337,489 | 39,596 | 11.73 | 132,122 | 39.15 | 27.42 |
| he 2025-08 | 308,711 | 29,188 | 9.45 | 100,848 | 32.67 | 23.21 |
| he 2025-09 | 308,702 | 27,044 | 8.76 | 88,859 | 28.78 | 20.02 |
| he 2025-10 | 338,111 | 30,132 | 8.91 | 106,120 | 31.39 | 22.47 |
| he 2025-11 | 304,487 | 35,084 | 11.52 | 108,223 | 35.54 | 24.02 |
| he 2025-12 | 353,683 | 36,867 | 10.42 | 127,766 | 36.12 | 25.70 |
| le 2025-01 | 337,494 | 44,691 | 13.24 | 140,720 | 41.70 | 28.45 |
| le 2025-08 | 308,711 | 43,707 | 14.16 | 119,867 | 38.83 | 24.67 |
| le 2025-09 | 308,710 | 42,140 | 13.65 | 126,122 | 40.85 | 27.20 |
| le 2025-10 | 338,113 | 47,045 | 13.91 | 125,589 | 37.14 | 23.23 |
| le 2025-11 | 304,492 | 26,854 | 8.82 | 77,483 | 25.45 | 16.63 |
| le 2025-12 | 353,690 | 31,871 | 9.01 | 90,032 | 25.46 | 16.44 |
| **nq 2025-01** *(TRADES-CLASSES-ONLY)* | 598,228 | 543,341 | 90.83 | 543,341 | 90.83 | 0.00 |
| **nq 2025-08** *(TRADES-CLASSES-ONLY)* | 540,531 | 470,095 | 86.97 | 470,095 | 86.97 | 0.00 |
| **nq 2025-09** *(TRADES-CLASSES-ONLY)* | 549,431 | 455,826 | 82.96 | 455,826 | 82.96 | 0.00 |
| **nq 2025-10** *(TRADES-CLASSES-ONLY)* | 590,786 | 524,165 | 88.72 | 524,165 | 88.72 | 0.00 |
| **nq 2025-11** *(TRADES-CLASSES-ONLY)* | 550,464 | 494,380 | 89.81 | 494,380 | 89.81 | 0.00 |
| **nq 2025-12** *(TRADES-CLASSES-ONLY)* | 620,108 | 525,629 | 84.76 | 525,629 | 84.76 | 0.00 |
| **zc 2025-01** *(the §14 cell)* | 338,159 | **89,568** | **26.49** | **254,315** | **75.21** | **48.72** |
| zc 2025-08 | 554,304 | 92,136 | 16.62 | 314,170 | 56.68 | 40.06 |
| zc 2025-09 | 580,945 | 109,981 | 18.93 | 344,076 | 59.23 | 40.30 |
| zc 2025-10 | 634,446 | 117,267 | 18.48 | 342,560 | 53.99 | 35.51 |
| zc 2025-11 | 304,506 | 57,662 | 18.94 | 163,822 | 53.80 | 34.86 |
| zc 2025-12 | 353,104 | 76,969 | 21.80 | 222,940 | 63.14 | 41.34 |
| zs 2025-01 | 337,845 | 78,300 | 23.18 | 210,254 | 62.23 | 39.06 |
| zs 2025-08 | 465,382 | 88,011 | 18.91 | 296,502 | 63.71 | 44.80 |
| zs 2025-09 | 429,466 | 72,942 | 16.98 | 268,482 | 62.52 | 45.53 |
| zs 2025-10 | 508,911 | 91,965 | 18.07 | 296,861 | 58.33 | 40.26 |
| zs 2025-11 | 304,506 | 62,578 | 20.55 | 185,931 | 61.06 | 40.51 |
| zs 2025-12 | 353,104 | 60,796 | 17.22 | 222,557 | 63.03 | 45.81 |

**What the 48 rows say, stated as arithmetic and with every quantity's class set named.**
Strict-positive cells: **48 / 48 restricted, 48 / 48 full-class** — the restriction moves no cell
off zero and none onto it, the contaminated-side analogue of §13(i)'s "same 18 cells" on the
corrected side. Equal-non-zero: **23 / 48 restricted vs 42 / 48 full-class**. Restricted strict
RATE spans **8.76%** (he 2025-09) to a summary-level peak of **88.17%** (es 2025-11, 484,420 /
549,424 — the EX-NQ peak, which §14 item 4's summary-level paragraph names here; the unqualified
maximum is **90.83%**, nq 2025-01, TRADES-CLASSES-ONLY, a coverage artifact and not the
headline), median **21.66%**. The summary-level restricted **ABSOLUTE** peak is **es 2025-01,
514,323 of 605,290 rows = 84.97%**, classes `trades_all` ≡ `trades_sell`. Full-class strict rate spans **25.45%**
(le 2025-11) to **98.93%** (es 2025-12, class `mbo_all`), median **63.08%** — the same
0.2545-0.9893 range §13(c) publishes, unchanged. The per-cell delta runs **0.00 pp** (all six nq
cells, for the coverage reason above) to **48.72 pp** (**zc 2025-01 — the largest of all 48**);
excluding nq it runs **10.57 pp** (es 2025-11) to that same 48.72 pp. **The restriction lowers
every non-nq contaminated headline and raises none**, which is the honest summary of what
applying Y1 symmetrically does to this side.

## 15. As-built defects — fixture-level facts (element h; R4; C5-DECIDED-WRAPPED)

> **MEASURED ON ARTIFACT A** (§0.1) — the f2 rebuild is the execution witness for the wrap. The
> defects themselves are properties of BOTH pipeline generations and therefore of Artifact B
> as well; the sentinel statement of §A.9 is the Artifact-B-side consequence.

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

**Claims split per R4** (the evidence-accounting practice is recorded in `PRACTICES.md` P-113;
criterion 4's treatment of the same defect is `PREREG.md` §6.2 SC-5(f), via the sentinel of
§A.9 — this section's defect record is that sentinel's instance):

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

> **NEITHER ARTIFACT — this section is about the ARCHIVE's silence** (§0.3's admissible third
> case). Items 1 and 2 are unverifiable facts about **Artifact B**'s generators and runtime;
> item 3 is an unverifiable fact about the source copies **Artifact A**'s lineage physically
> read. Nothing here is a measurement on either artifact.

Assumptions the declaration RELIES ON that no archive record can verify, recorded as such (the
disclosure practice is `PRACTICES.md` P-115; the three items are this fixture's own premises and
stay here in full):

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

> **MEASURED ON ARTIFACT A** (§0.1) — T4 reads the f2 build outputs. The 35-column TARGET of the
> projection is **Artifact B's** column universe under R3, which is what makes the projection
> informative about B and also what makes 7 columns unconstructible: they exist in B's universe
> and not in A's build output.

Projection of the F2 fixture builds onto the 35-column Phase 7 model set, under the
selection-or-renaming-only method (`PRACTICES.md` P-117 — a rebuild method practice; the
rebuild is outside the gate-scored fixture, `PREREG.md` §6.2 SC-4(d)(ii)), run under R3
*(instance: the F2 rebuild's projection result)*:

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
2. **THE CRITERION-1 PARTITION AND ITS DENOMINATOR (re-derived this pass under working
   resolution R11; this item replaces the earlier freeze of the count 25).** What freezes is
   the **three-class partition of the 35 fed columns**, each class **as an enumerated list of
   column names**, not as a count:
   - **REQUIRED — N = 11**, the list of §A.6.1: `net_delta_1s`, `net_delta_5s`, `net_delta_10s`,
     `net_delta_30s`, `net_delta_60s`, `sell_volume_10s`, `large_trade_count_10s`,
     `vwap_distance`, `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s`.
   - **OUT OF JURISDICTION — 22**, the two sub-lists of §A.6.2.
   - **UNSCORED — 2**, `buy_volume_10s` and `book_imbalance_ratio` (§A.6.3), plus the 72
     unscored map cells at cell level.
   - **The partition check itself: 11 + 22 + 2 = 35.** A gate report that cannot reproduce this
     sum against `f3\fixture_manifest_DRAFT.json` `counts.total_fed_to_phase7` has not scored
     this fixture.
   Moving any column between classes, or changing N, after the tag is a class C amendment.
   **The manifest's independently-leaking-source count 25 is NOT a frozen gate number** — it is
   line 446 manifest content, provenance only, and it is recorded in §A.2 with no arithmetic
   attached. The earlier draft froze 25 as though it were N; that is withdrawn.
3. **Every other gate-consumed number in this file.** Specifically and exhaustively: the
   declared ground-truth map `n1\declared_map.csv` in its entirety (984 rows: 888 SCORED, 72
   UNSCORED_FOR_LACK_OF_DATA, 24 diagnostic); the cohort predicate and its coverage
   (§13(d), §C.2); the reference AUC trio of §A.1; the criterion-1 column enumeration of §C.1
   and §C.2; the declared exclusions of §C.4 (`buy_volume_10s`, `book_imbalance_ratio`); the
   fixture identity and the pc2 exclusion (§8); the boundary `floor(t-1)+1s` (§1); **and the F3
   fixture manifest, pinned by path and by bytes** —
   `evidence\fixture_spike\f3\fixture_manifest_DRAFT.json`, sha256
   `0da59d53982188712073c9b7f5addcd66221babcd8555efabbbd0c3d3f208a1d`, 27,284 bytes.

   **And the code the manifest's meaning depends on, pinned with it (R102/§180.1):**
   `evidence/fixture_spike/f3/phase7_l2_sim.py`, sha256
   `c659d3ac167a13afb52651d4521ecc9fd5c8fabd59fd2d712eb4afa5b4669665`, **949 lines, 41,745 bytes**.
   §D.1 pinned the manifest's bytes; the manifest's **meaning** - what each class asserts about what
   a column reads - rests entirely on that file, and nothing pinned it. A frozen manifest whose
   semantics can move underneath it is not frozen.

   **THE FILE IS NOW IN THE REPOSITORY, and the hash above is unchanged by the move.** It was
   copied byte-for-byte from the archive at `results\pc2_all_phases\_scripts\scripts\`, and the
   sha256 was verified at the destination against the value already pinned here — the pin was not
   re-taken from the copy. It is hashed in the tag message with everything else the freeze ranges
   over.

   **Why it is filed under `f3/` and not under a producer's directory.** Producing code brought into
   the tree was filed with the artifacts it produced. **This file produced none of the spike
   groups**, so that pattern does not reach it, and a reader should not infer one. Placement follows
   this section's own stated relation instead: it is the code the F3 manifest's meaning depends on,
   and `evidence/ceremony/F3_MANIFEST_VERIFICATION.md` — the verification the author's sign-off was
   given over — is wholly about F3 and quotes this file throughout. `t4`'s claim on it is
   **consumption**, not production, and filing a file under a consumer becomes arbitrary the moment
   a second consumer appears.

   **`PREREG.md` SC-4(k2) does not read this file.** SC-4(k2) reads the fixture manifest's named
   list of columns classed as leaking sources. This file is what gives that list its meaning; it is
   not itself a gate input, and `phase7_l2_sim` appears nowhere in `PREREG.md`.

   **Why the manifest is in this list at all (R99/§167.1).** `PREREG.md` SC-4(k2) reads its **named
   list of columns classed as leaking sources** and says so in terms: *"Because the gate now reads
   that list, the manifest is an object the gate consumes: the declaration enumerates it in the
   SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag."* It is therefore a gate input,
   and a gate input outside the freeze is the thing this list exists to prevent. **Pinned by SHA-256
   and not only by filename**, so the freeze names the bytes: a same-named file with different
   contents is a different gate input.

   **Why F3 and not T4 (R99/§167.2).** This declaration already settles it — *"Why F3 governs and not
   T4"* — and `t4\fixture_manifest_35col_DRAFT.json` settles it from its own side: its
   `derived_from` field names the F3 manifest as its source, and it carries a **projection**
   (`projected_columns`, `unconstructible_columns`) rather than a classification. Only F3 carries the
   `LEAK-SOURCE` / `DESCENDANT` / `CLEAN` classes SC-4(k2) reads. **T4 is not in this freeze and does
   not belong in it.**

   **AUTHOR SIGN-OFF.** The author signed off on the F3 fixture manifest on 26 August 2026, over the
   verification at `evidence/ceremony/F3_MANIFEST_VERIFICATION.md`; the 25 LEAK-SOURCE
   names are a gate input alterable only by Class C.

   **Hash chain.** Verification was performed against `8fd3bb5a771af72d…`; the only later change was
   §179.3's `classification_basis` restatement, under which all 35 classifications were
   verified unchanged; the frozen bytes are `0da59d5398218871…`.

   **On the filename (R99/§167.5). The name ends `DRAFT` and is DELIBERATELY NOT CHANGED.** What
   SC-4(k2) requires is that the manifest's **recorded status** is not `DRAFT` at the tag — the
   `manifest_status` field, not the filename. The path is load-bearing in at least four places: this
   pin, the ceremony's C2.5 gate, the evidence manifest's own line, and this declaration's other
   citations of it. **Renaming a gate input's identity immediately before a tag buys tidiness and
   risks every reference to it.** The mismatch is recorded here instead, so no reader infers
   draft-ness from the name: **after the author's review the file is not a draft, and its name still
   says so.**

   **The status is NOT flipped by this entry.** Freezing which bytes are the gate input and
   confirming those bytes are correct are two different acts; the second is the author's.
4. **The class-set rule of §13(a)** — that `mbo_all_rows` is diagnostic and not one of the
   declared 10, and that any "max across classes" names its class set.
5. **The four §6.2 amendments and the §10.2 definition**, as written: §A.1 (reference AUC),
   §A.3 (contamination-availability-class recording locus), §A.4 (sliced variant re-registered
   as a Phase 1 CI obligation, with its ex-ante scoring rule), §A.8 (criterion 3 per R9), and
   §A.12's definition of "waived". Changing any of them after the tag is a further class C
   amendment.
6. **NOT frozen, and explicitly excluded from the freeze: §13(h).** The NQ cross-generation
   diagnostic is non-gated; its numbers may be added, revised or withdrawn without amendment,
   *provided* they are never moved into an acceptance denominator — which is class C (R12).

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

### D.2 — The v30a tag message's hash enumeration

**The enumeration is derived from `PREREG.md` §11 item 8, and from nothing else.** Item 8 is the
v30a clause that defines the set; it is cited here by anchor rather than by line, because this file
is living and a line reference into it drifts.

**Item 8's three limbs, and what each contributes:**

1. **"every registered document and every registration tool — the registration and its checking
   tools as item 1 names them."** §11 item 1 names nine paths. Eight are files; the ninth,
   `tests/registration/`, is a directory, and a directory name does not pin content — item 8's
   closing sentence speaks of a registered **file**, so the directory is enumerated as the files it
   contains.
2. **"every document an amendment registers under §0.2.1 (the availability declaration included)."**
   That is this file.
3. **"every file SC-8(f) requires hashed."** SC-8(f) reaches every file the freeze ranges over.
   Two of those are separate committed files rather than elements inside this one: the F3 fixture
   manifest, which SC-4(k2) reads and §D.1 pins, and the declared ground-truth map, which is the
   scoring key.

**DECLARED: the `prereg-v30a` tag message carries TWENTY SHA-256 lines.** The count is read from the
enumeration and is not an independent assertion about it; the enumeration is produced by the
ceremony's C2 step, whose output `v30a.hashes.txt` is the single authority for any `prereg-v30a`
hash value.

| limb | paths |
|---|---|
| 1 — item 1, named individually | `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `DEVIATIONS.md`, `PARKING_LOT.md`, `VALIDATED_CONFIG.toml`, `tools/check_registration.py`, `protocol/runtime_reference.py` |
| 1 — `tests/registration/`, expanded | `EXPECTED_OUTPUTS.md`, `conftest.py`, `generate_expected_outputs.py`, `test_checker.py`, `test_expected_outputs.py`, `test_invariants.py`, `test_traces.py`, `traces.py` |
| 2 — §0.2.1 | `AVAILABILITY_DECLARATION.md` |
| 3 — SC-8(f) | `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json`, `evidence/fixture_spike/n1/declared_map.csv` |
| §D.1's pinned producing code | `evidence/fixture_spike/f3/phase7_l2_sim.py` |

**WHY THE EARLIER SIX IS SUPERSEDED, recorded rather than quietly replaced.** This section previously
declared SIX and derived that number from a pair of sources: working resolution R7, which records
the set the `prereg-v30` tag actually carried, and `PREREG.md` §0.2.1 line 97's quantifier over the
files hashed at the time that line was written. **Neither is quoted here with its count**, because a
count restated outside its own site is a second assertion about the set and drifts from it; both are
dispositioned at their own sites.

**Item 8 names both of those in terms and supersedes them as the set:** *"where an earlier clause
names the hashed files or their number — item 3's three names, §0.2.1 line 97's 'both' — it records
the set at the time of its writing, stands as that record, and is superseded as the set by this
item."* The earlier derivation rested on the very clause item 8 retires, and it did not cite item 8.
Both earlier statements stand as the record of what was true when they were written; neither states
the set now.

**PRIOR_ART_VERIFICATION.md is not named by item 1, is not registered under §0.2.1, and is not
within the range SC-8(f) ranges over; it is outside the enumeration by rule.**

That file was the declined seventh candidate, closed as SIX at `COMMIT_PLAN.md` §6. **Growing the
set reopens that closure, so it is decided again here rather than inherited:** the earlier decision
turned on a judgement about what belonged, and this one turns on the rule item 8 states. The
outcome is the same and the ground is different, which is why it is restated rather than cited.

**Why the declaration is in the set at all.** This file carries the scoring key and the declared
elements the gate consumes. A tag that hashes the specification but not the declaration the
specification is evaluated under is an integrity chain with a hole exactly where the amendment
lives, and **an amendment weaker than the thing it amends is not one** (§0.2.1 line 97).

**Lock-time obligations arising elsewhere in this file — BOTH DISCHARGED, recorded so the change is
auditable rather than silent:**

- **(i) "Add the contamination availability class as a named field to the governing manifest"
  (§A.3) — DISCHARGED by amendment, not by doing it.** The recording locus is amended to this
  declaration, which the tag hashes; the manifest is an evidence artifact and is not edited
  (§A.3, working resolution R13). There is no residual manifest edit due before the tag.
- **(ii) "Produce or formally defer the CI sliced variant" (§A.4) — DISCHARGED by amendment.**
  The element is moved off the Phase 0 acceptance fixture and re-registered as a Phase 1 CI
  obligation with its scoring rule declared ex ante. It is not due at lock; it is due at the
  first CI run that exercises the padded slicer, and it is frozen by §D.1 item 5.

**No lock-time obligation remains outstanding in this file.** Obligations carried FORWARD rather
than discharged are named at §D.5, so a later reader does not mistake "nothing due at lock" for
"nothing due".

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
opposite by precedent. The tail's existing entries R1-R9 and R11-R13 are frozen byte-identical;
this rule governs anything appended after them.

#### D.3 entries — the registered hash-set language, read (R67/§14.3)

`PREREG.md` specifies the tag message's hash block in two places, written when the set was
smaller. **Neither is edited** — both are registered text. They fall into two **distinct**
categories, and collapsing them would hide the difference that matters.

**(i) `PREREG.md` §11 item 3 — a FLOOR, satisfied and exceeded. NOT violated.**
Registered text: *"SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed in the tag
message and the README."* It carries **no "only" and no "exactly"**, so it states a minimum, and a
superset satisfies it. **Over-delivery is strictly stronger**, so §0.2.1's "an amendment weaker
than the thing it amends is not one" is *satisfied* here rather than strained. The executed
`prereg-v30` tag already carried five, and v30a carries six; both include item 3's three. **A reader
who takes item 3 as exhaustive would conclude the v30 tag over-delivered.** That reading is
available on the text, and it is not a defect — it describes a tag that carried more than it had
to. The reading applied here is the floor reading; a reader is free to disagree with it.

**(ii) `PREREG.md` line 97 (§0.2.1) — NOT a floor. A closed quantifier that lost its referent.**
Registered text: *"An amendment inherits §11's integrity chain in full: signed tag, **both** file
hashes in the tag message, external timestamp receipt committed, repository publicly reachable at
lock."* **"Both" is a closed quantifier over exactly two things.** It is not a minimum, and it
cannot be read as one without changing the word. It was written when the block held two files;
`HISTORY.md` and the two tooling files joined later, and at that moment "both" lost its referent.
**Consequence, stated precisely:** the two files' hashes **are** in the tag message, so line 97 is
**not violated** — but it **supplies no rule for the files added since** and **does not govern the
current set**. The governing enumeration is `$FILES` at `CEREMONY_COMMANDS.md` §3.2; line 97 governs
its own two and nothing else. *(This is the same conclusion working resolution R7 reached, and R7's
own basis for it — that "both" is "a stale count predating `HISTORY.md` and the tooling files
joining the block" — is recorded as a class A mechanical fact.)*

**(iii) Working resolution R7 — STANDS UNAMENDED. There is no contradiction with §D.2.**
R7 reads: *"**R7. hash-count:** the v30a tag message carries ALL FIVE hashes, matching the
prereg-v30 tag as executed."* Read as a totality claim, that is false of a six-line message and
would put R7 against §D.2, which the same file hashes. **It is not a totality claim.** The survey at
R67/§14.2 resolved it by structure rather than by intent:

- **The predicate is true.** "Carries ALL FIVE hashes" is satisfied by any set **containing** those
  five, and the clause *"matching the prereg-v30 tag as executed"* fixes "FIVE" to the v30 five.
  A six-file set containing them satisfies it exactly.
- **The totality reading comes from the LABEL, not the predicate.** `hash-count:` is a topic tag.
  **Every label in that block is a topic tag** — R1 `ties`, R2 `boundary`, R3 `35-column`, R4
  `as-built defects`, R5 `weighted_mid`, R6 `weighted_mid flavor`, R7 `hash-count`, R8 `H-entry`.
  In each, the label names the QUESTION and the body supplies the ANSWER; **no label asserts a
  predicate its body does not.** The closest case is R4, whose label carries a *referent* (which
  defects) rather than a predicate — which is what a topic tag does.
- **The decisive structural evidence: half the block has no labels at all.** R9, R11, R12 and R13
  are recorded as bare `**R9.**`, `**R11.**` and carry their referents in the body. If labels were
  normative, dropping them would drop content; their absence is only intelligible if the label is
  an optional convenience tag.
- **Corroborated independently and earlier:** §D.3's own rule paragraph above already describes R7
  as *"reading 'both' as the executed five, not as a licence to publish two"* — the inheritance
  reading, written before this survey and not derived from it.

**So R7 stands, §D.2's inheritance reading is the literal reading, and nothing is edited.** The
verbatim block is not amended under any branch: it is a transcript of an author delta, and editing
it would falsify the word "verbatim" that introduces it.

**What this class of defect actually was.** None of (i)–(iii) is arithmetically wrong. The defect
was **structural**: the set was asserted independently in many places instead of derived once, and
independent assertions drift apart — at R67 the same set carried **five different values** across
registered text, this declaration and the ceremony package. The remedy is not a corrected numeral
but a single authority plus a detector: `$FILES` at `CEREMONY_COMMANDS.md` §3.2, enforced by
`tools/check_registration.py`'s `hash_set_single_source` check, whose D5/D6 exemptions point back
at these three entries by name.

### D.4 — The signing key, stated here so it is TIMESTAMPED and not merely asserted (R69/B2.2)

**DECLARED: the `prereg-v30a` tag is signed by the OpenPGP key whose primary fingerprint is**

```
991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7
```

**Why this belongs in THIS file and not only in the tag message.** The tag message asserts the
fingerprint, but a tag message is only as good as the signature over it — a message asserting a
fingerprint proves nothing about which key signed it, since the signer writes both. This file is
one of the six the tag message hashes, and the commit it is committed in is the commit
OpenTimestamps stamps. **So a fingerprint stated here is covered by the signature AND carries an
external Bitcoin-anchored timestamp**, which the tag message's own copy does not add.

**The verification chain this creates is three-way, deliberately mirroring §D.2's C2d-2 pattern:**

| leg | value | read from |
|---|---|---|
| 1 | the key that actually made the signature | `git verify-tag --raw`'s `[GNUPG:] VALIDSIG` **last field** (the PRIMARY key fingerprint, so a subkey signature still resolves here) |
| 2 | the fingerprint the tag message asserts | the signed tag body's `Key fingerprint = ` line |
| 3 | the fingerprint this declaration states | the block above |

**All three must agree, and C1b halts if they do not.** Two legs agreeing proves less than it
appears to: legs 1 and 2 together only establish that the signer was internally consistent.

**The key material itself ships.** `prereg-signing-key.asc` at the repository root is the
ASCII-armored public key, so the tagged tree carries the key a verifier needs. **It is deliberately
NOT added to the six-file hash list** — §14.1(b) holds: that list is a citation device, and the
commit tree already fixes every tracked file. **SIX is not reopened by this.**

**WHAT THIS DOES NOT ESTABLISH, stated plainly rather than left to inference.** Every leg above is
INTERNAL to this repository. Together they prove that the key which signed the tag is the key this
registration names — **they do not prove who holds that key.** Key-to-person binding cannot be
established by any repository-local check, because an attacker who could rewrite the tag could
rewrite all three legs. **That binding rests entirely on the key's publication outside this
repository, and §12's disclosure states where.**

### D.5 — Named open obligations

**Recorded under SC-9(c); neither is waived.** SC-9(c) holds that a locked obligation is discharged
only by being met or by being amended, and may not be discharged by a working resolution or by being
carried forward silently. These two are carried forward, and this section is what makes that
carrying explicit rather than silent.

**SC-2(e) is not engaged.** SC-2(e) governs moving an element between phases. Neither element moved:
both remain Phase 0 elements gated by §10.1. What a working resolution fixed was the **due event**,
not the phase.

**(i) §9.2 cross-tool comparison — Phase 0 element, gated by §10.1.**

- **DUE:** before any Phase 1 result is published. Not a condition on Phase 1 work commencing —
  §10.0 step 0 is the only such condition.
- **DISCHARGE:** each named comparator has been run against the acceptance fixture with its own
  positive control (W2b) and its findings recorded per tool. A comparator that cannot run is
  recorded could-not-run with the reason and counts as covered-with-exclusion, never as a pass.
  **Zero comparators run is not a pass** (SC-11a).

**(ii) Licence check — Phase 0 element, gated by §10.1.**

- **DUE:** before any third-party code enters the shipped distribution, and in any case before
  Phase 1 ship.
- **DISCHARGE:** every dependency in the shipped distribution has its licence recorded, and no
  copyleft licence appears in the vendored set. `deepchecks` is AGPL-3.0 and is named.
  Interoperation by optional import or separate process is not vendoring; the distinction is
  recorded with the determination.

**The shape of both entries is §D.2(ii)'s:** a named due event plus a discharge rule, with the rule
**cited rather than restated** where a registered clause already states it.

---

### D.6 — Disclosures at the tag

**What this section is.** Five disclosures accrued during the amendment. Each was written as it
should appear and none had been deployed into a registered file, so each existed only in a drafting
record. **A disclosure that lives only in a drafting record discloses nothing to a reader of the
tag**, and this file freezes at the tag. They are landed here for that reason.

**One of them was already load-bearing while absent.** §A's conformance walk states that `PREREG.md`
line 478 "is handled instead by **specific disclosure at D-STALE**, by line and by quotation" — a
registered pointer into a disclosure that did not exist. The pointer now resolves.

---

**D-KEY — the attestation boundary.**

> **What the ceremony verifies about the signing key, and what it does not.** Step C1b verifies
> three things and halts if any disagrees: the signature is good (`[GNUPG:] GOODSIG`); the primary
> key fingerprint gpg reports for the signature (`[GNUPG:] VALIDSIG`, last field) equals the
> fingerprint the signed tag message asserts; and both equal the fingerprint declared at §D.4, which
> is inside the tag's hash enumeration and therefore covered by the OpenTimestamps receipt over the
> commit.
>
> **All three legs are internal to this repository.** Together they establish that the tag was
> signed by the key this registration names, and that the naming was fixed before the timestamp.
> **They do not establish who holds that key.** Key-to-person binding cannot be established by any
> repository-local check: an actor able to rewrite the tag could rewrite all three legs together.
>
> **That binding rests on publication outside this repository.** The only external location this
> repository names is the GitHub remote `https://github.com/TheoJHoward/DataLeakageAuditor.git`.
> **No keyserver is referenced anywhere in the repository.** If the public key is published, the only
> location consistent with the repository's own contents is the author's GitHub account settings —
> **which is mutable, carries no date a reader can see, and can be removed or replaced without
> leaving a record.** For a pre-registration, whose whole value is that a claim was fixed at a
> knowable time, that is a weak external anchor, and it is disclosed as such rather than left to be
> discovered.
>
> **What shipping the key material fixes, and what it does not.** `prereg-signing-key.asc` at the
> repository root is the ASCII-armored public key, so the tagged tree carries the key material
> itself and a reader in ten years can verify the signature without a keyserver that may no longer
> exist. **This closes the availability problem, not the binding problem** — a key shipped inside
> the repository it signs proves internal consistency only, exactly as above. The uid on the shipped
> key reads `Theo Johann Howard <theojhoward1@gmail.com>`; it is recorded here because the key
> material ships and the uid ships with it.
>
> **A remedy available and NOT taken, stated so the choice is visible:** publishing the key to
> `keys.openpgp.org` and citing that URL in the README would give a dated, third-party, append-only
> anchor. It is an author action requiring control of the key and the email address; no ceremony
> step can perform it.

---

**D-ADVISORY — the five deferred advisory steps.**

> **Five ceremony steps emit output for a human to compare and assert nothing.** They are `C5`
> (2 items), `C2b` (6), `C3c` (3), `C3d` (2) and `V2` (2). Each is honest advisory — it claims no
> verdict — but a reader should know that at these five points the ceremony's correctness rested on
> a person reading output, not on an exit status. The ten steps whose printed verdict contradicted
> their exit status were converted and each carries a fired negative test; **these five were
> deferred, and this line is the record that they were deferred rather than overlooked.**

---

**D-STALE — the stale-description class, stated as a FLOOR.**

> **A class of stale descriptions is disclosed rather than fixed, and its extent is not known.**
>
> After the R9, R11, Y1, R1, R2, R16, SC-13 and Z1 amendments, a sweep was run for passages that
> still describe the amended objects as they were before. **The sweep found approximately
> seventy-six distinct sites and returned zero of ten amendments clean.** Of those, the
> ship-critical subset was fixed. **What is disclosed here is a different quantity from what the
> sweep found, and the two must not be read as one:** the sweep's finding is the seventy-six above;
> what remains uncorrected is **approximately thirteen sites in four classes** — the declared map's
> class set (Y1), what counts as a violation at equal timestamps (R1), a per-side criterion
> enumeration that omits criterion 1, and SC-13's description.
>
> **The number seventy-six is a FLOOR, not an extent.** The sweep's population was never measured.
> It was an agent-driven read over ten amendments, not a mechanically bounded scan, and no proof
> exists that it covered every passage describing every amended object. **The true size of this
> class is unknown and may be larger than the sweep found.** Nothing here should be read as bounding
> the class by seventy-six, or by thirteen.
>
> **The instrument's own limits, quoted verbatim rather than paraphrased:** its actual domain was
> *"ten amendments, agent-driven read"*; its gap was *"not mechanically bounded; no population
> proof"*; and its boundary test was *"none — this is the weakest instrument in the set, and its
> output is cited as evidence rather than relied on as coverage."*
>
> **WHICH INSTRUMENT PRODUCED THESE FIGURES — stated so the two are never conflated.** Both figures
> above are the **agent-driven description sweep's**. **Neither comes from any script.** In
> particular neither comes from `_K1_enumerate.py`, the K1 step-1 population enumerator, which
> shares the K1 label and nothing else: it enumerates blockquote runs in `SCHEMA_SET_FINAL.md` for
> the block manifest and has never counted a stale description. `_K1_enumerate.py` carries a defect
> — a literal BACKSPACE in its `MARK` regex, so the marker split it guards never runs — and **that
> defect does not touch these figures or anything else cited anywhere**: the script is superseded by
> `_K1_enumerate2.py`, and its own output is cited in no document. A later reader finding the K1
> defect should not go looking for its effect here, because there is none.
>
> **ONE STALE SENTENCE, NAMED BY LINE, NOT LEFT TO THE CLASS.** The class above is disclosed as a
> floor. **This sentence is disclosed individually, because it is known to be false and it was left
> in the registered text deliberately.**
>
> **Where:** `PREREG.md` **line 478 as registered at `prereg-v30`; line 948 in the amended file.**
>
> **Verbatim:** *"**This is a rebalance, not a tightening.** The two gates are incomparable: a
> fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old and
> passes the new; a fixture detected at PROVEN throughout but with one REVIEW finding on a clean
> source passes the old and fails the new. The trade is deliberate — drop the irrelevant requirement
> that acceptance detections be proofs, add the relevant requirement that **nothing shipped appears
> on clean or corrected material**."*
>
> **Why it is now false.** Its closing clause states criterion 3's purpose as a pure silence test on
> the corrected side. **SC-3 retired that premise.** Under the amendment the corrected side is
> scored against the declared ground-truth map: findings the map predicts are **required**, and a
> tool silent where the map declares a violation **fails**. The sentence describes a gate the
> registration no longer has.
>
> **The operative text is correct and is not affected.** The criterion itself — `PREREG.md` line 461
> as registered — **was replaced by SC-3**, and the replacement is what the gate reads. The applied
> text registers that *"the criteria of §6.2 as amended are the whole gate"*; line 948 is not a
> criterion, sits in §6.2's framing prose, is inside no clause block, and **no tool in the
> repository reads it** — verified by search, not assumed. **It is rationale, not operative.**
>
> **Why it was not amended.** Re-amending rationale prose would open a second approval cycle over a
> sentence that binds nothing, and line 97's rule — *"An amendment weaker than the thing it amends
> is not one"* — is not engaged, because **nothing is weakened by leaving it**: the operative
> criterion is strictly harder than the one this sentence describes. **The trade is accuracy of
> rationale against the cost of the tag, and it was taken knowingly.**
>
> **It was known false at tag time and left in place. That is the disclosure.** A reader who takes
> this sentence as a statement of what criterion 3 requires will be wrong, and should read SC-3.
>
> **Why the class was not measured before the tag.** Measuring the population means enumerating
> every passage in every corpus that describes every amended object, and judging each against what
> the object now is. That is larger than the amendment it would qualify, and it was ruled out of
> scope rather than attempted and abandoned. **The consequence is stated rather than mitigated: a
> reader relying on any description in these documents of an object amended by R9, R11, Y1, R1, R2,
> R16, SC-13 or Z1 should verify it against the registered text, because this registration does not
> warrant that such descriptions were all found.**

---

**D-INSTRUMENT — gaps in the verification apparatus itself.**

> **The checks that verify this ceremony have measured domains, and the gaps are disclosed.** Six
> remain open at the tag:
>
> 1. **`sha256sum -c` is one-directional.** It verifies listed→disk and cannot see a file on disk
>    that no manifest line covers. Two instruments outside it now assert the reverse direction (a
>    registration-checker scan of the tree, and a ceremony step against the index), but neither can
>    see a file added between the last check and `git commit`; the clean-tree assertion after commit
>    is the backstop.
> 2. **The line-citation check covers 6 of 395 citations.** The other 389 rest on classification,
>    and **71 of them could not be attributed to a target file at all** — a defect in the
>    classifier, recorded as such and not as coverage.
> 3. **The stale-description sweep has no measured population** (see D-STALE).
> 4. **The hash-count check cannot read informal quantifiers, Roman numerals, or the `six (6)`
>    form, and reads a range as its first value.**
> 5. **The staging check cannot see staging performed by any means other than a literal `git add`
>    line** — a wildcard, a variable or a loop is invisible to it.
> 6. **The round-reconciliation check reports that every working file is either in the
>    repository or declared ephemeral. Its population is a pinned scratchpad path, and that
>    path does not track the directory in which work is performed.** Its pass is therefore
>    evidence about the pinned directory alone, and is not evidence about files created
>    outside it. The files created during this amendment were placed in the repository or
>    declared ephemeral **by procedure, not by this check**. This states what the check does
>    not reach; it does not enumerate what it missed.
>
> **These are published because a verification apparatus that claims more than it delivers is the
> defect this project exists to detect in other people's pipelines**, and a pre-registration that
> exempted its own instruments from that standard would be making the claim it warns against.

---

**D-ARCHIVE — the external-input dependency.**

> **The fixture's inputs are not in this repository, and this is disclosed rather than resolved.**
>
> **The classifications were produced by `phase7_l2_sim.py`, committed in this repository and hashed
> in the tag message. The inputs it consumed are external to the repository, so a repository-only
> reader can audit the derivation but cannot re-execute it.**
>
> **THE FIGURES FOR THIS DISCLOSURE LIVE IN ONE ARTIFACT, AND THIS DISCLOSURE DOES NOT RESTATE
> THEM.** That artifact is `evidence/LARGE_ARTIFACTS_RECORD.md`, attested by its line in
> `evidence/MANIFEST.sha256`. Every per-file size, every count, and the archive's own total are
> there, measured and sourced. **A figure quoted in two places is a figure that will eventually
> disagree with itself.**
>
> **What is missing.** The producers read market data from a local archive outside the repository.
> The producing code is committed; the inputs are not. A reader holding this repository and nothing
> else **cannot regenerate the fixture from source** — they can verify every committed hash, re-run
> every check, and read every result, but the bytes the fixture was built from are not theirs to
> re-read. The position is: **(a) producing code in the repository — YES; (b) inputs in the
> repository — NO; (c) pipeline deterministic — YES, demonstrated twice over.**
>
> **MAGNITUDE.** The archive runs to **several hundred gigabytes**. What the producers actually read
> — traced through their own source rather than estimated — is **a few hundred megabytes across a
> bounded, enumerated set of files: a small fraction of one percent of the archive.** The inputs are
> **ZC 2025-01 and 2025-08 only**. The gap between what the archive holds and what the fixture needs
> is **roughly four orders of magnitude**, and that gap is the disclosable fact: the dependency
> looked like an archive-sized problem and is not one.
>
> **A NEGATIVE RESULT, REPORTED AS A POSITIVE FINDING.** The question *"what else does the fixture
> read?"* was put to the producers' own source, and the answer is **NONE**. The archive's other
> large trees — `processed/`, `pc2_transfer/`, `raw_data/`, each of them hundreds of gigabytes — are
> read by none of the producers. **The dependency is bounded, and it is bounded by reading the code
> rather than by asserting a scope.** A NONE that was looked for and not found is evidence; a NONE
> that was assumed is not — which is why the method is stated beside the result.
>
> **A second measured fact, disclosed because it changes what "durable" means.** The archive is
> **not synced to any cloud location, and neither is anything else**: the sync engine's database and
> the account file were both last written nearly three years before the tag. **Every copy of every
> artifact this registration depends on is on one machine, on one disk.**
>
> **Why the disclosure is not deleted now that the producing code ships.** Deleting it would claim a
> self-sufficiency the repository does not have. Bringing the file in closes the code half only.

---

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

> **NEITHER ARTIFACT — these are measurements OF THE ARCHIVE and of method** (§0.3's admissible
> third case). They bear on how every other number in this file was obtained, not on Artifact A
> or Artifact B.

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

**F.3 — THE ALL-ZERO CONTROL. An aggregate that comes back empty must be PROVED empty before it
may be reported, and a failed proof RAISES (item S4).**

**THE RULE, declared as binding method.** **Any aggregate that reports zero violations, zero
findings, all-clean, "no cells", "no rows", or an empty result set MUST be automatically
cross-checked against its source artifact before that result may be written down, printed, or
reported.** The cross-check is not optional, not a spot check, and not performed only when the
result looks surprising — it runs on **every** such aggregate, because the whole hazard is that a
broken aggregation and a genuine zero are indistinguishable at the point of reading. The minimum
sufficient form of the check is: **assert that the aggregation's keys exist in the source**
(every column name, class name, side value and boundary value it groups or filters on resolves to
a real field with a non-empty domain), **and assert that the source itself is non-empty on those
keys**; where a total is available by a second route, reconcile the two. **On mismatch the check
RAISES — it does not print a warning, does not annotate the output, and does not continue.** A
warning next to a zero is read as a zero; an exception is not read as anything, which is the
point. A zero that survives the check is reportable, and must be reported **with the check
named**, so that a reader can tell a proved zero from an unproved one.

**THE PROVENANCE, RECORDED HONESTLY, BECAUSE A RULE WITHOUT ITS NEAR-MISS IS A RULE NOBODY
BELIEVES.** Recorded here on the authority of item S4, as the account of the pass that produced
§13(i)'s R17(iii) check: **that near-miss was caught by visual inspection of a CSV row — by a
human eye on a line of data — and NOT by any control.** An aggregation keyed on **wrong column
names** returned **all zero** and raised nothing, because absent keys aggregated to an empty
group rather than to an error. Had that output been believed, it would have read as **"the
trade-class restriction makes the corrected side clean"** — and that is **the exact false result
R17(iii) exists to catch**: §13(i) states in terms that an all-zero return "would have meant that
the corrected-side violations recorded in §13(b) were carried entirely by an event source no
fixture column consumes, and that no fixture column violates anywhere on the corrected side —
which would have put criterion 1's REQUIRED list, and the discrimination framing of the corrected
side, in question." **So the check that this file's most consequential negative-result guard was
written to perform was, on that run, performed by luck.** The correct return — non-zero in the
same 18 cells — is the one §13(i) publishes; nothing in the record is wrong. **What was missing
was the control, and this note supplies it.**

**SCOPE: THIS BINDS FUTURE GATE REPORTING, NOT ONLY THIS FILE.** The rule is stated as method,
not as a note about one pass, and it applies wherever a zero or an all-clean is produced in this
programme — the gate report's per-criterion counts and its false-positive tallies; any
re-derivation of `n1\declared_map.csv` or of `y1\trade_class_only_map.csv`; any per-class,
per-side, per-instrument-month or per-column aggregation; and any statement that a column, class,
cell or criterion is clean. It composes with the dispositions already declared rather than
softening them: **§13(g)'s 72 UNSCORED cells are still UNSCORED and never clean**, **§C.4(a)'s
`buy_volume_10s` is still reported EXCLUDED and never MISSED**, and **§A.6.3's UNSCORED class
still "cannot be reported as a pass"** — F.3 adds that even a zero which IS reportable must first
be shown to be a measurement rather than an artefact of a broken key. It is the same principle
§F.1 states for archive-wide surveys (**"a negative result from such a search is not evidence of
absence"**) applied to aggregation instead of to search, and the same principle R9 records for
the gate as a whole: **silence and belief never convert into a pass.**

## 18. Element-to-evidence index (v30a assembly)

Covers **every** element and **every** section of this file, including the sections added by
item P2 and the two-artifact section §0 added by this pass. Lettered elements are the v30a
assembly elements; lettered SECTIONS are **§0 and §A-§F**.

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
| — | **THE TWO ARTIFACTS** — Artifact A (the f2 rebuild pair, 45-column MBO-reading lineage; what timing is MEASURED ON) vs Artifact B (the stored prediction pair, 35-column MBO-free; what the gate SCORES); the claims-to-artifact table; the lattice bridge; the asymmetry RESOLVED (the 45-column framing describes the LINEAGE, not the pair's two sides); the one-column-universe evidence and its limit; why §9's licence depends on it | **§0** (+ the header Fixture paragraph, rewritten) | y1\Y1_REPORT.md §1.1, §1.3, §4.1-§4.4; f2\ (phase5_ml_fixture.py, out\); results\phase7{,_fixed}\methodology_note.txt (SHA256 ea11e0…3535, identical); results\phase7{,_fixed}\l2_sim_results.csv headers; pc2_complete.txt / pc2_phase7_complete.txt; t4\fixture_manifest_35col_DRAFT.json (projection_verification) |
| — | **§6.2 conformance walk, element by element; the criterion-1 three-class partition (N = 11, 11+22+2 = 35); "waived" defined for §10.2; §A.6.5's SOURCE x GATE cross-tabulation of all 35 columns, all composing, with the two empty cells (S2)** | **§A**, incl. **§A.6.1-A.6.5** and **§A.12** | PREREG.md 443-481 (quoted verbatim per element); PREREG.md 93, 95, 97, 855, 1033, 1035 (verbatim); f1\f1_results.csv 50-52, 114-116; f3\fixture_manifest_DRAFT.json counts + 35-entry `columns` array; t4\fixture_manifest_35col_DRAFT.json counts_projected_subset; n1\declared_map.csv; n1\summary_corrected.csv; t1\t1_final_output.txt 61-67; y1\column_universe.csv (`source_class`); s13\s13_crosstab.py + s13\s13_crosstab_output.txt |
| a | Fixture identity; RE-EVALUATE from the stored predictions; reference AUCs; pc2 exclusion HARDENED | 8 | results\phase7{,_fixed}\l2_predictions\ (64 parquets each; columns pred_score/true_label/fwd_move_ticks/mid_price_t); f1\f1_results.csv; c3\label_equality.csv; c3\pc2_diff_summary.csv; f5\DEVIATIONS_entry_SKELETON.md 40-48 |
| b | Shared label vector — the feature-availability-only licence | 9 | c3\label_equality.csv 2-65 |
| c | **EVIDENCE for §1's boundary**; PRIMARY/cross-check table; off-by-one reconciliation; lag-image | 10 | t1\violation_table.csv 4, 67 (PRIMARY); c4\independent_counts.csv 3, 11; n1\lattice_profile.csv; n3\cohort_profile.csv; v1\mean_overhang_by_class.csv |
| d | Session-tail label semantics | 11 | t3\day_edge_table.csv 2-5; t3\day_edge_samples.csv; v2\reanchor_gaps.csv |
| — | **Fixture lattice provenance and generation** | **§B** | n2\lattice_provenance.csv (228 files); n2\provenance_notes.md (a)-(e); n2\block_overlap.csv; PC2_SETUP_README.txt; MASTER_FINDINGS\v4\G2_G3_summary.txt |
| e | `ties: available` (R1); both-branch counts INFORMATIONAL; 49 equal events are NON-VIOLATIONS; T1 PRIMARY and the contaminated-minus-1 qualifier on C4 | 12 | t1\violation_table.csv equal_count (PRIMARY); n1\declared_map.csv; m5\per_instrument_counts.csv; c4\independent_counts.csv (prev_row_B, lag-image, −1 on MBO classes) |
| f | **The DECLARED GROUND-TRUTH MAP (R9)** — 984 rows; 18/48 corrected non-zero; 13 measured-zero over scored classes (**nq — TRADES-CLASSES-ONLY, 4 of 10 classes scored, 6 UNSCORED not zero, NOT a pass** — its "clean on both branches" WITHDRAWN, R12); contaminated saturation; N3 predicate; ZC 2025-01 cell + pedigree; M5; 72 unscored for lack of an MBO file AT THE FIXTURE PATH `processed\nq\` (same-generation MBO exists out of path — §13(h) supersedes R12's stated reason); **(h) the non-gated NQ cross-generation diagnostic (X4)**; **(i) BOTH MAPS side by side per R17(ii) — full-class AS MEASURED vs fixture-universe-restricted, with the R17(iii) non-zero check**; **(j) the six `mbo_*` classes after Y1 — what they evidence and what they may never again be quoted as, with the `BOUNCE_FREE_FEATURES` caution** | 13 | n1\declared_map.csv; n1\summary_corrected.csv; n1\summary_contaminated.csv; n1\lattice_profile.csv; n1\unscored_ledger.csv; n1\m5_maxima_comparison.csv; n1\compare_to_m5_output.txt; n3\predicate_check.csv; n3\invariants.txt; n3\exceptions.csv; n3\converse_by_instrument_month.csv; n3\compare_output.txt; m5\ (whole round); t1\violation_table.csv; c4\independent_counts.csv; t1\t1_final_output.txt 19 |
| — | **Two-sided ground-truth enumeration; comparator pinned to at_source; column dispositions; §C.3's FOUR CATEGORIES stated separately (22 OOJ / `book_imbalance_ratio` UNSCORED one-class-only per R16 / the 8 Phase-5-only columns OUTSIDE the fixture's column universe / the REQUIRED 11), with the 27-column list RETIRED as a class claim; **§C.5's `vwap_distance` DUAL-GROUND statement — REQUIRED on the forward-join ground, OUT OF JURISDICTION on the same-row `mid[t]` ground, ONE gate class only under R16's discipline (S3)** | **§C** | f3\fixture_manifest_DRAFT.json (35-entry `columns` array, 19-entry `not_fed_to_phase7_models`, `counts`); y1\column_universe.csv; phase5_ml.py 222, 230-235, 237-258, 267-285; phase7_l2_sim.py 207, 216-231, 246-248, 266, 276; n1\declared_map.csv; n3\predicate_check.csv; n3\converse_by_instrument_month.csv; PREREG.md 190-197; t4\fixture_manifest_35col_DRAFT.json |
| g | Contaminated-side profile; overhang means 506.3-655.2 ms; M4 stamp-type concentration; **BOTH PROFILES side by side per S1 — full-class AS MEASURED (75.21%, `mbo_all`) vs fed-column-restricted (26.49%, `trades_all` ≡ `trades_sell`), delta −48.72 pp / −164,747 rows stated plainly; §13(j)'s forbidden-use rules restated for the contaminated side; §14.1's 48-cell restricted-vs-full table** | 14 + **14.1** | t1\violation_table.csv (contaminated/decision_T, lines 2, 5, 8, 11, 14, 17, 38, 41, 47, 50, 62, 65, 86, 89, 95, 98); t1\t1_final_output.txt 2-13, 22-52; v1\mean_overhang_by_class.csv; m4\stamp_type_breakdown.csv; m4\viol_rate_by_remaining_time.csv; y1\trade_class_only_map.csv (48 contaminated rows); n1\declared_map.csv (cross-check, 0 mismatches over all 96 rows); s13\s13_derive.py + s13\s13_derive_output.txt; s13\s13_peaks.py; s13\s13_table.py |
| h | As-built defects, INHERITED, R4 split, **C5-DECIDED-WRAPPED** | 15 | c2\aggregation_comparison.md; R2_consolidated_report.md C1/C2/C5; c5\env_records.md; t1\violation_table.csv note; t1\t1_final_output.txt 61-67; results\phase5_fixed\gpu_track2_log.txt |
| i | Documented-unverifiable assumptions (cite for item 2 CORRECTED) | 16 | f3\fixture_manifest_DRAFT.json (via Part I cross-check); c2\aggregation_comparison.md construct row 20; R2_consolidated_report.md C2 "Blockers (carried)" and C1 residual paragraph |
| j | T4 35-column projection results | 17 | t4\fixture_manifest_35col_DRAFT.json; t4\t4_verification_report.json |
| — | **Lock language: freeze, the hash enumeration, interpretation rule** | **§D** | prereg-v30 tag message (five SHA-256 lines, read this pass); PREREG.md 97, 95, 99, 480; n1\declared_map.csv |
| — | **Gate protocol input surface** | **§E** | this declaration's declared elements; n1\declared_map.csv named as withheld |
| — | **Method notes: Grep undercount; numbers discipline; §F.3's ALL-ZERO CONTROL — every zero/all-clean aggregate must be cross-checked against its source artifact and a mismatch RAISES, with the R17(iii) near-miss recorded as its provenance (S4)** | **§F**, incl. **§F.3** | c1\tagger_survey_capture.txt line 17 (119 by os.walk) vs 37 by default-excluded search, measured this pass; n2\provenance_notes.md (228-file walk); §13(i)'s R17(iii) paragraph (the false result the control exists to catch) |
| k | Working-resolution record **R1-R9 and R11-R13** (no R10), verbatim | file tail | this file (frozen byte-identical; the tail heading occurs exactly once, and the tail runs unbroken to EOF) |

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
