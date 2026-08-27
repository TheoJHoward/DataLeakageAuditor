"""A27 -- DERIVE the tag message's change list. R140 A27, branch 1.

THE COUPLING FIX. §3.5's hash lines are derived: *"the output of C2, pasted —
never retyped, never re-derived"*, with `v30a.hashes.txt` as their authority. The
change list beside them had no such authority — it was prose, and it drifted into
naming three §6.2 changes the file did not contain. This gives it one.

DERIVED FROM THE TWO FILES, NOT FROM AN APPROVAL RECORD. R140 offers
`SCHEMA_RECORDS.json` or the approval diff. Both are now too narrow: A24
superseded two further lines under a SECOND approval, so a list built from the
first approval would be wrong in the opposite direction — it would omit the two
changes that ARE there. The ground truth is the pair of files, and it stays true
however many approvals accumulate.

    superseded  = every non-blank line of `prereg-v30:PREREG.md` absent from the
                  applied file
    section     = the nearest `### n.n` heading above it IN v30, so the list
                  names where the change is in the REGISTERED text a reader of
                  the tag would fetch

Writes `v30a.changes.txt`, the change list's authority, beside `v30a.hashes.txt`.
Untracked and regenerated at ceremony time, exactly as the hash file is.

    usage: a27_derive_changes.py <v30-file> <out.txt>
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
APPLIED = REPO / "PREREG.md"
V30 = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])


def text_of(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


v30 = text_of(V30).split("\n")
applied = set(text_of(APPLIED).split("\n"))

print("=" * 78)
print("POPULATION, DERIVED AND ASSERTED FIRST")
print("=" * 78)
print("  prereg-v30:PREREG.md : %d lines" % (len(v30) - 1))
print("  applied PREREG.md    : %d lines" % (len(text_of(APPLIED).split('\n')) - 1))

HEAD = re.compile(r"^#{2,4}\s+([0-9]+(?:\.[0-9]+)*)\s+(.*)$")


def section_of(n):
    for i in range(n - 1, -1, -1):
        m = HEAD.match(v30[i])
        if m:
            return m.group(1), m.group(2).strip()
    return None, None


gone = [(i, l) for i, l in enumerate(v30, 1) if l.strip() and l not in applied]
print("  registered lines superseded: %d" % len(gone))
if not gone:
    sys.exit("HALT: nothing is superseded. An empty change list is not an empty "
             "amendment; the files are not what this deriver expects.")

# NO SUMMARISATION. A first version named each change by its first bolded
# phrase, which truncated §10.1's mid-word ("...and is silent on fi") and reduced
# §10.2's to an arrow. A hand-summary -- even a generated one -- is a second
# description of text that already exists, and it drifts from the text the
# moment either moves. The list names the SURFACE: section, its own heading
# title, and the registered line. A reader who wants the sentence fetches it
# with `git show prereg-v30:PREREG.md`, which the message already tells them.
rows = []
for n, line in gone:
    sec, title = section_of(n)
    if sec is None:
        sys.exit("HALT: v30 line %d sits under no numbered heading; the list "
                 "cannot name its surface." % n)
    rows.append({"line": n, "section": sec, "title": title})

print()
print("=" * 78)
print("DERIVED CHANGE LIST")
print("=" * 78)
by_sec = {}
for r in rows:
    by_sec.setdefault(r["section"], []).append(r)
for sec in sorted(by_sec, key=lambda s: [int(x) for x in s.split(".")]):
    for r in by_sec[sec]:
        print("  §%-6s l.%-5d %s" % (sec, r["line"], (r["title"] or "")[:66]))

parts = []
for sec in sorted(by_sec, key=lambda s: [int(x) for x in s.split(".")]):
    lines_ = ", ".join("line %d" % r["line"] for r in by_sec[sec])
    title = by_sec[sec][0]["title"] or ""
    # A COLON, NOT AN EM-DASH. §10.1's own heading is "Phase 0 kill gate —
    # objective", so an em-dash separator produced "…kill gate — objective —
    # line 1022" and a reader cannot tell which dash divides what.
    parts.append("§%s %s: %s" % (sec, title, lines_))

body = ("Amends PREREG.md: " + "; ".join(parts) + ".\n")
OUT.write_text(body, encoding="utf-8")
print()
print("=" * 78)
print("WRITTEN to %s" % OUT.name)
print("=" * 78)
import textwrap                                                 # noqa: E402
print(textwrap.fill(body.strip(), 92, initial_indent="  ", subsequent_indent="  "))
print()
print("  %d superseded line(s) across %d section(s). No numeral is stated: the"
      % (len(rows), len(by_sec)))
print("  count is read from the enumeration, as §11 item 8 requires of the hash set.")
