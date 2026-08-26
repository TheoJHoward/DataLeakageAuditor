# FROZEN ERRATA REGISTER — leakaudit / MBO paper

**Created:** 2026-08-12
**Status of ALL entries:** `DEFERRED-PER-R10`
**Scope:** paper-side errata candidates surfaced during the fixture verification rounds
(Phase 0 spikes S1–S5, F1–F5, T1–T4, DELTA R2 items C1–C6, DELTA R5 items V1–V7,
DELTA R6 items M3–M5 / N1–N3).
**Not in scope:** the class C amendment `prereg-v30a` (the acceptance-fixture amendment).
v30a stands on its own and neither asserts nor depends on any paper correction — see R10 below.

---

## 0. The deferral decision (R10), verbatim

> The paper-side errata are DEFERRED by author decision until the tool ships. They are not
> abandoned and not diminished. Record the deferral, its date, and its rationale (tool has a
> deadline; paper does not) in the errata register. No errata text is drafted, filed, or
> published until the author reopens it. The v30a amendment stands on its own and neither
> asserts nor depends on any paper correction.

**Deferral date:** 2026-08-12 (date this register was created and frozen).
**Deferral rationale (as stated in R10):** the tool has a deadline; the paper does not.
**Operative consequence:** no errata text is drafted, filed, or published until the author
reopens it. This register is a *record*, not a draft erratum. Nothing in it is an errata
notice, a correction, or a retraction; it does not commit the author to any of those.

---

## 1. How to read this register

Every entry carries an explicit three-way epistemic split. The three labels mean exactly this
and nothing more:

| Label | Meaning |
|---|---|
| **PROVEN** | Execution-witnessed or directly measured. Either a script under `scratchpad\fixture_spike\` ran and produced the number, or a file's own bytes/metadata were read and the value is a property of the file. A verbatim quote of source code or of the paper counts as proven text. |
| **DERIVED** | Follows from proven facts by a stated chain of reasoning. The reasoning is written out so a reader can reject it. Nothing here was executed to confirm it. |
| **UNVERIFIED** | Nobody checked. Named explicitly so a future reader does not mistake silence for confirmation. |

**Path conventions.** Archive root (READ-ONLY) =
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025`.
Evidence root (scratchpad) =
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad`,
with the verification artifacts under `…\scratchpad\fixture_spike\`.
Paper extracts: `…\scratchpad\main_paper.txt` (main paper, July 2026, 35 pp) and
`…\scratchpad\ia.txt` (Internet Appendix, May 2026, 15 pp). All line numbers are 1-indexed
file lines of the named file. Prereg repo =
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`, locked at signed tag `prereg-v30`
(registration commit `fe0d5a57`; HEAD `0ee26c4`).

**Numbers.** Where a figure quoted in the source item disagreed with a value re-measured while
writing this register, the register prints the re-measured value and says so under the entry's
"Correction made while writing this register" note. Two such corrections exist (Entries 7 and
8); one path correction exists (Entry 1, `phase7_l2_sim.py` location).

---

## 2. Artifact-path existence check (performed 2026-08-12, before citation)

Every evidence path cited below was checked for existence at write time.

**All cited `scratchpad\fixture_spike\` artifacts EXIST.** Verified present:
`c1\md5_match_capture.txt`, `c1\rowcount_338159_capture.txt`, `c1\tagger_survey_capture.txt`,
`c1\tagger_logic_compare.txt`, `c1\tagger_divergence_diff.txt`,
`c1\rowcount_addendum_v4gapfill.py`, `c2\aggregation_comparison.md`, `c5\env_records.md`,
`c6\a4_defect_audit.md`, `c6\era_attribution.md`, `t1\t1_final_output.txt`,
`t1\violation_table.csv`, `t1\t1_measure.py`, `t3\day_edge_table.csv`,
`t3\day_edge_samples.csv`, `t3\measure_day_edge.py`, `v3\g2_dtype_witness.md`,
`v3\schema_witness.py`, `v4c\one_cell_recompute.md`, `v4c\one_cell_recompute.py`,
`v5e\v4_day_edge.md`, `v6\a12_audit.md`, `R2_consolidated_report.md`,
`m5\per_instrument_counts.csv`, `m5\corrected_decisionT_summary.csv`,
`v7\v4_same_second_channel.md`.

**All cited archive artifacts EXIST**, with one path correction:

- **CORRECTION (path):** `phase7_l2_sim.py` does **not** exist at `scripts\phase7\phase7_l2_sim.py`.
  It exists at exactly one location in the archive:
  `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py`
  (this is the path `c2\aggregation_comparison.md` records, and it is correct; the shorthand
  "scripts\phase7\…" used in some session prose is wrong).

**Mirror-copy note.** A committed copy of the evidence lives at
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\evidence\fixture_spike\`. At write
time that copy contains `R2_consolidated_report.md`, `c1`–`c6`, `d1`, `f1`–`f5`, `m3`–`m5`,
`t1`, `t3`, `t4`, `v1`–`v6`. It does **not** contain `v7`, `n1`, `n2`, `n3` — those exist only
in the scratchpad. A future reader who finds only the committed copy will be missing the
Entry 10 (V7) evidence and the N-series lattice-provenance evidence.

---

# ENTRIES

---

## Entry 1 — `net_delta` corrupted in the Phase 5 / Phase 7 era (classifier + uint32 wrap)

**Status:** `DEFERRED-PER-R10`
**ERA:** Phase 5 / Phase 7

### Published claim touched

`main_paper.txt:488-489` (§4.4, Mechanism 1 magnitude), verbatim:

> "Correction: BFree feature set removing all price-lagged returns. Magnitude: Full AUC on
> ZC = 0.957 vs. BFree = 0.675 (28 pp inflation)."

and `main_paper.txt:368` (§ feature-set description), verbatim:

> "BFree gap on ZC is 28.2 percentage points (Full AUC 0.957, BFree AUC 0.675), confirming that the"

Neither sentence *names* `net_delta`. What this entry records is that the feature matrix behind
both AUCs contained a `net_delta_*` family computed from wrapped unsigned arithmetic and a
`buy_volume` that was identically zero — i.e. the Phase 5 "Full" and "BFree" sets both carried
degenerate trade-flow features. (`net_delta_1s…60s` and `buy_volume_10s`/`sell_volume_10s` are
in the Phase 5 feature list; both Full and BFree contain the trade block.)

### The two defects, verbatim

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py:231-233`:

```python
is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \
         else trades["side"].isin(["B","Buy","buy"])
trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])
```

The parquet's `aggressor_side` values are `BUY_AGGRESSOR` / `SELL_AGGRESSOR` / `UNKNOWN`
(written by `scripts\pipeline\process_zc.py:92-100` and its siblings), so
`.isin(["B","Buy","buy"])` matches nothing — `is_buy` is all-False. `-trades["size"]` then
negates an unsigned `size` column with no cast.

`results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py:207` and `:209` carry the identical
two lines (byte-identical at line 209; whitespace-only difference at 207).

### EVIDENCE CHAIN

| Link | Where | What it establishes |
|---|---|---|
| Writer survey | `fixture_spike\c1\tagger_survey_capture.txt` (460 `*.py` scanned, 119 files with mentions, 472 mention lines, 152 writer lines); `fixture_spike\c1\tagger_logic_compare.txt` (per-writer verbatim blocks + md5) | Every aggressor-tagging writer that ever existed in the archive emits `BUY_AGGRESSOR`/`SELL_AGGRESSOR`/`UNKNOWN` plus a boolean `is_buy_aggressor`; e.g. `scripts\pipeline\process_zc.py:92-95`, `scripts\pipeline\process_mbo.py:549-552`, `scripts\pipeline\process_gc.py:454-457`, `scripts\pipeline\process_gapfill.py:88-91`. No writer ever wrote `"B"` into `aggressor_side`. |
| Byte identity | `fixture_spike\c1\md5_match_capture.txt` | `pc2_transfer\transfer\checksums.txt` line 49 / line 61 MD5s (`ea2eee61…` snapshots, `a2ccce4d…` trades) recomputed today against `processed\zc\zc_snapshots_2025-01.parquet` and `processed\zc\zc_trades_tagged_2025-01.parquet`: **BOTH MATCH**. Manifest mtime 2026-04-07, inside the Phase 5 run window; parquet mtimes 2026-04-02. |
| Run-log fingerprint | `fixture_spike\c1\rowcount_338159_capture.txt` | The original ZC run log records 338,159 feature rows for 2025-01; re-deriving the hour filter `(hour_utc >= 14) & (hour_utc < 19)` from `processed\zc\zc_snapshots_2025-01.parquet` (1,262,191 rows) today yields **exactly 338,159**. Addendum: the later `v4_gapfill` build of the same month yields 378,000 under the same predicate — i.e. the count identifies the pre-gapfill generation uniquely. |
| Environment pin | `fixture_spike\c5\env_records.md` | pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1 / Python 3.12.10, PC1 node "VENGEANCE", continuous over 2026-04-05..08. Two corroborating 2026-04-17 records (`PC2_TRANSFER_v4\PC2_SETUP_README.txt` lines 42-59, git-committed in `2e75345`; `PC2_TRANSFER_v4\pilot\pilot_results_pc1.json` machine-generated env block) plus the dist-info creation dates of the very interpreter directory the archived launcher names. The conflicting `pc2_transfer\transfer\requirements.txt` (pandas 2.1.4 / numpy 1.26.4) is a prescription for a second computer, present on no interpreter on this machine. |
| Stored dtype | `fixture_spike\c5\env_records.md` §1.8 | `processed\zc\zc_trades_tagged_2025-01.parquet` `size`: parquet physical INT32, logical `Int(bitWidth=32, isSigned=false)`, arrow `uint32`; `num_rows = 397,457`. Read from file metadata only. |
| Execution witness | `fixture_spike\t1\t1_final_output.txt`, `t1\t1_measure.py`, `t1\violation_table.csv` | The f2 rebuild, run under the *pinned* versions, produced `{'trades_all': 397457, 'trades_buy': 0, 'trades_sell': 397457, …}` — **buy count exactly zero over 397,457 trades** — and `net_delta` values in the 2^32 range. |
| Phase 7 static | `fixture_spike\c2\aggregation_comparison.md` | 13-row construct-by-construct comparison of `phase7_l2_sim.py` vs `phase5_ml.py`; constructs 1–4 and 7–13 SAME; the only differences are `dollar_volume` (Phase 7 only) and `trade_count_10s` → `trade_*_1s`. SHA256s recorded for both files. |

