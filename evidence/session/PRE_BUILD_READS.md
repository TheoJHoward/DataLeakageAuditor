# Pre-build reads — two features reported before either is written

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. **No code was written for either feature.**

---

# 1. Inference — the signals, each with a case where it is wrong

**The rule this is written under** (R204, R212 §4.1): inference proposes; it never
picks. It produces a draft model file, not an audit. The audit path refuses an
inferred model that has not been accepted, a finding produced under one carries
that fact, and a column the inference cannot resolve is reported unresolved
rather than defaulted.

**The test R212 set for each signal:** name a case where it would be wrong. *"If
a signal has no wrong case you can construct, you do not understand it yet."*
Every signal below has one. That is the reassuring half; the unreassuring half is
at the end.

### S1 — a datetime column whose name suggests a release instant

`*_at`, `*_released`, `*_published`, `ts_*`. Proposes `at_source_timestamp`
naming that column.

**Wrong case:** `expiry_at`. A datetime column, matching the pattern, holding a
*future* instant — when the contract expires, not when the row became knowable.
Inferring `at_source_timestamp` on it puts availability after every decision in
the frame, and the probe then reports every feature reading that column as
leaking. **A false positive on a legitimate feature, produced by a name.**
`birth_date` fails the same way in the other direction: knowable decades early,
inferred as the availability instant.

### S2 — a key column floored to a second (or minute) boundary for ~all rows

The shape MV-1 measured on `magg.ts_floor` — 464,199 of 464,199 rows exactly on a
wall-clock second. Proposes an aggregate frame with `floor(key) + window`.

**Wrong case:** a 1 Hz sensor lattice. Every stamp is on an exact second and no
row is an aggregate — each is an instantaneous reading, knowable **at** its
stamp, not at stamp + 1 s. The inference adds a full second of latency that does
not exist and manufactures findings for every row deciding inside its own second.
The two cases are **indistinguishable from the column alone**: an aggregate over
[t, t+1s) and an instantaneous reading at t have identical key columns.

### S3 — monotonicity, to tell an event column from a decision column

**Wrong case:** the fixture's own trades frame carries `ts_recv` **and**
`ts_event`, both monotone, both plausible. Monotonicity gives no basis to choose,
and choosing `ts_recv` where the pipeline joins on `ts_event` infers a model of a
pipeline that does not exist. The signal cannot even rank them.

### S4 / S5 — a column constant in the sample, proposing `always`

**Wrong case:** constant *in the window* and not in general. `tick_size` is
genuinely static; a quarterly-revised configuration value sampled inside one
quarter looks identical and is not. The inference reads an accident of the
sampling window as a property of the world. This is also the family R203's
shuffle-check episode already burned: a statistic over one sample reporting
structure that is a property of the sample.

### S6 — the dependency map: which columns the build actually reads

The column probe already produces this, reliably, for free.

**Wrong case, and it is a category error rather than an edge case:** *which*
columns are read is not *when* they became knowable. Availability is a fact about
publication schedules in the world; the dependency map is a fact about the code.
Inferring the second from the first can only produce "this column is read, so it
was available" — **which is the assumption that there is no leak, restated as a
finding.** S6 is the most tempting signal because it is the most reliable, and it
is the one that would turn the tool into a mirror.

### S7 — a column named like the decision column, proposing `at_timestamp`

**Wrong case:** a reference or dimension table whose `timestamp` is its *load*
time. Nothing about that row's decision instant; often far later than the fact it
records.

### What the seven have in common, and it is the finding

**Every signal is a heuristic over SHAPE, and availability is a fact about the
world's publication schedule, which is not in the frames.** S2's wrong case is
the cleanest demonstration: two datasets with byte-identical key columns, one
where `floor(key) + window` is right and one where it is a full second wrong, and
no observation of the data distinguishes them. The information is not there to be
inferred — it is a fact about how the data was produced, which only the producer
knows.

**So inference cannot be made correct by better signals.** It can be made
*useful* by being a draft: every proposal annotated with the evidence that
produced it, every unresolved column named as unresolved, and the whole thing
refused by the audit path until a human has read it. That is the shape already
ruled, and this read supports it rather than qualifying it.

**One signal I would not ship at all: S6.** The others produce wrong answers a
reader can catch by looking at their own data. S6 produces an answer that is
always self-consistent and always says "clean", and a draft containing it would
be hardest to review precisely where review matters most.

---

# 2. The shuffle check — four answers, and the first one ends it

