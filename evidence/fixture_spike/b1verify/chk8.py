# Re-derivation of declaration numbers from artifacts.
import csv, json, os
from collections import Counter, defaultdict

B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
def rd(p):
    return list(csv.DictReader(open(os.path.join(B, p), newline='', encoding='utf-8-sig')))

def chk(label, got, want):
    ok = "OK " if str(got) == str(want) else "*** MISMATCH ***"
    print("%-4s %-58s got=%-22s decl=%s" % (ok, label, got, want))

print("== 1. n1/declared_map.csv structure (§13(a)) ==")
dm = rd(r"n1\declared_map.csv")
chk("rows in declared_map.csv", len(dm), 984)
sf = Counter(r['scored_flag'] for r in dm)
print("     scored_flag:", dict(sf))
chk("SCORED (declared-10)", sf.get('SCORED'), 888)
chk("UNSCORED_FOR_LACK_OF_DATA", sf.get('UNSCORED_FOR_LACK_OF_DATA'), 72)
chk("SCORED_DIAGNOSTIC_11TH_CLASS", sf.get('SCORED_DIAGNOSTIC_11TH_CLASS'), 24)
b = set(r['boundary'] for r in dm); print("     boundaries:", b)
cls = sorted(set(r['class'] for r in dm)); print("     classes(%d): %s" % (len(cls), cls))
ims = set((r['instrument'], r['month']) for r in dm); chk("instrument-months", len(ims), 48)

print("\n== 2. corrected side 18/48 and the peak (§13(b), §A.8) ==")
sc = rd(r"n1\summary_corrected.csv")
nz = [r for r in sc if float(r['max_strict']) > 0]
chk("corrected instrument-months with max_strict>0", len(nz), 18)
peak = max(nz, key=lambda r: float(r['max_strict_frac']))
chk("peak cell", peak['instrument'] + " " + peak['month'], "zc 2025-09")
chk("peak strict", peak['max_strict'], 111334)
chk("peak rows", peak['rows'], 580944)
chk("peak rate %.2f%%" % (100*float(peak['max_strict'])/float(peak['rows'])), "%.2f" % (100*float(peak['max_strict'])/float(peak['rows'])), "19.16")
chk("peak max_strict_frac", round(float(peak['max_strict_frac']),6), 0.191643)
chk("argmax class on all 18 == mbo_all", set(r['argmax_strict'] for r in nz), "{'mbo_all'}")
chk("classes_scored on all 18", sorted(set(r['classes_scored'] for r in nz)), "['10']")
nq = [r for r in sc if r['instrument']=='nq']
chk("nq classes_scored", sorted(set(r['classes_scored'] for r in nq)), "['4']")

print("\n== 3. contaminated saturation 48/48 and its range (§13(c)) ==")
sn = rd(r"n1\summary_contaminated.csv")
chk("contaminated cells", len(sn), 48)
chk("contaminated max_strict>0", sum(1 for r in sn if float(r['max_strict'])>0), 48)
lo = min(sn, key=lambda r: float(r['max_strict_frac'])); hi = max(sn, key=lambda r: float(r['max_strict_frac']))
chk("min frac cell", lo['instrument']+" "+lo['month']+" "+str(round(float(lo['max_strict_frac']),4)), "le 2025-11 0.2545")
chk("min strict/rows", lo['max_strict']+"/"+lo['rows'], "77483/304492")
chk("max frac cell", hi['instrument']+" "+hi['month']+" "+str(round(float(hi['max_strict_frac']),4)), "es 2025-12 0.9893")
chk("max strict/rows", hi['max_strict']+"/"+hi['rows'], "613447/620108")

print("\n== 4. N3 cohort predicate (§13(d), §C.2) ==")
pc = rd(r"n3\predicate_check.csv")
chk("predicate_check rows (scored cells)", len(pc), 456)
sv = sum(int(r['strict_viol']) for r in pc); ss = sum(int(r['same_second_viol']) for r in pc); ex = sum(int(r['exception_viol']) for r in pc)
chk("strict_viol total", sv, 5305430)
chk("same_second_viol total", ss, 5305430)
chk("exception_viol total", ex, 0)
cv = rd(r"n3\converse_by_instrument_month.csv")
cprof = rd(r"n3\cohort_profile.csv")
chk("converse rows", len(cv), 48)
coh = sum(int(r['cohort_size']) for r in cv); cr = sum(int(r['corrected_rows']) for r in cprof)
chk("cohort_profile nonmonotonic rows", sum(int(r['nonmonotonic_rows']) for r in cprof), 0)
chk("cohort_profile floor_decreasing rows", sum(int(r['floor_decreasing_rows']) for r in cprof), 0)
chk("lattice rows - corrected rows == 48 (one per im)", sum(int(r['rows'])-int(r['corrected_rows']) for r in cprof), 48)
chk("cohort rows total", coh, 1966088)
chk("corrected rows total", cr, 24768472)
chk("cohort share %.2f%%" % (100*coh/cr), "%.2f" % (100*coh/cr), "7.94")
lb = sum(int(r['LOWERBOUND_cohort_rows_violating_in_some_class']) for r in cv)
ub = sum(int(r['UPPERBOUND_cohort_rows_violating_in_no_class']) for r in cv)
chk("LOWERBOUND violating", lb, 1024196)
chk("UPPERBOUND non-violating", ub, 941892)
exf = open(os.path.join(B, r"n3\exceptions.csv"), encoding='utf-8').read().strip().split("\n")
chk("exceptions.csv data rows", len(exf)-1, 0)

