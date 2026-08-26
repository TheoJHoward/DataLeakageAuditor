# STAGED — `HISTORY.md` review-lesson line #2 (the all-zero control)

**Item S4, HISTORY part. STAGING ONLY.** Nothing in this file has been applied.
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` was **read only** and is
unmodified by this pass. No repo file was touched. No git command that changes state was run.

---

## 0. STOP — the item's two stated premises are both stale. Read this section before the draft.

Item S4 was written against the state of the world when `HISTORY_lesson_line_STAGED.md` (the
H-L12 staging file) was authored. Since then the H-L12 pair **landed in the working tree**, and a
**second** lesson (H-L13) landed with it. Both of S4's premises are now false against the file.

| S4's premise | Actual working-tree state (re-read this pass) | Consequence |
|---|---|---|
| "stage a second lesson … **as H-L13**" | `HISTORY.md` l.219 **already is** H-L13 — the cross-reference-fragility lesson, dated 12 Aug 2026 | **The next free ID is 14, not 13.** Drafting as 13 would collide with a landed entry. |
| "`DESIGN.md` line ~546's cross-reference becomes '**H-L1 through H-L13**', so the companion edit changes again" | `DESIGN.md` l.546 **no longer enumerates a tail.** It was rewritten to an open-range series reference — the fix that H-L13 exists to record | **No companion edit is required, and writing "H-L1 through H-L13" would REVERSE the H-L13 fix and re-create the exact defect H-L13 names.** See §4. |

The rest of this file is written against the verified state, not against the premises. Section 4
is the one the ceremony must read.

### 0.1 Verified working-tree state, re-read this pass

`HISTORY.md` is **313 lines** (`wc -l`). The lessons list at l.207–219 ends:

```
217:8. *(31 Jul 2026)* §0.2.1 was written to justify stopping the revision loop, …
218:12. *(12 Aug 2026)* An archive-wide survey for the two aggressor columns reported 37 files; …
219:13. *(12 Aug 2026)* A cross-reference in `DESIGN.md` §9 named the review-lesson list as `H-L1 through H-L11`. …
220:(blank — confirmed by `sed -n '218,221p' … | cat -A`, line 220 is a bare `$`)
221:### H-30 — from `PREREG.md` §6.6
```

`git diff` confirms l.218–219 are **working-tree additions not in `HEAD`** (`HISTORY.md | 33 +`,
which also covers the H-34 ledger entry added at l.265+). `DESIGN.md | 30 +++---` covers the
§2.11 prior-art table rewrite **and** the l.546 change.

`DESIGN.md` l.546, verbatim, as it stands now:

```
546:**Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range; the list grows as lessons are appended, and this cross-reference does not enumerate the current tail so appending a lesson cannot desynchronize this document). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
```

A repo-wide `grep -rn "H-L" --include=*.md` finds **exactly one** H-L cross-reference outside
`HISTORY.md` itself: this l.546. (`PRIOR_ART_VERIFICATION.md` l.3 cites `H-L1` by ID, not by
range — an ID citation is stable and needs no maintenance.) There is no second index to bump.

---

## 1. Register determination — review lesson, same as H-L12

The H-L12 staging file's four-register table applies unchanged; only the "fits?" reasoning
differs. Restated for this entry:

| Register | Fits? |
|---|---|
| Ledger notes `H-01`…`H-34` (`## Ledger notes, by ID`) — errata against a **specific locked clause** of `PREREG.md`/`DESIGN.md` | **No.** No clause is defective. The near-miss was in a Phase 0 derivation script, not in the specification text. |
| Version ledger (`- **vNN**`) — what a numbered version got wrong | **No.** No version is implicated; the published record is correct (see §2.1). |
| **Review lessons** (l.203, list l.207–219) — dated, generalizable process/method lessons | **YES.** Directly parallel to H-L11 (a silent `str.replace` no-match) and H-L12 (a silently under-reporting survey): a mechanism that fails without signalling, plus the control now in force. |
| Firings (`## H-B`, `### H-B addendum`) — stopping-rule firings under `PREREG.md` §0.2 | **No.** The stopping rule did not fire. |

**Register verdict: review lesson.** State it in the ceremony note. The firing count stays at
**twenty-one**, the H-B addendum entry count at **twenty-three**. Note that H-L12, H-L13 and this
entry are now **three** lesson additions in one ceremony that must not be miscounted as firings —
the addendum at l.264 already warns that entry-counting and firing-counting diverge.

