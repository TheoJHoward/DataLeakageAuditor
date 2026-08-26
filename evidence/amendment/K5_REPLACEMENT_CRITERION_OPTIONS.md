# K5 — §10.2 REPLACEMENT-CRITERION CANDIDATES

**Item K5. Design deliverable of OPTIONS, not a choice.** Three candidate replacement criteria for
PREREG.md §10.2 criterion 2, produced because R22 determined that R9's §6.2 criterion-3 amendment
does **not** discharge PREREG.md line 1033. Each candidate is stated in full against the six
required parts. **None is recommended.** The comparison table at the end sets out what each buys
and what each costs; §9 states plainly that the choice is the author's.

**Nothing here is drafted into `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` or
`HISTORY.md`.** No git command was run. All quotes are verbatim with line numbers, from the two
files as they stand this pass (`PREREG.md` 1099 lines, `AVAILABILITY_DECLARATION.md` 3684 lines).

---

## 1. THE REGISTERED TEXTS THE CANDIDATES MUST SATISFY

**PREREG.md lines 1030–1031** — the criterion being replaced:

> 2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**
>    **Where the fixture is semantically ambiguous** (§6.2), this criterion is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning.**

**PREREG.md line 1033** — the three-part obligation:

> On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**PREREG.md line 1035** — THE FLOOR. Its three limbs are the spine of §5 of this file:

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

**PREREG.md line 472** — the incumbent unit, and the only place in the registration where a
proof-tier count over labelled leaking sources is defined:

> **k of N** labelled leaking sources received at least one primary PROVEN finding **attributed to that source**.

**PREREG.md line 449** — the branch that fires, and the condition it attaches to the fixture:

> - **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.

**AVAILABILITY_DECLARATION.md lines 1548–1556** — §A.12's definition of the word in limb 2:

> A runtime detector is **WAIVED** with respect to a criterion when the criterion is written,
> configured, or reported in any way that makes the detector's own result incapable of changing
> the criterion's outcome. Concretely, a detector is waived if any of the following holds:
> **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but
> its findings are not required to be non-empty for a pass, so its contribution is optional;
> **(iii)** the criterion can be satisfied by the other detector's output alone; **(iv)** its
> threshold is set at a level it meets without executing, or by construction; or **(v)** its
> cases are reported under §7.7's `waived` coverage state rather than executed to a terminal
> result.

**The two runtime detectors are L2a and L3.1** — AVAILABILITY_DECLARATION.md lines 1543–1544,
citing PREREG.md lines 318, 320 and 1039.

---

## 2. SEVEN CROSS-CUTTING FINDINGS THAT BIND ALL THREE CANDIDATES

These are stated once, here, because every candidate inherits them. Each is a *drafting
consequence* the amendment must dispose of whichever candidate is chosen.

### X1 — "criterion 3's gates in force" is AMBIGUOUS, and the plural points away from R22's reading

Line 1035's third limb says "criterion 3's **gates** in force." There are two criterion 3s:

| Reading | Text | Does it have "gates", plural? |
|---|---|---|
| **§6.2 criterion 3** (PREREG.md line 461) | "**No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`." | No. One prohibition, no named gates. |
| **§10.2 criterion 3** (PREREG.md lines 1036–1040) | Excessive false alarms on clean cases → ships experimental | **Yes — exactly two, both named**: the "**Finding-rate gate**" (line 1037) and the "**Completion gate, separate and joint**" (line 1038). |

Line 1035 sits *inside* §10.2, three lines above §10.2 criterion 3, and the word "gates" matches
§10.2 criterion 3's own two named gates exactly. R22 read the limb as §6.2 criterion 3 and built
GROUND 1 partly on that reading ("Criterion 3 is named as a **component of the floor**"). **R22's
conclusion survives either reading** — under the §10.2 reading, R9's §6.2 amendment is *even more
plainly* a different object — but the ambiguity is live for drafting, because the two readings
impose different obligations on the replacement.

**Disposition available under §D.3** (resolve toward the stronger reading): **hold both in force.**
They do not conflict; they operate at different levels. §6.2 criterion 3 as amended by R9 is an
acceptance consequence (a false positive on a map-zero corrected cell **fails the gate**);
§10.2 criterion 3 is a shipping consequence (a detector or mode over the 20% finding-rate gate or
under the 60% completion floor **ships experimental** and is excluded from
`assert_no_proven_leakage()`). Every candidate below therefore carries **two** false-alarm limbs,
and each is instantiated per candidate in part 4.

### X2 — THE L2a PROBLEM. It is the hard one, and no candidate escapes it

The declaration removes L2a's findings from this gate in three places:

- **line 1223–1224 (§A.6.2):** "**An L2a label-base finding on them is neither credited nor
  penalized by this availability gate.**"
- **lines 2797–2798 (§C.3):** "**That character is assigned to L2a jurisdiction and is OUTSIDE this
  availability gate.**"
- **lines 454–455 (§5, item 4):** "**No separate label-availability criterion is created for them.**
  This declaration adds no new gate criterion; §6.2's four criteria as amended in §A are the whole
  gate."

So **the declaration as it stands enumerates no L2a-scored unit at all.** There is no L2a analogue
of §A.6.1's eleven. Measured against §A.12's own limbs, a criterion built only on the declared
availability map or the declared REQUIRED columns waives L2a under (i), (ii) and (iii) — which is
exactly R22's third finding, and it disqualifies such a criterion outright.

The consequence for candidate design is unavoidable and should not be softened:

> **Any admissible replacement needs a conjunctive L2a limb whose satisfaction requires L2a to
> execute and produce a non-empty, adjudicated result. That requires the declaration to enumerate
> a non-empty L2a expectation set — instance data that does not exist today, and that §5 item 4
> currently disclaims.**

Three further points that make this sharper, not softer:

1. **A silence-shaped L2a limb does not fix it.** Requiring L2a to be *silent* (on the corrected
   side, or on the shared label vector) is a threshold "it meets without executing" — **limb
   (iv)** — so a silence-only limb waives L2a just as surely as omitting it.
2. **PREREG.md line 816 is the mechanism by which L2a could be dropped "by registered rule", and
   §A.12 limb (i) calls that a waiver.** Line 816, verbatim: "**A combination that is
   `not_applicable` on every scope-eligible case in a body of data publishes its counts and
   suppresses its yields, rates, and gates**, naming the reason." If L2a is `not_applicable`
   across the fixture, line 816 suppresses **its gates** — and a §10.2 replacement whose L2a limb
   is suppressed is a criterion from whose denominator L2a has been excluded. **Line 816 and
   §A.12 limb (i) point in opposite directions and the amendment must say which governs for the
   §10.2 replacement.** §A.12's own limb 4 ("**'No data' is not 'waived'**") is the nearest
   existing hook, and it resolves *against* suppression, but it is written about cells, not about
   an entire combination.
3. **Whether a true L2a-detectable dependency exists on this fixture is NOT established by the
   declaration and is not established here.** The declaration's own material shows only that the
   fixture's features sit **at** the label base `mid(t)` (lines 2793–2799), which is
   contemporaneous and therefore *not* an unavailable-label read; §5's caveats record
   label-magnitude row filtering in the **phase5** lineage (`phase5_ml.py` line 679,
   `phase5_fixed.py` lines 678/747, declaration lines 465–483) whose presence or absence in the
   **phase7** fixture builder is not stated anywhere in this file. **Nothing in this deliverable
   asserts that such an instance exists.** Establishing one is a Phase 0 evidence task; if it
   cannot be established, candidate C's admissibility limb is the only one of the three that
   converts that fact into a stated outcome rather than a silent waiver.

### X3 — §A.12 limb 6 forces a PROMOTED-combination limb into every candidate

§A.12 limb 6 (declaration lines 1587–1589): "**Per-combination waiving is still waiving.** Line
1039 applies gates per combination; dropping a detector from one combination's criterion while
scoring it in another waives it for that combination, and is class C."

