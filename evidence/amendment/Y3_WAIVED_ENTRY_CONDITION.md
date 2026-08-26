# SC-12(w) — ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE

**Verification basis for every citation below** (read this pass, `PREREG.md` byte-identical to `prereg-v30`):

- `waived` occurs **exactly twice** in the registration: line **855** (§7.7's detector-case coverage row) and line **1035** (the §10.2 floor). It has **no producer and no consumer** anywhere else.
- Line **820** (§7.2.1): "**No runtime metric reads the detector-case state of §7.7**, which exists for `assert_audit_complete()` alone."
- Line **929** (§8.3): "**`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry" — and on neither of the other four.
- Lines **860–867** (§7.7, "Completion, locked") and line **915** (§8.2) between them select a coverage state for every cause; SC-6(b) covers the declared-unscoreable case.
- Line **97** (§0.2.1): "An amendment weaker than the thing it amends is not one." Line **1035**: "…**neither runtime detector waived**…"

---

## 1-2. THE CLAUSE, AND WHAT IT DOES NOT PERMIT — MOVED, NOT RESTATED

**The applied text of SC-12(w), limbs (w1)-(w7) and its closing "What this limb does NOT permit"
block, lives in exactly one place: `SCHEMA_SET_FINAL.md`, inside SC-12.** It is not reproduced here.

**Why it moved (DELTA R37/D1).** This file carried a second copy of the clause. The two drifted:
the applied text gained the §8.3 line-929 hunk that DELTA R35/B4 ordered, while this file's bound
(6) still read *"alters no assertion in §8.3"* — which that hunk falsifies. One rule with two copies
and no canonical source is the shape §0.2.1 exists to forbid, and it produced exactly the failure
§0.2.1 predicts: a correction applied to one copy and not the other, with nothing to say which
governed. The applied text is now single-sourced; this file cites it.

**What changed in the surviving copy, recorded so the change is auditable rather than silent:**

- **Bound (6) rewritten.** It previously claimed the limb *"amends no other coverage state's entry
  condition, moves no boundary in §8.2, and alters no assertion in §8.3."* The third clause was
  false. It now states that the limb reaches §8.3 in exactly one way and deliberately — `waived`
  joins `assert_audit_complete()`'s failure set at line 929 — and that this is the whole of its
  reach.
- **The §8.3 asymmetry is now argued inside the clause** (DELTA R37/D6), not left to apparatus:
  `unscored` is deliberately **not** added to that failure set, because `unscored` is a *permitted*
  state that honest coverage accounting produces, while `waived` is *prohibited* by (w1) and so a
  report emitting it is non-conforming on its face. A prohibition no assertion tests is not
  enforced; a permitted state that failed an assertion would punish correct reporting.

**What this file still carries, and still governs:** the three candidate drafts and why two were
rejected (§4), the judge-panel scores (§4 of the round report), the non-weakening argument tested
limb by limb (§5), the ledger placement reasoning (§6), and the residual risks (§7). Where this
file's *reasoning* and the applied text disagree, the applied text governs and this file is the
record of how it was reached.

## 3. DATA THE DECLARATION MUST SUPPLY

**None — and that is load-bearing, not an omission.** Three reasons, each of them a registered rule rather than a preference:

1. **There is nothing instance-shaped to supply.** The licensed-grounds enumeration is closed and empty. A declaration could supply a ledger of licensed waivers only if licensed waivers existed; supplying one would be **asserting a permission this limb does not create**, which SC-9(a) forbids in terms — "a declaration supplies data under a registered schema; **it creates no gate object**… no new coverage state".
2. **SC-12 consumes no instance data, and this limb does not change that.** SC-12's own DATA note states it. Routing the licence through the declaration would put the entry condition for a coverage state **inside the artifact the gate is scoring**, and would additionally cut against the governed-set paragraph's rule that "the declaration may not shorten the set".
3. **The one obligation this limb creates is report-side and is stated at (w7)**: the published `waived` count, per detector and per combination, which is zero.

Declaration text naming a detector-case as waived corroborates nothing, creates nothing, and is read under SC-9(e) — resolution toward the stronger reading only.

---

## 4. WHY THIS SHAPE

### 4.1 The design tension, and why SC-6(b)'s shape genuinely does not transfer

SC-6(b) works because **`unscored` is a property of a unit**. A unit exists before any detector runs, so it can be named in a frozen pre-run ledger, and the entry condition can be "appears in that ledger, with its ground". Nothing a run discovers can reach it.

Every limb of the definition above is a property of **how a criterion is written, configured, or reported**: excluded from the denominator (i); in the denominator but not required to be non-empty (ii); the criterion satisfiable by another detector alone (iii); a threshold met without executing or by construction (iv). Limb (v) is the reporting case of the same thing. **There is no run-side object whose property "waived" is.** A pre-run ledger of *units* would therefore be a false transfer: it would let a declaration name a case and thereby waive it, which is exactly what waiving is not.

The bridge is not a ledger. It is a **prohibition**, plus the registered rule that makes the prohibition's shape permanent: **(w3)** — the state records a waiver, it never makes one. That is the sentence that actually resolves the tension. It says, in registered text, that the *coverage state* is downstream of the *criterion's design*, and never upstream of it.

### 4.2 The circularity, and how it is closed

Limb (v) says a detector is waived when "its cases are reported under §7.7's `waived` coverage state rather than executed to a terminal result." Any entry condition that licenses the state therefore licenses the antecedent of a limb of the very definition it sits inside. A permissive rule drawn wide re-opens the hole; a permissive rule drawn narrowly still creates the shape of a door.

This limb closes it **structurally rather than by careful drawing**: with (w1)'s enumeration closed and empty, limb (v)'s antecedent can never be satisfied by a licensed act. And (w3) makes the closure survive the only event that could re-open it — a future class C amendment adding a ground — by requiring in advance that any such ground be **declaratory**. Registering that rule now, while the list is still empty, costs nothing and permanently constrains the shape of every ground that could ever be added; a later amendment wanting a constitutive ground must expressly supersede (w3), in the open, and be seen to do it.

### 4.3 Why not the registration-anchored permissive form

A permissive entry condition anchored in the criterion's **own registered text** — named detector, express non-bearing, stated ground, frozen before any run, unreachable by declaration, configuration, or report — **is** non-circular. It should not be pretended otherwise. It is not adopted for two reasons:

- **Nothing satisfies it.** No criterion registered in `PREREG.md`, as amended by v30a, names a detector and registers that its result does not bear on that criterion's outcome. Its extension on adoption is empty either way.
- **Registering a permission with an empty extension makes a later widening cheaper, not dearer.** The permissive form leaves a door with a narrow frame; widening the frame is an ordinary amendment to a rule that already licenses something. The prohibition leaves no door, and adding one is visibly the creation of a permission that did not exist.

What the permissive form got right is carried over intact: the anti-silence rule (bound (1)) and the declaratory principle (w3) are its two strongest devices, and both are here.

### 4.4 Why not a declaration-side waiver register

A frozen pre-run register of (criterion, detector, combination) triples, keyed on the criterion and grounded in a citation, is the most *implementable* of the shapes — and it is the one that must be refused. The register's citation supplies at most a *limb*; the **register** supplies the combination. That selection is **constitutive**, and item (6) above makes per-combination waiving class C — which a declaration cannot effect (SC-9(a), SC-9(c)). It also puts the entry condition inside the scored artifact and contradicts SC-12's registered statement that it consumes no instance data.

There is a concrete exploit, not a theoretical one. The definition's head is written at maximum breadth — "written, configured, or reported in **any way**". `PREREG.md` line 816 is registered text that on its face suppresses a gate:

> **A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

and SC-13c(c2) already concedes the reading: "A gate suppressed on the `not_applicable`-everywhere fact is a detector waived on it — SC-12's definition, head and limb (iii)". A citation-grounded register therefore has a ready-made citation for any criterion outside its protected list, at any single combination the declaration chooses. Any register whose protection is a **closed enumeration of criteria** fails open against §10.1's stop criteria, §10.2 criteria 4–5, and every criterion added later. A closed enumeration of *grounds* fails safe.

### 4.5 Does this make limb (v) dead letter? No — and the answer is deliberate

**Stated plainly: limb (v) is not dead letter. It is more load-bearing after this limb than before it.**

Limb (v) never licensed anything. Limbs (i)–(v) are **diagnostic**: they name ways a criterion has already gone out of specification. What (w1) does is remove limb (v)'s only possible reading as a route *into* waiving, leaving it as what it always was — the rule that **classifies** an assignment of the state as a waiver, with all of the floor's consequences attached where the detector is governed. (w5) applies it in terms.

Two things would kill limb (v), and both are expressly refused. **Striking `waived` from §7.7's table** would leave the act unnamed and limb (v) with no token to classify — refused at (w6). **Re-characterising an unlicensed entry as "not really waived, just mislabelled"** would convert a floor breach into a correction — refused at (w5), which classifies the entry as a waiver first and a reporting error second. The whole point is that a non-conforming report must not be able to argue "my entry was unlicensed, therefore not a waiver, therefore no floor breach."

### 4.6 What is deliberately *not* restated

`PREREG.md` line 77 forbids a rule having two normative copies, and SC-9(f) registers the same: "**A rule stated twice has no canonical source.**" The 816/830 duplicated-authority defect recorded in this amendment is what that failure looks like in practice. So (w2) **cites** §7.7's completion lock, §8.2, and SC-6(b) and reproduces none of their content — no cause-to-state table is restated here, and in particular no routing rule for `not_applicable` is stated, because §7.7's completion lock at line 867 already routes a failed required strategy with no finding in hand to `could_not_run`, and a second statement of that mapping inside this limb would both duplicate authority and risk stating it in the permissive direction.

---

## 5. NON-WEAKENING ARGUMENT

**The baseline §0.2.1 line 97 measures against is registered v30**, where §7.7's `waived` had **no** entry condition and any report could assign it on any ground. Against that baseline this limb removes permissions and adds none. Tested individually:

**Against the definition's limbs (declaration §A.12; SC-12 limbs (i)–(v)):**

| Limb | What it names | Effect of SC-12(w) |
|---|---|---|
| **(i)** excluded from the denominator | criterion-level exclusion | Untouched and unreachable from here. (w3) forbids the coverage state from *effecting* an exclusion; bound (1) forbids a criterion's silence from being read as one. **Strictly narrower.** |
| **(ii)** in the denominator, findings not required non-empty | criterion-level softening | Untouched. No entry, licensed or not, can supply this; (w5) makes an attempt a breach. **Neutral-to-narrower.** |
| **(iii)** criterion satisfiable by another detector alone | criterion-level substitution | Untouched; reinforced by bound (5), which cites SC-13c(c6) rather than re-settling it. **Neutral.** |
| **(iv)** threshold met without executing, or by construction | configuration-level neutralisation | Untouched; (w3) expressly denies the frozen configuration of §6.8 any power to license the state. **Strictly narrower.** |
| **(v)** cases reported under the `waived` coverage state | the reporting case | The only limb this clause touches, and it touches it by making its antecedent **unlicensable**. Limb (v) survives entire as the classification rule (w5) invokes. **Strictly narrower; nothing permitted that was not permitted before.** |

**Against the definition's later items:**

- Item **(3)** "Experimental is not waived" — carried forward at bound (4), citing not restating.
- Item **(4)** "'No data' is not 'waived'" — carried forward at bound (3), with both destinations (SC-6(b)'s ledger; §8.2's not-run states) cited, and with (w3) barring the declaration from converting either into this state. Nothing here converts an unscored cell into anything.
- Item **(5)** working resolution / `DEVIATIONS.md` — (w3) names both as incapable of licensing the state, adding to SC-9(c) and SC-9(e) rather than softening them.
- Item **(6)** "Per-combination waiving is still waiving, and is class C" — **(w4)** binds the prohibition at exactly that granularity. This is the limb that would fail first under a criterion-indexed or register-keyed design, and it does not fail here: no per-combination entry is licensed, so no per-combination waiver can be effected by a report or a declaration.
- Item **(7)** "licenses nothing after tuning" — carried forward at bound (8); bound (2) adds a timing constraint (before implementation or evaluation, never after a fixture result is observed) that §0.2.1 alone states generically.

**Against `PREREG.md` line 1035 ("neither runtime detector waived"):** the floor's text stands byte-exact and is not amended, extended, or excepted. This limb strengthens it twice. First, (w1) removes the one silent route by which a governed detector could have been waived without any criterion being rewritten — a report simply assigning the state, which no metric reads (line 820) and no assertion fails on (line 929). Second, bound (2) forecloses the future: no later amendment may add a ground that licenses the state for a governed detector at a replacement criterion. The floor is a prohibition, not a permission with conditions, and this limb supplies no procedure and may not be cited as one.

**Against §0.2.1 line 97 ("An amendment weaker than the thing it amends is not one"):** satisfied *a fortiori*. The amended object is a coverage state with no entry condition. The amendment adds a prohibition, a closed empty enumeration, a declaratory constraint binding on all future grounds, a granularity rule, a breach-classification rule, a non-deletion rule, and a publication duty. It changes no threshold, no denominator, no criterion, and no assertion, and it converts no unmet element into a satisfied one.

**One honest note on the measured baseline.** Against the *already-drafted* §7.7 pointer — which bars the state outright pending a class C change — the outcome is **identical**, not looser: both prohibit. This limb *is* the class C change that pointer anticipated. Where the two texts overlap, SC-9(e) resolves toward the stronger reading, and the stronger reading is the prohibition either way. The pointer must nonetheless be redrafted (§6 and §7 below), because its statement that the conditions "are not defined by this registration" becomes false on adoption.

---

## 6. LEDGER ROW

### 6.1 Which table — and why it is not a new row

**Table (c), New clauses inserted — and it is an amendment to the existing SC-12 row, not an additional row.**

Reasoning against the other three:

- **Not (a) — registered text superseded.** This limb supersedes no registered sentence. §7.7 line 855's coverage row is **already** in (a), superseded by SC-6 (which re-registers the row with `unscored` appended); SC-12(w) does not touch that row — it leaves `waived` in the vocabulary on purpose (w6). No other registered line is displaced.
- **Not (b) — registered text standing byte-exact with a marker at its site.** No registered sentence acquires a marker. The §7.7 site's cross-reference already exists and is a pointer, which the block files under (d), not (b).
- **Not a new row in (c).** The block's own closing rule reads: "the clauses it inserts are those in (c) and no others." SC-12 is **already** enumerated in (c) at the site "§10.2, after line 1035". SC-12(w) inserts **no new clause**; it is text inside SC-12's already-enumerated insertion, at the same site, under the same class C authority. A second (c) row for the same site and clause would assert a second insertion that does not exist and would double-count against §4's derived counts. The correct edit is to the **Registers** cell of the standing row.

### 6.2 The row, as it must now read (replacing the current SC-12 row in table (c))

```
| §10.2, after line 1035 | SC-12 | "waived", defined; which detectors the floor governs; what the definition does not permit; and **SC-12(w)** — the entry condition for §7.7's `waived` coverage state: a prohibition with a closed and empty list of licensed grounds, the rule that the state records a waiver and never makes one, and the report's duty to publish the count | C | declaration §A.12; schema pass |
```

### 6.3 Consequential and mandatory — table (d), the §7.7 pointer

The pointer's current descriptor in (d) reads "`waived` is defined in §10.2; **no entry condition for the coverage state is defined by this registration**". **That becomes false on adoption of SC-12(w)**, and its applied text (drafted as hunk H8, applied after line 856) additionally says "defining them is a class C change, **and until it is made** no case may be reported as `waived`" — a sentence that presupposes the change has not been made, when this amendment is that change. Two registered texts would then disagree about whether the entry condition exists, at the exact site of the defect being fixed.

**Replacement descriptor in (d):**

> §7.7 after the table (`waived` is defined in §10.2; **SC-12(w)** is its entry condition)

**Replacement applied pointer text, after `PREREG.md` line 856:**

*(MOVED, R80/§87. **The operative copy of this pointer text now lives in
`SCHEMA_SET_FINAL.md`, inside SC-12**, as the `INSERTION TEXT — §7.7 pointer` block. That file
is the source of record for applied text; this file is the HISTORICAL SOURCE and carries the
reasoning. The text below is retained verbatim so the derivation is auditable, and it is NOT a
second normative copy — if the two ever differ, `SCHEMA_SET_FINAL.md` governs. This is the same
correction DELTA R37/D1 applied to SC-12(w)'s limb text, for the same reason: one rule with two
copies and no canonical source is the shape §0.2.1 exists to forbid.)*

> **`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.

This keeps the pointer a pointer — it adds no rule, states no prohibition of its own, and leaves the single normative copy of the entry condition in SC-12(w) (§0.2.1 line 77; SC-9(f)).

### 6.4 Also required, outside the block

`AVAILABILITY_DECLARATION.md` §A.12 currently records "The gap (RS-3), as found" and says the gap "is closed by the amended registration, not by this file", and its "Where the definition lives" paragraph enumerates what SC-12 carries — "its head and limbs (i)–(v), the rule that it may not be invoked, and the seven limits". That enumeration is now short by one limb. It is a citation, not a restatement, so the fix is one clause: add "**and SC-12(w), the entry condition for §7.7's coverage state**". No declaration data changes, because this limb requires none.

---

## 7. RESIDUAL RISKS

1. **`assert_audit_complete()` still does not fail on a `waived` entry.** Line 929's failure set is `unsupported` and `could_not_run` only, and this limb deliberately does not amend §8.3 — that would be a third insertion point and a scope expansion. **Consequence, stated plainly: a non-conforming report that emits a `waived` entry passes all three assertions.** (w5) makes such a case not complete under §7.7's completion lock and (w7) makes the count publishable, so the breach is *visible and auditable*, but it is caught by a human reading a published zero, not by machine. Closing this properly is a separate class C amendment to §8.3's failure set.

2. **The token stays in the vocabulary, so schema validation cannot reject it.** (w6) is a deliberate trade: keeping the name alive keeps limb (v) alive, at the price that tooling accepts the token. A reader may fairly argue the cleaner act was to strike the state. The counter-argument is in (w6) and I hold it — but it is a judgment, not a proof.

3. **The empty enumeration is asserted on the registration as it now stands.** Two occurrences of the word, no producer, no consumer, every not-run cause already housed. If a deferred module — the supplemental rows under §7.0, or a future criterion — genuinely needs an "ex ante out-of-denominator" state, bound (2) is the only route out and it is deliberately narrow. That is the intended cost.

4. **(w7) is a new report-side obligation created by a limb whose function is to remove a permission.** It is cheap and it is what makes the prohibition checkable, but a strict reader can call it scope creep, and it is the only thing in this limb a report must actively *do*.

5. **Bound (1)'s anti-silence rule imposes real work.** A criterion legitimately scoped to a subset of detectors now has no conforming way to express that scoping through this state at all; every unnamed detector bears and its cases are executed. The failure mode is safe-side, and a detector added later is never accidentally waived — but the execution burden is genuine and this limb does not offer a cheaper conforming form.

6. **The §7.7 pointer redraft is load-bearing and is not optional.** If SC-12(w) is adopted and the pointer is left as drafted, v30a ships two registered texts disagreeing about whether the entry condition exists. §6.3 above supplies the replacement; it must be applied in the same tag.

7. **The declaratory rule (w3) binds future amendments only as strongly as registered text binds an author.** A later class C amendment could supersede (w3) itself. What (w3) buys is that doing so must be **express and visible** — a constitutive ground can no longer be slipped in as an ordinary widening of a permission that already exists. That is a real constraint on form, not on will.

8. **Two silences remain, and I am not closing them here.** This limb does not say whether "criterion" reaches §10.1's stop/pause criteria as well as §6.2's and §10.2's — under a total prohibition the question has no operative consequence today, but it will acquire one the moment bound (2) is ever exercised. And it says nothing about a `waived` entry in a report produced before adoption; bound (7) bars retro-fitting a licence, which speaks to it only obliquely. Neither is load-bearing on this fixture, where the published count is zero.