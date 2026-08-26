# SCHEMA SET — FINAL: SC-1 … SC-13c AS CORRECTED THROUGH R32 (S1), THE THREE DRAFTED INSERTIONS (S2) AND Q4's THREE DEFECTS (S3) — READY TO APPLY

**This file supersedes, for the clause text only, `SCHEMA_SET_ADOPTION.md` (SSA).** SSA was not
edited and stands as the superseded record. Where this file is silent, SSA's Part 2 (the Q1 record),
Part 3 (the Q2 table), Part 4 (the Q3 R24 scan, 132 rows), Part 5 (ledger E-1 … E-21) and Part 6
stand and are cited, not reproduced; behind them, K1's §2 accounting (76 rows), §3, §4, §5 and the
split file's Parts 2/4/6/7 stand likewise. **The K1 accounting is unchanged by anything in this
file** — no row moves, no tally changes.

**Nothing in the repository was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md`
and `HISTORY.md` in `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01` are untouched —
re-verified at the end of this pass: `PREREG.md` sha256 `f0a8f001…c7cc6` (1,099 lines),
`AVAILABILITY_DECLARATION.md` `f0829bd3…3310` (3,684 lines), `tools/check_registration.py`
`30d3ad4c…7425`, HEAD `80401d0`, `git status --short` unchanged (` M AVAILABILITY_DECLARATION.md`, `
M DESIGN.md`, ` M tools/check_registration.py`, `?? .claude/`, `?? LICENSE`, `?? evidence/`, `??
tagmsg.txt`). **No state-changing git command was run** (only `git status --short`, `git rev-parse
HEAD`, `git tag -n20 prereg-v30`). The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not
read.

**Files written this pass.** This file. Under the scratch copy `…\8b1d67a4…\scratchpad\applied\`
("`applied\`" below): the applier `_apply_R32_S2_S3.py`; snapshots `_PREREG_preR32.md.bak` (the
K9/J9 applied file, `a0c899a4…2ef5`), `_DECL_preR32.md.bak` (the working-tree declaration,
`f0829bd3…3310`), `_PREREG_R32_S3_only.md.bak`, `_PREREG_FINAL_stepC.md.bak`; checker outputs
`_S1_step0_baseline_checker.txt`, `_S1_stepA_prereg_checker.txt`, `_S1_stepB_decl_checker.txt`,
`_S1_stepC_s2_checker.txt`; pytest outputs `_S1_stepB_pytest.txt`, `_S1_stepC_pytest.txt`. The
scratch `applied\PREREG.md` and `applied\AVAILABILITY_DECLARATION.md` now carry the final applied
state (Part 2.4, file identities). `applied\CI_GATE_RESULT.md` was renamed to
`_CI_GATE_RESULT.md.hold` for the duration of the four checker runs (it is a scanned `.md` that
flags its own quotations — CI report §6 note) and renamed back unchanged. Two helper scripts live in
this session's own scratchpad (`build_final.py`, `write_final.py`): they carry SSA's Part 1 into
this file programmatically, apply the ledgered edits with asserted match counts, and verify every
edited paragraph against the scratch-applied text (Part 1's convention note).

**Read state this pass.** `PREREG.md` = 1,099 lines; `AVAILABILITY_DECLARATION.md` = 3,684 lines
(both tool-counted). Read: SSA in full (1,840 lines); `applied\CI_GATE_RESULT.md` in full;
`tools/check_registration.py` lines 55–170, 285–432, 440–700, 822–880 (the scratch copy =
working-tree copy, hash-verified); the Q4 record (`tasks\wndeu4eu9.output`, `result.q4`, all
findings and blockers); `PREREG_v30a_DIFF.md` H8 (lines 375–400);
`J1_GATE_CRITICAL_CLASSIFICATION.md` lines 376–391 (R23); `HISTORY.md` lines 215–219 (H-L11 …
H-L13); the repo's `tagmsg.txt` and `git tag -n20 prereg-v30` (the executed tag carries five
hashes); `PREREG.md` lines 70–104, 845–865, 900–969, 1040–1099; `AVAILABILITY_DECLARATION.md` lines
1025–1143; the applied scratch `PREREG.md` at every edit site. **Read, not edited** — except the
scratch copy, by permission.

**What this file contains, in the order the brief lists it.** **§0** conventions (carried, §0.1 list
corrected, application order updated) · **PART 1** the complete set SC-1 … SC-13c as now corrected,
verbatim, with the three S2 insertion texts in place under SC-6 / SC-8 / SC-11 · **PART 2 (S1)**
rule 9 quoted; SC-4 before/after; the declaration-side K4 proposal for lines 1047–1056; the scratch
re-run — command, full stdout, exit code, counts, delta classified; pytest · **PART 3 (S2)** the
three insertions — anchor verbatim with match count, text verbatim, one-line justification, the
H-L13 principle · **PART 4 (S3)** Q4's three defects, before/after · **PART 5** change ledger vs SSA
· **PART 6** carried open · closing tally.

---

## 0. CONVENTIONS (carried from SSA §0; §0.1's list corrected; application order updated)

**0.1 The heading tag `[SC-n]`** — unchanged from SSA §0.1: wherever applied clause text says
"SC-n", it means the clause whose heading carries the tag `[SC-n]`; "SC-n(x)" means the lettered
limb (x) inside it. Applied uniformly to SC-1 … SC-12 and SC-13a/b/c. **The cross-citation list that
must be resolved to section numbers if the author strikes the tags on SC-1 … SC-12 is, corrected for
Q4's nit (SC-6(c) was omitted):** SC-3(b) "(SC-6)", SC-3(h) "(SC-8)", SC-4(a) "SC-9(a), SC-9(f)"
(new, R32), SC-4(b) "(SC-6)", SC-5(a) "(SC-4)" and "(SC-3)", SC-6(b) "see SC-12", **SC-6(c) "(SC-3)"
and "(SC-4)"**, SC-7(e) "(SC-8)", SC-10(a) "SC-8", SC-11(g) "(SC-6)", SC-12 items (4) "(SC-6)" and
(5) "(SC-9(c), SC-9(e))"; plus the three S2 texts' citations — §8.2's "[SC-6]", §8.6's "[SC-11]",
§11 item 8's "[SC-8]" and "SC-8(f)" — and §13c-P's "[SC-13c(c2)]". The R32 declaration-side text
(Part 2.3) cites "SC-4(a)", "SC-4(b)", "SC-4(c)", "SC-4(e)", "SC-4(h)", "SC-9(a)" and resolves the
same way.

**0.2 What is applied text and what is apparatus** — unchanged from SSA §0.2 (only **THE CLAUSE**,
**SUPERSESSION MARKER** text at the superseded site, and — new — the **INSERTION TEXT** blocks enter
`PREREG.md`; REGISTERS / INSERTION POINT / DATA / ROWS / *Instance record* are apparatus), with one
addition: **the declaration-side text in Part 2.3 is a proposed K4 edit to
`AVAILABILITY_DECLARATION.md`, applied only to the scratch copy, not to the repo.**

**Application order, one tag.** SSA's fixed order stands: **SC-12 (revised) → SC-13a → SC-13b →
SC-13c → §13c-P → §AB**; for SC-1 … SC-11 ascending anchor order is the suggestion and is what the
CI gate followed (CI report §1.3, 30 hunks). **The three S2 insertions slot in as follows** (the
scratch run applied them in exactly this way, Part 2.4 step C): S2(i) after SC-6's marker M2 at §8.2
(pristine anchor line 915); S2(iii) after §8.6's line 961; S2(ii) as §11 item 8 after item 7 (line
1054), followed by the item-3 marker, with SC-8's M2 marker revised in place and the line-97 marker
placed after §0.2.1 line 97. Anchors are against the live 1,099-line `PREREG.md`; **every later
anchor is re-derived after any earlier edit lands** — H1's full-line convention (refuse on zero or
multiple matches), which `_apply_R32_S2_S3.py` follows and which every hunk of this pass satisfied
(match count 1 at every site, Part 2.4).

---

# PART 1 — THE SCHEMA SET, AS CORRECTED THROUGH R32 / S2 / S3, VERBATIM, READY TO APPLY

Convention for each clause (K1's): **REGISTERS** · **INSERTION POINT** · **SUPERSESSION MARKER** ·
**THE CLAUSE** · **DATA THE DECLARATION MUST SUPPLY** · **ROWS COVERED** — plus, new this pass and
applied text, **INSERTION TEXT** blocks under SC-6, SC-8 and SC-11 carrying the three S2 insertions.
Text is SSA Part 1's verbatim (carried programmatically from `SCHEMA_SET_ADOPTION.md` lines 76–1375)
except where the change ledger (Part 5) records an edit; every edit is marked in the ledger by
clause and limb, and every edited applied paragraph was verified this pass to equal, word for word
after whitespace normalisation, the text applied to the scratch `PREREG.md` and run through the
checker (Part 2.4).

---

### SC-1 — THE DECLARED AVAILABILITY MODEL IS THE GATE'S SEMANTIC AUTHORITY

**REGISTERS.** That the declaration, not the specification and not a role name, fixes the meaning of
every term the comparator reads; and the four ways a declaration can fix it wrongly.

**Self-count discipline (R37/D5).** SC-1's clause previously opened its enumeration with "Six
requirements follow". The numeral is now dropped: the limbs are lettered (a)-(f) and the count is
read off them. This is the shape `HISTORY.md` H-L13 records — a literal whose obligation to be
re-bumped lives outside the edit that grows the target — and it is the same shape SC-8(f) forbids
for the hash set, so the amendment should not commit it while removing it from §11.

**The scan, corrected at DELTA R39/F5 — and the earlier version of this paragraph was wrong.** It
claimed a scan of every clause had found "three further in-clause numerals" and defended all three.
The scan was incomplete: it missed at least five, and **two of the five were not closure statements
at all**. A false statement about a scan is worse than the defects the scan missed, because it tells
a later reader the ground has been covered.

**Fixed as fragile counts** — each enumerates without forbidding growth, so adding an item silently
falsifies the numeral, which is exactly H-L13's shape:

- SC-4(f), was "PUBLICATION DISCIPLINE — **three constraints**"; now "the constraints below". Its
  items 1–3 carry no "and no fourth".
- SC-10(d), was "**FOUR** FORBIDDEN USES OF NON-GATE DATA"; now "FORBIDDEN USES". Its items (1)–(4)
  carry no closure sentence either.

**Kept, because in these the number IS the rule** — it is what closes the set, and striking it would
delete a constraint rather than de-fragilise a reference:

- SC-4(b) "EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE", which continues "**There is no
  fourth class and no residue class.**"
- SC-3(b) "THREE DISPOSITIONS, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE MAP" — exhaustiveness is
  asserted in the heading itself.
- SC-6(c) "TWO LEVELS, AND THEY DO NOT COLLAPSE" — the count is the non-collapse rule.
- SC-7(a) "A DETECTOR RECEIVES EXACTLY TWO THINGS" — "exactly" is the input-surface restriction.
- SC-4(e) "Two grounds are registered here" and SC-13c(c2) "rests on two grounds **and on no other**".

**The test, stated so the next scan does not have to re-derive it:** if growth silently falsifies the
numeral, it is a stale reference and H-L13 applies. If growth is what the numeral forbids, it is a
closure constraint and removing it is a weakening §0.2.1 line 97 does not permit.

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
> the one the declaration declares. The requirements below follow, and a declaration that does not meet
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

**DATA THE DECLARATION MUST SUPPLY.** The map artifact and its schema; the cell key and its name; the
declared violation classes; the declared scored population and its subclasses; the per-cell expected
findings; the unscored ledger; any reporting re-aggregation with its delta.

**ROWS COVERED: 5, 6, 26, 55, 56, 74, 89, 95.**

---

### SC-4 — THE SCORED-SET PARTITION, AND CRITERION 1's DENOMINATOR

**REGISTERS.** That criterion 1's denominator is **derived** from the declared availability model by
**class predicates registered in this clause, applied to declared facts, the derivation shown per
unit by citation**; that the derivation yields a three-class partition of the declared scored set;
and the discipline that makes the partition auditable.

**INSERTION POINT.** After `PREREG.md` **line 464** (`Secondary findings on **manifest-listed
descendants** …`), carrying H1 hunk **H6**'s placement. Criterion 1's own text at line 459 **stands
byte-exact**; this clause states how its denominator is constituted, which the registered text left to
be inferred.

**SUPERSESSION MARKER.**

> **§6.2 line 459 — v30a. THE TEXT IS UNCHANGED; THE REQUIREMENT IS NOT.** *(Corrected at R54/W3.
> This marker previously read "**ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact." The first
> clause is true byte-for-byte and false at the outcome, and §0.2.1 line 97 measures at the outcome.)*
>
> **What is superseded is the INFERENCE** that the denominator is any construction-taxonomy count
> recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it.
>
> **WHAT THAT DOES, STATED AS ARITHMETIC BECAUSE THE CONSEQUENCE IS NOT VISIBLE IN THE DIFF.** The
> fixture manifest classes **25** of the 35 fed columns as leaking sources. Under the SC-4(b)
> partition:
>
> | manifest class | gate class | count | what a finding on it means |
> |---|---|---|---|
> | LEAK-SOURCE | REQUIRED | **11** | absence is a **miss** |
> | LEAK-SOURCE | OUT OF JURISDICTION | **13** | a finding is a **FALSE POSITIVE** |
> | LEAK-SOURCE | UNSCORED | **1** | neither for nor against |
>
> **On 14 of those 25 columns the gate's requirement REVERSES SIGN** — from *absence is a miss* to
> *a finding fails the gate*. **That is a supersession at the outcome, and it is recorded as one
> here**, whatever the byte-level text of line 459 does. It is made under the class C rule, which
> permits it; what §0.2.1 line 97 does not permit is making it while recording that nothing changed.
>
> **A reader comparing v30 and v30a byte-for-byte at line 459 will see no change and conclude
> wrongly.** That is why this is also carried as a disclosure on the face of the amendment (R54/W4,
> disclosure 7) rather than left here alone.
> **§6.2 line 446 — NOT AMENDED.** The manifest requirement stands; only the *arithmetic role* of
> what it records is constrained, which is a statement about denominators, not an edit to line 446.

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

**DATA THE DECLARATION MUST SUPPLY.** Per unit, the class assigned and the registered predicate
satisfied, cited to (b) by row, with the declared facts on which the unit satisfies it; the named
constant identifying the scored set; the three enumerated class lists; for each unit satisfying more
than one predicate, the record that (c)'s precedence decided it; the reading it derives under at
each edge; the declared exclusion grounds and the units excluded on each; the printed partition
check; N. **Not** a rule-form statement of any predicate (a).

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
   mistakable for a pass.", which is the existing hook; where marker M2 below is already placed at that
   site, the insertion follows M2. **Operative text: the INSERTION TEXT block below (S2(i), drafted this
   pass; Part 3).**

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

**INSERTION TEXT — §8.2, after `PREREG.md` line 915 (after marker M2 where placed) — S2(i).**

> **`unscored` — §7.7 (v30a) [SC-6] — is governed by this section's closing sentence as well.** It
> is neither a pass nor a not-run: this section's boundary sentence does not reach it, and its entry
> condition and semantics are SC-6's, not restated here. It is named here so that this section and
> §7.7's row cannot name different states — the closing sentence above ranges, by reference to
> §7.7's row and not to the enumeration in this section alone, over every detector-case coverage
> state that row carries other than `passed` and `failed`.

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
2. **§11 item 8**, added after line 1054 (item 7), so registration integrity indexes the freeze **and
   carries the hash-count rule** (R23; H-L13 open form) — text in the INSERTION TEXT block below (S2(ii),
   drafted this pass; Part 3). Two supersession markers accompany it: one beneath §11's list (item 3's
   file set), one after `PREREG.md` line 97 (§0.2.1's "both").

**SUPERSESSION MARKER.**

> **§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED.** The locked ordering stands byte-exact. SC-8
> states what the ordering ranges over and what happens when a frozen object is later found wrong,
> which line 480 left unstated.
> **§11 items 1–7 — v30a, EXTENDED.** Item 8 is added: it indexes the freeze (SC-8) and amends item
> 3's hash set; SC-8(f) states the requirement generically and does not fix a count.
>
> **§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT.** The registered v30 item
> names three files; the `prereg-v30` tag as executed enumerated five. The requirement — SHA-256 as
> committed, in the tag message and the README — stands byte-exact; the file set and its count are
> item 8's, derived from the tag message's own enumeration, and the three names are retained as the
> v30 record and are NOT the set.
>
> **§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT.** "both file hashes in the
> tag message" records the count at the time of writing; it is superseded as a count by §11 item 8,
> which derives the count from the tag message's own enumeration. The requirement — that an
> amendment inherit §11's integrity chain in full — stands byte-exact.

**INSERTION TEXT — §11 item 8, after `PREREG.md` line 1054 (item 7) — S2(ii).** *(Item 8 is inserted
as the list's eighth item; the item-3 marker and SC-8's revised M2 follow the list; the line-97 marker is
placed after line 97 in §0.2.1.)*

> 8. **The freeze, and the hash set that carries it — v30a.** What freezes at an amended
> registration's tag, in what form, and what may not happen to it afterwards is stated in §6.2
> (v30a) [SC-8] and is not restated here. The tag message of this registration and of every
> amendment to it carries the SHA-256, as committed, of **every registered document and every
> registration tool** — the registration and its checking tools as item 1 names them, every document
> an amendment registers under §0.2.1 (the availability declaration included), and every file
> SC-8(f) requires hashed — **one hash beside one path, enumerated in the tag message itself.** The
> set is that enumeration and its count is read from it: no clause of this file states the count as
> a literal, and where an earlier clause names the hashed files or their number — item 3's three
> names, §0.2.1 line 97's "both" — it records the set at the time of its writing, stands as that
> record, and is superseded as the set by this item; the requirement it states stands. A registered
> file absent from the enumeration is a defect in the tag, not a file outside the chain.

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
> **(d) FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**
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
961** (§8.6) so the reporting section indexes it — text in the INSERTION TEXT block below (S2(iii),
drafted this pass; Part 3).

**SUPERSESSION MARKER.** None — pure insertion. No registered clause states a control over
aggregation; §8.6 governs provenance of numbers that exist and is silent on numbers that come back
empty.

**INSERTION TEXT — §8.6, after `PREREG.md` line 961 — S2(iii).**

> **A zero, an empty result, or an all-clean statement is a published number and carries provenance
> under this section.** The control it must survive before it may be reported, and what it must name
> when it is, are stated in §7.8 (v30a) [SC-11] and govern here; they are not restated.

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

**INSERTION TEXT — §7.7 pointer, after `PREREG.md` line 856 — Y3 §6.3.** *(MOVED INTO THIS FILE
at R80/§87. SC-12's INSERTION POINT names this pointer as applied text and said "The operative
pointer text is Y3 §6.3's" — so the applied text lived outside the source of record and this file
was INCOMPLETE. Transcribed verbatim from `Y3_WAIVED_ENTRY_CONDITION.md` §6.3, which now cites this
block as the single normative copy. Same correction DELTA R37/D1 made for SC-12(w)'s own limb text.)*

> **`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.