### PROVEN

- The classifier line and the negation line, verbatim, in both `phase5_ml.py` (231-233) and
  `phase7_l2_sim.py` (207/209). *(source bytes read)*
- No archive writer ever produced the string `"B"` in `aggressor_side`. *(460-file survey, c1)*
- The ZC 2025-01 parquets the rebuild read are byte-identical (MD5) to the files hashed on
  2026-04-07, inside the run window. *(c1)*
- `size` is stored `uint32` in those parquets. *(c5 §1.8, metadata read)*
- Under pandas 3.0.1 / numpy 2.4.2, that code path yields `buy_count == 0` and wrapped
  `net_delta`. *(t1, execution)*
- The pinned versions were the installed versions on PC1 continuously across the run window.
  *(c5 §2, dist-info metadata)*

### DERIVED

- **C1 verdict INHERITED:** the buy-classifier defect was active in the *original* Phase 5 runs.
  Reasoning: the code is byte-verified; the only inputs it could have read are the parquets whose
  bytes are pinned by the run-window manifest; the row-count fingerprint identifies that exact
  generation; and no tagging implementation that ever existed could have made `.isin(["B","Buy","buy"])`
  match. Three independent chains, no conflicts. *(R2_consolidated_report.md §C1)*
- **C5 verdict WRAPPED:** the original runs wrapped mod 2^32 at the negation site. Reasoning:
  same bytes + same code + same library versions ⇒ same dtype outcome, and the f2 rebuild is an
  execution witness under exactly those versions. *(c5 §3 Part 2)*
- Phase 7 inherits both defects at the code level, since its two lines are the same lines.
  *(c2; static only)*

### UNVERIFIED

- Whether `C:\MBO_data\zc\` (the drive the Phase 5 launcher preferred, now gone) held
  byte-identical copies during the runs. The manifest covers the transfer *staging* copy.
  *(c5 blockers)*
- PATH contents on 2026-04-05..08 for the bare-`python` `phase5_fixed` launcher. (Recorded as
  outcome-invariant — both interpreters on the machine carry pandas 3.x / numpy 2.4.2 — but not
  directly recorded.)
- Whether `phase7_l2_sim.py` ever executed on PC2 with different inputs: PC2 runtime is
  unconfirmable from the archive. *(c2 blockers)*
- The actual `aggressor_side` value distribution was verified for **ZC 2025-01 only**. Other
  instruments/months rest on the writer survey, not on data reads. *(c2 blockers)*
- The magnitude and direction of the AUC error caused by these defects. Nobody re-ran Phase 5
  with corrected features.

---

## Entry 2 — `net_delta` still corrupted in the v4 era (dtype CARRIED, classifier CORRECTED)

**Status:** `DEFERRED-PER-R10`
**ERA:** v4 (and, by byte-identical reuse, v5)

### Published claims touched

Headline AUC inputs — `main_paper.txt:59-61`, verbatim:

> "The magnitude of predictability varies by a factor of 40 across cells. The strongest cells (corn
> futures overnight, AUC = 0.873) exhibit edge-over-chance of +0.361, while the weakest (NQ Nasdaq
> futures across all sessions) hover at +0.010-0.020, barely above the noise floor."

IA.1 row — `ia.txt:29`, verbatim:

> "zc full_session 0.3545 0.8579 CNN 5 T1 EXPLORATORY"

§9.4 feature-importance narrative — `main_paper.txt:1138-1142`, verbatim:

> "Feature ablation on the 17 T1/T2 cells (582 ablation runs) confirms: the maximum single-feature sig-
> nal contribution is 2.16%, with vwap_distance appearing most frequently in cells' top-5 (15/17 cells)
> but never exceeding ~2%. Signal is distributed across multiple features — principally vwap_distance,
> net_delta_1s, and l1_imbalance — with no single feature dominating. This rules out the possibility
> that the documented predictability is a feature-construction artifact."

The §9.4 sentence is the sharpest exposure: it names `net_delta_1s` as one of the three features
carrying the signal, and the 2.16% maximum is itself a `net_delta_1s` ablation
(`paper\v4\ia_tables\ia_table_4.csv` line 27: `es,europe_overnight,net_delta_1s,0.0732,0.0716,0.0016,2.16`).

### The defect, verbatim

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py:307`:

```python
tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
```

Classifier: **CORRECTED** — `a4_runner.py:218` loads `["ts_event", "price", "size", "is_buy_aggressor"]`
and never references the string `aggressor_side`; `is_buy_aggressor` is a genuine boolean
(`scripts\pipeline\flow_tagger.py:105  trades["is_buy_aggressor"] = trades["side"] == "B"`).
Dtype: **CARRIED** — no cast on `size` anywhere from `DBNStore…to_df()` through
`to_parquet` → `pq.read_table(...).to_pandas()` → line 307.

v5 executes the same function: `v5_lightgbm_runner.py:43` `import a4_runner as r`, `:106`
`feat = r.add_trade_features(feat, trades)`; `v5_wave_runner.py:279` likewise.

### EVIDENCE CHAIN

| Link | Where | What it establishes |
|---|---|---|
| Code audit | `fixture_spike\c6\a4_defect_audit.md` | Full-file audit of `a4_runner.py` (939 lines) + `v5_lightgbm_runner.py` (294 lines). Verdict table: classifier CORRECTED / dtype CARRIED, both generations. Pass-through map: all five `net_delta_*` wrap-affected; `buy_volume_10s`, `sell_volume_10s`, `trade_count_10s`, `large_trade_count_10s`, `vwap_distance` not. All 10 `TRADE_FEATURES` are in **both** Full and BFree sets (`a4_runner.py:115-123`). |
| Dtype witness | `fixture_spike\v3\g2_dtype_witness.md`, `v3\schema_witness.py` | Parquet-schema metadata read of the exact files `a4_runner.data_dir_for` resolves to, for all six g2 instruments (es/nq/cl/gc/zc/zs, month 2025-01): `size` = arrow `uint32` (physical INT32, logical `Int(bitWidth=32, isSigned=false)`), `is_buy_aggressor` = arrow `bool`, in all six. `created_by` = `parquet-cpp-arrow version 23.0.1`. **WITNESSED-uint32, six for six.** |
| Measurement | `fixture_spike\v4c\one_cell_recompute.md`, `v4c\one_cell_recompute.py` | zc `v4_gapfill` 2025-01, one session hour (5,294 trades, 1,412 one-second windows), pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1: executed `signed_size` dtype **uint32**, groupby-sum **uint64**. Raw identity `as_executed == 2^32 * sell_count + true_delta` holds in **1412/1412** windows. Strong form `float32(as_executed) == float32(2^32 * sell_count)` holds in **1076/1412 (76.2%)**; in the 336 violating windows the true delta survives only quantized to a float32 ulp (observed diffs −256, −512, −1024; worst true delta −762 stored as −1024). |
| Era attribution | `fixture_spike\c6\era_attribution.md` Claims 1–2 | Value-exact chain from `a4_runner.py` → `results\designA\a4_master_designA.csv` (line 947 `test_auc_overall = 0.8579033464898526`; line 2156 `= 0.8728528898420927`) → `results\final\a7_three_design_synthesis.csv` (line 4 / line 2, `edge_median = 0.360912`) → `paper\v4\ia_tables\ia_table_1a.csv` (line 4 = the exact IA.1 row). Ablation chain: `scripts\v4\a9_leakage_ablation.py:33` `import a4_runner as r`; `:93-94` `feat = r.build_snapshot_features(...)` / `r.add_trade_features(...)` — the ablation *rebuilds* features with the same code. |

