# ITEMS N1–N5 — SC-13 CORRECTED IN ONE PASS

**This file supersedes `M1_CANDIDATE_C_CLAUSE.md` for the clause text.** The M1 file is left
untouched as the superseded record. Where this file and M1 differ, this file governs; where M1 is
not contradicted here (Part 1 placement reasoning, Part 3 candidate rejections, Part 4 items 1–4),
its text stands and is cited rather than reproduced.

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are
untouched. **No git command was run.** The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was
not read. The only file written this pass is this one.

**Read state this pass:** `PREREG.md` = **1,099 lines**; `AVAILABILITY_DECLARATION.md` = **3,684
lines**. Both match the counts K5, K1 and M1 read under. Every anchor below is a line number as read
this pass; if any item edits `PREREG.md` first, every anchor must be re-derived.

**Files read this pass:** `M1_CANDIDATE_C_CLAUSE.md` (807 lines, in full);
`K5_REPLACEMENT_CRITERION_OPTIONS.md` (920 lines, in full); `K1_SCHEMA_CLAUSES.md` (§0 lines 1–66,
SC-12 lines 824–880, findings F-6/F-7/F-8/F-9 lines 1110–1150, accounting rows 916/926–928/934/947,
count line 972); `PREREG.md` §0.2.1 (72–101), §2.3–§2.8 (186–265), §4–§4.3 (309–350), §6.2
(440–481), §7.0–§7.5 (750–843), §10.1–§10.2 (1016–1043), §11 (1046–1055), line 722;
`AVAILABILITY_DECLARATION.md` §5 (405–485), Part II §0 (599–750), §A.8 (1407–1436), §A.12
(1525–1598), §8 (1599–1656), §9 (1657–1670), §11 (1748–1781), §13(a)–(b) (1946–2005), decision log
(3645–3684); evidence artifacts `t3\day_edge_table.csv`, `t3\day_edge_samples.csv`,
`t3\measure_day_edge.py`, `errata\ERRATA_REGISTER.md` (55–84, 500–600). **Read, not edited.**

---

# PART 0 — THE TWO ROUTE DECISIONS THE BRIEF REQUIRES ME TO STATE

## 0.1 N1 — ROUTE TAKEN: **RESTORE, NOT DECLARE A STRICTURE**

**Route: the registered denominator is restored unnarrowed. No stricture is declared, because none is
needed.** The narrowing M3 found was not a necessary stricture that had been mis-stated; it was a
mis-description of what limb (b)'s set actually is.

**Why the narrowing was unnecessary.** M1's limb (e) read as though limb (b)'s enumerated set were a
filter applied *on top of* §7.2's denominator. It is not. The two partitions SC-13 needs are both
already inside the registered denominator's own terms:

