# §21.2 — EVERY NUMBERED CHECK, CLASSIFIED

**Rule applied (§21.3 / §23.3):** EXECUTABLE = **exits non-zero, or halts a script, on failure**.
ADVISORY-PRINT = emits output for a human to compare; **exit status is 0 whether it passed or
failed**. NARRATIVE = prose only, no command.

**Classification was made from each check's actual command body, not from its heading.** Several
checks read as assertions and are not: the discriminator is whether the *last* command's exit
status carries the verdict.

---

## `evidence/ceremony/CEREMONY_COMMANDS.md`

| id | anchor | class | items a human must compare | note |
|---|---|---|---|---|
| **C5** | §2 l.111 | **ADVISORY-PRINT** | **2** (fetch + push remote lines) | bare `git remote -v` |
| **C2a** | §3.3 l.213 | **ADVISORY-PRINT** | **7** (6 IN-INDEX lines + the FAILED line) | ends `test "$missing" -eq 0 \|\| { echo "C2a FAILED — halt"; }` — the `\|\|` branch **echoes and succeeds**, so the block exits **0 on failure** |
| **C2b** | §3.3 l.226 | **ADVISORY-PRINT** | **6** (expect empty output over 6 paths) | bare `git diff --name-only -- $FILES` |
| **C2c** | §3.3 l.250 | **EXECUTABLE** | — | ends `test "$bad" -eq 0 && echo …`; on failure `test` fails, `&&` short-circuits, block exits **non-zero** |
| **C2d** | §3.3 l.270 | **EXECUTABLE** | — | `sha256sum -c` exits non-zero on any mismatch |
| **C2d-0** | §3.3 l.288 | **EXECUTABLE** | — | explicit `exit 1` |
| **C2d-2** | §3.3 l.298 | **ADVISORY-PRINT** | **3** (declaration / pointer / manifest hashes) | `[ … ] && echo "AGREE" \|\| echo "DISAGREE — HALT"` — the `\|\|` makes it exit **0 either way** |
| **C2** | §3.4 l.318 | *(operation, not a check)* | — | produces `v30a.hashes.txt`; asserts nothing |
| **C2e** | §3.4 l.330 | **EXECUTABLE** | — | `diff … && echo` — `diff` exits non-zero |
| **C2f** | §3.5 l.376 | **EXECUTABLE** | — | `diff … && echo` |
| **C2g(i)** | §3.6 l.412 | **EXECUTABLE** | — | `… \| diff - v30a.hashes.txt && echo` |
| **C2g(ii)** | §3.6 l.416 | **ADVISORY-PRINT** | **3** (`.claude/`, `tagmsg.txt`, `v30a.hashes.txt`) | trailing `git status --porcelain`; **also sets the block's exit to 0**, masking C2g(i) |
| **C1a** | §4 l.433 | *(operation, `[AUTHOR]`)* | — | `git tag -s` |
| **C1b(i)** | §4 l.443 | **EXECUTABLE** | — | `git tag -v` exits non-zero on a bad/absent signature |
| **C1b(ii)** | §4 l.446 | **ADVISORY-PRINT** | **2** (the "Good signature from" line + the fingerprint) | **see §21.6 — this is the important one** |
| **C1c** | §4 l.467 | **EXECUTABLE** | — | `git cat-file tag … \| diff - v30a.hashes.txt && echo` |
| **C3a / C3b** | §5 ll.487, 490 | *(operations)* | — | pushes |
| **C3c** | §5 l.496 | **ADVISORY-PRINT** | **3** (2 ls-remote lines + 1 rev-parse sha) | two bare prints, "the peeled sha must equal" |
| **C3d** | §5 l.504 | **ADVISORY-PRINT** | **2** | "# the two must match" |
| **C4a / C4c / C4d** | §6 | *(operations)* | — | rev-parse, commit, upgrade |
| **C4b** | §6 | **NARRATIVE** | — | `[AUTHOR]` web stamp, "(execute-nothing)" |

## `evidence/ceremony/COMMIT_PLAN.md`

