import csv, json, os
from collections import Counter
B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
def rd(p): return list(csv.DictReader(open(os.path.join(B, p), newline='', encoding='utf-8-sig')))
def chk(label, got, want):
    print("%-4s %-56s got=%-24s decl=%s" % ("OK " if str(got)==str(want) else "*** MISMATCH ***", label, got, want))

print("== t4 unconstructible names (17) ==")
t4 = json.load(open(os.path.join(B, r"t4\fixture_manifest_35col_DRAFT.json"), encoding='utf-8'))
names = sorted(u['name'] for u in t4['unconstructible_columns'])
chk("t4 unconstructible set", names, sorted(['tick_direction','dollar_volume_1s','session_open','session_mid','session_close','book_imbalance_ratio','weighted_mid']))
ub = t4['counts_projected_subset'].get('unconstructible_by_class')
chk("unconstructible_by_class", ub, {'leak_source': 3, 'descendant': 1, 'clean': 3})
pv = t4['projection_verification']
chk("determinism contaminated sha", pv['determinism']['contaminated']['run1'], "32edf4389d9ca9435cc7923a19e0730bf409023d460b378f7acdc3cba11d719a")
chk("determinism corrected sha", pv['determinism']['corrected']['run1'], "db4193aa1ad88fa052599bf6714f2ba401bd99f52008a938a5f475280dc66245")
chk("self-consistency cols", pv['self_consistency']['run1']['n_projected_cols_checked'], 28)
chk("max_abs_diff", pv['self_consistency']['run1']['max_abs_diff'], 0.0)
chk("nan mismatches", pv['self_consistency']['run1']['nan_placement_mismatches_total'], 0)
chk("value mismatches", pv['self_consistency']['run1']['value_mismatches_total'], 0)
chk("all lagged / none exempt", (pv['self_consistency']['run1']['all_projected_cols_lagged'], pv['self_consistency']['run1']['exempt_projected_cols']), "(True, [])")

print("\n== n2 block_overlap: B.2/B.4 ==")
bo = rd(r"n2\block_overlap.csv")
print("     generations:", dict(Counter(r['generation'] for r in bo)), " total rows:", len(bo))
fixv3 = [r for r in bo if r['generation'] == 'v3_pre_gapfill_FIXTURE_PATH']
chk("v3 fixture-path rows", len(fixv3), 48)
mb = [r for r in fixv3 if int(r['native_blocks'])>1 and int(r['overlapping_block_pairs'])>0]
chk("MULTI-BLOCK of 48", len(mb), 18)
exc = [r for r in fixv3 if int(r['filtered_excess_rows'])>0]
chk("carrying filtered excess of 48", len(exc), 41)
chk("zero-excess of 48", len(fixv3)-len(exc), 7)
chk("zero-excess names", sorted(r['instrument']+" "+r['month'] for r in fixv3 if int(r['filtered_excess_rows'])==0),
    sorted(['he 2025-11','le 2025-11','zc 2025-01','zc 2025-11','zs 2025-01','zs 2025-11','zs 2025-12']))
chk("multi-block names", sorted(r['instrument']+" "+r['month'] for r in mb),
    sorted(['cl 2025-01','cl 2025-08','cl 2025-09','cl 2025-10','cl 2025-11','cl 2025-12',
            'gc 2025-01','gc 2025-08','gc 2025-09','gc 2025-10','gc 2025-11','gc 2025-12',
            'zc 2025-08','zc 2025-09','zc 2025-10','zs 2025-08','zs 2025-09','zs 2025-10']))
