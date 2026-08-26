# Author read-through package — verbatim extraction — source `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` — sha256 `f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310` — 277411 bytes — 3684 lines (wc -l) — extracted 2026-08-13

NOTE: §A.6.0 was recovered from a session transcript after a restage destroyed it. §14's BINDING ex-nq clause is new this pass.

## Contents

| # | Section heading (verbatim from source) | Source lines | Line count |
|---|---|---|---|
| 1 | 1. `decision_time` | 127-176 | 50 |
| 2 | §A. Conformance walk against PREREG.md §6.2, element by element (item P2) | 751-1597 | 847 |
| 3 | 13. The DECLARED GROUND-TRUTH MAP (element f; R9) — the corrected side is CHARACTERIZED, never clean | 1946-2518 | 573 |
| 4 | 14. Contaminated-side violation profile (element g; T1 headline) | 2932-3207 | 276 |
| 5 | 16. Documented-unverifiable assumptions (element i) | 3280-3314 | 35 |
| 6 | Decision log — working resolutions (DELTA R2, 2026-08-10; PROVISIONAL until the prereg-v30a tag is signed) | 3649-3684 | 36 |

SOURCE: AVAILABILITY_DECLARATION.md lines 127-176

## 1. `decision_time`

Registered vocabulary (PREREG.md line 203): "how *d(i)* derives from row *i* — bar open, bar
close, offset, or a column".

**DECLARED value: a column — `d(i)` = the row's `timestamp` column value `t`, an instant on
the 1-second snapshot lattice.**

**DECLARED availability contract at that decision instant — THE SINGLE NORMATIVE STATEMENT OF
THE BOUNDARY IN THIS FILE:**

> The decision for row `t` admits information through **`floor(t-1) + 1s`** — the end of the
> wall-clock second joined to the previous lattice row. Not "through snapshot `t-1`", and not
> "through time `t-1`".

This is the MEASURED boundary of the corrected (post-fix) features, and the declaration states
the measured boundary rather than the intended one. The corrected row stamped `t` carries the
previous row's construction, and that construction's trade/MBO aggregates cover the whole
wall-clock second `[floor(t-1), floor(t-1)+1s)`; because lattice stamps are generally off
wall-clock boundaries (§2), that window's end can lie strictly after `t-1`. §10 is the
EVIDENCE section for this statement and restates nothing: it carries the measurement, the
magnitudes, and the cross-checks. No other section in this file states the boundary rule.

Evidence for the declared value:
- The measurement: §10 (T1 `t1\violation_table.csv`, `corrected` / `claimed_T_prev` rows;
  C4 `c4\independent_counts.csv` `prev_row_B` rows). Working resolution R2 (file tail) is the
  authority for stating the measured boundary as the declaration.
- The construction that produces it: `phase7_l2_sim.py` line 276
  `snap[feature_cols] = snap[feature_cols].shift(1)`; line 819 writes
  "lag_fix: universal (all features shift(1))" (established fact, prior spike). The shift is
  POSITIONAL — one lattice row — and the row it reaches back to carries a full wall-clock
  second of trade/MBO aggregate, which is exactly why the boundary is `floor(t-1)+1s` and not
  `t-1`.

**Historical contract text — retained ONLY as the quoted claim that measurement violated, and
retired as a description of anything in this fixture:**
`MASTER_FINDINGS\preregistration_v4.txt` lines 303-304 (verbatim): "Causal lag: Mandatory
shift(1) on all features. Features at time t use information available only through time t-1."
Measured against that claim, the corrected features absorb events strictly after `t-1` on
89,568 of 338,158 rows for trades_all and 254,314 for mbo_all (§10). The claim is quoted; it
is not the declaration.

**Recorded deviation (PRE-FIX fixture side, what actually held — NOT the declaration):**
`pc2_transfer\scripts\phase5\phase5_ml.py` contains no shift(1); features in row `T` are
computed at snapshot `T` itself (e.g. line 193 `snap[f"mid_return_{lag}s"] = mid.pct_change(lag)`
ending at row T; lines 252-258 rolling sums ending at row T; line 258
`snap["vwap_distance"] = (mid - snap["vwap"]) / tick` reading mid[t] and same-second vwap).
The archive's own audit confirms: `scripts\phase5\phase5_audit.py` lines 96-101:
"Q1: At prediction time t, does input include data from second t? ... ANSWER: YES — LEAKAGE
CONFIRMED ... The label predicts direction FROM mid[t]."

SOURCE: AVAILABILITY_DECLARATION.md lines 751-1597

## §A. Conformance walk against PREREG.md §6.2, element by element (item P2)

