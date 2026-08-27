"""A23 -- extract the two drafted §6.2 replacements and PRESENT them as a diff.

APPLIES NOTHING. It writes a proposal document and exits. R137 §1.2: "PRESENT A
PREREG DIFF for the author's approval. Do not apply it."

THE HUNK TEXT IS EXTRACTED, NEVER RETYPED. §1.2 says "wording unchanged from
the drafted text where drafted text exists", and the only way to guarantee that
is to read the words out of `PREREG_v30a_DIFF.md` rather than transcribe them.
Both the anchors and the replacements come from that file; nothing here is
authored except the framing.

ANCHORS ARE LOCATED, NEVER OFFSET. The drafted diff names v30 line numbers. The
applied file has moved 976 lines since; the recorded number is used only to
cross-check what was found, and the match itself is by exact line content. A
match count other than one halts -- a replacement applied against an ambiguous
anchor is a replacement applied somewhere nobody chose.

AND THE ANCHOR IS CHECKED FOR STILL BEING v30's TEXT. If the line the anchor
names has already been amended, this proposal is stale and would overwrite
something. That check is the point of A20's whole method applied one more time:
verify against the file, never against the plan.

    usage: a23_draft_diff.py <out.md>
"""
from __future__ import annotations

import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
DRAFT = REPO / "evidence/amendment/PREREG_v30a_DIFF.md"
PREREG = REPO / "PREREG.md"
OUT = pathlib.Path(sys.argv[1])


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


draft = text_of(DRAFT)
prereg_lines = text_of(PREREG).split("\n")

WANTED = [
    ("H2", "§6.2 reference AUC anchor", "Reference AUC anchor"),
    ("H3", "§6.2 contamination availability class", "Contamination availability class"),
]

print("=" * 78)
print("POPULATION, ASSERTED BEFORE ANYTHING IS EXTRACTED")
print("=" * 78)
print("  PREREG_v30a_DIFF.md : %d lines" % len(draft.split("\n")))
print("  PREREG.md           : %d lines" % (len(prereg_lines) - 1))
print("  hunks requested     : %s" % ", ".join(h for h, _, _ in WANTED))
print()

FENCE = re.compile(r"```\n(.*?)\n```", re.S)


def section(hid):
    start = draft.index("### %s — " % hid)
    nxt = draft.find("\n### ", start + 1)
    return draft[start:nxt if nxt > 0 else len(draft)]


hunks = []
for hid, title, stem in WANTED:
    body = section(hid)
    m = re.search(r"\*\*ANCHOR — `PREREG\.md` line (\d+), match count 1:\*\*\n\n```\n(.*?)\n```",
                  body, re.S)
    if not m:
        sys.exit("HALT: %s -- no anchor block found" % hid)
    v30_line, anchor = int(m.group(1)), m.group(2)

    # H2 writes `REPLACE with (4 lines).**` and H3 writes `REPLACE with (4 lines):**`
    # -- a period against a colon. The first version required the period and
    # halted on H3. It halted rather than matching something else, which is the
    # right failure, but the label is punctuation and the pattern should not be
    # a spelling test.
    m2 = re.search(r"\*\*REPLACE with \((\d+) lines?\)[.:]\*\*.*?```\n(.*?)\n```",
                   body, re.S)
    if not m2:
        sys.exit("HALT: %s -- no REPLACE block found" % hid)
    declared_n, replacement = int(m2.group(1)), m2.group(2)
    repl_lines = replacement.split("\n")

    hits = [i for i, l in enumerate(prereg_lines, 1) if l == anchor]
    if len(hits) != 1:
        sys.exit("HALT: %s -- its anchor matches %d lines of PREREG.md, expected "
                 "exactly 1. A replacement applied against an ambiguous anchor "
                 "is applied somewhere nobody chose." % (hid, len(hits)))
    at = hits[0]

    # STILL v30's TEXT? If the site had already been amended the anchor would not
    # match, so a match IS the check -- stated because it is easy to mistake this
    # for an unchecked assumption.
    already = stem in "\n".join(prereg_lines) and any(
        stem in l and "v30a" in l for l in prereg_lines)
    if already:
        sys.exit("HALT: %s -- PREREG.md already carries a v30a clause naming %r. "
                 "This proposal is stale." % (hid, stem))

    if len(repl_lines) != declared_n:
        print("FINDING  %s: the heading declares %d replacement lines; the block "
              "carries %d. The label is metadata about the hunk, not the hunk's "
              "wording -- reported, and the block used as it stands."
              % (hid, declared_n, len(repl_lines)))

    hunks.append({"id": hid, "title": title, "v30_line": v30_line,
                  "applied_line": at, "anchor": anchor, "replacement": repl_lines})
    print("  %-3s anchor located at applied l.%-5d (drafted against v30 l.%d) — "
          "%d replacement line(s), no v30a clause present at the site"
          % (hid, at, v30_line, len(repl_lines)))

# ---- emit the proposal ------------------------------------------------------
buf = []
w = buf.append
w("# A23 — PROPOSED `PREREG.md` DIFF, FOR APPROVAL. **NOT APPLIED.**")
w("")
w("**Nothing in this document has been applied.** `PREREG.md` is unchanged at")
w("`0c8da19f237cd243…`. R137 §1.2: *\"PRESENT A PREREG DIFF for the author's approval. Do not")
w("apply it.\"* R137 §1.4: `PREREG.md` is edited only by applying a diff the author has explicitly")
w("approved, and this delta does not authorise applying one.")
w("")
w("**The wording is extracted, not retyped.** Every line below comes out of")
w("`PREREG_v30a_DIFF.md`; §1.2 requires \"wording unchanged from the drafted text where drafted")
w("text exists\", and reading the words from the source is the only way to guarantee that.")
w("")
w("**Each anchor was LOCATED, not offset**, and matches exactly one line of `PREREG.md`. The")
w("drafted diff names v30 line numbers; the applied file has moved 976 lines since, so the")
w("recorded number is used only to cross-check what was found.")
w("")
for h in hunks:
    w("---")
    w("")
    w("## %s — %s" % (h["id"], h["title"]))
    w("")
    w("**Anchor**, drafted against v30 l.%d, located at applied **l.%d**, match count **1**:"
      % (h["v30_line"], h["applied_line"]))
    w("")
    w("```")
    w(h["anchor"])
    w("```")
    w("")
    w("**Replace with (%d lines), verbatim from `PREREG_v30a_DIFF.md` %s:**"
      % (len(h["replacement"]), h["id"]))
    w("")
    w("```")
    for l in h["replacement"]:
        w(l)
    w("```")
    w("")
OUT.write_text("\n".join(buf) + "\n", encoding="utf-8")
print()
print("wrote %s (%d lines) -- a PROPOSAL. Nothing applied." % (OUT, len(buf)))
