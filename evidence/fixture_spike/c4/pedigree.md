# C4 pedigree record — blind independent re-measurement of corrected-side availability (ZC 2025-01)

Assembled by item M2. This record documents the full provenance chain of the C4 gate result:
tasking, environment pins, blindness attestations, method structure (including the second
method), and the count-by-count comparison against T1's orchestrated measurement.

Primary sources (absolute paths):

| Role | Path |
|---|---|
| Tasking (verbatim) | `C:\Users\ttbea\.claude\projects\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\workflows\scripts\r2-gate-checks-wf_e5854e83-534.js` (lines 37-52) |
| C4 agent result | `C:\Users\ttbea\.claude\projects\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\subagents\workflows\wf_e5854e83-534\journal.jsonl` (line 5, agentId `a8b3830d5bf32c3c2`, key `v2:2fa62020de95408b4d9e70d1f83b48c3061a900648c27a4245d7833c3d88f1c2`) |
| Checker source | `...\scratchpad\fixture_spike\c4\independent_checker.py` |
| C4 counts | `...\scratchpad\fixture_spike\c4\independent_counts.csv` (20 data rows) |
| T1 counts | `...\scratchpad\fixture_spike\t1\violation_table.csv` (99 data rows = 33 feature columns x 3 (side, boundary) blocks; 100 lines incl. header) |
| Orchestrator comparison | `...\scratchpad\fixture_spike\R2_consolidated_report.md` (C4 section, lines 15-19) |
| M2 comparison derivation | `...\scratchpad\fixture_spike\c4\build_t1_c4_comparison.py`, output `t1_vs_c4_comparison.csv` + captured log `build_t1_c4_comparison_output.txt` |

(`...` abbreviates `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1` for readability; every file above sits at the full path.)

---

## 1. Tasking (verbatim)

Source: `r2-gate-checks-wf_e5854e83-534.js`, the `c4` agent prompt, **lines 37-52**, dispatched
with `{ label: 'C4-blind-remeasure', phase: 'Gate', schema: SCHEMA }`. Quoted verbatim from the
JS source: `${ARCHIVE}` and `${SCRATCH}` are template constants defined at lines 22-23
(`SCRATCH = 'C:\\Users\\ttbea\\AppData\\Local\\Temp\\claude\\...\\scratchpad\\fixture_spike'`,
`ARCHIVE = 'C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025'`), and doubled backslashes render as
single backslashes in the prompt the agent received.

```
const c4 = () => agent(`HARD BOUNDARIES: (1) The archive ${ARCHIVE} is READ-ONLY. (2) Write ONLY under ${SCRATCH}\\c4\\. (3) INDEPENDENCE REQUIREMENT — this is a blind re-measurement: you MUST NOT read anything under ${SCRATCH}\\t1\\, ${SCRATCH}\\f4\\, any file named *violation*, any prior task output under ...\\tasks\\, or any workflow journal. You may read ONLY: the fixture builder source at ${SCRATCH}\\f2\\phase5_ml_fixture.py (and ${SCRATCH}\\f2\\fixture.py), the raw archive parquets named below, and the built lattice pickles at ${SCRATCH}\\f2\\out\\ if needed for timestamps. (4) Implement ALL checker computation in POLARS or PYARROW — not pandas (pip install polars if absent; pandas is permitted solely, if unavoidable, to unpickle a timestamp column from a pkl, and for nothing else — prefer deriving the lattice from parquet instead). (5) Report exact counts; if anything is inconsistent, report it raw — do NOT reconcile.

ITEM C4 (GATE) — INDEPENDENT RE-MEASUREMENT of the corrected-side availability result on ZC 2025-01, written from the availability definitions below alone.