PREREG.md line 768: "**Proof yield exists only for the `preserving` combination.**" So any
threshold stated in proof-tier terms lives *only* in the preserving row, and the `promoted` row is
dropped from the criterion — waived for that combination on the declaration's own definition.

**Every candidate below therefore carries a promoted-row limb**, in the same shape in all three:
the `promoted` combination's **evidence yield** (PREREG.md line 768, line 792) is computed and
published against the same declared expectation set, its findings on declared-zero units count
against the false-alarm limbs, and **no promoted finding substitutes for a required PROVEN one**
(§3.2, PREREG.md lines 299–303, 517).

### X4 — Promoting §A.10's *k* of *N* = 11 is an ACT OF REGISTRATION and must be stated

PREREG.md line 470 reports proof capability **instead of requiring it**; line 476: "**It is
published as a count, never as a decimal or percentage**, and it is identified as a descriptive
fixture outcome rather than a performance rate." §A.10 item 1 (declaration lines 1477–1480) fixes
**N = 11** for that descriptive count.

Candidates A and B (and C's proof limb) turn a proof-tier count into a **pass/fail threshold**.
That is precisely the silent promotion R22's owed item 3 names. It is available — line 1035's own
first limb ("non-zero **proof yield**") already imports tier into §10.2, unlike §6.2, whose gate is
"discrimination, not tier" (PREREG.md line 453) — but it must be performed **on the record**, in
the amendment text, in words to the effect that:

> the *k*-of-*N* count of line 472 remains a descriptive, non-gating fixture outcome **for §6.2**,
> and is additionally **promoted to a gate threshold for §10.2's replacement criterion only**;
> §6.2's four acceptance criteria are unchanged by this promotion.

Without that sentence, a reader has one number doing two jobs under two authorities, which is the
duplicated-authority failure §7.0 exists to forbid.

### X5 — The unit grammar is closed, and "map cell" is not in it

PREREG.md line 722, constitution rule 2, verbatim: "Units come from the fixed grammar: case,
cohort, **feature**, feature-cohort, cluster, code-site, candidate."

- "Labelled leaking source" (line 472) maps onto **feature**. Legal.
- §7.2's EvidenceEvent pair maps onto **feature-cohort**. Legal.
- The declared map's **(side, instrument, month, class)** cell maps onto nothing in the grammar. A
  candidate using it must either (a) bind the cell explicitly onto **cohort** in the amendment
  text, or (b) add a unit to the grammar — itself class C on line 93's face ("a needed *new*
  branch, **unit**, denominator, coverage state, tier licence, or acceptance criterion").

This is a real cost against candidate B, and it is priced there.

### X6 — R22's "960 scored map cells" is loose; the artifact's own numbers are three-way

Declaration lines 1962–1965: "**984 rows** = **960 declared-class cells** (2 sides x 8 instruments
x 6 months x 10 classes) **plus 24 rows carrying the 11th diagnostic class** `mbo_all_rows`. Of
the 960: **888 `SCORED`** and **72 `UNSCORED_FOR_LACK_OF_DATA`**."

So "the 960 scored map cells" of R22's owed item 4 is **not** a scored-cell count: 960 is the
declared-class total and **888** is the scored count. Any candidate nominating a cell denominator
must name which of 984 / 960 / 888 it means, and the class-set rule at declaration lines 1965–1971
("Any statement of the form 'max across classes' … **must name the class set it maximises over**")
binds it.

**A further cut matters more than the SCORED/UNSCORED one.** Six of the declared ten classes are
`mbo_*` (line 1969), and declaration lines 1189–1192 state that **Phase 7 feeds no MBO columns at
all**, so the six MBO classes "characterise the fixture's MBO stream against the lattice **without
attaching to any fed column**." A detector auditing the 35 fed columns cannot produce a finding
against an `mbo_*` cell — those cells are unmatchable by construction, not by defect. The
**fed-consumed** cell set is therefore the trade classes only, and one of those is dead:

```
trade-class cells           4 classes x 48 instrument-months x 2 sides       = 384
less trades_buy             degenerate constant, "0 strict and 0 equal in
                            every one of its 96 cells, on BOTH sides"
                            (declaration lines 2812-2814; §C.4(a))           =  96
                                                                              ----
fed-consumed scored cells                                                    = 288
less trades_sell            "(= trades_all here, §15)" — declaration line
                            1164; 96 cells that duplicate trades_all and
                            carry no independent information                =  96
                                                                              ----
independent fed-consumed cells                                               = 192
```

**Derived in this file from the declaration's own figures; it must be re-read from
`n1\declared_map.csv` at freeze rather than taken from here.** The 288/192 split is the live
choice for candidate B: 288 inflates an agreement count with 96 duplicate cells, 192 is the honest
independent set.

### X7 — Two framing obligations that R22's five owed items do not name, and one defect

1. **Line 449's label.** Under the fired branch the fixture "may be used under an explicit
   **labelled hypothetical declaration**, and does not carry full acceptance weight." The
   replacement criterion must be stated as evaluated **under that label**, and the amendment
   should say what "does not carry full acceptance weight" costs — otherwise the replacement
   silently restores the weight the branch removed.
2. **§E's input surface must be carried into the criterion.** Declaration lines 3506–3513: a
   detector never receives "**the declared ground-truth map** … nor any summary, cohort list, or
   per-cell count derived from it", because "**Under the amended criterion 3 the map IS the
   scoring key.**" Every candidate scored against declared data inherits this: the criterion is a
   harness artifact, and the amendment must say so in the criterion's own text, not only in the
   declaration.
3. **Drafting defect, recorded once.** §10.2's printed enumeration **begins at item 2** — there is
   no item 1 (PREREG.md lines 1028–1043). The amendment touches this section and should fix the
   numbering, or state that criterion 1 is §10.1's kill gate and is deliberately numbered there.

---

## 3. THE THREE CANDIDATES AT A GLANCE

| | **A — Attributed proof floor** | **B — Cell-sign agreement** | **C — Two-detector separation with an admissibility limb** |
|---|---|---|---|
| Unit | labelled leaking source at PROVEN tier (**feature**) | fed-consumed scored map **cell**, bound onto **cohort** | **feature-cohort** pair |
| Denominator | the 11 REQUIRED columns + declared L2a set | 288 (or 192) fed-consumed trade-class cells | all scope-eligible declared labelled pairs, per side |
| Shape | count of proved sources ≥ a floor | sign agreement, cell by cell, both sides | yield floor + per-instrument-month indicator agreement |
| Distinct catch | tier collapse and wrong-ground attribution | wrong-side / wrong-instrument-month localisation | probing-coverage failure |
| L2a | conjunctive positive limb (needs declared set) | conjunctive positive limb (needs declared set) — **without it, disqualified** | conjunctive positive limb **plus** an explicit admissibility test that converts an empty set into a STOP |

---

## 4. THE CANDIDATES IN FULL

---

# CANDIDATE A — ATTRIBUTED PROOF FLOOR OVER THE REQUIRED ENUMERATION

**Stated as a §10.2 replacement, in the form it would take in `PREREG.md`:**

