# COMMIT_PLAN — the `prereg-v30a` ceremony commit

**ITEM PART D. PREPARED, NOT EXECUTED. Nothing in this file has been run.** No `git add`, no
`git commit`, no `git tag`, no `git push`, no hashing of staged or committed state, no `ots`.
Every git command used to build this plan was read-only (`status`, `log`, `show --stat`,
`ls-files`, `diff`, `cat-file`, `tag -l`, `check-ignore`, `rev-parse`, `remote -v`, `config`).

**Regenerated 2026-08-13 against the CURRENT state**, after the §A.6.0 recovery and under DELTA
R15's C1–C5. The previous revision of this file was written against commit `0ee26c4` and a tree
in which the declaration and `PRIOR_ART_VERIFICATION.md` were untracked. It is **superseded in
full, not patched.** The one open author decision it carried — the seventh tag-time hash — was
restated against current facts in §6 and is now **CLOSED as SIX** (R67/§14.1). **This file no
longer carries an open author decision.**

| | |
|---|---|
| Repository | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01` |
| `origin` | `https://github.com/TheoJHoward/DataLeakageAuditor.git` (fetch and push) |
| `HEAD` | **derived, never pinned** — `git rev-parse HEAD`. Every commit between `prereg-v30` and `HEAD` is enumerated and accounted for at `ceremony/COMMIT_ACCOUNTING.md`, gated by **C5b**. *(This row read `ffa6d942…` until R97 and went stale the moment `80401d0` landed — a pinned current-state value is a carried-forward value.)* |
| Tags present | **`prereg-v30`** only → `fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac` |
| Index | **empty** — `git diff --cached --stat` returns nothing; nothing is staged |
| State read | **2026-08-13** |

---

## 0. Read this before the path table

**The commit cannot be made yet.** `CEREMONY_COMMANDS.md` §0 carries the blockers in full; the
three that change *this* file's path table are:

1. **`PREREG.md` is clean.** sha256 `f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6`
   — byte-identical to the value in the signed `prereg-v30` tag message. The reviewed v30a diff
   has not been applied. The four §6.2 amendments and the §10.2 "waived" definition exist **only**
   inside `AVAILABILITY_DECLARATION.md` §A.1/§A.3/§A.4/§A.8/§A.12. `PREREG.md` §0.1 makes it the
   sole normative source for measurement semantics, and §0.2.1 line 95 says "the amended tag
   carries the new semantics". **A tag over the current tree would carry an unamended `PREREG.md`
   and therefore amend nothing.**
2. **`DEVIATIONS.md` is 0 bytes** (sha256 `e3b0c442…`, the empty-string digest). Draft:
   `DEVIATIONS_DRAFT.md` §1.
3. **`README.md` is clean** (sha256 `7a0a0310…`) and carries no v30a hash block.

A fourth — the `HISTORY.md` amendment ledger entry — is drafted in `H34_DRAFT.md`, and the ID
working resolution R8 assigns it is **already taken** (§3).

> ### ⚠ THE EVIDENCE TREE MOVED WHILE THIS PLAN WAS BEING WRITTEN
>
> `evidence/author_review/READ_THROUGH_PACKAGE.md` grew from **104,290** to **136,164** bytes
> between two measurements taken minutes apart in this same pass. Something outside this item is
> writing into `evidence/`. **Consequence for the ceremony: every byte total in §2 is a
> measurement at an instant, not a property**, and `evidence/MANIFEST.sha256` cannot be repaired
> and then left unattended — the repair and the `git add` must be adjacent, with
> `sha256sum -c` re-run immediately before the commit. See §5.

---

## 1. Path table — every path, its verified status, and its disposition

`git status --porcelain`, read this pass:

```
 M AVAILABILITY_DECLARATION.md
 M DESIGN.md
 M HISTORY.md
?? .claude/
?? evidence/
?? tagmsg.txt
```

`git diff --stat` against `HEAD`:

```
 AVAILABILITY_DECLARATION.md | 42 ++++++++++++++++++++++++++++++++++++++----
 DESIGN.md                   | 30 +++++++++++++++---------------
 HISTORY.md                  | 33 +++++++++++++++++++++++++++++++++
 3 files changed, 86 insertions(+), 19 deletions(-)
```

