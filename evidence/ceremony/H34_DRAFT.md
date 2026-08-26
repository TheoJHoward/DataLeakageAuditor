# H34_DRAFT — the amendment's `HISTORY.md` ledger entry

**ITEM PART D. DRAFT ONLY. NOT APPLIED.** `HISTORY.md` was read, never written. No state-changing
git command was run in this pass. Every fact below is a measurement taken this pass from the
working tree; nothing is carried forward from the previous revision of this file.

**Regenerated 2026-08-13 against the CURRENT state.** The previous revision of this file was
written before the §A.6.0 recovery and before C1–C5; it is superseded in full, not patched. What
is carried forward from it — the ID-collision finding, the format table, the reciprocal-pointer
count, the "what this entry must not do" list — is carried forward **re-verified**, and where the
re-verification changed the answer the new answer is stated.

Filename kept as `H34_DRAFT.md` because that is the path the orchestrator names and the path
`evidence/MANIFEST.sha256` line 79 records. **The entry inside it is numbered H-35, and §1 says
why.**

---

## 1. The ID the brief names is already taken — verified again this pass

The brief specifies the heading `### H-34 — from \`PREREG.md\` §0.2.1`, following working
resolution **R8** (`AVAILABILITY_DECLARATION.md` l.3665, verbatim):

> **R8. H-entry:** standard main-series form — `### H-34 — from PREREG.md §0.2.1` — with the
> entry text noting it is a class C amendment, the first post-tag entry. Addendum form rejected:
> H-nn is an open ledger and an amendment is a first-class event in it.

`HISTORY.md`'s `### H-34` heading (cited by heading, not line — `line 264` was read at an earlier pass and has since drifted), read this pass:

```
### H-34 — from `PREREG.md` §10.1 (kill-gate sign-off, prior art)
```

`grep -n '^### H-3' HISTORY.md` **re-derived R76** returns H-30 (l.229), H-31 (l.256), H-32 (l.261),
H-33 (l.267), **H-34 (l.272)**. *(These are a DATED SNAPSHOT and drift whenever lessons are
appended: they read 221/248/253/259/264 until R76, having moved 8-13 lines when H-L19, H-L20 and
H-L21 were filed. **The conclusion below does not depend on them** - it depends on H-34 being the
highest ledger ID, which is checked by anchor, not by line.)* The kill-gate sign-off took H-34 in the working-tree edit that
this same ceremony commit carries. **The highest ledger ID is H-34; the next free ID is H-35.**

**R8's form instruction is unchanged and is obeyed exactly** — main-series, `from \`PREREG.md\`
§0.2.1`, one italic parenthesized paragraph, noting class C and first-post-tag. **Only the number
moves.** The brief's `§0.2.1` suffix is kept; only `H-34` becomes `H-35`.

**Two ways to resolve, author's call:**

- **(a) Recommended — the amendment becomes H-35.** Nothing is renumbered. Matches the ledger's
  own habit: IDs are allocated in the order entries are written, and the review-lesson list next
  door is deliberately out of numeric order (`…9, 11, 10, 8, 12, 13`) precisely because the number
  is an ID, not a position. The draft in §3 is written for this.
- **(b) The sign-off is renumbered to H-35 and the amendment takes H-34.** Preserves R8's literal
  text and the brief's literal heading. **Costs more than it buys:** the sign-off's own text needs
  no change, but every reference to "H-34, the kill-gate sign-off" goes stale — including
  `evidence/ceremony/CEREMONY_COMMANDS.md`, `evidence/errata/HISTORY_lesson_line_S4_STAGED.md`
  §4.4, and this file — and renumbering a written ledger entry is the kind of retroactive edit
  this package exists to make visible rather than to perform. **The H-34-numbered heading is given
  verbatim in §3.2 if the author takes this path**; the paragraph text is identical either way.

Either way, **R8's ID is corrected in the ceremony record rather than silently reinterpreted.**

---

## 2. Format checked against the file's own main-series entries, re-measured this pass

Read this pass: H-01 (l.16), H-02 (l.21), H-03 (l.26), H-08 (l.51), H-30 (l.221/223),
H-31 (l.248/250), H-32 (l.253/255), H-33 (l.259/261), H-34 (l.264).

| Convention | Observed | Draft obeys |
|---|---|---|
| Heading | `### H-NN — from \`PREREG.md\`` or `` — from `DESIGN.md` ``, section suffix optional (H-01…H-29 carry none; H-30…H-33 carry `§6.6`, `§7.2`, `§4.6`, `§7.7`; H-34 carries a parenthetical gloss) | yes — `§0.2.1`, per R8 and the brief |
| Body | **exactly one paragraph, wrapped in `*(` … `)*`**. H-32 is the sole partial exception (italic opening sentence, then plain prose) | yes |
| Spacing | one blank line after the heading; **two** blank lines before the next `###` (verified by `cat -A` at ll.244–266; the H-32→H-33 gap is three, the H-31→H-32 and H-33→H-34 gaps are two) | yes — two |
| Tense / subject | past tense; subject is a **version** and what it said or locked (`v17 said…`, `v13 said…`, `v20's §0.2 named…`, `v23 gated on…`) | yes — subject is v30's §6.2 |
| Punctuation | em dashes for asides, never spaced hyphens; `§` bare; backticks for filenames, tags and identifiers; entry ends with a period **inside** the closing paren | yes |
| Numbers | quoted bare and exact, no rounding softeners (`six, two of them partial`; `eight of ten`) | yes |
| Length | measured this pass with `sed 's/[\`*]//g' \| wc -w`: **H-30 = 104, H-32 = 84, H-33 = 83, H-31 = 26.** H-08 is the shortest in the file at 14. **Longest = 104** | **§3.1 draft = 182; §3.3 short variant = 104.** See the length note |
| Register | records **what the specification got wrong and what that cost**, never what an implementer should do (l.3: "Nothing here instructs an implementer.") | yes |