> **§10.2 criterion 2 (replacement, ambiguity branch).** Where the acceptance fixture is recorded
> as semantically ambiguous under §6.2 and is used under a labelled hypothetical declaration
> (line 449), criterion 2 is replaced by the following, and failure of any limb is a **stop**.
> Evaluated on the frozen default configuration, on one side at a time, with the declaration's
> scoring key withheld from the detector.
>
> **(a) Proof limb, L3.1.** Over the declaration's frozen REQUIRED enumeration of size *N*, the
> `preserving` combination of L3.1 must produce at least **⌊N/2⌋ + 1** labelled sources each
> carrying **at least one primary PROVEN finding attributed to that source on its declared
> violation ground**, in a side and instrument-month where the declaration's map declares the
> violation for that source's governing class.
> **(b) Proof limb, L2a.** Over the declaration's frozen L2a expectation set of size *N₂*, the
> `preserving` combination of L2a must produce at least **1** unit carrying a primary PROVEN
> finding attributed to that unit. *N₂ ≥ 1 is a condition of the fixture's admissibility under
> this criterion.*
> **(c) Promoted-row limb.** Both detectors' `promoted` combinations are executed to a terminal
> result and publish evidence yield over the same denominators. A `dtype_promoted` finding
> satisfies neither (a) nor (b) (§3.2).
> **(d) False-alarm limbs.** §6.2 criterion 3 as amended remains in force cell by cell, and
> §10.2 criterion 3's finding-rate and completion gates are computed per combination over the
> declaration's declared-zero units.
>
> Limbs (a)–(d) are conjunctive.

**Schema / instance split (R24).** Generic in `PREREG.md`: the limb structure, the unit
("labelled leaking source at PROVEN tier, attributed on its declared ground"), the threshold
*rule* ⌊N/2⌋+1, the requirement that the denominator be a frozen declared enumeration, the
conjunction, and the promoted-row limb. Instance in the declaration: the eleven names (§A.6.1),
*N* = 11, the L2a expectation set and *N₂*, the governing map classes, the declared-zero units.
Estimated cost against the 8–12 generic-clause target: **one clause with four lettered limbs.**

### A.1 UNIT

**The labelled leaking source at PROVEN tier** — PREREG.md line 472's incumbent, taken unchanged.
In the constitution's grammar (line 722) the unit is **feature**. A unit is credited only on a
**primary** finding (not secondary, §7.6), at **PROVEN** tier (which by §3.1 means the
`preserving` combination), **attributed to that source**.

**One addition to the incumbent, and it is not a departure but a sharpening:** attribution is to
the source **on its declared violation ground**. This is the declaration's own §C.5(c) discipline
(lines 2886–2893): for `vwap_distance`, "**A finding that satisfies it must be a finding about the
absorbed wall-clock-second trade window** … A detector that flags `vwap_distance` for reading the
decision row's own mid has **not** produced the required finding … it has named the right column on
the wrong ground". Without the ground clause the unit is satisfiable by a coincidence of column
names; with it, the unit is what line 472's attribution clause was written to protect ("without it
a PROVEN finding on a *descendant* could be read as its source 'reaching PROVEN'", line 474).

For L2a the unit is the same shape one level over: a **declared unavailable-label dependency** —
a (feature, unavailable-label-cell class) unit that the declaration enumerates by name. Also a
**feature** unit in the grammar.

**Cost of not departing from line 472:** the unit says nothing about *where* the finding occurred.
One PROVEN finding on `net_delta_1s` in one instrument-month on one side credits the unit for the
whole gate. Candidate A cannot see localisation error at all. That is candidate B's ground.

### A.2 THRESHOLD

**Parameterised form:** *k_d ≥ max(1, ⌈f · N_d⌉)* for each runtime detector *d*, with *f* frozen
in the amendment.

**Stated value, L3.1: f such that the threshold is the strict majority rule ⌊N/2⌋ + 1. With the
declaration's N = 11 that is the number 6.**
**Stated value, L2a: k ≥ 1 of N₂** (the literal floor, because *N₂* is small or unknown).

**Selection procedure.** The threshold is a function of the declared enumeration's *size alone*,
computed by a stated arithmetic rule (⌊N/2⌋+1). It reads no detector output, no development-corpus
behaviour, and no fixture result. That is what makes it committable before Phase 1 under line
1035's closing sentence: "a criterion chosen because it works after tuning is a criterion shaped by
tuning." A strict majority is defensible as the point at which the count stops being an anecdote
about one column family and starts being a statement about the enumeration.

**Freeze point.** *N* and the enumeration freeze at the `prereg-v30a` tag under §D.1; the number
**6** is computed by the rule and **printed as a number in the amendment text**, so that a later
change to *N* is visible as a change to the criterion rather than silently recomputed. If *N*
changes (e.g. `book_imbalance_ratio` is reinstated per §C.4(c), which declaration line 1241 already
calls class C), the threshold is re-derived and the change is itself an amendment.

**Two alternatives the author should see, because the choice of *f* is where this candidate is
soft:**

| *f* | Threshold at N = 11 | Argument for | Argument against |
|---|---|---|---|
| floor only | **1** | the literal reading of line 1035's "non-zero proof yield"; unfalsifiably admissible | one proved column out of eleven passes a kill gate; a tool that proves `net_delta_1s` and nothing else is not distinguishable from a tool that got lucky |
| **⌊N/2⌋+1** | **6** | a function of *N* alone; not tunable; survives partial dtype promotion | the majority rule has no evidential meaning of its own — it is a convention, and the amendment should say so rather than dress it as a statistic |
| 1.0 | **11** | mirrors §6.2 criterion 1's coverage requirement, one tier higher | **at material risk from §3.2.** PREREG.md line 305: "On an integer-bearing frame the preserving set can collapse to `shuffle`". Several REQUIRED columns are integer counts by construction (`trade_count_1s`, `large_trade_count_10s`, and the volume rollups). Line 517 requires an integer-containing frame where only a promoting strategy fires to produce "**REVIEW `dtype_promoted`, never PROVEN**". An all-11-at-PROVEN threshold can therefore stop the project for a dtype reason rather than a detection reason — the exact failure §C.4(a) declares `buy_volume_10s` out of the denominator to avoid |

### A.3 DENOMINATOR

**The 11 REQUIRED columns of §A.6.1** (declaration lines 1147–1174; partition check line 1261:
REQUIRED 11 + OUT OF JURISDICTION 22 + UNSCORED 2 = 35), for L3.1; **the declared L2a expectation
set**, size *N₂*, for L2a.

**Justified among the real candidates:**

