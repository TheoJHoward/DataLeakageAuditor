#!/usr/bin/env python3
"""E3 composer, v2 (R39/F7): builds the composed sections straight from the SAME
operative_text the signable artifact renders, so the composed document and the diff
cannot diverge. PREREG.md is opened read-only."""
import json, re, pathlib
D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
hunks = json.loads((D/"_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]
pre = (REPO/"PREREG.md").read_text(encoding="utf-8").split("\n")

def ln(h):
    m = re.search(r"\d+", h.get("prereg_line") or "")
    return int(m.group(0)) if m else None

SECTIONS = [("6.2",443,481),("7.7",849,856),("8.3",917,932),("10.1",1016,1027),("10.2",1028,1043)]
L=[]; w=L.append
w("# COMPOSED SECTIONS — `PREREG.md` AS v30a WOULD LEAVE IT")
w("")
w("**SCRATCH composition for an adversarial read. Nothing has been applied to `PREREG.md`,**")
w("**which remains byte-identical to the `prereg-v30` tag.**")
w("")
w("Registered v30 text appears as-is. Text v30a substitutes or inserts is marked **[v30a]** and is")
w("the SAME operative text the signable diff renders. Read each section as a finished whole.")
w("")
for name,a,b in SECTIONS:
    w(""); w("---"); w(""); w(f"# §{name} — as composed"); w("")
    for n in range(a,b+1):
        reps=[h for h in hunks if ln(h)==n and h.get("operation") in ("replace","replace-row")]
        if reps:
            w(f"**[v30a REPLACES registered line {n} — {reps[0].get('clause','')}]**"); w("")
            w(reps[0].get("operative_text") or "[[MISSING]]"); w("")
        else:
            w(pre[n-1])
        for h in [h for h in hunks if ln(h)==n and h.get("operation") in ("insert","marker")]:
            w(""); w(f"**[v30a {h.get('operation').upper()} — {h.get('clause','')}]**"); w("")
            w(h.get("operative_text") or "[[MISSING]]"); w("")
out=D/"_E3_composed_sections.md"
out.write_text("\n".join(L),encoding="utf-8",newline="")
t=out.read_text(encoding="utf-8")
print(f"composed: {t.count(chr(10))} lines, {len(t)} chars, MISSING markers: {t.count('[[MISSING]]')}")
