"""A17‴ -- regenerate `tagmsg.txt`. Then C2f. Nothing here is typed.

THE TWO VARIABLE PARTS EACH HAVE EXACTLY ONE AUTHORITY:

    the change list   <- v30a.changes.txt   (a27_derive_changes.py's output)
    the hash lines    <- v30a.hashes.txt    (C2's output, staged content)

Both are pasted, never retyped. §3.5 of `CEREMONY_COMMANDS.md` states the rule
for the hashes -- "the output of C2, pasted, never retyped" -- and R140/A27
extended it to the change list, which until then was PROSE in the ceremony file
naming three §6.2 changes the file it hashes did not contain.

THE FIXED PARTS are carried from the existing message verbatim: the title, the
hash-block lead-in, the signing-key block and the OpenTimestamps paragraph. They
are located by anchor and reused, not respelled -- the key fingerprint in
particular is a value no script should ever retype.

WHY NOT THE CEREMONY FILE'S OWN C2h-1 SNIPPET: it asserts the hash file carries
SIX lines. The set grew to twenty at A5, so that assertion is stale and would
halt on correct input. It is also a shell heredoc, which D2.1 forbids for file
content. The rule it encodes -- fill from v30a.hashes.txt, never from tagmsg or
the v30 block -- is what this script implements.

    usage: a17_tagmsg.py
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
TAG = REPO / "tagmsg.txt"
HASHES = REPO / "v30a.hashes.txt"
CHANGES = REPO / "v30a.changes.txt"

old_raw = TAG.read_bytes()
if old_raw.count(b"\r\n"):
    sys.exit("HALT: tagmsg.txt carries CRLF; a tag message is LF")
old = old_raw.decode("utf-8")

hashes = [l for l in HASHES.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n") if l.strip()]
if len(hashes) != 20:
    sys.exit("HALT: v30a.hashes.txt carries %d lines, expected 20" % len(hashes))
changes = CHANGES.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
if not changes:
    sys.exit("HALT: v30a.changes.txt is empty")
print("authorities: %d hash lines, %d-char change list" % (len(hashes), len(changes)))

lines = old.split("\n")
title = lines[0]
if "v30a" not in title:
    sys.exit("HALT: the first line is not the v30a title: %r" % title[:60])

LEAD = "SHA-256 of the registration documents and tooling as committed:"
i_lead = next((n for n, l in enumerate(lines) if l.startswith(LEAD)), None)
if i_lead is None:
    sys.exit("HALT: the hash-block lead-in is missing")

# The TAIL -- signing key and OTS paragraph -- is carried verbatim from the
# existing message. The key fingerprint is never retyped by a script.
i_key = next((n for n, l in enumerate(lines) if l.startswith("Signing key:")), None)
if i_key is None:
    sys.exit("HALT: the signing-key block is missing")
tail = [l for l in lines[i_key:]]
while tail and not tail[-1].strip():
    tail.pop()
if "991F 5331 C584 CE5E AF7D  6939 B29C F0E8 4711 9AD7" not in "\n".join(tail):
    sys.exit("HALT: the key fingerprint is not in the carried tail")

out = [title, "", changes, "", LEAD, ""] + hashes + [""] + tail
new = "\n".join(out) + "\n"

if new == old:
    print("ALREADY CURRENT. Nothing written.")
else:
    TAG.write_bytes(new.encode("utf-8"))
    b = TAG.read_bytes()
    print("tagmsg.txt %s -> %s  (%d lines, %d CRLF / %d LF)"
          % (hashlib.sha256(old_raw).hexdigest()[:16],
             hashlib.sha256(b).hexdigest()[:16], b.count(b"\n"),
             b.count(b"\r\n"), b.count(b"\n")))
    bad = sorted({c for c in b if c < 32 and c not in (9, 10)})
    print("control chars beyond tab/LF: %s" % (bad or "none"))

# --- C2f: the message's hash block against C2's own output -----------------
cur = TAG.read_text(encoding="utf-8").split("\n")
block = [l for l in cur if re.match(r"^[0-9a-f]{64}  ", l)]
print()
print("C2f -- tagmsg hash block vs v30a.hashes.txt")
print("  lines in message : %d" % len(block))
print("  lines in C2 output: %d" % len(hashes))
if block != hashes:
    for a, b_ in zip(block, hashes):
        if a != b_:
            print("  FIRST DIFFERENCE\n    msg: %s\n    C2 : %s" % (a[:78], b_[:78]))
            break
    sys.exit("HALT: C2f RED -- the tag message and C2's output disagree")
print("  C2f GREEN -- identical, entry by entry and by count")

# The change list must be present verbatim too; C2f as written only checks the
# hashes, and a message can carry the right hashes under the wrong description.
if changes not in TAG.read_text(encoding="utf-8"):
    sys.exit("HALT: the change list in the message is not v30a.changes.txt's")
print("  change list: present verbatim from v30a.changes.txt")
