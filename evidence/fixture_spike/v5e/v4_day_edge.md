# ITEM V5 — V4 day-edge label check

**Method:** static read only. The static read fully decides the question; no measurement was run, no archive file was modified, no detector code touched.

**Files read (archive, read-only):**
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py` (full label path: lines 1-939)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\bucket_assigner.py` (full, 381 lines)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_lightgbm_runner.py` (lines 1-135, label path)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_label_generator.py` (lines 1-339)

---

## VERDICT: SHARED (v4 / a4_runner.py) — unpartitioned positional shift(-h)

The v4 label construction in `a4_runner.py` is a purely positional `shift(-horizon)` over the
whole-year concatenated, bucket-filtered, `reset_index(drop=True)` frame. There is **no groupby,
no session/day partition, and no gap/sentinel handling anywhere before or after the shift**.
Session-tail rows receive their "future" mid from the next session's head rows, so their labels
span closed-market gaps (overnight breaks, weekends, and for single-bucket cells the entire
~22-hour inter-window gap). These rows are **not** dropped by any downstream filter.

The v5 runner (`v5_lightgbm_runner.py`) does **not** share the defect: it builds no labels itself;
it loads labels produced by `v5_label_generator.py`, which uses a time-based (`merge_asof` forward,
tolerance-bounded) t+h lookup with an explicit `session_cross` exclusion. Details in section 3.

---

## 1. The v4 shift and its frame

### 1.1 The shift itself — a4_runner.py:350-356

```python
def build_target(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """y = 1 if mid[t+h] > mid[t], 0 if <, drop ties."""
    mid = df["mid_price"]
    fut = mid.shift(-horizon)
    df["y"] = np.where(fut > mid, 1, np.where(fut < mid, 0, -1))
    df["prev_return"] = (mid - mid.shift(horizon))  # for naive baseline
    return df
```

`fut = mid.shift(-horizon)` (line 353) is a positional pandas shift by row count
(horizon in {5, 10, 30, 60}, a4_runner.py:96 `HORIZONS = [5, 10, 30, 60]`). Nothing keys it to
timestamps, sessions, or days. Note also line 355: `prev_return` (the naive-baseline feature)
positionally crosses session **heads** the same way.

### 1.2 The frame the shift runs over — a concatenated, unpartitioned lattice

The frame passed in is `df_feat`, built in `process_cell` (a4_runner.py:762-785) as:

1. **Whole-year concat** — `load_snapshots` (a4_runner.py:194-206):
   ```python
   snap = pd.concat(dfs, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
   ```
   (line 205) — all 12 monthly parquets (`MONTHS`, line 89) into one frame.

2. **Bucket filter making day edges positionally adjacent** — `filter_to_bucket`
   (a4_runner.py:229-238):
   ```python
   out = tagged[mask].drop(columns=["bucket", "in_full_session"]).copy()
   out = out.rename(columns={"ts_event": "timestamp"})
   return out.reset_index(drop=True)
   ```
   (lines 236-238). After this `reset_index(drop=True)`, the last row of day N's bucket window is
   positionally row-adjacent to the first row of day N+1's window.

3. Features (`build_snapshot_features` 242-296, `add_trade_features` 299-340), causal lag
   (`apply_causal_lag` 343-347, `df[c] = df[c].shift(1)` — also positional/unpartitioned), then
   `design_a_split` (360-378) which builds **day-based train/val/test masks only** — it does not
   partition the frame or touch labels.

4. `run_single` receives the whole `feat_df` and calls the shift on it (a4_runner.py:644-645):
   ```python
   # target for this horizon
   df = build_target(df_feat, horizon)
   ```

**Grep confirmation:** the only `shift(` occurrences in a4_runner.py are lines 346 (causal lag +1),
353 (`shift(-horizon)`), and 355 (`shift(horizon)`); the only `groupby` is
`tr.groupby("second")` at line 311 (trade aggregation, unrelated to labels). No
session/day groupby exists in the file.

### 1.3 Size of the gaps being spanned (from bucket_assigner.py)

`filter_to_bucket` calls `assign_buckets` from `bucket_assigner.py` (imported at a4_runner.py:46).
Bucket windows (bucket_assigner.py:64-92), NY local time:

- 7bucket (es, nq, cl, gc): e.g. `("morning", time(10, 0), time(12, 0), False)` (line 70);
  full_session `(time(18, 0), time(16, 15), True)` (line 89).
- 5bucket grains (zc, zs): e.g. `("afternoon", time(12, 30), time(14, 20), False)` (line 78);
  full_session `(time(20, 0), time(14, 20), True)` (line 90).
- 4bucket livestock (he, le): `("afternoon", time(12, 30), time(14, 5), False)` (line 83);
  full_session `(time(9, 30), time(14, 5), False)` (line 91).

