## VERDICT

Amended §10.1 criterion 3 is a **tightening of a kill criterion, and the tightening exceeds the stated reason for the amendment**. The stated reason reaches the corrected-side limb only. The replacement also rewrites the contaminated-side limb from an existential test to a universal one, and no sentence in the amendment's own rationale mentions that.

---

## 1. HARDER — and the hard part is on the side the stated reason does not reach

**Registered (`PREREG.md` line 1022):**
> "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;"

**Amended (X5 §2.32 operative text; identical in `_E3_composed_sections.md` §10.1):**
> "3. Its runtime findings match the fixture's declared ground-truth map on **every** fixture side — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration, or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;"

Limb by limb:

**Contaminated side — strictly harder, by a large margin.** "Fires on `fixture_contaminated`" is existential and one-sided: one finding, anywhere, and the limb is met. It imposes no completeness requirement and no false-positive requirement. The replacement imposes both, per cell. The registered kill-gate limb was weaker even than the author's own acceptance criterion 1, which does carry the universal quantifier — "**Every** ground-truth leaking source column receives at least one **primary runtime finding**" (§6.2 line 459). The amendment moves the rival's test from *below* criterion 1 to *above* criteria 1+2 combined, at cell granularity. `evidence/fixture_spike/n1/declared_map.csv` is 984 data rows; **444 cells per side carry `SCORED`**. The rival must now match all of them.

**Corrected side — a swap, not a tightening.** Registered required silence; amended requires firing where the map records violations (per the declaration, 18 of 48 instrument-months on the corrected side are non-zero) and silence elsewhere. A silent tool passed under the registered text and misses under the amendment; a correctly-firing tool failed under the registered text and passes under the amendment. This limb is genuinely **incomparable**, and this is exactly the defect the stated reason describes.

**Net.** The two texts are not nested, so "strictly harder" is false as a logical claim. But the practically relevant fact is directional and clear: for the gate to fire, all five criteria must hold — "**Stop building and contribute upstream if a single maintained tool satisfies all five**" — and criterion 3 has gone from a two-bit observation to an 888-cell exact match. The set of tools that can satisfy it shrinks sharply. **Harder, and the project is correspondingly less likely to stop.**

There is a further, sharper effect. SC-3(d) requires: "**THE MAP IS STATED IN THE TERMS THE DECLARATION DECLARES.** It is stated in the representation §2.9(b) names and **side-relatively**." The map's cell key is `side,instrument,month,class,boundary` — the per-cell availability ontology. H-34's own equivalence test is "does the tool probe a user-supplied callable at runtime against a declared per-cell availability model?", and its verdict is "the per-cell availability model is the novel element and no candidate implements it." A tool that does not have a per-cell availability model **cannot emit output in the key the amended criterion 3 scores in**, so it cannot match the map, so it fails criterion 3 by construction. The amendment therefore makes criterion 3 approximately a restatement of criterion 1's novelty test. A five-criterion conjunction collapses toward "is the rival tool built the way this project is built" — and only a tool built that way can trigger the stop.

## 2. NO — the stated reason licenses only the corrected-side limb

The reason, quoted from the C2 retention block as composed:
> "*Retired because it is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire.*"

And from the hunk's own **Why** (X5 line 1255):
> "§10.1's criterion 3 is a second copy of the premise §6.2's criterion 3 retires — that silence on the corrected side is correct behaviour. Under SC-3 the corrected side is CHARACTERIZED, never clean, so a tool silent where the map declares a violation is silent where it should fire."

The retired premise is line 461, which is **entirely a corrected-side sentence**: "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`." Every clause of the reason is about the corrected side. **The contaminated-side limb is not a copy of anything §6.2 retires**, and no sentence in the rationale asserts a defect in it.

The hunk's own **What changes** describes the edit as corrected-side only:
> "§10.1's criterion 3 is replaced so the kill gate asks the question SC-3 registers: whether a candidate's findings MATCH the declared map on every side, **rather than whether it is SILENT on the corrected side**."

That sentence names only the silence limb as what is being displaced. The operative text displaces "Fires on `fixture_contaminated`" as well. **The stated scope of the change does not match the change.** The contaminated-side tightening rides in unremarked, and it is the half that makes the kill gate harder rather than merely differently-shaped.

## 3. Third-party evaluability degrades, but the amendment does provide for a cure

**Registered:** the predicate is over the rival's own outputs on two named artifacts — did it fire on one side, was it silent on the other. Given the fixture and the tool, anyone can compute it.

**Amended:** the predicate is against `n1\declared_map.csv`, an object the author reconstructs, declares, and freezes. The amendment does require publication — SC-3(a): the map "is **published as an artifact** with a **declared schema**: one row per scored cell" — and SC-8(f) puts every frozen file into §11's integrity chain. So this is not, in design, an author-only object.

