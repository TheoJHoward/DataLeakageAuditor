# PREREG.md v30a amendment — DRAFT DIFF, UNAPPLIED

**Status: UNAPPLIED. `PREREG.md` has not been edited by this item.** This file is a diff for author approval. Nothing here has been written to the repository, no git command that changes state has been run, and `AVAILABILITY_DECLARATION.md` has not been touched (R18: it remains the one live copy, edited only in place, by items authorized to do so).

**Form:** working resolution **R20**, form (ii') — a v30a amendments block near the top of `PREREG.md`; each amended clause carries an inline supersession marker naming v30a; **the new normative text lives inline in `PREREG.md`**, with the superseded text retained beside it marked superseded.

**Scope line applied to every sentence drafted below:** *would this still be true for a different fixture?* If yes it is a **RULE** and it belongs in `PREREG.md`. If no it is an **INSTANCE** and it belongs in `AVAILABILITY_DECLARATION.md`. Every hunk carries its rule/instance justification, and hunks 2 and 5 carry it sentence by sentence, as instructed.

**Source of every amendment:** the conformance walk, `AVAILABILITY_DECLARATION.md` §A (lines 751–1597), read in full. §A records **four §6.2 amendments (lines 445, 450, 451, 461)** in its summary at declaration line 1516, **plus** §A.6's criterion-1 denominator re-derivation (frozen separately as declaration §D.1 item 2) **plus** §A.12's "waived" definition. That is six. Nothing else in the walk is marked AMENDED — verified by scanning declaration lines 751–1600 for `AMENDED` / `class C` / `amendment`; every other entry is SATISFIED (§A.2, §A.5, §A.7, §A.9, §A.10, §A.6.5).

---

## (i) SUMMARY TABLE — every hunk

| Hunk | `PREREG.md` anchor | Line (today) | Anchor match count | Operation | Class | §A justification | Rule / instance justification |
|---|---|---|---|---|---|---|---|
| **H1a** | status line | **6** | **1** (exact line and substring) | INSERT 1 line after | — | §A.0, §A.11 | Navigation marker. Names the amendment and the recovery command; asserts no semantics. |
| **H1b** | `**Registration:** …` header line | **8** | **1** | INSERT 29 lines after | — | §A.0 (declaration 760–767), §A.11 (1516–1521) | The amendments block itself: a rule about how this registration is amended and where rules vs instances live. Fixture-independent. |
| **H2** | `- **Reference AUC:** 0.957 and 0.675, …` | **445** | **1** | REPLACE (1 → 4 lines) | **C** | **§A.1** (771–818) | RULE = how a reference anchor is constituted and what tolerance governs. INSTANCE = the trio, the horizons, the model family, the row counts. |
| **H3** | `- **Contamination availability class** recorded in the manifest.` | **450** | **1** | REPLACE (1 → 4 lines) | **C** | **§A.3** (882–934) | RULE = where a declaration may be recorded and why an evidence artifact may not be the locus. INSTANCE = the declared class and its mechanism. |
| **H4** | `- **Sliced variant** for CI, …` | **451** | **1** | REPLACE (1 → 4 lines) | **C** | **§A.4** (938–984) | RULE = which artifacts the acceptance criteria are evaluated on, when the slice obligation falls due, and how a slice is scored. INSTANCE = none yet (no slice exists). |
| **H5** | `3. **No runtime finding of any tier, primary or secondary**, appears on \`fixture_corrected\`.` | **461** | **1** | REPLACE (1 → 9 lines) | **C** | **§A.8** (1407–1434), working resolution R9 (declaration 3671) | RULE = findings are scored against a declared map; three dispositions; neither side assumed clean. INSTANCE = the map itself, the 18/48 incidence, the 72 unscored cells. |
| **H6** | `Secondary findings on **manifest-listed descendants** …` | **464** | **1** | INSERT 37 lines after | **C** | **§A.6** (1020–1045), **§A.6.0** (1047–1145), §A.6.4 (1257–1269), **§A.10** (1474–1492), working resolution R11 (declaration 3677–3682) | RULE = how the criterion-1 denominator is constituted, the three-class partition rule, the publication and reporting constraints. INSTANCE = the 35-column set, the 11 / 22 / 2 enumeration, `ts_floor`, the named columns. |
| **H7** | `   The replacement may be stricter than the floor …` | **1035** | **1** | INSERT 17 lines after | **C** | **§A.12** (1525–1597) | RULE, entirely. Defines a word in a locked floor. No fixture appears in it. |
| **H8** | `\| **Detector-case coverage** \| …` | **855** | **1** | INSERT 3 lines after the table | — (pointer) | **§A.12** (1539–1544, 1571–1573) | RULE. Cross-reference only; adds no permission and invents no entry condition. |
| **C1** | Phase 1 row of §10's phase table | **992** | **1** | REPLACE (1 → 1 line) | **C (consequential)** | derived from §A.1 + §A.4 — **not itself walk-cited** | Stale inbound reference to two superseded clauses. **AUTHOR ADJUDICATION REQUIRED.** |
| **C2** | `3. Fires on \`fixture_contaminated\` and is silent on \`fixture_corrected\` …` | **1022** | **1** | REPLACE (1 → 1 line) | **C (consequential)** | derived from §A.8 — **not itself walk-cited** | Second copy of the superseded clean-corrected premise, in the §10.1 kill gate. **AUTHOR ADJUDICATION REQUIRED.** |

**Anchor verification.** Every anchor above was matched against the live `PREREG.md` (1099 lines, ends with a newline) both as an **exact full line** and as a **substring**: **all eleven return match count 1.** The applier refuses to run if any anchor matches zero or more than one line.

### Lines of `PREREG.md` the amendment touches

| | Anchor points | Lines modified in place | Lines added | Total line-level changes |
|---|---|---|---|---|
| **Core amendment (H1a–H8)** | 9 | **4** (445, 450, 451, 461) | **104** | **108** |
| **With consequential C1 + C2** | 11 | **6** (+992, +1022) | **104** | **110** |

File length goes from **1099 → 1203 content lines** (+104). C1 and C2 are one-line-for-one-line replacements and add no lines.

Per hunk: H1a +1 · H1b +29 · H2 1→4 (+3) · H3 1→4 (+3) · H4 1→4 (+3) · H5 1→9 (+8) · H6 +37 · H7 +17 · H8 +3 · C1 1→1 · C2 1→1.

### Mechanical verification performed (on a scratch copy; the live repo was not touched)

The whole repository was copied to `…/scratchpad/amendment/_verify/repo`, the hunks applied there by `…/scratchpad/amendment/apply_v30a.py`, and the registration tooling run against the patched copy:

- `python tools/check_registration.py --stage prereg` → **RESULT: PASS, exit 0** (all 13 prereg-stage checks pass; the two declared banned-vocabulary exemptions still resolve). This is the tag gate of §6.8.
- `python -m pytest tests/registration -q` → **137 passed**, including `test_prereg_stage_on_real_repo_exits_zero`.
- Both runs repeated **with C1 and C2 included**: also PASS / 137 passed.

Four checker-facing facts worth recording, because each was a plausible way for this amendment to break CI silently:

1. **No banned term is introduced.** The v30 banned list is `capability matrix`, `noise floor`, `routing policy`, `comparison_mode`, `statistical mode`, `substituted gate`; the new text contains none, and no retained superseded line contains one either.
2. **`_prereg_version()` still reads 30.** It matches `**Status:** v(\d+)`; H1a adds a *separate* line and leaves line 6 byte-exact, so the ledger-note historical test (`v` < current) behaves exactly as at v30. This is the reason H1a does not rewrite the status line.
3. **`check_phase_arithmetic` is unaffected by C1** — it parses the phase table's *estimate* cell (`2–3 wknds`), which C1 does not touch.
4. **`sections_of()` gains no section.** The new `## v30a amendments (class C under §0.2.1)` heading does not match the numbered-heading regex `^#{2,4}\s+\d+(\.\d+)*`, so no section numbering shifts and `check_requirement_ids`' section lookups are unchanged. No requirement-ID-shaped token (`R\d+…-CAPS`) is introduced.

---

## (ii) THE HUNKS

Application convention below: **ANCHOR** is the exact line as it stands in `PREREG.md` today. **REPLACE** substitutes the anchor line with the block shown. **INSERT AFTER** leaves the anchor line untouched and inserts the block on the following line.

---

### H1a — amendment marker, immediately after the status line

**ANCHOR — `PREREG.md` line 6, match count 1:**

```
**Status:** v30 — supersedes v1–v29. Committed together with `DESIGN.md` v26 and `HISTORY.md`. **The last version under the self-imposed cap. Everything after this routes through §0.2.1's class A/B/C machinery, which is what it was built for.**
```

**SUPERSEDED TEXT: none.** Line 6 is a true statement about v30 and is **retained byte-exact**. It is not rewritten to say "v30a" — partly because it is a historical status, and partly because `tools/check_registration.py::_prereg_version` parses it.

**INSERT AFTER (1 line):**

```
**Amendment status:** **v30a — this file is amended.** Six class C changes under §0.2.1, listed in the v30a amendments block below. The v30 text of every amended clause is retained inline, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text byte-exact.
```

**Rule/instance:** navigation, no semantics. **§A citation:** §A.0 (declaration 760–767) for the class, §A.11 (1516–1521) for the count of six.

---

### H1b — THE v30a AMENDMENTS BLOCK

**ANCHOR — `PREREG.md` line 8, match count 1:**

```
**Registration:** committed unchanged as `PREREG.md` at first commit, before any detector code is written. See §11.
```

**SUPERSEDED TEXT: none.** This is an insertion.

**Placement note for the author.** The instruction was "after the status line". The block is placed after **line 8** — i.e. after the four-line metadata header (Working name / Author / Date / Status / Shape / Registration), before the `---` on line 10 — so that the v30 metadata lines stay contiguous and byte-exact, with the pointer of H1a sitting directly under the status line itself. Moving the block up two lines, to sit literally between line 6 and line 7, is a one-token change in the applier and breaks nothing.

**INSERT AFTER (29 lines):**

```
---

## v30a amendments (class C under §0.2.1)

**What this block is.** `prereg-v30a` is an **amended registration, not a restart** (§0.2.1, line 95). It carries six class C changes. Each was produced by the element-by-element conformance walk of the acceptance fixture's reconstructed availability declaration against §6.2 — `AVAILABILITY_DECLARATION.md` §A — and each hunk below cites the walk section that justifies it. That file is the reconstructed declaration §6.2 already requires and the carrier of this fixture's evidence. **It is not a normative annex and may not be cited as one.** Measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule). What lives there is this fixture's *instances*: its identity, its measured ground-truth map, its reference-anchor values, its evidence, its documented-unverifiable assumptions, and the per-column enumeration these rules yield for it.

**The test applied to every sentence below, so the split is checkable rather than asserted:** *would this still be true for a different fixture?* If yes it is a **rule** and it is here. If no it is an **instance** and it is in the declaration.

**How the amendment is written, so nothing is lost.**

1. **The superseded v30 text is retained inline, verbatim, in a block marked `SUPERSEDED BY v30a` and marked NOT operative.** No registered sentence is deleted from this file.
2. **Each amended clause carries an inline supersession marker naming v30a**, and the new normative text sits beside the old.
3. **The registered text is recoverable byte-exact independently of this file: `git show prereg-v30:PREREG.md`.** The retained inline copies are a reading convenience; the signed `prereg-v30` tag is the record.
4. **This amendment inherits §11's integrity chain in full** (§0.2.1, line 97): signed tag, file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock.

| # | Clause amended | Class | `AVAILABILITY_DECLARATION.md` §A justification | What it changes |
|---|---|---|---|---|
| 1 | §6.2 — reference AUC anchor | C | §A.1 | Retires the registered anchor pair; an anchor is henceforth **constituted by recomputation** from the fixture's stored per-row predictions, with the ±0.010 interval retained as an upper bound. |
| 2 | §6.2 — contamination availability class | C | §A.3 | Moves the **recording locus** from the manifest to the fixture's availability declaration, which the tag hashes; an evidence artifact may not be the locus of a declaration. |
| 3 | §6.2 — sliced variant for CI | C | §A.4 | Moves the sliced variant **off the Phase 0 acceptance fixture** and re-registers it as a Phase 1 CI obligation with its scoring rule declared ex ante. |
| 4 | §6.2 — criterion 3 | C | §A.8 (working resolution R9) | Replaces "no finding on the corrected side" with **scoring against a declared ground-truth map**; neither side is assumed clean. |
| 5 | §6.2 — criterion 1's denominator, and the scored-set partition rule | C | §A.6, §A.6.0–§A.6.4, §A.10 (working resolution R11) | Adds the rule constituting the denominator — derived from the declared map, three classes, each **enumerated by name**, never a residue or a bare count. Criterion 1's registered text itself stands unchanged. |
| 6 | §10.2 — the word "waived" in the replacement-criterion floor | C | §A.12 | Adds the **missing defining clause** to a floor that used the word without one. Changes no threshold and grants no permission. |

**All six are class C under §0.2.1 line 93** — each changes what a published number means, or what an acceptance criterion requires — **and are carried by this registration under line 95.** None is a `DEVIATIONS.md` entry standing alone.

**What an amendment may not do, restated here because this is the first one.** It may not be weaker than the thing it amends (line 97). It may not convert an unmet element into a satisfied one by re-reading it. Where an element cannot be met as written at the instant the amendment must be committed, it is **amended explicitly, never waived and never left outstanding** — which is what amendment 3 does.
```

**Rule/instance:** every sentence is fixture-independent. The block names the declaration as the carrier of instances and evidence and **explicitly refuses the "normative annex" framing** (R20). The only fixture-adjacent words — "this fixture's instances" — describe a location, not a value.

---

### H2 — §6.2 reference AUC anchor

**ANCHOR — `PREREG.md` line 445, match count 1:**

```
- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.
```

**§A justification:** **§A.1** (declaration 771–818), which quotes line 445 verbatim at 778, states the OLD at 780–781, the NEW at 783–793, and the three reasons at 795–816. Declaration §D.1 item 3 (3394) freezes the replacement entries. The `full` mode clause is preserved by §A.1's own closing sentence (818).

**REPLACE with (4 lines).** The superseded text is retained verbatim inside a nested quote on the second line, so the bullet list structure of §6.2 is preserved and the registered sentence remains greppable:

```
- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair on both sides (§A.1 item 1) — that fact, and the replacement entries themselves, are instances and are recorded in the declaration. **The clause "and because the anchor's model family changed" stood here until R55/W5 and is struck: it is false against its own cited source, which names six architectures with LightGBM listed first, and §A.1 item 2 was corrected on 21 August 2026 to say so.** Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

**Rule vs instance, sentence by sentence** (as instructed):

| Sentence of the new text | Side | Why |
|---|---|---|
| "The anchor is constituted by recomputation, not by transcription." | **RULE** | True of any fixture with stored predictions; it says what kind of object an anchor is. |
| "…computed from the fixture's own stored per-row prediction and outcome columns…" | **RULE** | Names the source *kind*, not the file. |
| "…declared … as an enumerated set of entries, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows…" | **RULE** (the requirement to enumerate and to name provenance) | The *entries themselves* are the instance; the obligation to publish them enumerated with provenance is fixture-independent, and matches §8.6. |
| "Where the fixture is of the re-evaluation class … the recomputation is authoritative over any figure recorded in a prior report." | **RULE** | Defines a fixture class by a property (stored predictions vs a training procedure) and attaches a precedence rule to it. §A.1 reason 3 (809–816) is exactly this argument. |
| "A lower-precision recorded figure that agrees is a secondary record … one that disagrees is a defect … never a competing anchor." | **RULE** | Disposition of a conflict between two records of one quantity. |
| "The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened." | **RULE** | Tolerance is a rule. **Drafting note below.** |
| "…a deviation approaching the interval indicates a defect … stop-and-report, not a pass." | **RULE** | Consequence attached to an exactly-reproducible quantity. |
| "The gate runs in `full` mode." | **RULE** | Carried unchanged from line 445 per §A.1's line 818. |
| "A report quoting an anchor entry names its model family and horizon…" | **RULE** | Reporting obligation, fixture-independent. |
| **0.966244 / 0.931536 / 0.939968 / 0.756504 / 0.856419 / 0.679288; 5s/10s/30s; 1,047,430 / 655,016 / 745,656; LightGBM; XGBoost→LightGBM; `f1\f1_results.csv` rows 50–52 and 114–116** | **INSTANCE — stays in the declaration §A.1** | None of it is true of another fixture. It is already there, and frozen by §D.1 item 3. |

**One drafting choice, flagged for the author.** §A.1 says the anchor is "retired and replaced" and is silent on what tolerance governs the replacement. The draft **retains ±0.010 absolute and forbids widening it**. Basis: §D.3's rule that an interpretation of locked text may resolve only toward the stronger reading — retaining a registered bound is stronger than dropping it. The alternative reading (the interval was part of the retired object and dies with it) would leave the replacement anchor with no tolerance at all, which is weaker. **This is a drafting choice, not a walk citation.** If the author prefers a tighter bound for an exactly-reproducible quantity — for example "reproduces to the stated precision, with ±0.010 as an absolute ceiling" — that is a one-sentence change here and needs no other hunk.

---

### H3 — §6.2 contamination availability class

**ANCHOR — `PREREG.md` line 450, match count 1:**

```
- **Contamination availability class** recorded in the manifest.
```

**§A justification:** **§A.3** (declaration 882–934). OLD quoted at 904–905, NEW at 907–909, the three "why this is not weaker" arguments at 911–927, and the explicit limits at 929–934. Declaration §D.2 (3460–3463) records the lock-time obligation as discharged **by amendment, not by editing the manifest**.

**REPLACE with (4 lines):**

```
- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*
```

**Rule vs instance.** RULE: the locus requirement, the tag-hash requirement, the prohibition on an evidence artifact carrying a declaration, the requirement that the class be recorded with mechanism + incidence + enumeration, and the explicit non-generalization ("this clause moves the locus of one element and nothing else"). INSTANCE, staying in the declaration: the declared class itself (`AVAILABILITY VIOLATION BY FORWARD JOIN`), the `ts_floor` mechanism, and the measured incidence in §14 and §C.

**Note on the sixth hash.** The new text says "hashed in the amended registration's tag message" without stating a count. The count is settled by declaration §D.2 and working resolution R7 as a **class A mechanical fact requiring no locked-file edit**; see §(iii) item 10 below. If the author rejects that class A call, §11 item 3 needs its own hunk — this one does not create the obligation and does not depend on the count.

---

### H4 — §6.2 sliced variant

**ANCHOR — `PREREG.md` line 451, match count 1:**

```
- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.
```

**§A justification:** **§A.4** (declaration 938–984). Measured state at 944–945; the structural unsatisfiability argument at 947–956; OLD at 958–959; the three binding parts of NEW at 961–974; "why class C" at 976–978; limits at 980–984. Declaration §D.1 item 5 freezes it; §D.2 (3464–3467) discharges the lock-time obligation and carries the Phase 1 obligation forward explicitly.

**REPLACE with (4 lines):**

```
- **Sliced variant — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.4). **The sliced variant is not part of the Phase 0 acceptance fixture.** It is a **Phase 1 CI obligation, due at the first CI run that exercises the padded slicer and before any user-facing slice auditing is published**, produced by that same padded slicer, with its slice boundaries declared. **Its scoring rule is declared now, ex ante, so it cannot be chosen after a result is seen:** a slice inherits the ground-truth-map cells its rows select and is scored against those cells under criterion 3 as amended — findings the selected cells predict are required, findings they exclude are false positives, cells the map does not cover are unscored. **A slice of a characterized side is never treated as clean, and a slice may not be reported as a pass on the strength of containing only unscored cells.** The obligation is not deletable by a `DEVIATIONS.md` entry or by a decision-log interpretation; dropping it is a further class C amendment. **Why it is amended rather than left outstanding:** the registered clause requires an artifact produced by a component of the tool under development, while §0.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly — leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure mode §2.7 exists to stop.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing."
  >
  > *The variant is moved and re-registered, not deleted: slice auditing is not dropped and the slicer is not exempt from CI.*