**One deliberate departure, stated.** Every other main-series entry is an erratum against one
clause or one coupling. This one is an erratum against four §6.2 elements *plus* the record of the
amendment event itself — R8's "first post-tag entry" requirement — *plus* the four structural
things v30a lands alongside the four amendments. The draft carries all of it by opening on the
event, running the four defects as one enumeration, running the four landed structures as a
second, and closing on the disposition.

---

## 3. THE DRAFT

**Insertion point.** After the H-34 kill-gate block (which ends at the bare `---` rule on l.292)
and **before** `### H-B addendum — firings v18 through v30` (l.295). Two blank lines above, two
below, matching the observed spacing at ll.262–264 and ll.293–295.

### 3.1 Primary — the complete landed set

```markdown
### H-35 — from `PREREG.md` §0.2.1


*(The first entry written after a tag, and the one this section exists to make possible. v30's §6.2 locked an acceptance gate on four elements Phase 0's reconstruction then measured otherwise: the reference AUC pair 0.957/0.675 ± 0.010, reproduced at no horizon of the fixture it names — 5s misses post by 0.2565, 30s misses pre by 0.1006; the contamination availability class, with no manifest field to sit in; the sliced variant, due at a gate it does not serve; and criterion 3's silence on `fixture_corrected`, falsified by the M5 sweep at 18 of 48 instrument-months. v30a carries the §6.2 conformance walk resolving all four, the fixture re-based on the recomputed LightGBM trio, the declared map criterion 3 now scores on both sides, the criterion-1 partition re-derived from it by §A.6.0's stated rule — 11 required, 22 out of jurisdiction, 2 unscored, 35 — and the fed-column restriction read across the contaminated side as well as the corrected. Each is class C by this section's own list: the amended tag carries the semantics, `DEVIATIONS.md` D-001 the measurement, and `prereg-v30` does not move.)*
```

**182 words, measured — not estimated** (words counted after stripping backticks and asterisks,
the same rule used for the house figures in §2). One paragraph, one pair of
italic parens, period inside. **No "not in this ceremony" clause appears, and none may be added:**
every element the amendment lands is named in the same sentence as the rest.

Every number in it is traceable, and every trace was re-walked this pass:

| Figure | Source, verified this pass |
|---|---|
| `0.957` / `0.675` / `±0.010` | `PREREG.md` l.445, quoted verbatim at `AVAILABILITY_DECLARATION.md` §A.1 l.777 |
| `0.2565`, `0.1006` | `AVAILABILITY_DECLARATION.md` §A.1, "Why the old anchor cannot stand" item 1 (ll.797–800) |
| LightGBM trio | §A.1 table ll.786–790, from `f1\f1_results.csv` `recomputed_auc` |
| `18 of 48` | §A.8 l.1425, from `n1\summary_corrected.csv`; corroborated §13 l.1698, l.1845 |
| criterion 3 registered text | §A.8 l.1410, quoting `PREREG.md` l.461 |
| `11 / 22 / 2 / 35` | §D.1 item 2 (ll.3374–3387) and §A.6.4 partition check |
| §A.6.0 derivation rule | §A.6.0 l.1047–1056, present in the working-tree declaration this pass |
| two-sided map | §13 heading l.1946 and R9 (l.3671) |
| fed-column restriction, both sides | §13(i) (corrected) and §14 / §14.1 (contaminated, delta item S1, l.2935–2955 and l.3124) |
| "four amendments (445, 450, 451, 461)" | §A.11 walk summary (by anchor) |

### 3.2 The same paragraph under the H-34 heading, if the author takes resolution (b)

```markdown
### H-34 — from `PREREG.md` §0.2.1
```

Paragraph text unchanged from §3.1. **If this path is taken, the kill-gate block currently at
l.264 must be renumbered to H-35 in the same edit**, and the four references listed in §1(b) go
with it.

### 3.3 Short variant — 104 words, exactly the house maximum

The overrun in §3.1 is carried by two things: the two AUC deltas, which are the only place the
entry *shows* rather than asserts that the registered anchor fails; and the second enumeration,
which is what makes the entry describe the complete landed set. **Dropping the deltas and
compressing the second enumeration yields exactly H-30's length:**

```markdown
### H-35 — from `PREREG.md` §0.2.1


*(The first entry after a tag. v30's §6.2 locked an acceptance gate on four elements Phase 0's reconstruction measured otherwise: a reference AUC pair reproduced at no horizon of the fixture it names, a contamination availability class with no manifest field to sit in, a sliced variant due at a gate it does not serve, and criterion 3's silence on `fixture_corrected`, falsified at 18 of 48 instrument-months. v30a carries the conformance walk resolving all four, the re-based fixture, the two-sided declared map, the criterion-1 partition re-derived by §A.6.0's rule, and the fed-column restriction read symmetrically. `DEVIATIONS.md` D-001 carries the measurement; `prereg-v30` does not move.)*
```

**104 words, measured — exactly H-30's length.** It still names every landed element, but it names
them without showing any of them, and a reader who has not read the declaration learns only that
five things changed.

**Recommendation: §3.1, the 182-word version.** H-30 at 104 words is a four-clause enumeration
with a worked example inside it; the register tolerates length when the entry carries more than
one defect, and this one carries four defects and four landed structures. The house maximum is a
measurement of what has been needed so far, not a rule stated anywhere in the file.

### 3.4 Header variant, if the author prefers the faulted section over the amendment's

```markdown
### H-35 — from `PREREG.md` §6.2
```

R8 and the brief both say `§0.2.1`, and the draft follows them — §0.2.1 is the clause the *event*
belongs to, and the adjacent H-34 sets the precedent of naming the section a ledger entry
**discharges** rather than the section it **faults**. `§6.2` is defensible and would match
H-30…H-33, all of which name the faulted section. **Not recommended**, because it would leave the
ledger with no entry pointing at §0.2.1, the clause that licenses the whole ceremony.

### 3.5 §10.2 — the amendment reaches outside §6.2, and the entry may need to say so

Declaration §A.12 (l.1525) adds a definition of "waived" for §10.2's replacement-criterion floor,
and §D.1 item 5 (l.3399–3403) freezes it **alongside** the four §6.2 amendments. The §3.1 draft
does not name it: it says "four elements" of §6.2, which is exact, and the §10.2 definition is an
addition of a defining clause rather than an erratum against a locked rule.

**If the reviewed A2 diff to `PREREG.md` touches line 1035**, the entry should say so. Shortest
fix — append to the closing clause, before the final period:

> …and `prereg-v30` does not move. §10.2's "waived" is defined in the same diff, for the same
> reason: an undefined word inside a floor that exists to stop criteria being dropped silently.

Adds 26 words. **The decision follows the reviewed diff, not this file.**

---

## 4. The one element of the landed set that does NOT belong in this entry

