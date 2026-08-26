# PRACTICES.md — non-normative working practices carried out of the v30a availability declaration (item K3)

## Preamble — what this file is, and what it is not

**This file binds nothing.** No sentence in it is a rule anyone is obliged to follow, no gate
verdict depends on anything written here, and no number published by the programme changes its
meaning if this file is edited, emptied, or deleted. It carries no obligation of its own and creates
none.

**This file is not a normative annex.** It is not part of the registration, it is not hashed in any
tag message, it does not inherit `PREREG.md`'s integrity chain, and nothing in it may be read as
amending, extending, softening, or interpreting any clause of `PREREG.md` or any declared element of
`AVAILABILITY_DECLARATION.md`. Where a sentence below resembles a registered rule, the registered
rule governs and this sentence is a description of how one pass of work chose to apply it.

**`PREREG.md` does not cite this file.** Under working resolution R21, `PREREG.md` is the single
normative source for measurement semantics and it references nothing here. The availability
declaration may point to an entry below where a practice was removed from it by the K4 scrub, and
such a pointer is a breadcrumb for a reader, not a citation of authority.

**What the contents are.** The nineteen entries below are the rows of the v30a declaration scrub
that J1 classified NON-GATE and that K1, applying R25, left outside `PREREG.md`: reporting,
provenance, labelling, and evidence-accounting practices that neither determine a gate verdict nor
protect the integrity of a declared instance. They were found useful in the Phase 0 work and are
recorded so they are not lost. **They are candidate input to Phase 1's registration work — to be
designed then, under Phase 1's own registration, and not reverse-engineered now from this list.**
Nothing here pre-empts, constrains, or forecasts what Phase 1 registers.

**Scope and provenance.** Source rows are identified by the J1 row id
(`J1_GATE_CRITICAL_CLASSIFICATION.md` §3) and K1's disposition table (`K1_SCHEMA_CLAUSES.md` §3,
"REMAINING PRACTICES (19 rows)"). Declaration line numbers are those of the scratch copy before the
K4 scrub (`applied\AVAILABILITY_DECLARATION.md`, 3,695 lines, sha256 `1290186e…1c30`); the scrub
replaces each source passage with a pointer to the entry here (K4_SCRUB_DIFF.md records every such
edit). The entries are numbered by their J1 row id (P-02 is J1 row 2, and so on) so the mapping is
checkable without a concordance.

---

## The nineteen entries

Each entry states: the practice, in this file's own words; its source section in the declaration (the
passage the scrub removes or re-points); and, in one line, why it is neither gate-determining nor
integrity-protecting. Where a registered clause already carries the substance, it is named, because
a reader should go there and not here.

### P-02 — Generation naming on every row count

**The practice.** Whenever a lattice row count is written down, write beside it the path the rows
were read from, the generation of that file (here `v3_pre_gapfill` or `v4_gapfill`), and the file's
sha256 — so that two counts from two generations of "the same month" can never be read as one.

**Source.** Declaration Part I §2 `bar_duration`, the bullet "Generation-naming rule (M1/N2), binding
on every row count in this file" (scratch lines 234–244).

**Why here.** No criterion reads a path or a hash; the obligation that every published number state
its provenance is already `PREREG.md` §8.6's. This entry holds only the specific naming form.

### P-10 — A measurement claim names the artifact it was measured on

**The practice.** Every measurement claim names which of the two fixture artifacts it rests on —
Artifact A (the f2 rebuild pair, where timing is measured) or Artifact B (the stored-prediction pair,
where the gate scores) — or says explicitly that it is a measurement of the archive itself. A claim
naming neither is treated as unpublishable until it does.

**Source.** Declaration Part II §0.3, "Reading rule, binding on this file and on any gate report"
(scratch lines 678–685).

**Why here.** It shapes how a claim is labelled, not what any verdict is; the lattice bridge between
the two artifacts is this fixture's instance and stays in the declaration.

### P-13 — The walk does not classify its own amendments

**The practice.** A conformance walk records, for each amended element, that the amendment's class is
the registration's to state (`PREREG.md` §0.2.1 lines 93 and 95 and the amendments block), and makes
no class assertion of its own.

**Source.** Declaration §A.0, "Every AMENDED entry below is a class C amendment carried by this
registration" (scratch lines 766–767).

**Why here.** A classification assertion about the walk's own entries; the verdict does not read the
amendment class and `PREREG.md` §0.2.1 already governs it. In the declaration it is now a citation.

### P-20 — A quoted leaking-source count names the scope it counts under

**The practice.** Where two manifests give two counts of independently leaking sources over two
scopes (here 25 over the fed 35-column set, 22 over the F2-reconstructible subset), every quotation
of either count names which scope it counts under.