- **Against the scored map cells:** the map's unit is (side, instrument, month, class); its classes
  are **event-source** classes, not columns. Line 472's unit is attributed **to a source**, and a
  cell carries no source attribution. Using cells for a proof-tier limb requires a bridge from
  class to column that the declaration supplies only in one direction (§A.6.1's "governing map
  class" column).
- **Against the instrument-months:** an instrument-month is a **case** in the grammar; it cannot
  carry a per-source attribution at all.
- **The known hazard of this choice, stated rather than buried.** Declaration line 1147 names the
  eleven as "**the criterion-1 denominator**". Re-using it as §10.2's replacement denominator means
  **one enumeration governs two criteria at two levels** — a §6.2 acceptance criterion and a §10.2
  kill criterion. A single error in the enumeration then flips both, and there is no independent
  check left. The amendment must state the re-use deliberately ("§10.2's replacement adopts §A.6.1's
  enumeration as its denominator") rather than let it happen by proximity.

### A.4 THE §10.2 FLOOR, TESTED LIMB BY LIMB

**Limb 1 — "non-zero proof yield".** **Satisfied, and exceeded.** Limb (a) requires 6 proved
sources and limb (b) requires 1, both at PROVEN tier, both in the `preserving` combination where
PREREG.md line 768 says proof yield exists. Line 1035 permits stricter.

**Limb 2 — "neither runtime detector waived", tested against §A.12 (i)–(v):**

| §A.12 limb | L3.1 | L2a |
|---|---|---|
| (i) excluded from the denominator | No — limb (a) is its denominator | No — limb (b) gives it its own denominator *N₂* |
| (ii) findings not required non-empty | No — 6 required | No — 1 required, non-empty by construction |
| (iii) satisfiable by the other detector's output alone | No — (a) and (b) are **conjunctive**; L3.1 output cannot satisfy (b) | No — same |
| (iv) threshold met without executing / by construction | No — a PROVEN finding requires a preserving intervention run under a passing determinism guard (§3.1) | No — same, and this is why limb (b) is *positive* and not a silence test |
| (v) reported under §7.7's `waived` coverage state | No — limb (c) requires terminal execution of both combinations | No — same |
| §A.12 limb 6 (per-combination) | Covered by limb (c) | Covered by limb (c) |

**Verdict: L2a unwaived — CONDITIONAL ON *N₂* ≥ 1 BEING DECLARED.** If the declaration cannot
enumerate a single L2a unit, limb (b) is unsatisfiable and candidate A becomes a criterion that
**stops the project by construction**. That is not a waiver (limb (iv) is about a threshold met
*without* executing, not a threshold that cannot be met), but it is a real and severe cost, and
candidate A does not make that outcome visible in its own text. Candidate C does.

**Limb 3 — "criterion 3's gates in force", under both readings (X1):**

- **§6.2 criterion 3 as amended by R9:** carried by limb (d) — findings on corrected-side cells the
  map marks zero remain false positives and still fail the gate (declaration lines 1431–1432).
- **§10.2 criterion 3:** carried by limb (d) — the finding-rate gate `k ≥ floor(0.20 × N) + 1` and
  the 60% completion floor computed **per combination** (line 1039), with *N* = the declared-zero
  units for that combination. On this fixture the natural instantiation is the **22 OUT OF
  JURISDICTION columns** (declaration line 1262), on which "**An availability-class finding on any
  of them is a FALSE POSITIVE**" (line 1197): `floor(0.20 × 22) + 1 = 5`, so five false positives
  on the 22 ships that combination experimental. **Note the two gates do not agree in
  consequence** — §6.2's is a fail, §10.2's is an experimental marking — and holding both is the
  §D.3-stronger reading, not a contradiction.

### A.5 THE FAILURE MODE IT CATCHES THAT THE OTHERS DO NOT

**Tier collapse, and wrong-ground attribution.**

1. **A detector whose entire evidence base is promoting strategies.** It fires on all eleven
   REQUIRED columns, every finding is `dtype_promoted` REVIEW, and §6.2 criterion 1 — which
   explicitly accepts REVIEW ("whether its promotion status makes the reported tier PROVEN or
   REVIEW", line 459) — **passes it**. Candidate A stops the project at limb (a). Candidate B's
   cell test is tier-agnostic and would pass it on 287 of 288 cells with a single PROVEN finding
   satisfying its bolted-on proof limb; candidate C's yield floor catches it only at the ≥1 level.
   **A is the only candidate whose threshold is tier-carrying at scale.**
2. **The right column on the wrong ground.** A detector that flags `vwap_distance` for its
   same-row `mid[t]` read — declared availability-legal at line 2896 — has named a REQUIRED column
   and produced a finding that §C.5(d) says "**neither satisfies criterion 1 nor substitutes for
   the finding (c) requires**". Only a unit carrying the ground clause rejects it. Cell-level and
   pair-level units do not: the cell is keyed on class, not ground.

### A.6 R22's FIVE OWED ITEMS, ITEMISED

| # | Owed | Supplied by A? | How |
|---|---|---|---|
| 1 | A replacement **stated as a §10.2 replacement** | **Yes** | Drafted above as replacement text for §10.2 criterion 2 under the ambiguity branch, with "→ stop" preserved as the consequence. It says what the runtime detectors must achieve *in place of* separating contaminated from corrected. |
| 2 | A **proof-yield unit** | **Yes** | Line 472's incumbent, unchanged and sharpened: labelled leaking source, primary, PROVEN, attributed to the source **on its declared ground** (§C.5(c)). Grammar unit: **feature** (line 722). |
| 3 | A **threshold** | **Yes, with the promotion declared** | ⌊N/2⌋+1 = **6** for L3.1, **1** for L2a; selection procedure is a function of *N* alone; frozen at the tag with the number printed. **Performs X4's promotion of §A.10's k-of-N from descriptive to gating, for §10.2 only, and the amendment must say so in terms.** |
| 4 | A **denominator** | **Yes** | The 11 REQUIRED columns (§A.6.1) for L3.1; the declared L2a expectation set for L2a. Nominated explicitly, with the re-use of criterion 1's enumeration declared rather than assumed. |
| 5 | An **L2a limb keeping L2a unwaived** | **Yes, conditionally** | Conjunctive limb (b) with its own denominator and a positive, execution-requiring threshold; clears (i)–(v) and limb 6. **Conditional on the declaration enumerating N₂ ≥ 1** (X2). If it cannot, A is unsatisfiable rather than admissible-and-weak. |

---

# CANDIDATE B — CELL-SIGN AGREEMENT OVER THE FED-CONSUMED MAP CELLS

**Stated as a §10.2 replacement, in the form it would take in `PREREG.md`:**

> **§10.2 criterion 2 (replacement, ambiguity branch).** … failure of any limb is a **stop**.
>
> **(a) Agreement limb.** Over the declaration's frozen set of **fed-consumed scored map cells** —
> the cells whose class attaches to at least one column of the fixture's fed universe, after the
> declared exclusions — the detector's per-cell output sign must agree with the map's:
> for every cell, *(the run for that side produced at least one primary finding attributed to a
> column whose governing class is that cell's class, in that instrument-month)* **iff** *(that
> cell's `strict_count` > 0)*. **Permitted disagreements: ⌊ε · D⌋, with ε frozen in the
> amendment; disagreements of the false-positive direction are counted separately and are capped
> at zero.**
> **(b) Proof limb.** At least one cell-agreement on the contaminated side and at least one within
> the declared corrected-side violating instrument-months must be carried by a **primary PROVEN**
> finding attributed to a REQUIRED column on its declared ground.
> **(c) L2a limb.** Conjunctive, over the declaration's frozen L2a expectation set, requiring at
> least one primary PROVEN L2a finding attributed to a declared unit. *Without this limb the
> criterion is inadmissible under line 1035 — see B.4.*
> **(d) Promoted-row limb** and **(e) false-alarm limbs**, as in candidate A.

**Schema / instance split (R24).** Generic: the sign-agreement rule, the "fed-consumed" qualifier
(a class attaches to a fed column or its cells are out of the criterion), the two-directional
disagreement accounting with the false-positive direction capped separately, the ε form and its
freeze point, the conjunctive L2a and promoted limbs. Instance: the cell set and its size *D*, the
class-to-column governing map, the exclusions (`trades_buy`, `book_imbalance_ratio`), the
per-cell `strict_count` values, the 18-of-48 list.

### B.1 UNIT

**The scored map cell** — (side, instrument, month, class) at boundary `decision_T`,
`scored_flag = SCORED`, schema at declaration lines 1960–1962.

**This is a departure from line 472's incumbent unit, and it costs three things. Named, because
the K5 brief requires it:**

1. **It is not in the grammar** (X5). The amendment must bind cell → **cohort** explicitly. That
   binding is defensible — the declaration's §C.2 cohort predicate already carves the rows within
   an instrument-month where a violation is possible, and a cell is a class-restricted view of one
   — but it is an act of registration, not a reading.
2. **It carries no source attribution.** Line 472's attribution clause has no purchase on a cell:
   a cell says "this class violates here", not "this column was correctly named". The bridge is
   §A.6.1's "governing map class" column, which runs class ← column; running it column ← class is
   **badly one-to-many on this fixture**. Read off declaration lines 1159–1169: **nine of the
   eleven REQUIRED columns are governed by `trades_all`** (rows 1–5, 8, 9, 10, 11), a **tenth**
   (`sell_volume_10s`) by `trades_sell`, which line 1164 records as "**(≡ `trades_all` here,
   §15)**", and **only `large_trade_count_10s` has an independent governing class**
   (`trades_large`). So a single correct finding on `net_delta_1s` credits the same cell that ten
   of the eleven columns point at, and **the entire cell denominator distinguishes at most two
   column families.** Cell agreement is therefore materially weaker than per-column attribution —
   this is the single strongest argument against candidate B — and limb (b) exists to stop it from
   being the whole criterion.
3. **It is tier-agnostic.** The map records `strict_count`, not tier. Limb 1 of the floor
   (non-zero proof yield) therefore cannot be satisfied by the agreement limb at all, which is
   why limb (b) is bolted on. A candidate whose headline limb cannot reach the floor's first limb
   is carrying an extra part, and that is a structural criticism of B, not a detail.

**What the departure buys:** the cell is the only unit among the three that is **keyed on side and
instrument-month**. It is the only one that can test the thing the original criterion 2 was
about — separating contaminated from corrected — now that the corrected side is not clean.

### B.2 THRESHOLD

**Form:** zero false-positive-direction disagreements; at most **⌊ε · D⌋** missed-direction
disagreements.

**Two stated sub-forms:**

| Sub-form | ε | With D = 288 | With D = 192 |
|---|---|---|---|
| **B-exact** | 0 | 0 permitted | 0 permitted |
| **B-tolerant** | **72/960 = 0.075** | ⌊21.6⌋ = **21** | ⌊14.4⌋ = **14** |

**Selection procedure for ε.** ε is **the map's own unscored fraction** — 72 `UNSCORED_FOR_LACK_OF_DATA`
of 960 declared-class cells (declaration lines 1962–1965). It is a property of the declared
artifact, computed before any detector exists, and it reads no detector output. The argument for
it as a tolerance: it is the fraction of the map the declaration itself could not measure, so it
is the scale at which the map's own coverage is imperfect. **The argument against it, stated
because it is not weak:** the unscored fraction is *nq's missing MBO data* (declaration lines
1242–1245) and has no causal relation to a detector's miss rate on trade-class cells. It is a
detector-blind number, which is what line 1035 requires, but it is not a *meaningful* number, and
the amendment should say that ε is a convention rather than an estimate.

**Freeze point.** *D*, the cell set, and every `strict_count` freeze at the `prereg-v30a` tag under
§D.1 item 3 ("`n1\declared_map.csv` as frozen"). ε and the resulting integer cap are printed in
the amendment.

**A promotion note.** B's limb (b) is a ≥1 proof-tier requirement, so B also performs X4's
promotion, at the floor rather than at 6. It must be stated on the record just the same.

### B.3 DENOMINATOR

**The fed-consumed scored trade-class cells: D = 288, or D = 192 on the independent cut.**
Derivation at X6, from declaration lines 1962–1969, 1189–1192, 2812–2814 and 1164.

**Justified among the real candidates:**

- **Not all 984 rows:** 24 are the `mbo_all_rows` 11th diagnostic class, which the class-set rule
  at lines 1965–1971 says is "**NOT one of the declared 10**".
- **Not all 960:** 72 are `UNSCORED_FOR_LACK_OF_DATA`, and declaration lines 1228–1229 are explicit that
  an unscored cell "enters no denominator, contributes to no rate, and **cannot be reported as a
  pass**".
- **Not all 888 SCORED:** 576 of the declared-class cells are `mbo_*`, and **no fed column consumes
  them** (lines 1189–1192). Including them puts cells in the denominator that a conforming
  detector cannot match by construction — the exact defect §C.4(a) removes `buy_volume_10s` for,
  at cell scale. A criterion whose denominator contains structurally unmatchable units is
  unpassable for a reason unrelated to detection.
- **288 vs 192:** 288 includes `trades_sell`, which declaration line 1164 records as "**(≡
  `trades_all` here, §15)**". Ninety-six duplicate cells inflate an agreement count by a third
  without adding information. **192 is the honest set; 288 is the set a literal reading of "trade
  classes" yields.** The amendment must pick one and say which.
- **Not the 11 columns:** they carry no side or instrument-month, which is precisely what B exists
  to test.
- **Not the 18-of-48 instrument-months alone:** that set is the *positive* corrected-side
  population; a criterion scored only there cannot see a false positive in the other 30, which is
  the corrected side's main failure surface.

### B.4 THE §10.2 FLOOR, TESTED LIMB BY LIMB

**Limb 1 — "non-zero proof yield".** **Satisfied only by limb (b), not by the headline limb.** The
agreement limb is tier-agnostic; strip (b) and the candidate fails the floor's first limb outright.
Recorded as a structural weakness, not a detail.

**Limb 2 — "neither runtime detector waived":**

> **WITHOUT limb (c), CANDIDATE B IS DISQUALIFIED. Stated plainly, as the K5 brief requires.**
> The declared map is an **availability**-violation map scored by L3.1; it says nothing about
> label availability. Measured against §A.12 (declaration lines 1548–1556), a criterion consisting
> of limbs (a)+(b) alone satisfies **(i)** — L2a is excluded from the cell denominator; **(ii)** —
> its findings are not required non-empty; and **(iii)** — the criterion is satisfiable by L3.1's
> output alone. **That is L2a waived three times over**, and §A.12 lines 1560–1562 say a criterion
> that waives a runtime detector "does not become admissible by being recorded, disclosed,
> justified, or approved." **This is R22's third finding reproduced exactly**, because limbs
> (a)+(b) are R9's map-scoring with a proof limb attached — the attachment fixes the *tier* gap
> and does nothing at all about the *detector* gap.

With limb (c) present, the table is as in candidate A: (i) no — own denominator; (ii) no — 1
required; (iii) no — conjunctive; (iv) no — positive and execution-requiring; (v) no — terminal
execution required by (d). **Same conditionality on *N₂* ≥ 1.**

**Limb 3 — "criterion 3's gates in force", both readings:**

- **§6.2 criterion 3 as amended:** B **is** R9's amended criterion 3 generalised to both sides, so
  this limb is carried natively — and that is also why B is the candidate most at risk of being
  read as "R9 again", which R22 has already ruled is a different object. The amendment must state
  that B *incorporates* the amended criterion 3 as one limb of a §10.2 kill criterion and does not
  *consist of* it.
- **§10.2 criterion 3:** the finding-rate gate has a natural denominator here — the cells the map
  marks zero within *D*. `k ≥ floor(0.20 × N_zero) + 1` per combination, plus the 60% completion
  floor over the same cells. *N_zero* must be read from the frozen artifact at tag time; the
  declaration establishes only that the trades classes are strict-positive on the contaminated
  side in **all 48** instrument-months and on the corrected side in **18** (lines 1154–1155), which
  bounds but does not fix it.

**One interaction the amendment must resolve.** Limb (a)'s false-positive direction is capped at
zero, and §10.2 criterion 3's finding-rate gate permits `floor(0.20 × N_zero)` false findings before
firing. Under §D.3's stronger reading the zero cap governs the **stop** and the 20% gate governs
the **experimental marking** — two different consequences from one count. If the amendment does not
say this, an implementer has two thresholds over one denominator.

### B.5 THE FAILURE MODE IT CATCHES THAT THE OTHERS DO NOT

**Localisation failure — a detector that is right about *what* and wrong about *where*.** Two
concrete shapes:

1. **The corrected side declared clean.** A detector that fires across the contaminated side and is
   silent everywhere on the corrected side passes candidate A completely (A never looks at the
   corrected side) and passes candidate C's positive limbs. It fails B at 18 instrument-months'
   worth of cells. **This is the exact failure the declaration's own near-miss produced** — §F.3
   (declaration lines 3576–3587): an aggregation keyed on wrong column names "returned **all
   zero**", which "would have read as **'the trade-class restriction makes the corrected side
   clean'**", and it was caught "by visual inspection of a CSV row … and **NOT by any control**."
   B is the only candidate of the three that makes that reading a gate failure rather than a
   plausible report.
2. **Spray.** A detector that fires on all eleven REQUIRED columns in every instrument-month on
   both sides has perfect coverage under A and a perfect positive rate under C's positive limb; B
   fails it on every corrected-side cell in the 30 non-violating instrument-months.

### B.6 R22's FIVE OWED ITEMS, ITEMISED

| # | Owed | Supplied by B? | How |
|---|---|---|---|
| 1 | A replacement **stated as a §10.2 replacement** | **Yes** | Drafted as §10.2 criterion 2 replacement text with "→ stop"; it states what the detectors must achieve in place of separation, and — unlike R9 — it is a criterion *over the runtime detectors' behaviour on both sides*, not an acceptance criterion over one side's findings. |
| 2 | A **proof-yield unit** | **Yes, but in the bolted-on limb** | Limb (b) uses line 472's unit unchanged. The headline unit (the cell) supplies no proof-yield unit at all — this is the candidate's structural seam. |
| 3 | A **threshold** | **Yes** | Zero false-positive-direction disagreements; ⌊ε·D⌋ missed-direction, with ε = 0 or 72/960 = 0.075 → 0 / 21 (D = 288) or 0 / 14 (D = 192). Selection procedure detector-blind; freeze at the tag with the integer printed. Also performs X4's promotion at the ≥1 level via limb (b). |
| 4 | A **denominator** | **Yes** | *D* = the fed-consumed scored trade-class cells, 288 or 192, derived at X6 from the declaration's own figures and to be re-read from `n1\declared_map.csv` at freeze. Nominated against the 984 / 960 / 888 / 11 / 18-of-48 alternatives with reasons. |
| 5 | An **L2a limb keeping L2a unwaived** | **Only via limb (c); without it, DISQUALIFIED** | Stated plainly at B.4. Limbs (a)+(b) alone waive L2a under (i), (ii) and (iii). With (c), unwaived and conditional on *N₂* ≥ 1. |

---

# CANDIDATE C — TWO-DETECTOR SEPARATION ON FEATURE-COHORT PAIRS, WITH AN EXPLICIT ADMISSIBILITY LIMB

**Stated as a §10.2 replacement, in the form it would take in `PREREG.md`:**

> **§10.2 criterion 2 (replacement, ambiguity branch).** … failure of any limb is a **stop**.
>
> **(a) Admissibility limb, tested first.** A semantically ambiguous fixture may discharge this
> criterion only if the declaration enumerates, before any run, a **non-empty labelled unit set
> for each runtime detector**. **If either set is empty, the fixture cannot discharge §10.2's
> ambiguity branch and the criterion fails — stop** — unless the fixture is supplemented with a
> declared instance for the empty detector and re-frozen under §11's integrity chain.
> **(b) Yield limb, per detector, per side.** Each runtime detector's `preserving` combination must
> achieve **proof yield > 0** over **all scope-eligible labelled pairs** for that detector (§7.2,
> §7.4), computed per side.
> **(c) Separation limb.** The detector's per-(side, instrument-month) **positive indicator** —
> at least one correct primary finding in that side and instrument-month — must reproduce the
> declaration's declared indicator. **Missed positives: at most ⌊ε · P⌋. False positives on
> declared-negative (side, instrument-month) cells: zero.**
> **(d) Promoted-row limb** and **(e) false-alarm limbs**, as in candidate A.

**Schema / instance split (R24).** Generic: the admissibility test and its stop consequence; the
per-detector, per-side yield floor stated over §7.2's registered denominator; the indicator-agreement
form with an asymmetric tolerance; the ε form; the promoted and false-alarm limbs. Instance: the
labelled pair sets for each detector, the declared per-instrument-month indicators (48 positive
contaminated, 18 positive corrected, 30 negative), *P*, and the cohort predicate.

### C.1 UNIT

**The feature-cohort pair** — §7.2's EvidenceEvent key minus promotion status (PREREG.md line 780:
"`(detector, promotion_status, feature, affected output cohort)` **within a case**"), which is
**feature-cohort** in the grammar (line 722) and is already the unit **proof yield is defined in**:

> PREREG.md line 791: "**proof yield** = correct PROVEN pairs ÷ **all scope-eligible labelled
> pairs**, so a case whose guard failed — or whose only firing strategies promoted — contributes
> misses and stays in the denominator. **This is the headline number for the runtime rows.**"

**Relation to line 472's incumbent.** This is not a departure so much as a refinement in the same
direction: line 472's source is a **feature**; §7.2's pair is that feature **× the cohort the
finding affects**. Both are grammar units, both are proof-tier, both carry attribution. The
declaration already supplies the cohort side: declaration lines 2606–2607 state the consequence —
"**In-cohort ⇒ a violation is POSSIBLE, and must be adjudicated against the map cell**" /
"**Out-of-cohort ⇒ NO violation, on any class, in any measured cell**" — and line 2617 records
that "the cohort predicate reads only the lattice `timestamp` column", so "a reviewer can
regenerate the cohort from the snapshot file alone."

**What the refinement costs:** the pair denominator is the largest of the three by orders of
magnitude, and §7.2's rule that "**A pair whose cohort was never probed counts as a miss only when
no valid probe detected it**" plus §7.4's "a pair in an `unsupported` or `not_applicable` case
remains scope-eligible and remains in §7.2's yield denominators as a miss" (line 830) mean the
denominator is dominated by pairs a real detector will never probe. **A proof yield over that
denominator is a small number by construction**, which is why C's yield limb is stated at the
literal floor (> 0) rather than at a fraction.

