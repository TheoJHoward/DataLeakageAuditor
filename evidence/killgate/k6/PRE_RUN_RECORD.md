# PRE_RUN_RECORD.md — item K6, written BEFORE any case was run

Item K6 of the kill-gate completion pass, 2026-08-14. This file discharges `PREREG.md` §9.2
items **1** (eligibility, from documentation), **2** (versions and configuration), **3** (label
mapping written down before running) and **6** (manual setup recorded), and it was written and
fixed **before the first tool was pointed at a case**.

`PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` are byte-unchanged by
this item. Nothing was installed into the repository or the archive; every environment is a
dedicated virtualenv outside both.

---

## 0. Scope ruling applied, and its check against §9.2's text

**The ruling given to this item:** include any tool that is PROGRAMMATICALLY RUNNABLE regardless
of language (R via `Rscript` counts); record IDE-only tools as **abstentions** with the recorded
reason "not programmatically runnable", published in the counts rather than omitted.

**Check against the registered text — the ruling does not contradict §9.2.** `PREREG.md` lines
973–981 name no language, no interface form, no IDE and no notion of runnability; §9.2 does not
define "tool". The ruling therefore fills a silence rather than overriding a clause. Two
registered clauses are consistent with it and none is in tension:

- line 980, "**Manual setup allowed** and recorded" — an R toolchain or a container prerequisite
  is ordinary manual setup, which item 6 permits rather than excuses.
- line 978, "**Ineligible cases score as abstentions, not misses**" — recording an unrunnable tool
  as a published abstention is exactly item 4's disposition, and item 5 ("counts published")
  confirms abstentions belong in the published counts rather than being dropped.

**One caveat reported rather than resolved:** §10.1 **criterion 4** (line 1023) — "Installs and
runs through a documented public interface without author modification" — is a *gate* criterion,
not a roster rule. Admitting an IDE-only tool to the §9.2 roster as an abstention says nothing
about whether it passes criterion 4. The two questions are kept separate throughout.

---

## 1. Machine and toolchain

