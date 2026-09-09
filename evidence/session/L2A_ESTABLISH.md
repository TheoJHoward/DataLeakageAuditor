# L2a, the label probe — what the registration determines, before any code

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. **L2a is a registered detector row implemented after
the registration closed. Its results are Phase 2.** Building it does not
retroactively touch the closed Phase 1.

**Tree state.** `git rev-parse HEAD` → `be928ee357608da075319007e78300664333be16`,
working tree clean but for this file. **No code was written this round.**

**Structural population of the reading below.** Every line of `PREREG.md` and
`DESIGN.md` carrying the token `L2a`, all of which were read:

    grep -c "L2a" PREREG.md DESIGN.md      ->  PREREG.md:34   DESIGN.md:11
    grep -o "L2a" PREREG.md | wc -l        ->  36
    grep -o "L2a" DESIGN.md  | wc -l       ->  13

at `be928ee`, plus `PREREG.md` §§2.3–2.8, §4, §4.1, §4.2, §6.2, §7.2, §7.7, §8.2
and `DESIGN.md` §§2.1–2.7, §3, §5.1 read whole. This is a reading of the
registration and it is offered with its population, not as fact without one.

---

## 0. The citation check — one of three does not resolve

R258 §3(a) requires that a section number failing to resolve be reported and not
proceeded on.

| cited | resolves? | what is at that number |
|---|---|---|
| `PREREG.md` §4, L2a's row | **YES** | `## 4. Coverage map` at line 403; the L2a row at line 412 |
| `PREREG.md` §2.6, *"the scoring unit: feature × affected output cohort, a cohort being ROWS sharing a decision time"* | **NO — partial** | `### 2.6 A probe's silence extends only to its cohort` at line 282 |
| `DESIGN.md` §2.7 | **YES** | `### 2.7 The label probe (L2a)` at line 129 |

**What §2.6 actually carries.** It locks the valid-finding rule and the scope of
a silence, and then *names* the scoring unit by forward reference in one closing
sentence: "the scoring unit is **feature × affected output cohort**, deduplicated
across probes, strategies, and runs (§7.2)". It does not define the unit and it
does not define a cohort.

**The sections that do carry the named content:**

- **the scoring unit** — `PREREG.md` §7.2, line 1294, `### 7.2 The runtime
  scoring unit, and how detection is counted`, which defines two units:
  `EvidenceEvent` keyed `(detector, promotion_status, feature, affected output
  cohort)` within a case, and `ReportedFinding` keyed `(detector, feature,
  affected output cohort)`.
- **a cohort being rows sharing a decision time** — `DESIGN.md` §2.3, line 82:
  "A **decision cohort** is the set of output rows sharing one decision time."
  **This definition is in the design document, not in the registration.**
  `PREREG.md` §2.6 uses the word throughout and never defines it.

The delta's parenthetical is a correct statement of the registered scheme; it is
assembled from three places and §2.6 is only one of them. **I proceeded on §7.2
and `DESIGN.md` §2.3 for the unit, and on §2.6 for the valid-finding rule, which
is what §2.6 does carry.**

---

## (a) What L2a is registered to detect, in the registration's own words

**The row, quoted from `PREREG.md` §4 line 412 — the closed table of eleven:**

> | **L2a** | Features from unavailable label values | PROVEN / REVIEW per §3 |
> Availability-restricted label perturbation | callable + label column +
> (temporal: `label_availability`; non-temporal: §2.5 policy) |

**Its two applicability modes, §4.2 quoted whole:**

> **Temporal.** At cohort *d*, corrupt only label cells unavailable at *d*.
> Realized labels stay identical, so a feature reading a realized `y.shift(1)` is
> clean and one reading an unrealized label is flagged.
>
> **Non-temporal.** Runs only under `labels_available_during_feature_construction
> = false` (§2.5). Otherwise `unsupported`. Cross-fitted target encoding,
> supervised transformations, and train-only class statistics are legitimate label
> use; without the narrowing, PROVEN would mean "depends on a label" rather than
> "depends on an unavailable label."
>
> **Division of labor with L3.1.** One method pointed at different columns, run as
> separate probes so findings can be attributed. Where labels are built inside the
> pipeline, L2a returns `unsupported` naming **L3.1 as covering detector**.
> **Residual case, uncovered:** a label built internally from a past-window
> statistic also used as a feature. Registry entry 5.

