# BLOCK MANIFEST — every applied source block, and the hunk it belongs to

**DELTA R44 / L1(b). HAND-AUTHORED from source. Not generated.**
**Revision 2 — corrected against L2's independent verification (R44/L2).**

Three extraction tools failed to produce this, each for the same reason and not for want of
better patterns: **the source's block boundaries do not align with hunk boundaries.** Six
blockquote runs in Part 1 carry markers or notes for several different sites. No pattern
over block structure can recover an assignment that block structure does not encode. So the
assignment is written; only the *check* is mechanical.

---

## §0 — WHAT THE CHECK IS FOR (changed at L2's finding)

**The manifest is the SOURCE the applier builds `operative_text` from. It is not a thing
checked against `operative_text`.**

L2 established that `_X5_hunks_v2.json` is *systematically displaced*: within each clause
group the earlier assembler wrote (marker + clause) into the group's first hunk and then
broadcast the clause into the rest. That produced two byte-identical pairs (**H3 == H37**,
2,741 chars; **H22 == H26**, 2,061 chars), one **empty** hunk (**H20**, 0 chars), and four
hunks with no text at all.

So a check scoring the manifest *against* the JSON would report the manifest ~13/42 wrong
when the manifest is right and the JSON is wrong. The direction of authority is therefore
fixed here: **manifest → JSON → artifact.** The three K1 assertions still hold, but assertion
(iii) becomes "the artifact renders what the manifest assigns", not "the JSON agrees with
the manifest".

---

## Scope, declared and proven (K3)

**POPULATION A — `SCHEMA_SET_FINAL.md` Part 1**, frozen at `_K1_population_FROZEN.json`:
**36 blocks**. **Five** of the 36 are multi-site runs, written out in §A below, giving
**45 entries**.

**Reconciliation — the count, its decomposition, and the miscount it pre-empts (R84/§100).** The
freeze at R43/K1 held **33** blocks over lines 89–1576, and its coverage proof was *33 inside + 31
outside = 64 blockquote runs and fenced blocks in the whole file*, which L2 re-derived
independently, confirming all 33 anchor ranges byte-correct. **That was the freeze, and it is
stated in the past tense because three blocks have been added since**, each declared in
`_POPULATION_CHANGES.md` before adoption, as N2's rule requires — *freeze means no SILENT change,
not no change*:

| round | block | what |
|---|---|---|
| **R53/Y1** | 34 | `§10.1-C2op` — the C2 operative item, moved in as a source of record |
| **R53/Y1** | 35 | `§10.1-C2ret` — the C2 retention block, moved in with it |
| **R58/W4** | 36 | `§AC` — the v30a disclosures block, which did not previously exist |

**33 + 3 = 36**, which is exactly what `_K1_population_FROZEN.json` holds. Entries follow from
blocks: **36 − 5 multi-site + 14 expanded rows = 45**, which is exactly what the §A table holds.
Under the freeze's 33 the same five expansions gave 42, which is where the older figure came from.

**A reader counting blocks in a pre-growth copy will get 33, and a reader counting entries will get
42; the three additions are declared at `_POPULATION_CHANGES.md` and carried in the table below, and
the reconciliation is here.** **The prose above was pre-growth until R84 while the table was
post-growth — one document describing one thing two ways. The TABLE is the authority.** The older
prose also said *six* multi-site runs where the expansion has only ever contained **five** (blocks 1,
3, 7, 10 and 14); 42 required five even then, so that figure was wrong at the freeze and is corrected
here rather than carried.

**POPULATION B — operative text from other sources.** §B lists hunks drawing text from
`K2_AMENDMENT_LEDGER.md`, `PREREG_v30a_DIFF.md`, `Y3_WAIVED_ENTRY_CONDITION.md`, or a delta
draft, so that "absent from §A" never means "undrafted". **§A ∪ §B = 38/38 hunks** (L2).

**Separator rule, stated because L2 found it applied inconsistently:** a bare `>` line
between two markers belongs to the entry ABOVE it. Lines 153, 567, 692 and 698 are absorbed
that way. Without the rule a mechanical partition check trips on 567, 692, 698.

