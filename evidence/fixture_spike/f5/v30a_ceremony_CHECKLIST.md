# prereg-v30a ceremony checklist — DRY RUN, NOTHING EXECUTED

> **SUPERSEDED (R68).** This file is the 2026-08-12 dry run. It is superseded in full by
> `evidence/ceremony/CEREMONY_COMMANDS.md` (regenerated 2026-08-13 under R15) and
> `evidence/ceremony/COMMIT_PLAN.md`. It is kept as the dated record of that walk.
>
> **EVERY HASH AND BYTE COUNT BELOW IS AS AT 2026-08-12 AND IS NOW STALE BY CONSTRUCTION.**
> In particular the `AVAILABILITY_DECLARATION.md` hash block records `d1f43f51…` / 215,256
> bytes; the declaration has moved several times since. **A mismatch against this file is not
> a tamper signal** — it is this file being a snapshot. Verify against
> `evidence/MANIFEST.sha256` and the declaration pointer, never against this checklist.

Produced by Phase 0 addendum 2, item F5. Repo: C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01

**Revision 2 — 2026-08-12, item Y5.** Every numbered step below was re-walked against the repo
state on that date; the per-step result is stamped at the tail (§RE-VERIFICATION STAMP). This
revision implements working resolutions **R14** (single normative copy) and **R15**
(single-operation hashing), raises the tag message from **five hashes to six**, brings the
working-tree edits to `HISTORY.md` and `DESIGN.md` into the ceremony commit's scope, adds the
new untracked paths (`AVAILABILITY_DECLARATION.md`, `evidence/`), and records the X6 citation
and Z2 pattern notes for the ceremony record. **Nothing here has been executed.**

## Baseline, re-verified 2026-08-12

| Fact | Value | How verified |
|---|---|---|
| HEAD (main) | `0ee26c44380f0a9c8538f34e23b8649d07da22f5` (`0ee26c4`) | `git rev-parse HEAD` |
| tag `prereg-v30` -> commit | `fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac` | `git rev-list -n 1 prereg-v30` |
| Tag gate on the CURRENT WORKING TREE | **PASS, exit 0** — 13 checks PASS, 0 FAIL, 8 deferred to `--stage implementation` / `--stage release` | `python tools/check_registration.py --stage prereg` (read-only: the file contains `read_text` only, no write/open-for-write/subprocess) |
| Remote | `origin  https://github.com/TheoJHoward/DataLeakageAuditor.git` | `git remote -v` |
| `user.signingkey` | `B29CF0E847119AD7` — matches the README fingerprint tail | `git config user.signingkey` |
| `DEVIATIONS.md` | **still 0 bytes — empty** | `stat -c '%s' DEVIATIONS.md` |
| Working tree | `M DESIGN.md`, `M HISTORY.md`; untracked `.claude/`, `AVAILABILITY_DECLARATION.md`, `evidence/`, `tagmsg.txt` | `git status --porcelain` |

**The gate PASS above is on the working tree, not on `HEAD`.** It was re-run after the H-L12
edits landed, so the H-L12 addition and the `DESIGN.md` cross-reference bump do **not** break
`single_source`, `lock_table`, or any other prereg-stage check. It must be re-run once more
after the v30a diff is applied (step A10) — this stamp does not substitute for that run.

Governing rules (verbatim anchors, all re-verified at the line numbers given):
- PREREG.md §0.2.1 (line 95): "Class C requires an amended registration, committed and
  externally timestamped before the affected detector is implemented or evaluated — a
  `prereg-v30a` tag, not a restart, and not a `DEVIATIONS.md` entry standing alone. The
  deviation records what was measured; the amended tag carries the new semantics. Both."
- PREREG.md §0.2.1 (line 97): "An amendment inherits §11's integrity chain in full: signed
  tag, both file hashes in the tag message, external timestamp receipt committed, repository
  publicly reachable at lock. An amendment weaker than the thing it amends is not one."
- PREREG.md §11 item 3 (line 1050): "SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md`
  as committed in the tag message and the README."
