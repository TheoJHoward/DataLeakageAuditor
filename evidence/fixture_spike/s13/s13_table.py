import csv, os, statistics
B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
rows = [r for r in csv.DictReader(open(os.path.join(B, "y1", "trade_class_only_map.csv"), newline="", encoding="utf-8"))
        if r["side"] == "contaminated"]
out = []
for r in rows:
    n = int(r["rows"]); rs = int(r["max_strict_trade_only"]); fs = int(r["max_strict_declared10"])
    lbl = r["instrument"] + " " + r["month"]
    if r["instrument"] == "nq":
        lbl = "**nq** 2".replace("2", "") + r["month"] + " *(TRADES-CLASSES-ONLY)*"
        lbl = "**nq %s** *(TRADES-CLASSES-ONLY)*" % r["month"]
    out.append("| %s | %s | %s | %.2f | %s | %.2f | %.2f |" % (
        lbl, format(n, ","), format(rs, ","), 100.0*rs/n, format(fs, ","), 100.0*fs/n,
        100.0*fs/n - 100.0*rs/n))
print("\n".join(out))

rates = sorted(((100.0*int(r["max_strict_trade_only"])/int(r["rows"]), r["instrument"]+" "+r["month"]) for r in rows), reverse=True)
print("\nrestricted rate ranking (desc):")
for i, (v, c) in enumerate(rates, 1):
    print("  %2d %-12s %6.2f%%" % (i, c, v))
zc = [i for i, (v, c) in enumerate(rates, 1) if c == "zc 2025-01"][0]
print("\nzc 2025-01 restricted rank: %d of 48 (higher = larger rate)" % zc)
print("median restricted rate: %.2f%%" % statistics.median(v for v, _ in rates))
frates = sorted(((100.0*int(r["max_strict_declared10"])/int(r["rows"]), r["instrument"]+" "+r["month"]) for r in rows), reverse=True)
zcf = [i for i, (v, c) in enumerate(frates, 1) if c == "zc 2025-01"][0]
print("zc 2025-01 full-class rank: %d of 48" % zcf)
print("median full-class rate: %.2f%%" % statistics.median(v for v, _ in frates))
deltas = sorted((100.0*int(r["max_strict_declared10"])/int(r["rows"]) - 100.0*int(r["max_strict_trade_only"])/int(r["rows"]),
                 r["instrument"]+" "+r["month"]) for r in rows)
print("delta pp range: %.2f (%s) .. %.2f (%s)" % (deltas[0][0], deltas[0][1], deltas[-1][0], deltas[-1][1]))
nonnq = [d for d in deltas if not d[1].startswith("nq")]
print("delta pp range excluding nq: %.2f (%s) .. %.2f (%s)" % (nonnq[0][0], nonnq[0][1], nonnq[-1][0], nonnq[-1][1]))
print("zc 2025-01 delta: %.2f pp  (the LARGEST of all 48)" % [d for d in deltas if d[1] == "zc 2025-01"][0][0])
