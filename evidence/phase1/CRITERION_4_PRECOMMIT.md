# CRITERION 4 — THE IDENTITY CONTROL ACROSS THE DECLARED POPULATION — THE PRE-COMMITMENT

**Committed before the harness is executed.** Nothing below is adjusted once a
number is visible. If the harness turns out to be wrong that is a finding, it is
recorded, its fix is a separate commit, and the re-run is a second and separately
labelled result with the first still in the record.

---

## 1. THE INVOCATION, EXACTLY

```
ACC_INSTRUMENTS=cl,es,gc,he,le,nq,zc,zs \
ACC_MONTHS=2025-01,2025-08,2025-09,2025-10,2025-11,2025-12 \
ACC_STRIDE=997 ACC_MAX_COHORTS=300 \
PYTHONPATH=<repo>;<repo>/src \
python tests/phase1/harness_identity_control.py
```

**Harness:** `tests/phase1/harness_identity_control.py`, committed with this
file. **Control:** `src/leakaudit/identity_control.py`. **Output:**
`evidence/phase1/criterion_4_population.json`, checkpointed after every
instrument-month. **stdout / stderr / exit status:** captured and committed
unmodified.

**Stride and cohort cap are unchanged from the two prior runs**, so the mask this
control writes back over is the mask the real probe perturbed.

**One run.** Interrupted and resumed from checkpoint with nothing read, it is one
run. Resumed after any criterion output has been read, it is a second run and
both are recorded.

## 2. WHAT IS SCORED, AND WHAT IT DOES NOT NEED

Criterion 4, registered text: *"Silent under the identity control on both."* It
incorporates §6.11's control 2 — *"replace unavailable cells with an exact copy
of themselves. Any delta is measurement artifact"* — and SC-5(f)'s declared
sentinels, enumerated ex ante at §A.9 with their signature.

**Neither route reads the pair-keyed labels the metric family consumes, and
neither reads the declared map.** Criterion 4 is not blocked by the
correspondence gap of `D-V30A-28`. Established R193 §2, accepted R194 §0.

## 3. THE ALIGNMENT FAMILY COUNT — F = 1, and its ground

The number of execution frames is **one original plus one per promoted alignment
family** (`DESIGN.md` §5.1; `PREREG.md` line 1181). This detector's perturbation
is dtype-preserving by construction, so no promoting strategy resolves and the
promoted combination has none. **Zero promoted families; F = 1**, identically in
every instrument-month and on both sides, because the count is fixed by the
frozen strategy set rather than by the data.

§6.11's *once per alignment family* therefore imposes **one identity control per
execution frame per audit**, and here that is one.

**A coverage fact, recorded and not repaired: F = 1 means the promoted-family
path is unexercised by this detector.** Nothing here fixes that, and nothing here
treats it as a defect.

## 4. THE AUDIT POPULATION — a choice, with the ground it is made on

**The registration does not settle how many audits criterion 4 is evaluated
over.** Its text fixes the side axis — *on both* — and says nothing about the
instrument-month axis.

**All 48 instrument-months, both sides, are run.** The ground is
**comparability**: the four criteria then share one population, and no later
sentence of the form *"three of four criteria scored"* quotes three different
ones. **It is not chosen for cost and not for safety, and it can be narrowed.**

## 5. TWO LIMBS, AND ONLY THE FIRST IS THE CRITERION

- **Limb (a) — the registered one.** Build after the identity write and compare
  against the baseline exactly. Any moved column is a delta, and a delta is
  measurement artifact.
- **Limb (b) — input invariance. BEYOND THE REGISTERED TEXT.** The write-back is
  checked for value, dtype and index equality on the frames it touched. It is
  reported separately and **is never quoted as satisfying criterion 4.**

**Why limb (b) exists, and why it is kept apart.** A builder can absorb an
input-side change — resetting an index, casting on merge — so limb (a) can pass
while the write-back has changed the frame the promotion status is computed
from. Promotion status keys the combination and decides the tier (§3.1), so a
silent promotion in the write-back moves the tier every real finding is reported
at. **Limb (b) is the only instrument that sees that, and it is not the
criterion.**

## 6. A SHAPE OR COLUMN-SET CHANGE IS A COMPATIBILITY FAILURE — settled, cited

Not a finding, and not a control artifact.

- §6.11 control 3 owns shape and index: *"Confirm output shape and index match
  the baseline… every comparison after that is meaningless, including ones that
  look clean. A failure discards that probe's result."*
- §6.11's head rules out the other reading: the three controls' *"failures are
  recorded per §7.7's two-level scheme, **never as findings**."*
