# Pre-Registration: Data Leakage Auditor

**Working name:** TBD (placeholder: `leakaudit`)
**Author:** Theo Johann Howard
**Date:** 30 July 2026
**Status:** v30 — supersedes v1–v29. Committed together with `DESIGN.md` v26 and `HISTORY.md`. **The last version under the self-imposed cap. Everything after this routes through §0.2.1's class A/B/C machinery, which is what it was built for.**
**Shape of this version:** closure patch. The two-axis resolver made total and its legality fixed, denominators made set-consistent, module ownership declared, the ambiguous-fixture criterion moved ahead of tuning, and a reference reducer added so closure is demonstrated rather than asserted.
**Registration:** committed unchanged as `PREREG.md` at first commit, before any detector code is written. See §11.

---

## 0. What this document is for

This file locks the things that, if changed quietly later, would make a past result look better than it was:

1. **What the tool covers** — and what it explicitly cannot do
2. **The primitive** — what "leakage" means here, precisely enough that a number computed against it means something
3. **What licenses each tier** — in particular, what is and is not sufficient for a proof
4. **How each detector is validated** — data, generation protocol, metrics, denominators
5. **What the report is allowed to say, and when to stop**

Changes are allowed. They go in `DEVIATIONS.md`, append-only, with a date and a reason. An unrecorded change is a protocol failure, not a change of plan.

### 0.1 What is locked here and what is not

`DESIGN.md` holds architecture, method, and API and is revisable. The test:

> If changing it would make a past result look better than it was, it is locked here. If changing it is just engineering, it goes in `DESIGN.md`.

Probe mechanics live in `DESIGN.md`, because through v9 they were specified in this file and were wrong three versions running. What is locked here is the requirement, not the mechanism:

| Locked here | Section | Revisable in `DESIGN.md` |
|---|---|---|
| Availability, per cell, is the primitive | §2.2 | how the matrix is built |
| The tie comparator and its default | §2.3 | mask construction |
| A probe's *silence* extends only to its decision cohort | §2.6 | cohort scheduling and selection |
| Runtime tier is determined by promotion status; only a dtype-preserving run is PROVEN | §3.1 | how promotion status is computed |
| Promotion is per run, and promoting-only findings are REVIEW | §3.2 | strategy selection and escalation |
| The canonical scoring unit and its deduplication | §7.2 | how findings are collected |
| What makes a detector-case complete, and tier-aware termination | §7.7 | which strategies are required, subject to §6.7 |
| Undeclared availability → `unsupported`, never pass | §2.7 | how declarations resolve from profiles |
| Conformance is a regression suite and publishes no aggregate rate | §7.8 | how the suite is run |

**Each row names its target section, and the CI script of §6.8 checks that the target contains the row's key phrase.** Three consecutive versions carried a wrong pointer in this table — the one table that declares what is locked — because an existence check cannot catch topic drift after a renumber.

Anything in `DESIGN.md` capable of changing a detector decision, a tier, execution eligibility, probe location, or strategy compatibility is serialized into `VALIDATED_CONFIG` (§6.8). Revisable does not mean unrecorded.

### 0.2 Stopping rule for revision

**v30 is committed unless a further review identifies something that changes what a published number would mean.**

**And the terminal condition is a property, not a count.** Zero findings is unreachable; every full pass has produced several. The active registration is **closed** when: every published number has one canonical definition in this file and no second normative statement anywhere; every execution trace resolves to exactly one `schedule_state` and one `evidence_outcome`, with every emitted pair legal under §6.6's table and the reducer's trace suite green (§6.6.1); every denominator is derivable from those; every gate is executable from them; every deleted symbol has zero inbound normative references; and the remaining open items are only class A mechanical facts, class B parameters under locked procedures, or future phase modules explicitly outside this registration. **At closure the right instrument stops being reading and becomes running.** A closed specification can still be conceptually wrong — the event model may omit something nobody anticipated — and the cost of stopping is that the next defect appears in Phase 1 execution rather than in prose. That is the trade being made deliberately.

The rule has fired twenty-one times. The per-firing enumeration is in `HISTORY.md` (**H-B**).

**Where the defects have been moving.** Each firing lands on the surface the previous round's fix created — the chain is traced and audited in §0.2.1, and it now runs through eleven links. A reviewer's attention lags one round behind the work. **The fresh surfaces in v30 are §6.6's both-statuses ratification and §7.2.1's suppression rule. Every other surface has been exercised by the reducer's trace suite rather than by reading, and **this is the last version under the cap** — further findings route through §0.2.1.** Start there, and read §0.2.1's audited chain first — a diff review does not otherwise have the causal history.

**A diff review is a focus, not a jurisdiction.** *(→ `HISTORY.md` H-01)*

### 0.2.1 Why twenty-one firings, and what may and may not move after the tag

The firings are not random. Each has landed on the surface the previous round's fix created — v9's comparator fix produced v11's accounting holes; v11's fix produced v12's guard failure; v12's fix produced v13's comparator gap; v13's tier work produced v14's orthogonality gap; v14's fix produced v15's trigger gap; v15's ordering fix produced v16's per-frame gap; v16's aggregation fix produced v17's level mismatch. The document closes a hole by adding machinery, and machinery has interfaces.

**The generator, as of v23, is named one level below where v19 found it.** v19 removed a coupling — the fixture gate demanding a reporting tier — and the firings continued in the measurement layer. The layer is the *location*. The generator is **duplicated authority plus collapsed axes**: the same rule stated normatively in two files with no canonical source, and one field asked to answer two independent questions.

Every residue defect of the last four rounds fits one of those two shapes:

| Residue | Shape |
|---|---|
| the parked regime deleted from the rule, retained as a `DESIGN.md` instruction | two copies, drifted |
| reach became a scan while the cost model stayed logarithmic | two copies, drifted |
| `non_proving` inside the operational denominators and excluded from every rate | two statements, one file |
| combination aggregation fixed here while `DESIGN.md` still called a single failed probe an unprobed cohort | two copies, drifted |

**Two structural rules follow, and they are locked.**

> **Single normative source.** `PREREG.md` is the sole normative source for measurement semantics — units, states, denominators, gates, and what any published number means. **`DESIGN.md` may reference a rule by its section but may never restate it.** A restated rule in `DESIGN.md` is a protocol failure, not a redundancy, and the CI script fails on any measurement formula, state enumeration, or denominator definition appearing outside this file.

> **No field answers two questions.** Where a measurement concept has two independent axes, the specification carries two fields. Compressing them into one guarantees that the single field misdescribes at least one axis on some case — which is how the combination state of §6.6 was defective in the version that introduced it.

The v19 coupling excision that preceded this diagnosis — what the clause was, what it generated, and the audited per-firing chain — is recorded in `HISTORY.md` (**H-C**, **H-A**).

Reading does not converge on this. Each full pass has produced two to four findings and each fix generates the text the next pass finds something in. Some of what it finds is settleable only by execution: whether `shuffle` can move a permutation-invariant statistic, whether a pipeline stays deterministic on a promoted frame, whether compatibility varies by mask. Those were argued for a full round because argument was the only instrument available. §0.3's three claims are the precedent — argued at length by multiple reviewers, two of them wrongly, settled in a morning of measurement.

**But "a measurement will settle it" is not a licence to rewrite locked semantics afterwards.** *(→ `HISTORY.md` H-03)*

**Three classes, and only two of them are Phase 1's to resolve.**

| Class | What it is | Phase 1 may | Examples |
|---|---|---|---|
| **A — mechanical branch facts** | A measurement selects between outcomes this document already defines | resolve, and record the fact | does a frame pass its determinism guard; does a strategy promote on this frame; does a probe preserve shape; does a probe preserve output shape on this mask |
| **B — parameters under a locked procedure** | A value chosen where the form, search space, objective, denominator, and freeze point are already fixed | select on the development corpus and freeze | the compatibility fraction and its minimum count; cohort count; strategy order |
| **C — semantic or accounting gaps** | The measurement reveals a needed *new* branch, unit, denominator, coverage state, tier licence, or acceptance criterion | **not resolve under this registration** | anything that changes what a published number means |

