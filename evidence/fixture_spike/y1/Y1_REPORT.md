# Item Y1 — MBO COLUMN-UNIVERSE CHECK

**Analysis and reporting only. No prior artifact was edited.** The archive
(`C:\Users\ttbea\OneDrive\Desktop\MBO_2025`) and the prereg repo were read only; every write
went to
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\y1\`.
No detector code was read or written; no development-corpus file was touched. All line numbers
are 1-indexed; all quotes are verbatim (leading indentation stripped).

**Deliverables**

| File | Contents |
|---|---|
| `y1\column_universe.csv` | the 35-row source table (§2) |
| `y1\trade_class_only_map.csv` | 96 rows = 48 instrument-months × 2 sides, trade-class-only vs declared-10 maxima (§6.1) |
| `y1\Y1_REPORT.md` | this file |
| `y1\y1_column_universe.py`, `y1\y1_trade_class_map.py` | the two generators (re-runnable, read-only over the archive and over `n1\declared_map.csv`) |
| `y1\y1_column_universe_output.txt`, `y1\y1_trade_class_map_output.txt` | their raw stdout |

---

## 0. THE ANSWER

**OUTCOME (a): no column of the fixture's 35-column model set is fed by MBO event data.**

`phase7_l2_sim.py` opens exactly two data files — a snapshots parquet and a trades_tagged
parquet — and never opens an MBO parquet or an MBO aggregate. All 35 columns of
`ALL_L2_FEATURES` trace to one of: snapshot parquet (13), trades_tagged parquet (11),
snapshot-derived (9), the row's own clock (1), or snapshot+trades mixed (1). MBO-fed: **0**.

**Two things follow, and they point in opposite directions:**

1. The six `mbo_*` map classes attach to **no fed column**. They cannot be quoted as evidence
   about any column the fixture contains.
2. **The published strict headline does not move.** Restricted to the four trade classes, the
   corrected side is non-zero on strict in **18 of 48** instrument-months — **the same 18 cells**
   as the published all-class figure. Only the *equal* arithmetic collapses: 35/48 → **11/48**
   non-zero, 17 equal-only → **2** equal-only. And **N = 11 is unchanged** — no REQUIRED column
   is MBO-fed, which §A.6.1 of the declaration already states at lines 839-842.

---

## 1. `phase7_l2_sim.py` READ IN FULL — COMPLETE FILE-IO ENUMERATION

**File:** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py`
— 949 lines of code + trailing newline (read in full, lines 1-950 as presented by the reader).
`find` over the whole archive for `*phase7*` `.py` returns **exactly this one path** (re-verified
this pass; agrees with C2 and with `f3\fixture_manifest_DRAFT.json` `feature_set_provenance.script_mtime`).

### 1.1 Every path construction, read, and write

Grep pattern `read_table|ParquetFile|read_parquet|read_csv|iter_batches|open\(|to_parquet|to_csv|\.parquet|\.exists\(\)|Path\(|/ f"` over the whole file yields **every** line below and nothing else.

| Line | Verbatim | Direction |
|---|---|---|
| 23 | `import pyarrow.parquet as pq` | (import) |
| 32 | `PROJECT = Path(r"C:\Users\Research\Desktop\pc2_transfer")` | root |
| 135 | `sp = data_dir / f"{sym}_snapshots_{month}.parquet"` | **READ path #1** |
| 136 | `if not sp.exists():` | existence test |
| 139 | `snap = pq.read_table(str(sp)).to_pandas()` | **READ #1 — snapshots** |
| 199 | `tp = data_dir / f"{sym}_trades_tagged_{month}.parquet"` | **READ path #2** |
| 200 | `if tp.exists():` | existence test |
| 201 | `trades = pq.read_table(str(tp)).to_pandas()` | **READ #2 — trades_tagged** |
| 715 | `pred_path = PRED_DIR / f"{sym}_{arch}_{hz}_predictions_fixed.parquet"` | WRITE path |
| 716 | `result["pred_df"].to_parquet(str(pred_path), index=False)` | WRITE |
| 764 | `df_checkpoint.to_csv(str(results_path), index=False)` | WRITE (`simulation_results_pc2_fixed.csv`, L674) |
| 787 | `df_results.to_csv(str(results_path), index=False)` | WRITE |
| 815 | `with open(str(comp_path), "w") as f:` | WRITE (`pc2_phase7_complete.txt`, L814) |
| 913 | `df.to_csv(str(out_path), index=False)` | WRITE (`phase6_l2_fixed_pc2.csv`, L912) |

`data_dir` is fixed at L132: `data_dir = PROC / sym`, with `PROC = PROJECT / "processed"` (L33).
There is no `LOCAL_DATA` fallback and no `get_data_dir` helper, unlike the Phase 5 builder.

**There are exactly two data reads and neither is MBO.** `json` is imported at L14 and never
called; there is no config read, no feature-builder import, and no side-channel. `build_features_month`
is defined locally at L127-279.

### 1.2 The script says so itself

- L4 (module docstring): `L2 features only (no L3/MBO cancel/add/rate features).`
- L57 (section banner): `# L1 + L2 FEATURE DEFINITIONS (35 total, NO L3/MBO features)`
- L128 (function docstring): `"""Build L1+L2 features for one month. NO L3/MBO features."""`
- L108: `ALL_L2_FEATURES = L1_FEATURES + L2_FEATURES  # 35 total`
- L549 (pilot assertion): `assert len(features) == 35, f"FAIL: expected 35 features, got {len(features)}"`

**C2's finding is CONFIRMED, not refuted.** C2 row 16 states: *"ABSENT — docstring L4: `L2 features only (no L3/MBO cancel/add/rate features).` No MBO file is opened anywhere in phase7_l2_sim.py"*. The full read reproduces that exactly.

### 1.3 The R3 caveat — stated plainly