**First CONFORMANCE section of Part II** (§0 precedes it and renumbers nothing). Every
registered element of PREREG.md §6.2 (lines 443-481, read
in full this pass at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`) is
quoted verbatim with its line number and marked **SATISFIED** (with how, and the artifact) or
**AMENDED** (old text quoted, new text stated, why, and that it is a class C amendment under
PREREG.md line 93). Amendments are PROVISIONAL until the prereg-v30a tag is signed.

**A.0 — the amendment class, stated once.** PREREG.md line 93 (verbatim): "**C — semantic or
accounting gaps** | The measurement reveals a needed *new* branch, unit, denominator, coverage
state, tier licence, or acceptance criterion | **not resolve under this registration** |
anything that changes what a published number means". Line 95 (verbatim): "**Class C requires
an amended registration**, committed and externally timestamped **before the affected detector
is implemented or evaluated** — a `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md`
entry standing alone." Every AMENDED entry below is a class C amendment carried by this
registration.

---

### A.1 — Reference AUC anchor — **AMENDED (class C)**

> **SCORED ON ARTIFACT B** (§0.2) — the trio is recomputed from Artifact B's stored `pred_score`
> / `true_label` columns. No Artifact A number enters it.

**Registered text, PREREG.md line 445 (verbatim):**

> **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

**OLD:** the pair (0.957, 0.675) with an acceptance interval of ±0.010 absolute, as the anchor
the fixture pair must reproduce.

**NEW:** the anchor is **retired and replaced** by the recomputed ZC **LightGBM** trio, computed
directly from the stored per-row predictions of the declared fixture pair (§8):

| Horizon | Pre-fix (contaminated) | Post-fix (corrected) | n rows |
|---|---|---|---|
| 5s | 0.966244 | 0.931536 | 1,047,430 |
| 10s | 0.939968 | 0.756504 | 655,016 |
| 30s | 0.856419 | 0.679288 | 745,656 |

Source: `f1\f1_results.csv`, column `recomputed_auc`, rows `pre/ZC/LightGBM/{5s,10s,30s}`
(lines 50-52) and `post/ZC/LightGBM/{5s,10s,30s}` (lines 114-116).

**Why the old anchor cannot stand, stated plainly:**

1. **No single horizon satisfies the old interval on both sides.** Against 0.957 ± 0.010 on the
   pre-fix side and 0.675 ± 0.010 on the post-fix side: 5s passes pre (|0.966244 − 0.957| =
   0.009244) and fails post by 0.2565; 10s fails pre by 0.0170 and fails post by 0.0815; 30s
   fails pre by 0.1006 and passes post (|0.679288 − 0.675| = 0.004288). There is no horizon at
   which the registered pair is reproduced. Keeping the interval would fail the gate on a
   fixture whose pair is otherwise exactly as registered.
2. **The model family changes: XGBoost → LightGBM.** The original documented protocol names
   XGBoost (`MASTER_FINDINGS\preregistration_v4.txt` line 273 "2. XGBoost (gradient boosted
   trees)"; line 284 records its hyperparameters). The declared trio above is LightGBM.
   `f1\f1_results.csv` carries both families across 128 rows (32 rows each for
   pre/LightGBM, pre/XGBoost, post/LightGBM, post/XGBoost); the declaration names LightGBM and
   states so rather than leaving the family implicit.
3. **The RE-EVALUATE class makes the recomputation authoritative, not merely alternative.** The
   fixture is the stored-prediction pair (§8): 64 parquets per side, each carrying `pred_score`
   and `true_label` per row. AUC over those columns is a pure function of bytes already on
   disk — no retraining, no re-randomization, no environment dependence, nothing that a rerun
   could move. The recorded meta AUCs are a 4-decimal secondary record of the same quantity;
   where meta exists it agrees (`flag_gt_5e-5` False on all 95 matched rows, §8). So the
   recomputation does not contradict the record — it supersedes it in precision, and it is the
   only form of the number that can be audited from the fixture itself.

The `full` mode clause of line 445 is unaffected and stands.

---

### A.2 — Ground-truth column DAG and the independently-leaking-source count — **SATISFIED, with the governing scope named**

**Registered text, PREREG.md line 446 (verbatim):**

> **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.

**SATISFIED.** **The count of independently leaking sources is 25**, and the **governing
manifest scope is `f3\fixture_manifest_DRAFT.json`** — the 35-column set the Phase 7 models are
fed. Its `counts` block (read this pass): `independently_leaking_sources: 25`, `leak_source: 25`,
`descendant: 6`, `clean: 4`, `total_fed_to_phase7: 35`, `not_fed_to_phase7: 19`, with the
leak-source flavor split `label_base_price: 7` / `contemporaneous_state_flow: 18`.

> **THIS COUNT CARRIES NO GATE ARITHMETIC (working resolution R11).** PREREG.md line 446 is a
> **manifest-content** requirement: the manifest must record the DAG and the count. It is
> satisfied by the manifest recording 25. **The criterion-1 denominator is a different object
> and derives from the DECLARED MAP, not from these construction classes** — see §A.6 and
> §D.1. The manifest's leak-source classification is **provenance context**: it says how a
> column was built, not whether the map declares a violation on it on the scored side under
> the declared tie branch. Reading 25 as N was the contradiction R11 resolves; **N is 11**
> (§A.6). Both numbers are in this file and neither is left to be inferred.

**The flavor split, stated BOTH ways (working resolution R13).** The manifest and the
declaration disagree on exactly one column's FLAVOR, and the disagreement is recorded rather
than removed:

| Flavor | Per `f3\fixture_manifest_DRAFT.json`, as of its date | Under R6 (the declaration's operative value) |
|---|---|---|
| `label_base_price` | **7** (incl. `weighted_mid`) | **6** |
| `contemporaneous_state_flow` | **18** | **19** (incl. `weighted_mid`) |
| leak_source total | 25 | 25 |

- **The manifest is NOT edited.** `f3\fixture_manifest_DRAFT.json` is an evidence artifact of a
  dated measurement round. **Evidence artifacts are never adjusted toward a decision** (R13).
  Editing its `flavor` field to agree with R6 would make the artifact appear to have measured
  what a later resolution decided, and would destroy the only record of what the F3 round
  actually judged.
- **R6 is the declaration's operative value** for `weighted_mid` — `contemporaneous_state_flow`,
  PROVISIONAL until the prereg-v30a tag is signed, on the information-content test recorded in
  the supersession note after the T2 addendum block.
- **The supersession is scoped to one column and one field.** The manifest's `flavor` for
  `weighted_mid` is superseded **for `weighted_mid` only**; every other flavor, every CLASS
  assignment (including `weighted_mid`'s own LEAK-SOURCE class, which was never ambiguous),
  the parent lists, and all four `counts` totals stand exactly as the manifest records them.
- **Nothing in the gate turns on the split.** Flavor enters no criterion, no denominator and no
  count that the gate consumes; it is reported because a reader comparing the two artifacts
  would otherwise find an unexplained 7-vs-6 and be entitled to distrust both.

**Why F3 governs and not T4.** `t4\fixture_manifest_35col_DRAFT.json` reports
`counts_projected_subset`: `projected_total: 28`, `unconstructible_total: 7`, `leak_source: 22`,
`descendant: 5`, `clean: 1`, with `unconstructible_by_class` = `leak_source: 3`, `descendant: 1`,
`clean: 3`. That 22 is a property of what the **F2 rebuild can reconstruct** under the
selection/renaming-only projection rule (§17), not a property of the fixture the gate scores.
The gate's fixture is the stored-prediction pair, whose feature set is the full 35 columns under
working resolution R3 (§16 item 1). **The declaration therefore governs on 25 and records 22 as
the reconstruction-limited subset**; both numbers appear in this file and neither is left to be
inferred. Any gate report quoting a leaking-source count must name which of the two scopes it
counts under — that is a declared reporting obligation, not a convention.

---

### A.3 — Contamination availability class — **SATISFIED BY SUBSTITUTE (class C amendment of the RECORDING LOCUS)**

**Registered text, PREREG.md line 450 (verbatim):**

> **Contamination availability class** recorded in the manifest.

**Declared class: AVAILABILITY VIOLATION BY FORWARD JOIN** — the contamination is not a value
corruption, a shuffle, or a label leak in the ordinary sense; it is a cell whose availability
time is strictly later than the decision time that consumes it. Mechanism: the `ts_floor`
wall-clock-second join (§3) attaches to snapshot row `T` an aggregate over
`[floor(T), floor(T)+1s)`, a window that completes at `floor(T)+1s` and can contain events with
`ts_event > T`. Measured incidence and per-column enumeration: §14 and §C.

**The measured gap:** neither `f3\fixture_manifest_DRAFT.json` nor
`t4\fixture_manifest_35col_DRAFT.json` carries a named field for the contamination availability
class — verified this pass by key search over both files.

**RESOLUTION — the recording locus is AMENDED, and the element is MET, not outstanding.** The
earlier draft left this element half-met ("this declaration is the record until the field is
added") and booked the field as a class A act due before the tag. That disposition is
withdrawn. It is replaced as follows:

**OLD (registered, PREREG.md line 450, verbatim):** "**Contamination availability class**
recorded in the manifest."

**NEW:** the contamination availability class is **recorded in this availability declaration**,
which the `prereg-v30a` tag message hashes as its sixth file (§D.2), and is frozen at the tag
by §D.1. The manifest is not the locus and is not edited.

**Why this substitute, and why it is not weaker (class C under PREREG.md line 93):**

1. **The manifest cannot take the field without becoming something it is not.**
   `f3\fixture_manifest_DRAFT.json` is an evidence artifact of a dated measurement round.
   Writing a *declaration* into it would make a measurement record carry a decision — precisely
   what working resolution R13 forbids in the neighbouring case ("evidence artifacts are never
   adjusted toward a decision"). The registered wording assumed one artifact where this fixture
   has two: a measurement manifest and a declaration.
2. **The substitute binds harder than the original.** The manifest is hashed in no tag message.
   This declaration is hashed in the v30a tag message (§D.2's sixth hash) and its contents are
   frozen by §D.1, so moving the class after the tag is itself a class C amendment. Recording
   the class here therefore subjects it to a stronger integrity chain than line 450 asked for —
   "an amendment weaker than the thing it amends is not one" (PREREG.md line 97) is satisfied
   in the direction the clause intends.
3. **Nothing is lost in reach.** The class is stated above with its mechanism, its measured
   incidence (§14), its per-column enumeration (§C) and its per-cell map (§13). A reader
   looking for it in the manifest is routed here by this section, which is itself hashed.

**What this amendment does NOT do.** It does not remove the obligation to record the class —
the class is recorded, verbatim, above. It does not license recording any *other* registered
manifest content outside the manifest: line 446's ground-truth DAG and independent-leak count
remain manifest content and are satisfied there (§A.2). And it does not retroactively make the
earlier "field OUTSTANDING" reading correct; that reading is superseded, and the lock-time
obligation it generated is discharged in §D.2.

---

### A.4 — Sliced variant for CI — **AMENDED (class C): moved off the Phase 0 acceptance fixture and re-registered as a Phase 1 CI obligation**

**Registered text, PREREG.md line 451 (verbatim):**

> **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**The measured state.** No artifact in this spike produces or names a sliced fixture variant,
and no padded slicer has been run against the fixture.

**The element is UNSATISFIABLE AS REGISTERED at the moment this amendment must be committed,
and the reason is structural, not an omission.** Line 451 requires the variant to come from
**the same padded slicer as user-facing slice auditing** — a component of the tool under
development. PREREG.md line 95 requires a class C amendment to be committed and externally
timestamped **"before the affected detector is implemented or evaluated"**. At that instant no
slicer exists, so no artifact satisfying line 451 can exist either. Leaving the element
"outstanding" would ship the registration with a permanently unmet registered element and would
invite it to be quietly re-read as satisfied later — the failure mode §2.7's undeclared-means-
unsupported rule exists to stop. **The instrument for an element that cannot be met as written
is an amendment. It is amended here, explicitly, and not waived.**

**OLD:** a sliced fixture variant, produced by the same padded slicer as user-facing slice
auditing, is part of the §6.2 acceptance fixture.

**NEW, in three binding parts:**

1. **Locus moved.** The sliced variant is **not** part of the v30a Phase 0 acceptance fixture.
   The fixture the v30a gate is evaluated on is exactly §8's stored-prediction pair.
2. **Obligation re-registered, not deleted.** The sliced variant becomes a **Phase 1 CI
   obligation, due at the first CI run that exercises the padded slicer** and before any
   user-facing slice auditing is published. It must be produced by that same padded slicer,
   with its slice boundaries declared.
3. **Its scoring rule is declared NOW, ex ante, so it cannot be chosen after seeing a result.**
   Under the amended criterion 3 (§A.8) a slice inherits the map cells its rows fall in: each
   slice is scored against the `n1\declared_map.csv` cells it selects, findings the selected
   cells predict are required, findings they exclude are false positives, and cells the map
   does not cover are unscored. **A slice of a CHARACTERIZED side is never treated as clean**,
   and a slice may not be reported as a pass on the strength of containing only unscored cells.

**Why this is class C and not class A.** It changes which artifacts the acceptance criteria are
evaluated on, and therefore what a published fixture number means — PREREG.md line 93's
definition exactly. It is carried by this registration under line 95.

**What this amendment does NOT do.** It does not delete slice auditing, does not exempt the
slicer from CI, and does not permit the Phase 1 obligation to be discharged by a
`DEVIATIONS.md` entry or by a working resolution — §D.3 forbids a decision-log entry from
weakening a locked obligation, and this obligation is now locked by §D.1. Dropping it later is
a further class C amendment.

---

### A.5 — Reconstruction discipline, timing, and the ambiguity clause — **SATISFIED**

**Registered text, PREREG.md line 447 (verbatim):**

> **The availability declaration is reconstructed, not chosen** — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon, and intended live execution protocol, with **evidence for each element recorded before any detector tuning.**

**SATISFIED.** Every element of the declaration carries a code or paper citation recorded before
any detector exists — Part I §§1-7 and the evidence-class table, plus §§8-17 and §§B-C. No
detector code has been written or tuned in any item of this spike; the declaration's numbers all
predate it.

**Registered text, PREREG.md line 448 (verbatim):**

> **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).

**SATISFIED.** This whole file is a Phase 0 product; no cross-tool comparison has been run.

**Registered text, PREREG.md line 449 (verbatim):**

> **If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous.** It may be used under an explicit **labelled hypothetical declaration**, and does not carry full acceptance weight. See §10.1 criterion 3 and §10.2 criterion 2.

**SATISFIED — the clause does not fire, and the reason matters.** The original work DID document
prediction timing: `MASTER_FINDINGS\preregistration_v4.txt` lines 303-304 (quoted in §1). The
fixture is therefore **not** semantically ambiguous and does **not** need a labelled hypothetical
declaration. What measurement established is a different thing: the documented timing was
**violated by the artifact** (§10). Documented-and-violated is not the same as undocumented, and
the declaration states the measured boundary (§1) precisely so that the distinction is not
smuggled. The one element Part I genuinely left ambiguous — `ties` — is resolved by R1 to the
registered default, not to a hypothetical (§12).

---

### A.6 — Criterion 1 — **SATISFIED; denominator RE-DERIVED FROM THE DECLARED MAP under working resolution R11. N = 11.**

**Registered text, PREREG.md line 459 (verbatim):**

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.

Related registered text, PREREG.md line 464 (verbatim):

> Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

and PREREG.md line 468 (verbatim):

> Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**SATISFIED.** The criterion-1 violation set is enumerated side-relatively and post-lag in §C,
by column. **The denominator derives from the DECLARED MAP (`n1\declared_map.csv`), not from
the manifest's construction classes** — working resolution R11, verbatim at the file tail. The
earlier draft's implicit denominator was the manifest's 25 independently-leaking sources; that
was the contradiction the P2 verifier found, because line 446's count is a statement about how
columns were BUILT and criterion 1 is a statement about what the map DECLARES VIOLATING on the
scored side under the declared tie branch. **The manifest's leak-source classification is
provenance context and carries no gate arithmetic** (§A.2).

**The three classes are mutually exclusive, exhaustive over the 35 fed columns, and each is
ENUMERATED BY NAME.** No class is defined as a residue and no class is stated as a bare count;
a count that cannot be written out as a list is a count nobody can audit.

#### A.6.0 — DERIVATION RULE. **The enumeration below is what the rule yields.**

Each column's class is determined by a single rule applied to its construction and its gate
status. The rule, stated verbatim so it can be re-applied when a column changes construction:

- **REQUIRED** iff its construction carries the wall-clock `ts_floor` join **and** it is not
  degenerate-constant.
- **OUT OF JURISDICTION** iff its construction reads only same-row book/clock values,
  availability-legal at the boundary instant under R1's `ties: available`.
- **UNSCORED** iff it is degenerate-constant **or** unconstructible under T4.

Three reading notes fix the rule's edges on the 35-column set. Each is a re-statement of
material already in this section, made explicit here because otherwise the rule leaves a
column ambiguously classed:

- **Precedence when clauses conflict.** UNSCORED wins. A column whose construction reads a
  merged `ts_floor` aggregate but is identically constant on the fixture (`buy_volume_10s`)
  satisfies both the REQUIRED first clause and the UNSCORED first limb; the enumeration
  classes it UNSCORED because a dead-zero column carries no evidence, and leaving it in
  REQUIRED would make criterion 1 unsatisfiable for a reason unrelated to detection
  (§A.6.3, first bullet). *(Strictly, precedence is not load-bearing for this column: the
  REQUIRED clause is a CONJUNCTION — "carries the `ts_floor` join **and** is not
  degenerate-constant" — so its second conjunct already excludes `buy_volume_10s` without
  appeal to precedence. The column where precedence IS load-bearing is
  `book_imbalance_ratio`: it fully satisfies the OUT OF JURISDICTION iff (a pure function of
  the same row's two depth sums) **and** fully satisfies the UNSCORED second limb
  (T4-EXCLUDED), so only "UNSCORED wins" resolves it — which it does, to UNSCORED, per
  §A.6.3 and frozen §D.1 item 2.)*
- **"Same-row book/clock" is read as "within-lattice book/clock", not literally single-row.**
  A same-lattice lagged read (`depth[t] - depth[t-5s]`, `mid[t] / mid[t-1s]`) reads two rows
  of the same book/clock column but carries no `ts_floor` join to a trade aggregate. Each
  constituent read is availability-legal at its own timestamp under R1's `ties: available`
  (§A.6.2's explicit basis; PREREG.md 190-197). These pass OUT OF JURISDICTION.
- **"Unconstructible under T4" is read as "gate status EXCLUDED under T4 applied to the
  gate-scored fixture", not as "F2-rebuild-unconstructible".** The F2 rebuild's seven
  selection/renaming-only unconstructibles (§17) are not gate-unscored; that reading would
  silently drop `dollar_volume_1s` (rule-REQUIRED) and `tick_direction` (rule-OUT OF
  JURISDICTION) out of the arithmetic, contradicting R11. §A.6.3's closing paragraph states
  this precisely; the rule inherits it verbatim.

**Column-by-column application (all 35 fed columns).** The class each column would be
placed in by the rule above is shown alongside the sub-section where the frozen enumeration
lists it. Any disagreement between the rule-derived class and the frozen class is a
stop-and-report; there is none this pass.

> **Reading the "construction" column, per §0.3's artifact rule.** These 35 are Artifact-B fed
> columns, and Y1 traces all 35 to `phase7_l2_sim.py`. Where a row cites a bare line number or a
> `phase5_ml.py` line, it names the **lineage** construction (Part I's citation base, §0.1) —
> the same construction exists in the Phase 7 builder, and the `ts_floor` join the rule turns on
> is present in BOTH generations, so no row's class depends on which file is read. The trade
> rollups are `phase5_ml.py` L253/L255/L257/L258 ≡ `phase7_l2_sim.py` L238-239/L241/L242/L243,
> with the trades merge at `phase5_ml.py` L248 ≡ `phase7_l2_sim.py` L231. Rows that cite
> `phase7_l2_sim.py` explicitly are Phase-7-only columns with no lineage counterpart.

| # | Column | Rule-derived class | Clause satisfied | Frozen at |
|---|---|---|---|---|
| 1  | `net_delta_1s`          | REQUIRED | `ts_floor` merge on `net_delta` (`phase5_ml.py` L253) | A.6.1 #1 |
| 2  | `net_delta_5s`          | REQUIRED | same L253 rolling(5)                                       | A.6.1 #2 |
| 3  | `net_delta_10s`         | REQUIRED | same L253 rolling(10)                                      | A.6.1 #3 |
| 4  | `net_delta_30s`         | REQUIRED | same L253 rolling(30)                                      | A.6.1 #4 |
| 5  | `net_delta_60s`         | REQUIRED | same L253 rolling(60)                                      | A.6.1 #5 |
| 6  | `sell_volume_10s`       | REQUIRED | L255, `sell_size` merged on `ts_floor`                     | A.6.1 #6 |
| 7  | `large_trade_count_10s` | REQUIRED | L257, large-count aggregate merged on `ts_floor`           | A.6.1 #7 |
| 8  | `vwap_distance`         | REQUIRED | L258, the `vwap` term is the merged per-second aggregate   | A.6.1 #8 |
| 9  | `trade_volume_1s`       | REQUIRED | `phase7_l2_sim.py` groupby L216-226, merge L231, assign L246 | A.6.1 #9 |
| 10 | `trade_count_1s`        | REQUIRED | groupby L220, assign L247                                  | A.6.1 #10 |
| 11 | `dollar_volume_1s`      | REQUIRED | L214 + groupby L223, assign L248                           | A.6.1 #11 |
| 12 | `minutes_since_open`    | OUT OF JURISDICTION | deterministic clock function of the row's own timestamp | A.6.2 (a) |
| 13 | `session_open`          | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 14 | `session_mid`           | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 15 | `session_close`         | OUT OF JURISDICTION | same                                                    | A.6.2 (a) |
| 16 | `spread_ticks`          | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 17 | `bid_size_1`            | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 18 | `ask_size_1`            | OUT OF JURISDICTION | same-row book read                                      | A.6.2 (b) |
| 19 | `l1_imbalance`          | OUT OF JURISDICTION | same-row derivation of bid/ask sizes                    | A.6.2 (b) |
| 20 | `total_bid_depth`       | OUT OF JURISDICTION | same-row sum across levels                              | A.6.2 (b) |
| 21 | `total_ask_depth`       | OUT OF JURISDICTION | same-row sum                                            | A.6.2 (b) |
| 22 | `depth_imbalance`       | OUT OF JURISDICTION | same-row ratio                                          | A.6.2 (b) |
| 23 | `book_slope_bid`        | OUT OF JURISDICTION | same-row slope across price levels                      | A.6.2 (b) |
| 24 | `book_slope_ask`        | OUT OF JURISDICTION | same-row slope across price levels                      | A.6.2 (b) |
| 25 | `depth_change_1s`       | OUT OF JURISDICTION | within-lattice lagged reads of `depth`; no trade join   | A.6.2 (b) |
| 26 | `depth_change_5s`       | OUT OF JURISDICTION | within-lattice lagged reads                             | A.6.2 (b) |
| 27 | `depth_change_30s`      | OUT OF JURISDICTION | within-lattice lagged reads                             | A.6.2 (b) |
| 28 | `mid_return_1s`         | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 29 | `mid_return_5s`         | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 30 | `mid_return_10s`        | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 31 | `mid_return_30s`        | OUT OF JURISDICTION | within-lattice `mid` reads                              | A.6.2 (b) |
| 32 | `tick_direction`        | OUT OF JURISDICTION | sign of within-lattice `mid` change                     | A.6.2 (b) |
| 33 | `weighted_mid`          | OUT OF JURISDICTION | same-row bid/ask weighting                              | A.6.2 (b) |
| 34 | `buy_volume_10s`        | UNSCORED (*degenerate-constant clause*) | `phase5_ml.py` L231 (= `phase7_l2_sim.py` L207) aggressor classifier matches none of the parquet's aggressor values → column identically 0 | A.6.3 |
| 35 | `book_imbalance_ratio`  | UNSCORED (*T4-unconstructible clause*)  | construction not verified equivalent from fixture code; gate status EXCLUDED (§C.4(c), §17 item 6) | A.6.3 |

**What the rule yields.** REQUIRED (rows 1-11): 11. OUT OF JURISDICTION (rows 12-33): 22 —
4 clock-function (rows 12-15) + 18 book/lattice (rows 16-33). UNSCORED (rows 34-35): 2.
Total 35. This matches the sub-sections' enumerations column by column and matches the
partition check in §A.6.4. **If a future column changes construction (for example,
`book_imbalance_ratio` becomes constructible per §C.4(c)), its class must be re-derived by
this rule and the change recorded as an amendment in the usual way; the enumeration is the
current output of the rule, not a substitute for it.**

#### A.6.1 — REQUIRED (the criterion-1 denominator). **N = 11.**

Columns the declared map declares violating on the scored side under the declared branch — the
**forward-join / `ts_floor` overhang family**. Derivation, stated so it is reproducible: these
are the columns of the 35-column fed set whose construction reads an aggregate merged on
`ts_floor`, the wall-clock-second key (§3, §C.1), so their true availability instant is
`ts_floor + 1s`; the map classes that govern them are the `trades_*` classes, which are
strict-positive on the contaminated side in **all 48** instrument-months (§13(c)) and on the
corrected side in the 18 of §13(b).

| # | Column | Construction | Governing map class |
|---|---|---|---|
| 1 | `net_delta_1s` | `phase5_ml.py` L253, rolling sum of merged `net_delta` | `trades_all` |
| 2 | `net_delta_5s` | L253 | `trades_all` |
| 3 | `net_delta_10s` | L253 | `trades_all` |
| 4 | `net_delta_30s` | L253 | `trades_all` |
| 5 | `net_delta_60s` | L253 | `trades_all` |
| 6 | `sell_volume_10s` | L255 | `trades_sell` (≡ `trades_all` here, §15) |
| 7 | `large_trade_count_10s` | L257 | `trades_large` |
| 8 | `vwap_distance` | L258, `(mid - snap["vwap"]) / tick` — the `vwap` term is the merged aggregate | `trades_all` |
| 9 | `trade_volume_1s` | `phase7_l2_sim.py` groupby L216-226, merge L231, assign L246 | `trades_all` |
| 10 | `trade_count_1s` | groupby L220, assign L247 | `trades_all` |
| 11 | `dollar_volume_1s` | L214 + groupby L223, assign L248 | `trades_all` |

**N = 11**, being the length of that list. A correct detector must produce at least one
**primary** runtime finding attributed to each of the eleven, on the side and in the
instrument-months where the map declares the violation. Line 468 binds: top-k presence does not
satisfy it, and an alias satisfies it only if recorded before the run.

Two notes that keep the list honest:

- **`vwap_distance` is REQUIRED for its `vwap` term, not for its `mid` term.** Its
  `(X - mid)/tick` form also makes it a label-base reader; that character is L2a's and is
  neither credited nor penalized here (§C.3). Its availability violation is the merged
  wall-clock-second aggregate, which is a §C.1 join-family violation like the other ten.
  **It is the fixture's SOLE dual-ground column — the only MIXED-source column of the 35 — and
  the full statement of what that means for this entry is §C.5**, which must be read with this
  row: the REQUIRED finding is specifically the **forward-join** finding (`ts_floor` trade
  window, `phase7_l2_sim.py` L224-225 / L231 / L235), and **an availability-class finding on its
  same-row `mid[t]` read (L149) is OUT OF JURISDICTION and does NOT satisfy this entry.** Naming
  the right column on the wrong ground does not satisfy criterion 1. Per R16's discipline the
  column still carries **one gate class only — REQUIRED** (§C.5's comparison table).
- **No MBO-derived column is in the list, and that is a scope fact, not an omission.** Phase 7
  feeds no MBO columns at all (§4's Phase 7 difference, §C.1's scope note), so the map's six
  `mbo_*` classes characterise the fixture's MBO stream against the lattice without attaching
  to any fed column. `trade_count_10s` is likewise absent because Phase 7 drops it.

#### A.6.2 — OUT OF JURISDICTION (22 columns)

Declared availability-legal at the boundary instant under R1's `ties: available`. **An
availability-class finding on any of them is a FALSE POSITIVE.** They enter no criterion-1
denominator and carry no required finding. Two sub-groups, because their false-positive routes
differ:

**(a) Manifest-CLEAN columns — 4. Route: criterion 2 (contaminated side) and the amended
criterion 3 (corrected side).** `minutes_since_open`, `session_open`, `session_mid`,
`session_close`. Role `always`, deterministic clock functions of the row's own timestamp
(§4, T2 addendum). The session-flag staleness quirk licenses no finding on either side
(§C.4(b)).

**(b) Same-row book and lattice reads that the manifest classes LEAK-SOURCE or DESCENDANT —
18. Route: declared false positive; criterion 2 has NO landing site for them.** `spread_ticks`,
`bid_size_1`, `ask_size_1`, `l1_imbalance`, `total_bid_depth`, `total_ask_depth`,
`depth_imbalance`, `book_slope_bid`, `book_slope_ask`, `depth_change_1s`, `depth_change_5s`,
`depth_change_30s`, `mid_return_1s`, `mid_return_5s`, `mid_return_10s`, `mid_return_30s`,
`tick_direction`, `weighted_mid`.

> PREREG.md line 460 (verbatim): "2. No **manifest-clean** source column receives **any runtime
> finding of any tier, primary or secondary**, on `fixture_contaminated`." Its scope is
> manifest-CLEAN columns. The 18 above are manifest LEAK-SOURCE or DESCENDANT, so **criterion 2
> cannot receive them** — routing them there was the error R11 deletes in §C.3. A finding on
> one of them is a false positive **by this declaration**, recorded as such in the gate report,
> and it is not converted into a criterion-2 failure.

**Their label-base character is real and is assigned to L2a.** `tick_direction`, `weighted_mid`
(and `vwap_distance`, which is REQUIRED for a different reason) sit at `mid(t)`, the base
`fwd_move_ticks_*` measures from. **An L2a label-base finding on them is neither credited nor
penalized by this availability gate.**

#### A.6.3 — UNSCORED (2 columns, plus a cell-level member)

Requires no finding and forbids none; enters no denominator, contributes to no rate, and
**cannot be reported as a pass**.

- **`buy_volume_10s` — degenerate constant.** `phase5_ml.py` L231's `isin(["B","Buy","buy"])`
  matches none of the parquet's `BUY_AGGRESSOR`/`SELL_AGGRESSOR`/`UNKNOWN` values, so the column
  is identically 0 and the `trades_buy` map class is 0 strict / 0 equal in all 96 of its cells
  on both sides (§C.4(a)). A dead-zero column cannot carry a finding for a reason connected to
  availability, and leaving it in would make criterion 1 unsatisfiable for a reason unrelated to
  detection. Must be named in the gate report as **EXCLUDED**, never as MISSED.
- **`book_imbalance_ratio` — gate status EXCLUDED, lag treatment UNRESOLVED** (§C.4(c), §17
  item 6). **It carries ONE gate class and one only — UNSCORED (working resolution R16).** That
  it WOULD be OUT OF JURISDICTION if it were constructible is recorded as a fact in §C.3
  category 2 and is **not applied**: a column carrying two frozen classes violates "no field
  answers two questions". Reinstating it changes the criterion-1 denominator and is class C.
- **Cell-level: the 72 `UNSCORED_FOR_LACK_OF_DATA` map cells** (nq's six MBO classes x 6 months
  x 2 sides, §13(g), §13(h)). These are **cells, not columns**; because Phase 7 feeds no MBO
  column, none of the 35 fed columns is put into UNSCORED by them. Recorded here so the class
  is complete and so nq's MBO absence is never read as a column-level pass.

**R11's third UNSCORED limb, read precisely.** R11 names "unconstructibles" as UNSCORED. That
must be read as *columns whose gate status is declared EXCLUDED*, which on this fixture is
`book_imbalance_ratio` alone. The 7 UNCONSTRUCTIBLE columns of §17 are unconstructible **in the
F2 rebuild's selection/renaming-only projection**, not in the fixture the gate scores — the gate
scores the stored-prediction pair over the full 35 columns under R3 (§A.2, §16 item 1). Reading
§17's seven as gate-unscored would silently drop `dollar_volume_1s` and `tick_direction` out of
the arithmetic, which is the opposite of what R11 does. **`dollar_volume_1s` is REQUIRED
(A.6.1 #11); `tick_direction`, `weighted_mid`, `session_open`, `session_mid`, `session_close`
are OUT OF JURISDICTION (A.6.2); only `book_imbalance_ratio` is UNSCORED.**

#### A.6.4 — PARTITION CHECK (must be reproduced by any gate report)

| Class | Count |
|---|---|
| REQUIRED (A.6.1) | **11** |
| OUT OF JURISDICTION (A.6.2) — 4 manifest-clean + 18 same-row reads | **22** |
| UNSCORED (A.6.3) | **2** |
| **Total** | **35** |

11 + 22 + 2 = **35** = `f3\fixture_manifest_DRAFT.json` `counts.total_fed_to_phase7`. **No
column appears in two classes and no fed column is missing from all three** — checked column by
column against the manifest's 35-entry `columns` array this pass. The check is printed here, in
the declaration, because a partition asserted but not shown is a partition nobody verified.

#### A.6.5 — CROSS-TABULATION of the TWO partitions: Y1 SOURCE class x R11 GATE class (item S2)

**What this is, and why it is not redundant with §A.6.4.** The 35 fed columns are cut twice by
two independent instruments. **Cut 1 — the Y1 SOURCE partition** (`y1\column_universe.csv`, 35
rows, each carrying its construction quote and upstream line numbers) asks *which raw file the
column's construction reads*: snapshot parquet **13**, trades parquet **11**,
derived-from-another-column **9**, clock-only **1**, MIXED snapshot+trades **1**; MBO **0**.
**Cut 2 — the R11 GATE partition** (§A.6.1 / §A.6.2 / §A.6.3, which are authoritative here and
are the lists transcribed below) asks *what the gate does with a finding on the column*:
REQUIRED **11**, OUT OF JURISDICTION **22**, UNSCORED **2**. The two cuts were built from
different artifacts for different purposes and neither was derived from the other. §A.6.4 checks
that Cut 2 is a partition; **this subsection checks that Cut 1 and Cut 2 COMPOSE** — that the
gate class of every column is the one its construction implies.

**WHY they should compose, stated as the mechanism before the table so the table can refute it.**
A column's gate class follows from **whether its construction carries the wall-clock `ts_floor`
join**. That join — `phase5_ml.py` L222/L230, merges L248/L273; `phase7_l2_sim.py` L206/L231
(§3, §C.1) — attaches to row `T` an aggregate over `[floor(T), floor(T)+1s)`, whose true
availability instant is `floor(T)+1s`, strictly after `T`. **Carrying that join is a property of
the SOURCE**: the trades parquet reaches the lattice only through it, while the snapshot parquet
*is* the lattice and needs no join, and the clock is a function of the row's own stamp. So
**trade-touching ⇒ forward-join ⇒ REQUIRED**, and **not-trade-touching ⇒ same-row read ⇒
availability-legal at the boundary under R1 ⇒ OUT OF JURISDICTION** — in each case *unless* a
separately-registered carve-out removes the column from scoring altogether. There are exactly two
such carve-outs, both pre-existing and neither invented here: `buy_volume_10s` (degenerate
constant, §C.4(a)) and `book_imbalance_ratio` (lag treatment unresolved, R16, §C.4(c)).

**THE 35 ROWS.** SOURCE class from `y1\column_universe.csv` (`source_class`); GATE class
transcribed by name from §A.6.1 (11), §A.6.2(a)+(b) (4 + 18) and §A.6.3 (2). The two name sets
were compared as sets before anything else: **identical, 35 = 35, no name in one and not the
other.**

| # | Column | Y1 SOURCE class | R11 GATE class | composes? |
|---|---|---|---|---|
| 1 | `mid_return_1s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 2 | `mid_return_5s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 3 | `mid_return_10s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 4 | `mid_return_30s` | snapshot parquet | OUT OF JURISDICTION | yes |
| 5 | `tick_direction` | snapshot parquet | OUT OF JURISDICTION | yes |
| 6 | `trade_volume_1s` | trades parquet | REQUIRED | yes |
| 7 | `trade_count_1s` | trades parquet | REQUIRED | yes |
| 8 | `dollar_volume_1s` | trades parquet | REQUIRED | yes |
| 9 | `minutes_since_open` | clock-only | OUT OF JURISDICTION | yes |
| 10 | `session_open` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 11 | `session_mid` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 12 | `session_close` | derived (parent `minutes_since_open`, clock-rooted) | OUT OF JURISDICTION | yes |
| 13 | `net_delta_1s` | trades parquet | REQUIRED | yes |
| 14 | `net_delta_5s` | trades parquet | REQUIRED | yes |
| 15 | `net_delta_10s` | trades parquet | REQUIRED | yes |
| 16 | `net_delta_30s` | trades parquet | REQUIRED | yes |
| 17 | `net_delta_60s` | trades parquet | REQUIRED | yes |
| 18 | `buy_volume_10s` | trades parquet | **UNSCORED** — carve-out, §C.4(a) | yes, **via the declared carve-out** |
| 19 | `sell_volume_10s` | trades parquet | REQUIRED | yes |
| 20 | `large_trade_count_10s` | trades parquet | REQUIRED | yes |
| 21 | `vwap_distance` | **MIXED: snapshot + trades** | REQUIRED | yes — **on the trades ground only; see §C.5** |
| 22 | `bid_size_1` | snapshot parquet | OUT OF JURISDICTION | yes |
| 23 | `ask_size_1` | snapshot parquet | OUT OF JURISDICTION | yes |
| 24 | `total_bid_depth` | snapshot parquet | OUT OF JURISDICTION | yes |
| 25 | `total_ask_depth` | snapshot parquet | OUT OF JURISDICTION | yes |
| 26 | `book_imbalance_ratio` | derived (parents `total_bid_depth`/`total_ask_depth`) | **UNSCORED** — carve-out, R16 / §C.4(c) | yes, **via the declared carve-out** |
| 27 | `weighted_mid` | snapshot parquet | OUT OF JURISDICTION | yes |
| 28 | `spread_ticks` | snapshot parquet | OUT OF JURISDICTION | yes |
| 29 | `depth_imbalance` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 30 | `book_slope_bid` | snapshot parquet | OUT OF JURISDICTION | yes |
| 31 | `book_slope_ask` | snapshot parquet | OUT OF JURISDICTION | yes |
| 32 | `depth_change_1s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 33 | `depth_change_5s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 34 | `depth_change_30s` | derived (parents `total_bid_depth`/`total_ask_depth`) | OUT OF JURISDICTION | yes |
| 35 | `l1_imbalance` | derived (parents `bid_size_1`/`ask_size_1`) | OUT OF JURISDICTION | yes |

**RESULT: all 35 compose. NO column is flagged, and there is no flagged row in the table above.**
This was checked **column by column and not by count** — every row was evaluated against the
mechanism paragraph individually, and the two count identities below were computed only
afterwards, from the per-column result. **A non-composing column would have been a FINDING and
would appear above as a flagged row** with its two classifications and the contradiction named:
a trade-touching column classed OUT OF JURISDICTION would mean the gate declares a forward-join
column availability-legal, and a snapshot-or-clock-rooted column classed REQUIRED would mean the
criterion-1 denominator contains a column with no forward join to violate on. Neither occurs.

**THE RECONCILIATION, STATED AS ARITHMETIC.** Both identities were confirmed, not assumed:

> **(1) TRADE-TOUCHING 12 = REQUIRED 11 + `buy_volume_10s` (UNSCORED). CONFIRMED.**
> Trade-touching = trades parquet **11** + MIXED **1** = **12**, enumerated:
> `trade_volume_1s`, `trade_count_1s`, `dollar_volume_1s`, `net_delta_{1,5,10,30,60}s`,
> `buy_volume_10s`, `sell_volume_10s`, `large_trade_count_10s`, `vwap_distance`. Of those,
> **11 are REQUIRED — exactly §A.6.1's list, name for name — 1 is UNSCORED (`buy_volume_10s`),
> and 0 are OUT OF JURISDICTION.** 11 + 1 = 12.
>
> **(2) SNAPSHOT-ROOTED + CLOCK 23 = OUT OF JURISDICTION 22 + `book_imbalance_ratio`
> (UNSCORED). CONFIRMED.** = snapshot parquet **13** + derived **9** + clock-only **1** = **23**.
> Of those, **22 are OUT OF JURISDICTION — exactly §A.6.2's list, name for name — 1 is UNSCORED
> (`book_imbalance_ratio`), and 0 are REQUIRED.** 22 + 1 = 23.
>
> **(3) 12 + 23 = 35**, and the two source buckets are disjoint and exhaustive over the fed set,
> so the two partitions are a clean 2 x 3 cross-tabulation with **four occupied cells**:
> trade-touching x REQUIRED **11**, trade-touching x UNSCORED **1**, snapshot/clock x OUT OF
> JURISDICTION **22**, snapshot/clock x UNSCORED **1**. **The two empty cells are the
> load-bearing ones:** trade-touching x OUT OF JURISDICTION is **empty**, and snapshot/clock x
> REQUIRED is **empty**. Those two zeros are the composition claim.

**A finer reconciliation, which the two partitions also pass.** Inside the 23, the SOURCE cut
separates **clock-rooted 4** (`minutes_since_open` plus the three session flags derived from it —
`raw_source_traced` = "snapshot parquet: timestamp (clock only)" on all four) from **book-rooted
19**. **The clock-rooted 4 are exactly §A.6.2(a)'s four manifest-CLEAN columns**, and the
book-rooted 19 are exactly §A.6.2(b)'s 18 plus `book_imbalance_ratio`. §A.6.2(b)'s 18 in turn
split **13 snapshot-parquet + 5 derived** under the SOURCE cut, and the 5 derived are
`l1_imbalance`, `depth_imbalance`, `depth_change_{1,5,30}s` — **the same five, by name**, that
§C.3 Category 1(b) records as the **5 DESCENDANT** against **13 LEAK-SOURCE**. Two taxonomies
built from different artifacts (Y1's construction trace vs the f3 manifest's construction class)
land on the identical 13 / 5 split. That is a third, independent corroboration and it is recorded
as such rather than as a coincidence.

**What this subsection does NOT do.** It does not re-derive N, change any class, or create a
fourth class. **§A.6.4's partition governs**; this is a consistency check on it, and its only
operative consequence is the pair of empty cells in (3), which is what licenses §13(i)'s
statement that every REQUIRED column is already governed by a `trades_*` class and therefore that
the restricted map drops no adjudicating cell. Derivation script and output:
`s13\s13_crosstab.py`, `s13\s13_crosstab_output.txt`.

---

### A.7 — Criterion 2 — **SATISFIED**

**Registered text, PREREG.md line 460 (verbatim):**

> 2. No **manifest-clean** source column receives **any runtime finding of any tier, primary or secondary**, on `fixture_contaminated`.

**SATISFIED and unchanged.** The manifest-clean set is the 4 clean columns of
`f3\fixture_manifest_DRAFT.json` (`counts.clean: 4`). Two declared dispositions bear on it and
are recorded in §C.4: the **session-flag staleness** quirk (§C.4(b)) is a documented artifact of
the shift and licenses **no** finding, on either side; and `book_imbalance_ratio` (§C.4(c)) is
gate-status **EXCLUDED**. Neither weakens the criterion — both remove a route by which a
non-availability artifact could be scored as one.

---

### A.8 — Criterion 3 — **AMENDED (class C), per working resolution R9**

**Registered text, PREREG.md line 461 (verbatim):**

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

**OLD (quoted from R9, file tail, verbatim):** "no findings on any corrected column".

**NEW (quoted from R9, file tail, verbatim):** "detector findings must match the declared
per-side, per-class, per-instrument-month violation map; findings the map predicts are required,
findings it excludes are false positives, cells the map does not cover are unscored."

**Rationale, recorded (R9, verbatim):** "the tool's own coverage principle (silence and belief
never convert into a pass) applied to its own exam." And: "The corrected side is described
throughout as CHARACTERIZED, never clean."