| Item | Value |
|---|---|
| OS | Windows 11 Home 10.0.26200 |
| Python | 3.12.10 (all venvs); **3.13.1 also present; no ≤3.11 interpreter exists on this machine** |
| R / `Rscript` | **NOT INSTALLED** |
| Docker | **NOT INSTALLED** |
| WSL | **NOT INSTALLED** (`wsl --status` → "The Windows Subsystem for Linux is not installed") |
| Souffle datalog engine | **NOT INSTALLED**, and not available as a Windows build |
| Run date | 2026-08-14 |
| Environment root | `C:\Users\ttbea\k6env\` — four dedicated virtualenvs, outside the repository and outside the archive |

**Recorded deviation on environment location.** The item directory was the intended venv location.
Windows `MAX_PATH` (260) defeated it: the scratchpad prefix is ~150 characters and `pip` failed
with "This system does not have Windows Long Path support enabled" while unpacking `scikit-learn`.
Long-path support is a system/security setting and was **not** changed. The venvs were relocated to
`C:\Users\ttbea\k6env\`; every deliverable, case file and raw output stays in the item directory.

---

## 2. Versions and configuration (§9.2 item 2, line 976)

Recorded **before results were read**. Four isolated virtualenvs; the tools disagree about
`numpy`/`pandas`, which is itself a finding about the roster's maintenance spread.

### 2.1 venv `general` — `leakage-buster`, `Leakly`, `temporalcv`, `leakfence`

```
python 3.12.10
leakage-buster==1.0.2      leakfence==0.5.0       Leakly==0.1.2      temporalcv==2.3.0
numpy==1.26.4   pandas==2.3.3   scikit-learn==1.6.1   scipy==1.15.3   statsmodels==0.14.6
```
Install channel: `pip install <name>` from PyPI. No non-default parameters except those recorded
per tool in §4. **Note:** `leakage-buster` pulled `numpy` down to 1.26.4 and `Leakly` pinned
`scikit-learn` to 1.6.1 during resolution; the versions above are the **post-resolution** state
these tools actually ran under.

### 2.2 venv `ld` — `leak-detect`

```
python 3.12.10
leak-detect==0.0.1   numpy==1.26.4   pandas==2.2.3   scikit-learn==1.9.0
```
Install channel: `pip install leak-detect` (PyPI). Manual setup: **`numpy` and `pandas` pinned back
to 1.26.4 / 2.2.3**, recorded in §3.

### 2.3 venv `dc` — `deepchecks`

```
python 3.12.10
deepchecks==0.19.1   numpy==1.26.4   pandas==2.2.3   scikit-learn==1.5.2
category-encoders==2.6.3   setuptools==80.10.2
```
Install channel: `pip install deepchecks==0.19.1` (PyPI). Manual setup: four dependency pins,
recorded in §3.

### 2.4 venv `omds` — OMDS / `oh-my-datascience`

```
python 3.12.10
omds==0.1.0   numpy==2.5.2   pandas==3.0.5   scikit-learn==1.9.0
```
Install channel — the repository's **own documented route** (`README.md` line 138), after the
repo-root route failed:
```
pip install "git+https://github.com/spkc83/omds.git#subdirectory=python/omds"
```
Repo `spkc83/omds`, Apache-2.0, pushed 2026-08-06. Entry point used: `omds-guardrails check --files`.

### 2.5 `leakage-analysis` (Yang et al.)

Checkout `malusamayo/leakage-analysis`, MIT, commit `a7d038bfec6b8ddbe21d87dde54b806aecdd79f7`,
authored **2023-05-02**. Not installed — see §3 and §5.

### 2.6 Documentation-vs-installed-version delta (`CROSS_TOOL_COMPARISON.md` §2.4's required field)

| Tool | Eligibility declared from | Installed | Delta |
|---|---|---|---|
| `leak-detect` | source read of `base.py` | 0.0.1 — same sole release | **none** |
| `deepchecks` | `stable` docs | 0.19.1 | check names verified against the installed galleries at run time; recorded per cell |
| `leakage-buster` | published API surface, `[P]` | 1.0.2 | **material** — see §4.2 |
| `Leakly` | PyPI one-line summary, `[P]` | 0.1.2 | **material** — see §4.3 |
| `temporalcv` | docs | 2.3.0 | **minor** — installed exposes six gates, protocol named two; see §4.4 |
| `leakfence` | docs | **0.5.0** | protocol recorded no version; check vocabulary read from source, §4.5 |
| OMDS | docs | 0.1.0 | route (b) of the README, not `uv`; see §4.6 |

---

## 3. Manual setup, recorded (§9.2 item 6, line 980)

Every step below is **dependency/environment configuration**. No tool's own source was edited, so
§10.1 criterion 4's "without author modification" is not engaged by any of it.

| # | Tool | Step | Why |
|---|---|---|---|
| S1 | `leak-detect` | **ATTEMPTED and FAILED:** `pip install "numpy<1.24"` | The pin `CROSS_TOOL_COMPARISON.md` §2.3 anticipates. It **cannot be satisfied on this machine**: `numpy` 1.23.x ships no cp312 wheel, its sdist build fails on Python 3.12 with `AttributeError: module 'pkgutil' has no attribute 'ImpImporter'`, and **no Python ≤3.11 interpreter exists here**. Recorded as an attempted, documented, failed setup step |
| S2 | `leak-detect` | `numpy==1.26.4`, `pandas==2.2.3` | Closest era-compatible stack reachable on Python 3.12. `np.complex` is still absent (verified: `hasattr(np,'complex')` → `False`), so S2 does **not** rescue the complex probe |
| S3 | `leak-detect` | run the vertical and horizontal detectors **twice**: once at library default (`only_nan=False`) and once with **`only_nan=True`** | `only_nan` is a **documented public parameter** of both `detect_vertical_leakage` and `detect_horizontal_leakage` (`base.py` lines 114, 244). Passing it is **configuration under item 2**, not modification. See the scoring consequence in §6.3 |
| S4 | `deepchecks` | `setuptools<81` | 0.19.1 imports `pkg_resources`, removed from the default environment |
| S5 | `deepchecks` | `scikit-learn==1.5.2` | 0.19.1 requests the `max_error` scorer, renamed in later sklearn → `ValueError` at import |
| S6 | `deepchecks` | `category_encoders==2.6.3` | 2.10.0 imports `sklearn.utils.Tags`, which needs sklearn ≥1.6 → conflicts with S5 |
| S7 | `deepchecks` | `pandas==2.2.3`, `numpy==1.26.4` | 0.19.1 predates pandas 3.0 |
| S8 | OMDS | documented route (b), `#subdirectory=python/omds` | The repo-root route fails: `error: Multiple top-level packages discovered in a flat-layout: ['hooks', 'skills']` |
| S9 | `leakage-analysis` | **ATTEMPTED and FAILED** — see §5 | Souffle, a customised pyright submodule and Python 3.8 are required; the documented alternative is Docker. Souffle has no Windows build; Docker and WSL are both absent, and installing either is a system-level change outside this item's authority |

