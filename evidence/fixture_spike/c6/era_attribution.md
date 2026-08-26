# C6b — Paper-Claim Era-Attribution Table

Scope: attribute each erratum-relevant published claim to its producing pipeline generation
(Phase 5 / Phase 6 / Phase 7 / v4-v5), with archive evidence. Static reads only; archive
root = `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` (read-only). Paper extracts:
`scratchpad\main_paper.txt` (July 2026, 35 pp) and `scratchpad\ia.txt` (IA, May 2026, 15 pp).
Line numbers below are 1-indexed file lines of the named files.

Established context relied on (cited as given, not re-derived):
- Phase 5/7-era trade aggregation carries two CONFIRMED defects: `is_buy = trades["aggressor_side"].isin(["B","Buy","buy"])` matches nothing (parquet values are BUY_AGGRESSOR/SELL_AGGRESSOR/UNKNOWN, e.g. `scripts\pipeline\process_zc.py:92-100`), and `signed_vol = np.where(is_buy, size, -size)` negates arrow-uint32 `size` without cast (wraps mod 2^32 under pinned pandas 3.0.1/numpy 2.4.2). `phase7_l2_sim.py` shares both (lines 207/209).
- v4-era reimplementation `scripts\v4\a4_runner.py` (file mtime 2026-04-21 19:10, untracked in git) rebuilds ~35 features itself (lines 101-123; `apply_causal_lag` 343-347) and its defect status is the subject of item C6a — **C6a's verdict governs all v4-attributed claims below; referenced as PENDING here**.
- Prior spike S4 reconciliations for Phase 6 numbers (restated where used, marked "established").

---

## Claim 1 — Headline AUCs (abstract/intro + IA.1 per-cell table)

**Published sentences (verbatim):**
- `main_paper.txt:59-61`: "The strongest cells (corn futures overnight, AUC = 0.873) exhibit edge-over-chance of +0.361, while the weakest (NQ Nasdaq futures across all sessions) hover at +0.010-0.020, barely above the noise floor."
- `ia.txt:29` (IA.1 row): "zc full_session 0.3545 0.8579 CNN 5 T1 EXPLORATORY"

**Generation: v4** (Design A runs; April–May 2026).

