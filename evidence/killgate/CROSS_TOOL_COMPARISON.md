# CROSS_TOOL_COMPARISON.md — `PREREG.md` §9.2

**Status: DRAFT, UNCOMMITTED, AND NOT A RUN.** Produced by item G3 of the kill-gate completion
pass, 2026-08-14. Nothing here has been committed and no third-party tool has been executed by
this item. This file is the *protocol* half of §9.2 plus the desk-verifiable half of its inputs;
the run half is genuinely outstanding and is enumerated in Part (iii).

**Headline determination (Part 1 below): §9.2 requires EXECUTING third-party tools. It cannot be
assembled from documents, and the cross-tool comparison therefore remains genuinely unrun.**
What documents *can* produce is the protocol and case set that §9.2 requires be committed
**before** any tool is run — which is where this file sits, correctly, in the registered order.

---

## 1. What §9.2 requires — the registered text, verbatim

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`, lines 971–981:

> **971** `### 9.2 Cross-tool comparison — protocol fixed before running`
>
> **973** Phase 0 runs on the acceptance fixture — **after its declaration is reconstructed** (§6.2) — plus a separately enumerated prior-art comparison set of hand-written cases, one per leakage type, committed with this protocol before any tool is run.
>
> **975** 1. **Eligibility** per tool × case, declared before any run, from documentation.
> **976** 2. **Versions** and configuration recorded.
> **977** 3. **Label mapping** written down before running.
> **978** 4. **Ineligible cases score as abstentions, not misses.**
> **979** 5. **Crashes score as abstentions**, counts published.
> **980** 6. **Manual setup allowed** and recorded.
> **981** 7. **No case excluded after results are seen.**

Two further registered lines bind it. `PREREG.md` line 448:

> **448** - **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).

and `PREREG.md` line 991, the Phase 0 row that carries the §10.1 kill gate:

> **991** | **0** | Fixture declaration reconstruction with evidence; prior-art verification; cross-tool comparison per §9.2; licence check | 1–2 wknds | **Kill gate (§10.1)** |

### 1.1 Determination: §9.2 requires execution, and cannot be discharged from documents

**Plainly: §9.2 requires running third-party tools. That cannot be assembled from documents and
remains genuinely unrun.**

Six clauses in the registered text are unsatisfiable without execution, and one is
unsatisfiable without it in principle:

| Clause | Line | Why it needs execution |
|---|---|---|
| "**Phase 0 runs** on the acceptance fixture … plus a … comparison set" | 973 | "runs" is the operative verb; the objects run on are two datasets/case sets, not documents |
| "committed with this protocol **before any tool is run**" | 973 | presupposes a later run this clause is ordered against |
| "declared before any **run**" | 975 | same |
| "**Versions** and configuration recorded" | 976 | configuration is what an operator sets on an installed tool; the installed version is not the documented version |
| "**Crashes score as abstentions**, counts published" | 979 | a crash count is an execution artifact and has no desk analogue |
| "**Manual setup** allowed and recorded" | 980 | setup is installation |
| "No case excluded **after results are seen**" | 981 | there are no results to see without a run |

Only clauses 1 (eligibility, explicitly "from documentation"), 3 (label mapping, explicitly
"written down before running"), and the case-set enumeration of line 973 are desk-completable.
Those three, plus the scoring rules, are what Part (i) below delivers.

The ordering is therefore intact rather than violated: §9.2's own design is that the protocol is
fixed on paper first. This file is the paper. **It is not the comparison.**

### 1.2 What this does and does not mean for the §10.1 kill gate

§10.1 requires **all five** criteria to be satisfied by **a single maintained tool** before the
stop triggers (`PREREG.md` lines 1018–1024). Criterion 1 — "Covers at least the same published
types at the same tier or better" — fails for every candidate on desk evidence alone, so the gate
cannot fire regardless of what the runs return. That is the basis on which `HISTORY.md` H-34
signed off, and it stands.

What the missing runs cost is **not** the gate verdict. It is:

- **§10.1 criterion 3** — "Fires on `fixture_contaminated` and is silent on `fixture_corrected`" —
  which is an execution predicate with no desk substitute. It is currently unevaluated for every
  candidate. Under §10.1's conjunctive structure an unevaluated criterion cannot make the gate
  fire, so the *verdict* is safe; the *record* is incomplete.
- **The published comparison itself.** §9.2 is a deliverable in its own right on line 991, not
  merely an input to §10.1. It is the evidence behind any future comparative statement about this
  tool, and §1.1 line 165 already commits: "**Comparative completeness is not claimed here.**
  Whether this is more complete than existing tooling is what Phase 0 (§10.1) tests." Until the
  runs happen, that test has not been performed and no comparative claim may be made.

---

## Part (i) — THE COMMITTED COMPARISON PROTOCOL

Everything in Part (i) is drafted **before any tool has been run**, which is where §9.2 line 973
requires it to sit. It is not yet committed; committing it is an author ceremony and is not
authorized by this run.

### 2.1 The two run surfaces

§9.2 line 973 names two, and they are not interchangeable:

1. **The acceptance fixture** — `fixture_contaminated` / `fixture_corrected`, under the
   reconstructed declaration of §6.2. This surface is what feeds §10.1 criterion 3.
   **Precondition, registered:** line 448 requires reconstruction to complete *before* this runs.
   The reconstruction currently exists as `AVAILABILITY_DECLARATION.md`, whose own header reads
   "**DRAFT — AUTHOR REVIEW REQUIRED** … Nothing in this file is a registered declaration"
   (lines 3–5), and whose §A.5 records at line 1003: "**SATISFIED.** This whole file is a Phase 0
   product; no cross-tool comparison has been run." **Fixture-surface runs are therefore blocked
   on author sign-off of the declaration, by the registered ordering — not merely by effort.**
2. **The prior-art comparison set** — hand-written cases, one per leakage type, enumerated in
   §2.2. This surface is *not* blocked on the declaration and could run first, except that
   §9.2 line 973 orders the whole of Phase 0's comparison after reconstruction. Read literally,
   "after its declaration is reconstructed" attaches to the fixture clause; whether it also gates
   the hand-written set is an **author reading**, recorded here rather than decided.

### 2.2 The comparison set — eight cases, one per published leakage type

**The enumeration "one per leakage type" resolves to eight cases.** Derivation, so the author can
check it: `PREREG.md` line 325 reads "**Eleven detector rows across the eight published types**",
and §4.1 line 332 partitions the eleven rows. Collapsing the sub-rows that share a published
type — L1.4a+L1.4b, L2a+L2b, L3.1+L3.1b — takes 11 rows to 8 types:

| # | Type | Detector rows (§4) |
|---|---|---|
| T1 | Missing or overlapping declared evaluation split | L1.1 |
| T2 | Preprocessing fit on train+test | L1.2 |
| T3 | Feature selection on train+test | L1.3 |
| T4 | Duplicates across the split | L1.4a, L1.4b |
| T5 | Illegitimate features | L2a, L2b |
| T6 | Features from unavailable cells (temporal availability) | L3.1, L3.1b |
| T7 | Non-independence train/test | L3.2 |
| T8 | Sampling bias in test set | L3.3 |

Cross-check: 1+1+1+2+2+2+1+1 = 11 rows ✓, and §4.1's split (6 RULE + 2 runtime + 3 REVIEW = 11) ✓.

> **Author decision required.** A competing reading is eleven cases, one per *row*. §9.2 says
> "type" and §4 line 325 defines eight types, so eight is the literal reading and is adopted here.
> **Consequence, stated because it is a real cost:** each of T4, T5, T6 instantiates only one of
> its two rows, so the comparison set does not exercise L1.4b, L2b, and L3.1b at all. Which
> sub-row each case instantiates is recorded below and must be recorded in the published result.

**Case specifications.** Each is a minimal hand-written case with known ground truth. They are
specified, not implemented; implementation is Phase 0 work.