| Path | Tracked? | Verified status this pass | Disposition | Basis |
|---|---|---|---|---|
| `AVAILABILITY_DECLARATION.md` | **tracked at `ffa6d94`** | **` M ` — MODIFIED since that commit.** Working tree, **derived not transcribed** (`sha256sum`, `wc -c`, `wc -l`) — as at R69: sha256 `4c07c76ffbb2fe7b04a903d01d74d56bd2f80bf266f70f7fe2e45ea73a636403`, **303,643 bytes**, **3,955 lines** (the file ends with a newline). *The diffstat against `ffa6d94` is not restated here: read it with `git diff --numstat ffa6d94 -- AVAILABILITY_DECLARATION.md`. This cell read `f0829bd3…` / 277,411 / 3,684 / "38 insertions, 4 deletions" after the file had moved three times; checked by D7 from R68.* | **STAGE** — the ceremony commit carries the **post-B3** state, not `ffa6d94`'s | §0.2.1 l.97 integrity chain "in full"; sixth tag hash per declaration §D.2. **§2.1 enumerates the three changes.** |
| `DESIGN.md` | tracked | ` M ` — **30 lines changed, 15 insertions / 15 deletions.** Working tree sha256 `39a944c1…` | **STAGE** | `PREREG.md` §11 item 3 — hashed in the tag. **Two independent changes; §2.2.** |
| `HISTORY.md` | tracked | ` M ` — **+33 lines, 0 deletions.** Working tree sha256 `3845b779…`, 313 lines | **STAGE** | §0.4; §11 item 3 — hashed in the tag. **Three additions today, a fourth due at ceremony time; §2.3.** |
| `PRIOR_ART_VERIFICATION.md` | **tracked at `ffa6d94`** | **CLEAN — verified.** Absent from `git diff --stat` and from `git status`. sha256 `b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`, 3,610 bytes, 48 lines | **NOTHING TO STAGE.** It is already in the commit graph and will be in the tagged tree by inheritance | Cited by name **and by that exact sha256** in `HISTORY.md` H-34 l.271 — re-verified byte-for-byte this pass — and by `DESIGN.md` §2.11. **§6 is the six-vs-seven decision.** |
| `evidence/` | **untracked** | **249 files, 13,047,641 bytes** at the instant of measurement (R67; was 245 / 13,004,254) — **and moving** (see §0). `git check-ignore` exits 1, so nothing in it is silently dropped | **`git add evidence`** | Supporting record for D-001 and for the declaration. **§2.4 gives the composition; §5 the manifest repair.** |
| `PREREG.md` | tracked | **clean.** sha256 `f0a8f001…` = the `prereg-v30` tagged value | **STAGE, once the reviewed diff is applied** | §0.2.1 l.95; §0.1. **Blocking — the diff does not exist.** |
| `DEVIATIONS.md` | tracked | **0 bytes** | **STAGE, once D-001 is appended** | §0.2.1 l.95 "The deviation records what was measured"; §11 item 6 append-only. Draft: `DEVIATIONS_DRAFT.md`. |
| `README.md` | tracked | **clean.** sha256 `7a0a0310…` | **STAGE, once the v30a block is written** | §11 item 3 "in the tag message **and the README**". README is revisable by its own l.23–24. **Filled from the C2 output, staged before the commit** — see `CEREMONY_COMMANDS.md` §3.5. |
| `tools/check_registration.py` | tracked | clean. sha256 `72ffc7c6…` = the `prereg-v30` tagged value | **do not touch** | Pure-text amendment. **Its hash is still recomputed at tag time — never restated.** |
| `protocol/runtime_reference.py` | tracked | clean. sha256 `215194c1…` = the `prereg-v30` tagged value | **do not touch** | Same. |
| `VALIDATED_CONFIG.toml` | tracked | clean | **do not touch** | §11 item 1 placeholder until the Phase 1 freeze. |
| `PARKING_LOT.md` | tracked | clean | **do not touch** | §11 item 1 — §13.9 entry only. |
| `protocol/__init__.py`, `tests/registration/*` (8 files) | tracked | clean | **do not touch** | Not touched by a text amendment. |
| `registration-commit.txt`, `registration-commit.txt.ots` | tracked | clean | **do not touch** | v30's OTS record. v30a writes a **new** pair, `amendment-commit-v30a.txt{,.ots}`, in a follow-up commit. |
| `.gitattributes`, `.gitignore` | tracked | clean | **do not touch** | `.gitattributes` pins `* -text`, which is what makes working-tree sha256 equal blob sha256 — the assumption `CEREMONY_COMMANDS.md` C2e tests. |

### 1.1 Deliberately excluded