**But as things stand today it is.** `git ls-files` returns 24 files; the map is not among them. It sits at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\evidence\fixture_spike\n1\declared_map.csv`, in the untracked `evidence/` tree. §11's first-commit enumeration does not name it. Freezing is not publishing, and the amendment does not state a date by which the map must be reachable.

Two evaluability facts that survive publication:
- The map is the author's reconstruction. A rival's failure can always be a defect in the map rather than in the rival, and criterion 3 no longer contains anything a third party can check independently of the author's reconstruction.
- Because of SC-3(d)'s side-relative key, a third party scoring a rival that does not partition by `(side, instrument, month, class)` has no mechanical procedure at all — the amendment states no mapping rule from a rival's output vocabulary into map cells.

Also relevant, and in the author's favour: **criterion 3 was never actually applied to any candidate.** `PRIOR_ART_VERIFICATION.md` contains no occurrence of the string "criterion", none of "fixture_contaminated" or "fixture_corrected", and no candidate was run on the fixture. Every candidate in H-34 was disposed on criterion 1 or on the equivalence test. The amendment therefore does not retroactively change the recorded H-34 verdict. It changes what happens under H-34's live re-fire condition: "if a tool implementing runtime probing against a per-cell availability model surfaces before Phase 2 completes, this gate re-triggers and this sign-off is void." **That is the only thing the amendment can affect, and it makes re-firing harder.**

## 4. A narrower amendment exists

The strictly minimal fix follows from the stated reason read literally. If the corrected-side limb "is a second copy of the premise criterion 3 retires", then a retired second copy is **deleted**, not replaced with a stronger test:

> **3. Fires on `fixture_contaminated` under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration;**

That is the whole of what the stated reason supports. Note the direction: applying the stated reason honestly makes the kill gate **easier**, not harder. The proposed amendment moves it the other way.

If the author judges bare deletion leaves too little corrected-side discipline, the conservative one-sentence version keeps the corrected limb map-relative while leaving the contaminated limb exactly as registered:

> **3. Fires on `fixture_contaminated`, and on `fixture_corrected` neither omits a finding the fixture's declared ground-truth map records for that side nor reports one the map excludes, under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration;**

Either version cures the stated defect — a kill criterion that credits a rival for behaviour the acceptance gate now scores as a miss — and neither raises the contaminated-side bar. A third option the diff itself already records at X5 line 1805 (O-25): reject C2 entirely, which "drops both rows from (a)".

## THE INCENTIVE, NAMED

The kill gate is the one criterion in the document whose satisfaction ends the project the author has spent thirty registered versions building. H-34 is committed and its verdict is "the project proceeds". The amendment raises the bar on the criterion that would reverse that, at a moment when the author knows the verdict he already holds, and it does so on a limb the amendment's own stated reason does not reach and does not mention.

**This is self-serving in effect.** I am not asserting it is self-serving in intent, and there is real evidence against intent: the corrected-side change is forced (line 461 is falsified by the fixture's own measured violations); the same map binds the author's own detectors under §6.2 criterion 3 as SC-3 rewrites it; SC-7 withholds the map from the author's own detectors at run time; SC-3(h) states in terms that "**THE AMENDMENT DOES NOT LOWER THE BAR**"; and criterion 3 played no part in the H-34 dispositions. The contaminated-side tightening reads much more like a drafting side-effect of reusing SC-3's whole-map formulation than like a manoeuvre.

But intent is not the test a pre-registration applies to itself. The test is whether the text can be read as shaped by a result the author already has, and here it can: a kill criterion was made harder to satisfy, after the gate was passed, beyond the scope of the reason given for touching it. The registration's own standard for this — §10.2's "a criterion chosen because it works after tuning is a criterion shaped by tuning" — applies with equal force to a criterion widened after a sign-off.

**Recommendation:** substitute one of the two narrow drafts in §4, or record on the face of the amendment that the contaminated-side limb is being tightened, state the reason for that tightening separately, and state its effect on the re-fire condition. The one option that should not stand is the current pairing — a tightening of a passed kill gate carried under a rationale that describes only the other limb.

## NOT ESTABLISHED

- Whether the author intended the contaminated-side tightening. Nothing in `X5_FINAL_PREREG_DIFF.md` §2.31–2.32 or `_E3_composed_sections.md` §10.1 addresses it either way.
- Whether the fixture itself is distributable to a third party. I found no redistribution or licensing clause for the fixture artifacts; without one, no third party can evaluate criterion 3 in **either** version.
- Whether `declared_map.csv` will be committed at the v30a tag. SC-8(f) and SC-3(a) point that way; no hunk I read names the file in a commit obligation.
- Whether any registered sentence requires the kill gate to be re-run under an amended criterion 3. I found none.

## FILES

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md` — §6.2 lines 445–462, §9.2 line 971, §10.1 lines 1018–1025, §10.2 lines 1030–1035
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` — H-34 at line 266
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PRIOR_ART_VERIFICATION.md` — 48 lines; no per-criterion scoring
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` — §13 (line 2009), withholding clause (line 3618), freeze enumeration (line 3504), R9 (line 3783)
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\evidence\fixture_spike\n1\declared_map.csv` — 984 data rows, untracked
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\X5_FINAL_PREREG_DIFF.md` — §2.15 (SC-3, line 609), §2.31 (C2 retention, line 1223), §2.32 (C2 operative, line 1241), O-25 (line 1805)
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\_E3_composed_sections.md` — §10.1 as composed, line 478

==============================================================================
# J4c-1 — Kill-gate criterion 3 re-run, candidate by candidate

## LEAD ANSWER

**The H-34 verdict does NOT change.** Under the v30a criterion 3, §10.1 still does **not** fire, for **no** candidate. No candidate's overall outcome flips. The amendment moves criterion 3 **strictly harder for every candidate on net**; there is no candidate for whom it is net easier, and none reaches satisfaction on the conjunction either way.

One nuance that is real and must not be lost: the amendment does **remove** a limb (the silence requirement on `fixture_corrected`) that a coarse both-sides-firing prober was failing. For `leak-detect` that is a genuine partial relief. It is swamped by two added limbs it cannot meet, so the net direction is still AWAY — but the relief component is not zero and is named per-candidate below.

---

## 1. The two texts, byte-exact

**Registered v30, `PREREG.md` line 1022** (verified with `sed -n '1022p'`):

> 3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;

**v30a operative replacement** (hunk 2.32, `X5_FINAL_PREREG_DIFF.md` line 1241 ff.; identical in `_E3_composed_sections.md` §10.1 as composed):

> 3. Its runtime findings match the fixture's declared ground-truth map on **every** fixture side — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration, or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;

**Minor discrepancy in the task brief:** the brief quotes "the fixture declared ground-truth map". Both the diff hunk and the composed section read "the fixture's declared ground-truth map" (possessive). Non-substantive, but the brief is not byte-exact.

**Scope confirmation:** §10.1 criteria 1, 2, 4 and 5 are **not touched** by v30a. The hunk index of `X5_FINAL_PREREG_DIFF.md` lists exactly two §10.1 entries at line 1022 — the operative replace and the K2 §9.2 retention blockquote. The closing sentence "Partial satisfaction is recorded and does not trigger the stop" survives unchanged. §10.1 remains a **five-way conjunction**.

**Ambiguity branch does not fire.** `AVAILABILITY_DECLARATION.md` line 1046-1049: "**SATISFIED — the clause does not fire… The original work DID document prediction timing… The fixture is therefore not semantically ambiguous and does not need a labelled hypothetical declaration.**" So both texts are evaluated under the **reconstructed declaration**, and the trailing branch clause (carried through byte-for-byte by the amendment) is inert on both sides of the comparison. It contributes nothing to any candidate's status either way.

---

## 2. Limb decomposition — what actually changed

| | v30 criterion 3 | v30a criterion 3 |
|---|---|---|
| Contaminated side | must **fire** (binary, side-level) | findings must **match the map per declared cell** — cell key `(side, instrument, month, class)`, 984 map rows, 888 SCORED / 72 UNSCORED |
| Corrected side | must be **silent** | must **fire where the map declares REQUIRED** — corrected side is non-zero in **18 of 48** instrument-months |
| False positives | not a limb of criterion 3 | **any** finding on an excluded cell fails, **on any side, at any tier, primary or secondary** (SC-3(b)); on the corrected side a false positive on one of the 22 OUT-OF-JURISDICTION columns is expressly a criterion-3 failure (`AVAILABILITY_DECLARATION.md` line 2877) |
| Uncovered cells | n/a | **UNSCORED** — "never reported as a pass" (SC-3(b), SC-3(f), SC-3(g)) |
| Object scored | any firing behaviour | **"Its runtime findings"** — narrowed to runtime output |

Net: **one limb removed (corrected-side silence), three limbs added** (per-cell match on contaminated, required firings on corrected, two-sided false-positive failure), plus a narrowing to runtime findings.

The removed limb is removed because it was false: `evidence/ceremony/H34_DRAFT.md` line 97 — "criterion 3's silence on `fixture_corrected`, falsified by the M5 sweep at 18 of 48 instrument-months"; `AVAILABILITY_DECLARATION.md` §13(b) — "**The corrected side carries strictly-post-decision absorption in 18 of the 48 instrument-months**… Peak: **zc 2025-09, 111,334 strict of 580,944 corrected rows = 19.16%**".

---

## 3. Per-candidate: criterion 3 under both texts

