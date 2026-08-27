"""A31 -- is §8.2 item 1 true of the file it would describe? READ-ONLY.

§8.2 item 1, the first thing the amendments block asserts:

    "Where registered text is superseded, the v30 text is retained inline,
     verbatim, at its own site, in a block marked `SUPERSEDED BY v30a` and
     marked NOT operative. **No registered sentence is deleted from this file.**"

R140 §1.2 puts the question and forbids discovering the answer after the block
lands. This answers it.

THE POPULATION IS DERIVED FROM THE FILES, NOT FROM A LIST OF REMOVALS.
`a20b_retention.py` took its population from `PREREG_v30a_APPROVAL.diff`'s five
removal lines. That was right then and is wrong now: A24 superseded two further
v30 lines under a SECOND approval, so a population read from the first approval
misses them. **The question item 1 asks is about every registered sentence that
is gone**, whatever approval removed it -- so the population here is every
non-blank line of `prereg-v30:PREREG.md` that is absent from the applied file.

RETENTION IS CREDITED BY THE MARKER, NOT BY SIMILARITY (A20b). The whole applied
file is normalised to one whitespace-collapsed string so a quotation wrapped
across lines cannot hide, the longest common run is measured, and a run is only
called retention when a retention marker sits at the site.

    usage: a31_item1_check.py <v30-file> <out.json>
"""
from __future__ import annotations

import difflib
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
APPLIED = REPO / "PREREG.md"
V30 = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

MARKERS = ("SUPERSEDED BY v30a", "retained verbatim", "NOT operative",
           "Registered v30 text")


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def norm(s):
    s = re.sub(r"^\s*>+\s?", " ", s, flags=re.M)
    return re.sub(r"\s+", " ", s)


v30 = text_of(V30).split("\n")
applied = text_of(APPLIED).split("\n")

chars, line_at = [], []
for i, l in enumerate(applied, 1):
    piece = norm(l).strip()
    if not piece:
        continue
    if chars:
        chars.append(" ")
        line_at.append(i)
    chars.extend(piece)
    line_at.extend([i] * len(piece))
applied_norm = "".join(chars)
applied_set = set(applied)

print("=" * 78)
print("POPULATION, DERIVED AND ASSERTED FIRST")
print("=" * 78)
print("  prereg-v30:PREREG.md : %d lines" % (len(v30) - 1))
print("  applied PREREG.md    : %d lines" % (len(applied) - 1))

gone = [(i, l) for i, l in enumerate(v30, 1) if l.strip() and l not in applied_set]
print("  v30 lines ABSENT from the applied file: %d" % len(gone))
print("  (population read from the two files, not from any approval's removal list)")
print()

rows = []
for n, textline in gone:
    target = norm(textline).strip()
    sm = difflib.SequenceMatcher(None, target, applied_norm, autojunk=False)
    m = sm.find_longest_match(0, len(target), 0, len(applied_norm))
    cov = m.size / len(target) if target else 0.0
    at = line_at[m.b] if m.b < len(line_at) else None
    marked = False
    if at:
        near = "\n".join(applied[max(0, at - 7):at + 1])
        marked = any(k in near for k in MARKERS)
    verdict = ("RETAINED" if cov >= 0.995 and marked else
               "RETAINED (part, marked)" if cov >= 0.25 and marked else
               "NOT RETAINED")
    rows.append({"v30_line": n, "coverage": round(cov, 3), "at": at,
                 "marked": marked, "verdict": verdict, "text": target[:100]})

print("=" * 78)
print("EVERY SUPERSEDED REGISTERED SENTENCE, AND WHETHER IT IS RETAINED")
print("=" * 78)
print("  %-9s %-24s %-9s %-7s %s" % ("v30 line", "verdict", "coverage", "at l.", "marker?"))
for r in rows:
    print("  %-9d %-24s %-9.3f %-7s %s"
          % (r["v30_line"], r["verdict"], r["coverage"], r["at"],
             "yes" if r["marked"] else "no"))
    print("        %s" % r["text"][:96])

ok = [r for r in rows if r["verdict"].startswith("RETAINED")]
bad = [r for r in rows if r["verdict"] == "NOT RETAINED"]
print()
print("=" * 78)
print("§8.2 ITEM 1 -- \"No registered sentence is deleted from this file.\"")
print("=" * 78)
print("  superseded sentences : %d" % len(rows))
print("  RETAINED with a marker at the site : %d  -> item 1 holds for these" % len(ok))
print("  NOT retained anywhere              : %d  -> item 1 is FALSE of these" % len(bad))
for r in bad:
    print("      v30 l.%-5d %s" % (r["v30_line"], r["text"][:84]))
print()
if bad:
    print("  ITEM 1 IS FALSE OF THIS FILE. Landing §8.2 as drafted would put that")
    print("  claim into registered text -- false in exactly the way the block exists")
    print("  to prevent.")
else:
    print("  Item 1 is TRUE of this file.")

OUT.write_text(json.dumps({"superseded": len(rows), "retained": len(ok),
                           "not_retained": len(bad), "rows": rows},
                          indent=1), encoding="utf-8")
print()
print("wrote %s" % OUT)
