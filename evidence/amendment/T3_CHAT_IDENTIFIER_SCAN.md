# T3 — CHAT-ONLY IDENTIFIER SCAN AND REPLACEMENT LIST

**Item T3.** Two-part deliverable:
1. **Sanitization confirmation** for the ledger entry drafted at T1 and the timing entry drafted at T2 — no chat-only identifier is present in either draft.
2. **Scan and replacement list** for the rest of the drafted normative text that lands in `PREREG.md` at ceremony time: the K2 §8 amendments block, the SC-N clauses of `SCHEMA_SET_FINAL.md` Part 1 that become PREREG.md insertion text, and the applied hunks of `PREREG_v30a_DIFF.md`. **Nothing here is applied.** The list is designed so a subsequent edit pass can execute the replacements deterministically with match-count asserts, and so an auditor can re-run the scan and compare.

---

## 1. THE RESOLVABILITY POLICY THAT DECIDES EACH CASE

An identifier is **resolvable** iff a reader, holding only the registered files (`PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md`, `HISTORY.md`, `DEVIATIONS.md`, `PRACTICES.md` after S7 lands, `PRIOR_ART_VERIFICATION.md`, `evidence/MANIFEST.sha256`, `tools/check_registration.py`, `protocol/runtime_reference.py`), can find where that identifier is defined. It is **chat-only** otherwise. The distinction turns on the file, not on the character shape of the identifier:

| Identifier class | Where defined | Resolvable? |
|---|---|---|
| `SC-1` … `SC-14` (schema clause tags) | in `PREREG.md` once the schema set applies (S7 + X2 land the SC-N insertion texts) | **RESOLVABLE** |
| `R1` … `R13` (working resolutions) | `AVAILABILITY_DECLARATION.md` §D tail — verbatim | **RESOLVABLE** |
| `R14` … `R17` (delta-issued working resolutions) | not in the declaration tail; delta ledger only | **CHAT-ONLY** |
| `R20` … `R37+` (delta ordinals) | planning-chat only | **CHAT-ONLY** |
| `H-L1` … `H-L13` (review-lesson series) | `HISTORY.md` §9 | **RESOLVABLE** |
| `H-1` … `H-34` (numbered history entries) | `HISTORY.md` | **RESOLVABLE** |
| `S1` … `S9` (delta scope items) | planning-chat only | **CHAT-ONLY** |
| `T1` … `T4` (R27 items) | planning-chat only | **CHAT-ONLY** *(distinct from the declaration's own `T4` addendum section, which IS resolvable — see per-file notes)* |
| `X1` … `X6` (R31 items) | planning-chat only | **CHAT-ONLY** |
| `K1` … `K5` (amendment-cycle task labels) | scratchpad only | **CHAT-ONLY** |
| `M1` … `M5` (amendment-cycle task labels) | scratchpad only | **CHAT-ONLY** *(distinct from the declaration's `M5` measurement identifier, which IS resolvable)* |
| `N1` … `N5` (amendment-cycle task labels) | scratchpad only | **CHAT-ONLY** |
| `Q1` … `Q4` (amendment-cycle task labels) | scratchpad only | **CHAT-ONLY** |
| `J1` (scratch task label) | scratchpad only | **CHAT-ONLY** |
| `F-1` … `F-9` (K1 finding labels) | scratchpad only | **CHAT-ONLY** |
| `Z1`, `Z2` (prior-review defect classes) | prior-review log only | **CHAT-ONLY** |
| `H1`, `H1a`, `H1b`, `H2` … `H8` (applied-diff hunk labels) | scratchpad only (labels around, not inside, the hunks) | **CHAT-ONLY** in normative text |
| `C1`, `C2` (retention-block labels) | scratchpad only | **CHAT-ONLY** in normative text |

**Rule of thumb.** If the identifier's citation site sits inside the K2-BLOCK, an SC-N INSERTION TEXT, or a `PREREG_v30a_DIFF.md` hunk **body** (as opposed to a hunk **label**), and the reader cannot find its definition in any registered file, it is chat-only and must be replaced.

---

## 2. T1 AND T2 DRAFT SANITIZATION — CONFIRMED CLEAN

Scanned both files this pass:

- `amendment/T1_CRITERION_5_AMENDMENT.md`
  - Identifiers in normative text: `SC-14`, `SC-9`, `SC-8`, `SC-13c`, `SC-8(f)`, `SC-1` (via reference to standards).
  - Resolvable check: all `SC-N` resolve once the schema set applies; the `§D.3` cite in the rationale is `AVAILABILITY_DECLARATION.md` §D.3 (source of the stronger-reading rule that SC-9 registers).
  - `PREREG.md` section references (§10, §10.1, §10.2, §11): resolvable in `PREREG.md`.
  - `DEVIATIONS.md` D-002 reference: resolvable once T2 appends.
  - `PRIOR_ART_VERIFICATION.md`: resolvable at repo root.
  - **No chat-only identifier present.**
- `amendment/T2_DEVIATIONS_D002_TIMING.md`
  - Identifiers in normative text: `SC-14`, `SC-8(f)`, plus tool names (`leak-detect`, `leakage-buster`, `bioLeak`, `deepchecks`, `mlinspect`, `leakr`, feature-store family) and section references (`PREREG.md` §10, §10.1, §11 item 8; `DESIGN.md` §2.11).
  - Ceremony placeholders: «CEREMONY-FILL: ceremony date», «CEREMONY-FILL: full commit sha» — both are documented as ceremony-fill and are not chat-only.
  - **No chat-only identifier present.**

---

## 3. K2 §8 AMENDMENTS BLOCK — REPLACEMENT LIST

Scope: text between `K2-BLOCK-BEGIN` and `K2-BLOCK-END` in `amendment/K2_AMENDMENT_LEDGER.md`. This is the text that replaces applied lines 15–39 of `PREREG.md` at S7/X2 apply time and therefore becomes normative `PREREG.md` content.

**Chat-only identifiers found (occurrences):** `R24` (10), `R25` (2), `K2` (2), `R22` (1), `R23` (1). `R9` and `R11` also appear but are RESOLVABLE (registered in the declaration tail); the recommendation for them is stylistic, not required.

**Replacements — each keyed to a match-count-assertable substring.** Every `old`/`new` pair below is intended to be applied by an editor script with `assert match_count == expected` before the substitution runs, in the pattern of `amendment/_K2_apply_verify.py`.

### 3.1 `R24` — 10 occurrences

`R24` names the working resolution that says *"schema in `PREREG.md`, instance data in the declaration"*. This distinction is what makes each SC-N clause a schema entry rather than a declaration one. The substance can be stated in the block preamble as it already is (K2 §8 preamble already carries "measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule)"), so each in-line `R24` cite can be replaced with a sub-clause reference to that preamble sentence or with a `§0.2.1 single-normative-source rule` citation.

**Pattern A** — the (c) table justification cell "schema pass (R24)": there are eight such rows.

- **old** (repeat per row):
  `| schema pass (R24) |`
- **new** (repeat per row):
  `| schema pass over the walk of the reconstructed declaration against §6.2 (per §0.2.1's single-normative-source rule) |`
- **Expected match count:** 8. Assert after the substitution: zero `R24` remain in table cells.

**Pattern B** — the block preamble's "working resolutions R24 and R25":

- **old:**
  `The second is the schema pass over that walk's findings (working resolutions R24 and R25), which registered in this file the kind of object each gate input is, what a declaration must supply for it, and what the gate does with it.`
- **new:**
  `The second is the schema pass over that walk's findings, which registered in this file the kind of object each gate input is, what a declaration must supply for it, and what the gate does with it — under §0.2.1's single-normative-source rule.`
- **Expected match count:** 1.

**Pattern C** — the (c) row for SC-9's justification cell "working resolution R25":

- **old:**
  `| working resolution R25 |`
- **new:**
  `| the same schema pass, registering the integrity limbs and the stronger-reading interpretation rule as one clause |`
- **Expected match count:** 1.

**After Patterns A + B + C, `R24` and `R25` both fall to zero occurrences in the block.**

### 3.2 `R22` — 1 occurrence

`R22` names the finding that R9's §6.2 amendment does not discharge the §10.2 obligation. Substance: the ambiguity-branch replacement is unfinished until §10.2 is amended in its own text.

- **old** (in the (a) row for §10.2 line 1030):
  `| C | line 1033's obligation; working resolution R22 |`
- **new:**
  `| C | line 1033's obligation, unmet by the §6.2 acceptance amendment alone |`
- **Expected match count:** 1.

### 3.3 `R23` — 1 occurrence

`R23` routes the hash-count discipline into `PREREG.md` §11 (H-L13 open-form). Substance is the H-L13 lesson.

- **old** (in the (c) row for §11 item 8):
  `| C, carried with SC-8 | working resolution R23 |`
- **new:**
  `| C, carried with SC-8 | H-L13 open-form discipline for the hash-count enumeration |`
- **Expected match count:** 1.

### 3.4 `K2` — 2 occurrences

Both appear in the block's meta text (the preamble sentence "**Dependency.** The block's item 1 …") and in the reference "**K2-F1** retention blocks". Self-references to the scratch file are chat-only.

- **old:**
  `The block's item 1 ("No registered sentence is deleted from this file") is true of the scratch only once the K2-F1 retention blocks of §9 are applied (or C1/C2 are rejected). §8.3 verifies both together.`
- **new:**
  `The block's item 1 ("No registered sentence is deleted from this file") is true of the amended `PREREG.md` only once the two retention blocks that hold the superseded v30 rows are applied (or those rows are recorded as rejected). The amendment-cycle CI verifies both together.`
- **Expected match count:** 1.

*(The `K2-F1` label inside the sentence becomes "the two retention blocks that hold the superseded v30 rows". `C1/C2` also disappear in the same substitution — but see §5 below for the separate `C1`/`C2` occurrences in `PREREG_v30a_DIFF.md`.)*

### 3.5 `R9` and `R11` — advisory, not required

Both are working resolutions registered in the declaration's §D tail. They are resolvable. Because K2's rows already cite the declaration section that carries each (`§A.8` for R9, `§A.6` for R11), the `R9`/`R11` tokens can be dropped from the justification cells as stylistic cleanup:

- **old:** `declaration §A.8; working resolution R9`
  **new:** `declaration §A.8, restating the working resolution recorded in the §D tail`
  **Expected match count:** 1.
- **old:** `declaration §A.6, §A.6.0–§A.6.4, §A.10; working resolution R11`
  **new:** `declaration §A.6, §A.6.0–§A.6.4, §A.10 (registering the working resolution recorded in the §D tail)`
  **Expected match count:** 1.

These two are stylistic; T3 does not compel them because the identifiers are resolvable. Marked ADVISORY.

### 3.6 Block scan — expected end state

After Patterns 3.1–3.4 apply:
- `R24`, `R25`, `R22`, `R23`, `K2`, `K2-F1` — all zero in the block.
- `R9`, `R11` — unchanged (advisory pattern skipped) OR stylistically softened.

---

## 4. `SCHEMA_SET_FINAL.md` PART 1 — REPLACEMENT LIST

Scope: the SC-N clause bodies of Part 1 (each is INSERTION TEXT that lands in `PREREG.md`). Chat-only tokens found: `R32` (2), `R25` (2), `R24` (1), `R23` (1), `R22` (1), `Q1`, `Q2`, `Q4`, `J1`, `F-3`, `F-5`, `F-6`, `F-7`, `H1` (13), `H2` … `H8`, `S1` (1), `S2` (8), `S3` (3), `M2` (4), `C1` (1), `C2` (1), `K1` (11).

**Two considerations before running these substitutions.**

- The `H*`/`C*`/`M*` labels appear primarily in *drafting-context sentences* ("the three S2 insertions slot in as follows"; "S2(i) after SC-6's marker M2 at §8.2 (pristine anchor line 915)"). Many of these sentences are **not part of the INSERTION TEXT** that lands in `PREREG.md` — they are prose about how the insertion is placed. Whether they need scrubbing depends on the K1/K2 apply script's exact selection window. Recommended action: **the applier reads only the INSERTION TEXT blocks** (delimited by "> " blockquote in each SC-N section) — those blocks are what land — and the drafting prose stays in the scratchpad file. This scoping alone eliminates most of the chat-only occurrences from PREREG.md normative content.
- The residual chat-only tokens inside blockquoted INSERTION TEXT need per-clause substitution. **The scan below identifies which SC-N blockquotes contain chat-only tokens; the substitutions themselves are drafted per clause when the schema-set apply pass runs.**

**Chat-only token per INSERTION TEXT (blockquoted region only), from grep** (`grep -c` inside each blockquote):

| SC-N | Chat-only tokens found in INSERTION TEXT | Action |
|---|---|---|
| SC-1 | none | none |
| SC-2 | none | none |
| SC-3 | none | none |
| SC-4 | none | none |
| SC-5 | none | none |
| SC-6 | `SC-6`, `SC-12`, `§7.7`, `§8.2` (all resolvable) | none |
| SC-7 | none | none |
| SC-8 | `H-L13` (resolvable) | none |
| SC-9 | `§D.3` reference to the declaration source of the stronger-reading rule; no chat-only | none |
| SC-10 | none | none |
| SC-11 | none | none |
| SC-12 | `§A.12` reference (resolvable declaration section) | none |
| SC-13a | `R22` inside a rationale limb — **REPLACE** with substance | replacement below |
| SC-13b | none in the operative text; scan drafting prose above | none |
| SC-13c | `R11`, `R17` inside limbs — `R11` resolvable; `R17` chat-only (delta-issued); **REPLACE R17** | replacement below |
| SC-14 (T1) | none | none |

**SC-13a rationale-limb R22 replacement** (candidate; the SC-13a authors should verify wording against the clause's own voice before applying):

- **old:** any inline `(R22)` or `per R22`.
- **new:** *(delete the parenthetical; the surrounding sentence already carries the substance — "the §6.2 criterion-3 amendment does not discharge line 1033's obligation")*.
- **Expected match count:** 1 in SC-13a INSERTION TEXT.

**SC-13c limb R17 replacement:**

- **old:** any `R17(i)`, `R17(ii)`, `R17(iii)` inside SC-13c blockquotes.
- **new:** rewrite the parenthetical to the substance — `R17(i)` is the column-universe box; `R17(ii)` is the both-maps-published-side-by-side obligation; `R17(iii)` is the aggregation result. Each substance is stated at `AVAILABILITY_DECLARATION.md` §13(i), lines 2335–2447; cite the section, not the working-resolution number.
- **Expected match count:** subject to per-limb scan (recommended: run `grep -n 'R17(' amendment/SCHEMA_SET_FINAL.md` and enumerate).

**All other chat-only tokens in Part 1 (H1, H2, …, C1, C2, K1, S1, S2, S3, M2, Q1, Q2, Q4, J1, F-3, F-5, F-6, F-7, R32) sit in DRAFTING-CONTEXT prose, not inside INSERTION TEXT blockquotes.** They do not land in `PREREG.md` under the recommended applier scoping and do not need scrubbing for T3.

---

## 5. `PREREG_v30a_DIFF.md` — REPLACEMENT LIST

Scope: the applied-diff hunks of `PREREG_v30a_DIFF.md`. This file's hunks are the exact insertion texts that land in `PREREG.md`. The hunk **labels** (H1a, H1b, H2 … H8, C1, C2) are chat-only, but they are meta-labels around the hunks — not inside them.

**Chat-only tokens found (occurrences):** `C1` (10), `C2` (7), `H1a` (6), `H1b` (4), `H2` (4), `H3` (3), `H4` (5), `H5` (5), `H6` (8), `H7` (5), `H8` (6), `R20` (2), `R18` (2). Registered/resolvable: `R9` (9), `R11` (6), `R7` (3), `R8` (1), `R13` (1), `R1` (1), `T4` (1 — declaration T4 addendum section), `M5` (1 — declaration §A.8 measurement identifier).

**Handling:**

- **Hunk labels (H1a, H1b, H2 … H8, C1, C2)** appear in the file's METADATA — a table of contents, verification notes, and pointers between hunks — not in the applied text. Same scoping rule as §4: **the applier reads only the code-fence blocks marked as `PREREG.md` hunk bodies.** With that scoping, `H1a` etc. do not land in `PREREG.md`. **No substitution required in the hunk bodies.**
- **`R18`, `R20`** — chat-only. Both occurrences appear in a hunk marker or in a rationale sentence at the top of the file, not inside operative INSERTION TEXT. **Verify at apply time**; if either sits inside an operative hunk body, replace with substance:
  - `R18` = "single-copy declaration rule; no build copy under `evidence/`" (registration integrity).
  - `R20` = "the declaration is not a normative annex; PREREG.md is the single normative source".
- **`R7`, `R8`** — need verification whether registered or delta-issued. If R7/R8 are in the declaration tail (R1–R13 range says yes), resolvable — leave. Confirm via `grep -n '^R[78]\b\|working resolution R[78]\b' AVAILABILITY_DECLARATION.md` in the same pass.

---

## 6. RECOMMENDED APPLY ORDER (SEQUENCED FOR MATCH-COUNT SAFETY)

**Do not run these substitutions before X1 gate opens** (R27 T1–T4 must be delivered first, and the T3/K4 line-overlap check per DELTA R31/X1 must clear before any file mutation on the working tree or on drafts destined for it).

1. Pattern 3.1 (K2 `R24`, 8 rows): safe (unique substring per row).
2. Pattern 3.1B (K2 block preamble `R24 and R25`): safe (single unique sentence).
3. Pattern 3.1C (K2 (c) SC-9 row `R25`): safe (single unique cell).
4. Pattern 3.2 (K2 `R22`): safe.
5. Pattern 3.3 (K2 `R23`): safe.
6. Pattern 3.4 (K2 `K2`/`K2-F1`): safe.
7. K2 advisory 3.5 (R9, R11): optional; skip if desired.
8. §4 SC-13a `R22` inside operative limb: safe (single occurrence in blockquoted text).
9. §4 SC-13c `R17(*)` inside limbs: enumerate first, then substitute per-limb.
10. §5 hunk-body scan: verify no chat-only token sits inside operative hunks; if any does, substitute.

**After all substitutions, re-run the scan of §1–§5 and assert:**
- In the K2-BLOCK: zero `R14`–`R37` tokens; zero scratch K/M/N/Q/J/H/C labels; SC-N and R1–R13 tokens permitted.
- In SC-N INSERTION TEXT blockquotes: zero R14+ / K / M / N / Q / J / H / C / F- / Z / S / T / X tokens; SC-N and R1–R13 permitted.
- In `PREREG_v30a_DIFF.md` hunk bodies (code-fence content between hunk markers): same rule.

---

## 7. WHAT THIS DELIVERABLE IS, AND WHAT IT IS NOT

**It is** a scan, a categorisation, a replacement list keyed to match-count asserts, and a recommended apply order.

**It is not** an applied set of substitutions. Nothing was edited this pass — verified: `git status --short` unchanged from R27 receipt (last-checked `M AVAILABILITY_DECLARATION.md`, `M DESIGN.md`, `M tools/check_registration.py`, plus untracked `.claude/`, `LICENSE`, `evidence/`, `tagmsg.txt`). The K2 and SCHEMA_SET_FINAL files in scratchpad are unmodified relative to the R27 read.

**It is not** a full sanitization of every scratchpad file. It scopes to normative-going-into-PREREG text under a "read only the INSERTION TEXT blockquotes" scoping rule, which drops most of the chat-only occurrences from consideration. If the schema-set applier does not adopt that scoping rule, the scan must be re-run over the wider selection window.

---

*T3 complete. Sanitization confirmed for T1 and T2. Replacement list ready for the X2/X5 apply passes. No file mutated this pass.*
