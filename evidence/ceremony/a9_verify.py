"""A9 -- the one verification pass over the tag target. Read-only.

C2's twenty hashes are derived ONCE and compared against every surface that
carries them. A surface that agrees with C2 but not with the file on disk is the
failure this exists to catch: C2 reads the INDEX, so index-and-tree drift makes
tagmsg and C2 agree while both are wrong.

FIVE SURFACES, not four -- the commit is included. A tag points at a COMMIT, and
a hash set that matches the index but not the committed tree would attest
something the tag does not contain.

    v30a.hashes.txt   C2's own output
    tagmsg.txt        what the key will sign
    README.md         the published block
    working tree      the bytes on disk
    HEAD              the bytes the tag will point at

    usage: a9_verify.py
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

REPO = pathlib.Path(__file__).resolve().parents[2]


def git(*a):
    r = subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True)
    if r.returncode:
        sys.exit("HALT: git %s -> %s" % (" ".join(a), r.stderr.decode()[:200]))
    return r.stdout


FILES = None
for line in (REPO / "evidence/ceremony/CEREMONY_COMMANDS.md").read_text(
        encoding="utf-8", errors="replace").split("\n"):
    if line.startswith("FILES="):
        FILES = line[len("FILES=\""):].rstrip("\"").split()
        break
if not FILES:
    sys.exit("HALT: the FILES line is unreadable -- the set has no authority")
print("set: %d paths, from the FILES line (count read, never stated)" % len(FILES))

head = git("rev-parse", "HEAD").decode().strip()
print("HEAD: %s" % head)
print()


def parse(text):
    return [l for l in text.replace("\r\n", "\n").split("\n")
            if re.match(r"^[0-9a-f]{64}  ", l)]


c2 = parse((REPO / "v30a.hashes.txt").read_text(encoding="utf-8"))
tag = parse((REPO / "tagmsg.txt").read_text(encoding="utf-8"))
rm_all = (REPO / "README.md").read_text(encoding="utf-8").replace("\r\n", "\n")
i = rm_all.find("<!-- V30A-HASH-BLOCK:")
a = rm_all.find("```", i)
b = rm_all.find("```", a + 3)
readme = parse(rm_all[a + 3:b])
tree = ["%s  %s" % (hashlib.sha256((REPO / f).read_bytes()).hexdigest(), f) for f in FILES]
commit = ["%s  %s" % (hashlib.sha256(git("show", "%s:%s" % (head, f))).hexdigest(), f)
          for f in FILES]

surfaces = [("v30a.hashes.txt", c2), ("tagmsg.txt", tag), ("README block", readme),
            ("working tree", tree), ("HEAD commit", commit)]

fail = 0
print("=== COUNT ===")
for name, s in surfaces:
    ok = len(s) == len(FILES)
    print("  %-18s %2d lines  %s" % (name, len(s), "OK" if ok else "** EXPECTED %d **" % len(FILES)))
    fail += 0 if ok else 1

print()
print("=== ENTRY BY ENTRY, against C2 ===")
for name, s in surfaces[1:]:
    diffs = [(i2, x, y) for i2, (x, y) in enumerate(zip(c2, s), 1) if x != y]
    if diffs and len(s) == len(c2):
        print("  %-18s ** %d DIFFERENCE(S) **" % (name, len(diffs)))
        for i2, x, y in diffs[:3]:
            print("      line %d\n        C2 : %s\n        %s: %s" % (i2, x[:74], name[:5], y[:74]))
        fail += 1
    elif len(s) != len(c2):
        print("  %-18s ** LENGTH MISMATCH, not compared **" % name)
        fail += 1
    else:
        print("  %-18s IDENTICAL, %d of %d" % (name, len(s), len(c2)))

print()
print("=== MANIFEST, three directions ===")
man = REPO / "evidence/MANIFEST.sha256"
entries = [l for l in man.read_text(encoding="utf-8").split("\n")
           if re.match(r"^[0-9a-f]{64}  ", l)]
listed = {l.split("  ", 1)[1] for l in entries}
ok_h = bad_h = 0
for l in entries:
    h, p = l.split("  ", 1)
    f = REPO / "evidence" / p
    if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() == h:
        ok_h += 1
    else:
        bad_h += 1
# PATHS ARE RESOLVED, NOT STRING-MATCHED. The manifest deliberately covers four
# repo-root files with `../` prefixes -- AVAILABILITY_DECLARATION.md and three
# others. A first version compared raw strings against an enumeration of
# `evidence/` only, so all four read as MISSING and A9 went red on a defect in
# the check rather than in the manifest. Direction 1 had already resolved them
# correctly and reported 0 failures, which is what exposed the contradiction.
EV = (REPO / "evidence").resolve()
listed_abs = {(EV / p).resolve() for p in listed}
on_disk_abs = {p.resolve() for p in EV.rglob("*")
               if p.is_file() and "__pycache__" not in p.parts}
# A manifest cannot carry its own hash: adding the line changes the file.
on_disk_abs.discard((EV / "MANIFEST.sha256").resolve())
missing = listed_abs - {p.resolve() for p in listed_abs if p.is_file()}
unlisted = on_disk_abs - listed_abs
print("  1. listed -> hash matches : %d OK / %d FAILED" % (ok_h, bad_h))
print("  2. listed -> on disk      : %d missing" % len(missing))
print("  3. on disk -> listed      : %d unlisted  (MANIFEST.sha256 excluded: "
      "self-reference is circular)" % len(unlisted))
fail += (1 if bad_h else 0) + (1 if missing else 0) + (1 if unlisted else 0)
for p in sorted(missing):
    print("       MISSING : %s" % p)
for p in sorted(unlisted)[:6]:
    print("       unlisted: %s" % p.relative_to(EV).as_posix())

print()
if fail:
    sys.exit("A9 RED: %d check group(s) failed" % fail)
print("A9: every surface agrees with C2, entry by entry and by count; the manifest "
      "reconciles in three directions.")
print("TAG TARGET: %s" % head)
