## 1. THE COMPOSED-GATE ANSWER

**YES at the registration level. NO in this instance. That gap is the whole signature decision.**

The two E3 readers do not disagree on this. They found the same hole by different routes and both are right: **every quantity §6.2 adjudicates resolves to an object the declaration authors, and no registered clause puts a floor under any of them.** I verified the route end to end against the composed text and it is not defeated at any step.

**The route, with the clause that fails to stop each step:**

1. **Draw the scored population.** SC-3(c): *"The declaration declares the scored population — the rows and units the criteria adjudicate."* SC-4(j) forbids identifying it by cardinality: *"identified by the named constant the declaration declares, never by its cardinality."* Nothing ties it to the fixture's content.
2. **N is whatever the map says.** SC-4(b): *"the map declares a violation on it, on the scored side, under the declared branch"* … *"**N is the length of the REQUIRED list**, and no other quantity is N."*
3. **The one independent anchor is affirmatively barred.** SC-4(a): *"**No classification of the scored set other than this derivation enters any criterion, denominator, or count**."* The manifest's ground-truth DAG and its count of independently leaking sources — the only dated measurement of what leaks — may not enter.
4. **The exit beats the entry and its ground list is open.** SC-4(c): *"Where a unit satisfies more than one class predicate, **UNSCORED wins.**"* SC-4(e): *"A unit is excluded only on a ground the declaration states. Two grounds are registered here **because** each is otherwise a guaranteed failure of criterion 1…"* — a reason for two, not a bar on a third. These drafters close enumerations in terms when they mean to (SC-12(w1): *"the enumeration is **closed**, and it has **no members**"*; SC-4(b): *"There is no fourth class and no residue class"*). SC-4(e) has no such sentence.
5. **With N = 0 all four criteria are vacuous.** Criterion 1 (*"**Every** ground-truth leaking source column…"*) is satisfied over the empty set; criterion 2 has no declared-clean units; criterion 3's findings land on cells the map does not cover, and SC-6(d) neutralises them — *"they carry **no criterion consequence in either direction**"*; criterion 4 is silent.
6. **The assertion battery cannot see it.** All three §8.3 assertions are negative and each disclaims the axis that would catch absence: two *"Ignore coverage"*, one *"Ignores findings."* No assertion in the registration fails on absence.
7. **The fix cannot be imported.** SC-13b(b1) is the exact missing test — *"If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is STOP."* I grepped the whole schema set: **every occurrence of "non-empty" is inside SC-13a/SC-13b/SC-13c.** SC-12 item (2) bars the citation — *"It does not reach any other criterion and may not be cited to soften §6.2's"* — and so does SC-13c(c6): *"It creates no acceptance criterion, amends none, and is never cited against one."* SC-9(a) bars the declaration from supplying it: *"The criteria of §6.2 as amended are the whole gate."*

**Why the instance is nonetheless not a cheap pass — and why that does not rescue the registration.** I read the live declaration. The gate partition is REQUIRED **11**, OUT OF JURISDICTION **22**, UNSCORED **2**, over 35 fed columns. The 2 unscored carry named, checkable grounds (`buy_volume_10s` identically zero; `book_imbalance_ratio` lag unresolved, gate status EXCLUDED). The 22 OOJ carry a *gate-failing* false-positive consequence, so the declaration has built itself a harder exam than the registration requires. And §A.6.5 does the reconciliation the registration omits — a second, independently built partition (`y1\column_universe.csv`, by source file) cross-tabbed column by column against the gate partition, *"identical, 35 = 35."*

**None of that is compelled by a registered clause.** §A.6.5 states of itself: *"it derives nothing, changes no class, and **is not a gate object**."* The declaration anchored its denominator voluntarily. The registration you are about to sign does not require the next declaration — or a revision of this one — to do so.

