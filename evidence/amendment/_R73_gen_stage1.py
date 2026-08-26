#!/usr/bin/env python3
"""§52 stage 1 — extract every clause from SCHEMA_SET_FINAL.md PART 1 and verify
its INSERTION POINT anchor resolves in the CURRENT PREREG.md.

Single source: evidence/amendment/SCHEMA_SET_FINAL.md. Neither applied/PREREG.md
nor PREREG_v30a_DIFF.md is read - both are pre-R49 and reading either would
launder undecided content into the approval package (§52.1).
"""
import hashlib, pathlib, re

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SRC = REPO / "evidence/amendment/SCHEMA_SET_FINAL.md"
PRE = REPO / "PREREG.md"

src = SRC.read_text(encoding="utf-8")
pre_lines = PRE.read_text(encoding="utf-8").split("\n")

print("SOURCE  %s  sha256 %s" % (SRC.name, hashlib.sha256(SRC.read_bytes()).hexdigest()[:16]))
print("TARGET  %s  sha256 %s  (%d lines)\n"
      % (PRE.name, hashlib.sha256(PRE.read_bytes()).hexdigest()[:16], len(pre_lines) - 1))

# PART 1 only
p1 = src[src.index("# PART 1 "):src.index("# PART 2 ")]
blocks = re.split(r"^### (SC-[0-9a-z]+) \u2014 ", p1, flags=re.M)[1:]
clauses = list(zip(blocks[0::2], blocks[1::2]))
print("PART 1 clauses found: %d\n" % len(clauses))

LINEREF = re.compile(r"\*\*INSERTION POINT\.\*\*(.*?)(?:\n\n)", re.S)
NUM = re.compile(r"line \*\*(\d+)\*\*|\*\*line (\d+)\*\*|line (\d+)")
# Delimiters must PAIR WITH THEMSELVES. A mixed character class pairs the backtick
# after `PREREG.md` with the quote before the anchor and returns garbage \u2014 it
# reported "10 anchors not found" before this was fixed.
QUOTED = [re.compile(r'"([^"]{12,})"'),
          re.compile(r"\u201c([^\u201d]{12,})\u201d"),
          re.compile(r"`([^`]{12,})`")]

rows = []
for cid, body in clauses:
    m = LINEREF.search(body)
    ip = m.group(1).strip().replace("\n", " ") if m else ""
    nums = [int(g) for mm in NUM.finditer(ip) for g in mm.groups() if g]
    anchors = [a for q in QUOTED for a in q.findall(ip)]
    status, detail = "NO INSERTION POINT", ""
    if nums:
        ln = nums[0]
        ok = 1 <= ln <= len(pre_lines)
        actual = pre_lines[ln - 1] if ok else ""
        hit = None
        for a in anchors:
            a2 = a.strip().rstrip("\u2026.").strip()
            if len(a2) >= 12 and a2 in actual:
                hit = a2
                break
        if hit:
            status, detail = "ANCHOR OK", "l.%d holds %r" % (ln, hit[:36])
        elif anchors:
            found = [i + 1 for i, l in enumerate(pre_lines)
                     if any(a.strip().rstrip("\u2026.").strip() in l
                            for a in anchors if len(a.strip()) >= 12)]
            status = "ANCHOR MOVED" if found else "ANCHOR NOT FOUND"
            detail = ("cited l.%d; text at %s" % (ln, found[:3])) if found \
                else "cited l.%d; quoted text absent" % ln
        else:
            status, detail = "LINE ONLY (no quoted anchor)", "cited l.%d -> %r" % (ln, actual.strip()[:36])
    rows.append((cid, status, detail))

for cid, status, detail in rows:
    print("  %-8s %-28s %s" % (cid, status, detail))

from collections import Counter
print("\n" + ", ".join("%s: %d" % (k, v) for k, v in Counter(r[1] for r in rows).items()))