**A finding that governs every row: no candidate has ever been run on the fixture.** H-34 records no fixture execution of any candidate; `PRIOR_ART_VERIFICATION.md` records `leak-detect` as source-read and every other candidate as **"assessed at interface level"** under its "Method note (sweep calibration)". Criterion 3 is an **empirical** criterion on both texts. Therefore for every candidate the honest status under **both** texts is **NOT ESTABLISHED BY MEASUREMENT**; what is establishable is a **construction-level inference** — whether the tool's API can in principle produce the required object. I give both columns as that inference, flagged.

| Candidate | (a) v30 crit 3 — fire on contaminated, silent on corrected | (b) v30a crit 3 — match declared per-cell map on every side | Direction |
|---|---|---|---|
| **leak-detect** (Pawar 2020, v0.0.1) | **NOT ESTABLISHED by measurement; inferred FAIL.** It has a runtime probe, so the "fires" limb is reachable. The silence limb is inferred failed: `PREREG.md` §1.1 — "it cuts on row position, so it cannot see current-bar inclusion and it **false-flags a legitimately lagged label**", which fires on corrected. | **FAIL, structurally.** Corruption region is one scalar row index applied as a row-block × column-list rectangle (`base.py:39`, `base.py:73`); signal is NaN-count propagation (`base.py:60/91`). It emits **no per-cell object at all**, so it cannot match a map keyed `(side, instrument, month, class)`. Its row-position false positives land on the 22 OUT-OF-JURISDICTION columns → criterion-3 failure on both sides. | **AWAY on net — the one candidate with a real TOWARD component.** The silence limb it was failing is removed. It gains the per-cell-match and two-sided false-positive limbs, both unsatisfiable by its construction. |
| **leakage-buster** (PyPI v1.0.2, 13 Sep 2025) | **NOT ESTABLISHED; inferred FAIL on the "fires" limb as a *runtime* matter.** Interface takes a dataframe, target, CV strategy; **"it executes no user-supplied feature function"**. | **FAIL, structurally.** v30a scores "**Its runtime findings**". With no user callable there is no runtime finding set; an empty set cannot match a map with REQUIRED cells on the saturated contaminated side. Its time check is **split-granular**, not per-cell. | **AWAY.** No relief applies (it was not failing by firing on corrected); it acquires limbs it cannot express. |
| **Leakly** | **NOT ESTABLISHED; inferred FAIL.** H-34: "runtime label permutation against chance performance; **no availability model**; CV-split and sample-position based." It does have a runtime component, so the "fires" limb is nominally reachable; silence on corrected is unmeasured. | **FAIL, structurally.** Its output unit is a model-level chance-performance comparison, not a per-cell finding. No availability model → nothing to align to the map's cells. | **AWAY.** |
| **LeakageDetector 1.0** (PyCharm) | **FAIL.** Static analysis — it reads source, not a run. It produces no runtime firing on either fixture side. | **FAIL.** v30a is expressly scoped to "**Its runtime findings**". A static analyser has an empty runtime finding set → misses every REQUIRED cell. | **AWAY (marginally), otherwise NEUTRAL** — it fails both texts for the same structural reason; the narrowing to *runtime* findings makes the failure explicit rather than inferred. |
| **LeakageDetector 2.0** (Jupyter/VS Code) | **FAIL.** Same ground. | **FAIL.** Same ground. | Same as 1.0. |
| **leakr** (CRAN, Nov 2025) | **NOT ESTABLISHED; inferred FAIL.** H-34: "statistical audit; temporal check is **split-granular** (train period plus lookahead window); **executes no user callable**." | **FAIL, structurally.** No user callable → no runtime findings. Split-granular output cannot be projected onto a per-cell map; and per SC-3(d) there is "**no side-independent statement of what leaks**" — a split-granular verdict is exactly the side-independent object the clause calls a category error. | **AWAY.** |
| **bioLeak** (CRAN v0.3.8, 21 May 2026) | **NOT ESTABLISHED; inferred FAIL.** "permutation-based statistical diagnostics; **no per-cell availability**." | **FAIL, structurally.** Diagnostic statistics, not per-cell findings. | **AWAY.** |
| **deepchecks** | **NOT ESTABLISHED; inferred FAIL.** H-34: "overlapping detector rows; **no runtime availability probe**." Its suite fires dataset/split-level conditions, not availability findings; whether they are silent on corrected is unmeasured. | **FAIL, structurally.** Its check results are suite-condition outcomes over a dataset pair, not per-cell findings keyed to the declared cell key. No runtime availability probe → nothing to match on the corrected side's 18/48 non-zero cells. | **AWAY.** |
| **mlinspect** | **FAIL.** H-34: "runtime instrumentation for data-distribution and provenance debugging; **different question**." It does instrument at runtime, but emits provenance/distribution records, not leakage findings. | **FAIL, structurally.** Provenance records are not findings the map adjudicates; there is no violation-class dimension to align to the map's `class` field. | **AWAY.** |
| **Feature stores — Feast, Tecton, Databricks** | **FAIL.** H-34: "enforce point-in-time correctness at retrieval; **do not audit arbitrary user feature code**." They are enforcement layers, not detectors — they emit no findings on either side. | **FAIL, structurally.** No finding set at all. Note this is the one family for which v30a is arguably *less* absurd to state: the amendment's map is per-cell and point-in-time enforcement is per-cell in spirit — but enforcement at retrieval produces **no findings to score**, so the limb is vacuously unsatisfiable. | **NEUTRAL.** They fail both texts by having no finding object whatsoever; neither text's limbs bind differently. |

**Summary of direction:** 7 AWAY, 2 AWAY-marginal/NEUTRAL (LeakageDetector 1.0 / 2.0), 1 NEUTRAL (feature stores). **Zero candidates move net TOWARD satisfaction.** One (`leak-detect`) has a genuine but non-decisive TOWARD component.

---

## 4. Criterion 1, verified independently

H-34's judgment sentence is *not* criterion 1's text. H-34 applied a proxy: "**Equivalence test applied: does the tool probe a user-supplied callable at runtime against a declared per-cell availability model?**" and concluded "No existing tool probes a user-supplied callable at runtime against a declared per-cell availability model." That sentence is a statement about the **method**, not about **type coverage at tier**, which is what criterion 1 asks:

> 1. Covers at least the same published types at the same tier or better;

**This gap is worth recording: H-34's operative test is a proxy for criterion 1, not criterion 1 itself.** Mapping proxy → criterion requires the argument that L2a and L3.1 are two of the eight published types and reach PROVEN tier (`PREREG.md` §4, §4.1), so a tool without an availability-based runtime probe cannot cover them at that tier. That argument holds, but H-34 does not spell it out. Criterion 1 nevertheless **does** fail independently, and on a broader ground than the proxy — coverage count:

Baseline: `PREREG.md` line 325 — "**Eleven detector rows across the eight published types**"; line 334 — "All eight published types are *touched*"; line 423 — "**all eight published leakage categories** — two demonstrated at runtime under a declared per-cell availability model, six rule-based within a declared input model, three surfaced for review". Tiers: 6 RULE, 3 REVIEW, L2a/L3.1 PROVEN-or-REVIEW per §3 (line 332).

