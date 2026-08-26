# J3 — C1 REDRAFTED, and the rule it is built on

**DELTA R42/J3. The previous C1 is WITHDRAWN, not amended.** This is a fresh draft against
the four requirements J3 sets, and it is unapplied: `PREREG.md` remains byte-identical to
the `prereg-v30` tag.

---

## 1. Why the previous draft was withdrawn

Registered `PREREG.md` line 992, Phase 1 gate cell, the clause at issue:

> …claims verified or a deviation filed with the measurement; **both fixture AUCs reproduce
> within ±0.010, full and sliced**; all four alignment-control cases behave as §6.5 requires;
> snapshots hashed

My withdrawn draft replaced that with *"every declared reference-anchor entry reproduces
within its registered acceptance interval, recomputed from the fixture's committed bytes"*.

**Four defects, all verified in the adversarial pass, and the first is fatal on its own.**

**(a) It converted a failable test into one already known to pass.** The registered target
is two literals of *external* origin — `0.957` and `0.675`, from the prior experiment's
record — and the fixture **demonstrably fails** them: `AVAILABILITY_DECLARATION.md` §A.1,
*"There is no horizon at which the registered pair is reproduced."* My replacement asks
whether a recomputation of committed bytes equals a recomputation of the same committed
bytes. H2 says so in terms: *"a pure function of bytes already committed, so no rerun,
reseeding, or environment change can move it."* Expected deviation is 0.000000, not
"within ±0.010". A gate row whose outcome is certain before the phase opens is not a gate
row.

**(b) WITHDRAWN at R49 — this ground does not survive R48/Q4.** This paragraph read: *"The one
substantive discrepancy became a disclosure duty. The anchor's model family changed — XGBoost →
LightGBM (§A.1 item 2)."* **§A.1 item 2 was corrected on 21 August 2026 and now says the opposite**:
the cited source names six architectures with LightGBM listed first, and **no family changed**. The
paragraph cited the very item that withdraws it. R48/Q4 required both dependents of that claim to be
re-grounded; H2's justification and the failure-mode table were, and **these two sites were missed
until the R49/R6 verification found them.** The withdrawal costs the C1 case nothing: defects (a),
(c) and (d) are independent and (a) is fatal on its own.

**(c) The sliced numeric target vanished with nothing numeric replacing it.** Registered:
±0.010 applied *"full and sliced"*. Mine: *"produced … CI obligation is discharged, with its
slice boundaries declared"* — three acts of production and declaration, no quantity. And
SC-2(d)'s entries are *"one per declared horizon and side"*, so full/sliced is not an entry
axis and the sliced variant never enters the first limb either.

**(d) The separation floor was silently dropped.** Requiring *both* 0.957 and 0.675 to
±0.010 entailed a pre/post gap of **0.282 ± 0.020** — the registered cell tested, at Phase 1,
that the fixture still exhibits a large leak signal. The declared trio's deltas are **0.0347,
0.1835, 0.1771**, every one below the registered gap, and no clause requires a minimum. The
project's own Phase 0 record concludes both fixture sides are availability-contaminated —
exactly the state a collapsed gap signals. The registered cell would have tripped on it; my
replacement could not.

---

## 2. The rule J3 asks to be registered

Drafted as a limb of SC-8, whose subject is the freeze and what a frozen object must be:

> **(g) EVERY GATE ITEM STATES WHAT MAKES IT FAIL — AND AN ITEM THAT CANNOT FAIL IS ONE OF
> TWO THINGS, ONLY ONE OF WHICH IS A DEFECT.** Every gate item states, in its own text or in
> the clause it cites, **the condition under which it fails** — an observation that is
> possible, that the artifact under test could produce, and that would deny the gate.
>
> **(g)(1) REGRESSION GUARD — legitimate, and LABELLED.** An item that cannot fail *given
> correct behaviour of a frozen artifact*, but that **would** fail on corruption,
> substitution, or drift in what it reads, is a **regression guard**. It is legitimate and it
> is kept. It is **labelled a regression guard where it is written**, and it **states what it
> guards against** — the specific change in the world that would trip it. It is **not counted
> as evidence that the phase's gate was met.**
>
> **(g)(2) DECORATION — removed.** An item that cannot fail under **any** state of the world
> — because both sides of its comparison are the same bytes, or because its condition is a
> tautology — is decoration. It is **removed**, not labelled.
>
> **(g)(3) A ROW CARRYING GUARDS NAMES WHERE ITS PASS/FAIL EVIDENCE COMES FROM.** Where a gate
> row contains regression guards, the row **names the items that carry its pass/fail evidence**
> — those whose outcome is not determined before the phase opens. Without that sentence a
> reader concludes the row is empty.
>
> Where an item's failure condition is a comparison, the quantity compared against is **named
> and its origin stated** — a target derived from the same bytes the item tests is an
> integrity check, not an agreement check, and the two may not be substituted for one another.
> **A registered item the artifact currently fails may not be replaced by one it passes, in
> the same amendment, without the replacement stating what the artifact must now do to fail
> it.**

