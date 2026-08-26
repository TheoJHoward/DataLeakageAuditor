# K6_RESULTS.md — the §9.2 cross-tool comparison, EXECUTED

**Item K6, 2026-08-14. This one ran.** Eleven tools, eight hand-written cases and their eight
clean paired controls, 88 tool × case cells, executed on Windows 11 with Python 3.12.10.

`PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are **byte-unchanged**.
No git state-changing command was run. The archive at `MBO_2025` was not touched. Every tool was
installed into a dedicated virtualenv outside the repository and outside the archive.

**Deliverables:** `PRE_RUN_RECORD.md` (versions, configuration, eligibility, label mapping — all
fixed *before* the first tool ran) · `RESULTS_MATRIX.md` (computed by `harness/score.py`) ·
`RUN_LOG.md` · `env/VERSIONS.txt` · `raw/` (per-tool JSON) · `cases/` (the case set and its
SHA-256 manifest) · `harness/` (case definitions, runners, scorer).

---

## 1. THE HEADLINE

**The §10.1 kill gate does NOT fire. No single tool satisfies all five criteria — every tool
fails criterion 1, and criterion 3 is unevaluated for every tool.**

**And the load-bearing negative result is measured rather than asserted — at the strength the
evidence actually supports, which is narrower than this file first claimed. On C6, the
one-bar-of-reach case, ONE in-kind tool was measured and missed.** *(Re-scoped 21 August 2026,
R57/W2a, after independent re-verification by a party that did not produce this run. The
sentence here previously read "five eligible tools produced zero hits", which is arithmetically
true and invites the reading that five independent detectors examined C6 and failed. One did.)*

Of the five declared eligible: **`leak-detect`** is the only informative miss — a demonstrably
live probe that fires on C5 both sides and on C2 contaminated. **`deepchecks`** could not
register a hit by construction: its only T6-mapped check tests train/test **date** overlap,
which C6 holds identical on both sides. **`Leakly`** fired on **0 of 8** cell-sides and no
positive control was ever established for it. **`temporalcv`**'s recorded evidence is unsound —
of its three T6-mapped gates, `gate_temporal_boundary` is **never called** and
`gate_suspicious_improvement` is wired with **inverted polarity** and cannot fire.
**`leakage-buster`** crashed on NaN because its adapter alone omits `.dropna()`, and C6 is the
**only** case in the set containing NaN — a harness defect landing on exactly the flagship case.

**Every one of these defects leans the same way: toward the conclusion this project wants.**
The harness fixes and the re-run are tracked separately as W2b; until they land, **no form of
the five-tool claim may be cited.** `PREREG.md` line 165's standing disclaimer ("Comparative completeness
is not claimed here. Whether this is more complete than existing tooling is what Phase 0 (§10.1)
tests") has now been tested, for the tools run and only for them.

---

## 2. COUNTS, INCLUDING ABSTENTIONS (§9.2 items 4 and 5)

| | Cells |
|---|---|
| **Total tool × case cells** | **88** (11 tools × 8 cases) |
| Eligible, declared before any run | 36 |
| Declared ineligible → abstention (item 4) | 52 |
| **HITS** | **9** |
| **MISSES** | **14** |
| **ABSTENTIONS, total** | **65** — 52 ineligible + 13 crash/not-runnable |

Counts are the conservative reading of the one ambiguous cell (§6). The strict reading is
8 hits / 15 misses / 65 abstentions; no verdict in this document changes between the two.

### 2.1 The matrix

| Tool | C1 T1 | C2 T2 | C3 T3 | C4 T4 | C5 T5 | C6 T6 | C7 T7 | C8 T8 | H | M | A |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leak-detect` 0.0.1 | abst | abst | abst | abst | miss | **miss** | abst | abst | 0 | 2 | 6 |
| `deepchecks` 0.19.1 | **HIT** | abst | abst | **HIT** | **HIT** | **miss** | abst | **HIT** | 4 | 1 | 3 |
| `leakage-buster` 1.0.2 | miss | abst | abst | miss | **HIT** | **abst¹** | miss | abst | 1 | 3 | 4 |
| `Leakly` 0.1.2 | abst | miss | miss | abst | miss | **miss** | abst | abst | 0 | 4 | 4 |
| `leakage-analysis` | abst² | abst² | abst² | abst² | abst | abst | abst | abst | 0 | 0 | 8 |
| `LeakageDetector` 2.0 | abst³ | abst³ | abst³ | abst³ | abst | abst | abst | abst | 0 | 0 | 8 |
| OMDS 0.1.0 | miss | **HIT** | abst | abst | abst | abst | abst | abst | 1 | 1 | 6 |
| `temporalcv` 2.3.0 | miss | abst | abst | abst | abst | **miss** | abst | abst | 0 | 2 | 6 |
| `leakfence` 0.5.0 | **HIT** | miss | abst | **HIT⁴** | abst | abst | **HIT** | abst | 3 | 1 | 4 |
| `leakr` 0.1.0 (R) | abst⁵ | abst | abst | abst⁵ | abst⁵ | abst | abst | abst | 0 | 0 | 8 |
| `bioLeak` 0.3.8 (R) | abst | abst | abst | abst | abst⁵ | abst | abst | abst | 0 | 0 | 8 |

