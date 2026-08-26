# T4 — SIDE-EFFECT CHECK: §8.2 CLOSING SENTENCE OPEN-FORM, REACHING `waived`

> **⚠ SUPERSEDED IN PART — DELTA R35/B3 and R37/D8.** This is a verification record written **before**
> SC-12(w) existed. Its finding about `§8.2`'s closing sentence stands. Its repeated conclusion that
> **F-6 remains open** — that `waived` has no registered entry condition and that closing it is "not
> part of the v30a schema set" — **is no longer true.** SC-12(w) registers that entry condition and it
> is in v30a. Read the statements below about `waived`'s entry condition as the state of the world on
> the date of this check, not as current.

**Item T4. VERIFICATION, NOT AN EDIT.** No file was touched. The check below reads the pre- and post-amendment texts side by side, identifies what actually changes for `waived`, and states the finding — rather than assuming that nothing changes.

**Scope of the disclosed side effect.** S2(i) (drafted in `SCHEMA_SET_FINAL.md` Part 1, INSERTION TEXT for SC-6 at `PREREG.md` §8.2 after line 915) makes §8.2's closing sentence range **not over §8.2's own enumeration alone**, but **by reference to §7.7's row**, over every detector-case coverage state that row carries other than `passed` and `failed`. That row includes `waived`. The consequence: §8.2's closing sentence, which pre-amendment covered only §8.2's own listed states, post-amendment reaches `waived` as well.

---

## 1. THE TWO TEXTS, VERBATIM

### 1.1 `PREREG.md` §8.2 as-tagged (v30, byte-identical to `prereg-v30`, working-tree copy sha256 `f0a8f001…c7cc6`, line 915 closing sentence)

> ### 8.2 Not-run states
>
> Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. **None may be displayed in a way mistakable for a pass.**

The **closing sentence** is: *"None may be displayed in a way mistakable for a pass."* Its scope is fixed by the enumeration two sentences earlier: `not_applicable`, `unsupported`, `could_not_run(reason)`. It does **not** reach `waived` under the v30 reading.

### 1.2 SC-6 S2(i) insertion (drafted, not applied), what will land after `PREREG.md` line 915

> **`unscored` — §7.7 (v30a) [SC-6] — is governed by this section's closing sentence as well.** It is neither a pass nor a not-run: this section's boundary sentence does not reach it, and its entry condition and semantics are SC-6's, not restated here. It is named here so that this section and §7.7's row cannot name different states — **the closing sentence above ranges, by reference to §7.7's row and not to the enumeration in this section alone, over every detector-case coverage state that row carries other than `passed` and `failed`.**

The bolded final phrase is the disclosed side effect: the closing sentence's scope is now "every §7.7 detector-case coverage state other than `passed`/`failed`" — a set that includes `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived`, and (post-amendment) `unscored`.

### 1.3 The set the closing sentence covers, pre and post

| State | Governed by §8.2 closing sentence pre-amendment (v30) | Governed post-amendment (v30a via S2(i)) |
|---|---|---|
| `passed` | no | no (explicitly excluded) |
| `failed` | no | no (explicitly excluded) |
| `not_applicable` | **yes** (listed) | yes |
| `unsupported` | **yes** (listed) | yes |
| `could_not_run(reason)` | **yes** (listed) | yes |
| `waived` | **no** (not in §8.2 enumeration) | **YES — via §7.7's row** ← the disclosed side effect |
| `unscored` | n/a (does not exist yet) | **yes** (the intended addition of S2(i) / SC-6) |

---

## 2. WHAT THE SIDE EFFECT ACTUALLY DOES TO `waived`, LIMB BY LIMB

Applying the check to each of the four things a coverage-state clause could touch (definition; entry; gate consequence; display):

### 2.1 Definition of `waived` — **UNCHANGED**

`waived` is defined at `AVAILABILITY_DECLARATION.md` §A.12 (declaration lines 1546–1556), which SC-12 re-registers into `PREREG.md`. §A.12 / SC-12 lists five limbs — exclusion from denominator, optional contribution, satisfiable by the other detector alone, threshold met without executing, or reported under §7.7's `waived` state.

S2(i) touches none of those limbs. It touches only §8.2's closing sentence and its scope. The definition is unchanged.

**Cross-check.** No text in SC-6's INSERTION TEXT — the block that lands at §8.2 after line 915 — mentions `waived` at all. `waived` is reached by the scope-widening of the closing sentence, not by any clause about `waived` itself. §A.12's / SC-12's five limbs are not re-stated, extended, or narrowed by S2(i).

### 2.2 Entry condition for `waived` — **UNCHANGED (still absent, per F-6)**

`waived` was registered in v30 §7.7 **without an entry condition** (F-6, K1 drafting record). This is a known defect. The intended entry-condition addition of S2(i) / SC-6(b) is for `unscored`, not for `waived` — F-6's own text: *"§7.7's `waived` still has none after this amendment."*

S2(i) does **not** add an entry condition for `waived`. Reaching `waived` under §8.2's closing sentence is a **display constraint**, not an entry-condition addition — the display constraint applies to whatever conditions elsewhere in the registration cause a detector to be reported `waived` (which, under v30a, remain unenumerated). The F-6 defect is unresolved; T4's check does not close it.