| Path | Status | Why excluded |
|---|---|---|
| `.claude/` | untracked, not ignored | Local agent and tooling configuration. **Never commit.** Not part of the registration and not covered by any §11 item. It appears in `git status` precisely because it is not ignored, so it must be excluded **by not naming it**, never by a blanket `git add -A` or `git add .`. |
| `tagmsg.txt` | untracked, **770 bytes**, sha256 `98c76f3ec9449b8b4da16c1ea4b2c3249c330690fcd80c87255b6d17c79bcaff` | **SUPERSEDED — checked and confirmed this pass.** Its content was diffed byte-for-byte against the body of the signed `prereg-v30` tag object (`git cat-file tag prereg-v30`, lines 6–20) and is **identical**: the v30 title line and the five v30 hash lines. It is a v30 ceremony leftover. **A new one supersedes it at tag time:** `CEREMONY_COMMANDS.md` §3.5 writes the v30a message to this same path from the C2 output. Overwriting it destroys nothing — the v30 message lives in the signed tag object in perpetuity. It stays **untracked and uncommitted**, matching the v30 precedent (confirmed absent from `git ls-files`). |
| `v30a.hashes.txt` | will not exist until C2 | The R15 audit record of the single hashing operation. Deleted after the tag verifies. **Never committed.** |
| `amendment-commit-v30a.txt{,.ots}` | will not exist until C4 | Committed, but in the **follow-up** commit, not this one — a commit cannot contain the receipt for its own hash. |

---

## 2. What each modified path actually contains

### 2.1 `AVAILABILITY_DECLARATION.md` — three changes since `ffa6d94`, all post-B3

The commit `ffa6d94` tracked the declaration at 3,650 lines. **The working tree is AHEAD of it**,
and the ceremony commit carries the working-tree state. Read from `git diff`:

1. **§A.6.0, the precedence reading note (ll.1067–1074, +7).** The B3 **ex-nq binding** work's
   companion correction: an italic clause recording that precedence is *not* load-bearing for
   `buy_volume_10s` — the REQUIRED clause is a conjunction, so its second conjunct already excludes
   the column — and that the column where precedence **is** load-bearing is
   `book_imbalance_ratio`, which satisfies both the OUT OF JURISDICTION iff and the UNSCORED
   second limb, so only "UNSCORED wins" resolves it.
2. **§A.6.1's construction-column reading note (ll.1092–1099, +9) and row 34 (±1).** States that a
   bare line number or a `phase5_ml.py` citation in the table names the **lineage** construction,
   that the `ts_floor` join the rule turns on is present in both generations, and gives the
   equivalence pairs. Row 34's citation is made explicit as `phase5_ml.py` L231 (= `phase7_l2_sim.py` L207).
3. **§14 item 4's BINDING ex-nq clause (ll.3105–3118, +15) and the §14.1 summary rewrite
   (ll.3194–3205, +5 / −3).** Declares that a **summary-level** statement of the restricted
   contaminated peak quotes the **EX-NQ** figures — RATE es 2025-11, 484,420 / 549,424 = 88.17%;
   ABSOLUTE es 2025-01, 514,323 of 605,290 = 84.97% — because nq's 90.83% is a **coverage
   artifact** (nq has no MBO classes to drop). §14.1's summary sentence is rewritten to lead with
   the ex-nq peak and carry the unqualified maximum as a labelled aside.

**All three are declaration-internal and none of them touches the four §6.2 amendments or the
§10.2 definition**, which §D.1 item 5 freezes at tag time. They are drafting and quotation-rule
corrections, and the ceremony commit must carry them: `ffa6d94`'s declaration bytes are **not**
the bytes §D.2's sixth hash is supposed to cover.

### 2.2 `DESIGN.md` — two independent changes. **Neither is a "cross-reference bump".**

- **§2.11 prior-art table, ll.195–213.** A third column, `leakage-buster`, added to the comparison
  table — all ten rows rewritten — and the closing sentence replaced by a longer one that names
  `leak-detect` explicitly, places `leakage-buster` in a different taxonomy (dataset-level audit
  rather than runtime probe), and points at `PRIOR_ART_VERIFICATION.md`. This is the DESIGN-side
  counterpart of the H-34 kill-gate sign-off.
- **§9 line 546.** The enumerated range was **removed, not bumped.** Old: "**Review lessons are
  recorded in `HISTORY.md`** (**H-L1** through **H-L11**)." New, verbatim in the working tree:

  > **Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range;
  > the list grows as lessons are appended, and this cross-reference does not enumerate the
  > current tail so appending a lesson cannot desynchronize this document).

  **This is the remedy H-L13 exists to record**, and H-L13's own text says so.

### 2.3 `HISTORY.md` — three additions in the tree, a fourth due at ceremony time

- **H-L12** (list item 12, l.218) — the 37-vs-119 grep-undercount lesson, **including** the
  appended date-convention sentence: "Dated by the day recorded, not the day worked — the
  convention this list follows from here."
- **H-L13** (list item 13, l.219) — the enumerated-range fragility lesson. Records the pattern
  reaching three instances and states the remedy applied to `DESIGN.md` l.546.
- **H-34** (ll.264–292) — the **kill-gate sign-off**, `from \`PREREG.md\` §10.1 (kill-gate
  sign-off, prior art)`, author-attributed, dated 12 August 2026, verdict "§10.1 does NOT fire". A
  26-line plain-prose block fenced by bare `---` rules. **This is not the amendment ledger entry
  the ceremony needs, and it occupies the ID that entry was assigned** (§3).
