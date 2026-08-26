#!/usr/bin/env python3
"""A6 / A5.5 / A7 — tagmsg.txt, DECLARATION_POINTER.md, README's v30a block.

All three take their values from v30a.hashes.txt, which is C2's output and the
single authority for any prereg-v30a hash. Nothing is retyped and nothing is
carried in from a report.

The tag message's prose comes from CEREMONY_COMMANDS.md §3.5's registered format
block, not from this script: the slot count is DERIVED from the block rather than
asserted, so growing the set does not require editing an assertion about its size.

None of these three files is in the hashed set, so writing them after C2 cannot
invalidate C2's output. That ordering is the point.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
CER = REPO / "evidence/ceremony/CEREMONY_COMMANDS.md"
HASHES = REPO / "v30a.hashes.txt"

vals = HASHES.read_text(encoding="utf-8").strip().split("\n")
HASH_LINE = re.compile(r"^([0-9a-f]{64})  (\S+)$")
parsed = [HASH_LINE.match(v) for v in vals]
if not all(parsed):
    sys.exit("HALT: v30a.hashes.txt has a malformed line")

for rel in ("tagmsg.txt", "README.md", "evidence/fixture_spike/f4/DECLARATION_POINTER.md"):
    if any(rel == m.group(2) for m in parsed):
        sys.exit("HALT: %s is in the hashed set; writing it after C2 is unsafe" % rel)

# ---- A6: tagmsg.txt --------------------------------------------------------
body = CER.read_text(encoding="utf-8").replace("\r\n", "\n")
m = re.search(r"\*\*Format of the file, written at tag time:\*\*\n\n```\n(.*?)\n```", body, re.S)
if not m:
    sys.exit("HALT: \u00a73.5's format block not found")
tmpl = m.group(1).split("\n")
SLOT = re.compile(r"^<64 hex>  (\S+)$")
slots = [i for i, l in enumerate(tmpl) if SLOT.match(l)]
if len(slots) != len(vals):
    sys.exit("HALT: the format block has %d slots, v30a.hashes.txt has %d lines"
             % (len(slots), len(vals)))
if slots != list(range(slots[0], slots[0] + len(slots))):
    sys.exit("HALT: the slots are not contiguous")
for k, i in enumerate(slots):
    want, got = SLOT.match(tmpl[i]).group(1), parsed[k].group(2)
    if want != got:
        sys.exit("HALT: slot %d names %r, v30a.hashes.txt names %r" % (k + 1, want, got))
    tmpl[i] = vals[k]
text = "\n".join(tmpl) + "\n"
if "<64 hex>" in text:
    sys.exit("HALT: a placeholder survived")
(REPO / "tagmsg.txt").write_text(text, encoding="utf-8", newline="\n")
print("A6  tagmsg.txt: %d bytes, %d lines, %d hash lines"
      % (len(text.encode("utf-8")), len(tmpl), len(slots)))

# ---- A7: README's v30a block ----------------------------------------------
R = REPO / "README.md"
raw = R.read_bytes()
crlf = raw.count(b"\r\n")
lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("### v30a \u2014 amended registration"))
idx = [i for i in range(start, len(lines)) if re.match(r"^[0-9a-f]{64}  \S", lines[i])]
if not idx or idx != list(range(idx[0], idx[0] + len(idx))):
    sys.exit("HALT: the README's v30a hash lines are absent or not contiguous")
lines[idx[0]:idx[0] + len(idx)] = vals
# the block's own lead-in says "six files"; it is derived from the set, not stated
for i in range(start, idx[0]):
    lines[i] = lines[i].replace(
        "**six files**, the five above\nrecomputed", "the set")
txt = "\n".join(lines)
txt = txt.replace(
    "SHA-256 of the documents and tooling as committed at `prereg-v30a` \u2014 **six files**, the five above\nrecomputed at their v30a state plus the availability declaration:",
    "SHA-256 of every file the `prereg-v30a` tag message enumerates, as committed. The set is the one\n"
    "`PREREG.md` \u00a711 item 8 defines and `AVAILABILITY_DECLARATION.md` \u00a7D.2 sets out; its count is read\n"
    "from the enumeration below, not stated separately:")
R.write_bytes(txt.replace("\n", "\r\n").encode("utf-8") if crlf else txt.encode("utf-8"))
print("A7  README: %d hash lines written from v30a.hashes.txt" % len(vals))

# ---- A5.5 REMOVED ----------------------------------------------------------
# The pointer update lived here and used broad substitutions over the whole
# file. It rewrote every historical hash to the current one and edited a dated
# entry's byte count while missing the current block. That file is a chain of
# frozen dated records; it is updated by _v30a_pointer_sync.py, which edits
# anchored fields only and asserts the chain still holds distinct hashes.
