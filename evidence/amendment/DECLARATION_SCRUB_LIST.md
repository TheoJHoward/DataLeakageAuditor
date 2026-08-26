# ITEM H2 — DECLARATION SCRUB LIST

Target: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md`
(3,684 lines, read IN FULL this pass: lines 1–560, 560–1179, 1180–1799, 1800–2359, 2360–2939,
2940–3498, 3499–3685).

Reference: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md` (1,099 lines).
Sections read this pass for clause-matching: §0.2.1 (lines 60–111), §2 (169–307), §6.1–§6.6
(430–549), §7.2.1–§7.10 (820–903), §8 (907–961), §10 (985–1043), §11 (1046–1054).

**Nothing was edited.** This is a list for author approval. PREREG.md was not touched;
AVAILABILITY_DECLARATION.md was not touched; no git command was run other than none.

---

## 0. HEADLINE — READ BEFORE APPROVING H1

**The list is 138 passages: 102 RULE and 36 normative-sounding passages that survive the scope
test as INSTANCE. That is not "larger than a dozen or so." The RULE count alone is roughly an
order of magnitude larger.** (Counts machine-derived from the table below: 138 numbered rows,
102 marked RULE, 36 marked INSTANCE, 40 marked `HOME = NONE`.)

Four consequences the author needs before approving H1's diff:

1. **The declaration is currently carrying the substance of the amendment, not just its
   evidence.** §A (lines 751–1597) is 847 lines and contains the *operative new text* of every
   §6.2 amendment. §A.12 alone (lines 1525–1597, 73 lines) is a pure definition of a word used
   in PREREG.md line 1035 and line 855 — zero fixture content. §D.3 (3473–3488), §E
   (3490–3519) and §F.3 (3558–3604) are three further blocks of pure, fixture-independent rule.

2. **The declaration amends PREREG.md in more places than the walk admits.** The declaration's
   §A.11 line 1516 says "**Four amendments (445, 450, 451, 461).**" The scope test finds
   normative changes to at least **eleven** further registered surfaces that the walk does not
   list as amendments:
   §2.3 line 205 (`column_roles` semantics, and `at_bar_close` never scored against — rows 3,
   96); §2.4 lines 220–222 (a **positional** label horizon, a new unit — row 4); §2.3 lines
   190–197 (both-branch counts informational; the comparator restated — rows 72, 124); §7.7
   line 855 (a new coverage state `UNSCORED` — rows 46, 82); §8.6 line 961 (at least fifteen
   reporting obligations — rows 2, 10, 20, 47, 51, 60, 75, 77, 83, 87, 92, 93, 110, 111, 133);
   §0.2.1 lines 93–99 (supersession and interpretation rules — rows 9, 128); §11 item 3 line
   1050 (the tag-message hash count — row 126); §6.2's gate framing (a detector input surface
   and a sequencing rule — rows 129, 130); §6.4/§7.8 (an all-zero control — rows 134, 135);
   §6.1 lines 431–441 (a "declared non-gated diagnostic" body of data — rows 85, 123); and
   §10.2 line 1035 (the `waived` definition — rows 62–65).
   **Each is class C by PREREG.md line 93's own definition** ("a needed *new* branch, unit,
   denominator, coverage state, tier licence, or acceptance criterion").

3. **40 rows have NO home clause in PREREG.md at all** (column `HOME` = NONE; 39 of them RULE
   rows, plus row 138 whose R13 content has no home). H1's diff must *create* the clause, not
   amend one. If H1's diff only touches lines 445, 450, 451 and 461, then those rules —
   currently stated normatively in the declaration — will, after H1, be stated normatively
   *nowhere*, because under R20 the declaration is not a normative annex. **That is the single
   largest risk in this amendment and it is why this list is delivered before H1's diff is
   approved.** The full row list is §3; verbatim row ids:
   **3, 4, 7, 8, 9, 11, 18, 28, 35, 44, 46, 47, 58, 62, 63, 64, 68, 70, 72, 80, 82, 85, 87, 90,
   96, 101, 111, 113, 115, 117, 123, 124, 126, 128, 129, 130, 131, 134, 135, 138.**

4. **One self-consistency risk, flagged because it bears on whether §10.2's branch fires.**
   §A.5 (lines 1009–1016) reads PREREG.md line 449's semantic-ambiguity clause as NOT firing,
   on the ground that "documented-and-violated is not the same as undocumented." That reading
   *avoids* PREREG.md line 1033's obligation (pause runtime development, commit a class C
   replacement criterion before any development-corpus access). §D.3 (lines 3478–3482) — the
   declaration's own interpretation rule — says an interpretation of locked text "may resolve
   ONLY toward the STRONGER reading." A reading that switches off a floor is the weaker one on
   its face. The reading may well be right; but it is an *interpretation of locked PREREG text*
   living in the declaration, it is not in the four-amendment ledger, and it is exactly the
   shape §D.3 exists to police. It needs to be adjudicated in PREREG.md, not here.

