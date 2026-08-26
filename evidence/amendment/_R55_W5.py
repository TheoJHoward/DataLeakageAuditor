#!/usr/bin/env python3
"""DELTA R55/W5 - strike the withdrawn model-family claim from OPERATIVE text.

WHY IT LANDED PARTIALLY, which is the part worth recording. H10 carries the claim in
TWO fields: `justification` (commentary about the hunk) and `operative_text` (the text
that lands in PREREG.md). At R48/Q4 I corrected the justification and left the operative
text, then wrote into the justification that the claim "is struck from both". So the
falsified claim survived in the ONLY field that ships, under a sentence asserting it had
been removed - which is worse than not correcting it, because the surviving instance now
reads as verified.

The general shape: a correction applied to the field a reviewer READS while the field
that SHIPS is left alone. Commentary and operative text are different objects and a
correction to one is not a correction to the other.

WHY NO EXISTING CHECK SAW IT. The provenance check compares hunk against source. Here
source and hunk AGREE - both carry the withdrawn claim - so coverage is 100% and the span
is intact. A provenance check is blind to source and hunk agreeing on withdrawn text, by
construction. The instrument that catches it is a register of withdrawn claims asserted
against operative text, added as `_withdrawn_claims.py`.
"""
import json
import pathlib

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

OLD = ("*Retired because no horizon of the declared fixture reproduces the registered pair, and "
       "because the anchor's model family changed \u2014 both facts, and the replacement entries "
       "themselves, are instances and are recorded in the declaration (\u00a7A.1).")
NEW = ("*Retired because no horizon of the declared fixture reproduces the registered pair on both "
       "sides (\u00a7A.1 item 1) \u2014 that fact, and the replacement entries themselves, are instances and "
       "are recorded in the declaration. **The clause \"and because the anchor's model family "
       "changed\" stood here until R55/W5 and is struck: it is false against its own cited source, "
       "which names six architectures with LightGBM listed first, and \u00a7A.1 item 2 was corrected on "
       "21 August 2026 to say so.**")

# ---- 1. the source of record -------------------------------------------------
src_p = D / "PREREG_v30a_DIFF.md"
s = src_p.read_text(encoding="utf-8")
assert s.count(OLD) == 1, "source match %d" % s.count(OLD)
src_p.write_text(s.replace(OLD, NEW, 1), encoding="utf-8")
print("PREREG_v30a_DIFF.md : operative text corrected (the source of record)")

# ---- 2. the hunk, from the SAME string ---------------------------------------
p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
n = 0
for h in d["hunks"]:
    op = h.get("operative_text") or ""
    if OLD in op:
        h["operative_text"] = op.replace(OLD, NEW, 1)
        n += 1
assert n == 1, "hunk operative_text match %d" % n
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("H10 operative_text  : corrected from the same string")

# ---- 3. the justification's own false claim of completion --------------------
FALSE = "and is struck from both."
TRUE = ("and is struck from the justification. **It was NOT struck from the operative text at that "
        "time \u2014 only from this commentary \u2014 so the falsified clause shipped for two further rounds "
        "under a sentence saying it had been removed. Struck from the operative text at R55/W5.**")
d = json.loads(p.read_text(encoding="utf-8"))
m = 0
for h in d["hunks"]:
    j = h.get("justification") or ""
    if FALSE in j:
        h["justification"] = j.replace(FALSE, TRUE, 1)
        m += 1
assert m == 1, "justification match %d" % m
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("H10 justification   : its own false completion claim corrected")
