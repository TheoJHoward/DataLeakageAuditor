#!/usr/bin/env python3
"""B1.1 — audit every D1-D7 exemption: pinned to a LINE, or to a VALUE?"""
import re, pathlib

ROOT = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
src = (ROOT / "tools/check_registration.py").read_text(encoding="utf-8")

KEY = re.compile(r'\("([^"]+)", (\d+)\): \(\n\s+"((?:[^"\\]|\\.)*)"', re.M)


def table(name):
    m = re.search(r"^%s = \{(.*?)^\}" % name, src, re.S | re.M)
    return KEY.findall(m.group(1)) if m else []


FILES = re.search(r'^FILES="([^"]+)"',
                  (ROOT / "evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8"),
                  re.M).group(1).split()
N = len(FILES)

WORD = {"both": 2, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
        "seven": 7, "eight": 8, "fifth": 5, "sixth": 6, "seventh": 7}
NOUN = r"(?:hashes|hash\s+lines|hash|SHA-?256\s+lines|SHA-?256|line\s+block|lines)"
ATT = re.compile(r"\b(both|two|three|four|five|six|seven|eight|fifth|sixth|seventh)\b"
                 r"(?:[-\s]+(?:\w+\s+){0,2})?" + NOUN, re.I)
STRIP = [r"\u00a7\s*[A-Z]?\.?\d+(\.\d+)*[a-z]?", r"\b[A-Z]\.\d+", r"\bl\.\s*\d+",
         r"\blines?\s+[\d,\u2013\-]+", r"\bv\d+[a-z]?\b", r"\bC\d[a-z]?\b",
         r"\b[A-Z]-?\d+\b", r"`[^`]*`", r"^\s*\d+\.\s", r"\b[0-9a-f]{8,}\b"]


def strip(line):
    out = re.sub(r"[*_]+", " ", line)
    for p in STRIP:
        out = re.sub(p, " ", out)
    return re.sub(r"\s+", " ", out)


d1 = table("_HASH_SET_EXEMPT")
d2 = table("_HASH_SET_ENUM_EXEMPT")
d7 = table("_D7_EXEMPT")

print("=== D1 / D5 / D6 COUNT exemptions: %d  (currently LINE-pinned) ===" % len(d1))
for path, ln, pin in d1:
    line = (ROOT / path).read_text(encoding="utf-8", errors="replace").split("\n")[int(ln) - 1]
    vals = sorted({WORD[m.group(1).lower()] for m in ATT.finditer(strip(line))})
    print('    ("%s", %s): allow %s' % (path, ln, [v for v in vals if v != N]))

print("\n=== D2 / D6 ENUMERATION exemptions: %d  (currently LINE-pinned) ===" % len(d2))
for path, ln, pin in d2:
    L = (ROOT / path).read_text(encoding="utf-8", errors="replace").split("\n")
    i = int(ln)
    win = " ".join(L[max(0, i - 2): i + 3])
    print('    ("%s", %s): allow %s' % (path, ln, [b for b in FILES if b in win]))

print("\n=== D7 exemptions: %d  (already VALUE-scoped, R68) ===" % len(d7))
for path, ln, pin in d7:
    print("    %s:%s" % (path, ln))

print("\nTOTAL EXEMPTIONS: %d   line-pinned: %d   value-scoped: %d"
      % (len(d1) + len(d2) + len(d7), len(d1) + len(d2), len(d7)))