chk("18 is subset of 41", set(id(r) for r in mb) <= set(id(r) for r in exc), True)
chk("18 + 23 single-block-with-excess = 41", len(mb) + len([r for r in exc if int(r['native_blocks'])==1]), 41)
v4 = [r for r in bo if r['generation'] != 'v3_pre_gapfill_FIXTURE_PATH']
chk("v4-family measured rows", len(v4), 36)
chk("v4 all single-block", all(int(r['native_blocks'])==1 and int(r['overlapping_block_pairs'])==0 for r in v4), True)
chk("v4 zero-excess", sum(1 for r in v4 if int(r['filtered_excess_rows'])==0), 12)
chk("v4 with 1-5 excess", sum(1 for r in v4 if 1 <= int(r['filtered_excess_rows']) <= 5), 24)
chk("v4 max rows/sec == 2 on those 24", sorted(set(r['filtered_max_rows_per_second'] for r in v4 if int(r['filtered_excess_rows'])>0)), "['2']")
z1 = [r for r in fixv3 if r['instrument']=='zc' and r['month']=='2025-01'][0]
chk("zc 2025-01 v3 filtered_rows", z1['filtered_rows'], 338159)
chk("zc 2025-01 v3 blocks/overlap/excess", (z1['native_blocks'], z1['overlapping_block_pairs'], z1['filtered_excess_rows']), "('1', '0', '0')")
z8 = [r for r in fixv3 if r['instrument']=='zc' and r['month']=='2025-08'][0]
chk("zc 2025-08 v3 blocks/overlap", (z8['native_blocks'], z8['overlapping_block_pairs']), "('17', '16')")
chk("zc 2025-08 v3 excess", z8['filtered_excess_rows'], 211450)
chk("zc 2025-08 v3 distinct seconds", z8['filtered_distinct_seconds'], 342854)
chk("zc 2025-08 v3 max rows/second", z8['filtered_max_rows_per_second'], 5)
chk("max excess among single-block v3", max(int(r['filtered_excess_rows']) for r in fixv3 if int(r['native_blocks'])==1), 17)
z1v4 = [r for r in v4 if r['instrument']=='zc' and r['month']=='2025-01']
if z1v4:
    chk("zc 2025-01 v4 rows/distinct", (z1v4[0]['filtered_rows'], z1v4[0]['filtered_distinct_seconds']), "('378000', '378000')")
z8v4 = [r for r in v4 if r['instrument']=='zc' and r['month']=='2025-08']
if z8v4:
    chk("zc 2025-08 v4 rows/distinct/excess", (z8v4[0]['filtered_rows'], z8v4[0]['filtered_distinct_seconds'], z8v4[0]['filtered_excess_rows']), "('366005', '366000', '5')")

print("\n== B.5: the 18 MULTI-BLOCK == the 18 corrected-nonzero ==")
sc = rd(r"n1\summary_corrected.csv")
nz = set((r['instrument'], r['month']) for r in sc if float(r['max_strict'])>0)
mbset = set((r['instrument'], r['month']) for r in mb)
excset = set((r['instrument'], r['month']) for r in exc)
chk("MULTI-BLOCK set == corrected-nonzero set", mbset == nz, True)
chk("EXCESS(41) set == corrected-nonzero set (should be False)", excset == nz, False)
chk("23 single-block-with-excess are corrected-ZERO", all(im not in nz for im in (excset - mbset)), True)

print("\n== n1 lattice_profile ==")
lp = rd(r"n1\lattice_profile.csv")
d = {(r['instrument'], r['month']): r for r in lp}
chk("zc 2025-01 same_second_rows", d[('zc','2025-01')]['same_second_rows'], 0)
chk("zc 2025-08 same_second_rows", d[('zc','2025-08')]['same_second_rows'], 211450)
chk("zc 2025-01 rows", d[('zc','2025-01')]['rows'], 338159)
chk("zc 2025-08 rows -> corrected", (d[('zc','2025-08')]['rows'], d[('zc','2025-08')]['corrected_rows']), "('554304', '554303')")
chk("rows-corrected == 1 in all 48", sorted(set(int(r['rows'])-int(r['corrected_rows']) for r in lp)), [1])

print("\n== t3 day-edge (11) ==")
t3 = rd(r"t3\day_edge_table.csv")
chk("cross-boundary pairs total", sum(int(r['cross_boundary_label_pairs']) for r in t3), 2100)
chk("per-horizon pairs", [r['cross_boundary_label_pairs'] for r in t3], ['100','200','600','1200'])
chk("cross-boundary NaN", sum(int(r['cross_boundary_label_nan']) for r in t3), 0)
chk("mag-filter pass fracs", [r['cross_boundary_mag_filter_pass_frac'] for r in t3], ['0.83','0.83','0.823','0.812'])
chk("overall baseline fracs", [r['overall_mag_filter_pass_frac'] for r in t3], ['0.0','0.001','0.004','0.01'])
chk("worst span h=60", t3[3]['worst_wallclock_span_cross'], '3 days 19:31:00')
chk("worst sameday span h=60", t3[3]['worst_wallclock_span_sameday'], '0 days 00:30:45.369966846')
chk("sameday >60s pairs", [r['sameday_pairs_span_gt60s'] for r in t3], ['34','61','158','255'])
chk("total_rows", sorted(set(r['total_rows'] for r in t3)), "['338159']")

