## COMPLETENESS CRITIC — v30a FINAL DIFF

### 0. Blocking meta-finding (read first)

**The artifact I was given is truncated.** It begins mid-sentence — `"written; it would cite a clause that does not exist."` — inside §3 item 1. **§1 and §2 ("THE HUNKS") were not supplied.** I never saw a single hunk body, hunk header, or hunk→anchor mapping. Everything below is checked against the sources and against the artifact's own §3/§4/§5 cross-references (hunks 1, 5, 6, 7, 12, 13, 15, 23, 25, 26, 28–33, 36, 37 are named there; the rest are invisible to me). **Any claim about a specific hunk's content is NOT ESTABLISHED by this pass.** Re-run this critic against the whole document.

---

### 1. Direct answers to the seven questions

| Question | Answer |
|---|---|
| Every clause SC-1…SC-13c has ≥1 hunk? | **Yes**, by anchor. All 15 clause anchors appear in §4.1: SC-1→266, SC-2→451, SC-3→461, SC-4→464, SC-5→464+466, SC-6→855/856+915, SC-7→468, SC-8→480+1054, SC-9→99, SC-10→441, SC-11→892+961, SC-12→1035+929+856, SC-13a→1030, SC-13b→1035, SC-13c→1035+816. |
| Every `INSERTION POINT` appears? | **Yes for all 17** clause-level paragraphs (SSF 107, 185, 251, 334, 453, 515, 595, 639, 739, 804, 862, 935, 1018, 1037, 1082, 1199, 1301) plus §13c-P's ANCHOR (SSF 1433). **One exception: §AB has no INSERTION POINT paragraph and no anchor anywhere** — see G-2. |
| Orphaned block rows? | **None.** All 37 rows ((a) 9 + (b) 10 + (c) 14 + (d) 4) land on a line present in §4.1's lists. |
| Hunks not backed by a block row? | **Yes — two.** See G-1. |
| SC-14 truly absent? | **Yes** in the three operative sources (0 hits, re-run). Stale in exactly four `amendment/` files, matching §4.2. **But see G-12 — T2 is a live ceremony deliverable built entirely on SC-14.** |
| §7.7 pointer redraft present? | **Confirmed.** Exists only at `Y3_WAIVED_ENTRY_CONDITION.md:184`; `SCHEMA_SET_FINAL.md:937` still routes to H8. §4.4 is correct. |
| Line-929 §8.3 hunk present? | **Confirmed.** Apparatus at `SCHEMA_SET_FINAL.md:1018–1046` (insertion point :1037, marker :1040); block (a) row 9; anchor 929 in §4.1. |

---

### 2. THE GAPS

#### G-1 — Two hunks have no row in the block, and the block asserts closure
Anchors **6** and **8** are in §4.1's verified list. They are H1a (`PREREG_v30a_DIFF.md:65`, insert after PREREG.md line 6) and H1b (`:85`, insert the block after line 8). **Neither has a row in (a), (b), (c) or (d).** The block's own closure sentence, `K2_AMENDMENT_LEDGER.md:495`:

> "the clauses it inserts are those in (c) and no others; the pointers are those in (d) and no others."

An `**Amendment status:**` line inserted into the registered header where no registered sentence is replaced is (c)'s own definition of *Inserted*. Either add a row, or add one sentence to the block excluding header apparatus from the enumeration. **The artifact's §4 does not raise this.**

#### G-2 — §AB is nowhere in the verification record, and applied text depends on it
`SCHEMA_SET_FINAL.md:1461` heading: *"§AB — THE v30a AMENDMENTS-BLOCK RECORDING TEXT (revised; **drafted, not applied**)"*. `K2_AMENDMENT_LEDGER.md:427` places it "at applied lines 41–53" and says the block "replaces applied lines 15–39" — **both are scratch-copy coordinates, not coordinates in the pristine 1,099-line target.** Against pristine `PREREG.md`, §AB (`SCHEMA_SET_FINAL.md:1471–1512`) must be an explicit part of the insertion after line 8. §4.1's anchor list, placement list and cross-reference list **never mention §AB**, and no hunk number is attached to it in §3/§4/§5.

This is load-bearing, not cosmetic. §13c-P's **applied** paragraph, `SCHEMA_SET_FINAL.md:1445`, ends:

> "The registered relationship between this sentence and §7.4's scope-eligibility definition (line 830) over the same state **is recorded in the v30a amendments block** and is not changed by the exception."

If the block hunk quotes only the 68 lines between `<!-- K2-BLOCK-BEGIN -->` and `<!-- K2-BLOCK-END -->` (`K2_AMENDMENT_LEDGER.md:429–498`), **§AB is missing and that applied sentence points at nothing** — and §3 item 6's claim ("§AB records it as a defect explicitly not resolved") is false of the file as applied. **NOT ESTABLISHED; verify before signing.**

#### G-3 — Line 915 carries TWO applied texts; §5's C4 tells the applier to expect one
C4 says: *"expect ONE hunk at line 816, not two … Ledger convention, **mirroring line 915**."* True at 816 (`SCHEMA_SET_FINAL.md:1310`, SC-13c's marker is "None — insertion, not supersession", so only §13c-P exists). **False at 915.** SC-6 supplies both:
- Marker — `SCHEMA_SET_FINAL.md:532–533`: "**§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED.** §8.2's list is the *not-run* subset and stays correct as far as it goes…"
- Insertion text — `SCHEMA_SET_FINAL.md:536` header, body `:538–544`.
- SC-6's insertion point itself orders them, `SCHEMA_SET_FINAL.md:519–522`: *"where marker M2 below is already placed at that site, **the insertion follows M2**."*

Block (b)'s 915 row = the marker; (d)'s 915 row = the insertion text. **An applier following C4 drops SC-6's §8.2 marker M2.** Correct C4.

#### G-4 — Nothing amends `PREREG.md` line 449, and no source calls that deliberate
`K1_SCHEMA_CLAUSES.md:903`, row 28:

> "§A.5: line 449's semantic-ambiguity clause **does not fire** | **NOT COVERABLE** | **FINDING F-1.** … disposing of it requires an explicit class C amendment of `PREREG.md` line 449. Until then §10.2's branch is live."

Repeated at `K1_SCHEMA_CLAUSES.md:1179`; still carried open at `SCHEMA_SET_FINAL.md:2216` item 2(c). Line 449 is cited by **applied** text — `SCHEMA_SET_FINAL.md:1095`, inside SC-13a's marker: *"where §6.2 line 449's ambiguity…"*. The block has no row for 449; §4.1 never verifies it. This is **the one GATE-CRITICAL row the schema set knowingly leaves uncovered**, and the artifact's §3 "deliberately absent" list (items 1–7) omits it entirely. It should be item 8 there: the ambiguity branch stays live by design, which is the whole reason SC-13a–c exist.

#### G-5 — SC-13b(b1)'s STOP fires today; that is a signature decision, and it is not in §5's A-list
`SCHEMA_SET_FINAL.md:2216` item 2(d): *"the N4 instance-data residue (**SC-13b(b1)'s STOP for the label-availability detector today**)."* The applied text, `SCHEMA_SET_FINAL.md:1218–1219`:

> "**If any governed detector's declared labelled-unit set is empty, the criterion is not discharged and the outcome is STOP.**"

Signing SC-13b registers a STOP already tripped for one governed detector on the present declaration. **Nothing in A1–A5 mentions it.** This belongs in section A ("cannot be settled at application"), not in D or E.

#### G-6 — Line 570 is named by SC-13b's marker and is not verified
`SCHEMA_SET_FINAL.md:1206`: *"The registered lines it relies on — **816, 830, 570** — stand byte-exact and are cited."* §4.1's cross-reference list is `117, 759, 760, 791, 820, 830, 1024, 1039` — **570 absent**. It does exist (`PREREG.md:570`, the `not_applicable` state definition). Secondary: `SCHEMA_SET_FINAL.md:2173` records the sentence is itself imprecise — *"'830, 570 … are cited' while the clause cites §6.6 by section — apparatus, pre-existing, left as is."* Neither fact is in the artifact's D-list.

#### G-7 — Line 446 is asserted by applied marker text and never verified
SC-4's marker, `SCHEMA_SET_FINAL.md:344–345`: *"**§6.2 line 446 — NOT AMENDED.** The manifest requirement stands…"*. The claim is true (`PREREG.md:446` is the ground-truth-column-DAG manifest bullet), but 446 appears in **none** of §4.1's three lists, in breach of the artifact's own stated discipline.

#### G-8 — H6 and H7 are displaced exactly as H5 is, and §3 names only H5 and H8
- `SCHEMA_SET_FINAL.md:334–335` — SC-4: *"After `PREREG.md` line 464 … carrying H1 hunk **H6**'s placement."*
- `SCHEMA_SET_FINAL.md:931` — SC-12: *"Carries H1 hunk **H7** essentially unchanged."*

H6 (`PREREG_v30a_DIFF.md:249`, INSERT 37 lines after 464) and H7 (`:333`, INSERT 17 lines after 1035) sit in H1's summary table (`PREREG_v30a_DIFF.md:13–28`). If either is carried alongside its schema replacement, **line 464 and line 1035 each receive two operative blocks** — precisely the double-targeting failure §3 item 2 and C2 raise for H5. Of H1's eleven hunks the artifact accounts for eight; **H6 and H7 are unaccounted for, and H1a/H1b only implicitly via anchors 6 and 8.** Add them to §3.

#### G-9 — "37 of 37 hunks" is stated against a 33-line list with no mapping
§4.1 asserts 37 verified and then prints 33 line numbers. The block holds exactly 37 rows, which invites a 1:1 reading — contradicted by G-1 (two hunks with no rows) and G-3/C4 (rows that split or collapse). Three anchors carry more than one hunk (**1035** → SC-12, SC-13b, SC-13c; **464** → SC-4, SC-5; **856** → SC-6's semantics block and SC-12's §7.7 pointer) and each is listed once. **§4.1 needs an explicit hunk-number → anchor-line table.** As it stands the 37 is unauditable.

#### G-10 — `PREREG_v30a_DIFF.md` is load-bearing and is not an authoritative source
Five of nine (a) rows have their **operative replacement text nowhere in SSF, K2 or Y3**: line 445 → H2 (`PREREG_v30a_DIFF.md:133`), 450 → H3 (`:171`), 451 → H4 (`:196`), 992 → C1 (`:401`), 1022 → C2 (`:423`). SC-2's marker says so at `SCHEMA_SET_FINAL.md:190–191`: *"Their markers stand as H1 wrote them and are cited, not re-drafted."* The artifact cites the file only in A5. **§4.6 records no byte-check of those five texts** against `PREREG_v30a_DIFF.md`, though every SSF clause got one. Add the check, and add the file to the source list.

#### G-11 — Anchors 466 and 998 are placement bounds mislabelled as anchors
`466` is SC-5's *upper* bound (`SCHEMA_SET_FINAL.md:455`: "before line 466's parenthetical"). `998` is the last row of §10's phase table — where C1's retained-verbatim superseded row must land, because a multi-line block cannot sit inside a markdown table cell. Both belong in §4.1's placement list. The C1 case needs one sentence besides: block (a)'s 992 row promises retention "**at its site**", and the retained row physically lands six lines below it, past the table.

#### G-12 — `T2_DEVIATIONS_D002_TIMING.md` is a live SC-14 deliverable, already overruled
§4.2's four-stale-file count is correct, but the artifact treats all four as inert scratch. T2 is not scratch: it is a staged `DEVIATIONS.md` **D-002** entry whose entire content asserts SC-14 fires (`T2:17, 25, 27, 29` — *"the consequence of §10.1's firing is deferral of release, not termination"*). `errata/Z1_Z2_Z5_RECORDS.md:104–107` has already ruled the opposite: *"**No `DEVIATIONS.md` entry** … `DEVIATIONS.md` stays 0 bytes until D-001 lands."* T2 is withdrawn in substance; **nothing in the artifact says so**, and the author signs PREREG + declaration in the same ceremony that would otherwise land it.

---

### 3. What I checked and found intact

- All 37 block rows resolve to a line the artifact verified. **No orphaned row.**
- All 17 SSF `INSERTION POINT` paragraphs resolve to an anchor in §4.1. **No missing insertion point** (except §AB, G-2).
- `grep -c SC-14` = **0 / 0 / 0** across SSF, K2, Y3 — independently re-run this pass. Two further mentions exist outside `amendment/` and are *correct*: `ceremony/X4_REGENERATION_REQUIREMENTS.md:107` ("SC-14 is **WITHDRAWN** and must appear nowhere") and `errata/Z1_Z2_Z5_RECORDS.md:26` ("SC-14 is withdrawn … The v30a diff loses one hunk and gains none").
- §4.5's guaranteeing sentence is at `K2_AMENDMENT_LEDGER.md:495` and reads verbatim as quoted, inside the markers. **Confirmed.**
- §4.4's finding confirmed independently: `SCHEMA_SET_FINAL.md:937` still says *"the §7.7 pointer H1 drafts as hunk **H8** after line 856"*; the redraft exists only at `Y3_WAIVED_ENTRY_CONDITION.md:184`.
- Every anchor line I sampled (6, 8, 95, 97, 99, 205, 220, 222, 266, 431, 441, 445, 446, 449, 450, 451, 459, 461, 464, 466, 468, 480, 570, 816, 818, 830, 855, 856, 892, 915, 929, 961, 992, 998, 1022, 1030, 1031, 1033, 1035, 1036, 1050, 1054) exists and reads as its clause claims. `wc -l PREREG.md` = **1099**. **No anchor failure found.**

### 4. Ranked

**Fix before the diff goes to the author:** G-2 (§AB may be missing outright), G-3 (C4 will make an applier drop marker M2), G-1 (two unenumerated hunks against a closure claim), G-8 (H6/H7 double-application risk).
**Add to §5 section A — decisions the signature makes:** G-5, G-4.
**Add to §4 — verification record:** G-6, G-7, G-9, G-10, G-11.
**Add to §3 or §5 D:** G-12.

---

## ANCHOR CRITIC — independent re-verification against `PREREG.md` (1,099 lines, sha256 `f0a8f001…c7cc6`, `git diff --stat prereg-v30 -- PREREG.md` empty)

Every line below was read with `sed -n 'Np' "C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/PREREG.md"`. Nothing was created, edited, or run against git state.

---

## 1. Anchors that are correct — count

**53 distinct pristine line numbers verified; 53 correct; 0 text mismatches.**

- **33 anchor lines** (the artifact's §4.1 list): `6, 8, 97, 99, 205, 220, 222, 266, 431, 441, 445, 450, 451, 459, 461, 464, 466, 468, 480, 816, 855, 856, 892, 915, 929, 961, 992, 998, 1022, 1030, 1035, 1050, 1054` — all exist, all match the text the clause claims is there.
- **20 placement / cross-reference lines** also read and confirmed: `93, 95, 101, 117, 207, 212, 213, 214, 225, 226, 246, 443, 452, 453, 470, 570, 759, 760, 780, 781, 791, 818, 820, 830, 857, 894, 909, 962, 999, 1000, 1023, 1024, 1031, 1033, 1036, 1039, 1048, 1049, 1055, 1056`.

Byte-exact containment checks that pass:
- `PREREG.md:461` (92 chars) verbatim in `SCHEMA_SET_FINAL.md` (SC-3's retention).
- `PREREG.md:816` (174 chars) verbatim in `SCHEMA_SET_FINAL.md` (SC-13c(c2)'s quote).
- `PREREG.md:855` (119), `:929` (187), `:1030` (128) verbatim (whitespace-normalised across the blockquote wraps) in `SCHEMA_SET_FINAL.md`.
- `PREREG.md:992` (526) and `:1022` (214) verbatim in `K2_AMENDMENT_LEDGER.md` §9.1/§9.2 retention blocks.

Foundational counts re-run independently: `waived` occurs **exactly twice** (855, 1035); `v30a` occurs **exactly once** (line 95, `prereg-v30a`); `§2.9` is **vacant**; `SC-14` returns **0** in all three operative sources; `SC-12(w)` returns 6 / 3 / 12; SC-7's negative-claim grep returns **exactly one** hit (line 896); lines 459–462 are **exactly four** criteria, so SC-13a's "§6.2's four acceptance criteria" is correct.

Section membership confirmed against the heading index: 816 ∈ §7.2.1 (802–821); 855–856 ∈ §7.7 (849–882); 892 ∈ §7.8; 915 ∈ §8.2 (913–916); 929 ∈ §8.3 (917–932); 961 ∈ §8.6 (959–964); 992 ∈ §10; 1022 ∈ §10.1 (1016–1027); 1030–1035 ∈ §10.2 (1028–1045); 1048–1054 ∈ §11 (1046–1057); 266 is the last line of §2.8 (254–267), 268 is the closing `---`.

## 2. Anchors where quoted text does NOT match the file

**None.** No anchor claim in the artifact or in the three operative sources misquotes `PREREG.md`.

Three citations are **sentence-quotes, not line-quotes**, and will return **zero** matches under the full-line convention SSF lines 82–83 mandates. Not mismatches; applier hazards:

| Site | Source quotes | File line actually reads |
|---|---|---|
| 441 (SC-10) | `"The descriptive proof count of §6.2 is the sole reported fixture outcome…"` | line begins `The fixture's AUC figures are provenance —` ; the quoted sentence is the **third** sentence of the line |
| 892 (SC-11) | `"Conformance cases contribute to no detection metric…"` | `**Conformance cases contribute to no detection metric.** Under a too-permissive…` — the `**` are dropped in the quote |
| 99 (SC-9) | `the class C "discovered after the affected detector already exists" paragraph` | `**A class C change discovered after the affected detector already exists** cannot be made…` — fragment is byte-exact, the line is not |

## 3. Anchors naming a line outside 1..1099

**None.** Every number cited (min 6, max 1056) is in range.

## 4. Collisions, and the order required

Ordering below is as pinned by `K2_AMENDMENT_LEDGER.md` **Part A** (lines 113–150), whose "Applied lines" column records the CI-executed placement in `applied\PREREG.md`.

| Site | Hunks sharing it | Required order |
|---|---|---|
| header | R01 (status line, after 6), R02 (block, after 8), R03 (§AB, same site) | R01 → R02 → R03. **Line 6 must stand byte-exact** — K2 line 407: "line 6 is untouched so `_prereg_version()` still reads 30" |
| 97 / 99 | R04 (marker after 97), R05 (SC-9 after 99) | R04 shifts the file above R05's anchor; re-derive |
| **451** | **R13 (H4 REPLACES 451) + R14 (SC-2 inserts after 451)** | **R13 first (A552–A555), then R14 (A557).** After R13 lands, a full-line match on line 451's registered text returns **0** → applier refuses. Worse under substring fallback: R13 retains line 451 **verbatim in a blockquote at A553**, so a loose match lands SC-2 *inside a superseded-text block* |
| **after 464** | **three:** R15 (criterion-1 marker, A604), R17 (SC-4, A606–A637), R18 (SC-5, A639–A651) | marker → SC-4 → SC-5, all before line 466 |
| after 480 | R20 (marker A681), R21 (SC-8 A683–A695) | marker → clause |
| **855 / 856** | **three:** R23 (REPLACES 855, retains it verbatim at A1075), R24 (SC-6 block A1077–A1087), R25 (§7.7 pointer A1089) | R23 → R24 → R25. Same retained-verbatim substring hazard as 451 |
| 915 | R27 marker (A1166) **and** R27 pointer S2(i) (A1168) | marker → pointer |
| **after 1035** | **three:** R32 (SC-12 A1307–A1317), R33 (SC-13b A1319–A1327), R34 (SC-13c A1329–A1347) | SC-12 → SC-13b → SC-13c, all before 1036, all at three-space indent (verified present on 1035 via `cat -A`) |
| **after 1054** | **three:** R36 item 8 (A1368), R35 item-3 marker (A1370), R36 items-1–7 marker (A1372) | **item 8 FIRST**, then the two markers beneath the list. Reversed, item 8 lands below the markers and breaks §11's enumeration |
| 992 / 998 | R29 rewrites the Gate cell of row 992; §9.1 retention goes after 998 | rewrite → retention |
| 1022 / 1023 | R30 rewrites 1022; §9.2 retention goes beneath it, before item 4 at 1023 | rewrite → retention |
| 461 | R16 (SC-3) **only** | H5 confirmed absent: block table (a) maps 461 → SC-3; Part A R16 names H5 as drafting basis only |
| 816 | R22 **only** (A1033, between 816 and 818) | one hunk |

## 5. Findings against the artifact

**F-1 (material). §4.1's "Three placements are NOT fixed by the sources" is false for two of the three, and the artifact's chosen lines contradict the pinned ones.** It is true of `SCHEMA_SET_FINAL.md` alone; `K2_AMENDMENT_LEDGER.md` Part A — a source the task names authoritative — pins both:

- **hunk 5** (SC-1's §2.3 `column_roles` marker): artifact says *after line 212*. **K2 R06 pins it at "A275 (placed after the table, i.e. after pristine line 213)"**, and adds "SSF fixes no placement line for SC-1's two markers; **the CI run chose this one** (K2-O2)." Off by one.
- **hunk 6** (SC-1's §2.4 formula marker): artifact says *after line 225, recommended*. **K2 R07 pins it at "A285 (placed after line 220)"**, with K2-O3: the marker "sits inside the 220–222 range it marks (between the formula and the bullets); cosmetic, no text displaced." The artifact moves it **five lines**, from between the formula and the bullets to below the last bullet.
- **hunk 13** (SC-2 after H4's block): the artifact's resolution is correct, but the source did fix it — R13 = A552–A555 (four lines), R14 = A557.

Consequence: hunks 5 and 6 as drafted place SC-1's markers at sites other than the ones §8.3's CI record was measured on — compounding the staleness the artifact itself records at §4.7.

**F-2. C4's "mirroring line 915" is backwards.** At **816** exactly one hunk exists (R22, pointer only). At **915** exactly **two** exist (R27: marker at A1166 **and** pointer S2(i) at A1168). An auditor told to expect one hunk at 915 comes up one short — the opposite of the error C4 is warning about.

**F-3. R02's anchor descriptor is loose in a way that misplaces the block.** Part A R02 reads "Header, after line 8 (`**Registration:** …`)", but its applied range is A15–A39 — i.e. **after the `---`** (pristine line 10), not immediately after line 8 (pristine 9 = blank, 10 = `---`). Taken literally, "after line 8" inserts the entire v30a amendments block **inside the front matter, above the rule**. The artifact lists 8 as an anchor and lists neither 10 nor 12.

**F-4. §4.7's "differ in six places" undercounts.** Re-diffed: the ledger's §8.2 block is **68** content lines, `_K2_BLOCK_TEXT.md` is **67**, and `difflib` reports **seven** change hunks, not six (the extra one is the §11 item-8 (c) row). The substantive conclusion — §8.3's CI record (`fb171ed8…788bc`, 136/1) was measured on the older block and on a `PREREG.md` carrying neither SC-12(w) nor the line-929 hunk — is **CONFIRMED**.

**F-5. Hunk count NOT ESTABLISHED.** The artifact says 37. Part A is 36 rows, but R27 and R36 each carry **two** applied sites (38), plus the §8.3 line-929 hunk (no R-row) and the two §9 retention blocks at 998 and 1023 → **41** physical insertions/replacements. The artifact's §2 hunk list was not in the excerpt supplied, so which convention yields 37 cannot be checked. The **anchor set** it lists is nonetheless complete against Part A — no Part A surface lacks an anchor in the artifact's list.

**F-6 (confirms artifact D6, verbatim).** `K2_AMENDMENT_LEDGER.md` R25 still names the pointer's applied text as *"`waived` is defined in §10.2 (v30a)", with the residual-gap statement (no entry condition for the coverage state is defined by this registration)* — the sentence SC-12(w) falsifies. The redraft exists **only** at `Y3_WAIVED_ENTRY_CONDITION.md:184`; `SCHEMA_SET_FINAL.md:937` still routes the §7.7 pointer to H1 hunk H8. Without hunk 23 in the diff, the stale text is applied by default. Confirmed.

**F-7 (confirms artifact B3, verbatim).** `feature-cohort pair` occurs **exactly once** in `PREREG.md`, at **line 830** (§7.4). §7.2's unit table at lines 780–781 registers `EvidenceEvent` and `ReportedFinding`. SC-13a(a1)'s "the **feature-cohort pair** §7.2 registers as its runtime scoring unit" cites the wrong section.

**F-8 (confirms artifact B6).** `SCHEMA_SET_FINAL.md:131` — SC-1's clause text reads "**Six requirements follow**", a literal count of its own enumeration, in applied text, in the amendment whose block guarantees (K2 line 495) "Their number is read from the enumeration and is stated nowhere as a numeral."

**Verified absent, as required:** SC-14 (0 hits in all three operative sources; stale hits survive only in `T1_CRITERION_5_AMENDMENT.md`, `T2_DEVIATIONS_D002_TIMING.md`, `T3_CHAT_IDENTIFIER_SCAN.md`, `T4_WAIVED_SIDE_EFFECT_CHECK.md`). Neither §10.1 criterion 5 (line 1024) nor §10.2 criterion 5 appears in any block table or any anchor.