"""A20b -- does each approved deletion retain its text? READ-ONLY.

THE PREVIOUS PROBE WAS A SAMPLE AND THIS IS A DERIVATION (§2.1). A20 asked
"does an 80-character prefix of the deleted line appear on some line of the
applied file?" and answered NOWHERE for four of five. That is a sample: it can
only ever bound the answer, and it misses the case §8.2 actually describes --
a retention block that QUOTES the old sentence inside a blockquote, where the
quotation wraps across lines and no single line carries the prefix.

So this does not test the applied file for a property. It NORMALISES both sides
-- blockquote markers stripped, all whitespace collapsed to single spaces, the
whole file as one string -- and then, for each deleted sentence, finds the
LONGEST COMMON SUBSTRING between that sentence and the entire applied file.
Line boundaries stop existing, so wrapping cannot hide anything.

WHAT IS REPORTED, per deletion:

  coverage     the longest run of the deleted sentence that survives anywhere,
               as a fraction of the sentence. 1.0 is verbatim retention;
               0.0 is nothing; anything between is a partial and is shown so a
               reader can judge it rather than being handed a yes/no.
  where        the applied line the surviving run starts on
  marked       whether a retention marker sits within six lines above it
  citations    lines of the applied file that still refer to the deleted
               surface -- because a deletion whose citations survive is an
               APPLIED defect (§1.2), not a description defect

A COVERAGE FLOOR, NOT A THRESHOLD. Short runs match by accident: "the" occurs
everywhere. The floor below is stated and applied to the REPORT, never to the
verdict -- every row prints its number.

    usage: a20b_retention.py <v30-file> <out.json>
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
DIFF = REPO / "evidence/amendment/PREREG_v30a_APPROVAL.diff"

V30 = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

FLOOR = 0.25            # below this, a match is reported as ACCIDENTAL


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def norm(s: str) -> str:
    """Blockquote markers out, all whitespace to single spaces."""
    s = re.sub(r"^\s*>+\s?", " ", s, flags=re.M)
    return re.sub(r"\s+", " ", s)


v30_lines = text_of(V30).split("\n")
applied_lines = text_of(APPLIED).split("\n")

# THE NORMALISED TEXT AND ITS LINE INDEX ARE BUILT IN ONE PASS, so they are the
# same string by construction. A first version normalised the joined file and
# then rebuilt the index line by line; `norm` collapses runs of whitespace, so
# consecutive blank lines became ONE space in the text and one space EACH in the
# index, and the reported line number drifted further the deeper into the file a
# hit was -- 1658 for a passage at 1678. Two derivations of one thing will
# disagree; there is only one here.
_chars: list[str] = []
line_at: list[int] = []
for i, l in enumerate(applied_lines, 1):
    piece = norm(l).strip()
    if not piece:
        continue                       # a blank line contributes no characters
    if _chars:
        _chars.append(" ")
        line_at.append(i)
    _chars.extend(piece)
    line_at.extend([i] * len(piece))
applied_norm = "".join(_chars)
assert len(applied_norm) == len(line_at), "text and index must be one pass"

print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS JUDGED")
print("=" * 78)
print("  v30                : %d lines" % (len(v30_lines) - 1))
print("  applied PREREG.md  : %d lines" % (len(applied_lines) - 1))
print("  applied normalised : %d characters" % len(applied_norm))

# The deletions ARE the approval diff's removal lines. Derived from the diff,
# not from a hand-kept list -- a hand-kept list is the thing this round is
# correcting everywhere else.
removals = [l[1:] for l in text_of(DIFF).split("\n")
            if l.startswith("-") and not l.startswith("--- ")]
print("  approved removals  : %d (read from the approval diff)" % len(removals))
if not removals:
    sys.exit("HALT: no removal lines parsed from the approval diff. An empty "
             "population is not an empty finding.")
print()


def v30_lineno(text):
    hits = [i for i, l in enumerate(v30_lines, 1) if l == text]
    return hits[0] if len(hits) == 1 else None


rows = []
for text in removals:
    n = v30_lineno(text)
    target = norm(text).strip()
    sm = difflib.SequenceMatcher(None, target, applied_norm, autojunk=False)
    m = sm.find_longest_match(0, len(target), 0, len(applied_norm))
    coverage = m.size / len(target) if target else 0.0
    at_line = line_at[m.b] if m.b < len(line_at) else None
    marked = False
    if at_line:
        near = "\n".join(applied_lines[max(0, at_line - 7):at_line + 1])
        marked = any(k in near for k in
                     ("SUPERSEDED BY v30a", "retained verbatim", "NOT operative",
                      "Registered v30 text"))
    # A LONG COMMON SUBSTRING IS NOT A QUOTATION. " under the reconstructed
    # declaration" is 36 characters of shared vocabulary between two clauses
    # about the same subject; scoring it as partial retention would report the
    # registration's own house style as evidence. Partial retention is credited
    # only where a RETENTION MARKER sits at the site -- which is what §8.2
    # actually promises ("in a block marked SUPERSEDED BY v30a") and the only
    # form a reader could recognise as a retention.
    verdict = ("RETAINED VERBATIM" if coverage >= 0.995 else
               "RETAINED IN PART" if coverage >= FLOOR and marked else
               "NOT RETAINED")
    rows.append({
        "v30_line": n, "coverage": round(coverage, 3),
        "longest_run_chars": m.size, "sentence_chars": len(target),
        "at_applied_line": at_line, "marked": marked, "verdict": verdict,
        "surviving_run": target[m.a:m.a + m.size][:120],
        "sentence": target[:120],
    })

print("=" * 78)
print("RETENTION -- longest surviving run of each deleted sentence")
print("=" * 78)
print("  %-9s %-19s %-9s %-8s %-8s %s"
      % ("v30 line", "verdict", "coverage", "run/len", "at l.", "marker near?"))
for r in rows:
    print("  %-9s %-19s %-9.3f %-8s %-8s %s"
          % (r["v30_line"], r["verdict"], r["coverage"],
             "%d/%d" % (r["longest_run_chars"], r["sentence_chars"]),
             r["at_applied_line"], "yes" if r["marked"] else "no"))
    print("        deleted : %s" % r["sentence"][:104])
    print("        survives: %s" % (r["surviving_run"][:104] or "(nothing)"))

# ---- live citations of a deleted surface ----------------------------------
# A deletion whose citations survive is an APPLIED defect, not a description
# defect (§1.2). The probe is the deleted line's most distinctive noun phrase,
# taken from the line itself rather than invented.
print()
print("=" * 78)
print("LIVE CITATIONS OF DELETED TEXT -- these are APPLIED defects (§1.2)")
print("=" * 78)
print("TWO SCREENS, EACH WITH ITS BOUND STATED. A citation of a deleted object is")
print("a semantic property and no regex decides it, so neither screen pretends to.")
print()
print("  (a) BY LINE NUMBER -- fully derived. Any applied line naming the")
print("      deleted surface's v30 line number cites something that is gone.")
print("  (b) DEICTIC, UNATTRIBUTED -- every `that row` / `the row above` /")
print("      `this table` in the file, listed ONCE and routed by a human.")
print("      A first version attributed these by PROXIMITY to where the deleted")
print("      sentence's longest surviving run happened to sit -- which is not")
print("      the deletion's site at all -- and put l.1544's `that row`, which")
print("      refers to §7.7's deleted row at v30 l.855, onto v30 l.929 because")
print("      it was 21 lines away. Proximity is not reference. The list is")
print("      unattributed and complete rather than attributed and wrong.")
print()

DEICTIC = re.compile(r"\b(that row|the row above|this row|that table|the table above"
                     r"|the enumeration above|that entry|the entry above)\b", re.I)

for r in rows:
    n = r["v30_line"]
    print("  (a) v30 l.%s" % n)
    by_num = []
    if n:
        rx = re.compile(r"\bline %d\b" % n)
        for i, l in enumerate(applied_lines, 1):
            if rx.search(l):
                by_num.append({"line": i, "text": l.strip()[:100]})
    r["citations_by_line_number"] = by_num
    if not by_num:
        print("        none")
    for h in by_num:
        print("        l.%-5d %s" % (h["line"], h["text"]))
    print()

deictic = [{"line": i, "text": l.strip()[:104]}
           for i, l in enumerate(applied_lines, 1) if DEICTIC.search(l)]
print("  (b) DEICTIC REFERENCES, whole file, unattributed -- %d" % len(deictic))
for h in deictic:
    print("        l.%-5d %s" % (h["line"], h["text"]))
print()
print("      Each needs a human to say what its referent is and whether that")
print("      referent still exists. That is A22's job, not this screen's.")

OUT.write_text(json.dumps({"floor": FLOOR, "removals": len(removals),
                           "rows": rows}, indent=1), encoding="utf-8")
print("wrote %s" % OUT)
