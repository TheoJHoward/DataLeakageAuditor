# LICENCE_CHECK.md — `PREREG.md` line 991, Phase 0 deliverable 4

**Status: DRAFT, UNCOMMITTED.** Produced by item G3, 2026-08-14. No file outside this directory
has been edited and no git operation has been performed.

**Not legal advice.** Every row below is a *fact about a published licence*, with its source.
Whether a given use is permitted is a determination for the author, and where a real obligation
attaches this file says so and stops.

**Scope.** `PREREG.md` line 991 lists "licence check" as one of four Phase 0 deliverables.
`PRIOR_ART_VERIFICATION.md` line 9 fixes what it is for:

> **When the licence line matters.** Any strategy, method, fixture, or defence borrowed from a
> listed tool carries an attribution note at the borrow site regardless of the tool's licence, and
> the licence itself is recorded here so a Phase 3 release audit can reproduce the trace.

The check therefore has **two halves**, and only one of them was partially done:

- **(A) Inbound** — the licence of every prior-art tool identified, and whether it constrains this
  project. **Completed by this item** (§1–§3 below).
- **(B) Outbound** — this project's own licence, `PREREG.md` §13.2, marked "**resolve in Phase 0**".
  **Not resolved, and not resolvable by research — it is an author decision** (§4 below).

---

## 1. Inbound — licence inventory, every prior-art tool identified

