# DECLARED CHANGES TO THE FROZEN POPULATION

**N2's rule: freeze means no SILENT change, not no change.** Every change to a block of
`SCHEMA_SET_FINAL.md` PART 1 after the R43/K1 freeze is declared here, with both hashes, before
`--refreeze` will adopt it. A change not declared here fails the check; that is the whole
mechanism.

An entry states: the round that made it, the block, `old sha12 -> new sha12`, and the reason.
Re-anchoring alone (same `sha12`, moved line range) is a consequence of another block's growth
and is recorded in the round's entry rather than per block.

---

## R47/P5 — SC-3(a): the map artifact is not the map

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 6 — THE CLAUSE — SC-3 | 305–352 -> 305–358 | `7189700b9305` -> `dfddb160a6b0` | SC-3(a)'s schema sentence |

**What changed.** SC-3(a) said the map is "published as an artifact with a **declared schema**:
one row per scored cell". The artifact `n1\declared_map.csv` holds **984 rows**, of which **888**
are `SCORED` — so "one row per scored cell" is false of it, and nothing in the corpus said the
artifact may carry rows that are not cells of the map. The sentence now reads "one row per cell of
the declared scored population" (960 cells: 888 `SCORED` + 72 `UNSCORED_FOR_LACK_OF_DATA`) and
states that the artifact may in addition carry rows of a class the declaration declares
**DIAGNOSTIC**, citing **SC-10(c)**.

**Why it is a citation and not a new rule.** SC-10(c) already registers that diagnostic classes
are not members of the declared scored set, and the declaration already cites SC-10(c) by name to
declare `mbo_all_rows` the 11th class. **SC-10(e) forbids restating it** — "these rules are stated
here and cited elsewhere". So the added text cites SC-10(c) and states only the thing no clause
stated: that the ARTIFACT and the MAP are not the same set of rows.

**Why it was needed (R47/P5).** Three independent review reports took the scored population to be
888 and none noticed the third `scored_flag` state. A checker joining on
`scored_flag != 'UNSCORED_FOR_LACK_OF_DATA'` picks up **912** rows, not 888. The exclusion was
sound and declared in the declaration; it was **unstated in the registration**, which is the shape
this round exists to eliminate.

**Does it weaken anything?** No. It adds requirements (declare the class, flag every such row,
name which population each published figure counts) and removes none. The dispositions of SC-3(b)
are unchanged.

**Consequential re-anchoring.** The block grew by **6 lines**, shifting the 27 PART 1 blocks below
it. `BLOCK_MANIFEST.md` was re-anchored by `_P5_reanchor.py`, which PROVED the re-anchor rather
than computing it: for all **42** manifest rows, the text at the new range in the new file is
byte-identical to the text at the old range in the pre-edit file (0 failures).

**Verification owed (R46/N5).** This is new normative text in the acceptance gate's map clause.
It has been drafted and mechanically checked; it has **not** had independent verification by a
non-author, nor a composed read of §6.2 as amended.

---

## R49/R5 — SC-4(k): the criterion-1 floor and the manifest reconciliation

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 — THE CLAUSE — SC-4 | 390–474 -> 390–509 | `4a2c05d77a08` -> `b286d4934a01` | new limb (k), 35 lines |

**What changed.** SC-4 ran (a)–(j) and **nothing floored the scored population**. N is defined as
the length of the REQUIRED list, but no clause required that list to be non-empty — so criterion 1
was satisfiable by a declaration that classed almost everything OUT OF JURISDICTION or UNSCORED.
The schema set already contained the closing sentence, at **SC-13b(b1)**, roughly 500 lines away
and applied to a branch that is switched off. Three clauses blocked importing it: **SC-4(g)** lets a
unit hold no gate class at all, **SC-3(c)** hands the scored population to the declaration, and
**SC-4(a)** forbids any other classification from entering a criterion — which bars the very check
that closes the hole.

**(k1) the floor.** Non-empty on every declared side; STOP otherwise; lifted only by supplementing
and re-freezing under §11 — SC-13b(b1)'s own remedy, not a new one. **Non-emptiness is the whole
floor** because any minimum above zero would be a threshold read off this fixture's own
distribution, which §7.0 forbids. That is the same reasoning that ruled P6 at R49/R1.

**(k2) the reconciliation.** Per unit, against the manifest's independently-leaking-source list,
every difference named with the registered predicate of (b) that produced its class. A count does
not satisfy it.

**(k3) the carve-out**, and it is load-bearing: *"a reconciliation published under this limb is a
disclosure, not a classification entering a criterion, denominator, or count."* Without it (k2)
contradicts (a).

**(k4) the failure condition**, stated because R49/R2's refined SC-8(g) requires it, and classified:
**a live gate item, not a regression guard.**

