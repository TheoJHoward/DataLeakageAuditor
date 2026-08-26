# SCHEMA SET ADOPTION — SC-1 … SC-13c AS CORRECTED (Q1 + Q2 + Q3), READY TO APPLY

**This file supersedes, for the clause text only, `K1_SCHEMA_CLAUSES.md` (SC-1 … SC-12) and
`SC13_SPLIT_ABC.md` (SC-13a / SC-13b / SC-13c and the SC-12 delta).** Neither prior file was
edited; both stand as the superseded record. Where this file is silent, K1's §2 accounting table
(76 rows), §3 (R25 disposition), §4 (36 instance rows), §5 findings F-1 … F-10 and §6 clause count,
and the split file's Part 2 (mapping table), Part 4 (P2 disposition), Part 6 (P4 regressions) and
Part 7 (seam statement) stand and are cited, not reproduced. **The K1 accounting is unchanged by
anything in this file** — no row moves, no tally changes.

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md`
are untouched. **No git command was run.** The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025`
was not read. The only file written this pass is this one.

**Read state this pass:** `PREREG.md` = **1,099 lines**; `AVAILABILITY_DECLARATION.md` = **3,684
lines** — both counted by tool this pass (`wc -l`), matching every prior round. Every anchor below is
a line number read directly this pass. Files read: `K1_SCHEMA_CLAUSES.md` (1,221 lines, in full);
`SC13_SPLIT_ABC.md` (785 lines, in full); the P7 verification record at `tasks\wb31ayqgv.output`
(`result.p7`, all 17 findings and 4 blockers, in full); `PREREG_v30a_DIFF.md` (hunk table lines
14–42, H7 at 336–373, H8 at 377–398); `PREREG.md` lines 77, 79, 93–99, 301, 318, 320, 429–470, 570,
756–762, 800–832, 848–860, 892, 915, 961, 1022, 1026–1042, 1054; `AVAILABILITY_DECLARATION.md`
§A.8 (1407–1436), §A.12 (1525–1598). **Read, not edited.**

**What this file contains, in the order the brief lists it:**

- **PART 1** — the complete schema set SC-1 … SC-13c **as corrected, verbatim, ready to apply**, plus
  the line-816 pointer and the revised amendments-block recording text.
- **PART 2** — the **Q1 record**: both normative edits, before/after; the R24-table-miss note with the
  entry quoted; `PREREG.md` line 818 verbatim; the principle.
- **PART 3** — the **Q2 corrections table**: clause names into headings; the line-759/760 anchor;
  waiver authority re-cited to SC-12; the line-816 pointer.
- **PART 4** — the **Q3 R24 scan table**: every clause SC-1 … SC-13c, limb by limb, every hit or
  "scanned, no breach", normative-text hits distinguished from DATA-block examples.
- **PART 5** — the **change ledger**: every edit in this file against the two prior files.
- **PART 6** — carried open: P7 items outside Q1–Q3, and pre-existing application gaps, reported not
  solved.

---

## 0. TWO CONVENTIONS THIS FILE ADDS, STATED ONCE

**0.1 The heading tag `[SC-n]` — how a clause name resolves in applied `PREREG.md`.** Every clause's
applied heading below ends with its clause name in square brackets — `[SC-1]` … `[SC-12]`, `[SC-13a]`,
`[SC-13b]`, `[SC-13c]`. **Resolution rule:** wherever applied clause text says "SC-n", it means the
clause whose heading carries the tag `[SC-n]`; "SC-n(x)" means the lettered limb (x) inside it. The
tag is one token per heading, adds no semantics, and is the whole of the fix for Q2(a). It is applied
**uniformly to SC-1 … SC-12 as well as SC-13a/b/c**, because K1's applied clause bodies already
cross-cite by clause name — SC-3(b) "(SC-6)", SC-3(h) "(SC-8)", SC-4(b) "(SC-6)", SC-5(a) "(SC-4)" and
"(SC-3)", SC-6(b) "see SC-12", SC-7(e) "(SC-8)", SC-10(a) "SC-8", SC-11(g) "(SC-6)", SC-12 items (4)
"(SC-6)" and (5) "(SC-9(c), SC-9(e))" — and those citations dangle in applied text for exactly the
reason P7 gave for SC-13a/b/c. The author may strike the tags on SC-1 … SC-12; if so, every citation
just listed must be resolved to a section number at application instead. **Why not limb tags alone
for SC-13a/b/c:** the limb tags (a1)–(a3), (b1)–(b4), (c1)–(c7) are globally unique and would let a
reader resolve "SC-13c(c3)" by searching for "(c3)", but bare "SC-13b" (SC-13a's opening: "SC-13b's
admissibility test is applied first") has no limb to search for; the heading tag is required for
those, and one convention for all clauses is cheaper than two.

**0.2 What is applied text and what is apparatus.** Following K1's convention, only **THE CLAUSE**
block (and, where a clause supersedes registered text, the **SUPERSESSION MARKER** text placed at the
superseded site) enters `PREREG.md`. **REGISTERS**, **INSERTION POINT**, **DATA THE DECLARATION MUST
SUPPLY**, **ROWS COVERED**, and any *Instance record* note beneath a clause are drafting apparatus and
are not applied. The Q3 scan (Part 4) is run over both, and reports each hit's location.

**Application order, one tag.** The split file's order is preserved and is the only order any prior
file fixed: **SC-12 (revised) → SC-13a → SC-13b → SC-13c**, then the **line-816 pointer** (Part 1,
§13c-P) and the **amendments-block recording text** (Part 1, §AB). For SC-1 … SC-11 no prior file
fixed an order; the suggestion — not a decision — is ascending anchor order (SC-9 §0.2.1 · SC-1 §2.9
· SC-10 §6.1 · SC-2, SC-3, SC-4, SC-5, SC-7, SC-8 in §6.2 · SC-6 §7.7/§8.2 · SC-11 §7.8/§8.6 · SC-8's
§11 pointer), so that each clause's anchor is re-derived only against edits above it. Anchors are line
numbers against the live 1,099-line `PREREG.md`; **once any earlier edit lands, every later anchor must
be re-derived** — H1's applier convention (full-line match; refuse on zero or multiple matches) is the
one to use. **No tooling was run against these clauses this pass** (see Part 6).

---

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
defect — stands as the drafting record for limb (b); the reference to it is kept here, in
apparatus, and removed from the applied clause text. **F-6's second half is now spent:** it recorded
that §7.7's `waived` would still have no entry condition after this amendment. **SC-12(w)
supplies one**, so that consequence no longer holds, and the sentence asserting it is struck rather
than softened.)*

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
the §7.7 pointer after line 856 — **redrafted at DELTA R35/B3; H1's H8 draft is SUPERSEDED** and may not be applied, because it asserts that the entry condition for the `waived` coverage state is not defined by this registration, which SC-12(w) makes false. The operative pointer text is Y3 §6.3's.

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

# PART 2 — Q1: THE TWO NORMATIVE EDITS, ON THE RECORD

## Q1(i) — SC-13c(c5)(i): the fixture's declared cell key stripped from PREREG schema text

**BEFORE** (`SC13_SPLIT_ABC.md` lines 336–343, verbatim):