Re-verified while writing this register (independent recount of the archive CSVs):
`results\final\a9_leakage_ablation.csv` = 583 lines / 582 data rows, of which 17 are
`__BASELINE__` rows (582 − 17 = 565 feature-removal runs); `paper\v4\ia_tables\ia_table_4.csv`
= 86 lines / 85 data rows. Both agree with `c6\era_attribution.md`.

### PROVEN

- Line 307 verbatim, and the absence of any `astype` on `size` in the whole chain. *(source read)*
- `size` is `uint32` in the exact parquets `a4_runner` loads, for **all six** g2 instruments.
  *(v3, metadata read)*
- For he/le, `a4_runner.data_dir_for` (line 140) routes to the ORIGINAL-family parquets whose
  `size` uint32 is separately witnessed. *(c6, c5 §1.8)*
- Executed behaviour on real v4 data: identity exact in 1412/1412 windows; float32 strong form
  exact in 76.2%. *(v4c, execution)*
- The published AUCs trace to `a4_runner` output value-exactly to 16 digits. *(c6 Claim 1)*
- The §9.4 ablation rebuilds features with `a4_runner`. *(c6 Claim 2, code read)*
- 582 / 17 / 565 / 85 row counts. *(recounted 2026-08-12)*

### DERIVED

- The stored v4 `net_delta_*` features are, to within ±2 float32 ulp, a pure encoding of
  `2^32 × (sell-trade count)` — a scaled sell-trade counter, not signed volume. Reasoning:
  the raw identity is exact; the float32 cast at `a4_runner.py:655` has a half-ulp rounding
  radius that exceeds the true-delta term in 76.2% of 1s windows and (since `k` grows with the
  window) in a larger fraction at 5s/10s/30s/60s. *(v4c verdict ¶3–4)*
- Every v4 result (Designs A/B/C, all six architectures, all cells) and every v5 LightGBM result
  carries these features, because the trade block is in both Full and BFree.
  *(c6 §4 + `a4_runner.py:115-123`)*
- The §9.4 claim "This rules out the possibility that the documented predictability is a
  feature-construction artifact" is argued from an ablation whose `net_delta_1s` column is the
  corrupted column — so the ablation cannot rule out a construction artifact *in that column*.
  This is the C6b attribution point.

### UNVERIFIED

- The direction and size of the AUC error. `v4c` states plainly that a corrupted feature is still
  a deterministic transform, so the AUCs are well-defined numbers that do not measure what the
  paper says they measure; whether they are inflated or deflated is not established.
- The 76.2% strong-form figure is from **one instrument, one month, one session hour**
  (zc `v4_gapfill` 2025-01, a 1-hour slice). Other instruments/months/horizons unmeasured.
- Whether any *other* v4 feature is affected: `c6` found no other unsigned-wrap site in the
  a4/v5 model-feature path, but that is a static search, not exhaustive execution.
- Whether re-running v4 with a cast changes any T1/T2 tier assignment.

---

## Entry 3 — a12 academic-signal complex: the numbers themselves are computed through wrapped arithmetic

**Status:** `DEFERRED-PER-R10`
**ERA:** v4 (`scripts\v4\a12_academic_signals.py`)

### ⚠ What distinguishes this entry from Entries 1–2

In Entries 1–2 the defect corrupts a *feature* that a model then consumes; the published AUC is
still a well-defined number and the erratum is about what it measures. **Here the published
NUMBERS themselves — the capture ratio, the Spearman correlation, the gap values, the VPIN
column — are computed through wrapped arithmetic.** The four-feature logistic regression's
`flow_5s` input and its `vpin` input are both wrap-carriers, so the reported quantities are
functions of wrapped values, not merely interpretations of them.

### Published claims touched

`main_paper.txt:24` (abstract), verbatim:

> "maker costs. Simple academic signals capture a median 89.5% of ML edge, confirming that"

`main_paper.txt:1063-1065` (§8.2), verbatim:

> "A logistic regression using only the four signals captures a median 89.5% of ML edge (Spearman ρ
> = +0.97, n = 43 testable cells; three full_session cells excluded due to out-of-memory failures during
> signal computation)."

`main_paper.txt:1066-1071` (Table 9), verbatim:

> "Table 9: Academic Signals vs. ML
> Metric Value
> Spearman (simple vs. ML) +0.97
> Median capture ratio 89.5%
> Cells where simple > 80% 30 / 43
> Cells where simple < 20% 0 / 43"

`main_paper.txt:1221-1222` (conclusion), verbatim:

> "Simple academic signals capture a median 89.5% of the ML edge, indicating that the documented
> predictability reflects known order book mechanics operating at varying intensities across market"

Also §5.9 + Figure 3 (`main_paper.txt:765-812`, including the caption at `:812`
"architecture per cell. Across 43 cells, Spearman ρ = +0.97; median capture ratio 89.5%."),
the page-29 gap table (`main_paper.txt:1078-1081`), the residual sentence at `:1076`, the
intro at `:101-103`, and IA.4's "OFA ∆ / Simple / Capture / Gap" columns for all 43 rows
(`ia.txt:151-203`).

