#!/usr/bin/env python3
"""A5.4 — restate the enumeration exemptions against the grown FILES set.

Each reported site is matched to its table entry the same way the checker
resolves it: by which ANCHOR sits on that line of that file. Matching by the
recorded tuple was tried first and refused itself, correctly -- one tuple occurs
more than once in the source and the replacement would have been a guess.

The new enumerations come from the check's own output. None of the four sites
changed a byte; the reference set grew, so more of what they already said became
recognisable as set members.

Written with the Write tool per D2.1.
"""
import ast
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
SRC = REPO / "tools/check_registration.py"
body = SRC.read_text(encoding="utf-8")

NAME = "_HASH_SET_ENUM_EXEMPT"
i = body.index(NAME + " = {")
depth, j = 0, i
while True:
    if body[j] == "{":
        depth += 1
    elif body[j] == "}":
        depth -= 1
        if depth == 0:
            break
    j += 1
table = eval(body[i + len(NAME) + 3:j + 1], {"__builtins__": {}}, {})  # noqa: S307

run = subprocess.run([sys.executable, "tools/check_registration.py", "--stage", "prereg"],
                     cwd=str(REPO), capture_output=True, text=True,
                     encoding="utf-8", errors="replace")
flat = " ".join((run.stdout + run.stderr).split())
PAT = re.compile(r"(\S+?):(\d+): D6: this site is exempt for the enumeration "
                 r"(\[[^\]]*\]), but it now enumerates (\[[^\]]*\])")
hits = PAT.findall(flat)
if not hits:
    sys.exit("HALT: no D6 enumeration mismatches parsed")

updates = {}
for rel, lineno, old_lit, new_lit in hits:
    src = REPO / rel
    line = src.read_text(encoding="utf-8", errors="replace").replace(
        "\r\n", "\n").split("\n")[int(lineno) - 1]
    keys = [k for k in table if k[0] == rel and k[1] in line]
    if len(keys) != 1:
        sys.exit("HALT: %s:%s -- %d anchors match that line, expected 1"
                 % (rel, lineno, len(keys)))
    key = keys[0]
    old_t, new_t = tuple(ast.literal_eval(old_lit)), tuple(ast.literal_eval(new_lit))
    if tuple(table[key][0]) != old_t:
        sys.exit("HALT: %s:%s -- the entry's recorded enumeration is not what the "
                 "check reported as exempt" % (rel, lineno))
    updates[key] = (new_t, table[key][1], len(old_t), len(new_t))

for key, (new_t, reason, a, b) in updates.items():
    table[key] = (new_t, reason)


def wrap(text, width=68):
    words, line, out = text.split(" "), "", []
    for w in words:
        if len(line) + len(w) + 1 > width and line:
            out.append(line + " ")
            line = w
        else:
            line = (line + " " + w).strip()
    out.append(line)
    return out


emit = [NAME + " = {"]
for (rel, anchor), (enum, reason) in table.items():
    emit.append("    (%r,\n     %r): (" % (rel, anchor))
    emit.append("        %r," % (tuple(enum),))
    chunks = wrap(reason)
    for k, c in enumerate(chunks):
        emit.append("        %r%s" % (c, ")," if k == len(chunks) - 1 else ""))
emit.append("}")
body = body[:i] + "\n".join(emit) + body[j + 1:]

head = subprocess.run(["git", "show", "HEAD:tools/check_registration.py"],
                      cwd=str(REPO), capture_output=True).stdout
crlf, lf = head.count(b"\r\n"), head.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: checker is MIXED at HEAD")
data = body.encode("utf-8")
if crlf:
    data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
SRC.write_bytes(data)
ast.parse(SRC.read_text(encoding="utf-8"))

for (rel, anchor), (_n, _r, a, b) in updates.items():
    print("restated  %-34s %d -> %d paths" % (rel, a, b))
print("%d entries; %d CRLF / %d LF; parses"
      % (len(table), data.count(b"\r\n"), data.count(b"\n")))
