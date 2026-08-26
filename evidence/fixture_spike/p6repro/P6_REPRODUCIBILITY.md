# P6 — T3 REPRODUCIBILITY: the day-edge table's three magnitude-filter columns

**Date:** 2026-08-16. **Verdict: REPRODUCED — all fourteen columns, byte-for-byte.**
**Track:** P6 (gates the tag independently). **Writes:** `p6repro\` only; no archive edit,
no git command, no evidence-tree sync (the orchestrator handles evidence-tree writes).

---

## 1. The gap, as verified

**The archived producer builds ELEVEN keys; the archived table carries FOURTEEN columns.**

`evidence\fixture_spike\t3\measure_day_edge.py` lines 82–94, verbatim — the complete
`rows_out.append` dict, eleven keys:

```python
    rows_out.append({
        "horizon_s": h,
        "total_rows": N,
        "nan_labels_total": nan_total,
        "month_tail_last_h_rows_nan": tail_nan,
        "cross_boundary_label_pairs": n_cross,
        "cross_boundary_label_real_value": n_cross_real,
        "cross_boundary_label_nan": n_cross_nan,
        "worst_wallclock_span_cross": str(worst),
        "median_wallclock_span_cross": str(med),
        "sameday_pairs_span_gt60s": n_sameday_gt60,
        "worst_wallclock_span_sameday": str(worst_sd),
    })
