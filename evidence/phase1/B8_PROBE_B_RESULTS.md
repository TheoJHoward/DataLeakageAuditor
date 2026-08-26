# B8 — PROBE B AGAINST THE ACCEPTANCE FIXTURE: THE COLUMN DEPENDENCY MAP

**What this is.** The first output of the tool. For each source column of the
acceptance fixture's corrected side, the column was corrupted and `build` re-run;
movement in the output means the pipeline reads that column. `zc` `2025-01`,
corrected side, 47 cohorts.

**What this is NOT.** It is **not scored against the declared ground-truth map,
and must not be.** `PREREG.md` SC-7(c) keeps that map out of the tool's input
surface, and this output is a **dependency map — Layer 1** — not a verdict set.
Presenting it as verdicts would be this tool making exactly the claim it exists
to catch other tools making.

| | |
|---|---|
| cohorts probed | **47** |
| fired | **33** |
| silent | **14** |
| baseline digest, identical across all four workers | `d8712f163cf9dcb6…` |
| reducers | **accepted both traces unchanged** |

**The excluded MBO frame appears in no probe population.** `not_probed` records
exactly `other:zc_mbo_2025-01.parquet`, and no cohort id derives from it. Serving
the aggregate means the builder never opens the raw frame, so probing its columns
would have recorded a silence the adapter caused and this document would have
presented it as a fact about the pipeline.

---

## 1. PER SOURCE FRAME

| frame | fired | silent | total |
|---|---|---|---|
| `snap` | 24 | 0 | 24 |
| `magg` | 6 | 0 | 6 |
| `trades` | 3 | **14** | 17 |

Every column of the snapshots and MBO-aggregate frames is read. **Fourteen of
seventeen trades columns are not** — and §3 gives the mechanism for the ones that
matter.

## 2. WHAT MOVED, FOR THE COHORTS THAT FIRED

**Book prices — one feature each.** `bid_price_1..5`, `ask_price_1..5` each move
only themselves: they pass through, and nothing derived reads them.

**Book sizes — eight to ten each.** `bid_size_1` and `ask_size_1` move ten
features including `book_slope_*` and `l1_imbalance`; the deeper levels move
eight, without the level-1-only features. The fan-out is `depth_change_{1,5,30}s`,
`depth_imbalance`, `depth_pctile_{60,300}s`, `total_*_depth`.

**The two widest.**

- `snap.timestamp` → **50 features.** It drives the hour filter, the session
  window and every rolling window, so nearly the whole frame is downstream of it.
- `snap.mid_price` → **16**, including all four `fwd_move_ticks_*` labels and
  every `mid_return_*`. It is the label base, and the probe shows it.

**The cross-frame joins are live**, which is the result that justifies `raw`
being a dict of frames rather than one:

- `magg.ts_floor` → **16 features**; `trades.ts_event` → **15**. These are the
  join keys, and perturbing them moves everything downstream of the merge.
- `trades.size` → **15**: `net_delta_*`, `trade_volume_*`, `large_trade_count*`,
  `sell_volume_10s`, `vwap_distance`.
- `trades.price` → **2**: `vwap`, `vwap_distance`.

## 3. THE SILENCE ACCOUNTING (§39)

**A silence without its domain is not a result.** Fourteen cohorts produced no
movement, and they are not one kind of thing.

| cohort | strategies that VALIDLY ran | invalid, and why |
|---|---|---|
| `trades.action` | **NONE** | sentinel=compatibility, shuffle=control_artifact |
| `trades.symbol` | **NONE** | sentinel=compatibility, shuffle=control_artifact |
| `trades.channel_id` | nan, sentinel | shuffle=control_artifact |
| `trades.instrument_id` | nan, sentinel | shuffle=control_artifact |
| `trades.publisher_id` | nan, sentinel | shuffle=control_artifact |
| `trades.rtype` | nan, sentinel | shuffle=control_artifact |
| `trades.aggressor_side` | shuffle | sentinel=compatibility |
| `trades.side` | shuffle | sentinel=compatibility |
| `trades.flags` | nan, sentinel, shuffle | — |
| `trades.is_buy_aggressor` | nan, sentinel, shuffle | — |
| `trades.order_id` | nan, sentinel, shuffle | — |
| `trades.sequence` | nan, sentinel, shuffle | — |
| `trades.ts_in_delta` | nan, sentinel, shuffle | — |
| `trades.ts_recv` | sentinel, shuffle | — |