- **Per detector** is `PREREG.md` **line 830**'s own scope-eligibility term, quoted verbatim:

  > > **scope-eligible** — the leakage risk logically applies to this unit. For a labelled feature-cohort pair this is a property of the corpus label, **not of what the detector could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss.

  "The leakage risk logically applies to this unit" is asked of a **risk kind**, and the risk kinds
  are the detector rows (§4's coverage map, lines 311–323). §7.2.1's formulas are already headed
  "Per `(detector, promotion_status)`" (**line 806**). A per-detector denominator is therefore the
  registered denominator read at the row whose metric is being computed — **not a narrowing of it.**

- **Per side** is §7.2's own body-of-data scope. `PREREG.md` **line 816**: "**A combination that is
  `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses
  its yields, rates, and gates**, naming the reason." Each declared fixture side is a body of data
  (§6.2 lines 460–461 name the two by name). Computing the registered metric on each declared body is
  **not a narrowing** either.

**And what limb (b)'s set actually is.** It is the declaration supplying the **corpus label** — which
pairs are labelled, and for which detector's risk kind. Line 830 makes scope-eligibility a property of
that label. So limb (b)'s set **instantiates** the registered denominator (R24: schema in `PREREG.md`,
instance data in the declaration); it does not restrict it. M1's limb (e) described an instantiation
as a restriction, and then denied the restriction was a second denominator. Both halves are corrected.

**Tested against line 1035, as the brief requires even on the restore route.** A narrowed denominator
raises a ratio and is easier to pass; line 1035 forbids "weaker". At a `> 0` threshold the direction
of the effect is smaller than that argument implies — `yield > 0` ⟺ numerator > 0, so shrinking the
denominator does not by itself flip a pass — **but that is not a defence and is not offered as one**:
a narrowing that also drops labelled pairs out of the numerator's "correct PROVEN pairs" set changes
what "correct" means, and a clause that cites a denominator it does not use is not auditable whichever
way the arithmetic runs. The corrected clause cites the denominator it uses.

**Explicitly recorded so it cannot be reintroduced by reading:** the corrected limb (e) declares **no
stricture at all**. If a future declaration finds it needs one, it is a stricture that must be
declared in terms, justified, and tested against line 1035 **in the amendment text** — never
introduced by a citation to a denominator it does not use.

## 0.2 N2 — RULING APPLIED: LIMB (g) NAMES ITS DEPENDENCY; LIMB (d) IS UNSCOPED

Applied as instructed. The dependency is named **in the clause text** (limb (g)), the adoption
consequence is stated **in the clause text** (limb (a)), and limb (d) carries an explicit
"unconditional, on every declared side" sentence so it cannot be read as scoped by an acceptance
criterion. **Consequence stated plainly at Part 3.3: SC-13 and the §6.2 criterion-3 amendment are
adopted together or not at all.**

---

# PART 1 — THE CORRECTED CLAUSE, VERBATIM

Placement is unchanged from M1 Part 1 and is not re-argued here: **SC-13, a new standalone clause,
applied after SC-12** (M1 §1.1). Convention follows K1's: **REGISTERS · INSERTION POINT ·
SUPERSESSION MARKER · THE CLAUSE · DATA THE DECLARATION MUST SUPPLY · ROWS COVERED.**

---

### SC-13 — THE §10.2 REPLACEMENT CRITERION ON THE AMBIGUITY BRANCH

**REGISTERS.** The criterion that replaces §10.2 criterion 2 wherever the §6.2 ambiguity branch has
fired: its unit, its threshold, its denominator, and the admissibility test that runs before all
three. Discharges `PREREG.md` line 1033's three-part obligation, which SC-12 defines the vocabulary
of but cannot supply (K1 finding F-7). **It has one named dependency inside this registration —
§6.2 criterion 3 as amended by this registration — and limb (g) states it.**

**INSERTION POINT.** **REPLACES `PREREG.md` line 1030**, the operative sentence of §10.2 criterion 2,
preserving the enumeration's `2.` marker and the three-space indentation of the continuation block.
**Lines 1031, 1033 and 1035 stand byte-exact and are NOT superseded** — line 1031 is the branch
sentence that authorises the replacement, line 1033 is the obligation being discharged, line 1035 is
the floor the replacement is measured against. A replacement that superseded its own authorising text
would have nothing left to be authorised by.

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
> no-`DEVIATIONS.md`-only rule), line 1035 (the floor). **§6.2's four acceptance criteria are not
> amended by this clause** (limb (h)) — SC-13 *depends on* the amendment this registration makes to
> §6.2 criterion 3 and does not make it (limb (g)).
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
> **(a) WHEN THIS CRITERION APPLIES, UNDER WHAT LABEL, AND WITH WHAT IT IS ADOPTED.** This criterion
> replaces the criterion above wherever §6.2's ambiguity branch has fired and been recorded in
> Phase 0, and it is evaluated **under the labelled hypothetical declaration that branch requires**,
> on the frozen default configuration, with the declaration's scoring key withheld from every
> detector. **Failure of any limb below is a stop.** The limbs are **conjunctive** and limb (b) is
> tested first.
> **ADOPTION.** This criterion is drafted against **§6.2 criterion 3 as amended by this
> registration** (limb (g)), and is **adopted with that amendment or not at all**: adopting this
> criterion while leaving §6.2 criterion 3 in its pre-amendment form would register a kill criterion
> whose per-side requirement can be discharged only by producing what that criterion forbids. The
> two are one adoption.
>
> **(b) ADMISSIBILITY — tested before any detector runs, and before any other limb.** A semantically
> ambiguous fixture may discharge this criterion only if the declaration enumerates, **by name,
> before any run, and frozen with everything else the gate consumes**, a **non-empty labelled-unit
> set for each runtime detector the floor governs**. **If any runtime detector's declared
> labelled-unit set is empty, this criterion is not discharged and the outcome is STOP.** The stop is
> lifted only by supplementing the declaration with a declared, enumerated set for the empty detector
> and re-freezing under §11's integrity chain — never by scoring the criterion on the remaining
> detector, never by suppressing the empty detector's gate, and never by a `DEVIATIONS.md` entry or a
> working resolution.
>
> > **WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the
> > detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination
> > rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows, and line 1039's "both
> > of L2a/L3.1's combinations". The declaration supplies each governed detector's labelled-unit set;
> > it does not supply the membership of the governed set, may not shorten it, and may not reach the
> > same effect by enumerating a set for some of them and omitting the rest. **A declaration that
> > enumerates a set for fewer than all of the governed detectors has not discharged this limb, and
> > the criterion is not discharged.**
>
> > **Why this limb exists, and what makes it a test rather than a formality.** A detector whose
> > declared labelled-unit set is empty **cannot change this criterion's outcome**, which is the
> > defining condition of a waiver under the floor's own definition. Four run conditions produce an
> > empty set, and each is a real state of a real fixture rather than a defect:
> > **(i)** the fixture contains no dependency of that detector's kind, so there is nothing for the
> > declaration to enumerate; **(ii)** the declaration assigns every unit of that detector's
> > character to another detector's jurisdiction **within this criterion's own scope**, so no unit of
> > that character is scored here; **(iii)** the detector's required declaration is absent or its
> > applicability mode is not selected, so it returns a not-run state on every case and the
> > declaration has no model under which to enumerate units; **(iv)** every unit that could carry that
> > detector's character is declared EXCLUDED or `unscored` on a stated ground, so none survives into
> > the enumeration. **In all four the criterion is silently satisfiable by the other detector alone,
> > and this limb converts that silence into a stated outcome.**
> >
> > **A not-run state is not an empty set, and the two must not be confused.** §7.4 keeps a pair in an
> > `unsupported` or `not_applicable` case scope-eligible and in the yield denominator as a miss. A
> > detector that is declared over a non-empty labelled-unit set and then fails to run scores **zero
> > yield and fails limb (d)** — a stop for a detection reason. This limb fires only where there is
> > **nothing declared to score**, which is a stop for an admissibility reason. The two stops are
> > reported under different limbs and are never pooled.
>
> **(c) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime scoring
> unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. **The yield is
> computed per runtime detector and per declared fixture side**, and each of those figures is
> published separately. *"Per detector, per side" partitions the computation; it does not redefine the
> unit, and it does not narrow the denominator — see limb (e).* **This unit is a declared alternative
> to the descriptive fixture unit of §6.2**, adopted deliberately and on the record, because the pair
> is the unit proof yield is already registered in and the floor's first limb is stated in proof-yield
> terms.
>
> **(d) THRESHOLD.** For **each** runtime detector, on **each** declared side, the `preserving`
> combination's proof yield must be **strictly greater than zero** — `proof yield > 0`. **This is the
> floor of line 1035 taken literally and applied per detector and per side rather than once
> globally.** It is not a chosen number and it may not be tuned: there is no selection procedure to
> shape, which is what makes it committable before any development-corpus contact. **A threshold met
> by any route other than a preserving intervention reaching PROVEN under a passing determinism guard
> does not satisfy this limb.**
> **This limb is unconditional on every declared side, including the side the fixture declares
> corrected.** It is not scoped, softened, or suspended by any acceptance criterion, by any
> jurisdictional routing statement, or by any per-side asymmetry in the declaration. Where an
> acceptance criterion and this limb appear to disagree about the corrected side, the disagreement is
> resolved by limb (g)'s named dependency and by nothing else.
>
> **(e) DENOMINATOR — THE REGISTERED ONE, UNNARROWED.** The yield of limb (d) is computed over **the
> denominator §7.2 registers for proof yield — all scope-eligible labelled pairs — with
> scope-eligibility as §7.4 defines it, taken unnarrowed.** **This clause cites that denominator and
> does not restate it**; a second normative statement of it here would leave the registration with two
> copies of one denominator and no canonical source.
> **This clause declares no stricture on that denominator, and performs no narrowing, restriction,
> projection, exclusion, or re-aggregation of it.** The two partitions limb (c) names are terms the
> registered denominator already carries and are not narrowings of it: **per detector** is §7.4's own
> scope-eligibility term read at the detector row whose metric is being computed — scope-eligibility
> being "a property of the corpus label, not of what the detector could do about it" — and **per
> side** is §7.2's body-of-data scope applied to each declared fixture side.
> **The labelled-unit set limb (b) requires is what INSTANTIATES this denominator, never what
> restricts it.** The declaration supplies which pairs the corpus labels and which detector's risk
> kind each is labelled for; that is the instance data the registered denominator is defined over.
> **A declaration may not use the enumeration to remove from the denominator a pair the corpus labels
> and the risk logically applies to** — that is a narrowing, it makes the criterion easier to pass,
> and line 1035 forbids a replacement weaker than the floor. **If a stricture on this denominator is
> ever genuinely necessary, it is declared in terms in the amendment text, justified, and tested
> against line 1035 — never introduced by a citation to a denominator it does not use. No other
> denominator is nominated.**
>
> **(f) EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED.** Proof yield is registered for the
> `preserving` combination only. A criterion stated in proof-yield terms therefore scores one
> combination, and dropping the other from the criterion **waives that combination**. So: the other
> combination is **executed to a terminal result on the same denominator and publishes its own
> registered yield**, per detector and per side, and **no finding of that combination substitutes for
> a proof this criterion requires**. Its published yield is a required output of the criterion and
> carries no threshold of its own.
>
> **(g) THE REMAINING FLOOR LIMBS ARE CARRIED BY CITATION, AND THIS CLAUSE NAMES WHICH VERSION IT
> CARRIES.** Line 1035's second and third limbs remain in force over this criterion exactly as written
> there. **Where "criterion 3's gates" admits more than one referent, every referent is held in force**
> — they operate at different levels and do not conflict, and holding all of them is the only reading
> that is not a weakening. **Each referent is held in the version this registration leaves standing,
> and this clause says which:**
> **(g)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**, in its
> declared-map-matching form, in which findings the declared map predicts are required, findings it
> excludes are false positives, and cells it does not cover are unscored. **It is never the
> pre-amendment prohibition on any finding on the corrected fixture**, and this clause may not be read
> against that text.
> **(g)(ii) — the §10.2 referent is §10.2 criterion 3's own two named gates**, the finding-rate gate
> and the completion gate, in force as registered and per combination, and **not amended by this
> clause**.
> **Why the version is named rather than left to the reader.** A clause whose meaning depends on
> which version of criterion 3 the reader happens to hold is the defect, not the fix: under the
> pre-amendment text limb (d)'s corrected-side requirement and criterion 3 contradict each other, and
> under the amended text they do not. **This clause states no gate of its own on this limb**; it adds
> a threshold to the first limb and adds the admissibility test of (b), and it changes neither of the
> other two.
>
> **(h) WHAT THIS CRITERION DOES NOT REACH, AND WHAT DOES NOT REACH IT.** It is a kill/pause criterion
> over the runtime detectors. **It creates no acceptance criterion, amends none, and is never cited
> against one.** The descriptive fixture proof count of §6.2 remains descriptive and non-gating **for
> §6.2**; this clause makes proof yield gating **for this criterion only**, which is what line 1035's
> first limb already requires, and it promotes no other count to a gate threshold. A fixture evaluated
> under this criterion is still evaluated under the labelled hypothetical declaration and **still does
> not carry full acceptance weight** (§6.2).
> **And in the other direction, stated because it is the collision this clause exists to resolve:** a
> declaration statement that assigns a finding's character to a detector row and places it **outside
> an acceptance gate** does not place it outside **this** criterion, and does not remove that detector
> from this criterion's denominator or from limbs (b) and (d). **A jurisdictional routing statement
> written about the acceptance gate reaches the acceptance gate and stops there.** Removing a detector
> from this criterion is a waiver, and the floor forbids it.
>
> **(i) WHAT THIS CRITERION IS FOR, so it is not read as a quality bar.** It fires on an approach that
> is **broken**, not on one that is **incomplete**. A detector that probes few cohorts, proves what it
> probes, and publishes its coverage honestly **passes this criterion and is supposed to**; its
> limitations are reported as numbers, not converted into a stop. **Partial capability honestly
> reported is the designed outcome of this programme and is never by itself a kill condition.**

**DATA THE DECLARATION MUST SUPPLY.** The labelled-unit set for **each** runtime detector the floor
governs, enumerated by name and frozen before any run, with the ground on which each unit is labelled
and the detector risk kind it is labelled for; the declared fixture sides; the cohort predicate and
its regeneration procedure; the labelled-unit set's partition by side; and the record that the
ambiguity branch fired. **The declaration does NOT supply which detectors the floor governs** — that
is pinned by limb (b) to §7.1's runtime rows and line 1039, and was removed from this block as part of
the N5(ii) correction.

**ROWS COVERED: none of J1's 76.** SC-13 does not carry a scrub row. It discharges `PREREG.md` line
1033, which J1 records as an **obligation**, not as a row — and it closes the drafting consequence K1
records at F-7 as "not closable by any schema clause". **The 76-row accounting of K1 §2 is unchanged
by this clause**; its tally (75 covered, row 28 uncoverable) stands exactly as written.

---

## 1.1 R24 RE-TESTED ON THE CHANGED LIMBS

K1's test, lines 14–15, verbatim: "**The test applied to every drafted sentence: would this clause
make sense in a registration that had never seen this fixture?**"

| Limb | Changed this pass? | Names a column, count, instrument, class, or boundary? | Would it make sense on a different fixture? |
|---|---|---|---|
| (a) applicability, label, **adoption** | **Yes** — adoption sentence added | No — names §6.2 criterion 3, a registered criterion | Yes |
| (b) admissibility, **governed set pinned** | **Yes** — pin added, condition (ii) reworded | No — cites §7.1's runtime rows and line 1039 by section and line | Yes |
| (c) unit | Minor — cross-ref to (e) | No | Yes |
| (d) threshold, **unconditional sentence** | **Yes** | No — "the side the fixture declares corrected" is a declared side, not a name | Yes |
| (e) denominator | **Yes — rewritten** | No — cites §7.2/§7.4 by section, quotes line 830's own term | Yes |
| (f) combinations | No | No | Yes |
| (g) floor limbs, **version named** | **Yes** | No — names criterion 3's amended *form*, not the map's contents | Yes |
| (h) scope, **reverse-direction sentence** | **Yes** | No — "a detector row", "an acceptance gate", never L2a or a site | Yes |
| (i) purpose | No | No | Yes |

**Two deliberate exceptions, declared rather than smuggled** (one carried from M1, one new):

1. **`preserving` in (d) and "the other combination" in (f).** `preserving` is **registered
   vocabulary** in `PREREG.md` §3.1 — a promotion state of the specification, not a property of this
   fixture. Unchanged from M1 §2.1.
2. **NEW — the governed detector set in limb (b).** The pin makes the clause depend on **§7.1 line
   759 and line 1039**, which name **L2a and L3.1**. Those are **rows of §4's registered coverage map**
   (lines 318, 320), i.e. registration vocabulary in the same sense as `preserving` — not properties of
   this fixture. Naming them by citation is therefore R24-safe. **A divergence from K1 is recorded
   with it:** SC-12's drafting note (K1 lines 837–839) says "the detector names are not hard-coded —
   the floor names 'the runtime detectors' and the declaration supplies which they are." SC-13 does
   **not** follow that choice, and the reason is N5(ii): under delegation a declaration naming only one
   detector satisfies limbs (b) and (d) with one detector, effecting §A.12 limb (iii) without amending
   SC-13. **The author should decide whether SC-12 is aligned to SC-13 or the two differ deliberately;
   this file does not change SC-12.**

---

# PART 2 — DEFECT BY DEFECT: M3's FINDING → WHAT CHANGED → THE QUOTE THAT PROVES IT

| # | M3 finding (defect in M1) | What changed in the corrected clause | The quote that proves the change was required |
|---|---|---|---|
| **1** | **Limb (e) narrowed §7.2's denominator.** M1 (e) read: "the denominator §7.2 registers for proof yield … **restricted to the labelled-unit set limb (b) requires the declaration to enumerate for that detector**", then "**No other denominator is nominated, and no re-projection, restriction, or re-aggregation of it is a second denominator for this criterion.**" A citation to a denominator the clause does not use; and a narrowed denominator raises yield, i.e. is easier to pass. | Limb (e) **rewritten**. The denominator is "**all scope-eligible labelled pairs — with scope-eligibility as §7.4 defines it, taken unnarrowed**". The word "restricted" is gone. Limb (b)'s set is re-described as what **instantiates** the denominator, with an explicit prohibition on using the enumeration to remove a labelled, scope-eligible pair. The per-detector and per-side partitions are re-grounded in line 830 and line 816 as terms the registered denominator already carries. **No stricture is declared.** | `PREREG.md` **line 791**: "**proof yield** = correct PROVEN pairs ÷ **all scope-eligible labelled pairs**…" · `PREREG.md` **line 830**: "For a labelled feature-cohort pair this is a property of the corpus label, **not of what the detector could do about it**" · `PREREG.md` **line 1035**: "The replacement may be stricter than the floor and **may not be weaker**" |
| **2** | **Limb (g) held "every referent" of criterion 3 in force without naming a version**, and one referent is registered line 461, which collides with limb (d)'s per-side yield on the corrected side. | Limb (g) **split into (g)(i) and (g)(ii)** and now names its dependency: the §6.2 referent is "**criterion 3 AS AMENDED BY THIS REGISTRATION**", never the pre-amendment prohibition; the §10.2 referent is criterion 3's own two named gates as registered. **Limb (d) gains an explicit "unconditional on every declared side, including the side the fixture declares corrected" sentence and is not scoped.** Limb (a) gains the adoption sentence. | `PREREG.md` **line 461**: "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`." · `AVAILABILITY_DECLARATION.md` **§A.8 lines 1415–1417** (R9, verbatim): "detector findings must match the declared per-side, per-class, per-instrument-month violation map; findings the map predicts are required, findings it excludes are false positives, cells the map does not cover are unscored." |
| **3** | **Limbs (f) and (g) exceed R30's author-confirmed core** (unit + threshold + denominator + admissibility limb) and M1 named them only in its "limits" section. | **Both limbs STAY, unchanged in substance.** The justification moves out of a limits list and into **the ledger** (Part 3.1 and 3.2), with line 768 and §A.12 limb 6 quoted verbatim, and with the consequence of dropping them stated: without them the criterion is inadmissible on line 1035's face. | `PREREG.md` **line 768**: "**Proof yield exists only for the `preserving` combination.**" · `AVAILABILITY_DECLARATION.md` **§A.12 limb 6, lines 1587–1589**: "**Per-combination waiving is still waiving.** Line 1039 applies gates per combination; dropping a detector from one combination's criterion while scoring it in another waives it for that combination, and is class C." |
| **4a** | **M1 Part 5.3 claimed limb (b) "FIRES ON THIS FIXTURE TODAY" on condition (ii)**, citing declaration §A.6.2 lines 1221–1224, §C.3 lines 2797–2798 and §5 lines 454–455. Those three sites are **column-scoped and character-scoped** and place the character outside "**this availability gate**" — which limb (h) says SC-13 is not. | **The claim is withdrawn from those three sites** and re-founded (Part 5.1). The limb still fires today, but **because the declaration enumerates no labelled-unit set for the label-availability detector at all**; and the *reason* it enumerates none is **condition (i)** — no dependency of that detector's kind on this fixture — **an OPEN Phase 0 evidence question this file does not answer**. Condition (ii)'s wording in the clause is also corrected: "outside this gate" → "**within this criterion's own scope**". Limb (h) gains the reverse-direction sentence that makes the doctrine explicit. | `AVAILABILITY_DECLARATION.md` **lines 1223–1224**: "**An L2a label-base finding on them is neither credited nor penalized by this availability gate.**" · **lines 2797–2798**: "**That character is assigned to L2a jurisdiction and is OUTSIDE this availability gate.**" · corrected clause limb (h): "**It creates no acceptance criterion, amends none, and is never cited against one.**" — the availability gate is §6.2's four criteria (§5 item 4, line 455: "§6.2's four criteria as amended in §A are the whole gate"), and SC-13 is not one of them. |
| **4b** | **SC-13 delegated "which detectors the floor governs" to the declaration**, so a declaration naming only one detector could satisfy limbs (b) and (d) with one detector — §A.12 limb (iii) effected without amending SC-13. | **Pinned by citation inside limb (b)**, with an explicit "a declaration that enumerates a set for fewer than all of the governed detectors has not discharged this limb". The line was **removed from DATA THE DECLARATION MUST SUPPLY**. | `PREREG.md` **line 759**: "\| **Runtime, `preserving`** \| L2a, L3.1 \| **proof yield**; conditional feature-cohort recall; cohort sensitivity; feature-cohort precision; feature discovery recall (secondary); unprobed feature-cohort rate; clean-case finding rate; completion and failure rates \|" · `PREREG.md` **line 1039**: "**Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others." · `AVAILABILITY_DECLARATION.md` **lines 1543–1544**: "**The two runtime detectors the floor governs are L2a and L3.1** (PREREG.md lines 318, 320; line 1039 names "both of L2a/L3.1's combinations")." · `AVAILABILITY_DECLARATION.md` **line 1553** (§A.12 limb (iii)): "**(iii)** the criterion can be satisfied by the other detector's output alone" |

---

# PART 3 — LEDGER ENTRIES

Text for the amendment's v30a ledger. Drafted, not applied. **M1 Part 3's rationale and the two
rejected candidates (A and B) stand unchanged and are not reproduced here.** Three entries are added
or corrected.

## 3.1 LEDGER ENTRY — WHY LIMB (f) EXCEEDS THE CONFIRMED CORE AND IS KEPT (N3)

> **SC-13 limb (f) is not in R30's confirmed core, and it is kept. The reason, on the record.**
>
> R30 confirms candidate C as **unit + threshold + denominator + admissibility limb**. Limb (f) — "every
> combination is executed, and none is dropped" — is a fifth part. It is drafted in because **without
> it the replacement is weaker than line 1035's floor**, and the two texts that make that true are
> quoted here in full rather than cited.
>
> **`PREREG.md` line 768, verbatim:**
>
> > **Proof yield exists only for the `preserving` combination.** *(→ `HISTORY.md` H-13)* The `promoted` combination publishes **evidence yield**, defined identically but over its own findings, and the two names are never used interchangeably.
>
> **`AVAILABILITY_DECLARATION.md` §A.12 limb 6, lines 1587–1589, verbatim:**
>
> > 6. **Per-combination waiving is still waiving.** Line 1039 applies gates per combination;
> >    dropping a detector from one combination's criterion while scoring it in another waives it
> >    for that combination, and is class C.
>
> **The arithmetic between the two.** A criterion stated purely in proof-yield terms scores the
> `preserving` combination and **only** the `preserving` combination, because line 768 says proof yield
> exists nowhere else. The `promoted` combination is therefore dropped from the criterion while the
> same detector is scored in the other combination — which is the exact fact pattern limb 6 defines,
> and limb 6 calls it a waiver and calls it class C. **A yield-only criterion silently waives
> `promoted` for both runtime detectors.** Limb (f) closes it by requiring the other combination to be
> executed to a terminal result on the same denominator and to publish its own registered yield.
>
> **The consequence of removing it, stated so the choice is the author's and is informed:** the
> confirmed core alone is **inadmissible on line 1035's face** — "neither runtime detector waived",
> read through §A.12's own limb 6. That is a report, not an argument.
>
> **What limb (f) does not do.** It sets no threshold on the other combination. Its published yield is
> a required output, not a gate. The criterion's pass condition remains limb (d)'s alone.

## 3.2 LEDGER ENTRY — WHY LIMB (g) EXCEEDS THE CONFIRMED CORE AND IS KEPT (N3)

> **SC-13 limb (g) is not in R30's confirmed core, and it is kept. The reason, on the record.**
>
> **`PREREG.md` line 1035, verbatim** — the floor is three limbs, not one:
>
> > The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.
>
> The confirmed core discharges the **first** limb (limb (d)) and, through limb (b) and the per-detector
> statement of limb (d), the **second**. It says nothing about the **third**. A replacement silent on
> "criterion 3's gates in force" is not a replacement that carries them; a floor limb that goes
> unmentioned is a floor limb that has been dropped, and line 1035 forbids weaker. Limb (g) carries the
> third limb by citation.
>
> **And limb (g) is where the version dependency is discharged, which is the second reason it cannot be
> dropped.** "Criterion 3's gates" admits two referents (K5 finding X1): §6.2 criterion 3 (`PREREG.md`
> line 461) and §10.2 criterion 3's two named gates (lines 1037–1038). Both are held in force — the
> stronger reading, admissible under §D.3 — and **each is held in the version this registration leaves
> standing**. Without limb (g) the clause would carry an unresolved version dependency into a locked
> registration, and the collision at Part 3.3 would be live and unstated.

## 3.3 LEDGER ENTRY — THE ADOPTION DEPENDENCY, AND WHAT IT MEANS BEFORE THE TAG (N2)

> **SC-13 and the §6.2 criterion-3 amendment are one adoption. Stated plainly, because a reader who
> holds only one of them holds a contradiction.**
>
> **The collision, in the registered text.** `PREREG.md` **line 461**, registered and today unamended:
>
> > 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.
>
> SC-13 limb (d) requires `proof yield > 0` **on each declared side**, and a correct PROVEN pair on the
> corrected side **is** a runtime finding on `fixture_corrected`. Under line 461 as registered, the only
> way to discharge SC-13 is to fail §6.2 criterion 3. **A registration cannot contain a kill criterion
> dischargeable only by failing an acceptance criterion**, and the fix is not to scope limb (d): a
> per-side yield limb that exempts one side hands that side to whichever detector is silent there, which
> is the waiver the floor forbids.
>
> **The amendment that resolves it**, `AVAILABILITY_DECLARATION.md` §A.8, quoting R9 verbatim
> (lines 1415–1417):
>
> > **NEW (quoted from R9, file tail, verbatim):** "detector findings must match the declared
> > per-side, per-class, per-instrument-month violation map; findings the map predicts are required,
> > findings it excludes are false positives, cells the map does not cover are unscored."
>
> Under that form a corrected-side finding the declared map predicts is **required**, not forbidden, and
> limb (d) and criterion 3 agree. §A.8 lines 1431–1432 keep the other direction closed: "A finding on a
> corrected-side cell the map marks zero is still a false positive and still fails the gate."
>
> **What this means BEFORE the tag, stated plainly.** The criterion-3 amendment is working resolution
> **R9**, and the decision log's own heading (line 3667) records its status: "**same provisional status,
> binding only when the v30a tag is signed**". Until the `prereg-v30a` tag is signed, **line 461 stands
> unamended and SC-13 is not adoptable on its own.** Concretely:
>
> 1. **Adopt both in one tag, or adopt neither.** SC-13 is drafted against criterion 3 as amended and
>    says so in limbs (a) and (g)(i).
> 2. **SC-13 alone is out of specification** — not because SC-13 is defective, but because its limb (d)
>    and registered line 461 cannot both be satisfied on the corrected side.
> 3. **The criterion-3 amendment alone remains admissible.** It does not depend on SC-13. The
>    dependency runs one way only, and this entry does not create a reverse one.
> 4. **A `DEVIATIONS.md` entry or a working resolution cannot substitute for the amendment** —
>    `PREREG.md` line 1033 forbids a `DEVIATIONS.md`-only criterion outright, and §A.12 limb 5 forbids
>    a working resolution from doing it.
>
> **One operational consequence, recorded because it is where the criterion will actually bite.** Under
> the amended criterion 3 the corrected side is scored against the declared map, so limb (d)'s
> corrected-side yield is discharged only where the declaration labels corrected-side pairs at all.
> Whether the declaration's corrected-side labelling supports a non-empty labelled pair set for each
> governed detector is instance data and is not settled by this clause; it is limb (b)'s question, and
> Part 4 is where this pass reports on it.

## 3.4 LEDGER ENTRY — THE LINE 816 / §A.12 LIMB (i) COLLISION (carried unchanged from M1 §5.4)

> `PREREG.md` **line 816**: "**A combination that is `not_applicable` on every scope-eligible case in a
> body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason."
> §A.12 limb **(i)** (declaration line 1551): "**(i)** it is excluded from the criterion's denominator".
>
> These point in opposite directions for this criterion. Line 816 would *suppress the gate* of a
> combination that is `not_applicable` everywhere; §A.12 limb (i) calls a criterion from whose
> denominator a detector has been removed a **waiver**. Limb (b) resolves the collision **in favour of
> §A.12, for this criterion only**: an empty declared set does not get its gate suppressed — it makes
> the fixture inadmissible and produces a stated STOP. **This is a class C change to how line 816 reads
> in this one place and the amendment must say so in terms. The collision remains live everywhere else
> in the registration and is not settled by this clause.**

---

# PART 4 — N4: THE LABELLED-UNIT SET. VERIFICATION, THE SCHEMA SIDE, AND A REPORTED FINDING

## 4.1 THE T3 FIGURES, VERIFIED AGAINST THEIR ARTIFACTS BEFORE USE

The brief requires verification before use. Performed this pass against
`evidence\fixture_spike\t3\`, read directly.

`t3\day_edge_table.csv` (5 lines: header + four horizons), columns as read:

| h | `cross_boundary_label_pairs` | `..._real_value` | `..._nan` | `worst_wallclock_span_cross` | `..._passing_mag_filter_abs_ge_2ticks` | `cross_boundary_mag_filter_pass_frac` | `overall_mag_filter_pass_frac` |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 100 | 0 | 3 days 19:30:05 | 83 | 0.83 | 0.0 |
| 10 | 200 | 200 | 0 | 3 days 19:30:10 | 166 | 0.83 | 0.001 |
| 30 | 600 | 600 | 0 | 3 days 19:30:30 | 494 | 0.823 | 0.004 |
| 60 | 1200 | 1200 | 0 | 3 days 19:31:00 | 974 | 0.812 | 0.01 |

| Declaration claim (§11 / §5) | Verified? | Against |
|---|---|---|
| 2,100 cross-boundary rows total | **YES** — 100 + 200 + 600 + 1200 = 2,100 | `day_edge_table.csv` lines 2–5 |
| "h × 20 boundaries" | **YES** — 100/5 = 200/10 = 600/30 = 1200/60 = 20 | same |
| ALL real values, zero NaN | **YES** — `real_value` = pairs, `nan` = 0 on all four rows | same |
| worst realization span 3d 19:31:00 at h=60 | **YES** | same, line 5 |
| magnitude-filter enrichment 81–83% vs a 0–1% baseline | **YES** — 0.83 / 0.83 / 0.823 / 0.812 against 0.000 / 0.001 / 0.004 / 0.010 | same |
| total frame 338,159 rows | **YES** — `total_rows` = 338159 on all four rows | same |
| MLK long-weekend samples at `day_edge_samples.csv` lines 4, 7, 10, 13 | **YES** — those four lines carry `2025-01-17 → 2025-01-21`, spans `3 days 19:30:05 / :10 / :30 / 19:31:00` | `day_edge_samples.csv` |
| same-day >60 s pairs 34 / 61 / 158 / 255, worst 30m45s | **YES** | `day_edge_table.csv`, `sameday_pairs_span_gt60s`, `worst_wallclock_span_sameday` |

**Two verification facts recorded because they qualify the use, not the numbers:**

1. **The three magnitude-filter columns are NOT produced by the archived script.**
   `t3\measure_day_edge.py` lines 82–94 build `rows_out` with **eleven** keys and no magnitude-filter
   key; the CSV carries **fourteen** columns. The enrichment figures — the sharpest part of the
   material N4 proposes to build on — are therefore **not reproducible from the archived producer**.
   They are independently recorded as measured in `evidence\errata\ERRATA_REGISTER.md` line 595
   ("The ≥2-tick magnitude filter enriches cross-boundary rows 81–83% vs 0–1%. *(execution)*") and
   tabulated at lines 566–575, so the numbers have a second home; but a re-run of the archived script
   would not reproduce them. **Recorded as a reproducibility gap in the evidence chain.**
2. **The measurement's input is named in the script and it is one side of Artifact A.**
   `t3\measure_day_edge.py` lines 9–10: `F2_OUT = HERE.parent / "f2" / "out"` /
   `PKL = F2_OUT / "contaminated_zc_2025-01_run1.pkl"`. One instrument-month (**zc 2025-01**), the
   **contaminated** build, the **f2 rebuild pair**. This is decisive for §4.3 below.

## 4.2 SCHEMA SIDE — WHERE THE REQUIREMENT LIVES IN SC-13 (deliverable (i))

**Already discharged by the corrected clause, and nothing further is added.** R24 puts the
requirement in `PREREG.md` and the set itself in the declaration. The schema-side requirement is
**limb (b)** in full, and specifically:

> A semantically ambiguous fixture may discharge this criterion only if the declaration enumerates,
> **by name, before any run, and frozen with everything else the gate consumes**, a **non-empty
> labelled-unit set for each runtime detector the floor governs**.

plus the pinned-governed-set block inside limb (b) (which detectors, not the declaration's to choose),
plus the corresponding line in **DATA THE DECLARATION MUST SUPPLY** ("the labelled-unit set for
**each** runtime detector the floor governs, enumerated by name and frozen before any run, with the
ground on which each unit is labelled and the detector risk kind it is labelled for"). The freeze is
`PREREG.md` §11's integrity chain, cited in limb (b) and not restated.

**The unit the set must be stated in is fixed by limb (c): the feature-cohort pair.** That is not
decoration — it is what §4.3's finding turns on.

## 4.3 DECLARATION SIDE — REPORTED FINDING: **THE SET CANNOT BE CONSTITUTED FROM THE T3 MATERIAL**, AND WHY

**The brief's instruction is followed literally: this is reported as a finding, not resolved by
falling back to accepting limb (b)'s STOP.** The T3 material was taken seriously, verified first
(§4.1), and carried as far as it honestly goes (§4.4). It stops short of a labelled-unit set for four
reasons. **Each is independently sufficient**; reason A is the one that cannot be worked around by
further declaration drafting.

### REASON A — THE UNIT AXIS IS MISSING. T3 SUPPLIES A COHORT AND A LABEL FACT; IT SUPPLIES NO FEATURE.

Limb (c) fixes the unit as the **feature-cohort pair**, and `PREREG.md` **line 722** closes the
grammar it must come from:

> 2. Units come from the fixed grammar: case, cohort, **feature**, feature-cohort, cluster, code-site, candidate.

A feature-cohort pair needs a **feature** that reads an unavailable label value. The detector's own
registered definition is what a labelled unit must satisfy — `PREREG.md` **line 318**:

> | **L2a** | Features from unavailable label values | PROVEN / REVIEW per §3 | Availability-restricted label perturbation | callable + label column + (temporal: `label_availability`; non-temporal: §2.5 policy) |

and **line 340** (§4.2, temporal mode):

> **Temporal.** At cohort *d*, corrupt only label cells unavailable at *d*. Realized labels stay identical, so a feature reading a realized `y.shift(1)` is clean and one reading an unrealized label is flagged.

**The T3 material establishes the cohort side and the availability side, and is silent on the feature
side.** It measures that `a(y_t)` for 2,100 rows lands in the next session, up to 3d 19:31:00 later.
It names no feature that reads `y_t`. **And the declaration's own material points the other way**: the
declared label base is `mid(t)` — the decision row's own snapshot mid (§5 line 412) — and the three
columns whose label character the declaration identifies sit **at** that base, contemporaneous with the
decision row. `AVAILABILITY_DECLARATION.md` **lines 1221–1223**:

> **Their label-base character is real and is assigned to L2a.** `tick_direction`, `weighted_mid`
> (and `vwap_distance`, which is REQUIRED for a different reason) sit at `mid(t)`, the base
> `fwd_move_ticks_*` measures from.

**A label-BASE read at `t` is not an unavailable-LABEL read.** Under L2a's own probe — corrupt the
label cells unavailable at *d* — a feature reading `mid(t)` does not move, so it is not flagged, so it
is not a labelled leaking unit for L2a. **Enumerating those three columns × the cross-boundary cohort
as "labelled" would declare a leak that has not been measured and that the declaration's own text says
is not there.** That is the one outcome worse than a STOP: a manufactured labelled set makes the
criterion look discharged while its denominator contains pairs no correct detector can prove and
every finding on which is a false positive under §6.2 criteria 2 and 3.

### REASON B — THE ARTIFACT BOUNDARY. T3 IS AN ARTIFACT **A** MEASUREMENT, AND THE REGISTERED BRIDGE TO **B** CARRIES MAP CELLS, NOT PAIRS.

`AVAILABILITY_DECLARATION.md` **line 1750** (§11's own scope line):

> > **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice.

and **§0.3's index row, line 665**, which assigns the very rows N4 proposes to use:

> | Session-tail / positional label semantics; the 2,100 cross-boundary rows | §5, §11 | **A** |

**§0.3's reading rule, lines 678–681, binding on any gate report:**

> **Reading rule, binding on this file and on any gate report.** A measurement made on Artifact A
> may be quoted as ground truth for Artifact B **only** through the lattice bridge above, and must
> name the artifact it was measured on. **A measurement claim that names neither artifact is not
> auditable and may not be published**

**And the bridge's own stated reach, §0.2 lines 653–656:**

> Artifact B's rows are rows of the same fixture-path snapshot lattice that Artifact A is built on
> (§B.2, generation `v3_pre_gapfill`), so a **per-side, per-class, per-instrument-month map cell**
> measured against that lattice indexes the same rows the stored predictions are scored over.

The bridge is stated for **map cells**. A labelled **feature-cohort pair** for a label-availability
detector is a different object class, and extending the bridge to carry it is itself an act of
registration, not a reading. **Two facts make that extension unavailable today rather than merely
undrafted:**

- **Artifact B stores no feature columns at all.** §0.2 lines 646–650: "Artifact B stores **no feature
  columns**. Its parquets carry `pred_score`, `true_label`, `fwd_move_ticks`, `mid_price_t` … **No
  event-to-row timing question can be answered from Artifact B at all.**"
- **The cohort cannot be regenerated on B either, because B's timestamp column is in dispute.** §8
  lines 1609–1611 read the schema this pass and list four columns, **not** including `timestamp`; §0.2
  line 648 records that a fifth, `timestamp`, appears only in "Y1 §1.3 item 4 … from the writer at
  `phase7_l2_sim.py` L402-408" — and §0.4 lines 719–723 establish that that writer "**produced neither
  directory**" and that there is "**no generator code for either side of Artifact B**". The
  session-boundary cohort predicate is a function of `timestamp` (`measure_day_edge.py` lines 22–23,
  60–63), so on B it is not computable from what §8 read.

### REASON C — THE ENRICHMENT IS A **PHASE 5 LINEAGE** FACT, AND ITS PRESENCE IN THE FIXTURE BUILDER IS UNSTATED

The enrichment is the part of the T3 material that carries actual leakage significance: population
membership selected on the label. Its source is `phase5_ml.py` line 679, quoted in the declaration at
**§5 lines 467–468**:

> Pre-fix `phase5_ml.py` line 679 instead applies a >=2-tick MAGNITUDE filter
> (`valid = valid[valid[ret_col].abs() >= 2.0].copy()`) to training and evaluation populations

Two things follow, and both were already on the record before this pass:

1. **K5 finding X2 point 3 records the gap in terms** — "§5's caveats record label-magnitude row
   filtering in the **phase5** lineage … whose presence or absence in the **phase7** fixture builder is
   not stated anywhere in this file." The gate scores the **phase7** pair (§8 lines 1606–1607). With no
   generator code for either side of Artifact B (§0.4), the question is not merely unanswered in the
   declaration — it is **unanswerable from the archive**.
2. **Even taken at its strongest, the object is the wrong one.** A row filter keyed on `|label| ≥ 2`
   selects a **population**; under line 722's grammar that lands on **case** or **code-site**, not on
   **feature-cohort**. It is not a unit limb (c) can score, and it is not a unit L2a's probe (corrupt
   unavailable label cells, observe a feature) produces.

### REASON D — SCOPE: ONE INSTRUMENT-MONTH, ONE SIDE, AND LIMB (d) IS PER SIDE

`measure_day_edge.py` reads `contaminated_zc_2025-01_run1.pkl` — the **contaminated** build of **one**
of the map's 48 instrument-months (§13(a) line 1967 lists the 48; **zc 2025-01 is among them**, so
scope is not fatal on the instrument-month axis). But limb (d) is per side, and **no corrected-side
counterpart of the T3 measurement exists**. §9 lines 1664–1667 supply a genuine partial bridge on this
axis and it should be recorded rather than ignored — "All 64 main-set pairs are bit-exact identical on
`true_label`, `fwd_move_ticks`, AND `mid_price_t` … one shared label vector per pair" — so a property
**of the label vector** is side-invariant on Artifact B. **That closes the side axis for a label
property and does not close it for a feature-cohort pair**, because the shared object is the label, and
§9's own caveat says so: "**A shared label vector is not a shared feature set.**"

### THE FINDING, STATED FOR THE RECORD

> **The T3 / §11 material is a real, verified, MEASURED label-availability fact about this fixture's
> lattice, and it is not a labelled-unit set for the label-availability detector.** It supplies a
> cohort and an availability measurement; it supplies no feature that reads an unavailable label, no
> Artifact B bridge for the object class, no evidence that the label-selected population survives into
> the scored artifact, and no corrected side. **Owed item 5's residue is therefore NOT discharged by
> this route, and this pass does not accept limb (b)'s STOP in its place — it reports the four reasons
> above as the finding.**
>
> **What would close it, named precisely so it is actionable rather than a shrug.** One measurement,
> on the artifact the gate scores or bridgeable to it, establishing **a named feature whose value
> changes when a label cell unavailable at its own decision cohort is corrupted** — L2a's own probe,
> run as a measurement rather than as a detector. If it exists, the labelled-unit set is (that feature
> × the cohorts in which it moves), and §4.4's cohort is already the natural cohort axis to run it
> over. If it does not exist, that is run condition (i) established as fact rather than left open, and
> limb (b)'s STOP is then the correct and stated outcome — reached by measurement, not by default.

## 4.4 WHAT **CAN** BE CONSTITUTED TODAY — DECLARATION-SIDE DRAFT, HONESTLY LABELLED

Drafted as a proposed insertion for later author application. **It is NOT a discharge of limb (b) and
says so in its own text.** It constitutes the cohort axis (fully measured, regenerable, ex ante) and
records the availability fact, so that the measurement §4.3 names has somewhere to land.

> ### 11.1 — CROSS-BOUNDARY LABEL COHORT (proposed insertion; declaration-side instance data)
>
> > **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice. **NOT bridged to Artifact B
> > by this subsection**, for the reason stated in item 5 below.
>
> **What this subsection is.** A declared, named, pre-run **cohort** and the availability measurement
> attached to it. **What it is NOT: a labelled-unit set under §10.2's replacement criterion.** That
> criterion's unit is the feature-cohort pair; this subsection supplies the cohort half and no feature.
> It is recorded so that the cohort is frozen and auditable and so that any later label-availability
> measurement has a declared population to run over.
>
> 1. **COHORT PREDICATE, declared ex ante and regenerable from the lattice alone.** For horizon *h*,
>    row *t* is **in the cross-boundary label cohort** iff the row *h* positions after *t* on the
>    filtered frame carries a different calendar UTC date. The predicate reads **only** the lattice
>    `timestamp` column, so a reviewer can regenerate it from the snapshot file alone — the same
>    property §13(d) records for the availability cohort predicate.
> 2. **MEMBERSHIP, as measured.** On the ZC 2025-01 fixture frame (338,159 lattice rows, generation
>    `v3_pre_gapfill`, sha256
>    `46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46`; 20 session boundaries):
>    **100 / 200 / 600 / 1,200** rows at
>    *h* = 5 / 10 / 30 / 60 — **2,100 rows in total**, i.e. *h* × 20 boundaries.
>    Evidence: `t3\day_edge_table.csv` lines 2–5.
> 3. **THE AVAILABILITY FACT ATTACHED TO THE COHORT.** Every member carries a **real** label value —
>    **zero NaN** on all four horizons — and its label realizes only in the next session: worst
>    realization span **3d 19:31:00** (*h* = 60, the 2025-01-17 → 2025-01-21 long weekend), median
>    overnight ~19h30m. Evidence: `t3\day_edge_table.csv` lines 2–5; `t3\day_edge_samples.csv`
>    lines 4, 7, 10, 13.
> 4. **THE ENRICHMENT, with its two caveats stated in place.** Under the ≥2-tick magnitude filter,
>    **81–83%** of cohort members survive (0.83 / 0.83 / 0.823 / 0.812) against an overall baseline of
>    **0.0–1.0%** (0.000 / 0.001 / 0.004 / 0.010). **Caveat 1:** the filter is a **phase5 lineage**
>    fact (`phase5_ml.py` line 679); **whether the phase7 fixture builder applies it is not
>    established, and cannot be established from the archive**, because no generator code for either
>    side of Artifact B exists (§0.4). **Caveat 2:** the three magnitude-filter columns of
>    `t3\day_edge_table.csv` are **not produced by the archived `t3\measure_day_edge.py`**, whose
>    `rows_out` carries eleven keys against the CSV's fourteen columns; the figures are corroborated at
>    `errata\ERRATA_REGISTER.md` lines 566–575 and 595 and are **not reproducible from the archived
>    producer**.
> 5. **WHAT THIS SUBSECTION DOES NOT DO, stated so it cannot be read as more than it is.** It declares
>    **no feature** that reads an unavailable label value, and therefore constitutes **no labelled
>    feature-cohort pair** and **no labelled-unit set** for any detector. It is measured on the
>    **contaminated** build of **one** instrument-month and has **no corrected-side counterpart**. It
>    is **not bridged to Artifact B**: §0.2's lattice bridge is stated for per-side, per-class,
>    per-instrument-month **map cells**, and Artifact B stores no feature columns and — on §8's read
>    schema — no `timestamp` column from which this cohort could be regenerated. **Being a member of
>    this cohort is, by itself, neither a licence for a finding nor a defence against one** (§5 item 3,
>    unchanged).
>
> **Interaction with §5 item 4, named rather than left to collide.** §5 item 4 states "**No separate
> label-availability criterion is created for them.**" This subsection creates **no criterion**; it
> declares a cohort and a measurement. It does not amend §5 item 4 and does not contradict it. Whether
> §5 item 4 must nevertheless be amended once SC-13's limb (b) is adopted is an open question this
> subsection does not decide (M1 Part 6 item 6; carried forward at Part 6.4 below).

---

# PART 5 — N5: THE TWO MECHANICAL CORRECTIONS IN FULL

## 5.1 (i) THE "FIRES ON THIS FIXTURE TODAY" CLAIM, RE-FOUNDED

**Withdrawn — M1 Part 5.3, the paragraph beginning "And more than load-bearing in the abstract".** It
claimed condition (ii) fires today "at three sites quoted verbatim above (§5 item 4 lines 454–455;
§A.6.2 lines 1221–1224; §C.3 lines 2797–2798)".

**Why it is wrong.** All three sites are scoped to **this availability gate**, and the availability
gate is §6.2's four criteria — §5 item 4, line 455, verbatim: "This declaration adds no new gate
criterion; **§6.2's four criteria as amended in §A are the whole gate.**" `AVAILABILITY_DECLARATION.md`
lines 1223–1224 ("neither credited nor penalized by **this availability gate**") and lines 2797–2798
("OUTSIDE **this availability gate**") both carry that same scope word, and both are stated about a
**column-level character** (`tick_direction`, `weighted_mid`, `vwap_distance`), not about a detector's
enumeration. **SC-13 is not that gate** — its own limb (h): "It creates no acceptance criterion, amends
none, and is never cited against one." A statement that a character is outside the acceptance gate
therefore says nothing about whether a unit of that character is inside SC-13's criterion; reading it
as though it did is precisely the reverse-direction error limb (h) now closes in terms.

**The corrected claim, resting on condition (i) as an open question.**

> **The limb fires on this fixture today, and the reason is that the declaration enumerates no
> labelled-unit set for the label-availability detector at all.** K5 finding X2 states the fact:
> "**the declaration as it stands enumerates no L2a-scored unit at all.** There is no L2a analogue of
> §A.6.1's eleven." That is not a jurisdictional routing consequence and is not cited as one; it is the
> absence of instance data the declaration has not yet supplied, and §5 item 4 declines to create a
> criterion that would have required it.
>
> **Whether that emptiness is permanent — i.e. whether run condition (i) holds, so that the fixture
> contains no dependency of the label-availability detector's kind at all — is an OPEN Phase 0
> evidence question. This file does not answer it and did not attempt to.** Part 4.3 reports the one
> measurement that would answer it. The declaration's own material leans toward condition (i) without
> establishing it: the fixture's label-base readers sit **at** `mid(t)` (§5 line 412; declaration lines
> 1221–1223), which is contemporaneous with the decision row and therefore not an unavailable-label
> read. **Leaning is not establishing, and this pass records the difference.**
>
> **Unchanged from M1, because M3 did not touch it:** the limb is load-bearing — four concrete run
> conditions are named, each grounded in registered or declared text (M1 §5.2, conditions (i), (iii)
> and (iv) unamended; condition (ii)'s clause wording corrected from "outside this gate" to "within
> this criterion's own scope") — and the two exits remain the author's: enumerate a non-empty set
> before the tag, or accept the STOP and act on it.

## 5.2 (ii) THE GOVERNED DETECTOR SET, PINNED BY CITATION

**The defect.** M1's **DATA THE DECLARATION MUST SUPPLY** opened with "Which detectors the floor
governs for this fixture". A declaration naming only L3.1 would then satisfy limb (b) (one non-empty
set, for the only detector it named) and limb (d) (yield > 0 for that one detector) with one detector —
**§A.12 limb (iii) effected without amending SC-13**, and without the clause ever saying a detector had
been dropped.

**The three registered sites the pin rests on, quoted as the brief requires.**

**`PREREG.md` line 759** (§7.1's metric table, first runtime row):

> | **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; conditional feature-cohort recall; cohort sensitivity; feature-cohort precision; feature discovery recall (secondary); unprobed feature-cohort rate; clean-case finding rate; completion and failure rates |

**`PREREG.md` line 1039** (§10.2 criterion 3's per-combination rule):

> - **Applied per combination** (§7.1): L1.2's static and confirmation paths, and both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently. A failure in one does not disable the others.

**`AVAILABILITY_DECLARATION.md` lines 1543–1544** (§A.12, stating the same set for this very floor):

> **The two runtime detectors the floor governs are L2a and L3.1** (PREREG.md
> lines 318, 320; line 1039 names "both of L2a/L3.1's combinations").

**The fix, as drafted into limb (b)**: the governed set is "**the detector rows §7.1's two runtime
metric rows name, and which §10.2 criterion 3's per-combination rule gates**", with the express
consequence "a declaration that enumerates a set for fewer than all of the governed detectors has not
discharged this limb, and the criterion is not discharged", and with the delegation line **deleted**
from DATA THE DECLARATION MUST SUPPLY. **The §A.12 citation is deliberately third**: §A.12 is
declaration text and provisional until the tag, so the pin's authority is the two `PREREG.md` sites and
§A.12 is corroboration, not the source. R24 clearance and the SC-12 divergence are recorded at §1.1.

---

# PART 6 — WHAT THIS PASS COULD NOT CORRECT, AND WHY

1. **Owed item 5's residue is not closed.** N4 asked for a non-empty labelled-unit set constituted from
   the T3 material. **It cannot be constituted from that material**, for the four reasons at Part 4.3 —
   the missing feature axis being the one no further drafting can supply. The permitted alternative
   (accepting the STOP) was **not** taken; the reasons are reported as a finding, and the single
   measurement that would close the question is named at the end of Part 4.3. **This is the largest
   open item leaving this pass, and it is instance data, not clause text.**
2. **The enrichment figures are not reproducible from their archived producer.**
   `t3\measure_day_edge.py` does not compute the three magnitude-filter columns present in
   `t3\day_edge_table.csv`. The numbers verify against a second record (`ERRATA_REGISTER.md` lines
   566–575, 595) and are used nowhere in the clause; **the gap is in the evidence chain and this pass
   cannot repair it — only a re-run under the archived script, amended and re-committed, can.**
3. **§10.2's numbering defect is untouched.** The printed enumeration begins at item 2; there is no item
   1. SC-13 replaces item 2 and touches the defect without fixing it. **Renumbering a registered
   enumeration is a change to registered text the author has not authorised** (carried from M1 §4.2
   item 3, unchanged).
4. **Whether declaration §5 item 4 must be amended is still undecided.** Limb (b) requires a declared
   label-availability unit set; §5 item 4 says "No separate label-availability criterion is created for
   them." Part 4.4's draft is written not to collide with it, but the question survives (carried from
   M1 Part 6 item 6).
5. **What "does not carry full acceptance weight" costs is still unpriced** (§6.2 line 449). Limb (h)
   preserves the downgrade; nothing here prices it (carried from M1 §4.2 item 2).
6. **The line 816 / §A.12 limb (i) collision is settled for this criterion only** and remains live
   everywhere else in the registration (Part 3.4).
7. **SC-12 is not aligned to SC-13's pin.** SC-12 deliberately does not hard-code the detector names
   (K1 lines 837–839); SC-13 now pins them by citation. **The two clauses treat the same set
   differently, and this file does not edit SC-12** — flagged for the author at §1.1.
8. **No tooling was run.** The clause is not verified against `tools/check_registration.py` or
   `tests/registration/`. SC-13 does not modify §7.7's line 855 table row, so K1's F-9 risk does not
   attach to it, but the registration checks must be re-run on a scratch copy before application.
   **Apply SC-12 before SC-13** (M1 §1.1); no anchor-match count was verified by tooling.
9. **Insertion points are line numbers as read this pass** against the live 1,099-line `PREREG.md`.
   Lines 461, 722, 759, 768, 791, 816, 830, 1030, 1031, 1033, 1035 and 1039 were read directly and are
   quoted verbatim above.