### C.2 THRESHOLD

**Two numbers, and they do different jobs.**

1. **Yield limb: proof yield > 0, per detector, per side.** This is line 1035's floor taken
   literally and applied twice per detector. **Selection procedure:** none needed — it is the
   registered floor, not a chosen number, which is the point. **Freeze:** the denominator
   (the labelled pair set) freezes at the tag; the threshold is the floor and cannot move.
2. **Separation limb: ⌊ε · P⌋ missed positives, zero false positives**, over the declared
   per-(side, instrument-month) indicators. With the declaration's figures the indicator
   population is **96 = 2 sides × 48 instrument-months**, of which the declared positives are
   **48 contaminated** (trades classes strict-positive in all 48, lines 1154–1155) **+ 18
   corrected** (§13(b), lines 1991–1993, naming them: cl all 6 months, gc all 6 months,
   zc 2025-08/-09/-10, zs 2025-08/-09/-10) = **P = 66**, and the declared negatives are **30**.
   - **ε = 0** → 0 misses permitted of 66.
   - **ε = 72/960 = 0.075** → ⌊4.95⌋ = **4** misses permitted of 66.

   **Selection procedure for ε:** as in candidate B — the map's own unscored fraction, a
   detector-blind property of the frozen artifact — with the same honest caveat that it is a
   convention rather than an estimate. **The asymmetry is the load-bearing design choice:** misses
   get a tolerance, false positives get none, because a false positive on one of the 30 declared-
   clean corrected instrument-months is the failure this criterion exists to catch and a tolerance
   there would license exactly the reading §F.3's near-miss produced.

   **Freeze:** *P*, the 48/18/30 split and the indicator table freeze at the tag under §D.1; the
   integer 4 (or 0) is printed in the amendment.

**Promotion note (X4):** C's yield limb is proof-tier, so C also promotes the *k*-of-*N* idea —
but at the floor and over §7.2's own registered denominator rather than over §A.10's *N* = 11. **Of
the three, C's promotion is the smallest**: it makes "proof yield > 0" gating, which line 1035
already states as the floor, rather than making the descriptive *k* of *N* a threshold. The
amendment should still record it.

### C.3 DENOMINATOR

**All scope-eligible labelled feature-cohort pairs, per detector, per side** — the denominator
PREREG.md §7.2 already defines for proof yield, with scope-eligibility per §7.4 line 830.

**Justified among the real candidates:**

- **It is the only one that is already registered.** A and B both nominate a denominator built in
  the declaration; C's is PREREG.md's own, instantiated by the declaration. That matters for R24:
  the generic clause names an existing registered denominator, and the declaration supplies only
  the labelled pair set. **It is the smallest schema change of the three.**
