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

## PROVENANCE

Each side was probed in **its own process invocation**, per SC-7(d): *"a single run given more than
one side satisfies none of the criteria, however its outputs are partitioned afterwards."* The
pairing above is the harness's act, never the tool's — the same shape as rows 1–6, each of which was
also invoked once per side. Determinism was verified per side by two clean builds before any
corruption. Seeds are explicit and recorded.