```

**Rule vs instance.** Entirely RULE — which artifacts the acceptance criteria are evaluated on, when the obligation falls due, how a slice is scored, and what may not discharge it. There is no instance: no sliced artifact exists, which is precisely §A.4's argument. The clause deliberately does **not** name this fixture's stored-prediction pair as "the fixture" in `PREREG.md`; §A.4 part 1 does that, and the identity of the fixture is an instance (declaration §8).

---

### H5 — §6.2 criterion 3, map-scored (R9)

**ANCHOR — `PREREG.md` line 461, match count 1:**

```
3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.
```

**§A justification:** **§A.8** (declaration 1407–1434). Registered text quoted at 1411; OLD and NEW quoted verbatim from R9 at 1413–1417; rationale at 1419–1421; "what forced it" (the M5 falsification sweep, 18 of 48 instrument-months, up to 111,334 of 580,944 rows) at 1423–1429; limits at 1431–1434. Working resolution R9 verbatim at declaration 3671. Frozen by §D.1 item 5.

**REPLACE with (9 lines).** The numbered-list item is preserved as item 3 and the superseded text sits in an indented quote inside the same list item, so criterion 4 does not renumber:

```
3. **Runtime findings on both fixture sides are scored against the fixture's DECLARED GROUND-TRUTH MAP — v30a, operative** (supersedes the registered criterion 3 quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.8, working resolution R9). The map is declared in the fixture's availability declaration and **frozen before any detector runs**. It is stated **per side, per declared violation class, and per declared map cell** — the cell key is the unit the declaration declares the fixture to be partitioned into, and the declaration names it. Three dispositions, mutually exclusive and exhaustive over the map:
   - **A finding the map predicts is REQUIRED.** Its absence is a miss.
   - **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on either side, at any tier, primary or secondary.
   - **A cell the map does not cover is UNSCORED.** It requires no finding and forbids none, enters no denominator, contributes to no rate, and **is never reported as a pass.**

   **Neither side is assumed clean.** The corrected side of a fixture is **CHARACTERIZED, never clean**, and no report may describe it as clean. This is the tool's own coverage principle — silence and belief never convert into a pass (§2.7, §8.1) — applied to the tool's own exam. **The amendment does not lower the bar:** a finding on a cell the map marks zero is still a false positive and still fails the gate, and the unscored disposition is not an escape hatch — unscored cells are named as unscored, never as clean, and they license no pass.
   > **SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:** "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`."
   >
   > *Retired because measurement falsified its premise: the corrected side of the declared fixture carries real, strictly-post-decision violations, so the registered criterion would fail the gate on a correctly-behaving detector reporting a violation the fixture really contains. The measured incidence is an instance and is recorded in the declaration.*
