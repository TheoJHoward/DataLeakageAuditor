# ITEM V7 — Does the v4 (and v5) pipeline carry the same-second residual channel?

Errata-queue item, not a tag gate. Method: static read first (the whole feature-join path,
verbatim quotes with line numbers), then two minimal measurements, because the static read
left exactly one question open — does the lattice v4/v5 load ever put two consecutive rows in
the same wall-clock second, and if so where do those rows fall? Archive
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025` read-only (timestamp column only); all writes under
this `v7\` directory.

## Verdict

| Pipeline | Verdict | Exposure |
|---|---|---|
| **v4** — `scripts\v4\a4_runner.py` | **CHANNEL PRESENT** — the fixture's exact construction: trade aggregates joined by EQUALITY on `floor(ts,'1s')`, causal lag applied as a one-**ROW** `shift(1)` | ~150-250 rows per instrument-year out of 4.1-21.1 M (measured); the affected row is the **last row of each reconstructed UTC day**, which for zc/zs/he/le sits **inside** the `afternoon` bucket and for es/nq/cl/gc inside `asia_overnight` |
| **v5** — `scripts\v5\v5_lightgbm_runner.py`, `v5_wave_runner.py` | **CHANNEL PRESENT** — byte-identical reuse of the same three v4 functions | Same lattice, **no bucket filter**, so every affected row reaches the feature frame |

Neither verdict is AMBIGUOUS: the code question is settled by the quotes in (a), the lattice
question by the counts in (b).

Files read in full or in all cited ranges:

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\a4_runner.py` (938 lines)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\g2_day_worker.py` (221 lines — writer of the v4 lattice)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\g2_reprocess.py` (month concat, lines 92-180)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v4\bucket_assigner.py` (lines 1-120)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\book_engine.py` (lines 310-417 — the v4 snapshot grid)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_mbo.py` (lines 322-370 — the he/le grid)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\pipeline\process_zc.py` (lines 250-287 — the phase-5 zc grid)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_lightgbm_runner.py` (293 lines)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_wave_runner.py` (lines 258-302)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\scripts\v5\v5_label_generator.py` (lines 50-130)

---

## (a) The v4 feature-join path, quoted

### a.1 — Trade aggregates attach by **exact equality on `floor(ts,'1s')`**, not by `merge_asof`

`scripts\v4\a4_runner.py:299-306` (function head — note the docstring):

```python
def add_trade_features(df: pd.DataFrame, trades: Optional[pd.DataFrame]) -> pd.DataFrame:
    """Merge-asof second-resolution aggregated trade stats into df."""
    for col in TRADE_FEATURES:
        df[col] = np.nan
    if trades is None or trades.empty:
        return df
    tr = trades.copy()
    tr["second"] = tr["ts_event"].dt.floor("1s")
```

`scripts\v4\a4_runner.py:311-319` (the per-second aggregate):

```python
    per_sec = tr.groupby("second").agg(
        net_delta=("signed_size", "sum"),
        buy_size=("buy_size", "sum"),
        sell_size=("sell_size", "sum"),
        trade_count=("size", "size"),
        large_count=("is_large", "sum"),
        vwap_num=("price", lambda s: (s * tr.loc[s.index, "size"]).sum()),
        total_sz=("size", "sum"),
    ).reset_index()
```

`scripts\v4\a4_runner.py:322-325` — **the join, decisive**:

```python
    # align with snapshot seconds
    tmp = df[["timestamp"]].copy()
    tmp["second"] = tmp["timestamp"].dt.floor("1s")
    merged = tmp.merge(per_sec, on="second", how="left")
