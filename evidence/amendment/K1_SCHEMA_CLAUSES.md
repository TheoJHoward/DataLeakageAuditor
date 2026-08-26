# ITEM K1 — THE v30a SCHEMA CLAUSE SET, DRAFTED AND UNAPPLIED

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are
untouched. No git command was run. The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not
read. This file is the only file this item wrote, and it is drafted for author approval.

**CLAUSE COUNT: 12.** (Designed at 13; three rows redistributed to reach 12 — every redistribution
is named in §4 finding F-2, and the 13th form is stated there so the author can choose. One
GATE-CRITICAL row, **row 28**, is **not coverable by any schema clause** — finding F-1.)

**What R24 means here, applied to every line below.** `PREREG.md` gains the SCHEMA: what kind of
object each gate input is, what the declaration must supply, and what the gate does with it. The
declaration keeps the DATA: the partition's cells, the map's rows, the per-instrument figures, the
enumerations these rules yield. **The test applied to every drafted sentence: would this clause make
sense in a registration that had never seen this fixture?** No clause below names a column, a count,
an instrument, a boundary expression, a class name, or any figure. Where a clause needs a parameter,
the clause says the declaration must supply it, and the parameter is listed in that clause's **DATA
THE DECLARATION MUST SUPPLY** block.

Sources read this pass:
- `…\scratchpad\amendment\J1_GATE_CRITICAL_CLASSIFICATION.md` (582 lines, in full) — the 76/26/36
  buckets and the R22 determination.
- `…\scratchpad\amendment\DECLARATION_SCRUB_LIST.md` (360 lines, in full) — the 138-row source.
- `…\scratchpad\amendment\PREREG_v30a_DIFF.md` (481 lines, in full) — H1's 9-hunk draft, taken as a
  foundation. Hunks H2, H3, H4, H5, H6, H7 are absorbed by clauses below and named where they are.
- `PREREG.md` — §0.2.1 (60–111), §2.3–§2.8 (185–266), §3 (270–283), §6.1–§6.6 (429–553), §7.5–§7.10
  (840–903), §8 (907–961), §10.1–§10.2 (1016–1042), §11 (1046–1054). **Read, not edited.**
- `AVAILABILITY_DECLARATION.md` — §D.1/§D.2/§D.3 (3363–3488), §E (3490–3519), §F.2/§F.3 (3550–3604).
  **Read, not edited.**

---

## 0. THE LINE 855 VERIFICATION, PERFORMED FIRST AS INSTRUCTED

`PREREG.md` **line 855**, read this pass, verbatim:

```
| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |
```

**CONFIRMED:** the current list is exactly `passed` · `failed` · `not_applicable` · `unsupported` ·
`could_not_run(reason)` · `waived` — six states — and **`UNSCORED` is absent.**

Two further facts read at the same time, both load-bearing for **SC-6**:

- **`PREREG.md` line 915** (§8.2) carries a *different, shorter* list: "coverage states are
  `not_applicable`, `unsupported`, and `could_not_run(reason)`". §8.2 enumerates the **not-run**
  subset only. A new state that is neither a pass nor a not-run therefore lands on **two** surfaces,
  and SC-6 must touch both or the two lists drift — which is §0.2.1 line 77's own failure shape.
- **`PREREG.md` line 915 closing sentence**, verbatim: "None may be displayed in a way mistakable for
  a pass." That is the existing hook SC-6 attaches to, exactly as J1 §5(f) recommends.

`UNSCORED` is therefore drafted below as **a new STATE with its own semantics, entry condition, and
gate consequences** (SC-6), not as a seventh word appended to a table row. `PREREG.md` line 93 names
"a needed *new* … coverage state" as class C **verbatim**, so this is class C on the registration's
own words.

---

## 1. THE CLAUSE SET

