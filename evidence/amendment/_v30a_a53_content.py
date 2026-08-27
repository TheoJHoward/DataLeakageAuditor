#!/usr/bin/env python3
"""A5.3 — repair every CONTENT site the grown FILES set put out of date.

Checker edits are NOT here. `tools/check_registration.py` is one of the twenty
hashed files, so editing it and C2 must be ordered: content first, checker next,
then one C2 over the result. Splitting them into two scripts makes that order
impossible to get wrong by accident.

Nothing here transcribes a hash. The two D7 sites take their values from
`v30a.hashes.txt`, which is C2's output and the single authority.

Every file is uniformly CRLF and is rewritten as such, per file.

Written with the Write tool per D2.1.
"""
import pathlib
import sys

REPO = pathlib.Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025(4mon)+2026-01")

HASHES = {}
for line in (REPO / "v30a.hashes.txt").read_text(encoding="utf-8").strip().split("\n"):
    d, p = line.split("  ", 1)
    HASHES[p] = d
if len(HASHES) != 20:
    sys.exit("HALT: v30a.hashes.txt carries %d lines, expected 20" % len(HASHES))

DECL_SHA = HASHES["AVAILABILITY_DECLARATION.md"]
DECL_BYTES = len((REPO / "AVAILABILITY_DECLARATION.md").read_bytes())
DECL_LINES = (REPO / "AVAILABILITY_DECLARATION.md").read_bytes().count(b"\n")

FILES = list(HASHES)
SLOTS = "\n".join("<64 hex>  %s" % p for p in FILES)

EDITS = [
    # ---- declaration: the ordinal is gone ---------------------------------
    ("AVAILABILITY_DECLARATION.md",
     "This declaration is hashed in the v30a tag message (\u00a7D.2's sixth hash) and its contents are",
     "This declaration is hashed in the v30a tag message (\u00a7D.2 enumerates the set) and its contents are"),

    # ---- ceremony: "the six" -> the set -----------------------------------
    ("evidence/ceremony/CEREMONY_COMMANDS.md",
     "**Why step 4 cannot move a single one of the six.** The six hashes were read at step 2 from the",
     "**Why step 4 cannot move a single one of the set.** The hashes were read at step 2 from the"),

    # ---- ceremony §3.5: the format block's slots become the set -----------
    ("evidence/ceremony/CEREMONY_COMMANDS.md",
     "<64 hex>  PREREG.md\n<64 hex>  DESIGN.md\n<64 hex>  HISTORY.md\n"
     "<64 hex>  tools/check_registration.py\n<64 hex>  protocol/runtime_reference.py\n"
     "<64 hex>  AVAILABILITY_DECLARATION.md",
     SLOTS),

    # ---- COMMIT_PLAN §6: SUPERSEDE the closure, do not erase it -----------
    ("evidence/ceremony/COMMIT_PLAN.md",
     "## 6. CLOSED \u2014 the tag message carries SIX hashes (R67/\u00a714.1, blocker item 8)",
     "## 6. SUPERSEDED \u2014 the tag message's hash enumeration\n"
     "\n"
     "**This section recorded the set as SIX, and that closure is superseded by `PREREG.md` \u00a711\n"
     "item 8, which defines the set by rule rather than by decision.** The record below stands as\n"
     "what was decided and why; it no longer states the set. The set is `CEREMONY_COMMANDS.md`\n"
     "\u00a73.2's `FILES` line, and its count is read from that line.\n"
     "\n"
     "**`PRIOR_ART_VERIFICATION.md` remains outside the enumeration**, and now by rule rather than\n"
     "by the judgement recorded here: item 1 does not name it, \u00a70.2.1 does not register it, and\n"
     "SC-8(f) does not reach it.\n"
     "\n"
     "### The superseded closure, retained"),

    # ---- COMMIT_PLAN §4: the add-set must cover the set -------------------
    ("evidence/ceremony/COMMIT_PLAN.md",
     "git add tools/check_registration.py protocol/runtime_reference.py",
     "git add tools/check_registration.py protocol/runtime_reference.py\n"
     "git add PARKING_LOT.md VALIDATED_CONFIG.toml\n"
     "git add tests/registration"),

    # ---- DEVIATIONS_DRAFT: the block is the set ---------------------------
    ("evidence/ceremony/DEVIATIONS_DRAFT.md",
     "- Tag message hash block: **SIX** SHA-256 lines \u2014 `PREREG.md`, `DESIGN.md`,\n"
     "  `HISTORY.md`, `tools/check_registration.py`, `protocol/runtime_reference.py`,",
     "- Tag message hash block: the set `PREREG.md` \u00a711 item 8 defines, enumerated at\n"
     "  `CEREMONY_COMMANDS.md` \u00a73.2's `FILES` line, whose count is read from that line \u2014"),

    # ---- F3 verification: §187's first resort, the reword -----------------
    ("evidence/ceremony/F3_MANIFEST_VERIFICATION.md",
     "against the sha256 already pinned at `AVAILABILITY_DECLARATION.md` \u00a7D.1 "
     "(`c659d3ac167a13af\u2026`,",
     "against the sha256 for `phase7_l2_sim.py` already pinned at "
     "`AVAILABILITY_DECLARATION.md` \u00a7D.1 \u2014 that\nfile's hash, "
     "`c659d3ac167a13af\u2026`,"),
]

for rel, old, new in EDITS:
    p = REPO / rel
    raw = p.read_bytes()
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    text = raw.decode("utf-8").replace("\r\n", "\n")
    if text.count(old) != 1:
        sys.exit("HALT: %s -- anchor occurs %d times, expected 1:\n  %r"
                 % (rel, text.count(old), old[:100]))
    text = text.replace(old, new, 1)
    out = text.encode("utf-8") if crlf == 0 else text.replace("\n", "\r\n").encode("utf-8")
    p.write_bytes(out)
    print("repaired  %-46s" % rel)

# ---- DECLARATION_POINTER: values from v30a.hashes.txt only ---------------
DP = REPO / "evidence/fixture_spike/f4/DECLARATION_POINTER.md"
raw = DP.read_bytes()
crlf = raw.count(b"\r\n")
text = raw.decode("utf-8").replace("\r\n", "\n")
import re
before = text
text = re.sub(r"\b10b65a00651b6e8c[0-9a-f]*", DECL_SHA, text)
text = re.sub(r"\b10b65a00651b6e8c\u2026", DECL_SHA[:12] + "\u2026", text)
text = text.replace("309001", "%d" % DECL_BYTES)
if text == before:
    sys.exit("HALT: DECLARATION_POINTER.md unchanged; its stale values were not found")
out = text.encode("utf-8") if crlf == 0 else text.replace("\n", "\r\n").encode("utf-8")
DP.write_bytes(out)
print("repaired  %-46s (from v30a.hashes.txt)" % "DECLARATION_POINTER.md")
print("\ndeclaration: sha256 %s / %d bytes / %d lines" % (DECL_SHA, DECL_BYTES, DECL_LINES))