---

## 4. Eligibility, declared from documentation, before any run (§9.2 item 1, line 975)

### 4.1 The governing declaration and one added rule

`CROSS_TOOL_COMPARISON.md` §2.3's matrix is the **primary, ex-ante** declaration and is carried
unchanged. Its `[P]` cells are explicitly provisional — the file requires each to be "re-declared
from documentation against the installed version before the run". That re-declaration is made here,
before any run, which is where item 1 puts it.

> **Union rule, declared now.** Where the installed version's documentation **contradicts** a `[P]`
> cell, the cell becomes the **union** of the protocol's declaration and the installed tool's
> documented capability — that is, eligibility is only ever **widened**, never narrowed. A widened
> cell gives a competitor **more** opportunities to score a hit against this project, and never
> fewer. This is the direction the instruction "score conservatively against this project's
> interest" requires, and it also means no tool is retro-excused from a case it could have handled.

### 4.2 `leakage-buster` 1.0.2 — material delta

Source read of `leakage_buster/core/checks.py` (installed) shows a detector registry emitting
seven leakage risk families, not the four the protocol's §2.5 anticipated. Documented entry point
`leakage_buster.api.audit(df, target, time_col=..., cv_type=...)`. Eligibility **widened** from
{C1, C5, C6, C7} to **{C1, C4, C5, C6, C7}** — its `KFold leakage risk` detector inspects duplicate
structure, so C4 is added. C2/C3 stay ineligible: nothing in the installed package inspects pipeline
construction.

### 4.3 `Leakly` 0.1.2 — material delta

The protocol declared Leakly eligible on **C5 and C6 only**, from a one-line PyPI summary. The
installed package's own `load_example_leakage_config()` shows what it actually models: a pipeline
**stage order** in which `imputation`, `normalization` and `feature_selection` run **before**
`data_split`. That is preprocessing-fit-on-train+test (**T2**) and selection-on-train+test (**T3**).
Eligibility **widened** to **{C2, C3, C5, C6}**. C5/C6 are retained, per the union rule, even though
the installed evidence does not support them — narrowing would excuse the tool from cases the
ex-ante protocol committed it to.

### 4.4 `temporalcv` 2.3.0 — minor delta

Installed exposes six gates (`gate_signal_verification`, `gate_suspicious_improvement`,
`gate_temporal_boundary`, `gate_synthetic_ar1`, `gate_residual_diagnostics`,
`gate_theoretical_bounds`) plus `run_gates`. Protocol named two. Eligibility {C1, C6} unchanged;
the **full gate suite** is run so the tool gets its widest shot, and `gate_temporal_boundary` is
mapped in §5 below.

### 4.5 `leakfence` 0.5.0

Check vocabulary read from installed source (`leakfence/_common.py`): `index_overlap`,
`duplicate_rows`, `group_overlap`, `temporal_overlap`, `global_preprocessing`. Documented entry
points `audit_split(train_idx, test_idx, subject=..., ...)`, `check_duplicates(X, train_idx,
test_idx)`, `lint_pipeline(pipe)`. Eligibility {C1, C2, C4, C7} unchanged — it matches the installed
check set exactly.

### 4.6 OMDS 0.1.0

