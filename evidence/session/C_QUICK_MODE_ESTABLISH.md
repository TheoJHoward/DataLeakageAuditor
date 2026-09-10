# `quick` as a CI default — what it is, what it licenses, and what it costs

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures. This is a Phase 2 establish report. **No code was
written for C in the round that produced it.**

**Why it is asked now.** L2a rebuilds once per cohort. Cost is therefore the
first thing a stranger meets, and CI is where a stranger runs the tool.
`--stride` and `--max-cohorts` ship; the framing around them does not.

---

## (a) What `quick` is on disk, and what the registration says about subsampling

**`DESIGN.md` §5.2, quoted whole — it is three sentences:**

> **`quick` mode is first-class.** Documented as the CI default, not a degraded
> option. Its coverage table states probed-cohort count and row coverage, and
> `assert_audit_complete()` treats a `quick` run as complete — cohort coverage is
> not detector coverage. Reach refinement is off, so reaches are suppressed
> rather than guessed.

**`DESIGN.md` §2.3** names it as one of four cohort-selection modes — "`full`,
`quick`, `dense_early`, explicit list" — and says selection is config: "evenly
spaced across the middle, skipping the leading and trailing exclusion fraction
where windows are NaN-padded, skipping profile intervals."

**Three things follow from that, and they are the design's claims rather than the
registration's:** `quick` is a named mode; it has a coverage table with two
specific numbers in it; and a `quick` run is *complete*, on the ground that
cohort coverage and detector coverage are different questions.

**What the registration says about subsampled cohorts.** It never defines
`quick`'s stride or cohort count, and it does not need to — what it fixes is what
a subsampled run's numbers MEAN:

- **§2.6, the licence limit, locked in both directions:** *"A change at any row
  with `d(i) ≤ d` is a valid finding"* and *"**Silence is informative only for the
  cohort `d(i) = d`.**"* That second clause is the whole of the CI question: a
  probe that skipped a cohort has said nothing about it.
- **§7.2** publishes an **unprobed feature-cohort rate** — *"fraction of labelled
  pairs whose affected cohort was not itself probed. A coverage statistic,
  independent of incidental detection"* — and rules that *"A pair whose cohort was
  never probed counts as a miss **only when no valid probe detected it**."*
- **§6.11's aggregation rule:** *"A cohort counts as probed for a combination when
  at least one strategy of that combination validly executed it."*
- **§7.2.1** mentions `quick` in passing, as the case that makes a bare fraction
  unfair to a strategy: *"a bare fraction condemns a strategy on one failure in a
  five-cohort `quick` run."* So the registration knows the mode exists.
- **§8.5's neighbourhood, line 1701:** *"Whether refinement runs at all is the
  frozen `reach_refinement_policy`, **not a property of `full` or `quick`**. Those
  modes may supply defaults; the policy is serialized configuration like any
  other decision-affecting value (§6.8)."* **This contradicts `DESIGN.md` §5.2's
  "reach refinement is off" if that is read as a property of the mode**, and the
  registration governs: `quick` may supply the default, and the policy is the
  frozen key.
- **§13's scale note, line 2201, explicitly not a locked figure:** *"with
  refinement off, the full audit is in the high eighties and `quick` is in the mid
  teens."* Those are **run counts** from `DESIGN.md` §5.1's formula, not seconds.

**So the registration constrains the accounting and leaves the schedule to the
design.** That is the right split, and it means C is mostly a reporting job.

---

## (b) What a quick result licenses, and how the result carries it today

**The registered licence, stated as the output would have to state it:** a
silence over a subsample is `observed_silence` **over the probed cohorts** and
`none` **over the rest**, and both numbers have to be visible, because §2.6 makes
the second set exactly the set the run said nothing about.

**What the tool carries today, measured rather than recalled:**

| what the licence needs | today |
|---|---|
| an outcome-classed exit code | **EXISTS.** `0` silent, `1` findings, `2` usage, `3` nothing probed |
| `none` distinguished from `observed_silence` at the exit code | **EXISTS**, and as of this round the verdict behind it is licensed too |
| probed-cohort count | **EXISTS** as `n_cohorts`, printed |
| row coverage — the fraction of output rows falling in a probed cohort | **DOES NOT EXIST.** No module computes it |
| a statement that cohorts were dropped by the cap | **DOES NOT EXIST** |
| a coverage table | **DOES NOT EXIST.** No module defines one |
| `assert_audit_complete()` | **DOES NOT EXIST** |

**The gap that matters is the exit code, and it is precise.** A run that probes
5 cohorts of 72 available and finds nothing exits **0**, exactly as a run that
probed all 72 and found nothing does. **The 0 reads as clean for cohorts that
were never probed.** Measured: on a 500-second frame at stride 7, 72 seconds are
candidates, `--max-cohorts 5` keeps five, `n_cohorts` reports 5, **and no note in
the run mentions the other 67.** The truncation is silent at the point where it
happens — `picked = seconds[::cohort_stride][:max_cohorts]` — and nothing
downstream reconstructs it.

