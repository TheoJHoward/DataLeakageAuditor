# STAGED — `HISTORY.md` review-lesson lines #3 and #4 (citation applied-holding; multi-question clause)

**Item Q5. STAGING ONLY.** Nothing in this file has been applied.
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` was **read only** and is
unmodified by this pass (`git diff --stat HISTORY.md` is empty; the file is at HEAD `80401d0`,
313 lines). `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` were read only. No git command
that changes state was run. The only file written this pass is this one.

Date recorded: **17 Aug 2026** (the convention H-L12 fixed in its own text, l.218: "Dated by the
day recorded, not the day worked").

---

## 0. READ FIRST — the ID numbers are free against the file but two other candidates are queued for them

The brief says "Draft H-L14 and H-L15 (verify the next free numbers against the file)".

**Verified against the file:** the review-lesson list at l.207–219 ends at item `13.` (l.219). No
`14.` exists in `HISTORY.md` at HEAD or in the working tree. **The next free IDs against the file
are 14 and 15**, and the two lines below carry those numbers.

**But two other lesson candidates already claim those numbers, in the staged/flagged record:**

| Candidate | Where | Status | Number it claims |
|---|---|---|---|
| The all-zero-control lesson | `…\scratchpad\errata\HISTORY_lesson_line_S4_STAGED.md` §3 (and its repo copy `evidence/errata/HISTORY_lesson_line_S4_STAGED.md`) | **staged, not landed** — an author decision (`evidence/ceremony/COMMIT_PLAN.md` l.206: "Whether H-L14 lands is an author decision") | **14** |
| The R19 recovery lesson (§A.6.0 restage overwrite) | `evidence/ceremony/H34_DRAFT.md` §4, l.200–202 | **flagged, not drafted** — "takes ID H-L15 if the S4-staged H-L14 lands first, H-L14 if it does not" | **15** (or 14) |

**Consequence — the numbers on the two lines below are provisional and are assigned at landing, in
landing order.** Numbering is an ID, not a position (convention 7, §2 below), and the only H-L range
cross-reference in the repository is open-range (§5), so a shift costs nothing outside this file:

| Author's decision on the queued candidates | This item's lesson (a) lands as | This item's lesson (b) lands as |
|---|---|---|
| Neither the S4 line nor R19 lands | **H-L14** | **H-L15** |
| S4 line lands, R19 does not | H-L15 | H-L16 |
| Both land (S4 first, R19 second) | H-L16 | H-L17 |

Whichever numbers they take, **(a) and (b) land adjacent and in that order** — (b)'s text refers to
"the preceding lesson", so the pair must not be separated. If the operator prefers a numeric
cross-reference inside (b), it must be filled with (a)'s *landed* ID, not with 14 (see §3.2 note).

**A related discrepancy the ceremony record should carry.** Commit `80401d0`'s message says
"H-L13 records that an aggregate reporting zero must be machine-cross-checked against its source and
raise on mismatch." The file's H-L13 (l.219) is the *enumerated-range* lesson; the all-zero lesson
is the S4-staged line and **has not landed**. That is a change log written from intent rather than
from the file (H-L11's genus). Nothing here fixes it — the commit is history and must not be
rewritten — but the author should not conclude from the message that the all-zero lesson is in the
record.

---

## 1. Register determination — both are review lessons; neither is a firing, a ledger note, or a version bullet

The four-register table from the H-L12 staging file applies unchanged. Restated for the two entries:

| Register | Fits (a)? | Fits (b)? |
|---|---|---|
| Ledger notes `H-01`…`H-34` (`## Ledger notes, by ID`, l.11 onward) — errata against a **specific locked clause** | **No.** No registered clause is defective. Two of the three instances are in *unadopted amendment drafts* (SC-13 ledger; SC-13b(b3)); the third was in an H-34 draft corrected before it entered the record (`80401d0`, correction 3). | **No.** SC-13 is draft amendment text; nothing in `PREREG.md` is faulted. |
| Version ledger (`- **vNN**`, l.181) — what a numbered version got wrong | **No.** No version is implicated. | **No.** v30a is not yet tagged, and no version is retracted. |
| **Review lessons** (`## Review lessons (from \`DESIGN.md\` §9)`, l.203; list l.207–219) — dated, generalizable process/method lessons | **YES.** Directly parallel to H-L1 (a claim about a source that a search falsified) and H-L11 (an artefact that says one thing while the file says another). | **YES.** Directly parallel to H-L9 (patch at the coupling, not the failure point) — see §3.2 for how (b) differs from H-L9 rather than repeating it. |
| Firings (`## H-B`, `### H-B addendum`, l.295) — stopping-rule firings under `PREREG.md` §0.2 | **No.** §0.2 did not fire. | **No.** The three SC-13 reviews were verifications of a *draft*, not §0.2 firings against a registered version. |

