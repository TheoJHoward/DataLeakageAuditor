# K2 — THE AUTHORITATIVE v30a AMENDMENT LEDGER (ITEM S4), ENUMERATION-FIRST

**Nothing in the repository was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and
`HISTORY.md` in `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01` are untouched — verified at the
start and end of this pass: repo `PREREG.md` sha256 `f0a8f001…c7cc6` (1,099 lines) = `git show
prereg-v30:PREREG.md` (same hash, 1,099 lines); `git status --short` unchanged (` M
AVAILABILITY_DECLARATION.md`, ` M DESIGN.md`, ` M tools/check_registration.py`, `?? .claude/`, `?? LICENSE`,
`?? evidence/`, `?? tagmsg.txt`). **No state-changing git command was run** (only `git status --short`
and `git show prereg-v30:PREREG.md` piped to `sha256sum`/`wc`). The archive at
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not read. `HISTORY.md` lines 210–222 (H-L12, H-L13) and
`tagmsg.txt` were read in the repo, not edited.

**Read state.** Pristine v30 `PREREG.md` = `applied\_PREREG_pristine.md.bak` (`f0a8f001…c7cc6`, 1,099
lines, hash-identical to the repo file and to the tag). Applied scratch `PREREG.md` =
`applied\PREREG.md` (`e7ab52d3…1706`, 1,417 lines — the SCHEMA_SET_FINAL step-C state). Applied scratch
declaration = `1290186e…1c30`, 3,695 lines — S1's K4 proposal for
lines 1047–1056 applied; every declaration line number below 1056 is unchanged from the working-tree
file `f0829bd3…3310`, and every line below it is shifted +11.

> **State note, recorded on re-verification (see K2-F7).** `applied\AVAILABILITY_DECLARATION.md` has
> since moved: item S7 (K4) is writing to the same scratch copy, and at re-verification the live file
> was `ddbf7f2d…48d6`, 3,796 lines, **still being written**. The `1290186e…1c30` state this ledger was
> built against is preserved there as `_DECL_preK4.md.bak` (verified byte-identical by hash). **This
> changes nothing in the table**: `applied\PREREG.md` is unmoved at `e7ab52d3…1706`, 1,417 lines
> (re-hashed at the end of this pass), every "Applied lines" cell is a `PREREG.md` line, and every
> declaration citation below is **working-tree** numbering (`f0829bd3…3310`, 3,684 lines — re-hashed,
> unchanged), which the scratch pass does not touch. What K4 does change is the disposition of K2-F5,
> recorded there.

Read in full: `SCHEMA_SET_FINAL.md`
(2,174 lines); the hunk-by-hunk diff of pristine → applied `PREREG.md` (25 diff hunks, written to
`_K2_diff_pristine_vs_applied.txt`); `PREREG_v30a_DIFF.md` §(i), H1a, H8, C1, C2, §(iii);
`J1_GATE_CRITICAL_CLASSIFICATION.md` §5(e)–(f) (lines 375–399); `K1_SCHEMA_CLAUSES.md` §0, §5, §6, §7;
the declaration's §A.11 (1506–1521), §D.1 item 5 (3391–3406), §D.2 (3420–3439) in working-tree
numbering; `tools/check_registration.py` `check_phase_arithmetic` (lines 708–741). **Read, not edited.**

