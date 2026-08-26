# DELTA R2 — consolidated report (pre-amendment closure, round 2)

Status: T4, C1, C2, C3, C4 complete; C5 PENDING (first attempt failed on session usage limit, resumed — this file will be updated when it lands).
Working resolutions R1–R5 recorded in the decision log at `f4\availability_declaration_DRAFT.md` (provisional until the prereg-v30a tag is signed).
Boundaries honored: archive read-only; all writes under `scratchpad\fixture_spike\`; no PREREG edits; no detector code; no development-corpus contact.

## Gate items (C3, C4) — both GREEN; v30a drafting unblocked

### C3 — label-vector equality: GREEN on the fixture pair set
- **Main set (results/phase7 vs phase7_fixed, the fixture pair source): all 64 pairs bit-exact identical** on `true_label`, `fwd_move_ticks`, AND `mid_price_t` (raw-bytes comparison after dtype/length checks). One shared label vector per pair — the feature-availability-only interpretation holds.
- pc2 timestamped variant set: NOT vector-equal — 30/32 pairs differ in row count by 1–7 rows; zs-60s equal-length but positionally shifted from index 1825. After timestamp alignment: **zero `true_label` disagreements at shared timestamps in all 32 pairs** (>99.99% matched). Breakout per spec: zc/zs unmatched rows 100% session-boundary; gc exactly 4 and nq exactly 3 interior rows per side per horizon — each a lattice row placed at a different second (same event, shifted 5 s / 1 s, identical subsecond ns) inside small mid-session gaps; plus 1 duplicate-timestamp multiplicity artifact in gc (×4 horizons) and zc-5s (float columns only, labels equal). Model-independence: 16/16 identical diff fingerprints across LightGBM/XGBoost.
- Consequence: the **main set** is the pair to cite; the pc2 variant is usable only via timestamp intersection.
- Evidence: `c3\label_equality.csv`, `c3\pc2_diff_summary.csv`, `c3\pc2_diff_rows.csv`, scripts in `c3\`.

### C4 — blind independent re-measurement: GREEN, full agreement with T1
- Blind agent (T1 implementation and outputs unread; no target numbers in prompt), checker in **polars 1.43.2** (no pandas), lattice **independently derived** from the snapshots parquet + builder filter definition: 338,159 rows, exact match.
- **Corrected side vs decision time: 0 strict + 0 equal for all 10 event classes over all 338,158 rows, including all 28 re-anchor gap rows.** Secondary boundary B=T_prev: trades_all 89,568/20; mbo_all 254,314/29; per-class MBO counts at contaminated−1 (last-row indicator), trades at −0 — exactly T1's published/implied values. Internal second-method cross-check (event-level join) agreed exactly.
- Orchestrator comparison vs T1: **no disagreement at any published count. No stop-and-report condition.**
- Evidence: `c4\independent_checker.py`, `c4\independent_counts.csv`.

## T4 — 35-column projection (run under R3)
> R3. 35-column: accepted as a documented-unverifiable assumption (basis: F3 manifest 9/9 agreement). T4 is unblocked by this.

- **28 of 35 constructible** (26 direct name matches + 2 verified intermediate mappings); 7 UNCONSTRUCTIBLE (projection is selection only — nothing synthesized).
- Determinism: run1 == run2 sha256 on both sides. Self-consistency: corrected[t] == contaminated[t−1] exact (max abs diff 0.0, 0 NaN mismatches) on all 28 columns, both run pairs.
- Manifest: `t4\fixture_manifest_35col_DRAFT.json` (json-validated, DRAFT, carries the R3 line and unconstructible entries with reasons).

## Context items (C1, C2) — the net_delta erratum inputs

### C1 — parquet provenance: **INHERITED**
Three independent chains, no conflicts:
1. **Run-time fingerprint:** the original ZC run log (`gpu_track2_log.txt`, mtime 2026-04-08, in-window) records 338,159 feature rows for 2025-01; that count derives solely from the snapshots parquet under the hour filter, and the current file reproduces exactly 338,159 today.
2. **Run-window checksums:** `pc2_transfer\transfer\checksums.txt` (mtime 2026-04-07, in-window) records MD5s for zc_snapshots_2025-01 and zc_trades_tagged_2025-01 that the current files match exactly; byte-identical SHA256 copies in four locations with pre/mid-window mtimes (originals mtime 2026-04-02, never touched); the post-run v4 rebuild went to a separate `v4_gapfill\` directory with different hashes.
3. **Single tagging implementation:** every aggressor-tagging writer that ever existed in the archive emits only BUY_AGGRESSOR/SELL_AGGRESSOR/UNKNOWN (+ boolean `is_buy_aggressor`); `process_zc.py` (mtime 2026-03-30) predates the parquets and runs. `isin(["B","Buy","buy"])` could never have matched any pipeline product.
**Therefore the buy-classifier defect was active in the original Phase 5 runs** (buy_volume ≡ 0; signed_vol = −size throughout). Residual ambiguity, reported not decisive: the physically read `C:\MBO_data` copies are gone and cannot themselves be hashed. Whether −size *wrapped* in the original environment is C5's question.

### C2 — phase7_l2_sim.py aggregation: **same defect, statically confirmed**
- Line 207: `is_buy = trades["aggressor_side"].isin(["B", "Buy", "buy"])` — matches none of the actual values → statically degenerate exactly like Phase 5.
- Line 209: `signed_vol = np.where(is_buy, size, -size)` — uncast uint32 negation, same wrap-prone dtype path.
- **7 of the 35 model features affected**: net_delta_1s/5s/10s/30s/60s (corrupted if wrapped), buy_volume_10s (dead-zero), sell_volume_10s (redundant with total volume).
- Differences from Phase 5 recorded: adds dollar_volume and per-second trade_1s features (drops trade_count_10s), universal shift(1) after construction, **reads no MBO data at all**, hardcodes the PC2 path.
- Blockers (carried): actual aggressor values verified for ZC 2025-01 only; original-env wrap → C5; PC2 runtime reads unconfirmable from archive.
- Evidence: `c2\aggregation_comparison.md`.

## C5 — wrap decidability: **DECIDABLE — the original runs wrapped**
- **Versions PINNED**: pandas 3.0.1 / numpy 2.4.2 / pyarrow 23.0.1 / Python 3.12.10 on PC1 ("VENGEANCE" — this machine), which produced ALL Phase 5 artifacts including the pinned ZC runs. Basis: two corroborating 2026-04-17 records (machine-generated pilot env JSON + git-committed frozen-env README) + launcher-named Python312 install whose dist-info metadata shows those versions installed 2026-02-12..18 and never changed — continuous coverage of the run window. The conflicting `requirements.txt` (pandas 2.1.4/numpy 1.26.4) is a prescription for a second computer, never installed on any interpreter here.
- **Dtype outcome DECIDED**: the original runs wrapped modulo 2^32 **identically to the f2 rebuild** — the parquet stores `size` as arrow uint32; pyarrow's documented conversion maps it to numpy uint32; the code is byte-verified; and the f2 rebuild is an execution witness under EXACTLY the pinned versions. Honest qualifier: no verbatim "unsigned negation wraps" sentence exists in the numpy docs — the airtight step is the version-identical execution witness (no new execution needed).
- Blockers recorded: no in-window (04-05..08) version record exists (bracketing records close the gap via dist-info); C:\MBO_data local-copy identity unrecorded (the md5 manifest covers the staging copy); PATH ambiguity is outcome-invariant (both interpreters carry pandas 3.x/numpy 2.4.2); pyarrow pin rests on README+dist-info.
- Evidence log: `c5\env_records.md`.

## Net effect on the v30a draft
- Drafting is cleared (C3/C4 green, per the sequencing rule).
- **The net_delta erratum call is now fully decided**: classifier defect inherited (C1), same code path in both generations (C2), and the wrap CONFIRMED in the original environment (C5) — the original Phase 5 (and, statically, Phase 7) runs computed net_delta from 2^32−size values, with buy_volume ≡ 0. Scope note: this covers the Phase 5/7 era; the v4-era paper pipeline (a4_runner.py) reimplements features and was NOT audited for the same defect — candidate follow-up, author's call.
- The fixture pair citation should name the **main** phase7/phase7_fixed prediction set (bit-exact shared labels); the pc2 variant set requires timestamp-intersection framing if used at all.