- **Due at ceremony time:** the amendment ledger entry, drafted as **H-35** in `H34_DRAFT.md` §3.

### 2.4 `evidence/` — composition, measured this pass

| Subtree | Files | Bytes |
|---|---|---|
| `evidence/fixture_spike/` | 236 | 12,632,519 |
| `evidence/author_review/` | 1 | 136,164 — **and growing during this pass (§0)** |
| `evidence/errata/` | 3 | 106,052 |
| `evidence/ceremony/` | 4 | 90,976 — **this package; rewritten by this item** |
| `evidence/MANIFEST.sha256` | 1 | 38,543 |
| **total** | **245** | **13,004,254** |

**Re-measure at stage time. Do not carry these numbers forward:**

```sh
find evidence -type f | wc -l
find evidence -type f -printf '%s\n' | awk '{s+=$1} END {print s}'
```

### 2.5 The H-L13 question the brief asks, answered against the file

**Does H-L13 land in THIS ceremony? YES — it is already in the working tree.** `HISTORY.md` l.219
is list item `13.`, and `git diff` shows ll.218–219 as working-tree additions not present in
`HEAD`. It is part of the ` M HISTORY.md` change this commit stages. There is no separate decision
to take about it.

**The staging file the brief names drafts H-L14, not H-L13.**
`evidence/errata/HISTORY_lesson_line_S4_STAGED.md` §0 records both of the brief's premises as
stale, and both were re-verified independently this pass:

| Premise | Verified state |
|---|---|
| "the H-L13 staging … would make that cross-reference `H-L1 through H-L13`" | The staged line is numbered **14**, because 13 is taken by the landed entry at l.219. |
| `DESIGN.md` l.546 needs a matching bump | **l.546 no longer enumerates a tail.** `grep -rn 'H-L' --include=*.md` finds exactly one range cross-reference repo-wide, and it is the open-range text quoted in §2.2. |

**What the `DESIGN.md` line must read — the same text either way.**

- **If H-L14 lands in this ceremony:** l.546 reads the open-range text, unchanged.
- **If H-L14 does not land:** l.546 reads the open-range text, unchanged.
- **It must NOT be set to `H-L1 through H-L13` or `H-L1 through H-L14`.** Doing so would reverse
  the fix that H-L13 — one line above it, in the same commit — exists to record, and would
  re-create the exact defect in a document the signed tag hashes.

**Whether H-L14 lands is an author decision and nothing else depends on it.** If it does, it is a
fourth `HISTORY.md` addition and `H34_DRAFT.md` §4 notes that working resolution R19 (the §A.6.0
recovery lesson) would then take **H-L15**.

---

## 3. The H-34 ID collision — BLOCKING, and unchanged since the previous revision

Working resolution **R8** (`AVAILABILITY_DECLARATION.md`, decision-log tail — cited by
identifier, not line: `l.3665` pointed at §D.3 by R69, R8 having moved to 3936) assigns the amendment entry the
ID **H-34**. `HISTORY.md`'s `### H-34` heading (cited by heading, not line — `l.264` was
empty by R69, the entry having moved to 271) now reads `### H-34 — from \`PREREG.md\` §10.1 (kill-gate
sign-off, prior art)`. **R8's ID assignment is stale; the next free ID is H-35.**
`H34_DRAFT.md` §1 gives both resolutions and recommends H-35. **R8's form instruction is
unaffected** — main-series, `from \`PREREG.md\` §0.2.1`, one italic parenthesized paragraph.

Two related observations, flagged and **not fixed by this package**: H-34's plain-prose block
form departs from the one-italic-paragraph convention every other main-series entry follows, and
its closing bare `---` rule sits immediately above `### H-B addendum`, where a reader will take it
as a section divider.

---

## 4. The exact `git add` invocations

**Do not run these.** They are the plan. Preconditions: `CEREMONY_COMMANDS.md` §0 cleared, §3
resolved, §5 repaired, §6 decided, and both gates green.

One commit, everything in it. Four invocations, split only so the shell history separates the
categories. **The group count is a restatement of the block below and nothing derives from it —
it read "Three" until R67/§15 added the checking tools:**

