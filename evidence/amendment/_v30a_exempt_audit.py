#!/usr/bin/env python3
"""Audit every line-keyed exemption before converting it to an anchor.

THE CHECK THAT MATTERS, and it is not "does the gate pass afterwards". A gate
that passes after a re-pin proves the COUNT matches at the new line; it does not
prove each exemption still covers the sentence it was written for. So, per
exemption:

    pre  = the line at the recorded number in HEAD's copy of the file
    post = the line the anchor text now selects in the working copy

and `pre` must equal `post`. Anything else is reported rather than repaired
silently: an exemption whose target changed is a different exemption.

Ambiguity is a finding, not a tie-break. An anchor matching more than one line
would exempt all of them, which widens the exemption without saying so.

Written with the Write tool per D2.1.
"""
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SRC = REPO / "tools/check_registration.py"

body = SRC.read_text(encoding="utf-8")


def table(name):
    """Extract (rel, line, pin) triples from a table literal by parsing the
    source, so this audit reads the same bytes the checker does."""
    i = body.index(name + " = {")
    depth, j = 0, i
    while True:
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    block = body[i:j + 1]
    out = []
    for m in re.finditer(r'\(\s*"([^"]+)",\s*(\d+)\s*\):\s*\(\s*\n?\s*"((?:[^"\\]|\\.)*)"',
                         block):
        out.append((m.group(1), int(m.group(2)), m.group(3).encode().decode("unicode_escape")))
    return out


def head_lines(rel):
    r = subprocess.run(["git", "show", "HEAD:" + rel], cwd=str(REPO),
                       capture_output=True)
    return r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")


bad = 0
for name in ("_HASH_SET_EXEMPT", "_HASH_SET_ENUM_EXEMPT"):
    rows = table(name)
    print("==== %s : %d entries parsed ====" % (name, len(rows)))
    for rel, line, pin in rows:
        hl = head_lines(rel)
        pre = hl[line - 1] if 0 < line <= len(hl) else "<<past EOF>>"
        cur = (REPO / rel).read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
        hits = [(i + 1, l) for i, l in enumerate(cur) if pin in l]

        status = []
        if pin not in pre:
            status.append("PIN NOT ON THE RECORDED LINE AT HEAD")
        if not hits:
            status.append("ANCHOR GONE from the working copy")
        elif len(hits) > 1:
            status.append("AMBIGUOUS: %d lines match" % len(hits))
        elif hits[0][1] != pre:
            status.append("CONTENT CHANGED: pre != post")

        flag = "  <-- " + " | ".join(status) if status else "  ok"
        if status:
            bad += 1
        print("  %-30s L%-5d %-46r %s"
              % (rel, line, pin[:44], flag))
        if status and hits:
            print("        now at line %d" % hits[0][0])
            if hits[0][1] != pre:
                print("        pre : %s" % pre[:110])
                print("        post: %s" % hits[0][1][:110])

print("\nentries needing attention: %d" % bad)
sys.exit(0)
