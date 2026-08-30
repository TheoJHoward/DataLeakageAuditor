# K2 — THE ARTIFACT-B ALLOCATION QUESTION. **NOT MOOTED BY v30a.**

**28 August 2026. Read-only determination. Nothing is acted on** — R154 §4: *"if it is NOT mooted,
record what it still requires and where it queues — do not act on it."*

---

## THE QUESTION

`I1_ALLOCATION_TABLE.md` (R64) found the availability declaration's §0 allocation sentences **exactly
inverted** with respect to §6.2's criteria 1–4:

| section | the sentence | I1's verdict |
|---|---|---|
| **§0.2** (Artifact B) | *"Criteria 1-4 … are all statements about Artifact B"* | **false for all four** |
| **§0.1** (Artifact A) | *"Nothing in §6.2's four criteria is evaluated on it"* | **false for all four** |

**Why the inversion happened, in I1's own words:** both sentences were written when criterion 3 read
*"no runtime finding appears on `fixture_corrected`"* — a pure silence test, answerable from any
artifact that can be observed to produce nothing. **R9 replaced silence with map-scoring, which made
the criterion require a column and a cell.** §0's allocation was never re-derived.

**And I1's own reasoning is structural, not stylistic:** *"A criterion about columns receiving
findings cannot be a statement about an artifact with no columns."* The declaration says so itself,
three paragraphs later — **"Artifact B stores no feature columns"** — which is why ground truth is
measured on A and applied to B through the R3 + §B.2 bridge.

## THE DETERMINATION: **NOT MOOTED.** Three checks, all derived from the attested files.

| check | result |
|---|---|
| §0.2's *"…are all statements about Artifact B"* in the v30a declaration | **PRESENT — 1 occurrence** |
| §0.1's *"Nothing in §6.2's four criteria is evaluated on it"* | **PRESENT — 1 occurrence** |
| `feature pipeline` defined in `PREREG.md` at v30a | **ABSENT — 0 occurrences** |

**Both inverted sentences survive verbatim in the declaration the `prereg-v30a` tag attests**
(`79357d77…`). v30a **did** amend §6.2 line 461 — criterion 3, the very clause whose R9 change caused
the inversion — but **amending the criterion is not re-deriving the allocation**, and the allocation
was not re-derived.

**I1's second condition is also unmet.** It stated that correcting §0 alone would not suffice:
*"`feature pipeline` occurs once in the declaration and zero times in `PREREG.md`. Correcting §0's
allocation does not give the object a registered definition — R42(i) does, and it must land in the
same pass, or the criteria allocate to something the registration does not define."* **At v30a
`PREREG.md` still contains it zero times.**

*(Method note: the first two checks were run line-scoped and returned a false negative on §0.1 —
the sentence wraps across a line break, and it uses a straight apostrophe where the quoted form has
a curly one. Re-run against flattened text, both are present. **Prose wraps; a line is not a unit of
meaning** — the same defect A34's sweep caught, met again here.)*

## WHAT IT STILL REQUIRES

1. **Re-derive §0.1's and §0.2's allocation sentences** against criterion 3 **as amended**, so each
   states which artifact its criteria are evaluated on. The declaration is one of the twenty hashed
   paths, so this cannot happen while the registration is frozen.
2. **A registered definition of `feature pipeline` in `PREREG.md`** (R42(i)). `PREREG.md` is
   **CLOSED**; every instrument is spent, applied, or refused. **This would require a further class C
   amendment beyond v30a** — it is not something v30a left half-done, it is something v30a did not
   reach.

## WHERE IT QUEUES

**Post-tag, and it does not fit in the current post-tag queue as written.** Item 1 edits a hashed
file and item 2 needs a **new amendment cycle** — a separate registration act with its own approval,
diff, and tag, not a Phase 1 task.

**It does not block the v30a tag.** §6.2's acceptance scores criteria whose registered text is
unambiguous; the defect is in the *declaration's description* of which artifact each criterion is
evaluated on, and in a term the registration uses without defining. **Both are disclosure-class
items** — they join the HELD set for `DEVIATIONS.md` at A15 rather than reopening a closed surface.

**Recorded, not acted on.**
