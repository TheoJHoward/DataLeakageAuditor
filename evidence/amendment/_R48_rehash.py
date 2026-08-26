#!/usr/bin/env python3
"""DELTA R48 - rewrite the declaration hash EVERYWHERE, in ONE pass.

R15's rule, and the reason the C2d-2 three-way agreement gate exists: `sha256sum -c`
verifies a pointer file's own BYTES, never the hash written INSIDE it. Last time a
scrub moved the declaration and only the manifest line was rewritten, the drift went
uncaught for a full round.

Three records must agree afterwards: the file, the pointer's recorded hash, the
manifest line. CEREMONY_COMMANDS.md also moved and is manifested.
"""
import hashlib
import pathlib
import re

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

OLD = "ddbf7f2d09842be09c0e9c1e3e0056e5f7a086b74551586ce571076c08aa48d6"
OLD_BYTES, OLD_LINES = "287480", "3,796"

decl = REPO / "AVAILABILITY_DECLARATION.md"
raw = decl.read_bytes()
NEW = hashlib.sha256(raw).hexdigest()
NEW_BYTES = str(len(raw))
NEW_LINES = "{:,}".format(decl.read_text(encoding="utf-8").count("\n") + 1)
print("declaration: %s -> %s" % (OLD[:12], NEW[:12]))
print("  bytes %s -> %s   lines %s -> %s" % (OLD_BYTES, NEW_BYTES, OLD_LINES, NEW_LINES))
assert NEW != OLD

# ---------------------------------------------------------------- 1. manifest
man = REPO / "evidence" / "MANIFEST.sha256"
m = man.read_text(encoding="utf-8")
line_old = OLD + "  ../AVAILABILITY_DECLARATION.md"
assert m.count(line_old) == 1, "manifest decl line match %d" % m.count(line_old)
m = m.replace(line_old, NEW + "  ../AVAILABILITY_DECLARATION.md", 1)

# CEREMONY_COMMANDS.md moved too
cer = REPO / "evidence" / "ceremony" / "CEREMONY_COMMANDS.md"
cer_new = hashlib.sha256(cer.read_bytes()).hexdigest()
rows = [l for l in m.split("\n") if l.strip().endswith("ceremony/CEREMONY_COMMANDS.md")
        or l.strip().endswith("ceremony\\CEREMONY_COMMANDS.md")]
assert len(rows) == 1, "ceremony manifest rows: %d" % len(rows)
old_row = rows[0]
new_row = re.sub(r"^[0-9a-f]{64}", cer_new, old_row)
m = m.replace(old_row, new_row, 1)
man.write_text(m, encoding="utf-8")
print("MANIFEST.sha256: declaration line + ceremony line rewritten")
print("  ceremony: %s -> %s" % (old_row[:12], cer_new[:12]))

# ---------------------------------------------------------------- 2. pointer
ptr = REPO / "evidence" / "fixture_spike" / "f4" / "DECLARATION_POINTER.md"
p = ptr.read_text(encoding="utf-8")
assert p.count("sha256: " + OLD) == 1, "pointer sha line match %d" % p.count("sha256: " + OLD)
p = p.replace("sha256: " + OLD, "sha256: " + NEW, 1)
assert p.count("bytes:  " + OLD_BYTES) == 1, "pointer bytes match"
p = p.replace("bytes:  " + OLD_BYTES, "bytes:  " + NEW_BYTES, 1)

OLD_AS_OF = ("    as of:  2026-08-20, at the writing of this hash block (the v30a declaration scrub; the")
assert p.count(OLD_AS_OF) == 1, "pointer as-of match %d" % p.count(OLD_AS_OF)
p = p.replace(OLD_AS_OF,
              "    as of:  2026-08-21, at the writing of this hash block (R48/Q2, Q4, Q7 corrections to\n"
              "            \u00a7A.1 and \u00a7A.5; supersedes the 2026-08-20 v30a scrub block below; the", 1)

# provenance paragraph: append the R48 movement rather than overwrite the scrub record
OLD_PROV = ("from `f0829bd3\u20263310` / 277,411 bytes / 3,684 lines to `ddbf7f2d\u202648d6` / 287,480 bytes / 3,796")
assert p.count(OLD_PROV) == 1, "pointer provenance match %d" % p.count(OLD_PROV)
p = p.replace(OLD_PROV,
              "from `f0829bd3\u20263310` / 277,411 bytes / 3,684 lines to `ddbf7f2d\u202648d6` / 287,480 bytes / 3,796", 1)

MARKER = "**Provenance of the current bytes \u2014 HISTORICAL RECORD, NOT A PROCEDURE.**"
assert p.count(MARKER) == 1
ADD = ("**2026-08-21 (R48) \u2014 the current bytes.** The declaration moved again, from `ddbf7f2d\u202648d6` / "
       "287,480 bytes / 3,796 lines to `" + NEW[:8] + "\u2026" + NEW[-4:] + "` / " + NEW_BYTES + " bytes / " +
       NEW_LINES + " lines, on three corrections: \u00a7A.5's statement that no cross-tool comparison had "
       "been run (false when written \u2014 one ran on 14 Aug 2026 and does not satisfy \u00a79.2), \u00a7A.1 item 2's "
       "model-family claim (false against its own cited source), and a new \u00a7A.1 item 4 registering **ex "
       "ante** that the post-fix trio has no originating counterpart. The manifest line and this hash "
       "block were rewritten **in the same pass**, which is what R15 requires and what failing to do "
       "produced the drift recorded below.\n\n" + MARKER)
p = p.replace(MARKER, ADD, 1)
ptr.write_text(p, encoding="utf-8")
print("DECLARATION_POINTER.md: hash, bytes, as-of, and provenance rewritten IN THE SAME PASS")
