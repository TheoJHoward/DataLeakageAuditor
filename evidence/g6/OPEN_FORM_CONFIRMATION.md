# OPEN-FORM CONFIRMATION — `DESIGN.md` line 546

**Item G6.** For the ceremony record.
**Date of check:** 14 Aug 2026.
**Verdict: CONFIRMED OPEN-FORM. The bump instruction is REFUSED. No file in the repository was edited by this item.**

Nothing in the registered corpus was written, staged, committed, or tagged for this item. Every
statement below is a read of the file as it stands in the working tree, quoted verbatim with line
numbers.

---

## 1. (a) The two texts, verbatim

### 1.1 `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\DESIGN.md`, line 546

Section context: `## 9. AI workflow and disclosure` (heading at l.530); l.546 is the closing line
of §9 and the last line of the file.

> **Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range; the list grows as lessons are appended, and this cross-reference does not enumerate the current tail so appending a lesson cannot desynchronize this document). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.

The line contains **no numeral and no range**. It names the series and states, inline, why it
declines to name a tail.

### 1.2 `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\HISTORY.md`, line 219 — the H-L13 entry

Section context: `## Review lessons (from \`DESIGN.md\` §9)` (heading at l.203); list runs
l.207–219; l.219 is the current last entry.

> 13. *(12 Aug 2026)* A cross-reference in `DESIGN.md` §9 named the review-lesson list as `H-L1 through H-L11`. Appending H-L12 left the range stale; appending H-L13 (this lesson) would have left it stale again. Two prior instances of the same shape — an obligation that names its target by enumerated index into a growing list — were recorded as Z2 in earlier review rounds and each was fixed by bumping the index in the same edit that changed the thing indexed. **Three instances is a structural defect, not bad luck: enumerated ranges in cross-references are fragile by construction, because the obligation to re-bump lives outside the edit that grows the target.** The `DESIGN.md` reference now names the series (`the H-L review-lesson series`, open range) rather than its current tail, so appending a lesson cannot desynchronize a registered document. The same shape — an index that must be re-bumped in a separate edit — is looked for in any future cross-reference whose target grows.

---

## 2. (b) The open-range wording IS the remedy H-L13 records

Confirmed by reading, on three independent grounds.

