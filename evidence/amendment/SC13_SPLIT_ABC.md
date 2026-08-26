# R31 + P1–P4 — SC-13 SPLIT INTO SC-13a / SC-13b / SC-13c, AND THE N6 DEFECTS CLOSED

**This file supersedes `M1_CANDIDATE_C_CLAUSE_CORRECTED.md` for the clause text**, which in turn
superseded `M1_CANDIDATE_C_CLAUSE.md`. Both prior files are untouched and stand as the superseded
record. Where this file is silent, the corrected file's non-clause material (Part 0 route reasoning,
Part 3.1–3.3 ledger entries as amended below, Part 4's N4 finding, Part 5's two corrections) stands
and is cited rather than reproduced. **On SC-12, `K1_SCHEMA_CLAUSES.md` stands as superseded record;
Part 6 (P3) below is a delta to it, and K1 was not edited.**

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are
untouched. **No git command was run.** The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was
not read. The only file written this pass is this one.

**Read state this pass:** `PREREG.md` = **1,099 lines**; `AVAILABILITY_DECLARATION.md` = **3,684
lines** — both counted by tool this pass and both matching the counts K5, K1, M1, the corrected file
and N6 read under. Every anchor below is a line number read directly this pass. Files read:
`M1_CANDIDATE_C_CLAUSE_CORRECTED.md` (833 lines, in full); the N6 verification record at
`tasks\w52h2p4lb.output` (`result.verifier2`, in full); `PREREG.md` §0.2.1 (72–101), §3.1–§3.2
(300–305), §4 (309–323), §6.2 (455–466), §6.6 (565–576), §7.0–§7.5 (750–844), §10.1–§10.2
(1016–1043), §11 (1046–1055), line 722; `AVAILABILITY_DECLARATION.md` §A.8 (1407–1436), §A.12
(1525–1598); `K1_SCHEMA_CLAUSES.md` (lines 10–18, SC-3 at 210–259, SC-9(e)/(f) at 685–699, SC-12 at
824–879). **Read, not edited.**

**Why the split (R31, restated once).** The corrected SC-13 answered eight questions in one clause,
and three independent reviews each patched one answer and disturbed another. That is `PREREG.md`
§0.2.1's own defect at clause scale — line 79: "**No field answers two questions.** Where a
measurement concept has two independent axes, the specification carries two fields. Compressing them
into one guarantees that the single field misdescribes at least one axis on some case." The split
gives each question one clause: **SC-13a** the criterion, **SC-13b** admissibility, **SC-13c**
interactions.

---

# PART 1 — THE THREE CLAUSES, VERBATIM

Convention follows K1's: **REGISTERS · INSERTION POINT · SUPERSESSION MARKER · THE CLAUSE · DATA THE
DECLARATION MUST SUPPLY · ROWS COVERED.** Application order: **SC-12 (as revised by Part 6), then
SC-13a, then SC-13b, then SC-13c**, in one tag. Anchors are line numbers against the live 1,099-line
`PREREG.md`; if any earlier edit lands first, every anchor must be re-derived.

---

## SC-13a — THE CRITERION

**REGISTERS.** The replacement criterion itself and nothing else: **unit, threshold, denominator**,
and the conditions under which it is evaluated. Discharges the "unit, threshold, and denominator"
core of `PREREG.md` line 1033's obligation. Admissibility is SC-13b's; every interaction with other
registered text is SC-13c's. **The three clauses are one class C amendment and are adopted together;
their one external dependency is stated at SC-13c(c1), not here.**

**INSERTION POINT.** **REPLACES `PREREG.md` line 1030**, the operative sentence of §10.2
criterion 2, preserving the enumeration's `2.` marker and the three-space indentation of the
continuation block. **Lines 1031, 1033 and 1035 stand byte-exact and are NOT superseded** — line
1031 is the branch sentence that authorises the replacement, line 1033 is the obligation being
discharged, line 1035 is the floor the replacement is measured against.

**SUPERSESSION MARKER.** One, conditional rather than absolute — carried from the corrected draft
with the clause names updated:

> **§10.2 criterion 2, line 1030 — v30a, SUPERSEDED ON THE AMBIGUITY BRANCH ONLY. Registered v30
> text, retained verbatim, operative where the branch has NOT fired:**
> "2. **The runtime detectors cannot separate contaminated from corrected fixture under the
> reconstructed declaration** → **stop.**"
> *Not deleted, and not superseded generally. Line 1031 already registers the disposition this
> marker performs — "this criterion is replaced, not deleted" — so where §6.2 line 449's ambiguity
> branch has not fired, the sentence above is the operative criterion and SC-13a–c do not apply.
> Where it has fired and been recorded, SC-13a is the operative criterion for that fixture, with
> SC-13b and SC-13c inseparable from it. Recover the registered line byte-exact with
> `git show prereg-v30:PREREG.md`.*
>
> **NOT SUPERSEDED, stated so the marker's scope cannot be widened by reading:** line 1031 (the
> branch and the before-tuning rule), line 1033 (the three-part obligation and the
> no-`DEVIATIONS.md`-only rule), line 1035 (the floor). **Line 816 is not superseded**: its text
> stands byte-exact; SC-13c(c2) states an express, scoped exception to its suppression clause for
> this criterion's required quantities only, and its publication clause is kept and required.
> **§6.2's four acceptance criteria are not amended by these clauses** (SC-13c(c6)) — SC-13a–c
> *depend on* the amendment this registration makes to §6.2 criterion 3 and do not make it
> (SC-13c(c1)).
>
> **Consequential — §10.1 criterion 3, line 1022.** The Phase 0 kill gate's third condition already
> carries the ambiguity branch on its face ("**or, where the fixture is semantically ambiguous
> (§6.2), under the labelled hypothetical declaration**") and is **not** amended by these clauses:
> §10.1 scores a *third-party tool*, SC-13a scores *this project's* runtime detectors. Named here so
> the two are not conflated during application.

**THE CLAUSE.**

> **2. Where the fixture is semantically ambiguous, the runtime detectors must reach a non-zero
> per-side proof yield on every detector — v30a, operative on the ambiguity branch.**
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

**DATA THE DECLARATION MUST SUPPLY.** None of its own. Every instance datum this clause consumes —
the labelled-unit sets, their per-side partition, the declared sides, the cohort predicate, the
branch record — is supplied under **SC-13b's** DATA block and frozen there.

**ROWS COVERED: none of J1's 76** — stated here once for SC-13a, SC-13b and SC-13c together. The
three clauses jointly discharge `PREREG.md` line 1033, which J1 records as an **obligation**, not as
a row, and they close the drafting consequence K1 records at F-7 as "not closable by any schema
clause". **The 76-row accounting of K1 §2 is unchanged**; its tally (75 covered, row 28 uncoverable)
stands exactly as written.

---

## SC-13b — ADMISSIBILITY

**REGISTERS.** The admissibility test that runs before SC-13a, and **the stated disposition of every
degenerate state**: the empty labelled-unit set, the labelled-unit set empty on one declared side,
and the combination `not_applicable` on every scope-eligible case. After this clause, no degenerate
state reaches SC-13a undisposed and no reader ever meets an undefined quantity or an unstated
outcome.

**INSERTION POINT.** **Pure insertion.** Inserted into §10.2 criterion 2's continuation block
**between line 1035's paragraph and line 1036** (criterion 3), at the block's three-space
indentation, **after** the "waived" definition SC-12 inserts at the same anchor — SC-12 is applied
first, and SC-13b follows SC-12's inserted block. The enumeration is untouched: criterion 3 still
follows the block.

**SUPERSESSION MARKER.** **None — insertion, not supersession.** No registered sentence is replaced
or retired by this clause. The registered lines it relies on — 816, 818, 830, 570 — stand byte-exact
and are cited. The one registered rule whose *effect* this clause's (b3) departs from, line 816's
suppression clause, is handled as an express, scoped exception **stated and recorded at SC-13c(c2)**
and in the v30a amendments block — not by superseding line 816.

**THE CLAUSE.**

> **ADMISSIBILITY FOR THE CRITERION ABOVE — v30a. Tested before any detector runs, and before any
> limb of the criterion.**
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
> published together. Line 818's own principle decides this rather than fighting it — "Suppression
> exists to remove numbers that measure nothing, never to remove one that does" — and at a kill
> criterion this zero measures exactly what the criterion asks: a combination that never applied
> cannot separate the fixture sides, and a gate suppressed on that fact is a detector waived on it
> (§A.12's head: a detector is waived when its result is made "incapable of changing the criterion's
> outcome").
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

**DATA THE DECLARATION MUST SUPPLY.** The labelled-unit set for **each** governed detector,
enumerated by name and frozen before any run, with the ground on which each unit is labelled and the
detector risk kind it is labelled for; **the set's partition by declared side, non-empty in every
(detector × side) cell, per (b2)**; the declared fixture sides; the cohort predicate and its
regeneration procedure; and the record that the ambiguity branch fired. **The declaration does NOT
supply which detectors the floor governs** — SC-13c(c3) pins that.

**ROWS COVERED:** see SC-13a's statement, made once for all three clauses.

---

## SC-13c — INTERACTIONS

**REGISTERS.** Every relationship the criterion has with other registered or amended text, so that
neither SC-13a nor SC-13b carries one: the one-way adoption dependency on the §6.2 criterion-3
amendment; the express, scoped exception to `PREREG.md` line 816; the pinned governed detector set;
the two floor limbs of line 1035 that the criterion's core does not itself discharge; and the scope
and purpose statements.

**INSERTION POINT.** **Pure insertion, immediately after SC-13b's block**, same three-space
indentation, still between line 1035's paragraph and line 1036. The enumeration is untouched.

**SUPERSESSION MARKER.** **None — insertion, not supersession**, with one relationship stated
precisely so it cannot be misread: **(c2) is an express, scoped exception to line 816's suppression
clause — a class C change to how line 816 reads at this one criterion, recorded in the v30a
amendments block — and not a supersession**: line 816's text stands byte-exact and governs unchanged
everywhere outside the quantities this criterion requires.

**THE CLAUSE.**

> **INTERACTIONS OF THE CRITERION ABOVE — v30a.**
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
> entry or a working resolution cannot substitute for the amendment (line 1033; §A.12 item 5).
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
> a detector waived on it — §A.12's head and limb (iii) — and line 1035 forbids the waiver.
> **This is a class C change to how line 816 reads at this one criterion, it is recorded in the v30a
> amendments block in terms, and it reaches nothing else**: everywhere outside this criterion, line
> 816 governs exactly as registered. **The registered conflict between line 816 and line 830 is NOT
> resolved by this clause** — it is recorded in the amendments block as a duplicated-authority
> defect and flagged for a future amendment; no reading of this clause settles it anywhere else.
>
> **(c3) WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the
> detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination
> rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows (line 759), and line
> 1039's "both of L2a/L3.1's combinations". The declaration supplies each governed detector's
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
> ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461 and that
> declaration §A.8 records per working resolution R9. **Its scoring rule and its three dispositions
> are SC-3(b)'s, held by citation and not restated here**; its map is indexed as SC-3(a) declares —
> **per side, per declared violation class, and per declared cell** of the declared scored
> population, which in this fixture's instance form §A.8 states as per-side, per-class,
> per-instrument-month. **It is never the pre-amendment prohibition on any finding on the corrected
> fixture**, and this clause may not be read against that text.
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

**DATA THE DECLARATION MUST SUPPLY.** None. This clause consumes no instance data, and it states the
one thing the declaration must **not** supply: the membership of the governed detector set.

**ROWS COVERED:** see SC-13a's statement, made once for all three clauses.

---

# PART 2 — THE LIMB-BY-LIMB MAPPING TABLE

Every element of the corrected SC-13 (`M1_CANDIDATE_C_CLAUSE_CORRECTED.md`, Part 1) is listed; each
lands in exactly one new location. **Nothing is dropped; nothing lands twice.** Elements marked NEW
have no old-limb source and exist to close P1/P2.

| Old element (corrected SC-13) | Content | New home | Changed beyond renumbering? |
|---|---|---|---|
| REGISTERS block | what the clause registers; F-7 note; the named dependency | split: SC-13a REGISTERS (criterion core), SC-13b REGISTERS (admissibility), SC-13c REGISTERS (dependency + interactions) | yes — dependency sentence moved to SC-13c(c1) |
| INSERTION POINT | replaces line 1030; 1031/1033/1035 stand | SC-13a INSERTION POINT | no |
| SUPERSESSION MARKER (incl. §10.1 consequential note) | conditional supersession of 1030 | SC-13a SUPERSESSION MARKER | yes — adds "line 816 is not superseded" sentence; clause names updated |
| (a) ¶1 — applicability, label, conjunctive-stop rule | when it applies, hypothetical declaration, frozen config, key withheld, (b) tested first | SC-13a opening paragraph | yes — "limb (b) is tested first" becomes "SC-13b's admissibility test is applied first"; (c4)-breach sentence added |
| (a) ¶2 — ADOPTION | drafted against criterion 3 as amended; "one adoption" | SC-13c(c1) | **yes — P4 regression 2 fix: mutual "one adoption" replaced by one-way dependency** |
| (b) main — declared set, empty-set STOP, lift procedure | admissibility core | SC-13b(b1) | yes — governed set now cited from SC-13c(c3); lift extended to (b2)'s per-side case |
| (b) inner block — governed set pinned | lines 759/1039, may-not-shorten | SC-13c(c3) | no in substance; moved, SC-12 alignment sentence added |
| (b) note — why the limb exists; four run conditions | waiver-by-emptiness rationale | SC-13b(b4) | **yes — P4 regression 3 fix: four conditions become three plus one named non-condition** |
| (b) note — "a not-run state is not an empty set" | routing of `not_applicable` states | SC-13b(b3) | **yes — P1 fix: the state is now disposed (zero yield, threshold fail, STOP, published), not merely routed; line 816 named** |
| (c) UNIT | pair, per detector, per side | SC-13a(a1) | cross-ref only ("see limb (e)" → "see (a3)") |
| (d) THRESHOLD + unconditional-per-side sentence | `> 0`, untunable, per detector and side | SC-13a(a2) | yes — cross-ref to (g) becomes SC-13c(c1); defined-quantity sentence added (P2 closure); terminal-execution sentence added (closes §A.12 limb (v) route) |
| (e) DENOMINATOR | registered, unnarrowed, instantiation not restriction | SC-13a(a3) | cross-refs only ("limb (c)" → "(a1)"; "limb (b)" → "SC-13b") |
| (f) EVERY COMBINATION EXECUTED | promoted executed, publishes evidence yield, no threshold | SC-13c(c4) | yes — one sentence added extending (c2)'s exception to its required published yield |
| (g) intro + (g)(i) | floor limbs by citation; §6.2 referent version | SC-13c(c5) + (c5)(i) | **yes — P4 regression 1 fix: restatement replaced by citation of SC-3(b), with SC-3(a)/§A.8's indexing axes restored** |
| (g)(ii) | §10.2 criterion 3's two named gates | SC-13c(c5)(ii) | no |
| (g) closing — why the version is named | anti-ambiguity rationale | SC-13c(c5) closing note | cross-refs only |
| (h) SCOPE, both directions | no acceptance criterion created; routing doctrine | SC-13c(c6) | cross-refs only ("limbs (b) and (d)" → SC-13b / SC-13a(a2)) |
| (i) PURPOSE | broken vs incomplete | SC-13c(c7) | no |
| DATA THE DECLARATION MUST SUPPLY | sets, sides, predicate, branch record; governed-set non-delegation | SC-13b DATA block (instance data) + SC-13c DATA block (the non-delegation) | yes — per-side non-emptiness added per (b2) |
| ROWS COVERED | none of J1's 76; F-7 closure | SC-13a ROWS block, stated once for all three | no |
| — NEW — | `not_applicable`-everywhere disposition (P1) | SC-13b(b3) | new |
| — NEW — | per-side non-emptiness and the 0/0 closure (P2) | SC-13b(b2) | new |
| — NEW — | the express line-816 exception and its recording (P1) | SC-13c(c2) | new — absorbs and supersedes ledger entry 3.4's framing |

**Lands-once check, by destination:** SC-13a holds old (a)¶1, (c), (d), (e) and the
insertion/supersession apparatus — and nothing else. SC-13b holds old (b) main, (b) note 1 (as b4),
(b) note 2 (as b3), plus NEW (b2) — and nothing else. SC-13c holds old (a)¶2, the (b) pinned block,
(f), (g), (h), (i), plus NEW (c2) — and nothing else. No old element appears in two destinations; the
only text appearing in more than one clause is cross-reference by clause name, which is citation, not
content.

---

# PART 3 — P1: THE LINE-816 ROUTE, CLOSED IN SC-13b

**`PREREG.md` line 816, verbatim:**

> **A combination that is `not_applicable` on every scope-eligible case in a body of data publishes
> its counts and suppresses its yields, rates, and gates**, naming the reason.

**What SC-13b now states explicitly** (all three of the brief's required statements, in SC-13b(b3)):

1. **"SC-13a(a2)'s gate is NOT suppressed by `PREREG.md` line 816."** — stated in those words, with
   the exception's authority at SC-13c(c2).
2. A combination `not_applicable` on every scope-eligible case **"is therefore zero — a defined 0/N
   over declared units, not a 0/0"**, which **"fails SC-13a(a2)'s strictly-greater-than-zero
   threshold, and the STOP is tripped and published."**
3. **"The `not_applicable` finding is PUBLISHED, never suppressed: the counts, the named reason, the
   computed zero yield, and the gate outcome are all published together."**

The exception is grounded in line 818's own registered principle rather than against it —
"Suppression exists to remove numbers that measure nothing, never to remove one that does" — because
at a kill criterion the zero measures exactly what the criterion asks. And it is scoped: line 816's
publication clause is kept and required; the suppression clause is excepted **only** for the
quantities this criterion requires; everywhere else in the registration line 816 governs as written.

**Why the previous draft failed here, in one sentence:** its ledger (Part 3.4) claimed limb (b)
resolved the collision, but limb (b)'s own text routed the `not_applicable`-everywhere state away
from itself ("A not-run state is not an empty set") to limb (d), where line 816 — never named in the
clause — would have suppressed the gate; the split puts the disposition in SC-13b(b3) in terms and
the exception's recording in SC-13c(c2), so no reading is left to do the work.

## 3.1 THE RECORDING TEXT FOR THE v30a AMENDMENTS BLOCK — drafted, not applied

The 816/830 conflict itself is **not resolved** here, per the brief. The following is the drafted
recording text:

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
> `not_applicable`-everywhere fact is a detector waived on it (§A.12 head and limb (iii)) and line
> 1035 forbids the waiver. Line 816's text is not edited and its publication clause is kept and
> required.
>
> **What this amendment does NOT do: resolve the conflict.** Everywhere outside SC-13a–c, lines 816
> and 830 both stand as registered and continue to point in opposite directions over the
> `not_applicable`-everywhere state. **Flagged for a future class C amendment** — the defect changes
> what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
> the state a single canonical disposition and make one of the two lines cite the other. Until that
> amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
> conflict (§0.2.1 line 95; §D.3; §A.12 item 5), and this recording supersedes the framing of the
> superseded ledger entry 3.4, which located the collision between line 816 and §A.12 limb (i):
> the operative conflict is registered-text-internal — 816 against 830 — and provisional declaration
> text cannot settle it.

---

# PART 4 — P2: PER-SIDE EMPTINESS, DISPOSED IN SC-13b(b2)

**The undefined case N6 found:** a governed detector's labelled-unit set is non-empty (old limb (b)
satisfied) but **empty on one declared side**; old limb (d) then gated a 0/0 — undefined — and the
clause never disposed it, while the ledger misassigned the question to a limb that did not ask it.

**The disposition chosen and drafted into SC-13b(b2): the empty side trips the same admissibility
STOP as the empty set** — non-emptiness is required in every (governed detector) × (declared side)
cell, and the lift is the same declared-supplement-and-re-freeze route and only that route.

**The justification, in one sentence:** an empty declared side is "nothing declared to score" on a
body of data the criterion gates — the admissibility genus, exactly parallel to (b1)'s empty set —
whereas the alternative (score the empty side as yield 0 and fail) would put a defined value on an
empty denominator, contradicting §7.2.1's registered rule that such a quantity is "**Undefined, not
0% or 100%, at an empty denominator**", and it stays consistent with P1's treatment because
(b3)'s zero is a defined 0/N over declared units while an empty side has no N.

**The closure this buys, stated in both clauses so no reader ever decides it:** SC-13b(b2) ends with
"every per-side denominator SC-13a(a2) reads is non-empty, every yield it gates is defined, and the
undefined 0/0 case cannot arise", and SC-13a(a2) carries the mirror sentence "Every quantity this
limb gates is defined and every gate it states is evaluated." The 0/0 is not left to arithmetic
convention in either direction.

---

# PART 5 — P3: SC-12 ALIGNED TO THE SAME PINNED SET — A DELTA TO K1's SC-12

`K1_SCHEMA_CLAUSES.md` stands as the superseded record on SC-12 and was not edited. The defect N6
carried forward: K1's SC-12 drafting note (K1 lines 837–839) reads "the detector names are not
hard-coded — the floor names 'the runtime detectors' and the declaration supplies which they are",
and its DATA block (K1 line 874) begins "Which detectors the floor governs for this fixture" — the
same delegation SC-13's N5(ii) correction removed from SC-13, so the two clauses treated the same
set differently.

**The three registered sites the revised SC-12 pins to — the SAME clauses SC-13c(c3) cites, quoted
verbatim as read this pass:**

**`PREREG.md` line 759** (§7.1's first runtime metric row):

> | **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; conditional feature-cohort recall; cohort sensitivity; feature-cohort precision; feature discovery recall (secondary); unprobed feature-cohort rate; clean-case finding rate; completion and failure rates |

**`PREREG.md` line 1039** (§10.2 criterion 3's per-combination rule):

> - **Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others.

**`AVAILABILITY_DECLARATION.md` lines 1543–1544** (§A.12, corroboration — declaration text,
provisional until the tag, deliberately cited third):

> **The two runtime detectors the floor governs are L2a and L3.1** (PREREG.md
> lines 318, 320; line 1039 names "both of L2a/L3.1's combinations").

## THE DELTA — three edits to K1's SC-12, everything else unchanged

**DELTA 1 — the drafting note (K1 lines 837–839).** DELETED: "*(… The one change from H7 is that the
detector names are not hard-coded — the floor names "the runtime detectors" and the declaration
supplies which they are.)*" REPLACED WITH:

> *(Generic form; H1's H7 text is compatible and is the drafting basis. The one change from H7 is
> that the governed set is pinned by citation, not hard-coded and not delegated: see the governed-set
> paragraph added to the clause below. SC-12 and SC-13c(c3) pin the same set to the same registered
> sites and never diverge on it.)*

**DELTA 2 — one paragraph added to THE CLAUSE, immediately after the five-limb definition block:**

> **Which detectors the floor governs is not the declaration's to choose.** They are the detector
> rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule
> gates — `PREREG.md` line 759's `Runtime, preserving` row and its `promoted` companion, and line
> 1039's "both of L2a/L3.1's combinations" — the same registered set SC-13c(c3) pins. The
> declaration's §A.12 states the same membership and is corroboration, not the source. The
> declaration may not shorten the set, and a criterion or report written over fewer than all of the
> governed detectors has waived the omitted ones.

**DELTA 3 — the DATA block (K1 lines 874–876).** OLD: "Which detectors the floor governs for this
fixture; and — if and when the branch is resolved — the replacement criterion's unit, threshold, and
denominator, which **this clause does not and cannot supply** (finding F-7)." REPLACED WITH:

> **DATA THE DECLARATION MUST SUPPLY.** Nothing for the governed set — **the declaration does NOT
> supply which detectors the floor governs**; the clause pins it by citation. The replacement
> criterion's unit, threshold, and denominator, which this clause does not and cannot supply
> (finding F-7), are discharged by SC-13a when the ambiguity branch has fired; SC-12 itself
> consumes no instance data.

No other change is made to SC-12: its insertion point (after line 1035, pure insertion, no
supersession), its five-limb definition, and its seven "does not permit" items stand as K1 drafted
them. One wording variance is noted for the author without being resolved here: K1's limb (iii)
reads "satisfied by **another** detector's output alone" where declaration §A.12's reads "satisfied
by **the other** detector's output alone" (line 1553); with the governed set pinned at two members
the two readings coincide, so the delta does not touch it.

---

# PART 6 — P4: N6's FOUR REGRESSION DEFECTS, CLEARED DEFECT BY DEFECT

Each N6 finding is quoted verbatim from `tasks\w52h2p4lb.output`, `result.verifier2.findings`
(TEST 6, regressions 1–4), followed by what changed and the new text.

## REGRESSION 1 — the duplicated normative rule

**N6, verbatim:**

> TEST 6, REGRESSION 1 — **limb (g)(i) restates a rule whose canonical source is another clause of
> the same amendment, and drops that rule's indexing axes while doing it.** New text: "(g)(i) …
> **in its declared-map-matching form, in which findings the declared map predicts are required,
> findings it excludes are false positives, and cells it does not cover are unscored.**" That is
> SC-3(b)'s three dispositions — "A finding the map predicts is REQUIRED … A finding the map
> excludes is a FALSE POSITIVE … A cell the map does not cover is UNSCORED" — restated inside
> §10.2, and it omits the axes both SC-3(a) and §A.8 carry ("per side, per declared violation
> class, per declared cell" / "per-side, per-class, per-instrument-month"). The clause holds itself
> to the opposite standard three limbs earlier: limb (e) refuses to restate the denominator because
> "a second normative statement of it here would leave the registration with two copies of one
> denominator and no canonical source", and the principle is registered at K1 SC-9(f), "**A RULE
> STATED TWICE HAS NO CANONICAL SOURCE.**" M1's limb (g) contained no restatement, so this is
> introduced by the N2 correction.

**What changed:** the restatement is deleted. SC-13c(c5)(i) now holds the referent **by citation**
— it names SC-3 as the canonical locus and §A.8 as the instance record, and it **restores the
indexing axes by naming them as SC-3(a)'s**, stating none of the dispositions' operative text.

**The new text, quoted from SC-13c(c5)(i):**

> **(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
> ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461 and that
> declaration §A.8 records per working resolution R9. **Its scoring rule and its three dispositions
> are SC-3(b)'s, held by citation and not restated here**; its map is indexed as SC-3(a) declares —
> **per side, per declared violation class, and per declared cell** of the declared scored
> population, which in this fixture's instance form §A.8 states as per-side, per-class,
> per-instrument-month.

*(The axis names "per side, per declared violation class, per declared cell" are SC-3(a)'s own
index vocabulary, cited as such — naming a rule's key is citation, not restatement of the rule; the
dispositions themselves appear nowhere in SC-13c.)*

## REGRESSION 2 — the adoption dependency's direction

**N6, verbatim:**

> TEST 6, REGRESSION 2 — the clause text and its ledger disagree about the direction of the
> adoption dependency. Limb (a): "is **adopted with that amendment or not at all** … **The two are
> one adoption.**" Ledger 3.3 item 3: "**The criterion-3 amendment alone remains admissible.** It
> does not depend on SC-13. **The dependency runs one way only**, and this entry does not create a
> reverse one." "One adoption" states a mutual condition; the ledger states a one-way one. The
> ledger's reading is the correct one on the merits (SC-3 stands alone; SC-13 does not), so the
> clause text is the half that is wrong, and it is the half that will be applied. Both sentences
> are new this pass.

**What changed:** the mutual "one adoption" formulation is deleted from the clause text. SC-13c(c1)
states the one-way dependency in the same direction as ledger 3.3 — SC-13a–c are not adoptable
without the criterion-3 amendment; the amendment stands alone — and says in terms that no reverse
dependency is created. (The only "adopted together" language remaining anywhere binds SC-13a, SC-13b
and SC-13c **to each other** — three clauses of one amendment — never the criterion-3 amendment to
them; SC-13a's REGISTERS block says exactly that and routes the external dependency to SC-13c(c1).)

**The new text, quoted from SC-13c(c1):**

> The criterion (SC-13a with SC-13b and this clause) is drafted against **§6.2 criterion 3 as
> amended by this registration** and **is not adoptable without that amendment** … **The dependency
> runs one way.** The criterion-3 amendment does not depend on these clauses and remains admissible
> alone; adopting it without them leaves the registration consistent, adopting them without it does
> not, and no reverse dependency is created here.

## REGRESSION 3 — run condition (ii) against limb (e)

**N6, verbatim:**

> TEST 6, REGRESSION 3 — limb (b)'s reworded condition (ii) now collides with the rewritten limb
> (e). Condition (ii): "the declaration assigns every unit of that detector's character to another
> detector's jurisdiction **within this criterion's own scope**, so no unit of that character is
> scored here" — offered as one of four states that are "a real state of a real fixture rather than
> a defect". Limb (e) forbids the act it describes: "**A declaration may not use the enumeration to
> remove from the denominator a pair the corpus labels and the risk logically applies to** — that
> is a narrowing, it makes the criterion easier to pass, and line 1035 forbids a replacement weaker
> than the floor." If the risk logically applies to the detector, (e) forbids the reassignment; if
> it does not, (ii) collapses into (i) ("the fixture contains no dependency of that detector's
> kind"). Either way (ii) is not an independent condition. In M1 the two did not collide, because
> (ii) was scoped "outside this gate" and (e) was a restriction rather than a prohibition. The net
> effect does not weaken the criterion — both readings end in a STOP or a prohibition — but the
> load-bearing justification for limb (b) is now a list of four in which one member is either
> forbidden or redundant.

**What changed:** condition (ii) is removed from the list. SC-13b(b4) now lists **three** run
conditions — old (i), (iii), (iv), renumbered (i)–(iii) — and names the removed state as a
non-condition, stating N6's own dichotomy as the reason so the removal cannot be read as a silent
narrowing of the list.

**The new text, quoted from SC-13b(b4):**

> Three run conditions produce an empty set or cell, and each is a real state of a real fixture
> rather than a defect: **(i)** the fixture contains no dependency of that detector's kind — on the
> affected side, none that reaches it — so there is nothing for the declaration to enumerate;
> **(ii)** the detector's required declaration is absent or its applicability mode is not selected,
> so it returns a not-run state on every case and the declaration has no model under which to
> enumerate units; **(iii)** every unit that could carry that detector's character is declared
> EXCLUDED or `unscored` on a stated ground, so none survives into the enumeration. …
> **One state the superseded drafts listed as a fourth condition is not one, and is removed.** A
> declaration that assigns every unit of a detector's character to the other detector's
> jurisdiction *within the criterion's own scope* is not an independent run condition: where the
> risk logically applies to the reassigned unit, the reassignment is the narrowing SC-13a(a3)
> forbids in terms; and where it does not, the state just is condition (i). Either way it adds
> nothing to this list, and keeping it would list a prohibited act as a "real state rather than a
> defect".

## REGRESSION 4 — the R24 self-assessment row

**N6, verbatim:**

> TEST 6, REGRESSION 4 — the R24 self-assessment misdescribes the change it is assessing. The
> corrected table's row for (g) reads: "| (g) floor limbs, **version named** | **Yes** | No — names
> criterion 3's amended *form*, not the map's contents | Yes |". But (g)(i) states the criterion's
> three operative dispositions, which are its contents, not merely its form. The row is R24-CLEAN
> on its own question (no fixture particular is named) — it is the characterisation that is wrong,
> and it is the characterisation that would let the restatement pass an audit of this table.

**What changed:** with regression 1's fix, the characterisation the row makes is now actually true
of the text — but the row is rewritten anyway so it describes the citation, not a "form", and the
R24 table is restated for the three new clauses (below). The (g)-successor row now reads:

**The new text — the R24 re-test for the split, replacing the corrected file's §1.1 table:**

| New clause / limb | Source | Names a column, count, instrument, class, or boundary? | Would it make sense on a different fixture? |
|---|---|---|---|
| SC-13a opening | old (a)¶1 | No | Yes |
| SC-13a(a1) unit | old (c) | No | Yes |
| SC-13a(a2) threshold | old (d) + new closure sentences | No — "the side the fixture declares corrected" is a declared side, not a name | Yes |
| SC-13a(a3) denominator | old (e) | No — cites §7.2/§7.4 by section, quotes line 830's own term | Yes |
| SC-13b(b1) declared set | old (b) main | No | Yes |
| SC-13b(b2) per-side | NEW | No — "declared side" is schema vocabulary | Yes |
| SC-13b(b3) `not_applicable`-everywhere | NEW + old (b) note 2 | No — `not_applicable` is §6.6's registered state (line 570), line 816/818/830 cited by number | Yes |
| SC-13b(b4) run conditions | old (b) note 1, minus condition (ii) | No | Yes |
| SC-13c(c1) adoption | old (a)¶2, direction fixed | No — names §6.2 criterion 3, a registered criterion | Yes |
| SC-13c(c2) line-816 exception | NEW (absorbs ledger 3.4) | No — a registered line cited by number | Yes |
| SC-13c(c3) governed set | old (b) pin | No — cites §7.1's runtime rows and line 1039 by section and line; L2a/L3.1 are §4's registered rows (lines 318, 320), registration vocabulary like `preserving` | Yes |
| SC-13c(c4) combinations | old (f) | No | Yes |
| SC-13c(c5) floor limbs | old (g), restatement replaced by citation | **No — cites SC-3(b)'s dispositions and SC-3(a)/§A.8's indexing axes by name; states none of the map's contents and none of the rule's operative text** | Yes |
| SC-13c(c6) scope | old (h) | No | Yes |
| SC-13c(c7) purpose | old (i) | No | Yes |

The two deliberate exceptions declared in the corrected file's §1.1 (registered vocabulary
`preserving`; the governed-set citation naming L2a/L3.1 rows by line) carry forward unchanged — and
the second one's recorded divergence from SC-12 is **closed** by Part 5's delta rather than left
flagged.

---

# PART 7 — THE SEAM STATEMENT

The eight questions the old SC-13 answered, and **the single clause that now answers each**. No
question is answered in two clauses; every cross-clause mention is citation by clause name.

| # | Question the old SC-13 answered | Answered now by, and only by |
|---|---|---|
| 1 | **When does the criterion apply, and under what label is it evaluated?** (old (a)¶1) | **SC-13a** — opening paragraph, with the supersession marker fixing the branch condition |
| 2 | **What must the declaration have supplied for the criterion to be scoreable at all — and what happens when it hasn't, per detector, per side, and in the `not_applicable`-everywhere state?** (old (b), plus the two questions the old clause left open) | **SC-13b** — (b1) the set, (b2) the side, (b3) the `not_applicable` disposition, (b4) why |
| 3 | **What is the unit?** (old (c)) | **SC-13a(a1)** |
| 4 | **What is the threshold, and over what partitions is it applied?** (old (d)) | **SC-13a(a2)** |
| 5 | **What is the denominator?** (old (e)) | **SC-13a(a3)** |
| 6 | **What happens to the combination proof yield does not exist for?** (old (f)) | **SC-13c(c4)** |
| 7 | **Which versions of "criterion 3's gates" are carried in force, and what adoption dependency follows?** (old (a)¶2 + (g)) | **SC-13c** — (c1) the dependency, (c5) the referents and versions |
| 8 | **What does the criterion not reach, what does not reach it, and what is it for?** (old (h) + (i)) | **SC-13c** — (c6) and (c7) |

**And the two questions the old clause failed to answer, now each answered in exactly one place:**
the line-816 route (N6 test 1) is answered by **SC-13b(b3)** operationally, with its authority and
recording in **SC-13c(c2)** — one disposition, one exception, stated once each; the per-side
emptiness (N6's undisposed 0/0) is answered by **SC-13b(b2)** alone. The governed-set question,
which the old clause answered inside limb (b), is now **SC-13c(c3)**'s alone, cited — not restated —
by SC-13b(b1) and by the revised SC-12.

---

# PART 8 — WHAT LEAVES THIS PASS OPEN, CARRIED HONESTLY

1. **The 816/830 conflict is recorded, flagged, and NOT resolved** (Part 3.1), per the brief.
2. **N4's instance-data residue is unchanged**: the labelled-unit set still cannot be constituted
   from the T3/§11 material (corrected file Part 4.3, standing), and under SC-13b as split the
   fixture today trips (b1)'s STOP for the label-availability detector unless the measurement named
   at the end of Part 4.3 closes run condition (i) first. The split changes where that outcome is
   stated, not what it is.
3. **N6's non-regression qualifications stand**: the Part 0.1 direction-of-effect argument
   (relaxation-to-the-floor, admissible) and the line-806 citation defect are properties of the
   superseded file's commentary, not of the clause text drafted here — this file's clauses cite
   lines 759/780/791/1039 for the per-detector partition and never cite line 806.
4. **No tooling was run** against the split clauses (`tools/check_registration.py`,
   `tests/registration/`); anchors are as read this pass (1,099 / 3,684 lines, tool-counted) and
   must be re-derived after any earlier edit. Application order: SC-12 (revised), SC-13a, SC-13b,
   SC-13c, one tag.
5. **Author decisions requested:** adopt the P2 disposition (per-side non-emptiness as an
   admissibility STOP); adopt Part 5's SC-12 delta; approve Part 3.1's amendments-block recording
   text; and decide the fate of the two prior ledger entries this file supersedes in part (3.3's
   "one adoption" phrasing, 3.4's framing of the collision).