print("\n== 10/12: corrected-vs-(t-1) and C4 ==")
vt = rd(r"t1\violation_table.csv")
for cls, s, e in [('trades_all', 89568, 20), ('mbo_all', 254314, 29)]:
    rs = [r for r in vt if r['side']=='corrected' and r['boundary']=='claimed_T_prev' and r['event_class']==cls]
    chk("t1 corrected/claimed_T_prev %s" % cls, sorted(set((r['strictly_after_count'], r['equal_count']) for r in rs)), "[('%d', '%d')]" % (s, e))
wo = [r for r in vt if r['side']=='corrected' and r['boundary']=='claimed_T_prev']
chk("worst overhang past t-1 (max over classes)", max(float(r['worst_overhang_ms']) for r in wo), 999.999579)
chk("worst overhang trades classes", max(float(r['worst_overhang_ms']) for r in wo if r['event_class'].startswith('trades')), 999.996869)
c4 = rd(r"c4\independent_counts.csv")
for cls, s, e in [('trades_all', 89568, 20), ('mbo_all', 254314, 29)]:
    rs = [r for r in c4 if r['boundary']=='prev_row_B' and r['event_class']==cls]
    chk("c4 prev_row_B %s" % cls, (rs[0]['strict_count'], rs[0]['equal_count']), "('%d', '%d')" % (s, e))
chk("c4 total_rows uniform", sorted(set(r['total_rows'] for r in c4)), "['338158']")
chk("c4 boundaries present", sorted(set(r['boundary'] for r in c4)), "['decision_T', 'prev_row_B']")
zt = [r for r in c4 if r['boundary']=='decision_T']
chk("c4 decision_T all-zero strict/equal", sorted(set((r['strict_count'], r['equal_count']) for r in zt)), "[('0', '0')]")
chk("c4 decision_T gap-row subset zero", sorted(set((r['gap_row_subset_strict'], r['gap_row_subset_equal']) for r in zt)), "[('0', '0')]")
ct = [r for r in vt if r['side']=='corrected' and r['boundary']=='decision_T']
chk("t1 corrected/decision_T all zero (ZC 2025-01)", sorted(set((r['strictly_after_count'], r['equal_count']) for r in ct)), "[('0', '0')]")
chk("t1 corrected/decision_T class count", len(set(r['event_class'] for r in ct)), 10)

print("\n== 12: the 49 exactly-equal ZC 2025-01 events ==")
cd = [r for r in vt if r['side']=='contaminated' and r['boundary']=='decision_T']
eq = {}
for r in cd: eq[r['event_class']] = r['equal_count']
print("     per-class equal:", eq)
chk("trades_all equal", eq.get('trades_all'), 20)
chk("mbo_all equal", eq.get('mbo_all'), 29)
chk("20 + 29", int(eq.get('trades_all'))+int(eq.get('mbo_all')), 49)
for k, v in [('mbo_bid_add',1),('mbo_ask_add',4),('mbo_bid_cancel',23),('mbo_ask_cancel',22),('mbo_cancel_any',24),('trades_large',20)]:
    chk("equal %s" % k, eq.get(k), v)

print("\n== 12/10: contaminated-minus-1 on MBO classes ==")
for k in ['mbo_all','mbo_bid_add','mbo_ask_add','mbo_bid_cancel','mbo_ask_cancel','mbo_cancel_any']:
    a = [r for r in cd if r['event_class']==k][0]['strictly_after_count']
    b = [r for r in c4 if r['boundary']=='prev_row_B' and r['event_class']==k][0]['strict_count']
    print("     %-16s contaminated %s -> prev_row_B %s  (delta %d)" % (k, a, b, int(a)-int(b)))
for k in ['trades_all','trades_large']:
    a = [r for r in cd if r['event_class']==k][0]['strictly_after_count']
    b = [r for r in c4 if r['boundary']=='prev_row_B' and r['event_class']==k][0]['strict_count']
    print("     %-16s contaminated %s -> prev_row_B %s  (delta %d)" % (k, a, b, int(a)-int(b)))

print("\n== 13(a) class-set rule maxima (n1 m5 comparison) ==")
mm = rd(r"n1\m5_maxima_comparison.csv")
print("     fields:", list(mm[0].keys()))
for r in mm:
    if r.get('instrument')=='cl' and r.get('month')=='2025-01' and 'corrected' in str(r.values()):
        print("    ", dict(r))
