# B9 — `valueread` AND `nullread` AGAINST THE ACCEPTANCE FIXTURE

**What this is.** The second and third detectors, run over the same 47 source columns as B8's
`columndep`, on `zc` `2025-01`, corrected side. `valueread` asks whether the output reads a column's
**values**; `nullread` asks whether it reads its **null pattern**.

**What this is NOT.** Not scored against the declared ground-truth map, and it must not be.
`PREREG.md` SC-7(c) keeps that map out of the tool's input surface. This is a **dependency map —
Layer 1**, not a verdict set.

**Same pipeline as B8, provably.** All four workers report baseline digest `d8712f163cf9dcb6…`,
identical to B8's, so the three detectors' results are about one object.

| | `valueread` | `nullread` |
|---|---|---|
| preserving | `incomplete(compatibility)` × `finding` — 47 cohorts, 433 records, **422 valid** | `incomplete(crash)` × `finding` — 22 cohorts, 68 records, **63 valid** |
| promoted | `completed` × `finding` — 25 cohorts, 125 records, **125 valid** | `completed` × `finding` — 25 cohorts, 127 records, **127 valid** |
| evidence events | 344 (**228** license PROVEN) | 180 (**62** license PROVEN) |
| fired / silent | **33 / 14** | **32 / 15** |

**The reducers accepted all four traces unchanged.** `resolve_state_pair` raises on an illegal pair
and did not.

**`nullread`'s two combinations partition the columns: 22 + 25 = 47**, no overlap, none uncovered —
asserted by the merge at run time, not argued here.

---

## 1. THE HEADLINE IS A NEGATIVE RESULT, AND IT IS THE HONEST ONE

Per `(cohort, feature)` pair, across every strategy in both detectors:

| strategy | pairs found | over cohorts | **pairs no other strategy found** |
|---|---|---|---|
| `shuffle` | 226 | 33 | — |
| `sentinel` (in-dtype) | 178 | 32 | — |
| **`sentinel_ood`** (out-of-dtype) | 116 | 16 | **0** |
| **`nan`** | 180 | 32 | **2** |

### 1.1 The out-of-dtype sentinel added nothing on this fixture

**`sentinel_ood` found zero pairs that `shuffle` or the in-dtype `sentinel` had not already found.**
Its promoted combination cost a determinism guard and a promoted baseline for each of 25 cohorts and
returned no coverage the preserving side lacked.

That is not evidence the strategy is pointless. Its reason for existing — **at a column pinned to
its dtype's ceiling both preserving strategies degenerate to the identity, and only an out-of-dtype
value can perturb at all** — is demonstrated in `test_detectors.py`. It is evidence that **this
fixture contains no such column**, which is a fact worth having and could not have been known
without running it.

### 1.2 The null detector found exactly two things, and they are real

**`nan` found two `(cohort, feature)` pairs no value strategy can reach:**

| cohort | feature |
|---|---|
| `col:trades.size` | `trade_count` |
| `col:trades.size` | `trade_count_10s` |

The builder computes `trade_count=("size","count")`. **A groupby count counts non-null values**, so a
permutation of `size` cannot move it and neither can an in-dtype sentinel — the multiset and the
null pattern both survive. Introducing a null does move it. **That is a pure null-mask dependency,
and it is structurally invisible to a value probe.**

### 1.3 The gap `columndep` published is real in principle and EMPTY in fact

`columndep`'s domain statement said: `nan` is configured only in its promoted combination, `nan`
promotes only on integer and boolean columns, therefore **a float column never receives a null**,
and a feature reading one only through its null mask would be reported silent.

`nullread`'s **preserving** combination is exactly that missing probe: `nan` over the **22**
float, datetime and object columns. **Sixteen of the 22 fired — and every feature they moved was
already found by `shuffle` or `sentinel`.**

**So the gap is measured closed with nothing behind it.** The two null-only findings above are on
`trades.size`, an **integer** column, which is `nullread`'s *promoted* side — the combination
`columndep` already had. **The published gap cost this fixture nothing.** That is a weaker result
than the gap statement implied, and it is stated plainly rather than left for a reader to work out.

---

## 2. THE THREE DETECTORS AGREE WHERE THEY SHOULD, AND DIFFER WHERE THEY SHOULD

`valueread`'s preserving combination runs the same two strategies over the same columns as
`columndep`'s. **It reproduces it exactly**: the same 33 cohorts fired, with identical feature sets
— **except one cohort.**

| cohort | `columndep` | `valueread` |
|---|---|---|
| `col:trades.size` | 15 features | **13** features |

The two missing are `trade_count` and `trade_count_10s` — §1.2's null-only pair. `columndep` found
them **through its promoted combination, which runs `nan`**; `valueread` never runs `nan` and
therefore cannot. **This is the split working as designed**, and it is worth stating because a
difference between two detectors over the same strategies would otherwise read as a defect. It was
checked, not assumed.