**Class C requires an amended registration**, committed and externally timestamped **before the affected detector is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md` entry standing alone. The deviation records what was measured; the amended tag carries the new semantics. Both.

**An amendment inherits §11's integrity chain in full:** signed tag, both file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock. An amendment weaker than the thing it amends is not one.

**A class C change discovered after the affected detector already exists** cannot be made ex ante by any ceremony. It is recorded, the amended registration is committed, and **the affected benchmark is regenerated as a new version under §6.4** — new snapshot version, new beacon draw, new single-use run — with the superseded results published alongside, exactly as §6.4's re-draw rule requires.

**Membership in A or B must be citable, not asserted.** Three conditions, all required:

1. **The assumption is stated in the locked text at commit time** — the document knew it was assuming the thing, and §0.3 or the rule itself names it.
2. **The measurement is scheduled before anything depends on the rule** — Phase 1, before the freezes of §10.0, so no rewrite can flatter a result that does not yet exist.
3. **The rewrite path is pre-authorized and cites the specific §0.3 verification item it falsifies.**

**A post-tag finding that cannot cite a stated assumption is not in class A or B.** It is a specification defect. It gets a loud `DEVIATIONS.md` entry, and if it changes what any published number means, an amended registration under the class C rule.

The structural protection is that nothing is published before the Phase 2 freeze, so the window between the tag and the first result is exactly where this machinery operates and where a correction still costs nothing but honesty.

**One honest note about this section's own reach.** Of v16's four firings, at most one and a half were genuinely settleable only by execution — the trigger defect was a logic error findable by reading, and the scoring-key defect was pure specification. The section that states the rule already overstates its own coverage, which is the reason for the citation requirement rather than a reason to drop the rule.

### 0.3 Three claims this document depends on that have been argued, not verified

Every version through v9 specified probe mechanics on paper, and three consecutive versions got them wrong. The response is not to keep arguing more carefully. It is to mark the load-bearing mechanical claims as unverified, and make verifying them a gate before the detectors that rest on them are built.

**Claim A — the tie comparator's default must be `available`.** With bar-close data and bar-open decisions, bar *i−1* closes at exactly the decision instant of row *i*. Under a `ties="unavailable"` default that cell is masked, so the canonical *clean* feature — a trailing window shifted off the decision bar — would be flagged. §2.3 locks the default on that argument. *(Both reviews of v9 proposed the opposite default. If `fixture_corrected` uses shifted features, the opposite default would fail pass-gate criterion 3 and fire kill criterion 2 against a method that works.)*

**Claim B — reach is a scanned observation, and no dependency threshold is assumed.** Earlier versions searched for a boundary where the change "dies," which assumed the change's persistence is monotone in the boundary. **For an arbitrary callable it is not** (§8.5), so no single dependency-death threshold exists to find. The locked quantity instead: **full refinement scans the frozen candidate grid and reports the latest boundary at which the selected corruption strategy produced an observable change.** That is an observed perturbation extent, not an exact dependency boundary, and Phase 1 verifies the scan's calibration on known shapes rather than the monotonicity of arbitrary pipelines.

**Claim C — permutation strategies are probabilistic at the decisive cell.** A permutation can leave any given cell where it was, so a real leak may go undetected at an individual cohort. Registry entries 14 and 16 rest on this, and it is why §3's dtype-preservation condition is costly rather than free.

**Verification is a Phase 1 gate item** (§10.0), performed before L3.1 and L2a are built, against these cases at minimum:

1. A **mixed frame** — a label column with a declared horizon alongside a joined, forward-filled column whose availability follows its source timestamp. This is where v8 died and is the thinnest part of the specification.
2. A cell whose availability equals the decision instant exactly, under both `ties` settings.
3. A feature reading exactly one unavailable cell, with the expected reach of one bar.
4. A centered window, with the expected reach of about half the window plus one bar.
5. A repeated permutation probe on a known leak, to establish that partial cohort counts occur.
6. **Per-frame determinism** (§6.10) — a pipeline deterministic on an integer frame and nondeterministic on its promoted complex branch must be caught by the promoted family's own guard, not reported as an exact-mode finding.
7. **Mask-dependent compatibility** (§6.10) — a pipeline whose row-dropping depends on which columns are masked must fail compatibility on the probes that trip it and pass on the ones that do not, rather than being decided once per strategy.
8. **The per-column alignment comparator of §6.11** against three pipelines: one with integer-typed outputs, one whose outputs propagate complex dtype, and one emitting an internally generated integer column that never touches a promoted input. All three are behaviourally identical after promotion and **all three must pass.** A fourth pipeline that genuinely branches on integer versus float dtype **must fail.**

Items 6 through 8 are the mechanical facts that §6.2, §6.9, and §6.10 currently assume. Each locked rule names its assumption; if measurement contradicts it, the rule is rewritten through `DEVIATIONS.md` before the detectors that depend on it are built (§10.0).

**If verification contradicts any of these claims, the response depends on §0.2.1's classes, not on convenience.** If the result instantiates a pre-defined class A branch or selects a class B parameter under its locked procedure, record it in `DEVIATIONS.md` and in the frozen configuration. **If it requires a class C change — a new branch, unit, denominator, coverage state, tier licence, or acceptance criterion — record the measurement and commit an amended pre-registration before implementing the affected detector.** §10.0 fixes the order relative to the Phase 1 freezes. *(→ `HISTORY.md` H-04)*

### 0.4 The version ledger lives in `HISTORY.md`

Every reversal, retraction, and firing this document has recorded is in `HISTORY.md`, committed with the pair and hashed in the tag message. It is required reading for a reviewer taking a diff — the causal history is the one instrument a single-diff review does not otherwise have — and it is deliberately absent from the implementer's normative input.

---

## 1. The problem

Data leakage makes ML results look better than they are. Kapoor & Narayanan (2023, *Patterns*) surveyed 20 review papers across 17 fields and found leakage affecting 329 papers. In their civil war case study, every paper claiming complex ML beat logistic regression failed once leakage was fixed — the complex models turned out no better than a decades-old baseline.

Their proposed fix is a **model info sheet**: a form filled in by hand.

### 1.1 What already exists

**Static code analysis.** Yang et al. (2022, ASE) built static analysis for three leakage types and found leakage widespread across 100,000+ public notebooks. Its descendants — LeakageDetector for PyCharm (2025), LeakageDetector 2.0 for VS Code (2025) — improved usability, cover the same three types, and did not independently measure detection accuracy. Drobnjaković et al. (NBLyzer) verify absence of leakage by abstract interpretation. All read source code.

**Data and split checks.** `deepchecks` ships a train-test leakage suite: date overlap, date duplicates, train-test sample mix, index leakage, identifier leakage, single-feature predictive-power screen. Mature, maintained, widely installed.

**Runtime perturbation.** `leak-detect` (Pawar, 2020, MIT, PyPI) treats a feature function as a black box, replaces all rows on one side of a cut point with NaNs or complex numbers, re-runs, reports which output columns changed. Same family as the runtime detectors here, and subject to the v7 defect: it cuts on row position, so it cannot see current-bar inclusion and it false-flags a legitimately lagged label.

### 1.2 The intended contribution

1. **Availability-based runtime probing** — perturbation defined against a declared, per-cell information-availability model rather than row order (§2). The one place this project's method differs from `leak-detect` in kind rather than degree.
2. **Unified execution** — one install, one call, checks spanning the published taxonomy.
3. **Explicit coverage accounting** — every check that did not run appears with a reason, and missing coverage is never converted into a pass.
4. **Model info sheet generation** — pre-filling Kapoor & Narayanan's manual form from real code and real runs.

**Comparative completeness is not claimed here.** Whether this is more complete than existing tooling is what Phase 0 (§10.1) tests.

---

## 2. The primitive: availability

### 2.1 Why row order is the wrong basis

`x.rolling(60).mean()` at row *t* uses rows *t−59…t*, all at or before *t* — and so does `.shift(1)`. A probe defined on row order changes neither and cannot tell them apart. But if the decision for row *t* is made before row *t* completes, the first is leakage. Symmetrically, a feature built from a realized `y.shift(1)` is legitimate, yet corrupting the whole label column changes it.

**Row order is not availability.** The current bar carries timestamp *t* and is not complete at *t*. A realized past label carries an earlier timestamp and is available.

### 2.2 Availability is per cell

Real input frames mix sources with different clocks: bar values available at bar close; prior-state values at bar open; book snapshots at event time; macro values published on their own schedule and then joined and forward-filled, so availability follows the **original release timestamp**, not the destination row's; static metadata always available.

> **`a(j, c)`** — availability time of the cell at row *j*, column *c*.
> **`d(i)`** — decision time for output row *i*.
> Availability is decided by the comparator of §2.3.
> A feature is correct when it depends only on cells available to its own row.

### 2.3 One versioned model — and the comparator

**The comparator, locked:**

| `ties` | cell available to row *i* iff |
|---|---|
| `available` **(default)** | `a(j,c) ≤ d(i)` |
| `unavailable` | `a(j,c) < d(i)` |

**One comparator serves L3.1, L2a, and L3.1b**, and every place that compares an availability time to a decision time states which branch it is using (§4.3).

**The default is `available`, on the argument of §0.3 Claim A**, which Phase 1 verifies before the detectors are built. `unavailable` remains selectable for data where the boundary instant is genuinely unusable, and it is never the default.

**`AvailabilityModel`**, versioned and recorded with every result:

| Element | Purpose | Scope |
|---|---|---|
| `decision_time` | how *d(i)* derives from row *i* — bar open, bar close, offset, or a column | all runtime rows |
| `timestamp_semantics` | whether the timestamp column is observation, event, or availability time, plus the mapping if not the last | all |
| `column_roles` | per-column rule: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column | all |
| `label_availability` | §2.4 | L2a, L3.1b |
| `ties` | the comparator above | all |
| `bar_duration` | fixed value, or inferred from successive timestamps; **at the final row the last known duration is carried forward** | roles using bar close |
| `availability_fn` | escape hatch: user callable returning `a(j, c)` | all |
| `panel_mask_scope` | **global, locked.** Masks are computed across all entities at a decision instant | L3.1, L2a |
| `panel_rule_scope` | per entity (default) or global, for L3.1b's comparison; per-entity results are reported with a global check alongside | L3.1b only |
| `embargo` | additional gap in L3.1b's comparison. **L3.1b only** — it has no meaning in a mask and is never applied to one | L3.1b only |

The last three exist because v9's merge gave one name to two jobs. `panel_mask_scope` is locked global: per-entity masking would leave one entity's unavailable cells visible to another entity's features. `embargo` is scoped explicitly because a field silently applying to masks would change every runtime rate.

Profiles supply defaults (`DESIGN.md`). No profile supplies `label_availability` (§2.4) or the non-temporal policy of §2.5.

### 2.4 Label availability is its own rule, and is never defaulted

> **`a(y_j) = label timestamp + label horizon + publication delay`**

- **All three terms are user-declared, as one `label_availability` declaration.** The publication delay **defaults to zero only when the user supplies the declaration** — it is part of the user's statement, not something a profile fills in. A declaration supplying only base and horizon is complete; a missing declaration is not.
- The label horizon feeds both L2a and L3.1b. It is not a separate L3.1b field.
- **No profile may default any term.** Supplying a label column on a temporal task without a declared label availability makes L2a — and L3.1b — `unsupported`.
- Without it the corpus is unadjudicable: §6.5 contains a lagged label that *is* realized (clean) and one that is *not yet* realized (leaking), and only a declared horizon separates them.

### 2.5 The non-temporal label policy

A task with no timestamp column has no decision timing, so `label_availability` cannot express anything about it. L2a still has a narrow job there (§4.2), and it needs its own declaration:

> **`labels_available_during_feature_construction`** — a required boolean when a label column is supplied on a non-temporal task. It is a declaration in its own right, not a field of `AvailabilityModel`, because there is no time for an availability model to describe.

`false` means the user asserts that no label was legitimately available while features were built, and L2a runs in the narrowed non-temporal mode. `true` — or absent — makes L2a `unsupported`, naming this policy as the missing element. The tool declines to judge legitimate label use rather than guessing at it.

### 2.6 A probe's silence extends only to its cohort

A mask built for decision time *d* corrupts cells unavailable at *d*. For an output row *i* with `d(i) < d`, the set unavailable to *i* is larger. Cells unavailable to *i* but available by *d* are not corrupted, so row *i* can leak silently.

Locked, in both directions:

- **A change at any row with `d(i) ≤ d` is a valid finding.** Those cells were unavailable to *i* as well, under either tie convention.
- **Silence is informative only for the cohort `d(i) = d`.**

Consequences, locked: the scoring unit is **feature × affected output cohort**, deduplicated across probes, strategies, and runs (§7.2); a labelled pair counts as a miss only when no valid probe found it; any reach inference derives from availability-boundary refinement (§8.5).

### 2.7 Undeclared means unsupported, never pass

If the required declaration is neither supplied nor defaulted, **L3.1, L2a, and L3.1b return `unsupported`** (§8.2), naming the missing element. They do not fall back to row order.

**L1.2's confirmation is not on that list.** Its intervention holds the training population fixed and perturbs test rows (§4.4), which depends on declared split membership, not decision timing.

**Non-temporal path.** Absence of a timestamp column — not absence of a declaration — selects it. There L3.1 is `not_applicable` and L2a runs only under the policy of §2.5.

### 2.8 The declaration is an assumption the tool cannot verify

**Every finding is conditional on the declaration it rests on, and the declarations differ by row:**

| Row | Conditional on |
|---|---|
| L3.1, temporal L2a, L3.1b | the declared `AvailabilityModel` |
| **non-temporal L2a** | `labels_available_during_feature_construction = false` — there is no availability model in that path (§2.5) |
| L1.2 PROVEN | the declared train/test split |

A wrong declaration produces wrong findings in **both** directions, whichever declaration it is.

Therefore: every L2a and L3.1 finding prints its declaration and its cohorts (§8.4); the declaration is in `VALIDATED_CONFIG` with every published rate; conformance is measured separately from detection (§7.8); registry entries 12 and 13 record the limitation.

---

## 3. Three tiers, and what licenses each

| Tier | Meaning | What a finding is |
|---|---|---|
| **PROVEN** | Information flow demonstrated at runtime by intervention, compared by **exact equality** under a **passing determinism guard** and a **dtype-preserving run**, under the declared model | a fact about this pipeline, given §2 |
| **RULE** | A deterministic rule over declared inputs. Correct within the declared input model and supported execution subset; a non-finding is not a decision | a fact about the declared inputs |
| **REVIEW** | Everything that falls short of proof, carrying its evidence label | a question |

### 3.1 One runtime regime, two promotion states, two tiers

**v0.1 has a single runtime comparison regime: exact, bitwise equality under a passing determinism guard.** *(→ `HISTORY.md` H-05)*

A runtime finding therefore carries one field, and the tier follows from it:

| `promotion_status` | Tier | Label |
|---|---|---|
| `preserving` | **PROVEN** | — |
| `promoted` | REVIEW | `dtype_promoted` |

`promotion_status` is computed **per strategy per frame** (§3.2). A pipeline that fails its determinism guard on a frame produces no finding from that frame at all: it is `could_not_run(determinism)` (§6.10). There is no fallback in v0.1, and the honest consequence is registry entry 15.

The REVIEW rows that are not runtime detectors — L1.4b, L2b, L3.3 — carry the label **`domain_judgment`** and are scored under §7.9.

### 3.2 Dtype-promoting runs cannot license a proof

The alignment control (§6.11) establishes that the original and aligned pipelines agree **on the unperturbed baseline**. That is a single-point check. It does not establish that they agree **under perturbation**, which is what the probe's conclusion rests on.

The counterexample is concrete: a pipeline that branches on input dtype, whose branches coincide on the baseline values and diverge afterwards. A clip that is a no-op on baseline data is enough. Alignment equivalence passes; after perturbation only the aligned branch runs; a finding appears. Calling that PROVEN would assert something about the user's original pipeline on the strength of a different branch's behaviour.

**Locked:**

- **Promotion is a property of the strategy *and the frame*, computed per run.** A strategy that promotes nothing on a given frame is `preserving` for that run and is treated as such. `shuffle` never promotes; `noise` preserves on floating-point columns; `nan` preserves on an all-float frame, since NaN is itself a float; `constant` preserves when its sentinel fits the column's dtype; `complex` always promotes.
- A finding seen **only** in promoted runs is REVIEW `dtype_promoted` per §3.1.
- A promoting run **may corroborate** a finding already PROVEN by a preserving run, and appears in that finding's evidence.

**The cost is real but narrower than v14 claimed** (registry 16). On an all-float frame, `noise` and `nan` are both preserving and neither is probabilistic, so proofs there do not rest on `shuffle` alone. On an integer-bearing frame the preserving set can collapse to `shuffle`, which is probabilistic at the decisive cell (Claim C). Strong evidence and the strong tier coincide less often than a user would expect, and the report shows both rather than collapsing them.

---

## 4. Coverage map

| ID | Detector | Kind | Method | Needs |
|---|---|---|---|---|
| **L1.1** | Missing or overlapping declared evaluation split | RULE | Indices disjoint and non-empty | split indices |
| **L1.2** | Preprocessing fit on train+test | RULE, **→ PROVEN under §4.4** | Static analysis (wrapped) + split-specific confirmation | source and/or callable + split |
| **L1.3** | Feature selection on train+test | RULE | Static analysis (wrapped) | source |
| **L1.4a** | Exact duplicate rows across split | RULE | Cluster hashing under a declared equality definition | data + split |
| **L1.4b** | Near-duplicate rows across split | REVIEW | Distance-based, threshold-dependent | data + split |
| **L2a** | Features from unavailable label values | PROVEN / REVIEW per §3 | Availability-restricted label perturbation | callable + label column + (temporal: `label_availability`; non-temporal: §2.5 policy) |
| **L2b** | Domain-illegitimate features | REVIEW | Single-feature screen, label-correlation ranking, profile rules | data + label |
| **L3.1** | Features from unavailable cells | PROVEN / REVIEW per §3 | Availability-restricted perturbation | callable + timestamp + §2 |
| **L3.1b** | **Training-label / test-decision overlap** | RULE | §4.3 | split + timestamp + §2 incl. `label_availability` |
| **L3.2** | Non-independence train/test | RULE with group IDs; **unsupported** without | Group/entity overlap across split | split + group col |
| **L3.3** | Sampling bias in test set | REVIEW | Train vs test distribution comparison | data + split |

**Eleven detector rows across the eight published types.**

**L3.1b is renamed.** v13 called it "train/test overlap in availability time," which is broader than what it tests: it compares the latest training *label* availability against the earliest test decision, and says nothing about feature cells, delayed or revised sources, or preprocessing state fit on data unavailable by the test decision. The narrow name matches the rule and the evaluation cases. The general version would require a declared fit-input scope and would usually be `unsupported`; it is in `PARKING_LOT.md`, not here.

### 4.1 Counting, stated precisely so it cannot be inflated later

- **L2a and L3.1 emit at a tier derived from promotion status alone** (§3.1): `preserving` reaches PROVEN, `promoted` is REVIEW `dtype_promoted`. They may also be `unsupported`, fail to run, or be silent.
- **6 RULE** (L1.1, L1.2, L1.3, L1.4a, L3.1b, L3.2-with-groups), of which **L1.2 upgrades to PROVEN only under §4.4**. **3 REVIEW** with basis `domain_judgment` (L1.4b, L2b, L3.3).
- **Declaration requirements, per row:** L3.1 and L3.1b require an `AvailabilityModel`. **Temporal L2a** requires one including `label_availability`; **non-temporal L2a** requires the §2.5 policy and no availability model at all. L1.2 requires neither (§2.7).
- All eight published types are *touched*. "Touched" is not "decided," and the two are not interchangeable in any public writing about this project.
- L1.1 is deliberately narrow: two disjoint non-empty index sets do not establish that a test set was held out, was not reused for model selection, and is not a renamed validation set. Those are REVIEW items on the info sheet.
- L1.2 and L1.3 are RULE by default because a positive static match is mechanically supported while a non-match is not a decision.

### 4.2 L2a: two applicability modes

**Temporal.** At cohort *d*, corrupt only label cells unavailable at *d*. Realized labels stay identical, so a feature reading a realized `y.shift(1)` is clean and one reading an unrealized label is flagged.

**Non-temporal.** Runs only under `labels_available_during_feature_construction = false` (§2.5). Otherwise `unsupported`. Cross-fitted target encoding, supervised transformations, and train-only class statistics are legitimate label use; without the narrowing, PROVEN would mean "depends on a label" rather than "depends on an unavailable label."

**Division of labor with L3.1.** One method pointed at different columns, run as separate probes so findings can be attributed. Where labels are built inside the pipeline, L2a returns `unsupported` naming **L3.1 as covering detector**. **Residual case, uncovered:** a label built internally from a past-window statistic also used as a feature. Registry entry 5.

### 4.3 L3.1b's rule, written as inequalities

Let **A** = latest training label-availability time, **E** = `embargo`, **D** = earliest test decision time:

| `ties` | violation iff |
|---|---|
| `available` | `A + E > D` |
| `unavailable` | `A + E ≥ D` |

Under `available` the boundary instant is usable, so exact coincidence is not a violation; under `unavailable` it is. The CI check of §6.7 verifies these inequalities against the shipped implementation.

`panel_rule_scope` governs whether the comparison is per entity or global. Any element undeclared → `unsupported`, not a pass.

### 4.4 L1.2's confirmation is split-specific

1. Hold the declared training population byte-identical.
2. Perturb only test observations.
3. Re-run the flagged preprocessing path.
4. Confirm that fitted state, or transformed **training** output, changes.
5. Attribute the change to the flagged source location.

A full-series scaler is confirmed because perturbing test rows changes the state applied to training rows. An unrelated future-looking feature elsewhere must not upgrade a scaler warning. Where attribution fails, the finding stays RULE with confirmation status `inconclusive`.

**The §3 proof licence applies to L1.2's confirmation without exception.** *(→ `HISTORY.md` H-06)*

> L1.2 upgrades to PROVEN **only when the split-specific confirmation is deterministic, exact, and dtype-preserving.** Where an attributable change is observed **only under a promoting run**, the static finding **remains RULE** and records the confirmation as **`non_proving`**, with its promotion status printed. It does not become a standalone REVIEW finding; L1.2 has no REVIEW output mode, and inventing one would need its own metrics and its own gate.

**L1.2's two epistemic modes are scored and gated separately** (§7.1, §10.2 criterion 3).

**This table is the scope. It closes.** New types go in `PARKING_LOT.md`, reviewed Sundays only. At first commit it contains only the §13.9 entry (§11 item 1).

---

## 5. Limitations

### 5.1 Fixable with engineering (and will be)

Slow runtime (parallelize, `quick` mode, padded slicing); missed session gaps (profile intervals); single-strategy blind spots (multiple strategies); dtype artifacts (alignment, per-column equivalence, compatibility); coverage misread as pass (§8); wrapped-tool fragility (optional extras); bus factor (tests and docs).

### 5.2 Partly fixable

- **Needs a callable.** A decorator lets people mark existing code instead of rewriting.
- **Needs a per-column availability declaration, including a label horizon no profile will guess.**
- **Random pipelines get nothing from the runtime rows** (§6.10, registry 15). The mitigation is user-side and the report states it: seed the pipeline, or run it single-threaded for the audit. Not fixable inside the tool without the parked fallback (§13.9).
- **Only sees what you pass in.** Leakage during collection or joining is invisible.
- **Static vs runtime disagreement.** Show both. Honest, not solved.
- **Chained leakage.** Marked, not resolved (§7.6, §8.5).
- **Adoption.** Easy install, real numbers, good posts. Improves odds only.

### 5.3 Blind-spot registry — structural, not fixable

**Additions are dated, whether or not convenient.**

1. **Three rows need human judgment.** L1.4b, L2b, L3.3 are REVIEW by design. Kapoor & Narayanan's own example — a hypertension model using anti-hypertensive prescriptions as an input — is undetectable from data alone.
2. **L2a catches direct label flow only.** A feature built from an upstream *proxy* of the label is invisible.
3. **Absence cannot be proven, and coverage is per cohort.** A pair found by no valid probe is missed, so "none found" reports on what was checked.
4. **Cells sharing an availability time are unordered.** In order-book data this is a real channel.
5. **Internally-built labels from past windows.** §4.2. Falls between L2a and L3.1.
6. **RULE rows cannot certify absence.** A static non-match, duplicate non-match, or temporal non-overlap is evidence under the declared input model, not a decision.
7. **The evaluation corpus is unseen, not blind.** Synthetic cases advertise their own construction, and the author wrote the generator.
8. **Hand-authored cases and REVIEW adjudication are author-produced.** §6.6, §7.9. Their numbers are labelled non-holdout throughout.
9. **The corpus contains only leakage the author thought of.** The families in §6.5 are the limit of what the rates describe.
10. **Leakage is not the only way to be wrong.** Test-set reuse, bad metrics, small samples, regime change: all invisible.
11. **The taxonomy may be incomplete.** The authors call their survey a lower bound.
12. **Every L2a and L3.1 finding is conditional on a declaration the tool cannot verify.** *(29 Jul 2026)* A wrong model produces wrong findings in both directions.
13. **The tie comparator changes findings at the boundary instant.** *(29 Jul 2026)* The same pipeline is clean under one convention and leaking under the other.
14. **Permutation strategies are probabilistic at the decisive cell.** *(29 Jul 2026)* Claim C. Multi-cohort and multi-strategy agreement is the mitigation.
<!-- banned-exempt: id=REG15 reason="the registry entry must name the parked mechanism to state what a user does not get" -->
15. **A pipeline that cannot be made deterministic gets nothing from the runtime rows.** *(30 Jul, widened 31 Jul, priced 1 Aug)* §3.1, §6.10. v0.1 has no fallback: a frame failing its guard produces `could_not_run(determinism)` and no finding of any tier. Earlier versions promised such users REVIEW findings from a noise-floor mode; that mode is parked (§13.9), so the promise is withdrawn rather than left standing unbuilt. **The affected population is not an edge case:** threaded gradient boosting, GPU training, and any unseeded stochastic step are ordinary in financial ML, so a large share of the pipelines this tool exists for will hit this on first contact. §12 prices it and §8.4 requires the report to carry the remedy.
16. **On integer-bearing frames, proofs rest on the probabilistic strategy.** *(30 Jul 2026, scoped 30 Jul)* §3.2. `complex` always promotes, so its standalone findings are REVIEW. On an **all-float** frame `noise` and `nan` both preserve and neither is probabilistic, so proofs there are well supported. On a frame containing integer columns the preserving set can collapse to `shuffle` alone, and `shuffle` can miss the decisive cell. The strength of a proof therefore depends on the user's dtypes, which is not something they would expect, so the report states the promotion status of every run.

### 5.4 The claims that survive

**v0.1 (Phase 3 release):**
> Audits a user-supplied pipeline for dependence on cells not available at the declared decision time, reports every check that did not run and why, states which decision cohorts were probed, and never converts missing coverage into a pass.

**v1.0 target:**
> One orchestration call runs every supported check for which the required inputs and declarations were supplied, spanning all eight published leakage categories — two demonstrated at runtime under a declared per-cell availability model, six rule-based within a declared input model, three surfaced for review — and pre-fills the model info sheet with unresolved fields explicitly marked.

**Never:** "catches 95% of data leakage." "The first tool to detect leakage at runtime." "The most complete leakage tooling that exists." "Auto-fills the model info sheet" without the unresolved-fields qualifier. "Blinded evaluation." Any runtime claim without its availability declaration. Any coverage claim implying whole-pipeline rather than per-cohort silence. Any conformance percentage (§7.8). Any suggestion that a nondeterministic pipeline receives graded evidence (§6.10). Any PROVEN claim resting on a promoting-only run (§3.2).

---

## 6. Data, generation, and configuration

### 6.1 Five bodies of data

| Body | Job | Defaults chosen on it? | Detection rates published from it? |
|---|---|---|---|
| **Acceptance fixture** (CME) | Pass/fail gate on the runtime detectors | No | **No** |
| **Development corpus** | Choose strategies, escalation order, cohort count, thresholds, safety factor | Yes | No |
| **Evaluation corpora** (four partitions, §6.3) | Published detection numbers | **No** | Yes, once each |
| **Conformance regression suite** (§7.8) | Does the tool obey the declaration it was given? | No | **No — per-case results only, no rate** |
| **Wild corpus** | Discover failure modes | No | No |

The fixture's AUC figures are provenance — they describe the pipeline it was built from, not the tool's accuracy. **No accuracy or generalization rate is published from the fixture.** The descriptive proof count of §6.2 is the sole reported fixture outcome; it is a count, receives no inferential interval, and is not a rate.

### 6.2 Acceptance fixture

- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.
- **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.
- **The availability declaration is reconstructed, not chosen** — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon, and intended live execution protocol, with **evidence for each element recorded before any detector tuning.**
- **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).
- **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.
- **Contamination availability class** recorded in the manifest.
- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**Pass gate — discrimination, not tier.**

*(Through v18 criterion 1 required a finding **at PROVEN tier**. That coupled acceptance to reporting: the gate asks whether the method separates two datasets whose answer is already known, while tier answers what a user may claim about their own pipeline. The coupling generated eight firings' worth of machinery — §0.2.1 — and all of it is now deleted.)*

Evaluated on the **frozen default configuration**, under the reconstructed declaration:

1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.
2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.
3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.
4. Silent under the identity control on both.

Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

*(v19 wrote criteria 2 and 3 as "no **primary** runtime finding," which let the tool's own primary/secondary classification exempt its own false positives: a finding on a clean column, or on the corrected fixture, passed the gate if the aggregator labelled it secondary. A classifier the tool controls cannot be allowed to decide what counts against it.)*

Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**What this gate does and does not guarantee, said plainly.** It gates **discrimination**. It does **not** guarantee that the tool can prove leakage on real-world data — the previous gate did guarantee that, and this one deliberately does not. Proof capability is reported instead of required: the manifest records, per independent leaking source, whether it was detected, the highest tier reached, promotion status, the strategies that produced the finding, primary or secondary, affected cohorts, and the declaration used. From that the harness reports a **descriptive fixture proof count**, and deliberately not a rate:

> **k of N** labelled leaking sources received at least one primary PROVEN finding **attributed to that source**.

The attribution clause matters: without it a PROVEN finding on a *descendant* could be read as its source "reaching PROVEN," and a missed source would count as proven.

**It is published as a count, never as a decimal or percentage**, and it is identified as a descriptive fixture outcome rather than a performance rate. *(→ `HISTORY.md` H-07)*

**This is a rebalance, not a tightening.** The two gates are incomparable: a fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old and passes the new; a fixture detected at PROVEN throughout but with one REVIEW finding on a clean source passes the old and fails the new. The trade is deliberate — drop the irrelevant requirement that acceptance detections be proofs, add the relevant requirement that nothing shipped appears on clean or corrected material.

**Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

### 6.3 Four evaluation partitions

| Partition | Detectors | Generated and unsealed after |
|---|---|---|
| `evaluation_runtime` | L2a, L3.1 | Phase 2 configuration freeze |
| `evaluation_split` | L1.1, L1.4a, L1.4b, L3.1b, L3.2 | Phase 4 configuration freeze |
| `evaluation_static` | L1.2, L1.3 | Phase 5 configuration freeze |
| `evaluation_review` | L2b, L3.3 | Phase 6 configuration freeze |

`VALIDATED_CONFIG` carries `[validated.runtime]`, `[validated.split]`, `[validated.static]`, `[validated.review]`.

### 6.4 Generation protocol

Three properties, kept separate: **tamper-evident** (committed hash), **unseen** (author has not inspected or executed the cases), and **label-blind** — **not achievable here and not claimed.**

1. **Freeze the evaluation generator in Phase 1** — code *and* parameter distributions — as an immutable snapshot with its own version and hash, **after Claims A–C are resolved** (§10.0). Any change is a deviation and creates a new benchmark version.
2. Freeze the detector configuration for the partition and sign the tag.
3. **Seeds come from the first pulse of the declared public randomness beacon published after that tag's timestamp**, with per-case seeds from a committed hash function. Source, pulse-selection rule, and derivation fixed before the value exists.
4. Generate immediately; hash the generated data files and the label file.
5. Run once, without modifying the detector.
6. Record beacon pulse, snapshot version, manifest hashes, date.

**Re-draws.** Any discarded draw is a `DEVIATIONS.md` entry, and **the discarded draw's results are published alongside the replacement's.**

**The conformance suite** is generated from the same frozen snapshot at Phase 1, after Claims A–C resolve, and hashed then. It is deliberately **visible during implementation** — see §7.8.

### 6.5 Case families (locked enumeration)

**Availability (L3.1):** trailing windows with and without `.shift(1)`, under both `at_timestamp` and `at_bar_close` roles; **tie-boundary cases under both `ties` settings**; centered windows; resample label/closed variants; forward- and back-fill across boundaries; expanding windows; full-series scaler fit; **a joined-and-forward-filled exogenous column whose availability follows its source timestamp**; cells sharing an availability time (known false negative, registry 4); **a leaking pair reachable only from a later probe cohort**; **a leaking pair reachable from no probe at all** (known miss, registry 3); **a reach case per shape** — current-bar inclusion (one bar) and centered window (about half the window plus one bar); **and a non-monotone reach case** built to §8.5's three-cell shape, whose observable change reappears as the mask shrinks, on which a binary search must be shown to return the earlier boundary and the full scan the later one.

**Label availability (L2a):** contemporaneous label; lagged label **realized** at decision time (clean); lagged label **not yet realized** (leaking); **tie-boundary label realizing exactly at the decision instant**; **a label with a non-zero publication delay**; label proxy (known false negative, registry 2); label built internally from a past window and reused as a feature (registry 5); **non-temporal cases under both settings of §2.5's policy.**

**Tier and mode:**
- **A stochastic pipeline with a genuine leak** — must produce `could_not_run(determinism)` on the affected frame and no finding at all (§6.10). v0.1 has no fallback.
- **An all-float frame where at least one configured strategy is preserving and detects the leak** — must reach PROVEN. *(→ `HISTORY.md` H-08)*
- **An integer-containing frame where only a promoting strategy fires** — must produce **REVIEW `dtype_promoted`, never PROVEN** (§3.2).
- **A leak found by both a preserving and a promoting strategy** — must be PROVEN with the promoting run recorded as corroboration, **regardless of which ran first** (§7.7).
- **A leak detectable only by a promoting strategy** — must produce `dtype_promoted` REVIEW and no PROVEN finding, and must still satisfy §6.2's criterion 1 if it were a fixture source.

**Split rows:** overlapping indices; empty test set; exact duplicate clusters at varying sizes; near-duplicates at varying distances; availability-time overlap with and without embargo; **exact coincidence of `A + E` and `D`, adjudicated oppositely under the two `ties` branches**; label horizon extending past the last training timestamp; entity overlap with and without group IDs; undeclared elements (must return `unsupported`).

**Static rows (L1.2, L1.3):** full-series scaler fit; per-split scaler fit (clean); a leaking future feature *elsewhere* in a correctly-split pipeline — **must not upgrade the scaler finding**; a confirmable non-temporal preprocessing leak with no availability model — **must still upgrade**; **a case where static precision is poor and confirmation precision is good, and its converse.**

**Alignment-control cases** (all four behaviourally identical after promotion except the last):
- integer-typed outputs — **must pass**;
- outputs propagating complex dtype — **must pass**;
- **an internally generated integer column that never touches a promoted input — must pass** (§6.10);
- a pipeline genuinely branching on integer versus float dtype — **must fail.**

**Clean-but-tricky controls, in every clean set:** legitimately random features, NaN-padded features, exogenous data on a different clock, integer columns that promote under NaN perturbation, pipelines with internal row-dropping, panel data with multiple entities per timestamp.

**Cases encoding known false negatives are included deliberately and scored as failures.**

### 6.6 Evaluation runs execute every combination, regardless of terminal findings

§7.1 publishes and §10.2 gates the two runtime combinations independently, while §7.7's tier-aware termination stops a detector-case on a PROVEN finding — so the promoted strategies may never run. If promoted strategies execute *only* where preserving ones found nothing, that combination is evaluated disproportionately on the hard and the negative cases, and its published rate is biased by another combination's result.

> **On the evaluation corpora, the conformance suite, and the acceptance fixture gate run, every configured strategy executes at every selected eligible cohort, regardless of any finding. No terminal short-circuit applies at any level.** A user-facing audit may short-circuit as §7.7 describes, for cost control, with the fact disclosed in its coverage table.

*(→ `HISTORY.md` H-09)*

*(v20 said "termination is per combination, not across them," which left termination live *within* a combination and so left evaluation denominators outcome-dependent after all: a preserving finding could still stop later cohorts, later preserving strategies, and later compatibility attempts, moving cohort sensitivity, the unprobed rate, the compatibility denominator, and per-strategy failure counts. It also made the claim below false, since failures after a terminal finding could still arise. `DESIGN.md` already carried the stricter rule; the two now agree.)*

**Combinations need their own state, and v20 announced one without defining it.**

*(→ `HISTORY.md` H-30)*

> **Two fields, keyed `(detector, promotion_status, case)`, because schedule and evidence are independent axes:**
>
> | Field | Values |
> |---|---|
> | **`schedule_state`** | `not_applicable`, `unsupported`, `completed`, `incomplete(reason)`, `short_circuited` |
> | **`evidence_outcome`** | `finding`, `observed_silence`, `none` |
>
> A case can be `incomplete(compatibility)` **and** `finding` at once — a strategy produced a valid finding at one cohort and the schedule then failed at a later one. v22 asked a single `completed`/`could_not_run` field to carry both, so it had to misdescribe one of them: calling it completed made completion depend on the observed outcome, and calling it could-not-run excluded a valid finding from the denominators §6.11 says prior EvidenceEvents belong in.
>
> **`schedule_state = completed`** requires that the frozen evaluation schedule ran — every configured strategy at every selected eligible cohort — not that some strategy reached a terminal result.
>
> **Every published preserving or promoted metric reads this state**, never the detector-case state of §7.7, which remains the unit `assert_audit_complete()` operates on. Both are stored.
>
> **"Every combination" means both promotion statuses, always.** §3.1's axis is closed and two-valued, so a case has exactly two combinations regardless of which strategies the frozen configuration happens to resolve on it. A combination on which nothing resolves is traced `not_applicable`, explicitly. **Enforcement may not depend on the configuration or on what happened** — the loose reading, where only combinations with at least one trace are checked, makes omitting a whole row silent while omitting one strategy raises, which is outcome-dependent enforcement of a rule against outcome-dependence.
>
> **Every labelled case carries an explicit trace for every combination.** A combination with no trace has no state, and silently skipping it drops the case from that combination's denominators — which inflates its yields and shrinks §10.2's *N*. The build demonstrated a gate verdict flipping on trace omission alone. **A missing trace is a protocol violation and must raise, never default.** This is the "absence carries meaning" failure the trace schema exists to prevent, and it is stated here rather than left implied.
>
> **Execution eligibility, per combination:** a combination is execution-eligible for a case when **at least one configured strategy resolves to that promotion status on that case** and has all required inputs. This is per case rather than per configuration because `noise`, `nan`, and `constant` preserve on some frames and promote on others (§3.2).
>
> **`schedule_state` resolution order**, evaluated independently of §7.7's user-facing required/optional policy — that policy governs the detector-case, not the combination:
>
> 1. `not_applicable` — no configured strategy resolves to this promotion status on this case, **or no eligible cohort was selected for it**. The second clause covers a combination with resolved strategies, available inputs, and nothing to do; without it that trace has no legal state, since vacuous `completed` with no valid execution would have to pair with `none`, which the table forbids. *(Found by the reducer, which raised rather than guessing.)*
> 2. `unsupported` — strategies resolve to the status, but required inputs or declarations are unavailable.
> 3. `short_circuited` — user-facing runs only; see below.
> 4. `completed` — every configured strategy of this combination executed validly at every selected eligible cohort.
> 5. `incomplete(reason)` — execution-eligible, and the schedule did not complete. **Reason precedence when strategies fail differently:** `determinism`, then `alignment`, then `compatibility`, then `control_artifact`, then `crash`.
>
> **`evidence_outcome` is resolved independently, and totally:**
>
> | Value | Condition |
> |---|---|
> | `finding` | at least one valid execution produced one |
> | `observed_silence` | at least one valid execution occurred and none produced a finding |
> | `none` | no valid execution occurred |
>
> **It says nothing about the schedule.** *(v23 defined the middle value as "the schedule ran validly and produced none," which left a real trace with no outcome at all: valid executions, no finding, then a later compatibility failure — not `finding`, not `silence` under that definition, not `none`. A non-total resolver violates this file's own terminal condition, in the section that introduced the condition.)* The name carries the restriction: `observed_silence` covers the executions actually performed, never the schedule.
>
> **Legal pairs, and the CI script fails on any emitted pair outside this table:**
>
> | `schedule_state` | `finding` | `observed_silence` | `none` |
> |---|---|---|---|
> | `not_applicable` | — | — | ✓ |
> | `unsupported` | — | — | ✓ |
> | `short_circuited` | ✓ | ✓ | ✓ |
> | `completed` | ✓ | ✓ | — |
> | `incomplete(reason)` | ✓ | ✓ | ✓ |
>
> Ten of fifteen. Completion implies valid execution, so `completed × none` cannot arise; the two no-execution states admit only `none`; `incomplete` and `short_circuited` admit all three, since a schedule can be cut short before, after, or instead of producing evidence. **Without this table a denominator over the product space is not derivable**, and two implementers computing over different assumed domains publish different completion, failure, and yield numbers.
>
> The optional/required distinction does **not** reach either resolver. A combination containing only an optional strategy whose frame failed its guard is `schedule_state = incomplete(determinism)`, `evidence_outcome = none`.
>
> **`short_circuited`** covers a combination whose remaining schedule was intentionally not run because a user-facing terminal decision stopped it — **whether the terminal finding came from this combination or another one.** It is excluded from every metric denominator (§7.7).
>
> *(v24 called this `superseded`, scoped it to preemption by *another* combination, and permitted only `× none`. Both halves were wrong, and in the same way. A preserving strategy that produces PROVEN early stops the rest of its own combination's schedule — not completed, not superseded, and not a failure, so that trace had no state at all. And a promoted strategy that produced REVIEW evidence before being preempted is `short_circuited × finding`, which the table forbade: being cut short says nothing about whether evidence was already observed. Forbidding the pair recompressed the two axes this section exists to separate — the third time in three rounds that rule was violated by text written to implement it.)*
>
> The reason a combination is excluded from denominators when cut short is unchanged: otherwise a case where the preserving row succeeds quickly would drag the promoted row's completion rate down and the 60% floor would mark the promoted combination experimental *because the tool worked well.*

**`short_circuited` cannot arise in an evaluation run**, because evaluation runs do not short-circuit. It exists for the user-facing coverage table, where the state must still be defined and no published number depends on it.

And §6.11's compatibility denominator *n* is well defined, because "how failures after a terminal finding are handled" does not arise in an evaluation run — which matters, since §0.2.1 class B requires that denominator locked before the tag.

### 6.6.1 Closure is demonstrated by the reducer, not asserted by the prose

§0.2's terminal condition requires that every trace resolve to exactly one pair and every denominator derive from it. **A prose scanner cannot establish that** — the non-total `evidence_outcome` above is the proof, since it read as complete and was not.

`protocol/runtime_reference.py` ships in the tag as protocol tooling, not detector implementation. **It exists and its suite is green; the tag remains blocked on that staying true.** `tests/registration/` enumerates the small traces exhaustively: zero valid executions; valid silence then failure; valid finding then failure; two strategies where one fails and one succeeds; a promoted finding before any preserving execution; a completed clean case with a finding; an incomplete clean case with a finding; a combination's own terminal finding with remaining work unrun; REVIEW evidence followed by another combination's terminal finding; and valid silence followed by another combination's terminal finding.

**Mechanical invariants the suite asserts:** exactly one `schedule_state` and one `evidence_outcome` per trace; every emitted pair legal under §6.6's table; every conditional numerator a subset of its denominator; every rate in [0, 1]; every gate deterministic; **no runtime metric accessing the detector-case state**; **candidate count above the cap implying `reach_basis = lower_bound`, and at or below the cap with every boundary scanned permitting `full_scan`**; **every case-level metric including no-event cases**, since a clean case that produced nothing must still sit in its own denominator; and **the two experimental-status cases of §8.3** — an experimental preserving event with a non-experimental promoted event on the same pair must **not** trip `assert_no_proven_leakage()`, and the inverse must trip it.

**The suite's expected outputs are derived by the author from this prose, so a misreading can be encoded in both.** The reducer proves internal consistency and totality; it cannot prove that either matches what was meant. The expected-output table is small and finite and is the **first** item in the human read, ahead of the blast radius — mechanical closure narrows what human eyes must check, and does not remove them.

**A runtime metric is published only if the reference reducer computes it.** A number named here but absent from the reducer does not exist and may not appear in the README, a post, or an application. *(The name-without-definition class has fired in three separate rounds — §7.1 naming metrics §7.2.1 had to supply, §7.4 publishing a second failure rate, §7.1's stale four-row sentence. This converts the whole class into a build error, and it is what makes the suite's "no runtime metric accesses detector-case state" assertion checkable at all: the assertion ranges over the metrics the reducer knows about.)*

**This file stays normative and the reducer is checked against it.** The reducer's requirement IDs are diffed against these sections in CI. Neither is hand-maintained against the other in both directions — a second normative source is the defect this version exists to remove, and a reference implementation is only safe while it is downstream.

### 6.7 Corpus size, power, and hand-authored timing

- **Script-generable rows: 25 leaking and 25 clean per corpus per row.**
- **Hand-authored rows: at least 10 and 10**, with the smaller *n* stated at every mention.
- **Hand-authored cases are written, frozen, and hashed before implementation of the detector they test**, and are labelled **non-holdout author-created results** wherever they appear. Writing them after seeing detector behaviour is a protocol failure.
- Intervals per §7.10.

### 6.8 Configuration completeness — the general rule

> **Every parameter capable of changing a detector decision, a tier assignment, execution eligibility, probe location, or strategy compatibility is serialized into, and hashed with, the applicable `VALIDATED_CONFIG` section.**

Non-exhaustively: cohort count, selection and spacing mode, exclusion fraction; reach-refinement policy and candidate grid; profile interval exclusions; strategy set, escalation order, **and each strategy's required-or-optional status (§7.7)**; **the terminal-decision policy (§7.7)**; whether probing stops at first finding; shuffle scope; noise distribution and scale; sentinel value; complex magnitude; **each strategy's permitted promotion set (§6.10)**; determinism-guard repetition count per frame; internal perturbation seeds; compatibility- and equivalence-failure behaviour; **and the complete `AvailabilityModel` of §2.3, including `ties`.**

**Subtractive rounds get a banned-vocabulary check.** When a version deletes a mechanism, its distinctive terms are added to a banned list, and the CI script fails if any appears outside §0.4, the `DESIGN.md` lessons, or `PARKING_LOT.md`. *(Run against v19 this would have caught all five residue items mechanically — the configuration list still serializing routing and noise-floor parameters, the lock-table axes row, §4.1's "other three," §5.2's promise, and the Phase 1 capability clause. A reviewer's sweep has a measured reliability; a grep does not have moods. Deleting a mechanism means removing every clause that could still instruct an implementer to build it, which is the class of clause a description-oriented read misses.)* <!-- banned-list: exempt-from-scan -->
Current banned terms: `capability matrix`, `noise floor`, `routing policy`, `comparison_mode`, `statistical mode`, `substituted gate`.
<!-- /banned-list -->

**Two normative spans are declared exempt, with their reason.** The blind-spot registry entry for a parked mechanism (§5.3 entry 15) and the `PARKING_LOT.md` pointer (§13.9) **must name what was parked** — the first to state what a user does not get, the second to say what an amendment would restore. Renaming the mechanism to satisfy the scan would make both less useful and neither more honest. They are marked in place, and the exemption is grounded in those clauses' function rather than in making the file pass.

**The check scans normative regions by explicit range, not by excluding prose that looks historical.** Each file marks its historical sections — §0.4 and the parenthetical ledger notes here, the numbered lessons in `DESIGN.md` — and everything else is normative and scanned. *(A blanket exemption for explanatory-sounding text would not have caught `DESIGN.md` §4.5, which read as an explanation of the determinism guard and was in fact an instruction to rebuild the deleted branch.)*

**The script also enforces the single-source rule and certifies deletions.** It fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md`; and a deletion is not complete until the symbol's inbound normative reference set is empty, with the CI artifact recording the removed symbols, the removed requirement IDs, zero remaining references, and negative tests showing the old configuration is rejected. The banned-vocabulary scan is a smoke alarm behind that, not the proof.

