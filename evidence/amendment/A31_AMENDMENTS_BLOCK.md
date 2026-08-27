# A31 — THE v30a AMENDMENTS BLOCK, ASSEMBLED AND PRESENTED. **NOT APPLIED.**

**Nothing here has been applied.** `PREREG.md` is unchanged by this document.
R140 A31: *present for approval; do not apply.*

---

## 1. AUTHORITY — and this is where it stops

`APPROVAL_RECORD.md` §140 records what the author approved on **25 August 2026**, and it is
a closed list of three artifacts:

| artifact | sha256 |
|---|---|
| `PREREG_v30a_APPROVAL.diff` | `c5d89db16f2c1fed…` |
| `SCHEMA_SET_FINAL.md` | `32358f6dfc7f96d2…` |
| `PREREG.md` (base) | blob `75bd93dec436` |

**`BLOCK_MANIFEST.md` l.141 names three components for this block, and they do not come from
one document:**

| component | source | in the 25 Aug approval? |
|---|---|---|
| §8.2, the block proper | `K2_AMENDMENT_LEDGER.md` | **NO** |
| §AB | `SCHEMA_SET_FINAL.md` | **yes** |
| §AC | `SCHEMA_SET_FINAL.md` | **yes** |

**§8.2 — the block proper, the largest of the three — is in `K2_AMENDMENT_LEDGER.md`, which
is not an approved artifact.** §AB and §AC are inside `SCHEMA_SET_FINAL.md` and are approved
content; the block that would carry them is not. **So the block is not already approvable on
the strength of anything in this repository.** It would need a fresh approval, exactly as the
two §6.2 diffs got one at R139 §1.1 — and §2 below is the reason to think hard before giving
it.

---

## 2. §8.2 ITEM 1 IS FALSE OF THE FILE IT WOULD DESCRIBE

Item 1 is the first thing the block asserts:

> **No registered sentence is deleted from this file.**

**Derived from the two files, not from any approval's removal list** — because A24 superseded
two further lines under a second approval, so a population taken from the first would miss them.
Every non-blank line of `prereg-v30:PREREG.md` absent from the applied file, with retention
credited only where a retention marker sits at the site:

| v30 line | what it is | retained? |
|---|---|---|
| 445 | reference AUC | **RETAINED**, applied l.575, marked |
| 450 | contamination class | **RETAINED**, applied l.583, marked |
| 461 | §6.2 criterion 3 | **NOT RETAINED** |
| 855 | §7.7 coverage row | **NOT RETAINED** |
| 929 | `assert_audit_complete()` | **NOT RETAINED** |
| 1022 | §10.1 criterion 3 | **RETAINED**, applied l.1688, marked |
| 1030 | §10.2 criterion 2 | **NOT RETAINED** |

**Seven superseded sentences: three retained with a marker, four not.**
*(R140 §1.2 put it at two and four; that missed v30 l.1022, which A20b established was
retained verbatim with a marker. The figure is three and four.)*

**Landing §8.2 as drafted would put a false claim about the amendment into registered text —
false in exactly the way the block exists to prevent.** The two clauses A24 applied are the
pattern item 1 describes: both retain verbatim, both marked. Four earlier deletions do not.

### The options, laid out. NOT chosen.

1. **Land it with item 1 as approved, and disclose the discrepancy** — the block goes in
   unchanged and a deviation records that item 1 is true of three of seven. A registered
   sentence and a disclosure then disagree, which is the shape §0.2.1 line 77 calls a protocol
   failure.
2. **Retro-retain the four, so item 1 becomes true** — restore each deleted sentence at its site
   in a marked, non-operative block, the way A24 did. This is the option that makes the
   registered text and its description agree, and it is the largest edit.
3. **Do not land the block.** The four citations at ll.1849, 1853, 1915, 1917 then cite a record
   that will never exist and join A30's correction class; the two absences become disclosed
   deviations. R140 A31's own fallback.

---

## 3. WHAT THE BLOCK WOULD RESOLVE, of A31's six