print("\n== 5. unscored ledger (§13(g)) ==")
ul = rd(r"n1\unscored_ledger.csv")
chk("unscored_ledger rows", len(ul), 6)
tot = sum(int(r['n_cells']) for r in ul)
chk("total unscored cells (6 x 12)", tot, 72)
chk("n_cells each", sorted(set(r['n_cells'] for r in ul)), "['12']")

print("\n== 6. §14 ZC 2025-01 contaminated profile ==")
vt = rd(r"t1\violation_table.csv")
def t1cell(side, boundary, cls):
    out = [r for r in vt if r['side']==side and r['boundary']==boundary and r['event_class']==cls]
    return out
for cls, want_s, want_e in [('trades_all',89568,20), ('trades_large',23633,20), ('trades_buy',0,0), ('mbo_all',254315,29)]:
    rs = t1cell('contaminated','decision_T',cls)
    s = set(r['strictly_after_count'] for r in rs); e = set(r['equal_count'] for r in rs)
    chk("t1 contaminated/decision_T %s strict" % cls, sorted(s), "['%d']" % want_s)
    chk("t1 contaminated/decision_T %s equal" % cls, sorted(e), "['%d']" % want_e)
rows_zc = 338159
chk("trades_all rate %.4f%%" % (100*89568/rows_zc), "%.2f" % (100*89568/rows_zc), "26.49")
chk("mbo_all rate", "%.2f" % (100*254315/rows_zc), "75.21")
chk("trades_large rate", "%.2f" % (100*23633/rows_zc), "6.99")
chk("delta pp", "%.2f" % (100*254315/rows_zc - 100*89568/rows_zc), "48.72")
chk("row delta", 254315-89568, 164747)
chk("restricted as share of published", "%.1f%%" % (100*89568/254315), "35.2%")
chk("factor", "%.2f" % (254315/89568), "2.84")

print("\n== 7. §14 / §10 overhang + stamp-type (v1, m4) ==")
v1 = rd(r"v1\mean_overhang_by_class.csv")
d = {r['class']: r for r in v1}
chk("trades_all mean_overhang_ms", d['trades_all']['mean_overhang_ms'][:10], "519.797439"[:10])
chk("trades_large mean_overhang_ms", d['trades_large']['mean_overhang_ms'][:10], "506.273305"[:10])
chk("mbo_all mean_overhang_ms", d['mbo_all']['mean_overhang_ms'][:10], "655.194723"[:10])
m4 = rd(r"m4\stamp_type_breakdown.csv")
dm4 = {r['event_class']: r for r in m4 if r['side']=='contaminated' and r['boundary']=='decision_T'}
print("     m4 fields:", list(m4[0].keys()))
chk("trades_all viol_rate_integral", round(float(dm4['trades_all']['viol_rate_integral']),6), 0.278688)
chk("trades_all rate_ratio", round(float(dm4['trades_all']['rate_ratio_integral_over_mid']),3), 2337.499)
chk("trades_all share_on_integral", round(float(dm4['trades_all']['share_of_viol_on_integral']),6), 0.999978)
chk("mbo_all share_on_integral", round(float(dm4['mbo_all']['share_of_viol_on_integral']),6), 0.999807)

