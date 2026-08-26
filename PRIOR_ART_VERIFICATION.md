# PRIOR_ART_VERIFICATION.md

Author's ledger of prior-art tools checked at source. Fulfills the "written down" clause of `HISTORY.md` H-L1 ("*Prior-art verification is a search task, done by the author, written down.*") and the Phase 0 gate obligation in `PREREG.md` §9.2 and §11 ("Fixture declaration reconstruction with evidence; **prior-art verification**; cross-tool comparison per §9.2; licence check"). Comparison-table summaries live in `DESIGN.md` §2.11; the details behind each row live here.

**What each entry records.** Name and version verified. Date of the source read. Whether the tool is equivalent-in-kind to any detector in this project. If not equivalent, the specific construction facts (file, line) that show the difference, so a later reader can re-verify without re-searching.

**When this file grows.** One entry per prior-art tool the author reads at source before making a novelty or equivalence claim. Entries are append-only within a review cycle; a claim of non-equivalence that later turns out wrong is recorded as a **correction** below the original entry, not as an edit to it.

**When the licence line matters.** Any strategy, method, fixture, or defence borrowed from a listed tool carries an attribution note at the borrow site regardless of the tool's licence, and the licence itself is recorded here so a Phase 3 release audit can reproduce the trace.

---

## Entries

- **leak-detect** (Pawar, 2020, v0.0.1, MIT, single release):
  VERIFIED AT SOURCE by author, 12 Aug 2026. Black-box runtime perturbation
  of a user-supplied `data_creation_func` — the runtime-probe idea is
  genuine prior art and is not claimed as novel here. NOT equivalent:
  the corruption region is a single scalar row index
  (`check_row_number`, `base.py:39`, default `int(len(data)/2)`) applied as
  a row-block × column-list rectangle (`base.py:73`), so there is no
  per-row decision time and no per-cell availability representation in
  the API. Detection signal is NaN-count propagation (`base.py:60/91`),
  not a per-row availability comparison. Also broken on NumPy >= 1.24
  (`np.complex` at `base.py:76` and `base.py:209`).

- **leakage-buster** (PyPI v1.0.2, released 13 Sep 2025, Production/Stable):
  dataset-level audit covering target leakage (`|corr| >= 0.98`), statistical
  leakage (target encoding, WOE, rolling stats), time leakage, group leakage,
  CV-strategy mismatch (`TimeSeriesSplit` / `KFold` / `GroupKFold`), and
  calibration consistency. NOT EQUIVALENT: its interface takes a dataframe,
  a target, and a CV strategy; it executes no user-supplied feature function,
  so a per-cell availability comparison is not expressible in its API. Its
  time check is split-granular (train/test ordering and splitter
  appropriateness), same class as `leakr`. ASSESSED FROM PUBLISHED API
  SURFACE, NOT SOURCE — recorded as such, because the absence of a
  user-callable parameter places it outside the primitive's neighbourhood
  by construction. Surfaced by the author's own search of 12 Aug 2026;
  NOT surfaced by the automated sweep conducted the same date. The
  divergence is recorded because it bears on how the coverage claim
  should be weighted: automated search did not reach this candidate. Broadest leakage-family
  coverage of any candidate found (~6 of 8).

- **Method note (sweep calibration).** The scrutiny tier applied to a
  candidate is set by one question — does its interface accept a
  user-supplied feature function? Candidates that do (`leak-detect`) are
  read at source. Candidates that do not (`leakage-buster`, `leakr`,
  `bioLeak`, `deepchecks`, `mlinspect`, feature stores) are assessed at
  interface level, since no availability comparison is expressible without
  a callable to probe.
