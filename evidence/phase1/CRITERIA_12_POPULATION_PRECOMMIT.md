# CRITERIA 1 AND 2 ACROSS THE DECLARED POPULATION — THE PRE-COMMITMENT

**Committed before the harness is executed.** Nothing below is adjusted once a
number is visible. If the harness turns out to be wrong that is a finding, it is
recorded, its fix is a separate commit, and the re-run is a second and separately
labelled result with the first still in the record.

**`CRITERIA_12_PRECOMMIT.md` (`58fe726`) is not superseded and not void.** It was
written for one instrument-month, its run is committed at `6b242b3`, and it
stands as what it is. This is a second and wider pre-commitment; §5 below states
exactly what in it was specific to zc 2025-01 and therefore had to be
re-established rather than carried.

---

## 1. THE INVOCATION, EXACTLY

```
ACC_INSTRUMENTS=cl,es,gc,he,le,nq,zc,zs \
ACC_MONTHS=2025-01,2025-08,2025-09,2025-10,2025-11,2025-12 \
ACC_STRIDE=997 ACC_MAX_COHORTS=300 ACC_SEED=20260828 \
PYTHONPATH=<repo>;<repo>/src \
python tests/phase1/harness_criteria_12_population.py
```

**Harness:** `tests/phase1/harness_criteria_12_population.py`, committed with
this file. **Output:** `evidence/phase1/criteria_12_population.json`,
checkpointed after every instrument-month. **stdout / stderr / exit status:**
captured to files and committed unmodified.

**Stride, cohort cap and seed are unchanged from the zc 2025-01 run**, so this
run is comparable with the recorded one rather than tuned against it.

**One run.** Interrupted and resumed from checkpoint with nothing read, it is one
run. Resumed after any criterion output has been read, it is a second run and
both are recorded. The test is not why it stopped but whether anything was looked
at before it continued.

## 2. THE POPULATION — enumerated, and it is the whole declared one

**The declared scored population is 48 instrument-months**: 8 instruments (`cl`,
`es`, `gc`, `he`, `le`, `nq`, `zc`, `zs`) x 6 months (`2025-01`, `2025-08`,
`2025-09`, `2025-10`, `2025-11`, `2025-12`), which is §13(a)'s scope and the
2 x 8 x 6 x 10 = 960 declared cells of the map.

**The archive on this machine carries all 48.** Verified by enumerating the
files the fixture's own loader reads — `<sym>_snapshots_<month>.parquet`,
`<sym>_trades_tagged_<month>.parquet`, `<sym>_mbo_<month>.parquet` — under the
archive's processed directory. Snapshots and trades are present for all 48.

**None is absent, so there is no absence list.** One partial absence is recorded
rather than left to be discovered: **`nq` carries no order-book file in any of
its six months.** That is not a gap in the run — it is the fixture's own
property, and the declaration already records it, saying the strict-positive
class count is "3 of 4 on nq" against 9 of 10 elsewhere. The probe notes the
absent aggregate frame and corrupts the trades frame alone. **All eleven
required units are trade-derived, so criterion 1 is unaffected by it.**

**Every instrument-month is run. Nothing is sampled.**

## 3. THE MEASURED SCALE, AND THE COST

Read from parquet metadata, no data loaded:

| | zc 2025-01 (the measured point) | the whole population |
|---|---|---|
| snapshot rows | 1,262,191 | **65,759,237** |
| raw order-book rows | 8,272,769 | **2,607,911,294** (42 instrument-months; `nq` has none) |
| trade rows | 397,457 | 174,000,000 approx |

**The cost model, and it has exactly one measured point behind it.** zc 2025-01
cost 444 s: a 34.8 s capture, and 409 s of builds and fingerprinting over
1,262,191 snapshot rows, of which about 68 s were two redundant column builds
this harness no longer performs. **341 s per 1.262M snapshot rows = 270 s per
million** is the coefficient.

- **Probe phase, predicted: 17,755 s ≈ 4.9 h.** 270 s/M x 65.76M rows.
- **Capture phase: not predicted.** Its cost is dominated by a scan of the raw
  order-book file, which varies from 1.4M rows (`he` 2025-12) to 360M rows (`es`
  2025-11) — a factor of 250. One measurement, taken with a warm page cache,
  does not support extrapolating that. **A linear extrapolation would give
  ≈ 10,970 s ≈ 3.1 h and it is quoted here as an order of magnitude, not as a
  prediction.**
- **Estimated total ≈ 8 hours.** Labelled an estimate. The single largest term
  is `es`, at 1.76 billion of the 2.61 billion order-book rows.

