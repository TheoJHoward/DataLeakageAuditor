#!/usr/bin/env python3
"""A4.4 — the three records that cited D-ARCHIVE, and the producing code's arrival.

TWO DIFFERENT TREATMENTS, because the records are different kinds:

  F3_MANIFEST_VERIFICATION.md is a DATED evidence record. Its warning was TRUE on
  its date. It is SUPERSEDED by a dated entry above it, never rewritten -- a
  frozen dated record edited to look current falsifies what was known when.

  DEFERRED_ITEMS.md and ROUND_STATE.md are LIVE working records. They are updated
  in place, because their job is to say what is true now.

THE SCOPE COLLISION, SAID OUT LOUD. D-ARCHIVE's draft said "the producing code IS
committed"; F3_MANIFEST_VERIFICATION.md said "THE PRODUCING CODE IS NOT IN THE
REPOSITORY". Both were true -- of the three spike producers and of
phase7_l2_sim.py respectively -- and nothing anywhere said they were talking about
different sets. The supersession note says it.

All three files are uniformly CRLF; line endings are preserved per file.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")

EDITS = []

# ---- 1. F3_MANIFEST_VERIFICATION.md : SUPERSEDE, do not rewrite -------------
F3 = "evidence/ceremony/F3_MANIFEST_VERIFICATION.md"
F3_ANCHOR = ("> **\u26a0 THE PRODUCING CODE IS NOT IN THE REPOSITORY.**")
F3_NOTE = (
    "**SUPERSEDED IN PART, 26 August 2026 \u2014 the producing code is now in the "
    "repository.**\n"
    "`phase7_l2_sim.py` was copied to `evidence/fixture_spike/f3/`, verified at the "
    "destination\n"
    "against the sha256 already pinned at `AVAILABILITY_DECLARATION.md` \u00a7D.1 "
    "(`c659d3ac167a13af\u2026`,\n"
    "41,745 bytes, 949 lines), and is hashed in the `prereg-v30a` tag message. **The "
    "warning\n"
    "below was true on its date and is retained unedited**; what follows it about "
    "reading from\n"
    "the archive copy records how this verification was actually performed, which "
    "does not\n"
    "change.\n"
    "\n"
    "**A scope collision this supersession also closes.** The `D-ARCHIVE` disclosure "
    "draft read\n"
    "*\"The producing code IS committed\"* while the warning below read *\"THE "
    "PRODUCING CODE IS\n"
    "NOT IN THE REPOSITORY\"*. **Both were true \u2014 of different sets:** the first "
    "of the three\n"
    "spike producers brought in earlier, the second of `phase7_l2_sim.py`, which was "
    "not among\n"
    "them. Nothing anywhere said they were speaking about different sets, so the pair "
    "read as a\n"
    "contradiction. It was not one, and it is no longer live either way.\n"
    "\n")
EDITS.append((F3, F3_ANCHOR, F3_NOTE + F3_ANCHOR, "supersede"))

# ---- 2. DEFERRED_ITEMS.md : update in place --------------------------------
DI = "evidence/session/DEFERRED_ITEMS.md"
DI_OLD = (
    "**949 lines, 41,745 bytes (~41 KB)**, currently\n"
    "resident only in the archive at `results\\pc2_all_phases\\_scripts\\scripts\\`.")
DI_NEW = (
    "**949 lines, 41,745 bytes (~41 KB)**.\n"
    "**DISCHARGED 26 August 2026: it is in the repository** at "
    "`evidence/fixture_spike/f3/phase7_l2_sim.py`,\n"
    "hashed in the `prereg-v30a` tag message and attested in the evidence manifest. It "
    "was copied\n"
    "from the archive at `results\\pc2_all_phases\\_scripts\\scripts\\` and verified at "
    "the\n"
    "destination against the pin, which was not re-taken from the copy.")
EDITS.append((DI, DI_OLD, DI_NEW, "update in place"))

DI_OLD2 = (
    "**Why it is post-tag.** Bringing it in **changes what ships**, and its absence "
    "makes\n"
    "**nothing in the signed object false**")
DI_NEW2 = (
    "**Why it was carried as post-tag, and why that changed.** Bringing it in **changes "
    "what\n"
    "ships**, and its absence made **nothing in the signed object false**")
EDITS.append((DI, DI_OLD2, DI_NEW2, "update in place"))

# ---- 3. ROUND_STATE.md : update in place -----------------------------------
RS = "evidence/session/ROUND_STATE.md"
RS_OLD = (
    "**949 lines, 41,745 bytes**, archive-resident, **not in the repository** \u2014 "
    "hash re-derived, not\n"
    "copied. D-ARCHIVE gained its own sentence. Bringing the file in is recorded "
    "**post-tag and\n"
    "RECOMMENDED** (~41 KB makes the 35 classifications independently verifiable).")
RS_NEW = (
    "**949 lines, 41,745 bytes** \u2014 hash re-derived, not copied. **The file is now IN "
    "THE\n"
    "REPOSITORY** at `evidence/fixture_spike/f3/phase7_l2_sim.py`, verified at the "
    "destination\n"
    "against that pin and hashed in the tag message; the 35 classifications are "
    "independently\n"
    "verifiable from the repository alone. D-ARCHIVE is deployed at "
    "`AVAILABILITY_DECLARATION.md`\n"
    "\u00a7D.6 and now states the narrower true position: the derivation can be audited "
    "from the\n"
    "repository, the inputs it consumed remain external, so it cannot be re-executed "
    "there.")
EDITS.append((RS, RS_OLD, RS_NEW, "update in place"))

for rel, old, new, kind in EDITS:
    p = REPO / rel
    raw = p.read_bytes()
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    if crlf != lf:
        sys.exit("HALT: %s is not uniformly CRLF (%d/%d)" % (rel, crlf, lf))
    text = raw.decode("utf-8").replace("\r\n", "\n")
    if text.count(old) != 1:
        sys.exit("HALT: %s -- anchor occurs %d times, expected 1:\n%r"
                 % (rel, text.count(old), old[:90]))
    text = text.replace(old, new, 1)
    p.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
    print("%-46s %s" % (rel, kind))

for rel in {e[0] for e in EDITS}:
    raw = (REPO / rel).read_bytes()
    print("  %-44s %d CRLF / %d LF  uniform=%s"
          % (rel, raw.count(b"\r\n"), raw.count(b"\n"),
             raw.count(b"\r\n") == raw.count(b"\n")))
