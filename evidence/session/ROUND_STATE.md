# ROUND_STATE.md — one-file re-orientation

**Purpose (R36).** After compaction, re-orient from THIS file. Rewrite it every round.

**CURRENT ROUND: R102** (§179–§182). Previous: R101 (dossier), R100, R99.

**STATE: ⛔ HOLDING AT C2.5 (i). NOTHING OPEN THAT IS NOT THE AUTHOR'S.** The only blocker is the
author's review of the F3 fixture manifest. Index reset; nothing committed, tagged, pushed or
stamped.

---

## §0 — THE LEDGER

| # | item | status | last moved | reported in substance |
|---|---|---|---|---|
| 1 | **C2.5 — fixture manifest is DRAFT, and absent from §D.1's freeze list** | ⛔ **HALT — ceremony stopped here** | R97 | R97 |
| 2 | §157 — `80401d0` is the base | ✅ verified from the commit | R97 | R97 |
| 3 | §158 — the pinned-HEAD check replaced by C5b | ✅ DONE, both directions tested | R97 | R97 |
| 4 | §158.5 sweep — other stale-able pins | ✅ 36 found, **2 actionable**, both fixed | R97 | R97 |
| 5 | §158.6 — lesson filed | ✅ **H-L24** | R97 | R97 |
| 6 | v30a applied to `PREREG.md` | ✅ blob `a90896785da528c8` | R93 | R93 |
| 7 | Signing, push, stamp | BLOCKED-ON-AUTHOR | R71 | R96 |
| 8 | §39 · §72.2 · §64/D11 · §139 | OPEN — post-tag/Phase 1 | R93 | `DEFERRED_ITEMS.md` |

---

## §1 — §157: `80401d0` VERIFIED FROM THE COMMIT

| | |
|---|---|
| files touched | **`HISTORY.md` only** — 1 file |
| numstat | **+33 −0** |
| parent | `ffa6d942c97baa9c…` |
| descendant of `prereg-v30`'s commit | **YES** |

**Recorded reason (§157.1):** `80401d0` is H-34's kill-gate sign-off, and under the author's routing
of 25 Aug 2026 (branch (b)) **H-34's verdict IS the sign-off the tag requires**. A tag based on
`ffa6d94` would exclude the record its own routing depends on.

**Correction to R96's report:** I said "exactly one commit landed since". That is true relative to
`ffa6d94`, but the accounting §158.2(b) requires runs from the **tag**, and there are **four**:
`5842857`, `0ee26c4`, `ffa6d94`, `80401d0`. All four are now accounted for.

---

## §2 — §158: DERIVATION AND ACCOUNTING, NOT A FRESHER LITERAL

`# expect ffa6d942…` is **gone**, not updated. In its place, **C5b** in `CEREMONY_COMMANDS.md` §2:
asserts HEAD descends from `prereg-v30`, **enumerates** every commit between, and requires each to
carry an `account:` line in **`evidence/ceremony/COMMIT_ACCOUNTING.md`** giving its hash, what it
did, and why it belongs in the tagged tree. **Unaccounted = HALT. Newly accounted = fine.**

**§158.4 both directions demonstrated:**

- `80401d0` un-accounted → `C5b UNACCOUNTED 80401d0 …` → **exit 1**
- accounting restored **byte-exact**, re-run → all four accounted → **exit 0**

**§158.5 sweep. Population (§30.1):** every line of `CEREMONY_COMMANDS.md` and `COMMIT_PLAN.md`,
looking for resolvable git object ids and `# expect` lines. **No exclusions.** **36 hits.**
**Two were current-state assertions of this class** and both were replaced:
`CEREMONY_COMMANDS.md`'s `HEAD` expectation (→ C5b) and `COMMIT_PLAN.md`'s `| HEAD | ffa6d942… |`
row (→ derived, pointing at C5b). The other 34 are **historical references** — v30's OTS commits,
"tracked at `ffa6d94`", the one-line-subject precedent — correct as history and deliberately
untouched. `prereg-v30 → fe0d5a5…` stays stated: **a tag never moves.**