**H1 cross-reference status: NOT POSSIBLE THIS PASS.** The delivery directory
`...\scratchpad\amendment\` did not exist when this item started (created by this item to hold
this file); no H1 diff, hunk list or draft exists at that path or anywhere under
`...\8b1d67a4-...\scratchpad\`. The sibling task output `...\7c596505-...\tasks\wnqornorz.output`
is 0 bytes and still running. Every RULE row below therefore names the PREREG.md clause it
*should* cite, and the `HOME` column flags whether such a clause exists. **Rows with
`HOME = NONE` are the gap candidates H1's diff must be checked against by name.**

---

## 1. METHOD

The scope test applied to every normative-sounding passage, verbatim from the working
resolution: **would it still be true for a DIFFERENT fixture? If yes it is a RULE (must move);
if no it is an INSTANCE (stays).**

Two refinements that did work in the hard cases:

- **A rule stated with fixture-specific tokens is still a rule.** §A.6.0's derivation rule
  (line 1052) says "carries the wall-clock `ts_floor` join." `ts_floor` is this fixture's
  column; *"REQUIRED iff the declared map declares the column violating on the scored side
  under the declared tie branch"* is the rule, and it is fixture-independent. The rule moves in
  its generic form; the `ts_floor` binding stays as the instance that satisfies it.
- **A count is an instance; the discipline that produces the count is a rule.** "N = 11" stays.
  "N is the length of the enumerated REQUIRED list, and no class may be stated as a bare count
  or defined as a residue" moves.

Columns: `#` · `§ / line range` · `passage` · `R/I` · `scope test in one line` · `PREREG clause
to cite` · `HOME` (EXISTS = a clause exists and must be amended; NONE = no clause exists, H1
must create one).

---

## 2. THE RULE TABLE — 101 rows

### Part I (lines 1–545)

| # | § / lines | Passage | R/I | Scope test | PREREG clause to cite | HOME |
|---|---|---|---|---|---|---|
| 1 | §1 / 142–148 | "the declaration states the measured boundary rather than the intended one" | **RULE** | Any reconstructed declaration faces documented-vs-measured divergence; the rule that the measured value governs is fixture-free | §6.2 line 447 (reconstruction rule) — add the measured-governs clause | EXISTS |
| 2 | §2 / 234–236 | "**Generation-naming rule (M1/N2), binding on every row count in this file:** whenever a lattice row count appears, name the count, the path, the generation and the sha256." | **RULE** | "name path + generation + hash with every row count" is a provenance obligation any fixture inherits | §8.6 line 961 (every published number states its provenance) | EXISTS |
| 3 | T2 addendum / 346–351 | "Every role below describes the RAW constructed column; the value FED to the models at row `T` is the lagged one" | **RULE** | Whether `column_roles` describes pre-lag construction or post-lag fed value is a semantics question for the registered vocabulary, not for this fixture | §2.3 line 205 (`column_roles` vocabulary) | **NONE** |
| 4 | §5 / 424–429 | "**AMENDED — label availability is POSITIONAL, not `T + h` seconds.** … `a(y_t)` = the realization time of the PAIRED ROW's mid — the `timestamp` of the row h POSITIONS after row `t`" | **RULE** | A positional label horizon is a **new unit** for §2.4's formula; true of any fixture whose labels come from `shift(-h)` | §2.4 lines 220–222 | **NONE** |
| 5 | §5 / 440–449 items 1–2 | "They are DECLARED … **They are IN the scored population.** They are not excluded, not masked, and not given a separate denominator." | **RULE** | A denominator rule for cross-boundary label rows holds for any fixture with session gaps | §7.4 lines 828–832 (eligibility denominators) + §2.4 | EXISTS |
| 6 | §5 / 450–453 item 3 | "**Findings on them are adjudicated by the declared map like any other row** … Being a cross-boundary row is, by itself, neither a licence for a finding nor a defence against one." | **RULE** | An adjudication rule for a row class, stated generically | §6.2 line 461 as amended (declared-map scoring) | EXISTS |
| 7 | §5 / 454–455 item 4 | "**No separate label-availability criterion is created for them.** This declaration adds no new gate criterion; §6.2's four criteria as amended in §A are the whole gate." | **RULE** | A constitutional statement about what a declaration may and may not create — fixture-free, and under R20 it is a PREREG statement by construction | §6.2 (criteria enumeration) + §0.2.1 line 93 | **NONE** |

### Part II preamble and §0 (lines 549–749)

| # | § / lines | Passage | R/I | Scope test | PREREG clause to cite | HOME |
|---|---|---|---|---|---|---|
| 8 | Pt II / 564–582 | "Working resolutions R14–R17 are DELTA-ISSUED and are NOT in the tail record … §D.3's interpretation rule binds them exactly as it binds the recorded ones." (same for S1–S4) | **RULE** | What authority an unrecorded working resolution carries is a registration-integrity question, identical for any fixture | §0.2.1 lines 93–99 + §11 line 1053 (`DEVIATIONS.md` append-only) | **NONE** |
| 9 | Pt II / 584–588 | "Where a later resolution supersedes an earlier one … the later one governs and the earlier text stands as the record." | **RULE** | A supersession rule over an append-only ledger; fixture-free | §0.2.1 lines 93–99 | **NONE** |
| 10 | §0.3 / 678–685 | "**Reading rule, binding on this file and on any gate report.** … **A measurement claim that names neither artifact is not auditable and may not be published**" | **RULE** | "every measurement claim names the artifact it was measured on, or it is not publishable" is provenance discipline, not a fixture fact | §8.6 line 961 | EXISTS |
| 11 | §0.4 / 730–739 | "That licence requires the two sides to differ in availability and in **nothing else**. **A column-set change is not an availability change.**" | **RULE** | The condition under which a pre/post delta may be read as an availability effect holds for any pre/post fixture | §6.2 lines 443–451 (acceptance fixture) | **NONE** |
| 12 | §0.1–§0.2 / 610–658 | Artifact A / Artifact B identities, column universes, the lattice bridge | INSTANCE | Names this fixture's two objects; false for any other fixture | — (stays) | — |

### §A — the conformance walk (lines 751–1597)

| # | § / lines | Passage | R/I | Scope test | PREREG clause to cite | HOME |
|---|---|---|---|---|---|---|
| 13 | §A.0 / 760–767 | PREREG lines 93 and 95 quoted verbatim, then: "Every AMENDED entry below is a class C amendment carried by this registration." | **RULE** (thin) | The verbatim quotes ARE citations and are fine; the *classification assertion* is amendment content and belongs in the v30a amendments block | v30a amendments block near the top of PREREG.md (per R20) | EXISTS |
| 14 | §A.1 / 780–782 + 818 | "**NEW:** the anchor is **retired and replaced** …" / "The `full` mode clause of line 445 is unaffected and stands." | **RULE** | *That line 445's registered pair and ±0.010 interval are retired, and that the replacement is the fixture's own recomputed trio*, is a change to registered text | §6.2 line 445 — inline | EXISTS |
| 15 | §A.1 / 786–793 | The LightGBM trio table (0.966244 / 0.931536 etc.) and its `f1\f1_results.csv` provenance | INSTANCE | These three pairs are this fixture's AUCs; false for any other | — (stays; §A.1's rule row above cites it) | — |
| 16 | §A.1 / 795–816 | "Why the old anchor cannot stand" — the three numbered reasons | INSTANCE | The arithmetic against 0.957/0.675 is this fixture's; the *rationale* is evidence for the rule, not the rule | — (stays as the amendment's evidence) | — |
| 17 | §A.2 / 834–841 | "**THIS COUNT CARRIES NO GATE ARITHMETIC (R11).** PREREG.md line 446 is a **manifest-content** requirement … **The criterion-1 denominator is a different object and derives from the DECLARED MAP**" | **RULE** | What line 446's count means, and that it is not the criterion-1 denominator, is a semantics rule for any fixture | §6.2 line 446 + line 459 — inline | EXISTS |
| 18 | §A.2 / 853–857 | "**The manifest is NOT edited.** … **Evidence artifacts are never adjusted toward a decision** (R13)." | **RULE** | A general integrity rule about measurement artifacts; nothing fixture-specific | §11 (registration integrity) + §6.4 (freeze/hash discipline) | **NONE** |
| 19 | §A.2 / 865–867 | "Nothing in the gate turns on the split. Flavor enters no criterion, no denominator and no count" | **RULE** | That DAG *flavor* carries no gate arithmetic is a semantics rule for line 446's manifest content | §6.2 line 446 | EXISTS |
| 20 | §A.2 / 876–878 | "**Any gate report quoting a leaking-source count must name which of the two scopes it counts under — that is a declared reporting obligation, not a convention.**" | **RULE** | A reporting obligation on gate reports generally | §8.6 line 961 | EXISTS |
| 21 | §A.2 / 828–832, 843–851, 869–876 | The count 25; the 7/18 vs 6/19 flavor split; the T4 22-column subset | INSTANCE | These are this manifest's numbers | — (stays) | — |
| 22 | §A.3 / 904–909 | "**OLD (registered, line 450) …** **NEW:** the contamination availability class is **recorded in this availability declaration**, which the tag message hashes as its sixth file, and is frozen at the tag. The manifest is not the locus and is not edited." | **RULE** | Where a registered element is *recorded* is a registration rule; any fixture with a two-artifact split hits it | §6.2 line 450 — inline | EXISTS |
| 23 | §A.3 / 929–932 | "It does not license recording any *other* registered manifest content outside the manifest: line 446's ground-truth DAG and independent-leak count remain manifest content" | **RULE** | The scope limit of the locus amendment is part of the amendment's operative text | §6.2 line 450 — inline | EXISTS |
| 24 | §A.3 / 888–893 | "**Declared class: AVAILABILITY VIOLATION BY FORWARD JOIN**" with its mechanism | INSTANCE | This fixture's contamination class; a different fixture has a different one | — (stays; this is exactly the content line 450 asks for) | — |
| 25 | §A.4 / 961–968 parts 1–2 | "**Locus moved.** The sliced variant is **not** part of the v30a Phase 0 acceptance fixture … **Obligation re-registered** … a **Phase 1 CI obligation, due at the first CI run that exercises the padded slicer**" | **RULE** | Moving a registered element between phases changes what the acceptance criteria are evaluated on — pure registration content | §6.2 line 451 — inline; §10 phase table line 992 | EXISTS |
| 26 | §A.4 / 969–974 part 3 | "**Its scoring rule is declared NOW, ex ante** … each slice is scored against the … cells it selects … **A slice of a CHARACTERIZED side is never treated as clean**, and a slice may not be reported as a pass on the strength of containing only unscored cells." | **RULE** | A slice-scoring rule; the artifact name is the instance, the rule is not | §6.2 line 451 — inline | EXISTS |
| 27 | §A.4 / 980–984 | "It does not permit the Phase 1 obligation to be discharged by a `DEVIATIONS.md` entry or by a working resolution … Dropping it later is a further class C amendment." | **RULE** | A discharge-prohibition on a locked obligation; fixture-free | §6.2 line 451 + §0.2.1 line 95 | EXISTS |
| 28 | §A.5 / 1009–1016 | "**SATISFIED — the clause does not fire, and the reason matters.** … **Documented-and-violated is not the same as undocumented**" | **RULE** | Whether line 449's ambiguity clause fires on documented-but-violated timing is an interpretation of locked text, true or false for every fixture alike | §6.2 line 449 (+ §10.2 line 1030–1035, whose branch it switches off) | **NONE** |
| 29 | §A.6 / 1034–1041 | "**The denominator derives from the DECLARED MAP … not from the manifest's construction classes** … The manifest's leak-source classification is provenance context and carries no gate arithmetic" | **RULE** | The definition of criterion 1's denominator is the criterion's semantics | §6.2 line 459 — inline | EXISTS |
| 30 | §A.6 / 1043–1045 | "**The three classes are mutually exclusive, exhaustive … and each is ENUMERATED BY NAME.** No class is defined as a residue and no class is stated as a bare count; a count that cannot be written out as a list is a count nobody can audit." | **RULE** | Partition discipline; "35" is the instance, the discipline is not | §6.2 line 459 — inline | EXISTS |
| 31 | §A.6.0 / 1052–1056 | The three iff-clauses: REQUIRED / OUT OF JURISDICTION / UNSCORED | **RULE** | **The item's own steer: the rule is fixture-independent, the enumeration is not.** Generic form: REQUIRED = declared violating by the map on the scored side under the declared branch; OOJ = declared availability-legal at the boundary under the declared branch; UNSCORED = degenerate-constant or gate-status EXCLUDED | §6.2 line 459 — inline (this is R11's own text, tail lines 3677–3682, which currently lives only in a working resolution) | EXISTS |
| 32 | §A.6.0 / 1062–1074 | "**Precedence when clauses conflict.** UNSCORED wins." | **RULE** | A precedence rule between class definitions; any fixture with a dual-satisfying column hits it | §6.2 line 459 — inline | EXISTS |
| 33 | §A.6.0 / 1075–1079 | "**'Same-row book/clock' is read as 'within-lattice book/clock', not literally single-row.**" | **RULE** | A reading rule fixing the class definition's edge | §6.2 line 459 — inline (+ §2.3 lines 190–197 for the tie basis) | EXISTS |
| 34 | §A.6.0 / 1080–1085 | "**'Unconstructible under T4' is read as 'gate status EXCLUDED under T4 applied to the gate-scored fixture'**, not as 'F2-rebuild-unconstructible'." | **RULE** | A reading rule fixing which unconstructibility counts; generic form: *reconstruction-limited unconstructibility never removes a column from the gate's arithmetic* | §6.2 line 459 — inline | EXISTS |
| 35 | §A.6.0 / 1087–1090 | "Any disagreement between the rule-derived class and the frozen class is a **stop-and-report**" | **RULE** | A verification obligation on the partition; fixture-free | §6.2 line 459 + §7.8 (conformance as regression) | **NONE** |
| 36 | §A.6.0 / 1142–1145 | "**If a future column changes construction … its class must be re-derived by this rule and the change recorded as an amendment** … the enumeration is the current output of the rule, not a substitute for it." | **RULE** | The rule/enumeration relationship and its amendment class | §6.2 line 459 + §0.2.1 line 93 | EXISTS |
| 37 | §A.6.0 / 1092–1137 | The 35-row rule-application table (column, rule-derived class, clause, frozen-at) | INSTANCE | The enumeration IS the fixture; the item names it as such | — (stays; cite the moved rule above it) | — |
| 38 | §A.6.1 / 1171–1174 | "A correct detector must produce at least one **primary** runtime finding attributed to each of the eleven, **on the side and in the instrument-months where the map declares the violation.**" | **RULE** | The side/cell qualifier *narrows criterion 1's satisfaction condition* — that narrowing is the rule; "eleven" is the instance | §6.2 line 459 — inline | EXISTS |
| 39 | §A.6.1 / 1184–1188 | "**an availability-class finding on its same-row `mid[t]` read is OUT OF JURISDICTION and does NOT satisfy this entry.** Naming the right column on the wrong ground does not satisfy criterion 1." | **RULE** | Generic form: *criterion 1 is not satisfied by column name alone; the finding must be on the ground the map declares* — a strengthening of line 459's own attribution clause | §6.2 line 459 — inline | EXISTS |
| 40 | §A.6.1 / 1149–1169 | The 11-column REQUIRED table with construction lines and governing map classes | INSTANCE | This fixture's denominator | — (stays) | — |
| 41 | §A.6.1 / 1189–1192 | "No MBO-derived column is in the list, and that is a scope fact, not an omission." | INSTANCE | True only because Phase 7 feeds no MBO columns | — (stays) | — |
| 42 | §A.6.2 / 1196–1198 | "**An availability-class finding on any of them is a FALSE POSITIVE.** They enter no criterion-1 denominator and carry no required finding." | **RULE** | The gate consequence attaching to the OOJ class is the class's definition | §6.2 line 459 / line 460 + §7.4 | EXISTS |
| 43 | §A.6.2 / 1214–1219 | "criterion 2 **cannot receive them** … A finding on one of them is a false positive **by this declaration**, recorded as such in the gate report, and it is **not converted into a criterion-2 failure**." | **RULE** | Creates a gate-report disposition ("declared false positive") that no PREREG criterion carries; scoping of criterion 2 is criterion 2's semantics | §6.2 line 460 — inline | EXISTS |
| 44 | §A.6.2 / 1221–1224 | "**An L2a label-base finding on them is neither credited nor penalized by this availability gate.**" | **RULE** | A jurisdiction boundary between two detector rows; fixture-free | §4.2 (L2a applicability) + §6.2 lines 459–462 | **NONE** |
| 45 | §A.6.2 / 1201–1212 | The 4 + 18 column lists | INSTANCE | This fixture's OOJ membership | — (stays) | — |
| 46 | §A.6.3 / 1228–1229 | "Requires no finding and forbids none; enters no denominator, contributes to no rate, and **cannot be reported as a pass**." | **RULE** | **This defines a new coverage state.** PREREG line 855's state list is `passed, failed, not_applicable, unsupported, could_not_run(reason), waived` — `UNSCORED` is not in it. Class C by line 93 verbatim | §7.7 line 855 (state table) + §8.2 line 915 | **NONE** |
| 47 | §A.6.3 / 1236 | "Must be named in the gate report as **EXCLUDED**, never as MISSED." | **RULE** | A reporting-vocabulary rule | §8.2 line 915 + §8.6 line 961 | **NONE** |
| 48 | §A.6.3 / 1239–1241 | "**It carries ONE gate class and one only** … a column carrying two frozen classes violates 'no field answers two questions'. Reinstating it changes the criterion-1 denominator and is class C." | **RULE** | One-class-per-column is a partition discipline; it already cites PREREG line 79 and should cite it *only* | §0.2.1 line 79 + §6.2 line 459 | EXISTS |
| 49 | §A.6.3 / 1242–1245 | "**These are cells, not columns**; because Phase 7 feeds no MBO column, none of the 35 fed columns is put into UNSCORED by them." | **RULE** (the cell/column distinction) | That UNSCORED exists at two levels, and a cell-level unscored never makes a column unscored, is structural | §6.2 line 459 / line 461 as amended | EXISTS |
| 50 | §A.6.3 / 1247–1255 | "**R11's third UNSCORED limb, read precisely.** … Reading §17's seven as gate-unscored would silently drop `dollar_volume_1s` and `tick_direction` out of the arithmetic" | **RULE** | A reading rule for the class definition (duplicate of row 34's generic form) | §6.2 line 459 — inline | EXISTS |
| 51 | §A.6.4 / 1257, 1266–1269 | "**PARTITION CHECK (must be reproduced by any gate report)**" / "a partition asserted but not shown is a partition nobody verified" | **RULE** | An obligation on gate reports; the 11/22/2/35 numbers are the instance | §6.2 line 459 + §8.6 line 961 | EXISTS |
| 52 | §A.6.4 / 1259–1266 | The count table 11 / 22 / 2 / 35 and the `total_fed_to_phase7` tie-out | INSTANCE | This fixture's partition | — (stays) | — |
| 53 | §A.6.5 / 1271–1388 | The whole SOURCE × GATE cross-tabulation, its 35 rows, its arithmetic, the two empty cells | INSTANCE | A consistency check on this fixture's two taxonomies; false for any other fixture. Its closing line "**§A.6.4's partition governs**" is a pointer, not a rule | — (stays) | — |
| 54 | §A.7 / 1398–1403 | "The manifest-clean set is the 4 clean columns … Neither weakens the criterion" | INSTANCE | This fixture's clean set and its two dispositions | — (stays; the dispositions themselves are rows 77–80) | — |
| 55 | §A.8 / 1415–1417 | "**NEW …** 'detector findings must match the declared per-side, per-class, per-instrument-month violation map; findings the map predicts are required, findings it excludes are false positives, cells the map does not cover are unscored.'" | **RULE** | **This is the amended criterion 3 itself.** Fixture-free in form; it is what criterion 3 now says | §6.2 line 461 — inline | EXISTS |
| 56 | §A.8 / 1431–1434 | "It does not lower the bar … It does not create an unscored escape hatch either: the 72 unscored cells are named as unscored, never as clean, and they license no pass. **The map is declared and frozen before any detector runs.**" | **RULE** | The amendment's scope limits and the ex-ante freeze condition are operative text | §6.2 line 461 — inline + line 480 | EXISTS |
| 57 | §A.8 / 1423–1429 | "What forced it" — M5, 18 of 48, 111,334 of 580,944 | INSTANCE | The measurement that forced the amendment; this fixture's | — (stays as the amendment's evidence) | — |
| 58 | §A.9 / 1444–1453 | "**SENTINEL STATEMENT.** … are **DATA CONTENT, not findings** … A detector that fires on the magnitude, the sign, or the 2^32 signature has produced a **false positive under criterion 4**" | **RULE** | Generic form: *an as-built defect present identically on both sides cannot differentiate them and must not fire the identity control*. The 4.29e9 magnitudes are the instance | §6.2 line 462 (criterion 4) + §6.11 (control runs) | **NONE** |
| 59 | §A.10 / 1477–1480 | "**N is 11**, and it is the REQUIRED list of §A.6.1, not the manifest's independent-leak count. **N = 25 is withdrawn as the gate's N**" | **RULE** (the identification) + INSTANCE (the value) | *That line 472's N is the REQUIRED-list length and not line 446's count* is the rule; 11 is the instance | §6.2 line 472 + line 459 — inline | EXISTS |
| 60 | §A.10 / 1481–1489 | "a report must say 'k of N = 11 REQUIRED columns'; must **separately report false positives on the 22 OUT OF JURISDICTION columns**; and must **separately report findings on the UNSCORED class, which are NOT false positives** … **Never fold any of the three classes into another, and never carry the false-positive consequence beyond the 22.**" | **RULE** | The structure of the gate report is fixture-free | §6.2 line 476 + §8.6 line 961 | EXISTS |
| 61 | §A.11 / 1498–1521 | The walk summary table and "**Four amendments (445, 450, 451, 461). NO registered §6.2 element is left NOT MET**" | **RULE** (ledger) | An amendment ledger is exactly what R20 puts in PREREG's v30a amendments block; and see §0 headline item 2 — **the count "four" is contradicted by rows 3, 4, 46, 49–52, 92, 94–97, 100** | v30a amendments block near the top of PREREG.md | EXISTS |
| 62 | §A.12 / 1546–1556 | The **DEFINITION** of WAIVED, limbs (i)–(v) | **RULE** | **Zero fixture content.** It defines a word in PREREG line 1035 and line 855. True verbatim for every fixture | §10.2 line 1035 — inline; §7.7 line 855 (coverage state) | **NONE** |
| 63 | §A.12 / 1558–1564 | "**WHAT INVOKING IT REQUIRES: nothing, because it may not be invoked.** … There is no procedure by which either runtime detector may be waived … Changing that requires amending line 1035 itself" | **RULE** | A prohibition over a locked floor; fixture-free | §10.2 line 1035 — inline | **NONE** |
| 64 | §A.12 / 1566–1592 | The seven "WHAT THIS DEFINITION DOES NOT PERMIT" items (not an escape hatch; does not reach other criteria; "experimental" ≠ "waived"; "no data" ≠ "waived"; a WR/DEVIATIONS entry cannot do it; per-combination waiving is waiving; nothing after tuning) | **RULE** | Seven scope limits on a definition of a registered word; every one fixture-free | §10.2 lines 1035–1039 — inline; item 4 also §7.7/§8.2 | **NONE** |
| 65 | §A.12 / 1594–1597 | "**Status:** class C amendment content added by v30a … by §D.3's rule it resolves toward the stronger reading" | **RULE** | Status and resolution direction of an amendment | v30a amendments block + §0.2.1 lines 93–95 | EXISTS |

### §§8–17 (lines 1599–3361)

| # | § / lines | Passage | R/I | Scope test | PREREG clause to cite | HOME |
|---|---|---|---|---|---|---|
| 66 | §8 / 1648–1655 | "**The exclusion is HARD** … **Any future use of it … changes the fixture the acceptance criteria are evaluated on, and therefore changes what a published number means. That is class C** … It may not be admitted by a DEVIATIONS entry, by an orchestrator decision, or by a working resolution" | **RULE** | *Changing the fixture the criteria are evaluated on is class C and cannot be done by a deviation or a working resolution* — fixture-free; the pc2 set is the instance | §0.2.1 lines 93–95 + §6.2 line 443 | EXISTS |
| 67 | §8 / 1603–1646 | Fixture identity, 64 parquets per side, RE-EVALUATE class, the recomputed trio, the 95/128 meta corroboration | INSTANCE | This fixture's identity | — (stays). **Flag:** "RE-EVALUATE class" is not registered vocabulary anywhere in PREREG.md — if it is meant to carry weight it is a rule with no home | — |
| 68 | §9 / 1664–1669 | "This is the **licence** for reading the pre/post AUC delta as a feature-availability-only effect — labels, label bases, and evaluation populations are identical across sides, so nothing but feature availability differs." | **RULE** (the licence condition) | *What must hold for a pre/post delta to be read as an availability effect* is a rule; the bit-exactness measurement is the instance | §6.2 lines 443–451 (acceptance fixture) | **NONE** |
| 69 | §10 / 1676 | "**This section states no rule.**" | INSTANCE | Correct as written and the model the rest of the file should follow | — (stays) | — |
| 70 | §10 / 1710–1719 | "**Corrected-vs-(t-1) is the LAG-IMAGE of contaminated-vs-T, not a third independent measurement** … Treating their agreement as independent corroboration would be double-counting one measurement" | **RULE** | An evidence-accounting rule: a lag-image is not an independent corroboration. Fixture-free | §8.6 line 961 + §7.5 (diagnostics) | **NONE** |
| 71 | §10 / 1680–1746 | The counts, the PRIMARY/cross-check table, the two off-by-one reconciliations | INSTANCE | This fixture's measurement record | — (stays) | — |
| 72 | §12 / 1918–1926 | "**The 49 exactly-equal events are NON-VIOLATIONS under the declared branch, and they enter no detection denominator.** Under `ties: available` a cell with `a(j,c) == d(i)` is available … They are published only as the both-branch disclosure, which is **informational**" | **RULE** (two of them) | (a) The first sentence **restates PREREG line 192's locked comparator** — a restatement, forbidden by PREREG line 77, must become a citation. (b) "both-branch disclosures are informational and no gate outcome may be computed from them" is a new rule | (a) §2.3 lines 190–193 — cite; (b) §2.3 + §8.6 — inline | (a) EXISTS (b) **NONE** |
| 73 | §12 / 1928–1944 | The 49 events, the T1-PRIMARY designation, the "contaminated-minus-1" qualifier on C4 | INSTANCE | This fixture's counts and artifact hygiene | — (stays) | — |
| 74 | §13(a) / 1960–1961 | "**Artifact: `n1\declared_map.csv`.** One row per scored cell, **schema** `side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag, missing_path`." | **RULE** (the schema) | *What a declared ground-truth map is* — its per-cell schema — is what amended criterion 3 scores against, for any fixture. The 984 rows are the instance | §6.2 line 461 as amended — inline | EXISTS |
| 75 | §13(a) / 1972–1982 | "**CLASS-SET RULE, binding.** `mbo_all_rows` is an **11th diagnostic class and is NOT one of the declared 10.** Any statement of the form 'max across classes' … **must name the class set it maximises over.**" | **RULE** | *Diagnostic classes are not declared classes, and every max names its class set* — fixture-free reporting rule; the class names are the instance | §8.6 line 961 | EXISTS |
| 76 | §13(a) / 1962–1970, 1984–1987 | 984 / 960 / 888 / 72 / 24; the declared 10 class names; the companion artifacts | INSTANCE | This map's contents | — (stays) | — |
| 77 | §13(b) / 1997–2004 | "**THE RANKING BELOW IS BY RATE** … **The metric is named because the rate order and the absolute-count order are different orders**, and any list of these cells that does not name its metric is unreadable." | **RULE** | *A ranking is quoted with its metric* — fixture-free | §8.6 line 961 | EXISTS |
| 78 | §13(b) / 2044–2051 | "**'Clean on both branches' is WITHDRAWN as a pass claim** … **Zero-over-scored-classes is not the same predicate as zero-over-the-declared-10** … **No row in this table may be quoted as a pass**" | **RULE** | *A measured zero over a partial class set is not a pass, and the scored-class count is named on every row* — fixture-free | §6.2 line 461 as amended + §8.2 line 915 | EXISTS |
| 79 | §13(b) / 2006–2042, 2053–2069 | The 18-row rate table, the 13 measured-zero rows, the 18+17+13=48 arithmetic | INSTANCE | This map's contents | — (stays) | — |
| 80 | §13(d)+§C.2 / 2134–2137, 2617–2619 | "**The predicate is checkable from the lattice alone — no event data.** That is what makes it usable as a **declared cohort definition** rather than as a post-hoc description." / "**Why this is checkable before any detector runs**" | **RULE** | *A declared cohort definition must be regenerable from the declared inputs alone, before any detector runs* — fixture-free; the predicate itself is the instance | §6.2 line 447 (evidence before tuning) + line 461 as amended | **NONE** |
| 81 | §13(d) / 2113, 2115–2132 | The predicate `floor(T_i)==floor(T_{i-1})`; 5,305,430/5,305,430; 7.94%; the −3 ns / −5 ns headroom | INSTANCE | This fixture's cohort | — (stays) | — |
| 82 | §13(g) / 2212–2216 | "**Gate consequence, declared:** an unscored cell **requires no finding and forbids none.** It enters no denominator, contributes to no rate, and **cannot be reported as a pass.** A gate report that counts the 72 as 'clean' … has converted absence of data into evidence" | **RULE** | The cell-level twin of row 46 — a new coverage state and its consequences | §7.7 line 855 + §8.2 line 915 + §6.2 line 461 | **NONE** |
| 83 | §13(g) / 2216–2223 | "**Whenever nq appears in any table in this file or in any gate output, it must carry the TRADES-CLASSES-ONLY label together with the correct reason**" | **RULE** (generic form) | *A partially-covered unit carries its coverage label and its reason on every appearance* — fixture-free; "nq" and "TRADES-CLASSES-ONLY" are the instance | §8.2 line 915 + §8.6 line 961 | EXISTS |
| 84 | §13(g) / 2193–2210 | The 72 cells, the missing path, the two out-of-path NQ MBO families | INSTANCE | This fixture's coverage hole | — (stays) | — |
| 85 | §13(h) / 2227–2229 + 2241–2250 | "**This subsection is NOT part of the gate. Nothing in it enters any acceptance criterion, any denominator, any rate, or the §D.1 freeze**" … "**Moving it into the acceptance denominator later is class C**" | **RULE** | *A declared non-gated diagnostic is a body of data with its own admissibility rules* — PREREG §6.1 enumerates five bodies of data and this is a sixth | §6.1 lines 431–441 (five bodies of data) + §0.2.1 line 93 | **NONE** |
| 86 | §13(h) / 2252–2323 | The X4 results, join soundness, day coverage, the premise correction | INSTANCE | This fixture's diagnostic | — (stays) | — |
| 87 | §13(i) / 2327–2333 | "**The obligation, stated first.** R17(ii) requires both maps to be published side by side with the delta explicit. **Neither replaces the other.**" | **RULE** | A publication obligation over a restricted re-aggregation; fixture-free | §8.6 line 961 | **NONE** |
| 88 | §13(i) / 2355–2359 | "**This justification makes no reference to what the restriction does to any count, and none may be added to it** … a restriction adopted for its effect on a number is a restriction shaped by that number — **the same failure PREREG.md line 480 forbids in the large**" | **RULE** | *A scope restriction is justified independently of its effect on the numbers* — a generalisation of line 480 to scope choices, fixture-free | §6.2 line 480 — inline extension | EXISTS |
| 89 | §13(i) / 2428–2436 | "**What the restricted map IS and IS NOT** … It is a **REPORTING object** … **It is NOT a second scoring key, and it changes no adjudication.**" | **RULE** | *A re-aggregation published for reporting is never a second scoring key* — fixture-free | §6.2 line 461 as amended + §8.6 | EXISTS |
| 90 | §13(i) / 2448–2452 | "**An all-zero return would have been a FINDING, not a pass**" | **RULE** | The special case of row 100's all-zero control; fixture-free | §7.8 + §8.6 (see rows 100–101) | **NONE** |
| 91 | §13(i) / 2335–2353, 2361–2426, 2438–2447 | The R17(i) column-universe box (13/11/9/1/1, MBO-fed 0 of 35); MAP 1 vs MAP 2 tables; the 18-cell table; the R17(iii) result | INSTANCE | This fixture's column universe and map | — (stays) | — |
| 92 | §13(j) / 2481–2502 | "**They must NEVER again be quoted as:** 1. Evidence about any fed column, in either direction … 2. Any criterion-1 arithmetic … 3. Any unqualified 'X of 48' headline … 4. Any unqualified 'max strict' or 'max equal' … **a peak is quoted with its class set AND its metric, or it is not quoted.**" | **RULE** (four of them) | Generic form: *a map class whose event source no fed column consumes may not be quoted as evidence about any fed column, in either direction; a headline names its class set; a peak names its class set and its metric* — fixture-free reporting rules binding any gate report | §8.6 line 961 — inline | EXISTS |
| 93 | §13(j) / 2514–2518 | "'the 35-column set' always means `ALL_L2_FEATURES` … **Any future re-derivation must name the constant, not the length.**" | **RULE** | *Name the constant, not the length* — a general anti-ambiguity rule; the two 35-sets are the instance | §8.6 line 961 | EXISTS |
| 94 | §13(j) / 2463–2479, 2504–2513 | "They STILL legitimately evidence" items 1–3; the `BOUNCE_FREE_FEATURES` trap quote | INSTANCE | What this fixture's MBO classes evidence | — (stays) | — |
| 95 | §C / 2527–2532 | "**Everything in this section is stated POST-LAG** … And **everything is stated SIDE-RELATIVELY** … **There is no side-independent list of leaking columns in this fixture, and writing one would be a category error.**" | **RULE** | *The criterion-1 violation set is stated post-lag and side-relatively; a side-independent list is a category error* — true of any pre/post fixture | §6.2 line 459 — inline | EXISTS |
| 96 | §C / 2534–2541 | "**The comparator, pinned.** … The **`at_bar_close` role … is an APPROXIMATION only**: it names where the value sits on the lattice, not when it became knowable. **`at_bar_close` is never scored against.**" | **RULE** | *What `at_bar_close` means relative to `at_source_timestamp`, and that a role is never the availability instant a comparator reads* — pure §2.3 vocabulary semantics, fixture-free, and **not in the four-amendment ledger** | §2.3 line 205 (+ lines 190–193) — inline | **NONE** |
| 97 | §C.1 / 2545–2585, §C.2 / 2589–2615 | The mechanism sentence, the (A)/(B)/(C) column tables, the cohort restriction, the 18 non-zero months | INSTANCE | This fixture's enumeration | — (stays) | — |
| 98 | §C.3 / 2640–2660 | "**These 27 constructions are not availability violations on either side.** That is the AVAILABILITY DECLARATION … **Its GATE CONSEQUENCE does not, so the consequence is stated PER CATEGORY below and no column carries two**" | **RULE** | *The availability declaration and the gate class are different objects, and no column carries two gate classes* — fixture-free | §0.2.1 line 79 + §6.2 line 459 | EXISTS |
| 99 | §C.3 / 2683–2733 (category definitions only) | Cat 1 "OUT OF JURISDICTION … an availability-class finding on any of them is a FALSE POSITIVE"; Cat 2 "**A column whose lag treatment is unresolved cannot be scored under ANY reading**"; Cat 3 "**OUT OF JURISDICTION is a gate class held by a fed column**; these are **not fed at all** and therefore hold **no gate class whatever** … Declaring them 'out of jurisdiction' would imply the gate adjudicates them and declines" | **RULE** | The category *definitions* are class semantics; every one is fixture-free. The names inside them are the instance | §6.2 line 459 — inline | EXISTS |
| 100 | §C.3 / 2758–2791 | "**What happens instead, declared:** 1. an availability-class finding on any of the 22 is a FALSE POSITIVE … not converted into a criterion-2 failure; 2. on the corrected side it is **also a criterion-3 failure**; 3. a LABEL-BASE finding belongs to **L2a** and is neither credited nor penalized; 4. the four manifest-CLEAN columns **DO route to criterion 2**" | **RULE** (four routing rules) | Routing rules between criteria and between detector rows; fixture-free | §6.2 lines 459 / 460 / 461 — inline | EXISTS |
| 101 | §C.3 / 2793–2803 | "**That character is assigned to L2a jurisdiction and is OUTSIDE this availability gate** … routing it here would let a label-base finding masquerade as an availability finding, corrupting both counts." | **RULE** | A jurisdiction boundary (duplicate of row 44); fixture-free | §4.2 + §6.2 | **NONE** |
| 102 | §C.3 / 2621–2635, 2662–2675 | The heading correction, the 27-column list, the "27 = 18 + 1 + 8" reconciliation, the retirement note | INSTANCE | This fixture's construction list and its retirement as a class claim | — (stays) | — |
| 103 | §C.4(a) / 2815–2818 | "**A dead-zero column cannot carry an availability finding for an availability reason**, and leaving it in the denominator would make criterion 1 unsatisfiable for a reason unrelated to detection. It is declared out, before any run, and must be named in the gate report as EXCLUDED rather than as MISSED." | **RULE** | *A degenerate-constant column is excluded pre-run and reported EXCLUDED, never MISSED* — fixture-free; `buy_volume_10s` is the instance | §6.2 line 459 + §8.2 line 915 | EXISTS |
| 104 | §C.4(b) / 2824–2829 | "**This is staleness, not unavailability** — a value from the past is always available, and the comparator asks whether a cell was knowable by `d(i)` … **this quirk licenses NO finding**" | **RULE** | *Staleness is not unavailability* — a comparator semantics rule, exactly §2.1's territory | §2.1 lines 171–175 + §2.3 lines 190–193 | EXISTS |
| 105 | §C.4(c) / 2836–2841 | "**The discrepancy is recorded as UNRESOLVED and the column's gate status is EXCLUDED** … no finding on it counts for or against any criterion. If it is ever reinstated the lag question must be resolved first, and reinstatement changes the criterion-1 denominator — class C." | **RULE** | *An unresolved construction/lag question forces EXCLUDED, and reinstatement is class C* — fixture-free | §6.2 line 459 + §0.2.1 line 93 | EXISTS |
| 106 | §C.4 / 2843–2845 | "The exclusions are **declared here, pre-run**, and are frozen at the tag by §D.1." | **RULE** | *Exclusions are declared before any run and freeze at the tag* — fixture-free ex-ante rule | §6.2 line 480 + §11 | EXISTS |
| 107 | §C.5 / 2886–2906 | "(c) … **criterion 1 is not satisfied by column name alone** … (d) … **It must be recorded on its own ground, not credited to the column's REQUIRED status.** Three characters, three dispositions, no double-counting" | **RULE** | *A required finding must be on the ground the map declares; a finding on another ground is recorded on its own ground* — fixture-free (duplicate of row 39, stated in full here) | §6.2 line 459 — inline | EXISTS |
| 108 | §C.5 / 2923–2930 | "**A column's gate class is a statement about what the gate does with a finding, and the gate needs exactly one answer per column.** … It appears once in §A.6.4's partition, in REQUIRED, and in no other class" | **RULE** | The definition of what a gate class *is*; fixture-free (the R16 comparison table is the instance) | §0.2.1 line 79 + §6.2 line 459 | EXISTS |
| 109 | §C.5 / 2849–2884, 2908–2922 | `vwap_distance`'s identification as the sole MIXED column, its two grounds traced to line numbers, the R16 comparison table | INSTANCE | This fixture's only dual-ground column | — (stays) | — |
| 110 | §14 / 3066–3104 | "**FORBIDDEN USE — §13(j)'s rules, applied to THIS side verbatim.**" items 1–5 | **RULE** (restatement) | Same four rules as row 92 plus the `trades_buy` three-live-classes note; fixture-free. **Restating them a second time is itself the duplicated-authority failure PREREG line 77 forbids** — after H1 both copies must be citations of one PREREG clause | §8.6 line 961 — cite, do not restate | EXISTS |
| 111 | §14 / 3105–3118 | "**BINDING — the EX-NQ figures are the summary-level peaks.** … The nq figure may be published **only as a per-cell entry** carrying its label and its coverage-artifact reason, **never as the restricted contaminated headline.** *(this clause governs SUMMARY-LEVEL quotation, where a single peak must be named and the coverage artifact must not be it)*" | **RULE** | *A summary-level peak excludes cells whose figure is a coverage artifact; per-cell and summary-level quotation obey different rules* — fixture-free; the es/nq cells are the instance | §8.6 line 961 — inline | **NONE** |
| 112 | §14 / 2956–3064, §14.1 / 3124–3207 | PROFILE 1 / PROFILE 2, the delta tables, the provenance block, the 48-cell table and its arithmetic | INSTANCE | This fixture's contaminated profile | — (stays) | — |
| 113 | §15 / 3247–3256 | "**Claims split per R4:** Timing-structural — **SUPPORTED** … Value-dependent — **QUALIFIED**" | **RULE** | *A claim resting on a column with an as-built value defect splits into timing-structural (supported) and value-dependent (qualified)* — an evidence-accounting rule, fixture-free | §8.6 line 961 + §3 (tiers/evidence) | **NONE** |
| 114 | §15 / 3215–3245, 3258–3278 | The two defects with line citations, the C1 INHERITED verdict's three chains, the C5 WRAPPED verdict, the 7 affected columns | INSTANCE | This fixture's as-built record | — (stays) | — |
| 115 | §16 / 3287 | "Assumptions the declaration **RELIES ON that no archive record can verify**; recorded as such" | **RULE** (the category) | *An assumption the record cannot verify is recorded as documented-unverifiable and named wherever it is relied on* — fixture-free; PREREG §2.8 says the declaration is unverifiable but registers no such record | §2.8 lines 254–266 + §6.2 line 447 | **NONE** |
| 116 | §16 / 3289–3314 | Items 1–3 (the 35-column assumption, the PC2 runtime inputs, the unhashable `C:\MBO_data` copies) | INSTANCE | This fixture's three unverifiables — **the item's own steer: documented-unverifiable assumptions stay** | — (stays) | — |
| 117 | §17 / 3323–3324 | "selection or renaming only (**nothing synthesized**)" as the projection rule | **RULE** (thin) | A method rule for a projection; fixture-free in form | §6.2 (fixture construction) | **NONE** |
| 118 | §17 / 3326–3357 | 28 constructible / 7 unconstructible with reasons; determinism hashes; the self-consistency result | INSTANCE | This fixture's projection result | — (stays) | — |

### §§D–F and the tail (lines 3363–3685)

| # | § / lines | Passage | R/I | Scope test | PREREG clause to cite | HOME |
|---|---|---|---|---|---|---|
| 119 | §D.1 / 3367–3369 | "**At the moment the `prereg-v30a` tag is signed, the following become LOCKED, and any subsequent change to any of them is a class C amendment requiring a further amended registration**" | **RULE** | *What freezes at a tag, and that moving it afterwards is class C* — pure registration-integrity, fixture-free | §11 lines 1046–1054 + §0.2.1 line 95 | EXISTS |
| 120 | §D.1 / 3374–3387 item 2 | "What freezes is the **three-class partition** … each class **as an enumerated list of column names, not as a count** … **A gate report that cannot reproduce this sum … has not scored this fixture.**" | **RULE** | The freeze-object definition (lists, not counts) and the gate-report obligation are both fixture-free; the eleven names are the instance | §11 + §6.2 line 459 | EXISTS |
| 121 | §D.1 / 3391–3396 item 3 | "**Every other gate-consumed number in this file.** Specifically and exhaustively: …" | **RULE** (the freeze scope) | *Every gate-consumed number freezes at the tag* is the rule; the enumerated list of this fixture's numbers is the instance | §11 + §6.2 line 480 | EXISTS |
| 122 | §D.1 / 3397–3403 items 4–5 | The class-set rule and the four §6.2 amendments + the §10.2 definition freeze | **RULE** | Freezing rule-objects; and note item 5 names **five** objects while §A.11 says "four amendments" | v30a amendments block + §11 | EXISTS |
| 123 | §D.1 / 3404–3406 item 6 | "**NOT frozen** … *provided* they are never moved into an acceptance denominator — which is class C" | **RULE** | The admissibility rule for non-gated numbers; fixture-free | §6.1 lines 431–441 + §0.2.1 line 93 | **NONE** |
| 124 | §D.1 / 3408–3411 | "**Both-branch counts are INFORMATIONAL ONLY** … **No gate outcome may be computed from them**, and reporting a pass or fail under the non-declared branch is out of specification." | **RULE** | Fixture-free rule about the non-declared tie branch | §2.3 lines 190–197 + §8.6 | **NONE** |
| 125 | §D.1 / 3413–3418 | "**Consequence of PREREG.md line 480's locked ordering** … A number discovered to be wrong after a fixture result has been observed **is not corrected in place** — it goes through PREREG.md line 99's route" | **RULE** (restatement) | This **restates** PREREG lines 480 and 99. Under PREREG line 77 a restatement is a protocol failure — it must become a bare citation | §6.2 line 480 + §0.2.1 line 99 — **cite, do not restate** | EXISTS |
| 126 | §D.2 / 3433–3435 | "**DECLARED: the `prereg-v30a` tag message carries SIX hashes** — those five, inherited and recomputed at their v30a state, **PLUS the SHA-256 of this availability-declaration file itself.**" | **RULE** | **A declaration cannot amend the registration's own integrity chain from outside it.** PREREG §11 item 3 registers *three* hashes; line 97 says "both"; the executed v30 tag carries *five*; this declares *six*. The count is a registration rule and must be settled inside PREREG.md | §11 item 3 line 1050 + §0.2.1 line 97 — inline | **NONE** |
| 127 | §D.2 / 3422–3431, 3451–3471 | The verbatim five-line v30 tag block; "Why the sixth"; the two discharged lock-time obligations | INSTANCE | The read state of this repository's tag and this pass's discharges | — (stays as the evidence for row 126) | — |
| 128 | §D.3 / 3478–3488 | "**A decision-log interpretation of locked text may resolve ONLY toward the STRONGER reading. Any interpretation that weakens a locked obligation — narrows a denominator, exempts a column, softens a criterion, admits an excluded set, converts a required finding into an optional one, or converts an unscored cell into a pass — is a class C amendment and may not be recorded as a working resolution.**" | **RULE** | **Zero fixture content.** A constitutional rule over the amendment machinery; true verbatim for every fixture and every future working resolution | §0.2.1 lines 93–99 — inline | **NONE** |
| 129 | §E / 3492–3513 | "**At gate time a detector receives exactly two things, for ONE SIDE AT A TIME** … **Nothing else.** In particular, a detector **NEVER** receives … the paired side … the other side's stored predictions … **the declared ground-truth map** … **Why the map in particular must be withheld.** … the gate would measure retrieval rather than discrimination." | **RULE** | **The gate protocol's input surface is fixture-free.** Any acceptance-fixture gate run has the same surface; the artifact names are the only instance content | §6.2 lines 453–462 (gate framing) + §6.11 (control runs) — inline | **NONE** |
| 130 | §E / 3515–3519 | "**Corollary — one side at a time is a hard sequencing rule, not a convention.** … A single run given both sides does not satisfy any of them, however its outputs are partitioned afterwards." | **RULE** | A sequencing rule over the criteria; fixture-free | §6.2 lines 459–462 — inline | **NONE** |
| 131 | §F.1 / 3543–3549 | "**Consequence, declared as a method rule:** any claim … of the form 'every X in the archive' … rests on a filesystem walk and **must not be re-verified with a default-excluded search. A negative result from such a search is not evidence of absence.**" | **RULE** | A survey-method rule; the 37-vs-119 measurement is the instance, the rule is general | §6.4 (generation/verification protocol) + §8.6 | **NONE** |
| 132 | §F.1 / 3532–3541 | The 37 vs 119 table and the `c1\tagger_survey_capture.txt` citation | INSTANCE | This archive's measurement | — (stays as the evidence for row 131) | — |
| 133 | §F.2 / 3551–3556 | "Every number written in this pass was read from a named artifact … **Where a quantity depends on a class set, a side, a boundary, or a lattice generation, all of those are named at the point of use**" | **RULE** | A provenance discipline for published numbers; fixture-free | §8.6 line 961 | EXISTS |
| 134 | §F.3 / 3561–3574 | "**THE RULE, declared as binding method.** **Any aggregate that reports zero violations … MUST be automatically cross-checked against its source artifact before that result may be written down** … **On mismatch the check RAISES — it does not print a warning** … A zero that survives the check is reportable, and must be reported **with the check named**" | **RULE** | **Zero fixture content.** A control over aggregation, stated as method | §7.8 (conformance/regression) + §8.6 + §6.2 — inline | **NONE** |
| 135 | §F.3 / 3592–3604 | "**SCOPE: THIS BINDS FUTURE GATE REPORTING, NOT ONLY THIS FILE.** … the gate report's per-criterion counts and its false-positive tallies; any re-derivation of …; any statement that a column, class, cell or criterion is clean." | **RULE** | The rule **says of itself** that it binds beyond this file — which is precisely the test for something that cannot live in a fixture declaration under R20 | §7.8 + §8.6 — inline | **NONE** |
| 136 | §F.3 / 3576–3590 | "**THE PROVENANCE, RECORDED HONESTLY** … that near-miss was caught by visual inspection of a CSV row … **performed by luck.**" | INSTANCE | The account of one pass on this fixture — and the evidence that makes row 134 credible | — (stays; **keep it here, it is exactly the kind of thing a declaration is for**) | — |
| 137 | §18 / 3606–3645 | The element-to-evidence index | INSTANCE | An index of this file's own sections and artifacts | — (stays; will need row-by-row rewording once §A/§D/§E/§F rules move) | — |
| 138 | Tail / 3649–3685 | Working resolutions R1–R13 verbatim (R9's criterion-3 text; R11's three-class rule; R13's evidence-artifact rule) | INSTANCE (as a **record**) | The tail is an append-only record of what was resolved and stays byte-identical. **But the normative content of R9 (criterion 3) and R11 (the three-class rule) currently has no home other than this record** — after H1 the tail must be the record *of* a rule that lives inline in PREREG.md, never the rule's only statement | R9 → §6.2 line 461; R11 → §6.2 line 459; R13 → §11/§6.4 | EXISTS / **NONE** (R13) |

---

## 3. GAP REGISTER — the 40 rows with `HOME = NONE`

Row ids, machine-extracted from the table above:
**3, 4, 7, 8, 9, 11, 18, 28, 35, 44, 46, 47, 58, 62, 63, 64, 68, 70, 72, 80, 82, 85, 87, 90,
96, 101, 111, 113, 115, 117, 123, 124, 126, 128, 129, 130, 131, 134, 135, 138.**

These are the rows H1's diff must be checked against **by name**. Each is a rule currently
stated normatively in the declaration for which **no PREREG.md clause exists to carry it**. If
H1's diff does not create the clause, the rule has no normative home after R20.

Grouped below by the PREREG surface that would have to receive it. A row appears in more than
one group where it lands on more than one surface, so the group tallies exceed 40.

**A. §0.2.1 — the amendment machinery (5 rules).** Rows 8 (delta-issued WR authority), 9
(supersession), 128 (**§D.3's interpretation rule — the single largest pure-rule block outside
§A.12**), 18 (evidence artifacts never adjusted toward a decision), 138-R13.

**B. §11 — registration integrity (2 rules).** Rows 126 (**the SIX-hash declaration — four
different hash counts are now in play: PREREG line 1050 says three, line 97 says "both", the
executed v30 tag carries five, the declaration declares six**), 18.

**C. §2.3/§2.4 — the availability primitive (4 rules).** Rows 3 (column_role describes pre-lag
construction), 4 (**positional label horizon — a new unit for §2.4's formula, and not in the
four-amendment ledger**), 96 (**`at_bar_close` is never scored against — not in the ledger
either**), 124 (both-branch counts informational).

**D. §7.7/§8.2 — coverage states (6 rows).** Rows 46 and 82 (**`UNSCORED` is a new coverage
state; PREREG line 855's list does not contain it, and line 93 names a new coverage state as
class C verbatim**), 47 (EXCLUDED-not-MISSED vocabulary), 62/63/64 via §A.12 (`waived` as a
coverage state as well as a floor term).

**E. §10.2 — the replacement-criterion floor (4 rows).** Rows 62, 63, 64 — the whole of §A.12's
definition, prohibition and seven scope limits. Also row 28 (§A.5's reading that switches off
line 449, and therefore line 1033's branch).

**F. §6.2 — gate framing (11 rows).** Rows 7 (the declaration creates no criterion), 11
(column-set change is not an availability change), 44 and 101 (L2a jurisdiction boundary), 58
(the sentinel), 68 (the feature-availability-only licence), 129 and 130 (**§E's input surface
and the one-side-at-a-time sequencing rule**), 35 (rule-vs-frozen stop-and-report), 80
(declared cohort checkable pre-run), 117 (selection/renaming-only projection).

**G. §8.6 — reporting provenance (4 rows).** Rows 70 (lag-image is not corroboration), 87
(both-maps publication obligation), 111 (summary-level vs per-cell peak quotation), 113 (R4's
claim split).

**H. §6.1/§6.4/§7.8 — bodies of data and method controls (7 rows).** Rows 85 and 123 (**the
"declared non-gated diagnostic" — a sixth body of data against §6.1's five**), 90, 131 (survey
method), 134 and 135 (**the all-zero control, which says of itself that it binds future gate
reporting**), 115 (the documented-unverifiable record).

---

## 4. WHAT STAYS — the declaration after the scrub

For the author's picture of the end state. If every RULE row moves and is replaced by a
citation, the declaration keeps:

- Part I §§1–7 as the **measurement record** and the **declared values** (the boundary
  `floor(t-1)+1s`, `bar_duration` 1 s with its five caveats, the bar-close semantics, the
  per-column roles, the label base/horizon/delay, `ties: available`, the remaining-elements
  list) — with the generation-naming rule, the pre-lag/post-lag semantics and the positional
  label formula lifted out as citations.
- The frozen T2 addendum block and its supersession note.
- §0's two-artifact identification and its claims-to-artifact table.
- Every measured number, table and enumeration in §§8–17, §B, §C.1/§C.2, §13(b)–(j), §14/§14.1.
- The 35-column partition **as an enumeration**, the 984-row map **as contents**, the 11
  REQUIRED names, the 22 OOJ names, the 2 UNSCORED names, the 72 unscored cells.
- §16's three documented-unverifiable assumptions **in full** (the item's own steer).
- §F.3's near-miss provenance narrative (row 136) — the evidence that makes the rule credible,
  which belongs with the fixture, not with the specification.
- The frozen working-resolution tail, unchanged, as the record.

That is still a large and load-bearing file. What it stops being is the place where the
programme's rules live.

---

## 5. LIMITS OF THIS PASS

1. **H1's diff was not available** (see §0). No hunk cross-reference was possible; the `HOME`
   column is this item's own reading of PREREG.md, not a check against H1's output.
2. **No file was edited.** PREREG.md, AVAILABILITY_DECLARATION.md, DESIGN.md and HISTORY.md are
   untouched; no git command was run; the archive was not read from.
3. **Line ranges are as-read this pass** against a 3,684-line
   `AVAILABILITY_DECLARATION.md` (277,411 bytes, mtime 2026-08-13 18:05). If H1 or any other
   item edits the declaration before this list is applied, every range must be re-derived.
4. **The RULE/INSTANCE calls on rows 13, 61, 117 and 138 are the least certain.** Row 13 is a
   thin assertion wrapped around correct citations; row 61 is a summary whose substance lives
   in rows 14–65; row 117 is a one-clause method rule that may be judged fixture-local; row 138
   is a frozen record whose *content* is rule but whose *status* is record. Each is flagged in
   place.