```sh
# from the repository root

# (1) the registration documents — all tracked, all hashed or hash-adjacent
git add PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md prereg-signing-key.asc

# (1a) PRACTICES.md — ADDED R99/§168.1. THE MANIFEST ATTESTS IT and it was
#      untracked and absent from this set, so the signed tree would have
#      attested content it did not contain. `sha256sum -c` cannot see that:
#      it runs where the file is present and reports green. Caught by D16,
#      which checks the third direction — listed -> IN THE COMMIT.
git add PRACTICES.md

# (2) the declaration — tracked at ffa6d94, MODIFIED since; the ceremony carries the
#     post-B3 state, not the ffa6d94 state
git add AVAILABILITY_DECLARATION.md

# (3) the checking tools — BOTH ARE IN THE HASHED SIX, and both were absent from
#     this block until R67/§15. `tools/check_registration.py` is ` M ` today.
#     A hashed file that is never `git add`ed does not fail: `git show :<path>`
#     silently returns its HEAD content, so the tag is signed over bytes the
#     author never approved (CEREMONY_COMMANDS.md §3.3). `git add` on the
#     unchanged one is a no-op and is named anyway, because the set is the
#     authority — not which members happen to be dirty this pass.
git add tools/check_registration.py protocol/runtime_reference.py

# (4) the evidence tree — currently untracked
git add evidence

# (5) PRIOR_ART_VERIFICATION.md — NOW STAGED. R110 CHANGED IT.
#     Until R110 this file was tracked and CLEAN since `ffa6d94`, so the commit
#     inherited it and `git add` was a no-op — that was §168.2's reasoning and it
#     was correct while it held. R110's register sweep edited it (the prior-art
#     provenance sentence), so it is MODIFIED and inheritance no longer carries
#     it. D16 asks after it because the manifest attests it.
git add PRIOR_ART_VERIFICATION.md

# (5a) THE SUPERSEDED REASONING, kept so it is not re-derived from scratch:
#     The manifest attests it, so D16 asks after it. It needs no `git add`
#     because it has been TRACKED since `ffa6d94` and is unmodified: the commit
#     inherits it from HEAD's tree, so the manifest's attestation is satisfied.
#     Naming it here would suggest to a later reader that it was new in this
#     ceremony, which is the reason §4 names the six even when some are no-ops
#     but does NOT name files that were never touched. **Recorded so this is not
#     re-opened**: tracked-and-clean and staged-here are two different ways of
#     being in the commit, and D16 accepts either.
```

**`PRIOR_ART_VERIFICATION.md` is deliberately absent from these lines.** It is tracked and clean;
`git add` on it is a no-op, and naming it would suggest to a later reader that it was new in this
commit. It entered the graph at `ffa6d94`.

**Never `git add -A`, `git add .`, or `git commit -a`.** `.claude/` and `tagmsg.txt` are untracked
and **not** ignored — a blanket add sweeps both into the registration commit.

### 4.1 Pre-commit verification, between the `git add` and the `git commit`

```sh
# THE INTENDED SET, derived from §4's own `git add` lines. Never restated here:
# a second copy of a set is the defect §15.2 names, and this file already carried
# one (the "245 paths" figure below was stale by four when R67 measured the tree).
intended=$(grep -E '^git add ' evidence/ceremony/COMMIT_PLAN.md \
           | sed 's/^git add //' | tr ' ' '\n' | sed '/^$/d' | sort -u)

# V1a — COMPLETENESS, over the subset that ACTUALLY CHANGED.
#       `git diff --cached --name-only` prints only paths whose staged bytes differ
#       from HEAD, so a path identical to HEAD can never appear and is not a miss.
#       Those are V1c's job, not this one.
v1a=0
for p in $intended; do
  [ -d "$p" ] && continue
  git diff --quiet HEAD -- "$p" && continue          # identical to HEAD: nothing to print
  git diff --cached --quiet HEAD -- "$p" && { echo "V1a NOT STAGED: $p"; v1a=1; }
done
[ "$v1a" -eq 0 ] || { echo "V1a FAILED. HALT."; exit 1; }
echo "V1a OK"

# V1b — SUPERSET. Nothing outside the intended set may be staged.
# NOTE: no pipe into the loop. A `cmd | while` runs the loop in a SUBSHELL, so a
# counter set inside it is lost and the check can only ever print.
v1b=0
for p in $(git diff --cached --name-only); do
  ok=0
  for q in $intended; do
    case "$p" in "$q"|"$q"/*) ok=1; break;; esac
  done
  [ "$ok" = 1 ] || { echo "V1b UNEXPECTED STAGED PATH: $p"; v1b=1; }
done
[ "$v1b" -eq 0 ] || { echo "V1b FAILED. HALT."; exit 1; }
echo "V1b OK"
# EXPECT no output. `.claude/` and `tagmsg.txt` are untracked and not ignored;
# either one appearing here means a blanket `git add` was used.

# V1c — MEMBERSHIP over the HASHED SIX. The only check that can see an
#       unchanged-but-unstaged hashed file. V1a cannot: an unstaged file and an
#       unchanged file are indistinguishable in `--cached` output, and `git show
#       :<path>` on a never-staged tracked file silently returns its HEAD content
#       (§3.3). The set is READ from its single authority, never restated.
eval "$(grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md)"
v1c=0
for f in $FILES; do
  git show ":$f" >/dev/null 2>&1 || { echo "V1c NOT IN INDEX: $f"; v1c=1; continue; }
  git show ":$f" | cmp -s - "$f"  || { echo "V1c INDEX != WORKTREE: $f"; v1c=1; }
