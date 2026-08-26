import csv
p = r"C:\Users\ttbea\AppData\Local\Temp\claude\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\fixture_spike\t1\violation_table.csv"
rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
print("fields:", list(rows[0].keys()))
for i, r in enumerate(rows, 2):
    if r.get("side") == "contaminated" and r.get("boundary") == "decision_T":
        print(i, r)
print("---- corrected/claimed_T_prev ----")
for i, r in enumerate(rows, 2):
    if r.get("side") == "corrected" and r.get("boundary") == "claimed_T_prev":
        print(i, r)
