# ITEM J1 — GATE-CRITICAL CLASSIFICATION OF ALL 138 SCRUB ROWS (R21 two-part test)

**Nothing was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md`
are untouched. No git command was run. The archive was not read from. This file is drafted for
author approval and is the only file this item wrote.

Sources read this pass:
- `...\scratchpad\amendment\DECLARATION_SCRUB_LIST.md` (360 lines, read IN FULL).
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\PREREG.md` — §0.2.1 (60–111), §2.3–§2.5
  (185–229), §6.1–§6.6 (425–554), §7.4–§7.10 (820–903), §8.1–§8.6 (907–962), §10–§10.2 (980–1042),
  §11 (1046–1054).
- `C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md` — §T2 addendum
  (344–355), §5 (420–459), §A.5 (1000–1017), §A.6.3 (1226–1257), §A.8/§A.9 (1413–1457), §A.12
  (1525–1599), §13(g)/(h) (2210–2254), §C (2527–2546), §D.1 items 4–6 and the ordering consequence
  (3400–3419), §D.2/§D.3 (3420–3488), §E (3490–3520), §F.3 (3556–3605), the working-resolution tail
  (3646–3685).

---

## 1. THE THREE COUNTS — FIRST, AS REQUIRED

| Bucket | Count |
|---|---|
| **GATE-CRITICAL** (rule; gate PASS/FAIL depends on it → `PREREG.md`) | **76** |
| **NON-GATE** (rule; gate PASS/FAIL does not depend on it → `PRACTICES.md`, non-normative) | **26** |
| **INSTANCE** (fails R21 test 1 → stays in the declaration) | **36** |
| **TOTAL** | **138** |

Cross-check against H2's own tallies: GATE-CRITICAL + NON-GATE = 76 + 26 = **102 RULE** ✓;
INSTANCE = **36** ✓. Both reconcile to H2's machine-derived counts exactly, so no row changed its
R/I call in this pass — J1 only subdivides H2's 102 RULE rows.

**Operational form of R21 test 2, applied uniformly and stated so the calls are auditable:**

> A rule is **GATE-CRITICAL** iff a gate run executed under a *different version of that rule*
> could return a different PASS / FAIL / halt verdict on the same fixture with the same detector.

Consequences of that form, applied consistently throughout:
- Rules that constitute a criterion, a denominator, a gate class, an adjudication routing, the
  declared inputs a detector is scored under, the scored population, a pre-run exclusion, or the
  ex-ante freeze → **GATE-CRITICAL**.
- Rules that govern only what the gate report must *say* → **NON-GATE** (the prompt's own steer).
- Rules about amendment machinery, ledger bookkeeping, recording locus, and registration
  integrity → **NON-GATE**, because a gate run computes its verdict from the frozen §D.1 objects,
  not from the amendment ledger. **See §5 for why this outcome is a problem the author must look
  at, not a clean result.**
- A rule that can convert a would-be PASS into a *halt* (stop-and-report, RAISE) is treated as
  gate-critical, because a halt is not a PASS.

---

## 2. STOP-AND-REPORT CHECK — **IT FIRES. LOUDLY.**

> **GATE-CRITICAL is 76, against the ~30 the scope decision assumed. That is 2.5×, not a margin.
> Under R21's own test, the acceptance gate depends on 76 rules that PREREG.md does not currently
> state, 26 of which have no clause in PREREG.md to amend at all. The author must revisit scope
> before any drafting begins.**

**What drives the excess — and it is not padding.** The excess is not spread thinly; it is four
dense clusters, and each one is a *new gate object* rather than a new sentence:

| Driver | Rows | Count | What it actually is |
|---|---|---|---|
| **The three-class column partition (R11)** | 17, 19, 29–36, 38, 39, 42–44, 46, 48–50, 59, 95, 98–101, 103–108 | **30** | PREREG.md has **no** column-partition object. R11 creates one, and a partition needs a derivation rule, a precedence rule, four reading rules, a one-class-per-column rule, a re-derivation rule, three class definitions, three sets of gate consequences, and a set of pre-run exclusions. Thirty rules is the *normal* size of that object, not an inflation. |
| **The declared ground-truth map as scoring key (R9)** | 6, 55, 56, 74, 75, 78, 80, 82, 85, 88–90, 92, 93, 123, 124 | **16** | PREREG.md's criterion 3 is a one-line silence test. Replacing it with a scored key drags in a schema, a scored class set, a coverage state, an ex-ante freeze, a cohort-checkability rule, a "not a second scoring key" rule, and four "may never be quoted as criterion-1 arithmetic" rules. |
| **The §D.1 freeze / ex-ante ordering machinery** | 66, 106, 119–122, 125, 128 | **8** | What freezes, in what form (lists not counts), and that no interpretation may weaken it. This is what makes the map and the partition *ex-ante* rather than post-hoc; without it every other gate-critical row is unenforceable. |
| **New gate protocol surface + controls** | 129, 130, 134, 135 | **4** | §E's detector input surface and one-side-at-a-time sequencing; §F.3's all-zero control, which says of itself that it binds the gate report's own per-criterion counts. |

Remaining 18 GATE-CRITICAL rows: declared-input semantics (1, 3, 4, 5, 7, 11, 96, 72), fixture
identity and exclusion (14, 25, 26), the §10.2 `waived` floor and §A.5's reading (28, 62, 63, 64),
criterion 4's sentinel (58), the criterion-1 report structure's adjudication limb (60), and the
duplicated §14 restatement (110).

**The root cause, stated plainly.** §A.11 line 1516's ledger — "**Four amendments (445, 450, 451,
461)**" — counts amendment **sites**. The scope decision was calibrated on that count. But v30a does
not amend four sentences; it introduces **four objects PREREG.md does not contain**:

1. a **three-class column partition** with its own derivation rule (R11);
2. a **declared per-cell ground-truth map** as criterion 3's scoring key (R9);
3. a **new coverage state, `UNSCORED`** — PREREG.md line 855's state list is `passed, failed,
   not_applicable, unsupported, could_not_run(reason), waived`, and does not contain it;
4. a **gate-protocol input surface** with a hard sequencing rule (§E).

Each object carries a dozen-plus rules by construction. Counting sites gave "a dozen or so";
counting objects gives 76. **The scope decision was made against the wrong denominator.**

Two further facts the author needs before revisiting scope:

- **Two of the four ledgered amendments are NOT gate-critical.** Line 450 (recording *locus* of the
  contamination availability class — rows 22, 23) and line 451's discharge-prohibition (row 27) do
  not change any verdict. Meanwhile 26 rules with **no ledger entry at all** are gate-critical
  (rows 3, 4, 7, 11, 28, 35, 44, 46, 58, 62, 63, 64, 72, 80, 82, 85, 90, 96, 101, 123, 124, 128,
  129, 130, 134, 135). The ledger and the gate-dependence set barely overlap.
- **26 of the 40 homeless rows are gate-critical.** H1's diff does not have 40 clauses to amend and
  14 to create — it has **26 gate-determining clauses to create from nothing**. §3 below names them.

---

## 3. THE FULL 138-ROW CLASSIFICATION

Bucket key: **GC** = GATE-CRITICAL → `PREREG.md`; **NG** = NON-GATE → `PRACTICES.md`
(non-normative); **INST** = INSTANCE → stays in `AVAILABILITY_DECLARATION.md`.
`H` column: **N** marks a row H2 flagged `HOME = NONE` (no PREREG clause exists to carry it).

### Part I (declaration lines 1–545)

| # | § | Statement (one line) | Bucket | H | Why the gate does / does not depend on it |
|---|---|---|---|---|---|
| 1 | §1 | The declaration states the **measured** boundary, not the intended one | **GC** | | The boundary is the availability truth the comparator reads; `floor(t−1)+1s` vs `t−1` changes the violation map, hence criteria 1 and 3 |
| 2 | §2 | Generation-naming rule: every row count names count, path, generation, sha256 | **NG** | | Provenance labelling on published counts; no criterion reads a hash or a path |
| 3 | T2 add. | `column_roles` describe the **RAW pre-lag** column; the fed value at row T is the lagged one | **GC** | N | Fixes the availability instant of every fed column; read post-lag, the REQUIRED set changes |
| 4 | §5 | Label availability is **POSITIONAL** (`timestamp` of the row h positions on), not `T + h` seconds | **GC** | N | A new unit for §2.4's formula and a declared detector input (§E); it decides whether the 2,100 cross-boundary rows are violations |
| 5 | §5 | Cross-boundary label rows are **IN the scored population** — not excluded, masked, or separately denominated | **GC** | | It is a denominator statement; excluding them removes 2,100 rows from adjudication |
| 6 | §5 | Findings on them are adjudicated by the **declared map** like any other row | **GC** | | Routing into required / false-positive / unscored — the verdict itself |
| 7 | §5 | The declaration **creates no new gate criterion**; §6.2's four as amended are the whole gate | **GC** | N | It enumerates the gate's extent; a fifth criterion would be a fifth way to fail |
| 8 | Pt II | Delta-issued working resolutions R14–R17 / S1–S4 bind exactly as recorded ones | **NG** | N | Authority of the WR ledger; a gate run reads §D.1's frozen objects, not the ledger. **Close call — see §5** |
| 9 | Pt II | A later resolution supersedes an earlier one; the earlier stands as record | **NG** | N | Ledger ordering; no criterion reads it |
| 10 | §0.3 | Every measurement claim names the artifact it was measured on, or it is not publishable | **NG** | | Publishability / auditability rule; shapes reporting, not the verdict |
| 11 | §0.4 | The pre/post licence requires the sides to differ in availability and **nothing else**; a column-set change is not an availability change | **GC** | N | It bounds what may be admitted into the fixture; admitting a column-set variant changes the scored universe and criterion 1's denominator |
| 12 | §0.1–0.2 | Artifact A / Artifact B identities, column universes, lattice bridge | INST | | Names this fixture's two objects |

### §A — the conformance walk (751–1597)

| # | § | Statement (one line) | Bucket | H | Why the gate does / does not depend on it |
|---|---|---|---|---|---|
| 13 | §A.0 | "Every AMENDED entry below is a class C amendment carried by this registration" | **NG** | | A classification assertion about the ledger; the verdict does not read the amendment class |
| 14 | §A.1 | Line 445's registered pair and ±0.010 interval are **retired and replaced** by the recomputed trio | **GC** | | Under the old anchor the fixture fails §10 line 992's reproduction gate outright (0.675 vs 0.931536); retiring it is what makes a pass reachable |
| 15 | §A.1 | The LightGBM trio table and its `f1\f1_results.csv` provenance | INST | | This fixture's AUCs |
| 16 | §A.1 | "Why the old anchor cannot stand" — three numbered reasons | INST | | The arithmetic is this fixture's; it is the amendment's evidence |
| 17 | §A.2 | Line 446's count carries **no gate arithmetic**; the criterion-1 denominator is a different object | **GC** | | N = 25 vs N = 11 is the difference between criterion 1 satisfiable and not |
| 18 | §A.2 | The manifest is not edited; **evidence artifacts are never adjusted toward a decision** (R13) | **NG** | N | Artifact integrity; the verdict does not read the manifest's edit history — and row 19 removes flavor from the arithmetic anyway. **Close call — see §5** |
| 19 | §A.2 | Nothing in the gate turns on the DAG **flavor** split; it enters no criterion, denominator or count | **GC** | | A negative scoping rule: if flavor entered the denominator, 7/18 vs 6/19 would move criterion 1's membership |
| 20 | §A.2 | A gate report quoting a leaking-source count must name which of the two scopes it counts under | **NG** | | Self-described "declared reporting obligation"; the count is the same either way |
| 21 | §A.2 | The count 25; the 7/18 vs 6/19 split; the T4 22-column subset | INST | | This manifest's numbers |
| 22 | §A.3 | The contamination availability class is **recorded in this declaration**, not the manifest (line 450 amended) | **NG** | | Recording **locus**. Line 450 is a fixture-construction bullet, not a pass criterion; the class's *content* (row 24) is what the map consumes |
| 23 | §A.3 | The locus amendment does not license recording other manifest content outside the manifest | **NG** | | Scope limit on a locus amendment; same reason as row 22 |
| 24 | §A.3 | Declared class: AVAILABILITY VIOLATION BY FORWARD JOIN, with its mechanism | INST | | This fixture's contamination class |
| 25 | §A.4 | The sliced variant is **moved off** the Phase 0 acceptance fixture and re-registered as a Phase 1 CI obligation | **GC** | | It changes what the Phase 0 fixture *is*; left in, §10 line 992's "full and sliced" reproduction is unmet and the gate fails |
| 26 | §A.4 | The slice scoring rule, declared ex ante: a slice of a CHARACTERIZED side is **never treated as clean**, and may not be reported as a pass on unscored cells alone | **GC** | | A pass/fail adjudication rule for a gate-scored object |
| 27 | §A.4 | The Phase 1 obligation may not be discharged by `DEVIATIONS.md` or a WR; dropping it is class C | **NG** | | Discharge machinery; the verdict does not read it |
| 28 | §A.5 | Line 449's semantic-ambiguity clause **does not fire** — "documented-and-violated is not the same as undocumented" | **GC** | N | Decides whether §10.2 criterion 2 is replaced and whether the fixture carries full acceptance weight. **REJECTED by R22 — see §6** |
| 29 | §A.6 | The criterion-1 denominator derives from the **DECLARED MAP**, not the manifest's construction classes | **GC** | | It *is* criterion 1's denominator |
| 30 | §A.6 | Partition discipline: mutually exclusive, exhaustive, **enumerated by name**, no residue, no bare count | **GC** | | A residue-defined class has different membership; membership is the denominator |
| 31 | §A.6.0 | The three iff-clauses: REQUIRED / OUT OF JURISDICTION / UNSCORED | **GC** | | The class definitions themselves |
| 32 | §A.6.0 | Precedence when clauses conflict: **UNSCORED wins** | **GC** | | A dual-satisfying column lands in REQUIRED or UNSCORED depending on this line |
| 33 | §A.6.0 | "Same-row book/clock" reads as **within-lattice**, not literally single-row | **GC** | | Fixes OOJ membership at its edge |
| 34 | §A.6.0 | "Unconstructible under T4" reads as **gate status EXCLUDED**, not F2-rebuild-unconstructible | **GC** | | The file says it itself: the other reading "would silently drop `dollar_volume_1s` and `tick_direction` out of the arithmetic" |
| 35 | §A.6.0 | Any disagreement between the rule-derived class and the frozen class is a **stop-and-report** | **GC** | N | A halt is not a PASS; and absent the rule a disagreement resolves silently to a different membership |
| 36 | §A.6.0 | A construction change forces class re-derivation and an amendment; **the enumeration is the rule's output, not a substitute** | **GC** | | Makes the rule, not the frozen list, the authority for membership after any change |
| 37 | §A.6.0 | The 35-row rule-application table | INST | | The enumeration IS the fixture |
| 38 | §A.6.1 | A required finding must be **on the side and in the instrument-months the map declares** | **GC** | | Narrows criterion 1's satisfaction condition |
| 39 | §A.6.1 | Criterion 1 is **not satisfied by column name alone**; a same-row `mid[t]` finding is OOJ and does not satisfy | **GC** | | Same — it decides whether a given finding counts |
| 40 | §A.6.1 | The 11-column REQUIRED table with construction lines | INST | | This fixture's denominator contents |
| 41 | §A.6.1 | No MBO-derived column is in the list; a scope fact, not an omission | INST | | True only because Phase 7 feeds no MBO columns |
| 42 | §A.6.2 | An availability-class finding on an OOJ column is a **FALSE POSITIVE**; they enter no criterion-1 denominator | **GC** | | The gate consequence attached to a class |
| 43 | §A.6.2 | Criterion 2 **cannot receive** OOJ columns; a finding is a declared false positive, not a criterion-2 failure | **GC** | | Decides whether criterion 2 fails on a given finding |
| 44 | §A.6.2 | An **L2a label-base** finding on them is neither credited nor penalized by this gate | **GC** | N | A jurisdiction boundary that decides whether an L2a finding counts against criterion 2 or 3 |
| 45 | §A.6.2 | The 4 + 18 OOJ column lists | INST | | This fixture's OOJ membership |
| 46 | §A.6.3 | **UNSCORED**: requires no finding and forbids none; no denominator, no rate, **cannot be reported as a pass** | **GC** | N | A new coverage state with gate consequences; it decides whether an unscored column can carry a pass |
| 47 | §A.6.3 | Must be named in the gate report as **EXCLUDED**, never MISSED | **NG** | N | Reporting vocabulary. The *exclusion* (row 103) is gate-critical; the word used for it is not |
| 48 | §A.6.3 | **One gate class per column**; reinstating `book_imbalance_ratio` changes the denominator and is class C | **GC** | | A column in two classes is in two denominators |
| 49 | §A.6.3 | These are **cells, not columns**; a cell-level unscored never makes a column unscored | **GC** | | Structural rule determining column membership from cell facts |
| 50 | §A.6.3 | R11's third UNSCORED limb read precisely: §17's seven are not gate-unscored | **GC** | | Same arithmetic consequence as row 34, stated at the class |
| 51 | §A.6.4 | The partition check **must be reproduced by any gate report** | **NG** | | An obligation on report content. Row 120 carries the consequence ("has not scored this fixture") and is where the gate-critical limb lives |
| 52 | §A.6.4 | The 11 / 22 / 2 / 35 count table and its tie-out | INST | | This fixture's partition |
| 53 | §A.6.5 | The SOURCE × GATE cross-tabulation, 35 rows | INST | | A consistency check on this fixture's two taxonomies |
| 54 | §A.7 | The manifest-clean set is the 4 clean columns; neither disposition weakens the criterion | INST | | This fixture's clean set |
| 55 | §A.8 | **The amended criterion 3 itself** — findings must match the declared per-side, per-class, per-instrument-month map | **GC** | | It is a gate criterion, verbatim |
| 56 | §A.8 | Scope limits + **the map is declared and frozen before any detector runs** | **GC** | | A map frozen after a run is a key shaped by the result; and "no unscored escape hatch" keeps failures failing |
| 57 | §A.8 | What forced it — M5, 18 of 48, 111,334 of 580,944 | INST | | The measurement that forced the amendment |
| 58 | §A.9 | **SENTINEL:** the wrapped `net_delta` values are DATA CONTENT; firing on them is a **false positive under criterion 4** | **GC** | N | Criterion 4's adjudication — without it, a firing on the 2^32 signature fails criterion 4 |
| 59 | §A.10 | **N is 11**, the REQUIRED list length, not line 446's count; **N = 25 is withdrawn** | **GC** | | Criterion-1 denominator identity |
| 60 | §A.10 | Report k of N = 11; report FPs on the 22 separately; **findings on UNSCORED are NOT false positives**; never fold classes | **GC** | | Mixed row. The reporting limbs are non-gate; the limb "UNSCORED findings are not false positives / do not carry the FP consequence beyond the 22" decides whether criterion 2 or 3 fails |
| 61 | §A.11 | The walk summary table and "Four amendments (445, 450, 451, 461)" | **NG** | | An amendment ledger; the verdict does not read it. **Its count is contradicted by §2 above** |
| 62 | §A.12 | The **DEFINITION of WAIVED**, limbs (i)–(v) | **GC** | N | Gates the admissibility of §10.2's replacement acceptance criterion, which is live under R22 — **see §4 and §6** |
| 63 | §A.12 | **It may not be invoked**: there is no procedure by which either runtime detector may be waived | **GC** | N | The floor's operative prohibition; a waiving replacement criterion is inadmissible on its face |
| 64 | §A.12 | The seven "does not permit" scope limits | **GC** | N | Limbs 4 ("no data" ≠ "waived" → UNSCORED) and 6 (per-combination waiving is waiving) each independently change admissibility; limbs 1, 2, 3, 5, 7 are guards over the same |
| 65 | §A.12 | Status: class C amendment content added by v30a; resolves toward the stronger reading | **NG** | | Status and classification bookkeeping |

### §§8–17 (1599–3361)

| # | § | Statement (one line) | Bucket | H | Why the gate does / does not depend on it |
|---|---|---|---|---|---|
| 66 | §8 | The pc2 exclusion is **HARD**; any future use changes the fixture the criteria are evaluated on — class C, not a DEVIATIONS entry or a WR | **GC** | | Admitting the excluded set changes the scored population |
| 67 | §8 | Fixture identity, 64 parquets/side, RE-EVALUATE class, recomputed trio, 95/128 corroboration | INST | | This fixture's identity. (H2's flag stands: "RE-EVALUATE class" is unregistered vocabulary) |
| 68 | §9 | The **licence** for reading the pre/post AUC delta as a feature-availability-only effect | **NG** | N | It licenses an *interpretation of the AUC delta*, which §6.1 line 441 declares provenance and which enters no criterion. Row 11 carries the fixture-admission limb and is GC |
| 69 | §10 | "This section states no rule." | INST | | Correct as written |
| 70 | §10 | Corrected-vs-(t−1) is the **lag-image** of contaminated-vs-T, not independent corroboration | **NG** | N | Evidence-accounting for the declaration's own diagnostics; no criterion reads it |
| 71 | §10 | The counts, the PRIMARY/cross-check table, the off-by-one reconciliations | INST | | This fixture's measurement record |
| 72 | §12 | The 49 equal events are **non-violations under the declared branch** and enter no detection denominator; both-branch figures are informational | **GC** | (b) N | Limb (a) applies line 192's comparator and sets the map's violation set; limb (b) forbids computing a gate outcome from the non-declared branch |
| 73 | §12 | The 49 events, the T1-PRIMARY designation, the C4 qualifier | INST | | This fixture's counts |
| 74 | §13(a) | The `declared_map.csv` **schema** — one row per scored cell, ten named fields | **GC** | | Criterion 3 scores against this object; its schema is the scoring key's shape |
| 75 | §13(a) | **CLASS-SET RULE:** `mbo_all_rows` is an 11th *diagnostic* class, not one of the declared 10; every "max" names its class set | **GC** | | The first limb fixes which classes are scored; a diagnostic class inside the declared set changes criterion 3's population |
| 76 | §13(a) | 984 / 960 / 888 / 72 / 24; the declared 10 class names; companion artifacts | INST | | This map's contents |
| 77 | §13(b) | A ranking is quoted with its metric (rate order ≠ count order) | **NG** | | Reporting legibility; the same cells rank either way |
| 78 | §13(b) | "Clean on both branches" **withdrawn as a pass claim**; zero-over-scored-classes ≠ zero-over-the-declared-10; **no row may be quoted as a pass** | **GC** | | A pass claim is a gate outcome; this forbids a partial-class zero from becoming one |
| 79 | §13(b) | The 18-row rate table, 13 measured-zero rows, 18+17+13 = 48 | INST | | This map's contents |
| 80 | §13(d)+§C.2 | A declared cohort definition must be **checkable from the lattice alone, before any detector runs** | **GC** | N | Ex-ante checkability is what stops the cohort being a post-hoc description; a post-hoc cohort is a key shaped by results (line 480) |
| 81 | §13(d) | The predicate, 5,305,430 rows, 7.94%, the −3 ns / −5 ns headroom | INST | | This fixture's cohort |
| 82 | §13(g) | Cell-level unscored: no finding required or forbidden, no denominator, no rate, **cannot be reported as a pass** | **GC** | N | Decides whether the 72 cells license a corrected-side pass — the exact "absence of data into evidence" failure |
| 83 | §13(g) | `nq` carries the TRADES-CLASSES-ONLY label and the correct reason on every appearance | **NG** | | A labelling obligation. (The denominator sentence inside the same range is carried by rows 85 / 123) |
| 84 | §13(g) | The 72 cells, the missing path, the two out-of-path NQ MBO families | INST | | This fixture's coverage hole |
| 85 | §13(h) | §13(h) is **NOT part of the gate**: nothing enters any criterion, denominator, rate or the §D.1 freeze; moving it in later is class C | **GC** | N | A body of data excluded from every denominator; admitted, the X4 numbers enter the arithmetic |
| 86 | §13(h) | The X4 results, join soundness, day coverage, premise correction | INST | | This fixture's diagnostic |
| 87 | §13(i) | R17(ii): both maps published side by side with the delta explicit; neither replaces the other | **NG** | N | A publication obligation. The "not a second scoring key" limb is row 89 and is GC |
| 88 | §13(i) | A scope restriction is **justified independently of its effect on any count**, and no such reference may be added | **GC** | | Generalises line 480's locked ordering to scope choices; a restriction shaped by its numeric effect reshapes the map |
| 89 | §13(i) | The restricted map is a **REPORTING object** — not a second scoring key, and it changes no adjudication | **GC** | | Fixes which map is the scoring key |
| 90 | §13(i) | **"An all-zero return would have been a FINDING, not a pass."** | **GC** | N | Converts a zero into a finding rather than a pass — a verdict statement |
| 91 | §13(i) | The R17(i) column-universe box; MAP 1 vs MAP 2; the 18-cell table; the R17(iii) result | INST | | This fixture's column universe and map |
| 92 | §13(j) | The four FORBIDDEN-USE rules — never evidence about a fed column, **never any criterion-1 arithmetic**, no unqualified "X of 48", no unqualified "max" | **GC** | | Limb 2 is an explicit criterion-1 arithmetic exclusion; limb 1 governs what the map classes may evidence |
| 93 | §13(j) | "The 35-column set" always means `ALL_L2_FEATURES`; **name the constant, not the length** | **GC** | | Binds the identity of the scored universe; the wrong 35-set changes partition membership |
| 94 | §13(j) | What the MBO classes STILL legitimately evidence; the `BOUNCE_FREE_FEATURES` trap | INST | | What this fixture's classes evidence |
| 95 | §C | Everything is stated **POST-LAG** and **SIDE-RELATIVELY**; a side-independent list of leaking columns is a category error | **GC** | | Criteria 2 and 3 are per-side; a side-independent list misroutes every finding |
| 96 | §C | The comparator is pinned to the `at_source_timestamp` truth; **`at_bar_close` is never scored against** | **GC** | N | The file states the flip itself: the other reading "would find the contaminated side clean" |
| 97 | §C.1/§C.2 | The mechanism sentence, the (A)/(B)/(C) tables, the cohort restriction, the 18 non-zero months | INST | | This fixture's enumeration |
| 98 | §C.3 | The **availability declaration and the gate class are different objects**; no column carries two gate classes | **GC** | | One class per column is denominator membership |
| 99 | §C.3 | The three category definitions (OOJ / unresolved-lag unscorable / not-fed-so-no-gate-class) | **GC** | | Class semantics; cat 3's "not fed at all → no gate class whatever" determines membership |
| 100 | §C.3 | The four routing rules (FP on the 22; also a criterion-3 failure on corrected; L2a neither credited nor penalized; the four clean columns DO route to criterion 2) | **GC** | | Routing between criteria decides which criterion a finding fails |
| 101 | §C.3 | Label-base character is assigned to **L2a jurisdiction, outside this availability gate** | **GC** | N | Duplicate of row 44; decides whether an L2a finding counts against a criterion |
| 102 | §C.3 | The heading correction, the 27-column list, the 27 = 18 + 1 + 8 reconciliation | INST | | This fixture's construction list |
| 103 | §C.4(a) | A **dead-zero column cannot carry an availability finding**; leaving it in the denominator makes criterion 1 unsatisfiable; declared out pre-run | **GC** | | Stated in the text itself as making criterion 1 unsatisfiable — a guaranteed FAIL |
| 104 | §C.4(b) | **Staleness is not unavailability**; a value from the past is always available; this quirk licenses NO finding | **GC** | | A finding on it would be a false positive under criterion 2 or 3 |
| 105 | §C.4(c) | An unresolved construction/lag question forces **EXCLUDED**; reinstatement changes the denominator, class C | **GC** | | Denominator membership |
| 106 | §C.4 | The exclusions are declared **pre-run** and frozen at the tag | **GC** | | A post-hoc exclusion is a denominator shaped by the result |
| 107 | §C.5 | Criterion 1 is not satisfied by column name alone; a finding on another ground is **recorded on its own ground** | **GC** | | Criterion-1 satisfaction condition, stated in full |
| 108 | §C.5 | A column's gate class is **what the gate does with a finding**, and the gate needs exactly one answer per column | **GC** | | The definition of the object criterion 1's denominator is built from |
| 109 | §C.5 | `vwap_distance` as the sole MIXED column; its two grounds; the R16 comparison table | INST | | This fixture's only dual-ground column |
| 110 | §14 | FORBIDDEN USE — §13(j)'s rules restated verbatim for this side, items 1–5 | **GC** | | Same content as row 92, including the criterion-1 arithmetic exclusion. **Duplicated authority — after drafting this must be a citation, not a second copy (PREREG line 77)** |
| 111 | §14 | The EX-NQ figures are the **summary-level** peaks; nq may appear only as a per-cell entry, never as the restricted headline | **NG** | N | Self-described as governing "SUMMARY-LEVEL quotation"; the underlying per-cell figures and their adjudication are unchanged |
| 112 | §14/§14.1 | PROFILE 1 / PROFILE 2, delta tables, provenance block, the 48-cell table | INST | | This fixture's contaminated profile |
| 113 | §15 | Claims split per R4 into timing-structural **SUPPORTED** vs value-dependent **QUALIFIED** | **NG** | N | Evidence-accounting for published claims; criterion 4's rule about the same defect is row 58 and is GC |
| 114 | §15 | The two defects with line citations; C1 INHERITED; C5 WRAPPED; the 7 affected columns | INST | | This fixture's as-built record |
| 115 | §16 | The **category**: assumptions relied on that no archive record can verify, recorded as such | **NG** | N | A disclosure discipline. It does not change a verdict; §16's items 1–3 (row 116) are the fixture's own premises |
| 116 | §16 | Items 1–3: the 35-column assumption, PC2 runtime inputs, unhashable `C:\MBO_data` copies | INST | | This fixture's three unverifiables — H2's own steer: these stay |
| 117 | §17 | Projection is **selection or renaming only (nothing synthesized)** | **NG** | N | A method rule for the F2 rebuild, which row 50 rules explicitly *out* of the gate-scored fixture. Cleanest non-gate call in the set |
| 118 | §17 | 28 constructible / 7 unconstructible with reasons; determinism hashes; self-consistency | INST | | This fixture's projection result |

### §§D–F and the tail (3363–3685)

| # | § | Statement (one line) | Bucket | H | Why the gate does / does not depend on it |
|---|---|---|---|---|---|
| 119 | §D.1 | What **freezes at the tag**, and that any subsequent change is class C | **GC** | | The freeze is what makes the map and partition ex-ante; unfrozen, the scoring key can move after a result |
| 120 | §D.1 | The three-class partition freezes as **enumerated lists, not counts**; "a gate report that cannot reproduce this sum has not scored this fixture" | **GC** | | Both limbs: the freeze object's form fixes membership, and the consequence is a not-scored (non-PASS) verdict |
| 121 | §D.1 | **Every other gate-consumed number** freezes at the tag, exhaustively enumerated | **GC** | | Any gate-consumed number that could move after a result could move the verdict |
| 122 | §D.1 | The class-set rule and the four §6.2 amendments + the §10.2 definition freeze | **GC** | | Freezing the amendments is what puts the *amended* criteria in force at gate time |
| 123 | §D.1 | §13(h) is **NOT frozen** — provided its numbers are never moved into an acceptance denominator (class C) | **GC** | N | Denominator admissibility; duplicate of row 85 at the freeze site |
| 124 | §D.1 | Both-branch counts are **INFORMATIONAL ONLY**; **no gate outcome may be computed from them** | **GC** | N | Explicitly forbids a verdict computed under the non-declared tie branch |
| 125 | §D.1 | Consequence of line 480: a number found wrong after a fixture result is **not corrected in place**; it goes through line 99's route | **GC** | | Locked ordering; in-place correction after a result is precisely how a FAIL becomes a PASS. **Restatement — must become a citation** |
| 126 | §D.2 | **DECLARED: the v30a tag message carries SIX hashes** | **NG** | N | The gate's verdict does not read the tag message. **But this cannot rest in a non-normative file — see §4 and §5; R23 already routes it to PREREG.md lines 1050 and 97 independently of this bucket** |
| 127 | §D.2 | The verbatim five-line v30 tag block; "why the sixth"; the two discharged lock-time obligations | INST | | The read state of this repository's tag |
| 128 | §D.3 | **A decision-log interpretation of locked text may resolve ONLY toward the STRONGER reading** | **GC** | N | Its own enumerated objects *are* gate arithmetic: narrowing a denominator, exempting a column, softening a criterion, admitting an excluded set, converting a required finding into optional, converting an unscored cell into a pass |
| 129 | §E | The **gate input surface**: two things, one side at a time; the map, the paired side, and the other side's predictions are NEVER received | **GC** | N | A detector that reads the scoring key is graded against a key it saw — the run measures retrieval, and its PASS is not the gate's PASS |
| 130 | §E | **One side at a time is a hard sequencing rule:** a single run given both sides satisfies none of the criteria | **GC** | N | Stated as a verdict rule — such a run cannot pass, however its outputs are partitioned afterwards |
| 131 | §F.1 | An "every X in the archive" claim rests on a filesystem walk and **must not be re-verified with a default-excluded search** | **NG** | N | Archive-survey method; it governs how declaration evidence is gathered, not how a verdict is computed |
| 132 | §F.1 | The 37 vs 119 table and its capture citation | INST | | This archive's measurement |
| 133 | §F.2 | Every number read from a named artifact; class set / side / boundary / generation named at point of use | **NG** | | Provenance discipline for published numbers |
| 134 | §F.3 | **THE ALL-ZERO CONTROL:** any aggregate reporting zero MUST be cross-checked against its source before it is written down; **on mismatch it RAISES** | **GC** | N | Under criterion 3 a zero-violation aggregate *is* a pass claim; the file's own near-miss shows a broken-key zero reading as "the corrected side is clean" |
| 135 | §F.3 | **SCOPE: this binds future gate reporting** — per-criterion counts, false-positive tallies, any statement that a column, class, cell or criterion is clean | **GC** | N | Without the scope clause, row 134 binds only this file and the gate's own zeros go unchecked |
| 136 | §F.3 | The provenance of the near-miss — caught by visual inspection, "performed by luck" | INST | | The account of one pass on this fixture; H2's steer: keep it here |
| 137 | §18 | The element-to-evidence index | INST | | An index of this file's own sections |
| 138 | Tail | Working resolutions R1–R13 verbatim | INST | N (R13) | An append-only **record** of what was resolved; it stays byte-identical. R9's and R11's *normative* content moves via rows 55 and 31; **R13's has no carrier at all — see §4** |

---

## 4. THE 40 HOMELESS ROWS — EACH BY ID

**Split: 26 GATE-CRITICAL · 13 NON-GATE · 1 INSTANCE.**

> **The headline for H1's drafting: 26 of the 40 rows that would otherwise be stated normatively
> nowhere are rules the gate's PASS/FAIL depends on.** These are not clauses to amend — there is no
> clause. They must be created.

**GATE-CRITICAL (26) — H1's diff must CREATE a PREREG.md clause for each:**

| Row | Ruling in one line |
|---|---|
| **3** | GC — pre-lag/post-lag `column_roles` semantics fix the availability instant of every fed column |
| **4** | GC — a positional label horizon is a new **unit** for §2.4 and a declared detector input |
| **7** | GC — enumerates the gate's extent ("the four criteria as amended are the whole gate") |
| **11** | GC — bounds what may be admitted as an availability difference, i.e. what the fixture is |
| **28** | GC — decides whether §10.2's ambiguity branch fires. **Rejected by R22; see §6** |
| **35** | GC — rule-vs-frozen disagreement halts the run; a halt is not a PASS |
| **44** | GC — L2a jurisdiction boundary; decides whether an L2a finding fails criterion 2 or 3 |
| **46** | GC — `UNSCORED` as a **column-level coverage state** and its gate consequences |
| **58** | GC — criterion 4's sentinel; without it a firing on the 2^32 signature fails criterion 4 |
| **62** | GC — the definition of `waived`, which gates §10.2's replacement criterion |
| **63** | GC — the prohibition; a waiving replacement criterion is inadmissible on its face |
| **64** | GC — limbs 4 and 6 independently change admissibility |
| **72** | GC — (b) both-branch counts informational; no gate outcome may be computed from them |
| **80** | GC — a declared cohort must be checkable pre-run, or it is a key shaped by results |
| **82** | GC — `UNSCORED` at **cell level**; decides whether the 72 cells license a corrected-side pass |
| **85** | GC — a declared non-gated diagnostic enters no denominator; a **sixth body of data** against §6.1's five |
| **90** | GC — an all-zero return is a FINDING, not a pass |
| **96** | GC — `at_bar_close` is never scored against; the other reading finds the contaminated side clean |
| **101** | GC — duplicate of 44 at §C.3; same consequence |
| **123** | GC — §13(h) unfrozen only on condition it never enters an acceptance denominator |
| **124** | GC — no gate outcome from the non-declared tie branch |
| **128** | GC — §D.3's stronger-reading rule; its enumerated objects are gate arithmetic verbatim |
| **129** | GC — the gate's input surface; withholding the map is what makes the run discrimination |
| **130** | GC — one side at a time; a both-sides run satisfies no criterion |
| **134** | GC — the all-zero control; a broken-key zero converts a FAIL into a PASS |
| **135** | GC — the scope clause that puts 134 on the gate report's own counts |

**NON-GATE (13) — `PRACTICES.md`, non-normative, per R21. Three of them are flagged in §5 as
rows where that outcome is uncomfortable:**

| Row | Ruling in one line |
|---|---|
| **8** | NG — WR authority; the gate reads §D.1's frozen objects, not the ledger. **§5 flag** |
| **9** | NG — supersession over an append-only ledger; no criterion reads it |
| **18** | NG — evidence artifacts never adjusted toward a decision. **§5 flag** |
| **47** | NG — EXCLUDED-not-MISSED is the *word*; the exclusion itself (row 103) is GC |
| **68** | NG — licenses an interpretation of the AUC delta, which §6.1 line 441 calls provenance |
| **70** | NG — a lag-image is not independent corroboration; evidence accounting only |
| **87** | NG — both-maps publication obligation; the "not a second scoring key" limb is row 89 (GC) |
| **111** | NG — governs summary-level quotation; per-cell figures and their adjudication unchanged |
| **113** | NG — R4's supported/qualified claim split; criterion 4's rule on the same defect is row 58 |
| **115** | NG — the documented-unverifiable *category*; a disclosure discipline |
| **117** | NG — the F2 projection rule, which row 50 rules explicitly out of the gate-scored fixture |
| **126** | NG by R21's test — **but it reaches PREREG.md anyway under R23. §5 flag** |
| **131** | NG — archive-survey method; governs evidence gathering, not verdict computation |

**INSTANCE (1):**

| Row | Ruling in one line |
|---|---|
| **138** | INSTANCE — the tail is an append-only **record** and stays byte-identical. **But R13's normative content ("evidence artifacts are never adjusted toward a decision") has no carrier: row 18 is its only other statement and row 18 is NON-GATE. Under R21 as written, R13's rule ends up in a file that binds nothing. §5 flag.** |

---

## 5. NAMED CALLS ON THE HEAVY ONES

**(a) The `waived` definition — rows 62, 63, 64. All three GATE-CRITICAL.**
The reasoning is conditional, and R22 supplies the condition. §A.12 defines a word used at
PREREG.md line 1035 (the §10.2 replacement-criterion floor) and at line 855 (a §7.7 coverage
state). The floor is live only if §10.2's ambiguity branch fires. §A.5 (row 28) says it does not.
**R22 rejects §A.5's reading**, so the branch fires, the replacement criterion is owed, and the
floor that constrains it is in force. A definition that decides whether a replacement *acceptance
criterion* is admissible decides a PASS/FAIL. Within the row: 62 is the definition, 63 is the
operative prohibition, and in 64 the load-bearing limbs are **4** ("no data" is not "waived" — it
is UNSCORED) and **6** (per-combination waiving is still waiving); limbs 1, 2, 3, 5 and 7 are guards
over the same ground and would survive as `PRACTICES.md` commentary if the author wanted to trim.
**They should not be trimmed** — §A.12 exists because an undefined word in a floor gets read
permissively later, and a guard in a non-binding file is not a guard.

**(b) §D.3's interpretation rule — row 128. GATE-CRITICAL, and it is the load-bearing one.**
It is the largest pure-rule block outside §A.12 and it has zero fixture content. Its own enumerated
prohibitions — "narrows a denominator, exempts a column, softens a criterion, admits an excluded
set, converts a required finding into an optional one, or converts an unscored cell into a pass" —
are a list of six ways the gate's verdict can be flipped by a decision-log entry. It is also the
rule R22 is currently *applying* to reject §A.5. A rule that is being used right now to settle a
gate-critical question cannot live in a file that binds nothing.

**(c) §E's gate input surface — rows 129, 130. Both GATE-CRITICAL.**
Row 129: under the amended criterion 3 the map **is** the scoring key. A detector that receives it
is graded against a key it has seen, and the run measures retrieval rather than discrimination —
its PASS is not the gate's PASS. Row 130: the corollary states its own verdict consequence, that a
single run given both sides "does not satisfy any of them, however its outputs are partitioned
afterwards." Both are entirely fixture-independent: any acceptance-fixture gate run has this
surface. PREREG.md's §6.2 gate framing currently specifies *what* is evaluated and never *what the
evaluated thing is allowed to see* — the largest silent hole the scrub found.

**(d) §F.3's all-zero control — rows 134, 135. Both GATE-CRITICAL, and 135 is why.**
Row 134 is the control: an aggregate reporting zero must be proved empty before it is written down,
and on mismatch it RAISES rather than warning. Under the amended criterion 3, **a zero-violation
aggregate is a pass claim** — the file's own near-miss (row 136) is the proof: an aggregation keyed
on wrong column names returned all zero and would have read as "the trade-class restriction makes
the corrected side clean." That is a FAIL rendered as a PASS by a broken key. Row 135 is the scope
clause and is not severable: it is what puts the control on "the gate report's per-criterion counts
and its false-positive tallies" rather than on this file alone. **Row 135 says of itself that it
binds beyond the declaration — under R20 that is the definitional test for something that cannot
live in a fixture declaration.** Keep 136 (the near-miss narrative) in the declaration; it is
evidence, and a rule without its near-miss is a rule nobody believes.

**(e) The SIX-hash declaration — row 126. NON-GATE by R21's test, and that is the wrong answer.**
Strictly applied, R21 test 2 fails: a gate run computes its verdict from the frozen §D.1 objects
and never reads the tag message. But four different hash counts are now in play — PREREG.md line
1050 says three, line 97 says "both", the executed `prereg-v30` tag carries five, the declaration
declares six — and PREREG.md line 97 makes the integrity chain a *validity* condition of the
amendment ("An amendment weaker than the thing it amends is not one"). A defective chain
invalidates the amendment that carries the amended criterion 3, which **is** gate-critical. So the
dependence is real but at one remove, which R21's binary test cannot express.
**Practical disposition: it reaches PREREG.md regardless of bucket, because R23 already directs
amending lines 1050 and 97 so the tag message carries the SHA-256 of every registered document and
tool as committed, with the count derived rather than stated.** R23 disposes of row 126; R21's test
should not be asked to.

**(f) `UNSCORED` as a coverage state — rows 46 (column level) and 82 (cell level). Both
GATE-CRITICAL, and they are two rows because they are two levels.**
PREREG.md line 855's state list is `passed, failed, not_applicable, unsupported,
could_not_run(reason), waived`. `UNSCORED` is not in it. PREREG.md line 93 names "a needed *new*
coverage state" as class C **verbatim**, so this is class C on the registration's own words.
Gate-dependence is direct in both rows and identical in shape: the state's defining consequence is
"cannot be reported as a pass," which is a verdict statement. Row 49 must move with them — it is
the rule that keeps the two levels from collapsing ("a cell-level unscored never makes a column
unscored"), and without it the 72 cells would put `nq`'s columns out of the arithmetic. **Note for
drafting: `UNSCORED` must be added to §7.7's table AND §8.2's not-run list, and §8.2's closing
sentence — "None may be displayed in a way mistakable for a pass" — is the existing hook the new
state should attach to.**

**(g) The positional label horizon — row 4. GATE-CRITICAL.**
§2.4's registered formula is `a(y_j) = label timestamp + label horizon + publication delay`, with
the horizon a duration. The declaration replaces the horizon's **unit** with a positional one — the
`timestamp` of the row h positions after row t on the filtered frame. A unit change to a registered
formula is class C on line 93's face ("a needed *new* branch, **unit**, denominator, coverage
state, tier licence, or acceptance criterion"). Gate-dependence: `label_availability` is one of the
declared elements §E hands a detector at gate time, and the positional reading is what makes the
2,100 cross-boundary rows next-session realizations (up to 3d 19:31:00) rather than `t + h` seconds.
A conforming detector adjudicates those rows differently under the two units. **This is not in the
four-amendment ledger and has no PREREG clause.**

**(h) "`at_bar_close` is never scored against" — row 96. GATE-CRITICAL, and the declaration says so
itself.** The passage states the flip in terms: gate arithmetic using `at_bar_close` as the
availability instant for a join-family column "would score the fixture against the wrong comparator
and would find the contaminated side clean." A rule whose stated consequence is that the gate finds
the contaminated side clean is the definition of gate-critical. It is pure §2.3 line 205 vocabulary
semantics — what a `column_roles` value means relative to the comparator — with zero fixture
content, **and it is not in the four-amendment ledger either.**

**(i) Three NON-GATE calls the author should look at before accepting the bucket — rows 8, 18, and
138's R13.** R21's two-part test, applied honestly, routes **registration-integrity rules into a
file that binds nothing.** Row 18 and R13 say "evidence artifacts are never adjusted toward a
decision" — a rule about not editing the manifest toward a wanted answer. Row 8 says delta-issued
working resolutions carry the same authority as recorded ones. Neither changes a verdict *given an
honest run*; both are what make the run honest. Under R21 as written they go to `PRACTICES.md`,
which "binds nothing, is not a normative annex, is not cited by `PREREG.md`". **That is a real
consequence of the scope rule, not a mistake in applying it, and it is the second reason — after
the count — that the author should revisit scope before drafting.** J1 has not resolved it in either
direction; the calls above apply R21 as written.

---

## 6. THE R22 DETERMINATION — SEPARATE DELIVERABLE

### 6.1 The two texts, verbatim

**PREREG.md line 1033** (the blockquote under §10.2 criterion 2), verbatim:

> On a Phase 0 finding of ambiguity: **record it, pause runtime development, commit and timestamp a class C amendment carrying the complete replacement criterion — unit, threshold, and denominator — and only then begin Phase 1 development or inspect the development corpus.** No `DEVIATIONS.md`-only criterion, and no development-corpus access until the branch is resolved (§10.0).

**PREREG.md §10.2 criterion 2** (lines 1030–1031), verbatim:

> 2. **The runtime detectors cannot separate contaminated from corrected fixture under the reconstructed declaration** → **stop.**
>    **Where the fixture is semantically ambiguous** (§6.2), this criterion is replaced, not deleted — **and the replacement is written before any development-corpus contact, not after tuning.** *(v23 permitted it after tuning, in `DEVIATIONS.md` alone, floored only at non-zero proof yield. An acceptance criterion is a class C semantic object by §0.2.1's own definition, and choosing its unit and threshold after seeing development behaviour can determine whether Phase 2 passes. It also contradicted §7.0's invariant, which requires a metric specification to precede corpus inspection and tuning — the carve-out and the new rule could not both stand.)*

**The floor that constrains the replacement, PREREG.md line 1035**, verbatim, because the
determination turns on it:

> The replacement may be stricter than the floor and may not be weaker: non-zero proof yield, neither runtime detector waived, criterion 3's gates in force. Committing it before knowing which criterion is practically useful is the cost of the ex-ante property — a criterion chosen because it works after tuning is a criterion shaped by tuning.

**R9, from the declaration's frozen tail (line 3671), verbatim:**

> **R9.** The acceptance gate scores against a DECLARED GROUND-TRUTH MAP on both fixture sides, not against an assumed-clean corrected side. §6.2 criterion 3 is amended within this class C registration: old — no findings on any corrected column; new — detector findings must match the declared per-side, per-class, per-instrument-month violation map; findings the map predicts are required, findings it excludes are false positives, cells the map does not cover are unscored. The corrected side is described throughout as CHARACTERIZED, never clean.

### 6.2 THE DETERMINATION: **NO.**

**R9's criterion-3 amendment is not the replacement criterion line 1033 requires, and it does not
supply line 1033's three parts.** Two independent grounds; either alone is sufficient.

---

**GROUND 1 — WRONG OBJECT. The text forecloses it.**

Line 1033's replacement replaces **§10.2 criterion 2**: *"The runtime detectors cannot separate
contaminated from corrected fixture under the reconstructed declaration → stop."* That is a
**kill/pause criterion over the runtime detectors**.

R9 amends **§6.2 criterion 3**: *"No runtime finding of any tier, primary or secondary, appears on
`fixture_corrected`."* That is one of four **fixture acceptance criteria**.

They are different objects at different levels, and **line 1035 says so explicitly**. The floor's
third limb is "**criterion 3's gates in force**." Criterion 3 is named as a **component of the floor
that constrains the replacement**. A thing named as a constraint *on* the replacement cannot also
*be* the replacement — the floor would then read "the replacement may not be weaker than itself,"
which is vacuous. Line 1035 requires the replacement to hold criterion 3's gates in force **and**
add non-zero proof yield **and** waive neither runtime detector. R9 supplies a modified version of
the third limb only.

**Under §D.3's rule (row 128), reading R9 as discharging line 1033 is the weaker reading on its
face** — it converts a required amendment into one already made, i.e. converts a live obligation
into a satisfied one. §D.3 permits resolution only toward the stronger reading. R22 has already
applied exactly this rule to reject §A.5; the same rule rejects this reading.

---

**GROUND 2 — MISSING PARTS. Tested against line 1033's own three-part requirement, even taking R9
as a candidate on its merits.**

| Part | Supplied? | Exactly what text does / does not supply it |
|---|---|---|
| **UNIT** | **PARTIAL — and not for the limb that needs one** | R9 *does* supply a scoring unit for criterion 3: the **(side, class, instrument-month) map cell**, given its schema at declaration §13(a) line 1960–1961 (`side, instrument, month, class, boundary, strict_count, equal_count, rows, scored_flag, missing_path`, one row per scored cell). But line 1035's first floor limb is **non-zero proof yield**, whose unit in PREREG.md is the **labelled leaking source at PROVEN tier** (line 472: "k of N labelled leaking sources received at least one primary PROVEN finding **attributed to that source**"). **R9 supplies no proof-yield unit and names no tier at all** — its criterion is tier-agnostic. The unit for the limb the floor actually floors is absent. |
| **THRESHOLD** | **NO** | R9 supplies a **match condition** for criterion 3 (predicted findings required, excluded findings are false positives), and §A.8 line 1431–1432 sharpens it ("A finding on a corrected-side cell the map marks zero is still a false positive and still fails the gate"). A match condition is not the threshold line 1033 asks for. **No number is stated anywhere** for the replacement: not a k, not an N, not a proof-yield floor. The closest candidate — §A.10's *k* of *N* = 11 — is explicitly **not a gate threshold**: PREREG.md lines 470–476 report proof capability *instead of requiring it*, and publish it "as a count, never as a decimal or percentage … a **descriptive fixture outcome** rather than a performance rate." Converting a declared non-gating descriptive count into the replacement's threshold is itself an act of registration, and nobody has performed it. |
| **DENOMINATOR** | **NO** | R9 supplies none. Three candidate denominators exist in the file and **none is nominated as the replacement's**: (i) §A.6.4's **11 REQUIRED columns**, which rows 29 and 59 declare to be *criterion 1's* denominator specifically; (ii) the map's **960 scored cells** of 984 (§13(a)); (iii) the **18 of 48 instrument-months** carrying corrected-side violations (§A.8 line 1425). Choosing among these changes the replacement's outcome, which is precisely why line 1033 names denominator as a separate required part. |

---

**A THIRD FINDING, recorded because it is worse than a gap.** Adopting R9's map-scored criterion 3
as the §10.2 replacement would **violate line 1035's second limb on the declaration's own
definition of the word.**

Line 1035 requires "**neither runtime detector waived**." The two runtime detectors are **L2a and
L3.1** (§A.12 line 1543–1544, citing PREREG.md lines 318, 320 and line 1039). The declared map is
an **availability**-violation map scored by L3.1; R9 says nothing about label availability. And the
declaration twice removes L2a's findings from this gate: §A.6.2 (row 44) — "**An L2a label-base
finding on them is neither credited nor penalized by this availability gate**" — and §C.3 (row 101),
which routes label-base character "to L2a jurisdiction and OUTSIDE this availability gate."

Measured against §A.12's own definition (declaration lines 1548–1556), a replacement criterion
consisting of R9's map-scored criterion 3 satisfies limb **(i)** (L2a excluded from the criterion's
denominator), limb **(ii)** (its findings not required to be non-empty for a pass), and limb
**(iii)** (the criterion is satisfiable by the other detector's output alone). **That is L2a waived,
three times over, by the declaration's own text.** So R9 is not merely an incomplete replacement —
as a replacement it would be *weaker than the floor*, which line 1035 forbids outright and §A.12
line 1560–1562 says "does not become admissible by being recorded, disclosed, justified, or
approved."

---

### 6.3 WHAT IS STILL OWED — stated precisely, and not closed by interpretation

Line 1033's obligation is **live and unmet**. J1 does not close any part of it by construction from
existing text. Owed:

1. **A replacement for §10.2 criterion 2, stated as such** — a criterion saying what the runtime
   detectors must achieve *in place of* separating contaminated from corrected under a
   non-ambiguous reconstructed declaration. R9 amends §6.2 criterion 3 and is silent on §10.2.
2. **A UNIT for the non-zero proof-yield limb** — the labelled leaking source at PROVEN tier per
   line 472, or an explicitly declared alternative. R9 names no tier.
3. **A THRESHOLD — a number.** None exists. §A.10's *k* of *N* = 11 is registered as a descriptive
   non-gating count (lines 470–476) and cannot be silently promoted.
4. **A DENOMINATOR for the replacement**, nominated among the 11 REQUIRED columns, the 960 scored
   map cells, or the 18-of-48 instrument-months — or a fourth, declared.
5. **An L2a limb that keeps L2a unwaived** under §A.12 limbs (i)–(iii), given that rows 44 and 101
   place its findings outside this gate. Without it the replacement is inadmissible on the
   declaration's own definition, not merely incomplete.

**Two procedural consequences of the branch being live, recorded so they are not overlooked:**

- Line 1033 also requires "**pause runtime development … and only then begin Phase 1 development or
  inspect the development corpus**," and "**no development-corpus access until the branch is
  resolved (§10.0)**." §10.0 step 0 repeats it: *"If Phase 0 recorded the fixture as semantically
  ambiguous, the class C amendment of §10.2 is committed and timestamped before anything below —
  including any development-corpus access."* **Phase 1 may not begin until items 1–5 above are in a
  committed, timestamped class C amendment.**
- Row 28 (§A.5's reading) is **GATE-CRITICAL and rejected**. It is currently the only text switching
  the branch off, it is not in the four-amendment ledger, and it has no PREREG clause. The drafting
  consequence is that PREREG.md line 449 must be **explicitly amended** if the branch is to be
  switched off — R22's own words: "line 1033's obligation stands unless line 449 is explicitly
  amended." An amendment to line 449 is itself class C and would need to state, on the record, that
  documented-and-violated timing does not trigger the ambiguity clause.

*(Incidental, noted once: §10.2's enumeration begins at item 2 — there is no item 1 in the printed
list. Not load-bearing for this determination, but it is a defect in a section the amendment must
touch.)*

---

## 7. LIMITS OF THIS PASS

1. **No file was edited.** `PREREG.md`, `AVAILABILITY_DECLARATION.md`, `DESIGN.md` and `HISTORY.md`
   are untouched; no git command was run; the archive at `C:\Users\ttbea\OneDrive\Desktop\MBO_2025`
   was not read.
2. **Row statements and line ranges are inherited from H2's scrub list**, spot-verified this pass
   against the declaration for rows 3, 4, 5, 28, 46, 49, 50, 55, 56, 58, 62–64, 74, 82, 85, 90, 96,
   123–126, 128–130, 134–136 and 138. Rows not spot-verified were classified from H2's one-line
   statements plus their cited PREREG surface.
3. **The R/I split is H2's and was not re-litigated.** J1 subdivides H2's 102 RULE rows only; the
   36 INSTANCE rows pass through unchanged. H2's own uncertainty flags on rows 13, 61, 117 and 138
   stand — of those, J1 buckets 13, 61 and 117 as NON-GATE and 138 as INSTANCE, so none of them is
   load-bearing for the gate-critical count.
4. **Mixed rows were bucketed by their strongest limb**, and the split is named in the row's
   justification. This affects rows **60** (reporting limbs non-gate, adjudication limb gate-critical),
   **72** (comparator limb and informational limb), **75** (class-set limb gate-critical, "name your
   class set" limb reporting), **83** (labelling limb non-gate) and **120** (freeze-form limb
   gate-critical, report-reproduction limb non-gate, overlapping row 51). If the author prefers
   finer granularity, these five rows split into eight.
5. **"Acceptance gate" was read as the §6.2 four-criterion pass gate**, plus the Phase-gate
   conditions of §10 line 992 that evaluate the same fixture (rows 14, 25, 26), plus §10.2's
   replacement criterion where it is live (rows 28, 62–64). Narrowing the reading to §6.2 alone
   removes at most 7 rows (14, 25, 26, 28, 62, 63, 64) and leaves GATE-CRITICAL at **69** — the
   stop-and-report still fires by more than 2×.