```

**Rule vs instance.** RULE: the scoring principle, the three dispositions, the freeze-before-any-run requirement, "never a pass" for unscored, "CHARACTERIZED, never clean", and the two non-weakening clauses. INSTANCE, staying in the declaration: `n1\declared_map.csv` and its 984 rows, the 18-of-48 corrected-side incidence, the 111,334/580,944 maximum, the 72 unscored cells, and the class names (`trades_*`, `mbo_*`).

**GENERALIZATION MADE, AND WHY.** R9's verbatim text says **"per-side, per-class, per-instrument-month"**. "Instrument-month" fails the scope-line test — it is this fixture's cell key and would be meaningless for a fixture with a different partition. The rule is therefore drafted as **"per side, per declared violation class, and per declared map cell — the cell key is the unit the declaration declares the fixture to be partitioned into, and the declaration names it."** The generalization is *only* on the third axis; "per side" and "per class" are carried across unchanged. The concrete key for this fixture — instrument-month — is an instance and is already declared (declaration §13). **The obligation that the declaration name its cell key explicitly is what keeps the generic form from being weaker than R9's:** without it, "per declared map cell" could be read as licensing an undeclared, post-hoc cell definition. R9's own text is quoted verbatim in the declaration at 1415–1417 and remains the audit trail.

---

### H6 — criterion 1's denominator (R11) and THE PARTITION RULE

**ANCHOR — `PREREG.md` line 464, match count 1:**

```
Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.
```

**SUPERSEDED TEXT: none — and this is the load-bearing fact about this hunk.** §A.6 marks criterion 1 **SATISFIED** (declaration 1020, 1034). **`PREREG.md` line 459 stands byte-exact.** What v30a adds is the rule that constitutes its *denominator*, which the registered text left to be inferred — and the inference the earlier draft made (the manifest's independently-leaking-source count) is the contradiction the P2 verifier found (declaration 1036–1041). Placement after line 464 keeps the four criteria contiguous and puts the derivation immediately after the descendants sentence it interacts with.

**§A justification:** **§A.6** (1020–1045) for the denominator's source and the three-class requirement; **§A.6.0** (1047–1145) for the derivation rule and its three reading notes; **§A.6.3** (1247–1255) for the "unconstructible" reading; **§A.6.4** (1257–1269) for the partition check; **§A.6.5** (1285–1296) for the mechanism the rule turns on; **§A.10** (1477–1489) for the per-class reporting obligations; **§A.6.1** (1178–1188) and **§C.5** for the one-class / right-column-wrong-ground rule; working resolution **R11** verbatim at declaration 3677–3682; frozen by **§D.1 item 2** (3374–3390).

**INSERT AFTER (37 lines):**

```

