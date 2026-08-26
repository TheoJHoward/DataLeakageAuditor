#!/usr/bin/env python3
"""§49 — record the author's blocker-1 routing decision, at the location §0 requires."""
import pathlib

CC = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                  "evidence/ceremony/CEREMONY_COMMANDS.md")
s = CC.read_text(encoding="utf-8")
EM = "\u2014"

ANCHOR = "**Nothing in this file may run until that is on the record.**"
assert s.count(ANCHOR) == 1, "anchor match %d" % s.count(ANCHOR)

RECORD = ANCHOR + """

### RECORDED """ + EM + """ THE AUTHOR'S ROUTING DECISION, 25 AUGUST 2026

**Branch (b) is chosen.** Recorded here, before C5, as §0 requires. Verbatim, attributed:

> **Blocker 1, §10.0 routing. Recorded by the author, 25 August 2026:** the §9.2 cross-tool
> comparison and the licence check gate **PHASE 1 ENTRY**, not the `prereg-v30a` amendment tag.
> H-34's verdict is the sign-off the tag requires. **Both items are carried forward as named open
> obligations that must be discharged before Phase 1 entry; neither is waived, satisfied, or
> weakened by the tag.** *Re-fire condition:* if a tool implementing runtime probing against a
> declared per-cell availability model surfaces before Phase 1 entry, the §10.1 gate **re-fires**
> and this routing does not shield it.

**Effect on this file.** The §0 precondition is satisfied: a statement is on the record. **C5 is
unblocked** on this ground. Every other §0 blocker stands unchanged """ + EM + """ this decision routes the
kill gate and does nothing else.

**What this is NOT.** It is not the §10.1 attestation, and it is not a finding that the gate does
not fire. It is a **routing decision** about which milestone the two outstanding Phase 0 work items
gate. *(Recorded because earlier rounds of this working session characterised blocker 1 as the
§10.1 attestation itself; that characterisation was wrong and is corrected here and at
`COMMIT_PLAN.md` §8.)*
"""

s = s.replace(ANCHOR, RECORD, 1)
CC.write_text(s, encoding="utf-8")
print("CEREMONY_COMMANDS.md \u00a70: routing decision recorded before C5")