**Register verdict: two review lessons.** State it in the ceremony note. The firing count stays at
**twenty-one** and the H-B addendum entry count at **twenty-three** (l.313 and l.297). With H-L12
and H-L13 already landed, plus the S4 line and R19 if adopted, the ceremony carries **up to six**
lesson additions that must not be miscounted as firings.

**Normative-vs-history split.** `HISTORY.md` l.3: "**Not a normative file.** Nothing here instructs
an implementer." Both bolded sentences below are therefore diagnoses, not instructions, and each
closing clause states a practice as a fact in force. The *binding* form of (b)'s principle already
exists in `PREREG.md` §0.2.1 l.79 (quoted in §3.2); the line cites it and does not restate it.

---

## 2. Format exemplars, quoted verbatim with line numbers

From `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` at HEAD `80401d0`.

**Section header and list preamble — l.203, l.205:**

```
203:## Review lessons (from `DESIGN.md` §9)
205:**Review lessons, dated.**
```

**Exemplar A — l.207 (H-L1), the shortest form and the closest *semantic* match for (a) — a claim about a source, falsified by looking:**

```
207:1. *(28 Jul 2026)* v3 claimed no existing tool probed at runtime. The claim survived several review rounds and was false; `leak-detect` had been on PyPI for six years. **Models are poor at telling you something already exists.** Prior-art verification is a search task, done by the author, written down.
```

**Exemplar B — l.214 (H-L9), the closest *semantic* match for (b) — a structural diagnosis with an audited count, an incident-family form, and a rule that names why an ensemble misses the class:**

```
214:9. *(31 Jul 2026, audited 1 Aug)* Six of eleven firings descended from one clause coupling the fixture gate to a reporting tier. Each round patched the failure point and each patch added a decision point — a trigger, a matrix, a state, a routing rule — which is where the next round's defect lived. Removing the coupling deleted all of them at once, and the version that did it is shorter than the version before it. The count was first published as "eight of ten" and audited down to six, two of them partial — a claim about the ledger's own history is still a claim. **Patch at the coupling, not at the failure point.** Reviewers examine the text where a defect surfaced, which is downstream of its cause, so this is the class of finding an ensemble is structurally poor at producing.
```

**Exemplar C — l.215 (H-L11), the "artefact says X, file says Y" form with a remediation clause:**

```
215:11. *(1 Aug 2026)* Three of v20's announced fixes were never in the file. They were applied as silent string substitutions that did not match, and spot-checking a few of them passed. **An edit that reports nothing when it fails is indistinguishable from an edit that worked**, and a change log written from intent rather than from the file will confidently describe fixes that do not exist. Every edit now asserts its match count, and the change log is written from a diff of the file.
```

**Exemplar D — l.219 (H-L13), the current last line of the list and the insertion anchor:**

```
219:13. *(12 Aug 2026)* A cross-reference in `DESIGN.md` §9 named the review-lesson list as `H-L1 through H-L11`. Appending H-L12 left the range stale; appending H-L13 (this lesson) would have left it stale again. Two prior instances of the same shape — an obligation that names its target by enumerated index into a growing list — were recorded as Z2 in earlier review rounds and each was fixed by bumping the index in the same edit that changed the thing indexed. **Three instances is a structural defect, not bad luck: enumerated ranges in cross-references are fragile by construction, because the obligation to re-bump lives outside the edit that grows the target.** The `DESIGN.md` reference now names the series (`the H-L review-lesson series`, open range) rather than its current tail, so appending a lesson cannot desynchronize a registered document. The same shape — an index that must be re-bumped in a separate edit — is looked for in any future cross-reference whose target grows.
```

