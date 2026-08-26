# COMPOSED SECTIONS — `PREREG.md` AS v30a WOULD LEAVE IT

**SCRATCH composition for an adversarial read. Nothing has been applied to `PREREG.md`,**
**which remains byte-identical to the `prereg-v30` tag.**

Registered v30 text appears as-is. Text v30a substitutes or inserts is marked **[v30a]** and is
the SAME operative text the signable diff renders. Read each section as a finished whole.


---

# §6.2 — as composed

### 6.2 Acceptance fixture

**[v30a REPLACES registered line 445 — H2 (schema layer: SC-2(d))]**

- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair on both sides (§A.1 item 1) — that fact, and the replacement entries themselves, are instances and are recorded in the declaration. **The clause "and because the anchor's model family changed" stood here until R55/W5 and is struck: it is false against its own cited source, which names six architectures with LightGBM listed first, and §A.1 item 2 was corrected on 21 August 2026 to say so.** Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*

- **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.
- **The availability declaration is reconstructed, not chosen** — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon, and intended live execution protocol, with **evidence for each element recorded before any detector tuning.**
- **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).
- **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.
**[v30a REPLACES registered line 450 — H3 (schema layer: SC-2, SC-9(b))]**

- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*

**[v30a REPLACES registered line 451 — H4 (schema layer: SC-2(e), SC-3(f))]**

- **Sliced variant — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.4). **The sliced variant is not part of the Phase 0 acceptance fixture.** It is a **Phase 1 CI obligation, due at the first CI run that exercises the padded slicer and before any user-facing slice auditing is published**, produced by that same padded slicer, with its slice boundaries declared. **Its scoring rule is declared now, ex ante, so it cannot be chosen after a result is seen:** a slice inherits the ground-truth-map cells its rows select and is scored against those cells under criterion 3 as amended — findings the selected cells predict are required, findings they exclude are false positives, cells the map does not cover are unscored. **A slice of a characterized side is never treated as clean, and a slice may not be reported as a pass on the strength of containing only unscored cells.** The obligation is not deletable by a `DEVIATIONS.md` entry or by a decision-log interpretation; dropping it is a further class C amendment. **Why it is amended rather than left outstanding:** the registered clause requires an artifact produced by a component of the tool under development, while §0.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly — leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure mode §2.7 exists to stop.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing."
  >
  > *The variant is moved and re-registered, not deleted: slice auditing is not dropped and the slicer is not exempt from CI.*


**[v30a INSERT — SC-2]**

**The acceptance fixture's composition — v30a [SC-2]**

**(a) THE FIXTURE IS AN ENUMERATED SET OF ARTIFACTS, DECLARED.** The declaration enumerates the
artifacts that constitute the acceptance fixture, by side, with the provenance of each. An artifact
not in that enumeration is **not part of the fixture** and no criterion is evaluated on it.

**(b) CHANGING THE COMPOSITION IS CLASS C — NEVER A DEVIATION, NEVER A WORKING RESOLUTION.**
Admitting an artifact the declaration excludes, or removing one it includes, **changes the object
the acceptance criteria are evaluated on and therefore changes what every published gate number
means.** It is a class C amendment under §0.2.1 line 93. It may not be done by a `DEVIATIONS.md`
entry, by an orchestrator decision, or by a working resolution. **Declared exclusions are hard.**

**(c) THE PRE/POST LICENCE IS BOUNDED.** Where the fixture is a paired pre/post construction and a
delta across the pair is read as an availability effect, the licence for that reading requires the
two sides to differ **in availability and in nothing else**. **A change to the column set, the
label set, the row population, or the evaluation population is not an availability change**, and a
variant carrying one is not admissible as a side of this fixture.

**(d) A REFERENCE ANCHOR IS CONSTITUTED BY RECOMPUTATION, NOT BY TRANSCRIPTION.** Where the gate
requires a reference quantity to reproduce, that quantity is **recomputed from the fixture's own
committed bytes** and declared as an **enumerated set of entries**, one per declared horizon and
side, each naming its provenance. **The recomputation is authoritative over any figure recorded in
a prior report**; a recorded figure that agrees is a secondary record and is reported as such, and
one that disagrees is a defect resolved before the gate runs, never a competing anchor. **The
declared tolerance applies per entry and may not be widened.** Because a recomputed anchor is a
pure function of committed bytes, a deviation approaching the tolerance is a **stop-and-report**,
not a pass.

**(e) MOVING AN ELEMENT BETWEEN PHASES IS AN AMENDMENT, AND ITS SCORING RULE IS DECLARED WITH THE
MOVE.** A registered element that cannot be satisfied at the instant the amendment must be
committed is **amended explicitly — never waived and never left outstanding.** Where the move
re-registers the element as a later-phase obligation, the obligation names the event that makes it
due, and its scoring rule is declared **ex ante, at the move**, so it cannot be chosen after a
result is seen.


**Pass gate — discrimination, not tier.**

*(Through v18 criterion 1 required a finding **at PROVEN tier**. That coupled acceptance to reporting: the gate asks whether the method separates two datasets whose answer is already known, while tier answers what a user may claim about their own pipeline. The coupling generated eight firings' worth of machinery — §0.2.1 — and all of it is now deleted.)*

Evaluated on the **frozen default configuration**, under the reconstructed declaration:

1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.

**[v30a MARKER — SC-4]**

**§6.2 line 459 — v30a. THE TEXT IS UNCHANGED; THE REQUIREMENT IS NOT.** *(Corrected at R54/W3.
This marker previously read "**ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact." The first
clause is true byte-for-byte and false at the outcome, and §0.2.1 line 97 measures at the outcome.)*

**What is superseded is the INFERENCE** that the denominator is any construction-taxonomy count
recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it.

**WHAT THAT DOES, STATED AS ARITHMETIC BECAUSE THE CONSEQUENCE IS NOT VISIBLE IN THE DIFF.** The
fixture manifest classes **25** of the 35 fed columns as leaking sources. Under the SC-4(b)
partition:

| manifest class | gate class | count | what a finding on it means |
|---|---|---|---|
| LEAK-SOURCE | REQUIRED | **11** | absence is a **miss** |
| LEAK-SOURCE | OUT OF JURISDICTION | **13** | a finding is a **FALSE POSITIVE** |
| LEAK-SOURCE | UNSCORED | **1** | neither for nor against |

**On 14 of those 25 columns the gate's requirement REVERSES SIGN** — from *absence is a miss* to
*a finding fails the gate*. **That is a supersession at the outcome, and it is recorded as one
here**, whatever the byte-level text of line 459 does. It is made under the class C rule, which
permits it; what §0.2.1 line 97 does not permit is making it while recording that nothing changed.

**A reader comparing v30 and v30a byte-for-byte at line 459 will see no change and conclude
wrongly.** That is why this is also carried as a disclosure on the face of the amendment (R54/W4,
disclosure 7) rather than left here alone.

**§6.2 line 446 — NOT AMENDED.** The manifest requirement stands; only the *arithmetic role* of
what it records is constrained, which is a statement about denominators, not an edit to line 446.

2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.
**[v30a REPLACES registered line 461 — SC-3]**

**SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:**
"3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`."
*Retired because a fixture side may carry real, strictly-post-decision violations, in which case
the registered criterion fails the gate on a correctly-behaving detector reporting a violation the
fixture really contains. The measured incidence is instance data and lives in the declaration.*

**Consequential — §10.1 line 1022** (H1 **C2**): the kill gate carries a second copy of the retired
premise ("silent on `fixture_corrected`") and must be amended with this clause or `PREREG.md` holds
both readings at once.

**3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH
MAP — v30a, operative. [SC-3]**

**(a) WHAT THE MAP IS.** The map is an **enumeration of expected findings**, declared in the
fixture's availability declaration, stated **per side**, **per declared violation class**, and
**per declared cell** of the declared scored population. **The declaration declares the cell key —
the unit it declares the fixture to be partitioned into — and names it explicitly.** The map is
published as an artifact with a **declared schema**: one row per cell of the declared scored
population, with every field named, including the field that records whether the cell is
scored. **The artifact may in addition carry rows of a class the declaration declares
DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no
criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the
map's cells, not over the artifact's row count**. A count taken from the artifact without
excluding them counts a different population, and **every figure published from the artifact
names which population it counts**.

**(b) THREE DISPOSITIONS, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE MAP.**
- **A finding the map predicts is REQUIRED.** Its absence is a miss.
- **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier,
  primary or secondary.
- **A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none,
  enters no denominator, contributes to no rate, and is **never reported as a pass.**

**(c) THE MAP COVERS THE WHOLE DECLARED SCORED POPULATION.** The declaration declares the scored
population — the rows and units the criteria adjudicate. **A subclass of that population is never
excluded, masked, or given a separate denominator by description**; the only way a unit leaves the
scored arithmetic is by being an UNSCORED cell of the map, declared as such before any detector
runs. Membership of a unit in a structurally awkward subclass — a boundary, a gap, a session
edge — is **by itself neither a licence for a finding nor a defence against one**; such units are
adjudicated by the map like any other.

**(d) THE MAP IS STATED IN THE TERMS THE DECLARATION DECLARES.** It is stated in the representation
§2.9(b) names and **side-relatively**. **There is no side-independent statement of what leaks**; a
side-independent list is a category error and misroutes every finding derived from it.

**(e) ONE SCORING KEY, AND ONLY ONE.** A re-aggregation, restriction, or re-projection of the map
published for reporting is a **REPORTING OBJECT**: it is **not a second scoring key and changes no
adjudication.** Where two views of the map are published, both are published with their delta
explicit and neither replaces the other.

**(f) A DERIVED SUBSET INHERITS ITS CELLS.** Where a subset of a scored artifact is produced (a
slice, a filtered variant, a projection), it **inherits the map cells its units select** and is
scored against those cells under this criterion. **A subset of a characterized side is never
treated as clean, and a subset may not be reported as a pass on the strength of containing only
unscored cells.**

**(g) NEITHER SIDE IS ASSUMED CLEAN.** A side the declaration characterizes is **CHARACTERIZED,
never clean**, and no report describes it as clean. Silence and belief never convert into a pass
(§2.7, §8.1), applied here to the tool's own exam.

**(h) THE AMENDMENT DOES NOT LOWER THE BAR.** A finding on a cell the map marks zero is still a
false positive and still fails the gate. The unscored disposition is not an escape hatch. The map
is **declared and frozen before any detector runs** (SC-8); a map frozen after a run is a key
shaped by the result and scores nothing.

4. Silent under the identity control on both.

Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

**[v30a INSERT — SC-4]**

**The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]**

