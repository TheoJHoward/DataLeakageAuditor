#!/usr/bin/env python3
"""DELTA R48 - rewrite ROUND_STATE's current-delta section. R36: every round."""
import hashlib
import pathlib

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

p = SCR / "ROUND_STATE.md"
t = p.read_text(encoding="utf-8")

OLD_H = "## 1. CURRENT DELTA \u2014 R47 (21 Aug 2026), items P1\u2013P10"
assert t.count(OLD_H) == 1
NEW_H = """## 1. CURRENT DELTA \u2014 R48 (21 Aug 2026), items Q1\u2013Q8 \u2014 ALL APPLIED

| item | subject | status |
|---|---|---|
| **Q1** | K6 admitted in three parts, none collapsed | **DONE** \u2014 D-003 \u00a72 |
| **Q2** | the three false statements corrected | **DONE** \u2014 declaration \u00a7A.5 + walk summary, `CEREMONY_COMMANDS.md` row |
| **Q3** | \u00a79.2/\u00a711 conflict recorded as a registration defect, \u00a70.2.2 l.107 quoted | **DONE** \u2014 D-003 \u00a72 |
| **Q4** | \u00a7A.1 item 2's model-family claim corrected; H2 + J3 re-grounded | **DONE** |
| **Q5** | transcription determination | **DONE \u2014 RE-DERIVED. Transcription REFUTED.** |
| **Q6** | limb (i) rekeyed | **DONE** \u2014 `(side, instrument, model family, horizon)` |
| **Q7** | post-fix trio registered ex ante | **DONE** \u2014 declaration \u00a7A.1 item 4 |
| **Q8** | H-L15 hardened **in the check** | **DONE** \u2014 self-check assertion (vii), now 7 |

### Q5 \u2014 RE-DERIVED, and the stated prior is defeated by mechanism

**The shuffle mean is not stochastic across runs.** `phase7_l2_sim.py` computes it over **fixed
seeds [42, 123, 456]** via `RandomState(seed).permutation` \u2014 deterministic by construction, so 32
byte-identical values are the EXPECTED output of a seeded re-run, not evidence of copying.

| leg | finding |
|---|---|
| producing script | trains its own models; **reads no Phase 6 output** (all 8 `phase6` refs are a rerun mode that WRITES) |
| Phase 6 predictions | **none exist** \u2014 Phase 7's 64 parquets cannot be copies |
| shuffle mean | fixed seeds \u2192 deterministic |
| empirical | AUC recomputed from Phase 7's own parquet = **0.966244**, matching the declared entry to 2.5e-7 |

**NOT ESTABLISHED:** no Phase 6 script survives on disk, so whether the agreement is deterministic
identity or independent convergence cannot be settled. **P8 therefore stands at 3 of 6.**

### THE CONSEQUENCE I OWE A CORRECTION FOR

**At R47/P7 I wrote that "the Phase 1 gate row FAILS ON TODAY'S ARTIFACT". That was wrong.** It
conflated two comparanda: limb (i) compares each entry against the **originating experiment's figure
for its own key** \u2014 Phase 6 \u2014 **not** against the retired 0.957/0.675 pair, which is what H2 retires
and is not limb (i)'s target. Against Phase 6 the pre-fix trio agrees to **|\u0394| \u2264 4.4e-5**. The row
does **not** fail today.

**And the honest consequence, now stated in J3 rather than buried:** with both operands frozen,
limb (i) **cannot fail on this artifact**, so under **SC-8(g)'s own rule** it is a **regression
test** and is labelled one. Limb (ii) likewise. **What still carries gate weight** in C1: the
separation floor (P6, author's, and live), **the sliced variant** (genuinely open \u2014 the padded
slicer is Phase 1 work that does not exist yet), the alignment controls, snapshot hashing, and the
\u00a710.0 ordering clauses. If P6's floor becomes a context figure with no pass/fail consequence, then
**none of this row's anchor content is failable on a frozen artifact** \u2014 a design that may be right
but should be chosen knowingly.

### REPO FILES EDITED THIS ROUND (first time this session `PREREG.md`'s neighbours moved)

| file | change |
|---|---|
| `AVAILABILITY_DECLARATION.md` | \u00a7A.5 corrected (Q2), walk-summary row (Q2), \u00a7A.1 item 2 corrected (Q4), **new \u00a7A.1 item 4** ex-ante registration (Q7) + the Q5 determination |
| `evidence/ceremony/CEREMONY_COMMANDS.md` | Phase 0 work-item row corrected (Q2) |
| `evidence/MANIFEST.sha256` | declaration line, ceremony line, pointer line \u2014 **rewritten in the same pass** (R15) |
| `evidence/fixture_spike/f4/DECLARATION_POINTER.md` | hash, bytes, as-of, provenance \u2014 same pass |
| `HISTORY.md` | **H-L15 hardened** (Q8) |

**`PREREG.md` STILL UNTOUCHED** \u2014 blob `75bd93dec436` == `prereg-v30:PREREG.md`.

### A LINE-ENDING FACT, RECORDED SO IT IS NOT REDISCOVERED

**This repository is natively CRLF** \u2014 `PREREG.md`, `DESIGN.md`, `HISTORY.md`, `PRACTICES.md`,
`declared_map.csv`, the declaration: all CRLF. Python `write_text` on Windows therefore matches the
convention and is correct. **The one exception is `evidence/MANIFEST.sha256`, which must be written
with `newline="\\n"`**: `sha256sum -c` takes a trailing CR as part of the filename, and a CRLF
manifest fails all 251 entries with "No such file or directory". Rewriting it with LF restored
251/251.

---

## 1b. R47 (21 Aug 2026), items P1\u2013P10 \u2014 all closed"""
t = t.replace(OLD_H, NEW_H, 1)

# refresh the fingerprint table
def h16(f):
    return hashlib.sha256((REPO / f).read_bytes()).hexdigest()[:16]

for f, old in [("HISTORY.md", "b0e40f30c8003cba"),
               ("AVAILABILITY_DECLARATION.md", "ddbf7f2d09842be0")]:
    line_old = "| `%s` | `%s` |" % (f, old)
    hits = [l for l in t.split("\n") if l.startswith("| `%s` | `%s`" % (f, old))]
    assert len(hits) == 1, "fingerprint row for %s: %d" % (f, len(hits))
    new_line = hits[0].replace(old, h16(f))
    # line count also moved
    t = t.replace(hits[0], new_line, 1)
    print("fingerprint refreshed: %-30s %s -> %s" % (f, old, h16(f)))

t = t.replace("| `AVAILABILITY_DECLARATION.md` | `%s` | 3796 |" % h16("AVAILABILITY_DECLARATION.md"),
              "| `AVAILABILITY_DECLARATION.md` | `%s` | 3854 |" % h16("AVAILABILITY_DECLARATION.md"), 1)
t = t.replace("| `HISTORY.md` | `%s` | 315 |" % h16("HISTORY.md"),
              "| `HISTORY.md` | `%s` | 316 |" % h16("HISTORY.md"), 1)

p.write_text(t, encoding="utf-8")
print("ROUND_STATE.md rewritten: %d lines" % len(t.split("\n")))
