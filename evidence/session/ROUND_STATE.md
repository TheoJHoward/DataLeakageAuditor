# ROUND_STATE.md — one-file re-orientation

**Purpose (R36).** After compaction, re-orient from THIS file. Rewrite it every round.

**CURRENT STATE: R134. Track A is ⛔ HALTED at A19″ on a derivation, not a question.** `main` is at
`87054020278eca99a09164a4bb3e11bf20620878`, clean, tags `prereg-v30` only; `PREREG.md` is byte-exact
at `0c8da19f237cd243…`; held banking is preserved in `stash@{0}`. Nothing has been committed,
tagged, pushed or stamped. **`main`'s gate is 23 checks, RESULT FAIL** — `round_reconciliation`
(D10), mechanism at RE-1 below, and it must be green before A17‴.

**Track A cannot advance past A19″ without an author ruling.** Three findings, any one of which is
a halt on its own: the tag message names three §6.2 changes that are not in the file it hashes
(F1); §7.7's detector-case coverage row is deleted and nothing re-registers it (F2); and the
amendments block §1.1 asks me to insert asserts that no registered sentence is deleted (F2 again,
from the other side).

**Track B runs on branch `phase1` and waits on none of it.** `phase1` at `7e8b902`;
`tests/phase1` 113 passed / 4 skipped, whole suite `tests/` 250 passed / 4 skipped.

**THIS FILE IS THE REPORT.** Each item is banked here when it completes, before the next begins.
A record that lives only in a chat message dies with the turn, and a turn that ends mid-item then
costs a full relay to reconstruct a state that was already on disk.

---

## §0 — THE LEDGER

| # | item | status | last moved | reported in substance |
|---|---|---|---|---|
| 1 | **C2.5 — fixture manifest DRAFT + absent from §D.1** | ✅ CLEARED — author sign-off 26 Aug 2026; §D.1 pins it by path and bytes | R99 | R99 |
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
**949 lines, 41,745 bytes** — hash re-derived, not copied. **The file is now IN THE
REPOSITORY** at `evidence/fixture_spike/f3/phase7_l2_sim.py`, verified at the destination
against that pin and hashed in the tag message; the 35 classifications are independently
verifiable from the repository alone. D-ARCHIVE is deployed at `AVAILABILITY_DECLARATION.md`
§D.6 and now states the narrower true position: the derivation can be audited from the
repository, the inputs it consumed remain external, so it cannot be re-executed there.

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

---

# v30a CLOSEOUT — ITEM RECORD

## A0 — STATE DISCOVERED

| | |
|---|---|
| branch / HEAD | `main` at `3257f07752a352ac4c56e595f8bd1caebc7bf857` |
| tags | `prereg-v30` only — **no tag exists**, so A0 does not halt |
| committed this round | **nothing** |
| unstaged diff | **EMPTY** — the A5 gate's precondition holds |
| staged | 13 files, +2442 −175 |
| declaration | §D.1–§D.6 present, verified **by reading** |
| exemption tables | already **anchor-keyed** — `('AVAILABILITY_DECLARATION.md', 'prereg-v30 tag message (five SHA-256 lines')` |

**Entering at A4.1.** A4.2's conversion (11 anchored, 3 deleted) landed last round;
what A4.2 still owes is the DEMONSTRATION of the three deletions.

---

## A4.1 — THE 3715 REWORD: TEST APPLIED, REWORD STANDS

**The test.** Can a reader of the signed object alone reconstruct why six was
wrong and twenty is right?

**Yes, and the reword did not remove the superseded basis.** The paragraph names
both sources of the old SIX — working resolution R7, and §0.2.1 line 97's
quantifier — and then quotes item 8 verbatim. **Item 8's own quotation names the
retired basis WITH its count:** *"item 3's three names, §0.2.1 line 97's 'both'
— it records the set at the time of its writing, stands as that record, and is
superseded as the set by this item."*

So the count that was removed from the surrounding prose is still present in the
authoritative place: inside the clause that does the superseding. The chain a
reader needs — old set, its two grounds, the clause that retires them, the three
limbs, the enumeration table, twenty — is complete without the separate
quotation. **A4.1 branch 1: the reword stands.**

**One defect found and fixed while applying the test.** The reword had joined two
paragraphs: `dispositioned at their own sites.` ran directly into `**Item 8 names
both of those…**` with no blank line, so markdown rendered them as one block.
Blank line restored. CRLF uniform after the fix.

