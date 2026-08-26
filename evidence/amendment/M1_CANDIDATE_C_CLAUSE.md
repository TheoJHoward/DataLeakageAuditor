# ITEMS M1, M2, M4 — CANDIDATE C DRAFTED AS A SCHEMA CLAUSE (SC-13)

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are
untouched. **No git command was run.** The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was
not read. This file is the only file this item wrote, and it is drafted for author approval.

**Read state this pass:** `PREREG.md` = **1,099 lines**; `AVAILABILITY_DECLARATION.md` = **3,684
lines**. Both match the counts K5 and K1 read under. Every anchor below is a line number as read this
pass; if any item edits `PREREG.md` first, every anchor must be re-derived.

**Authority for this item:** **R30, confirmed by the author 13 Aug 2026** — §10.2's replacement
criterion is **candidate C**: per-detector, per-side proof yield > 0 over §7.2's registered
cohort-pair denominator, with the admissibility limb converting an empty L2a set into a stated STOP.

**Files read this pass:** `K5_REPLACEMENT_CRITERION_OPTIONS.md` (920 lines, in full);
`K1_SCHEMA_CLAUSES.md` (1,221 lines, in full); `J1_GATE_CRITICAL_CLASSIFICATION.md` §6 (lines
433–582); `PREREG_v30a_DIFF.md` (form (ii') and the H2/H3 marker shapes); `PREREG.md` §0.2.1
(72–101), §2.3–§2.8 (186–266), §3–§3.2 (270–305), §4–§4.2 (309–344), §6.2 (443–480), §7.1–§7.4
(755–837), §7.7 (849–865), §8.1–§8.3 (907–931), §10.1–§10.2 (1016–1043), §11 (1046–1055);
`AVAILABILITY_DECLARATION.md` §5 (405–484), §A.6.2–§A.6.4 (1196–1264), §A.12 (1535–1594),
§C.3–§C.4 (2780–2829). **Read, not edited.**

---

# PART 0 — THE FOUR REQUIRED PARTS, AND WHERE EACH IS NAMED IN THE CLAUSE

The brief requires all four parts to be **named explicitly in the clause text, not merely implied**.
This table is the checklist; the clause itself is at Part 2.

| Required part | Value | Named in clause limb | Named in clause as the words… |
|---|---|---|---|
| **UNIT** | proof yield per detector per side | **(c)**, headed `UNIT` | "the scoring unit is the **feature-cohort pair** §7.2 registers… the quantity computed over it is **proof yield**… computed **per runtime detector** and **per declared fixture side**" |
| **THRESHOLD** | **> 0** | **(d)**, headed `THRESHOLD` | "**strictly greater than zero** — `proof yield > 0`" |
| **DENOMINATOR** | §7.2's registered cohort-pair denominator | **(e)**, headed `DENOMINATOR` | "**the denominator §7.2 registers for proof yield**, with scope-eligibility as **§7.4** defines it. **This clause cites that denominator and does not restate it**" |
| **ADMISSIBILITY LIMB** | empty L2a set → stated STOP | **(b)**, headed `ADMISSIBILITY`, tested first | "**If any runtime detector's declared labelled-unit set is empty, this criterion is not discharged and the outcome is STOP**" |

---

# PART 1 — PLACEMENT: WHY **SC-13**, AND NOT A LIMB OF SC-12

**Recommendation: number it SC-13, a new standalone clause. Do not fold it into SC-12.** Four
reasons, each grounded in text already drafted or registered.

**1. K1's own finding F-7 forecloses folding it in.** K1 lines 1120–1124, verbatim:

> **F-7 — SC-12 REGISTERS THE FLOOR'S VOCABULARY AND DOES NOT DISCHARGE R22's LIVE OBLIGATION.**
> … SC-12 defines the word the floor uses; it supplies **none** of line 1033's three
> required parts. Still owed, and **not closable by any schema clause** because a threshold and a
> denominator are choices, not schemas

Making the replacement a sub-limb of SC-12 would put inside SC-12 exactly the three parts K1 records
SC-12 as unable to supply. That is not a tidier set; it is a clause contradicting its own finding.

**2. SC-12 is a prohibition; SC-13 is gate arithmetic. One clause may not be both.** K1 line 835,
SC-12's supersession marker, verbatim: "**It changes no threshold, exempts nothing, and grants no
permission.**" SC-13 changes a threshold — that is its entire purpose. §0.2.1 line 79, verbatim:
"**No field answers two questions.** Where a measurement concept has two independent axes, the
specification carries two fields." Applied at clause level: the prohibition and the criterion the
prohibition constrains are two axes and take two clauses.

**3. The anchors differ, and so does the supersession status.** SC-12 is a **pure insertion** after
line 1035 (K1 lines 830–835). SC-13 is a **supersession** of line 1030. A clause carrying both a
"none — pure insertion" and a "SUPERSEDED BY v30a" marker cannot state either honestly.

**4. F-7's named collision is resolved by SC-13, and needs a clause of its own to resolve it in.**
K1 lines 1127–1132, verbatim:

> **Note the interaction with SC-5(e):** SC-5(e) registers the jurisdiction boundary that puts a
> detector's findings outside this gate — and SC-12 registers that a criterion satisfiable without
> that detector has waived it. **The two clauses are consistent only because they govern different
> criteria**; if the replacement criterion is ever drafted over this gate's map, they collide, and
> the collision is resolved by the replacement, not by these clauses.

SC-13 **is** that replacement, and limb (b) is where the collision is resolved. It must therefore be
a clause SC-5(e) and SC-12 can both be cited from, not a sub-part of one of them.

**Consequence for the clause count.** K1 delivered **12** against an 8–12 target, recorded at **F-2**
(line 1068) that the set was designed at 13 before three rows were redistributed, and states in its
count table (line 1176) that "**13 is defensible**". SC-13 takes the set to **13 clauses**. That is
one over K1's stated ceiling, and it is named here rather than hidden. The alternative — compressing
SC-13 into SC-12 to hold the count at 12 — buys a number and pays with reasons 1–4 above.

### 1.1 APPLICATION ORDER, because the two anchors interact

SC-12 inserts **after line 1035**; SC-13 replaces **line 1030**. Applying SC-13 first shifts line
1035's anchor by the length of the replacement block. Applying SC-12 first leaves lines 1030–1031
untouched.

> **Apply SC-12 first, then SC-13.** Use H1's applier convention (refuse on zero or multiple anchor
> matches). No anchor-match count was verified by tooling this pass.

**Note the document-order inversion**, so a reader is not confused by it: SC-13 has the higher index
but its text lands **above** SC-12's in `PREREG.md`. The index is a clause-set identifier, not a
position.

---

# PART 2 — THE CLAUSE, DRAFTED

Convention follows K1's exactly: **REGISTERS · INSERTION POINT · SUPERSESSION MARKER · THE CLAUSE ·
DATA THE DECLARATION MUST SUPPLY · ROWS COVERED.**

---

### SC-13 — THE §10.2 REPLACEMENT CRITERION ON THE AMBIGUITY BRANCH

**REGISTERS.** The criterion that replaces §10.2 criterion 2 wherever the §6.2 ambiguity branch has
fired: its unit, its threshold, its denominator, and the admissibility test that runs before all
three. Discharges `PREREG.md` line 1033's three-part obligation, which SC-12 defines the vocabulary
of but cannot supply (K1 finding F-7).

**INSERTION POINT.** **REPLACES `PREREG.md` line 1030**, the operative sentence of §10.2 criterion 2,
preserving the enumeration's `2.` marker and the three-space indentation of the continuation block.
**Lines 1031, 1033 and 1035 stand byte-exact and are NOT superseded** — line 1031 is the branch
sentence that authorises the replacement, line 1033 is the obligation being discharged, line 1035 is
the floor the replacement is measured against. A replacement that superseded its own authorising
text would have nothing left to be authorised by.

**SUPERSESSION MARKER.** One, and it is conditional rather than absolute:

> **§10.2 criterion 2, line 1030 — v30a, SUPERSEDED ON THE AMBIGUITY BRANCH ONLY. Registered v30
> text, retained verbatim, operative where the branch has NOT fired:**
> "2. **The runtime detectors cannot separate contaminated from corrected fixture under the
> reconstructed declaration** → **stop.**"
> *Not deleted, and not superseded generally. Line 1031 already registers the disposition this
> marker performs — "this criterion is replaced, not deleted" — so where §6.2 line 449's ambiguity
> branch has not fired, the sentence above is the operative criterion and SC-13 does not apply.
> Where it has fired and been recorded, SC-13 is the operative criterion for that fixture. Recover
> the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
>
> **NOT SUPERSEDED, stated so the marker's scope cannot be widened by reading:** line 1031 (the
> branch and the before-tuning rule), line 1033 (the three-part obligation and the
> no-`DEVIATIONS.md`-only rule), line 1035 (the floor). **§6.2's four acceptance criteria are
> untouched by this clause** (see limb (h)).
>
> **Consequential — §10.1 criterion 3, line 1022.** The Phase 0 kill gate's third condition already
> carries the ambiguity branch on its face ("**or, where the fixture is semantically ambiguous
> (§6.2), under the labelled hypothetical declaration**") and is **not** amended by SC-13: §10.1
> scores a *third-party tool*, SC-13 scores *this project's* runtime detectors. Named here so the
> two are not conflated during application.

**THE CLAUSE.**

> **2. Where the fixture is semantically ambiguous, the runtime detectors must reach a non-zero
> per-side proof yield on every detector — v30a, operative on the ambiguity branch.**
>
> **(a) WHEN THIS CRITERION APPLIES, AND UNDER WHAT LABEL.** This criterion replaces the criterion
> above wherever §6.2's ambiguity branch has fired and been recorded in Phase 0, and it is evaluated
> **under the labelled hypothetical declaration that branch requires**, on the frozen default
> configuration, with the declaration's scoring key withheld from every detector. **Failure of any
> limb below is a stop.** The limbs are **conjunctive** and limb (b) is tested first.
>
> **(b) ADMISSIBILITY — tested before any detector runs, and before any other limb.** A semantically
> ambiguous fixture may discharge this criterion only if the declaration enumerates, **by name,
> before any run, and frozen with everything else the gate consumes**, a **non-empty labelled-unit
> set for each runtime detector the floor governs**. **If any runtime detector's declared
> labelled-unit set is empty, this criterion is not discharged and the outcome is STOP.** The stop
> is lifted only by supplementing the declaration with a declared, enumerated set for the empty
> detector and re-freezing under §11's integrity chain — never by scoring the criterion on the
> remaining detector, never by suppressing the empty detector's gate, and never by a
> `DEVIATIONS.md` entry or a working resolution.
>
> > **Why this limb exists, and what makes it a test rather than a formality.** A detector whose
> > declared labelled-unit set is empty **cannot change this criterion's outcome**, which is the
> > defining condition of a waiver under the floor's own definition. Four run conditions
> > produce an empty set, and each is a real state of a real fixture rather than a defect:
> > **(i)** the fixture contains no dependency of that detector's kind, so there is nothing for the
> > declaration to enumerate; **(ii)** the declaration assigns every unit of that detector's
> > character to another detector's jurisdiction and outside this gate, so no unit of that character
> > is scored here; **(iii)** the detector's required declaration is absent or its applicability
> > mode is not selected, so it returns a not-run state on every case and the declaration has no
> > model under which to enumerate units; **(iv)** every unit that could carry that detector's
> > character is declared EXCLUDED or `unscored` on a stated ground, so none survives into the
> > enumeration. **In all four the criterion is silently satisfiable by the other detector alone,
> > and this limb converts that silence into a stated outcome.**
> >
> > **A not-run state is not an empty set, and the two must not be confused.** §7.4 keeps a pair in
> > an `unsupported` or `not_applicable` case scope-eligible and in the yield denominator as a miss.
> > A detector that is declared over a non-empty labelled-unit set and then fails to run scores
> > **zero yield and fails limb (d)** — a stop for a detection reason. This limb fires only where
> > there is **nothing declared to score**, which is a stop for an admissibility reason. The two
> > stops are reported under different limbs and are never pooled.
>
> **(c) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime scoring
> unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. **The yield is
> computed per runtime detector and per declared fixture side**, and each of those figures is
> published separately. *"Per detector, per side" partitions the computation; it does not redefine
> the unit.* **This unit is a declared alternative to the descriptive fixture unit of §6.2**, adopted
> deliberately and on the record, because the pair is the unit proof yield is already registered in
> and the floor's first limb is stated in proof-yield terms.
>
> **(d) THRESHOLD.** For **each** runtime detector, on **each** declared side, the `preserving`
> combination's proof yield must be **strictly greater than zero** — `proof yield > 0`. **This is the
> floor of line 1035 taken literally and applied per detector and per side rather than once
> globally.** It is not a chosen number and it may not be tuned: there is no selection procedure to
> shape, which is what makes it committable before any development-corpus contact. **A threshold met
> by any route other than a preserving intervention reaching PROVEN under a passing determinism
> guard does not satisfy this limb.**
>
> **(e) DENOMINATOR.** The yield of limb (d) is computed over **the denominator §7.2 registers for
> proof yield**, with scope-eligibility as **§7.4** defines it, restricted to the labelled-unit set
> limb (b) requires the declaration to enumerate for that detector, and partitioned by side. **This
> clause cites that denominator and does not restate it**; a second normative statement of it here
> would leave the registration with two copies of one denominator and no canonical source. **No
> other denominator is nominated, and no re-projection, restriction, or re-aggregation of it is a
> second denominator for this criterion.**
>
> **(f) EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED.** Proof yield is registered for the
> `preserving` combination only. A criterion stated in proof-yield terms therefore scores one
> combination, and dropping the other from the criterion **waives that combination**. So: the other
> combination is **executed to a terminal result on the same denominator and publishes its own
> registered yield**, per detector and per side, and **no finding of that combination substitutes
> for a proof this criterion requires**. Its published yield is a required output of the criterion
> and carries no threshold of its own.
>
> **(g) THE REMAINING FLOOR LIMBS ARE CARRIED BY CITATION, NOT RESTATED.** Line 1035's second and
> third limbs remain in force over this criterion exactly as written there. **Where "criterion 3's
> gates" admits more than one referent, every referent is held in force** — they operate at
> different levels and do not conflict, and holding all of them is the only reading that is not a
> weakening. **This clause states no gate of its own on that limb**; it adds a threshold to the
> first limb and adds the admissibility test of (b), and it changes neither of the other two.
>
> **(h) WHAT THIS CRITERION DOES NOT REACH.** It is a kill/pause criterion over the runtime
> detectors. **It creates no acceptance criterion, amends none, and is never cited against one.**
> The descriptive fixture proof count of §6.2 remains descriptive and non-gating **for §6.2**; this
> clause makes proof yield gating **for this criterion only**, which is what line 1035's first limb
> already requires, and it promotes no other count to a gate threshold. A fixture evaluated under
> this criterion is still evaluated under the labelled hypothetical declaration and **still does not
> carry full acceptance weight** (§6.2).
>
> **(i) WHAT THIS CRITERION IS FOR, so it is not read as a quality bar.** It fires on an approach
> that is **broken**, not on one that is **incomplete**. A detector that probes few cohorts, proves
> what it probes, and publishes its coverage honestly **passes this criterion and is supposed to**;
> its limitations are reported as numbers, not converted into a stop. **Partial capability honestly
> reported is the designed outcome of this programme and is never by itself a kill condition.**

**DATA THE DECLARATION MUST SUPPLY.** Which detectors the floor governs for this fixture; the
labelled-unit set for **each** of them, enumerated by name and frozen before any run, with the
ground on which each unit is labelled; the declared fixture sides; the cohort predicate and its
regeneration procedure; the labelled-unit set's partition by side; and the record that the ambiguity
branch fired.

**ROWS COVERED: none of J1's 76.** SC-13 does not carry a scrub row. It discharges `PREREG.md`
line 1033, which J1 records as an **obligation**, not as a row — and it closes the drafting
consequence K1 records at F-7 as "not closable by any schema clause". **The 76-row accounting of K1
§2 is unchanged by this clause**; its tally (75 covered, row 28 uncoverable) stands exactly as
written.

---

## 2.1 R24 — IS IT GENERIC? THE TEST APPLIED SENTENCE BY SENTENCE

K1's test, lines 14–15, verbatim: "**The test applied to every drafted sentence: would this clause make
sense in a registration that had never seen this fixture?**"

| Limb | Names a column, count, instrument, class, or boundary? | Would it make sense on a different fixture? |
|---|---|---|
| (a) applicability and label | No | Yes — any fixture whose ambiguity branch fires |
| (b) admissibility | No — "each runtime detector the floor governs", never L2a or L3.1 by name | Yes — the empty-set condition is a property of any declaration |
| (c) unit | No — cites §7.2's registered unit | Yes — §7.2 is registered for every runtime row |
| (d) threshold | No — `> 0` is the registered floor | Yes |
| (e) denominator | No — cites §7.2/§7.4 by section | Yes |
| (f) combinations | No — "the other combination", never `promoted` as an instance | Yes |
| (g) floor limbs | No | Yes |
| (h) scope | No | Yes |
| (i) purpose | No | Yes |

**No limb names L2a, L3.1, `preserving`-as-an-instance, a column, a count, an instrument, a month, a
class, or a figure.** Every instance-bearing thing the criterion needs is listed in **DATA THE
DECLARATION MUST SUPPLY**.

**One deliberate exception, declared rather than smuggled.** Limb (d) names `preserving` and limb (f)
names "the other combination". `preserving` is **registered vocabulary** in `PREREG.md` §3.1 — a
promotion state of the specification, not a property of this fixture — so naming it is a citation of
registered vocabulary, not instance data. The asymmetric phrasing in (f) ("the other combination")
keeps the clause correct if the promotion-state set ever changes.

**Why candidate C is the only one of the three that can be written this way, and it is worth
stating.** K1's F-7 says a threshold and a denominator "are choices, not schemas". C's threshold is
`> 0` — **the registered floor itself**, so no choice is made — and C's denominator is **§7.2's own**,
so no choice is made there either. The only choice C makes is *which registered objects to point at*.
Candidates A and B both require a number (⌊N/2⌋+1, ε) and a denominator built in the declaration (the
eleven, the fed-consumed cells); neither can be written generically without leaving a blank the
declaration fills, which is precisely the instance-data leak R24 forbids. **C is the candidate whose
choice collapses onto registered objects, which is why it survives F-7's objection and the other two
do not.**

---

# PART 3 — THE LEDGER RATIONALE

Text for the amendment's v30a ledger entry. Drafted, not applied.

---

> **SC-13 — the §10.2 replacement criterion. Rationale, and the two candidates rejected.**
>
> **What a kill criterion is for.** §10.2's criteria stop the project when the *approach* is broken.
> They are not a quality bar on the tool, and the registration says so in four places that all point
> the same way:
>
> - **§10.1, line 1026:** "**Partial satisfaction is recorded and does not trigger the stop.**"
> - **§6.2, line 470:** "It gates **discrimination**. It does **not** guarantee that the tool can
>   prove leakage on real-world data — the previous gate did guarantee that, and this one
>   deliberately does not. **Proof capability is reported instead of required.**"
> - **§7.2, line 796:** "**unprobed feature-cohort rate** = fraction of labelled pairs whose affected
>   cohort was not itself probed. **A coverage statistic, independent of incidental detection.**"
> - **§8.1, line 911:** the report says "**which decision cohorts were probed and what fraction of
>   rows they cover**, and what they found."
>
> **A tool that probes few cohorts, proves what it probes, and publishes its coverage as a number is
> the tool this registration is designed to produce.** Partial coverage honestly reported is the
> design goal, not a failure mode. A kill criterion that fires on it has stopped a working project
> for being incomplete, which is the one thing a kill gate must not do. The replacement was chosen
> against that test.
>
> **Why the threshold is the floor and not more than the floor.** Line 1035 permits a stricter
> replacement. This one is not stricter on the yield limb, deliberately: `proof yield > 0` is the
> boundary between *the approach demonstrates information flow at all* and *it does not*, and every
> number above zero measures how well rather than whether. **The stricter option was available and
> was declined on the record**, because a bar above zero is a quality bar wearing a kill gate's
> clothes. Where the criterion is stricter than the floor is limb (b), which adds a stop the floor
> does not name — and that limb tests admissibility, not performance.
>
> **CANDIDATE A — attributed proof floor over the REQUIRED enumeration. CONSIDERED AND REJECTED.**
> A required a strict majority of the declaration's REQUIRED enumeration to reach PROVEN tier,
> attributed on the declared ground (⌊N/2⌋+1 — six of eleven on this fixture).
>
> > **Rejection reason, stated explicitly: a majority bar can fire on a tool that works and reports
> > its limits correctly.** A detector that proves five of eleven labelled sources, publishes
> > `k = 5 of N = 11` as §6.2 line 472 requires, publishes its unprobed-cohort rate as §7.2 line 796
> > requires, and is silent where the declaration declares silence, is a **correct** tool reporting a
> > **partial** capability. Candidate A stops the project on it. That inverts §10.1 line 1026
> > ("partial satisfaction … does not trigger the stop") and §6.2 line 470 ("proof capability is
> > reported instead of required") inside the same registration.
> >
> > **Two further reasons recorded, neither of which is the primary one.** (1) The majority rule
> > has no evidential content — it is a convention about the size of an enumeration, and a kill
> > threshold that is a convention is a threshold with nothing behind it. (2) §3.2 makes the bar
> > partly a dtype test rather than a detection test: on an integer-bearing frame "the preserving
> > set can collapse to `shuffle`" (line 305), and several of the enumeration's members are integer
> > counts by construction, so a majority-at-PROVEN bar can stop the project for a promotion reason
> > while the detector is finding everything it should. **A kill gate that fires on dtype is not
> > measuring the approach.**
>
> **CANDIDATE B — cell-sign agreement over the fed-consumed map cells. CONSIDERED AND REJECTED.**
> B required the detector's per-cell output sign to agree with the declared map's, cell by cell, on
> both sides, with a tolerance on missed cells and none on false positives.
>
> > **Rejection reason, stated explicitly: without a separate L2a limb bolted on, B waives L2a — and
> > the waiver is threefold on the declaration's own definition.** The declared map is an
> > **availability**-violation map; it says nothing about label availability. Measured against the
> > waived definition, a criterion consisting of B's agreement and proof limbs alone satisfies
> > **(i)** — the label-availability detector is excluded from the criterion's denominator; **(ii)**
> > — its findings are not required to be non-empty for a pass; and **(iii)** — the criterion is
> > satisfiable by the other detector's output alone. Line 1035 forbids a replacement that waives
> > either runtime detector, and a waived criterion "does not become admissible by being recorded,
> > disclosed, justified, or approved."
> >
> > **The bolted-on limb does not rescue it, and that is the structural point.** A conjunctive L2a
> > limb makes B admissible, but B's headline limb is tier-agnostic — the map records counts, not
> > tiers — so B cannot reach line 1035's *first* limb either without a second attachment. **A
> > candidate that needs two attachments to reach a floor its headline limb cannot reach is carrying
> > the floor rather than satisfying it.** Recorded also: B's agreement limb is the amended
> > criterion 3 generalised to both sides, and a §10.2 replacement that consists of a §6.2 criterion
> > is the wrong-object error this amendment exists to correct.
>
> **CANDIDATE C — adopted.** Its unit is the one proof yield is already registered in, so the
> criterion and the floor speak the same vocabulary and no bridging argument is needed. Its
> threshold is the floor itself, so nothing is chosen and nothing can be tuned. Its denominator is
> pre-registered, so the declaration supplies data rather than a definition. And its admissibility
> limb converts the one case the other two are silent about — a detector with nothing declared to
> score — into a stated stop rather than a silent waiver.
>
> **What C costs, recorded because the ledger is not an advertisement.** (1) The labelled-unit sets
> the criterion runs over **do not exist yet for this fixture** and must be built, enumerated and
> frozen before the tag; C is the most expensive of the three to instantiate. (2) A yield over every
> scope-eligible pair on both sides and both combinations is the most expensive of the three to
> compute at gate time. (3) C is blind to *where within a side* a finding occurred — the localisation
> failure candidate B was the only one to catch is **not** caught by this criterion, and the
> corrected side's cell-level adjudication is left to §6.2 criterion 3 as amended, where limb (g)
> holds it in force. **That gap is real and is stated rather than closed by assertion.**

---

# PART 4 — R22's FIVE OWED ITEMS, DISCHARGED ONE BY ONE

R22's owed items are quoted verbatim from `J1_GATE_CRITICAL_CLASSIFICATION.md` §6.3, lines 524–535.
For each: the owed item, the verdict, and **the clause text that discharges it**.

---

### ITEM 1 — A REPLACEMENT STATED AS SUCH

**Owed, verbatim (J1 lines 524–526):**

> 1. **A replacement for §10.2 criterion 2, stated as such** — a criterion saying what the runtime
>    detectors must achieve *in place of* separating contaminated from corrected under a
>    non-ambiguous reconstructed declaration. R9 amends §6.2 criterion 3 and is silent on §10.2.

**Verdict: DISCHARGED.**

**Discharging text.** The clause is drafted **as replacement text at §10.2's own anchor**, carrying
the enumeration's `2.` marker, with the supersession marker naming line 1030 and the ambiguity-branch
condition. Its consequence is preserved: limb (a) — "**Failure of any limb below is a stop.**" What
the detectors must achieve *in place of* separation is stated in limb (d) — "the `preserving`
combination's proof yield must be **strictly greater than zero**… **per detector and per side**".

**The wrong-object error J1 GROUND 1 identifies is avoided on its face:** SC-13 is a kill/pause
criterion over the runtime detectors, and limb (h) says so — "**It is a kill/pause criterion over the
runtime detectors. It creates no acceptance criterion, amends none, and is never cited against one.**"

---

### ITEM 2 — A UNIT FOR THE NON-ZERO-PROOF-YIELD LIMB

**Owed, verbatim (J1 lines 527–528):**

> 2. **A UNIT for the non-zero proof-yield limb** — the labelled leaking source at PROVEN tier per
>    line 472, or an explicitly declared alternative. R9 names no tier.

**Verdict: DISCHARGED — by the second route, the explicitly declared alternative.**

**Discharging text**, limb (c):

> **(c) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime scoring
> unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. … **This unit is a
> declared alternative to the descriptive fixture unit of §6.2**, adopted deliberately and on the
> record

**The registered text the limb points at**, quoted here and cited (not restated) in the clause —
`PREREG.md` **line 780**:

> | **EvidenceEvent** | `(detector, promotion_status, feature, affected output cohort)` **within a case**; corpus-level records additionally carry case identity | every combination-specific metric in §7.1 |

**Two precisions recorded, because the owed item asks for a unit and the brief names the part as
"proof yield per detector per side":**

1. **Proof yield is a quantity, not a unit.** The unit is the feature-cohort pair; proof yield is
   what is computed over it. The clause states both and says so in terms: *"'Per detector, per side'
   partitions the computation; it does not redefine the unit."* Without that sentence the criterion
   would name a metric where line 1033 asks for a unit.
2. **The alternative is declared, not slipped in.** J1 permits "an explicitly declared alternative",
   and limb (c)'s closing sentence performs the declaration. **Line 472's unit is not disturbed** —
   limb (h) keeps the descriptive `k` of `N` count descriptive and non-gating for §6.2.

**The tier the owed item says R9 omits is carried.** Proof yield is registered over **correct PROVEN
pairs**, and limb (d) closes the route in: "**A threshold met by any route other than a preserving
intervention reaching PROVEN under a passing determinism guard does not satisfy this limb.**"

---

### ITEM 3 — A THRESHOLD

**Owed, verbatim (J1 lines 529–530):**

> 3. **A THRESHOLD — a number.** None exists. §A.10's *k* of *N* = 11 is registered as a descriptive
>    non-gating count (lines 470–476) and cannot be silently promoted.

**Verdict: DISCHARGED.**

**Discharging text**, limb (d):

> **(d) THRESHOLD.** For **each** runtime detector, on **each** declared side, the `preserving`
> combination's proof yield must be **strictly greater than zero** — `proof yield > 0`.

**The number is zero, as an exclusive lower bound.** It is stated in the clause as an inequality
rather than as a bare integer because the quantity it bounds is a ratio; the criterion's pass
condition is nonetheless a single fixed number with no free parameter.

**"Cannot be silently promoted" — the promotion that C performs, and the one it does not.**

| Promotion | Performed by SC-13? | Where it is stated |
|---|---|---|
| §A.10's descriptive *k* of *N* = 11 → a gate threshold | **NO. C does not use that count at all.** | Limb (h): "The descriptive fixture proof count of §6.2 remains descriptive and non-gating **for §6.2**" |
| proof yield → a gating quantity for §10.2's replacement | **YES, and it is stated on the record** | Limb (h): "this clause makes proof yield gating **for this criterion only**, which is what line 1035's first limb already requires" |

The second promotion is not an act of registration this clause invents: line 1035's own first limb
is "**non-zero proof yield**". C makes gating the thing the floor already names. **That is the
smallest promotion any of the three candidates performs, and stating it in limb (h) is what keeps one
number from doing two jobs under two authorities.**

**Recorded honestly, and it is a real limitation rather than a flourish:** `> 0` is *at* the floor,
not above it. Line 1035 permits a stricter replacement and this one declines on the yield limb. The
ledger states the reason (Part 3); a reader who wants a stricter yield bar will not find one here.

---

### ITEM 4 — A DENOMINATOR

**Owed, verbatim (J1 lines 531–532):**

> 4. **A DENOMINATOR for the replacement**, nominated among the 11 REQUIRED columns, the 960 scored
>    map cells, or the 18-of-48 instrument-months — or a fourth, declared.

**Verdict: DISCHARGED — by the fourth route, and the fourth is the pre-registered one.**

**Discharging text**, limb (e):

> **(e) DENOMINATOR.** The yield of limb (d) is computed over **the denominator §7.2 registers for
> proof yield**, with scope-eligibility as **§7.4** defines it, restricted to the labelled-unit set
> limb (b) requires the declaration to enumerate for that detector, and partitioned by side. **This
> clause cites that denominator and does not restate it** … **No other denominator is nominated**

**§7.2's definition, quoted verbatim here with its line number as the brief requires** —
`PREREG.md` **line 791**:

> - **proof yield** = correct PROVEN pairs ÷ **all scope-eligible labelled pairs**, so a case whose guard failed — or whose only firing strategies promoted — contributes misses and stays in the denominator. **This is the headline number for the runtime rows.**

**And the scope-eligibility term it depends on** — `PREREG.md` **line 830**:

> > **scope-eligible** — the leakage risk logically applies to this unit. For a labelled feature-cohort pair this is a property of the corpus label, **not of what the detector could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss.

**Cited, not restated — and why that is not optional.** §0.2.1 **line 77** registers the rule:

> **Single normative source.** `PREREG.md` is the sole normative source for measurement semantics — units, states, denominators, gates, and what any published number means. **`DESIGN.md` may reference a rule by its section but may never restate it.** A restated rule in `DESIGN.md` is a protocol failure, not a redundancy, and the CI script fails on any measurement formula, state enumeration, or denominator definition appearing outside this file.

**One precision, stated rather than glossed.** Line 77's literal scope is `DESIGN.md` and the CI scan
it drives targets material **outside** `PREREG.md`; SC-13 is inside `PREREG.md`, so the CI scan is not
what forbids a restatement here. What forbids it is the same principle at clause level, which K1
already registers as **SC-9(f)**: "**A rule stated twice has no canonical source.** *(Citation:
§0.2.1 line 77.)*" A second normative copy of §7.2's denominator inside §10.2 would leave two
statements of one denominator with nothing ranking them — the duplicated-authority failure, not a
redundancy. **The clause therefore names the object and cites the section, and defines nothing.**

**Two costs of this denominator, recorded because a nomination without its costs is not a
nomination.** (1) The denominator keeps unprobed pairs in as misses, so a real detector's yield over
it is small by construction — which is why the threshold is the floor and not a fraction. (2) The
labelled pair set for this fixture **does not exist today**: §A.6.1 enumerates columns and §13
enumerates cells, and neither enumerates pairs. Producing it is a Phase 0 declaration task that must
complete **before** the tag, under the same freeze. **SC-13 cannot create it and does not claim to;
it is listed in DATA THE DECLARATION MUST SUPPLY.**

---

### ITEM 5 — AN L2a LIMB KEEPING L2a UNWAIVED

**Owed, verbatim (J1 lines 533–535):**

> 5. **An L2a limb that keeps L2a unwaived** under §A.12 limbs (i)–(iii), given that rows 44 and 101
>    place its findings outside this gate. Without it the replacement is inadmissible on the
>    declaration's own definition, not merely incomplete.

**Verdict: DISCHARGED — conditionally, and the condition is stated inside the criterion rather than
left implicit. See the qualification below, which is reported, not argued away.**

**Discharging text — two limbs acting together.** Limb (d) gives each detector its own positive,
per-side threshold; limb (b) makes the empty case a stated stop:

> **(d) … For **each** runtime detector, on **each** declared side, the `preserving` combination's
> proof yield must be **strictly greater than zero**
>
> **(b) … If any runtime detector's declared labelled-unit set is empty, this criterion is not
> discharged and the outcome is STOP.**

**Tested against §A.12's own five limbs** (declaration lines 1548–1556), for the label-availability
detector specifically:

| §A.12 limb | Waived? | The clause text that answers it |
|---|---|---|
| **(i)** excluded from the criterion's denominator | **No** | (e) restricts the denominator "to the labelled-unit set limb (b) requires the declaration to enumerate **for that detector**" — each detector has its own |
| **(ii)** in the denominator but findings not required non-empty | **No** | (d) "**For each runtime detector** … proof yield **> 0**" — a zero-yield detector fails the criterion |
| **(iii)** satisfiable by the other detector's output alone | **No** | (a) "The limbs are **conjunctive**"; (d) is stated per detector, so one detector's yield cannot supply another's |
| **(iv)** threshold met without executing, or by construction | **No** | (d) "**A threshold met by any route other than a preserving intervention reaching PROVEN under a passing determinism guard does not satisfy this limb.**" The limb is **positive**, not a silence test — a silence-shaped limb would be waived under (iv) |
| **(v)** reported under §7.7's `waived` coverage state | **No** | (f) "executed to a terminal result on the same denominator" |
| **limb 6 — per-combination waiving** | **No** | (f) is the limb; see the note below |

**§A.12 limb 6 is why limb (f) exists, and it is not optional decoration.** Declaration lines
1587–1589: "**Per-combination waiving is still waiving.** Line 1039 applies gates per combination;
dropping a detector from one combination's criterion while scoring it in another waives it for that
combination, and is class C." `PREREG.md` line 768: "**Proof yield exists only for the `preserving`
combination.**" A criterion stated purely in proof-yield terms therefore scores `preserving` and
**drops `promoted`** — a per-combination waiver on the declaration's own words. Limb (f) closes it.

> **REPORTED, NOT ARGUED AWAY — the qualification on item 5.**
>
> **What SC-13 discharges:** the *structural* half of item 5. No route to a waiver under limbs (i),
> (ii), (iii), (iv), (v) or limb 6 survives the clause text, and — uniquely among the three
> candidates — the residual case (a detector with nothing declared to score) is converted into a
> stated STOP instead of a silent unsatisfiability.
>
> **What SC-13 does NOT and cannot discharge:** **the labelled-unit set for the label-availability
> detector does not exist in the declaration today, and this clause cannot create it.** §5 item 4 of
> the declaration (lines 454–455) currently declines to create one — "**No separate
> label-availability criterion is created for them.** This declaration adds no new gate criterion;
> §6.2's four criteria as amended in §A are the whole gate." Until the declaration enumerates a
> non-empty set, **limb (b) fires and the criterion's outcome is STOP.** That is the clause working
> as designed, not a defect in it — but it means item 5 is discharged *as a criterion* and **still
> owed *as instance data***.
>
> **STILL OWED, stated plainly:** a declared, enumerated, non-empty labelled-unit set for the
> label-availability detector, frozen before the tag — **or**, if no such unit exists on this
> fixture, the author's decision to accept limb (b)'s STOP and act on it. **Whether a genuine
> label-availability-detectable dependency exists on this fixture is an open Phase 0 evidence
> question that this file does not answer and did not attempt to answer.**

---

### 4.1 THE FIVE ITEMS, SUMMARISED

| # | Owed | Verdict | Discharging limb | What remains |
|---|---|---|---|---|
| 1 | A replacement stated as such | **DISCHARGED** | Whole clause + supersession marker; limbs (a), (h) | — |
| 2 | A unit for the proof-yield limb | **DISCHARGED** (declared alternative) | (c), with (d)'s tier clause | — |
| 3 | A threshold | **DISCHARGED** | (d); promotion stated at (h) | The threshold is *at* the floor, not above it — declined stricture recorded |
| 4 | A denominator | **DISCHARGED** (the pre-registered one) | (e) | The labelled pair set is instance data and **does not exist yet** |
| 5 | An L2a limb keeping L2a unwaived | **DISCHARGED as a criterion; STILL OWED as instance data** | (b) + (d) + (f) | A non-empty declared labelled-unit set for the label-availability detector, **or** acceptance of limb (b)'s STOP |

**No item is closed by interpretation, and no item is argued away.** Items 4 and 5 carry live
instance-data obligations, named above; item 3 carries a declined stricture, named above.

---

### 4.2 THREE THINGS SC-13 DOES NOT SUPPLY, CARRIED FORWARD FROM K5 §7

Recorded so the amendment does not inherit a gap silently.

1. **The disambiguation of "criterion 3's gates" (K5 X1).** Limb (g) holds **every** referent in
   force, which is the stronger reading and therefore admissible under the interpretation rule — but
   the amendment's prose should still say which referent it means, or the ambiguity survives into the
   replacement.
2. **What "does not carry full acceptance weight" costs (K5 X7.1).** Limb (h) preserves the
   downgrade; it does not price it. What the downgrade does to the Phase 2 gate is unstated in the
   registration and unstated here.
3. **§10.2's numbering defect (K5 X7.3).** The printed enumeration begins at item 2; there is no item
   1. SC-13 replaces item 2 and therefore touches the defect without fixing it. **The amendment
   should either renumber or state that criterion 1 is §10.1's kill gate and is deliberately numbered
   there.** Not fixed here, because renumbering a registered enumeration is a change to registered
   text that the author has not authorised.

---

# PART 5 — M4: IS THE ADMISSIBILITY LIMB LOAD-BEARING?

**The question, restated so the test is not softened:** can a concrete run condition be named under
which a label-availability detector's declared set is legitimately empty? If not, the limb is
decorative and the choice returns to the author.

## 5.1 THE OBJECT THE LIMB TESTS — a precision that decides the analysis

**Limb (b) tests the DECLARED labelled-unit set, ex ante, not the detector's run output.** That
distinction is what makes the limb checkable before any detector runs (SC-8(c) requires exactly
that), and it separates the limb from an ordinary miss:

| State | Which limb fires | Why |
|---|---|---|
| Set declared non-empty; detector runs; finds nothing | **(d)** — yield = 0 | A stop for a **detection** reason |
| Set declared non-empty; detector `unsupported` / `not_applicable` on every case | **(d)** — yield = 0 | §7.4 line 830 keeps those pairs scope-eligible and in the denominator **as misses**; a stop for a **detection** reason |
| **Set empty — nothing declared to score** | **(b)** — STOP | A stop for an **admissibility** reason |

The clause states this distinction in its own text ("A not-run state is not an empty set, and the two
must not be confused"), which is what stops limb (b) collapsing into limb (d).

## 5.2 FOUR CONCRETE CONDITIONS, EACH GROUNDED IN REGISTERED OR DECLARED TEXT

### (i) The fixture contains no unavailable-label dependency to find

`PREREG.md` **line 340**, §4.2, the temporal mode's definition:

> **Temporal.** At cohort *d*, corrupt only label cells unavailable at *d*. Realized labels stay identical, so a feature reading a realized `y.shift(1)` is clean and one reading an unrealized label is flagged.

**The condition, concretely:** if no feature of the fixture reads a label cell that is *unavailable at
its own decision cohort* — every label-derived read being of a realized or contemporaneous value —
then there is no labelled unit of this detector's kind to enumerate. The set is empty because the
fixture is clean of this leak type, which is an ordinary and expected property of a fixture built to
exercise a *different* leak type.

### (ii) The declaration routes every unit of that character to another detector, and outside this gate

`AVAILABILITY_DECLARATION.md` **lines 1221–1224** (§A.6.2), verbatim:

> **Their label-base character is real and is assigned to L2a.** `tick_direction`, `weighted_mid`
> (and `vwap_distance`, which is REQUIRED for a different reason) sit at `mid(t)`, the base
> `fwd_move_ticks_*` measures from. **An L2a label-base finding on them is neither credited nor
> penalized by this availability gate.**

`AVAILABILITY_DECLARATION.md` **lines 2797–2798** (§C.3), verbatim:

> **That character is assigned to L2a jurisdiction and is OUTSIDE this
> availability gate.**

`AVAILABILITY_DECLARATION.md` **lines 454–455** (§5 item 4), verbatim:

> 4. **No separate label-availability criterion is created for them.** This declaration adds no
>    new gate criterion; §6.2's four criteria as amended in §A are the whole gate.

**The condition, concretely:** a declaration may assign a character to a detector's jurisdiction and
simultaneously place that jurisdiction outside the criterion's gate. The character is acknowledged as
real, and no unit of it is scored. **This is not a hypothetical — it is what the current declaration
does, at three separate sites.** K1 registers the mechanism generically as SC-5(e) ("Where a finding's
character belongs to a detector row **outside** the criteria this gate scores, the declaration assigns
it to that row and it is **neither credited nor penalized here**").

### (iii) The detector's declaration is absent, or its applicability mode is not selected

Four registered routes, each producing a state in which the declaration has no model under which to
enumerate units:

- **`PREREG.md` line 224:** "**No profile may default any term.** Supplying a label column on a temporal task without a declared label availability makes L2a — and L3.1b — `unsupported`."
- **`PREREG.md` line 233:** "`true` — or absent — makes L2a `unsupported`, naming this policy as the missing element. The tool declines to judge legitimate label use rather than guessing at it."
- **`PREREG.md` line 248:** "If the required declaration is neither supplied nor defaulted, **L3.1, L2a, and L3.1b return `unsupported`** (§8.2), naming the missing element."
- **`PREREG.md` line 344:** "Where labels are built inside the pipeline, L2a returns `unsupported` naming **L3.1 as covering detector**."

**The condition, concretely:** where the required declaration is absent, or labels are built inside
the pipeline so the covering detector takes the whole character, the declaration cannot enumerate a
labelled unit for this detector at all. **Note the care needed here:** `unsupported` *by itself* does
not empty the set — §7.4 line 830 keeps such pairs in the denominator as misses. The set is empty only
where the `unsupported` route is what prevents the units from being *declared* in the first place.

### (iv) Every unit that could carry the character is EXCLUDED or `unscored`

`AVAILABILITY_DECLARATION.md` **lines 1234–1236** (§A.6.3), the registered shape of this ground:

> A dead-zero column cannot carry a finding for a reason connected to
> availability, and leaving it in would make criterion 1 unsatisfiable for a reason unrelated to
> detection. Must be named in the gate report as **EXCLUDED**, never as MISSED.

**The condition, concretely:** where every unit that could carry the detector's character is declared
EXCLUDED (degenerate, or with an UNRESOLVED construction/lag treatment) or `unscored` on a stated
ground, the surviving labelled-unit set is empty by declared exclusion rather than by absence. K1's
SC-4(e) and SC-6 register both grounds generically.

## 5.3 THE VERDICT

> # LOAD-BEARING.
>
> **Four conditions are named concretely, each grounded in registered or declared text, and each is a
> legitimate state of a real fixture rather than a defect. None was manufactured to save the limb.**

**And more than load-bearing in the abstract — the limb FIRES ON THIS FIXTURE TODAY.** Condition (ii)
is the current declaration's actual state, at three sites quoted verbatim above (§5 item 4 lines
454–455; §A.6.2 lines 1221–1224; §C.3 lines 2797–2798). **As the declaration stands, the
label-availability detector's declared labelled-unit set is empty, so limb (b) yields STOP.**

**This is the finding, and it is reported rather than softened:**

1. **The limb is not a formality that will never fire.** It is the **binding limb of the criterion as
   of this pass**. If SC-13 were tagged today against the declaration as it stands, §10.2's
   replacement would resolve to **STOP** at limb (b), before limb (d) is reached.
2. **That is what candidate C was chosen for.** K5 §5's floor table records the alternative: under
   candidates A and B the same fixture state is "**unsatisfiable, and silent about it**"; under C it
   is "**an explicit stop, stated in the criterion**". The limb converts a silent, three-fold waiver
   into a visible outcome the author must act on.
3. **Two exits exist and both are the author's, not this file's.** Either the declaration enumerates
   a non-empty labelled-unit set for the label-availability detector before the tag — which requires
   establishing that such a dependency exists on this fixture, an open Phase 0 evidence question —
   **or** the STOP is accepted and acted on. **This file does not assert that such a unit exists**, and
   the declaration's own material points the other way: the fixture's features sit **at** the label
   base `mid(t)` (declaration lines 2793–2796), which is contemporaneous with the decision row and
   therefore **not** an unavailable-label read.
4. **A silence-shaped limb would not have worked, and the clause says so.** Requiring the detector to
   be *silent* rather than to *produce* is a threshold "met without executing" — waived under §A.12
   limb (iv). Limb (b) is an **enumeration** test and limb (d) is a **positive** test, and neither can
   be satisfied by a detector that does not execute.

## 5.4 ONE RULE COLLISION THE LIMB SETTLES, AND IT MUST BE STATED ON THE RECORD

`PREREG.md` **line 816**, verbatim:

> **A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

`AVAILABILITY_DECLARATION.md` **§A.12 limb (i)** (line 1551), verbatim:

> **(i)** it is excluded from the criterion's denominator

**These point in opposite directions for this criterion.** Line 816 would *suppress the gate* of a
combination that is `not_applicable` everywhere; §A.12 limb (i) calls a criterion from whose
denominator a detector has been removed a **waiver**. Limb (b) resolves the collision **in favour of
§A.12, for this criterion only**: an empty declared set does not get its gate suppressed — it makes
the fixture inadmissible and produces a stated STOP.

> **This is a class C change to how line 816 reads in this one place, and the amendment must say so
> in terms, or the two rules stay in conflict.** SC-13's limb (b) performs the resolution; the ledger
> entry must record it. **The collision remains live everywhere else in the registration** and is not
> settled by this clause.

---

# PART 6 — LIMITS OF THIS PASS

1. **Nothing was edited and nothing was applied.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`,
   `DESIGN.md` and `HISTORY.md` are untouched; **no git command was run**; the archive at
   `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not read. The only file written is this one, under
   the permitted scratchpad path.
2. **Insertion points are line numbers as read this pass** against the live 1,099-line `PREREG.md`.
   Lines 1030, 1031, 1033 and 1035 were read directly and are quoted verbatim above. **Apply SC-12
   before SC-13** (§1.1). No anchor-match count was verified by tooling.
3. **The clause text is drafted, not applied, and is not verified against
   `tools/check_registration.py` or `tests/registration/`.** SC-13 does not modify §7.7's line 855
   table row, so K1's F-9 risk does not attach to it; but the registration checks must still be re-run
   on a scratch copy before application, and this pass did not run them.
4. **Two limbs go beyond the confirmed core, and both are named rather than smuggled.** R30 confirms
   candidate C as *unit + threshold + denominator + admissibility limb*. Limbs **(f)** and **(g)** are
   not in that core. They are drafted in because **without them the replacement is weaker than line
   1035's floor**: (f) prevents the per-combination waiver §A.12 limb 6 defines, and (g) carries the
   floor's second and third limbs. **If the author wants the confirmed core alone, the criterion is
   inadmissible on line 1035's face** — that is a report, not an argument, and the choice is the
   author's.
5. **This file establishes no instance data.** The labelled-unit sets, the sides, and the cohort
   predicate are the declaration's to supply; whether a label-availability-detectable dependency
   exists on this fixture is an open Phase 0 evidence question that this pass did not investigate and
   does not answer.
6. **Six edits to the declaration that K1's F-8 names remain unperformed**, and SC-13 adds a seventh
   candidate: if limb (b) is adopted, the declaration's §5 item 4 ("No separate label-availability
   criterion is created") sits beside a §10.2 criterion that requires a declared label-availability
   unit set. **Whether §5 item 4 must be amended is not decided here** — it is named so it is not
   lost.