**So today the answer to "what does a quick result license" is: less than the
run's exit code implies, and the run does not say by how much.** That is C's
subject.

---

## (c) The cost model, measured at fixture scale

**Measured, not estimated**, on the acceptance fixture `zc 2025-01` at
`b975ca7` plus this round's working tree, CPython 3.12.10 / numpy 2.4.2 /
pandas 3.0.1, by `evidence/session/r262_cost_per_cohort.py`. Fixture capture is
39 s and is excluded from every figure below; it happens once per process.

**The frame the figures need.** One clean build of the fixture's pipeline is
**34.6 s** over 2,123,847 raw rows across three probed frames, producing 338,159
rows by 87 columns. **That build is the unit both rows pay in**, and the whole
cost question is how many times each of them pays it.

| row | 1 cohort | 5 | 25 | marginal per cohort |
|---|---|---|---|---|
| **L3.1** | 185.7 s | 181.0 s | 181.5 s | **≈ 0.02 s** |
| **L2a** | 118.4 s | — | — | **≈ 48 s** |

L2a was timed at 1, 2 and 4 cohorts: 118.4 s, 168.2 s, 262.4 s, giving marginals
of 49.8 s and 47.1 s. Total run 1,171 s.

**The 5-cohort L3.1 figure is 4.7 s BELOW the 1-cohort figure**, a marginal of
−1.156 s per cohort, which is not a cost and is reported rather than smoothed:
it is run-to-run variation on a ~180 s measurement, and it is the honest reading
that **L3.1's marginal cohort is below this instrument's noise floor.** The
25-cohort figure gives 0.021 s and is the number to quote, with the caveat that
it too is inside the noise.

**What the two shapes mean, and it is the whole of C's cost problem.**

- **L3.1's cohorts are free.** It corrupts every probed second in ONE rebuild, so
  the run is one build plus classification whether it probes one cohort or three
  hundred. `--max-cohorts` buys almost nothing on this row.
- **L2a's cohorts cost a build each**, because §4.2 masks per cohort and
  `DESIGN.md` §5.1 gives the row a `C × S` term. 48 s per cohort against 34.6 s
  for the build itself is the build plus its corruption and comparison, and it is
  linear with no flat part to amortise.

**So the extrapolation a CI operator needs:** a full L3.1 audit of this fixture
is about three minutes at any cohort count. **L2a at 25 cohorts is about 21
minutes, and at the same 300 cohorts the guard uses it is about four hours.**
Those two extrapolate from the measured marginals and are labelled as
extrapolations; only the rows in the table were run.

**One consequence for the mode, stated because it falls out of the numbers and
not out of any reading.** A single `quick` setting cannot serve both rows well:
the cohort count that makes L2a affordable costs L3.1 almost nothing to raise,
and the cohort count that gives L3.1 its full coverage makes L2a unusable in CI.

---

## (d) What CI needs that the tool lacks

**1. Exit codes by outcome class — mostly there, one class missing.** The four
codes exist and are already outcome-classed. What has no code is *silent, but
over a subsample*: it is indistinguishable from *silent over everything*. A CI
job cannot gate on coverage it cannot see.

**2. A stable one-screen summary — not there, and drifting the wrong way.** The
run prints a notes block that has grown every round; this round alone added the
attribution counts, the separation figure, the silence licence and L2a's
per-cohort cell counts. Every one of those earns its place in a report and none
of them belongs in the first screen a CI log shows. **The failure mode is
specific: a summary nobody can read is a summary nobody reads**, and this
project's own register is full of figures that were present and unread —
D-V30A-100 was exactly that, a note carrying the truth beside a verdict that did
not.

**3. A time bound that refuses rather than truncates silently — not there in
either half.** There is no wall-clock bound at all. `--max-cohorts` is the only
bound and it truncates without a word, which is the same defect one level up: a
cap that reports nothing produces a smaller answer that looks like the same
answer. **A bound that refuses is the shape this project has already settled on
twice** — the slice rule refuses a slice with no declared padding, and L2a
refuses a declaration supplied in part.

**4. One thing not on the delta's list, and it is the largest.** L2a's cost is
linear in cohorts because it rebuilds per cohort, and that is the registered cost
model rather than an implementation choice. **A CI default that runs both rows
has to schedule them differently**, or L2a sets the budget for the whole audit.
Whether that means a smaller cohort count for L2a, a different default mode per
row, or something else is a design question this report does not answer.

---

## What this report does not establish

It does not propose a cohort count for `quick`, does not say what row coverage
should be required, and does not choose an exit-code scheme. Those are the
rulings C's build needs and they are not takeable from the reading: the
registration deliberately leaves the schedule to the design, and the design's own
three sentences predate both runtime rows being built.
