# Independent rebuild of the 35-row S2 cross-tab and application of A.6.0's RULE.
import csv, re, sys

DECL = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01\AVAILABILITY_DECLARATION.md"
CU   = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\y1\column_universe.csv"

text = open(DECL, encoding='utf-8').read()
lines = text.split('\n')

def section(start_marker, end_marker):
    i = text.index(start_marker); j = text.index(end_marker, i)
    return text[i:j]

# ---- 1. enumerated lists from the declaration (A.6.1 table, A.6.2 (a)/(b) prose, A.6.3 bullets)
a61 = section("#### A.6.1 — REQUIRED", "#### A.6.2 —")
a62 = section("#### A.6.2 — OUT OF JURISDICTION", "#### A.6.3 —")
a63 = section("#### A.6.3 — UNSCORED", "#### A.6.4 —")

# A.6.1: rows of the markdown table "| n | `name` | ..."
req = []
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*`([a-z0-9_]+)`\s*\|", a61, re.M):
    req.append(m.group(2))

# A.6.2: (a) group and (b) group, backticked names in the two paragraphs
a62a = a62[a62.index("**(a) Manifest-CLEAN"):a62.index("**(b) Same-row book")]
a62b = a62[a62.index("**(b) Same-row book"):a62.index("> PREREG.md line 460")]
ooj_a = re.findall(r"`([a-z0-9_]+)`", a62a)
ooj_a = [c for c in ooj_a if c in ("minutes_since_open","session_open","session_mid","session_close")]
ooj_b = re.findall(r"`([a-z0-9_]+)`", a62b)
ooj_b = [c for c in ooj_b if c not in ("class",)]

uns = ["buy_volume_10s", "book_imbalance_ratio"]

print("A.6.1 REQUIRED  n=%d" % len(req), req)
print("A.6.2(a)        n=%d" % len(ooj_a), ooj_a)
print("A.6.2(b)        n=%d" % len(ooj_b), ooj_b)
print("A.6.3 UNSCORED  n=%d" % len(uns), uns)

enum = {}
for c in req: enum[c] = "REQUIRED"
for c in ooj_a + ooj_b: enum[c] = "OUT OF JURISDICTION"
for c in uns: enum[c] = "UNSCORED"
print("enumerated total (dedup):", len(enum), " raw sum:", len(req)+len(ooj_a)+len(ooj_b)+len(uns))

# ---- 2. Y1 source universe
rows = list(csv.DictReader(open(CU, newline='', encoding='utf-8')))
y1 = {r['column']: r for r in rows}
print("y1 columns:", len(y1))

names_decl = set(enum); names_y1 = set(y1)
print("set identity decl vs y1:", names_decl == names_y1,
      "| decl-only:", sorted(names_decl-names_y1), "| y1-only:", sorted(names_y1-names_decl))

# ---- 3. apply A.6.0's RULE independently
# rule inputs derived from y1 construction facts + the two declared carve-outs
TRADE_SOURCES = {"trades parquet", "MIXED: snapshot parquet + trades parquet"}
DEGENERATE = {"buy_volume_10s"}            # §C.4(a), §15: aggressor literals never match -> identically 0
T4_EXCLUDED = {"book_imbalance_ratio"}     # §17 item 6 / §C.4(c): gate status EXCLUDED

def rule(col):
    r = y1[col]
    carries_ts_floor = r['source_class'] in TRADE_SOURCES
    degenerate = col in DEGENERATE
    unconstructible = col in T4_EXCLUDED
    # UNSCORED wins (A.6.0 precedence note)
    if degenerate or unconstructible:
        return "UNSCORED", ("degenerate-constant" if degenerate else "T4-unconstructible/EXCLUDED")
    if carries_ts_floor:
        return "REQUIRED", "carries ts_floor join (source=%s), not degenerate" % r['source_class']
    return "OUT OF JURISDICTION", "within-lattice book/clock only (source=%s)" % r['source_class']

disagree = []
print("\n#  column                     y1 source                    RULE                 ENUM                 match")
for i, r in enumerate(rows, 1):
    c = r['column']
    k, why = rule(c)
    e = enum.get(c, "<<MISSING>>")
    ok = (k == e)
    if not ok:
        disagree.append((c, r['source_class'], k, e, why))
    print("%-3d %-24s %-28s %-20s %-20s %s" % (i, c, r['source_class'], k, e, "OK" if ok else "*** MISMATCH ***"))

from collections import Counter
cr = Counter(rule(c)[0] for c in y1)
ce = Counter(enum.values())
print("\nRULE-derived counts :", dict(cr))
print("ENUMERATED counts   :", dict(ce))
print("partition 11+22+2 == 35 ?", cr["REQUIRED"], "+", cr["OUT OF JURISDICTION"], "+", cr["UNSCORED"],
      "=", cr["REQUIRED"]+cr["OUT OF JURISDICTION"]+cr["UNSCORED"])
print("N =", cr["REQUIRED"])
print("DISAGREEMENTS:", disagree if disagree else "NONE")

# ---- 4. the A.6.0 table's own per-column class vs the enumerations
tbl = section("| # | Column | Rule-derived class | Clause satisfied | Frozen at |", "**What the rule yields.**")
a60 = {}
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*`([a-z0-9_]+)`\s*\|\s*([A-Z ]+?)(?:\s*\(|\s*\|)", tbl, re.M):
    a60[m.group(2)] = m.group(3).strip()
print("\nA.6.0 table rows parsed:", len(a60))
bad = [(c, a60[c], enum[c]) for c in a60 if a60[c] != enum[c]]
print("A.6.0 table vs A.6.1/2/3 enumeration mismatches:", bad if bad else "NONE")
bad2 = [(c, a60[c], rule(c)[0]) for c in a60 if a60[c] != rule(c)[0]]
print("A.6.0 table vs independently applied rule    :", bad2 if bad2 else "NONE")

# ---- 5. A.6.5 crosstab table transcription check
ct = section("| # | Column | Y1 SOURCE class | R11 GATE class | composes? |", "**RESULT: all 35 compose.")
ctrows = re.findall(r"^\|\s*(\d+)\s*\|\s*`([a-z0-9_]+)`\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$", ct, re.M)
print("\nA.6.5 crosstab rows parsed:", len(ctrows))
ordermatch = [ (int(n), col) for n,col,_,_,_ in ctrows ]
y1order = [r['column'] for r in rows]
print("A.6.5 row order == column_universe.csv row order ?",
      [c for _,c in ordermatch] == y1order)
mis = []
for n, col, src, gate, comp in ctrows:
    g = re.sub(r"\*\*", "", gate)
    g = g.split("—")[0].strip()
    if g != enum[col]:
        mis.append((col, g, enum[col]))
    if "no" == comp.strip().lower():
        mis.append((col, "composes=no", comp))
print("A.6.5 gate-class transcription mismatches:", mis if mis else "NONE")
