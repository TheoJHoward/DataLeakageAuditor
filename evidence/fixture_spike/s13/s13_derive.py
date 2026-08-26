import csv, os
BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
TC = os.path.join(BASE, "y1", "trade_class_only_map.csv")
DM = os.path.join(BASE, "n1", "declared_map.csv")

rows = list(csv.DictReader(open(TC, newline="", encoding="utf-8")))
cont = [r for r in rows if r["side"] == "contaminated"]
corr = [r for r in rows if r["side"] == "corrected"]
print("rows total", len(rows), "contaminated", len(cont), "corrected", len(corr))

# ---- S1: contaminated side, restricted (trade classes only) vs full class ----
print("\n=== S1: CONTAMINATED per-instrument-month ===")
print(f"{'cell':14s} {'rows':>9s} {'restr_strict':>12s} {'restr_%':>8s} {'full_strict':>12s} {'full_%':>8s} {'delta_pp':>9s} {'ratio':>7s} {'r_eq':>5s} {'f_eq':>6s}")
recs = []
for r in cont:
    n = int(r["rows"]); rs = int(r["max_strict_trade_only"]); fs = int(r["max_strict_declared10"])
    re_ = int(r["max_equal_trade_only"]); fe = int(r["max_equal_declared10"])
    rp = 100.0 * rs / n; fp = 100.0 * fs / n
    recs.append(dict(cell=f"{r['instrument']} {r['month']}", n=n, rs=rs, fs=fs, rp=rp, fp=fp,
                     re_=re_, fe=fe, mbo=r["max_strict_mbo_only"], nclass=int(r["declared10_classes_scored"])))
    print(f"{r['instrument']+' '+r['month']:14s} {n:9d} {rs:12d} {rp:8.2f} {fs:12d} {fp:8.2f} {fp-rp:9.2f} {(fs/rs if rs else 0):7.2f} {re_:5d} {fe:6d}")

rp_all = [x["rp"] for x in recs]; fp_all = [x["fp"] for x in recs]
print("\nRESTRICTED strict-rate range over 48 contaminated cells: %.2f%% (%s) .. %.2f%% (%s)" % (
    min(rp_all), min(recs, key=lambda x: x["rp"])["cell"], max(rp_all), max(recs, key=lambda x: x["rp"])["cell"]))
print("FULL-CLASS strict-rate range over 48 contaminated cells: %.2f%% (%s) .. %.2f%% (%s)" % (
    min(fp_all), min(recs, key=lambda x: x["fp"])["cell"], max(fp_all), max(recs, key=lambda x: x["fp"])["cell"]))
# restricted / full among the 42 with MBO scored
mbo_scored = [x for x in recs if x["nclass"] == 10]
print("cells with 10 declared classes scored:", len(mbo_scored), " with 4 (nq):", len(recs) - len(mbo_scored))
mp = [100.0*int(x["mbo"])/x["n"] for x in mbo_scored]
print("MBO-only strict-rate range over the %d MBO-scored contaminated cells: %.2f%% .. %.2f%%" % (len(mbo_scored), min(mp), max(mp)))
print("equal-non-zero contaminated: restricted %d/48, full-class %d/48" % (
    sum(1 for x in recs if x["re_"] > 0), sum(1 for x in recs if x["fe"] > 0)))
print("strict-positive contaminated: restricted %d/48, full-class %d/48" % (
    sum(1 for x in recs if x["rs"] > 0), sum(1 for x in recs if x["fs"] > 0)))