- PREREG.md §11 item 6 (line 1053): "`DEVIATIONS.md` append-only."
- PREREG.md §6.8 (line 647): "The tag gate is `--stage prereg` exit 0."
- PREREG.md §0.1 (line 77): "`PREREG.md` is the sole normative source for measurement
  semantics — units, states, denominators, gates, and what any published number means."
- PREREG.md §0.4 (line 140): "Every reversal, retraction, and firing this document has
  recorded is in `HISTORY.md`, committed with the pair and hashed in the tag message."
- README.md line 20: "The tag never moves." line 22: "These hashes are of the files as of tag
  `prereg-v30`." lines 23-24: "`DESIGN.md` and this README are revisable".

### The hash-count question, resolved — SIX for v30a (was five for v30)

§0.2.1 line 97 says "both file hashes"; §11 item 3 names **three** files; the v30 tag message
carries **five** (`PREREG.md`, `DESIGN.md`, `HISTORY.md`, `tools/check_registration.py`,
`protocol/runtime_reference.py`). The v30 practice is a superset of both statements. **v30a
carries six**, appending `AVAILABILITY_DECLARATION.md`.

**Why the declaration is in the block.** §0.2.1 line 97 requires the amendment to inherit §11's
integrity chain **"in full"** and closes "An amendment weaker than the thing it amends is not
one." The v30a amendment's new semantics rest on the availability declaration: it is the
artifact the amended sections cite, and it is the artifact a verifier must be able to pin. A
declaration reachable only through an untracked, unhashed path would make v30a's chain weaker
than v30's, which line 97 forbids. Six is therefore the floor, not an embellishment.

**Placement.** The declaration goes **last**, after the v30 five, in the v30 order. This keeps
the v30 five-line block a verbatim prefix of the v30a six-line block, so the addition is
visible by inspection and no v30-era verification instruction is invalidated.

## WORKING RESOLUTIONS BINDING THIS CEREMONY

R14 and R15 are **delta-issued** (2026-08-12) alongside R16 and R17. Like R1-R13 they are
PROVISIONAL until the `prereg-v30a` tag is signed, and like R14-R17 generally they are **not**
appended to the declaration's tail record, which is frozen. They are stated here in full
because this checklist is where they are executed.

> **R14 — SINGLE NORMATIVE COPY.** The repository-root `AVAILABILITY_DECLARATION.md` is the ONE
> normative copy of the availability declaration. The evidence tree carries a **pointer plus a
> recorded hash**, never a duplicate file. When the declaration changes, exactly two records are
> rewritten in the same pass: `evidence\fixture_spike\f4\DECLARATION_POINTER.md` and the
> `../AVAILABILITY_DECLARATION.md` line of `evidence\MANIFEST.sha256`.

> **R15 — SINGLE-OPERATION HASHING.** All six tag-message hashes are computed **at tag time**,
> **in one invocation**, from the files **as committed**, each preceded by a byte-comparison
> against its source. **No hash may be carried forward from an earlier sync, an earlier draft
> of this checklist, or an earlier tag** — including hashes expected to be unchanged.

**State of R14 as of this revision (already applied, not a pending step).**

- `evidence\fixture_spike\f4\availability_declaration_DRAFT.md` — the full duplicate — was
  **deleted**.
- `evidence\fixture_spike\f4\DECLARATION_POINTER.md` was written in its place: pointer
  statement, recorded sha256, size, date, and the R14 rationale.
- The repository-root `AVAILABILITY_DECLARATION.md` was **refreshed first**, from the live
  build copy at `…\scratchpad\fixture_spike\f4\availability_declaration_DRAFT.md`, and
  byte-compared after writing (`cmp` exit 0; 215256 == 215256 bytes; sha256 equal), so the
  pointer's recorded hash is of the current bytes:
      d1f43f51e3c31108e42ba53f40ea72b4ac7db0a2f9224ed528acad2a5cf9f83c  AVAILABILITY_DECLARATION.md
