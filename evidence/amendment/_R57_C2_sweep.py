#!/usr/bin/env python3
"""DELTA R57/C2 - sweep for the C6 claim by IDENTIFIER and NUMERAL, not by prose.

My R56 sweep matched the literal "five tools" against text reading "Five eligible tools,
zero hits" and reported a false clean. That is the third too-narrow-literal in this round.
Prose paraphrases around fixed numbers; the numbers and identifiers are what survive
rewording, so they are what is searched.

POPULATION DECLARED, and proven below by printing what was walked:
  - the whole killgate tree (admitted to the Phase 0 record at R48/Q1(a); X4 item 7a puts
    it on the staging list, so it SHIPS)
  - the whole evidence tree (staged by the ceremony commit, hashed by the manifest)
  - every tracked markdown file at the repo root
  - the amendment scratch tree, so drafting copies are visible too
"""
import pathlib
import re

ROOTS = [
    ("killgate (SHIPS if admitted)",
     pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                  "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                  "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/killgate")),
    ("evidence (SHIPS)",
     pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/evidence")),
    ("repo root (SHIPS)",
     pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")),
    ("amendment scratch (does not ship)",
     pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                  "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                  "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")),
]

# identifiers and numerals, never prose
PATTERNS = [
    ("C6 + zero-hits", re.compile(r"C6.{0,160}?zero\s+hits|zero\s+hits.{0,160}?C6", re.I | re.S)),
    ("C6 + a tool count", re.compile(r"C6.{0,160}?\b(?:5|five)\b\s+\w*\s*tools?|\b(?:5|five)\b\s+\w*\s*tools?.{0,160}?C6", re.I | re.S)),
    ("bare 'zero hits'", re.compile(r"zero\s+hits", re.I)),
    ("flagship", re.compile(r"flagship", re.I)),
    ("T6 / L3.1 (C6's type)", re.compile(r"\bT6\b|\bL3\.1\b")),
]

SUFFIX = {".md", ".txt", ".json", ".csv", ".py"}
hits = {}
walked = 0
for label, root in ROOTS:
    if not root.exists():
        continue
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUFFIX]
    if root.name == "MBO_2025(4mon)+2026-01":
        files = [p for p in root.glob("*.md")]      # root-level docs only; subtrees walked above
    walked += len(files)
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pname, pat in PATTERNS:
            for m in pat.finditer(t):
                line = t[:m.start()].count("\n") + 1
                snippet = re.sub(r"\s+", " ", m.group(0))[:110]
                hits.setdefault((label, str(p), line), []).append((pname, snippet))

print("POPULATION WALKED: %d files across %d roots" % (walked, len(ROOTS)))
for label, root in ROOTS:
    print("   %-36s %s" % (label, root))
print()
print("HITS, grouped by file (identifier/numeral search, not prose):")
print()
by_root = {}
for (label, path, line), ms in sorted(hits.items()):
    by_root.setdefault(label, []).append((path, line, ms))
for label in [l for l, _ in ROOTS]:
    rows = by_root.get(label, [])
    print("  == %s == %d location(s)" % (label, len(rows)))
    for path, line, ms in rows:
        short = path.split("scratchpad")[-1].split("MBO_2025(4mon)+2026-01")[-1]
        pn = ", ".join(sorted({p for p, _ in ms}))
        print("     %s:%d" % (short, line))
        print("        [%s] %s" % (pn, ms[0][1]))
    print()
print("TOTAL LOCATIONS: %d" % len(hits))
