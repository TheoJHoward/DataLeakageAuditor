# §43 — DOES THE AMENDMENT EXIST? RESOLVED.

**ANSWER (§43.3): the v30a amendment lives IN `PREREG.md` AS AN APPLIED DIFF.**
`PREREG.md` gains the SCHEMA; the declaration keeps the DATA. **§43.4 applies.**

---

## THE FOUR TEXTS, SIDE BY SIDE, IN FULL

### (1) The two §0.1s — and §43.2 cites the wrong one

**`AVAILABILITY_DECLARATION.md` §0.1** (line 630) is *"Artifact A: the f2 REBUILD pair (what timing
is MEASURED ON)"*. **It says nothing about normativity.** It is the artifact split, not a source
rule. The §0.1 that blocker B1 invokes is `PREREG.md`'s:

> **### 0.1 What is locked here and what is not**
>
> "`DESIGN.md` holds architecture, method, and API and is revisable. The test:
> *If changing it would make a past result look better than it was, it is locked here. If changing
> it is just engineering, it goes in `DESIGN.md`.*"

**And the §0.1 in conflict with blocker 2 is neither of those — it is DELTA R66's §0.1**, a
standing constraint of the working session, not a clause of any registered document:

> "**0.1** `PREREG.md` is not edited. Not one byte. 478 is a PREREG line; the fix is a supersession
> marker in the declaration plus a walk extension, never an edit to the registered text. If any step
> below reads to you as 'edit PREREG.md,' you have misread it — stop and say so."

**Three different §0.1s were being treated as one.** That is the first half of the confusion and it
is worth naming before anything else.

### (2) R20 and R24 — the schema/instance ruling

**They are not in the repository.** `grep -rnE '\bR20\b|\bR24\b'` over every `.md` in the working
tree returns **zero hits**. They exist only in the amendment package under the scratchpad root, as
recorded author rulings.

**R24**, verbatim (`amendment/K1_SCHEMA_CLAUSES.md` l.11–18):

> "**What R24 means here, applied to every line below.** `PREREG.md` gains the SCHEMA: what kind of
> object each gate input is, what the declaration must supply, and what the gate does with it. The
> declaration keeps the DATA: the partition's cells, the map's rows, the per-instrument figures, the
> enumerations these rules yield. **The test applied to every drafted sentence: would this clause
> make sense in a registration that had never seen this fixture?** No clause below names a column, a
> count, an instrument, a boundary expression, a class name, or any figure. Where a clause needs a
> parameter, the clause says the declaration must supply it…"

**R20**, verbatim, in two places (`amendment/DECLARATION_SCRUB_LIST.md` l.52 and l.277):

> "If H1's diff only touches lines 445, 450, 451 and 461, then those rules — currently stated
> normatively in the declaration — will, after H1, be stated normatively *nowhere*, **because under
> R20 the declaration is not a normative annex.** **That is the single largest risk in this
> amendment and it is why this list is delivered before H1's diff is approved.**"
>
> "These are the rows H1's diff must be checked against **by name**. Each is a rule currently stated
> normatively in the declaration for which **no `PREREG.md` clause exists to carry it**. If H1's
> diff does not create the clause, **the rule has no normative home after R20.**"

**R20's form**, verbatim (`amendment/PREREG_v30a_DIFF.md` header):

> "**Form:** working resolution **R20**, form (ii') — a v30a amendments block near the top of
> `PREREG.md`; each amended clause carries an inline supersession marker naming v30a; **the new
> normative text lives inline in `PREREG.md`**, with the superseded text retained beside it marked
> superseded."

### (3) Blocker 2, in full

**§43.2 says "from `COMMIT_PLAN` §6 and §0". §6 is no longer where it lives** — I rewrote §6 at
R67/§14.1 as the closed six/seven ruling. Blocker 2 is in **§8, "What blocks this commit"**:

> `| 2 | `PREREG.md` v30a diff does not exist | AUTHOR | hard |`

Its substance is in `CEREMONY_COMMANDS.md` §0's secondary-blocker table, row **B1**:

> "**B1** | The amendment itself does not exist: `PREREG.md` is **clean** (sha256 `f0a8f001…`,
> byte-identical to its `prereg-v30` tagged state). The four §6.2 amendments and the §10.2 'waived'
> definition exist **only** in the declaration. §0.1 makes `PREREG.md` the sole normative source.
> **A tag over the current tree amends nothing.** | **NOT DONE**"

### (4) `PREREG.md:97`

> "**An amendment inherits §11's integrity chain in full:** signed tag, both file hashes in the tag
> message, external timestamp receipt committed, repository publicly reachable at lock. **An
> amendment weaker than the thing it amends is not one.**"

---

## THE ANSWER

**IN `PREREG.md`.** Every one of the four texts points the same way, and none of them supports the
alternative:

1. **R24 states it directly**: *"`PREREG.md` gains the SCHEMA… The declaration keeps the DATA."*
   Gaining a schema is an edit to `PREREG.md`.
