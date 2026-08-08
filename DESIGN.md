# Design: Data Leakage Auditor

**Companion to `PREREG.md` v30.** The primitive, tier licences, data protocol, metrics, reporting guarantees, and kill criteria are locked there. This file holds architecture, method, and API — including the probe mechanics deliberately kept out of the locked file.

**Revisable**, with three standing constraints:

0. **This file restates no measurement semantics.** `PREREG.md` is the sole normative source for units, states, denominators, gates, and what any published number means (`PREREG.md` §0.2.1). Where this file needs one it cites the section and does not paraphrase it. A restated rule here is a protocol failure, not a redundancy, and CI fails on any measurement formula, state enumeration, or denominator definition appearing in this file.
1. Any parameter capable of changing a detector decision, a tier, execution eligibility, probe location, or strategy compatibility is serialized into `VALIDATED_CONFIG` (`PREREG.md` §6.8).
2. Mechanics here must satisfy the locked requirements of `PREREG.md` §2, §3 (promotion status decides the tier), §6.6 (evaluation runs never short-circuit), §6.10, §6.12, and §7.7. A mechanism violating one of those is a protocol failure, not a design change.

`PREREG.md` freezes at commit, so this file cites it by section number. It does not cite this file by number, only by topic.

**Version:** v26, 2 August 2026. Synced to `PREREG.md` v30. **Net subtraction:** the statistical regime and the fixture branch-selection logic are removed. **No detector implementation exists.** The protocol reducer of `PREREG.md` §6.6.1 is built before the tag and its suite must be green for the tag to proceed; it is protocol tooling, not a detector.

---

## 1. Architecture

```
                        leakaudit.audit(...)
                                │
                    ┌───────────┴───────────┐
                    │   AvailabilityModel   │  ← PREREG §2; gates L3.1, L2a, L3.1b
                    └───────────┬───────────┘
 ┌─────┬─────┬─────┬─────┬──────┴──┬─────┬─────┬─────┬─────┬─────┐
L1.1  L1.2  L1.3  L1.4a L1.4b    L2a   L2b  L3.1 L3.1b L3.2  L3.3
 │     │     │     │     │        │     │     │     │     │     │
 └─────┴─────┴─────┴─────┴───┬────┴─────┴─────┴─────┴─────┴─────┘
                  Aggregator: normalize, dedupe, rank
                                │
                    AuditReport + model info sheet
```

Two rows sit outside the availability gate. L1.2's confirmation needs split membership, not decision timing; **non-temporal L2a needs only the `labels_available_during_feature_construction` boolean and no availability model at all** (`PREREG.md` §2.5, §2.8). The gate in the diagram covers L3.1, temporal L2a, and L3.1b.

### 1.1 Build vs wrap

**Built.** L1.1, L1.4a, L1.4b, L3.1b, L3.2 are tens of lines each. L2a and L3.1 are the technical core.

**Wrapped, optional.** L1.2 and L1.3 wrap static analysis, with the split-specific confirmation of §2.7 built on top. L2b and L3.3 may wrap `deepchecks`, decided at Phase 6.

All wrapped tools are optional extras (`pip install leakaudit[static]`, `leakaudit[deepchecks]`), never hard dependencies. Per `PREREG.md` §6.11 a tool that fits a model may only feed REVIEW rows.

### 1.2 Domain profiles

| Profile | `decision_time` | default `column_roles` | `label_availability` | `ties` |
|---|---|---|---|---|
| `generic` | bar close | `at_timestamp` | **unset** | `available` |
| `futures` | bar open | `at_bar_close` for bar-shaped columns; `at_source_timestamp` for joined columns declaring a source | **unset** | `available` |

Under `generic`, availability reduces to `ts ≤ d`. Under `futures` the current bar is unavailable, which is what makes current-bar inclusion detectable.

**No profile sets `label_availability` or `labels_available_during_feature_construction`** (`PREREG.md` §2.4, §2.5). Profiles also carry L2b rules, intervals to skip (session gaps, holidays, rolls), and expected column roles.

---

## 2. The runtime method

### 2.1 `AvailabilityModel` → `a(j, c)`

| `column_roles` value | `a(j, c)` |
|---|---|
| `at_timestamp` | `ts[j]` |
| `at_bar_close` | `ts[j] + bar_duration(j)` |
| `("at_source_timestamp", col)` | that column's value at row *j* — **not** `ts[j]`, which is what makes a forward-filled exogenous column behave correctly |
| `always` | negative infinity |
| `("explicit", col)` | that column's value at row *j* |
| `availability_fn` | user callable |

