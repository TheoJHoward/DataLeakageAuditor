import csv, os
BASE = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
CU = os.path.join(BASE, "y1", "column_universe.csv")

# (i) Y1 SOURCE class, read from the artifact
src = {}
root = {}
for r in csv.DictReader(open(CU, newline="", encoding="utf-8")):
    src[r["column"]] = r["source_class"]
    root[r["column"]] = r["raw_source_traced"]
print("column_universe.csv rows:", len(src))

# (ii) R11 GATE class, transcribed BY NAME from the declaration's own lists
REQUIRED = ["net_delta_1s","net_delta_5s","net_delta_10s","net_delta_30s","net_delta_60s",
            "sell_volume_10s","large_trade_count_10s","vwap_distance",
            "trade_volume_1s","trade_count_1s","dollar_volume_1s"]                      # A.6.1
OOJ_A = ["minutes_since_open","session_open","session_mid","session_close"]              # A.6.2(a)
OOJ_B = ["spread_ticks","bid_size_1","ask_size_1","l1_imbalance","total_bid_depth",
         "total_ask_depth","depth_imbalance","book_slope_bid","book_slope_ask",
         "depth_change_1s","depth_change_5s","depth_change_30s","mid_return_1s",
         "mid_return_5s","mid_return_10s","mid_return_30s","tick_direction",
         "weighted_mid"]                                                                # A.6.2(b)
UNSCORED = ["buy_volume_10s","book_imbalance_ratio"]                                    # A.6.3
gate = {}
for c in REQUIRED: gate[c] = "REQUIRED"
for c in OOJ_A + OOJ_B: gate[c] = "OUT OF JURISDICTION"
for c in UNSCORED: gate[c] = "UNSCORED"
print("A.6.1 n=%d  A.6.2 n=%d (%d+%d)  A.6.3 n=%d  total=%d" %
      (len(REQUIRED), len(OOJ_A)+len(OOJ_B), len(OOJ_A), len(OOJ_B), len(UNSCORED), len(gate)))
assert len(set(REQUIRED)) == 11 and len(set(OOJ_A+OOJ_B)) == 22 and len(set(UNSCORED)) == 2
assert len(gate) == 35, "gate lists overlap"

# name-set identity
print("gate names == universe names:", set(gate) == set(src))
print("only in gate lists:", sorted(set(gate) - set(src)))
print("only in column universe:", sorted(set(src) - set(gate)))

TRADE_TOUCHING = {"trades parquet", "MIXED: snapshot parquet + trades parquet"}
def bucket(c):
    return "TRADE-TOUCHING" if src[c] in TRADE_TOUCHING else "SNAPSHOT-ROOTED or CLOCK"

# ---- the 35-row cross-tab, column by column ----
print("\n=== 35-ROW CROSS-TAB ===")
print("%-3s %-24s %-42s %-20s %-24s %s" % ("#","column","Y1 SOURCE class","R11 GATE class","source bucket","COMPOSES?"))
rows = list(csv.DictReader(open(CU, newline="", encoding="utf-8")))
noncomposing = []
for r in rows:
    c = r["column"]; b = bucket(c); g = gate[c]
    if b == "TRADE-TOUCHING":
        ok = g in ("REQUIRED", "UNSCORED")
        rule = "trade-touching -> REQUIRED, unless carved out UNSCORED"
    else:
        ok = g in ("OUT OF JURISDICTION", "UNSCORED")
        rule = "no trade join -> OUT OF JURISDICTION, unless carved out UNSCORED"
    if not ok: noncomposing.append((c, src[c], g))
    print("%-3s %-24s %-42s %-20s %-24s %s" % (r["ordinal"], c, src[c], g, b, "yes" if ok else "*** NO ***"))

print("\nnon-composing columns:", noncomposing if noncomposing else "NONE")

# ---- reconciliation AS ARITHMETIC ----
tt = sorted(c for c in src if bucket(c) == "TRADE-TOUCHING")
sr = sorted(c for c in src if bucket(c) != "TRADE-TOUCHING")
print("\n=== RECONCILIATION ===")
print("trade-touching (trades parquet %d + MIXED %d) = %d" % (
    sum(1 for c in src if src[c]=="trades parquet"),
    sum(1 for c in src if src[c].startswith("MIXED")), len(tt)))
print("  members:", tt)
print("  of which REQUIRED :", sorted(c for c in tt if gate[c]=="REQUIRED"), len([c for c in tt if gate[c]=="REQUIRED"]))
print("  of which UNSCORED :", sorted(c for c in tt if gate[c]=="UNSCORED"))
print("  of which OOJ      :", sorted(c for c in tt if gate[c]=="OUT OF JURISDICTION"))
print("  CHECK  12 == REQUIRED 11 + buy_volume_10s :", len(tt) == 11 + 1,
      "and the +1 is", [c for c in tt if gate[c]=="UNSCORED"])
print("snapshot-rooted + clock (snapshot %d + derived %d + clock %d) = %d" % (
    sum(1 for c in src if src[c]=="snapshot parquet"),
    sum(1 for c in src if src[c]=="derived-from-another-column"),
    sum(1 for c in src if src[c]=="clock-only"), len(sr)))
print("  of which OOJ      :", len([c for c in sr if gate[c]=="OUT OF JURISDICTION"]))
print("  of which UNSCORED :", sorted(c for c in sr if gate[c]=="UNSCORED"))
print("  of which REQUIRED :", sorted(c for c in sr if gate[c]=="REQUIRED"))
print("  CHECK  23 == OOJ 22 + book_imbalance_ratio :", len(sr) == 22 + 1,
      "and the +1 is", [c for c in sr if gate[c]=="UNSCORED"])
print("TOTAL", len(tt), "+", len(sr), "=", len(tt)+len(sr))

# ---- sub-reconciliation: clock-rooted vs book-rooted inside the 23 ----
clock_rooted = sorted(c for c in sr if "clock only" in root[c])
book_rooted = sorted(c for c in sr if "clock only" not in root[c])
print("\nInside the 23: clock-rooted %d = %s" % (len(clock_rooted), clock_rooted))
print("             : book-rooted  %d" % len(book_rooted))
print("  A.6.2(a) manifest-CLEAN 4 == clock-rooted 4 :", set(clock_rooted) == set(OOJ_A))
print("  A.6.2(b) 18 == book-rooted minus book_imbalance_ratio :",
      set(OOJ_B) == set(book_rooted) - {"book_imbalance_ratio"})
snap_in_b = sorted(c for c in OOJ_B if src[c]=="snapshot parquet")
der_in_b = sorted(c for c in OOJ_B if src[c]=="derived-from-another-column")
print("  A.6.2(b) splits %d snapshot-parquet + %d derived = %d" % (len(snap_in_b), len(der_in_b), len(OOJ_B)))
print("    derived members:", der_in_b)
print("    (compare C.3 Cat 1(b): 13 LEAK-SOURCE + 5 DESCENDANT = 18; DESCENDANT members are",
      "l1_imbalance, depth_imbalance, depth_change_{1,5,30}s)")

# source-class tallies vs the Y1 headline
from collections import Counter
print("\nsource-class tally:", dict(Counter(src.values())))