**One instance fact sharpens this into the reason to hold the signature.** The manifest records `independently_leaking_sources: 25`; N is 11. Fourteen columns the manifest classifies as independently leaking are not in the criterion-1 denominator, and most sit in the 22 OOJ class where **a finding on them fails the gate**. SC-4(a) is right that "built" and "declared violating" are different questions — but the composed text turns that correct distinction into a rule with no reconciliation obligation, and the direction of the unreconciled difference is: *a detector that flags a column the fixture's own manifest calls an independently leaking source is charged a false positive.* That is defensible under the declared `ties: available` branch. It is not something a registration should permit to happen silently, and §A.6.5 cross-tabs source-file against gate class — **not manifest class against gate class**. The 25-to-11 difference is disclosed as two numbers and is nowhere resolved unit by unit.

---

## 2. FINDINGS THAT SHOULD STOP A SIGNATURE

### S1. No floor under the criterion-1 denominator, and no anchor to any object the declaration does not author

**What.** Nothing registered requires the REQUIRED list to be non-empty, bounds the UNSCORED list, or reconciles either against the manifest DAG. SC-4(a) forbids the reconciliation.

**Quoted.** SC-4(a): *"**No classification of the scored set other than this derivation enters any criterion, denominator, or count**, and no split within such a classification carries gate arithmetic."* SC-4(b): *"**N is the length of the REQUIRED list**, and no other quantity is N."* Against SC-13b(b1): *"If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is **STOP**."*

**Why it matters.** This is the amendment's own missing test, written for the other branch and withheld from the one gate that runs. And **the other branch does not fire for this fixture** — §A.5 records *"The original work DID document prediction timing… The fixture is therefore **not** semantically ambiguous."* So SC-13a/b/c, the best-built clauses in the set, are inoperative here, and §6.2 is the only gate operating. The registration's entire non-emptiness discipline sits on a branch that is switched off.

**Smallest fix.** One limb, SC-4(k), modelled on SC-13b(b1): the REQUIRED list is non-empty on every declared side, tested before any detector runs, on pain of STOP; and the REQUIRED list is published alongside a per-unit reconciliation against the manifest's leaking-source list, every difference named with the registered predicate that produced it. This requires an express carve-out in SC-4(a) — *"a reconciliation published under (k) is a disclosure, not a classification entering a criterion, denominator, or count"* — because as composed SC-4(a) forbids the very check that would close the hole.

### S2. SC-4(e)'s exclusion-ground enumeration is not closed, and SC-4(c) makes the unclosed class win

**What.** UNSCORED's predicate is satisfied by the act of declaring — *"scoring on it is declared impossible, **on a ground the declaration states**"* — and SC-4(c) gives it precedence over the substantive REQUIRED predicate.

**Quoted.** SC-4(c): *"Where a unit satisfies more than one class predicate, **UNSCORED wins.**"* SC-4(e): *"A unit is excluded **only on a ground the declaration states**."*

**Why it matters.** The more clearly the map declares a violation on a unit, the more SC-4(c) rewards finding it unscoreable. SC-3(h)'s *"The unscored disposition is not an escape hatch"* is a conclusion with no operative content — no test, no adjudicator, no consequence. SC-4(e)'s guard runs the wrong way: *"**Reinstating** an excluded unit changes the denominator and is class C"* prices re-entry, not exit.

**Smallest fix.** Append SC-12(w1)'s own sentence to SC-4(e): *"The enumeration of grounds is closed; a ground not registered here is not a ground, and adding one is a class C amendment."*

### S3. The registered ±0.010 acceptance interval is retired and its replacement has no registered floor

**What.** `PREREG.md` line 445 fixes *"acceptance interval **±0.010 absolute**"* as a literal inside the tagged registration. SC-2's marker retires it (H1 hunk H2) and SC-2(d) substitutes *"The **declared** tolerance applies per entry and **may not be widened**."*

**Why it matters.** "May not be widened" constrains movement from whatever the declaration first declares. I grepped the schema set: **the string `0.010` does not appear anywhere in it.** A gate threshold has moved from registered text to declared data, and §10 line 992's Phase 1 gate cell reads on it. SC-2(d)'s genuinely stricter limb — *"a deviation **approaching** the tolerance is a stop-and-report"* — scales with the declared value and has no registered threshold for "approaching."