`bar_duration(j)` is the declared bar length, or the gap to the next timestamp under `inferred`; **at the final row the last known duration is carried forward**, since there is no successor. The label column always uses `label_availability`, never a generic role.

`_availability_matrix` materializes lazily per column — most columns share one rule, and a dense per-cell matrix is wasteful on wide frames.

### 2.2 The comparator

`PREREG.md` §2.3 locks it:

The comparator and its default are `PREREG.md` §2.3 and are not restated here; this file specifies where the mask is built and cached. Why `available` is the default is §0.3 Claim A, verified at Phase 1 before the detectors exist.

### 2.3 Cohorts and probing

A **decision cohort** is the set of output rows sharing one decision time. For one-row-per-timestamp data with bar-open decisions a cohort is one row; for panel data it is all entities at that instant.

For each selected cohort *d*: run the controls of §4 → build the mask → corrupt masked cells → re-run → compare.

The validity of a change and the scope of a silence are `PREREG.md` §2.6; this file schedules the probes that produce them.

The coverage table reports probed-cohort count and the fraction of rows falling in a probed cohort, because `PREREG.md` §7.2 makes conditional recall depend on it and proof yield does not.

**Mask scope is global across entities.** Per-entity masking would leave one entity's unavailable cells visible to another's features.

Cohort selection is config: evenly spaced across the middle, skipping the leading and trailing exclusion fraction where windows are NaN-padded, skipping profile intervals. Modes `full`, `quick`, `dense_early`, explicit list.

### 2.4 One regime, and per-frame guards

`PREREG.md` §6.10 fixes the comparison regime for v0.1. What follows is where the guard runs, not what it licenses.

**Every execution frame is guarded, not just the original.** Preserving strategies run on the original frame; each promoting strategy runs on a promoted alignment family that may be nondeterministic where the original is not — a complex or float branch reaching different code. Each family carries its own guard.

**A frame that fails its guard yields no finding.** `could_not_run(determinism)` for that frame's strategies. No routing parameter, no fallback module, no mode-specific control comparators.

*(→ `HISTORY.md` H-26)*

### 2.5 Promotion status decides the tier

```
promotion_occurred(strategy, frame) = any column's aligned dtype
                                      differs from its original dtype
```

Tier is resolved by `PREREG.md` §3.1 and is not restated here. This file specifies where `promotion_status` is computed and stored, not what it implies.

**Promotion is per run, not per strategy name.** `shuffle` never promotes. `noise` preserves on floating-point columns and promotes on integer ones. **`nan` preserves on an all-float frame — NaN is a float** — and promotes only where an integer or nullable column must widen. `constant` promotes only where its sentinel exceeds the column's dtype. `complex` always promotes. The static table in §2.9 is a default-selection aid; `promotion_occurred` computed at run time is authoritative.

The aggregator resolves tier last, after all strategies have reported (§7). The resolution rule itself is `PREREG.md` §3.1; this file specifies only that resolution is deferred to the end rather than assigned on first report.

### 2.6 The availability probe (L3.1)

1. Controls (§4), then run the pipeline on aligned clean data → baseline.
2. Compute the unavailable set at *d*: every cell with `a(j,c)` beyond the comparator's threshold.
3. Corrupt those cells; everything else byte-identical.
4. Re-run.
5. Compare per §2.3.

**Assert every call:** the unmasked portion of the perturbed frame is byte-identical to the aligned baseline frame.

**Ordering.** Availability boundaries are timestamp-valued, never row-position-valued. Sort order is validated before baselining, never after — re-sorting after the baseline poisons order-sensitive pipelines. `sort=True` sorts before the baseline and records it.

### 2.7 The label probe (L2a)

Same machinery, mask intersected with the label column, using `a(y_j)` from `label_availability`. **Probes cohorts exactly as L3.1 does**, which is why the cost model gives it a `C × S` term (§5.1).

- **Temporal:** at cohort *d*, corrupt label cells unavailable at *d*. Realized labels stay identical.
- **Non-temporal:** runs only under `labels_available_during_feature_construction=False`. Otherwise `unsupported`.