done
[ "$v1c" -eq 0 ] || { echo "V1c FAILED. HALT."; exit 1; }
echo "V1c OK — all six staged at their worktree bytes"

# For the human reader, and NOT the check — the check is above:
#   expected to appear (modified by this ceremony): AVAILABILITY_DECLARATION.md
#   [hashed], DESIGN.md [hashed], HISTORY.md [hashed], tools/check_registration.py
#   [hashed], DEVIATIONS.md, README.md, and the evidence tree.
#   expected NOT to appear while unchanged, which is CORRECT and not a miss:
#   PREREG.md [hashed] — locked, byte-identical to v30 BY DESIGN and must stay so;
#   protocol/runtime_reference.py [hashed] — expected identical to v30;
#   PRIOR_ART_VERIFICATION.md — tracked and clean since ffa6d94.
# If either HASHED file in the second group DOES appear, that is a finding to
# record, not a typo to correct (CEREMONY_COMMANDS.md §3.1 item 4: "Expected
# identical" is a prediction to be tested, not a value to be copied).
#
# *(R67/A1: this block replaced a PRINT. The original V1 ran
# `git diff --cached --name-only | sort` under the words "EXPECT, exactly:" and
# listed PREREG.md among the expected paths. PREREG.md is byte-identical to v30 by
# design, so under set equality that list could never have been satisfied. Per the
# run record the ceremony has never been executed — no `prereg-v30a` tag, no
# `v30a.hashes.txt`, and §0 of CEREMONY_COMMANDS.md states in terms that nothing in
# it has been run — so V1 never passed and never failed. It had never been
# exercised at all.)*

# V2 — nothing intended was left behind
git status --porcelain
# EXPECT only:  ?? .claude/    ?? tagmsg.txt
# Any remaining ` M ` line is a hashed file edited after staging — STOP.
# (This is the same condition CEREMONY_COMMANDS.md C2b tests on the six.)

# V3 — the evidence manifest verifies against the tree being committed
(cd evidence && sha256sum -c MANIFEST.sha256)
# REQUIRED: every line OK, zero FAILED. See §5 — today this FAILS.

# V4 — the staged evidence count matches the manifest's own claim.
#      DERIVE, don't trust the numerals: the RELATION is the check, and the two
#      counts below were 245/246 until R67 measured the tree and found 249/251.
staged=$(git diff --cached --name-only -- evidence | wc -l)      # measured: 249
hashed=$(grep -cE '^[0-9a-f]{64}  ' evidence/MANIFEST.sha256)    # measured: 251
uplines=$(grep -cE '^[0-9a-f]{64}  \.\./' evidence/MANIFEST.sha256)  # measured: 3
[ "$hashed" -eq "$((staged - 1 + uplines))" ] || {
  echo "V4 FAILED — hashed=$hashed staged=$staged uplines=$uplines. HALT."; exit 1; }
echo "V4 OK"
# The manifest carries ONE line per in-tree file EXCEPT ITSELF, plus the `../`
# repository-root lines (the declaration, PRIOR_ART_VERIFICATION.md, PRACTICES.md).
# So: hashed == (staged - 1) + uplines. Any other relationship is a manifest defect.
# Any other relationship between these two numbers is a manifest defect.

# V5 — no unfilled placeholder reached the index
# A bare `grep` here was INVERTED: it exits 1 when it finds nothing, i.e. non-zero
# on success and zero on failure. Wired into any `set -e` runner it halted on a clean
# tree and passed on a dirty one.
if git diff --cached | grep -n '«CEREMONY-FILL'; then
  echo "V5 FAILED — an unfilled «CEREMONY-FILL» placeholder reached the index. HALT."; exit 1
fi
echo "V5 OK — no placeholder staged"

# V6 — append-only, PREREG §11 item 6
# Same inversion as V5, and worse: `grep -c` prints a count, so the human had to
# read a number rather than a verdict.
removed=$(git diff --cached -- DEVIATIONS.md | grep -c '^-[^-]' || true)
[ "$removed" -eq 0 ] || {
  echo "V6 FAILED — $removed line(s) removed from DEVIATIONS.md; PREREG §11 item 6 is append-only. HALT."; exit 1; }
echo "V6 OK — append-only holds"

