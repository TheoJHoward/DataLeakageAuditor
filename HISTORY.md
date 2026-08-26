# History — Data Leakage Auditor

**Not a normative file.** Nothing here instructs an implementer. `PREREG.md` and `DESIGN.md` contain the specification; this file contains the record of how it got there and what it got wrong on the way.

**Why the separation exists.** Through v22 the ledger lived inline in the locked file as parenthetical notes, and the numbered lessons lived in `DESIGN.md`. Normative and historical prose cannot be told apart linguistically — `DESIGN.md` §4.5 read as an explanation of the determinism guard and was in fact an instruction to rebuild a deleted branch, and it survived two rounds of sweeps because of it. The distinction is now structural: an implementer's input contains no recounting of deleted machinery at all.

Committed with the pair, hashed in the tag message, and referenced from both files by ID.

---

## Ledger notes, by ID


### H-01 — from `PREREG.md`

*(v17 said a bar-level defect in unchanged text "goes to `DEVIATIONS.md`" — which would have deferred a defect that changes a published number because it happened to be outside the current diff. Before the tag, a number-changing defect is a pre-registration defect wherever it lives; §0.2.1's classes govern from the tag forward, not before it. v17's sentence was written in the section arguing it was time to stop, which is the second time that section produced a rule favouring the author.)*


### H-02 — from `PREREG.md`

*(v19 said "eight of ten" with the confidence of a measurement. It is a causal claim about the document's own history, and this document has spent eleven days establishing that unaudited claims don't survive contact. The audited count is six, two of them partial.)*


### H-03 — from `PREREG.md`

*(v16 said any locked rule contradicted by a Phase 1 measurement could be rewritten through `DEVIATIONS.md`. A deviation makes a change visible; it does not make the revised rule ex ante. Under that wording a new branch, a moved denominator, or a different licence for a tier could be introduced after seeing the measurement and still be described as registered — which is the failure mode this whole document exists to prevent, appearing in the section written to justify stopping.)*


### H-04 — from `PREREG.md`

*(v17 said the affected lock is "rewritten" without limit here and in §10.0 step 3, which is the blanket permission §0.2.1 exists to withdraw — stated in the same document, two sections apart.)*


### H-05 — from `PREREG.md`

*(v14 through v18 pre-registered a second `statistical` regime — noise-floor comparison for nondeterministic pipelines — which §13.9 recommended deferring while the document specified it in full: four combinations, three REVIEW labels, guard-failure routing, statistical control comparators, a future partition, unbuilt-mode accounting, and its own gates and denominators. That is a large specification surface for a mode that is not scheduled, budgeted, or expected to ship, and it produced firings in v13, v15, and v17. It is removed and parked; see §13.)*


### H-06 — from `PREREG.md`

*(v14 stated the licence globally in §3 and then described the upgrade here without saying what happens when the confirmation is stochastic, needs a tolerance, or uses a promoting perturbation — so two implementations could tier the same confirmation differently.)*


### H-07 — from `PREREG.md`

*(v20 published it as a fraction while §6.1 forbids publishing rates from the fixture, and left it unclear whether §7.10's interval requirement and §8.6's provenance rules applied to it. A count carries no inferential interval and invites no population reading, which is the honest form for a single fixture.)*


### H-08 — from `PREREG.md`

*(v14 said "every strategy is preserving," which is impossible while `complex` is in the set.)*


### H-09 — from `PREREG.md`