**Assert every call:** every non-label column, and every *available* label cell, is byte-identical to the aligned baseline. Without this a finding cannot be attributed.

Run as a separate probe from L3.1 — perturb both and attribution is lost.

### 2.8 L1.2's split-specific confirmation

Needs the split, not the availability model.

1. Hold the declared training population byte-identical.
2. Perturb only test observations.
3. Re-run the flagged preprocessing path.
4. Check whether fitted state, or transformed **training** output, changed.
5. Attribute the change to the flagged source location — compare behaviour with that component stubbed where the wrapped analyser reports a location.

Tier and confirmation status are assigned by `PREREG.md` §4.4 and its module obligation in §7.1; this file specifies the intervention, not its status semantics. unavailable (no callable, compatibility failure) → RULE `unavailable`; a change that cannot be attributed → RULE `inconclusive`.

L1.2 has no REVIEW output mode. What its confirmation statuses mean, and which rates or gates they may enter, belong to `prereg-static` under the obligation in `PREREG.md` §7.1 and are not stated here. This file specifies the intervention that produces the status, not its consequences.

The two modes are reported and gated separately (`PREREG.md` §7.1, §10.2 criterion 3), so the implementation keeps their counters apart from the start rather than splitting a pooled counter later.

### 2.9 Corruption strategies

| Strategy | What it does | Promotes? | What it misses |
|---|---|---|---|
| `shuffle` | Permutes masked cells per column | **never** | features whose dependency set lies **entirely** inside the masked region and which are symmetric over that whole set; **probabilistically, the decisive cell itself** |
| `noise` | Large random noise on masked numbers | integer columns only | rank-based or noise-robust features |
| `nan` | Overwrites masked with NaN | **integer and non-nullable columns only — NaN is a float, so an all-float frame is preserving** | pipelines with aggressive row-dropping |
| `constant` | Overwrites masked with a sentinel | only where the sentinel exceeds the column's dtype | pipelines filtering sentinels |
| `complex` | Adds `0+1j` to masked values | **always** | pipelines rejecting or casting away complex dtypes |

*(→ `HISTORY.md` H-27)*

**`complex` is borrowed from `leak-detect` and is the strongest single strategy** — any arithmetic touching a tainted value carries a nonzero imaginary part through means, sums, and products, precisely where `shuffle` goes blind. It also always promotes, so its standalone findings are REVIEW (§2.5). That tension is real and is stated in `PREREG.md` registry 16 rather than resolved.

**`shuffle`'s blind spot is narrower than "permutation-invariant."** A trailing window straddling the availability boundary consumes one masked cell plus unmasked history; permuting the masked region swaps that cell's value and the feature moves — so `shuffle` *does* detect current-bar inclusion in a rolling mean. What it cannot move is a statistic over the *entire* masked region, where the permutation acts within exactly the consumed set. `PREREG.md` §6.2's ledger note states the condition and the correction.

**`shuffle` has a fixed-point failure mode**: a permutation can leave the deciding cell unchanged, so with *m* masked cells the per-cohort miss probability is roughly `1/m`. Partial cohort counts are the expected shape of a true finding.

**Provisional candidate default: `shuffle` (required) then `complex` (optional).** A candidate — the shipped set, order, and required/optional status are chosen on the development corpus and frozen into `VALIDATED_CONFIG`, along with cohort count and spacing, exclusion fraction, refinement policy, shuffle scope, noise scale, sentinel value, complex magnitude, permitted promotion sets, and determinism-guard repetitions.

Marking `complex` optional is deliberate: under §4.1 it is the strategy most likely to fail a control, and `PREREG.md` §7.7 says an optional failure is a diagnostic rather than a coverage state.

**Evaluation runs do not short-circuit at any level.** `PREREG.md` §6.6 requires every configured strategy to execute at every selected eligible cohort on the evaluation corpora, the conformance suite, **and the acceptance fixture gate run** — not merely every combination — because a terminal finding would otherwise stop later cohorts, later strategies, and later compatibility attempts, making cohort sensitivity, the unprobed rate, the compatibility denominator, and the per-strategy failure counts depend on when a finding happened to appear. The harness takes `short_circuit=False`; user-facing audits take the default, where `short_circuited` is the combination state for a preempted row.