- §6.6's reason precedence puts `compatibility` **ahead of** `control_artifact`,
  which is the state for a probe that did not validly happen (line 1094).

**It is not a pass.** §8.2: no not-run state is displayed in a way mistakable for
one. Criterion 4 has **no answer** on such a side, the harness records
`not_scored` with the verdicts that produced it, and that is reported as itself.

## 7. THE COST — 48 measured points, not one

`D-V30A-37` and `TB-10` record what a one-point model does: it interpolated its
own fitting point to 1.04x and missed the population by 2.35x, because at one
point every term is confounded and the model cannot see which term it omitted.

**This model uses each instrument-month's own measured probe cost** from the
committed population run, scaled by a ratio of two measured terms: a probe side
is 3 builds plus one compare and a control side is 2 builds plus one compare;
at zc 2025-01 a build measured 34 s and a probe side 176.8 s, so the compare term
is ≈75 s and the ratio is 143/177 = **0.81**.

- **Control phase, predicted: 33,862 s ≈ 9.41 h.** Per instrument-month from 181 s
  (`he` 2025-08) to 1,635 s (`gc` 2025-10).
- **Capture: 5,170 s measured** in the population run and expected to repeat.
- **Estimated total ≈ 39,000 s ≈ 10.8 h**, and claimed no better than that.

**The halt: any instrument-month whose control phase exceeds 10x ITS OWN
predicted control cost stops the run**, records the reason, and leaves every
completed instrument-month checkpointed.

## 8. THE EXPECTATIONS — specific, and able to fail

### Criterion 4 — EXPECTATION

**All 48 instrument-months reach `satisfied`: the output does not move under the
identity write, on either side. 96 sides, zero deltas, zero `not_scored`.**

- **Ground.** The write-back writes each selected cell's own value back through
  the same assignment path the perturbation uses; the builder is deterministic,
  which the control checks on two clean builds before writing anything.
- **What falsifies it:** any side whose verdict is `control_artifact`, named with
  its instrument-month, its side and the columns that moved. Any side that is
  `not_scored` is likewise reported and is never displayed as a pass.

### Limb (b) — EXPECTATION, reported apart

**Input invariance holds on all 96 sides: every checked column unchanged in
value, dtype and index.** **What falsifies it:** any column whose dtype moved,
whose index was replaced, or whose values differ — which would be a harness
defect reaching every real probe, and would be reported as one.

### SC-5(f), the sentinel route — EXPECTATION

**No moved column carries the declared sentinel on both sides**, trivially so if
the criterion expectation holds, since nothing moves. Reported for what it is
rather than as a pass. **The enumeration is the declaration's and is never
extended in response to what fires**: the harness checks that §A.9 still carries
the literals `4294967291` and `2^32` and raises if it does not, so a sentinel
that changed there fails loudly rather than being scored stale.

### The schema-uniformity prediction — stated so it can fail

R195 §2 is right that this is exactly the kind of claim that gets believed when
it should be tested. **PREDICTION: the frames the write-back touches carry ONE
distinct dtype signature across all 48 instrument-months**, so the control's
subject is the same object everywhere and the larger reading of §4 adds no
information beyond a shared denominator.

- **Ground.** The trades files carry one distinct parquet schema across all 48
  and the snapshot files likewise, read from metadata. The order-book aggregate
  is constructed in-process, so its dtypes come from code rather than from data.
- **What falsifies it:** more than one signature group in the output's
  `frame_signature_groups`. **That would be a finding, and it would mean the
  comparability ground of §4 was carrying more weight than it was given.**

### Every instrument-month completes — EXPECTATION

**Zero `could_not_run`.** The population run completed 48 of 48 with the same
captures. **Falsified by any failure**, recorded with its exception.

## 9. WHAT THE OUTPUT FILE CARRIES AS DATA

`criteria_scored: [4]` · `criterion_3: BLOCKED_LABEL_GAP_SEE_DEVIATIONS_D_V30A_28`
· `gate_result: NOT_A_GATE_RESULT_ONE_CRITERION` · the family count with its
ground and the unexercised-path coverage fact · the audit-population ground · the
limb (b) note that it is beyond the registered text · per side the verdict, its
scoreability, the moved columns, the sentinel columns and limb (b)'s failures ·
the per-instrument-month cost against its own measured prediction · and the
frame-signature groups that test the uniformity prediction.

**This is not a gate result and is not published as one.** One criterion of four.
Criteria 1 and 2 are scored separately and criterion 3 is blocked on the label
gap, which is a finding about the registration rather than a property of this
run.
