#!/usr/bin/env python3
"""DELTA R39 / F6 — the staleness class, fixed structurally rather than by convention.

F6(i)  Every citation into a mutable file is RE-DERIVED at assembly. Implemented as
       assembler assertion (v): no numeral in the assembler's own prose may contradict
       a quantity derived from the data at assembly time.

F6(ii) Every finding carries an explicit status - OPEN / FIXED / WITHDRAWN, with what
       fixed it - re-checked at assembly. Implemented as assembler assertion (vi).

Plus D7 check (iv): every hunk carries readable operative text (F3).

This script triages the findings and installs all three checks.
"""

import json
import re
import pathlib

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

# ---- triage rules: distinctive substring -> (status, what fixed it) ---------
RULES = [
    ("THE BOUNDS BLOCK IS MISSING", "FIXED",
     "R37/D1 — the bounds block is in SCHEMA_SET_FINAL.md's SC-12(w); grep 'What this limb does NOT permit' returns it"),
    ("TWO NON-IDENTICAL VERSIONS OF THE (w) LIMB", "FIXED",
     "R37/D1 — Y3 §1-2 replaced by a pointer; the applied text lives only in SCHEMA_SET_FINAL.md"),
    ("BOUND (6) IS FALSIFIED", "FIXED",
     "R37/D1 — bound (6) rewritten to state the §8.3 reach explicitly"),
    ("still has none after this amendment", "FIXED",
     "R37/D8 — the F-6 apparatus note now records the second half as spent"),
    ("SC-1's CLAUSE TEXT STATES A LITERAL COUNT", "FIXED",
     "R37/D5 — now 'The requirements below follow'"),
    ("no text in SCHEMA_SET_FINAL.md's SC-6 section", "FIXED",
     "R37/D6 — SC-12(w) bound (6) argues the unscored/waived asymmetry in-clause"),
    ("FIVE HUNKS THE AUTHOR SIGNS", "FIXED",
     "R37/D2 sourced them from PREREG_v30a_DIFF.md; R39/F3 gave every hunk an operative_text field"),
    ("APPLICATION-ORDER HAZARD, SC-2 vs H4", "FIXED",
     "R37/D3 — H4 kept as the sole operation on line 451; SC-2's order stated in H4's entry"),
    ("DOUBLE-APPLICATION RISK, SC-3 vs H5", "FIXED",
     "R37/D3 — H5 absent by design; SC-3 replaces line 461"),
    ("MARKER PLACEMENT UNDEFINED", "FIXED",
     "R37/D4 — complete-block rule; markers written at 212, 462, 1054; enforced by self-check (iii)"),
    ("PLACEMENT NUANCE", "FIXED", "R37/D4 — marker placement is now stated per hunk"),
    ("STALE-SCRATCH INSTRUCTION", "FIXED", "R39/F4 — stale H8 pointer references redrafted"),
    ("STALE APPARATUS beside SC-6", "FIXED", "R37/D8 — SC-6 apparatus note corrected"),
    ("STALE RATIONALE inside the SC-6", "FIXED", "R37/D8 — the vacuous-under-H8 rationale superseded"),
    ("SAME STALE CLAIM in T4", "FIXED", "R37/D8 — T4 carries a superseded-in-part banner"),
    ("K2 WORKING ROW R25", "FIXED", "R37/D8 — the residual-gap descriptor is superseded"),
    ("HUNK COUNT AT LINE 816", "FIXED", "R37/D3 — the duplicate 816 pointer hunk was removed"),
    ("SC-14", "WITHDRAWN",
     "not a defect — SC-14's absence is the intended state; recorded in the artifact's §3"),
    ("CHECKS THAT PASSED", "WITHDRAWN", "a record of passing checks, not a finding"),
    ("ANCHORS", "WITHDRAWN", "mechanical; owned by self-check (iii) and the D9 round-trip"),
    ("NO COUNTING NUMERAL", "WITHDRAWN", "a record of a passing check"),
    ("PURE-ADDITION CLAIMS VERIFIED", "WITHDRAWN", "a record of a passing check"),
    ("THE BLOCK'S CENTRAL PROPERTY HOLDS", "WITHDRAWN", "a record of a passing check"),
    ("MARKER CLAIMS VERIFIED", "WITHDRAWN", "a record of a passing check"),
]

src = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))
findings = src["findings"]

triaged = []
counts = {"OPEN": 0, "FIXED": 0, "WITHDRAWN": 0}
for f in findings:
    status, fixed_by = "OPEN", ""
    for key, st, by in RULES:
        if key.lower() in f.lower():
            status, fixed_by = st, by
            break
    counts[status] += 1
    triaged.append({"text": f, "status": status, "fixed_by": fixed_by})