---

## 3. THE SILENCE ACCOUNTING (§39)

**A silence carries the domain that produced it, or it is not a result.** `evidence_outcome` is
per-combination and is the wrong grain for this: a combination reads `finding` if *any* cohort
produced one. So each silent cohort is reported with the strategies that ran **validly**.

### 3.1 `valueread` — 14 silent, of which 2 are `none`

| cohort | ran validly | invalid, and why |
|---|---|---|
| `trades.action` | **NONE** | `sentinel`=compatibility, `shuffle`=control_artifact |
| `trades.symbol` | **NONE** | `sentinel`=compatibility, `shuffle`=control_artifact |
| `trades.aggressor_side` | `shuffle` | `sentinel`=compatibility |
| `trades.side` | `shuffle` | `sentinel`=compatibility |
| `trades.channel_id`, `instrument_id`, `publisher_id`, `rtype` | `sentinel`, `sentinel_ood` | `shuffle`=control_artifact |
| `trades.flags`, `is_buy_aggressor`, `order_id`, `sequence`, `ts_in_delta` | `sentinel`, `sentinel_ood`, `shuffle` | — |
| `trades.ts_recv` | `sentinel`, `shuffle` | — |

**`observed_silence` 12 · `none` 2.** `trades.action` and `trades.symbol` had **no strategy run
validly**, so their outcome is `none`. **A probe that did not happen found nothing, and that is not
the same as a probe that happened and found nothing.**

### 3.2 `nullread` — 15 silent, of which 5 are `none`, and all five are CRASHES

| cohort | `nan` outcome |
|---|---|
| `snap.timestamp` | **crash** |
| `trades.action` | **crash** |
| `trades.aggressor_side` | **crash** |
| `trades.side` | **crash** |
| `trades.symbol` | **crash** |
| `trades.channel_id`, `flags`, `instrument_id`, `is_buy_aggressor`, `order_id`, `publisher_id`, `rtype`, `sequence`, `ts_in_delta`, `ts_recv` | ran, no movement |

**`observed_silence` 10 · `none` 5.**

**The five crashes are a fact about the pipeline, recorded as `could_not_run(crash)` and never as a
finding.** Introducing a null into any of four object/string columns or into `snap.timestamp` kills
the build. **The builder has no null tolerance on those five columns** — which is a data-quality
property worth knowing, and also the reason the null detector can say nothing about them.

**`snap.timestamp` is the one cohort that fires in `columndep` and `valueread` (50 features) and is
silent in `nullread`.** It is not a disagreement: the null probe crashed there and its outcome is
`none`, not silence.

---

## 4. THE `aggressor_side` CLASS IS STILL UNREACHED — and the reason is sharper than expected

R135 predicted that the null detector would not catch `trades.aggressor_side` because *"the
mechanism is a constantly false predicate, not a null pattern."* Both halves are true, and the run
adds a **proximate** reason that is more immediate than either: **`nan` on `aggressor_side`
crashes the builder**, so the null probe never reaches the comparison at all.

So the class survives all three detectors, for two independent reasons:

- **no value probe can see it** — `isin(["B","Buy","buy"])` is false for every value of
  `SELL_AGGRESSOR` / `BUY_AGGRESSOR` / `UNKNOWN`, so no permutation and no in-dtype sentinel can
  move the output;
- **no null probe can see it either** — the strategy that would introduce a null cannot execute.

`tests/phase1/reference_but_silent.py` now finds this class mechanically, by intersecting the
builder source's column references with the cohorts no probe moved. Over these results it reduces
14 silences to **one** column a human must read. Whether that earns a third detector is a design
question and is left open.

---

## 5. PROVENANCE

Four worker processes, threads pinned to one before numpy is imported, round-robin cohort
assignment over `(frame, column)` cohort **ids** rather than bare column names — two frames sharing
a name would otherwise put one cohort in two shards.

**The harness calls the shipped detectors** with a `cohorts=` subset rather than reimplementing the
probe loop, so the thing under test is the shipped code path (H-L26).

**The merge refuses rather than warns**, on four conditions, and all four were demonstrated firing
on deliberately broken inputs before this run — each returning a real non-zero exit status and
writing no output: shards disagreeing on the baseline, an incomplete shard, a cohort covered twice,
and shards resolving different strategy sets for the same combination.

**Seeds are SHA-256 derived** and stable across processes (R134). This run is re-runnable to the
same trace; B8's original was not, and B8's fixed-seed re-run reproduced its merged artifact byte
for byte.

**Excluded from the population:** `other:zc_mbo_2025-01.parquet`, the 8.2M-row raw MBO frame. The
adapter serves the `magg` aggregate from memory, so the builder never opens the raw frame, and
probing its columns would record a silence the adapter caused.
