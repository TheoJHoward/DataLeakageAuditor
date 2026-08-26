# PHASE 1 PLAN — planning artifact

**Item F1.** Derived from `PREREG.md` as committed at signed tag `prereg-v30` (registration commit `fe0d5a5`; repo HEAD `0ee26c4`).
**Status: PLANNING ARTIFACT ONLY. No detector code, no availability-model implementation, no `audit()` surface, no corpus contact.** Nothing below is an instruction to build; it is a statement of what the registration requires, what would count as having built it correctly, and where the registered text is ambiguous enough that a decision must be taken *before* code starts.

**Source of truth.** `PREREG.md` is the sole normative source (§0.2.1, L77). `DESIGN.md` is revisable (§0.1, L26) and is quoted below only to show *where a rule lives*, never as a governing clause. `HISTORY.md` is quoted twice as causal context and is explicitly non-normative for an implementer (§0.4, L140: "it is deliberately absent from the implementer's normative input").

**Reading convention.** Every governing clause is quoted verbatim with its section number and `PREREG.md` line numbers. Nothing locked is paraphrased. Where the registration states no rule, that is said in those words rather than filled in.

---

## 0. Verifiable repository state at HEAD `0ee26c4`

Facts, not inferences — each is checkable with a read-only command:

| Fact | Evidence |
|---|---|
| Only tag present is `prereg-v30` | `git tag -l` |
| `DEVIATIONS.md` is 0 bytes | file size |
| `PARKING_LOT.md` contains exactly the §13.9 entry | file contents |
| `VALIDATED_CONFIG.toml` is the placeholder; all four `[validated.*]` sections are empty | file contents |
| `protocol/runtime_reference.py` ships and exposes all seven §11-item-1 minimum reducers | symbol scan |
| `tests/registration/` ships (`traces.py`, `test_traces.py`, `test_invariants.py`, `test_checker.py`, `EXPECTED_OUTPUTS.md`) | directory listing |
| `AVAILABILITY_DECLARATION.md` exists but is **untracked** and self-marked `## DRAFT — AUTHOR REVIEW REQUIRED` | `git status --porcelain`, file head |
| `evidence/` is untracked | `git status --porcelain` |

**Consequence, stated because it gates everything below.** At HEAD the repository records **no** Phase 0 ambiguity finding, **no** `DEVIATIONS.md` entry, and **no** amendment tag. Whether Phase 0 has formally "recorded the fixture as semantically ambiguous" in the sense of §6.2 L449 is an author determination that **cannot be verified from the repository as it stands** — the reconstruction document is untracked and marked DRAFT. This is flagged, not resolved. See §7 (Build order), precondition B0.

---

## 1. The availability model

### 1.1 What the registration requires

**The primitive (§2.2, L181–184), quoted verbatim:**

> **`a(j, c)`** — availability time of the cell at row *j*, column *c*.
> **`d(i)`** — decision time for output row *i*.
> Availability is decided by the comparator of §2.3.
> A feature is correct when it depends only on cells available to its own row.

**The comparator (§2.3, L188–197), quoted verbatim:**

L188: `**The comparator, locked:**`

L190–193:

> | `ties` | cell available to row *i* iff |
> |---|---|
> | `available` **(default)** | `a(j,c) ≤ d(i)` |
> | `unavailable` | `a(j,c) < d(i)` |

L195:

> **One comparator serves L3.1, L2a, and L3.1b**, and every place that compares an availability time to a decision time states which branch it is using (§4.3).

L197:

> **The default is `available`, on the argument of §0.3 Claim A**, which Phase 1 verifies before the detectors are built. `unavailable` remains selectable for data where the boundary instant is genuinely unusable, and it is never the default.

**The model's elements (§2.3, L199–212), quoted verbatim:**

L199: `**`AvailabilityModel`**, versioned and recorded with every result:`

> | Element | Purpose | Scope |
> |---|---|---|
> | `decision_time` | how *d(i)* derives from row *i* — bar open, bar close, offset, or a column | all runtime rows |
> | `timestamp_semantics` | whether the timestamp column is observation, event, or availability time, plus the mapping if not the last | all |
> | `column_roles` | per-column rule: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column | all |
> | `label_availability` | §2.4 | L2a, L3.1b |
> | `ties` | the comparator above | all |
> | `bar_duration` | fixed value, or inferred from successive timestamps; **at the final row the last known duration is carried forward** | roles using bar close |
> | `availability_fn` | escape hatch: user callable returning `a(j, c)` | all |
> | `panel_mask_scope` | **global, locked.** Masks are computed across all entities at a decision instant | L3.1, L2a |
> | `panel_rule_scope` | per entity (default) or global, for L3.1b's comparison; per-entity results are reported with a global check alongside | L3.1b only |
> | `embargo` | additional gap in L3.1b's comparison. **L3.1b only** — it has no meaning in a mask and is never applied to one | L3.1b only |

L214:

> The last three exist because v9's merge gave one name to two jobs. `panel_mask_scope` is locked global: per-entity masking would leave one entity's unavailable cells visible to another entity's features. `embargo` is scoped explicitly because a field silently applying to masks would change every runtime rate.

**Label availability (§2.4, L220–225), quoted verbatim:**

L220:

> > **`a(y_j) = label timestamp + label horizon + publication delay`**

L222:

> - **All three terms are user-declared, as one `label_availability` declaration.** The publication delay **defaults to zero only when the user supplies the declaration** — it is part of the user's statement, not something a profile fills in. A declaration supplying only base and horizon is complete; a missing declaration is not.

L223–225:

> - The label horizon feeds both L2a and L3.1b. It is not a separate L3.1b field.
> - **No profile may default any term.** Supplying a label column on a temporal task without a declared label availability makes L2a — and L3.1b — `unsupported`.
> - Without it the corpus is unadjudicable: §6.5 contains a lagged label that *is* realized (clean) and one that is *not yet* realized (leaking), and only a declared horizon separates them.

**The non-temporal policy (§2.5, L231–233), quoted verbatim:**

L231:

> > **`labels_available_during_feature_construction`** — a required boolean when a label column is supplied on a non-temporal task. It is a declaration in its own right, not a field of `AvailabilityModel`, because there is no time for an availability model to describe.

L233:

> `false` means the user asserts that no label was legitimately available while features were built, and L2a runs in the narrowed non-temporal mode. `true` — or absent — makes L2a `unsupported`, naming this policy as the missing element. The tool declines to judge legitimate label use rather than guessing at it.

**Cohort scope of silence (§2.6, L241–244), quoted verbatim:**

> - **A change at any row with `d(i) ≤ d` is a valid finding.** Those cells were unavailable to *i* as well, under either tie convention.
> - **Silence is informative only for the cohort `d(i) = d`.**

L244:

> Consequences, locked: the scoring unit is **feature × affected output cohort**, deduplicated across probes, strategies, and runs (§7.2); a labelled pair counts as a miss only when no valid probe found it; any reach inference derives from availability-boundary refinement (§8.5).

**Undeclared → unsupported (§2.7, L248), quoted verbatim:**

> If the required declaration is neither supplied nor defaulted, **L3.1, L2a, and L3.1b return `unsupported`** (§8.2), naming the missing element. They do not fall back to row order.

L252:

> **Non-temporal path.** Absence of a timestamp column — not absence of a declaration — selects it. There L3.1 is `not_applicable` and L2a runs only under the policy of §2.5.

### 1.2 Acceptance condition

The Phase 1 gate is the **only** per-phase acceptance statement in the registration. §10, L992, quoted verbatim (gate column):

> §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed

**The gate names no acceptance test for the availability model as such.** The nearest registered acceptance conditions are indirect, and are all verification-of-claims conditions:

§0.3, L123–128, quoted verbatim:

> **Verification is a Phase 1 gate item** (§10.0), performed before L3.1 and L2a are built, against these cases at minimum:
>
> 1. A **mixed frame** — a label column with a declared horizon alongside a joined, forward-filled column whose availability follows its source timestamp. This is where v8 died and is the thinnest part of the specification.
> 2. A cell whose availability equals the decision instant exactly, under both `ties` settings.
> 3. A feature reading exactly one unavailable cell, with the expected reach of one bar.
> 4. A centered window, with the expected reach of about half the window plus one bar.

And a CI consistency check, §6.8, L649, quoted verbatim (relevant clause):

> that the `ties` comparator is consistent across §2.3, §4.3, and the shipped mask

which is explicitly **deferred past registration**, §6.8, L647:

> Two of the checks below cannot pass before detector code exists — shipping defaults against the frozen `[validated.runtime]`, and the `ties` comparator against the shipped mask — while §11 requires the checker in the first commit. So it takes `--stage prereg | implementation | release`, **every stage prints the checks it defers and the stage that owns them**, and an omitted branch is a failure rather than a pass.

**Finding — stated because the task asks for it explicitly.** The registration states **no acceptance condition for the availability model itself**. It states an acceptance condition for the *claims the model rests on* (§0.3 items 1–2 via §10.0 step 2) and a deferred CI consistency check on one field (`ties`). There is no registered test that the model correctly computes `a(j,c)` for `at_bar_close`, `at_source_timestamp`, `always`, an explicit availability column, or `availability_fn`. The conformance suite (§7.8) is the natural home for that and is frozen at Phase 1 — but §7.8 L885 describes its purpose as declaration-conformance, not `a(j,c)` correctness:

> The conformance suite contains identical pipelines under a too-permissive and a too-strict declaration. Its purpose is to check that the tool implements the declaration it was given — including deliberately wrong ones, and both `ties` branches.