**Why (g)(1) and (g)(2) are separated — refined at R49/R2, on H-L13's ground.** The first draft
of this limb said only *"an item whose outcome is determined by the frozen artifact before the phase
opens is not a gate item"*. Applied literally that deletes the anchor's **substitution detector**
along with the tautology, and the two are not the same object: one cannot fail while the artifact is
correct, the other cannot fail at all. **Deleting a regression guard removes a real detector of a
swapped or corrupted fixture; keeping decoration inflates a row with weight it does not carry.**
Both directions are defects, which is why the limb now names both and disposes of them differently.
This is the same shape as H-L13's refinement: a rule written against one failure mode reached
something it should not have.


**Why the last sentence.** That is exactly the move the withdrawn C1 made, and no clause
forbade it. §0.2.1 line 97 forbids an amendment weaker than what it amends, but "weaker" was
being read as a property of the *text*, not of the *outcome*. This states the outcome test.

---

## 3. The redraft

**INSERTION POINT.** `PREREG.md` line 992, the Phase 1 row of §10's phase table. **Only the
Gate cell changes**; Phase, Work and Est. are byte-identical. The C1 retention block written
after the phase table (K2 §9.1, hunk at line 998) retains the registered row verbatim.

**OPERATIVE v30a TEXT at line 992** *(Gate cell only)*:

> §10.0 ordering followed; claims verified or a deviation filed with the measurement;
> **the reference anchor holds on both limbs**: *(i)* **AGREEMENT — this limb CANNOT FAIL while
> the fixture is unchanged, and FAILS on substitution, regeneration or corruption of it, which
> would move the recomputed entry off the figure the originating experiment recorded. It is
> therefore NOT evidence that this gate was met, and remains capable of failing it.** Each
> declared reference-anchor entry is compared against that figure **for the same
> `(side, instrument, architecture, horizon_s, tier)`** — the key stated in full because it is
> **the join key across two artifacts, neither of which carries all five fields**: the
> originating record is keyed `(instrument, architecture, horizon_s, tier)` and is one-to-one on
> those four, while `side` selects which declared entry is being compared and is not a column
> of it. `(horizon, side)` alone selects 16 rows spanning 0.5420–0.9662, **42× the tolerance
> below**, and dropping `tier` leaves three rows per combination whose 30s values are
> 0.8299 / 0.8564 / 0.8666 — **two of the three fail ±0.010 against the declared entry, so the
> key decides the outcome.** `tier` is the declared **L2**;
> `side` selects the declared entry and is not a column of the originating record. Any entry
> that does not reproduce its figure within ±0.010 absolute **fails this gate row**. An entry
> whose originating figure is **unavailable** fails this gate row **unless the declaration
> registered that entry ex ante as having no originating counterpart and stated why** — a
> ground declared before any Phase 1 measurement, never after one; *(ii)* **INTEGRITY — likewise
> incapable of failing on an unchanged fixture, and failing on byte corruption of the committed
> fixture or a changed AUC routine; likewise not evidence that this gate was met** — each entry
> is recomputed from the fixture's committed bytes and must equal its
> declared value exactly, a deviation of any size being a defect in the recomputation and a
> stop-and-report;
> **the declared pre-fix/post-fix separation is stated per horizon and side as a PUBLISHED
> CONTEXT FIGURE, carrying no pass/fail consequence** (R49/R1);
> **the sliced variant's Phase 1 CI obligation is discharged and the variant is scored under
> §6.2 (v30a) "Sliced variant — operative"**, whose ex-ante scoring rule governs it, with its
> slice boundaries declared;
> **all four alignment-control cases behave as §6.5 requires**; snapshots hashed
>
> **WHAT SHOWS THIS ROW WAS MET** is the sliced variant, the four alignment-control cases, the
> snapshot hashing, and the §10.0 ordering and claims-verified clauses. **Limbs (i) and (ii)
> cannot show it was met — neither can fail on an unchanged fixture — but either can still fail
> it, and a failure of either denies the row.**

