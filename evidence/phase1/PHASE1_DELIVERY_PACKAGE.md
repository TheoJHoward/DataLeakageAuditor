# PHASE 1 DELIVERY PACKAGE — item E

**What this is.** The consolidated Phase 1 preparation material for the planning chat, assembled from three
earlier planning artifacts and re-verified line-by-line against the registration.

**Status: PLANNING ARTIFACT ONLY.** No detector code, no availability-model implementation, no `audit()`
surface, no corpus contact. Nothing below is a decision; the flagged author decisions remain open and are
marked as such. Recommendations are marked as recommendations.

**Sources consolidated** (all under `…\scratchpad\phase1\`, all read in full):

| Item | File | Contributes |
|---|---|---|
| F1 | `PHASE1_PLAN.md` (956 lines) | §E1 — the consolidated ambiguity table |
| F2 | `CLAIMS_ABC_PLAN.md` (628 lines) | §E2 — Claims A–C verification plan |
| F3 | `REPO_READINESS.md` (729 lines) | §E3 — the readiness gap list |

**Repository state as consolidated.** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`, branch
`main`. F1/F2/F3 were written against HEAD `0ee26c4`; the declaration has since been committed locally as
`ffa6d94` (not pushed, no tag). `PREREG.md` is unchanged between those states — it is locked and the
amendment ceremony does not touch it — so every `PREREG.md` line number below is stable. Sole tag:
`prereg-v30`. `DEVIATIONS.md` is 0 bytes; `VALIDATED_CONFIG.toml` is the placeholder; there is no
`prereg-v30a` tag.

**Verification performed for this package.** I re-read `PREREG.md` at every cited line and confirmed each
quotation character-for-character. Four rows (PR-1, DP-1, PS-2, RS-4) carried their `PREREG.md`-side clause
in the source's section prose rather than inside the flag itself; I have supplied the verbatim clause for
each from `PREREG.md`. No row is delivered without a quoted governing clause. Two quotations that the
sources placed in `DESIGN.md` are reproduced as such and are explicitly **not** governing clauses —
`DESIGN.md` is revisable (`PREREG.md:26`).

---

# §E1 — The consolidated ambiguity table, in full

## E1.0 Count verification

**The count is correct as reported: 23 rows — 5 class A, 18 class B.** I enumerated and re-classified every
row independently of the source's summary line.

| Group | Rows | Class A | Class B |
|---|---|---|---|
| Availability model | AM-1 … AM-5 | 0 | 5 |
| Profiles | PR-1 … PR-3 | 0 | 3 |
| The four controls | CT-1 … CT-4 | 1 (CT-2) | 3 |
| Detector protocol | DP-1 … DP-3 | 1 (DP-3) | 2 |
| Report skeleton | RS-1 … RS-4 | 2 (RS-2, RS-4) | 2 |
| Padded slicer | PS-1 … PS-4 | 1 (PS-4) | 3 |
| **Total** | **23** | **5** | **18** |

Class here uses F1's own framing — **A** = mechanical or typographic; **B** = clarification needed before
code — which is *not* `PREREG.md` §0.2.1's class scheme. The two schemes are tracked separately throughout,
because a row that is "mechanical" in F1's sense can still route to §0.2.1 class C. Six rows carry
medium-or-higher risk of that routing: **CT-1, CT-2, CT-4, RS-3, PS-1, PS-3**.

Two rows are class A **on their `DESIGN.md` half only** (AM-2's role-vs-element divergence, DP-3, RS-4).
AM-2's primary class is B and it is counted as B; DP-3 and RS-4 are counted as A because their whole
substance is `DESIGN.md`-side.

**The governing constraint on what a planning chat may do with these**, `PREREG.md:95`, verbatim:

> **Class C requires an amended registration**, committed and externally timestamped **before the affected
> detector is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md`
> entry standing alone. The deviation records what was measured; the amended tag carries the new semantics.
> Both.

---

## E1.1 — Availability model (5 rows, all class B)

### AM-1 — `bar_duration` "inferred from successive timestamps" has no stated basis

**Item:** Availability model.
**Ambiguity:** `bar_duration` may be "inferred from successive timestamps". The registration never says
*successive what*. On panel data the two candidate bases differ materially.
**Candidate readings:**
- **(a)** successive **rows** — `ts[j+1] − ts[j]` over row order;
- **(b)** successive **distinct timestamps** — the gap on the unique-timestamp lattice.

Under (a), every entity sharing an instant on panel data gets a zero-duration bar, which collapses
`at_bar_close` onto `at_timestamp` and changes findings at the boundary.
**Class:** B. §0.2.1 routing risk: low, but it changes `a(j,c)` on panel data, so C if the resolution adds a
branch.
**Governing clause — `PREREG.md:208`, verbatim:**

> | `bar_duration` | fixed value, or inferred from successive timestamps; **at the final row the last known duration is carried forward** | roles using bar close |

Reinforcing, `PREREG.md:210`, verbatim — this is what puts panel data explicitly in scope:

> | `panel_mask_scope` | **global, locked.** Masks are computed across all entities at a decision instant | L3.1, L2a |

Decision-affecting, therefore reached by `PREREG.md:633`, verbatim:

> **Every parameter capable of changing a detector decision, a tier assignment, execution eligibility, probe location, or strategy compatibility is serialized into, and hashed with, the applicable `VALIDATED_CONFIG` section.**

---

### AM-2 — `availability_fn`'s relation to `column_roles` is unstated, and the two files disagree on what it is

**Item:** Availability model.
**Ambiguity:** `PREREG.md` lists `availability_fn` as a top-level `AvailabilityModel` element and enumerates
`column_roles` as exactly five values not including it; `DESIGN.md` §2.1 lists it as a sixth `column_roles`
value. Precedence when both are supplied is stated nowhere.
**Candidate readings** (on precedence):
- **(a)** `availability_fn` overrides all roles;
- **(b)** it fills only columns with no role;
- **(c)** supplying both is rejected.

The `DESIGN.md`/`PREREG.md` divergence on whether it is a role at all is a separate, mechanical half.
**Class:** B (A for the `DESIGN.md` half). §0.2.1 routing risk: low.
**Governing clauses — `PREREG.md:205` and `PREREG.md:209`, verbatim:**

> | `column_roles` | per-column rule: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column | all |

> | `availability_fn` | escape hatch: user callable returning `a(j, c)` | all |

For reference only, and **not** a governing clause — `DESIGN.md:68`, the sixth row of its role table:

> | `availability_fn` | user callable |

---

### AM-3 — `timestamp_semantics`' "mapping" has no stated form

**Item:** Availability model.
**Ambiguity:** the element requires "the mapping if not the last", and the mapping's form is never stated.
**Candidate readings:** **(a)** a fixed offset; **(b)** a user callable; **(c)** a named column.
**Class:** B. §0.2.1 routing risk: low; reading (b) strains the serialization requirement, since a callable
is not serializable in the sense the rest of `PREREG.md:635`'s list assumes.
**Governing clause — `PREREG.md:204`, verbatim:**

> | `timestamp_semantics` | whether the timestamp column is observation, event, or availability time, plus the mapping if not the last | all |

The serialization requirement it strains — `PREREG.md:635`, verbatim (closing clause):

> **and the complete `AvailabilityModel` of §2.3, including `ties`.**

---

### AM-4 — "versioned" is asserted without a versioning rule

**Item:** Availability model.
**Ambiguity:** the model is declared versioned and recorded with every result; no clause states how the
version is formed or what changes bump it.
**Candidate readings:** **(a)** a user-supplied string; **(b)** a content hash of the serialized
declaration; **(c)** the `VALIDATED_CONFIG` section hash.
**Class:** B. §0.2.1 routing risk: low.
**Governing clause — `PREREG.md:199`, verbatim:**

> **`AvailabilityModel`**, versioned and recorded with every result:

Why it matters — `PREREG.md:961`, verbatim:

> Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval, the availability declaration in force, and — for runtime rows — the probed-cohort count and row coverage. Non-holdout author-produced numbers say so in the same line.

and `PREREG.md:266`, verbatim (excerpt): "the declaration is in `VALIDATED_CONFIG` with every published rate".

---

### AM-5 — the "label timestamp" term of `a(y_j)` has no enumerated domain

**Item:** Availability model.
**Ambiguity:** the label-availability formula's base term is never bounded. §2.4 forbids profiles defaulting
any term but does not say what the term may be.
**Candidate readings:** **(a)** the frame's timestamp column only; **(b)** any declared column; **(c)** a
literal instant. Under (b), `label_availability` partly duplicates `at_source_timestamp` — which interacts
with AM-2.
**Class:** B. §0.2.1 routing risk: low.
**Governing clauses — `PREREG.md:220` and `PREREG.md:222`, verbatim:**

> **`a(y_j) = label timestamp + label horizon + publication delay`**

> - **All three terms are user-declared, as one `label_availability` declaration.** The publication delay **defaults to zero only when the user supplies the declaration** — it is part of the user's statement, not something a profile fills in. A declaration supplying only base and horizon is complete; a missing declaration is not.

And the prohibition that does not bound the domain — `PREREG.md:224`, verbatim:

> - **No profile may default any term.** Supplying a label column on a temporal task without a declared label availability makes L2a — and L3.1b — `unsupported`.

---

## E1.2 — Profiles (3 rows, all class B)

### PR-1 — Phase 1 "profiles" versus Phase 7 "Profiles"

**Item:** Profiles.
**Ambiguity:** §10's phase table assigns "profiles" to Phase 1 and "Profiles" to Phase 7, with the only
stated acceptance condition attached to Phase 7.
**Candidate readings:**
- **(a)** Phase 1 builds the profile *mechanism* (how a profile resolves into an `AvailabilityModel`); Phase 7 authors and ships the two named profiles;
- **(b)** Phase 1 builds mechanism *and* both profiles; Phase 7 only documents and polishes;
- **(c)** Phase 1's "profiles" means only the profile *schema* the availability model needs, with no resolution logic.

Material because the Phase 2 fixture gate runs on the frozen default configuration, and whether a profile is
inside that frozen configuration depends on the reading.
**Class:** B. §0.2.1 routing risk: low.
**Governing clauses — `PREREG.md:992` (Phase 1 row) and `PREREG.md:998` (Phase 7 row), verbatim:**

> | **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |

> | **7** | Profiles, docs, v1.0 | 1–2 wknds | `futures` and `generic` profiles ship |

The counter-consideration inside the registration — `PREREG.md:447`, verbatim (excerpt): "**The availability
declaration is reconstructed, not chosen**", which may mean the fixture path needs no profile at all.

---

### PR-2 — which model elements a profile may default is stated only negatively

**Item:** Profiles.
**Ambiguity:** exactly two elements are excluded from profile defaulting. Because a profile-defaulted
element counts as declared for the `unsupported` test, that two-item exclusion list is the entire boundary
between `unsupported` and a running detector.
**Candidate readings:**
- **(a)** everything except the two named exclusions may be profile-defaulted — including `ties`, `panel_mask_scope`, `panel_rule_scope`, `embargo`, `bar_duration`, `timestamp_semantics`, `availability_fn`;
- **(b)** only elements a domain profile can genuinely know (`decision_time`, `column_roles`, `bar_duration`, `ties`) may be defaulted, and the rest must be user-supplied.

Under (a) a profile could default `embargo`, which the registration warns about by name.
**Class:** B. §0.2.1 routing risk: **medium** — it decides `unsupported` versus running under §2.7, which
changes yields.
**Governing clauses — `PREREG.md:216` and `PREREG.md:248`, verbatim:**

> Profiles supply defaults (`DESIGN.md`). No profile supplies `label_availability` (§2.4) or the non-temporal policy of §2.5.

> If the required declaration is neither supplied nor defaulted, **L3.1, L2a, and L3.1b return `unsupported`** (§8.2), naming the missing element. They do not fall back to row order.

The specific warning reading (a) collides with — `PREREG.md:214`, verbatim (closing clause): "`embargo` is
scoped explicitly because a field silently applying to masks would change every runtime rate."

---

### PR-3 — "profile interval exclusions" is a serialized configuration item with no registered definition

**Item:** Profiles.
**Ambiguity:** the term is required in `VALIDATED_CONFIG` and appears once more as "profile intervals"; no
clause defines what an interval exclusion is or what it excludes.
**Candidate readings:** **(a)** intervals excluded from *cohort selection*; **(b)** intervals excluded from
the *availability matrix*; **(c)** both. Under (a) this is Phase 2 work; under (b) it is Phase 1
availability-model work — the phase assignment turns on the reading.
**Class:** B. §0.2.1 routing risk: low; it decides Phase 1 versus Phase 2 ownership.
**Governing clause — `PREREG.md:635`, verbatim (the item, in its list context):**

> Non-exhaustively: cohort count, selection and spacing mode, exclusion fraction; reach-refinement policy and candidate grid; profile interval exclusions; strategy set, escalation order, **and each strategy's required-or-optional status (§7.7)**; **the terminal-decision policy (§7.7)**; whether probing stops at first finding; shuffle scope; noise distribution and scale; sentinel value; complex magnitude; **each strategy's permitted promotion set (§6.10)**; determinism-guard repetition count per frame; internal perturbation seeds; compatibility- and equivalence-failure behaviour; **and the complete `AvailabilityModel` of §2.3, including `ties`.**

The only other occurrence — `PREREG.md:383`, verbatim (excerpt): "missed session gaps (profile intervals)".

---

## E1.3 — The four controls (4 rows: 1 class A, 3 class B)

> **Framing note carried forward from F1, because it changes what the group is.** `PREREG.md` says **three**
> controls plus a separate guard, not four. The "four" is `{determinism guard, alignment equivalence,
> identity perturbation, compatibility}`, and that four-way split is supported by the diagnostics and the
> reason codes. `PREREG.md:673`, verbatim: "Three, all before any real probe. Failures are recorded per
> §7.7's two-level scheme, never as findings:". `PREREG.md:992` names the deliverable verbatim as "the three
> controls and the determinism guard".

### CT-1 — no execution order for the four is locked in `PREREG.md`, and the order that exists is decision-affecting

**Item:** The four controls.
**Ambiguity:** the execution order usually cited — guard → alignment equivalence → identity → probe, with
compatibility per execution — is stated only in the revisable file. `PREREG.md` locks entailments, not a
sequence.
**Candidate readings:**
- **(a)** §6.11's numbering (1 alignment → 2 identity → 3 compatibility) *is* the locked order, with the guard prepended by §6.10;
- **(b)** no order is locked — only the entailments bind, and the sequence is `DESIGN.md` engineering;
- **(c)** §6.6's reason precedence (`determinism` → `alignment` → `compatibility` → `control_artifact`) is the intended order and §6.11's numbering is incidental.

(a) and (c) disagree about where the identity control sits — §6.11 numbers it **second**, the precedence puts
`control_artifact` **fourth**. That is not cosmetic: §7.5 keeps *separate* counters for the four failure
kinds and, unlike `incomplete(reason)`, those counters are not precedence-normalized, so a pipeline failing
two controls contributes to whichever counter its implementation reached first.
**Class:** B. §0.2.1 routing risk: **medium-high**.
**Governing clauses — `PREREG.md:574`, verbatim (the precedence, which is explicitly *not* an execution order):**

> 5. `incomplete(reason)` — execution-eligible, and the schedule did not complete. **Reason precedence when strategies fail differently:** `determinism`, then `alignment`, then `compatibility`, then `control_artifact`, then `crash`.

The counters it does not normalize — `PREREG.md:841`, verbatim:

> Per **detector × strategy × promotion status**: **eligible cases, completed cases, optional-strategy failures, required-strategy failures, alignment-equivalence failures, compatibility failures, determinism failures, control artifacts, correct primary findings, false findings.** Counted within the strategy, per §7.2's scoping, and derived from per-case records.

The lock test the row turns on — `PREREG.md:28` and `PREREG.md:30`, verbatim:

> If changing it would make a past result look better than it was, it is locked here. If changing it is just engineering, it goes in `DESIGN.md`.

> Probe mechanics live in `DESIGN.md`, because through v9 they were specified in this file and were wrong three versions running. What is locked here is the requirement, not the mechanism:

and the serialization backstop — `PREREG.md:46`, verbatim:

> Anything in `DESIGN.md` capable of changing a detector decision, a tier, execution eligibility, probe location, or strategy compatibility is serialized into `VALIDATED_CONFIG` (§6.8). Revisable does not mean unrecorded.

For reference only, and **not** governing — `DESIGN.md:355`: "*The guard precedes every comparison-based
control*, because it licenses the comparison the alignment control performs."

---

### CT-2 — "Three, all before any real probe" is contradicted by control 3's own block quote

**Item:** The four controls.
**Ambiguity:** the §6.11 preamble says all three controls run before any real probe; control 3's block quote
says there is no separate compatibility run at all.
**Candidate readings:**
- **(a)** the preamble is editing residue and the block quote governs — compatibility is per-execution and not a pre-probe control, so "three, all before any real probe" is literally false for one of the three;
- **(b)** both hold — a pre-probe compatibility check *and* per-execution validation.

(b) is directly contradicted by the block quote, so (a) is near-certain. The flag exists because the
contradicted sentence is in the **locked** file.
**Class:** A, with class-C risk. §0.2.1 routing risk: **medium** — under (b) a standalone pre-probe check
would add attempts to `n`, the compatibility denominator, changing a published escalation threshold's
denominator.
**Governing clauses — `PREREG.md:673` and `PREREG.md:691`, verbatim:**

> Three, all before any real probe. Failures are recorded per §7.7's two-level scheme, never as findings:

> > There is no separate compatibility run. Every perturbed execution validates shape and index against the baseline before its result is used. A failure discards that probe's result.

The denominator at risk — `PREREG.md:697`, verbatim:

> **Strategy-level escalation to `could_not_run(compatibility)`** uses a **failure fraction with a minimum absolute count**: the strategy is incompatible for the detector-case when `f ≥ m` **and** `f / n > q`, where `f` is failed perturbed executions, `n` is attempted eligible probes for that detector × case × strategy, aggregated by actual promotion status for publication (§7.5), and `m`, `q` come from `VALIDATED_CONFIG`.

---

### CT-3 — the identity control's mask is unspecified

**Item:** The four controls.
**Ambiguity:** the identity control runs once per alignment family, but "unavailable cells" is
cohort-relative — every cohort has a different unavailable set — and the clause does not say which cohort's
mask the single run uses.
**Candidate readings:** **(a)** the first selected eligible cohort's mask; **(b)** the union over all
selected cohorts; **(c)** a placement with an empty mask.
**Class:** B. §0.2.1 routing risk: **medium** — it decides `could_not_run(control_artifact)`, a detector-case
outcome and a §7.5 counter, and a pipeline can be artifact-free under one mask and not another for exactly
the reason the registration gives about compatibility.
**Governing clause — `PREREG.md:686`, verbatim in full:**

> 2. **Identity perturbation** — replace unavailable cells with an exact copy of themselves. Any delta is measurement artifact. On the aligned frame, once per alignment family.

The mask-dependence reasoning that makes this material — `PREREG.md:689`, verbatim (opening):

> **Compatibility is mask-dependent, so a single check cannot stand in for the probes.** L3.1 perturbs many columns and L2a perturbs only the label; early and late cohorts mask different cells; a mask that puts NaNs into a column feeding row-dropping logic behaves differently from one that does not.

Note: `DESIGN.md:329` offers a mechanism ("or place the cohort past the end of the data") with no counterpart
in `PREREG.md`. That is legitimately mechanism under `PREREG.md:30`, and it does not settle which of (a)–(c)
the registration intends.

---

### CT-4 — §6.11 defers the compatibility objective to Phase 1, while §0.2.1 makes an already-fixed objective a precondition of class B membership

**Item:** The four controls.
**Ambiguity:** the candidate ranges for `m` and `q` and the objective used to select them appear **nowhere**
in `PREREG.md`, yet the compatibility fraction is §0.2.1's own worked example of a class B parameter.
**Candidate readings:**
- **(a)** "Locked at Phase 1" means Phase 1 must *author and freeze* them — in which case, at the moment they are authored, the objective is not "already fixed" and the compatibility fraction fails class B's own precondition;
- **(b)** the objective *is* fixed by the clause's final sentence and Phase 1 only instantiates it — in which case the "objective" is a three-term balance with no stated weighting, and the weighting becomes the free parameter.

**Class:** B, with high class-C risk. §0.2.1 routing risk: **high**.
**Governing clauses — `PREREG.md:703` and `PREREG.md:92`, verbatim:**

> **Locked at Phase 1:** the fraction-plus-minimum form, the denominator, how failures after a terminal finding are handled, the candidate ranges for `m` and `q`, and the objective used to select them. **Chosen on the development corpus and frozen with the matching `VALIDATED_CONFIG` section:** the values. **`m` and `q` are not selected to keep completion above §10.2's 60% floor** — the objective balances false silence, probe loss, and detector-case failure on their own terms, and the floor remains a downstream kill gate rather than a target.

> | **B — parameters under a locked procedure** | A value chosen where the form, search space, objective, denominator, and freeze point are already fixed | select on the development corpus and freeze | the compatibility fraction and its minimum count; cohort count; strategy order |

The routing rule that makes reading (a) serious — `PREREG.md:107`, verbatim:

> **A post-tag finding that cannot cite a stated assumption is not in class A or B.** It is a specification defect. It gets a loud `DEVIATIONS.md` entry, and if it changes what any published number means, an amended registration under the class C rule.

---

## E1.4 — Detector protocol (3 rows: 1 class A, 2 class B)

### DP-1 — "detector protocol" is named as a deliverable and defined nowhere

**Item:** Detector protocol.
**Ambiguity:** the phrase occurs exactly once in `PREREG.md` — in Phase 1's work column. There is no section
defining it and no other occurrence.
**Candidate readings:**
- **(a)** it means the Python typing `Protocol` of `DESIGN.md` §6 (`id`, `requires`, `scope_applies`, `run`) — in which case the deliverable is entirely `DESIGN.md`-governed;
- **(b)** it means the normative contract itself — what a detector may and may not decide (it emits EvidenceEvents; it never assigns its own tier, `schedule_state`, or `evidence_outcome`);
- **(c)** both, with (a) as the surface and (b) as the invariant set.

Material because under (a) the whole deliverable is revisable and needs no registration discipline, while
under (b) parts are already locked and an implementation that deviates is a protocol failure rather than a
design change.
**Class:** B. §0.2.1 routing risk: low.
**Governing clause — `PREREG.md:992`, verbatim (the sole occurrence, in the Phase 1 work column):**

> | **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |

The locked obligations that reading (b) would draw on — `PREREG.md:780–781`, verbatim:

> | **EvidenceEvent** | `(detector, promotion_status, feature, affected output cohort)` **within a case**; corpus-level records additionally carry case identity | every combination-specific metric in §7.1 |
> | **ReportedFinding** | `(detector, feature, affected output cohort)` | user-facing display; carries the highest tier its events justify |

---

### DP-2 — the registration never says who constructs a `CombinationTrace`

**Item:** Detector protocol.
**Ambiguity:** a trace is required for **both** promotion statuses on **every** labelled case, regardless of
what the configuration resolves; a combination on which *nothing resolves* must still be traced
`not_applicable`. So something must emit a trace for a combination that never ran — and the registration
does not say what.
**Candidate readings:**
- **(a)** the detector emits per-execution records and the *harness* enumerates the two combinations per case and builds traces — the only reading under which a never-run combination gets a trace without the detector being invoked for it;
- **(b)** the detector emits traces directly, and must therefore be invoked once per combination even when no strategy resolves;
- **(c)** the reducer synthesizes missing traces — contradicted by the "must raise, never default" clause.

**Class:** B. §0.2.1 routing risk: **medium** — it decides whether trace completeness is enforceable at all.
**Governing clauses — `PREREG.md:562` and `PREREG.md:564`, verbatim:**

> > **"Every combination" means both promotion statuses, always.** §3.1's axis is closed and two-valued, so a case has exactly two combinations regardless of which strategies the frozen configuration happens to resolve on it. A combination on which nothing resolves is traced `not_applicable`, explicitly. **Enforcement may not depend on the configuration or on what happened** — the loose reading, where only combinations with at least one trace are checked, makes omitting a whole row silent while omitting one strategy raises, which is outcome-dependent enforcement of a rule against outcome-dependence.

> > **Every labelled case carries an explicit trace for every combination.** A combination with no trace has no state, and silently skipping it drops the case from that combination's denominators — which inflates its yields and shrinks §10.2's *N*. The build demonstrated a gate verdict flipping on trace omission alone. **A missing trace is a protocol violation and must raise, never default.** This is the "absence carries meaning" failure the trace schema exists to prevent, and it is stated here rather than left implied.

---

### DP-3 — `resolve_tier` is named by `DESIGN.md` as a canonical reducer import but is not among §11's minimum symbols and is not a top-level symbol in the shipped reducer

**Item:** Detector protocol.
**Ambiguity:** `DESIGN.md` §6 imports `resolve_tier` from `leakaudit.protocol`; §11's minimum list does not
name it, and a symbol scan of the shipped reducer shows no top-level `resolve_tier` (tier is assigned inside
`derive_reported_findings`).
**Candidate readings:**
- **(a)** no defect — §11's list is a minimum, `leakaudit.protocol` is the future package rather than the shipped reference file, and §3.1's rule is a two-row table any component may apply;
- **(b)** `DESIGN.md` names a canonical reducer the registration does not require to exist, so a detector written against `DESIGN.md` imports a symbol with no registered definition.

Which of (a) or (b) holds is genuinely undetermined from the documents. The underlying scan result is
verified and independently reconfirmed by F3 (`hasattr(rr, "resolve_tier")` → `False`).
**Class:** A (`DESIGN.md`-side). §0.2.1 routing risk: low.
**Governing clause — `PREREG.md:1048`, verbatim (the minimum-symbol clause):**

> 1. **The first commit contains the registration and its checking tools, and no detector implementation:** `PREREG.md` (locked, unchanged), `DESIGN.md`, **`HISTORY.md`**, an empty append-only `DEVIATIONS.md`, a `PARKING_LOT.md` **containing only the §13.9 entry**, a placeholder `VALIDATED_CONFIG.toml`, **`tools/check_registration.py`** carrying §6.8's checks plus the single-source and banned-vocabulary scans, **`protocol/runtime_reference.py`** — pure, non-detector reducers, **at minimum** `resolve_schedule_state`, `resolve_evidence_outcome`, `derive_evidence_events`, `derive_reported_findings`, `compute_runtime_metrics`, `apply_runtime_gates`, and `evaluate_runtime_assertions`, the last of which §8.3 requires and the earlier list omitted — and **`tests/registration/`** carrying negative tests that a deleted symbol is rejected plus the exhaustive small-trace suite of §6.6.1. Earlier versions said five files and no implementation while the document relied on validators and scans; protocol tooling is not detector implementation, and residue defenses absent from the registered repository are not reproducible from it.

---

## E1.5 — Report skeleton (4 rows: 2 class A, 2 class B)

### RS-1 — what "skeleton" means at Phase 1

**Item:** Report skeleton.
**Ambiguity:** several §8 obligations reference values that cannot exist until Phase 2 — probed-cohort count
and row coverage, reach and `reach_basis`, per-strategy diagnostics.
**Candidate readings:**
- **(a)** skeleton = the report's field and method surface with every §8 guarantee enforced structurally (states cannot render as a pass; counts render as numerator/denominator; reach fields exist but are suppressed) and no runtime content;
- **(b)** skeleton = a working report over the controls and the guard only — which is exactly what Phase 1 produces;
- **(c)** skeleton = the JSON schema and nothing rendered.

**Class:** B. §0.2.1 routing risk: low.
**Governing clause — `PREREG.md:911`, verbatim (the obligation that names Phase 2 values):**

> It says which detectors ran, in which mode, under which configuration and declaration, **which decision cohorts were probed and what fraction of rows they cover**, and what they found.

and `PREREG.md:949`, verbatim:

> - **A reach value is reported only from a full scan over the candidate availability boundaries present in the data**, and is described as the latest boundary at which a change was observed — not as the latest cell the feature depends on.

The deliverable naming — `PREREG.md:992`, "report skeleton", quoted in full under PR-1.

---

### RS-2 — §8.4 states the same requirement twice, in two wordings

**Item:** Report skeleton.
**Ambiguity:** the `dtype_promoted` display requirement is stated twice in one bullet, in two wordings.
**Candidate readings:** **(a)** editing residue — one requirement, duplicated, and either wording discharges
it; **(b)** two requirements — the first mandates the content, the second mandates that it be stated
*plainly*, i.e. a register constraint on the wording.
Consequential only for whether a checker should look for one clause or two. Flagged because it is in the
locked file and §0.2.1's own diagnosis is that duplicated statements drift.
**Class:** A. §0.2.1 routing risk: low.
**Governing clause — `PREREG.md:935`, verbatim:**

> - **Every L2a and L3.1 finding prints the availability declaration it was evaluated under, its promotion status, its probe cohort, and its affected output cohort.** A `dtype_promoted` finding names the promotion that occurred and states that no preserving run reproduced it. A `dtype_promoted` finding names the promotion that occurred and states plainly that a preserving run did not reproduce it.

---

### RS-3 — `waived` is an enumerated detector-case state with no defining clause

**Item:** Report skeleton.
**Ambiguity:** `waived` occurs exactly twice in `PREREG.md` and never in `DESIGN.md`. Nothing states what
produces it, what it means, or how `assert_audit_complete()` treats it — that assertion names only
`unsupported` and `could_not_run`, so on a literal reading a `waived` entry passes it.
**Candidate readings:**
- **(a)** `waived` *is* the recorded-exception mechanism reaching the coverage table — a `could_not_run` entry the user has explicitly excepted;
- **(b)** a distinct user-set state meaning "this detector was deliberately not requested";
- **(c)** vestigial, with no production rule.

Under (a) and (c) the assertion behaves as written; under (b) a detector could be silently waived out of it.
**Class:** B. §0.2.1 routing risk: **medium-high** — the second occurrence is inside the criterion the
pending v30a amendment must carry, so the reading is load-bearing for v30a, not only for Phase 1.
**Governing clauses — `PREREG.md:855` and `PREREG.md:1035`, verbatim:**

> | **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

The assertion that does not name it — `PREREG.md:929`, verbatim:

> - **`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings.

---

### RS-4 — the report's control fields compress per-frame results into scalars

**Item:** Report skeleton.
**Ambiguity:** `DESIGN.md` §8 lists `determinism_check_passed`, `alignment_equivalence_passed`,
`identity_control_passed` as `AuditReport` fields. The guard is per execution frame and the identity control
is per alignment family — so on a run with F frames there are F guard results and one identity result per
family, and a scalar boolean cannot carry them.
**Candidate readings:** **(a)** the booleans are summaries and the per-frame detail lives in
`strategy_diagnostics` — harmless; **(b)** they are the storage and the per-frame detail is lost, which is
the "no field answers two questions" failure applied to a frame axis.
**Class:** A (`DESIGN.md`-side). §0.2.1 routing risk: low.
**Governing clauses — `PREREG.md:661` and `PREREG.md:841`, verbatim:**

> > **Each distinct execution frame carries its own determinism guard**: the original frame for preserving runs, and each promoted alignment family for the strategies that use it.

> Per **detector × strategy × promotion status**: **eligible cases, completed cases, optional-strategy failures, required-strategy failures, alignment-equivalence failures, compatibility failures, determinism failures, control artifacts, correct primary findings, false findings.** Counted within the strategy, per §7.2's scoping, and derived from per-case records.

For reference only, and **not** governing — `DESIGN.md:516` lists the three scalar booleans among the
`AuditReport` fields.

---

## E1.6 — Padded slicer (4 rows: 1 class A, 3 class B)

### PS-1 — the padding rule is not in the registration, and §0.1's own test arguably locks it

**Item:** Padded slicer.
**Ambiguity:** `PREREG.md` states two things about the padded slicer and **no padding rule**. The rule lives
in the revisable file.
**Candidate readings:**
- **(a)** padding is probe mechanics, correctly in `DESIGN.md`, with the general rule requiring only that the resulting parameter be serialized;
- **(b)** padding determines which cohorts are probed on a sliced run, so under §0.1's own test it belongs in `PREREG.md` and is missing.

A concrete instance of (b): shortening padding moves the first probed cohort into the warmup region, where
head artifacts live, and can flip fixture criterion 3.
**Class:** B, with class-C risk. §0.2.1 routing risk: **medium**.
**Governing clauses — `PREREG.md:451`, `PREREG.md:28`, `PREREG.md:30`, `PREREG.md:461`, verbatim:**

> - **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

> If changing it would make a past result look better than it was, it is locked here. If changing it is just engineering, it goes in `DESIGN.md`.

> Probe mechanics live in `DESIGN.md`, because through v9 they were specified in this file and were wrong three versions running. What is locked here is the requirement, not the mechanism:

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

Consequence if (b) — `PREREG.md:633`, quoted under AM-1, requires the padding length to be frozen in
`[validated.runtime]` before the Phase 2 fixture run.

For reference only, and **not** governing — `DESIGN.md:393`: "**Any slice carries padding of at least the
maximum window length before the first probed cohort**, present in the data, excluded from probing, and
reported."

---

### PS-2 — padding is specified as "the maximum window length" with no unit

**Item:** Padded slicer.
**Ambiguity:** the padding quantity has no unit. On a regular lattice the two candidates coincide; on an
irregular one they do not, and the acceptance fixture's lattice is irregular.
**Candidate readings:** **(a)** rows — the count a `rolling(60)` consumes; **(b)** elapsed time — the span a
`rolling('60s')` consumes. Under (a) a time-based rolling window is under-padded; under (b) a row-based one
is over-padded, costing probed cohorts.
**Class:** B. §0.2.1 routing risk: low-medium; decision-affecting via probe location.
**Governing clauses — `PREREG.md:992` (the deliverable and its gate) and `PREREG.md:451`, quoted above; and
`PREREG.md:633`, verbatim, which is what makes the unit a serialized item:**

> **Every parameter capable of changing a detector decision, a tier assignment, execution eligibility, probe location, or strategy compatibility is serialized into, and hashed with, the applicable `VALIDATED_CONFIG` section.**

Note the absence, stated because it is the substance of the flag: `PREREG.md:635`'s non-exhaustive
serialization list does **not** name padding or `max_window`. The unit-bearing sentence exists only at
`DESIGN.md:393`, which is not a governing clause.

*(The irregular-lattice evidence — intra-day re-anchor gaps and same-second rows on some instrument-months —
is Phase 0 spike material and is untracked. Cited as context, not as a registered fact.)*

---

### PS-3 — what the sliced fixture's ±0.010 is measured against

**Item:** Padded slicer.
**Ambiguity:** the Phase 1 gate requires both fixture AUCs to reproduce within ±0.010 "full and sliced";
§6.2 gives one pair of reference AUCs and no separate sliced reference.
**Candidate readings:**
- **(a)** the sliced variant must reproduce the *same* 0.957/0.675 within ±0.010 — a substantive constraint on slice size and placement, which the registration nowhere constrains so as to make achievable;
- **(b)** each variant reproduces its own reference, and the sliced reference is established during Phase 1 — a reference established during the phase it gates is not an ex-ante criterion;
- **(c)** "full and sliced" modifies the *audit* rather than the AUC.

Load-bearing: (a) makes the Phase 1 gate potentially unsatisfiable by construction; (b) makes it
self-referential.
**Class:** B. §0.2.1 routing risk: **medium** — it is the Phase 1 gate's own wording.
**Governing clauses — `PREREG.md:992` (gate column, verbatim excerpt) and `PREREG.md:445`, verbatim:**

> both fixture AUCs reproduce within ±0.010, full and sliced

> - **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

---

### PS-4 — "full" carries at least four distinct senses in the registration

**Item:** Padded slicer.
**Ambiguity:** `full` means: audit *mode*; full **data** versus sliced; the `full_scan` reach basis; and
"full refinement".
**Candidate readings** for the gate's "full and sliced": **(a)** data extent, contrasted with the sliced
variant — near-certain from context; **(b)** audit mode, which would collide with §6.2's "The gate runs in
`full` mode" and make that sentence redundant.
Mechanical and low-stakes, but it is the term PS-3's reading partly turns on.
**Class:** A. §0.2.1 routing risk: low.
**Governing clauses — `PREREG.md:445` (quoted above), `PREREG.md:992` (gate column, quoted above), and
`PREREG.md:951`, verbatim:**

> - **Above the cap, the capped subset is not scanned at all.** When the complete candidate count exceeds the frozen grid cap of §12, the lower-bound procedure runs instead and `reach_basis = lower_bound` is serialized. *(An alternative reading — scan the first `cap` boundaries and call it `full_scan` — would let a configuration value silently convert a partial observation into a complete one, which is the overclaim this section exists to prevent. `DESIGN.md` carried that reading while this file carried the fallback; one rule, one place, and this is the place.)*

and `PREREG.md:119`, verbatim (excerpt): "**full refinement scans the frozen candidate grid and reports the
latest boundary at which the selected corruption strategy produced an observable change.**"

---

## E1.7 — One observation from my verification pass, NOT a 24th row

While re-reading §4.3 I noticed a cross-reference that neither F1 nor F2 flags. `PREREG.md:355`, verbatim
(closing sentence):

> The CI check of §6.7 verifies these inequalities against the shipped implementation.

The check it names actually lives in §6.8 — `PREREG.md:649`, verbatim (excerpt): "that §4.3's inequalities
match the shipped rule". §6.7 is the hand-authored-cases section. This is a pointer of the same kind §0.1
records having been wrong three versions running ("Three consecutive versions carried a wrong pointer in this
table", `PREREG.md:44`) — though this one is in §4.3's prose, not in the lock table, so the §6.8 lock-table
key-phrase check does not cover it.

**I am recording this as an observation, not adding it to the table.** The count of 23 is F1's and it is
correct as reported; a 24th row is an author's call, not mine. If the author wants it in, it is
mechanical/class A on its face, with the same low routing risk as PS-4.

---

# §E2 — Claims A–C verification plan

**The gate that dominates all three.** `PREREG.md:1006` (§10.0 step 0) makes the class C amendment a
precondition for *everything* below it — which includes step 1 (writing the throwaway tests) and step 2
(verifying Claims A–C). Verbatim:

> 0. **If Phase 0 recorded the fixture as semantically ambiguous, the class C amendment of §10.2 is committed and timestamped before anything below — including any development-corpus access.**

and `PREREG.md:1033`, verbatim:

> > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

At the time of writing there is no `prereg-v30a` tag. **Nothing in §E2 may execute yet.** This is a
pre-positioned plan.

**The single most important scheduling hazard, carried forward verbatim from F2.** Step 0 forces
`prereg-v30a` to be committed **before** Claim A is verified, and `prereg-v30a` carries the replacement
acceptance criterion for the fixture. Phase 0 evidence records the fixture's `ties` branch as
`AMBIGUOUS-PENDING-AUTHOR` and records that the two branches adjudicate the pre-fix side oppositely. If the
amendment's replacement criterion is written in terms of a specific tie branch and Claim A is subsequently
refuted, the criterion moves — requiring a *second* amendment to an object `PREREG.md:93` classifies as class
C by name ("acceptance criterion").

> **Mitigation to specify inside `prereg-v30a`, before it is tagged:** state the replacement criterion in a
> form that is *invariant under the tie branch*, or state it explicitly under both branches with the branch
> named as an open Phase 1 item. Do not let the amendment's threshold depend on an unverified default. This
> is a drafting instruction for the v30a item, not a Claims A–C action, and it is the one dependency that
> runs backwards from this plan into work already in flight.

**A second hazard, procedural.** Pre-computed both-branch counts from Phase 0 (T1/M5) make a post-hoc `ties`
flip *costless* — the property §0.2.1 exists to remove. **The Claim A decision rule must be written down and
hashed before any Claim A measurement runs, and the existing both-branch counts may not be used as the
Claim A measurement.** They were produced for a different question, on fixture data, after the fact.

**The pre-authorized rewrite path governing all three claims** — `PREREG.md:136`, verbatim:

> **If verification contradicts any of these claims, the response depends on §0.2.1's classes, not on convenience.** If the result instantiates a pre-defined class A branch or selects a class B parameter under its locked procedure, record it in `DEVIATIONS.md` and in the frozen configuration. **If it requires a class C change — a new branch, unit, denominator, coverage state, tier licence, or acceptance criterion — record the measurement and commit an amended pre-registration before implementing the affected detector.** §10.0 fixes the order relative to the Phase 1 freezes. *(→ `HISTORY.md` H-04)*

---

## E2.A — Claim A: the tie comparator's default must be `available`

### A.1 Registered statement — `PREREG.md:117`, verbatim

> **Claim A — the tie comparator's default must be `available`.** With bar-close data and bar-open decisions, bar *i−1* closes at exactly the decision instant of row *i*. Under a `ties="unavailable"` default that cell is masked, so the canonical *clean* feature — a trailing window shifted off the decision bar — would be flagged. §2.3 locks the default on that argument. *(Both reviews of v9 proposed the opposite default. If `fixture_corrected` uses shifted features, the opposite default would fail pass-gate criterion 3 and fire kill criterion 2 against a method that works.)*

The lock it supports — `PREREG.md:192–193`, verbatim:

> | `available` **(default)** | `a(j,c) ≤ d(i)` |
> | `unavailable` | `a(j,c) < d(i)` |

and `PREREG.md:197`, verbatim:

> **The default is `available`, on the argument of §0.3 Claim A**, which Phase 1 verifies before the detectors are built. `unavailable` remains selectable for data where the boundary instant is genuinely unusable, and it is never the default.

### A.2 Operational TRUE/FALSE form

Claim A is not about which comparator is correct in general — both branches are defined and both remain
selectable. It is about which branch is the right **default**, and its argument has two links that can fail
independently.

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **A-i (mechanical)** | Under `ties="unavailable"`, a cell whose availability time equals the decision instant is masked; under `ties="available"` it is not. | The comparator applied to a boundary cell with `a(j,c) == d(i)` yields *unmasked* under `available` and *masked* under `unavailable`. | Either branch produces the other result, or the boundary case is ill-defined (floating-point or timezone equality does not hold where the construction says it should). |
| **A-ii (consequential)** | With bar-close data and bar-open decisions, the canonical *clean* feature is **not** flagged under `available` and **is** flagged under `unavailable`. | The boundary-instant probe produces no observable change under `available` and an observable change under `unavailable`. | The clean feature is flagged under `available` too (premise fails), **or** it is not flagged under `unavailable` either (the argued cost of the opposite default does not exist — the *justification* fails even if the conclusion is convenient). |

**A-ii is load-bearing.** A-i is close to definitional; its main value is catching a construction defect. A
third link — the parenthetical's fixture consequence — is **not verifiable by any Phase 1 construct**; see
FLAG 2.

### A.3 Measurement — synthetic only, no corpus, no detector code

**Constructs** (hand-built, discarded afterwards, per `PREREG.md:1007` "Write the throwaway mechanical tests
for the §0.3 verification list"):

- **A1 (boundary cell).** Single-entity frame, `n` rows, uniform bar duration `Δ`, `column_roles = at_bar_close` for the feature column, `decision_time = bar open`. Row *i*'s decision instant is `ts[i]`; bar *i−1* closes at `ts[i−1] + Δ == ts[i]`. Exactly one cell sits on the boundary. Timestamps must be integral in the frame's time unit so `a(j,c) == d(i)` holds *exactly*, not to within a tolerance — a floating-point near-equality silently answers a different question. This is verification item 2, `PREREG.md:126`.
- **A2 (canonical clean feature).** Same frame, pipeline computing a trailing rolling window shifted off the decision bar. Plus a deliberately *unclean* twin reading the decision bar, as a positive control: if the unclean twin is silent under both branches the harness is broken, not the claim.

**Procedure.** (1) Materialize `a(j,c)` for both constructs from the role table, including the final-row
carry-forward. (2) For each `ties` branch derive the unavailable set at the chosen decision instant using
`≤` versus `<`; record per cell masked/unmasked — **A-i output**. (3) For A2 under each branch: baseline-run
the clean pipeline, re-run with that branch's masked cells corrupted, compare bitwise per `PREREG.md:653`
("Runtime findings in exact mode are decided by **bitwise equality, not a tolerance.**"); repeat for the
unclean twin — **A-ii output**. (4) Run the identity control of `PREREG.md:686` on both branches; any delta
invalidates the run rather than producing a result.

**Decision rule — fixed and hashed before step 1 runs.**
- **CONFIRMED** iff A-i holds both directions, **and** A2-clean is silent under `available` and changes under `unavailable`, **and** A2-unclean changes under both, **and** the identity control is silent.
- **REFUTED-PREMISE** iff A2-clean changes under `available`.
- **REFUTED-JUSTIFICATION** iff A2-clean is silent under `unavailable` as well.
- Any other combination is **INCONCLUSIVE — construction defect**: fix and re-run. A construction defect is not a claim result and must not be filed as one.

**Detector code / corpus check — CONFIRMED CLEAN.** Needs only: an availability-time function for two column
roles; a comparison of two timestamps; a corruption of a cell set; a bitwise frame comparison. No `audit()`
surface, no detector, no shipped availability model. **Corpus contact: none.** It **cannot be reused as the
implementation** — that would make step 1's throwaway the detector, and the detector must be built after
step 4's freeze.

### A.4 Artifact — path and schema

```
evidence/phase1/claims/claimA/
  claimA_construct.py            # throwaway harness, hashed, retained as evidence
  claimA_capture.txt             # raw stdout of the run, unedited
  claimA_result.json             # the citable record
  claimA_decision_rule.md        # written and hashed BEFORE the run
```

```json
{
  "claim": "A",
  "prereg_ref": {"file": "PREREG.md", "section": "0.3", "line": 117, "commit": "<HEAD at run time>"},
  "verification_items": [2],
  "run": {"utc": "<iso8601>", "host_env_hash": "<sha256>", "harness_sha256": "<sha256>",
          "decision_rule_sha256": "<sha256 of claimA_decision_rule.md, timestamped before the run>"},
  "constructs": [
    {"id": "A1", "rows": 0, "bar_duration": "<unit>", "roles": {"<col>": "at_bar_close"},
     "decision_time": "bar_open", "boundary_cells": [[0, "<col>"]]}
  ],
  "link_A_i": {
    "available":   {"boundary_cell_masked": false},
    "unavailable": {"boundary_cell_masked": true},
    "holds": true
  },
  "link_A_ii": {
    "clean_pipeline":   {"available": "silent", "unavailable": "changed"},
    "unclean_control":  {"available": "changed", "unavailable": "changed"},
    "identity_control": {"available": "silent", "unavailable": "silent"},
    "holds": true
  },
  "verdict": "CONFIRMED | REFUTED-PREMISE | REFUTED-JUSTIFICATION | INCONCLUSIVE-CONSTRUCTION",
  "amendment_class_if_refuted": "SEE claimA_result.notes — AUTHOR DECISION REQUIRED",
  "notes": "<free text, including anything the run could not decide>"
}
```

### A.5 Pre-authorized rewrite path and amendment class

Governed by `PREREG.md:136` (quoted above), routed through the class table, and repeated in ordering terms
at `PREREG.md:1009`, verbatim:

> 3. Record the result. A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration; **a class C change requires an amended registration committed and timestamped before step 4** (§0.2.1).

**Which class is a default flip? AMBIGUOUS — AUTHOR DECISION REQUIRED. Not resolved here.**

- *Class A reading.* `PREREG.md:91`, verbatim: "| **A — mechanical branch facts** | A measurement selects between outcomes this document already defines | resolve, and record the fact | …". Both `ties` values are defined at `PREREG.md:192–193`; `unavailable` is explicitly retained as selectable at `PREREG.md:197`. Flipping the default selects between two pre-defined outcomes and adds no new branch — and `PREREG.md:93` scopes class C to a "*new* branch, unit, denominator, coverage state, tier licence, or acceptance criterion".
- *Class C reading.* The **default** is a distinct object from the branch, and it is locked in the lock table at `PREREG.md:35` ("| The tie comparator and its default | §2.3 | mask construction |"), not merely described. Registry entry 13, `PREREG.md:411`, verbatim: "13. **The tie comparator changes findings at the boundary instant.** *(29 Jul 2026)* The same pipeline is clean under one convention and leaking under the other." Every runtime rate is computed over findings, so a flip changes what published numbers mean — `PREREG.md:93`'s catch-all "anything that changes what a published number means". Further, resolving it as class A would leave `PREREG.md:192` printing "**(default)**" against `available` while the frozen configuration said otherwise — two copies of one rule, drifted.

**Common to both readings and not ambiguous:** the measurement is recorded in `DEVIATIONS.md` and the value
is serialized into `VALIDATED_CONFIG` either way, because `PREREG.md:635` names it explicitly ("**and the
complete `AvailabilityModel` of §2.3, including `ties`.**").

**What must not change under any refutation:** the comparator table itself (`PREREG.md:192–193`); the
requirement that both branches remain selectable (`PREREG.md:197`); consistency across §2.3, §4.3 and the
shipped mask (`PREREG.md:649`); `panel_mask_scope` remaining locked global (`PREREG.md:210`, `:214`); the
conformance suite's obligation to exercise both branches (`PREREG.md:885`).

> ⚠️ **Correction to F2 §A.5, found during this package's verification pass.** F2 states that "A flip that
> touches §2.3 and not §4.3 fails CI by construction." **It does not, today.** The entire ties-consistency
> check is a single *implementation-stage* stub — `tools/check_registration.py:720–723`
> (`check_ties_comparator_vs_mask` → `_artifact_absent("ties_comparator_vs_shipped_mask", …)`), wired at
> line 778 — and none of the 13 `prereg`-stage checks covers the §2.3↔§4.3 document-level comparison.
> The protection F2 relies on is registered (`PREREG.md:649`) but not implemented. This bears directly on
> §E3's recommendation; see E3.3.

### A.6 Dependencies and two flags

**Preconditions:** (1) `prereg-v30a` committed and timestamped — hard block. (2) The `a(j,c)` role mapping
for `at_bar_close` including final-row carry-forward. (3) `claimA_decision_rule.md` written and hashed
before the run. (4) Verification item 1 (the mixed frame, `PREREG.md:125`) should run first — it is the
availability-matrix precondition, and A-i/A-ii are meaningless if the matrix is wrong.

**FLAG 1 — Claim A may not be verified on the fixture. Hard prohibition, not a preference.**
`PREREG.md:480`, verbatim:

> **Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

`ties` is a default and is configuration by `PREREG.md:635`; the fixture chooses no defaults. Selecting or
confirming the tie default from fixture behaviour is barred twice over. The fixture's *declared* `ties`
value is a separate object belonging to the v30a declaration and must not be conflated with the tool's
default.

**FLAG 2 — the claim's registered justification can no longer be re-derived from the fixture.** The
parenthetical at `PREREG.md:117` reasons from "If `fixture_corrected` uses shifted features…". Phase 0's M5
result records that `fixture_corrected` carries decision-time violations on 7 of 8 instruments in 2025-08
including ZC itself, by a same-second-lattice mechanism unrelated to `ties`. **Claim A must therefore be
verified on its own mechanical merits, and the fixture-consequence sentence must not be treated as evidence
for the claim in either direction.** A limitation on what the verification can conclude, not a refutation.

**Invalidation risk to work already done: MODERATE-TO-HIGH** — not to any executed measurement, but to the
in-flight v30a draft. See the Part-1 mitigation above.

---

## E2.B — Claim B: reach as a scanned observation

### B.1 Registered statement — `PREREG.md:119`, verbatim

> **Claim B — reach is a scanned observation, and no dependency threshold is assumed.** Earlier versions searched for a boundary where the change "dies," which assumed the change's persistence is monotone in the boundary. **For an arbitrary callable it is not** (§8.5), so no single dependency-death threshold exists to find. The locked quantity instead: **full refinement scans the frozen candidate grid and reports the latest boundary at which the selected corruption strategy produced an observable change.** That is an observed perturbation extent, not an exact dependency boundary, and Phase 1 verifies the scan's calibration on known shapes rather than the monotonicity of arbitrary pipelines.

The rule it supports — `PREREG.md:945`, verbatim (opening):

> **Reach is a scanned observation, never an inferred dependency.** The refinement in `DESIGN.md` searches for the boundary at which masking stops changing the output. That search assumed the persistence of the change is monotone in the boundary, and **for an arbitrary user callable it is not**: a feature can depend on the masked region, stop depending as the mask shrinks, and depend again — three cells with baseline values (1, 1, 1), a constant corruption to 0, and a feature returning whether the sum lies in {0, 2} changes, does not change, and changes again as the mask narrows. A binary search over that returns the first cancellation and reports it as the answer.

The scoping sentence that fixes what Phase 1 is and is not asked to establish — `PREREG.md:955`, verbatim:

> Phase 1's calibration cases (§0.3 items 3 and 4) establish the formula on simple windows; they do not establish monotonicity for arbitrary callables, and §6.5 now carries a case that breaks it.

### B.2 Operational TRUE/FALSE form

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **B-i (definability)** | The reported quantity is well-defined without assuming monotonicity. | On a non-monotone construct, the full scan returns the **latest** changed boundary and the binary search returns an **earlier** one. | The full scan returns the earlier boundary (the definition is not what the scan computes), or the two procedures cannot be distinguished on the construct. |
| **B-ii (calibration, one bar)** | A feature reading exactly one unavailable cell scans to a reach of one bar. | Full scan returns one bar under both `ties` branches, with the terminal empty-mask boundary present in the grid. | Returns zero (the known historical failure mode), or any other value, under a correct grid with a passing identity control. |
| **B-iii (calibration, centered)** | A centered window of length *w* scans to about *w*/2 plus one bar. | Full scan returns ⌊*w*/2⌋+1 bars (or the pre-committed formula's prediction). | Any other value under a correct grid. |
| **B-iv (out of scope)** | Monotonicity for arbitrary callables. | — | **Not attempted.** `PREREG.md:955` says so explicitly; attempting it is scope creep with no gate behind it. |

**The decisive design point — separating an implementation defect from a claim refutation.** The scan
procedure lives in `DESIGN.md` and is revisable; the *expected values* are locked at `PREREG.md:127–128` and
`PREREG.md:510`. A mismatch therefore has two possible causes and the decision rule must distinguish them
**before** the run: a wrong grid (missing terminal empty-mask boundary; boundaries derived from row positions
rather than timestamps) is a **harness defect** — fix and re-run, no claim result; a verifiably correct grid
returning a different value is a **claim result**, and specifically a refutation of the registered
*calibration*, not of the scanned-observation definition.

The locked expected values — `PREREG.md:127` and `PREREG.md:128`, verbatim:

> 3. A feature reading exactly one unavailable cell, with the expected reach of one bar.
> 4. A centered window, with the expected reach of about half the window plus one bar.

and the case-family statement, `PREREG.md:510`, verbatim (excerpt):

> **a reach case per shape** — current-bar inclusion (one bar) and centered window (about half the window plus one bar); **and a non-monotone reach case** built to §8.5's three-cell shape, whose observable change reappears as the mask shrinks, on which a binary search must be shown to return the earlier boundary and the full scan the later one.

### B.3 Measurement — synthetic only, no corpus, no detector code

**Constructs:** **B1** current-bar inclusion (trailing window including the decision bar, uniform-Δ,
`at_bar_close`); **B2** centered window of fixed odd length *w* ≥ 7 so ⌊*w*/2⌋+1 is unambiguous; **B3**
non-monotone, built to the three-cell shape stated verbatim in `PREREG.md:945` — which removes any freedom
to shape it.

**Procedure.** (1) Build the candidate boundary grid from distinct availability times, **plus the terminal
empty-mask boundary**; assert the grid is timestamp-valued. (2) Walk the grid exhaustively, recording
change/no-change at every boundary; report the **latest** changed boundary. (3) For B3 only, additionally
run a binary search over the same grid and record its return. (4) Convert boundary → bars using the known Δ
and compare against the registered expectation. (5) Identity control at every boundary; comparison bitwise.
(6) Run B1 and B2 under **both** `ties` branches — the cheapest available insurance against a Claim A flip
invalidating Claim B's result.

**Decision rule — fixed and hashed before the run.**
- **CONFIRMED** iff B1 → one bar, B2 → the pre-committed centered value, B3 → full scan latest / binary search earlier, all under a grid that passes its own assertions and with silent identity controls.
- **REFUTED-CALIBRATION** iff B1 or B2 returns a value other than the registered expectation under a verified-correct grid. Record which, and the returned value.
- **REFUTED-DEFINITION** iff B3's full scan does not return the latest changed boundary. This is the serious one — it means the scanned quantity is not what `PREREG.md:949` says it is.
- **INCONCLUSIVE — harness defect** for any grid-assertion or identity-control failure.

**Detector code / corpus check — CONFIRMED CLEAN.** Uses a **throwaway scan**, not the shipped refinement —
it must, because the shipped refinement does not exist and cannot exist before step 4's freeze of "reach
definitions" (`PREREG.md:1010`). Needs a grid of timestamps, a loop, a corruption, a bitwise compare. No
policy layer, no cap, no `reach_basis` serialization, no finding object. **Corpus contact: none.**

One labelled inference, carried forward from F2: `PREREG.md:510`'s non-monotone case is a *case family in the
evaluation generator*, frozen at §10.0 step 5 — after this measurement. B3 is a separate hand-built object
with the same shape. That distinction is **not stated verbatim** anywhere; it follows from the §10.0
ordering and step 1's "throwaway mechanical tests". **Labelled as inference from ordering, not as a quoted
rule.**

### B.4 Artifact — path and schema

```
evidence/phase1/claims/claimB/
  claimB_constructs.py           # throwaway, hashed
  claimB_capture.txt
  claimB_grid_B1.csv             # per-boundary change/no-change, the raw scan trace
  claimB_grid_B2.csv
  claimB_grid_B3.csv
  claimB_result.json
  claimB_decision_rule.md        # hashed before the run
```

```json
{
  "claim": "B",
  "prereg_ref": {"file": "PREREG.md", "section": "0.3", "line": 119, "commit": "<HEAD at run time>"},
  "verification_items": [3, 4],
  "run": {"utc": "<iso8601>", "harness_sha256": "<sha256>", "decision_rule_sha256": "<sha256>"},
  "grid_assertions": {"timestamp_valued": true, "terminal_empty_mask_present": true},
  "constructs": [
    {"id": "B1", "shape": "current_bar_inclusion", "bar_duration": "<unit>",
     "grid_size": 0, "ties": "available",
     "expected_reach_bars": 1, "observed_reach_bars": 1, "basis": "full_scan",
     "trace": "claimB_grid_B1.csv", "identity_control": "silent"},
    {"id": "B2", "shape": "centered_window", "window_length": 0,
     "expected_reach_bars": 0, "observed_reach_bars": 0, "basis": "full_scan", "...": "..."},
    {"id": "B3", "shape": "non_monotone_three_cell",
     "full_scan_boundary_index": 0, "binary_search_boundary_index": 0,
     "full_scan_is_later": true, "trace": "claimB_grid_B3.csv"}
  ],
  "both_ties_branches_run": true,
  "verdict": "CONFIRMED | REFUTED-CALIBRATION | REFUTED-DEFINITION | INCONCLUSIVE-HARNESS",
  "out_of_scope_declared": ["monotonicity for arbitrary callables — PREREG.md:955"],
  "notes": "<free text>"
}
```

### B.5 Pre-authorized rewrite path and amendment class

Governed by `PREREG.md:136`. The class assignment splits by which link failed:

- **REFUTED-CALIBRATION.** Arguably class A — the document defines the quantity and the measurement fills in its value on a known shape. But `PREREG.md:510`'s expectations are also the acceptance conditions for two evaluation **case families**, and a case family's required behaviour is close to `PREREG.md:93`'s "acceptance criterion". **AMBIGUOUS — AUTHOR DECISION REQUIRED.** The split is recorded, not resolved. If the author wants a route defensible under either reading, the class C route is it: `PREREG.md:95` permits an amendment and nothing forbids amending where class A would have sufficed.
- **REFUTED-DEFINITION.** Class C, stated with more confidence: `reach` is a published field with a serialized `reach_basis` (`PREREG.md:951`), and a change to what the full scan returns changes what that published field means. The amendment must precede step 4's freeze of "reach definitions" (`PREREG.md:1010`).

**What must not change under any refutation:** the prohibition on labelling a binary-searched reach as exact
(`PREREG.md:950`); the above-cap fallback with `reach_basis = lower_bound` serialized (`PREREG.md:951`);
`reach_refinement_policy` remaining frozen configuration (`PREREG.md:952`); the `exact`-refers-to-the-scan
sentence (`PREREG.md:953`); the suppression rule (`PREREG.md:957`); the cost consequences (`PREREG.md:1064`)
and the grid cap — a calibration correction does not license reopening the cost model.

### B.6 Dependencies

(1) `prereg-v30a` — hard block. (2) Verification item 1 (mixed frame) — same precondition as Claim A.
(3) Claim A **need not** precede Claim B if B1/B2 run under both branches (recommended); under one branch
only, Claim A must resolve first. (4) Nothing else — reach refinement's Phase 2 implementation is
downstream.

**Invalidation risk to work already done: LOW.** Forward exposure only: `PREREG.md:1010` freezes reach
definitions at step 4, and `PREREG.md:497` freezes the evaluation generator at step 5 "**after Claims A–C are
resolved**", so a late refutation after step 5 forces a snapshot discard under `PREREG.md:1014`.

---

## E2.C — Claim C: permutation strategies are probabilistic at the decisive cell

### C.1 Registered statement — `PREREG.md:121`, verbatim

> **Claim C — permutation strategies are probabilistic at the decisive cell.** A permutation can leave any given cell where it was, so a real leak may go undetected at an individual cohort. Registry entries 14 and 16 rest on this, and it is why §3's dtype-preservation condition is costly rather than free.

What rests on it, all locked: `PREREG.md:412` (registry 14), `PREREG.md:415` (registry 16), `PREREG.md:305`
(§3.2's cost paragraph), and the reporting guarantee, `PREREG.md:941`, verbatim:

> **A partial cohort count is not weak evidence.** Permutation strategies can leave the decisive cell fixed (Claim C, registry 14), so "found in 18 of 20 cohorts" is the expected shape of a real leak and the report says so.

The only quantitative form anywhere is in the **revisable** file — `DESIGN.md:172`, quoted to locate it, not
as a governing clause: "with *m* masked cells the per-cohort miss probability is roughly `1/m`."

### C.2 Operational TRUE/FALSE form

Claim C is a claim of **weakness**, which inverts the usual burden: confirming it needs one observed miss;
refuting it requires establishing a negative, which needs a stated repetition count and a stated bound. **The
registration supplies neither.**

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **C-i (existence)** | A permutation can leave the decisive cell where it was, so a real leak may go undetected at an individual cohort. | At least one silent probe is observed on a construct with a known leak, across repeated permutations. | Zero silences across *R* repetitions, with *R* large enough that the pre-committed upper bound on the miss rate excludes the predicted rate. |
| **C-ii (shape)** | Partial cohort counts are the expected shape of a real finding. | The observed silence count across cohorts is strictly between zero and all, on a construct whose leak is present at every cohort. | Silence is all-or-nothing across cohorts — the mechanism is not per-cohort-independent and `PREREG.md:941`'s reassurance is misdescribed. |
| **C-iii (rate, `DESIGN.md` only)** | Per-cohort miss probability ≈ `1/m`. | Observed miss rate consistent with `1/m` at the pre-committed tolerance. | Materially different. **A `DESIGN.md` statement, not a locked one** — a mismatch is a `DESIGN.md` correction, not a claim refutation. Recorded on a separate axis so it cannot be smuggled into the claim verdict. |

### C.3 Measurement — synthetic only, no corpus, no detector code

**Constructs:** **C1** single decisive cell — the pipeline's output depends on exactly one masked cell, in a
way that is *not* symmetric over the masked set; mask size *m* set explicitly and run at two values (e.g. 4
and 20) so the rate has a slope to check. This is verification item 5, `PREREG.md:129`. **C2** negative
control for the *other* blind spot — a statistic over the entire masked region, on which `shuffle` should be
silent on every repetition. C2's purpose is to prove the harness can tell the two blind spots apart;
reporting C2's silences as Claim C evidence would repeat the v17 error recorded at `HISTORY.md:198`.

**Procedure.** (1) Fix a decisive cell and a mask of size *m*; run both axes — *R* independent seeds per
cohort, *K* cohorts. (2) For each (cohort, seed): permute masked cells per column, re-run, compare bitwise;
record change/silence **and** whether the decisive cell was in fact left at its original position. Recording
the fixed point directly is what makes a zero-silence result interpretable rather than merely negative.
(3) Run C2 identically. (4) Identity control; bitwise comparison.

**Decision rule — fixed and hashed before the run. THE PARAMETERS ARE UNSPECIFIED IN THE REGISTRATION.**
`PREREG.md:129` asks only "to establish that partial cohort counts occur". Verbatim:

> 5. A repeated permutation probe on a known leak, to establish that partial cohort counts occur.

It fixes no repetition count, no silence threshold, no tolerance. **These are plan-level test-design choices,
not registered parameters, and they are not class B** — class B at `PREREG.md:92` requires "the form, search
space, objective, denominator, and freeze point [to be] already fixed", and none are. They must be written
into `claimC_decision_rule.md` and hashed before the run, so the burden of proof cannot be adjusted after
seeing the silence count.

- **CONFIRMED** iff at least one silence on C1 **and** that silence coincides with an observed fixed point at the decisive cell **and** C2 is silent throughout **and** the identity control is silent.
- **REFUTED-EXISTENCE** iff zero silences across *R*×*K* trials on C1 with the pre-committed *R* large enough that the one-sided upper bound on the per-trial miss rate falls below the smallest rate that would matter to `PREREG.md:941`'s reporting guarantee. State that rate in the decision rule.
- **DESIGN-MISMATCH (separate axis, never the claim verdict)** if the observed rate is inconsistent with `1/m` at the pre-committed tolerance across the two *m* values.
- **INCONCLUSIVE — harness defect** if C2 ever changes, or the identity control moves, or a recorded silence does not coincide with a fixed point.

**Detector code / corpus check — CONFIRMED CLEAN.** Needs a permutation with a seed, a mask, a re-run, and a
bitwise compare. Does **not** need strategy escalation, tier resolution, cohort scheduling policy,
compatibility accounting, or the `EvidenceEvent` machinery. **Corpus contact: none.**

**FLAG — this measurement must not be read as selecting `shuffle` scope or `shuffle`'s required/optional
status.** `PREREG.md:635` lists "shuffle scope" as frozen configuration; `PREREG.md:92` puts "strategy order"
in class B, to be selected on the development corpus — and development-corpus access is blocked by
`PREREG.md:1006` until v30a. The Claim C measurement fixes a scope *for the test* and must record which
scope it assumed; it does not select the shipped one.

### C.4 Artifact — path and schema

```
evidence/phase1/claims/claimC/
  claimC_constructs.py           # throwaway, hashed
  claimC_capture.txt
  claimC_trials.csv              # one row per (construct, cohort, seed): fixed_point, changed, m
  claimC_result.json
  claimC_decision_rule.md        # hashed before the run; carries R, K, the bound, the tolerance
```

```json
{
  "claim": "C",
  "prereg_ref": {"file": "PREREG.md", "section": "0.3", "line": 121, "commit": "<HEAD at run time>"},
  "verification_items": [5],
  "run": {"utc": "<iso8601>", "harness_sha256": "<sha256>", "decision_rule_sha256": "<sha256>"},
  "assumed_shuffle_scope": "<within-masked-cells-per-column | other>  # assumed for the test, NOT selected",
  "design": {"cohorts_K": 0, "seeds_per_cohort_R": 0, "mask_sizes_m": [4, 20],
             "precommitted_miss_rate_floor": 0.0, "precommitted_rate_tolerance": 0.0},
  "C1": {
    "trials": 0, "silences": 0, "fixed_points": 0,
    "silences_coinciding_with_fixed_point": 0,
    "per_cohort_silence_counts": [0],
    "partial_cohort_count_observed": true,
    "observed_miss_rate_by_m": {"4": 0.0, "20": 0.0}
  },
  "C2_negative_control": {"trials": 0, "changes": 0, "expected_changes": 0},
  "identity_control": "silent",
  "verdict": "CONFIRMED | REFUTED-EXISTENCE | INCONCLUSIVE-HARNESS",
  "design_md_rate_axis": "CONSISTENT | MISMATCH  # DESIGN.md:172 only; never the claim verdict",
  "notes": "<free text>"
}
```

### C.5 Pre-authorized rewrite path and amendment class

Governed by `PREREG.md:136`. The class depends on direction, and one direction is genuinely awkward:

- **REFUTED-EXISTENCE (`shuffle` never misses).** This would *strengthen* the tool, which is exactly why it needs more care rather than less. It would falsify registry 14, narrow registry 16, contradict §3.2's cost paragraph, and make `PREREG.md:941`'s reporting guarantee describe a shape that does not occur. That clause sits inside §8, *Reporting guarantees* — it tells a user what a published cohort count means — so changing it changes what a published number means. **F2's reading is class C, flagged as a reading and not a determination**, because the counter-argument is available (nothing new is introduced; a registry entry is narrowed, not a branch added). Note also `PREREG.md:397`, verbatim: "**Additions are dated, whether or not convenient.**" — the registry's stated discipline is about additions and says nothing about removals, so removal has no pre-authorized form.
- **REFUTED-SHAPE (silence all-or-nothing rather than partial).** Same reasoning, same section, same reading.
- **DESIGN-MISMATCH on the `1/m` rate.** Not a claim refutation. `DESIGN.md` is revisable — but `PREREG.md:645` ("It fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md`") makes the boundary worth checking before editing: correct the sentence in place, do not migrate a rate formula into `PREREG.md` as a side effect.

**What must not change under any refutation:** the dtype-preservation licence itself (`PREREG.md:302`) —
Claim C explains why that licence is *costly*, it is not the licence's justification, and weakening §3.2
because `shuffle` turned out reliable would be a tier-licence change, which `PREREG.md:93` names explicitly;
`PREREG.md:301`'s promotion facts; the distinction between the fixed-point blind spot and the
whole-masked-region blind spot; the scoring unit and its deduplication (`PREREG.md:244`).

### C.6 Dependencies

(1) `prereg-v30a` — hard block. (2) `claimC_decision_rule.md` with *R*, *K*, the miss-rate floor and the
tolerance, hashed before the run — without it a null result is uninterpretable and, worse, adjustable.
(3) Independent of Claims A and B; can run in parallel with B once verification item 1 has passed.

**Invalidation risk to work already done: LOW.** Forward exposure is that four locked text sites move
together if it falls — a lot of surface for one measurement.

---

## E2.D — Flagged author decisions, carried forward in full

**Four items. None is resolved here; all four are the author's.**

| # | Decision | The two positions | Where stated |
|---|---|---|---|
| **AD-1** | **Amendment class for a `ties` default flip** — class A or class C | A: both branches are pre-defined, so a flip selects between defined outcomes (`PREREG.md:91`, `:192–193`, `:197`). C: the *default* is a distinct locked object (`PREREG.md:35`) and registry 13 (`PREREG.md:411`) says the comparator changes findings at the boundary, so a flip changes what published numbers mean (`PREREG.md:93`) | §E2.A.5 |
| **AD-2** | **Amendment class for a reach-calibration correction** — class A or class C | A: the document defines the quantity; the measurement fills in a value on a known shape. C: `PREREG.md:510`'s per-shape expectations are also two case families' acceptance conditions, and "acceptance criterion" is class C by name | §E2.B.5 |
| **AD-3** | **Amendment class for a Claim C refutation** | F2 reads it as class C via `PREREG.md:941`'s status as a reporting guarantee; the counter-reading (a registry entry narrowed, no new branch) is available. Registry discipline covers additions only (`PREREG.md:397`), so removal has no pre-authorized form | §E2.C.5 |
| **AD-4** | **Claim C's repetition count *R*, cohort count *K*, miss-rate floor, and rate tolerance** | **UNSPECIFIED IN THE REGISTRATION.** `PREREG.md:129` asks only that partial cohort counts "occur". Proposed as plan-level choices requiring pre-run hashing. **Explicitly NOT class B** — `PREREG.md:92` requires form, search space, objective, denominator and freeze point to be already fixed, and none are | §E2.C.3 |

**A fifth item worth the author's attention, upstream of all four:** AD-1 is entangled with the v30a
drafting instruction in Part 1. If the amendment's replacement criterion is written tie-branch-invariant,
AD-1 stops being urgent; if it is not, AD-1 must resolve before the tag or a second amendment becomes likely.

---

## E2.E — Proposed execution order

Steps −1, 0, 7 and 8 are locked by `PREREG.md:1006–1014`; the ordering inside 1–6 is a proposal.

| # | Step | Authority |
|---|---|---|
| **−1** | `prereg-v30a` committed, signed, hashed, OTS-stamped, repository publicly reachable. Draft its replacement criterion tie-branch-invariant | `PREREG.md:1006`, `:1033`, `:95`, `:97` |
| **0** | Write and hash `claim{A,B,C}_decision_rule.md`. Record hashes before any construct runs | Part-1 hazard 2; `PREREG.md:104` |
| **1** | **Item 1 — mixed frame.** Precondition for everything else | `PREREG.md:125` |
| **2** | **Claim A** — item 2, constructs A1/A2, both branches | `PREREG.md:126`, `:117` |
| **3** | **Claim B** — items 3 and 4, both `ties` branches; B3 for the non-monotone definition check. Parallel with 4 | `PREREG.md:127–128`, `:945`, `:510` |
| **4** | **Claim C** — item 5, constructs C1/C2. Parallel with 3 | `PREREG.md:129` |
| **5** | Items 6–8 — the §6.10 comparator cases. Outside F2's scope, inside the same gate | `PREREG.md:130–132`, `:134` |
| **6** | Assemble `evidence/phase1/claims/CLAIMS_ABC_RESULT.json` — an index over the three records with verdicts, harness hashes, decision-rule hashes | `PREREG.md:1009` |
| **7** | **Record the result.** Class A/B → `DEVIATIONS.md` + `VALIDATED_CONFIG`. Class C → amended registration committed and timestamped **before** step 8 | `PREREG.md:1009`, `:136`, `:95` |
| **8** | Freeze comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, reach definitions. Then and only then: generator snapshot, conformance suite | `PREREG.md:1010–1014` |

**Why item 1 goes first.** It is the only case the registration singles out as "the thinnest part of the
specification" and the site of a prior death. If `a(j,c)` is wrong for a forward-filled exogenous column,
every A/B/C result measures the wrong matrix.

**Where the first delta should stop.** At step 6, with three `*_result.json` files and an index. Steps 7 and
8 are author actions with ceremony attached and do not belong in the same delta as the runs producing their
inputs.

---

# §E3 — Repository readiness: 17 gaps

Format per gap: **what is missing → why Phase 1 needs it → what would create it → does it touch a registered
document?**

**Registered-document status F3 worked from**, reproduced because it makes the classification auditable:
`PREREG.md` locked (change = class C amendment + new tag); `DESIGN.md` and `README.md` revisable;
`HISTORY.md` hashed at tag, revisability **not stated** (unresolved); `DEVIATIONS.md` append-only and Phase 1
is *required* to append; `VALIDATED_CONFIG.toml` a registered placeholder meant to be filled per phase;
`tools/check_registration.py` and `protocol/runtime_reference.py` registered **and hashed at the tag**;
`tests/registration/*` registered but not individually hashed.

**Baseline that all seventeen sit against.** 22 tracked files, matching §11 item 1 exactly. Suite green — 137
passed, 0 failed, in 0.66 s on Python 3.12.10 / pytest 9.1.1. `--stage prereg` PASS, 13/13 checks, 8 deferred
and named, exit 0. Byte-exactness verified against a hostile `core.autocrlf=true` clone: zero CRLF, all five
published hashes reproduce. **The tag gate holds.**

---

## E3.1 — Group 1: fillable WITHOUT touching any registered document (9 gaps)

All nine are **new files in new paths**. None edits a file that exists at `fe0d5a5`. None affects the tag,
the published hashes, or `--stage prereg`.

| # | What is missing | Why Phase 1 needs it | What would create it | Touches a registered doc? |
|---|---|---|---|---|
| **G1** | A directory for the §10.0 step 1 **throwaway mechanical tests**, separate from `tests/registration/` | `PREREG.md:1007` requires them. Putting them in `tests/registration/` would feed `check_structure`'s `test_*.py` glob (`check_registration.py:198`) and let throwaway files stand in as evidence the §6.6.1 suite exists | New `tests/phase1/` (or similar) + its own `conftest.py` replicating the `parents[2]` bootstrap | **No** — new path, invisible to `REQUIRED_PATHS` and to the glob |
| **G2** | **Suite separation** — a marker, `testpaths`, or a documented two-command split, so the registration suite's greenness is not entangled with Phase 1 tests that are *expected* to fail mid-investigation | The tag gate cites suite greenness (`PREREG.md:647`); after G1 a bare `python -m pytest` would mix them | `pyproject.toml [tool.pytest.ini_options]`, or `pytest.ini`, or a documented convention | **No** — new file. ⚠️ Caveat: creating `pyproject.toml` changes pytest's inferred rootdir anchor. Same directory, so no behavioural change expected, but **confirm by re-running the 137 tests before and after, do not assume** |
| **G3** | **Dependency pins + a declared Python floor** | Phase 1 measurements on pandas/numpy frames must be reproducible; §11 item 7 hashes artifacts, which proves immutability but not regenerability | `requirements-phase1.txt`, or `pyproject.toml` with `requires-python = ">=3.11"` | **No** — new file |
| **G4** | **A virtual environment**, isolated from the global interpreter shared with unrelated Desktop work | Prevents an unrelated `pip install` from silently changing a Phase 1 result or pytest's plugin set (`anyio`, `dash` autoload today) | `python -m venv .venv` + a `.gitignore` line | **No** for the venv itself; ⚠️ the `.gitignore` line is a registered-file edit — see C8 |
| **G5** | **An environment record** — interpreter, OS, library versions, captured at measurement time | Reproducing a Phase 1 number needs the environment, not just the artifact hash. Prior art outside the repo at `evidence\fixture_spike\c5\env_records.md` | New file under the Phase 1 artifact directory | **No** — new path |
| **G6** | **A location + format convention for §11 item 7 artifacts** (generator snapshot, conformance suite, parameter distributions, adjudication rubrics, beacon records, generated manifests) with their own hash files | `PREREG.md:1054` requires them "frozen in their own files with their own hashes"; there is no `snapshots/`, `manifests/`, or precedent format in the repo | New directories + a manifest-format decision. Prior art outside the repo: `evidence\fixture_spike\f3\fixture_manifest_DRAFT.json`, `.sha256` sidecars under `evidence\fixture_spike\f2\out\` | **No** — new paths |
| **G7** | **Hashing / manifest tooling** to produce and re-verify G6's hashes | §10.0 steps 5 and 6 both say "**Generate and hash**"; there is no hashing utility in the repo | New script, e.g. `tools/hash_manifest.py` | **No** — new file in `tools/`; `tools/` is not a package, so a new module there imports nothing and is imported by nothing |
| **G8** | **CI configuration** running the two gate commands | `PREREG.md:647` defines the gate; today it is enforced only by hand. No `.github/`, no active hooks, no Makefile | New `.github/workflows/*.yml` running `python -m pytest tests/registration` and `python tools/check_registration.py --stage prereg`. Must **not** make `--stage implementation`/`release` required yet — `_artifact_absent` correctly returns exit 1 today, and wiring them would make CI permanently red for a correct repo | **No** — new path |
| **G9** | **A shared path-bootstrap** (or a decision to keep duplicating it) | Four hand-written `sys.path` bootstraps with two different `parents[N]` values already exist; each new Phase 1 entry point adds a fifth | Either a `pyproject.toml` making the repo installable in editable mode, or an accepted convention documented once | **No** for a new `pyproject.toml`. ⚠️ But an installable package raises the `leakaudit/` layout question (C6), which is not a readiness call |

---

## E3.2 — Group 2: cannot be filled without touching a registered document (8 gaps)

| # | What is missing | Why Phase 1 needs it | What would create it | Which registered file, and its status |
|---|---|---|---|---|
| **C1** | **The implementation-stage checks are stubs.** All five return `_artifact_absent(...)` (`check_registration.py:714–717`, wired at 778–782). When Phase 1 freezes the comparator and permitted promotion sets, `shipping_defaults_vs_validated_runtime`, `ties_comparator_vs_shipped_mask`, `l31b_inequalities_vs_shipped_rule`, `deleted_config_fields_rejected` must become real checks | `PREREG.md:649` requires the CI script to diff shipping defaults against the frozen section and check comparator consistency; `PREREG.md:647` explicitly anticipates this — the stubs exist *to be replaced* | Editing `tools/check_registration.py` | **`tools/check_registration.py`** — registered at `fe0d5a5` **and SHA-256-published in both the tag message and `README.md:34`**. `README.md:23` names only `DESIGN.md` and the README as revisable; it does **not** cover this file |
| **C2** | **`DEVIATIONS.md` is empty and Phase 1 must write to it** | `PREREG.md:1009` — "A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration" | Appending entries | **`DEVIATIONS.md`** — registered; `PREREG.md:1053` makes it **append-only** and §10.0 step 3 *requires* the append. Mandated, not a violation. **Constraint: append only, never edit or reorder** |
| **C3** | **`VALIDATED_CONFIG.toml` carries no values** (four empty tables) | §10.0 step 4 freezes the comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form and reach definitions; `PREREG.md:633` requires each serialized into and hashed with the applicable section | Populating `[validated.runtime]` etc. | **`VALIDATED_CONFIG.toml`** — registered placeholder; filling it is the designed lifecycle. `check_config_schema` requires all four tables to remain present — **do not remove a table, only add keys** |
| **C4** | **The reducer does not compute §7.5 per-strategy diagnostics or §6.11 compatibility-escalation arithmetic** | `runtime_reference.py:29–32` states both are deliberately outside it and that neither may be published until the module grows them. Phase 1 step 4 freezes the compatibility-threshold form, whose arithmetic (`f ≥ m` **and** `f/n > q`, `PREREG.md:697`) lands here | Editing `protocol/runtime_reference.py` | **`protocol/runtime_reference.py`** — registered **and SHA-256-published at the tag** (`README.md:35`). `PREREG.md:1048` says "**at minimum**" those seven functions, so growth is licensed by locked text; the published hash still moves |
| **C5** | **The README's hash block does not say which of the five files are allowed to move** | Once C1 or C4 lands, `HEAD` hashes for the two tooling files will differ from the tag's, and a reader has no in-repo statement that this is legitimate for those two | Editing `README.md:22–26` to extend the revisability sentence, or adding a note under the hash block | **`README.md`** — explicitly **revisable** (`README.md:23`). The cheapest Group-2 item and the one that keeps C1/C4 legible to an outside auditor |
| **C6** | **`DESIGN.md` illustrates a `leakaudit.protocol` import path** (`DESIGN.md:411`) that does not exist, importing a `resolve_tier` that does not exist | If Phase 1 tooling is written against `DESIGN.md:411` it will not import. `PREREG.md:1048` pins `protocol/runtime_reference.py` and `check_structure` enforces it | Either revise `DESIGN.md` to match the registered layout, or leave it as a forward sketch and document the distinction | **`DESIGN.md`** — explicitly **revisable**. ⚠️ Constraint: `check_single_source` fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md` (`PREREG.md:645`). Any edit must re-run `--stage prereg` |
| **C7** | **No cost script exists**, and `cost_script_total` is a stub (`check_registration.py:741–743`, wired at 782) | `PREREG.md:1000` — "Computed by the CI script of §6.8, not by hand"; `PREREG.md:1064` — "**the CI cost script computes it from `VALIDATED_CONFIG` and the README quotes the script's output**" | A new script (Group 1) **plus** rewiring `check_cost_script` (Group 2) **plus** a README edit to quote its output | Script itself: **no**. Rewiring: **`tools/check_registration.py`**. Quoting the total: **`README.md`** (revisable) |
| **C8** | **`.gitignore` does not cover the Phase 1 working tree** — no `.venv/`, and untracked material shows as `??` on every `git status` | Noise in `git status` is how an accidental commit of scratch material gets missed in a registration repo | Editing `.gitignore` | **`.gitignore`** — registered at `fe0d5a5`, **not** in the published hash list, not named in any §11 clause. Lowest-consequence Group-2 edit, but still a file that existed at the registration commit |

**`PREREG.md` appears in no gap above.** No Phase 1 readiness item requires editing it. The one thing that
would — a class C change discovered during §0.3 verification — is `PREREG.md:1009`'s own branch and routes
through an amended registration, not through repo setup.

---

## E3.3 — The delta's question, answered

> **Of the 3 gaps that would move a published SHA-256, which should be folded into THIS ceremony rather than
> a later one?**

### The three, and a factual correction to the premise

The three are **C1**, **C4**, and **the rewiring half of C7**. Two files carry them:

- **`tools/check_registration.py`** — C1 and C7's rewiring half;
- **`protocol/runtime_reference.py`** — C4.

**Both files are in the pending ceremony's six-hash set.** I verified the set directly from
`evidence\ceremony\CEREMONY_COMMANDS.md:282`, verbatim:

> `FILES="PREREG.md DESIGN.md HISTORY.md tools/check_registration.py protocol/runtime_reference.py AVAILABILITY_DECLARATION.md"`

with line 280 recording that six is the current decision per declaration §D.2 and that a seventh
(`PRIOR_ART_VERIFICATION.md`) remains an open author item. Line 285 records the ordering rationale: the
declaration is appended **last** so the v30 five-line block stays a verbatim prefix of the v30a six-line
block.

So the delta's exclusion clause — "a change to a file NOT in the six-set is not made cheaper by this ceremony
at all" — **excludes none of the three.** All three are in scope on cheapness grounds, and the decision has
to be made on other criteria. The criterion I applied is: *can this change be authored correctly today, from
locked text alone, without pre-empting a §10.0 step that has not run?*

### Recommendations — these are RECOMMENDATIONS, not decisions

---

#### C1 (full) — **RECOMMEND: DEFER to a later ceremony**

**Reasoning.** The four implementation stubs check *against artifacts §10.0 step 4 has not yet produced*.
`PREREG.md:647` says so in the registration's own words, verbatim:

> Two of the checks below cannot pass before detector code exists — shipping defaults against the frozen `[validated.runtime]`, and the `ties` comparator against the shipped mask — while §11 requires the checker in the first commit.

Writing them now would either check nothing, or encode a comparator state and a set of permitted promotions
that Claims A–C may move — and Claim A's verification is **step 2**, before step 4's freeze
(`PREREG.md:1008`, `:1010`). Folding the full C1 into this ceremony inverts the registration's own ordering,
and does so in a file whose hash the ceremony publishes. **The cheapness gain does not survive the ordering
cost.** Defer to the ceremony that follows step 4.

---

#### C1 (partial — the §2.3↔§4.3 document-level ties-consistency check) — **RECOMMEND: FOLD IN, conditionally.** This is my one positive recommendation of the three.

**What it is.** `PREREG.md:649` requires the CI script to check, verbatim (excerpt):

> that the `ties` comparator is consistent across §2.3, §4.3, and the shipped mask; that §4.3's inequalities match the shipped rule

That is **two** comparisons welded into one sentence. The "§2.3 versus §4.3" half is a **document-to-document
check** — `PREREG.md:192–193`'s comparator table against `PREREG.md:352–353`'s inequality table:

> | `available` | `A + E > D` |
> | `unavailable` | `A + E ≥ D` |

against

> | `available` **(default)** | `a(j,c) ≤ d(i)` |
> | `unavailable` | `a(j,c) < d(i)` |

It needs no shipped mask, no frozen configuration, no detector, and no Phase 1 output. It is fully
specifiable from locked text **today**.

**Why now rather than later — four reasons.**

1. **Today it is checked at no stage at all.** `check_ties_comparator_vs_mask` is a single implementation-stage stub (`tools/check_registration.py:720–723`, wired at line 778), and none of the 13 `prereg`-stage checks covers the document-level half. The registration requires the check; the repository does not perform it, at any stage.
2. **It is the protection Claim A's rewrite path already assumes exists.** F2 §A.5 states that a flip touching §2.3 and not §4.3 "fails CI by construction". As verified above, that is not true today. Claim A is the *first* substantive thing Phase 1 does, and a `ties` flip is exactly the edit this check exists to catch.
3. **It also guards RS-3's neighbour and PS-4's terminology, indirectly** — anything that keeps the two comparator statements in lockstep reduces the drift `PREREG.md:77`'s single-source rule exists to prevent.
4. **The hash is being recomputed anyway.** The marginal cost is the edit plus re-verification, not a new hash-publication event; after the tag it becomes an edit that diverges `HEAD` from a *second* published hash set and forces C5 to cover two tags rather than one.

**The counter-argument, stated because it is real.** `PREREG.md:95` calls the amendment "a `prereg-v30a`
tag, not a restart". The amendment exists to carry the class C replacement acceptance criterion. Bundling
unrelated tooling growth into it muddies what the amendment amends, and an auditor reading the v30a diff
will see a checker change adjacent to a criterion change. That is a legitimate reason to keep the ceremony
minimal, and it is the strongest argument against my recommendation.

**Conditions I would attach.** Fold in **only if** all of these hold:
- the checker change is a *new* prereg-stage check, additive, leaving the existing 13 untouched in behaviour;
- the full gate is re-run before the ceremony's A10 step — `python -m pytest tests/registration` green **and** `--stage prereg` exit 0 — with the new count recorded (it will be 14 prereg checks, not 13, and the checklist's "13/13" expectation becomes stale);
- the v30a tag message or the ceremony record notes the checker change explicitly, so the amendment's scope is legible;
- C5 lands in the same pass (see below).

⚠️ **A cost this raises that the author should weigh.** `CEREMONY_COMMANDS.md:133` already records open item
10: the prereg gate has **not** been re-run against the current tree, and the checklist's PASS is from
2026-08-12, predating `DESIGN.md` §2.11, H-L13 and H-34. Adding a checker change makes that re-run
mandatory rather than merely advisable. **If the author is not prepared to re-run and re-verify the gate
before tagging, defer this too** — a stale gate result attached to a changed checker is worse than either
problem alone.

---

#### C4 — **RECOMMEND: DEFER to a later ceremony**

**Reasoning.** The compatibility arithmetic C4 would add is `f ≥ m` **and** `f/n > q` (`PREREG.md:697`), and
its *form* is frozen at §10.0 step 4 — after Claims A–C. Worse, **CT-4 flags the objective behind `m` and
`q` as unresolved and at high risk of routing to class C.** Implementing the arithmetic now would encode a
form whose own class-B eligibility is in question.

There is also no cost to waiting. `PREREG.md:620` blocks *publication*, not implementation, verbatim:

> **A runtime metric is published only if the reference reducer computes it.** A number named here but absent from the reducer does not exist and may not appear in the README, a post, or an application.

Nothing is published before the Phase 2 freeze. And `PREREG.md:1048`'s "**at minimum**" licenses the reducer's
growth whenever it happens — the licence does not expire with this tag. **Defer.**

---

#### C7 (rewiring half) — **RECOMMEND: DEFER to a later ceremony**

**Reasoning.** The cost script computes the total *from `VALIDATED_CONFIG`* — `PREREG.md:1064`, verbatim
(excerpt):

> The figure depends on the frozen strategy set and on how many distinct promotion targets it contains, so **the CI cost script computes it from `VALIDATED_CONFIG` and the README quotes the script's output.**

`VALIDATED_CONFIG.toml` is the placeholder with four empty tables. **There is nothing to compute.** Rewiring
`check_cost_script` now would replace a stub that correctly says "does not exist yet" with a check that
reads an empty configuration — strictly worse. The Group-1 half (writing the script) can proceed
independently at any time and touches nothing registered; the rewiring waits for C3.

---

### One adjacent item I would rank ahead of all three — **C5**

C5 is **not** one of the three SHA-256-moving gaps, and `README.md` is **not** in the six-hash set. But the
ceremony already opens `README.md`: step H4 pastes the v30a six-line block into it, and
`CEREMONY_COMMANDS.md:379–380` records that the README will then carry **eleven hash lines — the v30 five and
the v30a six**. So C5 is cheap now in a different sense from the other three: cheap because the file is
already being edited, not because a hash is already being recomputed.

**Recommendation: FOLD IN.** The gap C5 names — no in-repo statement of which hashed files may legitimately
move at `HEAD` — gets strictly worse the moment the README carries two hash blocks from two tags. An auditor
reading eleven hashes with `README.md:22–26` naming only `DESIGN.md` and the README as revisable has no way
to tell a legitimate divergence from tampering. F3's own bottom line already called this "the one gap worth
closing first because it costs nothing and it is what an outside auditor will check"; the ceremony makes it
more necessary, not less. It is also the **prerequisite** that makes C1 and C4 legible whenever they do land.

---

### Summary of the E3.3 recommendations

| Gap | In the six-set? | Recommendation | Primary reason |
|---|---|---|---|
| **C1 (full)** | Yes — `tools/check_registration.py` | **Defer** | Checks artifacts §10.0 step 4 has not produced; folding it in inverts the registration's own ordering |
| **C1 (§2.3↔§4.3 document half)** | Yes — same file | **Fold in, conditionally** | Fully specifiable from locked text today; currently checked at no stage; it is the protection Claim A's rewrite path already assumes exists |
| **C4** | Yes — `protocol/runtime_reference.py` | **Defer** | Form frozen at step 4; CT-4 flags its objective unresolved; nothing is published before Phase 2, so waiting costs nothing |
| **C7 (rewiring half)** | Yes — `tools/check_registration.py` | **Defer** | `VALIDATED_CONFIG` is empty; there is nothing for the cost check to compute |
| **C5** *(adjacent, not one of the three)* | No — but the ceremony edits `README.md` anyway | **Fold in** | Eleven hash lines across two tags with no statement of which may move; prerequisite for C1/C4 whenever they land |

**All five lines above are recommendations. None is a decision.** The two that would change the ceremony's
scope — the C1 carve-out and C5 — both require the author to accept a full gate re-run before tagging, which
is currently an open ceremony item.

---

# §E4 — Corrections and unresolved items carried forward

**Corrections to earlier briefings, recorded so they are not re-inherited.**

1. **`evidence/` and `AVAILABILITY_DECLARATION.md` were described as "committed".** At `0ee26c4` both were untracked and had never appeared in any commit (`git log --all` empty for both). The declaration has since been committed locally as `ffa6d94` (not pushed, no tag). Any Phase 1 result citing Phase 0 evidence should name the commit that carries it.
2. **F2 §A.5's claim that a §2.3-only `ties` flip "fails CI by construction" is not true today.** The check is an unimplemented implementation-stage stub. Verified this pass; see E3.3.
3. **The tag message carries five hashes today, six under the pending ceremony.** F3 correctly reports five for `prereg-v30`; the delta's "six" refers to the pending v30a set, which I verified at `CEREMONY_COMMANDS.md:282`. Both are right about different tags. Note `CEREMONY_COMMANDS.md:131` records that working resolution R7 still says five and is superseded by declaration §D.2.

**Unresolved, labelled rather than inferred.**

- Whether `HISTORY.md` is revisable. `README.md:22–23` classifies `PREREG.md`, `DESIGN.md` and the README and says nothing about it, though `PREREG.md:1050` requires it hashed alongside the other two. **Genuinely ambiguous.**
- Whether §6.8's "A CI script" is one script or several. `PREREG.md:649` says "A CI script"; `PREREG.md:1064` says "the CI cost script"; the checker implements most of §6.8's list but carries the cost check only as a stub. **No clause states the intended decomposition.**
- Whether `DESIGN.md:411`'s `leakaudit.protocol` is a layout commitment or a forward sketch. `PREREG.md:1048` pins the current path and `check_structure` enforces it, so **the reducer stays where it is** — but the intent behind the `DESIGN.md` sketch is not resolved.
- The Python floor of 3.11 is derived from `tomllib` being stdlib-since-3.11, not from testing. Only 3.12.10 was tested.
- Whether Phase 0 has formally "recorded the fixture as semantically ambiguous" in the sense of `PREREG.md:449` is an **author determination the repository did not evidence** at `0ee26c4`. Every Phase 1 step is downstream of that determination via §10.0 step 0.
- Whether §0.3's numbered cases are hand-built throwaways distinct from §6.5's case families is **inferred** from the §10.0 ordering and step 1's wording, not stated verbatim.
- Verification item 1 (the mixed frame) is **not assigned** to any of Claims A, B or C. This plan schedules it first on the reading that it is a precondition for all three; the registration does not say which claim it verifies. **Labelled as inference.**
