"""A34's §2.2 sweep -- prose that describes §AB, §AC or SC-12(w)'s limb as absent,
unapproved, or elsewhere. READ-ONLY. Reports the list; edits nothing.

R143 §1.3: a fix can falsify the note that described the defect. A30's provenance
note was TRUE until hunk 3 landed; then every clause of it was false. The same
hazard applies to any other prose written while these three blocks were absent,
so the sweep is run over the whole tree rather than the two places already known.

WHY THE PATTERNS ARE PAIRED, NOT SINGLE. Searching for "§AB" alone returns every
mention including the correct ones; searching for "not applied" alone returns
every unrelated use. A hit requires a SUBJECT (one of the three blocks, or the
container that was never created) AND an ABSENCE CLAIM on the same line. That
still over-collects -- deliberately. A sweep that under-collects hands back a
false all-clear, and every hit here is read by a human before anything is edited.

FENCE STATE IS TRACKED. A hit inside a fenced code block is drafting apparatus or
a quoted specimen, not operative prose, and is labelled as such -- the same
distinction that turned a five-citation count back into four.

    usage: a34_sweep.py
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

SUBJECTS = (
    ("§AB", re.compile(r"§AB|amendments block|amendments-block")),
    ("§AC", re.compile(r"§AC|disclosures block")),
    ("limb", re.compile(r"SC-12\(w\)|\(w1\)|waived.{0,20}entry condition", re.I)),
)
ABSENCE = re.compile(
    r"not in this file|never applied|not applied|drafted, not applied"
    r"|never offered|not offered for approval|does not exist|will not exist"
    r"|is absent|not yet applied|unapproved|not an approved|stops short"
    r"|in `?SCHEMA_SET_FINAL|lives outside|elsewhere", re.I)

# The instrument excludes itself and its own siblings: this script, the sweep's
# report, and the A33b/A34 documents ABOUT the defect necessarily quote the very
# phrases being hunted. Including them would inflate the count with the
# instrument's own text -- the population must exclude the instrument.
SELF = ("a34_sweep.py", "A33B_SUPERSEDING_PRESENTATION.md", "a33b_present.py",
        "a33b_divergence.py", "a33c_manifest_offset.py", "a33d_block_completeness.py",
        "A35_DISCLOSURE_DRAFT.md", "a33_apply.py", "a32_assemble.py")

SKIP_DIRS = {".git", "__pycache__", ".claude"}

hits = []
scanned = 0
for p in sorted(REPO.rglob("*.md")):
    if any(d in p.parts for d in SKIP_DIRS) or p.name in SELF:
        continue
    scanned += 1
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").split("\n")
    except OSError:
        continue
    # MATCHED OVER PARAGRAPHS, NOT LINES. A first version tested each line for
    # both a subject and an absence claim and returned ZERO hits in every
    # registered object -- a false all-clear, because the known hit spans a line
    # break: PREREG.md l.1533 carries "SC-12(w)'s limb" and l.1534 carries "not
    # in this file". Neither line holds both. Prose wraps; a line is not a unit
    # of meaning, and an instrument that assumes it is will report silence.
    units, cur, start, infence = [], [], 1, False
    for n, l in enumerate(lines, 1):
        if l.lstrip().startswith("```"):
            infence = not infence
            if cur:
                units.append((start, "\n".join(cur), not infence))
                cur = []
            continue
        if not l.strip():
            if cur:
                units.append((start, "\n".join(cur), infence))
                cur = []
            continue
        if not cur:
            start = n
        cur.append(l)
    if cur:
        units.append((start, "\n".join(cur), infence))

    for n, text, fence in units:
        if not ABSENCE.search(text):
            continue
        for name, pat in SUBJECTS:
            if pat.search(text):
                flat = " ".join(text.split())
                hits.append((p.relative_to(REPO).as_posix(), n, name, fence, flat))
                break

print("scanned %d markdown file(s); the instrument and its siblings excluded (%d names)"
      % (scanned, len(SELF)))
print("hits: %d  (%d operative, %d inside a fence)"
      % (len(hits), sum(1 for h in hits if not h[3]), sum(1 for h in hits if h[3])))
print()

REGISTERED = {"PREREG.md", "README.md", "DESIGN.md", "HISTORY.md", "DEVIATIONS.md",
              "AVAILABILITY_DECLARATION.md"}

for tier, want in (("REGISTERED OBJECTS -- these are the ones that matter", True),
                   ("supporting artifacts -- context, not registered text", False)):
    group = [h for h in hits if (h[0] in REGISTERED) == want]
    print("=" * 78)
    print("=== %s === (%d)" % (tier, len(group)))
    for path, n, subj, fence, text in group:
        print("  %-34s l.%-5d [%s]%s" % (path, n, subj, "  IN FENCE" if fence else ""))
        print("      %s" % text[:150])
print()
print("NOTHING EDITED. R143 §3 requires this list be reported before any of it is "
      "changed; each hit needs a human decision on whether it is now false.")
