# v30a APPROVAL PACKAGE

**APPLIED — 25 August 2026.** `PREREG.md` is now blob **`a90896785da528c8`**, sha256
`0c8da19f237cd243…`, **2,075 lines**. It is **EXPECTED TO DIFFER** from `prereg-v30:PREREG.md`
(blob `75bd93dec436`, 1,099 lines), and that inequality is the amendment. **§50.3 fires here:**
until application the byte-identity check meant *"the approved diff has not yet been applied"*;
from application it is an **expected inequality against the stated new blob**, and equality
would now mean the application was lost. `git show prereg-v30:PREREG.md` recovers the
registered v30 text byte-exact.

## FOR THE AUTHOR — WHAT THIS READ IS FOR (F3)

**You are not checking whether the diff is correct.** That is covered, and here is what covers it,
with results: the registration gate (**20 checks, PASS**); records-to-source and source-to-records
(**23/23** and **15/15**); anchors resolving exactly once (**23/23, zero halts**); anchors copied from
their own INSERTION POINT (**10/10**); independent extraction on two unlinked paths (**23/23**);
generated twice **byte-identical**; untraceable inserted lines **0 of 845**; and two boundary tests —
corrupting a declared range **halted the generator on the digest**, repointing an anchor **changed the
diff and was caught by the copied-anchor check**. Re-deriving any of that is not your job.

**Three things are yours, because no instrument can do them:**

1. **Does each hunk's "what it does" match the decision you made?** Read the §53.1 table's last two
   columns **from memory of the ruling**, not from the diff. An instrument can prove the text came
   from the source of record; **only you can say the source of record says what you decided.**
2. **Is the untraceable-lines list empty?** It is stated as **0**. Confirm the claim exists and reads
   as zero — a number you accept without seeing is a number nobody checked.
3. **Look for what should not be there.** Text you do not recognise, phrasing you would not have
   used, a decision you do not remember making. **This is the only check in the whole apparatus
   pointed at content nobody authored deliberately**, and it is the one that finds it.

**THE EXPECTED OUTPUT OF THIS READ IS QUESTIONS.** There are **23 insertion points across 15 hunks
and 15 clauses**. **Zero questions across 23 insertion points means the read did not happen** — not
that the package is clean. Two or three questions is the normal result of a real read, and a question
that turns out to be nothing is still the read working.

**The §10.1 line 1022 defect that was open at R83 is CLOSED** — ruled Option A at §108, two
records authored, regenerated, all six checks re-run. It is recorded below as a superseded pair, not
as an open question.

---

## §53.4 — THE FIXED PAIR

The approval is over **this diff derived from this source**, and neither alone:

## 🗄 HISTORICAL — R81/C2's HALT. **RESOLVED AT R87. APPLIED AT R93. NOT AN INSTRUCTION.**

