# A23 — THE THREE MISSING CLAUSES: ESTABLISH, THEN DISPOSE

**READ-ONLY investigation. `PREREG.md` is unchanged at `0c8da19f237cd243…`.** Where a clause is
found load-bearing, the drafted text is **extracted and presented** in
[`A23_PROPOSED_DIFF.md`](A23_PROPOSED_DIFF.md) — **not applied.**

**Per clause, on evidence, not as a batch.** R137 §1.2: *"They differ, and the whole point of this
ruling is per-element evidence."* They do differ, and the three dispositions below are three
different dispositions.

**First, a correction to the line numbers of record.** R137 §0.3 cites declaration lines 822, 994
and 1051. Those are **`phase1`'s** copy, which is one round behind. Re-derived against **`main`'s**
declaration — the Track A authority, 4,358 lines, last written at `8705402` — the citations are at
**l.860, l.1032 and l.1089**. The finding is unchanged: **all three named-clause citations resolve
to nothing, and all 71 distinct `SC-n` citations resolve.**

---

## Clause 1 — Reference AUC anchor (v30 l.445) — **LOAD-BEARING**

**Nothing in `PREREG.md` cites it.** The string `Reference AUC` occurs **exactly once** in the
applied file, at l.574 — its own v30 bullet. No criterion consumes it; §6.2's acceptance criteria 1
and 2 are about ground-truth leaking columns and manifest-clean columns, not AUC. **So the
"something downstream depends on it" test fails.**

**It is load-bearing for the other reason: the registered anchor is UNSATISFIABLE on the acceptance
fixture.** Computed here from the declaration's own recomputed anchor-entry set, against v30 l.445's
`0.957 / 0.675, ±0.010 absolute`:

| horizon | pre-fix | \|Δ − 0.957\| | ok | post-fix | \|Δ − 0.675\| | ok | **both** |
|---|---|---|---|---|---|---|---|
| 5s | 0.966244 | 0.009244 | ✓ | 0.931536 | 0.256536 | ✗ | **no** |
| 10s | 0.939968 | 0.017032 | ✗ | 0.756504 | 0.081504 | ✗ | **no** |
| 30s | 0.856419 | 0.100581 | ✗ | 0.679288 | 0.004288 | ✓ | **no** |

**No horizon satisfies both sides.** Two horizons satisfy one side each; none satisfies the pair.
The registered line says the fixture pair must reproduce `0.957 / 0.675` within `±0.010`, and it
cannot.

**Does SC-2(d) already retire it?** SC-2(d) **is applied**, and it says a reference anchor *"is
recomputed from the fixture's own committed bytes"* and that *"the recomputation is **authoritative
over any figure recorded in a prior report**"*. But **l.445's pair is in the registration, not in a
prior report.** SC-2(d) subordinates prior-report figures to recomputation; on its face it does not
retire a figure the registration itself states. **So the rule is registered and the retirement is
not.**

**DISPOSITION → draft and present.** [`A23_PROPOSED_DIFF.md`](A23_PROPOSED_DIFF.md) carries
`PREREG_v30a_DIFF.md` **H2** verbatim: anchor located at applied **l.574**, match count **1**, four
replacement lines, wording unchanged. **Not applied.**

---

## Clause 2 — Contamination availability class locus (v30 l.450) — **LOAD-BEARING, and it is two registered texts in conflict**

**Nothing in `PREREG.md` cites it either** — `Contamination availability class` occurs exactly once,
at l.579, its own v30 bullet.

**The registered requirement is unmet, and the only route it permits is one another registered
clause forbids.**

1. v30 l.450 requires the class ***"recorded in the manifest."***
2. `evidence/fixture_spike/f3/fixture_manifest_DRAFT.json` — one of the twenty hashed files — has
   **no key mentioning availability or contamination.** Derived: its top-level keys are
   `manifest_status`, `item`, `generated_utc_date`, `classification_basis`, `label_definition`,
   `feature_set_provenance`, `columns`, `not_fed_to_phase7_models`, `counts`,
   `reconciliation_with_45_set_dag`, `author_review`, `review_hash_chain`. **The requirement is
   unmet as registered.**
3. **SC-9(b) IS APPLIED**, and it forbids the fix: *"**EVIDENCE ARTIFACTS ARE NEVER ADJUSTED TOWARD
   A DECISION.** A manifest, a measurement record, a capture, or any artifact whose job is to record
   what was measured **is not edited to carry a declaration, a decision, or an amendment.**"*

