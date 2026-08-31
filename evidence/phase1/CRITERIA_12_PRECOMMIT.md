# CRITERIA 1 AND 2 ON L3.1 — THE PRE-COMMITMENT

**Committed before the harness is executed.** Nothing below is adjusted once a
number is visible. If the harness turns out to be wrong that is a finding, it is
recorded, its fix is a separate commit, and the re-run is a second and
separately labelled result with the first still in the record.

**This supersedes `ACCEPTANCE_PRECOMMIT.md` (`b065264`), which is VOID** — it was
frozen on a premise later refuted, and it named the column probe, which
`D-V30A-27` records is not an instrument section 6.2 scores. Its output is
quarantined unread at `void_b065264/`. Nothing in it is carried forward, and
nothing here is copied from it: every figure below was measured this round and
names how.

---

## 1. THE INVOCATION, EXACTLY

```
ACC_SYM=zc ACC_MONTH=2025-01 ACC_SIDES=contaminated,corrected \
ACC_SCORED_SIDE=contaminated ACC_STRIDE=997 ACC_MAX_COHORTS=300 \
ACC_SEED=20260828 PYTHONPATH=<repo>;<repo>/src \
python tests/phase1/harness_criteria_12.py
```

**Harness:** `tests/phase1/harness_criteria_12.py`, committed with this file.
**Output:** `evidence/phase1/criteria_12_run.json`, checkpointed after each side.
**stdout / stderr / exit status:** captured to files and committed unmodified.

**The stride, cohort cap and seed are the ones the B-9 run used**, so this run is
comparable with the recorded one rather than tuned against it. A stride of 1
would corrupt adjacent seconds and destroy the discrimination the probe rests on;
997 keeps corrupted seconds far apart.

**One run.** Interrupted and resumed from checkpoint with nothing read, it is one
run. Resumed after any criterion output has been read, it is a second run and is
labelled as one.

## 2. THE INSTRUMENT, AND THE REPAIR MADE BEFORE THE RUN

**L3.1 — the availability probe.** Established R188 §3.1, accepted R189 §1, and
recorded at `D-V30A-27`. The column probe is not one of the eleven detector rows
and is not scored here.

**One repair was made to the trace emitter first, and it is disclosed here rather
than in the result.** `traces_for` emitted `feats[0]` — the alphabetically first
column that moved in a cohort — and dropped the rest. The probe had them all.
That is wrong in both directions this round depends on: criterion 1 loses nine
attributions out of ten and reads as misses that never happened; criterion 2
loses a clean column that sorts after the survivor, which is a false negative in
the direction that hides a violation of the criterion the tool is being examined
by. It now emits one record per moved feature.

**The repair's known positives discriminate**, which is checked and not assumed:
the same synthetic cohorts through the replaced emitter and the repaired one —

| case | moved | replaced emitter | repaired emitter |
|---|---|---|---|
| a clean column sorting last | 2 | 1 finding (`net_delta_1s`) | 2 findings |
| ten required columns in one second | 10 | 1 finding (`net_delta_1s`) | 10 findings |

Eleven cases in `tests/phase1/test_availability_trace.py`; the two above fail on
the emitter that was replaced.

## 3. THE INPUTS, AND WHAT THE TOOL NEVER SEES

| input | what it supplies | read by |
|---|---|---|
| the f2 rebuild pair via `fixture_adapter` | Artifact A, both sides | the tool |
| the declared availability model | the two aggregate frames and their keys | the tool |
| `AVAILABILITY_DECLARATION.md` §A.6.1 | the REQUIRED list and each unit's governing class | the harness only |
| `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json` | the column classes and the DAG | the harness only |
| `evidence/fixture_spike/n1/declared_map.csv` | the declared cells | the harness only |

**The tool receives none of the last three.** SC-7(b)/(c) withhold the map, and
`tests/phase1/sc7c.py` states that executably: the package neither imports,
names, constructs nor reaches the label type, checked by parsing every module,
with one violating copy per route and a negative control.

**Ground truth is derived, never transcribed.** The REQUIRED list is parsed from
the declaration's table and the parse checks itself against the declaration's own
stated N; a first version of that parser returned ten units for a denominator of
eleven and a denominator short by one scores a different criterion. It raises now.

