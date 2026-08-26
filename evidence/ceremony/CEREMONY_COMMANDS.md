⛔ **BLOCKER — THE PHASE 0 KILL-GATE SIGN-OFF DOES NOT EXIST, `PREREG.md` §10.0 SEQUENCES IT BEFORE THE TAG, AND THE CEREMONY CANNOT PROCEED WITHOUT IT NO MATTER HOW FINISHED THE DOCUMENTS ARE.**

# CEREMONY_COMMANDS — `prereg-v30a`, exact ordered sequence

# ⛔ BLOCKED. DO NOT RUN ANY COMMAND IN THIS FILE.

**ITEM PART D. NOTHING BELOW HAS BEEN EXECUTED.** No `git add`, no `git commit`, no `git tag`,
no `git push`, no hashing of committed or staged state, no `ots`. Every command in this file is a
written plan for the author. The only commands run while producing it were read-only inspections
(`git status`, `log`, `show --stat`, `ls-files`, `diff`, `cat-file`, `tag -l`, `check-ignore`,
`remote -v`, `config`; `stat`, `find`, `cmp`, `sha256sum`, `sha256sum -c`).

**Regenerated 2026-08-13 against the CURRENT state**, after the §A.6.0 recovery and under DELTA
R15's C1–C5. The previous revision of this file is superseded in full, not patched.

---

# §0 — THE BLOCKER, RESTATED WITH ITS EVIDENCE