Entry point `omds-guardrails check --files <file>` — static ontology violations over **source
files**. Eligibility {C1, C2} unchanged. The runtime `fit()` taint guard is a kernel hook
(`install-kernel-hook`) that arms the *current interpreter*; it is exercised via the static route
only, and that limitation is recorded rather than scored against the tool.

### 4.7 The final eligibility matrix used for scoring

**E** eligible · **I** ineligible → abstention (item 4) · **+** widened by §4.1's union rule

| Tool | C1 T1 | C2 T2 | C3 T3 | C4 T4 | C5 T5 | C6 T6 | C7 T7 | C8 T8 | E |
|---|---|---|---|---|---|---|---|---|---|
| `leak-detect` 0.0.1 | I | I | I | I | **E** | **E** | I | I | 2 |
| `deepchecks` 0.19.1 | **E** | I | I | **E** | **E** | **E** | I | **E** | 5 |
| `leakage-buster` 1.0.2 | **E** | I | I | **E+** | **E** | **E** | **E** | I | 5 |
| `Leakly` 0.1.2 | I | **E+** | **E+** | I | **E** | **E** | I | I | 4 |
| `leakage-analysis` | **E** | **E** | **E** | **E** | I | I | I | I | 4 |
| `LeakageDetector` 2.0 | **E** | **E** | **E** | **E** | I | I | I | I | 4 |
| OMDS 0.1.0 | **E** | **E** | I | I | I | I | I | I | 2 |
| `temporalcv` 2.3.0 | **E** | I | I | I | I | **E** | I | I | 2 |
| `leakfence` 0.5.0 | **E** | **E** | I | **E** | I | I | **E** | I | 4 |
| `leakr` 0.1.0 (R) | **E** | I | I | **E** | **E** | I | I | I | 3 |
| `bioLeak` 0.3.8 (R) | I | I | I | I | **E** | I | I | I | 1 |

**Totals: 88 tool × case cells across 11 tools; 36 eligible, 52 declared ineligible → abstentions.**
The protocol's 9-tool roster gave 29/72; the two R tools admitted by the scope ruling add 4 eligible
cells and the union rule adds 3 (`leakage-buster` C4, `Leakly` C2/C3).

**R-pair eligibility, declared from documentation before any run.** `leakr` 0.1.0 documents
duplication, target-correlation and train/test contamination checks → C1, C4, C5. `bioLeak` 0.3.8
documents permutation-based statistical diagnostics → C5. Per `J6_SCOPED_PLAN.md` (b.3), C2/C3/C6
are **ineligible-by-port** for both: those cases are about pipeline construction and per-cell
availability semantics, and a port that flattens them into plain R data frames would be a **case
modification** forbidden by item 7, not setup.

---

## 5. Label mapping, written down before running (§9.2 item 3, line 977)

`CROSS_TOOL_COMPARISON.md` §2.5 is carried unchanged. The rows below are **additions** required by
the installed versions, and every one is fixed here, before the run.

### 5.1 Additions