> **(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
> ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461 and that
> declaration §A.8 records per working resolution R9. **Its scoring rule and its three dispositions
> are SC-3(b)'s, held by citation and not restated here**; its map is indexed as SC-3(a) declares —
> **per side, per declared violation class, and per declared cell** of the declared scored
> population, which in this fixture's instance form §A.8 states as per-side, per-class,
> per-instrument-month. **It is never the pre-amendment prohibition on any finding on the corrected
> fixture**, and this clause may not be read against that text.

**AFTER** (Part 1, SC-13c(c5)(i)):

> **(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
> ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461. **Its
> scoring rule and its three dispositions are SC-3(b)'s, held by citation and not restated here**;
> its map is indexed as SC-3(a) declares — **per side, per declared violation class, and per
> declared cell** of the declared scored population. **The cell key is the declaration's to supply,
> not this clause's to state**: SC-3(a) requires only that a key exist, be declared and named, and
> be frozen with the map before any detector runs (SC-3(h), SC-8), and this clause names no key.
> **It is never the pre-amendment prohibition on any finding on the corrected fixture**, and this
> clause may not be read against that text.

**What moved, and where.** Two deletions from the applied text: (1) "and that declaration §A.8 records
per working resolution R9" — a reference to this fixture's declaration section and to one of its
working resolutions; (2) "which in this fixture's instance form §A.8 states as per-side, per-class,
per-instrument-month" — the declared cell key itself. One sentence added, generic: the key exists, is
declared and named, and is frozen — which is exactly what SC-3(a) and SC-3(h) already require, cited
not restated. Both deleted facts survive in the *Instance record* note beneath SC-13c (apparatus, not
applied), which cites `AVAILABILITY_DECLARATION.md` §A.8 line 1416 as the instance's home. **Why this
is a breach and not a citation:** SC-3(a) makes the cell key instance data by definition ("The
declaration declares the cell key — the unit it declares the fixture to be partitioned into — and
names it explicitly"); K1's own R24 test is "would this clause make sense in a registration that had
never seen this fixture?" — and a registration that never saw this fixture has no §A.8, no working
resolution R9, and no instrument-month axis. Naming SC-3(a)'s *axes* ("per side, per declared
violation class, per declared cell") is citation of a schema key's shape; naming *this fixture's
values* for those axes is the instance.

**THE R24 TABLE MISSED IT — recorded explicitly.** The split file's own R24 re-test (`SC13_SPLIT_ABC.md`
Part 6, "The new text — the R24 re-test for the split", lines 713–731) is headed by exactly the right
question:

> | New clause / limb | Source | Names a column, count, instrument, class, or boundary? | Would it make sense on a different fixture? |

and its row for this limb (line 729) reads, verbatim:

> | SC-13c(c5) floor limbs | old (g), restatement replaced by citation | **No — cites SC-3(b)'s dispositions and SC-3(a)/§A.8's indexing axes by name; states none of the map's contents and none of the rule's operative text** | Yes |

That row **saw the §A.8 axes** — it says "SC-3(a)/§A.8's indexing axes by name" — and classified them
as citation, answering "No" to a question whose text names "instrument" and "Yes" to whether the limb
would make sense on a different fixture. A limb that says "per-instrument-month" names an instrument
axis, and would not make sense on a fixture with no instruments; both answers were wrong for the
sub-clause, and the row was written in the favourable direction. This is the genus N6 called
regression 4 (a self-assessment mischaracterizing the assessed text) recurring one round after it was
fixed, exactly as P7 reported. **Consequence for method:** the R24 self-check must be run on the
*applied text* token by token, not on the drafter's description of it — which is what Part 4 of this
file does, and why every row there quotes the token that was checked.

## Q1(ii) — SC-13b(b3): the line-818 characterization dropped

**`PREREG.md` line 818, verbatim, read this pass** (the whole paragraph, so the misreading is on the
record beside the sentence that was quoted):

> **"Scope-eligible case" means every labelled case in the body, clean cases included.** §7.4 defines scope-eligibility for a *unit*; applied to a case it needs saying, and the alternative — counting only cases that carry a labelled leaking pair — flips ten metrics and a gate on a concrete body: a combination `not_applicable` on every leaking case but `completed` on a clean one would be suppressed, hiding a clean-case finding rate that is a genuine measurement. Suppression exists to remove numbers that measure nothing, never to remove one that does. A yield computed over a combination that never applied is not a measurement of the tool: on a corpus of 25 labelled cases it reads `0/25`, which is indistinguishable in print from a mode that ran everywhere and found nothing. The `not_applicable` count carries that fact honestly; the yield does not. *(This is the cost of the strict reading above, and it is paid here rather than left in the numbers.)*

**What line 818 holds, in its own order.** (1) A general principle: "Suppression exists to remove
numbers that measure nothing, never to remove one that does." (2) An **applied holding for exactly the
state (b3) disposes** — a yield over a never-applied combination: it "is not a measurement of the
tool", reads (on 818's own 25-case example) `0/25`, "indistinguishable in print from a mode that ran
everywhere and found nothing", and "the `not_applicable` count carries that fact honestly; the yield
does not." Line 818 is the registered *rationale for line 816's suppression* of this very yield. The
clause quoted (1) and claimed 818 "decides this rather than fighting it", while (2) — the two
sentences immediately after the one quoted — decides it the other way.

**BEFORE** (`SC13_SPLIT_ABC.md` lines 220–225, the sentence in question, verbatim):

> Line 818's own principle decides this rather than fighting it — "Suppression exists to remove
> numbers that measure nothing, never to remove one that does" — and at a kill criterion this zero
> measures exactly what the criterion asks: a combination that never applied cannot separate the
> fixture sides, and a gate suppressed on that fact is a detector waived on it (§A.12's head: a
> detector is waived when its result is made "incapable of changing the criterion's outcome").

**AFTER** (Part 1, SC-13b(b3)):

> **The exception rests on two grounds and on no other.** *First*, it is a class C change to how line
> 816 reads at this one criterion, made on this amendment's own authority and recorded in the v30a
> amendments block (SC-13c(c2)). *Second*, this is a kill criterion over the detectors' capability: a
> combination that never applied on a declared side cannot separate the fixture sides, so a gate
> suppressed on that fact is a detector waived on it (SC-12's definition: a detector is waived when
> its result is made "incapable of changing the criterion's outcome"), and line 1035 forbids the
> waiver.

**And at the authority site**, SC-13c(c2) gains one sentence: "**The exception rests on this
amendment's class C authority and on that capability ground; it does not rely on `PREREG.md` line
818, whose text stands as registered.**" The amendments-block recording (§AB) carries the full
acknowledgment: that line 818's applied holding points the other way for this state, and that the
amendment departs from it for these quantities expressly and on its own authority. Consequentially,
SC-13b's SUPERSESSION MARKER no longer lists 818 among the lines (b3) relies on, and the split file's
Part 3 commentary sentence — "The exception is grounded in line 818's own registered principle rather
than against it" — is withdrawn and not reproduced.

**The principle, stated.** *A clause whose justification misreads a registered holding is weaker
than one that claims less.* The exception was never in need of line 818's blessing: it is a class C
amendment, and class C amendments change what registered text does on their own authority (§0.2.1
line 93; SC-13c(c2) says so in terms). Borrowing 818's principle bought nothing the amendment did not
already have, and it cost something real: a reader who follows the citation finds the adjacent
holding, and from that point on every other citation in the family carries a discount. A clause that
says "this departs from 818's holding, on our authority, for these quantities only" can be checked
and found true; a clause that says "818 agrees" can be checked and found false. The weaker-sounding
claim is the stronger clause.

---

# PART 3 — Q2: ANCHOR AND CITATION CORRECTIONS

| # | Item | Where it stood | What was wrong | Correction made in Part 1 |
|---|---|---|---|---|
| Q2(a)-1 | **Clause names into applied headings — SC-13a/b/c** | SC-13a heading "2. Where the fixture is semantically ambiguous … — v30a, operative on the ambiguity branch." (split line 88); SC-13b "ADMISSIBILITY FOR THE CRITERION ABOVE — v30a." (line 182); SC-13c "INTERACTIONS OF THE CRITERION ABOVE — v30a." (line 280) | The names SC-13a/SC-13b/SC-13c are used pervasively in applied text ("SC-13b's admissibility test is applied first"; "the set SC-13c(c3) pins") and appear in no heading; after application nothing in `PREREG.md` is labelled SC-13a/b/c. Limb tags (a1)–(c7) are globally unique and would resolve "SC-13c(c3)", but bare "SC-13b" has no limb to search for. | Each heading now ends with its tag: "… operative on the ambiguity branch. **[SC-13a]**"; "ADMISSIBILITY FOR THE CRITERION ABOVE — v30a **[SC-13b]**. Tested before …"; "INTERACTIONS OF THE CRITERION ABOVE — v30a **[SC-13c]**." Resolution rule stated once at §0.1. |
| Q2(a)-2 | **Same, extended to SC-1 … SC-12** | K1 headings carry no name; K1 applied bodies cite "(SC-6)" (SC-3(b), SC-4(b), SC-11(g), SC-12 item 4), "(SC-8)" (SC-3(h), SC-7(e), SC-10(a)), "(SC-4)/(SC-3)" (SC-5(a)), "see SC-12" (SC-6(b)), "(SC-9(c), SC-9(e))" (SC-12 item 5) | Same defect, same genus, more sites — P7 named K1 line 251 as the precedent. | `[SC-1]` … `[SC-12]` appended to each applied heading. Author may strike these; if so, every citation just listed must be resolved to a section number at application. |
| Q2(a)-3 | **Dangling drafting reference in SC-6(b)** (found by the scan) | K1 line 502: "*(This entry condition is stated explicitly because §7.7's `waived` was registered without one — see SC-12 and finding F-6.)*" | "finding F-6" is a K1 finding; nothing in applied `PREREG.md` is labelled F-6. Same genus as Q2(a). | Applied text now reads "— see SC-12.)"; the F-6 note is kept beneath SC-6 as apparatus. |
| Q2(b)-1 | **`Runtime, promoted` row anchor — SC-13c(c3)** | Split line 312: "§7.1's `Runtime, preserving` and `Runtime, promoted` rows (line 759)" | `PREREG.md` lines 758–761 read this pass: **758** = the table's separator row `\|---\|---\|---\|`; **759** = the `Runtime, preserving` row ("L2a, L3.1 — proof yield; conditional feature-cohort recall; …"); **760** = the `Runtime, promoted` row ("L2a, L3.1 — evidence yield and the same family below the first row, computed over dtype_promoted findings only"); **761** = the `Code-site, two modes` row ("L1.2, L1.3 — Deferred to prereg-static …"). Lines 759, 760 and 1039 are quoted verbatim in a fenced block under SC-12's *Instance record*. The promoted row is line **760**. | "(lines 759 and 760)". |
| Q2(b)-2 | **Same anchor — SC-12 governed-set paragraph (Part 5 Delta 2)** | Split lines 563–564: "`PREREG.md` line 759's `Runtime, preserving` row and its `promoted` companion" | Same: the companion is line 760, not an unanchored companion of 759. | "`PREREG.md` line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row". |
| Q2(b)-3 | **Same anchor — the split file's Part 5 header** | Split lines 531–536 quote line 759 only, headed "The three registered sites the revised SC-12 pins to — the SAME clauses SC-13c(c3) cites" | Quotes one of the two §7.1 rows and calls §A.12 the third "registered site" (P7: (c3) cites two sites, not three; §A.12 is declaration text). Commentary, superseded. | Not reproduced. The SC-12 *Instance record* note in Part 1 quotes **759, 760 and 1039** verbatim as the three `PREREG.md` sites, and lists §A.12 separately as corroboration. |
| Q2(c)-1 | **Waiver authority — SC-13b(b3)** | Split lines 224–225: "(§A.12's head: a detector is waived when its result is made 'incapable of changing the criterion's outcome')" | §A.12 is declaration text, provisional until the tag; the same tag registers SC-12's identical definition into `PREREG.md` first, physically adjacent to SC-13b's own insertion point. The family's own rule — split Part 5 Delta 2 (read this pass): §A.12 is "corroboration, not the source"; the corrected file's Part 5.2 and N6's blocker 1 say the same, per P7's record (not re-read this pass). | "(SC-12's definition: a detector is waived when its result is made 'incapable of changing the criterion's outcome')". SC-12's head reads, verbatim: "A detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or reported in any way that makes the detector's own result **incapable of changing the criterion's outcome**." |
| Q2(c)-2 | **Waiver authority — SC-13c(c2)** | Split lines 302–303: "a detector waived on it — §A.12's head and limb (iii) — and line 1035 forbids the waiver" | Same. | "— SC-12's definition, head and limb (iii) —". SC-12 limb (iii), verbatim: "the criterion can be satisfied by another detector's output alone". |
| Q2(c)-3 | **DEVIATIONS/WR prohibition — SC-13c(c1)** | Split line 291: "(line 1033; §A.12 item 5)" | Same source inversion; SC-12 item (5) is the registered site: "**A working resolution or a `DEVIATIONS.md` entry cannot do it** (SC-9(c), SC-9(e))." | "(line 1033; SC-12 item (5))". |
| Q2(c)-4 | **Waiver authority — amendments-block recording (§AB)** | Split lines 480–481: "(§A.12 head and limb (iii))"; lines 489–490: "(§0.2.1 line 95; §D.3; §A.12 item 5)" | Same; the amendments block is a record and may corroborate from the declaration, but must lead with the registered source. | "(SC-12's definition, head and limb (iii); the declaration's §A.12 states the same definition and corroborates)"; "(§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3 and §A.12 item 5)". |
| Q2(c)-5 | **§A.12 named in SC-12's applied text** | Split lines 565–566 (Delta 2): "The declaration's §A.12 states the same membership and is corroboration, not the source." | Right rule, wrong location: a `PREREG.md` schema clause naming this fixture's declaration section is the R24 breach of Q1(i)'s genus (a registration that never saw this fixture has no §A.12), even when the sentence's content is that §A.12 is not the source. | Applied text: "Where the fixture's declaration states the same membership, it is corroboration, not the source." The §A.12 citation (lines 1543–1544, quoted) moves to SC-12's *Instance record* (apparatus). |
| Q2(c)-6 | **Pointer at line 816's own site** | Absent. K1's SC-12 has H8's pointer at §7.7 line 856 so `waived`'s second site is not read bare; SC-13c(c2) left line 816 byte-exact and unannotated, its exception ~220 lines away inside §10.2's block. | An implementer of §7.2.1 meets an unconditional suppression rule with no signal that a scoped exception exists; suppression applied at metric level would leave §10.2's gate nothing to read (P7). | **§13c-P** drafted (Part 1): one paragraph after line 816, modelled on H8 — names where the exception lives, its scope, that everything else governs as registered, and that the 816/830 relationship is recorded and unchanged. SC-13c gains a second INSERTION POINT; SC-13a's marker names the pointer. |
| Q2-extra | **SC-13b marker's relied-on list** | Split line 175: "The registered lines it relies on — 816, 818, 830, 570 — stand byte-exact and are cited." | After Q1(ii), (b3) cites 818 nowhere. | "— 816, 830, 570 —". |

---

# PART 4 — Q3: THE SYSTEMATIC R24 SCAN, EVERY CLAUSE, EVERY LIMB

**Method.** Every element of every clause SC-1 … SC-13c — heading, opening, each lettered limb, the
supersession marker, the DATA block, and this file's two *Instance record* notes — was read token by
token against the brief's list: column counts (35, 45, 11, 22, 2, 28), instrument names (zc, nq, es,
…), instrument-months, cell keys, "the 35-column set", map dimensions (48, 960, 984), the ZC LightGBM
trio or any AUC, row counts (338,159 …), event-class names, `ts_floor`, `mid(t)`, phase5/phase7
script names, and *any figure true only of this fixture* — to which this scan adds, on Q1(i)'s
reasoning, **references to this fixture's declaration by section number or working-resolution id**
(§A.n, §D.n, §13, R9 …), because a registration that never saw this fixture has none of them. A
mechanical grep for the listed tokens over both prior files' clause regions was run first (hits: none
in K1's clause bodies; the five declaration-section references and the cell key in the split's clause
bodies) and then every limb was read by eye, because the grep cannot see "a figure true only of this
fixture" stated in words.