¹ crash-abstention (item 5): `Detector error: target_leakage` on **both** sides.
² crash-abstention (item 5): 16/16 runs died at `src/irgen.py:373 visit_Subscript AssertionError`.
³ **not programmatically runnable** — VS Code extension, no headless entry point (scope ruling).
⁴ the one ambiguous cell; see §6. Strict reading: miss + false alarm.
⁵ R toolchain could not be installed — machine-wide install requires administrator elevation.

### 2.2 The crash register (item 5 — "counts published")

| Tool | Cells crashed | Error |
|---|---|---|
| `leak-detect` | **8 of 8** default-configuration cells (the complex probe) | `AttributeError: module 'numpy' has no attribute 'complex'` at `base.py:76` / `base.py:209` |
| `leakage-buster` | 2 (C6 both sides) | `Detector error: target_leakage` — an internal detector exception the tool itself reports |
| `leakage-analysis` | **16 of 16** | `AssertionError` at `src/irgen.py:373 visit_Subscript` — its own IR generator, before the datalog stage |
| **Total crashed cell-runs** | **26** | |

`leak-detect`'s crash is **probe-specific and was scored probe-wise**, per
`J6_SCOPED_PLAN.md` (d.3): only the complex probe calls `np.complex`. The NaN probe was run
separately under the **documented public parameter** `only_nan=True` and its results were scored
on merit. Scoring the whole tool as a crash-abstention would have let the only in-kind competitor
escape the flagship case on a technicality, in this project's favour.

### 2.3 The false-alarm register (the clean controls doing their job)

| Tool | Case | What fired on the CLEAN control |
|---|---|---|
| `leak-detect` | C5 | horizontal probe fired on the legitimately **lagged** label — 399 of 400 rows |
| `leakage-buster` | C7 | `KFold leakage risk (use GroupKFold)` on both sides |
| `leakfence` | C2 | `global_preprocessing` on both sides — a structural lint cannot see what `fit()` was given |
| `leakfence` | C4 | `duplicate_rows` on both sides (the straddle marker differs — §6) |
| `deepchecks` | C1, C6, C7, C8 | `Identifier Label Correlation` on both sides — **attributable to the `row_id` adapter this item added to help the tool**, not to deepchecks' own defaults |
| OMDS | C1, C4–C8 | `ax:fit_on_train_only` at **warn** severity on both sides — the documented "murky" branch when a function contains no `train_test_split` |

### 2.4 The unmapped register (labels that scored nothing)

Published so a later reader cannot reconstruct a more flattering mapping. `deepchecks`
`Data Duplicates`, `Feature Label Correlation Change`, `Conflicting Labels`; `leakage-buster`
`CV strategy recommendation`, `Time-awareness suggestion`; `temporalcv` `gate_synthetic_ar1`,
`gate_residual_diagnostics`, `gate_theoretical_bounds`.

**One label was discovered only at run time and is therefore unmapped: `leakage-buster`'s
`WOE leakage risk`,** which fired on both sides of seven of eight cases. §9.2 item 3 requires the
mapping be written "before running", so it could not be mapped afterwards. **Note this cuts in the
competitor's favour:** had it been mapped to T5 as its detector family suggests, it would have
fired on C5's clean control and turned `leakage-buster`'s single hit into a miss.

---

## 3. WHAT THE COMPARISON ESTABLISHES

### 3.1 C6 — the flagship. One in-kind tool measured and missed; three could not register a hit; one crashed on a harness defect.

| Tool | C6 result | Evidence |
|---|---|---|
| `leak-detect` | **miss** | `No vertical leakage detected. Good to go! Yay!!` on **both** sides |
| `deepchecks` | **miss** | its only T6-mapped check, `Date Train Test Leakage Overlap`, ran and returned **0 on both sides** |
| `Leakly` | **miss** | permuted-label AUC 0.495 (contaminated) vs 0.496 (clean); p = 0.68 |
| `temporalcv` | **miss** | every gate PASS on both sides |
| `leakage-buster` | **abstention** | its `target_leakage` detector crashed on both sides; its T6-mapped `Rolling statistics` detector ran and was silent |