**The criterion-1 denominator, and the partition rule that constitutes it — v30a** (`AVAILABILITY_DECLARATION.md` §A.6, §A.6.0–§A.6.4 and §A.10; working resolution R11). **Criterion 1 above stands exactly as registered.** What follows states how its denominator is constituted, which the registered text left to be inferred.

**The denominator derives from the declared ground-truth map, not from a manifest's construction classes.** A manifest's leak-source classification says how a column was *built*; criterion 1 asks what the map *declares violating* on the scored side under the declared `ties` branch (§2.3). Those are different questions and they do not in general have the same answer. **The count of independently leaking sources is manifest content and provenance context; it carries no gate arithmetic and is not N.** Any report quoting a leaking-source count names the scope it counts under.

**Every column of the fixture's declared scored set is placed in exactly one of three classes.** The classes are mutually exclusive and exhaustive over that set:

| Class | What it is | What a finding on it means |
|---|---|---|
| **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
| **OUT OF JURISDICTION** | declared availability-legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
| **UNSCORED** | scoring on it is declared impossible | counts **neither for nor against** any criterion; reported as an unscored observation |

**N is the length of the REQUIRED list.** Three constraints on how the partition is published, and they are the point of the rule:

1. **Each class is published as an enumerated list of column names.** A class stated as a bare count is not auditable and does not satisfy this.
2. **No class is defined as a residue.** "Everything else" is not a class definition; each column's membership is derived by the rule below and shown.
3. **The partition check is printed and reproducible by any gate report:** the three class sizes sum to the size of the declared scored set, no column appears in two classes, and no column of the set is missing from all three. A report that cannot reproduce the check has not scored the fixture.

