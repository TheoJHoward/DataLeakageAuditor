# P5 RESULT — Owed item 5's measurement track (permission-gated)

**Date:** 2026-08-16. **Scope:** scratchpad record; NOT part of the package, NOT part of the
registration, NOT evidence-tree material. The probe script (`p5_probe.py`) is THROWAWAY per the
v10-spike precedent and carries that marking in its header.

---

## 1. THE PERMISSION READING (Step 1 — reported regardless of outcome)

### 1.1 The two governing texts, verbatim

`PREREG.md` §10.0 ("Phase 1 internal ordering, locked"), step 0, **line 1006**:

> 0. **If Phase 0 recorded the fixture as semantically ambiguous, the class C amendment of §10.2 is committed and timestamped before anything below — including any development-corpus access.**

`PREREG.md` §6.2, **line 448**:

> - **Reconstruction happens in Phase 0, before the cross-tool comparison** (§9.2).

### 1.2 The question

Do these texts permit a THROWAWAY FIXTURE MEASUREMENT using the perturbation mechanism —
corrupting a label cell and observing feature values — run as a Phase 0 measurement on the
fixture's own artifacts, while the class C amendment (v30a) is still pending?

### 1.3 The reading, stated plainly: PERMITTED

**(a) Line 1006's gate closes Phase 1, not Phase 0.** The words "anything below" scope over the
enumerated steps 1–6 of §10.0, a section titled "Phase 1 internal ordering, locked" (line 1004).
What the gate names as closed is Phase 1's step sequence plus one named extra: development-corpus
access. A measurement of a fixture property is not any of steps 1–6 and is not development-corpus
access.

**(b) The fixture artifacts are not the development corpus.** The development corpus is the tuning
corpus, a distinct registered object: `PREREG.md` line 92 defines class B parameters as values the
project may "select on the development corpus and freeze," and line 480 locks the ordering "tune on
the development corpus → freeze the candidate configuration → run the fixture gate" — two different
objects in sequence. The probe touches only the zc 2025-01 archive parquets (read-only) and the f2
builder — the Phase 0 fixture inputs that every Phase 0 measurement to date has consumed.

**(c) Line 448 places this class of work IN Phase 0, before anything else.** §6.2 line 447 requires
the declaration to be reconstructed "with **evidence for each element recorded before any detector
tuning**," and line 448 orders that reconstruction before the §9.2 cross-tool comparison. Whether a
feature reads an unavailable label value is an element-level fact of exactly that kind: the ordering
requirement cuts FOR running the measurement now (Phase 0, pre-tuning), not against it.

**(d) The §10.2 pause bars three named activities, none of which this is.** `PREREG.md` line 1033:
"record it, **pause runtime development**, commit and timestamp a class C amendment … and **only then
begin Phase 1 development or inspect the development corpus**." Fixture-property measurement is not
runtime development, not Phase 1 development, and not development-corpus inspection. Likewise §7.0's
invariant (line 745) enumerates what must wait for a phase tag — "development-corpus inspection,
hand-authored case writing, adjudication-rubric writing, wrapped-tool output inspection, default
tuning, detector implementation, and partition generation" — and a fixture perturbation measurement
is on no axis of that list.

**(e) Precedent, twice over.** The throwaway-measurement form: `PREREG.md` line 83 records §0.3's
three claims as "argued at length by multiple reviewers, two of them wrongly, settled in a morning of
measurement" — the v10-spike precedent. The Phase-0-measurement-on-fixture-artifacts form: T1
(ts_floor absorption, zc 2025-01), M5 (corrected-side sweep, stop-and-report), and N1 (48
instrument-month declared map) all ran AFTER the ambiguity finding and BEFORE the amendment, are
recorded as legitimate Phase 0 evidence, and the amendment drafting itself depends on their results.
The pause has never been read to bar them.