### Conventions these establish (as stated in the two prior staging files, re-verified against the file)

1. **Shape:** `N. *(D Mon YYYY)* <concrete incident(s), past tense, named artefacts and numbers> **<one bolded generalizable sentence>** <the practice now in force, or why the class is structurally hard to catch>.`
2. **Date:** italic parenthetical, `D Mon YYYY`, no leading zero; **date recorded** (H-L12, l.218). Today: `17 Aug 2026`.
3. **Exactly one bolded sentence per entry**, a diagnosis or generalization, never an instruction, never the incident narrative. Where two prior lessons are related, the new one names the relation (H-L13 names Z2; H-L9 names the firings) rather than repeating the old one.
4. **Backticks** for filenames, identifiers, and registered vocabulary; section references bare (`§0.2.1`, `§9`).
5. **Length band observed:** 45–162 words by whitespace-token count this pass (H-L13 = 162, H-L9 = 144, median ≈ 65; the two prior staging files quoted "48–155" under a looser count). Multi-instance entries run long by nature; a compact variant is offered for each line so the ceremony can hold the band if it wants to.
6. **Em dashes** for asides; entries end with a period.
7. **Numbering is an ID, not a position.** Source order is `1, 2, 3, 4, 5, 6, 7, 9, 11, 10, 8, 12, 13`. Appending never renumbers.
8. **No entry cites an evidence path.** Provenance stays in this staging file and the ceremony record. Names that are the *subject* of the incident (`leak-detect`, `/results/`, Z2, v20) are fine; scratchpad file paths are not.
9. **List items are consecutive lines with no blank line between them** (l.207–219 verified; l.220 is the single blank before `### H-30`).

---

## 3. The drafted lines

### 3.1 Lesson (a) — citing a clause requires its applied holding, not its principle

**Variant A (recommended) — full form, all three instances named as the brief requires. Insert as list item 14 (see §0 for the landing-order caveat).**

```
14. *(17 Aug 2026)* Three times in one amendment cycle a source was cited for a position its own text did not take. The kill-gate sign-off's draft said the assistant sweep had covered Google Scholar; the sweep's own log lists eight web searches and fetches to PyPI, CRAN, GitHub, arXiv and HAL, and no Scholar. The SC-13 draft's ledger said its admissibility limb resolved the collision with §7.2.1's suppression rule (line 816 at v30); that limb's text disclaimed the triggering state — "A not-run state is not an empty set" — and routed it to the threshold limb, where the rule governed unnamed. SC-13b(b3) said the rule's rationale (line 818 at v30) "decides this", quoting that suppression removes only numbers that measure nothing; the same paragraph holds, for that exact state, that a never-applied combination's yield "is not a measurement of the tool". **Citing a clause in support of a position requires quoting its applied holding on the point at issue, not its principle — a source cited for what it is for, rather than for what it says there, will support anything.** Each was caught by a reviewer reading the source whole, none by the citation's writer; a citation in normative or ledger text now carries the sentence that decides the point beside the sentence relied on.
```

Word count: **218** (whitespace tokens; the same method gives H-L13 = 162 and H-L9 = 144, so the
observed band is 45–162). Above the band by about a third. It is long because the brief requires
three instances each stated as *cited-vs-held*; H-L9 and H-L13, the list's two other multi-instance
entries, are its two longest lines for the same reason. If the ceremony wants the band held, take
Variant B (163) — it names all three instances but not the two draft-clause labels.

**Variant B — compact form, the three instances telegraphed (163 words — at the top of the band):**

