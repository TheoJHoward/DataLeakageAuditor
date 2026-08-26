# F3 FIXTURE MANIFEST — VERIFICATION AGAINST THE PRODUCING CODE

**What this is.** The verification underlying the author's sign-off. **Sign-off is the
author's act; it does not require the author to perform the verification personally.** The
verification was performed by automated analysis and is set out here in full, so that the
sign-off is given over a stated record rather than an unexamined assertion.

**It does not adjudicate whether the classification is correct.** It reports what the code
shows; the judgement rests with the author.

## THE SOURCES

| | |
|---|---|
| manifest | `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json`, sha256 `8fd3bb5a771af72d…` |
| producing code | `phase7_l2_sim.py`, **949 lines**, sha256 `c659d3ac167a13af…` |
| where that code lives | `MBO_2025\results\pc2_all_phases\_scripts\scripts\` — **the archive, NOT the repository** |

**SUPERSEDED IN PART, 26 August 2026 — the producing code is now in the repository.**
`phase7_l2_sim.py` was copied to `evidence/fixture_spike/f3/`, verified at the destination
against the sha256 for `phase7_l2_sim.py` already pinned at `AVAILABILITY_DECLARATION.md` §D.1 — that
file's hash, `c659d3ac167a13af…`,
41,745 bytes, 949 lines), and is hashed in the `prereg-v30a` tag message. **The warning
below was true on its date and is retained unedited**; what follows it about reading from
the archive copy records how this verification was actually performed, which does not
change.

**A scope collision this supersession also closes.** The `D-ARCHIVE` disclosure draft read
*"The producing code IS committed"* while the warning below read *"THE PRODUCING CODE IS
NOT IN THE REPOSITORY"*. **Both were true — of different sets:** the first of the three
spike producers brought in earlier, the second of `phase7_l2_sim.py`, which was not among
them. Nothing anywhere said they were speaking about different sets, so the pair read as a
contradiction. It was not one, and it is no longer live either way.

> **⚠ THE PRODUCING CODE IS NOT IN THE REPOSITORY.** All 35 columns cite `phase7_l2_sim.py` as
> their `construction_source`, and that file is absent from the repo. It is present in the
> read-only archive, inside the **118-file / 2.6 MB `results/pc2_all_phases/_scripts` reference**
> that `D-ARCHIVE` already discloses as an external input. **Every quotation below was read from
> the archive copy.** A reader with the repository alone cannot re-run this verification — which
> is `D-ARCHIVE`'s disclosure, arriving here in concrete form.

---

## (c) THE PRE-LAG BASIS, SHOWN

The manifest's classification basis says classes describe what each column reads relative to the
label base `mid(t)` **BEFORE** the universal `shift(1)`. Here is that shift, and what it exempts:

```python
 268|     raw_book_cols = {f"bid_price_{i}" for i in range(1, 6)} | \
 269|                     {f"ask_price_{i}" for i in range(1, 6)} | \
 270|                     {f"bid_size_{i}" for i in range(2, 6)} | \
 271|                     {f"ask_size_{i}" for i in range(2, 6)} | \
 272|                     {"spread", "book_imbalance"}
 273|     exempt = EXEMPT_COLS | label_cols | raw_book_cols
 274| 
 275|     feature_cols = [c for c in snap.columns if c not in exempt]
 276|     snap[feature_cols] = snap[feature_cols].shift(1)
```

And the label base itself:

```python
 149|     mid = snap["mid_price"].replace(0, np.nan)
 193|     for h in horizons:
 194|         fwd = mid.shift(-h)
 195|         snap[f"fwd_move_ticks_{h}s"] = (fwd - mid) / tick
```

**Two things the code shows that the summary does not.**

1. **The shift does not touch everything.** `exempt = EXEMPT_COLS | label_cols | raw_book_cols`,
   and `raw_book_cols` covers `bid_price_1..5`, `ask_price_1..5`, **`bid_size_2..5`**,
   **`ask_size_2..5`**, `spread`, `book_imbalance`. **`bid_size_1` and `ask_size_1` are NOT in
   that set**, so they are shifted with the ordinary features.
2. **The labels are built before the shift and from unlagged `mid`** — `fwd = mid.shift(-h)`,
   `fwd_move_ticks_{h}s = (fwd - mid) / tick`. So "reads `mid(t)`" and "reads what the label
   reads" are the same statement here.

---

## (b) LEAK-SOURCE — 25 columns, each located in the code

### `mid_return_1s` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **manifest note:** *pct_change(lag) at row t reads mid(t), the label base. In-code comment line 151 '(lagged - use data through t-1)' is FALSE pre-shift; the lag exists only via line 276 shift(1).*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   153| snap[f"mid_return_{lag}s"] = mid.pct_change(lag)
  ```