**Not covered:** Parts 2+ of `SCHEMA_SET_FINAL.md`, `AVAILABILITY_DECLARATION.md`, `PREREG.md`.

---

## §A — Population A: 36 blocks, 45 entries

`APPARATUS` = present in Part 1 but **not applied text**. It must be claimed by nothing; a
hunk claiming an apparatus block is a check failure.

**RANGES ARE DERIVED, NOT DECLARED**. Every range below was re-derived at R146/A39 from the structure's own delimiters in `SCHEMA_SET_FINAL.md` at the approved hash `32358f6dfc7f96d2…`, and 8 of them were wrong — 8 by exactly eight lines. **Do not extract inside a range from this table without re-deriving it**: the previous values ended before their blockquotes did, and extracting inside them truncated §AB and §AC by eight lines each, cutting §AC's disclosure 7 mid-sentence. A declared range is an assertion; the block's extent is a fact about the file.

| # | Anchor (lines) | What it is | → Hunk |
|---|---|---|---|
| 1a | 150–153 | MARKER — §2.3 line 205 `column_roles` | **H5** (205, marker) |
| 1b | 154–159 | MARKER — §2.4 lines 220–222, label-availability formula | **H6** (220, marker) |
| 2 | 163–202 | THE CLAUSE — SC-1, new §2.9 | **H7** (266, insert) |
| 3a | 228–229 | Citation — §6.2 line 445 superseded (H1 hunk H2) | **APPARATUS** |
| 3b | 230 | Citation — §6.2 line 450 superseded (H1 hunk H3) | **APPARATUS** |
| 3c | 231 | Citation — §6.2 line 451 superseded (H1 hunk H4) | **APPARATUS** |
| 3d | 232 | Citation — §10 line 992 consequential (H1 C1) | **APPARATUS** |
| 4 | 236–269 | THE CLAUSE — SC-2 | **H12** (451, insert) |
| 5 | 293–301 | MARKER — §6.2 criterion 3 retained verbatim, **incl. its §10.1 consequential note** | **H15** (461, replace) |
| 6 | 305–358 | THE CLAUSE — SC-3 | **H15** (461, replace) |
| 7a | 382–406 | MARKER — §6.2 line 459, criterion 1 added not superseded | **H14** (459, marker) |
| 7b | 407–408 | MARKER — §6.2 line 446 NOT AMENDED | **H14** (459, marker) |
| 8 | 412–570 | THE CLAUSE — SC-4 | **H16** (464, insert) |
| 9 | 598–636 | THE CLAUSE — SC-5 | **H17** (464, insert) |
| 10a | 663–669 | MARKER — §7.7 line 855, v30 row retained | **H21** (855, replace-row) |
| 10b | 670–671 | MARKER — §8.2 line 915 extended not superseded (M2) | **H25** (915, marker) |
| 11 | 675–680 | INSERTION TEXT — §8.2 after line 915, S2(i) | **H26** (915, insert) |
| 12 | 684–712 | THE CLAUSE — SC-6 `unscored` | **H22** (856, insert) |
| 13 | 744–764 | THE CLAUSE — SC-7 | **H18** (468, insert) |
| 14a | 789–794 | MARKER — §6.2 line 480 extended not superseded | **H19** (480, insert) |
| 14b | 792–793 | MARKER — §11 items 1–7 extended by item 8 | **H37** (1050, marker) |
| 14c | 795–800 | MARKER — §11 item 3 superseded as a file set | **H37** (1050, marker) |
| 14d | 801–804 | MARKER — §0.2.1 line 97 superseded as a count | **H3** (97, marker) |
| 15 | 810–821 | INSERTION TEXT — §11 item 8 after line 1054, S2(ii) | **H38** (1054, insert) |
| 16 | 825–861 | THE CLAUSE — SC-8 | **H19** (480, insert) |
| 17 | 887–926 | THE CLAUSE — SC-9 | **H4** (99, insert) |
| 18 | 950–954 | MARKER — §6.1 line 431 heading and table | **H8** (431, marker) |
| 19 | 958–985 | THE CLAUSE — SC-10 | **H9** (441, insert) |
| 20 | 1012–1014 | INSERTION TEXT — §8.6 after line 961, S2(iii) | **H28** (961, insert) |
| 21 | 1018–1055 | THE CLAUSE — SC-11 | **H24** (892, insert) |
| 22 | 1086–1125 | THE CLAUSE — SC-12 "Waived", defined | **H35** (1035, insert) |
| 23 | 1145–1181 | **SC-12(w) — the `waived` entry condition, (w1)–(w7) + bounds** | **H35** (1035, insert) |
| 24 | 1207–1212 | MARKER — §8.3 line 929, v30 bullet retained | **H27** (929, replace) |
| 25 | 1208 | **OPERATIVE v30a TEXT at line 929** — the replacement bullet | **H27** (929, replace) |
| 26 | 1215–1219 | Instance record under ROWS COVERED | **APPARATUS** |
| 27 | 1255–1280 | MARKER — §10.2 criterion 2 line 1030, branch-conditional | **H33** (1030, replace) |
| 28 | 1284–1342 | THE CLAUSE — SC-13a | **H33** (1030, replace) |
| 29 | 1378–1445 | THE CLAUSE — SC-13b | **H34** (1035, insert) |
| 30 | 1483–1583 | THE CLAUSE — SC-13c | **H36** (1036, insert) |
| 31 | 1596–1598 | ANCHOR — registered `PREREG.md` line 816 quoted verbatim | **APPARATUS** |
| 32 | 1604–1608 | INSERT AFTER — §13c-P, the line-816 pointer | **H20** (816, insert) |
| 33 | 1640–1687 | §AB — the amendments-block recording text | **H2** (8, insert) |
| 34 | 1754–1756 | §10.1-C2op — the C2 operative item (moved here R53/Y1) | **H32** (1022, replace) |
| 35 | 1760–1762 | §10.1-C2ret — the C2 retention block (moved here R53/Y1) | **H31** (1022, insert) |
| 36 | 1695–1745 | §AC — the v30a disclosures block, seven items (R58/W4) | **H2** (8, insert) |