### 1.3 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §0.1 lock table row 1 | L34 | availability per cell is the primitive; matrix construction is revisable |
| §0.1 lock table row 2 | L35 | comparator + default locked; mask construction revisable |
| §0.1 lock table row 3 | L36 | silence extends only to the decision cohort |
| §0.1 lock table row 8 | L41 | undeclared → `unsupported`; profile resolution revisable |
| §0.1 | L28, L30, L44, L46 | the lock test; probe mechanics live in `DESIGN.md`; CI checks the lock table's own pointers; anything decision-affecting is serialized |
| §0.2.1 | L77, L79 | single normative source; no field answers two questions |
| §0.3 Claim A | L117 | the default is argued, not verified |
| §0.3 verification list | L123–128 | items 1–2 bind the model |
| §2.2 | L181–184 | `a(j,c)`, `d(i)`, correctness definition |
| §2.3 | L188–216 | comparator table, default, model elements, scoping, profile defaults |
| §2.4 | L220–225 | `label_availability` |
| §2.5 | L229–233 | non-temporal policy |
| §2.6 | L237–244 | valid finding / cohort silence / scoring unit |
| §2.7 | L248–252 | undeclared → unsupported; non-temporal path selection |
| §2.8 | L256–266 | every finding is conditional on the declaration; what must be printed |
| §4.3 | L348–357 | the same comparator, as inequalities, for L3.1b |
| §5.3 registry 12, 13 | L410, L411 | the structural limits this creates |
| §6.5 | L510, L512 | case families the model must adjudicate |
| §6.8 | L633, L635, L647, L649 | serialization of the complete model incl. `ties`; staged CI |
| §10.0 | L1007–1010 | verification precedes the freeze of the comparator |
| §10, Phase 1 row | L992 | deliverable and gate |

### 1.4 Ambiguity flags

**AM-1 — `bar_duration` "inferred from successive timestamps" has no stated basis. (Class B)**
§2.3, L208: "`bar_duration` | fixed value, or inferred from successive timestamps; **at the final row the last known duration is carried forward** | roles using bar close".
Readings: **(a)** successive *rows* — `ts[j+1] − ts[j]` over row order; **(b)** successive *distinct timestamps* — the gap on the unique-timestamp lattice. On panel data these differ and (a) yields zero-duration bars for every entity sharing an instant, which collapses `at_bar_close` onto `at_timestamp` and changes findings at the boundary. §2.3 L210 locks `panel_mask_scope` global, so panel data is explicitly in scope for masks; the registration never reconciles that with (a). Decision-affecting: changes `a(j,c)` and therefore detector decisions, so §6.8 L633 reaches it.

**AM-2 — `availability_fn`'s relation to `column_roles` is unstated, and the two files disagree on what it is. (Class B; the `DESIGN.md` half is Class A)**
§2.3, L209 lists `availability_fn` as a **top-level model element**, "escape hatch: user callable returning `a(j, c)`", scope "all". §2.3, L205 enumerates `column_roles` values as exactly five: "`at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column" — `availability_fn` is not among them. `DESIGN.md` §2.1, L61–68 lists `availability_fn` as a **sixth `column_roles` value**.
Readings on precedence when both are supplied: **(a)** `availability_fn` overrides all roles; **(b)** it fills only columns with no role; **(c)** supplying both is rejected. The registration states none of the three. The `DESIGN.md`/`PREREG.md` divergence on whether it is a role at all is separately mechanical (Class A, `DESIGN.md`-side, since `DESIGN.md` is revisable).

**AM-3 — `timestamp_semantics`' "mapping" has no stated form. (Class B)**
§2.3, L204: "whether the timestamp column is observation, event, or availability time, plus the mapping if not the last".
Readings: **(a)** a fixed offset; **(b)** a user callable; **(c)** a named column. The mapping determines `a(j,c)` for every column, so this is decision-affecting and §6.8 L635's "the complete `AvailabilityModel` of §2.3" requires it serialized — but a callable is not serializable in the sense the rest of that list assumes.

**AM-4 — "versioned" is asserted without a versioning rule. (Class B)**
§2.3, L199: "**`AvailabilityModel`**, versioned and recorded with every result". No clause states how the version is formed or what changes bump it.
Readings: **(a)** a user-supplied string; **(b)** a content hash of the serialized declaration; **(c)** the `VALIDATED_CONFIG` section hash of §6.8 L633. Matters because §8.6 L961 requires every published number to name "the availability declaration in force", and §2.8 L266 requires the declaration to be "in `VALIDATED_CONFIG` with every published rate".

**AM-5 — the "label timestamp" term of `a(y_j)` has no enumerated domain. (Class B)**
§2.4, L220: "**`a(y_j) = label timestamp + label horizon + publication delay`**"; L222: "A declaration supplying only base and horizon is complete".
Readings on what "base"/"label timestamp" may be: **(a)** the frame's timestamp column only; **(b)** any declared column; **(c)** a literal instant. §2.4 L224 forbids profiles defaulting any term but does not bound the term's domain. Interacts with AM-2: if the base may be an arbitrary column, `label_availability` partly duplicates `at_source_timestamp`.

---

## 2. Profiles

### 2.1 What the registration requires

The registration says four things about profiles, and only four. All are quoted verbatim.

§2.3, L216:

> Profiles supply defaults (`DESIGN.md`). No profile supplies `label_availability` (§2.4) or the non-temporal policy of §2.5.

§2.4, L224:

> - **No profile may default any term.** Supplying a label column on a temporal task without a declared label availability makes L2a — and L3.1b — `unsupported`.

§0.1 lock table, L41 — the row that declares profile resolution **revisable**:

> | Undeclared availability → `unsupported`, never pass | §2.7 | how declarations resolve from profiles |

§6.8, L635 — the only profile element the registration requires serialized (excerpt of the non-exhaustive list):

> profile interval exclusions

Two supporting statements, both non-mechanism:

§5.2, L388: "- **Needs a per-column availability declaration, including a label horizon no profile will guess.**"
§5.1, L383 (excerpt): "missed session gaps (profile intervals)".

**The deliverable and the gate.** §10, L992 lists Phase 1's work as, verbatim: "Availability model and profiles; …". §10, L998 lists Phase 7's work and gate, verbatim:

> | **7** | Profiles, docs, v1.0 | 1–2 wknds | `futures` and `generic` profiles ship |

The two named profiles and their contents exist only in `DESIGN.md` §1.2 (L46–53), which is revisable.

### 2.2 Acceptance condition

**None is stated for Phase 1.** The Phase 1 gate (§10, L992, quoted in full in §1.2 above) does not mention profiles. The only registered profile acceptance condition is Phase 7's, §10, L998: "`futures` and `generic` profiles ship" — six phases later.

**This is a finding.** Profiles are a named Phase 1 deliverable with no Phase 1 acceptance condition, and their only acceptance condition anywhere is a shipping statement attached to the last phase.

Two negative acceptance conditions *are* registered, and are checkable at Phase 1 without any detector:

- §2.3, L216: a profile that supplies `label_availability` or the §2.5 policy violates the registration.
- §2.4, L224: a profile that defaults any of the three `a(y_j)` terms violates the registration.

### 2.3 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §0.1 lock table row 8 | L41 | profile→declaration resolution is `DESIGN.md`'s, subject to §2.7's outcome |
| §0.1 | L46 | any `DESIGN.md` element changing a decision/tier/eligibility/probe location is serialized |
| §2.3 | L216 | profiles supply defaults; two exclusions |
| §2.4 | L222, L224 | no profile may default any `label_availability` term |
| §2.5 | L231, L233 | the non-temporal policy is not a profile-supplied field |
| §2.7 | L248 | "neither supplied nor defaulted" → `unsupported` |
| §4.1 | L333 | per-row declaration requirements |
| §5.1, §5.2 | L383, L388 | profile intervals; no profile guesses a horizon |
| §6.8 | L633, L635 | profile interval exclusions serialized |
| §10 Phase 1 / Phase 7 | L992, L998 | the deliverable and the only stated acceptance |
| §12 | L1076 | declaration burden |

### 2.4 Ambiguity flags

**PR-1 — Phase 1 "profiles" versus Phase 7 "Profiles". (Class B)**
§10 L992 assigns "profiles" to Phase 1; §10 L998 assigns "Profiles" to Phase 7 with the gate "`futures` and `generic` profiles ship".
Readings: **(a)** Phase 1 builds the profile *mechanism* (how a profile resolves into an `AvailabilityModel`) and Phase 7 authors and ships the two named profiles; **(b)** Phase 1 builds mechanism *and* both profiles, Phase 7 only documents and polishes; **(c)** Phase 1's "profiles" means only the profile *schema* the availability model needs, with no resolution logic.
Material, because §6.2 L457 requires the fixture gate to run "on the **frozen default configuration**", and whether a profile is part of that frozen configuration at Phase 2 depends on which reading holds. Note the counter-consideration inside the registration: §6.2 L447 says the fixture declaration is "**reconstructed, not chosen**", which may mean the fixture path needs no profile at all.

**PR-2 — which model elements a profile may default is stated only negatively. (Class B)**
§2.3 L216 excludes exactly two things ("`label_availability` … or the non-temporal policy of §2.5"). §2.7 L248's phrase "neither supplied nor defaulted" makes a profile-defaulted element count as declared, so the exclusion list is the entire boundary between `unsupported` and a running detector.
Readings: **(a)** everything except the two named exclusions may be profile-defaulted, including `ties`, `panel_mask_scope`, `panel_rule_scope`, `embargo`, `bar_duration`, `timestamp_semantics`, `availability_fn`; **(b)** only elements a domain profile can genuinely know (`decision_time`, `column_roles`, `bar_duration`, `ties`) may be defaulted, and the rest must be user-supplied.
Under (a) a profile could default `embargo`, which §2.3 L212 restricts to L3.1b and L214 warns about specifically ("a field silently applying to masks would change every runtime rate"). Decision-affecting via §2.7.

**PR-3 — "profile interval exclusions" is a serialized configuration item with no registered definition. (Class B)**
§6.8 L635 requires "profile interval exclusions" in `VALIDATED_CONFIG`; §5.1 L383 calls them "profile intervals"; no clause defines what an interval exclusion is or what it excludes.
Readings: **(a)** intervals excluded from *cohort selection* (so no probe cohort falls in a session gap); **(b)** intervals excluded from the *availability matrix* (cells inside them treated specially); **(c)** both. Under (a) this is Phase 2 work (cohort selection is a Phase 2 deliverable per §10 L993) and Phase 1 only needs the schema; under (b) it is Phase 1 availability-model work. The phase assignment turns on the reading.

---

## 3. The four controls, in their locked order

### 3.1 What the registration requires

**First, the set — and the number.** The registration says **three** controls plus a separate guard. §6.11, L671 heading `### 6.11 Control runs`, L673 verbatim:

> Three, all before any real probe. Failures are recorded per §7.7's two-level scheme, never as findings:

and §10, L992 lists the Phase 1 deliverable verbatim as "… the three controls and the determinism guard". The "four" of this item is therefore `{determinism guard, alignment equivalence, identity perturbation, compatibility}`. That four-way split is independently supported by §7.5, L841, which counts them as four separate diagnostics, verbatim:

> Per **detector × strategy × promotion status**: **eligible cases, completed cases, optional-strategy failures, required-strategy failures, alignment-equivalence failures, compatibility failures, determinism failures, control artifacts, correct primary findings, false findings.**

and by §8.2, L915's reason codes, verbatim:

> Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`.

**The determinism guard (§6.10, L657–667), quoted verbatim:**

L657:

> L2a and L3.1 compare by **bitwise equality under a passing determinism guard** (§6.9). There is no second regime in v0.1.

L659:

> **The guard runs on every execution frame, not once.** A pipeline can be deterministic on its original integer frame and nondeterministic on a promoted float or complex branch. With a single original-frame guard, that pipeline passes, and a promoted run then reports a difference caused by nondeterminism as though it were caused by intervention — corrupting evidence yield, false-alarm rates, completion rates, strategy diagnostics, and the fixture result.

L661:

> > **Each distinct execution frame carries its own determinism guard**: the original frame for preserving runs, and each promoted alignment family for the strategies that use it.

L663:

> > **A frame that fails its guard produces no runtime finding.** It is recorded as `could_not_run(determinism)` for the strategies assigned to it. There is no routing decision, no fallback, and no configuration parameter selecting between outcomes.

L665:

> Case-level consequences follow from §7.7's required-or-optional machinery rather than from a separate rule: an original-frame failure reaches every preserving strategy, so the detector-case normally becomes `could_not_run(determinism)`; an optional promoted family's failure is a diagnostic that leaves a preserving proof untouched.

L667: "**`assert_audit_complete()` fails on any such entry.** A user who accepts the gap records an explicit exception (§8.3)."

**Control 1 — alignment equivalence (§6.11, L675–684), quoted verbatim:**

L675:

> 1. **Alignment equivalence.** Dtype alignment promotes the frame and recomputes the baseline, which removes promotion artifacts between probe arms but risks a different problem: the aligned pipeline may take different code paths than the user's. So: run the original baseline, run the aligned baseline unperturbed, and require equivalence.

L677–680:

> **The comparator is per column, not blanket:**
> - Where the original and aligned output columns have **the same dtype**, require byte equality directly.
> - Where they **differ**, the ordered pair (original dtype → aligned dtype) must appear in that strategy's **permitted promotion set**, and byte equality is required after promoting the original column to the aligned dtype.
> - **Any dtype difference outside the permitted set is divergence**, and that strategy is `could_not_run(alignment)`.

L684: "Genuine path divergence changes values, not just representation, and still fails. No tolerance is introduced; permitted promotion sets are serialized into `VALIDATED_CONFIG`."

Its epistemic limit, §3.2, L295: "The alignment control (§6.11) establishes that the original and aligned pipelines agree **on the unperturbed baseline**. That is a single-point check. It does not establish that they agree **under perturbation**, which is what the probe's conclusion rests on."

**Control 2 — identity perturbation (§6.11, L686), quoted verbatim in full:**

> 2. **Identity perturbation** — replace unavailable cells with an exact copy of themselves. Any delta is measurement artifact. On the aligned frame, once per alignment family.

**Control 3 — compatibility (§6.11, L687–703), quoted verbatim:**

L687:

> 3. **Compatibility, checked on every perturbed execution rather than once per strategy.** Confirm output shape and index match the baseline. A pipeline that drops rows under the NaN strategy returns a shorter frame, and every comparison after that is meaningless, including ones that look clean.

L689:

> **Compatibility is mask-dependent, so a single check cannot stand in for the probes.** L3.1 perturbs many columns and L2a perturbs only the label; early and late cohorts mask different cells; a mask that puts NaNs into a column feeding row-dropping logic behaves differently from one that does not.

L691:

> > There is no separate compatibility run. Every perturbed execution validates shape and index against the baseline before its result is used. A failure discards that probe's result.

L695:

> > **A cohort counts as probed for a combination when at least one strategy of that combination validly executed it.** The unprobed reclassification applies at the combination level only when **none** did. Strategy-level failures remain §7.5 diagnostics and never reach §7.2's rates directly.

L697:

> **Strategy-level escalation to `could_not_run(compatibility)`** uses a **failure fraction with a minimum absolute count**: the strategy is incompatible for the detector-case when `f ≥ m` **and** `f / n > q`, where `f` is failed perturbed executions, `n` is attempted eligible probes for that detector × case × strategy, aggregated by actual promotion status for publication (§7.5), and `m`, `q` come from `VALIDATED_CONFIG`.

L701: "**Escalation is prospective.** EvidenceEvents from a strategy's valid executions *before* it escalated stand and are scored; the escalated state governs coverage from that point forward. A strategy does not retroactively un-probe cohorts it validly executed."

L703:

> **Locked at Phase 1:** the fraction-plus-minimum form, the denominator, how failures after a terminal finding are handled, the candidate ranges for `m` and `q`, and the objective used to select them. **Chosen on the development corpus and frozen with the matching `VALIDATED_CONFIG` section:** the values. **`m` and `q` are not selected to keep completion above §10.2's 60% floor** — the objective balances false silence, probe loss, and detector-case failure on their own terms, and the floor remains a downstream kill gate rather than a target.

### 3.2 The order — what is actually locked, and by which clause

**The task asks for "the four controls IN THEIR LOCKED ORDER (name the order and the clause that locks it)". The honest answer is that `PREREG.md` does not lock a four-element execution order.** What it locks is:

| # | What is locked | Clause | Lines |
|---|---|---|---|
| 1 | The three §6.11 controls all precede any real probe | §6.11 preamble | L673 — "Three, all before any real probe." |
| 2 | Identity perturbation runs **on the aligned frame** — which entails alignment first | §6.11 control 2 | L686 — "On the aligned frame, once per alignment family." |
| 3 | The guard is per execution frame, and a failing frame yields nothing | §6.10 | L661, L663 |
| 4 | Compatibility is **not** a pre-probe step at all — it rides every perturbed execution | §6.11 control 3 | L691 — "There is no separate compatibility run." |
| 5 | A **reason precedence** for reporting `incomplete(reason)` — explicitly not an execution order | §6.6 | L574 — "**Reason precedence when strategies fail differently:** `determinism`, then `alignment`, then `compatibility`, then `control_artifact`, then `crash`." |

**The execution order that is usually cited — guard → alignment equivalence → identity → probe (with compatibility per execution) — is stated only in `DESIGN.md` §4.6, L337–351, which is revisable.** `DESIGN.md` L355 states its rationale: "*The guard precedes every comparison-based control*, because it licenses the comparison the alignment control performs." `HISTORY.md` H-32 (L253, non-normative) records the consequence of getting it wrong: a nondeterministic pipeline "died with reason `alignment`, never reached the guard, and thereby made the frozen routing policy unreachable, `PREREG.md` §7.5's determinism counts structurally zero, and §6.5's stochastic case unable to produce its own locked expected outcome."

So the ordering demonstrably moves §7.5's published per-strategy counts and can make a §6.5 locked expected outcome unreachable — and it lives in the revisable file. Whether that is a defect turns on §0.1's own test, L28, verbatim:

> If changing it would make a past result look better than it was, it is locked here. If changing it is just engineering, it goes in `DESIGN.md`.

against §0.1 L30, verbatim:

> Probe mechanics live in `DESIGN.md`, because through v9 they were specified in this file and were wrong three versions running. What is locked here is the requirement, not the mechanism

This is flagged as CT-1 below rather than adjudicated here.

### 3.3 Acceptance condition

The Phase 1 gate (§10, L992) names exactly one control-related acceptance condition, verbatim:

> **all four alignment-control cases behave as §6.5 requires**

and §6.5, L525–529 supplies those four cases, verbatim:

> **Alignment-control cases** (all four behaviourally identical after promotion except the last):
> - integer-typed outputs — **must pass**;
> - outputs propagating complex dtype — **must pass**;
> - **an internally generated integer column that never touches a promoted input — must pass** (§6.10);
> - a pipeline genuinely branching on integer versus float dtype — **must fail.**

Cross-referenced by §0.3 verification item 8, L132, verbatim:

> 8. **The per-column alignment comparator of §6.11** against three pipelines: one with integer-typed outputs, one whose outputs propagate complex dtype, and one emitting an internally generated integer column that never touches a promoted input. All three are behaviourally identical after promotion and **all three must pass.** A fourth pipeline that genuinely branches on integer versus float dtype **must fail.**

And §0.3 items 6–7, L130–131, verbatim:

> 6. **Per-frame determinism** (§6.10) — a pipeline deterministic on an integer frame and nondeterministic on its promoted complex branch must be caught by the promoted family's own guard, not reported as an exact-mode finding.
> 7. **Mask-dependent compatibility** (§6.10) — a pipeline whose row-dropping depends on which columns are masked must fail compatibility on the probes that trip it and pass on the ones that do not, rather than being decided once per strategy.

**Finding.** Acceptance is registered for **two** of the four (alignment equivalence, via four named cases with locked verdicts; the determinism guard, via §0.3 item 6) and **one and a half** more indirectly (compatibility, via §0.3 item 7's behaviour statement — but with no case-family entry pinning its expected verdict the way the alignment four are pinned). **The identity control has no registered acceptance condition at all.** §6.2 L462 requires the fixture to be "Silent under the identity control on both", which is a Phase 2 fixture criterion, not a Phase 1 control test; §6.5 lists no identity-control case family.

### 3.4 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §0.1 | L28, L30, L46 | the lock test; probe mechanics revisable; decision-affecting elements serialized |
| §0.2.1 | L77, L91–93, L101–107 | single source; class A/B/C definitions and the citation requirement |
| §0.3 items 6, 7, 8 | L130–132 | the three mechanical facts the controls assume |
| §0.3 closing | L134, L136 | "Items 6 through 8 are the mechanical facts that §6.2, §6.9, and §6.10 currently assume" |
| §3.1 | L289 | a frame failing its guard is `could_not_run(determinism)` |
| §3.2 | L295, L297, L301 | the alignment control's epistemic limit; per-strategy-per-frame promotion |
| §6.6 | L574, L598 | reason precedence; optional/required does not reach the resolvers |
| §6.6 | L608 | the compatibility denominator must be well-defined pre-tag |
| §6.8 | L635 | permitted promotion sets, guard repetition count, compatibility/equivalence failure behaviour all serialized |
| §6.9 | L653 | bitwise equality, not tolerance |
| §6.10 | L657–667 | the guard, per frame, no fallback |
| §6.11 | L671–703 | all three controls and the escalation rule |
| §7.5 | L841, L843 | the four failure counters, keyed by promotion status |
| §7.7 | L855–868 | the two-level state scheme failures are recorded under |
| §8.2 | L915 | reason codes |
| §8.4 | L939 | the determinism remedy is first-class report text |
| §6.5 | L515, L525–529 | the stochastic case and the four alignment cases |
| §6.2 | L462 | fixture must be silent under the identity control |
| §10 Phase 1 | L992 | deliverable and the one control acceptance condition |

### 3.5 Ambiguity flags

**CT-1 — no execution order for the four is locked in `PREREG.md`, and the order that exists is decision-affecting. (Class B)**
Readings: **(a)** §6.11's numbering (1 alignment → 2 identity → 3 compatibility) *is* the locked order, with the guard prepended by §6.10; **(b)** no order is locked — only the entailments of §3.2 above bind, and the sequence is `DESIGN.md` engineering; **(c)** §6.6 L574's reason precedence (`determinism` → `alignment` → `compatibility` → `control_artifact`) is the intended order, and §6.11's numbering is incidental.
(a) and (c) disagree about where the identity control sits: §6.11 numbers it **second**, §6.6's precedence puts `control_artifact` **fourth**. The disagreement is not merely cosmetic, because §7.5 L841 keeps *separate counters* for alignment-equivalence failures, compatibility failures, determinism failures and control artifacts — and unlike `incomplete(reason)`, those counters are not precedence-normalized, so a pipeline failing two controls contributes to whichever counter its implementation reached first. Under §0.1 L46 that makes the order a `VALIDATED_CONFIG` item at minimum.

**CT-2 — "Three, all before any real probe" is contradicted by control 3's own block quote. (Class A, with class-C risk)**
§6.11 L673 says all three run before any real probe; §6.11 L691 says "There is no separate compatibility run. Every perturbed execution validates shape and index against the baseline before its result is used."
Readings: **(a)** the preamble is editing residue from before the v16 fix and the block quote governs — compatibility is per-execution and not a pre-probe control, so "three, all before any real probe" is literally false for one of the three; **(b)** both hold — a pre-probe compatibility check *and* per-execution validation.
(b) is directly contradicted by L691's "no separate compatibility run", so (a) is near-certain; the flag exists because the contradicted sentence is in the **locked** file. Class-C risk: under (b) a standalone pre-probe check would add attempts to `n`, the compatibility denominator of §6.11 L697, changing a published escalation threshold's denominator — and §6.6 L608 asserts that denominator is well-defined pre-tag precisely because §0.2.1 class B requires it.

**CT-3 — the identity control's mask is unspecified. (Class B)**
§6.11 L686: "replace unavailable cells with an exact copy of themselves … On the aligned frame, once per alignment family." Once per family, but "unavailable cells" is cohort-relative — every cohort has a different unavailable set — and the clause does not say which cohort's mask the single run uses.
Readings: **(a)** the first selected eligible cohort's mask; **(b)** the union over all selected cohorts (the largest unavailable set); **(c)** a placement with an empty mask.
Decision-affecting: `could_not_run(control_artifact)` is a detector-case outcome under §8.2 L915 and a §7.5 counter, and a pipeline can be artifact-free under one mask and not another for exactly the reason §6.11 L689 gives about compatibility. Note that `DESIGN.md` §4.4 L329 offers a mechanism ("or place the cohort past the end of the data") that has no counterpart in `PREREG.md`; under §0.1 L30 that is legitimately mechanism, but it does not settle which of (a)–(c) the registration intends.

**CT-4 — §6.11 L703 defers the compatibility objective to Phase 1, while §0.2.1 L92 makes an already-fixed objective a precondition of class B membership. (Class B, with high class-C risk)**
§6.11 L703: "**Locked at Phase 1:** the fraction-plus-minimum form, the denominator, how failures after a terminal finding are handled, the candidate ranges for `m` and `q`, and the objective used to select them."
§0.2.1 L92, verbatim: "| **B — parameters under a locked procedure** | A value chosen where the form, search space, objective, denominator, and freeze point are already fixed | select on the development corpus and freeze | the compatibility fraction and its minimum count; cohort count; strategy order |".
The candidate ranges for `m` and `q` and the objective appear **nowhere in `PREREG.md`**. Readings: **(a)** "Locked at Phase 1" means Phase 1 must *author and freeze* them — in which case, at the moment they are authored, the objective is not "already fixed" and the compatibility fraction fails §0.2.1's own class B precondition, despite being §0.2.1 L92's own worked example; **(b)** the objective *is* fixed by L703's final sentence ("the objective balances false silence, probe loss, and detector-case failure on their own terms") and Phase 1 only instantiates it — in which case the "objective" is a three-term balance with no stated weighting, and the weighting becomes the free parameter.
Under §0.2.1 L107 ("A post-tag finding that cannot cite a stated assumption is not in class A or B. It is a specification defect."), reading (a) routes this to a specification defect and, if it changes what the escalation threshold means, to class C.

---

## 4. The detector protocol

### 4.1 What the registration requires

**The phrase "detector protocol" appears exactly once in `PREREG.md`** — in the Phase 1 work column, §10, L992: "… evaluation generator and conformance suite frozen; **detector protocol**; report skeleton; …". There is no section defining it, and no other occurrence.

What therefore governs it is the set of locked obligations any detector must satisfy. All quoted verbatim.

**The two scoring records (§7.2, L778–787):**

L778–781:

> | Unit | Key | Drives |
> |---|---|---|
> | **EvidenceEvent** | `(detector, promotion_status, feature, affected output cohort)` **within a case**; corpus-level records additionally carry case identity | every combination-specific metric in §7.1 |
> | **ReportedFinding** | `(detector, feature, affected output cohort)` | user-facing display; carries the highest tier its events justify |

L783:

> An EvidenceEvent is created once per combination that produced the pair, so a pair found by a preserving run and a promoting run yields two events — counted in the preserving and promoted rows respectively — and one ReportedFinding at PROVEN with the promoting event recorded as corroboration.

L785:

> **Within a single combination, probe cohorts, strategies, and repeated runs are corroborating evidence, not additional events.** A pair found by three probes and two preserving strategies is one EvidenceEvent, one true positive.

**The combination trace obligation (§6.6, L549–566), quoted verbatim in the parts that bind a detector:**

L549–554:

> > **Two fields, keyed `(detector, promotion_status, case)`, because schedule and evidence are independent axes:**
> >
> > | Field | Values |
> > |---|---|
> > | **`schedule_state`** | `not_applicable`, `unsupported`, `completed`, `incomplete(reason)`, `short_circuited` |
> > | **`evidence_outcome`** | `finding`, `observed_silence`, `none` |

L562:

> > **"Every combination" means both promotion statuses, always.** §3.1's axis is closed and two-valued, so a case has exactly two combinations regardless of which strategies the frozen configuration happens to resolve on it. A combination on which nothing resolves is traced `not_applicable`, explicitly. **Enforcement may not depend on the configuration or on what happened**

L564:

> > **Every labelled case carries an explicit trace for every combination.** A combination with no trace has no state, and silently skipping it drops the case from that combination's denominators — which inflates its yields and shrinks §10.2's *N*. … **A missing trace is a protocol violation and must raise, never default.**

L566:

> > **Execution eligibility, per combination:** a combination is execution-eligible for a case when **at least one configured strategy resolves to that promotion status on that case** and has all required inputs. This is per case rather than per configuration because `noise`, `nan`, and `constant` preserve on some frames and promote on others (§3.2).

**Tier is not the detector's to assign (§3.1, L284–286), quoted verbatim:**

> | `promotion_status` | Tier | Label |
> |---|---|---|
> | `preserving` | **PROVEN** | — |
> | `promoted` | REVIEW | `dtype_promoted` |

**The reducer is canonical (§6.6.1, L620), quoted verbatim:**

> **A runtime metric is published only if the reference reducer computes it.** A number named here but absent from the reducer does not exist and may not appear in the README, a post, or an application.

and L622:

> **This file stays normative and the reducer is checked against it.** The reducer's requirement IDs are diffed against these sections in CI. Neither is hand-maintained against the other in both directions — a second normative source is the defect this version exists to remove, and a reference implementation is only safe while it is downstream.

**No learned component (§6.12, L707), quoted verbatim:**

> > No learned component may produce a PROVEN or RULE finding. PROVEN findings arise only from runtime intervention compared by exact equality on a dtype-preserving run. RULE findings arise only from deterministic declared rules. REVIEW screens may fit auxiliary statistical or predictive models, and where they do, the model class, seed, training data, parameters, and output are reported with the finding.

**The eleven rows and their inputs** are §4's coverage map, L311–323 (the `Needs` column is the detector-protocol `requires` contract in substance), with §4.1 L333, verbatim:

> - **Declaration requirements, per row:** L3.1 and L3.1b require an `AvailabilityModel`. **Temporal L2a** requires one including `label_availability`; **non-temporal L2a** requires the §2.5 policy and no availability model at all. L1.2 requires neither (§2.7).

### 4.2 Acceptance condition

**None is stated.** The Phase 1 gate (§10, L992) does not mention the detector protocol. There is no clause anywhere in `PREREG.md` saying what a correct detector protocol looks like or how it would be checked.

The nearest registered checks are all about the **reducer**, which already ships at the tag — §6.6.1, L614, verbatim:

> `protocol/runtime_reference.py` ships in the tag as protocol tooling, not detector implementation. **It exists and its suite is green; the tag remains blocked on that staying true.**

and its invariants, §6.6.1 L616, verbatim (excerpt):

> **Mechanical invariants the suite asserts:** exactly one `schedule_state` and one `evidence_outcome` per trace; every emitted pair legal under §6.6's table; every conditional numerator a subset of its denominator; every rate in [0, 1]; every gate deterministic; **no runtime metric accessing the detector-case state**

**This is a finding.** The detector protocol is a named Phase 1 deliverable whose only registered acceptance surface belongs to a component (the reducer) that was already delivered at registration.

### 4.3 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §0.1 lock table rows 6, 7 | L39, L40 | canonical scoring unit and dedup; completion and tier-aware termination |
| §3.1 | L284–289, L291 | promotion status → tier; the non-runtime REVIEW label |
| §3.2 | L301–303 | promotion is per strategy per frame; corroboration rule |
| §4 coverage map | L311–323 | the eleven rows, their kinds, methods, and required inputs |
| §4.1 | L331, L333 | per-row tier and declaration requirements |
| §4.2 | L340–344 | L2a's two modes; `unsupported` naming a covering detector |
| §4.4 | L361–371 | L1.2's confirmation, and that it has no REVIEW output mode |
| §6.6 | L549–604 | the combination trace contract in full |
| §6.6.1 | L612–622 | the reducer is canonical and downstream |
| §6.12 | L707 | no learned component licenses PROVEN or RULE |
| §7.2 | L778–787 | the two records and their keys |
| §7.5 | L841, L843 | per-strategy diagnostics; promotion status is a key, not a field |
| §7.7 | L855–868, L875 | detector-case states; tier-aware termination; denominator membership |
| §8.2 | L915 | `unsupported` vs `could_not_run` boundary |
| §11 item 1 | L1048 | the seven minimum reducer symbols that ship at the tag |
| §10 Phase 1 | L992 | the deliverable |

### 4.4 Ambiguity flags

**DP-1 — "detector protocol" is named as a deliverable and defined nowhere. (Class B)**
Readings: **(a)** it means the Python typing `Protocol` of `DESIGN.md` §6 L402–406 (`id`, `requires`, `scope_applies`, `run`) — in which case the deliverable is entirely `DESIGN.md`-governed and `PREREG.md` contributes only the constraints in §4.3 above; **(b)** it means the normative contract itself — what a detector may and may not decide (it emits EvidenceEvents; it never assigns its own tier, `schedule_state`, or `evidence_outcome`); **(c)** both, with (a) as the surface and (b) as the invariant set.
Material because under (a) the whole deliverable is revisable and needs no registration discipline, while under (b) parts of it are already locked in §7.2/§6.6/§3.1 and an implementation that deviates is a protocol failure rather than a design change.

**DP-2 — the registration never says who constructs a `CombinationTrace`. (Class B)**
§6.6 L562 requires a trace for **both** promotion statuses on **every** labelled case, "regardless of which strategies the frozen configuration happens to resolve on it", and L564 makes a missing trace "a protocol violation [that] must raise, never default". A combination on which *nothing resolves* must still be traced `not_applicable` — so something must emit a trace for a combination that never ran.
Readings: **(a)** the detector emits per-execution records and the *harness* enumerates the two combinations per case and builds traces — the only reading under which a never-run combination gets a trace without the detector being invoked for it; **(b)** the detector emits traces directly, and must therefore be invoked once per combination even when no strategy resolves; **(c)** the reducer synthesizes missing traces — contradicted by L564's "must raise, never default".
Decision-affecting: the choice determines whether trace completeness is enforceable at all, which §6.6 L564 says flipped a gate verdict during the build ("The build demonstrated a gate verdict flipping on trace omission alone").

**DP-3 — `resolve_tier` is named by `DESIGN.md` as a canonical reducer import but is not among §11 item 1's minimum symbols and is not a top-level symbol in the shipped reducer. (Class A, `DESIGN.md`-side)**
§11 item 1, L1048, lists verbatim: "**at minimum** `resolve_schedule_state`, `resolve_evidence_outcome`, `derive_evidence_events`, `derive_reported_findings`, `compute_runtime_metrics`, `apply_runtime_gates`, and `evaluate_runtime_assertions`". `DESIGN.md` §6, L411–415 imports `resolve_tier`, `resolve_schedule_state`, `resolve_evidence_outcome` from `leakaudit.protocol`.
Verified observation, offered as fact: a symbol scan of `protocol/runtime_reference.py` shows no top-level `resolve_tier`; tier is assigned inside `derive_reported_findings` (`tier = "PROVEN" if any(c.event.licenses_proven ...)`).
Readings: **(a)** no defect — §11's list is a minimum, `leakaudit.protocol` is the future package rather than the shipped reference file, and §3.1's rule is a two-row table that any component may apply; **(b)** `DESIGN.md` names a canonical reducer the registration does not require to exist, so a detector written against `DESIGN.md` imports a symbol with no registered definition. **Whether (a) or (b) holds is genuinely undetermined from the documents and is labelled as such**; the underlying scan result is verified.

---

## 5. The report skeleton

### 5.1 What the registration requires

**The phrase "report skeleton" appears exactly once** — §10, L992, in Phase 1's work column. §8 supplies the obligations. All quoted verbatim.

§8.1, L909 heading `### 8.1 The report never says a pipeline is clean`, L911:

