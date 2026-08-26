#!/usr/bin/env python3
"""DELTA R58/W4 - draft the disclosures block, all seven, on the face of v30a.

FOUND WHILE DOING IT: the block did not exist. P9's six were established as FACTS at R47
and recorded in ROUND_STATE, and never drafted into the amendment. Worse, the line-459
marker landed at R54/W3 already says "carried as a disclosure on the face of the amendment
(R54/W4, disclosure 7)" - a forward reference to a block that was not there. Drafting the
block closes both.

WHERE. Appended to the SSAB amendments-block recording text, claimed by H2 - the block a
reader opens to learn what the amendment does. Not a new hunk: a second SSA row for H2,
which already carries two rows.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

BLOCK = """**WHAT THIS AMENDMENT DISCLOSES \u2014 seven things a reader would otherwise have to reconstruct.**

**1. This amendment changes a criterion of a gate that was already signed off.** `HISTORY.md`
**H-34**, dated **12 August 2026**, recorded the \u00a710.1 kill-gate sign-off with the verdict *"the
project proceeds"*. \u00a710.1's criterion 3 is amended here, after that date. \u00a70.2.1's ex-ante rule
makes the **ordering** the disclosable fact.

**2. The gate is harder to satisfy on net, and this is where.** \u00a76.2 criterion 3's corrected-side
limb moves from *silence* to *matching the declared map*, which is forced: the registered criterion
is falsified by the fixture's own measurement (18 of 48 instrument-months carry a non-zero corrected
count). **A contaminated-side tightening drafted alongside it is WITHDRAWN from this amendment**
(H-39), because its reason appeared nowhere in the clause carrying it.

**3. \u00a710.1 criterion 3 has never been evaluated, for any candidate, under either text.** No
candidate was run against either fixture side. **\u00a79.2's comparison-set surface DID run**, on 14
August 2026, over eight hand-written cases and eight clean paired controls \u2014 but it is committed
nowhere, so \u00a79.2's *"committed with this protocol"* is breached and uncurable for `prereg-v30`, and
**\u00a79.2 remains un-run in its registered form**. The acceptance-fixture surface was not run. The
kill-gate verdict rests on criterion 1. Recorded at `DEVIATIONS.md` **D-003**.

**4. Whether the kill gate is re-run under the amended criterion is NOT REGISTERED, and is an open
author decision.** No clause of this amendment creates such an obligation, and H-34's own re-fire
condition triggers on **a new tool surfacing**, not on **the criterion changing**. A reader must not
infer that amending criterion 3 re-opens the gate.

**5. The map ships; the fixture does not.** The declared ground-truth map is committed with this
registration and is publicly reachable at the tag. **The acceptance fixture is not** \u2014 it is 64
stored-prediction parquets per side, outside the repository, and **no clause requires publishing
it**. So a third party can read the map, the declaration and any published reconciliation, and
**cannot independently run a candidate against `fixture_contaminated` / `fixture_corrected`**.
Criterion 3 is not third-party evaluable today, and this amendment does not change that.

**6. \u00a710.1 registers no third state.** *Partial satisfaction* is defined nowhere in the corpus, so a
criterion that **could not be evaluated** is indistinguishable from one **evaluated NO**, and both
default to proceed. Given disclosure 3, that is not hypothetical \u2014 it describes what already
happened. **Recorded as a registration defect for a future amendment** (H-38), alongside the
twin-criterion-5 entry; this amendment does not widen its scope to cure it.

**7. Criterion 1's effective requirement REVERSES on 14 of 25 leaking-source columns, and the
registered text of line 459 does not move.** The fixture manifest classes **25** of the 35 fed
columns as leaking sources. Under the SC-4(b) partition **11** are REQUIRED \u2014 absence is a miss \u2014
while **13** are OUT OF JURISDICTION and **1** is UNSCORED, and on an OUT OF JURISDICTION column an
availability-class finding is a **FALSE POSITIVE**. So on 14 of those 25 the gate's demand inverts:
*absence is a miss* becomes *a finding fails the gate*. **A reader comparing v30 and v30a
byte-for-byte at line 459 will see no change and conclude wrongly.** The narrowing is made under the
class C rule, which permits it; \u00a70.2.1 line 97 measures at the outcome, and at the outcome this is a
supersession.

**These seven are disclosed because the record should not have to be reverse-engineered to find
them.** Each is verifiable from artifacts this registration commits, except where disclosure 5 says
otherwise."""

ssf = D / "SCHEMA_SET_FINAL.md"
s = ssf.read_text(encoding="utf-8")
MARK = "\n\n## \u00a710.1 LINE 1022 \u2014 THE KILL-GATE CRITERION 3 PAIR"
assert s.count(MARK) == 1, "insertion point match %d" % s.count(MARK)
assert "WHAT THIS AMENDMENT DISCLOSES" not in s, "already drafted"

quoted = "\n".join(("> " + x).rstrip() for x in BLOCK.split("\n"))
NEWSEC = ("\n---\n\n## \u00a7AC \u2014 THE v30a DISCLOSURES BLOCK (drafted R58/W4)\n\n"
          "Appended to the \u00a7AB amendments-block recording text and claimed by the same hunk. "
          "Disclosures 1\u20136 were established at R47/P9 and recorded only in the round state until "
          "now; **the block itself did not exist**, and the line-459 marker already referred to "
          "\u201cdisclosure 7\u201d. Both are closed here.\n\n"
          + quoted + "\n")
s = s.replace(MARK, NEWSEC + MARK, 1)
ssf.write_text(s, encoding="utf-8")
print("SCHEMA_SET_FINAL.md: \u00a7AC disclosures block added (%d quoted lines)"
      % len(quoted.split("\n")))

p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
tgt = [h for h in d["hunks"] if "v30a amendments (class C under" in (h.get("operative_text") or "")]
assert len(tgt) == 1, "H2 match %d" % len(tgt)
tgt[0]["operative_text"] = tgt[0]["operative_text"].rstrip() + "\n\n" + BLOCK
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("H2 operative_text extended with the disclosures block")