Sources marked **[sweep]** were verified against primary sources by the assistant prior-art sweep
recorded at
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\tasks\wv0bwus8j.output`.
Sources marked **[G3]** were verified by this item on 2026-08-14 — these are the rows that were
**missing** from the record before now.

| # | Tool | Licence | Source, and what it says | Verified |
|---|---|---|---|---|
| 1 | `leak-detect` (Pawar) | **MIT** | GitHub API `license.spdx_id = MIT`; `LICENSE` file in repo root; PyPI trove classifier "MIT License" (PyPI metadata `license` field itself empty) | [sweep] |
| 2 | `deepchecks` | **AGPL-3.0-or-later** | PyPI classifier "OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"; `LICENSE` on `main` read directly = GNU AGPL v3; README states AGPL 3.0 for the open-source projects, commercial licensing only for the separate Deepchecks **Monitoring** components | [sweep] |
| 3 | `leakage-buster` | **MIT** | PyPI JSON `license` field `"MIT"`; classifier "License :: OSI Approved :: MIT License"; latest 1.0.2 uploaded 2025-09-13T21:31:54 | **[G3]** |
| 4 | `Leakly` | **MIT** | PyPI JSON `license` field `"MIT"` (no trove classifier present); latest 0.1.2 uploaded 2026-05-14T09:56:43; summary "Leakage checks for machine-learning pipelines using permutation tests" | **[G3]** |
| 5 | `leakage-analysis` (Yang et al., ASE 2022) | **MIT** | GitHub API `malusamayo/leakage-analysis`, `license.spdx_id = MIT`, `pushed_at 2023-05-02` | [sweep] |
| 6 | `LeakageDetector` 1.0 (PyCharm plugin) | **NONE — no licence** | GitHub API `SE4AIResearch/DataLeakage_Fall2023`, `license: null`; last push 2024-05-14; absent from the JetBrains Marketplace (search API `total:0`) | [sweep] |
| 7 | `LeakageDetector` 2.0 (VS Code) | **MIT** | GitHub API `SE4AIResearch/DataLeakage_JupyterNotebook_Fall2024`, `license.spdx_id = MIT`, `pushed_at 2025-05-07` | [sweep] |
| 8 | NBLyzer | **MIT** | GitHub API `microsoft/NBLyzer`, `license.spdx_id = MIT`, `pushed_at 2023-05-23`, `archived: true` (archived 2026-06-15) | [sweep] |
| 9 | `temporalcv` | **MIT** | PyPI JSON; versions 1.0.0 (2026-01-08) through 2.3.0 (2026-06-14) | [sweep] |
| 10 | `leakr` (CRAN, R) | **MIT** | CRAN package page; v0.1.0 published 2025-10-26 | [sweep] |
| 11 | `bioLeak` (CRAN, R) | **MIT + file LICENSE** | CRAN package page: License "MIT + file LICENSE"; **Version 0.3.8, Published 2026-05-21** | **[G3]** |
| 12 | `leakfence` | **MIT** | GitHub `ptapal/leakfence`; PyPI; updated 2026-08 | [sweep] |
| 13 | OMDS / `oh-my-datascience` | **Apache-2.0** | GitHub `spkc83/omds`; not on PyPI (installs via `uv` from GitHub); active through 2026-07-31 | [sweep] |
| 14 | `train-test-leakage-detector` | **MIT** | GitHub `Krishna89287/train-test-leakage-detector`; 1 commit, Aug 2026 | [sweep] |
| 15 | `mlinspect` | **Apache-2.0** | GitHub API `stefan-grafberger/mlinspect`, `license.spdx_id = Apache-2.0`, `pushed_at 2024-02-24`, `archived: false` | **[G3]** |
| 16 | Feast (feature store) | **Apache-2.0** | GitHub API `feast-dev/feast`, `license.spdx_id = Apache-2.0`, `pushed_at 2026-08-14`, `archived: false` | **[G3]** |
| 17 | Hopsworks (feature store) | **AGPL-3.0** | GitHub API `logicalclocks/hopsworks`, `license.spdx_id = AGPL-3.0`, `pushed_at 2025-02-10`, `archived: false` | **[G3]** |
| 18 | Tecton; Databricks Feature Store; SageMaker Feature Store | **Proprietary / commercial service** | No open-source licence to check; they are hosted products, not distributable code. Cited descriptively in `HISTORY.md` H-34 line 285 | [sweep] |

**Coverage claim.** Rows 1–18 cover every tool named in `HISTORY.md` H-34 lines 277–285, every
tool named in `PRIOR_ART_VERIFICATION.md`, every tool in `DESIGN.md` §2.11's comparison table,
and every candidate in the 2026-08 sweep's four agent reports. **Before this item, six of them
(#3, #4, #11, #15, #16, #17) had no licence recorded anywhere in the project.** That is the
respect in which the licence check was partial.

---

## 2. Does it constrain this project?

The obligation depends entirely on **which of three activities** is performed. They are not the
same and the project has so far only done the first.

### 2.1 Activity 1 — reading and citing (what has happened to date)

`PREREG.md` §1.1, `DESIGN.md` §2.11, `PRIOR_ART_VERIFICATION.md` and `HISTORY.md` H-34 describe
and compare these tools and quote small identifying fragments of `leak-detect`'s source
(`base.py:39`, `:73`, `:60/91`, `:76`, `:209`) to evidence a non-equivalence claim.

**Constraint: none, on any row above.** Description and citation of a published work are not
distribution of it. No obligation attaches under MIT, Apache-2.0, or AGPL-3.0.

**Borrow ledger — current state: EMPTY.** Nothing has been copied from any listed tool into this
project: no code, no fixture, no test case, no defence. The runtime black-box probe *idea* is
credited as prior art rather than claimed, at `PREREG.md` line 156, line 160
("The one place this project's method differs from `leak-detect` in kind rather than degree"),
and `DESIGN.md` line 211. **That credit already discharges the attribution rule of
`PRIOR_ART_VERIFICATION.md` line 9 for the only thing taken, which is an idea and not a
copyrightable expression.** If anything is later copied, the ledger must gain a row naming the
borrow site.

### 2.2 Activity 2 — running the tools for the §9.2 cross-tool comparison

This is what §9.2 requires and has not yet happened (see `CROSS_TOOL_COMPARISON.md` Part (iii)).

**Constraint: low, but two rows are not clean.**

- **Rows 1–5, 7–17: no obligation from running.** MIT, Apache-2.0 and AGPL-3.0 all attach their
  obligations to *distribution* (AGPL additionally to *network provision to third parties*), not
  to running a program locally for one's own evaluation. Publishing *measurements about* a tool is
  not publishing the tool.
- **Row 6, `LeakageDetector` 1.0 — no licence at all.** With no licence, no rights are granted by
  default. Downloading and running it is at minimum an unresolved question and there is no need to
  resolve it: it is **excluded from the comparison roster** on independent grounds (no documented
  distribution channel, superseded by 2.0 which is MIT). **Recommendation: keep it excluded, and
  record "no licence" as one of the reasons** so the exclusion is not later read as arbitrary.
- **Row 2, `deepchecks` AGPL-3.0 — running is fine, but see §2.3.** Running deepchecks to score it
  on C1–C8 creates no obligation. The obligation question arises only at the wrap decision.

### 2.3 Activity 3 — wrapping, linking, or shipping — **the one live constraint**

`PREREG.md` §13.5 (line 1092) is an open decision: "Whether `deepchecks` is wrapped for L2b/L3.3 —
**Phase 6, on Phase 0 evidence.**" This licence check is that evidence, so the fact pattern is set
out precisely and the conclusion is left where it belongs.

**The fact pattern:**

1. `deepchecks` is **AGPL-3.0-or-later**. Its README offers commercial licensing only for the
   separate Deepchecks **Monitoring** product; **no commercial dual-licence is advertised for the
   core library**.
2. `PREREG.md` §11.5 requires: "**The repository is publicly reachable at the moment of tagging.**
   A registration nobody can fetch is not a registration." And §10 Phase 3's gate is "A stranger
   can install and run it." **This project distributes.** It is not a private internal tool, so
   the "obligations attach at distribution" carve-out of §2.2 does not protect the wrap decision.
3. AGPL-3.0 is a strong copyleft that extends to works that combine with the covered work, and its
   §13 additionally reaches users interacting over a network. Whether a particular wrapping is a
   combination triggering copyleft, or an arm's-length use of a separately-installed program
   through its public API, is a **legal determination that turns on how the wrap is built** — and
   it is not one this file will make.

**What this means for §13.5, stated as options rather than as a recommendation with a hidden cost:**

| Option | Licence consequence | Cost |
|---|---|---|
| **Do not wrap.** Reimplement L2b/L3.3 checks independently | none | duplicated effort; loses deepchecks' maturity |
| **Wrap and adopt AGPL-3.0 for this project** | consistent; no compatibility question | AGPL is a strong constraint on downstream adopters and on citability in commercial settings — likely to reduce uptake, which is the stated Phase 3 goal |
| **Optional extra: deepchecks not vendored, user installs it separately, interface via its public API only** | **the question, not the answer** — this is the arrangement whose status turns on the details of the combination, and it needs the author's determination before Phase 6 | if the determination goes the wrong way, the work is wasted late |

**This decision is due at Phase 6, not now.** What Phase 0 owed was the evidence, and the evidence
is: **AGPL-3.0-or-later, no dual licence for the core library, and this project distributes.**
That is recorded.

**Row 17, Hopsworks (AGPL-3.0)** is recorded for the same reason even though it is not in the
roster: it is the second AGPL item in the neighbourhood, and a later borrow should not happen
blind.

### 2.4 Permissive rows — the standing obligation if anything is ever borrowed

- **MIT** (rows 1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 14): copyright notice and permission notice must
  accompany copies and substantial portions. `PREREG.md` §13.2 line 1089 already commits beyond
  this: "`leak-detect` is MIT; **anything taken from it gets an attribution note regardless**."
- **`bioLeak`'s "MIT + file LICENSE"** is the CRAN convention for MIT plus a file naming the
  copyright holders. **That file must be read before any borrow**, because it carries the names
  the attribution has to reproduce. Not read by this item.
- **Apache-2.0** (rows 13, 15, 16): additionally requires retention of NOTICE content, a statement
  of changes to modified files, and carries a patent grant with a termination clause on patent
  litigation. **Materially more paperwork on borrow than MIT** — worth knowing before, not after.

---

## 3. Inbound verdict

**Nothing currently constrains this project**, because nothing has been borrowed and nothing has
been wrapped. **One future decision is genuinely constrained:** §13.5's deepchecks wrap, by
AGPL-3.0-or-later against a project that distributes publicly. The evidence Phase 0 owed that
decision is now on file.

---

## 4. Outbound — this project's own licence: **UNRESOLVED**

`PREREG.md` §13, line 1089:

> 2. Licence — **resolve in Phase 0**. `leak-detect` is MIT; anything taken from it gets an
>    attribution note regardless.

**It is not resolved, and the gap is verifiable in the repository as it stands:**

- **There is no `LICENSE` file.** `git ls-files` on
  `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01` returns 24 tracked files and none of
  them is a licence: `.gitattributes`, `.gitignore`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md`,
  `DEVIATIONS.md`, `HISTORY.md`, `PARKING_LOT.md`, `PREREG.md`, `PRIOR_ART_VERIFICATION.md`,
  `README.md`, `VALIDATED_CONFIG.toml`, `protocol/` (2), `registration-commit.txt`(+`.ots`),
  `tests/registration/` (7), `tools/check_registration.py`.