**The §A.6.0 recovery incident.** §A.6.0 itself — the derivation rule that yields the three gate
classes — **is** in the entry (§3.1, "the stated rule of §A.6.0"), because it is landed amendment
content and the criterion-1 partition is not re-derivable without it.

**How it came to be recovered is not.** The incident is recorded in commit `ffa6d94`'s message and
in `evidence/fixture_spike/f4/DECLARATION_POINTER.md`: a restage copied a transient build copy over
the repository-root declaration while the root was ahead of it, destroying ~7.6 KB that existed
only in the root, and the content was recovered from a session transcript because the file was
untracked and git held no history. That is a **process** failure, and `HISTORY.md` l.3 scopes the
main series to what the *specification* got wrong. Its register is the **review-lesson list**
(`H-L`), exactly as H-L11, H-L12 and H-L13 are, and its rule is already recorded as working
resolution **R19** in the `ffa6d94` commit message:

> an authoritative file outside version control has no history, and recovery then depends on
> artefacts that were never intended as backups.

**Not drafted here** — this file drafts the main-series entry the brief asked for. If the author
wants R19 in the lessons list it is a fifth `HISTORY.md` addition in the same commit and takes ID
**H-L15** if the S4-staged H-L14 lands first, **H-L14** if it does not. Flagged, not written.

---

## 5. Companion edit this entry requires — the reciprocal pointer

The convention is an inline `*(→ \`HISTORY.md\` H-NN)*` marker in the section the entry faults or
discharges.

**Measured this pass** across `PREREG.md` and `DESIGN.md`: **26** such markers, for H-01, H-03,
H-04, H-05, H-06, H-07, H-08, H-09, H-10, H-11, H-12, H-13, H-19, H-20, H-21, H-22, H-23, H-24,
H-25, H-26, H-27, H-28, H-29, H-30, H-31, H-33. **Missing:** H-02, H-14, H-15, H-16, H-17, H-18,
H-32, **H-34**. *(An earlier checklist says "21 such markers exist today"; that count is stale.)*

So the pointer is the convention, not an invariant — eight entries have none. Two consequences:

1. **Adding `*(→ \`HISTORY.md\` H-35)*` to `PREREG.md` §0.2.1 is an edit to the locked file.** It
   cannot be a free ceremony edit; it must be inside the reviewed A2 diff. If A2 lands without it,
   the entry is reachable only by reading `HISTORY.md` — which eight existing entries already are.
2. **H-34 has no pointer either.** If the author is adding one for H-35, `§10.1` is the natural
   place to add one for H-34 in the same pass, and that is likewise a locked-file edit belonging
   in the same reviewed diff.

**Not drafted here.** Placing a marker inside §0.2.1 means choosing which sentence it hangs off,
and that sentence is in the locked file.

---

## 6. What this entry must NOT do

- **Not a firing.** The stopping rule (§0.2) did not fire; this is an amendment under §0.2.1. The
  H-B addendum's count stays at **twenty-one firings in thirteen listed entries / twenty-three
  entries counted**. The addendum already warns that entry-counting and firing-counting diverge;
  adding H-35 — and H-34, H-L12, H-L13, and any H-L14 — must not move either number. **State this
  explicitly in the ceremony record.**
- **Not a version-ledger bullet.** The version ledger (l.181) records what a numbered version got
  wrong, opening `- **vNN**`. v30a is an amendment tag, not a revision round, and no version is
  being retracted.
- **Not a review lesson.** The `H-L` list (l.207) is process/method lessons. H-L12 and H-L13 are
  already in the working tree and are separate additions in the same commit; H-L14 is staged at
  `evidence/errata/HISTORY_lesson_line_S4_STAGED.md` and is an author decision; R19 is §4 above.
- **No evidence paths in the line.** No main-series entry cites an evidence path. Provenance for
  H-35 stays in `DEVIATIONS.md` D-001, in `AVAILABILITY_DECLARATION.md`, and in the ceremony
  record. The trace table in §3.1 above is provenance **for the drafter**, and does not go into
  `HISTORY.md`.
- **No hash values.** Under R15 no hash may be carried forward; the entry states no hash. The one
  inline sha256 already in `HISTORY.md` — `b97a2804…` for `PRIOR_ART_VERIFICATION.md` at l.271 —
  belongs to H-34 and was **re-verified against the file this pass: it matches** (3,610 bytes,
  48 lines, tracked and clean at `ffa6d94`).
