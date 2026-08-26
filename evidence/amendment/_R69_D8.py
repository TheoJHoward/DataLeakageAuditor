#!/usr/bin/env python3
"""B3.3 — D8: a line-pinned citation must still resolve to expected content."""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

D8 = '''
# ---------------------------------------------------------------------------
# D8 (R69/B3.3) - line-pinned citations must still resolve.
#
# §17.2 preferred anchors over line numbers, and most citations were converted.
# A few must stay line-pinned because their target has no heading: `FILES=` is a
# shell assignment, not a section. Those are registered here with the text that
# must be ON that line.
#
# The failure this prevents is specific and worse than a dead link: `l.1516` was
# cited in three files as the §A.11 walk summary and, after the declaration grew,
# resolved to "What this subsection does NOT do." A reader following it lands on
# real prose and has no way to know they are in the wrong place. A dead link
# announces itself; a drifted one does not.
# ---------------------------------------------------------------------------

# (target file, line, text that must be on it, who cites it)
_LINE_PINNED_CITATIONS = (
    ("evidence/ceremony/CEREMONY_COMMANDS.md", 180, 'FILES="PREREG.md',
     "COMMIT_PLAN.md \\u00a76 and DEVIATIONS_DRAFT.md cite \\u00a73.2 l.180 as the authority "
     "for the hash set; the target is a shell assignment and has no heading"),
    ("HISTORY.md", 271, "### H-34",
     "COMMIT_PLAN.md \\u00a73 cites the H-34 heading and its sha256 quotation"),
    ("HISTORY.md", 219, "13. *(12 Aug 2026)*",
     "COMMIT_PLAN.md cites H-L13 by line; the lesson list is numbered, not headed"),
    ("HISTORY.md", 218, "12. *(12 Aug 2026)*",
     "DEVIATIONS_DRAFT.md cites H-L12 by line for the date convention"),
    ("DESIGN.md", 546, "review-lesson",
     "COMMIT_PLAN.md cites DESIGN.md l.546 as the cross-reference H-L13 de-fragilised"),
    ("AVAILABILITY_DECLARATION.md", 3936, "R8. H-entry",
     "the decision-log tail is one block with no per-entry heading"),
)


def check_line_citations(root: Path) -> list[Finding]:
    """D8 - every registered line-pinned citation still resolves."""
    findings: list[Finding] = []
    for rel, lineno, expect, why in _LINE_PINNED_CITATIONS:
        path = root / rel
        if not path.exists():
            findings.append(Finding("line_citations", rel, lineno,
                                    "D8: cited file is missing"))
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").split("\\n")
        if lineno > len(lines):
            findings.append(Finding(
                "line_citations", rel, lineno,
                "D8: citation points past the end of the file (%d lines). %s"
                % (len(lines), why)))
            continue
        actual = lines[lineno - 1]
        if expect in actual:
            findings.append(Finding("line_citations", rel, lineno,
                                    "D8: resolves - %r" % expect, is_note=True))
            continue
        hits = [i for i, l in enumerate(lines, 1) if expect in l]
        moved = (" It is now at line %d." % hits[0] if len(hits) == 1
                 else " It now appears on lines %r." % (hits,) if hits
                 else " It is gone from the file.")
        findings.append(Finding(
            "line_citations", rel, lineno,
            "D8: this line no longer contains %r - it reads %r instead.%s "
            "A drifted citation resolves to plausible content and does not "
            "announce itself. Cited because: %s"
            % (expect, actual.strip()[:60], moved, why)))
    return findings

'''

ANCHOR = "def check_phase_arithmetic(root: Path) -> list[Finding]:"
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, D8.lstrip("\n") + "\n" + ANCHOR, 1)

REG = '    ("prereg", "declaration_values", check_declaration_values),\n'
assert s.count(REG) == 1
s = s.replace(REG, REG + '    ("prereg", "line_citations", check_line_citations),\n', 1)

TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D8 installed and registered; syntax OK")