C6 is one bar of reach: a trailing 5-bar mean that **includes the decision bar**, against a
declared per-cell availability model, versus a clean control ending at *t−1*. Both sides are
strictly backward-looking in row position, which is exactly why a row-position cut cannot see it.

### 3.2 `PREREG.md` line 156's claim about `leak-detect`, now executed rather than read

The registration states the v7 defect: **"it cuts on row position, so it cannot see current-bar
inclusion and it false-flags a legitimately lagged label."** Both halves reproduced:

- **Cannot see current-bar inclusion** — C6, silent on both sides. Its `check_row_number` defaults
  to `int(len(input_data)/2)`, i.e. pure row position (verified at source, `base.py:149`).
- **False-flags a legitimately lagged label** — C5, `Oops horizontal leakage detected!!
  risk_score : 399` on the **clean** control whose feature uses the *previous* row's label.

This is the single highest-value cell in the matrix and it now rests on an executed result.

### 3.3 What competitors DID do — reported because it is real

- **`deepchecks` is the strongest tool on this case set: 4 hits of 5 eligible cells** (T1, T4, T5,
  T8), and it is **the only tool in the roster with explicit executed/not-run accounting**.
- **`leakfence` scored 3 hits** (T1, T7, and T4 on the conservative reading) — a genuinely 2026
  tool, so the comparison cannot be dismissed as being against old software.
- **OMDS scored the only T2 hit**, at `certain` severity, silent on the clean control.
- **Six of eight published types were hit by at least one tool** — T1, T2, T4, T5, T7, T8.
  **T3 and T6 were hit by nothing.**

### 3.4 What it does NOT establish — stated plainly

- **Nothing about the acceptance-fixture surface.** It was not run. §10.1 criterion 3 is
  **unevaluated for every tool** and no wording here implies otherwise.
- **Nothing about `leakage-analysis`, `LeakageDetector` 2.0, `leakr` or `bioLeak`** — 32 cells,
  all abstentions, all with recorded reasons.
- **Nothing about L1.4b, L2b, L3.1b.** The eight-case reading instantiates only one sub-row each
  of T4, T5 and T6, exactly as `CROSS_TOOL_COMPARISON.md` §2.2 already recorded.
- **No completeness claim.** Nine of eleven tools produced any scored result; one of two surfaces
  was run; eight of eleven detector rows are exercised.
- **The cases are this project's own.** `CROSS_TOOL_COMPARISON.md` §2.2 records the residual
  design-bias risk and it is not eliminated by having run them.

---

## 4. THE §10.1 KILL GATE, CRITERION BY CRITERION

> **§10.1** (`PREREG.md` lines 1018–1024): "**Stop building and contribute upstream if a single
> maintained tool satisfies all five:** 1. Covers at least the same published types at the same
> tier or better; 2. Produces explicit executed / not-run accounting; 3. Fires on
> `fixture_contaminated` and is silent on `fixture_corrected` …; 4. Installs and runs through a
> documented public interface without author modification; 5. Has had a release or commit within
> the previous 12 months." Line 1026: "**Partial satisfaction is recorded and does not trigger the
> stop.**"

### Criterion 1 — coverage of the same published types at the same tier or better

**FAILS for every tool, and this is the criterion the gate dies on.**

| Tool | Types HIT | of 8 published |
|---|---|---|
| `deepchecks` | T1, T4, T5, T8 | **4** |
| `leakfence` | T1, T4, T7 | 3 |
| `leakage-buster` | T5 | 1 |
| OMDS | T2 | 1 |
| every other tool | — | 0 |

The best single tool covers **four of eight**. **No tool covers T6 at all**, and no tool covers
T3. Tier was not reached: coverage fails before the tier axis (`CROSS_TOOL_COMPARISON.md` §2.6
records that §9.2 defines no tier axis, a gap reported and not patched).

### Criterion 2 — explicit executed / not-run accounting

**PASSES for exactly one tool: `deepchecks`.** `SuiteResult.get_not_ran_checks()` returned, per
case, the checks that did not run *with their reasons* — e.g. on C1: `Date Train Test Leakage
Duplicates`, `Date Train Test Leakage Overlap`, `Index Train Test Leakage`, `Identifier Label
Correlation`, each with a `DatasetValidationError` explaining the missing input. `CheckFailure`
objects carry per-check exceptions.