| Candidate | Criterion 1 status, independently verified | Ground |
|---|---|---|
| leakage-buster | **FAILS** — strongest evidence of any candidate | `PRIOR_ART_VERIFICATION.md`: "**Broadest leakage-family coverage of any candidate found (~6 of 8)**". 6 < 8, on the project's own count. Tier limb not even reached. |
| LeakageDetector 1.0 / 2.0 | **FAILS** | `PREREG.md` §1.1: Yang et al. built static analysis "for **three** leakage types"; descendants "**cover the same three types**". 3 < 8. |
| leak-detect | **FAILS** | Single runtime perturbation family; no split rules, no duplicate detection, no sampling-bias check. Also §1.1: subject to the v7 defect. Covers at most the L3.1/L2a neighbourhood, and not at tier — no PROVEN-capable determinism guard. |
| deepchecks | **FAILS** | §1.1 enumerates its suite: "date overlap, date duplicates, train-test sample mix, index leakage, identifier leakage, single-feature predictive-power screen." No preprocessing-fit-on-train+test (L1.2), no feature-selection-on-train+test (L1.3), no availability-based runtime probe. H-34's own word is "**overlapping**", i.e. partial. |
| Leakly | **FAILS** | Single method (label permutation vs chance), CV-split and sample-position based. |
| leakr | **FAILS** | Statistical audit; split-granular temporal check only. |
| bioLeak | **FAILS** | Permutation-based statistical diagnostics only. H-34 states this expressly: "the verdict rests on **criterion 1, which it fails**." |
| mlinspect | **FAILS** | Answers a different question entirely (distribution/provenance debugging); covers zero of the eight as leakage types. |
| Feature stores | **FAILS** | Enforcement, not detection: "do not audit arbitrary user feature code." Zero published types covered as detectors. |

**Verdict on H-34's load-bearing claim: criterion 1 is genuinely failed by all ten candidates.** The claim survives independent check. Two qualifications:

- **Evidentiary tier.** For `leakage-buster` and the `LeakageDetector` family the failure is established from **explicitly published counts** (6 of 8; three types). For the remainder it is established from **published interface descriptions**, not source reads — consistent with `PRIOR_ART_VERIFICATION.md`'s "Method note (sweep calibration)", which sets that tier deliberately. Interface-level is sufficient here because criterion 1 asks about *published* coverage, but it is not source-verified and should not be reported as if it were.
- **Search coverage.** H-34 records its own limitation: **Google Scholar was searched by neither sweep**, and the two sweeps missed complementary candidates. Criterion 1's failure is therefore established **over the enumerated candidate set only**. NOT ESTABLISHED for any tool outside it. H-34's re-fire condition is the correct handling and remains operative.

---

## 5. The conjunction

§10.1 fires only if **one** tool satisfies **all five**. Since the amendment touches only criterion 3, a verdict flip requires some candidate for which criterion 3 was the *sole* failing criterion under v30 **and** is satisfied under v30a. Neither half holds for any candidate:

| | Crit 1 | Crit 2 | Crit 3 (v30) | Crit 3 (v30a) | Crit 4 | Crit 5 |
|---|---|---|---|---|---|---|
| leak-detect | FAIL | NOT ESTABLISHED | inferred FAIL | FAIL | **FAIL** — broken on NumPy ≥ 1.24 (`np.complex` at `base.py:76`, `base.py:209`), so it does not "install and run… without author modification" | **FAIL** — 2020, single release |
| leakage-buster | FAIL | NOT ESTABLISHED | NOT EST./inferred FAIL | FAIL | NOT ESTABLISHED | SATISFIED (13 Sep 2025) |
| Leakly | FAIL | NOT ESTABLISHED | NOT EST./inferred FAIL | FAIL | NOT ESTABLISHED | NOT ESTABLISHED (no date in H-34) |
| LeakageDetector 1.0 / 2.0 | FAIL | NOT ESTABLISHED | FAIL | FAIL | NOT ESTABLISHED | NOT ESTABLISHED (2025 stated, no date) |
| leakr | FAIL | NOT ESTABLISHED | NOT EST./inferred FAIL | FAIL | NOT ESTABLISHED | SATISFIED (Nov 2025) |
| bioLeak | FAIL | NOT ESTABLISHED | NOT EST./inferred FAIL | FAIL | NOT ESTABLISHED | SATISFIED (v0.3.8, 21 May 2026) |
| deepchecks | FAIL | NOT ESTABLISHED | NOT EST./inferred FAIL | FAIL | NOT ESTABLISHED | NOT ESTABLISHED (maintained, no date recorded) |
| mlinspect | FAIL | NOT ESTABLISHED | FAIL | FAIL | NOT ESTABLISHED | NOT ESTABLISHED |
| Feature stores | FAIL | NOT ESTABLISHED | FAIL | FAIL | NOT ESTABLISHED | NOT ESTABLISHED (maintained, no date recorded) |

**Criterion 1 fails for all ten under both texts, and criterion 1 is untouched by the amendment.** That alone closes the conjunction for every candidate regardless of what criterion 3 says. `leak-detect` fails three criteria independently (1, 4, 5). **§10.1 does not fire under v30a. H-34's verdict — "§10.1 does NOT fire… The project proceeds" — stands.**

---

## 6. NOT ESTABLISHED / recorded gaps

1. **Criterion 3 has never been evaluated by measurement for any candidate, under either text.** No candidate was run on `fixture_contaminated` / `fixture_corrected`. All criterion-3 entries above are construction-level inferences from API surface. H-34 does not claim otherwise, but it also does not say criterion 3 went unevaluated — it substitutes the equivalence proxy for the whole five-criterion test.
2. **Criterion 2 ("explicit executed / not-run accounting") is NOT ESTABLISHED for any candidate.** Neither H-34 nor `PRIOR_ART_VERIFICATION.md` evaluates it. It is not load-bearing while criterion 1 fails, but it is an unevaluated limb of a conjunction that was signed off.
3. **Criterion 4 is NOT ESTABLISHED for nine of ten** (established FAIL only for `leak-detect`).
4. **Criterion 5 dates are recorded for four candidates only** (leak-detect, leakage-buster, leakr, bioLeak). NOT ESTABLISHED for Leakly, LeakageDetector 1.0/2.0, deepchecks, mlinspect, feature stores.
5. **H-34's operative test is a proxy, not criterion 1's text.** The proxy→criterion mapping is sound but unstated in H-34. Recording it would make the sign-off self-checking.
6. **Google Scholar unsearched by both sweeps** — H-34's own recorded gap, unchanged by this re-run.
7. **The amendment is not applied.** `_E3_composed_sections.md` header: "**SCRATCH composition for an adversarial read. Nothing has been applied to `PREREG.md`, which remains byte-identical to the `prereg-v30` tag.**" Verified: `PREREG.md` line 1022 still carries the registered v30 text. This analysis is prospective.
8. **One consequence worth flagging to the parent, outside the asked question:** the amendment's rationale ("Left registered, a candidate tool could satisfy the kill gate by exhibiting exactly the behaviour the acceptance gate now scores as a miss") is a statement about a **hypothetical future** candidate, not about any of the ten. For the ten enumerated candidates the amendment is inert on outcome — every one fails criterion 1. The amendment's value at §10.1 is **forward-looking risk closure against the re-fire condition**, not a correction to H-34's arithmetic. That is a defensible reason to make it and it should be stated that way rather than as a fix to a wrong verdict.