**Escalation must not stop on a REVIEW finding while a required preserving strategy is unrun** (`PREREG.md` §7.7). The escalation loop therefore checks tier, not merely presence: a `dtype_promoted` finding is recorded and the loop continues; a PROVEN finding ends `exact` mode. On integer-bearing frames a preserving strategy beyond `shuffle` is worth configuring for exactly this reason.

### 2.10 Reach refinement — a scanned observation

What reach *is*, and when a scan may be labelled `full_scan` rather than `lower_bound`, are `PREREG.md` §8.5. This file specifies how each procedure walks the grid.

**`f(τ) = "change persists under the mask at τ"` is not monotone for an arbitrary user callable**, and v20's binary search assumed it was. Counterexample, deterministic and small: three cells with successive availability times, baseline values (1, 1, 1), a constant corruption to 0, and a feature returning whether the sum lies in {0, 2}. Baseline output is 0. Masking all three gives sum 0 → 1 (changed); two → sum 1 → 0 (unchanged); one → sum 2 → 1 (changed). The sequence is changed, unchanged, changed, so a binary search returns the first cancellation and reports a boundary the feature demonstrably reaches past.

**Default is a full scan** over the candidate availability boundaries present in the data — **including a terminal empty-mask boundary**, so that a change still observed at the last real boundary is distinguishable from a scan that simply ran out of candidates, which matters most under `ties="unavailable"`. Reported as `full_scan`. Binary search remains available as a fast mode and its result is reported as a **lower bound**, never as exact. `PREREG.md` §8.5 locks the reporting consequence.

Both earlier formulations were wrong: v9 searched for the largest τ ≤ *d* where the change persists, which is always *d*; the proposed correction searched for the largest persisting τ ≥ *d*, which is one grid step early and returns zero for a feature reading exactly one unavailable cell — current-bar inclusion, the flagship case.

Expected calibration, to be checked at Phase 1 (`PREREG.md` §0.3 Claim B): a trailing window including the decision bar → **one bar**; a centered window of length *w* → **about *w*/2 plus one bar**.

Refinement returns `(reach, basis)`. **Which procedure runs, and therefore which basis is reported, is decided by `PREREG.md` §8.5 against the frozen cap and `reach_refinement_policy` — not here.** Above the cap the capped subset is not scanned; the lower-bound procedure runs. This file specifies how each procedure walks the grid, not when either is chosen. Opt-in: on for `full`, off for `quick`. **Where refinement did not run, no reach and no fix is printed.**

### 2.11 Prior art

| | `leak-detect` | here |
|---|---|---|
| Basis of the cut | row position | declared per-cell availability |
| Current-bar inclusion | invisible | detectable, reach ≈ one bar |
| Legitimate lagged label | flagged (false positive) | clean |
| Forward-filled exogenous column | wrong clock | `at_source_timestamp` |
| Boundary instant | undefined | explicit `ties` comparator |
| Probe points | one, default midpoint | many cohorts, profile-aware |
| Determinism guard | none | required; licenses the comparison |
| Dtype artifacts | unhandled | aligned, per-column equivalence control, tier consequence |
| Silence claim | whole side of the cut | one cohort, stated |
| Validation | example notebook | acceptance fixture + four unseen generated partitions + a visible conformance regression suite |

The availability basis is the one difference in kind. The rest is hardening.

### 2.12 Why static analysis can't do this

Static analysis cannot tell whether a window at row *t* includes a cell unavailable at *t*'s decision time — that depends on window alignment, on how the result joins to the label, and on decision timing that appears nowhere in the source.

---

## 3. Public API

```python
from leakaudit import audit, AvailabilityModel

model = AvailabilityModel(
    timestamp_col="ts",
    decision_time="bar_open",
    timestamp_semantics="event",
    column_roles={
        "open": "at_bar_close", "high": "at_bar_close",
        "low": "at_bar_close", "close": "at_bar_close",
        "prev_close": "at_timestamp",
        "macro_surprise": ("at_source_timestamp", "macro_release_ts"),
        "contract_id": "always",
    },
    label_col="y",
    label_availability=("timestamp", "60s", "0s"),   # base, horizon, pub delay
    ties="available",
    bar_duration="inferred",
    panel_mask_scope="global",        # locked
    panel_rule_scope="per_entity",    # L3.1b only
    embargo="0s",                     # L3.1b only
)

report = audit(
    pipeline=build_features, data=df,
    timestamp_col="ts", label_col="y",
    availability=model,               # or inherited from profile=
    labels_available_during_feature_construction=None,  # non-temporal only
    train_idx=tr, test_idx=te,
    group_col="entity_id", source_path="pipeline.py",
    profile="futures", detectors="all",
    refine_reach=True, sort=False, seed=0,
)

report.coverage_table()      # per detector-case: state, mode, cohorts probed
report.strategy_table()      # per-strategy diagnostics (PREREG §7.5)
report.conformance_table()   # per-case pass/fail, no aggregate rate
report.info_sheet()
report.assert_no_proven_leakage()
report.assert_no_rule_violations()
report.assert_audit_complete(allow={})
```