**What forced it.** The M5 falsification sweep (`m5\`) extended the corrected-side check beyond
ZC 2025-01 and **falsified the assumption that the corrected side is clean** — see §13(f). The
corrected side carries strictly-post-decision absorption in **18 of 48** instrument-months, up
to **111,334 of 580,944 rows (19.16%)** on zc 2025-09 (`n1\summary_corrected.csv`). Criterion 3
as written would fail the gate on a correctly-behaving detector that reports a real violation
the fixture really contains. That is a semantic gap in the acceptance criterion — class C by
PREREG.md line 93 — and it is amended, not waived.

**What the amendment does NOT do.** It does not lower the bar. A finding on a corrected-side
cell the map marks zero is still a false positive and still fails the gate. It does not create
an unscored escape hatch either: the 72 unscored cells (§13(g)) are named as unscored, never as
clean, and they license no pass. The map is declared and frozen before any detector runs (§D.1).

---

### A.9 — Criterion 4, the identity control, and the sentinel statement — **SATISFIED**

**Registered text, PREREG.md line 462 (verbatim):**

> 4. Silent under the identity control on both.

**SATISFIED, with one declaration that must be stated explicitly or the criterion is unsafe:**

> **SENTINEL STATEMENT.** The wrapped `net_delta` values in this fixture — magnitudes near
> 4.29e9, e.g. the observed **4294967291** for a trade of `size` 5 (2^32 − 5) — are **DATA
> CONTENT, not findings.** They are the as-built product of an uncast uint32 negation (§15) and
> are present identically on BOTH sides. The identity control must remain silent on them. A
> detector that fires on the magnitude, the sign, or the 2^32 signature of these values has
> produced a **false positive under criterion 4**, not a detection — availability is a question
> about *when* a cell is knowable, and these values are equally knowable, and equally wrong, at
> every instant on both sides.

Evidence for the sentinel: `t1\t1_final_output.txt` lines 61-67 (the wrapped value observed in
the f2 rebuild); §15 for the defect's provenance and the C5 verdict that the ORIGINAL runs
wrapped identically. Because the defect is present on both sides and in both pipeline
generations, it cannot differentiate them, which is precisely why it must not be allowed to.

---

### A.10 — Gate framing, proof count, and ordering — **SATISFIED, carried unchanged**

**Registered text, PREREG.md line 453 (verbatim):** "**Pass gate — discrimination, not tier.**"
**Line 457 (verbatim):** "Evaluated on the **frozen default configuration**, under the
reconstructed declaration:". **Line 472 (verbatim):** "> **k of N** labelled leaking sources
received at least one primary PROVEN finding **attributed to that source**." **Line 476
(verbatim):** "**It is published as a count, never as a decimal or percentage**, and it is
identified as a descriptive fixture outcome rather than a performance rate." **Line 480
(verbatim):** "**Ordering, locked:** tune on the development corpus → freeze the candidate
configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults
may not be altered after observing a fixture result."

**SATISFIED, all five, carried unchanged.** Three consequences this declaration must honour and
does.

1. **N is 11**, and it is the REQUIRED list of §A.6.1, not the manifest's independent-leak
   count. Line 472's "**k of N** labelled leaking sources" is published against that
   denominator. **N = 25 is withdrawn as the gate's N** — 25 is line 446's manifest DAG count
   and carries no gate arithmetic (§A.2, working resolution R11).
2. **The proof count is published as a count, with its scope named**, per line 476 — and under
   §A.6 "scope" now means the class: a report must say "k of N = 11 REQUIRED columns"; must
   separately report **false positives on the 22 OUT OF JURISDICTION columns** (§A.6.2 — that
   class and no other bears the false-positive consequence); and must separately report
   **findings on the UNSCORED class, which are NOT false positives** — per §C.3 Category 2,
   §C.4(c) ("no finding on it counts for or against any criterion"), §A.6.3 and frozen §D.1
   item 2, a finding on an UNSCORED column counts neither for nor against any criterion and is
   reported as an unscored observation. Never fold any of the three classes into another, and
   never carry the false-positive consequence beyond the 22.
3. **The locked ordering of line 480 binds this file** — §D.1 freezes the map, the partition,
   and every gate-consumed number at the tag, so no number here can be moved after a fixture
   result is observed.

---

### A.11 — Walk summary

| §6.2 element | Line | Verdict |
|---|---|---|
| Reference AUC 0.957/0.675, ±0.010 | 445 | **AMENDED (class C)** — retired; LightGBM trio governs |
| Ground-truth column DAG + independent-leak count | 446 | SATISFIED — count 25, F3 scope governing; **no gate arithmetic attached** (R11); flavor split stated both ways (R13) |
| Declaration reconstructed, evidence before tuning | 447 | SATISFIED |
| Reconstruction in Phase 0, before cross-tool | 448 | SATISFIED |
| Semantic-ambiguity clause | 449 | SATISFIED — clause does not fire |
| Contamination availability class in manifest | 450 | **SATISFIED BY SUBSTITUTE (class C)** — locus amended to this declaration, hashed in the tag |
| Sliced variant for CI | 451 | **AMENDED (class C)** — off the Phase 0 fixture; re-registered as a Phase 1 CI obligation with its scoring rule declared ex ante |
| Pass gate framing; frozen default config | 453, 457 | SATISFIED |
| Criterion 1 | 459 | SATISFIED — **denominator re-derived from the declared map (R11); N = 11**; three-class partition summing to 35 |
| Criterion 2 | 460 | SATISFIED — scope is manifest-CLEAN columns only; the §C.3 mis-routing is deleted |
| Criterion 3 | 461 | **AMENDED (class C) per R9** — scored against the declared map |
| Criterion 4 (identity control) | 462 | SATISFIED — with the 4.29e9 sentinel statement |
| Descendants secondary; top-k; alias | 464, 468 | SATISFIED |
| k-of-N proof count, published as a count | 470-476 | SATISFIED — **N = 11** |
| Ordering, locked | 480 | SATISFIED — enforced by §D.1 |

**Four amendments (445, 450, 451, 461). NO registered §6.2 element is left NOT MET, and none is
left "outstanding".** Every element is now either SATISFIED as registered, AMENDED with the old
text quoted and the new text stated, or SATISFIED BY SUBSTITUTE with the substitute named and
shown to bind at least as hard. Everything not in the amended four stands exactly as registered.
All four amendments are class C under PREREG.md line 93 and are carried by this registration
under line 95; all are PROVISIONAL until the `prereg-v30a` tag is signed.

---

### A.12 — "Waived", defined for §10.2's replacement-criterion floor (finding RS-3) — **class C amendment content added by v30a**

**Outside §6.2 and stated here because the walk is where amendment content lives.** This
subsection defines one word. It adds a defining clause to a locked floor that uses the word
without one; it changes no threshold, exempts nothing, and narrows nothing.

**Registered text, PREREG.md line 1035 (verbatim):**

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

Context, PREREG.md line 1033 (verbatim), which is what that floor floors:

> On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**The gap (RS-3).** "Waived" appears in the floor with no defining clause anywhere in the
registration. It appears once more, at PREREG.md line 855, as a **detector-case coverage
state** in §7.7's vocabulary table — also undefined. An undefined term inside a floor that
exists to stop criteria being dropped silently is the exact shape of a term that gets read
permissively later. **The two runtime detectors the floor governs are L2a and L3.1** (PREREG.md
lines 318, 320; line 1039 names "both of L2a/L3.1's combinations").

**DEFINITION, declared.**

> A runtime detector is **WAIVED** with respect to a criterion when the criterion is written,
> configured, or reported in any way that makes the detector's own result incapable of changing
> the criterion's outcome. Concretely, a detector is waived if any of the following holds:
> **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but
> its findings are not required to be non-empty for a pass, so its contribution is optional;
> **(iii)** the criterion can be satisfied by the other detector's output alone; **(iv)** its
> threshold is set at a level it meets without executing, or by construction; or **(v)** its
> cases are reported under §7.7's `waived` coverage state rather than executed to a terminal
> result.

**WHAT INVOKING IT REQUIRES: nothing, because it may not be invoked.** The floor is a
prohibition, not a permission with conditions. **There is no procedure by which either runtime
detector may be waived in a §10.2 replacement criterion.** A replacement criterion that waives
one is *weaker than the floor* and is out of specification on its face; it does not become
admissible by being recorded, disclosed, justified, or approved. Changing that requires amending
line 1035 itself — a further class C amendment, committed and timestamped before the affected
detector is implemented or evaluated (PREREG.md line 95).

**WHAT THIS DEFINITION DOES NOT PERMIT — stated so it cannot be read as a general escape:**

1. **It is not an escape hatch of any kind.** The definition creates no exception, no
   "justified waiver", no reviewer-approved waiver and no time-limited waiver. It exists only
   to make a prohibition checkable.
2. **It does not reach any other criterion.** It defines the word for §10.2's
   replacement-criterion floor and for §7.7's coverage state. It says nothing about §6.2's four
   acceptance criteria, and it may not be cited to soften them.
3. **"Experimental" is not "waived", and may not become it.** §10.2 criterion 3 can ship a
   detector or mode marked experimental and exclude it from `assert_no_proven_leakage()`. That
   changes how findings are *labelled and asserted on*; it does not remove the detector from a
   replacement criterion's denominator. A criterion that drops a detector *because* it was
   marked experimental has waived it.
4. **"No data" is not "waived".** A cell with no data is **UNSCORED**: ledgered by name and
   path, entering no denominator, contributing to no rate, and **never reported as a pass**
   (§13(g), §A.6.3). The detector is still scored wherever data exists. Converting an unscored
   cell into a pass is the failure mode R9's rationale names, and doing it at the level of a
   whole detector is a waiver.
5. **A working resolution or `DEVIATIONS.md` entry cannot do it.** §D.3 forbids a decision-log
   interpretation from weakening a locked obligation, and PREREG.md line 1033 forbids a
   `DEVIATIONS.md`-only criterion outright.
6. **Per-combination waiving is still waiving.** Line 1039 applies gates per combination;
   dropping a detector from one combination's criterion while scoring it in another waives it
   for that combination, and is class C.
7. **It does not license anything after tuning.** The whole floor exists ex ante — line 1035's
   own closing sentence: a criterion chosen because it works after tuning is a criterion shaped
   by tuning.

**Status:** class C amendment content added by v30a, PROVISIONAL until the `prereg-v30a` tag is
signed, and frozen by §D.1 thereafter. It is an *addition of a defining clause*, and by §D.3's
rule it resolves toward the stronger reading: every ambiguity in "waived" is resolved against
the party that would benefit from dropping a detector.

SOURCE: AVAILABILITY_DECLARATION.md lines 1946-2518

## 13. The DECLARED GROUND-TRUTH MAP (element f; R9) — the corrected side is CHARACTERIZED, never clean

> **MEASURED ON ARTIFACT A** (§0.1) — every cell of the map is an event-to-row timing
> measurement on the lineage's lattice and event parquets. **APPLIED TO ARTIFACT B** through
> the §0.2 lattice bridge: the map is the key the gate scores Artifact B's findings against.
> Both halves of that sentence must appear wherever a map number is quoted.

**This section replaces the former "corrected-side zero".** That claim was falsified by
measurement (subsection (f)); working resolution R9 (file tail, verbatim) is the authority for
what stands in its place: "The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on
both fixture sides, not against an assumed-clean corrected side."

### (a) What the map is, and where it lives

**Artifact: `n1\declared_map.csv`.** One row per scored cell, schema
`side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag,
missing_path`. Read this pass: **984 rows** = **960 declared-class cells** (2 sides x 8
instruments x 6 months x 10 classes) **plus 24 rows carrying the 11th diagnostic class**
`mbo_all_rows`. Of the 960: **888 `SCORED`** and **72 `UNSCORED_FOR_LACK_OF_DATA`**; the 24
diagnostic rows are flagged `SCORED_DIAGNOSTIC_11TH_CLASS`. Boundary is `decision_T` on every
row. Scope: 8 instruments (cl, es, gc, he, le, nq, zc, zs) x 6 months (2025-01, 2025-08,
2025-09, 2025-10, 2025-11, 2025-12) = 48 instrument-months.

**The declared 10 classes** are trades_all, trades_buy, trades_sell, trades_large, mbo_all,
mbo_bid_add, mbo_ask_add, mbo_bid_cancel, mbo_ask_cancel, mbo_cancel_any.

> **CLASS-SET RULE, binding.** `mbo_all_rows` is an **11th diagnostic class and is NOT one of
> the declared 10.** Any statement of the form "max across classes" in this file or in any gate
> report **must name the class set it maximises over.** Two M5-quoted maxima came from the
> diagnostic class and differ from the declared-10 maximum: **cl 2025-01 corrected strict —
> 54,341 over the M5 class set (`mbo_all_rows`) vs 53,249 over the declared 10 (`mbo_all`)**;
> **es 2025-01 corrected equal — 6 over the M5 class set (`mbo_all_rows`) vs 4 over the declared
> 10 (`mbo_all`)**. Both are the same measurement reported over different class sets, not a
> disagreement: `n1\compare_to_m5_output.txt` records **453 of 453 M5 cells matched, 0
> disagreeing cells, 0 quoted-maxima disagreements** once the class set is named. Companion
> artifact: `n1\m5_maxima_comparison.csv` (columns `s10`/`e10` = declared-10, `sM5`/`eM5` = M5
> class set).

Companion artifacts: `n1\summary_corrected.csv`, `n1\summary_contaminated.csv` (per
instrument-month maxima over the declared 10, with `rows` and `max_strict_frac`),
`n1\lattice_profile.csv` (per instrument-month lattice profile), `n1\unscored_ledger.csv`
(the 72 unscored cells), `n1\full_map_all_boundaries.csv`, `n1\run_logs.json`.

### (b) The corrected side, stated honestly

**The corrected side carries strictly-post-decision absorption in 18 of the 48
instrument-months** (`n1\summary_corrected.csv`, `max_strict` > 0): **cl all 6 months, gc all 6
months, zc 2025-08/-09/-10, zs 2025-08/-09/-10**. Peak: **zc 2025-09, 111,334 strict of 580,944
corrected rows = 19.16%** (`max_strict_frac` 0.191643) on class `mbo_all`, and zc 2025-09 is the
peak under BOTH metrics.

**THE RANKING BELOW IS BY RATE**, i.e. by `max_strict_frac` = `max_strict` / `rows`, descending.
**The metric is named because the rate order and the absolute-count order are different orders**,
and any list of these cells that does not name its metric is unreadable. `argmax_strict` is
`mbo_all` on all 18 and `classes_scored` is 10 on all 18. Derived from
`n1\summary_corrected.csv` (rows with `max_strict` > 0), reproduced cell-for-cell with zero
disagreement by `y1\trade_class_only_map.csv` (`max_strict_declared10`, `rows`, side =
`corrected`). All 18 are listed — the set is small enough that a top-N would only re-create the
truncation defect this table replaces.

| rate rank | instrument-month | strict | corrected rows | rate (`max_strict_frac`) | absolute rank |
|---|---|---|---|---|---|
| 1 | zc 2025-09 | 111,334 | 580,944 | **19.16%** (0.191643) | 1 |
| 2 | zc 2025-10 | 109,332 | 634,445 | 17.23% (0.172327) | 2 |
| 3 | zc 2025-08 | 90,868 | 554,303 | 16.39% (0.163932) | 3 |
| 4 | zs 2025-08 | 64,404 | 465,381 | 13.84% (0.13839) | 5 |
| 5 | zs 2025-10 | 60,559 | 508,910 | 11.90% (0.118997) | 6 |
| 6 | zs 2025-09 | 45,255 | 429,465 | 10.54% (0.105375) | 11 |
| 7 | gc 2025-10 | 71,584 | 772,447 | 9.27% (0.092672) | 4 |
| 8 | gc 2025-09 | 59,691 | 734,280 | 8.13% (0.081292) | 7 |
| 9 | cl 2025-11 | 48,607 | 703,999 | 6.90% (0.069044) | 10 |
| 10 | cl 2025-01 | 53,249 | 801,410 | 6.64% (0.066444) | 8 |
| 11 | gc 2025-12 | 49,649 | 772,202 | 6.43% (0.064295) | 9 |
| 12 | gc 2025-08 | 42,886 | 692,041 | 6.20% (0.06197) | 12 |
| 13 | cl 2025-10 | 42,377 | 745,569 | 5.68% (0.056838) | 13 |
| 14 | cl 2025-12 | 38,945 | 768,531 | 5.07% (0.050675) | 14 |
| 15 | cl 2025-09 | 34,010 | 687,658 | 4.95% (0.049458) | 16 |
| 16 | gc 2025-01 | 37,065 | 761,736 | 4.87% (0.048659) | 15 |
| 17 | gc 2025-11 | 30,577 | 674,038 | 4.54% (0.045364) | 17 |
| 18 | cl 2025-08 | 27,852 | 664,076 | 4.19% (0.041941) | 18 |

**The two orders diverge, which is the whole reason the metric must be named:** zs 2025-09 is 6th
by rate and 11th by absolute; gc 2025-10 is 7th by rate and 4th by absolute; cl 2025-01 is 10th by
rate and 8th by absolute. **Under the ABSOLUTE metric the top five are** zc 2025-09 (111,334),
zc 2025-10 (109,332), zc 2025-08 (90,868), gc 2025-10 (71,584), zs 2025-08 (64,404).

> **WITHDRAWN: the earlier prose list** "Next: zc 2025-10 …; zc 2025-08 …; zs 2025-08 …; gc
> 2025-10 …". **Every number in it was correct; the ORDERING was not a ranking under either
> metric** — it ran zs 2025-08 (64,404) ahead of gc 2025-10 (71,584), which is not absolute
> order, and it terminated at gc 2025-10 (9.27%) while omitting **zs 2025-10 (60,559 of 508,910 =
> 11.90%)** and **zs 2025-09 (45,255 of 429,465 = 10.54%)**, both of which outrank gc 2025-10 by
> rate. The table above replaces it; no truncated restatement of it may be quoted.

**Equal counts, stated precisely:** `equal_count` is non-zero in **35 of 48** instrument-months;
of those, **17 are equal-only** (equal > 0 with strict == 0) and the other 18 are the
strict-positive cells above. That leaves **13 instrument-months with zero strict and zero equal
over the classes that are SCORED for them**. 18 + 17 + 13 = 48.

> **"Clean on both branches" is WITHDRAWN as a pass claim for the six nq months (working
> resolution R12).** The arithmetic above is a measurement and stands; the *label* does not.
> Zero-over-scored-classes is not the same predicate as zero-over-the-declared-10, and for nq
> the two differ by six unscored classes per month. The 13 rows below are therefore listed as
> **measured-zero over their scored classes**, with the scored-class count named on every row.
> Seven of the thirteen are zero over all ten declared classes; six — every nq month — are zero
> over four. **No row in this table may be quoted as a pass, and the six nq rows may not be
> quoted as evidence of cleanliness at all.**

**The 13 measured-zero instrument-months, named, with their scored-class count:**

| instrument-month | corrected rows | note |
|---|---|---|
| nq 2025-01 | 598,227 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 MBO classes UNSCORED, not zero. NOT a pass.** |
| nq 2025-08 | 540,530 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-09 | 549,430 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-10 | 590,785 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-11 | 550,463 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| nq 2025-12 | 620,107 | **TRADES-CLASSES-ONLY — 4 of 10 scored; 6 UNSCORED, not zero. NOT a pass.** |
| zc 2025-01 | 338,158 | all 10 classes scored (see (e)) |
| zc 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-01 | 337,844 | all 10 classes scored |
| zs 2025-11 | 304,505 | all 10 classes scored |
| zs 2025-12 | 353,103 | all 10 classes scored |
| he 2025-11 | 304,486 | all 10 classes scored |
| le 2025-11 | 304,491 | all 10 classes scored |

> **The six nq cells are NOT evidence of cleanliness.** `n1\summary_corrected.csv` records
> `classes_scored = 4` for every nq month: **nq's coverage in this map is TRADES-CLASSES-ONLY**
> — `trades_all`, `trades_buy`, `trades_sell`, `trades_large`. Its six MBO classes are
> **UNSCORED, not zero.** Reading "nq is clean" off this table is exactly the inference R9
> forbids.
>
> **The reason, restated correctly — it is NOT that no data exists, and it is NOT that no
> same-generation data exists** (R12, whose stated reason §13(h) supersedes on measured
> evidence). The earlier draft said the NQ MBO data does not exist; R12 replaced that with "no
> same-generation data". Both are false and are corrected here. **NQ MBO exists in the archive in
> TWO generations — one of them the fixture's own v3 — and what does not exist is an MBO file AT
> THE FIXTURE PATH.** `phase5_ml.py`'s `get_data_dir` resolves to `PROC/sym` = `processed\nq\`
> (because `C:\MBO_data` does not exist), and that directory holds **no MBO file of any
> generation** — which is exactly the file `n1\unscored_ledger.csv` records as missing
> (`missing_path` = `...\processed\nq\nq_mbo_{month}.parquet`, 6 rows, 12 cells each). The two
> families that do exist are **v4_gapfill** per-day parquets under
> `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\v4_gapfill\nq_mbo_YYYY-MM\` and
> **same-generation `v3_pre_gapfill`** month files under
> `pc2_transfer\processed\nq\nq_mbo_{month}.parquet` — a path the builder never reads (§13(h),
> verified this pass). **NQ's six MBO classes are therefore UNSCORED because the fixture path
> carries no MBO file**, and adopting either family into the acceptance denominator is class C.
>
> Both joins are worth having and both run as a **declared non-gated diagnostic** — §13(h). The
> v4 join is additionally **cross-generation**: §B.4's generation defect is precisely a
> lattice-timestamp defect, so the two generations do not share a row-to-second correspondence
> and a v4-event / v3-lattice count reports the mismatch as well as the fixture. The v3 join is
> the same-generation control. Neither is in the acceptance denominator, and moving either there
> later is class C.

### (c) The contaminated side is saturated — all 48

`n1\summary_contaminated.csv`: **`max_strict` > 0 in all 48 instrument-months**, with
`max_strict_frac` from **0.2545** (le 2025-11, 77,483 of 304,492) to **0.9893** (es 2025-12,
613,447 of 620,108) — i.e. between roughly 25% and 99% of rows. By instrument:
es **0.960-0.989**, nq **0.830-0.908**, gc 0.667-0.837, cl 0.592-0.706, zc 0.538-0.752,
zs 0.583-0.637, he 0.288-0.391, le 0.254-0.417. `classes_strict_gt0` is 9 of 10 on every non-nq
instrument-month (trades_buy is dead-zero — §C.4(a)) and 3 of 4 on nq. The two sides are
therefore separated everywhere in the map by one to three orders of magnitude, which is what
makes the fixture a discrimination fixture at all.

### (d) The cohort predicate (item N3) — necessary, NOT sufficient

**`floor(T_i) == floor(T_{i-1})`** — row `i` shares a wall-clock second with its predecessor.

**Coverage: 5,305,430 of 5,305,430 corrected strict violations — 100.000%, with ZERO
exceptions.** `n3\predicate_check.csv` (456 scored cells), summed this pass: `strict_viol` =
5,305,430, `same_second_viol` = 5,305,430, `exception_viol` = 0. `n3\exceptions.csv` is a
header line with no rows. `n3\invariants.txt` records both invariants — `same_second_viol <=
cohort_size` and `strict == same_second + exception` — violated in **0 cells**. (That total is
over the 11-class set including `mbo_all_rows`; the per-class breakdown is in
`n3\invariants.txt`.)

**NECESSARY, NOT SUFFICIENT — stated as a limit, not a hedge.** The cohort is **1,966,088 rows
of 24,768,472 corrected rows (7.94%)**; a lower bound on how many cohort rows actually violate
in some class is **1,024,196** (`n3\converse_by_instrument_month.csv`, column
`LOWERBOUND_cohort_rows_violating_in_some_class`, summed over 48 instrument-months), leaving up
to **941,892** cohort rows that violate in no class (`UPPERBOUND_cohort_rows_violating_in_no_class`).
So membership in the cohort does not imply a violation; **non-membership does imply no
violation.** Outside the cohort the headroom is strictly negative in every measured cell — the
tightest are zs 2025-08 mbo_all at **−3 ns** and le 2025-11 mbo_all at **−5 ns**
(`max_ts_event_minus_T_outside_cohort_ns`), i.e. the absorbed window ends before the decision
time by nanoseconds, but it does end before it.

**The predicate is checkable from the lattice alone — no event data.** It reads only the
`timestamp` column of the snapshot frame. That is what makes it usable as a **declared cohort
definition** in §C rather than as a post-hoc description. `n3\cohort_profile.csv` also records
**0 non-monotonic rows and 0 floor-decreasing rows** across all 48 instrument-months, so the
cohort is well-defined everywhere. Cross-checks: `n3\compare_output.txt` — 456 of 456 cells
matched against `n1\declared_map.csv` with 0 disagreements; 151 of 151 matched against M5 with 0
disagreements; 48 of 48 instrument-months agreeing on `cohort_size`/`corrected_rows`.

### (e) The ZC 2025-01 zero survives — as ONE CELL of the map, with its pedigree intact

**Scoped claim: on ZC 2025-01 the corrected side is 0 strict + 0 equal against decision time,
for all 10 event classes, over all 338,158 corrected rows — including all 28 re-anchor gap
rows.** (Lattice 338,159 rows, generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` — §2 naming rule.) This cell
is measured by TWO independent implementations with exact agreement at every count:

- **T1 (pandas):** `t1\violation_table.csv` (`corrected` / `decision_T` rows: strict=0,
  equal=0 for every class); gap-row restriction all zeros for all 10 classes
  (`t1\t1_final_output.txt` line 19).
- **C4 (polars 1.43.2, blind):** T1's implementation and outputs unread; no target numbers
  in the tasking; the 338,159-row lattice independently derived from the snapshots parquet
  plus the builder filter definition (exact row match); a second internal cross-check
  method (event-level join) agreed exactly. `c4\independent_counts.csv` (`decision_T`
  rows: strict_count=0, equal_count=0, gap_row_subset_strict=0, gap_row_subset_equal=0 for
  all 10 classes).

Orchestrator comparison: no disagreement at any published count; no stop-and-report
condition (`R2_consolidated_report.md` C4 section). N1 and M5 both reproduce the cell exactly.

**The pedigree is unchanged; only its SCOPE is.** What it licenses is a statement about one
cell — and the mechanism is now understood: ZC 2025-01's lattice is a **single native block with
0 overlapping block pairs and 0 excess rows** (§B.4), so its same-second cohort is **empty**
(`n1\lattice_profile.csv`: `same_second_rows` = 0; `n3\cohort_profile.csv`: `cohort_size` = 0),
and by (d)'s predicate an empty cohort forces zero violations. The cell is clean *because of a
generation property of that month's file*, not because the lag fix is universally sufficient.
Extending it to the corrected side as a whole was the error M5 caught.