**Source.** Declaration §A.2, closing sentence "Any gate report quoting a leaking-source count must
name which of the two scopes it counts under — that is a declared reporting obligation, not a
convention" (scratch lines 877–878).

**Why here.** The count is the same either way and enters no gate arithmetic (`PREREG.md` SC-4(a)).
**Flag — see §3 below:** SC-4(a) as applied ends "Any report quoting such a count names the scope it
counts under", which is this practice verbatim; the scrub cites SC-4(a) and points here.

### P-47 — Excluded units are named EXCLUDED, not MISSED

**The practice.** A unit declared out of the scored arithmetic before any run (here `buy_volume_10s`,
a dead-zero column) is reported under the word EXCLUDED, never under the word MISSED, so that a
declared exclusion is never read as a detection failure.

**Source.** Declaration §A.6.3, first bullet, "Must be named in the gate report as EXCLUDED, never as
MISSED" (scratch line 1247); §C.4(a), last sentence (scratch lines 2828–2829).

**Why here.** The exclusion itself is gate-critical (J1 row 103 → `PREREG.md` SC-4(e)); the word used
for it is vocabulary. **Flag — see §3 below:** `PREREG.md` SC-11(g) as applied reads "excluded units
remain excluded and are never reported as missed"; the scrub cites SC-11(g) and points here.

### P-51 — The partition check is shown, not asserted

**The practice.** Where a declaration partitions a set, it prints the check — the class sizes, their
sum, the identity with the declared set's size — in the declaration itself, so a reader verifies a
partition rather than trusting one.

**Source.** Declaration §A.6.4 heading "(must be reproduced by any gate report)" and its closing
sentence "a partition asserted but not shown is a partition nobody verified" (scratch lines
1268–1280).

**Why here.** The report-facing phrasing; the gate-critical twin (J1 row 120 → `PREREG.md` SC-8(b),
SC-4(f)3) carries the freeze form and the not-scored consequence. **Flag — see §3 below:**
SC-4(f)3 as applied reads "The partition check is printed and reproducible by any gate report"; the
scrub cites SC-4(f)3 and points here.

### P-61 — A walk summary is not the amendment ledger

**The practice.** A conformance walk's summary table lists the sites it walked and their verdicts; it
does not count or enumerate what the amendment comprises, which is the amended registration's own
amendments block's job. A count in a walk summary ("four amendments") is a count of walked sites,
not of amendment objects.

**Source.** Declaration §A.11, the walk summary table and "Four amendments (445, 450, 451, 461)"
(scratch lines 1507–1532).

**Why here.** Ledger bookkeeping; no criterion reads it. J1 records that the count "four" is
falsified by the object count the schema set introduces, which is exactly why the ledger of record is
`PREREG.md`'s amendments block and not a walk table.

### P-65 — Status bookkeeping for amendment content carried in a declaration

**The practice.** Where a declaration carries the text of a class C amendment ahead of the tag, it
marks the text PROVISIONAL until the tag is signed and records that, once registered, the text is
frozen with everything else — and says no more about its own authority than that.

**Source.** Declaration §A.12, "Status: class C amendment content added by v30a, PROVISIONAL until
the `prereg-v30a` tag is signed, and frozen by §D.1 thereafter … by §D.3's rule it resolves toward
the stronger reading" (scratch lines 1605–1608).

**Why here.** Status bookkeeping. The stronger-reading rule itself is `PREREG.md` SC-9(e) (J1 row
128) and the definition is SC-12; neither is this entry's.

### P-68 — Reading a pre/post AUC delta as an availability-only effect

**The practice.** Before reading the AUC delta across a pre/post pair as a feature-availability
effect, check and record that the two sides share one label vector, one label base, and one
evaluation population — and record what that check does not establish (a shared feature set is a
separate question).

**Source.** Declaration §9, "This is the licence for reading the pre/post AUC delta as a
feature-availability-only effect" (scratch lines 1675–1680).

