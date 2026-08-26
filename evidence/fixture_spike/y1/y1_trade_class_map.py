"""Y1 — re-derive the declared-map headline restricted to the FOUR TRADE CLASSES only.

Read-only over n1\declared_map.csv. Writes only into the y1 scratchpad.
"""
import csv
import os
from collections import defaultdict

MAP = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\n1\declared_map.csv"
OUT = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\y1"

TRADE_CLASSES = ["trades_all", "trades_buy", "trades_sell", "trades_large"]
MBO_CLASSES = ["mbo_all", "mbo_bid_add", "mbo_ask_add",
               "mbo_bid_cancel", "mbo_ask_cancel", "mbo_cancel_any"]
DECLARED_10 = TRADE_CLASSES + MBO_CLASSES

rows = list(csv.DictReader(open(MAP, newline="", encoding="utf-8-sig")))

# cell -> per class values
cells = defaultdict(dict)
for r in rows:
    key = (r["side"], r["instrument"], r["month"])
    cells[key][r["class"]] = r

def maxover(key, classes):
    """max strict / max equal over `classes`, counting only SCORED cells."""
    ms = me = 0
    n_scored = 0
    for c in classes:
        r = cells[key].get(c)
        if r is None:
            continue
        if not r["scored_flag"].startswith("SCORED"):
            continue
        n_scored += 1
        ms = max(ms, int(r["strict_count"] or 0))
        me = max(me, int(r["equal_count"] or 0))
    return ms, me, n_scored

sides = ["corrected", "contaminated"]
insts = sorted(set(r["instrument"] for r in rows))
months = sorted(set(r["month"] for r in rows))

out_rows = []
for side in sides:
    for inst in insts:
        for month in months:
            key = (side, inst, month)
            if key not in cells:
                continue
            ts, te, tn = maxover(key, TRADE_CLASSES)
            ms, me, mn = maxover(key, MBO_CLASSES)
            ds, de, dn = maxover(key, DECLARED_10)
            r0 = cells[key][TRADE_CLASSES[0]]
            out_rows.append({
                "side": side, "instrument": inst, "month": month,
                "rows": r0["rows"],
                "trade_classes_scored": tn,
                "max_strict_trade_only": ts,
                "max_equal_trade_only": te,
                "trade_only_status": ("STRICT_POSITIVE" if ts > 0
                                      else ("EQUAL_ONLY" if te > 0 else "ZERO_ZERO")),
                "mbo_classes_scored": mn,
                "max_strict_mbo_only": ms if mn else "",
                "max_equal_mbo_only": me if mn else "",
                "max_strict_declared10": ds,
                "max_equal_declared10": de,
                "declared10_status": ("STRICT_POSITIVE" if ds > 0
                                      else ("EQUAL_ONLY" if de > 0 else "ZERO_ZERO")),
                "declared10_classes_scored": dn,
            })

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "trade_class_only_map.csv")
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    w.writerows(out_rows)
print("wrote", path, len(out_rows), "rows")

# ── Headline arithmetic ──
for side in sides:
    sub = [r for r in out_rows if r["side"] == side]
    print("\n" + "=" * 72)
    print(f"SIDE = {side}   ({len(sub)} instrument-months)")
    print("=" * 72)
    for label, sk, ek in (("TRADE CLASSES ONLY (4)", "max_strict_trade_only", "max_equal_trade_only"),
                          ("DECLARED 10 (published)", "max_strict_declared10", "max_equal_declared10")):
        strict = [r for r in sub if r[sk] > 0]
        eq_any = [r for r in sub if r[ek] > 0]
        eq_only = [r for r in sub if r[ek] > 0 and r[sk] == 0]
        zz = [r for r in sub if r[sk] == 0 and r[ek] == 0]
        print(f"\n  {label}")
        print(f"    strict-positive : {len(strict)}/48")
        print(f"    equal non-zero  : {len(eq_any)}/48   (equal-only: {len(eq_only)})")
        print(f"    zero-zero       : {len(zz)}/48")
        print(f"    check {len(strict)}+{len(eq_only)}+{len(zz)} = {len(strict)+len(eq_only)+len(zz)}")
        if strict:
            print("    strict cells    : " + ", ".join(f"{r['instrument']} {r['month']}" for r in strict))
        if eq_only:
            print("    equal-only cells: " + ", ".join(f"{r['instrument']} {r['month']}" for r in eq_only))
        if zz:
            print("    zero-zero cells : " + ", ".join(f"{r['instrument']} {r['month']}" for r in zz))

# per-instrument-month table, trade-only
print("\n\nPER INSTRUMENT-MONTH, TRADE CLASSES ONLY (max strict / max equal)")
print(f"{'side':<13}{'inst':<5}{'month':<9}{'strict':>9}{'equal':>7}   {'d10_strict':>10}{'d10_equal':>10}")
for r in out_rows:
    print(f"{r['side']:<13}{r['instrument']:<5}{r['month']:<9}"
          f"{r['max_strict_trade_only']:>9}{r['max_equal_trade_only']:>7}   "
          f"{r['max_strict_declared10']:>10}{r['max_equal_declared10']:>10}")

# which class carries the trade-only max
print("\n\nWHICH TRADE CLASS CARRIES A NON-ZERO, per side")
for side in sides:
    cnt = defaultdict(int)
    for inst in insts:
        for month in months:
            key = (side, inst, month)
            if key not in cells:
                continue
            for c in TRADE_CLASSES:
                r = cells[key].get(c)
                if r and r["scored_flag"].startswith("SCORED"):
                    if int(r["strict_count"] or 0) > 0:
                        cnt[c + "|strict"] += 1
                    if int(r["equal_count"] or 0) > 0:
                        cnt[c + "|equal"] += 1
    print(f"  {side}: " + ", ".join(f"{k}={v}" for k, v in sorted(cnt.items())))