- **The near-miss this fixes, recorded.** Before the refresh, the evidence-tree duplicate and
  the repository-root copy were byte-identical at `e95063f4…` (176209 bytes) and **both were a
  version stale** — the live draft had already moved to `d1f43f51…` (215256 bytes) in the
  R11-batch pass. `sha256sum -c MANIFEST.sha256` would have returned **OK on both lines** while
  the declaration under verification was out of date. Two copies agreeing with each other and
  disagreeing with the source is the v23 duplicated-authority defect recurring in a new layer;
  the structural fix is one copy, not tighter synchronisation.

## FILES TOUCHED (mechanical envelope; content arrives as the reviewed diff)

| File | Change | Rule |
|---|---|---|
| PREREG.md | amended section(s) only | §0.2.1 l.95 "the amended tag carries the new semantics" |
| DEVIATIONS.md | APPEND entry D-001 — **file is still 0 bytes; writing it is ceremony step A3, not done** (skeleton at `f5\DEVIATIONS_entry_SKELETON.md`, filled with spike evidence) | §0.2.1 l.95 "The deviation records what was measured"; §11 item 6 append-only |
| HISTORY.md | **IN SCOPE, TWO CHANGES.** (1) ALREADY IN THE WORKING TREE: review lesson **H-L12** (the 37-vs-119 grep-undercount lesson, dated 12 Aug 2026) appended to the §9 lessons list. (2) STILL TO BE WRITTEN AT CEREMONY TIME: the **H-34** ledger entry for the amendment. Both are inside the one ceremony commit | §0.4 l.140; §11 item 3 |
| DESIGN.md | **IN SCOPE, ALREADY IN THE WORKING TREE:** §9's cross-reference bumped **H-L1..H-L11 -> H-L1..H-L12** (line 546) to match the H-L12 addition. Plus, conditionally, any section cross-reference the v30a diff moves. Reference only — "may never restate" | §0.1 l.77 single normative source |
| **AVAILABILITY_DECLARATION.md** | **NEW, currently UNTRACKED — `git add` it in the ceremony commit.** 215256 bytes, `d1f43f51…`. The R14 single normative copy; sixth hash in the tag message | §0.2.1 l.97 integrity chain "in full" |
| **evidence/** | **NEW, currently UNTRACKED — `git add evidence` in the ceremony commit.** 217 files under `evidence/fixture_spike/` plus `evidence/MANIFEST.sha256`. Not covered by `.gitignore` (verified: `git check-ignore` exit 1) | supporting record for D-001 and for the declaration |
| README.md | hash block: ADD a v30a block of **six** lines; KEEP the v30 five-line block (l.22: "These hashes are of the files as of tag `prereg-v30`."; l.20 "The tag never moves.") README is revisable (l.23-24) | §11 item 3 |
| VALIDATED_CONFIG.toml | untouched (placeholder until Phase 1 freezes) | §11 item 1 |
| tools/, protocol/, tests/ | untouched by a pure-text amendment. Their hashes are still **recomputed** at tag time under R15, never restated | no rule requires touching them |
| tagmsg-v30a.txt (NEW, working file) | tag message with the **six**-hash block | v30 precedent: `tagmsg.txt` exists untracked at repo root (confirmed absent from `git ls-files`) |
| amendment-commit-v30a.txt + .ots (NEW) | OTS artifact pair, committed AFTER the tag | §11 item 4; v30 precedent commits 5842857, 0ee26c4. Do NOT overwrite `registration-commit.txt` (v30's record) |

**Not touched, and it matters:** `.gitattributes` pins `* -text` — "every file is stored and
checked out byte-exact" — so working-tree sha256 == blob sha256 on every platform. Re-verified
on all five v30 files at `HEAD` on 2026-08-12; all five match the tag block exactly.

**Out of the checker's scan scope:** `check_registration.py` scans `PREREG.md` and `DESIGN.md`
for the single-source rule and lists `HISTORY.md` as out of scan scope by its own declaration.
`AVAILABILITY_DECLARATION.md` and `evidence/` are **not scanned at all**. The gate will not
catch a normative statement that migrates into the declaration; R14 and author review are the
only controls there. `REQUIRED_PATHS` is a presence-only list with no unexpected-file check, so
adding the two new paths cannot fail `structure` — confirmed by the PASS above, which was run
with both already on disk.

## HASH PROCEDURE — R15, SINGLE OPERATION (replaces the old two-command recompute)

**What this replaces and why.** Revision 1 of this checklist listed a working-tree
`sha256sum` recompute, a separate post-commit `git show | sha256sum` cross-check, and a block of
**pre-filled v30 hash values "for reference"**. That shape invites exactly one failure: a value
gets read off the reference block, or off an earlier sync, instead of off the file that is about
to be tagged — and the two hashes least likely to be re-derived are the two expected to be
unchanged. **The reference block is deleted.** No hash value appears anywhere in this section.

### R15 rule, stated

1. **One step.** All six hashes come from a **single invocation**, run once, at tag time.
2. **As committed.** Hashes are read from the **committed blobs** (`git cat-file -p HEAD:<path>`),
   not from the working tree.
3. **Byte-compared first.** Immediately before hashing, each of the six files is byte-compared
   against its source. Any non-zero `cmp` aborts the ceremony.
4. **Nothing carried forward.** No hash may be reused from an earlier sync, an earlier draft of
   this checklist, the v30 tag message, the v30 README block, `tagmsg.txt`, or
   `MANIFEST.sha256`. Every one of the six is re-derived, including
   `tools/check_registration.py` and `protocol/runtime_reference.py`, which are expected to be
   identical to v30 — **"expected identical" is a prediction to be tested, not a value to be
   copied.** If either differs from v30, that is a finding, not a typo to be corrected.

### Exact command sequence (run from the repository root, AFTER the ceremony commit exists)

**H0 — prove the working tree is the commit.** After A11, `AVAILABILITY_DECLARATION.md` and
`evidence/` are tracked, so the only untracked paths left are `.claude/`, `tagmsg.txt`,
`tagmsg-v30a.txt` and (after H2) `tagmsg-v30a.hashes.txt`. **Any ` M ` line** means a hashed
file was edited after the commit, and the ceremony aborts.

    git status --porcelain

**H1 — byte-compare each of the six files as committed against its working-tree source.**
All six must report `SAME`; a single `DIFFER` aborts. `cmp -s` is silent and returns 0 only on
byte-identity.

    bad=0
    for f in PREREG.md DESIGN.md HISTORY.md tools/check_registration.py \
             protocol/runtime_reference.py AVAILABILITY_DECLARATION.md; do
      if git cat-file -p "HEAD:$f" | cmp -s - "$f"; then
        printf 'SAME      %s\n' "$f"
      else
        printf 'DIFFER    %s  <-- ABORT\n' "$f"; bad=1
      fi
    done
    test "$bad" -eq 0 && echo "H1 OK — all six identical to their committed blobs"

**H1b — byte-compare the declaration against its build source** (the extra comparison R14
requires, because the declaration's source is outside the repository):

    cmp AVAILABILITY_DECLARATION.md \
      "C:/Users/ttbea/AppData/Local/Temp/claude/C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/fixture_spike/f4/availability_declaration_DRAFT.md"

**H2 — compute all six hashes in ONE invocation, from the committed blobs.** This is the only
place any v30a hash value is produced. Its output is the block that goes into `tagmsg-v30a.txt`
and into the README's v30a block, pasted, not retyped:

    for f in PREREG.md DESIGN.md HISTORY.md tools/check_registration.py \
             protocol/runtime_reference.py AVAILABILITY_DECLARATION.md; do
      printf '%s  %s\n' \
        "$(git cat-file -p "HEAD:$f" | sha256sum | cut -d' ' -f1)" "$f"
    done | tee tagmsg-v30a.hashes.txt

**H3 — independent cross-check, same six files, different reader.** Must be line-for-line
identical to H2's output (guaranteed by `* -text` plus the H1 comparison; if it is not, one of
those two assumptions is false and the ceremony aborts):

    sha256sum PREREG.md DESIGN.md HISTORY.md tools/check_registration.py \
              protocol/runtime_reference.py AVAILABILITY_DECLARATION.md \
      | sed 's/ \*/  /' | diff - tagmsg-v30a.hashes.txt && echo "H3 OK"