---

## A4.2 — EXEMPTIONS: 11 ANCHORED, 3 DELETED AND DEMONSTRATED

**Converted (landed last round, verified by reading this round).** Keys are now
`(path, anchor text)`; no line number remains in the source. `_HASH_SET_EXEMPT`
9 -> 7, `_HASH_SET_ENUM_EXEMPT` 5 -> 4.

**Deleted, with reasons.** All three anchors lived in the §D.2 the enumeration
rewrite replaced:

| deleted anchor | was exempt for | why deleted |
|---|---|---|
| `The \`prereg-v30\` tag message carries` | value 5 | sentence replaced; the replacement states no count |
| `signed tag, both file hashes in the tag message` | value 2 | the §0.2.1 l.97 quotation was removed from the surrounding prose (A4.1); item 8's own quotation carries it and does not fire |
| `covering \`PREREG.md\`, \`DESIGN.md\`, \`HISTORY.md\`...` | the executed v30 five | the enumeration was replaced by the three-limb table |

**DEMONSTRATED, because a deletion is invisible in a green gate.** If the sentence
an exemption covered is gone, the check has nothing to fire on either way, and
"no finding" looks the same whether the exemption was load-bearing or decorative.
Each deleted exemption's original sentence was put BACK into the declaration and
the detector had to fire on it:

| case | result |
|---|---|
| D5 / value 5 — the v30 count statement | **FIRED, unexempt** |
| D6 / value 2 — the line 97 verbatim quotation | **FIRED, unexempt** |
| D6 / enumeration — the executed v30 five | **FIRED, unexempt** |

Declaration restored byte-exact after each. **Each deleted exemption was
suppressing a real detection**, so its removal is meaningful rather than tidying.

The inverse holds too and is what makes the deletions safe: the text that replaced
each sentence does not fire — the gate reports one D1 finding, and it is the
legitimate 20-vs-6 that A5 resolves.

---

## A4.3 — THE D-STALE REFERENCE NOW RESOLVES

`AVAILABILITY_DECLARATION.md:1660` cites the **LABEL** `D-STALE`, not a section
number: *"The line is handled instead by **specific disclosure at D-STALE**, by
line and by quotation."*

§D.6 carries that label at l.3971 — `**D-STALE — the stale-description class,
stated as a FLOOR.**` **A4.3 branch 1: it resolves, and no citation is edited.**
Because the reference is by label rather than by number, it survives any later
movement of §D.6 within the file — which is the same property the exemption
anchors now have.

Two further references resolve as a side effect: §D.6's own introduction quotes
the l.1660 sentence (l.3917), and D-INSTRUMENT item 3's *"(see D-STALE)"*
(l.4062) now points at text that exists.

**This was the defect that made the disclosure deployment necessary rather than
merely prudent** — a registered file asserting that a known-false sentence "is
handled" by a disclosure that did not exist.

---

## A4.4 — THE THREE CITING RECORDS

| record | kind | treatment |
|---|---|---|
| `evidence/ceremony/F3_MANIFEST_VERIFICATION.md` | dated evidence record | **SUPERSEDED** by a dated entry above the warning. The warning is retained unedited — it was true on its date. |
| `evidence/session/DEFERRED_ITEMS.md` | live working record | updated in place; the item is marked DISCHARGED with its date |
| `evidence/session/ROUND_STATE.md` | live working record | updated in place |

**The scope collision is now stated rather than left to be inferred.** The
`D-ARCHIVE` draft said *"The producing code IS committed"*; the F3 verification
said *"THE PRODUCING CODE IS NOT IN THE REPOSITORY"*. **Both were true — of
different sets:** the first of the three spike producers, the second of
`phase7_l2_sim.py`, which was not among them. Nothing anywhere said they were
speaking about different sets, so the pair read as a contradiction. It was not
one, and it is no longer live either way.

---

## A4.5 / A4.6 — INSTRUMENTS IN, REPORT FOLDED, EVERYTHING STAGED

Ten build instruments from this closeout are in `evidence/amendment/` with
manifest entries, hashes computed from disk. §187's alternative — a D10 ephemeral
line — would have been inert: **D10's `_WORK_ROOT` names a different session's
scratchpad**, so a line for a file in the current one exempts something D10 never
looks at. That gap is recorded separately below.

