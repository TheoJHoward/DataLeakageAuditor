"""A17‴ -- repair every site the gate names. Values from `v30a.hashes.txt` ONLY.

TWO SITES, both named by D7 (`declaration_values`):

  README.md                                  the v30a hash block, 20 lines
  evidence/fixture_spike/f4/DECLARATION_POINTER.md   its CURRENT sha256/bytes

`README.md` l.60 is INSIDE the hash block, so replacing the block repairs it --
they are one site, not two, and treating them separately would have edited the
same line twice.

NOTHING IS TRANSCRIBED. The block is written from `v30a.hashes.txt` verbatim --
C2's own output, the file the README's own marker names: "FILLED AT CEREMONY
TIME FROM v30a.hashes.txt. DO NOT TRANSCRIBE." The pointer's byte count is
derived by reading the file, never copied from a report.

`PREREG.md` IS NOT TOUCHED AND CANNOT BE. R148 §1.1 closes the surface; this
script asserts PREREG.md's hash is unchanged across its own run and halts if it
moved.

    usage: a17_repair_sites.py
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]
README = REPO / "README.md"
PTR = REPO / "evidence/fixture_spike/f4/DECLARATION_POINTER.md"
HASHES = REPO / "v30a.hashes.txt"
DECL = REPO / "AVAILABILITY_DECLARATION.md"
MARKER = "<!-- V30A-HASH-BLOCK:"

prereg_before = hashlib.sha256((REPO / "PREREG.md").read_bytes()).hexdigest()

lines_auth = [l for l in HASHES.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n") if l.strip()]
if len(lines_auth) != 20:
    sys.exit("HALT: v30a.hashes.txt carries %d lines, expected 20" % len(lines_auth))
print("authority: v30a.hashes.txt, %d lines" % len(lines_auth))

decl_sha = next((l.split("  ")[0] for l in lines_auth
                 if l.endswith("  AVAILABILITY_DECLARATION.md")), None)
if decl_sha is None:
    sys.exit("HALT: the declaration is not in v30a.hashes.txt")
decl_bytes = len(DECL.read_bytes())
if hashlib.sha256(DECL.read_bytes()).hexdigest() != decl_sha:
    sys.exit("HALT: the declaration on disk does not match C2's staged hash -- "
             "the index and the working tree disagree and C2's output is not "
             "about the file this script is reading")
print("declaration: %s… / %d bytes (disk == staged)" % (decl_sha[:16], decl_bytes))


def rw(path, fn, label):
    raw = path.read_bytes()
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    if crlf and crlf != lf:
        sys.exit("HALT: %s is mixed (%d/%d)" % (label, crlf, lf))
    nl = "\r\n" if crlf else "\n"
    t = raw.decode("utf-8").replace("\r\n", "\n")
    new = fn(t)
    if new is None:
        print("  %-28s already correct, not rewritten" % label)
        return
    o = new.split("\n")
    for k, l in enumerate(o):
        if l.strip() == "---" and k and o[k - 1].strip() \
                and not o[k - 1].lstrip().startswith("|"):
            sys.exit("HALT: a `---` at %s l.%d sits flush against %r"
                     % (label, k + 1, o[k - 1][:60]))
    path.write_bytes(new.replace("\n", nl).encode("utf-8"))
    b = path.read_bytes()
    print("  %-28s %s  (%d lines, %s)"
          % (label, hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
             "CRLF" if b.count(b"\r\n") else "LF"))


def fix_readme(t):
    i = t.find(MARKER)
    if i < 0:
        sys.exit("HALT: README's V30A-HASH-BLOCK marker is gone")
    # The fence that FOLLOWS the marker. Located from the marker, never by line
    # number -- the file grows.
    a = t.find("```", i)
    b = t.find("```", a + 3)
    if a < 0 or b < 0:
        sys.exit("HALT: README's v30a fence is unbalanced")
    body = "\n".join(lines_auth)
    if t[a + 3:b].strip("\n") == body:
        return None
    return t[:a + 3] + "\n" + body + "\n" + t[b:]


def fix_pointer(t):
    out, changed = [], False
    for l in t.split("\n"):
        m = re.match(r"^(\s*sha256:\s*)([0-9a-f]{64})\s*$", l)
        if m and m.group(2) != decl_sha:
            out.append(m.group(1) + decl_sha)
            changed = True
            continue
        m = re.match(r"^(\s*bytes:\s+)(\d+)\s*$", l)
        if m and int(m.group(2)) != decl_bytes:
            out.append(m.group(1) + str(decl_bytes))
            changed = True
            continue
        out.append(l)
    return "\n".join(out) if changed else None


print("repairing:")
rw(README, fix_readme, "README.md")
rw(PTR, fix_pointer, "DECLARATION_POINTER.md")

prereg_after = hashlib.sha256((REPO / "PREREG.md").read_bytes()).hexdigest()
print()
print("PREREG.md unchanged across this run: %s" % (prereg_before == prereg_after))
if prereg_before != prereg_after:
    sys.exit("HALT: PREREG.md moved. R148 §1.1 closes that surface.")