```
14. *(17 Aug 2026)* Three citations in one amendment cycle claimed a source for a position its text did not take: a sweep record cited as covering Google Scholar, whose own log lists no such search; a draft clause's admissibility limb cited as resolving a suppression collision, whose own text disclaimed the triggering state — "A not-run state is not an empty set" — and routed it elsewhere; and §7.2.1's rationale paragraph cited as deciding a not-applicable-everywhere yield by its principle, when its applied holding for that state is that such a yield "is not a measurement of the tool". **Citing a clause in support of a position requires quoting its applied holding on the point at issue, not its principle — a source cited for what it is for will support anything.** Each was caught by a reviewer reading the source whole; a citation in normative or ledger text now carries the sentence that decides the point beside the sentence relied on.
```

**Variant C — Variant A with the bolded sentence in the shorter diagnosis form**, if the ceremony wants the bold to match H-L9's brevity:

```
**A source cited for what it is for, rather than for what it says on the point, will support anything; the citation that counts is the applied holding.**
```

**Recommendation: Variant A.** It is the only variant that satisfies the brief's "each named with what
was cited and what the holding actually said" without sending the reader to this staging file. The
line-number references are pinned "at v30" so they stay correct after v30a's insertions shift the
file; the section reference (§7.2.1) is what a reader will navigate by.

**Why the three instances are one lesson and not three.** In each, the writer of the citation
described the source by its *genus* — what kind of statement it is, what it is for — and the source's
*species* on the point at issue said otherwise: a sweep record is "coverage" but its log did not
cover the surface; an admissibility limb is "the collision-resolver" but its text disowned the
colliding state; a rationale paragraph "favours publishing real measurements" but holds that this
particular yield is not one. P7 named the class "citation/characterization/self-description genus"
(§6, row 9). H-L1 is the same class one level up (a claim about the *existence* of a source); H-L11
is its edit-time cousin (an artefact that says one thing while the file says another).

### 3.2 Lesson (b) — a clause answering many questions cannot be corrected, only disturbed

**Variant A (recommended) — full form. Insert as list item 15, immediately after (a).**

```
15. *(17 Aug 2026)* SC-13, the §10.2 replacement criterion, answered eight questions in one clause — when it applies, what the declaration must have supplied, unit, threshold, denominator, the combination without a proof yield, which versions of criterion 3's gates stay in force, and what it does not reach. As one clause it failed three reviews in succession, each correction answering one question and disturbing another: a narrowed denominator, then an unnamed suppression route, then a 0/0 gap and a restated rule. Redistributed under R31 into three single-purpose clauses — criterion, admissibility, interactions — with nothing dropped and nothing landing twice, the same content tripped no stop at its fourth review and drew no finding touching the criterion's semantics; what remained was of the citation genus the preceding lesson records. **A clause that answers many questions cannot be corrected, only disturbed: every patch to one answer moves another, and the fix is structural separation, not a further patch.** This is §0.2.1's "no field answers two questions" at clause scale, and H-L9's coupling rule seen from inside one clause — the coupling was the clause's own breadth.
```

Word count: **186** (whitespace tokens) — above H-L13's 162 by a sentence; the eight-question
enumeration is what carries it over, and it is the load-bearing fact of the lesson. Compact variant:

**Variant B — compact form (121 words):**

```
15. *(17 Aug 2026)* SC-13 answered eight questions in one clause and failed three reviews as one clause — each correction round patched one question and disturbed another: a narrowed denominator, an unnamed suppression route, a 0/0 gap, a restated rule. Split under R31 into three single-purpose clauses with nothing dropped and nothing landing twice, the same content tripped no stop at its fourth review and drew no finding touching the criterion's semantics. **A clause that answers many questions cannot be corrected, only disturbed: every patch to one answer moves another, and the fix is structural separation, not a further patch.** This is §0.2.1's "no field answers two questions" at clause scale, and H-L9's coupling rule seen from inside one clause.
```

**Two dependencies inside (b) that the ceremony must settle:**

1. **"R31".** R31 is the author's working resolution ordering the split (`SC13_SPLIT_ABC.md` l.1
   title and l.24 "Why the split (R31, restated once)"). **No tracked file records R31's text**:
   `grep -rn "R31"` over the repository's `*.md` files returns nothing; the highest working
   resolution recorded in a tracked file is R19 (`ffa6d94` commit message l.14) and R8/R17 in the
   declaration. If R31 is to be cited in `HISTORY.md`, it must be recorded somewhere a reader can
   reach — the v30a amendments block or the ceremony commit message, as R19 was — **or** the line
   drops the number: replace "Redistributed under R31 into" with "Redistributed, on the author's
   decision, into". Both readings are drafted; the brief asked for the citation, so Variant A carries
   it.
