All ranges verified mechanically against the file and against `_K1_population_FROZEN.json`; all hunk anchors verified byte-exact against `PREREG.md`. Verdicts for entries 14a–25.

## Range and partition check

Independent scan of `SCHEMA_SET_FINAL.md` for blockquote runs and fenced blocks returned, in my span, exactly: `687–702, 708–719, 723–759, 785–824, 848–852, 856–883, 910–912, 916–953, 984–1023, 1035–1071, 1097–1102, 1106, 1113–1117`. These match the manifest's stated anchors and the frozen population's idx 14–26 line pairs with no discrepancy. **Total runs in the whole file: 64** — the manifest's coverage proof (33 + 31 = 64) checks out.

**No block in my span is missing from the manifest.**

**14a–14d partition of parent run 687–702:** sub-ranges 687–689 / 690–691 / 693–697 / 699–702. Nothing double-counted; the only lines not claimed are **692** and **698**, each a bare `>` separator carrying no text. Content-complete. Note that 689→690 has *no* `>` separator, so 687–691 is a single markdown paragraph in the source — the two markers there are glued together, which is precisely the boundary failure the manifest exists to correct.

## Per-entry verdicts

| # | Verdict |
|---|---|
| 14a → H19 | **AGREE** |
| 14b → NO HUNK | **DISAGREE — it is H37** |
| 14c → H37 | **AGREE** |
| 14d → H3 | **AGREE** |
| 15 → H38 | **AGREE** |
| 16 → H19 | **AGREE** |
| 17 → H4 | **AGREE** |
| 18 → H8 | **AGREE** |
| 19 → H9 | **AGREE** |
| 20 → H28 | **AGREE** |
| 21 → H24 | **AGREE** |
| 22 → H35 | **AGREE** |
| 23 → H35 | **AGREE** |
| 24 → H27 | **AGREE** |
| 25 → H27 | **AGREE** |

**14a (687–689) → H19.** Block reads `**§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED.**`. H19 is `insert` at 480, and its `what_changes` states: "The marker '§6.2 line 480 — v30a, EXTENDED NOT SUPERSEDED' is placed at line 480's site". Site matches the marker's own self-declared site. Anchor at `PREREG.md:480` verified byte-exact.

**14b (690–691) → DISAGREE.** The manifest says NO HUNK and §C-1 asserts "The §11 hunks are H37 … and H38 …; **neither carries this marker**." That is false on H37's own text. H37's `what_changes` reads:

> "Beneath §11's list, after a blank line, **two marker blocks are placed**: '§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT' **and '§11 items 1–7 — v30a, EXTENDED'.** Items 1-7 all stand byte-exact, item 3 included."

