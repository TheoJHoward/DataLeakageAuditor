# J6_SCOPED_PLAN.md — scoping and costing the §9.2 cross-tool comparison

**Status: DRAFT, UNCOMMITTED, AND NOT A RUN.** Item J6 of the kill-gate completion pass,
2026-08-14. **Nothing was installed and nothing was executed by this item.** No file outside this
directory was written. `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md`
are byte-unchanged. This is a plan for work that has not been authorized.

**Input.** G3 established that §9.2 requires executing third-party tools and cannot be
desk-completed; its protocol half — case set C1–C8, 9-tool roster, eligibility matrix, label
mapping, scoring rules — is at `killgate\CROSS_TOOL_COMPARISON.md`. This file does not restate
that protocol. It answers a different question: **what would it actually take to run it, and what
does the acceptance fixture's real shape do to that answer.**

**Headline, stated first because it reorganizes everything below.** The acceptance fixture is a
stored per-second **prediction** pair. It carries no feature columns, no split declaration, no
pipeline callable, and no source code. **It presents an input surface that essentially no leakage
tool accepts.** Section 0 shows this is not an inconvenience to engineer around but a structural
property with a provable consequence for §10.1 criterion 3, and it is the single largest lever on
the cost estimate in Part (e).

---

## 0. The fixture surface — the fact that governs Parts (a), (d), (e) and (f)

### 0.1 What the fixture is, from the registered record

`AVAILABILITY_DECLARATION.md` §0.2, lines 637–641:

> **637** **What it is.** The stored per-row predictions —
> **638** `results\phase7\l2_predictions\` (pre-fix) against `results\phase7_fixed\l2_predictions\`
> **639** (post-fix), **64 parquets each**, same 64 filenames, 8 instruments x 2 architectures x 4
> **640** horizons. Column universe: the **35-column, MBO-FREE** `ALL_L2_FEATURES` set under working
> **641** resolution R3. Full identity, class and provenance: §8.

And lines 646–651, the decisive passage:

> **646** **The structural fact that forces the split.** Artifact B stores **no feature columns**. Its
> **647** parquets carry `pred_score`, `true_label`, `fwd_move_ticks`, `mid_price_t` (schema read in §8;
> **648** Y1 §1.3 item 4 additionally lists `timestamp` from the writer at `phase7_l2_sim.py` L402-408) —
> **649** and nothing else on either enumeration. **No event-to-row timing question can be answered from
> **650** Artifact B at all.** That is not a convenience; it is why the ground truth must be measured on
> **651** Artifact A and then applied to Artifact B.

Two further facts bear directly on runnability:

- **The fixture's own generators are gone.** `AVAILABILITY_DECLARATION.md` lines 656–658: "**That
  bridge rests on R3 plus §B.2's generation identification — not on a generator script**, because
  both of Artifact B's generators are absent from the archive (§0.4)." **Every source-reading tool
  is therefore ineligible on the fixture surface by absence of the object it audits.**
- **Artifact A is not a substitute.** `AVAILABILITY_DECLARATION.md` §0.1, lines 631–633: "**What it
  is NOT.** It is **not** the gate's fixture. It carries no stored predictions, no AUC the gate
  consumes, and no label vector the gate scores. Nothing in §6.2's four criteria is evaluated on
  it." And the reading rule at lines 678–681: "**Reading rule, binding on this file and on any gate
  report.** A measurement made on Artifact A may be quoted as ground truth for Artifact B **only**
  through the lattice bridge above, and must name the artifact it was measured on. **A measurement
  claim that names neither artifact is not auditable and may not be published**".

### 0.2 The consequence, derivable at the desk: criterion 3 on the fixture surface

`AVAILABILITY_DECLARATION.md` §9, lines 1664–1668:

> **1664** All 64 main-set pairs are bit-exact identical on `true_label`, `fwd_move_ticks`, AND
> **1665** `mid_price_t` (raw-bytes comparison after dtype/length checks): one shared label vector per
> **1666** pair. This is the licence for reading the pre/post AUC delta as a feature-availability-only
> **1667** effect — labels, label bases, and evaluation populations are identical across sides, so
> **1668** nothing but feature availability differs.

**Therefore: of the four columns the fixture carries, exactly one — `pred_score` — differs between
`fixture_contaminated` and `fixture_corrected`.** It follows immediately that

> **any tool whose output is a function of the fixture's stored columns and which does not read
> `pred_score` produces byte-identical output on both sides, and cannot satisfy §10.1 criterion 3's
> "Fires on `fixture_contaminated` and is silent on `fixture_corrected`" (`PREREG.md` line 1022).**

This is a derivation, not a prediction. It is why the fixture-surface run is near-zero information
for every rostered tool, and it is what makes the abstention route of Part (f) defensible rather
than lazy.

### 0.3 The one crack in that derivation — and a pre-run protocol fix it forces

A tool *could* read `pred_score` as though it were a feature. `pred_score` against `true_label` is
AUC 0.957 on the contaminated side and 0.675 on the corrected side (`PREREG.md` line 445:
"**Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**"). A
correlation/predictive-power screen pointed at `pred_score`-as-feature therefore **does** differ
across sides, and if its threshold happens to fall between those two values the tool technically
"fires on contaminated, is silent on corrected" — satisfying criterion 3 while detecting nothing
about leakage whatsoever. It would merely be re-reading the AUC gap the fixture was built to have.

`CROSS_TOOL_COMPARISON.md` §2.5 currently maps `deepchecks` `Feature Label Correlation`,
`Identifier Label Correlation` → **T5**. Under that mapping and this crack, deepchecks would be
recorded as scoring a **T5 hit on the fixture** — a false hit, produced by the fixture's design
rather than by deepchecks.

**Recommendation, and it is time-critical.** §9.2 item 3 (`PREREG.md` line 977) requires the label
mapping be "**written down before running**". Add a row to §2.5 **now**, before any run:

> `pred_score` is a **model output**, not a feature. Any tool finding whose subject column is
> `pred_score` is **unmapped** and scores nothing — neither hit nor miss — on either fixture side.

Adding it after a run is forbidden by the same item. Adding it now costs minutes.
**Author decision:** whether this is an implementation of item 3 or an addition to it.

---

## Part (a) — Which candidates are PROGRAMMATICALLY RUNNABLE, and against what

"Programmatically runnable" here means: **a Python API or CLI that can be pointed at data or at a
pipeline, driven from a script, without a human in an IDE.** Two surfaces must be judged
separately, because §9.2 line 973 names two and they are not interchangeable.

### (a.1) Summary — runnable at all

| Tool | Install route | Entry point | Programmatically runnable? |
|---|---|---|---|
| `leak-detect` 0.0.1 | `pip install leak-detect` (PyPI, MIT) | Python API: functions in `leak_detect/base.py` taking `input_data` (DataFrame), a **user callable** `data_creation_func`, input feature cols, output cols | **YES**, with a NumPy pin — see (c) |
| `deepchecks` 0.19.1 | `pip install deepchecks` (PyPI, AGPL-3.0) | Python API: `Dataset(train)`, `Dataset(test)`, suites/checks; fitted sklearn-API model or precomputed predictions | **YES** |
| `leakage-buster` 1.0.2 | `pip install leakage-buster` (PyPI, MIT) | Python API: dataframe + target + CV strategy | **YES** |
| `Leakly` 0.1.2 | `pip install Leakly` (PyPI, MIT) | Permutation tests over ML pipelines — **API not established from documentation** | **PROBABLY**, unverified |
| `temporalcv` 2.3.0 | `pip install temporalcv` (PyPI, MIT) | `gate_signal_verification`, `gate_suspicious_improvement` — take a **fitted model + X/y** | **YES** |
| `leakfence` | `pip install leakfence` (PyPI, MIT) | Python API over **numpy train/test index arrays** + metadata | **YES** |
| OMDS / `oh-my-datascience` | `uv` from GitHub (**not on PyPI**), Apache-2.0 | AST rules over **source files**, plus a runtime guard wrapping sklearn `fit()` | **YES**, install risk high |
| `leakage-analysis` (Yang et al.) | GitHub repo build (MIT), Souffle datalog engine, Docker path documented | Static analysis over a **Python source file** | **YES, headless** — see (c) |
| `LeakageDetector` 2.0 | VS Code Marketplace (MIT) + Node.js + native binaries or Docker | **IDE extension — no documented headless entry point** | **NO** — Part (b) |

### (a.2) The fixture surface, tool by tool — what "running it against the fixture" would concretely mean

The fixture presents: `pred_score`, `true_label`, `fwd_move_ticks`, `mid_price_t` (+ `timestamp`),
64 parquets per side, **no features, no split, no callable, no source**.

| Tool | What its entry point requires | What the fixture presents | Verdict |
|---|---|---|---|
| `leak-detect` | a **`data_creation_func` callable** that rebuilds features from raw rows, plus the input feature columns it perturbs | **no callable and no feature columns exist**. Artifact B's generators are absent from the archive (`AVAILABILITY_DECLARATION.md` lines 656–658) | **Not runnable. Declared INELIGIBLE from documentation (item 1) → abstention (item 4).** Nothing to perturb and nothing to re-run |
| `deepchecks` | two `Dataset`s carrying features + label; a fitted model or precomputed predictions | precomputed predictions **do** exist (`pred_score`); features do not; **no train/test split is declared anywhere in the fixture** | **Runnable only by inventing a split and by declaring `fwd_move_ticks`/`mid_price_t`/`pred_score` to be "features".** Both are fabrications. `fwd_move_ticks` is a **label base** — `true_label` is essentially its sign — so a feature-label screen would fire on both sides identically (§0.2). **Recommend: INELIGIBLE, abstention** |
| `leakage-buster` | dataframe + target + **CV strategy** | target yes; no features; **no CV strategy is declared** | **Not runnable as designed → INELIGIBLE, abstention** |
| `Leakly` | an ML pipeline to permute | no pipeline | **INELIGIBLE, abstention** |
| `temporalcv` | a **fitted model** + X/y | no model, no X | **INELIGIBLE, abstention** |
| `leakfence` | **numpy train/test index arrays** | no split indices exist for the fixture | **INELIGIBLE, abstention** |
| OMDS | source files (AST) + a live sklearn `fit()` call | **no source** (generators absent); no training run to guard | **INELIGIBLE, abstention** |
| `leakage-analysis` | a Python source file | **no source** (generators absent) | **INELIGIBLE, abstention** |

**This is the finding of Part (a) and it should not be softened: on the acceptance-fixture surface,
all nine rostered tools are ineligible, and every one of them is ineligible *from documentation* —
which is exactly the basis §9.2 item 1 specifies** ("**Eligibility** per tool × case, declared
before any run, **from documentation**", `PREREG.md` line 975). Under item 4 ("**Ineligible cases
score as abstentions, not misses.**", line 978) that yields a complete, §9.2-compliant fixture
result **without executing anything**: nine declared abstentions, with reasons.

**My reading, offered for the author to accept or reject:** a documented ineligibility is a §9.2
result, so the fixture surface can be discharged by declaration rather than by execution — and
§0.2's derivation independently shows criterion 3 is unreachable there for any tool that does not
read `pred_score`. **This is an author call**, because the plain reading of line 973 ("Phase 0
**runs** on the acceptance fixture") is that something is executed. The honest phrasing in the
published result would be: *"Fixture surface: 9/9 tools ineligible, declared from documentation
before any run; no tool accepts a stored-prediction pair as input. §10.1 criterion 3 is
consequently unevaluable on this surface, and the reason is recorded rather than left blank."*

**The Artifact A temptation, named so it is not taken silently.** Artifact A (the f2 rebuild pair)
*does* carry features (45-column `FULL_FEATURES`) and *does* have a byte-verified builder source
(`f2\phase5_ml_fixture.py`). Every tool ineligible above becomes eligible if pointed at Artifact A.
**Do not report that as a fixture run.** `AVAILABILITY_DECLARATION.md` lines 631–633 says Artifact
A "is **not** the gate's fixture", and the reading rule at lines 678–681 requires any measurement to
name the artifact it was made on. An Artifact A run is a legitimate *supplementary* result, clearly
labelled, and it is the only way any tool can be confronted with this project's actual data. It is
**not** §9.2's fixture surface and it is **not** §10.1 criterion 3. **Author call** whether to run
it at all; note it also means executing archive-lineage feature-build code, which is a
state-changing operation outside any read-only pass.

### (a.3) The comparison surface (C1–C8) — where the tools actually run

C1–C8 are hand-written, so we control the surface and can hand each tool the shape it wants. **This
is where the entire comparison actually lives.** Counted from `CROSS_TOOL_COMPARISON.md` §2.3's
matrix, **29 of 72** tool × case cells are eligible across the 9-tool roster (leak-detect 2,
deepchecks 5, leakage-buster 4, Leakly 2, leakage-analysis 4, LeakageDetector 2.0 4, OMDS 2,
temporalcv 2, leakfence 4); the remaining 43 are declared abstentions under item 4.

Three adapter costs are non-obvious and drive Part (e):

1. **`leak-detect` needs a `data_creation_func` per case.** Its input surface *is* a callable. Each
   case must therefore be written as a feature-building function, not just as a frame. That is a
   different authoring job from C2/C3's pipeline objects and from C1/C4's index sets.
2. **`temporalcv`'s gates need a fitted model per case.** A model must be trained on each case's
   contaminated and clean sides before the gates can be called at all.
3. **`leakage-analysis` and OMDS need each case as a standalone `.py` script** that they can read
   statically. The same case therefore exists in three forms — frame, callable, script — and
   §9.2 item 7 makes the boundary matter: `CROSS_TOOL_COMPARISON.md` §2.6 item 4 already fixes it
   ("An adapter that changes what a case tests is a **case modification** and is forbidden by
   item 7; an adapter that only reshapes the same content is setup"). **Every adapter needs that
   judgment recorded at the time it is written, not afterwards.**

---

## Part (b) — Tools that are not programmatically runnable, and what §9.2 says about them

### (b.1) The three groups

| Group | Members | Why not programmatically runnable |
|---|---|---|
| **IDE plugins** | `LeakageDetector` 2.0 (VS Code, MIT, v1.1.4); `LeakageDetector` 1.0 (PyCharm — already excluded on licence and distribution grounds, `CROSS_TOOL_COMPARISON.md` §2.3) | Distributed as a VS Code extension; requires Node.js plus pre-built native binaries or Docker. **No documented CLI or Python API.** Driving it means driving an editor UI |
| **R-only** | `leakr` 0.1.0 (CRAN, MIT, 2025-10-26); `bioLeak` 0.3.8 (CRAN, MIT + file LICENSE, 2026-05-21) | Runnable, but only from R. `leakr_audit()` takes R data frames. Requires an R toolchain and a port of all eight cases |
| **Archived / no interface** | NBLyzer (archived read-only 2026-06-15, template README) | Already excluded, `CROSS_TOOL_COMPARISON.md` §2.3 |

### (b.2) Does §9.2 scope them IN or OUT? — the text, quoted in full

`PREREG.md` lines 973–981, complete:

> **973** Phase 0 runs on the acceptance fixture — **after its declaration is reconstructed** (§6.2) — plus a separately enumerated prior-art comparison set of hand-written cases, one per leakage type, committed with this protocol before any tool is run.
>
> **975** 1. **Eligibility** per tool × case, declared before any run, from documentation.
> **976** 2. **Versions** and configuration recorded.
> **977** 3. **Label mapping** written down before running.
> **978** 4. **Ineligible cases score as abstentions, not misses.**
> **979** 5. **Crashes score as abstentions**, counts published.
> **980** 6. **Manual setup allowed** and recorded.
> **981** 7. **No case excluded after results are seen.**

**§9.2 does not say.** No clause mentions a language, an interface form, an IDE, a CLI, or
programmatic runnability. It does not define "tool". It scopes neither group in nor out.
**Flagged as an author call, not decided here.**

Three pieces of adjacent registered text bear on it, and none of them settles it:

1. **Item 6, line 980 — "Manual setup allowed and recorded" — cuts toward IN.** An R toolchain and
   a Docker prerequisite are ordinary manual setup. Item 6 is the closest §9.2 comes to
   anticipating awkward install paths, and it permits them rather than excusing them.
2. **§10.1 criterion 4, line 1023 — "Installs and runs through a documented public interface without
   author modification" — is a *gate* criterion, not a roster rule.** It governs whether a tool can
   trigger the stop; it says nothing about who enters the §9.2 comparison. Reading it as a roster
   filter would import a kill-gate criterion into a deliverable that §9.2 defines independently.
   Worth noting `LeakageDetector` 2.0 arguably *passes* criterion 4 — VS Code Marketplace is a
   documented public interface — while still being unrunnable from a script. **The two questions
   come apart.**
3. **§1.1 line 152 names them as prior art**: "Its descendants — LeakageDetector for PyCharm (2025),
   LeakageDetector 2.0 for VS Code (2025) — improved usability, cover the same three types, and did
   not independently measure detection accuracy." Being named in §1.1 is not being rostered in §9.2,
   but excluding from the comparison a tool the registration itself names as prior art is a visible
   asymmetry a reader may notice.

### (b.3) A routing option for the plugin family, offered rather than decided

`LeakageDetector` 2.0 **wraps Yang et al.'s static engine**, and its own authors state they did not
evaluate detection accuracy separately (arXiv 2509.15971: "we did not assess the detection accuracy
of the tool separately"). That engine — `leakage-analysis`, MIT — **is** headlessly runnable.

**Option:** run the engine, and record `LeakageDetector` 2.0 as *ineligible by interface (no
headless entry point), with its detection substance represented by `leakage-analysis`, and say so in
the published table.* This costs one install instead of three, represents the static branch
honestly, and does not pretend a UI was driven. **It is still an author call**, because "the tool"
in §9.2 is undefined and someone could reasonably insist the plugin is a distinct tool.

**For the R pair:** `CROSS_TOOL_COMPARISON.md` §2.3 already records the open question — whether the
eight cases port to R data frames without changing what they test. That is not a formality: C2, C3
and C6 are about pipeline construction and availability semantics, and a port that turns them into
plain frames **is a case modification under item 7**, not setup. **Recommendation: if R enters, port
only C1, C4, C5, C7, C8 and declare C2/C3/C6 ineligible-by-port for the R tools, with the reason
published.** Author call.

---

## Part (c) — Environment work per tool

| Tool | Known blockers | What installing costs |
|---|---|---|
| `leak-detect` 0.0.1 | **`np.complex` removed in NumPy 1.24.** Open Issue #1 (2023-01-14, "'numpy' has no attribute 'numpy.complex'") never fixed; last push 2020-07-23. Crash sites `base.py:76` / `base.py:209`. NumPy < 1.24 also forces **Python ≤ 3.11** (no 3.12+ wheels for numpy 1.23.x) | A **second, pinned interpreter and venv**: Python 3.10 or 3.11 + `numpy<1.24` + an era-compatible pandas. Recorded as manual setup under item 6. **Note the crash is probe-specific**: the NaN probe does not call `np.complex`; only the complex probe does. Expect a *partial* run even on modern NumPy — record per probe, not per tool |
| `deepchecks` 0.19.1 | **AGPL-3.0-or-later** (running creates no obligation — `LICENCE_CHECK.md` §2.2 — but the §13.5 wrap decision is live). API expects a **fitted sklearn-API model or precomputed predictions**; 0.19.1 is from 2024-12-15 and will pin against modern pandas/numpy | Its own venv, near-certainly with pandas/numpy pinned back. Largest dependency footprint of the roster. Also the **documentation-drift risk of `CROSS_TOOL_COMPARISON.md` §2.4**: eligibility was declared from `stable` docs, which describe checks under names that replaced earlier ones; the installed 0.19.1 must be re-read against the declaration |
| `leakage-buster` 1.0.2 | Eligibility is `[P]` throughout — assessed from published API surface, not source (`PRIOR_ART_VERIFICATION.md` lines 35–38) | Cheap pip install. The cost is **re-declaring eligibility from the installed version's documentation before running it**, which item 1 requires and which cannot be skipped |
| `Leakly` 0.1.2 | **API not established.** All the evidence on file is a PyPI one-liner and H-34's single characterization; not read at source or interface level | Cheap install, **expensive orientation**. Budget source reading. Highest uncertainty of the pip-installable tools |
| `temporalcv` 2.3.0 | Python ≥ 3.10; gates require a **fitted model + X/y** | Cheap install. Cost is in the adapter: a model must be trained per case per side |
| `leakfence` | Requires **numpy split index arrays**; designed for windowed biosignal pipelines | Cheap install. Cost is expressing each case as index arrays plus metadata |
| OMDS | **Not on PyPI** — three GitHub install routes via `uv`. 0 stars. Apache-2.0 (more borrow paperwork than MIT, though nothing is being borrowed) | Install risk is the cost, not install time. Runtime guard additionally needs a live sklearn `fit()` per case |
| `leakage-analysis` (Yang) | **Research prototype, dormant since 2023-05-02.** Souffle datalog engine; Docker path documented (the LeakageDetector family's README confirms "Docker must be installed and running") | **The single largest environment item.** Either build Souffle + Python deps from a 3-year-dormant repo, or go through Docker. **Real risk of outright failure** — which under item 5 is itself a recordable result (Part (d)) |
| `LeakageDetector` 2.0 | VS Code + Node.js + native binaries or Docker; **no headless entry point** | Not worth paying if (b.3)'s routing is adopted. If the author insists on running the plugin, budget a full working session and accept that the "run" is a human in an editor, recorded as such |
| `leakr` / `bioLeak` (R) | **Full R toolchain**, plus CRAN installs. `leakr`'s own vignette shows `detectors_run: NULL` — its run-accounting is schema-present but non-functional. `bioLeak` is "MIT + file LICENSE"; that LICENSE file names copyright holders and **has not been read** (`LICENCE_CHECK.md` §2.4) | R + Rtools on Windows, two CRAN installs, and a port of the cases. Two tools share one toolchain, so the marginal cost of the second is small |

**Docker note.** Docker is a prerequisite for the LeakageDetector family and the documented path for
Yang's analyzer. Installing Docker Desktop on this machine is a system-level change and is outside
the read-only scope of every pass so far. **Flag it as an explicit author authorization**, not as an
incidental step.

---

## Part (d) — The crash clause, and whether `leak-detect`'s NumPy breakage is a result or a blocker

### (d.1) The clause, verbatim

`PREREG.md` line 979:

> **979** 5. **Crashes score as abstentions**, counts published.

And immediately adjacent, line 980:

> **980** 6. **Manual setup allowed** and recorded.

### (d.2) The question

`leak-detect`'s complex probe calls `np.complex`, removed in NumPy 1.24. On a modern environment it
raises. Is that a **recorded abstention** (a result §9.2 wants published) or a **blocker to be
engineered around** by pinning `numpy<1.24`?

### (d.3) My reading

**Item 6 governs first; item 5 applies to what crashes after it.**

Items 5 and 6 sit adjacent and are not independent. Item 6 permits manual setup — and a dependency
pin is the most ordinary manual setup there is. It is **not** author modification of the tool: the
tool's own source is untouched, and §10.1 criterion 4's "without author modification" (line 1023)
is not engaged. If item 5 were read to license running a tool in a deliberately hostile environment
and banking the crash, **item 5 would swallow item 6**: any tool could be neutralized by choosing
its environment badly. That reading makes item 6 dead text, so it is the wrong reading.

**Therefore:** run `leak-detect` under a pinned `numpy<1.24` environment, **record the pin as manual
setup under item 6**, and reserve item 5 for whatever crashes *after* documented, non-invasive setup
has been applied.

**Three qualifications that keep this honest:**

1. **The reading that costs this project the most is the correct one here, and that is a reason for
   confidence rather than a reason to hedge.** `leak-detect` is the only in-kind competitor —
   `PREREG.md` line 160 calls availability-based probing "**The one place this project's method
   differs from `leak-detect` in kind rather than degree**", and C6 is built to test exactly that.
   Scoring `leak-detect` as a crash-abstention would let the one tool that could contest the
   flagship claim go untested, on a technicality, in this project's favour. **A protocol that
   conveniently silences the strongest competitor should be distrusted by its own author.**
2. **The environment must still be recorded as what it is.** `CROSS_TOOL_COMPARISON.md` §2.3 already
   requires the pin be "**recorded as manual setup** rather than silently applied". A 2020 tool
   scored in a 2020 environment is a fair comparison only if the published result says so — and
   "requires a pinned pre-1.24 NumPy" is itself informative about maintenance status, which is what
   §10.1 criterion 5 measures.
3. **The crash is probe-specific and must be scored probe-wise.** Only the complex probe touches
   `np.complex`; the NaN probe does not. A per-tool crash verdict would over- or under-report. If
   the complex probe still fails under the pin, *that* is item 5's abstention, counted and
   published; the NaN probe's result stands independently.

### (d.4) The harder case, and where the reading stops

Yang's `leakage-analysis` — a 3-year-dormant research prototype with a datalog engine — may fail to
build at all. There is no dependency pin that fixes "the toolchain no longer assembles". **That is
where item 5 does its real work:** a tool that cannot be made to run through documented setup is a
**crash-abstention, counted and published**, and the failure to build is a fact about the tool's
maintenance state that the published comparison should carry rather than hide. The line between the
two cases is: *does documented, non-invasive setup make it run?* If yes → item 6, run it. If no →
item 5, record the abstention with the error.

**This whole reading is the author's call.** §9.2 does not order items 5 and 6, and a reader could
hold that item 5 is unconditional. Nothing in this file decides it.

---

## Part (e) — Time estimate

**Basis and honesty statement.** These are focused-hours estimates by an author already fluent in
the case material. They exclude author review time, exclude the ceremony, and assume no
interruption. **The dominant variance is environmental, not intellectual:** Yang's Souffle build,
Leakly's undocumented API, and OMDS's non-PyPI install are the three items that could each triple
their own line. Ranges are honest ranges, not padding.

### (e.1) Prerequisite work, surface-independent

| # | Item | Hours |
|---|---|---|
| P1 | **Implement C1–C8 plus their eight clean controls** — 16 artifacts with ground truth and a manifest. C2/C3 need pipeline objects; C6 needs an availability model and a trailing-window feature; C7 needs group IDs; C8 needs a shifted subpopulation. Currently **specified, not implemented** (`CROSS_TOOL_COMPARISON.md` §2.2) | **6–12** |
| P2 | **Harness** — drives tool × case, captures stdout, exceptions, tracebacks, installed version strings, config; writes one record per cell | **4–8** |
| P3 | **Pre-run protocol fixes** — the `pred_score` mapping row of §0.3, the tier column, roster decisions, adapter/case-modification judgments recorded per adapter | **1–3** |
| | **Subtotal** | **11–23** |

### (e.2) Per tool

| Tool | Env setup | Adapter | Execution | Tool total |
|---|---|---|---|---|
| `leak-detect` | 2–5 | 2–4 | 0.5–1 | **4.5–10** |
| `deepchecks` | 1–3 | 2–4 | 0.5–1 | **3.5–8** |
| `leakage-buster` | 0.5–1.5 | 1–2 | 0.25–0.5 | **1.75–4** |
| `Leakly` | 1–3 | 2–5 | 0.5–1 | **3.5–9** |
| `temporalcv` | 0.5–1.5 | 2–4 | 0.5–1 | **3–6.5** |
| `leakfence` | 0.5–1.5 | 1–3 | 0.25–0.5 | **1.75–5** |
| OMDS | 1–4 | 2–5 | 0.5–1 | **3.5–10** |
| `leakage-analysis` (Yang) | **3–10** | 2–4 | 0.5–2 | **5.5–16** |
| `LeakageDetector` 2.0 | 2–6 | n/a (no headless entry) | manual | **2–6, and not recommended** |
| | **Nine-tool Python subtotal** (excluding LeakageDetector 2.0) | | | **26.5–68.5** |
| `leakr` + `bioLeak` (R), if included | 2.5–6.5 shared | 4–8 | 1–2 | **+7.5–16.5** |

### (e.3) Adjudication and publication

| # | Item | Hours |
|---|---|---|
| A1 | **Per-cell adjudication** — hit / miss / abstention / crash, plus the recommended tier column, over 29 eligible cells × 2 sides plus all 43 abstentions' recorded reasons | **8–16** |
| A2 | **Fixture-surface record** — nine documented ineligibility declarations, the §0.2 criterion-3 derivation, and the criterion-3 status statement | **2–4** |
| A3 | **Write-up** — the published comparison table, the crash/abstention register, the unmapped-label register, the manual-setup record | **6–12** |
| | **Subtotal** | **16–32** |

### (e.4) Totals

| Scope | Hours | Note |
|---|---|---|
| **Full run, 9 Python tools, both surfaces** | **53.5 – 123.5** | central ≈ **85 h** |
| **+ the R pair** | **61 – 140** | |
| **+ driving `LeakageDetector` 2.0 by hand** | **63 – 146** | not recommended |
| **Minimum viable run (Part f)** | **34 – 76** | central ≈ **52 h** |
| **Two-tool floor (`leak-detect` + `deepchecks`)** | **23 – 51** | central ≈ **35 h** |

**Against the registered budget.** `PREREG.md` line 991 allots "**1–2 wknds**" to **all four** Phase
0 deliverables — call that 12–32 focused hours in total. **§9.2 alone, run fully, is roughly 2–6×
the entire Phase 0 budget.** Even the two-tool floor consumes most of it, and two of the four
deliverables (the declaration ceremony, the outbound licence decision) are still open.

**Against the calendar.** `PREREG.md` line 987: "Hard constraints: **Concept A pre-registration —
September. UChicago — 1 November.** Neither moves." Today is 2026-08-14. §10.2 criterion 4, line
1041 — "4. **Any phase competing with September or 1 November** → pause." — is live, and an
85-hour item starting mid-August is exactly the shape of thing it was written for.

**What this estimate does not cover:** author review of the protocol before the run; the
`prereg-v30a` ceremony; sign-off of `AVAILABILITY_DECLARATION.md`, which registered ordering
(`PREREG.md` line 448) places **before** the fixture-surface work; and any Docker authorization.

---

## Part (f) — Recommended minimum viable run

**Shape: four tools × eight cases × two sides on the comparison surface, plus a declared-ineligible
fixture-surface record. 34–76 hours, central ≈ 52.**

### (f.1) The roster, and why each is in

| # | Tool | Why this one |
|---|---|---|
| 1 | **`leak-detect`**, under a pinned `numpy<1.24` environment | **Mandatory. If exactly one tool is run, it is this one.** It is the only in-kind runtime-callable prober, and `PREREG.md` line 160 stakes the intended contribution on the contrast with it. C6 is built to test precisely the v7 defect of line 156 ("it cuts on row position, so it cannot see current-bar inclusion and it false-flags a legitimately lagged label"). **Without this tool there is no comparison — there is only an assertion** |
| 2 | **`deepchecks`** | The mature data/split baseline named at `PREREG.md` line 154 ("Mature, maintained, widely installed"), and the broadest eligibility on the roster (5 of 8 cases — C1, C4, C5, C6, C8). The run doubles as evidence for the live §13.5 wrap decision |
| 3 | **`leakage-analysis`** (Yang) | Represents the entire static-analysis branch that `PREREG.md` line 152 names, **and** — per (b.3) — is the engine inside both LeakageDetector versions. One install covers the branch. It is also the roster's biggest env risk, so if it fails to build, that failure is itself an item-5 result worth having |
| 4 | **`leakfence`** | One genuinely 2026 tool, so the comparison cannot be dismissed as being against 2020–2024 software. Broadest cheap eligibility (T1/T2/T4/T7) and a low install cost. **Substitute `temporalcv`** if contesting T6 matters more than breadth — it is the only other T6-eligible candidate |

**Excluded from the MVR** (not from the roster — they remain declared, unrun): `leakage-buster`,
`Leakly`, OMDS, `temporalcv`, `LeakageDetector` 2.0, and the R pair. **Their exclusion must be
declared and reasoned before the run**, exactly as `CROSS_TOOL_COMPARISON.md` §2.3 declares its
exclusions — otherwise a partial roster reads as a chosen roster.

### (f.2) What the MVR would establish

- **§9.2 items 2, 4, 5, 6 discharged with real artifacts** for the tools run: installed version
  strings, configuration, abstention reasons, crash counts with errors, and the manual-setup record
  including the NumPy pin.
- **The one load-bearing comparative claim measured rather than asserted.** C6 against
  `leak-detect` converts `PREREG.md` line 160's in-kind-difference claim from a source reading into
  an executed result. This is the single highest-value cell in the entire 162-cell matrix.
- **A published false-alarm record** from the eight clean controls — the only thing that makes a
  hit interpretable.
- **All three tool families represented** — runtime perturbation, data/split checking, static
  analysis — so the comparison is not a strawman.
- **Enough to retire `PREREG.md` line 165's standing disclaimer** ("**Comparative completeness is
  not claimed here.** Whether this is more complete than existing tooling is what Phase 0 (§10.1)
  tests") *for the four tools run, and only for them.*

### (f.3) What it would NOT establish — stated plainly

- **Nothing about the five unrun tools**, including §10.1 criterion 3 for them. Under §10.1's
  conjunctive structure an unevaluated criterion cannot make the gate fire, so **the verdict stays
  safe and the record stays partial** — and the published result must say which tools were run and
  which were declared-but-unrun.
- **Nothing about the fixture surface by execution**, if §0.2's derivation and (a.2)'s abstention
  route are adopted. That route is defensible and I recommend it, **but it is an author call** and
  the published wording must not imply a fixture run happened.
- **Nothing about L1.4b, L2b, or L3.1b.** `CROSS_TOOL_COMPARISON.md` §2.2 already records this: the
  eight-case reading instantiates only one sub-row each of T4, T5, T6. The MVR does not worsen this
  and does not fix it.
- **No completeness claim of any kind.** Four of nine tools, eight of eleven detector rows, one of
  two surfaces. Every one of those fractions belongs in the published table's caption.

### (f.4) Sequencing, if the MVR is taken

1. **Author sign-off of `AVAILABILITY_DECLARATION.md`** — `PREREG.md` line 448 orders reconstruction
   before the comparison, and the file is header-marked DRAFT.
2. **Fix the protocol before touching a tool** — the `pred_score` mapping row (§0.3), the tier
   column, the MVR roster and its declared exclusions. Item 3 (line 977) makes "before running"
   binding, and this step is hours, not days.
3. **Commit the protocol.** Line 973 requires it be "committed with this protocol before any tool is
   run".
4. **P1 → P2** — implement the cases, then the harness.
5. **Run the four tools.** Record versions and configuration *before results are read* (§2.4).
6. **Adjudicate, then publish** — including the abstention and crash registers.

**Step 2 is the only step that is cheap now and impossible later.** Everything else can slip; the
ex-ante properties cannot be recovered once a result has been seen.

---

## Author decisions this file records rather than makes

1. **Whether a documented ineligibility discharges §9.2's fixture surface** (Part a.2), or whether
   line 973's "runs on the acceptance fixture" demands an execution even when no tool accepts the
   input.
2. **Whether the `pred_score`-is-unmapped row is added to the label mapping before any run**
   (§0.3). *Time-critical — item 3 forbids adding it afterwards.*
3. **Whether IDE plugins and R-only tools are in §9.2's scope at all** (Part b.2). §9.2 is silent;
   item 6 cuts toward IN; §10.1 criterion 4 is a gate rule, not a roster rule.
4. **Whether running `leakage-analysis` may stand for `LeakageDetector` 2.0** (Part b.3).
5. **Whether items 5 and 6 are ordered as Part (d.3) reads them** — setup first, crash-abstention
   for what fails after it — or whether item 5 is unconditional.
6. **Whether an Artifact A run happens at all**, and if so that it is published as an Artifact A
   result and never as a fixture result (Part a.2, `AVAILABILITY_DECLARATION.md` lines 631–633,
   678–681).
7. **Whether Docker is authorized** on this machine for the static-analysis branch (Part c).
8. **Full run, MVR, floor, or deferral.** `killgate\KILL_GATE_STATUS.md` already frames the third
   option: a `DEVIATIONS.md` entry recording that Phase 0 advanced with §9.2 unrun, carrying
   criterion 3 as explicitly unevaluated. **This file's contribution to that choice is the number:
   53.5–123.5 hours for the full run against a 12–32 hour Phase 0 budget, seven weeks before
   1 November.** Deferral is the cheapest option and the one most easily mistaken for having done
   the work — which is exactly why, if taken, it has to be written down.
