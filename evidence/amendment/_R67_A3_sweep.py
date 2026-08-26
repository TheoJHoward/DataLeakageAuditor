#!/usr/bin/env python3
"""DELTA R67 / A3 - sweep for the GENERAL form of the R23 defect.

A3.1's shape: prose asserting a COUNT of a thing ENUMERATED elsewhere in the same
corpus, with nothing tying the two together.

The defect is not "a count exists". It is "a count exists AND an enumeration
exists AND nothing derives one from the other". So a hit is only reported when an
enumeration is actually FOUND and MEASURED - which makes every hit checkable, and
lets the sweep report AGREE / DISAGREE rather than a pile of candidates.

Scope (A3.3): the six-file set + manifest-carrying prose. REPORT ONLY - no fixes.
"""
import re, pathlib

ROOT = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SIX = ["PREREG.md", "DESIGN.md", "HISTORY.md", "AVAILABILITY_DECLARATION.md"]
ROOTMD = ["README.md", "PRACTICES.md", "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md"]
CEREMONY = sorted(str(p.relative_to(ROOT)).replace("\\", "/")
                  for p in (ROOT / "evidence/ceremony").glob("*.md"))
CORPUS = SIX + ROOTMD + CEREMONY

WORD = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
        "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12}
SETNOUN = (r"invocations?|criteria|criterion|checks?|blockers?|steps?|reasons?|"
           r"categories|elements?|dispositions?|gates?|lessons?|items?|limbs?|"
           r"prongs?|guards?|conditions?|rules?|classes|branches|groups?|"
           r"exceptions?|commands?|stages?|entries")
COUNT = re.compile(r"\b(" + "|".join(WORD) + r"|[2-9]|1[0-2])\s+"
                   r"(?:\w+\s+){0,1}(" + SETNOUN + r")\b", re.I)

LIST_ITEM = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+|\|\s*\*?\*?[A-Za-z0-9`])")
FENCE = re.compile(r"^\s*```")


def clean(l):
    l = re.sub(r"[*_`]+", " ", l)
    for p in (r"\u00a7\s*[A-Z]?\.?\d+(\.\d+)*[a-z]?", r"\b[A-Z]\.\d+", r"\bl\.\s*\d+",
              r"\blines?\s+[\d,\u2013-]+", r"\bv\d+[a-z]?\b", r"\bC\d[a-z]?\b",
              r"\b[A-Z]-?\d+\b", r"\b[0-9a-f]{8,}\b", r"^\s*\d+\.\s",
              r"\b\d{4}-\d{2}(-\d{2})?\b", r"\b\d[\d,]{3,}\b"):
        l = re.sub(p, " ", l)
    return re.sub(r"\s+", " ", l)


def enumeration_after(lines, idx, limit=14):
    """Measure the first contiguous list that starts within `limit` lines."""
    i = idx
    end = min(len(lines), idx + limit)
    while i < end and not LIST_ITEM.match(lines[i]):
        if FENCE.match(lines[i]):
            return None, 0
        i += 1
    if i >= end:
        return None, 0
    start = i
    n = 0
    blanks = 0
    while i < len(lines):
        if LIST_ITEM.match(lines[i]):
            # a table separator row is not an item
            if not re.match(r"^\s*\|[\s:-]+\|", lines[i]):
                n += 1
            blanks = 0
        elif not lines[i].strip():
            blanks += 1
            if blanks >= 2:
                break
        elif not lines[i].startswith((" ", "\t")):
            break
        i += 1
    return start + 1, n


rows = []
for rel in CORPUS:
    p = ROOT / rel
    if not p.exists():
        continue
    lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
    for i, raw in enumerate(lines):
        if raw.lstrip().startswith(("|", ">")):
            continue
        c = clean(raw)
        for m in COUNT.finditer(c):
            tok = m.group(1).lower()
            n = WORD.get(tok)
            if n is None:
                try: n = int(tok)
                except ValueError: continue
            ls, cnt = enumeration_after(lines, i + 1)
            if not ls or cnt < 2:
                continue
            rows.append((rel, i + 1, n, m.group(2).lower(), ls, cnt,
                         "AGREE" if n == cnt else "DISAGREE", raw.strip()))

dis = [r for r in rows if r[6] == "DISAGREE"]
agr = [r for r in rows if r[6] == "AGREE"]
print("A3.2 SWEEP - counts sitting directly above a measurable enumeration")
print("  checkable sites : %d" % len(rows))
print("  count == list   : %d" % len(agr))
print("  count != list   : %d   <- these are the hits worth a P2 call\n" % len(dis))
cur = None
for rel, i, n, noun, ls, cnt, verdict, raw in dis:
    if rel != cur:
        print("\n### " + rel); cur = rel
    print("  line %-5d says %-2d %-12s | list at %-5d has %-2d items" % (i, n, noun, ls, cnt))
    print("        %s" % raw[:120])
