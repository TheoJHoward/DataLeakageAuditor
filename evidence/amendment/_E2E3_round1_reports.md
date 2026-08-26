## LEAD FINDING — the denominator is the declaration's to draw, and nothing sets a floor under it

The composed sections spend enormous force on *how* a unit leaves the scored arithmetic (declared, named, grounded, frozen, class C to move) and say **nothing about how few units may remain**. There is no non-emptiness test, no minimum-N test, and no cross-check against any artifact the declaration does not itself write. A detector that does nothing useful passes by being scored against a set the declaration shrank to the handful of units it happens to fire on.

Three composed facts produce this jointly. None of them is a defect alone.

**1. The scored population is declared, and identified only by a name the declaration coins.**

> SC-3(c): "**THE MAP COVERS THE WHOLE DECLARED SCORED POPULATION.** The declaration declares the scored population — the rows and units the criteria adjudicate."

> SC-4(j): "The declared scored set is identified by **the named constant the declaration declares**, never by its cardinality."

SC-4(j) forbids identifying the set by its size — which also removes the one quantity a reader could sanity-check it by. Nothing anywhere in the composed text ties the declared scored population to the fixture's actual content.

**2. The one independent cross-check that existed in registered v30 is affirmatively barred from entering.**

Registered §6.2 keeps a manifest-side ground truth: "**Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and **the count of independently leaking sources**." SC-4(a) then says:

> "An evidence artifact's classification of how a unit was *built* answers a different question from what the map declares *violating* on the scored side under the declared branch; the two do not in general have the same answer. **No classification of the scored set other than this derivation enters any criterion, denominator, or count**, and no split within such a classification carries gate arithmetic."

> SC-4(b): "**N is the length of the REQUIRED list**, and no other quantity is N."

So the manifest's count of independently leaking sources — a fact about the fixture, not about the declaration — may not enter any denominator or count. The REQUIRED list, derived from the map the declaration writes, is the only denominator. Criterion 1's own registered population term ("**Every** ground-truth leaking source column…") is a manifest classification and is therefore barred by SC-4(a) from entering criterion 1. The composition silently re-bases criterion 1 onto the declaration.

**3. The exit is unbounded below, and the closure language the drafters use elsewhere is absent here.**

> SC-4(b), UNSCORED row: "scoring on it is declared impossible, **on a ground the declaration states**"

> SC-4(e): "A unit is excluded only on a ground the declaration states. **Two grounds are registered here because** each is otherwise a guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that cannot carry a finding of the scored class at all**…, and a unit whose **construction or lag treatment is declared UNRESOLVED**…"

SC-4(e) requires *a* ground; it never says these are the only admissible grounds. Contrast the closure language these same drafters use when they mean closure:

> SC-12(w1): "The grounds on which this state may be entered are **exhaustively enumerated in this limb; the enumeration is closed, and it has no members.**"
> SC-4(b): "**There is no fourth class and no residue class.**"
> SC-3(b): "THREE DISPOSITIONS, **MUTUALLY EXCLUSIVE AND EXHAUSTIVE** OVER THE MAP."

The unscored-ground list is the one enumeration in the composed text that is *not* declared closed. And precedence runs the wrong way for the gate:

> SC-4(c): "Where a unit satisfies more than one class predicate, **UNSCORED wins.**"

A unit the map declares violating (REQUIRED) *and* for which the declaration states an unscoreability ground resolves to UNSCORED. UNSCORED beats REQUIRED, by registered rule.

**What the anti-shrink clauses actually forbid.** Each one regulates the exit rather than closing it:

- SC-3(c): "A subclass of that population is never excluded, masked, or given a separate denominator by description; **the only way a unit leaves the scored arithmetic is by being an UNSCORED cell of the map**, declared as such before any detector runs." — this *names the licensed exit*.
- SC-6(e)/SC-3(b): unscored units are "**never reported as a pass**". This forbids calling the *unscored units* passing. It does not forbid the **gate** passing while most of the fixture is unscored. That is the gap in one sentence: the pass prohibition attaches to the units, not to the gate outcome.
- SC-8(d): "the justification **makes no reference to what the restriction does to any count**, and none may be added to it." This constrains the wording of the justification, not the effect, and is unfalsifiable after the fact.
- SC-4(e): "**Reinstating an excluded unit changes the denominator and is class C.**" This makes shrinkage *sticky*, not bounded.

**The proof that this is an omission rather than a design choice: the same registration installs exactly the missing test 500 lines later, for the other gate.**

> SC-13b(b1): "**If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is STOP.**"
> SC-13b(b4): "A detector whose declared labelled-unit set is empty **cannot change the criterion's outcome**, which is the defining condition of a waiver under the floor's own definition."

SC-13b(b1)/(b2) is a non-empty-denominator admissibility test, tested "before any detector runs, and before any limb of the criterion." §6.2's gate has no counterpart. And the composed text expressly blocks importing one:

> SC-12, what the definition does NOT permit, item (2): "**It does not reach any other criterion and may not be cited to soften §6.2's.**"

That sentence was written to stop the waiver definition being used to *weaken* §6.2. Composed, it equally stops the waiver floor from *protecting* §6.2. §6.2's gate is the one gate in the registration with no admissibility test and no waiver floor.

---

## THE SIX ATTACKS

### 1. Fires on EVERYTHING — caught on three surfaces, all three shrinkable by the declaration

The catching limbs, quoted:

> Criterion 2: "No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`."
> SC-3(b): "**A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier, primary or secondary."
> Criterion 4: "Silent under the identity control on both."

Coverage is **not** uniform across sides and combinations:

- **Criterion 2 is single-sided** — `fixture_contaminated` only, by its own text. On the other side, clean columns are protected only by the map.
- **SC-3(b) bites only on cells the map *excludes*, not on cells it does not cover.** SC-3(b) itself: "**A cell the map does not cover is UNSCORED**… It requires no finding and **forbids none**". SC-6(d): "**FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored observations**, separately from the false-positive tally, and they **carry no criterion consequence in either direction.**" So the false-positive surface is exactly the size of the map's non-unscored rows — a quantity the declaration sets. Attack 1 composes directly with the lead finding: a maximally-unscored map leaves a promiscuous detector with almost no false-positive surface.
- **Criterion 2 has no population left after composition.** This is a distinct semantic defect. Three composed clauses give it three incompatible populations, and a fourth says it may have none:
  - Criterion 2 (registered): "**manifest-clean** source column"
  - SC-5(c): "that criterion's scope is **the units the declaration declares clean**, and those units **do** route to it"
  - SC-4(a): "**No classification of the scored set other than this derivation enters any criterion**"
  - SC-4(b): the derivation's three classes are REQUIRED / OUT OF JURISDICTION / UNSCORED — **there is no CLEAN class**, and "There is no fourth class and no residue class."

  Under SC-4(b) a clean column must be OUT OF JURISDICTION or UNSCORED. If OUT OF JURISDICTION, SC-5(c) expressly routes the finding *away* from criterion 2: "**It is not converted into a failure of the clean-source criterion, which has no landing site for such a unit**"; and "**The false-positive consequence is never carried beyond the out-of-jurisdiction class.**" If UNSCORED, SC-6(d) neutralises it. Either way criterion 2 — the strictest false-positive limb in the gate, the one whose drafting note says "A classifier the tool controls cannot be allowed to decide what counts against it" — is left with no units it can adjudicate. **NOT ESTABLISHED** that any composed clause supplies criterion 2 a population; SC-5(c) is the only clause that names one, and it names the declaration's, not the manifest's.

- **Criterion 4 may be evaluable on nothing.** SC-2(a): "An artifact **not in that enumeration is not part of the fixture and no criterion is evaluated on it.**" Nothing in the composed sections requires the identity control to appear in SC-2(a)'s enumeration. SC-5(f) presupposes an identity control exists and requires sentinels "**enumerated in the declaration ex ante**", but does not require the control itself to be enumerated. Whether criterion 4 survives turns on whether "the identity control" is an artifact (reachable by SC-2(a)) or a mode of evaluation (not reachable) — **NOT ESTABLISHED** in the composed text. If it is an artifact, attack 1's last unconditional catch is removable by omission from a declaration list.

### 2. Fires on NOTHING — the requirement is per-unit, but the unit count is not floored

Per-unit, correctly:

> Criterion 1: "**Every** ground-truth leaking source column receives at least one **primary runtime finding**"
> SC-4(b), REQUIRED row: "at least one **primary** runtime finding attributed to it is required; absence is a miss"

There is no aggregate satisfaction route — the descriptive count is expressly non-gating ("It is published as a count, never as a decimal or percentage… a descriptive fixture outcome rather than a performance rate"). So the *shape* of the requirement is sound.

**What is missing is the floor on N.** Nothing states that the REQUIRED list must be non-empty. With N = 0 criterion 1 is vacuously satisfied, criterion 2 is vacuous (no findings), criterion 3 produces no false positives, criterion 4 is silent. A detector that emits nothing passes all four. SC-13b(b1) is the exact test that would stop this and it is scoped to §10.2's ambiguity branch by its own opening ("ADMISSIBILITY FOR THE CRITERION ABOVE"), and SC-12 item (2) blocks citing the waiver floor into §6.2.

**A second gap in the same attack: a miss has no stated gate consequence at cell level.** SC-3(b) attaches "fails the gate" to false positives twice and to misses never:

> "**A finding the map predicts is REQUIRED.** Its absence is a miss." (no consequence stated)
> "**A finding the map excludes is a FALSE POSITIVE.** It fails the gate…"
> SC-3(h): "A finding on a cell the map marks zero is still a false positive and **still fails the gate.**"

Criterion 1 catches misses at *unit* level, and only to the depth of "at least one". SC-6(c) makes the levels independent: "**A cell-level `unscored` never makes its unit `unscored`**, and a unit-level `unscored` does not make every cell of that unit unscored." So a detector that fires once per REQUIRED unit and misses every other cell the map predicts satisfies criterion 1 in full, and criterion 3 records the misses with no quoted consequence. **NOT ESTABLISHED** that a criterion-3 miss fails the gate.

### 3. Tuned to the declared map — the runtime channel is closed; the design-time channel is not

Runtime is closed cleanly, and this is the best-drafted clause in the composition:

> SC-7(b): "**IT NEVER RECEIVES, AT ANY POINT IN A GATE RUN**: … **the declared ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it."
> SC-7(c): "A detector that could read it would be graded against a key it had seen, and the run would measure **retrieval rather than discrimination**… **A run that received the key has not produced a gate result, whatever it reports.**"
> SC-7(d): "**A single run given more than one side satisfies none of the criteria, however its outputs are partitioned afterwards.**"

The residue is that both scoping phrases are about the *run*: "**AT GATE TIME** a detector receives exactly two things" and "at any point **in a gate run**". The map is a committed, hashed file that must exist and be checkable *before* the detector is configured:

> SC-8(c): "**EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS.** Every declared object the gate consumes — the map, the partition, the exclusions… must be **regenerable and checkable from the declared inputs alone, before any detector runs.**"
> SC-8(f): "Every file the freeze ranges over — **including the declaration itself, which carries the scoring key** — is hashed in the amended registration's tag message"

So the key is published before the configuration freezes. The only text that touches the design-time channel is the ordering line, which names the licensed tuning object but states no prohibition:

> "**Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. **Defaults may not be altered after observing a fixture result.**"

The prohibition is on altering defaults after observing a **result**, not after reading the **key**. **Nothing in the composed sections prohibits tuning the frozen default configuration against the declared map before the tag.** A detector whose behaviour was fitted to the map at design time receives nothing forbidden at gate time and SC-7 is satisfied on its face. Closing this needs a sentence in SC-7 or SC-8 of the form "the frozen configuration is justified without reference to the map, and the map is not an input to configuration selection" — the SC-8(d) pattern, applied to the configuration instead of to a scope.

### 4. Non-terminal coverage state everywhere — `not_applicable` and `unscored` are free at §6.2

| State | What it costs at §6.2 |
|---|---|
| `waived` | Prohibited outright. SC-12(w1): "**NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.**" Plus §8.3 line 929 as amended and SC-12(w7): "The gate report publishes the count… **That count is zero.**" |
| `unsupported`, `could_not_run` | §8.3 only: "`assert_audit_complete()` — fails on any `unsupported`, `could_not_run`, or **`waived`** **detector-case** entry" |
| `not_applicable` | **Nothing.** Not in `assert_audit_complete()`'s failure set; §6.2 has no `not_applicable`-everywhere disposition. Costs only a criterion-1 miss on REQUIRED units. |
| `unscored` (SC-6) | **Nothing at all**, once the pre-run ledger names the unit. "It **enters no denominator**, **contributes to no rate**"; SC-6(d) no false-positive consequence; and SC-12(w6) item (6) keeps it out of the assertion: "**`unscored` is not added to that failure set, and must not be**". |

Two observations. First, SC-13b(b3) is a full, explicit disposition of the `not_applicable`-everywhere state — "its `preserving` proof yield on that side is therefore **zero**… **zero fails SC-13a(a2)'s strictly-greater-than-zero threshold, and the STOP is tripped and published**" — and it exists **only** for §10.2. §6.2 has no non-zero threshold anywhere, so §6.2 cannot make `not_applicable` cost anything except through criterion 1's per-unit requirement, which the lead finding shrinks. Second, **NOT ESTABLISHED** that §8.3's assertions gate §6.2 acceptance at all: §6.2's "Pass gate" enumerates four criteria and does not reference §8.3, so the assertion cost on `unsupported`/`could_not_run` may be a reporting cost only.

### 5. Correct on one combination, useless on the other — nothing in §6.2 stops this

Criterion 1 is expressly combination-agnostic:

> "at least one **primary runtime finding**, **whether its promotion status makes the reported tier PROVEN or REVIEW**"

A single `preserving` finding per REQUIRED unit discharges criterion 1; a `promoted` combination that is identically silent costs nothing. Every per-combination rule in the composition is walled off from §6.2:

- SC-12(w4): "**THE PROHIBITION BINDS PER CASE AND PER COMBINATION**" — but SC-12 item (2): "It does not reach any other criterion and **may not be cited to soften §6.2's**."
- SC-13c(c4): "**EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED**… the other combination is **executed to a terminal result**… and publishes its own registered yield" — but in the same limb: "Its published yield is a required output of the criterion and **carries no threshold of its own.**" And SC-13c(c6): "these clauses make proof yield gating **for this criterion only**".
- §10.2 criterion 3's per-combination gates are the finding-rate gate (fires on *too many* findings on clean cases) and the completion gate (60% reach `completed`). A combination that executes to `completed` and finds nothing passes both trivially.