Staged: **18 files**. Unstaged diff **EMPTY**, which is A5's precondition — C2
reads the index, so a modified-but-unstaged file would be hashed at its old
content and the tag would attest bytes that are not in the tree.

`tools/control_char_scan.py` remains untracked, deliberately: its own ephemeral
entry says committing it changes what ships.

---

## A5 — FILES GROWN TO TWENTY; THE BLAST RADIUS, DERIVED

`FILES` in `CEREMONY_COMMANDS.md` §3.2 now carries the twenty paths item 8
defines. Order is **not** alphabetical and must not be made so: the `prereg-v30`
five come first in the v30 order, so the v30 block stays a verbatim prefix and no
v30-era verification instruction is invalidated.

**Every restatement that now disagrees was named by the gate, not by a grep.**
Twenty findings, reported here before any of them is edited:

| check | sites |
|---|---|
| **D1** — states 6, authority says 20 | declaration l.1008 · `CEREMONY_COMMANDS.md` l.625 · `COMMIT_PLAN.md` l.459 · `DEVIATIONS_DRAFT.md` l.262 |
| **D2** — enumeration is not the set | declaration l.3707 (the limb-1 table row) · `DEVIATIONS_DRAFT.md` l.263 · `CEREMONY_COMMANDS.md` §3.5's tag-message body |
| **D3 / D4** — staging plan | `COMMIT_PLAN.md` §4's add-set omits `PARKING_LOT.md`, `VALIDATED_CONFIG.toml` and the eight `tests/registration/` files; the plan never names them |
| **D7** — stale declaration hash | `README.md` l.59 · `DECLARATION_POINTER.md` · `F3_MANIFEST_VERIFICATION.md` l.21 |
| **D8** — drifted line citations | `CEREMONY_COMMANDS.md` l.268 (moved by the FILES edit) · `HISTORY.md` l.275 → 277 · declaration l.4008 → 4294 |
| **D10** | three working files in neither the repository nor the ephemeral list |

**One of the D7 hits is a mis-attribution, not a stale value.**
`F3_MANIFEST_VERIFICATION.md` l.21 is read as stating the declaration's sha256,
but the hash on that line is `phase7_l2_sim.py`'s, sitting near the declaration's
name in the supersession note added at A4.4. The value is correct for what it
names; the parser attributed it to the wrong file.

**Nothing in this list has been edited.** The repair is the next item.

---

## OPEN — FOR THE AUTHOR

**D10's population is a session directory that is no longer the working one.**
`tools/check_registration.py` pins `_WORK_ROOT` to one session's scratchpad; the
work now happens in another. Every file created this round is outside D10's
domain, including the instruments that edited registered files. D10 prints
*"every working file is in the repository or declared ephemeral"* while not
looking at the directory the work happens in — which is the instrument-domain
failure the project's own review lessons record, occurring in the check that
exists to catch it.

**Recommended: disclose, do not re-pin.** Re-pinning to the current session
reproduces a stale literal that detaches at the next session; deriving the
directory is a design change to a registered tool under a tag deadline. A sixth
entry in D-INSTRUMENT plus the substance in `DEFERRED_ITEMS.md` fits the closeout
test; the code change does not.

---

## A5.1 — D10 DISCLOSED AS D-INSTRUMENT (6)

Appended to §D.6 in the register form of the other five. The closing sentence is
the D-STALE construction and is load-bearing: **it states what the check does not
REACH and refuses to imply an extent.** A disclosure claiming to enumerate what
was missed would assert a completeness it cannot have, because the check never
looked.

The lead-in was corrected from "Five remain open" to "Six" in the same edit — a
sentence that enumerates its own list and then disagrees with it is the
reconciliation defect the review lessons already record.

`DEFERRED_ITEMS.md` carries the fail-loud redesign **with its substance**, flagged
as the first post-tag item: derive the population rather than pin it; exit
non-zero when the population is empty or its root is absent; print the population
beside the verdict. Known-positive stated: point the check at a directory that
does not exist and at one that is empty, and require non-zero for both.

---

## A5.2 — C2 OVER THE GROWN SET: 20 LINES

The A5 gate held — `git diff --stat` empty before C2, so the index and the tree
agreed and C2 could not hash a superseded version.

`FILES` was read from its authority, not typed: 20 paths. `v30a.hashes.txt`
regenerated, 20 lines. `DEVIATIONS.md` hashes to the sha256 of the empty string,
which is correct — it is 0 bytes and an empty file still has a hash.

---

