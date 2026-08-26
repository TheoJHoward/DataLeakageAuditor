import csv, os
B = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike"
for sub, fn in (("v1", "mean_overhang_by_class.csv"), ("m4", "stamp_type_breakdown.csv")):
    p = os.path.join(B, sub, fn)
    print("=" * 70); print(p, os.path.exists(p))
    if not os.path.exists(p):
        print(" DIR:", os.listdir(os.path.join(B, sub))); continue
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    print("fields:", list(rows[0].keys()))
    for i, r in enumerate(rows, 2):
        print(" ", i, r)