**The checker runs in stages, and a deferred check is named rather than skipped.** Two of the checks below cannot pass before detector code exists — shipping defaults against the frozen `[validated.runtime]`, and the `ties` comparator against the shipped mask — while §11 requires the checker in the first commit. So it takes `--stage prereg | implementation | release`, **every stage prints the checks it defers and the stage that owns them**, and an omitted branch is a failure rather than a pass. **The tag gate is `--stage prereg` exit 0**, which is what "the checker is green" means at registration time and nothing more.

A CI script diffs shipping defaults against the frozen section, and additionally checks: that stated totals match their addends; that the `ties` comparator is consistent across §2.3, §4.3, and the shipped mask; that §4.3's inequalities match the shipped rule; and **that each §0.1 lock-table row's target section contains that row's key phrase.**

### 6.9 Comparison default: exact equality

Runtime findings in exact mode are decided by **bitwise equality, not a tolerance.** A probe compares baseline against perturbed on one machine in one session, so local reproducibility is all it needs. Environment recording applies to reproducing published numbers, not to whether a user's own audit is valid.

### 6.10 One regime, and what a determinism failure means

L2a and L3.1 compare by **bitwise equality under a passing determinism guard** (§6.9). There is no second regime in v0.1.

**The guard runs on every execution frame, not once.** A pipeline can be deterministic on its original integer frame and nondeterministic on a promoted float or complex branch. With a single original-frame guard, that pipeline passes, and a promoted run then reports a difference caused by nondeterminism as though it were caused by intervention — corrupting evidence yield, false-alarm rates, completion rates, strategy diagnostics, and the fixture result.