### `mid_return_5s` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   153| snap[f"mid_return_{lag}s"] = mid.pct_change(lag)
  ```

### `mid_return_10s` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   153| snap[f"mid_return_{lag}s"] = mid.pct_change(lag)
  ```

### `mid_return_30s` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   153| snap[f"mid_return_{lag}s"] = mid.pct_change(lag)
  ```

### `tick_direction` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **manifest note:** *Reads mid(t). Not in the Phase 5 45-set; new classification in this manifest.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   156| snap["tick_direction"] = np.sign(mid.pct_change(1)).fillna(0)
  ```

### `trade_volume_1s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Not in the 45-set; new classification. Full-second aggregation of second t while row is stamped within second t.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   246| snap["trade_volume_1s"] = snap["trade_volume"].fillna(0)
  ```

### `trade_count_1s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Not in the 45-set; new classification.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   247| snap["trade_count_1s"] = snap["trade_count"].fillna(0)
  ```

### `dollar_volume_1s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Not in the 45-set; new classification.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   248| snap["dollar_volume_1s"] = snap["dollar_volume"].fillna(0)
  ```

### `net_delta_1s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Rolling window includes full second t.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   239| snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
  ```

### `net_delta_5s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   239| snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
  ```

### `net_delta_10s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   239| snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
  ```

### `net_delta_30s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   239| snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
  ```

### `net_delta_60s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   239| snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
  ```

### `buy_volume_10s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   240| snap["buy_volume_10s"] = snap["buy_volume"].rolling(10, min_periods=1).sum()
  ```

### `sell_volume_10s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   241| snap["sell_volume_10s"] = snap["sell_volume"].rolling(10, min_periods=1).sum()
  ```

### `large_trade_count_10s` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   242| snap["large_trade_count_10s"] = snap["large_trade_count"].rolling(10, min_periods=1).sum()
  ```

### `vwap_distance` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **manifest note:** *Reads mid(t) AND same-second vwap - dual exposure; label_base_price flavor per the 45-set DAG precedent (phase5_ml.py line 258).*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   243| snap["vwap_distance"] = (mid - snap["vwap"]) / tick
  ```

### `bid_size_1` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Book state at t. NOT exempt from the universal shift(1): raw_book_cols at lines 268-272 exempts only bid_size_{2..5}/ask_size_{2..5}, so bid_size_1 IS lagged at line 276 in the archived (post-fix) script.*
- **NOT CONSTRUCTED — it is a raw column of the snapshots parquet**, read at
  `phase7_l2_sim.py` and never assigned there. Declared in `L2_FEATURES` (l.97) and
  loaded from `{sym}_snapshots_{month}.parquet` (l.135). **It is NOT in `raw_book_cols`**
  (which covers `bid_size_2..5` / `ask_size_2..5`), so it IS shifted at l.276.
  Its reads:

  ```python
    97| "bid_size_1", "ask_size_1",
   174| snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /
   175| (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)).fillna(0)
   178| snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb - 1, 1) if nb >= 2 else 0.0
  ```

### `ask_size_1` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Same treatment as bid_size_1.*
- **NOT CONSTRUCTED — it is a raw column of the snapshots parquet**, read at
  `phase7_l2_sim.py` and never assigned there. Declared in `L2_FEATURES` (l.97) and
  loaded from `{sym}_snapshots_{month}.parquet` (l.135). **It is NOT in `raw_book_cols`**
  (which covers `bid_size_2..5` / `ask_size_2..5`), so it IS shifted at l.276.
  Its reads:

  ```python
    97| "bid_size_1", "ask_size_1",
   174| snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /
   175| (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)).fillna(0)
   179| snap["book_slope_ask"] = (snap["ask_size_1"] - snap[ask_cols[-1]]) / max(na - 1, 1) if na >= 2 else 0.0
  ```

### `total_bid_depth` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   169| snap["total_bid_depth"] = snap[bid_cols].sum(axis=1)
  ```

