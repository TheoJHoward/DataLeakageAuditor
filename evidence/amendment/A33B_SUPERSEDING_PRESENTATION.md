# A33b — THE SIXTEEN LINES THAT WERE APPLIED BUT NEVER PRESENTED

**27 August 2026. Supersedes `A32_PROPOSED_DIFF.md` as a presentation of hunks 1–3 — it does not replace it as a record.** That document is the frozen account of what was read on the day it was approved and **is not touched**; rewriting it would destroy the only evidence of what was actually approved, which is the very gap this document exists to close.

**Nothing here is applied.** `PREREG.md` already carries this text, at `e7b0e5aec2c4523e…`, 2228 lines. **On approval the applied state stands as approved and nothing is re-applied.** Refused, the sixteen lines come back out.

---

## What went wrong

`BLOCK_MANIFEST.md`'s declared ranges **end eight lines before each blockquote actually ends**. A32 extracted inside them, so the presentation carried §AB and §AC each eight lines short. The ranges are the **right length** and **start eight lines early** — they cover each block's apparatus plus all but its last eight lines, which is why nothing looked obviously wrong.

| block | presented | applied | declared range | true extent | difference |
|---|---|---|---|---|---|
| §AB | 40 lines | **48 lines** | ll.1632–1679 | **ll.1640–1687** | **+8 appended** |
| §AC | 43 lines | **51 lines** | ll.1687–1737 | **ll.1695–1745** | **+8 appended** |
| SC-12(w)'s limb | 37 lines | **37 lines** | ll.1145–1181 | **ll.1145–1181** | identical |

**SC-12(w)'s limb is identical** because A32 happened to use ll.1145–1181 for it rather than `BLOCK_MANIFEST.md`'s own entry 23, which declares ll.1137–1173 and is **also eight early**. The limb was applied correctly by luck, not by check.

## The claim, proved mechanically rather than asserted

> **The applied text is the presented text plus exactly 16 lines, appended at the end of two blocks. No presented line was removed, reordered or altered.**

`a33b_divergence.py` establishes this by **prefix equality, line by line** — deliberately not by substring containment, which would also pass if a line had been inserted in the *middle* of a block. That is a different and worse fact, so the test is written to be able to fail on it. This generator re-runs the same comparison and **halts rather than emitting** if it does not hold.

---

## The 16 lines, in full

**Read out of `SCHEMA_SET_FINAL.md` at `32358f6dfc7f96d2…` — the approved hash, verified before a line was read.** Not retyped: a presentation that spells its own subject can misspell it.

### §AB — SSF ll.1680–1687, 8 lines

```
> what a published number means, which is §0.2.1's class C on its face (line 93) — which must give
> the state a single canonical disposition and make one of the two lines cite the other. Until that
> amendment is tagged, no reading, working resolution, or `DEVIATIONS.md` entry may resolve the
> conflict (§0.2.1 line 95; SC-9(c), SC-9(e); SC-12 item (5); corroborated by the declaration's §D.3
> and §A.12 item 5). **The operative conflict is registered-text-internal — line 816 against line
> 830.** It is not a conflict between line 816 and the declaration: declaration text on the same
> state is provisional until the tag, is at most corroboration, and cannot settle a disagreement
> between two registered lines.
```

### §AC — SSF ll.1738–1745, 8 lines

```
> *absence is a miss* becomes *a finding fails the gate*. **A reader comparing v30 and v30a
> byte-for-byte at line 459 will see no change and conclude wrongly.** The narrowing is made under the
> class C rule, which permits it; §0.2.1 line 97 measures at the outcome, and at the outcome this is a
> supersession.
>
> **These seven are disclosed because the record should not have to be reverse-engineered to find
> them.** Each is verifiable from artifacts this registration commits, except where disclosure 5 says
> otherwise.
```

## Why these lines are not a formality

**§AB's eight carry the block's central holding.** Without them §AB records the conflict and never says where it lies:

> **The operative conflict is registered-text-internal — line 816 against line 830.**

**§AC's eight carry disclosure 7's conclusion and the block's closing paragraph.** Without them the block ends mid-sentence inside item 7, and the sentence that says why the disclosures exist is absent:

> **These seven are disclosed because the record should not have to be reverse-engineered to find them.**

---

## What was verified

| | |
|---|---|
| SSF at the approved hash **before extraction** | `32358f6dfc7f96d2…` — extraction from unapproved bytes is not extraction from approved content |
| extents derived from **the blockquotes' own delimiters** | a declared range is an assertion; the block's extent is a fact about the file |
| `A32_PROPOSED_DIFF.md` **committed and unmodified** | the approved bytes are the committed ones; a presentation edited after approval is not what was approved |
| applied text = presented text **+ suffix only** | prefix equality line by line, not substring containment |
| **no other applied block is truncated** | `a33d_block_completeness.py`: 41 manifest rows, **0 truncated**, 24 complete — including SC-13a (59 lines), SC-13b (68) and SC-13c (101), whose declared ranges are also eight early |

**The offset is wider than two blocks.** `a33c_manifest_offset.py` finds **seven** decidable §A rows eight lines early — 23, 24, 26, 28, 31, 33, 36 — against twenty-one correct. Rows 34 and 35, annotated *“moved here R53/Y1”*, are correct because they were re-derived after the shift. **Only §AB and §AC were ever extracted inside a stale range**; the completeness sweep above is what establishes that, rather than assumption.

---

## What approval means

**Approve** — the applied state stands as approved. Nothing is re-applied, no file changes, and A34 unblocks.

**Refuse** — the 16 lines are removed from `PREREG.md`, returning §AB and §AC to the extents that were presented. The blocks then end mid-sentence, which is why this document recommends nothing and simply shows what is at stake.