> **Each distinct execution frame carries its own determinism guard**: the original frame for preserving runs, and each promoted alignment family for the strategies that use it.

> **A frame that fails its guard produces no runtime finding.** It is recorded as `could_not_run(determinism)` for the strategies assigned to it. There is no routing decision, no fallback, and no configuration parameter selecting between outcomes.

Case-level consequences follow from §7.7's required-or-optional machinery rather than from a separate rule: an original-frame failure reaches every preserving strategy, so the detector-case normally becomes `could_not_run(determinism)`; an optional promoted family's failure is a diagnostic that leaves a preserving proof untouched.

**`assert_audit_complete()` fails on any such entry.** A user who accepts the gap records an explicit exception (§8.3).

*(→ `HISTORY.md` H-10)*

### 6.11 Control runs

Three, all before any real probe. Failures are recorded per §7.7's two-level scheme, never as findings:

1. **Alignment equivalence.** Dtype alignment promotes the frame and recomputes the baseline, which removes promotion artifacts between probe arms but risks a different problem: the aligned pipeline may take different code paths than the user's. So: run the original baseline, run the aligned baseline unperturbed, and require equivalence.

   **The comparator is per column, not blanket:**
   - Where the original and aligned output columns have **the same dtype**, require byte equality directly.
   - Where they **differ**, the ordered pair (original dtype → aligned dtype) must appear in that strategy's **permitted promotion set**, and byte equality is required after promoting the original column to the aligned dtype.
   - **Any dtype difference outside the permitted set is divergence**, and that strategy is `could_not_run(alignment)`.

   *(→ `HISTORY.md` H-11)*

   Genuine path divergence changes values, not just representation, and still fails. No tolerance is introduced; permitted promotion sets are serialized into `VALIDATED_CONFIG`.

