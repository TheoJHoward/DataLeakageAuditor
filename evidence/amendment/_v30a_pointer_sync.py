#!/usr/bin/env python3
"""Update DECLARATION_POINTER.md's CURRENT block, and NOTHING else in the file.

WHY THIS IS A SEPARATE, NARROW SCRIPT. A broad substitution over this file is
actively dangerous and was tried twice: `re.sub(r"\\b[0-9a-f]{64}\\b", new, text)`
rewrote every historical hash in the file to the current one, and
`\\b\\d{6}\\b(?= bytes)` rewrote a 2026-08-21 dated entry's byte count while
MISSING the current block, whose field is written `bytes:  NNNNNN` with two
spaces. The file is mostly a chain of dated supersession entries, and those are
frozen records: rewriting one to look current falsifies what was true when.

So this edits three anchored fields in the CURRENT block, appends one dated
entry, and asserts afterwards that the historical chain still holds more than one
distinct hash -- the cheap invariant that catches a flattening substitution.

Written with the Write tool per D2.1.
"""
import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"
DP = REPO / "evidence/fixture_spike/f4/DECLARATION_POINTER.md"

db = DECL.read_bytes()
sha, nbytes, nlines = hashlib.sha256(db).hexdigest(), len(db), db.count(b"\n")

auth = {}
for line in (REPO / "v30a.hashes.txt").read_text(encoding="utf-8").strip().split("\n"):
    d, p = line.split("  ", 1)
    auth[p] = d
if auth["AVAILABILITY_DECLARATION.md"] != sha:
    sys.exit("HALT: the declaration on disk differs from C2's staged hash; re-stage first")

raw = DP.read_bytes()
crlf = raw.count(b"\r\n")
t = raw.decode("utf-8").replace("\r\n", "\n")
before_distinct = len(set(re.findall(r"\b[0-9a-f]{64}\b", t)))

m_sha = re.search(r"^    sha256: ([0-9a-f]{64})$", t, re.M)
m_b = re.search(r"^    bytes:  (\d+)$", t, re.M)
if not (m_sha and m_b):
    sys.exit("HALT: the CURRENT block's sha256/bytes fields were not found")
old_sha, old_bytes = m_sha.group(1), m_b.group(1)

t = t[:m_sha.start(1)] + sha + t[m_sha.end(1):]
m_b = re.search(r"^    bytes:  (\d+)$", t, re.M)
t = t[:m_b.start(1)] + str(nbytes) + t[m_b.end(1):]

ANCHOR = "**2026-08-26 (author sign-off) \u2014 the current bytes.**"
ENTRY = ("**2026-08-26 (v30a closeout) \u2014 the current bytes.** The declaration moved from "
         "`%s\u2026` / %s bytes to `%s\u2026` / %s bytes / %d lines, on the \u00a7D.2 hash-enumeration "
         "rewrite, \u00a7D.5's named open obligations, \u00a7D.6's five deployed disclosures, \u00a7D.1's "
         "repository path for the pinned producing code, and \u00a7146.2's frame extension to the tag "
         "message. **Rewritten in the same pass that moved the declaration, per R15.** Values "
         "derived with `sha256sum` and `wc`, never transcribed.\n\n"
         % (old_sha[:8], format(int(old_bytes), ","), sha[:8], format(nbytes, ","), nlines))
if t.count(ANCHOR) != 1:
    sys.exit("HALT: the dated-entry anchor is not unique")
t = t.replace(ANCHOR, ENTRY + ANCHOR, 1)

after_distinct = len(set(re.findall(r"\b[0-9a-f]{64}\b", t)))
if after_distinct < before_distinct:
    sys.exit("HALT: distinct hashes fell from %d to %d -- a historical value was "
             "overwritten" % (before_distinct, after_distinct))

DP.write_bytes(t.replace("\n", "\r\n").encode("utf-8") if crlf else t.encode("utf-8"))
print("CURRENT block: %s\u2026 / %s bytes / %d lines" % (sha[:12], format(nbytes, ","), nlines))
print("distinct hashes in the chain: %d -> %d (no historical value overwritten)"
      % (before_distinct, after_distinct))