**`trades.action` and `trades.symbol` are NOT observed silence.** No strategy ran
validly on either, so the evidence outcome for those cohorts is `none`, not
`observed_silence`. **A probe that did not happen found nothing, and that is not
the same as a probe that happened and found nothing.** Reporting them as silence
would be the exact error §39 exists to prevent.

**`control_artifact` means the perturbation was the identity.** Those columns are
single-valued in this month, so a permutation of identical values changes no
byte. The probe never ran; it is recorded as an artifact of the control, not as
a null.

**`compatibility` means the strategy had no realisation on that dtype** — no
in-dtype out-of-range value exists for those object columns.

## 4. A FINDING THE PROBE SURFACED — the aggressor predicate never matches

**`trades.aggressor_side` is silent under a VALID shuffle, and the builder
demonstrably reads it.** That combination is either a real property of the
pipeline or a hole in the probe, so it was checked rather than reported.

The builder computes

```python
is_buy = trades["aggressor_side"].isin(["B","Buy","buy"])
```

and the column's actual values, read from the source parquet, are

| value | rows |
|---|---|
| `SELL_AGGRESSOR` | 197,640 |
| `BUY_AGGRESSOR` | 172,705 |
| `UNKNOWN` | 27,112 |

**None of them is `B`, `Buy` or `buy`.** `is_buy` is therefore **False for every
row**, and:

- `buy_vol = where(is_buy, size, 0)` is **identically zero**
- `sell_vol = where(~is_buy, size, 0)` **always equals `size`**
- `net_delta = where(is_buy, size, -size)` is **always `-size`**

So `buy_volume_10s` is a constant zero, `sell_volume_10s` duplicates
`trade_volume_10s`, and `net_delta_*` is the negation of volume rather than a
signed flow. **Shuffling `aggressor_side` cannot move the output, because the
predicate is false for every permutation of those values.** The silence is
correct, and it names a mechanism.

`trades.side` is silent for a different reason in the same sentence: the
`aggressor_side` branch is taken, so `side` is never read at all.

**Independent corroboration, arrived at from the other direction.**
`AVAILABILITY_DECLARATION.md` §D.1 item 2 freezes `buy_volume_10s` as one of two
**UNSCORED** columns, described as a *"degenerate constant"*. The declaration
recorded the **symptom** by measuring the fixture; this probe recovered the
**mechanism** by perturbing it, without being given the declaration. Two
independent routes to the same column is the strongest form this evidence takes.

**This is a Layer 1 dependency fact, and it is left there.** Whether a constant
`buy_volume_10s` is a leak, a defect, or neither is a Layer 2 question about the
declared map, and this document does not reach it.

## 5. THE SCHEDULE

| combination | state | outcome | cohorts | records | valid |
|---|---|---|---|---|---|
| preserving | `incomplete(compatibility)` | `finding` | 47 | 433 | 422 |
| promoted | `completed` | `finding` | 25 | 127 | 127 |

**346 evidence events, 228 licensing PROVEN.**

`incomplete × finding` is legal and §6.6 names this case in terms: *"A case can
be `incomplete(compatibility)` and `finding` at once."* The eleven invalid
records are the schedule failing honestly — six `control_artifact`, four
`compatibility`, and one `crash` (`snap.timestamp` under sentinel, where pushing
the stamp to 2262 genuinely breaks the pipeline; recorded as `CRASH`, never
collapsed into determinism).

**The reducers accepted both traces without modification.** The scoring machinery
predates the tool and was not adjusted to accommodate it.

## 6. PROVENANCE

Four worker processes, threads pinned to one, round-robin cohort assignment, all
four reporting the identical baseline digest. **Equivalence to a serial run was
measured, not assumed:** an earlier serial run — unpinned threads, one process —
completed 15 cohorts before an unrelated defect ended it; those 15 were
snapshotted and compared against the parallel result, **15/15 identical, cohort
for cohort.**

The merge refuses rather than warns on three conditions: shards disagreeing on
the baseline, an incomplete shard, or a cohort covered twice or not at all. A
dropped cohort would read downstream as `observed_silence` — a finding-shaped
absence.
