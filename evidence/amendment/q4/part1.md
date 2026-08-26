# PART 1 — THE SCHEMA SET, AS CORRECTED, VERBATIM

Convention for each clause (K1's): **REGISTERS** · **INSERTION POINT** · **SUPERSESSION MARKER** ·
**THE CLAUSE** · **DATA THE DECLARATION MUST SUPPLY** · **ROWS COVERED**. Text is K1's / the split
file's verbatim except where the change ledger (Part 5) records an edit; every edit is marked in the
ledger by clause and limb.

---

### SC-1 — THE DECLARED AVAILABILITY MODEL IS THE GATE'S SEMANTIC AUTHORITY

**REGISTERS.** That the declaration, not the specification and not a role name, fixes the meaning of
every term the comparator reads; and the four ways a declaration can fix it wrongly.

**INSERTION POINT.** New **§2.9**, inserted after `PREREG.md` **line 266** (the closing sentence of
§2.8, "Therefore: every L2a and L3.1 finding prints its declaration…"), before the `---` at line 268.
It sits at the end of §2 because §2 is where the availability primitive is registered, and because
§2.8 already concedes that the declaration is an assumption the tool cannot verify — SC-1 is what
that concession requires in return.

**SUPERSESSION MARKER.** Two, both narrow:

> **§2.3 line 205 (`column_roles`) — v30a, ADDED NOT SUPERSEDED.** The role enumeration stands
> byte-exact. SC-1(c) states what a role value *is* relative to the comparator; it removes no role
> and adds none.
>
> **§2.4 lines 220–222 — v30a, PARTIALLY SUPERSEDED.** The formula
> `a(y_j) = label timestamp + label horizon + publication delay` stands byte-exact as the *form*.
> **Superseded is the assumption, unstated in v30, that the horizon term's unit is a duration.**
> Under SC-1(d) the horizon's unit is declared by the declaration, and a declared unit other than a
> duration is a class C amendment under §0.2.1 line 93's word "unit". The v30 reading is retained
> beside this marker and is NOT operative as an exclusive reading.

**THE CLAUSE.**

> **§2.9 What a reconstructed declaration fixes, and what it may not leave open — v30a [SC-1]**
>
> A declaration is the gate's semantic authority: every availability instant a comparator reads is
> the one the declaration declares. Six requirements follow, and a declaration that does not meet
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

**DATA THE DECLARATION MUST SUPPLY.** The measured value and the documented value of each element,
with the artifact each was read from; per element, the representation it describes and the transform
where one exists; per column, the declared availability instant and whether its role is an
approximation of it; the unit of every term it supplies to a registered formula; the declared `ties`
branch; the informational figures under the non-declared branch, labelled as such.

**ROWS COVERED: 1, 3, 4, 72, 96, 104, 124.**

---

### SC-2 — THE ACCEPTANCE FIXTURE: WHAT IT IS COMPOSED OF, AND WHAT MAY MOVE

**REGISTERS.** The identity of the object the criteria are evaluated on — which artifacts constitute
it, what may be admitted into it, what is excluded from it, and that reference anchors are declared
entries rather than transcribed figures.

**INSERTION POINT.** After `PREREG.md` **line 451** (`- **Sliced variant** for CI, …`), i.e.
immediately after §6.2's bulleted element list and before the `**Pass gate — discrimination, not
tier.**` heading at line 453. This keeps the fixture's *composition* together and above the criteria
that read it.

**SUPERSESSION MARKER.** This clause is the schema layer over three amendments H1 already drafts at
instance-bearing lines. Their markers stand as H1 wrote them and are cited, not re-drafted:

> **§6.2 line 445 — SUPERSEDED BY v30a** (H1 hunk **H2**): the registered anchor pair and its
> transcription are retired; SC-2(d) registers the anchor's *form*, H2 retires the *figures*.
> **§6.2 line 450 — SUPERSEDED BY v30a** (H1 hunk **H3**): recording locus.
> **§6.2 line 451 — SUPERSEDED BY v30a** (H1 hunk **H4**): the sliced variant re-registered.
> **§10 line 992 — CONSEQUENTIAL** (H1 **C1**): the Phase 1 gate cell reads on both retired objects.

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

**DATA THE DECLARATION MUST SUPPLY.** The artifact enumeration per side with provenance; the declared
exclusions and the ground of each; the pre/post pairing and the evidence that the sides differ in
availability only; the reference-anchor entries and their tolerance; any element moved between phases
with its due event.

**ROWS COVERED: 11, 14, 25, 66.**

---

### SC-3 — THE DECLARED GROUND-TRUTH MAP, AND THE POPULATION IT SCORES

**REGISTERS.** Criterion 3's scoring key as a schema object: a per-side, per-declared-class,
per-declared-cell enumeration of expected findings; the population it covers; the three dispositions;
the single-key rule; and the freeze that makes it ex ante.

**INSERTION POINT.** **REPLACES `PREREG.md` line 461** (criterion 3), carrying H1 hunk **H5**'s
structure. The generic cell-key formulation below **supersedes H5's** on one axis: H5 wrote "per
declared map cell — the cell key is the unit the declaration declares the fixture to be partitioned
into"; SC-3 keeps that and adds the *checkability* and *coverage* limbs H5 left to §A.

**SUPERSESSION MARKER.**

> **SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:**
> "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`."
> *Retired because a fixture side may carry real, strictly-post-decision violations, in which case
> the registered criterion fails the gate on a correctly-behaving detector reporting a violation the
> fixture really contains. The measured incidence is instance data and lives in the declaration.*
>
> **Consequential — §10.1 line 1022** (H1 **C2**): the kill gate carries a second copy of the retired
> premise ("silent on `fixture_corrected`") and must be amended with this clause or `PREREG.md` holds
> both readings at once.

**THE CLAUSE.**

> **3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH
> MAP — v30a, operative. [SC-3]**
>
> **(a) WHAT THE MAP IS.** The map is an **enumeration of expected findings**, declared in the
> fixture's availability declaration, stated **per side**, **per declared violation class**, and
> **per declared cell** of the declared scored population. **The declaration declares the cell key —
> the unit it declares the fixture to be partitioned into — and names it explicitly.** The map is
> published as an artifact with a **declared schema**: one row per scored cell, with every field
> named, including the field that records whether the cell is scored.
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

**DATA THE DECLARATION MUST SUPPLY.** The map artifact and its schema; the cell key and its name; the
declared violation classes; the declared scored population and its subclasses; the per-cell expected
findings; the unscored ledger; any reporting re-aggregation with its delta.

**ROWS COVERED: 5, 6, 26, 55, 56, 74, 89, 95.**

---

### SC-4 — THE SCORED-SET PARTITION, AND CRITERION 1's DENOMINATOR

**REGISTERS.** That criterion 1's denominator is **derived** from the declared availability model by a
**derivation rule the declaration states ex ante**, that the derivation yields a three-class partition
of the declared scored set, and the discipline that makes the partition auditable.

**INSERTION POINT.** After `PREREG.md` **line 464** (`Secondary findings on **manifest-listed
descendants** …`), carrying H1 hunk **H6**'s placement. Criterion 1's own text at line 459 **stands
byte-exact**; this clause states how its denominator is constituted, which the registered text left to
be inferred.

**SUPERSESSION MARKER.**

> **§6.2 line 459 — v30a, ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact.
> **SUPERSEDED BY v30a is the inference** that the denominator is any construction-taxonomy count
> recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it.
> **§6.2 line 446 — NOT AMENDED.** The manifest requirement stands; only the *arithmetic role* of
> what it records is constrained, which is a statement about denominators, not an edit to line 446.

**THE CLAUSE.**

> **The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]**
>
> **(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY A RULE THE DECLARATION STATES.** The
> declaration states, **ex ante and in full**, the rule by which each unit of the declared scored set
> is assigned its gate class, and the classes are **derived by that rule, never assigned by hand.**
> An evidence artifact's classification of how a unit was *built* answers a different question from
> what the map declares *violating* on the scored side under the declared branch; the two do not in
> general have the same answer. **No classification of the scored set other than this derivation
> enters any criterion, denominator, or count**, and no split within such a classification carries
> gate arithmetic. Any report quoting such a count names the scope it counts under.
>
> **(b) EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE DECLARED SCORED SET.**
>
> | Class | Definition (the declaration supplies the predicate) | What a finding on it means |
> |---|---|---|
> | **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
> | **OUT OF JURISDICTION** | every constituent read is declared legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
> | **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |
>
> **There is no fourth class and no residue class.** **N is the length of the REQUIRED list**, and no
> other quantity is N.
>
> **(c) PRECEDENCE, DECLARED.** Where a unit satisfies more than one class predicate, **UNSCORED
> wins.** The declaration states the precedence order it derives under, and a unit's class is the
> first the order yields.
>
> **(d) THE DECLARATION FIXES THE RULE'S EDGES, AND THE READINGS ARE PART OF THE RULE.** Where a class
> predicate admits two readings, the declaration states which it derives under and why. **Two
> readings are registered as forbidden outright**, because each silently removes units from the
> arithmetic: (i) a locality condition may not be read more narrowly than the declared lattice, so a
> read of the same source at another instant of the same lattice does not by itself create a
> cross-source violation; (ii) **unconstructibility in some other rebuild of the fixture is never
> gate-unscoredness** — only a gate status the declaration declares EXCLUDED on the artifact the gate
> actually scores removes a unit from the arithmetic.
>
> **(e) GROUNDS FOR EXCLUSION ARE DECLARED, AND DECLARED PRE-RUN.** A unit is excluded only on a
> ground the declaration states. Two grounds are registered here because each is otherwise a
> guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that
> cannot carry a finding of the scored class at all** (leaving it in the denominator makes criterion 1
> unsatisfiable), and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot
> be scored under any reading). **Reinstating an excluded unit changes the denominator and is class
> C.**
>
> **(f) PUBLICATION DISCIPLINE — three constraints, and they are the point of the rule.**
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