**Normative-vs-history split.** `HISTORY.md` l.3: "**Not a normative file.** Nothing here
instructs an implementer." The *binding* form of this rule is **§F.3 of the availability
declaration** ("An aggregate that comes back empty must be PROVED empty before it may be
reported, and a failed proof RAISES"). The `HISTORY.md` line records the incident and the
practice; it does not carry the obligation. This is why the drafted line below states the control
as a fact in force, not as an instruction. **See §5.3 — the repo's declaration copy does not yet
contain §F.3.**

---

## 2. Format exemplars, quoted verbatim with line numbers

From `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md`.

**Section header and list preamble — l.203, l.205:**

```
203:## Review lessons (from `DESIGN.md` §9)
205:**Review lessons, dated.**
```

**Exemplar A — l.207 (H-L1), the shortest form:**

```
207:1. *(28 Jul 2026)* v3 claimed no existing tool probed at runtime. The claim survived several review rounds and was false; `leak-detect` had been on PyPI for six years. **Models are poor at telling you something already exists.** Prior-art verification is a search task, done by the author, written down.
```

**Exemplar B — l.215 (H-L11), the closest *semantic* match — a mechanism that fails silently, with a remediation clause:**

```
215:11. *(1 Aug 2026)* Three of v20's announced fixes were never in the file. They were applied as silent string substitutions that did not match, and spot-checking a few of them passed. **An edit that reports nothing when it fails is indistinguishable from an edit that worked**, and a change log written from intent rather than from the file will confidently describe fixes that do not exist. Every edit now asserts its match count, and the change log is written from a diff of the file.
```

**Exemplar C — l.218 (H-L12), as it actually landed** — note it differs from the H-L12 staging file's Variant A: `so that parquet stays out of git` became `to keep parquet out of git`, and a **date-convention clause was appended**:

```
218:12. *(12 Aug 2026)* An archive-wide survey for the two aggressor columns reported 37 files; a filesystem walk over the same root found 119. The search tool honours the archive's `.gitignore`, which excludes `/PC2_TRANSFER_v4/scripts/` and `/results/` to keep parquet out of git — and with them two mirrored code trees, including the archive's only copy of the Phase 7 simulator, where a confirmed aggregation defect was later found. **A survey that inherits a search tool's default exclusions measures the ignore list, not the archive.** Archive-wide counts now come from a filesystem walk that reports how many files it scanned. Dated by the day recorded, not the day worked — the convention this list follows from here.
```

**Exemplar D — l.219 (H-L13), the current last line in the file** (this is the insertion anchor):

```
219:13. *(12 Aug 2026)* A cross-reference in `DESIGN.md` §9 named the review-lesson list as `H-L1 through H-L11`. Appending H-L12 left the range stale; appending H-L13 (this lesson) would have left it stale again. Two prior instances of the same shape — an obligation that names its target by enumerated index into a growing list — were recorded as Z2 in earlier review rounds and each was fixed by bumping the index in the same edit that changed the thing indexed. **Three instances is a structural defect, not bad luck: enumerated ranges in cross-references are fragile by construction, because the obligation to re-bump lives outside the edit that grows the target.** The `DESIGN.md` reference now names the series (`the H-L review-lesson series`, open range) rather than its current tail, so appending a lesson cannot desynchronize a registered document. The same shape — an index that must be re-bumped in a separate edit — is looked for in any future cross-reference whose target grows.
```

### Conventions these establish (updated for the two landed lines)

1. **Shape:** `N. *(D Mon YYYY)* <concrete incident, past tense, named artefacts and numbers> **<one bolded generalizable sentence>** <the control now in force>.`
2. **Date — SETTLED, no longer ambiguous.** The H-L12 staging file flagged the local-vs-UTC question as "author to confirm". H-L12 **as landed answers it in the line itself**: "Dated by the day recorded, not the day worked — the convention this list follows from here." Today's recorded date is **13 Aug 2026**. Format: italic parenthetical, `D Mon YYYY`, no leading zero. H-L13 rode 12 Aug because it was recorded that day; this entry is recorded today and takes **13 Aug 2026**. No author confirmation is outstanding.
3. **Exactly one bolded sentence per entry.** Never the incident narrative. Sits mid-entry (A, B, C, D). Every existing bold is a **diagnosis or generalization, never an instruction** — consistent with l.3's "Nothing here instructs an implementer".
4. **Backticks** for filenames, paths, column names and identifiers. Section references bare (`§9`, `§0.2.1`).
5. **Length — band has widened.** The H-L12 staging file observed 48–110 words. H-L12 landed at ~95 and **H-L13 at ~155**. Observed band is now **48–155**, median ≈ 65. A ~120-word entry is inside it; a shorter variant is offered anyway (§3.1).
6. **Em dashes** for asides; entries end with a period.
7. **Numbering is an ID, not a position.** Source order is `1, 2, 3, 4, 5, 6, 7, 9, 11, 10, 8, 12, 13` — deliberately non-sequential for the older block. Appending does not renumber. **The next free ID is 14.**
8. **No entry cites an evidence path.** Provenance stays in this staging file and the ceremony record. (H-L12 names archive paths — `/results/` — but those are the *subject* of the incident, not citations.)

---

## 3. The drafted line

Insert as list item **14** (= `H-L14`). **Not 13 — 13 is taken (§0).**

```
14. *(13 Aug 2026)* A re-derivation restricted to the four `trades_*` classes was keyed on column names the source CSV did not carry. It returned all zero and raised nothing, because absent keys aggregate to an empty group rather than to an error — and that zero read as *the trade-class restriction makes the corrected side clean*, the exact false result the check existed to catch. A human eye on one CSV row caught it; no control did. **A zero is the one result a broken aggregation and a true measurement produce identically, so an aggregate reporting zero or all-clean is not a finding until its keys have been machine-checked against its source.** Every such aggregate now asserts that its keys resolve and that the source is non-empty on them, and a mismatch raises rather than prints.
```

**121 words** — inside the 48–155 observed band, well under H-L13's 155. One bolded sentence,
mid-entry, in diagnosis form. Backticked identifiers. Closing clause states the control now in
force, matching Exemplars A, B and C. Names no evidence path (convention 8). The near-miss is
recorded rather than smoothed over — §F.3's own stated reason: "a rule without its near-miss is a
rule nobody believes."

### 3.1 Variant B — short form, inside the original 48–110 band

If the author prefers the list not to drift longer entry by entry:

```
14. *(13 Aug 2026)* A re-derivation keyed on column names its source CSV did not carry returned all zero and raised nothing — absent keys aggregate to an empty group, not to an error. The zero would have read as a clean result, which is precisely the false finding the check existed to exclude. A human eye on one CSV row caught it; no control did. **A broken aggregation and a true measurement produce an identical zero.** Zero and all-clean aggregates now assert their keys against the source, and a mismatch raises rather than prints.
```

89 words.

### 3.2 Variant C — if the author wants the incident's stakes named explicitly

Insert after "…no control did." in Variant A:

```
The correct return — non-zero in the same 18 cells — is the one the record publishes; what was missing was not the result but the control.
```

Takes Variant A to 146 words. **Recommended only if the ceremony wants the line to foreclose a
reader's inference that something published was wrong.** Nothing in the record is wrong; the
run's *correct* output was published. Variant A already implies this by saying the eye caught it.

**Recommendation: Variant A.** Diagnosis-form bold (every existing bold is a diagnosis, never an
instruction); the stakes clause is available as C if the ceremony wants it.

---

## 4. THE `DESIGN.md` COMPANION-EDIT CONSEQUENCE — the opposite of what S4 assumed

**S4 asks me to state that `DESIGN.md` l.546 "becomes `H-L1 through H-L13`, so the companion edit
changes again". It must not. Doing that would be a regression, not a companion edit.**

### 4.1 What actually happened to l.546

`DESIGN.md` l.546 no longer contains an enumerated range. `git diff` on the working tree:

```
-**Review lessons are recorded in `HISTORY.md`** (**H-L1** through **H-L11**). …
+**Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range; the list grows as lessons are appended, and this cross-reference does not enumerate the current tail so appending a lesson cannot desynchronize this document). …
```

That rewrite **is** the remedy H-L13 records. H-L13's own text says so: "The `DESIGN.md`
reference now names the series (`the H-L review-lesson series`, open range) rather than its
current tail, so appending a lesson cannot desynchronize a registered document."

### 4.2 The consequence, stated for the ceremony

> **Appending H-L14 requires NO edit to `DESIGN.md`.** The l.546 cross-reference is open-range by
> construction and stays correct at 13 lessons, at 14, and at any future count. **Any ceremony
> step that "bumps" l.546 to `H-L1 through H-L13` or `H-L1 through H-L14` REVERSES the Z2 fix and
> re-instates, in the same commit, the precise defect the lesson one line above it records.**
> `DESIGN.md` is hashed in the signed tag message; landing that reversal would hash a document
> that contradicts its own companion history file.

This is the stale-cross-reference risk S4 asked me to foreclose. It is real — but it points the
other way: **the danger is bumping l.546, not failing to bump it.**

### 4.3 `DESIGN.md` is still a second hashed file in this ceremony

For a different reason. `git diff --stat` this pass:

```
 DESIGN.md  | 30 +++++++++++++++---------------
 HISTORY.md | 33 +++++++++++++++++++++++++++++++++
```

`DESIGN.md`'s 30 changed lines are the **§2.11 prior-art table rewrite** (adding the
`leakage-buster` column) plus the l.546 open-range change. Both are already in the working tree.
Re-hashing `DESIGN.md` for the v30a tag remains required — H-L14 simply is not a reason for it.

