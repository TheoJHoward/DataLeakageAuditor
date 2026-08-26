# DEVIATIONS_DRAFT — entry D-001

**ITEM PART D. DRAFT ONLY. NOT APPLIED.** `DEVIATIONS.md` in the repository is **0 bytes**
(verified this pass: `stat -c '%s' DEVIATIONS.md` → 0; sha256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the empty-string digest) and
is append-only under `PREREG.md` §11 item 6. Nothing below has been written to it.

**Regenerated 2026-08-13 against the CURRENT state**, after the §A.6.0 recovery and under DELTA
R15's C1–C5. The previous revision of this file is superseded in full, not patched. **Its
substantive correction to the F5 skeleton is carried forward and re-verified** (§4); its
measurement paragraphs are re-verified line-by-line against the working-tree declaration and are
extended to the complete landed set.

**Carries no new semantics, by construction.** `PREREG.md` §0.2.1: "The deviation records what
was measured; the amended tag carries the new semantics. Both." Every rule statement below is
**quoted** from `PREREG.md` or from the declaration, never authored here. No new branch, unit,
denominator, coverage state, tier licence, or acceptance criterion appears in this entry.

**The entry describes the COMPLETE landed set.** There is no "not in this ceremony" clause
anywhere below, and none may be added: everything `prereg-v30a` lands is measured in the same
entry that records why it landed.

---

## 1. THE ENTRY — append verbatim to `DEVIATIONS.md`

The file is empty, so this becomes its whole content. The leading `---` is kept as the entry
separator so that D-002 can be appended below the same way.