So: **no composed clause requires the `promoted` combination to produce a finding anywhere**, at §6.2 or at §10.2. A detector half-built passes.

### 6. Shrinking the scored population — see the lead finding

The licensed routes, all declaration-side, all frozen pre-run, none floored:

1. **Draw the declared scored population narrow** — SC-3(c) first sentence; SC-4(j) forbids identifying it by cardinality.
2. **Mark rows UNSCORED inside it** — SC-3(b) third disposition; SC-6(b)'s ledger; SC-4(b)'s UNSCORED row; SC-4(c)'s precedence, under which UNSCORED beats REQUIRED.
3. **Omit artifacts from SC-2(a)'s enumeration** — "An artifact not in that enumeration is not part of the fixture and **no criterion is evaluated on it**." SC-2(b) makes *changing* the composition class C; it does not constrain the initial composition.
4. **Shrink the anchor by enumeration** — the same genus: "declared… as an **enumerated set of entries**, one per declared horizon and side". A one-entry enumeration is one check.

On the SC-3(b)/SC-3(c) tension: (c) says the map covers the whole declared scored population while (b) contemplates cells the map does not cover. The reconciliation is that "covers" means "has a row for" — SC-3(a) requires "the field that records whether the cell is scored", so an unscored row is coverage. Which means SC-3(b)'s uncovered-cell disposition applies precisely *outside* the declared scored population. **The exit from the arithmetic is the boundary of the declared scored population, and SC-3(c) hands the declaration the pen that draws it.**

---

## WHAT WOULD CLOSE THE LEAD HOLE

One clause, modelled on SC-13b(b1)/(b2), landing in §6.2:

- REQUIRED must be non-empty per side, tested before any detector runs, on pain of STOP;
- the REQUIRED list is reconciled against the manifest DAG's count of independently leaking sources, with every difference named and grounded per unit — which requires carving an exception into SC-4(a)'s "No classification of the scored set other than this derivation enters any criterion, denominator, or count", since that sentence as composed forbids the reconciliation;
- SC-4(e)'s grounds enumeration is declared **closed**, in SC-12(w1)'s language;
- SC-3(b)'s "fails the gate" is extended to misses on REQUIRED cells, or criterion 3 is stated to fail on a miss.

## FILES

- Composed sections read in full: `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\_E3_composed_sections.md`
- Nothing was created, edited, moved or deleted; no git command was run.

==============================================================================
## LEAD FINDING — the criterion-1 denominator has a declarer-controlled exit that beats the entry, and its ground list is not closed

The three-class table registers predicates that are not of the same kind. REQUIRED and OUT OF JURISDICTION are predicates about the fixture; UNSCORED is a predicate about the declaration:

| Class | Registered predicate |
|---|---|
| **REQUIRED** | "the map declares a violation on it, on the scored side, under the declared branch" |
| **OUT OF JURISDICTION** | "every constituent read is declared legal at the boundary instant under the declared branch" |
| **UNSCORED** | "**scoring on it is declared impossible, on a ground the declaration states**" |

UNSCORED is satisfied by the act of declaring it. Then SC-4(c):

> "**(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED wins.**"

So the self-satisfying predicate takes precedence over the substantive one. For any unit the map declares violating, the declarer states a ground of impossibility, both predicates fire, precedence resolves to UNSCORED, and the unit leaves the denominator — with SC-4(b) confirming the arithmetic consequence: "**N is the length of the REQUIRED list, and no other quantity is N**."

**The one clause that looks like a constraint does not close the list.** SC-4(e):

> "A unit is excluded only on a ground the declaration states. Two grounds are registered here because each is otherwise a guaranteed failure of criterion 1 for a reason unrelated to detection..."

"only on a ground the declaration states" is procedural — state *a* ground — not substantive. "Two grounds are registered here **because** each is otherwise a guaranteed failure" gives a rationale for those two; it does not say no third exists. This amendment demonstrably knows how to close an enumeration and says so in terms when it means it — SC-12(w1): "the enumeration is **closed**, and it has **no members**"; SC-4(b): "**There is no fourth class and no residue class.**" SC-4(e) has no such sentence.

**Worse: SC-4(e) may not even be about UNSCORED.** It governs a status called EXCLUDED, which is not one of the three classes SC-4(b) declares "mutually exclusive and exhaustive." SC-4(d)(ii) treats EXCLUDED as the removing status ("only a gate status the declaration declares EXCLUDED ... removes a unit from the arithmetic"), while SC-3(c) names UNSCORED as the removing status ("the only way a unit leaves the scored arithmetic is by being an UNSCORED cell of the map"), and SC-13b(b4)(iii) uses both as alternatives: "declared EXCLUDED or `unscored` on a stated ground." Whether EXCLUDED is UNSCORED renamed or a fourth status SC-4(b) forbids is **NOT ESTABLISHED**. Either reading hurts: if renamed, my point above stands directly; if distinct, SC-4(b)'s exhaustiveness claim is false and there are two exits.

**Nothing registers a floor on N.** No clause in the composed text states that the REQUIRED list is non-empty, that |UNSCORED| is bounded, or that N bears any relation to an independently measured quantity. With REQUIRED = ∅, criterion 1 ("**Every** ground-truth leaking source column receives at least one **primary runtime finding**") is vacuously satisfied, SC-4(f)(3)'s partition check passes (0 + |OOJ| + |UNSCORED| = |declared scored set|), and the descriptive count publishes "0 of 0."

**The asymmetry is the proof that this is an omission, not a design.** The same amendment registers exactly this floor on the other branch — SC-13b(b1): "**If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is STOP**," with (b2) extending it per side. And SC-13b(b4)(iii) names the manoeuvre verbatim as a real run condition: "**every unit that could carry that detector's character is declared EXCLUDED or `unscored` on a stated ground, so none survives into the enumeration.**" On §10.2's ambiguity branch that state trips a STOP. On §6.2's acceptance gate it trips nothing. SC-13b(b4)'s own reasoning — "cannot change the criterion's outcome, which is the defining condition of a waiver" — applies unaltered to SC-4 and is not applied there.

**SC-3(h) states the conclusion without registering a mechanism:** "The unscored disposition is not an escape hatch." That is an assertion. SC-4(c) is a rule. The rule runs the other way.

---

## SECOND FINDING — the map is unanchored, and SC-4(a) expressly bars the object that could have anchored it

Criterion 1's operative text still names a manifest object: "Every **ground-truth leaking source column**..." The manifest carries that object — "**Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources" — and the contamination-class clause keeps it there: "the ground-truth column DAG and the count of independently leaking sources **remain manifest content and are satisfied there.**"

But SC-4 relocates the denominator to the declaration's map and then severs the manifest from the count:

> "An evidence artifact's classification of how a unit was *built* answers a different question from what the map declares *violating* on the scored side under the declared branch; the two do not in general have the same answer. **No classification of the scored set other than this derivation enters any criterion, denominator, or count**"

And the manifest is an evidence artifact by this amendment's own words: "A manifest is the product of a dated measurement round and records what was measured."

Result: the only dated, independently measured record of what leaks is barred from the arithmetic, and **no clause requires the REQUIRED list to contain every column the manifest DAG lists as a leaking source**. I traced for one and found none — **NOT ESTABLISHED**. The distinction SC-4(a) draws (built-vs-violating) is real; its arithmetic effect is that the map floats free of measurement.

The direction of the re-anchoring is the direction of leniency, and the composed text is inconsistent about it. Criterion 2 — the criterion that can only *fail* a detector — retains its manifest anchor in the operative text: "No **manifest-clean** source column receives any runtime finding of any tier." But SC-5(c) re-anchors it to the declaration: "that criterion's scope is **the units the declaration declares clean**, and those units **do** route to it." Two different sets scope criterion 2 in the composed document. Which governs is **NOT ESTABLISHED**.

Chain of declarer-controlled reductions, all pre-tag, all frozen, none floored, each invisible to the check below it:
1. SC-2(a) — which artifacts are in the fixture ("An artifact not in that enumeration is **not part of the fixture** and no criterion is evaluated on it")
2. SC-3(c)/SC-4(j) — which units are in the declared scored population (identified "by **the named constant the declaration declares**, never by its cardinality")
3. SC-3(a)/(b) — which cells the map covers and what it declares
4. SC-4(c)+(e) — which covered units go to UNSCORED anyway

SC-4(f)(3)'s partition check sums over the set produced by step 2, so steps 1 and 2 are outside its reach entirely.

---

## Q1 — the freeze, traced

**Who decides the denominator.** The registered rule decides the *function*; the declaration supplies every *input*. SC-4(a): "The rule ... is **registered in this clause** ... and is not the declaration's to state, restate, or rewrite," with the declaration stating "the class assigned, and the registered predicate the unit satisfies, **by citation**." That correctly stops the declarer rewriting the predicates. It does not stop the declarer choosing the facts the predicates range over — and the REQUIRED predicate ranges over "what the map declares," which is the declarer's own artifact.

**Can the decision be made after a result is seen?** Not the primary decision. The freeze:

> "**(a) EVERYTHING THE GATE CONSUMES FREEZES AT THE AMENDED REGISTRATION'S TAG.** At the moment the tag is signed, every object a gate outcome can be computed from becomes **locked**, and any subsequent change to any of them is a class C amendment requiring a further amended registration."

> "**(b) WHAT FREEZES IS THE OBJECT IN ITS AUDITABLE FORM — LISTS, NOT COUNTS.** A partition freezes as its **enumerated lists of member names** ... **A count is not a freeze**"

Reinforced by SC-3(h) ("declared and frozen before any detector runs ... a map frozen after a run is a key shaped by the result and scores nothing"), SC-4(h) ("changing N, after the tag is a class C amendment"), SC-8(c) ("regenerable and checkable from the declared inputs alone, before any detector runs"), and SC-8(f), which hashes the declaration itself in the tag message.

**This freeze is strong, and it is the wrong tool for the hole.** It locks the declarer's choices against later revision. It places no constraint on what those choices may be. SC-8(f)'s hash proves the map did not move; it says nothing about whether the map was ever adequate.

**Two secondary leaks in the freeze itself:**

- **Disclosed post-result revision is licensed.** SC-8(e): a wrong number is "recorded, an amended registration is committed, and the affected benchmark is regenerated as a new version under §6.4 **with the superseded results published alongside.**" This is honest — the fail stays published — but it is a live path from an observed fail to a published pass, and it is stronger than SC-8(e)'s own headline ("In-place correction after a result has been observed is precisely how a fail becomes a pass") suggests, because the prohibition is on *in-place* correction only.
- **Two different post-tag procedures for the same frozen object.** SC-8(a) requires "a class C amendment requiring a further amended registration." SC-13b(b1) licenses "supplementing the declaration with a declared, enumerated set for the empty detector and **re-freezing under §11's integrity chain**" — not labelled class C, no further amended registration named. Both act on the frozen declaration. Which governs a post-tag supplement is **NOT ESTABLISHED**.

---

## Q2 — the partition, tested against a motivated declarer

Answered in the lead. To state the test explicitly: a declarer wanting a small N does not need to lie, hide, or act after a result. The compliant sequence is:

1. Declare the scored population (SC-4(j) — a named constant, no cardinality published, nothing to compare it against).
2. Declare the map over it (SC-3(a) — "declared in the fixture's availability declaration").
3. For each hard unit, state a ground of impossibility. SC-4(c) resolves the overlap to UNSCORED; SC-4(c) requires only that "the declaration records which it satisfies and that precedence decided it."
4. Publish the three lists (SC-4(f)(1)) and the partition check (SC-4(f)(3)). Both pass.

Everything is disclosed. Nothing fails. **SC-4's defence is auditability, not prevention** — the shrinkage is visible in the published UNSCORED list, and a reader must notice and object. The gate arithmetic itself registers no objection. SC-4(i) ("DISAGREEMENT HALTS") catches only disagreement "between the rule-derived class and the frozen class" — re-deriving the rule over the same declared facts reproduces the same classes, so it never fires on this.

Note the precedence direction: the more clearly the map declares a violation on a unit *and* the more plausibly it can be called unscoreable, the more SC-4(c) favours removal. SC-4(e) gives a defensible reason for that direction (a degenerate unit "makes criterion 1 unsatisfiable"). The reason is sound; the unbounded ground list is what converts it into a lever.

---

## Q3 — what `unscored` and `waived` cost a detector

**`waived` is fully priced.** SC-12(w1): "**NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.**" SC-12(w7): "The gate report publishes the count ... **That count is zero.**" And §8.3 makes it checkable: "`assert_audit_complete()` — fails on any `unsupported`, `could_not_run`, or **`waived`** detector-case entry." SC-12(w6) states the design correctly: "A prohibition no assertion tests is not enforced." This limb is well built.

**`unscored` costs exactly nothing.** SC-6(a): "It **enters no denominator**, **contributes to no rate**." SC-6(d): "they carry **no criterion consequence in either direction**." SC-12(w6): "**`unscored` is not added to that failure set, and must not be**."

**The question's axis is the wrong one, and the composed text says so.** There is no path to "neither a terminal result nor a penalising state" — SC-12(w2) closes it: "Those rules dispose of every detector-case between them, and **the residue this state would have carried is empty.**" The free path is the sharper combination: **terminal result *and* zero consequence**, licensed in terms by SC-6(a):

> "It is neither a pass nor a not-run: **the detector may have executed perfectly and there is still nothing to score.**"

A detector that fires on nothing, on a fixture whose declaration classes the hard units UNSCORED, executes every case to a terminal state, passes `assert_audit_complete()`, enters no denominator, and is charged nothing. `not_applicable` is equally free — it is in the §7.7 table and in no assertion's failure set.

**Same asymmetry as the lead finding.** `not_applicable`-everywhere is priced on §10.2's branch and nowhere else. SC-13b(b3): "its `preserving` proof yield on that side is therefore **zero — a defined 0/N over declared units, not a 0/0**; **zero fails SC-13a(a2)'s strictly-greater-than-zero threshold, and the STOP is tripped and published.**" §6.2 has no counterpart.