2. **Identity perturbation** — replace unavailable cells with an exact copy of themselves. Any delta is measurement artifact. On the aligned frame, once per alignment family.
3. **Compatibility, checked on every perturbed execution rather than once per strategy.** Confirm output shape and index match the baseline. A pipeline that drops rows under the NaN strategy returns a shorter frame, and every comparison after that is meaningless, including ones that look clean.

   **Compatibility is mask-dependent, so a single check cannot stand in for the probes.** L3.1 perturbs many columns and L2a perturbs only the label; early and late cohorts mask different cells; a mask that puts NaNs into a column feeding row-dropping logic behaves differently from one that does not. *(→ `HISTORY.md` H-12)*

   > There is no separate compatibility run. Every perturbed execution validates shape and index against the baseline before its result is used. A failure discards that probe's result.

   **Aggregation, locked, and it happens at two levels.** *(v16 recorded a failed probe as an unprobed cohort "for that detector × mode × strategy" while §7.2 publishes the unprobed rate and cohort sensitivity per **combination**, over EvidenceEvents that deduplicate across strategies. Take a row-dropping pipeline on a float frame: `nan` fails compatibility at cohort *d*, `shuffle` validly probes it, and both are `exact` × `preserving`. Was *d* probed? The strategy-scoped record said no, the successful execution said yes, and both published numbers moved with the answer.)*

   > **A cohort counts as probed for a combination when at least one strategy of that combination validly executed it.** The unprobed reclassification applies at the combination level only when **none** did. Strategy-level failures remain §7.5 diagnostics and never reach §7.2's rates directly.

   **Strategy-level escalation to `could_not_run(compatibility)`** uses a **failure fraction with a minimum absolute count**: the strategy is incompatible for the detector-case when `f ≥ m` **and** `f / n > q`, where `f` is failed perturbed executions, `n` is attempted eligible probes for that detector × case × strategy, aggregated by actual promotion status for publication (§7.5), and `m`, `q` come from `VALIDATED_CONFIG`.

   The minimum count exists because a bare fraction condemns a strategy on one failure in a five-cohort `quick` run. The denominator is attempted probes, not selected cohorts, so the rule measures the strategy's failure propensity rather than the cohort schedule. A consecutive-failure rule is **not** the definition — it assumes failures cluster, which is a development-corpus discovery rather than a form choice; it may serve as an execution circuit breaker, whose tripped probes still receive this same accounting.

   **Escalation is prospective.** EvidenceEvents from a strategy's valid executions *before* it escalated stand and are scored; the escalated state governs coverage from that point forward. A strategy does not retroactively un-probe cohorts it validly executed.

   **Locked at Phase 1:** the fraction-plus-minimum form, the denominator, how failures after a terminal finding are handled, the candidate ranges for `m` and `q`, and the objective used to select them. **Chosen on the development corpus and frozen with the matching `VALIDATED_CONFIG` section:** the values. **`m` and `q` are not selected to keep completion above §10.2's 60% floor** — the objective balances false silence, probe loss, and detector-case failure on their own terms, and the floor remains a downstream kill gate rather than a target.

