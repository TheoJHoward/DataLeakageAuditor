#!/usr/bin/env python3
"""D1, second half: leave exactly ONE copy of SC-12(w)'s applied text.

Which survives, and why. `SCHEMA_SET_FINAL.md` survives as the single applied text,
because it is the file the ceremony applier reads and the only one whose contents
land in `PREREG.md`. `Y3_WAIVED_ENTRY_CONDITION.md` is the design record — the three
candidates, the judge panel, the non-weakening argument, the ledger placement and the
residual risks — and it keeps all of that. What it stops carrying is a second copy of
the clause text, because two copies of a rule with no canonical source is the exact
shape PREREG §0.2.1 exists to forbid, and it is what let bound (6) go stale in one
copy while the other was corrected.
"""

import pathlib
import re

D = pathlib.Path(
    "C:/Users/ttbea/AppData/Local/Temp/claude/"
    "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
    "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")
Y3 = D / "Y3_WAIVED_ENTRY_CONDITION.md"

POINTER = """## 1-2. THE CLAUSE, AND WHAT IT DOES NOT PERMIT — MOVED, NOT RESTATED

**The applied text of SC-12(w), limbs (w1)-(w7) and its closing "What this limb does NOT permit"
block, lives in exactly one place: `SCHEMA_SET_FINAL.md`, inside SC-12.** It is not reproduced here.

**Why it moved (DELTA R37/D1).** This file carried a second copy of the clause. The two drifted:
the applied text gained the \u00a78.3 line-929 hunk that DELTA R35/B4 ordered, while this file's bound
(6) still read *"alters no assertion in \u00a78.3"* \u2014 which that hunk falsifies. One rule with two copies
and no canonical source is the shape \u00a70.2.1 exists to forbid, and it produced exactly the failure
\u00a70.2.1 predicts: a correction applied to one copy and not the other, with nothing to say which
governed. The applied text is now single-sourced; this file cites it.

**What changed in the surviving copy, recorded so the change is auditable rather than silent:**

- **Bound (6) rewritten.** It previously claimed the limb *"amends no other coverage state's entry
  condition, moves no boundary in \u00a78.2, and alters no assertion in \u00a78.3."* The third clause was
  false. It now states that the limb reaches \u00a78.3 in exactly one way and deliberately \u2014 `waived`
  joins `assert_audit_complete()`'s failure set at line 929 \u2014 and that this is the whole of its
  reach.
- **The \u00a78.3 asymmetry is now argued inside the clause** (DELTA R37/D6), not left to apparatus:
  `unscored` is deliberately **not** added to that failure set, because `unscored` is a *permitted*
  state that honest coverage accounting produces, while `waived` is *prohibited* by (w1) and so a
  report emitting it is non-conforming on its face. A prohibition no assertion tests is not
  enforced; a permitted state that failed an assertion would punish correct reporting.

**What this file still carries, and still governs:** the three candidate drafts and why two were
rejected (\u00a74), the judge-panel scores (\u00a74 of the round report), the non-weakening argument tested
limb by limb (\u00a75), the ledger placement reasoning (\u00a76), and the residual risks (\u00a77). Where this
file's *reasoning* and the applied text disagree, the applied text governs and this file is the
record of how it was reached.

"""

s = Y3.read_text(encoding="utf-8")
m = re.search(r"^## 1\. THE CLAUSE.*?(?=^## 3\. DATA THE DECLARATION MUST SUPPLY)",
              s, re.S | re.M)
assert m, "could not locate sections 1-2 of Y3"
old = m.group(0)
print(f"  replacing {old.count(chr(10))} lines of duplicated clause text")
Y3.write_text(s[:m.start()] + POINTER + s[m.end():], encoding="utf-8", newline="")

t = Y3.read_text(encoding="utf-8")
print(f"  Y3 now: {t.count(chr(10))} lines")
for label, pat in (("(w1) limb text", "(w1) THE CONDITION"),
                   ("bounds block", "What this limb does NOT permit"),
                   ("stale bound (6)", "alters no assertion in \u00a78.3")):
    print(f"  {label:18s} occurrences in Y3: {t.count(pat)}")