2. **R20 forecloses the alternative**: the declaration *"is not a normative annex"*, so a rule
   stated only there has **no normative home**. R20 also fixes the FORM — *"the new normative text
   lives inline in `PREREG.md`"*.
3. **Blocker 2 is the same claim from the ceremony's side**: the amendments *"exist only in the
   declaration"*, therefore *"a tag over the current tree amends nothing."*
4. **`PREREG.md:97` supplies the consequence**: an amendment that changed nothing in the locked file
   would be *"weaker than the thing it amends"*, which line 97 says is not an amendment at all.

**The artifact exists and has existed since before this phase began.** `amendment/PREREG_v30a_DIFF.md`
opens: *"# PREREG.md v30a amendment — DRAFT DIFF, UNAPPLIED … This file is a diff for author
approval."* A scratch applied file exists at `applied/PREREG.md`, **1,417 lines against the repo's
1,099** — 326 insertions, 8 deletions, 25 hunks, adding **SC-1 … SC-13c** (54 `SC-` mentions in the
applied file, **0** in the repo).

## §43.4 — WHAT I GOT WRONG, PLAINLY

**DELTA R66 §0.1 is wrong, and it has been wrong since R66.** It is not a restatement of a settled
rule; it **contradicts R20 and R24**, which settled the question earlier and which sat in the
amendment package the whole time.

**And my part is the larger part.** The author wrote §0.1 once, in one delta. **I copied it into
`ROUND_STATE.md` as a STANDING CONSTRAINT and carried it forward through seven rounds** — R66 to
R72 — under a heading reading *"THESE OVERRIDE ANY INSTRUCTION THAT READS OTHERWISE."* I verified
`PREREG.md`'s byte-identity after every single pass and reported it as an invariant holding, when it
was the symptom. **I never once checked the standing-constraint list against R20 or R24**, which I
read past repeatedly while working in the same directory.

**This is exactly the audited class, and it is the cleanest instance of it yet.** My
standing-constraints list was an instrument. Its CLAIMED CLASS was *"the settled design of this
registration"*. Its ACTUAL DOMAIN was *"whatever the most recent delta said"*. Its GAP was every
ruling older than the current delta — including the two that settle what an amendment IS. It had no
boundary test, and like the other ten it failed in the direction that produces a PASS: every round
it let me report an invariant as green.

**It also converted a good rule into a bad one.** The real standing rule is the author's explicit
approval of the final diff before it is applied — older, and better, because it permits the
amendment to exist while still preventing an unapproved edit. R66 §0.1 replaced a *gate* with a
*prohibition*, and a prohibition on editing `PREREG.md` makes a class C amendment impossible by
construction.

## §43.4 — THE DIFF, AND WHY I AM NOT HANDING YOU THE ONE THAT EXISTS

**Not applied. `PREREG.md` remains byte-identical to `prereg-v30:PREREG.md`.**

**Both existing artifacts are STALE, and handing either over for approval would be the same defect
this phase has been auditing.** Measured, not assumed:

| artifact | dated | `SC-4(k)` occurrences |
|---|---|---|
| `applied/PREREG.md` | **19 Aug** | **0** |
| `amendment/PREREG_v30a_DIFF.md` | 24 Aug (content predates R49) | **0** |
| `amendment/SCHEMA_SET_FINAL.md` — **the source of record** | 24 Aug | **11** |

SC-4(k) was drafted at R49/R5, restructured across the R49 addenda, and extended at R60/F3-B5.
**Neither approval artifact contains any of it**, nor the R60 (k4) failure conditions, nor Q4's
three defects, nor anything from R61–R72.

**Producing the approval diff means regenerating it from `SCHEMA_SET_FINAL.md`** — which is exactly
R66 §2.1's *"regeneration of the composed doc and X5"*, the first item of §41.3. I have not done it
inside this halt because §47.1 says nothing else runs until §43 reports, and because a regeneration
is the substantive work of a round, not a paragraph.

**What regeneration requires, so the estimate is yours and not mine:** apply
`SCHEMA_SET_FINAL.md` PART 1 to a fresh scratch copy of the current `PREREG.md`; verify each hunk's
anchor match count; re-derive the composed `_E3_composed_sections.md`; rebuild `X5` with its
CHANGED-SINCE-READ section; run the 38-hunk bidirectional provenance check; then present the diff.
**It also must now carry the 478 supersession and I2/I3's §0 allocation correction**, because §45.2
made those one cut unit with §2.1.

---

## §43.6 — RECORDED AS THE CLASS IT IS

**Ten instances became eleven, and the eleventh is the one that governed the other ten.** The
standing-constraints list is the instrument that decides what work is permitted. Its domain was one
delta wide. For seven rounds it reported an invariant as green while the invariant was the defect,
and it took an author challenge — not any check I built — to expose it. **Not softened: I built
nine boundary tests for other people's instruments this phase and none for my own.**
