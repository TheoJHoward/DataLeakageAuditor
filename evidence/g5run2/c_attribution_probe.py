"""Which part of H3's change causes the FAIL: the widened scope, or the new detectors?"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "tree" / "tools"))
import check_registration as cr
ROOT = Path(__file__).parent / "tree"

print("=== 1. SINGLE-SOURCE SCAN SET (files now read) ===")
for p in cr.single_source_scan_set(ROOT):
    print("   ", p.relative_to(ROOT).as_posix())

print("\n=== 2. EXCLUSIONS (with reasons) ===")
for d, r in cr.SINGLE_SOURCE_EXCLUDED_DIRS: print(f"    DIR  {d}: {r}")
for f, r in cr.SINGLE_SOURCE_EXCLUDED_FILES: print(f"    FILE {f}: {r}")

OLD_RULES = cr._SINGLE_SOURCE_RULES[:8]   # the 8 pre-H3 detectors
NEW_RULES = cr._SINGLE_SOURCE_RULES[8:]   # the 5 added by H3
print(f"\n=== 3. RULE COUNTS ===\n    pre-H3 detectors: {len(OLD_RULES)}")
print(f"    H3-added detectors: {len(NEW_RULES)}")
print(f"    H3-added definitional detectors: {len(cr._SINGLE_SOURCE_DEFINITIONAL_RULES)}")

state_tokens = ("not_applicable","unsupported","completed","incomplete","short_circuited")
print("\n=== 4. COUNTERFACTUAL: pre-H3 ruleset over the POST-H3 scope set ===")
tot_old = 0
for path in cr.single_source_scan_set(ROOT):
    name = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8"); n = 0
    for lineno, line in cr.normative_lines(path, text):
        for pat, msg in OLD_RULES:
            if re.search(pat, line): n += 1; print(f"    {name}:{lineno} OLD-RULE {msg}")
        if len([t for t in state_tokens if t in line]) >= 3:
            n += 1; print(f"    {name}:{lineno} OLD state-enumeration")
    tot_old += n
    print(f"    -> {name}: {n} finding(s) under pre-H3 rules")
print(f"    TOTAL under pre-H3 ruleset, post-H3 scope: {tot_old}")

print("\n=== 5. ATTRIBUTION OF EACH ACTUAL FINDING TO ITS DETECTOR ===")
from collections import Counter
c = Counter(); per_file = Counter()
for f in cr.check_single_source(ROOT):
    per_file[f.where] += 1
    for i,(pat,msg) in enumerate(cr._SINGLE_SOURCE_RULES):
        if msg in f.detail: c[f"RULE#{i+1} ({'pre-H3' if i<8 else 'H3-ADDED'})"] += 1
    for pat,msg in cr._SINGLE_SOURCE_DEFINITIONAL_RULES:
        if msg in f.detail: c["DEFINITIONAL (H3-ADDED)"] += 1
for k,v in sorted(c.items()): print(f"    {v:2d}  {k}")
print("\n    per-file:", dict(per_file))

print("\n=== 6. IS THE QUOTE EXEMPTION DOING ANYTHING? ===")
blob = cr._prereg_quote_blob(ROOT); exempted = 0
for path in cr.single_source_scan_set(ROOT):
    text = path.read_text(encoding="utf-8"); raw = text.splitlines()
    for lineno, line in cr.normative_lines(path, text):
        if cr._is_attributed_quote(line, raw, lineno, blob):
            exempted += 1
            print(f"    EXEMPT {path.relative_to(ROOT).as_posix()}:{lineno} {line.strip()[:80]!r}")
print(f"    verbatim-attributed-quote exemptions applied: {exempted}")
