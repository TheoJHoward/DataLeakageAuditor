# R66 §1.3 — THE SHIP-CRITICAL COUNT, PRODUCED BEFORE ANY FIXING

**Test applied (R66 §1.1).** Ship-critical **iff both**: **P1** it ships — inside the six-file hash
set, the tag-message body, or carrying an `evidence/MANIFEST.sha256` entry; **and P2** it is
load-bearing — a reader relying on it reaches a wrong conclusion about (i) what a gate tests,
(ii) a threshold/count/denominator, (iii) a pass/fail condition, or (iv) what an amendment changed.
**Reliance, not confusion** (§1.2).

**P1 verified from the manifest**, not assumed: `ceremony/CEREMONY_COMMANDS.md`,
`ceremony/COMMIT_PLAN.md`, `ceremony/DEVIATIONS_DRAFT.md`, `ceremony/H34_DRAFT.md`,
`author_review/READ_THROUGH_PACKAGE.md`, `../PRACTICES.md`, `../PRIOR_ART_VERIFICATION.md` all
carry entries. The six-file set is `PREREG.md`, `DESIGN.md`, `HISTORY.md`,
`tools/check_registration.py`, `protocol/runtime_reference.py`, `AVAILABILITY_DECLARATION.md`.
Anything under `scratchpad/` that is not applied text **fails P1**.

---

## SHIP-CRITICAL (P1 ∧ P2)

### R23 — hash-count literals (§2.3 names these in scope regardless)

Executed at tag time; a wrong count is a wrong gate. **P2(ii) on every one.**

| # | site | why load-bearing |
|---|---|---|
| 1 | `AVAILABILITY_DECLARATION.md:3589` | states a hash count as a literal |
| 2 | `AVAILABILITY_DECLARATION.md:3602` | §D.2's **SIX hashes** literal |
| 3 | `AVAILABILITY_DECLARATION.md:3607-3617` | the enumeration behind the literal |
| 4 | `AVAILABILITY_DECLARATION.md:3622-3626` | ditto |
| 5 | `AVAILABILITY_DECLARATION.md:993` | count restated |
| 6 | `AVAILABILITY_DECLARATION.md:3811` | count restated |
| 7 | `AVAILABILITY_DECLARATION.md:3833` | count restated |
| 8–14 | `evidence/ceremony/CEREMONY_COMMANDS.md:151, 154, 175-181, 189-191, 360-361, 371, 433` | **the executed ceremony steps** |
| 15 | `evidence/ceremony/COMMIT_PLAN.md:346-395` | staging/hash enumeration |
| 16 | `evidence/ceremony/DEVIATIONS_DRAFT.md:262` | count in a filed deviation |

### R9 / R11 — what criterion 3 tests, and the denominator

| # | site | why |
|---|---|---|
| 17 | `PREREG.md:478` ≡ `_E3_composed_sections.md:434` | states criterion 3 as a **silence test**; false under SC-3. §2.1. |
| 18 | `AVAILABILITY_DECLARATION.md:663-664` + `:652` | allocates criteria 1–4 to an artifact with no feature columns |
| 19 | `AVAILABILITY_DECLARATION.md:3684-3686` | per-side criterion enumeration, **omits criterion 1** |
| 20 | `AVAILABILITY_DECLARATION.md:2936` | describes criterion 3's pre-R9 behaviour |
| 21 | `AVAILABILITY_DECLARATION.md:1322` | ditto |
| 22 | `AVAILABILITY_DECLARATION.md:2840` | ditto |
| 23 | `_E3_composed_sections.md:426` (≡ `PREREG.md:470`) | denominator description pre-R11 |

### Y1 / R1 / R2 / R16 — class set, ties, boundary, disposition