## A5.3 — IN PROGRESS: 16 SITE GROUPS, ORDER FIXED BY DEPENDENCY

Three of the sites live in `tools/check_registration.py`, which is itself one of
the twenty hashed files. **Editing it after C2 would invalidate C2's own output**,
so the order is: repair every content site, then batch the checker edits, then
re-stage and re-run C2 once, then A6/A7 from the fresh hashes.

| group | disposition |
|---|---|
| declaration l.1008 "§D.2's sixth hash" | reword — the declaration is no longer an ordinal in a set of six |
| declaration l.3707 limb table | **exemption**, not reword: the limb split is the point of the table, and it is deliberately not the set in order |
| `CEREMONY_COMMANDS.md` l.625, §3.5 body | reword; the format block's hash slots grow to twenty |
| `COMMIT_PLAN.md` l.459 "CLOSED as SIX" | **supersede**, not rewrite — it records a decision that item 8 has since displaced |
| `COMMIT_PLAN.md` §4 add-set, plan naming | extend to the new paths |
| `DEVIATIONS_DRAFT.md` l.262–263 | update to the set |
| `F3_MANIFEST_VERIFICATION.md` l.21 | **reword** — see below |
| `DECLARATION_POINTER.md`, `README.md` l.59 | from `v30a.hashes.txt` only |
| three D8 citations | re-derive from content; registry and citing prose both |
| D10's three files | stale scratchpad copies of files that now live in the repository, plus one licence draft |

**The D7 mis-attribution is NOT the last-resort case.** `F3_MANIFEST_VERIFICATION.md`
l.21 sits inside the supersession note added this round — new text, not a frozen
dated record in rule 10's sense. So §187's first resort is available: reword so
the hash and the filename it belongs to are unambiguously adjacent. The exemption
route is not taken.

---

## A5.3 — CONTENT AND CHECKER SITES REPAIRED: 20 FINDINGS DOWN TO 5

**D1, D2, D3, D4 and D10 are all clear.** What remains are five sites that cannot
be repaired yet, because each carries a value derived from the declaration and the
declaration is not final until A6 decides whether §146.2's frame must be extended.
Repairing them now and editing the declaration after would invalidate every one —
the same trap the ordering note warns about.

| repair | disposition |
|---|---|
| declaration l.1008 | reworded — the declaration is no longer "§D.2's sixth hash" |
| `CEREMONY_COMMANDS.md` l.625, §3.5 slots | reworded; the format block's hash slots grew from six to the twenty |
| `COMMIT_PLAN.md` §6 | **SUPERSEDED, not erased.** The closure that set SIX stands as the record of what was decided; item 8 now defines the set by rule. `PRIOR_ART_VERIFICATION.md` stays out — by rule now, not by that judgement |
| `COMMIT_PLAN.md` §4 | the eight `tests/registration/` files and the three evidence paths named **file by file**. A prefix satisfies the staging check but not the plan: the plan is also the record of which paths the tag attests, and a path covered only by a directory sweep is named nowhere a reader can check |
| `DEVIATIONS_DRAFT.md` l.262–263 | points at the `FILES` authority instead of restating a count |
| `F3_MANIFEST_VERIFICATION.md` l.21 | **reworded** — §187's first resort was available |
| checker: licence draft | ephemeral entry with its reason — the committed `LICENSE` is on the Phase 1 branch, so on this branch the draft has no content twin and the check cannot reconcile it by hash |
| checker: limb table | **exemption** — see below |
| two stale scratchpad copies | synced to the repository versions they are copies of |

**The limb table is the genuine last-resort case, and the reason is recorded as
such.** §D.2 enumerates the set BY LIMB, showing which limb of item 8 admits each
path. That breakdown is the section's argument — the set is not a list someone
chose, it is what three stated rules produce. Flattening it into the set in order
would satisfy the enumeration check and delete the reason the enumeration is
there. §187's first resort was available and was rejected on that ground, which is
different from it being unavailable.

**The D7 mis-attribution was NOT the last-resort case.** The line sits in the
supersession note added this round — new text, not a frozen dated record — so the
reword was available and was taken.

### Remaining, in dependency order

1. **A6** — decide the tag-message line-reference frame. If §3.5's block is fixed
   prose, §146.2 is extended in the declaration, which changes its bytes.