**DATA THE DECLARATION MUST SUPPLY.** The derivation rule in full; the named constant identifying the
scored set; the three enumerated class lists; the precedence order; the reading it derives under at
each edge; the declared exclusion grounds and the units excluded on each; the printed partition check;
N.

**ROWS COVERED: 17, 19, 29, 30, 31, 32, 33, 34, 35, 36, 48, 50, 59, 93, 98, 99, 103, 105, 108.**
*(19 rows — the largest clause in the set. See K1 finding F-3 for the split option.)*

---

### SC-5 — ADJUDICATION ROUTING: WHICH CRITERION A FINDING IS CHARGED TO

**REGISTERS.** That every finding is routed to exactly one criterion by a declared rule; that
attribution is to the ground the map declares, not to the unit's name; the jurisdiction boundary
between detectors; and declared sentinels under the identity control.

**INSERTION POINT.** After the block SC-4 inserts (i.e. after `PREREG.md` line 464 + SC-4), before
line 466's parenthetical. Routing must sit below the partition it routes over.

**SUPERSESSION MARKER.** None — pure insertion. §6.2 criteria 1, 2 and 4 stand byte-exact; SC-5 states
which of them a given finding reaches, which the registered text left unstated.

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

**DATA THE DECLARATION MUST SUPPLY.** The routing table from gate class × map disposition to
criterion; the units with two grounds and which ground governs each; the detector rows this gate does
and does not score; the enumerated sentinels with their signatures.