**The halt: any instrument-month whose PROBE phase exceeds 10x its predicted
probe cost stops the run**, records the reason, and leaves every completed
instrument-month checkpointed. The halt is on the probe phase because that is
the term the one measured point measured; a halt built on the capture's
unmeasured coefficient would fire on the model rather than on the run.

**A per-instrument-month failure does not lose the others.** It is recorded as
`could_not_run` with its exception and traceback. §8.2 accounts that separately
from findings and never displays it as a pass. **The predicted number of such
failures is zero** (§6).

## 4. WHAT THE EXTENSION NEEDS, AND WHETHER IT EXISTS

**Population of the read, by heading:** §A.6.1 (the required list and each unit's
governing class); §13(a) (the map artifact, its declared cell key and its 960
cells); §13(b) and §13(c) (the per-instrument-month counts); §C.1 and §C.2 (the
side-relative column enumeration); §C.4 (the column-level gate dispositions);
§12 and §0.3 Claim A (the tie rule); the fixture manifest's column classes.

**Nothing the extension needs is missing.**

- The **required list is a column list, declared once for the fixture**, not per
  instrument-month. §A.6.1 derives it from the trade-derived join family and
  states that its governing classes are strict-positive on the contaminated side
  in all 48 and on the corrected side in the 18 of §13(b).
- The **manifest's column classes are global** to the fixture.
- The **map carries a cell for every one of the 960** (side x instrument x month
  x class) combinations, and **every governing cell this run reads is flagged
  `SCORED`** — checked across all 48, zero exceptions.
- The **tie rule is declared**: `available`, so the comparator reads
  `a(j,c) <= d(i)`.

**No undeclared object is required. There is nothing here of the shape of the
label gap.**

## 5. WHAT WAS SPECIFIC TO zc 2025-01, AND IS RE-ESTABLISHED RATHER THAN CARRIED

| in `58fe726` | why it does not extend | what replaces it |
|---|---|---|
| the invocation names one instrument-month | — | the population, enumerated in §2 |
| "the scored side is contaminated, because §13(b)'s eighteen do not include zc 2025-01" | true of that instrument-month only | criterion 1 is scored per **(side, instrument-month)** wherever a governing cell carries a strict count — see §6 |
| 8 of 11 required and 1 of 4 clean columns present | measured on one build | measured per instrument-month from the probe's own baseline, and predicted in §6 |
| the built frame is 338,159 x 87 | one instrument-month | recorded per instrument-month |
| capture 34.8 s, build 34.1 s | one instrument-month | the cost model of §3, with its halt |
| `vwap_distance` is scoreable | a property of a configuration | re-established per instrument-month by an executable condition — §7 |
| the corrected side is a silent control | true where the map declares nothing | conditioned on the map per instrument-month — §6 |

**One correction to the instrument, made before the run and disclosed here rather
than in the result.** The zc harness treated a cell as declaring no violation
only when strict **and** equal were both zero. **`ties` is declared `available`,
so only a strict count is a violation**; an equal count is a violation under the
branch the declaration did not take. It changes nothing at zc 2025-01, whose
contaminated cells carry 89,568 strict. It changes two cells of this population:
**`es` 2025-10 and `es` 2025-11 corrected carry 0 strict and 1 equal**, and under
the old predicate would have been scored as declaring a violation they do not
declare. The predicate is now `strict_count > 0`.

**A second instrument change, for cost.** The probe now carries its baseline's
column list out (`base_columns`) instead of the harness rebuilding the frame to
learn it. It removes two builds per instrument-month and removes the possibility
of the column set coming from a different build than the findings. Eight cases
cover the probe in `tests/phase1/test_availability_probe.py`, including its
known positive and the negative that has to move the following second or it
tests nothing.

## 6. THE EXPECTATIONS — specific claims about the population, written before the run

A result differing from any of these is reported as a finding. It is never a
reason to adjust the harness, the threshold, the inputs, or the expectation.
**Across 48 instrument-months a perfect result is a strong prior and it may well
be wrong. A miss is the result this run exists to be able to produce.**

### The scoring contexts, derived and stated as a number that can be checked

Criterion 1 is scored on a (side, instrument-month) wherever a governing class
carries a strict count. Computed from the map before the run: **66 contexts — 48
contaminated (all of them) and 18 corrected.** The eighteen are `cl` and `gc` in
all six months and `zc` and `zs` in 2025-08, 2025-09 and 2025-10, which is
exactly §13(b)'s list.

### Criterion 1 — EXPECTATION

**In all 66 scoring contexts, all 8 present required units reach `satisfied`, and
the 3 absent ones are `unsupported`. Zero misses across 66 x 11 = 726 unit
contexts.**

- **Ground.** All eleven units are built from the merged wall-clock-second trade
  aggregate (§C.1(A) and (B)), which is exactly what the probe corrupts; the
  eight present ones did so in all 250 eligible cohorts at zc 2025-01; and the
  map declares a strict count in every one of the 66 contexts.