## Files

- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md` — §10.1 lines 1018–1026; criterion 3 at line 1022
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` — H-34 at line 266
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PRIOR_ART_VERIFICATION.md`
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` — §13 (declared map) line 2009; §13(b) corrected side line 2057; ambiguity determination line 1046
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\DESIGN.md` — §2.11 prior art table, line 196
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\X5_FINAL_PREREG_DIFF.md` — hunk 2.32 at line 1241
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\_E3_composed_sections.md` — §6.2 SC-3 at line 106, §10.1 as composed at line 476
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\evidence\ceremony\H34_DRAFT.md` — line 97

No files were created, edited, moved or deleted; no git command was run.

==============================================================================
## VERDICT (up front)

**The stop CAN fire in principle — it is not a logical impossibility. But as registered, and more so as amended, criterion 3 is not evaluable to a definite YES for any candidate that is not already a per-cell availability prober, and §10.1 contains no rule distinguishing "evaluated NO" from "could not be evaluated". Both roads default to proceed. The gate is not un-fireable; it is *one-way biased with an unregistered evaluation path*, and the amendment makes that worse, not better.**

The concern's specific composition (§9.2 abstentions → criterion 3 never satisfied) is **NOT the registered mechanism** — §9.2 is nowhere incorporated into §10.1. But the concern's *conclusion* holds by a shorter route that needs no §9.2 at all.

---

## 1. Is the §9.2 → §10.1 composition real?

**No — it is not registered. Something blocks it, but what blocks it is worse than the composition.**

Exhaustive cross-reference check over `C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/PREREG.md`:

- `"10.1"` occurs at lines 165, 449, 991, 1016.
- `"9.2"` occurs at lines 448, 971, 991.
- The **only** co-occurrence is line 991, the Phase 0 row of the phase table: `| **0** | Fixture declaration reconstruction with evidence; prior-art verification; cross-tool comparison per §9.2; licence check | 1–2 wknds | **Kill gate (§10.1)** |`

That is an adjacency of Phase 0 work items, not a scoring link. **No sentence of §10.1 cites §9.2, imports its scoring, or uses the word "abstention".** The words `abstention`/`abstain` occur in `PREREG.md` at lines 762, 837, 900, 978, 979 only — never in §10.1 (lines 1016–1026) — and **zero times in the entire composed amendment** (`_E3_composed_sections.md`).

So: **NOT ESTABLISHED that a §9.2 abstention score enters §10.1 criterion 3.** The composition as stated is not real.

**But the conclusion survives without it, by §10.1's own silence.** §10.1 is a five-way conjunction closing with one undefined sentence, which occurs exactly once in the corpus (PREREG.md:1026, and nowhere in `DESIGN.md` or `AVAILABILITY_DECLARATION.md`):

> "Partial satisfaction is recorded and does not trigger the stop."

`Partial satisfaction` is defined nowhere. §10.1 registers **no third state**. Therefore a criterion that *cannot be evaluated* — for want of an interface, a run, a join, or a definition — has no registered disposition. Either reading defaults to proceed:

- read as **not satisfied** → satisfaction is partial → no stop;
- read as **indeterminate** → the five-way conjunction is never reached → no stop.

§9.2's abstention rule is not needed to produce that outcome. It merely *names* a state §10.1 already handles by defaulting. **The defect is in §10.1, not in the composition.**

**One partial blocker, stated fairly.** An abstention arising from a *crash* (§9.2 item 5) does not create a hidden pass: the same fact independently fails criterion 4, `"Installs and runs through a documented public interface without author modification"` — a definite NO, correctly recorded. An abstention arising from *ineligibility* (§9.2 item 1, declared "from documentation") has no such backstop, because criterion 3 is fixture-scoped, not case-scoped.

**Decisive empirical fact: §9.2 has never run.** §9.2 line 973 requires "a separately enumerated prior-art comparison set of hand-written cases, one per leakage type, **committed with this protocol before any tool is run**." The string `comparison set` occurs in the repository at exactly one place — PREREG.md:973 itself. No such enumerated set exists in the repo. Per `PRIOR_ART_VERIFICATION.md`, every candidate but one was "ASSESSED FROM PUBLISHED API SURFACE, NOT SOURCE"; `leak-detect` was "VERIFIED AT SOURCE", i.e. *read*, not *run*. **No candidate was ever executed against the fixture. No abstention was ever recorded. The abstention rule has never operated at all** — the kill gate was decided without §9.2 running.

---

## 2. Under the AMENDED criterion 3: better or worse?

**Worse, on four independent grounds. The amendment strictly narrows the set of satisfying behaviours while adding an evaluation requirement that nothing registers.**

### (a) It excludes whole classes of candidate ex ante
The amended item reads `"Its **runtime** findings match the fixture's declared ground-truth map…"`. A static-analysis candidate (`LeakageDetector` 1.0/2.0, per H-34) contributes the empty set of runtime findings, which cannot supply the map's REQUIRED entries. Definite NO by construction.

### (b) It inverts the corrected-side requirement
The retention block's own stated ground (hunk 2.31, applied text):

> "*Retired because it is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire.*"

Registered criterion 3 was satisfied by *silence* on `fixture_corrected`. Amended criterion 3 requires the candidate to **fire** wherever the map declares a violation on that side. `AVAILABILITY_DECLARATION.md` §13(b) records the corrected side carrying strictly-post-decision absorption in **18 of 48 instrument-months**, up to **111,334 of 580,944 rows (19.16%)** on zc 2025-09. A rival with no availability model cannot know where those are. **The behaviour the old criterion rewarded now fails.**

### (c) A single stray finding anywhere fails it
SC-3(b): "**A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier, primary or secondary." Combined with amended criterion 3's `"on **every** fixture side"` (a silent widening from H5's "both"/"either" — flagged unaddressed as open finding **O-21** in `X5_FINAL_PREREG_DIFF.md`), one spurious correlation flag from a general-purpose auditor fails the criterion outright.

### (d) **Can a rival be run against the map at all, and what registers the join? — NOTHING DOES.**

This is the load-bearing failure.

**The cell key, measured.** `AVAILABILITY_DECLARATION.md` §13(a):

> "**Cell key, declared and named:** (`side`, `instrument`, `month`, `class`) — the unit this declaration partitions the fixture into. One row per scored cell, schema `side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag, missing_path` … **984 rows** = **960 declared-class cells** (2 sides x 8 instruments x 6 months x 10 classes) **plus 24 rows carrying the 11th diagnostic class** `mbo_all_rows`."

> "**The declared 10 classes** are trades_all, trades_buy, trades_sell, trades_large, mbo_all, mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any."

These are **order-flow event classes on an MBO lattice, indexed by instrument-month** — not column names, not leakage-type labels. Scoring a rival under amended criterion 3 requires a join: *rival finding → (side, instrument, month, class)*.