**This is the clearest of the four limbs, and stating it is the point of T4:** the intended addition (SC-6(b), entry condition for `unscored`) does not apply to `waived`. The side effect does not accidentally add one either — it adds a display rule, which is a different object.

### 2.3 Gate consequence of `waived` — **UNCHANGED**

`waived`'s gate consequence lives in three places, none of which S2(i) touches:

- **`AVAILABILITY_DECLARATION.md` §A.12 limb 6 (declaration lines 1587–1589):** "**Per-combination waiving is still waiving.** Line 1039 applies gates per combination; dropping a detector from one combination's criterion while scoring it in another waives it for that combination, and is class C." Unchanged.
- **SC-12** (v30a re-registration of the waived definition in `PREREG.md`, with the governed-set paragraph and the item-(1)–(5) enumeration): pins which detectors the §10.2 floor governs. Unchanged.
- **SC-13c(c2)** (v30a, at `PREREG.md` §7.2.1 after line 816): the express exception to the not-applicable-everywhere suppression for one criterion's required quantities. Unchanged.

S2(i) is a §8.2 insertion. It does not enter §7.2.1, §7.7, §10.2, or §A.12 / SC-12. **Gate arithmetic is untouched.**

### 2.4 Display of `waived` — **NEW CONSTRAINT, IN-KIND**

**The one change that lands.** After S2(i), a `waived` entry may not be displayed in a way mistakable for a pass. Pre-amendment, this display rule was not registered for `waived` (it was registered only for the three states §8.2 enumerated).

Is this an IN-KIND extension or an OUT-OF-KIND change?
- **In-kind.** A `waived` detector, by §A.12's definition, produced no result capable of changing the criterion's outcome. Displaying such a detector as "passed" would be substantively wrong (it did not pass; it did not run to a terminal decision under that criterion's arithmetic). The display constraint aligns with the definition's intent — it forecloses a report-authoring failure mode that was already substantively forbidden by §A.12's limb (i)–(v) but was not explicitly display-regulated.

**Consequence for any current or future report authoring.** A report that would have printed `waived` as clean, covered, or passing is now explicitly non-conforming. In practice, this catches only report bugs; a well-formed report was not previously permitted to display `waived` as a pass under §A.12's definition of the state.

**No corresponding change is required in `AVAILABILITY_DECLARATION.md` §A.12 / SC-12** — the display rule extension is properly an §8.2 clause, and SC-12 was drafted knowing this extension was arriving (SCHEMA_SET_FINAL Part 1, SC-6 apparatus paragraph, cites SC-12 and F-6 as the drafting record).

---

## 3. THE FINDING, STATED FOR THE RECORD

**Finding.** S2(i)'s disclosed side effect — making §8.2's closing sentence open-form and thereby reaching `waived` — adds **one** new obligation to `waived` and only one: a **display constraint** ("none may be displayed in a way mistakable for a pass"). That obligation is **in-kind** with `waived`'s existing definition (§A.12 / SC-12), and **does not**:

- change `waived`'s definition (§A.12 limbs (i)–(v)) → **unchanged**;
- add or remove an entry condition for `waived` (F-6's known defect remains, not resolved by this amendment) → **unchanged**;
- change `waived`'s gate consequence (per-combination waiving under §A.12 limb 6; SC-12's governed-set pin; SC-13c(c2)'s §7.2.1 exception) → **unchanged**.

The one change is the display constraint, which is **not an entry-condition addition** and therefore is not "the intended entry-condition addition" R27 T4 names. R27 T4 is discharged by stating this fact rather than by asserting no change: there IS a change to `waived`, but it is exactly the display-constraint reach of the closing sentence, and nothing else about `waived` moves.

---

## 4. THE F-6 KNOWN DEFECT — STATED, NOT FIXED

`waived` remains without a registered entry condition after S2(i) lands. F-6 is the drafting-record acknowledgement of this defect. Its resolution requires a separate clause (a `waived` entry condition, drafted analogously to SC-6(b) for `unscored`) which is **not part of the v30a schema set**. T4's check confirms that the current amendment does not accidentally close F-6 by side effect; F-6 remains open and must be tracked as an item for a future amendment cycle.

*(Recommendation for `HISTORY.md` — non-normative, at author's discretion: consider adding a review-lesson at the H-L series head recording that the display extension caught a display-authoring gap for `waived` without fixing the deeper entry-condition gap, and that the two are different objects. This is a bookkeeping note, not part of T4's discharge.)*

---

## 5. WHAT T4 CANNOT DO

T4 verifies the amendment text as drafted. It does **not**:
- verify that no other v30a amendment (SC-1 through SC-14) accidentally intersects `waived`'s definition, entry, or gate consequence — that is a separate cross-cutting check;
- verify that report-authoring code (`tools/check_registration.py`, `protocol/runtime_reference.py`) actually implements the display rule for `waived`; a checker extension may be required at the X3 verification pass;
- close F-6.

---

*T4 complete. Side effect is the addition of one display constraint on `waived`, in-kind with `waived`'s existing definition; nothing else moves. F-6 remains open. No file mutated this pass.*
