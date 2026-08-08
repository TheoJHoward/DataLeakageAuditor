# EXPECTED_OUTPUTS — registration trace suite

**Generated from `tests/registration/traces.py` by
`generate_expected_outputs.py`. Do not edit by hand — regenerate.**

This is the artifact PREREG §6.6.1 puts first in the human read: the
expected outputs are derived by the author from the prose, so a misreading
can be encoded in both the reducer and this table. Reading it is the check
the machine cannot perform.

Every value below is also pinned by hand-derived expectations in
`traces.py`; `test_expected_outputs.py` fails if this file drifts from what
the reducer computes.

## Interpretation notes — all resolved as of v29

- **I1 (pair-level vs case-level denominators): confirmed.** PREREG §7.4
  (since v28) defines both denominators for every row including runtime:
  proof/evidence yield and the unprobed rate use the pair-level
  *scope-eligible* denominator, so labelled pairs from `not_applicable` and
  `unsupported` cases remain in them as misses (T14–T16); case-level rates
  use the *execution-eligible* membership of §7.7
  (`schedule_state ∈ {completed, incomplete}`).
- **I2 (short_circuited exclusion): confirmed.** `short_circuited` cases
  are excluded from every metric denominator including the pair-level ones
  (PREREG §6.6); they cannot arise in an evaluation run, so no published
  number depends on the exclusion (T08–T10).
- **I3 (unit grammar): resolved.** `feature` is in §7.0 rule 2's grammar
  (since v28), so feature discovery recall's unit is legal.
- **Canonized by v29:** the missing-trace protocol violation (§6.6's
  explicit-trace paragraph), the within-case scoring key with corpus-level
  case identity (§7.2), and the count-over-all-cases shape of the
  `not_applicable`/`unsupported`/`short_circuited` counts (§7.2.1) — the
  three decisions this suite previously carried as interpretation are now
  locked prose.
- **v30 suppression (§7.2.1).** A combination that is `not_applicable` on
  every scope-eligible case in a body publishes its counts and suppresses
  its yields, rates, and gate, naming the reason — a suppressed metric
  never renders as a number. The v30 closure pass ratified the granularity
  this suite implements: a scope-eligible case is every labelled case in
  the body, clean cases included (which is why T17's clean case had to be
  `not_applicable` for suppression to apply). The auto-added all-`not_applicable` promoted
  rows (T01–T04, T06–T08, T13–T16) and T15/T16's preserving rows are
  suppressed below; T05/T09/T10's promoted rows carry real promoted traces
  and publish numerically. T17 pins whole-body suppression on a multi-case
  body and T18 pins that a mixed body is NOT suppressed, its
  `not_applicable` cases contributing misses per §7.2/§7.4.

*(Metric ids contain literal `|` separators; in the tables below they are
escaped as `\|` so markdown renderers keep the columns intact.)*


## T01 — zero valid executions