**What registers such a join: nothing.** The only mapping obligation anywhere in the registration is §9.2 item 3 (PREREG.md:977):

> "3. **Label mapping** written down before running."

That is a *label* mapping, it lives in a section §10.1 does not cite, and it is not a cell-key join. SC-13c(c5)(i) is explicit that the key is not supplied by the specification: "**The cell key is the declaration's to supply, not this clause's to state**". SC-3(d) forbids the only shape a rival could plausibly emit: "**There is no side-independent statement of what leaks**; a side-independent list is a category error and misroutes every finding derived from it."

**NOT ESTABLISHED that any registered clause supplies the join from a third-party tool's output vocabulary to the declared cell key.** The axes are incommensurable: `leak-detect` emits NaN-count propagation over a row-block × column-list rectangle (`base.py:73`, `base.py:60/91`); `leakage-buster` emits dataset-level audit rows (`|corr| >= 0.98`, WOE, rolling stats, splitter appropriateness). Neither is indexed by instrument-month × order-flow class.

**Can a rival even be *run*? — SC-7 has no registered scope over §10.1.** SC-7(a): "**AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9). **Nothing else.**" SC-7 is inserted in §6.2 and says "a detector"; §10.1 scores a *third-party tool*. Both readings are defective:

- **If SC-7 governs**, the candidate must consume an availability declaration. `PRIOR_ART_VERIFICATION.md`'s method note forecloses this for the whole measured set: "*Candidates that do not [accept a user-supplied feature function] (`leakage-buster`, `leakr`, `bioLeak`, `deepchecks`, `mlinspect`, feature stores) are assessed at interface level, since **no availability comparison is expressible without a callable to probe**.*"
- **If SC-7 does not govern**, then §10.1 registers **no input surface for candidates at all**, and SC-7(c)'s key-withholding rule ("A run that received the key has not produced a gate result, whatever it reports") has no registered application to the kill gate.

**NOT ESTABLISHED which governs.** Note also a live inconsistency: `AVAILABILITY_DECLARATION.md` §E's corollary scopes "the amended criterion 3 on `fixture_corrected`", while both SC-3 and amended §10.1 criterion 3 say "**every** fixture side".

### (e) Ordering: amended criterion 3 was never in force when the gate ran
SC-8(a) freezes the map "at the amended registration's tag". The v30a tag is unsigned. H-34 is dated **12 August 2026**. **The amended criterion 3 therefore had no map to score against on the date the gate was signed off, and no clause in the composed amendment registers a re-run of §10.1 under the changed criterion** (`re-run`/`re-evaluat`/`re-fire` return no such obligation in `_E3_composed_sections.md`). H-34's re-fire condition is triggered by *a new tool surfacing*, not by *the criterion changing*.

---

## 3. Is there any candidate for which all five could reach a definite YES?

**No — and, more sharply, criterion 3 was never evaluated on any of them.**

H-34 records the test actually applied, which is **not** any of the five criteria: "*Equivalence test applied: does the tool probe a user-supplied callable at runtime against a declared per-cell availability model?*" The only candidate given explicit criterion-level verdicts is `bioLeak` ("*Criterion 5 is therefore satisfied for this candidate and the verdict rests on criterion 1, which it fails*"). **NOT ESTABLISHED that criterion 2, 3, or 4 was evaluated for any candidate.** The gate was decided on criterion 1 as a proxy for the equivalence test.

Per-candidate, from the measured facts in H-34 and `PRIOR_ART_VERIFICATION.md`:

| Candidate | First evaluable definite NO | Criterion 3 evaluable? |
|---|---|---|
| `leak-detect` (2020, v0.0.1) | **C5** (single release, 2020, outside 12 months); **C1** (one family; no per-cell availability representation in the API) | Runs a user callable, so runnable in principle; broken on NumPy ≥1.24 (`np.complex`, `base.py:76`/`209`); output is column-level NaN counts — **no join to (side, instrument, month, class)** |
| `leakage-buster` (v1.0.2, 13 Sep 2025) | **C1** (dataset-level audit; no tier); **C2 NOT ESTABLISHED** (interface-level assessment only) | Takes a dataframe/target/CV strategy so is *executable*, but emits dataset-level rows — **no join** |
| `Leakly` | **C1** (CV-split/sample-position; no availability model) | No |
| `LeakageDetector` 1.0/2.0 | **C1**; **C3** vacuous (static analysis → no runtime findings) | Definite NO by construction |
| `leakr` (CRAN, Nov 2025) | **C1** (split-granular; executes no user callable) | No |
| `bioLeak` (v0.3.8, 21 May 2026) | **C1** (H-34, explicit) | No |
| `deepchecks` | **C1** (no runtime availability probe) | No |
| `mlinspect` | **C1** (different question) | No |
| Feature stores (Feast/Tecton/Databricks) | **C1** (do not audit arbitrary user feature code) | No |

**Every candidate fails at least one criterion on a definite, evaluable NO** — so H-34's verdict does *not* rest on unevaluability, and the sign-off is sound on its own terms. But **no candidate could have reached a definite YES on criterion 3**, and none was tested for it. The gate has never exercised criterion 3 even once.

---

## 4. VERDICT, and the falsifiable firing circumstance

**The stop CAN fire.** It is not a gate that cannot fire in the logical sense, and the §9.2-abstention mechanism the concern posits is not registered, so it is not the thing to fix. What must be fixed is narrower and sharper:

**Three registered gaps make criterion 3 unreachable in practice, and all three default to proceed:**

1. **No registered join** from a candidate's output vocabulary to the declared cell key `(side, instrument, month, class)`. §9.2 item 3's "Label mapping" is a label mapping in a section §10.1 does not cite.
2. **No registered input surface for a candidate.** SC-7 governs "a detector" in §6.2; whether it reaches §10.1 is NOT ESTABLISHED, and under either reading the criterion is unscoreable for the measured set.
3. **No registered disposition for a criterion that cannot be evaluated.** "Partial satisfaction is recorded and does not trigger the stop" makes *non-evaluable* indistinguishable from *not satisfied*, with no obligation to record which occurred.

**The concrete, falsifiable circumstance in which the stop WOULD fire.** A maintained tool (release or commit within 12 months) whose documented public interface (a) accepts a user-supplied feature-construction callable **and** an availability declaration at the same per-cell lattice, (b) is run once per fixture side under the harness with the map withheld per SC-7(b)/§E, (c) emits findings in a vocabulary with a **pre-declared join** to `(side, instrument, month, class)` written down before the run, (d) on **both** sides produces exactly the map's REQUIRED findings — including the 18-of-48 corrected-side instrument-months — and **no** map-excluded finding among the 888 SCORED cells, and (e) covers the published types at the same tier or better with explicit executed/not-run accounting. That is exactly the re-fire condition H-34 already carries: "*if a tool implementing runtime probing against a per-cell availability model surfaces before Phase 2 completes, this gate re-triggers and this sign-off is void.*"