### 4.4 Three ceremony-checklist lines are now stale and will mis-drive the ceremony

`evidence\fixture_spike\f5\v30a_ceremony_CHECKLIST.md` was written before H-L13 landed and before
l.546 was rewritten. **Flagging, not editing** — the checklist is a repo file and outside this
item's write permission.

| Checklist line | What it says | Why it is now wrong |
|---|---|---|
| **l.111** | "`DESIGN.md` … §9's cross-reference bumped **H-L1..H-L11 -> H-L1..H-L12** (line 546)" | The working tree does **not** read `H-L1..H-L12`. It reads the open-range series text. Also mis-scopes the `DESIGN.md` diff, which is 30 lines (§2.11 table), not the l.546 bump alone. |
| **l.241–244, step A5** | "verify, do not re-apply … `DESIGN.md` line 546 already reads '**H-L1** through **H-L12**'. Confirm with `git diff --stat` (expect `DESIGN.md \| 2 +-`, `HISTORY.md \| 1 +`)" | **The most dangerous line.** As written, A5's verification **fails** against the real file, and an operator obeying it would edit l.546 *back* to an enumerated range — the §4.2 regression. Its expected diffstat is wrong on both files (actual: `DESIGN.md \| 30`, `HISTORY.md \| 33`). |
| **l.110, l.211, l.238** | `HISTORY.md` in-scope changes listed as "**H-L12** + **H-34**" | Short by one already (H-L13 is in the tree), and short by two once H-L14 lands. Correct scope: **H-L12, H-L13, H-L14, H-34** — four additions to `HISTORY.md` in the one ceremony commit. |