## 4. WHICH SIDE, AND WHY IT IS THIS ONE

**Both criteria are scored on `fixture_contaminated`.**

Criterion 2 names that side in its own text. Criterion 1 is scored where the map
declares the violations, which SC-5(b) requires — *"on the side, in the cells, and
on the ground the map declares"* — and for **this** instrument-month that is the
contaminated side: §13(c) has all 48 instrument-months strict-positive there,
while §13(b)'s eighteen non-zero corrected instrument-months are cl and gc in all
six months and zc and zs in 2025-08/-09/-10. **zc 2025-01 is not among them**;
§13(e) records its corrected cell as the surviving zero.

**The corrected side is run and reported as a control, and no criterion is scored
on it.** An instrument that fires on the contaminated side and is silent on the
corrected one is discriminating; one that fires on both is not, and the run
should show which.

## 5. THE VERIFIED FACTS — every one measured this round, with how

Measured 31 August 2026 on this machine, Python 3.12.10, numpy 2.4.2 / pandas
3.0.1 / pyarrow 23.0.1, by capturing the builder's inputs once and building each
side once. **No probe was executed to obtain any of these.**

| fact | value | how |
|---|---|---|
| capture cost | 42.3 s | measured |
| one build | 34.4 s contaminated, 34.1 s corrected | measured |
| built frame | 338,159 rows x 87 columns, both sides | measured |
| raw frames | snap 1,262,191 x 24; trades 397,457 x 17; magg 464,199 x 6 | measured |
| REQUIRED units present in the built frame | **8 of 11** | measured against the frame's own columns |
| REQUIRED units absent | `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s` | measured |
| manifest-CLEAN columns present | **1 of 4** — `minutes_since_open` | measured |
| manifest-CLEAN absent | `session_open`, `session_mid`, `session_close` | measured |
| manifest-DESCENDANT present | 5 of 6 | measured |
| the map's row count for this cell | 338,159 | read from `declared_map.csv`, and it equals the built frame's row count |

**The declared cells this run's units are governed by**, read from the map for
`contaminated / zc / 2025-01`:

| governing class | strict | equal | scored |
|---|---|---|---|
| `trades_all` | 89,568 | 20 | SCORED |
| `trades_sell` | 89,568 | 20 | SCORED |
| `trades_large` | 23,633 | 20 | SCORED |

All three are non-zero, so SC-5(b)'s *"in the cells"* limb is met for all eight
observable units. It is checked by the harness per unit rather than assumed here.

**The three absent REQUIRED units take `unsupported`** under §8.2 — *"missing or
impossible inputs are `unsupported`"* — on the ground that each is one of the
columns Phase 7 adds and the Phase 5 builder does not carry, so the column is
absent from the artifact the criteria are evaluated on. §8.2 governs the display:
none of these states appears in a way mistakable for a pass, here or in the
result file. **The denominator stays 11** (SC-4(b): N is the length of the
REQUIRED list and no other quantity is N; the denominator is never adjusted to
reachability).

**`vwap_distance` is scoreable, and R190 §1 is why.** Probe A's perturbation
domain is exactly the declared aggregate frames, `magg` and `trades`. `mid` is
`snap["mid_price"]` — a column of the snapshot frame, which the probe never
perturbs. So a `vwap_distance` movement under this probe can only come from the
`vwap` term, which is the merged wall-clock-second aggregate, which is the
forward-join ground the map declares violating. The legal same-row `mid[t]`
ground is unreachable by construction, not by classification.

**`minutes_since_open` cannot be reached by this probe either**, and the same
argument runs the other way: it is `(hour_utc - ds) * 60 + timestamp.dt.minute`,
built from the snapshot's own timestamp columns, and the snapshot frame is not
perturbed.

**Primary and secondary are decided by the harness, from the manifest's own DAG,
never from the tool's `is_secondary` flag.** PREREG.md line 914 records the
reason: a classifier the tool controls cannot be allowed to decide what counts
against it. A finding on a DESCENDANT column is secondary under §7.6, and line
700 says a secondary finding on a manifest-listed descendant neither satisfies
criterion 1 nor enters criterion 2.

