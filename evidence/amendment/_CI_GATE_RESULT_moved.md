# ITEM K9/J9 — CI GATE RUN AGAINST THE APPLIED v30a SCHEMA SET (SCRATCH COPY ONLY)

**Nothing in the real repository was touched.** `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`
still reads HEAD `80401d0`, `git status --short` is unchanged from the start of the item
(` M AVAILABILITY_DECLARATION.md`, ` M DESIGN.md`, ` M tools/check_registration.py`, `?? .claude/`,
`?? LICENSE`, `?? evidence/`, `?? tagmsg.txt`), and `PREREG.md` there still hashes
`f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6` (1,099 lines). **No state-changing
git command was run** (only `git archive HEAD | tar -x`, `git status`, `git rev-parse`, `git diff --quiet`).
The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not read. `PREREG.md`,
`AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md` **in the repo** were not edited.

**Headline.** The schema set applied cleanly — **30 hunks, every anchor matched exactly once** both
against the pristine v30 file and at apply time; **no stop-and-report**. Against the applied text:
`python tools/check_registration.py --stage prereg` → **12 of 13 checks PASS, `single_source` FAIL with
the same 14 findings as before application, all on the still-unscrubbed `AVAILABILITY_DECLARATION.md`
(K4 not landed); exit 1** — byte-identical output apart from the two exemption-note line numbers.
`pytest tests/registration` → **136 passed, 1 failed** (the same one test as before application:
`test_prereg_stage_on_real_repo_exits_zero`, which wraps the checker's exit code). **The applied schema
text introduces zero new findings and breaks zero tests.** The verbatim-quote exemption gains **one**
covered declaration line (1549) and **eleven** declaration lines become verbatim-but-unattributed
copies of now-registered text (K4 targets). Applied scratch `PREREG.md`:
**sha256 `a0c899a48a8ffe5363611bd9c5f4e2d82529a1dc8b6413721d58b3da96032ef5`, 1,408 lines, LF-only.**

All work is under
`C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\applied\`
(referred to below as `applied\`).

---

## 0. The scratch copy — how it was built, and what it contains

| Step | Command / action | Result |
|---|---|---|
| Export HEAD read-only | `git archive HEAD \| tar -x -C applied\` (run in the live repo) | 24 tracked files; `PREREG.md` sha256 `f0a8f001…c7cc6`, 1,099 lines, LF-only (`.gitattributes` is `* -text`); `AVAILABILITY_DECLARATION.md` at HEAD = 3,650 lines |
| Copy in working-tree versions of the files that differ from HEAD | `cp` of the four named files | **Copied: `AVAILABILITY_DECLARATION.md`** (working tree, 3,684 lines, sha256 `f0829bd3…3310` — replaces the 3,650-line HEAD copy), **`DESIGN.md`** (`39a944c1…dcc00`), **`tools/check_registration.py`** (`30d3ad4c…7425`, the 1,062-line scope-by-exclusion version), **`LICENSE`** (`595cb9e7…248a8`, untracked at HEAD). Hashes verified equal to the live working tree after copy. |
| Not copied | `.claude/`, `evidence/`, `tagmsg.txt` | Untracked; not part of the four named files. `evidence/` is a `SINGLE_SOURCE_EXCLUDED_DIRS` entry in the checker, so its absence changes no scan. |
| Baseline runs (before any edit) | checker + pytest on the scratch copy | checker: FAIL, 1 check (`single_source`), 14 findings; pytest: 136 passed / 1 failed — i.e. the historical 137 = 136/1 figure. Outputs kept at `applied\_baseline_checker.txt`, `applied\_baseline_pytest.txt`. |

`PREREG.md` in the working tree equals HEAD (`git diff --quiet HEAD -- PREREG.md` → 0), so the scratch
`PREREG.md` is the registered v30 file.

---

## 1. (a) APPLICATION — what was applied, where, and every anchor's match count

### 1.1 What SCHEMA_SET_ADOPTION.md's own instructions were read to require

Read in full: `SCHEMA_SET_ADOPTION.md` (1,840 lines), `PREREG_v30a_DIFF.md` §(i) and `apply_v30a.py`
(H1's applier, whose anchor constants and hunk payloads H1a/H1b/H2/H3/H4/H8/C1/C2 were imported and
used verbatim), `K1_SCHEMA_CLAUSES.md` header/§0/§5 F-8–F-10/§7, `PREREG.md` at every anchor.

- **§0.2 of the adoption file:** only **THE CLAUSE** text and **SUPERSESSION MARKER** text placed at
  the superseded site enter `PREREG.md`; REGISTERS / INSERTION POINT / DATA / ROWS / *Instance record*
  are apparatus and were **not** applied.
- **§0 "Application order":** SC-12 (revised) → SC-13a → SC-13b → SC-13c → §13c-P → §AB is the fixed
  order; ascending anchor order for SC-1 … SC-11 is a suggestion and was followed. Anchors re-derived
  against the current text before every edit (H1's full-line convention; refuse on ≠ 1).
- **H1 hunks the set depends on** (applied as H1 wrote them, from `apply_v30a.py`): **H1a, H1b** (the
  amendment-status line and the v30a amendments block — §AB is "the amendments-block recording text"
  and has nowhere to go without H1b); **H2, H3, H4** (SC-2's supersession-marker section: "Their
  markers stand as H1 wrote them and are cited, not re-drafted: §6.2 line 445 … (H1 hunk H2) … line
  450 (H3) … line 451 (H4)"); **H8** (SC-12's insertion point: "plus the §7.7 pointer H1 drafts as
  hunk H8 after line 856"); **C1** (SC-2's marker: "§10 line 992 — CONSEQUENTIAL (H1 C1)"); **C2**
  (SC-3's marker: "§10.1 line 1022 (H1 C2) … must be amended with this clause or `PREREG.md` holds
  both readings at once").
- **H1 hunks NOT applied, by the set's own design:** **H5** (SC-3 "REPLACES `PREREG.md` line 461,
  carrying H1 hunk H5's structure … supersedes H5's"), **H6** (SC-4 "carrying H1 hunk H6's placement";
  K1 line 25: "Hunks H2, H3, H4, H5, H6, H7 are absorbed by clauses below"), **H7** (SC-12 "Carries
  H1 hunk H7 essentially unchanged … H7 text is compatible and is the drafting basis"). Applying H5/H6/H7
  beside SC-3/SC-4/SC-12 would put two normative copies of the same rule in `PREREG.md`.

### 1.2 Formatting decisions made at application (all CI-neutral; recorded so the author can compare)

1. **One blockquote level stripped from clause text.** The adoption file wraps every clause in `> `;
   H1's operative text is plain and K1's SC-12 nests its definition `> >` — so the outer `>` is the
   file's delimiter and the inner `>` is the PREREG-level blockquote. Marker text is applied **as** a
   blockquote (H1's convention for retained superseded text).
2. **Hard-wrapped lines re-flowed to PREREG.md house style** (one paragraph / list item / table row /
   nested-quote paragraph per line). **No word was changed**; only line breaks inside paragraphs. The
   checker's quote blob joins all lines with spaces, so wrapping cannot affect any check.
3. **Enumeration markers preserved:** SC-3's heading `**3. Runtime findings …**` applied as
   `3. **Runtime findings … [SC-3]**` with 3-space continuation (H5's structure); SC-13a's as
   `2. **Where the fixture … [SC-13a]**` (the adoption file says "preserving the enumeration's `2.`
   marker and the three-space indentation"). SC-12, SC-13b, SC-13c indented 3 spaces inside §10.2
   criterion 2's block, as specified.
4. **The `[SC-n]` heading tags** applied to all fifteen headings, as drafted (§0.1).
5. **Marker placement.** Markers that retire a specific registered line sit beneath the replacement
   at that line (SC-3 at 461, SC-13a at 1030, SC-6 M1 after the §7.7 table). "ADDED NOT SUPERSEDED /
   EXTENDED / AMENDED IN FORM" markers sit at the head of their clause's inserted block (SC-4, SC-8 M1,
   SC-10) or at the site they name (SC-6 M2 after line 915; SC-8 M2 after §11 item 7). SC-1's two
   markers were placed at their own sites in §2.3/§2.4 rather than 60 lines away at §2.9: **M1 after
   the §2.3 table's last row (line 212), not after row 205 itself** — a blockquote inside a table
   would split it; **M2 after the §2.4 formula line (220)**, before the bullet list it names.
6. **SC-6's line-855 row: applier-derived text.** The set specifies the operation ("REPLACE the row
   to add the state") but drafts no row (Part 6 item 3). Applied as the registered row with
   `` , `unscored` `` appended — the state name is the clause heading's (`` `unscored` ``, lower-case;
   K1's R24 table writes `UNSCORED`). This is F-9's named CI risk and is what this run tests.
7. **§AB** appended as the last paragraphs of H1b's amendments block (after "What an amendment may
   not do…"). **§13c-P** inserted after line 816, blank line each side, as drafted.
8. **H8 placed after SC-6's block** (table → SC-6's superseded-row marker → SC-6 clause → H8), so the
   retained superseded row sits directly beneath the table that replaced it (H1's convention). The
   literal alternative — H8 immediately after row 856, then SC-6 — is equally CI-neutral.
9. Output written **LF-only** (`newline="\n"`), matching `.gitattributes`. (Python's `write_text`
   emits CRLF on Windows — H1's `apply_v30a.py` would too; anyone re-applying should note it.)

### 1.3 Every hunk, in application order, with anchor match counts

Pre-verify = full-line match count against the pristine 1,099-line v30 file **before any edit**;
"at apply" = count against the current text at the moment the hunk was applied. **Every count is 1.
Nothing was skipped.** ("chained" = the anchor is the last line of the named earlier hunk's block, which
does not exist in the v30 file by construction; its at-apply count is 1.)

| # | Hunk | Anchor (v30 line) | Pre-verify | At apply | Mode | Payload lines | Applied text now begins at line |
|---|---|---|---|---|---|---|---|
| 1 | H1a | L6 (`**Status:** v30 …`) | 1 | 1 | after | 1 | 8 |
| 2 | H1b | L8 (`**Registration:** …`) | 1 | 1 | after | 27 | 15 |
| 3 | SC-9 | L99 | 1 | 1 | after | 13 | 146 |
| 4 | SC-1 marker M1 (§2.3 line 205) | L212 (last row of §2.3 table) | 1 | 1 | after | 1 | 273 |
| 5 | SC-1 marker M2 (§2.4 lines 220–222) | L220 (formula) | 1 | 1 | after | 1 | 283 |
| 6 | SC-1 (§2.9) | L266 | 1 | 1 | after | 15 | 331 |
| 7 | SC-10 (+ §6.1 marker) | L441 | 1 | 1 | after | 13 | 522 (marker) / 524 (clause) |
| 8 | H2 | L445 | 1 | 1 | replace | 4 | 538 |
| 9 | H3 | L450 | 1 | 1 | replace | 4 | 546 |
| 10 | H4 | L451 | 1 | 1 | replace | 4 | 550 |
| 11 | SC-2 | chained (H4) | — | 1 | after | 11 | 555 |
| 12 | SC-3 (+ marker) | L461 | 1 | 1 | replace | 23 | 575 (marker at 595) |
| 13 | SC-4 (+ line-459/446 marker) | L464 | 1 | 1 | after | 34 | 602 (marker) / 604 (clause) |
| 14 | SC-5 | chained (SC-4) | — | 1 | after | 13 | 637 |
| 15 | SC-7 | L468 | 1 | 1 | after | 11 | 655 |
| 16 | SC-8 (+ line-480 marker) | L480 | 1 | 1 | after | 15 | 679 (marker) / 681 (clause) |
| 17 | §13c-P (line-816 pointer) | L816 | 1 | 1 | after | 1 | 1031 |
| 18 | SC-6 row (registered row + `unscored`) | L855 | 1 | 1 | replace | 1 | 1070 |
| 19 | SC-6 (line-855 marker + clause) | L856 | 1 | 1 | after | 13 | 1073 (marker) / 1075 (clause) |
| 20 | H8 | chained (SC-6) | — | 1 | after | 1 | 1087 |
| 21 | SC-11 | L892 | 1 | 1 | after | 15 | 1125 |
| 22 | SC-6 marker M2 (§8.2 line 915) | L915 | 1 | 1 | after | 1 | 1164 |
| 23 | C1 | L992 | 1 | 1 | replace | 1 | 1241 |
| 24 | C2 | L1022 | 1 | 1 | replace | 1 | 1271 |
| 25 | SC-13a (+ conditional marker) | L1030 | 1 | 1 | replace | 16 | 1279 (marker at 1289) |
| 26 | SC-12 | L1035 | 1 | 1 | after | 11 | 1301 |
| 27 | SC-13b | chained (SC-12) | — | 1 | after | 9 | 1313 |
| 28 | SC-13c | chained (SC-13b) | — | 1 | after | 19 | 1323 |
| 29 | SC-8 marker M2 (§11 items 1–7) | L1054 | 1 | 1 | after | 1 | 1363 |
| 30 | §AB (amendments-block recording) | chained (H1b) | — | 1 | after | 13 | 41 |

Post-application integrity check: every **replaced** anchor (445, 450, 451, 461, 855, 992, 1022, 1030)
now matches **0** lines of the applied file; every **insertion** anchor still matches exactly **1**
(so a re-run of the same anchors would refuse correctly). `_prereg_version()` still reads **30**
(H1a is a separate line; line 6 byte-exact). `sections_of()` still finds **75** numbered sections
(no new numbered heading — SC-1's "§2.9" is a bold paragraph as drafted, see §6). Registered anchor
line 816 still matches exactly once (its verbatim copies in SC-13c(c2) and §AB are prefixed/embedded).

### 1.4 Not applied — anchors named by the set that carry no drafted text (stop-and-report by omission)

Each anchor matches exactly once in the v30 file **and** in the applied file; nothing was invented.

| Item | Anchor | Match count (v30 / applied) | Why not applied |
|---|---|---|---|
| SC-6's §8.2 sentence ("INSERT after the sentence 'None may be displayed in a way mistakable for a pass.'") | line 915 | 1 / 1 | **No sentence is drafted** (adoption file Part 6 item 3). SC-6's marker M2 ("§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED … `unscored` joins it …") **was** placed there and serves as the pointer; the operative sentence remains for the author. |
| SC-8's "pointer item added to §11 after line 1054" | line 1054 | 1 / 1 | **Undrafted** (Part 6 item 3). SC-8's marker M2 ("§11 items 1–7 — v30a, EXTENDED …") was placed there. |
| SC-11's "one-line pointer after line 961 (§8.6)" | line 961 | 1 / 1 | **Undrafted** (Part 6 item 3); SC-11 has no marker text either, so **nothing** sits at §8.6. |

Sensitivity variant **S1** (§5) shows that filling all three with placeholder one-liners changes no CI outcome.

### 1.5 Marker/apparatus text deliberately NOT placed (per §0.2), and the drafting identifiers left unresolved

- **SC-2's SUPERSESSION MARKER block** is a cross-reference to H2/H3/H4/C1's own markers ("cited, not
  re-drafted"); those markers arrived with H2/H3/H4/C1. Not placed as separate text.
- **SC-5, SC-7, SC-9, SC-11, SC-12, SC-13b, SC-13c** markers read "None — pure insertion" with an
  explanatory paragraph; the explanations are apparatus and were not placed.
- **Drafting identifiers inside applied marker text** (adoption file Part 6 item 4 — "reported, not
  rewritten"): SC-3's marker paragraph "**Consequential — §10.1 line 1022** (H1 **C2**) …" is now in
  `PREREG.md` line 597 verbatim; SC-8's marker M2 names "R23"; SC-10's marker names "F-5". These
  resolve to nothing inside `PREREG.md` and must be resolved to registered citations or struck at
  the real application, exactly as Part 6 item 4 says. **CI does not see them.**

---

## 2. (b) THE CHECKER — exact invocation, full stdout, exit code, classification

**Invocation** (cwd = `applied\`, Python 3.12.10):

```
python tools/check_registration.py --stage prereg
```

**Exit code: 1.** Full stdout (byte-identical to `applied\_applied_checker.txt`):

```
== check_registration --stage prereg (root: C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\applied) ==
[PASS] structure
[PASS] config_schema
[PASS] lock_table
[PASS] banned_vocabulary
    note: PREREG.md:493: EXEMPTION APPLIED id=REG15 reason='the registry entry must name the parked mechanism to state what a user does not get'
    note: PREREG.md:1406: EXEMPTION APPLIED id=PARK9 reason='the parking-lot pointer must name the parked mechanism to state what an amendment would restore'
[PASS] deletion_certificate
[FAIL] single_source
    AVAILABILITY_DECLARATION.md:974: rule about what may be reported/published stated outside PREREG.md; what a published number means is owned by PREREG §7.2/§8.3/§10.2: 'and a slice may not be reported as a pass on the strength of containing only unscored cells.'
    AVAILABILITY_DECLARATION.md:1035: denominator constitution defined outside PREREG.md; owned by PREREG §7.2/§7.4: 'by column. **The denominator derives from the DECLARED MAP (`n1\\declared_map.csv`), not from'
    AVAILABILITY_DECLARATION.md:1052: state-classification rule stated as a biconditional; a rule for assigning a state is owned by PREREG §6.6/§7.0, not by a companion document: '- **REQUIRED** iff its construction carries the wall-clock `ts_floor` join **and** it is not'
    AVAILABILITY_DECLARATION.md:1054: state-classification rule stated as a biconditional; a rule for assigning a state is owned by PREREG §6.6/§7.0, not by a companion document: '- **OUT OF JURISDICTION** iff its construction reads only same-row book/clock values,'
    AVAILABILITY_DECLARATION.md:1056: state-classification rule stated as a biconditional; a rule for assigning a state is owned by PREREG §6.6/§7.0, not by a companion document: '- **UNSCORED** iff it is degenerate-constant **or** unconstructible under T4.'
    AVAILABILITY_DECLARATION.md:1228: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'Requires no finding and forbids none; enters no denominator, contributes to no rate, and'
    AVAILABILITY_DECLARATION.md:1546: a defining clause for a term used normatively by PREREG.md is opened here; what a term means is owned by PREREG.md (§0.2.1): '**DEFINITION, declared.**'
    AVAILABILITY_DECLARATION.md:1551: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: "> **(i)** it is excluded from the criterion's denominator; **(ii)** it is in the denominator but"
    AVAILABILITY_DECLARATION.md:1580: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'path, entering no denominator, contributing to no rate, and **never reported as a pass**'
    AVAILABILITY_DECLARATION.md:1580: rule about what may be reported/published stated outside PREREG.md; what a published number means is owned by PREREG §7.2/§8.3/§10.2: 'path, entering no denominator, contributing to no rate, and **never reported as a pass**'
    AVAILABILITY_DECLARATION.md:2213: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'enters no denominator, contributes to no rate, and **cannot be reported as a pass**. A gate'
    AVAILABILITY_DECLARATION.md:2712: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: 'either side. Its gate status is **EXCLUDED**, and it enters no denominator.'
    AVAILABILITY_DECLARATION.md:2754: denominator membership stated outside PREREG.md; owned by PREREG §7.2/§7.4/§7.7: '**None of the four categories enters the criterion-1 denominator except Category 4**, which is'
    AVAILABILITY_DECLARATION.md:3677: denominator constitution defined outside PREREG.md; owned by PREREG §7.2/§7.4: "- **R11.** Criterion-1 denominator derives from the DECLARED MAP, not from the manifest's construction classes"
[PASS] phase_arithmetic
[PASS] requirement_ids
[PASS] legality_table
[PASS] parking_lot
[PASS] reducer_functions
[PASS] unit_grammar
[PASS] suppression_anchor

Deferred at this stage (owned elsewhere; an omitted branch is a failure, not a pass):
    ties_comparator_vs_shipped_mask  -> owned by --stage implementation
    l31b_inequalities_vs_shipped_rule  -> owned by --stage implementation
    shipping_defaults_vs_validated_runtime  -> owned by --stage implementation
    deleted_config_fields_rejected  -> owned by --stage implementation
    cost_script_total  -> owned by --stage implementation
    readme_numbers_regenerated  -> owned by --stage release
    package_defaults  -> owned by --stage release
    installability  -> owned by --stage release

RESULT: FAIL — 1 check(s) failed, 14 finding(s)
```

**Diff against the pre-application baseline** (`_baseline_checker.txt`): identical except the two
`EXEMPTION APPLIED` note line numbers (**414 → 493**, **1097 → 1406**), which is the REG15 / PARK9
markers moving down with the insertions above them — both markers still bind to the line directly
beneath them, as the notes prove.

**Classification of every finding — 14 findings, all one class:**

| # | Line | Detector | Class | Basis |
|---|---|---|---|---|
| 1 | 974 (§A.4) | reported/published rule | **Expected — pre-existing, unscrubbed declaration (K4 not landed)** | Verbatim copy of H4's now-registered sentence ("a slice may not be reported as a pass on the strength of containing only unscored cells"); after application it is a **verbatim-but-unattributed** copy (§4) — nearest `PREREG.md` mention is 24 lines above, window is 6. K4: attribute or cite. |
| 2 | 1035 (§A.6) | denominator constitution | Expected — pre-existing | Restates SC-4(a) ("THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP"), now registered. K4: cite. |
| 3–5 | 1052 / 1054 / 1056 (§A.6.0) | biconditional class rule | Expected — pre-existing, **but flagged: not clearable by scrubbing alone** | These are this fixture's class predicates. **SC-4(a)/(b) as applied REQUIRE the declaration to state them** ("the declaration states, ex ante and in full, the rule by which each unit … is assigned its gate class"; table column "Definition (the declaration supplies the predicate)"). The working-tree checker's rule 9 (added with the scope extension) treats any `**CLASS** iff …` in a companion document as an owned-by-PREREG rule. That rule was calibrated against H1's H6, which registered the predicate in `PREREG.md`; SC-4 moved the predicate to the declaration as instance data (R24). **Author decision needed:** either the checker gets an SC-4(a)-grounded exemption for the declaration's derivation-rule block (an "affirmative reason grounded in PREREG.md", as the checker's docstring requires), or the predicate is expressed in a form rule 9 does not match. Neither the applied schema text nor the checker is *wrong*; they now disagree. |
| 6 | 1228 | denominator membership | Expected — pre-existing | Restates SC-3(b)/SC-6(a) text ("requires no finding and forbids none; enters no denominator …"), now registered. K4: cite. |
| 7 | 1546 (§A.12) | defining clause | Expected — pre-existing | `**DEFINITION, declared.**` opens the "waived" definition; SC-12 now registers it and the adoption file already demotes §A.12 to corroboration. K4: cite SC-12. |
| 8 | 1551 (§A.12) | denominator membership | Expected — pre-existing | Verbatim copy of SC-12's limb (i)/(ii) — now a **verbatim-but-unattributed** line (nearest `PREREG.md` is 8 lines above; window 6). Line 1549 of the same quote block **is** attributed and is the one newly exempt line (§4). K4: bring attribution within 6 lines or cite. |
| 9–10 | 1580 (×2) | denominator membership + reported rule | Expected — pre-existing | Restates SC-6(a)/SC-12 item (4). K4: cite. |
| 11 | 2213 | denominator membership | Expected — pre-existing | Restates SC-6(a). K4: cite. |
| 12 | 2712 | denominator membership | Expected — pre-existing | Instance statement about one column ("gate status EXCLUDED, enters no denominator") that matches the membership regex; under SC-4(e)/(g) it is an enumeration entry. K4: reword as an enumeration row (e.g. class name + ground, citing SC-4(e)). |
| 13 | 2754 | denominator membership | Expected — pre-existing | Instance accounting ("none of the four categories enters the criterion-1 denominator except Category 4") matching the regex. K4: reword/cite SC-4(a). |
| 14 | 3677 (§R11) | denominator constitution | Expected — pre-existing | Working resolution R11 restates SC-4(a). K4: cite. |

**Defects in the applied schema text found by the checker: none. Checker defects: none.** Every check
that reads `PREREG.md` — `structure`, `lock_table`, `banned_vocabulary` (no banned term in 309 added
lines; both declared exemptions still bind), `deletion_certificate` (no backticked `superseded`),
`phase_arithmetic` (C1 keeps the `2–3 wknds` cell), `requirement_ids`, `legality_table` (§6.6 table
untouched), `reducer_functions` (§11 still lists the seven names), `unit_grammar`, `suppression_anchor`
(line 816's sentence and line 818's "every labelled case in the body, clean cases included" both still
in §7.2.1 — the §13c-P pointer is inserted between them and does not disturb the substring test) —
**passes**. K1's F-9 risk (the line-855 row edit) is **not realised**: no check parses that row.

---

## 3. (c) THE TEST SUITE — command, summary, counts, exit code, diagnosis

**Command** (cwd = `applied\`): `python -m pytest tests/registration -q -p no:cacheprovider`
**Exit code: 1. Summary line: `1 failed, 136 passed in 1.04s`** (137 collected). Full output at
`applied\_applied_pytest.txt`.

| | Before application (baseline) | After application |
|---|---|---|
| passed | 136 | **136** |
| failed | 1 — `tests/registration/test_checker.py::test_prereg_stage_on_real_repo_exits_zero` | **1 — the same test** |
| exit | 1 | 1 |

**Diagnosis of the one failure — pre-existing, caused by the declaration state, not by the applied
text.** The test (`test_checker.py` lines 363–372) asserts `cr.run_stage("prereg", ROOT) == 0` and
`"RESULT: PASS" in out`; it is a wrapper around the checker's exit code. Its captured output is the
same 14 `single_source` findings on `AVAILABILITY_DECLARATION.md` shown in §2 — it fails before and
after application for the same reason (the K4 scrub has not landed). This is the historical
"136/1 after H3 by design" figure. **All 136 other tests — the invariants, traces, expected-outputs and
checker unit tests — pass against the applied `PREREG.md`**, including every test that reads
`PREREG.md` (`test_checker.py`'s parking-lot / lock-table / legality-table / suppression-anchor /
unit-grammar checks on the real repo).

---

## 4. (d) THE VERBATIM-QUOTE EXEMPTION — coverage before and after

Method: the checker's own functions (`single_source_scan_set`, `normative_lines`, `_quote_normalize`,
`_prereg_quote_blob`-equivalent, `_is_attributed_quote` logic, `_SINGLE_SOURCE_RULES`) were imported and
run twice — once with the blob built from the pristine v30 `PREREG.md`, once from the applied one —
over every scanned file. Script: `applied\_quote_exemption_probe.py`; data:
`applied\_quote_probe_before.json` / `_quote_probe_after.json`.

| File | Exempt lines (verbatim + attributed) before → after | Of which "load-bearing" (a rule would otherwise fire) | Verbatim-but-**un**attributed before → after |
|---|---|---|---|
| `AVAILABILITY_DECLARATION.md` | **22 → 23** | 0 → 0 | **1 → 12** |
| `DESIGN.md` | 0 → 0 | — | 2 → 2 |
| `README.md` | 0 → 0 | — | 1 → 1 |
| `DEVIATIONS.md`, `PRIOR_ART_VERIFICATION.md` | 0 → 0 | — | 0 → 0 |

**Yes — the applied text changes the exemption's coverage, by one line.** Exempt before: declaration
lines 761, 762, 764, 765, 778, 826, 886, 942, 992, 1001, 1007, 1024, 1028, 1032, 1396, 1411, 1442,
1533, 1537, 2765, 3445, 3446. **Newly exempt after: line 1549** (§A.12, "configured, or reported in
any way that makes the detector's own result incapable of changing" — now a verbatim substring of
SC-12's registered definition, and `PREREG.md` is named within 6 lines above). No line lost coverage.
The exemption is **not load-bearing** in either state: none of the 22/23 exempt lines would trigger a
single-source rule anyway, so it currently suppresses zero findings.

**Newly-surfaced findings: none** (the exemption only suppresses, and no finding was suppressed by the
new coverage). **Findings that disappeared: none.**

**Eleven declaration lines become verbatim copies of now-registered text without attribution** —
these are the sites where the declaration restates what the schema set registers, i.e. the K4 scrub's
targets, and two of them are already among the 14 findings:

| Decl. line | Section | Matches applied PREREG text of | Nearest `PREREG.md` above | Currently a finding? |
|---|---|---|---|---|
| 966 | §A.4 | H4 (sliced-variant obligation) | 16 lines | no |
| 974 | §A.4 | H4 ("a slice may not be reported as a pass …") | 24 lines | **yes (#1)** |
| 1471 | §A.10 | line 480's ordering rule (already verbatim before; unchanged) | 7 lines | no |
| 1551 | §A.12 | SC-12 limbs (i)–(ii) | 8 lines | **yes (#8)** |
| 1555 | §A.12 | SC-12 limb (v) | 12 lines | no |
| 1562 | §A.12 | SC-12 "What invoking it requires" | 19 lines | no |
| 3368 | §D.1 | SC-8(a) | ≥60 lines | no |
| 3480–3481 | §D.3 | SC-9(e) | 29–30 lines | no |
| 3511 | §E | SC-7(c) | ≥60 lines | no |
| 3563, 3572 | §F | SC-11(a), SC-11(c) | ≥60 lines | no |

Attributing each within the 6-line window (or replacing with a citation, per SC-9(f)/SC-10(e)) is what
the checker's own rule asks for; the two that are findings today (974, 1551) would clear under the
verbatim rule the moment they are attributed.

---

## 5. Sensitivity variants (each run once, then the applied file restored — hash re-verified `a0c899a4…2ef5`)

| Variant | Change | Checker | pytest | sha256 / lines |
|---|---|---|---|---|
| **S1** | The three undrafted pointers (§1.4) filled with clearly-labelled one-line placeholders (§8.2 sentence after SC-6 M2; §8.6 pointer after line 961; §11 item 8 after SC-8 M2) | identical: 12 PASS / `single_source` FAIL / same 14 / exit 1 | 136 / 1 (same test) | `970877ea23404c079269a5a09cb7e0fc6df610275006f5bbf6e68dab12c6c7d3` / 1,414 |
| **S2** | SC-1's "§2.9" heading written as a numbered markdown heading `### 2.9 …` instead of the drafted bold paragraph (so `sections_of()` gains a §2.9 — 76 sections) | identical | 136 / 1 (same test) | `f67e687906d53019a7b2eee868cf8ece63896269c5a4d291ea837f079a77c47b` / 1,408 |

Conclusion: the CI outcome is invariant to the open formatting choices; the only thing standing between
the applied set and `RESULT: PASS` / 137 passed is the declaration scrub (K4) — plus the SC-4(a) vs
checker-rule-9 decision at lines 1052/1054/1056 (§2, findings 3–5).

---

## 6. (e) IDENTITY OF THE APPLIED SCRATCH FILE

| | |
|---|---|
| Path | `applied\PREREG.md` |
| **sha256** | **`a0c899a48a8ffe5363611bd9c5f4e2d82529a1dc8b6413721d58b3da96032ef5`** |
| **Line count** | **1,408** (`wc -l`; 1,099 + 309), LF-only, no BOM, ends with a newline |
| Pristine v30 input | `f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6`, 1,099 lines (kept as `applied\_PREREG_pristine.md.bak`) |
| Unified diff v30 → applied | `applied\_PREREG_v30a_applied.diff` (16 hunks; 318 `+` lines, 9 `-` lines incl. headers) |
| Applier + log | `applied\_apply_schema_set.py` (re-runnable from the pristine backup; refuses the live path), `applied\_apply_log.json`, `applied\_apply_stdout.txt` |
| Comparison note | The hash is sensitive to the formatting decisions in §1.2 (blockquote stripping, re-flow, marker placement, the derived line-855 row, LF). An author application that makes different choices will differ in hash while being CI-equivalent (S1/S2 demonstrate). Content-level comparison: `diff` the author's file against this one after normalising whitespace, or re-run `_quote_exemption_probe.py` — the exempt-line set (23 lines, §4) is wrapping-independent. |

Note on this file itself: `CI_GATE_RESULT.md` sits at the scratch root, and the checker's
single-source scan is scope-by-exclusion — **a re-run in `applied\` with this report present scans
the report and flags its own quotations of the findings** (verified: 22 self-findings on
`CI_GATE_RESULT.md`, plus the same 14 on the declaration — the 14-finding result in §2 was recorded
before this file existed). Move or delete it before re-running, or ignore findings whose file is
`CI_GATE_RESULT.md`. All other work files are `.txt/.json/.py/.diff/.bak` and are not scanned.

---

## 7. Observations for the author (not CI failures; recorded because the run surfaced them)

1. **H1a still says "Six class C changes"** and **H1b's table lists six amendments**; with the schema set
   the amendments block undercounts (SC-1, SC-6, SC-7, SC-8, SC-9, SC-10, SC-11, SC-13a–c are class C
   on §0.2.1 line 93's own words). The adoption file did not revise H1a/H1b; §AB was appended beneath
   the six-row table. Not a checker matter; a consistency matter for the real application.
2. **The only `AVAILABILITY_DECLARATION.md` / `§A.n` references in the applied `PREREG.md` come from H1's
   own text** — H1b's table (§A.1, §A.3, §A.4, §A.8 + R9, §A.6 + R11, §A.12), H2/H3/H4's operative
   sentences, and §AB's corroboration citations. **None comes from SC-1 … SC-13c** (Q3 held). Same genus
   as Q1(i)/Q2(c) for H1's text, if the author wants the whole file free of declaration references.
3. **SC-3's applied marker carries "(H1 C2)"; SC-8 M2 carries "R23"; SC-10's marker carries "F-5"** —
   Part 6 item 4's unresolved identifiers, now physically in the applied file (§1.5).
4. **SC-4(a) vs checker rule 9** (§2, findings 3–5) is the one place the applied schema and the
   working-tree checker pull in opposite directions; K4 cannot close those three lines by citation
   because SC-4(a) requires the declaration to *state* the predicate.
5. **Line 1471** of the declaration was verbatim-unattributed *before* application too (it copies line
   480's ordering sentence, `PREREG.md` named 7 lines above — one outside the window). Pre-existing;
   noted because it is the same one-line-past-the-window shape as 1551.

---

## 8. Files written this item (all under `applied\`; nothing elsewhere)

`PREREG.md` (applied), `_PREREG_pristine.md.bak`, `_PREREG_applied.md.bak`, `_PREREG_v30a_applied.diff`,
`_apply_schema_set.py`, `_apply_log.json`, `_apply_stdout.txt`, `_baseline_checker.txt`,
`_baseline_pytest.txt`, `_applied_checker.txt`, `_applied_pytest.txt`, `_S1_checker.txt`,
`_S2_checker.txt`, `_quote_exemption_probe.py`, `_quote_probe_before.json`, `_quote_probe_after.json`,
and this file. Plus the four working-tree copies named in §0. **No file outside `applied\` was
created or modified.**