### 1. Which statistic, and does it detect leakage or signal?

**It detects SIGNAL. The check as conceived is the wrong check.**

A permutation test comparing the real-label score against a shuffled-label null
tests the hypothesis *"the features carry no information about the labels."* A
clean, working model rejects that hypothesis — **rejecting it is what a working
model does.** The statistic is a signal detector, and firing it on a good clean
pipeline is its correct behaviour, not a false positive.

Leakage is a different proposition: that the test score is *inflated* because
information about test labels reached the training features. The label-permutation
null says nothing about it. A pipeline with no leak and real signal, and a
pipeline with a leak and real signal, both reject the null identically.

**That is this round's result for the shuffle check, and it is a clean one.**

**Two shapes that would be about leakage, named so the next round starts from
something:**

- **Permute the SPLIT, not the labels.** Score the declared split against scores
  from random splits of the same sizes. Random splitting being *better* than the
  declared temporal split is a recognised leakage signature. It is a statement
  about the split rather than about the pipeline, which is a narrower claim than
  the one wanted — and it needs no chance level, because the comparison is
  between two empirical distributions.
- **Shift features forward in time relative to labels.** If predictive power
  survives a shift that should destroy it, something is reading ahead. Closer to
  the actual proposition, and confounded by autocorrelation — in this fixture's
  data, badly.

Neither is what was proposed, and neither is endorsed here. They are named so
that "the check was wrong" does not read as "there is nothing there."

### 2. Is "chance" knowable for a user-supplied `evaluate()`?

**Split answer, and the split is the useful part.**

For the **signal** test, chance IS knowable without any declaration — the
shuffled-label scores *are* the null distribution, estimated empirically. This
corrects the premise that the tool cannot know chance: for the statistic that was
proposed, it can.

For a **leakage** statistic, there is no analogous null to sample, because the
counterfactual is "the same pipeline without the leak" and the tool cannot
construct it.

**But `evaluate()` is under-specified in a way that bites either way:** it returns
a bare number with **no declared direction**. Whether higher is better is not
knowable from a callable, and a permutation test that assumes the wrong direction
inverts its own conclusion silently. That is the `_UNWIRED` shape exactly — a
declared direction, or a refusal naming what would consume it. Range and chance
level are not needed if the null is sampled; direction is needed regardless.

### 3. The pre-commitment

**Not stateable for the check as conceived**, because a threshold on a statistic
that answers the wrong question is a number with no meaning. Refusing to state
one is the honest output rather than an omission.

**For whichever statistic replaces it, fixed before any run and derived from the
metric's definition rather than from this fixture:** the shuffle count is set by
the p-value resolution wanted — a permutation p cannot be finer than 1/(N+1), so
N = 999 for a resolution of 0.001 — and alpha is fixed by convention before the
first run. Both are properties of a permutation test and of nothing in this data,
which is what makes them stateable in advance.

### 4. The known positive — and it exposes a limit of the known-positive rule

The positive is the frame where a feature **is** the label, or a lagged copy.

**It would fire. That is the problem.** A feature-is-the-label frame produces a
near-perfect score and a null far below it, so the signal test fires — and the
leakage test would fire, and so would almost any statistic anyone proposed. **A
known positive that fires for every candidate statistic cannot discriminate
between them.**

So the discipline that has protected this project repeatedly would not have
caught this. It confirms that a check *responds to the phenomenon*; it cannot
confirm that the check *computes the intended quantity*. TB-12 says a known
positive tests the premise and not only the code — this is the next layer down:
**a known positive tests that something is detected, not that the right thing is
being measured.**

What would discriminate is a **negative** the wrong statistic fails: a pipeline
with strong genuine signal and **no** leak. The signal test fires on it — loudly,
correctly by its own lights, and wrongly as a leakage report. That case
separates the two statistics, and any future shuffle check is built against it
before its positive.

---

# 3. Rulings from these reads — R215

## 3.1 The shuffle check is RETIRED, not replaced

**Status: retired. The slot it occupied is closed, not vacated.**

The analysis is in §2 above and the next person to propose a shuffle check should
meet it rather than repeat it: **a permutation test of the real-label score
against a shuffled-label null detects SIGNAL, not leakage.** A clean working model
rejects that null; rejecting it is what a working model does.

**Why nothing replaces it, and the third reason is the one to keep:**

1. **No missed leak has been demonstrated.** The availability probe is the
   registered detector and nothing has shown a leak it misses. The case for a
   second detector class starts from a missed leak, not from a line in a plan.