**H4 — destinations.** `tagmsg-v30a.txt` hash block, and the README's new v30a block. Both are
filled **from `tagmsg-v30a.hashes.txt` only**. After filling, re-diff both against it:

    diff <(sed -n '/^[0-9a-f]\{64\}  /p' tagmsg-v30a.txt) tagmsg-v30a.hashes.txt && echo "tagmsg OK"

Delete `tagmsg-v30a.hashes.txt` only after the tag is signed and verified — it is the audit
record of the single operation.

**Expected to change:** `PREREG.md` (always), `HISTORY.md` (H-L12 + H-34), `DESIGN.md` (the
H-L12 cross-reference bump, plus any moved reference), `AVAILABILITY_DECLARATION.md` (new).
**Expected unchanged:** `tools/check_registration.py`, `protocol/runtime_reference.py`.
`DEVIATIONS.md` is not in any hash block, so its D-001 append updates nothing here — but it is
still committed in the same commit, so it is inside the tagged tree.

## CEREMONY SEQUENCE (execute nothing now; [AUTHOR] = author-only step)

### Phase A — prepare and gate
A1. Clean baseline. `git status` at revision 2 shows ` M DESIGN.md`, ` M HISTORY.md`, and
    untracked `.claude/` (local tooling config, **never commit**), `AVAILABILITY_DECLARATION.md`,
    `evidence/`, `tagmsg.txt` (v30 ceremony leftover, untracked by precedent). The two modified
    files and the two new untracked paths are all IN SCOPE for this commit; `.claude/` and
    `tagmsg.txt` are not.