---

## 4. THE FAILURE MODE, stated as J3 requires

**What the fixture would have to do to fail this row.** Five distinct, observable ways —
each a thing the artifact can actually exhibit, not a hypothetical:

| # | Failure | Is it live on this fixture? |
|---|---|---|
| 1 | **An anchor entry does not reproduce the originating experiment's figure to ±0.010.** | **NO — NOT LIVE, and this corrects R47/P7.** The originating record is **Phase 6** (`phase6_main_summary.csv`, ZC/LightGBM/L2): 0.9662 / 0.9400 / 0.8564. The declared pre-fix trio reproduces it to **|Δ| ≤ 4.4e-5**, far inside ±0.010. §A.1's *"no horizon at which the registered pair is reproduced"* is about the **retired** 0.957/0.675 pair, which H2 retires and which is **not this limb's comparand**. The post-fix trio takes the no-counterpart branch on §A.1 item 4's ex-ante ground (R48/Q7). **Both operands are frozen, so this limb cannot fail on this artifact — it is a REGRESSION TEST and is labelled one.** It detects a swapped or corrupted fixture, which is worth having; it is not gate weight. |
| 2 | **A recomputed entry does not equal its declared value.** | **Also a regression test.** Expected deviation 0.000000 and any non-zero is a stop-and-report. Detects byte corruption, a changed AUC routine, a mis-transcribed declaration — none of which the frozen artifact can produce by itself. Labelled under SC-8(g), not counted as gate weight. |
| 3 | ~~A declared horizon's pre/post separation falls below the registered floor.~~ | **WITHDRAWN at R49/R1 — no floor is registered.** Separation is published as a context figure with no pass/fail consequence. Declared deltas remain **0.034708 / 0.183464 / 0.177131**, published, against the registered pair's implied **0.282**. |
| 4 | **The sliced variant fails the ex-ante scoring rule §6.2 (v30a) "Sliced variant — operative" registers for it** — not a ±0.010 comparison, which that clause does not create *(corrected R60/F3-B4)*. | Possible once the slicer exists — the padded slicer is Phase 1 work, and a slicing defect shows here as a numeric miss rather than as a missing artifact. |
| 5 | **An alignment-control case misbehaves, or a snapshot is unhashed.** | Carried unchanged from the registered row. |

**WHAT ACTUALLY CARRIES GATE WEIGHT, after R48.** Failure modes 1 and 2 are **regression tests**:
both operands are frozen, so neither can fail on this artifact, and SC-8(g) requires them to be
labelled rather than counted — *"an item whose outcome is determined by the frozen artifact before
the phase opens is not a gate item; it is a regression test, and it is labelled as one where it is
written."* **This draft now labels them.**

**The row remains failable, on other limbs**, and this is where its weight actually sits:

- **the separation floor (failure 3)** — failable the moment a floor is registered, and **live**:
  declared deltas 0.034708 / 0.183464 / 0.177131. **The floor is P6 and is the author's; it is not
  set here.**
- **the sliced variant (failure 4)** — genuinely open, because the padded slicer is Phase 1 work
  that does not yet exist. This is the limb most likely to fail on its merits.
- **the alignment controls and snapshot hashing (failure 5)**, and the §10.0 ordering and
  claims-verified clauses that open the row.