**Why here.** It licenses an interpretation of a provenance figure (`PREREG.md` §6.1 line 441: the
fixture's AUCs are provenance); the fixture-admission limb — that the sides differ in availability
and nothing else — is `PREREG.md` SC-2(c)'s (J1 row 11) and is not this entry's.

### P-70 — A lag-image is not independent corroboration

**The practice.** When one measurement is the positional re-indexing of another (here corrected-vs-
`t-1` is contaminated-vs-`T` shifted one row), their agreement is recorded as a consistency check,
not counted as an independent confirmation; independent confirmations are named separately.

**Source.** Declaration §10, "Corrected-vs-(t-1) is the LAG-IMAGE of contaminated-vs-T, not a third
independent measurement" (scratch lines 1721–1730).

**Why here.** Evidence accounting for the declaration's own diagnostics; no criterion reads it.

### P-77 — A ranking is quoted with its metric

**The practice.** Any ranked list of cells names the metric it is ranked by (rate or absolute count),
because the two orders differ and a list without its metric cannot be read.

**Source.** Declaration §13(b), "THE RANKING BELOW IS BY RATE … The metric is named because the rate
order and the absolute-count order are different orders" (scratch lines 2008–2011).

**Why here.** Reporting legibility; the same cells rank either way. For peaks specifically the
requirement is registered (`PREREG.md` SC-10(d)(4): a peak is quoted with its class set and its
metric); this entry covers full rankings.

### P-83 — A partially-covered unit carries its coverage label on every appearance

**The practice.** A unit scored over only part of the declared class set (here nq, scored on the four
trade classes and unscored on the six MBO classes) carries its coverage label ("TRADES-CLASSES-ONLY")
and the correct reason for the gap on every appearance in every table, never only where the gap is
explained.

**Source.** Declaration §13(g), closing paragraph "Whenever nq appears in any table in this file or
in any gate output, it must carry the TRADES-CLASSES-ONLY label together with the correct reason"
(scratch lines 2227–2234); also §14 item 4.

**Why here.** Labelling. The denominator limb (the unscored cells enter no arithmetic; moving the
diagnostic in is class C) is `PREREG.md` SC-6 / SC-10 (J1 rows 82, 85, 123) and is not this entry's.

### P-87 — Two views of one map are published side by side

**The practice.** Where a map is re-aggregated over a narrower class set for reporting, the full map
as measured and the restricted view are published together, with the delta between them stated as
a separate factual paragraph, and neither is described as replacing the other.

**Source.** Declaration §13(i), "The obligation, stated first. Delta-issued working resolution
R17(ii) requires both maps to be published side by side with the delta explicit" (scratch lines
2338–2344); §14's both-profiles banner.

**Why here.** A publication obligation; the "not a second scoring key" limb is `PREREG.md` SC-3(e)
(J1 row 89). **Flag — see §3 below:** SC-3(e) as applied also reads "Where two views of the map are
published, both are published with their delta explicit and neither replaces the other"; the scrub
cites SC-3(e) and points here.

### P-111 — Summary-level peaks exclude coverage-artifact cells

**The practice.** Where the unqualified maximum of a restricted surface is a cell whose restricted
and full-class figures coincide only because the cell has nothing to drop (a coverage artifact, here
nq), a summary-level statement of "the peak" names the next cell (the EX-NQ figure), and the
coverage-artifact cell appears only as a per-cell entry carrying its label and reason.

**Source.** Declaration §14 item 4, "BINDING — the EX-NQ figures are the summary-level peaks"
(scratch lines 3116–3129); §14.1's reference to it (scratch lines 3208–3211).

**Why here.** It governs summary-level quotation only; the per-cell figures, their class-set and
metric labels (`PREREG.md` SC-10(d)(4)), and their adjudication are unchanged.

### P-113 — Claims are split into timing-structural and value-dependent

**The practice.** Where a fixture carries an as-built value defect (here the uint32 wrap and the
dead aggressor classifier), every claim that rests on the affected columns is sorted into
timing-structural (supported — it does not depend on the numeric values) or value-dependent
(qualified — it does), and the split is recorded beside the claims.

**Source.** Declaration §15, "Claims split per R4" (scratch lines 3258–3267).

