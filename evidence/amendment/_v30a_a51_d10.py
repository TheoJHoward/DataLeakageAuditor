#!/usr/bin/env python3
"""A5.1 — disclose the round-reconciliation check's domain as D-INSTRUMENT (6),
and record the fail-loud redesign in DEFERRED_ITEMS.md with its substance.

The final sentence of the disclosure is load-bearing and is the D-STALE
construction: it states what the check does not REACH, and refuses to imply an
extent. A disclosure that said "these files were missed" would claim a
completeness it cannot have, because the check never looked.

Also updates the "five remain open" count to six -- a lead-in that enumerates
its own list and then disagrees with it is the reconciliation defect the review
lessons record, and it is one line away here.

Both files are uniformly CRLF; endings preserved per file.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")

ITEM6 = (
    "> 6. **The round-reconciliation check reports that every working file is either in the\n"
    ">    repository or declared ephemeral. Its population is a pinned scratchpad path, and that\n"
    ">    path does not track the directory in which work is performed.** Its pass is therefore\n"
    ">    evidence about the pinned directory alone, and is not evidence about files created\n"
    ">    outside it. The files created during this amendment were placed in the repository or\n"
    ">    declared ephemeral **by procedure, not by this check**. This states what the check does\n"
    ">    not reach; it does not enumerate what it missed.\n")

ANCHOR = (
    "> 5. **The staging check cannot see staging performed by any means other than a literal "
    "`git add`\n"
    ">    line** \u2014 a wildcard, a variable or a loop is invisible to it.\n")

COUNT_OLD = "> **The checks that verify this ceremony have measured domains, and the gaps are disclosed.** Five\n> remain open at the tag:"
COUNT_NEW = "> **The checks that verify this ceremony have measured domains, and the gaps are disclosed.** Six\n> remain open at the tag:"

DECL = REPO / "AVAILABILITY_DECLARATION.md"
raw = DECL.read_bytes()
if raw.count(b"\r\n") != raw.count(b"\n"):
    sys.exit("HALT: declaration is not uniformly CRLF")
text = raw.decode("utf-8").replace("\r\n", "\n")

for old, new, what in ((ANCHOR, ANCHOR + ITEM6, "D-INSTRUMENT item 6"),
                       (COUNT_OLD, COUNT_NEW, "the five/six lead-in")):
    if text.count(old) != 1:
        sys.exit("HALT: %s -- anchor occurs %d times, expected 1" % (what, text.count(old)))
    text = text.replace(old, new, 1)

DECL.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
print("D-INSTRUMENT (6) appended; lead-in count corrected to six")

# ---- DEFERRED_ITEMS.md: the redesign, with substance ----------------------
DI = REPO / "evidence/session/DEFERRED_ITEMS.md"
raw = DI.read_bytes()
if raw.count(b"\r\n") != raw.count(b"\n"):
    sys.exit("HALT: DEFERRED_ITEMS.md is not uniformly CRLF")
di = raw.decode("utf-8").replace("\r\n", "\n").rstrip("\n")

ENTRY = """

---

## FIRST POST-TAG ITEM — the round-reconciliation check fails silent

**The defect.** The check's population is a pinned absolute path to one session's
scratchpad. Work is performed in a different directory, so the population it walks
is not the population it claims. It reports `every working file is in the
repository or declared ephemeral` and prints the same green whether the pinned
directory holds the work, holds stale files, or does not exist at all.

**Why it is disclosed rather than repaired before the tag.** Repairing it turns
the gate red immediately, which forces a re-pin to the current session — and that
re-pin detaches again at the next session, which is the same defect with a fresher
value. It also puts a second edit into a hashed tool immediately before the hash
set is derived. The disclosure is the one-way door: the declaration freezes at the
tag, and a tool can be corrected in any later version.

**The end state, stated so it is not re-derived later.**

1. **Derive the population, never pin it.** The working directory is discoverable
   at run time; an absolute path written once is a carried-forward value and goes
   stale the way every other carried-forward value in this ceremony went stale.
2. **Exit non-zero when the population is empty or its root is absent.** A check
   that prints over nothing is not a check, and its silence is indistinguishable
   from a pass. This is the fail-loud half and it is the part that matters: had it
   been present, the pinned path would have announced itself the first time it
   pointed at a directory that no longer held the work.
3. **State the population with the result**, as the sweep discipline already
   requires elsewhere — the count of files walked and the root walked, printed
   beside the verdict, so a domain that has moved is visible in the output rather
   than only in the source.

**Known-positive required before the repair is believed:** point the check at a
directory that does not exist, and at one that exists but is empty. It must exit
non-zero for both. A check that has only ever run against a populated directory
has not been shown to detect an unpopulated one."""

DI.write_bytes((di + ENTRY + "\n").replace("\n", "\r\n").encode("utf-8"))
print("DEFERRED_ITEMS.md: redesign recorded with substance, flagged first post-tag")
for rel in ("AVAILABILITY_DECLARATION.md", "evidence/session/DEFERRED_ITEMS.md"):
    b = (REPO / rel).read_bytes()
    print("  %-34s %d CRLF / %d LF uniform=%s"
          % (rel, b.count(b"\r\n"), b.count(b"\n"), b.count(b"\r\n") == b.count(b"\n")))