**ROWS COVERED: 38, 39, 42, 43, 44, 58, 100, 101, 107.**

---

### SC-6 — `UNSCORED`: A NEW COVERAGE STATE, AT TWO LEVELS

**REGISTERS.** A **new coverage state** — not a word added to a list — with its semantics, its entry
condition, its two levels, and its gate consequences. Class C on `PREREG.md` line 93's own words ("a
needed *new* … coverage state").

**INSERTION POINT.** **Two, and both are required** (see K1 §0):

1. **`PREREG.md` line 855**, the §7.7 coverage-state table row — REPLACE the row to add the state,
   then INSERT the semantics block after the table (line 856).
2. **`PREREG.md` line 915**, §8.2 — INSERT after the sentence "None may be displayed in a way
   mistakable for a pass.", which is the existing hook.

**SUPERSESSION MARKER.**

> **§7.7 line 855 — SUPERSEDED BY v30a. Registered v30 row, retained verbatim, NOT operative:**
> "| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`,
> `could_not_run(reason)`, `waived` |"
> *Superseded because the six-state list has no state for a unit the declaration declares
> unscoreable. Absent such a state, an unscoreable unit is forced into `not_applicable` (which reads
> as "the question does not arise") or into a pass — which is the failure the state exists to stop.*
>
> **§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED.** §8.2's list is the *not-run* subset and stays
> correct as far as it goes; `unscored` joins it, and §8.2's closing sentence governs it unchanged.

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