2. Re-derive the three D8 citation line numbers by locating their anchors.
3. `DECLARATION_POINTER.md` and `README.md` from `v30a.hashes.txt`.
4. Re-stage, re-run C2 — the declaration's hash is one of the twenty.
5. A7, A8, A9.

---

# R134 — RE-ENTRY, A19″ DERIVED AND HALTED, TRACK B

## RE-ENTRY — §0 WAS STALE IN TWO PLACES, AND ONE OF THEM IS A FINDING

| §0 claim | actual | verdict |
|---|---|---|
| `main` at `8705402…`, clean tree, tags `prereg-v30` only | same | ✅ |
| `PREREG.md` byte-exact at `0c8da19f…` | same | ✅ |
| held banking in `stash@{0}` | present | ✅ |
| `phase1` at `7e8b902` | same | ✅ |
| **Track A gate PASS 23** | **23 checks, RESULT FAIL — `round_reconciliation` (D10)** | ❌ **stale** |
| Track B "113 tests, 4 skipped" | `tests/phase1` **113 passed, 4 skipped**; the whole suite `tests/` **250 passed, 4 skipped** | ⚠️ true of a subset, stated without its domain (§39) |

**RE-1 — D10 cannot be green on two branches at once, and clearing it on one breaks the other.**
`check_round_reconciliation` reconciles every work-root file against the **checked-out tree** by
content hash. Three round records live on both branches with different bytes —
`ROUND_STATE.md`, `DEFERRED_ITEMS.md`, `ceremony/COMMIT_ACCOUNTING.md`. The work root can be
byte-identical to at most one branch's copies, so D10's green is a statement about which branch
is checked out, not about whether the round is reconciled.

**RE-2 — B8.3's D10 fix cleared the check by syncing the work root to the OLDER copies.** Derived,
not asserted: `main`'s three records were last written at `d39643e` / `8705402` (26 Aug); `phase1`'s
at `0acab4e` / `32dd31b` (25 Aug). The lines `phase1` carried and `main` did not are **9 in
`ROUND_STATE.md`** (an `R102` header, a `C2.5 HALT` ledger row) and **4 in `DEFERRED_ITEMS.md`**
(describing `phase7_l2_sim.py` as *"not in the repository"* — it has been in the repository on
`main` since `8705402`); `COMMIT_ACCOUNTING.md` carried **0**. Every one of the thirteen is
superseded text. **D10 went green on `phase1` while the work root held a state one round behind,
and a guard that passes for the wrong reason is worse than one that fails (§2.4).**

**Resolved, PROVISIONAL (§2.6).** `phase1` adopts `main`'s three records verbatim — a supersession
with nothing lost, demonstrated above — so the three files are single-valued across both branches
and the work root, and D10's green means what it says. The alternatives were to leave the split
(which hides which copy is current) or to re-sync the work root to whichever branch is checked
out (which makes D10 vacuous). Nothing registered changes and no amendment meaning is decided;
`main`'s copies come level at A17‴, which rewrites them anyway.

---

## A19″ — THE AMENDMENTS BLOCK, DERIVED. ⛔ HALT.

`PREREG.md` untouched at `0c8da19f237cd243…`. Nothing staged or committed on `main`. No assembly
was written: §1.1's derivation reached a halt branch before the block could be assembled.

### §1.1(a) — §8.2's columns and its grouping key, reported before anything is derived

`K2_AMENDMENT_LEDGER.md` §8 is titled ***"THE v30a AMENDMENTS BLOCK TEXT — ENUMERATION-FIRST,
NUMERAL-FREE (replaces H1a and H1b; keeps §AB)"***. Its block, delimited `<!-- K2-BLOCK-BEGIN -->` /
`<!-- K2-BLOCK-END -->`, is **four enumerations, not one table**:

| group | heading | grouping key | columns |
|---|---|---|---|
| (a) | Registered text superseded | one row per registered surface, `§X.Y line N` in **pristine v30** numbering | surface · touch · operative text/clause · class · justification |
| (b) | Standing byte-exact, reading extended by a marker | same key | surface · what the marker states · clause · class |
| (c) | New clauses inserted | insertion site, `§X.Y after line N` | site · clause · what it registers · class · justification |
| (d) | Pointers | prose, semicolon-separated | — |

