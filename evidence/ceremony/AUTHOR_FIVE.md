# AUTHOR_FIVE — the five load-bearing clauses, verbatim

**What this is (§141.2).** The verbatim text of the clauses the author read on **25 August 2026**
before approving the v30a pair, placed in the evidence tree beside the record of what was read.
**It is for the ARCHIVE, not for the approval** — the approval is recorded at
`ceremony/APPROVAL_RECORD.md` and did not depend on this file existing.

**Source of record.** `SCHEMA_SET_FINAL.md`, sha256 `32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc`.
Every clause below was lifted from it at generation time and **its digest verified against the
record before use** — the same check the diff generator applies. Nothing here was retyped.

**Two independent extraction paths (R92).** Path A slices the record's declared range and
verifies its digest; **path B locates the clause by HEADER SEARCH and never reads the stored
range**. Neither is derived from the other, so a range mis-pinned at authoring time — the R79
failure — cannot pass both. Every clause below matches on both paths.

**Six entries for five clauses:** `SC-3-C2op` and `SC-3-C2ret` are the two halves of the §10.1
kill-gate pair and are never read or applied apart (a pair is never fixed on one side only).

---

## SC-3 — §6.2 criterion 3 — runtime findings scored against the declared ground-truth map

| | |
|---|---|
| target | `PREREG.md` line **461**, REPLACE_LINE |
| source | `SCHEMA_SET_FINAL.md` lines 303–359 (57 lines) |
| clause sha256 | `b7a57f75392a820fe885c44231d9a7e2fbccb65973f6ab88852b40a3f9a254f5` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
**THE CLAUSE.**

> **3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH
> MAP — v30a, operative. [SC-3]**
>
> **(a) WHAT THE MAP IS.** The map is an **enumeration of expected findings**, declared in the
> fixture's availability declaration, stated **per side**, **per declared violation class**, and
> **per declared cell** of the declared scored population. **The declaration declares the cell key —
> the unit it declares the fixture to be partitioned into — and names it explicitly.** The map is
> published as an artifact with a **declared schema**: one row per cell of the declared scored
> population, with every field named, including the field that records whether the cell is
> scored. **The artifact may in addition carry rows of a class the declaration declares
> DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no
> criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the
> map's cells, not over the artifact's row count**. A count taken from the artifact without
> excluding them counts a different population, and **every figure published from the artifact
> names which population it counts**.
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

```

## SC-3-C2op — §10.1 criterion 3 — the kill gate's operative item, consequential to SC-3

| | |
|---|---|
| target | `PREREG.md` line **1022**, REPLACE_LINE |
| source | `SCHEMA_SET_FINAL.md` lines 1782–1782 (1 line) |
| clause sha256 | `4c18ca940288cf36726263598416eb941e9384943884c6cc537ffff6a46b1eda` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
```

## SC-3-C2ret — §10.1 criterion 3 — the retention block, registered v30 text, NOT operative

| | |
|---|---|
| target | `PREREG.md` line **1022**, INSERT_AFTER |
| source | `SCHEMA_SET_FINAL.md` lines 1788–1788 (1 line) |
| clause sha256 | `6a8fdb49e45cac4eabf864397f1df0fe576705dded8f63f7f0fc416f14cf763c` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired **as to its corrected-side limb only**, because that limb is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. **The contaminated-side limb and the ambiguity branch are carried into the operative item byte-identical** (R47/P1); the contaminated-side tightening an earlier draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

## SC-12 — §10.2 — the replacement-criterion floor, and `waived` DEFINED

| | |
|---|---|
| target | `PREREG.md` line **1035**, INSERT_AFTER |
| source | `SCHEMA_SET_FINAL.md` lines 1081–1126 (46 lines) |
| clause sha256 | `8d4bb936ab1dabf9a9d5e4f3282c3a1bb5ce541e3f1e5434b0836108476d3e60` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
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

```

## SC-13a — §10.2 criterion 2 — the replacement criterion

| | |
|---|---|
| target | `PREREG.md` line **1030**, REPLACE_LINE |
| source | `SCHEMA_SET_FINAL.md` lines 1282–1343 (62 lines) |
| clause sha256 | `05a3803fe3ad38f86590e599b76ce6575480c38046e25e9ebe0adf169753d700` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
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

```

## SC-4 — §6.2 — the scored-set partition and criterion 1's denominator

