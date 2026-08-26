"""Verify the two tables written into the declaration against their source artifacts.
Applies F.3's own rule to this pass: every check RAISES on mismatch rather than printing."""
import csv, os, re, sys
B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
DOC = os.path.join(B, "f4", "availability_declaration_DRAFT.md")
txt = open(DOC, encoding="utf-8").read()

def fail(m):
    print("*** RAISE:", m); sys.exit(1)

# ---------- A.6.5 : 35-row cross-tab ----------
src = {r["column"]: r["source_class"] for r in
       csv.DictReader(open(os.path.join(B, "y1", "column_universe.csv"), newline="", encoding="utf-8"))}
ordinal = {r["column"]: int(r["ordinal"]) for r in
           csv.DictReader(open(os.path.join(B, "y1", "column_universe.csv"), newline="", encoding="utf-8"))}
REQUIRED = {"net_delta_1s","net_delta_5s","net_delta_10s","net_delta_30s","net_delta_60s",
            "sell_volume_10s","large_trade_count_10s","vwap_distance",
            "trade_volume_1s","trade_count_1s","dollar_volume_1s"}
UNSCORED = {"buy_volume_10s", "book_imbalance_ratio"}
sec = txt.split("#### A.6.5")[1].split("---\n\n### A.7")[0]
rows = re.findall(r"^\| (\d+) \| `([a-z0-9_]+)` \| (.+?) \| (.+?) \| (.+?) \|$", sec, re.M)
if len(rows) != 35: fail("A.6.5 table has %d rows, expected 35" % len(rows))
seen = set()
for num, col, s, g, comp in rows:
    if col not in src: fail("A.6.5 row %s: unknown column %s" % (num, col))
    if int(num) != ordinal[col]: fail("A.6.5 %s: ordinal %s != artifact %d" % (col, num, ordinal[col]))
    exp_g = "REQUIRED" if col in REQUIRED else ("UNSCORED" if col in UNSCORED else "OUT OF JURISDICTION")
    if exp_g not in g: fail("A.6.5 %s: gate cell %r lacks %s" % (col, g, exp_g))
    if exp_g == "REQUIRED" and "UNSCORED" in g: fail("A.6.5 %s: gate cell claims two classes" % col)
    a = src[col]
    if a == "snapshot parquet" and "snapshot parquet" not in s: fail("A.6.5 %s source %r" % (col, s))
    if a == "trades parquet" and "trades parquet" not in s: fail("A.6.5 %s source %r" % (col, s))
    if a == "clock-only" and "clock-only" not in s: fail("A.6.5 %s source %r" % (col, s))
    if a == "derived-from-another-column" and not s.startswith("derived"): fail("A.6.5 %s source %r" % (col, s))
    if a.startswith("MIXED") and "MIXED" not in s: fail("A.6.5 %s source %r" % (col, s))
    if not comp.startswith("yes"): fail("A.6.5 %s NOT flagged 'yes': %r" % (col, comp))
    seen.add(col)
if seen != set(src): fail("A.6.5 covers %d of 35 columns" % len(seen))
print("A.6.5 35-row cross-tab: OK (35 rows, ordinals, source classes, gate classes, all 'yes')")

# ---------- 14.1 : 48-row contaminated table ----------
tc = {(r["instrument"], r["month"]): r for r in
      csv.DictReader(open(os.path.join(B, "y1", "trade_class_only_map.csv"), newline="", encoding="utf-8"))
      if r["side"] == "contaminated"}
sec = txt.split("### 14.1 ")[1].split("## 15. As-built")[0]
rows = re.findall(r"^\| \*?\*?([a-z]{2})\*?\*? ?(?:\*\*)?(20\d\d-\d\d)(?:\*\*)?.*?\| ([\d,]+) \| \*?\*?([\d,]+)\*?\*? \| \*?\*?([\d.]+)\*?\*? \| \*?\*?([\d,]+)\*?\*? \| \*?\*?([\d.]+)\*?\*? \| \*?\*?([\d.]+)\*?\*? \|$", sec, re.M)
if len(rows) != 48: fail("14.1 table parsed %d rows, expected 48" % len(rows))
i = lambda s: int(s.replace(",", ""))
for inst, mon, n, rs, rp, fs, fp, dp in rows:
    a = tc.get((inst, mon))
    if a is None: fail("14.1 unknown cell %s %s" % (inst, mon))
    if i(n) != int(a["rows"]): fail("14.1 %s %s rows %s != %s" % (inst, mon, n, a["rows"]))
    if i(rs) != int(a["max_strict_trade_only"]): fail("14.1 %s %s restricted %s != %s" % (inst, mon, rs, a["max_strict_trade_only"]))
    if i(fs) != int(a["max_strict_declared10"]): fail("14.1 %s %s full %s != %s" % (inst, mon, fs, a["max_strict_declared10"]))
    for got, calc, lbl in ((rp, 100.0*i(rs)/i(n), "restricted%"), (fp, 100.0*i(fs)/i(n), "full%"),
                           (dp, 100.0*i(fs)/i(n) - 100.0*i(rs)/i(n), "delta")):
        if abs(float(got) - calc) > 0.005: fail("14.1 %s %s %s %s != %.4f" % (inst, mon, lbl, got, calc))
    if inst == "nq" and "TRADES-CLASSES-ONLY" not in sec.split("| **nq %s**" % mon)[1].split("\n")[0]:
        fail("14.1 nq %s row missing TRADES-CLASSES-ONLY label" % mon)
if len(set((a, b) for a, b, *_ in rows)) != 48: fail("14.1 has duplicate cells")
print("14.1 48-row table: OK (48 cells, rows/restricted/full-class exact, all 3 percentages recomputed, nq labelled)")

# ---------- headline consistency ----------
for needle in ["26.49% — 89,568 / 338,159", "75.21% — 254,315 / 338,159",
               "48.72 percentage points", "164,747 rows", "999.996869 ms", "999.999579 ms",
               "N = 11 and is unchanged"]:
    if needle not in txt: fail("missing expected string: %r" % needle)
print("headline strings present: OK")
print("\nALL TABLE VERIFICATIONS PASSED")