2. **"the preceding lesson".** (b) refers to (a) positionally rather than by ID, because (a)'s
   landed number depends on the queue in §0. If the operator prefers `(H-L14)`, it must be the ID (a)
   *actually lands under*. Do not write `(H-L14)` from this file without checking.

**Why (b) is not a repeat of H-L9.** H-L9 (l.214) records a coupling *between two concerns* — the
fixture gate and a reporting tier — where the fix was to *remove* the coupling and the text got
shorter. (b) records a single clause carrying *many concerns of one criterion*, where nothing could be
removed — every one of the eight questions must be answered — and the fix was to *separate* them so
each patch touches one. H-L9's rule says where to patch; (b) says when a clause cannot be patched
at all. The line names the relation in its last sentence rather than restating H-L9.

**The registered principle (b) cites, verbatim — `PREREG.md` l.79 (§0.2.1):**

```
79:> **No field answers two questions.** Where a measurement concept has two independent axes, the specification carries two fields. Compressing them into one guarantees that the single field misdescribes at least one axis on some case — which is how the combination state of §6.6 was defective in the version that introduced it.
```

The split file applies it at clause scale in its own words (`SC13_SPLIT_ABC.md` l.24–30): "The
corrected SC-13 answered eight questions in one clause, and three independent reviews each patched
one answer and disturbed another. That is `PREREG.md` §0.2.1's own defect at clause scale — line
79 …". The `HISTORY.md` line cites §0.2.1 by section and quotes only its five-word title, per
convention 4 and the single-source rule at l.77.

---

## 4. Exact insertion point

| | |
|---|---|
| **File** | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` |
| **Insert** | two new lines **after the current last item of the review-lesson list**. Against the file today that is after l.219 (`13. …`) and before the blank l.220. If the S4 line (and/or R19) has landed first, insert after *that* — the list's last item — and renumber per §0's table. |
| **Order** | (a) first, (b) second, adjacent, no blank line between (convention 9). |
| **Anchor — text the pair follows (today)** | end of l.219: `is looked for in any future cross-reference whose target grows.` — verified to occur **exactly once** in `HISTORY.md` (`grep -c` = 1). |
| **Anchor — text the pair precedes** | current l.220 (blank; verified a bare `$` under `cat -A`), then l.221 `### H-30 — from \`PREREG.md\` §6.6`. |
| **Net effect** | file grows **313 → 315** lines (or 314 → 316 / 315 → 317 if one / both queued candidates land first); everything from the blank line onward shifts down by two. |
| **Renumbering** | **none.** The out-of-order block `…9, 11, 10, 8` stays exactly as it is. |

### 4.1 Edit specification for the ceremony operator

Replacement = the anchor string above + `\n` + Variant A of (a) + `\n` + Variant A of (b). **Assert
match count = 1 for the anchor before the edit and = 1 after** (H-L11, l.215). If the anchor's match
count is 0, the list's tail has changed since this pass — re-read l.207 onward and re-anchor on the
new last item; do not force the edit.

### 4.2 Why staged rather than applied

`HISTORY.md` is hashed in the signed tag message (v30: `e8cf5bbb…`; today's HEAD copy hashes
`c597f653…`, already different because `80401d0` landed H-L12/H-L13/H-34), so any edit outside the
amendment ceremony would leave a fourth unhashed state. The ceremony already opens `HISTORY.md` for
H-35 (`H34_DRAFT.md` §3) and, at the author's option, the S4 line and R19; these two lines ride the
same open, in the lessons list, not the `H-NN` ledger.

---

## 5. `DESIGN.md` l.546 — NO change required. Quoted.

**Working tree, verbatim (the text the ceremony commits):**

```
546:**Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range; the list grows as lessons are appended, and this cross-reference does not enumerate the current tail so appending a lesson cannot desynchronize this document). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
```

