# What makes a guard recorder usable — the cost criterion

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. Every count carries its command and its resolved
interpreter version.

---

## First: this is stated AFTER the measurement, and that is a defect in the ordering

**R230 §1 asked for this criterion to be written and committed before the
`setprofile` number was read.** It could not be: the measurement completed and the
gate-versus-fallback decision was made and committed in R229 (`7abd492`) before
R230 arrived. **A criterion written now and presented as pre-committed would be
the exact failure R230 §1 is guarding against**, so it is not presented that way.

**What can honestly be done instead, and is done below:** state the criterion, and
then check whether it would have changed the decision. That is weaker than
pre-commitment and it is checkable, which pre-commitment claimed after the fact is
not.

**The reason this particular ordering failure did not contaminate the decision is
structural, not lucky.** The fallback was rejected on **what it recorded** — 2
modules against `sys.monitoring`'s 4 on the same run — and that is a correctness
property with no threshold in it. No cost criterion, chosen before or after, could
have rescued a recorder that sees half the executed set. The cost half was
reported and was not the operative reason. **The criterion below confirms that:
the measured cost would have PASSED it.**

---

## The criterion

**The question is not milliseconds. It is the cost at which the guard stops being
run at all** — because a guard that gets skipped protects nothing, and a fallback
that makes it skippable is worse than a gate that says plainly it does not run on
CPython 3.11.

**The anchor is behavioural, and this project has both ends of it on record.**

| observation | full guard, wall clock | what actually happened |
|---|---|---|
| routine runs, `sys.monitoring` | ~7–9.5 min (two sides of 180–266 s plus a 38–43 s capture) | run to completion, repeatedly, across R205, R211, R216, R227, R228 |
| R216's accidental `setprofile` run | **34+ min** | **killed rather than waited out** |

So the observed threshold between "waited for" and "abandoned" lies somewhere
between about 10 and 34 minutes, and it is bounded by behaviour rather than taste.

> **CRITERION.** A guard recorder is usable on cost if the **full guard** — both
> sides plus the fixture capture — completes in **under 20 minutes** on the
> reference machine. Twenty is chosen as roughly twice the longest routine run
> that has actually been completed, and comfortably below the one run that was
> abandoned. It is not set at the measurement it bounds.

**And it is asserted in both directions**, which is the shape used for the frozen
instrument's `N = 4`: a limit is only a limit if something checks that the
measurement is under it **and** that the limit was not quietly set to the
measurement. `tests/phase1/test_guard_cost_criterion.py` holds both.

---

## Applying it to the measurement that was already read

**The measurement** (`py -3.12 <scratch>/r229_setprofile_real.py`, CPython 3.12.10,
numpy 2.4.2, pandas 3.0.1 — one guard side over the acceptance fixture,
`stride=997, max_cohorts=300`, imports warmed):

| recorder | one side | ratio | modules recorded |
|---|---|---|---|
| none | 209.2 s | ×1.0 | 0 |
| `sys.monitoring` | 185.8 s | ×0.9 | **4** |
| `sys.setprofile` | 379.5 s | ×1.8 | **2** |

**Full guard under the fallback:** 2 × 379.5 s + 43 s capture = **802 s ≈ 13.4
minutes**.

**13.4 < 20, so the fallback PASSES the cost criterion.** It is slower than the
current recorder and not by enough to make the guard skippable.

**Which is the useful result, because it isolates the reason.** The fallback was
rejected, and now demonstrably **not for its cost**: on cost it was acceptable. It
was rejected because it recorded half the modules, which is a false negative in
the one direction a staleness guard exists to prevent. Had the report said only
"rejected", a reader would have assumed cost — and would have been wrong.

**It also corrects a belief this project carried for four rounds, and the
correction has a name: a killed run is not a measurement (D-V30A-64).** `setprofile`
was recorded as giving *"no answer in fifteen minutes"* and a guard run of *"over
thirty-four minutes"*. Both came from runs that were **killed**, so both were lower
bounds presented as costs. Completed, the ratio is ×1.8. **A killed run is not a
measurement, and this project quoted two of them as though they were.**

---

## What this does not settle

**A corrected fallback's cost is unknown and ×1.8 is a floor on it.** A hook that
also fires on module-level execution — matching `sys.monitoring`'s four — does
strictly more work than the one measured. Whether it stays under 20 minutes is an
open question, and the criterion above is what it would be tested against.

**One machine, one workload, one commit.** The ratio is not claimed to hold
elsewhere; the two mis-sized attempts recorded in MV-16 are the evidence that it
does not transfer to smaller workloads.