| Tool output label (installed) | Maps to | Note |
|---|---|---|
| `leakfence` `index_overlap` | **T1** | §2.5's "split-integrity error" under its installed name |
| `leakfence` `duplicate_rows` | **T4** | `check_duplicates` is called **with** `train_idx`/`test_idx`, so it is a cross-split test |
| `leakfence` `group_overlap` | **T7** | §2.5's "subject/session group overlap" |
| `leakfence` `temporal_overlap` | **T4** | per §2.5's explicit decision: window overlap → duplicates, **not** T6 |
| `leakfence` `global_preprocessing` | **T2** | §2.5's "preprocessing lint" |
| `leakage-buster` `Target leakage (high correlation)` | **T5** | §2.5's `|corr| ≥ 0.98` row |
| `leakage-buster` `Target leakage (categorical purity)` | **T5** | same family |
| `leakage-buster` `Target Encoding leakage risk` | **T5** | illegitimate-feature family |
| `leakage-buster` `Aggregation traces leakage risk` | **T5** | illegitimate-feature family |
| `leakage-buster` `Rolling statistics leakage risk` | **T6** | §2.5's "time leakage" under its installed name |
| `leakage-buster` `KFold leakage risk (use GroupKFold)` | **T7** | §2.5's "group leakage" |
| `leakage-buster` `CV strategy mismatch` | **T1** | §2.5's "CV-strategy mismatch" |
| `leakage-buster` `CV strategy recommendation` | **unmapped** | emitted whenever `cv_type` is not supplied; a configuration suggestion, not a finding. Left unmapped so it cannot become a guaranteed false alarm — the disposition **generous to the tool** |
| `leakage-buster` `Time column missing` / `Time parse errors` / `Time-awareness suggestion` | **unmapped** | data-quality, not leakage |
| `leakage-buster` `Detector error: <name>` | **unmapped**, and **counted as a crash** | an internal detector exception; item 5 applies to it |
| `temporalcv` `gate_temporal_boundary` | **T6** | temporal-boundary family, alongside §2.5's two named gates |
| `temporalcv` `gate_synthetic_ar1`, `gate_residual_diagnostics`, `gate_theoretical_bounds` | **unmapped** | model-adequacy diagnostics, not leakage types |
| OMDS `omds-guardrails check` ontology violation naming a split/preprocessing rule | **T1** / **T2** by the rule's own subject | its `ax:fit_on_train_only` family is §2.5's existing row |
| `leakr` `duplication` → **T4**; `target correlation` → **T5**; `train/test contamination` → **T1** | | declared from CRAN documentation |
| `bioLeak` permutation diagnostic | **T5** | declared from CRAN documentation |

### 5.2 The generic-verdict rule, declared now

> A tool whose documented output is a **single undifferentiated leakage / no-leakage verdict** —
> `Leakly`'s permutation verdict, and the boolean `has_leakage` returned by `leak-detect`'s
> wrappers — has that verdict mapped to **the type of the case it was run on**. Any other treatment
> would make a binary detector unscoreable.

This is deliberately **generous**: it lets a generic detector claim a hit on any eligible case.
`leak-detect` is unaffected in substance because §2.5 already separates its two probes
(vertical → T6, horizontal → T5) and this item scores it probe-wise.

### 5.3 The `pred_score` row recommended by `J6_SCOPED_PLAN.md` §0.3

Adopted, and recorded here before any run: **`pred_score` is a model output, not a feature; any
tool finding whose subject column is `pred_score` is unmapped and scores nothing on either fixture
side.** It binds only if a fixture-surface run happens; §7 records that none did.

---

## 6. Scoring rules

`CROSS_TOOL_COMPARISON.md` §2.6 items 1–4 are carried unchanged (ineligible → abstention; crash →
abstention with counts published; no case excluded after results are seen; manual setup allowed and
recorded). Three further rules are fixed here, before the run, because §2.6 does not cover them.

**6.1 What counts as a HIT.** Each case ships with a clean paired control. A tool scores a **HIT**
on a case only if it **fires on the contaminated side AND is silent on the clean side**, with the
firing label mapping to that case's type under §5. This is the pairing discipline of
`CROSS_TOOL_COMPARISON.md` §2.2 and it mirrors §10.1 criterion 3's own two-sided shape.

- fires contaminated, silent clean → **HIT**
- silent contaminated → **MISS**
- fires on **both** sides → **MISS**, and additionally recorded in the **false-alarm register**
- fires clean only → **MISS** + false alarm

**6.2 Ambiguity is scored against this project's interest.** Where the protocol is ambiguous, the
reading that credits the competitor is taken, and the ambiguity is recorded on the cell. Applied at:
the union rule (§4.1), the generic-verdict rule (§5.2), `deepchecks`'s generous T6 eligibility
(inherited from §2.3), and the unmapped treatment of `CV strategy recommendation` (§5.1).

**6.3 `leak-detect` is scored probe-wise, and the crash is published separately.** Per
`J6_SCOPED_PLAN.md` (d.3) qualification 3: only the **complex** probe calls `np.complex`; the NaN
probe does not. The default-configuration run (`only_nan=False`) is executed and its complex-probe
failure is recorded as an **item-5 crash-abstention with the error text, counted and published**.
The `only_nan=True` run — documented configuration, §3 S3 — is executed separately and **the NaN
probe's result is scored on its merits**. Scoring the whole tool as a crash-abstention would let the
only in-kind competitor escape the flagship case on a technicality, in this project's favour;
`CROSS_TOOL_COMPARISON.md` §2.6 and `J6_SCOPED_PLAN.md` (d.3) both reject that, and so does this
item.