---

## §3 — ⛔ THE HALT AT C2.5

**Gates that passed, in order:** C5 (remote character-exact; `prereg-v30a` does not exist) ·
**C5b** · staging (662 paths) · **V1b** (nothing outside the intended set) · **C2a** (all six in the
index) · **C2b** (none unstaged) · **C2c** (all six byte-identical, staged vs working tree) ·
**C2d-0** (manifest LF-only) · **C2d-1** (no manifest line without a file) · **C2d** (663 OK) ·
**C2d-2** (three-way agreement on the declaration hash).

**C2.5 FAILED, both conditions:**

| condition | result |
|---|---|
| **(i)** recorded status must not be DRAFT at the tag | **FAILED** — `manifest_status` is `'DRAFT - author review required'` |
| **(ii)** the manifest must be in §D.1's *"Specifically and exhaustively"* freeze list | **FAILED** — `fixture_manifest_DRAFT.json` is not in it |

§D.1 item 3's exhaustive list enumerates the declared ground-truth map, the cohort predicate, the
reference AUC trio, criterion 1's column enumeration, §C.4's declared exclusions, the fixture
identity and pc2 exclusion, and the `floor(t-1)+1s` boundary — **and no fixture manifest.** Both
files on disk are drafts: `f3/fixture_manifest_DRAFT.json` and `t4/fixture_manifest_35col_DRAFT.json`.

**Why it is a HALT and not a nuisance:** C2.5 exists because **SC-4(k2) reads this manifest**. A gate
clause reading a file the declaration never froze, whose own recorded status says it awaits author
review, is the shape the freeze rule exists to prevent.

**Stopped per §153.4, and nothing was left behind.** The index was **reset** — a half-staged index
invites an accidental commit, and §159.1 requires the next run to start from C5 whole anyway.

---

## §4 — VERIFIED STATE

| fact | value |
|---|---|
| `PREREG.md` | blob **`a90896785da528c8…`**, 2,075 lines |
| registration gate | **PASS, 22/22** |
| `evidence/MANIFEST.sha256` | **663 entries, 663 OK** |
| tags | **`prereg-v30` only** |
| HEAD | `80401d0cb819abe4…` — **unmoved** |
| staged files | **0** |
| `v30a.hashes.txt` | **absent — C2 never ran** |

---

## §5 — R99: BRANCH A EXECUTED, MINUS THE AUTHOR'S PART

**§167.1/§167.2 — §D.1's exhaustive freeze list now names the F3 manifest**, pinned by **path AND
SHA-256** `8fd3bb5a771af72d…` / 22,314 bytes, with the reason recorded: SC-4(k2) says in terms that
*"the manifest is an object the gate consumes"*, and F3-not-T4 is settled by this declaration's own
*"Why F3 governs and not T4"* plus t4's `derived_from` field. **C2.5 (ii) now passes.**

**§167.3 — the status is NOT flipped.** `manifest_status` still reads
`DRAFT - author review required`. **C2.5 (i) still fails, correctly**, and the ceremony stays halted.
Review package: `ceremony/F3_MANIFEST_REVIEW_PACKAGE.md`.