**Smallest fix.** SC-2(d) states the floor: *"The declared tolerance is not wider than the registered ±0.010 absolute per entry."* **Verify before signing whether H2 already carries this — it is not in `SCHEMA_SET_FINAL.md` and is therefore NOT ESTABLISHED from the sources read.** If H2 does carry it, S3 dissolves; if not, it blocks.

### S4. The design-time tuning channel against the scoring key is open

**What.** SC-7 closes the runtime channel cleanly and is the best-drafted clause in the set. Both its scoping phrases are about the *run*: *"**AT GATE TIME** a detector receives exactly two things"*, *"at any point **in a gate run**."* No clause forbids fitting the frozen default configuration to the map at design time.

**Quoted.** Line 480: *"tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. **Defaults may not be altered after observing a fixture result.**"* The prohibition attaches to observing a **result**, not to reading the **key**. And SC-8(f) hashes *"the declaration itself, which carries the scoring key"* into the tag message — line 480's own locked ordering places that tag **after** the run.

**Why it matters.** SC-7(c) states the stake exactly: *"A run that received the key has not produced a gate result, whatever it reports."* A configuration fitted to the map at design time receives nothing forbidden at gate time and satisfies SC-7 on its face, while the gate measures retrieval. The map is a Phase 0 object; runtime tuning is Phase 1. The key is in the author's hands throughout.

**Smallest fix.** One sentence in SC-7 or SC-8, in SC-8(d)'s existing pattern: *"The frozen default configuration is justified without reference to the declared map, and the map is not an input to configuration selection."*

### S5. Criterion 2 has three different scopes across three texts, and criterion 2 is declared byte-exact

**What.** Line 460 (unamended): *"No **manifest-clean** source column receives any runtime finding of any tier…"* SC-5(c): *"that criterion's scope is **the units the declaration declares clean**, and those units **do** route to it."* SC-4(a): no manifest classification *"enters any criterion."* SC-5's own marker says *"§6.2 criteria 1, 2 and 4 stand byte-exact."*

**Why it matters.** This is the duplicated-authority failure §0.2.1 line 77 registers, on the one criterion that can only ever *fail* a detector, whose drafting note says *"A classifier the tool controls cannot be allowed to decide what counts against it."* Re-scoping it from a manifest fact to a declaration fact by describing it, in a clause whose marker denies amending it, is the shape the registration exists to forbid. The instance resolves it benignly — §A.7 reads the scope as the manifest's 4 clean columns and §C.3 records that the declaration-clean set is those same 4 — but nothing registered requires the two to coincide, and SC-3(g)'s *"A side the declaration characterizes is **CHARACTERIZED, never clean**"* pushes the declared-clean set toward empty.

**Smallest fix.** One sentence in SC-5(c): *"Criterion 2's scope is line 460's manifest-clean set; SC-4(a) does not reach it, because line 460's population term is a scope, not a classification of the scored set carrying gate arithmetic."* Or amend line 460 explicitly and drop the byte-exact claim.

### S6. A miss has no stated gate consequence at cell level

**What.** SC-3(b) attaches "fails the gate" to false positives and never to misses: *"**A finding the map predicts is REQUIRED.** Its absence is a miss."* (no consequence) versus *"**A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier, primary or secondary."*

**Why it matters.** SC-6(c) makes the levels independent — *"A cell-level `unscored` never makes its unit `unscored`"* — so misses are caught only at unit level by criterion 1, and only to the depth of "at least one." A detector firing once per REQUIRED unit and missing every other predicted cell satisfies criterion 1 in full while amended criterion 3 records the misses with no quoted consequence. Given the instance's map is per `(side, instrument, month, class)` over 48 instrument-months, "at least one" is a very shallow requirement.

**Smallest fix.** One clause in SC-3(b): state whether a miss on a REQUIRED cell fails criterion 3, or state expressly that misses are adjudicated at unit level by criterion 1 alone and that this is the intended depth.

### S7. The declaration carries a drifted second normative copy of SC-9(e), and the tag is about to freeze it