**Producing artifacts:**
- `results\designA\a4_master_designA.csv` — line 947: `zc,full_session,CNN,5,BFree,...` with `test_auc_overall = 0.8579033464898526`; line 2156: `zc,overnight,Transformer,10,Full,...` with `test_auc_overall = 0.8728528898420927`.
- `results\final\a7_three_design_synthesis.csv` — line 4 carries `test_auc_A = 0.8579033464898526` for zc/full_session; line 2 carries `test_auc_A = 0.8728528898420927` and `edge_median = 0.360912` for zc/overnight (paper's "+0.361").
- `paper\v4\ia_tables\ia_table_1a.csv` — line 4: `zc,full_session,0.3545,0.8579,CNN,5,T1,EXPLORATORY` (exact IA.1 row); line 2: `zc,overnight,0.3609,0.8729,Transformer,10,T1,EXPLORATORY` (abstract's 0.873 rounded).

**Evidence chain (script + commit):**
- `scripts\v4\a4_runner.py` writes `a4_results_{PC}.csv` (line 56: `RESULTS_CSV = OUT_DIR / f"a4_results_{PC}.csv"`).
- `scripts\v4\a4_merge_designA.py` merges those into `a4_master_designA.csv` (lines 14-18 inputs, line 85 `master.to_csv(MASTER, ...)`).
- `scripts\v4\a7_three_design_synthesis.py` reads it (line 28: `A4_MASTER = ROOT / "results" / "designA" / "a4_master_designA.csv"`; read at line 122) and writes the synthesis.
- `scripts\v4\paper_ia_tables.py` reads the synthesis (line 63) and writes `paper/v4/ia_tables/ia_table_1a.csv` (line 17 `OUT = Path("paper/v4/ia_tables")`, line 91).
- Git commits: `7ac5de8` (2026-05-03 09:59) "Internet Appendix tables: IA.1a/1b/3/4 for v4 paper" (commit message states IA.1a = 46 rows, T1=9...); `8c2c66f` (2026-05-03 08:28) "Master-of-masters: consolidate v3 + v4 findings"; `741fc6a` (2026-04-30 15:08) "A8: Master findings v4 LOCKED". `a4_runner.py` itself is NOT git-tracked (confirmed via `git ls-files scripts/v4/`); its filesystem mtime is 2026-04-21 19:10.

**Decidability: DECIDED — v4.** Value match is exact to 16 digits across the whole chain.
**Defect exposure:** rests on v4 feature code (`a4_runner.py`). Governed by C6a's verdict (PENDING at time of writing). Not covered by the established Phase 5/7 defect confirmation.

---

## Claim 2 — Feature-importance / ablation (paper §9.4, IA.5)

**Published sentence (verbatim), `main_paper.txt:1138-1142`:**
"Feature ablation on the 17 T1/T2 cells (582 ablation runs) confirms: the maximum single-feature sig-nal contribution is 2.16%, with vwap_distance appearing most frequently in cells' top-5 (15/17 cells) but never exceeding ~2%. Signal is distributed across multiple features — principally vwap_distance, net_delta_1s, and l1_imbalance — with no single feature dominating."

**Generation: v4** (A9 leakage re-verification).

**Producing artifacts:**
- `results\final\a9_leakage_ablation.csv` — 583 lines = 582 data rows, of which 17 are `__BASELINE__` rows (grep count = 17) and 565 are feature-removal runs.
- `results\final\a9_leakage_summary.txt` — "Cells analyzed: 17 (T1_VERY_STRONG + T2_STRONG)"; "Total ablation runs: 565"; "Max 'max single-feature impact' across cells: 2.16% (cell: es/europe_overnight)".
- `paper\v4\ia_tables\ia_table_4.csv` (IA.5 source) — 86 lines = 85 data rows (17 cells x top-5); line 27: `es,europe_overnight,net_delta_1s,0.0732,0.0716,0.0016,2.16` — the paper's 2.16% maximum is a net_delta_1s ablation; line 3: `cl,afternoon_close,net_delta_1s,0.1342,0.1341,0.0001,0.08` matches `ia.txt:210` verbatim.
- `MASTER_FINDINGS\v4\master_of_masters.csv:397`: `a9_leakage,summary,n_total_ablation_rows,582` — the paper's "582 ablation runs" equals the CSV row count INCLUDING the 17 baselines; the summary's own "565" excludes them (582 − 17 = 565). Both counts are archive facts; the paper printed the row-count figure.

**Evidence chain (script + commit):**
- `scripts\v4\a9_leakage_ablation.py` — line 33: `import a4_runner as r`; line 70 reads `results/designA/a4_master_designA.csv` to pick each cell's best tree model; lines 93-94: `feat = r.build_snapshot_features(filt, inst)` / `feat = r.add_trade_features(feat, trades)` — i.e., the ablation REBUILDS features with the v4 `a4_runner` code (its docstring, lines 4-10: "rebuilds bucket-filtered features the same way A4 did ... same features, same causal [lag]").
- `scripts\v4\paper_ia_tables.py` line 69 reads `results/final/a9_leakage_ablation.csv`; line 221 writes `ia_table_4.csv`.
- Git commit: `f125e77` (2026-05-01 00:13) "A9: Leakage re-verification — L3 ablation on 17 T1/T2 cells"; IA table commit `7ac5de8` (2026-05-03), whose message states "IA.4: 85 rows ... Max pct = 2.16% ... vwap_distance (15x), net_delta_1s (13x), l1_imbalance (13x)".

**Decidability: DECIDED — v4.**
**Defect exposure:** the ablation's `net_delta_1s` (and all trade-flow features) were computed by `a4_runner.py`'s feature build. Whether they were computed on wrapped/mistagged values is exactly C6a's question — **C6a verdict governs (PENDING)**. Not covered by the established Phase 5/7 confirmation.

---

## Claim 3 — NQ "+0.10 -> +0.018" (paper §4.4, Mechanism 2)

**Published sentence (verbatim), `main_paper.txt:494-495`:**
"The single-instrument maximum (NQ) shows pre-fix gain of +0.10 declining to +0.018 post-fix, a 5.6-fold reduction."

**Generation: Phase 6** (both numbers; pre-fix ~2026-04-10, post-fix from the L3-fixed rerun).

**Producing artifacts + value match:**
- **"+0.10" (pre-fix, NQ):** `results\phase6\second_pc\phase6_main_summary.csv` — file line 4: `NQ,LightGBM,5,L3,...,marginal_gain_over_prev_tier = 0.1038`; file line 7: `NQ,XGBoost,5,L3,...,0.1051`. Second-PC Phase 6 pre-fix run. (Matches established S4 reconciliation.)
- **"+0.018" (post-fix):** `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` — NQ post-fix rows (file lines 34-41) have marginal gains of −0.0011, −0.0004, −0.0001, −0.0010, +0.0002, +0.0002, −0.0008, −0.0032; the NQ post-fix maximum is +0.0002. The only ~0.018 values in the file are HE's: line 18 `HE,LightGBM,5,L3,...,0.0182,...,shift_1s` and line 19 `HE,XGBoost,5,L3,...,0.0181,...,shift_1s`. **The published "+0.018 post-fix" numerically matches HE's post-fix maximum (0.0182), not any NQ value** — confirming the established S4 reconciliation directly against the CSVs. Whether this was a transcription error or a deliberate-but-unmarked substitution is not decidable from the archive.

**Evidence chain (script + commit):**
- No producing script exists anywhere in the archive: a repo-wide grep of `*.py` for `marginal_gain_over_prev_tier`, `flag_triggered`, `l3_fix_applied`, and `phase6_main_summary` returns zero hits; `find -iname "*phase6*"` returns only result CSVs/JSONs (four mirrored copies under `results\phase6\`, `results\phase6\pc2\`, `results\pc2_all_phases\phase6\`, `pc2_transfer\results\phase6\`) and no code.
- Phase 6 predates version control: the git repo's first commit is `9c37285` (2026-04-15, "v4 pre-registration: methodological lock"); Phase 6 main-PC completion stamp is `results\phase6\overnight_complete.txt`: "Timestamp: 2026-04-10T03:39:56.459212".

**Decidability:** era attribution **DECIDED — Phase 6** (artifact paths, column schema shared with phase6 JSON run files, completion stamp). Producing-script attribution **UNDECIDABLE from the archive** (script absent).
**Defect exposure:** pre-fix Phase 6 sits inside the era whose aggregation code is CONFIRMED defective for Phase 5 and Phase 7 (established); the Phase 6 runner itself is not in the archive, so line-level presence of the two defects in Phase 6 code is **undecidable from the archive**.

**Collision note (fact, not inference):** the string "+0.018" also appears at `main_paper.txt:614` ("+0.011 (nq/midday) to +0.018 (nq/asia_overnight)"), `:735`, `:800`, and `:947` ("+0.018, AUC 0.524"), where it denotes the v4-era edge of nq/asia_overnight (IA.1 `ia.txt:63`: "nq asia_overnight 0.0176 0.5235 XGBoost 5 T4"). Same printed value, different era and different quantity than the Mechanism-2 "+0.018 post-fix".

---

## Claim 4 — The "23-fold" figure

**Published sentence (verbatim), `main_paper.txt:492-493`:**
"Magnitude: mean L3 gain pre-fix = +0.035 AUC, post-fix = +0.0015 AUC — a 23-fold reduction (mean-to-mean across all 8 instruments)."
(Also `main_paper.txt:92`: "Mechanism 2, producing 23-fold apparent signal inflation"; `main_paper.txt:480`: "the 23-fold mean inflation from Mechanism 2".)

**Generation: Phase 6** (numerator and denominator both).

**Producing artifacts:**
- **Numerator (+0.035):** `results\phase6\phase6_main_summary.csv` — main-PC file containing ONLY ES/CL/HE/LE (verified: the file's instrument column contains no NQ/GC/ZC/ZS rows). Corroborated verbatim by `results\phase6\overnight_complete.txt`: "Mean L3 gain: 0.0346 (n=32)" (main PC, 96/96 runs, timestamp 2026-04-10). Per established S4: paper's "+0.035 pre-fix" = this 4-instrument mean 0.0346; the 8-instrument mean is 0.0280 — **the paper's "across all 8 instruments" phrasing does not match the numerator's actual 4-instrument scope** (established; file contents consistent with it).
- **Denominator (+0.0015):** `results\phase6\phase6_l3_fixed\phase6_l3_fixed_results.csv` — 65 lines = 64 data rows (matches established "mean over 64 runs" = 0.0015; all rows carry `l3_fix_applied = shift_1s`).
- **Ratio:** 23-fold = 0.0346/0.0015 (established S4).

**Evidence chain:** same as Claim 3 — no Phase 6 script in the archive; era decided by artifact paths + `overnight_complete.txt` stamp (2026-04-10, pre-dating the git repo and the v4 rebuild).
**Decidability:** era **DECIDED — Phase 6**; producing script **UNDECIDABLE from the archive**.
**Defect exposure:** same as Claim 3 (Phase 6-era artifacts; runner absent; Phase 5/7 defects established for the surrounding era's code).

---

## Claim 5 — The 0.957/0.675 pair (Mechanism 1 magnitude)

**Published sentence (verbatim), `main_paper.txt:488-489`:**
"Magnitude: Full AUC on ZC = 0.957 vs. BFree = 0.675 (28 pp inflation)."

**Generation: Phase 5** — ESTABLISHED (prior spike; restated per instruction, no re-derivation): the pair = Phase 5 pre-fix best-Full `zc_XGBoost_5s_Full` 0.956733 (or checkpoint 0.9573 `zc_XGBoost_30s_Full`) vs `zc_Transformer_5s_BFree` 0.675179.

**Archive anchors observed in this pass (locations only; attribution stands as established):**
- 0.9573: `results\phase5\phase5_master.csv` line 10 (run_key `zc_XGBoost_30s_Full`, test_auc column = 0.9573) and `results\phase5\checkpoint_zc.json` line 455 (`"test_auc": 0.9573` under `"zc_XGBoost_30s_Full"`).
- 0.956733: `USB_ALL_PHASES\phase5_fixed\master_phase5_384runs.csv` line 331 (`ZC,XGBoost,5,Full,...,0.956733,...`) and `USB_ALL_PHASES\phase5_fixed\cpu_track2\detail\zc_XGBoost_5s_Full_results.json`.
- 0.675179: `USB_ALL_PHASES\phase5_fixed\gpu_track2\detail\zc_Transformer_5s_BFree_results.json` line 12 (`"test_auc": 0.675179`); also in `gpu_track2\master_phase5_fixed.csv` and `master_phase5_384runs.csv`.

**Decidability: DECIDED — Phase 5 (established).**
**Defect exposure:** Phase 5 code carries both CONFIRMED defects (established: dead `is_buy` `.isin(["B","Buy","buy"])` match and uint32 negation wrap under the pinned original environment).

---

## Defect-exposure split by era (summary)

| # | Claim | Era | Rests on defect-CONFIRMED code? |
|---|-------|-----|-------------------------------|
| 1 | Headline AUCs (abstract 0.873 / IA.1 incl. zc full_session 0.8579) | v4 | No established confirmation — **C6a verdict governs (PENDING)**; features rebuilt by `scripts\v4\a4_runner.py` |
| 2 | §9.4 ablation (582 runs, 2.16% max, net_delta_1s named) | v4 | Same — ablation imports `a4_runner` and rebuilds features with it (`a9_leakage_ablation.py:33,93-94`); **C6a governs (PENDING)** |
| 3 | NQ "+0.10 -> +0.018" | Phase 6 (both numbers) | Pre-fix is defect-era output; Phase 6 runner absent from archive → line-level defect presence **undecidable**; published "+0.018" matches HE's post-fix 0.0182, not NQ (NQ post-fix max +0.0002) |
| 4 | "23-fold" (0.0346 / 0.0015) | Phase 6 (both) | Same as #3; numerator is the 4-instrument main-PC mean despite "all 8 instruments" phrasing (established, artifact-consistent) |
| 5 | ZC Full 0.957 vs BFree 0.675 | Phase 5 | **Yes — both defects CONFIRMED for Phase 5 code (established)** |

Cross-reference: item C6a (v4 `a4_runner.py` defect audit) decides the defect status of claims 1-2. If C6a finds the v4 rebuild clean, claims 1-2 are attributable to non-defective code; if C6a confirms either defect in `a4_runner.py`, claims 1-2 inherit it. This file takes no position — C6a was PENDING when this table was written.
