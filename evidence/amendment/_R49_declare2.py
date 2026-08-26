#!/usr/bin/env python3
"""DELTA R49 - declare the B5 and B7 population changes."""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ADD = """

---

## R49/R6 \u2014 blockers B5 and B7 from the N5 verification

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 \u2014 THE CLAUSE \u2014 SC-4 | 390\u2013509 -> 390\u2013517 | `b286d4934a01` -> `28ebb287a9b2` | (k2) rewritten (B5) |
| 30 \u2014 THE CLAUSE \u2014 SC-13c | 1414\u20131510 -> 1422\u20131522 | `cf421dcccf9e` -> `e53506718260` | (c5)(i) now cites instead of restating (B7) |

### B5 \u2014 SC-4(k2) made an uncommitted DRAFT a gate input

**The defect.** (k2) required a reconciliation against *"the manifest's
independently-leaking-source list"* and (k4) made its absence a gate failure. But
`f3\\fixture_manifest_DRAFT.json` carries `"manifest_status": "DRAFT - author review required"`;
the declaration's SC-8(a) freeze does not enumerate it; and the declaration **expressly withdraws
its leaking-source count from the arithmetic** \u2014 *"The manifest's independently-leaking-source
count 25 is NOT a frozen gate number."* SC-8(a): *"an object the gate consumes and the enumeration
omits is a defect in the enumeration."* **A complete reconciliation could be made incomplete by an
author review that is not a class C amendment.**

**The fix.** (k2) now names the **list** rather than the count, states that reading the list makes
neither the count a gate quantity nor admits it to a denominator, and requires the manifest to be
**enumerated in the SC-8(a) freeze** and **not `DRAFT` at the tag**. The pre-existing tension \u2014 the
count is already read for `total_fed_to_phase7` while not being frozen \u2014 is narrowed, not widened:
the two statements are now made to agree on the page.

### B7 \u2014 SC-13c(c5)(i) held a second, DIVERGENT copy of SC-3(a)'s indexing rule

**The defect, and it is the one \u00a70.2.1 line 77 exists for.** (c5)(i) declared that SC-3(b)'s
dispositions are *"held by citation and not restated here"* \u2014 and then, in the next clause,
**restated SC-3(a)'s indexing triple.** At R47/P5 I amended (a) to say the map artifact may carry
rows that are not cells of the map. **I did not touch the copy.** So the second copy went stale in
exactly the way the single-source rule predicts: it now describes an indexing rule (a) no longer
states alone.

**The fix.** (c5)(i) holds the map, its indexing, and what the publishing artifact may carry **all
by citation to SC-3(a), none restated**, with a dated note recording that the copy existed and how
it diverged. **Nothing about the kill gate's substance changes**; what changes is that there is now
one statement of the rule instead of two.

**The general lesson, recorded because it will recur.** Amending a clause that another clause
restates leaves a divergent copy **silently**. The R47/P5 edit passed every check at the time. Only
a composed read found it \u2014 which is the argument for N5's composed-read requirement existing at
all.

**Verification owed (N5).** Both edits are new normative text and neither has been read by a
non-author. They were made in response to a verification pass, which is not the same as having
passed one.
"""

p = D / "_POPULATION_CHANGES.md"
t = p.read_text(encoding="utf-8")
assert "R49/R6 \u2014 blockers B5 and B7" not in t
p.write_text(t.rstrip() + ADD, encoding="utf-8")
print("declared B5 and B7")