| ID | Type / row instantiated | Construction | Ground truth | The trap it sets |
|---|---|---|---|---|
| **C1** | T1 / L1.1 | A declared train/test index pair with a deliberate overlap of *k* indices, plus a clean paired control | Overlap present at exactly those *k* indices | A tool that checks only *disjointness of ranges* passes a set-overlap case constructed from interleaved indices |
| **C2** | T2 / L1.2 | A scaler fitted on the pooled frame, then applied to both sides; clean control fits on train only | Preprocessing fitted on train+test | A tool that inspects only data, not pipeline construction, is **ineligible** here — it must abstain, not miss |
| **C3** | T3 / L1.3 | A feature selector (`SelectKBest`-shaped) fitted on the pooled frame; clean control selects on train only | Selection fitted on train+test | Distinguishes tools that fold selection into "preprocessing" from those that separate it — a **label-mapping** question, settled in §2.5 before the run |
| **C4** | T4 / L1.4a | Exact duplicate rows placed across the split boundary; clean control has the duplicates within one side | Exact cross-split duplication | Within-side duplication must NOT score as a hit; a tool reporting generic "data duplicates" needs its label mapped carefully (§2.5) |
| **C5** | T5 / L2a | A feature column computed from the label value at the same row; clean control uses a properly lagged label | Label leakage into a feature | A pure correlation threshold catches this; the case is deliberately *easy* so that a miss is informative about the tool, not the threshold |
| **C6** | T6 / L3.1 | A trailing window feature that includes the decision bar, against a declared per-cell availability model; clean control excludes it | Current-bar inclusion — one bar of reach | **The flagship case.** Row-position cutting cannot see it (`PREREG.md` §1.1 line 156, the v7 defect). Expect near-universal ineligibility or miss; that is the finding |
| **C7** | T7 / L3.2 | Entity/group IDs appearing on both sides of the split; clean control splits by group | Group overlap across the split | A tool with no group-column concept is **ineligible**, not wrong |
| **C8** | T8 / L3.3 | A test set drawn from a shifted subpopulation; clean control drawn from the same distribution | Sampling bias in test | Drift detectors will fire; whether firing on drift *is* a T8 hit is a label-mapping decision (§2.5), fixed before the run |

**Each case ships with its clean paired control.** A tool that fires on both sides has produced a
false alarm, and the pairing is the only thing that makes that visible. This mirrors §6.2's
`contaminated`/`corrected` structure and is the same discipline.