*(v21 named only evaluation and conformance. The fixture gate run is a fourth execution context and it was left unstated, so its outcome was order-dependent: a promoted strategy that a short-circuiting order would never reach could produce the finding on `fixture_corrected` that fails criterion 3, or fail to produce the primary finding criterion 1 needs — and §6.2's k-of-N count, now the sole reported fixture outcome, moved with strategy order. An acceptance result that changes with an unstated execution choice is the bar this rule exists to clear.)*


### H-10 — from `PREREG.md`

*(v14 through v18 pre-registered a `statistical` regime here — noise-floor comparison, a routing policy, mode-specific control comparators, a future evaluation partition, and unbuilt-mode accounting — for a fallback §13.9 recommended deferring and no phase budgeted. It produced firings in v13, v15, and v17 and is now parked; see §13. Registry entry 15 states the cost to nondeterministic pipelines.)*


### H-11 — from `PREREG.md`

*(v13 said "apply the strategy's promotion map to the original baseline's output," which admits a blanket reading — promote every numeric column, then compare. That fails a pipeline emitting an internally generated integer column, such as a bar counter or an arange, which never touches a promoted input: the aligned run leaves it integer, the blanket-promoted original makes it complex, and a behaviourally identical pipeline is refused. The comparator decides execution eligibility, so the reading moves published rates. v12's plain byte equality failed even more broadly — see §0.4.)*


### H-12 — from `PREREG.md`

*(v15 checked once per strategy with no detector, cohort, or mask argument, so a pipeline could pass the check and then drop rows on a real probe.)*


### H-13 — from `PREREG.md`

*(v14 said the other rows use "the same metric family," which would have included proof yield — a number a mode incapable of producing proofs cannot have.)*


### H-14 — from `PREREG.md`

*(v20 said the four statuses partition attempts and separately that `non_proving` is excluded from every published rate; an attributable attempt cannot be both inside the partition and outside every rate computed from it.)*


### H-15 — from `PREREG.md`

*(v19 called a determinism-blocked confirmation `non_proving` in §4.4 and `unavailable` in §7.1. They mean opposite things: one asserts an effect was seen and merely could not be proven, the other says no valid comparison happened. Two implementations would have computed different attempted, attributable, and inconclusive figures from the same runs.)*


### H-16 — from `PREREG.md`

*(v21 said "excluded from every published rate" while the equations put it inside `attempted`; both could not be implemented.)*


### H-17 — from `PREREG.md`

*(The status was called `suggestive` through v16, which asserts the evidential weight the rule forbids, while §4.4 printed it and `DESIGN.md` said it "strengthens the narrative." The name was doing work the rule denies.)*


### H-18 — from `PREREG.md`

*(v15 published counts alone, which measures nothing about their reliability: an implementation could attach suggestive evidence to every false static warning and still pass its confirmation-mode gate, because none of it became PROVEN. Scoring them would need their own precision and false-alarm rates split by both runtime axes, on a row that already carries two modes; the cheaper honest option is to stop treating them as evidence.)*


### H-19 — from `PREREG.md`

*(v15 had one key that omitted `promotion_status`, so once the aggregator collapsed a pair found by both a preserving and a promoting run into a single PROVEN finding with the promoting run as corroboration, there was no `dtype_promoted` record left to count in the exact-promoted row — and whether corroborating evidence contributed to that row's evidence yield and false-alarm rate was undefined.)*


### H-20 — from `PREREG.md`

*(v13 collapsed them, so an optional strategy's failure produced a top-level `could_not_run` entry that failed `assert_audit_complete()` on a case §7.7 called complete.)*


### H-21 — from `PREREG.md`

*(v14 said only "a valid finding is terminal," which let a promoting strategy's REVIEW finding end the case before a required preserving strategy ran — so whether a leak reached PROVEN depended on escalation order, and `assert_audit_complete()` could pass with the proof-capable strategies unexhausted.)*


### H-22 — from `PREREG.md`

*(v21 defined the object and left these formulas saying "mode completed," so an implementer could keep computing from the detector-case state the object was introduced to replace.)*


### H-23 — from `PREREG.md`

*(v17 asserted "at least 88" while `DESIGN.md` refused to state a total and noted the same assertion came from terms summing to 86 — the pair could not both be committed.)*


### H-24 — from `PREREG.md`

*(v21 changed the default from binary search to a full scan for correctness and left the cost term logarithmic, so every quoted total silently excluded the new dominant term.)*


### H-25 — from `PREREG.md`

*(v16's open decisions 10 and 11 are resolved and moved into the locked text: the compatibility threshold's form is §6.11's fraction-with-minimum-count, and every execution frame uses one routing policy — §6.9. Decision 11 needed no special promoted-frame rule: a promoted family's failure already reaches only that family's strategies, and §7.7's required-or-optional machinery produces the asymmetry the permissive alternative was reaching for.)*


### H-26 — from `DESIGN.md`

*(v14 through v18 carried a `statistical` regime here, with `terminal_decision_policy.on_determinism_failure`, noise-floor controls, and an unbuilt-mode accounting rule, for a fallback that was never scheduled. Removing it deletes those three mechanisms along with two of the four metric rows.)*


### H-27 — from `DESIGN.md`

*(An earlier version marked `nan` and `constant` as always promoting. Since §2.5's per-run computation is authoritative no tier was ever at risk, but the table drives default selection, and the error made the proof story look worse than it is: on all-float frames `noise` and `nan` are both preserving and neither is probabilistic.)*


### H-28 — from `DESIGN.md`

*(Earlier versions stated a single minimum including a timestamp and an availability model, which is false for the non-temporal path and would have turned runnable cases into `unsupported`.)*


### H-29 — from `DESIGN.md`

*(v18 added a `select_fixture_branch` step choosing between ordinary, substituted, and not-fully-adjudicable acceptance, plus the capability matrix it consulted. `PREREG.md` §0.2.1 records why all of that went: it existed to reconcile a gate requiring PROVEN with a proof licence that correctly refuses PROVEN for promoted-only findings. Decoupling the gate from tier removed the conflict and the machinery together.)*


---

## H-A — the coupling audit (from `PREREG.md` §0.2.1)

| Firing | Descends from the gate's tier requirement? |
|---|---|
| v7 row order vs availability | No — the primitive |
| v8 mask valid for rows it wasn't built for | No — the primitive |
| v9 comparator contradicted itself | No — declaration merge |
| v11 scoring unit, false-alarm denominator, L3.1b stated twice | No — accounting |
| v12 alignment comparator failed by construction | No — the guard stack |
| v13 statistical mode unaccounted; blanket comparator reading | Half — the first is the parked regime, the second is the guard stack |
| v14 undefined substituted gate; orthogonality; termination | **Yes** — the substituted gate exists only because of it |
| v15 trigger excluded its motivating case; per-frame guards; scoring key; compatibility | **Partly** — the trigger, yes; the rest, no |
| v16 compatibility aggregation level | No |
| v17 false capability entry; combination execution policy | **Yes** — capability exists only for the trigger |
| v18 incomplete subtraction of the same tree | **Yes** |

*(→ `HISTORY.md` H-02)*

---

## Version ledger (from `PREREG.md` §0.4)

Recorded because a pre-registration showing no reversals is one nobody stress-tested.

- **v3** claimed the runtime perturbation method was novel. False — `leak-detect` had implemented it in 2020.
- **v5** let defaults be chosen on the corpus its rates come from; published rates without fixing denominators; returned *not applicable* where the risk was real and the tool merely could not test it.
- **v6** required the user's environment to match a recorded stack for exact equality, degrading nearly every real user to handle a case the determinism guard already covered. Unsealed all evaluation data four phases early. Described a hash as a seal.
- **v7** probed row order rather than availability, so a trailing window and its `.shift(1)` version were indistinguishable and current-bar inclusion was outside the flagship detector.
- **v8** fixed that primitive and introduced three defects doing it: an unsound comparison scope, conformance cases contaminating accuracy rates, and a fixture declaration that could be chosen to make the gate pass.
- **v9** merged L3.1b's declaration set into the general availability model under general field names, so `ties` contradicted the definition it implemented.
- **v10** stated the three claims of §0.3 as settled. They are argued.
- **v11** left three things underdetermined: no canonical count for a pair found by several probes; no clean-case denominator when a case fails to complete; and L3.1b stating its rule twice.
- **v12** tightened the alignment comparator to plain byte equality, which fails by construction on every dtype-promoting strategy. It also left five things undefined that decide eligibility or tier: non-temporal L2a's declaration, the fallback's tier, "completed case" under partial strategy failure, L1.2's two modes sharing one metric family, and conformance having neither a metric nor separation from the code debugged against it.
- **v13** created the statistical-evidence mode without giving it accounting — its metrics were never enumerated, clean-case rates had two readings for the same run, and nothing said whether a determinism failure routes to the fallback or to `could_not_run`. It also adopted a comparator fix whose blanket reading fails a pipeline emitting an internally generated integer column, and it treated promotion-aware *baseline* equivalence as sufficient to license a proof about *counterfactual* behaviour (§3).
- **v14** left three things underdetermined at the evidence/proof boundary: §6.2's promotion-forced fixture branch invoked a "corroborated-REVIEW form" defined nowhere, in a branch reachable whenever a permutation-invariant leak runs through integer columns; the evidence bases were enumerated as alternatives when comparison mode and promotion status are orthogonal, leaving a statistical promoting run unplaceable; and §7.7's "a valid finding is terminal" let a REVIEW finding from a promoting strategy end a case before a required preserving strategy ran, making proof yield depend on escalation order.
- **v15** left four things underdetermined, all at the boundary between a rule and the mechanical fact it assumes: §6.2's substituted-gate trigger required that no compatible preserving strategy exist, which excludes its own motivating case — `shuffle` is compatible and preserving and merely blind to a permutation-invariant leak, so the trigger would not fire and the ordinary gate would fail a working method; the determinism guard ran once on the original frame while promoted strategies execute on aligned frames that can be nondeterministic where the original is not, mislabelling a nondeterminism artifact as an exact-mode finding; the canonical scoring key omitted `promotion_status`, so the four combinations it is scored by could not be reconstructed once the aggregator collapsed a pair found by both a preserving and a promoting run; and compatibility was checked once per strategy for masks that differ by detector and by cohort.
- **v18** was correct and still wrong-shaped: it repaired the capability condition, the per-source mapping, the `unknown` bypass and the harness chronology rather than asking why any of them existed. It also justified the change with a claim that does not hold — that the new gate would be "strictly stricter." The acceptance sets are **incomparable**, not ordered: a fixture detected only at `dtype_promoted` with nothing on clean or corrected fails the old gate and passes the new one, while a fixture detected at PROVEN throughout but with one REVIEW finding on a clean source passes the old and fails the new. §6.2 now says decoupled and rebalanced, which is what it is.
- **v17** built its substitution gate on a capability claim that is false. "`shuffle` cannot move a permutation-invariant statistic" holds only when the permutation acts within exactly the set the statistic consumes. A trailing rolling mean at row *i* consumes one masked cell — the decision bar — plus unmasked history; permuting the masked region replaces that cell's value with a different one and the mean changes. The error ran in the permissive direction: it would have classified `shuffle` as incapable against the fixture's own likely mechanism and triggered the easier gate. v17 also keyed coverage and completion at detector × mode while publishing and gating four combinations, so a combination was evaluated only on cases where another combination found nothing — outcome-dependent denominators in a published rate — and it left `unknown` capability as a third, easier acceptance route.
- **v16** wrote §0.2.1 to justify stopping the revision loop and gave it a permission broader than a pre-registration can carry: any locked rule contradicted by a Phase 1 measurement could be rewritten through `DEVIATIONS.md`. Transparency is not the same as being ex ante, and that wording would have let a semantic change — a new branch, a moved denominator, a different licence for a tier — be made after seeing the measurement and still be described as registered. It also scoped §6.11's compatibility failures to a single strategy while §7.2 publishes over combinations, leaving one cohort probed and unprobed at the same time.

---

## Review lessons (from `DESIGN.md` §9)

**Review lessons, dated.**

1. *(28 Jul 2026)* v3 claimed no existing tool probed at runtime. The claim survived several review rounds and was false; `leak-detect` had been on PyPI for six years. **Models are poor at telling you something already exists.** Prior-art verification is a search task, done by the author, written down.
2. *(28 Jul 2026)* One reviewer returned "lock-quality, GO" on a version a parallel review found four exploitable defects in. **A single reviewer's approval is weak evidence** — this recurred four more times, in both directions, including a GO on v11 that missed three bar-level defects.
3. *(29 Jul 2026)* v6 added an environment-matching requirement that would have degraded nearly every real user, to handle a case the determinism guard already covered. v12 then locked an alignment comparator that failed every dtype-promoting strategy by construction. **A safeguard can make the tool worse.** *(The instances are listed in this entry and the count is read off them; it is deliberately not stated as a numeral. This entry once read "and it has happened twice" — a count that a third instance would have falsified in silence, since the obligation to re-bump it lived outside the edit that added the instance. That is H-L13's shape, and a lesson about safeguards is a poor place to keep one. Corrected 21 Aug 2026 while a third candidate instance was under examination, and corrected whether or not that instance is upheld — the numeral was fragile on its own terms.)* **The scrutiny a new guard needs is not "what does this prevent?" but "what does this ALSO prevent?"** — a guard is written against the harm its author has in mind, and reaches everything its words reach.
4. *(29 Jul 2026)* Through v7 the flagship detector could not catch the error this document names as the one it exists to catch, because the definition it rested on was not the definition that mattered. **Verify the primitive before hardening everything built on it.**
5. *(30 Jul 2026)* **The defect class migrates to wherever the previous round's fix landed.** v9's comparator fix produced v11's accounting holes; v11's accounting fix produced v12's guard failure; v12's guard fix produced v13's comparator gap; v13's tier demotion produced v13's unaccounted statistical mode. A reviewer's attention lags one round behind the work, so the next review starts at the newest text, not the oldest.
6. *(30 Jul 2026)* This file did not exist in reviewable form for four consecutive rounds while `PREREG.md` was revised six times, and its hash goes in the same tag message. **The binding constraint on a deliverable is not always the thing being worked on.** Producing both halves in one pass is what unblocked it.
7. *(31 Jul 2026)* Three of v16's four firings — whether `shuffle` can move a permutation-invariant statistic, whether a pipeline stays deterministic on a promoted frame, whether compatibility varies by mask — are questions a few executions answer and no volume of argument settles. They were adjudicated by argument for a full round because argument was the only instrument in the room. **When a specification question has a mechanical answer, the loop only converges once something runs.** `PREREG.md` §0.2.1 routes this class to the Phase 1 gate rather than to another version — under a citation test, and only for facts and parameters, never for new semantics.
9. *(31 Jul 2026, audited 1 Aug)* Six of eleven firings descended from one clause coupling the fixture gate to a reporting tier. Each round patched the failure point and each patch added a decision point — a trigger, a matrix, a state, a routing rule — which is where the next round's defect lived. Removing the coupling deleted all of them at once, and the version that did it is shorter than the version before it. The count was first published as "eight of ten" and audited down to six, two of them partial — a claim about the ledger's own history is still a claim. **Patch at the coupling, not at the failure point.** Reviewers examine the text where a defect surfaced, which is downstream of its cause, so this is the class of finding an ensemble is structurally poor at producing.
11. *(1 Aug 2026)* Three of v20's announced fixes were never in the file. They were applied as silent string substitutions that did not match, and spot-checking a few of them passed. **An edit that reports nothing when it fails is indistinguishable from an edit that worked**, and a change log written from intent rather than from the file will confidently describe fixes that do not exist. Every edit now asserts its match count, and the change log is written from a diff of the file.
10. *(1 Aug 2026)* A subtraction leaves residue, and the residue is operative rather than cosmetic: after v19 removed the statistical regime, the configuration list still serialized its routing policy and noise-floor parameters, the Phase 1 gate still demanded the deleted capability matrix, and the fixture gate forbade only *primary* findings on clean sources — so the tool's own classifier could exempt its own false positives. **Deleting a mechanism means sweeping every clause that could still instruct an implementer to build it**, not only the clauses that describe it.
8. *(31 Jul 2026)* §0.2.1 was written to justify stopping the revision loop, and its first draft granted a permission no pre-registration can carry: rewrite any locked rule that a measurement contradicts, transparently, and call it registered. **The section arguing that it is time to stop is exactly where a self-serving rule will appear**, and it took a reviewer to say so. The rewrite splits mechanical facts and locked-procedure parameters, which Phase 1 may resolve, from semantic changes, which need an amended registration tag before the affected detector exists.
12. *(12 Aug 2026)* An archive-wide survey for the two aggressor columns reported 37 files; a filesystem walk over the same root found 119. The search tool honours the archive's `.gitignore`, which excludes `/PC2_TRANSFER_v4/scripts/` and `/results/` to keep parquet out of git — and with them two mirrored code trees, including the archive's only copy of the Phase 7 simulator, where a confirmed aggregation defect was later found. **A survey that inherits a search tool's default exclusions measures the ignore list, not the archive.** Archive-wide counts now come from a filesystem walk that reports how many files it scanned. Dated by the day recorded, not the day worked — the convention this list follows from here.
13. *(12 Aug 2026)* A cross-reference in `DESIGN.md` §9 named the review-lesson list as `H-L1 through H-L11`. Appending H-L12 left the range stale; appending H-L13 (this lesson) would have left it stale again. Two prior instances of the same shape — an obligation that names its target by enumerated index into a growing list — were recorded as Z2 in earlier review rounds and each was fixed by bumping the index in the same edit that changed the thing indexed. **Three instances is a structural defect, not bad luck: enumerated ranges in cross-references are fragile by construction, because the obligation to re-bump lives outside the edit that grows the target.** The `DESIGN.md` reference now names the series (`the H-L review-lesson series`, open range) rather than its current tail, so appending a lesson cannot desynchronize a registered document. The same shape — an index that must be re-bumped in a separate edit — is looked for in any future cross-reference whose target grows. **What this lesson is NOT about, added 21 Aug 2026 after a sweep for the shape nearly deleted a constraint.** The fragile object is a numeral that *points at* an enumeration which may grow: it goes stale silently, because nothing in the edit that adds the eleventh item forces the sentence that said ten to be found. A numeral that *forbids* growth is the opposite object and is not covered here — "exactly three classes, mutually exclusive and exhaustive; there is no fourth class and no residue class", or "the exception rests on two grounds and on no other". There the count is not a reference to the set, it **is** the rule: it is what closes the set, and a reader who strikes the numeral in the name of this lesson has not de-fragilised a cross-reference, they have deleted the constraint and admitted a fourth class. **The test is what happens when the target grows.** If growth silently falsifies the numeral, the numeral is a stale reference and this lesson applies. If growth is what the numeral forbids, the numeral is a closure constraint and removing it is a weakening, which §0.2.1 line 97 does not permit an amendment to make.
14. *(21 Aug 2026)* A check written to enforce that every amendment hunk carries readable operative text asserted on the wrong object. It verified the field was present in the assembler's internal records and passed — thirty-eight of thirty-eight — while the delivered artifact rendered **none** of it. The field existed; the reader could not see it. **A check that asserts on an internal representation, while the delivered output is what the reader acts on, passes for the wrong reason — and a green check is worse than no check, because it is evidence of a property nobody has.** The rule taken from it: a check asserts on the delivered artifact. Where it must read an internal structure to know what to expect, it derives the expectation from that structure and then tests the artifact against it, never the structure against itself. Looked for in any future check whose subject and whose assertion are different objects. **A second form, and the sharper one, because it was a verification rather than a delivery.** A sweep written to find dropped source blocks reported "0 dropped" over a population it had defined as one heading shape; the file also held a differently-headed section, three fenced blocks, and five runs carrying markers for several sites at once. **Green inside an unverified scope is evidence of nothing.** So a check states the population it covers and PROVES the statement — by counting the whole file and showing the in-scope and out-of-scope parts sum to it — before reporting any result about that population. The rule paid for itself in the round it was written: it forced four successive widenings of one population definition, and without it the artifact built on that population would have been missing an entire section and every fenced block. A related trap sits one level down — a *size* threshold is a scope restriction wearing a different hat, and one silently dropped a 174-character block that the assignment depended on.
15. *(21 Aug 2026)* A review reported that a registered surface — a marker extending §11's items 1–7 — had no hunk to land it, and offered as one disposition that the ledger row was spurious and should be removed. It was not. The applied verification copy carried the marker in place, and three further records corroborated it; the search had been run over the drafting sources, which are not authoritative for what the applied text contains. **An absence finding is only as good as the search behind it, and its remedy is deletion — which makes it the most dangerous class of finding to get wrong.** A claim that something does not exist now names the artifact searched and states why that artifact is authoritative for the question; where it is not, the claim is downgraded to "not found in X" and no disposition follows from it. The same round produced the mirror case: a check reported an apparatus block "leaked" into applied text when the text was a registered line quoted verbatim under an attribution — a *presence* finding that was also an artifact of asking the wrong question of the wrong document. Both were fixed by making the assertion structural rather than textual. **Hardened 21 August 2026 (R48/Q8), after the shape recurred four times in a single workflow.** Four independent absence findings, each reported at PROVEN confidence, held that the §9.2 prior-art comparison set did not exist and that no tool had ever been run against one. All four were wrong: the set exists, and eleven tools were run against it on 14 August 2026. Every one of the four declared a search population that **excluded the active drafting root the round was working in** — one of them stopped a single directory level above it. **A stated population is not a proof of coverage**, and the four were not careless in any way this lesson, as previously written, would have caught: they each named what they searched. An absence finding now states the population it searched **and shows that population included the root the round declares itself to be working in**; where the claim is unscoped — asserting that a thing exists nowhere, rather than that it is absent from a named artifact — naming that root is required rather than optional. **The requirement now lives in the check that scores absence claims, not only in this entry.** That is the whole point of the hardening: this lesson had already been written, and written correctly, and it did not prevent the recurrence. **A rule that can only be complied with by remembering it is a rule that will be forgotten.**
16. *(21 Aug 2026)* A check written to replace a failed check inherited a new blind spot from its own design, and only mutation testing found it. The predecessor sampled five 110-char windows of each hand-assembled amendment hunk — 21% of one 2,612-char hunk — and passed every material mutation put to it, including **flipping "fails this gate row" to "is recorded as a deviation"**, which is precisely the reduction the rule it enforced exists to forbid. Its replacement tiled 100% of each hunk by longest match and caught that flip — and still passed both DELETIONS, because **coverage is deletion-blind by construction: removing text never lowers the provenance of what remains.** One blind spot had been traded for another, and reasoning about the design would not have shown it; mutating the artifact did, in one run. **A check that replaces a failed check is mutation-tested against two sets: the failures that defeated its predecessor, AND the failure modes its own design admits.** The second set is the one nobody thinks to assemble, because a check is written by someone who believes it works. **Reasoning about a check establishes its intent; mutating the artifact establishes its reach.** The fix here was a converse direction — the source block, extracted fresh and required to survive verbatim — and deletion is not a hypothetical class for this project: it is the class that produced hunk 2.33. *(A related property earned its keep in the same round and is worth naming: the interim check printed "NO SPAN DECLARED (deletion-blind, reported not assumed)" against the eight hunks it could not fully cover, rather than rounding the gap to PASS. That is this registration's own coverage-accounting discipline — declare the population and prove it was covered — implemented inside the verification tooling, and it is why the remaining gap was visible to be closed on purpose rather than discovered later by something failing.)*
17. *(21 Aug 2026)* One tool produced three separate failures in one session and each was patched where it surfaced before anyone asked what they had in common. A re-anchoring tool recomputes manifest line ranges after the source document moves. Its failures: a marker extracted without its trailing newline made the growth figure one short, leaving every shifted row one line shy of its block; a pairing rule matched blocks by start line, so an earlier block growing made a later changed block read as one block removed and a different one added; and sub-entry boundaries were shifted through a block that had grown from three lines to twenty-five, leaving one sub-entry pointing at text that was no longer there. **All three are the same assumption: that every change is DISPLACEMENT.** A block that moved but whose content is identical is displaced, and arithmetic on its offsets is valid. A block whose own content changed has **invalidated every boundary inside it**, and no offset arithmetic can recover them — they have to be re-derived from the markers in the source. **Patching each instance leaves the assumption in place, which is why there were three; the fix belongs at the coupling**, and the tool now detects which case it is in and **refuses** to shift sub-entries through a block that grew internally, reporting them for re-derivation instead of guessing. **The sharper half is which checks saw any of it.** Not the re-anchoring tool — its arithmetic was self-consistent every time and it reported success. Every one of the three was caught by a check that goes back to the SOURCE and compares text: byte-exact containment of a source block in its hunk, and a character-count proof over reconstructed content. **A check that re-derives from source catches what a check that recomputes offsets cannot, because the second one shares the first one's assumption** — they are not two independent opinions, they are one opinion stated twice. Where a value can be either recomputed or re-read, the re-read is the check and the recomputation is the thing being checked.
18. *(21 Aug 2026)* **A registered redesign changes what a criterion MEANS, and every passage that DESCRIBES it is stale from that moment until somebody re-derives it.** The descriptions do not announce this. They go on reading fluently, in the register of settled fact, describing an object that no longer exists — which is why all three instances here surfaced months later and none surfaced by being noticed in passing. **Instance one: the declared map lagged Y1.** Y1 ruled that no fed column is MBO-fed; the map went on carrying 360 SCORED, strict-positive cells across six `mbo_*` classes, predicting REQUIRED findings that no unit could carry, under a clause declaring its three dispositions "mutually exclusive and exhaustive over the map". **Instance two: the declaration's artifact allocation lagged R9.** §0.1 and §0.2 were written when criterion 3 read "no runtime finding appears on `fixture_corrected`" — a silence test, answerable from any artifact that can be observed to produce nothing. R9 replaced silence with map-scoring, which made the criterion require a **column** and a **cell**; the allocation was never re-derived, and went on saying criteria 1–4 were "all statements about Artifact B" — an artifact the same section says stores **no feature columns**. Under that description criterion 4's identity control had no `net_delta` to run over and was unevaluable, which is how far a stale description can travel without tripping anything. **Instance three: the §6.2 line-459 marker lagged R11.** It read "ADDED NOT SUPERSEDED — criterion 1 stands byte-exact", true of the bytes and false of the requirement: R11 moved the denominator to a derived partition, and on 14 of 25 leaking-source columns the demand inverts from *absence is a miss* to *a finding fails the gate*. **The common shape: the amendment edits the RULE and leaves the DESCRIPTION, and a description is what a reader actually reads.** A byte-level diff shows nothing at any of the three sites, which is precisely why the check has to be semantic. **After any semantic amendment, sweep the descriptions** — every passage in every corpus that describes the amended object, judged against what the object now is, with a passage that merely RESTATES the old rule counted stale even where it contradicts nothing. And the sweep is done by somebody who did not draft the amendment, because the drafter reads the description and sees what they meant.
19. *(24 Aug 2026)* **A rule restated as a literal does not merely go stale — it FORKS.** Lesson 13 covers a numeral that *points at* an enumeration and goes stale when the target grows; this is the adjacent failure, and its signature is different. The v30a tag message's hash set is defined once, as `FILES=` in the ceremony's §3.2, and every gate in the ceremony iterates that list — **no gate reads a numeral at all.** The count was nevertheless restated in prose about thirty-nine times, and by August 2026 the same set was being asserted with **five different values**: **two** (`PREREG.md` line 97's "both file hashes", a closed quantifier written when the block held two files), **three** (§11 item 3's enumeration by path), **five** (working resolution R7, true of the inherited v30 five), **six** (the declaration's §D.2 and the whole ceremony package) and **seven** (an open author decision that had sat unresolved for twenty rounds). Each was locally plausible and none was a reference to the others, so nothing could disagree with anything: **independent assertions do not contradict, they diverge.** **The evidence that this is structural and not carelessness is that it recurred inside the round that named it.** While rewriting the staging plan to fix the defect, the agent doing the fixing carried the figure "245 paths" forward into its own new text without re-deriving it; the tree had been 249 files for some time. The same round then drifted two line-keyed detector exemptions by sixty-four lines by inserting a section above them, and found three cross-references that had been one hundred and sixty-nine lines out of date. **A count that is not computed from the thing it counts is not a description of that thing; it is an independent claim about it, and independent claims drift apart.** The remedy is never a corrected numeral, because a corrected numeral is the same object again: it is **one authority plus a check that fails when a restatement disagrees with it**, and where a count cannot be mechanised, the form lesson 13's own neighbours already use — state the count, name the enumeration, and pre-empt the likely miscount, as the H-B addendum does with "a verifier counting entries rather than firings will get twenty-three; the reconciliation is here." **Lesson 13's exception is carried forward unchanged and matters more here, not less:** a numeral that *forbids* growth is a closure constraint, not a reference, and deriving it away deletes the rule. The test is unchanged — ask what happens when the target grows. **And the corollary that makes this checkable: a check whose failure mode is "the human did not notice" is not a check.** The staging verification that should have caught the miscount was `git diff --cached --name-only | sort` under the words "EXPECT, exactly" — a print with no assertion, which had never been executed, and whose expected list named a file that is byte-identical to the previous tag by design and therefore could never have appeared in it.
20. *(24 Aug 2026)* **A sweep result is not a result until its POPULATION and its EXCLUSIONS are stated with it.** Lesson 15 requires an absence finding to state its population and prove it covered the whole of it; this is that rule made **prospective**, and it is separate because it binds at a different moment. Lesson 15 is applied when a finding is written. This one binds when the sweep is DESIGNED, because by the time the finding is written the exclusion has already become invisible: it is a line of code, not a claim, and nobody reviews it as a claim. **The instance.** A sweep for count literals across the shipping corpus reported eleven verified sites and closed. Its matcher skipped every line beginning with a table pipe — a reasonable-looking choice, made because tables are mostly data — and **three stale declaration hashes and byte sizes lived in table rows**, so they were never in the population at all. They surfaced a round later, by accident, in the output of an unrelated command. The sweep was not wrong about what it examined; it was silent about what it did not, and a silence about coverage reads exactly like coverage. **The rule: state the population definition and the explicit exclusion list WITH the result, before anyone finds the gap.** And where an exclusion cannot be justified on the record, **it is not an exclusion, it is a miss — re-run rather than caveat.** A caveat added after the gap is found is a description of the gap, not a defence of the method. **The same discipline applies to a check's exemption list**, which is a population definition wearing different clothes: an exemption keyed to a line rather than to a value licenses every future error on that line, which is how the declaration-hash check passed a freshly injected wrong hash on an exempted line until its own negative test caught it.
21. *(24 Aug 2026)* **An instrument's PASS is a statement about its DOMAIN, not about the world — and until the domain is measured, nobody knows which.** Lesson 20 requires a sweep to publish its population; this is the harder case, because a CHECK does not look like it has a population. It looks like it has a rule. **Ten instances, and the direction is what matters: every one narrowed what could be seen, and every one therefore produced a PASS.** The conformance walk enumerated §6.2 by line and omitted one normative line. Four archive sweeps excluded the very directory the work was happening in. A count sweep excluded lines beginning with a table pipe, and three stale verification values were living in table rows. A declaration-value check had to be widened twice. A hash-count check had a vocabulary ceiling at "eight"; **the same check detected no NUMERALS at all**, so a count written in digits could have said anything, and it had reported PASS for its whole life; it also read "twenty-five" as twenty, which is worse than a miss because a wrong value can accidentally equal the right one and pass. Exemptions were keyed to a LINE rather than to a VALUE, so an exemption meant "this line may be wrong" rather than "this line may say this". A staging verification was a print with no assertion that had never once been executed. A registered condition had no command at all. **Not one of the ten was found by reviewing the instrument.** Reviewing an instrument recruits the same assumptions that built it — the reviewer and the author share a mental model of what counts as an input, and the gap lives exactly where that model is silent. **They were found by running the instrument against something outside its domain, or by accident.** The remedy is a BOUNDARY TEST: exercise the instrument at the edge of what it accepts and just beyond it, and record what it cannot see, as a property of the instrument rather than as a result about the corpus. **A mutation drawn from inside the accepted domain tests only that the instrument does what it does; it cannot test whether it does what it CLAIMS.** And an instrument whose gap is "none" must say how that was established: the evidence manifest's gap is none today only because a set comparison showed 248 listed and 248 on disk — the check itself can verify listed-against-disk and is structurally blind to disk-against-listed, so a file added without a manifest line would ship inside the signed tree with nothing attesting it. **Where the gap cannot be closed it is disclosed, because a verification apparatus that claims more than it delivers is the exact defect this project exists to detect in other people's pipelines.**
22. *(25 Aug 2026)* `BLOCK_MANIFEST.md` summarised its own table as *"**Six** of the 33 are multi-site runs, written out below, giving **42 entries**"*. The 42 was right and the *six* was not: the expansion has only ever held **five** multi-site runs, and 33 blocks less five expanded plus fourteen lettered rows is what gives 42 — six gives 43. The figure was wrong on the day it was written, and it sat inside a sentence whose grammatical job was to show the arithmetic closing. **A WRONG RECONCILIATION IS WORSE THAN AN ABSENT ONE: an absent one invites a reader to check, and a wrong one tells them it has already been checked.** It survived every later review precisely because it looked like the place where checking had happened. The corrected derivation, from the table rather than from the prose: **36 blocks − 5 multi-site + 14 expanded rows = 45 entries = 39 claimed by a hunk + 6 apparatus**, where the 36 is the freeze's 33 plus three additions declared at `_POPULATION_CHANGES.md` (R53/Y1 ×2, R58/W4 ×1). **This is distinct from the staleness in the same sentence** — the prose going pre-growth while the table grew is a second, independent failure, and a check that catches one does not catch the other. Detector **D13** now asserts block count, multi-site count, entry count, claimed and apparatus against the table, and was tested against both failure modes separately: reverting the count to the stale figure fires, and changing *five* to *six* with everything else left correct fires. **A reconciliation nobody can re-derive mechanically is a decoration.**
23. *(25 Aug 2026)* Three ruled items — a Phase 1 requirement for `DESIGN.md`, its companion clause, and a sweep over executed-procedure claims — were deferred rather than executed, and were carried for **eleven rounds** as the single ledger line *"Post-tag: §39 (+§72.2) into DESIGN.md; §64's D11 sweep"*. A corpus-wide search for any of those three labels returned **exactly one hit: that line**. The rulings were real and their substance existed only in chat. **A LEDGER LINE NAMING A SECTION NUMBER IS A POINTER INTO A TRANSIENT LOCATION**, and a pointer is not a record. The ledger itself could not catch this: its rule is that an item not on it does not exist, which is silent about an item that IS on it and whose substance never arrived — the opposite failure, and the one that happened. **A deferred ruling lands as a repository item WITH ITS SUBSTANCE at the moment it is deferred, not when it is executed**; recording is not doing, and it costs a paragraph. Two mechanisms now carry it: `evidence/session/DEFERRED_ITEMS.md` holds the substance, and the standing ledger gained a REPORTED-IN-SUBSTANCE column so an item that halts the tag, or waits on the author, with no round in which its substance was reported **says so on its own face**. Found only because a one-line ledger entry was challenged for its substance after three rounds of being reported as a line.
24. *(25 Aug 2026)* The ceremony's first command carried `git rev-parse HEAD  # expect ffa6d942…`. It halted the whole run — not on a defect, but on **its own success**: the commit that made it stale was `80401d0`, the kill-gate sign-off whose verdict the tag depends on. **A PINNED EXPECTATION WITH NO DERIVATION IS A CARRIED-FORWARD VALUE**, and it fails in the worst possible direction: it is silent while the world is still, and it fires on legitimate work while saying nothing about what the work was. **A ceremony is exactly where such a value detonates**, because a ceremony is the one procedure that runs long after it was written, once, under pressure, with no room to debug. The repair is not a fresher literal — that restores the defect with a newer value and buys one commit of quiet. It is to **replace the assertion with a derivation plus an accounting**: derive the fact (HEAD descends from the tag), ENUMERATE what changed, and require each item to be accounted for by name, with a reason it belongs. Stale-by-construction becomes informative-by-construction, and a new commit stops being a breakage and becomes a question worth answering. The same shape is why `git show ":$f"` reads the index rather than a remembered hash, and why H-L23's deferred rulings had to land as records rather than as pointers. **Swept for siblings on discovery** (R97/§158.5): 36 pinned values across the two ceremony files, of which **two** were current-state assertions of this class and were replaced; the rest are historical references, correct as history and deliberately untouched.
25. *(26 Aug 2026)* **Four failures of the same kind: a record made to look discharged by the things that referred to it.** **(a) An adversarial fleet found nothing its own search step had not already found.** Seventy-six per-occurrence refuters were spawned over a corpus sweep; seventy-two refuted, four survived, and every survivor confirmed what the sweep had already reported. A single completeness pass over the same corpus found a defect in the object about to be signed — an enumeration short by fourteen of the paths the registered text requires. **Redundancy tests whether a finding is right; it cannot test whether the question was the right one.** Scale the critic, not the refuters. **(b) An interface validated only against the harness that motivated it inherits that harness's blind spot.** The comparison harness passes a single frame in all eight of its cases; the acceptance fixture joins three, twice, on a wall-clock floor — and that join is the project's own headline leak channel. A contract validated against the harness alone would have been an instrument narrower than its claim, in the direction that hides findings. **(c) A fault in the auditor was reported as a fault in the audited pipeline.** A build raising on its own unperturbed input was recorded `could_not_run(determinism)`. It had not been shown nondeterministic; it had been shown not to run, which the reason precedence names `crash`. **A wrong reason is worse than an absent one: it sends the next reader to look for a fault that was never there**, and here it would have sent them into the user's pipeline for a defect in ours. Instruments that attribute their own failure to their subject are the failure mode this tool exists to detect, and it appeared first inside the tool. **(d) A disclosure that lives only in a drafting record discloses nothing.** Five disclosure lines — the attestation boundary, the deferred advisory steps, the stale-description floor, the instrument-domain gaps, and the external-input dependency — were written as they should appear and none was ever deployed into a registered file. **Three working records cited them as operative, and those citations are what made the absence invisible:** a reference reads as evidence that the thing referred to exists. One citation was in the registered declaration itself, which stated that a known-false sentence "is handled instead by specific disclosure at D-STALE" — a registered pointer into a disclosure that was not there. **The test is not whether a record is cited; it is whether the cited text resolves.**


### H-30 — from `PREREG.md` §6.6

*(v20's §0.2 named `CombinationCaseState` a fresh surface. The edit that was supposed to define it did not apply, and the file kept the sentence claiming §7.7's states suffice. They do not: §7.7 defines a *detector-case* state, and the two collapse. Take an evaluation case where the preserving strategies complete and produce PROVEN while every promoted strategy fails its frame's determinism guard. The detector-case is complete. For the promoted row, nothing said whether the case was completed, `could_not_run(determinism)`, in the promoted false-alarm denominator, or counted against the promoted 60% floor — and each answer moves evidence yield, completion rate, failure rate, and the experimental designation.)*


---

## H-B — the firing enumeration (from `PREREG.md` §0.2)

The rule has fired twenty-one times: v7 (row order rather than availability), v8 (one mask compared against rows it was not valid for), v9 (the comparator contradicted itself), v11 (scoring unit, false-alarm denominator, L3.1b stated twice), v12 (the tightened alignment comparator failed by construction), v13 (the statistical mode was created without accounting, and the comparator fix admitted a blanket reading), v14 (undefined substituted gate, evidence bases treated as alternatives when they are orthogonal, and a REVIEW finding able to terminate an unfinished proof search), v15 (the substituted gate's trigger excluded its own motivating case, the determinism guard covered one execution frame while probes run on several, the scoring key could not reconstruct the combinations it was scored by, and compatibility was checked once for masks that differ per detector and per cohort), v16 (§6.10 scoped compatibility failures to a strategy while §7.2 publishes over combinations), v17 (the one analytic capability entry the substitution gate was built around was false, and combination-level metrics were published from an execution policy that only runs a combination when another combination found nothing).

---

## H-C — the v19 coupling excision (from `PREREG.md` §0.2.1)

**v19 stopped patching and removed the coupling instead.** Six of the eleven firings descend from one clause, and the chain is shown rather than asserted:

The per-firing audit of that claim is in `HISTORY.md` (**H-A**): six of the eleven firings then recorded descend from it, two of them partially.

The clause: the fixture pass gate required a finding **at PROVEN tier**. §3.2 then made PROVEN require a dtype-preserving run, so a fixture catchable only by promoting strategies would fail the gate and fire kill criterion 2 against a working method. Every subsequent version patched that consequence — a substituted gate, then a trigger, then a capability matrix, then a dependency-set condition and a per-source mapping and a selection harness — and each patch introduced a decision point, and each decision point was somewhere new to be wrong.

The clause conflated two jobs. **Acceptance** asks whether the method separates contaminated from corrected on data whose answer is known. **Reporting** asks how much weight a user may place on a finding about their own pipeline. Tier answers the second and was never the right instrument for the first. Decoupling them deleted the substitution branch, the capability matrix, the mechanism taxonomy, the exemplar recipes, the `unknown` state, the per-source mixed gate, and the branch-selection logic — about 1,400 words and every decision point inside them.

**The rule this yields: patch at the coupling, not at the failure point.** A patch at the failure point adds a decision; a fix at the coupling removes several. Both instruments missed this for rounds because reviewers correctly examine the text where the defect surfaced, and the defect surfaces downstream of its cause. **Only the ledger sees across the loop**, so §0.2's migration chain and the table above are required reading for any reviewer taking a diff — the causal history is the one instrument a single-diff review does not otherwise have.



### H-31 — from `PREREG.md` §7.2

*(With one comparison regime, `comparison_mode` had a single value and was not carried as a key; v22 kept it as an axis after it stopped varying.)*


### H-32 — from `DESIGN.md` §4.6

*The guard precedes every comparison-based control.* §4.5 says the guard licenses exact comparison, and alignment equivalence compares an original baseline against an aligned one — under a preserving strategy those are the same frame, so it is two runs of one pipeline. A nondeterministic pipeline failed it under every strategy, died with reason `alignment`, never reached the guard, and thereby made the frozen routing policy unreachable, `PREREG.md` §7.5's determinism counts structurally zero, and §6.5's stochastic case unable to produce its own locked expected outcome.



### H-33 — from `PREREG.md` §7.7

*(v23 gated on a **completed-case false-alarm rate**, which excluded exactly the cases where a finding fired and the schedule later failed — a finding that would reach a user, omitted from the number that decides whether the detector ships experimental. That concept and that name are removed everywhere, not renamed; the active metric is the clean-case finding rate over execution-eligible cases. A global rename in v26 rewrote the old name inside this note, leaving it appearing to retract the metric it was explaining.)*


### H-34 — from `PREREG.md` §10.1 (kill-gate sign-off, prior art)

---
KILL-GATE SIGN-OFF — PREREG.md §10.1 (prior art)
Date: 12 August 2026
Author: Theo Johann Howard

I personally conducted a prior-art search on 12 August 2026, searching PyPI, GitHub (repository search and topic browsing), and general web search, using three term families: "data leakage detection" / "data leakage detector"; leakage combined with "python" and "ML pipeline"; and "lookahead bias" / "point-in-time". I did not search Google Scholar. An assistant-conducted sweep of 8–9 August 2026 (its agent prompts are self-dated 2026-08-08; an earlier draft of this entry mis-stated it as 12 August, the date of my own search) did not search Google Scholar either, on its own recorded search log — so that surface is unsearched by both sweeps and is recorded here as a gap rather than as covered. I reviewed the sweep's findings as an input, not as a substitute. Per-candidate verification detail is recorded in `PRIOR_ART_VERIFICATION.md` (sha256 `b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`).

Equivalence test applied: does the tool probe a user-supplied callable at runtime against a declared per-cell availability model?

Candidates and verdicts:

- `leak-detect` (Pawar, 2020, v0.0.1, MIT): source read by author. Black-box runtime perturbation of a user-supplied `data_creation_func` — the runtime-probe idea is genuine prior art and is NOT claimed as novel by this project. Not equivalent: the corruption region is one scalar row index (`check_row_number`, `base.py:39`, default `int(len(data)/2)`) applied as a row-block × column-list rectangle (`base.py:73`); no per-row decision time and no per-cell availability representation in the API; detection signal is NaN-count propagation (`base.py:60/91`). Broken on NumPy >= 1.24 (`np.complex` at `base.py:76` and `base.py:209`).
- `leakage-buster` (PyPI v1.0.2, 13 Sep 2025): broadest coverage found (~6 of 8 families) but no user-callable parameter; time check is split-granular. Assessed at interface level. Surfaced by the author's search; missed by the assistant sweep.
- `Leakly`: runtime label permutation against chance performance; no availability model; CV-split and sample-position based.
- `LeakageDetector` 1.0 / 2.0: static analysis (PyCharm plugin / Jupyter extension); overlap, preprocessing and multi-test leakage.
- `leakr` (CRAN, Nov 2025): statistical audit; temporal check is split-granular (train period plus lookahead window); executes no user callable.
- `bioLeak` (CRAN; v0.3.8, 21 May 2026 — an earlier draft of this entry dated it Dec 2025, which would have placed it outside §10.1 criterion 5's twelve-month window; it is in fact ACTIVE within that window): permutation-based statistical diagnostics; no per-cell availability. Criterion 5 is therefore satisfied for this candidate and the verdict rests on criterion 1, which it fails.
- `deepchecks`: overlapping detector rows; no runtime availability probe. Licence AGPL-3.0, constraining the Phase 6 wrap decision.
- `mlinspect`: runtime instrumentation for data-distribution and provenance debugging; different question.
- Feature stores (Feast, Tecton, Databricks): enforce point-in-time correctness at retrieval; do not audit arbitrary user feature code.

Judgment: §10.1 does NOT fire. No existing tool probes a user-supplied callable at runtime against a declared per-cell availability model. The runtime black-box probe is prior art (`leak-detect`) and is not claimed; the per-cell availability model is the novel element and no candidate implements it. The project proceeds.

Re-fire condition: if a tool implementing runtime probing against a per-cell availability model surfaces before Phase 2 completes, this gate re-triggers and this sign-off is void.

Recorded limitation: two independent sweeps each missed candidates, and their coverage was complementary rather than identical. Phase 0's sweep did not surface `bioLeak` or `Leakly`. It DID surface `leakr` (with CRAN vignette detail) and `LeakageDetector` 2.0 (extensively, by two of its four agents) — an earlier draft of this entry claimed otherwise, and that claim was wrong; `LeakageDetector` 2.0 is in any case named in `PREREG.md` §1.1. The assistant sweep of 8–9 Aug 2026 covered PyPI, GitHub, CRAN and general web search — not Google Scholar, on its own recorded log — and missed `leakage-buster`. The author's search covered PyPI, GitHub and general web but not Google Scholar, and found `leakage-buster`. Neither omission changes the verdict. Both are recorded as calibration facts, and together they are the reason the re-fire condition above is operative rather than decorative.
---


**CORRECTION NOTE — 21 August 2026. Recorded below the sign-off, not as an edit to it, per this
file's convention that a later contradiction is written under the original and never over it.**

*The verdict above stands and is not disturbed by anything here. What follows is a disclosure of
method that was owed when the entry was written and was not made.*

**1. The equivalence test applied above adjudicates criterion 1, not criterion 3.** The entry states
one test — *"does the tool probe a user-supplied callable at runtime against a declared per-cell
availability model?"* — and applies it to all ten candidates. §10.1's **criterion 1** is coverage of
the published types at the same tier or better; **criterion 3** asks what a tool's runtime findings
do on `fixture_contaminated` and on `fixture_corrected`. The test above is a proxy for criterion 1.
The entry does not say so, and a reader would reasonably take the ten verdicts for five-criterion
scoring.

**2. Criterion 3 was not evaluated, for any candidate, and still has not been.** No candidate was
run against either fixture side. The verdicts rest on criterion 1 failing, which is **sufficient** —
§10.1 is a five-way conjunction and a candidate failing criterion 1 cannot fire the stop — but
sufficiency is not evaluation, and the entry should have recorded which criteria were reached and
which were not.

**3. What happened with §9.2, established from artifacts on 21 August 2026 and recorded at
`DEVIATIONS.md` D-003.** Two days after this sign-off, on **14 August 2026**, a cross-tool comparison
was executed: **eleven tools over eight hand-written cases and their eight clean paired controls, 88
tool × case cells**, with the case set authored and hashed **before the first tool ran** (29.261 s,
corroborated independently of the clock by a hash chain — 112 declared case hashes recomputed, 0
mismatches). **It reached the same verdict as this entry, on the same ground: the kill gate does not
fire, and criterion 1 fails for every tool.** That corroborates the outcome above and does not repair
the method disclosure.

**It does not satisfy §9.2, which remains un-run in its registered form.** §9.2 requires the
comparison set *"committed with this protocol"*; the set is in no commit and the tagged tree of
`prereg-v30` is fixed, so that clause is **breached and uncurable for this tag**. The
acceptance-fixture half of §9.2 was not run. **§10.1 criterion 3 therefore remains unevaluated.** The
run is **unverified by any party that did not perform it**, and no result of it is cited
load-bearing here or anywhere else in the registration.

**4. Why this note exists at all.** v30a amends §10.1's criterion 3 — the criterion this gate was
signed off under. A reader comparing the two texts is entitled to learn, from the face of the record
rather than by reconstruction, that the criterion being amended had never been evaluated under
either wording. **The re-fire condition above is unaffected and remains operative.**

### H-B addendum — firings v18 through v30

The enumeration above stops at v17 because it was written then — ten firings. Completing it below adds **eleven**, for twenty-one. **Two entries are marked *not a firing*:** v19 and v23 were author-initiated restructures, not stopping-rule firings, and are listed only so the chain reads continuously. A verifier counting entries rather than firings will get twenty-three; the reconciliation is here.

- **v18** — incomplete subtraction of the substitution tree: the fixture gate forbade only *primary* findings on clean sources, so the tool's own secondary classification could exempt its own false positives.
- **v19** — *not a firing.* Author-initiated: the fixture gate's tier requirement identified as the coupling behind six earlier firings, and excised.
- **v20** — three announced fixes were never in the file (silent `str.replace` no-matches).
- **v21** — `superseded` scoped to another combination's preemption and permitted only `× none`; both halves wrong.
- **v22** — §10.2's gate still divided by completed cases after §7.7 moved the denominator.
- **v23** — *not a firing.* Author-initiated, on the parallel review's diagnosis: the measurement layer's generator named as duplicated authority plus collapsed axes.
- **v24** — `evidence_outcome` non-total; four supplemental registrations created while outlawing duplicated authority.
- **v25** — §7.4 published a second failure rate over the detector-case state.
- **v26** — reach above the cap described two different implementations across the two files.
- **v27** — assertion semantics undefined over merged findings with mixed gate status.
- **v28** — `scope-eligible` orphaned from the runtime rows by v26's own scoping.
- **v29** — the missing-trace protocol violation, found by the reducer.
- **v30** — whole-combination absence passed silently; enforcement was outcome-dependent.

Ten above plus eleven here: **twenty-one firings**, in thirteen listed entries. Every one is in this file with its cause.
