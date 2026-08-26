# Item C2 — phase7_l2_sim.py aggregation scan vs Phase 5 builder

STATIC READ ONLY. No execution. All quotes verbatim; line numbers are 1-indexed.

## Files compared

| File | Path | mtime | SHA256 | Lines |
|---|---|---|---|---|
| Phase 7 L2 sim | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py` | 2026-04-12 12:30:00 | C659D3AC167A13AFB52651D4521ECC9FD5C8FABD59FD2D712EB4AFA5B4669665 | 949 |
| Phase 5 builder | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py` | 2026-04-06 19:24:29 | 040BE5250443127B83A5E025796EC25268B939C0355E224B15C266C6356F0712 | 802 |

phase7_l2_sim.py exists at exactly ONE path in the archive (glob over the whole tree found no mirrors). The Phase 5 builder quoted here is the pc2_transfer copy already byte-verified in earlier items; the `results\pc2_all_phases\_scripts\scripts\phase5\phase5_ml.py` mirror has the identical `is_buy` line at its line 231.

## Side-by-side: trade/MBO aggregation constructs

| # | Construct | Phase 5 builder (phase5_ml.py) | phase7_l2_sim.py | Same/Different |
|---|---|---|---|---|
| 1 | Aggressor classification | L231-232: `is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \` / `else trades["side"].isin(["B","Buy","buy"])` | L207-208: `is_buy = trades["aggressor_side"].isin(["B", "Buy", "buy"]) if "aggressor_side" in trades.columns \` / `else trades["side"].isin(["B", "Buy", "buy"])` | SAME (whitespace-only difference). Same literals `"B","Buy","buy"`, same `aggressor_side`-then-`side` fallback. Neither reads the boolean `is_buy_aggressor` column. |
| 2 | Signed volume | L233: `trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])` | L209: `trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])` | SAME (byte-identical). No cast before negation in either file. |
| 3 | Buy/sell volume split | L234-235: `trades["buy_vol"] = np.where(is_buy, trades["size"], 0)` / `trades["sell_vol"] = np.where(~is_buy, trades["size"], 0)` | L210-211: identical text | SAME |
| 4 | Large-trade flag | L236: `trades["is_large"] = (trades["size"] >= 10).astype(int)` | L212: identical text | SAME |
| 5 | Dollar volume | ABSENT | L213-214: `# Dollar volume proxy: size * price` / `trades["dollar_vol"] = trades["size"] * trades["price"]` | DIFFERENT — Phase 7 only |
| 6 | Trade groupby key | L230: `trades["ts_floor"] = trades["ts_event"].dt.floor("1s")` (after L226-229 to_datetime, tz-strip, sort) | L206: identical text (after L202-205 to_datetime, tz-strip, sort) | SAME |
| 7 | Per-second agg | L237-243: `tagg = trades.groupby("ts_floor").agg(` `net_delta=("signed_vol","sum"), buy_volume=("buy_vol","sum"),` `sell_volume=("sell_vol","sum"), trade_count=("size","count"),` `trade_volume=("size","sum"), large_trade_count=("is_large","sum"),` `vwap=("price", lambda x: np.average(x, weights=trades.loc[x.index,"size"]) if trades.loc[x.index,"size"].sum() > 0 else np.nan),` | L216-226: same agg dict PLUS `dollar_volume=("dollar_vol", "sum"),` (L223); vwap lambda identical (L224-225) | SAME except Phase 7 adds `dollar_volume` |
| 8 | Merge + fill | L248-250: `snap = snap.merge(tagg, on="ts_floor", how="left")`; fillna(0) over `["net_delta","buy_volume","sell_volume","trade_count","trade_volume","large_trade_count"]` | L231-234: same merge; fillna(0) list additionally contains `"dollar_volume"` | SAME except added column |
| 9 | vwap fill | L251: `snap["vwap"] = snap["vwap"].ffill()` | L235: identical text | SAME |
| 10 | net_delta rollups | L252-253: `for w in [1, 5, 10, 30, 60]:` / `snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()` | L238-239: identical text | SAME |
| 11 | 10s volume rollups | L254-255: `buy_volume_10s` / `sell_volume_10s` = `.rolling(10, min_periods=1).sum()` | L240-241: identical text | SAME |
| 12 | Trade-count feature | L256: `snap["trade_count_10s"] = snap["trade_count"].rolling(10, min_periods=1).sum()` | ABSENT; instead L246-248: `snap["trade_volume_1s"] = snap["trade_volume"].fillna(0)` / `snap["trade_count_1s"] = snap["trade_count"].fillna(0)` / `snap["dollar_volume_1s"] = snap["dollar_volume"].fillna(0)` | DIFFERENT — Phase 5 models 10s rolling count; Phase 7 models raw 1s bucket values |
| 13 | large_trade_count_10s | L257: `.rolling(10, min_periods=1).sum()` | L242: identical text | SAME |
| 14 | vwap_distance | L258: `snap["vwap_distance"] = (mid - snap["vwap"]) / tick` | L243: identical text | SAME |
| 15 | Missing-trades fallback | L260-264: zero-fills `net_delta_*s`, `buy_volume_10s`, `sell_volume_10s`, `trade_count_10s`, `large_trade_count_10s`, `vwap_distance` | L250-255: zero-fills `net_delta_*s`, `buy_volume_10s`, `sell_volume_10s`, `large_trade_count_10s`, `vwap_distance`, `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s` | SAME mechanism, column list differs per #12 |
| 16 | MBO aggregation | L109-171 `load_mbo_aggregated` (adds/cancels by side per second); merged at L266-286 into add/cancel rate features | ABSENT — docstring L4: `L2 features only (no L3/MBO cancel/add/rate features).` No MBO file is opened anywhere in phase7_l2_sim.py | DIFFERENT — Phase 7 reads only snapshots + trades_tagged |
| 17 | Universal feature lag | ABSENT — no `shift(1)` of features anywhere; only label shift `fwd = mid.shift(-h)` (L218) | L260-276: `# ══ UNIVERSAL LAG FIX: shift ALL features by 1 second ══` ... `snap[feature_cols] = snap[feature_cols].shift(1)` (L276), with exempt set L266-273 (`timestamp, mid_price, month, ts_floor, hour_utc`, labels, raw book cols) | DIFFERENT — Phase 7 lags every feature (incl. all net_delta/buy/sell aggregates) by 1 s |
| 18 | Session window (ZC) | L55: `"zc": {... "day_start_utc": 14, "day_end_utc": 19 ...}`; filter L186 | L50-51: `"zc": {... "day_start_utc": 14, "day_end_utc": 19, ...}`; filter L145 | SAME hours (also nq 14-22, gc 13-22, zs 14-19 identical); Phase 5 covers 8 instruments, Phase 7 only nq/gc/zc/zs |
| 19 | Labels | L217-219: `fwd = mid.shift(-h)` / `snap[f"fwd_move_ticks_{h}s"] = (fwd - mid) / tick` | L193-195: identical construction | SAME |
| 20 | Data source | L38-40: `PROJECT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")`, `LOCAL_DATA = Path(r"C:\MBO_data")`; `get_data_dir` (L104-106) prefers `C:\MBO_data\<sym>` | L32-33: `PROJECT = Path(r"C:\Users\Research\Desktop\pc2_transfer")`, `PROC = PROJECT / "processed"`; no LOCAL_DATA fallback (L132, L135) | DIFFERENT — Phase 7 hardcodes a `C:\Users\Research\...` pc2 path, reads processed/ only |

