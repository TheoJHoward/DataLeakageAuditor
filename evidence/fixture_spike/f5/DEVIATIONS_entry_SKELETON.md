# DEVIATIONS.md skeleton entry — DRAFT, NOT APPLIED

<!-- STATUS: skeleton produced by Phase 0 addendum 2, item F5 (ceremony dry-run).
     DEVIATIONS.md in the repo is EMPTY as of HEAD 0ee26c4 and is append-only
     (PREREG.md section 11 item 6). This skeleton is the MEASUREMENT record only.
     Every [[V30A-TEXT: ...]] placeholder is where the author-reviewed amendment
     text lands. This skeleton itself introduces NO new branch, unit, denominator,
     coverage state, tier licence, or acceptance criterion. -->

---

## D-001 — Acceptance-fixture re-basis (class C amendment, `prereg-v30a`)

**Date recorded:** [[V30A-TEXT: date]]
**Class:** C per PREREG.md section 0.2.1 ("The measurement reveals a needed *new*
branch, unit, denominator, coverage state, tier licence, or acceptance criterion").
**Disposition:** amended registration, tag `prereg-v30a`, per section 0.2.1:
"Class C requires an amended registration, committed and externally timestamped
before the affected detector is implemented or evaluated — a `prereg-v30a` tag,
not a restart, and not a `DEVIATIONS.md` entry standing alone. The deviation
records what was measured; the amended tag carries the new semantics. Both."
**Amendment commit:** [[V30A-TEXT: commit hash]] — tag `prereg-v30a`.
**Amended sections:** [[V30A-TEXT: section list, expected to include section 6.2
(acceptance fixture reference AUC 0.957 / 0.675, interval ±0.010) and any
lock-table row whose key phrase the diff moves]]

### What was measured (facts only; no rule text here)

1. **Pair chronology.** The archive's Phase 5 feature builder
   `build_features_month()` (`C:\Users\ttbea\OneDrive\Desktop\MBO_2025\pc2_transfer\scripts\phase5\phase5_ml.py`
   lines 174–298) contains no `shift(1)`; the universal one-second feature lag
   exists only in
   `C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py`
   line 276 (`snap[feature_cols] = snap[feature_cols].shift(1)`, file mtime
   2026-04-12; line 819 writes `lag_fix: universal (all features shift(1))`).
   The post-fix `phase5_ml.py` variant described in `universal_lag_finding.txt`
   (lines 296–317, `_NO_LAG`/`_lag_cols` block) is MISSING from the archive.
   [[CONFIRM against spike items F1-F4 outputs AND delta-R2 items C1-C4/T4 (fixture_spike\R2_consolidated_report.md); C3 main-set label equality (all 64 phase7/phase7_fixed pairs bit-exact on true_label, fwd_move_ticks, mid_price_t) is the controlling evidence. C5 (wrap decidability) DECIDED 2026-08-10: the original runs WRAPPED — versions pinned pandas 3.0.1/numpy 2.4.2, the f2 rebuild is an execution witness (R2_consolidated_report.md C5 section; c5\env_records.md) — any net_delta erratum text in this entry cites that verdict.]]

2. **Both sides of the fixture pair are pre-fix.** The fixture pair pinned for
   the acceptance fixture (Phase 5 ZC CNN 5s per Phase 0 findings) derives from
   feature construction that predates the universal lag fix.
   Stored-prediction anchors: `results/phase7/l2_predictions/` (pre-fix, 64
   parquets) and `results/phase7_fixed/l2_predictions/` (post-fix, 64 parquets),
   ZC 5s = 1,047,430 rows on both sides; recorded meta
   `results/phase7/l2_model_meta.csv` lines 49–56 (ZC 5s 0.9662/0.9659
   LightGBM/XGBoost) and `results/phase7_fixed/l2_model_meta.csv` lines 18–25
   (ZC 5s 0.9315/0.9324).
   [[FILL: the spike's exact evidence chain for which builder produced each side of the registered pair — from spike items F1-F4, plus R2 item C3 (main phase7/phase7_fixed set: 64/64 pairs bit-exact shared labels; cite the MAIN set, not the pc2 timestamped variant) and C4 (blind independent re-measurement, full agreement with T1).]]

3. **Fixture re-basis.** PREREG.md section 6.2 locks "Reference AUC: 0.957 and
   0.675, acceptance interval ±0.010 absolute." The measured basis for those
   two numbers is [[FILL: spike AUC-recompute result — which stored artifact
   reproduces 0.957 and which reproduces 0.675, or the finding that one/both do
   not reproduce from the archived pair]].

### What this entry does NOT do

- It does not restate or alter any acceptance criterion, unit, denominator,
  state, or tier licence. Per section 0.2.1, "the amended tag carries the new
  semantics" — the semantics live in the `prereg-v30a` diff to PREREG.md, not
  here.
- It does not touch the `prereg-v30` tag ("This tag never moves" — tag message
  and README).
- Detector status at time of measurement: no detector implementation exists
  (README: "No detector implementation exists."), so the section 0.2.1 path
  "committed and externally timestamped before the affected detector is
  implemented or evaluated" applies — NOT the post-hoc re-draw path of
  section 0.2.1 / section 6.4 ("the affected benchmark is regenerated as a new
  version under §6.4"), which governs only a class C change discovered after
  the affected detector already exists.

### Integrity chain for this amendment (section 0.2.1)

"An amendment inherits §11's integrity chain in full: signed tag, both file
hashes in the tag message, external timestamp receipt committed, repository
publicly reachable at lock."

- Signed tag: `prereg-v30a` [[V30A-TEXT: tag date]]
- Tag message hash block: [[V30A-TEXT: five-line SHA-256 block as committed]]
- OTS receipt: [[V30A-TEXT: receipt filename]] committed in follow-up commit
  [[V30A-TEXT: hash]], upgraded at [[V30A-TEXT: block heights]]