> It says which detectors ran, in which mode, under which configuration and declaration, **which decision cohorts were probed and what fraction of rows they cover**, and what they found.

§8.2, L915:

> Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. None may be displayed in a way mistakable for a pass.

§8.3, L919:

> **Assertions consume unaggregated evidence, never the merged display tier.** A `ReportedFinding` collapses both combinations and takes the highest tier any of its events licenses, so a single PROVEN finding can rest on an **experimental** preserving event while carrying a **non-experimental** promoted event as corroboration. Whether that merged finding trips the assertion has three defensible readings and they disagree, so it is fixed here:

§8.3, L921–923:

> > **`assert_no_proven_leakage()` fails iff there exists an EvidenceEvent that (1) licenses PROVEN and (2) belongs to a non-experimental combination**, keyed `(detector, promotion_status)`.
> >
> > A `ReportedFinding` **retains the gate status of each constituent event** and carries no single inferred experimental boolean. Where its events differ, the display says so: *PROVEN — experimental preserving evidence; REVIEW — non-experimental promoted corroboration.*

§8.3, L927–929:

> - **`assert_no_proven_leakage()`** — fails per the rule above. Ignores coverage. **REVIEW findings of any basis do not trigger it**, and the report says so wherever any exist, so a passing assertion cannot be read as absence of evidence.
> - **`assert_no_rule_violations()`** — fails on any RULE finding from a non-experimental detector mode. Ignores coverage.
> - **`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings.

§8.3, L931:

> `assert_audit_complete()` accepts an allow-list of **explicit recorded exceptions** — no cryptographic signature mechanism is specified and the word "signed" is not used. Each carries detector entry, mode, reason, scope, date, and configuration hash, and all are printed in the report.

§8.4, L935–941:

> - **Every L2a and L3.1 finding prints the availability declaration it was evaluated under, its promotion status, its probe cohort, and its affected output cohort.** A `dtype_promoted` finding names the promotion that occurred and states that no preserving run reproduced it. A `dtype_promoted` finding names the promotion that occurred and states plainly that a preserving run did not reproduce it.
> - **Every L1.2 PROVEN finding prints the split declaration, the perturbed test population, the fitted state or training output that changed, and the attribution evidence.** L1.2 has no availability declaration to print.
> - RULE findings state their declared semantics, including which `ties` branch of §4.3 they applied.

L939:

> **A `could_not_run(determinism)` entry carries its remedy, in the report, as first-class text.** It names the columns that differed between runs and states the two user-side fixes — seed the pipeline, or run it single-threaded for the audit — rather than leaving them in a design note.

L941: "**A partial cohort count is not weak evidence.** Permutation strategies can leave the decisive cell fixed (Claim C, registry 14), so "found in 18 of 20 cohorts" is the expected shape of a real leak and the report says so."

§8.5, L949–953 (the reach display rules), verbatim:

> - **A reach value is reported only from a full scan over the candidate availability boundaries present in the data**, and is described as the latest boundary at which a change was observed — not as the latest cell the feature depends on.
> - **A binary-searched reach is reported as a lower bound and is never labelled exact.**
> - **Above the cap, the capped subset is not scanned at all.** When the complete candidate count exceeds the frozen grid cap of §12, the lower-bound procedure runs instead and `reach_basis = lower_bound` is serialized.
> - **Whether refinement runs at all is the frozen `reach_refinement_policy`**, not a property of `full` or `quick`.
> - **The word `exact` refers to the scan, not to the dependency**, and no reach claim asserts exactness of a black-box pipeline's dependency structure.

L957: "A reach claim appears only when refinement produced it, marked as scanned or as a lower bound. Where refinement did not run, no reach and no fix suggestion is printed."

§8.6, L961:

> Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval, the availability declaration in force, and — for runtime rows — the probed-cohort count and row coverage. Non-holdout author-produced numbers say so in the same line.

**Display-form constraints from elsewhere**, verbatim:

§6.2, L476: "**It is published as a count, never as a decimal or percentage**, and it is identified as a descriptive fixture outcome rather than a performance rate."
§7.2.1, L820: "**Each is published as a count over all cases for that combination** — numerator and denominator, per §6.6.1's `MetricValue` shape — so it reads as a proportion; that is the count, not a rate derived from a filtered denominator."
§7.8, L889: "- **Per-case pass/fail results are published. No aggregate conformance rate is published, ever**".
§5.4, L425 — the prohibited-claims list, which binds report text: "**Never:** "catches 95% of data leakage." … Any coverage claim implying whole-pipeline rather than per-cohort silence. Any conformance percentage (§7.8). Any suggestion that a nondeterministic pipeline receives graded evidence (§6.10). Any PROVEN claim resting on a promoting-only run (§3.2)."

### 5.2 Acceptance condition

**None is stated for Phase 1.** The Phase 1 gate (§10, L992) does not mention the report. §8's guarantees are written as guarantees, not as tests, and no clause states how compliance with them would be demonstrated.

Two acceptance-adjacent conditions exist but belong to other phases: §6.6.1 L616's reducer invariants include the two §8.3 experimental-status cases ("an experimental preserving event with a non-experimental promoted event on the same pair must **not** trip `assert_no_proven_leakage()`, and the inverse must trip it") — already discharged at the tag — and §10 Phase 3's gate, L994: "A stranger can install and run it".

**This is a finding**, and it is the third of three: the availability model, the detector protocol, and the report skeleton are all Phase 1 deliverables with no Phase 1 acceptance condition. Of Phase 1's eight named deliverables, the gate at L992 speaks to four (§10.0 ordering, claim verification, fixture AUC reproduction, alignment-control cases, snapshot hashing).

### 5.3 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §2.8 | L266 | every L2a/L3.1 finding prints its declaration and cohorts |
| §3.1 | L291 | the `domain_judgment` label for non-runtime REVIEW rows |
| §5.3 entry 15 | L414 | the report must carry the determinism remedy |
| §5.4 | L419–425 | what v0.1 may claim, and the "Never" list |
| §6.1 | L441 | fixture publishes provenance, not accuracy |
| §6.2 | L470–476 | the descriptive fixture proof count, as `k of N`, never a decimal |
| §7.2.1 | L810, L816, L818, L820 | undefined-at-empty-denominator; suppression; counts as num/den |
| §7.7 | L858, L870–875 | assertion input; clean-case rates never quoted singly |
| §7.8 | L889, L890 | per-case results, no aggregate rate |
| §7.10 | L900–903 | every published rate carries interval and *n* |
| §8.1–§8.6 | L909–961 | the whole reporting contract |
| §10.2 criterion 3 | L1036 | experimental labelling wherever findings appear |
| §11 item 1 | L1048 | `evaluate_runtime_assertions` ships as protocol tooling |
| §10 Phase 1 | L992 | the deliverable |

### 5.4 Ambiguity flags

**RS-1 — what "skeleton" means at Phase 1. (Class B)**
Several §8 obligations reference values that cannot exist until Phase 2 (probed-cohort count and row coverage, §8.1 L911; reach and `reach_basis`, §8.5 L949; per-strategy diagnostics, §7.5).
Readings: **(a)** skeleton = the report's field and method surface with every §8 guarantee enforced structurally (states cannot render as a pass; counts render as numerator/denominator; reach fields exist but are suppressed) and no runtime content; **(b)** skeleton = a working report over the controls and the guard only — which is exactly what Phase 1 produces; **(c)** skeleton = the JSON schema and nothing rendered.
Material for what Phase 1's own gate would even mean, and for whether the report skeleton is inside or outside the Phase 2 configuration freeze.

**RS-2 — §8.4 L935 states the same requirement twice, in two wordings. (Class A)**
Verbatim, L935: "A `dtype_promoted` finding names the promotion that occurred and states that no preserving run reproduced it. A `dtype_promoted` finding names the promotion that occurred and states plainly that a preserving run did not reproduce it."
Readings: **(a)** editing residue — one requirement, duplicated, and either wording discharges it; **(b)** two requirements — the first mandates the content, the second mandates that it be stated *plainly*, i.e. a register constraint on the wording.
Mechanical, and consequential only for whether a checker should look for one clause or two. Flagged because it is in the locked file and §0.2.1's own diagnosis is that duplicated statements drift.

**RS-3 — `waived` is an enumerated detector-case state with no defining clause. (Class B)**
`waived` occurs exactly twice in `PREREG.md` and never in `DESIGN.md`. §7.7, L855, verbatim: "| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |". §10.2, L1035, verbatim (excerpt): "The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force."
Nothing states what produces a `waived` state, what it means, or how `assert_audit_complete()` treats it — §8.3 L929 names only `unsupported` and `could_not_run` as failing that assertion, so on a literal reading a `waived` entry passes it.
Readings: **(a)** `waived` *is* the §8.3 L931 recorded-exception mechanism reaching the coverage table — a `could_not_run` entry the user has explicitly excepted; **(b)** a distinct user-set state meaning "this detector was deliberately not requested"; **(c)** vestigial, with no production rule.
Under (a) and (c) `assert_audit_complete()` behaves as written; under (b) a detector could be silently waived out of the assertion. It also directly conditions §10.2 criterion 2's replacement floor at L1035 — the amendment currently in preparation — so the reading is load-bearing for v30a, not only for Phase 1.

**RS-4 — the report's control fields compress per-frame results into scalars. (Class A, `DESIGN.md`-side)**
`DESIGN.md` §8 L516 lists `determinism_check_passed`, `alignment_equivalence_passed`, `identity_control_passed` as `AuditReport` fields. §6.10 L661 makes the guard per execution frame, and §6.11 L686 makes the identity control per alignment family — so on a run with F frames there are F guard results and one identity result per family, and a scalar boolean cannot carry them.
Readings: **(a)** the booleans are summaries and the per-frame detail lives in `strategy_diagnostics` (§7.5) — harmless; **(b)** they are the storage and the per-frame detail is lost, which is §0.2.1 L79's failure ("**No field answers two questions.**") applied to a frame axis rather than a semantic one.
`DESIGN.md`-side and revisable either way; flagged because §7.5 L841 requires determinism failures to be counted per detector × strategy × promotion status, which a run-level boolean cannot reconstruct.

---

## 6. The padded slicer

### 6.1 What the registration requires

**`PREREG.md` states two things about the padded slicer, and no padding rule.** Both quoted verbatim, in full.

§6.2, L451:

> - **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

§10, L992 — the Phase 1 work entry names it, and the gate names the reproduction requirement:

> … fixture harness and manifest; **padded slicer**; evaluation generator and conformance suite frozen; …
> … both fixture AUCs reproduce within ±0.010, full and sliced; …

Two supporting mentions, neither a rule:

§5.1, L383 (excerpt): "Slow runtime (parallelize, `quick` mode, padded slicing)".
§13, L1091: "4. Whether the CME fixture ships in the repo, full or sliced — **CME redistribution terms must be checked.** Blocks the Phase 3 release."

And the reference values the sliced variant must reproduce, §6.2, L445:

> - **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

**The padding rule itself exists only in `DESIGN.md` §5.3, L393**, quoted here to identify its location, not as a governing clause:

> Slicing shifts window warmup, manufacturing artifacts at the head and masking leakage deeper in. **Any slice carries padding of at least the maximum window length before the first probed cohort**, present in the data, excluded from probing, and reported. Where the maximum window is unknown, `audit()` requires `max_window=`; a slice without declared padding is refused, not silently run.

**The general rule that may or may not reach it**, §6.8, L633, verbatim:

> > **Every parameter capable of changing a detector decision, a tier assignment, execution eligibility, probe location, or strategy compatibility is serialized into, and hashed with, the applicable `VALIDATED_CONFIG` section.**

§6.8's non-exhaustive list at L635 does **not** name padding or `max_window`.

### 6.2 Acceptance condition

The registration states one, in the Phase 1 gate, §10, L992, verbatim:

> both fixture AUCs reproduce within ±0.010, full and sliced

This is the **only** registered acceptance condition for the padded slicer, and it is an acceptance condition on the *fixture's* reproduced AUCs rather than on the slicer's padding behaviour. There is no registered test that padding is present, that it equals or exceeds the maximum window length, that it is excluded from probing, or that a slice without declared padding is refused — every one of those requirements lives in the revisable file.

`DESIGN.md` §5.3 L395 asserts a self-test relationship ("The same slicer produces the CI variant of the acceptance fixture, so the padding rule is exercised by the project's own tests"), which is the mechanism `PREREG.md` §6.2 L451 requires — but exercising a rule is not the same as a stated pass condition, and `PREREG.md` states none.

### 6.3 Governing clause list

| Clause | Lines | What it constrains |
|---|---|---|
| §0.1 | L28, L30, L46 | the lock test; probe mechanics revisable; probe-location parameters serialized |
| §5.1 | L383 | padded slicing is named as an engineering mitigation |
| §6.2 | L445 | reference AUCs, ±0.010, `full` mode |
| §6.2 | L451 | one slicer serves the CI variant and user-facing slice auditing |
| §6.8 | L633 | anything changing probe location is serialized and hashed |
| §10 Phase 1 | L992 | deliverable; the full-and-sliced reproduction gate |
| §13 item 4 | L1091 | whether the fixture ships full or sliced — open, blocks Phase 3 |

Note the absence: no clause in §2 (availability), §6.5 (case families), §7 (metrics), or §8 (reporting) mentions slicing, padding, or `max_window`.

### 6.4 Ambiguity flags

**PS-1 — the padding rule is not in the registration, and §0.1's own test arguably locks it. (Class B, with class-C risk)**
Readings: **(a)** padding is probe mechanics, and §0.1 L30 puts probe mechanics in `DESIGN.md` — correctly revisable, with §6.8 L633 requiring only that the resulting parameter be serialized; **(b)** padding determines which cohorts are probed on a sliced run, so under §0.1 L28's test ("If changing it would make a past result look better than it was, it is locked here") it belongs in `PREREG.md` and is missing. A concrete instance of (b): §6.2 L461's criterion 3 requires "**No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`" — shortening padding moves the first probed cohort into the warmup region, where §5.3-style head artifacts live, and can flip that criterion.
Consequence if (b): `max_window` / padding length must be frozen in `[validated.runtime]` before the Phase 2 fixture run, per §6.8 L633.

