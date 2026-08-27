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

<!-- v30a SC-9 — INSERT_AFTER -->

**THE CLAUSE.**

> **Integrity of a declared instance — v30a [SC-9]**
>
> **(a) A DECLARATION SUPPLIES DATA UNDER A REGISTERED SCHEMA. IT CREATES NO GATE OBJECT.** A
> declaration supplies the values, enumerations, and evidence the registered clauses call for. **It
> creates no new criterion, no new denominator, no new coverage state, no new unit, and no new gate
> class.** Where a declaration finds it needs one, that is a class C amendment to this file, made
> before the declaration relies on it. **The criteria of §6.2 as amended are the whole gate**; a
> declaration that adds a fifth is adding a fifth way to fail, outside the registration.
>
> **(b) EVIDENCE ARTIFACTS ARE NEVER ADJUSTED TOWARD A DECISION.** A manifest, a measurement record, a
> capture, or any artifact whose job is to record what was measured **is not edited to carry a
> declaration, a decision, or an amendment.** Where a registered element's recording locus must move,
> the locus is **amended explicitly**, and the amendment says what moved and what did not. An evidence
> artifact edited toward a wanted answer is no longer evidence of anything.
>
> **(c) A LOCKED OBLIGATION IS DISCHARGED ONLY BY BEING MET OR BY BEING AMENDED.** It may not be
> discharged by a `DEVIATIONS.md` entry, by a working resolution, by an orchestrator decision, or by
> being carried forward silently. Dropping it is a further class C amendment. **An element that cannot
> be met as written at the instant an amendment must be committed is amended explicitly — never waived
> and never left outstanding**, because an outstanding element invites being re-read as satisfied
> later.
>
> **(d) WORKING-RESOLUTION AUTHORITY IS UNIFORM, AND SUPERSESSION IS ORDERED.** A working resolution
> binds by its content and its date, **not by where it was recorded**: a resolution issued in the
> course of the work binds exactly as one written into the record does, and the record is completed
> to contain it. Where a later resolution supersedes an earlier one, **the later governs and the
> earlier stands as the record**; the ledger is append-only and an entry is never rewritten to agree
> with its successor.
>
> **(e) THE INTERPRETATION RULE — resolution toward the stronger reading only.** **An interpretation
> of locked text may resolve ONLY toward the STRONGER reading. Any interpretation that weakens a
> locked obligation — narrows a denominator, exempts a unit, softens a criterion, admits an excluded
> set, converts a required finding into an optional one, or converts an unscored cell into a pass — is
> a class C amendment and may not be recorded as a working resolution, a decision-log entry, or a
> reading.** This binds every entry appended after the rule, and it binds the reading of this
> registration by its own author.
>
> **(f) A RULE STATED TWICE HAS NO CANONICAL SOURCE.** *(Citation: §0.2.1 line 77.)* Where a
> declaration needs one of these rules, it **cites this section and does not restate it.** A second
> normative copy in a declaration is the duplicated-authority failure, not a redundancy.



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

<!-- v30a SC-1 — INSERT_AFTER -->

**THE CLAUSE.**

> **§2.9 What a reconstructed declaration fixes, and what it may not leave open — v30a [SC-1]**
>
> A declaration is the gate's semantic authority: every availability instant a comparator reads is
> the one the declaration declares. The requirements below follow, and a declaration that does not meet
> them fixes nothing.
>
> **(a) MEASURED, NOT INTENDED.** Where a reconstructed element's *documented* value and its
> *measured* value differ, the declaration declares the **measured** value as the element's declared
> value, records the documented value beside it, and names the artifact each was read from. A gate
> scored against an intended value the artifact does not exhibit is scored against a fixture that
> does not exist.
>
> **(b) THE REPRESENTATION IS NAMED.** Every declared element states **which representation of the
> data it describes** — the value as constructed, or the value as fed to the model — and, where a
> transform separates them, names the transform. An element that does not say which representation
> it describes fixes no availability instant, and every downstream class derived from it is
> underivable.
>
> **(c) A ROLE IS A POSITION, NOT AN AVAILABILITY INSTANT.** A `column_roles` value (§2.3) names
> where a value sits on a lattice. The instant the comparator reads is the availability instant the
> declaration declares for that column. **Where a role is an approximation of that instant, the
> declaration says so, and that role is never scored against.** Scoring against a positional
> approximation instead of the declared availability instant is a scoring error, not a tie
> convention.
>
> **(d) UNITS ARE DECLARED, AND A CHANGE OF UNIT IS CLASS C.** Where a declared element supplies a
> term of a registered formula, the declaration states that term's **unit**. Where the declared unit
> differs from the unit the registered formula assumes, the substitution is a **class C amendment**
> under §0.2.1 line 93 and is carried by an amended registration — never by the declaration alone,
> and never by a working resolution.
>
> **(e) STALENESS IS NOT UNAVAILABILITY.** A value whose declared availability instant is legal at
> the decision instant under the declared `ties` branch is **available**, however old it is. Age
> licenses no finding. A finding resting on staleness alone is a false positive.
>
> **(f) ONE COMPARATOR BRANCH IS SCORED.** Exactly one `ties` branch (§2.3) is declared, and it alone
> is scored. Figures computed under any other branch are published as **informational disclosures**
> so the tie choice is auditable: they enter no denominator, contribute to no rate, and **no gate
> outcome may be computed from them.** Reporting a pass or a fail under a non-declared branch is out
> of specification.



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

<!-- v30a SC-10 — INSERT_AFTER -->

**THE CLAUSE.**

> **Declared non-gated data — v30a [SC-10]**
>
> **(a) A DECLARATION MAY CARRY DATA THE GATE DOES NOT CONSUME, IF IT SAYS SO IN TERMS.** The
> declaration marks such a body **NOT PART OF THE GATE**: nothing in it enters any acceptance
> criterion, any denominator, any rate, or the freeze of SC-8. It is published as a diagnostic, with
> its own provenance, and it is exempt from the freeze **precisely because** it is exempt from the
> arithmetic.
>
> **(b) THE EXEMPTION IS CONDITIONAL, AND THE CONDITION IS THE WHOLE POINT.** Non-gated data may be
> added, revised, or withdrawn without amendment **provided its figures are never moved into an
> acceptance denominator.** Moving any of them in is a class C amendment — and a body that is both
> unfrozen and admitted to a denominator is a denominator that can move after a result.
>
> **(c) DIAGNOSTIC CLASSES ARE NOT DECLARED CLASSES.** Where the declaration's class set carries
> classes for diagnosis alongside the classes the map scores, **the diagnostic classes are named as
> such and are not members of the declared scored set.** Any statement of the form "maximum across
> classes" **names the class set it maximises over**, and any headline over a partitioned population
> names the partition it counts.
>
> **(d) FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**
> Non-gated data, diagnostic classes, and figures the declaration marks informational may never be
> quoted as: **(1)** evidence about a unit the scored pipeline consumes, in either direction; **(2)**
> **any criterion-1 arithmetic**; **(3)** an unqualified headline over the scored population; **(4)**
> an unqualified maximum or peak. A peak is quoted with its class set **and** its metric, or it is not
> quoted.
>
> **(e) ONE COPY.** These rules are stated here and cited elsewhere. A declaration restating them for
> a particular side has created a second normative copy (§0.2.1 line 77) and must cite instead.



### 6.2 Acceptance fixture

- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair on both sides (§A.1 item 1) — that fact, and the replacement entries themselves, are instances and are recorded in the declaration. **The clause "and because the anchor's model family changed" stood here until R55/W5 and is struck: it is false against its own cited source, which names six architectures with LightGBM listed first, and §A.1 item 2 was corrected on 21 August 2026 to say so.** Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
- **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.
- **The availability declaration is reconstructed, not chosen** — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon, and intended live execution protocol, with **evidence for each element recorded before any detector tuning.**
- **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).
- **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.
- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*
- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

<!-- v30a SC-2 — INSERT_AFTER -->

**THE CLAUSE.**

> **The acceptance fixture's composition — v30a [SC-2]**
>
> **(a) THE FIXTURE IS AN ENUMERATED SET OF ARTIFACTS, DECLARED.** The declaration enumerates the
> artifacts that constitute the acceptance fixture, by side, with the provenance of each. An artifact
> not in that enumeration is **not part of the fixture** and no criterion is evaluated on it.
>
> **(b) CHANGING THE COMPOSITION IS CLASS C — NEVER A DEVIATION, NEVER A WORKING RESOLUTION.**
> Admitting an artifact the declaration excludes, or removing one it includes, **changes the object
> the acceptance criteria are evaluated on and therefore changes what every published gate number
> means.** It is a class C amendment under §0.2.1 line 93. It may not be done by a `DEVIATIONS.md`
> entry, by an orchestrator decision, or by a working resolution. **Declared exclusions are hard.**
>
> **(c) THE PRE/POST LICENCE IS BOUNDED.** Where the fixture is a paired pre/post construction and a
> delta across the pair is read as an availability effect, the licence for that reading requires the
> two sides to differ **in availability and in nothing else**. **A change to the column set, the
> label set, the row population, or the evaluation population is not an availability change**, and a
> variant carrying one is not admissible as a side of this fixture.
>
> **(d) A REFERENCE ANCHOR IS CONSTITUTED BY RECOMPUTATION, NOT BY TRANSCRIPTION.** Where the gate
> requires a reference quantity to reproduce, that quantity is **recomputed from the fixture's own
> committed bytes** and declared as an **enumerated set of entries**, one per declared horizon and
> side, each naming its provenance. **The recomputation is authoritative over any figure recorded in
> a prior report**; a recorded figure that agrees is a secondary record and is reported as such, and
> one that disagrees is a defect resolved before the gate runs, never a competing anchor. **The
> declared tolerance applies per entry and may not be widened.** Because a recomputed anchor is a
> pure function of committed bytes, a deviation approaching the tolerance is a **stop-and-report**,
> not a pass.
>
> **(e) MOVING AN ELEMENT BETWEEN PHASES IS AN AMENDMENT, AND ITS SCORING RULE IS DECLARED WITH THE
> MOVE.** A registered element that cannot be satisfied at the instant the amendment must be
> committed is **amended explicitly — never waived and never left outstanding.** Where the move
> re-registers the element as a later-phase obligation, the obligation names the event that makes it
> due, and its scoring rule is declared **ex ante, at the move**, so it cannot be chosen after a
> result is seen.