**§1.1(b) and (c) are already satisfied by §8.2, and the drafted six-row table is not its table.**
§8 replaces H1a and H1b in terms. Its own framing says *"Every count in it is read from its own
enumeration — adding a clause adds one row to (a), (b), (c) or (d) and changes no sentence"*, and
its closing paragraph states the population and the reading rule: *"the registered lines this
amendment supersedes are those in (a) and no others … **Their number is read from the enumeration
and is stated nowhere as a numeral**"*. **So SSF open-item (b) — the six-row undercount — is a
defect of the DIFF's H1a/H1b, and K2 §8 is the fix that was already written for it.**

### §1.1(b) — DERIVED AGAINST THE APPLIED FILE. Eleven of thirty-seven touches are not there.

Derivation, not assertion: `a19_derive.py`, three independent probes per row, reported separately
and never collapsed.

- **P1 RECORD** — `SCHEMA_RECORDS.json` carries a record whose `prereg_line` is the row's v30 line.
  That JSON is what `generate_prereg_diff.py` reads; **a surface absent from it was never offered
  for approval.**
- **P2 MARKER** — the applied `PREREG.md` carries a v30a marker citing that surface by v30 line.
- **P3 TEXT** — (a) rows only: whether v30's sentence at that line is still standing in the applied
  file, and whether anything marks it.

Population asserted first: **(a) 9 · (b) 10 · (c) 14 · (d) 4 = 37 enumerated touches**; 23 records
in `SCHEMA_RECORDS.json`; **23** `<!-- v30a … -->` markers in the applied `PREREG.md`.
*(The instrument's (d) parse over-splits on semicolons inside parentheses and prints 6; the four
pointers were read by hand and all four are applied. The over-split is recorded, not hidden.)*

| group | applied | NOT in the file |
|---|---|---|
| (a) superseded | **5** — §6.2 l.461, §7.7 l.855, §8.3 l.929, §10.1 l.1022, §10.2 l.1030 | **4** — §6.2 l.445, §6.2 l.450, §6.2 l.451, §10 l.992 |
| (b) marker | **3** — §6.2 l.480, §7.2.1 l.816, §8.2 l.915 | **7** — §0.2.1 l.97, §2.3 l.205, §2.4 ll.220–222, §6.1 l.431, §6.2 l.459, §11 item 3 (l.1050), §11 items 1–7 |
| (c) inserted | **14** | 0 |
| (d) pointers | **4** | 0 |
| **total** | **26** | **11** |

**Reverse direction, so the enumeration is checked both ways: all 23 records land on an enumerated
row.** Nothing was applied that §8.2 fails to name. The gap runs one way only.

**Why P1 alone would have lied.** (a)'s §6.2 line 451 row matches record `SC-2` on P1 — but SC-2 is
an `INSERT_AFTER` at 451, not a supersession, and P3 finds v30's line 451 still standing **unmarked**
at applied l.580. The row says *"superseded — retained verbatim at its site, NOT operative"*; the
line is operative and unmarked. One probe would have scored it applied.

### F1 — THE TAG MESSAGE ADVERTISES THREE CHANGES THAT ARE NOT IN THE FILE IT HASHES

`tagmsg.txt`, lines 3–5, verbatim: *"Amends `PREREG.md` §6.2 — **reference AUC (l.445)**,
**contamination availability class recording locus (l.450)**, **sliced CI variant (l.451)**,
criterion 3 (l.461) — and defines "waived" for §10.2's replacement-criterion floor."*

Of those four, **only l.461 is applied.** v30's lines 445, 450 and 451 stand byte-identical in
`PREREG.md` at lines 574, 579 and 580, unmarked and operative — verified by reading them out of
`git show prereg-v30:PREREG.md` and comparing, not by any gate.

`PREREG_v30a_APPROVAL.diff` — the diff generated from `SCHEMA_RECORDS.json` — has **15 hunks and
exactly 5 removal lines** (v30 ll. 461, 855, 929, 1022, 1030), matching `APPROVAL_PACKAGE.md`'s
`+981 −5`. **The three §6.2 replacements were never in the approved record set at all.** They exist
only as `PREREG_v30a_DIFF.md`'s H2, H3 and H4, alongside H1a and H1b — the same drafting file, the
same never-applied fate. §10 line 992's supersession (H29/H30) is the fourth of the same kind: the
string `SUPERSEDED BY v30a` occurs **once** in the whole applied file, at l.1678, and that is
§10.1's C2 retention block.

**This is not the amendments-block question.** The block is a record OF the amendment; these are
the amendment. A tag message naming three changes a reader will not find in the hashed file is a
false statement inside the signed object, and it is independent of anything §1.1 assembles.