- **What falsifies it:** any unit in state `missed` in any context. Each such
  miss is named with its instrument-month and side.

### Criterion 1 — the three absent units, predicted rather than assumed

**EXPECTATION: `trade_volume_1s`, `trade_count_1s` and `dollar_volume_1s` are
absent from the built frame in all 48 instrument-months, on both sides, and are
therefore `unsupported` in all 66 contexts.** They were established absent on one
build only. **Ground:** they are among the columns the later builder adds and the
Phase 5 builder this artifact runs does not construct, which is a property of the
builder rather than of any month's data. **What falsifies it:** any of the three
present in any built frame. That is a finding about what the artifact carries,
and it would move criterion 1's observable count.

### Criterion 2 — EXPECTATION

**In all 48 contaminated instrument-months, `minutes_since_open` reaches `clean`,
and `session_open`, `session_mid` and `session_close` are `unsupported`.**

- **Criterion 2's reach does not grow with the population, and the figure is
  stated with that attached.** Of four manifest-clean columns, **one** is present
  in the built frame. So the criterion has **one reachable unit per
  instrument-month**, 48 across the population, however many instrument-months
  are run. It is thin, not vacuous: a finding naming `minutes_since_open` fails it.
- **Ground.** It is `(hour_utc - ds) * 60 + timestamp.dt.minute`, built from the
  snapshot's own timestamp columns, and the snapshot frame is not perturbed.
- **What falsifies it:** any finding naming it, in any instrument-month.

### The control side — EXPECTATION

**The 30 corrected instrument-months with no strict count on any governing class
produce zero finding records. The 18 with a strict count produce at least one.**
The 30 are the complement of §13(b)'s list, and they include `es` 2025-10 and
`es` 2025-11, whose corrected cells carry an equal count and no strict one.
**Ground:** §13(e) and §C.2 — post-lag the corrected row reads the previous
second, which is available unless the two rows share a wall-clock second.
**What falsifies it:** findings where silence is expected, or silence where
findings are expected. Either is reported by instrument-month.

### Two further priors

- **No descendant column receives a finding, in any instrument-month.** All six
  are derived from snapshot book-depth columns, which are not perturbed.
- **Every instrument-month completes; zero `could_not_run`.** The known risk is
  memory on `es`, whose order-book aggregation concatenates arrays over up to
  360 million rows. **Falsified by any failure**, which is recorded with its
  exception rather than skipped.

## 7. THE `vwap_distance` GROUND CONDITION — established per instrument-month, never inherited

`vwap_distance` is the fixture's sole dual-ground column: required on the
forward-join ground, legal on the same-row `mid` read (§C.5, §C.3). SC-5(b)
satisfies the entry only by a finding on the ground the map declares, so a
finding on the legal ground would not count.

**What makes it scoreable is a property of the configuration, not of the
column:** the probe perturbs only the declared aggregate frames, and `mid_price`
is a column of the snapshot frame. **The harness asserts that per instrument-month
and records the answer**, checking that the perturbed frame set is the declared
one, that `mid_price` is present in the snapshot frame, and that it appears in
none of the perturbed frames.

**Where the condition holds**, `vwap_distance` is scored like the other ten.
**Where it does not**, it takes the state `excluded_ground_not_established` with
the ground recorded, and it is not credited to criterion 1's numerator there.

**EXPECTATION: the condition holds in all 48 instrument-months.** **What
falsifies it:** any instrument-month where it does not, which is reported by name
and moves that context's observable count from 8 to 7.

## 8. WHAT THE OUTPUT FILE CARRIES AS DATA

`criteria_scored: [1, 2]` · `criterion_3` and `criterion_4:
BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28` · `gate_result:
NOT_A_GATE_RESULT_TWO_OF_FOUR_CRITERIA` · `violation_predicate: strict_count > 0`
· the note that criterion 2's reach is one unit per instrument-month and does not
grow · the declared cell behind every scored unit · the per-instrument-month cost
against its prediction · the `vwap_distance` condition and its answer per
instrument-month · every feature that received a finding and is in neither
declared list · and the repository's own gate status with its disclosure.

**Findings are summarised, and the summary is labelled.** One instrument-month
produced 5,220 finding records; ninety-six sides of them is not a file anyone
commits. What the criteria read is whether a feature received at least one
finding, so the per-side record carries the feature-to-count map and the totals.

**This is not a gate result and is not published as one.** Two criteria of four.
Criteria 3 and 4 are blocked on the label gap of `D-V30A-28`, which is a finding
about the registration and not a property of this run. **The twenty-one columns
that moved at zc 2025-01 and appear in neither declared list are not coverage and
are never quoted as coverage.**