### 6.12 Learned components

> No learned component may produce a PROVEN or RULE finding. PROVEN findings arise only from runtime intervention compared by exact equality on a dtype-preserving run. RULE findings arise only from deterministic declared rules. REVIEW screens may fit auxiliary statistical or predictive models, and where they do, the model class, seed, training data, parameters, and output are reported with the finding.

---

## 7. Metrics

### 7.0 What is locked now, and what arrives per phase

**The constitution below is locked for every detector row, present and future. The row-specific formulas are locked only for what the next gate publishes.**

v0.1 ships the runtime rows at Phase 3. The four evaluation partitions unseal at Phases 2, 4, 5, and 6, and the last four firings all landed in specifications for rows whose detectors will not exist until winter — written blind of the detectors they measure, reviewed by a process with a demonstrated floor of several findings per full-surface pass. Locking them now buys nothing and costs the loop.

**The measurement constitution — locked, and binding on every future module:**

1. Every published number states its unit, numerator, denominator, interval, and provenance (§8.6). A denominator introduced by paraphrase is a protocol failure.
2. Units come from the fixed grammar: case, cohort, **feature**, feature-cohort, cluster, code-site, candidate. *(`feature` was missing while §7.2's feature discovery recall counts features — a rule violated by a metric in the same file. The reducer could not assign the metric a legal unit.)*
3. **scope-eligible** and **execution-eligible** denominators are distinguished everywhere (§7.4).
4. `unsupported` and `could_not_run` are accounted separately from findings, everywhere (§8.2).
5. Every module defines sensitivity or states why it is impossible; **no metric may be silently dropped after its module is registered.**
6. Clean-case gating stays at §10.2 criterion 3's threshold and completion floor unless an amended root rule changes it.
7. Intervals follow §7.10; the fixture, conformance suite, and wild corpus publish no rates (§6.1).
8. REVIEW adjudication conceals flag status, freezes its rubric before outputs, mixes unflagged controls, and reports ambiguity as a third category.
9. **Cross-module pooling is forbidden unless pre-registered**, and every shared component declares which module owns its semantics.
10. Every published result names its module's registration date.

**Ownership, declared, because a rule against duplicated authority must not create it.** *(v23 listed `prereg-runtime` among the supplements while this file already specified runtime metrics, states, denominators, and gates in full, and no phase gate required such a registration — leaving it undecidable whether a later module would add to this file or override it. That is duplicated authority at the registration level, introduced in the version that outlawed it at the clause level.)*

| Owner | Owns |
|---|---|
| **`PREREG.md` (this file)** | the root constitution **and the complete runtime module** |
| `prereg-split` | L1.1, L1.4a/b, L3.1b, L3.2 metrics |
| `prereg-static` | L1.2, L1.3 metrics |
| `prereg-review` | L2b, L3.3 metrics and adjudication formulas |

**There is no `prereg-runtime`.** A change to root or runtime semantics is a class C amendment to this file, not a supplemental module. **A module may instantiate the obligations assigned to it and may never override another owner's requirement**; every shared component — the aggregator, the report — declares which owner holds its semantics.

Each supplement inherits §11's integrity chain in full: signed tag, file hashes in the tag message, external timestamp receipt, repository public.

> **The invariant:** a phase module's complete metric specification is committed and timestamped **before** that phase's development-corpus inspection, hand-authored case writing, adjudication-rubric writing, wrapped-tool output inspection, default tuning, detector implementation, and partition generation. **No detector row ships without its module tag predating its code.**

"Before implementation" alone is insufficient — a metric can be shaped around development examples or a wrapped tool's behaviour with no detector code in existence, so the invariant names all seven.

**A phase module is not a deviation.** It is a planned registration, not a repair, and it does not enter `DEVIATIONS.md` merely for existing. §0.2.1's class C governs *corrections* to a registered protocol; this is a different mechanism with the same integrity chain.

**The honest trade, stated plainly.** The whole-system lock proved that a Phase 5 metric was not shaped by Phase 2 results. The phased lock cannot prove that: the Phase 5 module will be written by an author who has seen Phases 2 through 4. What constrains it is the constitution above, the public timestamped registration with its reasoning, and the fact that later specs govern different detectors on partitions generated after their own freeze. The residual channel is cross-phase narrative adaptation — choosing a later unit or emphasis that makes the eventual v1.0 package read better — and this document does not claim to have closed it.

**Deferred to their modules:** L1.2's confirmation-status partition and code-site formulas, L1.3's site metrics, the duplicate cluster scoring unit, the split/case metric rows, the REVIEW rows' adjudication formulas, and later-phase strategy diagnostics. Each has a placeholder in §7.1 naming its obligation and its module.

### 7.1 Metrics follow the detector's output unit and mode

| Detector class | Rows / combinations | Required metrics |
|---|---|---|
| **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; conditional feature-cohort recall; cohort sensitivity; feature-cohort precision; feature discovery recall (secondary); unprobed feature-cohort rate; clean-case finding rate; completion and failure rates |
| **Runtime, `promoted`** | L2a, L3.1 | **evidence yield** and the same family below the first row, computed over `dtype_promoted` findings only |
| **Code-site, two modes** | L1.2, L1.3 | **Deferred to `prereg-static`.** Obligation: per-mode metrics, never pooled, with the confirmation statuses partitioning attempts and a stated evidential/operational split. Due before Phase 5 |
| **Split/case-producing** RULE | L1.1, L3.1b, L3.2 | **Deferred to `prereg-split`.** Obligation: case-level sensitivity, precision, clean-case false-alarm rate, abstention rates. Due before Phase 4 |
| **Cluster-producing** RULE | L1.4a | **Deferred to `prereg-split`.** Obligation: the cluster scoring unit and its canonicalization, plus cluster precision and recall. Due before Phase 4 |
| **`domain_judgment` REVIEW** | L1.4b, L2b, L3.3 | **Deferred to `prereg-review`.** Obligation: candidate precision, ambiguity as a third category, adjudication under constitution rule 8, no sensitivity. Due before Phase 6 |

**Detection hit counts are derived from EvidenceEvents** (§7.2), not from ReportedFindings, so a combination's numbers survive the aggregator collapsing its evidence into a higher-tier finding. **Case-level finding, completion, and incompletion rates are derived from the combination state pair of §6.6**, not from events. *(v25 said all four rows are computed over EvidenceEvents — stale from when there were four, and wrong in a way that changes numbers: implemented literally, a clean case with no event at all would vanish from its own case-rate denominator.)*

**Proof yield exists only for the `preserving` combination.** *(→ `HISTORY.md` H-13)* The `promoted` combination publishes **evidence yield**, defined identically but over its own findings, and the two names are never used interchangeably.

**Clean-case rates are computed per combination**, not per detector, and §10.2 criterion 3 gates per combination.

**L1.2's confirmation semantics are deferred to `prereg-static`** (§7.0), due before Phase 5. The obligation it must discharge: a status set that partitions attempts exhaustively, an explicit split between operational counts and evidential-quality measures, and a rule for which statuses may be described as supporting a finding. Nothing about L1.2's confirmation may be published before that module is registered.

### 7.2 The runtime scoring unit, and how detection is counted

**Two units, because scoring and display need different ones.** *(→ `HISTORY.md` H-19)*

| Unit | Key | Drives |
|---|---|---|
| **EvidenceEvent** | `(detector, promotion_status, feature, affected output cohort)` **within a case**; corpus-level records additionally carry case identity | every combination-specific metric in §7.1 |
| **ReportedFinding** | `(detector, feature, affected output cohort)` | user-facing display; carries the highest tier its events justify |

An EvidenceEvent is created once per combination that produced the pair, so a pair found by a preserving run and a promoting run yields two events — counted in the preserving and promoted rows respectively — and one ReportedFinding at PROVEN with the promoting event recorded as corroboration. *(→ `HISTORY.md` H-31)*

**Within a single combination, probe cohorts, strategies, and repeated runs are corroborating evidence, not additional events.** A pair found by three probes and two preserving strategies is one EvidenceEvent, one true positive.

**Scope of the deduplication:** it governs the **detection metrics of §7.1**. §7.5's per-strategy diagnostics count within each strategy — that is their entire purpose — deduplicated across probes and repeated runs within that strategy.

Detection follows §2.6's valid-finding rule, not probe selection:

- **proof yield** = correct PROVEN pairs ÷ **all scope-eligible labelled pairs**, so a case whose guard failed — or whose only firing strategies promoted — contributes misses and stays in the denominator. **This is the headline number for the runtime rows.**
- **evidence yield** = correct findings of one REVIEW combination ÷ **all scope-eligible labelled pairs**. Same denominator, different numerator, published per combination and never summed with proof yield into a single figure.
- **conditional feature-cohort recall** = **correct pairs in cases whose `schedule_state` is `completed`** ÷ all labelled pairs in those same cases. *(v23 restricted only the denominator, so a finding from an `incomplete` case could enter the numerator while its case was excluded below — a rate that can exceed 100%.)* Published alongside proof yield, never instead of it.
- **cohort sensitivity** = fraction of probed cohorts containing at least one labelled leaking feature where a correct finding was produced.
- **feature discovery recall** = fraction of labelled leaking *features* found in at least one cohort — secondary, never quoted alone.
- **unprobed feature-cohort rate** = fraction of labelled pairs whose affected cohort was not itself probed. A coverage statistic, independent of incidental detection.

A pair whose cohort was never probed counts as a miss **only when no valid probe detected it**. A cohort counts as containing a leak when **at least one** row in it is labelled leaking.

Proof yield settles the denominator question for every non-proving outcome: the pair stays in, and counts as a miss for the proof number while counting as a hit in whichever REVIEW row found it.

### 7.2.1 The runtime formulas, stated canonically

§7.0 declares this file the complete runtime module, so every number §7.1 names is defined here or the claim is false. *(v24 named feature-cohort precision, completion rate, and failure rate without defining any of them, and §7.4's execution-failure rate read the detector-case state that §6.6.1 forbids published runtime metrics from reading.)*

Per `(detector, promotion_status)`:

> **feature-cohort precision** = correct primary EvidenceEvents ÷ (correct primary EvidenceEvents + false primary EvidenceEvents).
>
> Secondary EvidenceEvents (§7.6) are excluded from **both** terms. Valid findings from `incomplete` schedules **are included** — the evidence occurred and would reach a user. **Undefined, not 0% or 100%, at an empty denominator.**

> **combination completion rate** = cases with `schedule_state` = `completed` ÷ cases with `schedule_state` ∈ {`completed`, `incomplete`}.
>
> **combination schedule-incompletion rate** = cases with `schedule_state` = `incomplete` ÷ the same denominator.

**A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

**"Scope-eligible case" means every labelled case in the body, clean cases included.** §7.4 defines scope-eligibility for a *unit*; applied to a case it needs saying, and the alternative — counting only cases that carry a labelled leaking pair — flips ten metrics and a gate on a concrete body: a combination `not_applicable` on every leaking case but `completed` on a clean one would be suppressed, hiding a clean-case finding rate that is a genuine measurement. Suppression exists to remove numbers that measure nothing, never to remove one that does. A yield computed over a combination that never applied is not a measurement of the tool: on a corpus of 25 labelled cases it reads `0/25`, which is indistinguishable in print from a mode that ran everywhere and found nothing. The `not_applicable` count carries that fact honestly; the yield does not. *(This is the cost of the strict reading above, and it is paid here rather than left in the numbers.)*

The `not_applicable`, `unsupported`, and `short_circuited` counts are published separately and enter neither. **Each is published as a count over all cases for that combination** — numerator and denominator, per §6.6.1's `MetricValue` shape — so it reads as a proportion; that is the count, not a rate derived from a filtered denominator. **No runtime metric reads the detector-case state of §7.7**, which exists for `assert_audit_complete()` alone.

### 7.3 The duplicate counting unit — deferred

Deferred to `prereg-split` (§7.0), due before Phase 4. The obligation: a canonical atomic unit for duplicate findings, a canonicalization rule mapping any detector's output onto it, and a ground-truth definition for near-duplicates that does not depend on post-hoc clustering of the tool's own output.

### 7.4 Two eligibility denominators

**Both denominators are defined here for every row including runtime; only the *rates* built from them are scoped.**

> **scope-eligible** — the leakage risk logically applies to this unit. For a labelled feature-cohort pair this is a property of the corpus label, **not of what the detector could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss.
> **execution-eligible** — the intervention point, inputs, and declarations are available.

*(v26 scoped this whole section off the runtime rows to remove a second failure rate, and took the definition of `scope-eligible` with it — while §7.2 goes on using the term for proof and evidence yield. Two readings of the yield denominator, and they differ by every labelled pair in a case the combination could not address. §7.2's own sentence — a case whose only firing strategies promoted "contributes misses and stays in the denominator" — settles it, but a term whose definition was scoped away from the section that uses it is exactly the duplicated-authority failure in reverse. The reducer surfaced this by having to choose.)*

**The runtime *rates* remain scoped away from this section.** For L2a and L3.1, unsupported and failure accounting is defined exclusively by §6.6, §7.2.1, and §7.7, and **no runtime metric reads the detector-case state.** *(v25 published an execution failure rate over `could_not_run`, which is a detector-case state, while §7.2.1 forbade exactly that. The two cannot agree: a case whose preserving combination is `incomplete(determinism)` while its promoted combination is `completed × observed_silence` has one undifferentiated detector-case failure and two distinct combination rows, and the detector-case number cannot produce both.)*

For every other detector row the two denominators are **scope-eligible** (the risk logically applies) and **execution-eligible** (intervention point, inputs, declarations available), and **each supplemental module defines its own unsupported, execution-failure, and abstention formulas before its phase** (§7.0). Those formulas are deferred with the rest of their module rather than inherited from a shape built for a different state model.

### 7.5 Per-strategy diagnostics

Per **detector × strategy × promotion status**: **eligible cases, completed cases, optional-strategy failures, required-strategy failures, alignment-equivalence failures, compatibility failures, determinism failures, control artifacts, correct primary findings, false findings.** Counted within the strategy, per §7.2's scoping, and derived from per-case records.

**Promotion status is a key, not a field.** One strategy resolves `preserving` on an all-float case and `promoted` on an integer-bearing one, so it contributes to both metric rows; pooling its runs into a single record with an aggregated field makes the preserving and promoted rows' eligible cases, completed cases, failures, and findings unreconstructable. The compatibility denominator of §6.11 is likewise counted per **detector × case × strategy** during execution and aggregated by actual promotion status for publication.

### 7.6 Secondary findings

A finding on a unit whose leakage is entirely inherited from an upstream labelled leaking unit is **secondary**: counted and published separately, neither true nor false positive.

### 7.7 Completion, and the two levels of state

**Two levels, and they are not the same thing.** *(→ `HISTORY.md` H-20)*

| Level | States |
|---|---|
| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |
| **Strategy diagnostic** | `completed`, `optional_strategy_failed`, `required_strategy_failed` |

`assert_audit_complete()` operates on **detector-case coverage states only.** An optional strategy's failure is a diagnostic, appears in §7.5, and never becomes a top-level `could_not_run`.

**Completion, locked.** A detector-case in a given mode is **complete** when the frozen default decision policy reaches a terminal result:

- **Termination is tier-aware.** *(→ `HISTORY.md` H-21)*
  - A **PROVEN** finding is terminal.
  - A `dtype_promoted` REVIEW finding is **recorded but does not terminate** while any required dtype-preserving strategy remains unrun. A detector-case completes without a proof only after every required proof-capable strategy has run or failed under the frozen policy.
  - A terminal finding completes the case regardless of any other strategy's failure; those failures still appear in §7.5's diagnostics.
- Absent a terminal finding, the case is complete when every **required** strategy has run and produced silence.
- Failure of a **required** strategy with no finding in hand makes the case `could_not_run` with that strategy's reason code.
- Required-or-optional status and the terminal-decision policy are part of the frozen configuration (§6.8).

**Clean-case rates**, published per mode and per evidence basis, and neither quoted without the other:

- **clean-case finding rate** = execution-eligible clean cases whose `evidence_outcome` is `finding` ÷ **execution-eligible** clean cases for that combination.
- **clean-case schedule-incompletion rate** = execution-eligible clean cases whose `schedule_state` is `incomplete` ÷ **execution-eligible** clean cases for that combination.

**Metric-denominator membership is defined directly on the state, not by exclusion:** a case enters a combination's metric denominators when its **`schedule_state` ∈ {`completed`, `incomplete`}**. `not_applicable`, `unsupported`, and `short_circuited` are outside every one of them, and are reported as their own counts. *(v24 defined "execution-eligible" by exclusion of two states while §6.6 separately excluded `short_circuited` from eligibility — two definitions of one denominator, which is the defect class this file exists to forbid.)*

Both denominators are the same set and neither numerator depends on the other axis, so both rates are bounded by construction and **no false finding escapes the gate because its schedule later failed.** *(→ `HISTORY.md` H-33)*

**A false finding is scored wherever it occurred, whatever the schedule did.** An `incomplete` schedule with `evidence_outcome = finding` on a clean case still produces an EvidenceEvent, still counts against precision, and is reported.

**Every preserving or promoted rate reads the two combination fields** (§6.6), keyed `(detector, promotion_status)`, never the collapsed detector-case state. *(→ `HISTORY.md` H-22)*

### 7.8 Conformance is a regression suite, and publishes no rate

The conformance suite contains identical pipelines under a too-permissive and a too-strict declaration. Its purpose is to check that the tool implements the declaration it was given — including deliberately wrong ones, and both `ties` branches.

**It is frozen at Phase 1 and is visible during implementation.** The availability machinery is debugged against it; that is what it is for. Two consequences:

- **Per-case pass/fail results are published. No aggregate conformance rate is published, ever** — a percentage over cases the implementation was debugged against measures the debugging.
- **The scoring unit is one case × one declaration.** A case passes when the tool's finding set under that declaration matches the declaration-relative ground truth exactly. Partial credit is not defined and is not awarded.

**Conformance cases contribute to no detection metric.** Under a too-permissive declaration a genuine leak *correctly* produces no finding relative to that declaration; counting it as a true negative would improve the clean-case rate while the tool missed real leakage.

### 7.9 REVIEW adjudication — deferred, under locked principles

The formulas and the detector-specific rubrics are deferred to `prereg-review` (§7.0), due before Phase 6. **Constitution rule 8 binds that module now:** flag status concealed during adjudication, rubric frozen and hashed before any output is seen, unflagged controls mixed into the set, ambiguity reported as a third category and never silently dropped, and precision undefined rather than 0% or 100% at an empty denominator. The adjudicator is the author and is not blinded to the tool's involvement; every REVIEW number says so and is labelled non-holdout.

### 7.10 Intervals

- **One-outcome-per-case metrics** (case sensitivity, clean-case rates, abstention rates): binomial 95% intervals.
- **Cohort-, feature-, feature-cohort-, site-, and cluster-level metrics:** case-clustered bootstrap 95% intervals, resampling whole cases and retaining all units within each sampled case.

Every published rate carries its interval and its *n*.

---

## 8. Reporting guarantees

### 8.1 The report never says a pipeline is clean

It says which detectors ran, in which mode, under which configuration and declaration, **which decision cohorts were probed and what fraction of rows they cover**, and what they found.

### 8.2 Not-run states

Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. None may be displayed in a way mistakable for a pass.

### 8.3 Three assertions

**Assertions consume unaggregated evidence, never the merged display tier.** A `ReportedFinding` collapses both combinations and takes the highest tier any of its events licenses, so a single PROVEN finding can rest on an **experimental** preserving event while carrying a **non-experimental** promoted event as corroboration. Whether that merged finding trips the assertion has three defensible readings and they disagree, so it is fixed here:

> **`assert_no_proven_leakage()` fails iff there exists an EvidenceEvent that (1) licenses PROVEN and (2) belongs to a non-experimental combination**, keyed `(detector, promotion_status)`.
>
> A `ReportedFinding` **retains the gate status of each constituent event** and carries no single inferred experimental boolean. Where its events differ, the display says so: *PROVEN — experimental preserving evidence; REVIEW — non-experimental promoted corroboration.*

Aggregation is lossy by design, and assertion eligibility is one of the facts it may not collapse. The cost is that assertion logic cannot run over the `ReportedFinding` list alone; it reads the events and the gate-status table. That is the correct cost.

- **`assert_no_proven_leakage()`** — fails per the rule above. Ignores coverage. **REVIEW findings of any basis do not trigger it**, and the report says so wherever any exist, so a passing assertion cannot be read as absence of evidence.
- **`assert_no_rule_violations()`** — fails on any RULE finding from a non-experimental detector mode. Ignores coverage.
- **`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings.

`assert_audit_complete()` accepts an allow-list of **explicit recorded exceptions** — no cryptographic signature mechanism is specified and the word "signed" is not used. Each carries detector entry, mode, reason, scope, date, and configuration hash, and all are printed in the report.

### 8.4 Tiers, declarations, and evidence are visible

- **Every L2a and L3.1 finding prints the availability declaration it was evaluated under, its promotion status, its probe cohort, and its affected output cohort.** A `dtype_promoted` finding names the promotion that occurred and states that no preserving run reproduced it. A `dtype_promoted` finding names the promotion that occurred and states plainly that a preserving run did not reproduce it.
- **Every L1.2 PROVEN finding prints the split declaration, the perturbed test population, the fitted state or training output that changed, and the attribution evidence.** L1.2 has no availability declaration to print.
- RULE findings state their declared semantics, including which `ties` branch of §4.3 they applied.

**A `could_not_run(determinism)` entry carries its remedy, in the report, as first-class text.** It names the columns that differed between runs and states the two user-side fixes — seed the pipeline, or run it single-threaded for the audit — rather than leaving them in a design note. The difference between "the tool refused" and "the tool named what to change and refused until it was changed" is the difference between an uninstall and a rerun.

**A partial cohort count is not weak evidence.** Permutation strategies can leave the decisive cell fixed (Claim C, registry 14), so "found in 18 of 20 cohorts" is the expected shape of a real leak and the report says so.

### 8.5 Reach and fixes are printed only when derivable

**Reach is a scanned observation, never an inferred dependency.** The refinement in `DESIGN.md` searches for the boundary at which masking stops changing the output. That search assumed the persistence of the change is monotone in the boundary, and **for an arbitrary user callable it is not**: a feature can depend on the masked region, stop depending as the mask shrinks, and depend again — three cells with baseline values (1, 1, 1), a constant corruption to 0, and a feature returning whether the sum lies in {0, 2} changes, does not change, and changes again as the mask narrows. A binary search over that returns the first cancellation and reports it as the answer.

Locked consequences:

- **A reach value is reported only from a full scan over the candidate availability boundaries present in the data**, and is described as the latest boundary at which a change was observed — not as the latest cell the feature depends on.
- **A binary-searched reach is reported as a lower bound and is never labelled exact.**
- **Above the cap, the capped subset is not scanned at all.** When the complete candidate count exceeds the frozen grid cap of §12, the lower-bound procedure runs instead and `reach_basis = lower_bound` is serialized. *(An alternative reading — scan the first `cap` boundaries and call it `full_scan` — would let a configuration value silently convert a partial observation into a complete one, which is the overclaim this section exists to prevent. `DESIGN.md` carried that reading while this file carried the fallback; one rule, one place, and this is the place.)*
- **Whether refinement runs at all is the frozen `reach_refinement_policy`**, not a property of `full` or `quick`. Those modes may supply defaults; the policy is serialized configuration like any other decision-affecting value (§6.8).
- **The word `exact` refers to the scan, not to the dependency**, and no reach claim asserts exactness of a black-box pipeline's dependency structure.

Phase 1's calibration cases (§0.3 items 3 and 4) establish the formula on simple windows; they do not establish monotonicity for arbitrary callables, and §6.5 now carries a case that breaks it.

A reach claim appears only when refinement produced it, marked as scanned or as a lower bound. Where refinement did not run, no reach and no fix suggestion is printed. When more than one column is affected in one probe, reaches may be inherited: the report marks secondary columns and withholds the fix.

### 8.6 Every published number states its provenance

Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval, the availability declaration in force, and — for runtime rows — the probed-cohort count and row coverage. Non-holdout author-produced numbers say so in the same line.

---

## 9. Wild corpus and cross-tool comparison

### 9.1 Wild corpus

Public time-series notebooks, hand-labelled. Failure-mode discovery only. No rates published.

### 9.2 Cross-tool comparison — protocol fixed before running

Phase 0 runs on the acceptance fixture — **after its declaration is reconstructed** (§6.2) — plus a separately enumerated prior-art comparison set of hand-written cases, one per leakage type, committed with this protocol before any tool is run.

1. **Eligibility** per tool × case, declared before any run, from documentation.
2. **Versions** and configuration recorded.
3. **Label mapping** written down before running.
4. **Ineligible cases score as abstentions, not misses.**
5. **Crashes score as abstentions**, counts published.
6. **Manual setup allowed** and recorded.
7. **No case excluded after results are seen.**

---

## 10. Phases and kill criteria

Hard constraints: **Concept A pre-registration — September. UChicago — 1 November.** Neither moves. Phases 2+ do not run in September.

| Phase | Work | Est. | Gate |
|---|---|---|---|
| **0** | Fixture declaration reconstruction with evidence; prior-art verification; cross-tool comparison per §9.2; licence check | 1–2 wknds | **Kill gate (§10.1)** |
| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |
| **2** | L3.1 and L2a exact mode; cohort selection; reach refinement; development tuning | 2–3 wknds | Config frozen **before** the fixture run; §6.2 pass gate; `[validated.runtime]` tagged; `evaluation_runtime` generated and run once; conformance per-case results published |
| **3** | **Public v0.1 release** | 1 wknd | A stranger can install and run it |
| **4** | L1.1, L1.4a/b, L3.1b, L3.2 | 2–3 wknds | **`prereg-split` registered and timestamped before any of this phase's work began** (§7.0); `[validated.split]` frozen; partition run once; its metrics published |
| **5** | L1.2, L1.3 (wrap static) + split-specific confirmation + aggregator dedupe | 2–3 wknds | **`prereg-static` registered and timestamped before any of this phase's work began**; `[validated.static]` frozen; partition run once; the "leak elsewhere" case does not upgrade a clean scaler and the non-temporal case still upgrades |
| **6** | L2b, L3.3 + model info sheet generator | 2–3 wknds | **`prereg-review` registered and timestamped before any of this phase's work began**, rubrics frozen and hashed before outputs are seen; `[validated.review]` frozen; partition run once; info sheet fills with unresolved fields marked |
| **7** | Profiles, docs, v1.0 | 1–2 wknds | `futures` and `generic` profiles ship |

**13–20 working weekends** (minimum 1+2+2+1+2+2+2+1 = 13; maximum 2+3+3+1+3+3+3+2 = 20). Computed by the CI script of §6.8, not by hand.

**Release at Phase 3.**

### 10.0 Phase 1 internal ordering, locked

0. **If Phase 0 recorded the fixture as semantically ambiguous, the class C amendment of §10.2 is committed and timestamped before anything below — including any development-corpus access.**
1. Write the throwaway mechanical tests for the §0.3 verification list.
2. Verify Claims A–C and the comparator cases.
3. Record the result. A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration; **a class C change requires an amended registration committed and timestamped before step 4** (§0.2.1).
4. Freeze the final comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, and reach definitions.
5. Generate and hash the evaluation-generator snapshot.
6. Generate and hash the conformance suite.

Steps 5 and 6 may not precede step 4. A snapshot frozen out of order is discarded and regenerated, and the discard is a `DEVIATIONS.md` entry.

### 10.1 Phase 0 kill gate — objective

**Stop building and contribute upstream if a single maintained tool satisfies all five:**

1. Covers at least the same published types at the same tier or better;
2. Produces explicit executed / not-run accounting;
3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
4. Installs and runs through a documented public interface without author modification;
5. Has had a release or commit within the previous 12 months.

Partial satisfaction is recorded and does not trigger the stop.

### 10.2 Other kill / pause criteria

2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**
   **Where the fixture is semantically ambiguous** (§6.2), this criterion is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning.** *(v23 permitted it after tuning, in `DEVIATIONS.md` alone, floored only at non-zero proof yield. An acceptance criterion is a class C semantic object by §0.2.1's own definition, and choosing its unit and threshold after seeing development behaviour can determine whether Phase 2 passes. It also contradicted §7.0's invariant, which requires a metric specification to precede corpus inspection and tuning — the carve-out and the new rule could not both stand.)*

   > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

   The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.
3. **Excessive false alarms on clean cases, under the default configuration** → the affected detector **or mode** ships marked experimental, is excluded from `assert_no_proven_leakage()` and `assert_no_rule_violations()`, and is labelled experimental wherever its findings appear.
   - **Finding-rate gate:** with **N** = clean cases whose `schedule_state` ∈ {`completed`, `incomplete`} and **k** = those whose `evidence_outcome` is `finding`, fail at **k ≥ floor(0.20 × N) + 1**. With N = 25 that is 6; with N = 10, 3; with N = 16, 4. *(v24 gated on `floor(0.20 × completed clean cases) + 1` while §7.7 had already moved the rate's denominator off completion. On 25 in-denominator cases of which 16 complete and 4 emit false findings, the rate reads 16% and passes while the gate computes 4 and fails — the same run shipping or not shipping experimental depending on which sentence an implementer read.)*
   - **Completion gate, separate and joint:** if fewer than **60%** of those same N cases reach `completed`, the detector or mode ships experimental regardless of its finding rate. The two gates close a gaming pair — the finding-rate denominator admits cases that crashed before executing, which a detector could hide behind by failing on hard clean cases, and the completion floor is what stops that.
   - **Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others.
   - A point-estimate rule; a confidence-bound rule at these sample sizes would block nearly every detector, and the instability is stated rather than hidden.
4. **Any phase competing with September or 1 November** → pause.
5. **Not installable by a stranger by 15 October** → stop and resume after 1 November. A date, not a phase number.

---

## 11. Registration integrity

1. **The first commit contains the registration and its checking tools, and no detector implementation:** `PREREG.md` (locked, unchanged), `DESIGN.md`, **`HISTORY.md`**, an empty append-only `DEVIATIONS.md`, a `PARKING_LOT.md` **containing only the §13.9 entry**, a placeholder `VALIDATED_CONFIG.toml`, **`tools/check_registration.py`** carrying §6.8's checks plus the single-source and banned-vocabulary scans, **`protocol/runtime_reference.py`** — pure, non-detector reducers, **at minimum** `resolve_schedule_state`, `resolve_evidence_outcome`, `derive_evidence_events`, `derive_reported_findings`, `compute_runtime_metrics`, `apply_runtime_gates`, and `evaluate_runtime_assertions`, the last of which §8.3 requires and the earlier list omitted — and **`tests/registration/`** carrying negative tests that a deleted symbol is rejected plus the exhaustive small-trace suite of §6.6.1. Earlier versions said five files and no implementation while the document relied on validators and scans; protocol tooling is not detector implementation, and residue defenses absent from the registered repository are not reproducible from it.
2. **Signed git tag** (`prereg-v30`).
3. **SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed** in the tag message and the README.
4. Commit hash **externally timestamped via OpenTimestamps**; the `.ots` receipt committed alongside.
5. **The repository is publicly reachable at the moment of tagging.** A registration nobody can fetch is not a registration.
6. `DEVIATIONS.md` append-only.
7. Evaluation generator snapshot, conformance suite, adjudication rubrics, parameter distributions, beacon records, and generated manifests frozen in their own files with their own hashes.

---

## 12. Expected outcomes

**Money: roughly zero.** Those who most need this — retail algo traders, students, hobbyists — pay least.

**Adoption: assume low.** Yang et al.'s tool was rigorous, published, and shipped as an IDE plugin, and uptake was minimal. `leak-detect` has been on PyPI since 2020 with almost no users: the method was available and nobody ran it. Leakage detection makes results look *worse*.

**Cost, and it has gone up in every version that made the accounting honest.** Per-frame determinism guards (§6.10) add a guard per promoted alignment family; per-probe compatibility (§6.11) folds the old per-strategy check into executions already counted; §6.6's evaluation policy runs every combination rather than short-circuiting. **This document states no total.** The figure depends on the frozen strategy set and on how many distinct promotion targets it contains, so **the CI cost script computes it from `VALIDATED_CONFIG` and the README quotes the script's output.** *(→ `HISTORY.md` H-23)* **Refinement dominates unless it is bounded.** The default full scan is linear in the candidate boundary count *B* per affected column *K* — roughly `K × B`, not `K × log₂B`. On a frame with thousands of distinct availability times, refinement can exceed the rest of the audit by orders of magnitude. *(→ `HISTORY.md` H-24)*

Three consequences, locked:

- **`VALIDATED_CONFIG` carries a candidate-grid cap**, and the frozen value is part of the configuration like any other (§6.8). A scan beyond the cap falls back to the lower-bound mode and says so on the finding.
- **Refinement is off in the quoted default configuration.** Any scale figure that includes it says so.
- **The CI cost script computes the total including refinement under the frozen cap**, and the README quotes the script.

For scale only, and not as a locked figure: with refinement off, the full audit is in the high eighties and `quick` is in the mid teens. With refinement on it is bounded by the grid cap and is materially larger. **This number, not detector quality, decides whether anyone runs the tool.**

**Determinism is now a hard gate, and that is the third adoption cost — probably the largest.** Parking the fallback (§13.9) means a pipeline whose frames fail the guard receives nothing from L2a and L3.1. In this domain that is the common case rather than the exception: threaded boosting libraries, GPU training, and unseeded stochastic steps are all standard. **Expect a substantial fraction of first-contact audits to return `could_not_run(determinism)` and nothing else.** The mitigation is real and cheap — seed it, or run single-threaded for the audit — which is exactly why §8.4 requires the report to say so at the point of failure. A tool that refuses without instructions gets uninstalled; one that refuses with instructions gets rerun.

**Declaration burden is the second one.** Per-cell availability, a label horizon no profile will guess, and — for non-temporal tasks — an explicit label-construction policy.

**The proof tier is narrower than the evidence, and that is the third.** §3.2 means a user running the strongest strategy gets REVIEW, not PROVEN, unless a preserving run reproduces the finding. On all-float frames that costs little — `noise` and `nan` preserve there. On integer-bearing frames it can leave `shuffle` as the only proof-capable strategy. Some users will read that as hedging. It is the tool declining to assert something it has not established.

**What's actually worth having:** a finished artifact people can install; the end-to-end build that closes the implementation gap; a citable tool for Concept A; and a coherent arc — found the problem, measured it, built the instrument.

**For the record:** the stated motivation was that this sounds fun. Phases 5 and 7 are not fun. If it gets finished, it gets finished there.

---

## 13. Open decisions (author only)

1. Name and PyPI availability
2. Licence — **resolve in Phase 0**. `leak-detect` is MIT; anything taken from it gets an attribution note regardless.
3. Defaults — chosen on the **development** corpus, frozen before each gate. Never on an evaluation partition or after a fixture result.
4. Whether the CME fixture ships in the repo, full or sliced — **CME redistribution terms must be checked.** Blocks the Phase 3 release.
5. Whether `deepchecks` is wrapped for L2b/L3.3 — Phase 6, on Phase 0 evidence.
6. Whether panel probing covers all entities per cohort or samples them — Phase 2, with timing data.
7. Which public randomness beacon (§6.4). *(The timestamping service is resolved: **OpenTimestamps** — free, account-free, permanently verifiable, sufficient for §11.4. Flagged six consecutive rounds while nothing depended on it.)*
8. Whether the original CME experiment documented its prediction instant well enough to reconstruct the declaration (§6.2). **Resolve in Phase 0** — it decides whether kill criterion 2 applies or is replaced.
<!-- banned-exempt: id=PARK9 reason="the parking-lot pointer must name the parked mechanism to state what an amendment would restore" -->
9. *(Resolved and parked.)* **The statistical fallback is not built and is not pre-registered for v0.1.** `PARKING_LOT.md` carries one entry: *a potential noise-floor fallback for nondeterministic pipelines; requires an amended registration, separate development tuning, and a new unseen evaluation partition before any result is published.* It is not an engineering toggle — it introduces a new evidence standard, its own metrics, its own controls, and its own false-alarm regime — so an amendment is the correct mechanism rather than a config flag. The cost is registry entry 15: a pipeline that cannot be made deterministic gets nothing from this tool.

*(→ `HISTORY.md` H-25)*
