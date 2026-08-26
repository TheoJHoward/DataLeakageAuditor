# RUN_LOG.md — item K6, 2026-08-14

Chronological. Everything below happened on one machine on one date. `PREREG.md`,
`AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` were **not edited**; no git
state-changing command was run; the archive at `MBO_2025` was not touched.

| # | Step | Outcome |
|---|---|---|
| 1 | Read `CROSS_TOOL_COMPARISON.md`, `J6_SCOPED_PLAN.md`, `KILL_GATE_STATUS.md`, and `PREREG.md` §9.2 / §10.1 verbatim | §9.2 text at lines 973–981 confirmed identical to the protocol's quotation; §10.1 at 1018–1024 |
| 2 | Checked the scope ruling against §9.2's text | No contradiction: §9.2 names no language, interface form or runnability notion. Recorded in `PRE_RUN_RECORD.md` §0 |
| 3 | Surveyed the toolchain | Python 3.12.10 / 3.13.1 only. **No Python ≤3.11, no R, no Docker, no WSL, no Souffle** |
| 4 | Created venvs under the item directory | **FAILED** — Windows `MAX_PATH`; `pip` aborted unpacking `scikit-learn`. Long-path support is a system setting and was **not** changed |
| 5 | Relocated venvs to `C:\Users\ttbea\k6env\` | Five venvs: `general`, `ld`, `dc`, `omds`, `lav`. Deliverables stayed in the item directory |
| 6 | `pip install "numpy<1.24"` (the pin `CROSS_TOOL_COMPARISON.md` §2.3 anticipates) | **FAILED** — no cp312 wheel; sdist build dies on `pkgutil.ImpImporter`; no ≤3.11 interpreter exists. Recorded as attempted setup S1 |
| 7 | Installed `leak-detect` 0.0.1, pinned `numpy==1.26.4`/`pandas==2.2.3` | Installed. `hasattr(np,'complex')` → `False`, so the pin does **not** rescue the complex probe |
| 8 | Read `leak_detect/base.py` at source | `np.complex` confined to lines 76 and 209 (complex probe only). **`only_nan` is a documented public parameter** (lines 114, 244). `check_row_number` defaults to `int(len(data)/2)` — pure row position |
| 9 | Installed `leakage-buster` 1.0.2, `Leakly` 0.1.2, `temporalcv` 2.3.0, `leakfence` 0.5.0 | All from PyPI, clean |
| 10 | Installed `deepchecks` 0.19.1 | Needed four era pins (S4–S7): `setuptools<81`, `scikit-learn==1.5.2`, `category_encoders==2.6.3`, `pandas==2.2.3`/`numpy==1.26.4` |
| 11 | Installed OMDS | Repo-root route failed (`Multiple top-level packages ... ['hooks','skills']`); the README's documented route (b) `#subdirectory=python/omds` succeeded → `omds==0.1.0` |
| 12 | Enumerated every tool's output-label vocabulary **from source**, not from results | Fed the label-mapping additions of `PRE_RUN_RECORD.md` §5.1 |
| 13 | **Wrote `PRE_RUN_RECORD.md`** — versions, configuration, eligibility (union rule), label mapping, scoring rules, adapter judgments | Items 1, 2, 3, 6 discharged **before the first case ran** |
| 14 | Implemented C1–C8 + eight clean controls (`harness/case_defs.py`), materialised and hashed | 16 case-sides; `cases/MANIFEST.json`. Item 7's ex-ante fix |
| 15 | Determinism fix: C5's builder drew noise inside `build()` | Corrected **before any tool ran**; re-materialised; all 16 builders verified byte-identical across two calls; C5 hash updated in `PRE_RUN_RECORD.md` §8 |
| 16 | Ran `leak-detect` — 4 cases × 2 sides × 2 configurations | Default config crashed at the complex probe on **8/8 cells** (`AttributeError: module 'numpy' has no attribute 'complex'`) → item-5 crash count. `only_nan=True` ran clean and was scored |
| 17 | Ran `deepchecks` (first pass) | Every cell reported "no conditions fired" — **harness bug**: `ConditionResult.is_pass` is a *method*, so `bool(c.is_pass)` is always `True` |
| 18 | Fixed the deepchecks harness to read `ConditionResult.category`; added a `row_id` index adapter so `Index Train Test Leakage` could run at all | Re-ran. Real firings appeared. Without the fix this item would have published a false "deepchecks never fires" result |
| 19 | Ran `leakage-buster`, `leakfence`, `temporalcv` over all 16 case-sides | `leakage-buster` raised `Detector error: target_leakage` on both C6 sides → item-5 crash |
| 20 | Fixed two `leakfence` harness bugs: `check_duplicates` returns a `(groups, violations)` tuple; the C2 preprocessing lint was never exercised | Re-ran with `lint_pipeline` on a fitted sklearn `Pipeline` |
| 21 | Ran `Leakly` — permutation workflow, 25 permutations, firing rule declared before the run | Fired on **none** of its four eligible cells; permuted-label AUC stayed at chance throughout |
| 22 | Emitted each case as source; ran OMDS | First pass: **zero** violations everywhere, including a canonical positive control. Diagnosed from source: OMDS's rules are **intra-function only** and key on `train_test_split` |
| 23 | Re-emitted the cases function-wrapped, with `train_test_split` in C2/C3; re-ran OMDS | Positive control fired. C2 contaminated → `ax:fit_on_train_only` **certain**, clean silent |
| 24 | `leakage-analysis` (Yang): cloned, `git submodule update --init --recursive`, installed `requirements.txt` in venv `lav` | Souffle unavailable (no Windows build; Ubuntu PPA only). Docker and WSL both absent, and installing either is a system-level change outside this item's authority |
| 25 | Ran `python -m src.main` on all 16 case scripts | **16/16 crashed** at `src/irgen.py:373 visit_Subscript AssertionError` — the failure is in its own IR generator, before the datalog stage is reached |
| 26 | R install for `leakr` / `bioLeak`: `winget --location`, then default scope, then `--scope user`, then the vendor installer with `/VERYSILENT /CURRENTUSER /DIR=` | **All failed.** Machine-wide install needs administrator elevation (unavailable non-interactively and outside this item's authority); no user-scope installer is published. Recorded as an abstention with the reason |
| 27 | Scored with `harness/score.py`, using only the ex-ante eligibility and label mapping | 88 cells. Strict reading 8/15/65; conservative reading (adopted) **9 hits / 14 misses / 65 abstentions** |
| 28 | Wrote `RESULTS_MATRIX.md`, `env/VERSIONS.txt`, `K6_RESULTS.md` | — |
| 29 | Final integrity check of the repository | `PREREG.md` sha256 **`f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6`** — unchanged, matches `KILL_GATE_STATUS.md` line 5. **`HEAD` had advanced from `ffa6d94` to `80401d0` during this run, by a different item** ("Kill-gate sign-off (H-34, prior art) with four factual corrections…"), which also added an untracked `LICENSE` and modified `tools/check_registration.py`. **K6 made no commit and ran no git state-changing command; none of those changes is K6's.** |

## Harness bugs found and fixed before scoring — recorded because each would have flattered this project

| Bug | Would have produced |
|---|---|
| `bool(ConditionResult.is_pass)` on a bound method | "deepchecks fires on nothing" — a false clean sweep against the strongest data/split competitor |
| `check_duplicates` return value parsed as a report, not a `(groups, violations)` tuple | "leakfence detects no duplicates anywhere" — a false miss on C4 |
| `lint_pipeline` never called | leakfence silently unscored on C2, its own declared specialty |
| Case scripts emitted at module level | "OMDS detects nothing at all" — a false clean sweep; OMDS's rules are intra-function only |
| C5's builder drawing RNG inside `build()` | a non-deterministic probe surface for the one tool that calls the builder twice |

**Every one of these was a bug that would have made competitors look worse.** They are listed
because the run's credibility depends on the reader knowing they were looked for.

## What was NOT run

- **The acceptance-fixture surface.** Not run, and no fixture result is reported. `PREREG.md`
  line 448 orders reconstruction first and `AVAILABILITY_DECLARATION.md` is header-marked DRAFT;
  independently, `J6_SCOPED_PLAN.md` (a.2) declares all rostered tools ineligible there from
  documentation. **§10.1 criterion 3 is consequently unevaluated for every tool.**
- **`LeakageDetector` 2.0 by hand in an editor.** Recorded as an abstention with the reason
  "not programmatically runnable", per the scope ruling.
- **The R pair.** Install failed; abstention with the reason. C2/C3/C6 would in any case have been
  ineligible-by-port (`J6_SCOPED_PLAN.md` b.3) because porting them would be a case modification.