| # | site | why |
|---|---|---|
| 24 | `AVAILABILITY_DECLARATION.md:1565-1566` | class-set / count |
| 25 | `AVAILABILITY_DECLARATION.md:2309` | class-set / count |
| 26 | `AVAILABILITY_DECLARATION.md:2165-2168` | **false clean** — cross-class quantity without its class set |
| 27 | `AVAILABILITY_DECLARATION.md:499`, `:531`, `:531-534`, `:555` | what counts as a violation at equal timestamps |
| 28 | `evidence/ceremony/DEVIATIONS_DRAFT.md:55` | the measured boundary, in a filed deviation |
| 29 | `evidence/ceremony/DEVIATIONS_DRAFT.md:176-179` | `book_imbalance_ratio` disposition |
| 30 | `evidence/ceremony/H34_DRAFT.md:97`, `:115`, `:185` | kill-gate sign-off draft, R16 disposition |
| 31 | `evidence/ceremony/COMMIT_PLAN.md:113-118` | ditto |

### SC-13 / SC-12(w) / Z1 — gate text and what the amendment changed

| # | site | why |
|---|---|---|
| 32 | `evidence/ceremony/CEREMONY_COMMANDS.md:340-341` | **the tag-message body**, misdescribing SC-12(w). §2.2. |
| 33 | `evidence/ceremony/CEREMONY_COMMANDS.md:79` | amendment description |
| 34 | `evidence/ceremony/DEVIATIONS_DRAFT.md:44-49` (FILLED at `:284`) | D-001's "amended sections" |
| 35 | `evidence/ceremony/COMMIT_PLAN.md:406-408` | amendment description |
| 36 | `evidence/ceremony/H34_DRAFT.md:165-178` | amendment description |
| 37 | `SCHEMA_SET_FINAL.md:1355-1360` vs `:1459-1460` | SC-13 applied text, internally divergent |
| 38 | `_E3_composed_sections.md:855-961` | the composed rendering of the above |
| 39 | `AVAILABILITY_DECLARATION.md:1668`, `:1689-1693`, `:3568-3572`, `:3798` | `waived` described as a word, not a prohibition with an entry condition |
| 40 | `SCHEMA_SET_FINAL.md:1462-1465`/`:1610`, `:2174-2178` | ditto, applied text |
| 41 | `evidence/ceremony/DEVIATIONS_DRAFT.md:47-48` | ditto, filed deviation |
| 42 | `evidence/ceremony/COMMIT_PLAN.md:170` | Z1 / criterion-5 consequence |

**SHIP-CRITICAL COUNT: 42** (conservatively grouped; counting each cited line separately gives ~57).

---

## NOT SHIP-CRITICAL

| site | fails which prong |
|---|---|
| `HISTORY.md:56` (H-09) | **P2** — narrative of a past firing; nothing relies on it for a gate outcome |
| `evidence/author_review/READ_THROUGH_PACKAGE.md` (whole corpus, 4 amendments) | **P2** — it is the author-read baseline, expressly frozen at `2e23f1f2` and superseded by the CHANGED-SINCE-READ deltas; nothing decides a gate from it |
| `PRACTICES.md:140-144`, `:318` | **P2** — non-normative practices prose |
| `scratchpad/ceremony/*` (CEREMONY_COMMANDS, DEVIATIONS_DRAFT, H34_DRAFT, X4, DEVIATIONS_D003_DRAFT) | **P1** — scratch twins, not manifested, not staged |
| `scratchpad/errata/HISTORY_L5_R26_FIRING_STAGED.md` | **P1** — scratch |
| `evidence/fixture_spike/_snapshots/…PRE_R9.md` | **P2** — an explicitly dated pre-R9 snapshot; describing pre-R9 behaviour is its purpose |
| `amendment/PREREG_v30a_DIFF.md:458`, `:464` | **P1** — superseded drafting source, not applied |
| `X5_CRITIQUES.md`, `README.md`, `tagmsg.txt` mentions | not stale sites — citation noise from the extraction |

---

## §1.3 VERDICT: **THE SCOPE GUARD TRIPS.**

**42 > 25.** Option (1) has collapsed into option (2). Per §1.3 this is the author's ruling to
revisit and **not mine to absorb silently**, so nothing has been fixed and this document is the
report.

**Why it exceeds the threshold, in one line:** R23's hash-count literals alone are **16**
ship-critical sites, and §2.3 puts every one of them in scope — the count is not driven by the
described-object errors but by one rule being restated as a literal in sixteen places, seven of
them inside the ceremony's executed steps.

**Nothing was fixed. `PREREG.md` untouched. No evidence artifact amended. No content adjusted
toward a hash.**
