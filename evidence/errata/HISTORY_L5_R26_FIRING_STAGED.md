# STAGED — `HISTORY.md` entry for the 15 October firing (working resolution R26)

**Item S5 / L5. STAGING ONLY.** Nothing in this file has been applied.
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` was **read in full** (313 lines) and is
unmodified by this pass: `git status --short HISTORY.md` is empty, `git diff --stat HISTORY.md` is empty,
HEAD is `80401d0`, working-tree sha256 `c597f653469f42df867321c0db81fb55e3ec66e5194909db3f3daa1e9088f0a0`.
`PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` were read only. No state-changing git command was
run. The archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025` was not opened. The only file written this
pass is this one.

Date recorded: **19 Aug 2026** (the convention H-L12 fixed in its own text, `HISTORY.md` l.218: "Dated by
the day recorded, not the day worked"). The decision the entry records was taken **13 Aug 2026**; the entry
carries both dates and says which is which (§3).

---

## 0. READ FIRST — what R26 says, where it is recorded, and two things the ceremony must not get wrong

### 0.1 R26, verbatim

R26 is not in any tracked file. `grep -rn "R26" --include=*.md` over the repository and over the
`8b1d67a4…\scratchpad` tree returns nothing. Its only record is the session transcript, in the block
**"DELTA R21 (from planning chat, 13 Aug) — schema registration"** (enqueued 2026-08-15T00:44Z), item R26,
which reads:

> R26. The 15 October self-imposed kill is allowed to FIRE, by author decision of 13 Aug 2026. The tool
> waits until after 1 November. Record it as a dated decision with its reasoning — the amendment grew from
> a fixture replacement into a schema registration plus a separate §10.2 replacement criterion, and
> shipping under that deadline would mean registering crisis-drafted rules. Work does not stop; only the
> ship-by date is released. September remains blocked for Concept A; the 1 November application is
> unaffected.

Every element of the drafted entry traces to a sentence of that text or to a line of `PREREG.md` §10
(§6 table below). **Consequence for citation, same as the R31 finding in
`HISTORY_lessons_L14_L15_STAGED.md` §3.2:** if the landed entry names "R26", the resolution must be
recorded somewhere a reader can reach — the v30a amendments block or the ceremony commit message, as R19
was in `ffa6d94`. The drafted entry therefore **does not name R26**; it says "the author's decision of
13 August 2026", which is what R26 is. A variant naming it is one token away and is given in §3.3.

### 0.2 "Criterion 5" is ambiguous inside `HISTORY.md` — always write "§10.2's criterion 5"

`PREREG.md` has two criteria numbered 5: **§10.1's** ("Has had a release or commit within the previous 12
months", l.1024) and **§10.2's** ("Not installable by a stranger by 15 October", l.1042). `HISTORY.md`
already cites the first one — H-34, l.282: "outside §10.1 criterion 5's twelve-month window". An entry
about the second must never say bare "criterion 5". The heading and every sentence of the draft below say
**§10.2's criterion 5**, and the ceremony operator should not shorten it.

### 0.3 The criterion's verb is "stop"; R26's is "work does not stop" — the entry must make the reading visible

`PREREG.md` l.1042 (verbatim): `5. **Not installable by a stranger by 15 October** → stop and resume after
1 November. A date, not a phase number.` R26: "Work does not stop; only the ship-by date is released."

Those two sentences are reconcilable in two ways, and the entry must say which one the author means,
because a reader who compares l.1042 with registration work continuing through late August will
otherwise read the firing as fired-and-ignored — the shape H-L8 (l.217) exists to catch:

- **Reading (i) — "stop" attaches to the release.** Criterion 5 is Phase 3's gate ("A stranger can install
  and run it", l.994; "Release at Phase 3", l.1002) turned into a date. What it stops is the push to ship
  v0.1; what resumes after 1 November is that push. The registration work (v30a, which §10.0 step 0 and
  §10.2 l.1033 require before any Phase 1 development) is not the thing the criterion governs. Under this
  reading R26 narrows nothing.
- **Reading (ii) — "stop" attaches to the project.** The criterion pauses the project until after
  1 November, date-triggered ("A date, not a phase number"). R26 then applies a stop-and-resume
  consequence to the release only and lets the work continue — a **visible narrowing of a registered
  consequence**, which the entry must state as such, and which the author may also want in `DEVIATIONS.md`
  (append-only, currently 0 bytes) as a departure in timing from §10.2 — not as a class C change, since no
  semantics move.

**The draft in §3.1 is written so that it reads true under either reading** — "the criterion's consequence
is stop-and-resume, and the author applies it to the release, not to the work" — and it makes the
application explicit rather than smoothing it. **The author should confirm which reading he holds.** If
(i), the clause may be softened to "what stops is the push to ship, not the project" (§3.3 gives it). If
(ii), the clause stands as drafted and the `DEVIATIONS.md` question is his. Either way the entry does not
decide it for him; it records that the application was made.

---

## 1. Register determination — a ledger note in the main series, beside H-34; NOT an H-B firing; the count does not move

### 1.1 The registers `HISTORY.md` has, and the test applied

Read this pass, top to bottom:

| Register | Where | What it holds | Entry keyed by |
|---|---|---|---|
| **Ledger notes, by ID** — the main series H-01 … H-34 | `## Ledger notes, by ID`, l.11; entries at l.14–157, l.221–223, l.248–292 | H-01 … H-33: errata against a locked clause — what a version said and what it cost. **H-34 (l.264–292): a §10.1 kill-gate disposition** — author-attributed, dated, verdict "does NOT fire" | `### H-NN — from FILE §x.y[ (gloss)]` |
| H-A | l.161–177 | coupling audit table, v7–v18 | version |
| Version ledger | l.181–199 | what a numbered version got wrong | `- **vNN**` |
| Review lessons (H-L) | l.203–219 | dated, generalizable process lessons | `N. *(D Mon YYYY)*` |
| **H-B + H-B addendum** | l.228–230, l.295–313 | **firings of `PREREG.md` §0.2's stopping rule** — "The rule has fired twenty-one times" (l.230); v7 … v30, with two entries marked *not a firing* | version |
| H-C | l.234–244 | the v19 coupling excision | — |

R26 is a firing of **`PREREG.md` §10.2 criterion 5** — one of "Other kill / pause criteria" (l.1028) — a
date-triggered stop-and-resume on the project plan. It is an **event**, not an erratum, not a lesson, and
not a revision of any version.

| Register | Fits? | Why |
|---|---|---|
| **H-B / H-B addendum** | **No — and this is the one that matters.** | H-B's sentence is "**The rule** has fired twenty-one times" (l.230), and the rule is §0.2's stopping rule — a bar-level defect in the pre-tag revision loop produces a new version. Criterion 5 is a different rule with a different trigger (a calendar date) and a different consequence (stop and resume, not a new version), and it has no version to key on. Adding it there would make twenty-one twenty-two and would conflate two rules under one count. **The count stays twenty-one firings, thirteen listed entries, twenty-three entries counted** (l.297, l.313). |
| Review lessons (H-L) | No | A firing is an event. No lesson is derived from it yet — the criterion did what it was written to do. (A lesson about self-imposed dates may come later; none is drafted, none was asked for.) |
| Version ledger | No | No version is implicated; v30a is not retracted. |
| H-A / H-C | No | Pre-tag coupling history. |
| **Main series — ledger note by ID** | **Yes.** | The ledger is "by ID", open, and already holds a §10 gate disposition: **H-34** records §10.1 evaluated and not firing. Working resolution R8 (`AVAILABILITY_DECLARATION.md` l.3665, as quoted in `evidence/ceremony/H34_DRAFT.md` §1) states the principle: "H-nn is an open ledger and an amendment is a first-class event in it." A kill-criterion firing is a first-class event of the same kind as H-34's non-firing. The heading form is H-34's — section plus parenthetical gloss. |

**Register verdict: a main-series ledger note, `### H-36 — from \`PREREG.md\` §10.2 (kill criterion 5,
ship-by date)`, placed beside H-34 and H-35.** State it in the ceremony note as *not a firing under H-B*.

### 1.2 Why not a new register (an "H-D — §10 dispositions" table)

Considered and not recommended. It would hold two rows today (H-34: §10.1, 12 Aug 2026, did not fire;
H-36: §10.2 c.5, 13 Aug 2026, fired) and would require either moving H-34 out of the main series — a
retroactive edit of a committed entry — or duplicating it. The main series already distinguishes the kind
by its heading (`§10.1`, `§10.2`) and H-34 set the precedent. If a third and fourth §10 disposition arrive
(H-34's own re-fire condition, l.289; criterion 2's replacement under R22; criterion 3 at Phase 2), a table
can be added then, by the same open-range rule as §1.3.

### 1.3 How the ledger distinguishes this kind of firing from H-B's — H-L13 applied

Three things, none of which is an enumerated count or an ID range:

1. **The register itself.** H-B is "(from `PREREG.md` §0.2)" and keyed by version; this is a ledger note
   headed "from `PREREG.md` §10.2". A reader who knows the file's structure cannot mistake one for the
   other.
2. **The entry's own last sentence** says it is a §10.2 firing and not a §0.2 one, and that H-B's
   enumeration does not move — **without restating the number twenty-one**. Restating it would create a
   second site that must be re-bumped if the count were ever re-audited (H-L9's "eight of ten" → six is the
   precedent for a ledger count moving), which is exactly the shape H-L13 (l.219) names.
3. **One reconciliation sentence appended at the count** (§5), phrased over *sections*, not IDs: §10
   dispositions "are recorded as ledger notes under those sections' headings, as they occur, and are not
   counted here." §10.1 and §10.2 are locked section numbers; entries under them can grow without anyone
   re-bumping anything. That is H-L13's "name the series, open range" rule applied to a count instead of a
   cross-reference.

**What the entry must NOT do:** it must not add a row to H-B or its addendum; must not touch l.230, l.297
or l.313's numbers; must not write "the twenty-second firing" or any ordinal against H-B's count.

---

## 2. Format exemplars, quoted verbatim with line numbers

From `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` at HEAD `80401d0`.

**Exemplar A — H-34 heading (l.264), the only §10 entry and the heading form followed (section + gloss):**

```
264:### H-34 — from `PREREG.md` §10.1 (kill-gate sign-off, prior art)
```

**Exemplar B — H-33 (l.259–261), the standard main-series body: heading, one blank, one italic
parenthesized paragraph, period inside the paren:**

```
259:### H-33 — from `PREREG.md` §7.7
260:
261:*(v23 gated on a **completed-case false-alarm rate**, which excluded exactly the cases where a finding fired and the schedule later failed — a finding that would reach a user, omitted from the number that decides whether the detector ships experimental. That concept and that name are removed everywhere, not renamed; the active metric is the clean-case finding rate over execution-eligible cases. A global rename in v26 rewrote the old name inside this note, leaving it appearing to retract the metric it was explaining.)*
```

**Exemplar C — H-30 (l.221–223), the longest standard-form entry in the file (104 words by the house
count), showing the register tolerates a multi-clause entry with a worked case inside it:**

```
221:### H-30 — from `PREREG.md` §6.6
222:
223:*(v20's §0.2 named `CombinationCaseState` a fresh surface. The edit that was supposed to define it did not apply, and the file kept the sentence claiming §7.7's states suffice. They do not: §7.7 defines a *detector-case* state, and the two collapse. Take an evaluation case where the preserving strategies complete and produce PROVEN while every promoted strategy fails its frame's determinism guard. The detector-case is complete. For the promoted row, nothing said whether the case was completed, `could_not_run(determinism)`, in the promoted false-alarm denominator, or counted against the promoted 60% floor — and each answer moves evidence yield, completion rate, failure rate, and the experimental designation.)*
```

**Exemplar D — H-34's block body, opening and closing lines (l.266–269, l.287, l.289, l.292), the one
author-attributed, dated entry; its form is a departure flagged in `evidence/ceremony/COMMIT_PLAN.md` §3:**

```
266:---
267:KILL-GATE SIGN-OFF — PREREG.md §10.1 (prior art)
268:Date: 12 August 2026
269:Author: Theo Johann Howard
287:Judgment: §10.1 does NOT fire. No existing tool probes a user-supplied callable at runtime against a declared per-cell availability model. The runtime black-box probe is prior art (`leak-detect`) and is not claimed; the per-cell availability model is the novel element and no candidate implements it. The project proceeds.
289:Re-fire condition: if a tool implementing runtime probing against a per-cell availability model surfaces before Phase 2 completes, this gate re-triggers and this sign-off is void.
292:---
```

**Exemplar E — the date convention the brief asks the entry to carry, H-L12 (l.218), last sentence:**

```
218:… Dated by the day recorded, not the day worked — the convention this list follows from here.
```

**Exemplar F — the count the entry must not move, H-B addendum (l.297, l.313):**

```
297:The enumeration above stops at v17 because it was written then — ten firings. Completing it below adds **eleven**, for twenty-one. **Two entries are marked *not a firing*:** v19 and v23 were author-initiated restructures, not stopping-rule firings, and are listed only so the chain reads continuously. A verifier counting entries rather than firings will get twenty-three; the reconciliation is here.
313:Ten above plus eleven here: **twenty-one firings**, in thirteen listed entries. Every one is in this file with its cause.
```

**Spacing, measured with `cat -A` this pass (ll.259–266, 290–295):** heading, **one** blank line,
paragraph, **two** blank lines, next `###`. H-34's block is fenced by bare `---` (l.266, l.292) and is
followed by two blank lines (l.293–294) before `### H-B addendum` (l.295).

### Conventions these establish, as applied to the draft

1. **Heading:** `### H-NN — from \`PREREG.md\` §10.2 (gloss)` — H-34's form; the gloss names the
   criterion and the date, as H-34's names the gate and its subject.
2. **Body:** one paragraph in `*(` … `)*`, period inside. Not H-34's block (§3.2 gives the block variant
   if the author wants the two §10 dispositions to match; the paragraph is recommended because H-34's
   block is already flagged as a departure and a sign-off's attestation form does not fit a decision).
3. **Date:** stated inside the paragraph, both the recorded date and the decision date, with the
   convention named — the main-series paragraphs are otherwise undated, so this is said once, plainly.
4. **Register of voice:** past tense where it reports, present where it states what is now in force;
   quotes the locked clause verbatim; `§` bare; backticks for filenames; em dashes; no line numbers (H-L
   drafts pin lines "at v30"; main-series entries cite sections only).
5. **No evidence paths, no hashes, no R-numbers** — H-34 and H-25 cite none.
6. **Length band:** main series max is H-30 at 104 words; the H-35 draft the ceremony already carries is
   182 (`H34_DRAFT.md` §3.1, recommended there on the ground that "the register tolerates length when the
   entry carries more than one defect"). Variant A below is 201 by the same count — it carries seven
   required elements (date and convention, the firing and its timing, the reason, the release, the three
   non-releases, the register disambiguation) — and a 116-word variant is given.

---

## 3. THE DRAFT

### 3.1 Variant A (recommended) — the complete entry, 201 words by the house count

```markdown
### H-36 — from `PREREG.md` §10.2 (kill criterion 5, ship-by date)

*(Recorded 19 August 2026 — dated by the day recorded, not the day worked, the convention H-L12 set — for the author's decision of 13 August 2026: §10.2's criterion 5, "Not installable by a stranger by 15 October → stop and resume after 1 November", is allowed to fire, nine weeks ahead of its date, on the author's determination that the condition will hold rather than on the calendar's. The reason is the amendment's growth: a fixture replacement under §6.2 became a schema registration — `PREREG.md` takes the generic clauses, the declaration supplies the data — plus a separate replacement for §10.2's criterion 2, which §10.2 requires committed before any development-corpus contact. Registering those against a ship-by date would mean registering crisis-drafted rules. The firing releases one thing, the ship-by date: v0.1 waits until after 1 November. The criterion's consequence is stop-and-resume, and the author applies it to the release, not to the work — the registration continues, September stays blocked for Concept A, and the 1 November application is untouched. A firing of §10.2, the first of that section's criteria to fire, and not of §0.2's stopping rule: it is not counted with those, and H-B's enumeration does not move.)*
```

**Word count: 201** (backticks and asterisks stripped, `wc -w` — the method `H34_DRAFT.md` §2 used for the
house figures: H-30 = 104, H-32 = 84, H-33 = 83, H-31 = 26). One paragraph, one pair of italic parens,
period inside. **Every sentence answers to one of the brief's required elements:**

| Sentence | Carries |
|---|---|
| "Recorded 19 August 2026 … decision of 13 August 2026" | both dates; the H-L12 convention, named and quoted ("the day recorded, not the day worked") |
| "§10.2's criterion 5, '…', is allowed to fire, nine weeks ahead of its date, on the author's determination …" | the criterion, verbatim; that it fires; that it fires early and why that is honest — on a determination the condition will hold, stated as such rather than dressed as the calendar's verdict |
| "The reason is the amendment's growth: … schema registration … plus a separate replacement for §10.2's criterion 2 …" | R26's reasoning, with what "schema registration" means (R24) and why the replacement criterion is on the critical path (l.1031/1033) |
| "Registering those against a ship-by date would mean registering crisis-drafted rules." | R26, verbatim in substance |
| "The firing releases one thing, the ship-by date: v0.1 waits until after 1 November." | what it releases |
| "The criterion's consequence is stop-and-resume, and the author applies it to the release, not to the work — the registration continues, September stays blocked for Concept A, and the 1 November application is untouched." | what it does not release (all three of R26's); and the visible application of "stop" (§0.3) |
| "A firing of §10.2, the first of that section's criteria to fire, and not of §0.2's stopping rule: it is not counted with those, and H-B's enumeration does not move." | register disambiguation without restating the count (§1.3) |

### 3.2 Variant B — H-34's block form, if the author wants the two §10 dispositions to match

```markdown
### H-36 — from `PREREG.md` §10.2 (kill criterion 5, ship-by date)

---
KILL-CRITERION FIRING — PREREG.md §10.2 criterion 5 (ship-by date)
Decision: 13 August 2026 (author). Recorded: 19 August 2026 — dated by the day recorded, not the day worked (H-L12).
Author: Theo Johann Howard

§10.2's criterion 5 — "Not installable by a stranger by 15 October → stop and resume after 1 November" — is allowed to FIRE, nine weeks ahead of its date, on the author's determination that the condition will hold rather than on the calendar's.

Reason: the amendment's growth. A fixture replacement under §6.2 became a schema registration (`PREREG.md` takes the generic clauses, the declaration supplies the data) plus a separate replacement for §10.2's criterion 2, which §10.2 requires committed before any development-corpus contact. Registering those against a ship-by date would mean registering crisis-drafted rules.

Released: the ship-by date. v0.1 waits until after 1 November.

Not released: the work, which continues — the criterion's stop-and-resume is applied to the release, not to the work; September, which stays blocked for Concept A; the 1 November application, which is untouched.

Register: a firing of §10.2, the first of that section's criteria to fire. Not a firing of §0.2's stopping rule; not counted with those; H-B's enumeration does not move.
---
```

**Not recommended**, for three reasons already on the record: `COMMIT_PLAN.md` §3 flags H-34's block as a
departure from the one-paragraph convention "every other main-series entry follows" and notes that its
closing `---` "sits immediately above `### H-B addendum`, where a reader will take it as a section
divider" — a second block doubles both; H-34's first-person attestation fits a search the author
personally ran and signed, not a decision the ledger records in its own voice (the body above is
therefore kept in the ledger's voice — **the drafter does not put a first-person attestation in the
author's mouth; if he wants one, it is his text**); and the block adds lines without adding content.
Offered so the choice is his.

### 3.3 Variant C — compact, 116 words, for a ceremony that wants to hold near the house band

```markdown
### H-36 — from `PREREG.md` §10.2 (kill criterion 5, ship-by date)

*(Recorded 19 August 2026 — dated by the day recorded, not the day worked, per H-L12 — for the author's decision of 13 August 2026: §10.2's criterion 5, "Not installable by a stranger by 15 October → stop and resume after 1 November", is allowed to fire nine weeks early. The amendment grew from a fixture replacement into a schema registration plus a separate replacement for §10.2's criterion 2; registering those against a ship-by date would mean registering crisis-drafted rules. Released: the ship-by date — v0.1 waits until after 1 November. Not released: the work, which continues; September, blocked for Concept A; the 1 November application. A §10.2 firing, not §0.2's; H-B's count does not move.)*
```

It drops: *why* early firing is honest (the determination clause), *what* a schema registration is, *why*
the replacement criterion is on the critical path, and the explicit application of "stop" to the release.
A reader who has not seen R26 learns that the date was released and why, but not how the criterion's own
verb was applied. **Variant A is recommended** for the same reason `H34_DRAFT.md` gave for its 182-word
H-35: the register tolerates length when the entry carries more than one thing, and this one carries a
firing, its reasoning, its scope, and its register.

**Token-level options inside Variant A, author's choice:**

- **Naming the resolution:** replace "for the author's decision of 13 August 2026" with "for working
  resolution R26, the author's decision of 13 August 2026" — **only if R26 is recorded in a tracked file
  or the ceremony commit message** (§0.1). Otherwise leave it out.
- **Reading (i) of "stop"** (§0.3): replace "The criterion's consequence is stop-and-resume, and the
  author applies it to the release, not to the work — the registration continues, September …" with "What
  stops is the push to ship, not the project — the registration continues, September …". Shorter by nine
  words; says less. Use only if the author holds reading (i).
- **Recording date:** if the operator takes "the day recorded" to mean the day the entry lands in
  `HISTORY.md` rather than the day it was written, change `19 August 2026` to the ceremony date. Either is
  H-L12-consistent. **What is not:** dating the entry 13 August 2026 — that is the day worked, and the
  convention exists to forbid exactly that substitution. The decision date stays inside the text as a
  decision date under any choice.

---

## 4. Exact insertion point

| | |
|---|---|
| **File** | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` |
| **Where** | In the main series, **immediately after H-35** (the amendment entry `H34_DRAFT.md` §3 places after H-34's closing `---` at l.292 and before `### H-B addendum` at l.295) and **before `### H-B addendum — firings v18 through v30`**. If H-35 has not landed when this does, the same anchor applies: before `### H-B addendum`, after the two blank lines that follow H-34's `---`. |
| **Anchor — text the entry precedes** | `### H-B addendum — firings v18 through v30` — verified to occur **exactly once** (`grep -c` = 1, l.295 today). |
| **Anchor — text the entry follows (today, H-35 not yet landed)** | l.292 `---` (H-34's closing rule), then blank l.293, blank l.294. With H-35 landed: H-35's paragraph, then its two trailing blanks. |
| **Shape inserted** | five lines: `### H-36 — …` / blank / `*( … )*` / blank / blank — heading, one blank, paragraph, two blanks, matching ll.259–264 as measured. (Variant B inserts its block plus two blanks, as H-34 does at ll.264–294.) |
| **IDs** | **H-36 is provisional.** Verified this pass: `grep -n '^### H-3'` returns H-30, H-31, H-32, H-33, H-34 — H-35 is free against the file and is claimed by the amendment entry (`H34_DRAFT.md` §1, `COMMIT_PLAN.md` §3, `CEREMONY_COMMANDS.md` A4); no file in the repo or the scratchpad tree claims H-36 (`grep -rn "H-3[5-9]"`). If the author takes `H34_DRAFT.md` §1's path (b) and renumbers the sign-off to H-35 with the amendment at H-34, this entry is still H-36. If for any reason the amendment entry does not land, this entry takes **H-35** — assign at landing, as the IDs have always been. |
| **Net effect** | 313 → 318 lines if this lands alone; 318 → 323 with H-35 landed first. The reconciliation sentence (§5) adds no line. |
| **Renumbering** | none. |

### 4.1 Edit specification for the ceremony operator

Replacement = the five-line block of §3.1 (or §3.3) + `\n` + the anchor `### H-B addendum — firings v18
through v30`, substituted for the anchor alone. **Assert anchor match count = 1 before the edit and = 1
after** (H-L11, l.215). If the count is 0 the file's tail has changed since this pass — re-read from l.259
and re-anchor; do not force the edit. After the edit, `grep -c '^### H-36 '` must be 1 and `grep -c '^###
H-B addendum'` must be 1.

### 4.2 Why staged rather than applied

`HISTORY.md` is hashed in the signed tag message (v30: `e8cf5bbb…`; today's working tree already differs
at `c597f653…` because `80401d0` landed H-L12/H-L13/H-34). Any edit outside the amendment ceremony leaves a
further unhashed state. The ceremony already opens `HISTORY.md` for H-35 and, at the author's option, the
S4 line, R19, and the L14/L15 pair; this entry rides the same open.

---

## 5. The count-reconciliation sentence the ledger needs

**Append to l.313**, after "Every one is in this file with its cause." — same paragraph, no new line:

```
That count is of §0.2's stopping rule and of nothing else: the kill and pause criteria of §10.1 and §10.2 are a different rule, and their dispositions — fired or not — are recorded as ledger notes under those sections' headings, as they occur, and are not counted here.
```

**49 words.** Anchor: the full l.313 — `Ten above plus eleven here: **twenty-one firings**, in thirteen
listed entries. Every one is in this file with its cause.` — verified to occur **exactly once**. Assert
match count 1 before and after.

**Why it is shaped this way (H-L13):** it names the *sections* whose dispositions are excluded (§10.1 and
§10.2 — locked section numbers that do not grow) and the *kind* of entry they take (ledger notes under
those headings), and it names no ID, no range, and no count of them. H-34 and H-36 satisfy it today; a
third §10 disposition — H-34's re-fire condition (l.289), criterion 2's replacement, criterion 3 at Phase 2
— satisfies it without anyone editing l.313 again. Contrast the form to avoid: "the §10 dispositions are
H-34 and H-36" — true today, stale at the next one, and the obligation to re-bump would live outside the
edit that adds it, which is the defect H-L13 records at its third instance.

**Why it goes at l.313 and not only inside H-36:** a verifier counting firings reads the count, not the
main series. The H-B paragraph at l.230 ("The rule has fired twenty-one times") already names *the rule*;
the addendum at l.297 already reconciles entries-vs-firings (twenty-three vs twenty-one). This sentence
adds the third reconciliation the file now needs — firings-of-which-rule — at the line where the other
two are. **Optional but recommended.** If the author prefers the entry alone to carry the disambiguation,
Variant A's last sentence does so and l.313 stays byte-identical; the risk is a reader of the addendum who
never reaches H-36.

**What this sentence must not be mistaken for:** it changes no number. Twenty-one, thirteen, twenty-three
stand.

---

## 6. Provenance and verification status

Everything below was read this pass. Line numbers are as read, against HEAD `80401d0` working tree.

| # | Claim in the drafted entry | Status | Source |
|---|---|---|---|
| 1 | `HISTORY.md` 313 lines, clean at HEAD, sha256 `c597f653…` | **VERIFIED** | `git status --short HISTORY.md` empty; `git diff --stat` empty; `sha256sum`; `wc -l` |
| 2 | R26 text as quoted in §0.1; dated 13 Aug 2026; "Work does not stop; only the ship-by date is released"; "September remains blocked for Concept A; the 1 November application is unaffected" | **VERIFIED (quoted)** | session transcript, "DELTA R21 (from planning chat, 13 Aug)" block, item R26; acknowledged in-session as "the 15 October kill fires by author decision of 13 Aug 2026, ship-date released to after 1 November, work continues". **Not in any tracked file** (`grep -rn "R26"` over repo `*.md` and the `8b1d67a4…\scratchpad` tree: nothing). The auto-memory index (`phase0-findings.md`, DELTA R24 paragraph) also records "R26: 15 Oct kill FIRED by author decision, ship after 1 Nov". |
| 3 | Criterion text "Not installable by a stranger by 15 October → stop and resume after 1 November. A date, not a phase number." is §10.2 item 5 | **VERIFIED (quoted verbatim, bold stripped; `grep -c` = 1 on l.1042)** | `PREREG.md` l.1042; §10.2 heading l.1028 "Other kill / pause criteria"; the list numbers 2, 3, 4, 5 |
| 4 | "§10.2's criterion 5" is needed because §10.1 also has a criterion 5, and `HISTORY.md` already cites that one | **VERIFIED** | `PREREG.md` l.1024; `HISTORY.md` l.282 ("§10.1 criterion 5's twelve-month window") |
| 5 | "nine weeks ahead of its date" | **VERIFIED (arithmetic)** | 13 Aug → 15 Oct 2026 = 18 + 30 + 15 = 63 days = 9 weeks exactly |
| 6 | "a fixture replacement under §6.2" was the amendment's origin | **VERIFIED** | `H34_DRAFT.md` §3.1 (v30a "carries the §6.2 conformance walk resolving all four, the fixture re-based on the recomputed LightGBM trio"); memory note A1 ("Still routes to class C amendment `prereg-v30a`; §6.2 never patched directly") |
| 7 | "became a schema registration — `PREREG.md` takes the generic clauses, the declaration supplies the data" | **VERIFIED (quoted)** | R24, same DELTA block: "v30a registers the SCHEMA, not the instance. PREREG.md gains a small set of generic clauses; the declaration supplies the data"; `K1_SCHEMA_CLAUSES.md` l.11–18; `SCHEMA_SET_ADOPTION.md` (SC-1 … SC-13c) |
| 8 | "plus a separate replacement for §10.2's criterion 2" | **VERIFIED** | `K5_REPLACEMENT_CRITERION_OPTIONS.md` l.3–5 ("produced because R22 determined that R9's §6.2 criterion-3 amendment does **not** discharge PREREG.md line 1033"); SC-13a/b/c in `SCHEMA_SET_ADOPTION.md`; `K1_SCHEMA_CLAUSES.md` row 28 / F-1 ("Until then §10.2's branch is live") |
| 9 | "which §10.2 requires committed before any development-corpus contact" | **VERIFIED (quoted)** | `PREREG.md` l.1031 ("the replacement is written before any development-corpus contact, not after tuning") and l.1033 ("commit and timestamp a class C amendment carrying the complete replacement criterion … and only then begin Phase 1 development or inspect the development corpus") |
| 10 | "Registering those against a ship-by date would mean registering crisis-drafted rules" | **VERIFIED (R26 verbatim in substance)** | R26: "shipping under that deadline would mean registering crisis-drafted rules" |
| 11 | "v0.1 waits until after 1 November" | **VERIFIED** | R26 "The tool waits until after 1 November"; `PREREG.md` l.994 Phase 3 "**Public v0.1 release** … A stranger can install and run it"; l.1002 "**Release at Phase 3.**" — criterion 5 is that gate as a date |
| 12 | "September stays blocked for Concept A" | **VERIFIED** | `PREREG.md` l.987 "**Concept A pre-registration — September. UChicago — 1 November.** Neither moves. Phases 2+ do not run in September."; l.1041 criterion 4; R26 |
| 13 | "the 1 November application is untouched" | **VERIFIED** | R26 "the 1 November application is unaffected"; `PREREG.md` l.987 |
| 14 | "the first of that section's criteria to fire" | **VERIFIED against the file; H-L9's caveat applies** | `grep -n '§10' HISTORY.md`: l.31 (H-04, §10.0), l.264–287 (H-34, §10.1 does NOT fire), l.303 (v22, §10.2's gate as a *defect*, not a firing). No §10.2 criterion is recorded as having fired; `DEVIATIONS.md` is 0 bytes. Criterion 2's R22 branch is a *replacement*, not a firing. A claim about the ledger's own history is still a claim — the author may strike "the first of that section's criteria to fire" at no cost to the rest. |
| 15 | H-B counts §0.2 firings only; twenty-one / thirteen / twenty-three | **VERIFIED (quoted §2, Exemplar F)** | `HISTORY.md` l.230, l.297, l.313 |
| 16 | H-34 is a §10.1 disposition in the main series; R8's "open ledger … first-class event" | **VERIFIED (quoted)** | `HISTORY.md` l.264–292; `H34_DRAFT.md` §1 quoting `AVAILABILITY_DECLARATION.md` l.3665 |
| 17 | H-35 is claimed by the amendment entry; H-36 unclaimed | **VERIFIED** | `H34_DRAFT.md` §1, §3; `COMMIT_PLAN.md` §3; `CEREMONY_COMMANDS.md` l.111, l.185; `grep -rn "H-3[5-9]"` over repo and scratchpad: only H-35 references, all to the amendment entry |
| 18 | Anchors unique: `### H-B addendum — firings v18 through v30`; full l.313 | **VERIFIED** | `grep -c` = 1 each |
| 19 | Spacing: heading / one blank / paragraph / two blanks; H-34's `---` at l.292 followed by two blanks | **VERIFIED** | `cat -A` over ll.259–266 and 290–295 |
| 20 | H-L12 convention text | **VERIFIED (quoted §2, Exemplar E)** | `HISTORY.md` l.218 |
| 21 | `DEVIATIONS.md` empty | **VERIFIED** | `wc -c` = 0 |
| 22 | House word counts H-30 = 104, H-32 = 84, H-33 = 83, H-31 = 26 | **VERIFIED (re-measured)** | `sed 's/[\`*]//g' \| wc -w` on l.223, 255, 261, 250 |

### 6.1 Flags for the author and the ceremony — none decided here

- [ ] **Which reading of "stop" (§0.3).** Variant A's clause makes the application visible under either; confirm, and decide whether reading (ii) wants a `DEVIATIONS.md` line for the timing departure. This is the one substantive call in the entry.
- [ ] **R26 on the record or not (§0.1).** If cited by number, record it (amendments block / commit message); otherwise the entry stays as drafted, unnumbered.
- [ ] **"the first of that section's criteria to fire"** — keep or strike (§6 row 14).
- [ ] **ID at landing** — H-36 after H-35; H-35 if the amendment entry does not land; never assigned from this file.
- [ ] **Reconciliation sentence at l.313** — recommended; optional (§5). Match count 1 before and after.
- [ ] **No reciprocal pointer is drafted.** A `*(→ \`HISTORY.md\` H-36)*` at `PREREG.md` l.1042 would be a locked-file edit and belongs only inside the reviewed v30a diff; H-34 has none at §10.1 and eight main-series entries have none (`H34_DRAFT.md` §5). Not required.
- [ ] **H-34's re-fire condition (l.289) is phase-indexed** ("before Phase 2 completes"), not date-indexed; the firing moves dates, not phases, so H-34's verdict and its re-fire window are unaffected. Nothing in H-34 needs editing; noted so nobody "updates" it.
- [ ] **Always "§10.2's criterion 5"** in heading and text (§0.2). Do not shorten.
- [ ] Record in the ceremony note: **a ledger note, not a firing under H-B** — twenty-one / thirteen / twenty-three stand.
- [ ] Re-hash `HISTORY.md` for the v30a tag message after all additions land.