**Does it weaken anything?** No. It adds a STOP condition and a publication duty, and removes none.

**Is it satisfied today? NO — and that is the point of drafting it.** The declaration publishes
§A.6.5, a per-unit cross-tabulation of the construction-SOURCE cut against the gate cut. **That is a
different pair of partitions.** No per-unit reconciliation against the manifest's leaking-source
list exists anywhere in the declaration. Computed this round from
`f3\fixture_manifest_DRAFT.json` joined to §A.6.5's gate column, it would show:

```
25 LEAK-SOURCE  =  11 REQUIRED  +  13 OUT OF JURISDICTION  +  1 UNSCORED
 6 DESCENDANT   =   5 OUT OF JURISDICTION + 1 UNSCORED
 4 CLEAN        =   4 OUT OF JURISDICTION
                                                    35 total, both cuts
```

**Fourteen units** the manifest calls leaking sources are not classed REQUIRED — thirteen of them in
a class where **a finding on them is a false positive**: `mid_return_{1,5,10,30}s`, `bid_size_1`,
`ask_size_1`, `total_bid_depth`, `total_ask_depth`, `book_slope_bid`, `book_slope_ask`,
`spread_ticks`, `tick_direction`, `weighted_mid`, plus `buy_volume_10s` UNSCORED under §C.4(a).
**The data to satisfy (k2) exists; the publication does not.**

**Verification owed (N5).** New normative text in the acceptance gate. Drafted and mechanically
checked; **not** read by any non-author, and no composed read of §6.2 as amended.

---

## R49/R6 — blockers B5 and B7 from the N5 verification

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 — THE CLAUSE — SC-4 | 390–509 -> 390–517 | `b286d4934a01` -> `28ebb287a9b2` | (k2) rewritten (B5) |
| 30 — THE CLAUSE — SC-13c | 1414–1510 -> 1422–1522 | `cf421dcccf9e` -> `e53506718260` | (c5)(i) now cites instead of restating (B7) |

### B5 — SC-4(k2) made an uncommitted DRAFT a gate input

**The defect.** (k2) required a reconciliation against *"the manifest's
independently-leaking-source list"* and (k4) made its absence a gate failure. But
`f3\fixture_manifest_DRAFT.json` carries `"manifest_status": "DRAFT - author review required"`;
the declaration's SC-8(a) freeze does not enumerate it; and the declaration **expressly withdraws
its leaking-source count from the arithmetic** — *"The manifest's independently-leaking-source
count 25 is NOT a frozen gate number."* SC-8(a): *"an object the gate consumes and the enumeration
omits is a defect in the enumeration."* **A complete reconciliation could be made incomplete by an
author review that is not a class C amendment.**

**The fix.** (k2) now names the **list** rather than the count, states that reading the list makes
neither the count a gate quantity nor admits it to a denominator, and requires the manifest to be
**enumerated in the SC-8(a) freeze** and **not `DRAFT` at the tag**. The pre-existing tension — the
count is already read for `total_fed_to_phase7` while not being frozen — is narrowed, not widened:
the two statements are now made to agree on the page.

### B7 — SC-13c(c5)(i) held a second, DIVERGENT copy of SC-3(a)'s indexing rule

**The defect, and it is the one §0.2.1 line 77 exists for.** (c5)(i) declared that SC-3(b)'s
dispositions are *"held by citation and not restated here"* — and then, in the next clause,
**restated SC-3(a)'s indexing triple.** At R47/P5 I amended (a) to say the map artifact may carry
rows that are not cells of the map. **I did not touch the copy.** So the second copy went stale in
exactly the way the single-source rule predicts: it now describes an indexing rule (a) no longer
states alone.

**The fix.** (c5)(i) holds the map, its indexing, and what the publishing artifact may carry **all
by citation to SC-3(a), none restated**, with a dated note recording that the copy existed and how
it diverged. **Nothing about the kill gate's substance changes**; what changes is that there is now
one statement of the rule instead of two.

**The general lesson, recorded because it will recur.** Amending a clause that another clause
restates leaves a divergent copy **silently**. The R47/P5 edit passed every check at the time. Only
a composed read found it — which is the argument for N5's composed-read requirement existing at
all.

**Verification owed (N5).** Both edits are new normative text and neither has been read by a
non-author. They were made in response to a verification pass, which is not the same as having
passed one.

---

## R49 addendum S1–S3 — SC-4(k) revised: which mechanism does what, and what a reader can check

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 — THE CLAUSE — SC-4 | 390–517 -> 390–543 | `28ebb287a9b2` -> `c20383d0f2a3` | (k) restructured; (k2)(i) added |

### S1 — the floor was reading as the protection, and it is not