**Column precedence.** `timestamp_col` and `label_col` appear on both `AvailabilityModel` and `audit()`. **The model is the single source of truth**; the `audit()` parameters are conveniences that construct a model when none is supplied, and are rejected with an error when they disagree with a supplied one rather than being silently overridden either way.

**Minimum for a runtime finding, per row rather than in general:**

| Row | Minimum |
|---|---|
| L3.1 | `pipeline`, `data`, `timestamp_col`, an `AvailabilityModel` |
| **temporal** L2a | the above plus `label_availability` |
| **non-temporal** L2a | `pipeline`, `data`, a label column, and `labels_available_during_feature_construction=False` — **no timestamp and no availability model** |
| L1.2 confirmation | `pipeline`, `source_path`, and the split — no availability model |

*(→ `HISTORY.md` H-28)* `audit(pipeline, data)` alone runs no runtime detector.

`audit(...)` validates inputs → resolves the availability model → determines scope and execution eligibility per detector **per mode** → runs each in isolation → aggregates → returns report. A crashing detector becomes `could_not_run(crash)` and the audit continues.

---

## 4. The controls and the guard

Four things run before any probe. `PREREG.md` §6.10 locks the first three; §6.8 and §6.9 lock the fourth.

### 4.1 `_check_alignment_equivalence(fn, original, aligned, strategy)` — per column

Run the original baseline and the aligned baseline unperturbed, then compare **column by column**:

```
for each output column c:
    if dtype(original[c]) == dtype(aligned[c]):
        require byte equality
    else:
        require (dtype(original[c]) -> dtype(aligned[c])) in
                strategy.permitted_promotions
        require byte equality after promoting original[c] to aligned dtype
```

Any dtype difference outside the permitted set is divergence → `could_not_run(alignment)` for that strategy.

The per-column form matters because a blanket "promote everything, then compare" refuses a pipeline emitting an internally generated integer column — a bar counter, an arange, a constant — which the aligned run leaves integer while blanket promotion makes it complex. That pipeline is behaviourally identical and must pass. `PREREG.md` §6.5 carries it as a control case, alongside a pipeline that genuinely branches on dtype and must fail.

**What this control does not establish.** It shows the two pipelines agree on the unperturbed baseline. It does not show they agree under perturbation, which is what a finding's conclusion rests on. That gap is why `PREREG.md` §3.2 caps promoting-only findings at REVIEW; no amount of baseline checking closes it.

### 4.2 `_align_dtypes(data, strategy)`

Apply the promotion the strategy will cause to the entire frame, recompute the baseline on the aligned frame, then perturb only masked cells. Both arms see identical dtypes, so a remaining difference is information flow rather than representation.

Every comparison and byte-identity assertion is against the **aligned** baseline. The function also returns `promotion_occurred`, which §2.5 uses to resolve the tier.

### 4.3 Compatibility — validated per execution, not once

There is no standalone `_compat_check`. Every perturbed execution validates shape and index against its frame's baseline before its result is used:

```python
def _probe_once(fn, frame_baseline, perturbed, ...):
    out = fn(perturbed)
    if out.shape != frame_baseline.shape or not out.index.equals(frame_baseline.index):
        return ProbeResult(compatibility_failed=True)
    ...
```

The mask differs by detector (L3.1 perturbs many columns, L2a only the label), by cohort, and by strategy, so a single check cannot stand in for the probes — a pipeline can preserve shape under the check and drop rows on a real probe. A failed probe is recorded as failed **for that strategy**; whether the cohort counts as unprobed for the combination is decided by the reducer in `PREREG.md` §6.11, never here.

The form — a failure fraction with a minimum absolute count, over attempted eligible probes — is locked in `PREREG.md` §6.11; only the values `m` and `q` come from the development corpus.