# V7 — the gates, against the exact tree about to be committed
python -m pytest tests/registration
python tools/check_registration.py --stage prereg          # MUST exit 0 (PREREG §6.8)
```

**V7 has NOT been run in this pass.** The boundary is execute-nothing, so no checker run and no
test run was performed. Any previously recorded PASS predates the `DESIGN.md` §2.11 rewrite,
H-L12, H-L13, H-34 and the three declaration changes of §2.1. **Treat the gate as unverified
against the current tree.**

*(`AVAILABILITY_DECLARATION.md`, `PRIOR_ART_VERIFICATION.md` and `evidence/` are not scanned by
the checker, and `REQUIRED_PATHS` is presence-only with no unexpected-file check, so adding them
cannot fail `structure` — and equally the checker will not catch a normative statement that
migrates into the declaration. Author review and the R14 records are the only controls there.)*

---

## 5. The manifest VERIFIES. Regenerating this package staled four lines; they were re-derived.

`sha256sum -c MANIFEST.sha256`, run from inside `evidence/` this pass:

```
251 lines OK, 0 FAILED
```

**The `author_review/READ_THROUGH_PACKAGE.md` failure recorded here in the previous revision is
GONE** — that line verifies. *(This section read "245 of 246 lines verify OK" and named that one
failure; both statements were true when written and are false now. The counts were also stale by
construction: the tree is 249 files, not 245.)*

**Four lines went stale during R67 and were re-derived in the same pass, from the bytes then on
disk:** `ceremony/CEREMONY_COMMANDS.md`, `ceremony/COMMIT_PLAN.md`, `ceremony/DEVIATIONS_DRAFT.md`
and `../AVAILABILITY_DECLARATION.md`. **This is N2 — freeze means no SILENT change, not no
change.** The declaration moved because R67/§14.3(c) added the three §D.3 interpretation entries.

**The declaration's THREE records agree, verified this pass (C2d-2):** the file, the
`../AVAILABILITY_DECLARATION.md` manifest line, and the pointer at
`evidence/fixture_spike/f4/DECLARATION_POINTER.md` all read `06b2974a…` / 301,210 bytes. The
pointer and the manifest line were rewritten in the same pass as the declaration change, as R15
requires — the pointer's own manifest line was then re-derived in turn, because updating the
pointer stales it.

**Composition, measured rather than remembered:** 249 files in `evidence/`, 13,047,641 bytes; 251
hashed lines = 248 in-tree (one per file except the manifest itself) + 3 `../` repository-root
lines. V4 checks that relation rather than the numerals.

**Still required before staging:** re-run `sha256sum -c` **immediately before** `git add evidence`.
R15's no-carry-forward rule binds the manifest exactly as it binds the six tag hashes, and the
tree moves. The `# COUNTS.` comment block at the head of `MANIFEST.sha256` is human-readable and
unhashed; regenerate it in the same pass so it does not describe a tree that no longer exists.

## 6. CLOSED — the tag message carries SIX hashes (R67/§14.1, blocker item 8)

**DECIDED: SIX.** The set is `$FILES` at `CEREMONY_COMMANDS.md` §3.2 l.180, which is the single
authority; this section records the decision, not the set.

**The declined seventh candidate, named so the record shows what was refused:**
**`PRIOR_ART_VERIFICATION.md`** — tracked and clean since `ffa6d94`
(sha256 `b97a28044edcff7612d6deba5a8ae9cc5f6c14b99b1d11a6414f5ba9a0e733bb`, 3,610 bytes). *The
staging half of the old §3.3 was already discharged: the file is in the tagged tree whatever was
decided here. Only the hashing half was open, and it is now closed against admission.*

**The four reasons:**

**(a) Six is the implemented state.** `$FILES` (§3.2 l.180) names six; the tag-message body
(§3.5) enumerates six by path; and **every gate iterates the list** — C2a, C2b, C2c, C2, C2e,
C2f, C1c. Nothing in the chain reads a numeral. Choosing seven would mean changing the thing that
already works to match an argument, rather than the reverse.

**(b) The enumerated list is not the integrity boundary.** The tag references a commit, the commit
references a tree, and the tree fixes **every tracked file** — `PRIOR_ART_VERIFICATION.md`
included, since `ffa6d94`. The list's function is **citation**: it tells a reader which documents
the registration turns on and lets them check those without cloning. It is not what makes the
content tamper-evident; the commit object already does that.

**(c) The cost is real and the gain is near zero.** A seventh entry means re-touching the tag body,
`README.md`'s block, and the count literals this round is already correcting — at seven weeks out
from the §11 item 5 reachability deadline — to add a citation for a file whose hash is **already**
quoted inside `HISTORY.md` H-34, which the tag hashes, and whose content the tree already fixes.

**(d) It is reversible, so this is not a one-way door.** Adding a file to the block later is a
**Class B** change — a parameter of a locked procedure, not a change to what the registration
claims. If a later reader wants the citation, a supplement can carry it under `PREREG.md` §12
without disturbing this tag.