**SC-12(w) — ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE (item Y3, adopted at DELTA R35 B3).**
Full deliverable, with the judge-panel record and the non-weakening argument, in
`amendment/Y3_WAIVED_ENTRY_CONDITION.md`. The limb text as applied:

> **(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE — a prohibition, and a closed list of licensed grounds with no members.**
>
> §7.7's table carries `waived` as a detector-case coverage state and registers no condition under which a report may assign it. It is the only state in that table without one, and the omission is not cosmetic: **no runtime metric reads a detector-case state** (§7.2.1), and `assert_audit_complete()` reads it alone. A state the apparatus cannot bound by its consequences must be bounded at entry.
>
> **The direction of the bound is forced by limb (v) above.** Limb (v) makes assignment of this state one of the ways a detector *becomes* waived. Any permissive entry condition would license, in the definition's own words, the act the definition exists to name. The bound is therefore drawn as a prohibition.
>
> **(w1) THE CONDITION. NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.** The grounds on which this state may be entered are exhaustively enumerated in this limb; the enumeration is **closed**, and it has **no members**. No ground may be inferred from silence, from practice, from a report's convenience, or from the state's presence in §7.7's table.
>
> **(w2) EVERY DETECTOR-CASE TAKES THE COVERAGE STATE ITS CAUSE ALREADY SELECTS — cited, not restated.** §7.7's completion lock selects it where a terminal result is or is not reached; §8.2 draws the boundary between the not-run states and governs their display; SC-6(b) governs a unit the declaration declared unscoreable, by name, before any detector ran. Those rules dispose of every detector-case between them, and **the residue this state would have carried is empty.**
>
> **(w3) THE STATE RECORDS A WAIVER; IT NEVER MAKES ONE — and this governs every ground ever added.** Waiving is a property of how a criterion is **written, configured, or reported** — something a criterion's design does to a detector, never something a run does to a case. The coverage state can therefore only ever be the **record** of a waiver registered text has already effected under limbs (i)-(iv); it is never that waiver's source. **A report does not create a waiver by asserting the state.** Accordingly **no ground added to (w1)'s enumeration may be constitutive**, and **limb (v) may never be a ground under (w1)**; nor may an availability declaration, a working resolution, a `DEVIATIONS.md` entry, the frozen configuration of §6.8, or an `assert_audit_complete()` recorded exception.
>
> **(w4) THE PROHIBITION BINDS PER CASE AND PER COMBINATION.** A case may not be reported `waived` on one of §7.1's combinations and executed on the other. **Per-combination waiving is still waiving** (item (6) above).
>
> **(w5) AN ENTRY THAT APPEARS IS A BREACH, AND LIMB (v) IS WHAT CLASSIFIES IT.** By limb (v) the detector is thereby waived with respect to every criterion the case feeds. Where that detector is one the floor governs and the criterion is §10.2's replacement criterion or any part of it, the replacement is weaker than the floor and out of specification on its face, and **it does not become admissible by being recorded, disclosed, justified, or approved.** Everywhere else the case has reached no terminal result, is **not complete** under §7.7's completion lock, may not be counted or displayed as complete, covered, clean, or passing (§8.2), and is re-reported in the state its cause selects — or the fixture is not scored.
>
> **(w6) THE TOKEN IS NOT STRUCK FROM §7.7's TABLE.** The state stays in the vocabulary so that a report using it is **caught** by limb (v) and by this limb rather than silently accepted. Striking the name would leave the act unnamed, and limb (v) with nothing to classify.
>
> **(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` detector-case entries, **per detector and per combination**, as a count. **That count is zero.** A report that does not publish it has not discharged this limb: a prohibition whose observance is never published is not checkable.
>
> **What this limb does NOT permit.**
>
> **(1) It licenses the state in no case, and silence is not licence.** The empty enumeration is the whole of the permission. In particular, **a criterion's failure to name a detector licenses nothing**: a criterion that enumerates its detectors and omits this one, a criterion written before this detector existed, and a criterion that says nothing about detectors at all are **all silence for this purpose**. The omitted detector **bears on that criterion**, and its cases are executed to terminal results. Reading silence as licence would be waiving by omission — limbs **(i)** and **(iii)** above — and would move the licence from registered text to whoever last failed to update an enumeration.
>
> **(2) A ground may be added only by a further class C amendment to this limb** (§0.2.1 line 93), committed and externally timestamped **before the affected detector is implemented or evaluated** (line 95), never after a fixture result is observed (§6.2 line 480; SC-8). Any such ground must be **declaratory** under (w3). **And no such amendment may license the state for a detector the floor governs at a §10.2 replacement criterion**: the floor forbids that above, there is no procedure by which it may be done, and this limb supplies none and may not be cited as one.
>
> **(3) "No data" is still not "waived"** (item (4) above), and this limb creates no route by which it becomes so. A cell with no data is `unscored` where SC-6(b)'s declared-ledger condition is met; absence of data at run time is otherwise the not-run state its cause selects (§8.2). A run that produced nothing, a missing or impossible input, a crashed or failed strategy, and a surprising result are each disposed of there and by none of them does a case enter this state.
>
> **(4) "Experimental" is still not "waived"** (item (3) above). A detector or mode shipped experimental under §10.2 criterion 3 executes its cases and reports their terminal results; the marking changes how findings are **labelled and asserted on**, never which coverage state a case takes.
>
> **(5) Jurisdiction is not waiver.** What a jurisdictional routing statement reaches is settled at SC-13c(c6), cited and not restated. A boundary on **where a finding is charged** is never a licence to leave a case **unexecuted**.
>
> **(6) It amends no other coverage state's entry condition and moves no boundary in §8.2.** It reaches §8.3 in exactly one way, deliberately: `waived` joins `assert_audit_complete()`'s failure set at line 929, so that emitting the prohibited state **fails an assertion instead of passing silently**. That is the whole of its reach into §8.3 — no other assertion changes, and no other coverage state's treatment changes. **`unscored` is not added to that failure set, and must not be**: `unscored` is a *permitted* state that honest coverage accounting produces, whereas `waived` is *prohibited* by (w1), so a report emitting it is non-conforming on its face. A prohibition no assertion tests is not enforced; a permitted state that failed an assertion would punish correct reporting.
>
> **(7) It authorises no retro-fitting.** Text adopted or amended after a run does not reach a case already run, and a licence claimed after a case was reported is not a licence.
>
> **(8) It licenses nothing after tuning** (item (7) above).

**SC-12(w) SECOND INSERTION POINT — §8.3's assertion, so the prohibition is machine-checkable
(item B4, DELTA R35; measured contained before adoption).**

**WHY IT IS IN THIS AMENDMENT.** SC-12(w) registers a prohibition. Without this hunk no assertion
fails on a `waived` entry: §8.3's failure set is `unsupported` and `could_not_run` only, so a
non-conforming report emitting the state passes all three assertions, and the prohibition is
enforced by a human reading a published zero. Shipping a guard whose observance no machine checks,
in the same amendment that creates the guard, is shipping it knowingly incomplete.

**WHY IT IS CONTAINED — measured, not assumed.** `assert_audit_complete()` has no implementation:
the reducer implements `evaluate_runtime_assertions` for `assert_no_proven_leakage` only. The token
`waived` appears **zero** times in `protocol/runtime_reference.py`, **zero** times in
`tools/check_registration.py`, and **zero** times in `tests/registration/EXPECTED_OUTPUTS.md`. Its
one occurrence in the suite is `tests/registration/test_invariants.py`
(`test_no_runtime_metric_touches_detector_case_state`), which asserts the reducer **must not** name
it — an invariant this hunk preserves rather than disturbs, because §7.7's detector-case layer is
deliberately outside the reducer and exists, in `PREREG.md` line 820's own words, "for
`assert_audit_complete()` alone". The change is one registered sentence and cannot cascade.

**INSERTION POINT.** `PREREG.md` **line 929**, §8.3's third assertion bullet. Full-line match,
count asserted 1.

**SUPERSESSION MARKER — registered v30 text retained verbatim at its site, NOT operative:**

> **§8.3 line 929 — SUPERSEDED BY v30a, carried with SC-12(w).** Registered v30 text, retained
> verbatim, NOT operative: "- **`assert_audit_complete()`** — fails on any `unsupported` or
> `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable
> (§6.10). Ignores findings." *Superseded because SC-12(w) prohibits the `waived` state and a
> prohibition no assertion tests is not enforced. Recover the registered line byte-exact with
> `git show prereg-v30:PREREG.md`.*

**OPERATIVE v30a TEXT at line 929:**

> - **`assert_audit_complete()`** — fails on any `unsupported`, `could_not_run`, or **`waived`** **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings. *(`waived` added v30a, carried with SC-12(w), whose (w1) prohibits the state outright; the assertion is what makes that prohibition checkable rather than merely stated.)*

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
> scoring rule and its three dispositions are SC-3(b)'s, and **its map, its indexing, and what the
> artifact publishing it may carry are SC-3(a)'s — all held by citation and none restated here.**
> *(R49/B7: this clause previously restated (a)'s indexing triple in the same breath as declaring it
> unrestated. R47/P5 then amended (a) and left the copy behind, so the copy became DIVERGENT — it
> lacked (a)'s carve-out for artifact rows that are not cells of the map. Two normative copies of one
> rule is §0.2.1 line 77's defect; the second copy silently going stale is why.)* **The cell key is
> the declaration's to supply,
> not this clause's to state**: SC-3(a) requires that a key exist and be declared and named; SC-3(h)
> and SC-8 require it frozen with the map before any detector runs; and this clause names no key.
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

**The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a) [SC-13c(c2)].** That clause states which quantities the exception reaches and what is published for them; it governs the exception wherever this sentence is applied and is not restated here. Everywhere outside it, this sentence governs exactly as registered. The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is recorded in the v30a amendments block and is not changed by the exception.

```

**Why it is drafted this way.** It takes H8's form at §7.7 exactly: it names where the governing
text lives and that it governs at this site, and it adds no rule of its own — the exception's
authority, scope and recording remain SC-13c(c2)'s, which is the one normative copy (SC-9(f),
SC-10(e), §0.2.1 line 77). The excepted-quantity enumeration is NOT repeated here (Q4 defect 2,
folded in: S3(2)). It names the amendments-block recording of the 816/830 relationship because an
implementer at line 816 who then reads line 830 should find that the disagreement is known and
unresolved rather than discover it. **Rule vs instance:** entirely RULE; no fixture, column, count,
or figure appears in it. R24 test: passes — it would read identically in a registration that had
never seen this fixture.

---

### §AB — THE v30a AMENDMENTS-BLOCK RECORDING TEXT (revised; drafted, not applied)

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
> what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
> the state a single canonical disposition and make one of the two lines cite the other. Until that
> amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
> conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3
> and §A.12 item 5). **The operative conflict is registered-text-internal — line 816 against line
> 830.** It is not a conflict between line 816 and the declaration: declaration text on the same
> state is provisional until the tag, is at most corroboration, and cannot settle a disagreement
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
> *absence is a miss* becomes *a finding fails the gate*. **A reader comparing v30 and v30a
> byte-for-byte at line 459 will see no change and conclude wrongly.** The narrowing is made under the
> class C rule, which permits it; §0.2.1 line 97 measures at the outcome, and at the outcome this is a
> supersession.
>
> **These seven are disclosed because the record should not have to be reverse-engineered to find
> them.** Each is verifiable from artifacts this registration commits, except where disclosure 5 says
> otherwise.


## §10.1 LINE 1022 — THE KILL-GATE CRITERION 3 PAIR (source of record, moved here at R53/Y1)

**Why these two are here.** Both were drafted inside deltas — the operative item at R39/F2, the
retention block at K2 §9.2 — and redrafted at R47/P1 to the narrowest C2. Until this move
`_X5_hunks_v2.json` was their only source of record, which left **the amendment's most-revised
normative text as the only applied text no provenance check could reach.** They now sit where every
other piece of applied text sits. The manifest claims them in §A and M6 check (II) binds them, which
asserts the source block is contained in the hunk — the direction that catches a deletion.

**Order of application (R39/F2), unchanged by the move:** the REPLACE lands first; the retention
blockquote is then written directly beneath the resulting operative item 3, before item 4.

**THE RULING, AND ITS REASON (R87/§108).** These two blocks are **CARRIED by the v30a amendment**.
Two records were authored against them — `SC-3-C2op` (line 1022, REPLACE_LINE, from the fenced text
below) and `SC-3-C2ret` (line 1022, INSERT_AFTER) — in the order this section already fixes.

**Why not defer them.** Deferring would have required **three edits in the same tag, every one of
them weakening**: SC-3's supersession block, which states that the kill gate *"must be amended with
this clause or `PREREG.md` holds both readings at once"*, would have had to be softened; this
section's own heading, *"replaces `PREREG.md` line 1022"*, would have had to be withdrawn; and
`BLOCK_MANIFEST.md`'s rows claiming these blocks for hunks at line 1022 would have had to be struck.
**`PREREG.md` line 97 forbids that shape** — *"An amendment weaker than the thing it amends is not
one."* An amendment cannot buy its own consistency by retracting the sentences that make it binding.

**How they were missed for three rounds, recorded so the shape is recognisable.** Neither block has an
`**INSERTION POINT.**` field; each names its target in its own heading. Every check in the apparatus
reasoned forward from the record set, and both directions of §57.3(b) range over **clause** blocks,
which these are not. A block the record set never claimed could not make any of them fire. **D14 now
asks the question from the other end** — every normative block in this file must be reachable by at
least one record — and it fires on this pair when the two records are removed.

### §10.1-C2op — THE C2 OPERATIVE ITEM (replaces `PREREG.md` line 1022)

```
3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
```

### §10.1-C2ret — THE C2 RETENTION BLOCK (inserted beneath the operative item)

```
   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired **as to its corrected-side limb only**, because that limb is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. **The contaminated-side limb and the ambiguity branch are carried into the operative item byte-identical** (R47/P1); the contaminated-side tightening an earlier draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```


---

# PART 2 — S1: R32 APPLIED TO SC-4(a)/(b), CHECKED AGAINST RULE 9's TEXT, AND VERIFIED TO CLEAR

**The working resolution, restated for the record (R32).** The conflict the CI gate surfaced —
SC-4(a)/(b) as applied required the declaration to *state* the class predicates, while the checker's
rule 9 forbids any `**CLASS** iff …` form in a companion document — **resolves against the schema.**
The class predicates are the registration's; the declaration cites them per unit and states the
facts on which each unit satisfies the one it is classed under; no biconditional or other rule-form
predicate is required or permitted in any companion document. **Rule 9 is correct as written and is
not weakened, narrowed, or given an exemption.**

## 2.1 Rule 9, quoted from `tools/check_registration.py` (the working-tree copy, `30d3ad4c…7425`, lines 617–632)

```python
    # --- added with the scope extension -----------------------------------
    # The eight detectors above were written against the restatements that had
    # actually appeared in DESIGN.md, so they are DESIGN.md-shaped: widening the
    # file list alone finds nothing in AVAILABILITY_DECLARATION.md, whose
    # rule-shaped text takes different forms. These five catch those forms. Each
    # is file-agnostic, each names the PREREG section that owns the semantics,
    # and each was calibrated to fire on no other scanned file — the point is to
    # catch rules stated outside PREREG.md, not to editorialise about prose.
    #
    # A classification rule stated as a biconditional: "**REQUIRED** iff …" is
    # a rule for assigning a state, which §0.2.1 reserves ("units, states,
    # denominators, gates"). Deriving THIS fixture's per-column enumeration is
    # an instance; stating the rule that yields it is not.
    (r"\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b",
     "state-classification rule stated as a biconditional; a rule for assigning "
     "a state is owned by PREREG §6.6/§7.0, not by a companion document"),
```

**What the regex matches, read literally.** The pattern is

```
\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b
```

— a bold run whose content is two or more upper-case letters followed by any of upper-case letters,
space, underscore or hyphen, then one or more whitespace characters, then the token `iff` at a word
boundary. It matches `**REQUIRED** iff`, `**OUT OF JURISDICTION** iff`, `**UNSCORED** iff` — the
three declaration lines 1052/1054/1056 — and nothing of the form `**REQUIRED** — predicate: …`,
`satisfies the OUT OF JURISDICTION predicate`, or an unbolded `… OUT OF JURISDICTION iff …`
(declaration line 1071, now 1082: not a finding today; listed among the consequential K4 edits in
Part 2.3). **The rule's comment states its ground precisely — "Deriving THIS fixture's per-column
enumeration is an instance; stating the rule that yields it is not" — and R32 adopts that ground as
the schema's own.** The rewording below was drafted against this regex and this comment, not against
the CI report's paraphrase of them.

## 2.2 SC-4 — BEFORE / AFTER (applied text; the same words are in Part 1 and in the scratch `PREREG.md`)

### (a) — the obligation inverted: the rule is registered, the declaration shows the derivation by citation

**BEFORE** (SSA Part 1, SC-4(a); applied scratch `PREREG.md` line 606 pre-R32):

> **(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY A RULE THE DECLARATION STATES.** The
> declaration states, **ex ante and in full**, the rule by which each unit of the declared scored
> set is assigned its gate class, and the classes are **derived by that rule, never assigned by
> hand.** An evidence artifact's classification of how a unit was *built* answers a different
> question from what the map declares *violating* on the scored side under the declared branch; the
> two do not in general have the same answer. **No classification of the scored set other than this
> derivation enters any criterion, denominator, or count**, and no split within such a
> classification carries gate arithmetic. Any report quoting such a count names the scope it counts
> under.

**AFTER:**

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

**What changed.** (1) The head: the rule is "registered here" (the predicates of (b) under the
precedence of (c)) and "is not the declaration's to state, restate, or rewrite" — replacing "by a
rule the declaration states" / "the declaration states … the rule". (2) The declaration's obligation
is now *per unit*: the class assigned, the registered predicate satisfied **by citation to the row
of (b) that carries it**, and the declared facts on which it is satisfied. (3) A new sentence states
the prohibition in terms — no companion document states a class predicate in rule form,
biconditional or otherwise; cite, do not restate — grounded in §0.2.1 line 77 and SC-9(a)/(f), which
already say this generically. (4) Everything from "An evidence artifact's classification…" to the
end is byte-identical. **Direction:** strictly stronger — the declaration may do less (cite) and
must show more (per-unit facts); "derived … never assigned by hand" is kept.

### (b) — the table header and the after-table sentence

**BEFORE:**

> | Class | Definition (the declaration supplies the predicate) | What a finding on it means |

> **There is no fourth class and no residue class.** **N is the length of the REQUIRED list**, and
> no other quantity is N.

**AFTER:**

> | Class | Registered predicate (cited by the declaration, per unit; never restated) | What a finding on it means |

> **The declaration cites these rows, per unit, and states the facts on which each unit satisfies
> the row it cites; it does not restate them** (a). **There is no fourth class and no residue
> class.** **N is the length of the REQUIRED list**, and no other quantity is N.

**What changed.** The header no longer says the declaration *supplies* the predicate; it says the
predicate is registered and is cited per unit, never restated. The three rows are **byte-identical**
— they were already generic predicates ("the map declares a violation on it, on the scored side,
under the declared branch"; "every constituent read is declared legal at the boundary instant under
the declared branch"; "scoring on it is declared impossible, on a ground the declaration states")
and R32 promotes them from "definition the declaration supplies" to "registered predicate the
declaration cites" without changing a word of them. One sentence added after the table restates the
citation obligation at the table's own site.

### (c) and (d) — consequential, ledgered separately (C-1, C-2); the author may reject either without affecting R32

**(c) BEFORE:**

> **(c) PRECEDENCE, DECLARED.** Where a unit satisfies more than one class predicate, **UNSCORED
> wins.** The declaration states the precedence order it derives under, and a unit's class is the
> first the order yields.

**(c) AFTER:**

> **(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED
> wins.** The declaration derives under this precedence and states none of its own; a unit's class
> is the first the order yields, and for each unit that satisfies more than one predicate the
> declaration records which it satisfies and that precedence decided it.

**Why.** With the predicates registered, "the declaration states the precedence order it derives
under" was a residual instruction to put rule-form text in a companion document. The registered
precedence is "UNSCORED wins" and nothing else; the declaration derives under it and *records* per
multiply-satisfying unit that precedence decided it — data, not rule. **Observation for the author,
not drafted:** REQUIRED ("the map declares a violation on it") and OUT OF JURISDICTION ("every
constituent read is declared legal") are contradictories under SC-3(d)'s side-relative map, so a
unit satisfying both is a declaration defect, not a precedence question; saying so in (c) or (i)
would close the only gap the two-class order leaves.

**(d) BEFORE (head only; the forbidden-readings sentence onward is byte-identical):**

> **(d) THE DECLARATION FIXES THE RULE'S EDGES, AND THE READINGS ARE PART OF THE RULE.** Where a
> class predicate admits two readings, the declaration states which it derives under and why.

**(d) AFTER (head):**

> **(d) THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE
> DERIVATION.** Where a registered class predicate admits two readings, the declaration states which
> it derives under and why, before any detector runs.

**Why.** "THE RULE'S EDGES … PART OF THE RULE" read, after R32, as if the declaration's readings
were part of the *registered* rule. They are part of the *derivation* — readings of a registered
predicate, fixed ex ante ("before any detector runs", SC-8(c)) — and the two forbidden readings
stand as registered. No other word of (d) changes.

### REGISTERS and DATA (apparatus, not applied) — brought into line

REGISTERS: "by a **derivation rule the declaration states ex ante**" → "by **class predicates
registered in this clause, applied to declared facts, the derivation shown per unit by citation**".
DATA: "The derivation rule in full; … the precedence order; …" → "Per unit, the class assigned and
the registered predicate satisfied, cited to (b) by row, with the declared facts on which the unit
satisfies it; … for each unit satisfying more than one predicate, the record that (c)'s precedence
decided it; … **Not** a rule-form statement of any predicate (a)." Full text in Part 1.

**Unchanged and examined:** (e) exclusion grounds (the grounds are registered there already and the
declaration states *which* units fall on each — data); (f) publication discipline ("each unit's
membership is derived by (a) and shown" still reads correctly); (g); (h) ("re-derived by the rule of
(a)" — (a) now says where the rule lives); (i); (j); the SUPERSESSION MARKER ("SC-4(a) replaces it"
still true). SC-5(a) ("derived from the unit's gate class (SC-4)"), SC-8(c), SC-9(a) and H1b's table
row 5 ("Adds the rule constituting the denominator — derived from the declared map, three classes,
each enumerated by name") are consistent with R32 as written and were not touched.

## 2.3 The declaration-side rewording — PROPOSED K4 EDIT, applied to the scratch copy only

**Site.** `AVAILABILITY_DECLARATION.md` §A.6.0, lines **1047–1056** of the 3,684-line working-tree
file (the heading, the two-line lead-in, and the three `iff` bullets; findings 3–5 of the CI report
are lines 1052, 1054, 1056). The ten lines are replaced as one block — the lead-in had to move with
the bullets, because "The rule, stated verbatim so it can be re-applied" introduces exactly the
rule-form statement R32 removes. Block match count in the working-tree declaration: **1** (asserted
by the applier).

**BEFORE** (lines 1047–1056, verbatim):

```
#### A.6.0 — DERIVATION RULE. **The enumeration below is what the rule yields.**

Each column's class is determined by a single rule applied to its construction and its gate
status. The rule, stated verbatim so it can be re-applied when a column changes construction:

- **REQUIRED** iff its construction carries the wall-clock `ts_floor` join **and** it is not
  degenerate-constant.
- **OUT OF JURISDICTION** iff its construction reads only same-row book/clock values,
  availability-legal at the boundary instant under R1's `ties: available`.
- **UNSCORED** iff it is degenerate-constant **or** unconstructible under T4.
```

**AFTER** (21 lines, verbatim as applied to the scratch copy; lines 1047–1067 there):

```
#### A.6.0 — DERIVATION, BY CITATION. **The enumeration below is what the registered rule yields.**

Each column's class is derived by the registered rule — the class predicates `PREREG.md` SC-4(b)
registers, under SC-4(c)'s precedence — applied to the column's declared construction and gate
status. This section states no rule of its own (`PREREG.md` SC-4(a), SC-9(a)): per class it cites
the `PREREG.md` row that carries the predicate, and per column the table below states the class
assigned and the declared ground on which the column satisfies that predicate. Re-derivation when a
column changes construction re-applies the cited rows to the column's new facts (SC-4(h)). Where a
column's ground satisfies more than one row, SC-4(c)'s registered precedence decides — UNSCORED
wins — and the table says so for that column. The citations:

- **REQUIRED** — predicate: `PREREG.md` SC-4(b), row REQUIRED, cited and not restated. Declared
  ground, per column in the table below: its construction carries the wall-clock `ts_floor` join,
  which is the violation §C declares on it on the scored side under R1.
- **OUT OF JURISDICTION** — predicate: `PREREG.md` SC-4(b), row OUT OF JURISDICTION, cited and not
  restated. Declared ground, per column: its construction reads only same-row — read as
  within-lattice, reading note below — book/clock values, each read availability-legal at the
  boundary instant under R1's `ties: available` (§A.6.2).
- **UNSCORED** — predicate: `PREREG.md` SC-4(b), row UNSCORED, cited and not restated, on a ground
  `PREREG.md` SC-4(e) registers. Declared ground, per column: degenerate-constant, or
  unconstructible under T4 (gate status EXCLUDED on the gate-scored fixture; §A.6.3).
```

**How it meets R32.** Per class it cites the `PREREG.md` row that carries the predicate ("SC-4(b),
row REQUIRED, cited and not restated"); per column the existing table (declaration lines 1101–1137,
now 1112–1148) already states the class assigned and the ground — its "Clause satisfied" column is
that ground. The bullets state **declared facts** (this fixture's `ts_floor` join;
same-row/within-lattice book/clock reads legal under R1; degenerate-constant or T4-EXCLUDED), never
the predicate, and never in `iff` form. Precedence is cited to SC-4(c) ("UNSCORED wins") rather than
re-stated as a conjunct of the REQUIRED rule — which also retires the parenthetical at lines
1067–1074 (now 1078–1085) that reasoned about "the REQUIRED clause is a CONJUNCTION". **Checked
against rule 9's regex, not its description:** `**REQUIRED** — predicate:` has `—`, not `iff`, after
the bold run; no other curated detector fires (no "enters/excluded from … denominator", no
"denominator derives", no "never reported as", no "**DEFINITION"). The run in 2.4 confirms: −3, +0.

**Consequential K4 edits this proposal implies but does not draft** (same section, instance prose):
the table header at line 1101 (now 1112) "| # | Column | Rule-derived class | Clause satisfied |
Frozen at |" → "… | Class (derived) | Registered row cited · declared ground | …"; line 1071 (now
1082) "it fully satisfies the OUT OF JURISDICTION iff (a pure function of" → "… the OUT OF
JURISDICTION predicate (…"; the reading-note lead-in at 1058 (now 1069) "Three reading notes fix the
rule's edges" → "… fix the reading at each edge (`PREREG.md` SC-4(d))"; line 1139 (now 1150) "**What
the rule yields.**" → "**What the cited rows yield.**"; the `buy_volume_10s` parenthetical
(1067–1074, now 1078–1085) simplified to precedence-by-citation. None of these is a finding today;
all are K4's to carry with the scrub of the other 11 findings (CI report §2 classification table,
items 1–2 and 6–14).

## 2.4 The scratch re-run — commands, stdout, exit codes, counts, delta

All runs: cwd = `applied\`, Python 3.12.10, `CI_GATE_RESULT.md` held aside as
`_CI_GATE_RESULT.md.hold`. Exact checker command at every step: `python tools/check_registration.py
--stage prereg` (stdout captured to the named file; exit code from the shell). Pytest: `python -m
pytest tests/registration -q -p no:cacheprovider`.

| Step | State of `applied\` | Checker result | Exit | Findings | Output file |
|---|---|---|---|---|---|
| 0 | K9/J9 applied `PREREG.md` (`a0c899a4…2ef5`, 1,408 lines) + working-tree declaration (`f0829bd3…3310`, 3,684 lines) | 12 PASS / `single_source` FAIL | 1 | **14** — byte-identical to `_applied_checker.txt` (the CI report's §2) apart from the root line | `_S1_step0_baseline_checker.txt` |
| A | + `--step prereg`: R32 on SC-4 (5 edits) and S3 (3 edits) on `PREREG.md` → `c9c8c2d6…b7e`, 1,408 lines | identical | 1 | **14** — identical to step 0 (PREREG.md is not scanned by `single_source`; every PREREG-reading check still PASS) | `_S1_stepA_prereg_checker.txt` |
| **B** | + `--step decl`: the Part 2.3 block on the declaration → `1290186e…1c30`, 3,695 lines | 12 PASS / `single_source` FAIL | 1 | **11** | `_S1_stepB_decl_checker.txt` |
| C | + `--step s2`: the three S2 insertions + SC-8 M2 revised + two markers on `PREREG.md` → `e7ab52d3…1706`, 1,417 lines | identical to B | 1 | **11** — only the two `EXEMPTION APPLIED` note line numbers move (493→495, 1406→1415) | `_S1_stepC_s2_checker.txt` |

**Step B — the S1(d) result — full stdout, verbatim (exit code 1):**

```
== check_registration --stage prereg (root: C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\applied) ==
[PASS] structure
[PASS] config_schema
[PASS] lock_table
[PASS] banned_vocabulary
    note: PREREG.md:493: EXEMPTION APPLIED id=REG15 reason='the registry entry must name the parked mechanism to state what a user does not get'
    note: PREREG.md:1406: EXEMPTION APPLIED id=PARK9 reason='the parking-lot pointer must name the parked mechanism to state what an amendment would restore'
[PASS] deletion_certificate
[FAIL] single_source
    AVAILABILITY_DECLARATION.md:974: rule about what may be reported/published stated outside PREREG.md; what a published number means is owned by PREREG §7.2/§8.3/§10.2: 'and a slice may not be reported as a pass on the strength of containing only unscored cells.'
    AVAILABILITY_DECLARATION.md:1035: denominator constitution defined outside PREREG.md; owned by PREREG §7.2/§7.4: 'by column. **The denominator derives from the DECLARED MAP (`n1\\declared_map.csv`), not from'
    AVAILABILITY_DECLARATION.md:1239: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'Requires no finding and forbids none; enters no denominator, contributes to no rate, and'
    AVAILABILITY_DECLARATION.md:1557: a defining clause for a term used normatively by PREREG.md is opened here; what a term means is owned by PREREG.md (§0.2.1): '**DEFINITION, declared.**'
    AVAILABILITY_DECLARATION.md:1562: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: "> **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but"
    AVAILABILITY_DECLARATION.md:1591: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'path, entering no denominator, contributing to no rate, and **never reported as a pass**'
    AVAILABILITY_DECLARATION.md:1591: rule about what may be reported/published stated outside PREREG.md; what a published number means is owned by PREREG §7.2/§8.3/§10.2: 'path, entering no denominator, contributing to no rate, and **never reported as a pass**'
    AVAILABILITY_DECLARATION.md:2224: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'enters no denominator, contributes to no rate, and **cannot be reported as a pass**. A gate'
    AVAILABILITY_DECLARATION.md:2723: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'either side. Its gate status is **EXCLUDED**, and it enters no denominator.'
    AVAILABILITY_DECLARATION.md:2765: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: '**None of the four categories enters the criterion-1 denominator except Category 4**, which is'
    AVAILABILITY_DECLARATION.md:3688: denominator constitution defined outside PREREG.md; owned by PREREG §7.2/§7.4: "- **R11.** Criterion-1 denominator derives from the DECLARED MAP, not from the manifest's construction classes"
[PASS] phase_arithmetic
[PASS] requirement_ids
[PASS] legality_table
[PASS] parking_lot
[PASS] reducer_functions
[PASS] unit_grammar
[PASS] suppression_anchor

Deferred at this stage (owned elsewhere; an omitted branch is a failure, not a pass):
    ties_comparator_vs_shipped_mask  -> owned by --stage implementation
    l31b_inequalities_vs_shipped_rule  -> owned by --stage implementation
    shipping_defaults_vs_validated_runtime  -> owned by --stage implementation
    deleted_config_fields_rejected  -> owned by --stage implementation
    cost_script_total  -> owned by --stage implementation
    readme_numbers_regenerated  -> owned by --stage release
    package_defaults  -> owned by --stage release
    installability  -> owned by --stage release

RESULT: FAIL — 1 check(s) failed, 11 finding(s)
```

**Delta against step A / step 0 (14 → 11), classified line by line.** Removed: exactly the three
rule-9 findings — `AVAILABILITY_DECLARATION.md:1052` (`**REQUIRED** iff …`), `:1054` (`**OUT OF
JURISDICTION** iff …`), `:1056` (`**UNSCORED** iff …`). Retained, same detector and same quoted
text: 974 and 1035 (above the edited block, line numbers unchanged) and 1228→1239, 1546→1557,
1551→1562, 1580→1591 (×2), 2213→2224, 2712→2723, 2754→2765, 3677→3688 (below the block, each shifted
by exactly +11 = 21 new lines − 10 old). Added: **none**. **Delta = −3 exactly; the actual count is
the predicted 11.** The eleven that remain are the CI report's findings 1, 2 and 6–14 — all K4 scrub
targets on the unscrubbed declaration, none touching SC-4 or rule 9.

**Step C** (S2 applied) — stdout identical to step B except the two exemption-note line numbers (the
REG15 and PARK9 markers move down with the insertions above them and still bind to the line beneath,
as the notes prove); 11 findings, exit 1. Every PREREG-reading check — `structure`, `lock_table`,
`banned_vocabulary` (no banned term in the new text: `capability matrix`, `noise floor`, `routing
policy`, `comparison_mode`, `statistical mode`, `substituted gate` all absent),
`deletion_certificate`, `phase_arithmetic`, `requirement_ids`, `legality_table`, `parking_lot`,
`reducer_functions` (§11 still lists the seven names; item 8 does not disturb `sections_of("11")`),
`unit_grammar`, `suppression_anchor` (line 816's sentence and line 818's definition still in §7.2.1;
the reduced §13c-P still sits between them; registered anchor line 816 still matches exactly once as
a full line) — **PASS**.

**pytest** — `python -m pytest tests/registration -q -p no:cacheprovider`:

| State | Summary line | Exit | Failing test |
|---|---|---|---|
| step B (R32 + S3 + declaration block) | `1 failed, 136 passed in 0.95s` | 1 | `tests/registration/test_checker.py::test_prereg_stage_on_real_repo_exits_zero` — the checker's exit-code wrapper; its captured output is the 11-finding result above |
| step C (final, + S2) | `1 failed, 136 passed in 1.15s` | 1 | the same one test |

**136 passed / 1 failed at both states — the historical 136/1 figure, same test, same cause** (the
K4 scrub has not landed; 11 findings remain). The applied text of this pass introduces zero new
findings and breaks zero tests.

**File identities after this pass** (`sha256sum`, LF-only, no BOM):

| File | sha256 | Lines |
|---|---|---|
| `applied PREREG.md (final, step C)` | `e7ab52d35f603d1e8f91985176bf235b3b1089be8c4858fdbee70e7b7d991706` | 1417 |
| `applied AVAILABILITY_DECLARATION.md (step B/C)` | `1290186ed970df65968b5b979aa696e4dca4678e7b46fae40587c4948b8b1c30` | 3695 |
| `_PREREG_preR32.md.bak (K9/J9 applied input)` | `a0c899a48a8ffe5363611bd9c5f4e2d82529a1dc8b6413721d58b3da96032ef5` | 1408 |
| `_DECL_preR32.md.bak (working-tree declaration)` | `f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310` | 3684 |
| `_PREREG_R32_S3_only.md.bak (step A/B PREREG)` | `c9c8c2d69999e38e64c1807e5413ff4d36b92c0db3175ecaf2565ac9cd987b7e` | 1408 |
| `_PREREG_FINAL_stepC.md.bak (= final)` | `e7ab52d35f603d1e8f91985176bf235b3b1089be8c4858fdbee70e7b7d991706` | 1417 |
| `_PREREG_pristine.md.bak (v30)` | `f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6` | 1099 |
| `tools/check_registration.py (working tree)` | `30d3ad4cfd72e1cb611bdbc4f3fb72cc66b00a9c1292aa76c1d564b4ceed7425` | 1062 |

`_apply_R32_S2_S3.py --step restore` returns both scratch files to the pre-R32 state from the two
`_*_preR32.md.bak` snapshots; the applier refuses to run outside `scratchpad\applied`.

---

# PART 3 — S2: THE THREE UNDRAFTED INSERTION POINTS, DRAFTED

Standard: generic per R24 (would read identically in a registration that never saw this fixture); a
supersession marker where the text amends; cited not restated per SC-9(f) — H8's form
(`PREREG_v30a_DIFF.md` line 393: name where the governing text lives, say that it governs here, add
no rule) is the model, and the reduction of §13c-P to that form (Part 4) is applied to these three
from the start. Each anchor was re-counted this pass as a **full-line match against the pristine
1,099-line `PREREG.md`** (`_PREREG_pristine.md.bak`, `f0a8f001…c7cc6`) and again at apply time
against the current scratch text; every count is 1.

## 3(i) — §8.2, after `PREREG.md` line 915: `unscored` added to the second coverage-state list (SC-6)

**ANCHOR — line 915, verbatim (pristine match count 1; at apply, the insertion follows SC-6's marker M2, which sits directly beneath it):**

```
Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. None may be displayed in a way mistakable for a pass.
```

**What line 915 is.** §8.2's not-run enumeration — `not_applicable`, `unsupported`,
`could_not_run(reason)` with its five reasons — its boundary sentence ("missing or impossible inputs
are unsupported; supplied-and-valid inputs that then fail are could-not-run"), the covering-detector
sentence, and the closing sentence "None may be displayed in a way mistakable for a pass." SC-6's
semantics on line 855 (now the §7.7 row plus SC-6(a)–(e)): `unscored` is **neither a pass nor a
not-run**, entered only by the declaration's ledger before any detector runs, enters no denominator,
contributes to no rate, cannot be reported as a pass, and SC-6(e) already says "§8.2's rule governs
their display: none may be displayed in a way mistakable for a pass." The drift risk is concrete:
§7.7's row now carries `unscored`; §8.2's list does not, and §8.2 is the section that governs
display of every non-pass state.

**INSERT AFTER (one paragraph, blank line each side; after marker M2 where placed):**

```

**`unscored` — §7.7 (v30a) [SC-6] — is governed by this section's closing sentence as well.** It is neither a pass nor a not-run: this section's boundary sentence does not reach it, and its entry condition and semantics are SC-6's, not restated here. It is named here so that this section and §7.7's row cannot name different states — the closing sentence above ranges, by reference to §7.7's row and not to the enumeration in this section alone, over every detector-case coverage state that row carries other than `passed` and `failed`.

```

**Justification (one line).** Serves SC-6(e) ("§8.2's rule governs their display") and SC-6's marker
M2 ("`unscored` joins it, and §8.2's closing sentence governs it unchanged"): it names `unscored` in
§8.2 by citation to §7.7's row and SC-6, says in one clause why a non-not-run sits in a section
headed "Not-run states", keeps the boundary sentence off it, and restates nothing of SC-6(a)/(b).

**How the two lists cannot drift — the H-L13 principle applied.** The closing sentence's scope is
made **open-form, by reference to §7.7's row**: it ranges over every detector-case coverage state
that row carries other than `passed` and `failed`, "and not [over] the enumeration in this section
alone". A state added to §7.7's row by a future amendment is therefore governed by §8.2's display
rule the moment it is added, with no second edit to re-bump — exactly the open-range fix
`HISTORY.md` H-L13 records ("enumerated ranges in cross-references are fragile by construction,
because the obligation to re-bump lives outside the edit that grows the target"). **Disclosed
consequence:** the open-form scope also reaches §7.7's `waived`, which §8.2 does not name today. The
effect is that a `waived` entry may not be displayed in a way mistakable for a pass — strictly
stronger, consistent with SC-12 (a waived detector's result cannot change an outcome) and with H8
(no case may be reported `waived` at all until an entry condition is registered), and vacuous in
practice under H8; disclosed so it is a decision, not a discovery. If the author prefers §8.2 to
name `unscored` only, strike the final clause from "the closing sentence above ranges" onward; the
drift protection is then lost.

## 3(ii) — §11, after `PREREG.md` line 1054: item 8, the hash-count rule (R23), with markers for item 3 and §0.2.1 line 97

**ANCHOR — line 1054 (item 7), verbatim (pristine match count 1):**

```
7. Evaluation generator snapshot, conformance suite, adjudication rubrics, parameter distributions, beacon records, and generated manifests frozen in their own files with their own hashes.
```

**AMENDED SITE 1 — line 1050 (item 3), verbatim (pristine match count 1); text stands byte-exact, marker placed beneath the list:**

```
3. **SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed** in the tag message and the README.
```

**AMENDED SITE 2 — line 97 (§0.2.1), verbatim (pristine match count 1); text stands byte-exact, marker placed after it:**

```
**An amendment inherits §11's integrity chain in full:** signed tag, both file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock. An amendment weaker than the thing it amends is not one.
```

**What the two lines say, and why both are amended.** Item 3 names **three** files (`PREREG.md`,
`DESIGN.md`, `HISTORY.md`); line 97 says **"both file hashes"** (the count when two files were
hashed); the executed `prereg-v30` tag message (read this pass: `tagmsg.txt`; `git tag -n20
prereg-v30`) enumerates **five** (the three plus `tools/check_registration.py` and
`protocol/runtime_reference.py`); the declaration's §D.2 plans **six** for v30a (J1 row 126). Four
counts in play is the H-L13 shape — a literal that must be re-bumped by an edit outside the one that
grows the set — and SC-8(f) already says the count is "derived from the set of registered files,
never stated as a literal". Item 8 is where that rule lives in §11, and it is also SC-8's second
insertion point ("so registration integrity indexes the freeze"): one item does both, by citation.

**INSERT AFTER LINE 1054 — item 8 (one line, as the list's eighth item):**

```
8. **The freeze, and the hash set that carries it — v30a.** What freezes at an amended registration's tag, in what form, and what may not happen to it afterwards is stated in §6.2 (v30a) [SC-8] and is not restated here. The tag message of this registration and of every amendment to it carries the SHA-256, as committed, of **every registered document and every registration tool** — the registration and its checking tools as item 1 names them, every document an amendment registers under §0.2.1 (the availability declaration included), and every file SC-8(f) requires hashed — **one hash beside one path, enumerated in the tag message itself.** The set is that enumeration and its count is read from it: no clause of this file states the count as a literal, and where an earlier clause names the hashed files or their number — item 3's three names, §0.2.1 line 97's "both" — it records the set at the time of its writing, stands as that record, and is superseded as the set by this item; the requirement it states stands. A registered file absent from the enumeration is a defect in the tag, not a file outside the chain.
```

**THEN, BENEATH THE LIST (blank line, then the two markers; SC-8's M2 marker — already placed there by the CI run — is revised to the second text):**

```
> **§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT.** The registered v30 item names three files; the `prereg-v30` tag as executed enumerated five. The requirement — SHA-256 as committed, in the tag message and the README — stands byte-exact; the file set and its count are item 8's, derived from the tag message's own enumeration, and the three names are retained as the v30 record and are NOT the set.

> **§11 items 1–7 — v30a, EXTENDED.** Item 8 is added: it indexes the freeze (SC-8) and amends item 3's hash set; SC-8(f) states the requirement generically and does not fix a count.
```

**AND AFTER LINE 97 (blank line each side):**

```

> **§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT.** "both file hashes in the tag message" records the count at the time of writing; it is superseded as a count by §11 item 8, which derives the count from the tag message's own enumeration. The requirement — that an amendment inherit §11's integrity chain in full — stands byte-exact.

```

**Justification (one line).** Serves SC-8(f) ("hashed in the amended registration's tag message as
committed, and the count of hashes is derived from the set of registered files, never stated as a
literal") and §0.2.1 line 97's own requirement ("an amendment weaker than the thing it amends is not
one"): the set is the tag message's own enumeration, the count is read from it, the two stale
literals are superseded *as counts* while their requirements stand, and SC-8's freeze is indexed
from §11 by citation.

**The H-L13 lesson, recorded as the principle.** `HISTORY.md` H-L13 (12 Aug 2026): "Three instances
is a structural defect, not bad luck: enumerated ranges in cross-references are fragile by
construction, because the obligation to re-bump lives outside the edit that grows the target." The
fix there named the series in open form. Item 8 is the same fix for the hash count: **the
enumeration lives in the artifact that carries the hashes, and the count is a property read off it,
so growing the set and stating its size are one edit, not two.** A registered file absent from the
enumeration is a defect in the tag — fail-closed, the same standard the checker's scope-by-exclusion
sets for scan scope.

**Disclosed decisions for the author.** (1) *Genus of "registered document and registration tool".*
Item 8 defines it by reference — item 1's registration and checking tools, every document an
amendment registers (the declaration included), every file SC-8(f) requires — and item 1 names
`tests/registration/` (a directory) among the checking tools, which the executed v30 tag did not
hash; whether the suite is hashed file by file under item 8, or item 8 is narrowed to name the tools
it means, is the author's call and is not made here (narrowing must be done in item 8's text, not by
leaving the genus to be read). (2) *Drafting identifier resolved.* SC-8's M2 marker read "Item 3's
hash set is amended by R23 independently of this clause" — "R23" is a workflow id that resolves to
nothing inside `PREREG.md` (SSA Part 6 item 4; CI report §1.5). It now reads "Item 8 is added: it
indexes the freeze (SC-8) and amends item 3's hash set". (3) Item 3's README clause ("and the
README") is left standing — the marker says the *requirement* stands; whether the README must mirror
the full enumeration or may point to the tag is for the author.

## 3(iii) — §8.6, after `PREREG.md` line 961: the reporting-side pointer to SC-11 (zeros, absences and pass claims)

**ANCHOR — line 961, verbatim (pristine match count 1):**

```
Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval, the availability declaration in force, and — for runtime rows — the probed-cohort count and row coverage. Non-holdout author-produced numbers say so in the same line.
```

**What §8.6 says and what SC-11 needs there.** §8.6 ("Every published number states its provenance")
is one sentence about rates that *exist*: a rate names its config section, corpus, mode, evidence
basis, *n*, interval, declaration, and for runtime rows its probed-cohort count and row coverage;
author-produced numbers say so. SC-11's marker says exactly what is missing: "§8.6 governs
provenance of numbers that exist and is silent on numbers that come back empty." Under criterion 3 a
zero-violation aggregate **is** a pass claim (SC-11 REGISTERS), and SC-11(c) and (f) require that a
published zero name the check it survived and the population it is zero over — i.e. a zero's
*provenance* includes its *proof*. §8.6 needs to say that a zero is a published number under this
section and that what its provenance must additionally contain lives in SC-11 — and no more, or the
pointer becomes a second copy of (c) and (f).

**INSERT AFTER (one paragraph, blank line each side):**

```

**A zero, an empty result, or an all-clean statement is a published number and carries provenance under this section.** The control it must survive before it may be reported, and what it must name when it is, are stated in §7.8 (v30a) [SC-11] and govern here; they are not restated.

```

**Justification (one line).** Serves SC-11(c)/(f) (a reportable zero is reported "with the check
named" and "names the population it is zero over") and SC-11's INSERTION POINT ("a one-line pointer
after line 961 so the reporting section indexes it"): it brings zeros, empties and all-cleans under
§8.6's provenance rule by name and points to SC-11 for the control and the naming obligations,
restating neither — H8's form.

**Rule vs instance, all three:** entirely RULE. No fixture, column, count, file name or figure
appears in any of the three texts; each would read identically in a registration that had never seen
this fixture. Checked token by token against the Q3 list (SSA Part 4 method) — no hit.

---

# PART 4 — S3: Q4's THREE LESSER DEFECTS, FOLDED IN

Source: `tasks\wndeu4eu9.output`, `result.q4`, blockers[0] — "Pre-adoption edits recommended (none
is a stop)" — and the findings for ITEM 3 (the §AB miss), ITEM 6 (NEW DEFECT 1, §13c-P; NEW DEFECT
2, (c5)(i)) and ITEM 1 (the 'only' nit). Each is quoted before/after; each was applied to the
scratch `PREREG.md` in step A (CI-neutral, Part 2.4).

## 4(1) — §AB: the dangling "superseded ledger entry 3.4" reference struck

**Q4's finding (ITEM 3, verbatim in part):** "§AB, drafted for PREREG.md's v30a amendments block …
still reads … 'and this recording supersedes the framing of the superseded ledger entry 3.4, which
located the collision between line 816 and §A.12 limb (i)'. 'Ledger entry 3.4' is
M1_CANDIDATE_C_CLAUSE_CORRECTED.md's Part 3.4 … a scratchpad drafting file; nothing in applied
PREREG.md is labelled ledger 3.4. The editor fixed the identical genus at SC-6(b) (Q2(a)-3 …) but …
misses this."

**BEFORE** (SSA §AB, closing paragraph; applied scratch `PREREG.md` line 53 pre-S3):

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

**AFTER:**

> **What this amendment does NOT do: resolve the conflict.** Everywhere outside SC-13a–c, lines 816
> and 830 both stand as registered and continue to point in opposite directions over the
> `not_applicable`-everywhere state. **Flagged for a future class C amendment** — the defect changes
> what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
> the state a single canonical disposition and make one of the two lines cite the other. Until that
> amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
> conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3
> and §A.12 item 5). **The operative conflict is registered-text-internal — line 816 against line
> 830.** It is not a conflict between line 816 and the declaration: declaration text on the same
> state is provisional until the tag, is at most corroboration, and cannot settle a disagreement
> between two registered lines.

**What changed.** The clause from ", and this recording supersedes the framing of the superseded
ledger entry 3.4 …" to the end is replaced by two sentences that keep its substance — the operative
conflict is registered-text-internal, line 816 against line 830, and declaration text cannot settle
it — in the amendment block's own terms, with no reference to any drafting file or ledger number.
The fate of the superseded drafting entries 3.3/3.4 stays where SSA Part 6 item 7(v) left it: an
author decision, apparatus.

## 4(2) — §13c-P: reduced to H8's form (point, do not restate)

**Q4's finding (ITEM 6, NEW DEFECT 1, verbatim in part):** "§13c-P … restates the exception's scope
and effect … a paraphrase of (c2)'s enumeration … The H8 precedent it claims to mirror … does NOT
restate the definition it points to … So the file's self-description ('It mirrors H8's form … adds
no rule of its own') overstates, and the exception's scope now has two normative copies (SC-9(f) …;
SC-10(e) …; §0.2.1 line 77)." H8's text, for the form (`PREREG_v30a_DIFF.md` line 393): "**`waived`
is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this
table. …"

**BEFORE** (SSA §13c-P INSERT block; applied scratch `PREREG.md` line 1031 pre-S3):

> **The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a)
> [SC-13c(c2)].** For the quantities §10.2's ambiguity-branch replacement criterion requires — the
> per-detector, per-side `preserving` proof yields it gates, that gate itself, and the published
> yield it requires of the other combination — the suppression clause does not apply: the
> publication clause applies in full, and the computed yield and the gate outcome are published with
> the counts and the named reason. Everywhere else this sentence governs exactly as registered. The
> registered relationship between this sentence and §7.4's scope-eligibility definition (line 830)
> over the same state is recorded in the v30a amendments block and is not changed by the exception.

**AFTER:**

> **The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a)
> [SC-13c(c2)].** That clause states which quantities the exception reaches and what is published
> for them; it governs the exception wherever this sentence is applied and is not restated here.
> Everywhere outside it, this sentence governs exactly as registered. The registered relationship
> between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is
> recorded in the v30a amendments block and is not changed by the exception.

**What changed.** The excepted-quantity enumeration ("the per-detector, per-side `preserving` proof
yields it gates, that gate itself, and the published yield it requires of the other combination")
and the effect clause ("the suppression clause does not apply: the publication clause applies in
full, and the computed yield and the gate outcome are published with the counts and the named
reason") are deleted; in their place: "That clause states which quantities the exception reaches and
what is published for them; it governs the exception wherever this sentence is applied and is not
restated here." The pointer's first sentence, the "everywhere outside it" sentence and the
816/830-recording sentence stand. SC-13c(c2) is now the one normative copy of the exception's scope.
The apparatus paragraph "Why it is drafted this way" is revised to match (Part 1).
`suppression_anchor` still PASSes (the pointer sits between the two anchored sentences and disturbs
neither).

## 4(3) — SC-13c(c5)(i): "only" dropped; the freeze attributed to SC-3(h)/SC-8, not SC-3(a)

**Q4's finding (ITEM 1 nit / ITEM 6 NEW DEFECT 2, verbatim in part):** "'only' understates SC-3(a)
(which also requires a published artifact with a declared schema, one row per scored cell) and the
freeze is SC-3(h)/SC-8's requirement, not SC-3(a)'s. Recommend dropping 'only' ('SC-3(a) requires
that a key exist, be declared and named; SC-3(h) and SC-8 require it frozen with the map …')."

**BEFORE** (the sentence, inside SC-13c(c5)(i); applied scratch `PREREG.md` line 1337 pre-S3):

> SC-3(a) requires only that a key exist, be declared and named, and be frozen with the map before
> any detector runs (SC-3(h), SC-8), and this clause names no key.

**AFTER:**

> SC-3(a) requires that a key exist and be declared and named; SC-3(h) and SC-8 require it frozen
> with the map before any detector runs; and this clause names no key.

**What changed.** Exactly Q4's recommendation. SC-3(a) is no longer summarised with "only"; the
freeze is attributed to the clauses that impose it. No other word of (c5)(i) changes; the Q1(i)
genericisation stands.

**Q4's nits, recorded and not acted on** (Q4: "no action required for adoption"): (a) SC-13c(c1)'s
"(line 1033; SC-12 item (5))" — a waiver-scoped citation for an amendment-substitution point whose
direct source is SC-9(c); one hop away, left as is; (b) §0.1's cross-citation list omitted SC-6(c)'s
"(SC-3)"/"(SC-4)" — **fixed in this file's §0.1** (apparatus); (c) SC-13b's marker says lines "816,
830, 570 … are cited" while the clause cites §6.6 by section — apparatus, pre-existing, left as is.

---

# PART 5 — CHANGE LEDGER: EVERY DIFFERENCE BETWEEN THIS FILE'S PART 1 AND SSA's PART 1

Part 1 was carried from SSA lines 76–1375 programmatically; the only differences are the rows below
("A" = applied text; "M" = supersession-marker text at the superseded site; "X" = apparatus).
Anything not listed is byte-identical to SSA. SSA's own ledger E-1 … E-21 against K1 / the split
file stands beneath this one.

| # | Clause · element | Loc | Before (SSA) | After (this file) | Reason |
|---|---|---|---|---|---|
| F-1 | SC-4 REGISTERS | X | "by a **derivation rule the declaration states ex ante**" | "by **class predicates registered in this clause, applied to declared facts, the derivation shown per unit by citation**" | R32 (S1) |
| F-2 | **SC-4(a)** | A | "BY A RULE THE DECLARATION STATES … The declaration states, ex ante and in full, the rule …" (Part 2.2 BEFORE) | "BY THE RULE REGISTERED HERE, AND THE DECLARATION SHOWS THE DERIVATION … registered in this clause … not the declaration's to state, restate, or rewrite … per unit … by citation to the row of (b) … No companion document states a class predicate in rule form … cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f))" (Part 2.2 AFTER) | **R32 (S1)** |
| F-3 | **SC-4(b)** table header | A | "Definition (the declaration supplies the predicate)" | "Registered predicate (cited by the declaration, per unit; never restated)" | **R32 (S1)** — rows byte-identical |
| F-4 | SC-4(b) after-table sentence | A | "**There is no fourth class …**" | prefixed: "**The declaration cites these rows, per unit, and states the facts on which each unit satisfies the row it cites; it does not restate them** (a)." | R32 (S1) |
| F-5 | SC-4(c) | A | "PRECEDENCE, DECLARED … The declaration states the precedence order it derives under, and a unit's class is the first the order yields." | "PRECEDENCE, REGISTERED … The declaration derives under this precedence and states none of its own; a unit's class is the first the order yields, and for each unit that satisfies more than one predicate the declaration records which it satisfies and that precedence decided it." | consequential to R32 (C-1); author may reject |
| F-6 | SC-4(d) head | A | "THE DECLARATION FIXES THE RULE'S EDGES, AND THE READINGS ARE PART OF THE RULE. Where a class predicate admits two readings, the declaration states which it derives under and why." | "THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE DERIVATION. Where a registered class predicate admits two readings, the declaration states which it derives under and why, before any detector runs." — rest byte-identical | consequential to R32 (C-2); author may reject |
| F-7 | SC-4 DATA | X | "The derivation rule in full; … the precedence order; …" | "Per unit, the class assigned and the registered predicate satisfied, cited to (b) by row, with the declared facts …; … the record that (c)'s precedence decided it; … **Not** a rule-form statement of any predicate (a)." | R32 (S1) |
| F-8 | SC-6 INSERTION POINT 2; new **INSERTION TEXT** block (§8.2) | X + **A** | insertion point only; "no §8.2 sentence is drafted" (SSA Part 6 item 3) | operative sentence drafted (Part 3(i)), placed after marker M2 | **S2(i)** |
| F-9 | SC-8 INSERTION POINT 2; MARKER M2 revised; two new markers (item 3; line 97); new **INSERTION TEXT** block (§11 item 8) | X + **M** + **A** | "A pointer item added to §11 after line 1054 …" undrafted; M2 "Item 3's hash set is amended by R23 independently of this clause" | item 8 drafted (Part 3(ii)); M2 → "Item 8 is added: it indexes the freeze (SC-8) and amends item 3's hash set"; markers "§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT" and "§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT" | **S2(ii)**; resolves the R23 drafting identifier (SSA Part 6 item 4) |
| F-10 | SC-11 INSERTION POINT; new **INSERTION TEXT** block (§8.6) | X + **A** | "plus a one-line pointer after line 961 (§8.6)" undrafted | pointer drafted (Part 3(iii)) | **S2(iii)** |
| F-11 | **SC-13c(c5)(i)** | A | "SC-3(a) requires only that a key exist, be declared and named, and be frozen with the map before any detector runs (SC-3(h), SC-8), and this clause names no key." | "SC-3(a) requires that a key exist and be declared and named; SC-3(h) and SC-8 require it frozen with the map before any detector runs; and this clause names no key." | **S3(3)** — Q4 ITEM 1 / ITEM 6 NEW DEFECT 2 |
| F-12 | **§13c-P** INSERT text; "Why it is drafted this way" | **A** + X | the excepted-quantity enumeration and effect restated (Part 4(2) BEFORE); "It mirrors H8's form … adds no rule of its own" | H8 form: "That clause states which quantities the exception reaches and what is published for them; it governs the exception wherever this sentence is applied and is not restated here."; apparatus revised to say so | **S3(2)** — Q4 ITEM 6 NEW DEFECT 1 |
| F-13 | **§AB** intro note; closing paragraph | X + **A (record)** | "Three changes …"; "…, and this recording supersedes the framing of the superseded ledger entry 3.4, which located the collision between line 816 and §A.12 limb (i): the operative conflict is registered-text-internal — 816 against 830 — and provisional declaration text cannot settle it." | "Four changes …"; "…. **The operative conflict is registered-text-internal — line 816 against line 830.** It is not a conflict between line 816 and the declaration: declaration text on the same state is provisional until the tag, is at most corroboration, and cannot settle a disagreement between two registered lines." | **S3(1)** — Q4 ITEM 3 |
| F-14 | Part 1 title and convention note | X | "AS CORRECTED, VERBATIM"; K1's convention | "AS CORRECTED THROUGH R32 / S2 / S3, VERBATIM, READY TO APPLY"; INSERTION TEXT blocks named as applied text; provenance and verification stated | this file |
| F-15 | §0.1 cross-citation list (this file's §0, not Part 1) | X | omitted SC-6(c)'s "(SC-3)"/"(SC-4)" | added; S2/R32 citations added | Q4 nit |
| F-16 | **SC-4(k)** | **A** | *(absent — SSA's SC-4 runs (a)–(j))* | the whole of **(k)**: (k1) the floor, (k2) the reconciliation and (k2)(i) its provenance bar, (k3) the disclosure carve-out and the verifiability limit, (k4) the failure conditions | **R49/R5, restructured R49 addendum S1–S3, extended R60/F3-B5.** *Listed at R60/F3: (k)'s applied lines were an unlisted difference under this table's own completeness claim.* |

**Not changed, and examined:** every clause other than SC-4, SC-6 (apparatus + new block), SC-8
(marker + new block), SC-11 (apparatus + new block), SC-13c(c5)(i), §13c-P and §AB is byte-identical
to SSA Part 1 — SC-1, SC-2, SC-3, SC-5, SC-7, SC-9, SC-10, SC-12, SC-13a, SC-13b, and SC-13c outside
(c5)(i). The two *Instance record* notes stand. **The K1 accounting (§2 76 rows, §3 26 rows, §4 36
rows) is unchanged; the ROWS COVERED lines are untouched.** SSA's Part 4 R24 scan stands for every
unedited limb; the edited/added texts were re-scanned token by token this pass (Part 3 closing note;
SC-4's new (a)/(c)/(d) name no fixture particular — "the row of (b)", "declared facts",
"construction and legality facts" are kinds).

---

# PART 6 — CARRIED OPEN, REPORTED NOT SOLVED (SSA Part 6, updated)

1. **Closed by this pass:** SSA Part 6 item 3's three undrafted insertions (§8.2 sentence, §11 pointer item, §8.6 pointer) — drafted (Part 3) and applied to the scratch copy; SSA Part 6 item 4's "R23" identifier in SC-8's M2 marker — resolved to "item 8"; Q4's three lesser defects (Part 4); the SC-4 / rule-9 conflict (CI report §2 findings 3–5, §7 observation 4) — resolved against the schema (R32), −3 findings, +0.
2. **Still open from SSA Part 6 / CI report, unchanged:** (a) the remaining drafting identifiers in applied marker text — SC-3's "(H1 **C2**)" (applied line 597), SC-10's "F-5" — must be resolved to registered citations or struck at the real application (SSA Part 6 item 4; CI §1.5); (b) H1a's "Six class C changes" and H1b's six-row table undercount the amendment (CI §7 obs. 1); (c) K1's F-1 (row 28 / line 449), F-5 (§6.1's closed "Five bodies" heading vs SC-10), F-8 (declaration edits implied, not performed); (d) the N4 instance-data residue (SC-13b(b1)'s STOP for the label-availability detector today); (e) the 816/830 conflict recorded in §AB, flagged, deliberately unresolved; (f) P7's citation-scope items on SC-13a(a3) and SC-13b(b2); (g) the SC-12 / SC-13c(c3) governed-set mirror (deliberate, P7-accepted).
3. **K4 (the declaration scrub) — now 11 findings, all on the unscrubbed declaration** (CI report §2 items 1, 2, 6–14: attribute or cite per SC-9(f)/SC-10(e); two clear under the verbatim-quote rule the moment they are attributed within the 6-line window). Plus the consequential §A.6.0 edits Part 2.3 lists (table header, line 1082's unbolded "iff", the reading-note lead-in, "What the rule yields", the `buy_volume_10s` parenthetical) — not findings, consistency.
4. **Author decisions this pass adds:** (i) accept or reject the consequential SC-4(c)/(d) edits (C-1, C-2) — R32 stands without them; (ii) the open-form scope of §8.2's closing sentence (reaches `waived`; Part 3(i)); (iii) item 8's genus — whether `tests/registration/` is hashed file by file or item 8 names the tools it means (Part 3(ii)); (iv) item 3's README clause; (v) the observation that REQUIRED and OUT OF JURISDICTION are contradictories under SC-3(d) and a unit satisfying both is a declaration defect (Part 2.2 (c)); plus SSA Part 6 item 7's standing decisions (heading tags; Instance-record relocation; §13c-P text — now in H8 form; §AB text — now without the ledger reference; the split's P2 / SC-12 delta / ledger 3.3–3.4 decisions).
5. **Tooling caveat carried:** the checker run here is the working-tree checker on the scratch copy; the hash of the applied scratch `PREREG.md` is sensitive to the CI run's formatting choices (CI report §1.2) and to the placement choices stated in §0 above; an author application that makes different choices will differ in hash while being CI-equivalent.

---

## CLOSING TALLY

| | |
|---|---|
| Clauses delivered, verbatim, ready to apply | **15** — SC-1 … SC-12, SC-13a, SC-13b, SC-13c (+ §13c-P pointer in H8 form, + §AB recording text), **+ 3 INSERTION TEXT blocks** (§8.2, §11 item 8 with two markers, §8.6) |
| S1 — R32 | SC-4(a)/(b) reworded (F-2, F-3, F-4) + consequential (c)/(d) (F-5, F-6) + apparatus (F-1, F-7); rule 9 quoted and unchanged; declaration-side K4 proposal for lines 1047–1056 drafted and scratch-applied; checker **14 → 11, −3 exactly the rule-9 findings, +0**; exit 1 (K4 pending); pytest **136 / 1** (same test) at both states |
| S2 — three insertions | anchors 915 / 961 / 1054 (+ amended sites 1050, 97) each **match count 1** in the pristine file and at apply; texts in Part 3 and Part 1; H-L13 principle recorded at 3(ii); CI-neutral (11 findings, 136/1) |
| S3 — Q4's three defects | §AB ledger-3.4 reference struck (F-13); §13c-P reduced to H8 form (F-12); (c5)(i) 'only' dropped, freeze → SC-3(h)/SC-8 (F-11) |
| K1 accounting | unchanged — 75 covered / 1 uncoverable (row 28) / 26 non-gate (7 → PREREG, 19 PRACTICES) / 36 instance |
| Repo files edited | **none**; git state-changing commands run: **none** |