**SC-12 item (4) is the intended closure and does not reach §6.2.** "**'No data' is not 'waived'** — a cell with no data is `unscored` (SC-6) ... **doing at the level of a whole detector what SC-6 forbids at the level of a cell is a waiver.**" Two problems. First, what SC-6 forbids at cell level is *being reported as a pass* (SC-6(e)); it does not forbid a cell being unscored, that being its purpose — so the transposition to detector level yields "don't report a whole detector as passing," not "don't unscore a whole detector." Second, "waived" carries consequence only where a criterion is written over it: §10.2's floor and §8.3's assertion (which reads detector-case coverage states, not gate classes). SC-12 says so itself, in a sentence drafted for the opposite purpose: "**(2) It does not reach any other criterion and may not be cited to soften §6.2's.**" That cuts both ways — the waiver definition, and item (4) with it, does not reach §6.2's criteria at all.

---

## Q4 — the three assertions

**What must be true for all three to pass, read off the composed text:**

- `assert_no_proven_leakage()` — "fails iff there exists an EvidenceEvent that (1) licenses PROVEN and (2) belongs to a non-experimental combination." Passes iff no such event exists. "**Ignores coverage.**"
- `assert_no_rule_violations()` — "fails on any RULE finding from a non-experimental detector mode. **Ignores coverage.**"
- `assert_audit_complete()` — "fails on any `unsupported`, `could_not_run`, or **`waived`** detector-case entry ... **Ignores findings.**"

**Yes — all three pass on a run that established nothing.** Every assertion is negative. Two fail only on findings and explicitly ignore coverage; the third fails only on three coverage states and explicitly ignores findings. **No assertion in the set fails on absence.** A run in which every detector-case reaches `passed`, `not_applicable`, or `unscored` and emits zero findings passes all three, and the passes are truthful.

The composed text anticipates the reverse misreading only: "**REVIEW findings of any basis do not trigger it**, and the report says so wherever any exist, so a passing assertion cannot be read as absence of evidence." That guard covers "a pass hides findings." It has no counterpart for "a pass hides that nothing was attempted."

**The amendment makes the empty run marginally easier, not harder.** Adding `waived` to the failure set removes the one state a silent-by-design detector might have used, leaving `not_applicable` and `unscored` as the compliant routes — both outside the failure set. SC-12(w6) gives the reason and it is correct as far as it goes: "a permitted state that failed an assertion would punish correct reporting." The consequence is that the assertion battery has no positive limb, and §8.3's three assertions cannot distinguish a working tool from a silent one.

Note that SC-6(e)'s "**THE PASS PROHIBITION IS ABSOLUTE**" and SC-6(a)'s "cannot be reported as a pass" bind the *unit's display*. They do not bind the *gate's* outcome. A gate can pass while its unscored list carries everything that mattered, with no unit ever described as passing.

---

## Q5 — the floor on the ambiguity branch

Floor as carried: "The replacement may be stricter than the floor and may not be weaker: **non-zero proof yield, neither runtime detector waived, criterion 3's gates in force.**"

**Limb 1 — binding, and the tightest construction in the document.** I attempted each trivial-satisfaction route and each is closed by name:

| Route | Closed by |
|---|---|
| empty denominator | SC-13b(b1)/(b2) — STOP, "lifted the same way and only that way" |
| narrow the denominator | SC-13a(a3) — "declares no stricture ... and performs no narrowing, restriction, projection, exclusion, or re-aggregation" |
| narrow by enumeration | SC-13a(a3) — "A declaration **may not use the enumeration to remove** from the denominator a pair the corpus labels and the risk logically applies to" |
| suppress the gate under line 816 | SC-13b(b3), SC-13c(c2) — express scoped disapplication |
| `not_applicable` everywhere | SC-13b(b3) — defined zero, fails the threshold, STOP |
| 0/0 | SC-13b(b2) — "**Consequence, stated so no reader ever decides it**" |
| report `waived` | SC-12(w1) |
| shorten the governed set | SC-13c(c3), SC-12 — "The declaration may not shorten the set" |
| score one detector only | SC-13c(c3) — "has not discharged SC-13b" |
| drop the other combination | SC-13c(c4) — executed, published, no threshold |
| reassign by jurisdiction | SC-13b(b4)'s removed fourth condition; SC-13c(c6) |

The one honest qualification is not a hole but a bar height, and the text states it on the record. `proof yield > 0` per detector per side clears on a single proven pair, and SC-13c(c7) endorses that: "A detector that probes few cohorts, proves what it probes, and publishes its coverage honestly **passes this criterion and is supposed to.**"

**Limb 2 — binding.** SC-12's five limbs, the pinned governed set at SC-13c(c3), no invocation procedure ("**it may not be invoked**"; "it does not become admissible by being recorded, disclosed, justified, or approved"), and checkability via (w7) and §8.3.

**Limb 3 — in force in form, hollow in content.** SC-13c(c5) holds every referent and names the version:

> "**(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION** ... **Its scoring rule and its three dispositions are SC-3(b)'s, held by citation and not restated here** ... **The cell key is the declaration's to supply, not this clause's to state** ... and **this clause names no key.**"

Limb 3 therefore imports SC-3 and SC-4 wholesale — including SC-3(b)'s UNSCORED disposition and SC-4(c)'s precedence — into a floor whose stated purpose is to stop a replacement being weaker. Limb 1's own author refused to let a declared set be empty (SC-13b(b1)). Limb 3 imports a rule with no non-emptiness requirement and expressly declines to supply the missing constraint ("this clause names no key"). **So: the floor's third limb adds nothing that the amended criterion 3 does not already carry, and the amended criterion 3 carries the lead finding's hole.**

The §10.2 referent is weaker still. SC-13c(c5)(ii) holds "§10.2 criterion 3's own two named gates, the finding-rate gate and the completion gate." Both are one-sided in the same direction as §8.3: the finding-rate gate fails at "**k ≥ floor(0.20 × N) + 1**" where k counts clean cases emitting findings — a silent detector has k = 0 and passes. And neither is a stop: failing them means "the affected detector **or mode** ships marked experimental." A gate whose worst outcome is a label cannot bind a floor.

Whether §7.7's detector-case coverage states map onto the `schedule_state` values the completion gate reads ("`schedule_state` ∈ {`completed`, `incomplete`}") is **NOT ESTABLISHED** in the composed text — so whether an executed-but-`not_applicable` case counts toward the 60% completion floor cannot be determined from what is here.

**Net on Q5:** the floor is binding through limbs 1 and 2 and does real work there. Limb 3 is satisfiable trivially, because it delegates to a criterion whose denominator the declarer controls without a floor.

---

## Summary

I traced all five. Four of them close or nearly close: the freeze (Q1) is strong at what it does; `waived` (Q3) is fully priced; floor limbs 1 and 2 (Q5) are the best-constructed clauses in the document.

The arithmetic hole is one hole appearing in four places. **Every gate quantity in §6.2 resolves to the declaration, the declaration's reductions are unfloored, and the amendment registers the missing floor on the §10.2 branch only.** Concretely, in the composed text there is no clause requiring the REQUIRED list to be non-empty, no clause bounding the UNSCORED list, no clause anchoring the map to the manifest DAG (and SC-4(a) bars the manifest from "any criterion, denominator, or count"), no assertion in §8.3 that fails on absence, and — via SC-13c(c5)(i) — the same gap inherited by the floor's third limb.

The smallest change that would close it is the one the amendment already wrote for the other branch: SC-13b(b1)'s STOP, transposed to SC-4 as a non-emptiness requirement on the REQUIRED list stated against an object the declarer does not author, plus a closing sentence on SC-4(e)'s ground list in the form SC-12(w1) already uses ("the enumeration is **closed**").

==============================================================================
## TASK E2-1 — WHAT THE SCHEMA SET LICENSES

