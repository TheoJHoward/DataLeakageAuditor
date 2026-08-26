#!/usr/bin/env python3
"""§29 — the three stale declaration hash/size copies, plus the l.1516 drift.

§29.2: a hash or byte size is a VERIFICATION VALUE a reader checks. A stale one
emits a false tamper signal from inside the evidence tree. Ship-critical, not the
prose-count class.

Every value below is DERIVED from the file in this script, never typed.
The DECLARATION_POINTER.md mentions of f0829bd3/277,411 are NOT touched: they are
historical narrative recording a past transition ("moved from X to Y"), and
rewriting them would falsify the record rather than correct it.
"""
import hashlib, pathlib, subprocess

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
DECL = REPO / "AVAILABILITY_DECLARATION.md"
b = DECL.read_bytes()
H = hashlib.sha256(b).hexdigest()
BYTES = len(b)
LINES = b.count(b"\n")
EM = "\u2014"; S = "\u00a7"
print("derived: sha256 %s  bytes %d  lines %d" % (H[:16], BYTES, LINES))

edits = 0

# ---- 1. CEREMONY_COMMANDS.md:26 -------------------------------------------
P = REPO / "evidence/ceremony/CEREMONY_COMMANDS.md"
s = P.read_text(encoding="utf-8")
OLD = ("| Fixture declaration reconstruction with evidence | **done** | "
       "`AVAILABILITY_DECLARATION.md`, 277,411 bytes, sha256 `f0829bd3\u2026` |")
NEW = ("| Fixture declaration reconstruction with evidence | **done** | "
       "`AVAILABILITY_DECLARATION.md` \u2014 **do not read the size or hash from here.** "
       "Derive: `sha256sum AVAILABILITY_DECLARATION.md`, `wc -c`. As at R68: "
       "`%s\u2026`, %s bytes. *(Read `f0829bd3\u2026` / 277,411 for several rounds after the "
       "file had moved; checked by D7 from R68.)* |" % (H[:8], format(BYTES, ",")))
assert s.count(OLD) == 1, "CC:26 match %d" % s.count(OLD)
s = s.replace(OLD, NEW, 1); edits += 1
P.write_text(s, encoding="utf-8")
print("CEREMONY_COMMANDS.md:26  corrected")

# ---- 2. COMMIT_PLAN.md:80 --------------------------------------------------
P = REPO / "evidence/ceremony/COMMIT_PLAN.md"
s = P.read_text(encoding="utf-8")
OLD = ("**` M ` \u2014 MODIFIED since that commit.** 38 insertions, 4 deletions. Working tree: "
       "sha256 `f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310`, "
       "**277,411 bytes**, **3,684 lines** (`wc -l`; the file ends with a newline)")
NEW = ("**` M ` \u2014 MODIFIED since that commit.** Working tree, **derived not transcribed** "
       "(`sha256sum`, `wc -c`, `wc -l`) \u2014 as at R68: sha256 "
       "`%s`, **%s bytes**, **%s lines** (the file ends with a newline). "
       "*The diffstat against `ffa6d94` is not restated here: read it with "
       "`git diff --numstat ffa6d94 -- AVAILABILITY_DECLARATION.md`. This cell read "
       "`f0829bd3\u2026` / 277,411 / 3,684 / \"38 insertions, 4 deletions\" after the file had "
       "moved three times; checked by D7 from R68.*"
       % (H, format(BYTES, ","), format(LINES, ",")))
assert s.count(OLD) == 1, "CP:80 match %d" % s.count(OLD)
s = s.replace(OLD, NEW, 1); edits += 1

# ---- 4. COMMIT_PLAN.md l.1516 citation ------------------------------------
OLD_C = "the declaration's own walk summary (\u00a7A.11 l.1516)"
NEW_C = "the declaration's own walk summary (\u00a7A.11, heading \"A.11 \u2014 Walk summary\"; cited by anchor, not line)"
if s.count(OLD_C) == 1:
    s = s.replace(OLD_C, NEW_C, 1); edits += 1
    print("COMMIT_PLAN.md           l.1516 -> anchor")
P.write_text(s, encoding="utf-8")
print("COMMIT_PLAN.md:80        corrected")

# ---- 3. DEVIATIONS_DRAFT.md:307 -------------------------------------------
P = REPO / "evidence/ceremony/DEVIATIONS_DRAFT.md"
s = P.read_text(encoding="utf-8")
OLD = ("Line numbers are into the working-tree `AVAILABILITY_DECLARATION.md` (sha256\n"
       "`f0829bd3a0f11b05170a5e2686b953c5def39104af0bbfa2904afb3da2f53310`, 277,411 bytes) as read this\n"
       "pass.")
NEW = ("Line numbers are into the working-tree `AVAILABILITY_DECLARATION.md`, **derived not\n"
       "transcribed** \u2014 as at R68: sha256 `%s`,\n"
       "%s bytes, %s lines. **Any declaration line number below is stale unless it was\n"
       "re-derived against that hash**, which is why the citations that matter are given by anchor.\n"
       "*(This paragraph read `f0829bd3\u2026` / 277,411 for several rounds after the file had moved;\n"
       "checked by D7 from R68.)*" % (H, format(BYTES, ","), format(LINES, ",")))
assert s.count(OLD) == 1, "DD:307 match %d" % s.count(OLD)
s = s.replace(OLD, NEW, 1); edits += 1

OLD_D = "Source: declaration \u00a7A.11 walk summary l.1516"
NEW_D = "Source: declaration \u00a7A.11 walk summary (by anchor \u2014 heading \"A.11 \u2014 Walk summary\")"
if s.count(OLD_D) == 1:
    s = s.replace(OLD_D, NEW_D, 1); edits += 1
    print("DEVIATIONS_DRAFT.md      l.1516 -> anchor")
P.write_text(s, encoding="utf-8")
print("DEVIATIONS_DRAFT.md:307  corrected")

# ---- 5. H34_DRAFT.md l.1516 ------------------------------------------------
P = REPO / "evidence/ceremony/H34_DRAFT.md"
s = P.read_text(encoding="utf-8")
OLD_H = "\u00a7A.11 walk summary l.1516"
if s.count(OLD_H) == 1:
    s = s.replace(OLD_H, "\u00a7A.11 walk summary (by anchor)", 1); edits += 1
    P.write_text(s, encoding="utf-8")
    print("H34_DRAFT.md             l.1516 -> anchor")

print("\ntotal edits: %d" % edits)
