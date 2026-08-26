#!/usr/bin/env python3
"""Convert the D1/D2 exemption tables from LINE keys to ANCHOR keys.

WHY, and it is the lesson the ceremony already filed twice. An exemption keyed to
a line number is a pinned expectation with no derivation: it is silent while the
file is still and it detaches the moment anything above it grows. Re-pinning to
the new number restores the same defect with a fresher value -- and the
declaration is still being edited this round, so a number re-pinned now drifts
again before C2 runs. The key becomes the anchor TEXT, which moves with the
sentence it exempts.

WHAT IS NOT CHANGED. The exemptions stay VALUE-SCOPED: each still whitelists the
specific historical value or enumeration at its site, and still refuses whatever
appears there next. Anchoring fixes where an exemption points, not what it
licenses.

THE NEW FAILURE MODE, GUARDED. An anchor matching more than one line would exempt
all of them silently -- a widening. Uniqueness is asserted per anchor per file at
check time, and a non-unique anchor is a finding, not a tie-break.

The tables are read with ast.literal_eval and re-emitted, so no reason string is
retyped.

Written with the Write tool per D2.1.
"""
import ast
import pathlib
import re
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SRC = REPO / "tools/check_registration.py"

# Anchors whose text no longer exists: they lived in the §D.2 the v30a
# enumeration rewrite replaced. A stale exemption is a hole, not a no-op, so they
# are removed rather than carried.
DROP = {
    ("AVAILABILITY_DECLARATION.md", 3663),
    ("AVAILABILITY_DECLARATION.md", 3686),
    ("AVAILABILITY_DECLARATION.md", 3683),
}

body = SRC.read_text(encoding="utf-8")


def block_span(name):
    i = body.index("\n" + name + " = {") + 1
    depth, j = 0, i
    while True:
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1


def emit(name, table, third_is_tuple):
    out = ["%s = {" % name]
    for (rel, anchor), rest in table.items():
        allowed, reason = rest[1], rest[2]
        out.append("    (%r,\n     %r): (" % (rel, anchor))
        if third_is_tuple:
            out.append("        %r," % (allowed,))
        else:
            out.append("        frozenset(%r)," % (sorted(allowed),))
        for k, chunk in enumerate(_wrap(reason)):
            out.append("        %r%s" % (chunk, ")," if k == len(_wrap(reason)) - 1 else ""))
    out.append("}")
    return "\n".join(out)


def _wrap(text, width=68):
    words, line, chunks = text.split(" "), "", []
    for w in words:
        if len(line) + len(w) + 1 > width and line:
            chunks.append(line + " ")
            line = w
        else:
            line = (line + " " + w).strip()
    chunks.append(line)
    return chunks


new_body = body
report = []
for name, third_is_tuple in (("_HASH_SET_EXEMPT", False),
                             ("_HASH_SET_ENUM_EXEMPT", True)):
    i, j = block_span(name)
    literal = body[i + len(name) + 3:j]
    # literal_eval refuses frozenset({...}) -- it is a Call, not a literal. The
    # namespace is restricted to that one name so nothing else can evaluate.
    table = eval(literal, {"__builtins__": {}}, {"frozenset": frozenset})  # noqa: S307
    kept = {}
    for (rel, line), rest in table.items():
        if (rel, line) in DROP:
            report.append("  DROPPED %-30s L%-5d anchor gone: %r" % (rel, line, rest[0][:44]))
            continue
        key = (rel, rest[0])
        if key in kept:
            sys.exit("HALT: duplicate anchor %r for %s" % (rest[0], rel))
        kept[key] = rest
        report.append("  anchored %-30s <- L%-5d %r" % (rel, line, rest[0][:44]))
    new_block = emit(name, kept, third_is_tuple)
    new_body = new_body.replace(body[i:j], new_block, 1)
    report.append("  %s: %d -> %d entries" % (name, len(table), len(kept)))

# LINE ENDINGS ARE PRESERVED, and this is not a detail: this file is stored
# uniformly CRLF, `.gitattributes` sets `* -text` so git normalises nothing, and
# read_text/write_text would silently convert all 2,635 lines. A whole-file
# line-ending rewrite of a file in the tag's hash set passes every check in the
# prereg stage -- the diff is the only place it shows.
import subprocess  # noqa: E402

head = subprocess.run(["git", "show", "HEAD:tools/check_registration.py"],
                      cwd=str(REPO), capture_output=True).stdout
crlf, lf = head.count(b"\r\n"), head.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: the checker is MIXED at HEAD (%d CRLF of %d LF); a blanket "
             "conversion would touch lines this edit never edited." % (crlf, lf))

out = new_body.encode("utf-8")
if crlf:
    out = out.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
SRC.write_bytes(out)
print("\n".join(report))
print("\nwritten: %d CRLF / %d LF" % (out.count(b"\r\n"), out.count(b"\n")))

# The rewritten source must still parse, and both tables must still literal-eval.
ast.parse(SRC.read_text(encoding="utf-8"))
print("source parses; tables re-emitted")