> **Read this as a record, not as a direction.** It said DO NOT APPLY of the **R80** pair, and that
> pair was never applied — it is marked superseded below. The pair that WAS applied on 25 August 2026
> is the **R87** pair, which carries the fix this block called for. **Retained rather than deleted**
> (§140.2's rule, applied here): the finding is part of the record, and a reader who meets only the
> resolution cannot tell what was nearly signed. Its substance is repeated in the R80 superseded
> block, which is where a reader looking for *why* that pair died should land.

### The finding as it stood at R81

**Two blocks of PART 1 operative text reach no record and therefore no hunk.** Found by the
block-reachability check (`block_reachability_check.py`), run this round as an ADDITION to C2's
specified question, not a substitution for it (A2.3) — C2 as specified returned 16 of 16 clean while
this was true, because C2 is keyed on `**INSERTION POINT.**` fields and neither block has one.

| block | ssf | what it declares itself to be | records covering it | in the diff |
|---|---|---|---|---|
| `§10.1-C2op` | l.1760 | “THE C2 OPERATIVE ITEM (**replaces `PREREG.md` line 1022**)” | **none** | **no** |
| `§10.1-C2ret` | l.1766 | “THE C2 RETENTION BLOCK (inserted beneath the operative item)” | **none** | **no** |

`SCHEMA_RECORDS.json` carries no record with `prereg_line` 1022. The nearest hunks are `@@ -1027,12`
and `@@ -1052,6`; **no hunk covers line 1022.** Verified by span arithmetic, not by substring search.

**WHY THIS MAKES THE SIGNED OBJECT FALSE (§71.3 admits it on exactly this ground).** SC-3 replaces
§6.2 criterion 3 at line 461 so that on the corrected side the tool must **match the declared
ground-truth map**. §10.1 line 1022 — the **Phase 0 kill gate's** criterion 3 — still reads *“Fires on
`fixture_contaminated` and is **silent on `fixture_corrected`**”*. Applying the current diff yields a
`PREREG.md` in which the fixture gate requires findings on the corrected side and the kill gate
requires silence on it. Two registered texts contradicting each other, in the clause that decides
whether the project proceeds — the same failure SC-12p was created to prevent, in a heavier place.

**The source of record already says so, twice, in text that IS applied:** SC-3's supersession block
(ssf l.299) reads *“Consequential — §10.1 line 1022 (H1 C2): the kill gate carries a second copy of
the retired…”*, and SC-13a's (ssf l.1276) reads *“Consequential — §10.1 criterion 3, line 1022.”*
The consequential supersession is declared; the record set does not execute it.

**And the source of record predicted this exact failure.** The section header at ssf l.1748 records
why the pair was moved into `SCHEMA_SET_FINAL.md` at R53/Y1: until the move `_X5_hunks_v2.json` was
their only source, which left *“the amendment's most-revised normative text as the only applied text
no provenance check could reach.”* The move put the text where checks could reach it. **No check
reached it** — because every check in the ledger reasons forward from the record set, and a block the
record set never claimed has nothing to reason from.

**WHY THE EXISTING LEDGER PASSED.** Each check's PASS is a true statement about its own domain
(H-L21), and line 1022 is outside all of them:

- **§53.2** asks whether every line **in the diff** traces to a declared range. Text that is missing
  from the diff is not there to fail the test.
- **§53.3** asks whether every **clause** is represented. All 15 are. `§10.1-C2op` is not a clause; it
  is a replacement item in PART 1's annex region.
- **§82** compares two independent paths to **the same record's** text. A block with no record has no
  second path, so there is nothing to compare and nothing to mismatch.
- **§77.1 / §57.3** verify anchors and both directions **of the record set**. Same blind spot.

**THE REMEDY IS THE AUTHOR'S, NOT MINE.** It requires two new records (a `REPLACE_LINE` at
`prereg_line` 1022 carrying `§10.1-C2op`, and an `INSERT_AFTER` carrying `§10.1-C2ret` beneath it, in
the order ssf l.1758 fixes: *“the REPLACE lands first; the retention blockquote is then written
directly beneath the resulting operative item 3, before item 4”*), and regeneration — which produces a
**new diff hash and a new approval pair**. Nothing has been changed. `PREREG.md` remains blob
`75bd93dec436`.

---

### CURRENT PAIR — R87

| artifact | sha256 |
|---|---|
| `PREREG_v30a_APPROVAL.diff` | `c5d89db16f2c1fed0c500b5729bfcd751036705230f1098376bcf272f680b0c9` |
| `SCHEMA_SET_FINAL.md` (source of record) | `32358f6dfc7f96d2ac1e97cea9b6743dde674c78ac05cc114cc42e41ca33f2dc` |
| `PREREG.md` (base) | blob `75bd93dec436…`, 1,099 lines |

### ⛔ SUPERSEDED PAIR — R80. **DO NOT APPLY.** (§89.2)

| artifact | sha256 | why superseded |
|---|---|---|
| ~~`PREREG_v30a_APPROVAL.diff`~~ | ~~`335c81f00d4e3fde8a3013684aa2c866b09ae89c78340b05eafd684cd12950b5`~~ | **missing the §10.1 kill-gate criterion 3 pair** at `PREREG.md` line 1022 |
| ~~`SCHEMA_SET_FINAL.md`~~ | ~~`c8d9c22a4cd08107ab8dd4a9a908efea19c03208a8409ba853d7563f53e7d5b1`~~ | **superseded at §108.4 only** — the text was never at fault; the ruling and its reason were added to the §10.1 section, which moved the hash. |

**The source of record did not move, and that is the point.** R80's diff was complete against its
record set and incomplete against its own source: `§10.1-C2op` and `§10.1-C2ret` sat in
`SCHEMA_SET_FINAL.md` reachable by no record, so `PREREG.md` line 1022 got no hunk. Ruled **Option A**
at R87/§108 — the amendment CARRIES the pair. Two records were authored, the diff regenerated, and the DIFF hash moved. **SSF moved too, but only at §108.4** — recording the ruling
at the §10.1 section is prose, not applied text, so the regenerated diff is
byte-identical either way.