**Why here.** Evidence accounting for published claims; criterion 4's treatment of the same defect is
`PREREG.md` SC-5(f) (J1 row 58, via the declaration's §A.9 sentinel) and is not this entry's.

### P-115 — Documented-unverifiable assumptions are recorded as a category

**The practice.** Assumptions the declaration relies on that no archive record can verify are
collected under one heading, each with the basis on which it is accepted and the record that fails to
verify it, rather than being absorbed silently into the text that depends on them.

**Source.** Declaration §16, "Assumptions the declaration RELIES ON that no archive record can verify;
recorded as such" (scratch lines 3291–3298).

**Why here.** A disclosure discipline; it changes no verdict. The three items themselves (J1 row 116)
are this fixture's premises and stay in the declaration in full.

### P-117 — A rebuild projection is selection or renaming only

**The practice.** When an independently rebuilt artifact is projected onto a target column set to
check self-consistency, the projection selects or renames existing columns and synthesizes nothing;
a column that would need new construction is recorded unconstructible with its reason.

**Source.** Declaration §17, "Projection of the F2 fixture builds onto the 35-column Phase 7 model
set, selection or renaming only (nothing synthesized)" (scratch lines 3334–3335).

**Why here.** A method rule for the F2 rebuild, which `PREREG.md` SC-4(d)(ii) (J1 row 50) rules
explicitly out of the gate-scored fixture; the cleanest non-gate call in the set.

### P-131 — Archive-wide surveys use a filesystem walk

**The practice.** A claim of the form "every X in the archive" rests on an exhaustive filesystem walk
and is not re-verified with a default-excluded content search, whose negative result is not evidence
of absence (measured on this archive: 37 files by default-excluded search against 119 by `os.walk`).

**Source.** Declaration §F.1, "Consequence, declared as a method rule" (scratch lines 3554–3560).

**Why here.** Archive-survey method; it governs how evidence is gathered, not how a verdict is
computed.

### P-133 — Every number is read from a named artifact, with its scope named

**The practice.** Every number written is read from a named artifact opened in the pass, or computed
from such an artifact by an arithmetic stated at the point of use; where two artifacts report the
same quantity the PRIMARY one is named; and where a quantity depends on a class set, a side, a
boundary, or a lattice generation, all of those are named where the number appears.

**Source.** Declaration §F.2, "Numbers in this file" (scratch lines 3562–3567).

**Why here.** Provenance discipline; the published-number provenance obligation is `PREREG.md`
§8.6's, the class-set naming is SC-10(c)'s, and this entry holds only the working form.

---

## 2. Verification against J1 by row id

| J1 row | J1 bucket | K1 disposition | Entry here | Match |
|---|---|---|---|---|
| 2 | NG | PRACTICES | P-02 | yes |
| 10 | NG | PRACTICES | P-10 | yes |
| 13 | NG | PRACTICES | P-13 | yes |
| 20 | NG | PRACTICES | P-20 | yes (flagged) |
| 47 | NG | PRACTICES | P-47 | yes (flagged) |
| 51 | NG | PRACTICES | P-51 | yes (flagged) |
| 61 | NG | PRACTICES | P-61 | yes |
| 65 | NG | PRACTICES | P-65 | yes |
| 68 | NG | PRACTICES | P-68 | yes |
| 70 | NG | PRACTICES | P-70 | yes |
| 77 | NG | PRACTICES | P-77 | yes |
| 83 | NG | PRACTICES | P-83 | yes |
| 87 | NG | PRACTICES | P-87 | yes (flagged) |
| 111 | NG | PRACTICES | P-111 | yes |
| 113 | NG | PRACTICES | P-113 | yes |
| 115 | NG | PRACTICES | P-115 | yes |
| 117 | NG | PRACTICES | P-117 | yes |
| 131 | NG | PRACTICES | P-131 | yes |
| 133 | NG | PRACTICES | P-133 | yes |

**Count: 19.** J1's 26 NON-GATE rows (2, 8, 9, 10, 13, 18, 20, 22, 23, 27, 47, 51, 61, 65, 68, 70,
77, 83, 87, 111, 113, 115, 117, 126, 131, 133) minus K1's seven INTEGRITY → PREREG rows (8, 9, 18,
22, 23, 27, 126) leaves exactly the nineteen above. No row was added, dropped, or moved between
buckets by this file.

## 3. Rows flagged, not moved

Four entries describe practices whose substance an applied `PREREG.md` clause limb now carries
verbatim or nearly so. Under the instruction to flag rather than reclassify, they stay here and are
marked; the K4 scrub, for each, cites the registered limb in the declaration and adds the pointer
here, so nothing is lost whichever way the author decides.

| Entry | Applied clause limb that carries the substance | Recommendation |
|---|---|---|
| P-20 | SC-4(a), last sentence: "Any report quoting such a count names the scope it counts under." | Treat the declaration's statement as a citation of SC-4(a); the entry here becomes redundant. |
| P-47 | SC-11(g): "excluded units remain excluded and are never reported as missed". | Treat as a citation of SC-11(g); the entry here becomes redundant. |
| P-51 | SC-4(f)3: "The partition check is printed and reproducible by any gate report … A gate report that cannot reproduce the check has not scored the fixture." | Treat as a citation of SC-4(f)3; only the rationale sentence is practice. |
| P-87 | SC-3(e), last sentence: "Where two views of the map are published, both are published with their delta explicit and neither replaces the other." | Treat as a citation of SC-3(e); the entry here becomes redundant. |

None of the four is a reclassification performed by this file. If the author accepts the
recommendation, the entry is struck here and the declaration's pointer to it is removed; the
declaration's citation of the clause already stands either way.

## 4. What this file does not contain

- No INSTANCE row (J1's 36): those stay in the declaration, labelled by the K4 scrub as the data the
  schema requires.
- No GATE-CRITICAL row (J1's 76): those are citations of `PREREG.md` SC-1 … SC-13c in the declaration
  after the scrub; row 28 is the one the schema cannot carry and is flagged in K4_SCRUB_DIFF.md.
- No INTEGRITY row (K1's 7): those are citations of SC-9 / SC-8(f).
- Nothing from the two frozen regions of the declaration (the T2 addendum block, lines 338–392; the
  decision-log tail, lines 3660–3695), which the scrub does not touch.