- **`README.md` declares no licence.** Its only occurrence of the word is line 59, which is about
  `PREREG.md` §5.4's *tier* licences — an unrelated sense of the word.

**The consequence, stated plainly.** `PREREG.md` §11.5 requires the repository to be publicly
reachable at the moment of tagging. A publicly reachable repository with no licence file grants no
rights by default — which is **exactly the defect this project's own comparison roster cites when
excluding `LeakageDetector` 1.0** (row 6: "no licence … no reuse rights"). The same test applied
to this repository today returns the same answer.

**This is not a research task and this item cannot complete it.** Choosing a licence is an author
decision with a real trade-off — and the §13.5 deepchecks question above is entangled with it,
because wrapping an AGPL library and shipping under a permissive licence is the combination that
does not work. The two decisions should be made together, or the licence chosen in a way that does
not foreclose §13.5.

**Recorded as: GENUINELY UNRESOLVED.** Phase 0's licence-check deliverable is complete on the
inbound half and open on the outbound half.

### 4.1 Adjacent, and not a Phase 0 gate item

`PREREG.md` §13.4, line 1091:

> 4. Whether the CME fixture ships in the repo, full or sliced — **CME redistribution terms must be
>    checked.** Blocks the Phase 3 release.

**Not checked.** `PREREG.md` places it at Phase 3, not Phase 0, so it does not hold the §10.1 kill
gate — but it is a redistribution-terms check, it blocks the release the whole plan is aimed at
(§10 line 1002, "Release at Phase 3"), and it is the kind of item that is cheap now and expensive
in October. Recorded here so it is not lost between §13.2's Phase 0 deadline and §13.4's Phase 3
one. **Nothing in the archive was consulted for this; it is named, not assessed.**