| id | anchor | class | items | note |
|---|---|---|---|---|
| **V1a** | §4.1 l.276 | **ADVISORY-PRINT** | **0 expected** | `echo` inside a loop; exit 0 — **written by me this round** |
| **V1b** | §4.1 l.287 | **ADVISORY-PRINT** | **0 expected** | `echo` inside a `while` in a **pipeline subshell**; exit 0 — mine |
| **V1c** | §4.1 l.298 | **ADVISORY-PRINT** | **0 expected** | `\|\| { echo …; continue; }`; exit 0 — mine |
| **V2** | §4.1 l.331 | **ADVISORY-PRINT** | **2** (`.claude/`, `tagmsg.txt`) | bare `git status --porcelain` |
| **V3** | §4.1 l.337 | **EXECUTABLE** | — | `sha256sum -c` |
| **V4** | §4.1 l.341 | **ADVISORY-PRINT** | **3** | `[ … ] && echo "V4 OK" \|\| echo "V4 FAILED"` — exit 0 either way; mine |
| **V5** | §4.1 l.353 | **ADVISORY-PRINT** | **0 expected** | `grep -n '«CEREMONY-FILL'` — **exit status is INVERTED**: 1 on success, 0 on failure |
| **V6** | §4.1 l.356 | **ADVISORY-PRINT** | **1** | `grep -c '^-[^-]'` — prints a number; also inverted |
| **V7** | §4.1 l.359 | **EXECUTABLE** | — | `pytest` + `check_registration.py --stage prereg` |

## §21.7 — C2.5

| id | anchor | class | items | note |
|---|---|---|---|---|
| **C2.5** | `X4_REGENERATION_REQUIREMENTS.md` | **NARRATIVE** | — | states SC-4(k2)'s conditions in prose; **has no command at all**. Same class, one step further along: not a print that nobody reads, a check that was never written. |

---

## COUNT

**ADVISORY-PRINT: 15** — C5, C2a, C2b, C2d-2, C2g(ii), C1b(ii), C3c, C3d, V1a, V1b, V1c, V2, V4, V5, V6.
**EXECUTABLE: 9.** **NARRATIVE: 2** (C4b, C2.5). **Operations, not checks: 7.**

# §21.4 — THE VALVE TRIPS. 15 > 6. NO CONVERSIONS PERFORMED.

---

## WHAT THE TABLE SHOWS THAT THE COUNT DOES NOT

**1. The executable/advisory split is accidental, not designed.** C2a and C2c sit in the same
block, do the same kind of job, and differ only in shell punctuation: C2c ends `test … && echo`,
which propagates failure; C2a ends `test … || { echo …; }`, which swallows it. **Nothing in either
heading marks the difference**, and C2a's own text says "ERROR: REPORT AND HALT" while exiting 0.

**2. Two checks have INVERTED exit status.** V5 and V6 use bare `grep`, which exits **1 when it
finds nothing**. Their success condition returns non-zero and their failure condition returns zero.
Wired into any `set -e` runner they would halt on success and pass on failure.

**3. A trailing print masks a real check.** C2g(i) is a genuine `diff`; C2g(ii) is `git status`
appended after it. The block's exit status is `git status`'s, which is always 0 — **so the one
executable assertion in C2g is discarded by the line after it.**

**4. I made this worse before I found it.** V1a, V1b, V1c and V4 are mine, written this round to
fix V1-the-print. **All four are prints.** I replaced one advisory check with four. That is the
evidence for §21.1's claim that this is a class: the shape reproduces itself in the hands of
someone actively trying to remove it.

**5. Where the prints cluster is where the ceremony is least recoverable.** C3c and C3d verify
remote state **after the push** — the one point past which nothing can be re-cut.

---

## §21.6 — WHAT THE TAG MESSAGE AND README ACTUALLY SAY

**Neither asserts that a set of gates passed. No rewording is required on that ground.**

**The tag message** (v30a format block, §3.5; identical in shape to the executed v30 message, read
from `git cat-file tag prereg-v30`) makes exactly four claims:

> "SHA-256 of the registration documents and tooling **as committed**:"
> "Signing key: RSA 4096, Theo Johann Howard / Key fingerprint = 991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7"
> "The commit hash is timestamped via OpenTimestamps; the .ots receipt is committed in a follow-up commit."
> "The prereg-v30 tag never moves."

"**as committed**" is a provenance claim and it **is** backed executably — C2 reads staged content
and **C2g(i)** diffs the six back out of the finished commit. That one is sound.

**The README** says, under `## Verify`:

> "python -m pytest tests/registration"
> "python tools/check_registration.py --stage prereg"

That is an **instruction to the reader**, not an assertion that they passed, and both are
EXECUTABLE. Also sound.

### But §21.6's failure shape IS present — in the claim I did not expect

**The tag message asserts a KEY IDENTITY that the ceremony's own verification does not
mechanically establish.** `git tag -v` (C1b(i)) exits non-zero for a bad or unverifiable
signature — but it exits **zero for a good signature from any key git can verify**. The binding of
the signature to fingerprint `991F 5331 … 4711 9AD7` is checked **only by a human reading gpg's
output** (C1b(ii), ADVISORY-PRINT, 2 items).

So the signed object asserts *"signed by this key"*, and the step that is supposed to confirm it
confirms *"signed by a key"*. **Under §21.6 that assertion is made true by conversion** — trivially,
`git tag -v prereg-v30a 2>&1 | grep -q 'B29CF0E847119AD7'` or matching the fingerprint line — **and
the conversion is withheld because §21.4's valve tripped.** It is named here as the single
highest-value conversion in the table.

### One further live claim, flagged rather than buried

README l.12–13: *"Phase 0 — a kill gate that can end the project (`PREREG.md` §10.1) — **has not
run.**"* That is a **factual claim, currently true**, and blocker 1 is exactly the question of
whether it stays true at v30a. When the v30a README block is written, this sentence must be
re-derived against the state at that moment, not carried forward. It is not a gate assertion, so
§21.6 does not require action now — but it is the sentence most likely to be silently falsified by
the ceremony itself.

---

## §22 — THE FIVE UNVERIFIED SITES. **ALL FIVE AGREE. A3 CLOSES.**

| site | claim | enumeration | verdict |
|---|---|---|---|
| `PREREG.md:449` | "See §10.1 **criterion 3** and §10.2 **criterion 2**" | **not a count** — a cross-reference to two criteria; §10.1 has 5, §10.2 has ≥3 | **AGREE** (misclassified by the sweep) |
| `PREREG.md:521` | "under the **two** `ties` branches" | `ties` has exactly 2 branches (R1: strict counts + the 49 exactly-equal events) | **AGREE** |
| `PREREG.md:1038` | "The **two** gates close a gaming pair" | finding-rate gate + completion gate, both enumerated in the bullets above | **AGREE** |
| `HISTORY.md:219` | "**Three** instances is a structural defect" | `DESIGN.md` §9's stale range + **two** prior instances recorded as Z2 = 3 | **AGREE** |
| `AVAILABILITY_DECLARATION.md:3071` | "**two** frozen gate CLASSES" | OUT OF JURISDICTION + UNSCORED, both named on the same line | **AGREE** |

**§22.2 and §22.3 do not fire.** Nothing is wrong, so no hashed file carries a false statement and
no `PREREG.md` disclosure line is needed.

**`HISTORY.md:219` is worth more than its verdict.** Lesson 13 already draws the distinction §21
and A3 both need, and it is a constraint on this work: a numeral that *points at* an enumeration is
a fragile reference, but **a numeral that *forbids* growth is a closure constraint, and deriving it
away deletes the rule** — *"a reader who strikes the numeral in the name of this lesson has not
de-fragilised a cross-reference, they have deleted the constraint and admitted a fourth class."*
Any conversion pass authorised after this one must apply that test before touching a count.

---

## H-L19 — FILED

**`HISTORY.md` lesson 19**, in the numbered review-lesson series after 18. It cites lesson 13 rather
than repeating it, carries lesson 13's closure-constraint exception forward explicitly, and uses
**this round's 245-vs-249 as its evidence** (§21.5): the figure was carried forward without
re-derivation *by the agent rewriting the staging plan to fix that exact defect*, alongside the
+64 exemption drift and the +169 citations. It closes on the §21 corollary: **a check whose failure
mode is "the human did not notice" is not a check.**

*Recording it tripped the detector* — lesson 19 quotes all five historical values in a hash-set
context — which required a D5 exemption (`HISTORY.md:225`, pinned on `it FORKS`) stating that the
values are the defect being described, not an assertion of the count. The failure also broke
`test_prereg_stage_on_real_repo_exits_zero`, since that test asserts the prereg stage exits 0.
Both green again.