**(f) The distinction that carries the weight.** Running L2a AS A DETECTOR — its protocol, config,
tuning, evaluation — is Phase 1/2 work (`PREREG.md` lines 992–993) and is barred while the gate is
closed. Running a perturbation AS A MEASUREMENT of a fixture property uses no detector code, tunes
nothing, evaluates no detector, and asks a question about the fixture builder: does any feature
column read a label-forming value that is unavailable at the row's decision time? The corrected
clause draft (§4.3) names this exact object: "L2a's own probe, run as a measurement rather than as a
detector."

### 1.4 The counter-reading, stated fairly

Read line 1006's pause maximally: everything except amendment drafting is frozen, and a
perturb-rebuild-diff is mechanically what L2a does, so running it "as a measurement" is a relabeling
of barred detector development — and its result could shape the replacement criterion the way tuning
would ("a criterion chosen because it works after tuning is a criterion shaped by tuning,"
line 1035).

**Why that is the stretch and not the natural reading.** (i) It must add words to line 1033, which
pauses three named activities, not all activity; (ii) it must strike the project's own recorded
Phase 0 practice under this exact pause (T1/M5/N1 — same artifacts, same pending amendment, results
consumed by the amendment itself); (iii) the tuning-shaped-criterion concern does not attach: the
probe produces a fact about the fixture (which labelled units exist, if any) — instance data the
criterion's limb (b) consumes — not a detector performance number that could be used to pick a
flattering unit, threshold, or denominator; and (iv) the mechanism of a measurement does not change
its object — F2's determinism witness was mechanically "run twice and diff" (the determinism guard's
mechanism) and was still a fixture measurement, not detector work. The anti-rewrite caveat
(`PREREG.md` line 85: "a measurement will settle it" is not a licence to rewrite locked semantics)
is respected: nothing here rewrites semantics; the measurement lands as instance data or as
confirmation of a STOP.

**Conclusion: the permitting reading is the natural one. The measurement proceeded** — throwaway
script, p5probe scratchpad only, archive in read mode only, no detector code, no development-corpus
contact.

---

## 2. THE MEASUREMENT (Step 2)

### 2.1 Question

Does ANY fixture feature's value change when a label cell unavailable at its own decision cohort is
corrupted? This is L2a's registered probe semantics — `PREREG.md` line 318 (L2a: "Features from
unavailable label values … Availability-restricted label perturbation") and line 340 ("**Temporal.**
At cohort *d*, corrupt only label cells unavailable at *d*. Realized labels stay identical, so a
feature reading a realized `y.shift(1)` is clean and one reading an unrealized label is flagged.") —
run as a measurement of the fixture builder, not as a detector.

### 2.2 Method (as executed by `p5_probe.py`)

- **Object:** Artifact A, the only object with features — the f2 fixture builder
  (`fixture_spike\f2\fixture.py` + `phase5_ml_fixture.py`, unmodified), slice zc 2025-01 (the
  established slice; strictly ≥1 s spaced lattice per N1, so positional and temporal precedence
  coincide). Both sides built: `fixture_contaminated` (pre-fix builder) and `fixture_corrected`
  (builder + universal shift(1) wrapper). The retired declaration copy under `_retired` was not read.
- **Perturbation:** the label-forming future values. The label at row *r* is
  `fwd_move_ticks_{h}s[r] = (mid[r+h] − mid[r]) / tick` (builder lines 220–222), so the label cell's
  forming input beyond the decision row is future `mid_price`. `mid_price` was multiplied by 1.01 at
  every parquet row with `timestamp ≥ T_cut`, in a scratchpad COPY of the snapshot parquet (archive
  untouched). Every perturbed cell therefore sits strictly after every pre-cut decision time under
  BOTH tie branches (decision at T or at T−1s), so the perturbed label cells at pre-cut rows are
  unavailable at their own decision cohorts under either branch.