**The label's availability, §2.4:**

> **`a(y_j) = label timestamp + label horizon + publication delay`**
>
> All three terms are user-declared, as one `label_availability` declaration. The
> publication delay **defaults to zero only when the user supplies the
> declaration** … **No profile may default any term.**

**The scoring unit it emits into, §7.2:** an `EvidenceEvent` keyed `(detector,
promotion_status, feature, affected output cohort)` within a case, deduplicated
so that probe cohorts, strategies and repeated runs *within one combination* are
corroborating evidence rather than additional events.

**The valid-finding rule its mask obeys, §2.6, locked in both directions:**

> - **A change at any row with `d(i) ≤ d` is a valid finding.**
> - **Silence is informative only for the cohort `d(i) = d`.**

**Tier, §4.1:** promotion status alone decides it — `preserving` reaches PROVEN,
`promoted` is REVIEW `dtype_promoted`. L2a may also be `unsupported`, fail to
run, or be silent.

**Its declared blind spots, §5.3, which are named and not tested as positives:**
registry 2, a feature built from an upstream *proxy* of the label, is invisible;
registry 5, a label built internally from a past window and reused as a feature,
falls between L2a and L3.1 and is uncovered.

### The consequence of building it that lands on §6.2

**§6.2's pass gate never names a detector row.** Criterion 1 reads "Every ground
truth leaking source column receives at least one **primary runtime finding**";
the runtime rows are L2a and L3.1, assigned as such in §7.1's metrics table at
lines 1279–1280. **Today only L3.1 is built, so "a primary runtime finding"
identifies one row by accident.** Building L2a makes criterion 1 satisfiable by
either row, and the registration does not say whether both must fire, either
suffices, or each is scored on its own columns.

This is `NEXT_REGISTRATION_REQUIREMENTS.md` §1 line 41, *"Which detector row each
criterion is evaluated on, named explicitly"*, already recorded there from R188
§3.1 as `D-V30A-27` / `TB-08`. **Building L2a is the event that makes it bite.**
It is not a gap to fill by judgment this round.

---

## (b) Its relation to L3.1 — same machinery, different mask, different clock

`DESIGN.md` §2.7, quoted:

> Same machinery, mask intersected with the label column, using `a(y_j)` from
> `label_availability`. **Probes cohorts exactly as L3.1 does**, which is why the
> cost model gives it a `C × S` term (§5.1).
>
> **Assert every call:** every non-label column, and every *available* label cell,
> is byte-identical to the aligned baseline. Without this a finding cannot be
> attributed.
>
> Run as a separate probe from L3.1 — perturb both and attribution is lost.

So: **the same perturbation machinery, pointed at the label, run as a separate
probe.** Not a different mechanism.

### What L2a needs that L3.1 does not

1. **A label column locator, on the RAW input side.** The probe corrupts input
   cells and rebuilds, so it needs the frame and column the label lives in
   *before* the builder runs. The shipped `label_column` key is documented in
   `model_file.py` as *"The built output's label column"* and is listed there
   among the keys that **do not** correspond to registered vocabulary; it serves
   the model-free checks. These are two different objects with one name
   available.

2. **A second clock.** `a(y_j) = base + horizon + publication delay`, three
   declared terms. The shipped `AvailabilityModel` carries one rule per aggregate
   frame — `floor(key) + window` — plus per-column modes. The label's instant is
   neither: its base is a declared column and its offset is `horizon + delay`,
   not `window`. `DESIGN.md` §3 shows the declared shape as
   `label_availability=("timestamp", "60s", "0s")   # base, horizon, pub delay`.

3. **A path selector.** Absence of a timestamp column — *not* absence of a
   declaration — selects the non-temporal path (§2.7). L3.1 is `not_applicable`
   there; L2a still has a job. The shipped `run_probe_a` cannot express that
   path: it requires `aggregate_frames`, requires a `decision_column`, and
   refuses without either.