### F2 — §7.7's DETECTOR-CASE COVERAGE ROW IS DELETED, AND NOTHING RE-REGISTERS IT

v30 line 855, verbatim:

```
| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |
```

**`Detector-case coverage` occurs nowhere in the applied `PREREG.md`.** §8.2's (a) row for this
surface says *"superseded: **the row is re-registered with `unscored`**"*. It is not re-registered.
`SC-6a`'s `REPLACE_ROW_THEN_INSERT` removed it and inserted the clause; the replacement row was
never written.

This is a registered sentence **deleted** from the file — which §8.2's own item 1, the text §1.1
asks me to insert, states cannot have happened: *"**No registered sentence is deleted from this
file.**"* Inserting that sentence over this file would register a false assertion.

Two structural consequences, from a differential scan against v30 (§2.3 run rather than recalled):

| damage | v30 | applied | introduced |
|---|---|---|---|
| **T1** table header + separator with **no body row** | 0 | 1 | **1** — `\| Level \| States \|` at applied l.1380 |
| **T2** orphaned pipe row (renders as a paragraph, not a table row) | 17 | 18 | **1** — `\| **Strategy diagnostic** \| …` at applied l.1417 |
| **S1** `---` flush against a paragraph (setext heading underline) | 0 | 0 | 0 |

So §7.7's *"two levels"* table now has **zero rows**, and the surviving `Strategy diagnostic` row
sits 35 lines below its header behind two blank lines, where markdown renders it as literal text.
Meanwhile applied l.1544 still reads *"every detector-case coverage state **that row** carries other
than `passed` and `failed`"* — a citation to a row that no longer exists. **S1 fired nowhere: the
setext hazard §2.3 was written for did not recur, and that is reported because a rule proven clean
is worth as much as one proven violated.**

### F3 — THE APPLIED TEXT DESCRIBES ITS OWN MISSING HALVES, IN ITS OWN WORDS

Not inferred — quoted from `PREREG.md` as it stands:

- l.2013, inside SC-8b: *"(Item 8 is inserted as the list's eighth item; **the item-3 marker and
  SC-8's revised M2 follow the list; the line-97 marker is placed after line 97 in §0.2.1**.)"* —
  none of the three is in the file.
- l.1415, inside SC-6b: *"INSERTION TEXT — §8.2, after `PREREG.md` line 915 (**after marker M2
  where placed**)"* — M2 is not placed, and the applied text hedges its own anchor rather than
  failing on it.

The **substance** of (b) rows 1 and 9 does survive: item 8's body registers the rule in terms —
*"where an earlier clause names the hashed files or their number — item 3's three names, §0.2.1
line 97's 'both' — it … is superseded as the set by this item"*. **The rule is registered; the
markers at the sites are not, and a framing note asserts they are.** §0.2.1 line 97 still reads
*"both file hashes"*, unmarked, against a tag message that will carry twenty.

### The five citations, re-read directly