**Files written this pass — all under `…\8b1d67a4…\scratchpad\amendment\`, nothing elsewhere:** this
file; `_K2_diff_pristine_vs_applied.txt` (the 25-hunk diff, pristine and applied line numbers);
`_K2_BLOCK_TEXT.md` (the amendments-block text of §8, the file the applier reads);
`_K2_apply_verify.py` (applier, refuses to run outside `_K2_verify\`, asserts match count 1 at every
anchor); `_K2_BLOCK_TEXT_as_applied.md` (what the applier wrote, for word-for-word comparison with §8);
and the verification copy `_K2_verify\` (a copy of `applied\` minus `.bak`/probe files and
`CI_GATE_RESULT.md`, with `_K2_baseline_checker.txt`, `_K2_after_checker.txt`, `_K2_baseline_pytest.txt`,
`_K2_after_pytest.txt` inside it). `_K2_verify\` can be deleted once the author has read §8.3.

**What this file contains.** §1 the four numbers and why this is H-L13's third venue · §2 conventions ·
§3 THE TABLE (Part A, 36 rows; Part B, surfaces named but not touched) · §4 derived counts · §5
reconciliation of the four legacy numbers · §6 cross-check applied ↔ clause insertion points · §7
findings and observations · §8 the v30a amendments-block text (enumeration-first, numeral-free), with
the CI verification record · §9 the K2-F1 fix (C1/C2 retention), drafted and verified · §10 author
decisions and limits.

---

## 1. FOUR NUMBERS, ONE QUESTION — H-L13's THIRD VENUE

Four different numerals currently answer "what does v30a amend":

| Numeral | Where it is written | What it is a count of (derived in §5 from the table) |
|---|---|---|
| **four** | `AVAILABILITY_DECLARATION.md` §A.11, line 1516: "**Four amendments (445, 450, 451, 461).**"; line 1520: "All four amendments are class C under PREREG.md line 93" | the registered **§6.2 lines** the §A walk marked AMENDED — walk scope, §6.2 only |
| **five** | `AVAILABILITY_DECLARATION.md` §D.1 item 5, lines 3399–3403: "**The four §6.2 amendments and the §10.2 definition**, as written: §A.1 …, §A.3 …, §A.4 …, §A.8 …, and §A.12's definition of 'waived'" | the **amendment-content sections of the declaration** frozen at §D.1 item 5 |
| **six** | H1a/H1b — applied `PREREG.md` line 8 "Six class C changes under §0.2.1", line 17 "It carries six class C changes", line 37 "**All six are class C under §0.2.1 line 93**", and the six-row table at lines 28–35 (`PREREG_v30a_DIFF.md` lines 78, 104–131) | H1's **class C hunks** H2, H3, H4, H5, H6, H7 — "clauses amended" as of H1's drafting |
| **fifteen** | `SCHEMA_SET_FINAL.md` closing tally: "Clauses delivered … **15** — SC-1 … SC-12, SC-13a, SC-13b, SC-13c" | **schema clause texts** in the final set — not surfaces, not supersessions |

Each numeral was true on its own unit at the moment it was written and each was written as a literal
outside the edit that later grew the set. That is exactly the fragility `HISTORY.md` H-L13 (12 Aug 2026)
records — "enumerated ranges in cross-references are fragile by construction, because the obligation to
re-bump lives outside the edit that grows the target" — and **this is its third venue**: (1) the
`DESIGN.md` §9 cross-reference "H-L1 through H-L11", fixed by naming the series in open form (H-L13
itself); (2) the tag-message hash count — `PREREG.md` line 97 "both", §11 item 3 "three", the executed
`prereg-v30` tag five, the declaration's §D.2 six (J1 §5(e); `SCHEMA_SET_FINAL.md` Part 3(ii)), fixed
by §11 item 8 reading the count from the tag message's own enumeration; (3) the amendment count —
four / five / six / fifteen. The fix here is the same: **the ledger is built from the enumeration, every
count is derived from it below the table, and the amendments-block text of §8 states no numeral at all.**

---

## 2. CONVENTIONS OF THE TABLE

- **Registered surface** = a line, or a gap between lines, of the pristine v30 `PREREG.md` (1,099
  lines, `f0a8f001…c7cc6`) that the applied text addresses. Where a marker is *about* one line but
  physically placed at another (e.g. the line-459 marker sits above SC-4 after line 464), the surface
  is the line addressed and the "Applied lines" column says where the marker sits. Every line number
  in the "Registered surface" column is pristine v30 numbering — the numbering every v30a marker and
  `git show prereg-v30:PREREG.md` use.
- **Kind of touch**, one of: **SUPERSESSION** (the registered text at that line is replaced by operative
  v30a text); **CONSEQUENTIAL** (a one-line rewrite H1 flagged as derived from an amendment, not
  walk-cited); **INSERTION** (new text at a site where no registered sentence is replaced);
  **MARKER only** (the registered text stands byte-exact; a v30a marker at its site states what reading,
  count, or assumption is superseded or extended); **POINTER** (a cross-reference that adds no rule of
  its own).
- **Class** is §0.2.1 line 93's: A (mechanical branch fact), B (parameter under a locked procedure), C
  (semantic or accounting gap — "anything that changes what a published number means"). "—" means the
  text asserts no semantics (a navigation line, a record, a pointer). "Carried with SC-n" means the
  marker has no class of its own and rides with the clause named. Where the class is an author
  decision it is flagged (K2-F4).
- **Scope**: IN SCOPE (walk) = cited by the §A walk; IN SCOPE (schema) = produced by the R24 schema pass
  (J1 → K1 → SCHEMA_SET); IN SCOPE (integrity) = R25/R23 integrity routing; IN SCOPE (consequential) =
  H1's C1/C2, derived not walk-cited, author adjudication required; IN SCOPE (record) = the amendment's
  own record/navigation text. OUT OF SCOPE surfaces — named in marker text but not touched — are in
  Part B and are **not counted**.
- **Justification**: the §A walk section, the J1 rows (K1 §2 accounting; SCHEMA_SET_FINAL "ROWS
  COVERED"), or the K1 finding, as applicable. Declaration line numbers are working-tree numbering
  (`f0829bd3…3310`); add 11 for the applied scratch copy below line 1056.
- **Applied lines** are those of `applied\PREREG.md` at `e7ab52d3…1706` (1,417 lines), verified this
  pass line by line (`_K2_diff_pristine_vs_applied.txt`).

---

## 3. THE TABLE

### Part A — every registered surface v30a touches (36 rows, ascending by pristine line)

| # | Registered surface (pristine v30) | Kind of touch | Applied lines (`e7ab52d3…`) | Clause(s) responsible · source | Class (§0.2.1 L93) | Scope | Justification (§A walk / J1 rows / K1) | Notes |
|---|---|---|---|---|---|---|---|---|
| R01 | Header, after line 6 (`**Status:** v30 …`) | INSERTION — navigation line (amendment status) | A8 | H1 hunk **H1a** (`PREREG_v30a_DIFF.md` lines 65–78); not a schema clause | — (names the amendment and the recovery command; asserts no semantics) | IN SCOPE (record) | H1: §A.0, §A.11 | Carries "**Six class C changes**" — a stale numeral (K2-F2); replaced by §8.1. With R02, the only applied v30a surface not stated in any SC clause's insertion point (K2-O1). Line 6 itself stands byte-exact, so `_prereg_version()` still reads 30. |
| R02 | Header, after line 8 (`**Registration:** …`) | INSERTION — the v30a amendments block proper | A15–A39 | H1 hunk **H1b** (`PREREG_v30a_DIFF.md` lines 85–131) | — (the record of the amendment; the class C authority is each enumerated change's) | IN SCOPE (record) | H1: §A.0 (decl. 760–767), §A.11 (1516–1521) | Carries "six class C changes" (A17), the six-row table (A30–A35), "**All six are class C**" (A37), "amendment 3" (A39) — stale (K2-F2; CI report §7 obs. 1; SSF Part 6 item 2(b)). Replaced by §8.2. |
| R03 | Header, same site, following R02 | INSERTION — §AB recording text (RECORDED DEFECT, lines 816/830; what the exception claims and does not; what is NOT resolved) | A41–A53 | SSF §AB (ledger F-13; Q4 ITEM 3 → S3(1)); records SC-13c(c2) and SC-13b(b3) | — (record; the exception's class C authority is SC-13c(c2)'s) | IN SCOPE (record) | SC-13b(b3); SC-13c(c2); §0.2.1 lines 72, 77 | Kept byte-exact by §8.2. The 816/830 duplicated-authority defect is flagged for a future class C amendment and NOT resolved. |
| R04 | §0.2.1 line 97 — "both file hashes in the tag message" | MARKER only — "SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT"; text stands byte-exact | A144 (placed after line 97) | SC-8 insertion point 2 — S2(ii) marker (SSF Part 3(ii)) | C, carried with SC-8 — the count supersession alone changes no published number (K2-F4: R7 recorded the hash count as a class A mechanical fact; R23 / J1 §5(e) route it to `PREREG.md`) | IN SCOPE (integrity) | J1 §5(e) row 126; SSF Part 3(ii); H-L13 | H-L13's second venue (the hash count). |
| R05 | §0.2.1 gap after line 99, before line 101 | INSERTION — SC-9 (a)–(f), pure insertion; lines 93–99 stand byte-exact | A148–A160 | **SC-9** | C by carriage — integrity rules that "never flip a verdict alone" (SSF SC-9 REGISTERS) but govern how every locked obligation is read (SC-9(e)) | IN SCOPE (integrity, R25) | J1 gate-critical rows 7, 128; non-gate rows 8, 9, 18, 22, 23, 27 → PREREG (R25); row 138's R13 (K1 §3) | K1 F-2 (row 7 redistributed here). |
| R06 | §2.3 line 205 — `column_roles` row of the declaration-element table | MARKER only — "ADDED NOT SUPERSEDED"; the role enumeration stands byte-exact | A275 (placed after the table, i.e. after pristine line 213) | **SC-1(c)** | carried with SC-1 | IN SCOPE (schema) | SC-1's rows 1, 3, 4, 72, 96, 104, 124 | SSF fixes no placement line for SC-1's two markers; the CI run chose this one (K2-O2). |
| R07 | §2.4 lines 220–222 — the label-availability formula and its first bullet | MARKER only — "PARTIALLY SUPERSEDED": the unstated assumption that the horizon term's unit is a duration; the formula stands byte-exact as the form | A285 (placed after line 220) | **SC-1(d)** | **C** — line 93's word "unit" (SC-1(d)'s own terms) | IN SCOPE (schema) | same rows | K2-O3: the marker sits inside the 220–222 range it marks (between the formula and the bullets); cosmetic, no text displaced. |
| R08 | §2 end: gap after line 266 (close of §2.8), before the `---` at line 268 — new **§2.9** | INSERTION — SC-1 (a)–(f) | A333–A347 | **SC-1** | C | IN SCOPE (schema) | rows 1, 3, 4, 72, 96, 104, 124 | "§2.9" is a bold paragraph heading, not a `###` heading — `sections_of()` gains no numbered section. |
| R09 | §6.1 line 431 — heading "Five bodies of data" and its table (433–439) | MARKER only — "AMENDED IN FORM": the implication of exhaustiveness is superseded; heading and table stand byte-exact | A524 (placed after line 441, above SC-10) | **SC-10** | carried with SC-10 | IN SCOPE (schema) | rows 85, 123; K1 F-5 | OPEN: K1 F-5 (amend the heading and add a sixth row vs. SC-10 as drafted) is the author's call; the marker text carries the drafting identifier "F-5" (K2-F3). |
| R10 | §6.1 gap after line 441 (the section's closing paragraph) | INSERTION — SC-10 (a)–(e) | A526–A536 | **SC-10** | C — denominator membership; what a headline or peak means | IN SCOPE (schema) | rows 75, 85, 92, 110, 123 | K1 F-8: duplicate pairs 92/110, 85/123 collapse here; their declaration copies become citations (K4). |
| R11 | §6.2 line 445 — **Reference AUC** | **SUPERSESSION** — v30 line retained verbatim (A541), NOT operative | A540–A543 | H1 hunk **H2** (instance-bearing supersession); schema layer **SC-2(d)** | **C** | IN SCOPE (walk) | decl. §A.1 (771–818); J1 row 14 (K1 F-4: the row is discharged only with H2) | One of the declaration's "four". The operative text cites `AVAILABILITY_DECLARATION.md` §A.1 for the entries. |
| R12 | §6.2 line 450 — **Contamination availability class** | **SUPERSESSION** — retained verbatim (A549), NOT operative | A548–A551 | H1 hunk **H3**; schema layer SC-2, with **SC-9(b)** (evidence artifacts never adjusted toward a decision) | **C** | IN SCOPE (walk) | decl. §A.3 (882–934) | One of the "four". The locus moves to a tag-hashed file; the obligation is not removed. |
| R13 | §6.2 line 451 — **Sliced variant for CI** | **SUPERSESSION** — retained verbatim (A553), NOT operative | A552–A555 | H1 hunk **H4**; schema layer **SC-2(e)**, **SC-3(f)** | **C** | IN SCOPE (walk) | decl. §A.4 (938–984); J1 rows 25, 66 | One of the "four". The element "amended explicitly, never waived and never left outstanding". |
| R14 | §6.2 gap after line 451, before "**Pass gate**" (line 453) | INSERTION — SC-2 (a)–(e) | A557–A567 | **SC-2** | C | IN SCOPE (schema) | rows 11, 14, 25, 66 | The schema layer over R11–R13; it cites H2/H3/H4's markers and redrafts none. |
| R15 | §6.2 line 459 — **criterion 1** | MARKER only — "ADDED NOT SUPERSEDED": criterion 1 byte-exact; superseded is the inference that the denominator is a construction-taxonomy count; the marker also records "§6.2 line 446 — NOT AMENDED" | A604 (placed after line 464, above SC-4) | **SC-4** | carried with SC-4 | IN SCOPE (schema) | H1 §(iii) items 1 and 4; decl. §A.11 line 1508 (criterion 1 SATISFIED, denominator re-derived) | See Part B for line 446. |
| R16 | §6.2 line 461 — **criterion 3** | **SUPERSESSION** — registered criterion retained verbatim (A597), NOT operative; SC-3 is the operative criterion | A577–A596 (clause); A597–A599 (marker) | **SC-3**, carrying H1 hunk **H5**'s structure | **C** — an acceptance criterion | IN SCOPE (walk + schema) | decl. §A.8 (1407–1436), working resolution R9; rows 5, 6, 26, 55, 56, 74, 89, 95 | One of the "four". Marker A599 carries the drafting identifier "(H1 **C2**)" (K2-F3). SC-13a–c depend on this amendment one way (SC-13c(c1)); it depends on nothing. |
| R17 | §6.2 gap after line 464 ("Secondary findings on **manifest-listed descendants** …") | INSERTION — SC-4 (a)–(j), as corrected under R32 | A606–A637 | **SC-4** (H1 hunk **H6**'s placement) | **C** — the criterion-1 denominator | IN SCOPE (walk + schema) | decl. §A.6 (1020–1045), §A.6.0 (1047–1145), §A.6.4 (1257–1269), §A.10 (1474–1492); working resolution R11; rows 17, 19, 29, 30, 31, 32, 33, 34, 35, 36, 48, 50, 59, 93, 98, 99, 103, 105, 108 | H1b's #5. **Not** in the declaration's "four": §A.11 line 1508 marks criterion 1 SATISFIED with the denominator re-derived, not AMENDED. R32 applied (SSF Part 2). |
| R18 | same gap, following SC-4, before line 466 | INSERTION — SC-5 (a)–(f) | A639–A651 | **SC-5** | C — routing decides which criterion a finding reaches | IN SCOPE (schema) | rows 38, 39, 42, 43, 44, 58, 100, 101, 107 | K1 F-8 pairs 44/101, 39/107 collapse here. |
| R19 | §6.2 gap after line 468 ("Top-k presence …"), before line 470 | INSERTION — SC-7 (a)–(e) | A657–A667 | **SC-7** | C — "a run that received the key has not produced a gate result" | IN SCOPE (schema) | rows 129, 130; K1 F-9 (a new registered surface) | |
| R20 | §6.2 line 480 — **Ordering, locked** | MARKER only — "EXTENDED NOT SUPERSEDED"; the locked ordering stands byte-exact | A681 | **SC-8** | carried with SC-8 | IN SCOPE (schema) | H1 §(iii) item 9; decl. §A.10 item 3 (1490–1492) | |
| R21 | §6.2 gap after line 480 | INSERTION — SC-8 (a)–(f) | A683–A695 | **SC-8** | **C** — what freezes, in what form; "any subsequent change … is a class C amendment" | IN SCOPE (schema + integrity) | rows 80, 88, 106, 119, 120, 121, 122, 125; row 126 (INTEGRITY → PREREG, K1 §3) | SC-8(f) states the hash-count rule generically; §11 item 8 (R36) indexes it. |
| R22 | §7.2.1 line 816 — the `not_applicable`-everywhere suppression sentence | POINTER at a registered line (**§13c-P**) — line 816's text stands byte-exact; SC-13c(c2) states an express, scoped exception to its suppression clause for SC-13a's required quantities only | A1033 (between line 816 and line 818) | **SC-13c** insertion point 2 (§13c-P, reduced to H8's form — S3(2)) | pointer: — ; the exception it points to: **C** — "a class C change to how line 816 reads at this one criterion" (SC-13c(c2)), recorded in §AB | IN SCOPE (schema) | SC-13b(b3); SC-13c(c2); Q4 ITEM 6 (NEW DEFECT 1) | Line 818 stands as registered; the 816/830 conflict is recorded in §AB and NOT resolved. `suppression_anchor` still PASSes. |
| R23 | §7.7 line 855 — **Detector-case coverage** row | **SUPERSESSION** — the row is replaced (A1072: `unscored` appended); the registered row is retained verbatim (A1075), NOT operative | A1072; A1075 | **SC-6** insertion point 1 | **C** — line 93's "a needed *new* … coverage state", verbatim | IN SCOPE (schema) | J1 §5(f) rows 46, 82; K1 §0 (line 855 verified: six states, `unscored` absent); rows 46, 49, 60, 82 | The one hunk that modifies a table row the checker might parse (K1 F-9) — verified CI-neutral by the CI run and again this pass. |
| R24 | §7.7 gap after line 856 (after the table) | INSERTION — SC-6 (a)–(e) | A1077–A1087 | **SC-6** | C | IN SCOPE (schema) | same rows; K1 F-6 (the entry condition, a K1 drafting decision) | |
| R25 | same gap, following SC-6's block | POINTER — "`waived` is defined in §10.2 (v30a)", naming **SC-12(w)** as its entry condition (the residual-gap statement is superseded; DELTA R35/B3) | A1089 | H1 hunk **H8** = **SC-12** insertion point 2 | — (pointer; "adds no normative content", H1) | IN SCOPE (walk) | decl. §A.12 (1539–1544, 1571–1573); H1 §(iii) item 12; K1 F-6 | |
| R26 | §7.8 gap after line 892 ("Conformance cases contribute to no detection metric …") | INSERTION — SC-11 (a)–(g) | A1127–A1141 | **SC-11** | **C** — under criterion 3 a zero-violation aggregate is a pass claim | IN SCOPE (schema) | rows 78, 90, 134, 135; K1 F-9 | |
| R27 | §8.2 line 915 — the not-run-states paragraph | MARKER ("EXTENDED NOT SUPERSEDED") + POINTER **S2(i)** — `unscored` is governed by §8.2's closing sentence, by reference to §7.7's row; line 915's text stands byte-exact | A1166 (marker); A1168 (pointer) | **SC-6** insertion point 2 (SSF Part 3(i)) | carried with SC-6; the pointer adds no rule — its open-form range reaches `waived`, disclosed (SSF Part 3(i); author decision SSF Part 6 item 4(ii)) | IN SCOPE (schema) | J1 §5(f) drafting note; K1 §0 | The H-L13 open-range form applied to a coverage-state list. |
| R28 | §8.6 gap after line 961 | POINTER **S2(iii)** — a zero, an empty result, or an all-clean statement is a published number under §8.6; SC-11 governs what it must survive and name | A1216 | **SC-11** insertion point (SSF Part 3(iii)) | — (pointer) | IN SCOPE (schema) | SC-11(c), (f) | |
| R29 | §10 line 992 — Phase 1 row of the phase table, **Gate cell** | **CONSEQUENTIAL** — one-line rewrite of the Gate cell (H1 **C1**); Phase/Work/Est. byte-identical; **the v30 row is NOT retained inline** (K2-F1) | A1247 | H1 **C1**; cited by SC-2's marker ("§10 line 992 — CONSEQUENTIAL (H1 **C1**)") | **C (consequential)** | IN SCOPE (consequential) — derived from §A.1 + §A.4; NOT walk-cited; **author adjudication required** (H1 DIFF lines 401–419) | H1 C1; §6.8's deletion-certificate rationale (inbound reference to two retired objects) | K2-F1: breaches the amendments block's own item 1 ("No registered sentence is deleted from this file") until the retention block of §9 is applied. `check_phase_arithmetic` reads the Est. cell only — unaffected. |
| R30 | §10.1 line 1022 — kill-gate **criterion 3** | **CONSEQUENTIAL** — one-line rewrite (H1 **C2**); the ambiguity branch carried through unchanged; **the v30 text is NOT retained inline** (K2-F1) | A1277 | H1 **C2**; cited by SC-3's marker (A599) and by SC-13a's marker (A1299: "not amended by these clauses" — correct: it is amended by C2 under SC-3, not by SC-13a–c) | **C (consequential)** | IN SCOPE (consequential) — derived from §A.8; NOT walk-cited; author adjudication required (H1 DIFF lines 423–441) | H1 C2; SC-3's marker | K2-F1. |
| R31 | §10.2 line 1030 — kill/pause **criterion 2** | **SUPERSESSION ON THE AMBIGUITY BRANCH ONLY** — registered text retained verbatim (A1295) and operative where the branch has NOT fired; SC-13a operative where it has fired and been recorded | A1285–A1293 (clause); A1295–A1299 (markers) | **SC-13a** (with SC-13b and SC-13c: "one class C amendment … adopted together") | **C** — line 1033's "class C amendment carrying the complete replacement criterion — unit, threshold, and denominator" | IN SCOPE (schema; obligation) | line 1033's obligation (J1 §6.2–§6.3, R22); K1 F-1, F-7; K5 / M1 / SC13_SPLIT_ABC; SSF Part 1 | Markers state NOT SUPERSEDED: lines 1031, 1033, 1035, 816 (text); line 1022 not amended by these clauses. Rows covered: none of J1's 76 — it discharges an obligation, not a row. |
| R32 | §10.2 gap after line 1035 (the floor), before line 1036 | INSERTION — SC-12 ("Waived", defined; the governed set pinned by citation; what the definition does not permit) | A1307–A1317 | **SC-12** (H1 hunk **H7**'s drafting basis; split-file deltas merged) | **C** | IN SCOPE (walk + schema) | decl. §A.12 (1525–1597); rows 62, 63, 64 | H1b's #6; §D.1 item 5's fifth object. |
| R33 | same gap, following SC-12 | INSERTION — SC-13b (b1)–(b4) | A1319–A1327 | **SC-13b** | C (one amendment with SC-13a) | IN SCOPE (schema; obligation) | line 1033; SC13_SPLIT_ABC | N4 residue carried open: (b1)'s STOP for the label-availability detector today (SSF Part 6 item 2(d)). |
| R34 | same gap, following SC-13b, before line 1036 (criterion 3) | INSERTION — SC-13c (c1)–(c7) | A1329–A1347 | **SC-13c** | C; (c2) is the class C change to how line 816 reads at one criterion | IN SCOPE (schema; obligation) | line 1033; SC13_SPLIT_ABC; Q4 | (c5)(i) "only" dropped (S3(3)). (c3) and SC-12 pin the same governed set — deliberate mirror (SSF Part 6 item 2(g)). |
| R35 | §11 line 1050 — item 3 (the three hashed files) | MARKER only — "SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT"; text stands byte-exact | A1370 (placed beneath the list) | SC-8 / §11 item 8 — S2(ii) marker | C, carried with SC-8 (K2-F4) | IN SCOPE (integrity) | J1 §5(e) row 126; R23; H1 §(iii) item 10 (its open question is answered by item 8) | The README clause of item 3 is left standing (author decision, SSF Part 3(ii)). |
| R36 | §11 gap after line 1054 (item 7), and the list items 1–7 as a list | INSERTION — **item 8** (the freeze indexed from §11; the hash set read from the tag message's own enumeration) + MARKER "§11 items 1–7 — v30a, EXTENDED" (SC-8's M2, revised: the "R23" drafting identifier resolved to "item 8") | A1368 (item 8); A1372 (marker) | **SC-8** insertion point 2 — S2(ii) (SSF Part 3(ii)) | C, carried with SC-8 (K2-F4) | IN SCOPE (integrity) | J1 §5(e); R23; SC-8(f); H-L13 | Author decisions: item 8's genus (`tests/registration/` file by file?), item 3's README clause (SSF Part 3(ii)). |

### Part B — registered surfaces NAMED in v30a marker text but NOT touched (not counted anywhere below)

| Registered surface | Named by | What is said of it | Status |
|---|---|---|---|
| §6.2 line 446 — ground-truth column DAG, count of independently leaking sources | SC-4's marker (A604); H1 §(iii) item 1 | "NOT AMENDED. The manifest requirement stands; only the *arithmetic role* of what it records is constrained" | OUT OF SCOPE — untouched |
| §6.2 line 449 — the semantic-ambiguity clause | SC-13a's marker (A1295); K1 F-1 (row 28) | cited as "§6.2 line 449's ambiguity branch"; K1 F-1: row 28 is closable only by an explicit class C amendment of line 449 — **not made by v30a** | OUT OF SCOPE — untouched; F-1 open (closes by decision) |
| §10.2 lines 1031, 1033, 1035 — the branch sentence, the obligation, the floor | SC-13a's marker (A1297) | "NOT SUPERSEDED, stated so the marker's scope cannot be widened by reading" | OUT OF SCOPE — untouched (line 1035 is the anchor SC-12/13b/13c insert after) |
| §7.2.1 line 818 — the rationale for line 816's suppression | §AB (A51); SC-13c(c2) | "stands as registered"; the exception "does not rely on `PREREG.md` line 818" | OUT OF SCOPE — untouched |
| §7.4 line 830 — scope-eligibility | §AB (A41–A53); §13c-P (A1033) | the 816/830 duplicated-authority conflict "NOT resolved by this amendment … flagged for a future class C amendment" | OUT OF SCOPE — untouched; conflict open |
| §7.1 lines 759, 760; §10.2 line 1039 — the runtime metric rows and "both of L2a/L3.1's combinations" | SC-12's governed-set paragraph (A1313); SC-13c(c3) (A1339) | the governed set is pinned by citation to these three sites | OUT OF SCOPE — cited, untouched |
| §6.1 line 441 — "The fixture's AUC figures are provenance …" | H1 §(iii) item 16 | "Untouched and still exactly true of a recomputed anchor"; SC-10 is inserted *after* it (R10) | OUT OF SCOPE — untouched |
| §0.1 lock table | H1 §(iii) item 11 | no row added; SC-4's partition rule "is arguably lock-table material" | OUT OF SCOPE — open structural question |
| §0.3 line 117 — Claim A's historical parenthetical naming criterion 3 | H1 §(iii) item 17 | a ledger note, excluded from the normative scan by §6.8's rule | OUT OF SCOPE — untouched |

---

## 4. DERIVED COUNTS — EACH READ OFF THE TABLE ABOVE, NONE ASSERTED INDEPENDENTLY

Every number below is obtained by counting rows of Part A by their columns. None is a count stated
anywhere else and re-asserted here.

**D1 — Registered lines whose text is superseded** (Kind = SUPERSESSION or CONSEQUENTIAL): rows R11,
R12, R13, R16, R23, R29, R30, R31 — **8 registered lines**, derived from the table above. Of these:
**5** unconditional supersessions with the v30 text retained verbatim at the site (445, 450, 451, 461,
855); **1** conditional supersession with the v30 text retained verbatim and still operative off the
branch (1030); **2** consequential one-line rewrites whose v30 text is **not** retained as applied (992,
1022 — K2-F1). Excluding the two consequentials: **6**.

**D2 — Registered surfaces standing byte-exact whose reading is extended or partly superseded by a
marker** (Kind = MARKER only, MARKER + POINTER, or POINTER at a registered line): rows R04, R06, R07,
R09, R15, R20, R22, R27, R35 — **9 surfaces**, derived from the table above; **10 marker texts** counting
R36's "§11 items 1–7 — EXTENDED" marker, which shares R36's site with item 8.

**D3 — New schema clause texts inserted** (rows whose "Clause responsible" is an SC tag and whose kind
includes insertion of clause text): R05 (SC-9), R08 (SC-1), R10 (SC-10), R14 (SC-2), R16 (SC-3),
R17 (SC-4), R18 (SC-5), R19 (SC-7), R21 (SC-8), R24 (SC-6), R26 (SC-11), R31 (SC-13a), R32 (SC-12),
R33 (SC-13b), R34 (SC-13c) — **15 clause texts**, derived from the table above; **13** of them at pure
insertion sites and **2** (SC-3, SC-13a) at superseded lines. SC-13a, SC-13b and SC-13c declare
themselves "one class C amendment … adopted together" (SSF SC-13a REGISTERS), so by *amendment* rather
than by *text* the clause count is **13**.

**D4 — Other inserted texts** (derived from the table above): integrity item — **1** (R36, §11 item 8);
pointers — **4** (R22 §13c-P, R25 H8, R27 S2(i), R28 S2(iii)); record/navigation — **3** (R01 H1a, R02
H1b, R03 §AB).

**D5 — Surfaces, rows, sites** (derived from the table above): **36 object-rows**; **31 distinct
registered surfaces** (rows sharing one surface: R02/R03; R17/R18; R24/R25; R32/R33/R34); **25 physical
diff sites** in pristine → applied (`_K2_diff_pristine_vs_applied.txt`; difflib merges adjacent objects
into one hunk — the CI run reported 30 hunks for its own application order, and a hunk count depends
on the diff algorithm and the application order, so it is a count of nothing registered and is
recorded here only so no one re-derives a "30" or a "25" as an amendment count).

**D6 — Class C changes.** The count depends on the unit, and the table makes each unit derivable:

| Unit | Rows counted | Count (derived from the table above) |
|---|---|---|
| registered lines superseded (D1) | R11, R12, R13, R16, R23, R29, R30, R31 | **8** (6 substantive + 2 consequential) |
| class-C-bearing objects — schema clause texts | D3's fifteen | **15** (13 amendments, SC-13a/b/c as one) |
| class-C-bearing objects — instance-bearing supersessions with no clause of their own (SC-2 is their schema layer) | R11, R12, R13 (H2, H3, H4) | **3** |
| class-C-bearing objects — consequential rewrites | R29, R30 | **2** |
| class-C-bearing objects — integrity item whose class is the author's call (K2-F4) | R36 (item 8, with R04/R35 markers) | **1** |
| **class-C-bearing objects, all units above** | | **21** by clause text; **19** with SC-13a/b/c as one; **18** of those if R7's class A call stands for item 8; **16** of those excluding the consequentials |
| marker-only rows that carry no class of their own (ride with a clause) | R04, R06, R07, R09, R15, R20, R27, R35 (+ R36's marker) | **0** additional — R07 is class C on line 93's "unit" but is SC-1(d)'s own limb, not a separate change |
| rows with no class (record, pointer) | R01, R02, R03, R22 (pointer part), R25, R28 | **0** |

**No one numeral is "the number of class C changes".** That is the reason §8's block states none.

---

## 5. RECONCILIATION OF THE FOUR LEGACY NUMBERS TO THE TABLE

| Legacy numeral | = which rows of Part A | What it was counting | Why it differs from the others |
|---|---|---|---|
| **four** (decl. §A.11 L1516, L1520) | R11, R12, R13, R16 | the registered **§6.2 lines** the §A walk marked AMENDED (445, 450, 451, 461) — *sites, walk scope* | Walk scope is §6.2 only, so §10.2's "waived" (§A.12, R32) is outside it; the denominator rule (R17) is excluded because §A.11 L1508 marks criterion 1 **SATISFIED** with the denominator re-derived (R11), not AMENDED; 855 (R23), 1030 (R31), 992/1022 (R29/R30) and every schema clause post-date the walk. It is D1 restricted to §6.2 and to the walk's own markings. |
| **five** (decl. §D.1 item 5 L3399–3403) | R11, R12, R13, R16, R32 | the **amendment-content sections of the declaration** frozen at §D.1 item 5 (§A.1, §A.3, §A.4, §A.8, §A.12) — *objects, declaration scope* | Adds §A.12 ("waived") to the four because §D.1 freezes amendment *content* wherever it sits; still excludes the denominator because §D.1 freezes it under **item 2** as the enumeration/partition, not under item 5 as an amendment; knows nothing of the schema pass. |
| **six** (H1a/H1b, applied A8, A17, A37; DIFF L78, L104–131) | R11, R12, R13, R16, R17, R32 | H1's **class C hunks** H2–H7 — *"clauses amended" at H1's drafting* | Adds the denominator rule (H6 = R17) because H1 counts what it *adds to `PREREG.md`*, and the partition rule is added text even though the walk marks criterion 1 SATISFIED; excludes C1/C2 (R29/R30: "consequential, author adjudication"), H8 (R25: pointer), and everything the schema pass produced afterwards (SC-1, SC-2, SC-5 … SC-11, SC-13a–c, item 8). |
| **fifteen** (SSF closing tally) | R05, R08, R10, R14, R16, R17, R18, R19, R21, R24, R26, R31, R32, R33, R34 | **schema clause texts** SC-1 … SC-12, SC-13a, SC-13b, SC-13c — *clauses, not surfaces* | It counts texts, not changes: SC-3 and SC-13a are *also* supersessions (R16, R31); SC-13a/b/c are one amendment by their own text; H2/H3/H4 (R11–R13) are supersessions it does **not** count because SC-2 layers over them without replacing them; item 8 (R36), the four pointers, C1/C2 and the record block are outside it. |

**Overlaps, read off the rows:** six ∩ fifteen = {R16, R17, R32} (SC-3 carries H5's structure; SC-4
carries H6's placement; SC-12 carries H7's drafting basis). six \ fifteen = {R11, R12, R13} — the three
instance-bearing supersessions whose schema layer is SC-2. fifteen \ six = the twelve clauses J1/K1
produced. In none of the four = {R29, R30} (consequential), {R36} (item 8), {R23} (the 855 row, inside
SC-6), every marker-only row, every pointer, and the record block.

**Why they drifted apart (H-L13's shape, third venue).** Each numeral is a literal that was correct for
the set as it stood where and when it was written — the walk's §6.2 table, the declaration's freeze
list, H1's hunk table, the schema set's closing tally — and each sits outside the edit that later grew
the set. The declaration's "four" and "five" will go stale again when K4 lands unless the declaration
*cites* the amendments block's enumeration instead of restating a count (K2-F5); the applied `PREREG.md`'s
"six" is replaced by §8's enumeration, which states no numeral; "fifteen" is a scratchpad tally and
binds nothing.

---

## 6. CROSS-CHECK: APPLIED SCRATCH ↔ CLAUSE INSERTION POINTS, BOTH DIRECTIONS

**(a) Every surface in the applied scratch `PREREG.md` traced to a stated source.** All 25 diff hunks
(`_K2_diff_pristine_vs_applied.txt`) map onto rows R01–R36; none is unaccounted for. Two applied
surfaces are **not** stated in any SC clause's INSERTION POINT or SUPERSESSION MARKER: **R01 (H1a) and
R02 (H1b)** — they are H1's record/navigation hunks (`PREREG_v30a_DIFF.md` H1a, H1b), applied by the CI
run, and they are the very text S4 replaces. Not a defect; recorded as **K2-O1**. Everything else traces
to an SC clause's INSERTION POINT, SUPERSESSION MARKER, INSERTION TEXT, §13c-P or §AB, or to H1's
H2/H3/H4/H5/H6/H7/H8/C1/C2 as cited by an SC clause's marker (SC-2 cites H2/H3/H4/C1; SC-3 cites
H5/C2; SC-4 cites H6; SC-12 cites H7/H8).

**(b) Every clause-stated insertion point, marker and insertion text present in the applied scratch.**
SC-1: §2.9 after 266 (R08), markers 205 (R06) and 220–222 (R07) — present. SC-2: after 451 (R14); its
cited H2/H3/H4/C1 (R11/R12/R13/R29) — present. SC-3: replaces 461 (R16); cited C2 (R30) — present.
SC-4: after 464 (R17); marker 459/446 (R15) — present. SC-5 (R18), SC-7 (R19) — present. SC-6: 855 row
(R23), semantics after 856 (R24), 915 marker + S2(i) (R27) — present. SC-8: after 480 with marker
(R20/R21); §11 item 8 + item-3 marker + line-97 marker + items-1–7 marker (R36/R35/R04) — present.
SC-9 (R05), SC-10 with its 431 marker (R10/R09), SC-11 after 892 (R26) + S2(iii) (R28) — present.
SC-12 after 1035 (R32) + H8 pointer (R25) — present. SC-13a replaces 1030 (R31); SC-13b (R33); SC-13c
(R34) + §13c-P after 816 (R22) — present. §AB (R03) — present. **No stated insertion point is missing
from the applied file; no applied surface lacks a stated source.** Two placement choices the CI run made
that SSF does not fix are recorded: SC-1's two markers (R06 after line 213; R07 after line 220 — K2-O2,
K2-O3).

---

## 7. FINDINGS AND OBSERVATIONS

**K2-F1 — C1 and C2 delete registered sentences; the amendments block says none is deleted.** Applied
lines A1247 and A1277 rewrite pristine lines 992 and 1022 one-for-one, and the v30 text of neither is
retained anywhere in the applied file — "both fixture AUCs reproduce within ±0.010, full and sliced"
occurs nowhere; "is silent on `fixture_corrected`" survives only as a three-word fragment inside SC-3's
marker (A599). The amendments block's item 1 (A23) reads "**No registered sentence is deleted from this
file.**", and every other supersession (R11, R12, R13, R16, R23, R31) retains its v30 text verbatim at
its site. H1 drafted C1/C2 as bare replacements (`PREREG_v30a_DIFF.md` lines 413–417, 435–439) while
flagging them for author adjudication. **Fix, drafted and verified CI-neutral in §9:** a `SUPERSEDED BY
v30a` retention block at each site, in the form H2–H5 use. Until it is applied, §8's block sentence
"No registered sentence is deleted from this file" is false of the scratch file. Alternative the author
may prefer: reject C1/C2 and leave 992/1022 as registered (H1's stated alternative; then the Phase 1
gate and the kill gate keep requirements that read on retired objects — H1 records why it does not
recommend this).

**K2-F2 — Stale numerals in the applied v30a text itself.** "Six class C changes" (A8), "six class C
changes" (A17), "**All six are class C**" (A37), the six-row table (A28–A35), and "amendment 3" (A39 —
a table-index reference, the same fragility). These undercount the amendment (CI report §7 obs. 1; SSF
Part 6 item 2(b)). **Fixed by §8** — the replacement block states no numeral and refers to the
sliced-variant row by surface, not by index. After §8 is applied, the only "fifteen" left in the file is
the registered v30 sentence at §6.6 ("Ten of fifteen", **pristine line 596 = applied line 811** — a
product-space count over the schedule-state × evidence-outcome table, unrelated), verified by grep on
the applied file and on the verify copy. *(Line number corrected on re-verification: an earlier draft of
this finding cited "pristine line 808", which is the feature-cohort-precision definition and carries no
"fifteen". The finding is unaffected — only its citation was wrong — and is recorded because a wrong line
number in a ledger whose whole purpose is line-accurate citation is the defect class this item exists to
remove.)*

**K2-F3 — Drafting identifiers in applied marker text, carried open from SSF Part 6 item 2(a), not
closed here.** A524 (R09): "The alternative — adding a sixth row — is named in **F-5** and is the
author's call." A599 (R16): "**Consequential — §10.1 line 1022** (**H1 C2**): …". Proposed one-line
replacements, drafted not applied: A524 → "… The alternative — amending §6.1's heading and adding a
sixth row to its table — is the author's call and is recorded as open."; A599 → "**Consequential —
§10.1 line 1022:** the kill gate carries a second copy of the retired premise ("silent on
`fixture_corrected`") and is amended with this clause, or `PREREG.md` holds both readings at once." (The
second also updates "must be amended" → "is amended", since C2 is applied in the scratch.)

**K2-F4 — The class of the hash-set items (R04, R35, R36) is an author decision, flagged not made.**
Working resolution R7 (decl. line 3664, cited by H1 §(iii) item 10) recorded the hash count as "a class
A mechanical fact requiring no locked-file edit"; J1 §5(e) and R23 direct amending lines 97 and 1050 so
the count is derived; item 8 is that edit. An edit to registered text travels with the amended tag
whatever its class, and on line 93's test it changes no published number's meaning. The table marks
these rows "C, carried with SC-8"; if the author holds R7's class A call, the three Class cells change
and nothing else in the table or in §8 moves (the block's (b) and (c) rows say "C, carried with SC-8"
— edit those cells in the same way).

**K2-F5 — The declaration's own counts ("Four amendments" at §A.11 L1516/L1520; "The four §6.2
amendments and the §10.2 definition" at §D.1 item 5) are K4's to reconcile, not PREREG's.** They are
correct on their units (§5) and stale against the ledger. Recommended disposition for K4 (S7): have §A.11
and §D.1 item 5 *cite* `PREREG.md`'s v30a amendments block as the enumeration of what is amended and
state their own scope ("the §6.2 elements this walk marks AMENDED", "the amendment content this
declaration carries") without a count — H-L13's open-form fix. Not drafted here: the declaration is
outside S4's remit and K4 is live in another item.

> **Disposition on re-verification: HALF DISCHARGED by the live K4 pass, and the half that remains is
> the one that matters more.** K4 has since written `applied\AVAILABILITY_DECLARATION.md`
> (`ddbf7f2d…48d6`, 3,796 lines, still moving — K2-F7). In that copy:
>
> - **§A.11 is fixed, in exactly the recommended form.** Working-tree L1516–1521 ("**Four amendments
>   (445, 450, 451, 461).** … All four amendments are class C under PREREG.md line 93 and are carried by
>   this registration under line 95") now reads (scratch L1599–1607): "**Four §6.2 sites are amended in
>   this walk (445, 450, 451, 461). The ledger of record for what the amendment comprises is the amended
>   registration's own v30a amendments block (`PREREG.md`); this table is a walk summary, not that ledger
>   (`PRACTICES.md` P-61).**" — the numeral is **scoped to its unit** (§6.2 sites, this walk), the block is
>   named as the ledger of record, and the count-bearing class sentence is gone, replaced by "The class of
>   each amendment is `PREREG.md` §0.2.1 line 93's and it is carried under line 95." That is the open-form
>   fix, and it is the disposition §5 says the "four" needs: a number correct on a named unit, subordinated
>   to the enumeration. `PRACTICES.md` P-61 ("A walk summary is not the amendment ledger") exists and is
>   the cited practice — but note R21: `PRACTICES.md` binds nothing, so the citation is a pointer to a
>   rationale, not to an authority, and §A.11 does not depend on it.
> - **§D.1 item 5 is unchanged** — scratch L3511 still reads "**The four §6.2 amendments and the §10.2
>   definition**, as written", word for word as at working-tree L3399. This is the "five" of §1's table
>   (four + one, stated as a phrase rather than a numeral), it is a **freeze list** rather than a walk
>   summary, and it is the harder of the two: a freeze list that enumerates by count silently stops
>   freezing whatever the count omits. It omits the denominator rule (R17) and every schema clause. The
>   recommendation stands for it unchanged — have item 5 freeze "the amendment content this declaration
>   carries, section by section" and name the sections (§A.1, §A.3, §A.4, §A.8, §A.12), which is what it
>   already does after the phrase; deleting the four words "The four §6.2 amendments and" and letting the
>   §-list carry it would suffice.
>
> **Still not drafted here**, and deliberately: the declaration is outside S4's remit, K4 owns it, and K4
> is writing that file as this is recorded. This note is a finding for K4, not an edit.

**K2-F6 — SC-10's marker says "AMENDED IN FORM" of a heading and table that are byte-identical.** R09 is
a marker-only supersession of an *implication* (exhaustiveness); the heading "Five bodies of data" still
reads as closed. K1 F-5 leaves the choice (sixth row vs. SC-10 as drafted) to the author; SSF Part 6
item 2(c) carries it open. Recorded here because "AMENDED IN FORM" could be misread as an edit of line
431; the table says what actually happened (nothing at line 431; a marker after line 441).

**K2-F7 — `applied\` is being written by another item while this ledger cites it; `PREREG.md` is not
the file that moved.** At re-verification `applied\AVAILABILITY_DECLARATION.md` had gone from
`1290186e…1c30` (3,695 lines) to `ddbf7f2d…48d6` (3,796 lines, +101) with a `_DECL_preK4.md.bak` written
beside it, and `CI_GATE_RESULT.md` had been removed from that directory — K4 (item S7) is mid-pass, and
the file was still being written as this was recorded. **Nothing in this ledger moves**, and the reason
is worth stating rather than assuming: `applied\PREREG.md` is byte-unchanged at `e7ab52d3…1706`, 1,417
lines (re-hashed at the end of this pass), so every "Applied lines" cell, the 25-hunk diff, §6's
both-directions cross-check and §8.3's CI record all stand; and every declaration citation in this file
is **working-tree** numbering (`f0829bd3…3310`, 3,684 lines — re-hashed, unchanged), which no scratch
pass touches. **Two consequences for whoever reads this next.** (i) The `1290186e…1c30` state is no longer
reachable as `applied\AVAILABILITY_DECLARATION.md`; cite `applied\_DECL_preK4.md.bak` for it. (ii) §8.3's
CI record was taken against the `1290186e…` declaration; the 11 `single_source` findings are findings on
the **declaration**, so a K4 that scrubs them will change that number — downward, and by design (that is
what K4's scrub list is for). §8.3's claim is a **delta** claim (+0/−0 findings from applying §8.1+§8.2+§9
to `PREREG.md`), not a claim that 11 is the standing count, and the delta is unaffected by K4. Anyone
re-running it after K4 lands should expect a different absolute count and the same delta.

**K2-O1** — R01/R02 are the only applied surfaces with no SC-clause source (they are H1's record hunks
and the object of this item). **K2-O2** — SSF fixes no placement for SC-1's two markers; the CI run put
R06 after the §2.3 table (line 213) and R07 after the formula (line 220); both read correctly where they
are. **K2-O3** — R07's marker sits inside the 220–222 range it names (between the formula and the
bullets); cosmetic. **K2-O4** — SC-13a's marker (A1299) says line 1022 "is **not** amended by these
clauses" while C2 (R30) does amend it under SC-3; both statements are true and the table's R30 row
says so; a reader of A1299 alone could infer line 1022 is unamended — consider appending "(it is amended
consequentially under §6.2 criterion 3 as amended — see the v30a amendments block)" to A1299.
**K2-O5** — R27's S2(i) pointer has the one disclosed scope consequence (the closing sentence's open-form
range reaches `waived`); the block of §8 describes (d)'s pointers as adding "no rule of their own",
which is SSF's own characterisation; if the author keeps the open-form scope the description stands as
SSF states it, and if the author strikes the final clause of S2(i) (SSF Part 3(i) offers this) nothing
in §8 changes.

**K2-O6** — the block text of §8 does contain one numeral about itself: "**Two** passes produced them", in its opening paragraph. It is a count of the two production passes (the §A walk; the R24/R25 schema pass), not of changes, and it is self-enumerated in the two sentences immediately after it ("The first is … The second is …"), so it cannot go stale silently the way a change-count can. It is recorded because H-L13's rule is about *shape*, not subject matter: if a third pass ever contributes clauses, that word is the one place in the block that must be re-bumped. The zero-maintenance form is "Each row names the pass that produced it", followed by the same two sentences — a one-word change the author may take or leave. **K2-O7** — the declaration uses "four" in a **second, unrelated sense** that neither §1's table nor §5 counts: working-tree L455, "§6.2's four criteria as amended in §A are the whole gate" (K4 rewords it to "§A walks the four §6.2 criteria as amended", scratch L467). That "four" is criteria 1–4 at lines 459–462, of which the amendment touches one (461, R16) and marks one (459, R15). It is correct, it is not a stale count, and it is adjacent in the same document to "four amendments" — which is precisely why it is recorded: a reader reconciling counts will meet it, and it is not a fifth answer to §1's question. If §D.1 item 5 is opened under K2-F5, disambiguating this line in the same pass ("§6.2's four acceptance criteria") costs one word.

---

## 8. THE v30a AMENDMENTS BLOCK TEXT — ENUMERATION-FIRST, NUMERAL-FREE (replaces H1a and H1b; keeps §AB)

**Scope of the replacement.** (i) Applied line 8 (H1a, R01) is replaced by the one line in §8.1. (ii)
Applied lines 15–39 (H1b proper, R02 — from the heading "## v30a amendments (class C under §0.2.1)"
through the paragraph beginning "**What an amendment may not do**") are replaced by the block in §8.2.
(iii) Applied lines 41–53 (§AB, R03 — "**RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT …**" through
"… cannot settle a disagreement between two registered lines.") are **kept byte-exact** and follow the
block after one blank line, as now. The heading is left un-numbered so `sections_of()` gains no section
(H1's verification fact 4); line 6 is untouched so `_prereg_version()` still reads 30 (fact 2). The text
below is byte-identical to `_K2_BLOCK_TEXT.md`, the file the verification applier read, and to
`_K2_BLOCK_TEXT_as_applied.md`, what it wrote — checked programmatically this pass.

**How it survives a further clause.** Every count in it is read from its own enumeration — adding a
clause adds one row to (a), (b), (c) or (d) and changes no sentence; the closing paragraph says "those
in (a) and no others" and "their number is read from the enumeration and is stated nowhere as a
numeral". The sliced-variant element is referred to by its row, not by an index. Line numbers are
pristine v30 anchors, not counts.

**Dependency.** The block's item 1 ("No registered sentence is deleted from this file") is true of the
scratch only once the K2-F1 retention blocks of §9 are applied (or C1/C2 are rejected). §8.3 verifies
both together.

### 8.1 The status line (replaces applied line 8)

```
**Amendment status:** **v30a — this file is amended.** The class C changes under §0.2.1 are enumerated, by registered surface and clause, in the v30a amendments block below; their number is read from that enumeration and is stated nowhere as a numeral. The v30 text of every superseded clause is retained inline at its site, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text byte-exact.
```

### 8.2 The block (replaces applied lines 15–39; §AB at applied lines 41–53 follows unchanged)

<!-- K2-BLOCK-BEGIN -->
## v30a amendments (class C under §0.2.1)

**What this block is.** `prereg-v30a` is an **amended registration, not a restart** (§0.2.1, line 95). It carries the class C changes enumerated below — every registered surface this amendment touches, by section and v30 line, with the clause responsible — and no others. Two passes produced them, and each row names its source. The first is the element-by-element conformance walk of the acceptance fixture's reconstructed availability declaration against §6.2 (`AVAILABILITY_DECLARATION.md` §A), which superseded registered text at instance-bearing lines. The second is the schema pass over that walk's findings, which registered in this file the kind of object each gate input is, what a declaration must supply for it, and what the gate does with it — under §0.2.1's single-normative-source rule. The declaration is the reconstructed declaration §6.2 already requires and the carrier of this fixture's evidence. **It is not a normative annex and may not be cited as one.** Measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule). What lives there is this fixture's *instances*: its identity, its measured ground-truth map, its reference-anchor values, its evidence, its documented-unverifiable assumptions, and the per-unit enumerations these rules yield for it.

**The test applied to every sentence below, so the split is checkable rather than asserted:** *would this still be true for a different fixture?* If yes it is a **rule** and it is here. If no it is an **instance** and it is in the declaration.

**How the amendment is written, so nothing is lost.**

1. **Where registered text is superseded, the v30 text is retained inline, verbatim, at its own site, in a block marked `SUPERSEDED BY v30a` and marked NOT operative.** No registered sentence is deleted from this file. Where a registered sentence stands byte-exact and only its reading, its count, or its assumed scope is changed, a marker at its site states exactly what is superseded and what stands.
2. **Each amended or extended clause carries an inline marker naming v30a**, and the new normative text sits beside the old. New clauses carry the tag `[SC-n]` in their heading; a citation "SC-n" anywhere in this file means the clause whose heading carries that tag, and "SC-n(x)" its lettered limb.
3. **The registered text is recoverable byte-exact independently of this file: `git show prereg-v30:PREREG.md`.** The retained inline copies are a reading convenience; the signed `prereg-v30` tag is the record. Every line number in this block and in every v30a marker is a line number of that registered text.
4. **This amendment inherits §11's integrity chain in full** (§0.2.1, line 97): signed tag; the SHA-256, as committed, of every registered document and registration tool, enumerated in the tag message (§11 item 8); external timestamp receipt committed; repository publicly reachable at lock.

**The enumeration — one row per registered surface touched.** *Superseded*: the registered text at that line is replaced by operative v30a text and retained verbatim beside it. *Marker*: the registered text stands byte-exact and a v30a marker at its site states what reading is superseded or extended. *Inserted*: new text at a site where no registered sentence is replaced. *Pointer*: a cross-reference that adds no rule of its own. Class is §0.2.1 line 93's.

**(a) Registered text superseded — each retained verbatim at its site, NOT operative:**

| Registered surface (v30 line) | Touch | Operative v30a text · clause | Class | Justification |
|---|---|---|---|---|
| §6.2 line 445 — reference AUC anchor | superseded | operative clause at its site; schema SC-2(d) | C | declaration §A.1 |
| §6.2 line 450 — contamination availability class | superseded | operative clause at its site; schema SC-2, SC-9(b) | C | declaration §A.3 |
| §6.2 line 451 — sliced variant for CI | superseded | operative clause at its site; schema SC-2(e), SC-3(f) | C | declaration §A.4 |
| §6.2 line 461 — acceptance criterion 3 | superseded | SC-3 | C | declaration §A.8; working resolution R9 |
| §7.7 line 855 — detector-case coverage row | superseded: the row is re-registered with `unscored` | SC-6 | C — line 93's "coverage state" | schema pass over the walk of the reconstructed declaration against §6.2 |
| §10.2 line 1030 — kill/pause criterion 2 | superseded on the ambiguity branch only; operative where the branch has not fired | SC-13a, with SC-13b and SC-13c | C | line 1033's obligation, unmet by the §6.2 acceptance amendment alone |
| §10 line 992 — Phase 1 gate cell | superseded, consequential to lines 445 and 451 | operative row at its site | C (consequential) | derived from §A.1 and §A.4; not walk-cited |
| §10.1 line 1022 — kill-gate criterion 3 | superseded, consequential to line 461 | operative item at its site | C (consequential) | derived from §A.8; not walk-cited |
| §8.3 line 929 — `assert_audit_complete()` failure set | superseded: `waived` joins `unsupported` and `could_not_run` | operative bullet at its site; carried with SC-12(w) | C — line 93's "coverage state" | schema pass; the prohibition SC-12(w) registers |

**(b) Registered text standing byte-exact, its reading extended or partly superseded by a marker at its site:**

| Registered surface (v30 line) | What the marker states | Clause | Class |
|---|---|---|---|
| §0.2.1 line 97 — "both file hashes" | superseded as a count, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8 |
| §2.3 line 205 — `column_roles` | added, not superseded: a role is a position, not an availability instant | SC-1(c) | carried with SC-1 |
| §2.4 lines 220–222 — the label-availability formula | partially superseded: the unstated assumption that the horizon term's unit is a duration | SC-1(d) | C — line 93's "unit" |
| §6.1 line 431 — the five-bodies heading and table | amended in form: the implication that the enumeration is exhaustive | SC-10 | carried with SC-10 |
| §6.2 line 459 — criterion 1 | added, not superseded: the inference that the denominator is a construction-taxonomy count | SC-4 | carried with SC-4 |
| §6.2 line 480 — ordering, locked | extended: what the ordering ranges over, and what happens when a frozen object is found wrong | SC-8 | carried with SC-8 |
| §7.2.1 line 816 — the `not_applicable`-everywhere suppression | an express, scoped exception for one criterion's required quantities; the sentence governs as registered everywhere else | SC-13c(c2) | C — how line 816 reads at one criterion |
| §8.2 line 915 — not-run states | extended: `unscored` is governed by this section's closing sentence, by reference to §7.7's row | SC-6 | carried with SC-6 |
| §11 item 3 (line 1050) — the hashed files | superseded as a file set, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8 |
| §11 items 1–7 | extended by item 8 | SC-8 | carried with SC-8 |

**(c) New clauses inserted — no registered sentence replaced at the site:**

| Site (after v30 line) | Clause | Registers | Class | Justification |
|---|---|---|---|---|
| §0.2.1, after line 99 | SC-9 | integrity of a declared instance: what a declaration may not create, evidence never adjusted, obligations discharged only by being met or amended, working-resolution authority and supersession order, the stronger-reading interpretation rule, one normative copy | C | the same schema pass, registering the integrity limbs and the stronger-reading interpretation rule as one clause |
| §2, after line 266 (new §2.9) | SC-1 | the declaration as the gate's semantic authority: measured not intended, the representation named, roles are positions, units declared, staleness is not unavailability, one comparator branch scored | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.1, after line 441 | SC-10 | declared non-gated data, diagnostic classes, and the forbidden uses of non-gate data | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 451 | SC-2 | the acceptance fixture's composition, what may move, the pre/post licence, reference anchors by recomputation, moves between phases | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 464 | SC-4 | the criterion-1 denominator and the three-class partition rule: registered predicates, precedence, edge readings, exclusion grounds, publication discipline | C | declaration §A.6, §A.6.0–§A.6.4, §A.10; working resolution R11 |
| §6.2, after line 464, following SC-4 | SC-5 | adjudication routing: one criterion per finding, attribution to the ground, the false-positive class, detector jurisdiction, declared sentinels | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 468 | SC-7 | the gate's input surface and the one-side-at-a-time sequencing rule | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §6.2, after line 480 | SC-8 | the freeze: what freezes, in what form, checkable before any run, no number corrected in place, the integrity chain | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §7.7, after the table (line 856) | SC-6 | `unscored`: a coverage state with its semantics, entry condition, two levels, and gate consequences | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §7.8, after line 892 | SC-11 | the all-zero control over every empty aggregate and every pass claim | C | schema pass over the walk of the reconstructed declaration against §6.2 |
| §10.2, after line 1035 | SC-12 | "waived", defined; which detectors the floor governs; what the definition does not permit; and **SC-12(w)** — the entry condition for §7.7's `waived` coverage state: a prohibition with a closed and empty list of licensed grounds, the rule that the state records a waiver and never makes one, and the report's duty to publish the count | C | declaration §A.12; schema pass |
| §10.2, after line 1035, following SC-12 | SC-13b | admissibility for the ambiguity-branch criterion, and the disposition of every degenerate state | C | one amendment with SC-13a |
| §10.2, after line 1035, following SC-13b | SC-13c | that criterion's interactions: the one-way dependency on amended criterion 3, the line-816 exception, the pinned governed set, the floor limbs carried by citation | C | one amendment with SC-13a |
| §11, after item 7 (line 1054) | item 8 | the freeze indexed from §11, and the hash set read from the tag message's own enumeration | C, carried with SC-8 | the open-form discipline for the hash-count enumeration (`HISTORY.md` H-L13) |

**(d) Pointers — cross-references that add no rule of their own:** §7.2.1 after line 816 (to the exception SC-13c(c2) states); §7.7 after the table (`waived` is defined in §10.2; **SC-12(w)** is its entry condition); §8.2 after line 915 (`unscored` under this section's closing sentence, by reference to §7.7's row); §8.6 after line 961 (a zero, an empty result, or an all-clean statement is a published number; SC-11 governs what it must survive and name).

**What this enumeration is, and what is read from it.** The registered lines this amendment supersedes are those in (a) and no others; the registered lines whose reading it extends are those in (b) and no others; the clauses it inserts are those in (c) and no others; the pointers are those in (d) and no others. **Their number is read from the enumeration and is stated nowhere as a numeral** — so that a further clause added under §0.2.1 adds a row here and changes no count anywhere in this file. Every change enumerated in (a), (b) and (c) is class C under §0.2.1 line 93 — each changes what a published number means, what an acceptance or kill criterion requires, or what the gate may consume, or is carried with the clause that does — and each is carried by this registration under line 95. None is a `DEVIATIONS.md` entry standing alone.

**What an amendment may not do, restated here because this is the first one.** It may not be weaker than the thing it amends (line 97). It may not convert an unmet element into a satisfied one by re-reading it. Where an element cannot be met as written at the instant the amendment must be committed, it is **amended explicitly, never waived and never left outstanding** — which is what the sliced-variant row of (a) does.
<!-- K2-BLOCK-END -->

*(Then one blank line, then §AB verbatim as at applied lines 41–53 — "**RECORDED DEFECT, NOT RESOLVED BY
THIS AMENDMENT — `PREREG.md` lines 816 and 830 hold duplicated, conflicting authority over one state.**"
through "… cannot settle a disagreement between two registered lines." — unchanged; then `---` and
"## 0. What this document is for".)*

### 8.3 CI verification record — §8.1 + §8.2 + §9 applied together to `_K2_verify\PREREG.md`

| State | `PREREG.md` | Checker (`python tools/check_registration.py --stage prereg`) | Exit | Findings | pytest (`tests/registration -q -p no:cacheprovider`) |
|---|---|---|---|---|---|
| baseline (= `applied\` step C) | `e7ab52d3…1706`, 1,417 lines | 12 PASS / `single_source` FAIL | 1 | **11**, all on `AVAILABILITY_DECLARATION.md` (`1290186e…1c30`), byte-identical to SSF Part 2.4 step C | `1 failed, 136 passed` — `test_prereg_stage_on_real_repo_exits_zero` (the checker's exit-code wrapper) |
| after §8.1 + §8.2 + §9 | `fb171ed8…788bc`, 1,462 lines (+45: +42 block, +2 C1 retention, +1 C2 retention) | 12 PASS / `single_source` FAIL — stdout **identical** apart from the two `EXEMPTION APPLIED` note line numbers (REG15 495 → 537; PARK9 1415 → 1460), which move with the insertions above them and still bind to the line beneath | 1 | **11**, same detector, same quoted text | `1 failed, 136 passed` — the same one test |

Delta: **+0 findings, −0 findings**; every `PREREG.md`-reading check (`structure`, `config_schema`,
`lock_table`, `banned_vocabulary` — no banned term in the new text —, `deletion_certificate`,
`phase_arithmetic` — the retained row sits in a blockquote, so the `^\|\s*\*\*(\d)\*\*` row regex still
parses exactly 8 phase rows —, `requirement_ids`, `legality_table`, `parking_lot`, `reducer_functions`,
`unit_grammar`, `suppression_anchor`) **PASS**. The applier asserted match count **1** at every anchor
(H1a's full line; the block heading; the "What an amendment may not do" paragraph, span 24 lines; the
phase table's last row; §10.1 item 3's applied line with item 4 immediately beneath). Outputs:
`_K2_verify\_K2_baseline_checker.txt`, `_K2_after_checker.txt`, `_K2_baseline_pytest.txt`,
`_K2_after_pytest.txt`. The verify copy's declaration is the `1290186e…` state as found at copy time; K4
edits landing in `applied\` afterwards do not touch `PREREG.md` and do not affect this record.

---

## 9. THE K2-F1 FIX — C1/C2 RETENTION BLOCKS, DRAFTED, NOT APPLIED TO `applied\`, VERIFIED IN `_K2_verify\`

Form: the one H2–H5 use — operative text stands; beneath it a blockquote marked `SUPERSEDED BY v30a`
quoting the registered v30 line verbatim, marked NOT operative, with the retirement reason and the
recovery command. Each is entirely RULE (no fixture particular beyond what the registered line itself
names). Anchors are full-line matches in the applied file (count 1, asserted).

**9.1 — C1 (line 992).** The superseded object is a table row, so the retention cannot sit inside the
table without breaking it; it is placed immediately **after the phase table's last row** (pristine line
998, `| **7** | Profiles, docs, v1.0 | …`), blank line each side, before the weekend-total sentence at
pristine line 1000. The row is retained in full (Phase, Work, Est., Gate), so the retention is verbatim.
INSERT:

```

> **§10 line 992 (Phase 1 gate cell) — SUPERSEDED BY v30a, consequential to §6.2 lines 445 and 451. Registered v30 row, retained verbatim, NOT operative:** "| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |" *Retired because its Gate cell reads on two superseded objects: "both" names the retired anchor pair of line 445, and "sliced" names the artifact line 451 moves off the Phase 0 fixture and re-registers as a Phase 1 CI obligation. Only the Gate cell is changed in the operative row above; Phase, Work and Est. are byte-identical. Recover the registered row byte-exact with `git show prereg-v30:PREREG.md`.*

```

**9.2 — C2 (line 1022).** Placed directly beneath the operative item 3 of §10.1 (applied A1277), at the
list's three-space indentation, before item 4 — the placement SC-3's marker uses under §6.2 criterion 3.
INSERT (one line):

```
   > **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired because it is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. The ambiguity branch is carried through unchanged. Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

Verified together with §8 (§8.3): CI-neutral, 136/1. If the author instead **rejects** C1/C2 (H1's
alternative), lines 992 and 1022 revert to their registered text, the two "consequential" rows leave
(a) of the block, and the SC-2/SC-3 markers' "CONSEQUENTIAL" notes are struck — nothing else moves.

---

## 10. AUTHOR DECISIONS THIS PASS SURFACES, AND LIMITS

1. **K2-F1** — apply the §9 retention blocks (recommended) or reject C1/C2; either makes the block's item
   1 true. 2. **K2-F4** — class of the hash-set items: "C, carried with SC-8" (as tabled) or R7's class
   A; three cells change. 3. **K2-F3 / K2-O4** — the drafting identifiers "F-5" and "(H1 **C2**)" in
   applied marker text, and the A1299 clarification; one-line edits drafted in §7. 4. **K2-F5** — the
   declaration's "four"/"five" to be made citations under K4, not here. 5. Everything SSF Part 6 carries
   open stands (C-1/C-2 on SC-4(c)/(d); the open-form scope of S2(i); item 8's genus; item 3's README
   clause; K1 F-1/F-5/F-8; the N4 residue; the 816/830 conflict; P7's items; the SC-12/SC-13c(c3) mirror).

**Limits.** Nothing was applied to `applied\` or to the repository; §8 and §9 were applied only to the
verification copy `_K2_verify\` under `amendment\`. The table's "Applied lines" are those of
`applied\PREREG.md` at `e7ab52d3…` and will shift if SSF's placement choices are revisited (SSF Part 6
item 5). Class assessments for the schema clauses follow §0.2.1 line 93's test as SSF and H1b apply it;
where a clause's class is by carriage rather than on line 93's face (SC-9, item 8), the table says so.
The declaration was read for its counts only; its line numbers are working-tree numbering with the +11
shift noted. The archive was not read; no git state was changed.
