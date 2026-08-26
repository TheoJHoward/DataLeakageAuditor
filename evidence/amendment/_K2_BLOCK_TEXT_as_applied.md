## v30a amendments (class C under §0.2.1)

**What this block is.** `prereg-v30a` is an **amended registration, not a restart** (§0.2.1, line 95). It carries the class C changes enumerated below — every registered surface this amendment touches, by section and v30 line, with the clause responsible — and no others. Two passes produced them, and each row names its source. The first is the element-by-element conformance walk of the acceptance fixture's reconstructed availability declaration against §6.2 (`AVAILABILITY_DECLARATION.md` §A), which superseded registered text at instance-bearing lines. The second is the schema pass over that walk's findings (working resolutions R24 and R25), which registered in this file the kind of object each gate input is, what a declaration must supply for it, and what the gate does with it. The declaration is the reconstructed declaration §6.2 already requires and the carrier of this fixture's evidence. **It is not a normative annex and may not be cited as one.** Measurement semantics live in this file and only in this file (§0.2.1's single-normative-source rule). What lives there is this fixture's *instances*: its identity, its measured ground-truth map, its reference-anchor values, its evidence, its documented-unverifiable assumptions, and the per-unit enumerations these rules yield for it.

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
| §7.7 line 855 — detector-case coverage row | superseded: the row is re-registered with `unscored` | SC-6 | C — line 93's "coverage state" | schema pass (R24) |
| §10.2 line 1030 — kill/pause criterion 2 | superseded on the ambiguity branch only; operative where the branch has not fired | SC-13a, with SC-13b and SC-13c | C | line 1033's obligation; working resolution R22 |
| §10 line 992 — Phase 1 gate cell | superseded, consequential to lines 445 and 451 | operative row at its site | C (consequential) | derived from §A.1 and §A.4; not walk-cited |
| §10.1 line 1022 — kill-gate criterion 3 | superseded, consequential to line 461 | operative item at its site | C (consequential) | derived from §A.8; not walk-cited |

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
| §0.2.1, after line 99 | SC-9 | integrity of a declared instance: what a declaration may not create, evidence never adjusted, obligations discharged only by being met or amended, working-resolution authority and supersession order, the stronger-reading interpretation rule, one normative copy | C | working resolution R25 |
| §2, after line 266 (new §2.9) | SC-1 | the declaration as the gate's semantic authority: measured not intended, the representation named, roles are positions, units declared, staleness is not unavailability, one comparator branch scored | C | schema pass (R24) |
| §6.1, after line 441 | SC-10 | declared non-gated data, diagnostic classes, and the forbidden uses of non-gate data | C | schema pass (R24) |
| §6.2, after line 451 | SC-2 | the acceptance fixture's composition, what may move, the pre/post licence, reference anchors by recomputation, moves between phases | C | schema pass (R24) |
| §6.2, after line 464 | SC-4 | the criterion-1 denominator and the three-class partition rule: registered predicates, precedence, edge readings, exclusion grounds, publication discipline | C | declaration §A.6, §A.6.0–§A.6.4, §A.10; working resolution R11 |
| §6.2, after line 464, following SC-4 | SC-5 | adjudication routing: one criterion per finding, attribution to the ground, the false-positive class, detector jurisdiction, declared sentinels | C | schema pass (R24) |
| §6.2, after line 468 | SC-7 | the gate's input surface and the one-side-at-a-time sequencing rule | C | schema pass (R24) |
| §6.2, after line 480 | SC-8 | the freeze: what freezes, in what form, checkable before any run, no number corrected in place, the integrity chain | C | schema pass (R24) |
| §7.7, after the table (line 856) | SC-6 | `unscored`: a coverage state with its semantics, entry condition, two levels, and gate consequences | C | schema pass (R24) |
| §7.8, after line 892 | SC-11 | the all-zero control over every empty aggregate and every pass claim | C | schema pass (R24) |
| §10.2, after line 1035 | SC-12 | "waived", defined; which detectors the floor governs; what the definition does not permit | C | declaration §A.12 |
| §10.2, after line 1035, following SC-12 | SC-13b | admissibility for the ambiguity-branch criterion, and the disposition of every degenerate state | C | one amendment with SC-13a |
| §10.2, after line 1035, following SC-13b | SC-13c | that criterion's interactions: the one-way dependency on amended criterion 3, the line-816 exception, the pinned governed set, the floor limbs carried by citation | C | one amendment with SC-13a |
| §11, after item 7 (line 1054) | item 8 | the freeze indexed from §11, and the hash set read from the tag message's own enumeration | C, carried with SC-8 | working resolution R23 |

**(d) Pointers — cross-references that add no rule of their own:** §7.2.1 after line 816 (to the exception SC-13c(c2) states); §7.7 after the table (`waived` is defined in §10.2; no entry condition for the coverage state is defined by this registration); §8.2 after line 915 (`unscored` under this section's closing sentence, by reference to §7.7's row); §8.6 after line 961 (a zero, an empty result, or an all-clean statement is a published number; SC-11 governs what it must survive and name).

**What this enumeration is, and what is read from it.** The registered lines this amendment supersedes are those in (a) and no others; the registered lines whose reading it extends are those in (b) and no others; the clauses it inserts are those in (c) and no others; the pointers are those in (d) and no others. **Their number is read from the enumeration and is stated nowhere as a numeral** — so that a further clause added under §0.2.1 adds a row here and changes no count anywhere in this file. Every change enumerated in (a), (b) and (c) is class C under §0.2.1 line 93 — each changes what a published number means, what an acceptance or kill criterion requires, or what the gate may consume, or is carried with the clause that does — and each is carried by this registration under line 95. None is a `DEVIATIONS.md` entry standing alone.

**What an amendment may not do, restated here because this is the first one.** It may not be weaker than the thing it amends (line 97). It may not convert an unmet element into a satisfied one by re-reading it. Where an element cannot be met as written at the instant the amendment must be committed, it is **amended explicitly, never waived and never left outstanding** — which is what the sliced-variant row of (a) does.