**DATA THE DECLARATION MUST SUPPLY.** The unscored ledger at each level — every unscored cell and
every unscored unit, by name, each with its ground — frozen before any detector runs.

**ROWS COVERED: 46, 49, 60, 82.**

*(K1's finding F-6 — that `unscored` would otherwise have repeated `waived`'s missing-entry-condition
defect, and that §7.7's `waived` still has none after this amendment — stands as the drafting record
for limb (b); the reference to it is kept here, in apparatus, and removed from the applied clause
text.)*

---

### SC-7 — THE GATE'S INPUT SURFACE, AND THE SEQUENCING RULE

**REGISTERS.** What a detector may and may not receive at gate time. `PREREG.md` §6.2 currently
specifies *what* is evaluated and never *what the evaluated thing is allowed to see* — the largest
silent hole the scrub found.

**INSERTION POINT.** After `PREREG.md` **line 468** (`Top-k presence does not satisfy criterion 1. An
alias satisfies it only if recorded before the run.`), before line 470's "What this gate does and does
not guarantee". The surface belongs with the gate's framing, immediately after the criteria and before
the guarantee paragraph that characterizes them.

**SUPERSESSION MARKER.** None — pure insertion. No registered text states an input surface, which is
why it must be created rather than amended.

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

**DATA THE DECLARATION MUST SUPPLY.** The enumerated declared elements handed to a detector; the
enumerated artifacts withheld; the run order across sides.

**ROWS COVERED: 129, 130.**

---

### SC-8 — EX-ANTE DECLARATION AND THE FREEZE

**REGISTERS.** What makes "declared ex ante" mean anything: what freezes, in what form, when, and what
may not happen to it afterwards.

**INSERTION POINT.** **Two:**

1. After `PREREG.md` **line 480** (`**Ordering, locked:** tune … → run the fixture gate → tag …`) —
   the freeze is the ordering rule's enforcement mechanism and belongs beside it.
2. A pointer item added to **§11** after line 1054, so registration integrity indexes the freeze.

**SUPERSESSION MARKER.**

> **§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED.** The locked ordering stands byte-exact. SC-8
> states what the ordering ranges over and what happens when a frozen object is later found wrong,
> which line 480 left unstated.
> **§11 items 1–7 — v30a, EXTENDED.** Item 3's hash set is amended by R23 independently of this
> clause; SC-8(f) states the requirement generically and does not fix a count.

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

**DATA THE DECLARATION MUST SUPPLY.** The exhaustive enumeration of frozen objects; each in its
auditable form; the ex-ante checkability procedure for each; the justification of every scope
restriction; the file set the tag message hashes.

**ROWS COVERED: 80, 88, 106, 119, 120, 121, 122, 125.**
**Also carries NON-GATE row 126 as INTEGRITY → PREREG (see K1 §3).**

---

### SC-9 — DECLARATION INTEGRITY, AUTHORITY, AND INTERPRETATION

**REGISTERS.** R25's third disposition. These rules never flip a verdict alone, and that is exactly
why they belong here: they are what makes a declared instance honest, and a gate over a dishonest
instance is not a gate.