---

## 5. What this file changes about the record

Nothing yet — it is uncommitted and no other file has been edited. If the author adopts it, the
material that belongs in the permanent record is:

1. **Six licence rows** (`leakage-buster` MIT, `Leakly` MIT, `bioLeak` MIT + file LICENSE,
   `mlinspect` Apache-2.0, Feast Apache-2.0, Hopsworks AGPL-3.0) → `PRIOR_ART_VERIFICATION.md`,
   which line 9 designates as the place licences are recorded. **Note the append-only rule** in
   that file's line 7: entries are append-only within a review cycle, and a wrong non-equivalence
   claim is corrected *below* the original, not by editing it.
2. **`bioLeak` 0.3.8 / 2026-05-21** → corrects `HISTORY.md` H-34 line 282's "(CRAN, Dec 2025)" and
   flips its §10.1 criterion-5 status to active-within-window. H-34's verdict is unaffected.
3. **The `deepchecks` AGPL fact pattern of §2.3** → the evidence §13.5 says it will decide on.
4. **The outbound gap of §4** → §13.2 remains open and Phase 0 cannot be closed as "licence check
   done" without saying so.

**None of this touches `PREREG.md`.** Every item above is an instance record or a decision, not a
rule: what a licence *is*, what a specific tool *is*, what the author *decided*. The rule — that
licences are recorded and borrows are attributed — is already registered at
`PRIOR_ART_VERIFICATION.md` line 9 and `PREREG.md` line 1089, and needs no amendment.
