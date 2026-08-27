# THE `aggressor_side` CLASS — A PROPOSAL. NOTHING IS BUILT.

**27 August 2026. `phase1`.** R135 §4 deferred the question — *"whether it earns a third detector is
a design question for after the sweep"* — and R145 §4 asks for it now: **propose, do not build.**
No code in this document exists; no detector is added; `detectors.py` is untouched.

**Recommendation up front: do NOT build a third detector. Make the existing screen a reporting
obligation.** The reasoning is below, including the case against my own recommendation.

---

## 1. WHAT THE CLASS IS, precisely

A column the builder **reads and executes**, whose value **cannot move the output on this corpus**,
because a guard over it is **false for every row**:

```python
is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \
         else trades["side"].isin(["B","Buy","buy"])
```

The column holds `SELL_AGGRESSOR` / `BUY_AGGRESSOR` / `UNKNOWN`. The `isin` set is `B`/`Buy`/`buy`.
**The predicate is false for every row, so `is_buy` is a constant.**

**This is not a dead branch.** `trades.side` was the other surviving candidate and it is a different
thing entirely: its reference sits in the `else` limb of a ternary whose `if` limb always fires. The
reference never executes. **A dead predicate and a dead branch look identical from the outside and
are not the same defect**, which is why the screen captures the enclosing function and the receiver.

**The class has exactly one member on this fixture** — 14 silent cohorts → 3 name matches → 2
same-frame → 1 after the collision is removed.

## 2. WHY EVERY EXISTING PROBE IS BLIND — by mechanism, not by power

| probe | what it perturbs | why it cannot see this |
|---|---|---|
| `valueread` | permutes the column's values | every permutation of `SELL_AGGRESSOR`/`BUY_AGGRESSOR`/`UNKNOWN` leaves the predicate false |
| `nullread` | substitutes nulls | a null is not in the `isin` set either — still false |
| `promote_ood` / `SENTINEL_OOD` | substitutes an out-of-**dtype** sentinel | **it never runs at all** — see below |

**The OOD strategy is not merely blind here; it is ineligible.** `aggressor_side` is an `object`
column, and `_ood_target_dtype` returns `None` for `object` in terms: *"every value is
representable, so no insertion can change the dtype. There is nothing to promote TO."* The strategy
refuses as `Unsupportable` rather than running and reporting silence — which is the correct
behaviour, and worth stating because **a refusal and a silence are different facts** and only one of
them is evidence. *(This is consistent with B9-S, where `sentinel_ood` found 0 unique pairs across
the whole sweep.)*

**So the two probes that do run both perturb within the observed domain, and the predicate is false
across all of it.** The one region that would move the output is the *satisfying set of the guard*,
and no probe working from the data can find it, because **the satisfying set is a property of the
source, not of the corpus.**

**Adding a fourth value-perturbing detector would be blind for the same reason.** This is not a
coverage gap that more probing closes.

## 3. THE REAL FINDING — silence here is not silence elsewhere

On this fixture the guard is unsatisfied. **On a corpus where `aggressor_side` holds `"B"`, the
guard is satisfied and the dependence is live.** So the truthful statement is not *"this column does
not affect the output"* but:

> **no dependence was observed on this corpus, and the reference is live, and the guard's satisfying
> set is disjoint from the values present.**

That is precisely the distinction §6.6 already registers — **`observed_silence` is not `none`**
(l.1101: *"at least one valid execution occurred and none produced a finding"*) — and precisely what
§39 requires: **silence is honest only with its domain attached.**

**So the defect is in the REPORT, not in the detector suite.** A suite that reports `none` here is
making a claim about all corpora from evidence about one.

---

## 4. THE OPTIONS, with the case against each

### Option A — a third detector: the satisfying-value probe

Parse the builder's source, recover each guard's literal set (`["B","Buy","buy"]`), inject those
values, re-run, compare.

**Against it, and this is decisive:** *its domain cannot be stated.* A guard like `x > threshold`, a
regex, a lookup against another frame, or any computed set has **no finite literal set to recover**.
The probe would work on `isin([...])` and silently find nothing everywhere else — and **"found no
candidate values" would render as silence, which reads as clean.** That is the
never-fired-reads-as-clean failure this project has now hit four times in adapters alone. A detector
whose coverage depends on the *syntactic shape* of the guard has a domain no one can write down,
and §39 forbids reporting a silence whose domain cannot be stated.

**Also against it:** the class has **one** member. A detector that fires this rarely can never be
calibrated, and an uncalibrated detector's null is not informative.

### Option B — a new `evidence_outcome` value

Add a fourth value distinguishing *silent-and-unreferenced* from *silent-but-referenced*.

**Against it:** §6.6's two-axis resolver has **ten legal pairs** and a registered enumeration. Adding
a value is a **class C amendment to a registered text**, needing its own approval — an expensive move
to carry information that a published exception carries for free. **And it is the wrong axis:**
`evidence_outcome` describes what an execution produced; this is a fact about what the *source
references*, which is not an execution outcome at all.

### Option C — the screen becomes a reporting obligation ← **RECOMMENDED**

`tests/phase1/reference_but_silent.py` already exists, is tested, and **halts rather than returning
an empty candidate list when pointed at the wrong source.** Promote its output from a diagnostic to a
**required published exception**: every silent-but-referenced column is named in the gate report,
with its enclosing function and receiver, and the run's silence for that column is published **with
its domain attached** rather than as a clean result.

**In the §9.2 vocabulary this is `covered_with_exclusion`, never a pass** — the same shape as SC-6's
`unscored`: *a unit the apparatus cannot score, named rather than counted clean.*

**Against it, stated honestly:** it detects nothing. It converts an invisible limit into a visible
one and stops there — a human still reads each candidate and answers in two lines. **That is the
whole of what it offers, and it is why it should be preferred:** the alternative is a detector that
would claim to answer the question and would answer it only for guards of one syntactic shape.

---

## 5. WHY C, IN ONE SENTENCE EACH

- **The suite's blindness here is structural, so no probe removes it** — only disclosure does.
- **A detector for a one-member class cannot be calibrated**, and its nulls would carry unearned weight.
- **Option A's domain is unstatable**, and an unstatable domain is exactly what §39 refuses.
- **The screen already exists and already halts correctly** — the work is promotion, not construction.
- **A red that says one true thing beats a green bought by a probe that only reads `isin`.**

## 6. WHAT C WOULD NOT ESTABLISH — stated so it is not oversold

It does **not** find constantly-false predicates. It finds **columns referenced but unmoved**, which
is a **superset**: a candidate may be a dead branch, a name collision across frames, an unprobed
frame, or a genuine dead predicate. **Every candidate remains a question for a human**, and the
screen's value is only that there are now one or two of them instead of fourteen silences to read.

It also does **not** generalise beyond the builder whose source it reads. Pointed at the wrong
source it **halts** — deliberately — because **an empty screen is not an empty finding.**

## 7. WHAT WOULD CHANGE THE RECOMMENDATION

- **The class gains members on another fixture.** One member is an anecdote; five would be a
  population, and a population can calibrate a detector.
- **The guards in scope turn out to be uniformly `isin`-shaped.** Then Option A's domain becomes
  statable and it stops being a probe with a hidden edge.
- **A metric or gate comes to depend on the distinction.** Nothing does today; the screen's output is
  read by a human and by nothing else.

---

**Status: PROPOSED, NOT BUILT.** No detector added, no registered text touched, no `evidence_outcome`
value introduced. R135's design question is answered with a recommendation and its counter-case;
adopting it is the author's call, and adopting it would itself be a change to what the gate report
publishes.
