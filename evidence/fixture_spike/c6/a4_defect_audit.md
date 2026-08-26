# ITEM C6a — a4_runner.py (v4) + v5_lightgbm_runner.py defect audit

Static read audit. All paths absolute; all quotes verbatim with line numbers.
Audited files (read in full or in all cited ranges):

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py` (939 lines, read in full)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\bucket_assigner.py` (import; grepped — no trade-field string ops)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\g2_day_worker.py` (writer of the parquets a4 reads; read in full)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\g2_reprocess.py` (month concat; cited lines)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\flow_tagger.py` (tagger used by g2; lines 60-180)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\book_engine.py` (snapshot builder; lines 40-440)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_mbo.py` (he/le-era writer family; cited lines)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_lightgbm_runner.py` (294 lines, read in full) — **v5**
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_wave_runner.py` (feature-build section, lines 254-299) — **v5**

---

## VERDICT SUMMARY

| Defect | v4 (a4_runner.py) | v5 (v5_lightgbm_runner.py / v5_wave_runner.py) |
|---|---|---|
| Classifier (`isin(["B","Buy","buy"])` matching nothing) | **CORRECTED** — reads boolean `is_buy_aggressor` column; no string match on aggressor values anywhere | **CORRECTED** (identical by direct code reuse of a4_runner) |
| Dtype (uncast unsigned negation of `size`) | **CARRIED** — `np.where(cond, tr["size"], -tr["size"])` with no cast, on a `size` column that is never cast anywhere in its write/read chain | **CARRIED** (identical by direct code reuse of a4_runner) |

Deciding quotes below.

---

## (1) Aggressor-side classification

### v4 — what column is read, and how

`a4_runner.py` never loads or references `aggressor_side` (the string column with
`BUY_AGGRESSOR`/`SELL_AGGRESSOR`/`UNKNOWN`). It loads a **boolean** column
`is_buy_aggressor` explicitly:

`scripts\v4\a4_runner.py:218` (inside `load_trades`):
```python
df = pq.read_table(str(p), columns=["ts_event", "price", "size", "is_buy_aggressor"]).to_pandas()
```

and uses it as a boolean, never comparing against string literals:

`scripts\v4\a4_runner.py:307-309` (inside `add_trade_features`):
```python
tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
tr["buy_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], 0)
tr["sell_size"] = np.where(~tr["is_buy_aggressor"].astype(bool), tr["size"], 0)
```

### Is the boolean column real (does the split actually split)?

Yes. The parquets a4 reads carry `is_buy_aggressor` as a genuine boolean written
by the tagging implementations, alongside the string `aggressor_side`:

- For **es/nq/cl/gc/zc/zs** (v4_morning_chunk / v4_gapfill dirs, per
  `a4_runner.py:134-140 data_dir_for`): written by
  `scripts\v4\g2_day_worker.py:89` (`from flow_tagger import tag_aggressor`) →
  `g2_day_worker.py:192` (`trades = tag_aggressor(df, snapshots=None)`) →
  `g2_day_worker.py:195` (`trades.to_parquet(trades_out, ...)`), month-concat by
  `g2_reprocess.py:161-162` (`trade_df = pd.concat(trade_dfs, ignore_index=True)` /
  `trade_df.to_parquet(trades_out, index=False, engine="pyarrow")`).
  The tagger writes the boolean at
  `scripts\pipeline\flow_tagger.py:105`:
  ```python
  trades["is_buy_aggressor"] = trades["side"] == "B"
  ```
  (plus fallback assignments at lines 133/136/139 and `flow_tagger.py:145`:
  `trades.loc[still_na, "is_buy_aggressor"] = False`).

- For **he/le**: `data_dir_for` falls through (`a4_runner.py:140`:
  `return ROOT / "processed" / inst`), i.e., a4 reads the ORIGINAL-family
  parquets. Those writers also wrote the boolean, e.g.
  `scripts\pipeline\process_mbo.py:552`:
  ```python
  trades_df["is_buy_aggressor"] = trades_df["side"] == "B"
  ```
  and `scripts\pipeline\process_zc.py:95` (same statement; established context).

So the v4 buy/sell split is driven by a boolean that is True for genuine
buy-aggressor trades — the vacuous-`isin` defect is **not** present in any form.

**Classifier verdict (v4): CORRECTED.** Deciding quote: `a4_runner.py:307`
(boolean use) + `a4_runner.py:218` (column list excludes `aggressor_side`).

**Semantic caveat (not the audited defect):** UNKNOWN-side trades get
`is_buy_aggressor = False` (`flow_tagger.py:138-139` sets
`aggressor_side = "UNKNOWN"` with `is_buy_aggressor = False`; `flow_tagger.py:144-145`
same for still-NaN). In a4's construction, `sell_size` uses
`~is_buy_aggressor` (`a4_runner.py:309`), so UNKNOWN trades are counted as SELL
aggressors in `signed_size` and `sell_volume_10s`. This is a tagging design
choice inherited from the tagger, not a vacuous match.

### v5

`scripts\v5\v5_lightgbm_runner.py` performs **no trade construction of its
own** — it imports and reuses a4_runner byte-identically:

- `v5_lightgbm_runner.py:43`: `import a4_runner as r`
- `v5_lightgbm_runner.py:98`: `trades = r.load_trades(inst)`
- `v5_lightgbm_runner.py:106`: `feat = r.add_trade_features(feat, trades)`
- Its docstring states this (lines 3-6): "Reuses v4's a4_runner module
  byte-identically for: ... Feature engineering (build_snapshot_features,
  add_trade_features)".

`scripts\v5\v5_wave_runner.py` (batch driver) does the same:
`v5_wave_runner.py:273` `trades = r.load_trades(inst)`; `:279`
`feat = r.add_trade_features(feat, trades)`; `:295`
`result = run_cell(inst, h, fset, preloaded_feat=feat)`.

**Classifier verdict (v5): CORRECTED** (identical by code reuse).

---

## (2) Signed-volume / net_delta dtype path

### The construction (v4, also executed verbatim by v5)

`scripts\v4\a4_runner.py:305-320`:
```python
tr = trades.copy()
tr["second"] = tr["ts_event"].dt.floor("1s")
tr["signed_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
tr["buy_size"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], 0)
tr["sell_size"] = np.where(~tr["is_buy_aggressor"].astype(bool), tr["size"], 0)
tr["is_large"] = (tr["size"] >= tr["size"].quantile(0.95)).astype(int)
per_sec = tr.groupby("second").agg(
    net_delta=("signed_size", "sum"),
    ...
```
then `a4_runner.py:329-334`:
```python
ndel = merged["net_delta"].fillna(0)
df["net_delta_1s"] = ndel.rolling(1).sum().values
df["net_delta_5s"] = ndel.rolling(5).sum().values
df["net_delta_10s"] = ndel.rolling(10).sum().values
df["net_delta_30s"] = ndel.rolling(30).sum().values
df["net_delta_60s"] = ndel.rolling(60).sum().values
```

Line 307 is **structurally identical** to the confirmed Phase 5/7 defect
(`signed_vol = np.where(is_buy, size, -size)`): an unsigned `size` Series is
negated with **no cast** — no `astype(int64)`, no float conversion, no
buy_sum-minus-sell_sum restructuring — before aggregation.

### Is `size` actually unsigned at line 307?

There is **no cast on `size` at any point in the write/read chain**:

1. Load: `g2_day_worker.py:126-127`: `store = db.DBNStore.from_file(str(f))` /
   `df_i = store.to_df().reset_index()` — same loader-call family as the
   original pipeline (`process_zc.py:73-74`: `store = db.DBNStore.from_file(str(f))`
   / `dfs.append(store.to_df())`; `process_mbo.py:133-134` same), whose output
   parquet `size` is arrow-uint32 (execution-witnessed; established context).
2. Tag: `flow_tagger.tag_aggressor` (`flow_tagger.py:99-147`) only does
   `trades = df.loc[df["action"] == "T"].copy()` and adds the two aggressor
   columns — it never touches `size`.
3. Write: `g2_day_worker.py:195` `trades.to_parquet(trades_out, index=False, engine="pyarrow")`.
4. Month concat: `g2_reprocess.py:161-162` plain `pd.concat` + `to_parquet`, no casts
   (grep for `astype` in g2_reprocess.py: no hits in the concat function).
5. Read back: `a4_runner.py:218` `pq.read_table(...).to_pandas()` — no cast.
6. Negate: `a4_runner.py:307` — no cast.

Per-instrument decidability:

- **he/le**: a4 reads the ORIGINAL-family parquets directly
  (`a4_runner.py:140`), whose `size` is the established, execution-witnessed
  arrow-uint32. For he/le the uncast negation at line 307 is the same wrap
  path as the confirmed Phase 5/7 defect under the pinned environment
  (pandas 3.0.1 / numpy 2.4.2).
- **es/nq/cl/gc/zc/zs** (g2-produced v4 parquets): `size` dtype is inherited,
  uncast, from the identical `db.DBNStore...to_df()` loader family that
  produced the witnessed-uint32 originals. I found **no archive artifact that
  directly prints/asserts the dtype of the g2 parquets' `size` column** (grep
  for `uint` across `scripts\` returns zero hits), so for these six
  instruments the wrap is established by provenance of an uncast chain, not by
  a direct execution witness. Flagged as such; the code-level defect (uncast
  unsigned negation) is present regardless.

Supporting archive evidence that the author's own analysis code treats raw
`size` as needing a cast before signed arithmetic:
`scripts\analysis\validate_is_bid.py:92`:
```python
trades_copy["size_int"] = trades_copy["size"].astype(int)
```
(used at lines 97-100 precisely for a buy-minus-sell delta on original-family
data) — a cast a4_runner.py:307 does not perform.

**Dtype verdict (v4): CARRIED.** Deciding quote: `a4_runner.py:307`
(`... tr["size"], -tr["size"])` with no cast anywhere in the chain).

**Dtype verdict (v5): CARRIED** — v5 executes the exact same
`r.add_trade_features` (see `v5_lightgbm_runner.py:43,106`;
`v5_wave_runner.py:279`). No independent trade construction exists in v5.

Mechanism if wrap occurs (parallels the confirmed original): each
sell-aggressor (and UNKNOWN) trade contributes `2^32 - size` instead of
`-size` to `signed_size`; `groupby(...).sum()` then `rolling(...).sum()`
propagate the astronomically positive values into `net_delta_1s..60s`; final
model matrix is cast to float32 (`a4_runner.py:655`:
`X = df[feats].to_numpy(dtype=np.float32)`), preserving the wrong magnitudes.

Not affected by the negation: `buy_size`/`sell_size` (lines 308-309 use `0`,
never `-size`), `trade_count`, `large_count` (counts), `vwap_num`
(`a4_runner.py:317`: `(s * tr.loc[s.index, "size"]).sum()` — float64 price
times size → float64), `vwap_distance` (line 339, float arithmetic).

---

## (3) Either defect in another form

### String matches on trade/MBO fields

Every `isin` / `==` / `.map(` in `a4_runner.py` was checked:

- `a4_runner.py:647`: `valid = (df["y"].isin([0, 1])) & ...` — on the target
  column the script itself writes as {1, 0, -1} (`a4_runner.py:354`:
  `df["y"] = np.where(fut > mid, 1, np.where(fut < mid, 0, -1))`). Values
  match what is written. Not a defect.
- `a4_runner.py:849`: `df[~((df["inst"] == inst.lower()) & (df["bucket"] == bucket))]`
  — results-CSV bookkeeping, not MBO data.
- `a4_runner.py:884-886`: work-split cell filtering on CSV strings.
- `bucket_assigner.py`: no `aggressor`, `isin`, `.map(` or string-`==` on trade
  fields (grep: only the `__main__` guard matched).
- No occurrence of `aggressor_side`, `"B"`, `"Buy"`, `"buy"`,
  `BUY_AGGRESSOR` anywhere in `a4_runner.py` or `v5_lightgbm_runner.py`.

**No vacuous string-match exists in any other form in v4/v5 model code.**

### Unsigned negation / subtraction-into-negative at other sites

Candidate sites in `build_snapshot_features` (`a4_runner.py`):

- `:251-252`: `bas = (df["bid_size_1"] + df["ask_size_1"]).replace(0, np.nan)` /
  `df["l1_imbalance"] = (df["bid_size_1"] - df["ask_size_1"]) / bas`
- `:262`: `df["depth_imbalance"] = (df["total_bid_depth"] - df["total_ask_depth"]) / tot`
- `:280-282`: `df["depth_change_1s"] = td.diff(1)` (and 5s/30s)

These subtract size-like columns and DO go negative by design — but the
snapshot `bid_size_*`/`ask_size_*` columns are **signed by construction**:

- v4/g2 snapshots (es/nq/cl/gc/zc/zs): `book_engine.py:372` feeds the book
  with `size=int(sizes[i])` (Python int); level sizes accumulate in a
  `dict[float, int]` (`book_engine.py:48`, `:97`:
  `sizes[price] = sizes.get(price, 0) + size`); snapshot rows are dicts of
  Python ints (`book_engine.py:274`: `row[f"bid_size_{idx}"] = depth["bids"][i][1]`,
  `:277`: `row[f"bid_size_{idx}"] = 0`), assembled via
  `snap_df = pd.DataFrame(snapshots)` (`book_engine.py:406`) → pandas infers
  signed int64 from Python ints. No unsigned dtype survives into the snapshot
  parquet size columns.
- he/le snapshots: `process_mbo.py:360-363` likewise feeds
  `int(sizes[i])` into its inline OrderBook and builds
  `pd.DataFrame(snapshots)` (`process_mbo.py:370`).

**No other unsigned-wrap site found in the a4/v5 model-feature path.**

### Same-form site elsewhere in the v4 family (outside a4_runner's import chain)

`scripts\v4\a12_academic_signals.py:157` (and again at `:187`):
```python
tr["signed"] = np.where(tr["is_buy_aggressor"].astype(bool), tr["size"], -tr["size"])
```
— the identical uncast negation form, in the v4 academic-signals script (order
flow imbalance / VPIN-style constructions). This script is NOT imported by
a4_runner and does not feed the 35-feature model set, but it shares the
defect form on the same input parquets. Flagged for a separate audit item;
not further audited here (outside C6a scope).

---

## (4) Which trade/flow features feed the models, and which pass through the audited sites

Feature-set definitions, `a4_runner.py:101-123`:

- `SNAPSHOT_FEATURES` (15): lines 101-108
- `PRICE_LAG_FEATURES` (10): lines 109-114
- `TRADE_FEATURES` (10), lines 115-121 (verbatim):
```python
TRADE_FEATURES = [
    "net_delta_1s", "net_delta_5s", "net_delta_10s",
    "net_delta_30s", "net_delta_60s",
    "buy_volume_10s", "sell_volume_10s",
    "trade_count_10s", "large_trade_count_10s",
    "vwap_distance",
]
```
- `:122-123`: `FULL_FEATURES = SNAPSHOT_FEATURES + PRICE_LAG_FEATURES + TRADE_FEATURES`
  (35 features); `BFREE_FEATURES = SNAPSHOT_FEATURES + TRADE_FEATURES` (25).

**All 10 TRADE_FEATURES are in BOTH Full and BFree sets** — so the trade
features (including any wrapped net_delta values) feed every architecture in
every v4 run and every v5 LightGBM run.

Pass-through map (all sites in `add_trade_features`, `a4_runner.py:299-340`):

| Feature | Built at | Through classifier site (307-309)? | Through uncast negation (307)? |
|---|---|---|---|
| net_delta_1s/5s/10s/30s/60s | :307, :311-312, :329-334 | yes | **YES — wrap-affected** |
| buy_volume_10s | :308, :335 | yes | no (`np.where(cond, size, 0)`) |
| sell_volume_10s | :309, :336 | yes (negated bool) | no |
| trade_count_10s | :315 (`trade_count=("size", "size")` — row count), :337 | no | no |
| large_trade_count_10s | :310, :316, :338 | no | no |
| vwap_distance | :317, :320, :339 | no | no (float64 arithmetic) |

Causal lag (`a4_runner.py:343-347 apply_causal_lag`) shifts all of these by 1
second but does not change dtype or values otherwise.

v5 consumes the identical columns: `v5_lightgbm_runner.py:114-115` selects
`r.FULL_FEATURES` / `r.BFREE_FEATURES`, and `:111` applies
`r.apply_causal_lag(feat, r.FULL_FEATURES)`.

---

## Bottom line

- **Classifier defect: CORRECTED in v4 and v5.** The v4 reimplementation reads
  the boolean `is_buy_aggressor` column (a4_runner.py:218, 307-309) — a column
  genuinely written as `side == "B"` by every writer of the parquets it loads
  (flow_tagger.py:105; process_mbo.py:552; process_zc.py:95). The vacuous
  `isin(["B","Buy","buy"])` test appears nowhere in v4/v5.
- **Dtype defect: CARRIED in v4 and v5, in the same form.**
  `a4_runner.py:307` negates the uncast `size` column exactly as the
  confirmed Phase 5/7 code did; no cast exists anywhere from DBN load to model
  matrix. It contaminates the five `net_delta_*` features (5 of 35 Full / 5 of
  25 BFree), in both v4 (all six architectures, Designs A/B/C) and v5
  (LightGBM), for every instrument. For he/le the input parquets are the
  execution-witnessed arrow-uint32 originals; for es/nq/cl/gc/zc/zs the g2
  parquets inherit `size` uncast from the identical databento loader family —
  code-level defect certain, runtime wrap for those six established by
  provenance rather than by a direct dtype witness in the archive (no such
  witness exists; grep `uint` over `scripts\` = 0 hits).