| | |
|---|---|
| target | `PREREG.md` line **464**, INSERT_AFTER |
| source | `SCHEMA_SET_FINAL.md` lines 410–571 (162 lines) |
| clause sha256 | `115be757717c68e5e3687484e47611d3abf82f1f97c754e1fde035282e1f5184` — **VERIFIED** |
| two independent extraction paths (R92) | path A = stored range, digest-verified; path B = located by HEADER SEARCH, never reading the stored range — **MATCH** |

```
**THE CLAUSE.**

> **The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]**
>
> **(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY THE RULE REGISTERED HERE, AND THE
> DECLARATION SHOWS THE DERIVATION.** The rule by which each unit of the declared scored set is
> assigned its gate class is **registered in this clause — the class predicates of (b), under the
> precedence of (c) — and is not the declaration's to state, restate, or rewrite.** The declaration
> states, **ex ante, in full, and per unit**: the class assigned, and the registered predicate the
> unit satisfies, **by citation to the row of (b) that carries it**, together with the declared
> facts on which the unit satisfies it — what the map declares on it on the scored side under the
> declared branch, and the construction and legality facts the declaration records for it. The
> classes are **derived by the registered rule over those declared facts, never assigned by hand.**
> **No companion document states a class predicate in rule form** — as a biconditional ("CLASS iff
> …") or otherwise: the predicate is cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f)). An
> evidence artifact's classification of how a unit was *built* answers a different question from
> what the map declares *violating* on the scored side under the declared branch; the two do not in
> general have the same answer. **No classification of the scored set other than this derivation
> enters any criterion, denominator, or count**, and no split within such a classification carries
> gate arithmetic. Any report quoting such a count names the scope it counts under.
>
> **(b) EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE DECLARED SCORED SET.**
>
> | Class | Registered predicate (cited by the declaration, per unit; never restated) | What a finding on it means |
> |---|---|---|
> | **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
> | **OUT OF JURISDICTION** | every constituent read is declared legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
> | **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |
>
> **The declaration cites these rows, per unit, and states the facts on which each unit satisfies
> the row it cites; it does not restate them** (a). **There is no fourth class and no residue
> class.** **N is the length of the REQUIRED list**, and no other quantity is N.
>
> **(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED
> wins.** The declaration derives under this precedence and states none of its own; a unit's class
> is the first the order yields, and for each unit that satisfies more than one predicate the
> declaration records which it satisfies and that precedence decided it.
>
> **(d) THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE
> DERIVATION.** Where a registered class predicate admits two readings, the declaration states which
> it derives under and why, before any detector runs. **Two readings are registered as forbidden
> outright**, because each silently removes units from the arithmetic: (i) a locality condition may
> not be read more narrowly than the declared lattice, so a read of the same source at another
> instant of the same lattice does not by itself create a cross-source violation; (ii)
> **unconstructibility in some other rebuild of the fixture is never gate-unscoredness** — only a
> gate status the declaration declares EXCLUDED on the artifact the gate actually scores removes a
> unit from the arithmetic.
>
> **(e) GROUNDS FOR EXCLUSION ARE DECLARED, AND DECLARED PRE-RUN.** A unit is excluded only on a
> ground the declaration states. Two grounds are registered here because each is otherwise a
> guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that
> cannot carry a finding of the scored class at all** (leaving it in the denominator makes criterion 1
> unsatisfiable), and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot
> be scored under any reading). **Reinstating an excluded unit changes the denominator and is class
> C.**
>
> **(f) PUBLICATION DISCIPLINE — the constraints below, and they are the point of the rule.**
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
>
> **(k) TWO MECHANISMS AGAINST A COLLAPSING SCORED POPULATION, AND NEITHER IS SUFFICIENT ALONE.**
> There are two ways criterion 1 stops meaning anything, and they need different instruments. The
> population can go **empty** — the degenerate case, caught by the floor at (k1). Or it can be
> **narrowed unit by unit** until what survives is not worth scoring — the gradual case, caught by the
> reconciliation at (k2). **(k1) alone is satisfied by scoring a single column.** It is written below
> as the terminal backstop it is; **the operative protection is (k2)**, and a reader who takes the
> backstop for the mechanism has mistaken which failure this clause exists to stop.
>
> **(k1) THE FLOOR — THE TERMINAL BACKSTOP.** The declared scored set and the REQUIRED list are
> enumerated by name **before any detector runs** and are **non-empty on every declared side**. **If
> either is empty on any declared side, criterion 1 is not discharged and the outcome is STOP** —
> lifted only by supplementing the declaration with declared, enumerated units for that side and
> re-freezing under §11's integrity chain; never by scoring criterion 1 on the remaining side, never by
> suppressing the empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution.
> **Non-emptiness is the whole of this limb, and deliberately so:** any minimum above zero would be a
> threshold chosen from the distribution this fixture already exhibits, which §7.0 forbids. A floor
> that cannot be set without looking at the data is not set. **This limb therefore catches only the
> degenerate case; it is not the protection and must not be cited as one.**
>
> **(k2) THE RECONCILIATION — THE OPERATIVE MECHANISM.** The REQUIRED list is published alongside a
> **per-unit reconciliation against the fixture manifest's list of columns classed as leaking
> sources** — the **named list**, not the count. **Every unit the manifest so classes that this
> derivation does not class REQUIRED is named**, with **the registered predicate of (b) that produced
> its class** and the declared facts on which it satisfies that predicate. A difference stated as a
> count, a total, or a summary of where the differences "mostly" sit does not satisfy this limb; the
> unit is named or it is not reconciled.
>
> **(k2)(i) EVERY GROUND NAMES THE ARTIFACT AND LOCATION THAT SUPPORTS IT.** For each such unit the
> declaration cites **the artifact and the location within it** — file, and row, line, or field — on
> which the declared facts rest. **The quality of a ground is not something this registration can
> require**, and pretending otherwise would be vagueness dressed as a constraint; **provenance is.** A
> ground with an artifact behind it can be looked up and disagreed with. **A ground with nothing
> behind it becomes visible as such**, which is the whole of what this limb can achieve and is worth
> more than a bar no reader could apply.
>
> **The list is a publication input, and the count remains not a gate number.** Reading the list under
> this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
> denominator — (k3) governs, and §6.2 line 446's manifest requirement is unamended. **Because the
> gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
> in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
> own later revision cannot decide a gate outcome; an author review that silently made a complete
> reconciliation incomplete would be a change to a gate input outside the class C route.
>
> **(k3) A DISCLOSURE, NOT A CLASSIFICATION — AND THE LIMIT OF WHAT A READER CAN CHECK.** **A
> reconciliation published under this limb is a disclosure, not a classification entering a criterion,
> denominator, or count** (a). It derives nothing, changes no class, and no quantity appearing in it is
> N. That sentence is load-bearing: without it (a) forbids the very comparison that makes the
> denominator auditable, and the limb would contradict the clause it sits in.
>
> **What a third party can and cannot do with it, stated plainly rather than implied.** The declared
> map and this reconciliation are published with the registration; **the acceptance fixture is not,
> and no clause requires it to be.** So a reader can check the reconciliation for **completeness**
> (every manifest-classed leaking source accounted for), for **internal consistency** (each ground
> citing a registered predicate), and for **provenance** (each ground naming an artifact and
> location) — and **cannot** independently verify a classification against the fixture's data. **This
> limb is therefore a disclosure obligation with limited external verifiability, and it is registered
> as one.** Claiming it delivers an audit a reader cannot perform would be the same defect as an
> overstated availability claim.
>
> **(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared
> side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named
> without the registered predicate that produced its class, **or is named with a ground that cites no
> artifact and location (k2)(i)**; **or where the manifest the reconciliation reads is not enumerated
> in the declaration's SC-8(a) freeze, or carries a `DRAFT` status at the tag (k2)**. *(Both of those
> last two are conditions (k2) states, and until R60 neither was indexed here — a limb may not impose
> a condition and leave nothing to enforce it. **Both are unmet as at the date of this amendment**:
> the freeze's "specifically and exhaustively" list does not name the manifest, and the manifest's
> recorded status is still `DRAFT - author review required`.)* **This is a live gate item, not a check that only fires on
> corruption: it can fail on an artifact that is behaving correctly, and on the fixture as declared at
> the date of this amendment it is UNSATISFIED.** The declaration publishes a per-unit
> cross-tabulation of the construction-SOURCE cut against the gate cut, which is a different pair of
> partitions; it publishes no per-unit reconciliation against the manifest's leaking-source list. The
> difference the limb would surface is **fourteen units**.

```

