# ROUND_STATE.md — one-file re-orientation

**Purpose (R36).** After compaction, re-orient from THIS file. Rewrite it every round.

**CURRENT STATE: v30a closeout, Track A. The whole A4 edit batch is staged and
UNCOMMITTED.** `main` is at `3257f07752a352ac4c56e595f8bd1caebc7bf857`; tags are `prereg-v30`
only. Nothing has been committed, tagged, pushed or stamped.

**Track B runs in parallel on branch `phase1` and waits on none of this.**

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
