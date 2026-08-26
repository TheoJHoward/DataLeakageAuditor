#!/usr/bin/env python3
"""Prototype for §16's D1/D2 matching. Tune here, then port into the tool."""
import re, pathlib

ROOT = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
CORPUS = ["AVAILABILITY_DECLARATION.md", "PREREG.md", "DESIGN.md", "HISTORY.md", "README.md",
          "evidence/ceremony/CEREMONY_COMMANDS.md", "evidence/ceremony/COMMIT_PLAN.md",
          "evidence/ceremony/DEVIATIONS_DRAFT.md", "evidence/ceremony/H34_DRAFT.md"]

auth = (ROOT / "evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8")
FILES = re.search(r'^FILES="([^"]+)"', auth, re.M).group(1).split()
N = len(FILES)
print("AUTHORITY $FILES = %d paths\n" % N)

WORD = {"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,
        "second":2,"third":3,"fourth":4,"fifth":5,"sixth":6,"seventh":7}

def strip_refs(l):
    """Remove things that LOOK like counts but are addresses."""
    l = re.sub(r"§\s*[A-Z]?\.?\d+(\.\d+)*[a-z]?", " ", l)   # §6.2, §D.2, §3.2
    l = re.sub(r"\b[A-Z]\.\d+", " ", l)                      # D.2, A.11
    l = re.sub(r"\bl\.\s*\d+", " ", l)                       # l.180
    l = re.sub(r"\blines?\s+[\d,\u2013\-]+", " ", l)          # lines 184-186
    l = re.sub(r"\bv\d+[a-z]?\b", " ", l)                     # v30, v30a
    l = re.sub(r"\bC\d[a-z]?\b", " ", l)                      # C2a, C1c
    l = re.sub(r"\b[A-Z]-?\d+\b", " ", l)                     # R7, H-34, D-001
    l = re.sub(r"`[^`]*`", " ", l)                            # inline code
    l = re.sub(r"^\s*\d+\.\s", " ", l)                        # "3. " list marker
    l = re.sub(r"\b[0-9a-f]{8,}\b", " ", l)                   # hashes
    return l

# a count literal ABOUT the v30a hash set
NUMW = re.compile(r"\b(two|three|four|five|six|seven|eight|second|third|fourth|fifth|sixth|seventh)\b", re.I)
NUMD = re.compile(r"\b([2-8])\s+(?:hashes|hash lines|SHA-?256 lines|files\b)", re.I)
CTX = re.compile(
    r"(tag[- ]message[^.]{0,45}(hash|SHA-?256|line)"
    r"|(hash|SHA-?256)[^.]{0,35}tag message"
    r"|\$FILES|FILES=|files whose hashes"
    r"|hash(es)?[^.]{0,18}(block|set)\b"
    r"|(each |all |one of |member of |of )the (six|seven|five)\b"
    r"|(six|seven|five)[- ]line block"
    r"|the (fifth|sixth|seventh) hash)", re.I)
V30 = re.compile(r"prereg-v30\b(?!a)|the v30 |v30 (tag|order|block|five|era|-era)", re.I)

rows = []
for rel in CORPUS:
    p = ROOT / rel
    if not p.exists():
        print("  MISSING:", rel); continue
    for i, raw in enumerate(p.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        if not CTX.search(raw):
            continue
        clean = strip_refs(raw)
        nums = {WORD[w.lower()] for w in NUMW.findall(clean)}
        nums |= {int(d) for d in NUMD.findall(clean)}
        nums = {n for n in nums if 2 <= n <= 8}
        if not nums:
            continue
        bad = sorted(n for n in nums if n != N)
        if not bad:
            continue
        rows.append((rel, i, bad, bool(V30.search(raw)), raw.strip()))

print("=== lines carrying a count != %d in v30a-hash-set context ===" % N)
for rel, i, bad, v30, l in rows:
    print("  %-40s %5d  saw=%s  %s" % (rel, i, bad, "[v30 ctx]" if v30 else ""))
    print("        %s" % l[:150])
print("\nTOTAL requiring disposition: %d" % len(rows))