---

### ⛔ SUPERSEDED PAIR — R79. **DO NOT APPLY.** (§89.2)

| artifact | sha256 | why superseded |
|---|---|---|
| ~~`PREREG_v30a_APPROVAL.diff`~~ | ~~`50cb60d3f215cb51e745eeb68d6f26c076093c5821c7067c6da49a39f36fabdb`~~ | **missing SC-12's §7.7 pointer** at PREREG line 856 |
| ~~`SCHEMA_SET_FINAL.md`~~ | ~~`8d7efb128f34969ff050647ca4e32b06a74d22ef50e2057ebb9d2fb9248f00e8`~~ | **incomplete** — SC-12's pointer text lived only in `Y3_WAIVED_ENTRY_CONDITION.md` §6.3 |

**Marked rather than silently replaced.** An unlabelled superseded approval artifact is how a stale
diff gets applied. The R79 diff was complete against its declared source and **incomplete against
SC-12's stated intent**; R80/§87 moved Y3 §6.3's operative text into the source of record and
regenerated. R79's pair exists only in this record — the file itself was overwritten by regeneration.

**Reproducible (§77.3):** generated twice, byte-identical. **Re-derive at application time and
compare against the diff hash above; if it differs, do not apply.**

---

## §53.2 — UNTRACEABLE LINES: **ZERO**

**Every inserted line falls inside a declared clause range.**

| | |
|---|---|
| inserted lines | 981 |
| blank (generator spacing) | 113 |
| generator framing (`<!-- v30a ID -->`) | 23 |
| **inside a declared clause range** | **845** |
| **UNTRACEABLE** | **0** |

*(Re-derived at R94 by re-running the traceability check against the applied state — **not** by
adding the §10.1 pair's lines to the old figures. Framing is one comment per insertion point, so it
tracks the insertion-point count, 21 → 23. The five figures sum: 113 + 23 + 845 + 0 = 981.)*

**How that was established (B6.2 — not asserted).** The authorised set is built by expanding every
record's `[clause_first_line .. clause_last_line]` into its literal source lines. Each added line is
tested for membership. The only exempt lines are blanks and the generator's own framing comments,
**both counted above rather than waived**. A line that is neither blank, nor framing, nor a member
is reported — **there is no residual category**. 843 of 843 qualifying lines were members.

## §53.3 — THE OTHER DIRECTION: **15 of 15 clauses represented**

No clause in `SCHEMA_SET_FINAL.md` PART 1 is missing from the diff.

**4 lines are removed**, all supersessions the records declare:

- `3. **No runtime finding of any tier, primary or secondary**, appears on fixture_corrected.` — PREREG l.461, replaced by SC-3
- `| **Detector-case coverage** | passed, failed, not_applicable, unsupported, could_not_r…` — l.855, replaced by SC-6a
- `- **assert_audit_complete()** — fails on any unsupported or could_not_run **detector-case**…` — l.929, replaced by SC-12(w)
- `2. **The runtime detectors cannot separate contaminated from corrected fixture…** ` — l.1030, replaced by SC-13a

---

## §53.1 — THE HUNK TABLE

Applied **bottom-to-top** (§77.2), so no insertion shifts a later anchor. Listed here top-to-bottom
as the reader will encounter them.

