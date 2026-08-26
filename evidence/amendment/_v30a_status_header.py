#!/usr/bin/env python3
"""A16 — correct the declaration's own status marker.

WHAT IS WRONG. The file's top-level status reads "Status: DRAFT. Nothing in this
file is a registered declaration." PREREG.md SC-7(a) hands a detector "the
availability declaration's declared elements" and SC-8(f) calls this the file
that "carries the scoring key". Registered text says the file declares; the file
says it declares nothing. Two registered texts in conflict.

SCOPE, BOUNDED BY §36.2 AND BY WHAT THE FILE ALREADY DISPOSITIONS. The sweep
found four markers of the DRAFT class. Only two are claims about this file's
STANDING:

  l.29/31  the file's own status header          -> corrected here
  l.591    Part II's assembly heading, which is  -> corrected here
           the heading §D sits under

The other two are provenance markers on dated measurement records, and the file
already dispositions them at l.89-93: Part I stands as the measurement record,
and "the Phase-7-added-columns block (T2) and the working-resolution record at
the file tail ... are frozen byte-identical by this item and by every item after
it." Frozen dated records are superseded, never rewritten, so they are left
exactly as they are and named below instead.

"PROVISIONAL until the prereg-v30a tag is signed" is NOT in this class and is not
touched. It is a forward-looking conditional that is true as written and is
discharged by the act of signing.

WRITE-ONCE-GUARDED: if the corrected text is already present, this exits without
writing and says so. Verify its effect by reading the file, never by re-running.

Written with the Write tool per D2.1. CRLF preserved: this file is uniformly CRLF.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"

OLD_HEAD = """## DRAFT \u2014 AUTHOR REVIEW REQUIRED

Status: DRAFT. Nothing in this file is a registered declaration. Every element below is a
reconstruction from archive evidence, assembled by item F4 of "Phase 0 addendum 2: fixture
verification for v30a". Elements marked AMBIGUOUS-PENDING-AUTHOR are genuinely ambiguous on
the evidence and are NOT resolved here."""

NEW_HEAD = """## STATUS \u2014 REGISTERED, AND OPERATIVE AT THE `prereg-v30a` TAG

**This file is the availability declaration `PREREG.md` \u00a76.2 requires, and it is registered.**
Its SHA-256 is enumerated in the `prereg-v30a` tag message, \u00a7D.1's list freezes at that tag, and
`PREREG.md` SC-7(a) names its **declared elements** as one of the two things a detector receives
at gate time. SC-8(f) names it the file that **carries the scoring key**.

**What its earlier status said, and why it is corrected rather than retained.** Until the v30a
amendment was assembled this file read *"Status: DRAFT. Nothing in this file is a registered
declaration."* That was true when written: the file was then a reconstruction awaiting review,
and no tag enumerated it. **It stopped being true when the amendment made this file a hashed,
frozen object that registered clauses read from, and it was not updated.** A status marker is a
claim about the file's standing, so a stale one is a false statement inside the signed object \u2014
not a stale description of something else. Correcting it is the only disposition available:
a disclosure elsewhere cannot repair a claim the tag itself attests.

**Every element below is still a reconstruction from archive evidence**, assembled by item F4 of
"Phase 0 addendum 2: fixture verification for v30a". Registered and reconstructed are not
opposites: what is registered is that these are the declared elements, with the provenance each
one states.

**Section-level markers are NOT claims about this file's standing, and are deliberately left as
they are.** Part I's `AMBIGUOUS-PENDING-AUTHOR` entries record elements the measurement genuinely
did not resolve; where a working resolution later resolved one \u2014 `ties`, Part I section 6, carried
in Part II \u00a712 and frozen at \u00a7D.1 item 1 \u2014 **the resolution governs and Part I stands as the
measurement record.** The Phase-7-added-columns block (T2) and the working-resolution record at
the file tail are **frozen byte-identical** (l.89-93). Rewriting a dated record to look current
falsifies what was known when, which is the one thing those records exist to preserve.

**`PROVISIONAL until the prereg-v30a tag is signed` is a different marker and is untouched.** It
is a forward-looking condition, true as written, and discharged by the signing itself rather than
by an edit."""

OLD_PART2 = "## DRAFT \u2014 AUTHOR REVIEW REQUIRED (v30a assembly)"
NEW_PART2 = ("## PART II \u2014 THE v30a ASSEMBLY (registered; see STATUS above)")

raw = DECL.read_bytes()
crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
if crlf != lf:
    sys.exit("HALT: the declaration is not uniformly CRLF (%d/%d)" % (crlf, lf))
text = raw.decode("utf-8").replace("\r\n", "\n")

# ---- write-once guard ------------------------------------------------------
already = [name for name, probe in
           (("status header", NEW_HEAD.split("\n")[0]),
            ("Part II heading", NEW_PART2)) if probe in text]
if already:
    print("ALREADY APPLIED (%s). Nothing written." % ", ".join(already))
    sys.exit(0)

for old, new, what in ((OLD_HEAD, NEW_HEAD, "status header"),
                       (OLD_PART2, NEW_PART2, "Part II heading")):
    if text.count(old) != 1:
        sys.exit("HALT: %s -- anchor occurs %d times, expected 1" % (what, text.count(old)))
    text = text.replace(old, new, 1)

DECL.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
b = DECL.read_bytes()
print("A16 applied: status header + Part II heading")
print("  %d CRLF / %d LF  uniform=%s" % (b.count(b"\r\n"), b.count(b"\n"),
                                         b.count(b"\r\n") == b.count(b"\n")))
bad = sorted({c for c in b if c < 32 and c not in (9, 10, 13)})
print("  control chars beyond tab/LF/CR: %s" % (bad or "none"))