**What.** `AVAILABILITY_DECLARATION.md` §D.3 (line 3590) restates SC-9(e) verbatim but for one word — *"exempts a **column**"* against SC-9(e)'s *"exempts a **unit**"* — and presents it as its own rule (*"Stated as a rule so that the next entry cannot do the opposite by precedent"*), citing SC-9(e) nowhere. §AB then cites the copy as authority: *"corroborated by the declaration's §D.3."*

**Why it matters.** SC-9(f) makes this a registered failure in terms: *"**A RULE STATED TWICE HAS NO CANONICAL SOURCE.** … A second normative copy in a declaration is the duplicated-authority failure, not a redundancy."* SC-10(e) repeats it. The drift is on `unit`/`column` — the exact object SC-4 spends nine limbs partitioning. And SC-8(f) hashes the declaration into the tag, so signing freezes the drift into the integrity chain. SC-12 licenses the opposite (*"Where the fixture's declaration states the same membership, it is **corroboration, not the source**"*), so the registration would hold both readings.

**Smallest fix.** Delete §D.3's blockquote and cite SC-9(e). Same treatment for §E, which restates SC-7(a), (c) and (d) near-verbatim and has already dropped a word of scope (SC-7(b) withholds *"any summary, cohort list, **restriction**, or per-cell count"*; §E withholds *"any summary, cohort list, or per-cell count"*). Cost: two deletions and two citations. This is the cheapest item on the blocking list and the only one that gets worse by waiting.

---

## 3. FINDINGS WORTH FIXING BUT NOT BLOCKING

**The separation test.** SC-13a states two independent per-side thresholds (*"the `preserving` combination's proof yield must be **strictly greater than zero**"*) and never compares one side to the other, which is registered line 1030's entire subject (*"cannot **separate** contaminated from corrected"*). Not blocking **only because the ambiguity branch does not fire for this fixture** (§A.5), so line 1030 stands operative and SC-13a–c are inoperative. It becomes blocking the moment the branch fires. Fix when convenient: add a between-side limb to SC-13a(a2).

**SC-9(d)'s retroactive record completion.** *"A working resolution binds by its content and its date, **not by where it was recorded** … and the record is completed to contain it."* Every ex-ante rule in the registration depends on dates being evidenced rather than asserted. Bounded in practice by SC-9(e)'s stronger-reading-only rule and the append-only ledger, so not blocking; add a contemporaneity requirement (an external timestamp, or a statement that a completed entry is marked as completed and dated at completion).

**The cell key's granularity is unconstrained.** SC-3(a) requires only that a key *exist, be declared and named*; SC-13c(c5)(i) makes the discretion express (*"this clause names no key"*). Coarsening helps in both directions. The instance declares `(side, instrument, month, class)`, which is fine. Fix: extend SC-8(d)'s justification discipline to the key.

**SC-5(e) jurisdictional routing reaches §6.2, by SC-13c(c6)'s own words** — *"A jurisdictional routing statement written about the acceptance gate reaches the acceptance gate and stops there."* It is in live use (the label-base character of `tick_direction`, `vwap_distance`, `weighted_mid` assigned to L2a). This is a genuine detector-boundary question, declared ex ante, and the instance's use is substantively argued. Fix: put the assignment under SC-8(d)'s justification discipline.

**SC-6(a)'s unqualified "enters no denominator."** Placed at the §7.7 detector-case table, it collides on its face with line 875's *"a case enters a combination's metric denominators when its `schedule_state` ∈ {`completed`, `incomplete`}."* Not blocking: line 875 defines membership **positively on a different axis**, and line 820 walls §7.7 off from every runtime metric. Fix: scope SC-6(a) to the map-cell and declared-unit levels SC-6(c) names.

**SC-11(e)'s expectations are the declaration's to supply, and its disjunction licenses revising the declaration.** *"the zero is a finding about the aggregation **or about the declaration** — and never a pass … adjudicated **before any gate outcome is written**."* Declare no non-zero expectation and the limb never fires; declare one and an inconvenient zero is resolvable by revising the key, timed to sit inside the ex-ante window. Fix: require expectations to be complete over the declared aggregates, and route a declaration-side resolution through SC-8(e).