print("\n== 8. §14.1 restricted map, ex-nq peaks (y1) ==")
tc = rd(r"y1\trade_class_only_map.csv")
con = [r for r in tc if r['side']=='contaminated']
chk("contaminated rows in trade_class_only_map", len(con), 48)
def rate(r): return float(r['max_strict_trade_only'])/float(r['rows'])
pk = max(con, key=rate)
chk("unrestricted restricted-RATE peak", pk['instrument']+" "+pk['month']+" %.2f%%" % (100*rate(pk)), "nq 2025-01 90.83%")
exnq = [r for r in con if r['instrument']!='nq']
pk2 = max(exnq, key=rate)
chk("EX-NQ restricted RATE peak", pk2['instrument']+" "+pk2['month']+" %s/%s %.2f%%" % (pk2['max_strict_trade_only'], pk2['rows'], 100*rate(pk2)), "es 2025-11 484420/549424 88.17%")
pk3 = max(exnq, key=lambda r: int(r['max_strict_trade_only']))
chk("EX-NQ restricted ABSOLUTE peak", pk3['instrument']+" "+pk3['month']+" "+pk3['max_strict_trade_only']+" of "+pk3['rows'], "es 2025-01 514323 of 605290")
chk("EX-NQ absolute peak rate", "%.2f" % (100*rate(pk3)), "84.97")
pkabs_all = max(con, key=lambda r: int(r['max_strict_trade_only']))
chk("restricted ABSOLUTE peak incl nq", pkabs_all['instrument']+" "+pkabs_all['month']+" "+pkabs_all['max_strict_trade_only'], "nq 2025-01 543341")
fullpk = max(con, key=lambda r: float(r['max_strict_declared10'])/float(r['rows']))
chk("full-class RATE peak", fullpk['instrument']+" "+fullpk['month']+" %.2f%%" % (100*float(fullpk['max_strict_declared10'])/float(fullpk['rows'])), "es 2025-12 98.93%")
fullabs = max(con, key=lambda r: int(r['max_strict_declared10']))
chk("full-class ABSOLUTE peak", fullabs['instrument']+" "+fullabs['month']+" "+fullabs['max_strict_declared10']+" of "+fullabs['rows'], "gc 2025-10 646575 of 772448")
import statistics
rr = sorted(100*rate(r) for r in con)
chk("restricted rate span low", "%.2f" % rr[0], "8.76")
chk("restricted rate span high", "%.2f" % rr[-1], "90.83")
chk("restricted median", "%.2f" % statistics.median(rr), "21.66")
fr = sorted(100*float(r['max_strict_declared10'])/float(r['rows']) for r in con)
chk("full-class median", "%.2f" % statistics.median(fr), "63.08")
zc01 = [r for r in con if r['instrument']=='zc' and r['month']=='2025-01'][0]
dlt = 100*float(zc01['max_strict_declared10'])/float(zc01['rows']) - 100*rate(zc01)
chk("zc 2025-01 delta pp (largest of 48)", "%.2f" % dlt, "48.72")
deltas = [(100*float(r['max_strict_declared10'])/float(r['rows']) - 100*rate(r), r['instrument'], r['month']) for r in con]
chk("largest delta cell", max(deltas)[1]+" "+max(deltas)[2], "zc 2025-01")
exnq_d = [d for d in deltas if d[1]!='nq']
chk("min non-nq delta", "%.2f %s %s" % (min(exnq_d)[0], min(exnq_d)[1], min(exnq_d)[2]), "10.57 es 2025-11")
# equal-non-zero counts
chk("contaminated equal-nonzero restricted", sum(1 for r in con if int(r['max_equal_trade_only'])>0), 23)
chk("contaminated equal-nonzero full-class", sum(1 for r in con if int(r['max_equal_declared10'])>0), 42)
cor = [r for r in tc if r['side']=='corrected']
chk("corrected strict>0 restricted", sum(1 for r in cor if int(r['max_strict_trade_only'])>0), 18)
chk("corrected strict>0 full-class", sum(1 for r in cor if int(r['max_strict_declared10'])>0), 18)
chk("corrected equal-nonzero restricted", sum(1 for r in cor if int(r['max_equal_trade_only'])>0), 11)
chk("corrected equal-nonzero full-class", sum(1 for r in cor if int(r['max_equal_declared10'])>0), 35)
cpk = max(cor, key=lambda r: float(r['max_strict_trade_only'])/float(r['rows']))
chk("corrected restricted RATE peak", cpk['instrument']+" "+cpk['month']+" "+cpk['max_strict_trade_only']+"/"+cpk['rows']+" %.2f%%" % (100*float(cpk['max_strict_trade_only'])/float(cpk['rows'])), "zc 2025-10 34492/634445 5.44%")
cpa = max(cor, key=lambda r: int(r['max_strict_trade_only']))
chk("corrected restricted ABS peak", cpa['instrument']+" "+cpa['month']+" "+cpa['max_strict_trade_only'], "gc 2025-10 37913")

print("\n== 9. §A.1 / §8 reference AUC trio (f1) ==")
f1 = rd(r"f1\f1_results.csv")
for side, want in [('pre', {'5s':'0.966244','10s':'0.939968','30s':'0.856419'}), ('post', {'5s':'0.931536','10s':'0.756504','30s':'0.679288'})]:
    for hz, w in want.items():
        rows_ = [r for r in f1 if r.get('side')==side and r.get('instrument')=='ZC' and r.get('model')=='LightGBM' and r.get('horizon')==hz]
        if not rows_:
            rows_ = [r for r in f1 if side in str(r.values()) ]
        got = ("%.6f" % float(rows_[0]["recomputed_auc"])) if rows_ else "NOT FOUND"
        chk("AUC %s ZC LightGBM %s" % (side, hz), got, w)