H37 names this block verbatim and places it at the site the block itself names (§11's list, beneath line 1054). By the manifest's own decisive test — a marker belongs to the hunk acting at the site it names — 690–691 belongs to **H37**, alongside 14c. §B's row "H37 | 1050 | §A-14c **only**" is wrong for the same reason and should read §A-14b + §A-14c. Consequence if uncorrected: C-1 proposes drafting a new hunk or deleting the ledger row "§11 items 1–7 | extended by item 8", either of which would duplicate or delete text H37 already lands.

Two things are genuinely true and should survive the correction: (i) SC-8's own INSERTION POINT prose at L682–683 enumerates only **two** accompanying markers ("one beneath §11's list (item 3's file set), one after `PREREG.md` line 97"), omitting this one; (ii) H37's `operative_text` does not contain it. So the right finding is *"carried by H37's `what_changes`, absent from H37's `operative_text` and from SC-8's insertion-point enumeration"* — a text-field defect, not a missing hunk.

**14c (693–697) → H37.** AGREE — named verbatim in the same `what_changes` quoted above; site is §11 item 3, `PREREG.md:1050` (`3. **SHA-256 of PREREG.md, DESIGN.md, and HISTORY.md as committed**…`), verified.

**14d (699–702) → H3.** AGREE. H3 `what_changes`: "A marker block, '§0.2.1 line 97 — v30a, SUPERSEDED AS A COUNT, NOT AS A REQUIREMENT', is placed after line 97". `PREREG.md:97` contains "both file hashes in the tag message" — the exact numeral the block supersedes.

**15 (708–719) → H38.** AGREE. H38 is `insert` at 1054; `PREREG.md:1054` is item 7 and 1055 is blank, so item 8 is a pure append. H38's `operative_text` is the block's text verbatim under the header `[INSERTION TEXT — §11 item 8, after PREREG.md line 1054 (item 7) — S2(ii)]`.

**16 (723–759) → H19.** AGREE. SC-8 declares two insertion points; the clause itself goes to point 1 (line 480), point 2 is item 8 (entry 15). H19 `what_changes`: "…and the clause 'The freeze, and what "declared ex ante" requires — v30a [SC-8]', limbs (a)-(f), is inserted after it."

**17 (785–824) → H4.** AGREE. Source INSERTION POINT at L776 says "After `PREREG.md` line 99 … before line 101's 'Membership in A or B must be citable'". H4 is `insert` at 99 and its `what_changes` names line 101's text as the following line. `PREREG.md:101` confirmed.

**18 (848–852) → H8.** AGREE. Marker names "§6.1 line 431 heading and table"; H8 is `marker` at 431, anchor `### 6.1 Five bodies of data`, verified.

**19 (856–883) → H9.** AGREE. H9 `insert` at 441, anchor is §6.1's closing "The descriptive proof count of §6.2 is the sole reported fixture outcome…" — which is exactly the insertion point named at source L841–842. Correctly distinguished from H8 (the marker at 431) despite both being SC-10.

**20 (910–912) → H28.** AGREE. Block is headed "INSERTION TEXT — §8.6, after `PREREG.md` line 961 — S2(iii)"; H28 is `insert` at 961. Correctly *not* given to H24, SC-11's other hunk.

**21 (916–953) → H24.** AGREE. H24 `insert` at 892, anchor "Conformance cases contribute to no detection metric" = §7.8's closing paragraph, matching source L899–900.

**22 (984–1023) → H35.** AGREE. Source L972 gives the insertion point as "After `PREREG.md` line 1035"; H35 is the SC-12 hunk at 1035. Distinguished correctly from H34 (SC-13b) and H36 (SC-13c), which share the 1035/1036 site — H35's `what_changes` fixes the order: "SC-12's block is written first at this site; SC-13b then SC-13c follow it."

**23 (1035–1071) → H35.** AGREE, and this is the entry most at risk of being mis-sited, so the settling quote matters. H35's `what_changes` ends: "…and — **new at DELTA R35 B3 — limb SC-12(w) with sub-limbs (w1)-(w7), the entry condition for §7.7's `waived` coverage state.**" The competing candidates are ruled out on site: H23 (`insert` 856) carries only the one-paragraph §7.7 pointer, whose full text its `what_changes` quotes and which is *not* this block; H27 (`replace` 929) is SC-12(w)'s *second* insertion point, declared as such at source L1073. The limb text lands at 1035 with SC-12.

**24 (1097–1102) → H27.** AGREE. Block is the retained-v30 marker at §8.3 line 929; H27 is `replace` at 929 and its `what_changes` says the v30 bullet "is retained verbatim at the site in a SUPERSEDED BY v30a block, marked NOT operative, with the recovery command `git show prereg-v30:PREREG.md`." H27's `anchor_text` is byte-identical to `PREREG.md:929`.

**25 (1106) → H27.** AGREE. Single-line block is the replacement bullet adding `waived` to the failure set; H27's `what_changes`: "§8.3's third assertion bullet is replaced so the failure set becomes `unsupported`, `could_not_run`, or `waived`." Two blocks to one hunk here is correct and is the shape §C-3 declares.

## Separate finding — the hunks file, not the manifest

The manifest is right, but it is right *against* the `operative_text` fields, and an applier that reads `operative_text` instead of `what_changes` will misplace registered text. In my span:

- **H19.operative_text over-captures the whole 687–702 run** — all four markers, including item 3's and line 97's — then the clause. Applying it verbatim lands the §11 item-3 marker and the §0.2.1 line-97 marker at **line 480**.
- **H3.operative_text and H37.operative_text both contain the full SC-8 clause (723–759) and neither contains the marker each is supposed to place.** Applying them verbatim lands SC-8's clause a second and third time, at lines 97 and 1050, and places no marker at either.
- **H35.operative_text stops at 1023** — verified: `"(w) ENTRY CONDITION"` and `"(w7)"` are both absent from the 3,163-char field. The entire SC-12(w) limb block (1035–1071) is missing.
- **H27.operative_text contains only the marker (1097–1102)** — the operative bullet at 1106 is absent, so the assertion at line 929 would be marked superseded and never replaced.

The last two are exactly the two blocks §C-4 says K4 names, so the manifest already knows; but the first three are in my span and are not flagged anywhere I could find. The invariant worth stating for the applier: **`what_changes` is the assignment authority; `operative_text` is unreliable in at least H3, H19, H27, H35 and H37.**

==============================================================================
## Verdict: entries 26–33 — **8 AGREE, 0 DISAGREE**, with two hunk-side defects flagged (both are defects in `_X5_hunks_v2.json`, not in the manifest).

**Files**
- Manifest: `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\BLOCK_MANIFEST.md`
- Source: `...\scratchpad\amendment\SCHEMA_SET_FINAL.md`
- Hunks: `...\scratchpad\amendment\_X5_hunks_v2.json`
- Target: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`

---

### Coverage of my line span — clean

I enumerated every blockquote run and fenced block in lines 1108–1576 independently of the manifest. Exactly **eight** exist, and their ranges are byte-identical to the manifest's and to `_K1_population_FROZEN.json` idx 26–33:

`fence 1113–1117 · quote 1145–1170 · quote 1174–1232 · quote 1268–1335 · quote 1373–1469 · fence 1490–1492 · fence 1498–1502 · quote 1526–1573`

**No block in my span is unlisted.** No range is off by a line. The nested `>>` quotation of PREREG line 816 at SSF 1388–1389 is correctly absorbed into the 1373–1469 run rather than counted as a ninth block.

---

### Per-entry findings

**26 · 1113–1117 → APPARATUS — AGREE.**
The fence is a verbatim re-quotation of *already-registered* PREREG.md lines 759, 760 and 1039. I diffed all three against the target: identical. Introduced at SSF 1110 as *"Instance record (apparatus, not applied)"*. There is nothing to put into PREREG.md — the lines are already there and no hunk amends them. Had any hunk claimed this block it would have duplicated registered rows. Correctly unclaimed.

**27 · 1145–1170 → H33 (1030, replace, SC-13a) — AGREE, and this is the run most likely to be mis-split.**
H33's `operative_text` opens with the literal tag `[SUPERSESSION MARKER]` followed by this block, then `[THE CLAUSE]` followed by entry 28's block. Whitespace-normalized containment: **exact**.

This run *names* three other sites — line 1022, line 816, §6.2's four criteria — and superficially looks like a sixth multi-marker run. It is not, and the manifest is right not to split it, because every one of those references is **negative**: "**Line 816 is not superseded**"; "**§6.2's four acceptance criteria are not amended by these clauses**"; and at 1167–1168 "**is not** amended by these clauses: §10.1 scores a *third-party tool*, SC-13a scores *this project's* runtime detectors." A statement that a site is *not* amended creates no marker at that site. All three paragraphs land at 1030.

One reconciliation worth recording, since it reads as a contradiction on its face: the marker says line 1022 "is **not** amended by these clauses", while **H31** (insert 1022) and **H32** (replace 1022) do touch 1022. No conflict — the amendments block in H2 lists `§10.1 line 1022 — kill-gate criterion 3 | superseded, **consequential to line 461**`. It is amended by SC-3, not by SC-13a–c. The marker's qualifier "by these clauses" is doing real work.

**28 · 1174–1232 → H33 — AGREE.**
Anchor verified against the target: PREREG.md line 1030 reads exactly H33's `anchor_text` — *"2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**"* — and that same sentence is quoted inside entry 27's marker as the retained v30 text. Site is unambiguous. Containment in H33's `operative_text`: exact.

**29 · 1268–1335 → H34 (1035, insert, SC-13b) — AGREE.**
Source insertion point at SSF 1254–1257: *"Pure insertion ... between line 1035's paragraph and line 1036 ... after the "waived" definition SC-12 inserts at the same anchor — SC-12 is applied first, and SC-13b follows SC-12's inserted block."* H34's `prereg_line` is `1035 (after SC-12's inserted block; before line 1036)`, `clause: SC-13b`. Not H35 — H35 is the same anchor but `clause: SC-12`, and takes entries 22/23. H34's `operative_text` is this block prefixed by `[THE CLAUSE]` and nothing else (5759 vs 5746 chars). Anchor line 1035 verified in the target.

**30 · 1373–1469 → H36 (1036, insert, SC-13c) — AGREE, and the two-insertion-point split is correct.**
SC-13c declares **two** sites (SSF 1356–1363). The manifest sends the clause body to H36 and the pointer paragraph to H20, which is the only correct split. H36's `operative_text` is **exactly** this block, 7965 chars to 7965 — nothing added, nothing dropped. Its anchor is PREREG line 1036 (criterion 3) with insert-before semantics; verified in the target. The nominal "1036" vs the source's "still between line 1035's paragraph and line 1036" is the same site stated from the other side, and H36's own parenthetical restates the source verbatim.

**31 · 1490–1492 → APPARATUS — AGREE.**
The fence content is byte-equal to PREREG.md line 816 and byte-equal to H20's `anchor_text` (I compared both; `True` on each). SSF 1494 settles it: *"**SUPERSEDED TEXT: none.** Line 816 is unchanged; the paragraph is inserted after it, before line 818."* It is match-target, not payload. The manifest's invariant is about text *put into* PREREG.md, and this block is never put in. Correctly unclaimed — though note it is not inert: it is the verification copy of H20's anchor, so a check that deletes apparatus wholesale would strip H20's anchor evidence.

**32 · 1498–1502 → H20 (816, insert) — AGREE on the site. ⚠ But H20 cannot currently deliver it.**
H20's `what_changes` describes the paragraph at SSF 1500 clause by clause and matches it. It is the only hunk in the file whose `prereg_line` mentions 816. Site is right.

**Defect: `H20.operative_text` is the empty string** (`len 0`). Every other hunk in my scope carries its payload. This block at 1498–1502 is therefore the *sole* copy of the §13c-P pointer text, and any applier reading `operative_text` inserts nothing at line 816. That is precisely the failure H20's own `justification` warns about — *"Without this paragraph the kill criterion is silently disarmed at the point of implementation"* — arriving through the hunks file rather than through the registration. This is a hunk-file defect, not a manifest error, but it is in the same class as §C-1 and should be repaired before application.

**33 · 1526–1573 → H2 (8, insert) — AGREE.**
H2's own `clause` field settles the site: *"K2 §8.2 — the v30a amendments block (replaces H1b / applied lines 15–39; **§AB at applied 41–53 kept byte-exact**)"*, and `what_changes` adds *"followed after one blank line by §AB (the recorded-defect paragraphs on lines 816/830) byte-exact."* No other hunk touches lines 6–8. §AB is a component of the amendments block, and the amendments block lands at line 8.

**Caveat, and why it resolves.** `H2.operative_text` (12,445 chars) ends at *"…which is what the sliced-variant row of (a) does"* and does **not** contain §AB. I chased this, because SSF 1516 labels §AB *"revised; drafted, **not applied**"* with four enumerated changes, which raised the possibility that H2 would carry a stale §AB forward. It does not: I extracted §AB from `_K2_verify\PREREG.md` lines 83–95 and diffed it against SSF 1526–1573 — **identical** under whitespace normalization. The revision has already landed in the applied copy, so "kept byte-exact" is accurate as of now. (The truncated line dump in `_K2_diff_pristine_vs_applied.txt` A41–A53 shows spurious differences; that file clips long lines and is not usable for this comparison.)

Residual risk worth naming: H2 lands §AB by *carry-over*, not by restatement, so the assignment is only as sound as the applied copy staying in sync. An applier driven off `operative_text` alone drops §AB the same way it drops H20's paragraph.

---

### What I could not fault

Manifest §C-3's invariant holds in my span. Two blocks share H33 (27, 28); the marker and the clause land at one site in one `operative_text`, in that order. That is "one hunk per block", not "one block per hunk", exactly as declared. Every anchor I could check against the target — 816, 818, 1030, 1031, 1033, 1035, 1036, 759, 760, 1039 — is present and verbatim in the pristine `PREREG.md`.

==============================================================================
**SCOPE: manifest entries 1a–13 (SCHEMA_SET_FINAL.md lines 150–662). 19 entries checked against `_X5_hunks_v2.json` (38 hunks, H*n* = 1-based index), `_K1_population_FROZEN.json`, and `PREREG.md`.**

**RESULT: 17 AGREE, 2 DISAGREE (3d, 5). No unlisted block in the span. Three flags.**

---

## Range integrity — checked first

I recomputed every blockquote/fenced run in lines 89–1576 independently. In my span 150–662 there are **exactly 13 runs**, and they are exactly the 13 the manifest anchors: 150–159, 163–202, 228–232, 236–269, 293–301, 305–352, 376–380, 384–468, 496–534, 561–569, 573–578, 582–610, 642–662. Every one matches `_K1_population_FROZEN.json` idx 1–13 line-for-line. **Nothing in my span is unlisted, and no range is wrong.**

Partition checks on the multi-marker runs:
- **1a/1b** — 150–153 + 154–159 = 150–159. Clean. Line 153 is the `>` separator, carried in 1a. Two real paragraphs.
- **3a/3b/3c/3d** — 228–229 + 230 + 231 + 232 = 228–232. Clean. (One physical paragraph, four sentences, four sites — the split is by sentence, which is right here.)
- **7a/7b** — 376–378 + 379–380 = 376–380. Clean, but note this is **one unbroken paragraph** (`cat -A` shows no `>`-only line between 378 and 379), unlike 1a/1b. Immaterial: both halves go to the same hunk.
- **10a/10b** — 561–566 + 568–569 leaves **line 567 (`>`) unassigned**. Cosmetic only, but inconsistent with 1a, which absorbs its separator at 153. Worth one word in the manifest so a mechanical check doesn't trip.

---

## Per-entry verdicts

**1a (150–153) → H5 (205, marker). AGREE.** Block opens `**§2.3 line 205 (\`column_roles\`) — v30a, ADDED NOT SUPERSEDED.**`; H5's `prereg_line` is `205 (marker written at line 212, the end of its block)` and its `anchor_text` is the `column_roles` row, verified verbatim at PREREG.md:205. Site is explicit and matches.

**1b (154–159) → H6 (220–222, marker). AGREE — and this fixes a live duplication.** Block opens `**§2.4 lines 220–222 — v30a, PARTIALLY SUPERSEDED.**`; H6's `anchor_text` is `> **\`a(y_j) = label timestamp + label horizon + publication delay\`**`, verified at PREREG.md:220. Site match is exact. Note the correction being made: **H6's current `operative_text` is the whole SC-1 §2.9 clause (block 2), not this marker, and H5's current `operative_text` carries 1a *and* 1b.** Applied as the JSON now stands, 1b lands at 205 and the SC-1 clause lands twice (220 and 266). The manifest's split is right and repairs that.

**2 (163–202) → H7 (insert after 266, new §2.9). AGREE.** The source states its own insertion point at lines 142–143: *"New **§2.9**, inserted after `PREREG.md` **line 266** … before the `---` at line 268."* H7's `prereg_line` is `insert after 266 (before the \`---\` at 268); new §2.9`, anchor verified at PREREG.md:266. Decisive.

**3a (228–229) → H10 (445, replace). AGREE on site.** `**§6.2 line 445 — SUPERSEDED BY v30a** (H1 hunk **H2**)`; H10 replaces 445, anchor `- **Reference AUC:** 0.957 and 0.675…` verified. See **Flag 1**.

**3b (230) → H11 (450, replace). AGREE on site.** Names line 450; H11 replaces 450, anchor `- **Contamination availability class** recorded in the manifest.` verified. See **Flag 1**.

**3c (231) → H13 (451, replace). AGREE on site.** Names line 451 and cites *"(H1 hunk **H4**)"*; H13's `clause` field is literally `H4 (schema layer: SC-2(e), SC-3(f))` and it replaces 451. Correctly distinguished from H12, which *inserts after* 451. See **Flag 1**.

**3d (232) → H29 (992, replace). DISAGREE. It belongs to H30 (998).**
The block is `**§10 line 992 — CONSEQUENTIAL** (H1 **C1**): the Phase 1 gate cell reads on both retired objects.` — prose.
H29 is `operation: replace`, `prereg_line: 992`, and its entire `operative_text` is **a single markdown table row** (`| **1** | Availability model and profiles; … | 2–3 wknds | … snapshots hashed |`). Prose cannot be attached to a replaced table row; it splits the phase table.
The project has already ruled on exactly this. Triaged finding 45: *"Line 205 is a row of the `AvailabilityModel` table … A blockquote marker inserted after line 205 splits the table and breaks its rendering"* — status FIXED by *"R37/D4 — complete-block rule; markers written at 212, 462, 1054."* H5 obeys that rule (`205 (marker written at line 212…)`). Line 992 is a row of the §10 phase table, so its marker must be written after the table — which is precisely H30: `prereg_line: 998 (retention block written after the phase table; retains line 992)`, `operation: insert`, and whose operative text is already the prose marker `> **§10 line 992 (Phase 1 gate cell) — SUPERSEDED BY v30a, consequential to §6.2 lines 445 and 451…**`.
The manifest's own §B entry — *"H29 | 992 | Drafted at R39/F2 — the C1 operative row (plus marker §A-3d)"* — is what puts prose into a table row.

**4 (236–269) → H12 (insert after 451). AGREE.** Source insertion point, lines 220–223: *"After `PREREG.md` **line 451** (`- **Sliced variant** for CI, …`), i.e. immediately after §6.2's bulleted element list…"*. H12: `insert after 451 — but after H4's replacement block, not after the registered line`. Correctly ordered against H13.

**5 (293–301) → H15 (461, replace). DISAGREE — the range must be split; 299–301 belongs to H31 (1022).**
This is the substantive finding. The run is **two paragraphs separated by the `>`-only line 298**, and they name **two different sites**:
- 293–297: `**SUPERSEDED BY v30a — registered v30 criterion 3, retained verbatim, NOT operative:** "3. **No runtime finding of any tier…**"` → site §6.2 line 461 → **H15. Correct.**
- 299–301: `**Consequential — §10.1 line 1022** (H1 **C2**): the kill gate carries a second copy of the retired premise ("silent on \`fixture_corrected\`") and must be amended with this clause…` → **site §10.1 line 1022. Not 461.**

Three things settle it:
1. **The manifest's own rule, applied one entry earlier.** 3d is the byte-for-byte structural twin of 299–301 — same "Consequential — <other section, other line> (H1 **C**n)" shape — and the manifest routes it *away* from its host clause to the hunk at the named site. 299–301 gets the opposite treatment with no reason given.
2. **The manifest's own description of entry 5 covers only the first paragraph**: *"SUPERSESSION MARKER — §6.2 criterion 3 retained verbatim."* The 1022 paragraph is inside the range but outside the description — the signature of an oversight, not a decision.
3. **This text is applied, so it needs a real hunk.** Triaged finding 57(2): *"two drafting identifiers survive in **applied marker text** — 'F-5' at the SC-10 marker and '(H1 **C2**)' at the SC-3 marker."* The project treats it as applied.

Destination: **H31**, not H32. H32 is `replace` at 1022 whose operative text is a numbered list item; H31 is `prereg_line: 1022 (retention block written beneath item 3; retains line 1022)`, `operation: insert`, prose, already carrying `> **§10.1 line 1022 (kill-gate criterion 3) — SUPERSEDED BY v30a, consequential to §6.2 line 461…**`. Same reasoning as 3d.

Consequence for the manifest's arithmetic: §A's premise *"Five of the 33 are multi-marker runs … written out below as **39 entries**"* is wrong. **293–301 is a sixth multi-marker run.** Entries become 40, and the tally line "Entries: 39. Claimed by a hunk: 36" moves with it.

**6 (305–352) → H15 (461, replace). AGREE.** Source: *"**REPLACES `PREREG.md` line 461** (criterion 3)."* H15 `replace`, `461 (replaces the registered criterion 3 in place, as list item 3)`, anchor byte-matches PREREG.md:461. §C-3's two-blocks-one-hunk note is sound.

**7a (376–378) → H14 (459, marker). AGREE.** `**§6.2 line 459 — v30a, ADDED NOT SUPERSEDED.** Criterion 1 stands byte-exact.` H14: `459 (marker written at line 462, the end of its block)`, anchor = criterion 1 at PREREG.md:459.

**7b (379–380) → H14 (459, marker). AGREE, with a note.** `**§6.2 line 446 — NOT AMENDED.**` names line 446, and **no hunk acts at 446** — correctly, since the marker's whole content is that nothing is edited there. It must ride with SC-4's marker, and H14 already carries it. But this is structurally the same situation as §C-1's 14b ("§11 items 1–7 — EXTENDED", declared NO HUNK), and the manifest doesn't explain why one no-site marker gets a carrier and the other doesn't. The distinction is real — 446 asserts *no change*, §11 items 1–7 asserts a *change* — but it should be stated, or a reader will read the two as contradictory.

**8 (384–468) → H16 (464, insert). AGREE.** Source lines 369–370: *"After `PREREG.md` **line 464** (`Secondary findings on **manifest-listed descendants** …`), carrying H1 hunk **H6**'s placement."* H16 anchor verified at PREREG.md:464.

**9 (496–534) → H17 (464, insert). AGREE.** Source lines 488–489: *"After the block SC-4 inserts (i.e. after `PREREG.md` line 464 + SC-4), before line 466's parenthetical."* H17: `464 (insert after, following the SC-4 block) — immediately before line 466`. The ordering against H16 is explicit in both, which is what keeps two same-site inserts separable.

**10a (561–566) → H21 (855, replace-row). AGREE.** `**§7.7 line 855 — SUPERSEDED BY v30a. Registered v30 row, retained verbatim, NOT operative:**`; H21 `replace-row` at 855, anchor = the six-state coverage row verified at PREREG.md:855.

**10b (568–569) → H25 (915, marker). AGREE — another live duplication fixed.** `**§8.2 line 915 — v30a, EXTENDED NOT SUPERSEDED.**` names 915; H25 is `marker` at `915 (marker at its site, after the line)`, anchor verified at PREREG.md:915. This is marker **M2**, which the source's insertion point 2 (lines 554–557) refers to: *"where marker M2 below is already placed at that site, the insertion follows M2."* As the JSON now stands H21 carries 10a **and** 10b, so 10b would land at 855.

**11 (573–578) → H26 (915, insert). AGREE.** The block's own heading, source line 571, is `**INSERTION TEXT — §8.2, after \`PREREG.md\` line 915 (after marker M2 where placed) — S2(i).**`; H26 is `insert`, `915 (insert after, following marker M2)`. Exact.

**12 (582–610) → H22 (856, insert). AGREE.** Source insertion point 1: *"**\`PREREG.md\` line 855** … REPLACE the row to add the state, then INSERT the semantics block after the table (line 856)."* H22: `856 (insert after the table)`, anchor = the Strategy-diagnostic row at PREREG.md:856. Correctly separated from H21's row replacement. Note the JSON currently has this clause in **both** H22 and H26 — the manifest's 11→H26 / 12→H22 pair is what un-duplicates it.

**13 (642–662) → H18 (468, insert). AGREE.** Source lines 632–634: *"After `PREREG.md` **line 468** (`Top-k presence does not satisfy criterion 1. …`), before line 470's 'What this gate does and does not guarantee'."* Anchor verified at PREREG.md:468.

---

## Flags

**Flag 1 — 3a/3b/3c/3d: the sites are right, but whether this run is applied text at all is NOT ESTABLISHED, and the manifest doesn't ask.**
The prose introducing the block, source lines 225–226, says: *"This clause is the schema layer over three amendments H1 already drafts at instance-bearing lines. **Their markers stand as H1 wrote them and are cited, not re-drafted:**"* — the colon introduces the blockquote as a *citation list*. And the cited markers really do already exist at those sites: H10's operative text ends with its own `> **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675…"`, and H13's with the same for the sliced variant. Triaged finding 43 confirms the drafting history: *"SCHEMA_SET_FINAL cites them … and expressly does not re-draft them … Their only drafted text is in PREREG_v30a_DIFF.md"* (FIXED by R37/D2). So attaching 3a–3d on top adds a **second** supersession sentence at each site. Either this run is APPARATUS (like §A-26 and §A-31) or it is applied and duplicative; the manifest asserts the latter without addressing the source's "cited, not re-drafted". This needs the author's call, and §C is the place for it.

**Flag 2 — 3a/3b/3c/3d and 299–301 carry internal tooling identifiers into registered text.** `(H1 hunk **H2**)`, `(H1 hunk **H3**)`, `(H1 hunk **H4**)`, `(H1 **C1**)`, `(H1 **C2**)`. Triage already treats one of these as a defect — finding 57(2), status carried OPEN for the author at signing: *"two drafting identifiers survive in applied marker text — 'F-5' at the SC-10 marker and '(H1 **C2**)' at the SC-3 marker; one-line replacements are drafted in K2 §7 but not applied."* The manifest claims all five as applied text and mentions none of it. If Flag 1 resolves toward "applied", four *more* identifiers land in `PREREG.md` than that open finding accounts for.

**Flag 3 — line 567 is in no entry.** See partition check above. Trivial, but a mechanical checker will report block 10 as not fully partitioned.

---

## Files
- Manifest: `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\BLOCK_MANIFEST.md`
- Source: `…\scratchpad\amendment\SCHEMA_SET_FINAL.md`
- Hunks: `…\scratchpad\amendment\_X5_hunks_v2.json`
- Frozen population: `…\scratchpad\amendment\_K1_population_FROZEN.json`
- Target: `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`

Nothing was created, edited, moved or deleted; no git command was run.

==============================================================================
All six invariants checked against the sources. Counts below are mine, computed from the files, not from the manifest's own tallies.

---

# INVARIANT REPORT — BLOCK_MANIFEST.md

## 1. EXACTLY ONE HUNK PER BLOCK — **HOLDS**

42 rows in §A. 42 distinct entry names, 42 distinct anchor ranges, zero duplicate anchors. Every `→ Hunk` cell resolves to exactly one of: one X5 hunk id (39 rows), `NO HUNK` (1 row), `APPARATUS` (2 rows). No cell names two hunks.

One hazard for the mechanical check, not a violation: rows 3a/3b/3c carry `(H1 hunk **H2**)`, `(H1 hunk **H3**)`, `(H1 hunk **H4**)` in the *description* column. That is the H1-delta numbering, not X5 hunk ids. A checker that greps `H\d+` across the whole row reads 3a as naming both H2 and H10. The target column must be isolated first.

## 2. THE PARTITION IS COMPLETE — **coverage HOLDS, the stated count FAILS**

- Blocks in `_K1_population_FROZEN.json`: **33** (idx 1–33).
- Rows in §A of the manifest: **42**, not 39.

Arithmetic: 33 parents + 1 (1a/1b) + 3 (3a–3d) + 1 (7a/7b) + 1 (10a/10b) + 3 (14a–14d) = **42**. The manifest asserts "39 entries" in the Scope section and again in the tally line *"Entries: 39. Claimed by a hunk: 36. Apparatus: 2. Unclaimed and undrafted: 1."* The true figures are **42 / 39 / 2 / 1**. The tally is internally consistent (36+2+1=39), so this is one undercount of 3 propagated to both places, not two independent errors.

Coverage itself is sound: all 33 population blocks appear, every manifest line range falls inside the population (zero lines claimed outside it), and the only population lines not covered are 567, 692, 698 — the three `>` lines, which invariant 3 excepts.

## 3. THE MULTI-MARKER SPLITS PARTITION THEIR PARENTS — **HOLDS**

Verified line by line against `SCHEMA_SET_FINAL.md`:

| Parent | Range | Sub-entries | Gap | Overlap |
|---|---|---|---|---|
| 1 | 150–159 | 150–153, 154–159 | none | none |
| 3 | 228–232 | 228–229, 230, 231, 232 | none | none |
| 7 | 376–380 | 376–378, 379–380 | none | none |
| 10 | 561–569 | 561–566, 568–569 | **567** = `>` | none |
| 14 | 687–702 | 687–689, 690–691, 693–697, 699–702 | **692, 698** = `>` | none |

Lines 567, 692 and 698 each contain exactly `>` and nothing else. Every gap is a blank quote-marker line; no other line is uncovered; no sub-range overlaps another.

## 4. APPARATUS IS CORRECTLY IDENTIFIED — **HOLDS. Applying either would be wrong.**

**Entry 26 (1113–1117).** Sits under `**ROWS COVERED: 62, 63, 64.**` (L1108) and the label `*Instance record (apparatus, not applied).*` (L1110), which states the fence quotes `PREREG.md` **lines 759, 760 and 1039** verbatim. I checked all three against `PREREG.md`: they match. Applying it would re-insert three already-registered lines — the §7.1 `preserving` row, the `promoted` row, and the §10 per-combination bullet — as new text, at no declared site. Correctly apparatus.

**Entry 31 (1490–1492).** Byte-identical to `PREREG.md` line 816. The surrounding text says so twice: L1488 `ANCHOR — PREREG.md line 816, verbatim`, and L1494 `SUPERSEDED TEXT: none. Line 816 is unchanged`. It is the match target for H20, whose `anchor_text` field is that exact line with `anchor_verified: true`. Applying it would duplicate line 816 immediately above the paragraph inserted after it. Correctly apparatus.

(The line-816 text also occurs inside H36's operative text — but as a quotation inside SC-13c(c2), introduced by "`PREREG.md` line 816, verbatim:". That is a citation, not an application, and does not disturb the apparatus call.)

## 5. SECTION B ACCOUNTS FOR EVERY HUNK NOT IN SECTION A — **HOLDS as stated; its purpose is defeated once**

38 hunks in `_X5_hunks_v2.json`. §A names **33 distinct** hunks as targets — all except H1, H23, H30, H31, H32. §B has **11 rows**: H1, H2, H10, H11, H13, H23, H29, H30, H31, H32, H37. The five §A-absent hunks are exactly five of those eleven.

**Hunks appearing in neither section: none.** Union = 38/38.

But the stated purpose — "a hunk absent from §A is never mistaken for a hunk without text" — does not hold in reverse, and one hunk breaks it: **H20 (line 816, insert) is claimed in §A by entry 32, and its `operative_text` field is the empty string** (length 0). Presence in §A is therefore not evidence that a hunk has operative text. See §7 below.

## 6. FINDING C-1 IS REAL — **HOLDS in conclusion; the reason given is imprecise, and the finding is understated**

Verified in three parts.

**(i) No hunk lands the marker at §11.** Searching all 38 hunks' `operative_text` for `§11 items 1–7 — v30a, EXTENDED` / `Item 8 is added`: the only occurrence is inside **H19** — whose site is line **480**, not §11. H19's operative text contains the entire 687–702 marker run (14a, 14b, 14c and 14d) followed by the SC-8 clause. So the marker exists in the hunk set but is bound to the wrong site. C-1's conclusion — that nothing lands it at §11 — stands.

**(ii) H37 and H38 specifically.**
- **H38** (1054, insert): operative text is §11 item 8 only. Does not carry the marker. Confirmed.
- **H37** (1050, marker): its `what_changes` reads *"two marker blocks are placed: '§11 item 3 — v30a, SUPERSEDED AS A FILE SET, NOT AS A REQUIREMENT' and '§11 items 1–7 — v30a, EXTENDED'"* — it **does** declare this marker. Its `operative_text`, however, is the SC-8 clause body, byte-identical to H3's, and contains neither marker. So the manifest's flat *"neither carries this marker"* is wrong about H37 at the intent layer. The accurate statement is stronger, not weaker: H37 is the hunk this marker belongs to, and H37's operative text has been overwritten with the wrong content — losing not only 14b but **also 14c**, the §11 item 3 marker the manifest assigns to it.

**(iii) The ledger row is real and is not spurious.** `K2_AMENDMENT_LEDGER.md` line **472**, inside table **(b)** (header at line 459, table runs 461–472, (c) begins at 474), reads exactly:
```
| §11 items 1–7 | extended by item 8 | SC-8 | carried with SC-8 |
```
It is corroborated twice more in the same file: row **R36** (line 152) records the marker with placement id **A1372** at §11's site alongside item 8, and line 185 states the marker "shares R36's site with item 8". H2's own `operative_text` reproduces the (b) row verbatim. C-1's suggestion that "the ledger row is spurious and should go" is the wrong branch of its own disjunction — three independent records place this marker at §11. The hunk set is what is defective.

---

## 7. CROSS-CUTTING FINDING THE MANIFEST DOES NOT REPORT

The manifest defines belonging as: *"A block belongs to the hunk that will PUT THAT BLOCK INTO PREREG.md at that site."* Tested against that definition — block source text vs. the assigned hunk's `operative_text` — **26 of the 39 hunk-claiming entries verify; 13 do not.**

The manifest is a correct map of *intent*: every one of the 13 matches its hunk's declared `prereg_line` and, where a description exists, its `what_changes`. What fails is `_X5_hunks_v2.json`, in two patterns.

**Pattern 1 — text displaced within a clause group (9 entries).** The text exists, in the wrong hunk of the same group:

| Entry | Assigned | Text actually in | What the assigned hunk carries instead |
|---|---|---|---|
| 1b | H6 | H5 | the §2.9 SC-1 clause (block 2) |
| 3a, 3b, 3c, 3d | H10, H11, H13, H29 | H12 (all four) | replacement text from `PREREG_v30a_DIFF.md` |
| 10b | H25 | H21 | block 11's S2(i) text |
| 11 | H26 | H25 | block 12's SC-6 clause |
| 14c, 14d | H37, H3 | H19 (both) | the SC-8 clause body |

Two hunk pairs hold byte-identical operative text as a result — **H3 == H37** (2760 chars, the SC-8 clause) and **H22 == H26** (2070 chars, the SC-6 clause). Those are the only two duplicate pairs among 38 hunks.

**Pattern 2 — text in no hunk at all (4 entries). These are four more C-1s.**

| Entry | Block | Assigned | Status |
|---|---|---|---|
| 23 | SC-12(w), limbs (w1)–(w7), L1035–1071, 7329 chars | H35 | absent from every `operative_text`. H35's operative text is 3163 chars — exactly block 22's char count. Only H35's `what_changes` mentions (w1)/(w7). |
| 25 | the operative §8.3 bullet, L1106 | H27 | absent everywhere. H27 is 587 chars = block 24's marker alone; the replacement bullet the hunk exists to install is not in it. |
| 32 | §13c-P insert paragraph, L1498–1502 | H20 | **H20's `operative_text` is empty (0 chars).** |
| 33 | §AB recorded-defect text, L1526–1573 | H2 | absent from H2's 12,445-char operative text (no "RECORDED DEFECT", no reference to line 830), though H2's `what_changes` promises it "byte-exact". |

This bears directly on finding **C-4**, which states that entries 23 and 25 — "the two blocks K4 names" — are *"now claimed."* They are claimed in the manifest, and the manifest is right to claim them. But no hunk carries their text, so on the manifest's own definition of belonging they are in the same position as 14b: named, sited, and unlanded. C-1 should read as five findings, not one.

---

**Files read (all read-only, nothing modified):**
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\BLOCK_MANIFEST.md`
- `...\amendment\SCHEMA_SET_FINAL.md`
- `...\amendment\_X5_hunks_v2.json`
- `...\amendment\_K1_population_FROZEN.json`
- `...\amendment\K2_AMENDMENT_LEDGER.md`
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`

==============================================================================
## 1. IS THE MANIFEST SOUND ENOUGH TO BUILD THE CHECK ON?

**Yes — with three corrections applied first, and with one architectural change to what the check does.**

39 of 42 entries are right. I re-derived the block population independently (64 blockquote/fence runs in the whole file, 33 in lines 89–1576) and every one of the manifest's 33 anchor ranges is byte-correct against `_K1_population_FROZEN.json`. No block is missed. The two apparatus calls are right. The one-hunk-per-block invariant holds.

The architectural change: **the manifest must be the source the applier builds `operative_text` from, not a thing checked against `operative_text`.** I confirmed the hunks file is systematically displaced — within each clause group the assembler wrote (marker + clause) into the first hunk and then broadcast the clause into the group's remaining hunks. That produced two byte-identical pairs (H3 == H37, 2741 chars; H22 == H26, 2061 chars), one empty hunk (H20, 0 chars), and four hunks missing text entirely. A check that scores the manifest against `operative_text` will report the manifest as ~13/39 wrong when the manifest is right and the JSON is wrong.

## 2. ASSIGNMENTS TO CORRECT

**(a) Entries 3a, 3b, 3c, 3d (lines 228–232) → APPARATUS, not H10/H11/H13/H29.**

Four independent things settle this:

1. The source's own introduction at SSF 225–226: *"This clause is the schema layer over three amendments H1 already drafts at instance-bearing lines. **Their markers stand as H1 wrote them and are cited, not re-drafted:**"* — the colon introduces a citation list.
2. **The applied verification copy contains none of it.** `grep` on `_K2_verify/PREREG.md` returns 0 for "registered anchor pair and its", "sliced variant re-registered", and "§10 line 992 — CONSEQUENTIAL". SC-3's marker, by contrast, is present in full at criterion 3's site (line 641). The distinction was made deliberately, not by omission.
3. H10, H11 and H13 **already carry their own supersession markers** in their operative text (`> **SUPERSEDED BY v30a — registered v30 text, retained verbatim, NOT operative:** "- **Reference AUC:** 0.957 and 0.675…"` etc.). H29 + H30 fully cover 992 with a drafted operative row and a drafted retention block. Applying 3a–3d adds a second, differently-worded supersession statement at each of four sites.
4. **H2's amendments block enumerates the marker sites and these are not among them.** H2's `what_changes`: *"(a) nine superseded lines — 445, 450, 451, 461, 855, 1030, 992, 1022, 929; (b) ten byte-exact surfaces carrying markers — 97, 205, 220–222, 431, 459, 480, 816, 915, item 3 (1050), items 1–7"*. 445/450/451/992 sit in (a), not (b). The registration registers no marker at any of them.

Fallback, if the author rules them applied: they go **as one unit to H12** (451, insert), which is where the assembler put them and where SC-2's clause lands. They are never split across four hunks. And 3d never goes to H29 — H29's `operative_text` is a single markdown table row, and prose appended to a replaced row splits the §10 phase table (the R37/D4 complete-block rule, which H5 and H37 both obey).

**(b) Entry 14b (lines 690–691, "§11 items 1–7 — v30a, EXTENDED") → H37, not "NO HUNK".**

The applied copy settles it outright. At `_K2_verify/PREREG.md` line 1417, beneath §11's list and after item 8, two marker blocks stand in order: item 3's, then this one. That location is H37's declared site — `prereg_line: 1050 (marker written at line 1054, the end of its block)` — and H37's `what_changes` names both verbatim: *"two marker blocks are placed: '§11 item 3 — …' and '§11 items 1–7 — v30a, EXTENDED'."* Corroborated three more times: K2 ledger R36 (placement id A1372), ledger D2 line 185, and §8.2 table (b) line 472.

**§C-1 is therefore false, and its remedy is dangerous.** Its disjunct *"or the ledger row is spurious and should go"* would delete a row that four records support. §B's "H37 | 1050 | §A-14c **only**" must read §A-14b + §A-14c.

**(c) Entry 5 (293–301) → H15. The manifest is right; Verifier 1's split is wrong.**

`_K2_verify/PREREG.md` lines 644–645 show both paragraphs applied together at line 461's site, inside criterion 3's replacement, after limb (h) — including the "Consequential — §10.1 line 1022 (H1 **C2**)" paragraph. `H15.operative_text` matches. `X5_FINAL_PREREG_DIFF.md` O-25 names it as *"the CONSEQUENTIAL notes from the SC-2 and SC-3 markers"* — a note **in** the SC-3 marker, not a marker at 1022. Finding 57(2), which Verifier 1 cites in support, in fact says *"'(H1 C2)' at the **SC-3 marker**"* — i.e. at 461. H31 already carries its own separately drafted 1022 retention block from K2 §9.2; routing 299–301 there duplicates it.

## 3. INVARIANTS THAT FAIL

1. **The entry count is wrong.** §A has **42** rows (33 parents + 1 + 3 + 1 + 1 + 3 splits), not 39. Both the Scope paragraph and the tally line understate by 3. Corrected tally after §2 above: **Entries 42. Claimed by a hunk: 36. Apparatus: 6. Unclaimed and undrafted: 0.**
2. **§B's stated purpose is defeated once.** *"A hunk absent from §A is never mistaken for a hunk without text"* does not hold in reverse: **H20 is claimed in §A by entry 32 and its `operative_text` is the empty string.** Presence in §A is not evidence a hunk has text.
3. **The `>`-separator rule is unstated and applied inconsistently.** 1a absorbs its separator at 153; 10a and 14a/14c do not, leaving 567, 692, 698 uncovered. Each is a bare `>`. Cosmetic, but a mechanical partition check will trip. State the rule.
4. **Row-parsing hazard (not a violation).** Rows 3a/3b/3c carry `(H1 hunk **H2**/**H3**/**H4**)` in the *description* column — H1-delta numbering, not X5 ids. The checker must isolate the target column before matching `H\d+`.

Invariants that hold as claimed: one hunk per block; coverage of all 33 population blocks; the 33 + 31 = 64 coverage proof (I re-derived 64); the split-partition integrity; §A ∪ §B = 38/38 hunks.

## 4. BLOCKS MISSED, AND HUNKS LEFT WITH NO TEXT

**No block is missed.** All 33 are accounted for, ranges exact.

**Hunks with no usable text, in severity order:**

- **H20 (816, insert) — `operative_text` is empty.** Entry 32 (SSF 1498–1502) is the sole copy of the §13c-P pointer. Per H20's own justification, without it the kill criterion is silently disarmed at the point of implementation.
- **H27 (929, replace)** — 587 chars, entry 24's marker only. The operative bullet (entry 25, SSF 1106) that adds `waived` to the failure set is absent from every hunk.
- **H35 (1035, insert)** — 3163 chars, entry 22 only. SC-12(w)'s limb block (entry 23, SSF 1035–1071, ~7.3k chars) is absent from every hunk; only H35's `what_changes` mentions (w1)–(w7).
- **H2 (8, insert)** — §AB (entry 33) absent, though `what_changes` promises it *"byte-exact"*.
- **Displacement set** (text exists but in the wrong hunk of the group): H5 over-captures 1b; H6 holds block 2 instead of 1b; H21 over-captures 10b; H25 holds block 11 instead of 10b; H26 holds block 12 instead of 11; H19 over-captures 14b/14c/14d; H3 and H37 both hold the SC-8 clause instead of 14d and 14b+14c.

§C-4 says entries 23 and 25 are *"now claimed"* — true, and the manifest is right to claim them, but claimed is not carried. They are in the same position as 14b was: named, sited, unlanded.

## 5. WHERE THE VERIFIERS DISAGREED

| Dispute | Ruling | What settles it |
|---|---|---|
| Entry 5 — V1 says split 299–301 to H31 | **V1 wrong. Manifest right: whole run → H15.** | Applied copy line 645 has it at 461; O-25 calls it a note *in* the SC-3 marker; finding 57(2) locates it "at the SC-3 marker". |
| Entry 3d — manifest says H29, V1 says H30 | **Both wrong. Apparatus** (fallback: H12 as a unit). | Source "cited, not re-drafted"; 0 hits in applied copy; H2's enumeration puts 992 in (a) not (b). |
| Entry 14b — manifest NO HUNK, V2/V4 say H37 | **V2/V4 right: H37.** | Applied copy line 1417 places it beneath §11's list beside item 3's marker = H37's site; H37's `what_changes` names it; ledger R36/D2/§8.2(b). |
| V1's Flag 1 (is block 3 applied at all?) | **Correctly raised; resolves to APPARATUS.** | As above. V1 was right to refuse to certify it. |
| V4's count (42 vs 39) | **V4 right.** | Recounted: 42 rows. |
| V2/V3/V4 on `operative_text` being unreliable | **All right, and convergent.** | Independently confirmed: H3==H37, H22==H26, H20 empty, four missing payloads. |

## 6. WHAT IS CORRECT AND NEED NOT BE RE-CHECKED

- **All 33 anchor ranges**, verified line-by-line against the file and the frozen population.
- **The coverage proof** (33 in Part 1, 64 in the file).
- **The two apparatus calls, entries 26 and 31.** Entry 26's fence re-quotes PREREG lines 759/760/1039 verbatim under an explicit *"apparatus, not applied"* label; entry 31 is byte-equal to PREREG line 816 and to H20's `anchor_text`, under *"SUPERSEDED TEXT: none."* Applying either would duplicate registered text.
- **All 39 remaining assignments**, including the four the manifest exists to fix and which are genuinely repaired by it: 1b→H6, 10b→H25, 11→H26, 12→H22, plus 14c→H37 and 14d→H3.
- **§C-3's shape** — two blocks to one hunk at H15 (5+6), H33 (27+28), H27 (24+25), H14 (7a+7b), H35 (22+23). All confirmed against the hunks' declared sites.
- **7b (§6.2 line 446 — NOT AMENDED) riding on H14.** No hunk acts at 446 and none should; the marker asserts non-amendment. It is present once in the applied copy, at 462. This is not the same situation as 14b, which asserts a change and does have a hunk — the manifest should say so in one line.

**Files (all read-only; nothing created, edited, moved or deleted; no git command run):**
- `C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\amendment\BLOCK_MANIFEST.md`
- `…\amendment\SCHEMA_SET_FINAL.md`, `…\amendment\_X5_hunks_v2.json`, `…\amendment\_K1_population_FROZEN.json`
- `…\amendment\K2_AMENDMENT_LEDGER.md`, `…\amendment\X5_FINAL_PREREG_DIFF.md`, `…\amendment\_K2_verify\PREREG.md`
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md`