Scope note: I read the applied text only — the blockquote after each **THE CLAUSE.** heading and after each **INSERTION TEXT** heading in `SCHEMA_SET_FINAL.md` (SC-1 … SC-13c, §13c-P, plus §AB's recording text, which is marked drafted-not-applied and is flagged as such where cited). Apparatus (REGISTERS / INSERTION POINT / DATA / ROWS / *Instance record*) is used only to show where a clause's stated intent and its operative text diverge. Ranked by cost of the abuse: Tier 1 = one sentence in the declaration, pre-run, no amendment, no measurement. Tier 2 = a reading or a report-writing choice. Tier 3 = needs an amendment or a construction.

---

### TIER 1 — free: write a sentence in the declaration and the unit is gone

**E2-1.01 — SC-4(e) + SC-4(b) + SC-4(c) + SC-6(a)/(d): the exclusion-ground list is open, and UNSCORED wins.**

SC-4(e), first sentence:

> A unit is excluded only on a ground the declaration states. Two grounds are registered here because each is otherwise a guaranteed failure of criterion 1 for a reason unrelated to detection: …

SC-4(b), UNSCORED row of the registered-predicate table:

> | **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |

SC-4(c):

> Where a unit satisfies more than one class predicate, **UNSCORED wins.**

SC-6(a):

> A unit is **`unscored`** when the declaration declares, **before any detector runs**, that scoring it is impossible on a stated ground.

SC-6(d):

> **(d) FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored observations**, separately from the false-positive tally, and they carry no criterion consequence in either direction.

**What it permits.** The predicate for UNSCORED is *"a ground the declaration states"* — the ground is the declaration's, and no registered text tests it, bounds it, or requires it to be measured. UNSCORED takes precedence over REQUIRED by (c). An UNSCORED unit produces no miss (SC-3(b)), no false positive (SC-6(d)), enters no denominator, and contributes to no rate. So: for any unit the detector misses, write a ground, and the unit's entire gate consequence disappears in both directions. This is the exact shape the brief names — an escape hatch reachable by DECLARING rather than by MEASURING — and it sits at the top of the set because it is the cheapest and it is total.

The drafters saw the shape and answered it with a sentence that has no operative content. SC-3(h):

> The unscored disposition is not an escape hatch.

That sentence states a conclusion; it registers no test, no closed ground list, no adjudicator, and no consequence for a ground that fails it. Contrast SC-12(w1), where the same drafters knew how to close an enumeration: *"the enumeration is **closed**, and it has **no members**."* SC-4(e) and SC-4(b)'s UNSCORED row have no such closure.

**Not established:** whether SC-4(e)'s "Two grounds are registered here" was intended as closure. SC-1's apparatus asserts it is — *"they are **closure statements**, where the number IS the rule"* — but the applied text of SC-4(e) says only that two grounds are registered *"because each is otherwise a guaranteed failure of criterion 1"*, i.e. it gives a reason for registering those two, not a prohibition on others, and its own leading sentence ("only on a ground the declaration states") is an open grant. The apparatus's reading is not carried by the applied words.

---

**E2-1.02 — SC-3(a) + SC-13c(c5)(i): the granularity of the entire scoring key is unconstrained declarant discretion.**

SC-3(a):

> **The declaration declares the cell key — the unit it declares the fixture to be partitioned into — and names it explicitly.**

SC-13c(c5)(i), making the discretion express:

> **The cell key is the declaration's to supply, not this clause's to state**: SC-3(a) requires that a key exist and be declared and named; SC-3(h) and SC-8 require it frozen with the map before any detector runs; and this clause names no key.

**What it permits.** Every requirement in the set is on the *existence*, *naming* and *freezing* of the key — none on its *granularity*. Coarsening the cell key monotonically helps in both directions under SC-3(b): a REQUIRED cell is satisfied by one finding anywhere inside it (so misses collapse), and there are fewer excluded cells to fire a false positive on. A declaration that partitions per-instrument-year instead of per-instrument-month, or per-side only, satisfies SC-3(a) word for word and makes criterion 3 substantially easier. Cost: choose a coarser noun. No amendment, no measurement, no justification obligation anywhere in the set.

---

**E2-1.03 — SC-5(e): jurisdictional routing removes a finding from the gate in both directions, and SC-13c(c6) confirms it works.**

SC-5(e):

> Where a finding's character belongs to a detector row **outside** the criteria this gate scores, the declaration assigns it to that row and it is **neither credited nor penalized here.**

SC-13c(c6) closes this route for the §10.2 kill criterion, and in doing so confirms it is open for the acceptance gate:

> a declaration statement that assigns a finding's character to a detector row and places it **outside an acceptance gate** does not place it outside **this** criterion … **A jurisdictional routing statement written about the acceptance gate reaches the acceptance gate and stops there.**

**What it permits.** The *character* of a finding is assigned by the declaration; the assignment sends it to a row this gate does not score; the finding is then neither credited nor penalized. The only registered check is timing (*"declared before any detector runs; it may not be made after seeing where the findings landed"*). Nothing constrains what character a finding has, and no clause requires the character assignment to be derivable from anything measured. SC-13c(c6) is drafted specifically to stop this from reaching SC-13a — which means the drafters understood the mechanism and left it operative against §6.2's four acceptance criteria, in terms.

---

**E2-1.04 — SC-9(d): the record is "completed" with entries dated before they were written.**

> **(d) WORKING-RESOLUTION AUTHORITY IS UNIFORM, AND SUPERSESSION IS ORDERED.** A working resolution binds by its content and its date, **not by where it was recorded**: a resolution issued in the course of the work binds exactly as one written into the record does, and the record is completed to contain it.

**What it permits.** A resolution that was never written down at the time binds by *its date* once someone asserts that date, and the record "is completed to contain it." There is no requirement of contemporaneous evidence, no external timestamp, and no test that the resolution was in fact issued when claimed. After a result is seen, any convenient rule can be entered into the ledger bearing an earlier date, and SC-9(d) makes it bind as though it had always been there. The limb's own second half — *"the ledger is append-only and an entry is never rewritten to agree with its successor"* — protects entries that exist and says nothing about inserting entries that did not. This is a general-purpose retroactive-authority grant sitting inside the clause titled "DECLARATION INTEGRITY".

Pairs with SC-9(e), which routes *strengthening* interpretations through working resolutions without amendment (see E2-1.14). Together they are a post-hoc amendment path that does not touch §0.2.1's class C machinery.

---

**E2-1.05 — SC-10(a)/(b): "NOT PART OF THE GATE" buys exemption from the freeze, and the condition on the exemption covers only figures.**

SC-10(a):

> The declaration marks such a body **NOT PART OF THE GATE**: nothing in it enters any acceptance criterion, any denominator, any rate, or the freeze of SC-8. It is published as a diagnostic, with its own provenance, and it is exempt from the freeze **precisely because** it is exempt from the arithmetic.

SC-10(b):

> Non-gated data may be added, revised, or withdrawn without amendment **provided its figures are never moved into an acceptance denominator.**

**What it permits.** The exemption is granted for the whole *body*; the condition that redeems it is stated only over that body's **figures** and only over **denominators**. But the set makes non-numeric material gate-determinative everywhere: exclusion **grounds** (SC-4(e), SC-6(a)), the **facts** on which a unit satisfies its predicate (SC-4(a)), the **readings** chosen at each edge (SC-4(d)), sentinel **signatures** (SC-5(f)), the **provenance** of each artifact (SC-2(a)), the **justification** of a scope restriction (SC-8(d)). None of these is a figure and none enters a denominator. Park them in a body marked NOT PART OF THE GATE and they are outside SC-8's freeze by SC-10(a)'s own words, hence outside SC-8(f)'s hash set and outside §11 item 8's tag enumeration — freely revisable after a result with no amendment and no trace in the integrity chain. The clause states its own load-bearing assumption ("precisely because it is exempt from the arithmetic") and then conditions the exemption on a narrower thing than the assumption requires.

---

**E2-1.06 — SC-4(d)(i): the anti-removal limb removes units, via a lattice the declaration declares.**

> **Two readings are registered as forbidden outright**, because each silently removes units from the arithmetic: (i) a locality condition may not be read more narrowly than the declared lattice, so a read of the same source at another instant of the same lattice does not by itself create a cross-source violation;

**What it permits.** The limb's framing is prohibitive, so a reviewer reads past it. Its operative effect is a grant: same-source reads at different instants of **the declared lattice** are declared non-violating by rule. The lattice is the declaration's — SC-1(c): *"A `column_roles` value (§2.3) names where a value sits on a lattice."* Declare a coarse lattice and a wider set of reads falls inside "the same lattice" and is licensed out of cross-source violation, which removes units from REQUIRED. The floor the limb sets ("may not be read more narrowly than the declared lattice") is anchored to a quantity the abuser controls. Cost: one word in the lattice declaration.

---

**E2-1.07 — SC-8(a): the freeze instant is the tag, and PREREG line 480 places the tag after the gate run.**

SC-8(a):

> **(a) EVERYTHING THE GATE CONSUMES FREEZES AT THE AMENDED REGISTRATION'S TAG.** At the moment the tag is signed, every object a gate outcome can be computed from becomes **locked**, and any subsequent change to any of them is a class C amendment requiring a further amended registration.

PREREG.md line 480, verbatim as read:

> **Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

**What it permits.** What line 480 freezes before the run is *the candidate configuration*. SC-8(a) supplies the freeze instant for everything else the gate consumes — the map, the partition, the exclusions, the cell key, the unscored ledger — and sets it at **the tag**, which line 480's own locked ordering places *after* "run the fixture gate". Read alone, SC-8(a) licenses composing the scoring key after seeing the gate result and then tagging it. Line 480's closing sentence does not close this: it forbids altering **defaults**, not the declaration.

The set does contain contrary text — SC-3(h) *"declared and frozen before any detector runs"*, SC-6(b) *"frozen before any detector runs"*, SC-8(c) *"checkable before any detector runs"* — but SC-8(c) is a **checkability** requirement, not a **composition-time** requirement: an object written after a run can still be *"regenerable and checkable from the declared inputs alone"*. So the amendment registers two freeze instants for the same objects and SC-8(a), the one carrying the heading and the class C consequence, is the later one. SC-13b(b1) then contemplates the post-attempt route on its face: *"The stop is lifted only by supplementing the declaration with a declared, enumerated set for the empty detector and **re-freezing under §11's integrity chain**."*

---

**E2-1.08 — SC-13b(b1)/(b2): the two STOPs are lifted by declaring more units, not by the detectors doing anything.**

SC-13b(b1):

> **If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is STOP.** The stop is lifted only by supplementing the declaration with a declared, enumerated set for the empty detector and re-freezing under §11's integrity chain — never by scoring the criterion on the remaining detector, never by suppressing the empty detector's gate, and never by a `DEVIATIONS.md` entry or a working resolution.

SC-13b(b2), same for a per-side cell:

> **trips the same STOP as (b1), lifted the same way and only that way**: by supplementing the declaration with declared, enumerated units for that detector on that side and re-freezing under §11.

**What it permits.** Both limbs present as hard kill conditions and both are discharged by an act of writing. The units are the declaration's to enumerate; nothing registered tests whether an enumerated unit is real, distinct, or non-trivial. The "never by …" list forecloses four *other* routes and thereby draws attention away from the one route it grants. Combined with SC-13a(a2)'s threshold of **> 0**, the admissibility test is satisfied by naming one unit per governed detector per declared side.

---

**E2-1.09 — SC-13a(a3): risk-kind labelling is the declaration's, and it decides which detector gets the provable pair.**

> The declaration supplies which pairs the corpus labels and **which detector's risk kind each is labelled for**; that is the instance data the registered denominator is defined over. … **A declaration may not use the enumeration to remove from the denominator a pair the corpus labels and the risk logically applies to** — that is a narrowing, it makes the criterion easier to pass, and line 1035 forbids a replacement weaker than the floor.

**What it permits.** The prohibition is against **removal**. It is silent on **reassignment between the two governed detectors**. SC-13a(a2) requires `proof yield > 0` for **each** governed detector on **each** side; yields are computed per detector. So the pass condition is: each detector needs one provable pair, per side. The declaration chooses which detector each labelled pair's risk kind belongs to. Assign the pairs your detectors can actually prove to whichever detector needs one, and both thresholds clear — with no pair removed from any denominator, so (a3)'s prohibition is never touched.

SC-13b(b4) shows the drafters were within one step of this and stopped short — it strikes a "fourth condition" about assigning units *to the other detector's jurisdiction* and disposes of it as either the forbidden narrowing or condition (i):

> where the risk logically applies to the reassigned unit, the reassignment is the narrowing SC-13a(a3) forbids in terms; and where it does not, the state just is condition (i).

That reasoning holds for reassignment that *empties* a set. It does not hold for reassignment that *balances* two non-empty sets, which is the abuse, and no applied limb reaches it.

---

**E2-1.10 — SC-2(d): "may not be widened" leaves the initial width free, and "approaching" is untestable.**

> **The declared tolerance applies per entry and may not be widened.** Because a recomputed anchor is a pure function of committed bytes, a deviation approaching the tolerance is a **stop-and-report**, not a pass.

DATA block, same clause: *"the reference-anchor entries and their tolerance."*

**What it permits.** The tolerance is supplied by the declaration and the clause constrains only its *movement*. A tolerance declared wide enough at the outset never needs widening. The second sentence, which is the clause's real safeguard, turns on **"approaching"** — a word with no registered threshold — so a report that declares a deviation is not "approaching" the tolerance has satisfied the sentence. The clause's own premise ("a pure function of committed bytes") argues the tolerance should be zero or near it; nothing in the applied text requires that.

---

**E2-1.11 — SC-11(e) + SC-11 DATA: the expectations that trigger the all-zero finding are written by the same person, and the limb licenses blaming the declaration.**

SC-11(e):

> Where a declared expectation predicts non-zero and the aggregate returns zero, **the zero is a finding about the aggregation or about the declaration — and never a pass.** It is reported as such and adjudicated before any gate outcome is written.

SC-11 DATA THE DECLARATION MUST SUPPLY:

> The expectation each aggregate is checked against …

**What it permits.** Two things. (1) The limb fires only where *a declared expectation predicts non-zero*; the expectations are the declaration's. Declare no non-zero expectation for an aggregate and (e) never fires on it — the strongest limb in SC-11 is disarmed by omission, with no clause requiring expectations to be complete over the aggregates. (2) The disjunction *"about the aggregation **or about the declaration**"* is an express licence to resolve an inconvenient zero by revising the declaration — and *"adjudicated before any gate outcome is written"* places that revision **before** the outcome, so SC-8(e)'s after-a-result machinery is never engaged. That is key revision timed to sit just inside the window where the key is still nominally ex ante.

---

**E2-1.12 — SC-11(b)/(c): the "minimum sufficient" check does not test the thing the reader is told it tests.**

SC-11(b):

> Assert that **every key the aggregation groups or filters on resolves to a real field with a non-empty domain in the source**, and that **the source is non-empty on those keys**; where a total is available by a second route, reconcile the two.

SC-11(c):

> A zero that survives the check is reportable and is reported **with the check named**, so a reader can tell a proved zero from an unproved one.

**What it permits.** The asserted conditions are schema-resolution and source-non-emptiness. A filter predicate that is well-formed, resolves against real fields, runs over a non-empty source, and matches nothing passes every assertion — which is the commonest way an aggregation silently returns zero. The reconciliation that would catch it is conditional (*"where a total is available by a second route"*), and availability of that route is judged by the implementer. So SC-11 licenses attaching the named check to a zero it did not prove, and SC-11(c) then instructs the reader to treat the named check as the difference between a proved and an unproved zero. A safeguard that mislabels its own output is worse than none, because it retires the reader's suspicion.

---

### TIER 2 — a reading, or a report-writing choice

**E2-1.13 — SC-5(c) neutralises SC-3(b)'s false-positive consequence everywhere except one class.**

SC-3(b):

> **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier, primary or secondary.

SC-5(c):

> **(c) THE FALSE-POSITIVE CONSEQUENCE ATTACHES TO THE OUT-OF-JURISDICTION CLASS AND TO NO OTHER.** … **The false-positive consequence is never carried beyond the out-of-jurisdiction class.**

**What it permits.** SC-3(b) attaches the fail to *any finding the map excludes*. SC-5(c) attaches it to *the OOJ class and to no other*, twice, in absolute terms. SC-5(b) then supplies the case the pair creates: a finding on a REQUIRED unit but on a ground the map does not declare —

> **a finding on the legal ground does not satisfy the REQUIRED entry.** It is recorded on its own ground, and not credited to the unit's REQUIRED status.

— is a finding the map excludes (SC-3(b): false positive, fails the gate) on a unit that is not OOJ (SC-5(c): consequence never carried there). SC-5(c) is the more specific text and it is the one written as an absolute. A motivated reader classifies aggressively toward REQUIRED; spurious findings on REQUIRED units are then "recorded on their own ground" and carry no gate consequence at all. SC-5(d) partially recovers this via criterion 3 (*"charged under both the false-positive tally and criterion 3"*) but only *"Where a finding is a false positive under (c)"* — i.e. only for OOJ units, closing the loop back on itself.

---

**E2-1.14 — SC-9(e): "stronger" is undefined, multi-directional, and judged by the party it binds.**

> **An interpretation of locked text may resolve ONLY toward the STRONGER reading.** Any interpretation that weakens a locked obligation — narrows a denominator, exempts a unit, softens a criterion, admits an excluded set, converts a required finding into an optional one, or converts an unscored cell into a pass — is a class C amendment … This binds every entry appended after the rule, and **it binds the reading of this registration by its own author.**

**What it permits.** The prohibition side is enumerated and concrete. The permission side — *strengthening* — is unbounded and undefined, and it travels by **working resolution**, without amendment, without a tag, and (with SC-9(d)) without a contemporaneous record. There is no registered metric for "stronger", and the set contains obligations that trade against each other: widening one denominator strengthens one criterion and can relieve another; holding "every referent in force" (SC-13c(c5)) strengthens in one direction and multiplies the surfaces on which a disagreement can be resolved. The clause's last sentence — *"it binds the reading of this registration by its own author"* — is the tell: the author is both the bound party and the sole judge of which direction is stronger. Combined with E2-1.04, that is an amendment mechanism that bypasses class C by labelling.

---

**E2-1.15 — SC-12 item (2) and SC-13c(c6): the acceptance gate has no waiver prohibition, and two clauses forbid importing one.**

SC-12, "What this definition does NOT permit", item (2):

> (2) It does not reach any other criterion and may not be cited to soften §6.2's.

SC-13c(c6):

> **It creates no acceptance criterion, amends none, and is never cited against one.**

**What it permits.** SC-12 defines waiver — *"the criterion is written, configured, or reported in any way that makes the detector's own result **incapable of changing the criterion's outcome**"* — and forbids it, for **§10.2's replacement criterion only**. Item (2) then forecloses citing the definition against §6.2, and SC-13c(c6) forecloses citing SC-13a–c against an acceptance criterion. So the four criteria of §6.2 — the gate this entire amendment exists to make scorable — are the one place in the registration where a detector may be made incapable of changing an outcome, and the set expressly bars the two texts that would name the act.

Item (2) reads as a modesty limb. Its effect is a carve-out. Every mechanism above (E2-1.01, 02, 03, 06) achieves precisely a §6.2 waiver in SC-12's own words, and SC-12 has been drafted so that it cannot be cited to say so.

---

**E2-1.16 — SC-9(a): the closed list of what a declaration may not create omits everything the declaration actually controls.**

> **(a) A DECLARATION SUPPLIES DATA UNDER A REGISTERED SCHEMA. IT CREATES NO GATE OBJECT.** … **It creates no new criterion, no new denominator, no new coverage state, no new unit, and no new gate class.**

**What it permits.** Five things are forbidden. Not on the list, and each determinative of a gate outcome under the applied text: an **exclusion ground** (SC-4(e)), an **unscored ground** (SC-6(a)), the **cell key** (SC-3(a)), the **scored population** (SC-3(c)), the **lattice** (SC-4(d)(i)), the **edge reading** where a predicate admits two (SC-4(d): *"the declaration states which it derives under and why"*), the **character assignment** that routes a finding out of the gate (SC-5(e)), the **sentinel enumeration** (SC-5(f)), the **anchor tolerance** (SC-2(d)), the **risk-kind labelling** (SC-13a(a3)), and the **expectations** the all-zero control is checked against (SC-11 DATA). An enumeration this specific, in a clause whose heading is an absolute ("IT CREATES NO GATE OBJECT"), is read by everyone downstream as exhaustive — which converts every omission into a licence. The heading and the list say different things and the list governs.

---

**E2-1.17 — SC-3(b) vs SC-6(b): an omitted cell reaches the UNSCORED disposition without ever entering the ledger.**

SC-3(b):

> **A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none, enters no denominator, contributes to no rate, and is **never reported as a pass.**

SC-6(b):

> A unit may be reported `unscored` **only if it appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector runs.**

**What it permits.** SC-6(b)'s gate is on **reporting** a unit `unscored` and is stated at **unit** level. SC-3(b) confers the substantive disposition — no finding required, none forbidden, no denominator, no rate — on any **cell** by the bare fact of non-coverage, with no ledger entry and no ground. SC-3(c) tries to close this (*"the only way a unit leaves the scored arithmetic is by being an UNSCORED cell of the map, declared as such before any detector runs"*) but SC-3(b) has already made non-coverage sufficient at cell level, and SC-6(c) confirms the two levels do not collapse: *"A cell-level `unscored` never makes its unit `unscored`."* Net: cells can be dropped from the map by silence and inherit the full no-consequence disposition, while the ledger discipline applies only to the unit level.

---

**E2-1.18 — SC-8(d): the test is on the prose of the justification, not on the choice.**

> **(d) A SCOPE CHOICE IS JUSTIFIED INDEPENDENTLY OF ITS EFFECT ON ANY NUMBER.** Where the declaration restricts a scope — a class set, a cohort, a population — the justification **makes no reference to what the restriction does to any count, and none may be added to it.**

**What it permits.** The operative requirement is that the written justification not *mention* counts. A restriction adopted entirely for its effect on a count satisfies the limb provided the sentence justifying it is written in other terms. This is a syntactic check on a text, standing in for a substantive check on a motive, in the clause that carries the freeze. It is also the only place in the set that reaches the *drawing* of the scored population (E2-1.16), so it is bearing more weight than its form supports.

---

**E2-1.19 — SC-2(e) and SC-9(c): deferral to an event the deferring party names.**

SC-2(e):

> A registered element that cannot be satisfied at the instant the amendment must be committed is **amended explicitly — never waived and never left outstanding.** Where the move re-registers the element as a later-phase obligation, the obligation names the event that makes it due, and its scoring rule is declared **ex ante, at the move**, so it cannot be chosen after a result is seen.

SC-9(c) repeats the same grant verbatim in its second half.

**What it permits.** The framing is anti-waiver ("never waived and never left outstanding"); the grant is a route by which any element that is inconvenient *now* becomes an obligation due on an event **named by the party doing the moving**. Nothing requires the named event to be certain to occur, to be dated, or to be independently observable. An obligation due on an event that never arrives is discharged in form and waived in substance — the outcome both clauses open by forbidding. The rigor in the limb is all on the *scoring rule* being fixed at the move; none of it is on the *due event*.

---

### TIER 3 — needs an amendment, a construction, or a report the reader must not check

**E2-1.20 — SC-8(e): a registered route from a fail to a re-run.**

> **(e) A NUMBER FOUND WRONG AFTER A RESULT IS NOT CORRECTED IN PLACE.** … It is recorded, an amended registration is committed, and the affected benchmark is regenerated as a new version under §6.4 with the superseded results published alongside.

**What it permits.** The limb's target is in-place correction, and it is right about that. But it registers the alternative in operative terms: find a frozen number wrong → amend → **regenerate the benchmark**. "Found wrong" is not defined and requires no independent adjudicator; SC-4(i)'s *"Any disagreement between the rule-derived class and the frozen class is a **stop-and-report**"* halts the run but does not decide which side was wrong. The friction is publication of the superseded results alongside — real, but it is a disclosure obligation, not a bar. Cost: one class C amendment per attempt.

**E2-1.21 — SC-2(c): a four-item list of what disqualifies a pre/post pair reads as exhaustive.**

> the licence for that reading requires the two sides to differ **in availability and in nothing else**. **A change to the column set, the label set, the row population, or the evaluation population is not an availability change**, and a variant carrying one is not admissible as a side of this fixture.

**What it permits.** The first sentence is the rule and it is strict. The second enumerates four disqualifying differences and is the sentence an implementer will actually apply. A difference not in the four — the transform SC-1(b) contemplates, the horizon, the imputation, the sampling frequency, the model or seed — is not named, and on the enumeration's own reading is not disqualifying. The clause's structure invites reading limb two as the operative content of limb one.

**E2-1.22 — SC-1(f): a fully computed shadow gate, licensed and published.**

> Exactly one `ties` branch (§2.3) is declared, and it alone is scored. Figures computed under any other branch are published as **informational disclosures** so the tie choice is auditable: they enter no denominator, contribute to no rate, and **no gate outcome may be computed from them.**

**What it permits.** The prohibition is on *computing a gate outcome* from the non-declared branch. Computing every input to that outcome is not merely permitted, it is required ("are published"). The `ties` branch is the knob that flips boundary units between REQUIRED and OUT OF JURISDICTION under SC-4(b)'s two predicates, both of which read *"under the declared branch"*. So the set requires publication of exactly the information that tells you which branch you should have declared, and SC-8(e)/SC-9(d)/SC-9(e) supply routes to get there. Nothing in the set requires the branch choice to be justified, and SC-8(d)'s justification discipline reaches *"a class set, a cohort, a population"* — a tie convention is none of those.

**E2-1.23 — SC-3(e): reporting objects are unfrozen, unbounded, and quotable.**

> A re-aggregation, restriction, or re-projection of the map published for reporting is a **REPORTING OBJECT**: it is **not a second scoring key and changes no adjudication.**

**What it permits.** Because it changes no adjudication, a reporting object is not an object the gate consumes, so SC-8(a)'s freeze does not reach it and it is not in SC-8(f)'s hash set. It is derived from the map, so it is not "non-gated data" and SC-10(d)'s four forbidden uses — including *"(3) an unqualified headline over the scored population"* — do not reach it either. Result: arbitrarily many restricted views of the scoring key may be published, post-tag, revisable, and quoted as headline results, subject only to *"both are published with their delta explicit"*.

**E2-1.24 — SC-12(w7): the registered text pre-states the measurement's outcome.**

> **(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` detector-case entries, **per detector and per combination**, as a count. **That count is zero.**

**What it permits.** A report discharges (w7) by publishing the count the registered text has already asserted. This is the pattern SC-11 exists to stop — a zero that is stated rather than measured — appearing in the clause whose §8.3 hunk was added on the reasoning that *"a prohibition whose observance is never published is not checkable."* The §8.3 assertion (`waived` added to `assert_audit_complete()`'s failure set) does independent work and is the real guard; (w7)'s last sentence tells the report writer the answer in advance.

**E2-1.25 — SC-12 governed set pinned by reference, so amending §7.1 shrinks the floor without touching the floor.**

> **Which detectors the floor governs is not the declaration's to choose.** They are the detector rows §7.1's two runtime metric rows name … The declaration may not shorten the set

**What it permits.** The prohibition binds the *declaration*. The set is defined by reference to §7.1's rows, so a class C amendment to §7.1's metric table — an edit that on its face is about metrics, not about the floor — shrinks the governed set, and with it SC-13b's admissibility test and SC-13a(a2)'s per-detector threshold. The clause closes the declaration route and leaves the registration route open, unmarked, and not obviously a weakening of the floor to whoever reviews the §7.1 amendment.

**E2-1.26 — SC-7(a)/(b): the withheld set is defined by artifact identity, not by information content.**

SC-7(a):

> **(a) AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9). **Nothing else.**

SC-7(b):

> **the declared ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it.

**What it permits.** The map is withheld; the declaration's *declared elements* are handed over. But SC-4(a) requires the declaration to state, **per unit**, the class assigned and the facts on which it satisfies the predicate — and the REQUIRED list is, by SC-4(b), exactly the units the map declares violating. Whether that per-unit enumeration is a "declared element" (handed over) or a "summary … derived from" the map (withheld) is not settled by any applied text, and SC-7's DATA block hands the decision to the implementer: *"The enumerated declared elements handed to a detector."* SC-7(c) states the stake precisely — *"A run that received the key has not produced a gate result, whatever it reports"* — but the boundary that determines whether the key was received is drawn by artifact name rather than by information content, and one party enumerates.

---

### NOT ESTABLISHED

- Whether the drafters intended SC-4(e)'s "Two grounds are registered here" as a closed set. SC-1's apparatus asserts it; the applied text does not carry it (E2-1.01).
- Whether SC-8(a)'s tag-instant freeze or SC-6(b)/SC-3(h)/SC-8(c)'s pre-run freeze governs the declaration's composition. Both are applied text, they name different instants, and no applied limb orders them (E2-1.07).
- Whether the SC-4 per-unit class enumeration is inside or outside SC-7's input surface (E2-1.26).
- Whether any registered text bars exploratory (non-gate) runs against the acceptance fixture during the tuning phase PREREG line 480 licenses. I found none in the applied clause text; the ordering line freezes the *configuration*, not knowledge of fixture behaviour. This is the precondition that makes E2-1.01, 02, 06 and 09 targetable rather than blind, so its absence is load-bearing for the ranking above.

### ONE STRUCTURAL OBSERVATION

The strongest findings above share a form worth naming for the parent: **the clause states the abuse it fears in its own heading, then answers it with a sentence that has no operative content.** SC-3(h) "The unscored disposition is not an escape hatch." SC-4(d) "Two readings are registered as forbidden outright, because each silently removes units from the arithmetic" — and then registers a removal. SC-2(e)/SC-9(c) "never waived and never left outstanding" — and then registers a deferral to an event the mover names. SC-9(a) "IT CREATES NO GATE OBJECT" — followed by a five-item list that omits eleven gate-determinative objects the declaration does control. SC-12 item (2), which forecloses the one citation that would name any of it. A reader auditing this set by heading will find it airtight; the licences are all in the second half of limbs whose first half is a prohibition.

==============================================================================
# TASK E2-2 — DOES v30a WEAKEN ANY GATE OR KILL CRITERION?

**Scope read.** `SCHEMA_SET_FINAL.md` Part 1 in full (SC-1 … SC-13c, §13c-P, §AB, lines 89–1554), and `PREREG.md` §0–§0.2.1, §2, §4, §6.1–§6.2, §7.0–§7.10, §8, §10, §11, §12, §13.

**Scope limit, stated first.** SC-2, SC-3 and SC-12 perform their supersessions **through H1 hunks H2, H3, H4, H5, H6, H7, H8, C1, C2**, and those hunk texts are **not in this file** — SC-2's marker says only *"Their markers stand as H1 wrote them and are cited, not re-drafted."* So for `PREREG.md` §6.2 lines 445, 450, 451 and §10 line 992, the amended operative text is **NOT ESTABLISHED** from these two sources; F6 below is confined to what the SC-2 schema layer itself holds.

**Verdict.** Nine findings. Seven are weakenings of a gate or kill criterion; two are side effects that weaken on one available reading. The set's tightening work (SC-7, SC-8, SC-11, SC-12, SC-12(w), SC-13b(b3), SC-13a(a3)) is real and is recorded at the end as *not* weakening — but tightening elsewhere does not cure a weakening here, because `PREREG.md` line 97 is a per-clause test: *"An amendment weaker than the thing it amends is not one."*

---

## F1 — WEAKER. Criterion 3's absolute prohibition becomes conditional on declaration-supplied map coverage; findings on `unscored` cells carry no gate consequence. (SC-3(b), SC-6(a), SC-6(d))

**REGISTERED** — `PREREG.md` line 461, §6.2 criterion 3:

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

That criterion has one term and no exceptions: a finding, any tier, any cell, fails the gate.

**AMENDED** — SC-3(b), third disposition:

> - **A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none, enters no denominator, contributes to no rate, and is **never reported as a pass.**

and SC-6(d):

> **(d) FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored observations**, separately from the false-positive tally, and they carry no criterion consequence in either direction.

**The delta.** Under registered v30 a primary runtime finding on `fixture_corrected` fails the gate. Under v30a the same finding, landing on a cell or unit the declaration entered in its unscored ledger before the run, **"forbids none"** and carries **"no criterion consequence in either direction"** — the gate does not fail. A population is exempted, and the exemption is populated by the declaration, not by the registration.

SC-3(h) is written to deny this and does not reach it:

> **(h) THE AMENDMENT DOES NOT LOWER THE BAR.** A finding on a cell the map marks **zero** is still a false positive and still fails the gate. The unscored disposition is not an escape hatch.

(h) covers cells the map **marks zero**. It says nothing about cells the map **does not cover** — which is precisely the population (b) and SC-6(d) release. The two sentences dispose of two different sets, and only the first is defended.

The same exemption reaches **criterion 2** (line 460, *"No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`"*) by the identical route: SC-6(d)'s "no criterion consequence in either direction" is not limited to criterion 3.

Ex-ante freezing (SC-3(h), SC-6(b), SC-8) constrains *when* the exemption is fixed. It does not restore the registered criterion, which admitted no per-cell scored/unscored flag at all — SC-3(a) newly requires one: *"including the field that records whether the cell is scored."*

---

## F2 — WEAKER. Criterion 1's denominator moves from the manifest's ground truth to a declaration-derived class, and the manifest classification is expressly barred from entering it. (SC-4(a), (b), (e), (g))

**REGISTERED** — line 459 (criterion 1) read with line 446:

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW.

> - **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.

"Every … ground-truth leaking source column" is closure over a manifest-fixed list.

**AMENDED** — SC-4(a):

> **No classification of the scored set other than this derivation enters any criterion, denominator, or count**, and no split within such a classification carries gate arithmetic.

SC-4's own marker concedes the effect on line 446:

> **§6.2 line 446 — NOT AMENDED.** The manifest requirement stands; only the *arithmetic role* of what it records is constrained, which is a statement about denominators, not an edit to line 446.

**The delta, three routes.**

1. **Substitution.** The denominator becomes SC-4(b)'s **REQUIRED** class — *"the map declares a violation on it, on the scored side, under the declared branch"* — with *"**N is the length of the REQUIRED list**, and no other quantity is N."* The registered denominator (the manifest's leaking-source list) is not merely superseded; SC-4(a) forbids it from entering *"any criterion, denominator, or count."*

2. **Two registered exclusion grounds** — SC-4(e):

> a **degenerate unit that cannot carry a finding of the scored class at all** … and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot be scored under any reading).

   The second is declaration-triggered: a manifest-listed leaking source leaves criterion 1 by being **declared** UNRESOLVED. Registered criterion 1's word "Every" admitted no such route. SC-4(e)'s guard runs the other way — *"**Reinstating** an excluded unit changes the denominator and is class C"* — it prices re-entry, not exit.