### The two carrier sites, verbatim

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a12_academic_signals.py:187`
(inside `compute_ofa_lagged_signed`, **LIVE**):

```python
tr["signed"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
```

`a12_academic_signals.py:157` (inside `compute_ofa_lagged`) is byte-identical **but DEAD** —
a repo-wide grep finds no caller other than the definition and a docstring cross-reference.

`a12_academic_signals.py:134` (inside `compute_vpin_per_snapshot`, **LIVE**, a second and
previously unflagged carrier of the same family — an unsigned *subtraction*, not a negation,
so a form-match search for `-tr["size"]` would not have found it):

```python
grp["abs_imb"] = (grp["v_buy"] - grp["v_sell"]).abs()
```

with `v_buy`/`v_sell` built at lines 122-123 as `np.where(sign > 0, tr["size"], 0)` /
`np.where(sign < 0, tr["size"], 0)` (uint32 under NEP-50 weak-scalar rules) and summed by
groupby (uint64). `.abs()` on unsigned is a no-op, so any net-sell bucket yields
`abs_imb ≈ 1.8e19` and `vpin_raw` astronomically outside [0,1].

### What flows where

- `flow_5s` (the 5s rolling sum of the line-187 signed flow) → `a12_academic_signals.py:257`
  `feat["flow_5s"] = flow_5s.values`; `:288` `sig_cols = ["ofi_10s", "vpin", "flow_5s", "dar"]`;
  `:305-320` the four-feature LogReg → `simple_lr_test_auc` / `simple_lr_edge` →
  `write_summary()` (`:439-453`) → `results\final\a12_signals_vs_ml.csv`,
  `a12_session_variation.csv`, `a12_summary.txt`.
- `flow_5s` also → `a12_per_bucket_delta_auc.py:44` (import) and `:132-133` → the "OFA" signal
  in the LightGBM augmentation → `ofa_augmented_auc` / `ofa_delta_auc` in
  `results\final\a12_per_bucket_delta_auc.csv`.
- `vpin` is the second of the four LogReg features, so the Simple/Capture/Gap numbers carry
  **both** corrupted features simultaneously.

### NOT exposed (book-only, dtype-safe)

IA.4's `OFI ∆`, `DAR ∆` (identically 0.0000) and `DAR corr` columns; the "DAR ≡ l1_imbalance"
finding (`main_paper.txt:1055-1059`; `ia.txt:152-153`); the OFI `mean |r| = 0.019` claim
(pre-a12 provenance). Reason: OFI (a12 lines 68-99) and DAR (102-108) read snapshot
`bid_size_*`/`ask_size_*` columns, which are built from Python ints in the book engine
(`scripts\pipeline\book_engine.py:48-49`, `:274`, `:372`) → int64, and `.diff()`/`.shift(1)`
promote to float64 before any subtraction.

### EVIDENCE CHAIN

| Link | Where | What it establishes |
|---|---|---|
| Full-file audit | `fixture_spike\v6\a12_audit.md` | `a12_academic_signals.py` (553 lines) read in full, plus `a12_per_bucket_delta_auc.py`. Verdict table: classifier ABSENT (working boolean carried); uncast unsigned negation CARRIED (157 dead / 187 live); new same-family carrier CARRIED at 134. Complete `astype` inventory of the file confirms nothing casts `size`. |
| Dtype premise | `fixture_spike\v3\g2_dtype_witness.md` | Same six-instrument uint32 witness as Entry 2 — a12 loads via `r.load_trades` (`a12_academic_signals.py:412` → `a4_runner.py:218`), so the input files are the same witnessed parquets. |
| Numeric tie-out | `fixture_spike\v6\a12_audit.md` §(c) | Recomputation against `results\final\a12_signals_vs_ml.csv` (43 rows): Spearman = 0.9710, median ratio = 0.8955, mean 0.8242, 30/43 above 0.8, 0/43 below 0.2 — Table 9 row-for-row. Anchoring commits `bc1fee0` (A12 replication) and `cb9eedf` (per-bucket delta-AUC). |

Re-verified while writing this register, from `results\final\a12_signals_vs_ml.csv` (43 rows):
Spearman(`simple_lr_edge`, `ml_edge`) = **0.9710**; median `ratio_simple_over_ml` =
**0.8955072550668124**; mean = **0.8242**; count > 0.8 = **30**; count < 0.2 = **0**. Agrees exactly.

### PROVEN

- Lines 134, 157, 187 verbatim, and the fact that 157 has no callers. *(source read + grep)*
- `size` is uint32 in the parquets a12 loads. *(v3, metadata read)*
- The published Table 9 values are reproduced exactly from the archived CSV. *(v6 §(c); re-verified 2026-08-12)*
- The wiring `flow_5s` → `sig_cols` → LogReg → `simple_lr_edge` → published columns.
  *(source read, line-cited)*
- OFI/DAR read int64 snapshot columns. *(book_engine.py source read)*

### DERIVED

- Line 187 wraps at runtime for every sell-aggressor (and UNKNOWN) trade. Reasoning: identical
  construction to `a4_runner.py:307`, identical input dtype, identical environment — and that
  construction was measured to wrap in `v4c`.
- Line 134 fires under exactly the same dtype condition: if 187 is live, 134 is live. Reasoning
  spelled out in `v6` §(new same-family site) — `np.where(cond, uint32, 0)` stays uint32,
  groupby-sum promotes to uint64, unsigned subtraction wraps for net-sell buckets, `.abs()`
  is a no-op on unsigned.
- The 89.5%-capture complex, the ES/CL overnight gap numbers, the Figure-3 bars, and IA.4's
  OFA ∆ / VPIN ∆ / Simple / Capture / Gap columns are all functions of at least one wrapped
  quantity.
- An observation consistent with (but not proof of) the wrap firing: in
  `results\final\a12_academic_signals.csv` the `ofa_*` values are near-constant across buckets
  within each instrument (nq `ofa_5s` ≈ 0.4934 ± 0.0002; es ≈ 0.487; gc ≈ 0.2245; cl ≈ 0.1965;
  zc ≈ 0.0940; zs ≈ 0.1172; he ≈ 0.1240; le ≈ 0.1434). `v6` gives **two** compatible
  explanations and does not adjudicate between them: (i) the `[t_min, t_max]` restriction at
  lines 189-192 plus the reindex at 196-197 makes every bucket's "OFA" a near-identical
  full-period series — a design quirk independent of dtype; (ii) wrapped flow ≈
  2^32 × per-second sell count, whose autocorrelation measures trade-arrival clustering.

### UNVERIFIED

- **No execution witness exists for a12 specifically.** `v6` is a static audit; the wrap
  inference transfers from `v4c`'s measurement of the *structurally identical* a4 site. Nobody
  ran a12's own code path.
- The magnitude of the corrupted `vpin` values (predicted astronomically out of range) has not
  been read out of any archived intermediate.
- Which of the two explanations for the near-constant `ofa_*` values is operative.
- Whether a corrected recomputation would move the 89.5% median in either direction.
- The raw `ofa_1s/5s/10s/30s` autocorrelations appear in no paper or IA table (verified by
  search) — so the register does **not** claim a published OFA-autocorrelation erratum.

---

## Entry 4 — VPIN null contradicts the archived data (no defect required)

**Status:** `DEFERRED-PER-R10`
**ERA:** v4 (a12) — but this entry is an internal inconsistency, independent of any defect

### Published claim

`main_paper.txt:1096-1097` (§8.3), verbatim:

> "VPIN produces a complete null across all instruments, sessions, and horizons (max | ∆AUC| <
> 0.003), consistent with Andersen and Bondarenko's (2014) critique."

IA.4's "VPIN ∆" column (`ia.txt:151-203`) carries the 43 underlying values.

### The contradiction

Measured directly from `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\final\a12_per_bucket_delta_auc.csv`
(43 rows; columns `inst, bucket, n_train, n_test, baseline_auc, ofi_augmented_auc,
ofi_delta_auc, vpin_augmented_auc, vpin_delta_auc, ofa_augmented_auc, ofa_delta_auc,
dar_augmented_auc, dar_delta_auc, elapsed_seconds`):

| Rank | Cell | `vpin_delta_auc` | \|value\| |
|---|---|---|---|
| 1 | le / open | **−0.004571** | 0.004571 |
| 2 | cl / open | **+0.003191** | 0.003191 |
| 3 | he / afternoon | −0.002409 | 0.002409 |

**Two of 43 cells exceed the published bound of 0.003.** The maximum is 0.0046 (rounded),
which is 1.5× the printed bound. The archive's own commit message `cb9eedf` states
"max 0.0046" — so the correct number was known at commit time.

This entry requires **no** defect to be true: it is a plain disagreement between a printed
bound and the archived data the bound describes. (The VPIN *values* are separately implicated
by Entry 3's line-134 finding; that is a different, additive problem.)

### EVIDENCE CHAIN

- `fixture_spike\v6\a12_audit.md` §(c), "Published numbers that pass through the SECOND carried
  site" — records the contradiction and the commit-message corroboration.
- Archived CSV: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\final\a12_per_bucket_delta_auc.csv`
  (**verified to exist**; 43 data rows).
- Archive commit `cb9eedf` "A12 per-bucket delta-AUC: 43 cells x 4 signals", whose message
  states VPIN "median −0.0005 max 0.0046".
- Paper source: `main_paper.txt:1096-1097`.

### PROVEN

- The paper sentence, verbatim, with its `< 0.003` bound. *(text read)*
- `max |vpin_delta_auc| = 0.004571` at le/open, and `+0.003191` at cl/open, in the archived
  43-row CSV. *(measured 2026-08-12, and previously in v6)*
- The commit message itself says max 0.0046.

### DERIVED

- The printed bound is false as stated against its own source data. (Trivial derivation:
  0.004571 > 0.003.)
- The qualitative conclusion "VPIN produces a complete null" is not necessarily disturbed —
  0.0046 is still a very small ∆AUC — so the erratum is about the *bound*, not obviously about
  the *finding*. This is a judgement the author should make, not this register.

### UNVERIFIED

- Whether the paper's "< 0.003" was a transcription slip, a rounding convention applied to a
  different subset, or a stale number from an earlier run. Nothing in the archive resolves this.
- Whether the IA.4 "VPIN ∆" column as typeset matches the CSV row-for-row (spot-checked only:
  le/open −0.0046 = −0.004571 confirmed in `v6`).

---

## Entry 5 — Day-edge labels: v4 SHARED, v5 PARTITIONED

**Status:** `DEFERRED-PER-R10`
**ERA:** v4 (erratum attaches to v4-era outputs only; v5 is clean on this mechanism)

### Published claim touched

There is no paper sentence that states the label-partitioning policy for the v4 runs, so this
entry attaches to the v4-era numbers themselves — the headline AUCs and IA.1 table quoted in
Entry 2 (`main_paper.txt:59-61`; `ia.txt:29`) — and to the general causal-lag description at
`main_paper.txt:371-372`, verbatim:

> "All features are subject to a mandatory causal lag: features at time t use information available
> only through t −1 (implemented as shift(1)). The prediction target is binary mid-price direction at"

That sentence describes the *feature* lag, not the label horizon. **Label partitioning is
described nowhere in the extracted paper text.** Flagged as such rather than inferred: the
erratum candidate here is that v4 labels silently span closed-market gaps, and the paper does
not say either way.

### The finding

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py:350-356`, verbatim:

```python
def build_target(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """y = 1 if mid[t+h] > mid[t], 0 if <, drop ties."""
    mid = df["mid_price"]
    fut = mid.shift(-horizon)
    df["y"] = np.where(fut > mid, 1, np.where(fut < mid, 0, -1))
    df["prev_return"] = (mid - mid.shift(horizon))  # for naive baseline
    return df
```

`fut = mid.shift(-horizon)` is a **positional** shift by row count over a whole-year concat
(`a4_runner.py:205`), bucket-filtered and `reset_index(drop=True)`-ed
(`a4_runner.py:236-238`). After that reset, the last row of day N's bucket window is
positionally adjacent to the first row of day N+1's window. The only `shift(` occurrences in
the file are lines 346 (causal lag), 353, 355; the only `groupby` is `tr.groupby("second")` at
line 311 (trade aggregation). **No session or day partition exists anywhere in the file.**

Day-edge rows are **not** dropped: `a4_runner.py:646-648` keeps rows with `y in {0,1}`, and a
session-tail row's `fut` is the *next session's real mid*, so it gets a valid label and survives.

v5 does **not** share this: `v5_lightgbm_runner.py` builds no labels; it loads
`v5\labels\{inst}_h{h}.parquet` (`:76-80`) produced by `v5_label_generator.py`, which uses a
time-based `pd.merge_asof(..., direction="forward", tolerance=tol)` (`:248-255`, tolerance
`min(int(h*0.05), 10)` s at `:129-130`) plus an explicit `session_cross` exclusion
(`:297-302`), with excluded rows set to `label = NaN` (`:322`) and filtered out by the runner.
Documented exception: `--next-trading-day-mode` (amendment 001) deliberately skips the
session-cross exclusion (`v5_label_generator.py:295-296`) — a declared cross-session target,
not a silent defect.

### Measured magnitude (Phase 5 lattice, ZC 2025-01 — see caveat)

From `fixture_spike\t3\day_edge_table.csv` (338,159 rows, ZC 2025-01):

| horizon (s) | cross-boundary label pairs | all real-valued? | worst wall-clock span | same-day pairs > 60 s | worst same-day span | cross-boundary rows passing ≥2-tick filter | pass frac (cross) | pass frac (overall) |
|---|---|---|---|---|---|---|---|---|
| 5 | 100 | 100 real / 0 NaN | 3 d 19:30:05 | 34 | 0:20:03.47 | 83 | 0.83 | 0.000 |
| 10 | 200 | 200 / 0 | 3 d 19:30:10 | 61 | 0:23:44.42 | 166 | 0.83 | 0.001 |
| 30 | 600 | 600 / 0 | 3 d 19:30:30 | 158 | 0:25:12.26 | 494 | 0.823 | 0.004 |
| 60 | 1200 | 1200 / 0 | 3 d 19:31:00 | 255 | 0:30:45.37 | 974 | 0.812 | 0.010 |

The last two columns are the sharp part: under a ≥2-tick magnitude filter, **81–83% of
cross-boundary rows survive versus 0–1% of the overall population** — the filter *enriches*
for exactly the contaminated rows.

### EVIDENCE CHAIN

- `fixture_spike\v5e\v4_day_edge.md` — static verdict SHARED (v4) / PARTITIONED (v5), all
  quotes line-cited; covers `a4_runner.py` (full label path), `bucket_assigner.py` (381 lines),
  `v5_lightgbm_runner.py` (1-135), `v5_label_generator.py` (1-339).
- `fixture_spike\t3\day_edge_table.csv`, `t3\day_edge_samples.csv`, `t3\measure_day_edge.py` —
  the measurement above (Phase 5 ZC 2025-01 lattice).
- Bucket-window sizes that set the gap magnitude: `bucket_assigner.py:64-92` (7-bucket
  es/nq/cl/gc; 5-bucket grains zc/zs; 4-bucket livestock he/le), e.g. full_session for grains
  = 20:00 → 14:20 NY (line 90).

### PROVEN

- `build_target` is an unpartitioned positional shift; no groupby/session partition exists in
  `a4_runner.py`. *(source read + grep)*
- Day-edge rows survive the `y ∈ {0,1}` filter. *(source read)*
- `v5_label_generator.py` is time-based and session-guarded. *(source read)*
- The t3 magnitude table above, on the Phase 5 ZC 2025-01 lattice. *(execution)*
- The ≥2-tick magnitude filter enriches cross-boundary rows 81–83% vs 0–1%. *(execution)*

### DERIVED

- Every v4 result — Designs A/B/C, all cells, all horizons, all architectures — carries
  session-tail labels spanning closed-market gaps, in train, val and test alike. Reasoning: the
  label path is identical for all three designs (`configure_design` and `design_a_day_sets`
  change only day membership, `v5e` §2), and nothing downstream removes the rows.
- Bound on contamination: at most `horizon` rows per contiguous window boundary, at every
  trading-day boundary of every cell. *(v5e §1.4, static)*
- For a single-bucket cell (e.g. zc/morning 10:30–12:30 NY) the "future" mid is ~22 h away;
  for full_session cells it is across the maintenance break and weekends.

### UNVERIFIED

- **The t3 measurement was made on the Phase 5 ZC 2025-01 lattice, not on a v4 `v4_gapfill`
  lattice.** The v4 lattice is a different, larger build (378,000 rows in [14,19) for the same
  month vs 338,159 — `c1\rowcount_338159_capture.txt` addendum). The v4-era cross-boundary
  counts have **not** been measured. The static verdict (SHARED) does not depend on this; the
  numbers do.
- Per-instrument v4 day-edge counts for the other seven instruments: unmeasured.
- Whether removing day-edge rows changes any published AUC: unmeasured.
- Whether the paper intends any label-partitioning claim at all: the extracted text says nothing.

---

## Entry 6 — NQ "+0.10 → +0.018" pairs NQ's pre-fix maximum with HE's post-fix maximum

**Status:** `DEFERRED-PER-R10`
**ERA:** Phase 6

### Published claim

`main_paper.txt:494-495` (§4.4, Mechanism 2), verbatim:

> "The single-instrument maximum (NQ) shows pre-fix gain of +0.10 declining to +0.018 post-fix, a
> 5.6-fold reduction."

### The finding, re-measured 2026-08-12

**Pre-fix, NQ** — `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase6\second_pc\phase6_main_summary.csv`
(the PC2 file; instrument column contains exactly GC, NQ, ZC, ZS). NQ L3
`marginal_gain_over_prev_tier` values: **0.1038** and **0.1051** (both 5 s), 0.0644, 0.0639 (10 s),
0.0262, 0.0238 (30 s), 0.0058, 0.0098 (60 s). NQ pre-fix maximum = **+0.1051**; the paper's
"+0.10" is consistent with this.

**Post-fix, NQ** — `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` (64 data rows,
every row `l3_fix_applied = shift_1s`). NQ values, sorted descending:
**+0.0002, +0.0002, −0.0001, −0.0004, −0.0008, −0.0010, −0.0011, −0.0032**.
**NQ's post-fix maximum is +0.0002.** Nothing near 0.018 exists in NQ's rows.

**Where +0.018 does exist** — the same file's HE rows: **+0.0182** (LightGBM 5 s) and **+0.0181**
(XGBoost 5 s). The published "+0.018 post-fix" matches **HE's** post-fix maximum, not NQ's.

If the sentence's own ratio is recomputed from NQ's actual numbers, "5.6-fold" is not
recoverable: 0.1051 / 0.0002 ≈ 525.

### Producing code is ABSENT

No Phase 6 script exists anywhere in the archive. A repo-wide grep of `*.py` for
`marginal_gain_over_prev_tier`, `flag_triggered`, `l3_fix_applied`, and `phase6_main_summary`
returns **zero hits**; `find -iname "*phase6*"` returns only result CSVs/JSONs (mirrored in four
locations: `results\phase6\`, `results\phase6\pc2\`, `results\pc2_all_phases\phase6\`,
`pc2_transfer\results\phase6\`) and no code. Phase 6 predates version control — the archive
repo's first commit is `9c37285` (2026-04-15). The completion stamp
`results\phase6\overnight_complete.txt` reads "Timestamp: 2026-04-10T03:39:56.459212".

### Collision note (fact, not inference)

The string "+0.018" also appears at `main_paper.txt:614`, `:735`, `:800`, and `:947`, where it
denotes the **v4-era** edge of nq/asia_overnight (`ia.txt:63`: "nq asia_overnight 0.0176 0.5235
XGBoost 5 T4 EXPLORATORY"). Same printed value, different era, different quantity. A reader
reopening this entry should not conflate them.

### EVIDENCE CHAIN

- `fixture_spike\c6\era_attribution.md` Claim 3 — era attribution DECIDED = Phase 6; producing
  script UNDECIDABLE (absent); the HE-vs-NQ mismatch stated with file lines.
- `results\phase6\second_pc\phase6_main_summary.csv` (**verified to exist**) — pre-fix NQ.
- `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` (**verified to exist**) —
  post-fix, 64 rows.
- `results\phase6\overnight_complete.txt` (**verified to exist**) — the 2026-04-10 stamp.
- `main_paper.txt:494-495`; `ia.txt:63`.

### PROVEN

- The paper sentence, verbatim. *(text read)*
- NQ pre-fix L3 gains, all eight values. *(re-measured 2026-08-12)*
- NQ post-fix L3 gains, all eight values; maximum +0.0002. *(re-measured 2026-08-12)*
- HE post-fix maximum +0.0182 / +0.0181. *(re-measured 2026-08-12)*
- The PC2 summary file contains exactly GC/NQ/ZC/ZS; the main-PC file exactly ES/CL/HE/LE.
  *(re-measured 2026-08-12)*
- No Phase 6 producing script exists in the archive. *(grep + find, c6)*

### DERIVED

- The published "+0.018 post-fix" is HE's number attached to NQ's label. Reasoning: it matches
  HE's maximum to the printed precision and matches no NQ value at any horizon or model.
- The "5.6-fold reduction" is therefore a ratio across two different instruments.
- Because the runner is absent, the *line-level* presence of the Entry 1 defects in Phase 6 code
  cannot be decided from the archive — only that Phase 6 sits inside the era whose surrounding
  code is defect-confirmed.

### UNVERIFIED

- Whether this was a transcription error or a deliberate-but-unmarked substitution. The archive
  does not decide it, and this register does not guess.
- Whether a third variant exists: session notes mention a `universal_lag_finding.txt` carrying
  "+0.05" for a related quantity. **That file was not re-read while writing this register** —
  treat the "+0.05" variant as an unchecked lead, not a finding.
- Whether the Phase 6 pre-fix numbers themselves are defect-affected (undecidable, code absent).

---

## Entry 7 — "23-fold": a 4-instrument numerator published as "across all 8"

**Status:** `DEFERRED-PER-R10`
**ERA:** Phase 6

### Published claim

`main_paper.txt:491-493` (§4.4, Mechanism 2), verbatim:

> "puted at time t include the current second. Without shift(1), features at time t contain same-second
> information. Correction: shift(1) on all rolling features. Magnitude: mean L3 gain pre-fix = +0.035
> AUC, post-fix = +0.0015 AUC — a 23-fold reduction (mean-to-mean across all 8 instruments)."

(Line-number note: `c6\era_attribution.md` Claim 4 cites this passage as "`main_paper.txt:492-493`".
Re-checked 2026-08-12 against the extract: the sentence begins on **491** — line 490 is the
"Mechanism 2 (Level 3 MBO contemporaneous leakage): Rolling aggregation windows com-" header
line. A one-line off-by-one in the source item, corrected here.)

Repeated at `main_paper.txt:92-93`, verbatim:

> "nism 1), Level 3 MBO contemporaneous leakage (Mechanism 2, producing 23-fold apparent signal
> inflation), Level 2 market structure reflection (Mechanism 3), and Level 1 trade flow contamination"

and `main_paper.txt:480`, verbatim:

> "feature construction code, but the 23-fold mean inflation from Mechanism 2 alone suggests that any"

### The finding, re-measured 2026-08-12

| Quantity | Source | Value |
|---|---|---|
| Main-PC L3 pre-fix mean (ES, CL, HE, LE only; n = 32) | `results\phase6\phase6_main_summary.csv` | **0.034575** |
| Corroborating stamp | `results\phase6\overnight_complete.txt` | "Mean L3 gain: 0.0346 (n=32)" — main PC, 96/96 runs, 2026-04-10 |
| PC2 L3 pre-fix mean (GC, NQ, ZC, ZS; n = 32) | `results\phase6\second_pc\phase6_main_summary.csv` | **0.02144375** |
| **True 8-instrument pre-fix mean (n = 64)** | both files combined | **0.028009375** |
| Post-fix mean (n = 64) | `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` | **0.0015375** |

The published "+0.035 pre-fix" is the **4-instrument main-PC mean** (0.0346 → 0.035), not the
8-instrument mean. The parenthetical "across all 8 instruments" does not describe the numerator.

**Ratios:**

| Numerator | Denominator | Ratio |
|---|---|---|
| 0.0346 (rounded, 4-inst) | 0.0015 (rounded) | **23.07** ← the published "23-fold" |
| 0.034575 (exact, 4-inst) | 0.0015375 (exact) | **22.49** |
| 0.0280 (rounded, 8-inst) | 0.0015 (rounded) | **18.67** |
| **0.028009375 (exact, 8-inst)** | **0.0015375 (exact)** | **18.22** |

### ⚠ Correction made while writing this register

The task brief for this entry said the 8-instrument correction gives "~19x". **At full
precision it is 18.2×**; 18.7× only if one keeps the paper's own rounded inputs. Both are
recorded above so the author can choose the presentation. The published 23-fold is itself
partly a rounding artifact — even with the 4-instrument numerator, the exact ratio is 22.5×,
not 23×.

### EVIDENCE CHAIN

- `fixture_spike\c6\era_attribution.md` Claim 4 — era DECIDED = Phase 6 for both numerator and
  denominator; the 4-vs-8 scope mismatch recorded.
- `results\phase6\phase6_main_summary.csv` (**verified to exist**; 96 rows, 32 of them L3;
  instruments ES/CL/HE/LE only).
- `results\phase6\second_pc\phase6_main_summary.csv` (**verified to exist**; instruments
  GC/NQ/ZC/ZS).
- `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` (**verified to exist**; 64 data
  rows, all `l3_fix_applied = shift_1s`).
- `results\phase6\overnight_complete.txt` (**verified to exist**).
- `main_paper.txt:92`, `:480`, `:492-493`.

### PROVEN

- The paper sentences, verbatim. *(text read)*
- All five measured means and the four ratios in the tables above. *(re-measured 2026-08-12)*
- The main-PC file contains no NQ/GC/ZC/ZS rows; the PC2 file contains no ES/CL/HE/LE rows.
  *(re-measured 2026-08-12)*
- The `overnight_complete.txt` stamp says n=32 for the 0.0346 mean — i.e. the archive's own
  record states the numerator's sample size, and 32 ≠ 64.

### DERIVED

- The scope phrase "across all 8 instruments" is false of the numerator. (Direct: the numerator
  file has four instruments.)
- The denominator *is* an 8-instrument mean (64 rows). So the published ratio mixes a
  4-instrument numerator with an 8-instrument denominator.
- A consistent 8-vs-8 restatement is 18.2× (exact) / 18.7× (rounded inputs).

### UNVERIFIED

- Whether the paper intended "all 8" to modify only the denominator or the whole comparison.
- Whether the L2 mean (`overnight_complete.txt`: "Mean L2 gain: 0.0354 (n=32)") is quoted
  anywhere in the paper with the same scope problem. **Not checked.**
- The producing script is absent (same as Entry 6), so nothing about how the means were
  originally computed can be re-derived from code.

---

## Entry 8 — Full-side splice ambiguity behind the published 0.957

**Status:** `DEFERRED-PER-R10`
**ERA:** Phase 5 (cross-generation within Phase 5)

### Published claim

`main_paper.txt:488-489`, verbatim:

> "Correction: BFree feature set removing all price-lagged returns. Magnitude: Full AUC on
> ZC = 0.957 vs. BFree = 0.675 (28 pp inflation)."

and `main_paper.txt:368`, verbatim:

> "BFree gap on ZC is 28.2 percentage points (Full AUC 0.957, BFree AUC 0.675), confirming that the"

### The BFree side is unambiguous; the Full side is not

**BFree 0.675 pins to exactly one artifact.**
`USB_ALL_PHASES\phase5_fixed\master_phase5_384runs.csv` line 322:
`ZC,Transformer,5,BFree,39763.0,46276.0,72118.0,35.0,9.0,0.852169,0.675179,…,gpu_track2`
→ `test_auc = 0.675179`. Also in
`USB_ALL_PHASES\phase5_fixed\gpu_track2\detail\zc_Transformer_5s_BFree_results.json`.
**Verified while writing this register:** the pre-fix master
`results\phase5\phase5_master.csv` contains no ZC BFree test AUC near 0.675 at any horizon
(pre-fix ZC BFree test AUCs from `results\phase5\checkpoint_zc.json`: 5 s — XGBoost 0.7222,
LogReg 0.7901, LSTM 0.784, Transformer 0.7902, CNN null; 10 s — 0.5338 / 0.5423 / 0.5913 /
0.5469 / 0.6098; 30 s — 0.5148 / 0.6028 / 0.5587; 60 s — 0.5961 / 0.701 / 0.615). The single
`0.675` string match in `phase5_master.csv` is at line 155 and is an unrelated LE Transformer
30 s BFree **val**_auc of 0.6755. **So 0.675 is uniquely a `phase5_fixed` value.**

**The Full side has (at least) four candidate anchors, in three different generations:**

| # | Candidate | Exact archived value | Location | Generation |
|---|---|---|---|---|
| A | `zc_XGBoost_5s_Full` | **0.956733** | `USB_ALL_PHASES\phase5_fixed\master_phase5_384runs.csv` line 331; `…\phase5_fixed\cpu_track2\detail\zc_XGBoost_5s_Full_results.json` | `phase5_fixed` — **same generation as the BFree anchor** |
| B | `zc_XGBoost_30s_Full` | **0.9573** | `results\phase5\phase5_master.csv` line 10 (`run_key = zc_XGBoost_30s_Full`, `test_auc = 0.9573`, `val_auc = 0.944`); `results\phase5\checkpoint_zc.json` (`"test_auc": 0.9573`) | **pre-fix** — pairing it with the BFree anchor is a cross-generation splice |
| C | `zc_CNN_5s_Full` **mid-training validation curve** | val_auc **0.957317** (epoch 5) and **0.957585** (epoch 6) | `results\phase5\dl_rerun\detail\zc_CNN_5s_Full_curve.csv` | `dl_rerun`; the corresponding **test** AUC is **0.940778** (`…\zc_CNN_5s_Full_results.json`, `best_val_epoch: 11`, `val_auc: 0.959933`) |
| D | `zc_CNN_5s_Full` **pre-fix** | test 0.963, val 0.9756 | `results\phase5\checkpoint_zc.json` | pre-fix — a *fourth* distinct ZC CNN 5 s Full number, listed so a reader is not surprised by it |

For completeness: the `phase5_fixed` ZC CNN 5 s Full run is a fifth record and is nowhere near
0.957 — `master_phase5_384runs.csv` line 291 gives `val_auc 0.892755`, `test_auc 0.77216`.

**The candidate-C hazard is the sharp one.** Its 0.957-ish values are *validation* AUCs from
epochs 5–6 of a training curve, not a held-out test result. If the paper's "0.957" came from
there, it would be a mid-training validation number published as a test AUC, and the honest
test number for that run is 0.9408.

### ⚠ Correction / confirmation made while writing this register

The task brief said candidate C's test was "0.9408". **Confirmed exactly: 0.940778.** The brief
did not mention candidate D or the divergent `phase5_fixed` CNN run; both are added above.

### What the archive does not resolve

Nothing in the archive states which artifact the paper cites. Candidate A is the only choice
that makes the published pair internally consistent (same 384-run generation as the BFree
anchor); candidates B and C would each make the published "28 pp" gap a splice across
generations or across metric types. **The archive does not decide.**

### EVIDENCE CHAIN

- `fixture_spike\c6\era_attribution.md` Claim 5 — records candidates A and B with file lines
  and the 0.675179 anchor.
- Archive artifacts (all **verified to exist**): `USB_ALL_PHASES\phase5_fixed\master_phase5_384runs.csv`;
  `USB_ALL_PHASES\phase5_fixed\cpu_track2\detail\zc_XGBoost_5s_Full_results.json`;
  `USB_ALL_PHASES\phase5_fixed\gpu_track2\detail\zc_Transformer_5s_BFree_results.json`;
  `results\phase5\phase5_master.csv`; `results\phase5\checkpoint_zc.json`;
  `results\phase5\dl_rerun\detail\zc_CNN_5s_Full_curve.csv`;
  `results\phase5\dl_rerun\detail\zc_CNN_5s_Full_results.json`.
- Environment/machine attribution for all Phase 5 artifacts: `fixture_spike\c5\env_records.md` §1.6.
- `main_paper.txt:368`, `:488-489`.

### PROVEN

- The paper sentences, verbatim. *(text read)*
- All four candidate values and their exact locations, read from the archived files.
  *(re-measured 2026-08-12)*
- 0.675179 exists only in the `phase5_fixed` family; no pre-fix ZC BFree value is near it.
  *(re-measured 2026-08-12)*
- Candidate C's curve values are `val_auc` by column name; its test AUC is 0.940778.
  *(file read)*
- All Phase 5 artifacts (pre-fix and `phase5_fixed`) attribute to PC1 by embedded paths and
  batch sequencing. *(c5 §1.6)*

### DERIVED

- Candidate A is the only internally consistent pairing. Reasoning: it and the BFree anchor come
  from the same 384-run `phase5_fixed` analysis; A and B differ in horizon (5 s vs 30 s) as well
  as generation.
- If the source is B, the published gap splices a pre-fix Full against a post-fix BFree.
- If the source is C, the published Full is a validation number, not a test number.

### UNVERIFIED

- **Which artifact the paper actually cites.** No archive record resolves it. This is the entry's
  whole point; do not let a later reading smooth it over.
- Whether the paper's "28.2 percentage points" was computed from the same pair as the two AUCs
  it prints (0.9573 − 0.675179 = 0.282121; 0.956733 − 0.675179 = 0.281554 — **both round to
  28.2 pp**, so the gap figure does not discriminate between A and B). *Computed here; noted as
  a discriminator that fails.*
- Whether the paper's ±0.010 registered reference interval (raised as Reviewer B finding B3
  against the v30a draft) interacts with this ambiguity. Out of scope for this register.

---

## Entry 9 — §8.4 gradient ratios: DAR values printed under a "Simple LR Ratio" label

**Status:** `DEFERRED-PER-R10`
**ERA:** v4 (a12) — a labelling error, not an arithmetic one

### Published claim

`main_paper.txt:1099-1103` (§8.4), verbatim:

> "Academic signals exhibit the same session and matching-algorithm gradients as ML models, but
> attenuated:
> Gradient Simple LR Ratio ML Ratio
> Overnight / RTH 1.74 × 3.72×
> K-Algorithm / FIFO 4.91 × 8.79×"

followed at `main_paper.txt:1104-1106` by:

> "The simple LR gradient largely reflects depth asymmetry (DAR/l1_imbalance), which is present
> in both the simple and ML feature sets. The attenuation of the simple-vs-ML ratio indicates that
> ML captures non-linear amplifications of the same underlying depth-asymmetry mechanism — the"

### The finding, re-measured 2026-08-12

From `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\final\a12_session_variation.csv`
(columns: `metric, overnight_abs_med, rth_abs_med, k_algo_abs_med, fifo_abs_med, on_over_rth, k_over_f`):

| `metric` row | `on_over_rth` | `k_over_f` |
|---|---|---|
| `dar_predcorr` | **1.743752405308438** → 1.74 | **4.911926058437686** → 4.91 |
| `simple_lr_edge` | **1.8004587454874823** → 1.80 | **8.880814929180373** → 8.88 |
| `ml_edge` | **3.723377789443002** → 3.72 | **8.788251258638674** → 8.79 |

The printed "ML Ratio" column (3.72 / 8.79) matches `ml_edge` exactly. The printed **"Simple LR
Ratio"** column (1.74 / 4.91) matches **`dar_predcorr`**, not `simple_lr_edge`. The true
simple-LR gradients are **1.80×** and **8.88×**.

Archive commit `bc1fee0` attributes 1.74× / 4.9× to DAR explicitly, so the numbers are correct
DAR gradients carrying the wrong column label.

### Why this matters twice over

1. **The label is wrong.** The table's own following sentence says "The simple LR gradient
   largely reflects depth asymmetry (DAR/l1_imbalance)" — which reads as an *interpretation* of
   a simple-LR number but is, given the values, a restatement of what the numbers already are.
2. **The attenuation narrative reverses on the K/FIFO row.** As printed, simple LR (4.91×) is
   strongly attenuated relative to ML (8.79×). With the true simple-LR value (8.88×), simple LR
   slightly **exceeds** ML on that gradient. The Overnight/RTH row keeps its direction
   (1.80× vs 3.72×).
3. **Exposure interacts with Entry 3.** As *printed*, these two numbers are book-only DAR values
   and therefore do **not** pass through the wrapped arithmetic. If the label were taken at face
   value, the correct numbers (`simple_lr_edge`) are flow-fed and **do** pass through it. So
   correcting the label moves these two figures into Entry 3's exposed set.

### EVIDENCE CHAIN

- `fixture_spike\v6\a12_audit.md` §(c), "Published a12 numbers that NEVER touch signed trade
  flow" — records the mislabeling as an incidental finding of the V6 audit.
- `results\final\a12_session_variation.csv` (**verified to exist**; 6 metric rows) — the six
  values above.
- Archive commit `bc1fee0` "A12: Academic signal replication — OFI/VPIN/OFA/DAR per bucket +
  ML comparison".
- `main_paper.txt:1099-1106`.

### PROVEN

- The paper table, verbatim. *(text read)*
- All six CSV values to full printed precision. *(re-measured 2026-08-12)*
- `dar_predcorr` matches the printed "Simple LR Ratio" column; `simple_lr_edge` does not.
  *(re-measured 2026-08-12)*
- `ml_edge` matches the printed "ML Ratio" column. *(re-measured 2026-08-12)*

### DERIVED

- The column label is wrong; the numbers are DAR gradients.
- With the correctly-labelled values, the K/FIFO attenuation claim inverts (8.88 > 8.79).
- Correcting the label changes these two numbers' defect exposure from "not exposed" to
  "exposed" (Entry 3).

### UNVERIFIED

- Whether the author intended to print DAR gradients and mislabelled the column, or intended
  simple-LR gradients and pulled the wrong row. The archive does not say.
- Whether any other §8.x table draws from `a12_session_variation.csv` rows with the same
  row-selection slip. **Only the 8.4 table was checked.**
- Whether `ofi_10s_predcorr` (0.8307 / 1.4538), `vpin_vol_predcorr` (1.3246 / 0.7507) or
  `ofa_5s` (1.1423 / 0.4701) appear anywhere in the paper. **Not checked.**

---

## Entry 10 — v4 same-second residual channel (V7) — **PLACEHOLDER**

**Status:** `PENDING-MEASUREMENT` (register-level status remains `DEFERRED-PER-R10` once the
result lands — the deferral applies to *all* entries, including this one)

**ERA:** v4 (and v5 by code reuse) — to be confirmed by the V7 item

### What this stub is for

The V7 item asks whether the v4/v5 pipeline carries the same-second residual channel that item
M5 measured on the Phase 5/7 lattice — the channel in which two consecutive lattice rows fall in
the same wall-clock second, so a one-**row** `shift(1)` does not move the join window back a
second and the "corrected" row still carries its own second's events.

**This entry is a stub. The orchestrator appends the result when the running V7 item returns.**
No V7 finding is asserted here, and no number from V7 has been folded into any other entry in
this register.

### Why it belongs in the errata register at all (context established before V7 ran)

M5 measured the same-second mechanism on the Phase 5/7 corrected side and found it fires: the
corrected-side zero does **not** extend beyond ZC 2025-01. Corrected/decision-T is nonzero on 5
of 8 instruments in 2025-01 and 7 of 8 in 2025-08, **including ZC itself in 2025-08** (strict
90,868 + equal 2,857 of 554,303 rows). Every violating row satisfies
`floor(T_i) == floor(T_{i−1})`. ZC 2025-01 passed only because that lattice is strictly ≥1 s
spaced (0 same-second rows, versus 211,450 = 38.1% in 2025-08).
Evidence: `fixture_spike\m5\per_instrument_counts.csv`,
`m5\corrected_decisionT_summary.csv`, `m5\verify_violating_rows.json`
(directory **verified to exist**). If the same channel is present in the v4 join, it would touch
the v4-era published numbers of Entry 2.

### Artifacts present at the time this register was frozen

The directory `…\scratchpad\fixture_spike\v7\` **exists** and contains, as of 2026-08-12:
`v4_same_second_channel.md`, `affected_row_buckets.csv`, `affected_row_buckets.py`,
`affected_row_buckets_stdout.txt`, `affected_row_dow_verify.txt`,
`lattice_same_second_probe.csv`, `lattice_same_second_probe.py`, `probe_stdout.txt`.

**These files were NOT read into this register and none of their content is summarised here.**
Per the item's instruction, the V7 result is appended by the orchestrator, not transcribed by
the register author. A future reader must treat the V7 verdict as coming from the appended text
(or from `v4_same_second_channel.md` directly), not from this stub.

Note also that `v7\` is **absent** from the committed evidence mirror at
`…\MBO_2025(4mon)+2026-01\evidence\fixture_spike\` — see §2 above.

### PROVEN / DERIVED / UNVERIFIED

Deliberately empty pending the V7 return. Do not populate by inference.

---

# How to reopen

When the author reopens the paper-side errata, do these things **in this order**. The ordering
matters because each step changes what the next step is allowed to assume.

1. **Re-read this register end to end, before anything else.** It is the only self-contained
   record of what was found, what was proven, and what was never checked. Reading an individual
   artifact first invites reconstructing a conclusion that the register already qualifies.

2. **Re-read the cited artifacts, in this order of dependency:**
   - `fixture_spike\R2_consolidated_report.md` (round-2 synthesis, sets the C-item context)
   - `fixture_spike\c1\` → `c2\` → `c5\` (the Phase 5/7 defect chain: provenance → same code →
     environment pin)
   - `fixture_spike\c6\a4_defect_audit.md` → `c6\era_attribution.md` (which era owns which
     published claim)
   - `fixture_spike\v3\` → `v4c\` (dtype witness, then the measurement)
   - `fixture_spike\v5e\` + `t3\` (day-edge)
   - `fixture_spike\v6\` (a12 complex; Entries 3, 4, 9 all live here)
   - `fixture_spike\v7\` + the orchestrator's appended Entry 10 text
   - `fixture_spike\m5\`, `n1\`, `n2\`, `n3\` for the lattice-provenance context behind Entry 10

3. **Re-verify every number before drafting a single sentence.** Six of the ten entries were
   re-measured while writing this register and two carried figures that needed correcting
   (Entries 7 and 8). Assume the same rate applies to anything not re-measured here.

4. **Only then decide scope.** The entries are deliberately *not* grouped into proposed errata
   notices, because grouping is a scope decision and R10 reserves it to the author. The natural
   fault lines a scoping decision will have to choose among:
   - by **era** (Phase 5/7 vs Phase 6 vs v4/v5),
   - by **kind** (computational defect vs transcription/labelling vs internal contradiction),
   - by **severity** (does the qualitative conclusion move, or only the number?).
   Entries 4, 6, 7, 8 and 9 require **no** defect to be true — they are self-contained
   discrepancies between printed text and archived data, and are the cheapest to act on.
   Entries 1, 2, 3 and 10 involve computational defects and would require re-running code to
   quantify.

5. **Check the register against the world before publishing anything.** This register is frozen
   at 2026-08-12 against HEAD `0ee26c4`. If the archive, the paper draft, or the prereg has
   moved, re-derive rather than trust.

6. **Keep the v30a boundary.** Per R10, the amendment "stands on its own and neither asserts nor
   depends on any paper correction." Do not import errata language into amendment text, or
   amendment language into errata text.

---

# Cross-entry caveats — method limits that apply everywhere in this register

These are limits of the *verification method*, not of any single entry. Each has bitten at least
once already.

### C-1. The Grep-undercount lesson

`.gitignore` in the archive excludes `/pc2_transfer/`, `/results/`, `/transfer/`,
`/USB_ALL_PHASES/` and more. **Any ignore-respecting search silently misses most of the
archive** — including, specifically, every Phase 5/6/7 result tree and the `pc2_transfer` script
copies. All sweeps recorded in `c5\env_records.md` §4 had to be re-run with `--no-ignore` after
this was discovered. **A zero-hit search result in this project means nothing unless the search
explicitly disabled ignore files.** When reopening, re-run every negative search with
`--no-ignore` (or an equivalent) before relying on it.

### C-2. NQ's missing month-level MBO parquets

NQ has no `nq_mbo_YYYY-MM.parquet` files in the pattern every other instrument uses (e.g.
`processed\zc\zc_mbo_2025-01.parquet`). NQ's MBO data exists only as **per-day** parquets inside
directories `processed\nq\v4_gapfill\nq_mbo_2025-01\` (e.g. `nq_mbo_20250102.parquet`).
Verified 2026-08-12. Consequences: any tool or check written against the month-file pattern
finds nothing for NQ and may report a spurious zero; M5's NQ result is trades-only with 6 of 10
event classes unmeasured, so **NQ's clean result in M5 is not a clean pass**. Entries 6 and 7
concern NQ numbers, so this limit is directly relevant to reopening them.

### C-3. Phase 6 code is absent from the archive

No Phase 6 producing script exists anywhere (verified by grep for
`marginal_gain_over_prev_tier` / `flag_triggered` / `l3_fix_applied` / `phase6_main_summary`
across all `*.py`: zero hits; and by `find -iname "*phase6*"`: only result files). Phase 6
predates the repo's first commit (`9c37285`, 2026-04-15). **Everything in Entries 6 and 7 is
artifact-level only.** Era attribution is decidable; producing-script attribution is not; and
line-level defect presence in Phase 6 code is undecidable from the archive. Do not write an
erratum sentence that implies the Phase 6 code was inspected.

### C-4. Static audit ≠ execution witness

Entries 3 and 5 rest partly or wholly on static reading. `v6` (a12) has **no** execution witness
of its own — its wrap conclusion transfers from `v4c`'s measurement of the structurally
identical a4 site. `v5e` (day-edge) is static; its magnitudes come from `t3`, which measured a
*different* (Phase 5) lattice. The register labels these as DERIVED, and they should not be
promoted to PROVEN by repetition.

### C-5. Single-slice measurements

`v4c` measured one instrument, one month, one session hour (zc `v4_gapfill` 2025-01, 1,412
one-second windows). `t3` measured one instrument-month (ZC 2025-01, 338,159 rows). `v3`
witnessed one month per instrument (2025-01, the first in `a4_runner`'s own load order).
**M5 is the cautionary case: a result that held on ZC 2025-01 failed on ZC 2025-08.** Treat any
single-slice number as an existence proof, never as a population estimate.

### C-6. Lost run-time records

The Phase 5 pre-fix run logs were written to `C:\MBO_data\*.log`; that drive is gone and no copy
exists in the archive (`Glob **/phase5_batch*.log` → no files). Whether `C:\MBO_data\zc\` held
byte-identical copies during the runs is unrecorded. The environment pin in Entry 1 is
bracketing-plus-directory-metadata, not an in-window record.

### C-7. Mirrored result trees

Phase 6 results exist in four mirrored locations; `phase5_fixed` results in at least four;
`zc_CNN_5s_Full` artifacts in eight. **A path is not an identity.** When citing, name the exact
path and check whether siblings differ (they sometimes do — the `phase5_fixed` and `dl_rerun`
ZC CNN 5 s Full runs differ by 0.17 AUC).

### C-8. Rounding artifacts in published ratios

Entry 7 shows a published ratio (23×) that is not reproducible from the exact inputs (22.5×)
because it was computed from already-rounded means. Before writing any corrected ratio, decide
and state whether it is computed from exact or rounded inputs, and give both.

### C-9. Value collisions across eras

The same printed value can denote different quantities in different eras — "+0.018" is a Phase 6
post-fix L3 gain in one sentence and a v4-era nq/asia_overnight edge in four others; "0.957"
has four candidate anchors in three Phase 5 generations. Never identify a paper number by string
match alone.

### C-10. What this register does not contain

No detector code, no availability-model implementation, no `audit()` surface, and no
development-corpus contact were produced or used in building it. The register is a planning
artifact. The prereg repo was read only; nothing in it was edited, and no state-changing git
command was run.

---

*End of register. Frozen 2026-08-12. All entries `DEFERRED-PER-R10`. Entry 10 awaits the
orchestrator's appended V7 result.*