- **It is the only one that prices unprobed coverage.** §7.2 line 796 already publishes the
  "unprobed feature-cohort rate" as "a coverage statistic, independent of incidental detection",
  and line 791's denominator keeps unprobed pairs in as misses. A and B are both satisfiable by a
  detector that probes one cohort per column.
- **Against the 11 columns:** they are a feature set with no cohort axis, so they cannot express
  a coverage failure at all.
- **Against the map cells:** the cell axis is (class × instrument-month), which is neither feature
  nor cohort; using it forfeits the registered proof-yield denominator and requires X5's grammar
  binding.
- **The cost, stated:** the labelled pair set for this fixture **does not exist yet**. §A.6.1
  enumerates columns, §13 enumerates cells, and neither enumerates pairs. Producing it is a
  Phase 0 declaration task of real size, and it must be done **before** the tag, under the same
  freeze. **C is the most expensive of the three to instantiate.**

### C.4 THE §10.2 FLOOR, TESTED LIMB BY LIMB

**Limb 1 — "non-zero proof yield".** **Satisfied literally and by name.** Limb (b) *is* the floor's
first limb, applied per detector and per side rather than once globally. No bridging argument is
needed, which is C's cleanest property: the criterion and the floor speak the same vocabulary.

**Limb 2 — "neither runtime detector waived":**

| §A.12 limb | L3.1 | L2a |
|---|---|---|
| (i) excluded from the denominator | No — its own pair set | No — its own pair set, required non-empty by limb (a) |
| (ii) findings not required non-empty | No — yield > 0 per side | No — yield > 0 per side |
| (iii) satisfiable by the other's output alone | No — limbs are per detector and conjunctive | No — same |
| (iv) threshold met without executing | No — proof yield > 0 requires a preserving run reaching PROVEN under a passing determinism guard | No — same |
| (v) reported under §7.7's `waived` state | No — limb (d) requires terminal execution of both combinations | No — same |
| limb 6 (per-combination) | limb (d) | limb (d) |

**And one thing candidates A and B do not do:** limb (a) makes the *N₂* = 0 case an **explicit,
stated outcome of the criterion** rather than an implicit unsatisfiability. This is the direct
disposition of X2's second point: it settles the PREREG.md line 816 / §A.12 limb (i) collision in
favour of §A.12 for this criterion — a combination that is `not_applicable` everywhere does **not**
get its gate suppressed here; it makes the fixture inadmissible. **That is a class C change to how
line 816 reads in this one place, and the amendment must say so**, or the two rules stay in
conflict.

**Limb 3 — "criterion 3's gates in force", both readings:**

- **§6.2 criterion 3 as amended:** carried by limb (e), and reinforced by limb (c)'s zero-tolerance
  on the 30 declared-negative corrected instrument-months.
- **§10.2 criterion 3:** the finding-rate gate and 60% completion floor computed per combination
  over the clean/declared-negative population; §7.7's clean-case rates (lines 872–873) are already
  defined over "execution-eligible clean cases", and an instrument-month is a **case** in the
  grammar, so this instantiation needs no new vocabulary.

### C.5 THE FAILURE MODE IT CATCHES THAT THE OTHERS DO NOT

**Probing-coverage failure — a detector that passes by looking in few places.**

Concretely: a detector that selects one probe cohort per case, finds the leak there, and reports.
Under candidate A it credits all eleven sources and passes at 11 ≥ 6. Under candidate B it produces
a positive indicator in every cell whose class it touched and can reach full agreement. Under C its
proof yield is computed over **all** scope-eligible pairs — including every pair whose cohort was
never probed, which line 791 keeps in the denominator as a miss — so a detector with 3% coverage
reports 3% and the number is visible at the gate. C is also the only candidate whose failure mode
is *reported as a rate a reader can compare across phases*, because it is the same number §7.1
calls "the headline number for the runtime rows".

**Second, and specific to the fixture:** C is the only candidate that makes the *asymmetry between
the sides* a per-detector statement. Both sides get their own yield number, so "the detector found
the contaminated side and could not find the corrected 18" is visible as two numbers rather than
inferred from a cell tally.

### C.6 R22's FIVE OWED ITEMS, ITEMISED

| # | Owed | Supplied by C? | How |
|---|---|---|---|
| 1 | A replacement **stated as a §10.2 replacement** | **Yes** | Drafted as §10.2 criterion 2 replacement text with "→ stop", and it is the candidate closest in shape to the criterion being replaced: two sides, per-detector, separation stated as indicator agreement now that the corrected side is not clean. |
| 2 | A **proof-yield unit** | **Yes — the registered one** | The feature-cohort pair of §7.2 line 780/791, in which proof yield is already defined. No bridge, no grammar addition, no new attribution rule. |
| 3 | A **threshold** | **Yes** | proof yield > 0 per detector per side (the literal floor); plus indicator agreement at ⌊ε·P⌋ misses of P = 66 (0 or 4) and **zero** false positives of 30. Selection procedures detector-blind; freeze at the tag with the integers printed. Performs the smallest of the three X4 promotions. |
| 4 | A **denominator** | **Yes, and it is the pre-registered one** | All scope-eligible labelled feature-cohort pairs (§7.2, §7.4 line 830), per detector per side. Cost: the fixture's labelled pair set does not exist yet and must be enumerated and frozen before the tag. |
| 5 | An **L2a limb keeping L2a unwaived** | **Yes, and it is the only candidate that handles the empty case explicitly** | Limb (b) gives L2a its own positive per-side threshold; limb (a) makes an empty L2a set a **stated stop** rather than a silent unsatisfiability, and disposes of the line 816 / §A.12 limb (i) collision on the record. |

---

## 5. THE FLOOR, SIDE BY SIDE

Line 1035's limbs, quoted once more, against all three:

> The replacement may be stricter than the floor and may not be weaker: **non-zero proof yield**, **neither runtime detector waived**, **criterion 3's gates in force**.

| Floor limb | **A** | **B** | **C** |
|---|---|---|---|
| non-zero proof yield | Satisfied and exceeded (6 sources at PROVEN) | Satisfied **only by the bolted-on limb (b)**; the headline limb is tier-agnostic | Satisfied **literally and by name** — the limb *is* the floor, applied per detector per side |
| neither runtime detector waived — (i) denominator | clear, via limb (b) | **fails without limb (c)** | clear, via limb (b), and enforced by limb (a) |
| — (ii) findings required non-empty | clear | **fails without limb (c)** | clear |
| — (iii) satisfiable by the other alone | clear (conjunctive) | **fails without limb (c)** | clear (conjunctive) |
| — (iv) met without executing | clear (positive, PROVEN-tier) | clear | clear |
| — (v) `waived` coverage state | clear (limb c/d) | clear (limb d) | clear (limb d) |
| — limb 6, per combination | promoted-row limb | promoted-row limb | promoted-row limb |
| — **the N₂ = 0 case** | **unsatisfiable, and silent about it** | **unsatisfiable, and silent about it** | **an explicit stop, stated in the criterion** |
| criterion 3's gates — §6.2 reading | by limb (d) | natively (B *is* R9 generalised) | by limb (e) + limb (c)'s zero cap |
| criterion 3's gates — §10.2 reading | over the 22 OUT OF JURISDICTION: fail at 5 | over the map-zero cells in *D* | over the declared-negative instrument-months |

**No candidate as drafted waives L2a. Candidate B *minus* its limb (c) does — three times over —
and that is the shape R22 already disqualified.**

---

## 6. COMPARISON TABLE