Convention for each clause: **REGISTERS** (the schema object) · **INSERTION POINT** (with the anchor
line as it stands today) · **SUPERSESSION MARKER** (where it amends registered text; "none — pure
insertion" where it does not) · **THE CLAUSE** (drafted generic text) · **DATA THE DECLARATION MUST
SUPPLY** · **ROWS COVERED**.

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

> **§2.9 What a reconstructed declaration fixes, and what it may not leave open — v30a**
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

> **The acceptance fixture's composition — v30a**
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
> MAP — v30a, operative.**
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

> **The criterion-1 denominator, and the partition rule that constitutes it — v30a**
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
*(19 rows — the largest clause in the set. See finding F-3 for the split option.)*

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

> **Adjudication routing — v30a**
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

**INSERTION POINT.** **Two, and both are required** (see §0):

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

> **`unscored` — a coverage state, v30a**
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
> §7.7's `waived` was registered without one — see SC-12 and finding F-6.)*
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

> **The gate's input surface — v30a**
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

> **The freeze, and what "declared ex ante" requires — v30a**
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
**Also carries NON-GATE row 126 as INTEGRITY → PREREG (see §3).**

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

> **Integrity of a declared instance — v30a**
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
content of row 138's R13 (see §3).**

---

### SC-10 — DECLARED NON-GATED DATA, AND FORBIDDEN GATE ARITHMETIC

**REGISTERS.** That a declaration may carry data the gate does not consume, and the conditions under
which that data stays out of the arithmetic.

**INSERTION POINT.** After `PREREG.md` **line 441** (the closing sentence of §6.1, "The descriptive
proof count of §6.2 is the sole reported fixture outcome…"), immediately below the five-bodies table.
**See finding F-5: §6.1's table is a closed enumeration headed "Five bodies of data", and this clause
collides with it unless the heading or the table is amended.**

**SUPERSESSION MARKER.**

> **§6.1 line 431 heading and table — v30a, AMENDED IN FORM.** The five bodies stand unchanged as
> bodies of data. **Superseded is the implication that the enumeration is exhaustive of everything a
> fixture declaration may carry.** A declared non-gated diagnostic is not a sixth body of data; it is
> data attached to the acceptance fixture that the fixture's row of the table does not admit to any
> denominator. The alternative — adding a sixth row — is named in F-5 and is the author's call.

**THE CLAUSE.**

> **Declared non-gated data — v30a**
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

> **The all-zero control — v30a**
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

**REGISTERS.** The defining clause for a word used in a locked floor and in a coverage-state table
without one. Carries H1 hunk **H7** essentially unchanged; it is listed here because the accounting
must dispose of rows 62, 63 and 64, and because R22's determination makes the floor **live**.

**INSERTION POINT.** After `PREREG.md` **line 1035** (`The replacement may be stricter than the floor
and may not be weaker: …`), preserving the three-space indentation of §10.2 criterion 2's block; plus
the §7.7 pointer after line 856 — **redrafted at DELTA R35/B3; H1's H8 draft is SUPERSEDED** and may not be applied, because it asserts that the entry condition for the `waived` coverage state is not defined by this registration, which SC-12(w) makes false. The operative pointer text is Y3 §6.3's.

**SUPERSESSION MARKER.** None — pure insertion. The floor stands byte-exact; the definition is added
beneath it. **It changes no threshold, exempts nothing, and grants no permission.**

**THE CLAUSE.** *(Generic form; H1's H7 text is compatible and is the drafting basis. The one change
from H7 is that the detector names are not hard-coded — the floor names "the runtime detectors" and
the declaration supplies which they are.)*

> **"Waived", defined — v30a**
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

**DATA THE DECLARATION MUST SUPPLY.** Which detectors the floor governs for this fixture; and — if and
when the branch is resolved — the replacement criterion's unit, threshold, and denominator, which
**this clause does not and cannot supply** (finding F-7).

**ROWS COVERED: 62, 63, 64.**

---

## 2. THE 76-ROW ACCOUNTING TABLE

Every GATE-CRITICAL row is accounted for as **exactly one** of: **COVERED BY SCHEMA CLAUSE `<n>`** ·
**INSTANCE DATA (declaration)** · **INTEGRITY → PREREG per R25** · **PRACTICES**. Where a row is
schema-covered, the clause and the covering limb are named, and "how" says what the schema registers
versus what the declaration supplies.

| Row | Statement (one line) | Disposition | Clause · limb | How the clause covers it |
|---|---|---|---|---|
| 1 | Declaration states the **measured** boundary, not the intended one | **COVERED** | **SC-1(a)** | Schema: measured governs, documented recorded beside it with provenance. Declaration supplies both values. |
| 3 | `column_roles` describe the raw pre-lag column; the fed value is the lagged one | **COVERED** | **SC-1(b)** | Schema: every element names the representation it describes and the transform. Declaration says which. |
| 4 | Label availability is **POSITIONAL**, not `T + h` seconds | **COVERED** | **SC-1(d)** | Schema: the declaration states each formula term's **unit**, and a unit change is class C. Declaration supplies the positional unit. Carries the §2.4 supersession marker. |
| 5 | Cross-boundary label rows are **IN the scored population** | **COVERED** | **SC-3(c)** | Schema: the declared population is whole; a subclass leaves the arithmetic only as a declared UNSCORED cell. Declaration supplies the population and its subclasses. |
| 6 | Findings on them are adjudicated by the **declared map** like any other row | **COVERED** | **SC-3(c)** | Schema: awkward membership is neither licence nor defence; the map adjudicates. |
| 7 | The declaration **creates no new gate criterion** | **COVERED** | **SC-9(a)** | Schema: a declaration supplies data under a registered schema and creates no gate object; the amended criteria are the whole gate. This is R24's own boundary rule, registered. |
| 11 | Pre/post licence: the sides differ in availability and **nothing else** | **COVERED** | **SC-2(c)** | Schema: bounds what is admissible as a side; a column-set/population change is not an availability change. |
| 14 | The registered anchor pair and interval are **retired and replaced** | **COVERED** | **SC-2(d)** + H1 **H2** | Schema: an anchor is a declared entry set constituted by recomputation, tolerance per entry, non-widenable. **Partial — see F-4:** retiring the *registered figures* at line 445 is H2's instance-level supersession, which the schema does not perform. |
| 17 | Line 446's count carries **no gate arithmetic**; the denominator is a different object | **COVERED** | **SC-4(a)** | Schema: the denominator is derived by the declared rule; no other classification of the scored set enters any criterion. |
| 19 | Nothing turns on the DAG **flavor** split | **COVERED** | **SC-4(a)** | Same limb: "no split within such a classification carries gate arithmetic." |
| 25 | The sliced variant is **moved off** the Phase 0 fixture, re-registered as Phase 1 CI | **COVERED** | **SC-2(a)(e)** + H1 **H4** | Schema: the fixture is a declared artifact enumeration; moving an element between phases is an amendment with its scoring rule declared at the move. |
| 26 | Slice scoring declared ex ante; a slice of a characterized side is never clean | **COVERED** | **SC-3(f)** | Schema: a derived subset inherits the map cells its units select; never clean; no pass on unscored cells alone. |
| 28 | §A.5: line 449's semantic-ambiguity clause **does not fire** | **NOT COVERABLE** | — | **FINDING F-1.** R22 rejects the reading. It is an interpretation of locked text, not a rule the schema can register; disposing of it requires an explicit class C amendment of `PREREG.md` line 449. Until then §10.2's branch is live. |
| 29 | The criterion-1 denominator derives from the **DECLARED MAP** | **COVERED** | **SC-4(a)** | This *is* the clause's head limb. Schema: derivation rule declared ex ante; declaration supplies the rule and its output. |
| 30 | Partition discipline: exclusive, exhaustive, **enumerated by name**, no residue, no bare count | **COVERED** | **SC-4(b)(f)** | Schema: three classes, no fourth, no residue; enumerated lists, not counts. |
| 31 | The three iff-clauses: REQUIRED / OUT OF JURISDICTION / UNSCORED | **COVERED** | **SC-4(b)** | Schema: the three class definitions in generic form; the declaration supplies the predicate for each. |
| 32 | Precedence when clauses conflict: **UNSCORED wins** | **COVERED** | **SC-4(c)** | Schema: precedence exists and UNSCORED wins; declaration states its derivation order. |
| 33 | "Same-row book/clock" reads as **within-lattice**, not literally single-row | **COVERED** | **SC-4(d)(i)** | Schema: a locality condition may not be read more narrowly than the declared lattice. Generic form of the reading; the lattice is declaration data. |
| 34 | "Unconstructible under T4" reads as **gate status EXCLUDED**, not rebuild-unconstructible | **COVERED** | **SC-4(d)(ii)** | Schema: rebuild-unconstructibility is never gate-unscoredness — registered as forbidden outright, because it silently drops units. |
| 35 | Rule-vs-frozen disagreement is a **stop-and-report** | **COVERED** | **SC-4(i)** | Schema: disagreement halts; a run past it has not scored the fixture. A halt is not a PASS. |
| 36 | Construction change forces re-derivation; the enumeration is the rule's output | **COVERED** | **SC-4(h)** | Schema: re-derivation mandatory; the enumeration never substitutes for the rule. |
| 38 | A required finding must be on the side and cells the map declares | **COVERED** | **SC-5(b)** | Schema: attribution is to the ground, side and cells the map declares. |
| 39 | Criterion 1 not satisfied by column name alone | **COVERED** | **SC-5(b)** | Same limb, stated as the negative. |
| 42 | An availability finding on an OOJ column is a **FALSE POSITIVE** | **COVERED** | **SC-5(c)** | Schema: the false-positive consequence attaches to the OOJ class and to no other. |
| 43 | Criterion 2 **cannot receive** OOJ columns | **COVERED** | **SC-5(c)** | Same limb: not converted into a clean-source-criterion failure; the clean set does route there. |
| 44 | An **L2a label-base** finding is neither credited nor penalized | **COVERED** | **SC-5(e)** | Schema: jurisdiction between detector rows is declared ex ante and cuts both ways. |
| 46 | **UNSCORED**: requires no finding, forbids none, cannot be reported as a pass | **COVERED** | **SC-6(a)(e)** | Schema: the new state's semantics at unit level, with the pass prohibition absolute. |
| 48 | **One gate class per column**; reinstatement changes the denominator, class C | **COVERED** | **SC-4(g)** + **SC-4(e)** | Schema: one class per unit (§0.2.1 line 79 applied); reinstating an excluded unit is class C. |
| 49 | These are **cells, not columns**; a cell-level unscored never makes a column unscored | **COVERED** | **SC-6(c)** | Schema: two levels that do not collapse, in either direction; reports state the level. |
| 50 | R11's third UNSCORED limb read precisely | **COVERED** | **SC-4(d)(ii)** | Same registered forbidden reading as row 34, stated at the class rather than at the rule. |
| 55 | **The amended criterion 3 itself** — findings must match the declared map | **COVERED** | **SC-3(a)(b)** | The criterion, generically: per side, per declared class, per declared cell; three dispositions. |
| 56 | Scope limits + **the map is declared and frozen before any detector runs** | **COVERED** | **SC-3(h)** | Schema: bar not lowered, unscored is no escape hatch, freeze before any run (with SC-8). |
| 58 | **SENTINEL:** wrapped values are DATA CONTENT; firing is a criterion-4 false positive | **COVERED** | **SC-5(f)** | Schema: an artefact identical on every side cannot differentiate; enumerated ex ante or it is not a sentinel. The signature is declaration data. |
| 59 | **N is the REQUIRED list length**, not the manifest count | **COVERED** | **SC-4(b)** | Schema: "N is the length of the REQUIRED list, and no other quantity is N." The value of N is declaration data. |
| 60 | Report k of N; FPs separately; **UNSCORED findings are NOT false positives**; never fold | **COVERED** | **SC-6(d)** | Gate-critical limb only: unscored findings are unscored observations, not false positives; classes never folded. (Reporting limbs → PRACTICES with row 51.) |
| 62 | The **DEFINITION of WAIVED**, limbs (i)–(v) | **COVERED** | **SC-12** | Schema: the defining clause for a word in a locked floor; zero fixture content. |
| 63 | **It may not be invoked** — no procedure exists | **COVERED** | **SC-12** | Schema: the floor is a prohibition, not a permission with conditions. |
| 64 | The seven "does not permit" scope limits | **COVERED** | **SC-12** | All seven carried; limbs 4 and 6 are the load-bearing ones and are stated in terms. |
| 66 | The excluded set is **HARD**; any future use is class C | **COVERED** | **SC-2(b)** | Schema: changing the fixture's composition changes what every gate number means; never a deviation or a WR. |
| 72 | Equal events are non-violations under the declared branch; both-branch figures informational | **COVERED** | **SC-1(f)** | Schema: one branch is scored; other-branch figures are informational and carry no gate outcome. (The comparator restatement limb becomes a citation of §2.3.) |
| 74 | The map **schema** — one row per scored cell, named fields | **COVERED** | **SC-3(a)** | Schema: the map is published with a declared schema, one row per scored cell, every field named including the scored flag. The ten field names are declaration data. |
| 75 | **CLASS-SET RULE:** a diagnostic class is not one of the declared set; every "max" names its class set | **COVERED** | **SC-10(c)** | Schema: diagnostic classes named as such, outside the scored set; maxima and headlines name their population. |
| 78 | "Clean on both branches" **withdrawn**; zero over partial classes is not a pass | **COVERED** | **SC-11(f)** | Schema: a zero over a partial population is a different predicate; no such row may be quoted as a pass. |
| 80 | A declared cohort must be **checkable from the declared inputs alone, pre-run** | **COVERED** | **SC-8(c)** | Schema: ex ante means regenerable and checkable before any detector runs; otherwise it is a description of the result. |
| 82 | Cell-level unscored: no finding required or forbidden; **cannot be reported as a pass** | **COVERED** | **SC-6(a)(c)(e)** | Schema: the same state at cell level, with (c) keeping the levels apart. |
| 85 | §13(h) is **NOT part of the gate**; moving it in is class C | **COVERED** | **SC-10(a)(b)** | Schema: declared non-gated data, exempt from the freeze **because** exempt from the arithmetic; admission is class C. |
| 88 | A scope restriction is **justified independently of its effect on any count** | **COVERED** | **SC-8(d)** | Schema: generalises the locked ordering to scope choices; no numeric-effect reference may be added. |
| 89 | The restricted map is a **REPORTING object**, not a second scoring key | **COVERED** | **SC-3(e)** | Schema: one scoring key; re-aggregations change no adjudication; both views published with the delta. |
| 90 | **An all-zero return would have been a FINDING, not a pass** | **COVERED** | **SC-11(e)** | Schema: where a declared expectation predicts non-zero, a zero is a finding about the aggregation or the declaration. |
| 92 | Four FORBIDDEN-USE rules — never criterion-1 arithmetic, no unqualified headline or max | **COVERED** | **SC-10(d)** | Schema: the four uses registered generically, criterion-1 arithmetic named explicitly as limb 2. |
| 93 | "The 35-column set" always means the named constant; **name the constant, not the length** | **COVERED** | **SC-4(j)** | Schema: the scored set is identified by its declared constant; two sets of equal size are not the same set. |
| 95 | Everything is **POST-LAG** and **SIDE-RELATIVE**; a side-independent list is a category error | **COVERED** | **SC-3(d)** | Schema: the map is stated in the declared representation and side-relatively; no side-independent statement exists. |
| 96 | The comparator is pinned; **`at_bar_close` is never scored against** | **COVERED** | **SC-1(c)** | Schema: a role is a position, not an availability instant; an approximating role is declared as such and never scored against. |
| 98 | The availability declaration and the gate class are **different objects** | **COVERED** | **SC-4(g)** | Schema: one gate class per unit; declaration and gate class never conflated. |
| 99 | The three category definitions, incl. not-fed → **no gate class whatever** | **COVERED** | **SC-4(g)** | Same limb's closing sentence: an unfed unit holds no gate class; calling it OOJ would imply adjudication. |
| 100 | The four routing rules | **COVERED** | **SC-5(c)(d)(e)** | Schema: FP attaches to OOJ; the double charge on a characterized side; the out-of-gate detector row; the clean set routes to the clean-source criterion. |
| 101 | Label-base character is **L2a jurisdiction**, outside this gate | **COVERED** | **SC-5(e)** | Duplicate of row 44 at a second site; one clause limb, and the declaration's second copy becomes a citation. |
| 103 | A **dead-zero column cannot carry an availability finding**; declared out pre-run | **COVERED** | **SC-4(e)** | Schema: the degenerate-unit exclusion ground, with its stated reason (criterion 1 otherwise unsatisfiable for a non-detection reason). |
| 104 | **Staleness is not unavailability**; the quirk licenses NO finding | **COVERED** | **SC-1(e)** | Schema: a value legal at the decision instant is available however old; age licenses no finding. |
| 105 | An unresolved construction/lag question forces **EXCLUDED**; reinstatement is class C | **COVERED** | **SC-4(e)** | Schema: the second registered exclusion ground, with the class C reinstatement consequence. |
| 106 | The exclusions are declared **pre-run** and frozen at the tag | **COVERED** | **SC-8(a)(c)** | Schema: exclusions are frozen objects and must be checkable before any run. |
| 107 | Criterion 1 not satisfied by name alone; another ground is recorded on its own ground | **COVERED** | **SC-5(b)** | Full statement of the attribution limb; three characters, three dispositions, no double-counting. |
| 108 | A gate class is **what the gate does with a finding**; exactly one answer per column | **COVERED** | **SC-4(g)** | Schema: the definition of the object the denominator is built from. |
| 110 | FORBIDDEN USE restated verbatim for the second side | **COVERED** | **SC-10(e)** | Schema: one copy here, cited elsewhere. **The declaration's second copy must become a citation** (§0.2.1 line 77). |
| 119 | What **freezes at the tag**; any subsequent change is class C | **COVERED** | **SC-8(a)** | Schema: everything the gate consumes freezes; the declaration enumerates exhaustively. |
| 120 | The partition freezes as **enumerated lists, not counts**; a report that cannot reproduce the sum has not scored | **COVERED** | **SC-8(b)** + **SC-4(f)3** | Schema: freeze form is the auditable form; the partition check and its non-PASS consequence sit in SC-4(f)3. |
| 121 | **Every other gate-consumed number** freezes, exhaustively enumerated | **COVERED** | **SC-8(a)** | Schema: the exhaustiveness obligation, with the omission rule ("a defect in the enumeration, not an object outside the freeze"). |
| 122 | The class-set rule and the amendments themselves freeze | **COVERED** | **SC-8(a)** | Schema: rule-objects and the amendments are gate-consumed objects and freeze with the rest. |
| 123 | §13(h) is **NOT frozen** — conditional on never entering an acceptance denominator | **COVERED** | **SC-10(b)** | Schema: the conditional exemption, and why unfrozen-plus-admitted is a movable denominator. |
| 124 | Both-branch counts are **INFORMATIONAL ONLY**; no gate outcome from them | **COVERED** | **SC-1(f)** | Duplicate of row 72's second limb at the freeze site; one clause limb. |
| 125 | A number found wrong after a result is **not corrected in place** | **COVERED** | **SC-8(e)** | Schema: stated as a **citation** of §0.2.1 line 99, not a restatement — which is what row 125 itself requires. |
| 128 | An interpretation of locked text may resolve **ONLY toward the STRONGER reading** | **COVERED** | **SC-9(e)** | Schema: verbatim in generic form, with its six enumerated weakenings. **R25 routes it here explicitly.** |
| 129 | The **gate input surface**: two things, one side; the map is never received | **COVERED** | **SC-7(a)(b)(c)** | Schema: the surface itself, and why the key is withheld — a run that received it has not produced a gate result. |
| 130 | **One side at a time is a hard sequencing rule** | **COVERED** | **SC-7(d)** | Schema: a multi-side run satisfies no criterion, however partitioned afterwards. |
| 134 | **THE ALL-ZERO CONTROL**; on mismatch it RAISES | **COVERED** | **SC-11(a)(b)(c)** | Schema: the control, its minimum sufficient form, and the raise-not-warn rule. |
| 135 | **SCOPE: this binds future gate reporting** | **COVERED** | **SC-11(d)** | Schema: the scope clause, naming per-criterion counts, FP tallies, and any clean statement. Not severable from 134. |

**Tally of the accounting: 75 COVERED BY SCHEMA CLAUSE · 1 NOT COVERABLE (row 28) · 0 INSTANCE · 0
INTEGRITY-only · 0 PRACTICES.** Every GATE-CRITICAL row appears exactly once.

**Per-clause load:** SC-1 = 7 · SC-2 = 4 · SC-3 = 8 · SC-4 = 19 · SC-5 = 9 · SC-6 = 4 · SC-7 = 2 ·
SC-8 = 8 · SC-9 = 2 · SC-10 = 5 · SC-11 = 4 · SC-12 = 3 · uncovered = 1. **Sum = 76.** ✓

---

## 3. THE 26 NON-GATE ROWS — R25 DISPOSITION

R25's test applied: a rule that **protects the honesty of a declared instance** is gate-critical in
effect and goes to `PREREG.md` even though it never flips a verdict alone. `PRACTICES.md` holds only
what is **neither gate-determining nor integrity-protecting**.

**RECLASSIFIED BY R25 AS INTEGRITY → PREREG (7 rows):**

| Row | Statement | Lands at | Why R25 reclassifies it |
|---|---|---|---|
| **8** | Delta-issued working resolutions bind exactly as recorded ones | **SC-9(d)** | R25 names "supersession and working-resolution authority" verbatim. A resolution whose authority depends on where it was written is a resolution that can be disowned after a result. |
| **9** | A later resolution supersedes an earlier; the earlier stands as record | **SC-9(d)** | Same R25 clause. Append-only ordering is what makes the ledger evidence rather than a draft. |
| **18** | The manifest is not edited; **evidence artifacts are never adjusted toward a decision** (R13) | **SC-9(b)** | R25 names this rule verbatim. It is the single rule that keeps the fixture's evidence from being tuned to the wanted verdict. |
| **22** | The contamination availability class is recorded in the declaration, not the evidence artifact | **SC-9(b)** + H1 **H3** | The recording-locus rule *is* the never-adjust-evidence rule applied: an evidence artifact may not be made the locus of a decision. |
| **23** | The locus amendment licenses no other content moving out of the manifest | **SC-9(b)** + H1 **H3** | The scope limit is part of the same integrity rule; without it, one locus move becomes a general licence. |
| **27** | The Phase 1 obligation may not be discharged by `DEVIATIONS.md` or a WR | **SC-9(c)** | Discharge machinery is precisely the "supersession authority" family. An obligation dischargeable by a deviation is not locked. |
| **126** | The tag message carries the declaration's hash as well as the specification's | **SC-8(f)** | The freeze is only as good as the chain that carries it. R23 disposes of the count independently; SC-8(f) registers the *requirement* generically and derives the count rather than stating one. |

**REMAINING PRACTICES (19 rows).** Each is a reporting, provenance, labelling, or evidence-accounting
rule: it neither determines a verdict nor protects the integrity of the declared instance.

| Row | Statement | Note |
|---|---|---|
| 2 | Generation-naming rule on every row count | §8.6 line 961 already carries the obligation; PRACTICES holds the specific naming form. |
| 10 | Every measurement claim names its artifact or is not publishable | Same — §8.6's territory; PRACTICES holds the "or it is not publishable" sharpening. |
| 13 | "Every AMENDED entry is a class C amendment carried by this registration" | A classification assertion about this declaration's own entries; §0.2.1 lines 93/95 already govern. Should become a citation. |
| 20 | A leaking-source count names the scope it counts under | The count is the same either way; SC-4(a) already carries the gate-side limb. |
| 47 | Named EXCLUDED, never MISSED | Reporting vocabulary. **Close call:** the substance is already carried by SC-6(e) and §8.2 line 915; PRACTICES holds only the word preference. |
| 51 | The partition check must be reproduced by any gate report | Its gate-critical twin is row 120 → SC-4(f)3 / SC-8(b). PRACTICES holds the report-facing phrasing. |
| 61 | The walk summary table and "four amendments" | Ledger bookkeeping — and J1 records that the count "four" is falsified by the object count. |
| 65 | Status: class C content; resolves toward the stronger reading | Status bookkeeping; the stronger-reading rule itself is row 128 → SC-9(e). |
| 68 | The licence for reading the pre/post AUC delta as availability-only | Interpretation of a provenance figure (§6.1 line 441); the fixture-admission limb is row 11 → SC-2(c). |
| 70 | A lag-image is not independent corroboration | Evidence accounting; no criterion reads it. |
| 77 | A ranking is quoted with its metric | Reporting legibility. |
| 83 | A partially-covered unit carries its coverage label and reason on every appearance | Labelling; the denominator limb is rows 85/123 → SC-10. |
| 87 | Both maps published side by side with the delta explicit | Publication obligation; the "not a second scoring key" limb is row 89 → SC-3(e). |
| 111 | Summary-level peaks exclude coverage-artifact cells | Governs summary quotation; per-cell adjudication unchanged. |
| 113 | Claims split into timing-structural SUPPORTED vs value-dependent QUALIFIED | Evidence accounting; criterion 4's rule on the same defect is row 58 → SC-5(f). |
| 115 | The documented-unverifiable **category** | Disclosure discipline; the three items themselves are INSTANCE (row 116). |
| 117 | Projection is selection or renaming only | Method rule for a rebuild that row 50 rules out of the gate-scored fixture. |
| 131 | An "every X in the archive" claim rests on a filesystem walk | Archive-survey method; governs evidence gathering, not verdict computation. |
| 133 | Every number read from a named artifact, with its class set / side / boundary / generation | Provenance discipline; §8.6 line 961's territory. |

**Split: 7 INTEGRITY → PREREG · 19 PRACTICES · 26 total.** ✓

---

## 4. THE 36 INSTANCE ROWS — CONFIRMED, THEY STAY

**Rows 12, 15, 16, 21, 24, 37, 40, 41, 45, 52, 53, 54, 57, 67, 69, 71, 73, 76, 79, 81, 84, 86, 91, 94,
97, 102, 109, 112, 114, 116, 118, 127, 132, 136, 137, 138** — **36 rows, all confirmed INSTANCE DATA
(declaration). No row moves.** Checked against R24 clause by clause: every one of them is a value, an
enumeration, a table, a measurement, an identity, or a record, and each is the *output* of a schema
clause above rather than a rule.

Four confirmations worth stating explicitly because a reader may expect them to move:

- **Row 37** (the rule-application table), **row 40** (the REQUIRED list), **row 45** (the OOJ lists),
  **row 52** (the partition counts) — these are SC-4's **output**. SC-4(h) says so in terms: the
  enumeration is the current output of the rule and never a substitute for it. They stay.
- **Row 76 / 79 / 91** (the map's contents) are SC-3's output. The schema is the row shape; the rows
  are data.
- **Row 116** (the three documented-unverifiable assumptions) stays in full — H2's own steer, and
  nothing in the schema set reaches it.
- **Row 136** (the all-zero near-miss narrative) stays. SC-11 is the rule; row 136 is the evidence that
  makes it credible, and a rule without its near-miss is a rule nobody believes.
- **Row 138** (the working-resolution tail) stays **byte-identical as a record**. R13's normative
  content is now carried by **SC-9(b)**, so after this amendment the tail is the *record of* a rule
  that lives in `PREREG.md` rather than the rule's only statement — which is exactly what H2 flagged
  as missing.

**Grand reconciliation: 76 GATE-CRITICAL + 26 NON-GATE + 36 INSTANCE = 138.** ✓

---

## 5. FINDINGS

Reported rather than solved, per the instruction.

**F-1 — ONE GATE-CRITICAL ROW THE SCHEMA CANNOT COVER: ROW 28.**
§A.5's reading ("documented-and-violated is not the same as undocumented", switching off
`PREREG.md` line 449's semantic-ambiguity clause) is **not a rule and cannot be registered as one.**
It is an interpretation of locked text, and **R22 rejects it** under the very rule SC-9(e) registers.
No generic clause can carry it: a schema clause saying "the ambiguity clause does not fire where
timing was documented but violated" would be a fixture-shaped adjudication written into the
specification, and — under SC-9(e) — the *weaker* reading of line 449, adopted by the schema itself.
**What is required instead:** an explicit class C amendment of `PREREG.md` line 449 stating on the
record that documented-and-violated timing does not trigger the clause, **or** acceptance that the
branch fires. Until one of those happens, **line 1033's obligation is live and unmet**, SC-12's floor
is in force, and Phase 1 may not begin (J1 §6.3). This is the one row where the accounting cannot
close, and it closes by decision, not by drafting.

**F-2 — THE COUNT IS 12, AND IT WAS 13. THE COMPRESSION IS NAMED, NOT SILENT.**
The set was designed with a thirteenth clause, **"The gate's extent and its scored population"**,
carrying rows 5, 7 and 93. It was dissolved and its rows redistributed:
- **row 5** → SC-3(c) — the population the map covers is the map clause's own subject;
- **row 7** → SC-9(a) — "a declaration creates no gate object" is R24's boundary rule and belongs with
  declaration authority;
- **row 93** → SC-4(j) — naming the scored set is part of constituting the partition over it.
Each redistribution is a natural reading of the receiving clause, not a stretch. **If the author
prefers the gate-extent clause standalone — and there is a case for it, since "what the gate consists
of" is a different question from "who may declare it" — the count is 13, one over the ceiling.** The
author should choose; K1 does not treat 12 as a constraint that outranks clarity.

**F-3 — SC-4 CARRIES 19 OF THE 76 ROWS. IT IS THE SET'S PRESSURE POINT.**
This is not padding: J1 §2 identified the three-class partition as **one object carrying ~30 rules by
construction**, and SC-4 is that object. It is drafted with ten lettered limbs so it stays readable,
but it is by some distance the longest clause. **Split option, at a cost of +1 clause (13, or 14 with
F-2's):** SC-4a = the derivation rule, the class definitions, precedence, the edge readings, and the
exclusion grounds (rows 17, 19, 29, 31, 32, 33, 34, 50, 99, 103, 105); SC-4b = the publication and
maintenance discipline — enumerated lists, no residue, the printed check, one class per unit,
re-derivation, disagreement halts, the named constant, N (rows 30, 35, 36, 48, 59, 93, 98, 108).
The split is clean; K1 does not take it, in order to hold the ceiling.

**F-4 — ROW 14 IS ONLY HALF SCHEMA-COVERABLE, AND THE OTHER HALF IS ALREADY DRAFTED.**
SC-2(d) registers what a reference anchor **is** (recomputed from committed bytes, enumerated entries,
per-entry tolerance, non-widenable, deviation is a stop-and-report). It **cannot** retire the specific
registered figures at `PREREG.md` line 445 — that is an instance-level supersession of registered
text, which is H1 hunk **H2**'s job and is correctly there. The accounting marks row 14 COVERED BY
SC-2(d) because the *rule* it carries is schema; **the amendment does not discharge row 14 unless H2
is applied with it.** Flagged so no one reads "covered" as "done".

**F-5 — SC-10 COLLIDES WITH §6.1's CLOSED ENUMERATION ("Five bodies of data").**
Rows 85 and 123 register a body of data attached to the acceptance fixture that enters no denominator
and no freeze. §6.1's table is headed **Five bodies of data** and its columns are exactly "Defaults
chosen on it?" and "Detection rates published from it?" — neither of which expresses "enters no
acceptance denominator". Two dispositions, and the author must pick:
**(i)** amend §6.1's heading and add a sixth row (clean, but it is a change to a registered table that
the conformance walk does not cite, i.e. a scope expansion of the same kind H1 flags for C1/C2); or
**(ii)** draft SC-10 as written above — the diagnostic is *not* a sixth body but data attached to the
fixture's existing row, exempt from the arithmetic by declaration. K1 drafts (ii) and marks the
supersession as "AMENDED IN FORM", because (ii) touches less registered text. **Neither option is
free, and (ii) leaves §6.1's table looking exhaustive when it is not.**

**F-6 — `UNSCORED` WOULD HAVE REPEATED `waived`'s DEFECT, AND SC-6(b) IS THE FIX.**
§A.12 exists because `waived` was registered as a state **with no entry condition** (H1 §(iii) item 12
reports the gap and declines to invent one). A new state added the same way would inherit the same
defect within one amendment of diagnosing it. **SC-6(b) therefore supplies an entry condition:** a
unit may be reported `unscored` **only** from the declaration's pre-run unscored ledger, by name, with
its ground. This is a **drafting decision K1 made and is flagging**, not a walk citation — the
declaration's §A.6.3 and §13(g) state the state's *consequences* and never its entry condition.
**Consequence the author should note — SUPERSEDED, DELTA R35/B3.** As drafted this read: "§7.7's
`waived` still has no entry condition after this amendment, and now stands out as the only state in
the table without one." That was true of the set as K1 left it. **SC-12(w) closes it**: `waived` now
carries an entry condition, and no state in §7.7's table is left without one.

**F-7 — SC-12 REGISTERS THE FLOOR'S VOCABULARY AND DOES NOT DISCHARGE R22's LIVE OBLIGATION.**
Per J1 §6.2 the answer to "is R9's map-scored criterion 3 the §10.2 replacement?" is **NO**, on two
independent grounds. SC-12 defines the word the floor uses; it supplies **none** of line 1033's three
required parts. Still owed, and **not closable by any schema clause** because a threshold and a
denominator are choices, not schemas: a replacement for §10.2 criterion 2 stated as such; a **unit**
for the non-zero-proof-yield limb; a **threshold** (a number — none exists anywhere); a
**denominator**, nominated explicitly; and an **L2a limb** that keeps L2a unwaived under SC-12's own
limbs (i)–(iii), given that rows 44 and 101 place its findings outside this gate. **Note the
interaction with SC-5(e):** SC-5(e) registers the jurisdiction boundary that puts a detector's
findings outside this gate — and SC-12 registers that a criterion satisfiable without that detector
has waived it. **The two clauses are consistent only because they govern different criteria**; if the
replacement criterion is ever drafted over this gate's map, they collide, and the collision is
resolved by the replacement, not by these clauses.

**F-8 — FOUR DUPLICATE PAIRS COLLAPSE TO ONE LIMB EACH, AND THE DECLARATION'S SECOND COPIES MUST
BECOME CITATIONS.** Rows **44 / 101** (L2a jurisdiction, → SC-5(e)); rows **92 / 110** (forbidden use,
→ SC-10(d)/(e)); rows **85 / 123** (non-gated diagnostic, → SC-10(a)/(b)); rows **34 / 50**
(unconstructibility reading, → SC-4(d)(ii)); rows **72 / 124** (both-branch informational, → SC-1(f));
rows **39 / 107** (attribution, → SC-5(b)). Each pair is accounted separately in §2 (as required — one
disposition per row) but is **one clause limb**. After this amendment, the declaration's second copy
of each is a **duplicated authority under §0.2.1 line 77** and must become a citation. **That is six
edits to `AVAILABILITY_DECLARATION.md` this amendment creates and does not perform** — out of scope
for K1 by the hard boundary, and named here so it is not lost.

**F-9 — THREE NEW REGISTERED SURFACES, NOT THREE INSERTIONS.** SC-6 (a coverage state), SC-7 (an input
surface), SC-11 (a control over aggregation) each create an object `PREREG.md` does not contain. They
are the reason the clause count cannot go much below 12, and they are also where CI risk lives:
**SC-6 touches `PREREG.md` line 855, which `tools/check_registration.py` may parse as a state
enumeration** (H1's verification found `_prereg_version`, `check_phase_arithmetic`,
`check_requirement_ids` and `sections_of` all safe for its own hunks, but **none of H1's hunks modified
line 855 itself — H8 inserted after the table**). **SC-6 modifies the table row.** The applier and the
registration checks must be re-run against a scratch copy before this clause is treated as safe. K1
did not run them (no file was written outside the scratchpad).

**F-10 — WHAT THE SCHEMA CLAUSES ADD THAT J1's BUCKETS DID NOT ASK FOR, DECLARED SO IT IS NOT
SMUGGLED.** Four sentences in the drafted set are **generalisations beyond any single row**, each
made to keep a clause from being weaker than the rows it carries. Named for the author to accept or
strike: **(1)** SC-3(a)'s "the declaration declares the cell key and names it explicitly" — without
it, "per declared cell" licenses an undeclared post-hoc cell definition (inherited from H1's H5, which
makes the same argument). **(2)** SC-4(a)'s "no classification of the scored set other than this
derivation enters any criterion" — rows 17 and 19 each forbid one classification; the generic form
forbids all of them. **(3)** SC-8(a)'s "an object the gate consumes and the enumeration omits is a
defect in the enumeration, not an object outside the freeze" — row 121 requires exhaustiveness but
does not say what happens when it fails. **(4)** SC-5(d)'s "where two criteria would otherwise
adjudicate the same finding on the same ground, the declaration states which one governs" — row 100
routes four specific cases; the generic form requires the declaration to route all of them. Each is
the stronger reading, which SC-9(e) requires, but each is K1's drafting rather than a row's content.

---

## 6. CLAUSE COUNT, STATED PLAINLY

| | Count |
|---|---|
| **Schema clauses drafted (delivered)** | **12** |
| Target range | 8–12 |
| Over the ceiling | **0** — but see **F-2**: the set was 13 before three rows were redistributed, and 13 is defensible |
| Split options that would raise it | **F-3** (SC-4 → SC-4a/SC-4b): +1 |
| GATE-CRITICAL rows covered by a clause | **75 of 76** |
| GATE-CRITICAL rows the schema cannot cover | **1** — row 28 (**F-1**), closable only by an explicit class C amendment of `PREREG.md` line 449 |
| NON-GATE rows reclassified INTEGRITY → PREREG per R25 | **7** (rows 8, 9, 18, 22, 23, 27, 126) |
| NON-GATE rows remaining PRACTICES | **19** |
| INSTANCE rows confirmed staying in the declaration | **36 of 36** |

**Clause index.** SC-1 declared availability model · SC-2 fixture composition · SC-3 declared
ground-truth map and scored population · SC-4 the partition and criterion 1's denominator · SC-5
adjudication routing · SC-6 `UNSCORED` · SC-7 gate input surface · SC-8 ex-ante declaration and the
freeze · SC-9 declaration integrity and interpretation · SC-10 declared non-gated data · SC-11 zeros,
absences and pass claims · SC-12 the replacement-criterion floor and "waived".

**Coverage of R24's named minimum, checked one by one:**

| R24 requirement | Clause | Status |
|---|---|---|
| Criterion 3 scored against the declared ground-truth map, generically defined, declared and frozen before any detector runs | **SC-3** (+ SC-8(a)(c)) | Covered. The map is defined as a per-side, per-declared-class, per-declared-cell enumeration of expected findings; the cell key is declared, not hard-coded. |
| Criterion 1's denominator derived from the declared availability model by the declaration's own stated derivation rule, itself declared ex ante | **SC-4(a)** (+ SC-8(c)) | Covered. The rule is required to be stated ex ante and in full; the classes are derived, never assigned. |
| `UNSCORED` added to line 855's coverage-state list, as a new STATE with its semantics | **SC-6** | Covered. Line 855 verified (§0): six states, `UNSCORED` absent. Drafted as a state with semantics, an entry condition, two levels, and gate consequences — and touching §8.2 line 915 as well, which the six-state row alone would have missed. |
| The gate's input surface | **SC-7** | Covered. |
| Declaration-integrity and freeze requirements, including never-adjust-evidence, supersession / working-resolution authority, and the stronger-reading interpretation rule | **SC-8** + **SC-9** | Covered. All three R25-named rules are in SC-9 — (b), (d) and (e) respectively. |

---

## 7. LIMITS OF THIS PASS

1. **Nothing was applied and nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`,
   `DESIGN.md` and `HISTORY.md` are untouched; no git command was run; the archive was not read. The
   only file written is this one, under the permitted scratchpad path.
2. **Insertion points are line numbers as read this pass** against the live 1,099-line `PREREG.md`.
   Line 855 and line 915 were read directly and are quoted verbatim in §0. If any other item edits
   `PREREG.md` before these clauses are applied, every anchor must be re-derived. **No anchor-match
   count was verified by tooling this pass** — H1's applier convention (refuse on zero or multiple
   matches) should be used.
3. **The 76 / 26 / 36 buckets are J1's and were not re-litigated.** K1 disposes of them; it does not
   reclassify any row between buckets. Where K1 disagreed with a bucket's *consequence* — rows 8, 9,
   18, 22, 23, 27, 126 — it applied **R25**, which is a routing rule over J1's buckets, not a
   reclassification of them.
4. **The clause text is drafted, not applied, and is not verified against `tools/check_registration.py`
   or `tests/registration`.** F-9 names the specific risk (SC-6 modifies the line 855 table row, which
   no earlier hunk did). Both gates must be re-run on a scratch copy before any application.
5. **Six edits to the declaration that this amendment implies are named (F-8) and not performed** —
   the hard boundary forbids it, and they are not K1's to make.