**§167.5 — DECISION: KEEP THE NAME.** The path is load-bearing in four places (the §D.1 pin, C2.5's
gate, the evidence manifest line, and the declaration's other citations). SC-4(k2) requires the
**recorded status** not be `DRAFT` — the field, not the filename. Renaming a gate input's identity
immediately before a tag risks every reference to it for tidiness. **The mismatch is recorded in
§D.1** so no reader infers draft-ness from the name.

---

## §6 — §168 / §169: THE THIRD DIRECTION, CLOSED

**D16 registered** — every manifest-attested path is either tracked or in COMMIT_PLAN §4's staging
set. **Known-positive (§169.3): FIRED on `PRACTICES.md` before the fix**; after §168.1 added it to
the staging set, **PASS**. **Negative tests (§169.4): 3/3** — removing it again fires, a bogus
manifest line fires, and an **already-tracked** file correctly does **not** fire. Both files restored
byte-exact.

| file | disposition |
|---|---|
| `PRACTICES.md` | **§168.1 — added to COMMIT_PLAN §4's add-set.** Was attested-but-absent. |
| `PRIOR_ART_VERIFICATION.md` | **§168.2 — no action**, and the reasoning is now recorded at §4 so it is not re-opened: tracked since `ffa6d94`, so the commit inherits it. |
| `LICENSE` | **§168.3 — post-tag**, recorded in `DEFERRED_ITEMS.md` with the Phase 6 wrap / `deepchecks` AGPL interaction. |
| `tools/control_char_scan.py` | **§168.4 — NOT on D10's ephemeral list** (23 entries, none match). D10's domain is the **work root**, not the repo tree, so D10 never asks about it. Untracked, unattested, unlisted — see §7. |

---

## §7 — R101/R102: THE MANIFEST VERIFIED, AND WHAT PINS ITS MEANING

**R101 — the dossier.** `ceremony/F3_MANIFEST_VERIFICATION.md`. All 35 columns located in the
producing code: 21 direct assignments, 12 loop-constructed, **2 raw source columns read from the
snapshots parquet and never assigned** (`bid_size_1`, `ask_size_1`). Nothing unlocated.

**R102/§179 — the operative rule restated, no classification changed.** The manifest's stated rule
was raw-vs-derived inputs; its **operative** rule is **INDEPENDENCE OF PATH**. Verified across **all
35 before writing it: 0 disagreements.** Both rules are now recorded in `classification_basis`, with
why the second governs — raw-vs-derived agrees today **only** because `bid_size_2..5` are
unclassified, and would misclassify a derived-but-unclassified input.

**A first pass reported 4 disagreements. They were my input-inference, not the manifest** — it mapped
`bid_cols` to `bid_size_1` alone, missing the `2..5` ladder. Corrected before reporting anything.

**R102/§180 — what pins the manifest's MEANING.** §D.1 pinned the manifest's bytes; the meaning rests
on `phase7_l2_sim.py`, which nothing pinned. Now pinned beside it: sha256 `c659d3ac167a13af…`,
**949 lines, 41,745 bytes**, archive-resident, **not in the repository** — hash re-derived, not
copied. D-ARCHIVE gained its own sentence. Bringing the file in is recorded **post-tag and
RECOMMENDED** (~41 KB makes the 35 classifications independently verifiable).

**R102/§181 — both checks resolve, neither stops.**

- **§181.1:** `td = snap["total_bid_depth"] + snap["total_ask_depth"]` (l.171), and
  `depth_change_{lag}s = td.diff(lag)` (l.181). **Both parents are correct; the record is right.**
- **§181.2:** `ALL_L2_FEATURES = L1_FEATURES + L2_FEATURES  # 35 total`, and the model's set
  **equals the manifest's 35 exactly**. **No exempt `raw_book_col` is a model feature** — `spread`
  and `book_imbalance` are exempt raw columns; the *features* are `spread_ticks` and
  `book_imbalance_ratio`, different columns. **No coverage gap.**

---

## §8 — THE LEDGER

| # | item | status | whose |
|---|---|---|---|
| 1 | **F3 manifest SIGN-OFF** — verification done and shown | ⛔ **sign-off only** | **AUTHOR** |
| 2 | Signing, push, OTS stamp | BLOCKED | **AUTHOR** |
| 3 | §39 · §72.2 · §64/D11 · §139 · LICENSE · §173 · **§180.4** | recorded, post-tag / Phase 1 | later |

**Status still `DRAFT - author review required`. Nothing staged, committed, tagged, pushed or
stamped.**