```markdown
---

## D-001 — Fixture re-basis and §6.2 conformance walk (class C amendment, `prereg-v30a`)

**Date recorded:** «CEREMONY-FILL: date»
**Class:** C per PREREG.md section 0.2.1 ("The measurement reveals a needed *new*
branch, unit, denominator, coverage state, tier licence, or acceptance criterion").
**Disposition:** amended registration, tag `prereg-v30a`, per section 0.2.1:
"Class C requires an amended registration, committed and externally timestamped
before the affected detector is implemented or evaluated — a `prereg-v30a` tag,
not a restart, and not a `DEVIATIONS.md` entry standing alone. The deviation
records what was measured; the amended tag carries the new semantics. Both."
**Amendment commit:** «CEREMONY-FILL: commit hash» — tag `prereg-v30a`.
**Amended sections:** PREREG.md section 6.2, four elements — line 445 (reference
AUC 0.957 / 0.675, interval ±0.010), line 450 (contamination availability class,
recording locus), line 451 (sliced variant for CI), line 461 (criterion 3) — plus
section 10.2, which receives a definition of "waived" for its replacement-criterion
floor. No other registered section is amended. Any section 0.1 lock-table row whose
key phrase the reviewed diff moves is amended with it and is named in the commit.

### What was measured (facts only; no rule text here)

1. **Pair chronology.** The archive's Phase 5 feature builder
   `build_features_month()` (`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py`
   lines 174-298) contains no `shift(1)`; the universal one-second feature lag
   exists only in
   `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py`
   line 276 (`snap[feature_cols] = snap[feature_cols].shift(1)`, file mtime
   2026-04-12; line 819 writes `lag_fix: universal (all features shift(1))`).
   The post-fix `phase5_ml.py` variant described in `universal_lag_finding.txt`
   (lines 296-317, `_NO_LAG`/`_lag_cols` block) is MISSING from the archive.
   Confirmed by spike items F1-F4 and by delta-R2 items C1-C4 and T4. The
   controlling evidence is **C3**: all 64 phase7 / phase7_fixed prediction pairs
   of the MAIN set are bit-exact on `true_label`, `fwd_move_ticks` and
   `mid_price_t`, so the two sides share one label vector and one evaluation
   population. **C5 is DECIDED (2026-08-10): the original runs WRAPPED** — the
   versions pinned are pandas 3.0.1 / numpy 2.4.2 and the f2 rebuild is an
   execution witness, not a counterfactual. The uint32 wrap is therefore recorded
   as documented as-built behaviour of both lineages, not as a rebuild artifact.

2. **Both stored sides share ONE column universe — and the earlier "both sides
   pre-fix" reading was the LINEAGE mistaken for the pair.** The pinned fixture is
   the Phase 7 universal-lag pre/post pair, MAIN prediction set, RE-EVALUATE class:
   pre-fix `results/phase7/l2_predictions/` and post-fix
   `results/phase7_fixed/l2_predictions/`, 64 parquets each, same 64 filenames,
   8 instruments x 2 architectures x 4 horizons. ZC 5s = 1,047,430 rows on both
   sides. Recorded meta: `results/phase7/l2_model_meta.csv` lines 49-56 (ZC 5s
   0.9662 / 0.9659, LightGBM / XGBoost) and
   `results/phase7_fixed/l2_model_meta.csv` lines 18-25 (ZC 5s 0.9315 / 0.9324).
   Both sides are phase7-family `l2_` outputs over the 35-column, MBO-free
   `ALL_L2_FEATURES` set; the pre-fix stored side is **not** a 45-column
   MBO-reading Phase 5 build. Evidence, all from the archive: the two
   `methodology_note.txt` files share SHA256
   `ea11e0ffd382167d8209259a6847234c9dd99c7345ea29e801dbc8d0ee113535` and both
   state the models use "L1+L2 features only ... no MBO data"; neither
   `l2_sim_results.csv` carries a `feature_set` column, unlike every 45-set family
   file, which carries it with values `Full` / `BFree`; and the one phase7 pre/post
   pair whose provenance IS recorded — the PC2 sibling — is 35-column no-MBO on
   both sides, with the lag as the only recorded difference. Independently
   re-derived by the Y1 column-universe walk: of the 35 fed columns, source class
   is snapshot parquet 13, trades parquet 11, derived-from-another-column 9,
   clock-only 1, MIXED snapshot+trades 1, and **MBO 0 of 35**.
   **The limit, recorded rather than smoothed:** this is inference from prose and
   structure, not from code. Both stored sides were written by main-PC generators
   ABSENT from the archive — the one archived phase7 script writes a different
   filename pattern (`phase7_l2_sim.py` line 715) and produced neither directory.
   Two further gaps are recorded: no archived record accounts for the post-fix
   side's CL/ES/HE/LE prediction files, and the pre-fix side has 64 prediction
   files against 63 meta rows. The strongest positive evidence is T4's
   self-consistency result — on the projected 35-column set,
   `corrected[t] == contaminated[t-1]` EXACT on all 28 projected columns, max
   absolute difference 0.0, zero NaN-placement mismatches, on both run pairs —
   measured on the f2 rebuild, so it is evidence by lineage, and its artifact is
   named with it.

3. **Fixture re-basis.** PREREG.md section 6.2 line 445 locks "Reference AUC:
   0.957 and 0.675, acceptance interval ±0.010 absolute." **Neither number is
   reproduced by the fixture the registration names.** AUC recomputed directly
   from the stored `pred_score` / `true_label` columns of the pinned pair
   (ZC, LightGBM):

   | Horizon | Pre-fix | Post-fix | n rows |
   |---|---|---|---|
   | 5s  | 0.966244 | 0.931536 | 1,047,430 |
   | 10s | 0.939968 | 0.756504 |   655,016 |
   | 30s | 0.856419 | 0.679288 |   745,656 |

   Against 0.957 ± 0.010 on the pre-fix side and 0.675 ± 0.010 on the post-fix
   side: 5s passes pre (|0.966244 - 0.957| = 0.009244) and fails post by 0.2565;
   10s fails pre by 0.0170 and fails post by 0.0815; 30s fails pre by 0.1006 and
   passes post (|0.679288 - 0.675| = 0.004288). **There is no horizon at which the
   registered pair is reproduced.** The model family also changes: the original
   documented protocol names XGBoost
   (`MASTER_FINDINGS\preregistration_v4.txt` line 273, hyperparameters at line
   284); the recomputed trio above is LightGBM, and the declaration names the
   family rather than leaving it implicit. The recomputation is authoritative
   rather than merely alternative because the fixture is the stored-prediction
   pair: AUC over `pred_score` and `true_label` is a pure function of bytes
   already on disk — no retraining, no re-randomization, no environment
   dependence. Of 128 result rows, 95 carry recorded meta and all 95 match the
   recomputation at 4 decimal places (`flag_gt_5e-5` False throughout); the
   remaining 33 have no recorded counterpart and are therefore neither confirmed
   nor contradicted.

4. **The M5 falsification, and what it forced.** The M5 sweep extended the
   corrected-side check beyond ZC 2025-01 — the same strict/equal violation counts
   at boundary `decision_T`, both sides, over the per-class event sets — and
   **falsified the assumption that the corrected side is clean.** Row-level
   verification is recorded, not asserted: a named cl 2025-01 `trades_all` row at
   T_i = 2025-01-02 13:01:11.865879 absorbs a trade at 13:01:11.914518,
   **48,638,830 ns after the decision time.** Extended by N1 to 48
   instrument-months on both sides with unscored cells ledgered, the corrected
   side carries strictly-post-decision absorption in **18 of 48**
   instrument-months, peaking at **111,334 of 580,944 rows (19.16%)** on
   zc 2025-09, class `mbo_all`. N1 reproduces **every one of M5's 453 cells
   exactly, 0 disagreements**; M5 is superseded in coverage and is not superseded
   as the reason. Criterion 3 as registered — "**No runtime finding of any tier,
   primary or secondary**, appears on `fixture_corrected`" (line 461) — would
   therefore fail the gate on a correctly-behaving detector reporting a real
   violation the fixture really contains. That is the measurement that forced the
   criterion-3 amendment.

5. **The ground-truth map, measured on both sides.** What criterion 3 is amended
   to score against is an artifact, and the artifact was measured before the
   criterion was written: `n1\declared_map.csv`, **984 rows** = **960
   declared-class cells** (2 sides x 8 instruments x 6 months x 10 classes) plus
   **24 rows** carrying the 11th diagnostic class `mbo_all_rows`. Of the 960:
   **888 SCORED** and **72 UNSCORED_FOR_LACK_OF_DATA**. Boundary is `decision_T`
   on every row. Scope: 8 instruments (cl, es, gc, he, le, nq, zc, zs) x 6 months
   (2025-01, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12) = 48 instrument-months.
   The 72 unscored cells are ledgered by name and path and enter no denominator.
   `mbo_all_rows` is measured as a diagnostic class and is not one of the declared
   10, so a maximum quoted across classes is only defined once its class set is
   named — two M5-quoted maxima came from the diagnostic class and differ from the
   declared-10 maximum.

6. **The criterion-1 denominator, re-derived from the map by a stated rule.** The
   registration's criterion-1 denominator had been read off the fixture manifest's
   construction classes; the manifest's leak-source classification carries no gate
   arithmetic. Re-derived from the declared map, the 35 fed columns partition
   three ways, each class enumerated **by column name** rather than as a count:
   **REQUIRED 11**, **OUT OF JURISDICTION 22**, **UNSCORED 2**, and the partition
   check **11 + 22 + 2 = 35** against
   `f3\fixture_manifest_DRAFT.json` `counts.total_fed_to_phase7`. The rule that
   yields the partition is stated rather than assumed — REQUIRED iff the
   construction carries the wall-clock `ts_floor` join and is not
   degenerate-constant; OUT OF JURISDICTION iff it reads only same-row book/clock
   values; UNSCORED iff degenerate-constant or unconstructible under T4, with
   UNSCORED taking precedence where clauses conflict — and the rule was checked
   against the enumeration column by column with no disagreement. Cross-checked a
   second way: the 35 columns cut by SOURCE (snapshot 13 / trades 11 / derived 9 /
   clock 1 / MIXED 1 / MBO 0) and by GATE class (11 / 22 / 2) were built from
   different artifacts for different purposes, and the two cuts compose. The
   manifest's independently-leaking-source count **25** is measured and recorded
   as provenance with **no arithmetic attached**; it is not the denominator.

7. **The fed-column restriction, measured on both sides.** The fixture's column
   universe reads no MBO source on either side, so restricting the scored surface
   to the four `trades_*` classes was applied to the corrected side and to the
   contaminated side and both profiles were measured. **Corrected:** the strict
   cell set is UNCHANGED at **18 of 48** — the same 18 cells — and the equal
   arithmetic collapses, equal-non-zero **35 / 48 → 11 / 48** (equal-only 17 → 2);
   the corrected peak falls from **zc 2025-09, 111,334 strict (19.16% of 580,944
   rows)** to **zc 2025-10, 34,492 strict (5.44% of 634,445 rows)** — a different
   cell as well as a smaller number. **Contaminated:** strict-positive cells
   **48 / 48 restricted and 48 / 48 full-class**, so the restriction moves no cell
   off zero and none onto it; equal-non-zero **23 / 48 restricted vs 42 / 48
   full-class**; restricted strict RATE spans **8.76%** (he 2025-09) to a
   summary-level peak of **88.17%** (es 2025-11, 484,420 / 549,424), median
   **21.66%**, with the unqualified maximum **90.83%** (nq 2025-01) measured as a
   coverage artifact — nq has no MBO classes to drop, so its restricted and
   full-class figures coincide for a reason unrelated to the restriction. The
   restricted ABSOLUTE peak is **es 2025-01, 514,323 of 605,290 rows = 84.97%**.
   Full-class strict rate spans **25.45%** (le 2025-11) to **98.93%** (es 2025-12,
   class `mbo_all`), median **63.08%**; the per-cell delta runs **0.00 pp** (all
   six nq cells) to **48.72 pp** (zc 2025-01, the largest of all 48). On both
   sides `trades_buy` is **0 strict and 0 equal in all 48 cells** — identically
   zero in all 96 of its cells — so the restricted surface is carried by three
   live classes, not four.

8. **Two elements were measured UNSATISFIABLE as registered, and the measurement
   is recorded here.** (a) Line 450 requires the contamination availability class
   "recorded in the manifest"; key search over both
   `f3\fixture_manifest_DRAFT.json` and `t4\fixture_manifest_35col_DRAFT.json`
   found no named field for it. (b) Line 451 requires a sliced variant "from the
   same padded slicer as user-facing slice auditing"; no artifact in this spike
   produces or names one, and no padded slicer has been run — because at the
   instant line 95 requires the amendment to be committed, no slicer exists. What
   the registration does with each is in the `prereg-v30a` diff, not here.

9. **One measurement about the record itself.** The derivation rule of item 6 was
   destroyed and recovered during this work: a restage copied a transient build
   copy of the availability declaration over the repository-root file while the
   root was ahead of it, removing roughly 7.6 KB present only in the root. The
   file was outside version control at the time, so no git history and no on-disk
   copy survived, and the content was recovered from a session transcript. It is
   recorded here because the recovered text is part of what this amendment
   commits, and because a reader is entitled to know that one section of it has a
   recovery in its provenance rather than an unbroken edit history. The
   declaration and `PRIOR_ART_VERIFICATION.md` were placed under version control
   in a separate prior commit for that reason.

### What this entry does NOT do

- It does not restate or alter any acceptance criterion, unit, denominator,
  state, or tier licence. Per section 0.2.1, "the amended tag carries the new
  semantics" — the semantics live in the `prereg-v30a` diff to PREREG.md, not
  here. Every rule sentence above is a quotation.
- It does not touch the `prereg-v30` tag ("This tag never moves" — tag message
  and README).
- Detector status at time of measurement: no detector implementation exists
  (README: "No detector implementation exists."), so the section 0.2.1 path
  "committed and externally timestamped before the affected detector is
  implemented or evaluated" applies — NOT the post-hoc re-draw path of
  section 0.2.1 / section 6.4 ("the affected benchmark is regenerated as a new
  version under §6.4"), which governs only a class C change discovered after
  the affected detector already exists.
- It does not record a stopping-rule firing. Section 0.2 did not fire. The firing
  count stays at twenty-one, in thirteen listed entries, twenty-three entries
  counted.
- The restricted maps of item 7 are a REPORTING object. They are not a second
  scoring key and they change no adjudication; the gate scores against
  `n1\declared_map.csv` as frozen.

### Integrity chain for this amendment (section 0.2.1)

"An amendment inherits §11's integrity chain in full: signed tag, both file
hashes in the tag message, external timestamp receipt committed, repository
publicly reachable at lock."

- Signed tag: `prereg-v30a`, «CEREMONY-FILL: tag date»
- Tag message hash block: **SIX** SHA-256 lines — `PREREG.md`, `DESIGN.md`,
  `HISTORY.md`, `tools/check_registration.py`, `protocol/runtime_reference.py`,
  `AVAILABILITY_DECLARATION.md` — computed at tag time from the files as
  committed, in one operation. The values are not reproduced in this entry:
  «CEREMONY-FILL: paste the six-line block exactly as it appears in the signed
  tag object».
- OTS receipt: `amendment-commit-v30a.txt.ots`, committed in follow-up commit
  «CEREMONY-FILL: hash», upgraded at block heights «CEREMONY-FILL: heights».
```