DEFINITIONS (the fixture's availability model):
- The fixture lattice: rows of the ZC 2025-01 build = snapshot rows of ${ARCHIVE}\\processed\\zc\\zc_snapshots_2025-01.parquet after the builder's session-hour filter (read the filter definition from the builder source and apply it yourself in polars). Each row has a stamp T (its timestamp). Expected row count from the build record: 338,159 — verify; if your independently derived lattice differs, REPORT THE DISCREPANCY prominently and, as fallback, extract the timestamp column from ${SCRATCH}\\f2\\out\\corrected_zc_2025-01_run1.pkl, reporting both counts.
- Wall-clock join: trade and MBO event aggregates attach to a row via the row's wall-clock second ts_floor = floor(T, 1s). CORRECTED side: the feature content of row i comes from the PREVIOUS row's second [floor(T_{i-1}), floor(T_{i-1})+1s) (a one-row shift of all joined aggregates). Row 0 has no content.
- Decision time of row i = its own stamp T_i. Tie branches: an absorbed event with ts_event strictly AFTER T_i violates availability under BOTH branches; ts_event EXACTLY EQUAL to T_i is a violation only under ties=unavailable. Report strict and equal counts separately.
- Event classes (10), defined by the builder's aggregation semantics (verify the defining lines in the builder source and quote them): trades_all, trades_buy (per the builder's own is_buy test evaluated against the parquet's actual aggressor_side values — if the test matches nothing, the class is empty; measure, do not fix), trades_sell (complement per the builder), trades_large (is_large per builder); mbo_all, mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any. Raw events: ${ARCHIVE}\\processed\\zc\\zc_trades_tagged_2025-01.parquet and zc_mbo_2025-01.parquet (event time column: verify from the builder's loading code). Map each class to the wall-clock-joined feature columns it feeds (33 columns total per the builder's construction — enumerate them yourself from the source with line quotes).

MEASURE, for the CORRECTED side, for every row i >= 1 including every re-anchor gap row (spacing != 1 s; report how many such rows you find, and their counts as a separate subset):
(a) vs DECISION time T_i: per event class, count of rows whose absorbed window [floor(T_{i-1}), floor(T_{i-1})+1s) contains an event with ts_event > T_i (strict) and == T_i (equal).
(b) SECONDARY, same window vs the boundary B_i = T_{i-1}: strict (> T_{i-1}) and equal (== T_{i-1}) counts per class.
Justify window-length independence in one sentence (why w-second rolling windows reduce to the newest second) and verify it on a 500-row sample for one class.

Deliverables: c4\\independent_checker.py (polars/pyarrow), c4\\independent_counts.csv (class, boundary, strict_count, equal_count, total_rows, gap_row_subset_strict, gap_row_subset_equal), and findings carrying the full table inline plus the quoted builder lines you derived definitions from. State your polars/pyarrow versions. Your verdict states the measured counts plainly — you have no target numbers; whatever you measure is the result.`, { label: 'C4-blind-remeasure', phase: 'Gate', schema: SCHEMA })
```

### 1a. The blindness constraints (line 37, excerpt)

> "(3) INDEPENDENCE REQUIREMENT — this is a blind re-measurement: you MUST NOT read anything under `${SCRATCH}\\t1\\`, `${SCRATCH}\\f4\\`, any file named `*violation*`, any prior task output under `...\\tasks\\`, or any workflow journal. You may read ONLY: the fixture builder source at `${SCRATCH}\\f2\\phase5_ml_fixture.py` (and `${SCRATCH}\\f2\\fixture.py`), the raw archive parquets named below, and the built lattice pickles at `${SCRATCH}\\f2\\out\\` if needed for timestamps."

### 1b. Absence of target numbers (line 52, closing sentence)

> "Your verdict states the measured counts plainly — you have no target numbers; whatever you measure is the result."

Attestation on prompt contents: the ONLY measured-quantity numeral anywhere in the C4 prompt is
the lattice row count **338,159** (line 42), supplied for verification and paired with an explicit
failure branch ("if your independently derived lattice differs, REPORT THE DISCREPANCY prominently
and, as fallback, extract the timestamp column from ... reporting both counts"). Every other
numeral is structural, not a result: "2025-01" (dataset month), "1 s" (window length), "row 0" /
"i >= 1" (indexing), "10" (event-class count), "33" (feature-column count), "500" (sample size).
**No violation count appears in the prompt** — not 89,568, not 254,314, not any strict/equal/gap
figure, nor any zero-count claim for the decision-time boundary.

---

## 2. Environment / version pins

From the C4 agent's journal result (journal.jsonl line 5), verdict text and finding 10:

| Component | Pin | Role | Source |
|---|---|---|---|
| polars | **1.43.2** | ALL checker computation | journal verdict: "Tools: polars 1.43.2 (all checker computation)"; finding 10 |
| pyarrow | 23.0.1 | schema/metadata inspection only | journal verdict + finding 10 |
| Python | 3.12 | interpreter | journal finding 10 |
| pandas | **not used** | — | journal verdict: "pandas not used"; finding 10: "pandas not used anywhere" |

The version pin is executable, not just narrated — `independent_checker.py` prints it at runtime:

- Line 43: `import polars as pl`
- Line 52: `print("polars", pl.__version__)`

The checker's only imports are `sys` (line 42), `polars` (line 43), and `random` (line 192) — no
pandas import exists anywhere in the file. The pkl fallback was not needed: the independently
derived lattice matched the build record exactly (338,159 rows), so no pickle was unpickled and
the pandas concession in boundary (4) was never exercised (journal verdict: "pkl fallback not
needed since the lattice matched 338,159 exactly").

---

## 3. Blindness attestation chain

1. **Prompt-level prohibition** — the tasking itself (line 37, quoted in 1a) forbids reading
   `t1\`, `f4\`, any `*violation*` file, prior task outputs, and workflow journals, and whitelists
   exactly three inputs: builder source, raw archive parquets, and (timestamps only, if needed)
   the f2 lattice pickles.
2. **Prompt-level absence of targets** — line 52 (quoted in 1b): "you have no target numbers".
   Verified in 1b: no violation count appears anywhere in the prompt; the sole expected number
   (lattice 338,159) carries a report-the-discrepancy instruction, not a force-agreement one.
3. **Agent attestation** — journal.jsonl line 5, finding 10, verbatim: "no files under t1/, f4/,
   tasks/, or any *violation* file were read."
4. **Checker-source consistency** — `independent_checker.py` reads only
   `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\zc_snapshots_2025-01.parquet` (line 56),
   `zc_trades_tagged_2025-01.parquet` (line 89), and `zc_mbo_2025-01.parquet` (line 94) — `BASE`
   is the archive path (line 47); its docstring (lines 1-41) derives every definition from
   builder-source line numbers — the complete citation set appearing in the docstring is
   `f2/phase5_ml_fixture.py` L58, L126, L162, L163-167, L171, L187, L188, L189, L225, L233,
   L234-239 and `f2/fixture.py` L51 — never from T1 artifacts. (The additional citations L128 and
   L156-172 appear in the agent's journal findings 6 and 7, not in the persisted docstring; the two
   citation sets are recorded separately here rather than merged.)
5. **Post-hoc orchestrator comparison** — the count-by-count T1 comparison was performed by the
   orchestrator AFTER the blind result landed (`R2_consolidated_report.md` line 18: "Orchestrator
   comparison vs T1: no disagreement at any published count. No stop-and-report condition.").
6. **M2 independent re-derivation (this record)** — the full comparison table in section 6 was
   rebuilt mechanically from `t1\violation_table.csv` and `c4\independent_counts.csv` by
   `c4\build_t1_c4_comparison.py`; captured output in `c4\build_t1_c4_comparison_output.txt`,
   derived table in `c4\t1_vs_c4_comparison.csv`. Result: all 20 (class, boundary) cells agree
   exactly.

---

## 4. Method structure, including the second method

### 4a. Primary method — vectorized per-second aggregate join (`independent_checker.py` lines 115-174)

Per event class: reduce events to a per-second maximum event timestamp plus the set of distinct
exact event timestamps, join both onto the lattice, and evaluate the four boundary flags as
column expressions. Key lines, verbatim:

Lines 131-135:
```python
    # per-second max event timestamp
    agg = (ev.with_columns(pl.col("ts_event").dt.truncate("1s").alias("sec"))
             .group_by("sec").agg(pl.col("ts_event").max().alias("max_ts")))
    # distinct exact event timestamps (for equality tests)
    ets = ev.unique().with_columns(pl.lit(True).alias("has_ev"))
```

Lines 143-151 (the four flags — strict/equal against decision time `T` and against the
previous-row boundary `Tprev`):
```python
           .with_columns(
               # (a) vs decision time T_i
               (pl.col("max_ts").is_not_null() & (pl.col("max_ts") > pl.col("T"))).alias("strict_T"),
               (pl.col("ev_at_T").fill_null(False)
                & (pl.col("T").dt.truncate("1s") == pl.col("wstart"))).alias("equal_T"),
               # (b) vs boundary B_i = T_{i-1} (an event == T_{i-1} always lies in the window)
               (pl.col("max_ts").is_not_null() & (pl.col("max_ts") > pl.col("Tprev"))).alias("strict_B"),
               pl.col("ev_at_Tprev").fill_null(False).alias("equal_B"),
           )
```

### 4b. In-file second method — exact-ns brute-force union check (lines 180-213)

An independent implementation path (integer-nanosecond arithmetic, Python set/dict membership, no
polars joins) that verifies window-length independence on a 500-row random sample. Header comment,
verbatim (lines 180-183):

```python
# ── 4. Window-length independence: 500-row empirical check, class=mbo_all, w=5 ─
# Union window of corrected rolling-w at row i = union of seconds of rows i-w..i-1.
# Claim: strict/equal violation vs T_i in the union  <=>  violation in newest second (row i-1).
# All arithmetic in integer nanoseconds to keep exact ns precision.
```

Deterministic sampling: line 193 `random.seed(20260810)`, line 194
`sample_idx = sorted(random.sample(range(W, N), 500))`; verdict printed at lines 211-212.
Reported outcome (journal finding 9): **0 mismatches** over 500 sampled rows, class mbo_all, w=5,
for both strict and equal flags.

### 4c. Second counting method — event-level inner join (journal-attested)

The journal verdict additionally records a second, independent COUNTING method that re-derived the
headline counts by joining at event level rather than via per-second aggregates:

> "Counts cross-checked by a second, event-level join method with exact agreement (trades_all:
> 89568/20 strict/equal at B, 0 at T)."

and journal finding 4's source field:

> "cross-checked for trades_all by an independent event-level inner-join method (exact agreement:
> 89568 strict_B, 20 equal_B, 0 strict_T)"

Provenance note, reported raw: this event-level cross-check is attested in the journal result
(journal.jsonl line 5) and was run in the C4 agent's transcript; its code is NOT persisted inside
`c4\independent_checker.py` (the persisted file's second implementation path is the exact-ns
brute-force check of 4b). The persisted-file evidence and the journal attestation are therefore
distinct links in the chain and are both recorded here as such.

---

## 5. The C4 result (journal verdict, verbatim)

`journal.jsonl` line 5, `result.verdict`, quoted in full:

> MEASURED RESULT: Against decision time T_i, the corrected side shows ZERO availability
> violations — strict_count = 0 and equal_count = 0 for all 10 event classes over all 338,158
> measured rows (i>=1), including all 28 re-anchor gap rows. This is structurally forced and
> empirically confirmed: the independently derived lattice (338,159 rows, exactly matching the
> build record) has minimum row spacing of exactly 1s (338,130 rows at exactly 1s; 28 gaps all >=
> 68.84s; zero sub-second or duplicate spacings), so the absorbed window
> [floor(T_{i-1}), floor(T_{i-1})+1s) always ends at or before T_i. Against the secondary boundary
> B_i = T_{i-1} the same windows contain abundant post-boundary events — e.g. trades_all
> strict=89,568 / equal=20; mbo_all strict=254,314 / equal=29 — i.e. the absorbed second extends
> past the previous row's stamp (events between T_{i-1} and the end of its second), but never past
> the current row's decision time. Full table: trades_all decision_T 0/0, prev_row_B 89568/20
> (gap 12/0); trades_buy 0 events (builder's is_buy test matches nothing against actual
> aggressor_side values BUY_AGGRESSOR/SELL_AGGRESSOR/UNKNOWN — measured as empty, not fixed) all
> counts 0; trades_sell decision_T 0/0, prev_row_B 89568/20 (gap 12/0); trades_large (75,606
> events) decision_T 0/0, prev_row_B 23633/20 (gap 0/0); mbo_all (8,272,769 events) decision_T
> 0/0, prev_row_B 254314/29 (gap 19/0); mbo_bid_add (1,239,887) decision_T 0/0, prev_row_B
> 164958/1 (gap 13/0); mbo_ask_add (1,223,790) decision_T 0/0, prev_row_B 162753/4 (gap 16/0);
> mbo_bid_cancel (1,219,431) decision_T 0/0, prev_row_B 135980/23 (gap 11/0); mbo_ask_cancel
> (1,212,634) decision_T 0/0, prev_row_B 129333/22 (gap 14/0); mbo_cancel_any (2,432,065)
> decision_T 0/0, prev_row_B 179856/24 (gap 15/0). All gap-row equal counts are 0 on both
> boundaries. Window-length independence verified: 500-row random sample, class mbo_all, w=5, 0
> mismatches between union-of-absorbed-seconds flags and newest-second flags (strict and equal).
> Counts cross-checked by a second, event-level join method with exact agreement (trades_all:
> 89568/20 strict/equal at B, 0 at T). Tools: polars 1.43.2 (all checker computation), pyarrow
> 23.0.1 (schema inspection only); pandas not used; pkl fallback not needed since the lattice
> matched 338,159 exactly.

Orchestrator's C4 section (`R2_consolidated_report.md` lines 15-19, verbatim):

> ### C4 — blind independent re-measurement: GREEN, full agreement with T1
> - Blind agent (T1 implementation and outputs unread; no target numbers in prompt), checker in
>   **polars 1.43.2** (no pandas), lattice **independently derived** from the snapshots parquet +
>   builder filter definition: 338,159 rows, exact match.
> - **Corrected side vs decision time: 0 strict + 0 equal for all 10 event classes over all
>   338,158 rows, including all 28 re-anchor gap rows.** Secondary boundary B=T_prev: trades_all
>   89,568/20; mbo_all 254,314/29; per-class MBO counts at contaminated−1 (last-row indicator),
>   trades at −0 — exactly T1's published/implied values. Internal second-method cross-check
>   (event-level join) agreed exactly.
> - Orchestrator comparison vs T1: **no disagreement at any published count. No stop-and-report
>   condition.**
> - Evidence: `c4\independent_checker.py`, `c4\independent_counts.csv`.

---

## 6. Comparison table — T1 vs C4, all 10 classes, both boundaries

Derivation: T1's `violation_table.csv` is per feature COLUMN (33 columns across 10 event classes;
99 data rows = 33 columns x three (side, boundary) blocks — (contaminated, decision_T),
(corrected, decision_T), (corrected, claimed_T_prev), 33 rows each). `build_t1_c4_comparison.py`
collapsed it to
per-class values after ASSERTING that every column within a (class, side, boundary) cell carries
identical counts (all assertions passed; column coverage check: 33/33). Boundary-name mapping: T1
`claimed_T_prev` ≡ C4 `prev_row_B` (both are B_i = T_{i-1}); `decision_T` is named identically.
T1 corrected side and C4 both measure rows i >= 1 (total_rows = 338,158); T1 contaminated side
measures all rows (338,159).

### 6a. Boundary = decision time T_i (corrected side)

| event_class | T1 cols in class | T1 corrected strict/equal | C4 strict/equal | exact agreement |
|---|---:|---:|---:|---|
| trades_all | 11 | 0 / 0 | 0 / 0 | YES |
| trades_buy | 2 | 0 / 0 | 0 / 0 | YES |
| trades_sell | 2 | 0 / 0 | 0 / 0 | YES |
| trades_large | 2 | 0 / 0 | 0 / 0 | YES |
| mbo_all | 3 | 0 / 0 | 0 / 0 | YES |
| mbo_bid_add | 3 | 0 / 0 | 0 / 0 | YES |
| mbo_ask_add | 3 | 0 / 0 | 0 / 0 | YES |
| mbo_bid_cancel | 3 | 0 / 0 | 0 / 0 | YES |
| mbo_ask_cancel | 3 | 0 / 0 | 0 / 0 | YES |
| mbo_cancel_any | 1 | 0 / 0 | 0 / 0 | YES |

(C4 additionally reports the 28-row re-anchor gap subset: 0/0 for every class at this boundary.
T1 did not break out gap rows; no comparison cell exists for that subset.)

### 6b. Boundary = B_i = T_{i-1} (T1 `claimed_T_prev` ≡ C4 `prev_row_B`, corrected side)

| event_class | T1 corrected strict/equal | C4 strict/equal | exact agreement | C4 gap subset s/e | T1 contaminated decision_T strict/equal | contaminated − C4 strict |
|---|---:|---:|---|---:|---:|---:|
| trades_all | 89,568 / 20 | 89,568 / 20 | YES | 12 / 0 | 89,568 / 20 | **0** |
| trades_buy | 0 / 0 | 0 / 0 | YES | 0 / 0 | 0 / 0 | **0** |
| trades_sell | 89,568 / 20 | 89,568 / 20 | YES | 12 / 0 | 89,568 / 20 | **0** |
| trades_large | 23,633 / 20 | 23,633 / 20 | YES | 0 / 0 | 23,633 / 20 | **0** |
| mbo_all | 254,314 / 29 | 254,314 / 29 | YES | 19 / 0 | 254,315 / 29 | **1** |
| mbo_bid_add | 164,958 / 1 | 164,958 / 1 | YES | 13 / 0 | 164,959 / 1 | **1** |
| mbo_ask_add | 162,753 / 4 | 162,753 / 4 | YES | 16 / 0 | 162,754 / 4 | **1** |
| mbo_bid_cancel | 135,980 / 23 | 135,980 / 23 | YES | 11 / 0 | 135,981 / 23 | **1** |
| mbo_ask_cancel | 129,333 / 22 | 129,333 / 22 | YES | 14 / 0 | 129,334 / 22 | **1** |
| mbo_cancel_any | 179,856 / 24 | 179,856 / 24 | YES | 15 / 0 | 179,857 / 24 | **1** |

Row-count columns agree everywhere: T1 corrected total_rows = C4 total_rows = **338,158** in all
20 cells; T1 contaminated total_rows = **338,159**.

**Result: exact T1-vs-C4 agreement in all 20 (class, boundary) cells** — strict, equal, and
total_rows (captured log `build_t1_c4_comparison_output.txt`, final lines: "ALL 20
(class,boundary) cells exact T1-vs-C4 agreement: True").

### 6c. The documented contaminated-minus-1 relation at prev_row_B

The corrected side's prev_row_B measurement at row i+1 evaluates the SAME window
[floor(T_i), floor(T_i)+1s) against the SAME boundary T_i as the contaminated side's decision_T
measurement at row i. The corrected side (rows i >= 1) therefore absorbs the seconds of rows
0..N−2 only: the last lattice row's second (row N−1) is never absorbed by any subsequent row.
Hence, per class:

> corrected prev_row_B strict = contaminated decision_T strict − [last row's own second contains a
> post-T_{N−1} event of the class]

The delta is a **last-row indicator**: 1 for all six MBO classes (an MBO event follows T_{N−1}
within its second), 0 for all four trades classes (no trade does; trades_buy is empty as built).
Equal counts carry no last-row contribution here and match exactly in every class (20, 0, 20, 20,
29, 1, 4, 23, 22, 24). This is the relation the orchestrator documented in
`R2_consolidated_report.md` line 17: "per-class MBO counts at contaminated−1 (last-row indicator),
trades at −0 — exactly T1's published/implied values." Derived deltas (captured log, final lines):
mbo classes all 1; trades classes all 0.

---

## 7. File inventory (this record's evidence set)

Under `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\`:

- `c4\pedigree.md` — this record (item M2 deliverable)
- `c4\independent_checker.py` — the blind checker (polars; version print line 52)
- `c4\independent_counts.csv` — C4's 20-row result table (10 classes x 2 boundaries)
- `c4\build_t1_c4_comparison.py` — M2's mechanical comparison derivation
- `c4\t1_vs_c4_comparison.csv` — derived 20-row comparison table (all fields of sections 6a/6b)
- `c4\build_t1_c4_comparison_output.txt` — captured run log (assertions, per-cell verdicts, deltas)
- `c4\m2_verify_pedigree.py` — M2's claim-by-claim verification pass over this record (section 8)
- `c4\m2_verification_log.txt` — captured verification output (35 checks, 0 failures)
- `t1\violation_table.csv` — T1's per-column measurement (read-only input)
- `R2_consolidated_report.md` — orchestrator consolidation (C4 section lines 15-19)

External (read-only):

- `C:\Users\ttbea\.claude\projects\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\workflows\scripts\r2-gate-checks-wf_e5854e83-534.js` — tasking (lines 22-23, 37-52)
- `C:\Users\ttbea\.claude\projects\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\subagents\workflows\wf_e5854e83-534\journal.jsonl` — C4 result (line 5)

---

## 8. M2 verification pass (claim-by-claim re-check of this record)

Every assertion in sections 1-6 was re-checked mechanically against its primary source by
`c4\m2_verify_pedigree.py`; captured output at `c4\m2_verification_log.txt`. **35 checks, 0
failures.** What the pass confirms, beyond the quote-level checks already described:

- The section-1 tasking block is byte-identical to `r2-gate-checks-wf_e5854e83-534.js` lines 37-52,
  and the dispatch options `label: 'C4-blind-remeasure'` sit on line 52.
- The blindness attestation is machine-verified, not asserted: tokenizing every numeral in the C4
  prompt yields exactly `['0','01','01,','1','10','2','2025','3','33','338,159','4','5','500']` —
  `338,159` is the sole measured quantity, and an explicit search for each published count
  (89568, 254314, 23633, 164958, 162753, 135980, 129333, 179856, 338158) finds **none** in the prompt.
- The section-5 journal verdict is verbatim from `journal.jsonl` line 5 (agentId
  `a8b3830d5bf32c3c2`), and R2 lines 15-19 are verbatim from `R2_consolidated_report.md`.
- `independent_checker.py` contains exactly three import statements — lines 42, 43, 192 — so the
  "no pandas" claim is structural, and the file's only parquet reads are the three archive files.
- The T1-vs-C4 comparison was re-derived from the two CSVs by an independent code path in this
  session; its 20-row output is **byte-identical** to the stored `c4\t1_vs_c4_comparison.csv`, and
  its log matches `c4\build_t1_c4_comparison_output.txt` line for line (the only differences: a
  UTF-8 BOM on the stored file's first line, and the trailing `wrote <path>` line naming the
  re-run's own output path).
- All 30 T1 (class, side, boundary) cells are column-uniform, so the per-column-to-per-class
  collapse in section 6 is lossless.

### 8a. Corrections applied to this record by the verification pass

Two defects were found in the pre-verification draft and corrected in place; both were descriptive,
neither touched a measured count:

1. **T1 row count.** The draft described `t1\violation_table.csv` as "100 data rows" (sections 0
   and 6). The file holds **99 data rows** (33 feature columns x 3 (side, boundary) blocks); 100 is
   the line count including the header. Corrected in both places.
2. **Docstring citation set.** Section 3 item 4 listed the checker docstring's builder-source
   citations as "L58, L126, L128, L156-172, L187-189, L225, L233". The citations actually present in
   `independent_checker.py` lines 1-41 are `phase5_ml_fixture.py` L58, L126, L162, L163-167, L171,
   L187, L188, L189, L225, L233, L234-239 and `fixture.py` L51; **L128 and L156-172 appear in the
   agent's journal findings 6 and 7, not in the persisted docstring.** The draft had merged the two
   citation sets; they are now recorded separately, consistent with the same
   persisted-file-vs-journal-attestation distinction drawn in section 4c.