**Stated plainly for the author:** if the separation floor is declared a context figure with no
pass/fail consequence (P6's recommendation), then of this row's *anchor* content **nothing is
failable on a frozen artifact** — the anchor becomes a regression suite and the row's live weight
is the sliced variant, the alignment controls and the ordering clauses. That may well be the right
design; it should be chosen knowingly rather than arrived at.

---

## 5. Author decisions this draft surfaces, and does not take

**(a) The separation floor: RULED at DELTA R49/R1. There is no floor.** Separation is published as
a **context figure per horizon and side, carrying no pass/fail consequence.**

**The reasoning, recorded because the ruling is a reduction and a reader is entitled to it.** The
AUC gap is a property of the **FIXTURE**, not of the tool under test; the amended gate scores a
detector's **findings against the declared map**, so a separation floor imports a v30-era instrument
into a v30a-era gate and measures the wrong object. And the number could not be set honestly: any
value other than **0.282** would be chosen from the distribution this fixture already exhibits,
which §7.0 forbids — while 0.282, the separation the registered pair implied, **the fixture fails at
all three horizons** (0.034708 / 0.183464 / 0.177131), so registering it would mean the gate cannot
pass. A floor that can only be set by looking at the data is not set.

**DISCLOSED, because this is a reduction and R47/P2's rule cuts both ways.** The registered v30 row
required *both* 0.957 and 0.675 to ±0.010, which **entailed** a pre/post gap of 0.282 ± 0.020. That
entailment was the registered row's only separation test, and **this amendment removes it and
replaces it with a published figure that decides nothing.** It is recorded here, in the ledger, and
in the clause — the same treatment R47/P2 required of the contaminated-side tightening, in the
opposite direction. A reduction whose reason appears nowhere is the failure mode; a reduction the
author rules on the record is a decision.

**(b) Limb (i) hard-fails. SETTLED by the author at DELTA R47/P7; no longer an open decision.**
The draft above recorded a deviation instead of failing. That was the one place this redraft was
deliberately weaker than a maximal reading, and it does not survive its own rule: **SC-8(g)
requires a gate item to state the condition under which it FAILS, and an item that only records a
deviation states no such condition.** A limb that cannot fail is not a limb.

**The consequence, stated plainly because the author is entitled to it before signing.**
*(Corrected R60/F3-B6. This paragraph previously read that "the Phase 1 gate row fails as things
stand", which contradicted this document's own failure-mode table three sections above. The table
is right and this was stale.)* Limb (i) compares each entry against **the originating experiment's
figure for its own key** — Phase 6 — **not** against the retired 0.957/0.675 pair. Against Phase 6
the pre-fix trio agrees to **|Δ| ≤ 4.4e-5**, and the post-fix trio takes the no-counterpart branch
on the declaration's ex-ante ground. **The row does not fail on today's artifact.** What follows
from the hard fail is narrower and still real: an entry that later drifts off its originating
figure, or a post-fix entry whose ex-ante ground is not registered, denies the row.

**Interaction with P8, which is not yet settled.** If P8 finds the originating record is not keyed
per horizon and side, then the *unavailable* branch — not the comparison — governs every entry,
and under the hard fail the row fails for a record-keeping reason rather than anything about the
tool. **A limb whose exception branch governs every case is mis-drafted**, and limb (i) would need
re-scoping before adoption. Flagged because P7 and P8 interact: adopting P7 before P8 answers is
adopting a limb whose behaviour is unknown.

**(c) Where the originating figure comes from — SETTLED at R48/Q5 and Q7; no longer open.** The
originating record is **Phase 6**: `results\pc2_all_phases\phase6\second_pc\phase6_main_summary.csv`,
keyed (`instrument`, `architecture`, `horizon_s`, `tier`), 96 rows, four instruments (NQ, GC, ZC, ZS),
both families. ZC / LightGBM / L2 gives **0.9662 / 0.9400 / 0.8564** at 5s / 10s / 30s.

**3 of 6 declared entries have a counterpart.** The three post-fix entries have none and none can
exist — the universal-lag correction that defines that side was first applied in Phase 7 itself.
Registered **ex ante** at declaration §A.1 item 4 (R48/Q7), so the no-counterpart branch is
exercised deliberately, on a stated ground, rather than by accident.

**Transcription refuted (R48/Q5).** Phase 7 re-derived: it trains its own models, reads no Phase 6
output, and Phase 6 stored no predictions to copy. The 32 byte-identical `shuffle_mean` values are
the expected output of **fixed seeds [42, 123, 456]**, not evidence of copying. **Not established:**
no Phase 6 script survives, so whether the agreement is deterministic identity or independent
convergence cannot be settled from the artifacts — which is one more reason limb (i) is labelled a
regression test rather than an agreement gate.

---

## 6. Status

**DRAFTED, UNAPPLIED, UNVERIFIED BY ANY PARTY THAT DID NOT DRAFT IT.** *(R47/P7 applied:
limb (i) hard-fails. R47/P8 pending: whether every declared entry has an originating
counterpart — see §5(b).)* Per R46/N5's standard
for new normative text — and this is new normative text in a phase gate — it requires
independent verification by an agent that did not draft it, then a composed read of §10 as
amended, before it is fit to sign. It has had neither.
