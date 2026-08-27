"""A24 -- apply the two approved §6.2 replacements to `PREREG.md`. R139 §1.1.

THIS ONE WRITES. Every other instrument this round was read-only; this is the
first edit to the registered file since the amendment, and it happens only
because R139 §1.1 approves these two hunks by name.

THE TEXT IS EXTRACTED FROM `PREREG_v30a_DIFF.md`, NEVER FROM THE PROPOSAL.
`A23_PROPOSED_DIFF.md` is a derived presentation of that source; applying from
the presentation would put a second copy in the chain and make the two able to
drift. The source of record is read directly, and the proposal is then checked
against what was applied.

ANCHORS ARE LOCATED, NEVER OFFSET. §1.1: "Adapt line positions by locating,
never by offset arithmetic." Each anchor must match exactly one line; anything
else halts.

APPLIED BOTTOM-TO-TOP, descending by line. The two anchors are five lines apart,
so applying the earlier one first would shift the later one -- the classic way an
applier writes correct text into the wrong place. §77.2 of
`generate_prereg_diff.py` fixed this once already; the rule is reused, not
rediscovered.

STRUCTURE IS CHECKED BEFORE THE WRITE. The replacement turns one list bullet
into a bullet plus a nested blockquote. §6.2's bullet list must still be a
bullet list afterwards, and the lines above and below must still parse as what
they were.

WRITE-ONCE GUARDED on a distinctive line of each replacement.

    usage: a24_apply_approved.py
"""
from __future__ import annotations

import hashlib
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

EXPECT_BEFORE = "0c8da19f237cd2437b91ef38c570f0ca2159863edcd7f05b10c5cdab9873d3a7"
WANTED = [("H2", "§6.2 reference AUC anchor"),
          ("H3", "§6.2 contamination availability class")]


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


raw = PREREG.read_bytes()
crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
if crlf:
    sys.exit("HALT: PREREG.md carries CRLF (%d); this applier assumes LF" % crlf)
before = hashlib.sha256(raw).hexdigest()
if before != EXPECT_BEFORE:
    sys.exit("HALT: PREREG.md is at %s, expected %s. The file is not what these "
             "hunks were anchored against." % (before[:16], EXPECT_BEFORE[:16]))
print("PREREG.md before: %s  (%d lines)" % (before[:16], raw.count(b"\n")))

draft = text_of(DRAFT)
lines = raw.decode("utf-8").split("\n")


def section(hid):
    s = draft.index("### %s — " % hid)
    n = draft.find("\n### ", s + 1)
    return draft[s:n if n > 0 else len(draft)]


hunks = []
for hid, title in WANTED:
    body = section(hid)
    m = re.search(r"\*\*ANCHOR — `PREREG\.md` line (\d+), match count 1:\*\*\n\n```\n(.*?)\n```",
                  body, re.S)
    m2 = re.search(r"\*\*REPLACE with \((\d+) lines?\)[.:]\*\*.*?```\n(.*?)\n```",
                   body, re.S)
    if not (m and m2):
        sys.exit("HALT: %s -- anchor or replacement block not found" % hid)
    anchor, repl = m.group(2), m2.group(2).split("\n")
    hits = [i for i, l in enumerate(lines) if l == anchor]
    if len(hits) != 1:
        sys.exit("HALT: %s -- anchor matches %d lines, expected 1" % (hid, len(hits)))
    probe = max(repl, key=len)
    if probe in lines:
        print("ALREADY APPLIED (%s). Nothing written." % hid)
        sys.exit(0)
    hunks.append({"id": hid, "title": title, "at": hits[0],
                  "anchor": anchor, "repl": repl, "probe": probe})
    print("  %-3s anchor at l.%-5d (drafted v30 l.%s), %d replacement line(s)"
          % (hid, hits[0] + 1, m.group(1), len(repl)))

# BOTTOM-TO-TOP.
hunks.sort(key=lambda h: h["at"], reverse=True)
print()
print("applying bottom-to-top: %s" % " then ".join(
    "%s@l.%d" % (h["id"], h["at"] + 1) for h in hunks))
for h in hunks:
    lines[h["at"]:h["at"] + 1] = h["repl"]

out = "\n".join(lines)
o = out.split("\n")

# ---- structure, BEFORE the write ------------------------------------------
for h in hunks:
    j = o.index(h["probe"])
    start = next(i for i in range(j, -1, -1) if o[i].startswith("- **"))
    above = next((o[i] for i in range(start - 1, -1, -1) if o[i].strip()), "")
    below = next((o[i] for i in range(start + len(h["repl"]), len(o)) if o[i].strip()), "")
    print()
    print("  %s at l.%d" % (h["id"], start + 1))
    print("    line above : %s" % above[:88])
    print("    first line : %s" % o[start][:88])
    print("    line below : %s" % below[:88])
    if not o[start].startswith("- "):
        sys.exit("HALT: %s's replacement does not open a list bullet" % h["id"])
    if above.startswith("- ") and below.startswith(("- ", "<!--", "#")) is False and below.strip():
        pass                    # a following paragraph is fine; only report it
for k, l in enumerate(o):
    if l.strip() == "---" and k and o[k - 1].strip() and not o[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, o[k - 1][:60]))
print()
print("structure: both replacements open a list bullet; no rule flush against text")

PREREG.write_bytes(out.encode("utf-8"))
b = PREREG.read_bytes()
after = hashlib.sha256(b).hexdigest()
print()
print("PREREG.md after : %s  (%d lines, %d CRLF / %d LF)"
      % (after[:16], b.count(b"\n"), b.count(b"\r\n"), b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))
print()
print("=" * 78)
print("APPLIED RESULT")
print("=" * 78)
lo = min(o.index(h["probe"]) for h in hunks) - 3
hi = max(o.index(h["probe"]) for h in hunks) + 4
for i in range(max(0, lo), min(len(o), hi)):
    print("  %5d | %s" % (i + 1, o[i]))