**(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY THE RULE REGISTERED HERE, AND THE
DECLARATION SHOWS THE DERIVATION.** The rule by which each unit of the declared scored set is
assigned its gate class is **registered in this clause — the class predicates of (b), under the
precedence of (c) — and is not the declaration's to state, restate, or rewrite.** The declaration
states, **ex ante, in full, and per unit**: the class assigned, and the registered predicate the
unit satisfies, **by citation to the row of (b) that carries it**, together with the declared
facts on which the unit satisfies it — what the map declares on it on the scored side under the
declared branch, and the construction and legality facts the declaration records for it. The
classes are **derived by the registered rule over those declared facts, never assigned by hand.**
**No companion document states a class predicate in rule form** — as a biconditional ("CLASS iff
…") or otherwise: the predicate is cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f)). An
evidence artifact's classification of how a unit was *built* answers a different question from
what the map declares *violating* on the scored side under the declared branch; the two do not in
general have the same answer. **No classification of the scored set other than this derivation
enters any criterion, denominator, or count**, and no split within such a classification carries
gate arithmetic. Any report quoting such a count names the scope it counts under.

**(b) EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE DECLARED SCORED SET.**

| Class | Registered predicate (cited by the declaration, per unit; never restated) | What a finding on it means |
|---|---|---|
| **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
| **OUT OF JURISDICTION** | every constituent read is declared legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
| **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |

**The declaration cites these rows, per unit, and states the facts on which each unit satisfies
the row it cites; it does not restate them** (a). **There is no fourth class and no residue
class.** **N is the length of the REQUIRED list**, and no other quantity is N.

**(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED
wins.** The declaration derives under this precedence and states none of its own; a unit's class
is the first the order yields, and for each unit that satisfies more than one predicate the
declaration records which it satisfies and that precedence decided it.

**(d) THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE
DERIVATION.** Where a registered class predicate admits two readings, the declaration states which
it derives under and why, before any detector runs. **Two readings are registered as forbidden
outright**, because each silently removes units from the arithmetic: (i) a locality condition may
not be read more narrowly than the declared lattice, so a read of the same source at another
instant of the same lattice does not by itself create a cross-source violation; (ii)
**unconstructibility in some other rebuild of the fixture is never gate-unscoredness** — only a
gate status the declaration declares EXCLUDED on the artifact the gate actually scores removes a
unit from the arithmetic.

**(e) GROUNDS FOR EXCLUSION ARE DECLARED, AND DECLARED PRE-RUN.** A unit is excluded only on a
ground the declaration states. Two grounds are registered here because each is otherwise a
guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that
cannot carry a finding of the scored class at all** (leaving it in the denominator makes criterion 1
unsatisfiable), and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot
be scored under any reading). **Reinstating an excluded unit changes the denominator and is class
C.**

**(f) PUBLICATION DISCIPLINE — the constraints below, and they are the point of the rule.**
1. **Each class is published as an enumerated list of unit names.** A class stated as a bare count
   is not auditable and does not satisfy this. A count that cannot be written out as a list is a
   count nobody can audit.
2. **No class is defined as a residue.** "Everything else" is not a class definition; each unit's
   membership is derived by (a) and shown.
3. **The partition check is printed and reproducible by any gate report:** the three class sizes sum
   to the size of the declared scored set, no unit appears in two classes, and no unit of the set is
   missing from all three. **A gate report that cannot reproduce the check has not scored the
   fixture.**

**(g) ONE GATE CLASS PER UNIT.** A unit carries **one** gate class and one only — §0.2.1 line 79's
rule that no field answers two questions, applied to gate classes. **A unit's gate class is a
statement about what the gate does with a finding on it, and the gate needs exactly one answer per
unit.** An availability *declaration* about a unit and its *gate class* are different objects and
are never conflated: a unit the declaration does not feed to the scored pipeline holds **no gate
class whatever** — declaring it out of jurisdiction would imply the gate adjudicates it and
declines.

**(h) RE-DERIVATION IS MANDATORY, AND MOVING A UNIT IS AN AMENDMENT.** If a unit's construction
changes, or an excluded unit becomes constructible, its class is **re-derived by the rule of (a).**
**The declaration's enumeration is the current output of the rule and is never a substitute for
it.** Moving a unit between classes, or changing N, after the tag is a class C amendment.

**(i) DISAGREEMENT HALTS.** Any disagreement between the rule-derived class and the frozen class is
a **stop-and-report**. It is not resolved in favour of either at run time, and a run that proceeds
past it has not scored the fixture.

**(j) THE SCORED SET IS NAMED, NOT COUNTED.** The declared scored set is identified by **the named
constant the declaration declares**, never by its cardinality. Any re-derivation names the constant,
not the length; two sets of equal size are not thereby the same set.

**(k) TWO MECHANISMS AGAINST A COLLAPSING SCORED POPULATION, AND NEITHER IS SUFFICIENT ALONE.**
There are two ways criterion 1 stops meaning anything, and they need different instruments. The
population can go **empty** — the degenerate case, caught by the floor at (k1). Or it can be
**narrowed unit by unit** until what survives is not worth scoring — the gradual case, caught by the
reconciliation at (k2). **(k1) alone is satisfied by scoring a single column.** It is written below
as the terminal backstop it is; **the operative protection is (k2)**, and a reader who takes the
backstop for the mechanism has mistaken which failure this clause exists to stop.

**(k1) THE FLOOR — THE TERMINAL BACKSTOP.** The declared scored set and the REQUIRED list are
enumerated by name **before any detector runs** and are **non-empty on every declared side**. **If
either is empty on any declared side, criterion 1 is not discharged and the outcome is STOP** —
lifted only by supplementing the declaration with declared, enumerated units for that side and
re-freezing under §11's integrity chain; never by scoring criterion 1 on the remaining side, never by
suppressing the empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution.
**Non-emptiness is the whole of this limb, and deliberately so:** any minimum above zero would be a
threshold chosen from the distribution this fixture already exhibits, which §7.0 forbids. A floor
that cannot be set without looking at the data is not set. **This limb therefore catches only the
degenerate case; it is not the protection and must not be cited as one.**

**(k2) THE RECONCILIATION — THE OPERATIVE MECHANISM.** The REQUIRED list is published alongside a
**per-unit reconciliation against the fixture manifest's list of columns classed as leaking
sources** — the **named list**, not the count. **Every unit the manifest so classes that this
derivation does not class REQUIRED is named**, with **the registered predicate of (b) that produced
its class** and the declared facts on which it satisfies that predicate. A difference stated as a
count, a total, or a summary of where the differences "mostly" sit does not satisfy this limb; the
unit is named or it is not reconciled.

**(k2)(i) EVERY GROUND NAMES THE ARTIFACT AND LOCATION THAT SUPPORTS IT.** For each such unit the
declaration cites **the artifact and the location within it** — file, and row, line, or field — on
which the declared facts rest. **The quality of a ground is not something this registration can
require**, and pretending otherwise would be vagueness dressed as a constraint; **provenance is.** A
ground with an artifact behind it can be looked up and disagreed with. **A ground with nothing
behind it becomes visible as such**, which is the whole of what this limb can achieve and is worth
more than a bar no reader could apply.

**The list is a publication input, and the count remains not a gate number.** Reading the list under
this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
denominator — (k3) governs, and §6.2 line 446's manifest requirement is unamended. **Because the
gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
own later revision cannot decide a gate outcome; an author review that silently made a complete
reconciliation incomplete would be a change to a gate input outside the class C route.

**(k3) A DISCLOSURE, NOT A CLASSIFICATION — AND THE LIMIT OF WHAT A READER CAN CHECK.** **A
reconciliation published under this limb is a disclosure, not a classification entering a criterion,
denominator, or count** (a). It derives nothing, changes no class, and no quantity appearing in it is
N. That sentence is load-bearing: without it (a) forbids the very comparison that makes the
denominator auditable, and the limb would contradict the clause it sits in.

**What a third party can and cannot do with it, stated plainly rather than implied.** The declared
map and this reconciliation are published with the registration; **the acceptance fixture is not,
and no clause requires it to be.** So a reader can check the reconciliation for **completeness**
(every manifest-classed leaking source accounted for), for **internal consistency** (each ground
citing a registered predicate), and for **provenance** (each ground naming an artifact and
location) — and **cannot** independently verify a classification against the fixture's data. **This
limb is therefore a disclosure obligation with limited external verifiability, and it is registered
as one.** Claiming it delivers an audit a reader cannot perform would be the same defect as an
overstated availability claim.

**(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared
side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named
without the registered predicate that produced its class, **or is named with a ground that cites no
artifact and location (k2)(i)**; **or where the manifest the reconciliation reads is not enumerated
in the declaration's SC-8(a) freeze, or carries a `DRAFT` status at the tag (k2)**. *(Both of those
last two are conditions (k2) states, and until R60 neither was indexed here — a limb may not impose
a condition and leave nothing to enforce it. **Both are unmet as at the date of this amendment**:
the freeze's "specifically and exhaustively" list does not name the manifest, and the manifest's
recorded status is still `DRAFT - author review required`.)* **This is a live gate item, not a check that only fires on
corruption: it can fail on an artifact that is behaving correctly, and on the fixture as declared at
the date of this amendment it is UNSATISFIED.** The declaration publishes a per-unit
cross-tabulation of the construction-SOURCE cut against the gate cut, which is a different pair of
partitions; it publishes no per-unit reconciliation against the manifest's leaking-source list. The
difference the limb would surface is **fourteen units**.


**[v30a INSERT — SC-5]**

**Adjudication routing — v30a [SC-5]**

**(a) EVERY FINDING IS CHARGED TO EXACTLY ONE CRITERION, BY THE CLASS OF THE UNIT IT NAMES.** The
gate needs one answer per finding. Routing is derived from the unit's gate class (SC-4) and the
map's disposition of the cell (SC-3), and from nothing else.

**(b) ATTRIBUTION IS TO THE GROUND, NOT TO THE NAME.** A REQUIRED entry is satisfied only by a
finding **on the side, in the cells, and on the ground the map declares.** **Criterion 1 is not
satisfied by unit name alone.** Where a unit has two grounds — one the map declares violating, one
declared legal — **the gate class follows the violating ground**, the legal ground is recorded as a
fact and not applied, and **a finding on the legal ground does not satisfy the REQUIRED entry.** It
is recorded on its own ground, and not credited to the unit's REQUIRED status. Naming the right unit
on the wrong ground satisfies nothing.

**(c) THE FALSE-POSITIVE CONSEQUENCE ATTACHES TO THE OUT-OF-JURISDICTION CLASS AND TO NO OTHER.** An
availability-class finding on an out-of-jurisdiction unit is a **declared false positive**, recorded
as such in the gate report. **It is not converted into a failure of the clean-source criterion**,
which has no landing site for such a unit; that criterion's scope is the units the declaration
declares clean, and those units **do** route to it. **The false-positive consequence is never
carried beyond the out-of-jurisdiction class.**

**(d) A FINDING ON A CHARACTERIZED SIDE IS CHARGED TWICE ONLY WHERE THE CRITERIA ARE INDEPENDENT.**
Where a finding is a false positive under (c) **and** contradicts the map on a characterized side,
it is charged under both the false-positive tally and criterion 3, and the report says so. Where two
criteria would otherwise adjudicate the same finding on the same ground, the declaration states
which one governs, ex ante.

**(e) JURISDICTION BETWEEN DETECTORS IS DECLARED, AND A BOUNDARY CUTS BOTH WAYS.** Where a finding's
character belongs to a detector row **outside** the criteria this gate scores, the declaration
assigns it to that row and it is **neither credited nor penalized here.** Routing it into this gate
would let a finding of one character masquerade as a finding of another and corrupt both counts.
**The assignment is declared before any detector runs; it may not be made after seeing where the
findings landed.**

**(f) DECLARED SENTINELS UNDER THE IDENTITY CONTROL.** An as-built artefact of the fixture that is
**present identically on every side** is **data content, not a finding**: it cannot differentiate
the sides, and a detector firing on it has produced a **false positive under the identity control.**
Such artefacts are **enumerated in the declaration ex ante**, with their signature; a sentinel
claimed after a firing is not a sentinel.


*(v19 wrote criteria 2 and 3 as "no **primary** runtime finding," which let the tool's own primary/secondary classification exempt its own false positives: a finding on a clean column, or on the corrected fixture, passed the gate if the aggregator labelled it secondary. A classifier the tool controls cannot be allowed to decide what counts against it.)*

Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**[v30a INSERT — SC-7]**

**The gate's input surface — v30a [SC-7]**

**(a) AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline
for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9).
**Nothing else.**

**(b) IT NEVER RECEIVES, AT ANY POINT IN A GATE RUN:** the paired side or any artifact derived from
it; the paired side's stored predictions or any statistic derived from them; **the declared
ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it.

**(c) WHY THE MAP IN PARTICULAR IS WITHHELD.** Under criterion 3 the map **is** the scoring key. A
detector that could read it would be graded against a key it had seen, and the run would measure
**retrieval rather than discrimination**. The map is an artifact of the harness, not an input to the
tool. **A run that received the key has not produced a gate result, whatever it reports.**

**(d) ONE SIDE AT A TIME IS A HARD SEQUENCING RULE, NOT A CONVENTION.** The criteria are per-side,
and each is evaluated from a run that saw only its own side. **A single run given more than one side
satisfies none of the criteria, however its outputs are partitioned afterwards.**

**(e) THE SURFACE IS DECLARED AND FROZEN WITH EVERYTHING ELSE (SC-8).** Widening it — including by
supplying a derived summary "for convenience" — is a class C amendment, not a harness detail.


**What this gate does and does not guarantee, said plainly.** It gates **discrimination**. It does **not** guarantee that the tool can prove leakage on real-world data — the previous gate did guarantee that, and this one deliberately does not. Proof capability is reported instead of required: the manifest records, per independent leaking source, whether it was detected, the highest tier reached, promotion status, the strategies that produced the finding, primary or secondary, affected cohorts, and the declaration used. From that the harness reports a **descriptive fixture proof count**, and deliberately not a rate:

> **k of N** labelled leaking sources received at least one primary PROVEN finding **attributed to that source**.

The attribution clause matters: without it a PROVEN finding on a *descendant* could be read as its source "reaching PROVEN," and a missed source would count as proven.

**It is published as a count, never as a decimal or percentage**, and it is identified as a descriptive fixture outcome rather than a performance rate. *(→ `HISTORY.md` H-07)*

**This is a rebalance, not a tightening.** The two gates are incomparable: a fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old and passes the new; a fixture detected at PROVEN throughout but with one REVIEW finding on a clean source passes the old and fails the new. The trade is deliberate — drop the irrelevant requirement that acceptance detections be proofs, add the relevant requirement that nothing shipped appears on clean or corrected material.

**Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

**[v30a INSERT — SC-8]**

**§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED.** The locked ordering stands byte-exact. SC-8
states what the ordering ranges over and what happens when a frozen object is later found wrong,
which line 480 left unstated.
**§11 items 1–7 — v30a, EXTENDED.** Item 8 is added: it indexes the freeze (SC-8) and amends item
3's hash set; SC-8(f) states the requirement generically and does not fix a count.

**The freeze, and what "declared ex ante" requires — v30a [SC-8]**

**(a) EVERYTHING THE GATE CONSUMES FREEZES AT THE AMENDED REGISTRATION'S TAG.** At the moment the
tag is signed, every object a gate outcome can be computed from becomes **locked**, and any
subsequent change to any of them is a class C amendment requiring a further amended registration.
**The declaration enumerates the frozen objects exhaustively**; an object the gate consumes and the
enumeration omits is a defect in the enumeration, not an object outside the freeze.

**(b) WHAT FREEZES IS THE OBJECT IN ITS AUDITABLE FORM — LISTS, NOT COUNTS.** A partition freezes as
its **enumerated lists of member names**, a map as its **rows**, an exclusion as **the named unit and
its ground**. A count is not a freeze: a count admits substitutions that a list forbids, which is the
whole difference between a frozen partition and a frozen number.

**(c) EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS.** Every declared object the gate consumes —
the map, the partition, the exclusions, any declared cohort or restriction — must be **regenerable
and checkable from the declared inputs alone, before any detector runs.** An object that can only be
confirmed after a run is a description of the result, not a declaration; a cohort so confirmed is a
key shaped by results.

**(d) A SCOPE CHOICE IS JUSTIFIED INDEPENDENTLY OF ITS EFFECT ON ANY NUMBER.** Where the declaration
restricts a scope — a class set, a cohort, a population — the justification **makes no reference to
what the restriction does to any count, and none may be added to it.** A restriction adopted for its
effect on a number is a restriction shaped by that number, which is the failure line 480 forbids in
the large.

**(e) A NUMBER FOUND WRONG AFTER A RESULT IS NOT CORRECTED IN PLACE.** *(Citation, not restatement:
§0.2.1 line 99 governs.)* It is recorded, an amended registration is committed, and the affected
benchmark is regenerated as a new version under §6.4 with the superseded results published
alongside. **In-place correction after a result has been observed is precisely how a fail becomes a
pass.**

**(f) THE FREEZE IS ONLY AS GOOD AS THE INTEGRITY CHAIN THAT CARRIES IT.** Every file the freeze
ranges over — **including the declaration itself, which carries the scoring key** — is hashed in the
amended registration's tag message as committed, and the count of hashes is **derived from the set
of registered files, never stated as a literal**. A tag that hashes the specification but not the
declaration the specification is evaluated under is an integrity chain with a hole exactly where the
amendment lives, and **an amendment weaker than the thing it amends is not one** (§0.2.1 line 97).



---

# §7.7 — as composed

### 7.7 Completion, and the two levels of state

**Two levels, and they are not the same thing.** *(→ `HISTORY.md` H-20)*

| Level | States |
|---|---|
**[v30a REPLACES registered line 855 — SC-6]**

**§7.7 line 855 — SUPERSEDED BY v30a. Registered v30 row, retained verbatim, NOT operative:**
"| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`,
`could_not_run(reason)`, `waived` |"
*Superseded because the six-state list has no state for a unit the declaration declares
unscoreable. Absent such a state, an unscoreable unit is forced into `not_applicable` (which reads
as "the question does not arise") or into a pass — which is the failure the state exists to stop.*

| **Strategy diagnostic** | `completed`, `optional_strategy_failed`, `required_strategy_failed` |

**[v30a INSERT — SC-6]**

**`unscored` — a coverage state, v30a [SC-6]**

**(a) SEMANTICS.** A unit is **`unscored`** when the declaration declares, **before any detector
runs**, that scoring it is impossible on a stated ground. An `unscored` unit **requires no finding
and forbids none.** It **enters no denominator**, **contributes to no rate**, and **cannot be
reported as a pass.** It is neither a pass nor a not-run: the detector may have executed perfectly
and there is still nothing to score.

**(b) ENTRY CONDITION — declared, never inferred.** A unit may be reported `unscored` **only if it
appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector
runs.** A unit may not enter this state because a run produced nothing, because data was missing at
run time, or because a result was surprising. **Absence of data at run time is not `unscored`; it is
the not-run state its cause selects** (§8.2). *(This entry condition is stated explicitly because
§7.7's `waived` was registered without one — see SC-12.)*

**(c) TWO LEVELS, AND THEY DO NOT COLLAPSE.** The state exists at the **cell** level of the declared
map (SC-3) and at the **unit** level of the declared partition (SC-4). **A cell-level `unscored`
never makes its unit `unscored`**, and a unit-level `unscored` does not make every cell of that unit
unscored. A gate report states which level each `unscored` entry is at.

**(d) FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored
observations**, separately from the false-positive tally, and they carry no criterion consequence in
either direction. **The three gate classes are never folded into one another**, and a report that
pools them has not scored the fixture.

**(e) THE PASS PROHIBITION IS ABSOLUTE.** A report that counts `unscored` units or cells as clean,
as covered, or as passing **has converted absence of data into evidence**. `unscored` entries are
named as unscored, never as clean, and §8.2's rule governs their display: none may be displayed in a
way mistakable for a pass.


**[v30a INSERT — SC-12(w) consequential — the §7.7 pointer, redrafted (Y3 §6.3); replaces the H8 draft]**

**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.


---

# §8.3 — as composed

### 8.3 Three assertions

**Assertions consume unaggregated evidence, never the merged display tier.** A `ReportedFinding` collapses both combinations and takes the highest tier any of its events licenses, so a single PROVEN finding can rest on an **experimental** preserving event while carrying a **non-experimental** promoted event as corroboration. Whether that merged finding trips the assertion has three defensible readings and they disagree, so it is fixed here:

> **`assert_no_proven_leakage()` fails iff there exists an EvidenceEvent that (1) licenses PROVEN and (2) belongs to a non-experimental combination**, keyed `(detector, promotion_status)`.
>
> A `ReportedFinding` **retains the gate status of each constituent event** and carries no single inferred experimental boolean. Where its events differ, the display says so: *PROVEN — experimental preserving evidence; REVIEW — non-experimental promoted corroboration.*

Aggregation is lossy by design, and assertion eligibility is one of the facts it may not collapse. The cost is that assertion logic cannot run over the `ReportedFinding` list alone; it reads the events and the gate-status table. That is the correct cost.

- **`assert_no_proven_leakage()`** — fails per the rule above. Ignores coverage. **REVIEW findings of any basis do not trigger it**, and the report says so wherever any exist, so a passing assertion cannot be read as absence of evidence.
- **`assert_no_rule_violations()`** — fails on any RULE finding from a non-experimental detector mode. Ignores coverage.
**[v30a REPLACES registered line 929 — SC-12(w)]**

**§8.3 line 929 — SUPERSEDED BY v30a, carried with SC-12(w).** Registered v30 text, retained
verbatim, NOT operative: "- **`assert_audit_complete()`** — fails on any `unsupported` or
`could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable
(§6.10). Ignores findings." *Superseded because SC-12(w) prohibits the `waived` state and a
prohibition no assertion tests is not enforced. Recover the registered line byte-exact with
`git show prereg-v30:PREREG.md`.*

- **`assert_audit_complete()`** — fails on any `unsupported`, `could_not_run`, or **`waived`** **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings. *(`waived` added v30a, carried with SC-12(w), whose (w1) prohibits the state outright; the assertion is what makes that prohibition checkable rather than merely stated.)*


`assert_audit_complete()` accepts an allow-list of **explicit recorded exceptions** — no cryptographic signature mechanism is specified and the word "signed" is not used. Each carries detector entry, mode, reason, scope, date, and configuration hash, and all are printed in the report.


---

# §10.1 — as composed

### 10.1 Phase 0 kill gate — objective

**Stop building and contribute upstream if a single maintained tool satisfies all five:**

1. Covers at least the same published types at the same tier or better;
2. Produces explicit executed / not-run accounting;
**[v30a REPLACES registered line 1022 — C2 operative item (§10.1 kill-gate criterion 3) — drafted at R39/F2]**

3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;


**[v30a INSERT — K2 §9.2 — C2 retention block (§10.1 line 1022, kill-gate criterion 3)]**

   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired **as to its corrected-side limb only**, because that limb is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. **The contaminated-side limb and the ambiguity branch are carried into the operative item byte-identical** (R47/P1); the contaminated-side tightening an earlier draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*

4. Installs and runs through a documented public interface without author modification;
5. Has had a release or commit within the previous 12 months.

Partial satisfaction is recorded and does not trigger the stop.


---

# §10.2 — as composed

### 10.2 Other kill / pause criteria

**[v30a REPLACES registered line 1030 — SC-13a]**

**§10.2 criterion 2, line 1030 — v30a, SUPERSEDED ON THE AMBIGUITY BRANCH ONLY. Registered v30
text, retained verbatim, operative where the branch has NOT fired:**
"2. **The runtime detectors cannot separate contaminated from corrected fixture under the
reconstructed declaration** → **stop.**"
*Not deleted, and not superseded generally. Line 1031 already registers the disposition this
marker performs — "this criterion is replaced, not deleted" — so where §6.2 line 449's ambiguity
branch has not fired, the sentence above is the operative criterion and SC-13a–c do not apply.
Where it has fired and been recorded, SC-13a is the operative criterion for that fixture, with
SC-13b and SC-13c inseparable from it. Recover the registered line byte-exact with
`git show prereg-v30:PREREG.md`.*

**NOT SUPERSEDED, stated so the marker's scope cannot be widened by reading:** line 1031 (the
branch and the before-tuning rule), line 1033 (the three-part obligation and the
no-`DEVIATIONS.md`-only rule), line 1035 (the floor). **Line 816 is not superseded**: its text
stands byte-exact; SC-13c(c2) states an express, scoped exception to its suppression clause for
this criterion's required quantities only, its publication clause is kept and required, and a
pointer to the exception is inserted at line 816's own site (SC-13c, second insertion point).
**§6.2's four acceptance criteria are not amended by these clauses** (SC-13c(c6)) — SC-13a–c
*depend on* the amendment this registration makes to §6.2 criterion 3 and do not make it
(SC-13c(c1)).

**Consequential — §10.1 criterion 3, line 1022.** The Phase 0 kill gate's third condition already
carries the ambiguity branch on its face ("**or, where the fixture is semantically ambiguous
(§6.2), under the labelled hypothetical declaration**") and is **not** amended by these clauses:
§10.1 scores a *third-party tool*, SC-13a scores *this project's* runtime detectors. Named here so
the two are not conflated during application.

**2. Where the fixture is semantically ambiguous, the runtime detectors must reach a non-zero
per-side proof yield on every detector — v30a, operative on the ambiguity branch. [SC-13a]**

This criterion replaces the criterion above wherever §6.2's ambiguity branch has fired and been
recorded in Phase 0, and it is evaluated **under the labelled hypothetical declaration that branch
requires**, on the frozen default configuration, with the declaration's scoring key withheld from
every detector. **SC-13b's admissibility test is applied first, before any detector runs.** The
limbs of SC-13a and SC-13b are conjunctive, and **failure of any of them is a stop**; a criterion
evaluated in breach of SC-13c(c4)'s execution requirement is not discharged.

**(a1) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime
scoring unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. **The
yield is computed per runtime detector and per declared fixture side**, and each of those figures
is published separately. *"Per detector, per side" partitions the computation; it does not
redefine the unit, and it does not narrow the denominator — see (a3).* **This unit is a declared
alternative to the descriptive fixture unit of §6.2**, adopted deliberately and on the record,
because the pair is the unit proof yield is already registered in and the floor's first limb is
stated in proof-yield terms.

**(a2) THRESHOLD.** For **each** runtime detector the floor governs (the set SC-13c(c3) pins), on
**each** declared side, the `preserving` combination's proof yield must be **strictly greater than
zero** — `proof yield > 0`. **This is the floor of line 1035 taken literally and applied per
detector and per side rather than once globally.** It is not a chosen number and it may not be
tuned: there is no selection procedure to shape, which is what makes it committable before any
development-corpus contact. **A threshold met by any route other than a preserving intervention
reaching PROVEN under a passing determinism guard does not satisfy this limb.**
**Every quantity this limb gates is defined and every gate it states is evaluated.** SC-13b(b2)
requires the labelled-unit set to be non-empty on every declared side of every governed detector,
so no denominator this limb reads is empty and no undefined yield arises; SC-13b(b3) and
SC-13c(c2) provide that neither this gate nor the yields it reads are suppressed under `PREREG.md`
line 816. **Each governed `(detector, preserving)` combination is executed to a terminal result on
every declared side and reported under its actual §6.6 states — never under §7.7's `waived`
coverage state.**
**This limb is unconditional on every declared side, including the side the fixture declares
corrected.** It is not scoped, softened, or suspended by any acceptance criterion, by any
jurisdictional routing statement, or by any per-side asymmetry in the declaration. Where an
acceptance criterion and this limb appear to disagree about the corrected side, the disagreement
is resolved by SC-13c(c1)'s named dependency and by nothing else.

**(a3) DENOMINATOR — THE REGISTERED ONE, UNNARROWED.** The yield of (a2) is computed over **the
denominator §7.2 registers for proof yield — all scope-eligible labelled pairs — with
scope-eligibility as §7.4 defines it, taken unnarrowed.** **This clause cites that denominator and
does not restate it**; a second normative statement of it here would leave the registration with
two copies of one denominator and no canonical source.
**This clause declares no stricture on that denominator, and performs no narrowing, restriction,
projection, exclusion, or re-aggregation of it.** The two partitions (a1) names are terms the
registered denominator already carries and are not narrowings of it: **per detector** is §7.4's
own scope-eligibility term read at the detector row whose metric is being computed —
scope-eligibility being "a property of the corpus label, not of what the detector could do about
it" — and **per side** is §7.2's body-of-data scope applied to each declared fixture side.
**The labelled-unit set SC-13b requires is what INSTANTIATES this denominator, never what
restricts it.** The declaration supplies which pairs the corpus labels and which detector's risk
kind each is labelled for; that is the instance data the registered denominator is defined over.
**A declaration may not use the enumeration to remove from the denominator a pair the corpus
labels and the risk logically applies to** — that is a narrowing, it makes the criterion easier to
pass, and line 1035 forbids a replacement weaker than the floor. **If a stricture on this
denominator is ever genuinely necessary, it is declared in terms in the amendment text, justified,
and tested against line 1035 — never introduced by a citation to a denominator it does not use. No
other denominator is nominated.**

   **Where the fixture is semantically ambiguous** (§6.2), this criterion is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning.** *(v23 permitted it after tuning, in `DEVIATIONS.md` alone, floored only at non-zero proof yield. An acceptance criterion is a class C semantic object by §0.2.1's own definition, and choosing its unit and threshold after seeing development behaviour can determine whether Phase 2 passes. It also contradicted §7.0's invariant, which requires a metric specification to precede corpus inspection and tuning — the carve-out and the new rule could not both stand.)*

   > On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

   The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

**[v30a INSERT — SC-13b]**

**ADMISSIBILITY FOR THE CRITERION ABOVE — v30a [SC-13b]. Tested before any detector runs, and
before any limb of the criterion.**

**(b1) THE DECLARED SET.** A semantically ambiguous fixture may discharge the criterion above only
if the declaration enumerates, **by name, before any run, and frozen with everything else the gate
consumes**, a **non-empty labelled-unit set for each runtime detector the floor governs** — the
governed set is pinned at SC-13c(c3) and is not the declaration's to choose. **If any governed
detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is
STOP.** The stop is lifted only by supplementing the declaration with a declared, enumerated set
for the empty detector and re-freezing under §11's integrity chain — never by scoring the
criterion on the remaining detector, never by suppressing the empty detector's gate, and never by
a `DEVIATIONS.md` entry or a working resolution.

**(b2) THE DECLARED SET, PER SIDE.** The set's partition by declared fixture side is itself gate
input, and **the labelled-unit set must be non-empty in every (governed detector) × (declared
side) cell**. A cell that is empty — a governed detector whose set is non-empty overall but empty
on one declared side — **trips the same STOP as (b1), lifted the same way and only that way**: by
supplementing the declaration with declared, enumerated units for that detector on that side and
re-freezing under §11. An empty side is **nothing declared to score** on a body of data the
criterion gates — the admissibility genus (b1) already occupies, not the threshold genus — and
disposing it instead as a scored zero would put a defined value on an empty denominator, which
§7.2.1's own registered rule refuses: "**Undefined, not 0% or 100%, at an empty denominator.**"
**Consequence, stated so no reader ever decides it: every per-side denominator SC-13a(a2) reads is
non-empty, every yield it gates is defined, and the undefined 0/0 case cannot arise.**

**(b3) THE `not_applicable`-EVERYWHERE STATE — DISPOSED, NOT SUPPRESSED.** A governed combination
that is `not_applicable` on every scope-eligible case of a declared side, over a declared
non-empty labelled-unit set, is **not** an empty set: (b1) and (b2) do not fire, because there is
something declared to score. Its disposition is this, in full:
the combination is **executed and reported to terminal §6.6 states**, and its counts are published
naming the reason — line 816's publication clause, kept and required; its labelled pairs **stay in
the registered denominator as misses**, as §7.4 line 830 provides; its `preserving` proof yield on
that side is therefore **zero — a defined 0/N over declared units, not a 0/0**; **zero fails
SC-13a(a2)'s strictly-greater-than-zero threshold, and the STOP is tripped and published.**
**SC-13a(a2)'s gate is NOT suppressed by `PREREG.md` line 816.** For the quantities the criterion
requires, line 816's suppression clause does not apply — the express, scoped exception SC-13c(c2)
states and the amendments block records. **The `not_applicable` finding is PUBLISHED, never
suppressed**: the counts, the named reason, the computed zero yield, and the gate outcome are all
published together. **The exception rests on two grounds and on no other.** *First*, it is a class
C change to how line 816 reads at this one criterion, made on this amendment's own authority and
recorded in the v30a amendments block (SC-13c(c2)). *Second*, this is a kill criterion over the
detectors' capability: a combination that never applied on a declared side cannot separate the
fixture sides, so a gate suppressed on that fact is a detector waived on it (SC-12's definition: a
detector is waived when its result is made "incapable of changing the criterion's outcome"), and
line 1035 forbids the waiver.
**The two stop genera stay distinct and are never pooled**: (b1)/(b2) stop for an **admissibility
reason** — nothing declared to score; (b3) stops through the threshold for a **detection reason**
— declared units, terminal execution, and no proof. The two stops are reported under their own
limbs.

**(b4) WHY THIS TEST EXISTS, AND WHAT MAKES IT A TEST RATHER THAN A FORMALITY.** A detector whose
declared labelled-unit set is empty **cannot change the criterion's outcome**, which is the
defining condition of a waiver under the floor's own definition. Three run conditions produce an
empty set or cell, and each is a real state of a real fixture rather than a defect:
**(i)** the fixture contains no dependency of that detector's kind — on the affected side, none
that reaches it — so there is nothing for the declaration to enumerate; **(ii)** the detector's
required declaration is absent or its applicability mode is not selected, so it returns a not-run
state on every case and the declaration has no model under which to enumerate units; **(iii)**
every unit that could carry that detector's character is declared EXCLUDED or `unscored` on a
stated ground, so none survives into the enumeration. **In all three the criterion is silently
satisfiable by the other detector alone, and this clause converts that silence into a stated
outcome.**
**One state the superseded drafts listed as a fourth condition is not one, and is removed.** A
declaration that assigns every unit of a detector's character to the other detector's jurisdiction
*within the criterion's own scope* is not an independent run condition: where the risk logically
applies to the reassigned unit, the reassignment is the narrowing SC-13a(a3) forbids in terms; and
where it does not, the state just is condition (i). Either way it adds nothing to this list, and
keeping it would list a prohibited act as a "real state rather than a defect".


**[v30a INSERT — SC-12]**

**"Waived", defined — v30a [SC-12]**

The floor above uses the word without a defining clause, and the word appears again as a coverage
state in §7.7's table, also undefined. An undefined term inside a floor whose purpose is to stop
criteria being dropped silently is exactly the term that gets read permissively later. This adds the
defining clause.

> A detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or
> reported in any way that makes the detector's own result **incapable of changing the criterion's
> outcome**. Concretely, a detector is waived if any of: **(i)** it is excluded from the criterion's
> denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty
> for a pass; **(iii)** the criterion can be satisfied by another detector's output alone; **(iv)**
> its threshold is set at a level it meets without executing, or by construction; **(v)** its cases
> are reported under §7.7's `waived` coverage state rather than executed to a terminal result.

**Which detectors the floor governs is not the declaration's to choose.** They are the detector
rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule
gates — `PREREG.md` line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row,
and line 1039's "both of L2a/L3.1's combinations" — the same registered set SC-13c(c3) pins. Where
the fixture's declaration states the same membership, it is corroboration, not the source. The
declaration may not shorten the set, and a criterion or report written over fewer than all of the
governed detectors has waived the omitted ones.

**What invoking it requires: nothing, because it may not be invoked.** The floor is a **prohibition,
not a permission with conditions.** There is no procedure by which a detector the floor governs may
be waived in a replacement criterion. A replacement that waives one is weaker than the floor and is
out of specification on its face; **it does not become admissible by being recorded, disclosed,
justified, or approved.** Changing that requires amending the floor itself.

**What this definition does NOT permit.** (1) It is not an escape hatch of any kind and creates no
exception, justified, approved, or time-limited. (2) It does not reach any other criterion and may
not be cited to soften §6.2's. (3) **"Experimental" is not "waived"** — an experimental marking
changes how findings are labelled and asserted on; it does not remove a detector from a replacement
criterion's denominator, and a criterion that drops a detector *because* it was marked experimental
has waived it. (4) **"No data" is not "waived"** — a cell with no data is `unscored` (SC-6), and the
detector is still scored wherever data exists; doing at the level of a whole detector what SC-6
forbids at the level of a cell is a waiver. (5) **A working resolution or a `DEVIATIONS.md` entry
cannot do it** (SC-9(c), SC-9(e)). (6) **Per-combination waiving is still waiving**, and is class C.
(7) **It licenses nothing after tuning** — a criterion chosen because it works after tuning is a
criterion shaped by tuning.

**(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE — a prohibition, and a closed list of licensed grounds with no members.**

§7.7's table carries `waived` as a detector-case coverage state and registers no condition under which a report may assign it. It is the only state in that table without one, and the omission is not cosmetic: **no runtime metric reads a detector-case state** (§7.2.1), and `assert_audit_complete()` reads it alone. A state the apparatus cannot bound by its consequences must be bounded at entry.

**The direction of the bound is forced by limb (v) above.** Limb (v) makes assignment of this state one of the ways a detector *becomes* waived. Any permissive entry condition would license, in the definition's own words, the act the definition exists to name. The bound is therefore drawn as a prohibition.

**(w1) THE CONDITION. NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.** The grounds on which this state may be entered are exhaustively enumerated in this limb; the enumeration is **closed**, and it has **no members**. No ground may be inferred from silence, from practice, from a report's convenience, or from the state's presence in §7.7's table.

**(w2) EVERY DETECTOR-CASE TAKES THE COVERAGE STATE ITS CAUSE ALREADY SELECTS — cited, not restated.** §7.7's completion lock selects it where a terminal result is or is not reached; §8.2 draws the boundary between the not-run states and governs their display; SC-6(b) governs a unit the declaration declared unscoreable, by name, before any detector ran. Those rules dispose of every detector-case between them, and **the residue this state would have carried is empty.**

**(w3) THE STATE RECORDS A WAIVER; IT NEVER MAKES ONE — and this governs every ground ever added.** Waiving is a property of how a criterion is **written, configured, or reported** — something a criterion's design does to a detector, never something a run does to a case. The coverage state can therefore only ever be the **record** of a waiver registered text has already effected under limbs (i)-(iv); it is never that waiver's source. **A report does not create a waiver by asserting the state.** Accordingly **no ground added to (w1)'s enumeration may be constitutive**, and **limb (v) may never be a ground under (w1)**; nor may an availability declaration, a working resolution, a `DEVIATIONS.md` entry, the frozen configuration of §6.8, or an `assert_audit_complete()` recorded exception.

**(w4) THE PROHIBITION BINDS PER CASE AND PER COMBINATION.** A case may not be reported `waived` on one of §7.1's combinations and executed on the other. **Per-combination waiving is still waiving** (item (6) above).

**(w5) AN ENTRY THAT APPEARS IS A BREACH, AND LIMB (v) IS WHAT CLASSIFIES IT.** By limb (v) the detector is thereby waived with respect to every criterion the case feeds. Where that detector is one the floor governs and the criterion is §10.2's replacement criterion or any part of it, the replacement is weaker than the floor and out of specification on its face, and **it does not become admissible by being recorded, disclosed, justified, or approved.** Everywhere else the case has reached no terminal result, is **not complete** under §7.7's completion lock, may not be counted or displayed as complete, covered, clean, or passing (§8.2), and is re-reported in the state its cause selects — or the fixture is not scored.

**(w6) THE TOKEN IS NOT STRUCK FROM §7.7's TABLE.** The state stays in the vocabulary so that a report using it is **caught** by limb (v) and by this limb rather than silently accepted. Striking the name would leave the act unnamed, and limb (v) with nothing to classify.

**(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` detector-case entries, **per detector and per combination**, as a count. **That count is zero.** A report that does not publish it has not discharged this limb: a prohibition whose observance is never published is not checkable.

**What this limb does NOT permit.**

**(1) It licenses the state in no case, and silence is not licence.** The empty enumeration is the whole of the permission. In particular, **a criterion's failure to name a detector licenses nothing**: a criterion that enumerates its detectors and omits this one, a criterion written before this detector existed, and a criterion that says nothing about detectors at all are **all silence for this purpose**. The omitted detector **bears on that criterion**, and its cases are executed to terminal results. Reading silence as licence would be waiving by omission — limbs **(i)** and **(iii)** above — and would move the licence from registered text to whoever last failed to update an enumeration.

**(2) A ground may be added only by a further class C amendment to this limb** (§0.2.1 line 93), committed and externally timestamped **before the affected detector is implemented or evaluated** (line 95), never after a fixture result is observed (§6.2 line 480; SC-8). Any such ground must be **declaratory** under (w3). **And no such amendment may license the state for a detector the floor governs at a §10.2 replacement criterion**: the floor forbids that above, there is no procedure by which it may be done, and this limb supplies none and may not be cited as one.

**(3) "No data" is still not "waived"** (item (4) above), and this limb creates no route by which it becomes so. A cell with no data is `unscored` where SC-6(b)'s declared-ledger condition is met; absence of data at run time is otherwise the not-run state its cause selects (§8.2). A run that produced nothing, a missing or impossible input, a crashed or failed strategy, and a surprising result are each disposed of there and by none of them does a case enter this state.

**(4) "Experimental" is still not "waived"** (item (3) above). A detector or mode shipped experimental under §10.2 criterion 3 executes its cases and reports their terminal results; the marking changes how findings are **labelled and asserted on**, never which coverage state a case takes.

**(5) Jurisdiction is not waiver.** What a jurisdictional routing statement reaches is settled at SC-13c(c6), cited and not restated. A boundary on **where a finding is charged** is never a licence to leave a case **unexecuted**.

**(6) It amends no other coverage state's entry condition and moves no boundary in §8.2.** It reaches §8.3 in exactly one way, deliberately: `waived` joins `assert_audit_complete()`'s failure set at line 929, so that emitting the prohibited state **fails an assertion instead of passing silently**. That is the whole of its reach into §8.3 — no other assertion changes, and no other coverage state's treatment changes. **`unscored` is not added to that failure set, and must not be**: `unscored` is a *permitted* state that honest coverage accounting produces, whereas `waived` is *prohibited* by (w1), so a report emitting it is non-conforming on its face. A prohibition no assertion tests is not enforced; a permitted state that failed an assertion would punish correct reporting.

**(7) It authorises no retro-fitting.** Text adopted or amended after a run does not reach a case already run, and a licence claimed after a case was reported is not a licence.

**(8) It licenses nothing after tuning** (item (7) above).

3. **Excessive false alarms on clean cases, under the default configuration** → the affected detector **or mode** ships marked experimental, is excluded from `assert_no_proven_leakage()` and `assert_no_rule_violations()`, and is labelled experimental wherever its findings appear.

**[v30a INSERT — SC-13c]**

**INTERACTIONS OF THE CRITERION ABOVE — v30a [SC-13c].**

**(c1) ADOPTION, AND THE ONE NAMED DEPENDENCY — ONE WAY.** The criterion (SC-13a with SC-13b and
this clause) is drafted against **§6.2 criterion 3 as amended by this registration** and **is not
adoptable without that amendment**: under registered line 461 unamended, SC-13a(a2)'s
corrected-side requirement is dischargeable only by failing §6.2 criterion 3, and a registration
cannot contain a kill criterion dischargeable only by failing an acceptance criterion. **The
dependency runs one way.** The criterion-3 amendment does not depend on these clauses and remains
admissible alone; adopting it without them leaves the registration consistent, adopting them
without it does not, and no reverse dependency is created here. Until the `prereg-v30a` tag is
signed, line 461 stands unamended and these clauses are not adoptable at all. A `DEVIATIONS.md`
entry or a working resolution cannot substitute for the amendment (line 1033; SC-12 item (5)).

**(c2) THE LINE-816 EXCEPTION — EXPRESS, SCOPED, AND RECORDED.** `PREREG.md` line 816, verbatim:

> **A combination that is `not_applicable` on every scope-eligible case in a body of data
> publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

**For the quantities this criterion requires — the per-detector, per-side `preserving` proof
yields SC-13a(a2) gates, that gate itself, and the published yields (c4) requires — line 816's
suppression clause does not apply.** Its publication clause applies in full and is required:
counts published, reason named, and — for this criterion — the computed yield and the gate outcome
published with them, per SC-13b(b3). A gate suppressed on the `not_applicable`-everywhere fact is
a detector waived on it — SC-12's definition, head and limb (iii) — and line 1035 forbids the
waiver. **The exception rests on this amendment's class C authority and on that capability ground;
it does not rely on `PREREG.md` line 818, whose text stands as registered.**
**This is a class C change to how line 816 reads at this one criterion, it is recorded in the v30a
amendments block in terms, and it reaches nothing else**: everywhere outside this criterion, line
816 governs exactly as registered. **The registered conflict between line 816 and line 830 is NOT
resolved by this clause** — it is recorded in the amendments block as a duplicated-authority
defect and flagged for a future amendment; no reading of this clause settles it anywhere else.

**(c3) WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the
detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination
rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows (lines 759 and 760), and
line 1039's "both of L2a/L3.1's combinations". The declaration supplies each governed detector's
labelled-unit set; it does not supply the membership of the governed set, may not shorten it, and
may not reach the same effect by enumerating a set for some of them and omitting the rest. **A
declaration that enumerates a set for fewer than all of the governed detectors has not discharged
SC-13b, and the criterion is not discharged.** SC-12, as revised with these clauses, pins the same
set to the same registered sites, and the two clauses never diverge on it.

**(c4) EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED.** Proof yield is registered for the
`preserving` combination only. A criterion stated in proof-yield terms therefore scores one
combination, and dropping the other from the criterion **waives that combination**. So: the other
combination is **executed to a terminal result on the same denominator and publishes its own
registered yield**, per detector and per side, and **no finding of that combination substitutes
for a proof the criterion requires**. Its published yield is a required output of the criterion
and carries no threshold of its own. Where that combination is `not_applicable` everywhere, (c2)'s
exception covers its required published yield the same way: executed to terminal states, counts
and reason and yield published, nothing suppressed.

**(c5) THE REMAINING FLOOR LIMBS ARE CARRIED BY CITATION, AND THIS CLAUSE NAMES WHICH VERSION IT
CARRIES.** Line 1035's second and third limbs remain in force over the criterion exactly as
written there. **Where "criterion 3's gates" admits more than one referent, every referent is held
in force** — they operate at different levels and do not conflict, and holding all of them is the
only reading that is not a weakening. **Each referent is held in the version this registration
leaves standing, and this clause says which:**
**(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461. **Its
scoring rule and its three dispositions are SC-3(b)'s, and **its map, its indexing, and what the
artifact publishing it may carry are SC-3(a)'s — all held by citation and none restated here.**
*(R49/B7: this clause previously restated (a)'s indexing triple in the same breath as declaring it
unrestated. R47/P5 then amended (a) and left the copy behind, so the copy became DIVERGENT — it
lacked (a)'s carve-out for artifact rows that are not cells of the map. Two normative copies of one
rule is §0.2.1 line 77's defect; the second copy silently going stale is why.)* **The cell key is
the declaration's to supply,
not this clause's to state**: SC-3(a) requires that a key exist and be declared and named; SC-3(h)
and SC-8 require it frozen with the map before any detector runs; and this clause names no key.
**It is never the pre-amendment prohibition on any finding on the corrected fixture**, and this
clause may not be read against that text.
**(c5)(ii) — the §10.2 referent is §10.2 criterion 3's own two named gates**, the finding-rate
gate and the completion gate, in force as registered and per combination, and **not amended by
this clause**.
**Why the version is named rather than left to the reader.** A clause whose meaning depends on
which version of criterion 3 the reader happens to hold is the defect, not the fix: under the
pre-amendment text SC-13a(a2)'s corrected-side requirement and criterion 3 contradict each other,
and under the amended text they do not. **This clause states no gate of its own on this limb**; it
adds SC-13a's threshold to the floor's first limb and SC-13b's admissibility test, and it changes
neither of criterion 3's gates.

**(c6) WHAT THE CRITERION DOES NOT REACH, AND WHAT DOES NOT REACH IT.** It is a kill/pause
criterion over the runtime detectors. **It creates no acceptance criterion, amends none, and is
never cited against one.** The descriptive fixture proof count of §6.2 remains descriptive and
non-gating **for §6.2**; these clauses make proof yield gating **for this criterion only**, which
is what line 1035's first limb already requires, and they promote no other count to a gate
threshold. A fixture evaluated under this criterion is still evaluated under the labelled
hypothetical declaration and **still does not carry full acceptance weight** (§6.2).
**And in the other direction, stated because it is the collision these clauses exist to resolve:**
a declaration statement that assigns a finding's character to a detector row and places it
**outside an acceptance gate** does not place it outside **this** criterion, and does not remove
that detector from the criterion's denominator, from SC-13b's admissibility test, or from
SC-13a(a2)'s gate. **A jurisdictional routing statement written about the acceptance gate reaches
the acceptance gate and stops there.** Removing a detector from this criterion is a waiver, and
the floor forbids it.

**(c7) WHAT THE CRITERION IS FOR, so it is not read as a quality bar.** It fires on an approach
that is **broken**, not on one that is **incomplete**. A detector that probes few cohorts, proves
what it probes, and publishes its coverage honestly **passes this criterion and is supposed to**;
its limitations are reported as numbers, not converted into a stop. **Partial capability honestly
reported is the designed outcome of this programme and is never by itself a kill condition.**

   - **Finding-rate gate:** with **N** = clean cases whose `schedule_state` ∈ {`completed`, `incomplete`} and **k** = those whose `evidence_outcome` is `finding`, fail at **k ≥ floor(0.20 × N) + 1**. With N = 25 that is 6; with N = 10, 3; with N = 16, 4. *(v24 gated on `floor(0.20 × completed clean cases) + 1` while §7.7 had already moved the rate's denominator off completion. On 25 in-denominator cases of which 16 complete and 4 emit false findings, the rate reads 16% and passes while the gate computes 4 and fails — the same run shipping or not shipping experimental depending on which sentence an implementer read.)*
   - **Completion gate, separate and joint:** if fewer than **60%** of those same N cases reach `completed`, the detector or mode ships experimental regardless of its finding rate. The two gates close a gaming pair — the finding-rate denominator admits cases that crashed before executing, which a detector could hide behind by failing on hard clean cases, and the completion floor is what stops that.
   - **Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others.
   - A point-estimate rule; a confidence-bound rule at these sample sizes would block nearly every detector, and the instability is stated rather than hidden.
4. **Any phase competing with September or 1 November** → pause.
5. **Not installable by a stranger by 15 October** → stop and resume after 1 November. A date, not a phase number.