# peaks
pk_rate = max(recs, key=lambda x: x["rp"]); pk_abs = max(recs, key=lambda x: x["rs"])
print("RESTRICTED contaminated RATE peak :", pk_rate["cell"], pk_rate["rs"], "/", pk_rate["n"], "= %.2f%%" % pk_rate["rp"])
print("RESTRICTED contaminated ABS  peak :", pk_abs["cell"], pk_abs["rs"], "/", pk_abs["n"], "= %.2f%%" % pk_abs["rp"])
fpk_rate = max(recs, key=lambda x: x["fp"]); fpk_abs = max(recs, key=lambda x: x["fs"])
print("FULL-CLASS contaminated RATE peak :", fpk_rate["cell"], fpk_rate["fs"], "/", fpk_rate["n"], "= %.2f%%" % fpk_rate["fp"])
print("FULL-CLASS contaminated ABS  peak :", fpk_abs["cell"], fpk_abs["fs"], "/", fpk_abs["n"], "= %.2f%%" % fpk_abs["fp"])
top5 = sorted(recs, key=lambda x: -x["rp"])[:5]
print("restricted top-5 by rate:", ", ".join("%s %.2f%%" % (x["cell"], x["rp"]) for x in top5))
bot5 = sorted(recs, key=lambda x: x["rp"])[:5]
print("restricted bottom-5 by rate:", ", ".join("%s %.2f%%" % (x["cell"], x["rp"]) for x in bot5))

zc = [x for x in recs if x["cell"] == "zc 2025-01"][0]
print("\n*** ZC 2025-01 CONTAMINATED ***")
print("  rows                      :", zc["n"])
print("  restricted strict (trades):", zc["rs"], "= %.4f%%" % zc["rp"])
print("  restricted equal          :", zc["re_"])
print("  full-class strict         :", zc["fs"], "= %.4f%%" % zc["fp"])
print("  mbo-only strict           :", zc["mbo"], "= %.4f%%" % (100.0*int(zc["mbo"])/zc["n"]))
print("  delta (pp)                : %.2f" % (zc["fp"] - zc["rp"]))
print("  ratio full/restricted     : %.4f" % (zc["fs"]/zc["rs"]))
print("  absolute drop             :", zc["fs"] - zc["rs"])

# ---- cross-check against declared_map.csv ----
print("\n=== CROSS-CHECK vs n1\\declared_map.csv (zc 2025-01, contaminated, decision_T) ===")
dm = list(csv.DictReader(open(DM, newline="", encoding="utf-8")))
TRADE = {"trades_all", "trades_buy", "trades_sell", "trades_large"}
sel = [d for d in dm if d["side"] == "contaminated" and d["instrument"] == "zc" and d["month"] == "2025-01"]
for d in sorted(sel, key=lambda d: (d["boundary"], d["class"])):
    n = int(d["rows"]) if d["rows"] else 0
    sc = int(d["strict_count"]) if d["strict_count"] else 0
    print("  %-12s %-12s strict=%8d equal=%4s rows=%7d  %6.2f%%  %s" % (
        d["boundary"], d["class"], sc, d["equal_count"], n, 100.0*sc/n if n else 0, d["scored_flag"]))
dT = [d for d in sel if d["boundary"] == "decision_T" and d["scored_flag"] == "SCORED"]
mt = max(int(d["strict_count"]) for d in dT if d["class"] in TRADE)
ma = max(int(d["strict_count"]) for d in dT)
mm = max(int(d["strict_count"]) for d in dT if d["class"] not in TRADE)
print("  DERIVED from declared_map: max trade-class strict =", mt, "| max all-class =", ma, "| max mbo-class =", mm)
print("  AGREES with trade_class_only_map:", mt == zc["rs"], ma == zc["fs"], mm == int(zc["mbo"]))

# full 48-cell agreement check between the two artifacts
print("\n=== FULL 48x2 AGREEMENT CHECK (trade_class_only_map vs declared_map) ===")
bad = 0
for r in rows:
    key = (r["side"], r["instrument"], r["month"])
    sub = [d for d in dm if (d["side"], d["instrument"], d["month"]) == key
           and d["boundary"] == "decision_T" and d["scored_flag"] == "SCORED"]
    if not sub:
        print("  NO ROWS", key); bad += 1; continue
    t = [int(d["strict_count"]) for d in sub if d["class"] in TRADE]
    a = [int(d["strict_count"]) for d in sub]
    te = [int(d["equal_count"]) for d in sub if d["class"] in TRADE]
    ok = (max(t) == int(r["max_strict_trade_only"]) and max(a) == int(r["max_strict_declared10"])
          and max(te) == int(r["max_equal_trade_only"]))
    if not ok:
        print("  MISMATCH", key, max(t), r["max_strict_trade_only"], max(a), r["max_strict_declared10"]); bad += 1
print("  mismatches:", bad, "of", len(rows), "rows")