```

`pandas.DataFrame.merge` on key `second` = **exact equality of the floored wall-clock
second**. `merge_asof` appears nowhere in `a4_runner.py` (grep: zero hits); the only
occurrences of the phrase in the two pipelines are prose that does not match the code —
`a4_runner.py:300` (docstring above) and `v5_wave_runner.py:3-4`
("3+ minute trade-feature merge_asof is the bottleneck").

Consequence, identical to the fixture's contaminated side: row *i* with decision time `T_i`
receives the aggregate of the **whole second `[floor(T_i), floor(T_i)+1s)`**, including trades
with `ts_event > T_i`. Nothing in the code compares an event time to `T_i`.

`scripts\v4\a4_runner.py:327-339` — everything derived from that join (row-indexed rolling
windows over the joined per-second values; no time-based windowing):

```python
    # rolling sums aligned to df row order (snapshots are ~1s apart, so
    # rolling(W) ~ window of W seconds)
    ndel = merged["net_delta"].fillna(0)
    df["net_delta_1s"] = ndel.rolling(1).sum().values
    df["net_delta_5s"] = ndel.rolling(5).sum().values
    df["net_delta_10s"] = ndel.rolling(10).sum().values
    df["net_delta_30s"] = ndel.rolling(30).sum().values
    df["net_delta_60s"] = ndel.rolling(60).sum().values
    df["buy_volume_10s"] = merged["buy_size"].fillna(0).rolling(10).sum().values
    df["sell_volume_10s"] = merged["sell_size"].fillna(0).rolling(10).sum().values
    df["trade_count_10s"] = merged["trade_count"].fillna(0).rolling(10).sum().values
    df["large_trade_count_10s"] = merged["large_count"].fillna(0).rolling(10).sum().values
    df["vwap_distance"] = (df["mid_price"] - merged["vwap"].values)