**Not breaches, and why — stated once so the table can cite it:** (V1) **registration vocabulary** —
terms `PREREG.md` v30 itself registers and any fixture would meet: `column_roles`, `ties`,
`fixture_contaminated` / `fixture_corrected` (§6.2 lines 460–461, 464), the identity control, the
manifest, L2a / L3.1 (§4 rows, lines 318, 320), `preserving` / `promoted` (§3.1 line 301), PROVEN /
REVIEW, the §6.6 states (`not_applicable` line 570 …), §7.7's `waived`, feature-cohort pair, proof
yield, evidence yield, scope-eligible, the labelled hypothetical declaration (line 449), Phase 0 /
Phase 1 (§9–§10), `DEVIATIONS.md`, `prereg-v30` / `prereg-v30a` (line 95), `VALIDATED_CONFIG`; (V2)
**registered text quoted verbatim inside a supersession marker** (the retired v30 sentence is
reproduced, marked superseded — H1's convention); (V3) **generic illustrative nouns** that name a
*kind* of thing and no fixture value — "a boundary, a gap, a session edge", "a slice, a filtered
variant, a projection", "a manifest, a measurement record, a capture" — where `PREREG.md` already
uses the same nouns generically (session gaps line 383, boundary passim, lagged lines 156/225/512);
(V4) **registration arithmetic** — "a fifth [criterion]" against §6.2's four registered criteria,
"five bodies" against §6.1's registered heading, "six states" against line 855's registered row.
**Location codes:** **A** = applied clause text · **M** = supersession-marker text placed at the
superseded site · **X** = apparatus (REGISTERS / INSERTION POINT / DATA / ROWS / Instance record —
not applied).

## 4.1 The scan table

| Clause | Element | Loc | Tokens checked, and the finding | Verdict | Replacement |
|---|---|---|---|---|---|
| **SC-1** | heading + opening ("Six requirements follow") | A | "six" counts the clause's own limbs (a)–(f) | scanned, no breach | — |
| SC-1 | (a) measured, not intended | A | "documented value", "measured value", "artifact" — no value named | scanned, no breach | — |
| SC-1 | (b) representation named | A | "as constructed / as fed to the model", "transform" — no transform named (no "lag", no "shift") | scanned, no breach | — |
| SC-1 | (c) role is a position | A | `column_roles` (V1), "lattice" (generic); no role value named (no `at_bar_close`, no `at_timestamp`) | scanned, no breach | — |
| SC-1 | (d) units declared | A | "unit", "term of a registered formula" — no unit named (no "bars", no "positional") | scanned, no breach | — |
| SC-1 | (e) staleness | A | `ties` (V1) | scanned, no breach | — |
| SC-1 | (f) one branch scored | A | `ties` (V1) | scanned, no breach | — |
| SC-1 | marker (§2.3 line 205; §2.4 lines 220–222) | M | the registered formula `a(y_j) = …` quoted (V2); "duration" is the *registered assumption* being superseded, not the fixture's unit | scanned, no breach | — |
| SC-1 | INSERTION POINT / DATA | X | quotes line 266 ("every L2a and L3.1 finding …") (V1/V2); DATA generic | scanned, no breach | — |
| **SC-2** | heading | A | — | scanned, no breach | — |
| SC-2 | (a) enumerated set | A | "by side", "provenance" | scanned, no breach | — |
| SC-2 | (b) composition is class C | A | `DEVIATIONS.md` (V1) | scanned, no breach | — |
| SC-2 | (c) pre/post licence | A | "column set, label set, row population, evaluation population" — kinds, no counts | scanned, no breach | — |
| SC-2 | (d) reference anchor | A | "reference quantity", "per declared horizon and side", "tolerance" — no AUC, no interval, no horizon named | scanned, no breach | — |
| SC-2 | (e) moving between phases | A | "later-phase obligation" — no phase number | scanned, no breach | — |
| SC-2 | marker (lines 445, 450, 451; §10 line 992) | M/X | refers to line 445's "registered anchor pair" **without the figures**; "Phase 1 gate cell" (V1). Cites H1 hunks H2/H3/H4/C1 — drafting identifiers, see Part 6 item 4 | scanned, no breach | — |
| SC-2 | DATA | X | generic | scanned, no breach | — |
| **SC-3** | heading | A | `fixture` side, "DECLARED GROUND-TRUTH MAP" | scanned, no breach | — |
| SC-3 | (a) what the map is | A | "per side, per declared violation class, per declared cell", "the declaration declares the cell key … and names it explicitly" — the key is required to exist, **not stated** | scanned, no breach | — |
| SC-3 | (b) three dispositions | A | REQUIRED / FALSE POSITIVE / UNSCORED, "(SC-6)" | scanned, no breach | — |
| SC-3 | (c) whole population | A | "a boundary, a gap, a session edge" (V3) — kinds of awkward subclass, no cross-boundary count, no gap named | scanned, no breach | — |
| SC-3 | (d) declared terms, side-relative | A | "§2.9(b)" | scanned, no breach | — |
| SC-3 | (e) one scoring key | A | "re-aggregation, restriction, re-projection" | scanned, no breach | — |
| SC-3 | (f) derived subset | A | "a slice, a filtered variant, a projection" (V3) | scanned, no breach | — |
| SC-3 | (g) neither side clean | A | §2.7, §8.1 cited | scanned, no breach | — |
| SC-3 | (h) bar not lowered | A | "(SC-8)" | scanned, no breach | — |
| SC-3 | marker (line 461 retired; §10.1 line 1022) | M | v30 criterion 3 quoted verbatim incl. `fixture_corrected` (V2/V1); "strictly-post-decision violations" is availability vocabulary (a read after the decision instant), **no incidence figure** — the marker itself says "the measured incidence is instance data and lives in the declaration" (§A.8's 18/48, 111,334/580,944 appear nowhere) | scanned, no breach | — |
| SC-3 | INSERTION POINT / DATA | X | H5 quoted; DATA "the cell key and its name" — required, not stated | scanned, no breach | — |
| **SC-4** | heading | A | — | scanned, no breach | — |
| SC-4 | (a) denominator derived by rule | A | "evidence artifact's classification of how a unit was built" — generic (no "DAG", no "flavor", no line-446 count) | scanned, no breach | — |
| SC-4 | (b) three classes, N | A | table of REQUIRED / OUT OF JURISDICTION / UNSCORED; "N is the length of the REQUIRED list" — **no value of N**; "(SC-6)" | scanned, no breach | — |
| SC-4 | (c) precedence | A | "UNSCORED wins" | scanned, no breach | — |
| SC-4 | (d) edges, two forbidden readings | A | "(i) locality condition … declared lattice" (no "same-row book/clock"); "(ii) unconstructibility in some other rebuild" (no "T4") | scanned, no breach | — |
| SC-4 | (e) exclusion grounds | A | "degenerate unit that cannot carry a finding of the scored class" (no "dead-zero column"); "construction or lag treatment is declared UNRESOLVED" — "lag" is registration vocabulary (V3/V1: lines 156, 225, 512) | scanned, no breach | — |
| SC-4 | (f) publication discipline 1–3 | A | "three class sizes sum to the size of the declared scored set" — **no sizes** | scanned, no breach | — |
| SC-4 | (g) one gate class per unit | A | §0.2.1 line 79 cited | scanned, no breach | — |
| SC-4 | (h) re-derivation | A | — | scanned, no breach | — |
| SC-4 | (i) disagreement halts | A | — | scanned, no breach | — |
| SC-4 | (j) named, not counted | A | "the named constant the declaration declares, never by its cardinality" — **the constant is not named, the cardinality (35) is not stated** | scanned, no breach | — |
| SC-4 | marker (lines 459, 446) | M | "construction-taxonomy count recorded elsewhere in the fixture's evidence" — no count | scanned, no breach | — |
| SC-4 | DATA / ROWS | X | "N" as a required datum, no value; ROWS note cites K1 F-3 | scanned, no breach | — |
| **SC-5** | heading | A | — | scanned, no breach | — |
| SC-5 | (a) one criterion per finding | A | "(SC-4)", "(SC-3)" | scanned, no breach | — |
| SC-5 | (b) ground not name | A | "a unit has two grounds" — kinds, no unit named | scanned, no breach | — |
| SC-5 | (c) FP attaches to OOJ | A | "the clean-source criterion" = §6.2 criterion 2 (V1) | scanned, no breach | — |
| SC-5 | (d) charged twice only if independent | A | "criterion 3" | scanned, no breach | — |
| SC-5 | (e) jurisdiction between detectors | A | "a detector row outside the criteria this gate scores" — **no row named** (no "L2a label-base") | scanned, no breach | — |
| SC-5 | (f) sentinels under identity control | A | "an as-built artefact … present identically on every side", "signature" — **no artefact named** (no "wrapped values") | scanned, no breach | — |
| SC-5 | DATA | X | generic | scanned, no breach | — |
| **SC-6** | heading | A | `unscored` | scanned, no breach | — |
| SC-6 | (a) semantics | A | — | scanned, no breach | — |
| SC-6 | (b) entry condition | A | §8.2 cited; "see SC-12" (was "see SC-12 and finding F-6" — a dangling drafting reference, fixed under Q2(a)-3, not an R24 breach) | scanned, no breach | — |
| SC-6 | (c) two levels | A | "(SC-3)", "(SC-4)" | scanned, no breach | — |
| SC-6 | (d) not false positives | A | — | scanned, no breach | — |
| SC-6 | (e) pass prohibition | A | §8.2 | scanned, no breach | — |
| SC-6 | marker (line 855 row; line 915) | M | the registered six-state row quoted verbatim (V2/V4) | scanned, no breach | — |
| SC-6 | INSERTION POINT / DATA / F-6 note | X | generic; F-6 note names no fixture datum | scanned, no breach | — |
| **SC-7** | heading | A | — | scanned, no breach | — |
| SC-7 | (a) two things, one side | A | §2.3, §2.4, §2.9 | scanned, no breach | — |
| SC-7 | (b) never receives | A | "paired side", "stored predictions", "the declared ground-truth map" | scanned, no breach | — |
| SC-7 | (c) why the map is withheld | A | — | scanned, no breach | — |
| SC-7 | (d) one side at a time | A | — | scanned, no breach | — |
| SC-7 | (e) frozen | A | "(SC-8)" | scanned, no breach | — |
| SC-7 | DATA | X | generic | scanned, no breach | — |
| **SC-8** | heading | A | — | scanned, no breach | — |
| SC-8 | (a) freezes at the tag | A | — | scanned, no breach | — |
| SC-8 | (b) lists not counts | A | — | scanned, no breach | — |
| SC-8 | (c) checkable pre-run | A | "cohort", "restriction" — kinds | scanned, no breach | — |
| SC-8 | (d) scope choice | A | "a class set, a cohort, a population" — kinds | scanned, no breach | — |
| SC-8 | (e) not corrected in place | A | §0.2.1 line 99, §6.4 cited | scanned, no breach | — |
| SC-8 | (f) integrity chain | A | "the count of hashes is derived …, never stated as a literal" — **no count stated**; §0.2.1 line 97 | scanned, no breach | — |
| SC-8 | marker (line 480; §11 items 1–7) | M | "R23" — a workflow item id, drafting identifier (Part 6 item 4), not a fixture particular | scanned, no breach | — |
| SC-8 | DATA / ROWS | X | generic | scanned, no breach | — |
| **SC-9** | heading | A | — | scanned, no breach | — |
| SC-9 | (a) supplies data, creates no gate object | A | "a fifth" (V4 — §6.2 has four registered criteria) | scanned, no breach | — |
| SC-9 | (b) evidence never adjusted | A | "a manifest, a measurement record, a capture" (V3) | scanned, no breach | — |
| SC-9 | (c) locked obligation | A | `DEVIATIONS.md` (V1) | scanned, no breach | — |
| SC-9 | (d) WR authority uniform | A | — | scanned, no breach | — |
| SC-9 | (e) stronger reading only | A | six enumerated weakenings, all generic | scanned, no breach | — |
| SC-9 | (f) stated twice | A | §0.2.1 line 77 | scanned, no breach | — |
| SC-9 | DATA / ROWS | X | "row 138's R13" — a K1 accounting reference in apparatus | scanned, no breach | — |
| **SC-10** | heading | A | — | scanned, no breach | — |
| SC-10 | (a) non-gated data | A | "SC-8" | scanned, no breach | — |
| SC-10 | (b) exemption conditional | A | — | scanned, no breach | — |
| SC-10 | (c) diagnostic classes | A | "maximum across classes" — no class set named (no event-class name, no `mid(t)`) | scanned, no breach | — |
| SC-10 | (d) four forbidden uses | A | "criterion-1 arithmetic" | scanned, no breach | — |
| SC-10 | (e) one copy | A | §0.2.1 line 77 | scanned, no breach | — |
| SC-10 | marker (§6.1 line 431) | M | "five bodies" (V4 — registered heading) | scanned, no breach | — |
| SC-10 | INSERTION POINT / DATA | X | cites K1 F-5; DATA generic | scanned, no breach | — |
| **SC-11** | heading | A | — | scanned, no breach | — |
| SC-11 | (a) proved empty | A | "'no cells', 'no rows'" — generic strings | scanned, no breach | — |
| SC-11 | (b) minimum form | A | — | scanned, no breach | — |
| SC-11 | (c) raises | A | — | scanned, no breach | — |
| SC-11 | (d) scope | A | "per-class, per-side, per-cell or per-unit aggregation" — axes as kinds | scanned, no breach | — |
| SC-11 | (e) unexpected zero | A | — | scanned, no breach | — |
| SC-11 | (f) partial population | A | — | scanned, no breach | — |
| SC-11 | (g) composes | A | "(SC-6)" | scanned, no breach | — |
| SC-11 | DATA | X | generic (the near-miss narrative, row 136, is INSTANCE and stays in the declaration — K1 §4) | scanned, no breach | — |
| **SC-12** | heading + intro | A | §7.7's table | scanned, no breach | — |
| SC-12 | definition head + (i)–(v) | A | §7.7's `waived` (V1); "another detector" — no detector named | scanned, no breach | — |
| SC-12 | governed-set ¶ (Delta 2, corrected) | A | lines 759, 760, 1039 cited by number; "both of L2a/L3.1's combinations" quoted from line 1039 (V1/V2 — the exception both prior rounds declared, carried forward: L2a/L3.1 are §4's registered rows, not fixture names). **HIT (fixed):** the prior text "The declaration's §A.12 states the same membership and is corroboration, not the source" named this fixture's declaration section in applied schema text | **NORMATIVE — fixed** | "Where the fixture's declaration states the same membership, it is corroboration, not the source." §A.12 cite → Instance record (X). |
| SC-12 | invoking ¶ | A | — | scanned, no breach | — |
| SC-12 | does-not-permit (1)–(7) | A | "(SC-6)", "(SC-9(c), SC-9(e))"; item (6) "per-combination" (V1) | scanned, no breach | — |
| SC-12 | drafting note (Delta 1) | X | K1's superseded note "the declaration supplies which they are" was a delegation, not a particular; replaced by Part 5 Delta 1 | scanned, no breach | — |
| SC-12 | DATA (Delta 3) | X | K1's superseded DATA opened "Which detectors the floor governs **for this fixture**" — apparatus, delegation genus, already replaced by Delta 3; new DATA generic | scanned, no breach (superseded text noted) | — |
| SC-12 | Instance record (this file) | X | **contains instance data by design**: lines 759/760/1039 verbatim (registered), §A.12 lines 1543–1544 quoted (declaration), the "another/the other" variance | apparatus, labelled not applied — see 4.2 | keep in apparatus, or move to a declaration cross-reference; recommend keep (4.2) |
| **SC-13a** | marker (line 1030; not-superseded list; §10.1 line 1022) | M | v30 line 1030 quoted (V2: "contaminated from corrected fixture"); "Phase 0 kill gate", "labelled hypothetical declaration" (V1); "for that fixture" — generic; `git show prereg-v30:PREREG.md` (V1) | scanned, no breach | — |
| SC-13a | opening ¶ | A | "recorded in Phase 0" (V1), "labelled hypothetical declaration" (V1), "frozen default configuration" (line 457, V1) | scanned, no breach | — |
| SC-13a | (a1) unit | A | "feature-cohort pair", "proof yield" (V1); "per runtime detector and per declared fixture side" — no detector or side named | scanned, no breach | — |
| SC-13a | (a2) threshold | A | `preserving` (V1), "PROVEN under a passing determinism guard" (V1), §6.6 states, §7.7 `waived` (V1); "the side the fixture declares corrected" — a **declared** side, not a name (P7 concurs); "`proof yield > 0`" is the floor's own literal, not a fixture figure | scanned, no breach | — |
| SC-13a | (a3) denominator | A | §7.2, §7.4 cited; line 830's phrase quoted (V2); "which pairs the corpus labels" — no pair named | scanned, no breach | — |
| SC-13a | REGISTERS / INSERTION / DATA / ROWS | X | generic; ROWS cites J1/K1 accounting (apparatus) | scanned, no breach | — |
| **SC-13b** | marker | M | lines 816, 830, 570 (V1) — 818 removed (Q2-extra) | scanned, no breach | — |
| SC-13b | heading | A | — | scanned, no breach | — |
| SC-13b | (b1) declared set | A | §11 (V1), `DEVIATIONS.md` (V1); "each runtime detector the floor governs" — pinned by citation at (c3), not named | scanned, no breach | — |
| SC-13b | (b2) per side | A | "(governed detector) × (declared side) cell" — schema vocabulary; §7.2.1's rule quoted (V2; citation scope is a P7 item, Part 6) | scanned, no breach | — |
| SC-13b | (b3) `not_applicable`-everywhere | A | `not_applicable` (V1, line 570); lines 816, 830 (V1); "0/N" — a form, no N. **HIT (fixed):** "(§A.12's head: …)" named this fixture's declaration section in applied schema text | **NORMATIVE — fixed** | "(SC-12's definition: …)" — Q2(c)-1. (The line-818 misreading in the same sentence is Q1(ii), not R24.) |
| SC-13b | (b4) why the test exists | A | three run conditions — kinds; "the other detector" — follows from the pinned two-row set (registration-level, V1) | scanned, no breach | — |
| SC-13b | DATA | X | generic — no set, no side, no predicate named | scanned, no breach | — |
| **SC-13c** | marker | M | line 816 (V1) | scanned, no breach | — |
| SC-13c | (c1) adoption | A | §6.2 criterion 3, line 461, `prereg-v30a` (V1). **HIT (fixed):** "§A.12 item 5" — declaration section in applied schema text | **NORMATIVE — fixed** | "SC-12 item (5)" — Q2(c)-3. |
| SC-13c | (c2) line-816 exception | A | line 816 quoted (V2), line 830, line 1035; "(c4)". **HIT (fixed):** "§A.12's head and limb (iii)" | **NORMATIVE — fixed** | "SC-12's definition, head and limb (iii)" — Q2(c)-2; non-reliance sentence added (Q1(ii)). |
| SC-13c | (c3) governed set | A | §7.1 rows by line (759, 760), line 1039's "both of L2a/L3.1's combinations" (V1/V2 — declared exception carried forward); "as revised with these clauses" — a drafting-history phrase that still resolves in applied text (SC-12 is present); noted, not changed | scanned, no breach | — |
| SC-13c | (c4) every combination executed | A | `preserving` (V1); "the other combination" — no name | scanned, no breach | — |
| SC-13c | (c5) intro + (c5)(ii) + closing | A | line 1035's limbs; §10.2 criterion 3's two gates named by role (finding-rate, completion) — registered gates (lines 1037–1038) | scanned, no breach | — |
| SC-13c | **(c5)(i)** | A | **HIT (fixed, Q1(i)):** "which in this fixture's instance form §A.8 states as per-side, per-class, per-instrument-month" — this fixture's declared **cell key** (an instrument-month axis) in PREREG schema text. **HIT (fixed):** "and that declaration §A.8 records per working resolution R9" — declaration section + working-resolution id | **NORMATIVE — fixed** (two hits, one limb) | Both deleted; generic key sentence added; both facts → SC-13c Instance record (X). Text in Part 2, Q1(i). |
| SC-13c | (c6) scope | A | "labelled hypothetical declaration" (V1), "descriptive fixture proof count" (V1, line 470); "a detector row" — none named | scanned, no breach | — |
| SC-13c | (c7) purpose | A | — | scanned, no breach | — |
| SC-13c | DATA | X | "None." | scanned, no breach | — |
| SC-13c | Instance record (this file) | X | **contains instance data by design**: §A.8 line 1416's cell key ("per-side, per-class, per-instrument-month"), R9, §A.12 lines 1546–1556 | apparatus, labelled not applied — see 4.2 | keep in apparatus, or move to a declaration cross-reference; recommend keep (4.2) |
| **§13c-P** | line-816 pointer | A | `preserving` (V1), "the other combination", §7.4 line 830, "v30a amendments block" | scanned, no breach | — |
| **§AB** | amendments-block recording | A (record) | lines 816, 830, 818 quoted (V2); §0.2.1 lines 72/77/93/95; SC-9, SC-12 cited; **§D.3 and §A.12 named as corroboration** — a record of *this* amendment may name the declaration it is made under; retained deliberately, author may strike | scanned, no breach (corroboration cites disclosed) | — |

## 4.2 Tally, and the two categories the brief asks to be distinguished

**(i) Fixture particulars in NORMATIVE (applied) clause text — must fix. Six hits, in four limbs and
one paragraph, all fixed in Part 1:**

| # | Clause · limb | Offending text (quoted) | Genericized replacement |
|---|---|---|---|
| 1 | SC-13c(c5)(i) | "which in this fixture's instance form §A.8 states as per-side, per-class, per-instrument-month" | deleted; "**The cell key is the declaration's to supply, not this clause's to state**: SC-3(a) requires only that a key exist, be declared and named, and be frozen with the map before any detector runs (SC-3(h), SC-8), and this clause names no key." |
| 2 | SC-13c(c5)(i) | "and that declaration §A.8 records per working resolution R9" | deleted; fact moved to SC-13c *Instance record* |
| 3 | SC-13b(b3) | "(§A.12's head: a detector is waived when its result is made 'incapable of changing the criterion's outcome')" | "(SC-12's definition: a detector is waived when its result is made 'incapable of changing the criterion's outcome')" |
| 4 | SC-13c(c2) | "§A.12's head and limb (iii)" | "SC-12's definition, head and limb (iii)" |
| 5 | SC-13c(c1) | "(line 1033; §A.12 item 5)" | "(line 1033; SC-12 item (5))" |
| 6 | SC-12 governed-set ¶ | "The declaration's §A.12 states the same membership and is corroboration, not the source." | "Where the fixture's declaration states the same membership, it is corroboration, not the source." |

**Nothing from the brief's list of fixture figures — no column count, instrument name,
instrument-month, "35-column set", map dimension, AUC, model name, row count, event-class name,
`ts_floor`, `mid(t)`, or script name — appears in any applied clause text of SC-1 … SC-13c.** K1's
twelve clauses are clean on every limb; the split's clauses were clean except for the six
declaration-anchored hits above, of which hit 1 is the P7 breach and hits 2–6 are the same genus
found by extending Q1(i)'s reasoning to declaration section references. Hits 3–5 coincide with
Q2(c)'s citation-source correction, so one edit closes both defects at each site.

**(ii) Fixture particulars in a DATA-THE-DECLARATION-MUST-SUPPLY block used as an illustrative
example — none found.** Every DATA block in the set names *kinds* of data ("the cell key and its
name", "N", "the named constant") and no value. The only apparatus text in this file that carries
fixture particulars is the two *Instance record* notes this file adds beneath SC-12 and SC-13c, and
they carry them **by design**, labelled "not applied", so that the facts stripped from applied text
under Q1(i) and Q2(c) are not lost. **Recommendation, not decision:** examples in DATA blocks are
acceptable *only* if (a) the block is apparatus and never enters `PREREG.md` — which is K1's
convention and this file's — and (b) the example is labelled as one and cites the declaration section
that carries the instance. The cleaner discipline, and the one recommended, is to keep DATA blocks
example-free (as they are today) and put any instance the drafter wants on the record in a labelled
*Instance record* note that cites the declaration by section and line — as done here — or in the
declaration itself. If the author prefers the applied set to carry no declaration references at all
even in apparatus, the two *Instance record* notes can be moved verbatim into a cross-reference
paragraph of `AVAILABILITY_DECLARATION.md`'s §A walk; nothing in the applied clauses depends on
them.

**Registration-vocabulary exceptions carried forward, declared again so they are not silent:**
(1) `preserving` / `promoted` (§3.1 line 301) in SC-12, SC-13a(a2), SC-13c(c2)(c4), §13c-P;
(2) L2a / L3.1, quoted from line 1039 and named as §4's rows (lines 318, 320), in SC-12's governed-set
paragraph and SC-13c(c3) — a registration that never saw this fixture would still have these
detector rows and this line; (3) `fixture_contaminated` / `fixture_corrected` inside quoted v30 text
in SC-3's and SC-13a's markers. None is a fixture particular; (1) and (2) were declared as exceptions
in the corrected file's §1.1 (per the split's Part 6) and in the split's Part 6 table, and this scan
re-examined and upheld both; (3) is V2 (registered text quoted inside a supersession marker) and is
declared here for the first time so that it, too, is not silent.

---

# PART 5 — CHANGE LEDGER: EVERY EDIT IN THIS FILE AGAINST THE PRIOR FILES

Every difference between Part 1 and the clause text of `K1_SCHEMA_CLAUSES.md` (SC-1 … SC-12) and
`SC13_SPLIT_ABC.md` (SC-13a/b/c, Part 5 SC-12 delta, Part 3.1 recording) is listed. "A" = applied
text changed; "X" = apparatus only. Anything not listed is verbatim.

| # | Clause · element | Loc | Before (prior file) | After (this file) | Reason |
|---|---|---|---|---|---|
| E-1 | **All 15 clauses — applied heading** | A | K1 headings e.g. "**§2.9 What a reconstructed declaration fixes, and what it may not leave open — v30a**"; split headings as quoted in Part 3 Q2(a)-1 | each ends with its tag: `[SC-1]` … `[SC-12]`, `[SC-13a]`, `[SC-13b]`, `[SC-13c]` | Q2(a); §0.1 resolution rule |
| E-2 | SC-6(b) | A | "— see SC-12 and finding F-6.)*" (K1 line 502) | "— see SC-12.)*"; F-6 note added beneath SC-6 as apparatus | Q2(a) genus — dangling drafting reference in applied text |
| E-3 | SC-4 ROWS note; SC-6 INSERTION POINT; SC-8 ROWS; SC-9 ROWS; SC-10 INSERTION POINT; SC-12 DATA | X | "See finding F-3"; "(see §0)"; "(see §3)"; "(see §3)"; "See finding F-5"; "(finding F-7)" | "See K1 finding F-3"; "(see K1 §0)"; "(see K1 §3)"; "(see K1 §3)"; "See K1 finding F-5"; "(K1 finding F-7)" | apparatus cross-references re-pointed: this file does not reproduce K1 §0/§3/§5 |
| E-4 | SC-12 drafting note; SC-12 header note | X | K1 lines 837–839 ("… the detector names are not hard-coded — the floor names 'the runtime detectors' and the declaration supplies which they are"); no header note | split Part 5 **Delta 1** text, verbatim; a one-paragraph italic note under the SC-12 heading recording that the clause is K1's with the Part 5 deltas merged and two further corrections | adopts the split's SC-12 delta; provenance note |
| E-5 | SC-12 governed-set paragraph | A | absent in K1; split Part 5 **Delta 2** text | Delta 2 adopted with two changes: (i) "line 759's `Runtime, preserving` row and its `promoted` companion" → "line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row"; (ii) "The declaration's §A.12 states the same membership and is corroboration, not the source." → "Where the fixture's declaration states the same membership, it is corroboration, not the source." | Q2(b)-2; Q2(c)-5 / Q3 hit 6 |
| E-6 | SC-12 DATA block | X | K1 lines 874–876 ("Which detectors the floor governs for this fixture; …") | split Part 5 **Delta 3** text, with "(finding F-7)" → "(K1 finding F-7)" | adopts the split's SC-12 delta; E-3 |
| E-7 | SC-12 Instance record | X | — (new) | lines 759, 760, 1039 quoted verbatim; §A.12 lines 1543–1544 quoted as corroboration; the "another / the other" wording variance restated as disclosed | Q2(b)-3; Q2(c)-5; Q3 §4.2(ii) |
| E-8 | SC-13a SUPERSESSION MARKER, lead-in | X | "One, conditional rather than absolute — carried from the corrected draft with the clause names updated:" | "One, conditional rather than absolute:" | drafting-history phrase trimmed (apparatus) |
| E-9 | SC-13a SUPERSESSION MARKER, "Line 816 is not superseded" sentence | M | "… for this criterion's required quantities only, and its publication clause is kept and required." | "… for this criterion's required quantities only, its publication clause is kept and required, and a pointer to the exception is inserted at line 816's own site (SC-13c, second insertion point)." | Q2(c)-6 (pointer) |
| E-10 | SC-13b SUPERSESSION MARKER | X | "The registered lines it relies on — 816, 818, 830, 570 — stand byte-exact and are cited." | "— 816, 830, 570 —" | consequential to Q1(ii): 818 no longer cited by (b3) |
| E-11 | **SC-13b(b3)** | A | "Line 818's own principle decides this rather than fighting it — 'Suppression exists …' — and at a kill criterion this zero measures exactly what the criterion asks: a combination that never applied cannot separate the fixture sides, and a gate suppressed on that fact is a detector waived on it (§A.12's head: a detector is waived when its result is made 'incapable of changing the criterion's outcome')." | "**The exception rests on two grounds and on no other.** *First*, it is a class C change to how line 816 reads at this one criterion, made on this amendment's own authority and recorded in the v30a amendments block (SC-13c(c2)). *Second*, this is a kill criterion over the detectors' capability: a combination that never applied on a declared side cannot separate the fixture sides, so a gate suppressed on that fact is a detector waived on it (SC-12's definition: a detector is waived when its result is made 'incapable of changing the criterion's outcome'), and line 1035 forbids the waiver." | **Q1(ii)**; Q2(c)-1 / Q3 hit 3 |
| E-12 | SC-13c INSERTION POINT | X | one insertion point | two: (1) as before; (2) the line-816 pointer after line 816 | Q2(c)-6 |
| E-13 | SC-13c(c1) | A | "(line 1033; §A.12 item 5)" | "(line 1033; SC-12 item (5))" | Q2(c)-3 / Q3 hit 5 |
| E-14 | SC-13c(c2) | A | "— §A.12's head and limb (iii) — and line 1035 forbids the waiver." | "— SC-12's definition, head and limb (iii) — and line 1035 forbids the waiver. **The exception rests on this amendment's class C authority and on that capability ground; it does not rely on `PREREG.md` line 818, whose text stands as registered.**" | Q2(c)-2 / Q3 hit 4; Q1(ii) non-reliance sentence |
| E-15 | SC-13c(c3) | A | "§7.1's `Runtime, preserving` and `Runtime, promoted` rows (line 759)" | "… rows (lines 759 and 760)" | Q2(b)-1 |
| E-16 | **SC-13c(c5)(i)** | A | text quoted in Part 2, Q1(i) BEFORE | text quoted in Part 2, Q1(i) AFTER — two deletions ("and that declaration §A.8 records per working resolution R9"; "which in this fixture's instance form §A.8 states as per-side, per-class, per-instrument-month"), one generic sentence added | **Q1(i)**; Q3 hits 1–2 |
| E-17 | SC-13c Instance record | X | — (new) | §A.8 (1407–1436, line 1416) and R9 named as the instance home of the amended criterion 3 and its cell key; §A.12 (1546–1556) named as the corroborating waiver definition | Q1(i); Q2(c); Q3 §4.2(ii) |
| E-18 | **§13c-P — line-816 pointer** | A | — (new) | one paragraph after line 816, text in Part 1 | Q2(c)-6 |
| E-19 | **§AB — amendments-block recording** | A (record) | split Part 3.1 | three changes: (i) "(§A.12 head and limb (iii))" → "(SC-12's definition, head and limb (iii); the declaration's §A.12 states the same definition and corroborates)" and "a pointer to the exception is inserted at line 816's own site" appended; (ii) new paragraph "**What this amendment claims for the exception, and what it does not**" recording the departure from line 818's applied holding; (iii) "(§0.2.1 line 95; §D.3; §A.12 item 5)" → "(§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3 and §A.12 item 5)" | Q2(c)-4; Q1(ii) |
| E-20 | Split Part 3 commentary ("The exception is grounded in line 818's own registered principle rather than against it") | — | present in the superseded file | **withdrawn**, not reproduced; contradicted by E-11/E-14/E-19 | Q1(ii) |
| E-21 | Split Part 6 R24 re-test table (rows for (b3), (c5)) | — | "(b3) … line 816/818/830 cited by number"; "(c5) … cites SC-3(b)'s dispositions and SC-3(a)/§A.8's indexing axes by name … / Yes" | **superseded by Part 4** of this file, which re-runs the test token by token over the corrected text | Q1(i) R24-table-miss note; Q3 |

**Not changed, and noted so the scan is auditable:** SC-13c(c3)'s phrase "SC-12, as revised with
these clauses" (drafting history, but resolves in applied text); SC-13a(a3)'s "§7.2's body-of-data
scope" and its "per detector" reading of §7.4 (P7 items outside Q1–Q3, Part 6); SC-13b(b2)'s citation
of §7.2.1's empty-denominator sentence (same); K1's supersession markers' references to H1 hunks
H2/H3/H4/C1/C2, R23 and F-5 (Part 6 item 4). **The K1 accounting (§2 76 rows, §3 26 rows, §4 36
rows) is unchanged: no row moves, no tally changes; the split's "ROWS COVERED: none of J1's 76" for
SC-13a/b/c stands.**

---

# PART 6 — CARRIED OPEN, REPORTED NOT SOLVED

1. **P7 items outside Q1–Q3, unchanged in Part 1** (each is a citation-scope or characterization
   item with no weakening direction, per P7's own re-test): (a) SC-13a(a3) attributes the
   "body of data" scope to §7.2, whereas the phrase's registered home is line 816 in §7.2.1, and its
   "per detector" reading of §7.4 is an interpretive extension (line 830 does not mention detector
   rows; the detector-row connection is §4's coverage map and §7.1, which (a3) does not cite for that
   step) — the split's Part 8 item 3 claimed the clauses cite lines 759/780/791/1039 for the partition,
   which they do not, and that commentary is not reproduced here; (b) SC-13b(b2)'s "§7.2.1's own
   registered rule … 'Undefined, not 0% or 100%, at an empty denominator'" is registered inside the
   feature-cohort precision definition (lines 808–810), whose immediate referent is precision, not
   yields — an out-of-scope citation of N6-finding-14's genus; the disposition does not depend on it;
   (c) the `unsupported`-everywhere state is disposed only implicitly (via (a2)'s terminal-execution
   sentence and the defined 0/N arithmetic; line 816's trigger is `not_applicable` only, so no
   suppression route exists for it), where the round-2 draft named it; (d) SC-13a(a2)'s mirror of
   (b2)'s 0/0 closure is derivative and cites (b2), but is a latent two-statements site if (b2) is
   ever amended alone; (e) the "opposite directions" framing of 816/830 admits a harmonizing reading
   (830 governs denominator membership, 816 governs publication/gating) — recorded as an observation.
2. **No tooling was run** against any clause this pass (`tools/check_registration.py`,
   `tests/registration/`), and no anchor-match count was verified by an applier; the two anchors this
   file itself introduces (line 816 for §13c-P; the SC-12 / SC-13 chain after line 1035) were read
   directly and each matches once as a full line today. **Every anchor goes stale after the first
   edit lands**; SC-13b/c's stated anchor goes stale as soon as SC-13a's multi-line replacement of
   line 1030 lands. K1's F-9 stands: SC-6 modifies the line-855 table row, which no earlier hunk did.
3. **Pre-existing K1 application gaps this file inherits and does not close** (outside Q1–Q3): SC-6's
   replacement text for the line-855 row and its §8.2 (line 915) insert are specified as insertion
   points only — no replacement row and no §8.2 sentence is drafted; SC-8's §11 pointer item and
   SC-11's §8.6 pointer are likewise undrafted; K1's F-1 (row 28, needs an explicit class C amendment
   of line 449 or acceptance that the branch fires — until then line 1033's obligation is what SC-13a–c
   discharge, and §A.5's reading is not registered), F-5 (§6.1's closed "Five bodies" heading vs
   SC-10), F-8 (six declaration edits implied, not performed) all stand.
4. **Supersession-marker text in SC-2, SC-3, SC-8, SC-10 references drafting identifiers** — H1 hunks
   H2/H3/H4/C1/C2, item R23, finding F-5. K1's convention is that these markers "stand as H1 wrote
   them and are cited, not re-drafted"; at application the identifiers must resolve to the registered
   citations H1's diff carries (`PREREG_v30a_DIFF.md` H2/H3/H4 at lines 445/450/451, C1/C2 at
   992/1022), or be struck. Same genus as Q2(a); reported, not rewritten here because none is in a
   THE-CLAUSE body.
5. **The N4 instance-data residue is unchanged:** the labelled-unit set SC-13b(b1) requires does not
   yet exist for the label-availability detector; under SC-13b as written the fixture today trips
   (b1)'s STOP for that detector unless the measurement named at the end of the corrected file's
   Part 4.3 closes run condition (i) first. Whether L2a-preserving is in fact `not_applicable` on
   every scope-eligible case of this fixture remains uninstantiated instance data.
6. **The 816/830 conflict is recorded (§AB), flagged, and deliberately unresolved** pending a future
   class C amendment, exactly as the brief for the split required.
7. **Author decisions requested by this file:** (i) adopt the uniform `[SC-n]` heading tags (or
   strike them on SC-1 … SC-12 and resolve the listed cross-citations at application); (ii) accept
   the relocation of the §A.8 / §A.12 references from applied clause text into the two *Instance
   record* notes, or move those notes into the declaration's §A walk (Part 4, §4.2(ii)); (iii) approve
   §13c-P's text and anchor; (iv) approve §AB's revised recording text, including the paragraph
   acknowledging the departure from line 818's applied holding; (v) the standing decisions the split
   file requested — the P2 disposition, the SC-12 delta, the fate of the superseded ledger entries
   3.3 and 3.4 — remain open and are not decided here.

---

## CLOSING TALLY

| | |
|---|---|
| Clauses delivered, corrected, verbatim | **15** — SC-1 … SC-12, SC-13a, SC-13b, SC-13c (+ §13c-P pointer, + §AB recording text) |
| Q1 normative edits | **2** — SC-13c(c5)(i) cell key stripped (E-16); SC-13b(b3) line-818 characterization dropped (E-11), with (c2)/§AB non-reliance record (E-14, E-19) |
| Q2 corrections | headings tagged, all 15 (E-1); SC-6(b) dangling F-6 (E-2); line 759→760 at two applied sites (E-5, E-15) and one commentary site (E-7); waiver authority → SC-12 at five sites (E-5, E-11, E-13, E-14, E-19); line-816 pointer drafted (E-18, E-9, E-12) |
| Q3 scan | every element of every clause listed (Part 4.1); **6 normative hits, all fixed** (4.2(i)); **0 DATA-block example hits** (4.2(ii)); 3 registration-vocabulary exceptions re-examined and upheld |
| K1 accounting | unchanged — 75 covered / 1 uncoverable (row 28) / 26 non-gate (7 → PREREG, 19 PRACTICES) / 36 instance |
| Files edited outside this one | **none** |