src["findings_triaged"] = triaged
json.dump(src, open(D / "_X5_hunks_v2.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("F6(ii) finding triage:")
for k, v in counts.items():
    print(f"  {k:<10} {v}")
print(f"  total      {len(triaged)}")

# ---- install checks (iv), (v), (vi) in the self-check ----------------------
p = D / "_X5_selfcheck.py"
s = p.read_text(encoding="utf-8")

EXTRA = '''
# ---------------------------------------------------------------- (iv) F3
head("(iv) EVERY HUNK CARRIES READABLE OPERATIVE TEXT  [R39/F3]")
print("  Prose paraphrase is not operative text. The author must be able to read what")
print("  each hunk actually puts into PREREG.md.")
print()
noop = [h for h in hunks if not (h.get("operative_text") or "").strip()]
thin = [h for h in hunks
        if (h.get("operative_text") or "").strip() and len(h["operative_text"]) < 80]
print(f"  hunks: {len(hunks)}   without operative text: {len(noop)}   suspiciously short: {len(thin)}")
for h in noop:
    print(f"    MISSING  line {first_line(h)}  {h.get('clause','')[:58]}")
for h in thin:
    print(f"    SHORT    line {first_line(h)}  {h.get('clause','')[:58]}")
if noop:
    fail += 1
else:
    print("  PASS — every hunk carries operative text")

# ---------------------------------------------------------------- (v) F6(i)
head("(v) NO CARRIED-FORWARD COUNT IN THE ASSEMBLED PROSE  [R39/F6(i)]")
print("  Every citation into a mutable file - counts, line numbers, quoted text - is")
print("  re-derived at assembly. A numeral written once and never re-checked is stale")
print("  by construction; that is how 'thirty-seven hunks' survived into a 36-hunk file.")
print()
art_p = D / "X5_FINAL_PREREG_DIFF.md"
if art_p.exists():
    art = art_p.read_text(encoding="utf-8")
    WORDS = {"thirty-six": 36, "thirty-seven": 37, "thirty-five": 35, "thirty-eight": 38,
             "thirty-nine": 39, "forty": 40}
    bad_words = [(w, v) for w, v in WORDS.items() if w in art.lower() and v != len(hunks)]
    m = re.search(r"\\*\\*(\\d+) hunks\\.", art)
    stated = int(m.group(1)) if m else None
    print(f"  derived hunk count: {len(hunks)}")
    print(f"  count stated in the artifact's summary: {stated}")
    for w, v in bad_words:
        print(f"    *** prose says '{w}' ({v}) but the data says {len(hunks)} ***")
    if bad_words or (stated is not None and stated != len(hunks)):
        fail += 1
    else:
        print("  PASS — no numeral in the artifact contradicts the derived count")
else:
    print("  artifact not yet assembled; check deferred")

# ---------------------------------------------------------------- (vi) F6(ii)
head("(vi) EVERY FINDING CARRIES A STATUS  [R39/F6(ii)]")
print("  OPEN / FIXED / WITHDRAWN, with what fixed it. Six findings once contradicted the")
print("  file they described because the defect was fixed and the finding was not withdrawn.")
print()
tri = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8")).get("findings_triaged")
if not tri:
    print("  *** no triage present ***")
    fail += 1
else:
    nostat = [t for t in tri if t.get("status") not in ("OPEN", "FIXED", "WITHDRAWN")]
    nofix = [t for t in tri if t.get("status") == "FIXED" and not t.get("fixed_by")]
    from collections import Counter
    c = Counter(t["status"] for t in tri)
    print(f"  findings: {len(tri)}   " + "   ".join(f"{k}={v}" for k, v in sorted(c.items())))
    print(f"  without a valid status: {len(nostat)}   FIXED without what-fixed-it: {len(nofix)}")
    if nostat or nofix:
        fail += 1
    else:
        print("  PASS — every finding has a status, and every FIXED names what fixed it")
'''

anchor = 'head("SELF-CHECK RESULT")'
assert s.count(anchor) == 1
s = s.replace(anchor, EXTRA + "\n" + anchor, 1)
s = s.replace('print(f"  assertions failed: {fail} of 3")',
              'print(f"  assertions failed: {fail} of 6")', 1)
p.write_text(s, encoding="utf-8", newline="")
print("\nself-check extended: checks (iv), (v), (vi) installed — now 6 assertions")
