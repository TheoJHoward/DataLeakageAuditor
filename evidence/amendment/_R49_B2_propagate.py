#!/usr/bin/env python3
"""DELTA R49 / R6 blocker B2 - the signable artifact still carried the WITHDRAWN C1.

THE DEFECT AND WHY NOTHING CAUGHT IT. J3 withdrew C1 and redrafted it. The redraft
lives in J3_C1_REDRAFT.md. The artifact is built from _X5_hunks_v2.json. H29's
operative_text was never updated, so every build since J3 has rendered the withdrawn
text - and every check stayed green, because the checks verify
manifest -> hunk -> artifact consistency and H29 is a MANIFEST SECTION-B hunk whose
source is a drafting round, not SCHEMA_SET_FINAL.md. **No check binds a section-B hunk
to its drafting document.** Eleven hunks carry that exposure. This script fixes H29;
_R49_B2_check.py adds the missing binding.

The gate cell is rebuilt from J3's operative row, read out of J3 rather than retyped,
so the two cannot disagree.
"""
import json
import pathlib
import re

D = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                 "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                 "8b1d67a4-ce4f-4c55-b09d-1c72e7b6b5e1/scratchpad/amendment")

# ---- read the redrafted row OUT OF J3, never retyped -------------------------
L = (D / "J3_C1_REDRAFT.md").read_text(encoding="utf-8").split("\n")
s = next(i for i, l in enumerate(L) if l.startswith("> \u00a710.0 ordering followed"))
e = next(i for i in range(s, len(L))
         if L[i].rstrip().endswith("clauses. Limbs (i) and (ii) are guards and are not counted toward it."))
row = " ".join(re.sub(r"^>\s?", "", x).strip() for x in L[s:e + 1]).strip()
row = re.sub(r"\s+", " ", row)
assert "architecture, horizon_s, tier" in row, "B3's key did not come through"
assert "SC-8(g)" not in row, "B1's phantom citation is still in the row"
assert "different model family" not in row, "B6's unreachable branch is still in the row"
assert "reproduces its declared anchor entry within" not in row, "B4's orphan tolerance survived"
print("redrafted gate cell read from J3: %d chars, all four blockers absent" % len(row))

# ---- rebuild the table row, keeping Phase / Work / Est. byte-identical -------
p = D / "_X5_hunks_v2.json"
d = json.loads(p.read_text(encoding="utf-8"))
target = [h for h in d["hunks"] if "registered acceptance interval" in (h.get("operative_text") or "")]
assert len(target) == 1, "C1 hunk match %d" % len(target)
h = target[0]
old = h["operative_text"]
cells = old.split("|")
assert len(cells) == 6, "expected 4 table cells, got %d" % (len(cells) - 2)
head = "|".join(cells[:4])          # leading empty + Phase + Work + Est.
h["operative_text"] = head + "| " + row + " |"
assert h["operative_text"].startswith("| **1** | Availability model and profiles"), "Phase/Work cells moved"
assert "registered acceptance interval" not in h["operative_text"]

h["what_changes"] = (
    "The Phase 1 gate cell is replaced. **Phase, Work and Est. are byte-identical; only the Gate "
    "cell changes.** The registered *\"both fixture AUCs reproduce within \u00b10.010, full and sliced\"* "
    "is replaced by: a two-limb reference anchor, **both limbs labelled REGRESSION GUARDS with what "
    "each guards against stated**; the separation as a **published context figure with no pass/fail "
    "consequence** (R49/R1); the sliced variant discharged and scored under \u00a76.2's own ex-ante rule; "
    "the alignment controls and snapshot hashing carried unchanged; and a closing sentence naming "
    "**which items carry the row's pass/fail evidence**.\n\n"
    "**PROVENANCE, and a defect this hunk carried until R49.** The text above is read directly out "
    "of `J3_C1_REDRAFT.md`'s operative row at build time. Until the R49/R6 verification, this hunk "
    "carried the **WITHDRAWN** C1 \u2014 the draft J3 replaced over four defects \u2014 and every build since "
    "J3 rendered withdrawn text into the signable artifact while every check reported green. The "
    "checks verify manifest \u2192 hunk \u2192 artifact; this is a manifest **section-B** hunk whose source is "
    "a drafting round rather than `SCHEMA_SET_FINAL.md`, and **no check bound it to that source.** "
    "Eleven hunks share the exposure; `_R49_B2_check.py` installs the binding.")
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("H29 rebuilt from the redraft; Phase/Work/Est. cells untouched")
print("  new gate cell: %d chars" % len(row))
