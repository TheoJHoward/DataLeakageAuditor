# Item F2 — Claims A–C Verification Plan

**Status: PLANNING ARTIFACT ONLY.** No measurement was run to produce this document. No detector code, no availability-model implementation, no `audit()` surface, and no corpus contact occurred. Nothing here is a result.

**Provenance of every quotation below.** Repository `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`, branch `main`, HEAD `0ee26c4`, sole tag `prereg-v30`, working tree clean of tracked modifications (untracked only: `.claude/`, `AVAILABILITY_DECLARATION.md`, `evidence/`, `tagmsg.txt`). Files read: `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `VALIDATED_CONFIG.toml`, `DEVIATIONS.md` (0 bytes). Line numbers are as of this HEAD and are cited as `FILE:line`.

**One correction to the briefing I was given.** The briefing stated there is "a committed copy at `…\MBO_2025(4mon)+2026-01\evidence\fixture_spike\`". `git status --porcelain` at HEAD `0ee26c4` reports `?? evidence/` — the directory exists on disk but is **untracked, not committed**. Any citation of Phase 0 evidence as *registered* material is currently unsupported. Flagged, not fixed (repository is read-only to this item).

---

## Part 0 — The registered text, verbatim

### 0.1 Where the three claims live

`PREREG.md:113`:

> `### 0.3 Three claims this document depends on that have been argued, not verified`

`PREREG.md:115` — the section's own rationale:

> Every version through v9 specified probe mechanics on paper, and three consecutive versions got them wrong. The response is not to keep arguing more carefully. It is to mark the load-bearing mechanical claims as unverified, and make verifying them a gate before the detectors that rest on them are built.

The unverified status is also recorded in the version ledger, `HISTORY.md:191`:

> - **v10** stated the three claims of §0.3 as settled. They are argued.

And the section is invoked as precedent in `PREREG.md:83`:

> §0.3's three claims are the precedent — argued at length by multiple reviewers, two of them wrongly, settled in a morning of measurement.

### 0.2 The three claims, verbatim

**Claim A** — `PREREG.md:117`:

> **Claim A — the tie comparator's default must be `available`.** With bar-close data and bar-open decisions, bar *i−1* closes at exactly the decision instant of row *i*. Under a `ties="unavailable"` default that cell is masked, so the canonical *clean* feature — a trailing window shifted off the decision bar — would be flagged. §2.3 locks the default on that argument. *(Both reviews of v9 proposed the opposite default. If `fixture_corrected` uses shifted features, the opposite default would fail pass-gate criterion 3 and fire kill criterion 2 against a method that works.)*

**Claim B** — `PREREG.md:119`:

> **Claim B — reach is a scanned observation, and no dependency threshold is assumed.** Earlier versions searched for a boundary where the change "dies," which assumed the change's persistence is monotone in the boundary. **For an arbitrary callable it is not** (§8.5), so no single dependency-death threshold exists to find. The locked quantity instead: **full refinement scans the frozen candidate grid and reports the latest boundary at which the selected corruption strategy produced an observable change.** That is an observed perturbation extent, not an exact dependency boundary, and Phase 1 verifies the scan's calibration on known shapes rather than the monotonicity of arbitrary pipelines.

**Claim C** — `PREREG.md:121`:

> **Claim C — permutation strategies are probabilistic at the decisive cell.** A permutation can leave any given cell where it was, so a real leak may go undetected at an individual cohort. Registry entries 14 and 16 rest on this, and it is why §3's dtype-preservation condition is costly rather than free.

### 0.3 What the registration says about verifying them

`PREREG.md:123`:

> **Verification is a Phase 1 gate item** (§10.0), performed before L3.1 and L2a are built, against these cases at minimum:

