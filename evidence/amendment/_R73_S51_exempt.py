#!/usr/bin/env python3
"""§51 follow-up: the amendment records brought into evidence/ are DATED DRAFTING
RECORDS. They quote the declaration's hash and size as they were on the day each
was written. They are exempted, never updated - rewriting a drafting record to
match today's file would falsify the record (R13)."""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

ANCHOR = '    ("evidence/author_review/READ_THROUGH_PACKAGE.md", 1): ('
NEW = '''    # evidence/amendment/ - the R20/R24 rulings and the schema source of record,
    # brought inside the signed tree at R73/§51. Each quotes the declaration as it
    # stood on its own date. Dated records are exempted, NEVER updated: rewriting
    # one to match today's file would falsify the drafting record (R13).
    ("evidence/amendment/DECLARATION_SCRUB_LIST.md", 353): (
        "`AVAILABILITY_DECLARATION.md` (277,411 b",
        frozenset({"277411"}),
        "dated drafting record - the 138-row scrub list, written against the "
        "declaration as it stood that day"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 13): (
        "`AVAILABILITY_DECLARATION.md` `f0829bd3",
        frozenset({"3684", "f0829bd3"}),
        "dated drafting record - SCHEMA_SET_FINAL's own read-state block"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 14): (
        "`30d3ad4c",
        frozenset({"30d3ad4c"}),
        "dated drafting record - this is tools/check_registration.py's hash, on a "
        "line that also names the declaration"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 34): (
        "**Read state this pass.**",
        frozenset({"1099", "3684"}),
        "dated drafting record - line counts as read that pass"),
    ("evidence/amendment/SCHEMA_SET_FINAL.md", 2111): (
        "| `applied",
        frozenset({"1290186ed970df65968b5b979aa696e4dca4678e7b46fae40587c4948b8b1c30"}),
        "dated drafting record - the scrub's declared base, pinned deliberately"),
'''
assert s.count(ANCHOR) == 1, "anchor %d" % s.count(ANCHOR)
s = s.replace(ANCHOR, NEW + ANCHOR, 1)

# the §49 insertion shifted CEREMONY_COMMANDS: FILES= 180->203, exemption 239->262
for old, new in ((180, 203), (239, 262)):
    a = '("evidence/ceremony/CEREMONY_COMMANDS.md", %d' % old
    b = '("evidence/ceremony/CEREMONY_COMMANDS.md", %d' % new
    assert s.count(a) == 1, "reanchor %d: %d" % (old, s.count(a))
    s = s.replace(a, b, 1)
    print("  re-anchored CEREMONY_COMMANDS %d -> %d" % (old, new))

TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D7 exemptions added for evidence/amendment/; syntax OK")