**The case for seven, preserved rather than deleted, because a closure that hides the counterargument
is not a record:**

- `§0.2.1` line 97: *"An amendment weaker than the thing it amends is not one."* The file is cited
  by two documents the tag hashes, and a reader verifying the **tag message alone** — without
  cloning the tree — cannot check it. **Answered by (b):** verifying the message alone was never
  the property the chain provides; the message cites, the commit protects.
- If `PRIOR_ART_VERIFICATION.md` is a **registration document** rather than an **evidence
  artifact**, §11 item 3's pattern says its hash belongs in the message. It is the written record of
  a kill-gate verdict, which is closer to registration than to evidence. **Answered by (d):** the
  classification question survives this decision and can be revisited without re-cutting the tag.

**Consequence for §D.2.** The declaration's §D.2 declares SIX by name and is itself hashed by the
tag, so this closure and the declaration now agree. **No §D.2 edit is required** — which was the
strongest argument for six, and it is now simply the state.

*(The R7 question that sat here is resolved and is no longer an open flag: working resolution **R7**
predicates that the v30a message "carries ALL FIVE hashes", which is **TRUE** of a six-file set
containing those five. The totality reading came from R7's topic **label**, not its predicate; the
label survey at R67/§14.2 established that every label in that block is a topic tag. **R7 stands
unamended and does not contradict §D.2.** See `AVAILABILITY_DECLARATION.md` §D.3 and the survey
recorded in the amendment package.)*

## 7. The commit message

```sh
git commit -m "Pre-registration v30a: §6.2 reference AUC, contamination-class locus, sliced CI variant, and criterion 3 — class C amendment (PREREG §0.2.1)"
```

Wording rationale: the four amended §6.2 elements are enumerated rather than given as a section
number, because all four sit inside §6.2 and "§6.2" alone would not say which of its elements
moved. The four are fixed by the declaration's own walk summary (§A.11, heading "A.11 — Walk summary"; cited by anchor, not line): line 445 reference
AUC, line 450 contamination availability class, line 451 sliced variant, line 461 criterion 3.

**If the reviewed `PREREG.md` diff also touches §10.2** — declaration §A.12 adds a definition of
"waived" for §10.2's replacement-criterion floor, and §D.1 item 5 freezes it alongside the four —
**the message must name §10.2 too.** The final wording follows the reviewed diff, not this file.

Single-line `-m` is deliberate: the v30 precedent (`fe0d5a5`, `5842857`, `0ee26c4`) is one-line
subjects throughout, and the substance lives in the tag message and in `DEVIATIONS.md` D-001, not
in the commit subject. *(`ffa6d94` is the one multi-paragraph body in the log, and it is a
tracking commit, not a registration one.)*

---

## 8. What blocks this commit

| # | Blocker | Owner | Severity |
|---|---|---|---|
| 1 | ~~Phase 0 kill gate not signed off as a whole~~ **ROUTED, 25 Aug 2026: branch (b).** The §9.2 cross-tool comparison and the licence check gate **Phase 1 entry, not the tag**; H-34's verdict is the tag's sign-off. Both carried forward as named open obligations, neither waived. Recorded verbatim at `CEREMONY_COMMANDS.md` §0, before C5. *This blocker was a **routing decision**, not the §10.1 attestation; earlier rounds of the working session mischaracterised it.* | AUTHOR | **done, pending author confirmation of wording** |
| 2 | `PREREG.md` v30a diff does not exist | AUTHOR | hard |
| 3 | `DEVIATIONS.md` is 0 bytes | draft ready | hard |
| 4 | Amendment ledger entry not written, and R8's assigned ID is taken (§3) | draft ready | hard |
| 5 | `README.md` v30a block not written | AUTHOR | hard |
| 6 | ~~`MANIFEST.sha256` FAILS on one line~~ **RESOLVED R67: 251 OK / 0 FAILED, four R67-staled lines re-derived, C2d-2 three-way green (§5)** | mechanical | **done, re-verify at stage time** |
| 7 | The evidence tree is being written to by something outside this item (§0) | AUTHOR to quiesce | hard |
| 8 | ~~Six-vs-seven tag-hash decision (§6)~~ **CLOSED as SIX, R67/§14.1** | AUTHOR | **done** |
| 9 | ~~Prereg gate and trace suite not re-run~~ **RESOLVED R67: `--stage prereg` 14/14 PASS (incl. the new `hash_set_single_source`), `pytest tests/registration` 137 passed** | mechanical | **done, re-run at stage time (V7)** |
| 10 | `ots` CLI broken; stamp goes through the web UI (`CEREMONY_COMMANDS.md` §6) | AUTHOR | hard, but trails the tag |