**INSERTION POINT.** After `PREREG.md` **line 99** (the class C "discovered after the affected detector
already exists" paragraph), inside §0.2.1, before line 101's "Membership in A or B must be citable".
§0.2.1 is the amendment machinery; these are its integrity rules.

**SUPERSESSION MARKER.** None — pure insertion. §0.2.1 lines 93–99 stand byte-exact. SC-9 states what
the machinery may not be used to do, which lines 93–99 assume rather than say.

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

**DATA THE DECLARATION MUST SUPPLY.** Its working-resolution record, complete and append-only, with
the supersession order explicit; the recording locus of every registered element it carries; citations
in place of restatements.

**ROWS COVERED (GATE-CRITICAL): 7, 128.**
**Also carries NON-GATE rows 8, 9, 18, 22, 23, 27 as INTEGRITY → PREREG per R25, and the normative
content of row 138's R13 (see K1 §3).**

---

### SC-10 — DECLARED NON-GATED DATA, AND FORBIDDEN GATE ARITHMETIC

**REGISTERS.** That a declaration may carry data the gate does not consume, and the conditions under
which that data stays out of the arithmetic.

**INSERTION POINT.** After `PREREG.md` **line 441** (the closing sentence of §6.1, "The descriptive
proof count of §6.2 is the sole reported fixture outcome…"), immediately below the five-bodies table.
**See K1 finding F-5: §6.1's table is a closed enumeration headed "Five bodies of data", and this
clause collides with it unless the heading or the table is amended.**

**SUPERSESSION MARKER.**

> **§6.1 line 431 heading and table — v30a, AMENDED IN FORM.** The five bodies stand unchanged as
> bodies of data. **Superseded is the implication that the enumeration is exhaustive of everything a
> fixture declaration may carry.** A declared non-gated diagnostic is not a sixth body of data; it is
> data attached to the acceptance fixture that the fixture's row of the table does not admit to any
> denominator. The alternative — adding a sixth row — is named in F-5 and is the author's call.

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
> **(d) FOUR FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**
> Non-gated data, diagnostic classes, and figures the declaration marks informational may never be
> quoted as: **(1)** evidence about a unit the scored pipeline consumes, in either direction; **(2)**
> **any criterion-1 arithmetic**; **(3)** an unqualified headline over the scored population; **(4)**
> an unqualified maximum or peak. A peak is quoted with its class set **and** its metric, or it is not
> quoted.
>
> **(e) ONE COPY.** These rules are stated here and cited elsewhere. A declaration restating them for
> a particular side has created a second normative copy (§0.2.1 line 77) and must cite instead.

**DATA THE DECLARATION MUST SUPPLY.** The non-gated bodies, marked; the diagnostic classes, named as
diagnostic; the declared class set the map scores; the class set and metric attached to every peak it
publishes.

**ROWS COVERED: 75, 85, 92, 110, 123.**

---

### SC-11 — ZEROS, ABSENCES, AND PASS CLAIMS

**REGISTERS.** The all-zero control, and the rule that converts a zero into a finding rather than a
pass. Under criterion 3 a zero-violation aggregate **is** a pass claim, which is why this is
gate-critical rather than hygiene.

**INSERTION POINT.** After `PREREG.md` **line 892** (§7.8's closing paragraph, "Conformance cases
contribute to no detection metric…"), as a new §7.8 sub-block; plus a one-line pointer after **line
961** (§8.6) so the reporting section indexes it.

**SUPERSESSION MARKER.** None — pure insertion. No registered clause states a control over
aggregation; §8.6 governs provenance of numbers that exist and is silent on numbers that come back
empty.

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

**DATA THE DECLARATION MUST SUPPLY.** The expectation each aggregate is checked against; the named
check accompanying every reported zero; the population each zero is zero over.

**ROWS COVERED: 78, 90, 134, 135.**

---

### SC-12 — THE REPLACEMENT-CRITERION FLOOR, AND "WAIVED" DEFINED

*(K1's SC-12 with the split file's Part 5 deltas 1–3 merged in, and two further corrections recorded
in the ledger: the `promoted` row anchored to line 760, and the declaration-section corroboration
moved out of the applied clause text into the apparatus.)*

**REGISTERS.** The defining clause for a word used in a locked floor and in a coverage-state table
without one. Carries H1 hunk **H7** essentially unchanged; it is listed here because the accounting
must dispose of rows 62, 63 and 64, and because R22's determination makes the floor **live**.

**INSERTION POINT.** After `PREREG.md` **line 1035** (`The replacement may be stricter than the floor
and may not be weaker: …`), preserving the three-space indentation of §10.2 criterion 2's block; plus
the §7.7 pointer H1 drafts as hunk **H8** after line 856.

**SUPERSESSION MARKER.** None — pure insertion. The floor stands byte-exact; the definition is added
beneath it. **It changes no threshold, exempts nothing, and grants no permission.**

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

**DATA THE DECLARATION MUST SUPPLY.** Nothing for the governed set — **the declaration does NOT
supply which detectors the floor governs**; the clause pins it by citation. The replacement
criterion's unit, threshold, and denominator, which this clause does not and cannot supply (K1
finding F-7), are discharged by SC-13a when the ambiguity branch has fired; SC-12 itself consumes no
instance data.

**ROWS COVERED: 62, 63, 64.**

*Instance record (apparatus, not applied).* The three registered sites the governed-set paragraph
pins to, verbatim as read this pass — `PREREG.md` **lines 759, 760 and 1039**:

```
| **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; conditional feature-cohort recall; cohort sensitivity; feature-cohort precision; feature discovery recall (secondary); unprobed feature-cohort rate; clean-case finding rate; completion and failure rates |
| **Runtime, `promoted`** | L2a, L3.1 | **evidence yield** and the same family below the first row, computed over `dtype_promoted` findings only |
   - **Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others.
```

**Corroboration, this fixture:** `AVAILABILITY_DECLARATION.md`
§A.12 lines 1543–1544, "**The two runtime detectors the floor governs are L2a and L3.1** (PREREG.md
lines 318, 320; line 1039 names 'both of L2a/L3.1's combinations')" — provisional declaration text,
cited here in apparatus and not in the applied clause (see Part 3, Q2(c), and Part 4, SC-12 row).
The wording variance the split file disclosed and left unresolved stands as disclosed: limb (iii)
reads "**another** detector's output alone" here where §A.12 line 1553 reads "**the other**
detector's output alone"; with the governed set pinned at two members the readings coincide.

---

### SC-13a — THE CRITERION

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

**SUPERSESSION MARKER.** One, conditional rather than absolute:

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
> this criterion's required quantities only, its publication clause is kept and required, and a
> pointer to the exception is inserted at line 816's own site (SC-13c, second insertion point).
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

**DATA THE DECLARATION MUST SUPPLY.** None of its own. Every instance datum this clause consumes —
the labelled-unit sets, their per-side partition, the declared sides, the cohort predicate, the
branch record — is supplied under **SC-13b's** DATA block and frozen there.

**ROWS COVERED: none of J1's 76** — stated here once for SC-13a, SC-13b and SC-13c together. The
three clauses jointly discharge `PREREG.md` line 1033, which J1 records as an **obligation**, not as
a row, and they close the drafting consequence K1 records at F-7 as "not closable by any schema
clause". **The 76-row accounting of K1 §2 is unchanged**; its tally (75 covered, row 28 uncoverable)
stands exactly as written.

---

### SC-13b — ADMISSIBILITY

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
or retired by this clause. The registered lines it relies on — 816, 830, 570 — stand byte-exact
and are cited. The one registered rule whose *effect* this clause's (b3) departs from, line 816's
suppression clause, is handled as an express, scoped exception **stated and recorded at SC-13c(c2)**
and in the v30a amendments block — not by superseding line 816.

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

**DATA THE DECLARATION MUST SUPPLY.** The labelled-unit set for **each** governed detector,
enumerated by name and frozen before any run, with the ground on which each unit is labelled and the
detector risk kind it is labelled for; **the set's partition by declared side, non-empty in every
(detector × side) cell, per (b2)**; the declared fixture sides; the cohort predicate and its
regeneration procedure; and the record that the ambiguity branch fired. **The declaration does NOT
supply which detectors the floor governs** — SC-13c(c3) pins that.

**ROWS COVERED:** see SC-13a's statement, made once for all three clauses.

---

### SC-13c — INTERACTIONS

**REGISTERS.** Every relationship the criterion has with other registered or amended text, so that
neither SC-13a nor SC-13b carries one: the one-way adoption dependency on the §6.2 criterion-3
amendment; the express, scoped exception to `PREREG.md` line 816; the pinned governed detector set;
the two floor limbs of line 1035 that the criterion's core does not itself discharge; and the scope
and purpose statements.

**INSERTION POINT.** **Two:**

1. **Pure insertion, immediately after SC-13b's block**, same three-space indentation, still between
   line 1035's paragraph and line 1036. The enumeration is untouched.
2. **A pointer paragraph inserted after `PREREG.md` line 816** (§7.2.1), between line 816 and line
   818, so that the site of the excepted rule signals the exception — the same convention H1's hunk
   H8 applies at §7.7 for SC-12's `waived`. Text at §13c-P below. Anchor: line 816 as a full-line
   match (count 1 as read this pass); re-derive after any earlier edit.

**SUPERSESSION MARKER.** **None — insertion, not supersession**, with one relationship stated
precisely so it cannot be misread: **(c2) is an express, scoped exception to line 816's suppression
clause — a class C change to how line 816 reads at this one criterion, recorded in the v30a
amendments block — and not a supersession**: line 816's text stands byte-exact and governs unchanged
everywhere outside the quantities this criterion requires.

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
> scoring rule and its three dispositions are SC-3(b)'s, held by citation and not restated here**;
> its map is indexed as SC-3(a) declares — **per side, per declared violation class, and per
> declared cell** of the declared scored population. **The cell key is the declaration's to supply,
> not this clause's to state**: SC-3(a) requires only that a key exist, be declared and named, and
> be frozen with the map before any detector runs (SC-3(h), SC-8), and this clause names no key.
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

**DATA THE DECLARATION MUST SUPPLY.** None. This clause consumes no instance data, and it states the
one thing the declaration must **not** supply: the membership of the governed detector set.

**ROWS COVERED:** see SC-13a's statement, made once for all three clauses.

*Instance record (apparatus, not applied).* In this fixture, the amended criterion 3 that (c5)(i)
cites is recorded in `AVAILABILITY_DECLARATION.md` §A.8 (lines 1407–1436) per working resolution R9,
and §A.8 states the declared cell key in its instance form (line 1416: "per-side, per-class,
per-instrument-month violation map"). That key is SC-3(a)'s DATA — the declaration's to supply — and
appears in no applied clause of this set (Part 2, Q1(i)). The waiver definition (c2) and (b3) cite is
SC-12's; `AVAILABILITY_DECLARATION.md` §A.12 (lines 1546–1556) states the same definition and is
corroboration, provisional until the tag (Part 3, Q2(c)).

---

### §13c-P — THE LINE-816 POINTER (SC-13c, second insertion point)

**ANCHOR — `PREREG.md` line 816, verbatim (match count 1 as read this pass):**

```
**A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.
```

**SUPERSEDED TEXT: none.** Line 816 is unchanged; the paragraph is inserted after it, before line 818.

**INSERT AFTER (one paragraph, blank line each side):**

```

**The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a) [SC-13c(c2)].** For the quantities §10.2's ambiguity-branch replacement criterion requires — the per-detector, per-side `preserving` proof yields it gates, that gate itself, and the published yield it requires of the other combination — the suppression clause does not apply: the publication clause applies in full, and the computed yield and the gate outcome are published with the counts and the named reason. Everywhere else this sentence governs exactly as registered. The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is recorded in the v30a amendments block and is not changed by the exception.

```

**Why it is drafted this way.** It mirrors H8's form at §7.7: it names where the governing text lives,
states the scope of what it does and does not do, and adds no rule of its own — the exception's
authority and recording remain SC-13c(c2)'s. It names the amendments-block recording of the 816/830
relationship because an implementer at line 816 who then reads line 830 should find that the
disagreement is known and unresolved rather than discover it. **Rule vs instance:** entirely RULE; no
fixture, column, count, or figure appears in it. R24 test: passes — it would read identically in a
registration that had never seen this fixture.

---

### §AB — THE v30a AMENDMENTS-BLOCK RECORDING TEXT (revised; drafted, not applied)

*(Supersedes the split file's Part 3.1 text. Three changes, all in the ledger: the waiver authority
re-cited to SC-12 with §A.12 as corroboration; the working-resolution/deviation prohibition re-cited to
SC-9(c)/(e) and SC-12 item (5) with §D.3/§A.12 as corroboration; and one paragraph added recording
that the exception departs from line 818's applied holding on the amendment's own authority.)*

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
> and §A.12 item 5), and this recording supersedes the framing of the superseded ledger entry 3.4,
> which located the collision between line 816 and §A.12 limb (i): the operative conflict is
> registered-text-internal — 816 against 830 — and provisional declaration text cannot settle it.

---