3. **The un-fed unit, which needs no ground at all** — SC-4(g):

> a unit the declaration does not feed to the scored pipeline holds **no gate class whatever** — declaring it out of jurisdiction would imply the gate adjudicates it and declines.

   SC-4(b)'s partition is *"MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE **DECLARED SCORED SET**"*, and SC-4(f)(3)'s printed check reconciles the three classes to *"the size of the declared scored set"* — not to the manifest. **Nothing in the set requires the declared scored set to contain every manifest-listed ground-truth leaking source.** A unit not fed is outside all three classes, outside the partition check, and outside criterion 1, with no unscored-ledger entry and no class C event.

SC-4(j) (*"identified by the named constant the declaration declares, never by its cardinality"*) protects against a set being swapped for a same-sized one. It does not require the set to be the manifest's.

---

## F3 — WEAKER. Criterion 2's scope is restated as a declaration-supplied population while criterion 2 is declared byte-exact. (SC-5(c) against line 460)

**REGISTERED** — line 460:

> 2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.

**AMENDED** — SC-5(c), whose own marker says *"None — pure insertion. §6.2 criteria 1, 2 and 4 stand byte-exact"*:

> **It is not converted into a failure of the clean-source criterion**, which has no landing site for such a unit; that criterion's scope is **the units the declaration declares clean**, and those units **do** route to it.