### 4.4 Identity control

Replace masked cells with an exact copy of themselves, or place the cohort past the end of the data. **On the aligned frame, once per alignment family.** Any delta is measurement artifact: affected columns become `could_not_run(control_artifact)`.

### 4.5 `_baseline(fn, data, seed)` — determinism

Run the pipeline *n* times on unmodified data with a fixed seed and require identical output. **`n` is a config value, not a constant** — two matching runs is thin evidence for a threaded pipeline.

**This guard is the licence for the comparison.** A probe compares baseline against perturbed on one machine in one session, so local reproducibility is all it needs. On failure the frame's strategies are `could_not_run(determinism)` and produce no finding — there is no routing parameter and no fallback (`PREREG.md` §6.10). No environment fingerprint is required for a probe to be valid.

### 4.6 Order — guard first, and once per execution frame

```
for each execution frame F  (original, plus one per promoted alignment family):

    _baseline(F)                      determinism guard, on F itself
        └─ fail: could_not_run(determinism) for F's strategies,
                 no finding from F. No routing parameter, no fallback.
        └─ pass: this run is F's baseline

    if F is a promoted family:
        _check_alignment_equivalence(original baseline, F baseline)
    identity control on F
    probe on F   ── shape/index validated on every perturbed execution
```

**Two ordering facts, both learned the hard way.**

*The guard precedes every comparison-based control*, because it licenses the comparison the alignment control performs. The history of getting this wrong is in `HISTORY.md` (**H-32**).

*The guard covers every frame, not one.* A pipeline deterministic on `int64` can be nondeterministic on the `complex128` branch a promoting strategy forces. With a single original-frame guard that pipeline passes, and the promoted run's difference — caused by nondeterminism, not intervention — is reported as an exact-mode finding. It would be REVIEW by promotion status, so no proof is wrongly issued, but the combination-level rates, completion counts, and any fixture substitution resting on them are wrong.

**Compatibility is no longer a separate step.** Shape and index are validated after every perturbed execution, because the mask differs by detector, cohort, and strategy (`PREREG.md` §6.11). A failure is emitted as a **strategy-level execution record**; whether the cohort counts as unprobed for a combination, and whether the strategy escalates, are derived by the canonical reducer under `PREREG.md` §6.11 and are not decided here.

Remaining placements: alignment before anything comparing against the aligned baseline; equivalence immediately after, since a failure there invalidates that baseline; identity before probing, since it is the artifact check the probes depend on.

---

## 5. Cost

### 5.1 Run-count formula

```
(F x D)              determinism guard, D repetitions on each of F frames
+ A                  alignment equivalence + identity, per alignment family
+ (C_L31 x S)        L3.1 cohorts x strategies
+ (C_L2a x S)        L2a cohorts x strategies
+ R                  reach refinement: K x B when the complete candidate
                     count B is at or below the frozen cap; otherwise the
                     lower-bound procedure's cost. K = affected columns.
```

`F` is the number of distinct execution frames: one original plus one per promoted alignment family. The standalone compatibility term is gone — validation now rides on executions already counted (§4.3).

**Refinement is the dominant term when it runs**, and is off in the quoted default configuration (`PREREG.md` §12). `A` scales with the number of promoted families, so at F=2 it covers the original identity control plus the promoted family's equivalence and identity work.

**This file states no total.** The figure depends on the frozen strategy set — how many distinct promotion targets it contains — and on `F`, which follows from that set; **the CI cost script computes it from `VALIDATED_CONFIG` and the README quotes the script's output.** Earlier versions stated totals wrong three times by hand, and v16 asserted "at least 88" from a formula whose shown terms sum to 86, which is the same error one level of confidence up.

For scale only, and not as a locked figure: at candidate defaults the full audit is in the high eighties and `quick` is in the mid teens. On a pipeline taking two hours per pass that is over a week. **This is the number that decides whether anyone runs the tool**, and it has risen in every version that made the accounting honest.

### 5.2 `quick` mode is first-class

Documented as the CI default, not a degraded option. Its coverage table states probed-cohort count and row coverage, and `assert_audit_complete()` treats a `quick` run as complete — cohort coverage is not detector coverage. Reach refinement is off, so reaches are suppressed rather than guessed.

### 5.3 Auditing a slice