**SC-11(b)'s check does not test what SC-11(c) tells the reader it tests.** Schema-resolution plus source-non-emptiness passes for a well-formed filter predicate matching nothing — the commonest silent zero. SC-11(c) then instructs the reader that the named check separates a proved zero from an unproved one. Fix: make the second-route reconciliation unconditional, or narrow SC-11(c)'s claim.

**SC-12(w7) pre-states its own measurement.** *"The gate report publishes the count of `waived` detector-case entries … **That count is zero.**"* The §8.3 assertion is the real guard and does independent work; (w7)'s last sentence tells the report writer the answer. Fix: delete the sentence.

**§8.3 has no positive limb.** All three assertions are negative and each disclaims one axis, so the battery cannot distinguish a working tool from a silent one. This is inherited from registered v30, not created by v30a — adding `waived` to the failure set is a tightening. Worth naming in the amendments block so it is not later read as an oversight.

**§6.1 line 441 and §7.0 constitution rule 7 forbid publishing rates from the fixture; SC-13c(c4) requires a published yield from it.** *"**No accuracy or generalization rate is published from the fixture**"* / *"the fixture, conformance suite, and wild corpus **publish no rates**."* No marker in the set names either line. Inert while the ambiguity branch does not fire; it needs a marker before the branch could ever fire, because rule 7 is a locked constitution rule.

---

## 4. WHERE THE READERS DISAGREED — AND WHICH READING THE COMPOSED TEXT SUPPORTS

**(a) Does criterion 2 have any population at all?** Report 1: none — SC-4(b) has no CLEAN class and *"There is no fourth class and no residue class,"* so a clean column is OOJ (routed away by SC-5(c)) or UNSCORED (neutralised by SC-6(d)). Report 2: two candidate scopes, NOT ESTABLISHED which.

**Report 2 is right; Report 1 over-reads.** SC-4(b)'s partition is *"MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE **DECLARED SCORED SET**"* — it partitions the units the gate's *arithmetic* runs over. Criterion 2's population is a scope term in unamended line 460, and SC-5(c) says in terms that clean units *"**do** route to it."* The instance confirms a live population (4 manifest-clean columns, §A.7). The defect is S5's — three texts naming three scopes — not the absence of a population.

**(b) Does the freeze instant permit composing the key after the run?** Report 3 (E2-1.07): yes, SC-8(a) sets the freeze at the tag and line 480 puts the tag after the gate run. Report 4: SC-8 is stricter throughout.

**Report 4's reading governs.** SC-8(a) states what becomes *immutable* at the tag, not the earliest moment an object may be composed. Three limbs say pre-run in terms — SC-3(h) *"declared and frozen before any detector runs"*, SC-6(b) *"frozen before any detector runs"*, SC-8(c) *"**EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS**"* — and SC-9(e) resolves any residual ambiguity toward the stronger reading. Report 3's reading is available on SC-8(a) alone and worth one clarifying clause, but it is not the better reading and it does not block.

**(c) Does "NOT PART OF THE GATE" let non-numeric gate-determinative material escape the freeze?** Report 3 (E2-1.05): yes, because SC-10(b)'s condition covers only *"its **figures**"* and *"an acceptance **denominator**."* Report 4: closed.

**Report 4 is right.** SC-8(a) backstops it: *"an object the gate consumes and the enumeration omits is a **defect in the enumeration**, not an object outside the freeze."* A declared exclusion ground is an object the gate consumes. Worth a cross-reference in SC-10(a); not a hole.

**(d) Is SC-13b(b1)'s STOP real or discharged by writing?** Report 2: the tightest construction in the document. Report 3 (E2-1.08): discharged by an act of enumeration.

**Both are right and neither is load-bearing here.** (b1) is a genuine admissibility test whose satisfaction condition is a declared, frozen enumeration — which is the same declarer-control problem as S1, one level down. Moot for this signature: the branch does not fire.