Unresolved, all five, because the block they cite is absent: l.1338, l.1849 (*"the amendments
block records"*), l.1853 (*"recorded in the v30a amendments block (SC-13c(c2))"*), l.1915
(*"amendments block in terms"*), l.1917 (*"recorded in the amendments block"*). `PREREG.md` l.6
still reads `**Status:** v30 —`, which is **not** a defect (A18 F1, determination stands) — but
there is no amendment status line and no `## v30a amendments` heading anywhere in the file.

### DECISION 1.1 → ⛔ HALT

The branch reached is not the one §1.1 anticipated. It is not that a row cannot be derived without
choosing a rule — **§8.2's key is stated and every row derives cleanly.** It is that the derivation
succeeds and its answer is that **the block would be a false statement about the file it is
inserted into**: it enumerates 37 touches of which 11 are absent, and asserts as its item 1 that no
registered sentence is deleted, when one is.

Assembling and inserting §8.2 now would produce the fifth instance of this ceremony's one shape —
an applied half citing an unapplied half — with the block itself as the applied half.

---

## §1.2 — §AC's SEVEN AGAINST §D.6's FIVE: DISTINCT. Mapped before anything was written.

| §AC (SSF ll.1687–1737) | subject | any §D.6 twin? |
|---|---|---|
| 1 | amends a criterion of a gate signed off at H-34, 12 Aug 2026 — the **ordering** is the disclosable fact | none |
| 2 | the gate is harder on net; criterion 3's corrected-side limb; the contaminated-side tightening **withdrawn** (H-39) | none |
| 3 | §10.1 criterion 3 never evaluated; §9.2 un-run in its registered form; `DEVIATIONS.md` **D-003** | none |
| 4 | whether the kill gate re-runs under the amended criterion is **not registered** — open author decision | none |
| 5 | the map ships, **the fixture does not** — criterion 3 is not third-party evaluable | **nearest**: `D-ARCHIVE` |
| 6 | §10.1 registers no third state; *partial satisfaction* undefined (H-38) | none |
| 7 | criterion 1's requirement **reverses on 14 of 25** leaking-source columns while l.459 does not move | none |

§D.6's five are `D-KEY` (key-to-person binding), `D-ADVISORY` (five advisory ceremony steps),
`D-STALE` (the stale-description floor), `D-INSTRUMENT` (six apparatus gaps), `D-ARCHIVE` (the
external-input dependency). **No §D.6 disclosure is any of §AC's seven.** The one adjacency is
§AC-5 against `D-ARCHIVE`, and they are different objects with different consequences: §AC-5 is
about the **acceptance fixture** (64 stored-prediction parquets per side, outside the repository)
making **criterion 3 unevaluable by a third party**; `D-ARCHIVE` is about the **market-data inputs
`phase7_l2_sim.py` consumed**, making the **classification derivation un-re-executable**. Related
subject, neither a copy of the other. **DECISION 1.2 → distinct; §AC deploys as approved content —
blocked only by §1.1's halt.**

---

## §1.3 — `net_delta`: REPORTED, NOT DECIDED

**In the registration's own feature set, `net_delta` is load-bearing.**
`net_delta_{1,5,10,30,60}s` are **5 of the 11 REQUIRED columns** of the acceptance fixture's
35-column set (`AVAILABILITY_DECLARATION.md` §A.6.1 ll.1264–1268, §C.4 ll.1503–1507), each built at
`phase5_ml.py` **L253** — the `ts_floor` merge on `net_delta`.

**The declaration already holds the mechanism, and holds it more fully than B8.3 credited it.**
§A's defect record, l.3468, verbatim: *"every aggressor-tagging writer that ever existed in the
archive emits only `BUY_AGGRESSOR`/`SELL_AGGRESSOR`/`UNKNOWN`, so `isin(["B","Buy","buy"])` could
never have matched any pipeline product."* It names *"the 7 affected fixture columns"* —
`net_delta_{1,5,10,30,60}s` (corrupted if wrapped), `buy_volume_10s` (dead-zero),
`sell_volume_10s` (redundant with total volume) — splits the claims **timing-structural SUPPORTED /
value-dependent QUALIFIED**, records C5's verdict that the original runs **wrapped**, and states:
*"Either way the buy/sell sign information is absent from the 7 columns."* `buy_volume_10s` is
declared out of the criterion-1 denominator at §C.4(a).

**The paper itself is not in this repository and I will not guess at it.** The only reference to it
anywhere in the corpus is `preregistration_v4.txt`, cited by line at declaration ll.603 and 607 and
external to the tree. So: **whether `net_delta` appears in the CME microstructure paper's feature
set or published results is not determinable from this repository.** What the repository does
establish is the link that makes the question live — the fixture's builder **is** the original
experiment's builder (`f2\phase5_ml_fixture.py` is a byte-verified copy of `phase5_ml.py`,
`Y1_REPORT.md` l.186), so any `net_delta_*` figure the paper published came from the same
constantly-false predicate. **An author call, joining the errata already pending. It does not block
the tag.**

---

## TRACK B

**B8.3 — one sentence of `B8_PROBE_B_RESULTS.md` §4 overstated the corroboration, and is corrected.**
It read that the declaration recorded the **symptom** while the probe recovered the **mechanism**.
The declaration records both: §D.1 item 2 freezes `buy_volume_10s` as a degenerate constant *and*
§A l.3468 states the predicate. What survives, and is the load-bearing half, is the **independence**
— the probe was never given the declaration (SC-7(c)) and reached the same mechanism by perturbing.
The document is corrected to say that.

**Everything else in B8.3 stands.** 47 cohorts, 33 fired, 14 silent, reducers accepted both traces
unchanged.

**Suite, with its domain attached:** `tests/phase1` **113 passed, 4 skipped**; the whole suite
`tests/` **250 passed, 4 skipped**.