Slicing shifts window warmup, manufacturing artifacts at the head and masking leakage deeper in. **Any slice carries padding of at least the maximum window length before the first probed cohort**, present in the data, excluded from probing, and reported. Where the maximum window is unknown, `audit()` requires `max_window=`; a slice without declared padding is refused, not silently run.

The same slicer produces the CI variant of the acceptance fixture, so the padding rule is exercised by the project's own tests.

---

## 6. Detector interface and findings

```python
class Detector(Protocol):
    id: str
    requires: set[str]
    scope_applies: Callable[[AuditContext], bool]
    def run(self, ctx: AuditContext) -> list[EvidenceEvent]: ...


# Tier, schedule state, and evidence outcome are resolved by the
# canonical reducers. This file does not reimplement them.
from leakaudit.protocol import (
    resolve_tier,              # PREREG §3.1
    resolve_schedule_state,    # PREREG §6.6
    resolve_evidence_outcome,  # PREREG §6.6
)
```

Eleven files, one per detector.

**Two records, per `PREREG.md` §7.2.**

**`EvidenceEvent`** and **`ReportedFinding`** are the scoring and display records. Their keys, their deduplication behaviour, and which metrics may read which are defined by `PREREG.md` §7.2 and are not restated here; this file specifies where they are constructed and stored.

**Shared fields:** `detector_id`, `promotion_status`, `tier` (from `resolve_tier`), `evidence_label` (derived, never set independently), `confirmation_status`, `location`, `is_secondary`, `severity`, `evidence`, `suggested_fix`, `source`, `strategies` (the set that produced it), `corroborated_by` (other events on the same pair), `promotion_occurred`, `max_delta`, `tolerance`, `declared_semantics`, `availability_declaration`, `probe_cohort`, `affected_output_cohort`, `reach`, `reach_basis` (`full_scan` | `lower_bound`).

`probe_cohort` and `affected_output_cohort` are separate fields because they differ whenever a probe surfaces a leak at an earlier row, and `PREREG.md` §7.2 scores on the affected one.

```
[L3.1 · PROVEN] roll_vol_60 reads unavailable data
  Under: decision_time=bar_open, close=at_bar_close, ties=available
    (profile: futures).
  Probe cohort 09:31:00 · affected output cohort 09:31:00.
  Reach 60s (full scan) — one bar. The window includes the decision bar;
    .shift(1) would make it available-only.
  Found in 18 of 20 probed cohorts (20 of 4,812 rows probed).
    Partial cohort counts are expected: shuffle can leave the
    deciding cell fixed.
  Strategy: shuffle (dtype-preserving). Corroborated by: complex.
  Max delta 0.0043 (tolerance 0 — exact equality).
```

```
[L3.1 · REVIEW · dtype_promoted] vwap_dev reads unavailable data
  Seen only under complex, which promoted int64 -> complex128 on
    3 columns. No dtype-preserving run reproduced it.
  The alignment control shows the original and promoted pipelines
    agree on the unperturbed baseline; it does not show they agree
    under perturbation, so this is not stated as proven.
  Probe cohort 09:31:00 · affected output cohort 09:31:00.
```

```
[L1.2 · RULE] StandardScaler fit before split (inconclusive)
  Static match at pipeline.py:44. Perturbing test rows changed
    training output, but the change could not be attributed to
    line 44 — another component also reads unavailable cells.
  Not upgraded to PROVEN.
```

```
[L3.1 · exact mode · could_not_run(determinism)]
  The pipeline produced different output on two identical runs
    (columns: rand_feat). Exact comparison is unavailable, so no
    proof is possible for this pipeline. Seed the pipeline, or
    record an explicit exception.
  Seed the pipeline, or run it single-threaded for the audit, and
    re-run. There is no fallback comparison in v0.1.
```

```
[L3.1 · no findings — 20 of 4,812 rows probed]
  Silence covers the 20 probed cohorts only. Rows outside them
    were not tested. This is not a statement about the pipeline.
```

The last block is the one users will misread if written any other way.

---

## 6a. The fixture harness

`PREREG.md` §6.2's gate no longer selects between branches, so the harness no longer selects one. What remains is the ordinary work, and it is still needed:

