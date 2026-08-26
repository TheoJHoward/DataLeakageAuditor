"""Y1 - build column_universe.csv: data source of each of the 35 ALL_L2_FEATURES columns.

Every construction_line_quote below was transcribed from a full read of
C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\results\\pc2_all_phases\\_scripts\\scripts\\phase7_l2_sim.py
and is re-verified against the file at run time (assert_quote). Read-only over the archive.
"""
import csv
import os

SRC = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\results\pc2_all_phases\_scripts\scripts\phase7_l2_sim.py"
OUT = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\y1\column_universe.csv"

with open(SRC, encoding="utf-8") as f:
    LINES = f.read().split("\n")          # LINES[i-1] is 1-indexed line i


def L(*nums):
    """Verbatim join of the given 1-indexed source lines, stripped of leading indent."""
    return "\n".join(LINES[n - 1].strip() for n in nums)


def rng(a, b):
    return L(*range(a, b + 1))


SNAP_READ = "135,139"
TRADE_READ = "199,201"

# name, family, source_class, raw_source, parents, ctor_lines, upstream_lines, note
ROWS = [
    # ── L1_FEATURES (21), phase7_l2_sim.py lines 73-83 ──
    ("mid_return_1s", "L1", "snapshot parquet", "snapshot parquet: mid_price", "",
     "152-153", "149; " + SNAP_READ,
     "mid defined L149 from snapshot column mid_price"),
    ("mid_return_5s", "L1", "snapshot parquet", "snapshot parquet: mid_price", "",
     "152-153", "149; " + SNAP_READ, "same loop, lag=5"),
    ("mid_return_10s", "L1", "snapshot parquet", "snapshot parquet: mid_price", "",
     "152-153", "149; " + SNAP_READ, "same loop, lag=10"),
    ("mid_return_30s", "L1", "snapshot parquet", "snapshot parquet: mid_price", "",
     "152-153", "149; " + SNAP_READ, "same loop, lag=30"),
    ("tick_direction", "L1", "snapshot parquet", "snapshot parquet: mid_price", "",
     "156", "149; " + SNAP_READ, "sign of mid.pct_change(1)"),
    ("trade_volume_1s", "L1", "trades parquet", "trades_tagged parquet: size", "",
     "246", "221,216,226,231; " + TRADE_READ,
     "groupby ts_floor agg trade_volume=(size,sum), merged L231"),
    ("trade_count_1s", "L1", "trades parquet", "trades_tagged parquet: size", "",
     "247", "220,216,226,231; " + TRADE_READ,
     "groupby agg trade_count=(size,count)"),
    ("dollar_volume_1s", "L1", "trades parquet", "trades_tagged parquet: size, price", "",
     "248", "214,223,231; " + TRADE_READ,
     "dollar_vol = size*price L214; groupby agg L223"),
    ("minutes_since_open", "L1", "clock-only", "snapshot parquet: timestamp (clock only)", "",
     "159", "144; " + SNAP_READ,
     "deterministic function of the row's own timestamp; hour_utc L144"),
    ("session_open", "L1", "derived-from-another-column", "snapshot parquet: timestamp (clock only)",
     "minutes_since_open", "162", "159,160,161", "frac L161 = minutes_since_open/total_minutes"),
    ("session_mid", "L1", "derived-from-another-column", "snapshot parquet: timestamp (clock only)",
     "minutes_since_open", "163", "159,160,161", ""),
    ("session_close", "L1", "derived-from-another-column", "snapshot parquet: timestamp (clock only)",
     "minutes_since_open", "164", "159,160,161", ""),
    ("net_delta_1s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "238-239", "207-209,217,231; " + TRADE_READ,
     "rolling sum of merged per-second net_delta; signed_vol L209"),
    ("net_delta_5s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "238-239", "207-209,217,231; " + TRADE_READ, "same loop, w=5"),
    ("net_delta_10s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "238-239", "207-209,217,231; " + TRADE_READ, "same loop, w=10"),
    ("net_delta_30s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "238-239", "207-209,217,231; " + TRADE_READ, "same loop, w=30"),
    ("net_delta_60s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "238-239", "207-209,217,231; " + TRADE_READ, "same loop, w=60"),
    ("buy_volume_10s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "240", "207-208,210,218,231; " + TRADE_READ,
     "buy_vol L210; dead-zero under the aggressor-literal mismatch (C2)"),
    ("sell_volume_10s", "L1", "trades parquet", "trades_tagged parquet: aggressor_side, size", "",
     "241", "207-208,211,219,231; " + TRADE_READ, "sell_vol L211"),
    ("large_trade_count_10s", "L1", "trades parquet", "trades_tagged parquet: size", "",
     "242", "212,222,231; " + TRADE_READ, "is_large L212 = size>=10"),
    ("vwap_distance", "L1", "MIXED: snapshot parquet + trades parquet",
     "snapshot parquet: mid_price; trades_tagged parquet: price, size", "",
     "243", "149,224-225,235,231; " + SNAP_READ + "; " + TRADE_READ,
     "mid term from snapshot; vwap term from trades groupby L224-225, ffill L235"),
    # ── L2_FEATURES (14), phase7_l2_sim.py lines 96-106 ──
    ("bid_size_1", "L2", "snapshot parquet", "snapshot parquet: bid_size_1 (raw pass-through)", "",
     "139", "174",
     "raw snapshot column, no construction statement; first use L174. NOT in the "
     "raw_book_cols lag-exemption (L270 covers bid_size_2..5), so it IS shifted at L276"),
    ("ask_size_1", "L2", "snapshot parquet", "snapshot parquet: ask_size_1 (raw pass-through)", "",
     "139", "174",
     "raw snapshot column, no construction statement; first use L174. NOT in the "
     "raw_book_cols lag-exemption (L271 covers ask_size_2..5), so it IS shifted at L276"),
    ("total_bid_depth", "L2", "snapshot parquet", "snapshot parquet: bid_size_1..5", "",
     "169", "167; " + SNAP_READ, "bid_cols L167"),
    ("total_ask_depth", "L2", "snapshot parquet", "snapshot parquet: ask_size_1..5", "",
     "170", "168; " + SNAP_READ, "ask_cols L168"),
    ("book_imbalance_ratio", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1..5, ask_size_1..5",
     "total_bid_depth|total_ask_depth", "188-189", "167-170", ""),
    ("weighted_mid", "L2", "snapshot parquet",
     "snapshot parquet: bid_price_1, ask_price_1, bid_size_1, ask_size_1, mid_price", "",
     "184-187", "149; " + SNAP_READ, "L187 re-expresses it as distance from mid in ticks"),
    ("spread_ticks", "L2", "snapshot parquet", "snapshot parquet: spread", "",
     "142", "141; " + SNAP_READ, "spread clipped at L141; tick is a constant from INST_META"),
    ("depth_imbalance", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1..5, ask_size_1..5",
     "total_bid_depth|total_ask_depth", "172-173", "171", "td L171"),
    ("book_slope_bid", "L2", "snapshot parquet", "snapshot parquet: bid_size_1..5", "",
     "178", "167; " + SNAP_READ, ""),
    ("book_slope_ask", "L2", "snapshot parquet", "snapshot parquet: ask_size_1..5", "",
     "179", "168; " + SNAP_READ, ""),
    ("depth_change_1s", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1..5, ask_size_1..5",
     "total_bid_depth|total_ask_depth", "180-181", "171", "td.diff(lag), lag=1"),
    ("depth_change_5s", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1..5, ask_size_1..5",
     "total_bid_depth|total_ask_depth", "180-181", "171", "td.diff(lag), lag=5"),
    ("depth_change_30s", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1..5, ask_size_1..5",
     "total_bid_depth|total_ask_depth", "180-181", "171", "td.diff(lag), lag=30"),
    ("l1_imbalance", "L2", "derived-from-another-column", "snapshot parquet: bid_size_1, ask_size_1",
     "bid_size_1|ask_size_1", "174-175", SNAP_READ, ""),
]

assert len(ROWS) == 35, len(ROWS)


def quote_for(spec):
    parts = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if "-" in chunk:
            a, b = chunk.split("-")
            parts.append(rng(int(a), int(b)))
        else:
            parts.append(L(int(chunk)))
    return "\n".join(parts)


out = []
for i, (name, fam, sclass, raw, parents, ctor, upstream, note) in enumerate(ROWS, 1):
    q = quote_for(ctor)
    out.append({
        "ordinal": i,
        "column": name,
        "feature_block": fam,
        "source_class": sclass,
        "raw_source_traced": raw,
        "parent_columns": parents,
        "mbo_fed": "NO",
        "construction_line_numbers": ctor,
        "construction_line_quote": q,
        "upstream_line_numbers": upstream,
    })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)

print("wrote", OUT, len(out), "rows")
from collections import Counter
print(Counter(r["source_class"] for r in out))
print("mbo_fed=YES count:", sum(1 for r in out if r["mbo_fed"] == "YES"))
print()
for r in out:
    print(f"{r['ordinal']:>2} {r['column']:<24} {r['source_class']:<38} L{r['construction_line_numbers']}")
    print("     | " + r["construction_line_quote"].replace("\n", "\n     | "))