---

## 2. Every placeholder, and its disposition

**Filled: 2 of the skeleton's markers, plus all six measurement bodies. Cannot fill: 6.** All six
unfillable are ceremony-time values, and five of the six are values R15 or the OpenTimestamps
protocol forbids knowing in advance.

| Placeholder | Status | Value / reason |
|---|---|---|
| Date recorded | **CANNOT FILL** | The ceremony has not run. Convention to apply is settled by `HISTORY.md` H-L12 as landed (l.218): "Dated by the day recorded, not the day worked." Use the calendar date the entry is committed. |
| Amendment commit hash | **CANNOT FILL** | The commit does not exist. It is `git rev-parse prereg-v30a^{commit}`, read after the tag is cut. **Amend trap:** if the commit is amended after the hash is read, the pre-amend value is void. |
| Amended sections | **FILLED** | §6.2 lines 445, 450, 451, 461 plus §10.2. Source: declaration §A.11 walk summary (by anchor — heading "A.11 — Walk summary") ("Four amendments (445, 450, 451, 461)") and §A.12 / §D.1 item 5 for the §10.2 "waived" definition. The lock-table caveat is carried as a conditional sentence because the reviewed `PREREG.md` diff does not exist yet. |
| Item 1, chronology | **FILLED** | Confirmed against F1–F4 and delta-R2 C1–C4/T4; C3 named as controlling; C5 recorded as DECIDED-WRAPPED with the pinned versions. |
| Item 2, which builder produced each side | **FILLED — and the skeleton's framing is CORRECTED** | See §4. The honest answer is that **no generator code exists for either side**; the column-universe identity is established by three archive artifacts, by T4, and now independently by the Y1 source cut (MBO 0 of 35). The limit is stated in the entry rather than hidden. |
| Item 3, AUC recompute | **FILLED** | Both numbers fail to reproduce, at every horizon. Full trio, deltas, model-family change, and the 95-of-128 meta-corroboration reach are in the entry. |
| Items 4–9 | **FILLED** | New in this revision: item 5 (the map as a measured artifact), item 6 (the R11 partition and the §A.6.0 derivation rule), item 7 (the two-sided fed-column restriction), item 9 (the §A.6.0 recovery). Every figure re-verified against the working-tree declaration this pass — see §3. |
| Tag date | **CANNOT FILL** | Set when the author signs. |
| The SHA-256 block | **CANNOT FILL — and any earlier "five-line" instruction is wrong** | It is **SIX** lines (declaration §D.2, cited by anchor — the `l.3420` this carried until R67/§17.2 had drifted 169 lines; and the set itself is `$FILES` at `CEREMONY_COMMANDS.md` §3.2 l.180). R15 forbids any hash existing before the single tag-time operation; writing values here would create exactly the carried-forward value R15 prohibits. |
| OTS receipt filename | **FILLED** | `amendment-commit-v30a.txt.ots`, per the v30 precedent (commits `5842857`, `0ee26c4`). **Must not overwrite `registration-commit.txt{,.ots}`, which is v30's record and is tracked.** |
| Follow-up commit hash | **CANNOT FILL** | The follow-up commit does not exist. |
| Bitcoin block heights | **CANNOT FILL** | Not known until the OTS upgrade succeeds. v30's were 961654 and 961656. |

