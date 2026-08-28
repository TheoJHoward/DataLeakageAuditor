# THE COMPARISON, FINAL FORM — SEVEN ROWS

**28 August 2026. `phase1`.** Six external comparators and this project's tool, against the same
acceptance-fixture pair: `zc` `2025-01`, contaminated vs corrected, 338,159 × 87 each, hashes
`b62f5c16…` / `91102e67…`.

**Every row states what it is evidence of.** Per R151 §1.2 the argument has three parts and they are
kept distinct: the external tools fail to separate the pair · Layer 1 is identical **by design, not
by failure** · Layer 2 separates because it probes availability.

---

## THE TABLE

| # | tool | contaminated | corrected | separates? | evidence of |
|---|---|---|---|---|---|
| 1 | **leakage-buster** 1.0.2 | `finding=True` — 2 HIGH | `finding=True` — **same** 2 HIGH | **no** | encoding structure present in both sides; **constant firing is not detection** |
| 2 | **leakfence** 0.5.0 | dup 0; group **unposable** | dup 0; group **unposable** | **no** | no duplicated rows across the split; the fixture has no subject grouping, so the group check contributes nothing either way |
| 3 | **temporalcv** 2.3.0 | −2.04 → PASS | −2.07 → PASS | **no** | a Ridge fit does not beat persistence on either side; the gate is in its regime (precondition −1.195) and has nothing suspicious to flag |
| 4 | **deepchecks** 0.19.1 | max PPS 0.023 | max PPS **0.046** | **no** | no single feature predicts the target above 0.05 — and the corrected side scores *higher*, the opposite of a leakage signal |
| 5 | **Leakly** 0.1.2 | `unsupported` | `unsupported` | — | detects by varying **pipeline order**; a built table has no pipeline to reorder |
| 6 | **leak-detect** 0.0.1 | `could_not_run` | `could_not_run` | — | applicable in principle; the `ld` venv's pandas pin cannot import the builder. **A limit of this harness, not the tool** |
| **7** | **`leakaudit` — Probe A** | **`finding`** — 250 of 300 cohorts | **`observed_silence`** — 0 of 300 | **YES** | **the built output depends on cells the declared availability model says had not yet arrived at the row's decision time** |

**Rows 1–6 were each shown to fire on a documented positive through the same adapter path the
measurement used** (B-3). Rows 5–6 are `covered_with_exclusion`, never a pass.

---

## ROW 7, IN FULL

| | contaminated | corrected |
|---|---|---|
| verdict | **`finding`** | **`observed_silence`** |
| cohorts probed | 300 | 300 |
| cohorts with a finding | **250** | **0** |
| rows moved **in-second** | **250** | **0** |
| rows moved **next-second** | 250 | **250** |

**The discrimination is in the row indices, not in the fact of movement.** A single rebuild with a
*sparse* set of corrupted seconds asks *which* rows moved:

- a row stamped in second **F** moves ⇒ the build read F's aggregate at a decision instant **inside**
  F ⇒ the cell was **unavailable** ⇒ a finding;
- only rows stamped in **F+1** move ⇒ it read F's aggregate one second later ⇒ **available** ⇒ no
  finding.

**The corrected side's 250 next-second movements are the liveness proof.** Its silence is not the
silence of a probe that never reached the build: the corruption landed, the aggregate *was* read —
one second later, when the model says it had arrived. **A silent row without that number would be
worthless.**

### The model, from the declaration and not invented

The comparator is `a(j,c) <= d(i)`, **ties available**, locked at §0.3 Claim A. The declared
availability instant for the join families is the **`at_source_timestamp` truth, `ts_floor + 1s`** —
the instant the wall-clock-second aggregate completes. The declaration states in terms that the
`at_bar_close` role is an **approximation** of that instant and not the scored one, because *"scoring
`at_bar_close` as the availability instant for a join-family column would find the contaminated side
clean."* **Probe A scores the declared instant.**

### Controls, through the final path