**Reporting, per class, and never folded together** (§8.6): the descriptive proof count of this section is published as **k of N REQUIRED columns**, naming N; **false positives are reported against the OUT OF JURISDICTION class and no other** — that class alone bears the false-positive consequence; and findings on UNSCORED columns are reported as unscored observations, which are **not** false positives.

> **THE PARTITION RULE.** A column's class is **derived, not assigned**. Given the fixture declaration's decision instant, `ties` branch, and join keys:
>
> - **REQUIRED** iff its construction carries a **join whose window completes strictly after the decision instant of the row the aggregate is attached to** — the availability-violating join the declaration names — **and** it is **not degenerate-constant** on the fixture.
> - **OUT OF JURISDICTION** iff its construction reads **only values whose availability times are legal at the boundary instant under the declared `ties` branch** (§2.3) — that is, it carries no such join, and every constituent read is legal at its own timestamp.
> - **UNSCORED** iff it is **degenerate-constant** on the fixture, **or** its gate status is declared **EXCLUDED** because its construction is not verifiable from the fixture's own code.

Three reading rules fix the rule's edges. Each closes a hole measurement actually found, and each is part of the rule rather than a gloss on it:

- **Precedence: UNSCORED wins.** A column satisfying an UNSCORED limb and another class's clause is UNSCORED. (The REQUIRED clause is a conjunction, so a degenerate-constant column is already outside it without appeal to precedence; precedence is load-bearing for a column that is fully availability-legal *and* declared EXCLUDED.)
- **"Reads only same-row values" is read as "reads only within-lattice values", not literally one row.** A lagged read of the same column at another timestamp of the same lattice carries no cross-source join, and each constituent read is legal at its own timestamp; such a column is OUT OF JURISDICTION.
- **"Not constructible" means gate status EXCLUDED on the artifact the gate actually scores** — never "not reconstructible in some other rebuild of the fixture". Reading a rebuild's unconstructibles as gate-unscored silently drops columns out of the arithmetic in both directions.

**A column carries one gate class and one only** — §0.2.1's rule that no field answers two questions, applied to gate classes. Where a column has two grounds, one violating and one legal, **the gate class follows the violating ground**; the legal ground is recorded as a fact and not applied; and **a finding on the legal ground does not satisfy the REQUIRED entry.** Naming the right column on the wrong ground does not satisfy criterion 1.