**Ex-ante integrity, and its limit — stated rather than hidden.** These cases were written after
the desk sweep of the candidate tools, which is exactly what §9.2 item 1 requires ("from
documentation"). No results exist, so item 7 is not at risk. **But §9.2's ex-ante property
protects against post-hoc case *exclusion*, not against case-set *design* bias**, and a case set
written by this project's author with knowledge of what competitors cover could be shaped toward
this project's strengths. The mitigation adopted here: every case is derived from the §4 coverage
map's own row definition and its ground truth stated before eligibility is assessed, and C6 —
the one case this project expects to win — is flagged in the table as such rather than presented
neutrally. The residual risk is real and is recorded, not eliminated.

### 2.3 Tool roster and eligibility (§9.2 item 1)

**Roster inclusion rule, declared now.** A candidate enters the comparison iff it (a) is
installable through a documented public interface, and (b) claims at least one of the eight
published types. Exclusions and their reasons are declared here, before any run.

> **Scope flag for the author.** §9.2 item 7 fixes ex-ante treatment for *cases*. Binding tool
> *exclusions* to the same ex-ante rule is an interpretation made under item 1's authority, not
> registered text. If the author reads it as a new scoring rule rather than an implementation of
> item 1, it belongs in `PREREG.md` via the amendment path and not in this file. Recorded as a
> question, not resolved.

**Included (9).** **Excluded with reason (6),** below the matrix.

Legend — **E** eligible, **I** ineligible (→ abstention per item 4), **[D]** eligibility
documentation-verified in the 2026-08 sweep, **[P]** provisional, requires a documentation read
against the installed version before the run.

| Tool | C1 T1 | C2 T2 | C3 T3 | C4 T4 | C5 T5 | C6 T6 | C7 T7 | C8 T8 |
|---|---|---|---|---|---|---|---|---|
| `leak-detect` 0.0.1 | I [D] | I [D] | I [D] | I [D] | **E** [D] | **E** [D] | I [D] | I [D] |
| `deepchecks` 0.19.1 | **E** [D] | I [D] | I [D] | **E** [D] | **E** [D] | **E** [D] | I [D] | **E** [P] |
| `leakage-buster` 1.0.2 | **E** [P] | I [P] | I [P] | I [P] | **E** [P] | **E** [P] | **E** [P] | I [P] |
| `Leakly` 0.1.2 | I [P] | I [P] | I [P] | I [P] | **E** [P] | **E** [P] | I [P] | I [P] |
| `leakage-analysis` (Yang) | **E** [P] | **E** [D] | **E** [P] | **E** [P] | I [D] | I [D] | I [D] | I [D] |
| `LeakageDetector` 2.0 | **E** [P] | **E** [D] | **E** [P] | **E** [P] | I [D] | I [D] | I [D] | I [D] |
| OMDS / `oh-my-datascience` | **E** [D] | **E** [D] | I [P] | I [P] | I [D] | I [D] | I [D] | I [D] |
| `temporalcv` 2.3.0 | **E** [P] | I [D] | I [D] | I [D] | I [D] | **E** [D] | I [D] | I [D] |
| `leakfence` | **E** [D] | **E** [P] | I [P] | **E** [D] | I [D] | I [D] | **E** [D] | I [D] |

**Eligibility notes that carry weight.**

- **`deepchecks` on C6 is eligible only in the generous sense.** `Date Train Test Leakage Overlap`
  operates on a single `Dataset`-level datetime column (`datetime_name`) and tests whether test
  dates fall inside/before the train range. There is no per-feature or per-cell availability input
  anywhere in the check's API. Calling that eligible for T6 is a **decision made now, before the
  run**, and it is deliberately generous to the competitor: scoring it ineligible would let this
  project's flagship case go uncontested by definition.
- **`deepchecks` on C2/C3 is ineligible on verified absence.** Nothing in the
  `train_test_validation` or `data_integrity` galleries inspects pipeline construction; deepchecks
  sees `Dataset`s and a fitted model. Absence verified across both stable galleries and the
  model-interface contract.
- **`leak-detect` on C6 is the in-kind comparison and is expected to miss.** It is eligible — it
  takes a user callable — and its vertical probe cuts on row position, so it is the direct test of
  the v7 defect. Its complex probe additionally crashes on NumPy ≥ 1.24 (`np.complex`,
  `base.py:76`/`base.py:209`); under item 6 a pinned `numpy<1.24` environment is permitted, and
  **must be recorded as manual setup** rather than silently applied.
- **`leakage-buster` is [P] throughout** because `PRIOR_ART_VERIFICATION.md` records it as
  "ASSESSED FROM PUBLISHED API SURFACE, NOT SOURCE" (lines 35–38). Its eligibility must be
  re-declared from documentation against the installed version.
- **`Leakly` is [P] throughout.** Its PyPI summary ("Leakage checks for machine-learning pipelines
  using permutation tests") and H-34's one-line characterization are all the evidence there is;
  it has not been read at source or at interface level.
- **The R candidates `leakr` and `bioLeak` are held out of the matrix pending a portability
  decision.** §9.2 places no language restriction and item 6 permits manual setup, so excluding
  them needs a reason better than "R". The open question is whether the eight cases can be
  expressed as R data frames without changing what they test. **Author decision.**

**Excluded, with reasons declared before any run:**

| Excluded | Reason |
|---|---|
| `LeakageDetector` 1.0 (PyCharm, `SE4AIResearch/DataLeakage_Fall2023`) | **No licence** (GitHub API `license: null`) — no reuse or redistribution rights; also absent from the JetBrains Marketplace (search API `total:0`), so no documented public distribution channel. Superseded by 2.0, which is in the roster |
| NBLyzer (`microsoft/NBLyzer`) | Repository **archived read-only** 2026-06-15; README is an unfilled Microsoft template with no installation or usage documentation → fails roster rule (a) |
| `mlinspect` | Different object of audit — runtime instrumentation for data-distribution and provenance debugging, not leakage detection → fails roster rule (b) |
| `train-test-leakage-detector` | 1 commit, 0 stars, stdlib-only dataset inspector; author states it "finds leakage that is visible in the data". Borderline on rule (a). **Recommended include if the roster is widened; excluded here to keep the roster to tools with documented interfaces.** Author decision |
| Feature stores (Feast, Tecton, Hopsworks, Databricks, SageMaker) | Prevention-by-construction at retrieval time; they enforce point-in-time correctness rather than auditing arbitrary user feature code → fails rule (b) |
| HindsightBench, JupOtter | Different objects of audit (LLM parametric hindsight; notebook bug detection) → fails rule (b) |

### 2.4 Versions and configuration to record (§9.2 item 2)

Per tool, at run time, recorded before results are read:

`tool name` · `installed version string as reported by the tool itself` · `install channel and
exact command` · `Python or R version` · `OS` · `every non-default parameter set, with its value` ·
`for pinned environments, the pin and why` · `date of run` · `whether the documentation consulted
for §2.3 eligibility matches the installed version, and if not, the delta`.

**The last field is the one that matters** and is easy to skip: eligibility was declared from
documentation, and documentation drifts from releases. `deepchecks` is the live example — stable
docs describe checks under names (`Feature Label Correlation`, `Identifier Label Correlation`)
that replaced earlier ones (`SingleFeatureContribution`, `IdentifierLeakage`), while the last
release is 0.19.1 (2024-12-15) and `main` has moved since. An eligibility declared from `stable`
docs and a run against 0.19.1 are not automatically the same thing.

### 2.5 Label mapping, written down before running (§9.2 item 3)

Each tool's output label → this project's type. Fixed now; not revisable after results are seen.

| Tool output label | Maps to | Note |
|---|---|---|
| `deepchecks` `Index Leakage` | **T1** | |
| `deepchecks` `New Label`, `Datasets Size Comparison` | **T1** | split-integrity family |
| `deepchecks` `Train Test Samples Mix` | **T4** | cross-split row mix |
| `deepchecks` `Date Train Test Leakage Duplicates` | **T4** | |
| `deepchecks` `Data Duplicates` | **unmapped** | within-dataset duplication, not across-split → scores nothing on C4 |
| `deepchecks` `Date Train Test Leakage Overlap` | **T6** | dataset-level, not per-cell; the generous mapping of §2.3 |
| `deepchecks` `Feature Label Correlation`, `Identifier Label Correlation` | **T5** | heuristic PPS/correlation screens |
| `deepchecks` `Multivariate Drift`, `Feature Drift`, `Label Drift` | **T8** | **contested** — drift is not sampling bias; mapped anyway, and the mapping is flagged in the published result |
| `deepchecks` `Feature Label Correlation Change` | **unmapped** | train-vs-test PPS drift; neither T5 nor T8 cleanly |
| `leak-detect` vertical (`detect_vertical_leakage*`) | **T6** | row-position cut, the direct v7-defect test |
| `leak-detect` horizontal (`detect_horizontal_leakage*`) | **T5** | target→feature sentinel injection |
| Yang / `LeakageDetector` `preprocessing` | **T2** | |
| Yang / `LeakageDetector` `overlap` | **T4** | **decision:** overlap maps to duplicates, not to T1; T1 is a declared-split-integrity rule |
| Yang / `LeakageDetector` `multi-test` | **unmapped** | repeated test-set use; §4.1 line 335 explicitly places "reused for model selection" *outside* L1.1 as a REVIEW info-sheet item |
| OMDS `ax:fit_on_train_only`, runtime `LeakageViolation` | **T2** | |
| `leakfence` split-integrity error (SHA256 fingerprint) | **T1** | |
| `leakfence` subject/session group overlap | **T7** | |
| `leakfence` temporal window overlap | **T4** | near-duplicate windows across the split — non-independence by construction, mapped to duplicates not T6 |
| `leakfence` preprocessing lint | **T2** | |
| `temporalcv` `gate_signal_verification`, `gate_suspicious_improvement` | **T6** | heuristic; the tool's own HALT text reads "Signal detected — investigate (legitimate temporal pattern or leakage?)", i.e. it does not separate the two |
| `leakage-buster` target leakage (\|corr\| ≥ 0.98) | **T5** | |
| `leakage-buster` time leakage | **T6** | split-granular |
| `leakage-buster` group leakage | **T7** | |
| `leakage-buster` CV-strategy mismatch | **T1** | |

**Three unmapped labels are recorded deliberately.** An unmapped label scores nothing — it is
neither a hit nor a miss — and publishing the unmapped list is what stops a later reader from
reconstructing a more flattering mapping.

### 2.6 Scoring rules

Direct from §9.2 items 4, 5, 7, plus the one thing they do not cover.

1. **Ineligible × case → abstention, never a miss** (item 4). An abstention is published as an
   abstention and never rolled into a denominator that reads as failure.
2. **Crash → abstention, and the crash count is published** (item 5). Crashes are reported per
   tool × case with the error, not aggregated away.
3. **No case is excluded after results are seen** (item 7). The eight cases of §2.2 are the set.
   If a case turns out to be badly constructed, that fact is *published alongside its result*, and
   the case is not removed.
4. **Manual setup is allowed and is recorded** (item 6) — including the `leak-detect` NumPy pin,
   Docker for the static analyzers, and any hand-built adapter between a case and a tool's input
   form. An adapter that changes what a case tests is a **case modification** and is forbidden by
   item 7; an adapter that only reshapes the same content is setup. The distinction is recorded
   per adapter.

> **Gap between §9.2 and §10.1, reported not patched.** §10.1 criterion 1 asks whether a tool
> "covers at least the same published types **at the same tier or better**". §9.2's seven items
> define eligibility, versions, mapping, abstention, crash, setup, and exclusion — **but no tier
> axis**. Deciding criterion 1 from a §9.2 comparison therefore requires assigning each hit a tier
> under §3's definitions, which §9.2 does not instruct the comparison to record.
> **Recommendation:** record per hit the tier this project's §3 would license for the evidence the
> tool actually produced (RULE / PROVEN / REVIEW), as a separate column.
> **Author decision required:** whether that recording is an implementation detail permitted under
> §9.2, or a new scoring rule that belongs in `PREREG.md` under the amendment path. It is not
> decided here, and this gap does not change the gate verdict — criterion 1 fails on coverage for
> every candidate before tier is reached.

---

## Part (ii) — DESK-VERIFIED TOOL FACTS

Facts below are from primary sources (PyPI JSON, GitHub API, CRAN, project docs, paper PDFs).
Sources marked **[sweep]** were verified by the assistant prior-art sweep recorded at
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\tasks\wv0bwus8j.output`
(four agents, 104 tool calls, primary-source fetches). Sources marked **[G3]** were verified by
this item on 2026-08-14.

**These are facts about tools, not results of a comparison. No tool has been run.**

| Tool | Version / date | Method | Runtime probe of a user callable? | Per-cell availability model? | Not-run accounting? | Active ≤ 12 mo? |
|---|---|---|---|---|---|---|
| `leak-detect` | 0.0.1, 2020-07-22 (sole release) | row-position cut, NaN/complex sentinel, diff output columns | **yes** | **no** — `check_row_number = int(len(input_data)/2)`, positional only | no — "prints out" leaked columns | **no** [sweep] |
| `deepchecks` | 0.19.1, 2024-12-15; `main` commit 2025-11-24 | data/split inspection on `Dataset`s + a fitted model | **no** — requires a fitted sklearn-API model or precomputed predictions | **no** — single `datetime_name` column | **yes** — `SuiteResult.get_not_ran_checks()`, `CheckFailure`, `passed(fail_if_check_not_run)` | by commit yes, by release no [sweep] |
| `leakage-buster` | 1.0.2, 2025-09-13 | dataframe + target + CV strategy audit; ~6 of 8 families | **no** — no user-callable parameter | **no** — time check split-granular | not recorded | yes [G3] |
| `Leakly` | 0.1.2, 2026-05-14 | permutation tests over ML pipelines | not established | **no** | not established | yes [G3] |
| `leakage-analysis` (Yang et al., ASE 2022) | pushed 2023-05-02 | static datalog dataflow; 3 types | **no** — reads source | **no** | no (corpus-level: 6/100 notebooks failed) | **no** [sweep] |
| `LeakageDetector` 2.0 (VS Code) | v1.1.4; repo pushed 2025-05-07 | wraps Yang's static engine; adds LLM fix suggestions | **no** | **no** | no | **no** [sweep] |
| NBLyzer / abstract interpretation | pushed 2023-05-23; **archived** 2026-06-15 | abstract interpretation; taint + overlap | **no** | **no** | no (corpus-level: 302/2413 excluded) | **no** [sweep] |
| OMDS / `oh-my-datascience` | active through 2026-07-31; **not on PyPI** | AST rules + runtime sklearn `fit()` taint guard | **partial** — wraps estimator `fit()`, does not probe a feature callable | **no** | only an "unreadable" files key | yes [sweep] |
| `temporalcv` | 2.3.0, 2026-06-14 | time-series CV with gap enforcement + 2 statistical gates | **no** — gates take a fitted model + X/y | **no** | no | yes [sweep] |
| `leakfence` | updated 2026-08 | numpy split-index audit; SHA256 fingerprints, group/window overlap, preprocessing lint | **no** — "purely array/metadata inspection" | **no** | no | yes [sweep] |
| `leakr` | 0.1.0, CRAN 2025-10-26 | R; duplication, target-correlation, train/test contamination | **no** | **no** | schema present, non-functional (`detectors_run: NULL` in the vignette) | yes [sweep] |
| `bioLeak` | **0.3.8, CRAN 2026-05-21** | R; permutation-based statistical diagnostics | **no** | **no** | not established | **yes** [G3] |
| `mlinspect` | pushed 2024-02-24 | runtime instrumentation, provenance/distribution debugging | n/a — different object | **no** | n/a | **no** [G3] |

**The central negative result, restated because it is the load-bearing one.** No tool found — new
or old — probes a user *callable* at runtime against a *declared per-cell availability model*.
The two runtime mechanisms that exist are `leak-detect`'s row-position cut (2020, dormant, subject
to the v7 defect) and OMDS's sklearn `fit()` taint guard (split/preprocessing only, no temporal
dimension). This is the finding H-34 rests on and it is unchanged by this item.

**Two corrections to the record surfaced by this item** (reported, not applied — `HISTORY.md` is
not editable by this run):

- `HISTORY.md` H-34 line 282 records "`bioLeak` (CRAN, Dec 2025)". CRAN today shows **bioLeak
  0.3.8, published 2026-05-21** [G3]. bioLeak is therefore **active within §10.1 criterion 5's
  12-month window**. The verdict is unaffected — it fails criterion 1 (permutation-based
  statistical diagnostics, no per-cell availability) — but the parenthetical is stale and the
  criterion-5 status flips.
- H-34's provenance clauses about the two sweeps do not match the sweep evidence on file. Detail
  in §5 below.

---

## Part (iii) — WHAT REQUIRES EXECUTION

**Genuinely unrun. Nothing below can be produced from documents.**

| # | §9.2 clause | What must be executed | Blocked on |
|---|---|---|---|
| E1 | line 973, "runs on the acceptance fixture" | every rostered tool against `fixture_contaminated` and `fixture_corrected` | **the reconstructed declaration being signed off** (line 448 ordering; `AVAILABILITY_DECLARATION.md` is header-marked DRAFT) |
| E2 | line 973, "plus a … comparison set" | every rostered tool × each of C1–C8 and its clean control | C1–C8 being **written** (specified here, not implemented) and the protocol being **committed** |
| E3 | item 2, line 976 | installed version strings, install commands, full configuration per run | E1/E2 |
| E4 | item 5, line 979 | crash counts per tool × case, with errors | E1/E2 |
| E5 | item 6, line 980 | the manual-setup record — NumPy pin for `leak-detect`, Docker for the static analyzers, every adapter | E1/E2 |
| E6 | §10.1 criterion 3 (line 1022) | fires-on-contaminated / silent-on-corrected, per tool | E1 |
| E7 | the published comparison table itself | hit / miss / abstention / crash per tool × case, at tier | E1–E6 |

**Estimated shape of the work, for planning only and not a locked figure:** 9 rostered tools ×
8 cases × 2 sides = 144 case-runs on the comparison surface, plus 9 tools × 2 fixture sides = 18
on the fixture surface, plus per-tool installation and adapter work. `PREREG.md` line 991 budgets
1–2 weekends for **all four** Phase 0 deliverables.

**One constraint on how E1–E7 may be discharged.** Executing third-party tools means installing
and running third-party code. That is a state-changing operation on the machine and on the
environment, and it is not within the read-only scope of this pass. It is author work, or work
under an explicitly authorized run.

---

## 5. Discrepancies in the existing record, reported for author decision

Reported because `HISTORY.md` H-34 is the sign-off for a Phase 0 deliverable and is **still
uncommitted** (verified: `git show HEAD:HISTORY.md` contains no `H-34`; it is part of the
+33-line uncommitted working-tree diff). Correcting it is cheap now and expensive after the
ceremony. **No file has been edited by this item.**

1. **Sweep date.** H-34 line 271 states the author's search and "the assistant-conducted sweep of
   **the same date**" (12 August 2026). The sweep evidence on file is self-dated **2026-08-08 /
   2026-08-09** — its agent prompts read "Today is 2026-08-08" and its synthesis reads "as of
   2026-08-09". If these are the same sweep, H-34's date is wrong by three to four days.
2. **"Phase 0's sweep did not surface `leakr`, `bioLeak`, `LeakageDetector` 2.0 or `Leakly`"**
   (H-34 line 291). The sweep on file **did** surface `leakr` (with CRAN vignette detail,
   including the `detectors_run: NULL` observation) and `LeakageDetector` 2.0 (extensively, by two
   of the four agents). Further, `PREREG.md` §1.1 line 152 itself names "LeakageDetector 2.0 for
   VS Code (2025)". Either "Phase 0's sweep" denotes a different and earlier pass than the one on
   file — in which case which pass should be named — or the sentence is wrong.
3. **"covered Google Scholar and CRAN"** (H-34 line 291). CRAN, yes (`leakr`). Google Scholar does
   not appear in the sweep's own recorded search log, which lists eight WebSearch queries plus
   primary fetches to PyPI, CRAN, GitHub, arXiv and HAL.
4. **`bioLeak` date and criterion-5 status** — see Part (ii).

**What is *not* in question:** the `PRIOR_ART_VERIFICATION.md` hash cited in H-34 line 271,
`b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`, **verifies** against the file
as it stands [G3]. And none of items 1–4 changes H-34's judgment: no candidate probes a user
callable against a declared per-cell availability model, so §10.1 does not fire.

---

## 6. Author decisions this file records rather than makes

1. Eight cases (one per published type) vs eleven (one per detector row) — §2.2.
2. Whether line 448's "after its declaration is reconstructed" gates the hand-written comparison
   set as well as the fixture surface — §2.1.
3. Whether `leakr` and `bioLeak` (R) enter the roster, and whether the cases port to R data frames
   without changing what they test — §2.3.
4. Whether `train-test-leakage-detector` enters the roster — §2.3.
5. Whether the tier column of §2.6 is an implementation detail under §9.2 or a new scoring rule
   needing the amendment path — §2.6.
6. Whether ex-ante *tool* exclusion is implied by item 1 or is an addition — §2.3.
7. Whether to correct H-34 before the ceremony — §5.
