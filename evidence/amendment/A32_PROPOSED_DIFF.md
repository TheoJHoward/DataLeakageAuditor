# A32 — ONE FRESH APPROVAL DIFF, FOUR HUNKS. **NOT APPLIED.**

**Nothing here is applied.** `PREREG.md` is unchanged at `15baa648cb723b79…`.
R141 §1.3: §1.1 and §1.2 authorise **assembling and presenting**; they do not authorise applying.

**Each hunk is independently approvable — take some and refuse others.**

| # | hunk | act | source | source sha256 |
|---|---|---|---|---|
| 1 | §AB — the 816/830 duplicated-authority record | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1632–1679 | `32358f6dfc7f96d2…` **= the approved hash** |
| 2 | §AC — the seven `PREREG.md` disclosures | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1687–1737 | `32358f6dfc7f96d2…` **= the approved hash** |
| 3 | SC-12(w)'s limb | **EXTRACTED** | `SCHEMA_SET_FINAL.md` ll.1145–1181 | `32358f6dfc7f96d2…` **= the approved hash** |
| 4 | §7.7's row — operative + retention | **EXTRACTED, weaker provenance** | `X5_FINAL_PREREG_DIFF.md` | `a19ef62943aac8dd…` **not an approved artifact** |

---

## Placement — §AB and §AC need no container

They were anchored inside §8.2's block, which does not land. **They do not need a new one.**
`SCHEMA_SET_FINAL.md` l.77 fixes the application order:

> **SC-12 (revised) → SC-13a → SC-13b → SC-13c → §13c-P → §AB**

§13c-P is the §7.2.1 line-816 pointer and **is applied**, at `PREREG.md` **l.1346**. §AB follows it;
`BLOCK_MANIFEST.md` row 36 puts §AC immediately after §AB. **A32-placement's first branch fires**
and no container text is invented — which matters, because §8.2's item 1 is exactly the kind of
claim a container must not reintroduce.

---

## Hunk 1 — §AB. EXTRACTED, verbatim, from approved content

**Anchor:** insert after `PREREG.md` l.1346 (the §13c-P pointer paragraph), match count 1.

```markdown
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
```

---

## Hunk 2 — §AC. EXTRACTED, verbatim, from approved content

**Anchor:** immediately after hunk 1's §AB. **Seven items, and they are distinct from the
declaration's §D.6 five** — mapped at R136 and re-confirmed: no overlap, the one adjacency being
§AC-5 against `D-ARCHIVE`, which are different objects with different consequences.

```markdown
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
```

---

## Hunk 3 — SC-12(w)'s limb. EXTRACTED, verbatim, from approved content

**Why it is needed:** two operative clauses already cite it — SC-12p's pointer (*"SC-12(w)
registers the condition under which a detector-case may be reported in this state"*) and §8.3's
assertion (*"whose (w1) prohibits the state outright"*). Both cite a limb that is not in the file.

**Anchor:** after SC-12's clause at `PREREG.md` l.[1776], before the SC-13b marker.

```markdown
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
```

---

## Hunk 4 — §7.7's row. EXTRACTED, but read the provenance before approving

**Why it is needed:** SC-6b is operative and ranges over *"every detector-case coverage state
**that row** carries"*. The row is deleted, so the clause has an **empty domain** — closer to two
registered texts in conflict than to a citation defect (R141 §1.2).

**⚠️ PROVENANCE, stated because it is weaker than the other three.** `X5_FINAL_PREREG_DIFF.md` is
**not** one of the three approved artifacts. Worse, its own finding **O-11** records that the
operative row *"is nowhere quoted verbatim in `SCHEMA_SET_FINAL.md`"* and that the form below was
**recovered from a scratch applied file** — and O-11 says in terms: *"the author should not have
to reconstruct operative registered text from a scratch artifact in order to sign it."* **That is
what this hunk asks. It is flagged rather than smoothed.**

**4a — the operative row**, into §7.7's table, which currently has a header, a separator and no
body row at all:

```markdown
| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived`, `unscored` |
```

**4b — the retention marker**, after the table, so the deleted v30 row is retained the way §8.2
item 1 promises and the way A24's two clauses already do:

```markdown
**§7.7 line 855 — SUPERSEDED BY v30a. Registered v30 row, retained verbatim, NOT operative:**
"| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`,
`could_not_run(reason)`, `waived` |"
*Superseded because the six-state list has no state for a unit the declaration declares
unscoreable. Absent such a state, an unscoreable unit is forced into `not_applicable` (which reads
as "the question does not arise") or into a pass — which is the failure the state exists to stop.*
```

**A third option not taken here, flagged for you.** The `| **Strategy diagnostic** |` row sits
orphaned at l.1423, 37 lines below its header, where markdown renders it as a paragraph. Landing 4a
makes the table well-formed with **one** row and leaves that orphan where it is; R141 §A15
disposes it as a disclosure. **Moving it back into the table would repair the structure instead**
— that is a third hunk nobody has asked for, so it is named, not drafted.