| PREREG line | record | operation | source | what it does | what would be FALSE without it |
|---|---|---|---|---|---|
| 99 | **SC-9** | INSERT_AFTER | ssf 885–927 | declaration integrity, authority and interpretation, inside §0.2.1 | that the registration says who may interpret the declaration and how |
| 266 | **SC-1** | INSERT_AFTER | ssf 161–203 | new §2.9 — the declaration is the gate's semantic authority | that the declaration, not a role name, fixes what the comparator's terms mean |
| 441 | **SC-10** | INSERT_AFTER | ssf 956–986 | declared non-gated data; forbidden gate arithmetic | that non-gated bodies cannot enter gate arithmetic |
| 451 | **SC-2** | INSERT_AFTER | ssf 234–270 | what the acceptance fixture is composed of, and what may move | that the fixture's composition is registered rather than assumed |
| 461 | **SC-3** | **REPLACE_LINE** | ssf 303–359 | criterion 3 → scored against the declared ground-truth map | criterion 3 as a silence test — the R9 redesign would be unregistered |
| 464 | **SC-4** | INSERT_AFTER | ssf 410–571 | the scored-set partition and criterion 1's denominator | that the denominator is constituted by rule rather than inferred |
| 464 | **SC-5** | INSERT_AFTER (after SC-4) | ssf 596–637 | adjudication routing: which criterion a finding is charged to | that a finding's criterion is determined rather than chosen |
| 468 | **SC-7** | INSERT_AFTER | ssf 742–765 | the gate's input surface and the sequencing rule | that a detector's inputs are enumerated and closed |
| 480 | **SC-8a** | INSERT_AFTER | ssf 823–862 | ex-ante declaration and the freeze | that the declaration is frozen before the gate runs |
| 816 | **SC-13c-2** | INSERT_AFTER | ssf 1602–1609 | §13c-P pointer at §7.2.1 — the suppression clause's scoped exception | that the excepted rule's own site signals the exception |
| 855 | **SC-6a** | **REPLACE_ROW** + INSERT | ssf 682–713 | §7.7 coverage-state table gains `UNSCORED`, plus semantics | that `UNSCORED` is a registered coverage state |
| 856 | **SC-12p** | INSERT_AFTER | ssf (§7.7 pointer block) | the §7.7 pointer: `waived` is defined in §10.2 (v30a); SC-12(w) is its entry condition | that §7.7's own site points at the entry condition — without it two registered texts disagree about whether one exists |
| 892 | **SC-11a** | INSERT_AFTER | ssf 1016–1056 | zeros, absences and pass claims | that a zero may not be published as a pass |
| 915 | **SC-6b** | INSERT_AFTER | ssf 673–681 | §8.2 insertion text (S2(i)) for the second `UNSCORED` level | that the two levels do not collapse |
| 929 | **SC-12(w)** | **REPLACE_LINE** | ssf 1206–1209 | `assert_audit_complete()` also fails on `waived` | that the `waived` prohibition is machine-checkable |
| 961 | **SC-11b** | INSERT_AFTER | ssf 1010–1015 | §8.6 pointer (S2(iii)) so reporting indexes SC-11 | that the reporting section points at the control |
| 1030 | **SC-13a** | **REPLACE_LINE** | ssf 1274–1335 | §10.2 criterion 2 — the replacement criterion | the original criterion-2 sentence, which R35/B3 superseded |
| 1035 | **SC-12** | INSERT_AFTER | ssf 1081–1126 | the replacement-criterion floor, and `waived` DEFINED | that `waived` has an entry condition at all |
| 1035 | **SC-13b** | INSERT_AFTER (after SC-12) | ssf 1368–1438 | admissibility of the replacement criterion | that admissibility is registered, not argued at gate time |
| 1035 | **SC-13c-1** | INSERT_AFTER (after SC-13b) | ssf 1473–1576 | interactions between SC-13a/b and the rest | that the interactions are stated rather than left to inference |
| 1022 | **SC-3-C2op** | **REPLACE_LINE** | ssf 1763 | §10.1 kill-gate criterion 3 → scored against the declared map, consequential to SC-3 | the kill gate still demanding SILENCE on `fixture_corrected` while §6.2 demands findings there |
| 1022 | **SC-3-C2ret** | INSERT_AFTER (after SC-3-C2op) | ssf 1769 | the registered v30 criterion 3, retained verbatim and NOT operative | that the superseded text is recoverable at its own site |
| 1054 | **SC-8b** | INSERT_AFTER | ssf 806–822 | §11 item 8 (S2(ii)) — the freeze and the hash-count rule | that §11 indexes the freeze and carries the hash-count rule |

**Net: 1,099 → 2,075 lines; +981 −5; 15 hunks; 23 insertion points across 15 clauses.**
*(R87/§108 added the two §10.1 line 1022 records: +10 lines, one further replacement, and
a fifteenth hunk, since line 1022 fell between two existing ones.)*

---

## VERIFICATION LEDGER

