# T1 — CRITERION 5 AMENDMENT (SC-14), DRAFTED FOR THE X5 FINAL `PREREG.md` DIFF

**Item T1. DRAFT ONLY. NOT APPLIED.** No repository file was touched. The clause below is drafted in the same schema-set form as SC-1 through SC-13c, ready to be inserted into `SCHEMA_SET_FINAL.md` Part 1 as SC-14 and to appear as one hunk in the FINAL PREREG.md DIFF (X5 deliverable). It is delivered here so a reader can review the clause and its ledger row without opening the full schema set.

**T3 compliance.** No chat-only identifier appears in the clause text below or in its ledger row. The rationale narrative describes the clarification in its own words; citation authority is carried by the ceremony commit and by `DEVIATIONS.md` D-002 (delivered separately as T2). The trigger date is stated as a calendar date, not as "the criterion's date" (which is itself derivable from §10.1 read against the project's calendar).

---

## PART 1 — REGISTERED TEXT BEING AMENDED

**`PREREG.md` §10.1, criterion 5** (v30 line 1024, verbatim):

> 5. Has had a release or commit within the previous 12 months.

The heading it sits under (`PREREG.md` §10.1 v30 line 1017–1019):

> ### 10.1 Phase 0 kill gate — objective
>
> **Stop building and contribute upstream if a single maintained tool satisfies all five:**

Together these carry a **stop-building-and-contribute-upstream consequence** as the collective outcome of §10.1's five-criterion conjunction. The consequence is unqualified in v30. The word "stop" resolves, under the stronger-reading rule registered by SC-9 (drawn from `AVAILABILITY_DECLARATION.md` §D.3), toward **termination of the project**: the collective outcome does not by itself distinguish "release deferred" from "project killed". This clause fixes that.

---

## PART 2 — CLAUSE TEXT (SC-14, drafted in schema-set form)

### SC-14 — §10.1 KILL-GATE CONSEQUENCE, CLARIFIED

**INSERTION POINT.** After `PREREG.md` line 1024 (kill-gate criterion 5, the closing item of §10.1's five-criterion list), inline within §10.1 as a marker-and-paragraph block immediately below the list and above §10.2's heading.

**MARKER at the site of §10.1 lines 1017–1024** (block above the list, no registered text superseded):

> **§10.1 collective consequence — v30a, CLARIFIED.** §10.1's collective outcome is now the SC-14 consequence below. The five criteria and their conditions stand byte-exact; only the outcome that fires when they are jointly satisfied is clarified.

**INSERTION TEXT — §10.1, after `PREREG.md` line 1024 — SC-14.** *(Operative text below, inserted as a paragraph block.)*

> **§10.1 kill-gate consequence — v30a.** When a single maintained tool satisfies all five criteria of §10.1, the consequence is **deferral of release, not termination of the project**: the v0.1 release (§10 Phase 3) waits behind the maintained tool, and work on this project continues on the plan of §10 Phases 1–7. This clarifies §10.1's collective outcome without changing which conditions fire it, which candidates it applies to, or the upstream-contribution obligation §10.1's original text carries jointly with it.
>
> **How the gate is fired.** The five criteria may be evaluated on the calendar day at which §10.1 falls due, or the gate may be fired ahead of that day as an **AUTHOR DETERMINATION IN ADVANCE** — a stated finding that the five conditions will not be jointly satisfied against the calendar milestone `PREREG.md` §10 records ("UChicago — 1 November"). An advance firing is a determination, not a measurement, and is registered in `DEVIATIONS.md` as a timing entry that names the ceremony commit carrying this amendment. Once fired as an advance determination, the consequence is the deferral consequence above; **no later measurement converts deferral into termination**, because §10.1's collective outcome is the deferral consequence as of this amendment.
>
> **What this clause does not permit.** It does not weaken, add, or remove any of the five criteria. It does not change which candidates the gate ranges over. It does not permit deferral to be treated as a shipping event, or a shipping event to be treated as deferral. It does not remove the obligation to contribute upstream where the gate fires: the deferral consequence is joint with, not a substitute for, the upstream-contribution consequence.

**Tagging.** `[SC-14]` anywhere in `PREREG.md` means this clause; `SC-14(x)` means its lettered limb (none is added by this draft; the clause is drafted as three paragraphs, not sub-limbed).

---

## PART 3 — THE LEDGER ROW (K2 §8.2 amendments block)

Insertion into the K2 §8.2 amendments-block **table (b) Registered text standing byte-exact, its reading extended or partly superseded by a marker at its site**. This row is proposed for (b) rather than (a) because the criterion text itself is not superseded; only §10.1's collective consequence is clarified. The five criteria remain byte-exact.

| Registered surface (v30 line) | What the marker states | Clause | Class |
|---|---|---|---|
| §10.1 lines 1017–1024 — kill-gate collective outcome | the collective outcome is the SC-14 deferral consequence; the five criteria and their conditions stand byte-exact | SC-14 | C — §0.2.1 line 93's "acceptance criterion" (as read for the collective outcome of §10.1) |

**Justification cell (for the K2 authors' internal cross-check; the table above carries only the standard four columns).** `PRIOR_ART_VERIFICATION.md` (sha256 recorded in the tag message under §11 item 8 / SC-8(f)) records the two verify-at-source and six assessment-at-interface prior-art passes against §10.1's five conjunctive criteria; `DEVIATIONS.md` D-002 records the timing basis of the advance firing. No chat-only identifier appears in this row.

---

## PART 4 — RATIONALE, INCLUDING TIMING

**Why this is an amendment, not an interpretation.** The stronger-reading rule registered by SC-9 (originating in `AVAILABILITY_DECLARATION.md` §D.3, at `PREREG.md` insertion point after line 99) would otherwise resolve the ambiguity in §10.1's word "stop" toward the strongest reading — termination of the project. To prevent that reading from binding, the consequence is stated explicitly in the registered text via SC-14 rather than left to the interpretation rule.

**Why deferral, not termination.** The project's own calendar record — `PREREG.md` §10, "**Concept A pre-registration — September. UChicago — 1 November.**" — states 1 November 2026 as a hard milestone. A maintained tool that satisfies §10.1's five criteria does not extinguish the acceptance-fixture reproducibility work, the availability-primitive verification, or the eventual release with the author's own instrumentation; it changes the ordering by which they matter. Deferral of release preserves those work items; termination discards them.

**Timing of the firing.** This clarification is being made **nine weeks ahead of the criterion's calendar due date**, while firing the criterion voluntarily. No failure has occurred: `PRIOR_ART_VERIFICATION.md` records that no candidate satisfies §10.1's five conjunctive criteria as of the pass dated **12 August 2026**, and the ceremony commit that carries this amendment freezes that finding via the manifest hash chain. The AUTHOR DETERMINATION IN ADVANCE is made from a completed prior-art pass, not from an unresolved question, and is dated in `DEVIATIONS.md` D-002 as the calendar day of the ceremony commit.

**Standards inheritance.** The clause follows the SC-N drafting standards of SC-1 through SC-13c: insertion point stated by `PREREG.md` line number of the registered text as-tagged; text quoted in a blockquote and marked as insertion; a "does not permit" limb bounding the clause; the `[SC-14]` tag naming convention; ledger row entered under (b) of K2 §8.2 with a justification that carries no chat-only identifier; substance registered in `PREREG.md`, evidence in `PRIOR_ART_VERIFICATION.md`, timing in `DEVIATIONS.md` D-002.

---

*T1 complete. To land: (1) insert the SC-14 clause into `SCHEMA_SET_FINAL.md` Part 1 after SC-13c; (2) append the ledger row to `K2_AMENDMENT_LEDGER.md` §8.2 (b); (3) include the corresponding `PREREG.md` diff hunk in the FINAL PREREG.md DIFF for X5 delivery. Nothing above is applied. `DEVIATIONS.md` D-002 (T2) is a separate append-item at ceremony time and is delivered as its own file.*