### (f) The M5 falsification sweep — cited per K3 as the measurement that forced R9

`m5\` is the round that extended the corrected-side check beyond ZC 2025-01 and **falsified**
it. What it measured: the same strict/equal violation counts at boundary `decision_T`, on both
sides, for 16 instrument-months (8 instruments x 2025-01 and 2025-08), over the per-class event
sets, with per-instrument logs and a spot-check verification of individual violating rows.
Artifacts: `m5\per_instrument_counts.csv` and `m5\per_instrument_counts_detail.csv` (the cell
counts), `m5\corrected_decisionT_summary.csv` (the headline — the table on which cl 2025-01
first showed corrected strict 54,341 and zc 2025-08 showed 90,868), `m5\counts_{inst}_{month}.csv`
and `m5\log_{inst}_{month}.json` (per-cell), `m5\verify_violating_rows.py` /
`m5\verify_violating_rows_output.txt` / `m5\spot_check.txt` (row-level verification: a named
cl 2025-01 trades_all row at T_i = 2025-01-02 13:01:11.865879 absorbing a trade at
13:01:11.914518, **48,638,830 ns after the decision time**), `m5\verify_zc_vs_c4.txt` (the ZC
2025-01 cell re-verified against C4). Its stop-and-report is preserved as evidence, per K3.

N1 supersedes M5 in coverage (48 instrument-months vs 16, both sides, with unscored cells
ledgered) and **reproduces every one of M5's 453 cells exactly** — 0 disagreements
(`n1\compare_to_m5_output.txt`). M5 is not superseded as the *reason*: it is the measurement
that made R9 necessary, and it is cited as such.

### (g) The 72 unscored cells are UNSCORED — never clean

**72 of the 960 declared-class cells are `UNSCORED_FOR_LACK_OF_DATA`**: nq's 6 MBO classes
(mbo_all, mbo_ask_add, mbo_ask_cancel, mbo_bid_add, mbo_bid_cancel, mbo_cancel_any) x 6 months
x 2 sides = 72.

**Cause, stated correctly: NO MBO FILE AT THE FIXTURE PATH — not "no data exists", and not "no
same-generation data" either** (R12, whose stated reason §13(h) supersedes on measured evidence).
`phase5_ml.py`'s `get_data_dir` resolves to `PROC/sym` = `processed\nq\` (because `C:\MBO_data`
does not exist), and `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\nq\nq_mbo_{month}.parquet`
does not exist — that directory holds **no MBO file of any generation**. The `missing_path`
column names that exact absent file for each cell (`n1\unscored_ledger.csv`, 6 rows, `n_cells` =
12 each). **NQ MBO data does exist in the archive, in TWO families, neither of which the builder
reads**: `v4_gapfill` per-day parquets under `processed\nq\v4_gapfill\nq_mbo_YYYY-MM\`, and
**same-generation `v3_pre_gapfill`** month files under
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet` (§13(h) items 1-2, verified this pass).
Adopting either family into the acceptance denominator is a class C amendment; the v4 family
would in addition require a cross-generation join whose counts report the generation mismatch as
well as the fixture (§13(b), §13(h)). **Any statement of this cause that says "no NQ MBO data
exists", or that says same-generation NQ MBO data is absent, is wrong and is withdrawn.**

