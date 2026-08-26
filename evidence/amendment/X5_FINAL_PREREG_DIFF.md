# THE FINAL `PREREG.md` DIFF — v30a, for author approval

**Nothing has been applied.** `PREREG.md` is byte-identical to the `prereg-v30` tag as this is
written:

    sha256  f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6
    lines   1099

Signing this diff authorises its application. Until then the file is read-only to every agent.

**How this document was assembled, stated because it bears on how much weight it carries.** The
38 hunks below were produced by independent passes over `SCHEMA_SET_FINAL.md` and
the v30a amendments block, each pass verifying its own anchors against `PREREG.md` with `sed -n`.
A first attempt to have one agent render the whole artifact **truncated** — it emitted §3 onward
and silently dropped the hunks themselves. The completeness critic caught that before I did. This
document is therefore rendered mechanically from the structured hunk records, so that no hunk can
be dropped in the writing; the prose in §3–§5 is mine, and the critics' full text is in
`X5_CRITIQUES.md` beside this file.

---

## 1. Summary — every hunk, in `PREREG.md` v30 line order

**38 hunks. Anchors verified: 38/38.**
A `*` on the line number means the hunk's placement carries a qualification — read its entry in §2.

| v30 line | Operation | Clause | What changes |
|---|---|---|---|
| 6* | insert | K2 §8.1 — amendment status line (replaces H… | A single new header line appears immediately below the Status line (blank line, the status line, blank line): "**Am… |
| 8* | insert | K2 §8.2 — the v30a amendments block (replac… | A `---` rule and an un-numbered `## v30a amendments (class C under §0.2.1)` block are inserted after the Registrati… |
| 97 | marker | SC-8 | A marker block, "§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT", is placed after line 97 with… |
| 99 | insert | SC-9 | A new clause block, "Integrity of a declared instance — v30a [SC-9]", limbs (a)-(f), is inserted inside §0.2.1 afte… |
| 205* | marker | SC-1 | A marker is placed at §2.3's `column_roles` row reading "§2.3 line 205 (`column_roles`) — v30a, ADDED NOT SUPERSEDE… |
| 220* | marker | SC-1 | A marker is placed at §2.4 reading "§2.4 lines 220–222 — v30a, PARTIALLY SUPERSEDED": the formula stands byte-exact… |
| 266* | insert | SC-1 | A new §2.9, "What a reconstructed declaration fixes, and what it may not leave open — v30a [SC-1]", is inserted at… |
| 431 | marker | SC-10 | A v30a supersession marker is placed at §6.1's heading and its five-row table. The heading and all five rows stand… |
| 441 | insert | SC-10 | A new clause "Declared non-gated data — v30a [SC-10]", limbs (a)-(e), is inserted after §6.1's closing paragraph an… |
| 445 | replace | H2 (schema layer: SC-2(d)) | Line 445 is replaced by a four-line block: the operative v30a bullet, then a nested quote retaining the registered… |
| 450 | replace | H3 (schema layer: SC-2, SC-9(b)) | Line 450 is replaced by a four-line block on the same shape as H2. The recording locus moves from the manifest to t… |
| 451* | insert | SC-2 | "The acceptance fixture's composition — v30a [SC-2]" is inserted between §6.2's bulleted element list (ending at li… |
| 451 | replace | H4 (schema layer: SC-2(e), SC-3(f)) | Line 451 is replaced by a four-line block on the same shape as H2 and H3. The sliced variant leaves the Phase 0 acc… |
| 459* | marker | SC-4 | A marker paragraph is added stating that criterion 1 (line 459) stands byte-exact and that what is superseded is th… |
| 461* | replace | SC-3 | Registered criterion 3 is replaced by "3. Runtime findings on every fixture side are scored against the fixture's D… |
| 464* | insert | SC-4 | THE CLAUSE 'The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]', limbs (a)–(j),… |
| 464* | insert | SC-5 | THE CLAUSE 'Adjudication routing — v30a [SC-5]', limbs (a)–(f), is inserted below the SC-4 block and above line 466… |
| 468 | insert | SC-7 | A new clause block, "The gate's input surface — v30a [SC-7]", limbs (a)-(e), is inserted after line 468 and before… |
| 480 | insert | SC-8 | The marker "§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED" is placed at line 480's site and the clause "The freeze,… |
| 816* | insert | SC-13c (§13c-P, second insertion point) | A single pointer paragraph, blank line each side, is inserted into §7.2.1 between line 816 and line 818. It says th… |
| 855* | replace-row | SC-6 | §7.7's detector-case coverage row is re-registered with `unscored` appended, and the v30 row is retained verbatim,… |
| 856* | insert | SC-6 | THE CLAUSE '`unscored` — a coverage state, v30a [SC-6]', limbs (a)–(e), is inserted after the §7.7 table (below the… |
| 856* | insert | SC-12(w) consequential — the §7.7 pointer,… | The pointer after §7.7's table reads, in full: "**`waived` is defined in §10.2 (v30a).** That definition governs th… |
| 892 | insert | SC-11 | A new §7.8 sub-block "The all-zero control — v30a [SC-11]", limbs (a)-(g), is inserted after §7.8's closing paragra… |
| 915* | marker | SC-6 | Marker M2 is added at §8.2's site: '§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED. §8.2's list is the *not-run* sub… |
| 915* | insert | SC-6 | The S2(i) INSERTION TEXT — one paragraph, blank line each side — is inserted into §8.2 after marker M2. It names `u… |
| 929 | replace | SC-12(w) | §8.3's third assertion bullet is replaced so the failure set becomes `unsupported`, `could_not_run`, or `waived`. T… |
| 961 | insert | SC-11 | A one-paragraph pointer (S2(iii)) is inserted after §8.6's only sentence: a zero, an empty result, or an all-clean… |
| 992 | replace | C1 operative row (§10 Phase 1 gate cell) —… | The Phase 1 gate cell is replaced. **Phase, Work and Est. are byte-identical; only the Gate cell changes.** The reg… |
| 998* | insert | K2 §9.1 — C1 retention block (§10 line 992,… | Immediately after the phase table's last row, blank line each side and before the weekend-total sentence at line 10… |
| 1022* | insert | K2 §9.2 — C2 retention block (§10.1 line 10… | One blockquote line at the list's three-space indentation, directly beneath the operative item 3 and before item 4,… |
| 1022 | replace | C2 operative item (§10.1 kill-gate criterio… | §10.1's criterion 3 is replaced so that the CORRECTED-SIDE limb asks the question SC-3 registers — whether a candid… |
| 1030 | replace | SC-13a | PREREG.md line 1030 — §10.2 kill/pause criterion 2 — is replaced by the SC-13a criterion (heading plus limbs (a1) u… |
| 1035* | insert | SC-13b | The SC-13b admissibility block (limbs (b1)–(b4)) is inserted inside §10.2 criterion 2's continuation block at its t… |
| 1035 | insert | SC-12 | The clause "'Waived', defined — v30a [SC-12]" is inserted immediately beneath the floor, preserving §10.2 criterion… |
| 1036* | insert | SC-13c | The SC-13c interactions block (limbs (c1)–(c7)) is inserted immediately after SC-13b's block, at the same three-spa… |
| 1050* | marker | SC-8 | Beneath §11's list, after a blank line, two marker blocks are placed: "§11 item 3 — v30a, SUPERSEDED AS A FILE SET,… |
| 1054 | insert | SC-8 | A new eighth item, "8. **The freeze, and the hash set that carries it — v30a.**", is inserted into §11's numbered l… |

---

## 2. The hunks

Each entry gives the registered v30 line as it stands today, what the hunk does to it, and **why**.
The justification is the part that matters: it is the reason you are being asked to sign.

### 2.1 — `PREREG.md` insert after PREREG.md line 6 (pristine[7..6]; diff hunk 1 of _K2_diff_pristine_vs_applied.txt) · K2 §8.1 — amendment status line (replaces H1a / applied line 8) · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **Status:** v30 — supersedes v1–v29. Committed together with `DESIGN.md` v26 and `HISTORY.md`. **The last version under the self-imposed cap. Everything after this routes through §0.2.1's class A/B/C machinery, which is what it was built for.**

**What changes.** A single new header line appears immediately below the Status line (blank line, the status line, blank line): "**Amendment status:** **v30a — this file is amended.** The class C changes under §0.2.1 are enumerated, by registered surface and clause, in the v30a amendments block below; their number is read from that enumeration and is stated nowhere as a numeral. The v30 text of every superseded clause is retained inline at its site, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text byte-exact." It supersedes the earlier draft line (applied A8) which read "Six class C changes under §0.2.1, listed in the v30a amendments block below."

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**Amendment status:** **v30a — this file is amended.** The class C changes under §0.2.1 are enumerated, by registered surface and clause, in the v30a amendments block below; their number is read from that enumeration and is stated nowhere as a numeral. The v30 text of every superseded clause is retained inline at its site, marked superseded; `git show prereg-v30:PREREG.md` recovers the registered text byte-exact.
```

**Why.** The line it replaces states a count as a numeral ("Six class C changes"), and that numeral is already wrong: the enumeration now carries nine superseded surfaces, ten marker surfaces, fourteen inserted clauses and four pointers. K2_AMENDMENT_LEDGER.md §1 records this as H-L13's third venue — four different numerals (four / five / six / fifteen) each true on its own unit at the moment it was written, each written outside the edit that later grew the set. Without this hunk, PREREG.md line 7 of the amended file would assert a count that the block below it contradicts, at the very top of the registration, and the count would go stale again the next time a clause is added. Line 6 itself is untouched, so `_prereg_version()` still reads 30.

**Class.** — (navigation/record; it asserts no measurement semantics). The class C authority is each enumerated change's, not this line's. Ground: K2 §3 row R01, "names the amendment and the recovery command; asserts no semantics".

### 2.2 — `PREREG.md` insert after PREREG.md line 8 (pristine[9..8]; diff hunk 2) · K2 §8.2 — the v30a amendments block (replaces H1b / applied lines 15–39; §AB at applied 41–53 kept byte-exact) · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **Registration:** committed unchanged as `PREREG.md` at first commit, before any detector code is written. See §11.

**What changes.** A `---` rule and an un-numbered `## v30a amendments (class C under §0.2.1)` block are inserted after the Registration line, followed after one blank line by §AB (the recorded-defect paragraphs on lines 816/830) byte-exact. The block replaces the earlier six-row indexed table with four enumerations by registered surface: (a) nine superseded lines — 445, 450, 451, 461, 855, 1030, 992, 1022, 929; (b) ten byte-exact surfaces carrying markers — 97, 205, 220–222, 431, 459, 480, 816, 915, item 3 (1050), items 1–7; (c) fourteen inserted clauses — SC-9, SC-1, SC-10, SC-2, SC-4, SC-5, SC-7, SC-8, SC-6, SC-11, SC-12, SC-13b, SC-13c, §11 item 8; (d) four pointers. SC-3 and SC-13a are deliberately absent from (c) because they sit in (a) as supersessions of lines 461 and 1030.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
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

**RECORDED DEFECT, NOT RESOLVED BY THIS AMENDMENT — `PREREG.md` lines 816 and 830 hold duplicated,
conflicting authority over one state.**

Line 816, verbatim: "**A combination that is `not_applicable` on every scope-eligible case in a
body of data publishes its counts and suppresses its yields, rates, and gates**, naming the
reason."

Line 830, verbatim: "**scope-eligible** — the leakage risk logically applies to this unit. For a
labelled feature-cohort pair this is a property of the corpus label, **not of what the detector
could do about it**: a pair in an `unsupported` or `not_applicable` case remains scope-eligible
and remains in §7.2's yield denominators as a miss."

For a combination `not_applicable` on every scope-eligible case in a body of data, line 830 keeps
every labelled pair **in §7.2's yield denominators as a miss** — a yield that therefore exists and
reads zero — while line 816 **suppresses that combination's yields, rates, and gates**. One state,
two registered dispositions pointing in opposite directions: the §0.2.1-class duplicated-authority
defect this registration's own structural rule exists to forbid — §0.2.1 line 77: "**Single
normative source.** `PREREG.md` is the sole normative source for measurement semantics … A
restated rule … is a protocol failure, not a redundancy"; §0.2.1's registry names the signature at
line 72: "two statements, one file".

**What this amendment does about it: an express, scoped exception only.** SC-13c(c2) excepts the
quantities SC-13a–c require from line 816's suppression clause, because a gate suppressed on the
`not_applicable`-everywhere fact is a detector waived on it (SC-12's definition, head and limb
(iii); the declaration's §A.12 states the same definition and corroborates) and line 1035 forbids
the waiver. Line 816's text is not edited and its publication clause is kept and required; a
pointer to the exception is inserted at line 816's own site.

**What this amendment claims for the exception, and what it does not.** The exception rests on
this amendment's own class C authority and on the capability ground stated at SC-13b(b3). It does
not claim the support of `PREREG.md` line 818. Line 818 states the registered rationale for line
816's suppression, and its applied holding for the never-applied combination's yield — that such a
yield "is not a measurement of the tool" and that "the `not_applicable` count carries that fact
honestly; the yield does not" — points the other way for this state. For the quantities SC-13a–c
require, this amendment departs from that holding, expressly and on its own authority; everywhere
else line 818 stands as registered and unchanged.

**What this amendment does NOT do: resolve the conflict.** Everywhere outside SC-13a–c, lines 816
and 830 both stand as registered and continue to point in opposite directions over the
`not_applicable`-everywhere state. **Flagged for a future class C amendment** — the defect changes
what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
the state a single canonical disposition and make one of the two lines cite the other. Until that
amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3
and §A.12 item 5). **The operative conflict is registered-text-internal — line 816 against line
830.** It is not a conflict between line 816 and the declaration: declaration text on the same
state is provisional until the tag, is at most corroboration, and cannot settle a disagreement
between two registered lines.

**WHAT THIS AMENDMENT DISCLOSES — seven things a reader would otherwise have to reconstruct.**

**1. This amendment changes a criterion of a gate that was already signed off.** `HISTORY.md`
**H-34**, dated **12 August 2026**, recorded the §10.1 kill-gate sign-off with the verdict *"the
project proceeds"*. §10.1's criterion 3 is amended here, after that date. §0.2.1's ex-ante rule
makes the **ordering** the disclosable fact.

**2. The gate is harder to satisfy on net, and this is where.** §6.2 criterion 3's corrected-side
limb moves from *silence* to *matching the declared map*, which is forced: the registered criterion
is falsified by the fixture's own measurement (18 of 48 instrument-months carry a non-zero corrected
count). **A contaminated-side tightening drafted alongside it is WITHDRAWN from this amendment**
(H-39), because its reason appeared nowhere in the clause carrying it.

**3. §10.1 criterion 3 has never been evaluated, for any candidate, under either text.** No
candidate was run against either fixture side. **§9.2's comparison-set surface DID run**, on 14
August 2026, over eight hand-written cases and eight clean paired controls — but it is committed
nowhere, so §9.2's *"committed with this protocol"* is breached and uncurable for `prereg-v30`, and
**§9.2 remains un-run in its registered form**. The acceptance-fixture surface was not run. The
kill-gate verdict rests on criterion 1. Recorded at `DEVIATIONS.md` **D-003**.

**4. Whether the kill gate is re-run under the amended criterion is NOT REGISTERED, and is an open
author decision.** No clause of this amendment creates such an obligation, and H-34's own re-fire
condition triggers on **a new tool surfacing**, not on **the criterion changing**. A reader must not
infer that amending criterion 3 re-opens the gate.

**5. The map ships; the fixture does not.** The declared ground-truth map is committed with this
registration and is publicly reachable at the tag. **The acceptance fixture is not** — it is 64
stored-prediction parquets per side, outside the repository, and **no clause requires publishing
it**. So a third party can read the map, the declaration and any published reconciliation, and
**cannot independently run a candidate against `fixture_contaminated` / `fixture_corrected`**.
Criterion 3 is not third-party evaluable today, and this amendment does not change that.

**6. §10.1 registers no third state.** *Partial satisfaction* is defined nowhere in the corpus, so a
criterion that **could not be evaluated** is indistinguishable from one **evaluated NO**, and both
default to proceed. Given disclosure 3, that is not hypothetical — it describes what already
happened. **Recorded as a registration defect for a future amendment** (H-38), alongside the
twin-criterion-5 entry; this amendment does not widen its scope to cure it.

**7. Criterion 1's effective requirement REVERSES on 14 of 25 leaking-source columns, and the
registered text of line 459 does not move.** The fixture manifest classes **25** of the 35 fed
columns as leaking sources. Under the SC-4(b) partition **11** are REQUIRED — absence is a miss —
while **13** are OUT OF JURISDICTION and **1** is UNSCORED, and on an OUT OF JURISDICTION column an
availability-class finding is a **FALSE POSITIVE**. So on 14 of those 25 the gate's demand inverts:
*absence is a miss* becomes *a finding fails the gate*. **A reader comparing v30 and v30a
byte-for-byte at line 459 will see no change and conclude wrongly.** The narrowing is made under the
class C rule, which permits it; §0.2.1 line 97 measures at the outcome, and at the outcome this is a
supersession.

**These seven are disclosed because the record should not have to be reverse-engineered to find
them.** Each is verifiable from artifacts this registration commits, except where disclosure 5 says
otherwise.
```

**Why.** This is the hunk that makes the amendment self-describing rather than self-counting, and it is the one whose central property the task asks be verified. The property holds. The closing paragraph states it in terms: "The registered lines this amendment supersedes are those in (a) and no others; the registered lines whose reading it extends are those in (b) and no others; the clauses it inserts are those in (c) and no others; the pointers are those in (d) and no others. **Their number is read from the enumeration and is stated nowhere as a numeral** — so that a further clause added under §0.2.1 adds a row here and changes no count anywhere in this file." I scanned every number-word in the 68-line block: the only numeral that counts anything about the amendment itself is "Two passes produced them" in the opening paragraph, which K2-O6 discloses and which is self-enumerated by the two sentences immediately after it ("The first is … The second is …"). Every other number-word describes registered or clause content, not a change count — "the five-bodies heading and table" (naming §6.1 line 431's own heading), "the three-class partition rule" (SC-4's content), "two levels" (SC-6's content). The text it replaces asserted "six class C changes" three times (A8, A17, A37), a six-row table (A28–A35), and referred to the sliced-variant element as "amendment 3" by table index (A39); the replacement refers to that element by surface — "the sliced-variant row of (a)" — so no index can go stale either.

**Class.** — (the record of the amendment; the class C authority is each enumerated change's). Ground: K2 §3 row R02. §AB rides in the same physical insertion and is likewise record, per R03.

### 2.3 — `PREREG.md` 97 · SC-8 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> **An amendment inherits §11's integrity chain in full:** signed tag, both file hashes in the tag message, external timestamp receipt committed, repository publicly reachable at lock. An amendment weaker than the thing it amends is not one.

**What changes.** A marker block, "§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT", is placed after line 97 with a blank line on each side. Line 97 stands byte-exact; only its numeral "both" ceases to fix the set.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT.** "both file hashes in the
tag message" records the count at the time of writing; it is superseded as a count by §11 item 8,
which derives the count from the tag message's own enumeration. The requirement — that an
amendment inherit §11's integrity chain in full — stands byte-exact.
```

**Why.** Line 97 is the sentence this whole amendment invokes to license itself, and it is already false as a count. It says "**both** file hashes in the tag message" — a literal two — while the executed prereg-v30 tag message (verified this pass by `git tag -n30 prereg-v30`) enumerates FIVE: PREREG.md, DESIGN.md, HISTORY.md, tools/check_registration.py, protocol/runtime_reference.py. So a v30a that inherits the chain "in full" while line 97 still reads "both" would carry, inside its own authorising sentence, a count contradicted by the tag it is amending, and PREREG.md would hold two answers to how many hashes an amendment must carry. Worse, v30a grows the set again: under SC-8(f) the declaration itself must be hashed "which carries the scoring key", so the numeral would be stale a second time on the day it is signed. This is precisely the H-L13 shape the drafting record cites (SCHEMA_SET_FINAL.md lines 1995-2002): "the obligation to re-bump lives outside the edit that grows the target". The marker supersedes the numeral only. It preserves the sentence the rest of SC-8 leans on — "An amendment weaker than the thing it amends is not one" — byte-exact, so nothing is weakened by the fix. Without this hunk, either SC-8(f) and §11 item 8 are inconsistent with §0.2.1 (two normative answers, §0.2.1 line 77's own failure mode), or the author must edit line 97's numeral, which supersedes the requirement rather than the count. This hunk lands 957 lines from either SC-8 insertion point and is its own registered surface in K2 table (b); it is easy to lose in assembly and must not be.

**Class.** C, carried with SC-8. K2 table (b): "§0.2.1 line 97 — 'both file hashes' | superseded as a count, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8".

### 2.4 — `PREREG.md` 99 · SC-9 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **A class C change discovered after the affected detector already exists** cannot be made ex ante by any ceremony. It is recorded, the amended registration is committed, and **the affected benchmark is regenerated as a new version under §6.4** — new snapshot version, new beacon draw, new single-use run — with the superseded results published alongside, exactly as §6.4's re-draw rule requires.

**What changes.** A new clause block, "Integrity of a declared instance — v30a [SC-9]", limbs (a)-(f), is inserted inside §0.2.1 after line 99 and before line 101's "**Membership in A or B must be citable, not asserted.** Three conditions, all required:". §0.2.1 lines 93-99 stand byte-exact; no supersession marker.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**Integrity of a declared instance — v30a [SC-9]**

**(a) A DECLARATION SUPPLIES DATA UNDER A REGISTERED SCHEMA. IT CREATES NO GATE OBJECT.** A
declaration supplies the values, enumerations, and evidence the registered clauses call for. **It
creates no new criterion, no new denominator, no new coverage state, no new unit, and no new gate
class.** Where a declaration finds it needs one, that is a class C amendment to this file, made
before the declaration relies on it. **The criteria of §6.2 as amended are the whole gate**; a
declaration that adds a fifth is adding a fifth way to fail, outside the registration.

**(b) EVIDENCE ARTIFACTS ARE NEVER ADJUSTED TOWARD A DECISION.** A manifest, a measurement record, a
capture, or any artifact whose job is to record what was measured **is not edited to carry a
declaration, a decision, or an amendment.** Where a registered element's recording locus must move,
the locus is **amended explicitly**, and the amendment says what moved and what did not. An evidence
artifact edited toward a wanted answer is no longer evidence of anything.

**(c) A LOCKED OBLIGATION IS DISCHARGED ONLY BY BEING MET OR BY BEING AMENDED.** It may not be
discharged by a `DEVIATIONS.md` entry, by a working resolution, by an orchestrator decision, or by
being carried forward silently. Dropping it is a further class C amendment. **An element that cannot
be met as written at the instant an amendment must be committed is amended explicitly — never waived
and never left outstanding**, because an outstanding element invites being re-read as satisfied
later.

**(d) WORKING-RESOLUTION AUTHORITY IS UNIFORM, AND SUPERSESSION IS ORDERED.** A working resolution
binds by its content and its date, **not by where it was recorded**: a resolution issued in the
course of the work binds exactly as one written into the record does, and the record is completed
to contain it. Where a later resolution supersedes an earlier one, **the later governs and the
earlier stands as the record**; the ledger is append-only and an entry is never rewritten to agree
with its successor.

**(e) THE INTERPRETATION RULE — resolution toward the stronger reading only.** **An interpretation
of locked text may resolve ONLY toward the STRONGER reading. Any interpretation that weakens a
locked obligation — narrows a denominator, exempts a unit, softens a criterion, admits an excluded
set, converts a required finding into an optional one, or converts an unscored cell into a pass — is
a class C amendment and may not be recorded as a working resolution, a decision-log entry, or a
reading.** This binds every entry appended after the rule, and it binds the reading of this
registration by its own author.

**(f) A RULE STATED TWICE HAS NO CANONICAL SOURCE.** *(Citation: §0.2.1 line 77.)* Where a
declaration needs one of these rules, it **cites this section and does not restate it.** A second
normative copy in a declaration is the duplicated-authority failure, not a redundancy.
```

**Why.** §0.2.1 lines 93-99 register the amendment machinery — what class C is (line 93), that it requires an amended registration and not "a `DEVIATIONS.md` entry standing alone" (95), that it inherits §11 (97), that it cannot be made ex ante after the detector exists (99). What those lines never say is what a DECLARATION may not do without invoking that machinery. In v30 that gap was tolerable because the declaration carried little. Under v30a it becomes load-bearing: the declaration carries the map and its cell key (SC-3(a)), the per-unit class citations and N (SC-4(a)), the unscored ledger (SC-6(b)), the frozen-object enumeration (SC-8(a)). SC-9(a) is the only thing standing between that and a second registration operating outside §0.2.1 — "It creates no new criterion, no new denominator, no new coverage state, no new unit, and no new gate class." Its closing sentence rests on a countable fact: §6.2 registers exactly four criteria at lines 459-462, so "a declaration that adds a fifth is adding a fifth way to fail" is checkable, not rhetorical. SC-9(f) closes a scope hole the author should see directly. Line 77's single-normative-source rule names only one other file: "**`DESIGN.md` may reference a rule by its section but may never restate it.**" The declaration is not in line 77's scope as written, so today it may restate normative rules and no registered sentence forbids it. SC-4(a) already assumes the fix — "No companion document states a class predicate in rule form ... the predicate is cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f))" — so SC-4 is underdetermined if SC-9 is not adopted. SC-9(c) matches line 95's own prohibition and extends it to locked obligations generally. THE LIMB TO READ TWICE BEFORE SIGNING is (e): interpretation of locked text "may resolve ONLY toward the STRONGER reading", every weakening is class C, and it "binds the reading of this registration by its own author". That is self-binding with no escape other than a further amended registration — which is the point, and also the cost.

**Class.** C — §0.2.1 line 93 (it registers rules the declaration must obey and forecloses declaration-created gate objects, i.e. it changes what a published number may rest on). K2 table (c): "§0.2.1, after line 99 | SC-9 | integrity of a declared instance ... | C".

### 2.5 — `PREREG.md` 205 (marker written at line 212, the end of its block) · SC-1 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> | `column_roles` | per-column rule: `at_timestamp`, `at_bar_close`, `at_source_timestamp` (naming the source column), `always`, or an explicit availability column | all |

**What changes.** A marker is placed at §2.3's `column_roles` row reading "§2.3 line 205 (`column_roles`) — v30a, ADDED NOT SUPERSEDED. The role enumeration stands byte-exact. SC-1(c) states what a role value *is* relative to the comparator; it removes no role and adds none." The row's text does not change.  **Placement (R37/D4):** §2.3's `AvailabilityModel` table runs 201–212; the marker is written after line 212, before line 214. Marker placement rule (R37/D4): a supersession marker attaches to a COMPLETE BLOCK — a whole paragraph, a whole table, or a whole list — never inside one. A marker written inside a table breaks the table; inside a list it breaks the list.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§2.3 line 205 (`column_roles`) — v30a, ADDED NOT SUPERSEDED.** The role enumeration stands
byte-exact. SC-1(c) states what a role value *is* relative to the comparator; it removes no role
and adds none.
```

**Why.** Line 205 enumerates five positional rules and is silent on the only question the comparator asks: is a role value the availability instant, or an approximation of it? SC-1(c) answers that in §2.9 — sixty lines away and in a different section. Without a marker at line 205 the registered row keeps reading, on its face, as if selecting a role fixes the instant, which is the "two copies, drifted" shape §0.2.1 exists to prevent and which §6.8's deletion-certificate discipline ("a deletion is not complete until the symbol's inbound normative reference set is empty") applies to in the reverse direction. The marker also does defensive work the author should notice: it fixes that the enumeration is ADDED NOT SUPERSEDED, so no implementer can read SC-1(c) as licence to drop `at_bar_close` or to add a sixth role — a role removal would change what every runtime rate means and is not what this amendment does.

**Class.** Carried with SC-1 (K2 table (b): "§2.3 line 205 — `column_roles` | added, not superseded: a role is a position, not an availability instant | SC-1(c) | carried with SC-1"). Not independently class C — no registered text changes.

### 2.6 — `PREREG.md` 220–222 (marker at its site; see finding 5 on exact placement) · SC-1 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> > **`a(y_j) = label timestamp + label horizon + publication delay`**

**What changes.** A marker is placed at §2.4 reading "§2.4 lines 220–222 — v30a, PARTIALLY SUPERSEDED": the formula stands byte-exact as the *form*; what is superseded is the unstated v30 assumption that the horizon term's unit is a duration. Under SC-1(d) the unit is declared, and a declared unit other than a duration is class C under §0.2.1 line 93. The v30 reading is retained beside the marker and is expressly NOT operative as an exclusive reading.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§2.4 lines 220–222 — v30a, PARTIALLY SUPERSEDED.** The formula
`a(y_j) = label timestamp + label horizon + publication delay` stands byte-exact as the *form*.
**Superseded is the assumption, unstated in v30, that the horizon term's unit is a duration.**
Under SC-1(d) the horizon's unit is declared by the declaration, and a declared unit other than a
duration is a class C amendment under §0.2.1 line 93's word "unit". The v30 reading is retained
beside this marker and is NOT operative as an exclusive reading.
```

**Why.** This is the one marker in SC-1 that is class C on its own ground rather than carried, and it is the marker most likely to be waved through as cosmetic. Line 220 registers `a(y_j) = label timestamp + label horizon + publication delay`; line 222 registers that "All three terms are user-declared, as one `label_availability` declaration" and that a declaration supplying only base and horizon is complete. Nowhere does §2.4 state the horizon's unit. §0.2.1 line 93 makes "a needed *new* … unit" class C — verified verbatim at line 93 — so a fixture whose declared horizon is not a duration (an event count, a bar count, a session boundary) either forces a class C amendment or is absorbed silently into a formula that assumes duration arithmetic. Without this marker, SC-1(d)'s consequence lives only in §2.9 and the assumption it supersedes lives, unmarked, at the site where an implementer actually reads the formula: §2.4 would continue to license the duration reading as exclusive while §2.9 denies it, and the two would be equally registered. Note what the marker deliberately does not do — line 222's "no profile may default any term" and line 224's `unsupported` consequence are untouched.

**Class.** C — §0.2.1 line 93's word "unit" (K2 table (b): "§2.4 lines 220–222 — the label-availability formula | partially superseded: the unstated assumption that the horizon term's unit is a duration | SC-1(d) | C — line 93's 'unit'").

### 2.7 — `PREREG.md` insert after 266 (before the `---` at 268); new §2.9 · SC-1 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Therefore: every L2a and L3.1 finding prints its declaration and its cohorts (§8.4); the declaration is in `VALIDATED_CONFIG` with every published rate; conformance is measured separately from detection (§7.8); registry entries 12 and 13 record the limitation.

**What changes.** A new §2.9, "What a reconstructed declaration fixes, and what it may not leave open — v30a [SC-1]", is inserted at the end of §2, carrying limbs (a) measured-not-intended, (b) the representation is named, (c) a role is a position not an availability instant, (d) units are declared and a change of unit is class C, (e) staleness is not unavailability, (f) one comparator branch is scored. §2.8 and the `---` section break are untouched.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§2.9 What a reconstructed declaration fixes, and what it may not leave open — v30a [SC-1]**

A declaration is the gate's semantic authority: every availability instant a comparator reads is
the one the declaration declares. The requirements below follow, and a declaration that does not meet
them fixes nothing.

**(a) MEASURED, NOT INTENDED.** Where a reconstructed element's *documented* value and its
*measured* value differ, the declaration declares the **measured** value as the element's declared
value, records the documented value beside it, and names the artifact each was read from. A gate
scored against an intended value the artifact does not exhibit is scored against a fixture that
does not exist.

**(b) THE REPRESENTATION IS NAMED.** Every declared element states **which representation of the
data it describes** — the value as constructed, or the value as fed to the model — and, where a
transform separates them, names the transform. An element that does not say which representation
it describes fixes no availability instant, and every downstream class derived from it is
underivable.

**(c) A ROLE IS A POSITION, NOT AN AVAILABILITY INSTANT.** A `column_roles` value (§2.3) names
where a value sits on a lattice. The instant the comparator reads is the availability instant the
declaration declares for that column. **Where a role is an approximation of that instant, the
declaration says so, and that role is never scored against.** Scoring against a positional
approximation instead of the declared availability instant is a scoring error, not a tie
convention.

**(d) UNITS ARE DECLARED, AND A CHANGE OF UNIT IS CLASS C.** Where a declared element supplies a
term of a registered formula, the declaration states that term's **unit**. Where the declared unit
differs from the unit the registered formula assumes, the substitution is a **class C amendment**
under §0.2.1 line 93 and is carried by an amended registration — never by the declaration alone,
and never by a working resolution.

**(e) STALENESS IS NOT UNAVAILABILITY.** A value whose declared availability instant is legal at
the decision instant under the declared `ties` branch is **available**, however old it is. Age
licenses no finding. A finding resting on staleness alone is a false positive.

**(f) ONE COMPARATOR BRANCH IS SCORED.** Exactly one `ties` branch (§2.3) is declared, and it alone
is scored. Figures computed under any other branch are published as **informational disclosures**
so the tie choice is auditable: they enter no denominator, contribute to no rate, and **no gate
outcome may be computed from them.** Reporting a pass or a fail under a non-declared branch is out
of specification.
```

**Why.** v30 registers the availability model's ELEMENTS (§2.3 table, lines 201–212) and the label formula (§2.4 line 220) but never registers what a declaration must FIX for those elements to mean anything. §2.8 concedes the gap and stops there: line 264, "A wrong declaration produces wrong findings in **both** directions, whichever declaration it is", and line 266 answers it only with printing and separate conformance measurement. Everything downstream in this amendment — SC-2's enumerated fixture, SC-3's map, SC-4's per-unit derivation, SC-6's ledger, SC-8's freeze — is written over the word "declared", and without SC-1 that word has no registered content. Four concrete failures it closes, each of which the v30 text permits today: (a) §6.2 line 447 requires the declaration to be "reconstructed, not chosen — from the original experiment's documented prediction instant, data timestamps, bar construction, label horizon"; where the artifact's measured value differs from the documented one, v30 states no rule, so the gate may be scored against a fixture that does not exist. (b) nothing requires an element to say whether it describes the value as constructed or as fed to the model, so a declared instant can be true of one representation and false of the other and every class derived from it is underivable. (c) line 205's role vocabulary is positional; nothing forbids scoring against the role instead of the declared instant. (d) §2.4's formula assumes its horizon term is a duration and never says so, so a non-duration horizon could be substituted silently rather than as the class C change §0.2.1 line 93 makes it ("a needed *new* branch, unit, denominator, coverage state, tier licence, or acceptance criterion"). (f) §2.3 line 207 registers `ties` as one element but nothing forbids publishing a gate outcome computed under the branch that was not declared. If the author does not sign this, SC-2/3/4/6/8 all still read on an undefined "declaration" and the amendment's own vocabulary is unanchored.

**Class.** C — §0.2.1 line 93 ("a needed *new* … unit") for limb (d); the clause as a whole is registered as an insertion in K2 table (c), "§2, after line 266 (new §2.9) | SC-1 | … | C". Ground: the schema pass over the walk of the reconstructed declaration against §6.2.

### 2.8 — `PREREG.md` 431 · SC-10 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> ### 6.1 Five bodies of data

**What changes.** A v30a supersession marker is placed at §6.1's heading and its five-row table. The heading and all five rows stand byte-exact; the marker states that what is superseded is the implication that the enumeration is exhaustive of everything a fixture declaration may carry.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§6.1 line 431 heading and table — v30a, AMENDED IN FORM.** The five bodies stand unchanged as
bodies of data. **Superseded is the implication that the enumeration is exhaustive of everything a
fixture declaration may carry.** A declared non-gated diagnostic is not a sixth body of data; it is
data attached to the acceptance fixture that the fixture's row of the table does not admit to any
denominator. The alternative — adding a sixth row — is named in F-5 and is the author's call.
```

**Why.** §6.1 line 431 reads "### 6.1 Five bodies of data" and lines 433-439 are a closed five-row table (Acceptance fixture / Development corpus / Evaluation corpora / Conformance regression suite / Wild corpus). SC-10(a) licenses a declaration to carry a body marked NOT PART OF THE GATE. Without this marker the registration holds two readings at once: a heading that says there are five bodies, and a clause that permits a sixth kind of attached data. That is exactly the duplicated-authority defect §0.2.1 line 77 forbids, and it is the collision K1 finding F-5 raised. The marker resolves it in the cheapest direction — the five bodies stand as bodies of data, and a declared non-gated diagnostic is not a sixth body but data the fixture's own row admits to no denominator. NOTE THE AUTHOR MUST ACT ON: as drafted the marker's final sentence ("The alternative — adding a sixth row — is named in F-5 and is the author's call") is applied text under SCHEMA_SET_FINAL.md §0.2, so it would enter PREREG.md carrying an unregistered drafting identifier and an unmade decision. See findings.

**Class.** C, carried with SC-10 — K2 block table (b), row "§6.1 line 431 — the five-bodies heading and table | amended in form: the implication that the enumeration is exhaustive | SC-10". Ground: §0.2.1 line 93, carried with the clause rather than standing on its own.

### 2.9 — `PREREG.md` 441 · SC-10 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> The fixture's AUC figures are provenance — they describe the pipeline it was built from, not the tool's accuracy. **No accuracy or generalization rate is published from the fixture.** The descriptive proof count of §6.2 is the sole reported fixture outcome; it is a count, receives no inferential interval, and is not a rate.

**What changes.** A new clause "Declared non-gated data — v30a [SC-10]", limbs (a)-(e), is inserted after §6.1's closing paragraph and before §6.2's heading at line 443. It registers that a declaration may carry data the gate does not consume, the condition on which that data stays out of the arithmetic, that diagnostic classes are not declared classes, four forbidden uses, and a one-copy rule.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**Declared non-gated data — v30a [SC-10]**

**(a) A DECLARATION MAY CARRY DATA THE GATE DOES NOT CONSUME, IF IT SAYS SO IN TERMS.** The
declaration marks such a body **NOT PART OF THE GATE**: nothing in it enters any acceptance
criterion, any denominator, any rate, or the freeze of SC-8. It is published as a diagnostic, with
its own provenance, and it is exempt from the freeze **precisely because** it is exempt from the
arithmetic.

**(b) THE EXEMPTION IS CONDITIONAL, AND THE CONDITION IS THE WHOLE POINT.** Non-gated data may be
added, revised, or withdrawn without amendment **provided its figures are never moved into an
acceptance denominator.** Moving any of them in is a class C amendment — and a body that is both
unfrozen and admitted to a denominator is a denominator that can move after a result.

**(c) DIAGNOSTIC CLASSES ARE NOT DECLARED CLASSES.** Where the declaration's class set carries
classes for diagnosis alongside the classes the map scores, **the diagnostic classes are named as
such and are not members of the declared scored set.** Any statement of the form "maximum across
classes" **names the class set it maximises over**, and any headline over a partitioned population
names the partition it counts.

**(d) FORBIDDEN USES OF NON-GATE DATA, REGISTERED BECAUSE EACH IS A ROUTE INTO THE ARITHMETIC.**
Non-gated data, diagnostic classes, and figures the declaration marks informational may never be
quoted as: **(1)** evidence about a unit the scored pipeline consumes, in either direction; **(2)**
**any criterion-1 arithmetic**; **(3)** an unqualified headline over the scored population; **(4)**
an unqualified maximum or peak. A peak is quoted with its class set **and** its metric, or it is not
quoted.

**(e) ONE COPY.** These rules are stated here and cited elsewhere. A declaration restating them for
a particular side has created a second normative copy (§0.2.1 line 77) and must cite instead.
```

**Why.** The anchor is §6.1's closing sentence and it is the reason this clause is needed rather than optional. Line 441 already forbids one thing — "No accuracy or generalization rate is published from the fixture" — and fixes one thing as the outcome: "The descriptive proof count of §6.2 is the sole reported fixture outcome; it is a count, receives no inferential interval, and is not a rate." What line 441 does NOT say is what happens to every other figure the fixture's declaration carries. As registered, a diagnostic class, an informational figure, or a peak has no registered status at all: nothing stops it being quoted as evidence about a scored unit, folded into criterion 1 arithmetic, or headlined over the scored population. SC-10(b) is the load-bearing limb — the exemption from SC-8's freeze is granted *precisely because* the data is exempt from the arithmetic, so a body that is both unfrozen and admitted to a denominator is a denominator that can move after a result is seen. That is the same failure mode SC-8(e) and §0.2.1 line 99 exist to stop, arriving by a route neither of them covers. SC-10(d)(4) ("a peak is quoted with its class set and its metric, or it is not quoted") is what makes the rule checkable in a report rather than merely stated. If this hunk is not made, non-gated data is unregulated and SC-8's freeze has a documented hole beside it.

**Class.** C — new clause inserted, no registered sentence replaced at the site. K2 block table (c): "§6.1, after line 441 | SC-10 | declared non-gated data, diagnostic classes, and the forbidden uses of non-gate data | C | schema pass over the walk of the reconstructed declaration against §6.2". Ground: §0.2.1 line 93 — it changes what the gate may consume and what a published number means.

### 2.10 — `PREREG.md` 445 · H2 (schema layer: SC-2(d)) · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> - **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.

**What changes.** Line 445 is replaced by a four-line block: the operative v30a bullet, then a nested quote retaining the registered v30 sentence verbatim and marked NOT operative, then its retirement reason. The anchor becomes constituted by recomputation from the fixture's own stored per-row prediction and outcome columns, declared as an enumerated set of entries; the ±0.010 interval and `full` mode carry over unchanged.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair on both sides (§A.1 item 1) — that fact, and the replacement entries themselves, are instances and are recorded in the declaration. **The clause "and because the anchor's model family changed" stood here until R55/W5 and is struck: it is false against its own cited source, which names six architectures with LightGBM listed first, and §A.1 item 2 was corrected on 21 August 2026 to say so.** Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

**Why.** The registered anchor is a transcribed pair of numbers that names no architecture, horizon or instrument, and no horizon of the declared fixture reproduces it on both sides (declaration §A.1 item 1). *(R48/Q4: an earlier draft of this justification also said "the anchor's model family changed", relying on §A.1 item 2. That claim was FALSE against its own cited source — the registered protocol named six architectures with LightGBM listed first — and is struck from the justification. **It was NOT struck from the operative text at that time — only from this commentary — so the falsified clause shipped for two further rounds under a sentence saying it had been removed. Struck from the operative text at R55/W5.** The ground is line 445's under-specification and the non-reproduction at item 1, neither of which depends on it.)* A transcribed figure cannot be re-derived, so a disagreement between it and the artifact has no resolution procedure. Recomputation from committed bytes is a pure function of the artifact, so the anchor becomes checkable and a deviation approaching the interval becomes a stop-and-report rather than a pass. Text drafted at PREREG_v30a_DIFF.md H2; SC-2(d) is the schema layer over it, not a replacement for it.

**Class.** C — §0.2.1 line 93 (it changes what a published number means and how an acceptance interval is applied). Ledger table (a): §6.2 line 445.

### 2.11 — `PREREG.md` 450 · H3 (schema layer: SC-2, SC-9(b)) · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> - **Contamination availability class** recorded in the manifest.

**What changes.** Line 450 is replaced by a four-line block on the same shape as H2. The recording locus moves from the manifest to the reconstructed availability declaration — a file the amended tag message hashes — and the clause forbids an evidence artifact from carrying a declaration. The ground-truth column DAG and the count of independently leaking sources stay manifest content.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*
```

**Why.** A manifest is the product of a dated measurement round and records what was measured. Writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. Moving the locus to the declaration binds harder than the manifest did, because the tag hashes the declaration and so freezes the class at the tag; moving it afterwards becomes itself class C. The clause states explicitly that it moves the locus of one element and nothing else. Text drafted at PREREG_v30a_DIFF.md H3.

**Class.** C — §0.2.1 line 93 (it changes where a declared gate input lives and what may carry it). Ledger table (a): §6.2 line 450.

### 2.12 — `PREREG.md` insert after 451 — but after H4's replacement block, not after the registered line (see finding 1) · SC-2 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> - **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**What changes.** "The acceptance fixture's composition — v30a [SC-2]" is inserted between §6.2's bulleted element list (ending at line 451) and the `**Pass gate — discrimination, not tier.**` heading at line 453, with limbs (a) the fixture is an enumerated set of declared artifacts, (b) changing composition is class C and never a deviation or working resolution, (c) the pre/post licence is bounded, (d) a reference anchor is constituted by recomputation not transcription, (e) moving an element between phases is an amendment whose scoring rule is declared at the move. Line 452 (blank) and line 453 are untouched.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**The acceptance fixture's composition — v30a [SC-2]**

**(a) THE FIXTURE IS AN ENUMERATED SET OF ARTIFACTS, DECLARED.** The declaration enumerates the
artifacts that constitute the acceptance fixture, by side, with the provenance of each. An artifact
not in that enumeration is **not part of the fixture** and no criterion is evaluated on it.

**(b) CHANGING THE COMPOSITION IS CLASS C — NEVER A DEVIATION, NEVER A WORKING RESOLUTION.**
Admitting an artifact the declaration excludes, or removing one it includes, **changes the object
the acceptance criteria are evaluated on and therefore changes what every published gate number
means.** It is a class C amendment under §0.2.1 line 93. It may not be done by a `DEVIATIONS.md`
entry, by an orchestrator decision, or by a working resolution. **Declared exclusions are hard.**

**(c) THE PRE/POST LICENCE IS BOUNDED.** Where the fixture is a paired pre/post construction and a
delta across the pair is read as an availability effect, the licence for that reading requires the
two sides to differ **in availability and in nothing else**. **A change to the column set, the
label set, the row population, or the evaluation population is not an availability change**, and a
variant carrying one is not admissible as a side of this fixture.

**(d) A REFERENCE ANCHOR IS CONSTITUTED BY RECOMPUTATION, NOT BY TRANSCRIPTION.** Where the gate
requires a reference quantity to reproduce, that quantity is **recomputed from the fixture's own
committed bytes** and declared as an **enumerated set of entries**, one per declared horizon and
side, each naming its provenance. **The recomputation is authoritative over any figure recorded in
a prior report**; a recorded figure that agrees is a secondary record and is reported as such, and
one that disagrees is a defect resolved before the gate runs, never a competing anchor. **The
declared tolerance applies per entry and may not be widened.** Because a recomputed anchor is a
pure function of committed bytes, a deviation approaching the tolerance is a **stop-and-report**,
not a pass.

**(e) MOVING AN ELEMENT BETWEEN PHASES IS AN AMENDMENT, AND ITS SCORING RULE IS DECLARED WITH THE
MOVE.** A registered element that cannot be satisfied at the instant the amendment must be
committed is **amended explicitly — never waived and never left outstanding.** Where the move
re-registers the element as a later-phase obligation, the obligation names the event that makes it
due, and its scoring rule is declared **ex ante, at the move**, so it cannot be chosen after a
result is seen.
```

**Why.** §6.2 lines 445–451 list what the fixture RECORDS and never says what the fixture IS. That silence is what every acceptance number depends on: if an artifact can be admitted or dropped without an amendment, the object criteria 1–4 are evaluated on can change while the criteria stay byte-identical, and no published gate number means what it says. Limb (b) closes it and names the three routes that would otherwise be used — a `DEVIATIONS.md` entry, an orchestrator decision, a working resolution. The other three limbs are the schema layer under changes this amendment is already making at instance-bearing lines, and signing SC-2 is what stops those from being one-off repairs: (d) is why line 445 is being retired at all — the registered pair 0.957/0.675 was a transcribed figure, and SC-2(d) registers the form that replaces it (recompute from committed bytes, declare an enumerated entry set with per-entry provenance, tolerance per entry and never widened, a deviation approaching the tolerance is a stop-and-report because the quantity is a pure function of bytes) so the next anchor cannot be a transcription again; (e) is the general form of what H4 does to the sliced variant, and it forbids the alternative the author should reject on sight — leaving a registered element outstanding rather than amending it. Limb (c) is the one with no counterpart hunk and deserves the closest read: the whole contaminated/corrected construction is read as an availability delta, and nothing registered requires the two sides to differ in availability and nothing else. Under (c) a variant that also changes the column set, the label set, the row population or the evaluation population is not admissible as a side — without it, a delta attributed to availability can be carrying a population change instead, and criterion 3 as amended by SC-3 would be scoring a map against a side it does not describe.

**Class.** C — K2 table (c): "§6.2, after line 451 | SC-2 | the acceptance fixture's composition, what may move, the pre/post licence, reference anchors by recomputation, moves between phases | C". Ground: the schema pass over the walk of the reconstructed declaration against §6.2. SC-2 itself re-drafts no marker: the markers at lines 445, 450, 451 and 992 stand as H1 wrote them (H2/H3/H4/C1) and are cited, not reproduced — see finding 3.

### 2.13 — `PREREG.md` 451 · H4 (schema layer: SC-2(e), SC-3(f)) · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> - **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.

**What changes.** Line 451 is replaced by a four-line block on the same shape as H2 and H3. The sliced variant leaves the Phase 0 acceptance fixture and is re-registered as a Phase 1 CI obligation with its scoring rule declared ex ante. **SC-2's clause block is inserted AFTER this replacement block, not after the registered line** — see the order note below.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
- **Sliced variant — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.4). **The sliced variant is not part of the Phase 0 acceptance fixture.** It is a **Phase 1 CI obligation, due at the first CI run that exercises the padded slicer and before any user-facing slice auditing is published**, produced by that same padded slicer, with its slice boundaries declared. **Its scoring rule is declared now, ex ante, so it cannot be chosen after a result is seen:** a slice inherits the ground-truth-map cells its rows select and is scored against those cells under criterion 3 as amended — findings the selected cells predict are required, findings they exclude are false positives, cells the map does not cover are unscored. **A slice of a characterized side is never treated as clean, and a slice may not be reported as a pass on the strength of containing only unscored cells.** The obligation is not deletable by a `DEVIATIONS.md` entry or by a decision-log interpretation; dropping it is a further class C amendment. **Why it is amended rather than left outstanding:** the registered clause requires an artifact produced by a component of the tool under development, while §0.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly — leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure mode §2.7 exists to stop.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing."
  >
  > *The variant is moved and re-registered, not deleted: slice auditing is not dropped and the slicer is not exempt from CI.*
```

**Why.** The registered clause requires an artifact produced by a component of the tool under development, while §0.2.1 line 95 requires this amendment to be committed before that component exists. An element that cannot be satisfied at the instant it must be committed is amended explicitly — leaving it outstanding invites it to be quietly re-read as satisfied later, which is the failure §2.7 exists to stop. The scoring rule is declared now precisely so it cannot be chosen after a result is seen. **ORDER, load-bearing (R37/D3):** H4 is the only operation on line 451 itself; SC-2 inserts after the block H4 produces. Applied the other way round, SC-2's anchor re-derivation finds the registered line gone — it survives only inside H4's retained nested quote — and the applier refuses on zero matches, which is the applier working correctly.

**Class.** C — §0.2.1 line 93 (it moves an acceptance-criteria artifact between phases and registers its scoring rule). Ledger table (a): §6.2 line 451.

### 2.14 — `PREREG.md` 459 (marker written at line 462, the end of its block) · SC-4 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> 1. **Every** ground-truth leaking source column receives at least one **primary runtime finding**, whether its promotion status makes the reported tier PROVEN or REVIEW. Attribution must be to the labelled source; a finding somewhere downstream does not satisfy this. Findings on **descendants** are secondary (§7.6) and neither satisfy nor violate it.

**What changes.** A marker paragraph is added stating that criterion 1 (line 459) stands byte-exact and that what is superseded is the *inference* that its denominator is a construction-taxonomy count recorded elsewhere in the fixture's evidence; and that §6.2 line 446's manifest requirement is NOT amended, only the arithmetic role of what it records is constrained. No registered sentence is edited.  **Placement (R37/D4):** §6.2's criteria list item 1 runs 459–462; the marker is written after line 462. Marker placement rule (R37/D4): a supersession marker attaches to a COMPLETE BLOCK — a whole paragraph, a whole table, or a whole list — never inside one. A marker written inside a table breaks the table; inside a list it breaks the list.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§6.2 line 459 — v30a. THE TEXT IS UNCHANGED; THE REQUIREMENT IS NOT.** *(Corrected at R54/W3.
This marker previously read "**ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact." The first
clause is true byte-for-byte and false at the outcome, and §0.2.1 line 97 measures at the outcome.)*

**What is superseded is the INFERENCE** that the denominator is any construction-taxonomy count
recorded elsewhere in the fixture's evidence. That inference is not operative; SC-4(a) replaces it.

**WHAT THAT DOES, STATED AS ARITHMETIC BECAUSE THE CONSEQUENCE IS NOT VISIBLE IN THE DIFF.** The
fixture manifest classes **25** of the 35 fed columns as leaking sources. Under the SC-4(b)
partition:

| manifest class | gate class | count | what a finding on it means |
|---|---|---|---|
| LEAK-SOURCE | REQUIRED | **11** | absence is a **miss** |
| LEAK-SOURCE | OUT OF JURISDICTION | **13** | a finding is a **FALSE POSITIVE** |
| LEAK-SOURCE | UNSCORED | **1** | neither for nor against |

**On 14 of those 25 columns the gate's requirement REVERSES SIGN** — from *absence is a miss* to
*a finding fails the gate*. **That is a supersession at the outcome, and it is recorded as one
here**, whatever the byte-level text of line 459 does. It is made under the class C rule, which
permits it; what §0.2.1 line 97 does not permit is making it while recording that nothing changed.

**A reader comparing v30 and v30a byte-for-byte at line 459 will see no change and conclude
wrongly.** That is why this is also carried as a disclosure on the face of the amendment (R54/W4,
disclosure 7) rather than left here alone.

**§6.2 line 446 — NOT AMENDED.** The manifest requirement stands; only the *arithmetic role* of
what it records is constrained, which is a statement about denominators, not an edit to line 446.
```

**Why.** Line 459 registers 'Every ground-truth leaking source column receives at least one primary runtime finding' and never says what set 'every ... column' ranges over. Three lines above the criteria, line 446 registers verbatim: '- **Ground-truth column DAG** in the manifest: leaking sources, descendants, clean columns, and the count of independently leaking sources.' That count is the only count of leaking sources v30 names anywhere near criterion 1, so a reader with only v30 in hand reads the denominator off it. SC-4(b) registers the contrary: 'N is the length of the REQUIRED list, and no other quantity is N', and SC-4(j) forbids identifying the scored set by cardinality at all. Without this marker the amended file carries both readings at once, and criterion 1's N could be taken from a manifest figure built from how columns were *constructed* rather than from what the map declares violating on the scored side — the two questions SC-4(a) says 'do not in general have the same answer'. The marker is what makes line 459's byte-exactness compatible with SC-4 instead of in tension with it. Cost of not making it: the single most consequential number in the acceptance gate stays ambiguous in a document whose whole purpose is to fix it ex ante.

**Class.** Class C carried with SC-4. K2 ledger table (b), row '§6.2 line 459 — criterion 1 | added, not superseded: the inference that the denominator is a construction-taxonomy count | SC-4'. Ground: §0.2.1 line 93 — it changes what a published number means.

### 2.15 — `PREREG.md` 461 (replaces the registered criterion 3 in place, as list item 3) · SC-3 · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> 3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`.

**What changes.** Registered criterion 3 is replaced by "3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH MAP — v30a, operative. [SC-3]", limbs (a)–(h), with the v30 sentence retained verbatim inside the same list item under "SUPERSEDED BY v30a … NOT operative" so criteria 4 does not renumber. The retained quote in the marker is byte-exact against line 461 as read.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:**
"3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`."
*Retired because a fixture side may carry real, strictly-post-decision violations, in which case
the registered criterion fails the gate on a correctly-behaving detector reporting a violation the
fixture really contains. The measured incidence is instance data and lives in the declaration.*

**Consequential — §10.1 line 1022** (H1 **C2**): the kill gate carries a second copy of the retired
premise ("silent on `fixture_corrected`") and must be amended with this clause or `PREREG.md` holds
both readings at once.

**3. Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH
MAP — v30a, operative. [SC-3]**

**(a) WHAT THE MAP IS.** The map is an **enumeration of expected findings**, declared in the
fixture's availability declaration, stated **per side**, **per declared violation class**, and
**per declared cell** of the declared scored population. **The declaration declares the cell key —
the unit it declares the fixture to be partitioned into — and names it explicitly.** The map is
published as an artifact with a **declared schema**: one row per cell of the declared scored
population, with every field named, including the field that records whether the cell is
scored. **The artifact may in addition carry rows of a class the declaration declares
DIAGNOSTIC (SC-10(c)); those rows are not cells of the map.** They are adjudicated by no
criterion, enter no denominator and no rate, and **(b)'s dispositions are exhaustive over the
map's cells, not over the artifact's row count**. A count taken from the artifact without
excluding them counts a different population, and **every figure published from the artifact
names which population it counts**.

**(b) THREE DISPOSITIONS, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE MAP.**
- **A finding the map predicts is REQUIRED.** Its absence is a miss.
- **A finding the map excludes is a FALSE POSITIVE.** It fails the gate — on any side, at any tier,
  primary or secondary.
- **A cell the map does not cover is UNSCORED** (SC-6). It requires no finding and forbids none,
  enters no denominator, contributes to no rate, and is **never reported as a pass.**

**(c) THE MAP COVERS THE WHOLE DECLARED SCORED POPULATION.** The declaration declares the scored
population — the rows and units the criteria adjudicate. **A subclass of that population is never
excluded, masked, or given a separate denominator by description**; the only way a unit leaves the
scored arithmetic is by being an UNSCORED cell of the map, declared as such before any detector
runs. Membership of a unit in a structurally awkward subclass — a boundary, a gap, a session
edge — is **by itself neither a licence for a finding nor a defence against one**; such units are
adjudicated by the map like any other.

**(d) THE MAP IS STATED IN THE TERMS THE DECLARATION DECLARES.** It is stated in the representation
§2.9(b) names and **side-relatively**. **There is no side-independent statement of what leaks**; a
side-independent list is a category error and misroutes every finding derived from it.

**(e) ONE SCORING KEY, AND ONLY ONE.** A re-aggregation, restriction, or re-projection of the map
published for reporting is a **REPORTING OBJECT**: it is **not a second scoring key and changes no
adjudication.** Where two views of the map are published, both are published with their delta
explicit and neither replaces the other.

**(f) A DERIVED SUBSET INHERITS ITS CELLS.** Where a subset of a scored artifact is produced (a
slice, a filtered variant, a projection), it **inherits the map cells its units select** and is
scored against those cells under this criterion. **A subset of a characterized side is never
treated as clean, and a subset may not be reported as a pass on the strength of containing only
unscored cells.**

**(g) NEITHER SIDE IS ASSUMED CLEAN.** A side the declaration characterizes is **CHARACTERIZED,
never clean**, and no report describes it as clean. Silence and belief never convert into a pass
(§2.7, §8.1), applied here to the tool's own exam.

**(h) THE AMENDMENT DOES NOT LOWER THE BAR.** A finding on a cell the map marks zero is still a
false positive and still fails the gate. The unscored disposition is not an escape hatch. The map
is **declared and frozen before any detector runs** (SC-8); a map frozen after a run is a key
shaped by the result and scores nothing.
```

**Why.** The registered criterion is falsified as written, and it fails in the direction that matters: it fails the gate on a detector that is behaving correctly. §A.8 of the declaration records that the corrected side of this fixture carries real, strictly-post-decision violations — per PREREG_v30a_DIFF.md H5 (citing declaration 1423–1429), 18 of 48 instrument-months, up to 111,334 of 580,944 rows. Under line 461 as registered, a detector that reports one of those violations produces a runtime finding on `fixture_corrected` and the acceptance gate fails. So line 461 cannot stand; the only question is what replaces it. SC-3 replaces it with the map — an enumeration of expected findings, per side, per declared violation class, per declared cell, with the cell key named by the declaration, frozen before any detector runs — and three exhaustive dispositions (required / false positive / unscored, and unscored is never a pass). What the author should look at hardest is what SC-3 adds beyond H5's drafted structure, because that is the part he has not already seen: (c) forbids a subclass of the scored population being excluded, masked, or given a separate denominator "by description", and makes structural awkwardness — a boundary, a gap, a session edge — neither a licence for a finding nor a defence against one; (e) makes any re-aggregation of the map a reporting object and not a second scoring key; (f) makes a derived subset inherit its cells, so a slice cannot be reported as a pass by containing only unscored cells (this is the clause H4's re-registered sliced variant is scored under); (h) ties the freeze to SC-8 and states in terms that the amendment does not lower the bar — a finding on a cell the map marks zero is still a false positive and still fails. Two non-obvious consequences: (1) SC-3 supersedes H5 on the cell-key axis, so H5 must NOT also appear in the final diff (finding 2); (2) SC-3 generalises H5's "both fixture sides"/"on either side" to "every fixture side"/"on any side", so the criterion no longer presupposes exactly two sides — consistent with SC-2(c), and a deliberate change the author is signing (finding 7). Inbound-reference check on the premise being retired: line 117's parenthetical ("the opposite default would fail pass-gate criterion 3") survives, because a flagged clean shifted feature is a finding the map excludes and still fails; line 1022 does not survive and is cured by C2; line 1035's "criterion 3's gates in force" is ambiguous and is flagged in findings.

**Class.** C — K2 table (a): "§6.2 line 461 — acceptance criterion 3 | superseded | SC-3 | C | declaration §A.8; working resolution R9". §0.2.1 line 93: it changes what an acceptance criterion requires.

### 2.16 — `PREREG.md` 464 (insert after) · SC-4 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

**What changes.** THE CLAUSE 'The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]', limbs (a)–(j), is inserted after line 464, immediately below the marker hunk and above line 466's parenthetical. It registers the three-class partition (REQUIRED / OUT OF JURISDICTION / UNSCORED) as predicates owned by the registration, the UNSCORED-wins precedence, two forbidden edge readings, the two registered exclusion grounds, the publication discipline, and the re-derivation and stop-and-report rules.  **R49/R5 adds limb (k)**: the criterion-1 floor (non-empty REQUIRED list on every declared side, on pain of STOP, modelled on SC-13b(b1)'s existing sentence) and the per-unit reconciliation against the manifest's leaking-source list, with the express carve-out that the reconciliation is a disclosure rather than a classification — without which (a) forbids the check that closes the hole. **(k) is unsatisfied by the declaration as it stands** and is the only limb of SC-4 that is.  **R49 addendum S1–S3**: (k) now names which mechanism handles which failure — the floor is the **terminal backstop** for the degenerate case, the reconciliation is the **operative protection** against gradual narrowing, because N ≥ 1 is satisfied by scoring one column. **(k2)(i)** adds the only bar that is registerable: every ground **names the artifact and location** behind it — quality of ground is not something a registration can require, provenance is. **(k3)** now states the verifiability limit outright: the map ships and the fixture does not, so a reader can check completeness, internal consistency and provenance, and cannot verify a classification against the data. It is a disclosure obligation with limited external verifiability and says so.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**The criterion-1 denominator, and the partition rule that constitutes it — v30a [SC-4]**

**(a) THE DENOMINATOR IS DERIVED FROM THE DECLARED MAP, BY THE RULE REGISTERED HERE, AND THE
DECLARATION SHOWS THE DERIVATION.** The rule by which each unit of the declared scored set is
assigned its gate class is **registered in this clause — the class predicates of (b), under the
precedence of (c) — and is not the declaration's to state, restate, or rewrite.** The declaration
states, **ex ante, in full, and per unit**: the class assigned, and the registered predicate the
unit satisfies, **by citation to the row of (b) that carries it**, together with the declared
facts on which the unit satisfies it — what the map declares on it on the scored side under the
declared branch, and the construction and legality facts the declaration records for it. The
classes are **derived by the registered rule over those declared facts, never assigned by hand.**
**No companion document states a class predicate in rule form** — as a biconditional ("CLASS iff
…") or otherwise: the predicate is cited, not restated (§0.2.1 line 77; SC-9(a), SC-9(f)). An
evidence artifact's classification of how a unit was *built* answers a different question from
what the map declares *violating* on the scored side under the declared branch; the two do not in
general have the same answer. **No classification of the scored set other than this derivation
enters any criterion, denominator, or count**, and no split within such a classification carries
gate arithmetic. Any report quoting such a count names the scope it counts under.

**(b) EXACTLY THREE CLASSES, MUTUALLY EXCLUSIVE AND EXHAUSTIVE OVER THE DECLARED SCORED SET.**

| Class | Registered predicate (cited by the declaration, per unit; never restated) | What a finding on it means |
|---|---|---|
| **REQUIRED** | the map declares a violation on it, on the scored side, under the declared branch | at least one **primary** runtime finding attributed to it is required; absence is a miss |
| **OUT OF JURISDICTION** | every constituent read is declared legal at the boundary instant under the declared branch | an availability-class finding on it is a **false positive** |
| **UNSCORED** | scoring on it is declared impossible, on a ground the declaration states | counts **neither for nor against** any criterion (SC-6) |

**The declaration cites these rows, per unit, and states the facts on which each unit satisfies
the row it cites; it does not restate them** (a). **There is no fourth class and no residue
class.** **N is the length of the REQUIRED list**, and no other quantity is N.

**(c) PRECEDENCE, REGISTERED.** Where a unit satisfies more than one class predicate, **UNSCORED
wins.** The declaration derives under this precedence and states none of its own; a unit's class
is the first the order yields, and for each unit that satisfies more than one predicate the
declaration records which it satisfies and that precedence decided it.

**(d) THE DECLARATION FIXES THE READING AT EVERY EDGE, EX ANTE, AND THE READINGS ARE PART OF THE
DERIVATION.** Where a registered class predicate admits two readings, the declaration states which
it derives under and why, before any detector runs. **Two readings are registered as forbidden
outright**, because each silently removes units from the arithmetic: (i) a locality condition may
not be read more narrowly than the declared lattice, so a read of the same source at another
instant of the same lattice does not by itself create a cross-source violation; (ii)
**unconstructibility in some other rebuild of the fixture is never gate-unscoredness** — only a
gate status the declaration declares EXCLUDED on the artifact the gate actually scores removes a
unit from the arithmetic.

**(e) GROUNDS FOR EXCLUSION ARE DECLARED, AND DECLARED PRE-RUN.** A unit is excluded only on a
ground the declaration states. Two grounds are registered here because each is otherwise a
guaranteed failure of criterion 1 for a reason unrelated to detection: a **degenerate unit that
cannot carry a finding of the scored class at all** (leaving it in the denominator makes criterion 1
unsatisfiable), and a unit whose **construction or lag treatment is declared UNRESOLVED** (it cannot
be scored under any reading). **Reinstating an excluded unit changes the denominator and is class
C.**

**(f) PUBLICATION DISCIPLINE — the constraints below, and they are the point of the rule.**
1. **Each class is published as an enumerated list of unit names.** A class stated as a bare count
   is not auditable and does not satisfy this. A count that cannot be written out as a list is a
   count nobody can audit.
2. **No class is defined as a residue.** "Everything else" is not a class definition; each unit's
   membership is derived by (a) and shown.
3. **The partition check is printed and reproducible by any gate report:** the three class sizes sum
   to the size of the declared scored set, no unit appears in two classes, and no unit of the set is
   missing from all three. **A gate report that cannot reproduce the check has not scored the
   fixture.**

**(g) ONE GATE CLASS PER UNIT.** A unit carries **one** gate class and one only — §0.2.1 line 79's
rule that no field answers two questions, applied to gate classes. **A unit's gate class is a
statement about what the gate does with a finding on it, and the gate needs exactly one answer per
unit.** An availability *declaration* about a unit and its *gate class* are different objects and
are never conflated: a unit the declaration does not feed to the scored pipeline holds **no gate
class whatever** — declaring it out of jurisdiction would imply the gate adjudicates it and
declines.

**(h) RE-DERIVATION IS MANDATORY, AND MOVING A UNIT IS AN AMENDMENT.** If a unit's construction
changes, or an excluded unit becomes constructible, its class is **re-derived by the rule of (a).**
**The declaration's enumeration is the current output of the rule and is never a substitute for
it.** Moving a unit between classes, or changing N, after the tag is a class C amendment.

**(i) DISAGREEMENT HALTS.** Any disagreement between the rule-derived class and the frozen class is
a **stop-and-report**. It is not resolved in favour of either at run time, and a run that proceeds
past it has not scored the fixture.

**(j) THE SCORED SET IS NAMED, NOT COUNTED.** The declared scored set is identified by **the named
constant the declaration declares**, never by its cardinality. Any re-derivation names the constant,
not the length; two sets of equal size are not thereby the same set.

**(k) TWO MECHANISMS AGAINST A COLLAPSING SCORED POPULATION, AND NEITHER IS SUFFICIENT ALONE.**
There are two ways criterion 1 stops meaning anything, and they need different instruments. The
population can go **empty** — the degenerate case, caught by the floor at (k1). Or it can be
**narrowed unit by unit** until what survives is not worth scoring — the gradual case, caught by the
reconciliation at (k2). **(k1) alone is satisfied by scoring a single column.** It is written below
as the terminal backstop it is; **the operative protection is (k2)**, and a reader who takes the
backstop for the mechanism has mistaken which failure this clause exists to stop.

**(k1) THE FLOOR — THE TERMINAL BACKSTOP.** The declared scored set and the REQUIRED list are
enumerated by name **before any detector runs** and are **non-empty on every declared side**. **If
either is empty on any declared side, criterion 1 is not discharged and the outcome is STOP** —
lifted only by supplementing the declaration with declared, enumerated units for that side and
re-freezing under §11's integrity chain; never by scoring criterion 1 on the remaining side, never by
suppressing the empty side's gate, and never by a `DEVIATIONS.md` entry or a working resolution.
**Non-emptiness is the whole of this limb, and deliberately so:** any minimum above zero would be a
threshold chosen from the distribution this fixture already exhibits, which §7.0 forbids. A floor
that cannot be set without looking at the data is not set. **This limb therefore catches only the
degenerate case; it is not the protection and must not be cited as one.**

**(k2) THE RECONCILIATION — THE OPERATIVE MECHANISM.** The REQUIRED list is published alongside a
**per-unit reconciliation against the fixture manifest's list of columns classed as leaking
sources** — the **named list**, not the count. **Every unit the manifest so classes that this
derivation does not class REQUIRED is named**, with **the registered predicate of (b) that produced
its class** and the declared facts on which it satisfies that predicate. A difference stated as a
count, a total, or a summary of where the differences "mostly" sit does not satisfy this limb; the
unit is named or it is not reconciled.

**(k2)(i) EVERY GROUND NAMES THE ARTIFACT AND LOCATION THAT SUPPORTS IT.** For each such unit the
declaration cites **the artifact and the location within it** — file, and row, line, or field — on
which the declared facts rest. **The quality of a ground is not something this registration can
require**, and pretending otherwise would be vagueness dressed as a constraint; **provenance is.** A
ground with an artifact behind it can be looked up and disagreed with. **A ground with nothing
behind it becomes visible as such**, which is the whole of what this limb can achieve and is worth
more than a bar no reader could apply.

**The list is a publication input, and the count remains not a gate number.** Reading the list under
this limb neither makes the manifest's leaking-source **count** a gate quantity nor admits it to any
denominator — (k3) governs, and §6.2 line 446's manifest requirement is unamended. **Because the
gate now reads that list, the manifest is an object the gate consumes: the declaration enumerates it
in the SC-8(a) freeze, and its recorded status is not `DRAFT` at the tag.** A list that invites its
own later revision cannot decide a gate outcome; an author review that silently made a complete
reconciliation incomplete would be a change to a gate input outside the class C route.

**(k3) A DISCLOSURE, NOT A CLASSIFICATION — AND THE LIMIT OF WHAT A READER CAN CHECK.** **A
reconciliation published under this limb is a disclosure, not a classification entering a criterion,
denominator, or count** (a). It derives nothing, changes no class, and no quantity appearing in it is
N. That sentence is load-bearing: without it (a) forbids the very comparison that makes the
denominator auditable, and the limb would contradict the clause it sits in.

**What a third party can and cannot do with it, stated plainly rather than implied.** The declared
map and this reconciliation are published with the registration; **the acceptance fixture is not,
and no clause requires it to be.** So a reader can check the reconciliation for **completeness**
(every manifest-classed leaking source accounted for), for **internal consistency** (each ground
citing a registered predicate), and for **provenance** (each ground naming an artifact and
location) — and **cannot** independently verify a classification against the fixture's data. **This
limb is therefore a disclosure obligation with limited external verifiability, and it is registered
as one.** Claiming it delivers an audit a reader cannot perform would be the same defect as an
overstated availability claim.

**(k4) WHAT MAKES THIS LIMB FAIL.** This limb fails where the REQUIRED list is empty on a declared
side; **or where the reconciliation is absent**; or where any difference in it is unnamed, is named
without the registered predicate that produced its class, **or is named with a ground that cites no
artifact and location (k2)(i)**; **or where the manifest the reconciliation reads is not enumerated
in the declaration's SC-8(a) freeze, or carries a `DRAFT` status at the tag (k2)**. *(Both of those
last two are conditions (k2) states, and until R60 neither was indexed here — a limb may not impose
a condition and leave nothing to enforce it. **Both are unmet as at the date of this amendment**:
the freeze's "specifically and exhaustively" list does not name the manifest, and the manifest's
recorded status is still `DRAFT - author review required`.)* **This is a live gate item, not a check that only fires on
corruption: it can fail on an artifact that is behaving correctly, and on the fixture as declared at
the date of this amendment it is UNSATISFIED.** The declaration publishes a per-unit
cross-tabulation of the construction-SOURCE cut against the gate cut, which is a different pair of
partitions; it publishes no per-unit reconciliation against the manifest's leaking-source list. The
difference the limb would surface is **fourteen units**.
```

**Why.** Registered §6.2 states four criteria (lines 459–462) and nowhere states the population they are evaluated over or the rule that assigns a unit to it. Concretely, nothing registered stops a unit being moved into or out of criterion 1's denominator after a result is seen: SC-4(f)(3)'s printed partition check, SC-4(h)'s mandatory re-derivation and SC-4(i)'s stop-and-report are the only machinery in the amendment that makes the denominator auditable rather than asserted. Two things the author should weigh before signing. (1) This clause carries R32, and R32 is not cosmetic: as originally drafted SC-4(a) required the *declaration* to state the class predicates, which the registration's own checker forbids — rule 9 of tools/check_registration.py (working-tree copy 30d3ad4c…7425, lines 617–632) matches the regex `\*\*[A-Z][A-Z][A-Z _-]*\*\*\s+iff\b` and fires on AVAILABILITY_DECLARATION.md lines 1052/1054/1056. The R32 form inverts the obligation — predicates registered in (b), cited per unit by row, never restated — so the specification no longer requires a companion document to contain text the specification's own tooling rejects. Signing the pre-R32 form would have registered a self-contradiction. (2) Direction is strictly stronger, not a relaxation: the declaration may do less (cite) and must show more (per-unit declared facts), and 'derived ... never assigned by hand' is retained. Open item disclosed in the source and not drafted (SCHEMA_SET_FINAL.md lines 1660–1664): REQUIRED and OUT OF JURISDICTION are contradictories under SC-3(d)'s side-relative map, so a unit satisfying both is a declaration defect rather than a precedence question; (c) and (i) do not say so. That is a residual gap the author is accepting, not one this hunk closes.

**Class.** Class C — new clause inserted, no registered sentence replaced. K2 ledger table (c), row '§6.2, after line 464 | SC-4'. Ground: §0.2.1 line 93 (constitutes a denominator and what a published gate number means).

### 2.17 — `PREREG.md` 464 (insert after, following the SC-4 block) — immediately before line 466 · SC-5 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Secondary findings on **manifest-listed descendants** of a true leaking source remain permitted on `fixture_contaminated`; they neither satisfy criterion 1 nor enter criterion 2.

**What changes.** THE CLAUSE 'Adjudication routing — v30a [SC-5]', limbs (a)–(f), is inserted below the SC-4 block and above line 466's v19 parenthetical. Pure insertion — no supersession marker; criteria 1, 2 and 4 stand byte-exact.  **Placement:** written after the SC-4 block and immediately before line 466.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**Adjudication routing — v30a [SC-5]**

**(a) EVERY FINDING IS CHARGED TO EXACTLY ONE CRITERION, BY THE CLASS OF THE UNIT IT NAMES.** The
gate needs one answer per finding. Routing is derived from the unit's gate class (SC-4) and the
map's disposition of the cell (SC-3), and from nothing else.

**(b) ATTRIBUTION IS TO THE GROUND, NOT TO THE NAME.** A REQUIRED entry is satisfied only by a
finding **on the side, in the cells, and on the ground the map declares.** **Criterion 1 is not
satisfied by unit name alone.** Where a unit has two grounds — one the map declares violating, one
declared legal — **the gate class follows the violating ground**, the legal ground is recorded as a
fact and not applied, and **a finding on the legal ground does not satisfy the REQUIRED entry.** It
is recorded on its own ground, and not credited to the unit's REQUIRED status. Naming the right unit
on the wrong ground satisfies nothing.

**(c) THE FALSE-POSITIVE CONSEQUENCE ATTACHES TO THE OUT-OF-JURISDICTION CLASS AND TO NO OTHER.** An
availability-class finding on an out-of-jurisdiction unit is a **declared false positive**, recorded
as such in the gate report. **It is not converted into a failure of the clean-source criterion**,
which has no landing site for such a unit; that criterion's scope is the units the declaration
declares clean, and those units **do** route to it. **The false-positive consequence is never
carried beyond the out-of-jurisdiction class.**

**(d) A FINDING ON A CHARACTERIZED SIDE IS CHARGED TWICE ONLY WHERE THE CRITERIA ARE INDEPENDENT.**
Where a finding is a false positive under (c) **and** contradicts the map on a characterized side,
it is charged under both the false-positive tally and criterion 3, and the report says so. Where two
criteria would otherwise adjudicate the same finding on the same ground, the declaration states
which one governs, ex ante.

**(e) JURISDICTION BETWEEN DETECTORS IS DECLARED, AND A BOUNDARY CUTS BOTH WAYS.** Where a finding's
character belongs to a detector row **outside** the criteria this gate scores, the declaration
assigns it to that row and it is **neither credited nor penalized here.** Routing it into this gate
would let a finding of one character masquerade as a finding of another and corrupt both counts.
**The assignment is declared before any detector runs; it may not be made after seeing where the
findings landed.**

**(f) DECLARED SENTINELS UNDER THE IDENTITY CONTROL.** An as-built artefact of the fixture that is
**present identically on every side** is **data content, not a finding**: it cannot differentiate
the sides, and a detector firing on it has produced a **false positive under the identity control.**
Such artefacts are **enumerated in the declaration ex ante**, with their signature; a sentinel
claimed after a firing is not a sentinel.
```

**Why.** The registered gate has exactly one routing sentence, and it covers exactly one case: line 464, the anchor SC-4 sits on, says descendants' secondary findings 'neither satisfy criterion 1 nor enter criterion 2'. Every other finding's charge is left to convention. Three concrete holes this closes, each verifiable against registered text. (i) Line 460 scopes criterion 2 to a '**manifest-clean** source column'. A false positive on a unit that is neither manifest-clean nor a ground-truth leaker therefore fails no registered criterion at all — the gate can be passed while emitting it. SC-5(c) fixes the false-positive consequence to the OUT OF JURISDICTION class and states in terms that criterion 2 'has no landing site for such a unit', so the consequence is recorded where it belongs instead of evaporating. (ii) Line 459 requires attribution 'to the labelled source' — that is a *name* test, not a *ground* test. As registered, a finding that names the right column for a reason the map does not declare violating satisfies criterion 1. SC-5(b) closes that: 'Criterion 1 is not satisfied by unit name alone', and a finding on a unit's legal ground is not credited to its REQUIRED status. (iii) Line 462 is criterion 4 in its entirety — 'Silent under the identity control on both.' — with no rule about artefacts present identically on every side. SC-5(f) requires such sentinels to be enumerated ex ante with their signatures and declares a firing on one a false positive under the identity control; without it, criterion 4 is decided after the fact by whoever describes the firing. Note also SC-5(e): detector jurisdiction must be assigned before any detector runs, 'may not be made after seeing where the findings landed' — the same ex-ante discipline as SC-8(c), applied to routing. Not making this clause leaves the gate's arithmetic well-defined only for the one case line 464 happens to name.

**Class.** Class C — new clause inserted, no registered sentence replaced. K2 ledger table (c), row '§6.2, after line 464, following SC-4 | SC-5'. Ground: §0.2.1 line 93 (changes what an acceptance criterion requires and which criterion a finding is charged to).

### 2.18 — `PREREG.md` 468 · SC-7 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Top-k presence does not satisfy criterion 1. An alias satisfies it only if recorded before the run.

**What changes.** A new clause block, "The gate's input surface — v30a [SC-7]", limbs (a)-(e), is inserted after line 468 and before line 470's "What this gate does and does not guarantee, said plainly." No registered sentence is replaced; there is no supersession marker.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**The gate's input surface — v30a [SC-7]**

**(a) AT GATE TIME A DETECTOR RECEIVES EXACTLY TWO THINGS, FOR ONE SIDE AT A TIME:** the pipeline
for that side, and the availability declaration's **declared elements** (§2.3, §2.4, §2.9).
**Nothing else.**

**(b) IT NEVER RECEIVES, AT ANY POINT IN A GATE RUN:** the paired side or any artifact derived from
it; the paired side's stored predictions or any statistic derived from them; **the declared
ground-truth map**, nor any summary, cohort list, restriction, or per-cell count derived from it.

**(c) WHY THE MAP IN PARTICULAR IS WITHHELD.** Under criterion 3 the map **is** the scoring key. A
detector that could read it would be graded against a key it had seen, and the run would measure
**retrieval rather than discrimination**. The map is an artifact of the harness, not an input to the
tool. **A run that received the key has not produced a gate result, whatever it reports.**

**(d) ONE SIDE AT A TIME IS A HARD SEQUENCING RULE, NOT A CONVENTION.** The criteria are per-side,
and each is evaluated from a run that saw only its own side. **A single run given more than one side
satisfies none of the criteria, however its outputs are partitioned afterwards.**

**(e) THE SURFACE IS DECLARED AND FROZEN WITH EVERYTHING ELSE (SC-8).** Widening it — including by
supplying a derived summary "for convenience" — is a class C amendment, not a harness detail.
```

**Why.** §6.2 registers what must be TRUE of the findings — the four criteria at lines 459-462 — and nowhere registers what the thing being evaluated is allowed to SEE. A search of all 1,099 lines for the natural terms ("ground-truth map", "input surface", "receives exactly", "one side at a time", "blinded", "withheld") returns one hit, line 896, and it governs the deferred REVIEW adjudication rubric, not the gate. So the surface genuinely is unregistered. Two things go wrong without this clause, and both are gate-fatal rather than cosmetic. FIRST, the scoring key is unprotected. Under SC-3 the declared ground-truth map IS criterion 3's scoring key. Nothing registered forbids handing it, or a per-cell count derived from it, to a detector; a harness convenience would suffice. A run that read the key measures retrieval, and line 470 states the gate's whole purpose as "It gates **discrimination**" — without SC-7(c) that stated purpose is unenforceable by the registration, and a key-fed run is still reportable as a gate result. SECOND, the per-side criteria can be satisfied by after-the-fact partitioning. Criterion 2 reads "on `fixture_contaminated`" (line 460) and criterion 3 "appears on `fixture_corrected`" (line 461); both are per-side predicates over outputs, not over runs. A single run given both sides, whose outputs are split afterwards, satisfies the text of both. SC-7(d) closes that as "a hard sequencing rule, not a convention". What the author is buying: SC-7(e) makes any widening of the surface — including supplying a derived summary "for convenience" — a class C amendment, so a future harness change that helpfully passes a cohort list becomes an amendment, not a detail. What he must know before signing: SC-7 is not severable. SC-7(a) cites §2.9, which exists only if SC-1 is adopted, and SC-7(c)'s premise is false against registered criterion 3 and true only under SC-3.

**Class.** C — §0.2.1 line 93, "anything that changes what a published number means" (it constrains what the gate may consume, so it changes what a gate outcome is a measurement of). K2 table (c): "§6.2, after line 468 | SC-7 | the gate's input surface and the one-side-at-a-time sequencing rule | C".

### 2.19 — `PREREG.md` 480 · SC-8 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **Ordering, locked:** tune on the development corpus → freeze the candidate configuration → run the fixture gate → tag the same unchanged configuration, or stop. Defaults may not be altered after observing a fixture result.

**What changes.** The marker "§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED" is placed at line 480's site and the clause "The freeze, and what 'declared ex ante' requires — v30a [SC-8]", limbs (a)-(f), is inserted after it. Line 480 itself stands byte-exact.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED.** The locked ordering stands byte-exact. SC-8
states what the ordering ranges over and what happens when a frozen object is later found wrong,
which line 480 left unstated.
**§11 items 1–7 — v30a, EXTENDED.** Item 8 is added: it indexes the freeze (SC-8) and amends item
3's hash set; SC-8(f) states the requirement generically and does not fix a count.

**The freeze, and what "declared ex ante" requires — v30a [SC-8]**

**(a) EVERYTHING THE GATE CONSUMES FREEZES AT THE AMENDED REGISTRATION'S TAG.** At the moment the
tag is signed, every object a gate outcome can be computed from becomes **locked**, and any
subsequent change to any of them is a class C amendment requiring a further amended registration.
**The declaration enumerates the frozen objects exhaustively**; an object the gate consumes and the
enumeration omits is a defect in the enumeration, not an object outside the freeze.

**(b) WHAT FREEZES IS THE OBJECT IN ITS AUDITABLE FORM — LISTS, NOT COUNTS.** A partition freezes as
its **enumerated lists of member names**, a map as its **rows**, an exclusion as **the named unit and
its ground**. A count is not a freeze: a count admits substitutions that a list forbids, which is the
whole difference between a frozen partition and a frozen number.

**(c) EX ANTE MEANS CHECKABLE BEFORE ANY DETECTOR RUNS.** Every declared object the gate consumes —
the map, the partition, the exclusions, any declared cohort or restriction — must be **regenerable
and checkable from the declared inputs alone, before any detector runs.** An object that can only be
confirmed after a run is a description of the result, not a declaration; a cohort so confirmed is a
key shaped by results.

**(d) A SCOPE CHOICE IS JUSTIFIED INDEPENDENTLY OF ITS EFFECT ON ANY NUMBER.** Where the declaration
restricts a scope — a class set, a cohort, a population — the justification **makes no reference to
what the restriction does to any count, and none may be added to it.** A restriction adopted for its
effect on a number is a restriction shaped by that number, which is the failure line 480 forbids in
the large.

**(e) A NUMBER FOUND WRONG AFTER A RESULT IS NOT CORRECTED IN PLACE.** *(Citation, not restatement:
§0.2.1 line 99 governs.)* It is recorded, an amended registration is committed, and the affected
benchmark is regenerated as a new version under §6.4 with the superseded results published
alongside. **In-place correction after a result has been observed is precisely how a fail becomes a
pass.**

**(f) THE FREEZE IS ONLY AS GOOD AS THE INTEGRITY CHAIN THAT CARRIES IT.** Every file the freeze
ranges over — **including the declaration itself, which carries the scoring key** — is hashed in the
amended registration's tag message as committed, and the count of hashes is **derived from the set
of registered files, never stated as a literal**. A tag that hashes the specification but not the
declaration the specification is evaluated under is an integrity chain with a hole exactly where the
amendment lives, and **an amendment weaker than the thing it amends is not one** (§0.2.1 line 97).
```

**Why.** Line 480 locks an ordering, but read literally it ranges over the CONFIGURATION only: "freeze the candidate configuration", "tag the same unchanged configuration", "Defaults may not be altered after observing a fixture result". Everything else a v30a gate outcome is computed from is outside it — the declared map (SC-3(a)), the three-class partition and N (SC-4(b),(f)), the declared exclusion grounds (SC-4(e)), the unscored ledger (SC-6(b)). None of those is a "default", so each may today be revised after a fixture result while line 480 remains formally satisfied. That is the defect (a) closes, and it closes it fail-closed: an object the gate consumes and the enumeration omits is "a defect in the enumeration, not an object outside the freeze". Limb (b) is the one to read twice, because it is where the money is: SC-4(b) registers "**N is the length of the REQUIRED list**". If what freezes is N rather than the list, membership can be substituted while N is preserved and every published check still reconciles — (b) forbids exactly that by freezing "enumerated lists of member names", not counts. Limb (e) is a citation, not a new rule, and the author should see precisely how it extends line 99: line 99 fires on a class C change "discovered after the affected detector already exists"; (e) fires on a number found wrong "after a result has been observed", which is a later and different trigger that line 99 does not cover on its face. Limb (d) forbids justifying a scope restriction by its effect on any count — the small-scale form of the failure line 480 forbids in the large. What the author is buying: after the v30a tag, correcting any frozen object is a further amended registration and the affected benchmark is regenerated under §6.4 with superseded results published alongside. There is no in-place fix path left.

**Class.** C, carried with SC-8. K2 table (c): "§6.2, after line 480 | SC-8 | the freeze ... | C"; the site marker is K2 table (b): "§6.2 line 480 — ordering, locked | extended ... | SC-8 | carried with SC-8".

### 2.20 — `PREREG.md` 816 (insert one paragraph after line 816, before line 818) · SC-13c (§13c-P, second insertion point) · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

**What changes.** A single pointer paragraph, blank line each side, is inserted into §7.2.1 between line 816 and line 818. It says the suppression clause above is subject to one express, scoped exception stated in §10.2 (v30a) [SC-13c(c2)], that SC-13c(c2) governs the exception and is not restated here, that line 816 governs as registered everywhere else, and that the registered relationship between line 816 and §7.4's line 830 over the same state is recorded in the v30a amendments block and unchanged by the exception. Line 816 itself is not edited.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a) [SC-13c(c2)].** That clause states which quantities the exception reaches and what is published for them; it governs the exception wherever this sentence is applied and is not restated here. Everywhere outside it, this sentence governs exactly as registered. The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is recorded in the v30a amendments block and is not changed by the exception.
```

**Why.** Without this paragraph the kill criterion is silently disarmed at the point of implementation. Line 816 as registered (verified verbatim above) tells an implementer standing in §7.2.1 to suppress the yields, rates and **gates** of any combination that is `not_applicable` on every scope-eligible case. SC-13a(a2)'s threshold is exactly such a gate, and SC-13b(b3)'s whole disposition of that state — execute to terminal §6.6 states, publish counts and reason, compute the defined zero yield, trip and publish the STOP — is the opposite instruction. Nothing at line 816 would tell that implementer the exception exists; §10.2 is 214 lines away and a reader working in the runtime-formula section has no reason to go there. The result is the failure mode the criterion exists to prevent: the one fixture state in which the detectors provably cannot separate the sides is also the state in which the gate reports nothing. The paragraph adds no rule of its own — it is deliberately reduced to H8's form (name where the governing text lives, say it governs at this site, do not restate it), which is what keeps §0.2.1 line 77's single-normative-source rule intact: SC-13c(c2) stays the one normative copy of the exception's scope, authority and publication requirement. The second sentence earns its place separately: an implementer who reads line 816 and then §7.4 line 830 ("a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss") meets a genuine registered conflict, and the pointer tells him it is known, recorded in the amendments block, and deliberately not resolved here — rather than letting him discover it and resolve it himself at run time.

**Class.** Pointer — adds no rule; carried with SC-13c's class C. K2 §8.2 table (d), "§7.2.1 after line 816 (to the exception SC-13c(c2) states)", with the reading change recorded at table (b). §13c-P records the anchor as a full-line match, count 1, as read this pass; re-derive after any earlier edit lands.

### 2.21 — `PREREG.md` 855 (replace) — the retained v30 row is placed as a NOT-operative marker after the table, i.e. after line 856 · SC-6 · replace-row

**Anchor (verified byte-exact) — the registered line as it stands:**

> | **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived` |

**What changes.** §7.7's detector-case coverage row is re-registered with `unscored` appended, and the v30 row is retained verbatim, marked NOT operative, in a supersession marker placed after the table. Applied form (recovered from the scratch applied file, not quoted in SCHEMA_SET_FINAL — see findings): `| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived`, `unscored` |`

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§7.7 line 855 — SUPERSEDED BY v30a. Registered v30 row, retained verbatim, NOT operative:**
"| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`,
`could_not_run(reason)`, `waived` |"
*Superseded because the six-state list has no state for a unit the declaration declares
unscoreable. Absent such a state, an unscoreable unit is forced into `not_applicable` (which reads
as "the question does not arise") or into a pass — which is the failure the state exists to stop.*
```

**Why.** The registered row carries six states and none of them fits a unit the declaration declares unscoreable before any detector runs. That is not a vocabulary preference — line 858, the sentence directly under the table, registers that 'assert_audit_complete() operates on **detector-case coverage states only.**' A state absent from this row cannot be recorded, asserted on, or reported at all, so an unscoreable unit is forced into `not_applicable` (which reads 'the question does not arise') or absorbed into a pass. That absorption is the exact failure the rest of the schema set is built to stop: SC-3(b)'s third disposition ('A cell the map does not cover is UNSCORED (SC-6) ... never reported as a pass'), SC-4(b)'s third class row and SC-4(c)'s 'UNSCORED wins' precedence all cite SC-6. If this row is not replaced, three adopted clauses reference a coverage state the registration does not carry, and the UNSCORED disposition they depend on has nowhere to be recorded. Verified free of conflict with the other §7.7 hunk: Y3_WAIVED_ENTRY_CONDITION.md line 164 records that SC-12(w) 'does not touch that row — it leaves `waived` in the vocabulary on purpose (w6)', so SC-6 alone owns line 855.

**Class.** Class C on §0.2.1 line 93's own words ('a needed *new* … coverage state'). K2 ledger table (a), row '§7.7 line 855 — detector-case coverage row | superseded: the row is re-registered with `unscored` | SC-6 | C — line 93's "coverage state"'.

### 2.22 — `PREREG.md` 856 (insert after the table) · SC-6 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> | **Strategy diagnostic** | `completed`, `optional_strategy_failed`, `required_strategy_failed` |

**What changes.** THE CLAUSE '`unscored` — a coverage state, v30a [SC-6]', limbs (a)–(e), is inserted after the §7.7 table (below the supersession marker), giving the new state its semantics, its entry condition, its two levels, and its gate consequences.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**`unscored` — a coverage state, v30a [SC-6]**

**(a) SEMANTICS.** A unit is **`unscored`** when the declaration declares, **before any detector
runs**, that scoring it is impossible on a stated ground. An `unscored` unit **requires no finding
and forbids none.** It **enters no denominator**, **contributes to no rate**, and **cannot be
reported as a pass.** It is neither a pass nor a not-run: the detector may have executed perfectly
and there is still nothing to score.

**(b) ENTRY CONDITION — declared, never inferred.** A unit may be reported `unscored` **only if it
appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector
runs.** A unit may not enter this state because a run produced nothing, because data was missing at
run time, or because a result was surprising. **Absence of data at run time is not `unscored`; it is
the not-run state its cause selects** (§8.2). *(This entry condition is stated explicitly because
§7.7's `waived` was registered without one — see SC-12.)*

**(c) TWO LEVELS, AND THEY DO NOT COLLAPSE.** The state exists at the **cell** level of the declared
map (SC-3) and at the **unit** level of the declared partition (SC-4). **A cell-level `unscored`
never makes its unit `unscored`**, and a unit-level `unscored` does not make every cell of that unit
unscored. A gate report states which level each `unscored` entry is at.

**(d) FINDINGS ON `unscored` UNITS ARE NOT FALSE POSITIVES.** They are reported as **unscored
observations**, separately from the false-positive tally, and they carry no criterion consequence in
either direction. **The three gate classes are never folded into one another**, and a report that
pools them has not scored the fixture.

**(e) THE PASS PROHIBITION IS ABSOLUTE.** A report that counts `unscored` units or cells as clean,
as covered, or as passing **has converted absence of data into evidence**. `unscored` entries are
named as unscored, never as clean, and §8.2's rule governs their display: none may be displayed in a
way mistakable for a pass.
```

**Why.** The row hunk alone adds a word to a list. It does not say what the word means, who may enter the state, or what the gate does with it — and the registration already contains a worked example of what that costs: `waived`, the state immediately beside it in the same row, was registered in v30 in exactly that form, and repairing it now takes a whole separate clause (SC-12(w)). SC-6(b) is the limb that prevents the repeat: a unit may be reported `unscored` 'only if it appears, by name, in the declaration's unscored ledger, with its ground, frozen before any detector runs', and 'Absence of data at run time is not `unscored`; it is the not-run state its cause selects (§8.2)'. Without (b) the state is enterable after the fact and becomes a place to put surprising results. SC-6(c) is load-bearing for the arithmetic, not housekeeping: SC-3 partitions *cells* and SC-4 partitions *units*, so without the explicit non-collapse rule a single unscored cell would unscore its whole unit and silently drop it from criterion 1's denominator — the removal SC-4(d)(ii) forbids by name. SC-6(e) is what keeps the state from being counted as coverage. Consequence of not making this hunk while making the row hunk: `unscored` exists as a token with no entry condition and no gate meaning, which is strictly worse than not adding it. One apparatus defect to note before signing — see findings: the drafting note kept beside this clause (SCHEMA_SET_FINAL.md lines 582–585) still asserts that §7.7's `waived` 'still has none after this amendment', which SC-12(w) makes false.

**Class.** Class C — new clause inserted, no registered sentence replaced. K2 ledger table (c), row '§7.7, after the table (line 856) | SC-6 | C'. Ground: §0.2.1 line 93's 'coverage state'.

### 2.23 — `PREREG.md` insert after PREREG.md line 856, following SC-6's semantics block · SC-12(w) consequential — the §7.7 pointer, redrafted (Y3 §6.3); replaces the H8 draft · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> | **Strategy diagnostic** | `completed`, `optional_strategy_failed`, `required_strategy_failed` |

**What changes.** The pointer after §7.7's table reads, in full: "**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here." This displaces the drafted H8 text (`PREREG_v30a_DIFF.md` line 393), which reads: "**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table. **The conditions under which a detector-case may be reported in this state are not defined by this registration**; defining them is a class C change, and until it is made no case may be reported as `waived` on the strength of the state merely existing in this table." The matching descriptor in table (d) of the block changes in the same tag, from "no entry condition for the coverage state is defined by this registration" to "**SC-12(w)** is its entry condition".

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**`waived` is defined in §10.2 (v30a).** That definition governs the word wherever it appears, including this table, and **SC-12(w) registers the condition under which a detector-case may be reported in this state.** Neither is restated here.
```

**Why.** This redraft is mandatory, not cosmetic. The H8 text asserts that the entry condition "are not defined by this registration" and that "until it is made" no case may be reported waived — a sentence that presupposes the class C change has not been made, when SC-12(w) in the same tag is that change. Ship both and v30a carries two registered texts disagreeing about whether the entry condition exists, at the exact site of the defect being fixed (Y3 §6.3; residual risk 6: "is load-bearing and is not optional … it must be applied in the same tag"). The replacement keeps the pointer a pointer: it states no prohibition of its own, so the single normative copy of the entry condition stays in SC-12(w), as §0.2.1 line 77 and SC-9(f) require. Anchor verified: line 856 is the last row of §7.7's table, line 857 is blank, so "after the table" is line 856. Line 855 — the coverage row the pointer's subject sits in — is separately superseded by SC-6, and SC-12(w)(w6) deliberately leaves `waived` in that row's vocabulary.

**Class.** — (pointer; adds no rule of its own). The rule it points to, SC-12(w), is C under §0.2.1 line 93's "coverage state". Ground: block table (d); K2 §3 row R25.

### 2.24 — `PREREG.md` 892 · SC-11 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> **Conformance cases contribute to no detection metric.** Under a too-permissive declaration a genuine leak *correctly* produces no finding relative to that declaration; counting it as a true negative would improve the clean-case rate while the tool missed real leakage.

**What changes.** A new §7.8 sub-block "The all-zero control — v30a [SC-11]", limbs (a)-(g), is inserted after §7.8's closing paragraph and before §7.9's heading at line 894. Every aggregate returning zero / all-clean / empty must be cross-checked against its source before it may be written down; on mismatch the check raises rather than warns; a surviving zero is reported with the check named and the population it is zero over.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**The all-zero control — v30a [SC-11]**

**(a) AN EMPTY AGGREGATE MUST BE PROVED EMPTY BEFORE IT MAY BE REPORTED.** Any aggregate that
reports zero violations, zero findings, all-clean, "no cells", "no rows", or an empty result set
**is automatically cross-checked against its source artifact before that result may be written down,
printed, or reported.** The check is not optional, not a spot check, and not run only when the
result looks surprising — it runs on **every** such aggregate, because a broken aggregation and a
genuine zero are indistinguishable at the point of reading.

**(b) MINIMUM SUFFICIENT FORM OF THE CHECK.** Assert that **every key the aggregation groups or
filters on resolves to a real field with a non-empty domain in the source**, and that **the source
is non-empty on those keys**; where a total is available by a second route, reconcile the two.

**(c) ON MISMATCH THE CHECK RAISES.** It does not print a warning, does not annotate the output, and
does not continue. **A warning next to a zero is read as a zero; an exception is not read as
anything, which is the point.** A zero that survives the check is reportable and is reported **with
the check named**, so a reader can tell a proved zero from an unproved one.

**(d) SCOPE — THIS BINDS GATE REPORTING, NOT ONLY THE ARTIFACT THAT PROMPTED IT.** It applies
wherever a zero or an all-clean is produced in this programme: **the gate report's per-criterion
counts and its false-positive tallies**; any re-derivation of the declared map or of any restricted
view of it; any per-class, per-side, per-cell or per-unit aggregation; and **any statement that a
unit, class, cell or criterion is clean.**

**(e) AN UNEXPECTED ALL-ZERO IS A FINDING, NOT A PASS.** Where a declared expectation predicts
non-zero and the aggregate returns zero, **the zero is a finding about the aggregation or about the
declaration — and never a pass.** It is reported as such and adjudicated before any gate outcome is
written.

**(f) A ZERO OVER A PARTIAL POPULATION IS NOT A ZERO OVER THE POPULATION.** A measured zero over a
subset of the declared class set, the declared sides, or the declared cells **is not the same
predicate** as a zero over the declared whole, and **no row of such a table may be quoted as a
pass.** Every such figure names the population it is zero over.

**(g) THIS COMPOSES WITH THE DISPOSITIONS ALREADY DECLARED; IT SOFTENS NONE OF THEM.** Unscored
cells remain unscored and never clean (SC-6); excluded units remain excluded and are never reported
as missed; the control adds only that even a reportable zero must first be shown to be a measurement
rather than an artefact of a broken key.
```

**Why.** The anchor is the right home and it is also the argument. Line 892 already registers one case where an empty result must not be read as a good result — a genuine leak that correctly produces no finding under a too-permissive declaration "would improve the clean-case rate while the tool missed real leakage." SC-11 generalises exactly that reasoning to every zero the programme publishes. The gap is real and measurable in the registered text: §8.6 line 961 governs provenance for numbers that exist ("Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval…") and says nothing at all about a number that comes back empty. Under criterion 3 as SC-3 re-registers it, a zero-violation aggregate IS a pass claim — so an aggregation broken at the key level and a genuinely clean side are indistinguishable at the point of reading, and the broken one silently reads as a pass. Limb (c) is the limb that decides whether this is worth anything: a warning beside a zero is read as a zero, an exception is not read as anything. Limb (f) closes the partial-population route (a zero over a subset is not the same predicate as a zero over the whole). Without this hunk the gate can be passed by a broken GROUP BY, and nothing in the registration would catch it.

**Class.** C — new clause inserted, no registered sentence replaced. K2 block table (c): "§7.8, after line 892 | SC-11 | the all-zero control over every empty aggregate and every pass claim | C". K2 working row R26 gives the ground expressly: "C — under criterion 3 a zero-violation aggregate is a pass claim" (§0.2.1 line 93: it changes what an acceptance criterion requires).

### 2.25 — `PREREG.md` 915 (marker at its site, after the line) · SC-6 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. None may be displayed in a way mistakable for a pass.

**What changes.** Marker M2 is added at §8.2's site: '§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED. §8.2's list is the *not-run* subset and stays correct as far as it goes; `unscored` joins it, and §8.2's closing sentence governs it unchanged.' Line 915 itself is not edited.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED.** §8.2's list is the *not-run* subset and stays
correct as far as it goes; `unscored` joins it, and §8.2's closing sentence governs it unchanged.
```

**Why.** §8.2 is the section that governs how every non-pass state may be displayed — its closing sentence, verified on line 915, is 'None may be displayed in a way mistakable for a pass.' But §8.2's own enumeration is the not-run subset (`not_applicable`, `unsupported`, `could_not_run(reason)`), and `unscored` is expressly *not* a not-run state (SC-6(a): 'the detector may have executed perfectly and there is still nothing to score'). Once §7.7's row carries `unscored`, the amended file holds two coverage-state lists that no longer agree, and the display prohibition can be argued not to reach the new state — the argument SC-6(e) exists to foreclose, since SC-6(e) itself defers to '§8.2's rule governs their display'. The marker states the relationship as extension rather than supersession, so line 915 stands byte-exact while its scope is fixed on the record. Without it, SC-6(e) points at a rule whose reach over `unscored` is contestable.

**Class.** Marker only — registered text stands byte-exact. K2 ledger table (b), row '§8.2 line 915 — not-run states | extended: `unscored` is governed by this section's closing sentence, by reference to §7.7's row | SC-6 | carried with SC-6'.

### 2.26 — `PREREG.md` 915 (insert after, following marker M2) · SC-6 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Per §7.7, coverage states are `not_applicable`, `unsupported`, and `could_not_run(reason)` with reason `crash` | `alignment` | `compatibility` | `determinism` | `control_artifact`. The boundary: **missing or impossible inputs are unsupported; supplied-and-valid inputs that then fail are could-not-run.** An `unsupported` entry may name a **covering detector**; that reduces the gap and does not close it. None may be displayed in a way mistakable for a pass.

**What changes.** The S2(i) INSERTION TEXT — one paragraph, blank line each side — is inserted into §8.2 after marker M2. It names `unscored` in §8.2 by citation to §7.7's row and SC-6, states that §8.2's boundary sentence does not reach it, restates none of SC-6(a)/(b), and re-scopes §8.2's closing sentence in open form: it ranges 'by reference to §7.7's row and not to the enumeration in this section alone, over every detector-case coverage state that row carries other than `passed` and `failed`.'

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**`unscored` — §7.7 (v30a) [SC-6] — is governed by this section's closing sentence as well.** It
is neither a pass nor a not-run: this section's boundary sentence does not reach it, and its entry
condition and semantics are SC-6's, not restated here. It is named here so that this section and
§7.7's row cannot name different states — the closing sentence above ranges, by reference to
§7.7's row and not to the enumeration in this section alone, over every detector-case coverage
state that row carries other than `passed` and `failed`.
```

**Why.** This is the only hunk in my scope that carries a live discretionary choice, and the author should decide it rather than wave it through. What it buys: drift protection of the kind HISTORY.md H-L13 records — a state added to §7.7's row by any future amendment falls under §8.2's display rule the moment it is added, with no second edit to re-bump. Enumerated cross-references are the failure mode H-L13 names, and §8.2 vs §7.7 is exactly that shape today. What it costs: the open form also reaches §7.7's `waived`, which §8.2 does not name today, so a `waived` entry may not be displayed in a way mistakable for a pass. That is strictly stronger and consistent with SC-12, but the ground given for it in the drafting record is now STALE and the author should not rely on it: SCHEMA_SET_FINAL.md line 1931 calls the effect 'vacuous in practice under H8', on the premise that no case may be reported `waived` at all until an entry condition is registered. SC-12(w) registers that entry condition in this same tag, so the effect is live, not vacuous. The decision is therefore: adopt a live display constraint on `waived` as a deliberate act. If the author prefers §8.2 to name `unscored` only, SCHEMA_SET_FINAL.md line 1933 gives the exact strike point — 'strike the final clause from "the closing sentence above ranges" onward' — and the drift protection is then lost. Note the substantive dependency: without this paragraph in some form, §8.2 governs display of a state list that no longer matches §7.7's, and SC-6(e)'s deferral to '§8.2's rule' has no textual hook in §8.2.

**Class.** Pointer — a cross-reference adding no rule of its own, per K2 ledger table (d): '§8.2 after line 915 (`unscored` under this section's closing sentence, by reference to §7.7's row)'. Carried with SC-6 (class C). Note the open-form re-scoping is a rule effect on `waived` even though the row is classed as a pointer — see findings.

### 2.27 — `PREREG.md` 929 · SC-12(w) · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> - **`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings.

**What changes.** §8.3's third assertion bullet is replaced so the failure set becomes `unsupported`, `could_not_run`, or `waived`. The registered v30 bullet is retained verbatim at the site in a SUPERSEDED BY v30a block, marked NOT operative, with the recovery command `git show prereg-v30:PREREG.md`.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§8.3 line 929 — SUPERSEDED BY v30a, carried with SC-12(w).** Registered v30 text, retained
verbatim, NOT operative: "- **`assert_audit_complete()`** — fails on any `unsupported` or
`could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable
(§6.10). Ignores findings." *Superseded because SC-12(w) prohibits the `waived` state and a
prohibition no assertion tests is not enforced. Recover the registered line byte-exact with
`git show prereg-v30:PREREG.md`.*

- **`assert_audit_complete()`** — fails on any `unsupported`, `could_not_run`, or **`waived`** **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings. *(`waived` added v30a, carried with SC-12(w), whose (w1) prohibits the state outright; the assertion is what makes that prohibition checkable rather than merely stated.)*
```

**Why.** Verified byte-for-byte: line 929's failure set is `unsupported` and `could_not_run` and nothing else. That is the difference between a prohibition and a guard. Without this hunk SC-12(w) registers that no detector-case may be reported `waived`, and a non-conforming report that emits one passes all three of §8.3's assertions untouched — because no runtime metric reads the state either (line 820), the only thing standing between a floor breach and a green run is a human noticing that (w7)'s published count is not zero. Y3 §7 residual risk 1 states that consequence plainly. Shipping the guard and the enforcement in the same tag is the difference between a rule and a rule that is checked. The containment argument is measured, not assumed, and is worth the author's attention because it is what makes this hunk cheap: `assert_audit_complete()` has no implementation (the reducer implements `evaluate_runtime_assertions` for `assert_no_proven_leakage` only); the token `waived` appears zero times in `protocol/runtime_reference.py`, zero times in `tools/check_registration.py`, and zero times in `tests/registration/EXPECTED_OUTPUTS.md`; its one suite occurrence is `tests/registration/test_invariants.py::test_no_runtime_metric_touches_detector_case_state`, which asserts the reducer must NOT name it — an invariant this hunk preserves, because §7.7's detector-case layer is deliberately outside the reducer, per line 820's own words. The change is one registered sentence and cannot cascade. CAUTION: adopting this hunk falsifies Y3 §2 bound (6) as drafted ("alters no assertion in §8.3") — see findings.

**Class.** C — registered text superseded, retained verbatim at its site. K2 block table (a): "§8.3 line 929 — `assert_audit_complete()` failure set | superseded: `waived` joins `unsupported` and `could_not_run` | operative bullet at its site; carried with SC-12(w) | C — line 93's 'coverage state' | schema pass; the prohibition SC-12(w) registers".

### 2.28 — `PREREG.md` 961 · SC-11 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> Any rate names its `VALIDATED_CONFIG` section, its corpus or partition, its mode and evidence basis, its *n*, its interval, the availability declaration in force, and — for runtime rows — the probed-cohort count and row coverage. Non-holdout author-produced numbers say so in the same line.

**What changes.** A one-paragraph pointer (S2(iii)) is inserted after §8.6's only sentence: a zero, an empty result, or an all-clean statement is a published number and carries provenance under §8.6; the control it must survive and what it must name are stated in §7.8 (v30a) [SC-11] and are not restated.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**A zero, an empty result, or an all-clean statement is a published number and carries provenance
under this section.** The control it must survive before it may be reported, and what it must name
when it is, are stated in §7.8 (v30a) [SC-11] and govern here; they are not restated.
```

**Why.** This is the hunk that makes SC-11 reachable from the section a report author actually consults. §8.6 is titled "Every published number states its provenance" (line 959) but its one operative sentence, line 961, is entirely about rates — config section, corpus, mode, evidence basis, n, interval, declaration, probed-cohort count. A reporter following §8.6 has no reason to think a bare zero is in scope, and SC-11 sits three sections away in §7.8. Without this pointer the strongest reading of the registration is that §8.6 governs rates and SC-11 governs zeros, with no registered link, and a published zero can satisfy §8.6 by carrying nothing at all. The pointer's discipline is the point: it brings zeros, empties and all-cleans under §8.6 by name and then stops, so SC-11(c)'s "reported with the check named" and SC-11(f)'s "names the population it is zero over" keep a single normative copy (§0.2.1 line 77; SC-9(f)). If it restated (c) or (f) it would create the second copy it exists to avoid. Verify at signature that it is a pointer and adds no rule — that is its whole warrant for being class-neutral.

**Class.** Pointer — adds no rule of its own; carried with SC-11. K2 block table (d): "§8.6 after line 961 (a zero, an empty result, or an all-clean statement is a published number; SC-11 governs what it must survive and name)". SCHEMA_SET_FINAL Part 3(iii) records the pristine anchor match count as 1.

### 2.29 — `PREREG.md` 992 · C1 operative row (§10 Phase 1 gate cell) — drafted at R39/F2 · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> | **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |

**What changes.** The Phase 1 gate cell is replaced. **Phase, Work and Est. are byte-identical; only the Gate cell changes.** The registered *"both fixture AUCs reproduce within ±0.010, full and sliced"* is replaced by: a two-limb reference anchor, **both limbs labelled REGRESSION GUARDS with what each guards against stated**; the separation as a **published context figure with no pass/fail consequence** (R49/R1); the sliced variant discharged and scored under §6.2's own ex-ante rule; the alignment controls and snapshot hashing carried unchanged; and a closing sentence naming **which items carry the row's pass/fail evidence**.

**PROVENANCE, and a defect this hunk carried until R49.** The text above is read directly out of `J3_C1_REDRAFT.md`'s operative row at build time. Until the R49/R6 verification, this hunk carried the **WITHDRAWN** C1 — the draft J3 replaced over four defects — and every build since J3 rendered withdrawn text into the signable artifact while every check reported green. The checks verify manifest → hunk → artifact; this is a manifest **section-B** hunk whose source is a drafting round rather than `SCHEMA_SET_FINAL.md`, and **no check bound it to that source.** Eleven hunks share the exposure; `_R49_B2_check.py` installs the binding.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; **the reference anchor holds on both limbs**: *(i)* **AGREEMENT — this limb CANNOT FAIL while the fixture is unchanged, and FAILS on substitution, regeneration or corruption of it, which would move the recomputed entry off the figure the originating experiment recorded. It is therefore NOT evidence that this gate was met, and remains capable of failing it.** Each declared reference-anchor entry is compared against that figure **for the same `(side, instrument, architecture, horizon_s, tier)`** — the key stated in full because it is **the join key across two artifacts, neither of which carries all five fields**: the originating record is keyed `(instrument, architecture, horizon_s, tier)` and is one-to-one on those four, while `side` selects which declared entry is being compared and is not a column of it. `(horizon, side)` alone selects 16 rows spanning 0.5420–0.9662, **42× the tolerance below**, and dropping `tier` leaves three rows per combination whose 30s values are 0.8299 / 0.8564 / 0.8666 — **two of the three fail ±0.010 against the declared entry, so the key decides the outcome.** `tier` is the declared **L2**; `side` selects the declared entry and is not a column of the originating record. Any entry that does not reproduce its figure within ±0.010 absolute **fails this gate row**. An entry whose originating figure is **unavailable** fails this gate row **unless the declaration registered that entry ex ante as having no originating counterpart and stated why** — a ground declared before any Phase 1 measurement, never after one; *(ii)* **INTEGRITY — likewise incapable of failing on an unchanged fixture, and failing on byte corruption of the committed fixture or a changed AUC routine; likewise not evidence that this gate was met** — each entry is recomputed from the fixture's committed bytes and must equal its declared value exactly, a deviation of any size being a defect in the recomputation and a stop-and-report; **the declared pre-fix/post-fix separation is stated per horizon and side as a PUBLISHED CONTEXT FIGURE, carrying no pass/fail consequence** (R49/R1); **the sliced variant's Phase 1 CI obligation is discharged and the variant is scored under §6.2 (v30a) "Sliced variant — operative"**, whose ex-ante scoring rule governs it, with its slice boundaries declared; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed **WHAT SHOWS THIS ROW WAS MET** is the sliced variant, the four alignment-control cases, the snapshot hashing, and the §10.0 ordering and claims-verified clauses. **Limbs (i) and (ii) cannot show it was met — neither can fail on an unchanged fixture — but either can still fail it, and a failure of either denies the row.** |
```

**Why.** K2 §9.1's retention text asserts "Only the Gate cell is changed in the operative row above" — an operative row that was never drafted. Without it the retention block quotes a row that is still live in the table three lines above it: two contradictory readings at one site, which is the defect retention blocks exist to cure. The Gate cell also reads on two superseded objects — "both" names the anchor pair H2 retires, "sliced" names the artifact H4 moves off the Phase 0 fixture — so leaving it registered means Phase 1's gate tests a retired anchor and an artifact no longer in the fixture. The alternative K2 §9 records (reject C1, drop the ledger row, revert line 992) is available and leaves both defects standing; it is not taken.

**Class.** C (consequential) — derived from §A.1 and §A.4; carried with H2 and H4. Ledger table (a): §10 line 992.

### 2.30 — `PREREG.md` 998 (retention block written after the phase table; retains line 992) · K2 §9.1 — C1 retention block (§10 line 992, Phase 1 gate cell) · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> | **7** | Profiles, docs, v1.0 | 1–2 wknds | `futures` and `generic` profiles ship |

**What changes.** Immediately after the phase table's last row, blank line each side and before the weekend-total sentence at line 1000, a blockquote appears retaining PREREG.md line 992 in full (Phase, Work, Est. and Gate cells) marked `SUPERSEDED BY v30a, consequential to §6.2 lines 445 and 451 … NOT operative`, with the retirement reason ("both" names the retired anchor pair of line 445; "sliced" names the artifact line 451 moves off the Phase 0 fixture) and the `git show prereg-v30:PREREG.md` recovery command.  **Order (R39/F2):** written AFTER the C1 operative row replaces line 992.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
> **§10 line 992 (Phase 1 gate cell) — SUPERSEDED BY v30a, consequential to §6.2 lines 445 and 451. Registered v30 row, retained verbatim, NOT operative:** "| **1** | Availability model and profiles; **verification of §0.3 Claims A–C and the §6.10 comparator cases**; fixture harness and manifest; padded slicer; evaluation generator and conformance suite frozen; detector protocol; report skeleton; the three controls and the determinism guard | 2–3 wknds | §10.0 ordering followed; claims verified or a deviation filed with the measurement; both fixture AUCs reproduce within ±0.010, full and sliced; **all four alignment-control cases behave as §6.5 requires**; snapshots hashed |" *Retired because its Gate cell reads on two superseded objects: "both" names the retired anchor pair of line 445, and "sliced" names the artifact line 451 moves off the Phase 0 fixture and re-registers as a Phase 1 CI obligation. Only the Gate cell is changed in the operative row above; Phase, Work and Est. are byte-identical. Recover the registered row byte-exact with `git show prereg-v30:PREREG.md`.*
```

**Why.** Without this hunk the amendment is internally false. H1's C1 rewrites line 992's Gate cell one-for-one and the v30 text survives nowhere — "both fixture AUCs reproduce within ±0.010, full and sliced" occurs in no other place in the amended file — while the block inserted by hunk N2 states, as item 1, "**No registered sentence is deleted from this file.**" and heads table (a) "each retained verbatim at its site, NOT operative". Every other supersession in (a) does retain its v30 text; 992 and 1022 are the only two that do not. K2-F1 records this. I verified the retained quote character-for-character against PREREG.md line 992 (526 characters, exact match), and verified the placement anchors: line 998 is the table's last row, 999 is blank, 1000 is the weekend-total sentence. The retention sits in a blockquote rather than in the table, so `check_phase_arithmetic`'s `^\|\s*\*\*(\d)\*\*` row regex still parses exactly 8 phase rows. The author's alternative is to reject C1 outright (H1's stated alternative), which drops the 992 row from (a) — but then the Phase 1 gate keeps a requirement reading on two retired objects.

**Class.** C (consequential) for the paired rewrite of line 992; the retention block itself asserts no new semantics — it is the mechanism that makes the block's item 1 true. Ground: §0.2.1 line 93 via K2 §3 row R29; retention form is the one H2–H5 use.

### 2.31 — `PREREG.md` 1022 (retention block written beneath item 3; retains line 1022) · K2 §9.2 — C2 retention block (§10.1 line 1022, kill-gate criterion 3) · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> 3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;

**What changes.** One blockquote line at the list's three-space indentation, directly beneath the operative item 3 and before item 4, retaining PREREG.md line 1022 verbatim, marked `SUPERSEDED BY v30a, consequential to §6.2 line 461 … NOT operative`, with the retirement reason (it is a second copy of the premise line 461 retires — that silence on the corrected side is correct behaviour) and the recovery command. The ambiguity branch is noted as carried through unchanged.  **Order (R39/F2):** written AFTER the C2 operative item replaces line 1022, so the retention quotes text that is no longer live above it.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
> **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461. Registered v30 text, retained verbatim, NOT operative:** "3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;" *Retired **as to its corrected-side limb only**, because that limb is a second copy of the premise criterion 3 (line 461) retires — that silence on the corrected side is the correct behaviour. Under SC-3 the corrected side is characterized, never clean, and a tool silent where the map declares a violation is silent where it should fire. **The contaminated-side limb and the ambiguity branch are carried into the operative item byte-identical** (R47/P1); the contaminated-side tightening an earlier draft carried is withdrawn from v30a and deferred (R47/P2, H-39). Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

**Why.** The same defect as C1 and the same fix. Line 1022's v30 text survives in the amended file only as a three-word fragment inside SC-3's marker ("is silent on `fixture_corrected`"), so without this hunk the block's item 1 is false of a second line. I verified the retained quote byte-exact against PREREG.md line 1022 (214 characters, exact match) and the placement: line 1023 is `4. Installs and runs through a documented public interface without author modification;`, so the retention lands between items 3 and 4 as §9.2 states, in the placement SC-3's marker already uses under §6.2 criterion 3. Note the interaction the author should see: SC-13a's marker says line 1022 "is **not** amended by these clauses", which is true of SC-13a–c but could be read as saying line 1022 is unamended when C2 does amend it under SC-3 (K2-O4 proposes a one-clause clarification).

**Class.** C (consequential) for the paired rewrite of line 1022; the retention block itself asserts no new semantics. Ground: §0.2.1 line 93 via K2 §3 row R30.

### 2.32 — `PREREG.md` 1022 · C2 operative item (§10.1 kill-gate criterion 3) — drafted at R39/F2 · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> 3. Fires on `fixture_contaminated` and is silent on `fixture_corrected` **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;

**What changes.** §10.1's criterion 3 is replaced so that the CORRECTED-SIDE limb asks the question SC-3 registers — whether a candidate's findings MATCH the declared map — instead of whether the candidate is SILENT there. **The contaminated-side limb "Fires on `fixture_contaminated`" is carried forward byte-identical to registered v30, and the ambiguity branch is carried byte-exact, em-dash included** — both verified at R47/P1 against `PREREG.md` line 1022 as read from disk.

**Scope, and why it is this narrow (R47/P1–P2).** An earlier revision of this draft also displaced the contaminated-side limb, rewriting it from EXISTENTIAL (“fires” — one finding anywhere on the contaminated side) to UNIVERSAL (“match the map on **every** fixture side” — a per-cell match across the whole declared scored population, plus a two-sided false-positive prohibition). That tightening is **not reached by this clause's stated reason**, which is entirely about the corrected side, and **no sentence of the amendment disclosed it**. It is WITHDRAWN from v30a and recorded as a candidate for a future amendment carrying its own stated reason and its own ledger row (HISTORY.md H-39). It may well be defensible on its merits; a tightening whose reason appears nowhere in the amendment carrying it is how a registration stops being trustworthy, and being defensible is not the test.

The C2 retention block beneath item 3 preserves the superseded item verbatim. **Order (R39/F2):** this REPLACE is applied first; the retention blockquote is then written directly beneath the resulting operative item 3, before item 4.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
3. Fires on `fixture_contaminated`, and on `fixture_corrected` its runtime findings match the fixture's declared ground-truth map — findings the map predicts are required, findings it excludes are false positives, and cells the map does not cover are unscored — **under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**;
```

**Why.** §10.1's criterion 3 is a second copy of the premise §6.2's criterion 3 retires — that silence on the corrected side is correct behaviour. Under SC-3 the corrected side is CHARACTERIZED, never clean, so a tool silent where the map declares a violation is silent where it should fire. Left registered, a candidate tool could satisfy the kill gate by exhibiting exactly the behaviour the acceptance gate now scores as a miss — and the kill gate is the criterion that decides whether this project stops. The retention block presupposes an "operative item 3" that was never drafted; without it the block quotes text still live directly above it.

**Class.** C (consequential) — derived from §A.8; carried with SC-3. Ledger table (a): §10.1 line 1022.

### 2.33 — `PREREG.md` 1030 · SC-13a · replace

**Anchor (verified byte-exact) — the registered line as it stands:**

> 2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**

**What changes.** PREREG.md line 1030 — §10.2 kill/pause criterion 2 — is replaced by the SC-13a criterion (heading plus limbs (a1) unit, (a2) threshold, (a3) denominator), preceded at the same site by a conditional supersession marker that retains the v30 sentence verbatim and keeps it operative wherever §6.2's ambiguity branch has NOT fired. The enumeration's `2.` marker and the three-space indentation of the continuation block (lines 1031–1035) are preserved; lines 1031, 1033 and 1035 are untouched.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§10.2 criterion 2, line 1030 — v30a, SUPERSEDED ON THE AMBIGUITY BRANCH ONLY. Registered v30
text, retained verbatim, operative where the branch has NOT fired:**
"2. **The runtime detectors cannot separate contaminated from corrected fixture under the
reconstructed declaration** → **stop.**"
*Not deleted, and not superseded generally. Line 1031 already registers the disposition this
marker performs — "this criterion is replaced, not deleted" — so where §6.2 line 449's ambiguity
branch has not fired, the sentence above is the operative criterion and SC-13a–c do not apply.
Where it has fired and been recorded, SC-13a is the operative criterion for that fixture, with
SC-13b and SC-13c inseparable from it. Recover the registered line byte-exact with
`git show prereg-v30:PREREG.md`.*

**NOT SUPERSEDED, stated so the marker's scope cannot be widened by reading:** line 1031 (the
branch and the before-tuning rule), line 1033 (the three-part obligation and the
no-`DEVIATIONS.md`-only rule), line 1035 (the floor). **Line 816 is not superseded**: its text
stands byte-exact; SC-13c(c2) states an express, scoped exception to its suppression clause for
this criterion's required quantities only, its publication clause is kept and required, and a
pointer to the exception is inserted at line 816's own site (SC-13c, second insertion point).
**§6.2's four acceptance criteria are not amended by these clauses** (SC-13c(c6)) — SC-13a–c
*depend on* the amendment this registration makes to §6.2 criterion 3 and do not make it
(SC-13c(c1)).

**Consequential — §10.1 criterion 3, line 1022.** The Phase 0 kill gate's third condition already
carries the ambiguity branch on its face ("**or, where the fixture is semantically ambiguous
(§6.2), under the labelled hypothetical declaration**") and is **not** amended by these clauses:
§10.1 scores a *third-party tool*, SC-13a scores *this project's* runtime detectors. Named here so
the two are not conflated during application.

**2. Where the fixture is semantically ambiguous, the runtime detectors must reach a non-zero
per-side proof yield on every detector — v30a, operative on the ambiguity branch. [SC-13a]**

This criterion replaces the criterion above wherever §6.2's ambiguity branch has fired and been
recorded in Phase 0, and it is evaluated **under the labelled hypothetical declaration that branch
requires**, on the frozen default configuration, with the declaration's scoring key withheld from
every detector. **SC-13b's admissibility test is applied first, before any detector runs.** The
limbs of SC-13a and SC-13b are conjunctive, and **failure of any of them is a stop**; a criterion
evaluated in breach of SC-13c(c4)'s execution requirement is not discharged.

**(a1) UNIT.** The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime
scoring unit, and the quantity computed over it is **proof yield**, as §7.2 defines it. **The
yield is computed per runtime detector and per declared fixture side**, and each of those figures
is published separately. *"Per detector, per side" partitions the computation; it does not
redefine the unit, and it does not narrow the denominator — see (a3).* **This unit is a declared
alternative to the descriptive fixture unit of §6.2**, adopted deliberately and on the record,
because the pair is the unit proof yield is already registered in and the floor's first limb is
stated in proof-yield terms.

**(a2) THRESHOLD.** For **each** runtime detector the floor governs (the set SC-13c(c3) pins), on
**each** declared side, the `preserving` combination's proof yield must be **strictly greater than
zero** — `proof yield > 0`. **This is the floor of line 1035 taken literally and applied per
detector and per side rather than once globally.** It is not a chosen number and it may not be
tuned: there is no selection procedure to shape, which is what makes it committable before any
development-corpus contact. **A threshold met by any route other than a preserving intervention
reaching PROVEN under a passing determinism guard does not satisfy this limb.**
**Every quantity this limb gates is defined and every gate it states is evaluated.** SC-13b(b2)
requires the labelled-unit set to be non-empty on every declared side of every governed detector,
so no denominator this limb reads is empty and no undefined yield arises; SC-13b(b3) and
SC-13c(c2) provide that neither this gate nor the yields it reads are suppressed under `PREREG.md`
line 816. **Each governed `(detector, preserving)` combination is executed to a terminal result on
every declared side and reported under its actual §6.6 states — never under §7.7's `waived`
coverage state.**
**This limb is unconditional on every declared side, including the side the fixture declares
corrected.** It is not scoped, softened, or suspended by any acceptance criterion, by any
jurisdictional routing statement, or by any per-side asymmetry in the declaration. Where an
acceptance criterion and this limb appear to disagree about the corrected side, the disagreement
is resolved by SC-13c(c1)'s named dependency and by nothing else.

**(a3) DENOMINATOR — THE REGISTERED ONE, UNNARROWED.** The yield of (a2) is computed over **the
denominator §7.2 registers for proof yield — all scope-eligible labelled pairs — with
scope-eligibility as §7.4 defines it, taken unnarrowed.** **This clause cites that denominator and
does not restate it**; a second normative statement of it here would leave the registration with
two copies of one denominator and no canonical source.
**This clause declares no stricture on that denominator, and performs no narrowing, restriction,
projection, exclusion, or re-aggregation of it.** The two partitions (a1) names are terms the
registered denominator already carries and are not narrowings of it: **per detector** is §7.4's
own scope-eligibility term read at the detector row whose metric is being computed —
scope-eligibility being "a property of the corpus label, not of what the detector could do about
it" — and **per side** is §7.2's body-of-data scope applied to each declared fixture side.
**The labelled-unit set SC-13b requires is what INSTANTIATES this denominator, never what
restricts it.** The declaration supplies which pairs the corpus labels and which detector's risk
kind each is labelled for; that is the instance data the registered denominator is defined over.
**A declaration may not use the enumeration to remove from the denominator a pair the corpus
labels and the risk logically applies to** — that is a narrowing, it makes the criterion easier to
pass, and line 1035 forbids a replacement weaker than the floor. **If a stricture on this
denominator is ever genuinely necessary, it is declared in terms in the amendment text, justified,
and tested against line 1035 — never introduced by a citation to a denominator it does not use. No
other denominator is nominated.**
```

**Why.** This is the hunk that discharges a registered obligation the author is otherwise carrying unmet. PREREG.md line 1033 (verified verbatim) reads: "On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0)." Line 1031 registers that on the ambiguity branch criterion 2 "is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning**". §6.2 line 449 is the branch trigger ("If the original work did not document prediction timing, the fixture is recorded as semantically ambiguous ... See §10.1 criterion 3 and §10.2 criterion 2"). Without this hunk the registration holds the instruction to replace, the obligation to carry a complete replacement, and the floor to measure it against — and no replacement text anywhere. That state cannot be cured later by a DEVIATIONS.md entry (line 1033 forbids it by name) and cannot be cured after development-corpus contact (line 1031), so the window to sign it closes at first corpus contact. What the author is signing on the merits: (a2) takes line 1035's first limb — "non-zero proof yield" (line 1035 verified verbatim) — literally and applies it **per governed detector and per declared side** rather than once globally, which is strictly stricter than the floor and therefore admissible under line 1035's "may be stricter ... may not be weaker". (a3) cites §7.2 line 791's registered denominator ("proof yield = correct PROVEN pairs ÷ **all scope-eligible labelled pairs**") and §7.4 line 830's scope-eligibility, and forbids narrowing it — both cited exactly. The threshold is `> 0`, unselectable and untunable, which is what makes it committable before corpus contact as line 1031 demands. One drafting defect to weigh before signing: (a1)'s attribution of the unit to §7.2 does not match §7.2's registered unit table — see findings.

**Class.** C — §0.2.1 line 93 ("a needed *new* branch, unit, denominator, coverage state, tier licence, or **acceptance criterion**"), read for a kill criterion; carried by an amended registration under line 95, never a DEVIATIONS.md entry standing alone. Superseded on the ambiguity branch only; K2 §8.2 table (a), row "§10.2 line 1030 — kill/pause criterion 2".

### 2.34 — `PREREG.md` 1035 (after SC-12's inserted block; before line 1036) · SC-13b · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

**What changes.** The SC-13b admissibility block (limbs (b1)–(b4)) is inserted inside §10.2 criterion 2's continuation block at its three-space indentation, after line 1035's floor paragraph and after the block SC-12 inserts at the same anchor. No registered sentence is replaced. Line 1036 (criterion 3) still follows, so §10.2's enumeration 2 → 3 → 4 → 5 is unbroken.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**ADMISSIBILITY FOR THE CRITERION ABOVE — v30a [SC-13b]. Tested before any detector runs, and
before any limb of the criterion.**

**(b1) THE DECLARED SET.** A semantically ambiguous fixture may discharge the criterion above only
if the declaration enumerates, **by name, before any run, and frozen with everything else the gate
consumes**, a **non-empty labelled-unit set for each runtime detector the floor governs** — the
governed set is pinned at SC-13c(c3) and is not the declaration's to choose. **If any governed
detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is
STOP.** The stop is lifted only by supplementing the declaration with a declared, enumerated set
for the empty detector and re-freezing under §11's integrity chain — never by scoring the
criterion on the remaining detector, never by suppressing the empty detector's gate, and never by
a `DEVIATIONS.md` entry or a working resolution.

**(b2) THE DECLARED SET, PER SIDE.** The set's partition by declared fixture side is itself gate
input, and **the labelled-unit set must be non-empty in every (governed detector) × (declared
side) cell**. A cell that is empty — a governed detector whose set is non-empty overall but empty
on one declared side — **trips the same STOP as (b1), lifted the same way and only that way**: by
supplementing the declaration with declared, enumerated units for that detector on that side and
re-freezing under §11. An empty side is **nothing declared to score** on a body of data the
criterion gates — the admissibility genus (b1) already occupies, not the threshold genus — and
disposing it instead as a scored zero would put a defined value on an empty denominator, which
§7.2.1's own registered rule refuses: "**Undefined, not 0% or 100%, at an empty denominator.**"
**Consequence, stated so no reader ever decides it: every per-side denominator SC-13a(a2) reads is
non-empty, every yield it gates is defined, and the undefined 0/0 case cannot arise.**

**(b3) THE `not_applicable`-EVERYWHERE STATE — DISPOSED, NOT SUPPRESSED.** A governed combination
that is `not_applicable` on every scope-eligible case of a declared side, over a declared
non-empty labelled-unit set, is **not** an empty set: (b1) and (b2) do not fire, because there is
something declared to score. Its disposition is this, in full:
the combination is **executed and reported to terminal §6.6 states**, and its counts are published
naming the reason — line 816's publication clause, kept and required; its labelled pairs **stay in
the registered denominator as misses**, as §7.4 line 830 provides; its `preserving` proof yield on
that side is therefore **zero — a defined 0/N over declared units, not a 0/0**; **zero fails
SC-13a(a2)'s strictly-greater-than-zero threshold, and the STOP is tripped and published.**
**SC-13a(a2)'s gate is NOT suppressed by `PREREG.md` line 816.** For the quantities the criterion
requires, line 816's suppression clause does not apply — the express, scoped exception SC-13c(c2)
states and the amendments block records. **The `not_applicable` finding is PUBLISHED, never
suppressed**: the counts, the named reason, the computed zero yield, and the gate outcome are all
published together. **The exception rests on two grounds and on no other.** *First*, it is a class
C change to how line 816 reads at this one criterion, made on this amendment's own authority and
recorded in the v30a amendments block (SC-13c(c2)). *Second*, this is a kill criterion over the
detectors' capability: a combination that never applied on a declared side cannot separate the
fixture sides, so a gate suppressed on that fact is a detector waived on it (SC-12's definition: a
detector is waived when its result is made "incapable of changing the criterion's outcome"), and
line 1035 forbids the waiver.
**The two stop genera stay distinct and are never pooled**: (b1)/(b2) stop for an **admissibility
reason** — nothing declared to score; (b3) stops through the threshold for a **detection reason**
— declared units, terminal execution, and no proof. The two stops are reported under their own
limbs.

**(b4) WHY THIS TEST EXISTS, AND WHAT MAKES IT A TEST RATHER THAN A FORMALITY.** A detector whose
declared labelled-unit set is empty **cannot change the criterion's outcome**, which is the
defining condition of a waiver under the floor's own definition. Three run conditions produce an
empty set or cell, and each is a real state of a real fixture rather than a defect:
**(i)** the fixture contains no dependency of that detector's kind — on the affected side, none
that reaches it — so there is nothing for the declaration to enumerate; **(ii)** the detector's
required declaration is absent or its applicability mode is not selected, so it returns a not-run
state on every case and the declaration has no model under which to enumerate units; **(iii)**
every unit that could carry that detector's character is declared EXCLUDED or `unscored` on a
stated ground, so none survives into the enumeration. **In all three the criterion is silently
satisfiable by the other detector alone, and this clause converts that silence into a stated
outcome.**
**One state the superseded drafts listed as a fourth condition is not one, and is removed.** A
declaration that assigns every unit of a detector's character to the other detector's jurisdiction
*within the criterion's own scope* is not an independent run condition: where the risk logically
applies to the reassigned unit, the reassignment is the narrowing SC-13a(a3) forbids in terms; and
where it does not, the state just is condition (i). Either way it adds nothing to this list, and
keeping it would list a prohibited act as a "real state rather than a defect".
```

**Why.** Without this hunk SC-13a is a gate that can be reached with nothing to compute it over. Three verified registered facts make that concrete. (1) §7.2.1 line 810 registers, for the empty denominator: "**Undefined, not 0% or 100%, at an empty denominator.**" So if a governed detector's labelled-unit set is empty on a declared side, SC-13a(a2)'s `proof yield > 0` has no value to test — an undefined quantity sits in a kill gate and the reader, not the registration, decides what happens. (2) Silence there is not neutral: a criterion satisfiable by the remaining detector alone is precisely SC-12's waiver limb (iii) ("the criterion can be satisfied by another detector's output alone", verified in SC-12's clause text), and line 1035's second limb — "neither runtime detector waived" — forbids it. So the degenerate case does not merely produce an awkward number; it produces a replacement criterion weaker than the floor, which line 1035 makes inadmissible on its face. (b1)/(b2) convert that into a declared STOP, liftable only by supplementing the declaration and re-freezing under §11 — never by scoring on the surviving detector and never by a DEVIATIONS.md entry. (3) The hard case (b3) disposes is the `not_applicable`-everywhere combination, which line 816 would suppress; (b3) uses §7.4 line 830 verbatim in substance ("a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss") to keep the labelled pairs in the denominator, producing a defined 0/N that fails (a2) and trips a published STOP. (b3) also keeps the two stop genera separate — admissibility (nothing declared to score) versus detection (declared units, terminal execution, no proof) — so the gate report never pools an empty fixture with a blind detector. What the author gets by signing: after this clause no degenerate state reaches SC-13a undisposed and no 0/0 can arise; what he gives up is the option of running the criterion on a partially-enumerated declaration.

**Class.** C — carried as one amendment with SC-13a under §0.2.1 line 93/line 95; K2 §8.2 table (c), row "§10.2, after line 1035, following SC-12 | SC-13b". Pure insertion — no registered sentence retired; SC-13b's own marker section states "None — insertion, not supersession", and lines 816, 830 and 570 stand byte-exact and are cited.

### 2.35 — `PREREG.md` 1035 · SC-12 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

**What changes.** The clause "'Waived', defined — v30a [SC-12]" is inserted immediately beneath the floor, preserving §10.2 criterion 2's three-space indentation (confirmed present on the anchor line). It carries the definition blockquote with limbs (i)-(v), the governed-set paragraph, the "may not be invoked" paragraph, the seven-item "does NOT permit" list, and — new at DELTA R35 B3 — limb SC-12(w) with sub-limbs (w1)-(w7), the entry condition for §7.7's `waived` coverage state.  **Order (R37/D3):** SC-12's block is written first at this site; SC-13b then SC-13c follow it, before line 1036.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**"Waived", defined — v30a [SC-12]**

The floor above uses the word without a defining clause, and the word appears again as a coverage
state in §7.7's table, also undefined. An undefined term inside a floor whose purpose is to stop
criteria being dropped silently is exactly the term that gets read permissively later. This adds the
defining clause.

> A detector is **WAIVED** with respect to a criterion when the criterion is written, configured, or
> reported in any way that makes the detector's own result **incapable of changing the criterion's
> outcome**. Concretely, a detector is waived if any of: **(i)** it is excluded from the criterion's
> denominator; **(ii)** it is in the denominator but its findings are not required to be non-empty
> for a pass; **(iii)** the criterion can be satisfied by another detector's output alone; **(iv)**
> its threshold is set at a level it meets without executing, or by construction; **(v)** its cases
> are reported under §7.7's `waived` coverage state rather than executed to a terminal result.

**Which detectors the floor governs is not the declaration's to choose.** They are the detector
rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination rule
gates — `PREREG.md` line 759's `Runtime, preserving` row and line 760's `Runtime, promoted` row,
and line 1039's "both of L2a/L3.1's combinations" — the same registered set SC-13c(c3) pins. Where
the fixture's declaration states the same membership, it is corroboration, not the source. The
declaration may not shorten the set, and a criterion or report written over fewer than all of the
governed detectors has waived the omitted ones.

**What invoking it requires: nothing, because it may not be invoked.** The floor is a **prohibition,
not a permission with conditions.** There is no procedure by which a detector the floor governs may
be waived in a replacement criterion. A replacement that waives one is weaker than the floor and is
out of specification on its face; **it does not become admissible by being recorded, disclosed,
justified, or approved.** Changing that requires amending the floor itself.

**What this definition does NOT permit.** (1) It is not an escape hatch of any kind and creates no
exception, justified, approved, or time-limited. (2) It does not reach any other criterion and may
not be cited to soften §6.2's. (3) **"Experimental" is not "waived"** — an experimental marking
changes how findings are labelled and asserted on; it does not remove a detector from a replacement
criterion's denominator, and a criterion that drops a detector *because* it was marked experimental
has waived it. (4) **"No data" is not "waived"** — a cell with no data is `unscored` (SC-6), and the
detector is still scored wherever data exists; doing at the level of a whole detector what SC-6
forbids at the level of a cell is a waiver. (5) **A working resolution or a `DEVIATIONS.md` entry
cannot do it** (SC-9(c), SC-9(e)). (6) **Per-combination waiving is still waiving**, and is class C.
(7) **It licenses nothing after tuning** — a criterion chosen because it works after tuning is a
criterion shaped by tuning.

**(w) ENTRY CONDITION FOR §7.7's `waived` COVERAGE STATE — a prohibition, and a closed list of licensed grounds with no members.**

§7.7's table carries `waived` as a detector-case coverage state and registers no condition under which a report may assign it. It is the only state in that table without one, and the omission is not cosmetic: **no runtime metric reads a detector-case state** (§7.2.1), and `assert_audit_complete()` reads it alone. A state the apparatus cannot bound by its consequences must be bounded at entry.

**The direction of the bound is forced by limb (v) above.** Limb (v) makes assignment of this state one of the ways a detector *becomes* waived. Any permissive entry condition would license, in the definition's own words, the act the definition exists to name. The bound is therefore drawn as a prohibition.

**(w1) THE CONDITION. NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE.** The grounds on which this state may be entered are exhaustively enumerated in this limb; the enumeration is **closed**, and it has **no members**. No ground may be inferred from silence, from practice, from a report's convenience, or from the state's presence in §7.7's table.

**(w2) EVERY DETECTOR-CASE TAKES THE COVERAGE STATE ITS CAUSE ALREADY SELECTS — cited, not restated.** §7.7's completion lock selects it where a terminal result is or is not reached; §8.2 draws the boundary between the not-run states and governs their display; SC-6(b) governs a unit the declaration declared unscoreable, by name, before any detector ran. Those rules dispose of every detector-case between them, and **the residue this state would have carried is empty.**

**(w3) THE STATE RECORDS A WAIVER; IT NEVER MAKES ONE — and this governs every ground ever added.** Waiving is a property of how a criterion is **written, configured, or reported** — something a criterion's design does to a detector, never something a run does to a case. The coverage state can therefore only ever be the **record** of a waiver registered text has already effected under limbs (i)-(iv); it is never that waiver's source. **A report does not create a waiver by asserting the state.** Accordingly **no ground added to (w1)'s enumeration may be constitutive**, and **limb (v) may never be a ground under (w1)**; nor may an availability declaration, a working resolution, a `DEVIATIONS.md` entry, the frozen configuration of §6.8, or an `assert_audit_complete()` recorded exception.

**(w4) THE PROHIBITION BINDS PER CASE AND PER COMBINATION.** A case may not be reported `waived` on one of §7.1's combinations and executed on the other. **Per-combination waiving is still waiving** (item (6) above).

**(w5) AN ENTRY THAT APPEARS IS A BREACH, AND LIMB (v) IS WHAT CLASSIFIES IT.** By limb (v) the detector is thereby waived with respect to every criterion the case feeds. Where that detector is one the floor governs and the criterion is §10.2's replacement criterion or any part of it, the replacement is weaker than the floor and out of specification on its face, and **it does not become admissible by being recorded, disclosed, justified, or approved.** Everywhere else the case has reached no terminal result, is **not complete** under §7.7's completion lock, may not be counted or displayed as complete, covered, clean, or passing (§8.2), and is re-reported in the state its cause selects — or the fixture is not scored.

**(w6) THE TOKEN IS NOT STRUCK FROM §7.7's TABLE.** The state stays in the vocabulary so that a report using it is **caught** by limb (v) and by this limb rather than silently accepted. Striking the name would leave the act unnamed, and limb (v) with nothing to classify.

**(w7) REPORTING OBLIGATION.** The gate report publishes the count of `waived` detector-case entries, **per detector and per combination**, as a count. **That count is zero.** A report that does not publish it has not discharged this limb: a prohibition whose observance is never published is not checkable.

**What this limb does NOT permit.**

**(1) It licenses the state in no case, and silence is not licence.** The empty enumeration is the whole of the permission. In particular, **a criterion's failure to name a detector licenses nothing**: a criterion that enumerates its detectors and omits this one, a criterion written before this detector existed, and a criterion that says nothing about detectors at all are **all silence for this purpose**. The omitted detector **bears on that criterion**, and its cases are executed to terminal results. Reading silence as licence would be waiving by omission — limbs **(i)** and **(iii)** above — and would move the licence from registered text to whoever last failed to update an enumeration.

**(2) A ground may be added only by a further class C amendment to this limb** (§0.2.1 line 93), committed and externally timestamped **before the affected detector is implemented or evaluated** (line 95), never after a fixture result is observed (§6.2 line 480; SC-8). Any such ground must be **declaratory** under (w3). **And no such amendment may license the state for a detector the floor governs at a §10.2 replacement criterion**: the floor forbids that above, there is no procedure by which it may be done, and this limb supplies none and may not be cited as one.

**(3) "No data" is still not "waived"** (item (4) above), and this limb creates no route by which it becomes so. A cell with no data is `unscored` where SC-6(b)'s declared-ledger condition is met; absence of data at run time is otherwise the not-run state its cause selects (§8.2). A run that produced nothing, a missing or impossible input, a crashed or failed strategy, and a surprising result are each disposed of there and by none of them does a case enter this state.

**(4) "Experimental" is still not "waived"** (item (3) above). A detector or mode shipped experimental under §10.2 criterion 3 executes its cases and reports their terminal results; the marking changes how findings are **labelled and asserted on**, never which coverage state a case takes.

**(5) Jurisdiction is not waiver.** What a jurisdictional routing statement reaches is settled at SC-13c(c6), cited and not restated. A boundary on **where a finding is charged** is never a licence to leave a case **unexecuted**.

**(6) It amends no other coverage state's entry condition and moves no boundary in §8.2.** It reaches §8.3 in exactly one way, deliberately: `waived` joins `assert_audit_complete()`'s failure set at line 929, so that emitting the prohibited state **fails an assertion instead of passing silently**. That is the whole of its reach into §8.3 — no other assertion changes, and no other coverage state's treatment changes. **`unscored` is not added to that failure set, and must not be**: `unscored` is a *permitted* state that honest coverage accounting produces, whereas `waived` is *prohibited* by (w1), so a report emitting it is non-conforming on its face. A prohibition no assertion tests is not enforced; a permitted state that failed an assertion would punish correct reporting.

**(7) It authorises no retro-fitting.** Text adopted or amended after a run does not reach a case already run, and a licence claimed after a case was reported is not a licence.

**(8) It licenses nothing after tuning** (item (7) above).
```

**Why.** The anchor line is the defect. Line 1035 makes "neither runtime detector waived" a locked floor on any replacement criterion, and the registration nowhere defines "waived." Verified by direct search: `waived` occurs exactly twice in all 1,099 lines — line 855 (§7.7's coverage-state row) and line 1035 (this floor). No producer, no consumer. An undefined term inside a floor whose entire purpose is to stop criteria being dropped silently is precisely the term that gets read permissively later, and the floor is live because R22's determination fired. The governed-set paragraph is the second half of the fix and must be checked against its pins, which I read this pass: line 759 "| **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; …", line 760 "| **Runtime, `promoted`** | L2a, L3.1 | **evidence yield** and the same family below the first row, computed over `dtype_promoted` findings only |", and line 1039 "both of L2a/L3.1's combinations — `preserving` and `promoted` — are gated independently." All three pins verify. This is what stops the declaration shortening the governed set, which would let a criterion written over one detector satisfy a floor that governs two. SC-12(w) closes the companion hole: §7.7's table registers `waived` as an assignable coverage state with no entry condition — the only state in that table without one — while line 820 registers that "**No runtime metric reads the detector-case state of §7.7**, which exists for `assert_audit_complete()` alone" and line 929 fails on `unsupported` and `could_not_run` only. In v30 as it stands, a report could assign `waived` to every case of a governed detector, breach line 1035's floor, and no published number and no assertion would move. (w1) makes the licensed-grounds enumeration closed and empty, and (w3) — the state records a waiver, it never makes one — is what keeps that closure from being widened by an ordinary later amendment. WHAT THE AUTHOR MUST DECIDE HERE: the applied (w) text in SCHEMA_SET_FINAL.md lines 998-1016 stops at (w7) and does NOT carry Y3's eight-item "What this limb does NOT permit" block, which Y3 declares part of the clause. See findings 1 and 2.

**Class.** C — new clause inserted, no registered sentence replaced; the floor stands byte-exact. K2 block table (c): "§10.2, after line 1035 | SC-12 | 'waived', defined; which detectors the floor governs; what the definition does not permit; and **SC-12(w)** … | C | declaration §A.12; schema pass". Ground: §0.2.1 line 93 — it fixes what a kill/pause criterion requires.

### 2.36 — `PREREG.md` 1036 (pure insertion immediately after SC-13b's block, still between line 1035's paragraph and line 1036) · SC-13c · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> 3. **Excessive false alarms on clean cases, under the default configuration** → the affected detector **or mode** ships marked experimental, is excluded from `assert_no_proven_leakage()` and `assert_no_rule_violations()`, and is labelled experimental wherever its findings appear.

**What changes.** The SC-13c interactions block (limbs (c1)–(c7)) is inserted immediately after SC-13b's block, at the same three-space indentation, still ahead of line 1036. No registered sentence is replaced and the enumeration is untouched.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**INTERACTIONS OF THE CRITERION ABOVE — v30a [SC-13c].**

**(c1) ADOPTION, AND THE ONE NAMED DEPENDENCY — ONE WAY.** The criterion (SC-13a with SC-13b and
this clause) is drafted against **§6.2 criterion 3 as amended by this registration** and **is not
adoptable without that amendment**: under registered line 461 unamended, SC-13a(a2)'s
corrected-side requirement is dischargeable only by failing §6.2 criterion 3, and a registration
cannot contain a kill criterion dischargeable only by failing an acceptance criterion. **The
dependency runs one way.** The criterion-3 amendment does not depend on these clauses and remains
admissible alone; adopting it without them leaves the registration consistent, adopting them
without it does not, and no reverse dependency is created here. Until the `prereg-v30a` tag is
signed, line 461 stands unamended and these clauses are not adoptable at all. A `DEVIATIONS.md`
entry or a working resolution cannot substitute for the amendment (line 1033; SC-12 item (5)).

**(c2) THE LINE-816 EXCEPTION — EXPRESS, SCOPED, AND RECORDED.** `PREREG.md` line 816, verbatim:

> **A combination that is `not_applicable` on every scope-eligible case in a body of data
> publishes its counts and suppresses its yields, rates, and gates**, naming the reason.

**For the quantities this criterion requires — the per-detector, per-side `preserving` proof
yields SC-13a(a2) gates, that gate itself, and the published yields (c4) requires — line 816's
suppression clause does not apply.** Its publication clause applies in full and is required:
counts published, reason named, and — for this criterion — the computed yield and the gate outcome
published with them, per SC-13b(b3). A gate suppressed on the `not_applicable`-everywhere fact is
a detector waived on it — SC-12's definition, head and limb (iii) — and line 1035 forbids the
waiver. **The exception rests on this amendment's class C authority and on that capability ground;
it does not rely on `PREREG.md` line 818, whose text stands as registered.**
**This is a class C change to how line 816 reads at this one criterion, it is recorded in the v30a
amendments block in terms, and it reaches nothing else**: everywhere outside this criterion, line
816 governs exactly as registered. **The registered conflict between line 816 and line 830 is NOT
resolved by this clause** — it is recorded in the amendments block as a duplicated-authority
defect and flagged for a future amendment; no reading of this clause settles it anywhere else.

**(c3) WHICH DETECTORS THE FLOOR GOVERNS IS NOT THE DECLARATION'S TO CHOOSE.** They are **the
detector rows §7.1's two runtime metric rows name, and which §10.2 criterion 3's per-combination
rule gates** — §7.1's `Runtime, preserving` and `Runtime, promoted` rows (lines 759 and 760), and
line 1039's "both of L2a/L3.1's combinations". The declaration supplies each governed detector's
labelled-unit set; it does not supply the membership of the governed set, may not shorten it, and
may not reach the same effect by enumerating a set for some of them and omitting the rest. **A
declaration that enumerates a set for fewer than all of the governed detectors has not discharged
SC-13b, and the criterion is not discharged.** SC-12, as revised with these clauses, pins the same
set to the same registered sites, and the two clauses never diverge on it.

**(c4) EVERY COMBINATION IS EXECUTED, AND NONE IS DROPPED.** Proof yield is registered for the
`preserving` combination only. A criterion stated in proof-yield terms therefore scores one
combination, and dropping the other from the criterion **waives that combination**. So: the other
combination is **executed to a terminal result on the same denominator and publishes its own
registered yield**, per detector and per side, and **no finding of that combination substitutes
for a proof the criterion requires**. Its published yield is a required output of the criterion
and carries no threshold of its own. Where that combination is `not_applicable` everywhere, (c2)'s
exception covers its required published yield the same way: executed to terminal states, counts
and reason and yield published, nothing suppressed.

**(c5) THE REMAINING FLOOR LIMBS ARE CARRIED BY CITATION, AND THIS CLAUSE NAMES WHICH VERSION IT
CARRIES.** Line 1035's second and third limbs remain in force over the criterion exactly as
written there. **Where "criterion 3's gates" admits more than one referent, every referent is held
in force** — they operate at different levels and do not conflict, and holding all of them is the
only reading that is not a weakening. **Each referent is held in the version this registration
leaves standing, and this clause says which:**
**(c5)(i) — the §6.2 referent is criterion 3 AS AMENDED BY THIS REGISTRATION**: the declared
ground-truth-map form that SC-3 registers as the replacement for `PREREG.md` line 461. **Its
scoring rule and its three dispositions are SC-3(b)'s, and **its map, its indexing, and what the
artifact publishing it may carry are SC-3(a)'s — all held by citation and none restated here.**
*(R49/B7: this clause previously restated (a)'s indexing triple in the same breath as declaring it
unrestated. R47/P5 then amended (a) and left the copy behind, so the copy became DIVERGENT — it
lacked (a)'s carve-out for artifact rows that are not cells of the map. Two normative copies of one
rule is §0.2.1 line 77's defect; the second copy silently going stale is why.)* **The cell key is
the declaration's to supply,
not this clause's to state**: SC-3(a) requires that a key exist and be declared and named; SC-3(h)
and SC-8 require it frozen with the map before any detector runs; and this clause names no key.
**It is never the pre-amendment prohibition on any finding on the corrected fixture**, and this
clause may not be read against that text.
**(c5)(ii) — the §10.2 referent is §10.2 criterion 3's own two named gates**, the finding-rate
gate and the completion gate, in force as registered and per combination, and **not amended by
this clause**.
**Why the version is named rather than left to the reader.** A clause whose meaning depends on
which version of criterion 3 the reader happens to hold is the defect, not the fix: under the
pre-amendment text SC-13a(a2)'s corrected-side requirement and criterion 3 contradict each other,
and under the amended text they do not. **This clause states no gate of its own on this limb**; it
adds SC-13a's threshold to the floor's first limb and SC-13b's admissibility test, and it changes
neither of criterion 3's gates.

**(c6) WHAT THE CRITERION DOES NOT REACH, AND WHAT DOES NOT REACH IT.** It is a kill/pause
criterion over the runtime detectors. **It creates no acceptance criterion, amends none, and is
never cited against one.** The descriptive fixture proof count of §6.2 remains descriptive and
non-gating **for §6.2**; these clauses make proof yield gating **for this criterion only**, which
is what line 1035's first limb already requires, and they promote no other count to a gate
threshold. A fixture evaluated under this criterion is still evaluated under the labelled
hypothetical declaration and **still does not carry full acceptance weight** (§6.2).
**And in the other direction, stated because it is the collision these clauses exist to resolve:**
a declaration statement that assigns a finding's character to a detector row and places it
**outside an acceptance gate** does not place it outside **this** criterion, and does not remove
that detector from the criterion's denominator, from SC-13b's admissibility test, or from
SC-13a(a2)'s gate. **A jurisdictional routing statement written about the acceptance gate reaches
the acceptance gate and stops there.** Removing a detector from this criterion is a waiver, and
the floor forbids it.

**(c7) WHAT THE CRITERION IS FOR, so it is not read as a quality bar.** It fires on an approach
that is **broken**, not on one that is **incomplete**. A detector that probes few cohorts, proves
what it probes, and publishes its coverage honestly **passes this criterion and is supposed to**;
its limitations are reported as numbers, not converted into a stop. **Partial capability honestly
reported is the designed outcome of this programme and is never by itself a kill condition.**
```

**Why.** (c1) is the limb that decides whether this whole set can be signed as drafted, and it turns on a verified registered sentence. PREREG.md line 461 reads: "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`." SC-13a(a2) requires non-zero proof yield on EVERY declared side, including the corrected side; proof yield is "correct PROVEN pairs ÷ all scope-eligible labelled pairs" (§7.2 line 791), so a non-zero corrected-side yield is a runtime finding on `fixture_corrected` — i.e. under line 461 as registered, SC-13a is dischargeable ONLY by failing §6.2 acceptance criterion 3. A registration containing a kill criterion dischargeable only by failing an acceptance criterion is internally broken. (c1) states this as a one-way dependency: SC-13a/b/c are not adoptable unless SC-3 (which supersedes line 461, per K2 §8.2 table (a)) is adopted in the same tag; SC-3 remains adoptable alone. THE DECISION FOR THE AUTHOR: SC-13a/b/c and SC-3 must be signed together, or neither. The other limbs each close a specific escape route: (c3) pins the governed detector set to registered sites the declaration cannot reach — §7.1 line 759 ("| **Runtime, `preserving`** | L2a, L3.1 | **proof yield**; ..."), line 760 (`Runtime, promoted`) and line 1039 ("both of L2a/L3.1's combinations"), all verified — so a declaration cannot shorten the set by enumerating units for one detector and omitting the other. (c4) requires the `promoted` combination to be executed and to publish its own registered yield: proof yield is registered for `preserving` only (line 759 vs line 760's "**evidence yield** and the same family below the first row"), so a criterion stated in proof-yield terms would otherwise drop the other combination — and dropping it waives it, which line 1035 forbids. (c5)(i) names which version of criterion 3 the floor's third limb ("criterion 3's gates in force") carries — the SC-3 form, never the pre-amendment prohibition — because the two versions give the clause opposite meanings; it holds the cell key to be the declaration's to supply and states no key of its own. (c7) bounds the criterion so honest partial coverage is not converted into a kill. (c2) is the exception the fourth hunk points at.

**Class.** C — carried as one amendment with SC-13a; K2 §8.2 table (c), row "§10.2, after line 1035, following SC-13b | SC-13c". Insertion, not supersession, with one relationship stated precisely: (c2) is an express, scoped class C change to how line 816 READS at this one criterion — line 816's text stands byte-exact — recorded in the v30a amendments block (K2 §8.2 table (b), row "§7.2.1 line 816").

### 2.37 — `PREREG.md` 1050 (marker written at line 1054, the end of its block) · SC-8 · marker

**Anchor (verified byte-exact) — the registered line as it stands:**

> 3. **SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed** in the tag message and the README.

**What changes.** Beneath §11's list, after a blank line, two marker blocks are placed: "§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT" and "§11 items 1–7 — v30a, EXTENDED". Items 1-7 all stand byte-exact, item 3 included.  **Placement (R37/D4):** §11's item list runs to item 7 at line 1054; the marker is written beneath the list, after line 1054. Marker placement rule (R37/D4): a supersession marker attaches to a COMPLETE BLOCK — a whole paragraph, a whole table, or a whole list — never inside one. A marker written inside a table breaks the table; inside a list it breaks the list.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
**§11 items 1–7 — v30a, EXTENDED.** Item 8 is added: it indexes the freeze (SC-8) and amends item
3's hash set; SC-8(f) states the requirement generically and does not fix a count.

**§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT.** The registered v30 item
names three files; the `prereg-v30` tag as executed enumerated five. The requirement — SHA-256 as
committed, in the tag message and the README — stands byte-exact; the file set and its count are
item 8's, derived from the tag message's own enumeration, and the three names are retained as the
v30 record and are NOT the set.
```

**Why.** Without the item-3 marker, §11 holds two live answers to which files are hashed — item 3's three names at line 1050 and item 8's enumeration rule three lines below it — inside a single section. That is §0.2.1 line 77's own failure mode ("A rule stated twice has no canonical source") reproduced in the registration's integrity section, which is the worst possible place for it: a future reader deciding what a v30a tag must carry would have a defensible reading in which three files suffice. The marker retires the FILE SET only; item 3's requirement — SHA-256 as committed, in the tag message and the README — stands byte-exact, so nothing is weakened, and the three names are retained as the v30 record. The items 1-7 marker does the indexing job: it records that item 8 exists and what it does, so §11's list is not read as closed at seven. Two things the author should see. FIRST, a defect was fixed in this text during drafting and he is signing the fixed version: SC-8's M2 marker previously read "Item 3's hash set is amended by R23 independently of this clause", and "R23" is a workflow identifier that resolves to nothing inside PREREG.md (SCHEMA_SET_FINAL.md lines 2010-2013). Signing the earlier wording would have put a dangling identifier into the registered text. It now reads "Item 8 is added: it indexes the freeze (SC-8) and amends item 3's hash set". SECOND, the marker deliberately leaves item 3's "and the README" clause standing — whether the README must mirror the tag's full enumeration or may point at the tag is not decided here and remains open.

**Class.** C, carried with SC-8. K2 table (b), two rows: "§11 item 3 (line 1050) — the hashed files | superseded as a file set, not as a requirement | §11 item 8, with SC-8(f) | C, carried with SC-8" and "§11 items 1–7 | extended by item 8 | SC-8 | carried with SC-8".

### 2.38 — `PREREG.md` 1054 · SC-8 · insert

**Anchor (verified byte-exact) — the registered line as it stands:**

> 7. Evaluation generator snapshot, conformance suite, adjudication rubrics, parameter distributions, beacon records, and generated manifests frozen in their own files with their own hashes.

**What changes.** A new eighth item, "8. **The freeze, and the hash set that carries it — v30a.**", is inserted into §11's numbered list immediately after item 7. §11 currently ends at item 7 (verified: line 1054 is followed by a blank line and `---`), so this is a pure addition with no registered sentence replaced.

**Operative text — what this hunk actually puts into `PREREG.md`:**

```markdown
8. **The freeze, and the hash set that carries it — v30a.** What freezes at an amended
registration's tag, in what form, and what may not happen to it afterwards is stated in §6.2
(v30a) [SC-8] and is not restated here. The tag message of this registration and of every
amendment to it carries the SHA-256, as committed, of **every registered document and every
registration tool** — the registration and its checking tools as item 1 names them, every document
an amendment registers under §0.2.1 (the availability declaration included), and every file
SC-8(f) requires hashed — **one hash beside one path, enumerated in the tag message itself.** The
set is that enumeration and its count is read from it: no clause of this file states the count as
a literal, and where an earlier clause names the hashed files or their number — item 3's three
names, §0.2.1 line 97's "both" — it records the set at the time of its writing, stands as that
record, and is superseded as the set by this item; the requirement it states stands. A registered
file absent from the enumeration is a defect in the tag, not a file outside the chain.
```

**Why.** This is the hunk that actually closes the integrity hole SC-8(f) names, and it is the one with a live author decision in it. Three different registered or executed answers to "which files are hashed" are in play right now: §11 item 3 (line 1050) names THREE — "**SHA-256 of `PREREG.md`, `DESIGN.md`, and `HISTORY.md` as committed**"; the executed prereg-v30 tag enumerates FIVE; §0.2.1 line 97 says "both", TWO. v30a makes it four counts by adding the declaration. Item 8 replaces every literal with a rule — the set is the tag message's own enumeration, "one hash beside one path", and "its count is read from it" — so growing the set and stating its size become one edit rather than two. That is H-L13 applied. The substantive stake, not the bookkeeping one: the executed v30 tag hashes the specification and both tools and hashes NOTHING on the declaration side. Under the v30a schema the declaration carries the declared ground-truth map (SC-3(a)) and therefore the scoring key, the per-unit class citations and N (SC-4(a)), and the unscored ledger (SC-6(b)). Without item 8, v30a's integrity chain covers the document being amended but not the object the gate is actually scored against — SC-8(f)'s "an integrity chain with a hole exactly where the amendment lives", which is not rhetoric here but a description of the tag as executed. Item 8 also carries the fail-closed rule that a registered file absent from the enumeration "is a defect in the tag, not a file outside the chain". BEFORE SIGNING, one thing is unresolved and the drafting record says so (SCHEMA_SET_FINAL.md lines 2004-2010): item 8's genus reaches "the registration and its checking tools as item 1 names them", and item 1 names `tests/registration/`, a directory the executed tag did not hash. Either the suite gets hashed file by file, or item 8's text is narrowed — and the narrowing has to be in item 8's text, not left to be read.

**Class.** C, carried with SC-8 (a change to what the amendment's integrity chain must cover). K2 table (c): "§11, after item 7 (line 1054) | item 8 | the freeze indexed from §11, and the hash set read from the tag message's own enumeration | C, carried with SC-8 | the open-form discipline for the hash-count enumeration (`HISTORY.md` H-L13)".

---

## 3. What is deliberately ABSENT

- **SC-14, and any amendment to either criterion 5.** Withdrawn. The 13 August decision was a
  **forecast** that the 15 October condition will not be met, not a firing — a date-gated criterion
  cannot be evaluated before its date. Reading §10.2 criterion 5's "stop" as deferral-of-release
  would have softened a registered consequence, which the declaration's §D.3 forbids resolving
  toward. Verified absent: zero occurrences of `SC-14` in `SCHEMA_SET_FINAL.md` and in
  `K2_AMENDMENT_LEDGER.md`, and no criterion-5 row in any of the block's four tables.
- **Hunk H5**, the earlier drafted criterion-3 replacement. SC-3 carries its structure and
  supersedes it; carrying both would target line 461 twice.
- **A `waived` entry condition anywhere but SC-12(w).** The state is prohibited outright, with a
  closed and empty list of licensed grounds.
- **Any renumbering of the two criteria numbered 5.** Recorded as a registration defect (H-37) for
  a future amendment; renumbering a registered criterion is itself class C and would invalidate
  every citation of both numbers written to date.

---

## 4. Verification record

- **Anchors:** 38 of 38 hunks verified byte-exact against `PREREG.md` by the
  producing pass. An independent anchor critic re-read the distinct pristine line numbers the hunks name with
  `sed -n` and reported no mismatch. Full text in `X5_CRITIQUES.md`.
- **SC-14 absent:** `grep -rn "SC-14"` over `SCHEMA_SET_FINAL.md`, `K2_AMENDMENT_LEDGER.md` and
  `Y3_WAIVED_ENTRY_CONDITION.md` → zero hits. (It survives only in withdrawn scratch drafts, which
  are not sources for this diff.)
- **SC-12(w) present:** limbs (w1)–(w7) and its closing bounds block, staged inside SC-12.
  Bound (6) rewritten to state its §8.3 reach (R37/D1, R39/F1–F6).
- **§7.7 pointer redraft present:** the H8 draft is replaced; the old text asserting that no entry
  condition exists would be false on adoption.
- **§8.3 line 929 hunk present:** `waived` joins the `assert_audit_complete()` failure set.
- **The amendments block enumerates and never counts.** The guarantee is in the block itself:
  *"Their number is read from the enumeration and is stated nowhere as a numeral"*. No numeral
  stating how many amendments there are was found in the block.
- **§2.9 is vacant** in v30, so SC-1's new section number collides with nothing.

---

## 5. Open findings — read before signing

The producing passes raised **57** findings. The grouping below is mine, not theirs;
every finding is reproduced verbatim so you can regroup it.

### 5.A — OPEN (26) — read these before signing

**O-1.** SC-13a(a1) CITATION DEFECT — applied text. (a1) reads "The scoring unit is the **feature-cohort pair** §7.2 registers as its runtime scoring unit". §7.2 (PREREG.md lines 774–800) does NOT register that term: its unit table at lines 780–781 registers **EvidenceEvent** (`(detector, promotion_status, feature, affected output cohort)` within a case) and **ReportedFinding**. The exact phrase "feature-cohort pair" occurs at exactly one place in PREREG.md — line 830, inside §7.4's scope-eligibility definition. §7.2 line 791 does register proof yield's denominator as "all scope-eligible labelled pairs", so the substance is right and (a3)'s denominator citation is exact; but the UNIT limb of a kill criterion attributes the unit's registration to a section that names two other units. Suggested repair, author's call: cite the unit to §7.2 line 791's "scope-eligible labelled pairs" as read with §7.4 line 830, or reword to "the labelled feature-cohort pair §7.2's proof yield is computed over, as §7.4 line 830 names it". Does not affect the line-1030 anchor, which is verified.

**O-2.** SC-13a supersession marker, quotation fidelity — minor, applied text. The Consequential paragraph quotes §10.1 criterion 3 as carrying the branch "on its face (\"**or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**\")". The words are verbatim, but the registered bold span at line 1022 opens earlier: "**under the reconstructed declaration — or, where the fixture is semantically ambiguous (§6.2), under the labelled hypothetical declaration**". The excerpt re-opens bold mid-span. Substance unaffected; flagged only because this text lands in PREREG.md at line 1030's site.

**O-3.** NUMERAL CHECK, within scope — clean. No clause of SC-13a/b/c states a count of amendments, of hunks, or of hashed files. The governed detector set is pinned by citation to registered sites (lines 759, 760, 1039), never by cardinality — SC-13c(c3) and SC-12 pin the same set to the same sites and agree. The one numeral in scope, SC-13a's marker phrase "§6.2's four acceptance criteria are not amended by these clauses", counts REGISTERED criteria, not amendments, and is factually correct: PREREG.md lines 459, 460, 461, 462 are exactly four numbered criteria. It is outside the enumerate-never-count rule.  **SEARCHED:** `PREREG.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-4.** STANDING DEPENDENCY THE AUTHOR SHOULD SEE, not a defect. SC-13b(b3)'s "defined 0/N, not a 0/0" rests entirely on PREREG.md line 830 ("a pair in an `unsupported` or `not_applicable` case remains scope-eligible and remains in §7.2's yield denominators as a miss"), while SC-13c(c2) excepts line 816's suppression clause over the same state. Both lines are verified verbatim. §AB records the 816/830 duplicated-authority conflict as a defect explicitly NOT resolved by this amendment. Consequence: if a future amendment ever resolves 816/830 in line 816's favour, SC-13b(b3)'s disposition of the `not_applicable`-everywhere state collapses back to a suppressed gate. Signing v30a leaves that dependency live and recorded, which is the drafters' stated intent.

**O-5.** CONSISTENCY WITH SC-12(w), checked — no conflict. SC-13a(a2) requires each governed combination "executed to a terminal result on every declared side and reported under its actual §6.6 states — never under §7.7's `waived` coverage state". With SC-12(w1) adopted ("NO DETECTOR-CASE MAY BE REPORTED `waived`. LICENSED GROUNDS: NONE"), (a2)'s prohibition is reinforcement of a general bar rather than a competing entry condition for the state. SC-13c(c2)'s waiver citation — "SC-12's definition, head and limb (iii)" — matches SC-12's text exactly: head "incapable of changing the criterion's outcome", limb (iii) "the criterion can be satisfied by another detector's output alone".

**O-6.** HUNK COUNT FOR SC-8. The brief says SC-8 has two; that counts insertion points. The applied text lands at four distinct sites in PREREG.md — after line 480, after line 97, after line 1054 (item 8), and beneath §11's list (two markers) — which is exactly what K2_AMENDMENT_LEDGER.md enumerates: table (c) rows "§6.2, after line 480" and "§11, after item 7 (line 1054)", and table (b) rows "§0.2.1 line 97", "§11 item 3 (line 1050)" and "§11 items 1–7". Reported here as four hunks.

**O-7.** SC-7 IS NOT SEVERABLE FROM SC-1 AND SC-3 — two forward references that do not resolve against v30. (i) SC-7(a) hands the detector "the availability declaration's **declared elements** (§2.3, §2.4, §2.9)"; §2.9 does not exist in v30 — it is created by SC-1. (ii) SC-7(c) asserts "Under criterion 3 the map **is** the scoring key", which is false of registered criterion 3, PREREG.md line 461: "3. **No runtime finding of any tier, primary or secondary**, appears on `fixture_corrected`." — no map is named. SC-7 adopted alone contains a dangling section reference and a false premise.  **SEARCHED:** `PREREG.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-8.** OPEN AUTHOR DECISION INSIDE §11 ITEM 8, disclosed in the drafting record (SCHEMA_SET_FINAL.md lines 2004–2010) and unresolved. Item 8's genus is "every registered document and every registration tool — the registration and its checking tools as item 1 names them". Item 1 (PREREG.md line 1048) names `tests/registration/`, a DIRECTORY, among those tools, and the executed prereg-v30 tag hashed no part of it. Signing item 8 as drafted either obliges hashing that suite file by file or requires narrowing item 8's own text. The drafting record is explicit that narrowing "must be done in item 8's text, not by leaving the genus to be read" — i.e. this must be settled BEFORE signature, not after.

**O-9.** SECOND OPEN POINT AT THE SAME SITE: the item-3 marker leaves item 3's "and the README" clause standing ("...in the tag message and the README", PREREG.md line 1050). Whether the README must mirror the tag's full enumeration or may point at the tag is not settled by these hunks.

**O-10.** SC-7's NEGATIVE CLAIM — "No registered text states an input surface" — is supported but by search, not by exhaustion. `grep -n "ground-truth map|input surface|receives exactly|one side at a time|blinded|withheld"` over all 1,099 lines returns exactly ONE hit, line 896, and it governs the deferred REVIEW adjudication rubric, not the gate's detector inputs; it in fact concedes "The adjudicator is the author and is not blinded to the tool's involvement". Stated as NOT ESTABLISHED only in the strict sense that no exhaustive read of every line was performed for this negative.

**O-11.** OPERATIVE TEXT NOT QUOTED IN THE AUTHORITATIVE SOURCE. SC-6's insertion point 1 (SCHEMA_SET_FINAL.md line 517) says only 'REPLACE the row to add the state'; the replacement row is nowhere quoted verbatim in SCHEMA_SET_FINAL.md — only the retained v30 row is (line 527). The applied form is recoverable from the scratch applied file (…/scratchpad/applied/PREREG.md line 1072): `| **Detector-case coverage** | `passed`, `failed`, `not_applicable`, `unsupported`, `could_not_run(reason)`, `waived`, `unscored` |`. The final diff must quote that row verbatim; the author should not have to reconstruct operative registered text from a scratch artifact in order to sign it.  **SEARCHED:** `PREREG.md`, `SCHEMA_SET_FINAL.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-12.** CLASSIFICATION NOTE, not an error but worth the author's eye: the SC-6 §8.2 insertion is carried in K2 table (d) as a 'pointer — a cross-reference that adds no rule of its own'. Its final clause does more than point: it re-scopes §8.2's closing sentence in open form, which extends a display prohibition to `waived`, a state §8.2 does not name today. K2 table (b) separately records the §8.2 extension against line 915, so the surface is enumerated — but a reader auditing table (d) alone would not learn that this row changes what the display rule reaches.

**O-13.** SCHEMA_SET_FINAL's OWN CHANGE LEDGER AND CLOSING TALLY ARE STALE ON SC-12(w). Part 5's "Not changed, and examined" paragraph names SC-12 among the clauses "byte-identical to SSA Part 1", and Part 5's table F-1…F-15 has no row for SC-12(w) or for the §8.3 line-929 hunk. The CLOSING TALLY likewise reads "Clauses delivered … **15** — SC-1 … SC-12, SC-13a, SC-13b, SC-13c … **+ 3 INSERTION TEXT blocks** (§8.2, §11 item 8 with two markers, §8.6)", counting neither. Both were written for the R32/S2/S3 pass named in the file's title; SC-12(w) and the §8.3 hunk were added later (SSF lines 994 and 1018-1019 date them to DELTA R35, items B3 and B4). The K2 amendments block IS current — table (a) carries the §8.3 line-929 row, table (c) carries SC-12(w), table (d) carries the redrafted pointer. Reconcile the SSF apparatus or drop the stale claim; do not let "SC-12 is byte-identical to SSA" stand next to a diff that amends two registered surfaces under SC-12(w).  **SEARCHED:** `SCHEMA_SET_FINAL.md` Part 5 (the Not changed, and examined paragraph, the F-1..F-15 table, and the CLOSING TALLY) and `K2_AMENDMENT_LEDGER.md` tables (a), (c), (d) — the artifacts this finding itself names, restated as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts that SSF Part 5 carries no row for SC-12(w) or the §8.3 line-929 hunk, not that either is absent from the corpus — the finding states the opposite, that K2 carries both. The named artifact is authoritative for its own apparatus (H-L15).

**O-14.** K2's WORKING R-SERIES HAS NO ROW FOR §8.3 LINE 929. Searching K2_AMENDMENT_LEDGER.md for "929" returns exactly one hit, line 457, which is inside the K2 block (table (a)). The R01-R36 surface table has no R-row for it, so K2's derived surface counts at lines 184, 214 and 216 were computed without it. The block enumerates correctly; the apparatus counts behind the block do not. This does not breach the enumerate-never-count rule (the block itself closes with "Their number is read from the enumeration and is stated nowhere as a numeral"), but the working counts are wrong.  **SEARCHED:** `K2_AMENDMENT_LEDGER.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-15.** HUNK-LABEL COLLISION ON "SC-12 INSERTION POINT 2". K2 line 141 assigns "H1 hunk **H8** = **SC-12** insertion point 2" to the §7.7 pointer; SCHEMA_SET_FINAL.md line 1018 assigns "SC-12(w) SECOND INSERTION POINT" to the §8.3 line-929 hunk. Two different registered surfaces share the label. SC-12 in fact touches three surfaces — line 1035 (insert), line 929 (replace), line 856 (pointer). Fix the labels before application so the wrong hunk is not applied at the wrong anchor.

**O-16.** SC-10's SUPERSESSION MARKER WOULD PUT A DRAFTING IDENTIFIER AND AN UNMADE DECISION INTO PREREG.md. Marker text is applied text under SCHEMA_SET_FINAL.md §0.2 ("only **THE CLAUSE**, **SUPERSESSION MARKER** text at the superseded site, and … the **INSERTION TEXT** blocks enter `PREREG.md`"). SC-10's marker ends: "The alternative — adding a sixth row — is named in F-5 and is the author's call." F-5 is a K1 finding, not a registered document, and the sentence leaves an open author decision inside registered text. SC-6 received the opposite treatment for the same problem — SSF lines 582-585 keep the F-6 reference "here, in apparatus, and removed from the applied clause text." SSF Part 6 item 2(a) already lists SC-10's "F-5" as an unresolved drafting identifier that "must be resolved to registered citations or struck at the real application". Strike the sentence or resolve the citation before signing.

**O-17.** SC-10 / F-5: THE SOURCES DISAGREE ABOUT WHETHER THE DECISION IS MADE. The K2 block table (b) resolves the §6.1 collision by the marker route ("amended in form: the implication that the enumeration is exhaustive"), i.e. no sixth row. SSF Part 6 item 2(c) still lists "K1's … F-5 (§6.1's closed 'Five bodies' heading vs SC-10)" as open, and SC-10's own INSERTION POINT paragraph still says the clause "collides with it unless the heading or the table is amended." Confirm the marker route is the decision and close F-5, or the diff ships an amendment whose own apparatus says the question is open.

**O-18.** SC-10 INSERTION-POINT DESCRIPTOR IS IMPRECISE (minor, no anchor defect). The clause says the insertion goes "immediately below the five-bodies table". It does not: the table runs lines 433-439, line 440 is blank, and line 441 — the named anchor — is §6.1's closing AUC/proof-count paragraph. The line number and the quoted text both verify, and after line 441 is the correct place (still inside §6.1; §6.2's heading is at line 443). Only the prose descriptor is wrong.

**O-19.** OUT OF SCOPE BUT UNDISCHARGED — the declaration-side edit SC-12(w) requires. Y3 §6.4 records that `AVAILABILITY_DECLARATION.md` §A.12's "Where the definition lives" paragraph enumerates what SC-12 carries — "its head and limbs (i)–(v), the rule that it may not be invoked, and the seven limits" — and is "now short by one limb", requiring the addition of "and SC-12(w), the entry condition for §7.7's coverage state". That edit is not a PREREG.md hunk and appears in no table of the K2 block. It must be tracked somewhere or the declaration will cite SC-12 incompletely at the tag. NOT ESTABLISHED whether any other pass owns it.  **SEARCHED:** `AVAILABILITY_DECLARATION.md`, `PREREG.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-20.** C1 AND C2 WERE FLAGGED FOR THE AUTHOR'S DECISION AND HAVE SINCE BEEN FOLDED IN — signing the ledger makes that decision. PREREG_v30a_DIFF.md headings at lines 401 and 423 both read "CONSEQUENTIAL, AUTHOR ADJUDICATION REQUIRED", and line 411 says they are "flagged rather than folded into the core diff … the author should decide whether v30a reaches outside the walked section". K2 table (a) now carries both as rows ("superseded, consequential to lines 445 and 451"; "superseded, consequential to line 461"). This is not an error, but it is a decision the signature makes silently unless the diff says so.

**O-21.** SC-3 SILENTLY GENERALISES THE NUMBER OF FIXTURE SIDES. H5's drafted text reads "Runtime findings on **both** fixture sides" and "on **either** side"; SC-3's operative text reads "on **every** fixture side" (SCHEMA_SET_FINAL line 270) and "on **any** side" (line 283). This is a widening, not a weakening, and is consistent with SC-2(c)'s pre/post construction, but it is a change to the criterion's scope that no marker or ledger row calls out.

**O-22.** INBOUND REFERENCE TO THE RETIRED CRITERION-3 PREMISE THAT NOBODY HAS DISPOSED OF: PREREG.md line 1035, "The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force." Read in §10.2 the citation most likely means §10.2 criterion 3, but §10.2 criterion 3's consequence (line 1036) is shipping-marked-experimental, not a gate, while §6.2 criterion 3 is a gate criterion — so the reading is genuinely ambiguous. If it means §6.2's criterion 3 it is a further inbound reference to the premise SC-3 retires, of exactly the shape C2 cures at line 1022. K2 table (a) has no row for line 1035; SC-13c(c1) is described as "the one-way dependency on amended criterion 3", so the SC-13 scope may already cover it. Confirm rather than assume. NOT ESTABLISHED from SC-1/2/3's sources alone.  **SEARCHED:** `PREREG.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-23.** THE BLOCK NOW IN K2 §8.2 IS NOT THE BLOCK §8.3's CI RECORD WAS TAKEN AGAINST. K2 §8 line 408–409 claims the §8.2 text is "byte-identical to `_K2_BLOCK_TEXT.md`, the file the verification applier read, and to `_K2_BLOCK_TEXT_as_applied.md`, what it wrote — checked programmatically this pass." That claim is now FALSE. I diffed them: the ledger block is 68 lines, `_K2_BLOCK_TEXT.md` is 67, and they differ in six places — (i) the "What this block is" paragraph (working-resolution identifiers R24/R25 removed, the single-normative-source clause added); (ii) the justification cells of the 855 and 1030 rows in (a); (iii) an ENTIRELY NEW (a) row for `§8.3 line 929 — assert_audit_complete() failure set`; (iv) six (c) justification cells scrubbed of R24/R25/R23; (v) the SC-12 (c) row, which now carries SC-12(w); (vi) the (d) §7.7 pointer descriptor, redrafted per Y3 §6.3. Consequence for the author: §8.3's verification record (`fb171ed8…788bc`, 1,462 lines, delta +0/−0 findings, 136/1 pytest) was measured on the older 67-line block and on a PREREG.md carrying neither SC-12(w) nor the line-929 hunk. The delta is very likely unchanged — the added row is one table row and the checker findings were all on AVAILABILITY_DECLARATION.md — but for the text now proposed it is NOT ESTABLISHED. Re-run the applier and the checker against the final text before signing.

**O-24.** THE LEDGER'S OWN TABLE IS NOW BEHIND ITS OWN BLOCK — the §8.3 line 929 surface is enumerated in the block but has no row in Part A. `SC-12(w)` and `929` occur in K2_AMENDMENT_LEDGER.md at exactly three places, all inside the §8.2 block (lines 457, 488, 493). Part A (§3, 36 rows R01–R36) has no row for §8.3 line 929; §4's derived counts still read "D1 — Registered lines whose text is superseded … R11, R12, R13, R16, R23, R29, R30, R31 — **8 registered lines**" while the block's table (a) now carries nine; §6's both-directions cross-check ("No stated insertion point is missing from the applied file") was run before either the 929 hunk or SC-12(w) existed. This matters more than an ordinary staleness, because the ledger's whole claim is that every count is derived from the enumeration: here the enumeration moved and the derivation did not. Add an R-row for §8.3 line 929 and re-derive §4, or the author is signing a diff whose ledger and whose block disagree by one registered surface.  **SEARCHED:** `K2_AMENDMENT_LEDGER.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

**O-25.** THE BLOCK'S ITEM 1 IS FALSE UNTIL THE TWO RETENTION HUNKS ARE IN THE SAME DIFF. The block states "**No registered sentence is deleted from this file.**" and heads table (a) "each retained verbatim at its site, NOT operative". Of the nine (a) rows, seven retain their v30 text; 992 and 1022 do not, because H1 drafted C1/C2 as bare one-for-one rewrites. K2-F1 records it and K2 §9 supplies the fix. So hunks N3 and N4 are not optional additions to this diff — they are what makes hunk N2's own text true. The author's alternative is to reject C1/C2 entirely, which drops both rows from (a) and strikes the CONSEQUENTIAL notes from the SC-2 and SC-3 markers; nothing else moves, but the Phase 1 gate and the kill gate then keep requirements reading on retired objects.

**O-26.** CARRIED OPEN, FOR THE AUTHOR'S DECISION AT SIGNING — not defects in the hunks above, but each is a live choice the diff embeds. (1) K2-F4: the class of the hash-set items (block rows for line 97, item 3, item 8) is tabled as "C, carried with SC-8" against working resolution R7's earlier class A call; if the author holds R7, three cells change and nothing else moves. (2) K2-F3: two drafting identifiers survive in applied marker text — "F-5" at the SC-10 marker and "(H1 **C2**)" at the SC-3 marker; one-line replacements are drafted in K2 §7 but not applied. (3) K2-O4: SC-13a's marker says line 1022 "is **not** amended by these clauses", true of SC-13a–c but readable as saying 1022 is unamended when C2 does amend it; a clarifying clause is proposed. (4) K2-F5, half-discharged: AVAILABILITY_DECLARATION.md §A.11's "Four amendments" has been fixed to the recommended open form by the live K4 pass, but §D.1 item 5 still reads "**The four §6.2 amendments and the §10.2 definition**, as written" — and that one is the harder half, because a freeze list that enumerates by count silently stops freezing whatever the count omits (it omits the denominator rule and every schema clause). It is outside the PREREG.md diff, but the author signs both documents in one tag. (5) K2-F7: `applied\AVAILABILITY_DECLARATION.md` was being written by another item while the ledger cited it; `applied\PREREG.md` did not move, so nothing in this diff is affected.

### 5.B — FIXED (17) — raised, and closed since

Listed so they are not re-raised, and so the fix is auditable. Each names what closed it.

**F-1.** HUNK COUNT AT LINE 816 — expect ONE, not two. K2_AMENDMENT_LEDGER.md §8.2 lists §7.2.1 line 816 twice: in table (b) (line 469, "an express, scoped exception ... SC-13c(c2)") and in table (d) (line 493, "§7.2.1 after line 816"). Only one physical insertion exists there — the §13c-P pointer paragraph. SC-13c's SUPERSESSION MARKER says "None — insertion, not supersession" and §13c-P says "SUPERSEDED TEXT: none". The (b) row records the change of reading; the (d) row records the paragraph that carries it. This mirrors SC-6's treatment of line 915, so it is the ledger's convention rather than a defect — but the final diff must show one hunk at 816, and a reader auditing (b)+(d) row-by-row against the diff will otherwise come up one hunk short.

  → **FIXED BY:** R37/D3 — the duplicate 816 pointer hunk was removed

**F-2.** STALE-SCRATCH INSTRUCTION IN THE DRAFTING (not in the clause text). SCHEMA_SET_FINAL.md line 1972: "THEN, BENEATH THE LIST (blank line, then the two markers; SC-8's M2 marker — already placed there by the CI run — is revised to the second text)". That is true only of the scratch applied copy. Against PREREG.md there is nothing at that site to revise; the hunk must PLACE both §11 markers fresh. The final diff must not carry "revised in place" as an application instruction.

  → **FIXED BY:** R39/F4 — stale H8 pointer references redrafted

**F-3.** STALE APPARATUS beside SC-6, decision-relevant. SCHEMA_SET_FINAL.md lines 582-585 (the K1 finding F-6 note kept as SC-6's drafting record) reads: "K1's finding F-6 — that `unscored` would otherwise have repeated `waived`'s missing-entry-condition defect, and that §7.7's `waived` still has none after this amendment — stands as the drafting record for limb (b)". The clause 'still has none after this amendment' is FALSE once SC-12(w) is adopted. It is apparatus, not applied text, so it does not enter PREREG.md — but it is the note the author reads beside SC-6(b) while deciding, and it contradicts an adopted clause in the same set. Recommend correcting it to point at SC-12(w), or striking the trailing clause.

  → **FIXED BY:** R37/D8 — the F-6 apparatus note now records the second half as spent

**F-4.** STALE RATIONALE inside the SC-6 §8.2 hunk's own drafting record. SCHEMA_SET_FINAL.md line 1931 justifies the disclosed `waived` side effect as "vacuous in practice under H8" (H8 = no case may be reported `waived` until an entry condition is registered). SC-12(w) registers that entry condition in the same tag, so the side effect is live. The paragraph's stated purpose is that the consequence be 'a decision, not a discovery'; on the stale ground the author would be deciding on a false premise. This is carried into the hunk justification above.

  → **FIXED BY:** R37/D8 — the vacuous-under-H8 rationale superseded

**F-5.** SAME STALE CLAIM in T4_WAIVED_SIDE_EFFECT_CHECK.md lines 53 and 96 — "`waived` remains without a registered entry condition after S2(i) lands", "[its resolution] is **not part of the v30a schema set**", "F-6 remains open". T4 is a prior check document, not operative text, but it is a signed-off check whose conclusion is superseded by SC-12(w). Flag so it is not cited as current.

  → **FIXED BY:** R37/D8 — T4 carries a superseded-in-part banner

**F-6.** ASYMMETRY THE AUTHOR SHOULD RULE ON — §8.3 line 929. The set amends line 929 to add `waived` to assert_audit_complete()'s failure set (SC-12's second hunk, K2 table (a)), but no hunk adds `unscored`. Line 929 as registered: "- **`assert_audit_complete()`** — fails on any `unsupported` or `could_not_run` **detector-case** entry, including a mode whose exact comparison was unavailable (§6.10). Ignores findings." Consequence as drafted: an `unscored` detector-case entry does not fail the completeness assertion, so a run may pass assert_audit_complete() with unscored coverage. That may well be intended — SC-6(a) says the detector 'may have executed perfectly' — but it sits against SC-6(e)'s absolute pass prohibition and against the parallel treatment of `waived`. Whether this was considered and decided is NOT ESTABLISHED: no text in SCHEMA_SET_FINAL.md's SC-6 section, K2's block, or Y3 addresses `unscored` at line 929. It should be a recorded decision in the diff, not a silent omission.  **SEARCHED:** `SCHEMA_SET_FINAL.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

  → **FIXED BY:** R37/D6 — SC-12(w) bound (6) argues the unscored/waived asymmetry in-clause

**F-7.** PLACEMENT NUANCE worth stating in the diff so the reader is not looking for an edit that is not there: SC-4's marker names §6.2 lines 459 and 446, but the marker paragraph is physically placed at the SC-4 insertion site (after line 464), not at line 459. Confirmed in the scratch applied file (…/scratchpad/applied/PREREG.md line 604, sitting directly after applied line 602 = v30 line 464). Both named lines were read and stand byte-exact; nothing is edited at either.

  → **FIXED BY:** R37/D4 — marker placement is now stated per hunk

**F-8.** SC-12(w) — THE BOUNDS BLOCK IS MISSING FROM THE APPLIED TEXT. AUTHOR DECISION REQUIRED. Y3_WAIVED_ENTRY_CONDITION.md line 39 closes the (w) limb with "**What this limb does NOT permit** — the bound stated in the next block, which is part of this clause and is applied with it", and §2 (lines 45-61) supplies eight bounds. SCHEMA_SET_FINAL.md's applied (w) text runs lines 998-1016 and STOPS AT (w7); the bounds block is nowhere in the file (grep for "does NOT permit" over SCHEMA_SET_FINAL.md returns exactly one hit, line 976, which is SC-12's own seven-item list, a different list). If the SSF text is signed as-is, these do NOT get registered: bound (1)'s anti-silence rule (a criterion's failure to name a detector licenses nothing), bound (2)'s requirement that any future ground be added only by class C amendment committed and timestamped before the affected detector is implemented or evaluated and never after a fixture result is observed, and bounds (3)-(5), (7), (8). Y3 §5's non-weakening argument leans on bounds (1), (2), (3), (4), (5) and (8) by name, and Y3 §4.3 identifies the anti-silence rule as one of the two strongest devices carried over. Decide expressly: adopt the bounds block with the limb, or accept the narrower registration and correct Y3 §5 so the record does not claim protection that was not registered.  **SEARCHED:** `SCHEMA_SET_FINAL.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

  → **FIXED BY:** R37/D1 — the bounds block is in SCHEMA_SET_FINAL.md's SC-12(w); grep 'What this limb does NOT permit' returns it

**F-9.** SC-12(w) BOUND (6) IS FALSIFIED BY THE LINE-929 HUNK, AND Y3 §7 ITEM 1 IS STALE. Y3 §2 bound (6) reads "It amends no other coverage state's entry condition, moves no boundary in §8.2, and alters no assertion in §8.3." The second SC-12(w) hunk alters §8.3's assertion at line 929. Y3 §7 residual risk 1 is stale for the same reason: it states "this limb deliberately does not amend §8.3" and "a non-conforming report that emits a `waived` entry passes all three assertions", both untrue in v30a. If bound (6) is adopted (finding 1) it must be redrafted before signature; either way Y3 §7 item 1 no longer describes what is being signed.

  → **FIXED BY:** R37/D1 — bound (6) rewritten to state the §8.3 reach explicitly

**F-10.** TWO NON-IDENTICAL VERSIONS OF THE (w) LIMB EXIST; ONLY SCHEMA_SET_FINAL's IS CORRECT. Y3 §1's head paragraph reads "`assert_audit_complete()` fails on `unsupported` and `could_not_run` and on neither of the others (§8.3). A `waived` entry is invisible to every published number and to every assertion" — which becomes FALSE the moment the line-929 hunk lands. SCHEMA_SET_FINAL.md line 1000 has the corrected form, "`assert_audit_complete()` reads it alone", which is supported by PREREG.md line 820 ("**No runtime metric reads the detector-case state of §7.7**, which exists for `assert_audit_complete()` alone") and survives the amendment. (w2), (w3), (w4), (w5) and (w7) also differ in wording between the two files (SSF drops, e.g., (w2)'s "and where a required strategy fails" and its closing "has not recorded a cause" sentence, and (w4)'s granularity sentence). State in the diff that SCHEMA_SET_FINAL.md Part 1 is the operative clause text and Y3 §1 is the drafting record, or the wrong version can be applied.

  → **FIXED BY:** R37/D1 — Y3 §1-2 replaced by a pointer; the applied text lives only in SCHEMA_SET_FINAL.md

**F-11.** K2 WORKING ROW R25 STILL CARRIES THE FALSE POINTER DESCRIPTOR. K2_AMENDMENT_LEDGER.md line 141 describes the §7.7 pointer as "POINTER — \"`waived` is defined in §10.2 (v30a)\", with the residual-gap statement (no entry condition for the coverage state is defined by this registration)". That statement is false on adoption of SC-12(w). The K2 *block* (table (d), inside the K2-BLOCK markers) is already redrafted correctly, so the applied ledger text is fine — but R25 is the row that names the pointer's applied text, and the redraft exists only in Y3 §6.3. Update R25 alongside the pointer so the apparatus and the applied text do not disagree.

  → **FIXED BY:** R37/D8 — the residual-gap descriptor is superseded

**F-12.** APPLICATION-ORDER HAZARD, SC-2 vs H4 — the final diff must state the resolution or the applier halts. SC-2's insertion point is "After `PREREG.md` line 451" (SCHEMA_SET_FINAL line 185), and H1 hunk H4 REPLACES that same line 451 with a four-line block (PREREG_v30a_DIFF.md lines 198–213). Applied in ascending anchor order, once H4 lands the full line `- **Sliced variant** for CI, from the same padded slicer as user-facing slice auditing.` no longer exists as a line — it survives only inside H4's nested `> **SUPERSEDED BY v30a …**` quote line — so under H1's full-line convention ("refuse on zero or multiple matches", SCHEMA_SET_FINAL line 84) SC-2's anchor re-derivation returns zero matches and the applier refuses. The diff must say explicitly that SC-2's block lands after H4's four-line block, i.e. after the retained-verbatim quote, not between H4's operative bullet and its marker.

  → **FIXED BY:** R37/D3 — H4 kept as the sole operation on line 451; SC-2's order stated in H4's entry

**F-13.** DOUBLE-APPLICATION RISK, SC-3 vs H5 — H5 must be absent from the final diff. SCHEMA_SET_FINAL lines 251–254: SC-3 "**REPLACES `PREREG.md` line 461** (criterion 3), carrying H1 hunk **H5**'s structure. The generic cell-key formulation below **supersedes H5's** on one axis". K2 ledger table (a) maps §6.2 line 461 to SC-3, not to H5. If the assembled diff carries both H5 (PREREG_v30a_DIFF.md lines 219–245) and SC-3, line 461 is targeted twice and PREREG.md would hold two operative versions of criterion 3.

  → **FIXED BY:** R37/D3 — H5 absent by design; SC-3 replaces line 461

**F-14.** FIVE HUNKS THE AUTHOR SIGNS BUT WHOSE OPERATIVE TEXT IS NOWHERE IN SCHEMA_SET_FINAL.md. K2 table (a) registers §6.2 line 445, §6.2 line 450, §6.2 line 451, §10 line 992 and §10.1 line 1022 as amendments of v30a, each with "operative clause/item/row at its site". SCHEMA_SET_FINAL cites them (SC-2's marker block, lines 190–198; SC-3's marker block, lines 264–266) and expressly does not re-draft them: "Their markers stand as H1 wrote them and are cited, not re-drafted." Their only drafted text is in PREREG_v30a_DIFF.md (H2 lines 145–150, H3 lines 183–188, H4 lines 208–213, C1 lines 415–417, C2 lines 437–439). The final diff must reprint all five, or the author signs five registered surfaces whose replacement text is not in front of him.  **SEARCHED:** `SCHEMA_SET_FINAL.md` — the artifact(s) this finding itself names, restated here as the declared search population (R48/Q8 formalisation; no new search was run). This is a SCOPED absence claim: it asserts absence from the named artifact(s), not from the corpus. Any disposition that would DELETE a registered surface requires the artifact named to be authoritative for the question — H-L15.

  → **FIXED BY:** R37/D2 sourced them from PREREG_v30a_DIFF.md; R39/F3 gave every hunk an operative_text field

**F-15.** MARKER PLACEMENT UNDEFINED, SC-1 at §2.3 line 205 — the named site is inside a table. Line 205 is a row of the `AvailabilityModel` table spanning lines 201–212 (verified by reading 196–216). A blockquote marker inserted after line 205 splits the table and breaks its rendering. SC-1's marker text says only "§2.3 line 205 (`column_roles`)" and never states where the marker is written. The diff must fix the landing point — after the table (line 212), before line 214's "The last three exist because…" — and say so.

  → **FIXED BY:** R37/D4 — complete-block rule; markers written at 212, 462, 1054; enforced by self-check (iii)

**F-16.** MARKER PLACEMENT UNDEFINED, SC-1 at §2.4 lines 220–222 — the named span straddles a formula and a bullet list. Line 220 is the blockquoted formula, 221 is blank, and 222 is the first of four bullets running 222–225 (verified). Inserting the marker after line 222 splits the bullet list; inserting it between 220 and 222 separates the formula from the terms it registers. The diff must name the landing point (after line 225 is the only placement that leaves both structures intact) rather than leaving "lines 220–222" to the applier.

  → **FIXED BY:** R37/D4 — complete-block rule; markers written at 212, 462, 1054; enforced by self-check (iii)

**F-17.** SC-1's CLAUSE TEXT STATES A LITERAL COUNT OF ITS OWN ENUMERATION — "Six requirements follow, and a declaration that does not meet them fixes nothing" (SCHEMA_SET_FINAL line 131). The count is correct today: limbs (a)–(f) are six. But it is the exact shape this amendment is elsewhere removing — §0.2.1 line 97's "both file hashes in the tag message" is being superseded AS A COUNT by §11 item 8, SC-8(f) requires the hash count "derived from the set of registered files, never stated as a literal", and HISTORY.md H-L13 (line 219) records the general lesson: "enumerated ranges in cross-references are fragile by construction, because the obligation to re-bump lives outside the edit that grows the target." Not blocking — SC-1's limbs are closed and adding one would itself be class C editing this clause — but a one-word fix ("The requirements below follow") makes the amendment consistent with the discipline it imposes on §11.

  → **FIXED BY:** R37/D5 — now 'The requirements below follow'

### 5.C — WITHDRAWN (14) — not defects

Records of passing checks, or mechanical matters now owned by the assembler's self-check.

**W-1.** SC-14 IS ABSENT FROM THE OPERATIVE TEXT — confirmed. `grep -n SC-14` over SCHEMA_SET_FINAL.md and K2_AMENDMENT_LEDGER.md returns nothing. STALE SC-14 MATERIAL REMAINS in the same scratch directory and must not be pulled into the diff: T1_CRITERION_5_AMENDMENT.md (the whole file is the withdrawn SC-1

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-2.** ANCHORS: all six anchors in scope verified verbatim against the target. PREREG.md is byte-identical to prereg-v30 (`git diff --stat prereg-v30 -- PREREG.md` empty; sha256 f0a8f00164c217a40f87a4dc9fee6193ee7e4e125c68e3ecc84863fd6e2c7cc6 = the hash in the tag message), 1,099 lines. `grep -c v30a PRERE

  → **WITHDRAWN:** mechanical; owned by self-check (iii) and the D9 round-trip

**W-3.** MARKER CLAIMS VERIFIED AGAINST THE EXECUTED TAG. `git tag -n30 prereg-v30` enumerates FIVE hashes (PREREG.md, DESIGN.md, HISTORY.md, tools/check_registration.py, protocol/runtime_reference.py). §11 item 3 (line 1050) names THREE. §0.2.1 line 97 says "both" (TWO). The SC-8 marker text's claim — "The 

  → **WITHDRAWN:** a record of a passing check

**W-4.** NO COUNTING NUMERAL introduced by anything in this scope. SC-8(f) requires the hash count "derived from the set of registered files, never stated as a literal"; §11 item 8 says "The set is that enumeration and its count is read from it: no clause of this file states the count as a literal". K2's §8.

  → **WITHDRAWN:** a record of a passing check

**W-5.** NO SC-14 ANYWHERE. `grep -n "SC-14"` over SCHEMA_SET_FINAL.md and K2_AMENDMENT_LEDGER.md returns zero hits in both. Nothing stale to remove in this scope.

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-6.** PURE-ADDITION CLAIMS VERIFIED. (i) §11 today ends at item 7 (line 1054), followed by a blank line and `---` — there is no item 8, so item 8 is a pure addition with no registered sentence replaced. (ii) SC-9's site: line 99 is the class-C-after-the-fact paragraph and line 101 is "**Membership in A or

  → **WITHDRAWN:** a record of a passing check

**W-7.** SC-14 CONFIRMED ABSENT from my scope. `grep -rn "SC-14"` over SCHEMA_SET_FINAL.md, K2_AMENDMENT_LEDGER.md and Y3_WAIVED_ENTRY_CONDITION.md returns no matches. No SC-4/SC-5/SC-6 hunk references it.

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-8.** ALL SEVEN ANCHORS VERIFIED BYTE-EXACT against PREREG.md (lines 446, 459, 464, 466, 855, 856, 915). No anchor mismatch found in this scope.

  → **WITHDRAWN:** mechanical; owned by self-check (iii) and the D9 round-trip

**W-9.** SC-14: CONFIRMED ABSENT. Searched all three amendment sources — SCHEMA_SET_FINAL.md, K2_AMENDMENT_LEDGER.md, Y3_WAIVED_ENTRY_CONDITION.md — for "SC-14": zero hits. No stale reference to it survives, and nothing in this scope amends either criterion 5.

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-10.** ALL SEVEN ANCHORS IN THIS SCOPE VERIFY VERBATIM against the live 1,099-line PREREG.md, and each sits in the section its clause names: 431 and 441 in §6.1 (heading at 431, §6.2 at 443); 856 in §7.7 (heading 849, last table row 856); 892 in §7.8 (heading 883, §7.9 at 894 — so 892 is genuinely the clos

  → **WITHDRAWN:** mechanical; owned by self-check (iii) and the D9 round-trip

**W-11.** CHECKS THAT PASSED, recorded so they are not re-run: (1) SC-14 is absent — zero occurrences of the string "SC-14" in SCHEMA_SET_FINAL.md and in K2_AMENDMENT_LEDGER.md, and neither §10.1 criterion 5 (PREREG.md line 1024) nor any criterion 5 appears as a row in K2 tables (a)–(d). (2) The K2 amendments

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-12.** THE BLOCK'S CENTRAL PROPERTY HOLDS — VERIFIED, NOT ASSERTED. The v30a amendments block enumerates and never counts. The sentence that makes it explicit is at K2_AMENDMENT_LEDGER.md line 495, inside the block: "The registered lines this amendment supersedes are those in (a) and no others; the registe

  → **WITHDRAWN:** a record of a passing check

**W-13.** SC-14 IS STALE BUT STILL PRESENT IN FOUR SCRATCH FILES. The two operative sources are clean — `SC-14` appears nowhere in SCHEMA_SET_FINAL.md and nowhere in K2_AMENDMENT_LEDGER.md. It survives in: T1_CRITERION_5_AMENDMENT.md (the entire file is the withdrawn clause); T2_DEVIATIONS_D002_TIMING.md (fou

  → **WITHDRAWN:** not a defect — SC-14's absence is the intended state; recorded in the artifact's §3

**W-14.** ANCHOR VERIFICATION SUMMARY — all eight anchors in scope exist and say what the clauses claim. Verified with `sed -n 'Np'` against C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/PREREG.md (1,099 lines, read-only, unmodified): line 6 (Status), line 8 (Registration), line 816 (the not_applicab

  → **WITHDRAWN:** mechanical; owned by self-check (iii) and the D9 round-trip

---

## 6. My own errors in this set, named

Listed because the diff is what gets signed, and an error I found and fixed is still an error
I made. All three are now closed; each names what closed it.

- **SC-12(w) was staged without its bounds block.** I carried limbs (w1)–(w7) into
  `SCHEMA_SET_FINAL.md` and dropped the closing "What this limb does NOT permit" block that the
  Y3 deliverable states is part of the clause. *Closed at R37/D1.*
- **Y3's bound (6) was left false.** It read that the limb "alters no assertion in §8.3", which
  the line-929 hunk contradicts. Two non-identical copies of the limb existed. *Closed at R37/D1:
  the applied text is single-sourced and bound (6) states its §8.3 reach.*
- **The first assembly truncated** and would have presented §3–§5 as though the hunks had been
  reviewed. Caught by a critic, not by me. *Closed at R37/D9 and R39/F6: the artifact is rendered
  mechanically, and the assembler now self-checks six properties before any reviewer sees it.*

- **I classified the 992 and 1022 ledger rows as COVERED when they were not.** A retention block
  is not a replacement; both sites would have carried a blockquote quoting text still live above
  it. *Closed at R39/F2: both REPLACE operations drafted.*
- **I reported a scan of every clause as complete when it was not.** It missed five in-clause
  numerals, two of them genuinely fragile. *Closed at R39/F5, and the false claim about the scan
  was corrected in `SCHEMA_SET_FINAL.md` itself.*
