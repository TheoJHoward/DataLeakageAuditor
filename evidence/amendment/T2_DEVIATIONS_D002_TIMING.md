# T2 — `DEVIATIONS.md` D-002 TIMING ENTRY, DRAFT

**Item T2. DRAFT ONLY. NOT APPLIED.** `DEVIATIONS.md` at repo root is 0 bytes (verified this pass). Nothing below has been written to it. This entry is delivered here for author review; at ceremony fire time it is appended after D-001 (see `ceremony/DEVIATIONS_DRAFT.md`) under the append-only rule of `PREREG.md` §11 item 6.

**T3 compliance.** No chat-only identifier appears in the entry text. Citation authority is carried by the ceremony commit sha and by named registered files (`PREREG.md` sections, `PRIOR_ART_VERIFICATION.md`, `DESIGN.md` §2.11). Substance of the finding is stated in the entry's own words.

---

## THE ENTRY — append verbatim to `DEVIATIONS.md` after D-001

```markdown
---

## D-002 — §10.1 kill-gate collective consequence: advance firing (timing entry, class C amendment `prereg-v30a`)

**Date recorded:** «CEREMONY-FILL: ceremony date, DD Month YYYY»
**Class:** timing / procedural. The clarification of §10.1's collective consequence is a class C amendment (SC-14) carried by the same ceremony commit as this entry. This DEVIATIONS entry records the timing on which SC-14 is fired.

**What is recorded.** §10.1's five conjunctive kill-gate criteria have been evaluated by an **AUTHOR DETERMINATION IN ADVANCE** that they will not be jointly satisfied before the project's calendar milestone (`PREREG.md` §10 heading: "UChicago — 1 November"). This is not a measurement taken on the calendar due date; it is a finding, dated above, that no maintained tool exists which satisfies all five criteria against that milestone.

**Timing.** The finding is dated approximately **nine weeks ahead** of the calendar due date. The firing is voluntary: no failure has occurred in the prior-art surveys that would have compelled the finding to be delayed to a later measurement. The date above is the calendar day of the ceremony commit that carries SC-14.

**Basis.** `PRIOR_ART_VERIFICATION.md`, sha256 recorded in the same tag message under §11 item 8 (per SC-8(f)), records the author's verify-at-source pass of two candidate tools (`leak-detect`, `leakage-buster`) and the assessment-at-interface-level of six others (`bioLeak`, `deepchecks`, `mlinspect`, `leakr`, feature-store family, plus a method note on the sweep-calibration criterion). None satisfies §10.1's five conjunctive criteria against the reconstructed acceptance-fixture declaration. The comparison behind the finding is set out row-by-row in `DESIGN.md` §2.11 (three-column table: `leak-detect` | `leakage-buster` | here).

**Consequence stated.** Under SC-14 in the same ceremony commit, the consequence of §10.1's firing is **deferral of release, not termination of the project**: the v0.1 release (§10 Phase 3) waits behind any subsequently-verified maintained tool that satisfies all five criteria; work on Phases 1–7 continues on the plan of §10. The upstream-contribution consequence of §10.1's original text is unchanged and is joint with the deferral.

**No later measurement extinguishes the deferral.** SC-14 clarifies that a later measurement cannot convert deferral into termination, because §10.1's collective outcome is the deferral consequence as amended. Later prior-art discoveries that satisfy §10.1's five criteria continue to defer; they do not terminate.

**Cross-reference.** Ceremony commit: «CEREMONY-FILL: full commit sha». SC-14 clause: `PREREG.md` §10.1 v30a insertion after criterion 5. Ledger row: K2 §8.2 amendments block, table (b), row for §10.1 lines 1017–1024. Prior-art basis: `PRIOR_ART_VERIFICATION.md` sha256 recorded in the tag message under §11 item 8.
```

---

## PLACEHOLDERS THAT REMAIN AT LAND-TIME

- «CEREMONY-FILL: ceremony date, DD Month YYYY» — one placeholder, filled at the ceremony fire step (X4).
- «CEREMONY-FILL: full commit sha» — one placeholder, filled once the ceremony commit is written (X4, after `git commit` but before `git tag` when the sha is knowable, or as a follow-up patch to `DEVIATIONS.md` in the same ceremony).

Both are ceremony-fill values; neither is pre-computable. This matches the D-001 discipline stated in `ceremony/DEVIATIONS_DRAFT.md` (six placeholders not fillable before ceremony).

---

*T2 complete. Append point is the end of `DEVIATIONS.md`, after D-001, per `PREREG.md` §11 item 6's append-only rule. Nothing above is applied. Delivered for author review as part of the R27 T1–T4 deliverable set.*
