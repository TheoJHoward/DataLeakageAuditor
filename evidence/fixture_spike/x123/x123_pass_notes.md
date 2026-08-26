# X123 batched correction pass — working notes (2026-08-12)

Items implemented in one pass: X1, X2, X3, X6, plus R11 / R12 / R13 implementations.

## Baseline (pre-edit), matches `_snapshots\PRE_R9_HASHES.txt` exactly

    availability_declaration_DRAFT.md
      lines  1828   bytes 132242
      md5    f98b4d3d75d776aebcc54b6d33aaf511
      sha256 aab6400a003e69f204b37d36952ff3ef735cbb678b4e200fdbf33b80db2bcf8b
    frozen (i)  T2 addendum block  off 17389..23559  len 6170  md5 d4dd09b939540bdc2db33a2e13cb049e
    frozen (ii) decision-log tail  off 126498..EOF   len 5744  md5 059bbb1d33e4c93c254ac5f1dabf8dae

## End state (post-edit, re-read)

    availability_declaration_DRAFT.md
      lines  2306   bytes 167587
      md5    a6ed7fe1f7c732acf280c6a98656c74c
      sha256 4dcc654bfa42f8f12ac40069e4e183c159bd3f5f1d1d3931f7f3670ceb23e00e
    frozen (i)  T2 block  off 19292..25462  len 6170  md5 d4dd09b939540bdc2db33a2e13cb049e   MATCH
                                                      sha256 3a82ba45...24ae81               MATCH
    frozen (ii) tail      off 161843..EOF   len 5744  md5 059bbb1d33e4c93c254ac5f1dabf8dae   MATCH
                                                      sha256 ad8b3277...67e0                 MATCH
    `## Decision log` heading occurrences: 1

## R11 partition, verified programmatically against f3\fixture_manifest_DRAFT.json

REQUIRED (N = 11): net_delta_1s, net_delta_5s, net_delta_10s, net_delta_30s, net_delta_60s,
sell_volume_10s, large_trade_count_10s, vwap_distance, trade_volume_1s, trade_count_1s,
dollar_volume_1s

OUT OF JURISDICTION (22):
  (a) manifest-CLEAN, 4: minutes_since_open, session_open, session_mid, session_close
  (b) same-row book/lattice reads, 18: spread_ticks, bid_size_1, ask_size_1, l1_imbalance,
      total_bid_depth, total_ask_depth, depth_imbalance, book_slope_bid, book_slope_ask,
      depth_change_1s, depth_change_5s, depth_change_30s, mid_return_1s, mid_return_5s,
      mid_return_10s, mid_return_30s, tick_direction, weighted_mid

UNSCORED (2): buy_volume_10s, book_imbalance_ratio  (+ cell-level: the 72 unscored map cells)

11 + 22 + 2 = 35 = counts.total_fed_to_phase7. Set equality with the manifest's 35-entry
`columns` array confirmed; zero duplicates; zero omissions.

Judgment recorded: R11's UNSCORED limb "unconstructibles" is read as *columns whose gate status
is declared EXCLUDED* (book_imbalance_ratio alone). §17's 7 UNCONSTRUCTIBLE columns are
unconstructible in the F2 rebuild projection, not in the gate's fixture (R3 / §A.2), so reading
them as gate-unscored would drop dollar_volume_1s and tick_direction out of the arithmetic. The
reading is stated in the declaration at §A.6.3 so it is auditable.

## X3(c)/(d) numbers, verified against n2\block_overlap.csv before writing

v4 files (36): all native_blocks == 1, overlapping_block_pairs == 0.
  12 have filtered_excess_rows == 0 (rows == distinct seconds);
  24 have filtered_excess_rows in {1,4,5}, i.e. 1-5, all with filtered_max_rows_per_second == 2.
  So the exact 1 Hz totals are DISTINCT-SECOND counts, not row counts.
  e.g. zc 2025-01 v4: 378,000 rows / 378,000 seconds; zc 2025-08 v4: 366,005 rows / 366,000 s.

v3 fixture files (48): 18 multi-block (cl x6, gc x6, zc 08/09/10, zs 08/09/10);
  30 single-block, of which
    7 with filtered_excess_rows == 0: he 2025-11, le 2025-11, zc 2025-01, zc 2025-11,
      zs 2025-01, zs 2025-11, zs 2025-12
    23 with 1-17 (max 17 = he 2025-10), all filtered_max_rows_per_second == 2.

## R12 verification (read-only archive listing)

processed\nq\v4_gapfill\nq_mbo_2025-01 .. nq_mbo_2025-12 exist, each holding per-trading-day
`nq_mbo_YYYYMMDD.parquet` (2025-01 holds 63 entries). No processed\nq\nq_mbo_{month}.parquet at
the fixture path. So: NQ MBO data EXISTS at v4_gapfill; what is absent is same-generation
(v3_pre_gapfill) NQ MBO.

## X6 deviation, recorded

The staged HISTORY line (Variant A) carries no evidence-path citation, and the staging file's
own convention 7/8 says numbering is an ID and "No entry cites an evidence path. Provenance for
this entry stays in this staging file and in the ceremony record, not in the line." The
orchestrator's "FIX the citation: cite c1\tagger_survey_capture.txt" therefore has no target
inside the drafted line. The line was inserted WITHOUT a path. The corrected citation for the
ceremony record is:

    119-file figure  ->  fixture_spike\c1\tagger_survey_capture.txt line 17
                         ("files with >=1 mention: 119"; header "total *.py scanned: 460")
    There is no m1\ directory; the staging file's "the M1 finding" row is superseded by this.

The declaration's §F.1 already cites c1\tagger_survey_capture.txt line 17 correctly; no change
was needed there.
