# I1 — THE §6.2 ALLOCATION TABLE

**DELTA R64/I1. Built before any §0 edit, from the criteria's own text.** Every row cites what the
criterion NAMES; the allocation follows from that, not from §0's description of it.

---

## The four criteria of §6.2

| # | registered text (`PREREG.md`) | what it NAMES | evaluated on | scored against |
|---|---|---|---|---|
| **1** | L459 — *"**Every** ground-truth leaking source **column** receives at least one **primary runtime finding**"* | a **column**, a **runtime finding** | **the declared feature pipeline**, per declared dataset (side × instrument-month) | the declared map's REQUIRED class for that column, SC-4(b) |
| **2** | L460 — *"No **manifest-clean** source **column** receives **any runtime finding of any tier**, on `fixture_contaminated`"* | a **column**, a **runtime finding**, a **side** | the declared feature pipeline, **contaminated side** | the manifest's clean set (4 columns) |
| **3** | L461 as amended — *"Runtime findings on every fixture side are scored against the fixture's DECLARED GROUND-TRUTH MAP"* | **runtime findings**, **sides**, the **map** | the declared feature pipeline, **both sides** | the map's three dispositions, SC-3(b) |
| **4** | L462 — *"Silent under the identity control on both."* | the **identity control**, both **sides** | the declared feature pipeline — the control's declared sentinel is `net_delta`, **a feature column** (§A.9, wrapped uint32 values ~4.29e9 present identically on both sides) | the declared sentinel enumeration, SC-5(f) |

**All four allocate cleanly to one side of the partition. No criterion is split, and none required
forcing.** I1's stop condition is not triggered.

## What IS a statement about Artifact B

These are elements of §6.2 and its neighbours, and **none of them is one of the four criteria**:

| element | object |
|---|---|
| the reference AUC anchor (L445 → SC-2(d)) | **Artifact B** — its stored per-row predictions |
| fixture identity and the RE-EVALUATE class (§8) | **Artifact B** |
| the shared-label-vector licence (§9) | **Artifact B** |
| the k-of-N proof count | **Artifact B** |

---

## THE FINDING: §0.2 is not merely overbroad. It is BACKWARDS for the four criteria.

`side` is a **label on a dataset**, not a name for an artifact — **both** artifacts have a
contaminated and a corrected side. So `fixture_contaminated` in criterion 2 does not select
Artifact B; it selects a side, and the artifact is fixed by what the criterion needs to read.

Every one of the four criteria needs to read **a source column** and decide whether it **received a
runtime finding**. §0.2 states, of Artifact B: *"Artifact B stores **no feature columns**… **No
event-to-row timing question can be answered from Artifact B at all.**"*

**A criterion about columns receiving findings cannot be a statement about an artifact with no
columns.** So:

- §0.2's *"Criteria 1-4 … are all statements about Artifact B"* is **false for all four**.
- §0.1's *"Nothing in §6.2's four criteria is evaluated on it [A]"* is **false for all four** — A is
  the only object in the spike that has features and their event joins, which §0.1 itself says:
  *"it is the only one that contains features and their event joins."*

**The two sentences are exactly inverted with respect to criteria 1–4**, and each contradicts a
fact stated in its own section three paragraphs away. R42(iii) is confirmed and is stronger than
"overbroad".

## Why this went unseen

Both sentences were written when criterion 3 read *"no runtime finding appears on
`fixture_corrected`"* — a pure silence test, answerable from any artifact that can be observed to
produce nothing. **R9 replaced silence with map-scoring, which made the criterion require a column
and a cell.** The §0 allocation was never re-derived. The map lagged Y1 the same way, and §0 lagged
R9; both surfaced as composition findings months later.

## What still needs registering, and is not fixed by correcting §0

`feature pipeline` occurs **once** in the declaration (§E:3663, the grant) and **zero** times in
`PREREG.md`. Correcting §0's allocation does not give the object a registered definition — R42(i)
does, and it must land in the same pass, or the criteria allocate to something the registration
does not define.