Note l.388–392 of the checklist already describes the l.546 bump as "a third instance of the same
class … already fixed", and prescribes the *old* remedy ("bump the index in the same edit"). H-L13
supersedes that remedy for this case: the index was **removed**, not bumped. The checklist's
"standing remedy" paragraph (l.394–396) should be read as amended by H-L13.

---

## 5. Exact insertion point

| | |
|---|---|
| **File** | `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md` |
| **Insert** | as a **new line 220**, i.e. immediately **after** current line 219 and **before** the existing blank line 220 |
| **Anchor — text it follows** | end of l.219: `…is looked for in any future cross-reference whose target grows.` |
| **Anchor — text it precedes** | current l.220 (blank, verified `$` via `cat -A`), then l.221: `### H-30 — from \`PREREG.md\` §6.6` |
| **Net effect** | file grows **313 → 314** lines; l.220 onward shift down by one |
| **Renumbering** | **none.** Per convention 7 the number is an ID; the out-of-order block `…9, 11, 10, 8` stays exactly as it is. |

No other line in `HISTORY.md` changes. **No line in `DESIGN.md` changes on account of this
entry** (§4).

### 5.1 Exact-match edit specification (for the ceremony operator)

Append to the end of l.219, as a new line. The unique anchor string, verified to occur **once**
in `HISTORY.md`:

```
is looked for in any future cross-reference whose target grows.
```