**Entries: 45. Claimed by a hunk: 39. Apparatus: 6. Unclaimed and undrafted: 0.**
*(45 = 39 + 6. Pre-growth these read 42 = 36 + 6; the three R53/Y1 and R58/W4 additions are
all claimed, so the apparatus count is unchanged and the claimed count carries the growth.)*

---

## §B — Population B: hunks whose text comes from elsewhere

| Hunk | Site | Source of its operative text |
|---|---|---|
| **H1** | 6 | `K2_AMENDMENT_LEDGER.md` §8.1, amendment status line span:«**Amendment status:** **v30a — this file is amended.** »…«v30:PREREG.md` recovers the registered text byte-exact.» |
| **H2** | 8 | `K2_AMENDMENT_LEDGER.md` §8.2, the amendments block (plus §A-33) span:«## v30a amendments (class C under §0.2.1) **What this b»…«** — which is what the sliced-variant row of (a) does. » |
| **H10** | 445 | `PREREG_v30a_DIFF.md` H2 REPLACE block — **carries its own marker** span:«- **Reference AUC anchor — v30a, operative** (supersede»…« line byte-exact with `git show prereg-v30:PREREG.md`.*» |
| **H11** | 450 | `PREREG_v30a_DIFF.md` H3 REPLACE block — **carries its own marker** span:«- **Contamination availability class — v30a, operative*»…« tag hashes, which binds harder than the manifest did.*» |
| **H13** | 451 | `PREREG_v30a_DIFF.md` H4 REPLACE block — **carries its own marker** span:«- **Sliced variant — v30a, operative** (supersedes the »…«g is not dropped and the slicer is not exempt from CI.*» |
| **H23** | 856 | `Y3_WAIVED_ENTRY_CONDITION.md` §6.3, the redrafted §7.7 pointer span:«**`waived` is defined in §10.2 (v30a).** That definitio»…« be reported in this state.** Neither is restated here.» |
| **H29** | 992 | `J3_C1_REDRAFT.md` §3, the operative row — **rebuilt from it at R49/B2; it previously carried the WITHDRAWN R39/F2 draft** span:« §10.0 ordering followed; claims verified or a deviatio»…«ill fail it, and a failure of either denies the row.** » |
| **H30** | 998 | `K2_AMENDMENT_LEDGER.md` §9.1, the C1 retention block span:«**§10 line 992 (Phase 1 gate cell) — SUPERSEDED BY v30a»…«d row byte-exact with `git show prereg-v30:PREREG.md`.*» |
| **H31** | 1022 | **MOVED R53/Y1 — no longer section B.** Its text now lives in `SCHEMA_SET_FINAL.md` under `§10.1-C2ret` and is claimed by §A row 35; M6 check (II) binds it. It was section-B only because it was drafted inside a delta. |
| **H32** | 1022 | **MOVED R53/Y1 — no longer section B.** Its text now lives in `SCHEMA_SET_FINAL.md` under `§10.1-C2op` and is claimed by §A row 34; M6 check (II) binds it. It was section-B only because it was drafted inside a delta. |
| **H37** | 1050 | §A-14b **and** §A-14c |

---

## §C — Findings, and the two I got wrong

**C-1 — WITHDRAWN. My "§11 items 1–7 has no hunk" was false, and its remedy was dangerous.**
I found the marker at L690–691 unclaimed and offered, as one disjunct, that *"the ledger row
is spurious and should go"*. L2 settled it against me from the applied verification copy:
`_K2_verify/PREREG.md` line 1417 carries **both** markers beneath §11's list, in order, and
H37's own `what_changes` names both verbatim — *"two marker blocks are placed: '§11 item 3 —
…' and '§11 items 1–7 — v30a, EXTENDED'"*. Corroborated three further times in the K2 ledger.
It belongs to **H37**. Had the disjunct been taken, it would have deleted a registered surface
that four records support. **A finding of absence is only as good as the search behind it, and
mine searched the wrong artifact** — the drafting sources, not the applied copy.

**C-2 — CORRECTED. Entries 3a–3d are APPARATUS, not four assignments.** I routed each to the
hunk at the site it names. The source says the opposite, one line above them (SSF 225–226):
*"This clause is the schema layer over three amendments H1 already drafts at instance-bearing
lines. **Their markers stand as H1 wrote them and are cited, not re-drafted:**"* — a citation
list, not applied text. Three further confirmations: the applied copy contains none of the
four; H10/H11/H13 **already carry their own supersession markers**, so applying these would put
a second, differently-worded supersession statement at each site; and H2's amendments block
enumerates the marker surfaces — 445, 450, 451 and 992 are in its *superseded* list, not its
*marker* list. **My assignment would have created four duplicate markers.**

**C-3 — Entry 5 stands at H15, against a verifier's challenge.** One verifier read L299–301
(*"Consequential — §10.1 line 1022"*) as a sixth split belonging to H31. The applied copy shows
both paragraphs together at line 461's site inside criterion 3's replacement, and H31 already
carries its own separately drafted 1022 retention. Routing it there would duplicate. It is a
note *in* the SC-3 marker, not a marker *at* 1022.

**C-4 — the invariant is one-way.** Two blocks may share a hunk (5 and 6 at H15; 22 and 23 at
H35; 24 and 25 at H27; 14b and 14c at H37). One block may never have two hunks.

**C-5 — entries 23 and 25 are the two K4 names**: SC-12(w)'s limb text and the §8.3 operative
bullet. Both claimed here for the first time. No prior review saw either.

**C-6 — H20 is claimed and empty.** Entry 32 is the sole copy of the §13c-P line-816 pointer,
and H20's `operative_text` is the empty string. Presence in §A is *not* evidence a hunk has
text — which is why §0 fixes the direction of authority as manifest → JSON, not the reverse.