A2. [AUTHOR] Apply the reviewed v30a diff to `PREREG.md`. Amended sections only.
A3. Append `DEVIATIONS.md` entry D-001 (skeleton at `f5\DEVIATIONS_entry_SKELETON.md`, filled
    with spike evidence). **The file is still empty — this step has not been performed.**
    Append-only: nothing above the append point changes.
A4. Write the `HISTORY.md` **H-34** ledger entry for the amendment. Next free ID: H-33 is the
    highest (`HISTORY.md` line 258); H-34 goes after H-33's note and **before** the
    `### H-B addendum — firings v18 through v30` heading at line 263. Follow the house form:
    `### H-34 — from \`PREREG.md\` §<amended section>`, then an italic parenthetical note.
    **Add the reciprocal pointer** in the amended `PREREG.md` section: the convention is an
    inline `*(→ \`HISTORY.md\` H-34)*` marker (21 such markers exist today; H-33's is at
    `PREREG.md` line 877). A ledger entry no section points at is unreachable by the convention
    the other 21 follow.
    *(Revision 1 marked this "[AUTHOR decides]". §0.4 line 140 — "Every reversal, retraction,
    and firing this document has recorded is in `HISTORY.md`" — plus the H-L12 entry already
    sitting in the working tree settle it: the ledger is being written for this round either
    way, and an amendment absent from it is the one gap. Written, not decided.)*
A5. HISTORY.md/DESIGN.md working-tree edits: **verify, do not re-apply.** H-L12 is already
    appended in `HISTORY.md` §9's lessons list and `DESIGN.md` line 546 already reads
    "**H-L1** through **H-L12**". Confirm with `git diff --stat` (expect `DESIGN.md | 2 +-`,
    `HISTORY.md | 1 +`) before adding anything further.
A6. If the v30a diff moved any section reference `DESIGN.md` cites: update the reference only.
    The checker's `single_source` scan fails any restated formula, state, or denominator.
A7. **Do not compute hashes yet.** Hashing is R15's single operation and happens at step A12,
    after the commit exists. Revision 1 computed hashes here, before the commit — that ordering
    is what let a value drift between computation and tagging, and it is removed.
A8. Update `README.md`: add the v30a hash block (**six** lines) and the amendment paragraph;
    keep the v30 five-line block intact. Leave the six hash values as placeholders until A12.
