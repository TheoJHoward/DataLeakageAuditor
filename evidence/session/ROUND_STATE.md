# ROUND_STATE.md — one-file re-orientation

**Purpose (R36).** After compaction, re-orient from THIS file. Rewrite it every round.

**CURRENT STATE: R147. Track A halts at A36b — §13c-P is presented and awaits the author's read.
It is the only thing between here and A17‴.** `main` is at `e5b099b`; `phase1` at `5295089`.
**`PREREG.md` is at `fcacebb231438e31…`, 2228 lines.** Tags `prereg-v30` only;
`backup/held-banking` `655f613` pins the stash.

**A36b's presentation now LEADS with the consequence, and there are TWO.** *(1)* The pointer's
closing sentence records the line-816/830 relationship *“in the v30a **amendments block**”* — a
container ruled never to land, and the exact phrase A34 removed from all four operative sites one
commit earlier. *(2)* **NEW this round:** the fenced specimen at l.1344 is **byte-identical** to the
text being applied, so landing it without removing the `INSERT AFTER` apparatus puts the same
paragraph in the file **twice** — and any future citation anchored on it would then resolve to two
lines, which is exactly the failure A34 spent a correction class avoiding. **Three choices are laid
out; none is taken.**

**Added this round, absent from the first artifact:** the insertion anchor **located and asserted
unique** (`PREREG.md` l.1336, match count 1); the **markdown-structure check before any write plan**
— top-level paragraph, blank above and blank below, fenced apparatus below stays balanced; and
**what applying makes true** — §AB's assertion at l.1374, false today, to be verified by reading
rather than assumed.

**A34 and A39 are DONE** (`f1d66bf`, `09d4ca0`). A34's four citations are anchor-keyed by naming the
container, never by quoting the unique string; the self-inflicted collision on the limb's heading was
caught by its own sweep and repaired. A39 fixed **eight** ranges, all exactly +8, and **refused
sixteen** it could not derive.

**`main`'s gate: 23 checks, FAIL — the two C2-blocked findings. `phase1`'s adds D10**, which clears
at X1's post-push rebase.

**Track B: §9.2 step 2 COMPLETE (six of six).** `gate_suspicious_improvement` **was seen to fire** on
an error metric — MAE 0.0163 against a 0.8173 baseline, improvement **+0.980 → HALT**. **Leakly is
the only tool that supplied a vendor negative**; for the other five both limbs were constructed.
**Step 3 has begun**: the fixture reads, and both sides are being materialised one at a time per
SC-7(d).

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

---

> **CONSOLIDATED 27 AUGUST 2026 FROM `stash@{0}` (A38). THIS SECTION WAS NEVER COMMITTED.**
>
> **It was written on 26 August 2026 and held in the stash from that day until this one** — the one
> git ref that is unpushed, droppable and invisible to every branch. It is restored here verbatim
> and unedited; **68 lines of it existed in no committed file**, including the A9 all-green table,
> the point at which §1.6 attaches, and two defects of my own.
>
> **THE A9 RUN BELOW IS SUPERSEDED AS A VERIFICATION AND STANDS AS A RECORD.** It ran against
> `d39643e18fc5a6e1ffb26ebaa75e7d20ee1eb4ca` (26 Aug 2026). **Sixteen commits have landed on `main`
> since**, so nothing below attests the tree that exists now — A17‴ re-runs A9 against the tree that
> exists then. Every figure below was true of its own date and is not rewritten: **a dated record
> correct as of its date is not a stale verification value.**
>
> **The hold-rationale had lapsed.** Banking was held out of the repo so the tag-attested tree would
> be exactly the tree A9 verified. That tree was reopened sixteen commits ago, so holding the record
> outside the repository had stopped protecting anything and was only risking it.

## A5.4 / A6 / A5.5 / A7 / A8 / A9 — THE CEREMONY PASSED

**A5.4 — the limb-table exemption stands, and the question is now settled
empirically rather than by judgement.** The check requires every path of the set
to appear in a window **in `FILES` order**. `FILES` leads with the `prereg-v30`
five so the v30 block stays a verbatim prefix of the v30a one; the limb table
leads with limb 1, because its argument is that the set is what three stated
rules produce rather than a list someone chose. **No layout satisfies both**, so
the objection is structural and the exemption is not avoidable by reshaping.

**A6 — branch 2.** §3.5's format block carries substitutable fields only for the
hash slots; the sentence citing §6.2 by line is fixed prose. The registered format
was not edited. §146.2's frame was extended to reach the tag message and says so
in terms — the tag message cannot carry its own caveat, so the frame is stated in
a file the same tag hashes, which is what makes it as firmly attested as the
message it qualifies.

**A5.5 / A7 — the final five repaired.** Three D8 citations re-anchored by
locating, never by offset. The README and the declaration pointer written from
`v30a.hashes.txt` only.

**A8 — commit `d39643e18fc5a6e1ffb26ebaa75e7d20ee1eb4ca`**, 34 files,
+4124 −217.

### A9 — THE ONE PASS, ALL GREEN

| check | result |
|---|---|
| `--stage prereg` | **exit 0, PASS, 23 checks** |
| `pytest tests/registration` | **137 passed** |
| manifest, listed→disk | **687 OK** |
| manifest, D9 both directions | **exact, 683 files** |
| C2 vs `v30a.hashes.txt` | IDENTICAL |
| C2 vs `tagmsg.txt` | IDENTICAL |
| C2 vs the README block | IDENTICAL |
| C2 vs the working tree | IDENTICAL |
| C2 vs the commit | IDENTICAL |
| C5b, fresh baseline `3257f077` | every inherited commit accounted; `d39643e` is the ceremony's own |
| tags | `prereg-v30` only |

**§1.6 attaches from this point.** The registration is closed to pre-tag fixes;
any later finding is a `DEVIATIONS.md` disclosure.

### Two defects of mine this round, both caught and repaired

**A dated historical record was corrupted twice by the same broad substitution.**
`re.sub` over the whole pointer file rewrote every historical hash to the current
one and edited a 2026-08-21 entry's byte count — while MISSING the current block,
whose field is written with two spaces. Caught by reading the file rather than
the gate; the gate cannot see it, because a flattened history is internally
consistent. Reverted from HEAD both times. The replacement edits three anchored
fields only and asserts afterwards that the chain still holds more than one
distinct hash — the cheap invariant that catches a flattening substitution. The
unsafe section was excised from the script that carried it, in the tree as well
as the scratchpad, so it cannot run again.

**A `grep` in a pipeline masked the gate's exit status**, reporting `EXIT = 0`
when the gate had failed. Caught within the same step by re-running the gate
alone. Every exit status reported above is the gate's own.

---

## A0 (this round) — THE CEREMONY WAS ALREADY PASSED

**Entering state differed from the plan's premise.** The plan described `main` at
`3257f077` with nothing committed and A5.4's outcome unknown. In fact the A8
commit landed and A9 ran green in the preceding round.

| | |
|---|---|
| `main` | **`d39643e18fc5a6e1ffb26ebaa75e7d20ee1eb4ca`** |
| tags | `prereg-v30` only — nothing tagged, pushed or stamped |
| the tag target's tree | **gate PASS** — verified by stashing the working-tree edit and re-running |

**A5.4's uncertain script: determined by READING, not by re-running.** The four
enumeration exemptions carry 11, 8, 3, 6 and 4 paths — the restated values, not
the six-path-era ones. The gate agrees: the four D6 findings that script existed
to clear are absent, and the committed tree passes 23 checks. **The script
succeeded; no re-run was needed or attempted.**

**The one red finding was mine and is not a registration defect.** Banking A9
into this file after the commit changed its bytes, and the pinned scratchpad
holds a copy of it that no longer matched — so the round-reconciliation check
fired on the report about the work rather than on the work. Synced.

**This round's banking stays UNCOMMITTED until after the tag**, so the tree the
tag attests is exactly the tree A9 verified. It lands in a follow-up commit, the
same shape as the OpenTimestamps receipt, which cannot be inside the commit it
attests.

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

---

## B9 — DECISION, THE TWO DETECTORS, AND A SEED THAT WAS NOT REPRODUCIBLE

### DECISION B9 → the first branch, settled by registered text

`PREREG.md` §6.6 **l.1080**, verbatim: *"a combination is execution-eligible for a case when **at
least one configured strategy resolves to that promotion status on that case** and has all required
inputs. **This is per case rather than per configuration because `noise`, `nan`, and `constant`
preserve on some frames and promote on others (§3.2).**"*

The clause names `nan` in terms. A combination whose eligible cohorts are a dtype-defined subset is
not merely permitted — it is the case §6.6 was written for, and the null detector is that sentence
built into a detector.

**l.1084** closes the remaining question: *"`not_applicable` — no configured strategy resolves to
this promotion status on this case, **or no eligible cohort was selected for it**. The second clause
covers a combination with resolved strategies, available inputs, and nothing to do."* So the third
branch — an empty promoted combination is legal — is **also** true, and it is exercised as a test
rather than taken as a licence to drop the out-of-dtype sentinel. Dropping it would have removed the
promoted side's whole content.

### The two detectors

| detector | combination | strategies | eligible cohorts |
|---|---|---|---|
| `valueread` | preserving | `shuffle`, in-dtype `sentinel` | every column |
| `valueread` | promoted | `sentinel_ood` | columns for which a **wider dtype exists**: integer → `float64`, boolean → `int64` |
| `nullread` | preserving | `nan` | columns that already hold a null **in their own dtype** — float, datetime, object |
| `nullread` | promoted | `nan` | columns that do not — integer, boolean |

**The split is derived, not asserted, and it was derived from B8's own record.** `probe_b_merged.json`
names the cohorts that took a promoted frame under `nan`: **25 promote, 22 preserve, 25 + 22 = 47.**
`nullread`'s two combinations therefore partition the fixture's columns exactly, and the partition is
asserted at run time in both the detector's tests and the sweep's merge — a property nothing checks
is one that quietly stops holding.

**`nullread` closes the gap `columndep` published.** There, `nan` sat only in the promoted
combination, so a float column never received a null and a feature reading one only through
`isna()` was reported silent. **`columndep`'s domain statement is UPDATED, not deleted** (R134's
instruction, and there is a test that both halves survive): the gap sentence stays, because a reader
of an *earlier* `columndep` result needs to know the gap was open when that result was produced, and
a sentence naming `nullread` is added beside it.

**What the out-of-dtype sentinel buys, demonstrated rather than argued.** On a column pinned at its
dtype's maximum, *both* preserving strategies degenerate: a permutation of identical values is the
identity, and the in-dtype sentinel is capped by the dtype, so at the ceiling the cap **is** the
column's value. Both record `control_artifact`, the combination resolves `× none`, and the
out-of-dtype sentinel is the only strategy that can perturb the column at all — at the cost of
promotion. That trade is the promoted combination's entire content, and it is a test.

**What `nullread` still cannot see, stated because §39 requires the domain with the silence:**
introducing a null tests whether nulls are read, never whether an **existing** null pattern is read,
and a column with no nulls to begin with cannot answer the second question.

### B9-F1 — THE PERTURBATION SEED WAS NOT REPRODUCIBLE. Found reading the instrument, not running it.

All three call sites computed `abs(hash((frame, column, strategy))) % 2**31`. **CPython salts
`hash()` for `str` with `PYTHONHASHSEED`, which is random per process unless pinned, and nothing in
this repository pins it.** Demonstrated, not reasoned: the same expression in three processes gave
`1115184579`, `226073761`, `588577123`.

**Nothing it produced was invalid.** Any permutation is a legitimate shuffle, and the identity case
is caught explicitly as `control_artifact`. What it lacked is **reproducibility**: B8.3's sweep
cannot be re-run to the same trace, and the four workers each drew from a different salt. A shuffle
that moves nothing on one draw and something on the next turns `observed_silence` into a coin toss,
and an evidence record nobody can re-run to the same answer is a measurement nobody can check.

Replaced with a SHA-256-derived seed at all three sites. The regression test **spawns three
processes**, because that is the only place the defect lived — calling `seed_for` twice inside one
process would have passed against the old implementation too, which is the shape of guard that
proves nothing.

**The B8 sweep is re-running under the fixed seed**, four workers, into a separate shard directory
so the recorded result is not clobbered. The comparison against `probe_b_merged.json` is the point
of the re-run and is not yet in hand.

### The controls, and one that could not fire

Every detector has a positive **and** a negative control. The first draft of the value control could
not fire: the string column held `"a0"`/`"a1"`/`"a2"`, all length 2, so `map(len)` was constant and
no permutation could move it. The detector reported silence, correctly, and the control proved
nothing. **That is the `aggressor_side` class reproduced by accident inside the test written to
demonstrate the instrument** — which is worth more as a record than as a quietly-fixed line, so the
reason is in the test file.

A second draft asserted the out-of-dtype sentinel would "get past a clamp". That was wrong on its
face — a clamp means the output is insensitive to anything above the bound, so nothing should move —
and the test failed for the right reason before it could become a claim.

### Banked

| commit | what |
|---|---|
| `34f9ab4` | the R134 round record: A19″ derived and halted, RE-1/RE-2, §AC mapped, `net_delta` reported |
| `66063da` | the two detectors, the seed fix, 13 new tests |
| `560ec2a` | the sharded B9 sweep and its merge — apparatus only, not yet run |