**Re-derivation is mandatory, and moving a column is an amendment.** If a column's construction changes, or a column declared EXCLUDED becomes constructible, its class is re-derived by this rule. **Moving a column between classes, or changing N, after the tag is a class C amendment.** The declaration's enumeration is the current output of this rule and is never a substitute for it.
```

**Rule vs instance, clause by clause:**

| Clause | Side | Why |
|---|---|---|
| "derives from the declared map, not from a manifest's construction classes" | **RULE** | How a denominator is constituted — the scope line's own example of a rule. |
| "the count of independently leaking sources … carries no gate arithmetic and is not N" | **RULE** | What a published number means. Note it does **not** amend line 446; the count stays in the manifest, its *arithmetic role* is what is constrained. |
| the three-class table and their scoring consequences | **RULE** | What a state means. §A.10's three reporting consequences are stated here because they are what the classes *do*. |
| "N is the length of the REQUIRED list" | **RULE** | Definition of N. **N = 11 is the INSTANCE** and stays in declaration §A.6.1 / §D.1 item 2. |
| the three publication constraints (enumerated by name, no residue, printed partition check) | **RULE** | Auditability requirements, fixture-independent. §A.6's line 1044: "a count that cannot be written out as a list is a count nobody can audit." |
| the per-class reporting rule | **RULE** | §8.6 already requires provenance on published numbers; this says which denominator each class feeds. |
| **THE PARTITION RULE** (the three iff-clauses) | **RULE** | §A.6.0 states it as a rule explicitly: "stated verbatim so it can be re-applied when a column changes construction" (1050). |
| the three reading rules | **RULE** | §A.6.0's own three reading notes (1062–1085), which it calls part of the rule. |
| one-class-only and right-column-wrong-ground | **RULE** | §A.6.1's `vwap_distance` note and §C.5; grounded in §0.2.1's existing no-two-questions rule, applied rather than restated. |
| re-derivation and the class C consequence | **RULE** | §A.6.0's closing sentence (1142–1145) and §D.1 item 2's closing sentence. |
| **the 35-column set; REQUIRED 11 / OUT OF JURISDICTION 22 / UNSCORED 2; `ts_floor`; `net_delta_*`, `vwap_distance`, `buy_volume_10s`, `book_imbalance_ratio`; the `trades_*` classes; 11+22+2=35** | **INSTANCE — declaration §A.6.1–§A.6.4, frozen at §D.1 item 2** | None survives a change of fixture. |

**GENERALIZATIONS MADE, EACH STATED WITH ITS BASIS** (per the instruction not to hard-code `ts_floor` or 35, and not to over-generalize beyond what the walk supports):

1. **`ts_floor` → "a join whose window completes strictly after the decision instant of the row the aggregate is attached to".** Basis: §A.6.5's mechanism paragraph (1285–1294) states exactly this and derives the class from it — "attaches to row `T` an aggregate over `[floor(T), floor(T)+1s)`, whose true availability instant is `floor(T)+1s`, strictly after `T`." The general form is the walk's own stated mechanism with the fixture's second-granularity stripped out. The rule adds "the availability-violating join the declaration names" so the join cannot be identified post hoc.
2. **"the 35 fed columns" → "the fixture's declared scored set".** Basis: §A.6.4 ties the total to the declaration's own `total_fed_to_phase7`, i.e. to a declared quantity, not to the literal 35.
3. **"same-row book/clock values" → "values whose availability times are legal at the boundary instant under the declared `ties` branch".** Basis: §A.6.0's second reading note (1075–1079) explicitly rejects the literal single-row reading and grounds legality in R1's `ties: available` and `PREREG.md` 190–197 — which is §2.3, cited in the new text.
4. **"unconstructible under T4" → "gate status declared EXCLUDED because its construction is not verifiable from the fixture's own code".** Basis: §A.6.0's third reading note (1080–1085) and §A.6.3's closing paragraph (1247–1255), which insist on precisely this reading and name the two columns that would otherwise be dropped.

**NOT generalized, deliberately:**

- **The "degenerate-constant" limb is kept verbatim.** It is already fixture-independent and the walk gives no wider formulation.
- **The rule is stated for a column-level scored set only.** The walk derives it over columns; the map's cell level is handled by criterion 3 (H5), where the walk puts it. Extending the partition rule to rows or cells would go beyond §A.6.0.
- **No fourth class, and no "residue" class.** §A.6.5's closing paragraph (1383–1384) forbids exactly that.

---

### H7 — §10.2, "waived" defined

**ANCHOR — `PREREG.md` line 1035, match count 1** (note the three leading spaces — it is inside criterion 2's indented block):

```
   The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.
```

**Context, `PREREG.md` line 1033 (quoted here, unchanged by this diff), which is what that floor floors:**

> On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**SUPERSEDED TEXT: none.** §A.12 is explicit (declaration 1528–1529): "It adds a defining clause to a locked floor that uses the word without one; it changes no threshold, exempts nothing, and narrows nothing." The floor stands byte-exact; the definition is inserted immediately after it.

**§A justification:** **§A.12** (declaration 1525–1597). The gap statement at 1539–1544 (including that "waived" appears a second time, undefined, at `PREREG.md` line 855); the definition at 1546–1556; "what invoking it requires" at 1558–1564; the seven non-permissions at 1566–1592; status and the stronger-reading rule at 1594–1597. Frozen by §D.1 item 5.

**INSERT AFTER (17 lines), preserving the three-space indentation of criterion 2's block:**

```

   **"Waived", defined — v30a** (`AVAILABILITY_DECLARATION.md` §A.12). The floor above uses the word without a defining clause, and the word appears once more as a detector-case coverage state in §7.7's table, also undefined. An undefined term inside a floor whose purpose is to stop criteria being dropped silently is exactly the term that gets read permissively later. **This adds the defining clause. It changes no threshold, exempts nothing, and grants no permission.** The two runtime detectors the floor governs are **L2a and L3.1**.

   > A runtime detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or reported in any way that makes the detector's own result incapable of changing the criterion's outcome. Concretely, a detector is waived if any of the following holds: **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty for a pass, so its contribution is optional; **(iii)** the criterion can be satisfied by the other detector's output alone; **(iv)** its threshold is set at a level it meets without executing, or by construction; or **(v)** its cases are reported under §7.7's `waived` coverage state rather than executed to a terminal result.

   **What invoking it requires: nothing, because it may not be invoked.** The floor is a **prohibition, not a permission with conditions**. There is no procedure by which either runtime detector may be waived in a replacement criterion. A replacement criterion that waives one is weaker than the floor and is out of specification on its face; it does not become admissible by being recorded, disclosed, justified, or approved. Changing that requires amending the floor itself — a further class C amendment, committed and timestamped before the affected detector is implemented or evaluated (§0.2.1).

   **What this definition does NOT permit — stated so it cannot be read as a general escape:**

   1. **It is not an escape hatch of any kind.** It creates no exception, no justified waiver, no reviewer-approved waiver, no time-limited waiver. It exists only to make a prohibition checkable.
   2. **It does not reach any other criterion.** It defines the word for this floor and for §7.7's coverage state. It says nothing about §6.2's acceptance criteria and may not be cited to soften them.
   3. **"Experimental" is not "waived", and may not become it.** Criterion 3 below can ship a detector or mode marked experimental and exclude it from `assert_no_proven_leakage()`. That changes how findings are *labelled and asserted on*; it does not remove the detector from a replacement criterion's denominator. A criterion that drops a detector *because* it was marked experimental has waived it.
   4. **"No data" is not "waived".** A cell with no data is **unscored**: ledgered by name, entering no denominator, contributing to no rate, and never reported as a pass. The detector is still scored wherever data exists. Converting an unscored cell into a pass is the failure the amended §6.2 criterion 3 names; doing it at the level of a whole detector is a waiver.
   5. **A working resolution or a `DEVIATIONS.md` entry cannot do it.** The clause above forbids a `DEVIATIONS.md`-only criterion outright, and an interpretation of locked text may resolve only toward the stronger reading.
   6. **Per-combination waiving is still waiving.** Criterion 3 below applies its gates per combination; dropping a detector from one combination's criterion while scoring it in another waives it for that combination, and is class C.
   7. **It licenses nothing after tuning.** The whole floor exists ex ante — as the floor's own closing sentence says, a criterion chosen because it works after tuning is a criterion shaped by tuning.
