# What attests what — the integrity posture, stated rather than implied

Nothing here is a `PREREG.md` §6.2 result and no figure here belongs beside the
Phase 1 acceptance figures.

**Why this file exists.** R243 §3 asked for the two integrity mechanisms to be
recorded as *"disjoint and jointly cover"*. Measured, the first half holds and
the second does not, and the false half was written into
`tools/manifest_verify.py`'s own docstring before the measurement caught it —
the docstring-diverges-from-behaviour class (D-V30A-43), authored as a totality
claim nobody had checked.

**The correction is not to build coverage until the claim becomes true.** The two
mechanisms are partial by design and never claimed otherwise; the error was
implying they were exhaustive. What follows is the posture as it is.

---

## The two mechanisms, each with its actual population and purpose

| mechanism | population | what it attests | who checks it |
|---|---|---|---|
| **the manifest** | `evidence/` plus six `../` lines — **826 files** | a sha256 per file: this file's *content* is what it was | coverage by the gate (`manifest_coverage`), content by `tools/manifest_verify.py` |
| **the frozen comparison** | **2 files** — `tools/check_registration.py`, `protocol/runtime_reference.py` | the current instrument produces the same **verdicts** as the tagged one, or the difference is ruled and counted | the gate (`frozen_instrument_delta`), ceiling of 4 ruled differences, currently 2 |

**Neither claims totality and neither was ever meant to.** The manifest exists so
the evidence tree cannot change under a reader without saying so. The frozen
comparison exists so the instrument that certifies cannot drift from the one the
tag attests. Neither is a repository-wide integrity scheme.

**They are disjoint: 0 files are in both.** `check_registration.py` is
deliberately not in the manifest — its integrity is the verdict comparison, not a
hash. That is by design and is recorded here so a later reader meets the reason
rather than an apparent omission.

**BYTE-FROZEN AND VERDICT-FROZEN ARE DIFFERENT THINGS**, and conflating them is
what made R243's instruction destructive-if-literal:

    byte-identical to the tag     PREREG.md, protocol/runtime_reference.py —
                                  never changed since the freeze
    verdict-frozen, ruled         tools/check_registration.py — CHANGED, the
                                  changes ruled and counted. 141,431 bytes at
                                  the tag against 180,767 before R242.

*"Revert `check_registration.py` to byte-identical with the tag"* would have
reverted away both ruled repairs and every round since.

---

## The remainder — 132 tracked files, and what actually covers them

Over **956** tracked files: 826 manifest-attested, 2 frozen-compared, **0 in
both**, **132 in neither**.

| in neither | count |
|---|---|
| `tests/` | 88 |
| `src/` | 16 |
| `tools/` (other than the frozen checker) | 9 |
| root documents — `DEVIATIONS.md`, `DESIGN.md`, `AVAILABILITY_MODES.md`, `.gitattributes`, `.gitignore` | 5 |
| remainder | 14 |

**What covers them, stated as a fact rather than an alarm: git history, and
Phase 2 history is unsigned.** `git log --format=%G?` reports `N` on every Phase
2 commit. The signed `prereg-v30a` tag attests commit `b5a05c0` — the
registration — and not the current tree.

So for those 132 files, git's content addressing detects **corruption** and does
not attest **authorship or intent**. Nothing about that is new this round; it is
simply what was never written down.

**This is not a defect being disclosed.** A development phase whose registration
is signed and whose evidence tree is hashed is a coherent posture. What was
wrong was a sentence claiming more.

---

## The open question, with its cost — recorded, not acted on

**Whether to make integrity total is the author's decision, and signing is
`PREREG.md` §10-reserved.** R244 §1(c) rules it out of this round explicitly.
Recorded so the decision is available rather than rediscovered:

**Option A — sign the Phase 2 commits.** Cost: a signing key in the working
environment, a per-commit step, and a verification step in certification. Buys
authorship attestation for every tracked file at once, including the 132.
**Author-reserved; not available to the executing layer.**

**Option B — extend the manifest to `src/` and `tools/`.** Cost: every source
edit needs its hash restated, which is the failure mode R241/R243 already
produced twice on a 826-line manifest maintained by hand. Buys content
attestation without authorship. **Would likely need Option C first.**

**Option C — a manifest regeneration tool.** Cost: one instrument, and a rule
about when it runs. It makes a forgotten hash impossible rather than caught —
`manifest_verify.py` catches, a regenerator prevents. R243 recorded it as a
candidate; R244 leaves it a candidate. It would not belong inside the frozen
instrument.

**What this round did instead:** stated the posture. The claim was wrong, the
posture is what it is, and accuracy is the repair.
