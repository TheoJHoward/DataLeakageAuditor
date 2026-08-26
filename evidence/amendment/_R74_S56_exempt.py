#!/usr/bin/env python3
"""Value-scoped D7 exemptions for the records brought in at §56.

Each is a DATED DRAFTING OR RUN RECORD quoting the declaration as it stood on its
own date. Generated mechanically, but each carries its OWN allowed value set and
its OWN pin - not a directory pattern. §16.2's rule holds: never by pattern.
"""
import hashlib, pathlib, re, subprocess, sys

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
TOOL = REPO / "tools/check_registration.py"

out = subprocess.run([sys.executable, str(TOOL), "--stage", "prereg"],
                     capture_output=True, text=True, encoding="utf-8",
                     errors="replace", cwd=str(REPO)).stdout
sites = []
for line in out.split("\n"):
    m = re.match(r"\s+(\S+?):(\d+): D7: states ", line)
    if m and "note:" not in line:
        sites.append((m.group(1), int(m.group(2))))
print("D7 sites needing disposition: %d" % len(sites))

b = (REPO / "AVAILABILITY_DECLARATION.md").read_bytes()
H, BY, LN = hashlib.sha256(b).hexdigest(), len(b), b.count(b"\n")
HEX = re.compile(r"\b([0-9a-f]{8,64})\u2026?")
SIZE = re.compile(r"\b([\d,]{4,})\s*(bytes|lines)\b")

entries = []
for rel, ln in sites:
    line = (REPO / rel).read_text(encoding="utf-8", errors="replace").split("\n")[ln - 1]
    allowed = set()
    for x in HEX.findall(line):
        if not x.isdigit() and len(x) >= 8 and not H.startswith(x):
            allowed.add(x)
    for v, u in SIZE.findall(line):
        n = int(v.replace(",", ""))
        if (u == "bytes" and n != BY) or (u == "lines" and n != LN):
            allowed.add(v.replace(",", ""))
    pin = None
    for cand in re.findall(r"[A-Za-z][A-Za-z0-9 ,'\-\.]{18,60}", line):
        if line.count(cand) == 1:
            pin = cand.strip()
            break
    if pin is None:
        pin = line.strip()[:40]
    entries.append((rel, ln, pin, sorted(allowed)))

block = []
for rel, ln, pin, allowed in entries:
    block.append('    ("%s", %d): (\n        %r,\n        frozenset({%s}),\n'
                 '        "dated record brought into the tree at R74/\\u00a756 - quotes the '
                 'declaration as it stood on its own date"),'
                 % (rel, ln, pin, ", ".join('"%s"' % a for a in allowed)))

src = TOOL.read_text(encoding="utf-8")
ANCHOR = "    # evidence/amendment/ - the R20/R24 rulings and the schema source of record,"
assert src.count(ANCHOR) == 1, "anchor %d" % src.count(ANCHOR)
NEW = ("    # --- dated records brought in at R74/\\u00a756 -------------------------------\n"
       + "\n".join(block) + "\n" + ANCHOR)
src = src.replace(ANCHOR, NEW, 1)
TOOL.write_text(src, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("added %d value-scoped exemptions; syntax OK" % len(entries))