This is open-range by construction. It is correct at 13 lessons, at 15, at 17, and at any count.
**Appending (a) and (b) requires no edit to it, and it must NOT be "bumped" to `H-L1 through H-L15`
or any enumerated tail** — doing so would reverse the fix that H-L13 (l.219) records and re-create the
defect in a document the signed tag hashes. `grep -rn "H-L" --include=*.md` over the repository finds
this as the only H-L *range* cross-reference (the others are ID citations, which are stable, and the
ceremony-evidence files that discuss this very line).

**One state fact the ceremony must not lose.** At HEAD `80401d0`, `DESIGN.md` l.546 still reads the
*old* enumerated form:

```
HEAD:546:**Review lessons are recorded in `HISTORY.md`** (**H-L1** through **H-L11**). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
```

The open-range rewrite is an **uncommitted working-tree change** (`git diff --stat`: `DESIGN.md | 30
+++---`, covering the §2.11 prior-art table and this line). Meanwhile H-L13 — which *is* committed at
HEAD — states "The `DESIGN.md` reference now names the series … open range". So HEAD's `HISTORY.md`
describes a `DESIGN.md` fix that HEAD's `DESIGN.md` does not yet contain. The ceremony commit closes
that gap by carrying the working-tree `DESIGN.md`; nothing about (a) or (b) changes what that line
must say. Flagged so no operator "verifies" l.546 against HEAD and concludes the enumerated form is
current.

---

## 6. Provenance and verification status

Everything below was read this pass. Line numbers are as read.

