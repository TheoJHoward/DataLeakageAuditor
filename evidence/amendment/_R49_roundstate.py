#!/usr/bin/env python3
"""DELTA R49 - ROUND_STATE rewrite (R36: every round, before reporting)."""
import hashlib
import pathlib

SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")
REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")

p = SCR / "ROUND_STATE.md"
t = p.read_text(encoding="utf-8")

OLD = "## 1. CURRENT DELTA \u2014 R48 (21 Aug 2026), items Q1\u2013Q8 \u2014 ALL APPLIED"
assert t.count(OLD) == 1
NEW = """## 1. CURRENT DELTA \u2014 R49 (21 Aug 2026), items R1\u2013R7 \u2014 ALL APPLIED; TWO VERIFICATIONS RUNNING

| item | subject | status |
|---|---|---|
| **R1** | P6 ruled: separation is a **published context figure**, no pass/fail | **DONE** \u2014 J3 operative row + \u00a75(a); recorded as a **disclosed reduction** |
| **R2** | SC-8(g) refined: (g)(1) regression guard / (g)(2) decoration / (g)(3) name the evidence | **DONE** |
| **R3** | H-34 correction note | **DONE** \u2014 appended below the entry, dated 21 Aug, never as an edit |
| **R4** | independent re-verification of K6, C6 first | **DONE — C6 is OVERSTATED; five MORE harness bugs, all biased one way; the kill-gate verdict itself is ROBUST** |
| **R5** | **SC-4(k)** \u2014 the floor + the reconciliation | **DRAFTED AND LANDED IN SOURCE** |
| **R6** | N5 verification of J3 + SC-3(a) + SC-4(k), one pass | **RUNNING** |
| **R7** | LF-manifest fact recorded as ceremony-critical | **DONE** \u2014 X4 C2.3 **and** a runnable `C2d-0` gate |

### R5 \u2014 SC-4(k), the largest new normative text in the amendment

Built on the F7 draft (F1: a finding is not discarded because the round moved on), tightened three
ways. **(k1) the floor:** REQUIRED list non-empty on every declared side, STOP otherwise, lifted only
by supplementing and re-freezing under \u00a711 \u2014 SC-13b(b1)'s own remedy, which existed ~500 lines away
applied to a switched-off branch. **Non-emptiness is the whole floor** because any minimum above zero
would be read off this fixture's own distribution (\u00a77.0) \u2014 the same reasoning that ruled R1.
**(k2) the reconciliation:** per unit, against the manifest's leaking-source list, each difference
named with the registered predicate of (b) that produced it. **(k3) the carve-out**, load-bearing:
without it SC-4(a) forbids the very check that closes the hole. **(k4) the failure condition**, as
R2's refined SC-8(g) now requires, and the classification: **a live gate item, not a guard.**

**IT IS UNSATISFIED TODAY, and that is the point.** The declaration publishes \u00a7A.6.5 \u2014 a per-unit
cross-tabulation of the construction-SOURCE cut against the gate cut. **That is a different pair of
partitions.** Computed this round from `f3\\fixture_manifest_DRAFT.json` joined to \u00a7A.6.5's gate
column:

```
25 LEAK-SOURCE = 11 REQUIRED + 13 OUT OF JURISDICTION + 1 UNSCORED
 6 DESCENDANT  =  5 OUT OF JURISDICTION + 1 UNSCORED
 4 CLEAN       =  4 OUT OF JURISDICTION            35 total, both cuts agree
```

**Fourteen units** the manifest calls leaking sources are not classed REQUIRED, thirteen in a class
where **a finding on them is a false positive**. The data exists; the publication does not.

### R1 \u2014 the separation floor is gone, and that is a REDUCTION, disclosed

The registered v30 row required both 0.957 and 0.675 to \u00b10.010, which **entailed** a 0.282 gap \u2014 the
row's only separation test. It is removed and replaced with a published figure that decides nothing.
**Recorded in the clause, in \u00a75(a), and here**, because R47/P2's rule cuts both ways: a reduction
whose reason appears nowhere is the failure mode. Grounds: the AUC gap is a **fixture** property, the
amended gate scores findings against the map, and any floor but 0.282 is chosen from the data while
0.282 the fixture fails at all three horizons (0.034708 / 0.183464 / 0.177131).

### R2 \u2014 why SC-8(g) needed splitting

The first draft said only *"an item whose outcome is determined by the frozen artifact is not a gate
item"*. **Applied literally that deletes the anchor's substitution detector along with the
tautology.** One cannot fail while the artifact is correct; the other cannot fail at all. Both
directions are defects \u2014 deleting a guard removes a real detector of a swapped fixture; keeping
decoration inflates a row. H-L13's shape again: a rule written against one failure mode reaching
something it should not.

### APPARATUS: two more defects in my own tooling this round

**(a) The re-anchor under-shifted by one line.** The extracted marker had no trailing newline, so
GROWTH computed +34 where blocks moved +35, and all 29 re-anchored rows ended one line short. M6
caught it as 25 PARTIAL blocks. Corrected; the generic `_reanchor.py` now exists but **its boundary
arithmetic is still the weak point** \u2014 it PROVES text equality, which is why the error surfaced as a
partial rather than as a silent mis-claim.

**(b) I corrupted the source seam.** Concatenating the quoted blocks without a newline produced
`same set.>` inside SCHEMA_SET_FINAL.md. Found by the re-anchor's own proof (9350 vs 9352 chars),
repaired, and the marker re-extracted **from the file** rather than reconstructed from the script.

### REPO FILES EDITED THIS ROUND

| file | change |
|---|---|
| `HISTORY.md` | **H-34 correction note** (R3), below the entry, dated |
| `evidence/ceremony/CEREMONY_COMMANDS.md` | **`C2d-0`** line-ending gate (R7) |
| `evidence/MANIFEST.sha256` | ceremony hash rewritten same pass, **written LF** |

**`PREREG.md` STILL UNTOUCHED** \u2014 blob `75bd93dec436` == `prereg-v30:PREREG.md`.

---

## 1a. R48 (21 Aug 2026), items Q1\u2013Q8 \u2014 all closed"""
t = t.replace(OLD, NEW, 1)

def h16(f):
    return hashlib.sha256((REPO / f).read_bytes()).hexdigest()[:16]

for f, old, oldln, newln in [("HISTORY.md", "f4827623c73353cf", "316", "357")]:
    row = "| `%s` | `%s` | %s |" % (f, old, oldln)
    assert t.count(row) == 1, "fingerprint row %s: %d" % (f, t.count(row))
    t = t.replace(row, "| `%s` | `%s` | %s |" % (f, h16(f), newln), 1)
    print("fingerprint refreshed: %-14s %s -> %s" % (f, old, h16(f)))

p.write_text(t, encoding="utf-8")
print("ROUND_STATE.md rewritten: %d lines" % len(t.split("\n")))