`tests/phase1` **134 passed, 4 skipped**; gate **PASS 23**.

---

# R135 — A20 COMPLETE AND HALTED · B8-R REPRODUCED · B9-S RUNNING

**Track A is suspended below A20 and A20 is done. Nothing edited, staged or committed to `main`.**
`main` at `87054020278eca99…`, `PREREG.md` byte-exact at `0c8da19f237cd243…`, tags `prereg-v30`
only, held banking preserved in `stash@{0}`.

## RE-ENTRY — both gates, and where §0 was stale

| | |
|---|---|
| `phase1` gate | **23 checks, PASS** |
| `main` gate | **23 checks, FAIL** — expected, and now down to **one** finding |
| §0 said `phase1` is at `5e3aabb` | it is at `e194d82` — §0 was written before the comparator commit |

**`main`'s D10 is one file, not three.** `ROUND_STATE.md` alone: `phase1` adopted `main`'s
`DEFERRED_ITEMS.md` and `COMMIT_ACCOUNTING.md` verbatim last round, so the work root now matches
`main` on both, and only the round record — which this round rewrites again — differs. RE-2 settles
as recorded.

**`main`'s gate was run without a checkout**, by extracting `git archive main` to a scratch tree, so
the three running sweep workers were not disturbed. That method has two artifacts of its own and
they are named rather than reported as findings: `git archive` carries no untracked files, so four
`.pytest_cache` entries show as missing; and the extracted tree is not a git repository, so D16's
`git ls-files` cannot run. Neither is a fact about `main`.

## A20 — ⛔ HALTED AND PRESENTED

**The artifact is [`evidence/amendment/A20_DIFFERENTIAL_AUDIT.md`](../amendment/A20_DIFFERENTIAL_AUDIT.md).**
Three read-only instruments, all committed: `a20_differential_audit.py`, `a20_block_classes.py`,
`a20_artifacts.py`.

**The headline inverts the salvage question.** The reconstruction — v30 with
`PREREG_v30a_APPROVAL.diff` applied, every context and removal line verified against v30 first, 109
checks — is **byte-identical to the applied `PREREG.md`**, `0c8da19f237cd243…` on both sides.

| class | count |
|---|---|
| **UNAPPROVED-APPLIED** | **0** |
| **APPROVED-MISSING** | **0** |
| APPROVED-APPLIED | 15 hunks, 868/868 added lines present |
| DELETED | 5, of which **4 retain nothing** |

**Nothing was applied that nobody approved, and nothing approved failed to land.** The defect is not
in the application; it is in the **approval record**, one layer back.

**And the record set states its own population, which is the whole cause:** *"one record per
**clause**, authored by reading `SCHEMA_SET_FINAL.md` PART 1"*, located by a `### SC-<id>` header and
a `**THE CLAUSE.**` line. A MARKER block has neither. Derived: **MARKER blocks reaching the file,
0 of 14. CLAUSE blocks reaching the file, 16 of 16.** The markers were not dropped — they were never
eligible.

**A twelfth missing touch, not previously counted: `SC-12(w)`.** The `waived` entry condition — *"a
prohibition, and a closed list of licensed grounds with no members"* — is absent from `PREREG.md`,
cited from three applied lines, and its text sits **outside** the `SC-12` record's declared clause
span. `verify_schema_records.py` digests the declared span and cannot see that the span stops short
of the block it names.

**The hash half of the describing artifacts is sound and is the half a gate checks.** `tagmsg.txt`
v30a block: 20 enumerated, **20 match**. `README.md` v30a block: 20 enumerated, **20 match**.
`README.md`'s v30 block mismatches 4 of 5 and is a **dated record of what v30 was**, correct as
written. The defect is entirely in the prose: **21 of 25 enumerated claims do not hold**.

## B8-R — THE FIXED-SEED RE-RUN REPRODUCED THE ARTIFACT BYTE FOR BYTE

Four workers, fixed SHA-256 seed, merged into a separate path so the banked record could not be
clobbered — a hazard fixed before it fired, since `merge_probe_b.py` had an overridable input
directory and a hardcoded output.

**`probe_b_merged.json` sha256 `1cdae81ea761bc86…` — identical.** Same baseline, 33 fired / 14
silent, 433/422 preserving, 127/127 promoted, 346 events, 228 PROVEN. **No cohort changed
classification and no silence flipped.** On this fixture the salted seed cost reproducibility and
nothing else, and B8.3's numbers stand exactly as reported. `B8_PROBE_B_RESULTS.md` §6.1 now carries
the defect, the re-run and the comparison, so the document's silences carry the seed as part of
their domain.

**Narrower than it looks:** that is a fact about these columns, not a licence to leave a stochastic
instrument unseeded. A draw that happens to be output-equivalent is possible where a column has few
distinct values, and the only reason we can say it did not happen here is that the run was repeated.

## B9-S — RUNNING

Both detectors against `fixture_corrected`, four workers, launched as soon as B8-R released the
cores. Still in the `valueread` phase. **Known gap in the harness:** it logs once per detector
rather than per cohort, so a long run reports nothing for a long time. That is a reporting hole, not
a correctness one, and it is recorded rather than fixed mid-run.

## INSTRUMENT DEFECTS FOUND AND CORRECTED THIS ROUND

Every one would have put a false row into A20's tables. Full list with consequences in §8 of the
audit artifact.

| defect | what it would have reported |
|---|---|
| diff parser read the file's trailing newline as a context line | the applier halted on a mismatch **it had itself created** |
| block probe used each block's longest line | four `SC-` clauses ABSENT that are demonstrably present |
| block probe did not exclude text v30 already had | H29 PRESENT on **v30's own text** — the inference R135 forbids |
| cross-tab conclusion was half-checked | *"every clause is present"* printed while the column read 12 of 16 |
| claim table scored raw verdicts | the tag message's one **true** §6.2 claim listed as false |
| artifact audit read one tree and hashed another | `phase1`'s pre-growth README reported as `main`'s — six files where there are twenty |

**D2.1 was violated twice this round**, both times a heredoc running a file-writing patch script —
once before R135 restated the rule and once after. Both caught and rewritten through the Write tool;
`test_written_files_are_intact.py` found no damage.

---

## R135/B — THE `aggressor_side` CLASS, MADE MECHANICAL · §9.2 IS FEASIBLE