**PS-2 — padding is specified (in `DESIGN.md`) as "the maximum window length" with no unit. (Class B)**
Readings: **(a)** rows — the count a `rolling(60)` consumes; **(b)** elapsed time — the span a `rolling('60s')` consumes.
On a regular lattice these coincide; on an irregular one they do not, and the acceptance fixture's lattice is irregular (Phase 0 spike evidence records intra-day re-anchor gaps stretching same-day windows to 30m45s, and same-second rows on some instrument-months — cited as **context from untracked Phase 0 work, not as a registered fact**). Under (a) a time-based rolling window is under-padded; under (b) a row-based one is over-padded, costing probed cohorts. Decision-affecting via probe location.

**PS-3 — what the sliced fixture's ±0.010 is measured against. (Class B)**
§10 L992 requires "both fixture AUCs reproduce within ±0.010, full and sliced"; §6.2 L445 gives one pair of reference AUCs (0.957 and 0.675) and no separate sliced reference.
Readings: **(a)** the sliced variant must reproduce the *same* 0.957/0.675 within ±0.010 — a substantive constraint on slice size and placement, since AUC is a property of the original experiment's model on the retained population, and the registration nowhere constrains the slice so as to make this achievable; **(b)** each variant reproduces its own reference, and the sliced reference is established during Phase 1 — in which case a reference established during the phase it gates is not an ex-ante criterion; **(c)** "full and sliced" modifies the *audit* rather than the AUC, i.e. both audits run and the AUC check applies once.
Load-bearing: (a) makes the Phase 1 gate potentially unsatisfiable by construction; (b) makes it self-referential.