**Gate consequence, declared:** an unscored cell **requires no finding and forbids none**. It
enters no denominator, contributes to no rate, and **cannot be reported as a pass**. A gate
report that counts the 72 as "clean" — or that quietly folds them into a corrected-side
cleanliness statement — has converted absence of data into evidence, which is the failure mode
R9's rationale names ("silence and belief never convert into a pass"). Whenever nq appears in
any table in this file or in any gate output, it must carry the **TRADES-CLASSES-ONLY** label
together with the correct reason: **no MBO file at the fixture path `processed\nq\`** — where
`get_data_dir` resolves because `C:\MBO_data` is absent — and never "no data exists" and never
"no same-generation MBO data". Same-generation MBO **does** exist, at
`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`, a path the builder never reads; adopting
either that family or the v4 family into the acceptance denominator is class C. The
TRADES-CLASSES-ONLY label is required on every such appearance regardless.

### (h) NON-GATED DIAGNOSTIC — the NQ cross-generation MBO measurement (item X4)

**This subsection is NOT part of the gate. Nothing in it enters any acceptance criterion, any
denominator, any rate, or the §D.1 freeze as a gate-consumed number.** It is separated from
(a)-(g) for exactly that reason, and it is labelled at every point of use.

**What it is.** §13(g) records that nq's six MBO classes are unscored because **the fixture path
`processed\nq\` holds no MBO file of any generation** — not because the archive lacks NQ MBO, and
not because it lacks same-generation NQ MBO; the PREMISE CORRECTION below supersedes R12's stated
reason on measured evidence. The information is nevertheless worth having, so the measurement is
run against the archive's out-of-path MBO families and reported here as a **declared non-gated
diagnostic** under working resolution R12: v4 NQ MBO events
(`processed\nq\v4_gapfill\nq_mbo_YYYY-MM\nq_mbo_YYYYMMDD.parquet`), with the same-generation v3
month files (`pc2_transfer\processed\nq\nq_mbo_{month}.parquet`) as a control, measured against
the v3 fixture lattice, on the same strict/equal/`decision_T` definitions as the map.

**What it can and cannot support.**

- It **cannot** satisfy criterion 1, cannot convert any of the 72 unscored cells into scored
  cells, and cannot be quoted as a pass or a fail for nq.
- Its counts are **cross-generation**: the v3 lattice carries the §B.4 timestamp defect and the
  v4 lattice does not, so a v4-event / v3-lattice join reports a quantity that mixes the
  overhang with the generation mismatch. It is a diagnostic of *whether an MBO overhang is
  present at all* on nq, not a measurement of the fixture's own MBO overhang.
- **Moving it into the acceptance denominator later is class C** (PREREG.md line 93), not a
  working resolution and not a `DEVIATIONS.md` entry.

**Results (folded in by the orchestrator, 2026-08-12, from item X4; artifacts under `x4\`).**

**PREMISE CORRECTION — R12's stated reason is superseded by X4's own search, and this is the
third and (as measured) final statement of it. Recorded here as fact; the tail record of R12 is
append-only and is not edited.** R12 gives the reason for not gate-scoring nq MBO as "no
same-generation MBO data: the available NQ MBO is v4_gapfill". X4's exhaustive walk of the
archive root (26,596 files, 262 `nq*mbo*.parquet` hits) found **two** families, not one:

1. **v4** — `processed\nq\v4_gapfill\nq_mbo_{month}\nq_mbo_YYYYMMDD.parquet`, 250 per-day files,
   mtime 2026-04-16. (This is the family that falsified the earlier "no data exists" wording.)
2. **v3, same generation as the fixture lattice** — `pc2_transfer\processed\nq\nq_mbo_{month}.parquet`,
   12 month files, mtime 2026-03-31/04-01. Generation verified two ways: the sibling
   `pc2_transfer\processed\nq\nq_snapshots_2025-08.parquet` and the fixture-path
   `processed\nq\nq_snapshots_2025-08.parquet` share sha256
   `1A200A3A71A597C84E869D0CE647195B86250C0D28E3D0C813A3AAF40F1304D7`, and its build stamps
   interleave with the v3 snapshots/trades and precede every v4 artifact.

So the correct reason nq MBO is not gate-scored is **not** that same-generation data is absent.
It is that **the fixture path has no MBO file**: `phase5_ml.py`'s `get_data_dir` resolves to
`PROC/sym` = `processed\nq\` (because `C:\MBO_data` does not exist), and that directory contains
no MBO file of any generation. The v3 month files sit at a path the builder never reads.
Adopting either family into the acceptance denominator is a **class C amendment** — not
performed, not authorized here; `n1\unscored_ledger.csv` is untouched.

**Provenance fact recorded in passing:** no MBO file of either generation is covered by any
manifest in the archive — neither `PC2_TRANSFER_v4\manifest.csv` nor either `checksums.txt`. The
MBO layer is unattested archive-wide.

**Join soundness (measured before any count was reported).** The generational difference is not
a different event set on shared days but a smaller DAY set:

- Day coverage: the v4 day set is a strict subset of the lattice's — 126 of 154 dates, with
  `v4_only = 0` in every month. 78,353 of 3,449,548 lattice rows (2.272%; 5.824% in 2025-11) sit
  on v4-uncovered dates and therefore score as non-violating by construction, so **every v4
  contaminated strict count is a lower bound**. 24 of the 28 uncovered dates are thin spillover
  or Sunday-reopen fringes; **four are real sessions** — MLK 2025-01-20, Labor Day 2025-09-01,
  Thanksgiving 2025-11-27 and 11-28 — which alone are 63,448 (81%) of the uncovered rows. The
  hole is intrinsic to the v4 generation (its own snapshot lattice carries the same day set),
  not a transfer defect.
- Event counts on the 126 shared days: v4 exceeds v3 by **+0.12% to +0.19%** every month, per-day
  never negative (min +0.066%, median +0.154%, max +0.307%) — consistent with gap-fill adding
  rather than replacing.
- Timestamp alignment on covered days: session start agrees to the minute on 126 of 126; session
  end on 105 of 126, with the 21 exceptions characterized (14 are a 0.07-second overshoot at
  early closes; 6 are v3-lattice truncation confirmed by the v3 MBO source ending at the same
  point; 1 is a genuine v4 overrun).
- Soundness test: restricting **both** joins to the 126 v4-covered days collapses the
  cross-generation deficit — max |strict delta| from 27,194 to **745** (0.14%, the same order as
  the event-count delta) and max |equal delta| from 217 to **1**. The worst unrestricted delta is
  entirely the two Thanksgiving sessions.

**Corrected side, boundary decision_T: `strict_count = 0` in EVERY cell** — all six declared MBO
classes plus the diagnostic `mbo_all_rows`, all six months, under **all four joins** (v4, v3
same-generation, and both day-restricted). Corrected rows 598,227 / 540,530 / 549,430 / 590,785 /
550,463 / 620,107. `equal_count` is **0–7** per class (v4 `mbo_all` 5/5/5/5/3/5; v3 6/7/5/5/3/5;
the maxima are 6 in the v4 map at 2025-12 `mbo_all_rows` and 7 in the v3 map at 2025-08, on both
`mbo_all` and `mbo_all_rows`), **bounded by the lattice's 3–7 same-second rows per month**
(6/7/5/5/3/6) — the range and bound `x4\join_soundness.md` states. **The day hole cannot be masking
a corrected-side violation**, because the same-generation source that does cover those dates also
reports 0.

**Contaminated side, v4 join, `mbo_all` strict (rate on the full v3 lattice denominator):**
573,849 (95.92%) / 524,025 (96.95%) / 523,307 (95.25%) / 576,402 (97.57%) / 516,516 (93.83%) /
614,563 (99.11%) for 2025-01/08/09/10/11/12. All-class v4 rate range 93.01%–99.26%; on the
day-restricted denominator 96.00%–99.71%, so the sub-94% cells are the day-hole artifact, not a
lower contamination rate. **v3 same-generation control** (no day hole, the sounder of the two but
equally non-gated): `mbo_all` strict 588,354 (98.35%) / 523,573 / 532,341 / 576,194 / 543,253 /
614,564 (99.11%), all-class range 94.58%–99.26%.

Artifacts: `x4\nq_mbo_diagnostic.csv` (the mandated deliverable), `x4\join_soundness.md`,
`x4\nq_mbo_v3_same_generation_map.csv`, `x4\restricted_to_v4_covered_days_{v4,v3}source.csv`,
`x4\per_day_coverage.csv`, `x4\soundness_{a,b}_*.csv`, `x4\v4_vs_v3_count_delta.csv`, run logs.

### (i) BOTH MAPS, published side by side — the full-class map AS MEASURED and the fixture-universe-restricted map (R17(ii))

**The obligation, stated first.** Delta-issued working resolution **R17(ii)** requires both maps
to be published side by side with the delta explicit. **Neither replaces the other.** The
full-class map is the measurement and is what `n1\declared_map.csv` contains; the restricted map
is a re-aggregation of that same artifact over a narrower class set, adding no new measurement
and changing no cell. Source for the restricted figures: `y1\trade_class_only_map.csv` (96 rows
= 48 instrument-months x 2 sides, both class scopes on every row), re-derived from
`n1\declared_map.csv` by `y1\y1_trade_class_map.py`.

**THE RESTRICTED MAP'S JUSTIFICATION — BY THE COLUMN-UNIVERSE CRITERION ALONE (R17(i)).**

> **No fixture column consumes the MBO event source.** `phase7_l2_sim.py` opens exactly **two**
> data files in the whole script — `{sym}_snapshots_{month}.parquet` (path L135, read L139) and
> `{sym}_trades_tagged_{month}.parquet` (path L199, read L201) — and opens no MBO parquet and no
> MBO aggregate anywhere. `ALL_L2_FEATURES` (L108) contains **none** of the ten MBO-derived
> Phase 5 columns. The script asserts its own scope four times: L4 "L2 features only (no L3/MBO
> cancel/add/rate features).", L57 "# L1 + L2 FEATURE DEFINITIONS (35 total, NO L3/MBO
> features)", L128 "Build L1+L2 features for one month. NO L3/MBO features.", and L549
> `assert len(features) == 35`. Column by column, all 35 trace to: snapshot parquet **13**,
> trades parquet **11**, snapshot-derived **9**, clock-only **1** (`minutes_since_open`), MIXED
> snapshot+trades **1** (`vwap_distance`). **MBO-fed: 0 of 35.** Evidence:
> `y1\column_universe.csv` (35 rows, each with its construction quote and upstream line
> numbers); Y1 §1.1, §2, §3.1, §3.2.
>
> **The criterion follows from that alone:** a map class whose event source no fixture column
> consumes cannot bear on any fed column, so the scored surface that corresponds to the
> fixture's column universe is the four **trade** classes — `trades_all`, `trades_buy`,
> `trades_sell`, `trades_large`.

**This justification makes no reference to what the restriction does to any count, and none may
be added to it.** R17(i) requires the criterion to stand on the column universe by itself,
because a restriction adopted for its effect on a number is a restriction shaped by that number
— the same failure PREREG.md line 480 forbids in the large. The counts are stated below, as a
separate factual matter, and are not part of the reason.

**MAP 1 vs MAP 2 — CORRECTED SIDE.**

| Statistic (over SCORED cells) | Full-class map AS MEASURED (declared 10) | Fixture-universe-restricted map (4 trade classes) |
|---|---|---|
| strict-positive instrument-months | **18 / 48** | **18 / 48 — the SAME 18 cells** |
| `equal_count` non-zero | **35 / 48** | **11 / 48** |
| equal-only (equal > 0, strict == 0) | **17 / 48** | **2 / 48** — `es 2025-10`, `es 2025-11` |
| zero strict AND zero equal | **13 / 48** | **28 / 48** |
| partition check | 18 + 17 + 13 = **48** | 18 + 2 + 28 = **48** |
| peak strict by fraction | **zc 2025-09, 111,334 / 580,944 = 19.16%** (class `mbo_all`) | **zc 2025-10, 34,492 / 634,445 = 5.44%** |
| peak strict by absolute count | zc 2025-09, 111,334 | gc 2025-10, 37,913 / 772,447 = 4.91% |

**MAP 1 vs MAP 2 — CONTAMINATED SIDE.**

| Statistic (over SCORED cells) | Full-class map AS MEASURED (declared 10) | Restricted map (4 trade classes) |
|---|---|---|
| strict-positive instrument-months | **48 / 48** | **48 / 48** |
| `equal_count` non-zero | **42 / 48** | **23 / 48** |
| equal-only | 0 / 48 | 0 / 48 |
| zero strict AND zero equal | 0 / 48 | 0 / 48 |

**The 18 strict-positive corrected cells, both maps, cell by cell.** The cell set is identical;
only the magnitudes differ. (`corrected rows` from `y1\trade_class_only_map.csv`, column `rows`;
it agrees with `n1\summary_corrected.csv` on every row.)

| instrument-month | corrected rows | restricted strict | restricted equal | full-class strict | full-class equal |
|---|---|---|---|---|---|
| cl 2025-01 | 801,410 | 21,770 | 0 | 53,249 | 2,194 |
| cl 2025-08 | 664,076 | 9,048 | 0 | 27,852 | 1,427 |
| cl 2025-09 | 687,658 | 10,803 | 1 | 34,010 | 1,388 |
| cl 2025-10 | 745,569 | 15,002 | 3 | 42,377 | 1,893 |
| cl 2025-11 | 703,999 | 15,345 | 0 | 48,607 | 1,680 |
| cl 2025-12 | 768,531 | 10,837 | 2 | 38,945 | 1,985 |
| gc 2025-01 | 761,736 | 13,907 | 3 | 37,065 | 1,853 |
| gc 2025-08 | 692,041 | 16,051 | 0 | 42,886 | 1,907 |
| gc 2025-09 | 734,280 | 25,862 | 0 | 59,691 | 2,053 |
| gc 2025-10 | 772,447 | 37,913 | 0 | 71,584 | 2,588 |
| gc 2025-11 | 674,038 | 12,764 | 1 | 30,577 | 1,686 |
| gc 2025-12 | 772,202 | 20,195 | 0 | 49,649 | 1,793 |
| zc 2025-08 | 554,303 | 23,755 | 3 | 90,868 | 2,857 |
| zc 2025-09 | 580,944 | 30,617 | 1 | **111,334** | 2,640 |
| zc 2025-10 | 634,445 | **34,492** | 2 | 109,332 | 2,873 |
| zs 2025-08 | 465,381 | 17,717 | 2 | 64,404 | 2,161 |
| zs 2025-09 | 429,465 | 10,382 | 0 | 45,255 | 2,281 |
| zs 2025-10 | 508,910 | 16,397 | 0 | 60,559 | 2,353 |

The 18 are **cl all 6 months, gc all 6 months, zc 2025-08/-09/-10, zs 2025-08/-09/-10** — the
same list §13(b) publishes, unchanged.

**Which trade class carries the restricted map's non-zeros** (`y1\y1_trade_class_map_output.txt`
final block): corrected — `trades_all` 18 strict / 11 equal, `trades_sell` 18 / 11,
`trades_large` 18 / 1, **`trades_buy` 0 / 0**; contaminated — `trades_all` 48 / 23,
`trades_sell` 48 / 23, `trades_large` 48 / 8, **`trades_buy` 0 / 0**. `trades_buy` is identically
zero in all 96 of its cells on both sides, the dead-zero consequence of the aggressor-literal
mismatch (§C.4(a), §15). **The restricted surface is therefore carried by three live classes,
not four**, and a gate report may not describe it as a four-class surface without that note.

**THE DELTA, stated as a separate factual paragraph.** Restricting the scored surface to the
fixture's column universe leaves the **strict cell set UNCHANGED**: **18 of 48** corrected
instrument-months, **the same 18 cells**, and **48 of 48** contaminated. **The equal arithmetic
collapses**: corrected equal-non-zero **35 / 48 → 11 / 48** (equal-only 17 → 2), contaminated
equal-non-zero **42 / 48 → 23 / 48**. **The corrected peak falls** from **zc 2025-09, 111,334
strict (19.16% of 580,944 rows)** to **zc 2025-10, 34,492 strict (5.44% of 634,445 rows)** — a
different cell as well as a smaller number, and roughly a threefold fall in rate. Nothing else
moves: no cell changes sign, no unscored cell becomes scored, and the 72 unscored cells of
§13(g) are unaffected in either map.

**What the restricted map IS and IS NOT, so the two are never confused.** It is a **REPORTING
object**, published to satisfy R17(ii) and to make §13(j)'s quotation rules checkable. **It is
NOT a second scoring key, and it changes no adjudication.** The gate continues to score against
`n1\declared_map.csv` as frozen by §D.1 item 3, and no cell that adjudicates a fed-column
finding is dropped by the restriction — because **every one of the eleven REQUIRED columns is
already governed by a `trades_*` class** (§A.6.1's third table column: `trades_all` on nine,
`trades_sell` on `sell_volume_10s`, `trades_large` on `large_trade_count_10s`). The restricted
map adds no measurement, changes no cell value, and is regenerable from the frozen artifact by
`y1\y1_trade_class_map.py`; §D.1's freeze is therefore unaffected in either direction.

**R17(iii) — THE CHECK, RECORDED AS A FINDING.** The trade-class re-derivation **returns
NON-ZERO in the same 18 cells**. **That is the expected result, and it is recorded as a
substantive finding rather than as a formality**: the same-second mechanism is a property of the
**wall-clock JOIN KEY** — `ts_floor`, and the cohort predicate `floor(T_i) == floor(T_{i-1})`
(§13(d), §C.2) — **not of the event source**. Trades and MBO events are attached to a lattice
row by the identical `ts_floor` merge (§3; `phase5_ml.py` L222/L230 and L248, `phase7_l2_sim.py`
L206/L231), so a row whose absorbed window overhangs its own stamp overhangs it for **every**
event stream that has an event in that window. The MBO stream is denser and therefore populates
the overhang window more often and more sharply, which is why the magnitudes fall — but the
cells where an overhang exists at all are a property of the lattice, and they do not move.
**An all-zero return would have been a FINDING, not a pass:** it would have meant that the
corrected-side violations recorded in §13(b) were carried entirely by an event source no fixture
column consumes, and that no fixture column violates anywhere on the corrected side — which
would have put criterion 1's REQUIRED list, and the discrimination framing of the corrected
side, in question. The check was run for that possibility, and the possibility is excluded.

### (j) THE SIX `mbo_*` CLASSES AFTER Y1 — what they still evidence, and what they may never again be quoted as

**Standing, restated.** Y1 establishes that **0 of the 35 fixture columns is MBO-fed** (§13(i)'s
justification box). The six MBO classes — `mbo_all`, `mbo_bid_add`, `mbo_ask_add`,
`mbo_bid_cancel`, `mbo_ask_cancel`, `mbo_cancel_any` — therefore attach to **no fed column**.
They are not withdrawn, not deleted from the map, and not reclassified: they remain SCORED cells
of `n1\declared_map.csv` and every count in them stands as measured. What changes is what they
may be quoted **for**.

**They STILL legitimately evidence — and may be quoted for:**

1. **Lattice-irregularity characterization of the fixture's SOURCE stream.** The MBO event
   stream measured against the snapshot lattice is a real, measured property of the data the
   fixture is built from and of the wall-clock-second join geometry. §B.4's two counts — **18 of
   48 instrument-months MULTI-BLOCK, 41 of 48 carrying filtered excess rows** — and §3's root
   cause are statements about the *stream and the
   lattice*, and they stand.
2. **Boundary-instant characterization of that source stream** — how far past a claimed decision
   instant the wall-clock-second bucket reaches, measured on the densest available event stream.
   MBO is the densest, which is exactly why it yields the sharpest boundary measurement: worst
   overhang past `t-1` **999.999579 ms** on MBO classes against **999.996869 ms** on trades
   (§10, §14).
3. **Corroboration of the join-family MECHANISM.** The `ts_floor` geometry that produces the MBO
   overhang is the same geometry that produces the trades overhang. The MBO measurement is a
   higher-resolution view of ONE mechanism, not a second mechanism — which is also why §13(i)'s
   restricted map returns the same 18 cells.

**They must NEVER again be quoted as:**

1. **Evidence about any fed column, in either direction.** An `mbo_*` class being strict-positive
   in a cell says nothing about whether any of the 35 columns violates in that cell, and its
   being zero says nothing about any column being clean. They attach to no column at all.
2. **Any criterion-1 arithmetic** — no denominator, no REQUIRED finding, no `k of N` term.
   §A.6.1 already excludes them; Y1 confirms there is no route by which they could enter, and
   N = 11 is re-derived unchanged against the columns the fixture actually contains (§A.6.4).
3. **Any unqualified "X of 48" headline.** Where the sentence is about the fixture's FED
   columns, the class set is the four trade classes: **18/48 strict corrected (unchanged), but
   11/48 equal-non-zero and 2/48 equal-only — not 35 and 17** (§13(i)).
4. **Any unqualified "max strict" or "max equal" — and any peak stated without naming its
   METRIC.** The published corrected peak — zc 2025-09, 111,334, 19.16% — is an `mbo_all`
   figure. Restricted to the fed columns (trade classes), the peak differs by metric and both
   must be named: the **RATE peak is zc 2025-10 — 34,492 of 634,445 corrected rows, 5.44%**;
   the **ABSOLUTE peak is gc 2025-10 — 37,913 of 772,447 corrected rows, 4.91%**. Neither is
   "the" peak. §13(a)'s class-set rule already requires the class set to be named on every "max
   across classes"; after Y1 that rule is load-bearing, not housekeeping, and it is extended
   here: **a peak is quoted with its class set AND its metric, or it is not quoted.**
   (Derivation: `y1\trade_class_only_map.csv`, corrected rows, `max_strict_trade_only` over
   `rows`; top five by rate are zc 2025-10 5.44%, zc 2025-09 5.27%, gc 2025-10 4.91%,
   zc 2025-08 4.29%, zs 2025-08 3.81%.)

**CAUTION, recorded verbatim from Y1 §3.2 — the `BOUNCE_FREE_FEATURES` trap.** The reasoning
above depends on which 35-column set is meant, and the archive contains two sets of length 35
whose MBO content is opposite:

> **Consequence, stated explicitly:** the 35-set is **not** Phase 5's `BOUNCE_FREE_FEATURES`
> (L91 `BOUNCE_FREE_FEATURES = [f for f in FULL_FEATURES if f not in PRICE_LAG_FEATURES]`, which
> is also 35 long but **keeps all 10 MBO columns** and drops the 10 price-lag ones instead).
> Any reasoning that treats "the 35-set" as the bounce-free set would reach the opposite MBO
> conclusion. The sets are disjoint in exactly the way that matters here.

**Consequence for this file and for any gate report:** "the 35-column set" always means
`ALL_L2_FEATURES` (`phase7_l2_sim.py` lines 73-108), never `BOUNCE_FREE_FEATURES`. Any future
re-derivation must name the constant, not the length. The `feature_set` values `Full` / `BFree`
that the 45-set result families carry (§0.4 item 2) are exactly where a reader would otherwise
pick up the wrong 35.

SOURCE: AVAILABILITY_DECLARATION.md lines 2932-3207

## 14. Contaminated-side violation profile (element g; T1 headline)

> **MEASURED ON ARTIFACT A** (§0.1) — the ZC 2025-01 lineage lattice and its event parquets.

> **BOTH VERSIONS, PUBLISHED SIDE BY SIDE — THE FED-COLUMN RESTRICTION APPLIED SYMMETRICALLY
> (delta-issued item S1).** §13(i) applies the fixture-universe restriction to the CORRECTED side
> and publishes both maps. **Y1's premise is side-independent** — no fixture column consumes the
> MBO event source, on either side — so the same restriction governs THIS section, whose
> published headline (75.21%, the `total_events` family) has until now been an `mbo_*` figure.
> Both versions appear below: **PROFILE 1, the full-class profile AS MEASURED**, which is
> unchanged, stands as measured, and remains the measurement; and **PROFILE 2, the
> fed-column-restricted profile** over the four `trades_*` classes, which is what any statement
> about the fixture's 35 columns may quote. **Neither replaces the other**, and PROFILE 2 adds no
> measurement and changes no count — it is a re-read of the same artifact rows over a narrower
> class set.
>
> **The justification for the restriction is §13(i)'s R17(i) box and is NOT re-argued here.**
> That box establishes the criterion on the column universe alone — `phase7_l2_sim.py` opens two
> data files and no MBO file; `ALL_L2_FEATURES` contains none of the ten MBO-derived Phase 5
> columns; all 35 columns trace to snapshot 13 / trades 11 / snapshot-derived 9 / clock 1 / MIXED
> 1, **MBO-fed 0 of 35** (`y1\column_universe.csv`). **Per R17(i), the criterion makes no
> reference to what the restriction does to any count, and none may be added to it.** The counts
> below are a separate factual matter and are not part of the reason.

**Scope: ZC 2025-01 only** — lattice **338,159 rows** = `processed\zc\zc_snapshots_2025-01.parquet`
under UTC hours [14,19), generation **v3_pre_gapfill**, sha256
`46aa7639f3eb92ad7cfafecb78983340e83409f104b1fbf06d4c479078729b46` (md5
`ea2eee6136896b5f8a5b7ddc052f589c`) — §2's naming rule; this is NOT the v4_gapfill generation,
which is 378,000 rows under the same filter. The other 47 instrument-months are in §13's map.

**PROFILE 1 — THE FULL-CLASS PROFILE, AS MEASURED (all 10 declared classes). UNCHANGED BY S1;
this is the measurement, and every count in it stands.** On the contaminated (pre-fix) side,
measured against decision time `T` over 338,159 rows:

- **Strictly-post-decision absorption on 26.49% of rows** for the trades-all classes
  (89,568/338,159) — all trade-derived columns except the dead-zero buy_volume family
  (net_delta and its 1/5/10/30/60 s rollups, trade_count, trade_volume, sell_volume,
  sell_volume_10s, trade_count_10s, vwap, vwap_distance).
- Large-trade class: 6.99% (23,633/338,159).
- MBO classes: 38.2-75.2% — ask_cancels 38.25%, bid_cancels 40.21%, ask_adds 48.13%,
  bid_adds 48.78%, cancel_any 53.19%, and the total_events family 75.21%
  (254,315/338,159).
- Worst overhang past `T`: 999.999579 ms (MBO ask_cancel / total_events family). Mean
  overhang among violating rows: **per-class means 506.3-655.2 ms; trades_all 519.8,
  mbo_all 655.2** (`v1\mean_overhang_by_class.csv`, column `mean_overhang_ms`: trades_large
  506.273305 is the minimum, mbo_all 655.194723 the maximum, trades_all 519.797439; medians in
  the same file run 513.5-727.9 ms).
- **Stamp-type concentration — MEASURED, not inferred (M4).** 95.04% of in-hours row stamps are
  integral-second (321,384 of 338,159 rows with `T == floor(T)`; 16,775 mid-second). The
  violations do not merely "concentrate" there — **at least 99.98% of all violations sit on
  integral stamps, on every class that has any**: `share_of_viol_on_integral` runs from
  0.999807 (mbo_all, the minimum) to 1.0 (trades_large), i.e. **≥99.98%** (trades_buy is
  excluded from the range because it has zero violations — §C.4(a)). Per-row rates by stamp
  type: **trades_all 27.87% on integral stamps vs 0.012% on mid-second stamps** (89,566/321,384
  vs 2/16,775; rate ratio 2337.5x) and **mbo_all 79.12% vs 0.29%** (254,266/321,384 vs
  49/16,775; rate ratio 270.9x). The mechanism is exactly the one §3 predicts: the joined
  wall-clock second extends furthest past `T` precisely when `T` sits on the second boundary, so
  a mid-second stamp has almost no window left to overhang. The bucketed view bears that out —
  16,201 of the 16,775 mid-second rows have ≤1 ms of second remaining, and both of trades_all's
  mid-second violations plus 26 of mbo_all's 49 fall in that `(0,1] ms` bucket (the other 23 in
  `(500,750]` and `(750,999]`). M4's counts reproduce T1's totals exactly
  (`strict_total_matches_t1` and `equal_total_matches_t1` both True on all 10 classes) under two
  independent estimators with `row_disagreements=0`. Evidence:
  `m4\stamp_type_breakdown.csv`; `m4\viol_rate_by_remaining_time.csv`.

Evidence: `t1\violation_table.csv` (contaminated `decision_T` rows, `frac` and
`worst_overhang_ms` columns); `t1\t1_final_output.txt` lines 2-13 (lattice profile incl.
the 321,384 / 16,775 stamp split) and lines 22-52 (per-class summary).

**PROFILE 2 — THE FED-COLUMN-RESTRICTED PROFILE (the four `trades_*` classes). This is the only
version a statement about the fixture's 35 columns may quote.** Same cell, same artifacts, same
338,159 rows; **no new measurement and no changed count** — a re-read of the identical rows over
the class set that corresponds to the fixture's column universe.

| Quantity | PROFILE 1 — full-class AS MEASURED (10 classes) | PROFILE 2 — fed-column-restricted (4 `trades_*` classes) | delta |
|---|---|---|---|
| headline strict rate (max over the class set) | **75.21% — 254,315 / 338,159**, class `mbo_all` | **26.49% — 89,568 / 338,159**, classes `trades_all` ≡ `trades_sell` | **−48.72 pp**; 164,747 fewer rows; the restricted figure is **35.2%** of the published one |
| per-class strict-rate span, live classes | **6.99% – 75.21%**, 9 live classes | **6.99% – 26.49%**, 3 live classes | ceiling falls; **floor unmoved** — `trades_large` is the minimum in both |
| classes carrying any strict violation | 9 of 10 (`trades_buy` dead-zero, §C.4(a)) | 3 of 4 (the same dead zero) | — |
| worst overhang past `T` | **999.999579 ms**, classes `mbo_ask_cancel` / `mbo_all` / `mbo_cancel_any` | **999.996869 ms**, classes `trades_all` / `trades_sell` (`trades_large` 999.954529 ms) | **−2.71 µs** — the mechanism's ceiling is the same 1 s bucket under both |
| mean overhang among violating rows | **506.3 – 655.2 ms** (min `trades_large`, max `mbo_all`) | **506.3 – 519.8 ms** (min `trades_large`, max `trades_all`) | upper end falls **135.4 ms**; lower end unmoved |
| median overhang | **513.5 – 727.9 ms** | **513.5 – 536.4 ms** | upper end falls **191.5 ms** |
| share of violations on integral stamps | **≥ 99.98%** (minimum 0.999807, `mbo_all`) | **≥ 99.9978%** (minimum 0.999978, `trades_all`/`trades_sell`; `trades_large` exactly 1.0) | the concentration is **sharper** under the restriction, not weaker |
| integral vs mid-second per-row rate | `mbo_all` **79.12% vs 0.29%**, ratio 270.9x | `trades_all` **27.87% vs 0.012%**, ratio **2337.5x** | the rate RATIO is **8.6x larger** on the fed classes |
| strict / equal at the cell | 254,315 strict + 29 equal (`mbo_all`) | **89,568 strict + 20 equal** (`trades_all` ≡ `trades_sell`) | equal falls 29 → 20 |

**Provenance of every PROFILE 2 figure, row by row.** `t1\violation_table.csv`,
contaminated/`decision_T`: `trades_all` lines 2 / 11 / 14 / 23 / 26 / 29 / 32 / 35 / 44 / 50 (89568, 20,
`frac` 0.264869, `worst_overhang_ms` 999.996869), `trades_sell` lines 8 / 41 (identical),
`trades_large` lines 17 / 47 (23633, 20, 0.069887, 999.954529), `trades_buy` lines 5 / 38
(0, 0, 0.0 — dead-zero), `mbo_all` lines 65 / 95 / 98 (254315, 29, 0.752057, 999.999579),
`mbo_ask_cancel` lines 62 / 86 / 89 (129334, 22, 999.999579).
`v1\mean_overhang_by_class.csv` for the mean/median/worst triples (`trades_all`
519.797439 / 536.435824 / 999.996869; `trades_large` 506.273305 / 513.500435 / 999.954529;
`mbo_all` 655.194723 / 727.947559 / 999.999579). `m4\stamp_type_breakdown.csv` for the stamp
split (`trades_all` `viol_rate_integral` 0.278688, `viol_rate_mid_second` 0.000119,
`rate_ratio_integral_over_mid` 2337.499, `share_of_viol_on_integral` 0.999978; `trades_large`
`share_of_viol_on_integral` 1.0; `mbo_all` 0.791159 / 0.002921 / 270.851 / 0.999807).

**CROSS-CHECK, performed this pass and reported with its result.** The restricted figures were
derived from `y1\trade_class_only_map.csv` (contaminated/zc/2025-01: `max_strict_trade_only`
**89,568**, `max_equal_trade_only` **20**, `max_strict_declared10` **254,315**, `rows`
**338,159**) and independently re-derived from `n1\declared_map.csv` by taking the maximum
`strict_count` over that cell's SCORED `decision_T` rows within each class set: **max over the
four `trades_*` = 89,568; max over the six `mbo_*` = 254,315; max over all ten = 254,315** —
**exact agreement on all three**. The same re-derivation was run over **all 96 rows** of
`y1\trade_class_only_map.csv` against the **984-row** declared map, on `max_strict_trade_only`,
`max_equal_trade_only` and `max_strict_declared10` together: **0 mismatches**. The declared map's
per-class rows for this cell also reproduce PROFILE 1 exactly — `mbo_ask_cancel` 129,334 =
38.25%, `mbo_bid_cancel` 135,981 = 40.21%, `mbo_ask_add` 162,754 = 48.13%, `mbo_bid_add`
164,959 = 48.78%, `mbo_cancel_any` 179,857 = 53.19%, `mbo_all` 254,315 = 75.21%, `trades_all`
and `trades_sell` 89,568 = 26.49%, `trades_large` 23,633 = 6.99%, `trades_buy` 0 — so the two
profiles are two readings of one artifact and not two measurements.

**THE DELTA, STATED PLAINLY — AS THE POINT, NOT AS A CONCESSION.** **The fed-column-restricted
headline for this cell is MATERIALLY SMALLER than the headline this section published: 26.49%
where the published headline said 75.21%** — **89,568 rows where it said 254,315**, a fall of
**48.72 percentage points** and of **164,747 rows**, leaving **35.2%** of the published
magnitude, a factor of **2.84**. **A smaller honest number has replaced a larger one, and
recording that replacement IS the deliverable.** The 75.21% was never wrong as a *measurement* —
it is `mbo_all` at ZC 2025-01, it stands exactly as measured, and §13(j)'s "what they still
evidence" list continues to apply to it — but it was carried as **this section's headline** for a
fixture **none of whose 35 columns consumes the MBO event source**, so *as a statement about the
fixture* it overstated the contaminated side by 2.84x. Two further facts are stated here rather
than left to be discovered: **ZC 2025-01 is the cell where the restriction bites HARDEST of all
48** — its 48.72 pp delta is the largest in the map (§14.1) — so the section that headlines this
cell is exactly the section that most needed the correction; and the cell's **rank moves**, from
15th of 48 by full-class rate to 20th of 48 by restricted rate, i.e. it is nearer the middle of
the contaminated distribution than the full-class figure made it look. **Nothing about the
fixture's discrimination claim depends on the larger number:** the contaminated side is
strict-positive in **48 of 48** instrument-months under BOTH class sets (§13(i)), and the two
sides remain separated by one to three orders of magnitude in the restricted map exactly as in
the full one.

**FORBIDDEN USE — §13(j)'s rules, applied to THIS side verbatim.** §13(j) states them for the
corrected side. Y1's premise is side-independent, so they bind here identically, and they are
restated in this section's own terms so that a reader of §14 alone cannot miss them. The six
`mbo_*` classes remain SCORED cells of `n1\declared_map.csv`; every count in PROFILE 1 stands as
measured; **what changes is only what they may be quoted FOR.**

1. **PROFILE 1's MBO bullet is not evidence about any fed column, in either direction.**
   `mbo_all` at 75.21% says nothing about whether any of the 35 columns violates in this cell,
   and had it been zero it would have said nothing about any column being clean. **It attaches
   to no column at all.**
2. **No criterion-1 arithmetic may be built on it** — no denominator, no REQUIRED finding, no
   `k of N` term. **N = 11 and is unchanged** (§A.6.1, §A.6.4, §A.6.5); Y1 confirms there is no
   route by which an `mbo_*` figure could enter it.
3. **No unqualified "X of 48" headline.** Where the sentence is about the fixture's FED columns
   the class set is the four `trades_*` classes. On the contaminated side the **strict** cell
   count does not move — **48 / 48 under both class sets** — but the **equal** arithmetic does:
   **equal-non-zero 42 / 48 → 23 / 48** (§13(i)). Quoting 42 as a fed-column fact is precisely
   the error this rule stops.
4. **No unqualified "max strict" or "max equal", and NO peak quoted without BOTH its class set
   AND its metric.** Restated for the contaminated side (`y1\trade_class_only_map.csv`,
   contaminated rows, `max_strict_trade_only` / `max_strict_declared10` over `rows`):
   - **full-class RATE peak — es 2025-12, 613,447 / 620,108 = 98.93%, class `mbo_all`;**
   - **full-class ABSOLUTE peak — gc 2025-10, 646,575 of 772,448 rows = 83.70%, class
     `mbo_all`;**
   - **restricted RATE *and* ABSOLUTE peak — nq 2025-01, 543,341 / 598,228 = 90.83%, classes
     `trades_all` ≡ `trades_sell`.** **nq is TRADES-CLASSES-ONLY** — 4 of 10 classes scored, its
     six MBO classes UNSCORED and **not zero**, because there is no MBO file at the fixture path
     `processed\nq\` (§13(g), §13(h)). **The label is required on every appearance of nq in a
     table, including this one.** Its restricted and full-class figures are identical *because
     it has no MBO classes to drop* — not because the restriction spared it, and not because it
     is cleaner or dirtier than any other cell;
   - **restricted peaks EXCLUDING nq**, stated because the unqualified restricted peak is an
     nq cell for the coverage reason just given: **RATE — es 2025-11, 484,420 / 549,424 =
     88.17%**; **ABSOLUTE — es 2025-01, 514,323 of 605,290 rows = 84.97%**; both classes
     `trades_all` ≡ `trades_sell`.

   **None of those six figures is "the" peak, and none may be quoted without its class set and
   its metric.**

   **BINDING — the EX-NQ figures are the summary-level peaks.** nq's restricted peak (90.83%,
   nq 2025-01) is a **COVERAGE ARTIFACT**: nq's restricted and full-class figures coincide only
   because nq has **no MBO classes to drop**, not because the restriction spared it. **A
   summary-level statement of the restricted contaminated peak — in this file, in §14.1, or in
   any gate report — therefore quotes the EX-NQ peak: RATE es 2025-11, 484,420 / 549,424 =
   88.17%; ABSOLUTE es 2025-01, 514,323 of 605,290 rows = 84.97%; both classes `trades_all` ≡
   `trades_sell`.** The nq figure may be published only as a per-cell entry carrying its
   TRADES-CLASSES-ONLY label and its coverage-artifact reason, never as the restricted
   contaminated headline. Quoting 90.83% as the peak is the same error §13(j) item 4 stops on
   the corrected side. *(This clause resolves the tension a verifier found between the
   preceding sentence and the summary in §14.1: the "none is the peak" rule governs PER-CELL
   quotation, where every figure must carry its class set and metric; this clause governs
   SUMMARY-LEVEL quotation, where a single peak must be named and the coverage artifact must
   not be it.)*
5. **`trades_buy` is 0 strict and 0 equal in all 48 contaminated cells** (§C.4(a), §15), so the
   restricted contaminated surface is carried by **three live classes, not four** — the same note
   §13(i) attaches to the corrected side. A gate report may not describe the restricted
   contaminated surface as a four-class surface without it.

### 14.1 — The same restriction across all 48 contaminated cells (a declared scope step-out)

> **SCOPE NOTE, so §14's ZC 2025-01 banner is not silently contradicted.** §14 above is ZC
> 2025-01 only and stays so. This subsection **deliberately steps outside that cell**, for one
> purpose: to place ZC 2025-01 in the 48-cell distribution, so that a single-cell headline is
> never read as representative of the contaminated side. It is the contaminated-side analogue of
> §13(i)'s 18-cell corrected table. **It introduces no new measurement** — every figure is
> `y1\trade_class_only_map.csv`, contaminated rows, itself re-derived from `n1\declared_map.csv`
> and re-verified against it this pass with **0 mismatches over all 96 rows**.

`restricted` = max strict over the four `trades_*` classes (`max_strict_trade_only`);
`full-class` = max strict over the declared classes SCORED in that cell
(`max_strict_declared10`); rate = strict / `rows`. **nq is TRADES-CLASSES-ONLY in all six of its
months** — 4 of 10 classes scored, its six MBO classes UNSCORED and not zero (§13(g), §13(h)) —
which is why its two columns are equal and its delta is 0.00 pp. **That is a coverage fact about
nq's map cells, not a finding about nq**, and it is the reason nq must never be read as the
cell where "the restriction changed nothing".

| instrument-month | rows | restricted strict | restricted % | full-class strict | full-class % | delta pp |
|---|---|---|---|---|---|---|
| cl 2025-01 | 801,411 | 232,865 | 29.06 | 534,779 | 66.73 | 37.67 |
| cl 2025-08 | 664,077 | 142,974 | 21.53 | 406,797 | 61.26 | 39.73 |
| cl 2025-09 | 687,659 | 132,950 | 19.33 | 414,893 | 60.33 | 41.00 |
| cl 2025-10 | 745,570 | 190,595 | 25.56 | 493,760 | 66.23 | 40.66 |
| cl 2025-11 | 704,000 | 158,683 | 22.54 | 497,360 | 70.65 | 48.11 |
| cl 2025-12 | 768,532 | 126,520 | 16.46 | 454,867 | 59.19 | 42.72 |
| es 2025-01 | 605,290 | 514,323 | 84.97 | 585,940 | 96.80 | 11.83 |
| es 2025-08 | 546,610 | 424,624 | 77.68 | 524,929 | 96.03 | 18.35 |
| es 2025-09 | 553,280 | 420,017 | 75.91 | 532,496 | 96.24 | 20.33 |
| es 2025-10 | 599,190 | 490,161 | 81.80 | 576,377 | 96.19 | 14.39 |
| es 2025-11 | 549,424 | 484,420 | 88.17 | 542,495 | 98.74 | 10.57 |
| es 2025-12 | 620,108 | 499,061 | 80.48 | 613,447 | 98.93 | 18.45 |
| gc 2025-01 | 761,737 | 210,374 | 27.62 | 523,228 | 68.69 | 41.07 |
| gc 2025-08 | 692,042 | 204,014 | 29.48 | 461,530 | 66.69 | 37.21 |
| gc 2025-09 | 734,281 | 252,461 | 34.38 | 515,322 | 70.18 | 35.80 |
| gc 2025-10 | 772,448 | 371,565 | 48.10 | 646,575 | 83.70 | 35.60 |
| gc 2025-11 | 674,039 | 213,333 | 31.65 | 470,500 | 69.80 | 38.15 |
| gc 2025-12 | 772,203 | 264,176 | 34.21 | 604,763 | 78.32 | 44.11 |
| he 2025-01 | 337,489 | 39,596 | 11.73 | 132,122 | 39.15 | 27.42 |
| he 2025-08 | 308,711 | 29,188 | 9.45 | 100,848 | 32.67 | 23.21 |
| he 2025-09 | 308,702 | 27,044 | 8.76 | 88,859 | 28.78 | 20.02 |
| he 2025-10 | 338,111 | 30,132 | 8.91 | 106,120 | 31.39 | 22.47 |
| he 2025-11 | 304,487 | 35,084 | 11.52 | 108,223 | 35.54 | 24.02 |
| he 2025-12 | 353,683 | 36,867 | 10.42 | 127,766 | 36.12 | 25.70 |
| le 2025-01 | 337,494 | 44,691 | 13.24 | 140,720 | 41.70 | 28.45 |
| le 2025-08 | 308,711 | 43,707 | 14.16 | 119,867 | 38.83 | 24.67 |
| le 2025-09 | 308,710 | 42,140 | 13.65 | 126,122 | 40.85 | 27.20 |
| le 2025-10 | 338,113 | 47,045 | 13.91 | 125,589 | 37.14 | 23.23 |
| le 2025-11 | 304,492 | 26,854 | 8.82 | 77,483 | 25.45 | 16.63 |
| le 2025-12 | 353,690 | 31,871 | 9.01 | 90,032 | 25.46 | 16.44 |
| **nq 2025-01** *(TRADES-CLASSES-ONLY)* | 598,228 | 543,341 | 90.83 | 543,341 | 90.83 | 0.00 |
| **nq 2025-08** *(TRADES-CLASSES-ONLY)* | 540,531 | 470,095 | 86.97 | 470,095 | 86.97 | 0.00 |
| **nq 2025-09** *(TRADES-CLASSES-ONLY)* | 549,431 | 455,826 | 82.96 | 455,826 | 82.96 | 0.00 |
| **nq 2025-10** *(TRADES-CLASSES-ONLY)* | 590,786 | 524,165 | 88.72 | 524,165 | 88.72 | 0.00 |
| **nq 2025-11** *(TRADES-CLASSES-ONLY)* | 550,464 | 494,380 | 89.81 | 494,380 | 89.81 | 0.00 |
| **nq 2025-12** *(TRADES-CLASSES-ONLY)* | 620,108 | 525,629 | 84.76 | 525,629 | 84.76 | 0.00 |
| **zc 2025-01** *(the §14 cell)* | 338,159 | **89,568** | **26.49** | **254,315** | **75.21** | **48.72** |
| zc 2025-08 | 554,304 | 92,136 | 16.62 | 314,170 | 56.68 | 40.06 |
| zc 2025-09 | 580,945 | 109,981 | 18.93 | 344,076 | 59.23 | 40.30 |
| zc 2025-10 | 634,446 | 117,267 | 18.48 | 342,560 | 53.99 | 35.51 |
| zc 2025-11 | 304,506 | 57,662 | 18.94 | 163,822 | 53.80 | 34.86 |
| zc 2025-12 | 353,104 | 76,969 | 21.80 | 222,940 | 63.14 | 41.34 |
| zs 2025-01 | 337,845 | 78,300 | 23.18 | 210,254 | 62.23 | 39.06 |
| zs 2025-08 | 465,382 | 88,011 | 18.91 | 296,502 | 63.71 | 44.80 |
| zs 2025-09 | 429,466 | 72,942 | 16.98 | 268,482 | 62.52 | 45.53 |
| zs 2025-10 | 508,911 | 91,965 | 18.07 | 296,861 | 58.33 | 40.26 |
| zs 2025-11 | 304,506 | 62,578 | 20.55 | 185,931 | 61.06 | 40.51 |
| zs 2025-12 | 353,104 | 60,796 | 17.22 | 222,557 | 63.03 | 45.81 |

**What the 48 rows say, stated as arithmetic and with every quantity's class set named.**
Strict-positive cells: **48 / 48 restricted, 48 / 48 full-class** — the restriction moves no cell
off zero and none onto it, the contaminated-side analogue of §13(i)'s "same 18 cells" on the
corrected side. Equal-non-zero: **23 / 48 restricted vs 42 / 48 full-class**. Restricted strict
RATE spans **8.76%** (he 2025-09) to a summary-level peak of **88.17%** (es 2025-11, 484,420 /
549,424 — the EX-NQ peak, which §14 item 4's BINDING clause requires here; the unqualified
maximum is **90.83%**, nq 2025-01, TRADES-CLASSES-ONLY, a coverage artifact and not the
headline), median **21.66%**. The summary-level restricted **ABSOLUTE** peak is **es 2025-01,
514,323 of 605,290 rows = 84.97%**, classes `trades_all` ≡ `trades_sell`. Full-class strict rate spans **25.45%**
(le 2025-11) to **98.93%** (es 2025-12, class `mbo_all`), median **63.08%** — the same
0.2545-0.9893 range §13(c) publishes, unchanged. The per-cell delta runs **0.00 pp** (all six nq
cells, for the coverage reason above) to **48.72 pp** (**zc 2025-01 — the largest of all 48**);
excluding nq it runs **10.57 pp** (es 2025-11) to that same 48.72 pp. **The restriction lowers
every non-nq contaminated headline and raises none**, which is the honest summary of what
applying Y1 symmetrically does to this side.

SOURCE: AVAILABILITY_DECLARATION.md lines 3280-3314

## 16. Documented-unverifiable assumptions (element i)

> **NEITHER ARTIFACT — this section is about the ARCHIVE's silence** (§0.3's admissible third
> case). Items 1 and 2 are unverifiable facts about **Artifact B**'s generators and runtime;
> item 3 is an unverifiable fact about the source copies **Artifact A**'s lineage physically
> read. Nothing here is a measurement on either artifact.

Assumptions the declaration RELIES ON that no archive record can verify; recorded as such:

1. **The 35-column set for the main-PC pair (R3).** The stored main-set predictions carry
   no feature manifest; the assumption that they were produced from `ALL_L2_FEATURES` (the
   35 columns of `phase7_l2_sim.py` lines 73-108) is accepted as a documented-unverifiable
   assumption. Basis: the F3 manifest cross-check — 9/9 agreement of the Phase-7-added
   columns' DAG classes against `f3\fixture_manifest_DRAFT.json` (Part I, DAG cross-check
   block inside the Phase-7-added-columns section) — and the `working_resolution_R3` line
   carried in `t4\fixture_manifest_35col_DRAFT.json`. The 9/9 agreement is on **CLASS**; the
   one FLAVOR that cross-check left open, `weighted_mid`, is settled by **R6** as
   `contemporaneous_state_flow` (PROVISIONAL until the tag; see the supersession note after the
   T2 addendum block). Flavor does not enter the class agreement and the basis is unchanged.
2. **phase7_l2_sim.py runtime inputs.** The script hardcodes the PC2 path
   (`PROJECT = Path(r"C:\Users\Research\Desktop\pc2_transfer")`, lines 32-33) and reads
   `processed\` only; what bytes that machine's copies held at run time is unconfirmable
   from the archive. **Citation corrected (item P2):** the hardcoded-path fact is
   `c2\aggregation_comparison.md` **construct row 20** ("Data source", which records
   `phase5_ml.py` L38-40 / L104-106 against `phase7_l2_sim.py` L32-33 and the verdict
   "DIFFERENT — Phase 7 hardcodes a `C:\Users\Research\...` pc2 path, reads processed/ only").
   **That file carries no blockers list**; the blockers are in `R2_consolidated_report.md`'s C2
   section, "Blockers (carried)" bullet — "actual aggressor values verified for ZC 2025-01 only;
   original-env wrap → C5; PC2 runtime reads unconfirmable from archive". The prior draft cited
   a blockers list to `c2\aggregation_comparison.md`; that cite was wrong and is replaced by
   these two.
3. **The physical `C:\MBO_data` source copies are unhashable (C1 residue).** The local
   copies the original runs physically read are gone and cannot themselves be hashed; the
   checksum chain of section 15 covers the pc2_transfer copies, not the physically read
   ones. Evidence: `R2_consolidated_report.md` C1 residual-ambiguity paragraph.

SOURCE: AVAILABILITY_DECLARATION.md lines 3649-3684

## Decision log — working resolutions (DELTA R2, 2026-08-10; PROVISIONAL until the prereg-v30a tag is signed)

Recorded here per DELTA R2 instruction; NOT in any locked file. Verbatim from the delta:

- **R1. ties:** registered default `available` stands. The declaration reports contaminated-side counts under both branches (strict counts plus the 49 exactly-equal events).
- **R2. boundary:** the declaration states the measured boundary floor(t−1)+1s as the true information boundary of the corrected features. The t−1 wording is retired as a claim and kept only as the historical contract text that was violated.
- **R3. 35-column:** accepted as a documented-unverifiable assumption (basis: F3 manifest 9/9 agreement). T4 is unblocked by this.
- **R4. as-built defects (buy classifier, uint32 wrap):** recorded as documented as-built behavior. f2-backed claims split into timing-structural (supported — event-to-row timing, overhang counts, the corrected-side zero) vs value-dependent (qualified).
- **R5. weighted_mid:** still AMBIGUOUS-PENDING-AUTHOR. Leave the T2 addendum block untouched.

### Working resolutions — DELTA R5 (2026-08-11; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R6 supersedes R5's pending status for the weighted_mid FLAVOR (the T2 addendum block itself remains untouched as the measurement record):

- **R6. weighted_mid flavor:** contemporaneous_state_flow. Basis: the information-content test — mid is (bid1+ask1)/2, computed from the same cells lines 184–186 already read, so the (X−mid)/tick form adds no information; substance matches book_slope, not vwap_distance. Record the counter-reading (form-match with line 187) as considered and rejected.
- **R7. hash-count:** the v30a tag message carries ALL FIVE hashes, matching the prereg-v30 tag as executed. Governing clause: "an amendment weaker than the thing it amends is not one." Record as a class A mechanical fact that §0.2.1's "both" is a stale count predating HISTORY.md and the tooling files joining the block. No locked-file edit.
- **R8. H-entry:** standard main-series form — `### H-34 — from PREREG.md §0.2.1` — with the entry text noting it is a class C amendment, the first post-tag entry. Addendum form rejected: H-nn is an open ledger and an amendment is a first-class event in it.