Synthetic and independent of the fixture, so the probe's own test does not depend on the thing under
measurement: a builder reading its **own** second (unavailable) — **fires in-second, 126 rows**; a
builder reading the **previous** second (available) — **silent in-second, 126 rows moved
next-second**. The controls were re-run after a dtype fix to the corruption, because **a fix to the
measurement path re-opens the control**.

---

## WHY ROWS 1–6 COULD NOT SEE IT — a designed property, not a failure

**Layer 1 is side-invariant by construction.** `read_inputs` captures the builder's reads by running
one side, and `fixture_corrected` is *defined as* `fixture_contaminated` plus `apply_universal_lag`:
**both sides read exactly the same frames.** A dependency map over `raw` therefore **cannot** differ
between them, and any tool whose question is "which columns does this frame relate to" is asking a
question the pair does not distinguish.

**The two sides differ in *when*, not in *what*.** That is the registered claim, stated as an
experimental design — and it is why a probe against a declared per-cell availability model sees what
correlation, duplication, split-hygiene and predictive-power checks cannot.

**This is not a claim that rows 1–6 are bad tools.** Each fired on its own documented positive.
They are aimed at different leakage classes, and this fixture's contamination is not in their class.

## WHAT ROW 7 IS **NOT** EVIDENCE OF

- **Not** general superiority. One fixture, one instrument-month, one horizon, one contamination
  mechanism.
- **Not** a claim about any other dataset, or about leakage classes rows 1–6 do cover.
- **Not** a gate result under criterion 3 — Probe A never received the R9 ground-truth map (SC-7(c)),
  and this run is a comparison, not a graded evaluation.
- **Not** independent of the declaration. Row 7 depends on the declared availability model being
  right. If the declaration is wrong about when cells arrive, Probe A is wrong with it — and that
  dependency is the tool's design, stated rather than hidden.

---

## V-1 — THE 50 SILENT COHORTS. **MECHANISM ESTABLISHED.**

The contaminated side fired on 250 of 300 cohorts. **The mechanism is in the probe's own note**, not
in a guess: it recorded corrupting **250 aggregate rows across 300 seconds** — and the shortfall is
the answer.

| | |
|---|---|
| picked seconds with a `magg` row | **250** |
| picked seconds with **no aggregate row in any frame** | **50** |
| cohorts the probe reported silent | **50** |
| **the two sets are the same** | **yes** |

**Nothing was perturbed for those fifty seconds, so nothing could move.** The silence is the probe
having nothing to look at — **not** the probe failing to see. **Domain of the silence: 50 decision
rows, 0.0148% of the fixture's 338,159.**

**Set coherence holds.** Both sides build 338,159 rows, agree on every decision stamp, and therefore
pick **the same 300 seconds**. A mismatch would have been a finding; there is none.

*(Established without a rebuild: the picked seconds are deterministic, and whether a second carries an
aggregate row is a property of the raw frames. That is what keeps V-1 verification of the run rather
than a re-run.)*

## V-1's SECOND FINDING — a frame that was never corrupted at all

The same check showed **`trades` matched 0 of the 300 picked seconds.** `trades.ts_event` is
`datetime64[ns, UTC]`; `snap.timestamp` and `magg.ts_floor` are naive. **`isin` between tz-aware and
tz-naive never matches**, so the trades frame was silently never perturbed — an all-False mask that
looks exactly like *"no cells were unavailable."*

**The probe's own guard missed it because it summed across frames.** `touched == 0` raised only if
*every* frame matched nothing, so magg's 250 masked trades' zero: **a per-frame failure hidden by an
aggregate.** The guard is now **per frame**, and keys are converted into the decision stamps' frame of
reference rather than compared across it.

**The re-run changed the corruption and not the verdict** — which is the point of reporting it:

| | before | after |
|---|---|---|
| aggregate rows corrupted | 250 | **608** |
| contaminated | `finding`, 250/300 | **`finding`, 250/300** |
| corrected | `observed_silence`, 0/300 | **`observed_silence`, 0/300** |