**So l.450 requires a manifest edit that SC-9(b) prohibits.** That is two registered texts in
conflict — and **SC-9(b) itself names the remedy in the next sentence**: *"Where a registered
element's recording locus must move, the locus is **amended explicitly**, and the amendment says
what moved and what did not."* The amendment that would do that is the missing clause.

**DISPOSITION → draft and present.** `PREREG_v30a_DIFF.md` **H3** verbatim: anchor at applied
**l.579**, match count **1**, four replacement lines. **Not applied.**

---

## Clause 3 — Sliced CI variant (v30 l.451) — **CANNOT BE DETERMINED FROM THE REPOSITORY**

R137 §1.2 anticipated that §D.2(ii) already covers this element, *"in which case the citation is the
only defect."* **It does not hold as stated, and the reason is worth the detail.**

**What §D.2(ii) does.** The declaration records: *"**(ii) 'Produce or formally defer the CI sliced
variant' (§A.4) — DISCHARGED by amendment.** The element is moved off the Phase 0 acceptance fixture
and re-registered as a Phase 1 CI obligation with its scoring rule declared ex ante. It is not due
at lock; it is due at the first CI run that exercises the padded slicer, and it is frozen by §D.1
item 5."*

**That is exactly what SC-2(e) requires**, and **SC-2(e) is applied**: *"Where the move
re-registers the element as a later-phase obligation, **the obligation names the event that makes it
due, and its scoring rule is declared ex ante, at the move**."* The due event is named. The scoring
rule is declared. It is frozen.

**But §D.2(ii) says "DISCHARGED *by amendment*" — and the amendment is the missing clause.** The
disposition does not stand independently of the thing that is absent; it is a restatement of it.
And SC-2(e)'s own first words are *"MOVING AN ELEMENT BETWEEN PHASES **IS AN AMENDMENT**"*.

**Two readings, and the repository does not settle between them:**

- **(A) The element is dispositioned; the citation is the only defect.** SC-2(e) is the registered
  rule; SC-9(a) says a declaration *"supplies the values, enumerations, and evidence the registered
  clauses call for"*, and SC-2(e) calls for precisely a due event and an ex-ante scoring rule. The
  declaration supplies them. The missing §6.2 clause was a **marker at the site** recording that
  this element is the one being moved.
- **(B) The element is not moved.** SC-2(e) says the move *is* an amendment. No clause of
  `PREREG.md` records that this element moved, so nothing in the registered text effects the move,
  and l.451 stands as a Phase 0 obligation. **SC-9(a) also cuts this way**: *"A DECLARATION SUPPLIES
  DATA UNDER A REGISTERED SCHEMA. **IT CREATES NO GATE OBJECT** … no new criterion, no new
  denominator, no new coverage state"* — and moving when an obligation is due, from lock to a future
  CI run, is arguably creating one.

**DISPOSITION → HALT.** What is missing is not in the repository: a statement of whether SC-2(e)
plus a declaration instance effects a phase move, or whether a §6.2 site clause is required to
effect it. **That is a question about what the amendment means, so §2.6's provisional resolution
does not reach it.** R137 §1.2: *"Do not infer it from the fact that nothing has failed yet"* —
and nothing has failed, because the obligation is not due until a CI run that has not happened.

The drafted text exists (`PREREG_v30a_DIFF.md` **H4**, anchor v30 l.451) and is **not extracted
into the proposal**, because presenting a diff for an element whose disposition is undecided would
be answering the question by drafting.

---

## §D.2(i) — the same shape, recorded for the set

The clause-2 obligation is recorded the same way: *"**(i) 'Add the contamination availability class
as a named field to the governing manifest' (§A.3) — DISCHARGED by amendment, not by doing it.**"*
**Both of the declaration's discharged lock-time obligations are discharged by an amendment that is
absent from `PREREG.md`.** For clause 2 that is resolved by SC-9(b), which forbids the alternative
and names explicit amendment as the remedy. For clause 3 it is not resolved.

---

## Summary

| clause | v30 line | load-bearing? | disposition |
|---|---|---|---|
| Reference AUC anchor | 445 | **yes** — the registered anchor is unsatisfiable on the fixture | **diff presented** (H2) |
| Contamination class locus | 450 | **yes** — l.450 requires what SC-9(b) forbids | **diff presented** (H3) |
| Sliced CI variant | 451 | **undetermined** | **HALT** — two readings, stated above |

**Nothing was applied. `PREREG.md` sha256 `0c8da19f237cd2437b91ef38c570f0ca2159863edcd7f05b10c5cdab9873d3a7`,
unchanged.**
