#!/usr/bin/env python3
"""DELTA R67 - the manifest/tree count literals, same defect class as R23.

V4, §5, §1's path table and blockers 6 and 9 each restate the evidence tree's
composition independently. Measured from the tree this pass:
  249 files in evidence/ (including MANIFEST.sha256)
  251 hashed lines = 248 in-tree (files - 1, the manifest excludes itself) + 3 `../`
  13,047,641 bytes
Every number below is written from that measurement, and the RELATION is stated so
a reader can re-derive rather than trust the numerals.
"""
import pathlib, re

P = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                 "evidence/ceremony/COMMIT_PLAN.md")
s = P.read_text(encoding="utf-8")
EM = "\u2014"; S = "\u00a7"

# ---- V4 -------------------------------------------------------------------
OLD_V4 = """# V4 — the staged evidence count matches the manifest's own claim
git diff --cached --name-only -- evidence | wc -l          # EXPECT 245
grep -cE '^[0-9a-f]{64}  ' evidence/MANIFEST.sha256        # EXPECT 246
# The manifest carries ONE line per in-tree file except itself (244), PLUS the two
# `../` repository-root lines. 244 + 2 = 246 hashed lines over 245 staged files."""
NEW_V4 = """# V4 — the staged evidence count matches the manifest's own claim.
#      DERIVE, don't trust the numerals: the RELATION is the check, and the two
#      counts below were 245/246 until R67 measured the tree and found 249/251.
staged=$(git diff --cached --name-only -- evidence | wc -l)      # measured: 249
hashed=$(grep -cE '^[0-9a-f]{64}  ' evidence/MANIFEST.sha256)    # measured: 251
uplines=$(grep -cE '^[0-9a-f]{64}  \\.\\./' evidence/MANIFEST.sha256)  # measured: 3
[ "$hashed" -eq "$((staged - 1 + uplines))" ] && echo "V4 OK" || echo "V4 FAILED"
# The manifest carries ONE line per in-tree file EXCEPT ITSELF, plus the `../`
# repository-root lines (the declaration, PRIOR_ART_VERIFICATION.md, PRACTICES.md).
# So: hashed == (staged - 1) + uplines. Any other relationship is a manifest defect."""
assert s.count(OLD_V4) == 1, "V4 match %d" % s.count(OLD_V4)
s = s.replace(OLD_V4, NEW_V4, 1)

# ---- §5 -------------------------------------------------------------------
i0 = next(i for i, l in enumerate(s.split("\n")) if l.startswith("## 5. The manifest is FAILING"))
lines = s.split("\n")
i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith("## 6."))
NEW_5 = """## 5. The manifest VERIFIES. Regenerating this package staled four lines; they were re-derived.

`sha256sum -c MANIFEST.sha256`, run from inside `evidence/` this pass:

```
251 lines OK, 0 FAILED
```

**The `author_review/READ_THROUGH_PACKAGE.md` failure recorded here in the previous revision is
GONE** {em} that line verifies. *(This section read "245 of 246 lines verify OK" and named that one
failure; both statements were true when written and are false now. The counts were also stale by
construction: the tree is 249 files, not 245.)*

**Four lines went stale during R67 and were re-derived in the same pass, from the bytes then on
disk:** `ceremony/CEREMONY_COMMANDS.md`, `ceremony/COMMIT_PLAN.md`, `ceremony/DEVIATIONS_DRAFT.md`
and `../AVAILABILITY_DECLARATION.md`. **This is N2 {em} freeze means no SILENT change, not no
change.** The declaration moved because R67/{s}14.3(c) added the three {s}D.3 interpretation entries.

**The declaration's THREE records agree, verified this pass (C2d-2):** the file, the
`../AVAILABILITY_DECLARATION.md` manifest line, and the pointer at
`evidence/fixture_spike/f4/DECLARATION_POINTER.md` all read `06b2974a…` / 301,210 bytes. The
pointer and the manifest line were rewritten in the same pass as the declaration change, as R15
requires {em} the pointer's own manifest line was then re-derived in turn, because updating the
pointer stales it.

**Composition, measured rather than remembered:** 249 files in `evidence/`, 13,047,641 bytes; 251
hashed lines = 248 in-tree (one per file except the manifest itself) + 3 `../` repository-root
lines. V4 checks that relation rather than the numerals.

**Still required before staging:** re-run `sha256sum -c` **immediately before** `git add evidence`.
R15's no-carry-forward rule binds the manifest exactly as it binds the six tag hashes, and the
tree moves. The `# COUNTS.` comment block at the head of `MANIFEST.sha256` is human-readable and
unhashed; regenerate it in the same pass so it does not describe a tree that no longer exists.
"""
lines[i0:i1] = NEW_5.format(em=EM, s=S).split("\n")
s = "\n".join(lines)

# ---- blockers 6 and 9 -----------------------------------------------------
OLD6 = "| 6 | `MANIFEST.sha256` FAILS on one line, and four more go stale with this package (\u00a75) | mechanical | hard |"
NEW6 = "| 6 | ~~`MANIFEST.sha256` FAILS on one line~~ **RESOLVED R67: 251 OK / 0 FAILED, four R67-staled lines re-derived, C2d-2 three-way green (\u00a75)** | mechanical | **done, re-verify at stage time** |"
assert s.count(OLD6) == 1, "blocker 6 match %d" % s.count(OLD6)
s = s.replace(OLD6, NEW6, 1)

OLD9 = "| 9 | Prereg gate and trace suite not re-run against the current tree | AUTHOR | medium |"
NEW9 = "| 9 | ~~Prereg gate and trace suite not re-run~~ **RESOLVED R67: `--stage prereg` 14/14 PASS (incl. the new `hash_set_single_source`), `pytest tests/registration` 137 passed** | mechanical | **done, re-run at stage time (V7)** |"
assert s.count(OLD9) == 1, "blocker 9 match %d" % s.count(OLD9)
s = s.replace(OLD9, NEW9, 1)

# ---- §1 path table byte/file count ---------------------------------------
OLD_T = "**245 files, 13,004,254 bytes** at the instant of measurement"
NEW_T = "**249 files, 13,047,641 bytes** at the instant of measurement (R67; was 245 / 13,004,254)"
if s.count(OLD_T) == 1:
    s = s.replace(OLD_T, NEW_T, 1)
    print("COMMIT_PLAN \u00a71 path table : 245/13,004,254 -> 249/13,047,641")

P.write_text(s, encoding="utf-8")
print("COMMIT_PLAN V4           : numerals -> a derived RELATION (hashed == staged-1+uplines)")
print("COMMIT_PLAN \u00a75           : rewritten against the measured tree; C2d-2 recorded")
print("COMMIT_PLAN blockers 6,9 : both flipped to RESOLVED with their evidence")