**The delta.** Line 460 says the scope is **manifest-clean** columns. SC-5(c) says the scope is **the units the declaration declares clean**. Two normative statements of one criterion's scope, in one file, differing on the authority that fixes it — the shape §0.2.1 line 77 registers as *"a protocol failure, not a redundancy."* The substitution is a weakening in itself (a manifest-fixed population replaced by a declaration-supplied one), and it is compounded twice:

- SC-4(a) independently bars the manifest classification from *"any criterion"*, so the registered scope has no remaining source;
- nothing in the set obliges the declaration to declare **any** unit clean, and SC-3(g) pushes the opposite way: *"A side the declaration characterizes is **CHARACTERIZED, never clean**, and no report describes it as clean."* A criterion whose scope can be declared empty cannot fail.

SC-5(c)'s closing sentence — *"**The false-positive consequence is never carried beyond the out-of-jurisdiction class.**"* — is a further removal: registered criterion 2 attaches its consequence to the column's manifest status, not to a derived gate class.

---

## F4 — WEAKER. A declared jurisdictional routing statement exempts a runtime finding from §6.2's criteria, and SC-13c(c6) confirms the exemption reaches the acceptance gate. (SC-5(e), SC-13c(c6))

**REGISTERED** — lines 460 and 461 test **who produced the finding** ("any runtime finding of any tier, primary or secondary"), not what its character is.

**AMENDED** — SC-5(e):

> Where a finding's character belongs to a detector row **outside** the criteria this gate scores, the declaration assigns it to that row and it is **neither credited nor penalized here.**

**AMENDED** — SC-13c(c6), which guards SC-13a and, in the same breath, concedes §6.2:

> a declaration statement that assigns a finding's character to a detector row and places it **outside an acceptance gate** does not place it outside **this** criterion … **A jurisdictional routing statement written about the acceptance gate reaches the acceptance gate and stops there.**

**The delta.** SC-13c(c6) is explicit that the routing statement **does reach the acceptance gate**; only the §10.2 kill criterion is fenced off from it. So a runtime finding on `fixture_corrected` — which line 461 fails the gate on unconditionally — can be moved out of criteria 2 and 3 by a declared character assignment. That is a criterion made satisfiable by a route the registered text did not admit. SC-5(e)'s ex-ante requirement (*"declared before any detector runs; it may not be made after seeing where the findings landed"*) constrains timing only.

SC-13c(c6) closes this hole for SC-13a — *"Removing a detector from this criterion is a waiver, and the floor forbids it"* — and leaves it open for §6.2. The asymmetry is stated, not accidental.

---

## F5 — SIDE EFFECT, WEAKER ON ONE READING. `unscored`, registered as a §7.7 **detector-case** coverage state, carries an unqualified "enters no denominator" that reaches §10.2 criterion 3's N and its 60% completion floor. (SC-6(a) against lines 875, 1037, 1038)

**Where SC-6 lands.** SC-6's first insertion point is *"`PREREG.md` line 855, the §7.7 coverage-state table row"* — the **Detector-case coverage** row.

**SC-6(a), unqualified:**

> An `unscored` unit **requires no finding and forbids none.** It **enters no denominator**, **contributes to no rate**, and **cannot be reported as a pass.**

**REGISTERED, in the same section** — line 875:

> **Metric-denominator membership is defined directly on the state, not by exclusion:** a case enters a combination's metric denominators when its **`schedule_state` ∈ {`completed`, `incomplete`}**. `not_applicable`, `unsupported`, and `short_circuited` are outside every one of them…

**REGISTERED** — line 1037 defines the kill gate's denominator on the same axis: *"with **N** = clean cases whose `schedule_state` ∈ {`completed`, `incomplete`}"*.

**REGISTERED** — line 1038, stating the purpose that is at risk:

> The two gates close a gaming pair — the finding-rate denominator admits cases that crashed before executing, which a detector could hide behind by **failing on hard clean cases**, and the completion floor is what stops that.

**The delta.** Read narrowly, §7.7 line 875 and §7.2.1 line 820 (*"**No runtime metric reads the detector-case state of §7.7**"*) hold N immune and SC-6 is inert here. Read as written, SC-6(a) is a general sentence about `unscored` entering **no** denominator, placed in §7.7 beside line 875 — and §7.7 then carries two rules on denominator membership that disagree for the new state. On that reading, hard clean cases declared `unscored` ex ante leave N; the completion fraction over the surviving N rises; the 60% floor stops catching the behaviour line 1038 names. The finding-rate gate can flip with it — at N = 6, k = 2 the gate fails (`floor(0.20 × 6) + 1 = 2`); remove one finding-bearing case and N = 5, k = 1 passes (`floor(1.0) + 1 = 2`).

SC-6(c) compounds the ambiguity rather than resolving it: it registers the state at *"the **cell** level of the declared map (SC-3) and at the **unit** level of the declared partition (SC-4)"* — two levels — while the insertion places it in the table for a third, the detector-case. **Which denominators SC-6(a) removes an entry from is therefore not established by the clause text**, and one of the available readings weakens a kill criterion.

---

## F6 — WEAKER as to threshold. The registered acceptance interval is retired and replaced by a declaration-supplied "declared tolerance" with no registered floor. (SC-2(d) and the retirement of §6.2 line 445)

**REGISTERED** — line 445, and line 992 (Phase 1 gate cell):

> - **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

> … both fixture AUCs reproduce within ±0.010, full and sliced …

**SC-2's marker:**

> **§6.2 line 445 — SUPERSEDED BY v30a** (H1 hunk **H2**): the registered anchor pair and its transcription are retired; SC-2(d) registers the anchor's *form*, H2 retires the *figures*.
> **§10 line 992 — CONSEQUENTIAL** (H1 **C1**): the Phase 1 gate cell reads on both retired objects.

**AMENDED** — SC-2(d):

> that quantity is **recomputed from the fixture's own committed bytes** and declared as an **enumerated set of entries** … **The declared tolerance applies per entry and may not be widened.**

**The delta.** Registered v30 fixes the tolerance as a literal inside the tagged registration: **±0.010 absolute**. v30a replaces it with *"the **declared** tolerance"* and constrains only that it *"may not be widened"* — widened, that is, from whatever the declaration declares. **No clause in the set binds the declared tolerance to ±0.010, or to any registered value.** A threshold has moved from registered text to declared data, and a phase-gate cell (line 992) now reads on it.

SC-2(d) does add a genuinely stricter limb — *"a deviation approaching the tolerance is a **stop-and-report**, not a pass"* — but "approaching" scales with whatever tolerance is declared, so it does not restore the registered floor.

**NOT ESTABLISHED:** whether H2 or C1 carries a floor tying the declared tolerance to ±0.010. Those hunk texts are not in `SCHEMA_SET_FINAL.md`.

---

## F7 — WEAKER by side effect. The replacement kill criterion contains no separation test; separation survives only through a limb pinned to the criterion F1 weakens. (SC-13a, SC-13c(c5)(i))

**REGISTERED** — line 1030, the criterion being replaced:

> 2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**

The registered criterion's entire content is a **comparison between the two sides**.

**AMENDED** — SC-13a(a2):

> For **each** runtime detector the floor governs …, on **each** declared side, the `preserving` combination's proof yield must be **strictly greater than zero** — `proof yield > 0`. … **This limb is unconditional on every declared side, including the side the fixture declares corrected.**

**The delta.** SC-13a(a1)–(a3) states two independent per-side thresholds and **nowhere compares one side to the other**. A detector behaving identically on `fixture_contaminated` and `fixture_corrected` — i.e. separating nothing — satisfies `proof yield > 0` on each side and does not trip the stop. Registered line 1030 stops on exactly that state.

SC-13c(c5) is where the separation property is supposed to be recovered, by carrying line 1035's third limb — *"criterion 3's gates in force"* — and it names the version:

> **(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION** … **It is never the pre-amendment prohibition on any finding on the corrected fixture**, and this clause may not be read against that text.

So the only thing standing between the replacement criterion and a non-separating detector is criterion 3 **as amended** — the criterion F1 shows carries the UNSCORED exemption. The chain that preserves separation runs through the one criterion the amendment weakened, and (c5)(i) forbids reading it against the registered text that did not.

SC-13c(c1) states the dependency without denying the polarity change: *"under registered line 461 unamended, SC-13a(a2)'s corrected-side requirement is **dischargeable only by failing §6.2 criterion 3**."* Registered criterion 3 forbids every finding on the corrected side; SC-13a(a2) **requires** proven findings there. That is a full inversion of one registered criterion's polarity on the ambiguity branch, achieved by amending the criterion it inverts.

SC-13c(c7) then states the outcome for a state line 1030 would have stopped on:

> A detector that probes few cohorts, proves what it probes, and publishes its coverage honestly **passes this criterion and is supposed to** … **Partial capability honestly reported is the designed outcome of this programme and is never by itself a kill condition.**

Line 1035's first limb ("non-zero proof yield") does license a `> 0` threshold. It does not license the disappearance of the comparison, which is line 1030's whole subject.

---

## F8 — WEAKER. A recording obligation is made curable after the fact. (SC-9(d) against `PREREG.md` line 22)

**REGISTERED** — line 22:

> Changes are allowed. They go in `DEVIATIONS.md`, append-only, with a date and a reason. **An unrecorded change is a protocol failure, not a change of plan.**

**AMENDED** — SC-9(d):

> A working resolution binds by its content and its date, **not by where it was recorded**: a resolution issued in the course of the work binds exactly as one written into the record does, and **the record is completed to contain it.**

**The delta.** Registered v30 makes non-recording a **protocol failure**. SC-9(d) makes an unrecorded resolution **binding**, and makes the record's gap **curable by later completion**. "Its date" then becomes an asserted property of an instrument that was not contemporaneously recorded — which is the property every ex-ante rule in this registration depends on being evidenced: line 480 (*"Defaults may not be altered after observing a fixture result"*), line 1031 (*"the replacement is written before any development-corpus contact, not after tuning"*), SC-8(c) (*"EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS"*), SC-3(h) (*"a map frozen after a run is a key shaped by the result"*).

SC-9(e)'s stronger-reading-only rule and SC-12 item (5) block a working resolution from *weakening* a locked obligation. Neither restores line 22's holding that failure to record is itself a failure rather than a gap to be filled.

---

## F9 — LOW CONFIDENCE. The one marker attached to line 97 recites what survives and omits the non-weakening sentence. (SC-8's §0.2.1 marker)

**REGISTERED** — line 97, two sentences:

> **An amendment inherits §11's integrity chain in full:** signed tag, both file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock. **An amendment weaker than the thing it amends is not one.**

**AMENDED** — SC-8's marker, placed after line 97 per §0.2's application order:

> **§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT.** "both file hashes in the tag message" records the count at the time of writing; it is superseded as a count by §11 item 8 … **The requirement — that an amendment inherit §11's integrity chain in full — stands byte-exact.**

**The delta.** The marker declares line 97 partially superseded and then enumerates, by name, what stands: the integrity-chain requirement. The second sentence — the rule against which this entire amendment is measured, and the rule this task applies — is not named as standing. The marker's substance is narrow and correct; the risk is in its form, since it is the only marker at that line and it recites survival selectively. **NOT ESTABLISHED** whether any other clause re-recites line 97's second sentence as operative; I found none in Part 1.

---

## CHECKED AND FOUND STRICTER OR EQUAL — recorded so the absence of a finding is not read as an omission

- **SC-1(a)–(e)** — measured over documented, representation named, role never scored against, unit change is class C, staleness licenses no finding. All add obligations; none removes one.
- **SC-2(a)–(c), (e)** — fixture enumerated, composition change class C, pre/post licence bounded, phase moves amended not waived. Stricter.
- **SC-3(a), (c)–(g)** — map schema declared, whole declared population covered, no subclass excluded "by description", one scoring key, subsets inherit cells, neither side assumed clean. Stricter within the declared population; the weakening is at the boundary of that population (F1, F2).
- **SC-4(c), (d), (f), (h)–(j)** — precedence registered, two readings forbidden outright, lists not counts, printed partition check, re-derivation mandatory, set named not counted. Stricter.
- **SC-5(a), (b), (d), (f)** — one criterion per finding, attribution to the ground not the name (*"Naming the right unit on the wrong ground satisfies nothing"*), double charging where independent, sentinels enumerated ex ante. Stricter.
- **SC-7** — pure insertion; the registered text stated no input surface at all. Note two side effects, both **restrictive**: SC-7(a)'s *"**Nothing else**"* lists only *"the availability declaration's **declared elements** (§2.3, §2.4, §2.9)"*, which excludes §2.5's `labels_available_during_feature_construction` (line 231: *"a declaration in its own right, not a field of `AvailabilityModel`"*) and the frozen default configuration line 457 requires the gate to run under. Both push toward `unsupported` / gate failure, not toward a pass.
- **SC-8(a)–(f)** — freeze at tag, lists not counts, ex-ante checkability, scope justified independently of its effect on any number, no in-place correction, declaration itself hashed. Stricter throughout; item 8's *"The set is that enumeration and its count is read from it"* is closed against circularity by *"A registered file absent from the enumeration is a defect in the tag, not a file outside the chain."*
- **SC-9(a)–(c), (e), (f)** — declaration creates no gate object, evidence never adjusted toward a decision, obligations met or amended, interpretation only toward the stronger reading, cite don't restate. Stricter.
- **SC-10** — non-gated data exempt from the freeze *only* while exempt from the arithmetic, backstopped by SC-8(a)'s *"an object the gate consumes and the enumeration omits is a defect in the enumeration, not an object outside the freeze."* Equal.
- **SC-11(a)–(g)** — every empty aggregate proved empty before it may be reported, mismatch raises rather than warns, unexpected zero is a finding. Stricter.
- **SC-12 and SC-12(w)** — the floor becomes a prohibition with no invocation procedure (*"There is no procedure by which a detector the floor governs may be waived"*); the governed set is pinned to registered sites and is not the declaration's to shorten; §7.7's `waived` gets an entry condition whose licensed-grounds enumeration is closed and empty; `waived` is added to `assert_audit_complete()`'s failure set at line 929 so the prohibition is machine-checkable. Stricter throughout, and the governed set `{L2a, L3.1}` matches line 1035's *"neither runtime detector waived"* exactly.
- **SC-13a(a3)** — denominator cited unnarrowed, with *"A declaration may not use the enumeration to remove from the denominator a pair the corpus labels and the risk logically applies to."* Stricter. (Note the unresolved collision with SC-6(a)'s *"enters no denominator"* for `unscored` pairs; SC-13b(b4)(iii) disposes the total case as a STOP, so the collision does not open an escape at the `> 0` threshold.)
- **SC-13b(b1)–(b4)** — empty labelled-unit set is a STOP; empty per-side cell is the same STOP; the `not_applicable`-everywhere state is executed, published, and stopped through the threshold rather than suppressed. Stricter than registered line 816, and argued as such.
- **SC-13c(c2)–(c5)** — the line-816 exception runs toward publication and toward the gate firing, not away from it; every referent of "criterion 3's gates" held in force.
- **SC-3's marker on §10.1 line 1022** — the marker states the kill gate *"must be amended with this clause or `PREREG.md` holds both readings at once"*, and no clause in the set amends it. The effect is that §10.1 criterion 3 keeps *"is silent on `fixture_corrected`"* — the **stricter** reading, applied to a third-party tool. Not a weakening.

---

## ONE COLLISION THAT IS NOT A WEAKENING BUT IS A SEMANTIC OVERRIDE WITHOUT A MARKER

**SC-13c(c4)** requires a rate to be published from the acceptance fixture:

> the other combination is **executed to a terminal result on the same denominator and publishes its own registered yield**, per detector and per side … **Its published yield is a required output of the criterion**

Read with SC-13a(a1)–(a2), which compute **proof yield** — a rate (§7.2: *"correct PROVEN pairs ÷ **all scope-eligible labelled pairs**"*) — on the fixture.

**REGISTERED** — §6.1 line 441:

> **No accuracy or generalization rate is published from the fixture.** The descriptive proof count of §6.2 is the sole reported fixture outcome; it is a count, receives no inferential interval, and is not a rate.

**REGISTERED** — §7.0 constitution rule 7:

> Intervals follow §7.10; the fixture, conformance suite, and wild corpus **publish no rates** (§6.1).

SC-13c(c6) addresses only the §6.2 proof **count** — *"The descriptive fixture proof count of §6.2 remains descriptive and non-gating **for §6.2**"* — and never reaches §6.1's prohibition or rule 7. The direction is not a weakening of a gate; it is a registered publication prohibition overridden by a new obligation, with no supersession marker in the set naming line 441 or rule 7. Flagged here because rule 7 is a **constitution** rule, locked and *"binding on every future module."*

==============================================================================
Both files read in full (SCHEMA_SET_FINAL.md 2,268 lines; PREREG.md 1,099 lines; AVAILABILITY_DECLARATION.md 3,796 lines as it stands in the working tree — note it is 112 lines longer than the 3,684 the schema file records, and §A.6.0 already carries the Part 2.3 "DERIVATION, BY CITATION" text, so the K4 scrub has partly landed).

---

# PART 1 — RESTATEMENT: RULES WITH TWO NORMATIVE COPIES

## R1 (most serious). SC-9(e) and `AVAILABILITY_DECLARATION.md` §D.3 are the same rule, word for word, and they have already drifted

**Copy 1 — SC-9(e), applied clause text** (`SCHEMA_SET_FINAL.md` line 794):

> **(e) THE INTERPRETATION RULE — resolution toward the stronger reading only.** **An interpretation of locked text may resolve ONLY toward the STRONGER reading. Any interpretation that weakens a locked obligation — narrows a denominator, exempts a unit, softens a criterion, admits an excluded set, converts a required finding into an optional one, or converts an unscored cell into a pass — is a class C amendment and may not be recorded as a working resolution, a decision-log entry, or a reading.**

**Copy 2 — `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` §D.3, lines 3591–3595:**

> **A decision-log interpretation of locked text may resolve ONLY toward the STRONGER reading. Any interpretation that weakens a locked obligation — narrows a denominator, exempts a column, softens a criterion, admits an excluded set, converts a required finding into an optional one, or converts an unscored cell into a pass — is a class C amendment and may not be recorded as a working resolution.**

Identical but for `exempts a **unit**` / `exempts a **column**` and SC-9(e)'s added tail. §D.3 does not cite SC-9(e); it presents the rule as its own ("Stated as a rule so that the next entry cannot do the opposite by precedent," line 3598).

Three things make this the defect rather than an oversight:

1. The limb immediately beneath it forbids exactly this. SC-9(f) (line 802): "**A RULE STATED TWICE HAS NO CANONICAL SOURCE.** *(Citation: §0.2.1 line 77.)* Where a declaration needs one of these rules, it **cites this section and does not restate it.** A second normative copy in a declaration is the duplicated-authority failure, not a redundancy."
2. The amendment then *cites the offending copy as support*. §AB (line 1549): "…no reading, working resolution, or `DEVIATIONS.md` entry may resolve the conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); **corroborated by the declaration's §D.3** and §A.12 item 5)."
3. The drift is already present. "unit" vs "column" is the `PREREG.md` line 70/73 shape — "two copies, drifted" — on the object (`unit` vs `column`) that SC-4 spends nine limbs partitioning.

## R2. SC-7 and `AVAILABILITY_DECLARATION.md` §E are the same rule, near-verbatim, in three limbs

`AVAILABILITY_DECLARATION.md` §E begins at line 3602 ("Gate protocol input surface — what a detector receives, and what it never receives") and cites SC-7 nowhere.

| | SC-7 (`SCHEMA_SET_FINAL.md`) | §E (declaration) |
|---|---|---|
| (a) | "**AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9). **Nothing else.**" (line 624) | "**At gate time a detector receives exactly two things, for ONE SIDE AT A TIME:** 1. **the feature pipeline** for that side, and 2. **the availability declaration** … **Nothing else.**" (3604–3612) |
| (c) | "**WHY THE MAP IN PARTICULAR IS WITHHELD.** Under criterion 3 the map **is** the scoring key. A detector that could read it would be graded against a key it had seen, and the run would measure **retrieval rather than discrimination**. The map is an artifact of the harness, not an input to the tool." (line 632) | "**Why the map in particular must be withheld.** Under the amended criterion 3 the map IS the scoring key. A detector that could read it would be graded against a key it had seen, and the gate would measure retrieval rather than discrimination. The map is an artifact of the harness, not an input to the tool." (3622–3626) |
| (d) | "**ONE SIDE AT A TIME IS A HARD SEQUENCING RULE, NOT A CONVENTION.** The criteria are per-side, and each is evaluated from a run that saw only its own side. **A single run given more than one side satisfies none of the criteria, however its outputs are partitioned afterwards.**" (line 637) | "**Corollary — one side at a time is a hard sequencing rule, not a convention.** … each is evaluated from a run that saw only its own side. A single run given both sides does not satisfy any of them, however its outputs are partitioned afterwards." (3628–3633) |

SC-7's own DATA block asks the declaration for **data**, not the rule: "The enumerated declared elements handed to a detector; the enumerated artifacts withheld; the run order across sides." §E supplies the enumerations *and* restates the rule around them. Drift is already visible: SC-7(b) withholds "any summary, cohort list, **restriction**, or per-cell count derived from it"; §E withholds "any summary, cohort list, or per-cell count." One word of scope, two copies, no canonical source.

## R3. SC-2 and SC-9(c) state one rule twice, inside the amendment, neither citing the other

**SC-2(e)** (line 244): "A registered element that cannot be satisfied at the instant the amendment must be committed is **amended explicitly — never waived and never left outstanding.**"

**SC-9(c)** (line 780): "**An element that cannot be met as written at the instant an amendment must be committed is amended explicitly — never waived and never left outstanding**, because an outstanding element invites being re-read as satisfied later."

The same pair also duplicates the discharge prohibition:

**SC-2(b)** (line 222): "It may not be done by a `DEVIATIONS.md` entry, by an orchestrator decision, or by a working resolution."
**SC-9(c)** (line 780): "It may not be discharged by a `DEVIATIONS.md` entry, by a working resolution, by an orchestrator decision, or by being carried forward silently."

SC-9 is the clause the set treats as the home of integrity rules ("REGISTERS. R25's third disposition… what makes a declared instance honest"). SC-2(e) is the second copy and cites nothing.

## R4. The entry condition for `unscored` / UNSCORED is registered in three places, two of which each claim to be the registration

- **SC-4(b) table row** (line 389): "| **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |" — with **SC-4(a)** asserting authority over it: "the class predicates of (b), under the precedence of (c) — and is not the declaration's to state, restate, or rewrite."
- **SC-6(a)** (line 564): "A unit is **`unscored`** when the declaration declares, **before any detector runs**, that scoring it is impossible on a stated ground."
- **SC-6(b)** (line 570), also asserting authority: "A unit may be reported `unscored` **only if it appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector runs.**"

The copies are not identical, which is the point: SC-4(b)'s registered predicate omits the by-name ledger and the freeze that SC-6(b) makes constitutive. A unit satisfying the SC-4(b) row need not satisfy SC-6(b), and SC-4(a) forbids anyone from repairing the row by reading SC-6 into it.

The gate consequences are then stated twice as well:

**SC-3(b)** (line 300): "**A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none, enters no denominator, contributes to no rate, and is **never reported as a pass.**"
**SC-6(a)** (line 564): "An `unscored` unit **requires no finding and forbids none.** It **enters no denominator**, **contributes to no rate**, and **cannot be reported as a pass.**"

SC-3(b) cites `(SC-6)` and then restates SC-6 in full in the same bullet — a citation and a second copy in one sentence. That this sentence shape is a *rule* statement, not prose, is settled by the project's own checker, which fires on it: `AVAILABILITY_DECLARATION.md:1239: denominator membership stated outside PREREG.md … 'Requires no finding and forbids none; enters no denominator, contributes to no rate, and'` (SCHEMA_SET_FINAL.md line 1835).

## R5. SC-12's governed-set paragraph and SC-13c(c3) are the same rule twice — and only one of them is ever cited

**SC-12** (line 979): "**Which detectors the floor governs is not the declaration's to choose.** They are the detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule gates — `PREREG.md` line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row, and line 1039's 'both of L2a/L3.1's combinations' — the same registered set SC-13c(c3) pins."

**SC-13c(c3)** (line 1385): "**WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows (lines 759 and 760), and line 1039's 'both of L2a/L3.1's combinations'."

The file discloses this ("SC-12 and SC-13c(c3) pin the same set to the same registered sites and never diverge on it"; Part 6 item 2(g) "deliberate, P7-accepted"), but disclosure is not a canonical source. Every clause that *consumes* the set names only one copy — SC-13a(a2) "the set SC-13c(c3) pins", SC-13b(b1) "the governed set is pinned at SC-13c(c3)", SC-13b's DATA "SC-13c(c3) pins that" — so SC-12's copy is a normative statement with no citer, and it is the copy that carries an extra sentence the other does not (see the conflict below).

**Conflict inside the duplication.** SC-12's copy licenses declaration restatement; SC-9(f) and SC-10(e) forbid it.

SC-12 (line 983, applied text): "**Where the fixture's declaration states the same membership, it is corroboration, not the source.**"
SC-9(f) (line 802): "**A second normative copy in a declaration is the duplicated-authority failure, not a redundancy.**"
SC-10(e) (line 862): "**ONE COPY.** These rules are stated here and cited elsewhere. A declaration restating them for a particular side has created a second normative copy (§0.2.1 line 77) and must cite instead."

The declaration has taken up SC-12's licence: `AVAILABILITY_DECLARATION.md` §A.12 item 1 (line 1642) — "This file's statement that the two runtime detectors are L2a and L3.1 (PREREG.md lines 318, 320) is **corroboration** of that registered set, not its source." Under SC-9(f) that sentence is the failure; under SC-12 it is permitted. The registration would hold both readings.

Also carried forward as disclosed but unresolved drift (SC-12 *Instance record*, line 1103): SC-12 limb (iii) reads "**another** detector's output alone" where §A.12 reads "**the other** detector's output alone."

## R6. SC-8(e) restates `PREREG.md` line 99 while labelling itself a citation

**SC-8(e)** (line 728): "**(e) A NUMBER FOUND WRONG AFTER A RESULT IS NOT CORRECTED IN PLACE.** *(Citation, not restatement: §0.2.1 line 99 governs.)* It is recorded, an amended registration is committed, and the affected benchmark is regenerated as a new version under §6.4 with the superseded results published alongside."

**`PREREG.md` line 99:** "It is recorded, the amended registration is committed, and **the affected benchmark is regenerated as a new version under §6.4** — new snapshot version, new beacon draw, new single-use run — with the superseded results published alongside, exactly as §6.4's re-draw rule requires."

The parenthetical asserts the thing the sentence after it disproves: every operative word is line 99's, with "the amended registration" changed to "an amended registration". A clause that announces "Citation, not restatement" and then restates is worse than an unmarked copy, because the marking is what a later reader will rely on.

## R7. SC-6(e) restates `PREREG.md` line 915's closing sentence, where the drafted §8.2 insertion is careful not to

**SC-6(e)** (line 587): "`unscored` entries are named as unscored, never as clean, and §8.2's rule governs their display: **none may be displayed in a way mistakable for a pass.**"
**`PREREG.md` line 915 (registered, §8.2):** "None may be displayed in a way mistakable for a pass."

The same pass's S2(i) text (line 551) shows the discipline the set intends and SC-6(e) does not meet: "its entry condition and semantics are SC-6's, **not restated here**."

## R8. The no-restatement rule itself is stated four times

SC-4(a) (line 375), SC-9(f) (802), SC-10(e) (862), SC-13a(a3) (1195). Each cites `§0.2.1 line 77`, which is the correct canonical source — but SC-9(f) and SC-10(e) are not scoped applications of it; they are two general statements of one generalized rule ("Where a declaration needs one of these rules…" / "These rules are stated here and cited elsewhere"), each written as though it were the only one.

## R9. SC-13a restates SC-7's withholding rule without citing SC-7

SC-13a (line 1157): "…on the frozen default configuration, **with the declaration's scoring key withheld from every detector**." That is SC-7(b)/(c)'s rule, and SC-7 is nowhere cited in SC-13a, SC-13b or SC-13c.

---

# PART 2 — MISREAD CITATIONS

Ordered by how load-bearing the misread is.

## M1. SC-1(c) cites §2.3 for a proposition §2.3 contradicts

**The clause** (line 161): "**(c) A ROLE IS A POSITION, NOT AN AVAILABILITY INSTANT.** A `column_roles` value (§2.3) names where a value sits on a lattice. The instant the comparator reads is the availability instant the declaration declares for that column."

**`PREREG.md` §2.3, line 205 — the cited registration of `column_roles`:**

> | `column_roles` | **per-column rule**: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column | all |

§2.3 registers `column_roles` as the per-column **rule from which `a(j,c)` is derived** — `at_bar_close` *is* an availability instant, and §2.2 line 182 states "Availability is decided by the comparator of §2.3." The cited row does not hold that a role is a position rather than an availability instant; it holds the opposite. SC-1(c) then makes a scoring consequence turn on the distinction — "**that role is never scored against**" — so the misread is operative, not decorative.

## M2. SC-1(c) and SC-4(d)(i) rest on "lattice", a term with no registered meaning

`lattice` occurs **0 times in `PREREG.md`** and **105 times in `AVAILABILITY_DECLARATION.md`** (measured this pass), where it is this fixture's instance vocabulary — "the 1-second snapshot lattice" (declaration line 137), "the lattice is anchored to the day's FIRST EVENT" (line 195).

Two applied clauses put normative weight on it:

- SC-1(c): "names where a value sits on a **lattice**."
- SC-4(d)(i) (line 404): "a locality condition may not be read more narrowly than **the declared lattice**, so a read of the same source at another instant of the same lattice does not by itself create a cross-source violation."

SC-4(d) registers this as one of "**Two readings … registered as forbidden outright**". A forbidden-reading rule whose operative term is defined only in the companion document inverts §0.2.1 line 77 — the registration would depend on the declaration for the meaning of a registered prohibition — and it fails the set's own R24 test (Part 3, line 2085: "would read identically in a registration that had never seen this fixture"), which the pass applied to the three S2 texts but not to SC-1(c) or SC-4(d).

## M3. SC-12(w)'s founding premise is false on the registered text

**The justification** (line 1017): "§7.7's table carries `waived` as a detector-case coverage state and registers no condition under which a report may assign it. **It is the only state in that table without one**, and the omission is not cosmetic".

Measured: `` `passed` ``, `` `failed` `` and `` `waived` `` each occur **exactly once in `PREREG.md`**, all three at line 855, the §7.7 table row. No registered text assigns `passed` or `failed` either. §7.7's completion lock (lines 860–868) defines "**complete**", "terminal", and `could_not_run(reason)`; it never names `passed` or `failed`.

This propagates into (w2) (line 1023): "§7.7's completion lock selects it where a terminal result is or is not reached; §8.2 draws the boundary between the not-run states and governs their display; SC-6(b) governs a unit the declaration declared unscoreable… **Those rules dispose of every detector-case between them, and the residue this state would have carried is empty.**"

The residue is not established as empty, because the two states the argument needs the completion lock to select — `passed` and `failed` — are the two states the completion lock does not name. (w1)'s prohibition may still be right; the ground offered for it is not.

Related: the S2(i) insertion text (line 551) makes §8.2's closing sentence range over "every detector-case coverage state that row carries **other than `passed` and `failed`**", i.e. it treats those two as the pass-bearing states — an operative reading of two tokens that appear nowhere else in the registration.

## M4. SC-13a(a1) attributes the scoring unit to the wrong section

**The clause** (line 1164): "**(a1) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime scoring unit".

**`PREREG.md` §7.2 (lines 774–781)** registers two units, and neither is the bare pair:

> **Two units, because scoring and display need different ones.**
> | **EvidenceEvent** | `(detector, promotion_status, feature, affected output cohort)` **within a case** … | every combination-specific metric in §7.1 |
> | **ReportedFinding** | `(detector, feature, affected output cohort)` | user-facing display |

The unit SC-13a(a1) means — "feature × affected output cohort" — is registered at **§2.6 line 208** ("the scoring unit is **feature × affected output cohort**, deduplicated across probes, strategies, and runs (§7.2)"); in §7.2 the pair appears as the *denominator* of proof yield ("all scope-eligible labelled pairs", line 791), not as the scoring unit.

This is load-bearing because (a1) is the limb discharging line 1033's "unit" obligation, and because the next sentence — "*'Per detector, per side' partitions the computation; it does not redefine the unit*" — is in tension with the section actually cited: §7.2's scoring unit already carries `detector` and `promotion_status` **in its key**, so per-detector is not a partition over that unit at all.

## M5. SC-13b(b2) quotes a precision rule as a general §7.2.1 rule

**The clause** (line 1268): "…disposing it instead as a scored zero would put a defined value on an empty denominator, which **§7.2.1's own registered rule** refuses: '**Undefined, not 0% or 100%, at an empty denominator.**'"

**`PREREG.md` lines 806–810** — the sentence sits inside one blockquote, defining one metric:

> Per `(detector, promotion_status)`:
> > **feature-cohort precision** = correct primary EvidenceEvents ÷ (correct primary EvidenceEvents + false primary EvidenceEvents).
> >
> > Secondary EvidenceEvents (§7.6) are excluded from **both** terms. … **Undefined, not 0% or 100%, at an empty denominator.**

The registered sentence governs **feature-cohort precision**. SC-13b(b2) applies it to **proof yield**, a different metric defined in a different section (§7.2 line 791) whose own registered rule points the other way: a pair "contributes misses and stays in the denominator". The only other registered instance of the convention (§7.9 line 896) is again about *precision*. The proposition "§7.2.1 registers, generally, that an empty denominator yields undefined" is **NOT ESTABLISHED**.

(Recorded as open at Part 6 item 2(f) — "P7's citation-scope items on SC-13a(a3) and SC-13b(b2)" — so this is a known item, not a new one; I verify it here as correctly identified.)

## M6. SC-13a(a3) quotes line 830 in support of the very thing line 830 excludes

**The clause** (line 1200): "**per detector** is §7.4's own scope-eligibility term read at the detector row whose metric is being computed — scope-eligibility being '**a property of the corpus label, not of what the detector could do about it**'".

**`PREREG.md` line 830:** "**scope-eligible** — the leakage risk logically applies to this unit. For a labelled feature-cohort pair this is a property of the corpus label, **not of what the detector could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss."

The quoted clause is the sentence that makes scope-eligibility **detector-independent for a labelled pair**. It is quoted to license a **per-detector** reading of the same denominator. A per-detector reading may be defensible on line 830's first sentence ("the leakage risk logically applies to this unit", risks being detector-kinded), but the words actually quoted hold against it, and (a3) is the limb whose whole purpose is to forbid narrowing: "**A declaration may not use the enumeration to remove from the denominator a pair the corpus labels and the risk logically applies to**." (Also at Part 6 item 2(f).)

## M7. SC-13c(c2) and §AB cite the wrong limb of SC-12

**The citation, twice** — SC-13c(c2) (line 1375) and §AB (line 1529): "A gate suppressed on the `not_applicable`-everywhere fact is a detector waived on it — **SC-12's definition, head and limb (iii)**".

**SC-12's limbs** (line 971): "**(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty for a pass; **(iii)** the criterion can be satisfied by another detector's output alone;"

A suppressed gate leaves the detector in the denominator with its findings no longer capable of being required — limb **(ii)**. Limb (iii) requires that *another detector's output alone* satisfy the criterion, which is a fact about the other detector, not about suppression, and fails outright in the case where both governed detectors are suppressed. The head ("incapable of changing the criterion's outcome") does support the conclusion — and SC-13b(b3) (line 1291) cites the head *alone* and is correct. (c2) and §AB add a limb that does not hold, in the two places the exception's authority is recorded.

## M8. SC-5(c) restates unamended criterion 2's scope in terms criterion 2 does not use

**The clause** (line 490): "**It is not converted into a failure of the clean-source criterion**, which has no landing site for such a unit; that criterion's scope is **the units the declaration declares clean**, and those units **do** route to it."

**`PREREG.md` line 460, which SC-5's marker says stands byte-exact:** "2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`."

Criterion 2's scope is a **manifest** fact, not a declaration fact. The distinction is one the amendment itself insists on elsewhere — SC-4(a) (line 376): "An evidence artifact's classification of how a unit was *built* answers a different question from what the map declares *violating* on the scored side under the declared branch; the two do not in general have the same answer." The declaration reads line 460 the registered way (`AVAILABILITY_DECLARATION.md` §A.11: "Criterion 2 | 460 | SATISFIED — scope is manifest-CLEAN columns only"). SC-5(c) re-scopes an unamended criterion by describing it, in a clause whose marker says "§6.2 criteria 1, 2 and 4 stand byte-exact."

## M9. SC-4(g) cites §0.2.1 line 79 for the converse of what line 79 holds

**The clause** (line 429): "**(g) ONE GATE CLASS PER UNIT.** A unit carries **one** gate class and one only — **§0.2.1 line 79's rule that no field answers two questions, applied to gate classes.**"

**`PREREG.md` line 79:** "**No field answers two questions.** Where a measurement concept has two independent axes, the specification carries two fields. Compressing them into one guarantees that the single field misdescribes at least one axis on some case".

Line 79 forbids one *field* carrying two *axes*, and its remedy is to add a second field. SC-4(g)'s headline proposition — one *unit* carries one *value* — is a different rule, and line 79 does not hold it. The **second half** of (g) *is* line 79's rule correctly applied ("An availability *declaration* about a unit and its *gate class* are different objects and are never conflated"), which makes the head's misattribution easy to miss.

## M10. SC-1's §2.4 marker leans on a sense of "unit" that line 93 does not carry

**The marker** (line 136): "Under SC-1(d) the horizon's unit is declared by the declaration, and a declared unit other than a duration is a class C amendment under **§0.2.1 line 93's word 'unit'**."

**`PREREG.md` line 93:** "| **C — semantic or accounting gaps** | The measurement reveals a needed *new* branch, **unit**, denominator, coverage state, tier licence, or acceptance criterion | **not resolve under this registration** | anything that changes what a published number means |"

Read in its own list — beside "branch, denominator, coverage state, tier licence, acceptance criterion" — and against every other registered use of the word (§7.2 "The runtime scoring unit", §7.3 "The duplicate counting unit", SC-13a(a1) "**UNIT.** The scoring unit is…"), line 93's "unit" is a **scoring/counting unit**, not a unit of measure such as a duration. The class C conclusion survives on line 93's catch-all ("anything that changes what a published number means"), but the marker rests it specifically on "line 93's **word** 'unit'", and that word does not carry the sense claimed.

## M11. SC-3's consequential marker on §10.1 line 1022 transfers a ground that does not transfer

**The marker** (line 279): "**Consequential — §10.1 line 1022** (H1 **C2**): the kill gate carries **a second copy of the retired premise** ('silent on `fixture_corrected`') and must be amended with this clause or `PREREG.md` holds both readings at once."

**The ground SC-3 gives for retiring criterion 3** (line 275): "*Retired because a fixture side may carry real, strictly-post-decision violations, in which case the registered criterion **fails the gate on a correctly-behaving detector** reporting a violation the fixture really contains.*"

**`PREREG.md` §10.1, lines 1018–1022:** "**Stop building and contribute upstream if a single maintained tool satisfies all five:** … 3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;"

§10.1 is a **five-condition test on a third-party tool for stopping this project**. The same factual premise there does not fail a gate on a correctly-behaving detector; it makes the kill gate *not fire* on a correctly-behaving rival — the opposite direction of error, and the conservative one. The words are a second copy; the *holding* SC-3 cites as the reason to amend them is not. The set's own other reading of the same line says so: SC-13a's marker (line 1146) — "The Phase 0 kill gate's third condition already carries the ambiguity branch on its face … and is **not** amended by these clauses: §10.1 scores a *third-party tool*, SC-13a scores *this project's* runtime detectors. Named here so the two are not conflated during application."

---

## Checked and found sound (so the absence is not read as unexamined)

`§0.2.1 line 93` cited by SC-2(b)/(d), SC-6 REGISTERS ("a needed *new* … coverage state"), SC-12(w)(2); `line 97` cited by SC-8(f) and the S2(ii) marker (verified against `tagmsg.txt`: item 3 names three files, the executed tag enumerates five, line 97 says "both" — the marker's factual claim holds); `line 95`; `§2.7`/`§8.1` cited by SC-3(g); `§7.1` lines 759/760 and `§10.2` line 1039 cited by SC-12 and SC-13c(c3); `line 768` ("Proof yield exists only for the `preserving` combination") cited by SC-13c(c4); `line 820` ("No runtime metric reads the detector-case state of §7.7, which exists for `assert_audit_complete()` alone") cited by SC-12(w); `line 929` cited by the SC-12(w) second insertion; `§6.6` states cited by SC-13a(a2); `§7.7` line 855's row quoted byte-exact in SC-6's marker; `§10` line 992's Phase 1 gate cell cited by SC-2's C1 marker (it does read on both retired objects — "both fixture AUCs reproduce within ±0.010, full and sliced").

Already disclosed in the file and not re-litigated here: SC-13c(c1)'s "(line 1033; SC-12 item (5))" for an amendment-substitution point (Part 4, Q4 nit (a)); SC-13b's marker naming line 570 (Part 4, nit (c)); stale declaration line numbers in the two *Instance record* blocks (§A.12 is at 1611, not 1543; §A.8 at 1485, not 1407) — mechanical, and the substantive content at both sites checks out, including §A.8's declared cell key "(side, instrument, month, class)".

==============================================================================
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