**Partial, and recorded as partial:** `leakage-buster` surfaces detector exceptions as
`Detector error: <name>` risk items — real accounting of a failure, but not of the executed set.
OMDS emits a `summary` count. **All other tools: no accounting of any kind.**

### Criterion 3 — fires on `fixture_contaminated`, silent on `fixture_corrected`

**UNEVALUATED FOR EVERY TOOL.** The fixture surface was not run, for two registered reasons:

1. `PREREG.md` line 448 orders reconstruction **before** the comparison, and
   `AVAILABILITY_DECLARATION.md` lines 3–5 still read "**DRAFT — AUTHOR REVIEW REQUIRED** …
   Nothing in this file is a registered declaration".
2. `J6_SCOPED_PLAN.md` (a.2) declares all rostered tools ineligible on that surface **from
   documentation** — the fixture is a stored per-second prediction pair carrying `pred_score`,
   `true_label`, `fwd_move_ticks`, `mid_price_t`: no features, no split, no callable, no source.

Under §10.1's conjunctive structure an unevaluated criterion **cannot** make the gate fire, so the
verdict is safe. **The record is incomplete, and this is the gap.**

### Criterion 4 — installs and runs through a documented public interface without author modification

| Verdict | Tools |
|---|---|
| **PASSES** | `leak-detect`*, `deepchecks`*, `leakage-buster`, `Leakly`, `temporalcv`, `leakfence`, OMDS |
| **FAILS** | `leakage-analysis` (16/16 crash; cannot be made to run through documented setup on this platform), `LeakageDetector` 2.0 (no headless entry point) |
| **NOT ESTABLISHED** | `leakr`, `bioLeak` — install requires administrator elevation |

\* with dependency **pins** recorded as manual setup under item 6 (`leak-detect`: 2; `deepchecks`:
4). No tool's own source was edited, so "without author modification" is not engaged by any of it.

### Criterion 5 — a release or commit within the previous 12 months (since 2025-08-14)

| Tool | Latest | Verdict |
|---|---|---|
| `leakfence` 0.5.0 | 2026-08-09 | **PASS** |
| OMDS | pushed 2026-08-06 | **PASS** |
| `temporalcv` 2.3.0 | 2026-06-14 | **PASS** |
| `bioLeak` 0.3.8 | 2026-05-21 | **PASS** |
| `Leakly` 0.1.2 | 2026-05-14 | **PASS** |
| `leakr` 0.1.0 | 2025-10-26 | **PASS** |
| `leakage-buster` 1.0.2 | 2025-09-13 | **PASS** |
| `LeakageDetector` 2.0 | pushed 2025-05-07 | **PASS** |
| `deepchecks` 0.19.1 | release 2024-12-15; `main` commit 2025-11-24 | **PASS by commit**, fail by release — scored PASS, the reading generous to the competitor |
| `leakage-analysis` | 2023-05-02 | **FAIL** |
| `leak-detect` 0.0.1 | 2020-07-22 | **FAIL** |

**Correction to the record, confirmed:** `HISTORY.md` H-34 line 282 records "`bioLeak` (CRAN, Dec
2025)". CRAN shows **0.3.8, 2026-05-21**, so bioLeak **is** inside criterion 5's window. The
verdict is unaffected — it fails criterion 1 — but the parenthetical is stale. This reproduces
`CROSS_TOOL_COMPARISON.md` §5 item 4 independently.

### The verdict, plainly

**THE KILL GATE DOES NOT FIRE.**

**Why, per criterion:** **criterion 1 fails for every one of the eleven tools** — the best covers
four of eight published types and **nothing covers T6** — and **criterion 3 is unevaluated for
every tool** because the fixture surface was not run. Two of five criteria are therefore unmet or
unmeasured for every candidate, and §10.1 requires **all five** in **a single** tool.

**The closest candidate is `deepchecks`:** criterion 2 **pass** (the only tool that passes it),
criterion 4 **pass**, criterion 5 **pass by commit**, criterion 1 **fail** (4 of 8 types; no T6),
criterion 3 **unevaluated**. Under line 1026 that is **partial satisfaction, recorded, and it does
not trigger the stop.**

**The finding H-34 rests on is unchanged and is now executed rather than desk-read:** no tool —
new or old — probes a user callable at runtime against a declared per-cell availability model, and
on the case built to test exactly that, **the one in-kind tool able to register a hit did not**.
Three further tools were nominally eligible but structurally unable to register one, and a fifth
abstained on a harness-caused crash — so **this case does not carry the weight of five
independent negatives**, and is not to be cited as though it did (R57/W2a).

---

## 5. §9.2 ITEM-BY-ITEM COMPLIANCE