---

## 7. Surfaces run

**Comparison surface (C1–C8 + eight clean controls): RUN.** This is where the comparison lives.

**Acceptance-fixture surface: NOT RUN, and no fixture result is reported.** Two registered reasons,
both independent of effort:

1. `PREREG.md` line 448 orders reconstruction **before** the comparison, and
   `AVAILABILITY_DECLARATION.md` is header-marked "**DRAFT — AUTHOR REVIEW REQUIRED** … Nothing in
   this file is a registered declaration" (lines 3–5). The ordering is not satisfied.
2. `J6_SCOPED_PLAN.md` (a.2) declares all nine rostered tools **ineligible on the fixture surface
   from documentation**: the fixture is a stored per-second prediction pair carrying `pred_score`,
   `true_label`, `fwd_move_ticks`, `mid_price_t` — no features, no split, no callable, no source.

**Consequence, stated plainly and carried into the verdict: §10.1 criterion 3 is UNEVALUATED for
every tool.** No wording in this item's output implies a fixture run occurred.

---

## 8. Case set, fixed and hashed before the run (§9.2 item 7, line 981)

C1–C8 and their eight clean controls are implemented at `harness/case_defs.py` from
`CROSS_TOOL_COMPARISON.md` §2.2's specification table, materialised to `cases/`, and hashed in
`cases/MANIFEST.json` **before the first tool ran**. `full.csv` SHA-256, contaminated side:

| Case | Type / row | SHA-256 of `full.csv` (contaminated) |
|---|---|---|
| C1 | T1 / L1.1 | `fb01082ab455ed652ff6ee8931144ce0982bb370f8604388d4e1142be8e95f46` |
| C2 | T2 / L1.2 | `f5b905601b858d82041c25cf8f16505ed34f23767b7e90583c7e6b7754b9be54` |
| C3 | T3 / L1.3 | `bd116bb75c6217456c169835bc2343145bce3e1410f7c53821ed7734d1beb7d3` |
| C4 | T4 / L1.4a | `44f45a580677e4f3894725a04fb24ba206cfc46fff20092dd512723778b4b7d4` |
| C5 | T5 / L2a | `ed74f3228693cd471d5fde83d3ca88fb3e39bc122f0769c54ebb225b768c78bf` |
| C6 | T6 / L3.1 | `e5966f64284b58a15089de9ec9db8a30dadbdca85fe1e1b0c21292ef01867731` |
| C7 | T7 / L3.2 | `1c113c0c39d72ab4a5d7f8f6263acdc96086b538e66a9a5c853faf2f22dfda4b` |
| C8 | T8 / L3.3 | `6d5e32c488934690fa0520d82026c9dfabbaba9fb3786f7140476e322196e31d` |

C1 and C7 hash **identically across their two sides** — by construction: only the declared split
differs, not the data. That is the point of both cases.

**Adapters, and the item-7 judgment recorded per adapter** (`CROSS_TOOL_COMPARISON.md` §2.6 item 4:
an adapter that changes what a case tests is a forbidden case modification; one that only reshapes
the same content is setup):

| Adapter | Judgment |
|---|---|
| frame → `(train.csv, test.csv)` by the declared index arrays | **setup** — same rows, same values |
| frame → numpy index arrays for `leakfence` | **setup** — the split declaration restated in the tool's input form |
| case → `data_creation_func` callable for `leak-detect` | **setup** — `case_defs.build` is the case's own feature construction, not a new one |
| case → standalone `.py` script for OMDS / static analyzers | **setup** — the same construction expressed as source, which is the only form a static analyzer reads |
| model fitted per case for `temporalcv`'s gates | **setup** — the gates take a fitted model; the model is not part of the case |
| C2/C3/C6 → R data frames | **NOT ATTEMPTED — would be a case modification.** Declared ineligible-by-port instead |