**Ground 1 — H-L13 names the remedy in its own words, and the file matches them.** H-L13's
penultimate sentence reads "The `DESIGN.md` reference **now** names the series (`the H-L
review-lesson series`, open range) rather than its current tail". `DESIGN.md` l.546 reads
"as the `H-L` review-lesson series** (open range". The lesson's description of the remedy and the
remedied line agree token for token on both the phrase and the parenthetical. H-L13 is not
proposing the open form as future work — it is written in the past tense **about the line as it
now stands**, and the line stands that way.

**Ground 2 — the working-tree diff shows the remedy being applied, and nothing else.**
`git diff -- DESIGN.md` (read-only) on the l.546 hunk:

```
-**Review lessons are recorded in `HISTORY.md`** (**H-L1** through **H-L11**). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
+**Review lessons are recorded in `HISTORY.md` as the `H-L` review-lesson series** (open range; the list grows as lessons are appended, and this cross-reference does not enumerate the current tail so appending a lesson cannot desynchronize this document). They are process history, not implementation guidance, and an implementer needs none of them to build the tool correctly.
```

The removed side is the exact string H-L13 quotes as the defect (`H-L1 through H-L11`). The added
side is the exact form H-L13 quotes as the fix. The defect and its remedy are the two sides of
one hunk.

**Ground 3 — the remedy generalizes, which is what makes it a lesson rather than a patch.**
H-L13's bolded claim is that enumerated ranges are "fragile **by construction**, because the
obligation to re-bump lives outside the edit that grows the target." The open form removes the
outside obligation entirely: it is correct at 11 lessons, at 12, at 13, at 14, and at any future
count, with no companion edit in any future append. An enumerated tail restores the outside
obligation and therefore restores the fragility. There is no version of the enumerated form that
satisfies H-L13.

### 2.1 Why bumping it would reverse the remedy *inside a document the signed tag hashes*

`DESIGN.md` is one of the files whose hash goes in the signed tag message. Setting l.546 to
`H-L1 through H-L13` — or to `H-L1 through H-L14` — would:

1. **Reverse the fix,** restoring verbatim the construction H-L13 quotes as the defect;
2. **Re-create the defect in the same commit that records it,** since the H-L13 entry sits in
   `HISTORY.md` in the same working tree and lands in the same ceremony commit;
3. **Hash a self-contradicting pair.** The signed tag would attest a `DESIGN.md` whose l.546 uses
   an enumerated range next to a `HISTORY.md` whose l.219 states that this document's reference
   "now names the series … rather than its current tail". One of the two hashed documents would
   be false about the other, permanently, under signature;
4. **Go stale immediately on the next append.** `H-L1 through H-L13` is already stale if H-L14
   lands in the same ceremony; `H-L1 through H-L14` goes stale at H-L15. The bump does not buy
   correctness, it buys one append's worth of delay.

Item (3) is the one that cannot be repaired later. A stale range in an unsigned file is an
erratum. A stale range in a file hashed by a signed registration tag is part of the registration.

---

## 3. (c) Repo-wide sweep — the open form is consistent everywhere in the registered corpus

Method: case-insensitive `H-L` sweep over the repository root
`C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01`, cross-referenced against `git ls-files`
to separate tracked (registered, hashed) files from untracked `evidence\` working files. 94 total
occurrences across 11 files.

### 3.1 Tracked corpus — three files carry the token, zero live enumerated ranges

| Tracked file | Lines with `H-L` | Form | Verdict |
|---|---|---|---|
| `DESIGN.md` | l.546 only | Open-range series reference, no numerals | **The remedy. Correct.** |
| `HISTORY.md` | l.219 only | Contains `H-L1 through H-L11` **inside H-L13's own body**, as a quotation of the defective prior form | **Correct and must not be changed.** This is the historical record of what the defect was. It is a quotation, not a cross-reference: it does not point at the current tail and cannot go stale. |
| `PRIOR_ART_VERIFICATION.md` | l.3 only | Cites a single stable ID, `H-L1`, by ID | **Correct.** A single-ID citation, not a range. Numbering in the lessons list is an ID, not a position — source order is `1,2,3,4,5,6,7,9,11,10,8,12,13` — so `H-L1` names the same entry regardless of how the list grows. Cannot desynchronize on append. |

Zero occurrences of `H-L` in **`PREREG.md`**, `DEVIATIONS.md`, `README.md`, `PARKING_LOT.md`,
`VALIDATED_CONFIG.toml`, `protocol/`, `tests/`, `tools/`, `.gitattributes`, `.gitignore`,
`registration-commit.txt`.

**Conclusion for (c): there is exactly one live H-L cross-reference in the whole registered
corpus — `DESIGN.md` l.546 — and it is open-form. Nothing else needs to agree with it, because
nothing else indexes the list.** The open form is consistent everywhere by construction.

### 3.2 Untracked `evidence\` working files — one live stale prescription, flagged not fixed

Enumerated forms appear in eight untracked working files. Not hashed by the signed tag, but
recorded here because one register of them is operative.

- **Register A — historical quotation and analysis of the old form.** `evidence\ceremony\COMMIT_PLAN.md` l.143; `evidence\errata\HISTORY_lesson_line_S4_STAGED.md` l.30, l.177; `evidence\errata\HISTORY_lesson_line_STAGED.md` l.65, l.119 (a superseded staging file that predates the fix). Harmless — these quote the defect in order to discuss it.
- **Register B — explicit prohibitions against re-instating the enumerated form.** `evidence\ceremony\COMMIT_PLAN.md` l.202–203; `evidence\errata\HISTORY_lesson_line_S4_STAGED.md` l.18, l.187–192. These agree with this confirmation.
- **Register C — STALE LIVE PRESCRIPTIONS, in one file: `evidence\fixture_spike\f5\v30a_ceremony_CHECKLIST.md`.** Written before H-L13 landed.
  - **l.111** describes the `DESIGN.md` scope as "§9's cross-reference bumped **H-L1..H-L11 -> H-L1..H-L12** (line 546)". False against the file.
  - **l.241–244, step A5** — the dangerous one — instructs the operator to "**verify, do not re-apply** … `DESIGN.md` line 546 already reads '**H-L1** through **H-L12**'." An operator running A5 finds the verification failing and is nudged to edit l.546 *back* to an enumerated range: the exact reversal §2.1 forbids. Its expected diffstat (`DESIGN.md | 2 +-`) is also wrong; the actual `DESIGN.md` change is larger.
  - **l.388–392 and the "Standing remedy adopted" paragraph at l.394–396** prescribe the *superseded* remedy — "bump the index in the same edit that changes the thing indexed" — which is precisely the practice H-L13 rules out as structurally fragile. Read as amended by H-L13.

**Not edited by this item.** The checklist is outside this item's write permission and outside its
scope. It is flagged for the author. Its Register-C content is already flagged independently at
`evidence\errata\HISTORY_lesson_line_S4_STAGED.md` l.212–225 and
`evidence\ceremony\COMMIT_PLAN.md` l.195–203; this confirmation concurs with both.

---

## 4. (d) The instruction issued, and the refusal

### 4.1 The instruction

An upstream ceremony brief (the S4 staging brief, quoted at
`evidence\errata\HISTORY_lesson_line_S4_STAGED.md` l.169) instructed that

> `DESIGN.md` line ~546's cross-reference **becomes "H-L1 through H-L13"**, so the companion edit
> changes again

— i.e. bump l.546 to an enumerated tail as a "companion edit" accompanying the appended lesson.
The item G6 brief restates the same instruction in both of its live variants: bump to
`H-L1 through H-L13`, or, once H-L14 lands, to `…H-L14`.

The instruction is not malicious and not careless. It is the *correct* instruction under the old
standing remedy — the one still written at `v30a_ceremony_CHECKLIST.md` l.394–396 — which said
that whenever an obligation changes, the same pass rewrites every index that quotes it. Under
that rule, appending a lesson obliges a bump. The instruction simply predates the rule change.

### 4.2 The refusal

**Refused. `DESIGN.md` line 546 is left exactly as it stands. No edit was made to `DESIGN.md`, to
`HISTORY.md`, to `PREREG.md`, or to any other tracked file by this item.**

Reasoning, in order of weight:

1. **The instruction is premised on a false statement about the file.** It presupposes l.546
   contains an enumerated tail to be bumped. It does not — it was rewritten to open form, and
   that rewrite is in the working tree (§2, Ground 2). A "companion edit" that changes an
   enumerated range cannot be applied to a line that has none; carrying it out would mean
   *writing an enumerated range in*, which is not a bump but a reversal.
2. **Executing it would reverse a remedy in a document the signed tag hashes**, producing a signed
   pair of documents that contradict each other about their own cross-reference discipline
   (§2.1). This is unrepairable after signature.
3. **It would re-create the exact defect recorded one line above it, in the same commit.** H-L13
   sits at `HISTORY.md` l.219 and lands in the same ceremony commit as the `DESIGN.md` change.
   The commit would append a lesson saying "enumerated ranges are fragile by construction" while
   simultaneously restoring an enumerated range.
4. **It buys nothing.** `H-L1 through H-L13` is already stale if H-L14 lands in this ceremony;
   `H-L1 through H-L14` is stale at H-L15. The open form is correct at every count.
5. **A brief is not authority to reverse a locked remedy.** Under the standing constraints of this
   run, `PREREG.md` may not be edited by any item, and no instruction reaching an agent through a
   working document authorizes reversing a fix that a registered file records as applied. The
   correct response to an instruction contradicted by the file is to report the contradiction,
   not to make the file match the instruction.

**What replaces the instruction:** nothing. **Appending H-L14 — or any future lesson — requires no
edit to `DESIGN.md` at all.** The companion edit the brief anticipated has been permanently
eliminated, which was the entire point of the H-L13 remedy. Ceremony steps that expect a
`DESIGN.md | 2 +-` diffstat from an l.546 bump should expect no l.546 change whatsoever.

---

## 5. The observation for the ceremony record: H-L13 caught by its own fix

This item is not merely consistent with H-L13. **It is an instance of the defect class H-L13
names, intercepted by the very remedy H-L13 records — and the interception is what the remedy was
built to do.**

The mechanism, stated plainly:

- H-L13's bolded finding is that an enumerated cross-reference is fragile **because the obligation
  to re-bump lives outside the edit that grows the target**. The obligation propagates through
  ceremony briefs, checklists, and hand-offs rather than through the file — so it survives after
  the file has moved on, and it arrives at whoever acts next as a confident instruction.
- That is exactly what happened here. The bump instruction travelled through the S4 brief and
  through `v30a_ceremony_CHECKLIST.md` step A5, both authored before the fix landed. Neither
  document is wrong about the rule it was written under; both are wrong about the file.
- Under the **old** remedy ("bump the index in the same edit"), this instruction would have been
  obeyed. There is no check in that regime that catches it — the whole point of H-L13 is that the
  re-bump obligation is unverifiable from inside the edit that triggers it.
- Under the **new** open-range form, the instruction is *self-defeating on contact with the file*.
  The bump has no target. An agent or operator opening l.546 to perform the companion edit finds
  a line with no range in it and must stop and ask why. That failure-to-apply is the detection
  event, and it is structural rather than vigilant: it does not depend on anyone remembering
  H-L13, only on their reading line 546 before editing it.

**So the fourth instance of the Z2 class was caught by the fix installed after the third.** The
class did not stop generating instances — H-L13 does not claim it would; stale instructions were
already in flight when the fix landed and at least one (`v30a_ceremony_CHECKLIST.md` step A5) is
still in the tree. What changed is that an instance now fails loudly instead of landing silently.

This also supplies a small confirmation of H-L5 — *the defect class migrates to wherever the
previous round's fix landed* (`HISTORY.md` l.211). It migrated exactly as predicted: out of
`DESIGN.md`, which is now immune, and into the **instructions about** `DESIGN.md`, which are not.
The residual exposure is Register C of §3.2, and it is a paperwork exposure in untracked working
files, not a defect in a registered document.

**Recorded for the ceremony. No file in the registered corpus was modified by item G6.**