**Pass gate — discrimination, not tier.**

*(Through v18 criterion 1 required a finding **at PROVEN tier**. That coupled acceptance to reporting: the gate asks whether the method separates two datasets whose answer is already known, while tier answers what a user may claim about their own pipeline. The coupling generated eight firings' worth of machinery — §0.2.1 — and all of it is now deleted.)*

Evaluated on the **frozen default configuration**, under the reconstructed declaration:

1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.
2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.

<!-- v30a SC-3 — REPLACE_LINE -->

**THE CLAUSE.**

> **3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH
> MAP — v30a, operative. [SC-3]**
>
> **(a) WHAT THE MAP IS.** The map is an **enumeration of expected findings**, declared in the
> fixture's availability declaration, stated **per side**, **per declared violation class**, and
> **per declared cell** of the declared scored population. **The declaration declares the cell key —
> the unit it declares the fixture to be partitioned into — and names it explicitly.** The map is
> published as an artifact with a **declared schema**: one row per cell of the declared scored
> population, with every field named, including the field that records whether the cell is
> scored. **The artifact may in addition carry rows of a class the declaration declares
> DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no
> criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the
> map's cells, not over the artifact's row count**. A count taken from the artifact without
> excluding them counts a different population, and **every figure published from the artifact
> names which population it counts**.
>
> **(b) THREE DISPOSITIONS, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE MAP.**
> - **A finding the map predicts is REQUIRED.** Its absence is a miss.
> - **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier,
>   primary or secondary.
> - **A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none,
>   enters no denominator, contributes to no rate, and is **never reported as a pass.**
>
> **(c) THE MAP COVERS THE WHOLE DECLARED SCORED POPULATION.** The declaration declares the scored
> population — the rows and units the criteria adjudicate. **A subclass of that population is never
> excluded, masked, or given a separate denominator by description**; the only way a unit leaves the
> scored arithmetic is by being an UNSCORED cell of the map, declared as such before any detector
> runs. Membership of a unit in a structurally awkward subclass — a boundary, a gap, a session
> edge — is **by itself neither a licence for a finding nor a defence against one**; such units are
> adjudicated by the map like any other.
>
> **(d) THE MAP IS STATED IN THE TERMS THE DECLARATION DECLARES.** It is stated in the representation
> §2.9(b) names and **side-relatively**. **There is no side-independent statement of what leaks**; a
> side-independent list is a category error and misroutes every finding derived from it.
>
> **(e) ONE SCORING KEY, AND ONLY ONE.** A re-aggregation, restriction, or re-projection of the map
> published for reporting is a **REPORTING OBJECT**: it is **not a second scoring key and changes no
> adjudication.** Where two views of the map are published, both are published with their delta
> explicit and neither replaces the other.
>
> **(f) A DERIVED SUBSET INHERITS ITS CELLS.** Where a subset of a scored artifact is produced (a
> slice, a filtered variant, a projection), it **inherits the map cells its units select** and is
> scored against those cells under this criterion. **A subset of a characterized side is never
> treated as clean, and a subset may not be reported as a pass on the strength of containing only
> unscored cells.**
>
> **(g) NEITHER SIDE IS ASSUMED CLEAN.** A side the declaration characterizes is **CHARACTERIZED,
> never clean**, and no report describes it as clean. Silence and belief never convert into a pass
> (§2.7, §8.1), applied here to the tool's own exam.
>
> **(h) THE AMENDMENT DOES NOT LOWER THE BAR.** A finding on a cell the map marks zero is still a
> false positive and still fails the gate. The unscored disposition is not an escape hatch. The map
> is **declared and frozen before any detector runs** (SC-8); a map frozen after a run is a key
> shaped by the result and scores nothing.


4. Silent under the identity control on both.

Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

<!-- v30a SC-4 — INSERT_AFTER -->

**THE CLAUSE.**

> **The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]**
>
> **(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY THE RULE REGISTERED HERE, AND THE
> DECLARATION SHOWS THE DERIVATION.** The rule by which each unit of the declared scored set is
> assigned its gate class is **registered in this clause — the class predicates of (b), under the
> precedence of (c) — and is not the declaration's to state, restate, or rewrite.** The declaration
> states, **ex ante, in full, and per unit**: the class assigned, and the registered predicate the
> unit satisfies, **by citation to the row of (b) that carries it**, together with the declared
> facts on which the unit satisfies it — what the map declares on it on the scored side under the
> declared branch, and the construction and legality facts the declaration records for it. The
> classes are **derived by the registered rule over those declared facts, never assigned by hand.**
> **No companion document states a class predicate in rule form** — as a biconditional ("CLASS iff
> …") or otherwise: the predicate is cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f)). An
> evidence artifact's classification of how a unit was *built* answers a different question from
> what the map declares *violating* on the scored side under the declared branch; the two do not in
> general have the same answer. **No classification of the scored set other than this derivation
> enters any criterion, denominator, or count**, and no split within such a classification carries
> gate arithmetic. Any report quoting such a count names the scope it counts under.
>
> **(b) EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE DECLARED SCORED SET.**
>
> | Class | Registered predicate (cited by the declaration, per unit; never restated) | What a finding on it means |
> |---|---|---|
> | **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
> | **OUT OF JURISDICTION** | every constituent read is declared legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
> | **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |
>
> **The declaration cites these rows, per unit, and states the facts on which each unit satisfies
> the row it cites; it does not restate them** (a). **There is no fourth class and no residue
> class.** **N is the length of the REQUIRED list**, and no other quantity is N.
>
> **(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED
> wins.** The declaration derives under this precedence and states none of its own; a unit's class
> is the first the order yields, and for each unit that satisfies more than one predicate the
> declaration records which it satisfies and that precedence decided it.
>
> **(d) THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE
> DERIVATION.** Where a registered class predicate admits two readings, the declaration states which
> it derives under and why, before any detector runs. **Two readings are registered as forbidden
> outright**, because each silently removes units from the arithmetic: (i) a locality condition may
> not be read more narrowly than the declared lattice, so a read of the same source at another
> instant of the same lattice does not by itself create a cross-source violation; (ii)
> **unconstructibility in some other rebuild of the fixture is never gate-unscoredness** — only a
> gate status the declaration declares EXCLUDED on the artifact the gate actually scores removes a
> unit from the arithmetic.
>
> **(e) GROUNDS FOR EXCLUSION ARE DECLARED, AND DECLARED PRE-RUN.** A unit is excluded only on a
> ground the declaration states. Two grounds are registered here because each is otherwise a
> guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that
> cannot carry a finding of the scored class at all** (leaving it in the denominator makes criterion 1
> unsatisfiable), and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot
> be scored under any reading). **Reinstating an excluded unit changes the denominator and is class
> C.**
>
> **(f) PUBLICATION DISCIPLINE — the constraints below, and they are the point of the rule.**
> 1. **Each class is published as an enumerated list of unit names.** A class stated as a bare count
>    is not auditable and does not satisfy this. A count that cannot be written out as a list is a
>    count nobody can audit.
> 2. **No class is defined as a residue.** "Everything else" is not a class definition; each unit's
>    membership is derived by (a) and shown.
> 3. **The partition check is printed and reproducible by any gate report:** the three class sizes sum
>    to the size of the declared scored set, no unit appears in two classes, and no unit of the set is
>    missing from all three. **A gate report that cannot reproduce the check has not scored the
>    fixture.**
>
> **(g) ONE GATE CLASS PER UNIT.** A unit carries **one** gate class and one only — §0.2.1 line 79's
> rule that no field answers two questions, applied to gate classes. **A unit's gate class is a
> statement about what the gate does with a finding on it, and the gate needs exactly one answer per
> unit.** An availability *declaration* about a unit and its *gate class* are different objects and
> are never conflated: a unit the declaration does not feed to the scored pipeline holds **no gate
> class whatever** — declaring it out of jurisdiction would imply the gate adjudicates it and
> declines.
>
> **(h) RE-DERIVATION IS MANDATORY, AND MOVING A UNIT IS AN AMENDMENT.** If a unit's construction
> changes, or an excluded unit becomes constructible, its class is **re-derived by the rule of (a).**
> **The declaration's enumeration is the current output of the rule and is never a substitute for
> it.** Moving a unit between classes, or changing N, after the tag is a class C amendment.
>
> **(i) DISAGREEMENT HALTS.** Any disagreement between the rule-derived class and the frozen class is
> a **stop-and-report**. It is not resolved in favour of either at run time, and a run that proceeds
> past it has not scored the fixture.
>
> **(j) THE SCORED SET IS NAMED, NOT COUNTED.** The declared scored set is identified by **the named
> constant the declaration declares**, never by its cardinality. Any re-derivation names the constant,
> not the length; two sets of equal size are not thereby the same set.
>
> **(k) TWO MECHANISMS AGAINST A COLLAPSING SCORED POPULATION, AND NEITHER IS SUFFICIENT ALONE.**
> There are two ways criterion 1 stops meaning anything, and they need different instruments. The
> population can go **empty** — the degenerate case, caught by the floor at (k1). Or it can be
> **narrowed unit by unit** until what survives is not worth scoring — the gradual case, caught by the
> reconciliation at (k2). **(k1) alone is satisfied by scoring a single column.** It is written below
> as the terminal backstop it is; **the operative protection is (k2)**, and a reader who takes the
> backstop for the mechanism has mistaken which failure this clause exists to stop.
>
> **(k1) THE FLOOR — THE TERMINAL BACKSTOP.** The declared scored set and the REQUIRED list are
> enumerated by name **before any detector runs** and are **non-empty on every declared side**. **If
> either is empty on any declared side, criterion 1 is not discharged and the outcome is STOP** —
> lifted only by supplementing the declaration with declared, enumerated units for that side and
> re-freezing under §11's integrity chain; never by scoring criterion 1 on the remaining side, never by
> suppressing the empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution.
> **Non-emptiness is the whole of this limb, and deliberately so:** any minimum above zero would be a
> threshold chosen from the distribution this fixture already exhibits, which §7.0 forbids. A floor
> that cannot be set without looking at the data is not set. **This limb therefore catches only the
> degenerate case; it is not the protection and must not be cited as one.**
>
> **(k2) THE RECONCILIATION — THE OPERATIVE MECHANISM.** The REQUIRED list is published alongside a
> **per-unit reconciliation against the fixture manifest's list of columns classed as leaking
> sources** — the **named list**, not the count. **Every unit the manifest so classes that this
> derivation does not class REQUIRED is named**, with **the registered predicate of (b) that produced
> its class** and the declared facts on which it satisfies that predicate. A difference stated as a
> count, a total, or a summary of where the differences "mostly" sit does not satisfy this limb; the
> unit is named or it is not reconciled.
>
> **(k2)(i) EVERY GROUND NAMES THE ARTIFACT AND LOCATION THAT SUPPORTS IT.** For each such unit the
> declaration cites **the artifact and the location within it** — file, and row, line, or field — on
> which the declared facts rest. **The quality of a ground is not something this registration can
> require**, and pretending otherwise would be vagueness dressed as a constraint; **provenance is.** A
> ground with an artifact behind it can be looked up and disagreed with. **A ground with nothing
> behind it becomes visible as such**, which is the whole of what this limb can achieve and is worth
> more than a bar no reader could apply.
>
> **The list is a publication input, and the count remains not a gate number.** Reading the list under
> this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
> denominator — (k3) governs, and §6.2 line 446's manifest requirement is unamended. **Because the
> gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
> in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
> own later revision cannot decide a gate outcome; an author review that silently made a complete
> reconciliation incomplete would be a change to a gate input outside the class C route.
>
> **(k3) A DISCLOSURE, NOT A CLASSIFICATION — AND THE LIMIT OF WHAT A READER CAN CHECK.** **A
> reconciliation published under this limb is a disclosure, not a classification entering a criterion,
> denominator, or count** (a). It derives nothing, changes no class, and no quantity appearing in it is
> N. That sentence is load-bearing: without it (a) forbids the very comparison that makes the
> denominator auditable, and the limb would contradict the clause it sits in.
>
> **What a third party can and cannot do with it, stated plainly rather than implied.** The declared
> map and this reconciliation are published with the registration; **the acceptance fixture is not,
> and no clause requires it to be.** So a reader can check the reconciliation for **completeness**
> (every manifest-classed leaking source accounted for), for **internal consistency** (each ground
> citing a registered predicate), and for **provenance** (each ground naming an artifact and
> location) — and **cannot** independently verify a classification against the fixture's data. **This
> limb is therefore a disclosure obligation with limited external verifiability, and it is registered
> as one.** Claiming it delivers an audit a reader cannot perform would be the same defect as an
> overstated availability claim.
>
> **(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared
> side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named
> without the registered predicate that produced its class, **or is named with a ground that cites no
> artifact and location (k2)(i)**; **or where the manifest the reconciliation reads is not enumerated
> in the declaration's SC-8(a) freeze, or carries a `DRAFT` status at the tag (k2)**. *(Both of those
> last two are conditions (k2) states, and until R60 neither was indexed here — a limb may not impose
> a condition and leave nothing to enforce it. **Both are unmet as at the date of this amendment**:
> the freeze's "specifically and exhaustively" list does not name the manifest, and the manifest's
> recorded status is still `DRAFT - author review required`.)* **This is a live gate item, not a check that only fires on
> corruption: it can fail on an artifact that is behaving correctly, and on the fixture as declared at
> the date of this amendment it is UNSATISFIED.** The declaration publishes a per-unit
> cross-tabulation of the construction-SOURCE cut against the gate cut, which is a different pair of
> partitions; it publishes no per-unit reconciliation against the manifest's leaking-source list. The
> difference the limb would surface is **fourteen units**.



<!-- v30a SC-5 — INSERT_AFTER_RELATIVE -->

**THE CLAUSE.**

> **Adjudication routing — v30a [SC-5]**
>
> **(a) EVERY FINDING IS CHARGED TO EXACTLY ONE CRITERION, BY THE CLASS OF THE UNIT IT NAMES.** The
> gate needs one answer per finding. Routing is derived from the unit's gate class (SC-4) and the
> map's disposition of the cell (SC-3), and from nothing else.
>
> **(b) ATTRIBUTION IS TO THE GROUND, NOT TO THE NAME.** A REQUIRED entry is satisfied only by a
> finding **on the side, in the cells, and on the ground the map declares.** **Criterion 1 is not
> satisfied by unit name alone.** Where a unit has two grounds — one the map declares violating, one
> declared legal — **the gate class follows the violating ground**, the legal ground is recorded as a
> fact and not applied, and **a finding on the legal ground does not satisfy the REQUIRED entry.** It
> is recorded on its own ground, and not credited to the unit's REQUIRED status. Naming the right unit
> on the wrong ground satisfies nothing.
>
> **(c) THE FALSE-POSITIVE CONSEQUENCE ATTACHES TO THE OUT-OF-JURISDICTION CLASS AND TO NO OTHER.** An
> availability-class finding on an out-of-jurisdiction unit is a **declared false positive**, recorded
> as such in the gate report. **It is not converted into a failure of the clean-source criterion**,
> which has no landing site for such a unit; that criterion's scope is the units the declaration
> declares clean, and those units **do** route to it. **The false-positive consequence is never
> carried beyond the out-of-jurisdiction class.**
>
> **(d) A FINDING ON A CHARACTERIZED SIDE IS CHARGED TWICE ONLY WHERE THE CRITERIA ARE INDEPENDENT.**
> Where a finding is a false positive under (c) **and** contradicts the map on a characterized side,
> it is charged under both the false-positive tally and criterion 3, and the report says so. Where two
> criteria would otherwise adjudicate the same finding on the same ground, the declaration states
> which one governs, ex ante.
>
> **(e) JURISDICTION BETWEEN DETECTORS IS DECLARED, AND A BOUNDARY CUTS BOTH WAYS.** Where a finding's
> character belongs to a detector row **outside** the criteria this gate scores, the declaration
> assigns it to that row and it is **neither credited nor penalized here.** Routing it into this gate
> would let a finding of one character masquerade as a finding of another and corrupt both counts.
> **The assignment is declared before any detector runs; it may not be made after seeing where the
> findings landed.**
>
> **(f) DECLARED SENTINELS UNDER THE IDENTITY CONTROL.** An as-built artefact of the fixture that is
> **present identically on every side** is **data content, not a finding**: it cannot differentiate
> the sides, and a detector firing on it has produced a **false positive under the identity control.**
> Such artefacts are **enumerated in the declaration ex ante**, with their signature; a sentinel
> claimed after a firing is not a sentinel.



*(v19 wrote criteria 2 and 3 as "no **primary** runtime finding," which let the tool's own primary/secondary classification exempt its own false positives: a finding on a clean column, or on the corrected fixture, passed the gate if the aggregator labelled it secondary. A classifier the tool controls cannot be allowed to decide what counts against it.)*

Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

<!-- v30a SC-7 — INSERT_AFTER -->

**THE CLAUSE.**

> **The gate's input surface — v30a [SC-7]**
>
> **(a) AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline
> for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9).
> **Nothing else.**
>
> **(b) IT NEVER RECEIVES, AT ANY POINT IN A GATE RUN:** the paired side or any artifact derived from
> it; the paired side's stored predictions or any statistic derived from them; **the declared
> ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it.
>
> **(c) WHY THE MAP IN PARTICULAR IS WITHHELD.** Under criterion 3 the map **is** the scoring key. A
> detector that could read it would be graded against a key it had seen, and the run would measure
> **retrieval rather than discrimination**. The map is an artifact of the harness, not an input to the
> tool. **A run that received the key has not produced a gate result, whatever it reports.**
>
> **(d) ONE SIDE AT A TIME IS A HARD SEQUENCING RULE, NOT A CONVENTION.** The criteria are per-side,
> and each is evaluated from a run that saw only its own side. **A single run given more than one side
> satisfies none of the criteria, however its outputs are partitioned afterwards.**
>
> **(e) THE SURFACE IS DECLARED AND FROZEN WITH EVERYTHING ELSE (SC-8).** Widening it — including by
> supplying a derived summary "for convenience" — is a class C amendment, not a harness detail.



**What this gate does and does not guarantee, said plainly.** It gates **discrimination**. It does **not** guarantee that the tool can prove leakage on real-world data — the previous gate did guarantee that, and this one deliberately does not. Proof capability is reported instead of required: the manifest records, per independent leaking source, whether it was detected, the highest tier reached, promotion status, the strategies that produced the finding, primary or secondary, affected cohorts, and the declaration used. From that the harness reports a **descriptive fixture proof count**, and deliberately not a rate:

> **k of N** labelled leaking sources received at least one primary PROVEN finding **attributed to that source**.

The attribution clause matters: without it a PROVEN finding on a *descendant* could be read as its source "reaching PROVEN," and a missed source would count as proven.

**It is published as a count, never as a decimal or percentage**, and it is identified as a descriptive fixture outcome rather than a performance rate. *(→ `HISTORY.md` H-07)*

**This is a rebalance, not a tightening.** The two gates are incomparable: a fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old and passes the new; a fixture detected at PROVEN throughout but with one REVIEW finding on a clean source passes the old and fails the new. The trade is deliberate — drop the irrelevant requirement that acceptance detections be proofs, add the relevant requirement that nothing shipped appears on clean or corrected material.

**Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

<!-- v30a SC-8a — INSERT_AFTER -->

**THE CLAUSE.**

> **The freeze, and what "declared ex ante" requires — v30a [SC-8]**
>
> **(a) EVERYTHING THE GATE CONSUMES FREEZES AT THE AMENDED REGISTRATION'S TAG.** At the moment the
> tag is signed, every object a gate outcome can be computed from becomes **locked**, and any
> subsequent change to any of them is a class C amendment requiring a further amended registration.
> **The declaration enumerates the frozen objects exhaustively**; an object the gate consumes and the
> enumeration omits is a defect in the enumeration, not an object outside the freeze.
>
> **(b) WHAT FREEZES IS THE OBJECT IN ITS AUDITABLE FORM — LISTS, NOT COUNTS.** A partition freezes as
> its **enumerated lists of member names**, a map as its **rows**, an exclusion as **the named unit and
> its ground**. A count is not a freeze: a count admits substitutions that a list forbids, which is the
> whole difference between a frozen partition and a frozen number.
>
> **(c) EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS.** Every declared object the gate consumes —
> the map, the partition, the exclusions, any declared cohort or restriction — must be **regenerable
> and checkable from the declared inputs alone, before any detector runs.** An object that can only be
> confirmed after a run is a description of the result, not a declaration; a cohort so confirmed is a
> key shaped by results.
>
> **(d) A SCOPE CHOICE IS JUSTIFIED INDEPENDENTLY OF ITS EFFECT ON ANY NUMBER.** Where the declaration
> restricts a scope — a class set, a cohort, a population — the justification **makes no reference to
> what the restriction does to any count, and none may be added to it.** A restriction adopted for its
> effect on a number is a restriction shaped by that number, which is the failure line 480 forbids in
> the large.
>
> **(e) A NUMBER FOUND WRONG AFTER A RESULT IS NOT CORRECTED IN PLACE.** *(Citation, not restatement:
> §0.2.1 line 99 governs.)* It is recorded, an amended registration is committed, and the affected
> benchmark is regenerated as a new version under §6.4 with the superseded results published
> alongside. **In-place correction after a result has been observed is precisely how a fail becomes a
> pass.**
>
> **(f) THE FREEZE IS ONLY AS GOOD AS THE INTEGRITY CHAIN THAT CARRIES IT.** Every file the freeze
> ranges over — **including the declaration itself, which carries the scoring key** — is hashed in the
> amended registration's tag message as committed, and the count of hashes is **derived from the set
> of registered files, never stated as a literal**. A tag that hashes the specification but not the
> declaration the specification is evaluated under is an integrity chain with a hole exactly where the
> amendment lives, and **an amendment weaker than the thing it amends is not one** (§0.2.1 line 97).



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

<!-- v30a SC-13c-2 — INSERT_AFTER -->

**INSERT AFTER (one paragraph, blank line each side):**

```

**The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a) [SC-13c(c2)].** That clause states which quantities the exception reaches and what is published for them; it governs the exception wherever this sentence is applied and is not restated here. Everywhere outside it, this sentence governs exactly as registered. The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is recorded in the v30a amendments block and is not changed by the exception.

```

> **RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT — `PREREG.md` lines 816 and 830 hold duplicated,
> conflicting authority over one state.**
>
> Line 816, verbatim: "**A combination that is `not_applicable` on every scope-eligible case in a
> body of data publishes its counts and suppresses its yields, rates, and gates**, naming the
> reason."
>
> Line 830, verbatim: "**scope-eligible** — the leakage risk logically applies to this unit. For a
> labelled feature-cohort pair this is a property of the corpus label, **not of what the detector
> could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible
> and remains in §7.2's yield denominators as a miss."
>
> For a combination `not_applicable` on every scope-eligible case in a body of data, line 830 keeps
> every labelled pair **in §7.2's yield denominators as a miss** — a yield that therefore exists and
> reads zero — while line 816 **suppresses that combination's yields, rates, and gates**. One state,
> two registered dispositions pointing in opposite directions: the §0.2.1-class duplicated-authority
> defect this registration's own structural rule exists to forbid — §0.2.1 line 77: "**Single
> normative source.** `PREREG.md` is the sole normative source for measurement semantics … A
> restated rule … is a protocol failure, not a redundancy"; §0.2.1's registry names the signature at
> line 72: "two statements, one file".
>
> **What this amendment does about it: an express, scoped exception only.** SC-13c(c2) excepts the
> quantities SC-13a–c require from line 816's suppression clause, because a gate suppressed on the
> `not_applicable`-everywhere fact is a detector waived on it (SC-12's definition, head and limb
> (iii); the declaration's §A.12 states the same definition and corroborates) and line 1035 forbids
> the waiver. Line 816's text is not edited and its publication clause is kept and required; a
> pointer to the exception is inserted at line 816's own site.
>
> **What this amendment claims for the exception, and what it does not.** The exception rests on
> this amendment's own class C authority and on the capability ground stated at SC-13b(b3). It does
> not claim the support of `PREREG.md` line 818. Line 818 states the registered rationale for line
> 816's suppression, and its applied holding for the never-applied combination's yield — that such a
> yield "is not a measurement of the tool" and that "the `not_applicable` count carries that fact
> honestly; the yield does not" — points the other way for this state. For the quantities SC-13a–c
> require, this amendment departs from that holding, expressly and on its own authority; everywhere
> else line 818 stands as registered and unchanged.
>
> **What this amendment does NOT do: resolve the conflict.** Everywhere outside SC-13a–c, lines 816
> and 830 both stand as registered and continue to point in opposite directions over the
> `not_applicable`-everywhere state. **Flagged for a future class C amendment** — the defect changes
> what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
> the state a single canonical disposition and make one of the two lines cite the other. Until that
> amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
> conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3
> and §A.12 item 5). **The operative conflict is registered-text-internal — line 816 against line
> 830.** It is not a conflict between line 816 and the declaration: declaration text on the same
> state is provisional until the tag, is at most corroboration, and cannot settle a disagreement
> between two registered lines.

> **WHAT THIS AMENDMENT DISCLOSES — seven things a reader would otherwise have to reconstruct.**
>
> **1. This amendment changes a criterion of a gate that was already signed off.** `HISTORY.md`
> **H-34**, dated **12 August 2026**, recorded the §10.1 kill-gate sign-off with the verdict *"the
> project proceeds"*. §10.1's criterion 3 is amended here, after that date. §0.2.1's ex-ante rule
> makes the **ordering** the disclosable fact.
>
> **2. The gate is harder to satisfy on net, and this is where.** §6.2 criterion 3's corrected-side
> limb moves from *silence* to *matching the declared map*, which is forced: the registered criterion
> is falsified by the fixture's own measurement (18 of 48 instrument-months carry a non-zero corrected
> count). **A contaminated-side tightening drafted alongside it is WITHDRAWN from this amendment**
> (H-39), because its reason appeared nowhere in the clause carrying it.
>
> **3. §10.1 criterion 3 has never been evaluated, for any candidate, under either text.** No
> candidate was run against either fixture side. **§9.2's comparison-set surface DID run**, on 14
> August 2026, over eight hand-written cases and eight clean paired controls — but it is committed
> nowhere, so §9.2's *"committed with this protocol"* is breached and uncurable for `prereg-v30`, and
> **§9.2 remains un-run in its registered form**. The acceptance-fixture surface was not run. The
> kill-gate verdict rests on criterion 1. Recorded at `DEVIATIONS.md` **D-003**.
>
> **4. Whether the kill gate is re-run under the amended criterion is NOT REGISTERED, and is an open
> author decision.** No clause of this amendment creates such an obligation, and H-34's own re-fire
> condition triggers on **a new tool surfacing**, not on **the criterion changing**. A reader must not
> infer that amending criterion 3 re-opens the gate.
>
> **5. The map ships; the fixture does not.** The declared ground-truth map is committed with this
> registration and is publicly reachable at the tag. **The acceptance fixture is not** — it is 64
> stored-prediction parquets per side, outside the repository, and **no clause requires publishing
> it**. So a third party can read the map, the declaration and any published reconciliation, and
> **cannot independently run a candidate against `fixture_contaminated` / `fixture_corrected`**.
> Criterion 3 is not third-party evaluable today, and this amendment does not change that.
>
> **6. §10.1 registers no third state.** *Partial satisfaction* is defined nowhere in the corpus, so a
> criterion that **could not be evaluated** is indistinguishable from one **evaluated NO**, and both
> default to proceed. Given disclosure 3, that is not hypothetical — it describes what already
> happened. **Recorded as a registration defect for a future amendment** (H-38), alongside the
> twin-criterion-5 entry; this amendment does not widen its scope to cure it.
>
> **7. Criterion 1's effective requirement REVERSES on 14 of 25 leaking-source columns, and the
> registered text of line 459 does not move.** The fixture manifest classes **25** of the 35 fed
> columns as leaking sources. Under the SC-4(b) partition **11** are REQUIRED — absence is a miss —
> while **13** are OUT OF JURISDICTION and **1** is UNSCORED, and on an OUT OF JURISDICTION column an
> availability-class finding is a **FALSE POSITIVE**. So on 14 of those 25 the gate's demand inverts:
> *absence is a miss* becomes *a finding fails the gate*. **A reader comparing v30 and v30a
> byte-for-byte at line 459 will see no change and conclude wrongly.** The narrowing is made under the
> class C rule, which permits it; §0.2.1 line 97 measures at the outcome, and at the outcome this is a
> supersession.
>
> **These seven are disclosed because the record should not have to be reverse-engineered to find
> them.** Each is verifiable from artifacts this registration commits, except where disclosure 5 says
> otherwise.



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

<!-- v30a SC-6a — REPLACE_ROW_THEN_INSERT -->

**THE CLAUSE.**

> **`unscored` — a coverage state, v30a [SC-6]**
>
> **(a) SEMANTICS.** A unit is **`unscored`** when the declaration declares, **before any detector
> runs**, that scoring it is impossible on a stated ground. An `unscored` unit **requires no finding
> and forbids none.** It **enters no denominator**, **contributes to no rate**, and **cannot be
> reported as a pass.** It is neither a pass nor a not-run: the detector may have executed perfectly
> and there is still nothing to score.
>
> **(b) ENTRY CONDITION — declared, never inferred.** A unit may be reported `unscored` **only if it
> appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector
> runs.** A unit may not enter this state because a run produced nothing, because data was missing at
> run time, or because a result was surprising. **Absence of data at run time is not `unscored`; it is
> the not-run state its cause selects** (§8.2). *(This entry condition is stated explicitly because
> §7.7's `waived` was registered without one — see SC-12.)*
>
> **(c) TWO LEVELS, AND THEY DO NOT COLLAPSE.** The state exists at the **cell** level of the declared
> map (SC-3) and at the **unit** level of the declared partition (SC-4). **A cell-level `unscored`
> never makes its unit `unscored`**, and a unit-level `unscored` does not make every cell of that unit
> unscored. A gate report states which level each `unscored` entry is at.
>
> **(d) FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored
> observations**, separately from the false-positive tally, and they carry no criterion consequence in
> either direction. **The three gate classes are never folded into one another**, and a report that
> pools them has not scored the fixture.
>
> **(e) THE PASS PROHIBITION IS ABSOLUTE.** A report that counts `unscored` units or cells as clean,
> as covered, or as passing **has converted absence of data into evidence**. `unscored` entries are
> named as unscored, never as clean, and §8.2's rule governs their display: none may be displayed in a
> way mistakable for a pass.


| **Strategy diagnostic** | `completed`, `optional_strategy_failed`, `required_strategy_failed` |

<!-- v30a SC-12p — INSERT_AFTER -->

**INSERTION TEXT — §7.7 pointer, after `PREREG.md` line 856 — Y3 §6.3.** *(MOVED INTO THIS FILE
at R80/§87. SC-12's INSERTION POINT names this pointer as applied text and said "The operative
pointer text is Y3 §6.3's" — so the applied text lived outside the source of record and this file
was INCOMPLETE. Transcribed verbatim from `Y3_WAIVED_ENTRY_CONDITION.md` §6.3, which now cites this
block as the single normative copy. **Corrected at R140/A30:** this said the same correction was
made for SC-12(w)'s own limb text. **It was not.** SC-12(w)'s limb — the entry condition itself — is
in `SCHEMA_SET_FINAL.md` and **not in this file**; the `SC-12` record's clause span stops short of it,
so it was never offered for approval. The pointer above is unaffected and is transcribed verbatim as
stated.)*

> **`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.



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

<!-- v30a SC-11a — INSERT_AFTER -->

**THE CLAUSE.**

> **The all-zero control — v30a [SC-11]**
>
> **(a) AN EMPTY AGGREGATE MUST BE PROVED EMPTY BEFORE IT MAY BE REPORTED.** Any aggregate that
> reports zero violations, zero findings, all-clean, "no cells", "no rows", or an empty result set
> **is automatically cross-checked against its source artifact before that result may be written down,
> printed, or reported.** The check is not optional, not a spot check, and not run only when the
> result looks surprising — it runs on **every** such aggregate, because a broken aggregation and a
> genuine zero are indistinguishable at the point of reading.
>
> **(b) MINIMUM SUFFICIENT FORM OF THE CHECK.** Assert that **every key the aggregation groups or
> filters on resolves to a real field with a non-empty domain in the source**, and that **the source
> is non-empty on those keys**; where a total is available by a second route, reconcile the two.
>
> **(c) ON MISMATCH THE CHECK RAISES.** It does not print a warning, does not annotate the output, and
> does not continue. **A warning next to a zero is read as a zero; an exception is not read as
> anything, which is the point.** A zero that survives the check is reportable and is reported **with
> the check named**, so a reader can tell a proved zero from an unproved one.
>
> **(d) SCOPE — THIS BINDS GATE REPORTING, NOT ONLY THE ARTIFACT THAT PROMPTED IT.** It applies
> wherever a zero or an all-clean is produced in this programme: **the gate report's per-criterion
> counts and its false-positive tallies**; any re-derivation of the declared map or of any restricted
> view of it; any per-class, per-side, per-cell or per-unit aggregation; and **any statement that a
> unit, class, cell or criterion is clean.**
>
> **(e) AN UNEXPECTED ALL-ZERO IS A FINDING, NOT A PASS.** Where a declared expectation predicts
> non-zero and the aggregate returns zero, **the zero is a finding about the aggregation or about the
> declaration — and never a pass.** It is reported as such and adjudicated before any gate outcome is
> written.
>
> **(f) A ZERO OVER A PARTIAL POPULATION IS NOT A ZERO OVER THE POPULATION.** A measured zero over a
> subset of the declared class set, the declared sides, or the declared cells **is not the same
> predicate** as a zero over the declared whole, and **no row of such a table may be quoted as a
> pass.** Every such figure names the population it is zero over.
>
> **(g) THIS COMPOSES WITH THE DISPOSITIONS ALREADY DECLARED; IT SOFTENS NONE OF THEM.** Unscored
> cells remain unscored and never clean (SC-6); excluded units remain excluded and are never reported
> as missed; the control adds only that even a reportable zero must first be shown to be a measurement
> rather than an artefact of a broken key.



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

<!-- v30a SC-6b — INSERT_AFTER -->

**INSERTION TEXT — §8.2, after `PREREG.md` line 915 — S2(i).** *(Corrected at R140/A30: this read “after marker M2 where placed”. **Marker M2 was drafted and never applied**, so the conditional was describing a neighbour that does not exist; the insertion sits directly after line 915's not-run states. **The clause below is unchanged**, and so is what it governs.)*

> **`unscored` — §7.7 (v30a) [SC-6] — is governed by this section's closing sentence as well.** It
> is neither a pass nor a not-run: this section's boundary sentence does not reach it, and its entry
> condition and semantics are SC-6's, not restated here. It is named here so that this section and
> §7.7's row cannot name different states — the closing sentence above ranges, by reference to
> §7.7's row and not to the enumeration in this section alone, over every detector-case coverage
> state that row carries other than `passed` and `failed`.



### 8.3 Three assertions

**Assertions consume unaggregated evidence, never the merged display tier.** A `ReportedFinding` collapses both combinations and takes the highest tier any of its events licenses, so a single PROVEN finding can rest on an **experimental** preserving event while carrying a **non-experimental** promoted event as corroboration. Whether that merged finding trips the assertion has three defensible readings and they disagree, so it is fixed here:

> **`assert_no_proven_leakage()` fails iff there exists an EvidenceEvent that (1) licenses PROVEN and (2) belongs to a non-experimental combination**, keyed `(detector, promotion_status)`.
>
> A `ReportedFinding` **retains the gate status of each constituent event** and carries no single inferred experimental boolean. Where its events differ, the display says so: *PROVEN — experimental preserving evidence; REVIEW — non-experimental promoted corroboration.*

Aggregation is lossy by design, and assertion eligibility is one of the facts it may not collapse. The cost is that assertion logic cannot run over the `ReportedFinding` list alone; it reads the events and the gate-status table. That is the correct cost.

- **`assert_no_proven_leakage()`** — fails per the rule above. Ignores coverage. **REVIEW findings of any basis do not trigger it**, and the report says so wherever any exist, so a passing assertion cannot be read as absence of evidence.
- **`assert_no_rule_violations()`** — fails on any RULE finding from a non-experimental detector mode. Ignores coverage.

<!-- v30a SC-12w — REPLACE_LINE -->

**OPERATIVE v30a TEXT at line 929:**

> - **`assert_audit_complete()`** — fails on any `unsupported`, `could_not_run`, or **`waived`** **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings. *(`waived` added v30a, carried with SC-12(w), whose (w1) prohibits the state outright; the assertion is what makes that prohibition checkable rather than merely stated.)*



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

<!-- v30a SC-11b — INSERT_AFTER -->

**INSERTION TEXT — §8.6, after `PREREG.md` line 961 — S2(iii).**

> **A zero, an empty result, or an all-clean statement is a published number and carries provenance
> under this section.** The control it must survive before it may be reported, and what it must name
> when it is, are stated in §7.8 (v30a) [SC-11] and govern here; they are not restated.



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

<!-- v30a SC-3-C2op — REPLACE_LINE -->

3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;


<!-- v30a SC-3-C2ret — INSERT_AFTER -->

   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired **as to its corrected-side limb only**, because that limb is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. **The contaminated-side limb and the ambiguity branch are carried into the operative item byte-identical** (R47/P1); the contaminated-side tightening an earlier draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*

4. Installs and runs through a documented public interface without author modification;
5. Has had a release or commit within the previous 12 months.

Partial satisfaction is recorded and does not trigger the stop.

### 10.2 Other kill / pause criteria


<!-- v30a SC-13a — REPLACE_LINE -->

**THE CLAUSE.**

> **2. Where the fixture is semantically ambiguous, the runtime detectors must reach a non-zero
> per-side proof yield on every detector — v30a, operative on the ambiguity branch. [SC-13a]**
>
> This criterion replaces the criterion above wherever §6.2's ambiguity branch has fired and been
> recorded in Phase 0, and it is evaluated **under the labelled hypothetical declaration that branch
> requires**, on the frozen default configuration, with the declaration's scoring key withheld from
> every detector. **SC-13b's admissibility test is applied first, before any detector runs.** The
> limbs of SC-13a and SC-13b are conjunctive, and **failure of any of them is a stop**; a criterion
> evaluated in breach of SC-13c(c4)'s execution requirement is not discharged.
>
> **(a1) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime
> scoring unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. **The
> yield is computed per runtime detector and per declared fixture side**, and each of those figures
> is published separately. *"Per detector, per side" partitions the computation; it does not
> redefine the unit, and it does not narrow the denominator — see (a3).* **This unit is a declared
> alternative to the descriptive fixture unit of §6.2**, adopted deliberately and on the record,
> because the pair is the unit proof yield is already registered in and the floor's first limb is
> stated in proof-yield terms.
>
> **(a2) THRESHOLD.** For **each** runtime detector the floor governs (the set SC-13c(c3) pins), on
> **each** declared side, the `preserving` combination's proof yield must be **strictly greater than
> zero** — `proof yield > 0`. **This is the floor of line 1035 taken literally and applied per
> detector and per side rather than once globally.** It is not a chosen number and it may not be
> tuned: there is no selection procedure to shape, which is what makes it committable before any
> development-corpus contact. **A threshold met by any route other than a preserving intervention
> reaching PROVEN under a passing determinism guard does not satisfy this limb.**
> **Every quantity this limb gates is defined and every gate it states is evaluated.** SC-13b(b2)
> requires the labelled-unit set to be non-empty on every declared side of every governed detector,
> so no denominator this limb reads is empty and no undefined yield arises; SC-13b(b3) and
> SC-13c(c2) provide that neither this gate nor the yields it reads are suppressed under `PREREG.md`
> line 816. **Each governed `(detector, preserving)` combination is executed to a terminal result on
> every declared side and reported under its actual §6.6 states — never under §7.7's `waived`
> coverage state.**
> **This limb is unconditional on every declared side, including the side the fixture declares
> corrected.** It is not scoped, softened, or suspended by any acceptance criterion, by any
> jurisdictional routing statement, or by any per-side asymmetry in the declaration. Where an
> acceptance criterion and this limb appear to disagree about the corrected side, the disagreement
> is resolved by SC-13c(c1)'s named dependency and by nothing else.
>
> **(a3) DENOMINATOR — THE REGISTERED ONE, UNNARROWED.** The yield of (a2) is computed over **the
> denominator §7.2 registers for proof yield — all scope-eligible labelled pairs — with
> scope-eligibility as §7.4 defines it, taken unnarrowed.** **This clause cites that denominator and
> does not restate it**; a second normative statement of it here would leave the registration with
> two copies of one denominator and no canonical source.
> **This clause declares no stricture on that denominator, and performs no narrowing, restriction,
> projection, exclusion, or re-aggregation of it.** The two partitions (a1) names are terms the
> registered denominator already carries and are not narrowings of it: **per detector** is §7.4's
> own scope-eligibility term read at the detector row whose metric is being computed —
> scope-eligibility being "a property of the corpus label, not of what the detector could do about
> it" — and **per side** is §7.2's body-of-data scope applied to each declared fixture side.
> **The labelled-unit set SC-13b requires is what INSTANTIATES this denominator, never what
> restricts it.** The declaration supplies which pairs the corpus labels and which detector's risk
> kind each is labelled for; that is the instance data the registered denominator is defined over.
> **A declaration may not use the enumeration to remove from the denominator a pair the corpus
> labels and the risk logically applies to** — that is a narrowing, it makes the criterion easier to
> pass, and line 1035 forbids a replacement weaker than the floor. **If a stricture on this
> denominator is ever genuinely necessary, it is declared in terms in the amendment text, justified,
> and tested against line 1035 — never introduced by a citation to a denominator it does not use. No
> other denominator is nominated.**


   **Where the fixture is semantically ambiguous** (§6.2), this criterion is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning.** *(v23 permitted it after tuning, in `DEVIATIONS.md` alone, floored only at non-zero proof yield. An acceptance criterion is a class C semantic object by §0.2.1's own definition, and choosing its unit and threshold after seeing development behaviour can determine whether Phase 2 passes. It also contradicted §7.0's invariant, which requires a metric specification to precede corpus inspection and tuning — the carve-out and the new rule could not both stand.)*

   > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

   The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

<!-- v30a SC-12 — INSERT_AFTER -->

**THE CLAUSE.** *(Generic form; H1's H7 text is compatible and is the drafting basis. The one change
from H7 is that the governed set is pinned by citation, not hard-coded and not delegated: see the
governed-set paragraph added to the clause below. SC-12 and SC-13c(c3) pin the same set to the same
registered sites and never diverge on it.)*

> **"Waived", defined — v30a [SC-12]**
>
> The floor above uses the word without a defining clause, and the word appears again as a coverage
> state in §7.7's table, also undefined. An undefined term inside a floor whose purpose is to stop
> criteria being dropped silently is exactly the term that gets read permissively later. This adds the
> defining clause.
>
> > A detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or
> > reported in any way that makes the detector's own result **incapable of changing the criterion's
> > outcome**. Concretely, a detector is waived if any of: **(i)** it is excluded from the criterion's
> > denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty
> > for a pass; **(iii)** the criterion can be satisfied by another detector's output alone; **(iv)**
> > its threshold is set at a level it meets without executing, or by construction; **(v)** its cases
> > are reported under §7.7's `waived` coverage state rather than executed to a terminal result.
>
> **Which detectors the floor governs is not the declaration's to choose.** They are the detector
> rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule
> gates — `PREREG.md` line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row,
> and line 1039's "both of L2a/L3.1's combinations" — the same registered set SC-13c(c3) pins. Where
> the fixture's declaration states the same membership, it is corroboration, not the source. The
> declaration may not shorten the set, and a criterion or report written over fewer than all of the
> governed detectors has waived the omitted ones.
>
> **What invoking it requires: nothing, because it may not be invoked.** The floor is a **prohibition,
> not a permission with conditions.** There is no procedure by which a detector the floor governs may
> be waived in a replacement criterion. A replacement that waives one is weaker than the floor and is
> out of specification on its face; **it does not become admissible by being recorded, disclosed,
> justified, or approved.** Changing that requires amending the floor itself.
>
> **What this definition does NOT permit.** (1) It is not an escape hatch of any kind and creates no
> exception, justified, approved, or time-limited. (2) It does not reach any other criterion and may
> not be cited to soften §6.2's. (3) **"Experimental" is not "waived"** — an experimental marking
> changes how findings are labelled and asserted on; it does not remove a detector from a replacement
> criterion's denominator, and a criterion that drops a detector *because* it was marked experimental
> has waived it. (4) **"No data" is not "waived"** — a cell with no data is `unscored` (SC-6), and the
> detector is still scored wherever data exists; doing at the level of a whole detector what SC-6
> forbids at the level of a cell is a waiver. (5) **A working resolution or a `DEVIATIONS.md` entry
> cannot do it** (SC-9(c), SC-9(e)). (6) **Per-combination waiving is still waiving**, and is class C.
> (7) **It licenses nothing after tuning** — a criterion chosen because it works after tuning is a
> criterion shaped by tuning.




> **(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE — a prohibition, and a closed list of licensed grounds with no members.**
>
> §7.7's table carries `waived` as a detector-case coverage state and registers no condition under which a report may assign it. It is the only state in that table without one, and the omission is not cosmetic: **no runtime metric reads a detector-case state** (§7.2.1), and `assert_audit_complete()` reads it alone. A state the apparatus cannot bound by its consequences must be bounded at entry.
>
> **The direction of the bound is forced by limb (v) above.** Limb (v) makes assignment of this state one of the ways a detector *becomes* waived. Any permissive entry condition would license, in the definition's own words, the act the definition exists to name. The bound is therefore drawn as a prohibition.
>
> **(w1) THE CONDITION. NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.** The grounds on which this state may be entered are exhaustively enumerated in this limb; the enumeration is **closed**, and it has **no members**. No ground may be inferred from silence, from practice, from a report's convenience, or from the state's presence in §7.7's table.
>
> **(w2) EVERY DETECTOR-CASE TAKES THE COVERAGE STATE ITS CAUSE ALREADY SELECTS — cited, not restated.** §7.7's completion lock selects it where a terminal result is or is not reached; §8.2 draws the boundary between the not-run states and governs their display; SC-6(b) governs a unit the declaration declared unscoreable, by name, before any detector ran. Those rules dispose of every detector-case between them, and **the residue this state would have carried is empty.**
>
> **(w3) THE STATE RECORDS A WAIVER; IT NEVER MAKES ONE — and this governs every ground ever added.** Waiving is a property of how a criterion is **written, configured, or reported** — something a criterion's design does to a detector, never something a run does to a case. The coverage state can therefore only ever be the **record** of a waiver registered text has already effected under limbs (i)-(iv); it is never that waiver's source. **A report does not create a waiver by asserting the state.** Accordingly **no ground added to (w1)'s enumeration may be constitutive**, and **limb (v) may never be a ground under (w1)**; nor may an availability declaration, a working resolution, a `DEVIATIONS.md` entry, the frozen configuration of §6.8, or an `assert_audit_complete()` recorded exception.
>
> **(w4) THE PROHIBITION BINDS PER CASE AND PER COMBINATION.** A case may not be reported `waived` on one of §7.1's combinations and executed on the other. **Per-combination waiving is still waiving** (item (6) above).
>
> **(w5) AN ENTRY THAT APPEARS IS A BREACH, AND LIMB (v) IS WHAT CLASSIFIES IT.** By limb (v) the detector is thereby waived with respect to every criterion the case feeds. Where that detector is one the floor governs and the criterion is §10.2's replacement criterion or any part of it, the replacement is weaker than the floor and out of specification on its face, and **it does not become admissible by being recorded, disclosed, justified, or approved.** Everywhere else the case has reached no terminal result, is **not complete** under §7.7's completion lock, may not be counted or displayed as complete, covered, clean, or passing (§8.2), and is re-reported in the state its cause selects — or the fixture is not scored.
>
> **(w6) THE TOKEN IS NOT STRUCK FROM §7.7's TABLE.** The state stays in the vocabulary so that a report using it is **caught** by limb (v) and by this limb rather than silently accepted. Striking the name would leave the act unnamed, and limb (v) with nothing to classify.
>
> **(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` detector-case entries, **per detector and per combination**, as a count. **That count is zero.** A report that does not publish it has not discharged this limb: a prohibition whose observance is never published is not checkable.
>
> **What this limb does NOT permit.**
>
> **(1) It licenses the state in no case, and silence is not licence.** The empty enumeration is the whole of the permission. In particular, **a criterion's failure to name a detector licenses nothing**: a criterion that enumerates its detectors and omits this one, a criterion written before this detector existed, and a criterion that says nothing about detectors at all are **all silence for this purpose**. The omitted detector **bears on that criterion**, and its cases are executed to terminal results. Reading silence as licence would be waiving by omission — limbs **(i)** and **(iii)** above — and would move the licence from registered text to whoever last failed to update an enumeration.
>
> **(2) A ground may be added only by a further class C amendment to this limb** (§0.2.1 line 93), committed and externally timestamped **before the affected detector is implemented or evaluated** (line 95), never after a fixture result is observed (§6.2 line 480; SC-8). Any such ground must be **declaratory** under (w3). **And no such amendment may license the state for a detector the floor governs at a §10.2 replacement criterion**: the floor forbids that above, there is no procedure by which it may be done, and this limb supplies none and may not be cited as one.
>
> **(3) "No data" is still not "waived"** (item (4) above), and this limb creates no route by which it becomes so. A cell with no data is `unscored` where SC-6(b)'s declared-ledger condition is met; absence of data at run time is otherwise the not-run state its cause selects (§8.2). A run that produced nothing, a missing or impossible input, a crashed or failed strategy, and a surprising result are each disposed of there and by none of them does a case enter this state.
>
> **(4) "Experimental" is still not "waived"** (item (3) above). A detector or mode shipped experimental under §10.2 criterion 3 executes its cases and reports their terminal results; the marking changes how findings are **labelled and asserted on**, never which coverage state a case takes.
>
> **(5) Jurisdiction is not waiver.** What a jurisdictional routing statement reaches is settled at SC-13c(c6), cited and not restated. A boundary on **where a finding is charged** is never a licence to leave a case **unexecuted**.
>
> **(6) It amends no other coverage state's entry condition and moves no boundary in §8.2.** It reaches §8.3 in exactly one way, deliberately: `waived` joins `assert_audit_complete()`'s failure set at line 929, so that emitting the prohibited state **fails an assertion instead of passing silently**. That is the whole of its reach into §8.3 — no other assertion changes, and no other coverage state's treatment changes. **`unscored` is not added to that failure set, and must not be**: `unscored` is a *permitted* state that honest coverage accounting produces, whereas `waived` is *prohibited* by (w1), so a report emitting it is non-conforming on its face. A prohibition no assertion tests is not enforced; a permitted state that failed an assertion would punish correct reporting.
>
> **(7) It authorises no retro-fitting.** Text adopted or amended after a run does not reach a case already run, and a licence claimed after a case was reported is not a licence.
>
> **(8) It licenses nothing after tuning** (item (7) above).
<!-- v30a SC-13b — INSERT_AFTER_RELATIVE -->

**THE CLAUSE.**

> **ADMISSIBILITY FOR THE CRITERION ABOVE — v30a [SC-13b]. Tested before any detector runs, and
> before any limb of the criterion.**
>
> **(b1) THE DECLARED SET.** A semantically ambiguous fixture may discharge the criterion above only
> if the declaration enumerates, **by name, before any run, and frozen with everything else the gate
> consumes**, a **non-empty labelled-unit set for each runtime detector the floor governs** — the
> governed set is pinned at SC-13c(c3) and is not the declaration's to choose. **If any governed
> detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is
> STOP.** The stop is lifted only by supplementing the declaration with a declared, enumerated set
> for the empty detector and re-freezing under §11's integrity chain — never by scoring the
> criterion on the remaining detector, never by suppressing the empty detector's gate, and never by
> a `DEVIATIONS.md` entry or a working resolution.
>
> **(b2) THE DECLARED SET, PER SIDE.** The set's partition by declared fixture side is itself gate
> input, and **the labelled-unit set must be non-empty in every (governed detector) × (declared
> side) cell**. A cell that is empty — a governed detector whose set is non-empty overall but empty
> on one declared side — **trips the same STOP as (b1), lifted the same way and only that way**: by
> supplementing the declaration with declared, enumerated units for that detector on that side and
> re-freezing under §11. An empty side is **nothing declared to score** on a body of data the
> criterion gates — the admissibility genus (b1) already occupies, not the threshold genus — and
> disposing it instead as a scored zero would put a defined value on an empty denominator, which
> §7.2.1's own registered rule refuses: "**Undefined, not 0% or 100%, at an empty denominator.**"
> **Consequence, stated so no reader ever decides it: every per-side denominator SC-13a(a2) reads is
> non-empty, every yield it gates is defined, and the undefined 0/0 case cannot arise.**
>
> **(b3) THE `not_applicable`-EVERYWHERE STATE — DISPOSED, NOT SUPPRESSED.** A governed combination
> that is `not_applicable` on every scope-eligible case of a declared side, over a declared
> non-empty labelled-unit set, is **not** an empty set: (b1) and (b2) do not fire, because there is
> something declared to score. Its disposition is this, in full:
> the combination is **executed and reported to terminal §6.6 states**, and its counts are published
> naming the reason — line 816's publication clause, kept and required; its labelled pairs **stay in
> the registered denominator as misses**, as §7.4 line 830 provides; its `preserving` proof yield on
> that side is therefore **zero — a defined 0/N over declared units, not a 0/0**; **zero fails
> SC-13a(a2)'s strictly-greater-than-zero threshold, and the STOP is tripped and published.**
> **SC-13a(a2)'s gate is NOT suppressed by `PREREG.md` line 816.** For the quantities the criterion
> requires, line 816's suppression clause does not apply — the express, scoped exception SC-13c(c2)
> states and the amendments block records. **The `not_applicable` finding is PUBLISHED, never
> suppressed**: the counts, the named reason, the computed zero yield, and the gate outcome are all
> published together. **The exception rests on two grounds and on no other.** *First*, it is a class
> C change to how line 816 reads at this one criterion, made on this amendment's own authority and
> recorded in the v30a amendments block (SC-13c(c2)). *Second*, this is a kill criterion over the
> detectors' capability: a combination that never applied on a declared side cannot separate the
> fixture sides, so a gate suppressed on that fact is a detector waived on it (SC-12's definition: a
> detector is waived when its result is made "incapable of changing the criterion's outcome"), and
> line 1035 forbids the waiver.
> **The two stop genera stay distinct and are never pooled**: (b1)/(b2) stop for an **admissibility
> reason** — nothing declared to score; (b3) stops through the threshold for a **detection reason**
> — declared units, terminal execution, and no proof. The two stops are reported under their own
> limbs.
>
> **(b4) WHY THIS TEST EXISTS, AND WHAT MAKES IT A TEST RATHER THAN A FORMALITY.** A detector whose
> declared labelled-unit set is empty **cannot change the criterion's outcome**, which is the
> defining condition of a waiver under the floor's own definition. Three run conditions produce an
> empty set or cell, and each is a real state of a real fixture rather than a defect:
> **(i)** the fixture contains no dependency of that detector's kind — on the affected side, none
> that reaches it — so there is nothing for the declaration to enumerate; **(ii)** the detector's
> required declaration is absent or its applicability mode is not selected, so it returns a not-run
> state on every case and the declaration has no model under which to enumerate units; **(iii)**
> every unit that could carry that detector's character is declared EXCLUDED or `unscored` on a
> stated ground, so none survives into the enumeration. **In all three the criterion is silently
> satisfiable by the other detector alone, and this clause converts that silence into a stated
> outcome.**
> **One state the superseded drafts listed as a fourth condition is not one, and is removed.** A
> declaration that assigns every unit of a detector's character to the other detector's jurisdiction
> *within the criterion's own scope* is not an independent run condition: where the risk logically
> applies to the reassigned unit, the reassignment is the narrowing SC-13a(a3) forbids in terms; and
> where it does not, the state just is condition (i). Either way it adds nothing to this list, and
> keeping it would list a prohibited act as a "real state rather than a defect".



<!-- v30a SC-13c-1 — INSERT_AFTER_RELATIVE -->

**THE CLAUSE.**

> **INTERACTIONS OF THE CRITERION ABOVE — v30a [SC-13c].**
>
> **(c1) ADOPTION, AND THE ONE NAMED DEPENDENCY — ONE WAY.** The criterion (SC-13a with SC-13b and
> this clause) is drafted against **§6.2 criterion 3 as amended by this registration** and **is not
> adoptable without that amendment**: under registered line 461 unamended, SC-13a(a2)'s
> corrected-side requirement is dischargeable only by failing §6.2 criterion 3, and a registration
> cannot contain a kill criterion dischargeable only by failing an acceptance criterion. **The
> dependency runs one way.** The criterion-3 amendment does not depend on these clauses and remains
> admissible alone; adopting it without them leaves the registration consistent, adopting them
> without it does not, and no reverse dependency is created here. Until the `prereg-v30a` tag is
> signed, line 461 stands unamended and these clauses are not adoptable at all. A `DEVIATIONS.md`
> entry or a working resolution cannot substitute for the amendment (line 1033; SC-12 item (5)).
>
> **(c2) THE LINE-816 EXCEPTION — EXPRESS, SCOPED, AND RECORDED.** `PREREG.md` line 816, verbatim:
>
> > **A combination that is `not_applicable` on every scope-eligible case in a body of data
> > publishes its counts and suppresses its yields, rates, and gates**, naming the reason.
>
> **For the quantities this criterion requires — the per-detector, per-side `preserving` proof
> yields SC-13a(a2) gates, that gate itself, and the published yields (c4) requires — line 816's
> suppression clause does not apply.** Its publication clause applies in full and is required:
> counts published, reason named, and — for this criterion — the computed yield and the gate outcome
> published with them, per SC-13b(b3). A gate suppressed on the `not_applicable`-everywhere fact is
> a detector waived on it — SC-12's definition, head and limb (iii) — and line 1035 forbids the
> waiver. **The exception rests on this amendment's class C authority and on that capability ground;
> it does not rely on `PREREG.md` line 818, whose text stands as registered.**
> **This is a class C change to how line 816 reads at this one criterion, it is recorded in the v30a
> amendments block in terms, and it reaches nothing else**: everywhere outside this criterion, line
> 816 governs exactly as registered. **The registered conflict between line 816 and line 830 is NOT
> resolved by this clause** — it is recorded in the amendments block as a duplicated-authority
> defect and flagged for a future amendment; no reading of this clause settles it anywhere else.
>
> **(c3) WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the
> detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination
> rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows (lines 759 and 760), and
> line 1039's "both of L2a/L3.1's combinations". The declaration supplies each governed detector's
> labelled-unit set; it does not supply the membership of the governed set, may not shorten it, and
> may not reach the same effect by enumerating a set for some of them and omitting the rest. **A
> declaration that enumerates a set for fewer than all of the governed detectors has not discharged
> SC-13b, and the criterion is not discharged.** SC-12, as revised with these clauses, pins the same
> set to the same registered sites, and the two clauses never diverge on it.
>
> **(c4) EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED.** Proof yield is registered for the
> `preserving` combination only. A criterion stated in proof-yield terms therefore scores one
> combination, and dropping the other from the criterion **waives that combination**. So: the other
> combination is **executed to a terminal result on the same denominator and publishes its own
> registered yield**, per detector and per side, and **no finding of that combination substitutes
> for a proof the criterion requires**. Its published yield is a required output of the criterion
> and carries no threshold of its own. Where that combination is `not_applicable` everywhere, (c2)'s
> exception covers its required published yield the same way: executed to terminal states, counts
> and reason and yield published, nothing suppressed.
>
> **(c5) THE REMAINING FLOOR LIMBS ARE CARRIED BY CITATION, AND THIS CLAUSE NAMES WHICH VERSION IT
> CARRIES.** Line 1035's second and third limbs remain in force over the criterion exactly as
> written there. **Where "criterion 3's gates" admits more than one referent, every referent is held
> in force** — they operate at different levels and do not conflict, and holding all of them is the
> only reading that is not a weakening. **Each referent is held in the version this registration
> leaves standing, and this clause says which:**
> **(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
> ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461. **Its
> scoring rule and its three dispositions are SC-3(b)'s, and **its map, its indexing, and what the
> artifact publishing it may carry are SC-3(a)'s — all held by citation and none restated here.**
> *(R49/B7: this clause previously restated (a)'s indexing triple in the same breath as declaring it
> unrestated. R47/P5 then amended (a) and left the copy behind, so the copy became DIVERGENT — it
> lacked (a)'s carve-out for artifact rows that are not cells of the map. Two normative copies of one
> rule is §0.2.1 line 77's defect; the second copy silently going stale is why.)* **The cell key is
> the declaration's to supply,
> not this clause's to state**: SC-3(a) requires that a key exist and be declared and named; SC-3(h)
> and SC-8 require it frozen with the map before any detector runs; and this clause names no key.
> **It is never the pre-amendment prohibition on any finding on the corrected fixture**, and this
> clause may not be read against that text.
> **(c5)(ii) — the §10.2 referent is §10.2 criterion 3's own two named gates**, the finding-rate
> gate and the completion gate, in force as registered and per combination, and **not amended by
> this clause**.
> **Why the version is named rather than left to the reader.** A clause whose meaning depends on
> which version of criterion 3 the reader happens to hold is the defect, not the fix: under the
> pre-amendment text SC-13a(a2)'s corrected-side requirement and criterion 3 contradict each other,
> and under the amended text they do not. **This clause states no gate of its own on this limb**; it
> adds SC-13a's threshold to the floor's first limb and SC-13b's admissibility test, and it changes
> neither of criterion 3's gates.
>
> **(c6) WHAT THE CRITERION DOES NOT REACH, AND WHAT DOES NOT REACH IT.** It is a kill/pause
> criterion over the runtime detectors. **It creates no acceptance criterion, amends none, and is
> never cited against one.** The descriptive fixture proof count of §6.2 remains descriptive and
> non-gating **for §6.2**; these clauses make proof yield gating **for this criterion only**, which
> is what line 1035's first limb already requires, and they promote no other count to a gate
> threshold. A fixture evaluated under this criterion is still evaluated under the labelled
> hypothetical declaration and **still does not carry full acceptance weight** (§6.2).
> **And in the other direction, stated because it is the collision these clauses exist to resolve:**
> a declaration statement that assigns a finding's character to a detector row and places it
> **outside an acceptance gate** does not place it outside **this** criterion, and does not remove
> that detector from the criterion's denominator, from SC-13b's admissibility test, or from
> SC-13a(a2)'s gate. **A jurisdictional routing statement written about the acceptance gate reaches
> the acceptance gate and stops there.** Removing a detector from this criterion is a waiver, and
> the floor forbids it.
>
> **(c7) WHAT THE CRITERION IS FOR, so it is not read as a quality bar.** It fires on an approach
> that is **broken**, not on one that is **incomplete**. A detector that probes few cohorts, proves
> what it probes, and publishes its coverage honestly **passes this criterion and is supposed to**;
> its limitations are reported as numbers, not converted into a stop. **Partial capability honestly
> reported is the designed outcome of this programme and is never by itself a kill condition.**


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

<!-- v30a SC-8b — INSERT_AFTER -->

**INSERTION TEXT — §11 item 8, after `PREREG.md` line 1054 (item 7) — S2(ii).** *(Item 8 is
inserted as the list's eighth item — that part stands. **Corrected at R140/A30:** this note also said
“the item-3 marker and SC-8's revised M2 follow the list; the line-97 marker is placed after line 97 in
§0.2.1”. **None of those three markers was applied**; all three were drafted and left behind. The
substance they carried is not lost — **item 8's own body below states it**, naming item 3's three names and
§0.2.1 line 97's “both” and superseding each as the set. What is missing is a marker AT those two sites,
so a reader arriving at line 97 or at item 3 is not told. **Item 8 itself is unchanged.**)*

> 8. **The freeze, and the hash set that carries it — v30a.** What freezes at an amended
> registration's tag, in what form, and what may not happen to it afterwards is stated in §6.2
> (v30a) [SC-8] and is not restated here. The tag message of this registration and of every
> amendment to it carries the SHA-256, as committed, of **every registered document and every
> registration tool** — the registration and its checking tools as item 1 names them, every document
> an amendment registers under §0.2.1 (the availability declaration included), and every file
> SC-8(f) requires hashed — **one hash beside one path, enumerated in the tag message itself.** The
> set is that enumeration and its count is read from it: no clause of this file states the count as
> a literal, and where an earlier clause names the hashed files or their number — item 3's three
> names, §0.2.1 line 97's "both" — it records the set at the time of its writing, stands as that
> record, and is superseded as the set by this item; the requirement it states stands. A registered
> file absent from the enumeration is a defect in the tag, not a file outside the chain.



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