4. **A decision time per row — no.** This is the delta's own question and the
   answer is that L2a needs nothing L3.1 does not already have. `decision_column`
   is required by both and is already refused-not-defaulted at the shared
   consumption point (`require_decision_column`, R236 §3(c)).

### The asymmetry that is not cosmetic, and is the round's finding

**`DESIGN.md` §2.7's "probes cohorts exactly as L3.1 does" is true of cohort
SELECTION and false of the attribution arithmetic.**

L3.1's shipped discrimination is stated in `availability.py`'s own docstring:
corrupt a sparse set of seconds, rebuild once, and read *which* rows moved —

    a row stamped in second F moves       -> unavailable -> a finding
    only rows stamped in second F+1 move  -> available   -> no finding

with `CohortResult.finding()` returning `moved_in_second > 0`. **That rule is
exact only because the aggregate's availability instant is `floor(key) + window`
with `window = 1s` — exactly one second later.**

The label's instant is `ts + horizon + delay`. Under a horizon `H`, a corrupted
label row in second `F` is unavailable to every output row whose decision time
lies in `[F, F+H)`. So the finding set is rows in `F … F+H−1`, not rows in `F`.
`PREREG.md` §2.6 states the general rule — a change at any row with `d(i) ≤ d` is
valid — and the shipped counters are that rule specialised to a one-second
offset.

**Reusing the counters unchanged reports a real leak with a 60s horizon as
`moved_next_second`, which is no finding.** That is the R236 shape exactly: a
real leak arriving as this tool's affirmative evidence of absence.

**And the stride is the same defect one level up.** `cohort_stride=97` exists so a
moved row attributes to exactly one corrupted second. The separation the label
needs is the declared horizon, not one second. Where `horizon` exceeds the gap
between corrupted seconds, two corrupted seconds' influence windows overlap and
attribution is lost silently.

---

## (c) The discriminating known positive — established before the design is fixed

R258 §4 halts a known positive that L3.1 or the correlation check would also fire
on. `OPERATING_RULES.md` §3 (R257) requires the pair to vary exactly what is
under test and to **name what is held constant**.

**Why a wiring test is not sufficient here.** R215/R218's scope clause exempts a
positive that confirms a *hard failure* nobody reads the absence of as evidence.
The failure being confirmed here is a **silence** — `observed_silence` from L3.1
and a clean result from the correlation check — and this project reads
`observed_silence` as evidence. So the discriminating positive is required.

### The construction

One frame set, one builder, built once and cut two ways.

- **Frames.** A `labels` frame with `ts` (the label timestamp) and `y` (the
  label), one row per second. `y` drawn i.i.d. from a seeded generator, so
  successive values are independent by construction.
- **Builder.** Output row *i* is stamped `d(i) = ts_i` and carries one feature
  `f_i = y_{i−1}` — the previous second's label — plus the decision column.
- **Declaration, positive half.** `label_availability = (base="ts", horizon=60s,
  publication_delay=0s)`. Then `a(y_{i−1}) = ts_{i−1} + 60s = d(i) + 59s > d(i)`.
  **Unavailable.** L2a corrupts it at cohort `d(i)`; row *i* moves; **finding.**
- **Declaration, clean half.** `horizon = 0s`. Then `a(y_{i−1}) = ts_{i−1} =
  d(i) − 1s ≤ d(i)`. **Available.** Not corrupted; **silence.**

**This is the registration's own separator**, §2.4: "§6.5 contains a lagged label
that *is* realized (clean) and one that is *not yet* realized (leaking), and only
a declared horizon separates them."

**What is HELD CONSTANT, stated because R257 requires it to be stated:** the
frame bytes (one generation, one object, both runs), the builder, the row
population, the label column, the decision column, the cohort selection (same
stride, same `max_cohorts`), the corruption strategy and its seed, the comparator
(`ties_available=True`), and the count of probed cohorts. **What varies is one
declared scalar: the label horizon.** A pair varying two things can fire on
either, so its pass proves neither — R257 §3, and the reason that row exists.