So for a **single-bucket cell** (e.g. zc/morning 10:30-12:30 NY), the row after a day's last
in-bucket row is the **next trading day's** first in-bucket row: the shifted "future" mid is
~22 hours (or a weekend) away. For a **full_session cell**, the tail rows of each session take
their future mid from after the maintenance break / overnight close (7bucket: 16:15 -> 18:00;
grains: 14:20 -> 20:00; livestock: 14:05 -> 09:30 next day) and across weekends. Additionally,
any coverage gaps inside the stored snapshot lattice itself (es is loaded from
`processed\es\v4_morning_chunk`, a4_runner.py:136-137; per-file coverage not inspected here) are
crossed the same way, since nothing partitions the shift.

### 1.4 Day-edge rows are NOT dropped — a4_runner.py:646-648

```python
# drop rows where y not in {0,1} or all features NaN
valid = (df["y"].isin([0, 1])) & (~df[feats].isna().all(axis=1))
df = df.loc[valid].reset_index(drop=True)
```

`y == -1` (dropped) arises only from ties or from `fut` being NaN. `fut` is NaN only for the final
`horizon` rows of the **entire concatenated frame** and for rows whose matched future mid was
NaN-masked (negative-spread mask, a4_runner.py:246-247 and 287). A session-tail row's `fut` is the
next session's real mid price, so it gets y in {0,1} — a label for the closed-market gap move —
and survives the filter. No other mask (embargo handling in `design_a_split` is day-set based on
the split masks only, lines 360-378) removes these rows.

**Bound on contamination (static, not measured):** at most `horizon` rows per contiguous window
boundary carry a cross-gap label (h in {5,10,30,60}); every trading-day boundary of every cell is
affected, at every horizon, in train, val, and test alike.

---

## 2. Design B/C note

`configure_design` (a4_runner.py:61-87) and `design_a_day_sets` (160-190) change only which days
are test/embargo. The label construction path (`build_target` on the unpartitioned frame) is
identical for Designs A, B, and C.

---

## 3. v5 label path — PARTITIONED (does not share the defect)

`v5_lightgbm_runner.py` builds no labels. It loads precomputed labels and inner-joins on timestamp:

- Load (v5_lightgbm_runner.py:76-80):
  ```python
  label_path = ROOT / "v5" / "labels" / f"{inst}_h{h}.parquet"
  ...
  lab = lab[lab["label"].notna()][["timestamp_t", "label"]].copy()
  ```
- Join (lines 120-122): `feat.merge(lab[["timestamp_t", "y"]], left_on="timestamp", right_on="timestamp_t", how="inner")`.

The labels come from `v5_label_generator.py`, which is time-based and session-guarded:

- **Time-based t+h lookup, not positional** (v5_label_generator.py:224, 248-255):
  `ts_target_series = snap["timestamp"] + h` then
  ```python
  merged_valid = pd.merge_asof(
      target_valid.sort_values("ts_target"),
      right.sort_values("ts_match"),
      left_on="ts_target", right_on="ts_match",
      direction="forward", tolerance=tol,
  )
  ```
  with `tolerance = min(int(h*0.05), 10)` seconds (lines 129-130). A session-tail row whose t+h
  falls in the closed market finds no match within tolerance and gets `'no_t_plus_h'`
  (lines 286-288).
- **Explicit session partition** (docstring lines 8-9: "D2 (sessions): Policy A (strict). Exclude
  any (t, t+h) where t and t+h fall in different trading sessions"; implementation lines 297-302):
  ```python
  if not next_trading_day_mode:
      sess_t = merged["session_t"].to_numpy()
      sess_h = merged["session_match"].to_numpy()
      sess_cross = (sess_t != sess_h)
      mask_sc = (reason == None) & sess_cross
      reason[mask_sc] = "session_cross"
  ```
  Session ids come from `compute_session_id` (lines 92-110) with per-instrument NY session-start
  hours (`SESSION_START_HOUR_NY`, lines 43-51).
- Excluded rows get `label = NaN` (line 322), and the v5 runner keeps only `label.notna()`
  (v5_lightgbm_runner.py:80), so session-crossing pairs never enter training/eval.
- Caveat: in `--next-trading-day-mode` (amendment 001) the session-cross exclusion is skipped
  **by design** (v5_label_generator.py:295-296 comment: "session crossing — SKIPPED in
  next_trading_day_mode (amendment 001). In that mode t and t+h are explicitly in adjacent
  sessions by design") — that is a deliberate, declared cross-session target, not the silent
  positional defect.

Note the v5 generator's docstring (line 20) says path routing is a "small embedded copy in
v4_paths.py"; the actual file implements `data_dir_for` inline (v5_label_generator.py:60-67,
"Byte-identical routing to scripts/v4/a4_runner.py:data_dir_for"). No `v4_paths.py` was needed for
this item; noted as a doc/actual discrepancy only.

---

## 4. Gate consequence

The day-edge erratum candidate is LIVE for v4: every v4 result produced by `a4_runner.py`
(Designs A/B/C, all cells, all horizons, all architectures) carries session-tail labels that span
closed-market gaps, with the affected rows retained in train, val, and test. The v5 LightGBM
results are not affected by this mechanism because their labels are session-guarded at generation
time (except the explicitly-declared next_trading_day_mode labels).