```

All ten `TRADE_FEATURES` (`a4_runner.py:115-121`) come from this join, and all ten are in
**both** `FULL_FEATURES` and `BFREE_FEATURES` (`a4_runner.py:122-123`).

### a.2 — The causal lag is a **row shift**, not a time shift, and it is not grouped

`scripts\v4\a4_runner.py:343-347`, verbatim and complete:

```python
def apply_causal_lag(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Shift all features by 1 second (use t-1 info to predict t+horizon)."""
    for c in feature_cols:
        df[c] = df[c].shift(1)
    return df
```

The docstring says "by 1 second"; the implementation is `Series.shift(1)` — **one ROW**. No
`freq=`, no `groupby`, no per-day or per-instrument grouping. It is called once on the whole
concatenated frame, `a4_runner.py:781-782`:

```python
    # apply causal lag to ALL features (both full + bfree use shifted values)
    feat_df = apply_causal_lag(feat_df, FULL_FEATURES)
```

(Separate consequence of the missing grouping, recorded for the errata queue but not pursued
here: the first row of every day / bucket window inherits the previous day's or previous
window's feature vector — staleness, not leakage.)

Order of operations per cell, `a4_runner.py:767-782`:

```python
    snap = load_snapshots(inst)
    ...
    filt = filter_to_bucket(snap, inst, bucket)
    ...
    trades = load_trades(inst)
    ...
    feat_df = build_snapshot_features(filt, inst)
    feat_df = add_trade_features(feat_df, trades)
    ...
    feat_df = apply_causal_lag(feat_df, FULL_FEATURES)
```

i.e. **bucket filter → features → second-equality join → row shift**. The lag therefore pairs
each row with its predecessor *inside the bucket-filtered frame*.

### a.3 — The lattice: v4 does **not** rebuild snapshots; it reads pre-built parquets

`scripts\v4\a4_runner.py:134-140` (generation routing):

```python
def data_dir_for(inst: str) -> Path:
    inst = inst.lower()
    if inst == "es":
        return ROOT / "processed" / "es" / "v4_morning_chunk"
    if inst in ("nq", "cl", "gc", "zc", "zs"):
        return ROOT / "processed" / inst / "v4_gapfill"
    return ROOT / "processed" / inst
```

`scripts\v4\a4_runner.py:194-206` (the loader):

```python
def load_snapshots(inst: str) -> pd.DataFrame:
    inst = inst.lower()
    d = data_dir_for(inst)
    dfs = []
    for mm in MONTHS:
        p = d / f"{inst}_snapshots_{mm}.parquet"
        if not p.exists():
            continue
        df = pq.read_table(str(p)).to_pandas()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        dfs.append(df)
    snap = pd.concat(dfs, ignore_index=True).sort_values("timestamp").reset_index(drop=True)
    return snap
```

with `MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]` (`a4_runner.py:89`). The frame the lag
runs over is therefore 12 months of one instrument, concatenated and sorted by timestamp,
**with no de-duplication and no per-day grouping**.

Generation per instrument: **es** → `processed\es\v4_morning_chunk\`; **nq, cl, gc, zc, zs** →
`processed\<inst>\v4_gapfill\`; **he, le** → `processed\<inst>\` (fall-through, line 140) —
i.e. for he/le the **same files as the Phase-5 lattice** named in the M5 sweep.

How each generation's grid is built (this is what decides the same-second question):

- **v4 generation** (`v4_gapfill`, `v4_morning_chunk`): one UTC day at a time —
  `g2_day_worker.py:137-139`
  (`day_start = pd.Timestamp(day_iso, tz="UTC")` / `day_end = day_start + pd.Timedelta(days=1)` /
  `df = df[(df["ts_event"] >= day_start) & (df["ts_event"] < day_end)]`), then
  `g2_day_worker.py:181-183`:
  ```python
          snaps = reconstruct_day(
              df, day_iso, snapshot_interval_seconds=1.0, levels=5
          )
  ```
  month-concatenated with no sort and no dedupe (`g2_reprocess.py:140-141`:
  `snap_df = pd.concat(snap_dfs, ignore_index=True)` / `snap_df.to_parquet(snap_out, ...)`).
  Inside `scripts\pipeline\book_engine.py:350` the grid is
  `next_snapshot_ts = ts_events[0] + np.timedelta64(interval_ns, "ns")`, advanced only by
  `interval_ns` (`:364`) — so **within a UTC day rows are exactly 1 s apart**, at whatever
  sub-second phase the day's first event had. Then one extra row per day,
  `book_engine.py:388-392`:
  ```python
      # Final snapshot
      if ts_events[-1] >= next_snapshot_ts - np.timedelta64(interval_ns, "ns"):
          snap = book.get_book_snapshot(levels=levels)
          snap["timestamp"] = pd.Timestamp(ts_events[-1])
          snapshots.append(snap)
  ```
  — stamped at the day's **last event**, i.e. < 1 s after the last grid point, hence usually in
  the *same wall-clock second* as it. **That is the whole source of the channel in v4.**

- **he/le generation** (`scripts\pipeline\process_mbo.py:342-368`): same 1 s grid, plus a
  re-anchor after gaps > 60 s (`:347-352`: `gap = (ts - next_snap).astype("int64")` /
  `if gap > max_gap_ns:` … `next_snap = ts`) and the same terminal row
  (`:365-368`, `snap["timestamp"] = pd.Timestamp(ts_events[-1])`). A re-anchor changes the
  sub-second phase but leaves a >60 s gap between the two rows involved, so it does not itself
  create a same-second pair; the terminal row does.

---

## (b) Can two consecutive rows share a wall-clock second — and does the shift leave a residual?

**Structurally: yes and yes.** Write `S_i = floor(T_i, 1s)`. After `add_trade_features`, row
*i* carries the aggregate of `[S_i, S_i+1s)`; after the one-row shift, row *i* carries the
aggregate of `[S_{i-1}, S_{i-1}+1s)`.

- `S_{i-1} < S_i` (rows 1 s apart, the normal case): every delivered event is strictly before
  `S_i ≤ T_i` → no availability violation.
- `S_{i-1} == S_i` (two consecutive rows inside one second): row *i* is handed **its own
  second**, so every event in it with `ts_event > T_i` is post-decision → **availability
  violation, identical in kind to the Phase 5/7 fixture's corrected side**.

**Measurement 1 — how often `S_{i-1} == S_i` in the lattice v4/v5 actually load.**
Timestamp column only; replicating `load_snapshots` exactly (concat 2025-01…2025-12 →
`sort_values("timestamp")`):

| inst | directory `data_dir_for` returns | rows (12 mo) | same-second adjacent pairs | exact duplicate ts | adjacent gaps < 1 s |
|---|---|---:|---:|---:|---:|
| es | `processed\es\v4_morning_chunk` | 21,094,473 | **250** | 0 | 250 |
| nq | `processed\nq\v4_gapfill` | 21,093,391 | **249** | 0 | 250 |
| cl | `processed\cl\v4_gapfill` | 21,094,993 | **233** | 0 | 250 |
| gc | `processed\gc\v4_gapfill` | 21,095,855 | **247** | 0 | 250 |
| zc | `processed\zc\v4_gapfill` | 19,106,953 | **237** | 0 | 250 |
| zs | `processed\zs\v4_gapfill` | 19,107,618 | **229** | 0 | 250 |
| he | `processed\he` | 4,131,656 | **166** | 1 | 251 |
| le | `processed\le` | 4,131,877 | **149** | 1 | 251 |

`adjacent gaps < 1 s` is exactly 250 for all six v4-generation instruments, and
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc\v4_gapfill\zc_mbo_2025-*\zc_snapshots_*.parquet`
counts 250 per-day files (21+19+21+21+21+20+22+21+21+23+18+22). One sub-second-spaced
adjacency per reconstructed day, exactly as `book_engine.py:388-392` predicts; the same-second
count is slightly lower because some terminal rows land in the *next* second. Pairs are
isolated (never three rows in one second), and `exact duplicate ts` is 0/1 — the concatenation
introduces no extra adjacency.

**Measurement 2 — where the affected rows fall**, i.e. which v4 cells keep them. For each
same-second pair the *later* row (the one that receives the residual) was classified with the
archive's own `bucket_assigner.assign_buckets`, months 2025-01 / 2025-08:

| inst | pairs 01 / 08 | bucket of the affected row (01) | bucket of the affected row (08) |
|---|---|---|---|
| es | 21 / 21 | `asia_overnight` 16, `outside_session` 5 | `asia_overnight` 16, `outside_session` 5 |
| nq | 21 / 20 | `asia_overnight` 16, `outside_session` 5 | `asia_overnight` 15, `outside_session` 5 |
| cl | 17 / 20 | `asia_overnight` 16, `outside_session` 1 | `asia_overnight` 16, `outside_session` 4 |
| gc | 21 / 21 | `asia_overnight` 16, `outside_session` 5 | `asia_overnight` 16, `outside_session` 5 |
| zc | 14 / 21 | **`afternoon` 14** | **`afternoon` 5**, `outside_session` 16 |
| zs | 18 / 21 | **`afternoon` 18** | **`afternoon` 5**, `outside_session` 16 |
| he | 15 / 15 | **`afternoon` 15** | **`afternoon` 15** |
| le | 14 / 13 | **`afternoon` 14** | **`afternoon` 13** |

Sample affected pairs (verbatim from the probe):

```
zc 2025-01: 2025-01-02 19:19:59.199155501+00:00 -> 2025-01-02 19:19:59.869251991+00:00   (NY 14:19:59.869)
he 2025-01: 2025-01-03 19:04:59+00:00           -> 2025-01-03 19:04:59.753047879+00:00   (NY 14:04:59.753)
es 2025-01: 2025-01-02 23:59:59.000011059+00:00 -> 2025-01-02 23:59:59.862084861+00:00   (NY 18:59:59.862)
es 2025-01: 2025-01-03 22:00:00.000011323+00:00 -> 2025-01-03 22:00:00.064126539+00:00   (NY 17:00:00.064)
```

Reading (day-of-week and NY clock time verified directly, 2025-08 sample):

- **es/nq/cl/gc** — 16 rows/month at **19:59:59 NY, Mon-Thu** (= 23:59:59 UTC, the UTC-day
  cut, EDT), inside `asia_overnight` → **retained**; 5 rows/month at **17:00:00 NY, Fridays**
  (the Friday close, no evening session after it), labelled `outside_session` → dropped.
  In EST months the same Mon-Thu rows read 18:59:59 NY, still inside `asia_overnight`.
- **zc/zs** — Fridays: **14:19:59 NY**, the grain session close, inside `afternoon` (12:30→14:20)
  and `full_session` → **retained** (5/month in 2025-08; all 14 resp. 18 pairs in 2025-01, an
  EST month where the UTC day ends before the 20:00 NY reopen). Mon-Thu in EDT months:
  **19:59:59 NY**, one second before the 20:00 NY overnight open, `outside_session` → dropped.
- **he/le** — all at **~14:04:5x NY**, the livestock session close, inside `afternoon`
  (12:30→14:05) and `full_session` → **retained**, every trading day.

So **v4 retains the affected rows** in `asia_overnight` + `full_session` (es/nq/cl/gc) and in
`afternoon` + `full_session` (zc/zs/he/le); it drops them in every other bucket. Filtering
cannot *create* new same-second adjacencies here because the pairs are isolated.
**v5 retains all of them** — `v5_lightgbm_runner.py:13-14`: "Uses full-session data (no bucket
filtering — v5 is bucket-agnostic)".

**Magnitude.** Order 10^2 rows per instrument-year against 4.1-21.1 x 10^6 (≈ 0.001-0.004 %),
one per trading day, always the session's terminal row. The mechanism is the fixture's; the
incidence on this lattice is not.

Artifacts (all under
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\v7\`):
`lattice_same_second_probe.py` + `probe_stdout.txt` + `lattice_same_second_probe.csv`
(measurement 1, 1208.6 s for 8 instruments x 12 months + the 7-instrument x 2-month Phase-5
cross-check); `affected_row_buckets.py` + `affected_row_buckets_stdout.txt` +
`affected_row_buckets.csv` (measurement 2); `affected_row_dow_verify.txt` (NY clock time and
day-of-week of every affected row, zc/es 2025-08).

### Cross-check on the Phase-5 lattice (raw, no reconciliation attempted)

Same probe, `processed\{inst}\{inst}_snapshots_{month}.parquet` (M5's lattice; = the v4 lattice
only for he/le), months 2025-01 and 2025-08. "file order" = rows as stored; "sorted" = after
`sort_values("timestamp")`, which both M5's checker and `load_snapshots` do:

| inst | 2025-01 rows / pairs (file order) | 2025-08 rows / pairs (file order) | pairs after sorting the two months | exact dup ts (sorted) |
|---|---|---|---:|---:|
| zc | 1,262,191 / 20 | 1,666,968 / 20 | **297,426** | 101,651 |
| zs | 1,275,375 / 16 | 1,597,846 / 17 | **200,437** | 56,272 |
| gc | 1,884,670 / 20 | 1,851,278 / 19 | **172,496** | 21,293 |
| cl | 1,939,381 / 18 | 1,809,537 / 15 | **177,786** | 21,337 |
| es | 1,811,402 / 30 | 1,757,598 / 25 | 55 | 5 |
| he | 343,499 / 15 | 346,496 / 15 | 30 | 1 |
| le | 343,507 / 14 | 346,498 / 13 | 27 | 1 |

A separate single-file run isolates it: `processed\zc\zc_snapshots_2025-08.parquet` alone has
20 same-second pairs in file order but **297,406 after sorting, with 101,650 exact duplicate
timestamps**, while `zc_snapshots_2025-01.parquet` has 20 either way. I.e. the Phase-5 month
file for zc 2025-08 stores multiple interleaved/duplicated snapshot series that only collide
once sorted. Same signature for zs, gc, cl; not for es, he, le.

This is a property of the **Phase-5** lattice, not of the lattice v4/v5 load for those four
instruments (`v4_gapfill` shows 0 duplicate timestamps and ~250 pairs per year). No comparison
with the M5 counts is made here: M5 measured *absorbed events violating availability*, per
event class, on the session-hour-filtered lattice; this item measures *adjacent row pairs
sharing a second*, unfiltered. Different statistics — reported raw, side by side, and not
reconciled.

---

## (c) v5 — same question, labelled separately

v5 implements no feature join of its own; it imports the v4 module and calls the same three
functions. `scripts\v5\v5_lightgbm_runner.py:3-8` (docstring):

```
Reuses v4's a4_runner module byte-identically for:
  - Path routing (data_dir_for)
  - Snapshot/trade loading
  - Feature engineering (build_snapshot_features, add_trade_features)
  - Causal lag (shift(1))
```

`v5_lightgbm_runner.py:43` `import a4_runner as r`, and `:95-111`:

```python
        snap = r.load_snapshots(inst)
        ...
        trades = r.load_trades(inst)
        ...
        feat = r.build_snapshot_features(snap, inst)
        del snap; gc.collect()
        log(f"  adding trade features...")
        feat = r.add_trade_features(feat, trades)
        del trades; gc.collect()

        # apply causal lag using superset (Full) — BFree is a subset
        log(f"  applying causal lag (Full feature set, BFree is subset)...")
        feat = r.apply_causal_lag(feat, r.FULL_FEATURES)
```

The batch driver does the same once per instrument and passes the frame to every cell,
`scripts\v5\v5_wave_runner.py:270-282` and `:295`:

```python
    snap = r.load_snapshots(inst)
    ...
    trades = r.load_trades(inst)
    ...
    feat = r.build_snapshot_features(snap, inst)
    del snap; gc.collect()
    log(f"  adding trade features (~3 min for big instruments)...")
    feat = r.add_trade_features(feat, trades)
    del trades; gc.collect()
    log(f"  applying causal lag (Full feature set, BFree is subset)...")
    feat = r.apply_causal_lag(feat, r.FULL_FEATURES)
...
            result = run_cell(inst, h, fset, preloaded_feat=feat)
```

v5-specific differences — they change the exposure, not the mechanism:

1. **No bucket filter** (`v5_lightgbm_runner.py:13-14`, quoted in (b)). Every same-second row
   in the lattice reaches the model frame, including the es/nq/cl/gc Friday-close and the
   zc/zs pre-open rows that v4 drops.
2. **Labels join after the lag**, by exact timestamp equality (`v5_lightgbm_runner.py:120-122`):
   ```python
   feat = feat.merge(
       lab[["timestamp_t", "y"]],
       left_on="timestamp", right_on="timestamp_t", how="inner")
   ```
   so an affected row is used iff `v5\labels\<inst>_h<h>.parquet` carries a label at that exact
   timestamp. The label generator builds its timestamps from the same lattice
   (`v5_label_generator.py:60-67` — `data_dir_for` is a byte-identical copy of the v4 routing;
   `:70-87` `load_all_snapshots` globs `<inst>_snapshots_*.parquet` from it), so the terminal
   rows are candidates; whether each gets a non-NaN label depends on the label rule and was
   not measured here.
3. Same instrument routing, so v5's he/le runs use the Phase-5-generation files.

**v5 verdict: CHANNEL PRESENT**, same mechanism, same lattice, wider row exposure than v4.

---

## (d) Verdicts and affected published claims

| Pipeline | Verdict | Decisive quotes |
|---|---|---|
| **v4** (`a4_runner.py`) | **CHANNEL PRESENT** | join: `a4_runner.py:325` `merged = tmp.merge(per_sec, on="second", how="left")` with `:324` `tmp["second"] = tmp["timestamp"].dt.floor("1s")`; lag: `a4_runner.py:346` `df[c] = df[c].shift(1)`; lattice: `book_engine.py:391` `snap["timestamp"] = pd.Timestamp(ts_events[-1])` |
| **v5** (`v5_lightgbm_runner.py`, `v5_wave_runner.py`) | **CHANNEL PRESENT** | `v5_lightgbm_runner.py:43, 106, 111` and docstring `:3-8`; `v5_wave_runner.py:279, 282` |

**Published claims affected** (reusing the C6b era map,
`…\scratchpad\fixture_spike\c6\era_attribution.md`, which attributes Claims 1 and 2 to v4):

- **Claim 1 — headline AUCs.** `main_paper.txt:59-61` ("The strongest cells (corn futures
  overnight, AUC = 0.873) …") and IA.1 (`ia.txt:29` "zc full_session 0.3545 0.8579 CNN 5 T1
  EXPLORATORY"). Produced by `a4_runner.py` Design-A runs, i.e. by the audited feature path.
  Per measurement 2 the affected rows are in the buckets as follows:
  - **zc `full_session`** (the IA.1 0.8579 cell): the `afternoon` rows are inside
    `full_session` → **exposed** (14 rows in 2025-01, 5 in 2025-08 of ~1.3-1.7 M month rows).
  - **zc `overnight`** (the abstract's 0.873 cell): `overnight` is 20:00→08:45 NY and contains
    none of the affected rows → **not exposed**.
  - es/nq/cl/gc `asia_overnight` and `full_session` cells in the same IA.1 table → **exposed**;
    their `europe_overnight`/`open`/`morning`/`midday`/`afternoon_close` cells → not exposed.
  - zs `afternoon` + `full_session`, and he/le `afternoon` + `full_session` → **exposed**
    (he/le every trading day); zc/zs `overnight`/`open`/`morning` and he/le `open`/`morning`
    → not exposed.
- **Claim 2 — §9.4 feature importance / ablation.** `main_paper.txt:1138-1142` (582 ablation
  runs, max single-feature impact 2.16 %, `vwap_distance` / `net_delta_1s` / `l1_imbalance`
  named). Per C6b, `scripts\v4\a9_leakage_ablation.py:33, 93-94` imports `a4_runner` and
  rebuilds the same features, so it inherits the same join + shift; the two named trade
  features are both products of the equality join (`a4_runner.py:329-339`).
- **v5 outputs** (`results\v5\runs\*.json`, `results\v5\summaries\all_runs.csv`,
  `MASTER_FINDINGS\v5\03_ml_runs\`) inherit the channel wherever v5 numbers are published;
  C6b's map covers v4 claims only, so no v5 published sentence is named here.

**Scope of the erratum this supports.** The defensible statement is a
**mechanism/description correction**: v4 and v5 attach trade aggregates by wall-clock-second
equality and then lag by one *row*, so the pipeline does not guarantee the availability
property its own docstring asserts ("Shift all features by 1 second"); on the v4/v5 lattice
this leaves a measured residual on ~1 row per instrument-trading-day, at the session's terminal
row, retained in the `asia_overnight`/`afternoon`/`full_session` cells. It is **not** support
for a claim that published v4 AUCs are materially driven by this channel — quantifying any AUC
impact would require re-running cells, which is outside this item.

**Note for the record (not a measurement contradiction).** C6a
(`…\fixture_spike\c6\a4_defect_audit.md:305-306`) writes "Causal lag (`a4_runner.py:343-347
apply_causal_lag`) shifts all of these by 1 second" — that restates the function's docstring.
The implementation is `.shift(1)` on rows (`a4_runner.py:346`), which equals one second only
where the lattice is exactly 1 s spaced. C6a's own verdicts (classifier CORRECTED, dtype
CARRIED) are untouched by this item.