Every unfillable value is marked `«CEREMONY-FILL: …»` rather than with a bracket that could be
mistaken for prose or for a citation, so one grep before the commit finds all of them:

```sh
grep -n '«CEREMONY-FILL' DEVIATIONS.md    # MUST return nothing before the commit
```

---

## 3. Provenance of every figure in the entry, re-verified this pass

Line numbers are into the working-tree `AVAILABILITY_DECLARATION.md`, **derived not
transcribed** — as at R69: sha256 `4c07c76ffbb2fe7b04a903d01d74d56bd2f80bf266f70f7fe2e45ea73a636403`,
303,643 bytes, 3,955 lines. **Any declaration line number below is stale unless it was
re-derived against that hash**, which is why the citations that matter are given by anchor.
*(This paragraph read `f0829bd3…` / 277,411 for several rounds after the file had moved;
checked by D7 from R68.)* **These citations are for the drafter and the ceremony record; they do not go into
`DEVIATIONS.md`.**

| Figure in the entry | Verified at |
|---|---|
| Registered AUC pair 0.957 / 0.675 ± 0.010 | §A.1 l.777, quoting `PREREG.md` l.445 |
| LightGBM trio and row counts | §A.1 table ll.786–790, source `f1\f1_results.csv` `recomputed_auc` rows 50–52 / 114–116 |
| Deltas 0.009244 / 0.2565 / 0.0170 / 0.0815 / 0.1006 / 0.004288 | §A.1 "Why the old anchor cannot stand" item 1, ll.797–800 |
| Criterion 3 registered text | §A.8 l.1410, quoting `PREREG.md` l.461 |
| 18 of 48; 111,334 / 580,944 = 19.16%; class `mbo_all` | §A.8 ll.1425–1426; §13 ll.1993–1994, l.2008 |
| cl 2025-01 row, 48,638,830 ns | §13 l.2183 |
| M5's 453 cells reproduced exactly, 0 disagreements | §13 l.1708, l.2187 |
| `declared_map.csv` 984 / 960 / 24 / 888 / 72; 10 classes + `mbo_all_rows` | §13(a), ll.1963–1975 |
| REQUIRED 11 / OUT OF JURISDICTION 22 / UNSCORED 2 / 35 | §D.1 item 2 ll.3374–3387; §A.6.4 partition check l.1257 |
| The derivation rule and its precedence clause | §A.6.0 ll.1047–1068 |
| SOURCE cut 13 / 11 / 9 / 1 / 1, MBO 0 | §A.6.5 ll.1274–1280 |
| Manifest count 25 recorded with no arithmetic attached | §A.11 l.1501; §D.1 item 2 ll.3388–3390 |
| Corrected restriction: 18 of 48 unchanged; equal 35/48 → 11/48; peak zc 2025-09 → zc 2025-10, 34,492 / 634,445 = 5.44% | §13(i) ll.2418–2424 |
| Contaminated restriction: 48/48 both; equal 23/48 vs 42/48; 8.76% – 88.17%, median 21.66%; 90.83% coverage artifact; ABSOLUTE 514,323 / 605,290 = 84.97%; full-class 25.45% – 98.93%, median 63.08%; delta 0.00 pp – 48.72 pp | §14 item 4 BINDING clause ll.3105–3118; §14.1 ll.3194–3205 |
| `trades_buy` 0 / 0 on both sides, all 96 cells | §13(i) ll.2410–2416 |
| §A.6.0 recovery incident | commit `ffa6d94` message; `evidence/fixture_spike/f4/DECLARATION_POINTER.md` |