2. **The two shapes named below point at different failure classes.** Neither is
   a variant of the retired check.
3. **A vacated slot in a plan has gravity.** The plan still says *something goes
   here*, and what falls in is chosen by the shape of the hole rather than on its
   merits. That is how a project acquires features nobody argued for. **So the
   slot is closed with a reason, which is a decision, rather than left open,
   which is a gravity well.**

### Two shapes, recorded as UNEVALUATED PROPOSALS

**Explicitly not endorsed. Explicitly not inheriting the retired slot.** Each
would need its own establish step — the same four questions §2 answered for the
retired check — before any code.

- **Permute the SPLIT, not the labels.** Score the declared split against random
  splits of the same sizes. Random splitting scoring *better* than a declared
  temporal split is a recognised leakage signature. It needs no chance level, and
  it is a claim about the split rather than about the pipeline — narrower than
  what was wanted.
- **Shift features forward in time relative to labels.** If predictive power
  survives a shift that should destroy it, something reads ahead. Closer to the
  proposition, and confounded by autocorrelation — badly, in this fixture's data.

## 3.2 A standing requirement on any user-supplied scoring callable

**Filed as a requirement on the SHAPE, not on the retired check, so it outlives
the feature it was found in.**

> **Any surface that accepts a user-supplied scoring callable must have the
> callable's DIRECTION declared, or refuse.** `evaluate(...) -> score` returns a
> bare number. Whether higher is better is not knowable from a callable, and a
> permutation test — or any comparison against a null — with the direction wrong
> inverts its own conclusion **silently**. This is the `_UNWIRED` shape: a
> declared direction, or a refusal naming what would consume it.

**Note what is NOT the requirement**, because an earlier reading got this wrong:
chance level does not need declaring where the null can be sampled — the
shuffled scores *are* the null, and the metric's scale cancels. Direction does,
always, and it is the smaller and truer gap.

## 3.3 Inference — the split the killer case forces

**"Propose, never declare" is not good enough**, and the reason is in §1's S2.
Two datasets can have byte-identical key columns where flooring is right for one
and a full second wrong for the other. A draft presented as *the tool's proposal,
please review* gets rubber-stamped, and a rubber-stamped guess about publication
schedules is the mirror the whole design was avoiding.

**The line lands exactly where the information does:**

> **Infer what is IN the data. Require what is ABOUT the world.**

| | what the tool does |
|---|---|
| **Structure** — column identification, key candidates, granularity, join shape, whether a key sits on second boundaries | **Determined, filled in, marked as determined-from-data**, with the evidence named per column |
| **Availability** — publication lag, availability instant, when a value became knowable | **Left UNFILLED**, with the observable evidence attached beside each column to help the user fill it — never with a value |

- **The audit refuses an unfilled availability field.** It does not default it,
  and it does not read "the user left it" as agreement.
- **A column whose STRUCTURE cannot be determined is also unfilled**, with the
  ambiguity named. §8.2's shape applies: not resolved is reported as not
  resolved, never as a default.

### The draft's header sentence — the feature depends on this landing

> **The structure below was determined from your data. The availability column is
> blank because your data does not contain it: when a value became knowable is a
> fact about how it was published, not a shape in the frames — two datasets with
> identical timestamps can have availability a full second apart. Fill it in, or
> the audit will refuse rather than guess on your behalf.**

## 3.4 S6 — the dependency map — omitted in code, and the reason placed where a person looks

**The ruling, to be quoted verbatim wherever this lands:**

> *Which columns are read is not when they became knowable; it can only produce
> "read, therefore available" — the assumption of no leak restated as a finding.*

**Refusing in code is the wrong instrument here.** `_UNWIRED` refuses on a path a
user already reasonably takes. There is no signal-selection surface, so a refusal
would mean building a request path for the sole purpose of declining on it.

**But omission is invisible, and S6 is the most reliable-LOOKING signal in the
set** — which makes it precisely what a future contributor adds as an obvious
improvement, having never seen this argument. So the reason goes in three places
a person actually looks:

1. **The draft's own output** — a line naming which signals were used, and that
   the dependency map was deliberately not one, with the reason. *(Conditional on
   the draft existing; no inference code has been written.)*
2. **A comment at the signal registry**, where someone adding a signal is already
   reading. *(Same condition.)*
3. **Here**, which exists now and is where the analysis lives.

**The conditional, recorded now so it is not rediscovered:** *if a
signal-selection surface is ever built, S6 gets an explicit refusal on it then.*