**(e) The residual disagreement worth naming.** Report 1 treats SC-9(e) as an available cure for several gaps. It is not. SC-9(e) governs *interpretation of locked text* — it resolves ambiguity toward the stronger reading. **It cannot supply a floor no text states.** The absence of a non-emptiness requirement is a gap, not an ambiguity, and SC-9(a) forecloses the declaration filling it: *"The criteria of §6.2 as amended are the whole gate."* S1 through S6 are amendments or nothing.

---

## 5. WHAT WAS CHECKED AND FOUND SOUND — do not re-check

- **SC-7 as a runtime input surface.** *"**AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME** … **Nothing else.**"* plus SC-7(c)'s stake and SC-7(d)'s *"A single run given more than one side satisfies none of the criteria, however its outputs are partitioned afterwards."* The runtime channel is closed. Only the design-time channel (S4) is open.
- **SC-8(a)–(f) as a freeze.** Lists not counts, ex-ante checkability, the declaration itself hashed, no in-place correction, an enumeration whose gaps are defects rather than exemptions. Strong at what it does — it locks the declarer's choices against revision. It is simply the wrong instrument for S1, which is about what those choices may be.
- **`waived` is fully priced.** SC-12(w1) *"**NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.**"*, the floor as a prohibition with no invocation procedure, the governed set `{L2a, L3.1}` pinned to §7.1 lines 759/760 and matching line 1035's *"neither runtime detector waived"* exactly, and `waived` added to `assert_audit_complete()`'s failure set so the prohibition is machine-checkable. SC-12(w6) states the design correctly: *"A prohibition no assertion tests is not enforced."*
- **SC-13a(a3) and SC-13b(b1)–(b4).** Every trivial-satisfaction route on the ambiguity branch is closed by name — empty denominator, narrowing, narrowing by enumeration, line-816 suppression, `not_applicable`-everywhere, 0/0, reporting `waived`, shortening the governed set, scoring one detector, dropping a combination. This is the best-constructed machinery in the document. It is also inoperative for this fixture.
- **SC-11 as a discipline on zeros.** Every empty aggregate proved empty before it may be reported; mismatch raises rather than warns; an unexpected zero is a finding and never a pass. Sound in shape; the two narrow gaps are in §3.
- **SC-3(a), (c)–(g); SC-4(f), (h)–(j); SC-5(a), (b), (d), (f); SC-9(a)–(c), (e), (f); SC-2(a)–(c), (e).** Stricter than what they amend or pure additions. SC-5(b)'s *"Naming the right unit on the wrong ground satisfies nothing"* and SC-4(f)(1)'s *"A count that cannot be written out as a list is a count nobody can audit"* are doing real work.
- **SC-3's marker on §10.1 line 1022.** The kill gate keeps *"is silent on `fixture_corrected`"* — the stricter reading, applied to a third-party tool. Correctly left unamended, and SC-13a's marker correctly refuses to conflate §10.1 (scores a rival) with SC-13a (scores this project).
- **Instance arithmetic.** REQUIRED 11 + OUT OF JURISDICTION 22 + UNSCORED 2 = 35 fed columns; partition check printed; the two unscored grounds are independently checkable (`trades_buy` strict-viol 0 in all 96 cells; `book_imbalance_ratio` EXCLUDED with a stated construction gap); the Y1 source-file partition and the gate partition compose column by column, 35 = 35, built from different artifacts. The declaration's own workmanship is not the problem.
- **The ambiguity branch does not fire** (§A.5, against `PREREG.md` line 449). Registered §10.2 criterion 2 line 1030 is operative; SC-13a/b/c are not. Anything ranked on the assumption that the floor protects this fixture should be re-ranked.

**NOT ESTABLISHED and must be resolved before signing:** whether H1 hunk H2 floors the declared AUC tolerance to the registered ±0.010 (S3). The hunk texts are not in `SCHEMA_SET_FINAL.md`.

## FILES

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md`
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\SCHEMA_SET_FINAL.md`

Nothing was created, edited, moved or deleted; no git command was run.