```

`evidence\fixture_spike\t3\day_edge_table.csv` line 1, verbatim — fourteen columns:

```
horizon_s,total_rows,nan_labels_total,month_tail_last_h_rows_nan,cross_boundary_label_pairs,cross_boundary_label_real_value,cross_boundary_label_nan,worst_wallclock_span_cross,median_wallclock_span_cross,sameday_pairs_span_gt60s,worst_wallclock_span_sameday,cross_boundary_passing_mag_filter_abs_ge_2ticks,cross_boundary_mag_filter_pass_frac,overall_mag_filter_pass_frac
```

**The three columns the archived producer does not build** (columns 12–14 of the header):

1. `cross_boundary_passing_mag_filter_abs_ge_2ticks` — per-horizon count of
   cross-boundary label rows passing the ≥2-tick magnitude filter (83 / 166 / 494 / 974).
2. `cross_boundary_mag_filter_pass_frac` — per-horizon cross-boundary magnitude-filter
   pass fraction (0.83 / 0.83 / 0.823 / 0.812).
3. `overall_mag_filter_pass_frac` — overall baseline pass fraction over the whole lattice
   (0.0 / 0.001 / 0.004 / 0.01).

No other script in `evidence\fixture_spike\t3\` exists (directory holds exactly
`measure_day_edge.py`, `day_edge_table.csv`, `day_edge_samples.csv`), so the archive
contains NO producer for those three columns. They were corroborated only in
`evidence\errata\ERRATA_REGISTER.md` (Entry 5, "Measured magnitude" table, lines
562–575) and cited by `AVAILABILITY_DECLARATION.md`:

- lines 458–464 (caveat: "81-83% of cross-boundary labels pass the >=2-tick magnitude
  filter (0.83 / 0.83 / 0.823 / 0.812 by horizon) against an overall baseline of
  0.0-1.0% (0.000 / 0.001 / 0.004 / 0.010) ... Evidence: `t3\day_edge_table.csv` lines 2-5.")
- lines 1771–1774 (§A.11 "Magnitude-filter ENRICHMENT" restatement of the same figures).

**Filter definition source:** pre-fix `phase5_ml.py` line 679,
`valid = valid[valid[ret_col].abs() >= 2.0].copy()`, quoted at
`AVAILABILITY_DECLARATION.md` lines 466–469 — i.e. pass ⇔ |`fwd_move_ticks_{h}s`| ≥ 2.0.

## 2. The complete producer

`p6repro\measure_day_edge_full.py` — replicates the archived script's eleven-key logic
verbatim (marked ARCHIVED LOGIC in-file) and adds the three magnitude-filter columns.

**Input and its attestation.** The archived script's path convention is
`HERE.parent / "f2" / "out" / "contaminated_zc_2025-01_run1.pkl"` (t3 and f2 are
siblings). The archive's `f2\out\` carries only `.sha256`/`.meta.json` — no pickle
bytes — so the producer reads the same-named pickle from the scratchpad f2 build tree
(`scratchpad\fixture_spike\f2\out\`, sibling-relative exactly as in the archived
script) and ATTESTS it: it recomputes the f2 canonical-CSV sha256 (`run_fixture.py`
lines 28–31: `to_csv(index=False, float_format="%.12g")`, sha256 of utf-8 bytes) and
hard-fails unless it equals the archived sidecar. Result:

```
canonical_csv_sha256 recomputed: 73143359a90022f30af60cde7e637fd0b1585716f09d09437696fae411a10465 (163349778 bytes)
```

— identical to `evidence\fixture_spike\f2\out\contaminated_zc_2025-01_run1.sha256`
line 1 and to `.meta.json` `canonical_csv_sha256`/`canonical_csv_bytes` (lines 97–98).
(A raw pickle-byte hash is NOT the attestation convention: the sidecar records the
canonical CSV hash, not pickle bytes.) Environment matches the build meta exactly:
pandas 3.0.1, numpy 2.4.2 (meta.json lines 100–101), Python 3.12.10.

**The three new computations:**

- `cross_boundary_passing_mag_filter_abs_ge_2ticks` = count over the cross-boundary
  label values of |label| ≥ 2.0 (NaN compares False; all 2,100 cross labels are real
  anyway — `cross_boundary_label_nan` = 0 everywhere).
- `cross_boundary_mag_filter_pass_frac` = that count / `cross_boundary_label_pairs`,
  rounded to 3 decimals (the archived CSV stores 3-decimal values; 3-dp rounding is the
  serialization convention being reproduced — inferred, since no original producer for
  these columns is archived, and confirmed by the byte-identical reproduction below).
- `overall_mag_filter_pass_frac` = (count over ALL lattice rows of |label| ≥ 2.0) / N,
  rounded to 3 decimals.

**Denominator ambiguity, resolved empirically.** "Overall" admits three a-priori
denominators: all N = 338,159 rows; the N − nan_total real-labelled rows; the N − h
positional pairs. The producer computes all three
(`p6repro\overall_denominator_diagnostics.csv`); at 3 decimals they are IDENTICAL at
every horizon (worst raw spread is at h = 60: 0.010122 vs 0.010124 vs 0.010124, all →
0.010), so the archived values do not pin the original choice and the reproduction does
not depend on it. Emitted column uses all-N-rows. Overall pass counts, previously
recorded nowhere: 132 / 298 / 1,235 / 3,423 by horizon.

## 3. Per-column comparison — produced vs archived `day_edge_table.csv`

Producer output: `p6repro\day_edge_table_full.csv`. Comparison performed inside the
producer run (both sides re-read through identical CSV parsing, then additionally
compared as raw serialized lines).

| # | column | type | max abs deviation | verdict |
|---|---|---|---|---|
| 1 | `horizon_s` | count | 0 | MATCH |
| 2 | `total_rows` | count | 0 | MATCH |
| 3 | `nan_labels_total` | count | 0 | MATCH |
| 4 | `month_tail_last_h_rows_nan` | count | 0 | MATCH |
| 5 | `cross_boundary_label_pairs` | count | 0 | MATCH |
| 6 | `cross_boundary_label_real_value` | count | 0 | MATCH |
| 7 | `cross_boundary_label_nan` | count | 0 | MATCH |
| 8 | `worst_wallclock_span_cross` | string | exact | MATCH |
| 9 | `median_wallclock_span_cross` | string | exact | MATCH |
| 10 | `sameday_pairs_span_gt60s` | count | 0 | MATCH |
| 11 | `worst_wallclock_span_sameday` | string | exact | MATCH |
| 12 | `cross_boundary_passing_mag_filter_abs_ge_2ticks` | count | 0 | MATCH |
| 13 | `cross_boundary_mag_filter_pass_frac` | fraction (3-dp) | 0 | MATCH |
| 14 | `overall_mag_filter_pass_frac` | fraction (3-dp) | 0 | MATCH |

- Column set and order: identical (14 columns).
- **Raw CSV lines byte-for-byte identical: True** — every serialized token of all five
  lines (header + 4 horizon rows) matches the archived file exactly.
- Tolerance statement: counts and timedelta strings were required EXACT and are exact.
  For the two fraction columns a tolerance of 5e-4 (half-ulp at the archived file's
  3-decimal storage precision) was allowed in principle — the archived CSV stores only
  3 decimals, so full-precision raw fractions can only be compared at that precision —
  but the observed deviation is exactly 0, because the producer applies the same 3-dp
  rounding and the serialized tokens coincide byte-for-byte.

## 4. (d) The declaration's enrichment figures, re-verified from this producer

From `p6repro\day_edge_table_full.csv` (this run's output, not the archived CSV):

- cross-boundary pass fractions: **0.83 / 0.83 / 0.823 / 0.812** — equals the
  declaration's "0.83 / 0.83 / 0.823 / 0.812 by horizon"
  (`AVAILABILITY_DECLARATION.md` lines 461, 1772).
- overall baseline: **0.000 / 0.001 / 0.004 / 0.010** — equals the declaration's
  "0.000 / 0.001 / 0.004 / 0.010" (lines 462, 1773).
- underlying counts: 83/100, 166/200, 494/600, 974/1200 cross-boundary; the "81-83%
  vs 0-1%" enrichment sentence is arithmetically consistent with all four horizons
  (0.812–0.83 vs 0.00039–0.0101 raw).

## 5. Evidence-tree sync needed (NOT performed here)

The archive currently holds a producer that cannot regenerate 3 of the 14 columns the
declaration cites. `p6repro\measure_day_edge_full.py` closes that gap and is verified
byte-for-byte against the archived table. **The evidence tree needs this corrected
producer synced in** (e.g. alongside or replacing-with-supersession-note
`evidence\fixture_spike\t3\measure_day_edge.py`), together with
`p6repro\overall_denominator_diagnostics.csv` if the overall-denominator note is wanted
on the record. Per the P6 permission boundary, this report does NOT perform the sync —
the orchestrator handles evidence-tree writes. The archived `measure_day_edge.py` and
`day_edge_table.csv` were not touched.

## Files in `p6repro\`

- `measure_day_edge_full.py` — the complete fourteen-column producer (+ built-in
  attestation, comparison, and declaration re-verification; exit 0 = REPRODUCED).
- `day_edge_table_full.csv` — its output; byte-identical lines to the archived table.
- `overall_denominator_diagnostics.csv` — the three overall-denominator candidates,
  raw and 3-dp, per horizon.
- `P6_REPRODUCIBILITY.md` — this report.