Replacement = that string + `\n` + the Variant A line. The operator must **assert match count = 1**
before and after (H-L11's own lesson, l.215: "Every edit now asserts its match count").

### 5.2 Why this is staged rather than applied

`HISTORY.md` is hashed in the signed tag message (`e8cf5bbb…` for the v30 tag), so any edit
outside the amendment ceremony invalidates the v30 registration hash. The ceremony already opens
`HISTORY.md` for the H-34 ledger entry — **which is itself already in the working tree at l.265+,
a further drift from the checklist's "STILL TO BE WRITTEN AT CEREMONY TIME" at l.110.** This
lesson line rides the same open, in the lessons list rather than the `H-NN` ledger.

### 5.3 Separate flag — the repo's declaration copy does not carry §F.3

`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` is **3155
lines** and contains R17(iii) (l.2272) but **no §F.3**. The f4 scratchpad draft
(`…\scratchpad\fixture_spike\f4\availability_declaration_DRAFT.md`, §F.3 at l.3440–3486) is
ahead. **The normative form of this rule is in the f4 draft only.** If the ceremony commits the
repo copy as-is, `HISTORY.md` H-L14 will describe a control that the registered declaration does
not state. The declaration copy must be refreshed from the f4 draft before hashing.

---

## 6. Provenance and verification status

| Claim | Status | Source |
|---|---|---|
| Aggregation keyed on **wrong column names** returned **all zero** and **raised nothing** | **VERIFIED (quoted)** | f4 draft §F.3, l.3461–3463: "An aggregation keyed on **wrong column names** returned **all zero** and raised nothing, because absent keys aggregated to an empty group rather than to an error." |
| Caught by **visual inspection of a CSV row**, not by any control | **VERIFIED (quoted)** | f4 draft §F.3, l.3460: "that near-miss was caught by visual inspection of a CSV row — by a human eye on a line of data — and NOT by any control." |
| The all-zero would have read as "the trade-class restriction makes the corrected side clean" | **VERIFIED (quoted)** | f4 draft §F.3, l.3463–3465: "…it would have read as **'the trade-class restriction makes the corrected side clean'** — and that is **the exact false result R17(iii) exists to catch**". |
| The aggregation was the **trade-class re-derivation** over the four `trades_*` classes | **VERIFIED** | f4 draft §13(i) R17(iii), l.2338–2339, and the `restricted` definition at l.3019: "max strict over the four `trades_*` classes (`max_strict_trade_only`)". Source artifact: `y1\trade_class_only_map.csv` (96 rows). |
| The correct return is **non-zero in the same 18 cells** — nothing published is wrong | **VERIFIED** | f4 draft l.2338–2339 ("returns NON-ZERO in the same 18 cells") and l.3470–3472 ("The correct return … is the one §13(i) publishes; nothing in the record is wrong"). 18 of 48 instrument-months, corroborated at l.2265, l.2319–2320. |
| An all-zero return would have been a **FINDING, not a pass** | **VERIFIED (quoted)** | f4 draft l.2348 / §13(i), and the declaration's repo copy l.2282. |
| The rule's binding form: cross-check against source, **mismatch RAISES not prints** | **VERIFIED (quoted)** | f4 draft §F.3, l.3452–3454: "**On mismatch the check RAISES — it does not print a warning, does not annotate the output, and does not continue.** A warning next to a zero is read as a zero; an exception is not read as anything, which is the point." |
| Minimum sufficient check = **keys resolve** + **source non-empty on those keys** | **VERIFIED (quoted)** | f4 draft §F.3, l.3449–3452. |
| `HISTORY.md` l.219 is already `13.` | **VERIFIED** | `Read` of `HISTORY.md` l.198–229 this pass; `git diff` shows l.218–219 as working-tree additions. |
| `DESIGN.md` l.546 is open-range, not enumerated | **VERIFIED** | `grep -n "H-L" DESIGN.md` → single hit, open-range text; `git diff` shows the `-`/`+` pair. |
| Exactly one H-L range cross-reference exists repo-wide | **VERIFIED** | `grep -rn "H-L" --include=*.md .` → `DESIGN.md:546` only (plus `PRIOR_ART_VERIFICATION.md:3`, an ID citation, not a range). |
| Date `13 Aug 2026` | **SETTLED, not ambiguous** | H-L12 as landed (l.218) declares the convention in its own text: "Dated by the day recorded, not the day worked — the convention this list follows from here." Recorded today. |

### 6.1 Ceremony checklist additions proposed

- [ ] Insert the Variant A line as new l.220 of `HISTORY.md` (after l.219), match count asserted = 1.
- [ ] **DO NOT touch `DESIGN.md` l.546.** It is open-range and correct at any lesson count (§4.2).
- [ ] **Strike or rewrite checklist step A5 (l.241–244)** — as written it verifies against text that no longer exists and would drive an operator to reverse the Z2 fix (§4.4).
- [ ] **Correct checklist l.110/l.111/l.211** — `HISTORY.md` scope is **H-L12 + H-L13 + H-L14 + H-34** (H-34 already in the tree); `DESIGN.md` scope is the §2.11 table + the l.546 open-range change, diffstat `DESIGN.md | 30`, `HISTORY.md | 33` **before** this line lands.
- [ ] Record in the ceremony note that this is a **review lesson**, not a firing — firing count stays twenty-one, H-B addendum entry count twenty-three.
- [ ] **Refresh `AVAILABILITY_DECLARATION.md` from the f4 draft before hashing** — the repo copy lacks §F.3, the normative rule this lesson's practice clause refers to (§5.3).
- [ ] Re-hash `HISTORY.md` **and** `DESIGN.md` for the v30a tag message (`DESIGN.md` for §2.11 + l.546, not for this lesson).