chk("f1 rows", len(f1), 128)

print("\n== 10. §A.2 / §A.6.4 f3 manifest counts ==")
f3 = json.load(open(os.path.join(B, r"f3\fixture_manifest_DRAFT.json"), encoding='utf-8'))
c = f3['counts']
for k, want in [('independently_leaking_sources',25),('leak_source',25),('descendant',6),('clean',4),('total_fed_to_phase7',35),('not_fed_to_phase7',19)]:
    chk("f3 counts.%s" % k, c.get(k), want)
chk("f3 columns array length", len(f3['columns']), 35)
chk("f3 not_fed array length", len(f3['not_fed_to_phase7_models']), 19)
fl = Counter(x.get('flavor') for x in f3['columns'] if x.get('class')=='LEAK-SOURCE')
print("     flavor split on LEAK-SOURCE:", dict(fl))
cl = Counter(x.get('class') for x in f3['columns'])
print("     class split over 35:", dict(cl))

print("\n== 11. §17 / t4 manifest ==")
t4 = json.load(open(os.path.join(B, r"t4\fixture_manifest_35col_DRAFT.json"), encoding='utf-8'))
cp = t4['counts_projected_subset']
for k, want in [('projected_total',28),('unconstructible_total',7),('leak_source',22),('descendant',5),('clean',1)]:
    chk("t4 counts_projected_subset.%s" % k, cp.get(k), want)
un = t4.get('unconstructible_columns')
names = [u['column'] if isinstance(u, dict) else u for u in (un if isinstance(un, list) else un.keys())]
chk("t4 unconstructible columns", sorted(names), sorted(['tick_direction','dollar_volume_1s','session_open','session_mid','session_close','book_imbalance_ratio','weighted_mid']))

print("\n== 12. §B.4 / n2 block_overlap ==")
bo = rd(r"n2\block_overlap.csv")
print("     block_overlap rows:", len(bo), "fields:", list(bo[0].keys()))
fx = [r for r in bo if r.get('generation','')=='v3_pre_gapfill' or 'v3' in str(r.get('generation',''))]
print("     generations:", Counter(r.get('generation') for r in bo))

print("\n== 13. §10 corrected-vs-(t-1) (t1, c4) ==")
for cls, s, e in [('trades_all', 89568, 20), ('mbo_all', 254314, 29)]:
    rs = [r for r in vt if r['side']=='corrected' and r['boundary']=='claimed_T_prev' and r['event_class']==cls]
    chk("t1 corrected/claimed_T_prev %s" % cls, (rs[0]['strictly_after_count'], rs[0]['equal_count']) if rs else "NOT FOUND", (str(s), str(e)))
c4 = rd(r"c4\independent_counts.csv")
for cls, s, e in [('trades_all', 89568, 20), ('mbo_all', 254314, 29)]:
    rs = [r for r in c4 if r['boundary']=='prev_row_B' and r['event_class']==cls]
    chk("c4 prev_row_B %s" % cls, (rs[0]['strict_count'], rs[0]['equal_count']) if rs else "NOT FOUND", (str(s), str(e)))
chk("c4 total_rows on every row", sorted(set(r['total_rows'] for r in c4)), "['338158']")
chk("c4 has contaminated rows?", sorted(set(r.get('side','<none>') for r in c4)), "(expect no 'contaminated')")
zeroT = [r for r in c4 if r['boundary']=='decision_T']
chk("c4 decision_T all zero strict", sorted(set(r['strict_count'] for r in zeroT)), "['0']")

print("\n== 14. §11 / t3 day-edge ==")
t3 = rd(r"t3\day_edge_table.csv")
print("     t3 fields:", list(t3[0].keys()))
for r in t3:
    print("    ", dict(r))
tot = sum(int(r['cross_boundary_label_pairs']) for r in t3)
chk("total cross-boundary label pairs", tot, 2100)
chk("cross-boundary NaN", sum(int(r['cross_boundary_label_nan']) for r in t3), 0)
chk("mag-filter pass fracs", [r['cross_boundary_mag_filter_pass_frac'] for r in t3], ['0.83','0.83','0.823','0.812'])
chk("overall baseline fracs", [r['overall_mag_filter_pass_frac'] for r in t3], ['0.0','0.001','0.004','0.01'])
chk("worst span h=60", t3[3]['worst_wallclock_span_cross'], '3 days 19:31:00')
chk("sameday >60s pairs", [r['sameday_pairs_span_gt60s'] for r in t3], ['34','61','158','255'])

