# R49 addendum T1–T4 — verification result, and what I verified first-hand

**Workflow `wlhf11296`, 21 August 2026. Nine agents: two cold verifiers who saw no prior version
(T3), one closure verifier holding the seven blockers (T2), a composed read (T4), four refuters, a
synthesis.** Everything marked VERIFIED below I re-ran myself against the artifacts rather than
accepting from the report.

---

## 1. T4 — CAN THE GATE BE PASSED CHEAPLY BY A USELESS DETECTOR?

**NO.** The cheapest route is defeated at criterion 3 on three independent registered grounds:
SC-5(b)'s three-part conjunction (a REQUIRED entry is satisfied only by a finding *"on the side, in
the cells, and on the ground the map declares"*), the per-side run obligation, and SC-11(e)
(*"AN UNEXPECTED ALL-ZERO IS A FINDING, NOT A PASS"*).

**But the NO is thinner than it looks, and three qualifications belong on the record:**

1. **SC-4(k) is not what stops it.** (k1) says so of itself. The limb is aimed at a different
   failure and touches this one nowhere.
2. **Criterion 1's answer key is inside the detector's granted input surface** — see §2, the
   headline finding of this pass.
3. **The cell projection's content is unconstrained** — no clause fixes which map class governs
   which fed column. On this fixture the choice is immaterial (the three `trades_*` positive sets
   are identical); that is a fact about this fixture, not a property of the rule.

---

## 2. THE HEADLINE: CRITERION 1's ANSWER KEY IS INSIDE THE GRANTED INPUT SURFACE

**VERIFIED FIRST-HAND, and it is independent of everything else in this round.**

SC-1(c) *compels* the declaration to mark where a column role is an approximation. SC-7(a)
*affirmatively grants* the detector "§4 + T2 `column_roles`". Those annotations are the answer key:

```
approximation-annotated columns : 13   (12 of them fed; trade_count_10s is not fed)
REQUIRED list                   : 11
REQUIRED *not* annotated        : NONE
annotated but not REQUIRED      : buy_volume_10s  — and it is UNSCORED, so firing on it is FREE
=> a detector that fires on every annotated fed column scores criterion 1 at 11/11
```

**That is retrieval, not discrimination** — and it is SC-7(c)'s own stated reasoning
(*"graded against a key it had seen"*), applied to an object SC-7(b) does not withhold, because
SC-7(b) withholds only what is *derived from the map* and the role annotation is not.

**The gate survives because criterion 3's key is withheld, not because criterion 1's is.**

**This is an author decision, not a drafting fix.** Closing it means either narrowing SC-7(a)'s
grant or weakening SC-1(c)'s disclosure duty, and the two pull against each other. Nothing has been
changed.

---

## 3. THE SEVEN BLOCKERS — CLOSURE NOT CONFIRMED

| # | status | what actually decides it |
|---|---|---|
| **B1** | **NOT CLOSED — MOVED** | The citations are gone (verified: zero `SC-8(g)` in applied text). **But the shipping row still uses the CATEGORY** — "A REGRESSION GUARD, AND LABELLED ONE", "ALSO A REGRESSION GUARD" — and no registered rule creates it: neither "regression guard" nor "regression test" occurs anywhere in the applied set. **And registering SC-8(g) verbatim would not fix it:** (g)(1) is drafted ASYMMETRICALLY (*"not counted as evidence that the phase's gate was **met**"*) while the row states it SYMMETRICALLY (*"not counted toward the **pass/fail** evidence"*). Both cold verifiers missed this; the refuter caught it. |
| **B2** | **NOT CLOSED — my fix is theatre. VERIFIED BY MUTATION.** | Check (viii) probes five 110-char windows, first hit wins, **21.1% coverage of 2,612 chars**. I mutated H29 five ways and re-ran the binding: tolerance `±0.010`→`±0.100`, deleting the fails-this-gate-row sentence, dropping `tier`, **flipping "fails this gate row" → "is recorded as a deviation"**, and deleting the pass/fail-evidence sentence. **All five still BIND and PASS.** The check reports green on the exact reduction it was written to catch — and the flip is the precise defect R47/P7 exists to eliminate. |
| **B3** | **PARTLY CLOSED** | `tier` is in the key. Two defects remain: *"the only one that is one-to-one"* is **false** (the four-field key over `phase6_main_summary.csv` is already one-to-one), and the five-tuple is a key of **neither** artifact — Phase 6 has no `side`; `f1_results.csv` has no `tier` and calls the field `model`, not `architecture`. |
| **B4** | **CLOSED in the row — MOVED into J3** | The limb defers to a clause that exists. But J3's failure-mode table still states mode 4 as *"misses its declared entry by more than ±0.010"* — a test the deferred-to clause does not create. |
| **B5** | **PARTLY CLOSED** | (k2) now adds two conditions and **neither is met**: the freeze's "specifically and exhaustively" list of seven objects does not include the manifest, and it still reads `"manifest_status": "DRAFT - author review required"`. (k4) indexes neither breach. |
| **B6** | **NOT CLOSED — MOVED** | The operative row is clean, but **J3 §5(b) still says *"the Phase 1 gate row fails as things stand"*** while the failure table three sections earlier says *"NO — NOT LIVE"*. I corrected the table and left the prose. J3 also tells the author three different things about R47/P8's status. |
| **B7** | **CLOSED for SC-3(a); the CLASS is not closed** | One normative site now, verified over five documents. But the line-451 sliced-variant clause is a larger copy of the same shape, ten registered lines from its source. |

---

## 4. THREE PLACES MY ACCOUNT DOES NOT MATCH THE TEXT

**(a) VERIFIED — the model-family claim is struck from NEITHER operative site.** `X5:486`, inside
the block headed *"Operative text — what this hunk actually puts into `PREREG.md`"*, still reads
*"because the anchor's model family changed"*. It stands identically at `_E3_composed_sections.md`
and `PREREG_v30a_DIFF.md`. **Three lines below it, `X5:489` — my own commentary — asserts the claim
*"is struck from both."*** The correction landed on the commentary and not on the text, and then
claimed otherwise. **This is the third occurrence of one family in three rounds**: §A.1 item 2's
false citation, the SC-8(g) phantom citation, and now a false claim of correction.

**(b) SC-4(k)'s 68 lines are an unlisted difference under a completeness claim.** PART 5 is headed
*"EVERY DIFFERENCE BETWEEN THIS FILE'S PART 1 AND SSA's PART 1"* and states *"Anything not listed is
byte-identical to SSA."* The SC-4 rows are F-1…F-7 and none is (k). *(Application is unaffected —
the manifest carries 390–543 into H16 and M6 (II) is byte-exact containment. The gap is in the
record, not the plan.)*

**(c) §6.2 line 446 "NOT AMENDED"** — asserted while (k2) now makes the gate read the manifest's
list. The two statements need reconciling on the page.

---

## 5. WHAT THIS MEANS FOR SIGNATURE

**SC-4(k), the J3 redraft, and the SC-3(a) change are NOT fit to sign as they stand.** Three of the
seven prior blockers are not closed, one of the three is my own verification apparatus reporting
green on drift it cannot see, and the composed read surfaced a criterion-1 leak that no clause in
this amendment addresses.

**Nothing in this round is retracted by that.** The T4 answer is still NO, and it is NO on
registered text. What is not established is that SC-4(k) contributes to it.
