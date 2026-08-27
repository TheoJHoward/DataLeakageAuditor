"""A38 -- restore the held banking into the committed record.

`stash@{0}` carries 68 substantive lines that exist in NO committed file: the A9
all-green table, the point at which §1.6 attaches, and two recorded defects. The
committed record runs A5.3 straight into `# R134`; the held section is exactly
what belongs between them. The two are EXTENSIONS of one another, not divergent
accounts, so A38's first branch applies -- verified by
`a38_reconcile_sources.py` before this script runs.

THE STASH IS READ WITH `git show`. R144 §6 makes applying, popping or dropping it
a halt. Nothing here writes to the stash, and the backup ref stays until A15.

NOTHING IS DELETED AND NOTHING IS REWRITTEN. The held text is inserted verbatim.
A banner marks it superseded AS A VERIFICATION -- its A9 ran against a tree that
is now sixteen commits behind -- while leaving it standing AS A RECORD, because a
dated record correct as of its date is not a stale verification value. The banner
is read from a fragment authored with the file-write tool, never spelled inside
this script.

INSERTED BY ANCHOR, NEVER BY LINE NUMBER. The file grows every round; a line
number would silently target the wrong region.

    usage: a38_consolidate.py
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
REL = "evidence/session/ROUND_STATE.md"
TARGET = REPO / REL
BANNER = pathlib.Path(
    r"C:\Users\ttbea\AppData\Local\Temp\claude"
    r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
    r"\33e8c843-30fa-4bfb-aa9f-814c77bdb2e6\scratchpad\a38_banner.md")
WORK_ROOT = pathlib.Path(
    r"C:\Users\ttbea\AppData\Local\Temp\claude"
    r"\C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01"
    r"\8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1\scratchpad\ROUND_STATE.md")

HELD_START = "## A5.4 / A6 / A5.5 / A7 / A8 / A9 — THE CEREMONY PASSED"
INSERT_BEFORE = "# R134 —"
GUARD = "CONSOLIDATED 27 AUGUST 2026 FROM"

raw = TARGET.read_bytes()
crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
if crlf and crlf != lf:
    sys.exit("HALT: ROUND_STATE.md is mixed (%d CRLF / %d LF)" % (crlf, lf))
nl = "\r\n" if crlf else "\n"
print("ROUND_STATE.md before: %s  (%d lines, %s)"
      % (hashlib.sha256(raw).hexdigest()[:16], lf, "CRLF" if crlf else "LF"))

lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
if any(GUARD in l for l in lines):
    print("ALREADY APPLIED. Nothing written.")
    sys.exit(0)

r = subprocess.run(["git", "show", "stash@{0}:" + REL],
                   cwd=REPO, capture_output=True)
if r.returncode:
    sys.exit("HALT: could not read the stash: %s" % r.stderr.decode()[:200])
stash = r.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n").split("\n")

hs = [i for i, l in enumerate(stash) if l.startswith(HELD_START)]
if len(hs) != 1:
    sys.exit("HALT: the held section's heading occurs %d times in the stash, "
             "expected 1" % len(hs))
held = stash[hs[0]:]
while held and not held[-1].strip():
    held.pop()
print("held section: stash ll.%d-%d, %d lines (%d carrying text)"
      % (hs[0] + 1, hs[0] + len(held), len(held),
         sum(1 for l in held if l.strip())))

at = [i for i, l in enumerate(lines) if l.startswith(INSERT_BEFORE)]
if len(at) != 1:
    sys.exit("HALT: %r occurs %d times in the record, expected 1"
             % (INSERT_BEFORE, len(at)))
i = at[0]
print("inserting before l.%d  %r" % (i + 1, lines[i][:60]))

# The heading above the insertion point, so the report says what it lands after.
prev = next((l for l in reversed(lines[:i]) if l.startswith("## ")), "(none)")
print("lands after: %s" % prev[:70])

banner = BANNER.read_text(encoding="utf-8").replace("\r\n", "\n").strip("\n").split("\n")
block = banner + [""] + held + [""]

out = lines[:i] + block + lines[i:]

# Structure BEFORE the write: a `---` flush against text becomes a setext heading
# and silently re-reads the line above it as a title.
for k, l in enumerate(out):
    if l.strip() == "---" and k and out[k - 1].strip() \
            and not out[k - 1].lstrip().startswith("|"):
        sys.exit("HALT: a `---` at l.%d sits flush against %r" % (k + 1, out[k - 1][:60]))
print("structure: no rule flush against text")

# Every held line must survive the splice -- the whole point is that none is lost.
joined = set(l.strip() for l in out)
lost = [l for l in held if l.strip() and l.strip() not in joined]
if lost:
    sys.exit("HALT: %d held line(s) did not survive the splice" % len(lost))
print("every held line carrying text is present after the splice")

TARGET.write_bytes(("\n".join(out)).replace("\n", nl).encode("utf-8"))
b = TARGET.read_bytes()
print("ROUND_STATE.md after : %s  (%d lines, %d CRLF / %d LF)"
      % (hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
         b.count(b"\r\n"), b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("control chars beyond tab/LF/CR: %s" % (bad or "none"))

WORK_ROOT.write_bytes(b)
ok = hashlib.sha256(WORK_ROOT.read_bytes()).hexdigest() == hashlib.sha256(b).hexdigest()
print("work-root copy identical: %s" % ok)
if not ok:
    sys.exit("HALT: the work-root copy does not match; D10 would not reconcile")
