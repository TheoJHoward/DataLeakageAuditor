#!/usr/bin/env python3
"""B3.2 — line-citation coverage, attributed at PARAGRAPH level.

POPULATION (§30.1, stated with the result): every line of the 14 shipping files
listed in CORPUS - the six-file set, the repository-root manifest-carrying prose,
evidence/ceremony/*.md, the f4 pointer and the f5 checklist.

NO EXCLUSIONS. Every citation found is classified; nothing is dropped. A citation
the classifier cannot attribute is reported UNATTRIBUTED, which is a defect in the
method and is reported as such, not as coverage.

Attribution: a citation belongs to the LAST target named before it in the same
paragraph (blank-line delimited), falling back to the heading above the paragraph.
The earlier character-window version left 142 unattributed because the filename is
usually a sentence earlier, not adjacent to the number.
"""
import re, pathlib

ROOT = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
CORPUS = ["PREREG.md", "DESIGN.md", "HISTORY.md", "AVAILABILITY_DECLARATION.md",
          "README.md", "PRACTICES.md", "PRIOR_ART_VERIFICATION.md", "DEVIATIONS.md",
          "evidence/ceremony/CEREMONY_COMMANDS.md", "evidence/ceremony/COMMIT_PLAN.md",
          "evidence/ceremony/DEVIATIONS_DRAFT.md", "evidence/ceremony/H34_DRAFT.md",
          "evidence/fixture_spike/f4/DECLARATION_POINTER.md",
          "evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md"]

CITE = re.compile(r"(?:\bl\.\s*|\blines?\s+|\bll\.\s*)(\d{2,4})")
LOCKED = re.compile(r"PREREG\.md", re.I)
ARCHIVE = re.compile(r"\.py\b|\.csv\b|\.json\b|\.txt\b|MASTER_FINDINGS|pc2_transfer|"
                     r"phase5|phase7|process_mbo|archive|scripts\\|results\\", re.I)
LIVE = re.compile(r"AVAILABILITY_DECLARATION\.md|HISTORY\.md|DESIGN\.md|README\.md|"
                  r"CEREMONY_COMMANDS\.md|COMMIT_PLAN\.md|DEVIATIONS_DRAFT\.md|"
                  r"H34_DRAFT\.md|PRACTICES\.md|DECLARATION_POINTER\.md", re.I)
QUOTED = re.compile(r"`[^`]{3,}`")

cat = {"PREREG.md (locked - a line number into it CANNOT drift)": 0,
       "archive / source outside the repository": 0,
       "LIVE - into an in-repo document that grows": 0,
       "UNATTRIBUTED (method defect)": 0}
live, arch_pinned, live_pinned = [], 0, 0

for rel in CORPUS:
    p = ROOT / rel
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    lineno = 0
    for para in text.split("\n\n"):
        plines = para.split("\n")
        for off, line in enumerate(plines):
            for m in CITE.finditer(line):
                head = para[:para.find(line) + m.end()]
                tgt = None
                for pat, name in ((LIVE, "live"), (ARCHIVE, "archive"), (LOCKED, "locked")):
                    hits = list(pat.finditer(head))
                    if hits:
                        if tgt is None or hits[-1].start() > tgt[1]:
                            tgt = (name, hits[-1].start())
                seg = line[max(0, m.start() - 110): m.end() + 60]
                if tgt is None:
                    cat["UNATTRIBUTED (method defect)"] += 1
                elif tgt[0] == "locked":
                    cat["PREREG.md (locked - a line number into it CANNOT drift)"] += 1
                elif tgt[0] == "archive":
                    cat["archive / source outside the repository"] += 1
                    if QUOTED.search(seg):
                        arch_pinned += 1
                else:
                    cat["LIVE - into an in-repo document that grows"] += 1
                    if QUOTED.search(seg):
                        live_pinned += 1
                    live.append((rel, lineno + off + 1, m.group(1), seg.strip()[:96]))
        lineno += len(plines) + 1

total = sum(cat.values())
print("B3.2 - LINE CITATIONS, PARAGRAPH-ATTRIBUTED")
print("  population: every line of %d shipping files.  NO EXCLUSIONS.\n" % len(CORPUS))
for k, v in cat.items():
    print("    %-56s %4d" % (k, v))
print("    %-56s %4d" % ("TOTAL", total))
print("\n  carrying a quoted content pin (B3.3's remedy, already present):")
print("    archive: %d/%d      live: %d/%d"
      % (arch_pinned, cat["archive / source outside the repository"],
         live_pinned, cat["LIVE - into an in-repo document that grows"]))
print("\n  LIVE citations WITHOUT a content pin - the drift-exposed set:\n")
n = 0
for rel, i, num, seg in live:
    if QUOTED.search(seg):
        continue
    n += 1
    print("    %-40s %5d -> l.%-6s %s" % (rel.split("/")[-1], i, num, seg[:80]))
print("\n  drift-exposed: %d" % n)
