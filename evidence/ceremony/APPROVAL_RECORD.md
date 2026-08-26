# APPROVAL RECORD — prereg-v30a

**Facts and dates only. The read is not characterised.**

---

## §140 — THE APPROVAL

On **25 August 2026** the author read the five load-bearing clauses — **SC-3**, **SC-3-C2op** and
**SC-3-C2ret**, **SC-12**, **SC-13a**, **SC-4** — raised one question on SC-3's scope, received the
answer recorded at §138 below, and **approved the R87 pair**:

| artifact | sha256 |
|---|---|
| `PREREG_v30a_APPROVAL.diff` | `c5d89db16f2c1fed0c500b5729bfcd751036705230f1098376bcf272f680b0c9` |
| `SCHEMA_SET_FINAL.md` | `32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc` |
| `PREREG.md` (base) | blob `75bd93dec4365aec8138bdded4817406b8f5ced5` |

**No §12 disclosure is owed for the approval basis.**

### THE APPLICATION, AND THE CHAIN IT RESOLVES (added R96/§152.2)

**Applied 25 August 2026.** The record carried the base and the diff but not the result until now;
the chain is stated here so it can be checked without reconstructing it.

| | |
|---|---|
| base | blob **`75bd93dec4365aec8138bdded4817406b8f5ced5`** — `prereg-v30:PREREG.md`, 1,099 lines |
| \+ approved diff | sha256 **`c5d89db16f2c1fed0c500b5729bfcd751036705230f1098376bcf272f680b0c9`** |
| → result | blob **`a90896785da528c8ce4ffd1aa839d1573d5a71ec`**, sha256 `0c8da19f237cd243…`, **2,075 lines**, 0 CRLF |

**Verified from the base and the diff alone (R96).** The diff's hunks were replayed against the
tagged base, every context and removal line asserted against the base as it went, and the result
hashed as a git blob: **`a90896785da528c8…`, equal to `PREREG.md` on disk.**

**`SCHEMA_SET_FINAL.md` is deliberately not consulted for this check.** It has moved since
application — it gained the §146.2 and §148.1 frames — so it is no longer the right instrument for
the question *"did this base plus this diff produce this file"*. The base and the diff are both
frozen; they are what the chain is made of.

**Equality with `prereg-v30:PREREG.md` would now mean the application was lost.** The inequality is
the amendment.

**On earlier drafts (§140.2).** This is the **first and only** record of the approval. A corpus-wide
search at R93 found no earlier draft of it in the repository — nothing describing the read as
"offered and declined" was ever written to disk, so there was nothing to strike. Recorded here
because "struck" and "never written" are different states and the record should say which.

---

## §138 — THE QUESTION, AND ITS ANSWER

**Q** *(author, 25 August 2026, on SC-3)* — does the user supply the ground-truth map, or does the
tool produce it?

**A** — **Neither.** The R9 ground-truth map is an **acceptance-test artifact over the declared
fixture** (ZC 2025-01, 2025-08), used to score the auditor during validation. **It is not an input to
the released tool, and no user of the tool supplies or receives one.** What a user supplies is the
**availability declaration** — `a(j,c)` per cell and `d(i)` per output row — plus the **feature
callable under test**.

### §138.2 — the answer VERIFIED against the text before recording

Checked against `SCHEMA_SET_FINAL.md` and `AVAILABILITY_DECLARATION.md`, not taken on assertion.
**The answer holds, and one clause states it in terms.**

| what was checked | what the text says |
|---|---|
| **The map is an artifact of the harness, not a tool input** | **SC-7(c), ssf l.754–757, in terms:** *"The map is an artifact of the harness, not an input to the tool."* And *"A run that received the key has not produced a gate result, whatever it reports."* |
| **A detector never receives it** | **SC-7(b), ssf l.750–752:** a detector never receives *"the paired side or any artifact derived from it … **the declared ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it."* |
| **What a detector DOES receive** | **SC-7(a), ssf l.746–748:** *"AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME: the pipeline for that side, and the availability declaration's declared elements (§2.3, §2.4, §2.9). **Nothing else.**"* |
| **The map's scope is the fixture** | **SC-3(a), ssf l.308–309:** the map is *"declared in the **fixture's** availability declaration"*, and SC-3's own heading scores *"Runtime findings on every **fixture side** … against the **fixture's** DECLARED GROUND-TRUTH MAP"*. |
| **§6.2 is an acceptance test, not a user surface** | `PREREG.md` **§6.2 is headed "Acceptance fixture"**; its criteria are evaluated *"on the frozen default configuration, under the reconstructed declaration"* against `fixture_contaminated` / `fixture_corrected`, and the fixture's declaration is *"**reconstructed, not chosen**"*. |
| **Nothing in v30 makes it user-facing** | **`PREREG.md` at `prereg-v30` contains ZERO occurrences of "ground-truth map".** The term enters only with this amendment. |
| **The fixture is ZC 2025-01 / 2025-08** | `AVAILABILITY_DECLARATION.md` throughout, e.g. the ZC 2025-01 fixture frame at 338,159 lattice rows. |
| **What the user supplies** | `PREREG.md` l.182 `d(i)` — decision time for output row *i*; l.192–193 the `a(j,c) ≤ d(i)` availability rule; l.209 `availability_fn` — *"escape hatch: **user callable** returning `a(j, c)`"*; l.318 L2a's detector input — *"callable + label column"*. |
| **Is the map ever named an input?** | **No occurrence anywhere** in `SCHEMA_SET_FINAL.md` or `AVAILABILITY_DECLARATION.md` of the map as something a user supplies or receives. |

**One point sharper than the answer as put.** *"The map ships; the fixture does not"* (§AC item 5,
ssf l.1720) could be misread as the map being distributed to users. It is not about users: the map is
**committed with the registration and publicly reachable at the tag** so a third party can inspect the
scoring key, while the acceptance fixture — 64 stored-prediction parquets per side — stays outside the
repository. Publication for inspection, not an input to anything.

**No text contradicts the answer. No HALT.**

---

## LINE REFERENCES IN THE CEREMONY RECORD — WHICH REGISTRATION VERSION THEY MEAN (R95/§146.2)

**Unqualified `PREREG.md` line numbers in records predating 25 August 2026 are v30 line numbers.**
A line reference written before the v30a amendment was applied refers to the registration version
current at that record's date, and is **correct as history**. The v30a amendment inserted 981 lines
after `PREREG.md` line 99, so **every v30 line number above 99 differs from its v30a position** —
`git show prereg-v30:PREREG.md` recovers the registered v30 text byte-exact and is where such a
reference resolves.

**They are deliberately NOT renumbered.** Renumbering a dated record falsifies what was cited when,
which is the one thing the record exists to preserve. Where this file quotes registered text, it
quotes it verbatim beside the line number, so a reader can verify the quotation against the tag
without needing the number to resolve in the current file.

---

## PROVENANCE OF THIS RECORD

Every quotation above was read from the file at R93 and cited by path and line. Line numbers into
`SCHEMA_SET_FINAL.md` are as of sha256 `32358f6d…`; line numbers into `PREREG.md` are as of the
**unapplied** base, blob `75bd93dec436`, recoverable byte-exact with
`git show prereg-v30:PREREG.md`.
