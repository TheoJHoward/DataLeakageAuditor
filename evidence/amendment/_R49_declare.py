#!/usr/bin/env python3
"""DELTA R49/R5 - declare SC-4(k)'s population change so N2 can absorb it."""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ADD = """

---

## R49/R5 \u2014 SC-4(k): the criterion-1 floor and the manifest reconciliation

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 \u2014 THE CLAUSE \u2014 SC-4 | 390\u2013474 -> 390\u2013509 | `4a2c05d77a08` -> `b286d4934a01` | new limb (k), 35 lines |

**What changed.** SC-4 ran (a)\u2013(j) and **nothing floored the scored population**. N is defined as
the length of the REQUIRED list, but no clause required that list to be non-empty \u2014 so criterion 1
was satisfiable by a declaration that classed almost everything OUT OF JURISDICTION or UNSCORED.
The schema set already contained the closing sentence, at **SC-13b(b1)**, roughly 500 lines away
and applied to a branch that is switched off. Three clauses blocked importing it: **SC-4(g)** lets a
unit hold no gate class at all, **SC-3(c)** hands the scored population to the declaration, and
**SC-4(a)** forbids any other classification from entering a criterion \u2014 which bars the very check
that closes the hole.

**(k1) the floor.** Non-empty on every declared side; STOP otherwise; lifted only by supplementing
and re-freezing under \u00a711 \u2014 SC-13b(b1)'s own remedy, not a new one. **Non-emptiness is the whole
floor** because any minimum above zero would be a threshold read off this fixture's own
distribution, which \u00a77.0 forbids. That is the same reasoning that ruled P6 at R49/R1.

**(k2) the reconciliation.** Per unit, against the manifest's independently-leaking-source list,
every difference named with the registered predicate of (b) that produced its class. A count does
not satisfy it.

**(k3) the carve-out**, and it is load-bearing: *"a reconciliation published under this limb is a
disclosure, not a classification entering a criterion, denominator, or count."* Without it (k2)
contradicts (a).

**(k4) the failure condition**, stated because R49/R2's refined SC-8(g) requires it, and classified:
**a live gate item, not a regression guard.**

**Does it weaken anything?** No. It adds a STOP condition and a publication duty, and removes none.

**Is it satisfied today? NO \u2014 and that is the point of drafting it.** The declaration publishes
\u00a7A.6.5, a per-unit cross-tabulation of the construction-SOURCE cut against the gate cut. **That is a
different pair of partitions.** No per-unit reconciliation against the manifest's leaking-source
list exists anywhere in the declaration. Computed this round from
`f3\\fixture_manifest_DRAFT.json` joined to \u00a7A.6.5's gate column, it would show:

```
25 LEAK-SOURCE  =  11 REQUIRED  +  13 OUT OF JURISDICTION  +  1 UNSCORED
 6 DESCENDANT   =   5 OUT OF JURISDICTION + 1 UNSCORED
 4 CLEAN        =   4 OUT OF JURISDICTION
                                                    35 total, both cuts
```

**Fourteen units** the manifest calls leaking sources are not classed REQUIRED \u2014 thirteen of them in
a class where **a finding on them is a false positive**: `mid_return_{1,5,10,30}s`, `bid_size_1`,
`ask_size_1`, `total_bid_depth`, `total_ask_depth`, `book_slope_bid`, `book_slope_ask`,
`spread_ticks`, `tick_direction`, `weighted_mid`, plus `buy_volume_10s` UNSCORED under \u00a7C.4(a).
**The data to satisfy (k2) exists; the publication does not.**

**Verification owed (N5).** New normative text in the acceptance gate. Drafted and mechanically
checked; **not** read by any non-author, and no composed read of \u00a76.2 as amended.
"""

p = D / "_POPULATION_CHANGES.md"
t = p.read_text(encoding="utf-8")
assert "R49/R5" not in t, "already declared"
p.write_text(t.rstrip() + ADD, encoding="utf-8")
print("declared: %d lines" % len(p.read_text(encoding='utf-8').split("\n")))
