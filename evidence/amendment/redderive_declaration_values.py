#!/usr/bin/env python3
"""RE-DERIVE every recorded copy of the declaration's hash/size, in one pass.

Run this after ANY edit to AVAILABILITY_DECLARATION.md. R15's no-carry-forward
rule binds these exactly as it binds the six tag hashes: every value below is
computed here, never copied.

Covers: the f4 pointer's current block, the `../AVAILABILITY_DECLARATION.md`
manifest line, and the ceremony package's three recorded copies. Then re-derives
every stale manifest line so the tree verifies.

This exists because the cascade recurred on every declaration edit and was being
done by hand each time, which is how the values drifted in the first place.
"""
import hashlib, pathlib, re, sys

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"
b = DECL.read_bytes()
H = hashlib.sha256(b).hexdigest()
BYTES, LINES = len(b), b.count(b"\n")
print("declaration: %s / %d bytes / %d lines" % (H[:16], BYTES, LINES))

changed = []

# ---- 1. the f4 pointer's current block -----------------------------------
P = REPO / "evidence/fixture_spike/f4/DECLARATION_POINTER.md"
s = P.read_text(encoding="utf-8")
s2 = re.sub(r"^    sha256: [0-9a-f]{64}$", "    sha256: " + H, s, count=1, flags=re.M)
s2 = re.sub(r"^    bytes:  \d+$", "    bytes:  %d" % BYTES, s2, count=1, flags=re.M)
if s2 != s:
    P.write_text(s2, encoding="utf-8"); changed.append("f4/DECLARATION_POINTER.md")

# ---- 2. the ceremony package's recorded copies ---------------------------
def swap(rel, pattern, repl):
    p = REPO / rel
    t = p.read_text(encoding="utf-8")
    t2 = re.sub(pattern, repl, t, count=1)
    if t2 != t:
        p.write_text(t2, encoding="utf-8"); changed.append(rel)

swap("evidence/ceremony/CEREMONY_COMMANDS.md",
     r"As at R\d+: `[0-9a-f]{8}\u2026`, [\d,]+ bytes",
     "As at R69: `%s\u2026`, %s bytes" % (H[:8], format(BYTES, ",")))
swap("evidence/ceremony/COMMIT_PLAN.md",
     r"as at R\d+: sha256\n`[0-9a-f]{64}`, \*\*[\d,]+ bytes\*\*, \*\*[\d,]+ lines\*\*",
     "as at R69: sha256\n`%s`, **%s bytes**, **%s lines**"
     % (H, format(BYTES, ","), format(LINES, ",")))
swap("evidence/ceremony/COMMIT_PLAN.md",
     r"as at R\d+: sha256 `[0-9a-f]{64}`, \*\*[\d,]+ bytes\*\*, \*\*[\d,]+ lines\*\*",
     "as at R69: sha256 `%s`, **%s bytes**, **%s lines**"
     % (H, format(BYTES, ","), format(LINES, ",")))
swap("evidence/ceremony/DEVIATIONS_DRAFT.md",
     r"as at R\d+: sha256 `[0-9a-f]{64}`,\n[\d,]+ bytes, [\d,]+ lines",
     "as at R69: sha256 `%s`,\n%s bytes, %s lines"
     % (H, format(BYTES, ","), format(LINES, ",")))

# ---- 3. every stale manifest line, LF preserved ---------------------------
mp = REPO / "evidence/MANIFEST.sha256"
lines = mp.read_bytes().decode("utf-8").split("\n")
n = 0
for i, l in enumerate(lines):
    m = re.match(r"^([0-9a-f]{64})  (.+)$", l)
    if not m:
        continue
    target = (REPO / "evidence" / m.group(2)).resolve()
    if not target.exists():
        continue
    new = hashlib.sha256(target.read_bytes()).hexdigest()
    if new != m.group(1):
        lines[i] = "%s  %s" % (new, m.group(2)); n += 1
mp.write_bytes("\n".join(lines).encode("utf-8"))
raw = mp.read_bytes()
assert raw.count(b"\r\n") == 0, "manifest must stay LF"

print("re-derived text sites: %s" % (", ".join(changed) or "none"))
print("re-derived manifest lines: %d   (LF preserved)" % n)