**One figure deliberately not carried into the entry.** The 2,587-byte / 584-byte OTS receipt
sizes and the v30 block heights 961654 / 961656 appear in §2 as *reasons a placeholder cannot be
filled*, never as values for D-001's own receipt.

---

## 4. The substantive correction to the F5 skeleton, restated and re-verified

**The skeleton's item 2 heading — "Both sides of the fixture pair are pre-fix" — and its
parenthetical "(Phase 5 ZC CNN 5s per Phase 0 findings)" are both superseded by the declaration's
own later work. The entry above does not carry them forward.** This correction was made in the
previous revision of this file and is re-verified here rather than assumed.

- **On the pair's identity.** Declaration §8 (l.1599) pins the fixture as the Phase 7
  universal-lag pre/post pair, MAIN prediction set, RE-EVALUATE class, and §A.1 declares the ZC
  **LightGBM** trio. "Phase 5 ZC CNN 5s" is not that object. The entry names §8's object.
- **On "both sides pre-fix".** §0.4 (item Y1) resolves it explicitly: the earlier reading —
  pre-fix side = 45-column MBO-reading `phase5_ml.py` build, post-fix side = `phase7_l2_sim.py` —
  "is not an asymmetry of the fixture. It is the LINEAGE described as if it were the pair." Both
  stored sides are phase7-family `l2_` outputs over one 35-column MBO-free universe.
