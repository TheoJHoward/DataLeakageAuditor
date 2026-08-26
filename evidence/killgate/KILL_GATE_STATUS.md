# KILL-GATE STATUS — `PREREG.md` line 991, Phase 0

Item G3, 2026-08-14. **Nothing outside this directory was edited. No git command was run other
than read-only inspection. `PREREG.md` is byte-unchanged** (`git diff --stat PREREG.md` empty;
sha256 `f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6`).

**The registered row, verbatim** — `PREREG.md` line 991:

> | **0** | Fixture declaration reconstruction with evidence; prior-art verification; cross-tool comparison per §9.2; licence check | 1–2 wknds | **Kill gate (§10.1)** |

---

## The four deliverables

| # | Deliverable | State | What remains |
|---|---|---|---|
| 1 | **Fixture declaration reconstruction with evidence** | **ASSEMBLED, NOT SIGNED OFF** | `AVAILABILITY_DECLARATION.md` (3,684 lines) exists and its §A.5 marks §6.2's three reconstruction clauses SATISFIED, with a code or paper citation per element recorded before any detector exists. But its own header lines 3–5 still read "**DRAFT — AUTHOR REVIEW REQUIRED** … Nothing in this file is a registered declaration", it carries **42 lines of uncommitted modification** over commit `ffa6d94`, and it carries a **class C amendment** awaiting the `prereg-v30a` ceremony — which is not authorized in this run. **Remaining: author review, then the ceremony.** |
| 2 | **Prior-art verification** | **SIGNED OFF — IN THE WORKING TREE ONLY, NOT COMMITTED** | `HISTORY.md` H-34 (lines 264–292) is a complete signed kill-gate sign-off: search surfaces, equivalence test, nine candidate verdicts, judgment, re-fire condition, and a recorded two-sweep miss calibration. **It is not in `HEAD`** — `git show HEAD:HISTORY.md` contains no `H-34`; it is part of the +33-line uncommitted diff. The `PRIOR_ART_VERIFICATION.md` sha256 it cites **verifies**. **Remaining: four factual corrections (below), then the commit.** |
| 3 | **Cross-tool comparison per §9.2** | **GENUINELY UNRUN** | §9.2 requires **executing third-party tools**. Seven of its clauses are unsatisfiable without a run. **This cannot be assembled from documents and it has not been done.** What this item produced is the half §9.2 requires be fixed *before* any run — case set, roster, eligibility matrix, label mapping, scoring rules — in `CROSS_TOOL_COMPARISON.md`. **Remaining: E1–E7 in that file — ~162 case-runs plus installation, and author sign-off of the declaration first (line 448 ordering).** |
| 4 | **Licence check** | **INBOUND COMPLETED THIS ITEM; OUTBOUND GENUINELY UNRESOLVED** | **Inbound done:** 18 rows, every tool named in H-34, `PRIOR_ART_VERIFICATION.md`, `DESIGN.md` §2.11 and the 2026-08 sweep — **six of which had no licence recorded anywhere in the project before now**. **Outbound not done:** `PREREG.md` §13.2 line 1089 says "Licence — **resolve in Phase 0**"; there is **no `LICENSE` file among the 24 tracked files** and `README.md` declares none. **Remaining: an author decision, entangled with §13.5's deepchecks wrap.** |

---

## The §10.1 gate verdict, and the distinction that matters

**§10.1 does not fire.** No single maintained tool satisfies all five criteria; every candidate
fails **criterion 1** (coverage at the same tier or better) on desk evidence alone. No tool found —
new or old — probes a user *callable* at runtime against a *declared per-cell availability model*.
That is H-34's judgment and this item found nothing that disturbs it.

**But the gate not firing is not the same as the phase being complete.** Line 991's Work column
lists four deliverables and two are unfinished. Concretely:

- **§10.1 criterion 3** — "Fires on `fixture_contaminated` and is silent on `fixture_corrected`" —
  is an execution predicate and is **currently unevaluated for every candidate**. Under §10.1's
  conjunctive structure an unevaluated criterion cannot cause the stop, so the *verdict* is safe.
  The *record* is incomplete, and a reader who checks will find criterion 3 blank.
