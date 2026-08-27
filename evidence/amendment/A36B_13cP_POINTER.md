# A36b — §13c-P, THE LINE-816 POINTER. **NOT APPLIED.** ⛔ HALTS FOR YOUR READ.

## ⚠️ THE CONSEQUENCE, FIRST — there are two, and neither is a reason to refuse on its own

**1. The pointer cites a container that was ruled never to land.** Its closing sentence reads:

> …is recorded in the v30a **amendments block** and is not changed by the exception.

**§8.2 — the amendments block — never lands** (unapproved content; its item 1 is false). The phrase is the same one A34 removed from all four operative sites at `f1d66bf`. **Applying this text verbatim puts that citation back into registered prose**, one commit after it was taken out.

**2. Applying it while the drafting apparatus stays would put the same paragraph in the file twice.** The fenced specimen at l.1344 is **byte-identical** to the text being applied. Landing the paragraph without removing the `INSERT AFTER` apparatus leaves an operative copy and a fenced copy — and any future citation anchored on that text would then resolve to two lines, which is the failure A34 spent a whole correction class avoiding.

### The choices. **None is taken here.**

| | what it costs |
|---|---|
| **apply verbatim, disclose the citation** | faithful to approved content; **registered prose then cites a container that does not exist**, and that needs its own A34-class correction later |
| **apply with the citation corrected** to A34's form — *“the v30a recorded-defect block in §7.2.1”* | leaves the file self-consistent; **but it is no longer verbatim extraction from approved content**, so it needs its own approval, exactly as the sixteen lines did |
| **do not apply** | nothing false is added; **§AB's assertion at l.1374 stays false** and joins HELD, disclosed at A15 |

**Whether the apparatus is removed is a second, separable question** — it is drafting scaffolding, not registered prose, but removing it is a deletion and is not proposed here.

---

## The text, in full

**Extracted verbatim from SSF ll.1612–1616** — the fence under §13c-P's `INSERT AFTER` apparatus, heading at SSF l.1600.

```
**The suppression clause above is subject to one express, scoped exception, stated in §10.2 (v30a) [SC-13c(c2)].** That clause states which quantities the exception reaches and what is published for them; it governs the exception wherever this sentence is applied and is not restated here. Everywhere outside it, this sentence governs exactly as registered. The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state is recorded in the v30a amendments block and is not changed by the exception.
```

**Extent derived from the fence's own delimiters, never from a declared range.** `BLOCK_MANIFEST.md` row 32 declares ll.1604–1608 — **+8, eight lines early**. Extracting inside the declared range would have returned **nothing at all**. *(A39 left row 32 uncorrected: it has no length-preserving candidate, and a number the instrument cannot derive is one it must not write.)*

## Where it would go, and what sits there now

**The insertion anchor is `PREREG.md` l.1336 — the registered line-816 suppression clause — and it occurs exactly once**, asserted before anything else was read.

```
l.1335  **A combination that is `not_applicable` on every scope-eligible case in a body of data publishes its counts and suppresses its yields, rates, and gates**, naming the reason.
l.1336  **A combination that is `not_applicable` on every scope-eligible case in a body of dat   <-- THE ANCHOR
l.1337  (blank)
l.1338  <!-- v30a SC-13c-2 — INSERT_AFTER -->
l.1339  (blank)
l.1340  **INSERT AFTER (one paragraph, blank line each side):**
l.1341  (blank)
l.1342  ```
l.1343  (blank)
```

**Structure, checked before any write plan.** The anchor is a **top-level paragraph**, not inside a blockquote, list or table; the line above it is blank and the line below it is blank, so a paragraph inserted with a blank line each side **cannot merge into either neighbour** and cannot turn a following `---` into a setext heading. **The apparatus below it (ll.1340–1346) is a fenced block**, and inserting above the fence leaves the fence balanced — both still parse as what they were.

## What applying it would make true

**`PREREG.md` l.1374, inside §AB, currently asserts:**

> …a pointer to the exception is inserted at line 816's own site.

**That is false today** — §13c-P is the only one of 23 v30a markers still carrying unapplied `INSERT` apparatus, and the pointer exists solely as the fenced specimen. **Applying the paragraph makes §AB's sentence true**; refusing leaves it false and disclosable. Either way it is verified by reading after the fact, not assumed.

---

## What was verified

| | |
|---|---|
| SSF byte-equal to the approved hash **before extraction** | `32358f6dfc7f96d2…` |
| extent from **the fence's own delimiters** | ll.1612–1616; the declared range is **+8** and is used only as a cross-check |
| the paragraph is **exactly one line** | asserted, not assumed |
| the insertion anchor is **unique** | `PREREG.md` l.1336, match count 1 |
| **markdown structure** above and below the anchor | blank / blank; fenced apparatus below stays balanced |
| **byte-identical copy already in the file** | l.1344 — so applying changes no wording, only status |
| it **cites the non-existent container** | `True` |

**Nothing is applied. `PREREG.md` is unchanged at `fcacebb231438e31…`, 2228 lines.**
