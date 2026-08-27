# B-4 — THE OWN-TOOL ROW. **PROPOSED, NOT BUILT.**

**28 August 2026. `phase1`.** R150 §4. The comparison table shows six external tools and **no row for
this project's tool**. A reader will ask for that row first, and the comparison is asymmetric until
it exists. Nothing here is built: no detector run, no row filled, no registered text touched.

**The `aggressor_side` precedent governs — propose, then the author's word.**

---

## 1. THE ROW IS CONSTRUCTIBLE, AND SC-7 PERMITS IT

The obvious objection is SC-7(d): *"A single run given more than one side satisfies none of the
criteria, however its outputs are partitioned afterwards."*

**That forbids one run seeing both sides. It does not forbid the harness comparing two per-side
runs** — which is precisely what the six comparator rows already are: each tool was invoked twice, in
separate processes, each invocation seeing one side. **The pairing is the harness's act, never the
tool's.** So the own-tool row is commensurable with the others by construction, and the discipline
that makes it so is already in force.

**What the tool would receive, per SC-7(a):** the pipeline for that side, and the availability
declaration's declared elements. **Nothing else.** Per SC-7(b) it never receives the paired side or
**the declared ground-truth map** — and SC-7(c) says why in terms: under criterion 3 *"the map **is**
the scoring key … a run that received the key has not produced a gate result, whatever it reports."*

## 2. THE BLOCKING FACT — our existing results are ONE-SIDED

| | |
|---|---|
| `b9_merged.json` `case` | **`fixture_corrected_zc_2025-01`** |
| `probe_b_merged.json` | corrected only — the string `contaminated` does not appear |
| `B9_DETECTOR_SWEEP_RESULTS.md` | *"on `zc` `2025-01`, **corrected side**"* |

**Every result this project has from its own detectors is from the corrected side.** The comparators
were run on both. **The row cannot be filled from what exists**; it needs a contaminated-side run
that has never been performed.

## 3. WHAT "SEPARATES" MEANS HERE — and why the obvious reading is wrong

**The obvious reading is that the dependency map differs between sides. It does not, and cannot.**
`read_inputs` captures the builder's reads by running **one** side, and `fixture_corrected` is
*defined as* `fixture_contaminated` plus `apply_universal_lag` — **the two sides read exactly the
same frames.** A column-dependency map over `raw` is therefore **side-independent by construction**,
and a row claiming our tool "sees a different map" would be false.

**Where a difference could live, in decreasing order of confidence:**

1. **The `build` differs even though `raw` does not.** The probes perturb a raw column and rebuild;
   the contaminated builder reads at *t* where the corrected reads at *t − lag*. The **set** of
   `(cohort, feature)` pairs that move may differ, or the same pairs may move with different
   coverage states.
2. **Coverage states rather than pair membership.** The interesting signal may be `nan`-preserving
   versus `nan`-promoting behaviour on the two sides, which is where B9's two unique pairs
   (`trades.size → trade_count`, `trade_count_10s`) already live.
3. **Availability verdicts.** SC-7(a) hands the tool the declaration's declared elements, and the
   declaration **is** side-aware (§13(c) contaminated in all 48 instrument-months; §13(b) corrected
   in 18). A per-side verdict against a per-side declaration is the most likely locus of separation.

**None of these is measured. Ordering them by confidence is a proposal, not a result.**

## 4. WHAT THE ROW WOULD STATE, AND WHAT IT WOULD BE EVIDENCE OF

> **leakaudit** · contaminated: ⟨verdict⟩ · corrected: ⟨verdict⟩ · separates: ⟨yes/no⟩ ·
> *evidence of:* whether a runtime dependency probe against a declared per-cell availability model
> distinguishes a lag-contaminated pipeline from its corrected twin, **on one fixture, one
> instrument-month, one horizon.**

**What it would NOT be evidence of:** general superiority; performance on any other fixture; anything
about the six comparators beyond the same single pair they were given.

## 5. THE RISK, STATED PLAINLY

**The tool may not separate the pair either.** If the dependency map is side-independent and the
coverage states coincide, our row reads exactly like the others — and that is a finding to publish,
not to bury or to re-run until it changes. **The standard applied to leakage-buster, leakfence,
temporalcv and deepchecks applies here without discount:** constant firing is not detection, an
adapter that never poses the question produces a silence about itself, and a control must run through
the final path.

**The asymmetry to guard against is subtler than favouritism.** We know this fixture's contamination
mechanism; the comparators did not. Any adapter choice that exploits that knowledge — a probe aimed
at the lag because we know the lag is there — makes the row incomparable with the six. **The
own-tool run must be configured from the declaration and the registered detector set, exactly as a
stranger would configure it.**

## 6. WHAT MUST BE SETTLED BEFORE ANYTHING IS BUILT

1. **Does a contaminated-side availability declaration exist with declared elements sufficient for
   SC-7(a)?** The declaration is side-aware, but whether its contaminated-side elements are complete
   enough to run against is unverified.
2. **Is a contaminated-side run inside Phase 1's scope, or does it belong to the acceptance-fixture
   evaluation the registration sequences later?** This is the question that decides whether B-4 is
   work-now or work-later.
3. **Does the row go in the same table as the six, or in its own?** Same table reads as a
   like-for-like benchmark; separate reads as context. The first is stronger and more easily
   overclaimed.

## 7. COST

Roughly **1–2 hours** given the harness already exists: a contaminated-side `read_inputs`/`build`
capture, the registered detector set over it, and a per-side comparison at harness level. **The
expensive part is not the run — it is deciding §6.2 and §6.3 correctly**, and neither is the
agent's to decide.

---

**Status: PROPOSED, NOT BUILT.** No detector was run for this document, no row was filled, no
registered text was touched. **The single most consequential fact it establishes is that our own
results are corrected-side only** — which means the table's missing row is not an oversight in
presentation but a measurement that has never been made.