`PREREG.md:125–132` — the eight enumerated cases (items 1–5 carry Claims A–C; items 6–8 are the §6.10 comparator cases, out of F2's scope but inside the same gate):

> 1. A **mixed frame** — a label column with a declared horizon alongside a joined, forward-filled column whose availability follows its source timestamp. This is where v8 died and is the thinnest part of the specification.
> 2. A cell whose availability equals the decision instant exactly, under both `ties` settings.
> 3. A feature reading exactly one unavailable cell, with the expected reach of one bar.
> 4. A centered window, with the expected reach of about half the window plus one bar.
> 5. A repeated permutation probe on a known leak, to establish that partial cohort counts occur.
> 6. **Per-frame determinism** (§6.10) — a pipeline deterministic on an integer frame and nondeterministic on its promoted complex branch must be caught by the promoted family's own guard, not reported as an exact-mode finding.
> 7. **Mask-dependent compatibility** (§6.10) — a pipeline whose row-dropping depends on which columns are masked must fail compatibility on the probes that trip it and pass on the ones that do not, rather than being decided once per strategy.
> 8. **The per-column alignment comparator of §6.11** against three pipelines: one with integer-typed outputs, one whose outputs propagate complex dtype, and one emitting an internally generated integer column that never touches a promoted input. All three are behaviourally identical after promotion and **all three must pass.** A fourth pipeline that genuinely branches on integer versus float dtype **must fail.**

`PREREG.md:134`:

> Items 6 through 8 are the mechanical facts that §6.2, §6.9, and §6.10 currently assume. Each locked rule names its assumption; if measurement contradicts it, the rule is rewritten through `DEVIATIONS.md` before the detectors that depend on it are built (§10.0).

### 0.4 The pre-authorized rewrite path, verbatim

`PREREG.md:136` — the governing clause for all three claims:

> **If verification contradicts any of these claims, the response depends on §0.2.1's classes, not on convenience.** If the result instantiates a pre-defined class A branch or selects a class B parameter under its locked procedure, record it in `DEVIATIONS.md` and in the frozen configuration. **If it requires a class C change — a new branch, unit, denominator, coverage state, tier licence, or acceptance criterion — record the measurement and commit an amended pre-registration before implementing the affected detector.** §10.0 fixes the order relative to the Phase 1 freezes. *(→ `HISTORY.md` H-04)*

The class table, `PREREG.md:89–93`:

> | Class | What it is | Phase 1 may | Examples |
> |---|---|---|---|
> | **A — mechanical branch facts** | A measurement selects between outcomes this document already defines | resolve, and record the fact | does a frame pass its determinism guard; does a strategy promote on this frame; does a probe preserve shape; does a probe preserve output shape on this mask |
> | **B — parameters under a locked procedure** | A value chosen where the form, search space, objective, denominator, and freeze point are already fixed | select on the development corpus and freeze | the compatibility fraction and its minimum count; cohort count; strategy order |
> | **C — semantic or accounting gaps** | The measurement reveals a needed *new* branch, unit, denominator, coverage state, tier licence, or acceptance criterion | **not resolve under this registration** | anything that changes what a published number means |

`PREREG.md:95`:

> **Class C requires an amended registration**, committed and externally timestamped **before the affected detector is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md` entry standing alone. The deviation records what was measured; the amended tag carries the new semantics. Both.

The citation requirement that makes a class A/B claim admissible at all, `PREREG.md:101–105`:

> **Membership in A or B must be citable, not asserted.** Three conditions, all required:
>
> 1. **The assumption is stated in the locked text at commit time** — the document knew it was assuming the thing, and §0.3 or the rule itself names it.
> 2. **The measurement is scheduled before anything depends on the rule** — Phase 1, before the freezes of §10.0, so no rewrite can flatter a result that does not yet exist.
> 3. **The rewrite path is pre-authorized and cites the specific §0.3 verification item it falsifies.**

`HISTORY.md:26` (H-03) and `HISTORY.md:31` (H-04) record why the permission is this narrow:

> *(v16 said any locked rule contradicted by a Phase 1 measurement could be rewritten through `DEVIATIONS.md`. A deviation makes a change visible; it does not make the revised rule ex ante. …)*

> *(v17 said the affected lock is "rewritten" without limit here and in §10.0 step 3, which is the blanket permission §0.2.1 exists to withdraw — stated in the same document, two sections apart.)*

### 0.5 The locked ordering

`PREREG.md:1004–1014`:

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

---

## Part 1 — The gate that dominates this entire plan

**Nothing in Part 2 may execute yet.**

`PREREG.md:1006` (step 0) makes the class C amendment a precondition for *everything* below it in §10.0 — which includes step 1 (writing the throwaway tests) and step 2 (verifying Claims A–C). Phase 0 did record the fixture as semantically ambiguous: the class C amendment `prereg-v30a` is in preparation and, at HEAD `0ee26c4`, is **not committed** (`DEVIATIONS.md` is 0 bytes; there is no `prereg-v30a` tag; `VALIDATED_CONFIG.toml` is still the §11.1 placeholder).

The amendment's required content is fixed by `PREREG.md:1033`:

> > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**Consequence for scheduling.** The earliest legal start for step 1 is the moment `prereg-v30a` is committed, signed, hashed and OTS-stamped per `PREREG.md:97` ("An amendment inherits §11's integrity chain in full…"). This plan is therefore a *pre-positioned* plan: written now, executed after the amendment ceremony.

**A hazard created by that ordering, and it is the single most important finding in this document.** Step 0 forces `prereg-v30a` to be committed **before** Claim A is verified. `prereg-v30a` carries the replacement acceptance criterion for the fixture. Phase 0 evidence (F4, T2) records the fixture's `ties` branch as `AMBIGUOUS-PENDING-AUTHOR`, and records that the two branches adjudicate the pre-fix side oppositely. If the amendment's replacement criterion is written in terms of a specific tie branch, and Claim A is subsequently refuted, the amendment's criterion moves — which would require a *second* amendment (`prereg-v30b`) to a criterion that `PREREG.md:93` classifies as class C by name ("acceptance criterion").

> **Mitigation to specify inside `prereg-v30a`, before it is tagged:** state the replacement criterion in a form that is *invariant under the tie branch*, or state it explicitly under both branches with the branch named as an open Phase 1 item. Do not let the amendment's threshold depend on an unverified default. This is a drafting instruction for the v30a item, not a Claims A–C action, and it is the one dependency that runs backwards from this plan into work that is already in flight.

**A second hazard, already surfaced by review.** Phase 0's Reviewer B finding B4 recorded that pre-computed both-branch counts make a post-hoc `ties` flip *costless*. That is precisely the property §0.2.1 exists to remove. The countermeasure is procedural and belongs in this plan: **the Claim A decision rule (Part 2, §A.3) must be written down and hashed before any Claim A measurement is run, and the existing both-branch counts from T1/M5 may not be used as the Claim A measurement.** They were produced for a different question, on fixture data, after the fact.

---

## Part 2 — Claim A: the tie comparator's default

### A.1 Exact statement and what it locks

Registered statement: `PREREG.md:117` (quoted in full at §0.2 above).

The lock it supports, `PREREG.md:192–193`:

> | `ties` | cell available to row *i* iff |
> |---|---|
> | `available` **(default)** | `a(j,c) ≤ d(i)` |
> | `unavailable` | `a(j,c) < d(i)` |

`PREREG.md:197`:

> **The default is `available`, on the argument of §0.3 Claim A**, which Phase 1 verifies before the detectors are built. `unavailable` remains selectable for data where the boundary instant is genuinely unusable, and it is never the default.

The default is named in the lock table, `PREREG.md:35`:

> | The tie comparator and its default | §2.3 | mask construction |

`DESIGN.md:78` defers to it and does not restate it:

> The comparator and its default are `PREREG.md` §2.3 and are not restated here; this file specifies where the mask is built and cached. Why `available` is the default is §0.3 Claim A, verified at Phase 1 before the detectors exist.

### A.2 Operational form — what makes it TRUE vs FALSE

Claim A is not a claim about which comparator is *correct in general* — both branches are defined and both remain selectable. It is a claim about which branch is the right **default**, and its argument has exactly two links. Verification must test both links separately, because they can fail independently.

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **A-i (mechanical)** | Under `ties="unavailable"`, a cell whose availability time equals the decision instant is masked; under `ties="available"` it is not. | The comparator of `PREREG.md:192–193`, applied to a boundary cell with `a(j,c) == d(i)`, yields *unmasked* under `available` and *masked* under `unavailable`. | Either branch produces the other result, or the boundary case is ill-defined (e.g. floating-point or timezone equality does not hold where the construction says it should). |
| **A-ii (consequential)** | With bar-close data and bar-open decisions, the canonical *clean* feature — a trailing window shifted off the decision bar — is **not** flagged under `available` and **is** flagged under `unavailable`. | On the constructed clean pipeline, the boundary-instant probe produces no observable change under `available` and an observable change under `unavailable`. | The clean feature is flagged under `available` too (default is not protective — Claim A's premise fails), **or** it is not flagged under `unavailable` either (the argued cost of the opposite default does not exist — Claim A's *justification* fails even if its conclusion is convenient). |

**A-ii is the load-bearing half.** A-i is close to definitional and its main value is catching a construction defect (equality that is not exact). A-ii is what "must be" in the claim's first sentence actually asserts.

A third link is asserted in the parenthetical and is **not verifiable by any Phase 1 construct**: whether the opposite default "would fail pass-gate criterion 3 and fire kill criterion 2 against a method that works" depends on the fixture. See §A.6.

### A.3 The measurement

**What it runs on.** Hand-built synthetic frames only. Two minimal constructions, both authored for this test and discarded afterwards (`PREREG.md:1007`: "Write the throwaway mechanical tests for the §0.3 verification list"):

- **Construct A1 (boundary cell).** A single-entity frame, `n` rows, uniform bar duration `Δ`, `column_roles = at_bar_close` for the feature column, `decision_time = bar open`. Row *i*'s decision instant is `ts[i]`; bar *i−1* closes at `ts[i−1] + Δ == ts[i]`. Exactly one cell sits on the boundary. Timestamps must be integral in the frame's time unit so that `a(j,c) == d(i)` holds exactly and not to within a tolerance — a floating-point near-equality would silently answer a different question. This is `PREREG.md:126` item 2.
- **Construct A2 (canonical clean feature).** The same frame with a pipeline computing a trailing rolling window that is shifted off the decision bar (`.shift(1)`-style), i.e. the feature the claim calls "the canonical *clean* feature". Plus a deliberately *unclean* twin that reads the decision bar, as a positive control: if the unclean twin is silent under both branches the harness is broken, not the claim.

**Procedure.**

1. Materialize `a(j,c)` for both constructs from the `DESIGN.md:61–70` role table (`at_bar_close` → `ts[j] + bar_duration(j)`), including the final-row carry-forward rule (`PREREG.md:208`, `DESIGN.md:70`).
2. For each branch of `ties` ∈ {`available`, `unavailable`}, derive the unavailable set at the chosen decision instant `d` using the comparator of `PREREG.md:192–193` — `≤` versus `<` — and record, per cell, masked/unmasked. **(A-i output.)**
3. For construct A2 under each branch: baseline-run the clean pipeline, run it again with the branch's masked cells corrupted, and compare bitwise (`PREREG.md:653`: "Runtime findings in exact mode are decided by **bitwise equality, not a tolerance**"). Record change / no-change. Repeat for the unclean twin. **(A-ii output.)**
4. Run the identity control of `PREREG.md:686` on both branches — replace masked cells with an exact copy of themselves — and require no delta. Any delta invalidates the run rather than producing a result.

**Decision rule, to be fixed and hashed before step 1 runs.**

- Claim A is **CONFIRMED** iff: A-i holds in both directions, **and** A2-clean is silent under `available` and changes under `unavailable`, **and** A2-unclean changes under both, **and** the identity control is silent.
- Claim A is **REFUTED-PREMISE** iff A2-clean changes under `available`. (The default is not protective.)
- Claim A is **REFUTED-JUSTIFICATION** iff A2-clean is silent under `unavailable` as well. (The stated cost of the opposite default does not exist; the conclusion may still be defensible but the registered argument for it is not.)
- Any other combination is **INCONCLUSIVE — construction defect**, and the construct is fixed and re-run before a verdict is recorded. A construction defect is not a claim result and must not be filed as one.

**Does it need detector code?** No. It needs (i) an availability-time function for two column roles, (ii) a comparison of two timestamps, (iii) a corruption of a cell set, (iv) a bitwise frame comparison. None of that is the `audit()` surface, a detector, or the shipped availability model; it is the throwaway harness `PREREG.md:1007` pre-authorizes as step 1 and it is deleted rather than promoted. **It cannot be reused as the implementation** — doing so would make step 1's throwaway the detector, and the detector must be built after step 4's freeze.

**Corpus contact:** none. Synthetic constructs only.

### A.4 The artifact

Author-created, in the repository so it is citable (this item may not write there):

```
evidence/phase1/claims/claimA/
  claimA_construct.py            # throwaway harness, hashed, retained as evidence
  claimA_capture.txt             # raw stdout of the run, unedited
  claimA_result.json             # the citable record
  claimA_decision_rule.md        # written and hashed BEFORE the run
```

`claimA_result.json` schema:

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

### A.5 Pre-authorized rewrite path if refuted

**What is already permitted.** `PREREG.md:136` (quoted at §0.4) is the whole of it, routed through the class table at `PREREG.md:89–93`. `PREREG.md:1009` (step 3) repeats the ordering: "A class A branch or class B parameter is applied and recorded in `DEVIATIONS.md` and the frozen configuration; **a class C change requires an amended registration committed and timestamped before step 4**".

**Which class is a default flip? AMBIGUOUS — author decision required. I will not resolve it.** The two readings, both defensible from the locked text:

- *Class A reading.* `PREREG.md:91` defines class A as "A measurement selects between outcomes this document already defines". Both `ties` values are defined at `PREREG.md:192–193`; `unavailable` is explicitly retained as selectable at `PREREG.md:197`. Flipping the default therefore selects between two pre-defined outcomes and adds no new branch — and `PREREG.md:93` scopes class C to a "*new* branch, unit, denominator, coverage state, tier licence, or acceptance criterion" (emphasis in original).
- *Class C reading.* The **default** is a distinct object from the branch, and it is locked in the lock table at `PREREG.md:35`, not merely described. Registry entry 13 (`PREREG.md:411`) states the consequence: "**The tie comparator changes findings at the boundary instant.** *(29 Jul 2026)* The same pipeline is clean under one convention and leaking under the other." Every runtime rate is computed over findings; a flip therefore changes what those published numbers mean, which is `PREREG.md:93`'s own catch-all ("anything that changes what a published number means"). Further, resolving it as class A would leave `PREREG.md:192` printing "**(default)**" against `available` while the frozen configuration said otherwise — two copies of one rule, drifted, which is the exact failure `PREREG.md:77`'s single-normative-source rule forbids.

I record both and flag the decision. **What is common to both readings and is not ambiguous:** the measurement is recorded in `DEVIATIONS.md` and the value is serialized into `VALIDATED_CONFIG` either way, because `PREREG.md:635` names it explicitly —

> …**and the complete `AvailabilityModel` of §2.3, including `ties`.**

**What must not change under any refutation:**

- The comparator **table** itself (`PREREG.md:192–193`). Claim A is about which row is default, not about what `≤` and `<` mean. Redefining either inequality is a different and much larger change.
- The requirement that both branches remain selectable (`PREREG.md:197`).
- Consistency across the three places the comparator appears — `PREREG.md:649` requires the CI script to check "that the `ties` comparator is consistent across §2.3, §4.3, and the shipped mask; that §4.3's inequalities match the shipped rule". A flip that touches §2.3 and not §4.3 (`PREREG.md:350–353`) fails CI by construction.
- `panel_mask_scope` remains locked global (`PREREG.md:210`, `PREREG.md:214`); it is a separate field and Claim A does not reach it.
- The conformance suite's obligation to exercise both branches (`PREREG.md:885`: "including deliberately wrong ones, and both `ties` branches").

### A.6 Dependencies, ordering, and two flags

**Must exist before this measurement is possible:**

1. `prereg-v30a` committed and timestamped (`PREREG.md:1006`). Hard block.
2. The `a(j, c)` role mapping for `at_bar_close`, including the final-row carry-forward — available from `DESIGN.md:61–70` and `PREREG.md:208`; no implementation required beyond the throwaway.
3. `claimA_decision_rule.md` written and hashed **before** the run (Part 1's second hazard).
4. Item 1 of `PREREG.md:125` — the mixed-frame case — should run first. It is the availability-matrix precondition ("This is where v8 died and is the thinnest part of the specification"), and A-i/A-ii are meaningless if the matrix is wrong.

**FLAG 1 — Claim A may not be verified on the fixture, and this is a hard prohibition, not a preference.** `PREREG.md:480`:

> **Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

`ties` is a default and is configuration by `PREREG.md:635`. `PREREG.md:435` records that the fixture chooses no defaults ("| **Acceptance fixture** (CME) | Pass/fail gate on the runtime detectors | No | **No** |"). Selecting or confirming the tie default from fixture behaviour is therefore barred twice over. The measurement runs on synthetic constructs; the fixture's *declared* `ties` value is a separate object, belongs to the fixture declaration (v30a), and must not be conflated with the tool's default. This is `PREREG.md:79`'s rule applied to a scheduling question: **one field, one question.**

**FLAG 2 — the claim's registered justification can no longer be re-derived from the fixture.** The parenthetical at `PREREG.md:117` reasons from "If `fixture_corrected` uses shifted features…". Phase 0's M5 result (evidence at `…\scratchpad\fixture_spike\m5\`) records that `fixture_corrected` carries decision-time violations on 7 of 8 instruments in 2025-08 including ZC itself, by a same-second-lattice mechanism unrelated to `ties`. So the consequence the parenthetical describes — criterion 3 failing under the opposite default — is now entangled with an independent channel that already threatens criterion 3. **Claim A must therefore be verified on its own mechanical merits, and the fixture-consequence sentence in `PREREG.md:117` must not be treated as evidence for the claim in either direction.** This is a limitation on what the verification can conclude, not a refutation.

**Invalidation risk to work already done: MODERATE-TO-HIGH.** A refutation does not invalidate any executed measurement, but it directly touches the v30a draft (whose fixture declaration must state a `ties` value, currently `AMBIGUOUS-PENDING-AUTHOR` per Phase 0 F4/T2) and the pending author decision listed first in the Phase 0 findings. See Part 1's mitigation.

---

## Part 3 — Claim B: reach as a scanned observation

### B.1 Exact statement and what it locks

Registered statement: `PREREG.md:119` (quoted in full at §0.2 above).

The rule it supports, `PREREG.md:945`:

> **Reach is a scanned observation, never an inferred dependency.** The refinement in `DESIGN.md` searches for the boundary at which masking stops changing the output. That search assumed the persistence of the change is monotone in the boundary, and **for an arbitrary user callable it is not**: a feature can depend on the masked region, stop depending as the mask shrinks, and depend again — three cells with baseline values (1, 1, 1), a constant corruption to 0, and a feature returning whether the sum lies in {0, 2} changes, does not change, and changes again as the mask narrows. A binary search over that returns the first cancellation and reports it as the answer.

The locked consequences, `PREREG.md:949–953`:

> - **A reach value is reported only from a full scan over the candidate availability boundaries present in the data**, and is described as the latest boundary at which a change was observed — not as the latest cell the feature depends on.
> - **A binary-searched reach is reported as a lower bound and is never labelled exact.**
> - **Above the cap, the capped subset is not scanned at all.** When the complete candidate count exceeds the frozen grid cap of §12, the lower-bound procedure runs instead and `reach_basis = lower_bound` is serialized. …
> - **Whether refinement runs at all is the frozen `reach_refinement_policy`**, not a property of `full` or `quick`. …
> - **The word `exact` refers to the scan, not to the dependency**, and no reach claim asserts exactness of a black-box pipeline's dependency structure.

And the scoping sentence that tells us exactly what Phase 1 is and is not asked to establish, `PREREG.md:955`:

> Phase 1's calibration cases (§0.3 items 3 and 4) establish the formula on simple windows; they do not establish monotonicity for arbitrary callables, and §6.5 now carries a case that breaks it.

The registered expected values appear twice — `PREREG.md:127–128` (items 3 and 4, quoted at §0.3) and `PREREG.md:510`:

> **a reach case per shape** — current-bar inclusion (one bar) and centered window (about half the window plus one bar); **and a non-monotone reach case** built to §8.5's three-cell shape, whose observable change reappears as the mask shrinks, on which a binary search must be shown to return the earlier boundary and the full scan the later one.

`DESIGN.md:192` states the same calibration as a Phase 1 check and `DESIGN.md:188` adds a grid requirement the PREREG text does not:

> **Default is a full scan** over the candidate availability boundaries present in the data — **including a terminal empty-mask boundary**, so that a change still observed at the last real boundary is distinguishable from a scan that simply ran out of candidates, which matters most under `ties="unavailable"`.

`DESIGN.md:190` records why both earlier formulations were wrong, which is the trap this calibration must not fall back into:

> Both earlier formulations were wrong: v9 searched for the largest τ ≤ *d* where the change persists, which is always *d*; the proposed correction searched for the largest persisting τ ≥ *d*, which is one grid step early and returns zero for a feature reading exactly one unavailable cell — current-bar inclusion, the flagship case.

### B.2 Operational form — what makes it TRUE vs FALSE

Claim B decomposes into three separable assertions. Only two of them are Phase 1's job; the third is explicitly out of scope by `PREREG.md:955` and must not be silently attempted.

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **B-i (definability)** | The reported quantity — "the latest boundary at which the selected corruption strategy produced an observable change" — is well-defined without assuming monotonicity. | On a non-monotone construct, the full scan returns the **latest** changed boundary and the binary search returns an **earlier** one, exactly as `PREREG.md:510` requires. | The full scan returns the earlier boundary (the definition is not what the scan computes), or the two procedures cannot be distinguished on the construct. |
| **B-ii (calibration, one bar)** | A feature reading exactly one unavailable cell scans to a reach of one bar. | Full scan returns one bar on the current-bar-inclusion construct, under both `ties` branches, with the terminal empty-mask boundary present in the grid. | Returns zero (the `DESIGN.md:190` failure mode), or any other value, with a correct grid and a passing identity control. |
| **B-iii (calibration, centered)** | A centered window of length *w* scans to about *w*/2 plus one bar. | Full scan returns ⌊*w*/2⌋+1 bars (or the value the pre-committed formula predicts) on the centered construct. | Any other value under a correct grid. |
| **B-iv (out of scope)** | Monotonicity for arbitrary callables. | — | — | Not attempted. `PREREG.md:955` says so explicitly, and attempting it would be scope creep with no gate behind it. |

**The decisive design point: separating an implementation defect from a claim refutation.** The scan procedure lives in `DESIGN.md` and is revisable (`PREREG.md:26`: "`DESIGN.md` holds architecture, method, and API and is revisable"). The *expected values* live in `PREREG.md:127–128` and `PREREG.md:510` and are locked. So a mismatch has two possible causes and the decision rule must distinguish them **before** the run, not after:

- If the scan's own grid is wrong (missing the terminal empty-mask boundary; boundaries derived from row positions rather than timestamps, which `DESIGN.md:127` forbids: "Availability boundaries are timestamp-valued, never row-position-valued"), the mismatch is a **harness defect**. Fix the harness, re-run, no claim result.
- If the grid is verifiably correct and the returned value still differs from the registered expectation, that is a **claim result** — and specifically a refutation of the registered *calibration*, not of the scanned-observation definition.

Confusing these two is how `DESIGN.md:190`'s "one grid step early" error survived a version.

### B.3 The measurement

**What it runs on.** Three hand-built constructs, all synthetic, all discarded:

- **B1 — current-bar inclusion.** A trailing window that includes the decision bar, on a uniform-Δ frame with `at_bar_close` roles. Expected reach: one bar (`PREREG.md:127`).
- **B2 — centered window.** A centered window of a fixed odd length *w* (choose *w* ≥ 7 so that ⌊*w*/2⌋+1 is unambiguous). Expected reach: about *w*/2 plus one bar (`PREREG.md:128`).
- **B3 — non-monotone.** Built to §8.5's stated shape verbatim: "three cells with baseline values (1, 1, 1), a constant corruption to 0, and a feature returning whether the sum lies in {0, 2}" (`PREREG.md:945`; the walk-through is at `DESIGN.md:186`). This construct is fully specified in the registration, which removes any freedom to shape it.

**Procedure.**

1. Build the candidate boundary grid from the distinct availability times present in each construct, **plus the terminal empty-mask boundary** (`DESIGN.md:188`). Assert the grid is timestamp-valued.
2. For each construct, walk the grid exhaustively (the full-scan procedure), recording change/no-change at every boundary. Report the **latest** boundary at which a change was observed.
3. For B3 only, additionally run a binary search over the same grid and record its return.
4. Convert boundary → bars using the construct's known Δ, and compare against the registered expectation.
5. Identity control per `PREREG.md:686` at every boundary; comparison is bitwise (`PREREG.md:653`).
6. Run B1 and B2 under **both** `ties` branches, so the calibration result does not depend on Claim A's outcome. This is the cheapest available insurance against a Claim A flip invalidating Claim B's result.

**Decision rule, fixed and hashed before the run.**

- **CONFIRMED** iff B1 → one bar, B2 → the pre-committed centered value, and B3 → full scan latest / binary search earlier, all under a grid that passes its own assertions and with silent identity controls.
- **REFUTED-CALIBRATION** iff B1 or B2 returns a value other than the registered expectation under a verified-correct grid. Record which, and the returned value.
- **REFUTED-DEFINITION** iff B3's full scan does not return the latest changed boundary. This is the serious one: it means the scanned quantity is not what `PREREG.md:949` says it is.
- **INCONCLUSIVE — harness defect** for any grid-assertion or identity-control failure.

**Does it need detector code?** No, and this is worth stating precisely because reach refinement is scheduled for Phase 2 (`PREREG.md:993`: "L3.1 and L2a exact mode; cohort selection; reach refinement; development tuning"). The Phase 1 measurement uses a **throwaway scan**, not the shipped refinement — it must, because the shipped refinement does not exist and cannot exist before step 4's freeze of "reach definitions" (`PREREG.md:1010`). The throwaway needs: a grid of timestamps, a loop, a corruption, a bitwise compare. It has no policy layer, no cap, no `reach_basis` serialization, no finding object.

**Corpus contact:** none. Note that `PREREG.md:510`'s non-monotone case is a *case family in the evaluation generator*, which is frozen at step 5 — after this measurement. The B3 construct here is a separate hand-built object with the same shape. This distinction is not stated verbatim in the registration; it follows from the §10.0 ordering (the generator is frozen at step 5, the claims are verified at step 2) and from step 1's "throwaway mechanical tests". **Labelled as inference from ordering, not as a quoted rule.**

### B.4 The artifact

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

`claimB_result.json` schema:

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

### B.5 Pre-authorized rewrite path if refuted

`PREREG.md:136` governs, as for all three. The class assignment splits by which link failed:

- **REFUTED-CALIBRATION.** The registered expectations at `PREREG.md:127–128` and `PREREG.md:510` are statements about what a known shape scans to. A corrected value is arguably a class A fact — the document defines the quantity and the measurement fills in its value on a known shape. But `PREREG.md:510`'s expectations are also the acceptance conditions for two evaluation **case families**, and a case family's required behaviour is close to `PREREG.md:93`'s "acceptance criterion". **AMBIGUOUS — author decision required.** I record the split and do not resolve it. The safe route, if the author wants one that is defensible under either reading, is the class C route: `PREREG.md:95` permits an amendment and nothing forbids amending where class A would have sufficed.
- **REFUTED-DEFINITION.** Class C, and I state that with more confidence: `reach` is a published field with a serialized `reach_basis` (`PREREG.md:951`), and a change to what the full scan returns changes what that published field means — `PREREG.md:93`'s catch-all. The amendment must precede step 4's freeze of "reach definitions" (`PREREG.md:1010`).

**What must not change under any refutation:**

- The prohibition on labelling a binary-searched reach as exact (`PREREG.md:950`).
- The above-cap fallback: the capped subset is not scanned and `reach_basis = lower_bound` is serialized (`PREREG.md:951`). The parenthetical there records that the alternative reading "would let a configuration value silently convert a partial observation into a complete one".
- `reach_refinement_policy` remains frozen configuration rather than a property of `full`/`quick` (`PREREG.md:952`).
- The `exact`-refers-to-the-scan sentence (`PREREG.md:953`).
- The suppression rule at `PREREG.md:957`: where refinement did not run, no reach and no fix is printed.
- The cost consequences at `PREREG.md:1064` and the grid cap at `PREREG.md:1068` — a calibration correction does not license reopening the cost model.

### B.6 Dependencies and ordering

1. `prereg-v30a` (Part 1). Hard block.
2. Item 1 of `PREREG.md:125` (mixed frame) — same precondition as Claim A.
3. Claim A **need not** precede Claim B if B1/B2 are run under both branches (recommended). If they are run under one branch only, Claim A must resolve first, or a Claim A flip invalidates the calibration result.
4. Nothing else. Reach refinement's Phase 2 implementation is downstream, not upstream.

**Invalidation risk to work already done: LOW.** No executed Phase 0 measurement depends on Claim B. The exposure is forward-looking only: `PREREG.md:1010` freezes "reach definitions" at step 4, and `PREREG.md:497` freezes the evaluation generator at step 5 "**after Claims A–C are resolved**" — so a late refutation after step 5 would force a snapshot discard under `PREREG.md:1014`.

---

## Part 4 — Claim C: permutation strategies are probabilistic at the decisive cell

### C.1 Exact statement and what it carries

Registered statement: `PREREG.md:121` (quoted in full at §0.2 above).

What rests on it — three places, all locked:

`PREREG.md:412` (registry 14):

> 14. **Permutation strategies are probabilistic at the decisive cell.** *(29 Jul 2026)* Claim C. Multi-cohort and multi-strategy agreement is the mitigation.

`PREREG.md:415` (registry 16):

> 16. **On integer-bearing frames, proofs rest on the probabilistic strategy.** *(30 Jul 2026, scoped 30 Jul)* §3.2. `complex` always promotes, so its standalone findings are REVIEW. On an **all-float** frame `noise` and `nan` both preserve and neither is probabilistic, so proofs there are well supported. On a frame containing integer columns the preserving set can collapse to `shuffle` alone, and `shuffle` can miss the decisive cell. …

`PREREG.md:305` (§3.2's cost paragraph):

> **The cost is real but narrower than v14 claimed** (registry 16). On an all-float frame, `noise` and `nan` are both preserving and neither is probabilistic, so proofs there do not rest on `shuffle` alone. On an integer-bearing frame the preserving set can collapse to `shuffle`, which is probabilistic at the decisive cell (Claim C). …

And the reporting guarantee that translates it for a user, `PREREG.md:941`:

> **A partial cohort count is not weak evidence.** Permutation strategies can leave the decisive cell fixed (Claim C, registry 14), so "found in 18 of 20 cohorts" is the expected shape of a real leak and the report says so.

`DESIGN.md:172` supplies the only quantitative form anywhere, and it is in the revisable file:

> **`shuffle` has a fixed-point failure mode**: a permutation can leave the deciding cell unchanged, so with *m* masked cells the per-cohort miss probability is roughly `1/m`. Partial cohort counts are the expected shape of a true finding.

`DESIGN.md:170` bounds the *other* `shuffle` blind spot, which must not be confused with this one:

> **`shuffle`'s blind spot is narrower than "permutation-invariant."** A trailing window straddling the availability boundary consumes one masked cell plus unmasked history; permuting the masked region swaps that cell's value and the feature moves — so `shuffle` *does* detect current-bar inclusion in a rolling mean. What it cannot move is a statistic over the *entire* masked region, where the permutation acts within exactly the consumed set.

### C.2 Operational form — what makes it TRUE vs FALSE

Claim C is a claim of **weakness**, which inverts the usual burden: confirming it needs one observed miss; refuting it requires establishing a negative, which needs a stated repetition count and a stated bound. The registration supplies neither. See the UNSPECIFIED flag in §C.3.

| Link | Assertion | TRUE iff | FALSE iff |
|---|---|---|---|
| **C-i (existence)** | A permutation can leave the decisive cell where it was, so a real leak may go undetected at an individual cohort. | At least one silent probe is observed on a construct with a known leak, across repeated permutations. | Zero silences across *R* repetitions, with *R* large enough that the pre-committed upper bound on the miss rate excludes the predicted rate. |
| **C-ii (shape)** | Partial cohort counts are the expected shape of a real finding (`PREREG.md:941`). | The observed silence count across cohorts is strictly between zero and all, on a construct whose leak is present at every cohort. | Silence is all-or-nothing across cohorts (which would mean the mechanism is not per-cohort-independent, and `PREREG.md:941`'s reassurance to the user is misdescribed). |
| **C-iii (rate, DESIGN only)** | Per-cohort miss probability ≈ `1/m`. | Observed miss rate is consistent with `1/m` at the pre-committed tolerance. | Materially different. **This is a `DESIGN.md` statement, not a locked one** — a mismatch is a `DESIGN.md` correction, not a claim refutation. Recorded separately so it cannot be smuggled into the claim verdict. |

### C.3 The measurement

**What it runs on.** One hand-built construct, plus one negative control:

- **C1 — single decisive cell.** A frame where the pipeline's output depends on exactly one masked cell, in a way that is *not* symmetric over the masked set — so that a permutation moving that cell's value changes the output and a permutation fixing it does not. Mask size *m* is set explicitly (run at two values, e.g. *m* = 4 and *m* = 20, so the rate has a slope to check against `1/m`). This is `PREREG.md:129` item 5.
- **C2 — negative control for the other blind spot.** A statistic over the *entire* masked region (`DESIGN.md:170`'s "acts within exactly the consumed set"). `shuffle` should be silent on **every** repetition here. Its purpose is to prove the harness can tell the two blind spots apart. Reporting C2's silences as Claim C evidence would repeat the v17 error — `HISTORY.md:198`:

  > v17 built its substitution gate on a capability claim that is false. "`shuffle` cannot move a permutation-invariant statistic" holds only when the permutation acts within exactly the set the statistic consumes. … The error ran in the permissive direction …

**Procedure.**

1. Fix a decisive cell and a mask of size *m*. Enumerate cohorts (`PREREG.md:129` says "repeated permutation probe", so repetition is across seeds, and `PREREG.md:941` reads the result across cohorts — run both axes: *R* independent seeds per cohort, *K* cohorts).
2. For each (cohort, seed): permute the masked cells per column, re-run, compare bitwise. Record change/silence **and** whether the decisive cell was in fact left at its original position — the mechanism, not just the outcome. Recording the fixed-point directly is what makes a zero-silence result interpretable rather than merely negative.
3. Run C2 identically.
4. Identity control per `PREREG.md:686`; bitwise comparison per `PREREG.md:653`.

**Decision rule, fixed and hashed before the run — and the parameters are UNSPECIFIED IN THE REGISTRATION.**

`PREREG.md:129` asks only "to establish that partial cohort counts occur". It fixes no repetition count, no silence threshold, and no tolerance. **This plan proposes them; they are plan-level test-design choices, not registered parameters, and they are not class B** — class B at `PREREG.md:92` is "A value chosen where the form, search space, objective, denominator, and freeze point are already fixed", and none of those are fixed here. They must be written into `claimC_decision_rule.md` and hashed before the run, so the burden of proof cannot be adjusted after seeing the silence count.

- **CONFIRMED** iff at least one silence is observed on C1 **and** that silence coincides with an observed fixed point at the decisive cell **and** C2 is silent throughout **and** the identity control is silent.
- **REFUTED-EXISTENCE** iff zero silences across *R*×*K* trials on C1 with the pre-committed *R* large enough that the one-sided upper bound on the per-trial miss rate falls below the smallest rate that would matter to `PREREG.md:941`'s reporting guarantee. State that rate in the decision rule.
- **DESIGN-MISMATCH (separate axis, never the claim verdict)** if the observed rate is inconsistent with `1/m` at the pre-committed tolerance across the two *m* values.
- **INCONCLUSIVE — harness defect** if C2 ever changes, or the identity control moves, or a recorded silence does not coincide with a fixed point.

**Does it need detector code?** No. It needs a permutation with a seed, a mask, a re-run, and a bitwise compare. It does **not** need strategy escalation, tier resolution, cohort scheduling policy, compatibility accounting, or the `EvidenceEvent` machinery.

**Corpus contact:** none.

**FLAG — this measurement must not be read as selecting `shuffle` scope or `shuffle`'s required/optional status.** `PREREG.md:635` lists "shuffle scope" as frozen configuration; `PREREG.md:92` puts "strategy order" in class B, to be "select[ed] on the development corpus and freeze[d]" — and development-corpus access is blocked by `PREREG.md:1006` until v30a. `DESIGN.md:174` records the current status as provisional: "**Provisional candidate default: `shuffle` (required) then `complex` (optional).** A candidate — the shipped set, order, and required/optional status are chosen on the development corpus and frozen into `VALIDATED_CONFIG`". The Claim C measurement fixes a scope *for the test* and must record which scope it assumed; it does not select the shipped one.

### C.4 The artifact

```
evidence/phase1/claims/claimC/
  claimC_constructs.py           # throwaway, hashed
  claimC_capture.txt
  claimC_trials.csv              # one row per (construct, cohort, seed): fixed_point, changed, m
  claimC_result.json
  claimC_decision_rule.md        # hashed before the run; carries R, K, the bound, the tolerance
```

`claimC_result.json` schema:

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

### C.5 Pre-authorized rewrite path if refuted

`PREREG.md:136` governs. The class assignment depends on direction, and one direction is genuinely awkward:

- **REFUTED-EXISTENCE (`shuffle` never misses).** This would *strengthen* the tool, which is exactly why it needs care rather than less. It would falsify registry entry 14 (`PREREG.md:412`), narrow registry 16 (`PREREG.md:415`), contradict §3.2's cost paragraph (`PREREG.md:305`), and make `PREREG.md:941`'s reporting guarantee — "'found in 18 of 20 cohorts' is the expected shape of a real leak and the report says so" — describe a shape that does not occur. `PREREG.md:941` is inside §8, *Reporting guarantees*: it tells a user what a published cohort count means. Changing it changes what a published number means, which is `PREREG.md:93`'s class C catch-all. **My reading is class C; I flag it as a reading, not a determination**, because the counter-argument (nothing new is introduced; a registry entry is being narrowed, not a branch added) is available. Note also `PREREG.md:397`: "**Additions are dated, whether or not convenient.**" — the registry's stated discipline is about additions and says nothing about removals, so removal has no pre-authorized form.
- **REFUTED-SHAPE (silence is all-or-nothing rather than partial).** Same reasoning, same section, same reading.
- **DESIGN-MISMATCH on the `1/m` rate.** Not a claim refutation. `DESIGN.md` is revisable (`PREREG.md:26`) and `DESIGN.md:172` is a mechanism description, not a measurement formula — but the single-source rule at `PREREG.md:77` and the CI scan at `PREREG.md:645` ("It fails if any measurement formula, state enumeration, or denominator definition appears in `DESIGN.md`") make the boundary worth checking before editing: correct the sentence in place, do not migrate a rate formula into `PREREG.md` as a side effect.

**What must not change under any refutation:**

- The dtype-preservation licence itself (`PREREG.md:302`: "A finding seen **only** in promoted runs is REVIEW `dtype_promoted` per §3.1"). Claim C explains why that licence is *costly*; it is not the licence's justification. Weakening §3.2 because `shuffle` turned out reliable would be a tier-licence change — `PREREG.md:93` names "tier licence" explicitly.
- `PREREG.md:301`'s promotion facts (`shuffle` never promotes; per-run promotion status).
- The distinction between the fixed-point blind spot and the whole-masked-region blind spot (`DESIGN.md:170`). `HISTORY.md:198` is the standing warning about collapsing them.
- The scoring unit and its deduplication (`PREREG.md:244`, §7.2), which is what makes "18 of 20 cohorts" a legible number in the first place.

### C.6 Dependencies and ordering

1. `prereg-v30a` (Part 1). Hard block.
2. `claimC_decision_rule.md` with *R*, *K*, the miss-rate floor and the tolerance — hashed before the run. Without it a null result is uninterpretable and, worse, adjustable.
3. Independent of Claims A and B. The construct does not sit on an availability boundary and does not need a reach scan. It can run in parallel with B once item 1 (mixed frame) has passed.

**Invalidation risk to work already done: LOW.** No Phase 0 measurement rests on Claim C. The forward exposure is that `PREREG.md:305`, `PREREG.md:412`, `PREREG.md:415` and `PREREG.md:941` are all locked text that a refutation touches at once — four sites, one mechanism, which is a lot of surface for a single measurement to move.

---

## Part 5 — Cross-cutting findings

### 5.1 Corpus contact

**None of Claims A, B, or C requires corpus contact.** All three verify on hand-built synthetic constructs. This matters because `PREREG.md:1006` and `PREREG.md:1033` both block development-corpus access until `prereg-v30a` is committed, and `PREREG.md:497` freezes the evaluation generator only at step 5.

Two adjacent things **do** touch protected data and are excluded from this plan:

- Verifying Claim A's fixture parenthetical against `fixture_corrected` — barred by `PREREG.md:480` (defaults may not be altered after observing a fixture result) and by `PREREG.md:435` (the fixture chooses no defaults). See Part 2 FLAG 1.
- Selecting `shuffle` scope, strategy order, or required/optional status — class B, development corpus, blocked. See Part 4's FLAG.

### 5.2 The detector-code boundary

`PREREG.md:1007` pre-authorizes "throwaway mechanical tests for the §0.3 verification list" as Phase 1 step 1. `PREREG.md:1048` establishes that the registration commit carries "no detector implementation" and draws the line explicitly: "protocol tooling is not detector implementation". Three rules follow, and they are mine to propose rather than quoted:

1. The throwaway harness is **deleted or archived as evidence, never promoted** into the implementation. Promotion would place detector code before step 4's freeze.
2. It implements **no** `audit()` surface, no finding object, no tier resolution, no schedule/evidence state, no metric. It computes availability times, masks, corruptions, and bitwise comparisons — nothing that reads or writes the reducers in `protocol/runtime_reference.py`.
3. It is hashed and its hash recorded in each `*_result.json`, so a later reader can tell which code produced which number.

Under the present item's constraints, **none of it is written now.** This document stops at the specification.

### 5.3 Claims whose refutation would invalidate existing work

| Claim | Invalidates executed work? | Detail |
|---|---|---|
| **A** | **Yes, indirectly — MODERATE-TO-HIGH** | Not a measurement, but the in-flight `prereg-v30a` draft: its fixture declaration must state a `ties` value that Phase 0 recorded as `AMBIGUOUS-PENDING-AUTHOR`, and §10.0 step 0 forces that amendment to be tagged *before* Claim A is verified. If the amendment's replacement acceptance criterion depends on a tie branch and Claim A flips, a second amendment follows. Mitigation in Part 1. |
| **B** | No | Nothing executed depends on it. Forward exposure only: `PREREG.md:1010` step 4 freezes reach definitions; `PREREG.md:1014` forces a snapshot discard if step 5 ran early. |
| **C** | No | No Phase 0 measurement rests on it. Four locked text sites move together if it falls. |

### 5.4 Open ambiguities — flagged, not resolved

1. **Amendment class for a `ties` default flip** — class A or class C. Both readings stated at §A.5. Author decision.
2. **Amendment class for a reach-calibration correction** — class A or class C, turning on whether `PREREG.md:510`'s per-shape expectations are acceptance criteria. Stated at §B.5. Author decision.
3. **Amendment class for a Claim C refutation** — I read `PREREG.md:941` as making it class C; the counter-reading is available. Stated at §C.5. Author decision.
4. **Repetition count, bound, and tolerance for Claim C** — UNSPECIFIED IN THE REGISTRATION. `PREREG.md:129` asks only that partial cohort counts "occur". Proposed here as plan-level choices requiring pre-run hashing. Not class B.
5. **Whether §0.3's numbered cases are hand-built throwaways distinct from §6.5's case families** — not stated verbatim anywhere. Inferred from the §10.0 ordering (generator frozen at step 5, claims verified at step 2) and step 1's wording. Labelled as inference.
6. **Whether `evidence/` is registered material** — it is untracked at HEAD `0ee26c4`. Any Phase 1 result citing Phase 0 evidence should say which commit, if any, carries it.
7. **Item 1 of `PREREG.md:125` (the mixed frame) is not assigned to any of Claims A, B, or C.** It reads as a precondition for all of them ("This is where v8 died and is the thinnest part of the specification"), and this plan schedules it first on that reading — but the registration does not say which claim it verifies. Labelled as inference.

---

## Part 6 — Proposed execution order for the first Phase 1 delta

Every step below is **blocked** until the gate at step −1 clears. The ordering inside steps 1–6 is a proposal; the ordering of steps −1, 0, 7 and 8 is locked by `PREREG.md:1006–1014`.

| # | Step | Authority | Blocks |
|---|---|---|---|
| **−1** | `prereg-v30a` committed, signed, hashed, OTS-stamped, repository public. Draft its replacement criterion tie-branch-invariant (Part 1). | `PREREG.md:1006`, `:1033`, `:95`, `:97` | everything |
| **0** | Write and hash `claim{A,B,C}_decision_rule.md`. Record hashes before any construct runs. | Part 1 hazard 2; `PREREG.md:104` | 1–6 |
| **1** | **Item 1 — mixed frame.** Label column with declared horizon + joined forward-filled column following its source timestamp. Verify `a(j,c)` per `DESIGN.md:61–70` and `PREREG.md:220`. Precondition for everything else. | `PREREG.md:125` | 2–6 |
| **2** | **Claim A** — item 2, constructs A1/A2, both branches. | `PREREG.md:126`, `:117` | 7 |
| **3** | **Claim B** — items 3 and 4, constructs B1/B2, both `ties` branches; construct B3 for the non-monotone definition check. May run in parallel with 4. | `PREREG.md:127–128`, `:945`, `:510` | 7 |
| **4** | **Claim C** — item 5, constructs C1/C2. May run in parallel with 3. | `PREREG.md:129` | 7 |
| **5** | Items 6–8 — the §6.10 comparator cases. **Outside F2's scope**, inside the same gate, and `PREREG.md:992` makes "all four alignment-control cases behave as §6.5 requires" a Phase 1 gate condition. | `PREREG.md:130–132`, `:134` | 7 |
| **6** | Assemble `evidence/phase1/claims/CLAIMS_ABC_RESULT.json` — an index over the three per-claim records with verdicts, harness hashes, and decision-rule hashes. | `PREREG.md:1009` | 7 |
| **7** | **Record the result.** Class A/B → `DEVIATIONS.md` + `VALIDATED_CONFIG`. Class C → amended registration committed and timestamped **before** step 8. | `PREREG.md:1009`, `:136`, `:95` | 8 |
| **8** | Freeze the comparator, permitted promotion sets, terminal-decision policy, compatibility-threshold form, and reach definitions. Then and only then: generator snapshot (step 5 of §10.0), conformance suite (step 6). | `PREREG.md:1010–1014` | — |

**Why item 1 goes first.** It is the only case the registration singles out as "the thinnest part of the specification" and the site of a prior death (`PREREG.md:125`). If `a(j,c)` is wrong for a forward-filled exogenous column, every A/B/C result is measuring the wrong matrix, and all three would need re-running. It is also the cheapest of the five.

**Why A precedes B and C but does not gate them.** Running B1/B2 under both `ties` branches (§B.3 step 6) removes B's dependence on A's outcome at negligible cost. C is independent by construction. So A's position is about tidiness and about resolving the pending author decision early, not about correctness — and if A stalls on that decision, B and C can proceed.

**Where the first delta should stop.** At step 6, with three `*_result.json` files and an index. Step 7 is a repository write governed by `PREREG.md:1009` and step 8 is the freeze — neither is a measurement, both are author actions with ceremony attached, and neither belongs in the same delta as the runs that produce their inputs.
