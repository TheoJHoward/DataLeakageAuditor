# ITEM V6 — Static audit: a12_academic_signals.py (C6a same-form negation, lines 157/187)

Target: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a12_academic_signals.py` (553 lines, read in full).
Downstream importer also audited (required for exposure tracing): `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a12_per_bucket_delta_auc.py`.
Method: static reading only. No detector code, no contact with development-corpus parquets. Dtype claims below distinguish execution-witnessed (prior item, he/le) from static writer-chain inference.

---

## (a) The two negation sites, classifier, dtype path, and what each signed quantity feeds

### Site 1 — line 157, inside `compute_ofa_lagged` (lines 149–175) — DEAD CODE

Verbatim, a12_academic_signals.py:149–175 (elisions marked):

```python
149  def compute_ofa_lagged(trades: pd.DataFrame | None,
150                            snap_ts: pd.Series, lags: list[int]) -> dict:
151      """Compute order-flow autocorrelation at given lags (in seconds).
152      Returns {lag: autocorr_value} computed on per-second signed flow."""
153      if trades is None or trades.empty:
154          return {L: float("nan") for L in lags}
155      tr = trades[["ts_event", "size", "is_buy_aggressor"]].copy()
156      tr["sec"] = tr["ts_event"].dt.floor("1s")
157      tr["signed"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
158      flow = tr.groupby("sec")["signed"].sum().sort_index()
...
167      full_idx = pd.date_range(flow.index.min(), flow.index.max(), freq="1s", tz="UTC")
168      flow = flow.reindex(full_idx, fill_value=0)
...
174          out[L] = float(flow.autocorr(lag=L))
```

**Callers: none.** A repo-wide grep for `compute_ofa_lagged` finds only its definition (line 149), the docstring cross-reference at line 180, the live call to the `_signed` variant at a12_academic_signals.py:256, and the import/call of the `_signed` variant in a12_per_bucket_delta_auc.py:44 and :132. Site 1 is dead code carrying the defect form; it produces no published number.

### Site 2 — line 187, inside `compute_ofa_lagged_signed` (lines 178–212) — LIVE, feeds two published pipelines

Verbatim, a12_academic_signals.py:178–212 (elisions marked):

```python
178  def compute_ofa_lagged_signed(trades: pd.DataFrame | None,
179                                   snap_ts: pd.Series, lags: list[int]) -> tuple[dict, pd.Series]:
180      """Same as compute_ofa_lagged but also returns per-second signed flow
181      as a snapshot-aligned series for use as a model feature."""
...
185      tr = trades[["ts_event", "size", "is_buy_aggressor"]].copy()
186      tr["sec"] = tr["ts_event"].dt.floor("1s")
187      tr["signed"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
188      flow = tr.groupby("sec")["signed"].sum().sort_index()
189      if len(snap_ts):
190          t_min = pd.to_datetime(snap_ts.min(), utc=True)
191          t_max = pd.to_datetime(snap_ts.max(), utc=True)
192          flow = flow.loc[(flow.index >= t_min) & (flow.index <= t_max)]
...
196      full_idx = pd.date_range(flow.index.min(), flow.index.max(), freq="1s", tz="UTC")
197      flow_full = flow.reindex(full_idx, fill_value=0)
198      out: dict = {}
199      for L in lags:
200          if L >= len(flow_full):
201              out[L] = float("nan")
202          else:
203              out[L] = float(flow_full.autocorr(lag=L))
204      # broadcast to snapshots: 5s rolling sum of signed flow at snapshot ts
205      flow_5s = flow_full.rolling(5, min_periods=1).sum()
...
209      merged = pd.merge_asof(snap_df, flow_df, on="ts_event", direction="backward")
...
212      return out, aligned
```

The negation is byte-identical in form to the established a4 defect (`a4_runner.py:307  tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])`).

### Classifier used at both sites

`is_buy_aggressor` — the **working boolean classifier**, same one a4 uses. Chain:

- Created at write time: `scripts\pipeline\flow_tagger.py:105  trades["is_buy_aggressor"] = trades["side"] == "B"` (Databento T-message records the aggressor order; BBO fallback at lines 115–139; residual NaN forced False at line 145). Returns bool dtype (docstring line 97: "is_buy_aggressor — bool").
- Loaded: a12_academic_signals.py:412 `trades = r.load_trades(inst)` → `a4_runner.py:218  df = pq.read_table(str(p), columns=["ts_event", "price", "size", "is_buy_aggressor"]).to_pandas()`; paths per `a4_runner.py:134–140` (`es` → `processed\es\v4_morning_chunk`; `nq/cl/gc/zc/zs` → `processed\{inst}\v4_gapfill`; `he/le` → `processed\{inst}`).
- The `astype(bool)` at 157/187 is applied only to `is_buy_aggressor`, never to `size`.

Note: the VPIN function (`compute_vpin_per_snapshot`, lines 111–146) does NOT use `is_buy_aggressor`; it uses its own tick-rule classifier (lines 119–121: price-diff sign, ffill, zeros default) per Easley et al. — a design choice, not a defect.

### Dtype path of `size` at the negation sites

1. Origin: `g2_day_worker.py:126–127` loads Databento `DBNStore.from_file(...).to_df()`; the Databento MBO schema `size` field is uint32. No cast anywhere in the worker; trades written at `g2_day_worker.py:192–195` (`trades = tag_aggressor(df, snapshots=None)`; `trades.to_parquet(trades_out, index=False, engine="pyarrow")`). `flow_tagger.tag_aggressor` (lines 99–147) adds only `aggressor_side`/`is_buy_aggressor`, never touches `size` dtype.
2. Month concat: `g2_reprocess.py:161–162  trade_df = pd.concat(trade_dfs, ignore_index=True); trade_df.to_parquet(trades_out, ...)` — no cast.
3. Parquet dtype: **execution-witnessed arrow-uint32 for the he/le family** (established, prior item). For es/nq/cl/gc/zc/zs the writer chain above statically implies the same uint32, but this audit did not execution-witness those files (no corpus contact) — reported as static inference, not witness.
4. Load: `a4_runner.py:218` `pq.read_table(...).to_pandas()` → numpy uint32 column (pyarrow's default conversion for a null-free unsigned column; a null-bearing column would promote to float64 and would defuse the wrap — not witnessed here, but the identical loader underlies the established a4 finding).
5. In a12: line 155/185 column-select `.copy()` preserves dtype. **No `astype` touches `size` anywhere in a12_academic_signals.py.** Full astype inventory of the file: line 127 `.astype("int64")` on `bucket_idx` (VPIN volume-bucket index, after the subtraction-free cumsum), lines 157/187 `.astype(bool)` on `is_buy_aggressor`, lines 371, 376 str casts on inst/bucket keys. Environment: pinned original env = current env (pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1).
6. At line 157/187, `-tr["size"]` on a numpy-uint32 Series wraps mod 2^32 (sell of size s becomes 4294967296−s); `np.where(bool, uint32, uint32)` yields a uint32 "signed" column; the groupby-sum at 158/188 accumulates the wrapped values (pandas sums unsigned into uint64). `warnings.filterwarnings("ignore")` at line 37 suppresses any warning that might otherwise surface.

### What each signed quantity feeds

- `out` (OFA autocorr at lags 1/5/10/30) → `process_cell` line 256 → CSV columns `ofa_1s/ofa_5s/ofa_10s/ofa_30s` in `results\final\a12_academic_signals.csv` (row dict lines 334–337). **These raw autocorrelations never reach the paper or IA** (verified by search; see (c)).
- `flow_5s` (5s rolling sum of the signed flow, snapshot-aligned) →
  - a12_academic_signals.py:257 `feat["flow_5s"] = flow_5s.values`; line 288 `sig_cols = ["ofi_10s", "vpin", "flow_5s", "dar"]`; lines 305–320 the 4-feature LogReg → `simple_lr_test_auc` / `simple_lr_edge` → merged against `master_findings_v4.csv` `edge_median` in `write_summary()` (lines 439–453) → `a12_signals_vs_ml.csv` (`ml_edge`, `ratio_simple_over_ml`), `a12_session_variation.csv`, `a12_summary.txt`.
  - a12_per_bucket_delta_auc.py:132–133 (via `from a12_academic_signals import ... compute_ofa_lagged_signed` at line 44) → `flow_5s` is the "OFA" signal in the LightGBM augmentation (SIGNAL_COLS line 136) → `ofa_augmented_auc` / `ofa_delta_auc` in `results\final\a12_per_bucket_delta_auc.csv` and comparison CSV.
- Sanity observation consistent with (but not proof of) the wrap firing: in `a12_academic_signals.csv` the ofa_* values are nearly constant across buckets within an instrument (all nq buckets ofa_5s ≈ 0.4934±0.0002; es ≈ 0.487; gc ≈ 0.2245; cl ≈ 0.1965; zc ≈ 0.0940; zs ≈ 0.1172; he ≈ 0.1240; le ≈ 0.1434). Two compatible static explanations: (i) the [t_min, t_max] restriction at lines 189–192 spans essentially the whole 4-month calendar for every bucket (min/max of the bucket's snapshot timestamps), and the reindex at 196–197 fills all non-bucket hours with 0, so every bucket's "OFA" is computed on nearly the same full-period series — a design quirk independent of dtype; (ii) wrapped flow ≈ 2^32 × (per-second sell-trade count), whose autocorrelation measures trade-arrival clustering, not signed flow. Not adjudicated here (would require execution).

### Additional same-family site found in this file (not flagged by C6a): line 134, VPIN unsigned subtraction

```python
122      tr["buy_sz"] = np.where(sign > 0, tr["size"], 0)
123      tr["sell_sz"] = np.where(sign < 0, tr["size"], 0)
...
129      grp = tr.groupby("bucket_idx").agg(
130          ts_end=("ts_event", "last"),
131          v_buy=("buy_sz", "sum"),
132          v_sell=("sell_sz", "sum"),
133      ).reset_index()
134      grp["abs_imb"] = (grp["v_buy"] - grp["v_sell"]).abs()
135      grp["vpin_raw"] = grp["abs_imb"] / (grp["v_buy"] + grp["v_sell"]).replace(0, np.nan)
```

Static dtype reasoning under the same uint32 premise: `np.where(sign > 0, uint32, 0)` → uint32 (NEP-50 weak scalar); pandas groupby-sum of unsigned → uint64; `v_buy − v_sell` on uint64 wraps to ~1.8e19 for any net-sell volume bucket; `.abs()` on unsigned is a no-op; `vpin_raw` then astronomically exceeds its [0,1] range for net-sell buckets, and the N=50 rolling mean (line 136) propagates it. Fires under exactly the same dtype condition as the line-187 negation — if C6a's negation is live, this is live. There is no negation here, so C6a's form-match would not have flagged it. (Checked in passing: `tr["cum_vol"] = tr["size"].cumsum()` at line 126 stays uint32 but 4-month per-instrument contract volume is far below 2^32, so no plausible overflow; and OFI/DAR are not exposed — see below.)

### Sites confirmed dtype-safe (book-side)

- OFI (lines 68–99): all inputs are snapshot `bid/ask_size_L` columns via `.diff()` and `.shift(1)` — pandas promotes both to float64 (NaN insertion) before any subtraction/negation, so no wrap; and snapshot sizes are built from Python ints in the book engine (`scripts\pipeline\book_engine.py:48–49  self._bid_sizes: dict[float, int]`, row dicts of Python ints at 274/281, `size=int(sizes[i])` at 372) → pandas infers signed int64 at DataFrame construction → parquet int64.
- DAR (lines 102–108): `(bid − ask) / tot` on raw snapshot columns — safe for the same reason (int64 snapshot sizes). DAR is algebraically `l1_imbalance` (a4_runner.py:252).

---

## (b) Per-defect verdicts for a12_academic_signals.py

| Defect | Verdict | Basis |
|---|---|---|
| Boolean aggressor classifier | **ABSENT (working classifier carried)** | Both sites use `is_buy_aggressor.astype(bool)`, the verified Databento-side flag (flow_tagger.py:105), same as a4_runner:218/307. No tick-rule substitution at the OFA sites. VPIN deliberately uses a tick rule per its published definition — not a classifier defect. |
| Uncast unsigned negation (`-tr["size"]`) | **CARRIED** — line 157 (dead code, no callers) and line 187 (live; feeds two published pipelines). No `astype` touches `size` anywhere in the writer→loader→negation chain (full inventory above). Dtype premise: witnessed arrow-uint32 for he/le; statically inferred uint32 (Databento origin, cast-free writers) for es/nq/cl/gc/zc/zs. | |
| (New, same family) unsigned `v_buy − v_sell` in VPIN | **CARRIED** — line 134, live, fires under the identical dtype condition; corrupts `vpin` for every net-sell volume bucket. | |

Caveat stated, not inferred away: for the six non-he/le instruments the uint32 premise rests on the static writer chain (databento uint32 → cast-free parquet → `to_pandas()`), not on execution witness; and a null-bearing parquet `size` column would load as float64 and defuse both sites. Nothing in the read code inserts nulls into `size`.

---

## (c) Which published results flow through it

Anchoring commits (archive repo `C:\Users\ttbea\OneDrive\Desktop\MBO_2025`):
- `bc1fee0` "A12: Academic signal replication — OFI/VPIN/OFA/DAR per bucket + ML comparison" (headlines: rho=+0.97, 89.5% median capture, 30/43, 0/43, ES/CL gap cells, DAR gradients 1.74x/4.9x, ML 8.9x).
- `cb9eedf` "A12 per-bucket delta-AUC: 43 cells x 4 signals" (headlines: OFI median +0.0009 max +0.0083; VPIN median −0.0005 max 0.0046; OFA median +0.0001 max +0.0013; DAR identically 0.0000).

Numeric verification performed against the archived output CSVs (43 rows each):
- `a12_signals_vs_ml.csv`: Spearman(simple_lr_edge, ml_edge) = **0.9710**, median ratio = **0.8955**, mean = 0.8242, 30/43 above 0.8, 0/43 below 0.2 — the paper's Table 9 row-for-row ("+0.97", "89.5%", "30 / 43", "0 / 43").
- `a12_per_bucket_delta_auc.csv`: max|ofa_delta_auc| = 0.0013, max|vpin_delta_auc| = 0.0046, dar_delta_auc = 0.0000 everywhere — matches IA.4 cell values spot-checked (zc/overnight OFA ∆ −0.0009 = −0.000913; gc/morning OFA ∆ −0.0011 = −0.001067; le/open VPIN ∆ −0.0046 = −0.004571; he/afternoon OFI ∆ 0.0083 = 0.008279; DAR corr column = dar_predcorr, e.g. zc/overnight 0.1301 = 0.130066).

### Published numbers that PASS THROUGH the line-187 negation (flow_5s-fed)

Every "Simple", "Capture", "Gap" figure is the output of the 4-feature LogReg whose feature `flow_5s` is the corrupted signed flow; every "OFA ∆" figure is the marginal AUC of that corrupted feature.

main_paper.txt:
1. Line 24 (abstract): "Simple academic signals capture a median 89.5% of ML edge…"
2. Lines 101–103 (intro): "captures a median 89.5% of the ML edge (Spearman ρ = +0.97, n = 43 cells)… (ES Europe overnight: simple +0.056 vs. ML +0.182)".
3. Section 5.9 + Figure 3, lines 765–812: "+0.056… +0.182… a +0.126 gap", "+0.111 simple, +0.193 ML, gap +0.082", the ten Figure-3 gap bars (+0.126, +0.082, +0.065, +0.035, +0.027, +0.026, +0.026, +0.024, +0.023, +0.018 — each equals ml_edge − simple_lr_edge from the CSV), and the caption "Across 43 cells, Spearman ρ = +0.97; median capture ratio 89.5%."
4. Section 8.2 Table 9, lines 1063–1071: all four table values.
5. Page-29 gap table, lines 1078–1081: ES/europe_overnight +0.056/+0.182/+0.126; ES/asia_overnight +0.111/+0.193/+0.082; CL/europe_overnight +0.082/+0.148/+0.065.
6. Line 1076: "The residual 10.5% where ML exceeds simple signals…" (= 1 − 0.895).
7. Line 1221 (conclusion): "Simple academic signals capture a median 89.5% of the ML edge…"

ia.txt (Internet Appendix IA.4, lines 151–203): the "OFA ∆", "Simple", "Capture", and "Gap" columns for all 43 rows (pages 7–8).

### Published numbers that pass through the SECOND carried site (line 134, VPIN)

- main_paper.txt lines 1096–1097: "VPIN produces a complete null across all instruments, sessions, and horizons (max |∆AUC| < 0.003)". (Also note an independent internal inconsistency: the archived vpin_delta_auc max |value| is 0.0046 (le/open), and cl/open is +0.0032 — both exceed the "< 0.003" printed bound; commit cb9eedf itself says "max 0.0046".)
- ia.txt IA.4 "VPIN ∆" column (43 values).
- `vpin` is also one of the 4 LogReg features, so the "Simple/Capture/Gap" numbers above carry both corrupted features simultaneously.

### Published a12 numbers that NEVER touch signed trade flow (book-only, dtype-safe path)

- IA.4 "OFI ∆" column and "DAR ∆" column (identically 0.0000) and "DAR corr" column — all from snapshot book columns (int64 origin; diff/shift promote to float64).
- Paper 8.1/IA.4 claim "DAR ∆AUC is identically 0.0000 … DAR ≡ l1_imbalance" (main_paper 1055–1059; ia.txt 152–153) — book-only.
- Paper 8.3 OFI discussion ("mean |r| = 0.019 across eight instruments", lines 1088–1089 and 503–504) — quotes the earlier v3/phase9 full-session analysis, not a12 output.
- Paper 8.4 gradient table (lines 1101–1103): the printed values 1.74× (Overnight/RTH) and 4.91× (K/FIFO) match the **dar_predcorr** row of `a12_session_variation.csv` (1.7438, 4.9119) — book-only — and the ML row matches ml_edge (3.7234, 8.7883). **However the column is labeled "Simple LR Ratio"; the actual simple_lr_edge gradients in the same CSV are 1.80× and 8.88× (flow-fed).** Commit bc1fee0 attributes 1.74×/4.9× to DAR explicitly, so the printed numbers are DAR gradients under a wrong label. As printed, these two numbers do not pass through the negation; if the label were taken at face value, the correct numbers would.
- The raw OFA autocorrelations (`ofa_1s/5s/10s/30s` columns, corrupted) appear in no paper or IA table — they surface only in the unpublished `a12_summary.txt`/logs.

### Bottom line

The C6a-flagged negation is CARRIED (live at line 187; dead at 157) with the working boolean classifier (classifier defect ABSENT), plus a second, previously unflagged same-family carrier at line 134 (VPIN). Exposed published claims: the paper's headline "simple academic signals capture ~89.5% of ML edge" complex (abstract, intro, Table 9, Figure 3, Section 5.9 case study, page-29 gap table, conclusion), the ES/CL overnight gap numbers, IA.4's OFA ∆ / VPIN ∆ / Simple / Capture / Gap columns (43 rows), and the "VPIN complete null" claim. Not exposed: IA.4's OFI ∆, DAR ∆, DAR corr columns, the DAR≡l1_imbalance finding, the OFI |r|=0.019 claim (pre-a12 provenance), and — as printed — the 8.4 gradient ratios (which are DAR values mislabeled "Simple LR").

Scope note on interpretation (stated precisely, not adjudicated): a corrupted `flow_5s` is still a deterministic monotone transform dominated by per-5s sell-trade counts, so the LogReg/LightGBM AUCs computed from it are well-defined numbers — the defect means they do not measure what the paper says they measure (signed order-flow/OFA content), not necessarily that the AUC magnitudes are inflated or deflated in a known direction. Determining the sign/size of the error requires execution, which is outside this item's boundaries.