- **§9.2 is a deliverable in its own right**, not merely an input to §10.1. It is the evidence
  behind any comparative statement about this tool, and `PREREG.md` line 165 already commits:
  "**Comparative completeness is not claimed here.** Whether this is more complete than existing
  tooling is what Phase 0 (§10.1) tests." **That test has not been performed.** Until it is, no
  comparative claim may be made — and the registration is honest precisely because it says so.

---

## The decision this actually forces

`PREREG.md` line 448 orders the comparison **inside Phase 0**, after reconstruction. It cannot
quietly slide into Phase 1. Against that:

- The execution surface is **9 rostered tools × 8 cases × 2 sides = 144 case-runs**, plus
  9 tools × 2 fixture sides = 18, plus per-tool installation and adapters.
- Line 991 budgets **1–2 weekends for all four deliverables**.
- §10.2 criterion 4: "**Any phase competing with September or 1 November → pause**", against hard
  constraints at line 987 — "Concept A pre-registration — September. UChicago — 1 November.
  Neither moves." Today is 14 August 2026.

So the question is not "is §9.2 done" — it is not — but **which of three the author chooses**:

1. **Run it.** Execute E1–E7 after the declaration is signed off. Honest, complete, and the
   schedule is tight.
2. **Descope it by amendment.** Narrowing "one per leakage type" or the roster changes what a
   published comparison means and is therefore **class C** under §0.2.1 line 93 — an amended
   registration, not a `DEVIATIONS.md` entry.
3. **Defer it with a `DEVIATIONS.md` entry** recording that Phase 0 advanced with §9.2 unrun, and
   carry criterion 3 as explicitly unevaluated. This changes no rule and no published number, so
   it is the mechanism that fits — **provided the deferral is recorded rather than assumed.**

**This file does not choose.** Option 3 is the cheapest and the one most easily mistaken for
having done the work, which is exactly why it has to be written down if taken.

---

## Corrections recommended to H-34 before it is committed

Reported, not applied. H-34 is uncommitted, so these are cheap now and expensive after the
ceremony. Full evidence in `CROSS_TOOL_COMPARISON.md` §5.

| # | H-34 text | Problem |
|---|---|---|
| 1 | line 271, "the assistant-conducted sweep of **the same date**" (12 Aug 2026) | The sweep evidence on file is self-dated **2026-08-08 / 2026-08-09** (its agent prompts read "Today is 2026-08-08"; its synthesis reads "as of 2026-08-09") |
| 2 | line 291, "Phase 0's sweep did not surface `leakr`, `bioLeak`, `LeakageDetector` 2.0 or `Leakly`" | The sweep on file **did** surface `leakr` (with CRAN vignette detail) and `LeakageDetector` 2.0 (extensively, by two of four agents). `PREREG.md` §1.1 line 152 also names LeakageDetector 2.0. Either "Phase 0's sweep" denotes a different earlier pass — which should then be named — or the sentence is wrong |
| 3 | line 291, "covered Google Scholar and CRAN" | CRAN yes. **Google Scholar does not appear** in the sweep's own recorded search log (eight WebSearch queries plus primary fetches to PyPI, CRAN, GitHub, arXiv, HAL) |
| 4 | line 282, "`bioLeak` (CRAN, Dec 2025)" | CRAN today: **bioLeak 0.3.8, published 2026-05-21**. It is **active within §10.1 criterion 5's window**. Verdict unaffected — it still fails criterion 1 |

**Not in question:** the `PRIOR_ART_VERIFICATION.md` sha256 cited at H-34 line 271,
`b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`, **verifies** against the file
as it stands. And none of items 1–4 changes H-34's judgment.

**Note the append-only rule** at `PRIOR_ART_VERIFICATION.md` line 7 if item 4 is carried into that
file: corrections go *below* the original entry, not as an edit to it.

---

## Files produced by this item

| File | Contents |
|---|---|
| `killgate\CROSS_TOOL_COMPARISON.md` | The §9.2 determination (requires execution), the committed protocol — 8 cases, 9-tool roster with eligibility matrix, label mapping, scoring rules — desk-verified tool facts, the execution list E1–E7, and 7 author decisions |
| `killgate\LICENCE_CHECK.md` | 18-row licence inventory with sources; the three-activity constraint analysis; the deepchecks AGPL fact pattern for §13.5; the unresolved §13.2 outbound gap |
| `killgate\KILL_GATE_STATUS.md` | This file |

All three are **drafts, uncommitted**, under
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\killgate\`.