- reproduce both reference AUCs, full and sliced, within ±0.010;
- run `fixture_contaminated` and `fixture_corrected` under the reconstructed declaration on the frozen default configuration;
- check attribution against the manifest's column DAG — labelled source, descendant, or clean;
- validate the identity control on both;
- evaluate the four criteria;
- write the per-source record: detected or missed, highest tier reached, promotion status, producing strategies, primary or secondary, affected cohorts, declaration used;
- report the descriptive fixture proof count defined by `PREREG.md` §6.2, serialized as a numerator and a denominator rather than a computed rate.

*(→ `HISTORY.md` H-29)*

---

## 7. Aggregator

Normalizes output from built and wrapped detectors into **EvidenceEvents**, then derives **ReportedFindings** from them (`PREREG.md` §7.2). Deduplication happens *within* a combination — probes, strategies, and repeated runs collapse into one event — and *across* combinations only for display.

**Both records are kept.** Collapsing a promoting event into a PROVEN finding and discarding it would leave the exact-promoted row with nothing to count, which is precisely what v15 did.

**Tier resolution happens here, last**, once every frame and strategy has reported (§2.5): the ReportedFinding takes the highest tier among its events, so a pair found by a preserving run is PROVEN with the promoting event recorded as corroboration.

A merged finding takes the **highest** tier of its components and records all sources — but an L1.2 static match merges with an L3.1 runtime finding only when §2.8 attributed the flow to the flagged component; otherwise both appear separately.

When static and runtime **disagree**, show both and say so. No principled rule picks a winner.

Chained leakage is marked, not resolved: downstream findings in one cohort are marked `is_secondary` and the fix is withheld from all of them. Duplicates from L1.4a/b are canonicalized to equivalence clusters before aggregation.

**This component is the real engineering difficulty of the design**, and the canonical-unit rule plus tier resolution made it harder. Budget for it.

---

## 8. `AuditReport`

**Fields:** `findings`, `coverage` (per detector-case), `schedule_state` and `evidence_outcome` (per `(detector, promotion_status, case)`, `PREREG.md` §6.6), `strategy_diagnostics` (keyed detector × strategy × promotion status), `cohorts_probed`, `rows_covered`, `runtime`, `determinism_check_passed`, `alignment_equivalence_passed`, `identity_control_passed`, `config_name`, `availability_declaration`, `conformance_results`, `recorded_exceptions`.

**Three state layers are stored** — detector-case coverage, the combination pair, and strategy diagnostics. Their values, resolution, and consumers are defined in `PREREG.md` §6.6 and §7.7 and are not restated here; the assertions read the detector-case layer only:

| Detector-case coverage | Strategy diagnostic |
|---|---|
| values defined by `PREREG.md` §7.7 | values defined by `PREREG.md` §7.5 |

**Methods:** `summary()`, `coverage_table()`, `strategy_table()`, `info_sheet()`, `conformance_table()`, `to_json()`, `assert_no_proven_leakage()`, `assert_no_rule_violations()`, `assert_audit_complete(allow=...)`.

Guarantees implemented here are locked in `PREREG.md` §8: the report never says a pipeline is clean; not-run states are never displayed as `passed`; tiers and evidence bases are visually distinct; every L2a and L3.1 finding prints its declaration, mode, and cohorts; reaches appear only when refined; recorded exceptions are printed.

---

## 9. AI workflow and disclosure

**A judge model shares the ceiling of the models it judges**, so quality control lives in protocol — fixtures, assertions, guards, and executable tests — not in another model's opinion.

| Tier | Where | Tasks |
|---|---|---|
| **T0** | Author, no AI | Phase 0 verdict, build/wrap decisions, thresholds, kill decisions, the availability model, every public claim |
| **T1** | Frontier chat | Adversarial review of detector logic, API design, edge cases, prior-art search, editing |
| **T2** | Frontier coding agent | Implementation from spec — **never without a reviewed spec diff** |
| **T3** | Local models | Docstrings, changelog, boilerplate |
| **T4** | Deterministic scripts | Fixture harness, corpus generation, cost and phase arithmetic, test suite, CI. **Validation numbers come from scripts, never from a model.** |

`PREREG.md` is read-only to agents. This file is not, but changes arrive by reviewed diff.

**Hazard specific to this project.** Models trained on the same corpus share its blind spots, and the modal error in that corpus *is* the rolling window that silently includes the current bar. A panel of models will unanimously approve a leaking window. The controls in §4 and the availability model exist because model consensus cannot catch the error this tool is built to catch.

**Review lessons are recorded in `HISTORY.md`** (**H-L1** through **H-L11**). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