**Prior measured cost of the same probe under the frozen contract:** 223.6 s
contaminated and 214.9 s corrected, each including its own capture
(`evidence/phase1/probe_a/wrapped/`). This run captures once for both sides and
builds one extra frame per side to enumerate its columns, so it is expected to
cost of the order of seven minutes. **That is an estimate and is labelled one;
the measured figure goes in the result.**

## 6. THE EXPECTATIONS — falsifiable, written before the run

A result differing from any of these is reported as a finding. It is never a
reason to adjust the harness, the threshold, the inputs, or the expectation.

### Criterion 1 — every ground-truth leaking source column receives at least one primary runtime finding

- **Registered denominator: 11.** Observable in this artifact: **8**. Remainder
  **3**, state `unsupported`, named in §5.
- **EXPECTATION: all 8 observable units reach `satisfied`** — at least one primary
  finding attributed to the unit, in a cell the map declares non-zero.
- **The ground, and it is prior published evidence rather than hope.** All eight
  are built from the merged `ts_floor` aggregate (§C.1(A)), which is exactly what
  the probe corrupts. The B-9 run of this probe on this side recorded findings in
  250 of 250 eligible cohorts. The fixture adapter's own recorded known positive
  states that perturbing `trades.size` moved `net_delta`, `sell_volume`,
  `trade_volume`, `large_trade_count` and `net_delta_1s`.
- **The risk this expectation runs, stated rather than discovered later.** That
  known positive perturbed a whole column; this probe corrupts 608 aggregate rows
  across 300 seconds, and the sampled cohorts carry about one output row each. A
  unit whose construction does not move on that single row would read as a miss.
  The expectation is still all 8.
- **What falsifies it:** any of the 8 in state `missed`. That is a miss, and
  criterion 1 fails over this scope.

### Criterion 2 — no manifest-clean source column receives any finding of any tier on the contaminated side

- **Clean population: 4. Reachable in this artifact: 1** — `minutes_since_open`.
  The other three are Phase-7-added and take `unsupported`, same ground as above.
- **Stated plainly: the reachable clean population is one. The criterion is thin,
  not vacuous.** It can fail, and what would fail it is a finding naming
  `minutes_since_open` on the contaminated side.
- **EXPECTATION: `minutes_since_open` reaches `clean`** — no finding of any tier
  names it — because it is a deterministic function of the row's own timestamp
  and no perturbed frame feeds it.
- **What falsifies it:** any finding naming it. That is a false positive and
  criterion 2 fails over its reachable population.

### Not criteria — two further falsifiable priors, reported the same way

- **The corrected side is silent.** EXPECTATION: `probe_verdict` is
  `observed_silence` with zero finding records. Ground: §13(e) records zc
  2025-01's corrected cell as the surviving zero, and the B-9 run measured
  exactly that. **Falsified by** any finding on the corrected side, which would
  mean the instrument does not discriminate the pair.
- **No finding lands on a DESCENDANT column.** EXPECTATION: none of the five
  present descendants appears among the features with findings. Ground: all six
  are derived from snapshot book-depth columns, and the snapshot frame is not
  perturbed. **Falsified by** any of them appearing, which would be evidence of a
  path this pre-commitment did not anticipate and would be reported as such.

## 7. WHAT THE OUTPUT FILE CARRIES AS DATA

`criteria_scored: [1, 2]` · `criterion_3` and `criterion_4:
BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28` · `gate_result:
NOT_A_GATE_RESULT_TWO_OF_FOUR_CRITERIA_ONE_INSTRUMENT_MONTH` · the declared cells
it scored against · every finding with its feature, cohort and the tool's own
secondary claim · every feature that received a finding and is in neither
declared list · and the repository's own gate status with the disclosure that
closes it as a known false positive, so a reader seeing a red gate beside these
numbers can tell which it is.

**This is not a gate result and is not published as one.** Two of four criteria,
one of forty-eight instrument-months, one of two sides scored. Criteria 3 and 4
are blocked on the label gap of `D-V30A-28`, which is a finding about the
registration and not a property of this run.