`PREREG.md` **§10's phase table, the Phase 0 row** lists Phase 0's work as **four items behind one gate**:
*(Was "line 991" until R95/§146.4. This file points a CURRENT reader at CURRENT text, so the reference is an anchor now — §17.2's remedy — and survives the next insertion.)*

> | **0** | Fixture declaration reconstruction with evidence; prior-art verification; cross-tool comparison per §9.2; licence check | 1–2 wknds | **Kill gate (§10.1)** |

| Phase 0 work item | State, measured this pass | Evidence |
|---|---|---|
| Fixture declaration reconstruction with evidence | **done** | `AVAILABILITY_DECLARATION.md` — **do not read the size or hash from here.** Derive: `sha256sum AVAILABILITY_DECLARATION.md`, `wc -c`. As at R69: `4c07c76f…`, 303,643 bytes. *(Read `f0829bd3…` / 277,411 for several rounds after the file had moved; checked by D7 from R68.)* |
| Prior-art verification | **DONE and signed off** | `HISTORY.md` H-34 (cited by its `### H-34` heading, not by line — `l.264–292` drifted as lessons were appended; author-attributed, 12 Aug 2026, verdict "§10.1 does NOT fire"); `PRIOR_ART_VERIFICATION.md` sha256 `b97a2804…` |
| **Cross-tool comparison per §9.2** | **RAN 14 Aug 2026, but does NOT satisfy §9.2** | Executed: 11 tools, 8 hand-written cases + 8 clean paired controls, 88 cells (`killgate/k6/K6_RESULTS.md`); case set authored before the first run (29.261 s, hash chain 112/112). **Not §9.2-compliant:** the set is in no commit, so "committed with this protocol" is breached and uncurable for `prereg-v30`; the acceptance-fixture half was not run; **§10.1 criterion 3 remains unevaluated**. Unverified by any party that did not perform it. `DEVIATIONS.md` D-003. *(Row corrected 21 Aug 2026, R48/Q2 — it previously read **NOT RUN**, citing a declaration line that was itself false.)* |
| **Licence check** | **partial** | `deepchecks` AGPL-3.0 recorded in H-34 with the Phase 6 wrap constraint noted; no completed licence-check artifact exists |

**One of four items is signed off. The gate is not.** A sign-off for prior art is not a sign-off
for Phase 0, and §10.0 sequences Phase 0's gate before everything below it.

**The judgment this leaves to the author, stated rather than decided here.** §10.1 stops the
project only if a single maintained tool satisfies all five criteria. H-34 argues the gate cannot
fire because no candidate is equivalent in kind — criterion 1 fails for every candidate, so
criterion 3, which the §9.2 cross-tool run would measure, cannot rescue any of them. **That
reasoning may well stand without the run.** What it does not do is discharge the two remaining
Phase 0 *work* items, which line 991 lists as deliverables independent of how the gate resolves.

**The author must put one of two statements on the record before step C5 runs:**

- **(a)** the §9.2 cross-tool comparison and the licence check gate the **tag** — the ceremony does
  not proceed until they are run; or
- **(b)** they gate **Phase 1 entry** but not the amendment tag — H-34's verdict is the sign-off
  the tag needs, and the two items are carried forward as named open obligations.

**Nothing in this file may run until that is on the record.**

### RECORDED — THE AUTHOR'S ROUTING DECISION, 25 AUGUST 2026

**Branch (b) is chosen.** Recorded here, before C5, as §0 requires. Verbatim, attributed:

> **Blocker 1, §10.0 routing. Recorded by the author, 25 August 2026:** the §9.2 cross-tool
> comparison and the licence check gate **PHASE 1 ENTRY**, not the `prereg-v30a` amendment tag.
> H-34's verdict is the sign-off the tag requires. **Both items are carried forward as named open
> obligations that must be discharged before Phase 1 entry; neither is waived, satisfied, or
> weakened by the tag.** *Re-fire condition:* if a tool implementing runtime probing against a
> declared per-cell availability model surfaces before Phase 1 entry, the §10.1 gate **re-fires**
> and this routing does not shield it.

**Effect on this file.** The §0 precondition is satisfied: a statement is on the record. **C5 is
unblocked** on this ground. Every other §0 blocker stands unchanged — this decision routes the
kill gate and does nothing else.

**What this is NOT.** It is not the §10.1 attestation, and it is not a finding that the gate does
not fire. It is a **routing decision** about which milestone the two outstanding Phase 0 work items
gate. *(Recorded because earlier rounds of this working session characterised blocker 1 as the
§10.1 attestation itself; that characterisation was wrong and is corrected here and at
`COMMIT_PLAN.md` §8.)*


## Ordering that is NOT in doubt

- **`PREREG.md` §10.0 item 0** — "If Phase 0 recorded the fixture as semantically ambiguous, the
  class C amendment of §10.2 is committed and timestamped before anything below" — **does not
  fire.** Declaration §A.5: the original work DID document prediction timing, so the fixture is
  not semantically ambiguous. The clause is satisfied by not applying.
- **`PREREG.md` §10.0 step 3** — "a class C change requires an amended registration committed and
  timestamped before step 4" — **does bind.** Step 4 is the Phase 1 freeze. So the OTS stamp of
  §5 must complete before any Phase 1 freeze.
- **`PREREG.md` §0.2.1 line 95** — "committed and externally timestamped **before the affected
  detector is implemented or evaluated**." No detector exists (`README.md` line 12), so the
  ex-ante path is available and the §6.4 re-draw path does not apply. **That window is what the
  ceremony is for, and it closes the moment detector work starts.**
- **⛔ THE CHECKER EDIT AND THE AMENDMENT ARE ONE COMMIT. THIS ORDERING IS LOAD-BEARING AND MUST
  NOT BE SPLIT.** `tools/check_registration.py` exempts the declaration's decision-log tail from
  the single-source scan, by explicit range and **only while that region hashes to the value
  recorded in the checker**. That exemption is sound **only once `PREREG.md` carries the rules the
  tail records** — SC-4 for the criterion-1 denominator and the three-class partition, SC-3 for the
  amended acceptance criterion 3. **Until SC-4 lands, the tail's R11 text is that rule's only
  statement, and exempting it would mask a real §0.2.1 defect rather than excuse a quotation.**
  Staging the checker without the amendment ships a checker that passes for the wrong reason.
  Staging the amendment without the checker ships a red CI gate. **Both files are in the fixed six
  (§3.2); neither may be committed without the other.** If the ceremony is ever split across two
  commits, this constraint is violated and the split is the defect, not the fix.

## Secondary blockers, each independently sufficient to stop the ceremony

| # | Blocker | State this pass |
|---|---|---|
| B1 | The amendment itself does not exist: `PREREG.md` is **clean** (sha256 `f0a8f001…`, byte-identical to its `prereg-v30` tagged state). The four §6.2 amendments and the §10.2 "waived" definition exist **only** in the declaration. §0.1 makes `PREREG.md` the sole normative source. **A tag over the current tree amends nothing.** | **NOT DONE** |
| B2 | `DEVIATIONS.md` is **0 bytes**. Draft: `DEVIATIONS_DRAFT.md` §1. | **NOT DONE** |
| B3 | The `HISTORY.md` amendment ledger entry is not written, and the ID working resolution R8 assigns it (**H-34**) is **taken** by the kill-gate sign-off. Draft, as **H-35**: `H34_DRAFT.md` §3. | **NOT DONE** |
| B4 | `README.md` carries no v30a hash block. `README.md` is clean, sha256 `7a0a0310…`. | **NOT DONE** |
| B5 | ~~`evidence/MANIFEST.sha256` does not verify: 245 OK, 1 FAILED~~ **RESOLVED R67/R68: 251 OK, 0 FAILED**, re-derived in the same pass as each change (R15), LF preserved, and C2d-2's three-way agreement green. *This row read "245 OK, 1 FAILED" after the failure was repaired — a stale blocker is as misleading as a stale count.* Re-verify at stage time; the tree moves. See `COMMIT_PLAN.md` §5. | **DONE, re-verify at stage time** |
| B6 | The `ots` CLI is broken in this environment. See §5. | **AUTHOR-ONLY workaround** |

---

# §1 — AUTHOR-ONLY STEPS

**`[AUTHOR]` marks a step no agent may perform under any circumstances.**

| Step | Why author-only |
|---|---|
| §0 blocker resolution | A judgment about the registration's own sequencing. |
| The reviewed `PREREG.md` v30a diff | Content of a locked file. The author signs what the author wrote. |
| Final content approval before the commit | Same. |
| **C1 — `git tag -s`** | **THE GPG KEY PASSPHRASE IS NEVER HANDLED BY AN AGENT — never typed by an agent, never stored, never read, never echoed. The author signs at their own terminal.** |
| **C4 — the OpenTimestamps stamp** | Per the v30 precedent the stamp is performed by the author through the OpenTimestamps **web UI**. The `ots` CLI in this environment crashes at import. |

Everything else is mechanical and reproducible, and every mechanical step has an explicit halt.

---

# §2 — C5: REMOTE IDENTITY. THE MANDATORY FIRST COMMAND.

**Nothing else in this file runs before this. Not a `git add`, not a hash, not a status check.**
A ceremony whose §11 obligation is "the repository is publicly reachable at the moment of tagging"
must first establish *which* repository it is about to make reachable.

```sh
# C5 — FIRST COMMAND OF THE CEREMONY. Run from the repository root,
#      C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01
git remote -v
```

**EXPECTED, exactly — both lines, both directions:**

```
origin	https://github.com/TheoJHoward/DataLeakageAuditor.git (fetch)
origin	https://github.com/TheoJHoward/DataLeakageAuditor.git (push)
```

**HALT CONDITION.** If the URL differs in any character — a different host, a different owner, a
different repository name, an `ssh://` or `git@` form, an extra remote, a missing `push` line, or
no `origin` at all — **STOP. Do not stage, do not commit, do not tag, do not push.** The
registration's public-reachability obligation names one repository; a tag pushed to a different
one is not the registration being amended, and a signed tag cannot be un-pushed.

Two supporting reads, run immediately after, neither of which may be skipped:

```sh
git rev-list -n 1 prereg-v30             # expect fe0d5a5708cfe1f817bd50e12a2cd02c2b4456ac
                                         # (a TAG never moves — safe to state)
git tag -l                               # expect exactly one line: prereg-v30
git config user.signingkey               # expect B29CF0E847119AD7
git config gpg.program                   # expect C:\Program Files\GnuPG\bin\gpg.exe
```

`prereg-v30a` **must not already exist**. If `git tag -l` shows it, stop and find out why.

## C5b — HEAD IS DERIVED AND ACCOUNTED FOR, NEVER PINNED (R97/§158)

**This replaced a `# expect <hash>` literal for `HEAD`.** That literal was a carried-forward value:
it named the commit that happened to be current when the line was written, and the first legitimate
commit after it — `80401d0`, H-34's kill-gate sign-off — made the ceremony halt on its own success.
**Writing a fresher hash there would restore the defect with a newer value.** So the assertion is
replaced by a derivation plus an accounting.

```sh
# C5b — (a) HEAD descends from the tag; (b) enumerate; (c) each accounted for;
#       (d) unaccounted = HALT, newly accounted = fine.
base=$(git rev-list -n 1 prereg-v30)
git merge-base --is-ancestor "$base" HEAD || {
  echo "C5b FAILED — HEAD does not descend from prereg-v30. HALT."; exit 1; }

acct=evidence/ceremony/COMMIT_ACCOUNTING.md
unaccounted=0
for c in $(git rev-list "$base"..HEAD); do
  short=$(git rev-parse --short=7 "$c")
  if grep -q "account: $short" "$acct"; then
    printf 'C5b  accounted   %s  %s\n' "$short" "$(git log -1 --format=%s "$c")"
  else
    printf 'C5b  UNACCOUNTED %s  %s\n' "$short" "$(git log -1 --format=%s "$c")"
    unaccounted=1
  fi
done
[ "$unaccounted" -eq 0 ] || {
  echo "C5b FAILED — a commit between prereg-v30 and HEAD is not accounted for in $acct."
  echo "             Account for it there, or establish that it does not belong in the"
  echo "             tagged tree. Do NOT widen this check. HALT."; exit 1; }
echo "C5b OK — HEAD descends from prereg-v30 and every commit since is accounted for"
```

**Why this shape.** A pinned expectation goes stale on legitimate work and says nothing about what
changed; a derivation plus an accounting **reports the work and demands a reason for it**. New
commits are expected — that is what a live repository does — and the check now asks the question
worth asking: *does this commit belong in the tree the tag is about to lock?*

---

# §3 — STAGE, THEN C2: THE SINGLE HASHING OPERATION

Staging is `COMMIT_PLAN.md` §4 and is not repeated here. **C2 runs after `git add` and before
`git commit`**, so the hashes are read from the index — which is what the commit will contain,
byte for byte — and no amend is ever needed to fill the tag message.

## 3.1 The rule, stated so it cannot be softened in the moment

1. **ONE OPERATION.** All six hashes come from a **single invocation**, run once, at tag time.
2. **FROM STAGED CONTENT.** Every hash is read from the index — `git show :<path>` — never from
   the working tree and never from an earlier commit.
3. **BYTE-COMPARED FIRST.** Immediately before hashing, each of the six is byte-compared against
   its working-tree source. Any difference halts.
4. **NOTHING CARRIED FORWARD.**

> ## 🚫 NO HASH MAY BE CARRIED FORWARD — FROM ANYTHING
>
> Not from an earlier sync. Not from an earlier checklist. Not from the `prereg-v30` tag message.
> Not from the v30 README block. Not from the existing `tagmsg.txt`. Not from
> `evidence/MANIFEST.sha256`. Not from `evidence/fixture_spike/f4/DECLARATION_POINTER.md`. Not
> from this package — **`COMMIT_PLAN.md`, `DEVIATIONS_DRAFT.md` and §0 above quote hash values as
> evidence of state, and NONE of them may be typed into a tag message or a README.** Not from an
> earlier run of C2 in the same session.
>
> Every one of the six is re-derived, **including `tools/check_registration.py` and
> `protocol/runtime_reference.py`, which are expected to be identical to their v30 values.
> "Expected identical" is a prediction to be tested, not a value to be copied.** If either differs
> from v30, **that is a finding, not a typo to be corrected** — halt and record it.
>
> **No hash value appears anywhere in §3 of this file.** That is deliberate and must stay true of
> any revision of it.

## 3.2 The FIXED SIX. The list is closed.

```sh
# The six files whose hashes the prereg-v30a tag message carries.
# FIXED. Not derived from `git status`, not filtered, not extended, not shortened.
FILES="PREREG.md DESIGN.md HISTORY.md tools/check_registration.py protocol/runtime_reference.py AVAILABILITY_DECLARATION.md"
```

Declared by `AVAILABILITY_DECLARATION.md` **§D.2** (heading: “D.2 — The v30a tag message carries
SIX hashes” — cited by anchor, not by line: the declaration is a living document and the line
number this read until R67/§17.2, `l.3420`, had drifted 169 lines): the five the `prereg-v30` tag carries,
recomputed at their v30a state, **plus** the SHA-256 of the declaration itself. Order is the v30
order with the declaration appended **last**, so the v30 five-line block stays a verbatim prefix
of the v30a six-line block and no v30-era verification instruction is invalidated.

**The six/seven question is `COMMIT_PLAN.md` §6's, not this file's — and it is now CLOSED as SIX** (R67/§14.1; `COMMIT_PLAN.md` §6, blocker item 8). This file is
written for **SIX**, and that is now the decided state, not a default awaiting an author.

*(The declined candidate was `PRIOR_ART_VERIFICATION.md`. Had it been admitted, the change was
exactly two edits: append it to the `FILES` line above **and to nothing else in this file**, and
edit §D.2 to say seven *before* C2 runs. Recorded so the record shows what was declined and why;
the reasons are at `COMMIT_PLAN.md` §6. Adding a file later is a Class B change — a parameter of a
locked procedure — so this is reversible.)*

**`FILES` above is the single authority for the set.** Every gate in this file iterates it — C2a,
C2b, C2c, C2, C2e, C2f, C1c — and no gate reads a numeral. Any count elsewhere in this repository
is a RESTATEMENT of this line and is checked against it by `tools/check_registration.py`'s
single-source scan (R67/§16). If a count and this line disagree, **this line wins**.

## 3.3 The pre-hash checks. An unstaged member is an ERROR TO REPORT, never a file to skip.

**This is the check the whole operation turns on.** `git show :<path>` on a tracked file that was
never `git add`ed does **not** fail — it silently returns the file's `HEAD` content. So a
registration document edited in the working tree and left unstaged would be hashed at its *old*
bytes, the tag would be signed over content the author did not approve, and nothing in the
ceremony would say so.

```sh
# C2a — DOES EVERY MEMBER OF THE SIX EXIST IN THE INDEX?
missing=0
for f in $FILES; do
  if git show ":$f" > /dev/null 2>&1; then
    printf 'IN-INDEX  %s\n' "$f"
  else
    printf 'NOT-IN-INDEX  %s  <-- ERROR: REPORT AND HALT\n' "$f"; missing=1
  fi
done
test "$missing" -eq 0 && echo "C2a OK — all six are in the index" || {
  echo "C2a FAILED — a member of the six is not staged. HALT."; exit 1; }
```

```sh
# C2b — IS ANY MEMBER OF THE SIX MODIFIED IN THE WORKING TREE BUT NOT STAGED?
git diff --name-only -- $FILES
```

**EXPECTED: no output.** Any path printed here is a hashed registration document whose staged
bytes and working-tree bytes differ.

> ### ⛔ WHAT TO DO WITH AN UNSTAGED MEMBER OF THE SIX
>
> **HALT AND REPORT IT. Do not skip the file. Do not drop it from `FILES`. Do not reflexively
> `git add` it and continue.**
>
> The six is a fixed set: a tag message with five lines is not a v30a tag message, and a tag
> message whose sixth line is absent because the file "wasn't ready" is precisely the
> "amendment weaker than the thing it amends" §0.2.1 line 97 forbids. Equally, quietly staging the
> file substitutes the agent's judgment for the author's content approval on a locked-registration
> document.
>
> The correct response is: **stop, print the path, print `git diff -- <path>`, and put the
> divergence in front of the author.** The author decides whether the working-tree state is the
> state to be tagged. Only then is the file staged, and **C2 restarts from C2a** — the whole
> operation, not the remaining files.

```sh
# C2c — BYTE-COMPARE EACH OF THE SIX, STAGED CONTENT vs WORKING-TREE SOURCE.
#       This is the loop, verbatim. It runs immediately before the hashing and
#       nothing may run between them.
bad=0
for f in $FILES; do
  if git show ":$f" | cmp -s - "$f"; then
    printf 'SAME      %s\n' "$f"
  else
    printf 'DIFFER    %s  <-- HALT\n' "$f"; bad=1
  fi
done
test "$bad" -eq 0 && echo "C2c OK — all six staged blobs are byte-identical to their sources"
```

All six must report `SAME`. **A single `DIFFER` halts the ceremony.** `cmp -s` is silent and
returns 0 only on byte-identity. `.gitattributes` pins `* -text`, so no line-ending translation
can make a staged blob differ from its working-tree file for a benign reason — a `DIFFER` here is
always a real divergence.

```sh
# C2d-1 — REVERSE DIRECTION. Run BEFORE C2d.
#   `sha256sum -c` walks the MANIFEST and checks each listed path against disk.
#   It cannot see a file that is STAGED BUT NOT LISTED. Such a file ships inside
#   the signed commit with nothing attesting its bytes, and C2d still reports OK.
git diff --cached --name-only -- evidence \
  | sed 's|^evidence/||' | grep -v '^MANIFEST\.sha256$' | sort > /tmp/_staged.$$
grep -oE '^[0-9a-f]{64}  .+$' evidence/MANIFEST.sha256 \
  | sed 's/^[0-9a-f]\{64\}  //' | grep -v '^\.\./' | sort > /tmp/_listed.$$
unlisted=$(comm -23 /tmp/_staged.$$ /tmp/_listed.$$)
rm -f /tmp/_staged.$$ /tmp/_listed.$$
if [ -n "$unlisted" ]; then
  echo "C2d-1 FAILED — staged but NOT in the manifest, would ship unattested:"
  printf '%s\n' "$unlisted"; exit 1
fi
echo "C2d-1 OK — every staged evidence file has a manifest line"

# C2d — the evidence manifest verifies against the tree about to be committed
(cd evidence && sha256sum -c MANIFEST.sha256)
# REQUIRED: every line OK, zero FAILED. Any FAILED line halts. (Blocker B5 today.)
```

### C2d-2 — THREE-WAY AGREEMENT ON THE DECLARATION HASH. A GATE, NOT A NOTE.

**Why this is a gate.** Three artifacts record the declaration's hash: the declaration itself, the
pointer at `evidence/fixture_spike/f4/DECLARATION_POINTER.md`, and the `../AVAILABILITY_DECLARATION.md`
line of `evidence/MANIFEST.sha256`. The manifest header states the rule — *"The pointer's recorded
hash and the `../AVAILABILITY_DECLARATION.md` line are rewritten in the same pass, always; a hash
carried forward from an earlier sync is prohibited (R15)"* — and **that rule was broken once**: after
the v30a declaration scrub the manifest line was rewritten and the pointer was not, so the pointer
recorded a superseded hash for a full round. `sha256sum -c` did **not** catch it, and cannot: it
verifies the pointer file's own bytes, never the hash written *inside* it. Nothing enforced the
agreement, so it drifted. This check is what enforces it.

```sh
# C2d-0 — LINE ENDINGS. Run BEFORE C2d. `evidence/MANIFEST.sha256` must be LF while the rest
# of this repository is CRLF: sha256sum -c takes a trailing CR as part of the filename, so a CRLF
# manifest fails all 251 entries with "No such file or directory" - which looks exactly like
# corrupted evidence. Observed 21 Aug 2026: 251/251 failed, then 251/251 passed after an LF rewrite.
if grep -q $'\r' evidence/MANIFEST.sha256; then
  echo "MANIFEST.sha256 has CRLF - HALT. Rewrite it with LF before verifying."; exit 1
else
  echo "MANIFEST.sha256 is LF - proceed"
fi

# C2d-2 — the declaration, the pointer's recorded hash, and the manifest line must agree.
#         Run from the repository root. All three values must be identical.
ACTUAL=$(sha256sum AVAILABILITY_DECLARATION.md | awk '{print $1}')
POINTER=$(grep -oE '[0-9a-f]{64}' evidence/fixture_spike/f4/DECLARATION_POINTER.md | head -1)
MANIFEST=$(awk '$2=="../AVAILABILITY_DECLARATION.md"{print $1}' evidence/MANIFEST.sha256)
printf 'declaration : %s\npointer     : %s\nmanifest    : %s\n' "$ACTUAL" "$POINTER" "$MANIFEST"
if [ "$ACTUAL" = "$POINTER" ] && [ "$ACTUAL" = "$MANIFEST" ]; then
  echo "C2d-2 OK — declaration, pointer and manifest agree"
else
  echo "C2d-2 FAILED — the three do not agree. HALT."; exit 1
fi
```

**REQUIRED: `AGREE — proceed`.** A `DISAGREE` halts the ceremony. Do not repair it by editing
whichever record looks wrong: re-derive the declaration's hash, then rewrite the pointer block and
the manifest line **in the same pass**, which is what R15 requires and what failing to do produced
the drift this check exists to catch.

### C2.5 — SC-4(k2)'s TWO CONDITIONS ON THE FIXTURE MANIFEST. A GATE, NOT A NOTE.

SC-4(k2) makes the gate read the fixture manifest's list of leaking-source columns, and imposes
two conditions on it. **SC-4(k4) indexes both as ways the limb FAILS.** Until R68 those conditions
lived only as prose in the regeneration requirements: **a condition stated by a clause and enforced
by no step.** That is the §21 class one stage earlier than a print — not a check that fails to
assert, but a check that was never written.

**Both conditions are UNMET as this is written, and this gate is expected to FAIL today.** That is
its purpose: it turns a known blocker from a paragraph somebody must remember into a step that
stops the ceremony.

```sh
# C2.5 — the manifest SC-4(k2) reads must be frozen, and must not be a draft.
MANIFEST='evidence/fixture_spike/f3/fixture_manifest_DRAFT.json'
c25=0

# (i) recorded status must not be DRAFT at the tag
status=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('manifest_status',''))" "$MANIFEST")
case "$status" in
  ''|*DRAFT*|*draft*) echo "C2.5 (i) FAILED — manifest_status is '$status'"; c25=1 ;;
  *)                  echo "C2.5 (i) OK — manifest_status is '$status'" ;;
esac

# (ii) the manifest must be enumerated in the declaration's SC-8(a) freeze.
#      SCOPED TO §D.1 ITEM 3's "Specifically and exhaustively" list — NOT to §D.1 as a whole.
#      Grepping the whole section returns a FALSE OK: the filename does appear in §D.1,
#      inside item 2's prose, which is not membership of the exhaustive enumeration.
exhaustive=$(sed -n '/^### D\.1 /,/^### D\.2 /p' AVAILABILITY_DECLARATION.md \
             | sed -n '/Specifically and exhaustively/,/^4\. /p')
if printf '%s\n' "$exhaustive" | grep -q 'fixture_manifest_DRAFT\.json'; then
  echo "C2.5 (ii) OK — the manifest is enumerated in the §D.1 exhaustive freeze list"
else
  echo "C2.5 (ii) FAILED — §D.1 item 3's exhaustive list does not name the manifest"; c25=1
fi

[ "$c25" -eq 0 ] || { echo "C2.5 FAILED — SC-4(k4) makes each of these a limb failure. HALT."; exit 1; }
echo "C2.5 OK — both SC-4(k2) conditions hold"
```

**Why this halts rather than warns.** Tagging with either condition unmet ships an amendment whose
own gate limb is unsatisfied on the day it is signed, **by its own registered text**. `PREREG.md`
§0.2.1 line 97: an amendment weaker than the thing it amends is not one.

## 3.4 C2 — THE SINGLE OPERATION

**This is the only place any `prereg-v30a` hash value is produced.**

```sh
# C2 — one invocation, six files, staged content, run once.
for f in $FILES; do
  printf '%s  %s\n' "$(git show ":$f" | sha256sum | cut -d' ' -f1)" "$f"
done | tee v30a.hashes.txt
```

Two spaces between hash and path, matching `sha256sum` output and the `prereg-v30` tag block.
`v30a.hashes.txt` is the audit record of the operation. **It is never committed** — it is
untracked, it is excluded from the commit by `COMMIT_PLAN.md` §2, and it is deleted only after the
tag verifies at C1b.

```sh
# C2e — independent cross-check: same six files, different reader, working tree not index.
sha256sum $FILES | sed 's/ \*/  /' | diff - v30a.hashes.txt && echo "C2e OK"
```

Must be line-for-line identical. Identity is guaranteed by `.gitattributes`' `* -text` plus C2c's
comparison. **If it is not identical, one of those two assumptions is false. HALT.**

## 3.5 The tag message, written to `tagmsg.txt` at tag time

**`tagmsg.txt` at the repository root is SUPERSEDED and is overwritten at this step.** Its current
content (770 bytes, sha256 `98c76f3e…`) was compared byte-for-byte this pass against the body of
the signed `prereg-v30` tag object and is **identical** — it is the v30 ceremony's leftover
message file. Overwriting it destroys nothing: the v30 message is recoverable in perpetuity from
the signed tag object itself (`git cat-file tag prereg-v30`). It stays **untracked** and is
**excluded from the commit**, matching the v30 precedent.

**Format of the file, written at tag time:**

```
Pre-registration v30a — Data Leakage Auditor (class C amendment, PREREG §0.2.1)

Amends PREREG.md §6.2 — reference AUC (l.445), contamination availability class
recording locus (l.450), sliced CI variant (l.451), criterion 3 (l.461) — and
defines "waived" for §10.2's replacement-criterion floor.

SHA-256 of the registration documents and tooling as committed:

<64 hex>  PREREG.md
<64 hex>  DESIGN.md
<64 hex>  HISTORY.md
<64 hex>  tools/check_registration.py
<64 hex>  protocol/runtime_reference.py
<64 hex>  AVAILABILITY_DECLARATION.md

Signing key: RSA 4096, Theo Johann Howard
Key fingerprint = 991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7

The commit hash is timestamped via OpenTimestamps; the .ots receipt is
committed in a follow-up commit. The prereg-v30 tag never moves.
```

**The six hash lines are the output of C2, pasted — never retyped, never re-derived, never
reordered.** Two spaces between hash and path. Six lines, in the `FILES` order. The block's first
five lines are the v30 block's paths in the v30 order; only the values change.

```sh
# C2h — README's v30a block, and the Phase 0 sentence. TWO EXECUTING GATES.
#
# NAMED C2h, NOT C2g (corrected R96). §3.6 already has a C2g — the verification
# that re-reads the six out of the finished commit — and two different steps under
# one name in a ceremony is exactly the ambiguity this file exists to remove. The
# duplicate also restated §3.5.1 steps 3 and 3a, which already existed as prose;
# what was missing was never the instruction, it was an EXECUTING gate (§154.4).
#
# C2h-1  FILL THE BLOCK FROM v30a.hashes.txt. Never from tagmsg.txt, never from
#        the v30 block above it, never typed. The placeholder line between the
#        <<<V30A-HASHES ...>>> markers is REPLACED by the file's six lines.
python - <<'EOF'
import pathlib, re
r = pathlib.Path("README.md"); s = r.read_text(encoding="utf-8")
h = pathlib.Path("v30a.hashes.txt").read_text(encoding="utf-8").strip()
assert len(h.split("\n")) == 6, "v30a.hashes.txt must carry six lines"
s2 = re.sub(r"<<<V30A-HASHES.*?>>>", h, s, count=1, flags=re.S)
assert s2 != s, "C2g-1: the V30A-HASHES placeholder was not found"
r.write_text(s2, encoding="utf-8")
print("C2g-1 OK - six lines written from v30a.hashes.txt")
EOF

# C2h-2  RE-DERIVE THE PHASE 0 SENTENCE (§31). It is NOT carried forward and it
#        is NOT copied from the v30 README. Establish each clause from the record
#        at write time, then write the sentence the record supports:
#
#          (a) does a detector implementation exist?   -> search the tree
#          (b) has Phase 0 run?  §10's phase table lists FOUR items behind one
#              gate: fixture declaration reconstruction; prior-art verification;
#              cross-tool comparison per §9.2; licence check. Establish EACH.
#
#        KNOWN AT R95, and why this step exists: the v30 sentence "Phase 0 ...
#        has not run" is NO LONGER ACCURATE as written. Prior-art verification
#        was signed off at HISTORY.md H-34 (12 Aug 2026), and the declaration's
#        §A.11 records that a cross-tool comparison ran 14 Aug 2026 and does NOT
#        satisfy §9.2. Phase 0 is PARTLY run with one item unsatisfied. The
#        re-derived sentence must say which items are done and which are not.
#        DO NOT resolve this from this comment - it is dated. Re-derive.
#        The sentence must COVER four facts (§154.1). If the sources contradict
#        any of them, HALT rather than write it:
#          1. Phase 0 is PARTLY RUN.
#          2. Prior-art verification signed off — HISTORY.md H-34, 12 Aug 2026.
#          3. Cross-tool comparison RAN 14 Aug 2026 and does NOT satisfy §9.2.
#          4. §9.2 and the licence check are carried as PHASE 1 ENTRY obligations
#             under the author's recorded routing of 25 Aug 2026 — NOT open tag
#             blockers. Without the fourth a reader concludes the tag shipped
#             over an open gate. It did not.
#
# THIS GATE EXECUTES. It exits non-zero; it does not print and continue. §27.
if grep -q "has not run" README.md; then
  echo "C2h-2 FAILED — the Phase 0 sentence is still the v30 wording, un-re-derived. HALT."
  exit 1
fi
for probe in "partly run" "H-34" "9.2" "Phase 1 entry"; do
  grep -qi -- "$probe" README.md || {
    echo "C2h-2 FAILED — the re-derived sentence does not cover: $probe. HALT."; exit 1; }
done
echo "C2h-2 OK — Phase 0 sentence re-derived and covers all four facts"

# C2f — the message file carries exactly the operation's output
diff <(sed -n '/^[0-9a-f]\{64\}  /p' tagmsg.txt) v30a.hashes.txt && echo "tagmsg OK"
```

### 3.5.1 `README.md`'s v30a block — the ordering, stated so it is not circular

*(Until R67/§17.3 this read "filled from `v30a.hashes.txt` — and is staged and committed
**before** C2 runs". `v30a.hashes.txt` is C2's **output** (§3.4: "the only place any `prereg-v30a`
hash value is produced"), so as written the block had to be filled from a file that did not
yet exist. Corrected to the executable order below.)*

**The order, and it is not circular because `README.md` is NOT one of the six:**

1. `git add` the six and everything else in `COMMIT_PLAN.md` §4 **except `README.md`**.
2. **C2** — hashes **staged** content (`git show :<path>`, §3.4) —> `v30a.hashes.txt`.
3. Fill `README.md`'s v30a block from `v30a.hashes.txt`. Never retyped.
3a. **RE-DERIVE `README.md`'s Phase 0 sentence — do not carry it forward (R68/§31).**
   The README states, at the head: *"Phase 0 — a kill gate that can end the project
   (`PREREG.md` §10.1) — **has not run**."* That is a **factual claim about the state at
   the moment of tagging**, and blocker 1 is precisely the question of whether it is still
   true. Read the Phase 0 work-item table in §0 of this file and write the sentence against
   what it says **then**, not against what it said when the block was drafted. If Phase 0 has
   run, the sentence is false and the README ships a false statement about the registration's
   own gate. **This is the sentence the ceremony is most likely to falsify by executing.**
4. `git add README.md`.
5. `git commit` — so `README.md` IS in the commit the tag points at, which is what the old
   wording was reaching for.
6. Write `tagmsg.txt` from the same `v30a.hashes.txt`, then tag.

**Why step 4 cannot move a single one of the six.** The six hashes were read at step 2 from the
index entries for `$FILES`. `README.md` is not in `$FILES`, so staging it adds an index entry
that no hash in the block covers. **C2g** (§3.6) re-reads the six out of the finished commit and
must still match `v30a.hashes.txt`; that is the gate which would catch it if this reasoning were
wrong, and it is not waived here.

**`README.md` is not one of the six and is not self-referentially hashed** — it carries the block,
so hashing it would require its own hash to be inside itself. `PREREG.md` §11 item 3 puts the block
"in the tag message **and the README**": two loci, one source, and that source is `v30a.hashes.txt`.

## 3.6 Commit, then confirm the commit is what was hashed

```sh
git commit -m "Pre-registration v30a: §6.2 reference AUC, contamination-class locus, sliced CI variant, and criterion 3 — class C amendment (PREREG §0.2.1)"

# C2g — VERIFICATION ONLY. Its sole permitted outcome is byte-identity.
#        This is NOT a second source for the tag message and its output may never
#        be pasted anywhere. If it disagrees with v30a.hashes.txt, HALT.
for f in $FILES; do
  printf '%s  %s\n' "$(git show "HEAD:$f" | sha256sum | cut -d' ' -f1)" "$f"
done | diff - v30a.hashes.txt || { echo "C2g FAILED — the commit does not carry what was hashed. HALT."; exit 1; }
echo "C2g OK — the commit carries exactly what was hashed"

# The tree must be clean apart from the three known untracked paths. This ran as a
# bare `git status --porcelain` until R68, AFTER the diff above — so the block's exit
# status was git status's, always 0, and C2g's real verdict was discarded by the line
# following it. It is now an assertion, and it runs after the diff has already halted.
# C2g working-tree assertion — A DERIVATION, NOT A LIST (R113/NODE A).
#
# This was a hardcoded list of three paths and it went stale the moment LICENSE
# and tools/control_char_scan.py entered the tree — both RECORDED, neither in the
# list. A pinned expectation with no derivation is a carried-forward value
# (H-L24), and this is the second time that class has stopped a ceremony.
#
# Every untracked path must now be ONE of three things, each derived from a file
# that is itself under the gate:
#   (1) a ceremony artifact  — tagmsg.txt, v30a.hashes.txt, .claude/
#   (2) on D10's ephemeral list in tools/check_registration.py
#   (3) recorded in evidence/session/DEFERRED_ITEMS.md
# Anything else fails, and the failure names the path and all three tests.
#
# ` M ` or any staged-but-modified line still means a hashed file moved after
# staging. That remains a HALT and is checked separately below.
python - <<'C2G_EOF'
import json, re, subprocess, sys, pathlib
REPO = pathlib.Path(".")
un = [l[3:] for l in subprocess.run(["git","status","--porcelain"],capture_output=True,
      text=True,check=True).stdout.split("\n") if l.startswith("?? ")]
CEREMONY = {"tagmsg.txt", "v30a.hashes.txt", ".claude/"}
eph = re.findall(r'\(\s*"([^"]+)"\s*,\s*\n?\s*"', (REPO/"tools/check_registration.py")
                 .read_text(encoding="utf-8").split("_EPHEMERAL = (")[1].split("\n)")[0])
deferred = (REPO/"evidence/session/DEFERRED_ITEMS.md").read_text(encoding="utf-8")
bad = []
for p in un:
    base = p.rstrip("/").split("/")[-1]
    why = []
    if p in CEREMONY or base in {c.rstrip("/") for c in CEREMONY}: why.append("ceremony artifact")
    if any(tok in p or p.endswith(tok) for tok in eph): why.append("D10 ephemeral list")
    if base in deferred or p in deferred: why.append("recorded in DEFERRED_ITEMS.md")
    if why:
        print("C2g  accounted   %-34s (%s)" % (p, "; ".join(why)))
    else:
        bad.append(p)
        print("C2g  UNACCOUNTED %-34s not a ceremony artifact, not on D10's "
              "ephemeral list, not in DEFERRED_ITEMS.md" % p)
if bad:
    print("C2g FAILED — %d untracked path(s) accounted for by none of the three." % len(bad))
    sys.exit(1)
print("C2g OK — every untracked path is accounted for by derivation")
C2G_EOF
```

**No `--amend`.** Hashing from the index removes the reason the v30-era plan needed one. If an
amend becomes unavoidable for some other reason, **every step from C2a re-runs against the amended
commit**, because an amend changes `HEAD` and any value computed against the pre-amend `HEAD` is
exactly the carried-forward value the rule forbids.

---

# §4 — C1: SIGN, THEN VERIFY BEFORE ANY PUSH

## C1a `[AUTHOR]` — cut the signed tag

```sh
git tag -s prereg-v30a -F tagmsg.txt
```

Signing key **`B29CF0E847119AD7`**, already set as `user.signingkey` and matching the README
fingerprint tail `991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7`. `gpg.program` is already
configured to `C:\Program Files\GnuPG\bin\gpg.exe`; if it were not, the equivalent is
`git -c gpg.program="C:\Program Files\GnuPG\bin\gpg.exe" tag -s prereg-v30a -F tagmsg.txt`.

> **`[AUTHOR]` — THE PASSPHRASE PROMPT.** This command prompts for the key passphrase. **No agent
> types it, reads it, stores it, or observes it.** If the ceremony is being driven with an agent
> present, the agent stops at this line and the author runs it alone.

## C1b — VERIFY THE SIGNATURE. **BEFORE ANY PUSH.**

```sh
# C1b — GOOD SIGNATURE **AND THE RIGHT KEY**. Both, or halt.
#
# Until R68 this step was `git tag -v prereg-v30a` and a human reading gpg's prose
# for the fingerprint. `git tag -v` exits 0 for a good signature from ANY key the
# local keyring can verify — so the exit status attested "signed by a key", while
# the tag message asserts "signed by THIS key". Demonstrated at R68: a tag signed
# by a throwaway key, carrying a message that asserts the registration fingerprint,
# passed `git tag -v` with exit status 0.
#
# The expected fingerprint is NOT restated here. It is read from the signed object's
# own message, so the check is: *the object asserts fingerprint X; prove gpg agrees
# the signature over that object came from X.*
#
# Anchored on `--raw`'s machine-readable [GNUPG:] status lines, never on gpg's prose,
# which is localized and version-dependent. VALIDSIG's LAST field is the PRIMARY key
# fingerprint (verified against prereg-v30 this pass), so a future subkey signature
# still resolves to the registration key.
raw=$(git verify-tag --raw prereg-v30a 2>&1)
body=$(git cat-file tag prereg-v30a)

printf '%s\n' "$raw" | grep -q '^\[GNUPG:\] GOODSIG ' || {
  echo "C1b FAILED — not a good signature (expired, revoked, or unverifiable). HALT."; exit 1; }

asserted=$(printf '%s\n' "$body" | sed -n 's/^Key fingerprint = //p' | tr -d ' ' | tr 'a-f' 'A-F')
actual=$(printf '%s\n' "$raw" | awk '/^\[GNUPG:\] VALIDSIG /{print $NF}')

# Leg 3: the fingerprint the DECLARATION states (§D.4). The declaration is in the six
# and is OTS-covered, so this leg is timestamped rather than merely asserted. Legs 1 and 2
# alone only prove the signer was internally consistent with themselves.
declared=$(sed -n '/^### D\.4 /,/^## /p' AVAILABILITY_DECLARATION.md \
           | grep -oE '[0-9A-F]{4}( +[0-9A-F]{4})+' | head -1 | tr -d ' ')
#   NOTE ` +` not ` `: the canonical gpg rendering puts a DOUBLE space mid-fingerprint
#   ("AF7D  6939"). A single-space pattern truncates at that gap and yields a 20-hex
#   prefix, which would fail C1b every run for a reason that has nothing to do with the key.

[ -n "$asserted" ] || { echo "C1b FAILED — the tag message states no fingerprint. HALT."; exit 1; }
[ -n "$declared" ] || { echo "C1b FAILED — §D.4 states no fingerprint. HALT."; exit 1; }
[ "$asserted" = "$actual" ] || {
  echo "C1b FAILED — signed by $actual, but the message asserts $asserted. HALT."; exit 1; }
[ "$declared" = "$actual" ] || {
  echo "C1b FAILED — signed by $actual, but §D.4 declares $declared. HALT."; exit 1; }
echo "C1b OK — good signature; signing key, tag message and §D.4 all read $actual"

# The public key ships in the tree, so a verifier needs no keyserver:
#   gpg --import prereg-signing-key.asc
# NOTE THE BOUNDARY. All three legs are INTERNAL to this repository. They prove the tag
# was signed by the key this registration names; they do NOT prove who holds that key.
# That binding rests on the key's publication outside this repository (§12 disclosure).
```

**GATE — the output must contain, from gpg:**

```
gpg: Good signature from "Theo Johann Howard <ttbear2000@gmail.com>"
```

together with the primary key fingerprint `991F 5331 C584 CE5E AF7D 6939 B29C F0E8 4711 9AD7`.
`BAD signature`, `Can't check signature`, `No public key`, or a fingerprint that is not that one:
**HALT. Do not push.** A tag that has not been pushed can be deleted and re-cut
(`git tag -d prereg-v30a`); a tag that has been pushed and then moved is exactly the thing the
registration's "this tag never moves" property exists to make impossible.

```sh
# C1c — read the six hashes back out of the SIGNED OBJECT, not out of the file that fed it
git cat-file tag prereg-v30a | grep -E '^[0-9a-f]{64}  ' | diff - v30a.hashes.txt \
  && echo "C1c OK — the signed object carries the six"
```

The diff is against `v30a.hashes.txt`, **not** against `tagmsg.txt`. `tagmsg.txt` is the file that
was fed in and cannot detect its own mistranscription. **Any difference: HALT, delete the tag,
re-cut it.**

**Only after C1b and C1c are green does anything leave this machine.**

---

# §5 — C3: PUSH THE COMMIT AND THE TAG, THEN VERIFY REACHABILITY

`PREREG.md` §11 item 5 and §0.2.1 line 97: **the repository is publicly reachable at the moment of
lock.** The commit and the tag both have to be there — a tag object whose target commit is not on
the remote is not reachable, and a commit without its tag is not the lock.

```sh
# C3a — the commit
git push origin main

# C3b — the tag, as a separate, explicit push. Never `--tags`, never `--follow-tags`:
#        this ceremony pushes ONE named tag and nothing else.
git push origin prereg-v30a
```

```sh
# C3c — VERIFY the tag is visible on the remote, read back from the remote itself
git ls-remote --tags origin
# EXPECT two lines for the new tag — the annotated tag object and its ^{} peel:
#   <tagobj-sha>  refs/tags/prereg-v30a
#   <commit-sha>  refs/tags/prereg-v30a^{}
# and the peeled sha must equal:
git rev-parse prereg-v30a^{commit}

# C3d — VERIFY the commit is on the remote branch
git ls-remote origin refs/heads/main
git rev-parse HEAD          # the two must match
```

**HALT if `refs/tags/prereg-v30a` is absent from `ls-remote`, or if the peeled sha does not equal
the local `prereg-v30a^{commit}`, or if the remote `main` does not equal local `HEAD`.** Until
C3c and C3d are green the amendment is not locked, and §10.0 step 4 stays closed.

---

# §6 — C4: OPENTIMESTAMPS. **AFTER THE TAG AND AFTER THE PUSH.**

The stamp comes last for the reason `README.md` lines 18–20 give: "a commit cannot contain the
receipt for its own hash." The v30 precedent is two commits, `5842857` then `0ee26c4`.

## C4a — record the commit the tag points at

```sh
git rev-parse prereg-v30a^{commit} > amendment-commit-v30a.txt
```

**Do not overwrite `registration-commit.txt`** — that is v30's record and it is tracked.

## C4b `[AUTHOR]` — stamp, via the web precedent

**The `ots` CLI is broken in this environment.** The entry point at
`C:\Users\ttbea\AppData\Local\Programs\Python\Python312\Scripts\ots` crashes at import:
`python -c "import bitcoin.rpc"` exits 1 with a `ctypes`
`TypeError: argument of type 'NoneType' is not iterable` — a python-bitcoinlib /
Windows `find_library(ssl)` failure. Re-recorded from the prior pass and **not re-tested here**
(execute-nothing).

**So the stamp is taken the way v30's was: through the OpenTimestamps web UI.** Upload
`amendment-commit-v30a.txt`, download the returned `amendment-commit-v30a.txt.ots`, and place it
beside the `.txt` at the repository root.

**`[AUTHOR]`-only.** This step leaves the machine and touches a third-party service; it is the
author's, exactly as the v30 stamp was.

## C4c — commit the pair in a FOLLOW-UP commit (mirrors `5842857`)

```sh
git add amendment-commit-v30a.txt amendment-commit-v30a.txt.ots
git commit -m "OpenTimestamps receipt for v30a amendment commit"
git push origin main
```

**This is a separate commit from the ceremony commit, and it is made after the tag exists.** The
tag does not move to cover it, and it must not: the tag points at the commit whose hash the
receipt attests.

## C4d `[AUTHOR]` — the Bitcoin attestation upgrade, a SEPARATE LATER STEP

Hours to days after C4b, the calendar servers publish the Bitcoin attestation. This mirrors
`0ee26c4`, which took v30's `.ots` from 584 to 2,587 bytes at blocks **961654** and **961656**.

The CLI upgrade path is broken for the same import reason, so the recorded workaround is the
pure-Python upgrader used for v30:

```
C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\ots_upgrade.py
```

*(Verified present this pass: 3,764 bytes, mtime 2026-08-09 — the day of the v30 upgrade. It sits
in a session scratchpad, which is transient; if it has been swept, the web UI's own upgrade path
is the fallback.)*

```sh
# upgrade, verify, then a THIRD commit
python "…\scratchpad\ots_upgrade.py" amendment-commit-v30a.txt.ots
git add amendment-commit-v30a.txt.ots
git commit -m "OpenTimestamps receipt upgraded: Bitcoin attestations at blocks <N>, <M>"
git push origin main
```

The block heights go into `DEVIATIONS.md` D-001's last `«CEREMONY-FILL»` at this point, and not
before — they are not knowable until the upgrade returns them.

**Hard ordering.** §0.2.1 line 95 requires the amendment "committed and externally timestamped
before the affected detector is implemented or evaluated"; §10.0 step 3 requires it before step 4.
So **C4a–C4c precede any Phase 1 freeze and any detector work. C4d may trail.**

---

# §7 — EVERY HALT CONDITION, IN ONE PLACE, IN ORDER

| Step | Condition | Action |
|---|---|---|
| §0 | Phase 0 kill-gate sign-off not on the record | **do not start** |
| §0 | any of B1–B6 unresolved | do not start |
| **C5** | `git remote -v` is not exactly `https://github.com/TheoJHoward/DataLeakageAuditor.git` on both lines | **HALT — wrong repository** |
| C5 | `prereg-v30a` already exists in `git tag -l` | halt; find out why |
| stage | staged set contains `.claude/`, `tagmsg.txt`, `v30a.hashes.txt`, or any unlisted path | unstage and re-verify |
| **C2a** | a member of the six is not in the index | **ERROR — report and halt. Never skip the file.** |
| **C2b** | a member of the six is modified but unstaged | **ERROR — report and halt. Never skip, never silently `git add`.** |
| C2c | any `DIFFER` | halt |
| C2d | `sha256sum -c MANIFEST.sha256` reports any FAILED | halt; repair the manifest |
| C2e | C2 and C2e outputs differ | halt; `* -text` or C2c is false |
| C2 | `tools/check_registration.py` or `protocol/runtime_reference.py` differs from its v30 value | **a finding, not a typo** — halt and record |
| C2f | `tagmsg.txt`'s hash block differs from `v30a.hashes.txt` | halt; re-paste, never retype |
| C2g | the committed blobs do not reproduce `v30a.hashes.txt` | halt |
| **C1b** | anything other than `Good signature` with the expected fingerprint | **HALT. Do not push.** Delete and re-cut. |
| C1c | the signed object's hash lines ≠ `v30a.hashes.txt` | halt; delete the tag and re-cut before any push |
| **C3c/C3d** | tag absent from `ls-remote`, peel mismatch, or remote `main` ≠ local `HEAD` | halt; the amendment is not locked |
| C4b | the stamp cannot be taken | halt; the amendment is not externally timestamped and §10.0 step 4 stays closed |

---

# §8 — THE SEQUENCE, AS ONE LIST

1. **§0** — Phase 0 kill-gate sign-off on the record; B1–B6 cleared. `[AUTHOR]`
2. **C5** — `git remote -v` identity check. **First command.**
3. Stage per `COMMIT_PLAN.md` §4; fill `README.md`'s v30a block after C2 and stage it before the commit.
4. **C2a / C2b / C2c / C2d** — index presence, unstaged check, byte-compare, manifest.
5. **C2** — the single hashing operation → `v30a.hashes.txt`.
6. **C2e / C2f** — cross-check; write `tagmsg.txt` from the operation's output.
7. `git commit`, then **C2g** — the commit carries what was hashed.
8. **C1a `[AUTHOR]`** — `git tag -s prereg-v30a -F tagmsg.txt`.
9. **C1b / C1c** — verify the signature and the signed object. **Before any push.**
10. **C3a / C3b** — push commit, then tag.
11. **C3c / C3d** — verify reachability on the remote.
12. **C4a**, **C4b `[AUTHOR]`**, **C4c** — record the commit, stamp, follow-up commit, push.
13. Delete `v30a.hashes.txt`.
14. **C4d `[AUTHOR]`, later** — upgrade the receipt, third commit, push.