**What this amendment should add, minimally:**
- A fourth disposition in §10.1: **a criterion that could not be evaluated is recorded as NOT EVALUATED, with its ground, and is published separately from a criterion evaluated NO** — so "partial" can no longer absorb both.
- A registered **join obligation** for criterion 3: the candidate-output → cell-key mapping is declared before any candidate is run, in the shape §9.2 item 3 declares label mappings, but cited from §10.1 and keyed to SC-3(a)'s cell key.
- An explicit **scope statement for SC-7** — whether the gate's input surface governs §10.1 candidates or not.
- A **re-evaluation trigger**: §10.1 was signed off under registered criterion 3 on 12 Aug 2026; the amendment changes that criterion and registers no obligation to re-run the gate under it.

**Files read (absolute paths):** `C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/PREREG.md` (§9.2 lines 971–981, §10.1 lines 1016–1026, §10.2, §10 phase table), `C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/HISTORY.md` (H-34), `C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/PRIOR_ART_VERIFICATION.md`, `C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/AVAILABILITY_DECLARATION.md` (§A.8, §13(a)–(b), §E), `C:/Users/ttbea/AppData/Local/Temp/claude/C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment/_E3_composed_sections.md`, `.../amendment/X5_FINAL_PREREG_DIFF.md` (hunks 2.31, 2.32; open findings O-7, O-10, O-21, O-25).

==============================================================================
## ADJUDICATION — v30a §10.1 criterion 3

Verified independently against `PREREG.md` (lines 445–462, 971–981, 991, 1016–1026, 70–110), `HISTORY.md` H-34, `PRIOR_ART_VERIFICATION.md`, `AVAILABILITY_DECLARATION.md`, `evidence/fixture_spike/n1/declared_map.csv`, and the two amendment scratch files. Nothing was created, edited or deleted; no git command other than `ls-files`.

**Three corrections to the three reports, up front.**

1. **The brief's quotation of the v30a text is not byte-exact.** It reads "the fixture declared ground-truth map". Both `X5_FINAL_PREREG_DIFF.md` hunk 2.32 and `_E3_composed_sections.md` §10.1 read "**the fixture's** declared ground-truth map". Report 1 caught this; Reports 2 and 3 did not.
2. **The ambiguity branch is NOT carried through byte-for-byte, and two places in the amendment say it is.** v30 reads `…**under the reconstructed declaration — or, where the fixture…**`. v30a reads `…**under the reconstructed declaration, or, where the fixture…**` — em-dash replaced by comma. Hunk 2.32's "What changes" says "The ambiguity branch is carried through byte-for-byte" and the C2 retention block says "The ambiguity branch is carried through unchanged." Both statements are false as written. The change is non-semantic; the false byte-exactness claim is not, in a document whose retention discipline is built on byte-exact quotation. Report 1 asserted byte-for-byte carriage and was wrong.
3. **The cell arithmetic.** `declared_map.csv` is 984 data rows. `scored_flag` partitions as **SCORED 888** (444/side), **SCORED_DIAGNOSTIC_11TH_CLASS 24** (12/side), **UNSCORED_FOR_LACK_OF_DATA 72** (36/side). So **912 rows carry a scored flag of some kind**, not 888. Whether the 24 diagnostic-class rows (`mbo_all_rows`) are adjudicated by criterion 3 or are reporting objects under SC-3(e) is **NOT ESTABLISHED** from the map or from SC-3. All three reports used 888 and none noticed the third state.

---

## 1. DOES THE H-34 VERDICT CHANGE UNDER THE AMENDED CRITERION 3?

**NO. Not for any candidate. §10.1 does not fire under v30a, exactly as it does not fire under v30. Drafting continues.**

The three reports agree and the agreement survives independent check. The reason is structural and does not depend on any contested reading of criterion 3:

**§10.1 is a five-way conjunction — "Stop building and contribute upstream if a single maintained tool satisfies all five" — and the amendment touches criterion 3 only.** Criteria 1, 2, 4 and 5 stand byte-identical; the closing sentence "Partial satisfaction is recorded and does not trigger the stop" is untouched. A verdict flip therefore requires a candidate for which criterion 3 was the **sole** failure under v30 and is **satisfied** under v30a. No candidate meets either half.

**Criterion 1 fails for all ten candidates under both texts, and criterion 1 is untouched.** That closes the conjunction on its own. The strongest instances are published counts, not inference: `leakage-buster` — "Broadest leakage-family coverage of any candidate found (~6 of 8)" against `PREREG.md` line 325's "Eleven detector rows across the eight published types"; the `LeakageDetector` family — three types per §1.1; `bioLeak` — H-34 states the disposition expressly, "the verdict rests on criterion 1, which it fails."