| check | result |
|---|---|
| §57.3(b) direction 1 — records trace to source | **23 / 23** |
| §57.3(b) direction 2 — source clauses have records | **15 / 15** |
| §57.3(c) — anchors resolve exactly once | **23 / 23, ZERO HALTS** |
| §77.1 — anchor copied from its own INSERTION POINT | **10 / 10** |
| §82 — independent extraction, two unlinked paths | **23 / 23** |
| §77.3 — generated twice | **byte-identical** |
| **D14 — block reachability, every normative block** | **0 unreachable; fires on the pre-fix set** |
| §53.2 — untraceable lines | **0** (845 of 845 traced) |
| §53.3 — clauses missing from the diff | **0** |
| §53.5 boundary test 1 — corrupt a range | **HALTED on the digest** |
| §53.5 boundary test 2 — corrupt an anchor | **diff changed; §77.1 caught it** |

**§53.5 in full.** Shrinking SC-7's declared range by three lines did not produce a wrong diff — the
generator **halted**, because the digest no longer matched. Repointing SC-10's anchor to SC-7's line
**did** change the diff, and §82's extraction still passed (it verifies clause *text*, not
*placement*) — **but §77.1's copied-anchor check caught it**, because `anchor_quoted` was no longer
a substring of that clause's own INSERTION POINT. **Placement and content are guarded by different
checks, and the second boundary test is what established that.**

---

## RESOLVED AT R80/§87 — SC-12's §7.7 pointer

**Was:** SC-12's INSERTION POINT named a second target — the §7.7 pointer after `PREREG.md` line 856 —
whose operative text lived in `Y3_WAIVED_ENTRY_CONDITION.md` §6.3, **not** in the source of record.

**Ruled option (b) and done:** the text was **moved into `SCHEMA_SET_FINAL.md`**, inside SC-12, as an
`INSERTION TEXT — §7.7 pointer` block. §87.2's reasoning is recorded there: SSF is the source of
record for applied text, so applied text outside it made **SSF incomplete** — a defect in SSF, not a
reason to read from two files at generation time.

**§87.3(a) — SETTLED, not a draft.** SC-12(w) was *"adopted at DELTA R35 B3"*; Y3 §6.3 is headed
*"Consequential and mandatory"*; Y3 §7 residual risk 6 reads *"load-bearing and is not optional …
§6.3 above supplies the replacement; it must be applied in the same tag."* No open-decision marker
anywhere in Y3. **Precedent:** DELTA R37/D1 already moved SC-12(w)'s own limb text out of Y3 into SSF
because two copies had drifted — the same correction, for the same reason.

**§87.3(b) — Y3 is in the repository** with a manifest entry (`f102afef…`, 23,460 bytes).

**§87.4 — transcription checks:** verbatim lift, **verified by exact substring in both directions**,
and Y3 §6.3 now carries a note recording that SSF holds the operative copy, that Y3 is the
**historical source**, and that **if the two ever differ, SSF governs**.

**New record `SC-12p`** — PREREG line 856, INSERT_AFTER. That is the 21st insertion point.

---

## §88 — SWEEP FOR OTHER EXTERNAL OPERATIVE TEXT

**Population (§30.1):** all **16** `**INSERTION POINT.**` fields in PART 1, read header-to-break.
**No exclusions.** Every document reference in each is reported, benign ones included.

| clause | reference | resolves to | in repo | assessment |
|---|---|---|---|---|
| **SC-6** | `K1 §0` | `K1_SCHEMA_CLAUSES.md` | **yes** | **benign** — cited for *why* two insertion points are required; not applied text |
| **SC-11** | `Part 3` | *internal to `SCHEMA_SET_FINAL.md`* | n/a | **benign** — internal section reference; the operative text is SSF's own `INSERTION TEXT — §8.6` block |
| **SC-12** | `Y3 §6.3` | `Y3_WAIVED_ENTRY_CONDITION.md` | **yes** | **RESOLVED at R80/§87** — text moved into SSF |

**13 of 16 fields name no external document at all.** No further instance of operative text outside
the source of record.

**The sweep found a defect in itself first, and it is recorded because §88.4 is the reason it exists.**
Its first version matched only *filenames* (`\S+\.md`) and returned **16/16 clean** — while `Y3 §6.3`,
the very reference that prompted the sweep, sat in the population. A document identifier with no file
extension was invisible to it. Widened to identifiers, it then **still** returned 16/16, because a
heredoc had written literal backspace bytes into the regex where `\b` was intended, so three
alternatives could never match. **Both were caught only by testing the sweep against the instance
already known to exist** — which is the whole of H-L21 in one paragraph.