| Item | Line | Discharged how |
|---|---|---|
| 1. Eligibility per tool × case, before any run, from documentation | 975 | `PRE_RUN_RECORD.md` §4, written before the first case ran. The `[P]` cells were re-declared against installed versions under a **union rule that only widens** eligibility |
| 2. Versions and configuration recorded | 976 | `PRE_RUN_RECORD.md` §2 and `env/VERSIONS.txt`, captured before results were read, including the documentation-vs-installed delta field |
| 3. Label mapping written down before running | 977 | `CROSS_TOOL_COMPARISON.md` §2.5 carried unchanged + `PRE_RUN_RECORD.md` §5 additions. **`WOE leakage risk` was discovered at run time and is therefore unmapped**, not retro-mapped |
| 4. Ineligible → abstentions, not misses | 978 | 52 cells, each with a reason in `RESULTS_MATRIX.md` |
| 5. Crashes → abstentions, counts published | 979 | 26 crashed cell-runs, §2.2, with errors |
| 6. Manual setup allowed and recorded | 980 | `PRE_RUN_RECORD.md` §3, nine steps S1–S9 including two **failed** attempts |
| 7. No case excluded after results are seen | 981 | All eight cases and both sides scored. `cases/MANIFEST.json` hashes were fixed before the run. **No case was removed, and none of the four ineligible-by-port R cases was dropped — each is a published abstention** |

---

## 6. THE ONE AMBIGUOUS CELL, AND HOW IT WAS SCORED

`leakfence` × **C4 (T4)**. `duplicate_rows` fires on **both** sides, but the message differs:
contaminated `…(24, 224), straddles train/test`; clean `…(24, 124)` with no straddle marker.
`PRE_RUN_RECORD.md` §5.1 declared the mapping with the note that `check_duplicates` is called
*with* the split indices and "is a cross-split test" — so the declared mapping's subject was
already the cross-split violation.

Per the instruction to score ambiguity **against this project's interest**, the reading that
credits the competitor is adopted: **HIT**. The strict label-level reading (miss + false alarm) is
published alongside it in `RESULTS_MATRIX.md`. **No verdict in this document changes either way.**

Other places the same rule was applied, always toward the competitor: the union eligibility rule
(§4.1 of the pre-run record); the generic-verdict mapping for `Leakly` and `leak-detect`;
`deepchecks`'s generous T6 eligibility, inherited from the protocol; scoring `deepchecks` PASS on
criterion 5 by commit; leaving `CV strategy recommendation` and `WOE leakage risk` unmapped rather
than letting them become guaranteed false alarms; and adding the `row_id` index adapter and the
function-wrapped source form so `deepchecks` and OMDS could run checks that were otherwise
skipped entirely.

---

## 7. WHAT REMAINS OPEN

1. **§10.1 criterion 3 is unevaluated.** It is an execution predicate on the fixture surface,
   which is blocked by registered ordering on sign-off of `AVAILABILITY_DECLARATION.md`.
2. **Four tools produced no scored result** — `leakage-analysis`, `LeakageDetector` 2.0, `leakr`,
   `bioLeak` — 32 abstention cells with reasons. Docker/WSL and an elevated R install would close
   the first, third and fourth; both are system-level changes outside this item's authority.
3. **Two supplementary observations, published because they cut in competitors' favour and item 1
   forbids widening eligibility after results are seen.** `leak-detect` separated C2's sides
   (fired contaminated, silent clean) and OMDS separated C3's sides at `certain` severity. **Both
   cells are declared-ineligible abstentions and are scored as such.** Under the fixed §2.5
   mapping `leak-detect`'s vertical probe maps to T6 regardless, so C2 could not have been
   credited in any case. A future re-declaration should consider widening both — *before* the
   next run.
4. **`HISTORY.md` H-34 was committed by a different item while this run was in progress** —
   commit `80401d0`, "Kill-gate sign-off (H-34, prior art) with four factual corrections, plus
   review lessons H-L12 and H-L13". **K6 did not make that commit and ran no git state-changing
   command.** The corrections it carries include the `bioLeak` date, which this item confirms
   independently from CRAN (0.3.8, 2026-05-21). Two consequences worth flagging:
   - **H-34's sign-off now sits in `HEAD` while §9.2 was still unrun at the moment it was
     committed.** This item supplies the missing execution. Nothing in the executed results
     disturbs H-34's judgment — no tool probes a user callable against a declared per-cell
     availability model — so the sign-off stands, but the ordering is worth recording.
   - The working tree also gained an untracked `LICENSE` and a modified
     `tools/check_registration.py` from that concurrent item. **Neither was produced by K6.**