```

**Rule vs instance.** Entirely RULE — the word appears in a locked floor and the definition is fixture-independent. No fixture, column, map, or number appears in it. Two adaptations from §A.12's wording, both to keep the text local to `PREREG.md`:

- §A.12 item 5 cites the declaration's §D.3; the drafted item 5 states the substance (a decision-log interpretation may resolve only toward the stronger reading) and cites `PREREG.md`'s own line 1033 for the `DEVIATIONS.md` prohibition, so the clause does not make `PREREG.md` depend on a rule that lives only in the declaration. See §(iii) item 13 for the open question this raises.
- §A.12 item 4 cites declaration §13(g)/§A.6.3 for the unscored ledger; the drafted item 4 cites the amended §6.2 criterion 3 instead — the rule, not the instance.

---

### H8 — §7.7 vocabulary table pointer (recommended; adds no normative content)

**ANCHOR — `PREREG.md` line 855, match count 1:**

```
| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |
```

**SUPERSEDED TEXT: none.** The table row is unchanged; the block is inserted after the last row of the table (line 856).

**§A justification:** §A.12's gap statement, declaration 1540–1542 — "It appears once more, at PREREG.md line 855, as a **detector-case coverage state** in §7.7's vocabulary table — also undefined" — and 1571–1573, where the definition is scoped to cover it.

**INSERT AFTER THE TABLE (3 lines):**

```

**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.