Prose basis: PREREG §6.6 (incomplete, reason precedence), §7.2 (miss stays in)

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: invalid(determinism); shuffle@c2: invalid(determinism)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t01`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t01`) → `incomplete(determinism)` × `none`
- `L3.1|promoted` (`t01`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|combination_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 1 | 0 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 1 | 0 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> Guard failed everywhere: the labelled pair is a miss and stays in the proof-yield denominator; nothing was probed. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T02 — valid silence, then a later failure

Prose basis: PREREG §6.6 (totalized evidence_outcome — the v23 counterexample)

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, silence; shuffle@c2: invalid(compatibility)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t02`: leaking pairs [('f1', 'c2')]

**Expected state pair:**

- `L3.1|preserving` (`t02`) → `incomplete(compatibility)` × `observed_silence`
- `L3.1|promoted` (`t02`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|combination_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 1 | 0 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 1 | 0 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> observed_silence covers the executions actually performed, never the schedule. The leaky cohort c2 was never probed, so cohort sensitivity has an empty denominator. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T03 — valid finding, then a later failure

Prose basis: PREREG §6.6 (incomplete x finding), §7.2.1 (findings from incomplete schedules count), §7.7

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: invalid(compatibility)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t03`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t03`) → `incomplete(compatibility)` × `finding`
- `L3.1|promoted` (`t03`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|combination_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 1 | 1 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> Proof yield 1/1 while conditional recall is undefined (no completed case): the two metrics answer different questions. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T04 — two strategies, one fails and one succeeds

Prose basis: PREREG §6.6 (reason precedence: compatibility over crash), §6.11

- `L3.1|preserving` — context evaluation, strategies ['shuffle', 'noise'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: valid, silence; noise@c1: invalid(compatibility); noise@c2: invalid(crash)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t04`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t04`) → `incomplete(compatibility)` × `finding`
- `L3.1|promoted` (`t04`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|combination_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 1 | 1 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> Both cohorts count as probed for the combination — shuffle validly executed them (PREREG §6.11 aggregation). noise's failures leave the schedule incomplete under reason precedence. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T05 — a promoted finding before any preserving execution

Prose basis: PREREG §6.5 (regardless of which ran first), §7.2 (two events, one PROVEN finding with corroboration)

- `L3.1|promoted` — context evaluation, strategies ['complex'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: complex@c1: valid, finding(f1@c1); complex@c2: valid, silence
- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: valid, silence
- labels `t05`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|promoted` (`t05`) → `completed` × `finding`
- `L3.1|preserving` (`t05`) → `completed` × `finding`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 1 | 1 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|promoted\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|promoted\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | 1 | 1 | 1 |
| `L3.1\|promoted\|evidence_yield` | 1 | 1 | 1 |
| `L3.1\|promoted\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|promoted\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|promoted\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

> Two EvidenceEvents (one per combination), one ReportedFinding at PROVEN with the promoted event as corroboration.

## T06 — a completed clean case with a finding

Prose basis: PREREG §7.7 (clean-case finding rate), §10.2 criterion 3

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: valid, silence
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t06`: clean (no leaking pairs)

**Expected state pair:**

- `L3.1|preserving` (`t06`) → `completed` × `finding`
- `L3.1|promoted` (`t06`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 1 | 0 |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|preserving`: experimental=True (finding gate fired=True, completion gate fired=False; clean N=1, k=1, completed=1)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> N=1 clean case, k=1 false finding: k >= floor(0.20*1)+1 = 1, so the finding gate fires. Yield denominators are empty on a clean-only corpus and read None, never 0.0 or 1.0. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T07 — an incomplete clean case with a finding

Prose basis: PREREG §7.7 (no false finding escapes the gate because its schedule later failed), §10.2 criterion 3 (completion floor)

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: invalid(compatibility)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t07`: clean (no leaking pairs)

**Expected state pair:**

- `L3.1|preserving` (`t07`) → `incomplete(compatibility)` × `finding`
- `L3.1|promoted` (`t07`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|combination_incompletion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 1 | 0 |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|preserving`: experimental=True (finding gate fired=True, completion gate fired=True; clean N=1, k=1, completed=0)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> The incomplete case sits in both clean-case denominators; the false finding still counts and the completion floor also fires. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T08 — a combination's own terminal finding, remaining work unrun

Prose basis: PREREG §6.6 (short_circuited covers a combination's own terminal finding — the v24 gap), user runs only

- `L3.1|preserving` — context user, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=yes
  - records: shuffle@c1: valid, finding(f1@c1)
- `L3.1|promoted` — context user, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=yes
  - records: (no records)
- labels `t08`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t08`) → `short_circuited` × `finding`
- `L3.1|promoted` (`t08`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|short_circuited_count` | 1 | 1 | 1 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> short_circuited x finding is legal; the case is excluded from every metric denominator and published only as a count. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T09 — REVIEW evidence, then another combination's terminal finding

Prose basis: PREREG §6.6 (short_circuited x finding — being cut short says nothing about whether evidence was already observed)

- `L3.1|promoted` — context user, strategies ['complex'], cohorts ['c1', 'c2'], inputs available, terminal=yes
  - records: complex@c1: valid, finding(f1@c1)
- `L3.1|preserving` — context user, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=yes
  - records: shuffle@c1: valid, finding(f1@c1)
- labels `t09`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|promoted` (`t09`) → `short_circuited` × `finding`
- `L3.1|preserving` (`t09`) → `short_circuited` × `finding`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|short_circuited_count` | 1 | 1 | 1 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|combination_completion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|combination_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|evidence_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|short_circuited_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

> The promoted combination recorded REVIEW evidence at c1 before the preserving combination's terminal finding preempted it.

## T10 — valid silence, then another combination's terminal finding

Prose basis: PREREG §6.6 (short_circuited x observed_silence; completed under a terminal decision when nothing remained)

- `L3.1|promoted` — context user, strategies ['complex'], cohorts ['c1', 'c2'], inputs available, terminal=yes
  - records: complex@c1: valid, silence
- `L3.1|preserving` — context user, strategies ['shuffle'], cohorts ['c1'], inputs available, terminal=yes
  - records: shuffle@c1: valid, finding(f1@c1)
- labels `t10`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|promoted` (`t10`) → `short_circuited` × `observed_silence`
- `L3.1|preserving` (`t10`) → `completed` × `finding`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 1 | 1 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|combination_completion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|combination_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|evidence_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|short_circuited_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

> The preserving schedule had one selected cohort and finished it, so a terminal decision with nothing unrun resolves completed, not short_circuited. The promoted row is preempted mid-schedule.

## T13 — a completed clean case with no event at all

Prose basis: PREREG §6.6.1 (every case-level metric includes no-event cases)

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, silence; shuffle@c2: valid, silence
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t13`: clean (no leaking pairs)

**Expected state pair:**

- `L3.1|preserving` (`t13`) → `completed` × `observed_silence`
- `L3.1|promoted` (`t13`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|preserving`: experimental=False (finding gate fired=False, completion gate fired=False; clean N=1, k=0, completed=1)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> A clean case that produced nothing still sits in its own denominator: clean-case finding rate is 0/1, not 0/0. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T14 — unsupported: strategies resolve, inputs missing

Prose basis: PREREG §2.7 (undeclared means unsupported, never pass), §6.6, §7.2 (the pair stays in — interpretation note I1)

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs MISSING, terminal=no
  - records: (no records)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t14`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t14`) → `unsupported` × `none`
- `L3.1|promoted` (`t14`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_completion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|feature_discovery_recall` | 0 | 1 | 0 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|proof_yield` | 0 | 1 | 0 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 1 | 1 | 1 |
| `L3.1\|preserving\|unsupported_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> The case leaves every case-level denominator and is published as a count, while its labelled pair stays in the pair-level yield denominator as a miss — dropping it would convert missing coverage into a better rate. The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T15 — not_applicable: no strategy resolves to this status

Prose basis: PREREG §6.6 (resolution order step 1), §7.2 (a case whose only firing strategies promoted contributes misses — note I1)

- `L3.1|preserving` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t15`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t15`) → `not_applicable` × `none`
- `L3.1|promoted` (`t15`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|preserving\|proof_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|preserving`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> Preserving row on a case where nothing resolves preserving. In this one-case body the combination is not_applicable everywhere, so its yields, rates, and gate are suppressed with the counts as the honest signal (PREREG §7.2.1, v30); in a mixed body the labelled pair stays a yield miss (T18). The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T16 — not_applicable: strategies resolve, no eligible cohort selected

Prose basis: PREREG §6.6 resolution order step 1, second clause (v28) — vacuous completed x none is illegal, so nothing-to-do resolves not_applicable

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts [], inputs available, terminal=no
  - records: (no records)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t16`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t16`) → `not_applicable` × `none`
- `L3.1|promoted` (`t16`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|preserving\|proof_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|preserving\|unsupported_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 1 | 1 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 1 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 1 | 0 |

Gate `L3.1|preserving`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> Resolved strategies, available inputs, zero selected eligible cohorts: not_applicable x none. As in T15, the one-case body is all-not_applicable for this combination, so suppression applies (PREREG §7.2.1, v30). The promoted combination is traced not_applicable explicitly — a missing trace raises (PREREG §6.6) — and, being not_applicable on this whole one-case body, its yields, rates, and gate are suppressed (PREREG §7.2.1, v30).

## T17 — multi-case body, promoted not_applicable everywhere: suppressed

Prose basis: PREREG §7.2.1 (v30) — an all-not_applicable combination publishes its counts and suppresses its yields, rates, and gate, naming the reason

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: valid, silence
- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, silence; shuffle@c2: valid, silence
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- labels `t17a`: leaking pairs [('f1', 'c1')]
- labels `t17b`: clean (no leaking pairs)

**Expected state pair:**

- `L3.1|preserving` (`t17a`) → `completed` × `finding`
- `L3.1|preserving` (`t17b`) → `completed` × `observed_silence`
- `L3.1|promoted` (`t17a`) → `not_applicable` × `none`
- `L3.1|promoted` (`t17b`) → `not_applicable` × `none`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 1 | 1 |
| `L3.1\|preserving\|combination_completion_rate` | 2 | 2 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 2 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 1 | 1 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 2 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 1 | 1 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 2 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 1 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 2 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|cohort_sensitivity` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_completion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|combination_incompletion_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|evidence_yield` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_cohort_precision` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|feature_discovery_recall` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|not_applicable_count` | 2 | 2 | 1 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 2 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | — | — | **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1) |
| `L3.1\|promoted\|unsupported_count` | 0 | 2 | 0 |

Gate `L3.1|preserving`: experimental=False (finding gate fired=False, completion gate fired=False; clean N=1, k=0, completed=1)

Gate `L3.1|promoted`: **suppressed** — not_applicable on every scope-eligible case in this body: a yield over a combination that never applied is not a measurement of the tool (PREREG §7.2.1)

> The promoted combination never applied anywhere in this two-case body: its evidence yield would print 0/1 and read as a mode that ran and found nothing, so it is suppressed with the not_applicable count 2/2 as the honest signal.

## T18 — multi-case body, promoted not_applicable on some cases only: no suppression

Prose basis: PREREG §7.2.1 (v30) — suppression is all-or-nothing over the body; a mixed body publishes normally, with not_applicable cases contributing misses per §7.2/§7.4

- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, finding(f1@c1); shuffle@c2: valid, silence
- `L3.1|preserving` — context evaluation, strategies ['shuffle'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: shuffle@c1: valid, silence; shuffle@c2: valid, silence
- `L3.1|promoted` — context evaluation, strategies [], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: (no records)
- `L3.1|promoted` — context evaluation, strategies ['complex'], cohorts ['c1', 'c2'], inputs available, terminal=no
  - records: complex@c1: valid, silence; complex@c2: valid, silence
- labels `t18a`: leaking pairs [('f1', 'c1')]
- labels `t18b`: leaking pairs [('f1', 'c1')]

**Expected state pair:**

- `L3.1|preserving` (`t18a`) → `completed` × `finding`
- `L3.1|preserving` (`t18b`) → `completed` × `observed_silence`
- `L3.1|promoted` (`t18a`) → `not_applicable` × `none`
- `L3.1|promoted` (`t18b`) → `completed` × `observed_silence`

| metric | num | den | value |
|---|---|---|---|
| `L3.1\|preserving\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|preserving\|cohort_sensitivity` | 1 | 2 | 0.5 |
| `L3.1\|preserving\|combination_completion_rate` | 2 | 2 | 1 |
| `L3.1\|preserving\|combination_incompletion_rate` | 0 | 2 | 0 |
| `L3.1\|preserving\|conditional_feature_cohort_recall` | 1 | 2 | 0.5 |
| `L3.1\|preserving\|feature_cohort_precision` | 1 | 1 | 1 |
| `L3.1\|preserving\|feature_discovery_recall` | 1 | 2 | 0.5 |
| `L3.1\|preserving\|not_applicable_count` | 0 | 2 | 0 |
| `L3.1\|preserving\|proof_yield` | 1 | 2 | 0.5 |
| `L3.1\|preserving\|short_circuited_count` | 0 | 2 | 0 |
| `L3.1\|preserving\|unprobed_feature_cohort_rate` | 0 | 2 | 0 |
| `L3.1\|preserving\|unsupported_count` | 0 | 2 | 0 |
| `L3.1\|promoted\|clean_case_finding_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|clean_case_incompletion_rate` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|cohort_sensitivity` | 0 | 1 | 0 |
| `L3.1\|promoted\|combination_completion_rate` | 1 | 1 | 1 |
| `L3.1\|promoted\|combination_incompletion_rate` | 0 | 1 | 0 |
| `L3.1\|promoted\|conditional_feature_cohort_recall` | 0 | 1 | 0 |
| `L3.1\|promoted\|evidence_yield` | 0 | 2 | 0 |
| `L3.1\|promoted\|feature_cohort_precision` | 0 | 0 | None (denominator 0) |
| `L3.1\|promoted\|feature_discovery_recall` | 0 | 2 | 0 |
| `L3.1\|promoted\|not_applicable_count` | 1 | 2 | 0.5 |
| `L3.1\|promoted\|short_circuited_count` | 0 | 2 | 0 |
| `L3.1\|promoted\|unprobed_feature_cohort_rate` | 1 | 2 | 0.5 |
| `L3.1\|promoted\|unsupported_count` | 0 | 2 | 0 |

Gate `L3.1|preserving`: experimental=False (finding gate fired=False, completion gate fired=False; clean N=0, k=0, completed=0)

Gate `L3.1|promoted`: experimental=False (finding gate fired=False, completion gate fired=False; clean N=0, k=0, completed=0)

> The promoted combination applied on t18b, so nothing is suppressed: t18a's labelled pair is an evidence-yield miss from a not_applicable case (scope-eligible per §7.4) and an unprobed pair, while t18b's was probed and missed by silence.

## Assertion scenarios (PREREG §8.3)


### T11 — experimental preserving event + non-experimental promoted event: passes

Prose basis: PREREG §8.3 — the assertion reads unaggregated events and the gate table, never a merged finding's inferred boolean

- gate status: `L3.1|preserving` experimental, `L3.1|promoted` non-experimental
- events: 2; reported findings: 1 (tier PROVEN, per-event gate status retained, no single inferred boolean)
- `assert_no_proven_leakage()` → passes (0 triggering event(s))

> The only PROVEN-licensing event belongs to an experimental combination; the non-experimental event is promoted and does not license PROVEN. A single inferred boolean on the merged finding would get this wrong in either direction.

### T12 — non-experimental preserving event + experimental promoted event: fails

Prose basis: PREREG §8.3

- gate status: `L3.1|preserving` non-experimental, `L3.1|promoted` experimental
- events: 2; reported findings: 1 (tier PROVEN, per-event gate status retained, no single inferred boolean)
- `assert_no_proven_leakage()` → FAILS (1 triggering event(s))

> The preserving event licenses PROVEN and its combination is non-experimental: assert_no_proven_leakage() must fail.