*(Banked while B9-S runs. B9-S's own results are not in this section.)*

### The `aggressor_side` class — a screen, not a verdict

R135 §4: *"Note where it would have been missed; whether it earns a third detector is a design
question for after the sweep."* B8.3 found `trades.aggressor_side` by noticing one odd silence and
then reading the source. `tests/phase1/reference_but_silent.py` makes the noticing mechanical:
**the columns the builder's source references, minus the columns the probes moved.**

Over B8's 47 cohorts:

| | |
|---|---|
| silent cohorts | 14 |
| name matches anywhere in the builder source | 3 |
| **…of which SAME-FRAME candidates** | **2** |
| …of which name collisions with another frame | 1 |
| unreferenced — ordinary silence | 11 |

**The first version of the screen reported three candidates and two were wrong.** `col:trades.side`
and `col:trades.action` matched `df["side"]` and `df["action"]` inside `load_mbo_aggregated` — a
function that reads *a different parquet*, the 8.2M-row MBO frame the adapter deliberately never
opens. A bare column name collides across frames. The screen now captures the **receiver** and the
**enclosing function** with every match, so a collision reads as a collision.

**Both surviving candidates were then read, and they are different from each other:**

```python
is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \
         else trades["side"].isin(["B","Buy","buy"])
```

- **`trades.aggressor_side` — the class.** The reference **executes**, and the predicate is false
  for every row of `SELL_AGGRESSOR` / `BUY_AGGRESSOR` / `UNKNOWN`. No permutation can move the
  output. **Invisible to a value probe, and invisible to the null detector too** — the mechanism is
  a constantly false predicate, not a null pattern.
- **`trades.side` — NOT the class.** Its reference is the `else` limb of a ternary whose `if` limb
  always fires, because `aggressor_side` is present. **A dead branch, not a dead predicate.**
  B8.3's one-line explanation — *"the `aggressor_side` branch is taken, so `side` is never read at
  all"* — is confirmed by the screen rather than merely restated.

**So the class has exactly one member on this fixture**, and the screen reduced fourteen silences to
one question a human answers in two lines. Whether that earns a third detector stays a design
question for after B9-S, as R135 directs. Three tests cover the screen, including that it **halts**
rather than returning an empty candidate list when pointed at the wrong source — an empty screen is
not an empty finding.

### §9.2 — the comparators are runnable. Feasibility established, nothing executed.

**The k6 virtualenvs survive at `C:\Users\ttbea\k6env\`**, and their versions match the environment
record captured on 14 Aug 2026 before results were read:

| venv | tools |
|---|---|
| `general` | `Leakly` 0.1.2, `leakage-buster` 1.0.2, `leakfence` 0.5.0, `temporalcv` 2.3.0 |
| `ld` | `leak-detect` 0.0.1 |
| `dc` | `deepchecks` 0.19.1 |
| `omds`, `lav`, `la`, `R`, `omdsrc` | present |

**None is importable from the main interpreter, and that is by design** — they carry conflicting
`pandas` and `scikit-learn` pins (2.2.3 / 2.3.3 / 3.0.5 and 1.5.2 / 1.6.1 / 1.9.0). Any §9.2 runner
must invoke each tool through its own venv's interpreter, as k6's did.

**What §9.2 still needs**, stated so the next round starts from it rather than rediscovering it:

1. **The acceptance fixture materialised as tool inputs, both sides.** Cheap: `fixture_corrected`
   *literally calls* `fixture_contaminated` and adds `apply_universal_lag`, so one `read_inputs`
   capture serves both — `builder_for(inputs, side)` switches at zero extra I/O.
2. **A positive control per tool first** (W2b steps 1–2). *"A tool that has never been shown to fire
   through its adapter has not been tested; it has been mishandled."* A tool whose adapter does not
   fire on its own documented positive is recorded **NOT RUN** — never an abstention, never a miss.
3. **R is still not installed**, so `leakr` and `bioLeak` remain structurally unrunnable, as
   recorded at k6.

### A related observation, HELD — SC-7(d) and the adapter

`read_inputs` executes **`fixture_contaminated`** to capture the builder's reads, and the probes
then build the **corrected** side from that capture. That looks like both sides in one run.
**It is not**, and the reason is structural rather than a matter of care: `fixture_corrected` is
*defined as* `fixture_contaminated` plus a lag, so the two sides read exactly the same inputs and
the capture cannot carry side-specific information. The contaminated builder's **output** is
discarded; only its reads are kept.

**But the corollary is worth recording:** the two sides are one argument apart from the same
`FixtureInputs`, so **SC-7(d)'s one-side-at-a-time rule is enforced by harness discipline, not by
the adapter.** Nothing structurally prevents a caller from building both. For §9.2, which needs both
sides, that is exactly the place where the sequencing rule has to be honoured deliberately.

---

## B9-S — DONE. The sweep's headline is a NEGATIVE result.

**Artifact: [`evidence/phase1/B9_DETECTOR_SWEEP_RESULTS.md`](../phase1/B9_DETECTOR_SWEEP_RESULTS.md).**
Four workers, 47 cohorts, baseline `d8712f163cf9dcb6…` — **identical to B8's**, so all three
detectors probed one object. All four traces accepted by the reducers unchanged.

| | `valueread` | `nullread` |
|---|---|---|
| preserving | `incomplete(compatibility)` × `finding` — 47 cohorts, 433/**422** valid | `incomplete(crash)` × `finding` — 22 cohorts, 68/**63** valid |
| promoted | `completed` × `finding` — 25 cohorts, 125/**125** | `completed` × `finding` — 25 cohorts, 127/**127** |
| events | 344 (228 PROVEN) | 180 (62 PROVEN) |
| fired / silent | 33 / 14 | 32 / 15 |

**`nullread`'s partition holds: 22 + 25 = 47**, no overlap, none uncovered, asserted by the merge.

### What each strategy uniquely contributed

| strategy | pairs | cohorts | **pairs no other strategy found** |
|---|---|---|---|
| `shuffle` | 226 | 33 | — |
| `sentinel` | 178 | 32 | — |
| `sentinel_ood` | 116 | 16 | **0** |
| `nan` | 180 | 32 | **2** |

**The out-of-dtype sentinel added nothing on this fixture.** Zero pairs the preserving strategies had
not already found, for the cost of a determinism guard and a promoted baseline on 25 cohorts. Its
reason for existing — that at a dtype ceiling both preserving strategies degenerate to the identity
— is demonstrated in a unit test and **does not arise in this fixture's data**. Worth having;
stated as the negative it is.

**`nan` found exactly two pairs no value strategy can reach:** `trades.size → trade_count` and
`→ trade_count_10s`. `trade_count=("size","count")` counts **non-null** values, so a permutation
and an in-dtype sentinel both leave it alone. A pure null-mask dependency, structurally invisible
to a value probe.

### The gap `columndep` published is real in principle and EMPTY in fact

`nullread`'s preserving combination is precisely the probe `columndep` said it was missing: `nan`
over the **22** float/datetime/object columns. **Sixteen fired, and every feature they moved was
already found by `shuffle` or `sentinel`.** The two null-only findings are on `trades.size`, an
**integer** column — `nullread`'s *promoted* side, the combination `columndep` already had.

**So the published gap cost this fixture nothing.** That is weaker than the gap statement implied
and is stated plainly rather than left for a reader to derive.

### The three detectors agree where they should, and differ where they should

`valueread`'s preserving side reproduces `columndep`'s **exactly** — same 33 cohorts, identical
feature sets — **except `col:trades.size`, 15 features vs 13.** The two missing are the null-only
pair: `columndep` found them through its *promoted* combination, which runs `nan`; `valueread` never
runs `nan` and cannot. **Checked, not assumed** — a difference between two detectors over the same
strategies would otherwise read as a defect.

### Five crashes, and they are a fact about the pipeline

`nan` **crashes the builder** on `snap.timestamp`, `trades.action`, `trades.aggressor_side`,
`trades.side` and `trades.symbol` — recorded `could_not_run(crash)`, never as a finding, and they
are why `nullread`'s preserving trace is `incomplete(crash)`. **The builder has no null tolerance on
those five columns.** `snap.timestamp` is the single cohort that fires in `columndep`/`valueread`
(50 features) and is silent in `nullread`; that is not a disagreement — the probe crashed, so its
outcome is `none`, not silence.

### The `aggressor_side` class survives all three detectors, for TWO reasons

R135 predicted the null detector would not catch it because the mechanism is a constantly false
predicate rather than a null pattern. True — and the run adds a **proximate** reason that bites
first: **`nan` on `aggressor_side` crashes the builder**, so the null probe never reaches a
comparison. The class is unreachable both because no value probe can see it and because the null
probe cannot execute. Whether it earns a third detector stays open.

### Silence accounting, per cohort (§39)

`valueread`: **12 `observed_silence`, 2 `none`** (`trades.action`, `trades.symbol` — no strategy ran
validly). `nullread`: **10 `observed_silence`, 5 `none`** — all five the crashes above. A probe that
did not happen found nothing, and that is not the same as a probe that happened and found nothing.

---

# R136 — A20b DONE · A21 ⛔ HALTS TWICE · THE DEFECT REACHES A HASHED FILE

**Track A unchanged on disk.** `main` at `87054020278eca99…`, `PREREG.md` byte-exact at
`0c8da19f237cd243…`, tags `prereg-v30` only, held banking in `stash@{0}`. Nothing edited, staged or
committed to `main`.

## RE-ENTRY

| | |
|---|---|
| `phase1` gate | **23 checks, PASS** |
| `main` gate | **23 checks, FAIL — 1 finding**, D10 on `ROUND_STATE.md`, run in the real tree this time |
| §0.2 said `phase1` at `5e3aabb`, B8-R running, B9-S queued | **stale** — `phase1` at `8121549`; **B8-R landed** (byte-identical) and **B9-S is DONE** |
| §1.4 says `B8_PROBE_B_RESULTS.md` is provisional until the re-run lands | **the re-run landed.** §6.1 of that file carries the defect, the re-run and the comparison |

**No silence flipped.** The fixed-seed re-run reproduced `probe_b_merged.json` byte for byte, sha256
`1cdae81ea761bc86…`, so there is nothing to report individually and the provisional marking is
discharged.

---

## A20b — THE DELETED CLASS, FINISHED. The wrapping hypothesis was checked and does not hold.

A20's probe asked whether an 80-character prefix appeared on **some line**. That is a sample.
R136 was right that a retention block may wrap a quotation across lines, so this replaced it with a
derivation: **both sides normalised — blockquote markers stripped, all whitespace collapsed, the
whole file as one string — then the longest common substring between each deleted sentence and the
entire applied file.** Line boundaries stop existing, so wrapping cannot hide anything.

| v30 line | what it is | longest surviving run | at | marker? | verdict |
|---|---|---|---|---|---|
| **461** | §6.2 acceptance criterion 3 | 54/92 | l.630 | no | **NOT RETAINED** |
| **855** | §7.7 detector-case coverage row | 37/119 | l.1067 | no | **NOT RETAINED** |
| **929** | §8.3 `assert_audit_complete()` | 108/187 | l.1565 | no | **NOT RETAINED** |
| 1022 | §10.1 kill-gate criterion 3 | **214/214** | l.1678 | **yes** | **RETAINED VERBATIM** |
| **1030** | §10.2 kill/pause criterion 2 | 36/128 | l.627 | no | **NOT RETAINED** |

**A20's answer survives the stronger test: one of five retained, four not.**

**A long common substring is not a quotation.** `" under the reconstructed declaration"` is 36
characters of shared vocabulary between two clauses about the same subject. Partial retention is
credited **only where a retention marker sits at the site** — which is what §8.2 actually promises
(*"in a block marked `SUPERSEDED BY v30a`"*) and the only form a reader could recognise.

**l.929 is the interesting near-miss.** 108 of its 187 characters survive at l.1565 — but l.1565 is
the **operative v30a replacement**, which is the old bullet with `waived` added. A reader can
recover most of the old sentence only by noticing the replacement is a near-copy. **Nothing marks it
as the retained original**, so it is not retention in §8.2's sense.

### DECISION A20b — the branches that fired

- **retains its text →** v30 l.1022. §8.2's description is accurate for that row.
- **retains nothing → a DESCRIPTION defect in §8.2, not an applied defect.** Four rows: 461, 855,
  929, 1030. The deletions were approved; **`PREREG.md` is not edited.**
- **leaves a live citation → an APPLIED defect.** **Exactly one: l.1544**, *"state that row carries
  other than `passed` and `failed`"*, whose *"that row"* is §7.7's deleted coverage row.

### The citation screens, and what they cost me

Two screens, each with its bound stated. **(a) by v30 line number** — fully derived. **(b) deictic**
— every *"that row"* / *"the table above"* in the file, **listed once and unattributed**.

**The first version attributed deictics by proximity** to where each deleted sentence's longest
surviving run happened to sit — which is not the deletion's site at all — and put **l.1544's
*"that row"*, which refers to §7.7's row at v30 l.855, onto v30 l.929** because it was 21 lines
away. **Proximity is not reference.** The list is now unattributed and complete rather than
attributed and wrong.

Three deictics exist. Two were **read and cleared**: l.895's *"that row"* refers to a detector row
named in its own sentence; l.1163's refers to *"each §0.1 lock-table row"*, also named in its own
sentence. Only **l.1544** refers to something deleted.

**And four "line 461" citations were read and cleared too.** l.1892 and l.1898 say *"under
registered line 461 **unamended**"* and *"**Until the `prereg-v30a` tag is signed**, line 461 stands
unamended"* — **forward-looking conditionals that are true as written**, discharged by signing, the
same class as `PROVISIONAL until the tag is signed`. Not defects.

---

## A21 — ⛔ HALTS, TWICE, AND THE SECOND ONE IS NEW

### HALT 1 — `tagmsg.txt`'s change-list is hand-authored, exactly as R136's branch anticipated

`CEREMONY_COMMANDS.md` §3.5, l.503, inside the format block:

> `Amends PREREG.md §6.2 — reference AUC (l.445), contamination availability class`
> `recording locus (l.450), sliced CI variant (l.451), criterion 3 (l.461) — and`
> `defines "waived" for §10.2's replacement-criterion floor.`

**There is no source to correct.** The hash lines below it *are* derived — §3.5 says they are *"the
output of C2, pasted — never retyped, never re-derived"*, and `v30a.hashes.txt` is their authority.
**The change list has no equivalent.** It is prose, and it is the same defect class as the
six-versus-twenty-three count: a hand-authored value with no derivation, that no gate asks about.

**DECISION A21 → "it is hand-authored in the format block → HALT and present."**

### HALT 2 — the defect reaches inside the twenty hashed files

`AVAILABILITY_DECLARATION.md` is **not a drafting record**. It is one of the twenty files
`tagmsg.txt` hashes, frozen at the tag by its own §D.1, and `PREREG.md` SC-7(a) names its declared
elements as a gate input.

Its §A conformance walk discharges three §6.2 elements **by citing `PREREG.md` clauses by name**:

| declaration line | cites | resolves? |
|---|---|---|
| l.822 | `PREREG.md` §6.2 *"Reference AUC anchor — v30a, operative"* | **NO — not in `PREREG.md` at all** |
| l.994 | *"Contamination availability class — v30a, operative"* | **NO** — the stem is at l.579, but that is **v30's own unamended line** |
| l.1051 | *"Sliced variant — v30a, operative"* | **NO** — same, at l.580 |

**All three of the declaration's named-clause citations resolve to nothing**, and they are exactly
the three §6.2 changes A20 proved were never in the approval record. **All 67 distinct `SC-n`
citations resolve.** So the damage is bounded and it is precisely these three.

**This is not a wording fix.** Three declared elements are reported discharged on the authority of
registered text that was never registered. Making the declaration true requires **applying the three
clauses** — a new `PREREG.md` diff needing its own approval. Making it accurate as it stands
requires **re-dispositioning three elements as undischarged**. Either way it is a decision about
what the amendment means, so §2.3's provisional resolution does not reach it.

### What is CLEAN, checked and reported as such

**`README.md`'s v30a block carries no change list at all** — twenty hash lines and nothing else, and
**all twenty match** the registered branch. `tagmsg.txt`'s twenty likewise: **20 of 20 match.**
`README.md`'s v30 block mismatches four of five and is a **dated record of what v30 was**, correct
as written.

**The mechanical half — the half a gate checks — is entirely sound. Every defect found this round is
in prose no gate reads.**

### The §36.2 survey, and the line it draws

Twenty-odd files mention `l.445`. Almost all are **drafting records of the plan** — `K1`, `X5`,
`SCHEMA_SET_ADOPTION`, `PREREG_v30a_DIFF`, `_E2E3` — and a record saying *"the plan includes l.445"*
is **true**. Only a document asserting the amendment **did** amend l.445 is false. That reduces the
set to four: `tagmsg.txt`, `CEREMONY_COMMANDS.md` §3.5 (its source), `K2_AMENDMENT_LEDGER.md` §8.2,
and `AVAILABILITY_DECLARATION.md`. **Nothing was edited** — §36.2 says find the set before fixing
any of it, and two of the four halt.

---

## INSTRUMENT DEFECTS THIS ROUND

| defect | what it would have reported |
|---|---|
| the normalised text and its line index were built in two passes | reported line numbers drifted further the deeper into the file a hit was — **1658 for a passage at 1678** |
| a long common substring scored as partial retention | four deletions credited as **RETAINED IN PART** on shared house-style vocabulary |
| deictic references attributed by proximity | **l.1544's citation put on the wrong deleted row** |
| the declaration's clause probe searched for the heading stem alone | **"Contamination availability class" and "Sliced variant" reported as RESOLVING at PREREG.md l.579 and l.580 — the very lines A20 proved were never replaced.** The probe found the thing the citation says was superseded and called that resolution |

The last one is the sharpest instance yet of a guard passing for the wrong reason: it would have
reported two of the three most serious findings of this round as clean.

---

# R137 — §1.1 HALTS · A23 DISPOSES THREE CLAUSES SEPARATELY · A22 PRESENTS SIXTEEN

**Track A unchanged on disk.** `main` at `87054020278eca99…`, `PREREG.md` byte-exact at
`0c8da19f237cd243…`, tags `prereg-v30` only, held banking in `stash@{0}`. Nothing edited, staged or
committed to `main`.

## RE-ENTRY

| | |
|---|---|
| `phase1` gate | 23 checks, **PASS**; 145 passed / 4 skipped |
| `main` gate | 23 checks, **FAIL — 1 finding**, D10 on `ROUND_STATE.md` alone, run in the real tree |
| §0.4: *"B9-S — Done, results not reported"* | **stale.** Reported at `8121549`: [`B9_DETECTOR_SWEEP_RESULTS.md`](../phase1/B9_DETECTOR_SWEEP_RESULTS.md) |
| §4: *"B8.3 — remove the provisional marking"* | **there is none to remove.** `grep -i provisional` on that file returns nothing; §6.1 records the defect, the re-run and the byte-identical comparison directly |

**B9-R is discharged, and against R137 §4's own checklist:** fired/silent per cohort per detector
with the moved features (§2 and `b9_merged.json`); silence accounting with domains (§3); `none`
distinguished from `observed_silence` (12/2 and 10/5); reducers accepted every trace unchanged;
the partition held at run time, **22 + 25 = 47**; not scored against the R9 map; and §4 names where
the `aggressor_side` class would have been missed.

---

## §0.3's LINE NUMBERS WERE `phase1`'s. Re-derived on the authority.

`main`'s declaration is **4,358** lines, last written at `8705402`; `phase1`'s is **4,027**, one
round behind. My A21 finding came from the older copy. Re-derived against `main`:

| §0.3 says | actually |
|---|---|
| decl l.822 | **l.860** |
| decl l.994 | **l.1032** |
| decl l.1089 → l.1051 | **l.1089** |

**The finding is unchanged and now stronger: all three named-clause citations resolve to nothing,
and all 71 distinct `SC-n` citations resolve** (61 on the stale copy). Same mixed-tree hazard as
last round's README, caught by re-running rather than by trusting a number.

---

## §1.1 — ⛔ HALT. §3.2's Class B precedent does not reach §3.5's change list.

R137's DECISION 1.1 is explicit: *"Do not stretch a precedent."* On reading, **§3.2's language is
narrower.**

**What §3.2 actually says**, in a parenthetical about a *declined* candidate file: *"Adding a file
later is a Class B change — a parameter of a locked procedure — so this is reversible."* And it
scopes the edit in the same breath: *"append it to the `FILES` line above **and to nothing else in
this file**."*

**What class B is**, per the authority — `PREREG.md` §0.2.1's table, not the ceremony file:
*"**B — parameters under a locked procedure** — a value chosen where the **form, search space,
objective, denominator, and freeze point are already fixed**."* The table's column is *"Phase 1
may"*: it classifies what a **measurement** may resolve.

**Why `FILES` fits and the change list does not:**

| | `FILES` | §3.5's change list |
|---|---|---|
| form fixed | a path list | prose |
| search space fixed | §11 item 8 defines the set | none stated |
| objective fixed | hash every registered file | none stated |
| freeze point fixed | C2, before the tag | none stated |
| consumed by the procedure | **every gate iterates it — C2a, C2b, C2c, C2, C2e, C2f, C1c** | **no gate reads it** |
| single authority | *"`FILES` above is the single authority for the set"* | none |

**The property that makes `FILES` a parameter is exactly what the change list lacks.** Extending the
precedent from a gate-iterated set-membership parameter to a hand-authored assertion is stretching
it, and R137 forbids that.

**The other route is available and does not depend on §3.2.** R137's own second argument stands on
its own: the change list is *"an assertion about what the amendment did, inside the text the key
attests"* — a **verification value** under §187, fixed rather than disclosed. **That ground reaches
the correction without touching §3.2's precedent, and it is the author's to take.** Both readings
are presented; neither is acted on.

---

## A23 — THE THREE CLAUSES, DISPOSED SEPARATELY

**Artifacts: [`A23_THREE_CLAUSES.md`](../amendment/A23_THREE_CLAUSES.md) and, for the two that are
load-bearing, [`A23_PROPOSED_DIFF.md`](../amendment/A23_PROPOSED_DIFF.md) — extracted verbatim from
`PREREG_v30a_DIFF.md`, anchors located and match-counted, NOT APPLIED.**

| clause | v30 line | verdict | why |
|---|---|---|---|
| Reference AUC anchor | 445 | **LOAD-BEARING** | the registered anchor is **unsatisfiable** on the fixture |
| Contamination class locus | 450 | **LOAD-BEARING** | l.450 requires what **SC-9(b) forbids** |
| Sliced CI variant | 451 | **UNDETERMINED** | §D.2(ii) discharges it *"by amendment"* — the missing one |

**Clause 1 is not load-bearing by citation — nothing in `PREREG.md` reads the reference AUC** (the
string occurs once, its own v30 bullet). It is load-bearing by arithmetic. Computed here, not
quoted, against `0.957 / 0.675 ± 0.010`: 5s passes pre by 0.009244 and fails post by 0.256536; 10s
fails both; 30s fails pre by 0.100581 and passes post by 0.004288. **No horizon satisfies both
sides.** SC-2(d) registers the recomputation rule but subordinates *"any figure recorded in a prior
report"* — and l.445's pair is in the **registration**, not a prior report, so on its face SC-2(d)
does not retire it.

**Clause 2 is two registered texts in conflict.** l.450 requires the class *"recorded in the
manifest"*; `fixture_manifest_DRAFT.json` has **no key mentioning availability or contamination**;
and **SC-9(b), which is applied**, forbids the fix outright: *"A manifest, a measurement record, a
capture … **is not edited to carry a declaration, a decision, or an amendment**."* SC-9(b)'s next
sentence names the remedy: *"the locus is **amended explicitly**."*

**Clause 3 — R137's hypothesis does not hold as stated.** §D.2(ii) *does* do what SC-2(e) requires:
it names the due event (*"the first CI run that exercises the padded slicer"*), declares the scoring
rule ex ante, and freezes it at §D.1 item 5. **But it records itself *"DISCHARGED by amendment"* —
and that amendment is the missing clause.** The disposition is not independent of the thing that is
absent. Two readings are stated in the artifact; SC-2(e) says the move *is* an amendment, and
SC-9(a) says a declaration *"creates no gate object"*. **The repository does not settle it, and
H4's drafted text is deliberately NOT extracted** — presenting a diff for an element whose
disposition is undecided would be answering the question by drafting.

---

## A22 — THE APPLIED-DEFECT SET: SIXTEEN, NOT SIX

**Artifact: [`A22_APPLIED_DEFECT_SET.md`](../amendment/A22_APPLIED_DEFECT_SET.md). ⛔ Halts by
construction.**

R137 §1.3 enumerates six. The derivation finds **sixteen**, and §36.2 says report the set before
fixing any of it. R137's list **counts l.1544 twice** — once by line, once as *"the one uncleared
deictic"* — and **omits** the four amendments-block citations and the three `SC-12(w)` citations.

| class | n | what |
|---|---|---|
| 0 | 2 | the amendments block and status line the rest of the set refers to |
| A | 4 | citations of the absent block — ll.1849, 1853, 1915, 1917 |
| B | 4 | clauses describing markers never placed — l.1415, l.2013 ×3 |
| C | 1 | l.1544, citing the **deleted** §7.7 row |
| D | 3 | ll.1425, 1427, 1565 citing `SC-12(w)`'s absent limb |
| E | 2 | l.1380's zero-row table header, l.1417's orphaned row |

**l.1338 is cleared and removed from the set.** Earlier rounds said *"the five citations at ll.
1338, 1849, 1853, 1915, 1917"*; l.1338 cites `SC-13c(c2)`, which **resolves**. The class is four.

**Every one was approved that way.** None is an application failure.

---

## INSTRUMENT NOTES

| | |
|---|---|
| the A21 tool was re-run against `main` by pinning `REPO` | a scratchpad copy computes `REPO` from `__file__`'s grandparent and reads the wrong tree — the mixed-tree hazard, avoided deliberately this time |
| pinning it through `python -c` produced a `unicodeescape` SyntaxError on `\U` in a Windows path | rewritten through the Write tool — D2.1's rule one layer up, in a script that patches a script |
| the H3 extraction halted on `REPLACE with (4 lines):**` against H2's `.**` | it **halted** rather than matching something else, which is the right failure; the label is punctuation and the pattern should not be a spelling test |

---

# R138 — A25 APPLIED (TWO SITES, NOT ONE) · A26 PRESENTS · `phase1` GATE NOW RED, ACCURATELY

**`PREREG.md` untouched at `0c8da19f237cd243…`, verified before and after every write this round.
Nothing staged on `main`, nothing committed to `main`, tags `prereg-v30` only, `stash@{0}` preserved.
Neither presented diff was applied.**

## RE-ENTRY

| | |
|---|---|
| `main` gate | 23 checks, **FAIL — 1 finding**, D10 on `ROUND_STATE.md` alone (expected) |
| `phase1` gate, before this round's work | 23 checks, **PASS**; 145 passed / 4 skipped |
| `phase1` gate, after A25 | 23 checks, **FAIL — 2 findings**, both named below and both **blocked on C2** |

---

## A25 — §36.2 FOUND TWO SITES, NOT ONE. Both corrected.

R138 §1.3's first branch assumes §D.2(ii) is the only site claiming discharge by the missing
amendment. **The survey found two**, and no other file in the repository makes the claim:

| site | element | claimed |
|---|---|---|
| §D.2 **(i)** | contamination availability class → the manifest (§A.3) | *"DISCHARGED by amendment, not by doing it"* |
| §D.2 **(ii)** | the CI sliced variant (§A.4) | *"DISCHARGED by amendment"* |

So the **second** branch governs — *"report the full list before editing any of it, then correct
consistently"* — and both were corrected in one edit, each naming **its own** discharge condition.

**(i)** is now recorded NOT DISCHARGED, with the reasoning intact: the manifest is an evidence
artifact and applied **SC-9(b)** forbids editing one to carry a declaration, so the obligation
cannot be met as line 450 words it. **What would discharge it** is named: the drafted §6.2
replacement at `A23_PROPOSED_DIFF.md`, **approved and applied**. Nothing else — a declaration cannot
amend `PREREG.md` (SC-9(a)).

**(ii)** is now recorded NOT DISCHARGED, **and it is the weaker failure**: everything SC-2(e)
requires of a phase move is present and stands — the due event is named, the scoring rule is
declared ex ante, §D.1 item 5 freezes it. **What is missing is the move's own record in the
registered file**, since SC-2(e)'s first words are *"MOVING AN ELEMENT BETWEEN PHASES IS AN
AMENDMENT"*. **Two routes are named** and the choice is the author's: a §6.2 clause recording the
move, or a ruling that SC-2(e) plus this declaration's instance already effects it — in which case
the entry becomes discharged **by SC-2(e), cited**, not by an unapplied amendment.

**H4 was not drafted** (§2.2). The count of discharged lock-time obligations in this file goes from
**two to zero**.

---

## THE MIXED-TREE HAZARD, FIXED AT THE ROOT

**A25 could not be written on `phase1`'s declaration** — that copy is a round behind and still
carries the `Status: DRAFT. Nothing in this file is a registered declaration.` header A16 corrected.
Writing a correction into a stale copy is worse than deriving from one, which is the very thing
R138's RE-ENTRY forbids.

**And adopting one file broke the branch.** Taking `main`'s declaration alone left it against
`phase1`'s **pre-growth six-file** `CEREMONY_COMMANDS.md`: the gate went to **3 checks / 15
findings**, D1 reporting *"states 20 for the v30a hash set; the authority says 6."*

**So the set was derived, not guessed.** Files `main` changed since the merge base **and `phase1`
did not**: **31**, adopted — lossless by construction, since `phase1` had touched none of them.
Files **both** changed: 4, left alone. `git merge-base` = `3257f07`.

After adoption: **15 findings → 4 → 2.** Manifest **703 OK / 0 failed**; tests **145 passed /
4 skipped**.

---

## THE TWO REMAINING FINDINGS ARE ACCURATE, AND BOTH ARE BLOCKED ON C2

Editing a file the tag hashes has a blast radius, and this is it.

| finding | why it is not fixed here |
|---|---|
| `README.md` l.60 states the declaration's **old** sha256 | README's v30a block carries its own banner: **`FILLED AT CEREMONY TIME FROM v30a.hashes.txt. DO NOT TRANSCRIBE.`** Filling it now, by hand, is what that banner forbids |
| `DECLARATION_POINTER.md`'s CURRENT block states the old sha256 / byte count | **R15 does instruct** re-deriving the pointer in the same pass — and the purpose-built `_v30a_pointer_sync.py` **halts** first: *"the declaration on disk differs from C2's staged hash; re-stage first."* Verified by reading `v30a.hashes.txt`, which still carries `3a5790159ec4…` against the file's `12d9ee233243…` |

**Both are downstream of C2, which is A17‴'s loop, suspended pending the author's §1.2 and §1.4
rulings.** A green gate here would mean transcribing a hash block that says do not transcribe.
**The red is the correct signal**, and it says exactly one thing: the declaration changed and the
ceremony has not re-derived from it.

**Two smaller consequences, fixed because they were mine:**

- A line-keyed citation in `tools/check_registration.py` drifted — `AVAILABILITY_DECLARATION.md`
  **4339 → 4377**, the 38 lines A25 inserted above it. **The gate caught it, which is what that
  check is for.** Corrected from the gate's own report, located not guessed.
  **HELD:** this citation is **line-keyed**, so every future declaration edit drifts it again.
  Earlier rounds converted the checker's *exemptions* from line keys to **anchor** keys for exactly
  this reason. Converting this one is a design change beyond A25's scope — recorded, not taken.
- 22 adopted `_v30a_*.py` instruments and `phase7_l2_sim.py` had no manifest line on this branch and
  *"would ship inside the signed commit unattested"*. Added.

**The manifest reconciler now DERIVES.** It walks the evidence tree instead of carrying a
hand-maintained `TARGETS` tuple — the same hand-maintained-enumeration defect this whole round is
about. It rehashes a mismatch, adds an unlisted file, and **reports a listed-but-absent file without
ever removing the line**, because removing one is how an attestation quietly stops covering
something. Distinct digests **628 → 650**, asserted not to fall.

---

## A26 — A22's SIXTEEN, PRESENTED. ⛔ HALTS.

**[`A22_APPLIED_DEFECT_SET.md`](../amendment/A22_APPLIED_DEFECT_SET.md)** — unchanged since R137 and
re-presented here as §1.4 requires: each defect's text, what is actually there, and that it was
approved that way.

| class | n | what |
|---|---|---|
| 0 | 2 | the amendments block and status line the rest of the set refers to |
| A | 4 | citations of the absent block — ll.1849, 1853, 1915, 1917 |
| B | 4 | clauses describing markers never placed — l.1415, l.2013 ×3 |
| C | 1 | l.1544, citing the **deleted** §7.7 row |
| D | 3 | ll.1425, 1427, 1565 citing `SC-12(w)`'s absent limb |
| E | 2 | l.1380's zero-row table header, l.1417's orphaned row |

**Every one was approved that way**; none is an application failure. **`l.1338` is cleared** — it
cites `SC-13c(c2)`, which resolves. **The author rules the whole set at once:** correct-by-diff or
disclose-as-deviation.

---

## STILL ⏳ AWAITING APPROVAL — the two diffs

[`A23_PROPOSED_DIFF.md`](../amendment/A23_PROPOSED_DIFF.md), unchanged and unapplied. Anchors
re-verified this round at applied **l.574** and **l.579**, match count 1 each. **A25's correction to
§D.2(i) names the first of them as the only thing that discharges that obligation** — so the
declaration now points at the pending diff instead of claiming a discharge that never happened.

---

# R139 — A28 · A24 · A29 DONE ON `main`. THE DECLARATION NOW RESOLVES ENTIRELY.

**`main` is at `66ee10c`**, three commits past `8705402`. `PREREG.md` is at **`f927e67efd2b27f9…`**
— changed for the first time since the amendment, and only under R139 §1.1's approval. Tags
`prereg-v30` only. `stash@{0}` preserved.

## RE-ENTRY

`phase1` `6947d27`, gate 23 checks FAIL — 2 findings, 145 passed / 4 skipped. `main` was 23 checks
FAIL — 1 finding, D10 on `ROUND_STATE.md`. Both as §0 described.

---

## A28 — Track A's work comes back to `main`, derived not transcribed

**The set was derived.** Every file `phase1` changed since merge-base `3257f07` was attributed to
the commits that touched it, and **each commit labelled Track A or Track B from its own subject
line** — not from a path rule, because "src/ is Track B" is the hand-authored enumeration this round
exists to remove.

| | |
|---|---|
| Track A only | **43** files |
| Track B only | **32** files |
| touched by both | **3**, decided explicitly |
| of the Track A set, actually differing between branches | **13** |

The three touched by both: `MANIFEST.sha256` **re-derived here, never copied**;
`B8_PROBE_B_RESULTS.md` Track B, stays; `ROUND_STATE.md` moves, and `main`'s D10 finding was about
it.

**Losslessness checked, not assumed.** `main` had not moved since `8705402`, so its blobs are
exactly what `phase1` adopted. My ancestry check flagged `AVAILABILITY_DECLARATION.md` — because I
adopted `main`'s bytes into the working tree and edited them **before** committing, so no commit
boundary carries `main`'s exact blob. **Verified directly instead: one hunk at l.3775, every removed
line exactly A25's replaced block, 51 insertions / 13 deletions, nothing else touched.**

**`main`'s D10 finding CLEARED.**

---

## A24 — the two approved §6.2 replacements, applied

**`PREREG.md` `0c8da19f` → `f927e67e`, 2075 → 2081 lines.**

| hunk | at | what |
|---|---|---|
| **H2** | l.574 | Reference AUC anchor — the registered pair retired, replaced by an anchor **constituted by recomputation**, declared as an enumerated entry set |
| **H3** | l.579 | Contamination availability class — the recording locus moves to the declaration, because applied SC-9(b) forbids editing an evidence artifact |

**The text came from `PREREG_v30a_DIFF.md`, not from the proposal.** `A23_PROPOSED_DIFF.md` is a
derived presentation of that source; applying from the presentation would put a second copy in the
chain and let the two drift.

**Applied bottom-to-top** — H3 at l.579 before H2 at l.574. The anchors are five lines apart, so
applying the earlier first would have shifted the later one, which is exactly how an applier writes
correct text into the wrong place. Structure checked **before** the write.

**Both v30 lines are RETAINED VERBATIM** in nested blockquotes marked `SUPERSEDED BY v30a …
NOT operative` — what §8.2 item 1 promises, and what four of the amendment's five earlier deletions
did not do.

---

## A29 — the declaration's final state

**§D.2's ledger: BOTH DISCHARGED, and each by a different thing.** (i) the contamination class
**by amendment, and the amendment now exists** — A24's clause at `PREREG.md` l.582; that entry was
false from the day it was written until A24, and the gap is recorded rather than smoothed over.
(ii) the CI sliced variant **by SC-2(e), cited, and by no amendment** — §1.3's ruling. SC-2(e) is
the registered rule; the declaration supplies the instance it calls for. Same shape as §D.5
recording SC-9(c) obligations here, and SC-9(a) is respected because **no gate object is created**:
SC-2(e) already created it.

**§A.4's citation** named `PREREG.md` §6.2 *"Sliced variant — v30a, operative"*, which does not
exist. Re-pointed at **SC-2(e)**, which does. **Only the citation changes** — the obligation, its
due event and its scoring rule are untouched, and the replacement says so in its own text.

**VERIFIED: every named-clause citation in the declaration now RESOLVES — zero missing, down from
three.** All **71** distinct `SC-n` citations resolve, across **268** citations.

**§36.2 was re-surveyed before either edit.** Three other files match *"discharged by amendment"*:
`A23_THREE_CLAUSES.md` quotes the old text inside a dated audit record; `g5run1/tree` and
`g5run2/tree` are frozen snapshot copies. All dated records correct as of their dates; none touched.

### D8's citation is now ANCHOR-KEYED (§1.4)

**The pin drifted twice in two rounds on the same file** — 4339 → 4377 on A25's insert, 4377 → 4376
on A29's. §17.2 already preferred anchors; this one stayed line-pinned because its target has no
heading — but *"has no heading"* is a reason not to cite a **section**, never a reason to cite a
**line number**.

`lineno = None` now marks an entry anchor-keyed: the text must occur **exactly once**, and where it
occurs is reported rather than required. **It changes what the checker LOCATES, never what it
CHECKS** — and a duplicate anchor now **fails**, where a line pin would silently have taken the
first. The three remaining pins stay; their targets are in files this round does not touch.

**The reconciler's one-shot re-pin was REMOVED, not re-pointed.** A one-shot fix left inside a
re-runnable script becomes a landmine the moment the thing it fixed is superseded — it halted here,
correctly, on work that was done. Re-pointing it would have put a line number back into a script
whose whole subject is that line numbers go stale.

---

## STATE

| | |
|---|---|
| `main` gate | 23 checks, **FAIL — 2 findings**, both C2-blocked (§1.5), unchanged in character |
| manifest | **699 OK / 0 failed** |
| `PREREG.md` | `f927e67efd2b27f9…` |
| declaration | `79357d774b330dfa…` |

**The two remaining findings are the same pair §1.5 rules must stand:** `README.md` l.60 and
`DECLARATION_POINTER.md`'s CURRENT block carry a pre-A24/A29 declaration hash. Both clear at A17‴
when C2 re-derives. Not forced.

**Also fixed at A24: the reconciler's `PREREG.md` tripwire pinned a literal hash and halted** —
correct refusal, wrong question. Changed to assert the file is unchanged **across its own run**,
which is what the script actually promises and cannot be satisfied by editing a number.

**Next: A30, A31, A27, A17‴.**

---

# R140 — A30 · A31 · A27. ⛔ A31 HALTS: §8.2 IS NOT APPROVED CONTENT, AND ITS ITEM 1 IS FALSE.

**`main` at `1950afb`. `PREREG.md` at `15baa648cb723b79…`, 2089 lines.** Gate 23 checks, FAIL — the
two C2-blocked findings only. Manifest **703 OK / 0 failed**. Tags `prereg-v30` only. `stash@{0}`
preserved. **A17‴ has NOT been run** — see the halt below.

---

## A30 — five corrected, three sent to the author

Each of the eight was tested one at a time against §1.1's sentence — *"does nothing but make a false
existence claim true, or removes the claim, changing no substantive rule"* — and the split is
**five to three**, not eight to zero.

**Applied — five, all FRAMING NOTES, none operative.** Each correction names in its own text the
rule it leaves untouched, so a reader of `PREREG.md` can see what did not change.

| site | said | now |
|---|---|---|
| SC-6b's insertion note | *"after marker M2 **where placed**"* | M2 was drafted and never applied; the conditional hedged its own anchor instead of failing on it. **The clause below and what it governs are unchanged.** |
| SC-8b's insertion note | names the item-3 marker, SC-8's revised M2, the line-97 marker | **none was applied.** The substance survives in item 8's own body; what is missing is a marker **at** those sites, so a reader arriving at line 97 is not told. **Item 8 itself is unchanged.** |
| SC-12p's provenance note | the same correction was made for SC-12(w)'s limb | **it was not.** That limb is in SSF and not in this file; the `SC-12` record's span stops short of it. **The pointer above it is untouched.** |

**Not applied — three, all inside OPERATIVE text, and they are TWO questions, presented whole
rather than half-fixed:**

- **§7.7's deleted row.** SC-6b's clause ranges over *"every detector-case coverage state **that
  row** carries"*, and the row is gone. Making the claim true means **re-registering a row**;
  removing it means **rewording an operative clause**. Either is a rewrite.
- **SC-12(w)'s absent limb**, cited twice: SC-12p's pointer *"SC-12(w) registers the condition…"*
  and §8.3's *"whose (w1) prohibits the state outright"*. Landing the limb — **it is approved
  content, inside SSF** — and deleting both citations are both substantive, and they are **one**
  question.

Anchors located, never offset: every line moved by six at A24. Register form checked — the
corrections use the file's dominant curly-quote style, **360 against 59**.

---

## A31 — ⛔ HALTS, and on two independent grounds

**Artifact: [`A31_AMENDMENTS_BLOCK.md`](../amendment/A31_AMENDMENTS_BLOCK.md)** — the block
assembled and presented in full. **Nothing applied.**

### Ground 1 — §8.2 is not approved content

Authority was established **before** anything was assembled, because assembling first and asking
afterwards is how an artifact becomes its own argument. `APPROVAL_RECORD.md` §140 records what the
author approved on **25 August 2026**, and it is a **closed list of three**:
`PREREG_v30a_APPROVAL.diff` (`c5d89db1…`), `SCHEMA_SET_FINAL.md` (`32358f6d…`), and the `PREREG.md`
base blob. **Both hashes verify byte-exact on disk.**

`BLOCK_MANIFEST.md` l.141 names three components, from two documents:

| component | source | in the approval? |
|---|---|---|
| **§8.2, the block proper** | `K2_AMENDMENT_LEDGER.md` | **NO** |
| §AB | `SCHEMA_SET_FINAL.md` | yes |
| §AC | `SCHEMA_SET_FINAL.md` | yes |

**The largest of the three is not approved content.** §AB and §AC are; the block that would carry
them is not. The block would need a **fresh approval**, exactly as the two §6.2 diffs got one.

### Ground 2 — §8.2 item 1 is FALSE of the file it would describe

Item 1 is the first thing the block asserts: *"**No registered sentence is deleted from this
file.**"*

**Derived from the two files, not from any approval's removal list** — because A24 superseded two
further lines under a second approval, so a population taken from the first would miss them.

| v30 line | retained? |
|---|---|
| 445 | **RETAINED** at l.575, marked |
| 450 | **RETAINED** at l.583, marked |
| 1022 | **RETAINED** at l.1688, marked |
| **461, 855, 929, 1030** | **NOT RETAINED** |

**Seven superseded sentences: three retained with a marker, four not.** *(R140 §1.2 put it at two
and four; that missed v30 l.1022, which A20b had established was retained verbatim with a marker.
The figure is three and four.)*

**The two clauses A24 applied are exactly the pattern item 1 describes** — both retain verbatim,
both marked. Four earlier deletions do not. **Landing §8.2 as drafted would put a false claim about
the amendment into registered text, false in the way the block exists to prevent.**

**Three options are laid out in the artifact and NONE is chosen**, per §1.2: land it and disclose
the discrepancy; retro-retain the four so item 1 becomes true; or do not land it, in which case the
four block citations join A30's correction class and the two absences become disclosed deviations.

**What the block would resolve, of A31's six: FIVE.** The four block citations and the missing block
itself. **Not** the missing `**Amendment status:**` line — that is §8.1, a separate hunk at line 6,
not assembled here.

---

## A27 — the change list becomes derived

The hash lines beside it were already derived — *"the output of C2, pasted, never retyped"*, with
`v30a.hashes.txt` as their authority. **The change list had none.** It now has
**`v30a.changes.txt`**, generated by `a27_derive_changes.py`, and §3.5 carries a placeholder
instead of prose.

**Derived from the two files, not from an approval record.** R140 offered `SCHEMA_RECORDS.json` or
the approval diff; both are now too narrow **in the opposite direction** — A24 superseded two
further lines under a second approval, so a list built from the first would omit changes that ARE
there. The pair of files is true however many approvals accumulate.

> Amends PREREG.md: §6.2 Acceptance fixture: line 445, line 450, line 461; §7.7 Completion, and the
> two levels of state: line 855; §8.3 Three assertions: line 929; §10.1 Phase 0 kill gate —
> objective: line 1022; §10.2 Other kill / pause criteria: line 1030.

**No summarisation.** A first version named each change by its first bolded phrase, which truncated
§10.1's mid-word (*"…and is silent on fi"*) and reduced §10.2's to an arrow. **A hand-summary — even
a generated one — is a second description of text that already exists, and it drifts.** The list
names the **surface**; a reader who wants the sentence fetches it with `git show
prereg-v30:PREREG.md`, which the message already tells them.

**Scope determination, recorded.** §0.2.1's class table classifies what a **measurement** may
resolve about `PREREG.md` — its column is *"Phase 1 may"* and class C is *"a class C amendment to
**this file**"*. It does not reach `CEREMONY_COMMANDS.md`, which is the procedure that produces the
tag, not a registered object. **The edit is §187's ordinary case: a stale verification value
corrected at its source.**

**`tagmsg.txt` is not regenerated here** — C2f compares it against C2's own output, and C2 is
A17‴'s.

---

## WHY A17‴ HAS NOT RUN

A17‴ produces the commit that becomes the tag target. **A31's halt means the registered text may not
be final:** if the author chooses option 2 — retro-retain the four deletions so item 1 becomes true —
that is a further `PREREG.md` edit, and the loop would have to run again over a superseded result.
Running it now would produce a tag target likely to be discarded. **Held for the ruling.**

## INSTRUMENT NOTES

| | |
|---|---|
| the reconciler's `PREREG.md` tripwire pinned a literal hash and halted at A24 | correct refusal, wrong question — **changed to assert the file is unchanged across its own run**, which is what the script promises and cannot be satisfied by editing a number (§2.2) |
| the reconciler still carried a one-shot line re-pin | **removed, not re-pointed.** A one-shot fix inside a re-runnable script becomes a landmine when the thing it fixed is superseded |
| two indirect `python -c` patches misfired on quote style | switched to the Edit tool. The same class as D2.1, one layer up: a patch that spells the text it edits can misspell it |

---

# R141 — A32 ASSEMBLED AND ⛔ HALTING · §9.2 STARTED, SIX COMPARATORS REACHABLE

**`main` at `26d4856`. `PREREG.md` unchanged at `15baa648cb723b79…`, 2089 lines** — A32 applies
nothing. Gate 23 checks, FAIL — the two C2-blocked findings only. Manifest **705 OK / 0 failed**.
Tags `prereg-v30` only. `stash@{0}` preserved.

## A32 — one fresh approval diff, four independently approvable hunks

**Artifact: [`A32_PROPOSED_DIFF.md`](../amendment/A32_PROPOSED_DIFF.md). NOT APPLIED.**

| # | hunk | act | source | source sha256 |
|---|---|---|---|---|
| 1 | §AB — the 816/830 duplicated-authority record | **EXTRACTED** | SSF ll.1632–1679 | `32358f6d…` **= the approved hash** |
| 2 | §AC — the seven `PREREG.md` disclosures | **EXTRACTED** | SSF ll.1687–1737 | `32358f6d…` **= approved** |
| 3 | SC-12(w)'s limb | **EXTRACTED** | SSF ll.1145–1181 | `32358f6d…` **= approved** |
| 4 | §7.7's row — operative + retention | **EXTRACTED, weaker provenance** | `X5_FINAL_PREREG_DIFF.md` | `a19ef629…` **not approved** |

**SSF was verified equal to the approved hash before anything was extracted from it.**

### Hunk 4 is flagged, not smoothed

`X5_FINAL_PREREG_DIFF.md` is not one of the three approved artifacts — **and its own finding O-11
says the operative row *"is nowhere quoted verbatim in `SCHEMA_SET_FINAL.md`"* and was recovered
from a scratch applied file**, adding in terms: *"the author should not have to reconstruct
operative registered text from a scratch artifact in order to sign it."* **That is exactly what
hunk 4 asks**, and the hunk says so at the top.

### Placement — no container invented

§AB and §AC were anchored inside §8.2's block, which does not land. **They do not need a new one.**
`SCHEMA_SET_FINAL.md` l.77 fixes the application order — *"SC-12 (revised) → SC-13a → SC-13b →
SC-13c → **§13c-P → §AB**"* — and §13c-P is the §7.2.1 line-816 pointer, **which is applied**.
`BLOCK_MANIFEST.md` row 36 puts §AC immediately after §AB. **A32-placement's first branch fires**,
which matters: §8.2's item 1 is exactly the kind of claim a container must not reintroduce.

### Two extraction failures on the way, both refusals rather than guesses

- **`BLOCK_MANIFEST`'s §A ranges cover apparatus as well as applied text.** §AB's range opens on a
  change note. SSF §0.2 draws the line — only THE CLAUSE, SUPERSESSION MARKER and INSERTION TEXT
  enter `PREREG.md` — so the extractor narrows to the blockquote. Taking everything between the
  first and last quote marker swept §AB's tail into §AC's range, and **the contiguity check
  refused**; the fix was to take the run carrying the expected text.
- **Anchoring §AB on §13c-P's paragraph would have placed it INSIDE a fenced code block.** The
  pointer lives in a fence. The anchor is the **block**, located from its marker and closed at its
  fence — never by counting lines.

Anchors, all match count 1: §13c-P's block ends **l.1346**; §7.7's table header **l.1385**; SC-12's
clause heading **l.1776**.

**A third option is named, not drafted.** The orphaned `| **Strategy diagnostic** |` row at l.1423
renders as a paragraph; landing 4a leaves the table well-formed with **one** row. Moving it back
would repair the structure — a hunk nobody asked for, so it is named rather than written.

---

## §9.2 — STARTED. Step 1 done: the comparators are reachable.

**Artifact: [`W2B_API_INVENTORY.md`](../killgate/w2b/W2B_API_INVENTORY.md), on `phase1` at
`0885766`.**

§9.2's first question is not *"what did the tools report"* but ***"can they be called at all."***
W2b exists because k6's nulls were uninterpretable, and **a control written against an API that has
moved fails for the wrong reason — which is precisely what would be mistaken for a tool that does
not fire.** So each package was imported **in its own venv** and its surface read, rather than
trusting k6's two-round-old runners or memory.

**All six runnable comparators import; every entry point k6 used is intact.**

| venv | tool | version |
|---|---|---|
| `general` | `leakage-buster` | 1.0.2 |
| `general` | `leakfence` | 0.5.0 |
| `general` | `temporalcv` | 2.3.0 |
| `general` | `Leakly` | 0.1.2 |
| `ld` | `leak-detect` | 0.0.1 |
| `dc` | `deepchecks` | 0.19.1 |

Versions match `k6/env/VERSIONS.txt`, captured 14 Aug 2026 **before results were read**.

### Two findings that change the plan

- **Leakly ships BOTH fixtures** — `load_example_leakage_config()`, which W2b names, **and
  `load_example_nonleakage_config()`**. A vendor-supplied **positive *and* negative pair** is
  stronger than a positive alone: **a tool that fires on both is not discriminating, and only the
  pair shows it.**
- **`temporalcv.gates` is a module, and `gate_suspicious_improvement` is the gate k6 got wrong** —
  W2b defect #7 records it was fed an **accuracy** where the formula expects an **error** metric, so
  a mapped gate silently never fired. **The control must pass an error metric and must be seen to
  fire.**

**This establishes reachability ONLY.** Nothing here says any tool detects anything. W2b step 2 —
each adapter demonstrated to fire on a documented positive **through the same invocation path the
real run uses** — is next, and until it passes for a tool, **that tool's acceptance-fixture result
is `uninterpretable`, not a null.**

**Not runnable, and not re-litigated:** `leakr` and `bioLeak` need R; `leakage-analysis` needs
`souffle`; `LeakageDetector` is a VS Code extension. All four recorded at k6.

---

# R142/R143 — A33 APPLIED · ⛔ A33b HALTS ON SIXTEEN UNSEEN LINES · A35 DONE · §9.2 AT THREE OF SIX

**RE-ENTRY, both branches.** `main` `682566c`, `phase1` `a8263e7`, both trees clean, index clean,
tags `prereg-v30` only, `stash@{0}` preserved. `main` 23 checks / 2 findings; `phase1` 23 checks /
3 findings. **EXPECTED on both — reported, not forced.**

**§0 was stale in three places**, and RE-ENTRY is what established it: A33 was **committed**, not
uncommitted; the line count is **2228, not 2212** (2212 was the truncated first application); and
**A35 was already done and committed**. A34 had been attempted and halted.

## A33 — hunks 1–3 applied, `+139 −0`

| block | at | lines |
|---|---|---|
| §AB | ll.1348–1395 | 48 |
| §AC | ll.1397–1447 | 51 |
| SC-12(w)'s limb | ll.1921–1957 | 37 |

**The first application was defective and was reverted before it was committed.** It trusted
`BLOCK_MANIFEST.md` and wrote §AB and §AC each eight lines short — **cutting §AC's disclosure 7
mid-sentence and dropping the block's closing paragraph.** Caught by reading the applied tail.
Extents are now derived from each blockquote's own delimiters: **a declared range is an assertion;
the block's extent is a fact about the file.**

**Dependent clauses, verified by reading.** l.1538 SC-12p's pointer → the limb at l.1921. l.1676
§8.3's *“whose (w1) prohibits the state outright”* → (w1) at l.1927, *“NO DETECTOR-CASE MAY BE
REPORTED `waived`. LICENSED GROUNDS: NONE.”* And **l.1533 A30's provenance note now reads FALSE** —
hunk 3 falsified every clause of it. **A33 created that defect;** it is A34's.

## ⛔ A33b — the sixteen lines require their own approval

**Artifact: [`A33B_SUPERSEDING_PRESENTATION.md`](../amendment/A33B_SUPERSEDING_PRESENTATION.md).**
Supersedes `A32_PROPOSED_DIFF.md` **as a presentation, not as a record** — that file stays frozen at
`26d4856`, because rewriting it would destroy the only evidence of what was actually approved, which
is the gap this document exists to close. The generator **halts if it is dirty.**

| block | presented | applied | declared | true extent |
|---|---|---|---|---|
| §AB | 40 | **48** | ll.1632–1679 | **ll.1640–1687** |
| §AC | 43 | **51** | ll.1687–1737 | **ll.1695–1745** |
| limb | 37 | 37 | ll.1145–1181 | ll.1145–1181 |

**Proved, not asserted:** the applied text is the presented text **plus a suffix** — prefix equality
line by line, deliberately not substring containment, which would also pass if a line had been
inserted in the *middle*. **The sixteen lines are read out of SSF, never retyped**; a presentation
that spells its own subject can misspell it.

**They are not a formality.** §AB's eight carry *“**The operative conflict is registered-text-internal
— line 816 against line 830.**”* §AC's carry disclosure 7's conclusion and *“**These seven are
disclosed because the record should not have to be reverse-engineered to find them.**”*

## The offset, derived across the whole table

**Seven** decidable §A rows are eight lines early — 23, 24, 26, 28, 31, 33, 36 — against **twenty-one**
correct. Six BOTH and seven NEITHER are reported **UNDECIDABLE rather than forced**: a tidy boundary
manufactured out of ambiguity is the failure this exercise exists to catch. Rows 34–35, annotated
*“moved here R53/Y1”*, are correct because they were re-derived after the shift.

**Entry 23 declares the limb at 1137–1173; its true extent is 1145–1181.** A32 used the true range,
so **the limb was applied correctly by luck, not by check** — and my A33 commit's claim that it
“MATCHES” was measured against A32, not against the manifest.

**Row 28 is SC-13a, a fifty-nine-line clause that was applied**, so truncation in already-registered
text was a live risk and was **checked, not assumed**: **41 rows — 0 TRUNCATED, 24 complete, 9 absent
(markers and apparatus), 8 no-structure.** SC-13a's 59, SC-13b's 68, SC-13c's 101, SC-4's 159 all
present in full.

**Why the gate did not catch it.** `block_reachability` asks whether a block is **reachable** — a
block truncated at its *tail* still has its opening line, so it passes. `block_manifest_counts`
audits the table's **shape** and never compares a range against SSF. **Reachability and completeness
are different questions, and only the first was being asked.**

## A35 — hunk 4 does not land

**Artifact: [`A35_DISCLOSURE_DRAFT.md`](../amendment/A35_DISCLOSURE_DRAFT.md). HELD, NOT APPLIED.**

Line 1080 decides it: *“**Every published preserving or promoted metric reads this state**, never the
detector-case state of §7.7.”* All four consumers tested separately — `assert_audit_complete()` names
its states by name, `unscored` is named expressly in SC-6b's own clause, §8.2 carries its own
enumeration, and no runtime metric reads §7.7 at all. **SC-6b's extension is a no-op, not a break.**

**What the empty range costs, since a no-op is not the same as no effect:** `waived` falls outside
§8.2's display prohibition. **The gap is closed by SC-12(w)(w1)'s outright prohibition** — no entry
can exist to be displayed. **The protection is at entry, not at display.**

**Two defects disclosed.** SC-12(w)'s limb opens *“§7.7's table carries `waived`… It is the only
state in that table without one”* — **§7.7's table has zero data rows**, so the uniqueness claim is
**vacuous over an empty set**. It is approved content applied verbatim, so this is **not A33's
error**. Separately, `| **Strategy diagnostic** |` sits **thirty-six lines below the separator**,
outside the table. **Named, not written.**

## A34's §2.2 sweep — READ-ONLY, reported before anything is edited

**The registered repair set is exactly five sites**: the four block citations (ll.1998, 2002, 2064,
2066) plus A30's provenance note (ll.1528–1536). **A31's count of four was right** — a raw grep found
five because it ignored fence state; l.1344 is §13c-P's fenced *specimen*.

**A false all-clear was caught.** The first sweep matched line-by-line and returned **zero** hits in
every registered object — wrong in the worst direction, because the known hit spans a line break.
**Prose wraps; a line is not a unit of meaning.** Matching over paragraphs took 18 hits to 40 and 0
registered hits to 2. **A silence is checked, not reported.**

**Of 38 supporting-artifact hits, none should be edited.** SSF still annotates §AB *“(revised;
drafted, not applied)”*, now false — but SSF is **frozen at the approved hash**, so it is
disclosable and not fixable. The rest are dated records: **superseded, never rewritten.**

## Also found

**§13c-P was never applied.** Of 23 v30a markers, **exactly one — SC-13c-2 at l.1338 — still carries
unapplied `INSERT` apparatus**; the pointer exists only as a fenced specimen. **§AB asserts *“a
pointer to the exception is inserted at line 816's own site.”* It is not.** My R141 record said
§13c-P was applied; **the file contradicts it.**

## TRACK B — §9.2 step 2, three of six DISCRIMINATING

| tool | vendor negative? | positive | negative | verdict |
|---|---|---|---|---|
| **Leakly** 0.1.2 | **YES** | leaky median AUC **0.635** | clean **0.519** | **DISCRIMINATING** |
| **temporalcv** 2.3.0 | no | MAE +0.980 → **HALT** | +0.012 → PASS | **DISCRIMINATING** |
| **leakfence** 0.5.0 | no | `group_overlap`, `duplicate_rows` | silent | **DISCRIMINATING** |
| leakage-buster 1.0.2 | no | — | — | **uninterpretable** |
| leak-detect 0.0.1 | — | — | — | **uninterpretable** |
| deepchecks 0.19.1 | — | — | — | **uninterpretable** |

**Leakly's pair is the vendor's own** and differs in exactly one key — where `data_split` sits — which
the control **asserts** rather than assumes. Labels are permuted first, so **the only thing that can
produce an above-chance score is leakage**. **13 of 15 seeds separate**; a first run at three seeds
put the clean median at 0.540 with one draw deciding it.

**temporalcv: defect #7 REPRODUCED.** Fed the identical leakage as an *accuracy*, the gate reports
*“Improvement **−76.4%** is reasonable.”* **k6's null was an unfired instrument** — demonstrated, not
inferred. Direction was read out of the **source**, not guessed from parameter names.

**leakfence: my adapter was wrong, not the tool.** The first run recorded `check_duplicates` as not
firing on a byte-identical row. `audit_split` returns an AuditReport with `.violations`;
`check_duplicates` returns a plain **tuple**. Had it stood, **a finding about my call would have been
written down as a finding about the tool** — the same shape as defect #7. The adapter now **raises on
an unrecognised return shape** rather than returning an empty list, because an empty list reads as
*clean*.

## INSTRUMENT NOTES

| | |
|---|---|
| an ambient instruction told the agent to edit files with `sed`/heredocs | **D2.1 outranks it.** Shell used for reads and searches; the file-write tool for content; the conflict flagged, not silently resolved |
| the A34 sweep's first version matched line-by-line | **false all-clear** on every registered object — fixed to match over paragraphs |
| the leakfence adapter read `.violations` off a tuple | recorded a live detection as a non-firing tool; now **raises** rather than returning empty |
| `grep -c $'\r'` as a line-ending probe | **measured nothing**; replaced with a byte-level count, which showed `evidence/amendment/*.md` has **no single convention** (39 LF / 16 CRLF) and that nothing needed “correcting” |
| my A33 commit said the limb's declared range “MATCHES” | it matched **A32's** range, not `BLOCK_MANIFEST`'s, which is also eight early |

---

# R144 — A37 · A36 · A38: THE RECORD COMES INTO THE REPO · §9.2 STEP 2 COMPLETE

**RE-ENTRY.** `main` `b1b2ed9` → `451555b`; `phase1` `ac065f3` → `cfb8a89`. Trees clean, index
clean, tags `prereg-v30` only, `stash@{0}` present and **now pinned**. `main` 23 checks / 2 findings;
`phase1` 23 / 3. **EXPECTED on both.**

## A37 — the held banking is GC-proof, and its contents are finally named

`git branch backup/held-banking stash@{0}` → **`655f613`**, identical to the stash commit. **The
stash is not applied, popped or dropped** — R144 §6 reserves that to A15, and the branch ref is the
only write.

**The inventory prior rounds never gave: `stash@{0}` contains EXACTLY ONE FILE** —
`evidence/session/ROUND_STATE.md`, +92 lines. **The "held banking" was the report itself.**

## A36 — the contradiction dissolves, and the fault was my instrument

| question | answer |
|---|---|
| tracked? | **yes** — `evidence/session/ROUND_STATE.md`, on **both** branches |
| history | **fifteen commits**, continuous, never deleted |
| manifest | **attested**, line 896 |
| `main` HEAD | `b1b2ed9`; **A33 (`2ca816c`) IS an ancestor** |

Last round's sentence — *"does not exist, is not tracked on either branch, and has never been
committed"* — was **true of the path `ROUND_STATE.md` at the repo root**, which is what `ls`,
`git ls-files`, `git ls-tree` and `git log` were every one of them given. **It was stated about the
file.**

**That is H-L21, narrower than its claim: the population was a filename, not the tree.** The same
turn found the real path minutes later and used it correctly throughout — **so the work was right
and only the sentence was wrong, which is the more dangerous shape**, because nothing downstream
failed and nothing flagged it.

## A38 — 68 lines that existed in no committed file

**Tested by line-set containment, not by diff.** The committed file has moved through fifteen
commits and its header is rewritten every round *by design*; a diff would bury the only question —
**is any HELD line MISSING** — under thousands of expected changes. Blank and rule lines are excluded
so a file of blanks cannot score as contained.

> **before: 68 substantive held lines, 0 present in any committed file**
> **after : 68 of 68 present, 0 missing**

**What was at risk:** the **A9 ALL-GREEN TABLE** (23 checks, 137 passed, C2 identical against all
five surfaces), **the point at which §1.6 attaches**, and **two recorded defects of mine** — a broad
`re.sub` that flattened a dated historical record twice, and a `grep` in a pipeline that masked the
gate's exit status.

**A gap, not a divergence.** The committed record ran A5.3 straight into `# R134`; the stash holds
exactly the A5.4/A6/A5.5/A7/A8/A9 section that belongs between them. **Checked for a competing
account before concluding it** — the only mention of `d39643e` in the committed file is a passing
reference inside R134's section.

**Inserted verbatim and marked, not rewritten.** A banner records that the section was held from 26
to 27 August 2026, and that **its A9 run is SUPERSEDED AS A VERIFICATION and STANDS AS A RECORD**: it
ran against `d39643e`, and **sixteen commits have landed on `main` since**, so it attests nothing
about the present tree. Every figure is left as written — **a dated record correct as of its date is
not a stale verification value.**

**The hold-rationale had lapsed.** Banking was held out of the repo so the tag-attested tree would be
exactly the tree A9 verified. **That tree was reopened sixteen commits ago.** Holding the record
outside the repository had stopped protecting anything and was only risking it.

## TRACK B — §9.2 STEP 2 COMPLETE. SIX OF SIX.

**Artifact: [`W2B_STEP2_CONTROLS.md`](../killgate/w2b/W2B_STEP2_CONTROLS.md).** Discharges §D.5(i)'s
precondition; publishes no Phase 1 result; does not block the tag.

| tool | version | vendor negative? | POSITIVE | NEGATIVE | verdict |
|---|---|---|---|---|---|
| **Leakly** | 0.1.2 | **YES — the only one** | AUC **0.635** | **0.519** | **DISCRIMINATING** |
| **temporalcv** | 2.3.0 | no | **+0.980 → HALT** | +0.012 → PASS | **DISCRIMINATING** |
| **leakfence** | 0.5.0 | no | `group_overlap`, `duplicate_rows` | silent | **DISCRIMINATING** |
| **leakage-buster** | 1.0.2 | no | 2 × `high` | 0 × `high` | **DISCRIMINATING** |
| **leak-detect** | 0.0.1 | no | returns **True** | returns **False** | **DISCRIMINATING** *(NaN-only)* |
| **deepchecks** | 0.19.1 | no | **1.0000** / **1.0000** | **0.0000** / **0.0000** | **DISCRIMINATING** |

All six: **pip from the PyPI index**, no `direct_url` — index installs, not VCS or local.

**Two findings about the tools.** *temporalcv:* fed the identical leakage as an **accuracy** the way
k6 fed it, the gate reports **“Improvement −76.4% is reasonable”** — **k6's null was an unfired
instrument**, now demonstrated rather than inferred. *leak-detect:* its **vendor default is broken**
against NumPy 1.26.4 (`np.complex`, removed in 1.24); it works in NaN-only mode, and the breakage is
kept as its own limb because the default is what an adapter written from the signature would use.

**AGPL-3.0-or-later, determined.** deepchecks is AGPLv3+ by classifier — its `License` field is
literally `UNKNOWN`, so the classifier is the authority. **Interoperation is not vendoring**: a
separate program in its own virtualenv, no source copied, nothing modified or redistributed, §13's
network clause not engaged. **The determination lapses** if any of that changes.

### Four adapter defects of mine, every one caught before anything was recorded

| tool | what my adapter did | what it would have been recorded as |
|---|---|---|
| leakfence | read `.violations` off a plain **tuple** | *“does not fire on identical rows”* — it had detected them |
| leak-detect | ran the **crashing vendor default** | *“does not discriminate”* — a different fact entirely |
| leak-detect | `ret is not None` on a **bool** | *“fires on the clean case too”* — `False` is an answer, not an absence |
| deepchecks | `train_dataset=` to a **SingleDatasetCheck** | *“the positive did not fire”* — the call never happened |

**A raise is never evidence about a tool; it is evidence the call did not happen.** Every shape
resolver now **raises on an unrecognised shape** rather than returning empty, because empty reads as
*clean*. **Each of the four would have been a plausible, publishable, false finding about someone
else's software** — and each was caught by checking my own call first, which is the discipline W2b
applies to vendors, turned inward.

---

# R145 — RE-ENTRY VERIFIES A38 ALREADY COMPLETE · `aggressor_side` PROPOSED, NOT BUILT

## RE-ENTRY — HEADs reported explicitly, as R145 requires

| | |
|---|---|
| `main` HEAD | **`caf87ee761464fa17e92d6c18eb7dab364f8ff0c`** |
| `phase1` HEAD | **`cfb8a891835116b7daa016adacb96efa3fd35c38`** (→ `5295089` this round) |
| working / index | **clean on both**; untracked ceremony files only |
| tags | **`prereg-v30`** only — no unexpected tag |
| `main` gate | 23 checks, **FAIL — 2 findings**, the C2-blocked pair. `round_reconciliation` **PASS** |
| `phase1` gate | 23 checks, **FAIL — 3 findings**, those plus **D10** |

**`phase1`'s D10 has NOT cleared, and the mechanism is now evidenced:**

| copy | sha256 |
|---|---|
| pinned work-root | **`3dc4e498…`** |
| `main` committed | **`3dc4e498…`** — identical |
| `phase1` checked-out | `1bafc19e…` |

**D10 hashes the checked-out tree.** On `main` the work-root copy finds its twin; on `phase1` it
cannot, because `phase1`'s copy has not moved since before R134. **Not a defect — the settled
branch-split property, with the hashes behind it rather than the label.**

## §0 WAS STALE IN FOUR PLACES — established by derivation, not memory

| §0 said | the tree says |
|---|---|
| *"A33b's superseding presentation has not yet been produced"* | **produced at `094486d`**, 89 lines, the sixteen in full |
| *"§9.2 … step 2 next"* | **COMPLETE at `cfb8a89`** — six of six |
| *"A35 pending"* | **done at `4585994`** |
| A38 listed as this round's work | **done at `451555b`** |

## A38 — verified complete, and it took the branch §1.1 cares about

`a38_reconcile_sources.py` re-run: **68 held lines carrying text, 68 present, 0 missing.** The
**UNIQUE** branch was taken at R144 and the framing §1.1 requires is already in place — the banner at
ll.521–535 dates the section, names it the `d39643e` pass, and marks the A9 run **superseded as a
verification, standing as a record**, *above* the `THE CEREMONY PASSED` heading at l.538. **It cannot
be read as current status**, which was the whole hazard.

**The stash is redundant by construction. It is not dropped** — R145 §6 reserves that to A15's
verify-and-drop, and `backup/held-banking` stays until then.

## TRACK B — `aggressor_side`: PROPOSED, NOT BUILT

**Artifact: [`AGGRESSOR_SIDE_CLASS_PROPOSAL.md`](../phase1/AGGRESSOR_SIDE_CLASS_PROPOSAL.md).**
Nothing built: no detector, `detectors.py` untouched, no registered text edited, no new
`evidence_outcome` value.

**Recommendation: no third detector.** Promote the existing screen from a diagnostic to a
**reporting obligation** — every silent-but-referenced column named with its enclosing function and
receiver, published as **`covered_with_exclusion`, never a pass**.

**The blindness is structural.** `valueread` permutes within the observed domain and the predicate is
false across all of it; `nullread` substitutes a null, also outside the `isin` set. **And the OOD
strategy does not merely miss it — it is INELIGIBLE:** `aggressor_side` is an `object` column, and
`_ood_target_dtype` returns `None` for `object` in terms — *"every value is representable, so no
insertion can change the dtype. There is nothing to promote TO."* It **refuses as `Unsupportable`**
rather than running and reporting silence. **A refusal and a silence are different facts, and only
one of them is evidence.**

*(I first wrote that row as "an out-of-distribution sentinel" — wrong twice: it is out-of-**dtype**,
and here it does not run at all. Corrected by reading `corruption.py` instead of trusting the shape
of the name.)*

**The real defect is in the report, not the suite.** The guard is unsatisfied on **this** corpus; on
one where `aggressor_side` holds `"B"` the dependence is live. **A suite reporting `none` makes a
claim about all corpora from evidence about one** — and §6.6 already registers `observed_silence` ≠
`none` (l.1101), while §39 already requires silence to carry its domain. **The vocabulary exists and
is not being used.**

**Why not a satisfying-value probe (Option A): its domain cannot be stated.** It would work on
`isin([...])` and silently find nothing for `x > threshold`, a regex, a lookup, or any computed
set — and *"found no candidate values"* renders as silence, which reads as clean. **That is the
never-fired-reads-as-clean failure, hit four times in adapters in a single sweep.** Secondarily, the
class has **one** member, and a detector firing that rarely can never be calibrated.

**Why not a fourth `evidence_outcome` value (Option B):** §6.6's resolver has **ten legal pairs of
fifteen** — verified against the registered table — so adding one is a class C amendment needing its
own approval. It is also **the wrong axis**: `evidence_outcome` describes what an *execution*
produced; this is a fact about what the *source* references.

**What the recommendation would NOT establish, stated so it is not oversold:** the screen does not
find constantly-false predicates. It finds **columns referenced but unmoved — a superset**; a
candidate may be a dead branch, a cross-frame name collision, an unprobed frame, or a genuine dead
predicate. **Every candidate stays a question for a human.** Three conditions that would change the
recommendation are named in the artifact; **none holds today.**

---

# R146 — A34 CORRECTS FIVE SITES · ⛔ A36b HALTS ON A COLLISION · A39 FIXES EIGHT RANGES

**RE-ENTRY.** `main` `7f3f1a8` → `09d4ca0`; `phase1` `5295089`. Trees clean, tags `prereg-v30` only,
`backup/held-banking` == `stash@{0}`. `main` 23 checks / 2 findings; `phase1` 23 / 3. **EXPECTED.**
**§0 was stale in one place:** B-1's step-2 results were already in the report and the chat at R144.

## A34 — five corrections, and the obvious anchor was the wrong one

**The citation form was chosen against the obvious candidate.** §AB's headline — `RECORDED DEFECT,
NOT RESOLVED BY THIS AMENDMENT` — is the natural anchor. **Quoting it in four citations would have
put it in the file five times, and D8 resolves an anchor only when it occurs exactly once.** The
obvious fix destroys the property that makes the citation resolvable.

So the block is named by **section plus a non-colliding descriptor**: *“the v30a recorded-defect
block in §7.2.1”*. Verified before writing — `recorded-defect` occurs **zero** times, and §7.2.1
(ll.1322–1454) contains **exactly one** such block. `§AB` is not used: it is SSF's label, occurs zero
times in `PREREG.md`, and would point at nothing.

| site | was | now |
|---|---|---|
| l.1999 | *“the amendments block records”* | the v30a recorded-defect block in §7.2.1 |
| l.2003 | *“recorded in the v30a amendments block (SC-13c(c2))”* | same form |
| ll.2064–2065 | **spans a line break** | the newline and its `> ` are part of the match |
| l.2067 | *“recorded in the amendments block”* | *“recorded in that block (§7.2.1)”* |
| l.1533 | A30's note — **true when written, falsified by hunk 3** | the limb **was applied and is in the file** |

The provenance note is **spliced between anchors, never respelled** — it carries em-dashes and
backticked identifiers, and a patch that spells the text it edits can misspell it.

### A34b — the same trap, two paragraphs later

Having carefully not quoted §AB's headline, A34 **quoted SC-12(w)'s limb heading verbatim**, taking
`(w) ENTRY CONDITION FOR` from 1 occurrence to **2**. A34's guard asserted §AB's anchor and nothing
else, **so nothing failed**. **A guard that pins one invariant does not pin its neighbour.** Caught
by verifying the effect **by reading**, not by trusting the applier's own OK lines. Repaired to *“as
SC-12(w)'s entry-condition limb in §10.2”*; A34b asserts **both** anchors, because checking one is
the defect it repairs.

**Post-fix sweep run and reported:** 125 files, 41 hits, **one** in a registered object — the
provenance paragraph, matching on *“stops short”* + *“SC-12(w)”*. **Over-collection by design; the
surviving sentence is true.** No further registered site needs correcting.

## ⛔ A36b — §13c-P presented. It halts on a collision, not on the extraction.

**Artifact: [`A36B_13cP_POINTER.md`](../amendment/A36B_13cP_POINTER.md). NOT APPLIED.**

The pointer **is** in SSF at the approved hash `32358f6d…`, verified before a line was read.
Extracted verbatim from **SSF ll.1612–1616**, the fence under §13c-P's `INSERT AFTER` apparatus.
**`BLOCK_MANIFEST` row 32 declares ll.1604–1608 — eight early — so extracting inside the declared
range would have returned nothing at all.** A **byte-identical** copy already sits at `PREREG.md`
l.1344 inside the unapplied specimen, so applying changes no wording, only its status.

**What halts it:** the pointer's last sentence cites *“the v30a amendments block”* — **the container
that does not exist, and the exact phrase A34 removed from all four operative sites one commit
earlier.** Applying it verbatim re-plants the false citation.

| option | what it costs |
|---|---|
| apply verbatim | faithful to approved content; **plants a citation needing its own A34-class correction** |
| apply with the citation corrected | leaves the file consistent; **no longer verbatim extraction**, so it needs its own approval, exactly as the sixteen lines did |
| do not apply | nothing false is added; **§AB's pointer assertion stays false** and joins HELD |

**No recommendation is offered** — a presentation that arrives with its own preferred answer has
stopped being an extraction.

## A39 — eight ranges fixed, sixteen refused, and the first attempt was worse than the defect

`BLOCK_MANIFEST.md` is a working document, so §1.4 fixes rather than discloses. **Eight rows
corrected — 23, 24, 27, 28, 29, 30, 33, 36 — every one exactly +8.** A note above the §A table now
states the ranges are **derived** and warns against extracting inside one without re-deriving it.

**The first version wrote invented numbers that looked derived, and was reverted before commit.**
Taking `extent(first) or extent(first + 8)` and writing the result **expanded** rows that
deliberately declare a **sub-range** of a longer run — row 1a's 150–153 became 150–159, swallowing
row 1b whole; row 14a's swallowed 14b, 14c and 14d — and **short-circuited**: row 32's
`extent(1604)` found the ANCHOR fence, so `extent(1612)`, where A36b had just proved the INSERT
fence is, was never tried, and rows 31 and 32 both collapsed onto `1604-1604`.

**A block that moved keeps its length.** Length preservation is now the acceptance test. **Sixteen
rows have no length-preserving candidate and are left untouched and named** — several certainly
stale, 26, 31 and 32 among them. **A number the instrument cannot derive is one it must not write.**

**D10 earned its keep.** `round_reconciliation` failed on `main` immediately after A39, because the
pinned work root held `BLOCK_MANIFEST.md` at its **pre-A39 hash** and no longer had a twin. Synced as
bytes, re-gated: **PASS**. This is precisely the drift the check exists to find, caught in the same
round the file changed.

## TRACK B — §9.2 step 3: preconditions established, runs NOT started

**B-1 was already discharged at R144** — the six-of-six table reached both the report and the chat.

**Step 3's preconditions are established and one of them is a finding.** `fixture_adapter.read_inputs`
/ `builder_for` are intact, and the fixture's producing code is reachable. **But `F2_DIR` is an
absolute path into the pinned session scratchpad**, and the adapter's own docstring says so: *“it is
a session scratchpad and is not guaranteed to survive.”*

**Checked rather than assumed — all four files are byte-identical to their committed copies:**

| file | scratchpad | repo `evidence/fixture_spike/f2/` |
|---|---|---|
| `fixture.py` | `f1a8bddf…` | **identical** |
| `phase5_ml_fixture.py` | `fb9760fe…` | **identical** |
| `check_external.py` | `3a1b5013…` | **identical** |
| `check_self_consistency.py` | `eb86a42f…` | **identical** |

**So there is no drift — and the risk is still real.** The adapter loads from a transient location
code that the repository already holds. **If that scratchpad is cleaned, `_import_fixture()` raises
and §9.2 cannot run, with the identical bytes sitting committed a few directories away.** A fallback
to the repo copy is a one-line change; it is **named, not made**, because `fixture_adapter.py` is
Phase 1 code and no ruling this round reaches it.

**The comparator runs themselves have not started.** Step 3 is a 2–3 hour block and is reported as
not begun rather than half-recorded.

---

# R147 — A36b's PRESENTATION LEADS WITH THE CONSEQUENCE · B-2 BEGINS

**RE-ENTRY.** `main` `6b30e30` → `e5b099b`; `phase1` `5295089`. Trees clean, tags `prereg-v30` only,
`backup/held-banking` == `stash@{0}`. `main` 23 checks / 2 findings; `phase1` 23 / 3. **EXPECTED.**

**§0 was stale in three places**, established by derivation: `main` was at **`6b30e30`**, not
`f1d66bf`; **A36b's presentation was produced** at `09d4ca0`; and **A39 was done** in the same commit
— eight ranges fixed, sixteen refused.

## A36b — the consequence now leads, and a second one was found

**The requirement was met in substance last round and not in form.** The consequence was stated in
the chat and in the artifact, but it sat in the artifact's **fourth section**. R147 §3 puts it first,
and that reordering surfaced something the first version had missed.

**Consequence 1 — the pointer cites a container ruled never to land.** Its closing sentence records
the line-816/830 relationship *“in the v30a **amendments block**”*. §8.2 never lands, and that phrase
is the one A34 removed from all four operative sites at `f1d66bf`. **Applying verbatim puts it back
into registered prose one commit after it came out.**

**Consequence 2 — NEW, and it follows from R147 §2.1's own rule.** The fenced specimen at l.1344 is
**byte-identical** to the text being applied. Landing the paragraph without removing the
`INSERT AFTER` apparatus leaves **an operative copy and a fenced copy** — so any future citation
anchored on that text resolves to **two** lines. **That is precisely the failure A34 spent a whole
correction class avoiding**, arriving from the opposite direction: not a citation that quotes an
anchor, but an application that duplicates one. **Whether the apparatus is removed is named as a
separable question and is not proposed** — it is scaffolding, but removing it is a deletion.

| choice | what it costs |
|---|---|
| apply verbatim, disclose | faithful to approved content; **prose then cites a container that does not exist** |
| apply with the citation corrected | file stays self-consistent; **no longer verbatim extraction**, so it needs its own approval, as the sixteen did |
| do not apply | nothing false added; **§AB's assertion at l.1374 stays false**, joins HELD |

**Added, and absent from the first artifact:** the insertion anchor **located and asserted unique**
(l.1336, match count 1); the **structure check before any write plan** — the anchor is a top-level
paragraph, blank above and blank below, so an inserted paragraph cannot merge into either neighbour
nor turn a following rule into a setext heading, and the fenced apparatus below stays balanced; and
**what applying makes true** — §AB's l.1374 assertion, to be verified by reading rather than assumed.

## TRACK B

### B-1 residual — the two facts owed to the chat

**`gate_suspicious_improvement` WAS seen to fire on an error metric.** MAE **0.0163** against a
persistence baseline of **0.8173** → improvement **+0.980 → HALT**, *“Model 98.0% better than
baseline (max: 20%)”*. The honest limb returned **+0.012 → PASS**. And the defect-7 limb, fed the
identical leakage as an **accuracy** the way k6 fed it, returns **PASS at −0.764** — *“Improvement
−76.4% is reasonable.”*

**Leakly is the ONLY tool that supplied a vendor negative.** For temporalcv, leakfence,
leakage-buster, leak-detect and deepchecks, **both limbs were constructed here.**

> **A false fact was caught before it reached the chat.** The readout script asked
> `d.get("vendor_negative", None)` and printed a `None` as *“vendor pair used”* — but the key is
> simply **absent** from Leakly's and temporalcv's result JSON, because those two controls were
> written before the field existed. **A missing key is not a value**, and defaulting it to a
> favourable reading would have reported temporalcv as vendor-backed when both its limbs are mine.
> Corrected against the committed coverage table, which is the authority.

### B-2 — §9.2 step 3 has begun

**The fixture reads.** `read_inputs("zc", "2025-01")` completes in **46.4s** and returns four frames
— `trades` 397,457×17, `snap` 1,262,191×24, `magg` 464,199×6, and the 8,272,769-row MBO frame the
adapter deliberately never opens.

**`b2_materialise.py` builds both sides ONE AT A TIME**, per SC-7(d): build, write, drop the
reference, `gc.collect()`, then the other side. The order is recorded, and the script **halts if the
two sides come out byte-identical** — which would mean it had built one side twice and no downstream
comparator result would mean anything.

**Two instrument defects on the way, both mine:**

- **`sys.path` for a script is not `sys.path` for `python -c`.** `leakaudit.contract` imports
  `protocol.runtime_reference` from the repo root; an inline `-c` probe succeeded because `-c` puts
  the cwd on the path, which **made the missing entry invisible until it ran as a file**. Both the
  root and `src` are now added explicitly.
- **The harness's “completed” notification tracked the `nohup &` wrapper, not the job.** The wrapper
  exits immediately; the python process was still running at 1.3 GB resident. **A wrapper's exit
  status is not its child's**, and reading the log alone would have shown an empty file and looked
  like silent failure.

**The comparator runs themselves are not done.** Step 3 is reported as **in progress**, not complete.