```

**Why the second sentence is drafted the way it is — REVISED, DELTA R35/B3 and R37/D8.** The earlier draft recorded a residual gap: §A.12 defines what *being waived* means and supplied no entry condition for §7.7's coverage state, and inventing one would have exceeded the walk. **That gap is closed by this amendment.** SC-12(w) registers the entry condition — a prohibition with a closed and empty list of licensed grounds — so the pointer now names it instead of reporting its absence. The superseded sentence asserted the condition did not exist; leaving it standing would have shipped two registered texts disagreeing at the exact site of the defect being fixed.

---

### C1 — CONSEQUENTIAL, AUTHOR ADJUDICATION REQUIRED — §10's Phase 1 gate cell

**ANCHOR — `PREREG.md` line 992, match count 1** (long single-line table row):

```
| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |
```

**The problem, stated precisely.** This is the **only other place in `PREREG.md`** where the retired anchor and the moved sliced variant are relied on. The Gate cell says *"both fixture AUCs reproduce within ±0.010, full and sliced"* — **"both"** is the retired pair (H2 replaces it with an enumerated entry set of unstated cardinality), and **"sliced"** is the artifact H4 moves off the Phase 0 fixture and re-registers as a CI obligation of this very phase. Left unamended, `PREREG.md` would carry a Phase 1 gate that no longer names an existing object, which is §0.2.1's "two copies, drifted" shape and is what §6.8's deletion-certificate rule ("a deletion is not complete until the symbol's inbound normative reference set is empty") exists to prevent.

**Why it is flagged rather than folded into the core diff.** The §A walk is a walk of §6.2 and does **not** quote or dispose of line 992. Amending it is a *derived* consequence of §A.1 and §A.4, not a walk citation, and the author should decide whether v30a reaches outside the walked section.

**REPLACE with (1 line) — proposed:**

```
| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; **every declared reference-anchor entry reproduces within ±0.010 absolute by recomputation from the fixture's stored predictions (§6.2 as amended by v30a); the sliced variant is due under §6.2's amended Phase 1 CI obligation, not here**; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |
```

Only the Gate cell changes; the Phase, Work and Est. cells are byte-identical, so `check_phase_arithmetic` is unaffected (verified: PASS with C1 applied). **The alternative is to leave line 992 unchanged**, in which case the Phase 1 gate keeps a requirement that reads on a retired object — I do not recommend it, and record the recommendation as a recommendation.

---

### C2 — CONSEQUENTIAL, AUTHOR ADJUDICATION REQUIRED — §10.1 kill-gate criterion 3

**ANCHOR — `PREREG.md` line 1022, match count 1:**

```
3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
```

**The problem.** This is a **second copy of the premise H5 retires**: that silence on the corrected side is the correct behaviour. Under the amended criterion 3 the corrected side is characterized and carries real violations, so a rival tool that is silent there is silent where the map declares a violation — and under this clause that silence would count in its favour on the kill gate. `PREREG.md` would then hold both readings at once, in two sections.

**Why it is flagged.** §A.8 disposes of line 461 only. The walk does not quote line 1022. This is derived.

**REPLACE with (1 line) — proposed:**

```
3. Fires on `fixture_contaminated` and, on `fixture_corrected`, reports findings **consistent with the declared ground-truth map — silent where the map is silent, firing where the map declares a violation** (§6.2 criterion 3 as amended by v30a) **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
```

The ambiguity branch is carried through unchanged. **Note that §A.5 records the ambiguity clause as not firing for this fixture** (declaration 1009–1016), so the branch is inert here and is preserved only because it is a rule about any fixture.

---

## (iii) WHAT THIS DIFF DOES **NOT** CHANGE, AND WHY

1. **`PREREG.md` line 446 — the ground-truth column DAG and the count of independently leaking sources.** SATISFIED per §A.2 (822–841). The manifest requirement stands; the count stays where it is. What v30a constrains is its *arithmetic role*, and that constraint is stated in H6 as a rule about denominators, not as an edit to line 446. Editing 446 would also collide with R13's prohibition on adjusting evidence artifacts toward a decision.
2. **Lines 447, 448, 449 — reconstruction discipline, Phase 0 timing, and the semantic-ambiguity clause.** SATISFIED per §A.5 (988–1016). The ambiguity clause does not fire: the original work *did* document prediction timing; it was violated by the artifact, which is a different fact and is stated in the declaration, not here.
3. **Lines 453 and 457 — pass-gate framing and the frozen default configuration.** SATISFIED per §A.10 (1462–1472), carried unchanged.
4. **Line 459 — criterion 1's own text.** Stands byte-exact. §A.6 marks it SATISFIED; only its denominator's constitution is added (H6). Rewriting 459 would misrepresent the walk, which found the criterion sound and its denominator underspecified.
5. **Line 460 — criterion 2.** SATISFIED per §A.7 (1392–1403). Its scope is manifest-CLEAN columns and is unchanged. The mis-routing that R11 deletes was a *declaration-side* error (routing OUT OF JURISDICTION columns to criterion 2, which has no landing site for them); no registered text carried it, so there is nothing to amend here.
6. **Line 462 — criterion 4, the identity control.** SATISFIED per §A.9 (1438–1458). The sentinel statement (the wrapped `net_delta` magnitudes near 4.29e9 present identically on both sides) is an **instance** — this fixture's as-built defect — and stays in the declaration. Writing it into `PREREG.md` would put a fixture's data content into the specification.
7. **Lines 464 and 468 — descendants secondary, top-k, aliases.** SATISFIED per §A.11 (1512). H6 inserts *after* 464 and does not modify it.
8. **Lines 470–476 — the k-of-N descriptive proof count.** SATISFIED per §A.10 (1481–1489). The rule that it is a count and never a rate is unchanged; H6 adds only *which* N it is counted against, and the value of N stays in the declaration.
9. **Line 480 — the locked ordering.** SATISFIED per §A.10 item 3 (1490–1492); enforced by declaration §D.1, which freezes every gate-consumed number before the first gate run.
10. **§11 item 3 — the tag-message hashes.** Not amended. Working resolution **R7** (declaration 3664) records the hash count as a **class A mechanical fact requiring no locked-file edit**, and declaration §D.2 (3420–3455) declares the v30a tag's six hashes on that basis, citing §0.2.1 line 97 as the governing clause. **Open question for the author:** if you reject R7's class A call, §11 item 3 needs its own hunk; nothing else in this diff depends on the count.
11. **§0.1's lock table — no row added.** The new rules land in §6.2 and §10.2, which the table does not index, and each added row obliges a key-phrase target that `check_lock_table` verifies. **Open question:** the partition rule of H6 is arguably lock-table material ("how a denominator is constituted"); adding a row is a two-line change but is a structural decision the walk does not record.
12. **§7.7's `waived` entry condition — deliberately not invented.** §A.12 defines what being waived *means* but supplies no condition under which a detector-case may take the state. H8 says so explicitly instead of filling the gap. **Residual gap, reported rather than closed.**
13. **The declaration's §D.3 (a decision-log interpretation may resolve only toward the stronger reading) is not relocated into `PREREG.md`.** By the scope line it looks rule-shaped, but the walk records it as the declaration's own lock language governing its own decision-log tail, and does not record it as a `PREREG.md` amendment. H7 item 5 states the substance locally rather than citing §D.3, so `PREREG.md` does not become dependent on it. **Open scope-line question for the author.**
14. **§6.4's re-draw rule, §6.5's case families, §6.6, and every §7 metric definition.** No walk entry touches them.
15. **§13 item 4 — "whether the CME fixture ships in the repo, full or sliced".** An open decision about redistribution, not a normative statement about the Phase 0 gate; H4 does not reach it.
16. **Line 441 — "the fixture's AUC figures are provenance … no accuracy or generalization rate is published from the fixture."** Untouched and still exactly true of a recomputed anchor.
17. **Line 117's Claim A parenthetical**, which mentions criterion 3 and `fixture_corrected`. It is a historical ledger note naming v9 and is excluded from the normative scan by §6.8's own rule; amending a ledger note would falsify the record of what was argued at the time.
18. **§10.2 criterion 2's main clause (lines 1030–1031).** "The runtime detectors cannot separate contaminated from corrected fixture" survives the map amendment intact — under a map that differs per side, separation remains exactly the right question. Only its floor's undefined word is addressed (H7).
19. **`AVAILABILITY_DECLARATION.md` — not edited by this diff at all.** R18 holds: one live copy, edited in place, by items authorized to do so. Every instance this diff pushes out of `PREREG.md` is already in the declaration and already frozen by §D.1; **no new declaration content is required by this diff.**
20. **`DEVIATIONS.md`, `HISTORY.md`, `DESIGN.md`, `tools/`, `protocol/`, `tests/` — untouched.** Two are companion obligations rather than parts of this diff: §0.2.1 line 95 requires the deviation record *and* the amended tag ("Both"), and working resolution R8 fixes the `HISTORY.md` entry form as `### H-34 — from PREREG.md §0.2.1`. **Neither is drafted here; both are outstanding before the tag.**
21. **No git state was changed and none is proposed here.** No `add`, `commit`, `tag`, `push`, or `ots`. The `git show prereg-v30:PREREG.md` command quoted inside H1b is a read-only recovery instruction addressed to a future reader, not an action taken.

---

## (iv) APPLICATION

`…/scratchpad/amendment/apply_v30a.py` applies the hunks mechanically. It requires an explicit `--root`, **refuses to run against the live project directory**, matches every anchor as a full line, and raises if any anchor matches zero or more than one line. `--with-consequential` adds C1 and C2; without it, only H1a–H8 are applied.

```
python apply_v30a.py --root <copy-of-repo>            # core amendment, 9 hunks
python apply_v30a.py --root <copy-of-repo> --with-consequential   # 11 hunks
```

After applying, the two gates to re-run are `python tools/check_registration.py --stage prereg` (must exit 0 — this is §6.8's tag gate) and `python -m pytest tests/registration` (137 tests). Both were run on a scratch copy for both variants and both pass.