- **Why the correction is load-bearing rather than cosmetic.** §9's licence reads the pre/post AUC
  delta as a **feature-availability-only** effect, which requires the two sides to differ in
  availability and nothing else. A column-set change is not an availability change. Had the two
  sides genuinely carried different column universes, the delta would confound a change of columns
  with a change of *when* columns are knowable, and the licence would fail outright — taking §A.1's
  reference trio and the discrimination framing of the whole gate with it.
- **Newly available corroboration, not present at the previous revision.** The Y1 source cut
  (§A.6.5) independently establishes MBO **0 of 35** on the fed universe, and the fed-column
  restriction of item 7 is applied to *both* sides on exactly that premise — the premise is
  side-independent, which is what makes the symmetric restriction legitimate. The correction is now
  supported by a second instrument rather than by prose comparison alone.

---

## 5. Append-only compliance

`PREREG.md` §11 item 6: "`DEVIATIONS.md` append-only." The file is 0 bytes, so D-001 is a pure
append and nothing above the append point exists to change. For D-002 and later the rule binds:
append below, never edit above. **Verification before commit:**

```sh
stat -c '%s' DEVIATIONS.md                               # 0 before; non-zero after
git diff --cached -- DEVIATIONS.md | grep -c '^-[^-]'    # MUST be 0 — no deleted lines, ever
grep -n '«CEREMONY-FILL' DEVIATIONS.md                   # MUST return nothing
```