## Degeneracy verdict (static)

Phase 7's classifier literals `"B", "Buy", "buy"` (L207-208) match NONE of the known actual `aggressor_side` values in the ZC trades_tagged parquet (SELL_AGGRESSOR 197,640 / BUY_AGGRESSOR 172,705 / UNKNOWN 27,112; `isin` is exact, case-sensitive string equality). Because `aggressor_side` exists in the parquet, the `side` fallback branch is never taken. Therefore, statically:

- `is_buy` is all-False; every trade takes the else-branch of every `np.where`.
- `buy_vol` ≡ 0 → `buy_volume` ≡ 0 → `buy_volume_10s` ≡ 0 (dead model feature).
- `sell_vol` ≡ `size` → `sell_volume_10s` ≡ 10s total volume (duplicates `trade_volume` information).
- `signed_vol` = `-size` for every trade → `net_delta` and all `net_delta_{1,5,10,30,60}s` carry no buy/sell information. Same degeneracy class as the Phase 5 builder — byte-identical mechanism.
- dtype path: identical to Phase 5 — no cast before `-trades["size"]`. On a uint32 `size` column the negation wraps modulo 2^32 in the environment measured during the f2 rebuild (pandas 3.0.1/numpy 2.4.2). Whether the original 2026-04 run environment wrapped or promoted to int64 cannot be determined statically; either way the sign information is absent.

Scope caveat: actual parquet values were measured only for ZC 2025-01. The verdict extends to NQ/GC/ZS months only if those trades_tagged files use the same value convention (unverified).

## Which trade aggregates feed the 35-column model set

`ALL_L2_FEATURES = L1_FEATURES + L2_FEATURES` (L108). Trade-derived members, all in `L1_FEATURES` (L73-83): `net_delta_1s, net_delta_5s, net_delta_10s, net_delta_30s, net_delta_60s, buy_volume_10s, sell_volume_10s, large_trade_count_10s, vwap_distance, trade_volume_1s, trade_count_1s, dollar_volume_1s` — 12 of 21 L1 features. All 14 L2 features are snapshot-only.

Intermediates only (never in the model set): per-second merged columns `net_delta, buy_volume, sell_volume, trade_count, trade_volume, large_trade_count, dollar_volume, vwap` and in-trades columns `signed_vol, buy_vol, sell_vol, is_large, dollar_vol`.

Affected by the aggressor mismatch: 7 of the 35 model features (5x net_delta_*s corrupted, buy_volume_10s dead-zero, sell_volume_10s redundant). Unaffected: trade_volume_1s, trade_count_1s, dollar_volume_1s, large_trade_count_10s, vwap_distance (vwap uses only price and size).

## Ancillary fact

Elsewhere in the same tree the correct enum literals ARE used: `results\pc2_all_phases\_scripts\scripts\phase9_ofi_pc2.py` L149 `is_buy = trades["aggressor_side"] == "BUY_AGGRESSOR"` (and L151 `SELL_AGGRESSOR`), and `phase9_ofa_dar_pc2.py` L116-117. The `["B","Buy","buy"]` variant also recurs in `phase4\phase4_ml.py` L243, `phase4\phase4_v2.py` L346, `phase4\phase4_shuffle_fix.py` L236, `phase45\phase45b_audit.py` L213, `phase45\phase45_verify.py` L202 (paths relative to `results\pc2_all_phases\_scripts\scripts\`).