**The fix could have weakened the separation and did not.** Two further dtype defects were fixed on
the way, both under R152 §2.2 — *a cast to make a perturbation fit is a second perturbation*: a flat
`+1_000_000` overflowed `uint8`, and a modular wrap overflowed `int64` (span 2⁶⁴). The offset now
chooses its **direction** per element, needs no arithmetic wider than the column, and is `>= 1` so the
value is guaranteed to differ.

## V-2 — DISCIPLINE CONFIRMATION

| | |
|---|---|
| determinism guard, per side | **YES** — two clean builds compared before any corruption, `determinism_ok=true` on both |
| seed stable and recorded | **YES** — `20260828`, now written into each result file |
| cross-process reproducibility | **YES** — both sides re-run in fresh processes reproduced every figure exactly |
| **traces through the existing reducers, unchanged** | **NO — and this is a real gap.** |

**Probe A does not emit registered traces.** It compares built outputs directly and produces no
`CombinationTrace` / `ExecutionRecord`, so **no reducer has seen its output**. That is the difference
between Probe A as a research instrument, which it is, and Probe A as a registered detector, which it
is not yet. **Row 7 is therefore a comparison result, not a gate result** — consistent with what the
row already disclaims, and recorded here rather than left for a reader to notice.

### B-9 — the gap is now narrowed, and the row is unchanged

**28 August 2026.** Probe A was wrapped in the frozen output contract and re-run. **Reported here
separately; row 7 above is not restated or replaced** (R153 §1.1).

| side | PRESERVING | PROMOTED | agrees with the published run |
|---|---|---|---|
| contaminated | **`completed` × `finding`** — 250 cohorts, 250 records, **250 findings** | `not_applicable` × `none` | **yes** |
| corrected | **`completed` × `observed_silence`** — 250 cohorts, 250 records, **0 findings** | `not_applicable` × `none` | **yes** |

**Every trace was accepted by `resolve_state_pair` UNMODIFIED.** Adjusting a reducer to accept a
trace is a halt; none was touched. An illegal pair or a malformed trace raises, and none did.

**Three mappings were derived from the registered legality table, not chosen:**

- **Eligibility.** The 50 seconds with no aggregate row are **not eligible cohorts** — nothing to
  corrupt, so nothing scheduled. Including them with no record would resolve to
  `incomplete(crash)`: *a missing schedule slot with no recorded failure*, reporting a dead process
  where the truth is an empty probe surface.
- **Promotion.** The corruption is dtype-preserving by construction, so every execution is
  `PRESERVING`. The `PROMOTED` combination has **no resolved strategy** → `not_applicable` × `none`,
  a legal pair, and it is **emitted rather than omitted**: a combination that ran nothing is a fact.
- **Outcome.** A moved cohort carries a `FindingRecord`; a probed cohort that did not move is a valid
  record with no finding. **The distinction the artifact draws in prose is the one the contract draws
  in types.**

**One thing the contract forced that the probe could not supply.** `FindingRecord` requires a
**`feature`**, and the probe compared whole-row fingerprints — it knew *which rows* moved, not *which
columns*. **A placeholder there would be a fabricated fact inside a registered trace**, so per-column
attribution was added and the emitter **raises** if movement is recorded without a named feature.

**Row 7's classification does not change.** Traces that resolve are necessary for a gate result, not
sufficient: §6.2's acceptance scores them through `compute_runtime_metrics` and the rest of the
acceptance apparatus, which has not been run. **Row 7 remains a comparison result.**

---

## PROVENANCE

Each side was probed in **its own process invocation**, per SC-7(d): *"a single run given more than
one side satisfies none of the criteria, however its outputs are partitioned afterwards."* The
pairing above is the harness's act, never the tool's — the same shape as rows 1–6, each of which was
also invoked once per side. Determinism was verified per side by two clean builds before any
corruption. Seeds are explicit and recorded.
