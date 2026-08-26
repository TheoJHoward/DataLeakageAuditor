#!/usr/bin/env python3
"""§50 — withdraw R66 §0.1, restore the rule it displaced, relabel the check,
and put a cited ruling behind every standing constraint (§50.4)."""
import pathlib

p = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/ROUND_STATE.md")
t = p.read_text(encoding="utf-8")
i0 = t.index("## 1. STANDING CONSTRAINTS")
i1 = t.index("\n---", i0)

NEW = """## 1. STANDING CONSTRAINTS \u2014 EVERY ITEM CITES THE RULING THAT ESTABLISHED IT (\u00a750.4)

**\u00a750.4 rule: a constraint with no cited ruling is a working-session PREFERENCE and is labelled
one.** R66 \u00a70.1 would have failed at write time under this rule, which is why the rule exists.

| # | constraint | source ruling |
|---|---|---|
| 1 | **`PREREG.md` is edited ONLY by applying a diff the author has EXPLICITLY APPROVED.** A gate, not a prohibition. | **R20 / R24** (form (ii'), schema-in-PREREG) + the author's standing approval rule |
| 2 | **Evidence artifacts are never adjusted toward a decision.** | **R13** (`AVAILABILITY_DECLARATION.md` decision log) \u2014 *"the f3 manifest is NOT edited. Evidence artifacts are never adjusted toward a decision."* |
| 3 | **No hash may be carried forward; never adjust content toward a hash.** | **R15** (`CEREMONY_COMMANDS.md` \u00a73.1) + **R67 \u00a710.1**, which extends it to counts |
| 4 | **Nothing executes past a HALT. Report and stop.** | *no ruling \u2014 **WORKING-SESSION PREFERENCE**, labelled as such* |

### WITHDRAWN \u2014 R66 \u00a70.1, on 25 August 2026 (\u00a750.1)

> ~~"`PREREG.md` is not edited. Not one byte."~~

**Withdrawn by the author.** It was presented as a restatement of settled design and was not one:
it **contradicted R20 and R24**, which had already ruled that `PREREG.md` gains the SCHEMA and that
the declaration is not a normative annex. **It made a Class C amendment impossible by
construction** \u2014 the amendment's whole content is new normative text in `PREREG.md`.

**Consequence, recorded rather than smoothed over: seven rounds (R66\u2013R72) ran under a constraint
that made the round's own goal unreachable**, and `PREREG.md` byte-identity was reported GREEN every
one of those rounds **while byte-identity was the defect**. The author wrote it once; **this file
carried it forward seven times under a heading claiming it overrode everything else**, and never
checked it against R20 or R24, which sat in the same package.

### THE BYTE-IDENTITY CHECK STAYS \u2014 RELABELLED (\u00a750.3)

**Same measurement. Honest label.** It does NOT mean "the invariant holds". It means:

> **THE APPROVED DIFF HAS NOT YET BEEN APPLIED.**

`git hash-object PREREG.md` == `git rev-parse prereg-v30:PREREG.md` \u2192 blob `75bd93dec436\u2026`.
**On application this flips to an EXPECTED INEQUALITY** against a stated new blob, and equality at
that point becomes the failure. Report it in whichever direction the state calls for; never report
it as an unqualified invariant again.
"""

t = t[:i0] + NEW + t[i1:]
p.write_text(t, encoding="utf-8")
print("ROUND_STATE \u00a71: R66 \u00a70.1 withdrawn; rule restored; check relabelled; all 4 constraints sourced")