| item | resolved by landing the block? |
|---|---|
| l.1849 cites *"the amendments block records"* | **yes** |
| l.1853 cites *"recorded in the v30a amendments block"* | **yes** |
| l.1915 cites *"amendments block in terms"* | **yes** |
| l.1917 cites *"recorded in the amendments block"* | **yes** |
| absence: no `## v30a amendments` block | **yes** — this is the block |
| absence: no `**Amendment status:**` line | **no** — that is §8.1, a separate insert at line 6 |

**Five of six.** §8.1's status line is a different hunk and is not assembled here.

---

## 4. THE ASSEMBLED BLOCK — presentation only

Extracted verbatim: §8.2 from `K2_AMENDMENT_LEDGER.md` between its own `K2-BLOCK-BEGIN` and
`K2-BLOCK-END` markers; §AB from `SCHEMA_SET_FINAL.md` ll.1632–1679; §AC from ll.1687–1737 — the ranges
`BLOCK_MANIFEST.md`'s §A table gives. Nothing below is authored here.

```markdown
## v30a amendments (class C under §0.2.1)

**What this block is.** `prereg-v30a` is an **amended registration, not a restart** (§0.2.1, line 95). It carries the class C changes enumerated below — every registered surface this amendment touches, by section and v30 line, with the clause responsible — and no others. Two passes produced them, and each row names its source. The first is the element-by-element conformance walk of the acceptance fixture's reconstructed availability declaration against §6.2 (`AVAILABILITY_DECLARATION.md` §A), which superseded registered text at instance-bearing lines. The second is the schema pass over that walk's findings, which registered in this file the kind of object each gate input is, what a declaration must supply for it, and what the gate does with it — under §0.2.1's single-normative-source rule. The declaration is the reconstructed declaration §6.2 already requires and the carrier of this fixture's evidence. **It is not a normative annex and may not be cited as one.** Measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule). What lives there is this fixture's *instances*: its identity, its measured ground-truth map, its reference-anchor values, its evidence, its documented-unverifiable assumptions, and the per-unit enumerations these rules yield for it.

**The test applied to every sentence below, so the split is checkable rather than asserted:** *would this still be true for a different fixture?* If yes it is a **rule** and it is here. If no it is an **instance** and it is in the declaration.

**How the amendment is written, so nothing is lost.**

1. **Where registered text is superseded, the v30 text is retained inline, verbatim, at its own site, in a block marked `SUPERSEDED BY v30a` and marked NOT operative.** No registered sentence is deleted from this file. Where a registered sentence stands byte-exact and only its reading, its count, or its assumed scope is changed, a marker at its site states exactly what is superseded and what stands.
2. **Each amended or extended clause carries an inline marker naming v30a**, and the new normative text sits beside the old. New clauses carry the tag `[SC-n]` in their heading; a citation "SC-n" anywhere in this file means the clause whose heading carries that tag, and "SC-n(x)" its lettered limb.
3. **The registered text is recoverable byte-exact independently of this file: `git show prereg-v30:PREREG.md`.** The retained inline copies are a reading convenience; the signed `prereg-v30` tag is the record. Every line number in this block and in every v30a marker is a line number of that registered text.
4. **This amendment inherits §11's integrity chain in full** (§0.2.1, line 97): signed tag; the SHA-256, as committed, of every registered document and registration tool, enumerated in the tag message (§11 item 8); external timestamp receipt committed; repository publicly reachable at lock.

**The enumeration — one row per registered surface touched.** *Superseded*: the registered text at that line is replaced by operative v30a text and retained verbatim beside it. *Marker*: the registered text stands byte-exact and a v30a marker at its site states what reading is superseded or extended. *Inserted*: new text at a site where no registered sentence is replaced. *Pointer*: a cross-reference that adds no rule of its own. Class is §0.2.1 line 93's.

**(a) Registered text superseded — each retained verbatim at its site, NOT operative:**

| Registered surface (v30 line) | Touch | Operative v30a text · clause | Class | Justification |
|---|---|---|---|---|
| §6.2 line 445 — reference AUC anchor | superseded | operative clause at its site; schema SC-2(d) | C | declaration §A.1 |
| §6.2 line 450 — contamination availability class | superseded | operative clause at its site; schema SC-2, SC-9(b) | C | declaration §A.3 |
| §6.2 line 451 — sliced variant for CI | superseded | operative clause at its site; schema SC-2(e), SC-3(f) | C | declaration §A.4 |
| §6.2 line 461 — acceptance criterion 3 | superseded | SC-3 | C | declaration §A.8; working resolution R9 |
| §7.7 line 855 — detector-case coverage row | superseded: the row is re-registered with `unscored` | SC-6 | C — line 93's "coverage state" | schema pass over the walk of the reconstructed declaration against §6.2 |
| §10.2 line 1030 — kill/pause criterion 2 | superseded on the ambiguity branch only; operative where the branch has not fired | SC-13a, with SC-13b and SC-13c | C | line 1033's obligation, unmet by the §6.2 acceptance amendment alone |
| §10 line 992 — Phase 1 gate cell | superseded, consequential to lines 445 and 451 | operative row at its site | C (consequential) | derived from §A.1 and §A.4; not walk-cited |
| §10.1 line 1022 — kill-gate criterion 3 | superseded, consequential to line 461 | operative item at its site | C (consequential) | derived from §A.8; not walk-cited |
| §8.3 line 929 — `assert_audit_complete()` failure set | superseded: `waived` joins `unsupported` and `could_not_run` | operative bullet at its site; carried with SC-12(w) | C — line 93's "coverage state" | schema pass; the prohibition SC-12(w) registers |

**(b) Registered text standing byte-exact, its reading extended or partly superseded by a marker at its site:**

| Registered surface (v30 line) | What the marker states | Clause | Class |
|---|---|---|---|
| §0.2.1 line 97 — "both file hashes" | superseded as a count, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8 |
| §2.3 line 205 — `column_roles` | added, not superseded: a role is a position, not an availability instant | SC-1(c) | carried with SC-1 |
| §2.4 lines 220–222 — the label-availability formula | partially superseded: the unstated assumption that the horizon term's unit is a duration | SC-1(d) | C — line 93's "unit" |
| §6.1 line 431 — the five-bodies heading and table | amended in form: the implication that the enumeration is exhaustive | SC-10 | carried with SC-10 |
| §6.2 line 459 — criterion 1 | added, not superseded: the inference that the denominator is a construction-taxonomy count | SC-4 | carried with SC-4 |
| §6.2 line 480 — ordering, locked | extended: what the ordering ranges over, and what happens when a frozen object is found wrong | SC-8 | carried with SC-8 |
| §7.2.1 line 816 — the `not_applicable`-everywhere suppression | an express, scoped exception for one criterion's required quantities; the sentence governs as registered everywhere else | SC-13c(c2) | C — how line 816 reads at one criterion |
| §8.2 line 915 — not-run states | extended: `unscored` is governed by this section's closing sentence, by reference to §7.7's row | SC-6 | carried with SC-6 |
| §11 item 3 (line 1050) — the hashed files | superseded as a file set, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8 |
| §11 items 1–7 | extended by item 8 | SC-8 | carried with SC-8 |

**(c) New clauses inserted — no registered sentence replaced at the site:**

| Site (after v30 line) | Clause | Registers | Class | Justification |
|---|---|---|---|---|
| §0.2.1, after line 99 | SC-9 | integrity of a declared instance: what a declaration may not create, evidence never adjusted, obligations discharged only by being met or amended, working-resolution authority and supersession order, the stronger-reading interpretation rule, one normative copy | C | the same schema pass, registering the integrity limbs and the stronger-reading interpretation rule as one clause |
| §2, after line 266 (new §2.9) | SC-1 | the declaration as the gate's semantic authority: measured not intended, the representation named, roles are positions, units declared, staleness is not unavailability, one comparator branch scored | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.1, after line 441 | SC-10 | declared non-gated data, diagnostic classes, and the forbidden uses of non-gate data | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 451 | SC-2 | the acceptance fixture's composition, what may move, the pre/post licence, reference anchors by recomputation, moves between phases | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 464 | SC-4 | the criterion-1 denominator and the three-class partition rule: registered predicates, precedence, edge readings, exclusion grounds, publication discipline | C | declaration §A.6, §A.6.0–§A.6.4, §A.10; working resolution R11 |
| §6.2, after line 464, following SC-4 | SC-5 | adjudication routing: one criterion per finding, attribution to the ground, the false-positive class, detector jurisdiction, declared sentinels | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 468 | SC-7 | the gate's input surface and the one-side-at-a-time sequencing rule | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 480 | SC-8 | the freeze: what freezes, in what form, checkable before any run, no number corrected in place, the integrity chain | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §7.7, after the table (line 856) | SC-6 | `unscored`: a coverage state with its semantics, entry condition, two levels, and gate consequences | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §7.8, after line 892 | SC-11 | the all-zero control over every empty aggregate and every pass claim | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §10.2, after line 1035 | SC-12 | "waived", defined; which detectors the floor governs; what the definition does not permit; and **SC-12(w)** — the entry condition for §7.7's `waived` coverage state: a prohibition with a closed and empty list of licensed grounds, the rule that the state records a waiver and never makes one, and the report's duty to publish the count | C | declaration §A.12; schema pass |
| §10.2, after line 1035, following SC-12 | SC-13b | admissibility for the ambiguity-branch criterion, and the disposition of every degenerate state | C | one amendment with SC-13a |
| §10.2, after line 1035, following SC-13b | SC-13c | that criterion's interactions: the one-way dependency on amended criterion 3, the line-816 exception, the pinned governed set, the floor limbs carried by citation | C | one amendment with SC-13a |
| §11, after item 7 (line 1054) | item 8 | the freeze indexed from §11, and the hash set read from the tag message's own enumeration | C, carried with SC-8 | the open-form discipline for the hash-count enumeration (`HISTORY.md` H-L13) |

**(d) Pointers — cross-references that add no rule of their own:** §7.2.1 after line 816 (to the exception SC-13c(c2) states); §7.7 after the table (`waived` is defined in §10.2; **SC-12(w)** is its entry condition); §8.2 after line 915 (`unscored` under this section's closing sentence, by reference to §7.7's row); §8.6 after line 961 (a zero, an empty result, or an all-clean statement is a published number; SC-11 governs what it must survive and name).

**What this enumeration is, and what is read from it.** The registered lines this amendment supersedes are those in (a) and no others; the registered lines whose reading it extends are those in (b) and no others; the clauses it inserts are those in (c) and no others; the pointers are those in (d) and no others. **Their number is read from the enumeration and is stated nowhere as a numeral** — so that a further clause added under §0.2.1 adds a row here and changes no count anywhere in this file. Every change enumerated in (a), (b) and (c) is class C under §0.2.1 line 93 — each changes what a published number means, what an acceptance or kill criterion requires, or what the gate may consume, or is carried with the clause that does — and each is carried by this registration under line 95. None is a `DEVIATIONS.md` entry standing alone.

**What an amendment may not do, restated here because this is the first one.** It may not be weaker than the thing it amends (line 97). It may not convert an unmet element into a satisfied one by re-reading it. Where an element cannot be met as written at the instant the amendment must be committed, it is **amended explicitly, never waived and never left outstanding** — which is what the sliced-variant row of (a) does.

*(Supersedes the split file's Part 3.1 text. Four changes, all in the ledger: the waiver authority
re-cited to SC-12 with §A.12 as corroboration; the working-resolution/deviation prohibition re-cited
to SC-9(c)/(e) and SC-12 item (5) with §D.3/§A.12 as corroboration; one paragraph added recording
that the exception departs from line 818's applied holding on the amendment's own authority; and —
this pass, S3(1) — the dangling reference to a drafting-file ledger entry struck from the closing
paragraph, which now states the registered-text-internal character of the conflict in its own
terms.)*

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

> between two registered lines.

---

## §AC — THE v30a DISCLOSURES BLOCK (drafted R58/W4)

Appended to the §AB amendments-block recording text and claimed by the same hunk. Disclosures 1–6 were established at R47/P9 and recorded only in the round state until now; **the block itself did not exist**, and the line-459 marker already referred to “disclosure 7”. Both are closed here.

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
```