- **Two cuts, two cohort classes:**
  - **Cut A (intra-session):** T* = {t ≥ 2025-01-16 16:30:00 UTC} — plain strictly-future cohort.
  - **Cut B (session boundary):** T* = {t ≥ 2025-01-16 00:00:00 UTC} — the affected pre-cut label
    rows are the session tail of 2025-01-15, whose labels land in the next session: the
    cross-boundary label cohort class (T3 / declaration §11 / draft §4.4's cohort axis).
- **Staging:** every variant's snapshot went through the SAME read/modify/write parquet cycle
  (identity modification for the baseline), so variants differ ONLY in the multiplied cells. Trades
  parquet byte-copied; MBO aggregate generated once from the archive through the builder's own
  `load_mbo_aggregated` and served identically to all variants via the builder's own cache path.
- **Determinism re-witness:** the baseline was built twice and diffed over ALL columns before any
  perturbed comparison (F2's proof, re-witnessed in-run under pandas 3.0.1 / numpy 2.4.2 /
  pyarrow 23.0.1 — the pinned original-run environment).
- **Comparison:** all 44 registered fixture features (`FULL_FEATURES`) at all frame rows with
  `timestamp < T_cut`, NaN-aware, on both sides. Label columns excluded from the feature claim and
  used as positive control 1 (the perturbation MUST move label cells at pre-cut decision rows —
  exactly *h* rows per horizon *h* ∈ {5,10,30,60}). Positive control 2: post-cut features must move.
  Secondary sweep: every non-feature, non-label column pre-cut.

### 2.3 Numbers

Run 2026-08-16, 109.2 s total; environment python 3.12.10, pandas 3.0.1, numpy 2.4.2,
pyarrow 23.0.1 (the pinned original-run environment per C5). Full per-column output:
`p5_probe_results.json`; run log: `p5_probe_log.txt`.

| Quantity | Variant A (intra-session, cut 2025-01-16 16:30:00) | Variant B (session boundary, cut 2025-01-16 00:00:00) |
|---|---|---|
| Perturbed parquet mid_price cells | 637,707 of 1,262,191 | 690,071 of 1,262,191 |
| Frame rows (both sides, all variants) | 338,159 | 338,159 |
| pos_cut (first frame row ≥ cut) | 167,159 | 159,959 |
| Pre-cut comparison rows | 167,159 | 159,959 |
| **Feature diffs, pre-cut, CONTAMINATED (44 features)** | **0 — every column 0** | **0 — every column 0** |
| **Feature diffs, pre-cut, CORRECTED (44 features)** | **0 — every column 0** | **0 — every column 0** |
| Non-feature non-label column diffs, pre-cut | 0 — every column 0 | 0 — every column 0 |
| Corrected-side feature diffs AT row pos_cut | 0 | 0 |
| Positive control 1 — pre-cut label-cell diffs, per horizon h ∈ {5,10,30,60} | exactly 5 / 10 / 30 / 60, at positions pos_cut−h … pos_cut−1, identical both sides | exactly 5 / 10 / 30 / 60, at positions pos_cut−h … pos_cut−1, identical both sides |
| Positive control 2 — post-cut feature diffs (4-column sample) | 171,874 | 178,666 |
| Determinism re-witness (baseline built twice, ALL columns) | 0 differing cells | 0 differing cells |

Both positive controls behaved exactly as predicted: the perturbation demonstrably corrupted label
cells at rows whose decision times precede every perturbed timestamp (exactly *h* cells per horizon,
at exactly the last *h* pre-cut positions — for variant B these are the session-tail rows of
2025-01-15 whose labels land in the next session, i.e. the cross-boundary cohort class), and
demonstrably reached the feature pipeline (post-cut features moved en masse). Between those two
controls, not one of the 44 features moved at any of the 167,159 (A) / 159,959 (B) pre-cut rows, on
either side, and neither did any other column.

---

## 3. THE RESULT AND WHAT IT MEANS (Step 3)

### 3.1 The finding

**Clean null. No fixture feature's value changes when label cells unavailable at their own decision
cohorts are corrupted** — measured on Artifact A (zc 2025-01, 338,159 rows), on BOTH sides
(contaminated and corrected), for BOTH probed cohort classes (intra-session strictly-future, and the
cross-boundary session-tail cohort that T3 / declaration §11 measured), under the proven-deterministic
builder in the pinned environment, with both positive controls confirming the probe's reach.

**The labelled-unit set for L2a on this fixture slice is therefore EMPTY by measurement, on each
side separately.** There is no (feature × cohort) pair to enumerate; owed item 5's missing instance
data is answered in the negative.

### 3.2 Consequence for the clause

This is **run condition (i) established as fact rather than left open** — the corrected clause
draft's own enumeration (limb (b) commentary): "(i) the fixture contains no dependency of that
detector's kind, so there is nothing for the declaration to enumerate." The draft's §4.3 named
precisely this measurement as the closer: "a named feature whose value changes when a label cell
unavailable at its own decision cohort is corrupted — L2a's own probe, run as a measurement rather
than as a detector … If it does not exist, that is run condition (i) established as fact rather than
left open, and limb (b)'s STOP is then the correct and stated outcome — reached by measurement, not
by default."

**Limb (b)'s STOP is accordingly the correct outcome, reached by measurement.** And because the
emptiness was measured per side, the fixture-side instance fact for N6 defect 2 (the undefined 0/0
per-side yield under limb (d)) is also on record: the set is empty on the contaminated side and empty
on the corrected side — measured, not silent. Whatever per-side disposition SC-13b adopts, this
fixture's instance data is no longer the open part.

This also lands consistently with the declaration's own text: the three columns with label-BASE
character (`tick_direction`, `weighted_mid`, `vwap_distance` — declaration lines 1221–1223) sit at
`mid(t)` and were predicted NOT to move under L2a's probe, since a label-base read at *t* is not an
unavailable-label read (PREREG.md line 340 semantics). The measurement confirms the prediction:
`vwap_distance` (present in this builder's 44) moved at zero pre-cut rows in both variants.

### 3.3 Scope limits, stated so the record cannot overclaim

1. **One instrument-month measured.** The null is a measured fact for zc 2025-01 (both cuts, both
   sides). Extension to the other 47 instrument-months is a structural argument — the builder is one
   code path for all instrument-months, and its data-dependent branches (trades-missing,
   mbo-missing) write constants that cannot read future mid — not a measurement. If the amendment
   needs the null as measured fact on another slice, the probe re-runs there unchanged.
2. **The same-second / label-base channel is outside T\* by construction.** Features reading
   `mid(t)` — the label's base at the decision row — do not move under this probe and are not
   supposed to (line 340: corrupt only cells unavailable at *d*). Whether `mid(t)` itself is
   available at the decision instant is the ties-branch question, AMBIGUOUS-PENDING-AUTHOR, and is
   untouched by this result.
3. **The probe corrupts the label-forming inputs, not the label column cells.** The builder computes
   features independently of the `fwd_move_ticks_*` columns (no feature reads them — code fact,
   builder lines 192–296 vs 220–222), so the shared-input route (future `mid_price`) is the only
   live route, and it is the one measured.
4. **Artifact boundary.** This is an Artifact A measurement (the only object with features). Nothing
   here bridges to Artifact B beyond what the declaration's §0.3 reading rule already governs.

### 3.4 Files

All under `p5probe\` (this directory), outside the repo, outside the evidence tree:

- `p5_probe.py` — THROWAWAY probe script (header marks it: not part of the package, not part of the
  registration, to be deleted rather than committed).
- `p5_probe_results.json` — full per-column diff record, env pins, perturbation counts.
- `p5_probe_log.txt` — timestamped run log.
- `data_baseline\`, `data_pertA_intrasession\`, `data_pertB_sessionboundary\` — staged scratch data
  roots (~90 MB total; safe to delete with the script).
- `P5_RESULT.md` — this record.