### `total_ask_depth` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   170| snap["total_ask_depth"] = snap[ask_cols].sum(axis=1)
  ```

### `weighted_mid` — LEAK-SOURCE

- **manifest flavor:** `label_base_price`
- **manifest note:** *Not in the 45-set; new classification. DUAL exposure: reads raw contemporaneous book (bid/ask_price_1, bid/ask_size_1 at t) AND subtracts mid(t), the label base, at line 187. Flavor assigned label_base_price per the vwap_distance precedent; author should confirm.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   184| snap["weighted_mid"] = (snap["bid_price_1"] * snap["ask_size_1"] +
   187| snap["weighted_mid"] = (snap["weighted_mid"] - mid) / tick  # distance from mid in ticks
  ```

### `spread_ticks` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *spread is a raw snapshot column at t.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   142| snap["spread_ticks"] = snap["spread"] / tick
  ```

### `book_slope_bid` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **manifest note:** *Reads raw book columns at t directly (bid_size_1, bid_size_5); classified LEAK-SOURCE per the 45-set DAG, not DESCENDANT.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   178| snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb - 1, 1) if nb >= 2 else 0.0
  ```

### `book_slope_ask` — LEAK-SOURCE

- **manifest flavor:** `contemporaneous_state_flow`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   179| snap["book_slope_ask"] = (snap["ask_size_1"] - snap[ask_cols[-1]]) / max(na - 1, 1) if na >= 2 else 0.0
  ```

---

## (d) DESCENDANT — 6 columns, and what each descends from

### `book_imbalance_ratio` — DESCENDANT

- **manifest parents:** `['total_bid_depth', 'total_ask_depth']`
- **manifest note:** *Not in the 45-set; new classification. Pure function of two contemporaneous leak sources - inherits, does not independently leak.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   188| snap["book_imbalance_ratio"] = (snap["total_bid_depth"] /
  ```

### `depth_imbalance` — DESCENDANT