Per-candidate, criterion 3 moves **AWAY** from satisfaction for seven, is **NEUTRAL** for the feature stores (no finding object at all) and marginally away for the two static analysers (v30a's "**Its runtime findings**" makes their empty runtime set an explicit rather than inferred failure). **Zero candidates move net toward satisfaction.** `leak-detect` is the only one with a genuine toward-component — the silence limb it was failing is deleted — and it fails criteria 1, 4 (`np.complex`, `base.py:76`/`209`, broken on NumPy ≥ 1.24) and 5 (2020, single release) independently.

**Confirmed, and it should be stated plainly in the record: criterion 3 has never been evaluated for any candidate, under either text.** `PRIOR_ART_VERIFICATION.md`'s method note is explicit — candidates without a user callable "are assessed at interface level, since no availability comparison is expressible without a callable to probe". `leak-detect` was read at source, not run. And §9.2's precondition has never been met: line 973 requires "a separately enumerated prior-art comparison set of hand-written cases, one per leakage type, committed with this protocol before any tool is run." No such set is in the repository. H-34 substituted a single equivalence test — "does the tool probe a user-supplied callable at runtime against a declared per-cell availability model?" — for the five-criterion scoring. That test is a **proxy for criterion 1, not criterion 1's text**, and H-34 does not say so.

**Verdict: H-34's judgment sentence — "§10.1 does NOT fire… The project proceeds" — stands under v30a on its own terms. It is sound in outcome and under-documented in method.**

## 2. IS THE AMENDMENT SELF-SERVING IN EFFECT?

**Direction: HARDER. Scope: it EXCEEDS its stated reason. Third-party evaluability: it DEGRADES, and today it is nil. Self-serving in effect: YES. Self-serving in intent: NOT ESTABLISHED, and there is real evidence against it.**

**It is harder.** The corrected-side limb is a genuine swap, not a tightening — silence passed before and misses now; correct firing failed before and passes now — and that swap is **forced**, because registered §6.2 criterion 3 ("No runtime finding of any tier, primary or secondary, appears on `fixture_corrected`") is falsified by the fixture's own measurement: 18 of 48 instrument-months carry strictly-post-decision absorption, peak zc 2025-09 at 111,334 of 580,944 rows. But the **contaminated-side limb is rewritten from existential to universal**. "Fires on `fixture_contaminated`" is one finding anywhere. The replacement requires a per-cell match across 444 SCORED cells on that side plus a two-sided false-positive prohibition (SC-3(b): "It fails the gate — on any side, at any tier, primary or secondary"). The registered kill-gate limb was weaker than the author's own acceptance criterion 1; the replacement is stronger than acceptance criteria 1 and 2 combined.

**It exceeds its stated reason.** The reason, in both the retention block and hunk 2.32's "Why", is entirely corrected-side: line 461, the premise being retired, is a corrected-side sentence in every clause. The hunk's own "What changes" describes the edit as displacing one limb — "**rather than whether it is SILENT on the corrected side**." The operative text displaces the contaminated limb as well, and **no sentence anywhere in the amendment mentions that**. Report 2 is correct on this and it is the finding that matters most in this section.

**Third-party evaluability.** In design the amendment provides for it — SC-3(a) requires the map "published as an artifact with a **declared schema**", and SC-8(f) reaches the declaration that carries it. **In fact it does not exist yet.** `git ls-files` returns 24 files; `declared_map.csv` is not among them, and the whole `evidence/` tree is untracked. Freezing is not publishing. Two residual problems survive publication: the map is the author's reconstruction, so a rival's failure is always arguably a defect in the map; and **no registered clause supplies the join** from a rival's output vocabulary to the cell key `(side, instrument, month, class)`. §9.2 item 3's "Label mapping written down before running" is a label mapping in a section §10.1 never cites. Report 3 is right that this is the load-bearing gap.

**On intent.** The countervailing evidence is real and I weigh it: the corrected-side change is forced by measurement; the same map binds the author's own detectors; SC-7 withholds it from them at run time; SC-3(h) says in terms that the amendment does not lower the bar; and criterion 3 played no part in any H-34 disposition. The contaminated-side tightening reads as a drafting side-effect of reusing SC-3's whole-map formulation. **But intent is not the test a pre-registration applies to itself.** §10.2's own standard — "a criterion chosen because it works after tuning is a criterion shaped by tuning" — applies to a kill criterion widened after a sign-off the author already holds. And §0.2.1's rule cuts the same way: "A class C change discovered after the affected detector already exists cannot be made ex ante by any ceremony." The kill gate already ran.

## 3. CAN THE §10.1 STOP FIRE AT ALL?

**CAN.** It is not a gate that cannot fire.

Report 3's rejection of the posited mechanism is correct and I adopt it: **§9.2 abstentions do not enter §10.1.** "10.1" occurs at lines 165, 449, 991, 1016; "9.2" at 448, 971, 991; the sole co-occurrence is line 991, a Phase 0 work-item cell in the phase table, which is adjacency and not a scoring link. `abstention`/`abstain` never occur in §10.1. §9.2 has in any case never run.

The concrete circumstance in which the stop fires, stated so it is falsifiable: **a tool with a release or commit within twelve months, installable and runnable through a documented public interface without author modification, covering at least the eight published types at the same tier or better with explicit executed/not-run accounting, which accepts a user-supplied feature-construction callable and an availability declaration at the declared per-cell lattice, is run once per fixture side with the map withheld, and — under a join to `(side, instrument, month, class)` declared before the run — produces exactly the map's REQUIRED findings on both sides, including the 18 non-zero corrected-side instrument-months, and no map-excluded finding.** That is H-34's live re-fire condition, unchanged.

**But the amendment narrows the firing set close to a tautology, and this must be recorded.** Because SC-3(d) forbids side-independent output and the map's key is the per-cell availability ontology, a tool without a per-cell availability model cannot emit output in the vocabulary criterion 3 scores in — so it fails criterion 3 **by construction**, which is the same ground on which H-34's proxy fails it under criterion 1. The five-way conjunction collapses toward "is the rival built the way this project is built". That is a real defect. It is not un-fireability, and the two should not be conflated.

The second defect is dispositional: **§10.1 registers no third state.** "Partial satisfaction" is defined nowhere in the corpus, and a criterion that *could not be evaluated* is therefore indistinguishable from one *evaluated NO*. Both default to proceed. Given that criterion 3 has never actually been evaluated for any candidate, this is not hypothetical — it describes what already happened.

## 4. THE NARROWEST AMENDMENT

Report 2's bare-deletion draft is **rejected**. It cures the stated defect but leaves criterion 3 easier to satisfy than registered, and §0.2.1 forecloses that: "**An amendment weaker than the thing it amends is not one.**" Deletion is not available.

The narrowest amendment that cures the stated defect, weakens nothing, and touches no limb the stated reason does not reach:

> 3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;

Three properties. The contaminated limb is **byte-identical to registered v30**. The corrected limb is rewritten in SC-3's own three-disposition vocabulary, which is exactly what the retirement of line 461 requires. The ambiguity branch is carried **genuinely** byte-exact, em-dash included — which the current draft does not do.

The C2 retention block needs no change beyond deleting the words "The ambiguity branch is carried through unchanged" (true of this draft, false of the current one — keep it here, strike it there).

If the author wants the contaminated-side tightening on its merits, that is a defensible position — but it is **a second amendment with its own stated reason**, its own ledger row, and its own statement of effect on the re-fire condition. It is not this one.

## 5. WHAT MUST BE DISCLOSED BEFORE THE TAG

H-34 is committed, dated 12 August 2026, and its verdict is "the project proceeds." The following must appear on the face of v30a, not be discoverable only by reconstruction:

1. **That §10.1's criterion 3 is being changed after the kill gate was signed off**, with H-34's date and verdict named. §0.2.1's ex-ante rule makes the ordering the disclosable fact.
2. **That the change makes the kill gate harder to satisfy on net**, and specifically that the contaminated-side limb moves from existential to universal — the limb the stated reason does not reach. Either strike that change (§4 above) or state it and give it its own reason.
3. **That criterion 3 was never evaluated for any candidate under either text**, that §9.2's required comparison set was never committed and §9.2 never ran, and that H-34's operative test was a proxy for criterion 1 rather than the five-criterion scoring. The verdict survives all three; the record should not have to be reverse-engineered to learn them.
4. **Whether the kill gate is re-run under the amended criterion.** No clause in the composed amendment registers such an obligation, and H-34's re-fire condition triggers on a **new tool surfacing**, not on the **criterion changing**. Say which, expressly.
5. **The publication status of `declared_map.csv`.** It is the object criterion 3 now scores against and it is untracked. Either commit it at the v30a tag under SC-3(a)/SC-8(f) and name it in §11's enumeration, or state that criterion 3 is not third-party evaluable at the tag and when it will become so.
6. **That no registered clause supplies the candidate-output → cell-key join**, and that SC-7's scope over §10.1 candidates is unsettled. Both should be closed; at minimum both should be disclosed.
7. **A disposition for a criterion that could not be evaluated**, distinct from one evaluated NO, so "Partial satisfaction is recorded and does not trigger the stop" can no longer absorb both silently.
8. **The two textual corrections in this adjudication**: the ambiguity branch's punctuation change (and the two false byte-exactness claims), and the map's three-valued `scored_flag` — 888 / 24 / 72, with the 24 diagnostic rows' adjudication status stated rather than left to inference.

**NOT ESTABLISHED:** whether the contaminated-side tightening was intended; whether the fixture is distributable to a third party at all (no redistribution or licensing clause found — without one, criterion 3 is unevaluable by anyone but the author under *either* text); whether `declared_map.csv` will be committed at the v30a tag; whether the 24 diagnostic-class cells are scored by criterion 3; whether criterion 2 or criterion 4 was evaluated for any candidate other than `leak-detect`.