**This answer rests on the archived PC2 variant as the best available evidence.** The fixture's
ACTUAL prediction pair — `results\phase7\l2_predictions\` (pre-fix) vs
`results\phase7_fixed\l2_predictions\` (post-fix) — was produced by **main-PC variants of this
script that are ABSENT from the archive**. That the 35-column set is the fixture's column
universe is **working resolution R3, documented-unverifiable**, not a byte-verified fact about
the generators of the stored pair. §4 below sets out what the archive does and does not decide
about those two sides.

**What would change this answer:**

1. **Recovery of either main-PC generator script.** If a main-PC `phase7_l2_sim.py` (or whatever
   it was named — no such file exists in the archive) defines an `ALL_L2_FEATURES` containing any
   `bid_add_rate_*` / `ask_add_rate_*` / `bid_cancel_rate_*` / `ask_cancel_rate_*` /
   `cancel_ratio_asymmetry` / `order_flow_accel`, or calls a `load_mbo_aggregated`, the outcome
   flips to (b) for the side that script produced.
2. **A stored feature-name list for the 8-instrument runs.** `train_predict` returns
   `"features_used": features` (L419) but nothing in `results\phase7*` persists it: neither
   `l2_model_meta.csv` (columns `instrument,architecture,horizon_s,test_auc,shuffle_mean,n_test`)
   nor `l2_sim_results.csv` nor the `paper_tables` carries a feature column or count. If a
   feature-name list for those runs surfaces, it decides §4 directly.
3. **A feature-importance or model dump** for any of the 128 stored prediction files naming an
   MBO column.
4. Nothing in the *stored predictions themselves* can decide it: the prediction parquets carry
   `timestamp, pred_score, true_label, mid_price_t, fwd_move_ticks` (L402-408) — no feature columns.

---

## 2. THE 35-COLUMN SOURCE TABLE

Full machine-readable version: **`y1\column_universe.csv`** (columns: `ordinal, column,
feature_block, source_class, raw_source_traced, parent_columns, mbo_fed,
construction_line_numbers, construction_line_quote, upstream_line_numbers`). Order is
`ALL_L2_FEATURES` order = `L1_FEATURES` (L73-83) then `L2_FEATURES` (L96-106).

**Source-class tally: snapshot parquet 13 · trades parquet 11 · derived-from-another-column 9 ·
clock-only 1 · MIXED (snapshot + trades) 1 · MBO parquet 0.**

| # | Column | Source (traced to raw) | Construction line quote | Line(s) |
|---|---|---|---|---|
| 1 | `mid_return_1s` | snapshot parquet: `mid_price` | `for lag in [1, 5, 10, 30]:` / `snap[f"mid_return_{lag}s"] = mid.pct_change(lag)` | 152-153 |
| 2 | `mid_return_5s` | snapshot parquet: `mid_price` | same loop, lag=5 | 152-153 |
| 3 | `mid_return_10s` | snapshot parquet: `mid_price` | same loop, lag=10 | 152-153 |
| 4 | `mid_return_30s` | snapshot parquet: `mid_price` | same loop, lag=30 | 152-153 |
| 5 | `tick_direction` | snapshot parquet: `mid_price` | `snap["tick_direction"] = np.sign(mid.pct_change(1)).fillna(0)` | 156 |
| 6 | `trade_volume_1s` | **trades parquet**: `size` | `snap["trade_volume_1s"] = snap["trade_volume"].fillna(0)` | 246 |
| 7 | `trade_count_1s` | **trades parquet**: `size` | `snap["trade_count_1s"] = snap["trade_count"].fillna(0)` | 247 |
| 8 | `dollar_volume_1s` | **trades parquet**: `size`, `price` | `snap["dollar_volume_1s"] = snap["dollar_volume"].fillna(0)` | 248 |
| 9 | `minutes_since_open` | **clock-only** (snapshot `timestamp`) | `snap["minutes_since_open"] = (snap["hour_utc"] - ds) * 60 + snap["timestamp"].dt.minute` | 159 |
| 10 | `session_open` | derived ← `minutes_since_open` → clock-only | `snap["session_open"] = (frac < 0.1).astype(float)` | 162 |
| 11 | `session_mid` | derived ← `minutes_since_open` → clock-only | `snap["session_mid"] = ((frac >= 0.1) & (frac < 0.85)).astype(float)` | 163 |
| 12 | `session_close` | derived ← `minutes_since_open` → clock-only | `snap["session_close"] = (frac >= 0.85).astype(float)` | 164 |
| 13 | `net_delta_1s` | **trades parquet**: `aggressor_side`, `size` | `for w in [1, 5, 10, 30, 60]:` / `snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()` | 238-239 |
| 14 | `net_delta_5s` | **trades parquet** | same loop, w=5 | 238-239 |
| 15 | `net_delta_10s` | **trades parquet** | same loop, w=10 | 238-239 |
| 16 | `net_delta_30s` | **trades parquet** | same loop, w=30 | 238-239 |
| 17 | `net_delta_60s` | **trades parquet** | same loop, w=60 | 238-239 |
| 18 | `buy_volume_10s` | **trades parquet**: `aggressor_side`, `size` | `snap["buy_volume_10s"] = snap["buy_volume"].rolling(10, min_periods=1).sum()` | 240 |
| 19 | `sell_volume_10s` | **trades parquet**: `aggressor_side`, `size` | `snap["sell_volume_10s"] = snap["sell_volume"].rolling(10, min_periods=1).sum()` | 241 |
| 20 | `large_trade_count_10s` | **trades parquet**: `size` | `snap["large_trade_count_10s"] = snap["large_trade_count"].rolling(10, min_periods=1).sum()` | 242 |
| 21 | `vwap_distance` | **MIXED**: snapshot `mid_price` + trades `price`,`size` | `snap["vwap_distance"] = (mid - snap["vwap"]) / tick` | 243 |
| 22 | `bid_size_1` | snapshot parquet (raw pass-through) | `snap = pq.read_table(str(sp)).to_pandas()` (no construction statement; first use L174) | 139 |
| 23 | `ask_size_1` | snapshot parquet (raw pass-through) | `snap = pq.read_table(str(sp)).to_pandas()` (first use L174) | 139 |
| 24 | `total_bid_depth` | snapshot parquet: `bid_size_1..5` | `snap["total_bid_depth"] = snap[bid_cols].sum(axis=1)` | 169 |
| 25 | `total_ask_depth` | snapshot parquet: `ask_size_1..5` | `snap["total_ask_depth"] = snap[ask_cols].sum(axis=1)` | 170 |
| 26 | `book_imbalance_ratio` | derived ← `total_bid_depth`,`total_ask_depth` → snapshot | `snap["book_imbalance_ratio"] = (snap["total_bid_depth"] /` / `snap["total_ask_depth"].replace(0, np.nan)).fillna(1.0)` | 188-189 |
| 27 | `weighted_mid` | snapshot parquet: `bid_price_1`,`ask_price_1`,`bid_size_1`,`ask_size_1`,`mid_price` | `snap["weighted_mid"] = (snap["bid_price_1"] * snap["ask_size_1"] +` … / `snap["weighted_mid"] = (snap["weighted_mid"] - mid) / tick` | 184-187 |
| 28 | `spread_ticks` | snapshot parquet: `spread` | `snap["spread_ticks"] = snap["spread"] / tick` | 142 |
| 29 | `depth_imbalance` | derived ← `total_bid_depth`,`total_ask_depth` → snapshot | `snap["depth_imbalance"] = ((snap["total_bid_depth"] - snap["total_ask_depth"]) /` / `td.replace(0, np.nan)).fillna(0)` | 172-173 |
| 30 | `book_slope_bid` | snapshot parquet: `bid_size_1..5` | `snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb - 1, 1) if nb >= 2 else 0.0` | 178 |
| 31 | `book_slope_ask` | snapshot parquet: `ask_size_1..5` | `snap["book_slope_ask"] = (snap["ask_size_1"] - snap[ask_cols[-1]]) / max(na - 1, 1) if na >= 2 else 0.0` | 179 |
| 32 | `depth_change_1s` | derived ← `total_bid_depth`,`total_ask_depth` → snapshot | `for lag in [1, 5, 30]:` / `snap[f"depth_change_{lag}s"] = td.diff(lag)` | 180-181 |
| 33 | `depth_change_5s` | derived ← same | same loop, lag=5 | 180-181 |
| 34 | `depth_change_30s` | derived ← same | same loop, lag=30 | 180-181 |
| 35 | `l1_imbalance` | derived ← `bid_size_1`,`ask_size_1` → snapshot | `snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /` / `(snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)).fillna(0)` | 174-175 |

### 2.1 Tracing notes for the derived columns

- **`session_open/mid/close` (10-12)** are functions of `frac` (L161 `frac = snap["minutes_since_open"] / total_minutes`, L160 `total_minutes = (de - ds) * 60`), which is a function of `minutes_since_open` (L159), which is a function of the row's own `timestamp` and `hour_utc` (L144 `snap["hour_utc"] = snap["timestamp"].dt.hour`) plus the `INST_META` constants. **Raw root: the clock.** No market data.
- **`book_imbalance_ratio`, `depth_imbalance`, `depth_change_{1,5,30}s` (26, 29, 32-34)** all reduce to `td` (L171 `td = snap["total_bid_depth"] + snap["total_ask_depth"]`) ← L169/L170 ← `bid_cols`/`ask_cols` (L167-168, `bid_size_1..5`/`ask_size_1..5`). **Raw root: snapshot parquet.**
- **`l1_imbalance` (35)** ← `bid_size_1`,`ask_size_1`, raw snapshot columns. **Raw root: snapshot parquet.**
- **The trade-derived eleven (6-8, 13-20)** all reduce to the single `groupby("ts_floor")` at L216-226 over the trades_tagged frame read at L201, merged at L231 (`snap = snap.merge(tagg, on="ts_floor", how="left")`). The in-trades intermediates are L209 `signed_vol`, L210 `buy_vol`, L211 `sell_vol`, L212 `is_large`, L214 `dollar_vol`, with the aggressor test at L207-208. **Raw root: trades_tagged parquet.**
- **`vwap_distance` (21) is the only genuinely MIXED column.** Its `mid` term is the snapshot `mid_price` (L149 `mid = snap["mid_price"].replace(0, np.nan)`); its `vwap` term is the trades aggregate (L224-225 groupby lambda over `price` weighted by `size`, forward-filled at L235 `snap["vwap"] = snap["vwap"].ffill()`). This matches §A.6.1's note at declaration line 835: *"`vwap_distance` is REQUIRED for its `vwap` term, not for its `mid` term."*
- **`bid_size_1` / `ask_size_1` (22-23)** have **no construction statement at all** — they are raw snapshot columns that survive into the model set unmodified. Note the lag-exemption at L268-272 covers `bid_size_2..5` / `ask_size_2..5` only (`{f"bid_size_{i}" for i in range(2, 6)}`), so `bid_size_1`/`ask_size_1` **are** shifted by L276.

### 2.2 Agreement with the two draft manifests

`f3\fixture_manifest_DRAFT.json` `columns` (35 entries) and `t4\fixture_manifest_35col_DRAFT.json`
enumerate the same 35 names. Every `construction_source` in `f3` agrees with the line numbers
above. **`f3` classifies by leak-flavour (LEAK-SOURCE / DESCENDANT / CLEAN); this table classifies
by raw data source.** They are orthogonal axes and neither contradicts the other. Neither
manifest lists any MBO source for any of the 35.

---

## 3. CROSS-CHECK AGAINST THE PHASE 5 BUILDER

`f2\phase5_ml_fixture.py` (byte-verified copy of `phase5_ml.py`) **does** read MBO:

- L112-174 `def load_mbo_aggregated(sym, month):`
- L113 `agg_path = LOCAL_DATA / f"{sym}_mbo_agg" / f"{sym}_mbo_agg_{month}.parquet"`
- L118 `path = get_data_dir(sym) / f"{sym}_mbo_{month}.parquet"`
- L156 `df = pq.read_table(str(path), columns=["ts_event","action","side"]).to_pandas()`
- L270 `magg = load_mbo_aggregated(sym, month)`; L276 `snap = snap.merge(magg, on="ts_floor", how="left")`
- L279-283 `for w in [5, 10]:` / `snap[f"bid_add_rate_{w}s"] = snap["bid_adds"].rolling(w, min_periods=1).sum()` (and the ask-add, bid-cancel, ask-cancel analogues)
- L285-286 `snap["cancel_ratio_asymmetry"] = ((snap["bid_cancel_rate_10s"] - snap["ask_cancel_rate_10s"]) /` / `tc10.replace(0, np.nan)).fillna(0)`
- L287-288 `snap["event_rate_10s"] = snap["total_events"].rolling(10, min_periods=1).sum()` / `snap["order_flow_accel"] = snap["event_rate_10s"].diff(5)`

`FULL_FEATURES` (L63-83) has **45** names, of which **10 are MBO-derived** (L78-82).

### 3.1 Membership check — how many of the 10 appear in `ALL_L2_FEATURES`?

**ZERO.** `ALL_L2_FEATURES = L1_FEATURES + L2_FEATURES` (L108) and the two lists are quoted here
in full so the check is auditable:

> **L73-83:**
> ```
> L1_FEATURES = [
>     "mid_return_1s", "mid_return_5s", "mid_return_10s", "mid_return_30s",
>     "tick_direction",
>     "trade_volume_1s", "trade_count_1s", "dollar_volume_1s",
>     "minutes_since_open",
>     "session_open", "session_mid", "session_close",
>     "net_delta_1s", "net_delta_5s", "net_delta_10s", "net_delta_30s", "net_delta_60s",
>     "buy_volume_10s", "sell_volume_10s",
>     "large_trade_count_10s",
>     "vwap_distance",
> ]
> ```
>
> **L96-106:**
> ```
> L2_FEATURES = [
>     "bid_size_1", "ask_size_1",
>     "total_bid_depth", "total_ask_depth",
>     "book_imbalance_ratio",
>     "weighted_mid",
>     "spread_ticks",
>     "depth_imbalance",
>     "book_slope_bid", "book_slope_ask",
>     "depth_change_1s", "depth_change_5s", "depth_change_30s",
>     "l1_imbalance",
> ]
> ```

Neither list contains `bid_adds`, `ask_adds`, `bid_cancels`, `ask_cancels`, `total_events`,
`event_rate_10s`, or any `*_add_rate_*` / `*_cancel_rate_*` / `cancel_ratio_asymmetry` /
`order_flow_accel`.

### 3.2 THE DROPPED MBO-COLUMN LIST — the 35-set drops ALL of them

**All 10 MBO-derived Phase 5 columns are dropped by the 35-column set:**

| # | Dropped column | Phase 5 construction (f2 copy) |
|---|---|---|
| 1 | `bid_add_rate_5s` | L280 `snap[f"bid_add_rate_{w}s"] = snap["bid_adds"].rolling(w, min_periods=1).sum()`, w=5 |
| 2 | `ask_add_rate_5s` | L281, w=5 |
| 3 | `bid_cancel_rate_5s` | L282, w=5 |
| 4 | `ask_cancel_rate_5s` | L283, w=5 |
| 5 | `bid_add_rate_10s` | L280, w=10 |
| 6 | `ask_add_rate_10s` | L281, w=10 |
| 7 | `bid_cancel_rate_10s` | L282, w=10 |
| 8 | `ask_cancel_rate_10s` | L283, w=10 |
| 9 | `cancel_ratio_asymmetry` | L285-286 |
| 10 | `order_flow_accel` | L288 (via `event_rate_10s` L287) |

**Nine further Phase 5 columns are also dropped** (non-MBO, listed for completeness because the
45→35 delta is not "45 minus 10"): `mid_return_60s`, `mid_return_300s`, `volatility_30s`,
`volatility_300s`, `range_60s`, `range_300s`, `depth_pctile_60s`, `depth_pctile_300s`,
`trade_count_10s`. **19 dropped in total**, matching `f3\fixture_manifest_DRAFT.json`
`counts.not_fed_to_phase7: 19` and its 19-entry `not_fed_to_phase7_models` array.

**And nine columns are ADDED that the 45-set never had:** `tick_direction`, `trade_volume_1s`,
`trade_count_1s`, `dollar_volume_1s`, `session_open`, `session_mid`, `session_close`,
`book_imbalance_ratio`, `weighted_mid`. Arithmetic: 45 − 19 = 26 shared, 26 + 9 = **35**. This
reproduces `f3`'s `relation_to_phase5_full_features` (`shared_with_45_set: 26`,
`phase7_only_not_in_45_set` = those nine).

> **Consequence, stated explicitly:** the 35-set is **not** Phase 5's `BOUNCE_FREE_FEATURES`
> (L91 `BOUNCE_FREE_FEATURES = [f for f in FULL_FEATURES if f not in PRICE_LAG_FEATURES]`, which
> is also 35 long but **keeps all 10 MBO columns** and drops the 10 price-lag ones instead).
> Any reasoning that treats "the 35-set" as the bounce-free set would reach the opposite MBO
> conclusion. The sets are disjoint in exactly the way that matters here.

---

## 4. THE ASYMMETRY QUESTION

### 4.1 What the two sides of the ACTUAL gate fixture are

The gate fixture is the stored prediction pair:

- **pre-fix side:** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase7\l2_predictions\` — **64 parquets**, 8 instruments (`cl, es, gc, he, le, nq, zc, zs`) × 2 architectures × 4 horizons, named `{sym}_{arch}_{h}s_predictions.parquet`.
- **post-fix side:** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\phase7_fixed\l2_predictions\` — **64 parquets**, the **same 64 filenames**.

**Both sides were produced by phase7-family code, and NEITHER was produced by the archived PC2
script.** The archived script writes `f"{sym}_{arch}_{hz}_predictions_fixed.parquet"` (L715) —
no `s` after the horizon, and a `_fixed` suffix. Neither stored directory uses that pattern. The
archived PC2 outputs live elsewhere, in `results\pc2_all_phases\phase7\l2_predictions\`, where
both `gc_LightGBM_5_predictions.parquet` and `gc_LightGBM_5_predictions_fixed.parquet` patterns
appear.

**The archived pre-fix phase7 variant is ABSENT — and so is the archived post-fix variant for
the 8-instrument runs.** `find` for `*phase7*.py` over the whole archive returns one file, the
PC2 post-fix script. So on the asymmetry question the archive gives no code for **either** side
of the actual pair.

### 4.2 What the archive DOES decide

**(i) Both sides are documented, in prose, as the same no-MBO feature family — and the two
documents are byte-identical.**

`results\phase7\methodology_note.txt` and `results\phase7_fixed\methodology_note.txt` have the
**same SHA256** `ea11e0ffd382167d8209259a6847234c9dd99c7345ea29e801dbc8d0ee113535`, and both open:

> `Phase 7 trading simulation uses models retrained on L1+L2 features only`
> `(order book and trade flow, no MBO data).`

**(ii) The `l2_*` output family carries no `feature_set` column, unlike the 45-set family.**
`results\phase7\l2_sim_results.csv` and `results\phase7_fixed\l2_sim_results.csv` share the header
`n_trades,win_rate,mean_gross_pnl,mean_net_pnl,total_net_pnl,sharpe,max_drawdown,breakeven_wr,mean_abs_move,instrument,architecture,horizon_s,threshold,entry_type,cost_ticks`
— **no `feature_set`**. By contrast `results\phase7\full_sim_results.csv`,
`results\phase7\main_pc_results.csv` and `results\phase7\pilot_main.csv` all **do** carry
`feature_set` (values `Full` / `BFree`, the Phase 5 45-column families). A single feature set on
both `l2_` sides is exactly what a missing `feature_set` column implies.

**(iii) The PC2 sibling pair — for which BOTH completion records survive — is 35-column,
no-MBO on BOTH sides.**

- pre-fix, `results\pc2_all_phases\phase7\pc2_complete.txt`, `timestamp: 2026-04-11T19:56:59`:
  `feature_set: L2 (35 features, 21 L1 + 14 L2)`
- post-fix, `results\pc2_all_phases\phase7\pc2_phase7_complete.txt`, `timestamp: 2026-04-12T14:02:53`:
  `feature_set: L1+L2 (35 features, universal lag)`

This is the closest thing the archive has to a controlled answer: on the one phase7 pre/post pair
whose provenance IS recorded, **both sides are 21 L1 + 14 L2 = 35, no MBO**, and the only
difference recorded is the universal lag.

**(iv) The pre-fix AUCs quoted in the fix documentation are the stored pre-fix side's own
numbers, and that document calls them "L2 features".**
`results\phase7\universal_lag_finding.txt` L41 heads its table
`Pre-fix AUCs (L2 features, LightGBM, 5s horizon):` and lists ZC 0.9662, ZS 0.9527, CL 0.8224,
GC 0.7077, HE 0.6385, LE 0.5848, NQ 0.5420 — **all seven reproduce exactly** in
`results\phase7\l2_model_meta.csv` (`ZC,LightGBM,5,0.9662`; `ZS,LightGBM,5,0.9527`;
`CL,LightGBM,5,0.8224`; `GC,LightGBM,5,0.7077`; `HE,LightGBM,5,0.6385`; `LE,LightGBM,5,0.5848`;
`NQ,LightGBM,5,0.542`). So the pre-fix stored side IS the "L2 features" run that document
describes. (Its eighth row, `ES 0.6017`, has no exact match: the pre-fix meta has 63 rows, and
`ES,LightGBM,5` is the one missing model; `ES,XGBoost,5` is 0.602. A one-row labelling slip in a
prose document, noted for completeness, not load-bearing.)

**(v) The L2-fix note enumerates the 14 L2 names and they are exactly `L2_FEATURES`.**
`results\pc2_all_phases\phase7\l2_leakage_finding.txt` `L2_LAG_COLS = [...]` lists
`bid_size_1, ask_size_1, total_bid_depth, total_ask_depth, l1_imbalance, depth_imbalance,
book_imbalance_ratio, book_slope_bid, book_slope_ask, weighted_mid, spread_ticks,
depth_change_1s, depth_change_5s, depth_change_30s` — the same 14 as L96-106, same membership.

### 4.3 What the archive does NOT decide

- **No code for either side of the actual pair.** Everything in §4.2 is prose, filename
  convention, and family analogy. None of it is a feature list emitted by the generator.
- **`results\phase7_fixed\l2_overnight_complete.txt` does not account for its own directory.**
  It records `Instruments: ['GC', 'NQ', 'ZC', 'ZS']` and `Models trained: 32`, yet
  `phase7_fixed\l2_predictions\` holds 64 parquets across 8 instruments, and
  `phase7_fixed\l2_model_meta.csv` holds **32** rows covering only GC/NQ/ZC/ZS. **No archived
  record accounts for the CL/ES/HE/LE files on the post-fix side.** (This reproduces the
  DISCREPANCY already flagged in `f3\fixture_manifest_DRAFT.json`
  `feature_set_provenance.stored_prediction_sets.main_8inst_postfix`.) On the pre-fix side the
  count mismatch runs the other way: 64 prediction files, 63 meta rows, 63 models trained.
- **Therefore the post-fix side's CL/ES/HE/LE predictions have no provenance record at all** —
  not a script, not a completion file, not a meta row.

### 4.4 VERDICT ON THE ASYMMETRY

**Stated plainly: on the best available evidence the two sides of the actual gate fixture share
one column universe — 35 columns, no MBO — but this is an INFERENCE from prose and structure,
not a code-verified fact, and it is exactly working resolution R3.**

- The claim "**both** sides are 35-column, no-MBO" is supported by: byte-identical methodology
  notes on both sides saying "no MBO data"; the absence of a `feature_set` column in the `l2_`
  family on both sides; the PC2 sibling pair recording 35 no-MBO on both sides; and the
  pre-fix AUC table matching the stored pre-fix meta under the heading "L2 features".
- The claim is **not** established by any archived generator. Both generators are absent.
- **The "pre-fix = phase5_ml.py build_features_month (45 columns, MBO-reading)" framing in the
  declaration describes the PHASE 5 → PHASE 7 lineage, not the two sides of the stored pair.**
  Both sides of the stored pair are phase7-family `l2_` outputs. If the declaration's naming of
  the fixture's "two sides" is read as *the two sides of the stored prediction pair*, then naming
  the pre-fix side as a 45-column MBO-reading builder is **not supported by the archive** — the
  pre-fix stored side is the `l2_` family, whose own documentation says no MBO. This is a
  reporting-precision point for the author; it changes nothing about outcome (a), because under
  **either** reading no MBO column reaches the 35-column set the gate scores under R3.
- **What cannot be concluded:** that the pre-fix side was byte-for-byte the same feature list as
  the post-fix side; that CL/ES/HE/LE post-fix predictions came from the same run as GC/NQ/ZC/ZS;
  or that either side's generator lacked some column not in `ALL_L2_FEATURES`.

---

## 5. OUTCOME

### **(a) — no fixture column is MBO-fed.**

Decisive evidence, in descending order of strength:

1. **`phase7_l2_sim.py` opens exactly two data files** (L135/L139 snapshots, L199/L201
   trades_tagged) and no others. Complete IO enumeration in §1.1.
2. **`ALL_L2_FEATURES` (L108) contains none of the 10 MBO-derived Phase 5 columns.** Both member
   lists quoted in full in §3.1.
3. **The script asserts its own scope** at L4, L57, L128, and L549.
4. **Both sides of the stored pair are documented as "no MBO data"** in byte-identical
   methodology notes (§4.2(i)), and the PC2 sibling pair records 35 no-MBO on both sides (§4.2(iii)).

**Precision about what (a) means, given R3:** (a) is a statement about the **column universe the
gate scores under R3** — the 35-column set of `phase7_l2_sim.py`. It is not a byte-verified
statement about the absent main-PC generators. If R3 is ever retired in favour of a recovered
generator, this outcome must be re-derived against that generator's feature list.

---

## 6. CONSEQUENCES

### 6.1 The map's scored surface, restricted to the TRADE CLASSES ONLY

Re-derived from `n1\declared_map.csv` (984 rows; 8 instruments × 6 months × 2 sides × 10 declared
classes, plus 24 `mbo_all_rows` diagnostic rows which are excluded here as they are for the
published figure). Trade classes = `trades_all`, `trades_buy`, `trades_sell`, `trades_large`.
Per-cell figures are the **max over the class set**, counting only SCORED cells — the same
statistic the published headline uses, with the class set narrowed. Full output:
**`y1\trade_class_only_map.csv`**.

#### CORRECTED SIDE

| Statistic | Trade classes only (4) | Published, declared 10 | Difference |
|---|---|---|---|
| strict-positive instrument-months | **18 / 48** | 18 / 48 | **none** |
| `equal_count` non-zero instrument-months | **11 / 48** | 35 / 48 | **−24** |
| equal-only (equal > 0, strict = 0) | **2 / 48** | 17 / 48 | **−15** |
| zero-strict-and-zero-equal | **28 / 48** | 13 / 48 | **+15** |
| partition check | 18 + 2 + 28 = 48 | 18 + 17 + 13 = 48 | ✔ both |

**The 18 strict cells are IDENTICAL to the published 18** — cl ×6 (2025-01, -08, -09, -10, -11,
-12), gc ×6 (same six months), zc 2025-08/-09/-10, zs 2025-08/-09/-10. This is exactly the list
at `f4\availability_declaration_DRAFT.md` lines 1459-1460, verbatim: *"**cl all 6 months, gc all 6
months, zc 2025-08/-09/-10, zs 2025-08/-09/-10**"*. **Restricting the scored surface to the trade
classes does not move the strict headline at all.** (The published equal figures being restated
here are from line 1465: *"`equal_count` is non-zero in **35 of 48** instrument-months; of those,
**17 are equal-only**"*.)

**The 2 equal-only cells** are `es 2025-10` and `es 2025-11` (both `equal_count` = 1 on
`trades_all`/`trades_sell`). Under the declared 10 the equal-only set was 17 cells
(es ×6, he ×5, le ×5, zc 2025-12); the other 15 were carried by MBO classes alone.

**Per-instrument-month max strict / max equal, trade classes only** (all 48; zero rows condensed):

| instrument-month | trade-only strict | trade-only equal | declared-10 strict | declared-10 equal |
|---|---|---|---|---|
| cl 2025-01 | 21,770 | 0 | 53,249 | 2,194 |
| cl 2025-08 | 9,048 | 0 | 27,852 | 1,427 |
| cl 2025-09 | 10,803 | 1 | 34,010 | 1,388 |
| cl 2025-10 | 15,002 | 3 | 42,377 | 1,893 |
| cl 2025-11 | 15,345 | 0 | 48,607 | 1,680 |
| cl 2025-12 | 10,837 | 2 | 38,945 | 1,985 |
| gc 2025-01 | 13,907 | 3 | 37,065 | 1,853 |
| gc 2025-08 | 16,051 | 0 | 42,886 | 1,907 |
| gc 2025-09 | 25,862 | 0 | 59,691 | 2,053 |
| gc 2025-10 | 37,913 | 0 | 71,584 | 2,588 |
| gc 2025-11 | 12,764 | 1 | 30,577 | 1,686 |
| gc 2025-12 | 20,195 | 0 | 49,649 | 1,793 |
| zc 2025-08 | 23,755 | 3 | 90,868 | 2,857 |
| zc 2025-09 | 30,617 | 1 | 111,334 | 2,640 |
| zc 2025-10 | 34,492 | 2 | 109,332 | 2,873 |
| zs 2025-08 | 17,717 | 2 | 64,404 | 2,161 |
| zs 2025-09 | 10,382 | 0 | 45,255 | 2,281 |
| zs 2025-10 | 16,397 | 0 | 60,559 | 2,353 |
| es 2025-10 | 0 | 1 | 0 | 4 |
| es 2025-11 | 0 | 1 | 0 | 3 |
| es 2025-01/-08/-09/-12; he ×6; le ×6; nq ×6; zc 2025-01/-11/-12; zs 2025-01/-11/-12 (28 cells) | 0 | 0 | see CSV | see CSV |

**The peak moves and shrinks.** Published peak (declared 10): **zc 2025-09, 111,334 strict of
580,944 rows = 19.16%**, on class `mbo_all`. **Trade-class-only peak by fraction: zc 2025-10,
34,492 / 634,445 = 5.44%**; by absolute count: **gc 2025-10, 37,913 / 772,447 = 4.91%**. Top six
by fraction, trade-only vs declared-10 on the same cell:

| cell | trade-only strict | frac | declared-10 strict | frac |
|---|---|---|---|---|
| zc 2025-10 | 34,492 / 634,445 | 5.44% | 109,332 | 17.23% |
| zc 2025-09 | 30,617 / 580,944 | 5.27% | 111,334 | 19.16% |
| gc 2025-10 | 37,913 / 772,447 | 4.91% | 71,584 | 9.27% |
| zc 2025-08 | 23,755 / 554,303 | 4.29% | 90,868 | 16.39% |
| zs 2025-08 | 17,717 / 465,381 | 3.81% | 64,404 | 13.84% |
| gc 2025-09 | 25,862 / 734,280 | 3.52% | 59,691 | 8.13% |

#### CONTAMINATED SIDE

| Statistic | Trade classes only (4) | Published, declared 10 | Difference |
|---|---|---|---|
| strict-positive instrument-months | **48 / 48** | 48 / 48 | **none** |
| `equal_count` non-zero | **23 / 48** | 42 / 48 | **−19** |
| equal-only | 0 / 48 | 0 / 48 | none |
| zero-zero | 0 / 48 | 0 / 48 | none |

**The contaminated-side saturation claim survives the restriction intact: 48 of 48 remain
strict-positive on trade classes alone.** Only the equal arithmetic thins (42 → 23). Peak
fractions barely move on nq (identical, because nq's MBO classes are unscored: nq 2025-01
543,341 / 598,228 = 90.83% under both class sets) and drop on es (es 2025-01: 84.97% trade-only
vs 96.80% declared-10).

#### Which trade class carries the non-zeros

| side | `trades_all` | `trades_buy` | `trades_sell` | `trades_large` |
|---|---|---|---|---|
| corrected — strict > 0 | 18 cells | **0 cells** | 18 cells | 18 cells |
| corrected — equal > 0 | 11 cells | **0 cells** | 11 cells | 1 cell |
| contaminated — strict > 0 | 48 cells | **0 cells** | 48 cells | 48 cells |
| contaminated — equal > 0 | 23 cells | **0 cells** | 23 cells | 8 cells |

`trades_buy` is **identically zero in all 96 of its cells on both sides** — the dead-zero
consequence of the aggressor-literal mismatch recorded at §A.6.3 / §C.4(a) of the declaration
and at C2's degeneracy verdict. So the trade-class-only surface is effectively carried by three
live classes, not four.

#### The difference, stated plainly

> **The strict headline is unchanged: 18 of 48 on the corrected side and 48 of 48 on the
> contaminated side hold over the trade classes alone.** The all-class figure was never carrying
> the strict result on the MBO classes' back. **What the MBO classes were carrying is the EQUAL
> arithmetic:** corrected equal-non-zero falls 35 → 11 and equal-only falls 17 → 2; contaminated
> equal-non-zero falls 42 → 23. And the *magnitudes* fall roughly threefold on the corrected side
> (peak 19.16% → 5.44%). **Any statement of the form "35 of 48" or "17 equal-only", and any
> quoted maximum, is an all-class statement whose class set includes six classes that feed no
> fed column.** It should be quoted with the class set named — which the declaration's own
> §13(a) boxed rule already requires ("Any statement of the form 'max across classes' … must
> name the class set it maximises over").

### 6.2 R11's partition — does N change?

**Check performed: is ANY of the 11 REQUIRED columns of §A.6.1 / §D.1 MBO-fed?**

| # | REQUIRED column | Source per `y1\column_universe.csv` | MBO-fed? |
|---|---|---|---|
| 1 | `net_delta_1s` | trades parquet (L238-239 ← L217 ← L209 ← L201) | NO |
| 2 | `net_delta_5s` | trades parquet | NO |
| 3 | `net_delta_10s` | trades parquet | NO |
| 4 | `net_delta_30s` | trades parquet | NO |
| 5 | `net_delta_60s` | trades parquet | NO |
| 6 | `sell_volume_10s` | trades parquet (L241 ← L219 ← L211) | NO |
| 7 | `large_trade_count_10s` | trades parquet (L242 ← L222 ← L212) | NO |
| 8 | `vwap_distance` | MIXED snapshot + trades (L243; `vwap` from L224-225/L235) | NO |
| 9 | `trade_volume_1s` | trades parquet (L246 ← L221) | NO |
| 10 | `trade_count_1s` | trades parquet (L247 ← L220) | NO |
| 11 | `dollar_volume_1s` | trades parquet (L248 ← L214/L223) | NO |

**N IS UNCHANGED. N = 11.** Re-derived against the columns the fixture actually contains: all
eleven REQUIRED columns are present in the 35-column set, all eleven are trades-parquet-fed
(number 8 partly snapshot-fed for its `mid` term), and **none is MBO-fed**. The full partition
also holds unchanged:

| Class | Count | Any MBO-fed member? |
|---|---|---|
| REQUIRED (§A.6.1) | **11** | none |
| OUT OF JURISDICTION (§A.6.2) — 4 clock-only + 18 same-row reads | **22** | none |
| UNSCORED (§A.6.3) — `buy_volume_10s`, `book_imbalance_ratio` | **2** | none |
| **Total** | **35** | **0 of 35** |

11 + 22 + 2 = 35. Cross-checked column by column against `y1\column_universe.csv`: every one of
the 35 is snapshot-fed, trades-fed, clock-only, snapshot-derived, or the one mixed column. **This
is a valuable null: the Y1 finding does not disturb R11's partition, its denominator, or any
criterion-1 arithmetic.**

**Consistency note — the declaration already says this.** §A.6.1's second honesty note, at
`f4\availability_declaration_DRAFT.md` lines 839-842, reads verbatim:

> **No MBO-derived column is in the list, and that is a scope fact, not an omission.** Phase 7
> feeds no MBO columns at all (§4's Phase 7 difference, §C.1's scope note), so the map's six
> `mbo_*` classes characterise the fixture's MBO stream against the lattice without attaching
> to any fed column. `trade_count_10s` is likewise absent because Phase 7 drops it.

And §A.6.3's cell-level limb, lines 889-892:

> **Cell-level: the 72 `UNSCORED_FOR_LACK_OF_DATA` map cells** (nq's six MBO classes x 6 months
> x 2 sides, §13(g), §13(h)). These are **cells, not columns**; because Phase 7 feeds no MBO
> column, none of the 35 fed columns is put into UNSCORED by them.

**Y1 independently confirms both statements by full read and by column-by-column source
tracing.** The declaration's partition needs no amendment on account of this item.

### 6.3 What the six MBO classes still legitimately evidence

**They still evidence, and may still be quoted for:**

- **Lattice-irregularity characterization.** The MBO event stream measured against the snapshot
  lattice is a real, measured property of the fixture's underlying data and of the wall-clock-second
  join geometry. §B.4's "the lattice is not a 1 Hz grid on 18 of 48 instrument-months" and the
  overhang measurements (worst overhang past `t-1` = 999.999579 ms on MBO classes vs 999.996869 ms
  on trades) are statements about the *stream and the lattice*, not about a fed column, and they
  stand.
- **Boundary-instant characterization of the fixture's source data**, i.e. how far past a
  claimed decision instant the wall-clock-second bucket reaches, measured on the densest
  available event stream. MBO is the densest stream, which is precisely why it yields the
  sharpest boundary measurement.
- **Corroboration of the join-family mechanism.** The same `ts_floor` forward-join geometry that
  produces the MBO overhang produces the trades overhang; the MBO measurement is a
  higher-resolution view of one mechanism, not a second mechanism.

**They must NO LONGER be quoted as:**

- **Evidence about any column the fixture contains.** No fed column reads MBO. An MBO class
  being strict-positive in a cell says nothing about whether any of the 35 columns is violating
  in that cell.
- **Contributors to the criterion-1 denominator or to any REQUIRED finding.** Already excluded
  by §A.6.1; Y1 confirms there is no route by which they could enter.
- **Part of an unqualified "the map declares violation in X of 48" headline.** Where the sentence
  is about the *fixture's fed columns*, the class set must be the four trade classes, giving
  18/48 strict corrected (unchanged) but **11/48 equal-non-zero and 2/48 equal-only** (not 35 and 17).
- **Part of an unqualified "max strict" or "max equal".** The published corrected peak
  (zc 2025-09, 111,334, 19.16%) is an `mbo_all` figure. The fed-column-relevant peak is
  zc 2025-10, 34,492, 5.44%.
- **Evidence that any column is or is not clean.** They attach to no column in either direction.

---

## 7. NQ / R12 INTERACTION — OBSERVATION ONLY, NOT A RESTATEMENT OF R12

*Recorded for the author. This is an observation that follows from outcome (a); it does not
restate, reopen, or amend R12, and it proposes no change to any locked text.*

Outcome (a) implies the six unscored NQ MBO classes are **vacuous for every instrument, not just
nq**. The 72 `UNSCORED_FOR_LACK_OF_DATA` cells are nq's six MBO classes × 6 months × 2 sides —
but under (a) the six MBO classes attach to no fed column for **any** of the eight instruments.
So nq's MBO gap and es/cl/gc/he/le/zc/zs's MBO *presence* are, with respect to the fixture's
column universe, the same thing: neither says anything about a column the fixture contains.

Three consequences the author may wish to weigh:

1. **The nq asymmetry disappears entirely once the class set is narrowed to the trade classes.**
   Under trade-class-only scoring every one of the 8 instruments is scored on exactly 4 of 4
   classes, in all 6 months, on both sides — `classes_scored` is uniform, and the
   `classes_scored = 4` vs `10` split that motivates the "TRADES-CLASSES-ONLY / NOT a pass"
   annotation on the six nq rows no longer distinguishes nq from anything else.
2. **The 13-cell measured-zero table becomes a 28-cell table**, and the reason a cell is in it
   becomes uniform (zero over the four trade classes) rather than mixed (zero over 10 for seven
   cells, zero over 4 for six nq cells). The six nq rows and, e.g., the zc 2025-01 row would then
   be zero for the same reason and over the same class set.
3. **None of this converts any measured-zero cell into a pass**, and nothing here licenses
   quoting nq as clean. The observation is that the *ground* for the current annotation shifts:
   under (a), the annotation's force comes from "MBO classes evidence nothing about fed columns"
   rather than from "nq is missing MBO data". Both hold; they are different reasons.

---

## 8. LIMITS OF THIS ITEM — what Y1 does NOT establish

1. **Y1 does not verify the generators of the stored prediction pair.** Both are absent (§4.1).
   The 35-column universe remains **working resolution R3, documented-unverifiable**.
2. **Y1 does not measure any data.** It is a static read of two scripts plus a re-aggregation of
   `n1\declared_map.csv`. No parquet was opened.
3. **Y1 does not revisit the aggressor-literal degeneracy** (C2 §"Degeneracy verdict"). That
   finding is orthogonal: `buy_volume_10s` is dead-zero and the `net_delta_*` family carries no
   buy/sell information, but all of those columns are trades-fed either way.
4. **Y1 does not re-derive the map.** The trade-class-only figures are a restriction of
   `n1\declared_map.csv` to a subset of its own classes, using the same per-cell max-over-classes
   statistic. Every number in §6.1 is reproducible by re-running `y1\y1_trade_class_map.py`.
5. **Y1 does not address the post-fix CL/ES/HE/LE provenance gap** (§4.3) beyond recording it.
   That gap is a pre-existing manifest DISCREPANCY, independently reproduced here.