- **manifest parents:** `['total_bid_depth', 'total_ask_depth']`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   172| snap["depth_imbalance"] = ((snap["total_bid_depth"] - snap["total_ask_depth"]) /
  ```

### `depth_change_1s` — DESCENDANT

- **manifest parents:** `['total_bid_depth', 'total_ask_depth']`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   181| snap[f"depth_change_{lag}s"] = td.diff(lag)
  ```

### `depth_change_5s` — DESCENDANT

- **manifest parents:** `['total_bid_depth', 'total_ask_depth']`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   181| snap[f"depth_change_{lag}s"] = td.diff(lag)
  ```

### `depth_change_30s` — DESCENDANT

- **manifest parents:** `['total_bid_depth', 'total_ask_depth']`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   181| snap[f"depth_change_{lag}s"] = td.diff(lag)
  ```

### `l1_imbalance` — DESCENDANT

- **manifest parents:** `['bid_size_1', 'ask_size_1']`
- **constructed at `phase7_l2_sim.py`:**

  ```python
   174| snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /
  ```

---

## (e) CLEAN — 4 columns

### `minutes_since_open` — CLEAN

- **manifest note:** *Clock time only. Same CLEAN class as in the 45-set DAG (phase5_ml.py line 189).*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   159| snap["minutes_since_open"] = (snap["hour_utc"] - ds) * 60 + snap["timestamp"].dt.minute
  ```

### `session_open` — CLEAN

- **manifest parents:** `['minutes_since_open']`
- **manifest note:** *Deterministic function of clock time; parent is CLEAN, so class is CLEAN, not DESCENDANT. Not in the 45-set.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   162| snap["session_open"] = (frac < 0.1).astype(float)
  ```

### `session_mid` — CLEAN

- **manifest parents:** `['minutes_since_open']`
- **manifest note:** *Not in the 45-set.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   163| snap["session_mid"] = ((frac >= 0.1) & (frac < 0.85)).astype(float)
  ```

### `session_close` — CLEAN

- **manifest parents:** `['minutes_since_open']`
- **manifest note:** *Not in the 45-set.*
- **constructed at `phase7_l2_sim.py`:**

  ```python
   164| snap["session_close"] = (frac >= 0.85).astype(float)
  ```

---

## (f) THE BORDERLINE CALLS — BOTH READINGS, AND THE MANIFEST'S CHOICE

**The manifest flags its own judgement calls.** Both readings are stated; which is right is not
decided here (§177.4).

### 1. `book_slope_bid` / `book_slope_ask` — LEAK-SOURCE or DESCENDANT?

The code: `snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb - 1, 1)`.

- **Reading A (the manifest’s): LEAK-SOURCE.** It reads raw book columns at `t` *directly* —
  `bid_size_1` and `bid_size_5` — rather than reading another engineered feature. Its note:
  *“classified LEAK-SOURCE per the 45-set DAG, not DESCENDANT.”*
- **Reading B: DESCENDANT.** `bid_size_1` is itself classed LEAK-SOURCE, so a function of it could
  be said to *inherit* rather than *independently* leak — which is exactly the test the manifest
  applies to `book_imbalance_ratio` to reach the opposite answer.
- **The tension is real and worth the author’s eye:** the same “pure function of contemporaneous
  leak sources” shape yields DESCENDANT for `book_imbalance_ratio` and LEAK-SOURCE here. The
  manifest’s stated discriminator is *raw* book columns versus *derived* ones — `book_slope_*`
  reads `bid_size_*` (raw), `book_imbalance_ratio` reads `total_bid_depth` (derived).

### 2. `book_imbalance_ratio` — DESCENDANT, and it is the only one

The code: `snap["book_imbalance_ratio"] = (snap["total_bid_depth"] / snap["total_ask_depth"]…)`.

- **Reading A (the manifest’s): DESCENDANT** — *“Pure function of two contemporaneous leak
  sources — inherits, does not independently leak.”* Both parents are themselves LEAK-SOURCE.
- **Reading B: LEAK-SOURCE**, on the ground that a ratio of two `t`-state quantities is still a
  `t`-state quantity, and the DAG’s inherit/independent distinction does not change what instant
  it reads.
- **Note it is “not in the 45-set”** — a new classification made by this manifest, so no earlier
  DAG decision constrains it.

### 3. A THIRD ITEM THE MANIFEST RAISES ITSELF — an in-code comment it calls FALSE

`mid_return_1s`’s note says the comment at line 151, *“L1: Price returns (lagged — use data
through t-1)”*, is **FALSE pre-shift**: `pct_change(lag)` at row `t` reads `mid(t)`, the label base.
**The code comment and the classification disagree, and the manifest sides against the comment.**
Verified: line 151 carries that comment and line 153 is `snap[f"mid_return_{lag}s"] =
mid.pct_change(lag)`, with no shift applied at that point — the universal shift is 123 lines later
at l.276. **The manifest’s reading is what the code shows.**

---

## §177.3 — TWO INDEPENDENT PATHS, WHERE TWO EXIST

| classification | path A | path B | two paths? |
|---|---|---|---|
| the 25 LEAK-SOURCE names | the manifest’s `columns` array | located and quoted in `phase7_l2_sim.py`, independently of the manifest | **YES** |
| the class counts | the manifest’s `counts` block | counted from the `columns` array itself | **YES** |
| the pre-lag basis | the manifest’s `classification_basis` prose | the `shift(1)` site at l.276 and the `exempt` set at l.268–273 | **YES** |
| the label definition | the manifest’s `label_definition` | l.193–195, `fwd = mid.shift(-h)` | **YES** |
| **whether a class is CORRECT** | the manifest’s judgement | — | **NO — one path only** |

**Where only one path exists, and why:** correctness of a *class* is a judgement about what
constitutes leakage, not a fact the code can settle. The code shows what a column reads and when;
it cannot show whether reading that constitutes a leak. **That is the irreducible part, and it is
the author’s** — which is what §177.4 says and why this dossier stops short of it.

## (g) THE ARITHMETIC, RECONCILED AGAINST THE ACTUAL LIST

Counted from the `columns` array itself, not from the manifest's `counts` block:

| class | counted from the list | manifest's summary |
|---|---|---|
| LEAK-SOURCE | **25** | 25 |
| DESCENDANT | **6** | 6 |
| CLEAN | **4** | 4 |
| **total** | **35** | 35 |

**25 + 6 + 4 = 35**, and the list holds 35 columns. **Reconciled.**

## §177.2 — CLASSIFICATIONS NOT ESTABLISHABLE FROM CODE **IN THE REPOSITORY**

**All 35.** The producing code is not in the repository; every classification rests on
`phase7_l2_sim.py`, which lives only in the archive. **From the archive, the count is 0** —
every one of the 35 columns' construction was located and quoted above.

## CONSTRUCTION-SITE COVERAGE

| | |
|---|---|
| located directly (`snap["name"] = …`) | 21 |
| raw source columns (read, never assigned) | 2 |
| located via the loop form (`snap[f"…{lag}s"] = …`) | 12 |
| **not located** | **0** |