| | **A — Attributed proof floor** | **B — Cell-sign agreement** | **C — Pair yield + separation + admissibility** |
|---|---|---|---|
| **Unit** | labelled leaking source at PROVEN tier, attributed on its declared ground (grammar: **feature**) | scored map cell (side, instrument, month, class), bound onto **cohort** — **not in the grammar as it stands** | feature-cohort pair (grammar: **feature-cohort**), the unit proof yield is already defined in |
| **Departure from line 472's incumbent** | none (sharpened by the ground clause) | **substantial** — no source attribution, tier-agnostic, grammar addition required | minimal — same tier, same attribution, one axis finer |
| **Threshold** | ⌊N/2⌋+1 = **6** of 11 (L3.1), **1** of *N₂* (L2a) | 0 false-positive-direction; ⌊ε·D⌋ missed, ε ∈ {0, 0.075} → 0 or 21 (D=288) / 14 (D=192) | proof yield **> 0** per detector per side; indicator agreement 0 or 4 misses of P=66, **0** false positives of 30 |
| **Threshold is a function of** | the enumeration's size alone | the map's own unscored fraction | the registered floor + the map's unscored fraction |
| **Denominator** | 11 REQUIRED columns + declared L2a set | **288** (or **192**) fed-consumed scored trade-class cells | all scope-eligible labelled pairs, per detector per side |
| **Denominator exists today?** | the 11 do (§A.6.1); the L2a set **does not** | the cells do (`n1\declared_map.csv`); the fed-consumed cut is **derived here and must be re-read at freeze**; L2a set **does not** | **neither** — the labelled pair set must be built and frozen before the tag |
| **Distinct failure mode caught** | tier collapse (all-`dtype_promoted` evidence); right column, wrong ground | corrected side reported clean; spray across instrument-months | low probing coverage; per-side asymmetry as two published numbers |
| **Can be passed by** | a detector that proves 6 columns in one instrument-month on one side and ignores the corrected side | a detector with one PROVEN finding and 287 tier-blind cell matches; a detector that gets `trades_all` right and thereby credits ten of the eleven columns | a detector with perfect coverage but no localisation within a side |
| **Sensitivity to the §A.6.1 enumeration** | **total** — one enumeration governs both §6.2 criterion 1 and §10.2 | indirect (via the class-to-column bridge) | indirect (via the labelled pair set) |
| **Size of the X4 promotion** | largest — makes *k* of *N* = 11 a gate threshold | medium — ≥1 at PROVEN | smallest — makes "proof yield > 0" gating, which the floor already states |
| **Grammar / registration side-effects** | none beyond X4 | **adds or binds a unit** (line 722, class C on line 93's face) | resolves line 816 vs §A.12 limb (i) for this criterion (class C, and it must be stated) |
| **Instantiation cost before the tag** | low (the eleven exist) + the L2a set | medium (re-read and cut the map) + the L2a set | **high** (build the pair set) + the L2a set |
| **Computation cost at gate time** | low | low | **high** — a yield over every scope-eligible pair, both sides, both combinations |
| **Behaviour when *N₂* = 0** | unsatisfiable; the criterion does not say so | unsatisfiable; the criterion does not say so | **explicit stop, in the criterion's own text** |
| **Reads as "R9 again"?** | no | **yes, at first reading** — the amendment must distinguish it | no |

---

## 7. WHAT NONE OF THE THREE SUPPLIES

Recorded so the amendment does not inherit a gap silently.

1. **The L2a expectation set itself.** All three depend on it (X2). None of them can create it;
   it is instance data, it must come from the declaration, and §5 item 4 currently declines to
   create it. **Whether a genuine L2a-detectable dependency exists on this fixture is an open
   Phase 0 evidence question and this file does not answer it.**
2. **A resolution of PREREG.md line 816 against §A.12 limb (i)** for cases other than this
   criterion. Candidate C settles it here; A and B leave it live; and it remains live everywhere
   else in the registration regardless of which is chosen.
3. **The disambiguation of "criterion 3's gates"** (X1). All three are drafted to hold both
   readings, but the amendment must *say* which it means, or the ambiguity survives into the
   replacement.
4. **What "does not carry full acceptance weight" (line 449) costs.** The branch that makes the
   replacement necessary also downgrades the fixture, and none of the three states what that
   downgrade does to the Phase 2 gate.
5. **The §10.2 numbering defect** (X7.3).
6. **Any re-reading of R22's GROUND 1 under the §10.2-criterion-3 reading of the floor.** R22's
   determination stands under both readings, but its GROUND 1 prose cites the §6.2 reading, and
   the amendment's rationale should not reproduce a citation the amendment itself disambiguates
   the other way.

---

## 8. VERIFICATION NOTE ON THE NUMBERS USED HERE

| Number | Source, with line |
|---|---|
| *N* = 11 REQUIRED; 22 OUT OF JURISDICTION; 2 UNSCORED; total 35 | AVAILABILITY_DECLARATION.md 1147, 1171, 1261–1264 |
| 984 rows = 960 declared-class cells + 24 diagnostic; 888 SCORED, 72 UNSCORED | AVAILABILITY_DECLARATION.md 1962–1965 |
| the declared 10 classes; `mbo_all_rows` is the 11th and is not one of them | AVAILABILITY_DECLARATION.md 1969, 1965–1971 |
| Phase 7 feeds no MBO columns; the six `mbo_*` classes attach to no fed column | AVAILABILITY_DECLARATION.md 1189–1192 |
| `trades_buy` is 0 strict and 0 equal in every one of its 96 cells, both sides | AVAILABILITY_DECLARATION.md 2812–2814 |
| `trades_sell` ≡ `trades_all` here | AVAILABILITY_DECLARATION.md 1164 |
| trades classes strict-positive on the contaminated side in all 48 instrument-months, and on the corrected side in the 18 | AVAILABILITY_DECLARATION.md 1154–1155; §13(b) |
| 288 and 192 fed-consumed cell counts | **derived in this file at X6** from the rows above; must be re-read from `n1\declared_map.csv` at freeze |
| *P* = 66 declared-positive (side, instrument-month) indicators; 30 declared-negative | **derived in this file at C.2** from 48 + 18 and 96 − 66 |
| ε = 72/960 = 0.075 | AVAILABILITY_DECLARATION.md 1962–1965 |
| the floor, the obligation, the incumbent unit, the grammar, proof yield, the suppression rule, the per-combination rule, the finding-rate and completion gates | PREREG.md 1035, 1033, 472, 722, 768, 791, 816, 1039, 1037, 1038 |
| §A.12's five limbs and its seven "does not permit" items | AVAILABILITY_DECLARATION.md 1548–1556, 1566–1592 |

Every other figure in this file is quoted with its line number at the point of use. No number here
was computed from an artifact this pass did not open; the two derived counts are marked as derived
and carry a re-read instruction.

---

## 9. THE CHOICE IS THE AUTHOR'S

**This file recommends none of the three.** Each is admissible under line 1035 as drafted, each
fails differently, and the differences are not reducible to a single ordering:

- **A** is the cheapest to instantiate and the only one whose threshold is tier-carrying at scale,
  and it is blind to *where* a finding occurred and couples §10.2 to §6.2 criterion 1's
  enumeration.
- **B** is the only one that tests the corrected side cell by cell — the failure the declaration's
  own §F.3 near-miss nearly produced — and it departs furthest from the registered unit, needs a
  grammar binding, carries its proof limb as an attachment, and reads as R9 at first glance.
- **C** speaks the floor's own vocabulary, prices probing coverage, and is the only one that turns
  the *N₂* = 0 case into a stated outcome; it is also the most expensive to build and to run, and
  it settles a rule collision (line 816 vs §A.12 limb (i)) that the other two leave alone.

A fourth option exists and is not developed here because K5 asked for replacement criteria: **amend
PREREG.md line 449 explicitly**, on the record, to state that documented-and-violated timing does
not trigger the ambiguity clause — R22's own stated alternative ("line 1033's obligation stands
unless line 449 is explicitly amended"). That path removes the need for a replacement criterion
entirely and pays for it with a class C amendment to the ambiguity clause itself, which must state
in terms what it is switching off.

**Whichever is chosen, three things travel with it:** the L2a expectation set (X2), the on-the-record
promotion of the *k*-of-*N* count (X4), and the disambiguation of "criterion 3's gates" (X1). None
of them is optional, and none of them is supplied by any of the three candidates on its own.