**PS-4 — "full" carries at least four distinct senses in the registration. (Class A)**
`full` mode (§6.2 L445, "The gate runs in `full` mode"; §12 L1072, "the full audit"); full **data** vs sliced (§10 L992; §13 L1091); `full_scan` reach basis (§8.5 L951; §6.6.1 L616); "full refinement" (§0.3 L119, "full refinement scans the frozen candidate grid").
Readings for §10 L992's "full and sliced": **(a)** data extent, contrasted with the sliced variant — near-certain from the context "both fixture AUCs reproduce … full and sliced"; **(b)** audit mode. Under (b) it would conflict with §6.2 L445's "The gate runs in `full` mode", which would then be redundant. Mechanical and low-stakes, but it is the term on which PS-3's reading partly turns, so it is worth fixing in the same pass.

---

## 7. Build order

### 7.1 What the registration says must happen in what order

**The phase sequence**, §10, L989–999 (the gate column of each row is the phase's acceptance condition). Phase 1's row, L992, verbatim:

> | **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |

**Phase 1's internal ordering**, §10.0, L1004–1014, quoted verbatim in full:

> ### 10.0 Phase 1 internal ordering, locked
>
> 0. **If Phase 0 recorded the fixture as semantically ambiguous, the class C amendment of §10.2 is committed and timestamped before anything below — including any development-corpus access.**
> 1. Write the throwaway mechanical tests for the §0.3 verification list.
> 2. Verify Claims A–C and the comparator cases.
> 3. Record the result. A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration; **a class C change requires an amended registration committed and timestamped before step 4** (§0.2.1).
> 4. Freeze the final comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, and reach definitions.
> 5. Generate and hash the evaluation-generator snapshot.
> 6. Generate and hash the conformance suite.
>
> Steps 5 and 6 may not precede step 4. A snapshot frozen out of order is discarded and regenerated, and the discard is a `DEVIATIONS.md` entry.

**Reinforcing ordering clauses**, quoted verbatim:

§6.4, L497:

> 1. **Freeze the evaluation generator in Phase 1** — code *and* parameter distributions — as an immutable snapshot with its own version and hash, **after Claims A–C are resolved** (§10.0). Any change is a deviation and creates a new benchmark version.

§6.4, L506:

> **The conformance suite** is generated from the same frozen snapshot at Phase 1, after Claims A–C resolve, and hashed then. It is deliberately **visible during implementation** — see §7.8.

§0.3, L123 (excerpt): "**Verification is a Phase 1 gate item** (§10.0), performed before L3.1 and L2a are built".

§0.3, L134:

> Items 6 through 8 are the mechanical facts that §6.2, §6.9, and §6.10 currently assume. Each locked rule names its assumption; if measurement contradicts it, the rule is rewritten through `DEVIATIONS.md` before the detectors that depend on it are built (§10.0).

§6.7, L628:

> - **Hand-authored cases are written, frozen, and hashed before implementation of the detector they test**, and are labelled **non-holdout author-created results** wherever they appear. Writing them after seeing detector behaviour is a protocol failure.

§10.2 criterion 2, L1033 (the replacement-criterion rule, which conditions all of Phase 1 when triggered):

> > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

§6.2, L480 (Phase 2's ordering, stated here because it constrains what Phase 1 may leave unfrozen):

> **Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

§7.0, L745 (the module invariant; binds Phases 4–6, and is quoted because it fixes what "before" means):

> > **The invariant:** a phase module's complete metric specification is committed and timestamped **before** that phase's development-corpus inspection, hand-authored case writing, adjudication-rubric writing, wrapped-tool output inspection, default tuning, detector implementation, and partition generation. **No detector row ships without its module tag predating its code.**

### 7.2 The resulting order for Phase 1

Stated as the registration states it, with each step's governing clause. Nothing is added.

| Step | Action | Governing clause |
|---|---|---|
| **B0** | If Phase 0 recorded the fixture as semantically ambiguous: commit and externally timestamp the class C amendment carrying the complete replacement criterion — unit, threshold, denominator — **before anything else, including any development-corpus access** | §10.0 step 0, L1006; §10.2 criterion 2, L1033; §0.2.1 L95, L97 |
| **B1** | Write the throwaway mechanical tests for the §0.3 verification list (items 1–8, L125–132) | §10.0 step 1, L1007 |
| **B2** | Verify Claims A–C and the §6.10 comparator cases | §10.0 step 2, L1008; §0.3 L123 |
| **B3** | Record the result; apply class A/B outcomes to `DEVIATIONS.md` and the frozen configuration; a class C outcome requires an amended registration committed and timestamped **before B4** | §10.0 step 3, L1009; §0.3 L136 |
| **B4** | Freeze the final comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, and reach definitions | §10.0 step 4, L1010 |
| **B5** | Generate and hash the evaluation-generator snapshot — code *and* parameter distributions | §10.0 step 5, L1011; §6.4 L497 |
| **B6** | Generate and hash the conformance suite, from the same frozen snapshot | §10.0 step 6, L1012; §6.4 L506 |

**Hard constraint on B5/B6**, §10.0 L1014, verbatim: "Steps 5 and 6 may not precede step 4. A snapshot frozen out of order is discarded and regenerated, and the discard is a `DEVIATIONS.md` entry."

**Where the other six Phase 1 deliverables sit is not stated.** §10.0's six steps cover verification and freezing. The availability model, profiles, fixture harness and manifest, padded slicer, detector protocol, report skeleton, the three controls and the determinism guard are named in §10's work column (L992) and placed nowhere in §10.0's locked ordering. Two ordering facts about them *are* derivable from other clauses and are quoted rather than inferred:

- The controls and guard must exist by B2, because §0.3 items 6–8 (L130–132) are verification cases *about* the guard, the alignment comparator, and mask-dependent compatibility, and §10.0 step 2 verifies them.
- L3.1 and L2a must **not** exist before B2, per §0.3 L123: "performed before L3.1 and L2a are built".

### 7.3 What must not exist yet — the prohibitions, quoted

**§11 item 1, L1048** (excerpt), verbatim:

> **The first commit contains the registration and its checking tools, and no detector implementation:** `PREREG.md` (locked, unchanged), `DESIGN.md`, **`HISTORY.md`**, an empty append-only `DEVIATIONS.md`, a `PARKING_LOT.md` **containing only the §13.9 entry**, a placeholder `VALIDATED_CONFIG.toml`, **`tools/check_registration.py`** carrying §6.8's checks plus the single-source and banned-vocabulary scans, **`protocol/runtime_reference.py`** — pure, non-detector reducers … and **`tests/registration/`** …

**Scope note, stated because it is easy to over-read.** This prohibition binds **the first commit**, which is `fe0d5a5` and has already occurred. It is a satisfied historical constraint, not a standing bar on Phase 1 implementation. The clause continues, L1048: "protocol tooling is not detector implementation, and residue defenses absent from the registered repository are not reproducible from it."

**The prohibitions that are live during Phase 1**, each quoted verbatim:

| Prohibition | Clause | Text |
|---|---|---|
| L3.1 and L2a must not be built before Claims A–C are verified | §0.3, L123 | "performed before L3.1 and L2a are built" |
| No development-corpus access until the §10.0 step 0 branch is resolved | §10.2, L1033 | "no development-corpus access until the branch is resolved (§10.0)" |
| Snapshot and conformance suite must not be generated before the step-4 freeze | §10.0, L1014 | "Steps 5 and 6 may not precede step 4." |
| A class C change must not be implemented before its amended registration is committed and timestamped | §0.2.1, L95 | "**Class C requires an amended registration**, committed and externally timestamped **before the affected detector is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md` entry standing alone." |
| Hand-authored cases must not be written after seeing detector behaviour | §6.7, L628 | "Writing them after seeing detector behaviour is a protocol failure." |
| The statistical fallback must not be built | §13.9, L1097 | "**The statistical fallback is not built and is not pre-registered for v0.1.**" |
| No second comparison regime | §6.10, L657 | "There is no second regime in v0.1." |
| No routing/fallback parameter on determinism failure | §6.10, L663 | "There is no routing decision, no fallback, and no configuration parameter selecting between outcomes." |
| No learned component may license PROVEN or RULE | §6.12, L707 | "No learned component may produce a PROVEN or RULE finding." |
| No measurement formula, state enumeration, or denominator definition in `DESIGN.md` | §0.2.1, L77 | "the CI script fails on any measurement formula, state enumeration, or denominator definition appearing outside this file" |
| No runtime metric may read the detector-case state | §7.2.1, L820 | "**No runtime metric reads the detector-case state of §7.7**, which exists for `assert_audit_complete()` alone." |
| No runtime metric may be published that the reference reducer does not compute | §6.6.1, L620 | "**A runtime metric is published only if the reference reducer computes it.**" |
| Defaults may not be altered after observing a fixture result | §6.2, L480 | "Defaults may not be altered after observing a fixture result." |
| Banned vocabulary must not appear outside the declared exemptions | §6.8, L637–638 | "the CI script fails if any appears outside §0.4, the `DESIGN.md` lessons, or `PARKING_LOT.md`. … Current banned terms: `capability matrix`, `noise floor`, `routing policy`, `comparison_mode`, `statistical mode`, `substituted gate`." |

### 7.4 Precondition B0 — status

**B0 is the gate on everything else and its trigger condition cannot be verified from the repository.** §10.0 L1006's trigger is "**If** Phase 0 recorded the fixture as semantically ambiguous"; §6.2 L449 defines the finding: "**If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.**"

At HEAD `0ee26c4`: `DEVIATIONS.md` is empty, no amendment tag exists, and the reconstruction document is untracked and self-marked DRAFT. **Whether Phase 0 has made this recording is an author determination that the repository does not evidence.** Per the task's framing a class C amendment (`v30a`) is in preparation covering the acceptance fixture, which is consistent with the trigger having fired — but consistency is not the record, and §10.2 L1033 requires the amendment "committed and timestamped" before Phase 1 begins, which has not happened at HEAD.

**Planning consequence: every item in this plan is downstream of B0. No Phase 1 step below B0 may begin, and no development corpus may be touched, until the amendment is committed and externally timestamped.**

---

## 8. Consolidated ambiguity table

Class column uses the task's framing: **A** = mechanical or typographic; **B** = clarification needed before code. The final column records where `PREREG.md` §0.2.1's *own* class definitions (L91–93) and its citation requirement (L101–107) would route the item differently — because a class-C item cannot be settled in a planning chat at all: §0.2.1 L95 requires an amended, timestamped registration **before the affected detector is implemented or evaluated**.

| # | Item | Ambiguity | Candidate readings | Class | §0.2.1 routing risk |
|---|---|---|---|---|---|
| **AM-1** | Availability model | `bar_duration` "inferred from successive timestamps" — no basis stated | (a) successive rows; (b) successive distinct timestamps on the lattice | B | Low — but changes `a(j,c)` on panel data, so C if the resolution adds a branch |
| **AM-2** | Availability model | `availability_fn` vs `column_roles` precedence unstated; `DESIGN.md` lists it as a role, `PREREG.md` as a model element | (a) `availability_fn` overrides; (b) fills unroled columns only; (c) both supplied is an error | B (A for the `DESIGN.md` half) | Low |
| **AM-3** | Availability model | `timestamp_semantics`' "mapping" has no stated form | (a) fixed offset; (b) callable; (c) named column | B | Low; (b) strains §6.8 L635's serialization requirement |
| **AM-4** | Availability model | "versioned" asserted with no versioning rule | (a) user string; (b) content hash; (c) `VALIDATED_CONFIG` section hash | B | Low |
| **AM-5** | Availability model | `a(y_j)`'s "label timestamp" term has no enumerated domain | (a) the timestamp column; (b) any declared column; (c) a literal | B | Low |
| **PR-1** | Profiles | Phase 1 "profiles" vs Phase 7 "Profiles" — which is the deliverable | (a) Ph1 mechanism / Ph7 content; (b) Ph1 both / Ph7 polish; (c) Ph1 schema only | B | Low |
| **PR-2** | Profiles | Which model elements a profile may default is stated only by two exclusions | (a) everything but the two exclusions; (b) only domain-knowable elements | B | Medium — decides `unsupported` vs running under §2.7, which changes yields |
| **PR-3** | Profiles | "profile interval exclusions" is serialized config with no definition | (a) excluded from cohort selection; (b) excluded from the availability matrix; (c) both | B | Low; decides Phase 1 vs Phase 2 ownership |
| **CT-1** | Four controls | No execution order for the four is locked in `PREREG.md`; the order lives in revisable `DESIGN.md` §4.6 and moves §7.5's counters | (a) §6.11's numbering + guard prepended; (b) no order locked — engineering; (c) §6.6 L574's reason precedence is the order | B | **Medium-high** — §0.1 L28's test and §0.1 L46 arguably require it locked/serialized |
| **CT-2** | Four controls | §6.11 L673 "Three, all before any real probe" contradicts L691 "There is no separate compatibility run" | (a) preamble is stale, block quote governs; (b) both a pre-probe check and per-execution validation | A | **Medium** — (b) changes `n`, the §6.11 L697 compatibility denominator §6.6 L608 says is locked pre-tag |
| **CT-3** | Four controls | Identity control runs "once per alignment family" but its mask is cohort-relative and unspecified | (a) first eligible cohort's mask; (b) union over selected cohorts; (c) empty/past-the-end placement | B | Medium — decides `could_not_run(control_artifact)` and a §7.5 counter |
| **CT-4** | Four controls | §6.11 L703 defers the compatibility **objective** to Phase 1, while §0.2.1 L92 makes an already-fixed objective a precondition of class B | (a) Phase 1 authors them → class B's own precondition fails; (b) L703's last sentence is the objective → its weighting is the free parameter | B | **High** — §0.2.1 L107 routes an uncitable post-tag finding to specification defect, and to C if it changes a published threshold's meaning |
| **DP-1** | Detector protocol | "detector protocol" is named once and defined nowhere | (a) the `DESIGN.md` §6 typing Protocol; (b) the normative contract in §7.2/§6.6/§3.1; (c) both | B | Low |
| **DP-2** | Detector protocol | Who constructs a `CombinationTrace` for a combination on which nothing resolves is unstated | (a) harness enumerates and builds; (b) detector emits per combination; (c) reducer synthesizes — barred by §6.6 L564 | B | Medium — decides whether §6.6 L564's raise-never-default is enforceable |
| **DP-3** | Detector protocol | `resolve_tier` imported by `DESIGN.md` §6, absent from §11 L1048's minimum list and from the shipped reducer's top level (verified) | (a) no defect — minimum list, future package; (b) `DESIGN.md` names a reducer with no registered definition | A (`DESIGN.md`-side) | Low |
| **RS-1** | Report skeleton | What "skeleton" means at Phase 1, given §8 references Phase 2 values | (a) surface + structural guarantees, no content; (b) working report over controls/guard only; (c) schema only | B | Low |
| **RS-2** | Report skeleton | §8.4 L935 states the `dtype_promoted` display requirement twice, in two wordings | (a) editing residue, one requirement; (b) two requirements, the second a register constraint | A | Low |
| **RS-3** | Report skeleton | `waived` is an enumerated detector-case state (§7.7 L855) with no defining clause; conditions §10.2 L1035's replacement floor | (a) = the §8.3 L931 recorded-exception mechanism; (b) a distinct user-set state; (c) vestigial | B | **Medium-high** — L1035 is inside the criterion the pending v30a amendment must carry |
| **RS-4** | Report skeleton | `DESIGN.md` §8 L516's scalar control booleans cannot carry per-frame guard / per-family identity results | (a) summaries, detail in `strategy_diagnostics`; (b) storage, detail lost — §0.2.1 L79 violation on the frame axis | A (`DESIGN.md`-side) | Low |
| **PS-1** | Padded slicer | The padding rule is absent from `PREREG.md`; §0.1 L28's test arguably locks it | (a) probe mechanics, correctly in `DESIGN.md` per §0.1 L30; (b) probe-location parameter, locked by §0.1 L28 and serializable by §6.8 L633 | B | **Medium** — under (b) it can flip §6.2 L461 criterion 3 on the sliced fixture |
| **PS-2** | Padded slicer | "maximum window length" has no unit | (a) rows; (b) elapsed time | B | Low-medium — diverges on the fixture's irregular lattice |
| **PS-3** | Padded slicer | What the sliced fixture's ±0.010 is measured against | (a) the same 0.957/0.675 — constrains slice construction; (b) a sliced reference set during Phase 1 — self-referential; (c) "full and sliced" modifies the audit, not the AUC | B | **Medium** — it is the Phase 1 gate's own wording |
| **PS-4** | Padded slicer | "full" carries four senses: audit mode, data extent, `full_scan`, "full refinement" | (a) L992's "full and sliced" = data extent; (b) = audit mode, colliding with §6.2 L445 | A | Low; PS-3 partly turns on it |

**Count: 23 flags — 5 class A, 18 class B**, of which six (CT-1, CT-2, CT-4, RS-3, PS-1, PS-3) carry medium-or-higher risk of routing to class C under §0.2.1's own definitions. Under §0.2.1 L95 a class C item cannot be resolved in a planning chat; it needs an amended, timestamped registration before the affected detector is implemented or evaluated.

---

## 9. Considered and found not ambiguous

Recorded so the absence of a flag is not mistaken for an unread clause.

- **§2.5's "required boolean" vs "absent → `unsupported`".** L231 calls the boolean required; L233 settles the consequence of absence explicitly ("`true` — or absent — makes L2a `unsupported`"). Resolved by the text.
- **§2.7's "neither supplied nor defaulted".** Settles PR-2's *other* half: a profile-defaulted element counts as declared for the `unsupported` test. Resolved by the text.
- **§8.3 L931's "the word 'signed' is not used"** vs **§11 item 2 L1049's "Signed git tag".** The clause is scoped to the recorded-exception mechanism, not to the registration ceremony. Resolved by scope.
- **§6.2 L445's "The gate runs in `full` mode"** vs **§10 L992's "full and sliced".** Resolved in favour of mode-vs-data-extent by context; the residual terminological collision is flagged as PS-4 rather than as a conflict.
- **§6.6 L574's reason precedence.** It is explicitly a precedence for the `incomplete(reason)` field, not an execution order. It does not by itself lock CT-1; it is one of CT-1's candidate readings.
- **§11 item 1's "no detector implementation".** Scoped to the first commit, which has occurred. Not a standing Phase 1 prohibition — recorded in §7.3 to prevent over-reading.

---

## 10. Three summary findings

1. **Of Phase 1's named deliverables, only two have registered acceptance conditions.** The Phase 1 gate (§10, L992) tests §10.0 ordering, claim verification, fixture AUC reproduction, the four alignment-control cases, and snapshot hashing. The **availability model**, **profiles**, **detector protocol**, **report skeleton**, **identity control**, and — beyond the AUC reproduction — the **padded slicer** have no stated pass condition. Each is called out in its own section as a finding.

2. **Two Phase 1 deliverables have their operative rule only in the revisable file.** The four controls' execution order lives in `DESIGN.md` §4.6 (and `HISTORY.md` H-32 records that getting it wrong makes §7.5's determinism counts structurally zero); the padded slicer's padding rule lives in `DESIGN.md` §5.3. Both are probe mechanics, which §0.1 L30 explicitly assigns to `DESIGN.md` — and both are capable of moving a published number, which §0.1 L28 and §6.8 L633 say belongs here. That tension is CT-1 and PS-1 and is the single most consequential pair of decisions to take before code starts.

3. **The whole plan is blocked behind §10.0 step 0.** If Phase 0 recorded the fixture as semantically ambiguous, the class C amendment must be committed and externally timestamped before **anything** in Phase 1, "including any development-corpus access" (L1006), and §10.2 L1033 adds "No `DEVIATIONS.md`-only criterion". At HEAD `0ee26c4` no amendment tag exists and `DEVIATIONS.md` is empty. Whether the trigger has fired is an author determination the repository does not evidence — labelled unverified, not inferred.