### Working resolution — DELTA R7 (2026-08-11; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R9 responds to the M5 falsification sweep (the corrected-side zero does not extend beyond ZC 2025-01); that sweep and its stop-and-report are preserved as evidence per K3:

- **R9.** The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on both fixture sides, not against an assumed-clean corrected side. §6.2 criterion 3 is amended within this class C registration: old — no findings on any corrected column; new — detector findings must match the declared per-side, per-class, per-instrument-month violation map; findings the map predicts are required, findings it excludes are false positives, cells the map does not cover are unscored. The corrected side is described throughout as CHARACTERIZED, never clean. Rationale recorded: the tool's own coverage principle (silence and belief never convert into a pass) applied to its own exam.

### Working resolutions — DELTA R9 (2026-08-12; same provisional status, binding only when the v30a tag is signed)

Verbatim from the delta. R11 resolves the criterion-1 denominator contradiction found by the P2 verifier; R12 corrects the NQ coverage claim; R13 governs the weighted_mid manifest disagreement:

- **R11.** Criterion-1 denominator derives from the DECLARED MAP, not from the manifest's construction classes. The manifest's leak-source classification is provenance context with no gate arithmetic attached. Three-way, mutually exclusive, enumerated BY NAME from the map artifact (never as a residue or a count):
  - **REQUIRED** — columns the map declares violating on the scored side under the declared branch (the forward-join / ts_floor overhang family). A correct detector must fire on each.
  - **OUT OF JURISDICTION** — columns declared availability-legal at boundary under R1 (the same-row book reads of §C.3). An availability-class finding on them is a false positive; a label-base finding on them belongs to L2a and is neither credited nor penalized by this gate. §C.3's "routes to criterion 2" is deleted — it had no landing site (PREREG line 460 scopes criterion 2 to manifest-clean columns).
  - **UNSCORED** — degenerate constants (buy_volume_10s), unconstructibles, and map-uncovered cells.

  N = the REQUIRED count, stated as the enumerated list plus its length, with the §D.1 freeze re-derived accordingly.
- **R12.** NQ MBO: NOT gate-scored, with the reason restated correctly — "no same-generation MBO data: the available NQ MBO is v4_gapfill; the fixture lattice is v3_pre_gapfill" — never "no data exists." NQ's coverage is restated as trade-classes-only; its "clean on both branches" advertisement is withdrawn as a pass claim. The cross-generation measurement runs as a declared NON-GATED DIAGNOSTIC (X4) so the information exists; moving it into the acceptance denominator later is class C.
- **R13.** weighted_mid: the f3 manifest is NOT edited. Evidence artifacts are never adjusted toward a decision. The declaration records the disagreement explicitly — manifest records label_base_price as of its date; R6 provisionally resolves contemporaneous_state_flow; the declaration's operative value is R6's, and the manifest field is superseded for this column only. §A.2's split is stated both ways: 7/18 per manifest, 6/19 under R6.
