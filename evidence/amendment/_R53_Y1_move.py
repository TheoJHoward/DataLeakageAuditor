#!/usr/bin/env python3
"""DELTA R53/Y1 - move H31's and H32's text into SCHEMA_SET_FINAL.md.

WHY. Both lived in `_X5_hunks_v2.json` alone because they were drafted inside a delta -
a historical accident, not a design decision. The consequence: the amendment's newest
and most-revised normative text (the narrowest C2, redrafted at R47/P1) was the ONLY
applied text no provenance check could reach.

ONE SOURCE OF RECORD. They go into SCHEMA_SET_FINAL.md PART 1, under their own
headings, alongside every other piece of applied text. No second document for
delta-drafted hunks - that would be the duplicated-authority shape this registration
forbids.

MECHANICS, checked before writing (Y2):
  - FENCED blocks, not blockquotes: the enumerator already treats fences as population
    blocks (3 of the 33 frozen blocks are fences), and a fence takes its content
    literally, so H32's plain list item and H31's leading-space nested quote both
    survive without re-quoting games.
  - APPENDED at PART 1's tail, after the last existing block and before the PART 2
    rule, so NO existing block's line range shifts and no re-anchor is needed.
  - They become section-A blocks, bound by M6 check (II), which asserts `src in op` -
    the SOURCE contained in the HUNK. That is the converse direction, so it catches
    deletions. Section-A binding was already deletion-safe; section B was not.

Prose around each fence is plain paragraph text, not blockquoted, so exactly ONE new
population block is created per hunk.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

hunks = json.loads((D / "_X5_hunks_v2.json").read_text(encoding="utf-8"))["hunks"]


def ln(h):
    m = re.search(r"\d+", h.get("prereg_line", "") or "")
    return int(m.group(0)) if m else 9999


HN = {f"H{i}": h for i, h in enumerate(sorted(hunks, key=ln), 1)}
op31 = HN["H31"]["operative_text"]
op32 = HN["H32"]["operative_text"]
assert op31.lstrip().startswith("> **\u00a710.1 line 1022"), op31[:40]
assert op32.startswith("3. Fires on `fixture_contaminated`"), op32[:40]

NEW = """
## \u00a710.1 LINE 1022 \u2014 THE KILL-GATE CRITERION 3 PAIR (source of record, moved here at R53/Y1)

**Why these two are here.** Both were drafted inside deltas \u2014 the operative item at R39/F2, the
retention block at K2 \u00a79.2 \u2014 and redrafted at R47/P1 to the narrowest C2. Until this move
`_X5_hunks_v2.json` was their only source of record, which left **the amendment's most-revised
normative text as the only applied text no provenance check could reach.** They now sit where every
other piece of applied text sits. The manifest claims them in \u00a7A and M6 check (II) binds them, which
asserts the source block is contained in the hunk \u2014 the direction that catches a deletion.

**Order of application (R39/F2), unchanged by the move:** the REPLACE lands first; the retention
blockquote is then written directly beneath the resulting operative item 3, before item 4.

### \u00a710.1-C2op \u2014 THE C2 OPERATIVE ITEM (replaces `PREREG.md` line 1022)

```
""" + op32 + """
```

### \u00a710.1-C2ret \u2014 THE C2 RETENTION BLOCK (inserted beneath the operative item)

```
""" + op31 + """
```

"""

ssf = D / "SCHEMA_SET_FINAL.md"
s = ssf.read_text(encoding="utf-8")
MARK = "\n---\n\n# PART 2 \u2014 S1: R32 APPLIED"
assert s.count(MARK) == 1, "PART 2 boundary match %d" % s.count(MARK)
assert "\u00a710.1-C2op" not in s, "already moved"
s = s.replace(MARK, "\n" + NEW + MARK, 1)
ssf.write_text(s, encoding="utf-8")
print("SCHEMA_SET_FINAL.md: two fenced blocks appended at PART 1's tail (+%d lines)"
      % len(NEW.split("\n")))
print("  C2 operative item : %d chars" % len(op32))
print("  C2 retention block: %d chars" % len(op31))
