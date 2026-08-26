#!/usr/bin/env python3
"""R49 addendum S4 - declare the S1-S3 revision of SC-4(k)."""
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

ADD = """

---

## R49 addendum S1\u2013S3 \u2014 SC-4(k) revised: which mechanism does what, and what a reader can check

| block | lines (before -> after) | sha12 before -> after | change |
|---|---|---|---|
| 8 \u2014 THE CLAUSE \u2014 SC-4 | 390\u2013517 -> 390\u2013543 | `28ebb287a9b2` -> `c20383d0f2a3` | (k) restructured; (k2)(i) added |

### S1 \u2014 the floor was reading as the protection, and it is not

**The defect in the previous draft.** (k) was headed *"THE REQUIRED LIST IS NON-EMPTY, AND THE
DENOMINATOR IS RECONCILED"* \u2014 two obligations in sequence, with nothing saying which stops what.
**A reader would take the floor for the protection.** It is not: **N \u2265 1 is satisfied by scoring a
single column.** A declaration could class thirty-four of thirty-five units out of the scored set
and clear (k1) intact.

**The fix.** (k) now opens by naming both failure modes and assigning an instrument to each: the
**degenerate** case (population empty) to the floor, the **gradual** case (narrowed unit by unit
until what survives is not worth scoring) to the reconciliation. (k1) is retitled **THE TERMINAL
BACKSTOP** and closes with *"it is not the protection and must not be cited as one"*; (k2) is
retitled **THE OPERATIVE MECHANISM**. Nothing about either obligation weakens \u2014 what changes is that
the clause now says which one is load-bearing.

### S3 \u2014 the adversarial test on (k), and the only bar that is registerable

**What (k) licensed, before this revision.** A declarer satisfies it by classing 24 of 25
manifest-classed leaking sources OUT OF JURISDICTION, naming each one and citing a registered
predicate for each \u2014 **on grounds of any quality whatever.** The predicate citation is a form
requirement; it constrains the shape of the answer, not its substance.

**Why the obvious fix is not available.** A requirement that grounds be *adequate*, *substantive* or
*well-founded* is unregisterable vagueness \u2014 no reader could apply it and no check could score it,
and writing it would be a constraint in appearance only. This registration already has a rule about
that shape of drafting.

**What is achievable, and is now required \u2014 (k2)(i): PROVENANCE.** Every ground **names the artifact
and the location within it** \u2014 file, and row, line, or field. A ground with an artifact behind it
can be looked up and disagreed with. **A ground with nothing behind it becomes visible as such**,
rather than reading as plausible. That is the whole of what the clause can achieve at this site, and
it is worth more than a bar nobody could apply.

### S2 \u2014 the verifiability limit, stated instead of implied

**Established at R47/P9 disclosure 5:** `n1\\declared_map.csv` is staged by the ceremony plan and
ships with the tag; **the acceptance fixture does not** \u2014 Artifact B is 64 parquets per side under
`results\\phase7*\\l2_predictions\\`, outside the repository, with no clause requiring publication.

**So (k3) now says what a reader can and cannot do.** Can check: **completeness** (every
manifest-classed leaking source accounted for), **internal consistency** (each ground citing a
registered predicate), **provenance** (each ground naming an artifact and location). **Cannot:**
independently verify any classification against the fixture's data. The limb is registered as **a
disclosure obligation with limited external verifiability**, in those words.

**Why this belongs in the clause rather than in a note.** An obligation that implies an audit the
reader cannot perform is the same defect class as an overstated availability claim \u2014 and this
project has already corrected one of those this round, at \u00a7A.1 item 2.

### S4 \u2014 the procedure was exercised, not assumed

The growth check **crashed** the first time it was asked to absorb a change this session
(`KeyError('lines')` \u2014 two enumerators, two schemas), and its MODIFIED pairing then **failed a
second time** when an earlier block's growth shifted a later modified block. Both are fixed and both
were found by running it. This pass: re-enumerated (33 blocks, delta reported \u2014 **1 modified, 25
re-anchored, 7 identical**), re-anchored **dry-run first** with 42 of 42 rows resolved and 0
unresolved, manifest row 8 extended to the block's new end, then refrozen against the declared hash
pair above.

**Verification owed (N5).** Unchanged and now larger: (k) is the biggest piece of new normative text
in the amendment and **no non-author has read the revised form.** The R49/R6 pass read the previous
draft and returned NOT_FIT on it; these revisions answer S1\u2013S3, not R6's blockers, which were
answered separately.
"""

p = D / "_POPULATION_CHANGES.md"
t = p.read_text(encoding="utf-8")
assert "R49 addendum S1\u2013S3" not in t
p.write_text(t.rstrip() + ADD, encoding="utf-8")
print("declared S1-S3 revision")