**The defect in the previous draft.** (k) was headed *"THE REQUIRED LIST IS NON-EMPTY, AND THE
DENOMINATOR IS RECONCILED"* — two obligations in sequence, with nothing saying which stops what.
**A reader would take the floor for the protection.** It is not: **N ≥ 1 is satisfied by scoring a
single column.** A declaration could class thirty-four of thirty-five units out of the scored set
and clear (k1) intact.

**The fix.** (k) now opens by naming both failure modes and assigning an instrument to each: the
**degenerate** case (population empty) to the floor, the **gradual** case (narrowed unit by unit
until what survives is not worth scoring) to the reconciliation. (k1) is retitled **THE TERMINAL
BACKSTOP** and closes with *"it is not the protection and must not be cited as one"*; (k2) is
retitled **THE OPERATIVE MECHANISM**. Nothing about either obligation weakens — what changes is that
the clause now says which one is load-bearing.

### S3 — the adversarial test on (k), and the only bar that is registerable

**What (k) licensed, before this revision.** A declarer satisfies it by classing 24 of 25
manifest-classed leaking sources OUT OF JURISDICTION, naming each one and citing a registered
predicate for each — **on grounds of any quality whatever.** The predicate citation is a form
requirement; it constrains the shape of the answer, not its substance.

**Why the obvious fix is not available.** A requirement that grounds be *adequate*, *substantive* or
*well-founded* is unregisterable vagueness — no reader could apply it and no check could score it,
and writing it would be a constraint in appearance only. This registration already has a rule about
that shape of drafting.

**What is achievable, and is now required — (k2)(i): PROVENANCE.** Every ground **names the artifact
and the location within it** — file, and row, line, or field. A ground with an artifact behind it
can be looked up and disagreed with. **A ground with nothing behind it becomes visible as such**,
rather than reading as plausible. That is the whole of what the clause can achieve at this site, and
it is worth more than a bar nobody could apply.

### S2 — the verifiability limit, stated instead of implied

