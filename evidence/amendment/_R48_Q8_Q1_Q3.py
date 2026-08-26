#!/usr/bin/env python3
"""DELTA R48 - Q8 (harden H-L15's text), Q1 (K6 admitted in three parts),
Q3 (the §9.2/§11 conflict recorded as a registration defect).
"""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad")

# ------------------------------------------------------------------ Q8: H-L15
h = REPO / "HISTORY.md"
t = h.read_text(encoding="utf-8")
OLD = "Both were fixed by making the assertion structural rather than textual."
assert t.count(OLD) == 1, "H-L15 tail match %d" % t.count(OLD)
NEW = (OLD + " **Hardened 21 August 2026 (R48/Q8), after the shape "
 "recurred four times in a single workflow.** Four independent absence findings, each reported at "
 "PROVEN confidence, held that the \u00a79.2 prior-art comparison set did not exist and that no tool had "
 "ever been run against one. All four were wrong: the set exists, and eleven tools were run against "
 "it on 14 August 2026. Every one of the four declared a search population that **excluded the "
 "active drafting root the round was working in** \u2014 one of them stopped a single directory level "
 "above it. **A stated population is not a proof of coverage**, and the four were not careless in "
 "any way this lesson, as previously written, would have caught: they each named what they searched. "
 "An absence finding now states the population it searched **and shows that population included the "
 "root the round declares itself to be working in**; where the claim is unscoped \u2014 asserting that a "
 "thing exists nowhere, rather than that it is absent from a named artifact \u2014 naming that root is "
 "required rather than optional. **The requirement now lives in the check that scores absence "
 "claims, not only in this entry.** That is the whole point of the hardening: this lesson had "
 "already been written, and written correctly, and it did not prevent the recurrence. **A rule that "
 "can only be complied with by remembering it is a rule that will be forgotten.**")
t = t.replace(OLD, NEW, 1)
h.write_text(t, encoding="utf-8")
print("HISTORY.md: H-L15 hardened (%d lines)" % len(t.split("\n")))

# ------------------------------------------------------------------ Q1 + Q3
d = SCR / "ceremony" / "DEVIATIONS_D003_DRAFT.md"
x = d.read_text(encoding="utf-8")
MARK = "## 2. WHAT THIS ENTRY DOES NOT DECIDE"
i = x.index(MARK)
NEW2 = """## 2. THE AUTHOR'S DECISIONS \u2014 TAKEN AT DELTA R48

### Q1 \u2014 K6 IS ADMITTED, IN THREE PARTS THAT MAY NOT BE COLLAPSED

**(a) Admitted to the Phase 0 record AS EVIDENCE.** D-003 above states exactly what conformed \u2014 the
ordering, corroborated by a hash chain independently of the clock \u2014 and exactly what did not \u2014 the
commitment clause, breached and uncurable for `prereg-v30`.

**(b) IT DOES NOT SATISFY \u00a79.2.** \u00a79.2 remains **un-run in its registered form**. The
acceptance-fixture half never ran. **\u00a710.1 criterion 3 remains unevaluated for every rostered tool.**
**No clause, ledger row, work-item table or disclosure may imply otherwise** \u2014 including the Phase 0
work-item row in the ceremony package, which now states both halves rather than flipping to "done".

**(c) ITS RESULTS ARE UNVERIFIED.** K6 was drafted, run, scored and written up by a single agent, and
no other party has checked it. **Before any K6 result is cited load-bearing \u2014 the C6
five-tools-zero-hits result included \u2014 it gets independent re-verification by a party that did not
produce it.** This project has already measured the calibration case: a lone producer's clean report
of its own work. K6's author reports five harness bugs found and fixed, every one of which would
have flattered this project; that is the right disclosure and also the reason a sixth cannot be
assumed absent.

### Q3 \u2014 THE \u00a79.2 / \u00a711 CONFLICT IS A REGISTRATION DEFECT, NOT RESOLVED IN v30a

**Recorded, not cured**, alongside the twin-criterion-5 defect and \u00a710.1's missing third state.
Resolving it means choosing which registered clause governs, which is a semantic change with
knock-ons; its practical consequence is already recorded in D-003 above.

**The route, quoted so a future amendment starts from the text rather than rediscovering it \u2014
`PREREG.md` \u00a70.2.2 line 107:**

> A post-tag finding that cannot cite a stated assumption\u2026 is a specification defect. It gets a loud
> `DEVIATIONS.md` entry, and if it changes what any published number means, an amended registration
> under the class C rule.

**The conflict.** \u00a79.2 (line 973) requires the prior-art comparison set to be "committed with this
protocol". \u00a711 item 1 (line 1048) enumerates the first commit's contents as a **closed list** \u2014
`PREREG.md`, `DESIGN.md`, `HISTORY.md`, an empty `DEVIATIONS.md`, `PARKING_LOT.md`, a placeholder
`VALIDATED_CONFIG.toml`, `tools/check_registration.py`, `protocol/runtime_reference.py`, and
`tests/registration/` \u2014 which does not include a comparison set. **Both are inside the signed hash
of `prereg-v30`. No single first commit could have satisfied both as drafted.**

**Which limb of line 107 applies is left open**, deliberately: its test is whether the defect
"changes what any published number means", and nothing is published yet, so the artifacts do not
decide it. A future amendment must give the state a single canonical disposition and make one clause
cite the other.

## 3. WHAT IS STILL NOT DECIDED HERE

The **wording** of the three corrections was settled at R48/Q2 and applied; the **substance** of
whether K6's individual findings hold is expressly reserved to Q1(c)'s independent re-verification.
Nothing in K6 is cited load-bearing anywhere in the registration, the declaration, or the ceremony
package as of this entry.

"""
x = x[:i] + NEW2 + x[x.index("## 3. IF K6 IS ADMITTED"):].replace(
    "## 3. IF K6 IS ADMITTED \u2014 WHAT THE CEREMONY MUST ADD",
    "## 4. WHAT THE CEREMONY MUST ADD (K6 IS ADMITTED \u2014 Q1(a))", 1)
d.write_text(x, encoding="utf-8")
print("DEVIATIONS_D003_DRAFT.md: Q1 three parts + Q3 recorded (%d lines)" % len(x.split("\n")))
