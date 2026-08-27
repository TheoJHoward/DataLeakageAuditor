# A23 — PROPOSED `PREREG.md` DIFF, FOR APPROVAL. **NOT APPLIED.**

**Nothing in this document has been applied.** `PREREG.md` is unchanged at
`0c8da19f237cd243…`. R137 §1.2: *"PRESENT A PREREG DIFF for the author's approval. Do not
apply it."* R137 §1.4: `PREREG.md` is edited only by applying a diff the author has explicitly
approved, and this delta does not authorise applying one.

**The wording is extracted, not retyped.** Every line below comes out of
`PREREG_v30a_DIFF.md`; §1.2 requires "wording unchanged from the drafted text where drafted
text exists", and reading the words from the source is the only way to guarantee that.

**Each anchor was LOCATED, not offset**, and matches exactly one line of `PREREG.md`. The
drafted diff names v30 line numbers; the applied file has moved 976 lines since, so the
recorded number is used only to cross-check what was found.

---

## H2 — §6.2 reference AUC anchor

**Anchor**, drafted against v30 l.445, located at applied **l.574**, match count **1**:

```
- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode.
```

**Replace with (4 lines), verbatim from `PREREG_v30a_DIFF.md` H2:**

```
- **Reference AUC anchor — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.1). **The anchor is constituted by recomputation, not by transcription.** It is computed from the acceptance fixture's own stored per-row prediction and outcome columns — committed bytes — and is declared in the fixture's availability declaration as an **enumerated set of entries**, one per declared horizon and side, each naming its model family, its row count, and the artifact and rows it was computed from. **Where the fixture is of the re-evaluation class** — the scored artifact carries stored per-row predictions rather than a training procedure — **the recomputation is authoritative over any figure recorded in a prior report**: it is a pure function of bytes already committed, so no rerun, reseeding, or environment change can move it. A lower-precision recorded figure that agrees is a secondary record and is reported as such; one that disagrees is a defect to be resolved before the gate runs, never a competing anchor. **The acceptance interval remains ±0.010 absolute, applied per entry, and may not be widened.** Because the anchor is a pure function of committed bytes, a deviation approaching the interval indicates a defect in the recomputation and is a **stop-and-report, not a pass**. **The gate runs in `full` mode** (carried unchanged from the superseded clause). **A report quoting an anchor entry names its model family and horizon**, and says so explicitly where the family differs from the one the original experiment documented.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675, **acceptance interval ±0.010 absolute**. The gate runs in `full` mode."
  >
  > *Retired because no horizon of the declared fixture reproduces the registered pair on both sides (§A.1 item 1) — that fact, and the replacement entries themselves, are instances and are recorded in the declaration. **The clause "and because the anchor's model family changed" stood here until R55/W5 and is struck: it is false against its own cited source, which names six architectures with LightGBM listed first, and §A.1 item 2 was corrected on 21 August 2026 to say so.** Recover the registered line byte-exact with `git show prereg-v30:PREREG.md`.*
```

---

## H3 — §6.2 contamination availability class

**Anchor**, drafted against v30 l.450, located at applied **l.579**, match count **1**:

```
- **Contamination availability class** recorded in the manifest.
```

**Replace with (4 lines), verbatim from `PREREG_v30a_DIFF.md` H3:**

```
- **Contamination availability class — v30a, operative** (supersedes the registered clause quoted immediately below; `AVAILABILITY_DECLARATION.md` §A.3). **The contamination availability class is recorded in the fixture's reconstructed availability declaration** — the declaration this section already requires — **and that file is hashed in the amended registration's tag message**, so the class is frozen at the tag and moving it afterwards is itself a class C amendment. **The recording locus may not be an evidence artifact.** A manifest is the product of a dated measurement round and records what was measured; writing a declaration into it makes a measurement record carry a decision, and an evidence artifact is never adjusted toward a decision. The class is recorded together with its mechanism, its measured incidence, and its per-column enumeration. **This clause moves the locus of one element and nothing else:** the ground-truth column DAG and the count of independently leaking sources remain manifest content and are satisfied there.
  > **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Contamination availability class** recorded in the manifest."
  >
  > *The obligation to record the class is not removed — only its locus moves, and it moves to a file the tag hashes, which binds harder than the manifest did.*
```