### Why L3.1 does not catch it, and why the weaker version would not count

Point L3.1 at the same frames **with the labels frame declared in
`aggregate_frames`**. L3.1's rule for it is `floor(ts) + window = ts + 1s`. At
cohort `F` it corrupts label cells in second `F`; the row that moves is stamped
`F + 1s`, so it lands in `moved_next_second`, `finding()` is `False`, and
`verdict()` returns **`observed_silence`** — a probe that ran, over the frame
carrying the leak, and affirmatively found nothing.

**The weaker version must not be the shipped positive.** Leave the labels frame
out of `aggregate_frames` and L3.1 reports it under `unmodelled_frames` as
`NOT PROBED`, and its silence is `none` — a probe that did not happen. That pair
would discriminate a probe from a non-probe, which is a wiring test wearing the
costume of a discrimination. **The positive must be the first construction, and
an assertion must pin that L3.1's verdict on it is `observed_silence` and not
`none`.**

### Why the model-free check does not catch it

`check_pairwise_label_correlation` screens each built feature against the declared
label at |Pearson| ≥ 0.999 **and** |Spearman| ≥ 0.999 (extended at R231 §5). The
feature is `y_{i−1}` and the label is `y_i`, independent by construction, so both
statistics sit near zero and the check is silent at any threshold in
`LABEL_SCREEN_CASES.md`'s grid. **Both numbers are to be measured and printed by
the positive, not asserted** — a discriminating positive that asserts its own
discrimination has not discriminated.

### What the pair does not cover, named so it is not oversold

Registry 2 (a label *proxy*) and registry 5 (a label built internally from a
past window and reused as a feature) are declared blind spots in `PREREG.md`
§5.3. They are named here and are not candidates for the positive.

---

## (d) What L2a refuses

**The declared inputs, from §4's row and §4.1:**

| path | required |
|---|---|
| both | the callable, and a **label column** |
| **temporal** | `label_availability` — base, horizon, publication delay, as **one** declaration. No profile may default any term (§2.4). The delay defaults to zero **only inside a supplied declaration** |
| **non-temporal** | `labels_available_during_feature_construction = false`, and **no availability model at all** (§2.8, `DESIGN.md` §3) |

**What the registration says happens when they are absent — §2.7:** "If the
required declaration is neither supplied nor defaulted, **L3.1, L2a, and L3.1b
return `unsupported`**, naming the missing element. They do not fall back to row
order." §8.2's boundary: "missing or impossible inputs are unsupported;
supplied-and-valid inputs that then fail are could-not-run", and none may be
displayed in a way mistakable for a pass.

**§2.5's refusal runs in an unusual direction and is registered explicitly:**
`labels_available_during_feature_construction = true` **or absent** both make
L2a `unsupported`. A supplied `true` is neither missing nor impossible, so
§8.2's boundary sentence does not reach it, yet §2.5 and §4.2 route it there in
terms. Determined, and it sits oddly against §8.2 — recorded below.

### The gap between the registered refusal and the shipped one, in kind

**The registration returns a state. The shipped tool raises.**
`require_decision_column` raises `ProbeError`; `plan_slice` raises `SliceError`;
`cli._run_availability` raises `SystemExit`. `ProbeAResult.verdict()` has four
values — `could_not_run(determinism)`, `could_not_run(no_cohorts)`, `finding`,
`observed_silence` — and **`unsupported` is not among them.** There is no state
for L2a to return that the shipped result type can express.

### Where the refusal sits — the population is three entry points, not two

R255 §5's lesson is that a refusal covers the surfaces that *join* at it and no
others. For L2a:

1. **The library export**, a sibling of `run_probe_a` in `availability.py`.
2. **`cli._run_availability`**, which calls into it, so one refusal covers both —
   the same join the slice refusal uses.
3. **`cli._run_checks` → `run_all(built, label=…)`**, which consumes a
   `label_column` today and reaches no probe at all. This is R255 §5's *third
   path, which does not join the other two*, and it carried its own refusal for
   exactly that reason.