| # | Claim in the drafted lines | Status | Source |
|---|---|---|---|
| 1 | Next free list IDs against the file are 14 and 15; l.219 is item `13.`; l.220 blank | **VERIFIED** | `HISTORY.md` l.207–221 read; `sed -n '219,221p' \| cat -A`; `git diff --stat HISTORY.md` empty; 313 lines |
| 2 | S4-staged all-zero lesson claims 14 and has not landed | **VERIFIED** | `HISTORY_lesson_line_S4_STAGED.md` §3 l.128 ("Insert as list item **14**"); `grep -n "all zero\|reporting zero\|aggregate" HISTORY.md` → no hits; `COMMIT_PLAN.md` l.189, l.206 |
| 3 | R19 recovery lesson flagged for H-L15 / H-L14 | **VERIFIED (quoted)** | `H34_DRAFT.md` l.200–202 |
| 4 | `80401d0` message describes H-L13 as the all-zero lesson; file's H-L13 is the range lesson | **VERIFIED** | `git log -1 --format=%B 80401d0` ("H-L13 records that an aggregate reporting zero…") vs `HISTORY.md` l.219 |
| 5 | **Instance 1** — H-34's draft claimed the sweep "covered Google Scholar and CRAN"; the sweep's own log lists eight WebSearch queries plus fetches to PyPI, CRAN, GitHub, arXiv, HAL; corrected before commit | **VERIFIED (quoted)** | `…\scratchpad\killgate\KILL_GATE_STATUS.md` l.83 (row 3: `line 291, "covered Google Scholar and CRAN"` / "**Google Scholar does not appear** in the sweep's own recorded search log (eight WebSearch queries plus primary fetches to PyPI, CRAN, GitHub, arXiv, HAL)"); `…\killgate\CROSS_TOOL_COMPARISON.md` l.403–405; `80401d0` commit message correction 3 ("The claim that the sweep covered Google Scholar is unsupported by its own recorded search log. Neither sweep searched it"); landed H-34 at `HISTORY.md` l.271 ("did not search Google Scholar either, on its own recorded search log — so that surface is unsearched by both sweeps and is recorded here as a gap rather than as covered") and l.291 |
| 6 | **Instance 2** — the corrected SC-13's ledger (Part 3.4) claimed limb (b) resolved the line-816/§A.12 collision; limb (b)'s own text disclaimed the `not_applicable` state and routed it to limb (d) | **VERIFIED (quoted)** | `M1_CANDIDATE_C_CLAUSE_CORRECTED.md` l.460–461 ("Limb (b) resolves the collision **in favour of §A.12, for this criterion only**: an empty declared set does not get its gate suppressed"); l.181–186 ("**A not-run state is not an empty set, and the two must not be confused.** … A detector that is declared over a non-empty labelled-unit set and then fails to run scores **zero yield and fails limb (d)** … This limb fires only where there is **nothing declared to score**"); N6 verdict, `tasks\w52h2p4lb.output` `result.verifier2` ("The clause's own ledger (Part 3.4) states the collision and asserts that limb (b) settles it — but limb (b)'s text expressly disclaims the triggering state ('A not-run state is not an empty set'), routing it to limb (d) instead. So the ledger claims a resolution the clause does not perform"); restated at `SC13_SPLIT_ABC.md` l.446–450 |
| 7 | **Instance 3** — SC-13b(b3) says "Line 818's own principle decides this rather than fighting it", quoting "Suppression exists to remove numbers that measure nothing, never to remove one that does"; line 818's applied holding for the never-applied combination is the opposite | **VERIFIED (quoted)** | `SC13_SPLIT_ABC.md` l.220–222 (the clause sentence); `PREREG.md` l.818 in full — the cited sentence *and*, two sentences later, "A yield computed over a combination that never applied is not a measurement of the tool: on a corpus of 25 labelled cases it reads `0/25`, which is indistinguishable in print from a mode that ran everywhere and found nothing. The `not_applicable` count carries that fact honestly; the yield does not."; P7 finding 6, `tasks\wb31ayqgv.output` `result.p7` ("the clause's grounding sentence claims support that 818's own text withholds, by quoting the favorable sentence and omitting the adjacent holding") |
| 8 | Lines 816 and 818 sit in §7.2.1 | **VERIFIED** | `PREREG.md` l.802 `### 7.2.1 The runtime formulas, stated canonically`; l.816, l.818 read; P7 finding 13 ("line 816 in §7.2.1") |
| 9 | P7 called the round's new defects "citation/characterization/self-description genus", roughly nine, two in normative text | **VERIFIED (quoted)** | `wb31ayqgv.output` `result.p7.verdict` ("this round introduces roughly nine NEW defects, all of citation/characterization/self-description genus rather than criterion-weakening genus. Two sit in normative clause text") |
| 10 | Each of the three was caught by a reviewer, not by the citation's writer | **VERIFIED** | Instance 1: the killgate audit pass (KILL_GATE_STATUS.md, "Reported, not applied") reported it against the drafted H-34; instance 2: N6 (verifier2); instance 3: P7 finding 6. In each case the writer's own record asserted the citation held (H-34 draft l.291; corrected file Part 3.4; split file l.440–442 "grounded in line 818's own registered principle rather than against it") |
| 11 | SC-13 answered **eight** questions in one clause | **VERIFIED (quoted)** | `SC13_SPLIT_ABC.md` l.742 ("The eight questions the old SC-13 answered") and the Part 7 table l.745–754 (the eight, as paraphrased in the line); P7 finding 1 ("Each of the eight questions is answered by exactly one clause") |
| 12 | "failed three reviews in succession" / "three independent reviews each patched one answer and disturbed another" | **VERIFIED AS THE RECORD'S OWN COUNT; two of the three review files located** | Count: `SC13_SPLIT_ABC.md` l.24–25 (quoted above); P7 self-designates "FOURTH INDEPENDENT VERIFICATION" (`wb31ayqgv.output` `result.p7.item`) and finding 17 ("Rounds 1-3 each introduced defects that touched criterion semantics (narrowed denominator; suppression route; 0/0 gap; restated rule)"). Located: **M3** (`tasks\wkwkawgh8.output` `result.verifier`, "STOP AND REPORT", FAIL on denominator fidelity = *narrowed denominator*) and **N6** (`tasks\w52h2p4lb.output` `result.verifier2`, "STOP-AND-REPORT", test 1 fails = *suppression route*; also the undisposed *0/0* and the *restated rule* among its four regressions). **The third review's file was not located in this session's task outputs**; M3's verdict refers to an earlier §A.12 test that "disqualified candidate B", which is the likely third and predates the clause draft. **H-L9's own caveat applies — "a claim about the ledger's own history is still a claim" — so the author should confirm the count of three before the line lands, or accept it as the record's stated count.** The four named defects are verified independently of the count. |
| 13 | The four round-defects named: narrowed denominator; unnamed suppression route; 0/0 gap; restated rule | **VERIFIED** | M3 check 4 ("FAIL ON FIDELITY … NARROWS the denominator"); N6 verdict test 1 (line 816 route, "the clause text never names, cites, or supersedes line 816"); N6 finding on the per-side 0/0 (split file l.756–759, "N6's undisposed 0/0"); N6 regression 1 (split file l.403, "restatement replaced by citation of SC-3(b)"); P7 finding 17 lists the same four |
| 14 | Split = three single-purpose clauses (criterion / admissibility / interactions), nothing dropped, nothing landing twice | **VERIFIED (quoted)** | `SC13_SPLIT_ABC.md` l.29–30, l.385 ("**Nothing is dropped; nothing lands twice.**"), l.414–419; P7 finding 15(iii) ("I traced all 19 rows — every old element lands in exactly one destination") |
| 15 | Fourth review: no stop; no finding touching criterion semantics; the remaining findings citation-genus | **VERIFIED (quoted)** | P7 verdict "NO STOP. No §A.12 waiver limb is tripped"; finding 17 ("Round 4's new defects are uniformly of citation/characterization/self-description genus: none narrows a denominator, softens a threshold, opens a waiver route, or makes the criterion easier to pass"). **Not overstated as "passed":** P7 also says "Findings only; no adoption recommendation" and requires two normative-text edits before adoption — the line says "tripped no stop … drew no finding that touched the criterion's semantics", which is exactly what P7 found |
| 16 | R31 ordered the split | **VERIFIED as cited in the split file; R31's text NOT on record in any tracked file** | `SC13_SPLIT_ABC.md` l.1, l.24; `wb31ayqgv.output` summary "R31 three-way SC-13 split"; `grep -rn "R31" --include=*.md` over the repo → nothing; highest recorded working resolution in a tracked file is R19 (`ffa6d94` message). See §3.2 dependency 1 |
| 17 | `PREREG.md` §0.2.1 "No field answers two questions" is at l.79 | **VERIFIED (quoted in §3.2)** | `PREREG.md` l.75–79 |
| 18 | `DESIGN.md` l.546 is open-range in the working tree; enumerated at HEAD | **VERIFIED (both quoted in §5)** | `grep -n "H-L" DESIGN.md`; `git show HEAD:DESIGN.md \| grep -n "H-L"`; `git diff DESIGN.md` |
| 19 | Only one H-L range cross-reference repo-wide | **VERIFIED** | `grep -rn "H-L" --include=*.md .` → `DESIGN.md:546` plus ceremony/errata evidence files that discuss it and `PRIOR_ART_VERIFICATION.md` (ID citation) |
| 20 | Date `17 Aug 2026` | **SETTLED by H-L12's own text** | `HISTORY.md` l.218, "Dated by the day recorded, not the day worked" |

### 6.1 Ceremony checklist additions proposed

- [ ] Author decides the S4 all-zero line and R19 first; then assign (a)/(b) their IDs by §0's table. Never write `(H-L14)` inside (b) from this file — use (a)'s landed ID or keep "the preceding lesson".
- [ ] Insert (a) then (b), adjacent, after the list's last item; anchor match count asserted = 1 before and after.
- [ ] **DO NOT touch `DESIGN.md` l.546.** Open-range; correct at any count. Verify it against the **working tree**, not HEAD.
- [ ] Decide whether R31 is recorded (amendments block / commit message) or the R-number is dropped from (b) (§3.2, dependency 1).
- [ ] Author confirms the "three reviews" count or accepts it as the record's own count (§6 row 12).
- [ ] Record in the ceremony note that both are **review lessons**, not firings — firing count stays twenty-one, H-B addendum entry count twenty-three.
- [ ] Record the `80401d0` message/file discrepancy on H-L13 (§0) in the ceremony note; do not rewrite the commit.
- [ ] Re-hash `HISTORY.md` and `DESIGN.md` for the v30a tag message.