**Established at R47/P9 disclosure 5:** `n1\declared_map.csv` is staged by the ceremony plan and
ships with the tag; **the acceptance fixture does not** — Artifact B is 64 parquets per side under
`results\phase7*\l2_predictions\`, outside the repository, with no clause requiring publication.

**So (k3) now says what a reader can and cannot do.** Can check: **completeness** (every
manifest-classed leaking source accounted for), **internal consistency** (each ground citing a
registered predicate), **provenance** (each ground naming an artifact and location). **Cannot:**
independently verify any classification against the fixture's data. The limb is registered as **a
disclosure obligation with limited external verifiability**, in those words.

**Why this belongs in the clause rather than in a note.** An obligation that implies an audit the
reader cannot perform is the same defect class as an overstated availability claim — and this
project has already corrected one of those this round, at §A.1 item 2.

### S4 — the procedure was exercised, not assumed

The growth check **crashed** the first time it was asked to absorb a change this session
(`KeyError('lines')` — two enumerators, two schemas), and its MODIFIED pairing then **failed a
second time** when an earlier block's growth shifted a later modified block. Both are fixed and both
were found by running it. This pass: re-enumerated (33 blocks, delta reported — **1 modified, 25
re-anchored, 7 identical**), re-anchored **dry-run first** with 42 of 42 rows resolved and 0
unresolved, manifest row 8 extended to the block's new end, then refrozen against the declared hash
pair above.

**Verification owed (N5).** Unchanged and now larger: (k) is the biggest piece of new normative text
in the amendment and **no non-author has read the revised form.** The R49/R6 pass read the previous
draft and returned NOT_FIT on it; these revisions answer S1–S3, not R6's blockers, which were
answered separately.

---

## R53/Y1 — the last two hunks get a source of record

| block | lines | sha12 | change |
|---|---|---|---|
| 34 — §10.1-C2op | 1669–1671 | `4c18ca940288` | **ADDED** — the C2 operative item |
| 35 — §10.1-C2ret | 1675–1677 | `cbf0368075a1` | **ADDED** — the C2 retention block |

**What moved, and why it was wrong where it was.** Both texts lived in `_X5_hunks_v2.json` and
nowhere else. That was never a decision — they were drafted inside deltas (the operative item at
R39/F2, the retention block at K2 §9.2) and redrafted at R47/P1 to the narrowest C2. The
consequence, surfaced at R52: **the amendment's newest and most-revised normative text was the only
applied text no provenance check could reach.** Every other hunk had a source document to be checked
against; these two were checkable by review alone.

**Where they went.** `SCHEMA_SET_FINAL.md` PART 1, under their own headings, as **fenced** blocks.
One source of record for all applied text. **No second document was created for delta-drafted
hunks** — that would be the duplicated-authority shape, and the fix for a provenance gap must not
introduce a worse defect than the one it closes.

**What this changes about how they are checked.** They leave manifest §B and enter §A. §A is bound
by **M6 check (II)**, which asserts `src in op` — the SOURCE block contained in the HUNK. **That is
the converse direction, so it catches a deletion**, which is the whole reason for the move. §B's
rows are retired with a MOVED note rather than deleted, so where the text used to live is still on
the record.

**Structural obstacles: none, and each was checked before writing rather than after (R53/Y2).**
The enumerator already treats fences as population blocks — 3 of the 33 frozen blocks were fences.
The blocks were appended at PART 1's tail, after the last existing block, so **no existing block's
line range moved**: N2 reports `added 2, removed 0, modified 0, re-anchored 0, identical 33`, and no
re-anchor was required. The assembler is unaffected: it builds from the hunk JSON, and the JSON is
now bound to the source rather than being the source.

**Verification owed (N5).** Neither text changed a character in this move — both were copied from
the hunks verbatim and M6 (II) proves containment. What changed is what can check them. The texts
themselves still carry the R49/R6 verification's open findings.

---

## R54/W3 — the line-459 marker states the sign reversal

| block | sha12 before -> after | change |
|---|---|---|
| SUPERSESSION MARKER — §6.2 line 459 | `6d663899faa4` -> `8a07d997c85c` | marker corrected, +22 lines |

**The defect.** The marker read *"ADDED NOT SUPERSEDED. Criterion 1 stands byte-exact."* True
byte-for-byte; false at the outcome. Of the 25 columns the manifest classes LEAK-SOURCE, **11 stay
REQUIRED and 14 move to OUT OF JURISDICTION or UNSCORED**, where SC-4(b) makes an availability-class
finding a **false positive**. On those 14 the requirement **reverses sign** — absence-is-a-miss
becomes a-finding-fails-the-gate — under a marker telling the reader nothing changed.
**§0.2.1 line 97 measures at the outcome.**

**The fix.** The marker now carries the 25 / 11 / 13 / 1 table, states that the reversal **is** a
supersession at the outcome whatever the byte-level text does, and says plainly that a reader
diffing v30 against v30a at line 459 will see no change and conclude wrongly. The narrowing itself
is unchanged and is permitted as class C; what was not permitted was recording it as no change.

---

## R58/W4 — the disclosures block, which did not exist

| block | lines | sha12 | change |
|---|---|---|---|
| 36 — §AC disclosures | 1682–1732 | `7d72cae05ccb` | **ADDED** — seven disclosures |

**What was found while doing this.** P9's six disclosures were established as facts at R47 and
recorded **only in the round state**. The block itself was never drafted into the amendment. Worse,
the line-459 marker landed at R54/W3 already said the reversal is *"carried as a disclosure on the
face of the amendment (R54/W4, disclosure 7)"* — **a forward reference to a block that did not
exist.** Both are closed here.

**The seventh (R56/W4):** criterion 1's effective requirement **reverses on 14 of 25** leaking-source
columns — 11 REQUIRED, 13 OUT OF JURISDICTION, 1 UNSCORED — while line 459's registered text does
not move, so a reader diffing v30 against v30a there sees no change and concludes wrongly.

**Claimed by H2**, the §AB amendments-block hunk: the block a reader opens to learn what the
amendment does. Not a new hunk; a second §A row for a hunk that already carried two.

**Verification owed (N5):** new normative text, unread by any non-author.

---

## R60/F3 — W6 group 2 (B5): (k4) indexes the two conditions (k2) imposes

| block | lines | sha12 | change |
|---|---|---|---|
| 8 — SC-4 | 412–570 | `415e8562be7e` | (k4) extended |

**The defect.** (k2) required the manifest to be enumerated in the declaration's SC-8(a) freeze and
to carry a non-`DRAFT` status at the tag. **(k4) indexed neither.** A limb may not impose a
condition and leave nothing to enforce it — that is a requirement with no failure mode, which is the
shape SC-8(g) was drafted against.

**Both are unmet as at this date**, and (k4) now says so: the freeze's *"specifically and
exhaustively"* list does not name the manifest, and `fixture_manifest_DRAFT.json` still reads
`"manifest_status": "DRAFT - author review required"`. Both are on the ceremony landing list.

**Also (P5):** PART 5 is headed *"EVERY DIFFERENCE BETWEEN THIS FILE'S PART 1 AND SSA's PART 1"* and
states *"Anything not listed is byte-identical to SSA"*. **SC-4(k)'s applied lines were not listed.**
Row **F-16** now lists them. A completeness claim with an unlisted difference under it is false on
its face, and PART 5 is apparatus rather than applied text, so this changes the record and not the
amendment.