**And R238 §1's rule applies to all three:** the refusal must not rest on a
neighbouring line's position. `require_column_name` exists because a
consolidated refusal was weaker than the boundary it replaced, and completeness
was resting on a membership test that happened to sit on the next line.

### The schema version

`_KEYS_BY_VERSION` in `model_file.py` is built on "keys arrive with their
consumer — a key the loader reads and ignores is the discarded-parameter defect
in a file." `label_availability` is a new key, so it arrives at **version 4**, and
a version-3 file naming it is refused.

---

## What you must rule on, before anything is built

1. **The attribution arithmetic.** Reuse `moved_in_second` / `moved_next_second`
   as they stand, or generalise the finding rule to `d(i) < a(y_j)` under the
   declared comparator — which reduces to the shipped rule at `horizon = window`?
   **My reading is that the counters as they stand would report the discriminating
   positive of (c) as clean**, which is the R236 shape. I have not changed them
   and I am not proposing to without your ruling.

2. **The cohort stride.** Derive the required separation from the declared
   horizon, or refuse where the horizon exceeds the gap between corrupted
   seconds? Keeping `97` silently loses attribution on any horizon larger than
   the stride's span.

3. **The label locator.** A new key naming the raw frame and column, or extend the
   existing `label_column`? The existing one is the **built output's** label and
   is classified as non-registered vocabulary. One key doing two jobs is §2.3's
   `panel_mask_scope` / `embargo` defect — "v9's merge gave one name to two jobs".

4. **Refusal shape: raise, or state.** The registration says `unsupported`; every
   shipped refusal raises, and `ProbeAResult` has no `unsupported`. A raise is
   louder and matches the tool; a state matches the registration and can sit in a
   coverage table without being mistakable for a pass. Neither is free and I have
   not picked.

5. **The non-temporal mode: build it, or refuse it, in this round.** It needs no
   availability model and has no cohorts — and §7.2's scoring unit is *feature ×
   affected output **cohort***, with the cohort defined by decision time. Building
   it means naming a cohort identity the registration does not supply.

6. **Which construction is the shipped positive** — (c)'s first version, where
   L3.1 probes the labels frame and returns `observed_silence`, or the weaker one
   where it never probes it and returns `none`. I recommend the first and would
   pin L3.1's verdict on it as an assertion.

---

## For `NEXT_REGISTRATION_REQUIREMENTS.md` — findings, not gaps to fill

Recorded here and not acted on. `DESIGN.md` §2.7 filling any of these would not
make it registered.

- **(i) How "labels built inside the pipeline" is established.** §4.2 makes L2a
  return `unsupported` naming L3.1 as covering detector in that case, and states
  no test for it. It is mechanically derivable — the declared label is absent
  from the raw frames and present in the built output — but the registration does
  not say so, and a derivation this consequential should not be invented at
  build time.
- **(ii) The non-temporal path has no scoring unit.** §7.2's unit is *feature ×
  affected output cohort*; a cohort is rows sharing a decision time
  (`DESIGN.md` §2.3); the non-temporal path has no decision times. §7.2 does not
  say what replaces the cohort there, and §6.5 line 1032 nonetheless requires
  "non-temporal cases under both settings of §2.5's policy" in the corpus.
- **(iii) §2.5 routes a supplied, valid value to `unsupported`.**
  `labels_available_during_feature_construction = true` is neither missing nor
  impossible, and §8.2's boundary sentence covers only missing or impossible
  inputs. The routing is registered in terms; the boundary sentence does not
  reach it.
- **(iv) The cohort is defined in the design document, not the registration.**
  §2.6 and §7.2 use "cohort" as a settled term; the definition sits at
  `DESIGN.md` §2.3. The registration's scoring unit therefore depends on a term
  the registration does not define.
- **(v) §6.2's criteria adjudicate "runtime findings" and name no row** — already
  recorded as §1 item 2 of that file from R188 §3.1. Noted here because building
  L2a is the event that makes two rows eligible and the phrase ambiguous.