A9. Write `tagmsg-v30a.txt` modeled on the v30 tag message (verbatim v30 structure: title line,
    then "SHA-256 of the registration documents and tooling as committed:", then the hash
    lines, then "Signing key: RSA 4096, Theo Johann Howard / Key fingerprint = 991F 5331 C584
    CE5E AF7D 6939 B29C F0E8 4711 9AD7", then the OTS paragraph "The commit hash is timestamped
    via OpenTimestamps; the .ots receipt is committed in a follow-up commit. This tag never
    moves."). For v30a: **six** hash lines (values placeholder until A12), and additionally name
    the amended sections and cite §0.2.1 class C.
A10. Gates, both green before commit (README Verify block, ll.47-50):

        python -m pytest tests/registration
        python tools/check_registration.py --stage prereg      # must exit 0 (§6.8)

     Note: the `lock_table` check requires each §0.1 lock-table row's key phrase to be present
     in its target section (§6.8 l.649) — if the v30a diff edits a locked section, the
     lock-table row must be part of the same reviewed diff or the checker fails.
A11. [AUTHOR] Final content approval, then commit — **one commit, everything in it**:

        git add PREREG.md DEVIATIONS.md HISTORY.md DESIGN.md README.md \
                AVAILABILITY_DECLARATION.md evidence
        git status --porcelain     # expect only ?? .claude/, ?? tagmsg.txt, ?? tagmsg-v30a.txt
        git commit -m "Pre-registration v30a: <amended sections> — class C amendment (PREREG §0.2.1)"

A12. **R15 single-operation hashing — run H0, H1, H1b, H2, H3 from the section above, in that
     order, now that the commit exists.** Paste H2's six lines into `tagmsg-v30a.txt` and the
     README v30a block (H4), then amend the commit to pick up the two filled files:

        git add README.md
        git commit --amend --no-edit
     Then **re-run H0-H3 against the amended commit** — amending changes `HEAD`, and hashes
     computed against the pre-amend `HEAD` are exactly the "carried forward" values R15
     forbids. `PREREG.md`, `HISTORY.md`, `DESIGN.md`, `AVAILABILITY_DECLARATION.md`,
     `tools/`, `protocol/` are unchanged by the amend, so their six values must reproduce
     byte-identically; `README.md` is not among the six.
     *(Alternative that avoids the amend entirely: fill README and tagmsg from a hash run
     against the staged index — `git cat-file -p :<path>` instead of `HEAD:<path>` — after
     `git add` but before `git commit`. Same single operation, same six files, no second
     commit. Choose one and record which in the ceremony record.)*

### Phase B — sign, verify, publish
B1. [AUTHOR — key passphrase] Sign the tag over the amendment commit:

        git -c gpg.program="C:\Program Files\GnuPG\bin\gpg.exe" tag -s prereg-v30a -F tagmsg-v30a.txt

    (`git config user.signingkey` = `B29CF0E847119AD7`, matches the README fingerprint tail;
     `gpg.exe` present at that path, re-verified 2026-08-12; secret key rsa4096/B29CF0E847119AD7
     in the keyring.)
B2. Verify the signature:

        git -c gpg.program="C:\Program Files\GnuPG\bin\gpg.exe" tag -v prereg-v30a

    Then read the six hash lines back **out of the signed tag object** and diff them against
    the single operation's output — not against `tagmsg-v30a.txt`, which is the file that was
    fed in and cannot detect its own mistranscription:

        git cat-file tag prereg-v30a | grep -E '^[0-9a-f]{64}  ' \
          | diff - tagmsg-v30a.hashes.txt && echo "B2 OK — signed object carries the six"
B3. Publish — §11 item 5: "The repository is publicly reachable at the moment of tagging."

        git push origin main
        git push origin prereg-v30a

    Remote: `origin = https://github.com/TheoJHoward/DataLeakageAuditor.git` (re-verified).

### Phase C — OpenTimestamps (v30 precedent: commits 5842857 then 0ee26c4)
Precedent, verbatim from `git log`: 5842857 "OpenTimestamps receipt for registration commit"
(added `registration-commit.txt` [1 line: `fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac`] +
`registration-commit.txt.ots` [584 bytes, pending]); 0ee26c4 "OpenTimestamps receipt upgraded:
Bitcoin attestations at blocks 961654 and 961656" (.ots 584 -> 2587 bytes). Rationale in README
ll.18-20: "a commit cannot contain the receipt for its own hash."

C1. Record the amendment commit hash (the commit the tag points at):

        git rev-parse prereg-v30a^{commit} > amendment-commit-v30a.txt

C2. [AUTHOR] Stamp:

        ots stamp amendment-commit-v30a.txt

    **READINESS BLOCKER — STILL OPEN, re-tested 2026-08-12.** The `ots` entry point at
    `C:\Users\ttbea\AppData\Local\Programs\Python\Python312\Scripts\ots` still crashes at
    import: `python -c "import bitcoin.rpc"` exits 1 with
    `ctypes\__init__.py line 369 ... TypeError: argument of type 'NoneType' is not iterable`
    (a python-bitcoinlib / Windows `find_library(ssl)` failure). The v30 receipt was nevertheless
    produced on 2026-08-08/09; which environment produced it is not determinable from the repo.
    The author must use whatever environment stamped v30, or repair this one. NOT fixed in this
    dry run.
C3. Commit the pair (follow-up commit, mirrors 5842857):

        git add amendment-commit-v30a.txt amendment-commit-v30a.txt.ots
        git commit -m "OpenTimestamps receipt for v30a amendment commit"
        git push origin main

C4. Hours-to-days later, upgrade and re-commit (mirrors 0ee26c4):

        ots upgrade amendment-commit-v30a.txt.ots
        ots verify amendment-commit-v30a.txt.ots
        git add amendment-commit-v30a.txt.ots
        git commit -m "OpenTimestamps receipt upgraded: Bitcoin attestations at blocks <N>, <M>"
        git push origin main

### Ordering constraint (hard)
§0.2.1 l.95: the amendment must be "committed and externally timestamped BEFORE the affected
detector is implemented or evaluated." Phase C1-C3 therefore precede any detector work that
depends on the amended semantics; the C4 upgrade may trail.

## FOR THE CEREMONY RECORD (not for any committed line)

**X6 — the corrected citation for the 119-file figure.** The H-L12 review lesson quotes "37
files" against "119". The evidence for 119 is:

    fixture_spike\c1\tagger_survey_capture.txt line 17 — "files with >=1 mention: 119"
    (line 16 carries the denominator, "total *.py scanned: 460")

**This citation does NOT go in the `HISTORY.md` line.** The staging file's own convention 7/8
states that the numbering is an ID and that "No entry cites an evidence path. Provenance for
this entry stays in this staging file and in the ceremony record, not in the line." The
orchestrator's instruction to "FIX the citation" therefore had no target inside the drafted
line, and the line was inserted without a path — the endorsed editor call. The citation lives
here, in the ceremony record, and in the declaration's §F.1, which already cites
`c1\tagger_survey_capture.txt` line 17 correctly. There is no `m1\` directory; any staging-file
row calling this "the M1 finding" is superseded by this note.

**Z2 — the obligation-vs-index staleness pattern has now occurred twice.** The pattern: an
obligation is stated in one place, and an index elsewhere that must reflect it goes stale,
while both remain internally consistent and therefore look correct.

1. **§13(g)'s labelling obligation vs the §18 evidence-class index.** §13(g) binds every
   appearance of `nq` in a table to carry the **TRADES-CLASSES-ONLY** label (4 of 10 classes
   scored; six MBO classes UNSCORED, not zero). The §B lattice-provenance table and the §18
   index row `f` still carried the pre-R12 wording. Fixed by the Z2 edits (r11batch edit ledger
   rows E23 and E24).
2. **The declaration vs `MANIFEST.sha256` and the f4 duplicate** — the R14 near-miss recorded
   above. The manifest is an index; the declaration is the obligation-bearing artifact. The
   index recorded `e95063f4…` while the source had moved to `d1f43f51…`, and because the f4
   duplicate carried the same stale bytes, the index verified **OK** against a stale file.

   *(A third instance of the same class sits in the working tree and is already fixed:
   `DESIGN.md` line 546's `H-L1 through H-L11` was an index into `HISTORY.md`'s lessons list,
   and went stale the moment H-L12 was appended. It is listed here because it is the same
   failure shape, and because the fix — bump the index in the same edit that changes the thing
   indexed — is the general remedy.)*

**Standing remedy adopted:** whenever an obligation changes, the same pass rewrites every index
that quotes it, and the pass names them. R14's two-record rule and R15's no-carry-forward rule
are the two instances of this remedy that are mechanically enforced.

> **Provenance caveat on this note, flagged for the author.** There is **no `z2\` directory** in
> the build tree and no artifact that records Z2's own finding in its own words. Instance 1 above
> is reconstructed from the r11batch edit ledger (`r11batch\edit_ledger.py`, rows E23 and E24,
> both labelled `(Z2)`) and from §13(g)'s obligation text as it now stands; instance 2 is
> measured directly in this pass. If the pair Z2 actually intended is a different pair, this note
> is the thing to correct — the pattern claim does not depend on which two, but the ceremony
> record should name the right ones.

## RE-VERIFICATION STAMP — 2026-08-12 (item Y5)

Every numbered step re-walked against the repo state on this date. **No ceremony step was
executed.** The read-only `--stage prereg` run and the read-only `import bitcoin.rpc` probe are
verifications of this checklist's own baseline claims, not performances of steps A10 or C2.

| Step | Status | Note |
|---|---|---|
| Baseline block | CURRENT (rewritten) | HEAD, tag, remote, signingkey, DEVIATIONS size, gate PASS all re-derived today |
| Governing-rule anchors | CURRENT | all eight line anchors re-read and matching |
| Hash-count note | CURRENT (rewritten) | five -> six, with the §0.2.1 l.97 justification and the placement rule |
| FILES TOUCHED table | CURRENT (rewritten) | HISTORY/DESIGN moved from conditional to in-scope; declaration and evidence/ added |
| Hash procedure | CURRENT (rewritten as R15) | reference hash block deleted; single operation; byte-compare; no-carry-forward |
| A1 | CURRENT (rewritten) | working tree is no longer clean; the two ` M ` files are in scope |
| A2 | CURRENT | unchanged |
| A3 | CURRENT | `DEVIATIONS.md` re-confirmed 0 bytes; still a ceremony step, still not done |
| A4 | CURRENT (rewritten) | was "[AUTHOR decides]"; now written, with H-34 placement and the reciprocal `*(→ HISTORY.md H-34)*` pointer |
| A5 | NEW | verify-don't-reapply step for the H-L12 pair already in the working tree |
| A6 | CURRENT | was A5 |
| A7 | CURRENT (rewritten) | was "recompute the five hashes here"; hashing moved to A12 under R15 |
| A8 | CURRENT (rewritten) | was A7; six-line block, placeholders until A12 |
| A9 | CURRENT (rewritten) | was A8; six hash lines |
| A10 | CURRENT | was A9; both gate commands re-verified present and correct |
| A11 | CURRENT (rewritten) | was A10; `git add` list now names all six paths + `evidence` |
| A12 | NEW | the R15 single operation, plus the amend-re-hash trap and the staged-index alternative |
| B1 | CURRENT | gpg.exe present; signingkey matches README fingerprint tail |
| B2 | CURRENT (extended) | added the read-back-from-the-signed-object check |
| B3 | CURRENT | remote re-verified |
| C1 | CURRENT | unchanged |
| C2 | CURRENT — **BLOCKER STILL OPEN** | `import bitcoin.rpc` still raises the same ctypes TypeError |
| C3 | CURRENT | unchanged |
| C4 | CURRENT | unchanged |
| Ordering constraint | CURRENT | unchanged |
| Author-only summary | CURRENT (rewritten) | A12 added |

### Author-only summary
- A2 / A11: reviewed amendment text and final approval (standing rule: the author signs).
- A12: the R15 hashing operation is mechanical, but the paste into `tagmsg-v30a.txt` and the
  README is the author's, and the abort conditions are the author's call.
- B1: GPG key passphrase.
- C2 / C4: OTS stamping from the author's working environment — **blocked in this one**.
